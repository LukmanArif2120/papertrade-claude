# QC data AUTOTUNE A02

- Tarikan: 2026-10-18T08:59Z; julat bar 2009-01-02 hingga 2026-10-16
- Calon: 5374; dimuat turun (ada data, termasuk SPY/QQQ): 5376; gagal: 0
- Ticker dengan sekurang-kurangnya satu split: 1906 (lajur faktor_split; harga kekal auto_adjust)
- Bar dibuang: 8597 (harga tidak sah 7224, high<low 0, lonjakan >40% yang berbalik 1373); senarai penuh dalam qc.csv
- Tiada ticker dibuang kerana kemeruapan
- Ticker pernah dalam universe (disimpan dalam harga_*.parquet): 3260
- Baris universe: 333368; kumpulan (ticker pernah dalam universe): A=1673, B=1587; purata sebulan A=829, B=797
- Saiz aset Release: 218 MB

Saiz universe sebulan mengikut tahun berkuat kuasa (min / median / maks):

| Tahun | min | median | maks |
|---|---|---|---|
| 2009 | 937 | 944 | 951 |
| 2010 | 969 | 1025 | 1051 |
| 2011 | 1047 | 1119 | 1140 |
| 2012 | 1081 | 1118 | 1140 |
| 2013 | 1156 | 1238 | 1320 |
| 2014 | 1343 | 1384 | 1416 |
| 2015 | 1433 | 1460 | 1486 |
| 2016 | 1421 | 1475 | 1563 |
| 2017 | 1591 | 1632 | 1700 |
| 2018 | 1704 | 1742 | 1796 |
| 2019 | 1691 | 1773 | 1813 |
| 2020 | 1638 | 1832 | 1940 |
| 2021 | 1989 | 2000 | 2000 |
| 2022 | 2000 | 2000 | 2000 |
| 2023 | 2000 | 2000 | 2000 |
| 2024 | 2000 | 2000 | 2000 |
| 2025 | 2000 | 2000 | 2000 |
| 2026 | 2000 | 2000 | 2000 |

Semakan keahlian universe (kedudukan ikut median nilai dagangan; "-" = tiada):

| Ticker | 2013-06 | 2016-06 | 2019-06 |
|---|---|---|---|
| NVDA | 176 | 59 | 9 |
| AAPL | 2 | 1 | 2 |
| TSLA | 107 | 8 | 6 |
| AVGO | 316 | 61 | 40 |
| NFLX | 10 | 6 | 7 |
| ANET | - | 490 | 141 |
| SMCI | 1207 | 957 | 1564 |
| CMG | 131 | 26 | 69 |

Nota: harga universe = close dilaras x faktor_split (tidak dilaras split, tetapi masih dilaras dividen); median 60 hari memerlukan >= 50 bar sah. Tiada saham delist (bias survivorship; had atas).
