# Sahkan modul pengeluaran calon K145+ (BacktestShariah2/kod/kaedah/Mxx.py) dan jana registry v1.2.
# 1) dagangan modul = dagangan WFO (Kaedah.dagangan) bagi gabungan beku yang sama (bait demi bait);
# 2) registry set 431 + S1–S4 melalui tambahan.baris2 (enjin v1.2 asal) → kod/registry/Mxx.csv.
#   python3 WFO/kod/registry_baru.py M115 ... M161
import os, sys, importlib, warnings
from multiprocessing import Pool
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
import wfo, enjin
from sahkan_enjin import sama_T
KOD = wfo.KOD; REG = os.path.join(KOD, 'registry')


def satu(mid):
    warnings.filterwarnings('ignore')
    import tambahan
    fr, idx, _ = wfo.muat_data(buang8=False)
    d = pd.concat([pd.read_csv(os.path.join(wfo.DATA, f'dataset_S{i}.csv'), usecols=['ticker']).drop_duplicates().assign(s=f'S{i}') for i in range(1, 5)])
    asal = dict(zip(d.ticker, d.s))
    spec = importlib.util.spec_from_file_location(f'kaedah.{mid}', os.path.join(KOD, 'kaedah', mid + '.py'))
    m = importlib.util.module_from_spec(spec); sys.modules[f'kaedah.{mid}'] = m; spec.loader.exec_module(m)
    f = wfo.salin(fr); m.sedia(f, idx); f = {t: enjin.siap(g) for t, g in f.items()}
    T = enjin.trades(f, m.TMAX, m.WARM)
    # 1) banding dengan WFO (alam 423, modul kaedah_baru + gabungan sama)
    fr423 = {t: g for t, g in fr.items() if t not in wfo.BUANG8}
    k = wfo.Kaedah(mid, fr423, idx)
    W = k.dagangan(m.HENTI_KOD, m.KELUAR_KOD, m.TMAX or 0)
    P = T[~T.ticker.isin(wfo.BUANG8)].reset_index(drop=True)
    ok, why = sama_T(W.reset_index(drop=True), P)
    # 2) registry
    rows = []
    for s in ['431', 'S1', 'S2', 'S3', 'S4']:
        frs = tambahan.subset(f, asal, s)
        Ts = T if s == '431' else T[T.ticker.isin(frs)]
        cv = enjin.portfolio(Ts, frs)
        rows.append(tambahan.baris2(s, mid, m.NAMA, m.VARIAN, Ts, cv, frs, idx, m.ADA_HENTI,
                                    catatan=f'Calon K145+; entry katalog + henti {m.HENTI_KOD}, keluar {m.KELUAR_KOD}, tmax {m.TMAX} (pilihan WFO 2026S4, dalam sampel)'))
    pd.DataFrame(rows)[tambahan.LAJUR2].to_csv(os.path.join(REG, mid + '.csv'), index=False)
    r = rows[0]
    return mid, ok, why, len(T), r['keputusan'], r['cagr'], r['mdd']


if __name__ == '__main__':
    with Pool(4) as p:
        for mid, ok, why, n, k, c, d in p.imap_unordered(satu, sys.argv[1:]):
            print(mid, 'SAMA' if ok else 'BEZA ' + why, n, k, round(c, 3), round(d, 3), flush=True)
