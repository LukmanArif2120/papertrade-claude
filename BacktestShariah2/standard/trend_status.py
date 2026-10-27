# trend_status.py — status trend D10+H2 bagi posisi Papertrade C dan watchlist (dashboard: pill Trend, dokumen db harian/trend).
# Kajian: reports/Penentuan status trend saham mendalam.md (23 Okt 2026). Status ini REKOD SEJARAH, bukan peramal dan bukan
# isyarat jual: dalam ujian 2020–2026 ia tidak meramal pulangan 3–30 hari; risiko diukur oleh ATR14%, jarak lorong 2 dan earnings.
#
# Takrif (versi D10H2-r2):
#   mentah_t  = Bullish jika C > SMA50 > SMA150 > SMA200 (ketat); Bearish jika C < SMA50 < SMA150 < SMA200; Neutral selainnya
#   status_t  = status_{t-1}, kecuali mentah_{t-1} = mentah_t = X != status_{t-1} -> X (tutup kedua = tarikh_sah, beku)
#   umur      = bar dari tarikh_sah hingga hari ini (tarikh_sah = 1); sub-label baharu <= 20, lama > 60 (Neutral tiada sub-label)
#   titik mula= Bullish: rendah intrahari terendah, Bearish: tinggi tertinggi, dalam 63 bar berakhir pada tarikh_sah (seri -> bar
#               paling akhir); beku; "tembus" = tarikh pertama harga melepasi titik itu selepas tarikh_sah
#   ATR14%    = purata mudah 14 julat sebenar ÷ tutup × 100 (sama dengan enjin.atr / keluar_lorong.atr); atr_q = kuintil
#               merentas semua saham stor pada tarikh yang sama (1 rendah … 5 sangat tinggi)
#   lonjak    = pulangan 5 sesi dalam 20% teratas stor pada tarikh sama (tooltip sahaja)
#   rejim     = SPY D10+H2 + RV21 SPY (sisihan piawai 21 pulangan log × √252): Tertekan jika SPY Bearish atau RV21 >= 21.8%;
#               Tenang jika RV21 < 14.0%; Biasa selainnya (ambang = tertil IS 2020–2022)
# Siri harga: stor repo (konvensyen backtest) + bar terkini.csv yang lebih baharu daripada bar akhir stor; jika bar bertindih
# terakhir berbeza > 0.3% (faktor belum dilaras), stor sahaja dipakai dan ditanda "semak data".
#
# Guna:
#   python3 BacktestShariah2/standard/trend_status.py tulis [--folder <papertrade>] [--keluar data/trend/status.json]
#       -> dokumen (dibaca jana_db.py -> db harian/trend); medan beku dibawa dari fail sedia ada jika tarikh_sah
#          sudah keluar daripada tetingkap stor (520 bar)
#   python3 BacktestShariah2/standard/trend_status.py garis TICKER   -> garis masa silang SMA dan pertukaran status
import argparse, csv, glob, json, os, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
STOR = os.path.join(BS2, 'data', 'harga', 'stor')
TERKINI = os.path.join(BS2, 'data', 'harga', 'terkini.csv')
PT = os.path.join(BS2, 'papertrade')
FAIL = os.path.join(BS2, 'data', 'trend', 'status.json')
AMBIL_ALIH = os.path.join(BS2, 'data', 'ambil_alih.csv')

VERSI = 'D10H2-r2'
N_PENDEK, N_TENGAH, N_PANJANG = 50, 150, 200
MIN_BAR = N_PANJANG + 1        # SMA200 + dua tutup
BAHARU, LAMA = 20, 60
TETINGKAP_TITIK = 63
N_ATR = 14
TOL_LARAS = 0.003              # sama dengan kod/stor.py nisbah_laras
LOMPAT_SEMAK = 0.40
RV_TENANG, RV_TERTEKAN = 14.0, 21.8
NAMA = {1: 'Bullish', 0: 'Neutral', -1: 'Bearish'}
LAJUR = ['saham', 's', 'sub', 'sah', 'umur', 'tepat', 'pct_sejak', 'dari', 'sebab', 'isyarat', 'titik_tarikh', 'titik_harga',
         'pct_titik', 'tembus', 'atr_pct', 'atr_q', 'mentah', 'calon', 'susun', 'jarak', 'c', 'c_sah', 'sma50', 'n60', 'lonjak',
         'tarikh_data']
K = {n: i for i, n in enumerate(LAJUR)}


# ------------------------------------------------------------------ data
def _baca(paths):
    fr = [pd.read_csv(p, dtype={'date': str}) for p in paths if os.path.exists(p)]
    return pd.concat(fr, ignore_index=True) if fr else pd.DataFrame(columns=['ticker', 'date', 'open', 'high', 'low', 'close'])


def muat_harga(stor=STOR, terkini=TERKINI, fail=('harga_A.csv', 'harga_B.csv'),
               lajur=('date', 'open', 'high', 'low', 'close')):
    """-> ({ticker: DataFrame lajur (date int) menaik}, {ticker: nota}); lajur yang tiada dalam fail dilangkau
    (stage.py meminta 'volume')."""
    S = _baca([os.path.join(stor, f) for f in fail])
    T = _baca([terkini]) if terkini else S.iloc[:0]
    Tg = dict(tuple(T.groupby('ticker'))) if len(T) else {}
    out, nota = {}, {}
    for t, g in S.groupby('ticker'):
        g = g.sort_values('date').drop_duplicates('date', keep='last')
        tk = Tg.get(t)
        if tk is not None and len(tk):
            sama = g.merge(tk, on='date', suffixes=('_s', '_t'))
            if len(sama):
                x = sama.iloc[-1]; r = float(x.close_t / x.close_s)
                if abs(r - 1) > TOL_LARAS:
                    nota[t] = f'bar {x.date} terkini/stor = {r:.4f} (faktor belum dilaras?): stor sahaja dipakai, semak data'
                    tk = None
            if tk is not None:
                g = pd.concat([g, tk[tk.date > g.date.max()]], ignore_index=True)
        g = g.assign(date=g.date.astype(int))
        out[t] = g[[k for k in lajur if k in g.columns]].reset_index(drop=True)
    return out, nota


def atr(h, l, c, n=N_ATR):
    pc = np.r_[np.nan, c[:-1]]
    tr = np.fmax(h - l, np.fmax(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr).rolling(n).mean().to_numpy()


def sma(c, n):
    return pd.Series(c).rolling(n).mean().to_numpy()


# ------------------------------------------------------------------ teras
def mentah(c, s50, s150, s200):
    """+1 / 0 / -1; NaN sebelum SMA200. Kesamaan -> 0."""
    m = np.where((c > s50) & (s50 > s150) & (s150 > s200), 1.0,
                 np.where((c < s50) & (s50 < s150) & (s150 < s200), -1.0, 0.0))
    m[np.isnan(s200)] = np.nan
    return m


def mesin(m):
    """Pengesahan 2 tutup. -> status (NaN = belum diketahui), peristiwa [(i_isyarat, i_sah, dari, ke)], i_mula.
    Status pertama = mentah apabila dua mentah berturut pertama sama (tersensor)."""
    n = len(m); st = np.full(n, np.nan); ev = []; cur = None; i_mula = None
    for i in range(1, n):
        x, xp = m[i], m[i - 1]
        if np.isnan(x) or np.isnan(xp):
            continue
        if cur is None:
            if x == xp:
                cur = x; i_mula = i
        elif x != cur and xp == x:
            ev.append((i - 1, i, int(cur), int(x))); cur = x
        if cur is not None:
            st[i] = cur
    return st, ev, i_mula


SYARAT = ('C50', '50_150', '150_200')


def sebab(c, s50, s150, s200, i1, dari, ke):
    """Syarat yang menyebabkan pertukaran (dinilai pada tutup pertama i1), kod dipisah '+'."""
    def gagal(i, arah):
        a = [c[i] > s50[i], s50[i] > s150[i], s150[i] > s200[i]] if arah == 1 else \
            [c[i] < s50[i], s50[i] < s150[i], s150[i] < s200[i]]
        return [k for k, ok in zip(SYARAT, a) if not ok]
    f = gagal(i1, dari) if dari != 0 else gagal(i1 - 1, ke)
    return '+'.join(f) or None


def titik_mula(lo, hi, i_sah, arah, w=TETINGKAP_TITIK):
    a = max(0, i_sah - w + 1)
    if arah == 1:
        seg = lo[a:i_sah + 1]; j = a + len(seg) - 1 - int(np.argmin(seg[::-1]))
        return j, float(lo[j])
    if arah == -1:
        seg = hi[a:i_sah + 1]; j = a + len(seg) - 1 - int(np.argmax(seg[::-1]))
        return j, float(hi[j])
    return None, None


def kira(g):
    """Ringkasan status satu ticker (DataFrame date/open/high/low/close menaik)."""
    d = g.date.to_numpy(int); h, l, c = (g[k].to_numpy(float) for k in ('high', 'low', 'close'))
    n = len(c)
    r = dict(n_bar=n, tarikh_data=int(d[-1]) if n else None)
    if n > N_ATR:
        a = atr(h, l, c)
        if not np.isnan(a[-1]):
            r['atr_pct'] = float(a[-1] / c[-1] * 100)
    if n > 5:
        r['r5'] = float(c[-1] / c[-6] - 1)
    if n:
        r['c'] = float(c[-1])
    if n < MIN_BAR:
        r.update(status=None, sebab=f'sejarah {n} sesi < {MIN_BAR}')
        return r
    s50, s150, s200 = sma(c, N_PENDEK), sma(c, N_TENGAH), sma(c, N_PANJANG)
    m = mentah(c, s50, s150, s200); st, ev, i_mula = mesin(m)
    lomp = np.abs(c[1:] / c[:-1] - 1)
    tanda = lambda x, y: '+' if x > y else ('-' if x < y else '=')
    r.update(susun=tanda(c[-1], s50[-1]) + tanda(s50[-1], s150[-1]) + tanda(s150[-1], s200[-1]),
             jarak=[float((c[-1] / s50[-1] - 1) * 100), float((s50[-1] / s150[-1] - 1) * 100), float((s150[-1] / s200[-1] - 1) * 100)],
             sma50=float(s50[-1]), mentah=int(m[-1]), n60=sum(1 for _, b, _, _ in ev if b >= n - 60),
             semak_data=bool(np.any(lomp[-60:] > LOMPAT_SEMAK)))
    if i_mula is None:
        r.update(status=None, sebab='belum ada dua tutup berturut dengan susunan sama')
        return r
    s = int(st[-1]); r['status'] = s
    if ev:
        i_isy, i_sah, dari, ke = ev[-1]; tepat = True
        r['sebab'] = sebab(c, s50, s150, s200, i_isy, dari, ke)
    else:
        i_isy, i_sah, dari, tepat = None, i_mula, None, False
    umur = n - i_sah
    r.update(tepat=tepat, sah=int(d[i_sah]), isyarat=int(d[i_isy]) if i_isy is not None else None, umur=umur,
             pct_sejak=float((c[-1] / c[i_sah] - 1) * 100), dari=dari, c_sah=float(c[i_sah]), sub=sub_label(s, umur, tepat))
    if s != 0 and tepat:
        j, p = titik_mula(l, h, i_sah, s)
        r.update(titik_tarikh=int(d[j]), titik_harga=p, pct_titik=float((c[-1] / p - 1) * 100))
        k = np.flatnonzero(l[i_sah + 1:] < p if s == 1 else h[i_sah + 1:] > p)
        r['tembus'] = int(d[i_sah + 1 + k[0]]) if len(k) else None
    r['calon'] = int(m[-1]) if m[-1] != s else None
    return r


def sub_label(s, umur, tepat):
    if s == 0 or umur is None:
        return ''
    if umur > LAMA:
        return 'lama'
    return 'baharu' if tepat and umur <= BAHARU else ''


def rejim(g):
    """Rejim pasaran daripada siri SPY."""
    if g is None or len(g) < MIN_BAR:
        return None
    r = kira(g); c = g.close.to_numpy(float)
    rv = float(np.std(np.diff(np.log(c[-22:])), ddof=1) * np.sqrt(252) * 100)
    lbl = 'Tertekan' if r.get('status') == -1 or rv >= RV_TERTEKAN else ('Tenang' if rv < RV_TENANG else 'Biasa')
    return dict(spy_s=r.get('status'), spy_umur=r.get('umur'), spy_sah=r.get('sah'), rv21=round(rv, 1), label=lbl,
                tarikh=r.get('tarikh_data'), ambang=[RV_TENANG, RV_TERTEKAN])


# ------------------------------------------------------------------ alam dan dokumen
def benar(v):
    return str(v).strip().lower() == 'true'


def alam(folder=PT, H=None):
    """Saham yang dipapar dashboard: semua posisi Papertrade C dan Moomoo lama (dipegang atau sudah keluar), watchlist,
    dan semua saham stor H (jika diberi) supaya posisi baharu esok sudah ada status."""
    u = set(H or ())
    for p in sorted(glob.glob(os.path.join(folder, 'claude*.csv'))) + [os.path.join(folder, 'moomoo.csv')]:
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                u |= {x['saham'] for x in csv.DictReader(f) if x.get('saham') and not benar(x.get('tidak_dibeli'))}
    p = os.path.join(folder, 'watchlist.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            u |= {x['Saham'] for x in csv.DictReader(f) if x.get('Saham')}
    return u


def ambil_alih(path=AMBIL_ALIH):
    try:
        with open(path, encoding='utf-8') as f:
            return {x['saham']: int(x['tarikh_umum'].replace('-', '')) for x in csv.DictReader(f)
                    if x.get('saham') and x.get('tarikh_umum')}
    except OSError:
        return {}


def _r2(v):
    return None if v is None else round(float(v), 2)


def baris(t, r):
    o = [None] * len(LAJUR); o[0] = t
    if not r:
        return o
    for f in ('s', 'sub', 'sah', 'umur', 'tepat', 'dari', 'sebab', 'isyarat', 'titik_tarikh', 'tembus', 'atr_q', 'mentah', 'calon',
              'susun', 'n60', 'lonjak', 'tarikh_data'):
        v = r.get('status' if f == 's' else f)
        o[K[f]] = int(v) if isinstance(v, (bool, np.bool_)) else v
    for f in ('pct_sejak', 'titik_harga', 'pct_titik', 'atr_pct', 'c', 'c_sah', 'sma50'):
        o[K[f]] = _r2(r.get(f))
    o[K['jarak']] = [_r2(x) for x in r['jarak']] if r.get('jarak') else None
    o[K['sub']] = o[K['sub']] or ''
    return o


def kuintil(nilai, v):
    """Kuintil 1..5 bagi v berbanding ambang [p20, p40, p60, p80]."""
    return None if v is None or not nilai else 1 + int(np.searchsorted(nilai, v, side='right'))


def dokumen(H, saham, nota=None, idx=None):
    """Dokumen db harian/trend. H: semua ticker stor (untuk kuintil ATR% dan lonjakan 5 sesi); saham: alam papan."""
    nota = dict(nota or {})
    R = {t: kira(g) for t, g in H.items()}
    tarikh = max((r.get('tarikh_data') or 0) for r in R.values()) if R else 0
    semasa = [r for r in R.values() if r.get('tarikh_data') == tarikh]
    a = [r['atr_pct'] for r in semasa if r.get('atr_pct') is not None]
    ambang = [round(float(x), 3) for x in np.percentile(a, [20, 40, 60, 80])] if len(a) >= 50 else []
    r5 = [r['r5'] for r in semasa if r.get('r5') is not None]
    p80 = float(np.percentile(r5, 80)) if len(r5) >= 50 else None
    AA = ambil_alih(); aa = []; rows = []
    for t in sorted(saham):
        r = R.get(t)
        if r is None:
            rows.append(baris(t, None)); continue
        r['atr_q'] = kuintil(ambang, r.get('atr_pct'))
        r['lonjak'] = int(p80 is not None and r.get('r5') is not None and r['r5'] >= p80 and r.get('tarikh_data') == tarikh)
        rows.append(baris(t, r))
        if t in AA and AA[t] <= (r.get('tarikh_data') or 0):
            aa.append(t)
        if r.get('semak_data'):
            nota[t] = (nota[t] + '; ' if nota.get(t) else '') + 'pergerakan > 40% sehari dalam 60 sesi: semak data'
    return dict(tarikh=tarikh, versi=VERSI, lajur=LAJUR, rows=rows, atr_ambang=ambang,
                r5_ambang=round(p80 * 100, 2) if p80 is not None else None, ambil_alih=aa,
                rejim=rejim((idx or {}).get('SPY')),
                takrif='Bullish = tutup > SMA50 > SMA150 > SMA200; Bearish = terbalik; lain Neutral; bertukar selepas 2 tutup berturut; '
                       'umur dari tutup kedua (= 1); baharu <= 20 sesi, lama > 60; titik mula = rendah/tinggi ekstrem 63 sesi '
                       'hingga tarikh sah (beku). Rekod sejarah, bukan isyarat jual.',
                nota={k: v for k, v in nota.items() if k in saham})


def bawa_semalam(baru, lama):
    """Bawa medan beku dari dokumen sebelumnya apabila tarikh_sah sudah keluar daripada tetingkap stor (status sama;
    kiraan baharu tersensor tetapi lama tepat). Umur = umur lama + 1 jika tarikh data maju."""
    if not lama or lama.get('lajur') != LAJUR:
        return baru
    L = {r[0]: r for r in lama.get('rows', [])}
    for r in baru['rows']:
        o = L.get(r[0])
        if not o or r[K['s']] is None or o[K['s']] != r[K['s']] or r[K['tepat']] or not o[K['tepat']]:
            continue
        tambah = 1 if (r[K['tarikh_data']] or 0) > (o[K['tarikh_data']] or 0) else 0
        for f in ('sah', 'tepat', 'dari', 'sebab', 'isyarat', 'titik_tarikh', 'titik_harga', 'tembus', 'c_sah'):
            r[K[f]] = o[K[f]]
        r[K['umur']] = o[K['umur']] + tambah
        c = r[K['c']]
        r[K['pct_sejak']] = _r2((c / r[K['c_sah']] - 1) * 100) if c and r[K['c_sah']] else None
        r[K['pct_titik']] = _r2((c / r[K['titik_harga']] - 1) * 100) if c and r[K['titik_harga']] else None
        r[K['sub']] = sub_label(r[K['s']], r[K['umur']], True)
    return baru


def bina(folder=PT, stor=STOR, terkini=TERKINI, semalam=FAIL):
    H, nota = muat_harga(stor, terkini)
    I, _ = muat_harga(stor, terkini, fail=('harga_idx.csv',))
    doc = dokumen(H, alam(folder, H), nota, I)
    lama = None
    if semalam and os.path.exists(semalam):
        try:
            lama = json.load(open(semalam, encoding='utf-8'))
        except ValueError:
            lama = None
    return bawa_semalam(doc, lama)


# ------------------------------------------------------------------ garis masa
def garis(g):
    d = g.date.to_numpy(int); c = g.close.to_numpy(float)
    s50, s150, s200 = sma(c, 50), sma(c, 150), sma(c, 200)
    m = mentah(c, s50, s150, s200); st, ev, i_mula = mesin(m)
    pas = {'C×SMA50': c - s50, 'C×SMA150': c - s150, 'C×SMA200': c - s200, 'SMA50×SMA150': s50 - s150,
           'SMA50×SMA200': s50 - s200, 'SMA150×SMA200': s150 - s200}
    out = []
    for k, x in pas.items():
        sg = np.sign(x)
        for i in range(1, len(x)):
            if np.isnan(x[i - 1]) or np.isnan(x[i]) or sg[i] == sg[i - 1] or sg[i] == 0:
                continue
            out.append((int(d[i]), k, 'naik' if sg[i] > 0 else 'turun', c[i]))
    for a_, b_, x_, y_ in ev:
        out.append((int(d[b_]), 'STATUS', f'{NAMA[x_]}→{NAMA[y_]} (tutup pertama {d[a_]})', c[b_]))
    if i_mula is not None:
        out.append((int(d[i_mula]), 'STATUS', f'mula diketahui: {NAMA[int(st[i_mula])]} (tersensor)', c[i_mula]))
    return sorted(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Status trend D10+H2 (dashboard harian/trend)')
    ap.add_argument('arahan', choices=['tulis', 'garis']); ap.add_argument('ticker', nargs='?')
    ap.add_argument('--folder', default=PT); ap.add_argument('--stor', default=STOR); ap.add_argument('--terkini', default=TERKINI)
    ap.add_argument('--keluar', default=FAIL)
    a = ap.parse_args(argv)
    if a.arahan == 'tulis':
        doc = bina(a.folder, a.stor, a.terkini, a.keluar)
        os.makedirs(os.path.dirname(os.path.abspath(a.keluar)), exist_ok=True)
        s = json.dumps(doc, separators=(',', ':'), ensure_ascii=False)
        open(a.keluar, 'w', encoding='utf-8').write(s)
        n = {1: 0, 0: 0, -1: 0, None: 0}
        for r in doc['rows']:
            n[r[K['s']]] += 1
        print(f"{len(doc['rows'])} saham, {len(s.encode())} bait, tarikh {doc['tarikh']}: Bullish {n[1]}, Neutral {n[0]}, "
              f"Bearish {n[-1]}, tiada status {n[None]}; rejim {(doc['rejim'] or {}).get('label')}")
    else:
        H, _ = muat_harga(a.stor, a.terkini)
        for x in garis(H[a.ticker]):
            print(x[0], f'{x[1]:14s}', f'{x[2]:40s}', round(x[3], 2))


if __name__ == '__main__':
    main()
