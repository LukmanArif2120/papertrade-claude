# cs_pegang14.py — pusingan CS14 (SPEC_CARIAN_SETUP.md pindaan 16 Nov 2026 (x); permintaan pengguna: "pegang selagi untung,
# kalau rugi jual; tak boleh limit"). Cara pegang "jual yang rugi, pegang yang untung" TANPA had masa bagi 2,001 setup senarai
# utama: 4 komponen rugi x 9 komponen trend tamat x 3 had masa = 108 cara + rujukan "jual hari ke-20". 20 sesi pertama tidak
# diubah (stop loss 4xATR14 sahaja). Pemilihan pada kumpulan A, bacaan dikunci pada kumpulan B. Laporan dan cadangan sahaja:
# senarai utama, registry dan kohort TIDAK diubah.
#   python3 cs_pegang14.py kira <kerja>    -> <kerja>/cs14_stat.pkl (atom setiap isyarat sekali, statistik setiap setup x cara)
#   python3 cs_pegang14.py kawalan <kerja> -> tambah kawalan rawak (tambahan post hoc) ke cs14_stat.pkl
#   python3 cs_pegang14.py lapor <kerja>   -> hasil/CS14/PEGANG.md, cara.csv, tangga.csv, setup.csv.gz, bacaan.json
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402
import cs_cari12 as c12  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_keluar10 as k10  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

PUS = 'CS14'
T20, KOS = 20, teras.KOS
S_HENTI = k7.HENTI.index('4xATR14')
SMA_N = (20, 50, 100, 200)
CH_K = np.array([4.0, 6.0, 8.0])
JATUH = 0.75
BESAR = 1 << 30
RUGI = {'r0': 'tiada', 'r1': 'tutup di bawah harga beli', 'r2': 'tutup di bawah harga beli − 1×ATR',
        'r3': 'rugi pada hari ke-20 (semak sekali)'}
TREND = {'t0': 'tiada', 't1': 'tutup di bawah purata 20 hari', 't2': 'tutup di bawah purata 50 hari',
         't3': 'tutup di bawah purata 100 hari', 't4': 'tutup di bawah purata 200 hari', 't5': 'jatuh 4×ATR dari tutup tertinggi',
         't6': 'jatuh 6×ATR dari tutup tertinggi', 't7': 'jatuh 8×ATR dari tutup tertinggi', 't8': 'jatuh 25 % dari tutup tertinggi'}
HAD = (126, 252, 0)                                      # 0 = tiada had masa
NR, NT = len(RUGI), len(TREND)
NK = 1 + (NR - 1) + (NT - 1)                             # komponen atom: 0 stop loss; 1-3 r1-r3; 4-11 t1-t8
CARA = ['J20'] + [f'r{r}.t{t}.{h}' for h in HAD for r in range(NR) for t in range(NT)]
RW = np.array([0] + [r for h in HAD for r in range(NR) for t in range(NT)], np.int64)
TW = np.array([0] + [t for h in HAD for r in range(NR) for t in range(NT)], np.int64)
HW = np.array([-1] + [h for h in HAD for r in range(NR) for t in range(NT)], np.int64)
W = len(CARA)
SEKARANG, P126, SIMPAN = CARA.index('r0.t1.126'), CARA.index('r0.t0.126'), CARA.index('r0.t0.0')
CALON = [w for w in range(W) if HW[w] == 0 and w != SIMPAN]
KELAS_A = [w for w in CALON if TW[w] == 0]
KELAS_B = [w for w in CALON if TW[w] > 0]
STAT = ('n', 'purata', 'menang', 'rugi15', 'k10', 'k50', 'sesi_med', 'sesi_purata', 'terbuka', 'per20',
        'n_K1', 'n_K2', 'n_K3', 'purata_K1', 'purata_K2', 'purata_K3', 'menang_K1', 'menang_K2', 'menang_K3')
NS = len(STAT)
IX = {k: i for i, k in enumerate(STAT)}
MIN_DAG, MIN_K3, D_MENANG, D_RUGI = 30, 20, -0.02, 0.02  # dikunci pindaan (x); dua ambang akhir sama seperti CS11
N_KAWALAN, BENIH_KAWALAN, SAMA = 300_000, 20261116, 0.001  # tambahan post hoc (x): kawalan rawak; beza < 0.1 mata = "sama"
TANGGA = ['r0.t1.126', 'r0.t2.0', 'r0.t5.0', 'r0.t4.0', 'r0.t7.0', 'r1.t0.0']
F_ = lambda kerja: os.path.join(kerja, 'cs14_stat.pkl')
HASIL = os.path.join(SINI, 'hasil', PUS)
CS13 = os.path.join(SINI, 'hasil', 'CS13')


def teks(w):
    """Ayat biasa bagi satu cara."""
    if HW[w] == -1:
        return 'jual pada hari ke-20'
    r, t, h = f'r{RW[w]}', f't{TW[w]}', HW[w]
    if w == SEKARANG:
        return 'cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan)'
    bhg = [x for x in (RUGI[r] if RW[w] else '', TREND[t] if TW[w] else '') if x]
    asas = 'jual bila ' + ' ATAU '.join(bhg) if bhg else 'stop loss sahaja'
    return asas + (' · tanpa had masa' if h == 0 else f' · had {h} sesi')


# ---------- enjin ----------
@njit(parallel=True, cache=True)
def atom14(ev, o, l, c, atr, akhir, M):
    """Satu laluan ke hadapan bagi setiap isyarat (hingga stop loss atau bar terakhir saham itu). Pulangkan
    X[n, NK] sesi jual setiap komponen (BESAR = tidak tercetus) dan PJ[n, NK] harga jual / harga beli;
    PC[n, 5] = buka sesi 2, tutup sesi 20, tutup sesi 126, tutup sesi 252, tutup terakhir (NaN jika tiada), semuanya / harga beli;
    nm[n] = bilangan sesi selepas sesi beli yang ada dalam data; h0[n] = tutup hari beli <= paras stop loss.
    Komponen dinilai mulai tutup sesi ke-20 dan dijual pada buka sesi berikutnya (mekanik cs_semak11.pegang)."""
    n = ev.shape[0]
    X = np.full((n, NK), BESAR, np.int64)
    PJ = np.full((n, NK), np.nan)
    PC = np.full((n, 5), np.nan)
    nm = np.zeros(n, np.int64)
    h0 = np.zeros(n, np.bool_)
    for k in prange(n):
        i = ev[k]
        e = i + 1
        P = o[e]
        a0 = atr[i]
        Ls = P - 4.0 * a0
        m = akhir[k] - e
        nm[k] = m
        h0[k] = c[e] <= Ls
        if m >= 1:
            PC[k, 0] = o[e + 1] / P
        if m >= T20 - 1:
            PC[k, 1] = c[e + T20 - 1] / P
        if m >= 125:
            PC[k, 2] = c[e + 125] / P
        if m >= 251:
            PC[k, 3] = c[e + 251] / P
        PC[k, 4] = c[e + m] / P
        hc = c[e]
        for d in range(m + 1):
            b = e + d
            if d >= 1:
                if o[b] <= Ls:
                    X[k, 0], PJ[k, 0] = d, o[b] / P
                    break
                if l[b] <= Ls:
                    X[k, 0], PJ[k, 0] = d, Ls / P
                    break
            cb = c[b]
            if cb > hc:
                hc = cb
            if d < T20 - 1 or d >= m:
                continue
            pj = o[b + 1] / P
            if X[k, 1] == BESAR and cb < P:
                X[k, 1], PJ[k, 1] = d + 1, pj
            if X[k, 2] == BESAR and cb < P - a0:
                X[k, 2], PJ[k, 2] = d + 1, pj
            if d == T20 - 1 and cb < P:
                X[k, 3], PJ[k, 3] = d + 1, pj
            for j in range(4):
                if X[k, 4 + j] == BESAR and cb < M[j, b]:
                    X[k, 4 + j], PJ[k, 4 + j] = d + 1, pj
            for j in range(3):
                if X[k, 8 + j] == BESAR and cb < hc - CH_K[j] * atr[b]:
                    X[k, 8 + j], PJ[k, 8 + j] = d + 1, pj
            if X[k, 11] == BESAR and cb < JATUH * hc:
                X[k, 11], PJ[k, 11] = d + 1, pj
    return X, PJ, PC, nm, h0


@njit(cache=True)
def hasil14(X, PJ, PC, nm, h0, rw, tw, hw):
    """(R, SK, TB)[isyarat, cara]: pulangan bersih, sesi jual (bar jual = isyarat + 1 + SK) dan "masih terbuka pada hujung data"."""
    n, nw = X.shape[0], rw.shape[0]
    R = np.empty((n, nw))
    SK = np.empty((n, nw), np.int64)
    TB = np.zeros((n, nw), np.bool_)
    for k in range(n):
        ds = X[k, 0]
        for w in range(nw):
            if h0[k] and nm[k] >= 1:
                R[k, w], SK[k, w] = PC[k, 0] - 1.0 - KOS, 1
                continue
            h = hw[w]
            if h == -1:
                if ds <= T20 - 1:
                    R[k, w], SK[k, w] = PJ[k, 0] - 1.0 - KOS, ds
                else:
                    R[k, w], SK[k, w] = PC[k, 1] - 1.0 - KOS, T20 - 1
                continue
            cap = h - 1 if h > 0 else BESAR
            lim = min(cap, nm[k])
            x, px = BESAR, np.nan
            if rw[w] > 0:
                x, px = X[k, rw[w]], PJ[k, rw[w]]
            if tw[w] > 0 and X[k, 3 + tw[w]] < x:
                x, px = X[k, 3 + tw[w]], PJ[k, 3 + tw[w]]
            if x <= lim and x <= ds:
                R[k, w], SK[k, w] = px - 1.0 - KOS, x
            elif ds <= lim:
                R[k, w], SK[k, w] = PJ[k, 0] - 1.0 - KOS, ds
            elif cap <= nm[k]:
                R[k, w], SK[k, w] = PC[k, 2 if h == 126 else 3] - 1.0 - KOS, cap
            else:
                R[k, w], SK[k, w], TB[k, w] = PC[k, 4] - 1.0 - KOS, nm[k], True
    return R, SK, TB


@njit(cache=True)
def stat14(ev, tid, tp, R, SK, TB):
    """Satu posisi setiap saham (ikut sesi jual cara itu sendiri), kemudian statistik setiap cara -> S[cara, NS] (susunan STAT)."""
    n, nw = R.shape
    S = np.full((nw, NS), np.nan)
    buf = np.empty(n)
    for w in range(nw):
        t_akhir, b_akhir, m = -1, -1, 0
        jr = mng = r15 = k10_ = k50 = js = tb = 0.0
        nk, jk, mk = np.zeros(3), np.zeros(3), np.zeros(3)
        for k in range(n):
            if tid[k] == t_akhir and ev[k] <= b_akhir:
                continue
            t_akhir, b_akhir = tid[k], ev[k] + 1 + SK[k, w]
            r = R[k, w]
            buf[m] = SK[k, w] + 1
            m += 1
            jr += r
            js += SK[k, w] + 1
            mng += r > 0
            r15 += r <= -0.15
            k10_ += r >= 0.10
            k50 += r >= 0.50
            tb += TB[k, w]
            p = tp[k]
            if 0 <= p < 3:
                nk[p] += 1
                jk[p] += r
                mk[p] += r > 0
        S[w, 0] = m
        S[w, 10:13] = nk
        if m == 0:
            continue
        S[w, 1], S[w, 2], S[w, 3], S[w, 4], S[w, 5] = jr / m, mng / m, r15 / m, k10_ / m, k50 / m
        S[w, 6], S[w, 7], S[w, 8], S[w, 9] = np.median(buf[:m]), js / m, tb / m, jr / js * 20.0
        for p in range(3):
            if nk[p] > 0:
                S[w, 13 + p], S[w, 16 + p] = jk[p] / nk[p], mk[p] / nk[p]
    return S


def atom_panel(pan, ev):
    """Atom bagi senarai isyarat (indeks bar) pada satu panel."""
    ev = np.ascontiguousarray(ev, dtype=np.int64)
    akhir = (pan['mula'][pan['tid'][ev] + 1] - 1).astype(np.int64)
    M = np.stack([k10.sma_panel(pan, n) for n in SMA_N])
    return atom14(ev, pan['o'], pan['l'], pan['c'], pan['atr'], akhir, M)


# ---------- larian ----------
def senarai():
    """(baharu, lama): kod CS13 dengan peraturan masuk masing-masing, dan ID setup lama dalam senarai utama."""
    U = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv'))
    C = pd.read_csv(os.path.join(CS13, 'calon.csv.gz'))
    C = C[C.id_F.notna() & (C.id_F.astype(str) != '')]
    baharu = C[C.id_F.isin(set(U.id[U.asal == 'baharu']))]
    assert len(baharu) == int((U.asal == 'baharu').sum())
    return baharu, list(U.id[U.asal == 'lama'])


def isyarat(kerja, set_, pan):
    """dict id setup -> isyarat (tetingkap 126 sesi lengkap, tersusun) bagi semua setup senarai utama pada satu kumpulan."""
    baharu, lama = senarai()
    L = lapis.muat(kerja, set_)
    Lr = (L['L1'], L['L2'])
    EV = c12.semua_pencetus(kerja, set_)
    sah = s11.sah126(pan)
    bersih = lambda ev: np.ascontiguousarray(ev[sah[ev]], dtype=np.int64)
    out = {}
    for r in baharu.itertuples():
        ev = EV[r.pencetus]
        out[r.id_F] = bersih(ev[c5.topeng(pan, Lr, ev, int(r.q1), int(r.q2), int(r.f1), int(r.f2))])
    for x in s11.setup_f(kerja, set_, pan, t7.semua_ev(kerja, set_, 'asal'), Lr):
        if x['id'] in lama:
            out[x['id']] = bersih(x['ev'])
    assert len(out) == len(baharu) + len(lama)
    return out


def kira(kerja):
    """Statistik setiap setup x cara pada kumpulan A dan B -> cs14_stat.pkl {ids, A[n, W, NS], B[n, W, NS], mxl}."""
    t0, out = time.time(), {}
    for set_ in ('A', 'B'):
        pan = cari.panel(kerja, set_)
        E = isyarat(kerja, set_, pan)
        ids = sorted(E, key=lambda i: int(i[1:]))
        U = np.unique(np.concatenate([E[i] for i in ids]))
        cari.log(f'CS14 {set_}: {len(ids)} setup · {len(U):,} isyarat berbeza · {time.time() - t0:.0f}s')
        X, PJ, PC, nm, h0 = atom_panel(pan, U)
        cari.log(f'CS14 {set_}: atom siap · {time.time() - t0:.0f}s')
        S = np.full((len(ids), W, NS), np.nan)
        for j, i in enumerate(ids):
            ev = E[i]
            if not len(ev):
                continue
            ix = np.searchsorted(U, ev)
            R, SK, TB = hasil14(X[ix], PJ[ix], PC[ix], nm[ix], h0[ix], RW, TW, HW)
            S[j] = stat14(ev, pan['tid'][ev].astype(np.int64), pan['tempoh'][ev].astype(np.int64), R, SK, TB)
        out['ids'], out[set_] = ids, S
        if set_ == 'B':
            out['mxl'] = kes(pan, 'MXL', 20260421)
        cari.log(f'CS14 {set_}: statistik siap · {time.time() - t0:.0f}s')
    pickle.dump(out, open(F_(kerja), 'wb'), protocol=4)
    return out


def kawalan(kerja):
    """Tambahan post hoc (x): bar layak rawak kumpulan B (benih tetap), cara dan mekanik sama -> D['kawalan'][cara, NS]."""
    D = pickle.load(open(F_(kerja), 'rb'))
    pan = cari.panel(kerja, 'B')
    sah = np.flatnonzero(s11.sah126(pan))
    ev = np.sort(np.random.default_rng(BENIH_KAWALAN).choice(sah, N_KAWALAN, replace=False)).astype(np.int64)
    R, SK, TB = hasil14(*atom_panel(pan, ev), RW, TW, HW)
    D['kawalan'] = stat14(ev, pan['tid'][ev].astype(np.int64), pan['tempoh'][ev].astype(np.int64), R, SK, TB)
    D['n_kawalan'] = int(len(ev))
    pickle.dump(D, open(F_(kerja), 'wb'), protocol=4)
    cari.log(f"CS14 kawalan: {len(ev):,} bar rawak · cara sekarang purata {D['kawalan'][SEKARANG, 1]:+.4f}")
    return D


def kumpulan(D):
    """Tiga kumpulan setup bagi tangga tukar ganti: semua, 42 lama, "pilihan" (senarai utama CS13)."""
    U = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv')).set_index('id').loc[D['ids']]
    return (('semua setup', np.ones(len(U), bool)), ('setup lama yang dipercayai', (U.asal == 'lama').to_numpy()),
            ('setup "pilihan"', U.pilihan.astype(bool).to_numpy()))


def tangga(D):
    """Tambahan post hoc (x): cara sekarang + lima cara wakil bagi tiga kumpulan setup (kumpulan B; nilai tengah)."""
    S, baris = D['B'], []
    for nama, g in kumpulan(D):
        for c in TANGGA:
            w = CARA.index(c)
            k3 = g & (S[:, w, IX['n_K3']] >= MIN_K3) & (S[:, SEKARANG, IX['n_K3']] >= MIN_K3)
            b = dict(kumpulan=nama, n_setup=int(g.sum()), cara=c, teks=teks(w))
            b.update({st: float(np.nanmedian(S[g, w, IX[st]])) for st in ('n', 'purata', 'menang', 'rugi15', 'k50', 'sesi_med', 'per20')})
            b.update(d_purata_K3=float(np.nanmedian(S[k3, w, IX['purata_K3']] - S[k3, SEKARANG, IX['purata_K3']])) if k3.any() else np.nan,
                     d_menang_K3=float(np.nanmedian(S[k3, w, IX['menang_K3']] - S[k3, SEKARANG, IX['menang_K3']])) if k3.any() else np.nan)
            baris.append(b)
    return pd.DataFrame(baris)


def kes(pan, ticker, tarikh):
    """Satu kes rujukan (contoh, bukan bukti): hasil setiap cara bagi isyarat pada (ticker, tarikh)."""
    t = np.flatnonzero(pan['ticker'] == ticker)
    if not len(t):
        return None
    a, b = pan['mula'][t[0]], pan['mula'][t[0] + 1]
    i = np.flatnonzero(pan['tarikh'][a:b] == tarikh)
    if not len(i) or a + i[0] + 1 >= b:
        return None
    ev = np.array([a + i[0]], np.int64)
    X, PJ, PC, nm, h0 = atom_panel(pan, ev)
    R, SK, TB = hasil14(X, PJ, PC, nm, h0, RW, TW, HW)
    e = ev[0] + 1
    return dict(ticker=ticker, beli=int(pan['tarikh'][e]), harga=float(pan['o'][e]), hingga=int(pan['tarikh'][b - 1]),
                puncak=float(pan['c'][e:b].max() / pan['o'][e] - 1),
                R=[float(x) for x in R[0]], sesi=[int(x) + 1 for x in SK[0]], terbuka=[bool(x) for x in TB[0]],
                jual=[int(pan['tarikh'][min(e + int(x), b - 1)]) for x in SK[0]])


# ---------- pemilihan dan bacaan ----------
def beza(S, ok, w, stat):
    """Beza cara w lawan cara sekarang bagi setiap setup layak."""
    return S[ok, w, IX[stat]] - S[ok, SEKARANG, IX[stat]]


def pilih(SA, ok, calon):
    """Cara terpilih pada kumpulan A (pindaan (x)): Δpurata tertinggi antara calon yang Δmenang >= -2 mata dan Δrugi15 <= +2
    mata; jika tiada, Δpurata tertinggi antara semua calon. Pulangkan (w, menepati_syarat)."""
    md = lambda w, st: float(np.nanmedian(beza(SA, ok, w, st)))
    lulus = [w for w in calon if md(w, 'menang') >= D_MENANG and md(w, 'rugi15') <= D_RUGI]
    kolam = lulus or list(calon)
    return max(kolam, key=lambda w: md(w, 'purata')), bool(lulus)


def baca(SB, ok, w):
    """Bacaan dikunci pada kumpulan B bagi cara w lawan cara sekarang."""
    dp, dm, dr = beza(SB, ok, w, 'purata'), beza(SB, ok, w, 'menang'), beza(SB, ok, w, 'rugi15')
    k3 = ok & (SB[:, w, IX['n_K3']] >= MIN_K3) & (SB[:, SEKARANG, IX['n_K3']] >= MIN_K3)
    d3 = SB[k3, w, IX['purata_K3']] - SB[k3, SEKARANG, IX['purata_K3']]
    b = dict(cara=CARA[w], n=int(ok.sum()), lebih=int((dp > 0).sum()), d_purata=float(np.nanmedian(dp)),
             d_menang=float(np.nanmedian(dm)), d_rugi15=float(np.nanmedian(dr)), n_K3=int(k3.sum()),
             d_purata_K3=float(np.nanmedian(d3)) if k3.any() else float('nan'),
             lebih_K3=int((d3 > 0).sum()))
    b['s1'], b['s2'], b['s3'] = bool(b['lebih'] > b['n'] / 2), bool(b['d_menang'] >= D_MENANG), bool(b['d_rugi15'] <= D_RUGI)
    b['s4'] = bool(b['d_purata_K3'] > 0)
    b['ya'] = bool(b['s1'] and b['s2'] and b['s3'] and b['s4'])
    return b


def bacaan(D):
    SA, SB = D['A'], D['B']
    ok = (SA[:, SEKARANG, 0] >= MIN_DAG) & (SB[:, SEKARANG, 0] >= MIN_DAG)
    out = dict(n_setup=int(len(D['ids'])), n_layak=int(ok.sum()))
    for nm, calon in (('semua', CALON), ('kelas_A', KELAS_A), ('kelas_B', KELAS_B)):
        w, tepat = pilih(SA, ok, calon)
        out[nm] = dict(baca(SB, ok, w), w=int(w), menepati_A=tepat,
                       A=dict(d_purata=float(np.nanmedian(beza(SA, ok, w, 'purata'))), d_menang=float(np.nanmedian(beza(SA, ok, w, 'menang'))),
                              d_rugi15=float(np.nanmedian(beza(SA, ok, w, 'rugi15')))))
    return out, ok


def pariti(D):
    """Cara sekarang (r0.t1.126) mesti menghasilkan semula angka senarai utama pada kumpulan B. Pulangkan beza terbesar."""
    U = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv')).set_index('id').loc[D['ids']]
    S = D['B'][:, SEKARANG]
    return {k: float(np.nanmax(np.abs(S[:, IX[a]] - U[b].to_numpy(float)))) for k, a, b in (
        ('n', 'n', 'n_B'), ('menang', 'menang', 'menang_B'), ('purata', 'purata', 'purata_B'), ('rugi15', 'rugi15', 'rugi15_B'),
        ('hari', 'sesi_med', 'hari_B'))}


def jadual_cara(D, ok):
    """Satu baris setiap cara x kumpulan: nilai tengah merentas setup layak, dan beza lawan cara sekarang."""
    baris = []
    for set_ in ('A', 'B'):
        S = D[set_]
        for w in range(W):
            md = lambda st: float(np.nanmedian(S[ok, w, IX[st]])) if np.isfinite(S[ok, w, IX[st]]).any() else np.nan
            b = dict(set=set_, cara=CARA[w], rugi=f'r{RW[w]}' if HW[w] >= 0 else '', trend=f't{TW[w]}' if HW[w] >= 0 else '',
                     had={-1: 20, 0: 0}.get(int(HW[w]), int(HW[w])), teks=teks(w), calon=w in CALON,
                     kelas='A' if w in KELAS_A else 'B' if w in KELAS_B else '')
            b.update({st: md(st) for st in STAT})
            b.update(d_purata=float(np.nanmedian(beza(S, ok, w, 'purata'))), d_menang=float(np.nanmedian(beza(S, ok, w, 'menang'))),
                     d_rugi15=float(np.nanmedian(beza(S, ok, w, 'rugi15'))),
                     lebih=float((beza(S, ok, w, 'purata') > 0).mean()))
            baris.append(b)
    return pd.DataFrame(baris)


# ---------- laporan ----------
def _bersih(x):
    """NaN -> None dan jenis numpy -> jenis Python, secara rekursif (JSON sah)."""
    if isinstance(x, dict):
        return {k: _bersih(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_bersih(v) for v in x]
    if isinstance(x, (float, np.floating)):
        return None if x != x else round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def lapor_(kerja):
    D = pickle.load(open(F_(kerja), 'rb'))
    par = pariti(D)
    assert par['n'] == 0 and par['hari'] == 0 and max(par['menang'], par['purata'], par['rugi15']) < 2e-5, f'pariti gagal: {par}'
    B, ok = bacaan(D)
    B['pariti'] = par
    for k in ('semua', 'kelas_A', 'kelas_B'):
        B[k]['sama'] = bool(abs(B[k]['d_purata']) < SAMA)                # post hoc: lulus tetapi secara praktikal cara yang sama
    T = jadual_cara(D, ok)
    if 'kawalan' in D:
        kw = pd.DataFrame(D['kawalan'], columns=STAT)
        kw.insert(0, 'cara', CARA)
        T = T.merge(kw[['cara', 'n', 'purata', 'menang', 'rugi15', 'per20']].rename(columns=lambda c: c if c == 'cara' else 'rawak_' + c), on='cara')
        B['n_kawalan'] = D['n_kawalan']
    G = tangga(D)
    os.makedirs(HASIL, exist_ok=True)
    T.to_csv(os.path.join(HASIL, 'cara.csv'), index=False, float_format='%.5f')
    G.to_csv(os.path.join(HASIL, 'tangga.csv'), index=False, float_format='%.5f')
    utama = list(dict.fromkeys([CARA.index(c) for c in TANGGA] + [B[k]['w'] for k in ('semua', 'kelas_A', 'kelas_B')]))
    lajur = ('n', 'purata', 'menang', 'rugi15', 'k50', 'sesi_med', 'terbuka', 'purata_K3', 'menang_K3')
    Sx = pd.DataFrame({'id': D['ids'], 'layak': ok})
    for w in utama:
        for st in lajur:
            Sx[f'{CARA[w]}:{st}'] = D['B'][:, w, IX[st]]
    Sx.to_csv(os.path.join(HASIL, 'setup.csv.gz'), index=False, float_format='%.4f')
    json.dump(_bersih(dict(B, mxl=D.get('mxl'), cara=CARA, utama=[CARA[w] for w in utama], tangga=G.to_dict('records'))),
              open(os.path.join(HASIL, 'bacaan.json'), 'w'), indent=1)
    open(os.path.join(HASIL, 'PEGANG.md'), 'w', encoding='utf-8').write(teks_laporan(D, B, T, G))
    cari.log(f"CS14 lapor: terpilih {B['semua']['cara']} -> {'MENOLONG' if B['semua']['ya'] else 'TIDAK menolong'}"
             f"{' (secara praktikal sama dengan cara sekarang)' if B['semua']['sama'] else ''}")
    return B


def teks_laporan(D, B, T, G):
    p = lambda x, d=0, tanda=False: '–' if x is None or x != x else f'{x * 100:{"+" if tanda else ""}.{d}f}'
    TB_ = T[T.set == 'B'].set_index('cara')
    TA_ = T[T.set == 'A'].set_index('cara')
    ada_kw = 'rawak_purata' in T.columns
    s, a, b = B['semua'], B['kelas_A'], B['kelas_B']
    ya = lambda x: 'ya' if x else 'TIDAK'
    nama_w = lambda w: 'beli dan simpan, stop loss sahaja (rujukan)' if w == SIMPAN else 'pegang 6 bulan, stop loss sahaja' if w == P126 else teks(w)

    def baris(w):
        r = TB_.loc[CARA[w]]
        rawak = f" {p(r.rawak_purata, 1, True)} · {p(r.rawak_menang)} · {p(r.rawak_per20, 2, True)} |" if ada_kw else ''
        return (f"| {nama_w(w)} | {p(r.purata, 1, True)} | {p(r.menang)} | {p(r.rugi15)} | {p(r.k50, 1)} | {r.sesi_med:.0f} | "
                f"{p(r.per20, 2, True)} | {p(r.terbuka, 1)} | {r.n:.0f} |{rawak}")

    kepala = ('| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | '
              'Untung setiap 20 hari pegang % | Masih dipegang pada hujung data % | Dagangan setiap setup |'
              + (' Saham rawak, cara sama: purata % · menang % · setiap 20 hari % |' if ada_kw else '')
              + '\n|---|---|---|---|---|---|---|---|---|' + ('---|' if ada_kw else ''))

    def baca_teks(x, tajuk):
        nota = (' Beza purata kurang 0.1 mata: **secara praktikal ini cara yang sama dengan cara sekarang**, jadi lulus ujian di sini '
                'TIDAK bermakna ada pembaikan.' if x['sama'] else '')
        return (f"- **{tajuk}: {teks(x['w'])}** (`{x['cara']}`; {'menepati' if x['menepati_A'] else 'TIADA calon menepati'} syarat pemilihan "
                f"pada saham carian). Pada saham yang carian tidak lihat, lawan cara sekarang: (1) purata lebih tinggi bagi "
                f"{x['lebih']:,} daripada {x['n']:,} setup → {ya(x['s1'])}; (2) beza kadar menang {p(x['d_menang'], 1, True)} mata "
                f"(perlu ≥ −2) → {ya(x['s2'])}; (3) beza rugi ≥ 15 % {p(x['d_rugi15'], 1, True)} mata (perlu ≤ +2) → {ya(x['s3'])}; "
                f"(4) dagangan 2025–26: beza purata {p(x['d_purata_K3'], 1, True)} mata ({x['lebih_K3']:,} daripada {x['n_K3']:,} setup "
                f"lebih tinggi; perlu > 0) → {ya(x['s4'])}. **Keputusan: {'MENOLONG' if x['ya'] else 'TIDAK menolong'}.**{nota}")

    A = ['# CS14: cara pegang "jual yang rugi, pegang yang untung", tanpa had masa (backtest; BUKAN bukti)', '',
         'Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (x). Dijana `cs_pegang14.py`; jangan sunting.', '',
         '- Permintaan pengguna 16 Nov 2026: pegang selagi untung, jual bila rugi, tiada had 20 hari; keputusan "ya dan C".',
         f"- {B['n_setup']:,} setup senarai utama; {B['n_layak']:,} dengan ≥ {MIN_DAG} dagangan dalam kedua-dua kumpulan saham. Peraturan beli dan "
         'stop loss (4×ATR14) tidak diubah; 20 hari pertama tidak diubah. Kadar tangkap tidak terkesan oleh cara pegang.',
         f'- {W - 1} cara diuji: 4 peraturan "rugi" × 9 peraturan "trend tamat" × 3 had masa (126 sesi, 252 sesi, tiada). Cara dipilih pada '
         'saham carian; keputusan dibaca pada saham yang carian tidak lihat.',
         f"- Semakan pariti: cara sekarang menghasilkan semula angka senarai utama (beza terbesar kadar menang "
         f"{B['pariti']['menang']:.6f}, purata {B['pariti']['purata']:.6f}).", '',
         '## 1. Keputusan (ujian ditetapkan dahulu)', '', baca_teks(s, 'Cara terpilih'), baca_teks(a, 'Terbaik tafsiran A (selagi di atas harga beli)'),
         baca_teks(b, 'Terbaik tafsiran B (selagi trend naik)'), '',
         '**Ringkasnya:** tiada cara yang menaikkan purata setiap dagangan TANPA menurunkan kadar menang. Makin longgar peraturan jual, makin '
         'besar purata dan makin kurang dagangan yang menang (tangga di bawah). "Jual hanya bila sudah rugi" bermakna hampir setiap dagangan '
         'yang dijual ialah dagangan rugi: untung yang ada dipulangkan dahulu sebelum jualan.', '',
         '## 2. Tangga tukar ganti (tambahan selepas hasil dilihat; saham yang carian tidak lihat; nilai tengah setiap kumpulan setup)', '']
    for nama in G.kumpulan.unique():
        X = G[G.kumpulan == nama]
        A += [f'**{nama[0].upper() + nama[1:]} ({int(X.n_setup.iloc[0]):,})**', '',
              '| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | Untung setiap 20 hari pegang % | '
              '2025–26: beza purata lawan cara sekarang (mata) | 2025–26: beza menang (mata) |', '|---|---|---|---|---|---|---|---|---|']
        for r in X.itertuples():
            A.append(f"| {r.teks} | {p(r.purata, 1, True)} | {p(r.menang)} | {p(r.rugi15)} | {p(r.k50, 1)} | {r.sesi_med:.0f} | {p(r.per20, 2, True)} | "
                     f"{p(r.d_purata_K3, 1, True)} | {p(r.d_menang_K3, 1, True)} |")
        A.append('')
    if ada_kw:
        A += [f"**Saham rawak, cara sama ({B['n_kawalan']:,} belian rawak mana-mana saham mana-mana hari):** berapa banyak hasil pegang lama "
              'datang daripada sekadar memegang saham dalam data ini (pasaran naik; tiada saham delist), bukan daripada setup.', '',
              '| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung setiap 20 hari pegang % |', '|---|---|---|---|---|']
        for c in TANGGA:
            r = TB_.loc[c]
            A.append(f"| {teks(CARA.index(c))} | {p(r.rawak_purata, 1, True)} | {p(r.rawak_menang)} | {p(r.rawak_rugi15)} | {p(r.rawak_per20, 2, True)} |")
        A.append('')
    A += ['## 3. Sebelah-menyebelah dengan rujukan (nilai tengah merentas semua setup; saham yang carian tidak lihat)', '', kepala]
    for w in dict.fromkeys([0, SEKARANG, P126, SIMPAN, a['w'], b['w'], s['w']]):
        A.append(baris(w))
    A += ['', '"Untung setiap 20 hari pegang" = jumlah untung ÷ jumlah hari pegang × 20: pegang lebih lama menaikkan purata setiap dagangan '
          'walaupun tanpa kemahiran, jadi lajur ini menunjukkan untung bagi tempoh pegang yang sama.', '',
          '## 4. Semua cara tanpa had masa (saham yang carian tidak lihat; beza lawan cara sekarang, nilai tengah)', '',
          '| Peraturan rugi | Peraturan trend tamat | Purata % | Menang % | Rugi ≥ 15 % % | Median hari | Δ purata (mata) | Δ menang (mata) | Δ rugi ≥ 15 % (mata) | Setup lebih baik % |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for w in [SIMPAN] + CALON:
        r = TB_.loc[CARA[w]]
        A.append(f"| {RUGI[f'r{RW[w]}']} | {TREND[f't{TW[w]}']} | {p(r.purata, 1, True)} | {p(r.menang)} | {p(r.rugi15)} | {r.sesi_med:.0f} | "
                 f"{p(r.d_purata, 1, True)} | {p(r.d_menang, 1, True)} | {p(r.d_rugi15, 1, True)} | {p(r.lebih)} |")
    w0 = s['w']
    A += ['', '## 5. Kesan had masa pada cara terpilih', '', kepala]
    for h in HAD:
        A.append(baris(CARA.index(f'r{RW[w0]}.t{TW[w0]}.{h}')))
    A += ['', '## 6. Pemilihan pada saham carian (kumpulan A; nilai tengah beza lawan cara sekarang)', '',
          '| Cara | Δ purata (mata) | Δ menang (mata) | Δ rugi ≥ 15 % (mata) |', '|---|---|---|---|']
    for w in sorted(CALON, key=lambda w: -TA_.loc[CARA[w]].d_purata)[:12]:
        r = TA_.loc[CARA[w]]
        A.append(f'| {teks(w)} | {p(r.d_purata, 1, True)} | {p(r.d_menang, 1, True)} | {p(r.d_rugi15, 1, True)} |')
    m = D.get('mxl')
    if m:
        A += ['', f"## 7. Kes rujukan pengguna: {m['ticker']} (satu contoh, bukan bukti)", '',
              f"Beli {m['beli']} pada {m['harga']:.2f}; data hingga {m['hingga']}; tutup tertinggi {p(m['puncak'], 0, True)} %.", '',
              '| Cara pegang | Jual | Hari | Untung % |', '|---|---|---|---|']
        for w in dict.fromkeys([0] + [CARA.index(c) for c in TANGGA] + [SIMPAN]):
            A.append(f"| {nama_w(w).replace(' (rujukan)', '')} | {'masih dipegang' if m['terbuka'][w] else m['jual'][w]} | {m['sesi'][w]} | {p(m['R'][w], 0, True)} |")
    A += ['', '## 8. Kaveat', '',
          '- Tiada saham delist dalam data: saham yang gagal hilang, dan bias ini membesar dengan tempoh pegang. Purata cara yang memegang '
          'bertahun-tahun (cth. "tutup di bawah harga beli" sahaja) dikuasai beberapa saham yang naik berganda dan TIDAK boleh dipercayai.',
          '- Posisi yang masih dipegang pada hujung data dinilai pada harga terakhir, bukan harga jual.',
          f'- {W - 1} cara dicuba; yang terbaik condong ke atas. Kumpulan saham "tidak dilihat" sudah dilihat berkali-kali; 2025–26 pendek.',
          '- Tangga tukar ganti dan kawalan rawak ditambah SELEPAS hasil dilihat (maklumat; bukan sebahagian ujian yang ditetapkan dahulu).',
          '- Laporan dan cadangan sahaja: senarai utama, registry dan kohort tidak diubah. Menukar cara pegang ialah keputusan pengguna.', '']
    return '\n'.join(A)


if __name__ == '__main__':
    langkah, kerja = sys.argv[1], sys.argv[2]
    {'kira': kira, 'kawalan': kawalan, 'lapor': lapor_}[langkah](kerja)
