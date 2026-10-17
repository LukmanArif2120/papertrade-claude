# Penala satu tugasan = (kaedah, kajian) — SPEC A01 §4–§5.
#   kajian 0–10 : ujian tahun 2013+k penuh; 11: ujian 2024-01-01–2024-09-30; latih = 3 tahun sebelum mula ujian.
#   kajian 12   : AKHIR  — latih 2021-10-01–2024-09-30; ujian = 2024-10-01–hujung data (tempoh kunci, A+B juga).
#   kajian 13   : SEMASA — latih 3 tahun terakhir data; tiada ujian.
# Percubaan: sedia() atas [mula latih − 400 hari, akhir latih] (subset tempoh SPEC; kaedah tanpa pandang ke
# hadapan memberi dagangan latih yang sama); penilaian ujian: sedia() sekali atas [mula latih − 400, akhir ujian].
# Guna: python3 tala.py M54 12 [--percubaan 120] [--cache AUTOTUNE/.cache] [--keluar AUTOTUNE/hasil/tala]
import os, sys, json, time, math, argparse, traceback, warnings, importlib.util, types
import numpy as np, pandas as pd

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TERAS = os.path.join(AKAR, 'AUTOTUNE', 'teras')
KOD = os.path.join(AKAR, 'BacktestShariah2', 'kod')
for p in (KOD, TERAS):
    if p not in sys.path: sys.path.insert(0, p)
import enjin_at as E
import objektif as O

DIR_KAEDAH = os.path.join(AKAR, 'AUTOTUNE', 'kaedah')
DIR_ASAL = os.path.join(KOD, 'kaedah')
KELUAR = os.path.join(AKAR, 'AUTOTUNE', 'hasil', 'tala')
PANAS = pd.Timedelta(days=400)
BERSIH = ('2013-01-01', '2018-12-31')
BENIH = 42
PERCUBAAN = 120
HAD_MINIT = 300
NAMA_KAJIAN = {12: 'AKHIR', 13: 'SEMASA'}


# ---------- kajian ----------
def tetingkap(k, akhir_data):
    """dict(latih=(L0, L1), ujian=(U0, U1) | None) bagi kajian k."""
    T = pd.Timestamp; ad = T(akhir_data)
    if 0 <= k <= 10:
        y = 2013 + k; return dict(latih=(T(f'{y - 3}-01-01'), T(f'{y - 1}-12-31')), ujian=(T(f'{y}-01-01'), T(f'{y}-12-31')))
    if k == 11: return dict(latih=(T('2021-01-01'), T('2023-12-31')), ujian=(T('2024-01-01'), T('2024-09-30')))
    if k == 12: return dict(latih=(T('2021-10-01'), T('2024-09-30')), ujian=(T('2024-10-01'), ad))
    if k == 13: return dict(latih=(ad - pd.DateOffset(years=3) + pd.Timedelta(days=1), ad), ujian=None)
    raise ValueError(f'kajian {k} tidak sah')


def senarai_kajian(s):
    """'0-13' / '0,12' / '0-3,12' → senarai int."""
    out = []
    for b in str(s).split(','):
        b = b.strip()
        if not b: continue
        if '-' in b:
            a, z = b.split('-'); out += list(range(int(a), int(z) + 1))
        else: out.append(int(b))
    return sorted(set(out))


# ---------- kaedah ----------
def _muat_fail(nama, f):
    sp = importlib.util.spec_from_file_location(nama, f); m = importlib.util.module_from_spec(sp)
    sys.modules[nama] = m; sp.loader.exec_module(m); return m


def muat_kaedah(mid):
    """Salinan berparameter AUTOTUNE/kaedah/Mxx.py; jika tiada, modul asal dibalut (BELUM_DITALA, P diabaikan)."""
    f = os.path.join(DIR_KAEDAH, mid + '.py')
    if os.path.exists(f):
        if DIR_KAEDAH not in sys.path: sys.path.insert(0, DIR_KAEDAH)
        m = _muat_fail('at_' + mid, f)
        for k, v in dict(PARAM={}, JULAT={}, TALA=[], BELUM_DITALA=False).items():
            if not hasattr(m, k): setattr(m, k, v)
        if m.BELUM_DITALA: m.TALA = []
        return m
    a = _muat_fail('asal_' + mid, os.path.join(DIR_ASAL, mid + '.py'))
    m = types.SimpleNamespace(**{k: getattr(a, k) for k in ('ID', 'NAMA', 'VARIAN', 'TMAX', 'WARM', 'ADA_HENTI',
                                                               'SILANG', 'PERLU_BAR') if hasattr(a, k)})
    m.PARAM, m.JULAT, m.TALA, m.BELUM_DITALA, m.ASAL = {}, {}, [], True, True
    m.sedia = lambda fr, idx, P=None: a.sedia(fr, idx)
    return m


def semua_kaedah():
    d = DIR_KAEDAH if os.path.isdir(DIR_KAEDAH) and any(
        f.startswith('M') and f.endswith('.py') for f in os.listdir(DIR_KAEDAH)) else DIR_ASAL
    ids = [f[:-3] for f in os.listdir(d) if f.startswith('M') and f.endswith('.py') and f[1:-3].isdigit()]
    return sorted(ids, key=lambda x: int(x[1:]))


# ---------- data ----------
class Sumber:
    """Pembungkus teras/data.py: muat() dicache bagi setiap (mula, akhir, kumpulan); topeng dicache.
    dir: direktori data yang sudah disahkan (hasil data.ambil); None → data.muat memanggil ambil() sendiri."""
    def __init__(self, dir=None, modul=None):
        if modul is None:
            import data as modul
        self.D = modul; self.dir = str(dir) if dir else None; self._fr = {}; self._akhir = None

    def muat(self, mula, akhir, kumpulan):
        k = (pd.Timestamp(mula), pd.Timestamp(akhir), kumpulan)
        if k not in self._fr:
            if len(self._fr) >= 2: self._fr.clear()
            self._fr[k] = self.D.muat(k[0], k[1], kumpulan, dir=self.dir)
        return self._fr[k]

    def akhir_data(self):
        if self._akhir is None:
            if hasattr(self.D, 'akhir_data'): self._akhir = pd.Timestamp(self.D.akhir_data(self.dir))
            else:
                d = self.dir or str(self.D.ambil())
                self._akhir = pd.Timestamp(pd.read_parquet(os.path.join(d, 'idx.parquet'), columns=['date'])['date'].max())
        return self._akhir

    def topeng(self, fr, univ, kumpulan):
        return {t: self.D.topeng(g, t, univ, kumpulan) for t, g in fr.items()}


def salin(fr):
    lj = ['open', 'high', 'low', 'close', 'volume', 'turnover']
    return {t: g[[k for k in lj if k in g]].copy() for t, g in fr.items()}


# ---------- penilaian ----------
class Penilai:
    """sedia() + dagangan + portfolio bagi satu set data dan tetingkap. Pasaran, medv dan topeng dikira sekali."""
    def __init__(self, m, fr, idx, univ, sumber, mula, akhir, kumpulan_list):
        tpd = {k: sumber.topeng(fr, univ, k) for k in kumpulan_list}
        if not m.SILANG:   # tanpa kebergantungan merentas saham: buang saham yang tiada hari topeng dalam tetingkap
            fr = {t: g for t, g in fr.items()
                  if any(bool(d[t][(g.index >= mula) & (g.index <= akhir)].any()) for d in tpd.values())}
        self.m, self.fr, self.idx, self.mula, self.akhir = m, fr, idx, mula, akhir
        self.pasaran = E.Pasaran(fr, mula, akhir)
        self.nama = list(fr); self.panjang = [len(g) for g in fr.values()]
        self.medv = E.medv_bersambung(fr)
        self.tp = {k: E.topeng_bersambung(d, fr) for k, d in tpd.items()}
        self.univ, self.sumber = univ, sumber

    def jalan(self, P, kumpulan_list=None, harian=False):
        """Pulang {kumpulan: (metrik, pulangan_harian | None)} bagi P (digabung atas PARAM)."""
        m = self.m; Pp = dict(m.PARAM); Pp.update(P or {})
        f = salin(self.fr); m.sedia(f, self.idx, Pp)
        tmax = Pp['tmax'] if 'tmax' in Pp else m.TMAX
        sejajar = list(f) == self.nama and [len(g) for g in f.values()] == self.panjang
        S = E.Susun(f, medv=self.medv if sejajar else None)
        out = {}
        for k in (kumpulan_list or list(self.tp)):
            tp = self.tp[k] if sejajar else self.sumber.topeng(f, self.univ, k)
            T = S.dengan_topeng(tp).dagangan(tmax, m.WARM, self.mula, self.akhir)
            cv = self.pasaran.lengkung(T)
            out[k] = (O.ringkas(T, cv), E.pulangan_harian(cv) if harian else None)
        return out


def _cadang(tr, m):
    P = {}
    for p in m.TALA:
        jenis, lo, hi = m.JULAT[p]
        P[p] = tr.suggest_int(p, int(lo), int(hi)) if jenis == 'int' else tr.suggest_float(p, float(lo), float(hi))
    return P


def _jiran(m, P):
    """Jiran dataran: setiap parameter TALA ±10%, ±25% (int dibundar, dihadkan JULAT; nilai sama dibuang)."""
    out = []
    for p in m.TALA:
        jenis, lo, hi = m.JULAT[p]; v0 = P[p]
        seen = {v0}
        for f in (0.75, 0.9, 1.1, 1.25):
            v = v0 * f
            v = int(min(max(round(v), lo), hi)) if jenis == 'int' else float(min(max(v, lo), hi))
            if v in seen: continue
            seen.add(v); Q = dict(P); Q[p] = v; out.append((p, f, Q))
    return out


def _bulat(x, n=6):
    if x is None: return None
    if isinstance(x, dict): return {k: _bulat(v, n) for k, v in x.items()}
    if isinstance(x, (float, np.floating)): return None if not math.isfinite(x) else round(float(x), n)
    if isinstance(x, (np.integer,)): return int(x)
    return x


def _metrik_json(mt):
    d = {k: mt[k] for k in ('cagr', 'mdd', 'n', 'win', 'avg', 'days', 'thn_min')}
    d['tahunan'] = {str(y): v for y, v in mt['tahunan'].items()}
    return _bulat(d)


def tala(mid, k, sumber, n_trials=PERCUBAAN, had_minit=HAD_MINIT, tamat=None, keluar=KELUAR, tulis=True):
    """Jalankan satu tugasan; pulang dict hasil (juga ditulis ke keluar/Mxx/kNN.json). tamat: cap masa (epoch)
    yang tidak boleh dilepasi (had shard)."""
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING); warnings.filterwarnings('ignore')
    t0 = time.time(); masa = {}
    tamat = min(tamat or math.inf, t0 + had_minit * 60)
    H = dict(kaedah=mid, kajian=k, nama_kajian=NAMA_KAJIAN.get(k, f'WF{k:02d}'), n_trials_diminta=n_trials,
             ralat=[], status='MULA', mula=pd.Timestamp.now('UTC').strftime('%Y-%m-%dT%H:%M:%SZ'))
    try:
        m = muat_kaedah(mid)
        H.update(belum_ditala=bool(m.BELUM_DITALA), asal=bool(getattr(m, 'ASAL', False)), tala=list(m.TALA),
                 silang=bool(m.SILANG), tmax_asal=m.TMAX, warm=m.WARM)
        w = tetingkap(k, sumber.akhir_data()); L0, L1 = w['latih']
        H['latih'] = [str(L0.date()), str(L1.date())]
        H['ujian'] = [str(w['ujian'][0].date()), str(w['ujian'][1].date())] if w['ujian'] else None
        kl = 'AB' if m.SILANG else 'A'
        t = time.time(); fr, idx, univ = sumber.muat(L0 - PANAS, L1, kl); masa['muat_latih'] = time.time() - t
        H['n_ticker_latih'] = len(fr)
        if not fr or not any((g.index >= L0).any() for g in fr.values()): raise RuntimeError('tiada data latih')
        pn = Penilai(m, fr, idx, univ, sumber, L0, L1, ['A'])
        rekod = []; jejak = {}; s_cuba = []

        def obj(tr):
            ts = time.time()
            P = _cadang(tr, m) if m.TALA else {}
            kunci = tuple(sorted(P.items()))
            if kunci in jejak:
                r = jejak[kunci]; tr.set_user_attr('ulang', True); return r['skor']
            try:
                mt, rh = pn.jalan(P, ['A'], harian=True)['A']
                r = dict(P=P, skor=O.skor(mt), lulus=O.lulus(mt), thn_min=mt['thn_min'], m=mt,
                         rh=rh.values.astype(np.float32))
            except Exception as e:
                r = dict(P=P, skor=-2.0, lulus=False, thn_min=-1.0, m=None, rh=None,
                         ralat=f'{type(e).__name__}: {e}'[:300])
                if len(H['ralat']) < 5: H['ralat'].append('percubaan: ' + r['ralat'])
            if not math.isfinite(r['skor']): r['skor'] = -2.0
            jejak[kunci] = r; rekod.append(r); s_cuba.append(time.time() - ts)
            return r['skor']

        lebih = (4 * len(m.TALA) + 2 if k == 12 else 0) + (6 if k == 0 else 0) + (3 if w['ujian'] else 0)

        def henti(st, tr):
            purata = np.mean(s_cuba) if s_cuba else 0
            if time.time() + purata * (1 + lebih) > tamat: st.stop()

        st = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=BENIH + k))
        if m.TALA:
            st.enqueue_trial({p: m.PARAM[p] for p in m.TALA})
            n_cuba = n_trials
        else:
            n_cuba = 1
        t = time.time()
        st.optimize(obj, n_trials=n_cuba, callbacks=[henti], catch=(Exception,))
        masa['optuna'] = time.time() - t
        H['n_trials'] = len(st.trials); H['n_unik'] = len(rekod)
        masa['s_percubaan'] = float(np.mean(s_cuba)) if s_cuba else None
        if len(st.trials) < n_cuba: H['ralat'].append(f'had masa: {len(st.trials)}/{n_cuba} percubaan')
        sah = [r for r in rekod if r['m'] is not None]
        if not sah: raise RuntimeError('semua percubaan gagal')
        pil, ada_lulus = O.pilih_teguh(sah)
        H['ada_lulus'] = ada_lulus
        H['params'] = _bulat(pil['P']); H['params_penuh'] = _bulat({**m.PARAM, **pil['P']})
        H['skor'] = _bulat(pil['skor']); H['latih_A'] = _metrik_json(pil['m'])
        H['top10'] = [dict(params=_bulat(r['P']), skor=_bulat(r['skor']), lulus=r['lulus'], cagr=_bulat(r['m']['cagr']),
                           mdd=_bulat(r['m']['mdd']), thn_min=_bulat(r['thn_min']))
                      for r in sorted(sah, key=lambda r: r['skor'], reverse=True)[:10]]
        asal = jejak.get(tuple(sorted({p: m.PARAM[p] for p in m.TALA}.items())))
        if asal and asal['m'] is not None: H['latih_A_asal'] = _metrik_json(asal['m'])

        # --- kajian 12: dataran + PBO (data latih) ---
        if k == 12 and m.TALA:
            t = time.time(); jir = []
            for p, f, Q in _jiran(m, pil['P']):
                if time.time() > tamat: H['ralat'].append('had masa: dataran tidak lengkap'); break
                try: jir.append((p, f, pn.jalan(Q, ['A'])['A'][0]['cagr']))
                except Exception as e: H['ralat'].append(f'dataran {p}x{f}: {type(e).__name__}')
            c0 = pil['m']['cagr']; cs = [c for _, _, c in jir]
            H['dataran'] = _bulat(dict(n=len(cs), cagr_pilihan=c0, median_jiran=float(np.median(cs)) if cs else None,
                                       min_jiran=float(min(cs)) if cs else None,
                                       nisbah=float(np.median(cs) / c0) if cs and c0 not in (0, None) else None,
                                       ikut_param={p: float(np.median([c for q, _, c in jir if q == p]))
                                                   for p in m.TALA if any(q == p for q, _, _ in jir)}))
            atas = [r for r in sorted(sah, key=lambda r: r['skor'], reverse=True) if r['rh'] is not None][:50]
            if len(atas) >= 2:
                M = np.column_stack([r['rh'] for r in atas])
                H['pbo'] = _bulat(dict(O.pbo(M, 8), n_percubaan=len(atas)))
            masa['dataran_pbo'] = time.time() - t
        del pn, fr; sumber._fr.clear()

        # --- ujian A / B (/ AB bagi kajian 12) ---
        if w['ujian']:
            U0, U1 = w['ujian']; t = time.time()
            fr, idx, univ = sumber.muat(L0 - PANAS, U1, 'AB')
            kum = ['A', 'B', 'AB'] if k == 12 else ['A', 'B']
            pu = Penilai(m, fr, idx, univ, sumber, U0, U1, kum)
            hs = pu.jalan(pil['P'], kum, harian=True)
            H['harian_ujian'] = dict(tarikh=[str(d.date()) for d in pu.pasaran.tarikh])
            for g, (mt, rh) in hs.items():
                H[f'ujian_{g}'] = _metrik_json(mt)
                H['harian_ujian'][g] = [round(float(x), 6) for x in rh]
            del pu, fr; sumber._fr.clear(); masa['ujian'] = time.time() - t

        # --- kajian 0: bersih (PARAM asal, 2013–2018, A+B) ---
        if k == 0:
            t = time.time(); B0, B1 = pd.Timestamp(BERSIH[0]), pd.Timestamp(BERSIH[1])
            try:
                fr, idx, univ = sumber.muat(B0 - PANAS, B1, 'AB')
                pb = Penilai(m, fr, idx, univ, sumber, B0, B1, ['AB'])
                mt, rh = pb.jalan({}, ['AB'], harian=True)['AB']
                H['bersih_AB'] = _metrik_json(mt)
                H['harian_bersih_AB'] = dict(tarikh=[str(d.date()) for d in rh.index], r=[round(float(x), 6) for x in rh])
                del pb, fr; sumber._fr.clear()
            except Exception as e:
                H['ralat'].append(f'bersih: {type(e).__name__}: {e}'[:300])
            masa['bersih'] = time.time() - t
        H['status'] = 'SIAP'
    except Exception as e:
        H['status'] = 'RALAT'; H['ralat'].append(f'{type(e).__name__}: {e}'[:500])
        H['jejak'] = traceback.format_exc()[-1500:]
    masa['jumlah'] = time.time() - t0
    try:
        import resource; H['rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    except Exception: pass
    H['masa'] = _bulat(masa, 2); H['n_trials'] = H.get('n_trials', 0)
    if tulis: simpan(H, keluar)
    return H


def simpan(H, keluar=KELUAR):
    d = os.path.join(keluar, H['kaedah']); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f"k{int(H['kajian']):02d}.json")
    with open(f + '.tmp', 'w') as fh: json.dump(H, fh, separators=(',', ':'))
    os.replace(f + '.tmp', f)
    return f


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('kaedah'); a.add_argument('kajian', type=int)
    a.add_argument('--percubaan', type=int, default=PERCUBAAN); a.add_argument('--had-minit', type=float, default=HAD_MINIT)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', 'AUTOTUNE/.cache'))
    a.add_argument('--keluar', default=KELUAR)
    x = a.parse_args(argv)
    import data
    H = tala(x.kaedah, x.kajian, Sumber(data.ambil(x.cache)), x.percubaan, x.had_minit, keluar=x.keluar)
    print(H['kaedah'], H['kajian'], H['status'], 'skor', H.get('skor'), 'masa', H['masa'].get('jumlah'), H['ralat'][:2])


if __name__ == '__main__':
    main()
