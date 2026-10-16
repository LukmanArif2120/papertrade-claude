# W01 — Walk-forward optimization stop/exit/tempoh pegangan bagi setiap kaedah M.
# Spec: WFO/spec/SPEC_WFO_SISTEM_SWING.md. Enjin v1.2 diimport tanpa ubah.
#
# Guna:
#   python3 wfo.py senarai                 # kaedah layak dan status
#   python3 wfo.py jalan M30 M96 ...       # WFO kaedah tertentu (selari, maks 5 proses)
#   python3 wfo.py kelompok [5] [10]       # jalankan 10 kaedah BELUM seterusnya, 5 serentak
#   python3 wfo.py w01                     # WFO gabungan (entry turut dipilih)
import sys, os, json, time, importlib, traceback, warnings, subprocess
from collections import OrderedDict
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))                     # WFO/kod
REPO = os.path.join(ROOT, '..', '..')
KOD = os.path.join(REPO, 'BacktestShariah2', 'kod')                   # enjin v1.2 + kaedah (baca sahaja)
BARU = os.path.join(ROOT, '..', 'kaedah_baru')                      # calon K145+ (M115–M161), di luar imbasan harian
sys.path.insert(0, KOD); sys.path.insert(0, os.path.join(KOD, 'kaedah')); sys.path.insert(0, BARU)
import enjin
from enjin import atr
import enjin_laju

ENJIN = os.environ.get('WFO_ENJIN', 'laju')   # 'laju' (numba, disahkan setara v1.2) atau 'asal' (enjin v1.2)

DATA = os.path.join(REPO, 'data_mentah')
KELUAR = os.path.join(ROOT, '..', 'data')
BUANG8 = ['ASST', 'FCEL', 'MTDR', 'OVV', 'PR', 'SM', 'VAL', 'XENE']
DIKECUALI = {'M40': 'isyarat bergantung pada pra-simulasi 8 slot kaedah sendiri',
             'M45': 'isyarat bergantung pada pra-simulasi 8 slot kaedah sendiri'}
W01_ENTRY = ['M96', 'M30', 'M79', 'M111', 'M74', 'M05', 'M80', 'M37', 'M04']
LATIH_THN = 3
OOS_MULA = '2023-01-01'
PERCUBAAN = int(os.environ.get('WFO_PERCUBAAN', 150))
MDD_HAD = -0.35
N_MIN_LATIH = 30
HAD_HENTI = 0.85          # stop >= 0.85 x tutup (had global 15%)
SEMAK_POTONG = '2024-06-28'
CACHE_MAKS = 200          # had cache dagangan setiap kaedah (memori)
MASA_MAKS = 7200          # saat; proses satu kaedah dihentikan selepas ini
HAD_LANCAR = 4200         # saat; tiada kaedah baharu dilancarkan selepas ini (larian muat < 2 jam)
# Bar terakhir data dipotong dikecualikan: ~60 modul menolak entry jika buka esok <= henti (peraturan langkau
# pelaksanaan, tugasan_v3 §5) dan beberapa modul mengesan hujung minggu/bulan dengan bar berikutnya. Kedua-duanya
# hanya menyentuh bar terakhir; pandang ke hadapan sebenar (data > 1 bar ke hadapan) tetap dikesan pada bar lain.

STOPS = ([f'PCT{p}' for p in (6, 8, 10, 12, 15)] + [f'ATR{k}' for k in (1.5, 2, 2.5, 3, 3.5, 4)]
         + [f'LOW{n}' for n in (1, 5, 10)] + ['ASAL'])
EXITS = ['EMA10', 'EMA21', 'SMA20', 'SMA50', 'CHAN2', 'CHAN3', 'CHAN4', 'ASAL', 'TIADA']
TMAXS = [10, 21, 42, 63, 0]   # 0 = tiada had


# ---------- data ----------
def _bingkai(df):
    df = df.copy(); df['date'] = pd.to_datetime(df.date.astype(str))
    return {t: g.drop(columns='ticker').set_index('date').sort_index() for t, g in df.groupby('ticker')}

def muat_data(buang8=True):
    d = pd.concat([pd.read_csv(os.path.join(DATA, f'dataset_S{i}.csv')).assign(_set=f'S{i}') for i in range(1, 5)])
    subset = d.groupby('ticker')['_set'].first().to_dict()
    fr = _bingkai(d.drop(columns='_set'))
    if buang8:
        fr = {t: g for t, g in fr.items() if t not in BUANG8}
    idx = _bingkai(pd.read_csv(os.path.join(DATA, 'index_benchmark.csv')))
    return fr, idx, {t: s for t, s in subset.items() if t in fr}

def salin(fr):
    return {t: g[['open', 'high', 'low', 'close', 'volume', 'turnover']].copy() for t, g in fr.items()}


# ---------- komponen stop / exit ----------
def lajur_stop(g, kod, asal, a14=None):
    c = g.close
    if kod.startswith('PCT'): s = c * (1 - int(kod[3:]) / 100)
    elif kod.startswith('ATR'): s = c - float(kod[3:]) * (atr(g) if a14 is None else a14)
    elif kod.startswith('LOW'): s = g.low.rolling(int(kod[3:])).min()
    else: s = asal
    return np.maximum(s.astype(float).fillna(-np.inf), HAD_HENTI * c)

def lajur_exit(g, kod, asal_ex, asal_tg, a22=None):
    c = g.close; tg = pd.Series(np.nan, g.index)
    if kod.startswith('EMA'): ex = c < c.ewm(span=int(kod[3:]), adjust=False).mean()
    elif kod.startswith('SMA'): ex = c < c.rolling(int(kod[3:])).mean()
    elif kod.startswith('CHAN'): ex = c < g.high.rolling(22).max() - int(kod[4:]) * (atr(g, 22) if a22 is None else a22)
    elif kod == 'ASAL': ex, tg = asal_ex, asal_tg
    else: ex = pd.Series(False, g.index)
    return ex.fillna(False).astype(bool), tg

def sah(stop, exit_, tmax):
    return not (exit_ == 'TIADA' and tmax == 0)


# ---------- kaedah ----------
class Kaedah:
    """Isyarat entry sekali; dagangan bagi setiap gabungan dicache."""
    def __init__(self, mid, fr, idx, f=None):
        self.mid = mid; self.m = importlib.import_module(mid)
        if f is None: f = salin(fr); self.m.sedia(f, idx)
        f = {t: enjin.siap(g) for t, g in f.items()}
        self.f = f; self.warm = self.m.WARM; self.tmax_asal = self.m.TMAX
        self.cache = OrderedDict(); self.pcache = {}
        # lajur stop/exit dikira sekali bagi setiap kod
        a14 = {t: atr(g) for t, g in f.items()}; a22 = {t: atr(g, 22) for t, g in f.items()}   # dikira sekali
        self.st = {s: {t: lajur_stop(g, s, g.stop, a14[t]) for t, g in f.items()} for s in STOPS}
        self.ex = {e: {t: lajur_exit(g, e, g.exitc, g.tgt, a22[t]) for t, g in f.items()} for e in EXITS}
        self.asas = {t: g[['open', 'high', 'low', 'close', 'sig', 'rank']] for t, g in f.items()}
        if ENJIN == 'laju':   # tatasusunan bersambung, penukaran sama seperti enjin.trades
            self.susun = enjin_laju.Susun(f)
            self.st_a = {s: np.concatenate([v.astype(float).values for v in d.values()]) for s, d in self.st.items()}
            self.ex_a = {e: (np.concatenate([x.fillna(False).astype(bool).values for x, _ in d.values()]),
                             np.concatenate([tg.astype(float).values for _, tg in d.values()])) for e, d in self.ex.items()}

    def dagangan(self, stop, exit_, tmax):
        k = (stop, exit_, tmax)
        if k not in self.cache:
            if ENJIN == 'laju':
                ex, tg = self.ex_a[exit_]
                T = self.susun.dagangan(self.st_a[stop], tg, ex, tmax or None, self.warm)
            else:
                fr = {}
                for t, g in self.asas.items():
                    ex, tg = self.ex[exit_][t]
                    fr[t] = g.assign(stop=self.st[stop][t], exitc=ex, tgt=tg)
                T = enjin.trades(fr, tmax or None, self.warm)
            if len(T):
                T['ticker'] = T.ticker.astype('category'); T['why'] = T.why.astype('category')
            self.cache[k] = T
            if len(self.cache) > CACHE_MAKS: self.cache.popitem(last=False)
        else:
            self.cache.move_to_end(k)
        return self.cache[k]

    def dagangan_asal(self):
        if ENJIN == 'laju': return enjin_laju.trades_laju(self.f, self.tmax_asal, self.warm)
        return enjin.trades(self.f, self.tmax_asal, self.warm)


def semak_kaedah(mid, fr, idx, penuh=None):
    """Pulang None jika layak, atau sebab tidak layak (pandang ke hadapan / ralat).
    penuh: hasil sedia() atas data penuh jika sudah ada (elak kira semula)."""
    if mid in DIKECUALI: return DIKECUALI[mid]
    m = importlib.import_module(mid)
    pot = pd.Timestamp(SEMAK_POTONG)
    if penuh is None: penuh = salin(fr); m.sedia(penuh, idx)
    a = penuh
    b = salin({t: g[g.index <= pot] for t, g in fr.items() if (g.index <= pot).sum() > 0})
    m.sedia(b, {k: v[v.index <= pot] for k, v in idx.items()})
    beza = 0
    for t, g in b.items():
        g = g.iloc[:-1]
        x = a[t].loc[g.index]
        s1 = g['sig'].fillna(False).astype(bool) if 'sig' in g else pd.Series(False, g.index)
        s2 = x['sig'].fillna(False).astype(bool) if 'sig' in x else pd.Series(False, g.index)
        beza += int((s1 != s2).sum())
    return None if beza == 0 else f'pandang ke hadapan: {beza} isyarat berubah apabila data selepas {SEMAK_POTONG} dibuang'


# ---------- penilaian ----------
def potong(T, mula, akhir, fr):
    """Dagangan masuk dalam [mula, akhir]; posisi yang masih terbuka pada `akhir` ditutup pada tutup `akhir`
    (setara enjin apabila data berakhir pada `akhir`)."""
    T = T[(T.ent >= mula) & (T.ent <= akhir)]
    lps = T.ex > akhir
    if lps.any():
        T = T.copy(); T['why'] = T.why.astype(object)
        e = np.array([fr[t].open.at[d] for t, d in zip(T.ticker[lps], T.ent[lps])])
        z = [_tutup_akhir(fr, t, akhir) for t in T.ticker[lps]]
        c = np.array([x[0] for x in z])
        T.loc[lps, 'ret'] = c / e * (1 - enjin.COST) / (1 + enjin.COST) - 1
        T.loc[lps, 'ex'] = [x[1] for x in z]
        T.loc[lps, 'why'] = 'hujung'
    return T

_AKHIR = {}
def _tutup_akhir(fr, t, akhir):
    """(tutup, tarikh) bar terakhir saham t pada atau sebelum akhir (= fr[t].close[:akhir].iloc[-1])."""
    k = (t, akhir)
    if k not in _AKHIR:
        if len(_AKHIR) > 50000: _AKHIR.clear()
        s = fr[t].close[:akhir]; _AKHIR[k] = (s.iloc[-1], s.index[-1])
    return _AKHIR[k]

_PASARAN = {}
def pasaran(frw):
    """Pasaran (tarikh + matriks asof) dicache bagi setiap dict fr; rujukan disimpan supaya id tidak diguna semula."""
    k = id(frw)
    if k not in _PASARAN:
        if len(_PASARAN) > 8: _PASARAN.clear()
        _PASARAN[k] = (frw, enjin_laju.Pasaran(frw))
    return _PASARAN[k][1]

def lengkung(T, frw, mula):
    if len(T) == 0: return None
    cv = pasaran(frw).lengkung(T) if ENJIN == 'laju' else enjin.portfolio(T, frw)
    return cv[cv.index >= mula]

def ukur(cv):
    if cv is None or len(cv) < 20 or cv.iloc[-1] <= 0: return dict(cagr=-1.0, mdd=-1.0, thn_min=-1.0)
    cv = cv / cv.iloc[0]
    th = cv.resample('YE').last().pct_change()
    th.iloc[0] = cv.resample('YE').last().iloc[0] - 1
    return dict(cagr=enjin._cagr(cv), mdd=enjin._mdd(cv), thn_min=float(th.min()))

def suku_ujian(akhir_data):
    q = pd.period_range(OOS_MULA, akhir_data, freq='Q')
    return [(p.start_time, min(p.end_time.normalize(), akhir_data)) for p in q]


def pilih(kaedah_list, fr, mula_latih, akhir_latih, benih):
    """Optuna atas tetingkap latihan. kaedah_list: dict mid -> Kaedah."""
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    frw = {t: g[(g.index >= mula_latih) & (g.index <= akhir_latih)] for t, g in fr.items()}
    frw = {t: g for t, g in frw.items() if len(g)}
    rekod = []

    def obj(tr):
        mid = tr.suggest_categorical('entry', list(kaedah_list)) if len(kaedah_list) > 1 else next(iter(kaedah_list))
        s = tr.suggest_categorical('stop', STOPS); e = tr.suggest_categorical('exit', EXITS)
        x = tr.suggest_categorical('tmax', TMAXS)
        if not sah(s, e, x): return -9.0
        kk = kaedah_list[mid]; kc = (s, e, x, mula_latih)
        if kc not in kk.pcache:
            T = potong(kk.dagangan(s, e, x), mula_latih, akhir_latih, fr)
            kk.pcache[kc] = (len(T), ukur(lengkung(T, frw, mula_latih)) if len(T) >= N_MIN_LATIH else None)
        n, u = kk.pcache[kc]
        if u is None: return -9.0
        if u['mdd'] < MDD_HAD: return -9.0
        rekod.append(dict(entry=mid, stop=s, exit=e, tmax=x, n=n, **u))
        return u['cagr']

    st = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=benih))
    st.optimize(obj, n_trials=PERCUBAAN)
    if not rekod: return None
    R = pd.DataFrame(rekod).drop_duplicates(['entry', 'stop', 'exit', 'tmax'])
    return R.nlargest(10, 'cagr').sort_values(['thn_min', 'cagr'], ascending=False).iloc[0].to_dict()


def tumpuan(T):
    u = T.groupby('ticker').ret.sum(); pos = u[u > 0]
    return float(pos.max() / pos.sum()) if len(pos) and pos.sum() > 0 else np.nan

def metrik_oos(T, cv):
    if len(T) == 0 or cv is None: return dict(n=0)
    u = ukur(cv); w = T.ret > 0
    return dict(n=len(T), cagr=u['cagr'], mdd=u['mdd'], mar=u['cagr'] / abs(u['mdd']) if u['mdd'] < 0 else np.nan,
                win=float(w.mean()), avg=float(T.ret.mean()), hit10=float((T.mfe >= 0.10).mean()),
                ret10=float((T.ret >= 0.10).mean()), hari=float(T.days.mean()), tumpuan_maks=tumpuan(T))

def ew(fr, mula):
    s = pd.concat([g.close[g.index >= mula] / g.close[g.index >= mula].iloc[0]
                   for g in fr.values() if (g.index >= mula).any()], axis=1).ffill().mean(axis=1)
    return ukur(s)


def wfo(kaedah_list, fr, idx, subset, label):
    akhir = max(g.index.max() for g in fr.values())
    mula_oos = pd.Timestamp(OOS_MULA)
    pil = []; oos = []
    for n, (qa, qz) in enumerate(suku_ujian(akhir)):
        za = qa - pd.Timedelta(days=1); ma = pd.Timestamp(year=qa.year - LATIH_THN, month=qa.month, day=1)
        p = pilih(kaedah_list, fr, ma, za, 42 + n)
        if p is None:
            pil.append(dict(suku=str(qa.to_period('Q')), catatan='tiada gabungan sah')); continue
        T = kaedah_list[p['entry']].dagangan(p['stop'], p['exit'], int(p['tmax']))
        T = T[(T.ent >= qa) & (T.ent <= qz)]
        oos.append(T.assign(suku=str(qa.to_period('Q')), entry=p['entry']))
        pil.append(dict(suku=str(qa.to_period('Q')), latih=f'{ma.date()}..{za.date()}', **p))
    T = pd.concat(oos) if oos else pd.DataFrame()
    cv = lengkung(T, fr, mula_oos) if len(T) else None
    hasil = dict(id=label, oos=metrik_oos(T, cv), ew=ew(fr, mula_oos))
    for k in ('SPY', 'QQQ'):
        s = idx[k].close; hasil[k.lower()] = ukur(s[s.index >= mula_oos])
    # subset S1-S4: gabungan terpilih yang sama, alam subset
    sub = {}
    for sname in sorted(set(subset.values())):
        tk = sorted(t for t, s in subset.items() if s == sname); fs = {t: fr[t] for t in tk}
        Ts = T[T.ticker.isin(tk)] if len(T) else T
        cs = lengkung(Ts, fs, mula_oos) if len(Ts) else None
        sub[sname] = dict(cagr=ukur(cs)['cagr'], ew=ew(fs, mula_oos)['cagr'], n=len(Ts))
    hasil['subset'] = sub
    hasil['menang_ew_subset'] = int(sum(v['cagr'] > v['ew'] for v in sub.values()))
    return hasil, pd.DataFrame(pil), T, cv


def asal_oos(k, fr, mula):
    T = k.dagangan_asal(); T = T[T.ent >= mula]
    return metrik_oos(T, lengkung(T, fr, mula) if len(T) else None)


# ---------- larian ----------
def _simpan(label, hasil, pil, T, cv):
    os.makedirs(os.path.join(KELUAR, 'hasil'), exist_ok=True)
    b = os.path.join(KELUAR, 'hasil', label)
    with open(b + '.json', 'w') as f: json.dump(hasil, f, indent=1, default=lambda x: None if x != x else str(x))
    pil.to_csv(b + '_pilihan.csv', index=False)
    if len(T):
        T[['ticker', 'sig', 'ent', 'ex', 'ret', 'days', 'why', 'mfe', 'suku', 'entry']].round(5).to_csv(b + '_dagangan_oos.csv', index=False)
    if cv is not None:
        cv.round(5).rename('ekuiti').to_csv(b + '_ekuiti.csv')

def jalan_satu(mid):
    warnings.filterwarnings('ignore'); t0 = time.time()
    try:
        fr, idx, subset = muat_data()
        m = importlib.import_module(mid) if mid not in DIKECUALI else None
        penuh = None
        if m is not None: penuh = salin(fr); m.sedia(penuh, idx)
        sebab = semak_kaedah(mid, fr, idx, penuh)
        asas = dict(id=mid, nama=getattr(m, 'NAMA', ''), varian=getattr(m, 'VARIAN', ''))
        if sebab:
            _simpan(mid, dict(**asas, status='TIDAK LAYAK', sebab=sebab), pd.DataFrame(), pd.DataFrame(), None)
            return mid, 'TIDAK LAYAK', round(time.time() - t0)
        k = Kaedah(mid, fr, idx, penuh)
        hasil, pil, T, cv = wfo({mid: k}, fr, idx, subset, mid)
        hasil.update(asas, status='SIAP', beku=asal_oos(k, fr, pd.Timestamp(OOS_MULA)),
                     percubaan=PERCUBAAN, saat=round(time.time() - t0))
        _simpan(mid, hasil, pil, T, cv)
        return mid, 'SIAP', round(time.time() - t0)
    except Exception:
        os.makedirs(os.path.join(KELUAR, 'hasil'), exist_ok=True)
        with open(os.path.join(KELUAR, 'hasil', mid + '.json'), 'w') as f:
            json.dump(dict(id=mid, status='RALAT', sebab=traceback.format_exc()[-1500:]), f, indent=1)
        return mid, 'RALAT', round(time.time() - t0)

def semua_kaedah():
    f = os.listdir(os.path.join(KOD, 'kaedah')) + os.listdir(BARU)
    return sorted({x[:-3] for x in f if x.startswith('M') and x.endswith('.py')}, key=lambda x: int(x[1:]))

def status():
    out = {}
    for mid in semua_kaedah():
        p = os.path.join(KELUAR, 'hasil', mid + '.json')
        out[mid] = (json.load(open(p)).get('status', '?') if os.path.exists(p)
                    else 'SEDANG' if os.path.exists(os.path.join(KELUAR, 'hasil', mid + '.sedang')) else 'BELUM')
    return out

def jalan(mids, proses=5):
    """Satu subproses bagi setiap kaedah (proses yang mati tidak menggantung yang lain)."""
    giliran = list(mids); aktif = {}; mula = time.time()
    os.makedirs(os.path.join(KELUAR, 'hasil'), exist_ok=True)
    while giliran or aktif:
        if time.time() - mula > HAD_LANCAR: giliran = []
        while giliran and len(aktif) < proses:
            m = giliran.pop(0)
            if status().get(m) != 'BELUM': continue
            open(os.path.join(KELUAR, 'hasil', m + '.sedang'), 'w').close()
            aktif[m] = (subprocess.Popen([sys.executable, os.path.abspath(__file__), 'satu', m],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), time.time())
        time.sleep(5)
        for m, (pr, t0) in list(aktif.items()):
            if pr.poll() is None and time.time() - t0 > MASA_MAKS: pr.kill(); pr.wait()
            if pr.poll() is None: continue
            del aktif[m]
            try: os.remove(os.path.join(KELUAR, 'hasil', m + '.sedang'))
            except OSError: pass
            f = os.path.join(KELUAR, 'hasil', m + '.json')
            if pr.returncode != 0 or not os.path.exists(f):
                os.makedirs(os.path.dirname(f), exist_ok=True)
                json.dump(dict(id=m, status='RALAT', sebab=f'proses mati (kod {pr.returncode}; mungkin memori/masa)'), open(f, 'w'))
            print(f"{m}\t{json.load(open(f)).get('status')}\t{round(time.time() - t0)}s", flush=True)

def jalan_w01():
    warnings.filterwarnings('ignore'); t0 = time.time()
    fr, idx, subset = muat_data()
    ks = {m: Kaedah(m, fr, idx) for m in W01_ENTRY if semak_kaedah(m, fr, idx) is None}
    hasil, pil, T, cv = wfo(ks, fr, idx, subset, 'W01')
    hasil.update(status='SIAP', entry=list(ks), percubaan=PERCUBAAN, saat=round(time.time() - t0))
    _simpan('W01', hasil, pil, T, cv)
    print('W01 SIAP', round(time.time() - t0), 's')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'senarai':
        s = status(); print(json.dumps(s)); print({v: list(s.values()).count(v) for v in set(s.values())})
    elif a[0] == 'jalan':
        jalan(a[1:])
    elif a[0] == 'satu':
        print(jalan_satu(a[1]))
    elif a[0] == 'kelompok':
        import fcntl
        os.makedirs(KELUAR, exist_ok=True)
        kunci = open(os.path.join(KELUAR, '.kunci'), 'w')
        try: fcntl.flock(kunci, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError: print('SEDANG BERJALAN'); sys.exit(0)
        n = int(a[1]) if len(a) > 1 else 5      # bilangan proses serentak
        had = int(a[2]) if len(a) > 2 else 99   # had bilangan kaedah; masa dihadkan oleh HAD_LANCAR
        belum = [m for m, v in status().items() if v in ('BELUM',)]
        if not belum: print('SEMUA SIAP')
        else: jalan(belum[:had], n)
    elif a[0] == 'w01':
        jalan_w01()
