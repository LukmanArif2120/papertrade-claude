# Semakan keteguhan kaedah M: H1 (1 Nov 2019 – 31 Dis 2022) lawan H2 (1 Jan 2023 – hujung data).
# Guna:  python3 BacktestShariah2/standard/semak_h1_h2.py [--out BacktestShariah2/laporan/SEMAKAN_H1_H2.md]
# Sumber: data/registry_M_gabung.csv (lajur h1, h2 = CAGR portfolio 8 slot enjin v1.2 bagi setiap separuh)
#         + data_mentah/ (penanda aras EW, SPY, QQQ dikira dengan enjin.penanda()). Enjin TIDAK diubah.
import sys, os, argparse
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(AKAR, 'kod'))
from enjin import penanda, START, H1_END

MENTAH = os.path.join(os.path.dirname(AKAR), 'data_mentah')


def muat_mentah():
    fr = {}
    for s in ['S1', 'S2', 'S3', 'S4']:
        d = pd.read_csv(os.path.join(MENTAH, f'dataset_{s}.csv')); d['date'] = pd.to_datetime(d.date.astype(str))
        for t, g in d.groupby('ticker'): fr[t] = g.sort_values('date').set_index('date')
    ix = pd.read_csv(os.path.join(MENTAH, 'index_benchmark.csv')); ix['date'] = pd.to_datetime(ix.date.astype(str))
    idx = {t: g.sort_values('date').set_index('date') for t, g in ix.groupby('ticker')}
    return fr, idx


def pilih(g):
    """Varian dipilih (tugasan_v3 §3): skor tertinggi bukan DITOLAK; jika tiada, CAGR tertinggi."""
    ok = g[g.keputusan != 'DITOLAK']
    return ok.loc[ok.skor.astype(float).idxmax()] if len(ok) else g.loc[g.cagr.idxmax()]


def pct(x): return '' if pd.isna(x) else f'{x * 100:.1f}%'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(AKAR, 'laporan', 'SEMAKAN_H1_H2.md'))
    a = ap.parse_args()

    fr, idx = muat_mentah(); B = penanda(idx, fr)
    ew1, ew2 = B['Sama rata 100']['h1'], B['Sama rata 100']['h2']
    reg = pd.read_csv(os.path.join(AKAR, 'data', 'registry_M_gabung.csv'))
    reg['set'] = reg['set'].astype(str)
    r431 = reg[reg.set == '431'].copy()
    sub = reg[reg.set != '431']

    # 1. Varian dipilih bagi setiap kaedah (penuh) dan konsistensi lawan EW setiap separuh
    rows = []
    for mid, g in r431.groupby('id'):
        p = pilih(g)
        s = sub[(sub.id == mid) & (sub.varian == p.varian)]
        s_menang = int(s.menang_ew.astype(str).str.lower().eq('true').sum()) if len(s) else None
        # Pilihan berasaskan H1 sahaja (tanpa melihat H2): varian bukan gagal G1/G2/G4/G6 dengan h1 tertinggi
        gh = g[~g.gate_gagal.fillna('').str.contains('G1|G2|G4|G6')]
        ph = (gh if len(gh) else g).sort_values('h1', ascending=False).iloc[0]
        kep = p.keputusan + (f' ({p.gate_gagal})' if isinstance(p.gate_gagal, str) and p.gate_gagal else '')
        rows.append(dict(id=mid, kaedah=p.kaedah, varian=p.varian, keputusan=kep,
                         skor=p.skor, cagr=p.cagr, h1=p.h1, h2=p.h2, lebih1=p.h1 - ew1, lebih2=p.h2 - ew2,
                         subset=s_menang, n_subset=len(s), nvar=len(g), h2_pilih_h1=ph.h2, varian_h1=ph.varian, beza_varian=ph.varian != p.varian))
    D = pd.DataFrame(rows)
    D['menang'] = (D.lebih1 > 0).astype(int) + (D.lebih2 > 0).astype(int)
    D['minlebih'] = D[['lebih1', 'lebih2']].min(axis=1)

    def label(r):
        if r.menang == 2 and (r.subset is None or r.subset >= 3): return 'TEGUH'
        if r.menang == 2: return 'TEGUH (subset lemah)'
        if r.menang == 1: return 'SATU SEPARUH'
        return 'LEMAH'
    D['label'] = D.apply(label, axis=1)
    D = D.sort_values(['menang', 'minlebih'], ascending=False).reset_index(drop=True)

    # 2. Bias pemilihan: H2 bagi varian dipilih guna data penuh lawan varian dipilih guna H1 sahaja
    bias = (D.h2 - D.h2_pilih_h1)
    # 3. Korelasi kedudukan H1 lawan H2 (semua 550 varian dan 88 varian dipilih)
    rho_all = r431.h1.rank().corr(r431.h2.rank())
    rho_sel = D.h1.rank().corr(D.h2.rank())
    # 4. Pilih 10 teratas ikut H1 sahaja -> prestasi H2
    t10 = D.sort_values('h1', ascending=False).head(10)
    t10_lulus = int((t10.h2 > ew2).sum())

    L = []
    w = L.append
    w('# Semakan Keteguhan H1 lawan H2 (Kaedah M, set 431)\n')
    w(f'Dijana oleh `standard/semak_h1_h2.py` daripada `data/registry_M_gabung.csv` (enjin v1.2, tanpa larian semula). '
      f'H1 = {START} hingga {H1_END}; H2 = 2023-01-01 hingga hujung data. CAGR portfolio 8 slot × 12.5%.\n')
    w('## Penanda aras\n')
    for k in ['Sama rata 100', 'SPY', 'QQQ']:
        w(f'- {"EW (sama rata 431)" if k == "Sama rata 100" else k}: H1 {pct(B[k]["h1"])}, H2 {pct(B[k]["h2"])}, penuh {pct(B[k]["cagr"])}')
    w('')
    w('## Takrif label\n')
    w('- **TEGUH**: CAGR mengalahkan EW dalam H1 DAN H2, dan menang EW dalam ≥ 3/4 subset S1–S4.')
    w('- **TEGUH (subset lemah)**: menang EW dalam kedua-dua separuh tetapi < 3/4 subset.')
    w('- **SATU SEPARUH**: menang EW dalam satu separuh sahaja (kemungkinan bergantung pada rejim pasaran).')
    w('- **LEMAH**: kalah EW dalam kedua-dua separuh.')
    w('- Kedudukan: bilangan separuh menang, kemudian lebihan minimum atas EW (separuh yang lebih lemah).\n')
    w('## Ringkasan\n')
    for k, v in D.label.value_counts().items(): w(f'- {k}: {v} kaedah')
    w(f'- Korelasi kedudukan (Spearman) H1 lawan H2: {rho_all:.2f} (550 varian), {rho_sel:.2f} (88 varian dipilih). '
      'Hampir 0 = prestasi H1 tidak meramal H2; ≥ 0.5 = konsisten.')
    w(f'- 10 kaedah teratas ikut H1 sahaja: {t10_lulus}/10 mengalahkan EW dalam H2; median H2 {pct(t10.h2.median())} '
      f'(EW {pct(ew2)}).')
    w(f'- Bias pemilihan varian: median H2 varian dipilih (data penuh) {pct(D.h2.median())} lawan varian dipilih '
      f'ikut H1 sahaja {pct(D.h2_pilih_h1.median())}; {int(D.beza_varian.sum())}/88 kaedah memilih varian berbeza, '
      f'dan bagi kaedah itu purata H2 jatuh {pct(bias[D.beza_varian].mean())}. '
      'Beza positif = sebahagian prestasi H2 datang daripada memilih varian selepas melihat H2.\n')
    w('## Kedudukan semua kaedah\n')
    w('| # | ID | Kaedah | Keputusan | Skor | H1 | H2 | H1−EW | H2−EW | Subset menang EW | Label | H2 jika pilih ikut H1 |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for i, r in D.iterrows():
        sb = f'{r.subset}/{r.n_subset}' if r.n_subset else '–'
        w(f'| {i + 1} | {r.id} | {r.kaedah} | {r.keputusan} | {r.skor if pd.notna(r.skor) else ""} | {pct(r.h1)} | {pct(r.h2)} | '
          f'{pct(r.lebih1)} | {pct(r.lebih2)} | {sb} | {r.label} | {pct(r.h2_pilih_h1)} |')
    w('\n## Had\n')
    w('- Bias survivorship: set 431 ialah senarai Shariah semasa; saham delist atau dahulu bukan Shariah tiada. '
      'Ia menaikkan CAGR semua kaedah dan EW, jadi perbandingan relatif lawan EW kurang terjejas.')
    w('- H1 dan H2 bukan ujian luar sampel sebenar: spec kaedah dan varian disusun selepas data 2019–2026 dilihat.')
    w('- Subset S1–S4 hanya ada bagi satu varian setiap kaedah; "–" = tiada baris subset bagi varian dipilih.')
    open(a.out, 'w').write('\n'.join(L) + '\n')
    print(f'Ditulis {a.out}: ' + ', '.join(f'{k} {v}' for k, v in D.label.value_counts().items()) +
          f'; rho {rho_all:.2f}/{rho_sel:.2f}; H1 top10 lulus H2 {t10_lulus}/10')


if __name__ == '__main__':
    main()
