"""Carian setup — pusingan CS10: keluar daripada maklumat baharu pada LORONG TREND T01-T12 (SPEC pindaan 15 Nov 2026 (s)).

Lorong CS08 (pegang hingga 126 sesi): 38 atom lama `cs_trend8` + 90 atom baharu dalam enam kelas (P pasaran, S sektor/
industri, E peristiwa syarikat, R relatif kepada pasaran, K kemuncak, L keadaan laluan/saham), diskala untuk 6 bulan.
Peraturan: X00, setiap atom tunggal dan SEMUA pasangan (ATAU, DAN). Kernel sendiri (topeng bit 125 sesi, dua kata 63 bit);
mekanik sama seperti cs_trend8.hasil_semua (pariti diuji): atom pada tutup sesi d -> jual buka sesi d + 1; henti intrahari;
pegang minimum (p); kos 0.5 %.
Guna: python3 cs_keluar10.py benihm|atom|cari|pilih|kunci|lapor <kerja>. Jangan sunting keluaran secara manual."""
import os
import pickle
import re
import sys
import time

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_keluar9 as k9  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402
import cs_trend8 as t8  # noqa: E402

H_MAX, TB, KOS, HENTI, NH, AKTIF, NG = t8.H_MAX, t8.TB, t8.KOS, t8.HENTI, t8.NH, t8.AKTIF, t8.NG
N_SEJAGAT, SIMPAN_MIN, TP_LONGGAR = 10, 0.90, 0.005     # dikunci pindaan (s)
BIT = 63                                                # bit setiap kata (int64 tanpa bit tanda)
STAT = ('n', 'tb', 'rugi15', 'menang', 'R', 'n_besar', 'R_besar')
NST = len(STAT)
KELAS = {'P': 'pasaran', 'S': 'sektor/industri', 'E': 'peristiwa syarikat', 'R': 'relatif kepada pasaran',
         'K': 'kemuncak / terlalu panas', 'L': 'keadaan laluan/saham'}
PLASEBO = ('P', 'S', 'E')
PUS = 'CS10'


def atom_baharu():
    """Senarai (kod, kelas, jenis, par, par2, par3, teks, spek). jenis 0 = siri setiap bar; 4 = tiada tutup tertinggi baharu
    k sesi; 5 = pulang f daripada untung puncak; 6 = gagal corak (sesi d, ambang x); 7 = lantai untung (a, b); 8 = tutup <
    rendah bar tutup tertinggi; 10 = Chandelier mengetat ikut masa (k0, k1, sesi); 11 = Chandelier mengetat ikut untung
    (k0, k1, a)."""
    A = []

    def add(kelas, jenis, teks, par=0.0, par2=0.0, par3=0.0, **spek):
        A.append((kelas, jenis, float(par), float(par2), float(par3), teks, spek))
    for a in k9.ATOM9:                                                  # P dan S: takrif (r) yang sama (baris cs09_XB)
        if a[1] in ('P', 'S'):
            add(a[1], 0, a[5], k9=a[0])
    add('E', 0, 'earnings pada sesi berikutnya (jual sebelum laporan)', e='esok')
    for x in (-0.10, -0.05, 0.0):
        add('E', 0, f'reaksi earnings terakhir (0-5 sesi lalu) <= {x:.0%}', e='reaksi', x=x)
    add('E', 0, 'hari reaksi earnings (0-5 sesi lalu) tutup < buka', e='merah')
    add('E', 0, '0-10 sesi selepas earnings DAN tutup < tutup sebelum earnings', e='bawah_pra')
    for x in (0.20, 0.10, 0.0):
        add('E', 0, f'hasil suku terkini tumbuh < {x:.0%}', e='hasil', x=x)
    add('E', 0, 'kejutan untung terkini negatif (SUE < 0)', e='sue')
    for k, x in ((20, 0.10), (20, 0.20), (60, 0.15), (60, 0.30)):
        add('R', 0, f'pulangan {k} sesi saham - QQQ <= -{x:.0%}', r='beza', k=k, x=x)
    for x in (70, 90):
        add('R', 0, f'RS < {x}', r='rs', x=x)
    for a in k9.ATOM9:                                                  # K: 17 atom (r) + regangan jangka panjang
        if a[1] == 'K':
            add('K', 0, a[5], k9=a[0])
    for x in (0.30, 0.50, 0.70):
        add('K', 0, f'tutup >= {x:.0%} di atas SMA50', k='sma50', x=x)
    for x in (6, 8, 10):
        add('K', 0, f'(tutup - SMA50) / ATR14 >= {x}', k='atr50', x=x)
    add('K', 0, 'tutup >= 100% di atas SMA200', k='sma200', x=1.0)
    for k in (20, 40, 60):
        add('L', 4, f'tiada tutup tertinggi baharu selama {k} sesi', k)
    for f, t in ((1 / 3, '1/3'), (1 / 2, '1/2'), (2 / 3, '2/3')):
        add('L', 5, f'pulang >= {t} daripada untung puncak', f)
    for d, x in ((20, 0.05), (40, 0.10), (60, 0.10), (60, 0.20), (90, 0.20)):
        add('L', 6, f'gagal corak (selepas {d} sesi, tutup < harga beli +{x:.0%})', d, x)
    for a, b in ((0.20, 0.05), (0.30, 0.10), (0.50, 0.20), (0.50, 0.30), (1.00, 0.50)):
        add('L', 7, f'lantai untung (selepas tutup tertinggi >= +{a:.0%}, tutup < +{b:.0%})', a, b)
    add('L', 8, 'tutup < rendah bar tutup tertinggi sejak beli')
    for k0, k1 in ((8, 4), (6, 3), (5, 3)):
        add('L', 10, f'Chandelier {k0}xATR14 hingga sesi 60, kemudian {k1}xATR14', k0, k1, 60)
    for k0, k1, a in ((8, 4, 0.50), (6, 3, 0.50), (8, 5, 0.30)):
        add('L', 11, f'Chandelier {k0}xATR14 hingga tutup tertinggi >= +{a:.0%}, kemudian {k1}xATR14', k0, k1, a)
    for k in (4, 5, 6):
        add('L', 0, f'distribution day saham >= {k} dalam 25 sesi', l='dist', n=k)
    bil, out = {}, []
    for kelas, jenis, par, par2, par3, teks, spek in A:
        bil[kelas] = bil.get(kelas, 0) + 1
        out.append((f'Z{kelas}{bil[kelas]:02d}', kelas, jenis, par, par2, par3, teks, spek))
    return out


ATOM10 = atom_baharu()
NB, NL = len(ATOM10), t8.NA                             # 90 baharu, 38 lama
NA = NL + NB                                            # indeks atom: 0..NL-1 lama (cs_trend8), NL.. baharu
N_XT = int((t8.JENIS == 0).sum())                       # baris siri atom lama (cs08_XT)
_j9 = np.asarray([a[2] for a in ATOM10], np.int64)
N_SIRI = N_XT + int((_j9 == 0).sum())                   # baris matriks siri gabungan: lama dahulu, kemudian baharu
JENIS = np.concatenate([t8.JENIS, _j9])
PAR = np.concatenate([t8.PAR, [a[3] for a in ATOM10]])
PAR2 = np.concatenate([np.zeros(NL), [a[4] for a in ATOM10]])
PAR3 = np.concatenate([np.zeros(NL), [a[5] for a in ATOM10]])
BARIS = np.concatenate([np.where(t8.JENIS == 0, t8.BARIS, 0), np.where(_j9 == 0, N_XT + np.cumsum(_j9 == 0) - 1, 0)]).astype(np.int64)
KELAS_ATOM = np.asarray(['lama'] * NL + [a[1] for a in ATOM10])
teks_atom = lambda a: t8.ATOM[a][3] if a < NL else ATOM10[a - NL][6]
kod_atom = lambda a: f'V{a + 1:02d}' if a < NL else ATOM10[a - NL][0]     # V01-V38 = atom cs_trend8 (di sana berkod T01-T38)


def peraturan10():
    """(a1, a2, op): X00; setiap atom tunggal; semua pasangan a < b dengan ATAU (2) dan DAN (3)."""
    a1, a2, op = [0], [0], [0]
    for a in range(NA):
        a1.append(a), a2.append(a), op.append(1)
    for a in range(NA):
        for b in range(a + 1, NA):
            for o in (2, 3):
                a1.append(a), a2.append(b), op.append(o)
    return np.asarray(a1, np.int64), np.asarray(a2, np.int64), np.asarray(op, np.int64)


A1, A2, OP = peraturan10()
NR = len(A1)
NKOL = NR * NG                                          # lajur = peraturan * NG + aktif
TUNGGAL = np.flatnonzero(OP == 1)                       # peraturan tunggal: indeks peraturan = 1 + atom


def nama_peraturan(kol):
    r, g = divmod(int(kol), NG)
    if OP[r] == 0:
        return 'X00 tiada keluar indikator (henti + 126 sesi)'
    t = teks_atom(A1[r]) if OP[r] == 1 else f"{teks_atom(A1[r])} {'ATAU' if OP[r] == 2 else 'DAN'} {teks_atom(A2[r])}"
    return t if g == 0 else f'{t} [aktif {AKTIF[g]}]'


def kod_peraturan(kol):
    r, g = divmod(int(kol), NG)
    if OP[r] == 0:
        return 'X00'
    t = kod_atom(A1[r]) if OP[r] == 1 else f"{kod_atom(A1[r])} {'ATAU' if OP[r] == 2 else 'DAN'} {kod_atom(A2[r])}"
    return t + ('' if g == 0 else f'@{(10, 20)[g - 1]}')


def kelas_peraturan(kol):
    r = int(kol) // NG
    if OP[r] == 0:
        return 'X00'
    ks = [KELAS_ATOM[A1[r]]] + ([KELAS_ATOM[A2[r]]] if OP[r] > 1 else [])
    return '+'.join(sorted(set(ks), key=lambda k: (k == 'lama', k)))


# ---------- siri atom jenis 0 ----------
def sma_panel(pan, n):
    """SMA n bar tutup setiap bar dalam saham masing-masing (NaN jika kurang n bar)."""
    c = pan['c']
    S = np.concatenate([[0.0], np.cumsum(c)])
    i = np.arange(len(c))
    ok = (i - n + 1) >= pan['mula'][pan['tid']]
    return np.where(ok, (S[i + 1] - S[np.maximum(i + 1 - n, 0)]) / n, np.nan)


def kira_golek(x, mula, tid, n):
    """Bilangan benar dalam n bar terakhir (termasuk bar ini) dalam saham yang sama."""
    S = np.concatenate([[0], np.cumsum(x.astype(np.int64))])
    i = np.arange(len(x))
    a = np.maximum(i + 1 - n, mula[tid])
    return S[i + 1] - S[a]


def syarikat10(pan):
    """Siri kelas E setiap bar daripada kalendar 8-K (takrif cs_keluar9.earnings_siri) dan SUE/hasil titik-masa
    (diumumkan SEBELUM hari bar, seperti cs_prasyarat.earnings)."""
    import cs_prasyarat as pr
    e = pd.read_csv(os.path.join(pr.BS2, 'data', 'sec', 'earnings_8k.csv'), usecols=['saham', 'tarikh_fail', 'masa_terima', 'items'])
    e = e[e['items'].astype(str).str.contains('2.02', regex=False)]
    e['d'] = e.tarikh_fail.str.replace('-', '').astype(int)
    e['lewat'] = pd.to_datetime(e.masa_terima, errors='coerce', utc=True).dt.hour >= 20
    su = pd.read_csv(os.path.join(pr.BS2, 'data', 'sec', 'sue.csv'), usecols=['saham', 'sue', 'tumbuh_hasil', 'tarikh_umum'])
    su = su.dropna(subset=['tarikh_umum'])
    su['d'] = su.tarikh_umum.str.replace('-', '').astype(int)
    return syarikat_siri(pan, {n: (g.d.to_numpy(), g.lewat.to_numpy()) for n, g in e.groupby('saham')},
                         {n: (g.d.to_numpy(), g.sue.to_numpy(float), g.tumbuh_hasil.to_numpy(float))
                          for n, g in su.sort_values('d').groupby('saham')})


def syarikat_siri(pan, eg, sg):
    """eg: ticker -> (tarikh pemfailan, lewat); sg: ticker -> (tarikh umum tersusun, sue, tumbuh_hasil). dict kod -> bool."""
    E = [a for a in ATOM10 if a[1] == 'E']
    N = len(pan['c'])
    out = {a[0]: np.zeros(N, bool) for a in E}
    o, c, tarikh, mula = pan['o'], pan['c'], pan['tarikh'], pan['mula']
    for t, nama in enumerate(pan['ticker']):
        a, b = mula[t], mula[t + 1]
        d, T = tarikh[a:b], b - a
        ev = np.zeros(0, np.int64)
        if nama in eg:
            dd, lewat = eg[nama]
            ev = np.where(lewat, np.searchsorted(d, dd, 'right'), np.searchsorted(d, dd, 'left'))
            ev = np.unique(ev[(ev > 0) & (ev < T)])
        if len(ev):
            i = np.arange(T)
            kn = np.searchsorted(ev, i, 'right')
            hingga = np.where(kn < len(ev), ev[np.minimum(kn, len(ev) - 1)] - i, 10 ** 6)
            ada_l = kn > 0
            lalu = ev[np.maximum(kn - 1, 0)]
            sejak = np.where(ada_l, i - lalu, 10 ** 6)
            cs, os_ = c[a:b], o[a:b]
            pra = cs[np.maximum(lalu - 1, 0)]
            reaksi = np.where(ada_l, cs[lalu] / pra - 1, np.nan)
        if nama in sg:
            ds, sue, th = sg[nama]
            k = np.searchsorted(ds, d, 'left') - 1                    # diumumkan SEBELUM hari bar
            ok, kk = k >= 0, np.maximum(k, 0)
        for kod, _, _, _, _, _, _, sp in E:
            j = sp['e']
            if j in ('hasil', 'sue'):
                if nama not in sg:
                    continue
                with np.errstate(invalid='ignore'):
                    out[kod][a:b] = ok & ((th[kk] < sp['x']) if j == 'hasil' else (sue[kk] < 0))
                continue
            if not len(ev):
                continue
            if j == 'esok':
                s = hingga == 1
            elif j == 'reaksi':
                s = (sejak <= 5) & (reaksi <= sp['x'])
            elif j == 'merah':
                s = (sejak <= 5) & (cs[lalu] < os_[lalu])
            else:
                s = (sejak <= 10) & (cs < pra)
            out[kod][a:b] = s
    return out


def qqq_pulangan(kerja, ks=(20, 60)):
    """Pulangan k sesi QQQ atas hari cs09_pasaran (kesatuan hari panel A dan B)."""
    sys.path.insert(0, cari.AKAR)
    from AUTOTUNE.teras import data as D
    hu = k9.hari_pasaran(kerja)['hu']
    ix = pd.read_parquet(D.ambil(tag='autotune-data-a02') / 'idx.parquet')
    ix['d'] = ix.date.dt.year * 10000 + ix.date.dt.month * 100 + ix.date.dt.day
    q = ix[ix.ticker == 'QQQ'].set_index('d').close.reindex(hu).ffill().reset_index(drop=True)
    return {k: (q / q.shift(k) - 1).to_numpy() for k in ks}


def siri_set(kerja, set_):
    """(X, Xp): matriks uint8 [N_SIRI, bar] = baris atom lama cs_trend8 + baris atom baharu jenis 0; Xp = kelas P, S, E
    dianjak (plasebo)."""
    f, fp = (os.path.join(kerja, f'cs10_X{x}_{set_}.npy') for x in ('', 'p'))
    if os.path.exists(f) and os.path.exists(fp):
        return np.load(f, mmap_mode='r'), np.load(fp, mmap_mode='r')
    t0 = time.time()
    pan = cari.panel(kerja, set_)
    N = len(pan['c'])
    XT = t8.siri_set(kerja, set_)
    XB9, XB9p = k9.siri_set(kerja, set_)
    b9 = {a[0]: k9.BARIS9[i] for i, a in enumerate(k9.ATOM9) if a[2] == 0}
    hi = np.searchsorted(k9.hari_pasaran(kerja)['hu'], pan['tarikh'])
    qret = qqq_pulangan(kerja)
    E = syarikat10(pan)
    Ep = {k: lapis.anjak_saham(v, pan['mula']) for k, v in E.items()}
    c, s50, s200 = pan['c'], sma_panel(pan, 50), sma_panel(pan, 200)
    dist = kira_golek(np.asarray(XB9[k9.N_SIRI]) > 0, pan['mula'], pan['tid'], 25)
    X, Xp = np.zeros((N_SIRI, N), np.uint8), np.zeros((N_SIRI, N), np.uint8)
    X[:N_XT] = Xp[:N_XT] = XT
    with np.errstate(invalid='ignore', divide='ignore'):
        for a, (kod, kelas, jenis, par, par2, par3, teks, sp) in enumerate(ATOM10):
            if jenis:
                continue
            r = BARIS[NL + a]
            if 'k9' in sp:
                x, xp = XB9[b9[sp['k9']]], XB9p[b9[sp['k9']]]
            elif 'e' in sp:
                x, xp = E[kod], Ep[kod]
            elif 'r' in sp:
                x = (k9.beza_qqq(pan, qret[sp['k']][hi], sp['k']) <= -sp['x']) if sp['r'] == 'beza' else (
                    pan['F'][15 if sp['x'] == 70 else 16] == 0)       # BUKAN F16 (RS >= 70) / BUKAN F17 (RS >= 90)
                xp = x
            elif 'l' in sp:
                x = xp = dist >= sp['n']
            elif 'k' in sp:
                x = (c / s50 - 1 >= sp['x']) if sp['k'] == 'sma50' else ((c - s50) / pan['atr'] >= sp['x']) if sp['k'] == 'atr50' \
                    else (c / s200 - 1 >= sp['x'])
                xp = x
            else:
                raise ValueError(kod)
            X[r], Xp[r] = x, xp
    np.save(f, X), np.save(fp, Xp)
    sah = t8.sah8(pan)
    cari.log(f'siri atom keluar CS10 {set_}: {X.shape}, {time.time() - t0:.0f}s; % bar sah benar (baharu): '
             + ' '.join(f'{ATOM10[a][0]}={X[BARIS[NL + a], sah].mean() * 100:.0f}' for a in range(NB) if _j9[a] == 0))
    return np.load(f, mmap_mode='r'), np.load(fp, mmap_mode='r')


# ---------- kernel 126 sesi dengan topeng bit ----------
@njit(cache=True)
def _ctz(x):
    n = 0
    while (x & 1) == 0:
        x >>= 1
        n += 1
    return n


@njit(parallel=True, cache=True)
def sedia(ev, o, l, c, atr, X, jenis, par, par2, par3, baris, pegang_min):
    """Bagi setiap isyarat: topeng atom M[isyarat, atom, 2] (bit d = benar pada tutup sesi d; kata = d // 63), topeng aktif
    ARM[isyarat, 2, 2] (+10 %, +20 %), keadaan henti (DS, PS, H0), buka setiap sesi / P (OPN), tutup sesi 126 / P (CF) dan
    label [besar, puncak]. Bit hanya dipasang bagi d >= pegang_min - 1, seperti cs_trend8.hasil_semua."""
    n, nA = ev.shape[0], jenis.shape[0]
    M = np.zeros((n, nA, 2), np.int64)
    ARM = np.zeros((n, 2, 2), np.int64)
    DS = np.full((n, NH), 999, np.int64)
    PS = np.zeros((n, NH))
    H0 = np.zeros((n, NH), np.bool_)
    OPN = np.zeros((n, H_MAX))
    CF = np.zeros(n)
    LAB = np.zeros((n, 2))
    for k in prange(n):
        i = ev[k]
        e = i + 1
        P = o[e]
        L = np.zeros(NH)
        t8._aras(P, atr[i], L)
        hc, d_hc, low_hc = c[e], 0, l[e]
        for d in range(H_MAX - 1):
            b = e + d
            if c[b] > hc:
                hc, d_hc, low_hc = c[b], d, l[b]
            if d < pegang_min - 1:
                continue
            w, bit = d // BIT, 1 << (d % BIT)
            if hc >= P * 1.10:
                ARM[k, 0, w] |= bit
            if hc >= P * 1.20:
                ARM[k, 1, w] |= bit
            for a in range(nA):
                j = jenis[a]
                if j == 0:
                    ya = X[baris[a], b] != 0
                elif j == 1:
                    ya = c[b] < hc - par[a] * atr[b]
                elif j == 2:
                    ya = c[b] < par[a] * hc
                elif j == 3:
                    ya = (d + 1 >= par[a]) and (c[b] < P)
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
                elif j == 10:
                    ya = c[b] < hc - (par[a] if d + 1 <= par3[a] else par2[a]) * atr[b]
                else:
                    ya = c[b] < hc - (par[a] if hc < P * (1.0 + par3[a]) else par2[a]) * atr[b]
                if ya:
                    M[k, a, w] |= bit
        for s in range(NH):
            H0[k, s] = c[e] <= L[s]
            for d in range(1, H_MAX):
                b = e + d
                if o[b] <= L[s]:
                    DS[k, s] = d
                    PS[k, s] = o[b] / P
                    break
                if l[b] <= L[s]:
                    DS[k, s] = d
                    PS[k, s] = L[s] / P
                    break
        mx, mati = c[e], False
        for d in range(H_MAX):
            x = c[e + d]
            if d >= 1:
                OPN[k, d] = o[e + d] / P
            if x > mx:
                mx = x
            if not mati:
                if x >= P * (1.0 + t8.NAIK):
                    LAB[k, 0] = 1.0
                if x <= P * (1.0 - t8.JATUH):
                    mati = True
        LAB[k, 1] = mx / P - 1.0
        CF[k] = c[e + H_MAX - 1] / P
    return M, ARM, DS, PS, H0, OPN, CF, LAB


@njit(cache=True)
def _x(Mk, ARMk, a1, a2, op, r, g):
    """Indeks sesi jual indikator bagi peraturan r dengan syarat aktif g (999 = tiada)."""
    if op[r] == 0:
        return 999
    for w in range(2):
        if op[r] == 1:
            m = Mk[a1[r], w]
        elif op[r] == 2:
            m = Mk[a1[r], w] | Mk[a2[r], w]
        else:
            m = Mk[a1[r], w] & Mk[a2[r], w]
        if g > 0:
            m &= ARMk[g - 1, w]
        if m != 0:
            return w * BIT + _ctz(m) + 1
    return 999


@njit(cache=True)
def _R(x, s, k, DS, PS, H0, OPN, CF):
    """(R bersih, sesi jual). Sama seperti cs_trend8.hasil_semua."""
    if H0[k, s]:
        return OPN[k, 1] - 1.0 - KOS, 1
    if x != 999 and x <= DS[k, s]:
        return OPN[k, x] - 1.0 - KOS, x
    if DS[k, s] != 999:
        return PS[k, s] - 1.0 - KOS, DS[k, s]
    return CF[k] - 1.0 - KOS, H_MAX - 1


@njit(parallel=True, cache=True)
def kumpul(M, ARM, DS, PS, H0, OPN, CF, LAB, era, n_era, a1, a2, op):
    """Acc[henti, lajur, era, statistik] atas semua isyarat; lajur = peraturan * NG + aktif."""
    n, nR = M.shape[0], a1.shape[0]
    Acc = np.zeros((NH, nR * NG, n_era, NST), np.float32)
    for r in prange(nR):
        for g in range(NG):
            loc = np.zeros((NH, n_era, NST))
            for k in range(n):
                x = _x(M[k], ARM[k], a1, a2, op, r, g)
                p = era[k]
                for s in range(NH):
                    R, _ = _R(x, s, k, DS, PS, H0, OPN, CF)
                    v = loc[s, p]
                    v[0] += 1.0
                    if R >= TB:
                        v[1] += 1.0
                    if R <= -0.15:
                        v[2] += 1.0
                    if R > 0:
                        v[3] += 1.0
                    v[4] += R
                    if LAB[k, 0] > 0:
                        v[5] += 1.0
                        v[6] += R
            for s in range(NH):
                for p in range(n_era):
                    for j in range(NST):
                        Acc[s, r * NG + g, p, j] = loc[s, p, j]
    return Acc


@njit(parallel=True, cache=True)
def hasil(M, ARM, DS, PS, H0, OPN, CF, a1, a2, op, s, kol):
    """(R, sesi jual) setiap isyarat bagi satu (henti s, lajur kol)."""
    n = M.shape[0]
    R = np.empty(n)
    sk = np.empty(n, np.int64)
    r, g = kol // NG, kol % NG
    for k in prange(n):
        R[k], sk[k] = _R(_x(M[k], ARM[k], a1, a2, op, r, g), s, k, DS, PS, H0, OPN, CF)
    return R, sk


def sedia_pan(pan, X, ev, pegang_min=None):
    return sedia(np.ascontiguousarray(ev, dtype=np.int64), pan['o'], pan['l'], pan['c'], pan['atr'], X, JENIS, PAR, PAR2, PAR3,
                 BARIS, t8.PEGANG_MIN if pegang_min is None else pegang_min)


# ---------- setup papan CS08 ----------
def papan8():
    """12 setup papan CS08 dibaca semula daripada hasil/CS08/papan.csv: nama pencetus, prasyarat, penapis dan henti CS08."""
    D = pd.read_csv(os.path.join(SINI, 'hasil', 'CS08', 'papan.csv'))
    bersih = lambda t: c5.buang_kod(t).replace(' DAN ', ' + ')
    pra = {bersih(c5.tk_pra(q1, q2)): (q1, q2) for q1 in range(-1, lapis.N1) for q2 in range(-1, lapis.N2)}
    nf = len(atom.PENAPIS)
    pen = {bersih(c5.tk_pen(f1, f2)): (f1, f2) for f1 in range(-1, nf) for f2 in range(-1, nf) if f2 == -1 or f1 < f2}
    out = []
    for r in D.itertuples():
        m = re.match(r'^(M\d+) .*\(benih M, varian ([0-9a-z]+)[:)]', r.pencetus)
        nama = f'{m.group(1)}.{m.group(2)}' if m else (r.pencetus.split()[0] + ('.0' if r.pencetus.startswith('M') else ''))
        assert str(r.keluar).startswith('X00'), r.id                  # keluar CS08 = X00 bagi kesemua 12 setup
        (q1, q2), (f1, f2) = pra[r.prasyarat], pen[r.penapis]
        out.append(dict(id=r.id, pencetus=nama, q1=q1, q2=q2, f1=f1, f2=f2, s8=HENTI.index(r.henti),
                        tb_semua_x00=float(r.tb_semua_x00), n8=int(r.n)))
    return out


def benih_m(kerja):
    tugas = k9.tugas_m([b['pencetus'] for b in papan8()])
    cari.log(f"CS10 benih M: {len(tugas)} varian ({', '.join(t[0] for t in tugas)})")
    for s in ('A', 'B'):
        cari.benih(kerja, s, tugas=tugas, fail=t7.FAIL_M.format(s))


def senarai_setup(kerja, set_):
    """(pan, senarai dict papan8 + ev): ev = SEMUA isyarat masuk setup pada set itu dengan tetingkap 126 sesi lengkap."""
    pan = cari.panel(kerja, set_)
    L = lapis.muat(kerja, set_)
    Lr, S8 = (L['L1'], L['L2']), t8.sah8(pan)
    out = []
    for b in papan8():
        ev = t7.ev_satu(kerja, set_, b['pencetus'])
        ev = ev[S8[ev]]
        out.append(dict(b, ev=ev[c5.topeng(pan, Lr, ev, b['q1'], b['q2'], b['f1'], b['f2'])]))
    return pan, out


_A1S = np.concatenate([[0], A1[TUNGGAL]])                # plasebo: X00 + atom tunggal sahaja
_A2S, _OPS = _A1S.copy(), np.concatenate([[0], np.ones(NA, np.int64)])


def cari_(kerja):
    """Peringkat cari (kumpulan A, semua isyarat): Acc setiap setup -> kerja/cs10_keluar/<id>_A.npy (+ plasebo _Ap.npy)."""
    d = os.path.join(kerja, 'cs10_keluar')
    os.makedirs(d, exist_ok=True)
    pan, S = senarai_setup(kerja, 'A')
    X, Xp = siri_set(kerja, 'A')
    t0 = time.time()
    for k, s in enumerate(S, 1):
        f = os.path.join(d, f"{s['id']}_A.npy")
        if os.path.exists(f):
            continue
        ev = s['ev']
        era = pan['tempoh'][ev].astype(np.int64)
        np.save(os.path.join(d, f"{s['id']}_Ap.npy"), kumpul(*sedia_pan(pan, Xp, ev), era, 2, _A1S, _A2S, _OPS))
        np.save(f + '.tmp.npy', kumpul(*sedia_pan(pan, X, ev), era, 2, A1, A2, OP))
        os.replace(f + '.tmp.npy', f)
        cari.log(f"  keluar A {k}/{len(S)} {s['id']}: {len(ev):,} isyarat · {time.time() - t0:.0f}s")


def _kadar(Acc):
    """tb, purata [s, kol, era]; beza min-era lawan X00 henti sama (dtb, dR); R pada `besar` (rb); rugi15 [s, kol]."""
    n = np.maximum(Acc[..., 0], 1).astype(np.float64)
    tb, pur = Acc[..., 1] / n, Acc[..., 4] / n
    return (tb, pur, (tb - tb[:, :1]).min(-1), (pur - pur[:, :1]).min(-1), Acc[..., 6].astype(np.float64).sum(-1),
            Acc[..., 2].sum(-1) / n.sum(-1))


def _sejagat(D, DR, RT, kol_sah, k=N_SEJAGAT):
    simpan = RT / np.where(RT[:, :1] > 0, RT[:, :1], np.nan)
    lulus = (simpan >= SIMPAN_MIN) & kol_sah[None, :]
    nk = D.shape[1]
    ambil = lambda skor: [(int(f // nk), int(f % nk)) for f in np.argsort(-skor, axis=None, kind='stable')[:k]
                          if np.isfinite(skor.flat[f])]
    return ambil(np.where(lulus, D, -np.inf)), ambil(np.where(lulus & (D >= 0), DR, -np.inf)), simpan, lulus


def pilih(kerja):
    """Peringkat pilih (kumpulan A sahaja): senarai sejagat T dan R, pilihan setiap setup, atom tunggal terbaik setiap kelas
    (sebenar dan plasebo). -> cs10_pilih.pkl"""
    d = os.path.join(kerja, 'cs10_keluar')
    ids = sorted(f[:-6] for f in os.listdir(d) if f.endswith('_A.npy'))
    D, DR, RT = np.zeros((NH, NKOL)), np.zeros((NH, NKOL)), np.zeros((NH, NKOL))
    nkp = (NA + 1) * NG
    Dp, DRp, RTp = np.zeros((NH, nkp)), np.zeros((NH, nkp)), np.zeros((NH, nkp))
    for i in ids:
        _, _, dtb, dr, rb, _ = _kadar(np.load(os.path.join(d, f'{i}_A.npy')))
        D += dtb
        DR += dr
        RT += rb
        _, _, dtb, dr, rb, _ = _kadar(np.load(os.path.join(d, f'{i}_Ap.npy')))
        Dp += dtb
        DRp += dr
        RTp += rb
    D, DR, Dp, DRp = D / len(ids), DR / len(ids), Dp / len(ids), DRp / len(ids)
    bukan_x00 = np.arange(NKOL) >= NG
    sejT, sejR, simpan_s, lulus = _sejagat(D, DR, RT, bukan_x00)
    kelas, kelas_p = {}, {}
    for kl in list(KELAS) + ['lama']:
        ra = np.asarray([r for r in TUNGGAL if KELAS_ATOM[A1[r]] == kl])
        m = np.zeros(NKOL, bool)
        m[(ra[:, None] * NG + np.arange(NG)[None, :]).ravel()] = True
        t, r_, _, _ = _sejagat(D, DR, RT, m, 1)
        kelas[kl] = {'T': t[0] if t else None, 'R': r_[0] if r_ else None}
        if kl in PLASEBO:
            mp_ = np.zeros(nkp, bool)
            mp_[(ra[:, None] * NG + np.arange(NG)[None, :]).ravel()] = True      # ruang tunggal: peraturan = 1 + atom (sama)
            t, r_, _, _ = _sejagat(Dp, DRp, RTp, mp_, 1)
            kelas_p[kl] = {'T': t[0] if t else None, 'R': r_[0] if r_ else None,
                           'D_T': float(Dp[t[0]]) if t else np.nan, 'D_R': float(DRp[r_[0]]) if r_ else np.nan}
    P = {}
    for i in ids:
        tb, pur, dtb, dr, rb, rugi = _kadar(np.load(os.path.join(d, f'{i}_A.npy')))
        simpan = rb / np.where(rb[:, :1] > 0, rb[:, :1], np.nan)
        tbm, purm = tb.min(-1), pur.min(-1)
        bT = kT = None
        for s, kol in [(s, 0) for s in range(NH)] + sejT:
            if kol and not (simpan[s, kol] >= SIMPAN_MIN):
                continue
            k_ = (float(tbm[s, kol]), -float(rugi[s, kol]))
            if kT is None or k_ > kT:
                bT, kT = (s, kol), k_
        bR = kR = None
        for s, kol in [(s, 0) for s in range(NH)] + sejR:
            if kol and not ((simpan[s, kol] >= SIMPAN_MIN) and (tbm[s, kol] >= tbm[s, 0])):
                continue
            if kR is None or float(purm[s, kol]) > kR:
                bR, kR = (s, kol), float(purm[s, kol])
        P[i] = {'T': bT, 'R': bR, 'tb_A': kT[0], 'tb_X00_A': float(tbm[bT[0], 0]), 'pur_A': kR, 'pur_X00_A': float(purm[bR[0], 0])}
    g = lambda M_, L_: [float(M_[x]) for x in L_]
    out = {'ids': ids, 'sejT': sejT, 'sejR': sejR, 'D_T': g(D, sejT), 'simpan_T': g(simpan_s, sejT), 'D_R': g(DR, sejR),
           'Dtb_R': g(D, sejR), 'simpan_R': g(simpan_s, sejR), 'n_lulus': int(lulus.sum()), 'setup': P, 'kelas': kelas,
           'kelas_p': kelas_p, 'kelas_D': {kl: {j: (float((D if j == 'T' else DR)[v[j]]) if v[j] else np.nan) for j in 'TR'}
                                           for kl, v in kelas.items()},
           'D_tanpa_syarat': float(np.max(np.where(bukan_x00[None, :], D, -np.inf)))}
    pickle.dump(out, open(os.path.join(kerja, 'cs10_pilih.pkl'), 'wb'), protocol=4)
    cari.log(f"pilih keluar CS10: {len(ids)} setup; {out['n_lulus']:,} daripada {NH * (NKOL - NG):,} calon lulus syarat simpan")
    for nama, L_, Dl in (('T', sejT, out['D_T']), ('R', sejR, out['D_R'])):
        if L_:
            cari.log(f"  {nama}#1 {HENTI[L_[0][0]]} · {nama_peraturan(L_[0][1])} ({Dl[0] * 100:+.2f} mata)")
    return out


def ukur(pan, ev, R, sk, LAB):
    """Statistik satu keluar: semua isyarat (semua tempoh), K3 sahaja, dan satu posisi setiap saham."""
    def st(q):
        r, bs = R[q], LAB[q, 0] > 0
        if not q.any():
            return dict(n=0, tb=np.nan, rugi15=np.nan, menang=np.nan, purata=np.nan, median=np.nan, pegang=np.nan,
                        n_besar=0, R_besar=np.nan, jumlah_tb=0.0, jumlah_R=0.0)
        return dict(n=int(q.sum()), tb=float((r >= TB).mean()), rugi15=float((r <= -0.15).mean()), menang=float((r > 0).mean()),
                    purata=float(r.mean()), median=float(np.median(r)), pegang=float(np.median(sk[q]) + 1),
                    n_besar=int(bs.sum()), R_besar=float(r[bs].mean()) if bs.any() else np.nan,
                    jumlah_tb=float((r >= TB).sum()), jumlah_R=float(r.sum()))
    semua = np.ones(len(ev), bool)
    return {'semua': st(semua), 'K3': st(pan['tempoh'][ev] == 2), 'satu': st(teras.satu_posisi(ev, sk, pan['tid']))}


def kunci(kerja):
    """Peringkat semak pada kumpulan B. -> cs10_kunci.pkl"""
    S0 = pickle.load(open(os.path.join(kerja, 'cs10_pilih.pkl'), 'rb'))
    pan, S = senarai_setup(kerja, 'B')
    X, Xp = siri_set(kerja, 'B')
    out, t0 = {}, time.time()
    for s_ in S:
        i, ev = s_['id'], s_['ev']
        st = sedia_pan(pan, X, ev)
        LAB = st[7]
        u = lambda s, kol: ukur(pan, ev, *hasil(*st[:7], A1, A2, OP, s, kol), LAB)
        p = S0['setup'][i]
        r = {'n': len(ev), 's8': s_['s8'], 'tb_semua_x00_cs08': s_['tb_semua_x00'], 'n8': s_['n8'],
             'x00': {s: u(s, 0) for s in range(NH)}, 'T': u(*p['T']), 'R': u(*p['R']),
             'sejT': [u(a, b) for a, b in S0['sejT']], 'sejR': [u(a, b) for a, b in S0['sejR']],
             'kelas': {kl: {j: (u(*v[j]) if v[j] else None) for j in 'TR'} for kl, v in S0['kelas'].items()}}
        sp = sedia_pan(pan, Xp, ev)
        up = lambda s, kol: ukur(pan, ev, *hasil(*sp[:7], _A1S, _A2S, _OPS, s, kol), LAB)
        r['kelas_p'] = {kl: {j: (up(*v[j]) if v[j] else None) for j in 'TR'} for kl, v in S0['kelas_p'].items()}
        out[i] = r
    pickle.dump(out, open(os.path.join(kerja, 'cs10_kunci.pkl'), 'wb'), protocol=4)
    cari.log(f'kunci keluar CS10: {len(out)} setup · {time.time() - t0:.0f}s')
    return out


# ---------- laporan ----------
def jadual(S0, K):
    """Satu baris setiap setup (kumpulan B, semua isyarat; perbandingan berpasangan)."""
    baris = []
    for i, r in K.items():
        p = S0['setup'][i]
        (sT, kT), (sR, kR) = p['T'], p['R']
        t, x, x8, rr, xr = r['T'], r['x00'][sT], r['x00'][r['s8']], r['R'], r['x00'][sR]
        g, k3 = (lambda m, k: m['semua'][k]), (lambda m, k: m['K3'][k])
        nis = lambda m, m0: (g(m, 'R_besar') * g(m, 'n_besar')) / (g(m0, 'R_besar') * g(m0, 'n_besar')) \
            if g(m0, 'n_besar') and g(m0, 'R_besar') > 0 else np.nan
        baris.append(dict(
            id=i, n=r['n'], n_K3=k3(t, 'n'), henti_cs08=HENTI[r['s8']],
            henti_T=HENTI[sT], keluar_T=kod_peraturan(kT), keluar_T_teks=nama_peraturan(kT), kelas_T=kelas_peraturan(kT),
            tb_T=g(t, 'tb'), tb_x00T=g(x, 'tb'), tb_cs08=g(x8, 'tb'), simpan_T=nis(t, x),
            rugi15_T=g(t, 'rugi15'), rugi15_x00T=g(x, 'rugi15'), rugi15_cs08=g(x8, 'rugi15'),
            menang_T=g(t, 'menang'), menang_x00T=g(x, 'menang'), pur_T=g(t, 'purata'), pur_x00T=g(x, 'purata'),
            median_T=g(t, 'median'), median_x00T=g(x, 'median'), pegang_T=g(t, 'pegang'), pegang_x00T=g(x, 'pegang'),
            Rbesar_T=g(t, 'R_besar'), Rbesar_x00T=g(x, 'R_besar'),
            K3_tb_T=k3(t, 'jumlah_tb'), K3_tb_x00T=k3(x, 'jumlah_tb'),
            henti_R=HENTI[sR], keluar_R=kod_peraturan(kR), keluar_R_teks=nama_peraturan(kR), kelas_R=kelas_peraturan(kR),
            pur_R=g(rr, 'purata'), pur_x00R=g(xr, 'purata'), rugi15_R=g(rr, 'rugi15'), rugi15_x00R=g(xr, 'rugi15'),
            tb_R=g(rr, 'tb'), tb_x00R=g(xr, 'tb'), simpan_R=nis(rr, xr), menang_R=g(rr, 'menang'), menang_x00R=g(xr, 'menang'),
            median_R=g(rr, 'median'), median_x00R=g(xr, 'median'), pegang_R=g(rr, 'pegang'),
            K3_R_R=k3(rr, 'jumlah_R'), K3_R_x00R=k3(xr, 'jumlah_R'),
            satu_n=t['satu']['n'], satu_tb_T=t['satu']['tb'], satu_pur_R=rr['satu']['purata'], satu_rugi15_R=rr['satu']['rugi15'],
            tb_A=p['tb_A'], tb_X00_A=p['tb_X00_A'], pur_A=p['pur_A'], pur_X00_A=p['pur_X00_A'],
            pariti_tb_x00_cs08=r['tb_semua_x00_cs08'], pariti_n_cs08=r['n8'], pariti_n=r['x00'][r['s8']]['satu']['n']))
    return pd.DataFrame(baris)


def bacaan(T):
    """Dua bacaan dikunci pindaan (s) daripada jadual setiap setup (kumpulan B). K3 digabung merentas setup."""
    med = lambda s: float(s.median()) if len(s) else np.nan
    nk3 = float(T.n_K3.sum())
    b1 = (T.tb_T > T.tb_x00T) & (T.tb_T > T.tb_cs08)
    b2 = (T.pur_R > T.pur_x00R) & (T.rugi15_R < T.rugi15_x00R) & (T.tb_R >= T.tb_x00R - TP_LONGGAR)
    o = {'n': len(T), 'n1': int(b1.sum()), 'atas_x00': int((T.tb_T > T.tb_x00T).sum()), 'atas_cs08': int((T.tb_T > T.tb_cs08).sum()),
         'simpan_T': med(T.simpan_T), 'd_rugi_T': med(T.rugi15_T - T.rugi15_cs08), 'n_k3': int(nk3),
         'k3_T': float((T.K3_tb_T.sum() - T.K3_tb_x00T.sum()) / nk3) if nk3 else np.nan,
         'n2': int(b2.sum()), 'simpan_R': med(T.simpan_R),
         'k3_R': float((T.K3_R_R.sum() - T.K3_R_x00R.sum()) / nk3) if nk3 else np.nan}
    o['ya1'] = bool(o['n1'] > o['n'] / 2 and o['simpan_T'] >= SIMPAN_MIN and o['d_rugi_T'] <= 0.01 and o['k3_T'] > 0)
    o['ya2'] = bool(o['n2'] > o['n'] / 2 and o['simpan_R'] >= SIMPAN_MIN and o['k3_R'] > 0)
    return o


def _beza(m, j):
    """m: senarai (ukur keluar, ukur X00 henti sama). (purata beza, % setup lebih baik, nisbah simpan jumlah, beza K3
    digabung, purata beza rugi15)."""
    m = [(a, b) for a, b in m if a is not None]
    if not m:
        return (np.nan,) * 5
    dl = np.asarray([a['semua'][j] - b['semua'][j] for a, b in m])
    rt = sum(a['semua']['R_besar'] * a['semua']['n_besar'] for a, _ in m if a['semua']['n_besar'])
    rx = sum(b['semua']['R_besar'] * b['semua']['n_besar'] for _, b in m if b['semua']['n_besar'])
    kj = 'jumlah_tb' if j == 'tb' else 'jumlah_R'
    nk = sum(a['K3']['n'] for a, _ in m)
    k3 = (sum(a['K3'][kj] for a, _ in m) - sum(b['K3'][kj] for _, b in m)) / nk if nk else np.nan
    dr = np.asarray([a['semua']['rugi15'] - b['semua']['rugi15'] for a, b in m])
    return float(dl.mean()), float((dl > 0).mean()), rt / rx if rx else np.nan, float(k3), float(dr.mean())


def lapor_(kerja):
    """hasil/CS10/KELUAR.md, keluar.csv (setiap setup) dan sejagat.csv daripada cs10_pilih.pkl + cs10_kunci.pkl."""
    import cs_lapor as lapor
    S0 = pickle.load(open(os.path.join(kerja, 'cs10_pilih.pkl'), 'rb'))
    K = pickle.load(open(os.path.join(kerja, 'cs10_kunci.pkl'), 'rb'))
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
    sT = [_beza([(r['sejT'][q], r['x00'][s]) for r in K.values()], 'tb') for q, (s, _) in enumerate(S0['sejT'])]
    sR = [_beza([(r['sejR'][q], r['x00'][s]) for r in K.values()], 'purata') for q, (s, _) in enumerate(S0['sejR'])]
    rek = [dict(senarai=nm, kedudukan=j, henti=HENTI[s], keluar=kod_peraturan(kol), keluar_teks=nama_peraturan(kol),
                kelas=kelas_peraturan(kol), A_tambah=dA, A_simpan=sA, B_tambah=b[0], B_setup_lebih_baik=b[1], B_simpan=b[2],
                K3_tambah=b[3], B_beza_rugi15=b[4])
           for nm, L_, DA, SA, BB in (('T', S0['sejT'], S0['D_T'], S0['simpan_T'], sT), ('R', S0['sejR'], S0['D_R'], S0['simpan_R'], sR))
           for j, ((s, kol), dA, sA, b) in enumerate(zip(L_, DA, SA, BB), 1)]
    pd.DataFrame(rek, columns=['senarai', 'kedudukan', 'henti', 'keluar', 'keluar_teks', 'kelas', 'A_tambah', 'A_simpan', 'B_tambah',
                               'B_setup_lebih_baik', 'B_simpan', 'K3_tambah', 'B_beza_rugi15']
                 ).to_csv(os.path.join(d_, 'sejagat.csv'), index=False, float_format='%.5f')
    kom = lambda L_: ', '.join(f'{k} {v}' for k, v in pd.Series([kelas_peraturan(kol) for _, kol in L_]).value_counts().items()) \
        if L_ else 'tiada calon lulus'
    A = ['# CS10: keluar daripada maklumat baharu pada LORONG TREND `T01`–`T12` (pegang hingga 6 bulan; backtest; BUKAN bukti)',
         '', status, '',
         'Dijana `kajian/carian_setup/cs_keluar10.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (s), dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.**', '',
         '## 1. Apa yang dicari', '',
         f'- CS08 menguji {NL} indikator "trend tamat" TUNGGAL daripada harga saham sendiri (tiada yang menolong). Pusingan ini '
         f'menambah **{NB} atom baharu**: ' + '; '.join(f'{k} = {v} ({int((KELAS_ATOM == k).sum())})' for k, v in KELAS.items())
         + ', dan menguji SEMUA pasangan (ATAU, DAN).',
         f'- {NR:,} peraturan × 3 syarat aktif × {NH} henti = **{NH * NKOL:,} cara keluar setiap setup**, bagi {len(S0["ids"])} setup '
         'papan CS08, dipilih pada kumpulan A sahaja.',
         '- Ukuran: **dijual dengan untung ≥ +30 %** (sama seperti CS08). Syarat "tidak jual awal": untung terealisasi pada pelari '
         f'besar (naik ≥ +50 % sebelum jatuh −15 %) mesti ≥ {SIMPAN_MIN:.0%} daripada "pegang sahaja 126 sesi". '
         f'{S0["n_lulus"]:,} cara lulus syarat itu pada A.',
         '- Pegang minimum 3 sesi terpakai; henti rugi kekal aktif.', '',
         '## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)', '',
         '**Bacaan 1 — keluar lorong trend ("pegang sampai trend tamat"):**', '',
         f"- Keluar terpilih mengatasi `X00` (pegang sahaja, henti sama): **{B['atas_x00']} daripada {B['n']}** setup; mengatasi "
         f"keluar CS08: **{B['atas_cs08']} daripada {B['n']}**; kedua-duanya: **{B['n1']} daripada {B['n']}** (perlu lebih separuh).",
         f"- Nisbah simpan (median): {B['simpan_T']:.2f} (perlu ≥ {SIMPAN_MIN:.2f}). Rugi ≥ 15 %: median beza lawan keluar CS08 "
         f"{B['d_rugi_T'] * 100:+.1f} mata (perlu ≤ +1.0).",
         f"- 2025–26 (K3, digabung merentas setup; {B['n_k3']} isyarat): tambahan dijual ≥ +30 % lawan pegang sahaja "
         f"{B['k3_T'] * 100:+.2f} mata (perlu > 0).",
         f"- Median dijual ≥ +30 %: pegang sahaja {p(T.tb_x00T.median())} % → keluar terpilih **{p(T.tb_T.median())} %**; rugi ≥ 15 % "
         f"{p(T.rugi15_x00T.median())} % → {p(T.rugi15_T.median())} %; untung pada pelari besar {p(T.Rbesar_x00T.median(), 0, True)} % → "
         f"{p(T.Rbesar_T.median(), 0, True)} %.",
         f"- **Keputusan bacaan 1: keluar baharu {'MENOLONG' if B['ya1'] else 'TIDAK menolong'}.**", '',
         '**Bacaan 2 — sisi rugi (adakah keluar baharu mengurangkan rugi tanpa menjual pelari besar):**', '',
         f"- Purata dagangan lebih tinggi DAN rugi ≥ 15 % lebih rendah daripada pegang sahaja (henti sama), tanpa mengurangkan "
         f"\"dijual ≥ +30 %\" lebih 0.5 mata: **{B['n2']} daripada {B['n']}** setup (perlu lebih separuh).",
         f"- Nisbah simpan (median): {B['simpan_R']:.2f}. 2025–26 (digabung): tambahan purata dagangan {B['k3_R'] * 100:+.2f} mata "
         "(perlu > 0).",
         f"- Median merentas setup: purata dagangan pegang sahaja {p(T.pur_x00R.median(), 2, True)} % → terpilih "
         f"**{p(T.pur_R.median(), 2, True)} %**; rugi ≥ 15 % {p(T.rugi15_x00R.median())} % → **{p(T.rugi15_R.median())} %**; menang "
         f"{p(T.menang_x00R.median(), 0)} % → {p(T.menang_R.median(), 0)} %; median dagangan {p(T.median_x00R.median(), 1, True)} % → "
         f"{p(T.median_R.median(), 1, True)} %.",
         f"- **Keputusan bacaan 2: potong rugi {'MENOLONG' if B['ya2'] else 'TIDAK menolong'}.**", '',
         '## 3. Keluar sejagat ikut "dijual ≥ +30 %" (senarai T; dipilih pada A, disemak pada B)', '',
         f'Komposisi kelas: {kom(S0["sejT"])}.', '',
         '| # | Henti | Peraturan keluar | Kelas | A: tambahan (mata) | A: nisbah simpan | B: tambahan (mata) | B: % setup lebih baik | B: nisbah simpan | B: beza rugi ≥ 15 % | 2025–26: tambahan |',
         '|---' * 11 + '|']
    for j, ((s, kol), dA, sA, b) in enumerate(zip(S0['sejT'], S0['D_T'], S0['simpan_T'], sT), 1):
        A.append(f'| {j} | {HENTI[s]} | {nama_peraturan(kol)} | {kelas_peraturan(kol)} | {dA * 100:+.2f} | {sA:.2f} | {b[0] * 100:+.2f} | '
                 f'{b[1]:.0%} | {b[2]:.2f} | {b[4] * 100:+.1f} | {b[3] * 100:+.2f} |')
    A += ['', '## 4. Keluar sejagat ikut sisi rugi (senarai R)', '', f'Komposisi kelas: {kom(S0["sejR"])}.', '',
          '| # | Henti | Peraturan keluar | Kelas | A: tambahan purata dagangan (mata) | A: tambahan dijual ≥ +30 % | A: nisbah simpan | B: tambahan purata | B: % setup lebih baik | B: beza rugi ≥ 15 % | B: nisbah simpan | 2025–26: tambahan purata |',
          '|---' * 12 + '|']
    for j, ((s, kol), dA, tA, sA, b) in enumerate(zip(S0['sejR'], S0['D_R'], S0['Dtb_R'], S0['simpan_R'], sR), 1):
        A.append(f'| {j} | {HENTI[s]} | {nama_peraturan(kol)} | {kelas_peraturan(kol)} | {dA * 100:+.2f} | {tA * 100:+.2f} | {sA:.2f} | '
                 f'{b[0] * 100:+.2f} | {b[1]:.0%} | {b[4] * 100:+.1f} | {b[2]:.2f} | {b[3] * 100:+.2f} |')
    A += ['', '## 5. Setiap kelas maklumat: atom tunggal terbaik (dipilih pada A; maklumat, bukan bacaan)', '',
          'Plasebo = siri yang sama dianjak 437 sesi (kelas P, S, E sahaja): jika plasebo sama baik, kelas itu tidak membawa maklumat.', '',
          '| Kelas | Ikut | Atom tunggal terbaik (henti) | A (mata) | B (mata) | B: % setup lebih baik | B: nisbah simpan | B: beza rugi ≥ 15 % | 2025–26 | Plasebo: A / B |',
          '|---' * 10 + '|']
    for kl, nama in list(KELAS.items()) + [('lama', 'atom CS08 (harga saham sendiri)')]:
        for j, uk, label in (('T', 'tb', 'dijual ≥ +30 %'), ('R', 'purata', 'purata dagangan')):
            v = S0['kelas'][kl][j]
            if v is None:
                A.append(f'| {kl} {nama} | {label} | tiada yang lulus syarat | – | – | – | – | – | – | – |')
                continue
            b = _beza([(r['kelas'][kl][j], r['x00'][v[0]]) for r in K.values()], uk)
            pl = '–'
            if kl in S0['kelas_p'] and S0['kelas_p'][kl][j] is not None:
                vp = S0['kelas_p'][kl][j]
                bp = _beza([(r['kelas_p'][kl][j], r['x00'][vp[0]]) for r in K.values()], uk)
                pl = f"{S0['kelas_p'][kl]['D_' + j] * 100:+.2f} / {bp[0] * 100:+.2f}"
            A.append(f"| {kl} {nama} | {label} | {nama_peraturan(v[1])} ({HENTI[v[0]]}) | {S0['kelas_D'][kl][j] * 100:+.2f} | "
                     f"{b[0] * 100:+.2f} | {b[1]:.0%} | {b[2]:.2f} | {b[4] * 100:+.1f} | {b[3] * 100:+.2f} | {pl} |")
    A += ['', '## 6. Setiap setup (kumpulan B; semua isyarat, perbandingan berpasangan)', '',
          '| ID | Isyarat | Keluar terpilih-T | Dijual ≥ +30 %: pegang sahaja → **T** | Untung pada pelari besar: pegang → T | Nisbah simpan | '
          'Keluar terpilih-R | Purata %: pegang → R | Median %: pegang → R | Rugi ≥ 15 %: pegang → R | Menang %: pegang → R |',
          '|---' * 11 + '|']
    for r in T.itertuples():
        A.append(f"| `{r.id}` | {r.n} | {r.henti_T} · {r.keluar_T_teks} | {p(r.tb_x00T)} → **{p(r.tb_T)}** | "
                 f"{p(r.Rbesar_x00T, 0, True)} → {p(r.Rbesar_T, 0, True)} | {r.simpan_T:.2f} | {r.henti_R} · {r.keluar_R_teks} | "
                 f"{p(r.pur_x00R, 1, True)} → {p(r.pur_R, 1, True)} | {p(r.median_x00R, 1, True)} → {p(r.median_R, 1, True)} | "
                 f"{p(r.rugi15_x00R, 0)} → {p(r.rugi15_R, 0)} | {p(r.menang_x00R, 0)} → {p(r.menang_R, 0)} |")
    par = float((T.pariti_tb_x00_cs08 - T.tb_cs08).abs().max())
    A += ['', '## 7. Kaveat', '',
          f'- Pariti dengan CS08: "dijual ≥ +30 %" `X00` setiap setup berbeza paling banyak {par * 100:.3f} mata daripada '
          f'`hasil/CS08/papan.csv`; bilangan belian satu posisi sama bagi {int((T.pariti_n == T.pariti_n_cs08).sum())} daripada {len(T)} setup.',
          '- Hanya 12 setup dan beberapa berkongsi pencetus/prasyarat: bukan 12 ujian bebas.',
          '- Kumpulan B berkongsi HARI yang sama dengan kumpulan A: bagi keluar ikut pasaran (kelas P) saham B bukan ujian bebas; '
          '2025–26 pendek (tetingkap 126 sesi berakhir ~April 2026).',
          '- Ratusan ribu calon atas beberapa ratus isyarat setiap setup: angka A melambung, angka B yang dibaca.',
          '- Tiada saham delist — bias LEBIH besar bagi pegangan 6 bulan. Papan `T01`–`T12` tidak diubah. Backtest sahaja; kad skor '
          'kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'KELUAR.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"lapor keluar CS10: {len(T)} setup; bacaan 1 {B['n1']}/{B['n']} -> {'MENOLONG' if B['ya1'] else 'TIDAK'}; "
             f"bacaan 2 {B['n2']}/{B['n']} -> {'MENOLONG' if B['ya2'] else 'TIDAK'}; pariti tb X00 maks {par:.6f}")
    return T, B


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'benihm':
        benih_m(kerja)
    elif cmd == 'atom':
        for st_ in ('A', 'B'):
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
