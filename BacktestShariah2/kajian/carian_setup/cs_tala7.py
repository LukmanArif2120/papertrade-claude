"""Carian setup — pusingan CS07 bahagian (a): tala parameter masuk SEMUA kaedah (SPEC pindaan 14 Nov 2026 (n)).

Kaedah M: varian rawak julat penuh (v3-v10) dan varian setempat ±25 %; indikator dan kaedah N: keluarga berparameter K01-K25
(`cs_param.py`). Setiap varian diskor dengan enjin (i) pada kumpulan A, sasaran `terus`; kumpulan B untuk laporan sahaja.
Guna: python3 cs_tala7.py benih1|keluarga|skor|benih2|skor2|pilih|kunci|lapor <kerja>
Fail kerja berawalan cs07_. Jangan sunting keluaran secara manual."""
import os
import pickle
import sys

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import multiprocessing as mp  # noqa: E402
import time  # noqa: E402

import cs_akhir as ak  # noqa: E402
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_param as kp  # noqa: E402

V_RAWAK = tuple(range(3, 11))          # 8 varian rawak julat penuh setiap kaedah M (v1, v2 sudah ada dalam benih asal)
N_M_SETEMPAT, N_SETEMPAT = 50, 8       # 50 kaedah M teratas x 8 varian setempat ±25 %
FAIL_M = 'benih_{}_cs07.pkl'


def _pj():
    pj = pd.read_csv(os.path.join(cari.AKAR, 'AUTOTUNE', 'kaedah', 'param_julat.csv'))
    return pj[pj.tala == 'Y']


def varian_m1():
    """Tugas (nama, modul, P): varian rawak v3-v10 bagi setiap kaedah M yang ada parameter boleh tala."""
    pj = pd.read_csv(os.path.join(cari.AKAR, 'AUTOTUNE', 'kaedah', 'param_julat.csv'))
    tugas = []
    for mid in sorted({t[1] for t in cari.senarai_benih() if t[1].startswith('M')}):
        for v in V_RAWAK:
            P = cari.param_varian(pj, mid, v)
            if P:
                tugas.append((f'{mid}.{v}', mid, P))
    return tugas


def varian_m2(terbaik, param):
    """Varian setempat: terbaik = {mid: nama varian terbaik}; param = {nama: dict parameter atau None (lalai)}."""
    pj = _pj()
    tugas, asal = [], {}
    for mid, nama in sorted(terbaik.items()):
        d = pj[pj.kaedah == mid]
        asas = param.get(nama) or {x.nama: x.nilai_asal for x in d.itertuples()}
        for v in range(1, N_SETEMPAT + 1):
            rng = np.random.default_rng([atom.BENIH, 7, int(mid[1:]), v])
            Pv = {}
            for x in d.itertuples():
                nilai = float(np.clip(asas.get(x.nama, x.nilai_asal) * rng.uniform(0.75, 1.25), x.bawah, x.atas))
                Pv[x.nama] = int(round(nilai)) if x.jenis == 'int' else nilai
            tugas.append((f'{nama}s{v}', mid, Pv))
            asal[f'{nama}s{v}'] = nama
    return tugas, asal


# ---------- keluarga K: isyarat (hari pertama, layak) setiap varian ----------
_W = {}


def _k_satu(julat):
    a, b = julat
    G, out = _W['G'], [[] for _ in _W['G']]
    for ti in range(a, b):
        g = _W['fr'][_W['tick'][ti]]
        m0, m1 = int(_W['mula'][ti]), int(_W['mula'][ti + 1])
        assert len(g) == m1 - m0, _W['tick'][ti]
        M = kp.kira(g, _W['RS'][_W['tick'][ti]].reindex(g.index), G)
        dulu = np.zeros_like(M)
        dulu[:, 1:] = M[:, :-1]
        M &= ~dulu
        M &= _W['sah'][m0:m1][None, :]
        for i in range(len(G)):
            ix = np.flatnonzero(M[i])
            if len(ix):
                out[i].append((ix + m0).astype(np.int32))
    return out


def keluarga_grid(kerja, set_, G):
    """dict nama -> indeks bar isyarat (hari pertama, layak) bagi senarai varian G pada set A/B."""
    pan = cari.panel(kerja, set_)
    fr, _, _ = cari.muat_set(set_)
    tick = sorted(fr)
    assert list(pan['ticker']) == tick
    px = pd.DataFrame({t: fr[t].close for t in tick})
    _W.update(G=G, fr=fr, tick=tick, mula=pan['mula'], sah=pan['sah'], RS=(px / px.shift(126) - 1).rank(axis=1, pct=True) * 100)
    julat = [(a, min(a + 25, len(tick))) for a in range(0, len(tick), 25)]
    t0, bah = time.time(), [[] for _ in G]
    with mp.get_context('fork').Pool(cari.PEKERJA) as pool:
        for k, out in enumerate(pool.imap(_k_satu, julat), 1):
            for i, x in enumerate(out):
                bah[i] += x
            if k % 20 == 0:
                cari.log(f'  keluarga {set_}: {k}/{len(julat)} · {time.time() - t0:.0f}s')
    ev = {G[i][0]: (np.sort(np.concatenate(x)) if x else np.zeros(0, np.int32)) for i, x in enumerate(bah)}
    for k in ('fr', 'RS'):
        _W.pop(k, None)
    cari.log(f"keluarga {set_}: {len(G)} varian, {sum(len(v) for v in ev.values()):,} isyarat, {time.time() - t0:.0f}s")
    return ev


def keluarga(kerja, set_):
    """Isyarat grid penuh keluarga K pada set (A/B): cs07_K_<set>.pkl = {'ev': {nama: indeks bar}, 'grid': [...]}."""
    f = os.path.join(kerja, f'cs07_K_{set_}.pkl')
    if os.path.exists(f):
        return pickle.load(open(f, 'rb'))
    G = kp.grid()
    out = {'ev': keluarga_grid(kerja, set_, G), 'grid': G}
    pickle.dump(out, open(f, 'wb'), protocol=4)
    return out


# ---------- label sasaran `terus` + skor enjin (i) ----------
def label_terus(pan):
    """V[bar] = (terus, asas hari sama x tercile ATR %, asas era x tercile); Lb = [m10, terus, puncak] bagi bar sah."""
    sah = np.flatnonzero(pan['sah'])
    Lb = ak.label2(sah, pan['o'], pan['l'], pan['c'])
    hari = pan['hari'][sah]
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(hari).rank(pct=True).to_numpy()
    terc = np.minimum((pct * 3).astype(np.int64), 2)
    V = np.zeros((len(pan['c']), 3))
    V[sah, 0] = Lb[:, 1]
    for a, g in ((1, hari * 3 + terc), (2, pan['tempoh'][sah].astype(np.int64) * 3 + terc)):
        V[sah, a] = (np.bincount(g, Lb[:, 1]) / np.maximum(np.bincount(g), 1))[g]
    return V


def semua_ev(kerja, set_, bahagian):
    """dict nama -> indeks bar isyarat bagi satu bahagian: asal | K | M1 | M2."""
    pan = cari.panel(kerja, set_)
    if bahagian == 'asal':
        return cari.pencetus(pan, pickle.load(open(os.path.join(kerja, f'benih_{set_}.pkl'), 'rb')))
    if bahagian == 'K':
        return keluarga(kerja, set_)['ev']
    bn = pickle.load(open(os.path.join(kerja, FAIL_M.format(set_)), 'rb'))
    N = len(pan['c'])
    mula = lambda bit: np.flatnonzero(atom.mula_isyarat(np.unpackbits(bit)[:N].astype(bool), pan['mula']) & pan['sah'])
    ya = (lambda n: 's' in n) if bahagian == 'M2' else (lambda n: 's' not in n)
    return {n: mula(bit) for n, bit in bn['sig'].items() if ya(n)}


def _skor_satu(nama):
    pan, ev = c5._G['pan'], c5._G['ev'][nama]
    tp = pan['tempoh'][ev].astype(np.int64)
    out = {'n_ev': (int((tp == 0).sum()), int((tp == 1).sum()))}
    if min(out['n_ev']) < c5.N_MIN:
        return nama, dict(out, cukup=False)
    V = np.ascontiguousarray(c5._G['V'][ev])
    Acc = np.zeros((c5.NQ, c5.NC, 2, 4))
    c5.kumpul5(tp, V, np.ascontiguousarray(c5._G['FS'][:, ev].T), np.ascontiguousarray(c5._G['L1'][:, ev].T),
               np.ascontiguousarray(c5._G['L2'][:, ev].T), c5.PASANG, Acc)
    ok, sp, sj = c5.skor_acc(Acc)
    sm = np.where(ok, sp, -np.inf)
    a0 = Acc[0, 0]                                                # pencetus sahaja
    with np.errstate(divide='ignore', invalid='ignore'):
        out.update(cukup=True, n_ok=int(ok.sum()), atas=c5._atas(sm, 5), atas_S=c5._atas(sm[:1], 5),
                   mentah=(a0[:, 1] / a0[:, 0]).tolist(), mentah_asas=(a0[:, 2] / a0[:, 0]).tolist(),
                   skor0=float(sp[0, 0]) if ok[0, 0] else np.nan)
    return nama, out


def skor_ev(kerja, ev, siap=None, simpan=None, V=None):
    """Skor setiap pencetus dalam ev (nama -> indeks bar) pada kumpulan A. Sasaran lalai `terus`; V = (label, asas hari sama,
    asas era) setiap bar bagi sasaran lain (cth. `besar`, CS08). Pulangkan dict nama -> hasil."""
    siap = {} if siap is None else siap
    tugas = sorted([n for n in ev if n not in siap], key=lambda n: -len(ev[n]))
    if not tugas:
        return siap
    pan = cari.panel(kerja, 'A')
    L = lapis.muat(kerja, 'A')
    c5._G.update(pan=pan, ev=ev, V=label_terus(pan) if V is None else V, FS=np.ascontiguousarray(pan['F'][c5.SAHAM]),
                 L1=L['L1'], L2=L['L2'])
    c5.kumpul5(np.zeros(1, np.int64), np.zeros((1, 3)), np.zeros((1, c5.NS), np.uint8), np.zeros((1, lapis.N1), np.uint8),
               np.zeros((1, lapis.N2), np.uint8), c5.PASANG, np.zeros((c5.NQ, c5.NC, 2, 4)))       # kompil sebelum fork
    t0 = time.time()
    with mp.get_context('fork').Pool(cari.PEKERJA) as pool:
        for k, (n, r) in enumerate(pool.imap_unordered(_skor_satu, tugas), 1):
            siap[n] = r
            if k % 100 == 0:
                cari.log(f'  {k}/{len(tugas)} · {time.time() - t0:.0f}s')
                if simpan:
                    pickle.dump(siap, open(simpan + '.tmp', 'wb'), protocol=4)
                    os.replace(simpan + '.tmp', simpan)
    return siap


def skor(kerja, bahagian):
    """Skor setiap pencetus bahagian itu pada kumpulan A (sasaran `terus`): cs07_skor_<bahagian>.pkl."""
    f = os.path.join(kerja, f'cs07_skor_{bahagian}.pkl')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    ev = semua_ev(kerja, 'A', bahagian)
    cari.log(f'skor {bahagian}: {sum(1 for n in ev if n not in siap)} pencetus (siap {len(siap)})')
    siap = skor_ev(kerja, ev, siap, f)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    cari.log(f"skor {bahagian} siap: {sum(1 for r in siap.values() if r.get('cukup'))} cukup isyarat daripada {len(siap)}")
    return siap


# ---------- pilih (kumpulan A) ----------
N_PAPAN, MAKS_INDUK, MAKS_PRA = 12, 2, 3                    # papan baharu CS07 dan had kepelbagaian
BAHAGIAN = ('asal', 'K', 'M1', 'M2')


def induk(nama):
    return nama[:3] if nama[0] == 'K' else nama.split('.')[0] if nama[0] == 'M' else nama


def jadual(kerja, awalan='cs07'):
    """Satu baris setiap pencetus yang cukup isyarat: skor A terbaik dan peraturan masuknya (awalan fail: cs07 / cs08)."""
    R = []
    for bhg in BAHAGIAN:
        f = os.path.join(kerja, f'{awalan}_skor_{bhg}.pkl')
        if not os.path.exists(f):
            continue
        for nama, r in pickle.load(open(f, 'rb')).items():
            if not r.get('cukup') or not len(r['atas'][0]) or not np.isfinite(r['atas'][1][0]):
                continue
            q1, q2, f1, f2 = (int(x[0]) for x in c5.nyah(r['atas'][0][:1]))
            _, _, g1, g2 = (int(x[0]) for x in c5.nyah(r['atas_S'][0][:1])) if len(r['atas_S'][0]) else (0, 0, -1, -1)
            R.append(dict(nama=nama, bahagian=bhg, induk=induk(nama), skor=float(r['atas'][1][0]), q1=q1, q2=q2, f1=f1, f2=f2,
                          skor_S=float(r['atas_S'][1][0]) if len(r['atas_S'][0]) else np.nan, s1=g1, s2=g2,
                          skor0=r['skor0'], n_E1=r['n_ev'][0], n_E2=r['n_ev'][1]))
    T = pd.DataFrame(R)
    asal = kp.asal()
    T['asal'] = T.nama.map(asal).fillna('')
    T['ibu'] = ((T.bahagian == 'asal') & (T.nama.str.endswith('.0') | ~T.nama.str.startswith('M'))) | (T.asal != '')
    return T.sort_values(['skor', 'nama'], ascending=[False, True], kind='stable').reset_index(drop=True)


def param_semua(kerja):
    P = dict(pickle.load(open(os.path.join(kerja, 'benih_A.pkl'), 'rb'))['param'])
    f = os.path.join(kerja, FAIL_M.format('A'))
    if os.path.exists(f):
        P.update(pickle.load(open(f, 'rb'))['param'])
    return P


def benih2(kerja):
    """Peringkat 2: 50 kaedah M dengan skor A terbaik -> 8 varian setempat ±25 % di sekitar varian terbaiknya."""
    T = jadual(kerja)
    M = T[T.nama.str.startswith('M') & (T.bahagian != 'M2')].drop_duplicates('induk').head(N_M_SETEMPAT)
    tugas, asal_ = varian_m2(dict(zip(M.induk, M.nama)), param_semua(kerja))
    pickle.dump(asal_, open(os.path.join(kerja, 'cs07_m2_asal.pkl'), 'wb'))
    cari.log(f'CS07 benih2 A: {len(tugas)} varian setempat bagi {len(M)} kaedah M')
    return cari.benih(kerja, 'A', tugas=tugas, fail=FAIL_M.format('A'))


def pilih(kerja):
    """Anak terbaik setiap induk + papan baharu CS07. -> cs07_pilihan.pkl, cs07_papan.pkl"""
    T = jadual(kerja)
    baris = []
    for ind, g in T.groupby('induk', sort=True):
        ibu = g[g.ibu]
        if ind[0] not in 'KM' or len(g) < 2:
            continue                                               # pencetus P/N tanpa keluarga: tidak ditala pusingan ini
        anak = g.iloc[0]
        ib = ibu.iloc[0] if len(ibu) else None
        baris.append(dict(induk=ind, n_varian=len(g), anak=anak.nama, skor_anak=anak.skor,
                          ibu=ib.nama if ib is not None else '', skor_ibu=ib.skor if ib is not None else np.nan,
                          sama=bool(ib is not None and ib.nama == anak.nama)))
    P = pd.DataFrame(baris)
    baharu = T[T.bahagian != 'asal']
    papan, bil_i, bil_p = [], {}, {}
    for r in baharu.itertuples():
        if r.asal or bil_i.get(r.induk, 0) >= MAKS_INDUK or bil_p.get((r.q1, r.q2), 0) >= MAKS_PRA or r.skor <= 0:
            continue
        bil_i[r.induk] = bil_i.get(r.induk, 0) + 1
        bil_p[(r.q1, r.q2)] = bil_p.get((r.q1, r.q2), 0) + 1
        papan.append(dict(id=f'C{len(papan) + 1:02d}', pencetus=r.nama, q1=r.q1, q2=r.q2, f1=r.f1, f2=r.f2, skor=r.skor))
        if len(papan) == N_PAPAN:
            break
    pickle.dump({'T': T, 'P': P}, open(os.path.join(kerja, 'cs07_pilihan.pkl'), 'wb'), protocol=4)
    pickle.dump(papan, open(os.path.join(kerja, 'cs07_papan.pkl'), 'wb'), protocol=4)
    ada = P[P.ibu != '']
    cari.log(f"pilih: {len(T)} pencetus berskor; {len(P)} induk ditala ({int((P.induk.str[0] == 'M').sum())} M, "
             f"{int((P.induk.str[0] == 'K').sum())} K); anak mengatasi ibu pada A: {int((~ada.sama).sum())} daripada {len(ada)}; "
             f"papan baharu {len(papan)}")
    return T, P, papan


# ---------- kunci (kumpulan B) ----------
def ev_satu(kerja, set_, nama):
    """Indeks bar isyarat satu pencetus pada set (asal, keluarga K atau varian M CS07)."""
    if ('asal', set_) not in _W:
        _W[('asal', set_)] = semua_ev(kerja, set_, 'asal')
    if nama in _W[('asal', set_)]:
        return _W[('asal', set_)][nama]
    if nama[0] == 'K':
        if ('K', set_) not in _W:
            _W[('K', set_)] = keluarga(kerja, set_)['ev']
        return _W[('K', set_)][nama]
    if ('M', set_) not in _W:
        ev = semua_ev(kerja, set_, 'M1')
        ev.update(semua_ev(kerja, set_, 'M2'))
        _W[('M', set_)] = ev
    return _W[('M', set_)][nama]


def benih_b(kerja):
    """Benih kumpulan B bagi varian M baharu yang terpilih (anak dan papan) sahaja."""
    S = pickle.load(open(os.path.join(kerja, 'cs07_pilihan.pkl'), 'rb'))
    papan = pickle.load(open(os.path.join(kerja, 'cs07_papan.pkl'), 'rb'))
    T = S['T']
    atas = top20(T, True).nama.tolist() + top20(T, False).nama.tolist()
    mahu = sorted({n for n in list(S['P'].anak) + [b['pencetus'] for b in papan] + atas
                   if n[0] == 'M' and n in set(T[T.bahagian.isin(['M1', 'M2'])].nama)})
    P = param_semua(kerja)
    tugas = [(n, n.split('.')[0], P[n]) for n in mahu]
    cari.log(f'CS07 benih B: {len(tugas)} varian M terpilih')
    return cari.benih(kerja, 'B', tugas=tugas, fail=FAIL_M.format('B'))


def top20(T, dengan_baharu, k=20):
    """20 pencetus teratas ikut skor A (maks 2 setiap induk), dengan atau tanpa varian baharu."""
    D = T if dengan_baharu else T[T.bahagian == 'asal']
    return D[D.groupby('induk').cumcount() < MAKS_INDUK].head(k)


def kadar7(pan, V, e):
    """{tempoh atau -1: (n, kadar terus, asas hari sama)}; satu posisi setiap saham (pegang 20 sesi)."""
    import cs_teras as teras
    e = e[teras.satu_posisi(e, np.full(len(e), atom.TMAX - 1), pan['tid'])]
    tp = pan['tempoh'][e]
    out = {}
    for p in list(range(int(pan['tempoh'].max()) + 1)) + [-1]:
        k = e if p < 0 else e[tp == p]
        out[p] = (len(k), float(V[k, 0].mean()) if len(k) else np.nan, float(V[k, 1].mean()) if len(k) else np.nan)
    return out


def kunci(kerja):
    """Nilai induk, anak, papan dan 20 teratas pada kumpulan B. -> cs07_kunci.pkl"""
    S = pickle.load(open(os.path.join(kerja, 'cs07_pilihan.pkl'), 'rb'))
    T, P = S['T'].set_index('nama'), S['P']
    papan = pickle.load(open(os.path.join(kerja, 'cs07_papan.pkl'), 'rb'))
    pan = cari.panel(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr, V = (L['L1'], L['L2']), label_terus(pan)

    def nilai(nama):
        r = T.loc[nama]
        ev = ev_satu(kerja, 'B', nama)
        return kadar7(pan, V, ev[c5.topeng(pan, Lr, ev, int(r.q1), int(r.q2), int(r.f1), int(r.f2))])
    mahu = set(P.anak) | set(P.ibu[P.ibu != '']) | {b['pencetus'] for b in papan}
    mahu |= set(top20(S['T'], True).nama) | set(top20(S['T'], False).nama)
    out = {n: nilai(n) for n in sorted(mahu)}
    pickle.dump(out, open(os.path.join(kerja, 'cs07_kunci.pkl'), 'wb'), protocol=4)
    cari.log(f'kunci: {len(out)} pencetus dinilai pada kumpulan B')
    return out


# ---------- laporan ----------
_GRID = {}


def nama7(nama, param):
    """Nama penuh satu pencetus (keluarga K, kaedah M / N atau indikator P)."""
    import cs_lapor as lapor
    if nama[0] == 'K':
        if not _GRID:
            _GRID.update({n: (fam, p) for n, fam, p in kp.grid()})
        return f'{nama} {kp.teks(*_GRID[nama])}'
    return lapor.nama_pencetus(nama, param)


def lapor_(kerja):
    """hasil/CS07/TALA_MASUK.md + tala_masuk.csv + papan_masuk.csv."""
    import cs_lapor as lapor
    S = pickle.load(open(os.path.join(kerja, 'cs07_pilihan.pkl'), 'rb'))
    T, P = S['T'], S['P']
    K = pickle.load(open(os.path.join(kerja, 'cs07_kunci.pkl'), 'rb'))
    papan = pickle.load(open(os.path.join(kerja, 'cs07_papan.pkl'), 'rb'))
    param = param_semua(kerja)
    Ti = T.set_index('nama')
    kl = lambda n, p=-1: (K[n][p][1] - K[n][p][2]) if n in K and K[n][p][0] else np.nan
    kd = lambda n, p=-1: K[n][p][1] if n in K and K[n][p][0] else np.nan
    nb = lambda n, p=-1: K[n][p][0] if n in K else 0
    P = P.assign(kl_anak=[kl(n) for n in P.anak], kl_ibu=[kl(n) if n else np.nan for n in P.ibu],
                 kl3_anak=[kl(n, 2) for n in P.anak], kl3_ibu=[kl(n, 2) if n else np.nan for n in P.ibu],
                 terus_anak=[kd(n) for n in P.anak], terus_ibu=[kd(n) if n else np.nan for n in P.ibu],
                 n_anak=[nb(n) for n in P.anak], n_ibu=[nb(n) if n else 0 for n in P.ibu],
                 baharu=[Ti.loc[n, 'bahagian'] != 'asal' and not Ti.loc[n, 'asal'] for n in P.anak])
    d_ = os.path.join(SINI, 'hasil', 'CS07')
    os.makedirs(d_, exist_ok=True)
    P.to_csv(os.path.join(d_, 'tala_masuk.csv'), index=False, float_format='%.5f')
    pas = P[(P.ibu != '') & ~P.sama & P.kl_anak.notna() & P.kl_ibu.notna()]
    menang_b = int((pas.kl_anak > pas.kl_ibu).sum())
    p3 = pas[pas.kl3_anak.notna() & pas.kl3_ibu.notna()]
    med3 = float((p3.kl3_anak - p3.kl3_ibu).median()) if len(p3) else np.nan
    ya = len(pas) > 0 and menang_b > len(pas) / 2 and med3 > 0
    p = lambda x, k=1, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')

    def ringkas20(dengan):
        D = top20(T, dengan)
        return dict(n=len(D), baharu=int((D.bahagian != 'asal').sum()), skor=float(D.skor.mean()),
                    kl=float(np.nanmean([kl(n) for n in D.nama])), kl3=float(np.nanmean([kl(n, 2) for n in D.nama])),
                    terus=float(np.nanmean([kd(n) for n in D.nama])),
                    tahan=int(sum(all(kl(n, j) > 0 for j in range(3)) and nb(n) >= 300 for n in D.nama)))
    r1, r0 = ringkas20(True), ringkas20(False)
    pb = pd.DataFrame([dict(b, nama=nama7(b['pencetus'], param), prasyarat=c5.tk_pra(b['q1'], b['q2']),
                            penapis=c5.tk_pen(b['f1'], b['f2']), n_B=nb(b['pencetus']), terus_B=kd(b['pencetus']),
                            asas_B=K[b['pencetus']][-1][2], **{f'kl_K{j + 1}': kl(b['pencetus'], j) for j in range(3)},
                            **{f'n_K{j + 1}': nb(b['pencetus'], j) for j in range(3)}) for b in papan])
    pb['dipercayai'] = (pb.n_B >= 300) & (pb[['kl_K1', 'kl_K2', 'kl_K3']] > 0).all(axis=1)
    pb.to_csv(os.path.join(d_, 'papan_masuk.csv'), index=False, float_format='%.5f')
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    nM, nK = T[T.bahagian.isin(['M1', 'M2'])], T[T.bahagian == 'K']
    bil = {b: len(pickle.load(open(os.path.join(kerja, f'cs07_skor_{b}.pkl'), 'rb')))
           for b in BAHAGIAN if os.path.exists(os.path.join(kerja, f'cs07_skor_{b}.pkl'))}
    liput = sorted(set(kp.asal().values()))
    baki = [x[:3] for x in atom.PENCETUS if x[:3] not in liput] + sorted(
        n for n in set(T[(T.bahagian == 'asal') & T.nama.str.startswith('N')].nama) if n not in liput)
    A = ['# CS07 (a): tala parameter masuk SEMUA kaedah (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_tala7.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(a), dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.**', '',
         '## 1. Apa yang dicuba', '',
         f"- Kaedah M: {bil.get('M1', 0):,} varian rawak julat penuh (8 setiap kaedah, 134 kaedah) + {bil.get('M2', 0):,} varian setempat "
         f"±25 % di sekitar varian terbaik 50 kaedah teratas; {len(nM):,} cukup isyarat untuk diskor.",
         f"- Indikator dan kaedah N: 25 keluarga berparameter, {bil.get('K', 0):,} varian grid penuh; {len(nK):,} cukup isyarat. "
         f"{len(liput)} takrif asal (`P`/`N`) ada dalam keluarga sebagai induk.",
         f"- Bersama {bil.get('asal', 0)} pencetus sedia ada, setiap satu diskor atas 544 gabungan prasyarat × 379 gabungan penapis "
         'saham pada kumpulan A. Sasaran: kadar **"naik lagi"** (naik ≥ 5 % minggu pertama DAN naik lagi hingga minggu ke-4 tanpa '
         'kena henti −8 %) lawan saham rawak hari sama.', '',
         '## 2. Bacaan dikunci: adakah tala menolong pada saham yang tidak dilihat?', '',
         f"- Induk yang ditala: {len(P)} ({int((P.induk.str[0] == 'M').sum())} kaedah M, {int((P.induk.str[0] == 'K').sum())} keluarga "
         f"indikator). Anak berbeza daripada ibu pada kumpulan A: {int(((P.ibu != '') & ~P.sama).sum())} daripada "
         f"{int((P.ibu != '').sum())} (selebihnya, takrif asal sudah yang terbaik).",
         f"- Pada kumpulan B, anak mengatasi ibu (kelebihan \"naik lagi\"): **{menang_b} daripada {len(pas)}** pasangan; median beza "
         f"{p(float((pas.kl_anak - pas.kl_ibu).median()) if len(pas) else np.nan, 2, True)} mata; dalam 2025–26 (K3) median beza "
         f"{p(med3, 2, True)} mata ({int((p3.kl3_anak > p3.kl3_ibu).sum())} daripada {len(p3)}).",
         f"- **Keputusan: tala {'MENOLONG' if ya else 'TIDAK menolong'}** mengikut bacaan yang dikunci (lebih separuh pasangan DAN "
         'median beza K3 > 0).', '',
         '## 3. 20 pencetus teratas ikut skor A, dinilai pada kumpulan B', '',
         '| | Bilangan varian baharu | Purata skor A (mata) | Purata "naik lagi" B % | Purata kelebihan B (mata) | Purata kelebihan 2025–26 | '
         'Bertahan K1, K2 DAN K3 |', '|---|---|---|---|---|---|---|',
         f"| Tanpa varian baharu | {r0['baharu']} | {p(r0['skor'], 2, True)} | {p(r0['terus'])} | {p(r0['kl'], 2, True)} | "
         f"{p(r0['kl3'], 2, True)} | {r0['tahan']} daripada {r0['n']} |",
         f"| Dengan varian baharu | {r1['baharu']} | {p(r1['skor'], 2, True)} | {p(r1['terus'])} | {p(r1['kl'], 2, True)} | "
         f"{p(r1['kl3'], 2, True)} | {r1['tahan']} daripada {r1['n']} |", '',
         f'## 4. Papan masuk baharu CS07 ({len(pb)} setup; maks 2 setiap induk, 3 setiap pasangan prasyarat)', '',
         '| ID | Pencetus (parameter) | Prasyarat | Penapis saham | Skor A (mata) | Belian B | Naik lagi B % (rawak) | Kelebihan K1 / K2 / K3 | '
         'Dipercayai |', '|---' * 9 + '|']
    for r in pb.itertuples():
        A.append(f"| `{r.id}` | {r.nama} | {r.prasyarat} | {r.penapis} | {p(r.skor, 2, True)} | {r.n_B:,} | {p(r.terus_B)} "
                 f"({p(r.asas_B)}) | {p(r.kl_K1, 1, True)} / {p(r.kl_K2, 1, True)} / {p(r.kl_K3, 1, True)} | "
                 f"{'**ya**' if r.dipercayai else 'tidak'} |")
    A += ['', '## 5. Setiap keluarga indikator: takrif asal lawan parameter terbaik', '',
          '| Keluarga | Varian | Ibu (takrif asal terbaik) | Skor A ibu | Anak (parameter terbaik) | Skor A anak | Kelebihan B: ibu → anak | '
          '2025–26: ibu → anak |', '|---' * 8 + '|']
    for r in P[P.induk.str[0] == 'K'].itertuples():
        A.append(f"| `{r.induk}` | {r.n_varian} | {nama7(r.ibu, param) if r.ibu else '– (keluarga baharu)'} | {p(r.skor_ibu, 2, True)} | "
                 f"{nama7(r.anak, param)} | {p(r.skor_anak, 2, True)} | {p(r.kl_ibu, 1, True)} → {p(r.kl_anak, 1, True)} | "
                 f"{p(r.kl3_ibu, 1, True)} → {p(r.kl3_anak, 1, True)} |")
    Mx = P[P.induk.str[0] == 'M'].sort_values('skor_anak', ascending=False)
    A += ['', f'## 6. Kaedah M: 30 teratas ikut skor A anak (kesemua {len(Mx)} dalam `tala_masuk.csv`)', '',
          '| Kaedah | Varian | Skor A: parameter asal → anak | Anak | Kelebihan B: asal → anak | 2025–26: asal → anak |',
          '|---' * 6 + '|']
    for r in Mx.head(30).itertuples():
        A.append(f"| `{r.induk}` | {r.n_varian} | {p(r.skor_ibu, 2, True)} → {p(r.skor_anak, 2, True)} | "
                 f"{'(parameter asal kekal terbaik)' if r.sama else nama7(r.anak, param)} | {p(r.kl_ibu, 1, True)} → "
                 f"{p(r.kl_anak, 1, True)} | {p(r.kl3_ibu, 1, True)} → {p(r.kl3_anak, 1, True)} |")
    A += ['', '## 7. Baki yang BELUM ditala (untuk mesin)', '',
          f"Corak berbilang syarat tanpa keluarga berparameter dalam pusingan ini ({len(baki)}): {', '.join(f'`{x}`' for x in baki)}. "
          'Ia kekal pada takrif asal dan tetap diskor bersama.', '',
          '## 8. Kaveat', '',
          '- Skor A melambung apabila lebih banyak varian dicuba; hanya angka kumpulan B dan 2025–26 yang dibaca. Kumpulan B sudah '
          'dilihat dalam pusingan terdahulu (bukan tahanan bersih).',
          '- Hampir semua skor tertinggi memakai prasyarat earnings 1–5 sesi akan datang (tarikh sebenar, bukan kalendar awal).',
          '- Tiada saham delist. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'TALA_MASUK.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"lapor tala: anak > ibu pada B {menang_b}/{len(pas)}; median beza K3 {med3 * 100:+.2f}; "
             f"keputusan {'MENOLONG' if ya else 'TIDAK'}; papan {len(pb)} ({int(pb.dipercayai.sum())} dipercayai)")
    return P, pb, ya


def benih1(kerja, set_='A', hanya=None):
    tugas = varian_m1()
    cari.log(f'CS07 benih1 {set_}: {len(tugas)} varian M')
    return cari.benih(kerja, set_, hanya=hanya, tugas=tugas, fail=FAIL_M.format(set_))


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'benih1':
        b = benih1(kerja)
        pickle.dump({'siap': len(b['sig']), 'ralat': len(b['ralat'])}, open(os.path.join(kerja, 'cs07_benih1.siap'), 'wb'))
    elif cmd == 'keluarga':
        keluarga(kerja, sys.argv[3] if len(sys.argv) > 3 else 'A')
    elif cmd == 'skor':
        skor(kerja, sys.argv[3])
    elif cmd == 'benih2':
        benih2(kerja)
    elif cmd == 'pilih':
        pilih(kerja)
    elif cmd == 'benihB':
        benih_b(kerja)
    elif cmd == 'kunci':
        kunci(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
