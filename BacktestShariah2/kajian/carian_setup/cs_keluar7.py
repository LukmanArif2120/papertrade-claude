"""Carian setup — pusingan CS07 bahagian (b): cari dan tala KELUAR (SPEC pindaan 14 Nov 2026 (n)).

Atom keluar berparameter (97), peraturan X00 / tunggal / pasangan ATAU / DAN, setiap satu dengan syarat aktif {sentiasa,
selepas tutup tertinggi >= +5 %, selepas >= +10 %}, dan 8 henti. Kernel sendiri: enjin lama (cs_teras) tidak disentuh.
Mekanik sama seperti cs_teras: isyarat pada tutup -> beli buka esok; atom dinilai pada tutup sesi d -> jual buka sesi d + 1;
henti intrahari; had 20 sesi; kos 0.5 %.
Guna: python3 cs_keluar7.py atom|cari|pilih|kunci|lapor <kerja>. Jangan sunting keluaran secara manual."""
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
import cs_param as kp  # noqa: E402
import cs_teras as teras  # noqa: E402

TMAX, KOS = teras.TMAX, teras.KOS
HENTI = ['-8%', '-10%', '-12%', '-15%', '3xATR14', '4xATR14', '5xATR14', 'min(-10%, 4xATR14)']
NH = len(HENTI)
AKTIF = ['sentiasa', 'selepas +5%', 'selepas +10%']
NG = len(AKTIF)
N_SEJAGAT, SIMPAN_MIN = 30, 0.90                       # 30 keluar sejagat; syarat "tidak jual awal" (dikunci pindaan (n))
PEGANG_MIN = atom.PEGANG_MIN                           # pindaan (p): indikator keluar hanya menjual mulai buka sesi ke-4
STAT = ('n', 'tp', 'jadi', 'rugi8', 'menang', 'R', 'n_terus', 'R_terus', 'kurang')
NST = len(STAT)
_k = lambda x: x


def atom_keluar():
    """Senarai (kod, jenis, parameter, teks). jenis 0 = siri setiap bar; 1 = Chandelier k x ATR14 dari tutup tertinggi sejak
    beli; 2 = ekor p x tutup tertinggi; 3 = tiada kemajuan (selepas d sesi, tutup < harga beli)."""
    A = []
    add = lambda fam, jenis, teks, **p: A.append((fam, jenis, p, teks))
    for n in (5, 8, 10, 15, 20, 30, 50):
        add('Y01', 0, f'tutup < MA{n}', n=n)
    for n in (5, 8, 10, 15, 20, 30):
        add('Y02', 0, f'tutup < EMA{n}', n=n)
    for n in (5, 10, 20):
        add('Y03', 0, f'dua tutup berturut < MA{n}', n=n)
    for f, s in ((5, 10), (5, 20), (10, 20), (10, 30)):
        add('Y04', 0, f'MA{f} < MA{s}', f=f, s=s)
    for f, s, g in ((12, 26, 9), (8, 17, 9), (5, 35, 5), (6, 19, 6)):
        add('Y05', 0, f'MACD({f},{s},{g}) < isyarat', f=f, s=s, g=g)
    for k in (2, 3, 4):
        add('Y06', 0, f'histogram MACD turun {k} hari', k=k)
    for n, x in ((14, 40), (14, 45), (14, 50), (14, 55), (7, 40), (7, 50), (5, 40), (5, 50)):
        add('Y07', 0, f'RSI{n} < {x}', n=n, x=x)
    for n in (7, 14):
        for x in (60, 65, 70, 75, 80):
            add('Y08', 0, f'RSI{n} silang turun bawah {x}', n=n, x=x)
    for n, x in ((14, 75), (14, 80), (14, 85), (7, 85), (7, 90), (2, 95), (2, 98)):
        add('Y09', 0, f'RSI{n} > {x}', n=n, x=x)
    for n, m in ((10, 2.0), (10, 3.0), (10, 4.0), (14, 3.0), (7, 2.0)):
        add('Y10', 0, f'Supertrend({n}, {m}) turun', n=n, m=m)
    for k in (2, 3, 4, 5, 7, 10):
        add('Y11', 0, f'tutup < rendah {k} hari', k=k)
    for n in (9, 14):
        for x in (70, 80, 90):
            add('Y12', 0, f'Stochastic({n}) silang turun di atas {x}', n=n, x=x)
    for v in (1.5, 2.0, 3.0):
        add('Y13', 0, f'hari turun dengan volum >= {v}x', v=v)
    add('Y14', 0, 'tutup < buka dan < rendah semalam', k=1)
    for k in (2, 3, 4):
        add('Y14', 0, f'{k} tutup menurun berturut', k=k)
    for n in (7, 14):
        add('Y15', 0, f'+DI{n} < -DI{n}', n=n)
    for k in (1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0):
        add('Y17', 1, f'Chandelier {k}xATR14 dari tutup tertinggi', k=k)
    for p in (0.85, 0.88, 0.90, 0.92, 0.94, 0.95, 0.96, 0.97):
        add('Y18', 2, f'tutup < {p:.0%} tutup tertinggi sejak beli', k=p)
    for d in (3, 5, 8, 10):
        add('Y19', 3, f'tiada kemajuan (selepas {d} sesi, tutup < harga beli)', k=d)
    bil, out = {}, []
    for fam, jenis, p, teks in A:
        bil[fam] = bil.get(fam, 0) + 1
        out.append((f'{fam}.{bil[fam]}', jenis, p, teks))
    return out


ATOM = atom_keluar()
NA = len(ATOM)
JENIS = np.asarray([a[1] for a in ATOM], np.int64)
PAR = np.asarray([float(a[2].get('k', 0)) if a[1] else 0.0 for a in ATOM])
BARIS = np.cumsum(JENIS == 0) - 1                       # baris matriks siri bagi atom jenis 0
A1, A2, OP = teras.peraturan_keluar(NA)                 # X00, tunggal, ATAU, DAN
NR = len(A1)
NKOL = NR * NG                                          # lajur = peraturan * NG + aktif


def nama_peraturan(kol):
    r, g = divmod(int(kol), NG)
    if OP[r] == 0:
        return 'X00 tiada keluar indikator (henti + 20 sesi)'
    t = ATOM[A1[r]][3] if OP[r] == 1 else f"{ATOM[A1[r]][3]} {'ATAU' if OP[r] == 2 else 'DAN'} {ATOM[A2[r]][3]}"
    return t if g == 0 else f'{t} [aktif {AKTIF[g]}]'


def kod_peraturan(kol):
    r, g = divmod(int(kol), NG)
    if OP[r] == 0:
        return 'X00'
    t = ATOM[A1[r]][0] if OP[r] == 1 else f"{ATOM[A1[r]][0]} {'ATAU' if OP[r] == 2 else 'DAN'} {ATOM[A2[r]][0]}"
    return t + ('' if g == 0 else f'@{(5, 10)[g - 1]}')


# ---------- siri atom jenis 0 ----------
def siri(g):
    """Matriks boolean [atom jenis 0, bar] bagi satu saham."""
    I = kp.Ind(g, None)
    c, o, l = I.c, I.o, I.l
    out = []
    for kod, jenis, p, _ in ATOM:
        if jenis:
            continue
        f = kod[:3]
        if f == 'Y01':
            s = c < I.sma(p['n'])
        elif f == 'Y02':
            s = c < I.ema(p['n'])
        elif f == 'Y03':
            x = c < I.sma(p['n'])
            s = x & atom._dulu(x)
        elif f == 'Y04':
            s = I.sma(p['f']) < I.sma(p['s'])
        elif f == 'Y05':
            m = I.ema(p['f']) - I.ema(p['s'])
            s = m < m.ewm(span=p['g'], adjust=False).mean()
        elif f == 'Y06':
            m = I.ema(12) - I.ema(26)
            hs = m - m.ewm(span=9, adjust=False).mean()
            t = hs < hs.shift(1)
            s = t
            for i in range(1, p['k']):
                s = s & atom._dulu(t, i)
        elif f == 'Y07':
            s = I.rsi(p['n']) < p['x']
        elif f == 'Y08':
            r = I.rsi(p['n'])
            s = (r < p['x']) & (r.shift(1) >= p['x'])
        elif f == 'Y09':
            s = I.rsi(p['n']) > p['x']
        elif f == 'Y10':
            s = I.st(p['n'], p['m']) < 0
        elif f == 'Y11':
            s = c < I.ll(p['k'])
        elif f == 'Y12':
            sk, sdd = I.stoch(p['n'])
            s = (sk < sdd) & (sk.shift() >= sdd.shift()) & (sk.shift() > p['x'])
        elif f == 'Y13':
            s = (c < I.pc) & (I.vr >= p['v'])
        elif f == 'Y14':
            if p['k'] == 1:
                s = (c < o) & (c < l.shift(1))
            else:
                s = c < c.shift(1)
                for i in range(1, p['k'] - 1):
                    s = s & (c.shift(i) < c.shift(i + 1))
        elif f == 'Y15':
            _, pdi, ndi = I.adx(p['n'])
            s = pdi < ndi
        else:
            raise ValueError(kod)
        out.append(np.asarray(s.fillna(False) if s.dtype != bool else s, dtype=bool))
    return np.stack(out)


_W = {}


def _siri_satu(julat):
    a, b = julat
    return np.concatenate([siri(_W['fr'][t]) for t in _W['tick'][a:b]], axis=1).astype(np.uint8)


def siri_set(kerja, set_):
    """Matriks uint8 [atom jenis 0, bar panel] bagi set A/B (cs07_XA_<set>.npy)."""
    f = os.path.join(kerja, f'cs07_XA_{set_}.npy')
    if os.path.exists(f):
        return np.load(f, mmap_mode='r')
    pan = cari.panel(kerja, set_)
    fr, _, _ = cari.muat_set(set_)
    tick = sorted(fr)
    assert list(pan['ticker']) == tick
    _W.update(fr=fr, tick=tick)
    julat = [(a, min(a + 25, len(tick))) for a in range(0, len(tick), 25)]
    t0 = time.time()
    with mp.get_context('fork').Pool(cari.PEKERJA) as pool:
        XA = np.concatenate(list(pool.imap(_siri_satu, julat)), axis=1)
    assert XA.shape == (int((JENIS == 0).sum()), len(pan['c']))
    np.save(f, XA)
    cari.log(f'siri atom keluar {set_}: {XA.shape}, {time.time() - t0:.0f}s')
    return XA


# ---------- kernel ----------
@njit(cache=True)
def _ctz(x):
    n = 0
    while (x & 1) == 0:
        x >>= 1
        n += 1
    return n


@njit(cache=True)
def _aras_henti(P, a, L):
    L[0], L[1], L[2], L[3] = P * 0.92, P * 0.90, P * 0.88, P * 0.85
    L[4], L[5], L[6] = P - 3.0 * a, P - 4.0 * a, P - 5.0 * a
    L[7] = min(L[1], L[5])


@njit(parallel=True, cache=True)
def sedia(ev, o, h, l, c, atr, XA, jenis, par, baris, pegang_min, px):
    """Bagi setiap isyarat: topeng atom M (bit d = benar pada tutup sesi d), topeng aktif ARM, keadaan henti (DS, PS, H0),
    buka setiap sesi / P (OPN), tutup sesi 20 / P (CF) dan label [m5, terus, puncak]. pegang_min: bit atom hanya dipasang
    bagi d >= pegang_min - 1, iaitu indikator menjual paling awal pada buka indeks sesi pegang_min (1 = tiada had).
    px[k] > 0: harga beli khas pada bar beli (cth. pecah tinggi intrahari, pindaan (ac)); 0 = buka bar beli."""
    n, nA = ev.shape[0], jenis.shape[0]
    M = np.zeros((n, nA), np.int32)
    ARM = np.zeros((n, 2), np.int32)
    DS = np.full((n, NH), 99, np.int64)
    PS = np.zeros((n, NH))
    H0 = np.zeros((n, NH), np.bool_)
    OPN = np.zeros((n, TMAX))
    CF = np.zeros(n)
    LAB = np.zeros((n, 3))
    for k in prange(n):
        i = ev[k]
        e = i + 1
        P = px[k] if px[k] > 0 else o[e]
        L = np.zeros(NH)
        _aras_henti(P, atr[i], L)
        hc = c[e]
        for d in range(TMAX - 1):
            b = e + d
            if c[b] > hc:
                hc = c[b]
            if hc >= P * 1.05:
                ARM[k, 0] |= (1 << d)
            if hc >= P * 1.10:
                ARM[k, 1] |= (1 << d)
            for a in range(nA):
                j = jenis[a]
                if j == 0:
                    ya = XA[baris[a], b] != 0
                elif j == 1:
                    ya = c[b] < hc - par[a] * atr[b]
                elif j == 2:
                    ya = c[b] < par[a] * hc
                else:
                    ya = (d + 1 >= par[a]) and (c[b] < P)
                if ya and d >= pegang_min - 1:
                    M[k, a] |= (1 << d)
        mx = c[e]
        h8 = c[e] <= P * 0.92
        for d in range(1, TMAX):
            b = e + d
            OPN[k, d] = o[b] / P
            if c[b] > mx:
                mx = c[b]
            if o[b] <= P * 0.92 or l[b] <= P * 0.92:
                h8 = True
        for s in range(NH):
            H0[k, s] = c[e] <= L[s]
            for d in range(1, TMAX):
                b = e + d
                if o[b] <= L[s]:
                    DS[k, s] = d
                    PS[k, s] = o[b] / P
                    break
                if l[b] <= L[s]:
                    DS[k, s] = d
                    PS[k, s] = L[s] / P
                    break
        CF[k] = c[e + TMAX - 1] / P
        LAB[k, 0] = c[e + 4] >= P * 1.05
        LAB[k, 1] = (c[e + 4] >= P * 1.05) and (c[e + TMAX - 1] > c[e + 4]) and (not h8)
        LAB[k, 2] = mx / P - 1.0
    return M, ARM, DS, PS, H0, OPN, CF, LAB


@njit(cache=True)
def _topeng(Mk, ARMk, a1, a2, op, r, g):
    if op[r] == 0:
        return 0
    if op[r] == 1:
        mr = Mk[a1[r]]
    elif op[r] == 2:
        mr = Mk[a1[r]] | Mk[a2[r]]
    else:
        mr = Mk[a1[r]] & Mk[a2[r]]
    if g > 0:
        mr &= ARMk[g - 1]
    return mr


@njit(cache=True)
def _R(mr, s, k, DS, PS, H0, OPN, CF):
    """(R bersih, sesi keluar). Sama seperti cs_teras._hasil."""
    if H0[k, s]:
        mr |= 1
    if mr != 0:
        dx = _ctz(mr) + 1
        if dx <= DS[k, s]:
            return OPN[k, dx] - 1.0 - KOS, dx
    if DS[k, s] != 99:
        return PS[k, s] - 1.0 - KOS, DS[k, s]
    return CF[k] - 1.0 - KOS, TMAX - 1


@njit(parallel=True, cache=True)
def kumpul(M, ARM, DS, PS, H0, OPN, CF, LAB, era, n_era, a1, a2, op):
    """Acc[henti, lajur, era, statistik] atas semua isyarat; lajur = peraturan * NG + aktif."""
    n, nR = M.shape[0], a1.shape[0]
    Acc = np.zeros((NH, nR * NG, n_era, NST), np.float32)
    for r in prange(nR):
        for g in range(NG):
            loc = np.zeros((NH, n_era, NST))
            for k in range(n):
                mr = _topeng(M[k], ARM[k], a1, a2, op, r, g)
                p = era[k]
                for s in range(NH):
                    R, _ = _R(mr, s, k, DS, PS, H0, OPN, CF)
                    x = loc[s, p]
                    x[0] += 1.0
                    if R >= 0.10:
                        x[2] += 1.0
                        if LAB[k, 0] > 0:
                            x[1] += 1.0
                    if R <= -0.08:
                        x[3] += 1.0
                    if R > 0:
                        x[4] += 1.0
                    x[5] += R
                    if LAB[k, 1] > 0:
                        x[6] += 1.0
                        x[7] += R
                    x[8] += LAB[k, 2] - R
            for s in range(NH):
                for p in range(n_era):
                    for j in range(NST):
                        Acc[s, r * NG + g, p, j] = loc[s, p, j]
    return Acc


@njit(parallel=True, cache=True)
def hasil(M, ARM, DS, PS, H0, OPN, CF, a1, a2, op, s, kol):
    """(R, sesi keluar) setiap isyarat bagi satu (henti s, lajur kol)."""
    n = M.shape[0]
    R = np.empty(n)
    sk = np.empty(n, np.int64)
    r, g = kol // NG, kol % NG
    for k in prange(n):
        R[k], sk[k] = _R(_topeng(M[k], ARM[k], a1, a2, op, r, g), s, k, DS, PS, H0, OPN, CF)
    return R, sk


def sedia_pan(pan, XA, ev, pegang_min=None, px=None):
    return sedia(np.ascontiguousarray(ev, dtype=np.int64), pan['o'], pan['h'], pan['l'], pan['c'], pan['atr'],
                 XA, JENIS, PAR, BARIS, PEGANG_MIN if pegang_min is None else pegang_min,
                 np.zeros(len(ev)) if px is None else np.ascontiguousarray(px, dtype=np.float64))


# ---------- setup yang dinilai ----------
def senarai_setup(kerja, set_):
    """Senarai dict {id, ev (semua isyarat masuk pada set), lajur_lama} bagi 61 setup kedudukan akhir (m) dan, jika ada,
    setup papan baharu CS07 (cs07_papan.pkl daripada cs_tala7)."""
    import cs_cs05 as c5
    import cs_lapis as lapis
    import cs_lapor as lapor
    import cs_portfolio6 as p6
    pan = cari.panel(kerja, set_)
    EV = cari.pencetus(pan, pickle.load(open(os.path.join(kerja, f'benih_{set_}.pkl'), 'rb')))
    L = lapis.muat(kerja, set_)
    Lr = (L['L1'], L['L2'])
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    ids = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv')).id.tolist()
    out = []
    for i in ids:
        d = p6.dari_takrif5(reg.loc[i, 'takrif'])
        ev = EV[d['pencetus']]
        out.append({'id': i, 'ev': ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])], 'lajur_lama': d['lajur']})
    f = os.path.join(kerja, 'cs07_papan.pkl')
    if os.path.exists(f):
        import cs_tala7 as t7
        for b in pickle.load(open(f, 'rb')):
            ev = t7.ev_satu(kerja, set_, b['pencetus'])
            out.append({'id': b['id'], 'ev': ev[c5.topeng(pan, Lr, ev, b['q1'], b['q2'], b['f1'], b['f2'])],
                        'lajur_lama': None})
    return pan, out


def cari_(kerja):
    """Peringkat cari: Acc setiap setup pada kumpulan A (semua isyarat) -> kerja/cs07_keluar/<id>_A.npy."""
    d = os.path.join(kerja, 'cs07_keluar')
    os.makedirs(d, exist_ok=True)
    pan, S = senarai_setup(kerja, 'A')
    XA = siri_set(kerja, 'A')
    t0 = time.time()
    for k, s in enumerate(S, 1):
        f = os.path.join(d, f"{s['id']}_A.npy")
        if os.path.exists(f):
            continue
        ev = s['ev']
        Acc = kumpul(*sedia_pan(pan, XA, ev), pan['tempoh'][ev].astype(np.int64), 2, A1, A2, OP)
        np.save(f, Acc)
        cari.log(f"  keluar A {k}/{len(S)} {s['id']}: {len(ev):,} isyarat · {time.time() - t0:.0f}s")


def _kadar(Acc):
    """tp[s, kol, era], kelebihan tp atas X00 henti sama (min era), nisbah simpan (R pada `terus` lawan X00), rugi8, n."""
    n = np.maximum(Acc[..., 0], 1)
    tp = Acc[..., 1] / n
    d = (tp - tp[:, :1]).min(axis=-1)
    rt = Acc[..., 7].sum(-1)
    simpan = rt / np.where(rt[:, :1] > 0, rt[:, :1], np.nan)
    return tp, d, simpan, Acc[..., 3].sum(-1) / n.sum(-1), rt


def pilih(kerja):
    """Peringkat pilih (kumpulan A sahaja): 30 keluar sejagat, kemudian pilihan setiap setup. -> cs07_keluar_pilih.pkl"""
    d = os.path.join(kerja, 'cs07_keluar')
    ids = sorted(f[:-6] for f in os.listdir(d) if f.endswith('_A.npy'))
    D = np.zeros((NH, NKOL))
    RT = np.zeros((NH, NKOL))
    for i in ids:
        tp, dd, _, _, rt = _kadar(np.load(os.path.join(d, f'{i}_A.npy')))
        D += dd
        RT += rt
    D /= len(ids)
    simpan_s = RT / np.where(RT[:, :1] > 0, RT[:, :1], np.nan)
    lulus = simpan_s >= SIMPAN_MIN
    skor = np.where(lulus, D, -np.inf)
    skor[:, :NG] = -np.inf                                        # X00 (dan salinan aktifnya) bukan calon sejagat
    flat = np.argsort(-skor, axis=None, kind='stable')[:N_SEJAGAT]
    sej = [(int(f // NKOL), int(f % NKOL)) for f in flat]
    calon = [(s, 0) for s in range(NH)] + sej
    P = {}
    for i in ids:
        tp, dd, simpan, rugi, _ = _kadar(np.load(os.path.join(d, f'{i}_A.npy')))
        terbaik, kunci_t = None, None
        for s, kol in calon:
            if kol and not (simpan[s, kol] >= SIMPAN_MIN):
                continue
            k_ = (float(tp[s, kol].min()), -float(rugi[s, kol]))
            if kunci_t is None or k_ > kunci_t:
                terbaik, kunci_t = (s, kol), k_
        bebas = np.unravel_index(np.argmax(np.where(simpan >= SIMPAN_MIN, tp.min(-1), -np.inf)), (NH, NKOL))
        P[i] = {'pilih': terbaik, 'tp_A': kunci_t[0], 'tp_X00_A': float(tp[terbaik[0], 0].min()),
                'simpan_A': float(simpan[terbaik]), 'bebas': (int(bebas[0]), int(bebas[1])),
                'tp_bebas_A': float(tp[bebas].min())}
    out = {'sejagat': sej, 'D': [float(D[s, k]) for s, k in sej], 'simpan': [float(simpan_s[s, k]) for s, k in sej],
           'n_lulus': int(lulus.sum()), 'n_setup': len(ids), 'setup': P,
           'D_tanpa_syarat': float(np.max(np.where(np.arange(NKOL)[None, :] >= NG, D, -np.inf)))}
    pickle.dump(out, open(os.path.join(kerja, 'cs07_keluar_pilih.pkl'), 'wb'), protocol=4)
    cari.log(f"pilih keluar: {len(ids)} setup; {out['n_lulus']:,} daripada {NH * NKOL:,} calon lulus syarat simpan; "
             f"sejagat teratas {HENTI[sej[0][0]]} · {nama_peraturan(sej[0][1])} (+{out['D'][0] * 100:.2f} mata tp)")
    return out


def _ukur(pan, ev, R, sk, LAB):
    """Statistik satu keluar pada satu set isyarat: semua isyarat dan satu posisi setiap saham, setiap tempoh + semua."""
    out = {}
    amb = teras.satu_posisi(ev, sk, pan['tid'])
    for nama, m in (('semua', np.ones(len(ev), bool)), ('satu', amb)):
        tpd = pan['tempoh'][ev]
        for p in list(range(int(pan['tempoh'].max()) + 1)) + [-1]:
            q = m & ((tpd == p) if p >= 0 else True)
            r, lab = R[q], LAB[q]
            t = lab[:, 1] > 0
            out[(nama, p)] = dict(n=int(q.sum()), tp=float(((lab[:, 0] > 0) & (r >= 0.10)).mean()) if q.any() else np.nan,
                                  jadi=float((r >= 0.10).mean()) if q.any() else np.nan,
                                  menang=float((r > 0).mean()) if q.any() else np.nan,
                                  rugi8=float((r <= -0.08).mean()) if q.any() else np.nan,
                                  purata=float(r.mean()) if q.any() else np.nan,
                                  R_terus=float(r[t].mean()) if t.any() else np.nan, n_terus=int(t.sum()),
                                  kurang=float((lab[:, 2] - r).mean()) if q.any() else np.nan,
                                  pegang=float(sk[q].mean() + 1) if q.any() else np.nan)
    return out


def kunci(kerja):
    """Peringkat semak pada kumpulan B: keluar terpilih, X00 henti sama, keluar lama, sejagat #1. -> cs07_keluar_kunci.pkl"""
    import cs_pegang as pg
    S0 = pickle.load(open(os.path.join(kerja, 'cs07_keluar_pilih.pkl'), 'rb'))
    pan, S = senarai_setup(kerja, 'B')
    XA = siri_set(kerja, 'B')
    out, t0 = {}, time.time()
    sj = S0['sejagat']
    if os.environ.get('CS07_UJI'):                                  # uji kering laluan kod sahaja
        S = S[:int(os.environ['CS07_UJI'])] + S[-2:]
    for s_ in S:
        i, ev = s_['id'], s_['ev']
        if i not in S0['setup'] or len(ev) < 30:
            continue
        st = sedia_pan(pan, XA, ev)
        M, ARM, DS, PS, H0, OPN, CF, LAB = st
        h = lambda s, kol: hasil(M, ARM, DS, PS, H0, OPN, CF, A1, A2, OP, s, kol)
        s, kol = S0['setup'][i]['pilih']
        r = {'pilih': _ukur(pan, ev, *h(s, kol), LAB), 'x00': _ukur(pan, ev, *h(s, 0), LAB),
             'sejagat1': _ukur(pan, ev, *h(*sj[0]), LAB), 'x00_sejagat1': _ukur(pan, ev, *h(sj[0][0], 0), LAB)}
        if s_['lajur_lama'] is not None:                              # keluar lama di bawah pegang minimum yang sama (pindaan (p))
            r['lama'] = _ukur(pan, ev, *h(*pg.lama_ke_baharu(s_['lajur_lama'])), LAB)
        r['sejagat'] = [(_ukur(pan, ev, *h(a, b), LAB)[('semua', -1)], _ukur(pan, ev, *h(a, 0), LAB)[('semua', -1)])
                        for a, b in sj]
        out[i] = r
    pickle.dump(out, open(os.path.join(kerja, 'cs07_keluar_kunci.pkl'), 'wb'), protocol=4)
    cari.log(f'kunci keluar: {len(out)} setup · {time.time() - t0:.0f}s')
    return out


def lapor_(kerja):
    """hasil/CS07/KELUAR.md dan keluar.csv daripada cs07_keluar_pilih.pkl + cs07_keluar_kunci.pkl."""
    import cs_cs05 as c5
    import cs_lapor as lapor
    S0 = pickle.load(open(os.path.join(kerja, 'cs07_keluar_pilih.pkl'), 'rb'))
    K = pickle.load(open(os.path.join(kerja, 'cs07_keluar_kunci.pkl'), 'rb'))
    d_ = os.path.join(SINI, 'hasil', 'CS07')
    os.makedirs(d_, exist_ok=True)
    p = lambda x, k=1, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    baris = []
    for i, r in K.items():
        s, kol = S0['setup'][i]['pilih']
        a, x, b1 = r['pilih'], r['x00'], r['pilih'][('satu', -1)]
        la = r.get('lama')
        g = lambda m, k: m[('semua', -1)][k]
        baris.append(dict(
            id=i, henti=HENTI[s], keluar=kod_peraturan(kol), keluar_teks=nama_peraturan(kol), sejagat=bool(kol >= NG),
            n=g(a, 'n'), tp_pilih=g(a, 'tp'), tp_x00=g(x, 'tp'), tp_lama=g(la, 'tp') if la else np.nan,
            simpan=g(a, 'R_terus') / g(x, 'R_terus') if g(x, 'R_terus') > 0 else np.nan,
            rugi8_pilih=g(a, 'rugi8'), rugi8_x00=g(x, 'rugi8'), rugi8_lama=g(la, 'rugi8') if la else np.nan,
            menang_pilih=g(a, 'menang'), menang_lama=g(la, 'menang') if la else np.nan,
            purata_pilih=g(a, 'purata'), purata_x00=g(x, 'purata'), purata_lama=g(la, 'purata') if la else np.nan,
            kurang_pilih=g(a, 'kurang'), kurang_x00=g(x, 'kurang'), kurang_lama=g(la, 'kurang') if la else np.nan,
            pegang_pilih=g(a, 'pegang'), pegang_lama=g(la, 'pegang') if la else np.nan,
            tp_K3_pilih=a[('semua', 2)]['tp'], tp_K3_x00=x[('semua', 2)]['tp'],
            tp_K3_lama=la[('semua', 2)]['tp'] if la else np.nan,
            satu_n=b1['n'], satu_tp=b1['tp'], satu_menang=b1['menang'], satu_rugi8=b1['rugi8'], satu_purata=b1['purata'],
            satu_tp_lama=la[('satu', -1)]['tp'] if la else np.nan, tp_A=S0['setup'][i]['tp_A'],
            tp_X00_A=S0['setup'][i]['tp_X00_A']))
    T = pd.DataFrame(baris)
    T.to_csv(os.path.join(d_, 'keluar.csv'), index=False, float_format='%.5f')
    L = T[T.tp_lama.notna()]
    menolong = L[(L.tp_pilih > L.tp_x00) & (L.tp_pilih > L.tp_lama)]
    atas_x00, atas_lama = int((T.tp_pilih > T.tp_x00).sum()), int((L.tp_pilih > L.tp_lama).sum())
    simpan_ok = int((T.simpan >= SIMPAN_MIN).sum())
    d_rugi = float((L.rugi8_pilih - L.rugi8_lama).median())
    ya = (len(menolong) > len(L) / 2) and (T.simpan.median() >= SIMPAN_MIN) and (d_rugi <= 0.01)
    # keluar sejagat pada B: purata merentas setup bagi (tp - tp X00 henti sama), semua isyarat
    sj = []
    for j, (s, kol) in enumerate(S0['sejagat']):
        dl = [r['sejagat'][j][0]['tp'] - r['sejagat'][j][1]['tp'] for r in K.values()]
        rt = sum(r['sejagat'][j][0]['R_terus'] * r['sejagat'][j][0]['n_terus'] for r in K.values() if r['sejagat'][j][0]['n_terus'])
        rx = sum(r['sejagat'][j][1]['R_terus'] * r['sejagat'][j][1]['n_terus'] for r in K.values() if r['sejagat'][j][1]['n_terus'])
        sj.append((s, kol, S0['D'][j], S0['simpan'][j], float(np.mean(dl)), float(np.mean(np.asarray(dl) > 0)), rt / rx))
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    lama_kod = lambda i: (f"{reg.loc[i, 'henti'].split()[0]} · {c5.kod_keluar(__import__('cs_portfolio6').dari_takrif5(reg.loc[i, 'takrif'])['lajur']).split('· ')[-1]}"
                          if i in reg.index else '–')
    A = ['# CS07 (b): cari dan tala KELUAR — "indikator yang memberitahu kenaikan sudah tamat" (backtest; BUKAN bukti)', '',
         status, '', 'Dijana `kajian/carian_setup/cs_keluar7.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(b) '
         'dan penjelasan (n)-1, dikomit sebelum dijalankan. **Jangan sunting secara manual.**', '',
         '## 1. Apa yang dicari', '',
         f'- {NA} atom keluar berparameter (MA, EMA, MACD, RSI, Supertrend, rendah k hari, Stochastic, volum, Chandelier, ekor, '
         f'"tiada kemajuan") → {NR:,} peraturan (tunggal, ATAU, DAN) × 3 syarat aktif (sentiasa / selepas +5 % / selepas +10 %) × '
         f'{NH} henti = **{NH * NKOL:,} cara keluar setiap setup**, bagi {S0["n_setup"]} setup, pada kumpulan A sahaja.',
         '- Ukuran: **tangkap penuh** = naik ≥ 5 % minggu pertama DAN dijual dengan untung ≥ 10 %. Syarat "tidak jual awal": untung '
         f'pada saham yang terus naik mesti ≥ {SIMPAN_MIN:.0%} daripada "pegang sahaja 20 sesi".',
         f'- {S0["n_lulus"]:,} daripada {NH * NKOL:,} cara keluar lulus syarat itu pada kumpulan A. Tanpa syarat, keluar terbaik '
         f'menaikkan tangkap penuh +{S0["D_tanpa_syarat"] * 100:.1f} mata tetapi dengan menjual saham yang masih naik.', '',
         '## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)', '',
         f"- Keluar terpilih mengatasi `X00` (pegang sahaja, henti sama): **{atas_x00} daripada {len(T)}** setup; mengatasi keluar "
         f"lama: **{atas_lama} daripada {len(L)}**; mengatasi kedua-duanya: **{len(menolong)} daripada {len(L)}**.",
         f"- Syarat \"tidak jual awal\" kekal pada B: {simpan_ok} daripada {len(T)} setup (median nisbah {T.simpan.median():.2f}).",
         f"- Rugi ≥ 8 %: median beza lawan keluar lama {d_rugi * 100:+.1f} mata.",
         f"- Median tangkap penuh (semua isyarat): keluar lama {p(L.tp_lama.median())} % → pegang sahaja {p(T.tp_x00.median())} % → "
         f"keluar terpilih **{p(T.tp_pilih.median())} %**. Median kekurangan dari puncak: lama {p(L.kurang_lama.median())} → "
         f"terpilih {p(T.kurang_pilih.median())} mata.",
         f"- **Keputusan: keluar {'MENOLONG' if ya else 'TIDAK menolong'}** mengikut bacaan yang dikunci.", '',
         '## 3. Keluar sejagat (10 teratas daripada 30; dipilih pada A, disemak pada B)', '',
         '| # | Henti | Peraturan keluar | A: tambahan tangkap penuh (mata) | A: nisbah simpan | B: tambahan (mata) | B: % setup lebih baik | B: nisbah simpan |',
         '|---|---|---|---|---|---|---|---|']
    for j, (s, kol, dA, sA, dB, fB, sB) in enumerate(sj[:10], 1):
        A.append(f'| {j} | {HENTI[s]} | {nama_peraturan(kol)} | {dA * 100:+.2f} | {sA:.2f} | {dB * 100:+.2f} | {fB:.0%} | {sB:.2f} |')
    A += ['', '## 4. Setiap setup (kumpulan B; semua isyarat, perbandingan berpasangan)', '',
          '| ID | Keluar lama | Keluar terpilih | Tangkap penuh %: lama / pegang sahaja / **terpilih** | 2025–26: lama / pegang / terpilih | '
          'Nisbah simpan | Rugi ≥ 8 %: lama → terpilih | Menang %: lama → terpilih | Kurang dari puncak: lama → terpilih | Pegang (sesi) |',
          '|---' * 10 + '|']
    for r in T.itertuples():
        A.append(f"| `{r.id}` | {lama_kod(r.id)} | {r.henti} · {r.keluar_teks} | {p(r.tp_lama)} / {p(r.tp_x00)} / **{p(r.tp_pilih)}** | "
                 f"{p(r.tp_K3_lama)} / {p(r.tp_K3_x00)} / {p(r.tp_K3_pilih)} | {r.simpan:.2f} | {p(r.rugi8_lama, 0)} → {p(r.rugi8_pilih, 0)} | "
                 f"{p(r.menang_lama, 0)} → {p(r.menang_pilih, 0)} | {p(r.kurang_lama)} → {p(r.kurang_pilih)} | "
                 f"{r.pegang_lama:.0f} → {r.pegang_pilih:.0f} |")
    A += ['', '## 5. Kaveat', '',
          '- Keluar dipilih pada kumpulan A daripada ratusan ribu calon; angka A melambung, angka B yang dibaca. Kumpulan B sudah '
          'dilihat dalam pusingan terdahulu.',
          '- Henti yang lebih longgar menaikkan tangkap penuh kerana lebih sedikit dagangan terhenti sebelum sampai +10 %, tetapi '
          'rugi besar setiap dagangan yang gagal turut lebih besar.',
          '- Tiada saham delist. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'KELUAR.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"lapor keluar: {len(T)} setup; menolong {len(menolong)}/{len(L)}; keputusan {'MENOLONG' if ya else 'TIDAK'}")
    return T, ya


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'atom':
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
