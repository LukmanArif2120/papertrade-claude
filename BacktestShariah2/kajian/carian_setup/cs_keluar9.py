"""Carian setup — pusingan CS09: KELUAR daripada maklumat yang belum dicuba (SPEC pindaan 15 Nov 2026 (r)).

80 atom baharu dalam enam kelas: P pasaran, S sektor/industri, E peristiwa earnings, R relatif kepada pasaran, K kemuncak /
terlalu panas, L keadaan laluan sejak beli. Peraturan: X00, atom baharu tunggal, pasangan baharu x baharu, pasangan
baharu x lama (97 atom CS07) dan SATU penanda aras CS07. Topeng, henti dan statistik = cs_keluar7 (tidak disentuh); hanya
topeng atom baharu dikira di sini (`sedia_baharu`). Mekanik sama: atom dinilai pada tutup sesi d -> jual buka sesi d + 1;
pegang minimum (p); had 20 sesi; kos 0.5 %.
Guna: python3 cs_keluar9.py benihm|atom|cari|pilih|kunci|lapor <kerja>. Jangan sunting keluaran secara manual."""
import multiprocessing as mp
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_param as kp  # noqa: E402

TMAX, NH, NG, NST, HENTI, AKTIF = k7.TMAX, k7.NH, k7.NG, k7.NST, k7.HENTI, k7.AKTIF
N_SEJAGAT, SIMPAN_MIN = 30, 0.90                       # dikunci pindaan (r) (sama seperti (n)(b))
TP_LONGGAR = 0.005                                     # bacaan 2: tp terpilih-R >= tp X00 - 0.5 mata
N_K3_MIN = 30                                          # bacaan K3: setup dengan isyarat K3 >= 30
ARAS7 = ('Y08.10', 'Y09.4')                            # penanda aras: keluar sejagat terbaik CS07 (ATAU, aktif selepas +10 %)
KELAS = {'P': 'pasaran', 'S': 'sektor/industri', 'E': 'peristiwa earnings', 'R': 'relatif kepada pasaran',
         'K': 'kemuncak / terlalu panas', 'L': 'keadaan laluan sejak beli'}
PLASEBO = ('P', 'S', 'E')                              # kelas yang ada plasebo (siri dianjak 437 sesi/bar)
PUS = 'CS09'
S_ARAS = HENTI.index('5xATR14')                        # henti penanda aras CS07


def atom_baharu():
    """Senarai (kod, kelas, jenis, par, par2, teks, spek). jenis 0 = siri setiap bar; 4 = tiada tutup tertinggi baharu k
    sesi; 5 = pulang f daripada untung puncak; 6 = gagal corak (sesi d, ambang x); 7 = lantai untung (a, b); 8 = tutup <
    rendah bar tutup tertinggi; 9 = distribution day saham sejak beli >= k; 10 = Chandelier mengetat ikut masa (k0, k1)."""
    A = []

    def add(kelas, jenis, teks, par=0.0, par2=0.0, **spek):
        A.append((kelas, jenis, float(par), float(par2), teks, spek))
    for kod, teks, tidak in (('QA02', 'QQQ OFF', 0), ('QA04', 'SPY bawah SMA200', 0), ('QA06', 'QQQ >= 10% di bawah puncak', 0),
                             ('QA09', 'rejim OFF baharu (<= 10 sesi)', 0), ('QA10', 'QQQ RSI14 < 35', 0),
                             ('QB01', 'turun-naik SPY 21 hari >= 25% setahun', 0), ('QC02', '<= 30% saham di atas MA50', 0),
                             ('QH03', 'distribution day QQQ >= 5 dalam 25 sesi', 0), ('QH06', 'nisbah 4% (10 hari) < 0.5', 0),
                             ('QH08', 'QQQ SMA10 <= SMA20', 1), ('QB03', 'turun-naik SPY 21 hari >= 63 hari', 1)):
        add('P', 0, f'pasaran: {teks}', lapis=kod, tidak=tidak)
    for n in (10, 20, 50):
        add('P', 0, f'pasaran: QQQ tutup < SMA{n}', q='sma', n=n)
    for n in (5, 10):
        add('P', 0, f'pasaran: QQQ tutup < rendah {n} hari', q='ll', n=n)
    for x in (0.015, 0.025):
        add('P', 0, f'pasaran: QQQ turun >= {x:.1%} sehari', q='r1', x=x)
    for x in (0.03, 0.05):
        add('P', 0, f'pasaran: QQQ turun >= {x:.0%} dalam 5 sesi', q='r5', x=x)
    add('P', 0, 'pasaran: QQQ 3 tutup menurun berturut', q='turun3')
    add('P', 0, 'pasaran: keluasan turun >= 10 mata dalam 10 sesi', q='luas')
    add('S', 0, 'sektor 3 terbawah (pulangan 63 sesi)', lapis2='QD02')
    add('S', 0, 'industri 20% terbawah (pulangan 63 sesi)', lapis2='QE03')
    add('E', 0, 'earnings pada sesi berikutnya (jual sebelum laporan)', e='esok')
    for x in (-0.05, -0.03, 0.0):
        add('E', 0, f'reaksi earnings terakhir (0-5 sesi lalu) <= {x:.0%}', e='reaksi', x=x)
    add('E', 0, 'reaksi earnings terakhir (0-5 sesi lalu) < +3%', e='reaksi_lt', x=0.03)
    add('E', 0, 'hari reaksi earnings (0-5 sesi lalu) tutup < buka', e='merah')
    add('E', 0, '0-10 sesi selepas earnings DAN tutup < tutup sebelum earnings', e='bawah_pra')
    for k in (1, 3, 5):
        add('E', 0, f'{k} hingga 10 sesi selepas reaksi earnings', e='sejak', k=k)
    for k, x in ((5, 0.05), (5, 0.10), (10, 0.10), (10, 0.15)):
        add('R', 0, f'pulangan {k} sesi saham - QQQ <= -{x:.0%}', r='beza', k=k, x=x)
    add('R', 0, 'RS < 70', r='rs')
    for x in (3, 4, 5, 6):
        add('K', 0, f'(tutup - SMA20) / ATR14 >= {x}', k='regang_atr', x=x)
    for x in (0.10, 0.15, 0.20):
        add('K', 0, f'tutup >= {x:.0%} di atas SMA10', k='regang_ma', x=x)
    for x in (2.5, 3.0):
        add('K', 0, f'tutup > jalur atas Bollinger(20, {x})', k='bb', x=x)
    for n in (4, 5, 6):
        add('K', 0, f'{n} tutup naik berturut', k='naik', n=n)
    for x in (0.02, 0.04):
        add('K', 0, f'gap naik >= {x:.0%} DAN tutup < buka', k='gap', x=x)
    add('K', 0, 'julat hari >= 2.5xATR14 DAN tutup dalam separuh bawah julat', k='julat', x=2.5)
    add('K', 0, 'naik >= 2xATR14 sehari dengan volum >= 2x purata 50', k='letus', x=2.0)
    add('K', 0, 'ekor atas >= 60% julat dengan volum >= 1.5x', k='ekor')
    for k in (3, 5, 7, 10):
        add('L', 4, f'tiada tutup tertinggi baharu selama {k} sesi', k)
    for f, t in ((1 / 3, '1/3'), (1 / 2, '1/2'), (2 / 3, '2/3')):
        add('L', 5, f'pulang >= {t} daripada untung puncak', f)
    for d, x in ((5, 0.03), (5, 0.05), (8, 0.05), (10, 0.05), (10, 0.10)):
        add('L', 6, f'gagal corak (selepas {d} sesi, tutup < harga beli +{x:.0%})', d, x)
    for a, b in ((0.05, 0.0), (0.10, 0.03), (0.10, 0.05), (0.15, 0.08), (0.20, 0.10)):
        add('L', 7, f'lantai untung (selepas tutup tertinggi >= +{a:.0%}, tutup < +{b:.0%})', a, b)
    add('L', 8, 'tutup < rendah bar tutup tertinggi sejak beli')
    for k in (2, 3, 4):
        add('L', 9, f'distribution day saham sejak beli >= {k}', k)
    for k0, k1 in ((4, 2), (5, 2.5), (3, 1.5)):
        add('L', 10, f'Chandelier {k0}xATR14 hingga sesi 10, kemudian {k1}xATR14', k0, k1)
    bil, out = {}, []
    for kelas, jenis, par, par2, teks, spek in A:
        bil[kelas] = bil.get(kelas, 0) + 1
        out.append((f'W{kelas}{bil[kelas]:02d}', kelas, jenis, par, par2, teks, spek))
    return out


ATOM9 = atom_baharu()
NB, NL = len(ATOM9), k7.NA                              # 80 baharu, 97 lama
NA = NL + NB                                            # indeks atom: 0..NL-1 lama (cs_keluar7), NL.. baharu
JENIS9 = np.asarray([a[2] for a in ATOM9], np.int64)
PAR9 = np.asarray([a[3] for a in ATOM9])
PAR29 = np.asarray([a[4] for a in ATOM9])
N_SIRI = int((JENIS9 == 0).sum())                       # baris siri atom baharu jenis 0; baris N_SIRI = distribution day saham
BARIS9 = np.where(JENIS9 == 0, np.cumsum(JENIS9 == 0) - 1, np.where(JENIS9 == 9, N_SIRI, 0)).astype(np.int64)
KELAS_ATOM = np.asarray(['lama'] * NL + [a[1] for a in ATOM9])
teks_atom = lambda a: k7.ATOM[a][3] if a < NL else ATOM9[a - NL][5]
kod_atom = lambda a: k7.ATOM[a][0] if a < NL else ATOM9[a - NL][0]


def peraturan9():
    """(a1, a2, op): X00; baharu tunggal; baharu x baharu (ATAU, DAN); baharu x lama (ATAU, DAN); penanda aras CS07."""
    a1, a2, op = [0], [0], [0]
    for a in range(NL, NA):
        a1.append(a), a2.append(a), op.append(1)
    for a in range(NL, NA):
        for b in range(a + 1, NA):
            for o in (2, 3):
                a1.append(a), a2.append(b), op.append(o)
    for a in range(NL, NA):
        for b in range(NL):
            for o in (2, 3):
                a1.append(a), a2.append(b), op.append(o)
    kod = [x[0] for x in k7.ATOM]
    a1.append(kod.index(ARAS7[0])), a2.append(kod.index(ARAS7[1])), op.append(2)
    return np.asarray(a1, np.int64), np.asarray(a2, np.int64), np.asarray(op, np.int64)


A1, A2, OP = peraturan9()
NR = len(A1)
NKOL = NR * NG
KOL_ARAS = (NR - 1) * NG + 2                            # penanda aras CS07 dengan syarat aktif "selepas +10 %"
TUNGGAL = np.flatnonzero(OP == 1)                       # peraturan atom baharu tunggal (indeks peraturan)


def nama_peraturan(kol):
    r, g = divmod(int(kol), NG)
    if OP[r] == 0:
        return 'X00 tiada keluar indikator (henti + 20 sesi)'
    t = teks_atom(A1[r]) if OP[r] == 1 else f"{teks_atom(A1[r])} {'ATAU' if OP[r] == 2 else 'DAN'} {teks_atom(A2[r])}"
    return t if g == 0 else f'{t} [aktif {AKTIF[g]}]'


def kod_peraturan(kol):
    r, g = divmod(int(kol), NG)
    if OP[r] == 0:
        return 'X00'
    t = kod_atom(A1[r]) if OP[r] == 1 else f"{kod_atom(A1[r])} {'ATAU' if OP[r] == 2 else 'DAN'} {kod_atom(A2[r])}"
    return t + ('' if g == 0 else f'@{(5, 10)[g - 1]}')


def kelas_peraturan(kol):
    """Kelas atom dalam peraturan, cth. 'K', 'P+lama', 'E+L'."""
    r = int(kol) // NG
    if OP[r] == 0:
        return 'X00'
    ks = [KELAS_ATOM[A1[r]]] + ([KELAS_ATOM[A2[r]]] if OP[r] > 1 else [])
    return '+'.join(sorted(set(ks), key=lambda k: (k == 'lama', k)))


# ---------- siri atom baharu jenis 0 ----------
def hari_pasaran(kerja):
    """Siri pasaran harian baharu (QQQ, keluasan) atas kesatuan hari panel A dan B. -> cs09_pasaran.pkl"""
    f = os.path.join(kerja, 'cs09_pasaran.pkl')
    if os.path.exists(f):
        return pickle.load(open(f, 'rb'))
    sys.path.insert(0, cari.AKAR)
    from AUTOTUNE.teras import data as D
    pans = {s: cari.panel(kerja, s) for s in ('A', 'B')}
    hu = np.union1d(pans['A']['hari_unik'], pans['B']['hari_unik'])
    atas, semua = np.zeros(len(hu)), np.zeros(len(hu))
    for pan in pans.values():
        hi, ly = np.searchsorted(hu, pan['tarikh']), pan['layak']
        semua += np.bincount(hi[ly], minlength=len(hu))
        atas += np.bincount(hi[ly], (pan['F'][1][ly] > 0).astype(float), minlength=len(hu))
    b50 = pd.Series(atas / np.where(semua > 0, semua, np.nan))
    ix = pd.read_parquet(D.ambil(tag='autotune-data-a02') / 'idx.parquet')
    ix['d'] = ix.date.dt.year * 10000 + ix.date.dt.month * 100 + ix.date.dt.day
    q = ix[ix.ticker == 'QQQ'].set_index('d')[['low', 'close']].reindex(hu).ffill().reset_index(drop=True)
    out = {'hu': hu, 'siri': siri_qqq(q.close, q.low, b50), 'qret': {k: (q.close / q.close.shift(k) - 1).to_numpy() for k in (5, 10)}}
    pickle.dump(out, open(f, 'wb'), protocol=4)
    return out


def siri_qqq(qc, ql, b50):
    """dict (jenis, parameter) -> ndarray bool setiap hari. Hanya data hingga hari itu (tiada pandang hadapan)."""
    S = {}
    for kod, kelas, jenis, par, par2, teks, sp in ATOM9:
        j = sp.get('q')
        if j is None:
            continue
        if j == 'sma':
            s = qc < qc.rolling(sp['n']).mean()
        elif j == 'll':
            s = qc < ql.rolling(sp['n']).min().shift(1)
        elif j == 'r1':
            s = qc / qc.shift(1) - 1 <= -sp['x']
        elif j == 'r5':
            s = qc / qc.shift(5) - 1 <= -sp['x']
        elif j == 'turun3':
            s = (qc < qc.shift(1)) & (qc.shift(1) < qc.shift(2)) & (qc.shift(2) < qc.shift(3))
        else:
            s = b50 - b50.shift(10) <= -0.10
        S[kod] = np.asarray(s.fillna(False), dtype=bool)
    return S


def earnings9(pan):
    """Siri kelas E setiap bar. Indeks peristiwa = sesi reaksi, takrif sama seperti cs_prasyarat.earnings (8-K item 2.02;
    pemfailan selepas 20:00 UTC -> sesi berikutnya)."""
    import cs_prasyarat as pr
    e = pd.read_csv(os.path.join(pr.BS2, 'data', 'sec', 'earnings_8k.csv'), usecols=['saham', 'tarikh_fail', 'masa_terima', 'items'])
    e = e[e['items'].astype(str).str.contains('2.02', regex=False)]
    e['d'] = e.tarikh_fail.str.replace('-', '').astype(int)
    e['lewat'] = pd.to_datetime(e.masa_terima, errors='coerce', utc=True).dt.hour >= 20
    eg = dict(tuple(e.groupby('saham')))
    return earnings_siri(pan, {n: (g.d.to_numpy(), g.lewat.to_numpy()) for n, g in eg.items()})


def earnings_siri(pan, eg):
    """eg: dict ticker -> (tarikh pemfailan yyyymmdd, lewat bool). Pulangkan dict kod atom E -> ndarray bool."""
    E = [a for a in ATOM9 if a[1] == 'E']
    N = len(pan['c'])
    out = {a[0]: np.zeros(N, bool) for a in E}
    o, c, tarikh, mula = pan['o'], pan['c'], pan['tarikh'], pan['mula']
    for t, nama in enumerate(pan['ticker']):
        if nama not in eg:
            continue
        a, b = mula[t], mula[t + 1]
        d, T = tarikh[a:b], b - a
        dd, lewat = eg[nama]
        ev = np.where(lewat, np.searchsorted(d, dd, 'right'), np.searchsorted(d, dd, 'left'))
        ev = np.unique(ev[(ev > 0) & (ev < T)])
        if not len(ev):
            continue
        i = np.arange(T)
        kn = np.searchsorted(ev, i, 'right')                        # peristiwa seterusnya (> i)
        hingga = np.where(kn < len(ev), ev[np.minimum(kn, len(ev) - 1)] - i, 10 ** 6)
        ada_l = kn > 0
        lalu = ev[np.maximum(kn - 1, 0)]                            # sesi reaksi terakhir (<= i)
        sejak = np.where(ada_l, i - lalu, 10 ** 6)
        cs, os_ = c[a:b], o[a:b]
        pra = cs[np.maximum(lalu - 1, 0)]                           # tutup sebelum earnings
        reaksi = np.where(ada_l, cs[lalu] / pra - 1, np.nan)
        for kod, _, _, _, _, _, sp in E:
            j = sp['e']
            if j == 'esok':
                s = hingga == 1
            elif j == 'reaksi':
                s = (sejak <= 5) & (reaksi <= sp['x'])
            elif j == 'reaksi_lt':
                s = (sejak <= 5) & (reaksi < sp['x'])
            elif j == 'merah':
                s = (sejak <= 5) & (cs[lalu] < os_[lalu])
            elif j == 'bawah_pra':
                s = (sejak <= 10) & (cs < pra)
            else:
                s = (sejak >= sp['k']) & (sejak <= 10)
            out[kod][a:b] = s
    return out


def siri_k(g):
    """Matriks boolean [17 atom kelas K + distribution day saham, bar] bagi satu saham."""
    I = kp.Ind(g, None)
    c, o, h, l = I.c, I.o, I.h, I.l
    a14, s20, s10, sd20 = I.atr(14), I.sma(20), I.sma(10), I.sd(20)
    out = []
    for kod, kelas, jenis, par, par2, teks, sp in ATOM9:
        if kelas != 'K':
            continue
        j = sp['k']
        if j == 'regang_atr':
            s = (c - s20) / a14 >= sp['x']
        elif j == 'regang_ma':
            s = c / s10 - 1 >= sp['x']
        elif j == 'bb':
            s = c > s20 + sp['x'] * sd20
        elif j == 'naik':
            u = c > I.pc
            s = u
            for i in range(1, sp['n']):
                s = s & atom._dulu(u, i)
        elif j == 'gap':
            s = (I.gap >= sp['x']) & (c < o)
        elif j == 'julat':
            s = ((h - l) >= sp['x'] * a14) & (I.pos < 0.5)
        elif j == 'letus':
            s = ((c - I.pc) >= sp['x'] * a14) & (I.vr >= 2.0)
        else:
            s = ((h - np.maximum(o, c)) >= 0.6 * (h - l)) & (h > l) & (I.vr >= 1.5)
        out.append(np.asarray(s.fillna(False) if s.dtype != bool else s, dtype=bool))
    dist = (c < I.pc) & (I.v > I.v.shift(1)) & (I.vr >= 1.0)
    out.append(np.asarray(dist.fillna(False) if dist.dtype != bool else dist, dtype=bool))
    return np.stack(out)


_W = {}


def _siri_satu(julat):
    a, b = julat
    return np.concatenate([siri_k(_W['fr'][t]) for t in _W['tick'][a:b]], axis=1).astype(np.uint8)


def beza_qqq(pan, qret_bar, k):
    """Pulangan k sesi saham - pulangan k sesi QQQ, setiap bar (NaN jika k bar lalu bukan saham yang sama)."""
    c = pan['c']
    i = np.arange(len(c))
    lalu = np.maximum(i - k, 0)
    ok = (i - k) >= pan['mula'][pan['tid']]
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.where(ok & (c[lalu] > 0), c / c[lalu] - 1, np.nan)
    return r - qret_bar


def siri_set(kerja, set_):
    """(XB, XBp): matriks uint8 [N_SIRI + 1, bar panel] bagi set A/B; XBp = sama tetapi kelas P, S, E dianjak (plasebo)."""
    f, fp = (os.path.join(kerja, f'cs09_XB{x}_{set_}.npy') for x in ('', 'p'))
    if os.path.exists(f) and os.path.exists(fp):
        return np.load(f, mmap_mode='r'), np.load(fp, mmap_mode='r')
    t0 = time.time()
    pan = cari.panel(kerja, set_)
    N = len(pan['c'])
    L = lapis.muat(kerja, set_)
    H = hari_pasaran(kerja)
    hi = np.searchsorted(H['hu'], pan['tarikh'])
    fr, _, _ = cari.muat_set(set_)
    tick = sorted(fr)
    assert list(pan['ticker']) == tick
    _W.update(fr=fr, tick=tick)
    julat = [(a, min(a + 25, len(tick))) for a in range(0, len(tick), 25)]
    with mp.get_context('fork').Pool(cari.PEKERJA) as pool:
        XK = np.concatenate(list(pool.imap(_siri_satu, julat)), axis=1)
    assert XK.shape[1] == N
    E = earnings9(pan)
    Ep = {k: lapis.anjak_saham(v, pan['mula']) for k, v in E.items()}
    kod1, kod2 = [x[:4] for x in lapis.PASARAN], [x[:4] for x in lapis.KUMPULAN]
    XB, XBp, ik = np.zeros((N_SIRI + 1, N), np.uint8), np.zeros((N_SIRI + 1, N), np.uint8), 0
    for a, (kod, kelas, jenis, par, par2, teks, sp) in enumerate(ATOM9):
        if jenis:
            continue
        r = BARIS9[a]
        if 'lapis' in sp:
            x, xp = L['L1'][kod1.index(sp['lapis'])] > 0, L['L1p'][kod1.index(sp['lapis'])] > 0
            x, xp = (~x, ~xp) if sp['tidak'] else (x, xp)
        elif 'q' in sp:
            x, xp = H['siri'][kod][hi], np.roll(H['siri'][kod], lapis.ANJAK)[hi]
        elif 'lapis2' in sp:
            x, xp = L['L2'][kod2.index(sp['lapis2'])] > 0, L['L2p'][kod2.index(sp['lapis2'])] > 0
        elif 'e' in sp:
            x, xp = E[kod], Ep[kod]
        elif 'r' in sp:
            if sp['r'] == 'beza':
                x = beza_qqq(pan, H['qret'][sp['k']][hi], sp['k']) <= -sp['x']
            else:
                x = pan['F'][15] == 0                                   # BUKAN F16 (RS >= 70)
            xp = x
        else:
            x = xp = XK[ik] > 0
            ik += 1
        XB[r], XBp[r] = x, xp
    XB[N_SIRI] = XBp[N_SIRI] = XK[ik]
    assert ik == XK.shape[0] - 1
    np.save(f, XB), np.save(fp, XBp)
    sah = pan['sah']
    cari.log(f'siri atom keluar baharu {set_}: {XB.shape}, {time.time() - t0:.0f}s; % bar sah benar: '
             + ' '.join(f'{ATOM9[a][0]}={XB[BARIS9[a], sah].mean() * 100:.0f}' for a in range(NB) if JENIS9[a] == 0))
    return np.load(f, mmap_mode='r'), np.load(fp, mmap_mode='r')


# ---------- kernel atom baharu ----------
@njit(parallel=True, cache=True)
def sedia_baharu(ev, o, l, c, atr, XB, jenis, par, par2, baris, baris_dist, pegang_min):
    """Topeng atom baharu M[isyarat, atom] (bit d = benar pada tutup sesi d; d = 0 ialah hari beli). Bit hanya dipasang
    bagi d >= pegang_min - 1 (indikator menjual paling awal pada buka indeks sesi pegang_min), seperti cs_keluar7.sedia."""
    n, nA = ev.shape[0], jenis.shape[0]
    M = np.zeros((n, nA), np.int32)
    for k in prange(n):
        e = ev[k] + 1
        P = o[e]
        hc, d_hc, low_hc, nd = c[e], 0, l[e], 0
        for d in range(TMAX - 1):
            b = e + d
            if c[b] > hc:
                hc, d_hc, low_hc = c[b], d, l[b]
            if XB[baris_dist, b] != 0:
                nd += 1
            for a in range(nA):
                j = jenis[a]
                if j == 0:
                    ya = XB[baris[a], b] != 0
                elif j == 4:
                    ya = (d - d_hc) >= par[a]
                elif j == 5:
                    ya = (hc > P) and (c[b] <= P + (1.0 - par[a]) * (hc - P))
                elif j == 6:
                    ya = (d + 1 >= par[a]) and (c[b] < P * (1.0 + par2[a]))
                elif j == 7:
                    ya = (hc >= P * (1.0 + par[a])) and (c[b] < P * (1.0 + par2[a]))
                elif j == 8:
                    ya = (d > d_hc) and (c[b] < low_hc)
                elif j == 9:
                    ya = nd >= par[a]
                else:
                    ya = c[b] < hc - (par[a] if d + 1 <= 10 else par2[a]) * atr[b]
                if ya and d >= pegang_min - 1:
                    M[k, a] |= (1 << d)
    return M


def sedia_pan(pan, XA, XB, ev, pegang_min=None):
    """(M [isyarat, 97 lama + 80 baharu], ARM, DS, PS, H0, OPN, CF, LAB). Bahagian lama = cs_keluar7.sedia tepat."""
    pm = k7.PEGANG_MIN if pegang_min is None else pegang_min
    ev = np.ascontiguousarray(ev, dtype=np.int64)
    st = k7.sedia_pan(pan, XA, ev, pm)
    Mb = sedia_baharu(ev, pan['o'], pan['l'], pan['c'], pan['atr'], XB, JENIS9, PAR9, PAR29, BARIS9, N_SIRI, pm)
    return (np.ascontiguousarray(np.concatenate([st[0], Mb], axis=1)),) + st[1:]


# ---------- setup yang dinilai ----------
def tugas_m():
    """Tugas benih (nama, modul, P) bagi varian M CS07 yang dipakai setup kedudukan akhir (F88-F95) SAHAJA; parameter
    dijana semula secara deterministik seperti cs_tala7 (varian rawak v3+; varian setempat 's')."""
    import cs_cs07 as c7
    import cs_lapor as lapor
    import cs_tala7 as t7
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('')
    mahu = sorted({c7.dari_takrif7(r.takrif)['pencetus'] for r in reg[reg.pusingan == 'CS07'].itertuples()})
    mahu = [n for n in mahu if n[0] == 'M' and n.split('.')[1] not in ('0', '1', '2')]
    pj = pd.read_csv(os.path.join(cari.AKAR, 'AUTOTUNE', 'kaedah', 'param_julat.csv'))
    par = lambda n: cari.param_varian(pj, n.split('.')[0], int(n.split('.')[1]))
    tugas, terbaik, param = [], {}, {}
    for n in mahu:
        if 's' not in n:
            tugas.append((n, n.split('.')[0], par(n)))
            continue
        ibu = n.split('s')[0]
        assert terbaik.setdefault(ibu.split('.')[0], ibu) == ibu, n       # satu ibu setiap kaedah
        param[ibu] = par(ibu)
    setempat, _ = t7.varian_m2(terbaik, param)
    return tugas + [t for t in setempat if t[0] in mahu]


def benih_m(kerja):
    import cs_tala7 as t7
    tugas = tugas_m()
    cari.log(f"CS09 benih M: {len(tugas)} varian ({', '.join(t[0] for t in tugas)})")
    for s in ('A', 'B'):
        cari.benih(kerja, s, tugas=tugas, fail=t7.FAIL_M.format(s))


def senarai_setup(kerja, set_):
    """(pan, senarai dict {id, ev, aras7}) bagi 69 setup kedudukan akhir. ev = SEMUA isyarat masuk setup pada set itu;
    aras7 = (henti, lajur cs_keluar7) keluar terbaik CS07 setup itu (hasil/CS07/keluar.csv; F88-F95: registry)."""
    import cs_cs05 as c5
    import cs_cs07 as c7
    import cs_lapor as lapor
    import cs_portfolio6 as p6
    import cs_tala7 as t7
    pan = cari.panel(kerja, set_)
    EV = cari.pencetus(pan, pickle.load(open(os.path.join(kerja, f'benih_{set_}.pkl'), 'rb')))
    L = lapis.muat(kerja, set_)
    Lr = (L['L1'], L['L2'])
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    ids = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv')).id.tolist()
    k7csv = pd.read_csv(os.path.join(SINI, 'hasil', 'CS07', 'keluar.csv')).set_index('id')
    out = []
    for i in ids:
        r = reg.loc[i]
        if r.pusingan == 'CS07':
            d = c7.dari_takrif7(r.takrif)
            ev, aras = t7.ev_satu(kerja, set_, d['pencetus']), (d['s'], d['kol'])
        else:
            d = p6.dari_takrif5(r.takrif)
            ev, aras = EV[d['pencetus']], (HENTI.index(k7csv.loc[i, 'henti']), c7._kol(k7csv.loc[i, 'keluar']))
        out.append({'id': i, 'ev': ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])], 'aras7': aras})
    return pan, out


_A1S = np.concatenate([[0], A1[TUNGGAL]])                # plasebo: X00 + atom tunggal sahaja
_A2S, _OPS = _A1S.copy(), np.concatenate([[0], np.ones(NB, np.int64)])


def cari_(kerja):
    """Peringkat cari (kumpulan A, semua isyarat): Acc setiap setup -> kerja/cs09_keluar/<id>_A.npy; plasebo atom tunggal
    -> <id>_Ap.npy."""
    d = os.path.join(kerja, 'cs09_keluar')
    os.makedirs(d, exist_ok=True)
    pan, S = senarai_setup(kerja, 'A')
    XA = k7.siri_set(kerja, 'A')
    XB, XBp = siri_set(kerja, 'A')
    t0 = time.time()
    for k, s in enumerate(S, 1):
        f = os.path.join(d, f"{s['id']}_A.npy")
        if os.path.exists(f):
            continue
        ev = s['ev']
        era = pan['tempoh'][ev].astype(np.int64)
        st = sedia_pan(pan, XA, XB, ev)
        np.save(os.path.join(d, f"{s['id']}_Ap.npy"), k7.kumpul(*sedia_pan(pan, XA, XBp, ev), era, 2, _A1S, _A2S, _OPS))
        np.save(f + '.tmp.npy', k7.kumpul(*st, era, 2, A1, A2, OP))
        os.replace(f + '.tmp.npy', f)
        cari.log(f"  keluar A {k}/{len(S)} {s['id']}: {len(ev):,} isyarat · {time.time() - t0:.0f}s")


def _kadar(Acc):
    """tp, purata [s, kol, era]; beza min-era lawan X00 henti sama (dtp, dR); R pada `terus` (rt); rugi8 [s, kol]."""
    n = np.maximum(Acc[..., 0], 1).astype(np.float64)
    tp, pur = Acc[..., 1] / n, Acc[..., 5] / n
    return (tp, pur, (tp - tp[:, :1]).min(-1), (pur - pur[:, :1]).min(-1), Acc[..., 7].astype(np.float64).sum(-1),
            Acc[..., 3].sum(-1) / n.sum(-1))


def _sejagat(D, DR, RT, kol_sah):
    """Senarai T dan R (30 teratas setiap satu) daripada purata merentas setup; kol_sah = topeng lajur calon."""
    simpan = RT / np.where(RT[:, :1] > 0, RT[:, :1], np.nan)
    lulus = (simpan >= SIMPAN_MIN) & kol_sah[None, :]
    nk = D.shape[1]
    ambil = lambda skor, k=N_SEJAGAT: [(int(f // nk), int(f % nk)) for f in np.argsort(-skor, axis=None, kind='stable')[:k]
                                       if np.isfinite(skor.flat[f])]
    return ambil(np.where(lulus, D, -np.inf)), ambil(np.where(lulus & (D >= 0), DR, -np.inf)), simpan, lulus


def pilih(kerja):
    """Peringkat pilih (kumpulan A sahaja): senarai sejagat T dan R, pilihan setiap setup, atom tunggal terbaik setiap
    kelas (sebenar dan plasebo). -> cs09_pilih.pkl"""
    d = os.path.join(kerja, 'cs09_keluar')
    ids = sorted(f[:-6] for f in os.listdir(d) if f.endswith('_A.npy'))
    D, DR, RT = np.zeros((NH, NKOL)), np.zeros((NH, NKOL)), np.zeros((NH, NKOL))
    nkp = (NB + 1) * NG
    Dp, DRp, RTp = np.zeros((NH, nkp)), np.zeros((NH, nkp)), np.zeros((NH, nkp))
    for i in ids:
        _, _, dtp, dr, rt, _ = _kadar(np.load(os.path.join(d, f'{i}_A.npy')))
        D += dtp
        DR += dr
        RT += rt
        _, _, dtp, dr, rt, _ = _kadar(np.load(os.path.join(d, f'{i}_Ap.npy')))
        Dp += dtp
        DRp += dr
        RTp += rt
    D, DR, Dp, DRp = D / len(ids), DR / len(ids), Dp / len(ids), DRp / len(ids)
    bukan_x00 = np.arange(NKOL) >= NG
    sejT, sejR, simpan_s, lulus = _sejagat(D, DR, RT, bukan_x00)
    # atom tunggal terbaik setiap kelas (maklumat): sebenar pada ruang penuh, plasebo pada ruang tunggal
    kelas, kelas_p = {}, {}
    for kl in KELAS:
        ra = np.asarray([r for r in TUNGGAL if KELAS_ATOM[A1[r]] == kl])
        m = np.zeros(NKOL, bool)
        m[(ra[:, None] * NG + np.arange(NG)[None, :]).ravel()] = True
        t, r_, _, _ = _sejagat(D, DR, RT, m)
        kelas[kl] = {'T': t[0] if t else None, 'R': r_[0] if r_ else None}
        if kl in PLASEBO:
            mp_ = np.zeros(nkp, bool)
            mp_[((ra - TUNGGAL[0] + 1)[:, None] * NG + np.arange(NG)[None, :]).ravel()] = True
            t, r_, _, _ = _sejagat(Dp, DRp, RTp, mp_)
            kelas_p[kl] = {'T': t[0] if t else None, 'R': r_[0] if r_ else None,
                           'D_T': float(Dp[t[0]]) if t else np.nan, 'D_R': float(DRp[r_[0]]) if r_ else np.nan}
    P = {}
    for i in ids:
        tp, pur, dtp, dr, rt, rugi = _kadar(np.load(os.path.join(d, f'{i}_A.npy')))
        simpan = rt / np.where(rt[:, :1] > 0, rt[:, :1], np.nan)
        tpm, purm = tp.min(-1), pur.min(-1)
        bT = kT = None
        for s, kol in [(s, 0) for s in range(NH)] + sejT + [(s, KOL_ARAS) for s in range(NH)]:
            if kol and not (simpan[s, kol] >= SIMPAN_MIN):
                continue
            k_ = (float(tpm[s, kol]), -float(rugi[s, kol]))
            if kT is None or k_ > kT:
                bT, kT = (s, kol), k_
        bR = kR = None
        for s, kol in [(s, 0) for s in range(NH)] + sejR:
            if kol and not ((simpan[s, kol] >= SIMPAN_MIN) and (tpm[s, kol] >= tpm[s, 0])):
                continue
            if kR is None or float(purm[s, kol]) > kR:
                bR, kR = (s, kol), float(purm[s, kol])
        P[i] = {'T': bT, 'R': bR, 'tp_A': kT[0], 'tp_X00_A': float(tpm[bT[0], 0]), 'pur_A': kR,
                'pur_X00_A': float(purm[bR[0], 0])}
    g = lambda M_, L_: [float(M_[x]) for x in L_]
    out = {'ids': ids, 'sejT': sejT, 'sejR': sejR, 'D_T': g(D, sejT), 'simpan_T': g(simpan_s, sejT), 'D_R': g(DR, sejR),
           'Dtp_R': g(D, sejR), 'simpan_R': g(simpan_s, sejR), 'n_lulus': int(lulus.sum()), 'setup': P, 'kelas': kelas,
           'kelas_p': kelas_p, 'kelas_D': {kl: {j: (float((D if j == 'T' else DR)[v[j]]) if v[j] else np.nan) for j in 'TR'}
                                           for kl, v in kelas.items()},
           'D_aras': float(D[S_ARAS, KOL_ARAS]), 'DR_aras': float(DR[S_ARAS, KOL_ARAS]), 'simpan_aras': float(simpan_s[S_ARAS, KOL_ARAS]),
           'D_tanpa_syarat': float(np.max(np.where(bukan_x00[None, :], D, -np.inf)))}
    pickle.dump(out, open(os.path.join(kerja, 'cs09_pilih.pkl'), 'wb'), protocol=4)
    cari.log(f"pilih keluar CS09: {len(ids)} setup; {out['n_lulus']:,} daripada {NH * (NKOL - NG):,} calon lulus syarat simpan")
    cari.log(f"  T#1 {HENTI[sejT[0][0]]} · {nama_peraturan(sejT[0][1])} (+{out['D_T'][0] * 100:.2f} mata tp); penanda aras CS07 "
             f"+{out['D_aras'] * 100:.2f}")
    if sejR:
        cari.log(f"  R#1 {HENTI[sejR[0][0]]} · {nama_peraturan(sejR[0][1])} (+{out['D_R'][0] * 100:.2f} mata purata)")
    return out


def _ring(u):
    """Ringkasan k7._ukur: semua isyarat (semua tempoh dan K3) + satu posisi setiap saham."""
    return {'semua': u[('semua', -1)], 'K3': u[('semua', 2)], 'satu': u[('satu', -1)]}


def kunci(kerja):
    """Peringkat semak pada kumpulan B. -> cs09_kunci.pkl"""
    S0 = pickle.load(open(os.path.join(kerja, 'cs09_pilih.pkl'), 'rb'))
    pan, S = senarai_setup(kerja, 'B')
    XA = k7.siri_set(kerja, 'B')
    XB, XBp = siri_set(kerja, 'B')
    out, t0 = {}, time.time()
    if os.environ.get('CS09_UJI'):                                  # uji kering laluan kod sahaja
        S = S[:int(os.environ['CS09_UJI'])]
    for s_ in S:
        i, ev = s_['id'], s_['ev']
        if i not in S0['setup'] or len(ev) < 30:
            continue
        M, ARM, DS, PS, H0, OPN, CF, LAB = sedia_pan(pan, XA, XB, ev)
        u = lambda s, kol: _ring(k7._ukur(pan, ev, *k7.hasil(M, ARM, DS, PS, H0, OPN, CF, A1, A2, OP, s, kol), LAB))
        x00 = {s: u(s, 0) for s in range(NH)}
        p = S0['setup'][i]
        Ml = np.ascontiguousarray(M[:, :NL])
        r = {'n': len(ev), 'x00': x00, 'T': u(*p['T']), 'R': u(*p['R']),
             'aras7': _ring(k7._ukur(pan, ev, *k7.hasil(Ml, ARM, DS, PS, H0, OPN, CF, k7.A1, k7.A2, k7.OP, *s_['aras7']), LAB)),
             'aras_sejagat': u(S_ARAS, KOL_ARAS),
             'sejT': [u(a, b) for a, b in S0['sejT']], 'sejR': [u(a, b) for a, b in S0['sejR']],
             'kelas': {kl: {j: (u(*v[j]) if v[j] else None) for j in 'TR'} for kl, v in S0['kelas'].items()}}
        Mp = sedia_pan(pan, XA, XBp, ev)[0]
        up = lambda s, kol: _ring(k7._ukur(pan, ev, *k7.hasil(Mp, ARM, DS, PS, H0, OPN, CF, _A1S, _A2S, _OPS, s, kol), LAB))
        r['kelas_p'] = {kl: {j: (up(*v[j]) if v[j] else None) for j in 'TR'} for kl, v in S0['kelas_p'].items()}
        out[i] = r
    pickle.dump(out, open(os.path.join(kerja, 'cs09_kunci.pkl'), 'wb'), protocol=4)
    cari.log(f'kunci keluar CS09: {len(out)} setup · {time.time() - t0:.0f}s')
    return out


# ---------- laporan ----------
def bacaan(T):
    """Dua bacaan dikunci pindaan (r) daripada jadual setiap setup (kumpulan B). Pulangkan dict."""
    med = lambda s: float(s.median()) if len(s) else np.nan
    k3 = T[T.n_K3 >= N_K3_MIN]
    b1 = (T.tp_T > T.tp_x00T) & (T.tp_T > T.tp_aras7)
    b2 = (T.pur_R > T.pur_x00R) & (T.rugi8_R < T.rugi8_x00R) & (T.tp_R >= T.tp_x00R - TP_LONGGAR)
    o = {'n': len(T), 'n1': int(b1.sum()), 'atas_x00': int((T.tp_T > T.tp_x00T).sum()), 'atas_aras7': int((T.tp_T > T.tp_aras7).sum()),
         'simpan_T': med(T.simpan_T), 'd_rugi_T': med(T.rugi8_T - T.rugi8_aras7), 'n_k3': len(k3),
         'k3_T': med(k3.tp_K3_T - k3.tp_K3_x00T), 'n2': int(b2.sum()), 'simpan_R': med(T.simpan_R),
         'k3_R': med(k3.pur_K3_R - k3.pur_K3_x00R)}
    o['ya1'] = bool(o['n1'] > o['n'] / 2 and o['simpan_T'] >= SIMPAN_MIN and o['d_rugi_T'] <= 0.01 and o['k3_T'] > 0)
    o['ya2'] = bool(o['n2'] > o['n'] / 2 and o['simpan_R'] >= SIMPAN_MIN and o['k3_R'] > 0)
    return o


def jadual(S0, K):
    """Satu baris setiap setup (kumpulan B, semua isyarat; perbandingan berpasangan)."""
    baris = []
    for i, r in K.items():
        p = S0['setup'][i]
        (sT, kT), (sR, kR) = p['T'], p['R']
        t, x, a7, rr, xr = r['T'], r['x00'][sT], r['aras7'], r['R'], r['x00'][sR]
        g, k3 = (lambda m, k: m['semua'][k]), (lambda m, k: m['K3'][k])
        nis = lambda m, m0: g(m, 'R_terus') / g(m0, 'R_terus') if g(m0, 'R_terus') > 0 else np.nan
        baris.append(dict(
            id=i, n=r['n'], n_K3=k3(t, 'n'),
            henti_T=HENTI[sT], keluar_T=kod_peraturan(kT), keluar_T_teks=nama_peraturan(kT), kelas_T=kelas_peraturan(kT),
            tp_T=g(t, 'tp'), tp_x00T=g(x, 'tp'), tp_aras7=g(a7, 'tp'), simpan_T=nis(t, x),
            rugi8_T=g(t, 'rugi8'), rugi8_x00T=g(x, 'rugi8'), rugi8_aras7=g(a7, 'rugi8'),
            menang_T=g(t, 'menang'), menang_aras7=g(a7, 'menang'), pur_T=g(t, 'purata'), pur_aras7=g(a7, 'purata'),
            kurang_T=g(t, 'kurang'), kurang_x00T=g(x, 'kurang'), pegang_T=g(t, 'pegang'), pegang_x00T=g(x, 'pegang'),
            tp_K3_T=k3(t, 'tp'), tp_K3_x00T=k3(x, 'tp'), tp_K3_aras7=k3(a7, 'tp'),
            henti_R=HENTI[sR], keluar_R=kod_peraturan(kR), keluar_R_teks=nama_peraturan(kR), kelas_R=kelas_peraturan(kR),
            pur_R=g(rr, 'purata'), pur_x00R=g(xr, 'purata'), rugi8_R=g(rr, 'rugi8'), rugi8_x00R=g(xr, 'rugi8'),
            tp_R=g(rr, 'tp'), tp_x00R=g(xr, 'tp'), simpan_R=nis(rr, xr), menang_R=g(rr, 'menang'), menang_x00R=g(xr, 'menang'),
            pegang_R=g(rr, 'pegang'), pur_K3_R=k3(rr, 'purata'), pur_K3_x00R=k3(xr, 'purata'),
            satu_n=t['satu']['n'], satu_tp_T=t['satu']['tp'], satu_pur_R=rr['satu']['purata'], satu_rugi8_R=rr['satu']['rugi8'],
            tp_A=p['tp_A'], tp_X00_A=p['tp_X00_A'], pur_A=p['pur_A'], pur_X00_A=p['pur_X00_A']))
    return pd.DataFrame(baris)


def _sej_b(K, senarai, kunci_, j):
    """Bagi setiap peraturan sejagat: purata merentas setup B bagi (ukuran - X00 henti sama), % setup lebih baik, nisbah
    simpan jumlah, dan purata beza K3 (setup dengan isyarat K3 >= N_K3_MIN)."""
    out = []
    for q, (s, kol) in enumerate(senarai):
        m = [(r[kunci_][q] if q is not None else None, r['x00'][s]) for r in K.values()]
        out.append(_beza(m, j))
    return out


def _beza(m, j):
    m = [(a, b) for a, b in m if a is not None]
    if not m:
        return (np.nan,) * 5
    dl = np.asarray([a['semua'][j] - b['semua'][j] for a, b in m])
    rt = sum(a['semua']['R_terus'] * a['semua']['n_terus'] for a, _ in m if a['semua']['n_terus'])
    rx = sum(b['semua']['R_terus'] * b['semua']['n_terus'] for _, b in m if b['semua']['n_terus'])
    k3 = [a['K3'][j] - b['K3'][j] for a, b in m if a['K3']['n'] >= N_K3_MIN]
    dr = np.asarray([a['semua']['rugi8'] - b['semua']['rugi8'] for a, b in m])
    return float(dl.mean()), float((dl > 0).mean()), rt / rx if rx else np.nan, float(np.mean(k3)) if k3 else np.nan, float(dr.mean())


def lapor_(kerja):
    """hasil/CS09/KELUAR.md, keluar.csv (setiap setup) dan sejagat.csv (senarai T, R dan penanda aras) daripada cs09_pilih.pkl +
    cs09_kunci.pkl."""
    import cs_lapor as lapor
    S0 = pickle.load(open(os.path.join(kerja, 'cs09_pilih.pkl'), 'rb'))
    K = pickle.load(open(os.path.join(kerja, 'cs09_kunci.pkl'), 'rb'))
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    p = lambda x, k=1, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    T = jadual(S0, K)
    T.to_csv(os.path.join(d_, 'keluar.csv'), index=False, float_format='%.5f')
    B = bacaan(T)
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    sT, sR = _sej_b(K, S0['sejT'], 'sejT', 'tp'), _sej_b(K, S0['sejR'], 'sejR', 'purata')
    aras = _beza([(r['aras_sejagat'], r['x00'][S_ARAS]) for r in K.values()], 'tp')
    rek = [dict(senarai='T', kedudukan=j, henti=HENTI[s], keluar=kod_peraturan(kol), keluar_teks=nama_peraturan(kol),
                kelas=kelas_peraturan(kol), A_tambah=dA, A_simpan=sA, B_tambah=b[0], B_setup_lebih_baik=b[1], B_simpan=b[2],
                K3_tambah=b[3], B_beza_rugi8=b[4])
           for j, ((s, kol), dA, sA, b) in enumerate(zip(S0['sejT'], S0['D_T'], S0['simpan_T'], sT), 1)]
    rek += [dict(senarai='R', kedudukan=j, henti=HENTI[s], keluar=kod_peraturan(kol), keluar_teks=nama_peraturan(kol),
                 kelas=kelas_peraturan(kol), A_tambah=dA, A_simpan=sA, B_tambah=b[0], B_setup_lebih_baik=b[1], B_simpan=b[2],
                 K3_tambah=b[3], B_beza_rugi8=b[4])
            for j, ((s, kol), dA, sA, b) in enumerate(zip(S0['sejR'], S0['D_R'], S0['simpan_R'], sR), 1)]
    rek.append(dict(senarai='aras CS07', kedudukan=0, henti=HENTI[S_ARAS], keluar=kod_peraturan(KOL_ARAS),
                    keluar_teks=nama_peraturan(KOL_ARAS), kelas='lama', A_tambah=S0['D_aras'], A_simpan=S0['simpan_aras'],
                    B_tambah=aras[0], B_setup_lebih_baik=aras[1], B_simpan=aras[2], K3_tambah=aras[3], B_beza_rugi8=aras[4]))
    pd.DataFrame(rek).to_csv(os.path.join(d_, 'sejagat.csv'), index=False, float_format='%.5f')
    kom = lambda L_: ', '.join(f'{k} {v}' for k, v in pd.Series([kelas_peraturan(kol) for _, kol in L_]).value_counts().items())
    A = ['# CS09: KELUAR daripada maklumat yang belum dicuba — pasaran, sektor, earnings, relatif, kemuncak, laluan (backtest; BUKAN bukti)',
         '', status, '',
         'Dijana `kajian/carian_setup/cs_keluar9.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (r), dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.**', '',
         '## 1. Apa yang dicari', '',
         f'- CS07 mencari keluar daripada harga/volum saham itu sendiri sahaja ({NL} atom). Pusingan ini menambah **{NB} atom '
         'baharu dalam enam kelas**: ' + '; '.join(f'{k} = {v} ({int((KELAS_ATOM == k).sum())})' for k, v in KELAS.items()) + '.',
         f'- {NR:,} peraturan (atom baharu tunggal, pasangan baharu × baharu, pasangan baharu × lama, dan penanda aras CS07) × 3 '
         f'syarat aktif × {NH} henti = **{NH * NKOL:,} cara keluar setiap setup**, bagi {len(S0["ids"])} setup, dipilih pada '
         'kumpulan A sahaja.',
         '- Ukuran sama seperti CS07: **tangkap penuh** = naik ≥ 5 % minggu pertama DAN dijual dengan untung ≥ 10 %; syarat '
         f'"tidak jual awal" (untung pada saham yang terus naik ≥ {SIMPAN_MIN:.0%} daripada "pegang sahaja 20 sesi"). '
         f'{S0["n_lulus"]:,} cara lulus syarat itu pada A.',
         '- Pegang minimum 3 sesi terpakai: indikator keluar menjual paling awal pada buka sesi ke-4; henti rugi kekal aktif.', '',
         '## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)', '',
         '**Bacaan 1 — item 4 matlamat ("indikator yang memberitahu kenaikan sudah tamat"):**', '',
         f"- Keluar terpilih mengatasi `X00` (pegang sahaja, henti sama): **{B['atas_x00']} daripada {B['n']}** setup; mengatasi "
         f"keluar terbaik CS07: **{B['atas_aras7']} daripada {B['n']}**; mengatasi kedua-duanya: **{B['n1']} daripada {B['n']}** "
         f"(perlu lebih separuh).",
         f"- Nisbah simpan (median): {B['simpan_T']:.2f} (perlu ≥ {SIMPAN_MIN:.2f}). Rugi ≥ 8 %: median beza lawan keluar terbaik "
         f"CS07 {B['d_rugi_T'] * 100:+.1f} mata (perlu ≤ +1.0).",
         f"- 2025–26 (K3, tahun yang carian tidak lihat; {B['n_k3']} setup dengan ≥ {N_K3_MIN} isyarat): median tambahan tangkap "
         f"penuh lawan pegang sahaja {B['k3_T'] * 100:+.2f} mata (perlu > 0).",
         f"- Median tangkap penuh: pegang sahaja {p(T.tp_x00T.median())} % → keluar terbaik CS07 {p(T.tp_aras7.median())} % → "
         f"keluar terpilih CS09 **{p(T.tp_T.median())} %**.",
         f"- **Keputusan bacaan 1: keluar baharu {'MENOLONG' if B['ya1'] else 'TIDAK menolong'}.**", '',
         '**Bacaan 2 — sisi rugi (BUKAN item 4; adakah keluar baharu mengurangkan rugi tanpa menjual pelari):**', '',
         f"- Purata dagangan lebih tinggi DAN rugi ≥ 8 % lebih rendah daripada pegang sahaja (henti sama), tanpa mengurangkan "
         f"tangkap penuh lebih 0.5 mata: **{B['n2']} daripada {B['n']}** setup (perlu lebih separuh).",
         f"- Nisbah simpan (median): {B['simpan_R']:.2f}. 2025–26: median tambahan purata dagangan {B['k3_R'] * 100:+.2f} mata "
         "(perlu > 0).",
         f"- Median merentas setup: purata dagangan pegang sahaja {p(T.pur_x00R.median(), 2, True)} % → terpilih "
         f"**{p(T.pur_R.median(), 2, True)} %**; rugi ≥ 8 % {p(T.rugi8_x00R.median())} % → **{p(T.rugi8_R.median())} %**; menang "
         f"{p(T.menang_x00R.median(), 0)} % → {p(T.menang_R.median(), 0)} %.",
         f"- **Keputusan bacaan 2: potong rugi {'MENOLONG' if B['ya2'] else 'TIDAK menolong'}.**", '',
         '## 3. Keluar sejagat ikut tangkap penuh (senarai T; 10 teratas daripada 30; dipilih pada A, disemak pada B)', '',
         f'Komposisi kelas 30 teratas: {kom(S0["sejT"])}. Penanda aras CS07 ({HENTI[S_ARAS]} · {nama_peraturan(KOL_ARAS)}): A '
         f'{S0["D_aras"] * 100:+.2f} mata, B {aras[0] * 100:+.2f} mata ({aras[1]:.0%} setup lebih baik), 2025–26 {aras[3] * 100:+.2f}.', '',
         '| # | Henti | Peraturan keluar | Kelas | A: tambahan tangkap penuh (mata) | A: nisbah simpan | B: tambahan (mata) | B: % setup lebih baik | B: nisbah simpan | 2025–26: tambahan |',
         '|---' * 10 + '|']
    for j, ((s, kol), dA, sA, b) in enumerate(list(zip(S0['sejT'], S0['D_T'], S0['simpan_T'], sT))[:10], 1):
        A.append(f'| {j} | {HENTI[s]} | {nama_peraturan(kol)} | {kelas_peraturan(kol)} | {dA * 100:+.2f} | {sA:.2f} | {b[0] * 100:+.2f} | '
                 f'{b[1]:.0%} | {b[2]:.2f} | {b[3] * 100:+.2f} |')
    A += ['', '## 4. Keluar sejagat ikut sisi rugi (senarai R; 10 teratas daripada 30)', '',
          f'Komposisi kelas 30 teratas: {kom(S0["sejR"]) if S0["sejR"] else "tiada calon lulus"}.', '',
          '| # | Henti | Peraturan keluar | Kelas | A: tambahan purata dagangan (mata) | A: tambahan tangkap penuh | A: nisbah simpan | B: tambahan purata | B: % setup lebih baik | B: beza rugi ≥ 8 % | B: nisbah simpan | 2025–26: tambahan purata |',
          '|---' * 12 + '|']
    for j, ((s, kol), dA, tA, sA, b) in enumerate(list(zip(S0['sejR'], S0['D_R'], S0['Dtp_R'], S0['simpan_R'], sR))[:10], 1):
        A.append(f'| {j} | {HENTI[s]} | {nama_peraturan(kol)} | {kelas_peraturan(kol)} | {dA * 100:+.2f} | {tA * 100:+.2f} | {sA:.2f} | '
                 f'{b[0] * 100:+.2f} | {b[1]:.0%} | {b[4] * 100:+.1f} | {b[2]:.2f} | {b[3] * 100:+.2f} |')
    A += ['', '## 5. Setiap kelas maklumat: atom tunggal terbaik (dipilih pada A; maklumat, bukan bacaan)', '',
          'Plasebo = siri yang sama dianjak 437 sesi (kelas P, S, E sahaja): jika plasebo sama baik, kelas itu tidak membawa maklumat.', '',
          '| Kelas | Ikut | Atom tunggal terbaik (henti) | A (mata) | B (mata) | B: % setup lebih baik | B: nisbah simpan | 2025–26 | Plasebo: A / B |',
          '|---' * 9 + '|']
    for kl, nama in KELAS.items():
        for j, uk, label in (('T', 'tp', 'tangkap penuh'), ('R', 'purata', 'purata dagangan')):
            v = S0['kelas'][kl][j]
            if v is None:
                A.append(f'| {kl} {nama} | {label} | tiada yang lulus syarat | – | – | – | – | – | – |')
                continue
            b = _beza([(r['kelas'][kl][j], r['x00'][v[0]]) for r in K.values()], uk)
            pl = '–'
            if kl in S0['kelas_p'] and S0['kelas_p'][kl][j] is not None:
                vp = S0['kelas_p'][kl][j]
                bp = _beza([(r['kelas_p'][kl][j], r['x00'][vp[0]]) for r in K.values()], uk)
                pl = f"{S0['kelas_p'][kl]['D_' + j] * 100:+.2f} / {bp[0] * 100:+.2f}"
            A.append(f"| {kl} {nama} | {label} | {nama_peraturan(v[1])} ({HENTI[v[0]]}) | {S0['kelas_D'][kl][j] * 100:+.2f} | "
                     f"{b[0] * 100:+.2f} | {b[1]:.0%} | {b[2]:.2f} | {b[3] * 100:+.2f} | {pl} |")
    A += ['', '## 6. Setiap setup (kumpulan B; semua isyarat, perbandingan berpasangan)', '',
          '| ID | Keluar terpilih-T | Tangkap penuh %: pegang sahaja / CS07 / **CS09** | 2025–26: pegang / CS09 | Nisbah simpan | Keluar terpilih-R | '
          'Purata %: pegang → R | Rugi ≥ 8 %: pegang → R | Menang %: pegang → R |',
          '|---' * 9 + '|']
    for r in T.itertuples():
        A.append(f"| `{r.id}` | {r.henti_T} · {r.keluar_T_teks} | {p(r.tp_x00T)} / {p(r.tp_aras7)} / **{p(r.tp_T)}** | "
                 f"{p(r.tp_K3_x00T)} / {p(r.tp_K3_T)} | {r.simpan_T:.2f} | {r.henti_R} · {r.keluar_R_teks} | "
                 f"{p(r.pur_x00R, 2, True)} → {p(r.pur_R, 2, True)} | {p(r.rugi8_x00R, 0)} → {p(r.rugi8_R, 0)} | "
                 f"{p(r.menang_x00R, 0)} → {p(r.menang_R, 0)} |")
    A += ['', '## 7. Kaveat', '',
          '- Kumpulan B berkongsi HARI yang sama dengan kumpulan A: bagi keluar ikut pasaran (kelas P), saham B bukan ujian bebas; '
          'hanya 2025–26 (K3) yang tidak dilihat dari segi masa, dan ia pendek.',
          '- Keluar dipilih pada A daripada ratusan ribu calon: angka A melambung, angka B dan K3 yang dibaca. Kumpulan B sudah '
          'dilihat dalam pusingan terdahulu.',
          '- Tarikh earnings = tarikh pemfailan 8-K sebenar; "earnings pada sesi berikutnya" mengandaikan tarikh diumumkan lebih awal.',
          '- Tiada saham delist. Registry F, kedudukan akhir dan kohort jejak TIDAK diubah oleh pusingan ini. Backtest sahaja; '
          'kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'KELUAR.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"lapor keluar CS09: {len(T)} setup; bacaan 1 {B['n1']}/{B['n']} -> {'MENOLONG' if B['ya1'] else 'TIDAK'}; "
             f"bacaan 2 {B['n2']}/{B['n']} -> {'MENOLONG' if B['ya2'] else 'TIDAK'}")
    return T, B


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'benihm':
        benih_m(kerja)
    elif cmd == 'atom':
        for st_ in ('A', 'B'):
            k7.siri_set(kerja, st_)
            siri_set(kerja, st_)
    elif cmd == 'cari':
        cari_(kerja)
    elif cmd == 'pilih':
        pilih(kerja)
    elif cmd == 'kunci':
        kunci(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
