# QC data AUTOTUNE

- Tarikan: 2026-10-17T13:59Z; julat bar 2009-01-02 hingga 2026-10-16
- Calon: 5374; dimuat turun (ada data, termasuk SPY/QQQ): 5376; gagal: 0
- Bar dibuang (harga <=0/NaN/high<low): 7222
- Ticker ditanda (>5 hari |pulangan|>50%, dikeluarkan): 605 (cth AACG, ABAT, ABTS, ABVC, ACB, ACCS, ACON, ACRS)
- Ticker pernah dalam universe (disimpan dalam harga_*.parquet): 3227
- Ticker unik dalam universe: 3227; baris universe: 332417
- Kumpulan (ticker pernah dalam universe): A=1653, B=1574; purata sebulan A=829, B=792
- Saiz aset Release: 216 MB

Saiz universe sebulan mengikut tahun berkuat kuasa (min / median / maks):

| Tahun | min | median | maks |
|---|---|---|---|
| 2009 | 853 | 861 | 870 |
| 2010 | 887 | 954 | 998 |
| 2011 | 989 | 1075 | 1098 |
| 2012 | 1027 | 1074 | 1097 |
| 2013 | 1117 | 1212 | 1310 |
| 2014 | 1326 | 1383 | 1421 |
| 2015 | 1431 | 1464 | 1485 |
| 2016 | 1433 | 1486 | 1579 |
| 2017 | 1614 | 1648 | 1728 |
| 2018 | 1737 | 1770 | 1821 |
| 2019 | 1718 | 1806 | 1840 |
| 2020 | 1665 | 1861 | 1956 |
| 2021 | 2000 | 2000 | 2000 |
| 2022 | 2000 | 2000 | 2000 |
| 2023 | 2000 | 2000 | 2000 |
| 2024 | 2000 | 2000 | 2000 |
| 2025 | 2000 | 2000 | 2000 |
| 2026 | 2000 | 2000 | 2000 |

Nota: median nilai dagangan 60 hari memerlukan >= 50 bar sah; ticker ditanda dan ticker yang tidak pernah layak dibuang daripada harga_*.parquet (senarai penuh dalam qc.csv). Tiada saham delist (bias survivorship).
