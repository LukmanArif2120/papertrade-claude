"""Carian setup — pusingan CS19 (SPEC pindaan 16 Nov 2026 (ae) Bahagian A): AUDIT BEBAS senarai utama F.

Bukan carian: tiada kod F baharu, registry / senarai utama / kohort tidak diubah. Tiga perkara:
  1. KIRAAN SEMULA BEBAS: bahagian "KOD BEBAS" di bawah mengira sendiri bar layak, harga beli, label, asas saham rawak,
     satu posisi dan cara pegang B daripada harga mentah, TANPA kernel enjin (cs_teras, cs_semak11, cs_tala7).
  2. UJIAN "TENGOK MASA DEPAN": ujian bar terakhir (isyarat pada data yang dipotong lawan data penuh) dan mod tanpa intai.
  3. UKURAN BAHARU: jatuh >= 5 % minggu pertama, arah, menang / purata LAWAN saham rawak yang dipegang sama, gred A-D.

Guna (folder kerja di luar repo; panel_A/B, lapis_B dan cs07_K_B sudah ada -- lihat SERAHAN_CARIAN_SETUP.md §10):
  python3 cs_audit19.py benih  <kerja>   isyarat benih M/N kumpulan B bagi semua setup senarai utama (asal + tanpa intai)
  python3 cs_audit19.py bebas  <kerja>   7 setup contoh + kawalan, isyarat pun ditulis semula secara bebas
  python3 cs_audit19.py setup  <kerja>   semua setup senarai utama: pariti + ukuran baharu (+ versi tanpa intai)
  python3 cs_audit19.py intai  <kerja>   ujian bar terakhir setiap pencetus
  python3 cs_audit19.py lapor  <kerja>   hasil/CS19/AUDIT.md, audit.csv.gz, gabungan.csv, intai.csv, bebas.csv, bacaan.json
Jangan sunting keluaran secara manual."""
import glob
import importlib
import json
import os
import pickle
import re
import sys
import warnings

import numpy as np
import pandas as pd
from numba import njit

SINI = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.normpath(os.path.join(SINI, '..', '..', '..'))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
PUS = 'CS19'
HASIL = os.path.join(SINI, 'hasil', PUS)
SEC = os.path.join(BS2, 'data', 'sec', 'earnings_8k.csv')
MULA, AKHIR = pd.Timestamp('2010-01-04'), pd.Timestamp('2026-08-28')
TEMPOH_B = ((20100104, 20191231), (20200102, 20241231), (20250102, 20260828))        # K1, K2, K3 (sama seperti enjin)
KOS = 0.005
N_ATAS = 300                                                                         # "300 teratas" permintaan pengguna
LAB = ['m5', 'terus', 'j5', 'm10', 'j10', 'r5', 'r20']
TOL = 0.0005                                                                         # pariti (pindaan (ae) A1)
KOHORT = ['F421', 'F1057', 'F1033', 'F200', 'F1247', 'F1448', 'F1285', 'F668', 'F833', 'F1030', 'F571', 'F1288', 'F203',
          'F479', 'F694', 'F1589', 'F363', 'F1207', 'F1539', 'F1347', 'F733', 'F263', 'F1564', 'F1583', 'F1354', 'F706',
          'F742', 'F557', 'F707']                                                    # gred A dalam 300 teratas (dikunci (ae))
KALENDAR = 'Mei-Okt|Januari|Nov-Apr|hari pertama bulan'
F_ = lambda kerja, nama: os.path.join(kerja, f'cs19_{nama}.pkl')


def log(*a):
    import time
    print(time.strftime('%H:%M:%S'), *a, flush=True)


# =====================================================================================================================
# KOD BEBAS: tiada import cs_* di bahagian ini. Ditulis daripada takrif bertulis (spec / laporan), bukan disalin.
# =====================================================================================================================
def folder_data():
    sys.path.insert(0, AKAR)
    from AUTOTUNE.teras import data as D                     # pemuat turun Release sahaja (bukan kernel)
    return str(D.ambil(tag='autotune-data-a02')) + os.sep


def muat(kump='B'):
    """Harga mentah kumpulan `kump` (tersusun ticker, tarikh) + keahlian universe bulanan + indeks."""
    d = folder_data()
    u = pd.read_parquet(d + 'universe.parquet')
    u = u[u.kumpulan == kump]
    tick = sorted(u.ticker.unique())
    df = pd.concat([pd.read_parquet(d + f'harga_{y}.parquet', filters=[('ticker', 'in', tick)]) for y in range(2009, 2027)])
    df = df.sort_values(['ticker', 'date']).reset_index(drop=True)
    for k in ('open', 'high', 'low', 'close'):
        df[k] = df[k].astype('float64')
    ahli = set(zip(u.ticker, u.bulan))
    df['dalam'] = [(t, b) in ahli for t, b in zip(df.ticker, df.date.dt.strftime('%Y-%m'))]
    return df, pd.read_parquet(d + 'idx.parquet')


def wilder(s, n):
    return s.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def sedia(df):
    """Lajur asas setiap saham + kelayakan + HASIL (harga masa depan dipakai untuk hasil sahaja, bukan isyarat)."""
    g = df.groupby('ticker', sort=False)
    df['k'] = g.cumcount()
    df['T'] = g.close.transform('size')
    pc = g.close.shift(1)
    tr = pd.concat([df.high - df.low, (df.high - pc).abs(), (df.low - pc).abs()], axis=1).max(axis=1)
    df['atr'] = tr.groupby(df.ticker, sort=False).transform(lambda s: wilder(s, 14))
    df['P'] = g.open.shift(-1)                               # harga beli = buka esok
    df['c1'], df['c5'], df['c20'] = g.close.shift(-1), g.close.shift(-5), g.close.shift(-20)
    lo, tk, n = df.low.to_numpy(), df.ticker.to_numpy(), len(df)
    mn = np.full(n, np.inf)
    for d in range(2, 21):                                   # rendah terendah sesi 2..20 selepas beli
        x = np.full(n, np.nan)
        x[:-d] = lo[d:]
        sama = np.zeros(n, bool)
        sama[:-d] = tk[d:] == tk[:-d]
        mn = np.where(sama & (x < mn), x, mn)
    df['sah'] = ((df.k >= 252) & df.dalam & (df.date >= MULA) & (df.date <= AKHIR) & (df.k + 20 < df['T'])
                 & (df.atr > 0) & (df.P > 0))
    P = df.P
    h8 = (df.c1 <= P * 0.92) | (mn <= P * 0.92)
    df['m5'] = df.c5 >= P * 1.05
    df['terus'] = df.m5 & (df.c20 > df.c5) & ~h8
    df['j5'] = df.c5 <= P * 0.95                             # ukuran baharu audit: JATUH >= 5 % minggu pertama
    df['m10'], df['j10'] = df.c5 >= P * 1.10, df.c5 <= P * 0.90
    df['r5'], df['r20'] = df.c5 / P - 1, df.c20 / P - 1
    return df


def asas_rawak(df, lajur):
    """Purata setiap label antara SEMUA bar layak pada hari yang sama dan tercile ATR % yang sama."""
    s = df[df.sah].copy()
    s['terc'] = np.minimum(((s.atr / s.close).groupby(s.date).rank(pct=True) * 3).astype(int), 2)
    out = s.groupby(['date', 'terc'])[lajur].transform('mean')
    out.columns = ['a_' + c for c in lajur]
    df[out.columns] = np.nan
    df.loc[s.index, out.columns] = out
    df['terc'] = -1
    df.loc[s.index, 'terc'] = s.terc
    return df


def hingga_laporan(df, zon='utc20'):
    """hingga = bilangan sesi dari bar ini ke hari pasaran PERTAMA yang boleh bertindak balas kepada laporan seterusnya
    (8-K butiran 2.02). zon='utc20': selepas tutup = jam terima UTC >= 20; zon='ny': >= 16:00 waktu New York."""
    e = pd.read_csv(SEC, usecols=['saham', 'tarikh_fail', 'masa_terima', 'items'])
    e = e[e['items'].astype(str).str.contains('2.02', regex=False)]
    t = pd.to_datetime(e.masa_terima, errors='coerce', utc=True)
    if zon == 'utc20':
        e['lewat'], e['hari'] = (t.dt.hour >= 20).to_numpy(), pd.to_datetime(e.tarikh_fail)
    else:
        from zoneinfo import ZoneInfo
        tn = t.dt.tz_convert(ZoneInfo('America/New_York'))
        e['lewat'] = (tn.dt.hour >= 16).fillna(False).to_numpy()
        e['hari'] = pd.to_datetime(tn.dt.strftime('%Y-%m-%d'), errors='coerce').fillna(pd.to_datetime(e.tarikh_fail))
    eg = dict(tuple(e.groupby('saham')))
    hingga, ada = np.full(len(df), 10 ** 6, np.int64), np.zeros(len(df), bool)
    mula = df.groupby('ticker', sort=False).head(1).index.to_numpy()
    tk, tarikh = df.ticker.to_numpy(), df.date.to_numpy()
    for a, b in zip(mula, np.append(mula[1:], len(df))):
        g = eg.get(tk[a])
        if g is None:
            continue
        ada[a:b] = True
        d, hr = tarikh[a:b], g.hari.to_numpy()
        ev = np.where(g.lewat.to_numpy(), np.searchsorted(d, hr, 'right'), np.searchsorted(d, hr, 'left'))
        ev = np.unique(ev[(ev > 0) & (ev < b - a)])
        if len(ev):
            i = np.arange(b - a)
            kn = np.searchsorted(ev, i, 'right')
            hingga[a:b] = np.where(kn < len(ev), ev[np.minimum(kn, len(ev) - 1)] - i, 10 ** 6)
    return hingga, ada


def rejim_qqq(df, ix):
    hu = np.sort(df.date.unique())
    q = ix[ix.ticker == 'QQQ'].set_index('date').close.astype(float).reindex(hu).ffill()
    m50 = q.rolling(50).mean()
    on = (q > m50) & (q.rolling(10).mean() > q.rolling(20).mean())
    off = (~on) & m50.notna()
    umur, u, dulu = [], 0, None
    for v in on.to_numpy():                                  # umur rejim = bilangan sesi berturut dalam keadaan yang sama
        u = u + 1 if v == dulu else 1
        dulu = v
        umur.append(u)
    return pd.DataFrame({'off': off, 'off_baharu': off & (pd.Series(umur, index=hu) <= 10)})


def per_saham(df, f):
    return df.groupby('ticker', sort=False, group_keys=False).apply(f, include_groups=False).reindex(df.index)


def hari_pertama(df, s):
    s = s.fillna(False).astype(bool)
    return s & ~s.groupby(df.ticker, sort=False).shift(1, fill_value=False)


def _rsi(c, n):
    d = c.diff()
    return 100 - 100 / (1 + wilder(d.clip(lower=0), n) / wilder((-d).clip(lower=0), n).replace(0, np.nan))


def _adx14(g):
    pc = g.close.shift()
    a = wilder(pd.concat([g.high - g.low, (g.high - pc).abs(), (g.low - pc).abs()], axis=1).max(axis=1), 14)
    um, dm = g.high.diff(), -g.low.diff()
    pdm = pd.Series(np.where((um > dm) & (um > 0), um, 0.0), index=g.index)
    ndm = pd.Series(np.where((dm > um) & (dm > 0), dm, 0.0), index=g.index)
    pdi, ndi = 100 * wilder(pdm, 14) / a, 100 * wilder(ndm, 14) / a
    return wilder(100 * (pdi - ndi).abs() / (pdi + ndi).replace(0, np.nan), 14)


def _stoch_silang(g, n, x):
    lo, hi = g.low.rolling(n).min(), g.high.rolling(n).max()
    sk = (100 * (g.close - lo) / (hi - lo).replace(0, np.nan)).rolling(3).mean()
    sd = sk.rolling(3).mean()
    return (sk > sd) & (sk.shift() <= sd.shift()) & (sk.shift() < x)


@njit(cache=True)
def pegang_b(ix, o, l, c, atr, sma20):
    """Cara pegang B: stop loss 4xATR14 (hari isyarat); mulai tutup sesi ke-20, jual pada buka esok selepas tutup < purata
    20 hari; paling lama 126 sesi. Pulangkan R, sesi jual, jenis (0 had masa, 1 trend, 2 stop biasa, 3 stop lompat)."""
    n = ix.shape[0]
    R, SK, J = np.empty(n), np.empty(n, np.int64), np.empty(n, np.int64)
    for k in range(n):
        i = ix[k]
        e = i + 1
        P = o[e]
        Ls = P - 4.0 * atr[i]
        if c[e] <= Ls:
            R[k], SK[k], J[k] = o[e + 1] / P - 1.0 - KOS, 1, 3
            continue
        R[k], SK[k], J[k] = c[e + 125] / P - 1.0 - KOS, 125, 0
        for d in range(1, 126):
            b = e + d
            if d >= 20 and c[b - 1] < sma20[b - 1]:
                R[k], SK[k], J[k] = o[b] / P - 1.0 - KOS, d, 1
                break
            if o[b] <= Ls:
                R[k], SK[k], J[k] = o[b] / P - 1.0 - KOS, d, 3
                break
            if l[b] <= Ls:
                R[k], SK[k], J[k] = Ls / P - 1.0 - KOS, d, 2
                break
    return R, SK, J


@njit(cache=True)
def sesi20(ix, o, l, c, atr):
    """Sesi keluar "pegang 20 sesi + stop loss 4xATR14" (hanya untuk peraturan satu posisi)."""
    SK = np.empty(ix.shape[0], np.int64)
    for k in range(ix.shape[0]):
        e = ix[k] + 1
        Ls = o[e] - 4.0 * atr[ix[k]]
        SK[k] = 19
        if c[e] <= Ls:
            SK[k] = 1
            continue
        for d in range(1, 20):
            if o[e + d] <= Ls or l[e + d] <= Ls:
                SK[k] = d
                break
    return SK


@njit(cache=True)
def satu(ix, sk, tid):
    """Satu posisi setiap saham: isyarat semasa saham masih dipegang diabaikan."""
    amb = np.zeros(ix.shape[0], np.bool_)
    t, b = -1, -1
    for k in range(ix.shape[0]):
        if tid[ix[k]] != t or ix[k] > b:
            amb[k] = True
            t, b = tid[ix[k]], ix[k] + 1 + sk[k]
    return amb


def bina_bebas():
    """Bingkai audit kumpulan B + tatasusunan yang dikongsi semua langkah."""
    df, ixd = muat('B')
    df = asas_rawak(sedia(df), LAB)
    df['hingga'], df['ada_e'] = hingga_laporan(df, 'utc20')
    A = {k: df[k].to_numpy(float) for k in ('open', 'low', 'close', 'atr')}
    A['tid'] = df.groupby('ticker', sort=False).ngroup().to_numpy().astype(np.int64)
    A['sma20'] = df.groupby('ticker', sort=False).close.transform(lambda s: s.rolling(20).mean()).to_numpy()
    A['sah'] = df.sah.to_numpy()
    A['sah126'] = A['sah'] & ((df.k + 126) < df['T']).to_numpy()
    A['tarikh'] = (df.date.dt.year * 10000 + df.date.dt.month * 100 + df.date.dt.day).to_numpy()
    A['tempoh'] = np.full(len(df), -1, np.int64)
    for p, (a, z) in enumerate(TEMPOH_B):
        A['tempoh'][(A['tarikh'] >= a) & (A['tarikh'] <= z)] = p
    A['hingga'] = df.hingga.to_numpy()
    A['V'] = {k: df[k].to_numpy(float) for k in LAB + ['a_' + x for x in LAB]}
    # cara pegang B bagi SEMUA bar layak -> asas "saham rawak hari sama, dipegang dengan cara sama"
    semua = np.flatnonzero(A['sah126'])
    Rb, SKb, Jb = pegang_b(semua, A['open'], A['low'], A['close'], A['atr'], A['sma20'])
    g = pd.DataFrame({'date': A['tarikh'][semua], 'terc': df.terc.to_numpy()[semua], 'R': Rb, 'W': (Rb > 0).astype(float),
                      'L': (Rb <= -0.15).astype(float)})
    a = g.groupby(['date', 'terc'])[['R', 'W', 'L']].transform('mean')
    for nm, v in (('RB', Rb), ('aR', a.R.to_numpy()), ('aW', a.W.to_numpy()), ('aL', a.L.to_numpy())):
        A[nm] = np.full(len(df), np.nan)
        A[nm][semua] = v
    A['SKB'], A['JB'] = np.zeros(len(df), np.int64), np.zeros(len(df), np.int64)
    A['SKB'][semua], A['JB'][semua] = SKb, Jb
    A['rawak_B'] = dict(menang=float((Rb > 0).mean()), purata=float(Rb.mean()), rugi15=float((Rb <= -0.15).mean()))
    return df, ixd, A


def ukur(A, ev):
    """Semua ukuran audit bagi satu senarai isyarat (indeks bar, sudah layak)."""
    V, tp = A['V'], A['tempoh']
    e = ev[satu(ev, sesi20(ev, A['open'], A['low'], A['close'], A['atr']), A['tid'])]
    d = dict(n=len(e))
    if not len(e):
        return d, e, e
    for k in LAB:
        d[k], d['a_' + k] = float(V[k][e].mean()), float(V['a_' + k][e].mean())
    d['kl_terus'] = d['terus'] - d['a_terus']
    arah = (V['m5'][e] - V['a_m5'][e]) - (V['j5'][e] - V['a_j5'][e])
    d['arah'], d['r5x'], d['r20x'] = float(arah.mean()), d['r5'] - d['a_r5'], d['r20'] - d['a_r20']
    for p in range(3):
        q = tp[e] == p
        d[f'n_K{p + 1}'] = int(q.sum())
        d[f'kl_terus_K{p + 1}'] = float((V['terus'][e[q]] - V['a_terus'][e[q]]).mean()) if q.any() else np.nan
        d[f'arah_K{p + 1}'] = float(arah[q].mean()) if q.any() else np.nan
    d['esok'] = float((A['hingga'][e] == 1).mean())
    eb = ev[A['sah126'][ev]]
    eb = eb[satu(eb, A['SKB'][eb], A['tid'])]
    if len(eb):
        rb, jb = A['RB'][eb], A['JB'][eb]
        d.update(n_B=len(eb), menang_B=float((rb > 0).mean()), purata_B=float(rb.mean()), rugi15_B=float((rb <= -0.15).mean()),
                 a_menang_B=float(np.nanmean(A['aW'][eb])), a_purata_B=float(np.nanmean(A['aR'][eb])),
                 a_rugi15_B=float(np.nanmean(A['aL'][eb])), stop=float((jb >= 2).mean()), stop_lompat=float((jb == 3).mean()),
                 R_stop_lompat=float(rb[jb == 3].mean()) if (jb == 3).any() else np.nan,
                 R_stop_biasa=float(rb[jb == 2].mean()) if (jb == 2).any() else np.nan)
        for p in range(3):
            q = tp[eb] == p
            ok = q.sum() >= 20
            d[f'menangx_K{p + 1}'] = float((rb[q] > 0).mean() - np.nanmean(A['aW'][eb[q]])) if ok else np.nan
            d[f'puratax_K{p + 1}'] = float(rb[q].mean() - np.nanmean(A['aR'][eb[q]])) if ok else np.nan
    return d, e, eb


# =====================================================================================================================
# Isyarat daripada penjana enjin (pencetus, penapis, prasyarat) -- BUKAN kod bebas
# =====================================================================================================================
def _enjin():
    sys.path.insert(0, SINI)
    import cs_atom as atom
    import cs_cari as cari
    import cs_cs05 as c5
    import cs_lapis as lapis
    import cs_tala7 as t7
    return atom, cari, c5, lapis, t7


def senarai():
    U = pd.read_csv(os.path.join(SINI, 'hasil', 'CS13', 'senarai_utama.csv'))
    reg = pd.read_csv(os.path.join(BS2, 'data', 'registry_F.csv'), dtype=str).fillna('').set_index('id')
    U['takrif'] = [r.takrif if isinstance(r.takrif, str) else reg.loc[r.id, 'takrif'] for r in U.itertuples()]
    U['pencetus'] = U.takrif.str.split('|').str[0]
    return U


def tugas_benih(nama):
    """(nama, modul, parameter) bagi pencetus benih M / N, dibina semula secara deterministik daripada namanya."""
    _, cari, _, _, t7 = _enjin()
    pj = pd.read_csv(os.path.join(AKAR, 'AUTOTUNE', 'kaedah', 'param_julat.csv'))
    nmod = {}
    for f in sorted(glob.glob(os.path.join(BS2, 'kod', 'kaedah', 'N*.py'))):
        mod = os.path.basename(f)[:-3]
        nmod.setdefault(mod.split('X')[0], f'kaedah.{mod}')

    def asas(n):
        mid, v = n.split('.')
        return None if v == '0' else cari.param_varian(pj, mid, int(v))
    out = []
    for n in sorted(nama):
        if n[0] == 'N':
            out.append((n, nmod[n], None))
            continue
        mid, v = n.split('.')
        if 's' in v:                                           # varian setempat CS07: <induk>s<k>
            dasar = f"{mid}.{v.split('s')[0]}"
            out.append([t for t in t7.varian_m2({mid: dasar}, {dasar: asas(dasar)})[0] if t[0] == n][0])
        else:
            out.append((n, mid, asas(n)))
    return out


def modul_intai():
    """Modul kaedah M yang membaca bar ESOK (imbasan sumber): (anjak 'open', indeks tatasusunan, siri kalendar).
    "anjak" = `open.shift(-1)` ditulis terus ATAU melalui fungsi kongsi `_k145.langkau(g, stop)` ("langkau jika buka esok <=
    henti"); kedua-duanya dibetulkan oleh `cs_cari.tanpa_intai()`."""
    anjak, indeks, kal = set(), set(), set()
    for f in glob.glob(os.path.join(AKAR, 'AUTOTUNE', 'kaedah', 'M*.py')):
        s, m = open(f, encoding='utf-8').read(), os.path.basename(f)[:-3]
        if re.search(r'(open|\bo)\.shift\(-', s) or re.search(r'\blangkau\(g', s):
            anjak.add(m)
        if re.search(r'\bo\[i \+ 1\]|open\.values\[i \+ 1\]', s):
            indeks.add(m)
        if re.search(r'(wk|ws|dts)[^\n]*\.shift\(-1\)', s):
            kal.add(m)
    return anjak, indeks, kal


INTAI_LAIN = ('M02', 'M38', 'M40', 'M41', 'M45', 'M81', 'M82', 'M24', 'M50', 'M52')   # tidak dibetulkan `tanpa_intai`


def benih(kerja):
    _, cari, _, _, _ = _enjin()
    U = senarai()
    nama = sorted(set(p for p in U.pencetus if p[0] in 'MN'))
    T = tugas_benih(nama)
    cari.benih(kerja, 'B', tugas=T, fail='benih_B_audit.pkl')
    anjak = modul_intai()[0]
    cari.benih(kerja, 'B', tugas=[t for t in T if t[1] in anjak], fail='benih_B_kausal.pkl', kausal=True)


def isyarat(kerja, kausal=False):
    """dict id setup -> indeks bar isyarat (kumpulan B, layak, selepas penapis dan prasyarat)."""
    atom, cari, c5, lapis, _ = _enjin()
    pan = cari.panel(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr = (L['L1'], L['L2'])
    bn = pickle.load(open(os.path.join(kerja, 'benih_B_audit.pkl'), 'rb'))
    if kausal:
        bn = {'sig': {**bn['sig'], **pickle.load(open(os.path.join(kerja, 'benih_B_kausal.pkl'), 'rb'))['sig']}}
    EV = cari.pencetus(pan, bn)
    EV.update(pickle.load(open(os.path.join(kerja, 'cs07_K_B.pkl'), 'rb'))['ev'])
    kq1, kq2 = [x[:4] for x in lapis.PASARAN], [x[:4] for x in lapis.KUMPULAN]
    out = {}
    for r in senarai().itertuples():
        b = r.takrif.split('|')
        fs = [int(x.split('@')[0][1:]) - 1 for x in b[1].split('+') if x and x != '-'] + [-1, -1]
        q1 = q2 = -1
        for kod in (b[4].split('+') if len(b) > 4 and b[4] else []):
            if kod in kq1:
                q1 = kq1.index(kod)
            else:
                q2 = kq2.index(kod)
        if b[0] in EV:
            ev = EV[b[0]]
            out[r.id] = np.ascontiguousarray(ev[c5.topeng(pan, Lr, ev, q1, q2, fs[0], fs[1])].astype(np.int64))
    return out, pan


# ---------- langkah: setup ----------
def setup(kerja):
    df, _, A = bina_bebas()
    EV, pan = isyarat(kerja)
    assert len(pan['c']) == len(df) and (pan['tarikh'] == A['tarikh']).all() and (pan['ticker'][pan['tid']] == df.ticker.to_numpy()).all()
    beza_sah = int((pan['sah'] != A['sah']).sum())
    log(f"CS19 setup: bar layak enjin {int(pan['sah'].sum()):,} audit {int(A['sah'].sum()):,} beza {beza_sah}")
    EVk, _ = isyarat(kerja, kausal=True)
    U, baris, ENT = senarai(), [], {}
    for r in U.itertuples():
        if r.id not in EV:
            baris.append(dict(id=r.id, diaudit=False))
            continue
        ev = EV[r.id][A['sah'][EV[r.id]]]
        d, e, eb = ukur(A, ev)
        d.update(id=r.id, diaudit=True)
        if not np.array_equal(EV[r.id], EVk[r.id]):
            dk, _, _ = ukur(A, EVk[r.id][A['sah'][EVk[r.id]]])
            d.update({'k_' + k: dk.get(k, np.nan) for k in ('n', 'terus', 'kl_terus', 'menang_B', 'purata_B')})
        ENT[r.id] = (e.astype(np.int32), eb.astype(np.int32))
        baris.append(d)
    pickle.dump({'T': pd.DataFrame(baris), 'ENT': ENT, 'beza_sah': beza_sah, 'rawak_B': A['rawak_B'],
                 'A': {k: A[k] for k in ('V', 'RB', 'aW', 'aR', 'aL', 'SKB', 'tempoh', 'tid', 'hingga', 'sah', 'sah126', 'open',
                                         'low', 'close', 'atr')}}, open(F_(kerja, 'setup'), 'wb'), protocol=4)
    log(f"CS19 setup: {len(baris)} setup, diaudit {sum(1 for b in baris if b['diaudit'])}")


# ---------- langkah: bebas (isyarat pun ditulis semula) ----------
CONTOH = ('F1674', 'F1719', 'F479', 'F571', 'F114', 'F363')


def bebas(kerja):
    df, ix, A = bina_bebas()
    pm = rejim_qqq(df, ix)
    for k in pm:
        df[k] = pm[k].reindex(df.date).to_numpy()
    px = df.pivot(index='date', columns='ticker', values='close')
    rs = (px / px.shift(126) - 1).rank(axis=1, pct=True) * 100
    df['rs'] = rs.stack().rename('rs').reset_index().merge(df[['date', 'ticker']], on=['date', 'ticker'], how='right').rs.to_numpy()
    c, gt = df.close, df.groupby('ticker', sort=False)
    df['ma20'] = gt.close.transform(lambda s: s.rolling(20).mean())
    df['sd20'] = gt.close.transform(lambda s: s.rolling(20).std(ddof=0))
    df['h252'] = gt.high.transform(lambda s: s.rolling(252).max())
    df['rsi2'] = gt.close.transform(lambda s: _rsi(s, 2))
    df['adx'] = per_saham(df, _adx14)
    E15 = (df.hingga >= 1) & (df.hingga <= 5)
    hny, _ = hingga_laporan(df, 'ny')
    bulan = df.date.dt.month
    T = dict(st10=hari_pertama(df, per_saham(df, lambda g: _stoch_silang(g, 14, 10))),
             st40=hari_pertama(df, per_saham(df, lambda g: _stoch_silang(g, 14, 40))),
             jatuh=hari_pertama(df, (c / gt.close.shift(20) - 1) <= -0.10), rsi2=hari_pertama(df, df.rsi2 < 5),
             bb=hari_pertama(df, c < df.ma20 - 2.0 * df.sd20),
             turun=hari_pertama(df, (c < gt.close.shift(1)) & (gt.close.shift(1) < gt.close.shift(2)) & (gt.close.shift(2) < gt.close.shift(3))))
    S = [('F1674', T['st10'] & (df.rs >= 70) & bulan.isin([5, 6, 7, 8, 9, 10]) & E15),
         ('F1719', T['jatuh'] & (df.adx > 25) & df.off & E15), ('F479', T['rsi2'] & df.off_baharu & E15),
         ('F571', T['bb'] & df.off_baharu & E15), ('F114', T['st40'] & (df.rs >= 90) & (c >= 0.85 * df.h252) & E15),
         ('F363', T['turun'] & df.off_baharu & E15),
         ('KAWALAN laporan 1-5 sesi, tiada isyarat beli', E15), ('KAWALAN yang sama, waktu New York', (hny >= 1) & (hny <= 5)),
         ('KAWALAN laporan esok (beli selepas laporan keluar)', df.hingga == 1),
         ('KAWALAN laporan 2-5 sesi lagi', (df.hingga >= 2) & (df.hingga <= 5)),
         ('KAWALAN laporan 6-10 sesi lagi', (df.hingga >= 6) & (df.hingga <= 10)),
         ('KAWALAN tiada laporan dalam 20 sesi', df.ada_e & (df.hingga > 20))]
    U = senarai().set_index('id')
    baris = []
    for nama, isy in S:
        isy = pd.Series(np.asarray(isy), index=df.index).fillna(False).astype(bool)
        d, _, _ = ukur(A, np.flatnonzero((isy & df.sah).to_numpy()))
        d['setup'] = nama
        if nama in U.index:
            d.update(n_enjin=int(U.loc[nama, 'n']), m5_enjin=U.loc[nama, 'm5'], terus_enjin=U.loc[nama, 'terus'], a_terus_enjin=U.loc[nama, 'a_terus'])
        baris.append(d)
        log(nama, d['n'], round(d['m5'] * 100, 2), round(d['terus'] * 100, 2))
    s = df[df.sah]
    r5 = (df.c5 / df.P - 1)[df.sah]
    fs = df.groupby('ticker', sort=False).faktor_split.shift(-20)
    data = dict(saham=int(df.ticker.nunique()), saham_ada_laporan=int(df[df.ada_e].ticker.nunique()), bar_layak=int(df.sah.sum()),
                bar_tanpa_laporan=float((~s.ada_e).mean()), m5_ada=float(s[s.ada_e].m5.mean()), m5_tiada=float(s[~s.ada_e].m5.mean()),
                r5_lebih100=int((r5 > 1.0).sum()), r5_kurang60=int((r5 < -0.6).sum()),
                ohlc_tak_konsisten=int((df.sah & ((df.low > df[['open', 'close']].min(axis=1) + 1e-6)
                                                 | (df.high < df[['open', 'close']].max(axis=1) - 1e-6))).sum()),
                split_dalam_20=int((df.sah & (fs != df.faktor_split) & fs.notna()).sum()),
                saham_bar_terakhir_sebelum_2026_08=int((df.groupby('ticker').date.max() < '2026-08-01').sum()))
    pickle.dump({'T': pd.DataFrame(baris), 'data': data}, open(F_(kerja, 'bebas'), 'wb'), protocol=4)


# ---------- langkah: intai (ujian bar terakhir) ----------
N_SAHAM_INTAI, N_POTONG_INTAI, BENIH_INTAI = 12, 40, 20261116


_I = {}


def _intai_satu(tugas):
    """Satu pencetus benih: (nama, dict hasil). Dijalankan dalam proses pekerja (fork; data dalam _I)."""
    import contextlib
    warnings.filterwarnings('ignore')
    nama, modul, P = tugas
    cari, fr, idx, tick, potong = _I['cari'], _I['fr'], _I['idx'], _I['tick'], _I['potong']
    try:
        m = importlib.import_module(modul)
        if getattr(m, 'SILANG', False):                         # bergantung pada saham lain: ujian ini tidak sah
            return nama, dict(modul=modul, silang=True)
        out = dict(modul=modul, silang=False)
        for mod in (False, True):                               # (asal, tanpa intai)
            f2 = {t: fr[t][cari.LAJUR].copy() for t in tick}
            for t in tick:
                for j, cpt in enumerate(potong[t]):
                    f2[f'{t}#{j}'] = fr[t][cari.LAJUR].iloc[:cpt + 1].copy()
            with (cari.tanpa_intai() if mod else contextlib.nullcontext()):
                m.sedia(f2, idx) if modul.startswith('kaedah.') else m.sedia(f2, idx, P)
            b_ = j_ = 0
            for t in tick:
                penuh = np.asarray(pd.Series(f2[t]['sig']).fillna(False), bool)
                for j, cpt in enumerate(potong[t]):
                    ptg = np.asarray(pd.Series(f2[f'{t}#{j}']['sig']).fillna(False), bool)
                    b_ += int((ptg[-3:] != penuh[cpt - 2:cpt + 1]).sum())
                    j_ += int(ptg[-3:].sum())
            out.update(dict(beza_kausal=b_) if mod else dict(beza=b_, isyarat=j_))
        return nama, out
    except Exception as e:
        return nama, dict(modul=modul, ralat=f'{type(e).__name__}: {str(e)[:80]}')


def intai(kerja):
    """Bagi setiap pencetus benih: isyarat pada 3 bar TERAKHIR data yang dipotong (kebenaran kausal) lawan isyarat pada bar
    yang sama apabila data penuh diberi. Beza > 0 = isyarat bergantung pada bar selepasnya. Salinan dipotong dijalankan
    sebagai "saham" berasingan dalam satu panggilan modul; kedua-dua mod (asal, tanpa intai) diuji."""
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    warnings.filterwarnings('ignore')
    atom, cari, _, _, _ = _enjin()
    import cs_param as kp
    fr, idx, _ = cari.muat_set('B')
    rng = np.random.default_rng(BENIH_INTAI)
    tick = sorted(rng.choice(sorted(t for t in fr if len(fr[t]) > 3500), N_SAHAM_INTAI, replace=False))
    potong = {t: sorted(rng.choice(np.arange(600, len(fr[t]) - 5), N_POTONG_INTAI, replace=False)) for t in tick}
    U = senarai()
    T = tugas_benih(sorted(set(p for p in U.pencetus if p[0] in 'MN')))
    f = F_(kerja, 'intai')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    _I.update(cari=cari, fr={t: fr[t] for t in tick}, idx=idx, tick=tick, potong=potong)
    T = [t for t in T if t[0] not in siap]
    with ProcessPoolExecutor(max_workers=cari.PEKERJA, mp_context=mp.get_context('fork')) as ex:
        for k, (nama, d) in enumerate(ex.map(_intai_satu, T), 1):
            siap[nama] = d
            if k % 25 == 0:
                log(f'  intai {k}/{len(T)}')
                pickle.dump(siap, open(f, 'wb'), protocol=4)
    # keluarga K (656 ahli) + atom P / F / X: pemotongan pada dua tarikh
    G, bK, bP = kp.grid(), 0, 0
    px = pd.DataFrame({t: fr[t].close for t in sorted(fr)})
    for cut in (pd.Timestamp('2016-03-15'), pd.Timestamp('2021-09-10')):
        RS = (px / px.shift(126) - 1).rank(axis=1, pct=True) * 100
        pxc = px[px.index <= cut]
        RSc = (pxc / pxc.shift(126) - 1).rank(axis=1, pct=True) * 100
        on, sa = atom._pasaran(idx)
        onc, sac = atom._pasaran({k_: v[v.index <= cut] for k_, v in idx.items()})
        for t in tick:
            g = fr[t]
            gc = g[g.index <= cut]
            n = len(gc)
            if n < 400:
                continue
            bK += int((kp.kira(g, RS[t].reindex(g.index), G)[:, :n] != kp.kira(gc, RSc[t].reindex(gc.index), G)).sum())
            pa = atom.indikator(g, RS[t].reindex(g.index), on.reindex(g.index).ffill(), sa.reindex(g.index).ffill())
            pb = atom.indikator(gc, RSc[t].reindex(gc.index), onc.reindex(gc.index).ffill(), sac.reindex(gc.index).ffill())
            bP += sum(int((pa[j][k_][:n] != pb[j][k_]).sum()) for j in range(3) for k_ in pa[j])
    siap['_K'] = dict(ahli=len(G), beza=bK, saham=len(tick))
    siap['_PFX'] = dict(beza=bP)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    log(f"CS19 intai: {sum(1 for k_, v in siap.items() if k_[0] != '_' and v.get('beza'))} pencetus benih berbeza; K {bK}; P/F/X {bP}")


# ---------- gred dan laporan ----------
def gredkan(T):
    """Tambah lajur gred (pindaan (ae) A4) kepada jadual audit yang sudah digabung dengan senarai utama dan CS16."""
    b = lambda s: s.astype(str).str.lower().eq('true')
    T['solid'] = b(T.cs16_solid)
    T['rapuh'] = ~b(T.cs16_s1) | ~b(T.cs16_s3) | ~b(T.cs16_s5)
    T['arah3'] = (T[['arah_K1', 'arah_K2', 'arah_K3']] > 0).all(axis=1)
    T['menangx'], T['puratax'], T['rugix'] = T.menang_B - T.a_menang_B, T.purata_B - T.a_purata_B, T.rugi15_B - T.a_rugi15_B
    T['atas_rawak'] = (T.menangx > 0) & (T.puratax > 0)
    T['atas_rawak_K3'] = (T.menangx_K3 > 0) & (T.puratax_K3 > 0)
    T['laporan'] = T.prasyarat.fillna('').str.contains('earnings dalam 1-5')
    T['kalendar'] = T.prasyarat.fillna('').str.contains(KALENDAR)
    anjak, indeks, kal = modul_intai()
    semua_intai = anjak | indeks | kal
    T['intai'] = [p[0] == 'M' and p.split('.')[0] in semua_intai for p in T.pencetus]

    def g(r):
        if not r.diaudit:
            return ''
        if r.rapuh:
            return 'D'
        if r.solid and r.arah3 and r.atas_rawak and r.atas_rawak_K3:
            return 'A'
        return 'B' if (r.arah3 or (r.atas_rawak and r.atas_rawak_K3)) else 'C'

    def nota(r):
        if not r.diaudit:
            return ''
        return ''.join(k for k, ya in (('x', not r.laporan), ('k', r.kalendar), ('i', r.intai),
                                       ('h', str(r.cs16_s5).lower() != 'true'), ('y', str(r.cs16_s3).lower() != 'true'),
                                       ('t', str(r.cs16_s1).lower() != 'true')) if ya)
    T['gred'], T['nota'] = T.apply(g, axis=1), T.apply(nota, axis=1)
    return T


def gabung(Z, nama, ids=None, e=None, eb=None):
    A = Z['A']
    V, tp = A['V'], A['tempoh']
    if ids is not None:
        e = np.unique(np.concatenate([Z['ENT'][i][0] for i in ids])).astype(np.int64)
        eb = np.unique(np.concatenate([Z['ENT'][i][1] for i in ids])).astype(np.int64)
    e = e[satu(e, sesi20(e, A['open'], A['low'], A['close'], A['atr']), A['tid'])]
    eb = eb[satu(eb, A['SKB'][eb], A['tid'])]
    out = []
    for p, nm in ((None, 'semua'), (0, '2010-19'), (1, '2020-24'), (2, '2025-26')):
        x = e if p is None else e[tp[e] == p]
        xb = eb if p is None else eb[tp[eb] == p]
        out.append(dict(kumpulan=nama, tempoh=nm, belian=len(x), tangkap=V['terus'][x].mean(), r_tangkap=V['a_terus'][x].mean(),
                        naik5=V['m5'][x].mean(), r_naik5=V['a_m5'][x].mean(), jatuh5=V['j5'][x].mean(), r_jatuh5=V['a_j5'][x].mean(),
                        minggu1x=V['r5'][x].mean() - V['a_r5'][x].mean(), menang=(A['RB'][xb] > 0).mean(),
                        r_menang=np.nanmean(A['aW'][xb]), purata=A['RB'][xb].mean(), r_purata=np.nanmean(A['aR'][xb]),
                        rugi15=(A['RB'][xb] <= -0.15).mean(), r_rugi15=np.nanmean(A['aL'][xb])))
    return out


def jadual(kerja):
    Z = pickle.load(open(F_(kerja, 'setup'), 'rb'))
    U = senarai()
    S = pd.read_csv(os.path.join(SINI, 'hasil', 'CS16', 'solid.csv.gz')).set_index('id')
    T = U[['kedudukan', 'id', 'asal', 'prasyarat', 'nama', 'penapis', 'pencetus', 'pilihan', 'n', 'm5', 'terus', 'n_B', 'menang_B',
           'purata_B', 'rugi15_B']].rename(columns={k: k + '_enjin' for k in ('n', 'm5', 'terus', 'n_B', 'menang_B', 'purata_B', 'rugi15_B')})
    T = T.merge(Z['T'], on='id', how='left')
    T['diaudit'] = T.diaudit.fillna(False).astype(bool)
    for k in ('solid', 's1', 's3', 's5'):
        T['cs16_' + k] = [S.loc[i, k] if i in S.index else np.nan for i in T.id]
    T['pariti'] = (T.diaudit & (T.n == T.n_enjin) & ((T.m5 - T.m5_enjin).abs() <= TOL) & ((T.terus - T.terus_enjin).abs() <= TOL)
                   & (T.n_B == T.n_B_enjin) & ((T.menang_B - T.menang_B_enjin).abs() <= TOL)
                   & ((T.purata_B - T.purata_B_enjin).abs() <= TOL))
    return gredkan(T), Z


def bacaan(T, G, Z):
    a3 = T[T.kedudukan <= N_ATAS]
    sp = lambda x, y: float(x.rank().corr(y.rank()))
    lalu = (a3.arah_K1 > 0) & (a3.arah_K2 > 0) & (a3.menangx_K1 > 0) & (a3.menangx_K2 > 0) & (a3.puratax_K1 > 0) & (a3.puratax_K2 > 0)
    return dict(
        n_utama=len(T), diaudit=int(T.diaudit.sum()), pariti=int(T.pariti.sum()), pariti_300=int(a3.pariti.sum()),
        beza_bar_layak=int(Z['beza_sah']), rawak_B=Z['rawak_B'],
        gred_300={k: int(v) for k, v in a3.gred.value_counts().sort_index().items()},
        gred_semua={k: int(v) for k, v in T[T.diaudit].gred.value_counts().sort_index().items()},
        kohort=KOHORT, kohort_sama_gred_A_300=sorted(a3[a3.gred == 'A'].id) == sorted(KOHORT),
        laporan_300=int(a3.laporan.sum()), laporan_semua=int(T.laporan.sum()),
        median_300={k: float(a3[k].median()) for k in ('m5', 'a_m5', 'j5', 'a_j5', 'terus', 'a_terus', 'arah', 'menang_B', 'a_menang_B',
                                                         'purata_B', 'a_purata_B', 'rugi15_B', 'a_rugi15_B', 'stop', 'stop_lompat',
                                                         'R_stop_lompat', 'R_stop_biasa', 'esok')},
        arah3_300=int(a3.arah3.sum()), arah_K3_pos_300=int((a3.arah_K3 > 0).sum()),
        spearman_kl=dict(K1_K2=sp(T.kl_terus_K1, T.kl_terus_K2), K1_K3=sp(T.kl_terus_K1, T.kl_terus_K3), K2_K3=sp(T.kl_terus_K2, T.kl_terus_K3)),
        spearman_arah_300=dict(K1_K3=sp(a3.arah_K1, a3.arah_K3), K2_K3=sp(a3.arah_K2, a3.arah_K3)),
        lalu_baik=dict(n=int(lalu.sum()), arah_K3=float(a3[lalu].arah_K3.median()), menangx_K3=float(a3[lalu].menangx_K3.median()),
                       puratax_K3=float(a3[lalu].puratax_K3.median())),
        lalu_lain=dict(n=int((~lalu).sum()), arah_K3=float(a3[~lalu].arah_K3.median()), menangx_K3=float(a3[~lalu].menangx_K3.median()),
                       puratax_K3=float(a3[~lalu].puratax_K3.median())),
        intai_setup=int(T.intai.sum()), intai_300=int(a3.intai.sum()),
        intai_diukur=int(T.k_n.notna().sum()) if 'k_n' in T else 0,
        intai_beza_terus_median=float((T.k_terus - T.terus).median()) if 'k_terus' in T else np.nan,
        intai_beza_terus_maks=float((T.k_terus - T.terus).abs().max()) if 'k_terus' in T else np.nan,
        intai_beza_menang_maks=float((T.k_menang_B - T.menang_B).abs().max()) if 'k_menang_B' in T else np.nan)


def lapor(kerja):
    sys.path.insert(0, os.path.join(BS2, 'standard'))
    T, Z = jadual(kerja)
    a3 = T[T.kedudukan <= N_ATAS]
    A = Z['A']
    G = []
    G += gabung(Z, f'{N_ATAS} teratas', a3[a3.diaudit].id.tolist())
    for g in 'ABCD':
        G += gabung(Z, f'gred {g} ({N_ATAS} teratas)', a3[a3.gred == g].id.tolist())
    G += gabung(Z, '30 teratas ikut kedudukan', T[(T.kedudukan <= 30) & T.diaudit].id.tolist())
    G += gabung(Z, 'semua setup senarai utama yang diaudit', T[T.diaudit].id.tolist())
    for nama, m in (('KAWALAN: semua saham 1-5 sesi sebelum laporan, tiada isyarat beli', (A['hingga'] >= 1) & (A['hingga'] <= 5)),
                    ('KAWALAN: laporan esok (beli selepas laporan keluar)', A['hingga'] == 1),
                    ('KAWALAN: laporan 2-5 sesi lagi', (A['hingga'] >= 2) & (A['hingga'] <= 5))):
        e = np.flatnonzero(A['sah'] & m)
        G += gabung(Z, nama, e=e, eb=e[A['sah126'][e]])
    G = pd.DataFrame(G)
    B = bacaan(T, G, Z)
    Bb = pickle.load(open(F_(kerja, 'bebas'), 'rb'))
    I = pickle.load(open(F_(kerja, 'intai'), 'rb')) if os.path.exists(F_(kerja, 'intai')) else {}
    B['data'] = Bb['data']
    Bt = Bb['T']
    B['bebas_sama'] = int(((Bt.n == Bt.n_enjin) & ((Bt.m5 - Bt.m5_enjin).abs() <= TOL) & ((Bt.terus - Bt.terus_enjin).abs() <= TOL)).sum())
    B['bebas_bil'] = int(Bt.n_enjin.notna().sum())
    It = pd.DataFrame([dict(pencetus=k, **v) for k, v in I.items() if k[0] != '_'])
    if len(It):
        B['intai_ujian'] = dict(pencetus=len(It), berbeza=int((It.get('beza', 0) > 0).sum()),
                                berbeza_selepas_tanpa_intai=int((It.get('beza_kausal', 0) > 0).sum()),
                                K=I.get('_K'), PFX=I.get('_PFX'))
    os.makedirs(HASIL, exist_ok=True)
    lajur = ['kedudukan', 'id', 'diaudit', 'pariti', 'gred', 'nota', 'n', 'm5', 'a_m5', 'j5', 'a_j5', 'm10', 'a_m10', 'j10', 'a_j10', 'terus',
             'a_terus', 'kl_terus', 'arah', 'r5x', 'r20x', 'kl_terus_K1', 'kl_terus_K2', 'kl_terus_K3', 'arah_K1', 'arah_K2', 'arah_K3',
             'n_K3', 'n_B', 'menang_B', 'a_menang_B', 'purata_B', 'a_purata_B', 'rugi15_B', 'a_rugi15_B', 'menangx_K1', 'menangx_K2',
             'menangx_K3', 'puratax_K1', 'puratax_K2', 'puratax_K3', 'stop', 'stop_lompat', 'R_stop_lompat', 'R_stop_biasa', 'esok',
             'solid', 'rapuh', 'arah3', 'atas_rawak', 'atas_rawak_K3', 'laporan', 'kalendar', 'intai', 'k_n', 'k_terus', 'k_kl_terus',
             'k_menang_B', 'k_purata_B']
    for k in lajur:
        if k not in T:
            T[k] = np.nan
    T[lajur].round(5).to_csv(os.path.join(HASIL, 'audit.csv.gz'), index=False)
    G.round(5).to_csv(os.path.join(HASIL, 'gabungan.csv'), index=False)
    Bt.round(5).to_csv(os.path.join(HASIL, 'bebas.csv'), index=False)
    if len(It):
        It.to_csv(os.path.join(HASIL, 'intai.csv'), index=False)
    json.dump(B, open(os.path.join(HASIL, 'bacaan.json'), 'w'), indent=1, ensure_ascii=False, default=float)
    open(os.path.join(HASIL, 'AUDIT.md'), 'w', encoding='utf-8').write(teks(T, G, B, Bt, It))
    log(f"CS19 lapor: pariti {B['pariti']}/{B['diaudit']} diaudit daripada {B['n_utama']}; gred 300 {B['gred_300']}; gred semua {B['gred_semua']}")


def teks(T, G, B, Bt, It):
    try:
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda v, d=0: '–' if v != v else f'{v * 100:.{d}f}'
    pp = lambda v, d=1: '–' if v != v else f'{v * 100:+.{d}f}'
    a3 = T[T.kedudukan <= N_ATAS]
    m, D = B['median_300'], B['data']
    g3 = G[G.kumpulan == f'{N_ATAS} teratas'].set_index('tempoh')
    kw = G[G.kumpulan.str.startswith('KAWALAN: semua saham')].set_index('tempoh')
    iu = B.get('intai_ujian', {})
    L = [f'# CS19: audit bebas senarai utama setup F (backtest; BUKAN bukti)', '', status, '',
         'Peraturan: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (ae). Dijana `cs_audit19.py`; jangan sunting.', '',
         '- Permintaan pengguna 16 Nov 2026: semak satu demi satu setup F teratas sebagai juru audit; "check betul-betul".',
         '- **Urutan sebenar:** audit ini dijalankan dalam chat SEBELUM pindaan (ae) ditulis; takrif gred ditulis sebelum angka setiap '
         'setup dilihat tetapi tidak dikomit dahulu. Gred ialah label maklumat, bukan ujian dikunci.',
         '- Kod audit mengira sendiri bar layak, harga beli, label, saham rawak dan cara pegang daripada harga mentah, tanpa kernel '
         'enjin. Isyarat beli diambil daripada penjana enjin; bagi 6 setup contoh isyarat pun ditulis semula.', '',
         '## 1. Yang betul', '',
         f"- **Pariti:** {B['pariti']:,} daripada {B['diaudit']:,} setup yang diaudit menyamai `hasil/CS13/senarai_utama.csv` (bilangan belian "
         f"sama tepat; kadar tangkap, kadar menang dan purata dalam {TOL * 100:.2f} mata). {N_ATAS} teratas: {B['pariti_300']} daripada "
         f"{int(a3.diaudit.sum())}. Tidak dapat diaudit (pencetus tidak dijana semula): {B['n_utama'] - B['diaudit']}. Bar layak: beza "
         f"{B['beza_bar_layak']} antara enjin dan audit.",
         f"- **Isyarat ditulis semula secara bebas:** {B['bebas_sama']} daripada {B['bebas_bil']} setup contoh sama tepat (`bebas.csv`).",
         f"- **Tengok masa depan:** keluarga K ({(iu.get('K') or {}).get('ahli', 656)} ahli) beza {(iu.get('K') or {}).get('beza', '–')}; "
         f"atom P / penapis / keluar beza {(iu.get('PFX') or {}).get('beza', '–')}; prasyarat dan label disemak dalam kod (tiada anjakan "
         'negatif). Tarikh laporan (8-K butiran 2.02) memakai masa terima: waktu UTC ≥ 20 atau waktu New York ≥ 16:00 memberi '
         'hasil yang sama.',
         f"- **Data:** {D['saham']:,} saham kumpulan B, {D['saham_ada_laporan']:,} ada data laporan ({p(D['bar_tanpa_laporan'], 1)} % bar layak "
         f"tanpa data; kadar asas naik ≥ 5 % sama: {p(D['m5_ada'], 1)} lawan {p(D['m5_tiada'], 1)}). Pulangan 5 hari > +100 %: "
         f"{D['r5_lebih100']} bar daripada {D['bar_layak']:,} (GME, AMC, RGC dan seumpamanya: benar); bar OHLC tidak konsisten: "
         f"{D['ohlc_tak_konsisten']}.", '',
         '## 2. Yang terlepas', '',
         f"1. **Satu idea sahaja.** {B['laporan_300']} daripada {N_ATAS} teratas ({B['laporan_semua']:,} daripada {B['n_utama']:,} semua) = "
         f"\"beli 1–5 sesi sebelum laporan kewangan\". Tanpa isyarat beli, prasyarat itu sahaja: {p(kw.loc['semua', 'naik5'])} naik ≥ 5 % "
         f"daripada 100 (rawak {p(kw.loc['semua', 'r_naik5'], 1)}).",
         f"2. **Jatuh hampir sama banyak.** {N_ATAS} teratas digabung ({int(g3.loc['semua', 'belian']):,} belian unik): naik ≥ 5 % minggu "
         f"pertama {p(g3.loc['semua', 'naik5'])} (rawak {p(g3.loc['semua', 'r_naik5'])}); jatuh ≥ 5 % {p(g3.loc['semua', 'jatuh5'])} (rawak "
         f"{p(g3.loc['semua', 'r_jatuh5'])}). Nilai tengah setiap setup: {p(m['m5'])} lawan {p(m['a_m5'])}; {p(m['j5'])} lawan {p(m['a_j5'])}.",
         f"3. **Menang dan purata hampir sama dengan saham rawak yang dibeli hari sama dan dipegang cara sama.** Gabungan: menang "
         f"{p(g3.loc['semua', 'menang'])} lawan {p(g3.loc['semua', 'r_menang'])}; purata {pp(g3.loc['semua', 'purata'])} % lawan "
         f"{pp(g3.loc['semua', 'r_purata'])} %. Pada 2025–26: {p(g3.loc['2025-26', 'menang'])} lawan {p(g3.loc['2025-26', 'r_menang'])}; "
         f"{pp(g3.loc['2025-26', 'purata'])} % lawan {pp(g3.loc['2025-26', 'r_purata'])} %. (Saham rawak mana-mana hari, cara pegang B: menang "
         f"{p(B['rawak_B']['menang'])}, purata {pp(B['rawak_B']['purata'])} %.)",
         f"4. **Kedudukan tidak stabil.** Korelasi pangkat kelebihan tangkap antara tempoh (semua setup): 2010–19 lawan 2020–24 "
         f"{B['spearman_kl']['K1_K2']:.2f}; 2010–19 lawan 2025–26 {B['spearman_kl']['K1_K3']:.2f}; 2020–24 lawan 2025–26 "
         f"{B['spearman_kl']['K2_K3']:.2f}. Setup yang \"baik dahulu\" ({B['lalu_baik']['n']} daripada {N_ATAS}) pada 2025–26: arah "
         f"{pp(B['lalu_baik']['arah_K3'])}, menang lawan rawak {pp(B['lalu_baik']['menangx_K3'])}; yang lain: {pp(B['lalu_lain']['arah_K3'])}, "
         f"{pp(B['lalu_lain']['menangx_K3'])}.",
         '5. **2025–26 bukan lagi tempoh tidak dilihat** bagi setup berdaftar: ia syarat lulus CS13 (kelebihan > 0 dalam ketiga-tiga '
         'tempoh). Bukti bersih hanya daripada papertrade.',
         f"6. **Tiada saham mati.** {D['saham_bar_terakhir_sebelum_2026_08']} daripada {D['saham']:,} saham berakhir sebelum Ogos 2026. "
         'Angka condong ke atas, terutama setup "≥ 30 % di bawah puncak 52 minggu".',
         f"7. **Intai buka esok.** {B['intai_setup']} setup ({B['intai_300']} dalam {N_ATAS} teratas) memakai pencetus kaedah M yang membaca "
         f"bar esok. Diukur semula tanpa intai: {B['intai_diukur']} setup berubah; kadar tangkap nilai tengah "
         f"{pp(B['intai_beza_terus_median'], 2)} mata, paling besar {p(B['intai_beza_terus_maks'], 1)} mata; kadar menang paling besar "
         f"{p(B['intai_beza_menang_maks'], 1)} mata. Ujian bar terakhir: {iu.get('berbeza', '–')} daripada {iu.get('pencetus', '–')} pencetus "
         f"benih berbeza; selepas mod tanpa intai {iu.get('berbeza_selepas_tanpa_intai', '–')} (modul `INTAI_LAIN` tidak dibetulkan mod itu).",
         f"8. **Stop loss dan hari laporan.** Nilai tengah {N_ATAS} teratas: {p(1 - m['esok'])} % belian dipegang melalui hari laporan; "
         f"{p(m['stop'])} % dagangan kena stop, {p(m['stop_lompat'], 1)} % harganya melompat melepasi paras (rugi purata "
         f"{pp(m['R_stop_lompat'])} % lawan {pp(m['R_stop_biasa'])} % bagi stop biasa).",
         '9. **Nama:** "k tutup menurun berturut" (keluarga K06) bermaksud k − 1 hari turun berturut-turut.', '',
         f'## 3. Gred ({N_ATAS} teratas; label maklumat)', '',
         '| Gred | Bil. | Maksud |', '|---|---|---|',
         f"| A | {B['gred_300'].get('A', 0)} | Solid (CS16), arah > 0 dalam ketiga-tiga tempoh, menang dan purata melebihi rawak termasuk 2025–26 |",
         f"| B | {B['gred_300'].get('B', 0)} | Lulus sebahagian |",
         f"| C | {B['gred_300'].get('C', 0)} | Tangkap saham bergerak besar sahaja |",
         f"| D | {B['gred_300'].get('D', 0)} | Rapuh (gagal S1, S3 atau S5 CS16) |", '',
         f"Semua setup yang diaudit: {B['gred_semua']}. **Gred A bukan bukti** (ia memakai 2025–26). Kohort papertrade = {len(KOHORT)} setup "
         f"gred A dalam {N_ATAS} teratas (sama dengan senarai dikunci pindaan (ae): {'ya' if B['kohort_sama_gred_A_300'] else 'TIDAK'}).", '',
         '## 4. Gabungan belian unik (daripada 100 belian; kurungan = saham rawak hari sama, dipegang cara sama)', '',
         '| Kumpulan | Tempoh | Belian | Tangkap | Naik ≥ 5 % | Jatuh ≥ 5 % | Menang | Purata % | Rugi ≥ 15 % |', '|---|---|---|---|---|---|---|---|---|']
    for r in G.itertuples():
        L.append(f"| {r.kumpulan} | {r.tempoh} | {r.belian:,} | {p(r.tangkap, 1)} ({p(r.r_tangkap, 1)}) | {p(r.naik5, 1)} ({p(r.r_naik5, 1)}) | "
                 f"{p(r.jatuh5, 1)} ({p(r.r_jatuh5, 1)}) | {p(r.menang, 1)} ({p(r.r_menang, 1)}) | {pp(r.purata)} ({pp(r.r_purata)}) | "
                 f"{p(r.rugi15, 1)} ({p(r.r_rugi15, 1)}) |")
    L += ['', f'## 5. {N_ATAS} teratas satu demi satu', '',
          'Tangkap = naik ≥ 5 % minggu pertama dan naik lagi hingga minggu ke-4. Naik:Jatuh = berapa naik ≥ 5 % : berapa jatuh ≥ 5 % minggu '
          'pertama. Kurungan = saham rawak hari sama (dipegang cara sama). Nota: x bukan setup laporan kewangan · k prasyarat kalendar · '
          'i pencetus membaca bar esok · h bergantung beberapa hari · y kalah rawak banyak tahun · t belian terlalu sedikit.', '',
          '| # | ID | Prasyarat | Isyarat beli | Tangkap (rawak) | Naik:Jatuh | Menang (rawak) | Purata % (rawak) | Gred |', '|---|---|---|---|---|---|---|---|---|']
    for r in a3.sort_values('kedudukan').itertuples():
        if not r.diaudit:
            L.append(f'| {r.kedudukan} | `{r.id}` | {r.prasyarat} | {r.nama} | – | – | – | – | tidak diaudit |')
            continue
        L.append(f"| {r.kedudukan} | `{r.id}` | {r.prasyarat if isinstance(r.prasyarat, str) else '–'} | {str(r.nama)[:60]} | {p(r.terus)} ({p(r.a_terus)}) | "
                 f"{p(r.m5)}:{p(r.j5)} | {p(r.menang_B)} ({p(r.a_menang_B)}) | {pp(r.purata_B)} ({pp(r.a_purata_B)}) | {r.gred}{' ' + r.nota if r.nota else ''} |")
    L += ['', '## 6. Fail', '',
          '- `audit.csv.gz`: satu baris setiap setup senarai utama (semua ukuran, gred, nota, versi tanpa intai `k_*`).',
          '- `gabungan.csv`, `bebas.csv`, `intai.csv`, `bacaan.json`.', '']
    return '\n'.join(L)


if __name__ == '__main__':
    {'benih': benih, 'bebas': bebas, 'setup': setup, 'intai': intai, 'lapor': lapor}[sys.argv[1]](sys.argv[2])
