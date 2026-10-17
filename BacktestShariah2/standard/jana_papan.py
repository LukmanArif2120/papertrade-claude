# Jana laporan/PAPAN_KEDUDUKAN_M.md daripada data/registry_M_gabung.csv (set 431; tiada larian semula).
# Guna: python3 BacktestShariah2/standard/jana_papan.py [--out BacktestShariah2/laporan/PAPAN_KEDUDUKAN_M.md]
# Varian dipilih (tugasan_v3 §3): skor tertinggi bukan DITOLAK; jika semua DITOLAK, CAGR tertinggi.
import os, argparse
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); AKAR = os.path.dirname(HERE)


def pct(x): return '' if pd.isna(x) else f'{x * 100:.1f}%'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(AKAR, 'laporan', 'PAPAN_KEDUDUKAN_M.md'))
    a = ap.parse_args()
    g = pd.read_csv(os.path.join(AKAR, 'data', 'registry_M_gabung.csv'))
    g = g[g['set'].astype(str) == '431']
    pil = []
    for _, d in g.groupby('id'):
        ok = d[d.keputusan != 'DITOLAK']
        pil.append(ok.loc[ok.skor.astype(float).idxmax()] if len(ok) else d.loc[d.cagr.idxmax()])
    P = pd.DataFrame(pil); P['_lulus'] = P.keputusan != 'DITOLAK'
    P = pd.concat([P[P._lulus].sort_values('skor', ascending=False), P[~P._lulus].sort_values('cagr', ascending=False)])
    k = P.keputusan.value_counts()
    L = ['# Papan Kedudukan Kaedah M (set 431, varian skor tertinggi)', '',
         f'Jana daripada data/registry_M_gabung.csv oleh `standard/jana_papan.py`. {len(P)} kaedah, {len(g)} varian diuji atas 431 saham. '
         f'Status terbaik setiap kaedah: DITOLAK {k.get("DITOLAK", 0)}, SIMPAN {k.get("SIMPAN", 0)}, UJI KERTAS {k.get("UJI KERTAS", 0)}, GUNA {k.get("GUNA", 0)}.', '',
         'Skor kosong = gagal gate (DITOLAK); bagi kaedah yang semua variannya DITOLAK, varian CAGR tertinggi dipaparkan (sebelum 17 Okt 2026: V0). Angka DALAM SAMPEL (1 Nov 2019 – 2 Okt 2026).', '',
         '| # | ID | Kaedah | Varian terbaik | Keputusan | Skor | CAGR | MDD | Win | Purata/dagangan | Hit10 | Menang EW |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(P.itertuples(), 1):
        sk = '' if pd.isna(r.skor) else f'{float(r.skor):.1f}'
        ew = 'Ya' if str(r.menang_ew) == 'True' else 'Tidak'
        L.append(f'| {i} | {r.id} | {r.kaedah} | {str(r.varian).replace("|", "\\|")} | {r.keputusan} | {sk} | {pct(r.cagr)} | {pct(r.mdd)} | {pct(r.win)} | {pct(r.avg)} | {pct(r.hit10)} | {ew} |')
    open(a.out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(a.out, len(P), 'kaedah')


if __name__ == '__main__':
    main()
