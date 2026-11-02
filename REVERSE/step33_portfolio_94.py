"""Portfolio 94 kombinasi produksi lawan SPUS — pradaftar `REVERSE/SPEC_PORTFOLIO_94.md`.

MENGAPA: `portfolio_n_ringkas.csv` menguji `GB02_atau3/atau4/RAWAK` sahaja — konfigurasi
yang sudah BERSARA dan berpangkat 7/1,496 dalam grid penuh. Tiada satu pun daripada 94
kombinasi produksi pernah diuji sebagai portfolio, jadi "0/36 gagal" ialah kesimpulan
tentang kohort yang LAIN. Larian ini mengukur kohort yang sebenarnya dijalankan.

Enjin portfolio diguna semula daripada `REVERSE/pembinaan.py` + corak `step22_portfolio_n.py`
supaya tiada enjin kedua. Topeng masuk datang daripada `step18_nxx.topeng()` — fungsi kajian
SENDIRI, bukan transkripsi tangan, jadi pariti dengan grid penuh automatik.

UNIT POSISI (spec §3): satu posisi = satu pasangan (saham, keluar). Saham sama dengan DUA
keluar berbeza = DUA posisi; dengan keluar SAMA daripada dua masuk = SATU posisi.

Guna: python3 REVERSE/step33_portfolio_94.py [--benih 20] [--laporan-sahaja]
Output: REVERSE/PORTFOLIO_94.md, REVERSE/portfolio_94.csv
"""
import argparse
import csv
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.pembinaan as PB  # noqa: E402
import REVERSE.step18_nxx as S18  # noqa: E402
from REVERSE.teras import kos as K  # noqa: E402

KELUAR = AKAR / 'REVERSE'
CACHE = KELUAR / '.cache'
MAT = CACHE / 'p94_matriks.npz'
CAND = CACHE / 'p94_calon.npz'
JEJAK = KELUAR / 'jejak_semua.csv'
KELOMPOK = KELUAR / 'bertindih_kelompok.csv'

UJI0, UJI1 = '2020-01-01', '2025-12-31'
HAD_IMBAS = 504          # spec §4 — had imbasan keluar
TMAX = 126               # had pegangan, sama seperti modul produksi
TRAIL_ATR = 4.0          # X15 Chandelier
N_BENIH = 20
AMBANG_NISBAH = 0.669    # spec §5 P4
SPUS_CAGR, SPUS_MDD = 17.95, -26.82

# kod keluar -> indeks tetap, supaya (ti, keluar) boleh disimpan sebagai dua int32
RULE = ['X13', 'X14', 'X15', 'X16', 'X17', 'X36']
RID = {r: i for i, r in enumerate(RULE)}


# ---------------------------------------------------------------- kohort
def kohort():
    """94 pasangan (masuk, keluar) + 36 wakil kelompok. Daripada fail keputusan, bukan tangan."""
    J = list(csv.DictReader(open(JEJAK, encoding='utf-8')))
    p94 = [(x['masuk'], x['keluar']) for x in J]
    assert len(p94) == len(set(p94)), 'jejak_semua.csv ada pasangan berganda'
    # wakil kelompok: ID pangkat TERBAIK dalam setiap kelompok pertindihan
    peta = {}
    for r in csv.DictReader(open(KELOMPOK, encoding='utf-8')):
        for t in r['topeng'].split():
            peta[t] = r['kelompok']
    terbaik = {}
    for x in sorted(J, key=lambda z: int(z['pangkat'])):
        k = peta.get(x['masuk'], 'x' + x['masuk'])
        terbaik.setdefault(k, (x['masuk'], x['keluar']))
    p36 = sorted(terbaik.values())
    return p94, p36


# ---------------------------------------------------------------- matriks
def matriks():
    """Matriks ticker x tarikh yang enjin perlukan, daripada panel kajian yang sama."""
    if MAT.exists():
        z = np.load(MAT, allow_pickle=True)
        return {k: z[k] for k in z.files}
    t0 = time.time()
    P = PB.Panel()                      # O, C, A(atr), N(nilai), tick, tarikh
    it = {t: i for i, t in enumerate(P.tick)}
    idt = {d: i for i, d in enumerate(P.tarikh)}
    LJ = ['rsi14', 'supertrend', 'adx14', 'ma50']
    M = {k: np.full((len(P.tick), len(P.tarikh)), np.nan, 'float32') for k in LJ}
    import pyarrow.parquet as pq
    for i, bk in enumerate(S18.kelompok_ticker()):
        x = pq.read_table(S18.PANEL, columns=['ticker', 'date'] + LJ,
                          filters=[('ticker', 'in', set(bk))]).to_pandas()
        x = x[x.ticker.isin(it)]
        if x.empty:
            continue
        ii = x.ticker.map(it).to_numpy()
        jj = np.array([idt.get(d, -1) for d in x.date.to_numpy()])
        ok = jj >= 0
        for k in LJ:
            M[k][ii[ok], jj[ok]] = x[k].to_numpy('float32')[ok]
        del x
        print(f'    [{time.time() - t0:.0f}s] matriks kelompok {i + 1}', flush=True)
    M['O'], M['C'], M['A'], M['N'] = P.O, P.C, P.A, P.N
    # Tarikh dinormalkan ke datetime64[D]. Pepijat yang ini betulkan: str(Timestamp) beri
    # '2011-01-03 00:00:00' manakala str(numpy.datetime64) beri
    # '2009-01-02T00:00:00.000000000', jadi TIADA satu pun kunci sepadan dan calon = 0 hari.
    M['tarikh'] = np.asarray(pd.to_datetime(list(P.tarikh)).values, dtype='datetime64[D]')
    M['tick'] = np.asarray(list(P.tick))
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(MAT, **M)
    return M


def u14_matriks(C):
    """U14 = momentum 12-1 = C[t-21] / C[t-252] - 1. NaN -> -9e9 (sama seperti produksi)."""
    n, m = C.shape
    U = np.full((n, m), -9e9, 'float32')
    a, b = C[:, :-21], C[:, :-252]
    # susun supaya U[:, t] guna C[:, t-21] dan C[:, t-252]
    for t in range(252, m):
        num, den = C[:, t - 21], C[:, t - 252]
        with np.errstate(invalid='ignore', divide='ignore'):
            v = num / den - 1.0
        U[:, t] = np.where(np.isfinite(v), v, -9e9)
    del a, b
    return U


# ---------------------------------------------------------------- calon
def calon(p94):
    """CAL[a] = (ti[], kcode[]) semua pasangan (saham, keluar) yang dicetus pada sauh a."""
    if CAND.exists():
        z = np.load(CAND, allow_pickle=True)
        return {int(k): (z[f't{k}'], z[f'k{k}']) for k in z['hari']}
    t0 = time.time()
    M = matriks()
    it = {t: i for i, t in enumerate(M['tick'])}
    idt = {d: i for i, d in enumerate(M['tarikh'])}
    masuk_ke_keluar = {}
    for m_, k_ in p94:
        masuk_ke_keluar.setdefault(m_, []).append(RID[k_])
    rsf = S18.rs_persentil()
    bucket = {}
    for i, bk in enumerate(S18.kelompok_ticker()):
        P = S18._sedia(bk, S18.PUL, rsf)
        T = S18.topeng(P)
        tk = P.ticker.to_numpy()
        dt = P.date.to_numpy().astype('datetime64[D]')
        for m_, kods in masuk_ke_keluar.items():
            if m_ not in T:
                continue
            sel = np.asarray(T[m_], bool)
            if not sel.any():
                continue
            tt = np.array([it.get(x, -1) for x in tk[sel]])
            dd = np.array([idt.get(x, -1) for x in dt[sel]])
            ok = (tt >= 0) & (dd >= 0)
            for kc in kods:
                for a, ti in zip(dd[ok], tt[ok]):
                    bucket.setdefault(int(a), set()).add((int(ti), kc))
        del P, T
        print(f'    [{time.time() - t0:.0f}s] calon kelompok {i + 1}', flush=True)
    if not bucket:
        raise SystemExit('calon KOSONG — kunci ticker/tarikh tidak sepadan; jangan cache ini')
    out, simpan = {}, {'hari': np.asarray(sorted(bucket), 'int64')}
    for a, s in bucket.items():
        arr = np.array(sorted(s), 'int32')
        out[a] = (arr[:, 0].copy(), arr[:, 1].copy())
        simpan[f't{a}'], simpan[f'k{a}'] = out[a]
    np.savez_compressed(CAND, **simpan)
    return out


# ---------------------------------------------------------------- keluar
def hari_keluar(M, ti, e, kc, cache):
    """(idx_jual, px_jual) — syarat keluar pertama pada/selepas e, jual buka bar BERIKUTNYA."""
    kunci = (ti, e, kc)
    if kunci in cache:
        return cache[kunci]
    akhir = M['C'].shape[1] - 1
    hi = min(e + min(HAD_IMBAS, TMAX), akhir)
    r = RULE[kc]
    if r == 'X13':
        w = M['rsi14'][ti, e:hi + 1]
        kena = np.flatnonzero(np.isfinite(w) & (w > 70.0))
    elif r == 'X14':
        w = M['rsi14'][ti, e - 1:hi + 1].astype('float64')
        naik = np.isfinite(w[1:]) & np.isfinite(w[:-1]) & (w[1:] > 50) & (w[:-1] <= 50)
        kena = np.flatnonzero(naik)
    elif r == 'X15':
        atr = float(M['A'][ti, e - 1])
        c = M['C'][ti, e:hi + 1].astype('float64')
        sah = np.isfinite(c)
        puncak = np.maximum.accumulate(np.where(sah, c, -np.inf))
        kena = np.flatnonzero(sah & (c < puncak - TRAIL_ATR * atr)) if np.isfinite(atr) else np.array([], int)
    elif r == 'X16':
        w = M['supertrend'][ti, e:hi + 1]
        kena = np.flatnonzero(np.isfinite(w) & (w <= 0))
    elif r == 'X17':
        w = M['adx14'][ti, e:hi + 1]
        kena = np.flatnonzero(np.isfinite(w) & (w < 20.0))
    else:                                     # X36 — DUA tutup berturut bawah ma50
        c = M['C'][ti, e - 1:hi + 1].astype('float64')
        ma = M['ma50'][ti, e - 1:hi + 1].astype('float64')
        b = np.isfinite(c) & np.isfinite(ma) & (c < ma)
        kena = np.flatnonzero(b[1:] & b[:-1])
    bar = e + int(kena[0]) if kena.size else hi
    k = min(bar + 1, akhir)
    if np.isfinite(M['O'][ti, k]) and M['O'][ti, k] > 0:
        px = float(M['O'][ti, k])
    else:
        sah = np.flatnonzero(np.isfinite(M['C'][ti, e:akhir + 1]))
        k = e + int(sah[-1]) if sah.size else e
        px = float(M['C'][ti, k])
    hasil = (int(k), px)
    cache[kunci] = hasil
    return hasil


# ---------------------------------------------------------------- simulasi
def simulasi(M, U, CAL, slot, urut, benih, had_slot=True):
    """Ekuiti harian, pendedahan harian, bilangan dagangan. slot=None -> kolam penuh."""
    rng = np.random.default_rng(benih)
    m = M['C'].shape[1]
    cache = {}
    tunai, prev, n_dag = 1.0, 1.0, 0
    buka = []                                  # (ti, kc, unit, idx_jual, px_jual)
    ek = np.full(m, np.nan)
    dz = np.full(m, np.nan)
    for d in range(1, m):
        if buka:
            for p in [x for x in buka if x[3] == d]:
                tunai += p[2] * p[4] * (1 - K.kos_sisi(M['N'][p[0], d]))
                buka.remove(p)
        a = d - 1
        c = CAL.get(a)
        if c is not None and c[0].size and (not had_slot or len(buka) < slot):
            ti_a, kc_a = c
            # kelayakan: harga buka esok sah, cair
            ok = (np.isfinite(M['O'][ti_a, d]) & (M['O'][ti_a, d] > 0) &
                  np.isfinite(M['N'][ti_a, a]) & (M['N'][ti_a, a] >= PB.CAIR))
            ti_a, kc_a = ti_a[ok], kc_a[ok]
            if ti_a.size:
                if urut == 'U01':
                    o = rng.permutation(ti_a.size)
                elif urut == 'U14':
                    o = np.argsort(-U[ti_a, a], kind='stable')
                elif urut == 'U08':
                    o = np.argsort(np.nan_to_num(M['A'][ti_a, a] / np.maximum(M['C'][ti_a, a], 1e-9),
                                                 nan=9e9), kind='stable')
                else:                           # U02 proksi RS = momentum 6 bulan
                    o = np.argsort(-U[ti_a, a], kind='stable')
                ti_a, kc_a = ti_a[o], kc_a[o]
                ada = {(x[0], x[1]) for x in buka}
                n_slot = slot if had_slot else max(1, ti_a.size)
                for ti, kc in zip(ti_a.tolist(), kc_a.tolist()):
                    if had_slot and len(buka) >= slot:
                        break
                    if (ti, kc) in ada:
                        continue
                    belanja = min(prev / n_slot, tunai)
                    if belanja <= 1e-12:
                        break
                    kx, pj = hari_keluar(M, ti, d, kc, cache)
                    if kx <= d:
                        continue
                    px = float(M['O'][ti, d])
                    unit = belanja * (1 - K.kos_sisi(M['N'][ti, a])) / px
                    tunai -= belanja
                    buka.append((ti, kc, unit, kx, pj))
                    ada.add((ti, kc))
                    n_dag += 1
        nilai = tunai
        for ti, _, unit, _, _ in buka:
            cc = M['C'][ti, d]
            if np.isfinite(cc):
                nilai += unit * float(cc)
        ek[d] = prev = nilai
        dz[d] = 1.0 - (tunai / nilai if nilai > 0 else 1.0)
    return ek, dz, n_dag


# ---------------------------------------------------------------- larian
def tingkap(M, ek, dz):
    """Metrik tingkap TAHAN. PB.cagr mahu ARRAY tarikh (ia buat hari[ok] dan
    (n[-1]-n[0]).days), BUKAN kiraan hari — itu pepijat kedua yang larian pertama dedahkan."""
    t = pd.to_datetime(M['tarikh'])
    sel = np.asarray((t >= UJI0) & (t <= UJI1))
    e = np.asarray(ek)[sel]
    hari = t[sel]
    ok = np.isfinite(e)
    if ok.sum() < 50:
        return dict(cagr=np.nan, mdd=np.nan, nisbah=np.nan, dedah=np.nan)
    e0 = e[ok][0]
    if not (e0 > 0):
        return dict(cagr=np.nan, mdd=np.nan, nisbah=np.nan, dedah=np.nan)
    cg = PB.cagr(e / e0, hari)
    md = PB.mdd(np.concatenate([[1.0], e[ok] / e0]))
    return dict(cagr=cg, mdd=md, nisbah=cg / abs(md) if md and np.isfinite(md) else np.nan,
                dedah=float(np.nanmean(dz[sel]) * 100))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', type=int, default=N_BENIH)
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    p94, p36 = kohort()
    print(f'kohort: {len(p94)} kombinasi, {len(p36)} wakil kelompok', flush=True)
    M = matriks()
    print('matriks siap', flush=True)
    U = u14_matriks(M['C'])
    C94 = calon(p94)
    print(f'calon: {len(C94)} hari dengan isyarat', flush=True)
    set36 = {(m_, k_) for m_, k_ in p36}
    kod36 = {RID[k_] for _, k_ in p36}
    masuk36 = {m_ for m_, _ in p36}
    # C36 ditapis daripada C94 memakai pasangan yang sama — tiada larian topeng kedua
    C36 = {}
    P94set = set(p94)
    del P94set
    for d_, (ti_, kc_) in C94.items():
        keep = np.isin(kc_, list(kod36))
        if keep.any():
            C36[d_] = (ti_[keep], kc_[keep])
    del set36, masuk36

    R = []
    t0 = time.time()

    def lari(nama, CAL, slot, urut, benih, had=True):
        ek, dz, nd = simulasi(M, U, CAL, slot, urut, benih, had_slot=had)
        r = tingkap(M, ek, dz)
        r.update(lengan=nama, slot=('penuh' if not had else slot), urut=urut,
                 benih=benih, n_dag=nd)
        R.append(r)
        print(f"  [{time.time() - t0:.0f}s] {nama:8s} slot={r['slot']:>5} {urut} b{benih:<3} "
              f"CAGR {r['cagr']:+7.2f}%  MDD {r['mdd']:+7.2f}%  nisbah {r['nisbah']:.2f}  "
              f"dedah {r['dedah']:.0f}%  n {nd}", flush=True)
        return r

    for slot in (8, 40):
        lari('P94', C94, slot, 'U14', 0)
        lari('P36', C36, slot, 'U14', 0)
    lari('PENUH', C94, None, 'U14', 0, had=False)
    for slot in (8, 40):
        for b in range(a.benih):
            lari('RAWAK', C94, slot, 'U01', b)
    for urut in ('U01', 'U02', 'U08'):
        lari('UKAWAL', C94, 8, urut, 0)

    d = pd.DataFrame(R)
    d.to_csv(KELUAR / 'portfolio_94.csv', index=False)
    laporan(d)
    return 0


def laporan(d):
    L = ['# Portfolio 94 kombinasi produksi lawan SPUS', '',
         'Pradaftar `REVERSE/SPEC_PORTFOLIO_94.md` — dikomit sebelum keputusan dilihat.',
         f'Penanda aras SPUS: CAGR {SPUS_CAGR:+.2f}%  MDD {SPUS_MDD:+.2f}%  '
         f'nisbah {SPUS_CAGR / abs(SPUS_MDD):.3f}', '']
    rw = d[d.lengan == 'RAWAK']
    jalur = {s: (np.nanpercentile(g.cagr, 5), np.nanpercentile(g.cagr, 95))
             for s, g in rw.groupby('slot')}
    L += ['## Keputusan', '',
          '| Lengan | Slot | Urutan | CAGR | MDD | Nisbah | Dedah | Dagangan | P1 | P2 | P3 | P4 | T1 |',
          '|---|---|---|--:|--:|--:|--:|--:|:-:|:-:|:-:|:-:|:-:|']
    for _, r in d[d.lengan != 'RAWAK'].iterrows():
        p1 = r.cagr > SPUS_CAGR
        p2 = r.mdd >= SPUS_MDD
        p3 = r.cagr > jalur.get(r.slot, (np.nan, np.nan))[1]
        p4 = r.nisbah > AMBANG_NISBAH
        y = lambda b: '✓' if b else '✗'  # noqa: E731
        L.append(f'| {r.lengan} | {r.slot} | {r.urut} | {r.cagr:+.2f}% | {r.mdd:+.2f}% | '
                 f'{r.nisbah:.2f} | {r.dedah:.0f}% | {int(r.n_dag)} | {y(p1)} | {y(p2)} | '
                 f'{y(p3)} | {y(p4)} | {y(p1 and p2)} |')
    L += ['', '## Jalur kawalan RAWAK (20 benih)', '',
          '| Slot | p5 | median | p95 |', '|---|--:|--:|--:|']
    for s, g in rw.groupby('slot'):
        L.append(f'| {s} | {np.nanpercentile(g.cagr, 5):+.2f}% | '
                 f'{np.nanmedian(g.cagr):+.2f}% | {np.nanpercentile(g.cagr, 95):+.2f}% |')
    (KELUAR / 'PORTFOLIO_94.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L[:12]))


if __name__ == '__main__':
    raise SystemExit(main())
