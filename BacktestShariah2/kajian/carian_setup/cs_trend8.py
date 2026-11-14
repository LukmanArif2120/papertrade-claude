"""Carian setup — pusingan CS08: LORONG KEDUA "beli selepas pengesahan uptrend, pegang sampai trend tamat"
(SPEC pindaan 14 Nov 2026 (q); permintaan pengguna, kes MXL).

Lorong berasingan daripada swing 20 sesi: had pegang 126 sesi; label masuk `besar` = tutup capai >= +50 % sebelum mana-mana
tutup <= -15 %; skor dan enjin prasyarat x penapis sama seperti (i)/(n); keluar = indikator trend tamat (38 atom x 3 syarat
aktif x 6 henti). Henti rugi wajib, tiada jual hari beli, pegang minimum 3 sesi (pindaan (p)).
Guna: python3 cs_trend8.py skor|pilih|benihB|keluar|kunci|lapor <kerja>. Jangan sunting keluaran secara manual."""
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
import cs_cs05 as c5  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_param as kp  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

H_MAX, NAIK, NAIK2, JATUH, TB, KOS = 126, 0.50, 1.00, 0.15, 0.30, teras.KOS      # dikunci pindaan (q)
HENTI = ['-10%', '-15%', '-20%', '4xATR14', '6xATR14', 'min(-15%, 5xATR14)']
NH = len(HENTI)
AKTIF = ['sentiasa', 'selepas +10%', 'selepas +20%']
NG = len(AKTIF)
N_PAPAN, MAKS_INDUK, MAKS_PRA, N_SEJAGAT = 12, 2, 3, 10
MIN_BELIAN, MIN_TAHUN = 200, 8
PEGANG_MIN = atom.PEGANG_MIN
BAHAGIAN = ('asal', 'K', 'M1', 'M2')


def atom_keluar():
    """(kod, jenis, parameter, teks): jenis 0 siri bar; 1 Chandelier k x ATR14; 2 ekor p x tutup tertinggi; 3 tiada kemajuan."""
    A = []
    add = lambda jenis, teks, **p: A.append((jenis, p, teks))
    for n in (20, 50, 100, 150):
        add(0, f'tutup < MA{n}', f='ma', n=n)
    for n in (20, 50, 100):
        add(0, f'dua tutup berturut < MA{n}', f='ma2', n=n)
    add(0, 'MA20 < MA50', f='silang')
    add(0, 'MA50 menurun (lawan 5 sesi lalu)', f='cerun')
    for n in (20, 50, 100):
        add(0, f'tutup < EMA{n}', f='ema', n=n)
    for n, m in ((10, 3.0), (10, 4.0), (14, 3.0), (14, 4.0), (20, 5.0)):
        add(0, f'Supertrend({n}, {m}) turun', f='st', n=n, m=m)
    for k in (10, 20, 50):
        add(0, f'tutup < rendah {k} hari', f='ll', k=k)
    for a, b, g in ((12, 26, 9), (24, 52, 18)):
        add(0, f'MACD({a},{b},{g}) < isyarat', f='macd', a=a, b=b, g=g)
    for x in (35, 40, 45, 50):
        add(0, f'RSI14 < {x}', f='rsi', x=x)
    for k in (3.0, 4.0, 5.0, 6.0, 8.0):
        add(1, f'Chandelier {k}xATR14 dari tutup tertinggi', k=k)
    for p in (0.70, 0.75, 0.80, 0.85, 0.90):
        add(2, f'tutup < {p:.0%} tutup tertinggi sejak beli', k=p)
    for d in (20, 40):
        add(3, f'tiada kemajuan (selepas {d} sesi, tutup < harga beli)', k=d)
    return [(f'T{i + 1:02d}', j, p, t) for i, (j, p, t) in enumerate(A)]


ATOM = atom_keluar()
NA = len(ATOM)
JENIS = np.asarray([a[1] for a in ATOM], np.int64)
PAR = np.asarray([float(a[2].get('k', 0)) if a[1] else 0.0 for a in ATOM])
BARIS = np.cumsum(JENIS == 0) - 1
NKOL = 1 + NA * NG                                      # lajur 0 = X00; lajur 1 + atom * NG + aktif
_T = [a[3] for a in ATOM]
# keluar rujukan untuk laporan (maklumat, bukan pilihan): lajur X00 dan beberapa indikator "trend tamat" yang biasa
RUJUKAN = [0] + [1 + _T.index(t) * NG for t in (
    'tutup < MA50', 'dua tutup berturut < MA50', 'MA20 < MA50', 'tutup < rendah 20 hari', 'Supertrend(14, 4.0) turun',
    'Chandelier 5.0xATR14 dari tutup tertinggi', 'Chandelier 8.0xATR14 dari tutup tertinggi',
    'tutup < 80% tutup tertinggi sejak beli', 'tiada kemajuan (selepas 40 sesi, tutup < harga beli)')]


def nama_keluar(kol):
    if kol == 0:
        return 'X00 tiada keluar indikator (henti + 126 sesi)'
    a, g = divmod(int(kol) - 1, NG)
    return ATOM[a][3] + ('' if g == 0 else f' [aktif {AKTIF[g]}]')


def siri(g):
    I = kp.Ind(g, None)
    c = I.c
    out = []
    for _, jenis, p, _ in ATOM:
        if jenis:
            continue
        f = p['f']
        if f == 'ma':
            s = c < I.sma(p['n'])
        elif f == 'ma2':
            x = c < I.sma(p['n'])
            s = x & atom._dulu(x)
        elif f == 'silang':
            s = I.sma(20) < I.sma(50)
        elif f == 'cerun':
            s = I.sma(50) < I.sma(50).shift(5)
        elif f == 'ema':
            s = c < I.ema(p['n'])
        elif f == 'st':
            s = I.st(p['n'], p['m']) < 0
        elif f == 'll':
            s = c < I.ll(p['k'])
        elif f == 'macd':
            m = I.ema(p['a']) - I.ema(p['b'])
            s = m < m.ewm(span=p['g'], adjust=False).mean()
        else:
            s = I.rsi(14) < p['x']
        out.append(np.asarray(s.fillna(False) if s.dtype != bool else s, dtype=bool))
    return np.stack(out)


_W = {}


def _siri_satu(julat):
    a, b = julat
    return np.concatenate([siri(_W['fr'][t]) for t in _W['tick'][a:b]], axis=1).astype(np.uint8)


def siri_set(kerja, set_):
    f = os.path.join(kerja, f'cs08_XT_{set_}.npy')
    if os.path.exists(f):
        return np.load(f, mmap_mode='r')
    pan = cari.panel(kerja, set_)
    fr, _, _ = cari.muat_set(set_)
    tick = sorted(fr)
    assert list(pan['ticker']) == tick
    _W.update(fr=fr, tick=tick)
    julat = [(a, min(a + 25, len(tick))) for a in range(0, len(tick), 25)]
    with mp.get_context('fork').Pool(cari.PEKERJA) as pool:
        XT = np.concatenate(list(pool.imap(_siri_satu, julat)), axis=1)
    _W.clear()
    assert XT.shape == (int((JENIS == 0).sum()), len(pan['c']))
    np.save(f, XT)
    return XT


# ---------- label ----------
def sah8(pan):
    """Bar layak dengan tetingkap 126 sesi lengkap."""
    i = np.arange(len(pan['c']))
    akhir = pan['mula'][pan['tid'] + 1]
    return pan['sah'] & (i + H_MAX < akhir)


@njit(parallel=True, cache=True)
def label8(ev, o, c):
    """[besar, besar100, puncak]: tutup capai >= +50 % (+100 %) sebelum mana-mana tutup <= -15 %, dalam 126 sesi."""
    out = np.zeros((ev.shape[0], 3), np.float32)
    for k in prange(ev.shape[0]):
        e = ev[k] + 1
        P = o[e]
        mx = c[e]
        mati = False
        for d in range(H_MAX):
            x = c[e + d]
            if x > mx:
                mx = x
            if not mati:
                if x >= P * (1.0 + NAIK):
                    out[k, 0] = 1.0
                if x >= P * (1.0 + NAIK2):
                    out[k, 1] = 1.0
                if x <= P * (1.0 - JATUH):
                    mati = True
        out[k, 2] = mx / P - 1.0
    return out


def label_v(pan):
    """(S8 topeng bar, V[bar] = (besar, asas hari sama x tercile ATR %, asas era x tercile), L8[bar] = label penuh)."""
    S8 = sah8(pan)
    sah = np.flatnonzero(S8)
    Lb = label8(sah, pan['o'], pan['c'])
    hari = pan['hari'][sah]
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(hari).rank(pct=True).to_numpy()
    terc = np.minimum((pct * 3).astype(np.int64), 2)
    N = len(pan['c'])
    V = np.zeros((N, 3))
    V[sah, 0] = Lb[:, 0]
    g = hari * 3 + terc
    for a, gg in ((1, g), (2, pan['tempoh'][sah].astype(np.int64) * 3 + terc)):
        V[sah, a] = (np.bincount(gg, Lb[:, 0]) / np.maximum(np.bincount(gg), 1))[gg]
    L8 = np.zeros((N, 4), np.float32)                       # besar, besar100, puncak, asas besar100
    L8[sah, :3] = Lb
    L8[sah, 3] = (np.bincount(g, Lb[:, 1]) / np.maximum(np.bincount(g), 1))[g]
    G = np.full(N, -1, np.int64)
    G[sah] = g
    return S8, V, L8, G


# ---------- skor masuk (kumpulan A) ----------
def skor(kerja, bahagian):
    f = os.path.join(kerja, f'cs08_skor_{bahagian}.pkl')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    pan = cari.panel(kerja, 'A')
    S8, V, _, _ = label_v(pan)
    ev = {n: e[S8[e]] for n, e in t7.semua_ev(kerja, 'A', bahagian).items()}
    cari.log(f'CS08 skor {bahagian}: {sum(1 for n in ev if n not in siap)} pencetus; asas besar {V[S8, 0].mean() * 100:.2f}%')
    siap = t7.skor_ev(kerja, ev, siap, f, V=V)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    cari.log(f"CS08 skor {bahagian} siap: {sum(1 for r in siap.values() if r.get('cukup'))} cukup isyarat daripada {len(siap)}")


def pilih(kerja):
    """Papan 12 setup teratas ikut skor A -> cs08_papan.pkl, cs08_jadual.pkl."""
    T = t7.jadual(kerja, awalan='cs08')
    papan, bil_i, bil_p = [], {}, {}
    for r in T.itertuples():
        if bil_i.get(r.induk, 0) >= MAKS_INDUK or bil_p.get((r.q1, r.q2), 0) >= MAKS_PRA or r.skor <= 0:
            continue
        bil_i[r.induk] = bil_i.get(r.induk, 0) + 1
        bil_p[(r.q1, r.q2)] = bil_p.get((r.q1, r.q2), 0) + 1
        papan.append(dict(id=f'T{len(papan) + 1:02d}', pencetus=r.nama, q1=r.q1, q2=r.q2, f1=r.f1, f2=r.f2, skor=r.skor,
                          bahagian=r.bahagian))
        if len(papan) == N_PAPAN:
            break
    pickle.dump(T, open(os.path.join(kerja, 'cs08_jadual.pkl'), 'wb'), protocol=4)
    pickle.dump(papan, open(os.path.join(kerja, 'cs08_papan.pkl'), 'wb'), protocol=4)
    cari.log(f"CS08 pilih: {len(T)} pencetus berskor; skor > 0: {int((T.skor > 0).sum())}; papan {len(papan)}; "
             f"teratas {T.nama.iloc[0]} {T.skor.iloc[0] * 100:+.2f} mata")
    return T, papan


def benih_b(kerja):
    """Benih kumpulan B bagi varian M CS07 pada papan yang belum ada."""
    papan = pickle.load(open(os.path.join(kerja, 'cs08_papan.pkl'), 'rb'))
    P = t7.param_semua(kerja)
    tugas = [(b['pencetus'], b['pencetus'].split('.')[0], P[b['pencetus']]) for b in papan if b['bahagian'] in ('M1', 'M2')]
    if tugas:
        cari.benih(kerja, 'B', tugas=tugas, fail=t7.FAIL_M.format('B'))


# ---------- kernel keluar 126 sesi ----------
@njit(cache=True)
def _aras(P, a, L):
    L[0], L[1], L[2] = P * 0.90, P * 0.85, P * 0.80
    L[3], L[4] = P - 4.0 * a, P - 6.0 * a
    L[5] = min(P * 0.85, P - 5.0 * a)


@njit(parallel=True, cache=True)
def hasil_semua(ev, o, l, c, atr, XT, jenis, par, baris, pegang_min):
    """R[isyarat, henti, lajur] (float32) dan indeks sesi jual (int16). Mekanik seperti cs_keluar7, had 126 sesi."""
    n, nA = ev.shape[0], jenis.shape[0]
    R = np.zeros((n, NH, 1 + nA * NG), np.float32)
    SK = np.zeros((n, NH, 1 + nA * NG), np.int16)
    for k in prange(n):
        i = ev[k]
        e = i + 1
        P = o[e]
        L = np.zeros(NH)
        _aras(P, atr[i], L)
        dx = np.full((nA, NG), 999, np.int64)
        hc = c[e]
        for d in range(H_MAX - 1):
            b = e + d
            if c[b] > hc:
                hc = c[b]
            if d < pegang_min - 1:
                continue
            a10, a20 = hc >= P * 1.10, hc >= P * 1.20
            for a in range(nA):
                if dx[a, 0] != 999 and dx[a, 1] != 999 and dx[a, 2] != 999:
                    continue
                j = jenis[a]
                if j == 0:
                    ya = XT[baris[a], b] != 0
                elif j == 1:
                    ya = c[b] < hc - par[a] * atr[b]
                elif j == 2:
                    ya = c[b] < par[a] * hc
                else:
                    ya = (d + 1 >= par[a]) and (c[b] < P)
                if ya:
                    if dx[a, 0] == 999:
                        dx[a, 0] = d + 1
                    if a10 and dx[a, 1] == 999:
                        dx[a, 1] = d + 1
                    if a20 and dx[a, 2] == 999:
                        dx[a, 2] = d + 1
        for s in range(NH):
            h0 = c[e] <= L[s]
            ds, ps = 999, 0.0
            for d in range(1, H_MAX):
                b = e + d
                if o[b] <= L[s]:
                    ds, ps = d, o[b]
                    break
                if l[b] <= L[s]:
                    ds, ps = d, L[s]
                    break
            for kol in range(1 + nA * NG):
                x = 999
                if kol > 0:
                    x = dx[(kol - 1) // NG, (kol - 1) % NG]
                if h0:
                    R[k, s, kol], SK[k, s, kol] = o[e + 1] / P - 1.0 - KOS, 1
                elif x != 999 and x <= ds:
                    R[k, s, kol], SK[k, s, kol] = o[e + x] / P - 1.0 - KOS, x
                elif ds != 999:
                    R[k, s, kol], SK[k, s, kol] = ps / P - 1.0 - KOS, ds
                else:
                    R[k, s, kol], SK[k, s, kol] = c[e + H_MAX - 1] / P - 1.0 - KOS, H_MAX - 1
    return R, SK


def _hasil(pan, XT, ev):
    return hasil_semua(np.ascontiguousarray(ev, dtype=np.int64), pan['o'], pan['l'], pan['c'], pan['atr'], XT, JENIS, PAR,
                       BARIS, PEGANG_MIN)


def _ev_papan(kerja, set_, pan, Lr, S8, b):
    ev = t7.ev_satu(kerja, set_, b['pencetus'])
    ev = ev[S8[ev]]
    return ev[c5.topeng(pan, Lr, ev, b['q1'], b['q2'], b['f1'], b['f2'])]


def keluar(kerja):
    """Pilih keluar pada kumpulan A (dua peringkat) -> cs08_keluar.pkl."""
    papan = pickle.load(open(os.path.join(kerja, 'cs08_papan.pkl'), 'rb'))
    pan = cari.panel(kerja, 'A')
    L = lapis.muat(kerja, 'A')
    Lr, XT = (L['L1'], L['L2']), siri_set(kerja, 'A')
    S8 = sah8(pan)
    TBx = {}
    for b in papan:
        ev = _ev_papan(kerja, 'A', pan, Lr, S8, b)
        R, _ = _hasil(pan, XT, ev)
        era = pan['tempoh'][ev]
        TBx[b['id']] = np.stack([(R[era == p] >= TB).mean(axis=0) if (era == p).any() else np.zeros(R.shape[1:])
                                 for p in (0, 1)], axis=-1)                           # [henti, lajur, era]
        cari.log(f"  CS08 keluar A {b['id']}: {len(ev):,} isyarat")
    D = np.mean([(t - t[:, :1]).min(axis=-1) for t in TBx.values()], axis=0)
    skor_ = D.copy()
    skor_[:, 0] = -np.inf
    flat = np.argsort(-skor_, axis=None, kind='stable')[:N_SEJAGAT]
    sej = [(int(f // NKOL), int(f % NKOL)) for f in flat]
    calon = [(s, 0) for s in range(NH)] + sej
    P = {}
    for i, t in TBx.items():
        m = t.min(axis=-1)
        P[i] = max(calon, key=lambda c_: (float(m[c_]), -c_[1]))
    out = {'sejagat': sej, 'D': [float(D[c_]) for c_ in sej], 'pilih': P}
    pickle.dump(out, open(os.path.join(kerja, 'cs08_keluar.pkl'), 'wb'), protocol=4)
    cari.log(f"CS08 keluar: sejagat teratas {HENTI[sej[0][0]]} · {nama_keluar(sej[0][1])} ({D[sej[0]] * 100:+.2f} mata tb)")
    return out


# ---------- kunci (kumpulan B) ----------
def kunci(kerja):
    papan = pickle.load(open(os.path.join(kerja, 'cs08_papan.pkl'), 'rb'))
    KL = pickle.load(open(os.path.join(kerja, 'cs08_keluar.pkl'), 'rb'))
    pan = cari.panel(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr, XT = (L['L1'], L['L2']), siri_set(kerja, 'B')
    S8, V, L8, G = label_v(pan)
    n_tahun = float(np.sum((pan['hari_unik'] >= atom.TEMPOH['B'][0][1]) & (pan['hari_unik'] <= atom.TEMPOH['B'][-1][2])) / 252)
    mxl = int(np.flatnonzero(pan['ticker'] == 'MXL')[0]) if 'MXL' in set(pan['ticker']) else -1
    sah = np.flatnonzero(S8)
    ng = np.maximum(np.bincount(G[sah]), 1)
    unik = sorted({tuple(KL['pilih'][b['id']]) for b in papan})         # asas rawak tb: keluar yang sama pada semua bar layak
    asas_tb = {c_: np.zeros(len(ng)) for c_ in unik}
    for a in range(0, len(sah), 100_000):
        evc = sah[a:a + 100_000]
        Rc = _hasil(pan, XT, evc)[0]
        for c_ in unik:
            asas_tb[c_] += np.bincount(G[evc], (Rc[:, c_[0], c_[1]] >= TB).astype(float), minlength=len(ng))
    asas_tb = {c_: v / ng for c_, v in asas_tb.items()}
    out = {'asas': dict(besar=float(L8[sah, 0].mean()), besar100=float(L8[sah, 1].mean()), n=int(len(sah))), 'setup': {}}
    for b in papan:
        e0 = _ev_papan(kerja, 'B', pan, Lr, S8, b)
        s, kol = KL['pilih'][b['id']]
        R, SK = _hasil(pan, XT, e0)
        r = {}
        for nama, (ss, kk) in (('pilih', (s, kol)), ('x00', (s, 0))):
            Rr, sk = R[:, ss, kk].astype(np.float64), SK[:, ss, kk].astype(np.int64)
            amb = teras.satu_posisi(e0, sk, pan['tid'])
            e, Rr, sk = e0[amb], Rr[amb], sk[amb]
            tp = pan['tempoh'][e]
            d = dict(n=len(e), setahun=len(e) / n_tahun, tahun=int(len(np.unique(pan['tarikh'][e] // 10000))),
                     besar=float(L8[e, 0].mean()), a_besar=float(V[e, 1].mean()), besar100=float(L8[e, 1].mean()),
                     a_besar100=float(L8[e, 3].mean()), tb=float((Rr >= TB).mean()), a_tb=float(asas_tb[(s, kol)][G[e]].mean())
                     if nama == 'pilih' else np.nan, menang=float((Rr > 0).mean()), rugi15=float((Rr <= -0.15).mean()),
                     purata=float(Rr.mean()), median=float(np.median(Rr)), pegang=float(np.median(sk) + 1),
                     jual_awal=float((sk < PEGANG_MIN).mean()), puncak=float(L8[e, 2].mean()),
                     R_besar=float(Rr[L8[e, 0] > 0].mean()) if (L8[e, 0] > 0).any() else np.nan,
                     kl=[float((L8[e[tp == j], 0] - V[e[tp == j], 1]).mean()) if (tp == j).any() else np.nan for j in range(3)],
                     nk=[int((tp == j).sum()) for j in range(3)],
                     tb_semua=float((R[:, ss, kk] >= TB).mean()))
            if nama == 'pilih' and mxl >= 0:                            # kes rujukan (maklumat): termasuk isyarat yang
                ea = t7.ev_satu(kerja, 'B', b['pencetus'])                # tetingkap 126 sesinya belum lengkap
                ea = ea[(pan['tid'][ea] == mxl) & (pan['tarikh'][ea] >= 20260301) & (pan['tarikh'][ea] <= 20260630)]
                ea = ea[c5.topeng(pan, Lr, ea, b['q1'], b['q2'], b['f1'], b['f2'])]
                d['mxl'] = [(int(pan['tarikh'][x]), round(float(pan['o'][x + 1]), 2)) for x in ea]
            r[nama] = d
        ruj = {}                                                       # keluar rujukan (maklumat sahaja), henti 6xATR14
        for kol in RUJUKAN:
            Rr, sk = R[:, 4, kol].astype(np.float64), SK[:, 4, kol].astype(np.int64)
            amb = teras.satu_posisi(e0, sk, pan['tid'])
            e, Rr, sk = e0[amb], Rr[amb], sk[amb]
            bs = L8[e, 0] > 0
            ruj[kol] = dict(n=len(e), tb=float((Rr >= TB).mean()), menang=float((Rr > 0).mean()),
                            rugi15=float((Rr <= -0.15).mean()), purata=float(Rr.mean()), median=float(np.median(Rr)),
                            pegang=float(np.median(sk) + 1), R_besar=float(Rr[bs].mean()) if bs.any() else np.nan,
                            puncak_besar=float(L8[e[bs], 2].mean()) if bs.any() else np.nan)
        r['rujukan'] = ruj
        p_ = r['pilih']
        r['dipercayai'] = bool(p_['n'] >= MIN_BELIAN and p_['tahun'] >= MIN_TAHUN and all(x > 0 for x in p_['kl']))
        out['setup'][b['id']] = r
        cari.log(f"  CS08 kunci {b['id']}: {p_['n']} belian; besar {p_['besar'] * 100:.1f}% (rawak {p_['a_besar'] * 100:.1f}%)")
    pickle.dump(out, open(os.path.join(kerja, 'cs08_kunci.pkl'), 'wb'), protocol=4)
    return out


def lapor_(kerja):
    import cs_lapor as lapor
    papan = pickle.load(open(os.path.join(kerja, 'cs08_papan.pkl'), 'rb'))
    KL = pickle.load(open(os.path.join(kerja, 'cs08_keluar.pkl'), 'rb'))
    K = pickle.load(open(os.path.join(kerja, 'cs08_kunci.pkl'), 'rb'))
    T = pickle.load(open(os.path.join(kerja, 'cs08_jadual.pkl'), 'rb'))
    param = t7.param_semua(kerja)
    p = lambda x, k=1, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    baris = []
    for b in papan:
        r = K['setup'][b['id']]
        a, x = r['pilih'], r['x00']
        s, kol = KL['pilih'][b['id']]
        baris.append(dict(id=b['id'], pencetus=t7.nama7(b['pencetus'], param), prasyarat=c5.buang_kod(c5.tk_pra(b['q1'], b['q2'])).replace(' DAN ', ' + '),
                          penapis=c5.buang_kod(c5.tk_pen(b['f1'], b['f2'])).replace(' DAN ', ' + '), henti=HENTI[s], keluar=nama_keluar(kol),
                          skor_A=b['skor'], dipercayai=r['dipercayai'], kl_K1=a['kl'][0], kl_K2=a['kl'][1], kl_K3=a['kl'][2],
                          n_K3=a['nk'][2], tb_x00=x['tb'], tb_semua=a['tb_semua'], tb_semua_x00=x['tb_semua'],
                          purata_x00=x['purata'], mxl='; '.join(f'{t} @ {h}' for t, h in a.get('mxl', [])),
                          **{k_: v for k_, v in a.items() if k_ not in ('kl', 'nk', 'mxl', 'tb_semua')}))
    D = pd.DataFrame(baris)
    d_ = os.path.join(SINI, 'hasil', 'CS08')
    os.makedirs(d_, exist_ok=True)
    D.to_csv(os.path.join(d_, 'papan.csv'), index=False, float_format='%.5f')
    n_dp = int(D.dipercayai.sum())
    kel_ok = int((D.tb_semua > D.tb_semua_x00).sum())
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    bil = {b_: len(pickle.load(open(os.path.join(kerja, f'cs08_skor_{b_}.pkl'), 'rb')))
           for b_ in BAHAGIAN if os.path.exists(os.path.join(kerja, f'cs08_skor_{b_}.pkl'))}
    A = ['# CS08: lorong KEDUA — beli selepas pengesahan uptrend, pegang sampai trend tamat (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_trend8.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (q), dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.** Lorong ini BERASINGAN daripada swing 4 minggu (keluarga F); ID '
         '`T..` bukan kod F.', '',
         '## 1. Apa yang dicari', '',
         '- Permintaan pengguna (kes MXL): tunggu pengesahan uptrend besar, beli di tengah, pegang sampai trend tamat.',
         f'- **Pelari besar** = selepas beli, tutup mencapai ≥ +{NAIK:.0%} dalam {H_MAX} sesi (≈ 6 bulan) SEBELUM mana-mana tutup '
         f'≤ −{JATUH:.0%}. Saham rawak (mana-mana hari, kumpulan B): **{p(K["asas"]["besar"])} %** jadi pelari besar; '
         f'{p(K["asas"]["besar100"])} % capai +100 %.',
         f"- Dicari pada kumpulan A: {sum(bil.values()):,} pencetus ({', '.join(f'{v:,} {k_}' for k_, v in bil.items())}) × 544 "
         f'gabungan prasyarat × 379 gabungan penapis; {len(T):,} cukup isyarat, {int((T.skor > 0).sum()):,} dengan skor > 0.',
         f'- Keluar: {NA} indikator trend tamat × 3 syarat aktif × {NH} henti; ukuran = dijual dengan untung ≥ +{TB:.0%}. Pegang '
         'minimum 3 sesi; tiada jual hari beli; henti rugi wajib.', '',
         '## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)', '',
         f"- Setup papan Dipercayai-T (belian ≥ {MIN_BELIAN}, ≥ {MIN_TAHUN} tahun aktif, mengatasi rawak dalam K1, K2 DAN K3): "
         f"**{n_dp} daripada {len(D)}** → lorong trend **{'ADA kelebihan' if n_dp >= len(D) / 2 else 'TIADA kelebihan yang boleh dipercayai'}** "
         'mengikut bacaan yang dikunci.',
         f"- Keluar terpilih mengatasi pegang sahaja (henti sama) pada B: **{kel_ok} daripada {len(D)}** → keluar "
         f"**{'MENOLONG' if kel_ok > len(D) / 2 else 'TIDAK menolong'}**.",
         f"- Median papan: pelari besar {p(D.besar.median())} % (rawak hari sama {p(D.a_besar.median())} %); dijual ≥ +30 % "
         f"{p(D.tb.median())} %; menang {p(D.menang.median(), 0)} %; rugi ≥ 15 % {p(D.rugi15.median(), 0)} %; purata "
         f"{p(D.purata.median(), 1, True)} %; pegang median {D.pegang.median():.0f} sesi.", '',
         f'## 3. Papan lorong trend ({len(D)} setup)', '',
         '| ID | Prasyarat | Pencetus (parameter) | Penapis saham | Henti · keluar | Belian (setahun) | **Pelari besar %** (rawak) | '
         'Capai +100 % % (rawak) | Dijual ≥ +30 % % (rawak) | Menang % | Rugi ≥ 15 % % | Purata % | Pegang (sesi) | '
         'Kelebihan K1 / K2 / K3 | Dipercayai-T |', '|---' * 15 + '|']
    for r in D.itertuples():
        A.append(f"| `{r.id}` | {r.prasyarat or 'tiada'} | {r.pencetus} | {r.penapis or 'tiada'} | {r.henti} · {r.keluar} | "
                 f"{r.n:,} ({r.setahun:.0f}) | **{p(r.besar)}** ({p(r.a_besar)}) | {p(r.besar100)} ({p(r.a_besar100)}) | "
                 f"{p(r.tb)} ({p(r.a_tb)}) | {p(r.menang, 0)} | {p(r.rugi15, 0)} | {p(r.purata, 1, True)} | {r.pegang:.0f} | "
                 f"{p(r.kl_K1, 1, True)} / {p(r.kl_K2, 1, True)} / {p(r.kl_K3, 1, True)} | {'**ya**' if r.dipercayai else 'tidak'} |")
    A += ['', '## 4. Keluar "trend tamat" sejagat (dipilih pada A)', '',
          '| # | Henti | Keluar | A: tambahan "dijual ≥ +30 %" atas pegang sahaja (mata) |', '|---|---|---|---|']
    for j, ((s, kol), d) in enumerate(zip(KL['sejagat'], KL['D']), 1):
        A.append(f'| {j} | {HENTI[s]} | {nama_keluar(kol)} | {d * 100:+.2f} |')
    A += ['', '## 4a. "Pegang sampai trend tamat": keluar rujukan (maklumat; purata 12 setup papan, kumpulan B, henti 6xATR14)', '',
          '| Keluar | Dijual ≥ +30 % % | Menang % | Rugi ≥ 15 % % | Purata % | Median % | Pegang median (sesi) | Pada pelari besar: untung dapat / '
          'puncak % |', '|---' * 8 + '|']
    for kol in RUJUKAN:
        v = pd.DataFrame([K['setup'][b['id']]['rujukan'][kol] for b in papan]).mean()
        A.append(f"| {nama_keluar(kol)} | {p(v.tb)} | {p(v.menang, 0)} | {p(v.rugi15, 0)} | {p(v.purata, 1, True)} | "
                 f"{p(v['median'], 1, True)} | {v.pegang:.0f} | {p(v.R_besar, 0, True)} / {p(v.puncak_besar, 0, True)} |")
    ada = D[D.mxl.fillna('') != '']
    A += ['', '## 5. Kes rujukan pengguna: MXL (Mac–Jun 2026)', '',
          ('MXL berada dalam kumpulan B. Isyarat setup papan pada MXL (tarikh isyarat @ harga beli): ' + '; '.join(
              f"`{r.id}`: {r.mxl}" for r in ada.itertuples()) + '.') if len(ada) else
          'Tiada setup papan memberi isyarat pada MXL antara Mac dan Jun 2026 (atau MXL tiada dalam kumpulan B).',
          'Isyarat selepas pertengahan April 2026 tidak masuk statistik (tetingkap 126 sesi belum lengkap) tetapi ditunjukkan di sini.',
          'Satu kes bukan bukti; ia hanya menunjukkan sama ada setup terbaik akan menangkap contoh yang pengguna ingat.', '',
          '## 6. Kaveat', '',
          '- Tiada saham delist: bagi pegang 6 bulan, bias ini LEBIH besar daripada lorong swing (saham yang gagal hilang).',
          '- K3 pendek: tetingkap 126 sesi bermakna isyarat selepas ~April 2026 tidak dikira.',
          '- Kumpulan B sudah dilihat untuk label lain; skor A melambung kerana banyak calon. Backtest sahaja; kad skor kekal '
          'satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'LAPORAN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f'CS08 lapor: {n_dp}/{len(D)} dipercayai-T; keluar menolong {kel_ok}/{len(D)}')
    return D


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    t0 = time.time()
    if cmd == 'skor':
        for bhg in (sys.argv[3:] or BAHAGIAN):
            skor(kerja, bhg)
    elif cmd == 'pilih':
        pilih(kerja)
    elif cmd == 'benihB':
        benih_b(kerja)
    elif cmd == 'keluar':
        keluar(kerja)
    elif cmd == 'kunci':
        kunci(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
    cari.log(f'{cmd} siap · {time.time() - t0:.0f}s')
