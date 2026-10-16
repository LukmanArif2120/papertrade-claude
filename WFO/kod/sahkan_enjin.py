# Sahkan enjin_laju setara bait demi bait dengan enjin v1.2 bagi semua kaedah M.
# Bagi setiap kaedah: tetapan asal + 3 gabungan rawak stop/exit/tmax; trades() dibanding semua lajur,
# portfolio() dibanding atas data penuh dan satu tetingkap latihan (2020–2022, selepas potong()).
#   python3 WFO/kod/sahkan_enjin.py [M01 M02 ...]   → WFO/laporan/ENJIN_LAJU_SAHKAN.md
import os, sys, json, random, warnings, importlib
from multiprocessing import Pool
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
import wfo, enjin, enjin_laju as L

KELUAR = os.path.join(ROOT, '..', 'laporan', 'ENJIN_LAJU_SAHKAN.md')
MA, ZA = pd.Timestamp('2020-01-01'), pd.Timestamp('2022-12-31')


def sama_T(A, B):
    if len(A) == 0 and len(B) == 0: return True, ''
    if len(A) != len(B): return False, f'n {len(A)} lawan {len(B)}'
    for k in ('ticker', 'why'):
        if not (np.asarray(A[k], object) == np.asarray(B[k], object)).all(): return False, k
    for k in ('sig', 'ent', 'ex'):
        if not (pd.to_datetime(A[k]).values == pd.to_datetime(B[k]).values).all(): return False, k
    if not (A.days.values == B.days.values).all(): return False, 'days'
    for k in ('ret', 'rank', 'mfe'):
        if not np.array_equal(A[k].values.astype(float), B[k].values.astype(float), equal_nan=True): return False, k
    return True, ''

def sama_cv(a, b):
    return len(a) == len(b) and (a.index == b.index).all() and np.array_equal(a.values, b.values, equal_nan=True)


def satu(mid):
    warnings.filterwarnings('ignore')
    try:
        fr, idx, _ = wfo.muat_data()
        m = importlib.import_module(mid)
        f = wfo.salin(fr); m.sedia(f, idx); f = {t: enjin.siap(g) for t, g in f.items()}
        rng = random.Random(int(mid[1:]))
        cfg = [('ASAL', 'ASAL', m.TMAX or 0, True)] + [(rng.choice(wfo.STOPS), rng.choice(wfo.EXITS), rng.choice(wfo.TMAXS), False)
                                                       for _ in range(3)]
        frw = {t: g[(g.index >= MA) & (g.index <= ZA)] for t, g in fr.items()}
        frw = {t: g for t, g in frw.items() if len(g)}
        P, Pw = L.Pasaran(f), L.Pasaran(frw)
        hasil = []
        for s, e, x, asal in cfg:
            if asal: h = f
            else:
                h = {}
                for t, g in f.items():
                    ex, tg = wfo.lajur_exit(g, e, g.exitc, g.tgt)
                    h[t] = g.assign(stop=wfo.lajur_stop(g, s, g.stop), exitc=ex, tgt=tg)
            A = enjin.trades(h, x or None, m.WARM); B = L.trades_laju(h, x or None, m.WARM)
            ok, why = sama_T(A, B); n = len(A); cv1 = cv2 = True
            if ok and n:
                cv1 = sama_cv(enjin.portfolio(A, f), P.lengkung(B))
                Ap, Bp = wfo.potong(A, MA, ZA, fr), wfo.potong(B, MA, ZA, fr)
                cv2 = len(Ap) == 0 or sama_cv(enjin.portfolio(Ap, frw), Pw.lengkung(Bp))
            hasil.append(dict(cfg=f'{s}/{e}/{x}', n=n, trades=ok, beza=why, penuh=cv1, tetingkap=cv2))
        return mid, hasil, None
    except Exception as ex:
        return mid, [], f'{type(ex).__name__}: {ex}'


def main(mids):
    out = {}
    with Pool(4) as p:
        for mid, h, err in p.imap_unordered(satu, mids):
            out[mid] = (h, err); ok = not err and all(r['trades'] and r['penuh'] and r['tetingkap'] for r in h)
            print(mid, 'SAMA' if ok else 'BEZA/RALAT', err or '', flush=True)
    sem = sorted(out, key=lambda x: int(x[1:]))
    lulus = [k for k in sem if not out[k][1] and all(r['trades'] and r['penuh'] and r['tetingkap'] for r in out[k][0])]
    ujian = sum(len(out[k][0]) for k in sem)
    L_ = ['# Pengesahan enjin laju lawan enjin v1.2', '',
          f'Kaedah disemak: {len(sem)}. Sama bait demi bait (semua gabungan): **{len(lulus)}/{len(sem)}**. '
          f'Jumlah gabungan diuji: {ujian} (tetapan asal + 3 rawak setiap kaedah).', '',
          'Setiap gabungan: `trades()` dibanding semua lajur (ticker, sig, ent, ex, ret, days, why, rank, mfe; float tepat, NaN = NaN); '
          '`portfolio()` dibanding atas data penuh dan tetingkap 2020–2022 selepas `potong()`.', '',
          '| Kaedah | Gabungan | n | trades | portfolio penuh | portfolio tetingkap |', '|---|---|---|---|---|---|']
    for k in sem:
        h, err = out[k]
        if err: L_.append(f'| {k} | RALAT: {err} | | | | |'); continue
        for r in h:
            b = lambda v: 'sama' if v else '**BEZA**'
            L_.append(f"| {k} | {r['cfg']} | {r['n']} | {b(r['trades'])}{' ' + r['beza'] if r['beza'] else ''} | {b(r['penuh'])} | {b(r['tetingkap'])} |")
    open(KELUAR, 'w').write('\n'.join(L_) + '\n')
    print(f'{len(lulus)}/{len(sem)} sama; ditulis {KELUAR}')


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a if a else [m for m in wfo.semua_kaedah() if m not in wfo.DIKECUALI])
