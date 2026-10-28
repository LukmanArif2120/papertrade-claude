"""DIAGNOSIS fasa 1 — siling pandangan sempurna: portfolio 8 slot yang MEMILIH DENGAN SEMPURNA.

Hadapan: antara run yang tarikh_sahnya hari ini, pilih yang %_naik_dagang tertinggi; keluar
tepat pada tarikh_puncak. Ini bukan strategi - ia had atas mutlak bagi pemilihan.
Kos penuh dikenakan kedua-dua sisi (0.1% komisen + 0.1% slippage anggaran sederhana).
"""
import pandas as pd
import numpy as np
from pathlib import Path
R = Path('/home/user/papertrade-claude/REVERSE')
KOS = 0.002  # satu sisi, anggaran pertengahan (slippage 0.1%)
SLOT = 8

print('Siling pandangan sempurna, portfolio 8 slot x 12.5%, kos penuh dua sisi\n')
out = []
for y in (2020, 2021, 2022, 2023, 2024, 2025):
    d = pd.read_csv(R / f'runs_{y}.csv')
    d = d[(d.entry_sah == 'ya') & (d.sebab_kecuali.isna() | (d.sebab_kecuali == ''))].copy()
    d['tarikh_sah'] = pd.to_datetime(d.tarikh_sah)
    d['tarikh_puncak'] = pd.to_datetime(d.tarikh_puncak)
    d['naik'] = pd.to_numeric(d.pct_naik_dagang, errors='coerce')
    d = d[np.isfinite(d.naik)].sort_values(['tarikh_sah', 'naik'], ascending=[True, False])
    hari = pd.date_range(f'{y}-01-01', f'{y}-12-31', freq='B')
    ekuiti, slot, siri, n_dag = 1.0, [], [], 0
    peta = {t: g for t, g in d.groupby('tarikh_sah')}
    for h in hari:
        baki = []
        for p in slot:
            if p['keluar'] <= h:
                ekuiti += p['nilai'] * (1 + p['naik'] / 100.0) * (1 - KOS) ** 2 - p['nilai']
                n_dag += 1
            else:
                baki.append(p)
        slot = baki
        if h in peta:
            calon = peta[h]
            for _, r in calon.iterrows():
                if len(slot) >= SLOT:
                    break
                if any(p['ticker'] == r.ticker for p in slot):
                    continue
                slot.append(dict(ticker=r.ticker, nilai=ekuiti * 0.125, naik=r.naik,
                                 keluar=r.tarikh_puncak))
        siri.append((h, ekuiti))
    s = pd.Series([e for _, e in siri], index=[t for t, _ in siri])
    bl = s.resample('ME').last().pct_change()
    bl.iloc[0] = s.resample('ME').last().iloc[0] / 1.0 - 1
    bl = bl.dropna() * 100
    out.append(dict(tahun=y, n_dagangan=n_dag, pulangan_tahun=round((s.iloc[-1] - 1) * 100, 1),
                    median_bulanan=round(float(bl.median()), 2),
                    purata_bulanan=round(float(bl.mean()), 2),
                    pct_bulan_ge10=round(float((bl >= 10).mean() * 100), 1),
                    bulan_terburuk=round(float(bl.min()), 2),
                    n_calon_setahun=len(d)))


print(pd.DataFrame(out).to_string(index=False))
o = pd.DataFrame(out)
print(f'\nPurata siling: pulangan {o.pulangan_tahun.mean():.1f}%/tahun, '
      f'median bulanan {o.median_bulanan.mean():.2f}%')
print(f'Tahun yang siling mencapai median >= +10%/bulan: '
      f'{int((o.median_bulanan >= 10).sum())}/{len(o)}')
