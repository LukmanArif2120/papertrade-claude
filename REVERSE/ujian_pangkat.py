"""DIAGNOSIS fasa 1 — ujian PEMANGKATAN. Dua sasaran, perbezaan yang menentukan.

(A) %_naik_dagang run induk  -> hanya atas peristiwa yang MEMANG menjadi run (hindsight)
(B) pul_henti2atr            -> SEMUA peristiwa sah, kos + henti dikenakan (boleh didagangkan)
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import spearmanr
C = Path('/home/user/papertrade-claude/REVERSE/.cache')
TH = [2020, 2021, 2022, 2023, 2024, 2025]


def muat(y):
    sig = pd.read_parquet(C / f'signals_{y}.parquet')
    had = pd.read_parquet(C / f'hadapan_{y}.parquet')
    return sig[(sig.jenis_peristiwa != '') & (sig.dalam_univ == 1)].merge(
        had[['ticker', 'tarikh', 'pul_henti2atr']], on=['ticker', 'tarikh'], how='left')


kol = set.intersection(*[set(json.loads((C / f'kuintil_{y}.json').read_text())['simpan'])
                         for y in TH])
A, B, n_a, n_b = {}, {}, {}, {}
for y in TH:
    d = muat(y)
    da = d[(d.jenis_peristiwa == 'mula_run') & np.isfinite(d.run_dagang)]
    db = d[np.isfinite(d.pul_henti2atr)]
    n_a[y], n_b[y] = len(da), len(db)
    for k in kol:
        for nama, dd, sas in (('A', da, 'run_dagang'), ('B', db, 'pul_henti2atr')):
            x, v = dd[k].to_numpy('float64'), dd[sas].to_numpy('float64')
            m = np.isfinite(x) & np.isfinite(v)
            r = spearmanr(x[m], v[m])[0] if m.sum() > 200 else np.nan
            (A if nama == 'A' else B).setdefault(k, []).append(r)
print('n baris: (A) peristiwa yang menjadi run  vs  (B) semua peristiwa sah')
for y in TH:
    print(f'  {y}: A={n_a[y]:>5}  B={n_b[y]:>6}  (A ialah {n_a[y]/n_b[y]*100:.0f}% daripada B)')


def ring(D):
    rows = []
    for k, v in D.items():
        if any(not np.isfinite(x) for x in v):
            continue
        rows.append(dict(indikator=k, rho_purata=round(float(np.mean(v)), 3),
                         rho_min=round(min(v), 3), rho_maks=round(max(v), 3),
                         konsisten='ya' if (all(x > 0 for x in v) or all(x < 0 for x in v))
                         else 'tidak'))
    return pd.DataFrame(rows).sort_values('rho_purata', key=abs, ascending=False)


for nama, D in (('(A) sasaran = puncak run induk (HINDSIGHT)', A),
                ('(B) sasaran = pulangan boleh didagangkan (KAUSAL)', B)):
    d = ring(D)
    print(f'\n{nama}')
    print(d.head(8).to_string(index=False))
    print(f'  tanda konsisten 6/6 tahun: {int((d.konsisten == "ya").sum())}/{len(d)}'
          f' | |rho| purata tertinggi: {abs(d.rho_purata).max():.3f}')
    kon = d[d.konsisten == 'ya']
    if len(kon):
        print(f'  konsisten: ' + ', '.join(f'{r.indikator} ({r.rho_purata:+.3f})'
                                           for _, r in kon.iterrows()))
