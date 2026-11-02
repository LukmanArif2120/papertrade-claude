"""Kajian 2 — paksi CARA: bagaimana pesanan diisi. Pradaftar `REVERSE/SPEC_PORTFOLIO_N.md` §4.

Masuk `GB02_atau3`, keluar `X13`, 6 cara pengisian, dua tingkap. m = 6 dipradaftar untuk
BH-FDR; SE berkelompok ikut hari isyarat. Konvensyen kos dan ufuk 126 bar sama seperti
`step19_nxx_keluar.py` supaya nombor boleh dibanding terus dengan `SILANG_AKHIR.md`.

Guna: python3 REVERSE/step23_cara.py [--laporan-sahaja]
Output: REVERSE/CARA.md, REVERSE/cara.csv
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.step18_nxx as S18  # noqa: E402
from REVERSE.teras import kos as K  # noqa: E402

KELUAR = AKAR / 'REVERSE'
LATIH, TAHAN = (2012, 2019), (2020, 2025)
CAIR, MIN_N, IMBAS = 100_000.0, 200, 126
M_PRADAFTAR = 6                      # spec §4.3 CARA2
RSI_KELUAR = 70.0
KOLAM3 = ['N19', 'N37', 'N115']

# Paksi KELUAR boleh ditukar oleh pemanggil (`step38_cara_94.py`) supaya kajian CARA boleh
# dijalankan pada keluar yang 94 kombinasi produksi SEBENARNYA pakai, bukan `X13` sahaja.
# Lalai `X13` = tingkah laku asal, bit-identik (disemak dengan md5 cara.csv).
# Peraturan sama seperti `step33_portfolio_94.hari_keluar()` — satu definisi, bukan dua.
KELUAR_ID = 'X13'
KELUAR_SAH = ('X13', 'X14', 'X15', 'X16', 'X17', 'X36')
TRAIL_ATR = 4.0                      # X15 Chandelier, sama seperti step33

# (id, had bar pengisian, penerangan)
CSPEC = [
    ('C01', 1, 'pasaran pada buka esok (asas repo)'),
    ('C02', 5, 'buy-stop tinggi20 x 1.002, sah 5 bar'),
    ('C03', 3, 'buy-limit tutup x 0.985, sah 3 bar'),
    ('C04', 3, 'buy-limit tutup x 0.99, sah 3 bar'),
    ('C05', 5, 'OCO buy-limit x0.98 lawan buy-stop x1.02, sah 5 bar'),
    ('C06', 1, 'bracket: pasaran + sasaran +6% + henti -3%'),
]
KOD = [k for k, _, _ in CSPEC]
BRAKET_SASARAN, BRAKET_HENTI = 1.06, 0.97


def pulangan_cara(P):
    """Bagi setiap bar: pulangan bersih setiap cara, offset isi, dan bendera henti hari-0."""
    o = P.buka.to_numpy('float64')
    h = P.tinggi.to_numpy('float64')
    lo = P.rendah.to_numpy('float64')
    c = P.tutup.to_numpy('float64')
    rsi = P.rsi14.to_numpy('float64')
    t20 = P.tinggi20.to_numpy('float64')
    # Array yang hanya keluar bukan-X13 perlukan. ATR diambil pada bar ISYARAT (bukan bar
    # pengisian) supaya lebar ekor X15 SAMA merentas enam cara — jika tidak, paksi CARA dan
    # lebar henti bergerak serentak dan keputusan mengelirukan kedua-duanya.
    ma50 = P.ma50.to_numpy('float64')
    adx = P.adx14.to_numpy('float64')
    sup = P.supertrend.to_numpy('float64')
    atr_sig = P.atr14.to_numpy('float64')
    tk = P.ticker.to_numpy()
    m = len(c)
    idx = np.arange(m)
    akhir = np.concatenate([tk[1:] != tk[:-1], [True]])
    buka_next = np.where(akhir, c, np.concatenate([o[1:], [np.nan]]))
    ks = K.KOMISEN + np.array([K.slippage(x) for x in P.nilai20.to_numpy('float64')])

    fo = {k: np.full(m, -1) for k in KOD}        # offset bar pengisian (dari bar isyarat)
    fpx = {k: np.full(m, np.nan) for k in KOD}

    # --- fasa 1: pengisian
    paras = {'C02': t20 * 1.002, 'C03': c * 0.985, 'C04': c * 0.99,
             'C05L': c * 0.98, 'C05S': c * 1.02}
    for j in range(1, 6):
        kk = np.minimum(idx + j, m - 1)
        sah = ((idx + j) < m) & (tk[kk] == tk)
        ok = np.isfinite(o[kk]) & (o[kk] > 0)
        hk, lk, ok_ = np.where(sah, h[kk], np.nan), np.where(sah, lo[kk], np.nan), sah & ok

        def isi(k, kena, harga, had):
            if j > had:
                return
            a, p = fo[k], fpx[k]
            kn = ok_ & (a < 0) & kena
            a[kn], p[kn] = j, harga[kn]

        isi('C01', np.ones(m, bool), o[kk], 1)
        isi('C06', np.ones(m, bool), o[kk], 1)
        isi('C02', hk >= paras['C02'], np.maximum(paras['C02'], o[kk]), 5)
        isi('C03', lk <= paras['C03'], np.minimum(paras['C03'], o[kk]), 3)
        isi('C04', lk <= paras['C04'], np.minimum(paras['C04'], o[kk]), 3)
        # C05 OCO: jika kedua-dua disentuh dalam bar sama, andaikan yang MERUGIKAN kita
        # (buy-stop, harga lebih tinggi) berlaku dahulu — spec §4.1.
        kena_s = hk >= paras['C05S']
        kena_l = lk <= paras['C05L']
        isi('C05', kena_s, np.maximum(paras['C05S'], o[kk]), 5)
        isi('C05', kena_l & ~kena_s, np.minimum(paras['C05L'], o[kk]), 5)

    # --- fasa 2: keluar
    bar = {k: np.full(m, -1) for k in KOD}
    pxk = {k: np.full(m, np.nan) for k in KOD}
    hari0 = np.zeros(m, bool)                    # C06 dihentikan pada bar masuk
    hidup = idx.copy()
    # X15 ialah satu-satunya peraturan dengan KEADAAN setiap posisi (puncak bergerak), dan
    # puncak mesti bermula pada bar PENGISIAN yang berbeza setiap cara — jadi ia per-cara.
    puncak = {k: np.full(m, -np.inf) for k in KOD}
    for j in range(1, IMBAS + 1):
        kk = np.minimum(idx + j, m - 1)
        sah = ((idx + j) < m) & (tk[kk] == tk)
        rk = np.where(sah, rsi[kk], np.nan)
        hk, lk = np.where(sah, h[kk], np.nan), np.where(sah, lo[kk], np.nan)
        bk = buka_next[kk]
        ck = np.where(sah, c[kk], np.nan)
        kp = np.maximum(kk - 1, 0)               # bar sebelum; sah sudah jamin ticker sama
        if KELUAR_ID == 'X13':
            cet = rk > RSI_KELUAR
        elif KELUAR_ID == 'X14':
            cet = (rk > 50.0) & (np.where(sah, rsi[kp], np.nan) <= 50.0)
        elif KELUAR_ID == 'X16':
            cet = np.where(sah, sup[kk], np.nan) <= 0.0
        elif KELUAR_ID == 'X17':
            cet = np.where(sah, adx[kk], np.nan) < 20.0
        elif KELUAR_ID == 'X36':                 # DUA tutup berturut bawah ma50
            cet = ((ck < np.where(sah, ma50[kk], np.nan))
                   & (np.where(sah, c[kp], np.nan) < np.where(sah, ma50[kp], np.nan)))
        elif KELUAR_ID == 'X15':
            cet = None                           # per-cara, dikira dalam gelung di bawah
        else:
            raise SystemExit(f'KELUAR_ID tidak dikenali: {KELUAR_ID}')
        for k in KOD:
            a, p = bar[k], pxk[k]
            hidup_k = sah & (fo[k] > 0) & (j >= fo[k]) & (a < 0)
            if cet is None:                      # X15 Chandelier tutup, puncak per cara
                pk = puncak[k]
                np.maximum(pk, np.where(hidup_k, ck, -np.inf), out=pk)
                cetk = hidup_k & np.isfinite(ck) & (ck < pk - TRAIL_ATR * atr_sig)
            else:
                cetk = cet
            if k == 'C06':
                sas = fpx[k] * BRAKET_SASARAN
                hen = fpx[k] * BRAKET_HENTI
                kena_h = hidup_k & (lk <= hen)
                kena_s = hidup_k & (hk >= sas) & ~kena_h       # henti didahulukan
                a[kena_h], p[kena_h] = kk[kena_h], np.minimum(hen, o[kk])[kena_h]
                hari0 |= kena_h & (j == fo[k])
                a[kena_s], p[kena_s] = kk[kena_s], np.maximum(sas, o[kk])[kena_s]
                sisa = hidup_k & (a < 0) & cetk
                a[sisa], p[sisa] = kk[sisa], bk[sisa]
            else:
                kena = hidup_k & cetk
                a[kena], p[kena] = kk[kena], bk[kena]
        hidup = np.where(sah, kk, hidup)

    out = {}
    for k in KOD:
        a, p = bar[k], pxk[k]
        belum = (a < 0) & (fo[k] > 0)
        a2 = a.copy()
        a2[belum] = hidup[belum]
        p = p.copy()
        p[belum] = buka_next[a2[belum]]
        with np.errstate(invalid='ignore', divide='ignore'):
            r = (p * (1 - ks)) / (fpx[k] * (1 + ks)) - 1.0
        r = np.where(fo[k] > 0, r, np.nan)
        out[k] = (r, fo[k], fpx[k], a2)
    return out, hari0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = KELUAR / 'cara.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f))

    t0 = time.time()
    rsf = S18.rs_persentil()
    kel = S18.kelompok_ticker()
    AK = {}                       # (cara, tingkap) -> senarai array
    HARI = {}                     # tingkap -> senarai array hari
    EKSTRA = {}                   # (cara, tingkap) -> [n_isyarat, n_isi, hari0, px_rel]
    print(f'1/2 {len(kel)} kelompok x 6 cara...', flush=True)
    for i, bk in enumerate(kel):
        P = S18._sedia(bk, S18.PUL, rsf)
        T = S18.topeng(P)
        sig = np.logical_or.reduce([T[k] for k in KOLAM3])
        PU, hari0 = pulangan_cara(P)
        th = P.date.dt.year.to_numpy()
        hari = P.date.to_numpy().astype('datetime64[D]').astype('int64')
        cair = P.nilai20.to_numpy() >= CAIR
        W = {'latih': (th >= LATIH[0]) & (th <= LATIH[1]) & cair & sig,
             'tahan': (th >= TAHAN[0]) & (th <= TAHAN[1]) & cair & sig}
        px01 = PU['C01'][2]
        for w, wm in W.items():
            if not wm.any():
                continue
            HARI.setdefault(w, []).append(hari[wm])
            for k in KOD:
                r, fo_, fpx_, _ = PU[k]
                rr = np.where(wm, r, np.nan)[wm]
                AK.setdefault((k, w), []).append(rr.astype('float32'))
                e = EKSTRA.setdefault((k, w), [0, 0, 0, 0.0, 0])
                e[0] += int(wm.sum())
                isi = (fo_ > 0) & wm
                e[1] += int(isi.sum())
                if k == 'C06':
                    e[2] += int((hari0 & isi).sum())
                rel = np.where(isi & np.isfinite(px01) & (px01 > 0), fpx_ / px01 - 1.0, np.nan)
                rel = rel[np.isfinite(rel)]
                e[3] += float(rel.sum()); e[4] += int(rel.size)
        del P, T, PU
        print(f'    [{time.time() - t0:.0f}s] kelompok {i + 1}/{len(kel)}', flush=True)

    H = {w: np.concatenate(v) for w, v in HARI.items()}
    R = {}
    for (k, w), v in AK.items():
        R[(k, w)] = np.concatenate(v)
    baris = []
    for w in ('latih', 'tahan'):
        base = R[('C01', w)]
        for k in KOD:
            x = R[(k, w)]
            terisi = x[np.isfinite(x)]
            per_sig = np.where(np.isfinite(x), x, 0.0)
            e = EKSTRA[(k, w)]
            d = per_sig - np.where(np.isfinite(base), base, 0.0)
            tt, pp, kk = (np.nan, np.nan, 0) if k == 'C01' else S18.t_kelompok(d, H[w])
            u = np.sort(terisi)[::-1]
            baris.append(dict(
                cara=k, tingkap=w, n_isyarat=e[0], n_isi=e[1],
                kadar_isi=100.0 * e[1] / max(1, e[0]),
                jangkaan_sig=float(per_sig.mean() * 100),
                jangkaan_isi=float(terisi.mean() * 100) if terisi.size else np.nan,
                menang=float((terisi > 0).mean() * 100) if terisi.size else np.nan,
                tanpa5=float(u[int(np.ceil(0.05 * u.size)):].mean() * 100)
                if u.size > 20 else np.nan,
                px_rel=100.0 * e[3] / max(1, e[4]), henti_hari0=e[2],
                beza=float((per_sig.mean() - np.where(np.isfinite(base), base, 0.0).mean())
                           * 100),
                t=tt, p=pp, n_hari=kk))
    D = pd.DataFrame(baris)
    D.to_csv(f, index=False, float_format='%.6f')
    return laporan(D)


def laporan(D):
    t = D[D.tingkap == 'tahan'].set_index('cara')
    l = D[D.tingkap == 'latih'].set_index('cara')
    alt = [k for k in KOD if k != 'C01']
    p = np.array([t.loc[k, 'p'] for k in alt], dtype='float64')
    lulus2, amb = S18.bh_m(p, M_PRADAFTAR)
    g1 = {k: bool(t.loc[k, 'beza'] > 0 and l.loc[k, 'beza'] > 0) for k in alt}
    g2 = {k: bool(lulus2[i]) for i, k in enumerate(alt)}
    g3 = {k: bool(t.loc[k, 'jangkaan_sig'] > 0) for k in alt}
    D['CARA1'] = [g1.get(r.cara, False) for r in D.itertuples()]
    D['CARA2'] = [g2.get(r.cara, False) for r in D.itertuples()]
    D['CARA3'] = [g3.get(r.cara, False) for r in D.itertuples()]
    D.to_csv(KELUAR / 'cara.csv', index=False, float_format='%.6f')
    n1 = sum(g1.values()); n2 = sum(g2.values()); n3 = sum(g3.values())
    lulus = [k for k in alt if g1[k] and g2[k] and g3[k]]
    print()
    print(f'gate (m dipradaftar = {M_PRADAFTAR}, ambang BH p = {amb}):')
    print(f'  CARA1 beza > 0 dua tingkap : {n1}/5')
    print(f'  CARA2 BH-FDR q <= 0.05     : {n2}/5')
    print(f'  CARA3 jangkaan mutlak > 0  : {n3}/5')
    print(f'  LULUS KETIGA-TIGA          : {len(lulus)}/5  {lulus}')
    print()
    kol = ['cara', 'n_isyarat', 'n_isi', 'kadar_isi', 'jangkaan_sig', 'jangkaan_isi',
           'menang', 'tanpa5', 'px_rel', 'beza', 'p', 'henti_hari0']
    for w in ('tahan', 'latih'):
        print(f'=== tingkap {w} ===')
        print(D[D.tingkap == w][kol].to_string(index=False,
                                               float_format=lambda v: f'{v:.3f}'))
        print()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
