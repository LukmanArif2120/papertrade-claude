# LAPORAN REVERSE 2021 — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.

> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = **satu rejim pasaran**. Peta sektor bukan titik-masa. Gate 8.1 ada 5 tahun lain ([2020, 2022, 2023, 2024, 2025]); keputusan **maksimum CALON** (SPEC §11.8).

## 0. Jawapan ringkas

1. **4413 run layak** dikenal pasti dalam 2021; setiap 12 bulan ada calon (tiada "TIADA CALON"). 44 SUPER PADU (≥100%), 1598 PADU, 2771 BIASA.

2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada 315 run yang masih naik pada hari ke-63, **15.6% akhirnya melebihi +100%**, dengan median kenaikan penuh **59.9%** lawan 37.6% pada hari ke-63.

3. **Signal entry: TIADA CALON** daripada 27 yang masuk corong. 27 gagal gate bootstrap (G4) dan 27 ditanda BERGANTUNG PADA OUTLIER (G5). Ini keputusan, bukan kegagalan teknikal: tiada signal ENTRY tahun ini bertahan selepas had bawah 95% bootstrap blok dan ujian tanpa 5% pemenang teratas.

4. **196 daripada 234 sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan** — berbeza daripada tahun lain. Rujukan terbaik hanya -2.81% setiap dagangan ("jual hari ke-63"): -2.81% (jual hari ke-63), -3.42% (Chandelier 4×ATR14), -19.13% (pegang tanpa jual hingga hari ke-252). Apabila memegang tanpa jual tidak lagi menguntungkan, exit aktif baru berbaloi. **Perhatikan: ambang itu NEGATIF.** Mengalahkan rujukan yang merugikan hanya bermakna "kurang rugi", bukan untung — periksa lajur `jangkaan` dan `median_pulangan` setiap sistem, bukan hanya kedudukannya berbanding rujukan.

5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan pegang-252 hanya membuka **8 posisi sepanjang tahun** (8 slot terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. Pulangannya 12.28% ialah hasil **8 saham**, bukan sistem.

6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik ialah 1.02% sebulan (median) dengan MDD -22.16%.

7. **Keluarga EXIT dan SISTEM pada FDR:** 0/62 signal EXIT dan 173/234 sistem lulus q ≤ 0.01.

## 1. Semakan kesediaan Step 0

| Semakan | Hasil |
|---|---|
| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, 2009-01-02 → 2026-10-16; semua sha256 sepadan |
| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |
| c. Sumber sektor/industri setiap ticker | **LULUS** — 2358/2370 = 99.5% (2 kelas saham diisi daripada ticker asas; 103 ticker = `Lain-lain`) |
| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 (indeks sektor A02; diluluskan pengguna) |
| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — 0.138 s/ticker; larian penuh 2370 ticker = 328 s |
| f. `semak_hadapan` atas modul indikator | **LULUS** — 14 tarikh potong (≥ 12), 26,950 perbandingan, **0 kegagalan** (`REVERSE/PANDANG_HADAPAN_2021.md`) |

## 2. Step 1–2 — run

Saiz universe 2021 setiap bulan: min **1989**, median **2000**, maks **2000**; 2370 ticker berbeza sepanjang tahun.


> **KAVEAT SAIZ UNIVERSE.** Universe 2021 lebih kecil daripada had 2000 saham (min 1989 sebulan). Jumlah run, peristiwa dan kemunculan tahun ini **tidak setara** dengan tahun yang universenya penuh 2000; bandingkan kadar dan peratusan, bukan bilangan mutlak, dalam `BANDING_TAHUN.md`.

| bulan | n_run | n_super | n_padu | n_biasa | n_bertangga | n_lonjakan | n_stabil | n_entry_sah | n_masih_naik | n_peristiwa | med_naik |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021-01 | 196 | 6 | 104 | 86 | 31 | 79 | 86 | 188 | 37 | 1069 | 32.4 |
| 2021-02 | 188 | 1 | 92 | 95 | 15 | 76 | 97 | 136 | 26 | 1405 | 28.1 |
| 2021-03 | 717 | 6 | 328 | 383 | 51 | 339 | 327 | 544 | 85 | 1347 | 27.9 |
| 2021-04 | 316 | 4 | 87 | 225 | 8 | 165 | 143 | 254 | 8 | 1539 | 21.6 |
| 2021-05 | 378 | 8 | 157 | 213 | 24 | 171 | 183 | 267 | 33 | 1236 | 26.0 |
| 2021-06 | 135 | 1 | 46 | 88 | 4 | 74 | 57 | 112 | 13 | 938 | 22.9 |
| 2021-07 | 408 | 3 | 175 | 230 | 19 | 212 | 177 | 253 | 61 | 1481 | 25.4 |
| 2021-08 | 338 | 5 | 179 | 154 | 24 | 142 | 172 | 266 | 58 | 1107 | 31.0 |
| 2021-09 | 386 | 4 | 141 | 241 | 18 | 142 | 226 | 336 | 17 | 1153 | 24.8 |
| 2021-10 | 424 | 2 | 111 | 311 | 8 | 243 | 173 | 348 | 12 | 1126 | 20.8 |
| 2021-11 | 237 | 2 | 62 | 173 | 4 | 156 | 77 | 145 | 12 | 887 | 21.4 |
| 2021-12 | 690 | 2 | 116 | 572 | 18 | 410 | 262 | 460 | 37 | 1971 | 16.7 |


Jumlah: **4413 run layak**, 3309 (75.0%) dengan `entry_sah = ya` (tiada amaran: syarat 10 hari menolak 25.0% < 50%). Dilangkau: 17105 (15931 "terlalu perlahan").


### Bucket %_naik × tempoh

| bucket_pct | <=21 | <=42 | <=63 |
|---|---|---|---|
| 10%+ | 1630 | 0 | 0 |
| 100%+ | 5 | 13 | 21 |
| 20%+ | 450 | 691 | 0 |
| 200%+ | 0 | 1 | 2 |
| 30%+ | 208 | 306 | 719 |
| 300%+ | 0 | 1 | 1 |
| 50%+ | 50 | 87 | 228 |


### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)

| kumpulan | PANTAS | PERLAHAN | SEDANG |
|---|---|---|---|
| BIASA | 2080 | 0 | 691 |
| PADU | 258 | 947 | 393 |
| SUPER PADU | 5 | 24 | 15 |


Sel SAMPEL KECIL: [('SUPER PADU', 'PANTAS'), ('SUPER PADU', 'SEDANG')]


### Jenis kenaikan

| jenis | n |
|---|---|
| LONJAKAN | 2209 |
| STABIL | 1980 |
| BERTANGGA | 224 |


`graf_menaik = ya` (S3): 2547 (57.7%). `masih_naik = ya`: 399.


### 10 run terbaik setiap bulan (ikut %_naik_rendah)


**2021-01**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| DAC | Industrials | 2021-01-04 | 2021-03-26 | 57 | 160.9 | SUPER PADU | BERTANGGA | ya | tidak |
| FUBO | Communication Services | 2021-01-04 | 2021-02-01 | 19 | 126.15 | SUPER PADU | LONJAKAN | ya | tidak |
| FNKO | Consumer Cyclical | 2021-01-04 | 2021-04-06 | 63 | 119.62 | SUPER PADU | BERTANGGA | ya | ya |
| LGND | Healthcare | 2021-01-07 | 2021-02-09 | 22 | 109.87 | SUPER PADU | STABIL | ya | tidak |
| AA | Basic Materials | 2021-01-29 | 2021-04-29 | 62 | 109.11 | SUPER PADU | STABIL | ya | ya |
| PERI | Communication Services | 2021-01-20 | 2021-03-02 | 28 | 107.18 | SUPER PADU | LONJAKAN | ya | tidak |
| QTRX | Healthcare | 2021-01-11 | 2021-02-19 | 27 | 95.05 | PADU | STABIL | ya | tidak |
| BTBT | Financial Services | 2021-01-19 | 2021-02-16 | 19 | 92.24 | PADU | LONJAKAN | ya | tidak |
| MX | Technology | 2021-01-07 | 2021-04-05 | 59 | 87.87 | PADU | LONJAKAN | ya | tidak |
| OLN | Basic Materials | 2021-01-27 | 2021-04-15 | 54 | 86.49 | PADU | BERTANGGA | ya | tidak |


**2021-02**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| PRTA | Healthcare | 2021-02-05 | 2021-03-25 | 33 | 100.14 | SUPER PADU | LONJAKAN | ya | tidak |
| MGNX | Healthcare | 2021-02-18 | 2021-04-29 | 49 | 88.72 | PADU | STABIL | ya | tidak |
| JYNT | Healthcare | 2021-02-24 | 2021-05-25 | 63 | 83.99 | PADU | STABIL | ya | ya |
| LQDT | Consumer Cyclical | 2021-02-11 | 2021-05-12 | 62 | 78.66 | PADU | LONJAKAN | ya | ya |
| DBI | Consumer Cyclical | 2021-02-26 | 2021-05-17 | 55 | 70.69 | PADU | STABIL | ya | tidak |
| ZNTL | Healthcare | 2021-02-01 | 2021-04-26 | 58 | 70.55 | PADU | STABIL | tidak | tidak |
| NBR | Energy | 2021-02-23 | 2021-03-08 | 9 | 64.61 | PADU | LONJAKAN | ya | tidak |
| SSTK | Communication Services | 2021-02-01 | 2021-04-15 | 51 | 63.49 | PADU | LONJAKAN | ya | tidak |
| CLF | Basic Materials | 2021-02-26 | 2021-05-11 | 51 | 60.75 | PADU | LONJAKAN | ya | tidak |
| HVT | Consumer Cyclical | 2021-02-01 | 2021-04-29 | 61 | 60.54 | PADU | BERTANGGA | ya | ya |


**2021-03**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| MVIS | Technology | 2021-03-05 | 2021-04-26 | 35 | 161.26 | SUPER PADU | LONJAKAN | ya | tidak |
| GME | Consumer Cyclical | 2021-03-25 | 2021-06-09 | 52 | 158.82 | SUPER PADU | STABIL | ya | tidak |
| MARA | Financial Services | 2021-03-05 | 2021-04-05 | 20 | 134.59 | SUPER PADU | STABIL | ya | tidak |
| CLDX | Healthcare | 2021-03-29 | 2021-06-28 | 63 | 127.65 | SUPER PADU | BERTANGGA | tidak | ya |
| TIGR | Financial Services | 2021-03-26 | 2021-06-11 | 53 | 119.52 | SUPER PADU | STABIL | ya | tidak |
| PDS | Energy | 2021-03-25 | 2021-06-23 | 62 | 108.09 | SUPER PADU | BERTANGGA | ya | ya |
| IDT | Communication Services | 2021-03-09 | 2021-06-08 | 63 | 98.66 | PADU | BERTANGGA | ya | ya |
| NCTY | Financial Services | 2021-03-05 | 2021-03-15 | 6 | 97.55 | PADU | LONJAKAN | ya | tidak |
| CELH | Consumer Defensive | 2021-03-11 | 2021-06-07 | 60 | 96.45 | PADU | STABIL | tidak | tidak |
| QFIN | Financial Services | 2021-03-05 | 2021-06-04 | 63 | 92.47 | PADU | LONJAKAN | ya | ya |


**2021-04**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ANVS | Healthcare | 2021-04-16 | 2021-07-13 | 60 | 485.81 | SUPER PADU | STABIL | ya | tidak |
| SPCE | Industrials | 2021-04-20 | 2021-06-25 | 47 | 176.65 | SUPER PADU | LONJAKAN | tidak | tidak |
| DDD | Technology | 2021-04-19 | 2021-06-28 | 49 | 117.01 | SUPER PADU | LONJAKAN | tidak | tidak |
| BEAM | Healthcare | 2021-04-12 | 2021-07-01 | 57 | 101.6 | SUPER PADU | STABIL | ya | tidak |
| ASTS | Technology | 2021-04-19 | 2021-07-06 | 54 | 90.03 | PADU | LONJAKAN | tidak | tidak |
| LFMD | Healthcare | 2021-04-15 | 2021-06-08 | 37 | 88.47 | PADU | LONJAKAN | tidak | tidak |
| RTB | Technology | 2021-04-15 | 2021-06-17 | 44 | 87.59 | PADU | LONJAKAN | tidak | tidak |
| CHPT | Consumer Cyclical | 2021-04-21 | 2021-06-29 | 48 | 87.45 | PADU | STABIL | ya | tidak |
| IRLA | Healthcare | 2021-04-12 | 2021-07-08 | 61 | 87.41 | PADU | STABIL | ya | ya |
| JKS | Technology | 2021-04-13 | 2021-07-12 | 62 | 79.68 | PADU | LONJAKAN | ya | ya |


**2021-05**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| NEGG | Consumer Cyclical | 2021-05-12 | 2021-07-07 | 38 | 1024.29 | SUPER PADU | LONJAKAN | ya | tidak |
| FLNA | Healthcare | 2021-05-11 | 2021-07-28 | 54 | 275.31 | SUPER PADU | BERTANGGA | ya | tidak |
| AVXL | Healthcare | 2021-05-13 | 2021-06-28 | 31 | 188.31 | SUPER PADU | LONJAKAN | ya | tidak |
| NTLA | Healthcare | 2021-05-10 | 2021-07-01 | 37 | 182.46 | SUPER PADU | LONJAKAN | tidak | tidak |
| BNTX | Healthcare | 2021-05-13 | 2021-08-09 | 60 | 158.93 | SUPER PADU | STABIL | ya | tidak |
| INTZ | Technology | 2021-05-06 | 2021-06-02 | 18 | 106.8 | SUPER PADU | LONJAKAN | ya | tidak |
| ARCT | Healthcare | 2021-05-06 | 2021-08-03 | 61 | 101.42 | SUPER PADU | LONJAKAN | tidak | ya |
| BTBT | Financial Services | 2021-05-19 | 2021-08-06 | 55 | 100.11 | SUPER PADU | LONJAKAN | tidak | tidak |
| MARA | Financial Services | 2021-05-13 | 2021-08-09 | 60 | 96.4 | PADU | STABIL | tidak | tidak |
| ZDGE | Communication Services | 2021-05-11 | 2021-06-17 | 26 | 94.2 | PADU | STABIL | ya | tidak |


**2021-06**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ABTS | Financial Services | 2021-06-02 | 2021-07-13 | 28 | 217.81 | SUPER PADU | STABIL | ya | tidak |
| PDSB | Healthcare | 2021-06-16 | 2021-09-02 | 55 | 79.06 | PADU | STABIL | ya | tidak |
| CYTK | Healthcare | 2021-06-30 | 2021-09-27 | 61 | 78.84 | PADU | LONJAKAN | tidak | ya |
| CACC | Financial Services | 2021-06-08 | 2021-09-03 | 62 | 73.2 | PADU | STABIL | ya | ya |
| PRTA | Healthcare | 2021-06-25 | 2021-09-23 | 62 | 70.46 | PADU | BERTANGGA | ya | ya |
| SAFE | Real Estate | 2021-06-04 | 2021-08-31 | 61 | 61.97 | PADU | BERTANGGA | ya | ya |
| AMC | Communication Services | 2021-06-10 | 2021-06-17 | 5 | 52.93 | PADU | LONJAKAN | ya | tidak |
| CVM | Healthcare | 2021-06-30 | 2021-09-02 | 45 | 52.32 | PADU | STABIL | tidak | tidak |
| FATE | Healthcare | 2021-06-03 | 2021-08-09 | 46 | 46.98 | PADU | LONJAKAN | ya | tidak |
| DQ | Technology | 2021-06-22 | 2021-07-21 | 20 | 45.92 | PADU | LONJAKAN | ya | tidak |


**2021-07**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| RSI | Consumer Cyclical | 2021-07-19 | 2021-10-08 | 58 | 114.36 | SUPER PADU | STABIL | tidak | tidak |
| DAO | Consumer Defensive | 2021-07-27 | 2021-09-07 | 29 | 113.68 | SUPER PADU | LONJAKAN | tidak | tidak |
| AMTX | Basic Materials | 2021-07-08 | 2021-10-01 | 60 | 108.03 | SUPER PADU | STABIL | tidak | tidak |
| TVTX | Healthcare | 2021-07-19 | 2021-10-08 | 58 | 98.41 | PADU | STABIL | ya | tidak |
| EDIT | Healthcare | 2021-07-27 | 2021-09-02 | 27 | 93.83 | PADU | BERTANGGA | ya | tidak |
| MI | Consumer Cyclical | 2021-07-14 | 2021-09-01 | 35 | 89.23 | PADU | LONJAKAN | tidak | tidak |
| FLNA | Healthcare | 2021-07-30 | 2021-08-13 | 10 | 88.57 | PADU | STABIL | ya | tidak |
| CAR | Industrials | 2021-07-08 | 2021-10-05 | 62 | 83.29 | PADU | STABIL | ya | ya |
| GOGO | Communication Services | 2021-07-08 | 2021-10-01 | 60 | 82.06 | PADU | LONJAKAN | tidak | tidak |
| BXC | Industrials | 2021-07-19 | 2021-08-24 | 26 | 80.43 | PADU | BERTANGGA | ya | tidak |


**2021-08**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| SM | Energy | 2021-08-20 | 2021-11-08 | 55 | 154.72 | SUPER PADU | BERTANGGA | ya | tidak |
| ENTA | Healthcare | 2021-08-13 | 2021-11-05 | 59 | 111.54 | SUPER PADU | STABIL | ya | tidak |
| AUPH | Healthcare | 2021-08-31 | 2021-10-29 | 42 | 104.96 | SUPER PADU | LONJAKAN | ya | tidak |
| PLBY | Consumer Cyclical | 2021-08-19 | 2021-11-16 | 62 | 103.34 | SUPER PADU | LONJAKAN | ya | ya |
| INMB | Healthcare | 2021-08-04 | 2021-09-07 | 23 | 100.36 | SUPER PADU | STABIL | tidak | tidak |
| NOG | Energy | 2021-08-20 | 2021-10-12 | 36 | 91.22 | PADU | BERTANGGA | ya | tidak |
| AXSM | Healthcare | 2021-08-10 | 2021-11-08 | 63 | 88.24 | PADU | STABIL | tidak | ya |
| FLNA | Healthcare | 2021-08-27 | 2021-11-05 | 49 | 84.44 | PADU | LONJAKAN | tidak | tidak |
| MTDR | Energy | 2021-08-20 | 2021-10-26 | 46 | 83.97 | PADU | BERTANGGA | ya | tidak |
| OVV | Energy | 2021-08-19 | 2021-10-20 | 43 | 82.61 | PADU | STABIL | ya | tidak |


**2021-09**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| LCID | Consumer Cyclical | 2021-09-01 | 2021-11-16 | 53 | 244.42 | SUPER PADU | BERTANGGA | ya | tidak |
| PTGX | Healthcare | 2021-09-20 | 2021-11-12 | 39 | 189.84 | SUPER PADU | LONJAKAN | tidak | tidak |
| MPU | Communication Services | 2021-09-01 | 2021-09-29 | 19 | 145.77 | SUPER PADU | LONJAKAN | ya | tidak |
| LWLG | Basic Materials | 2021-09-30 | 2021-12-10 | 50 | 115.89 | SUPER PADU | STABIL | tidak | tidak |
| M | Consumer Cyclical | 2021-09-13 | 2021-11-18 | 48 | 83.87 | PADU | LONJAKAN | ya | tidak |
| HAPN | Financial Services | 2021-09-29 | 2021-11-01 | 23 | 79.86 | PADU | LONJAKAN | ya | tidak |
| CUBI | Financial Services | 2021-09-20 | 2021-12-16 | 62 | 76.68 | PADU | STABIL | ya | ya |
| DLTR | Consumer Defensive | 2021-09-24 | 2021-11-24 | 43 | 74.0 | PADU | STABIL | ya | tidak |
| FLR | Industrials | 2021-09-21 | 2021-12-14 | 59 | 69.54 | PADU | BERTANGGA | ya | tidak |
| AMRC | Industrials | 2021-09-29 | 2021-11-05 | 27 | 68.02 | PADU | STABIL | ya | tidak |


**2021-10**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| BE | Industrials | 2021-10-04 | 2021-11-08 | 25 | 111.41 | SUPER PADU | LONJAKAN | ya | tidak |
| LAR | Basic Materials | 2021-10-06 | 2021-11-29 | 37 | 109.51 | SUPER PADU | STABIL | ya | tidak |
| CIFR | Technology | 2021-10-13 | 2021-11-01 | 13 | 92.01 | PADU | LONJAKAN | ya | tidak |
| ENPH | Technology | 2021-10-04 | 2021-11-19 | 34 | 85.33 | PADU | LONJAKAN | ya | tidak |
| PI | Technology | 2021-10-12 | 2021-12-27 | 52 | 83.11 | PADU | LONJAKAN | ya | tidak |
| PERI | Communication Services | 2021-10-01 | 2021-11-12 | 30 | 80.94 | PADU | LONJAKAN | ya | tidak |
| NVAX | Healthcare | 2021-10-20 | 2021-11-26 | 26 | 79.62 | PADU | STABIL | ya | tidak |
| BLNK | Industrials | 2021-10-04 | 2021-11-15 | 30 | 78.75 | PADU | LONJAKAN | ya | tidak |
| ANET | Technology | 2021-10-01 | 2021-12-27 | 59 | 72.39 | PADU | BERTANGGA | ya | tidak |
| MPU | Communication Services | 2021-10-20 | 2022-01-03 | 51 | 70.49 | PADU | STABIL | ya | tidak |


**2021-11**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| KRYS | Healthcare | 2021-11-23 | 2021-11-29 | 3 | 121.43 | SUPER PADU | LONJAKAN | ya | tidak |
| BXC | Industrials | 2021-11-02 | 2021-12-31 | 41 | 108.81 | SUPER PADU | BERTANGGA | ya | tidak |
| EBS | Healthcare | 2021-11-05 | 2022-01-14 | 48 | 74.77 | PADU | STABIL | tidak | tidak |
| SABR | Technology | 2021-11-26 | 2022-02-16 | 56 | 68.65 | PADU | LONJAKAN | ya | tidak |
| TTD | Communication Services | 2021-11-05 | 2021-11-16 | 7 | 63.07 | PADU | LONJAKAN | ya | tidak |
| TGTX | Healthcare | 2021-11-30 | 2022-01-03 | 23 | 62.04 | PADU | STABIL | tidak | tidak |
| SBLK | Industrials | 2021-11-16 | 2022-02-15 | 62 | 61.59 | PADU | STABIL | ya | ya |
| SLI | Basic Materials | 2021-11-18 | 2021-11-29 | 6 | 61.33 | PADU | LONJAKAN | ya | tidak |
| NBR | Energy | 2021-11-19 | 2022-02-16 | 60 | 58.5 | PADU | STABIL | tidak | tidak |
| PCT | Industrials | 2021-11-11 | 2021-11-22 | 7 | 55.67 | PADU | LONJAKAN | ya | tidak |


**2021-12**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| PBF | Energy | 2021-12-17 | 2022-03-11 | 57 | 135.82 | SUPER PADU | BERTANGGA | ya | tidak |
| HCC | Basic Materials | 2021-12-13 | 2022-03-10 | 60 | 111.48 | SUPER PADU | STABIL | ya | tidak |
| IPI | Basic Materials | 2021-12-06 | 2022-03-08 | 63 | 91.49 | PADU | STABIL | ya | ya |
| INVX | Energy | 2021-12-02 | 2022-03-04 | 63 | 82.44 | PADU | STABIL | tidak | ya |
| SBSW | Basic Materials | 2021-12-15 | 2022-03-07 | 55 | 82.24 | PADU | BERTANGGA | ya | tidak |
| BCRX | Healthcare | 2021-12-01 | 2022-02-16 | 53 | 75.33 | PADU | LONJAKAN | tidak | tidak |
| AR | Energy | 2021-12-06 | 2022-03-07 | 62 | 70.68 | PADU | STABIL | tidak | ya |
| CLB | Energy | 2021-12-17 | 2022-03-08 | 54 | 66.29 | PADU | LONJAKAN | ya | tidak |
| STNG | Energy | 2021-12-03 | 2022-03-04 | 62 | 64.18 | PADU | STABIL | tidak | ya |
| DAC | Industrials | 2021-12-15 | 2022-03-17 | 63 | 63.26 | PADU | BERTANGGA | ya | ya |


### Semua run SUPER PADU (≥ 100%)

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|
| NEGG | Consumer Cyclical | 2021-05-12 | 38 | 1024.29 | LONJAKAN | ya | tidak |
| ANVS | Healthcare | 2021-04-16 | 60 | 485.81 | STABIL | ya | tidak |
| FLNA | Healthcare | 2021-05-11 | 54 | 275.31 | BERTANGGA | ya | tidak |
| LCID | Consumer Cyclical | 2021-09-01 | 53 | 244.42 | BERTANGGA | ya | tidak |
| ABTS | Financial Services | 2021-06-02 | 28 | 217.81 | STABIL | ya | tidak |
| PTGX | Healthcare | 2021-09-20 | 39 | 189.84 | LONJAKAN | tidak | tidak |
| AVXL | Healthcare | 2021-05-13 | 31 | 188.31 | LONJAKAN | ya | tidak |
| NTLA | Healthcare | 2021-05-10 | 37 | 182.46 | LONJAKAN | tidak | tidak |
| SPCE | Industrials | 2021-04-20 | 47 | 176.65 | LONJAKAN | tidak | tidak |
| MVIS | Technology | 2021-03-05 | 35 | 161.26 | LONJAKAN | ya | tidak |
| DAC | Industrials | 2021-01-04 | 57 | 160.9 | BERTANGGA | ya | tidak |
| BNTX | Healthcare | 2021-05-13 | 60 | 158.93 | STABIL | ya | tidak |
| GME | Consumer Cyclical | 2021-03-25 | 52 | 158.82 | STABIL | ya | tidak |
| SM | Energy | 2021-08-20 | 55 | 154.72 | BERTANGGA | ya | tidak |
| MPU | Communication Services | 2021-09-01 | 19 | 145.77 | LONJAKAN | ya | tidak |
| PBF | Energy | 2021-12-17 | 57 | 135.82 | BERTANGGA | ya | tidak |
| MARA | Financial Services | 2021-03-05 | 20 | 134.59 | STABIL | ya | tidak |
| CLDX | Healthcare | 2021-03-29 | 63 | 127.65 | BERTANGGA | tidak | ya |
| FUBO | Communication Services | 2021-01-04 | 19 | 126.15 | LONJAKAN | ya | tidak |
| KRYS | Healthcare | 2021-11-23 | 3 | 121.43 | LONJAKAN | ya | tidak |
| FNKO | Consumer Cyclical | 2021-01-04 | 63 | 119.62 | BERTANGGA | ya | ya |
| TIGR | Financial Services | 2021-03-26 | 53 | 119.52 | STABIL | ya | tidak |
| DDD | Technology | 2021-04-19 | 49 | 117.01 | LONJAKAN | tidak | tidak |
| LWLG | Basic Materials | 2021-09-30 | 50 | 115.89 | STABIL | tidak | tidak |
| RSI | Consumer Cyclical | 2021-07-19 | 58 | 114.36 | STABIL | tidak | tidak |
| DAO | Consumer Defensive | 2021-07-27 | 29 | 113.68 | LONJAKAN | tidak | tidak |
| ENTA | Healthcare | 2021-08-13 | 59 | 111.54 | STABIL | ya | tidak |
| HCC | Basic Materials | 2021-12-13 | 60 | 111.48 | STABIL | ya | tidak |
| BE | Industrials | 2021-10-04 | 25 | 111.41 | LONJAKAN | ya | tidak |
| LGND | Healthcare | 2021-01-07 | 22 | 109.87 | STABIL | ya | tidak |
| LAR | Basic Materials | 2021-10-06 | 37 | 109.51 | STABIL | ya | tidak |
| AA | Basic Materials | 2021-01-29 | 62 | 109.11 | STABIL | ya | ya |
| BXC | Industrials | 2021-11-02 | 41 | 108.81 | BERTANGGA | ya | tidak |
| PDS | Energy | 2021-03-25 | 62 | 108.09 | BERTANGGA | ya | ya |
| AMTX | Basic Materials | 2021-07-08 | 60 | 108.03 | STABIL | tidak | tidak |
| PERI | Communication Services | 2021-01-20 | 28 | 107.18 | LONJAKAN | ya | tidak |
| INTZ | Technology | 2021-05-06 | 18 | 106.8 | LONJAKAN | ya | tidak |
| AUPH | Healthcare | 2021-08-31 | 42 | 104.96 | LONJAKAN | ya | tidak |
| PLBY | Consumer Cyclical | 2021-08-19 | 62 | 103.34 | LONJAKAN | ya | ya |
| BEAM | Healthcare | 2021-04-12 | 57 | 101.6 | STABIL | ya | tidak |
| ARCT | Healthcare | 2021-05-06 | 61 | 101.42 | LONJAKAN | tidak | ya |
| INMB | Healthcare | 2021-08-04 | 23 | 100.36 | STABIL | tidak | tidak |
| PRTA | Healthcare | 2021-02-05 | 33 | 100.14 | LONJAKAN | ya | tidak |
| BTBT | Financial Services | 2021-05-19 | 55 | 100.11 | LONJAKAN | tidak | tidak |


(dipaparkan 60 teratas daripada 44)


### Run BERTANGGA (S2) — 40 teratas

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | bilangan_kaki | pct_hari_atas_ema21 | kumpulan |
|---|---|---|---|---|---|---|---|
| FLNA | Healthcare | 2021-05-11 | 54 | 275.31 | 4 | 94.2 | SUPER PADU |
| LCID | Consumer Cyclical | 2021-09-01 | 53 | 244.42 | 4 | 90.9 | SUPER PADU |
| DAC | Industrials | 2021-01-04 | 57 | 160.9 | 4 | 96.5 | SUPER PADU |
| SM | Energy | 2021-08-20 | 55 | 154.72 | 2 | 98.1 | SUPER PADU |
| PBF | Energy | 2021-12-17 | 57 | 135.82 | 2 | 84.9 | SUPER PADU |
| CLDX | Healthcare | 2021-03-29 | 63 | 127.65 | 2 | 64.1 | SUPER PADU |
| FNKO | Consumer Cyclical | 2021-01-04 | 63 | 119.62 | 5 | 96.8 | SUPER PADU |
| BXC | Industrials | 2021-11-02 | 41 | 108.81 | 2 | 100.0 | SUPER PADU |
| PDS | Energy | 2021-03-25 | 62 | 108.09 | 4 | 93.1 | SUPER PADU |
| IDT | Communication Services | 2021-03-09 | 63 | 98.66 | 2 | 95.2 | PADU |
| EDIT | Healthcare | 2021-07-27 | 27 | 93.83 | 2 | 100.0 | PADU |
| NOG | Energy | 2021-08-20 | 36 | 91.22 | 2 | 93.8 | PADU |
| XPEL | Consumer Cyclical | 2021-03-25 | 50 | 86.76 | 2 | 97.8 | PADU |
| OLN | Basic Materials | 2021-01-27 | 54 | 86.49 | 3 | 100.0 | PADU |
| BCRX | Healthcare | 2021-03-29 | 48 | 85.38 | 4 | 69.4 | PADU |
| MVIS | Technology | 2021-05-13 | 19 | 84.78 | 3 | 77.8 | PADU |
| MTDR | Energy | 2021-08-20 | 46 | 83.97 | 2 | 92.9 | PADU |
| SBSW | Basic Materials | 2021-12-15 | 55 | 82.24 | 2 | 90.2 | PADU |
| BXC | Industrials | 2021-07-19 | 26 | 80.43 | 2 | 94.7 | PADU |
| ENPH | Technology | 2021-05-11 | 59 | 78.11 | 3 | 86.8 | PADU |
| CYH | Healthcare | 2021-04-20 | 36 | 77.88 | 2 | 100.0 | PADU |
| INMD | Healthcare | 2021-07-12 | 53 | 76.48 | 3 | 88.7 | PADU |
| GTM | Technology | 2021-05-17 | 56 | 75.86 | 2 | 83.7 | PADU |
| ZNTL | Healthcare | 2021-08-12 | 58 | 74.75 | 2 | 86.2 | PADU |
| RDNT | Healthcare | 2021-03-25 | 57 | 73.58 | 2 | 91.1 | PADU |
| CHRD | Energy | 2021-03-09 | 58 | 72.47 | 3 | 96.6 | PADU |
| ANET | Technology | 2021-10-01 | 59 | 72.39 | 2 | 92.9 | PADU |
| JKS | Technology | 2021-08-19 | 62 | 71.17 | 3 | 71.4 | PADU |
| PRTA | Healthcare | 2021-06-25 | 62 | 70.46 | 2 | 91.9 | PADU |
| URBN | Consumer Cyclical | 2021-01-04 | 50 | 70.08 | 2 | 85.7 | PADU |
| MTDR | Energy | 2021-04-21 | 46 | 69.97 | 2 | 97.8 | PADU |
| FLR | Industrials | 2021-09-21 | 59 | 69.54 | 2 | 91.4 | PADU |
| MP | Basic Materials | 2021-05-13 | 60 | 68.85 | 4 | 68.9 | PADU |
| CLFD | Technology | 2021-09-20 | 61 | 66.53 | 3 | 88.3 | PADU |
| SPT | Technology | 2021-08-03 | 36 | 66.47 | 3 | 100.0 | PADU |
| NUE | Basic Materials | 2021-03-23 | 48 | 66.34 | 3 | 97.9 | PADU |
| COKE | Consumer Defensive | 2021-03-02 | 63 | 66.12 | 2 | 78.7 | PADU |
| IDT | Communication Services | 2021-09-20 | 39 | 65.59 | 2 | 60.0 | PADU |
| DVN | Energy | 2021-09-09 | 62 | 65.56 | 3 | 88.5 | PADU |
| XPEV | Consumer Cyclical | 2021-10-04 | 40 | 64.08 | 3 | 94.7 | PADU |


(daripada 224 run BERTANGGA)


### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)

n peristiwa PADU dalam S2, populasi keputusan (a) = **128** (rujukan: semua peristiwa = 1326). < 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat.


Peristiwa sah: **15259** (populasi keputusan 5571).


## 3. Step 2b — kohort "naik dan naik"

Dijejak 315 run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari tarikh_sah.


| Metrik | Nilai |
|---|---|
| % akhirnya melebihi +100% | **15.6%** |
| median %_naik_penuh | **59.9%** |
| median %_naik pada hari ke-63 | 37.6% |
| median hari ke puncak penuh | 116 |
| median MFE 252 selepas kos | 45.5% |
| median MAE 252 | -9.1% |
| median hari pegang Chandelier 4×ATR | 85 |
| median pulangan Chandelier selepas kos | 18.3% |
| terpotong hujung data | 0.0% |


Exit yang menyala dahulu:


| exit | n |
|---|---|
| bawah_ema9 | 105 |
| bawah_ma50 | 83 |
| hist_neg3 | 40 |
| rsi_70_60 | 29 |
| bawah_ema21 | 27 |
| macd_bawah | 15 |
| hari_agihan | 13 |
| trail_8pct | 2 |
| trail_2atr | 1 |


### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari

| kohort | n | median_naik_63 | pct_bertangga | pct_super | median_hari_ke_puncak |
|---|---|---|---|---|---|
| masih_naik = ya | 315 | 37.6 | 22.9 | 1.3 | 63.0 |
| reda dalam 63 hari | 2994 | 22.2 | 4.6 | 0.9 | 21.0 |


Kohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya diketahui pada hari ke-63.


## 4. Step 3 — populasi kuintil dan dedup

POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **7884** baris. Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **31** daripada 41; dibuang 10.


| buang | kerana | rho |
|---|---|---|
| j_ma150 | j_ma200 | 0.968 |
| cerun_ema21 | j_ma50 | 0.811 |
| cerun_ma200 | j_ma200 | 0.86 |
| rsi14 | j_ma50 | 0.816 |
| roc60 | cerun_ma50 | 0.927 |
| willr14 | stoch_k | 1.0 |
| julat10 | atr_pct | 0.84 |
| bb_pctb | stoch_k | 0.801 |
| kelt_pos | j_ema21 | 0.913 |
| rs_spy_3b | cerun_ma50 | 0.886 |


Signal dibina: **213** (31 binari + 62 hujung kuintil + 120 pemicu × 1 konteks).


## 5. Step 4 — common & unique (ENTRY)

Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. N ujian ENTRY sebenar (populasi a, kumpulan A) = **852** baris (213 signal × 2 subset × 2 keluarga).


### Kelas (S2, kumpulan A, keluarga PADU)

| kelas | n |
|---|---|
| TIDAK BERGUNA | 180 |
| UNIQUE | 14 |
| COMMON BIASA | 8 |
| SEDERHANA | 7 |
| LANGKA | 4 |


### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)

| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n | n_industri | n_minggu | purata_pct_naik_rendah | purata_hari_ke_puncak | pct_bertangga | pct_lonjakan | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | UNIQUE | 29.58 | 0.0 | 2.55 | 0.86 | 11.582 | 34.424 | 34.33 | 8.355 | 67 | 37 | 26 | 62.17 | 50.6 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:bb_lebar | UNIQUE | 28.17 | 0.0 | 2.73 | 0.82 | 10.327 | 34.346 | 31.88 | 7.76 | 69 | 39 | 25 | 61.38 | 50.7 | 100.0 | 0.0 |  |
| q5:julat20 | UNIQUE | 47.89 | 0.0 | 5.05 | 25.93 | 9.484 | 1.847 | 29.84 | 7.262 | 124 | 55 | 34 | 58.65 | 47.2 | 100.0 | 0.0 |  |
| macd_cross&q5:bb_lebar | LANGKA | 9.86 | 0.0 | 1.28 | 0.96 | 7.722 | 10.304 | 29.03 | 7.066 | 31 | 25 | 17 | 72.71 | 45.2 | 100.0 | 0.0 |  |
| pocket_pivot&q1:j_52w_tinggi | UNIQUE | 16.9 | 0.0 | 1.74 | 1.31 | 9.707 | 12.918 | 28.57 | 6.954 | 42 | 26 | 25 | 54.22 | 44.4 | 100.0 | 0.0 |  |
| ema_crossback&q5:bb_lebar | UNIQUE | 18.31 | 0.0 | 1.97 | 0.49 | 9.279 | 37.506 | 27.66 | 6.732 | 47 | 31 | 17 | 50.03 | 48.2 | 100.0 | 0.0 |  |
| ema_crossback&q5:julat20 | UNIQUE | 18.31 | 0.0 | 1.97 | 0.59 | 9.279 | 31.255 | 27.66 | 6.732 | 47 | 33 | 17 | 49.6 | 47.2 | 100.0 | 0.0 |  |
| q5:j_ema9 | UNIQUE | 47.89 | 0.0 | 6.27 | 10.97 | 7.64 | 4.364 | 25.52 | 6.21 | 145 | 76 | 34 | 62.45 | 49.2 | 100.0 | 0.0 |  |
| q5:bb_lebar | UNIQUE | 43.66 | 0.0 | 5.8 | 28.33 | 7.523 | 1.541 | 25.37 | 6.175 | 134 | 64 | 33 | 59.97 | 46.5 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:cerun_ma50 | LANGKA | 11.27 | 0.0 | 1.63 | 0.78 | 6.934 | 14.425 | 22.22 | 5.408 | 36 | 25 | 19 | 57.94 | 52.9 | 100.0 | 0.0 |  |
| ema_crossback&q5:atr_pct | LANGKA | 12.68 | 0.0 | 2.03 | 0.43 | 6.24 | 29.506 | 20.45 | 4.978 | 44 | 30 | 18 | 55.07 | 43.3 | 100.0 | 0.0 |  |
| ema_crossback&q5:cerun_ma50 | LANGKA | 14.08 | 0.0 | 2.44 | 0.84 | 5.778 | 16.774 | 19.23 | 4.68 | 52 | 35 | 22 | 52.76 | 47.9 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:j_ma200 | UNIQUE | 15.49 | 0.0 | 2.79 | 0.66 | 5.561 | 23.335 | 18.64 | 4.538 | 59 | 34 | 22 | 48.27 | 50.6 | 100.0 | 0.0 |  |
| ema_crossback&q5:j_ma200 | UNIQUE | 16.9 | 0.0 | 3.37 | 0.8 | 5.021 | 21.11 | 17.14 | 4.172 | 70 | 40 | 22 | 46.57 | 48.6 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:rs_spy_6b | UNIQUE | 16.9 | 0.0 | 3.95 | 0.66 | 4.283 | 25.457 | 15.0 | 3.651 | 80 | 46 | 25 | 49.79 | 51.5 | 100.0 | 0.0 |  |
| q5:j_52w_rendah | UNIQUE | 26.76 | 0.0 | 7.14 | 17.05 | 3.749 | 1.57 | 14.58 | 3.549 | 144 | 67 | 36 | 55.83 | 48.1 | 100.0 | 0.0 |  |
| ema_crossback&q5:rs_spy_6b | UNIQUE | 18.31 | 0.0 | 4.59 | 0.72 | 3.993 | 25.342 | 14.13 | 3.439 | 92 | 51 | 25 | 48.11 | 49.5 | 100.0 | 0.0 |  |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 15.49 | 0.0 | 4.53 | 1.03 | 3.422 | 14.97 | 12.36 | 3.008 | 89 | 45 | 33 | 54.47 | 50.0 | 100.0 | 0.0 |  |


### Rujukan S1 (semua run layak)

_(tiada baris)_


### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja

S3 mengandungi 2293 run; ia **bukan keluarga carian** (tidak menambah N). 7.8% daripadanya BERTANGGA lawan 6.3% keseluruhan.


### Keluarga SUPER PADU (FDR sendiri)

| signal | kelas | K_super | lift | lift_rawak | n | tanda |
|---|---|---|---|---|---|---|
| gap_and_go&q5:bb_lebar | TERAS | 66.67 | 1200.667 | 1200.667 | 2 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q5:atr_pct | TERAS | 66.67 | 1200.667 | 1200.667 | 2 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q5:julat20 | TERAS | 66.67 | 1200.667 | 1138.0 | 2 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q1:cerun_ma50 | TERAS | 66.67 | 1148.667 | 1200.667 | 3 | SAMPEL KECIL |
| donchian20&q5:bb_lebar | UNIQUE | 33.33 | 600.333 | 12.193 | 1 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q1:rs_spy_6b | UNIQUE | 33.33 | 600.333 | 600.333 | 1 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| donchian20&q5:julat20 | UNIQUE | 33.33 | 600.333 | 17.418 | 1 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q5:sektor_1b | UNIQUE | 33.33 | 600.333 | 569.0 | 1 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q1:lapis | UNIQUE | 33.33 | 600.333 | 600.333 | 1 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| donchian20&q5:atr_pct | UNIQUE | 33.33 | 600.333 | 33.471 | 1 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| gap_and_go&q1:j_ma200 | UNIQUE | 33.33 | 574.333 | 600.333 | 2 | SAMPEL KECIL; BERGANTUNG PADA TEMA |
| b:gap_and_go | TERAS | 66.67 | 287.167 | 487.714 | 7 | SAMPEL KECIL |
| gap_and_go&q5:vol_n50 | TERAS | 66.67 | 287.167 | 487.714 | 7 | SAMPEL KECIL |
| pocket_pivot&q5:julat20 | TERAS | 66.67 | 127.63 | 32.514 | 21 |  |
| pocket_pivot&q5:atr_pct | TERAS | 66.67 | 104.424 | 44.921 | 20 |  |
| pocket_pivot&q5:bb_lebar | TERAS | 66.67 | 88.359 | 25.289 | 24 |  |
| macd_cross&q5:julat20 | TERAS | 66.67 | 76.578 | 71.125 | 23 |  |
| macd_cross&q5:atr_pct | TERAS | 66.67 | 76.578 | 75.867 | 25 |  |
| donchian20&q1:cerun_ma50 | UNIQUE | 33.33 | 71.792 | 58.862 | 9 | SAMPEL KECIL |
| macd_cross&q5:bb_lebar | TERAS | 66.67 | 52.212 | 69.673 | 31 |  |


### PEMICU YANG TIDAK MEMBEZAKAN

Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.


| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n |
|---|---|---|---|---|---|---|---|---|---|---|
| b:donchian20 | TIDAK BERGUNA | 1.41 | 0.0 | 9.17 | 8.14 | 0.154 | 0.173 | 1.25 | 0.304 | 160 |
| b:ema_crossback | TIDAK BERGUNA | 32.39 | 50.0 | 21.59 | 3.53 | 0.648 | 9.165 | 5.79 | 1.41 | 397 |
| b:gap_and_go | TIDAK BERGUNA | 1.41 | 0.0 | 0.23 | 0.14 | 6.067 | 10.304 | 42.86 | 10.431 | 7 |
| b:macd_cross | TIDAK BERGUNA | 25.35 | 0.0 | 20.08 | 4.37 | 1.262 | 5.796 | 5.46 | 1.33 | 366 |
| b:pocket_pivot | TIDAK BERGUNA | 33.8 | 0.0 | 18.46 | 8.71 | 1.832 | 3.881 | 7.56 | 1.839 | 344 |
| b:rsi_lintas50 | COMMON BIASA | 61.97 | 75.0 | 41.09 | 5.82 | 0.826 | 10.65 | 6.08 | 1.479 | 757 |


**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis yang diuji dalam kajian ini, dan ia disokong oleh data 2025.


### Corong ke Step 7
27 signal diteruskan (had 30; layak sebelum had: 27).


## 6. Step 5 — HOLD

> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana berjaya. Semua CALON.


### Kelas pullback

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| AMARAN | 4778 | 43.9 | -16.83 | 11.4 |
| PULLBACK PASARAN | 394 | 85.3 | -8.05 | 8.0 |
| PULLBACK SIHAT | 798 | 89.0 | -8.24 | 5.7 |


Pullback yang trend sahamnya utuh (SIHAT 89.0%, PASARAN 85.3%) menyambung ke puncak baru jauh lebih kerap daripada pullback AMARAN (43.9%). Ini sokongan paling jelas bagi falsafah "pegang selagi naik".


### Grid 18 peraturan HOLD (deskriptif)

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| X=5%,Y=ema9 | 2 | 100.0 | -5.0 | 1.5 |
| X=5%,Y=ema21 | 1322 | 91.8 | -7.13 | 5.3 |
| X=5%,Y=ma50 | 1963 | 88.1 | -8.45 | 7.1 |
| X=7%,Y=ema9 | 1164 | 91.8 | -5.88 | 5.1 |
| X=7%,Y=ema21 | 1650 | 91.6 | -6.91 | 5.4 |
| X=7%,Y=ma50 | 2218 | 88.8 | -8.16 | 6.9 |
| X=10%,Y=ema9 | 2221 | 87.9 | -7.09 | 6.6 |
| X=10%,Y=ema21 | 2338 | 88.0 | -7.4 | 6.6 |
| X=10%,Y=ma50 | 2638 | 87.0 | -8.24 | 7.1 |
| X=12%,Y=ema9 | 2736 | 85.1 | -7.81 | 7.6 |
| X=12%,Y=ema21 | 2789 | 85.0 | -7.97 | 7.6 |
| X=12%,Y=ma50 | 2965 | 84.2 | -8.54 | 7.8 |
| X=15%,Y=ema9 | 3388 | 79.4 | -8.9 | 8.5 |
| X=15%,Y=ema21 | 3408 | 79.4 | -8.97 | 8.4 |
| X=15%,Y=ma50 | 3501 | 78.8 | -9.3 | 8.5 |
| X=20%,Y=ema9 | 4224 | 70.5 | -10.58 | 9.3 |
| X=20%,Y=ema21 | 4233 | 70.4 | -10.61 | 9.3 |
| X=20%,Y=ma50 | 4277 | 70.0 | -10.78 | 9.3 |


### Common/unique HOLD (lulus FDR)

10 / 18 signal HOLD lulus BH-FDR q ≤ 0.01: `b:macd_atas0`, `b:bb_squeeze`, `b:ad_tinggi_baru`, `b:atas_awan`, `b:tenkan_atas`, `b:hammer`, `b:vcp`, `b:sektor_atas_ma50`, `b:supertrend_naik`, `b:psar_naik`


| nama | subset | n | K_padu | K_gagal | lift | presisi | lift_presisi | kelas |
|---|---|---|---|---|---|---|---|---|
| b:atas_ema21 | S1 | 673 | 19.94 | 1.63 | 12.252 | 93.16 | 1.769 | UNIQUE |
| b:supertrend_naik | S1 | 1780 | 51.72 | 5.45 | 9.491 | 91.35 | 1.735 | TERAS |
| b:vcp | S1 | 132 | 3.82 | 0.42 | 8.989 | 90.91 | 1.726 | LANGKA |
| b:bb_squeeze | S1 | 65 | 1.84 | 0.25 | 7.448 | 89.23 | 1.694 | TIDAK BERGUNA |
| b:atas_ma50 | S1 | 1612 | 45.61 | 6.3 | 7.241 | 88.96 | 1.689 | UNIQUE |
| b:psar_naik | S1 | 863 | 24.14 | 3.68 | 6.56 | 87.95 | 1.67 | UNIQUE |
| b:tenkan_atas | S1 | 2079 | 57.67 | 9.41 | 6.126 | 87.21 | 1.656 | TERAS |
| b:atas_awan | S1 | 1712 | 46.98 | 8.32 | 5.649 | 86.27 | 1.638 | UNIQUE |
| b:macd_atas0 | S1 | 2168 | 59.0 | 11.08 | 5.327 | 85.56 | 1.625 | TERAS |
| b:pullback_dalam_7pct | S1 | 3178 | 79.17 | 24.38 | 3.247 | 78.32 | 1.487 | TERAS |
| b:sektor_atas_ma50 | S1 | 1702 | 37.37 | 18.65 | 2.004 | 69.04 | 1.311 | SEDERHANA |
| b:sektor_naik | S1 | 1702 | 37.37 | 18.65 | 2.004 | 69.04 | 1.311 | SEDERHANA |
| b:ad_tinggi_baru | S1 | 63 | 1.37 | 0.71 | 1.933 | 68.25 | 1.296 | TIDAK BERGUNA |
| b:vcp | S2 | 33 | 5.43 | 0.53 | 10.16 | 96.97 | 1.278 | LANGKA |
| b:atas_ema21 | S2 | 177 | 28.69 | 4.28 | 6.707 | 95.48 | 1.258 | UNIQUE |
| b:supertrend_naik | S2 | 445 | 71.82 | 11.76 | 6.104 | 95.06 | 1.252 | TERAS |
| b:psar_naik | S2 | 187 | 30.05 | 5.35 | 5.62 | 94.65 | 1.247 | UNIQUE |
| b:tenkan_atas | S2 | 480 | 76.91 | 14.44 | 5.327 | 94.38 | 1.243 | TERAS |
| b:atas_ma50 | S2 | 412 | 65.87 | 12.83 | 5.133 | 94.17 | 1.241 | TERAS |
| b:atas_awan | S2 | 412 | 65.2 | 14.97 | 4.354 | 93.2 | 1.228 | TERAS |


## 7. Step 6 — EXIT (semua CALON)

> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.


| nama | n | pct_menyala | median_hari_dari_puncak | median_pulangan_exit | median_pct_kekal | kadar_exit_palsu |
|---|---|---|---|---|---|---|
| atr_lonjak_15x | 887 | 28.1 | 19.0 | -5.33 | -34.8 | 39.1 |
| bawah_ema21 | 3159 | 100.0 | -8.0 | -0.84 | -4.9 | 52.8 |
| bawah_ema9 | 3159 | 100.0 | -12.0 | -0.38 | -1.9 | 54.7 |
| bawah_ma50 | 3123 | 98.9 | -5.0 | -0.9 | -5.8 | 50.6 |
| chandelier_4atr | 2756 | 87.2 | 15.0 | -2.94 | -23.6 | 40.3 |
| climax_25_15h | 663 | 21.0 | -8.0 | 18.3 | 62.5 | 56.7 |
| div_macd | 2754 | 87.2 | -12.0 | 3.96 | 31.1 | 47.6 |
| div_rsi | 2447 | 77.5 | -10.0 | 5.16 | 39.8 | 47.5 |
| gap_besar | 212 | 6.7 | -3.0 | 26.59 | 76.9 | 50.0 |
| hari_agihan | 2520 | 79.8 | 7.0 | -0.14 | 1.0 | 43.9 |
| hist_neg3 | 3131 | 99.1 | -6.0 | 0.27 | 3.0 | 50.6 |
| jauh_ma50_2x | 1304 | 41.3 | -8.0 | 9.48 | 63.2 | 39.8 |
| macd_bawah | 3143 | 99.5 | 1.0 | 0.95 | 10.1 | 46.8 |
| pullback_amaran | 3115 | 98.6 | 22.0 | -7.19 | -52.2 | 67.5 |
| rsi_70_60 | 1990 | 63.0 | 1.0 | 7.11 | 46.2 | 46.2 |
| trail_10pct | 2920 | 92.4 | 9.0 | -2.91 | -20.2 | 44.0 |
| trail_15pct | 2313 | 73.2 | 17.0 | -7.69 | -54.9 | 47.2 |
| trail_2atr | 3147 | 99.6 | 3.0 | 0.11 | 3.5 | 44.4 |
| trail_3atr | 3045 | 96.4 | 9.0 | -1.04 | -6.9 | 40.3 |
| trail_8pct | 3066 | 97.1 | 6.0 | -1.56 | -9.4 | 43.2 |


`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala 5–12 hari sebelum puncak dan mengekalkan hanya -2% hingga -6% keuntungan. Kadar exit palsu 39%–68%.


**Keluarga EXIT: 0 / 62 signal lulus BH-FDR q ≤ 0.01.** Tiada signal EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas kawalan pelbagai ujian.


## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)

Setiap signal corong diimbas atas **semua** hari universe 2021 (596,955 baris (ticker, hari); 503,786 selepas topeng universe). Kadar asas KAWALAN RAWAK (MFE63 ≥ 30%) = 10.87%.


| signal | n_kemunculan | kadar_tepat_mfe30 | lift_tepat | kadar_palsu_bawah10 | kadar_tepat_bertangga | ketulenan_trend_median | mfe63_p50 | mfe63_p75 | mfe63_p90 | pct_mfe63_ge30 | pct_mfe63_ge100 | mfe252_p90 | pct_mfe252_ge100 | median_hari_mfe63 | jangkaan_henti2atr | kadar_menang | kapasiti | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | 5072 | 22.18 | 2.041 | 42.94 | 2.46 | 76.2 | 12.79 | 27.73 | 47.07 | 22.18 | 1.66 | 95.03 | 9.15 | 21.0 | -3.777 | 26.12 | PELENGKAP |  |
| rsi_lintas50&q5:bb_lebar | 4733 | 22.14 | 2.037 | 42.47 | 2.62 | 76.9 | 12.89 | 27.54 | 46.47 | 22.14 | 1.61 | 93.21 | 8.77 | 22.0 | -3.203 | 27.93 | PELENGKAP |  |
| q5:julat20 | 134058 | 19.89 | 1.83 | 43.11 | 2.12 | 66.1 | 12.47 | 25.52 | 44.33 | 19.89 | 1.29 | 86.05 | 7.65 | 23.0 | -3.902 | 27.04 | PELENGKAP |  |
| macd_cross&q5:bb_lebar | 4646 | 20.15 | 1.853 | 43.24 | 1.87 | 70.8 | 12.55 | 25.57 | 44.05 | 20.15 | 1.53 | 86.24 | 7.99 | 24.0 | -4.299 | 25.87 | PELENGKAP |  |
| pocket_pivot&q1:j_52w_tinggi | 5753 | 17.24 | 1.586 | 44.46 | 1.81 | 88.5 | 11.98 | 23.65 | 39.37 | 17.24 | 1.3 | 64.47 | 4.5 | 19.0 | -5.159 | 21.17 | PELENGKAP |  |
| ema_crossback&q5:julat20 | 3357 | 23.8 | 2.19 | 40.96 | 2.65 | 77.6 | 13.77 | 28.99 | 48.88 | 23.8 | 1.88 | 102.0 | 10.31 | 22.0 | -2.687 | 29.01 | PELENGKAP |  |
| ema_crossback&q5:bb_lebar | 3116 | 23.04 | 2.12 | 41.4 | 2.82 | 77.8 | 13.42 | 28.25 | 47.34 | 23.04 | 1.86 | 99.21 | 9.92 | 23.0 | -2.407 | 30.2 | PELENGKAP |  |
| rsi_lintas50&q5:atr_pct | 5284 | 23.52 | 2.164 | 42.37 | 2.42 | 76.2 | 13.09 | 28.85 | 48.9 | 23.52 | 1.85 | 98.58 | 9.75 | 19.0 | -4.54 | 24.74 | PELENGKAP |  |
| q5:j_ema9 | 52861 | 16.03 | 1.474 | 45.35 | 2.03 | 91.9 | 11.51 | 22.69 | 38.87 | 16.03 | 1.1 | 78.58 | 6.25 | 27.0 | -2.715 | 26.49 | PELENGKAP | BUNYI LATAR |
| q5:bb_lebar | 145950 | 18.17 | 1.672 | 43.83 | 2.05 | 70.0 | 12.1 | 24.21 | 41.77 | 18.17 | 1.13 | 81.19 | 6.87 | 25.0 | -3.408 | 27.61 | PELENGKAP |  |
| q5:atr_pct | 101770 | 23.39 | 2.152 | 41.33 | 2.15 | 61.2 | 13.47 | 28.57 | 49.75 | 23.39 | 1.73 | 96.74 | 9.42 | 20.0 | -5.061 | 25.57 | PELENGKAP |  |
| rsi_lintas50&q5:cerun_ma50 | 4706 | 17.93 | 1.65 | 41.5 | 3.36 | 77.8 | 13.21 | 25.06 | 39.1 | 17.93 | 0.7 | 80.93 | 6.16 | 29.0 | -0.092 | 34.85 | PELENGKAP |  |
| ema_crossback&q5:atr_pct | 3342 | 25.31 | 2.329 | 40.01 | 2.51 | 77.1 | 14.2 | 30.25 | 51.21 | 25.31 | 2.15 | 108.09 | 11.49 | 20.0 | -3.509 | 27.23 | PELENGKAP |  |
| ema_crossback&q5:cerun_ma50 | 5966 | 17.55 | 1.614 | 41.94 | 2.7 | 80.0 | 12.83 | 24.56 | 38.66 | 17.55 | 0.77 | 79.82 | 5.98 | 30.0 | -0.335 | 33.66 | PELENGKAP |  |
| pocket_pivot&q1:cerun_ma50 | 4644 | 13.78 | 1.268 | 46.34 | 1.72 | 84.1 | 11.1 | 21.16 | 34.79 | 13.78 | 0.93 | 61.23 | 4.46 | 25.0 | -4.562 | 22.78 | PELENGKAP |  |
| rsi_lintas50&q5:j_ma200 | 4343 | 20.01 | 1.841 | 41.93 | 3.27 | 78.0 | 13.16 | 26.22 | 42.45 | 20.01 | 1.27 | 93.36 | 8.63 | 28.0 | -0.327 | 33.99 | PELENGKAP |  |
| ema_crossback&q5:j_ma200 | 4932 | 19.81 | 1.822 | 41.63 | 2.86 | 80.0 | 13.17 | 25.81 | 41.32 | 19.81 | 1.09 | 90.91 | 7.93 | 28.0 | -0.381 | 33.76 | PELENGKAP |  |
| pocket_pivot&q5:rs_spy_6b | 11295 | 18.1 | 1.665 | 42.01 | 2.38 | 90.6 | 12.72 | 24.39 | 40.96 | 18.1 | 1.21 | 87.18 | 7.48 | 30.0 | -1.14 | 29.19 | PELENGKAP |  |
| macd_cross&q1:j_52w_tinggi | 4555 | 17.26 | 1.587 | 43.51 | 1.49 | 65.2 | 12.06 | 23.19 | 38.69 | 17.26 | 0.97 | 66.88 | 5.09 | 25.0 | -4.352 | 25.6 | PELENGKAP |  |
| rsi_lintas50&q5:rs_spy_6b | 4762 | 18.82 | 1.731 | 43.85 | 2.86 | 78.7 | 12.31 | 24.87 | 41.06 | 18.82 | 1.28 | 91.34 | 8.29 | 27.0 | -0.897 | 33.18 | PELENGKAP |  |
| q5:j_52w_rendah | 91019 | 23.02 | 2.118 | 36.89 | 2.96 | 77.8 | 14.97 | 28.45 | 47.25 | 23.02 | 1.42 | 97.66 | 9.52 | 29.0 | -0.793 | 32.83 | PELENGKAP |  |
| ema_crossback&q5:rs_spy_6b | 4921 | 18.19 | 1.673 | 43.1 | 2.52 | 80.0 | 12.4 | 24.39 | 39.76 | 18.19 | 1.02 | 89.06 | 7.82 | 28.0 | -0.854 | 33.29 | PELENGKAP |  |
| macd_cross&q1:cerun_ma50 | 4574 | 13.51 | 1.243 | 46.7 | 1.42 | 62.5 | 10.95 | 20.24 | 34.45 | 13.51 | 0.61 | 60.87 | 4.15 | 28.0 | -3.178 | 28.36 | PELENGKAP |  |
| q1:roc20 | 140224 | 13.02 | 1.198 | 45.62 | 1.66 | 54.2 | 11.22 | 20.62 | 34.13 | 13.02 | 0.51 | 62.42 | 4.06 | 30.0 | -1.613 | 33.22 | PELENGKAP | BUNYI LATAR |
| pocket_pivot&q1:lapis | 3410 | 10.15 | 0.933 | 48.48 | 1.41 | 82.7 | 10.32 | 18.8 | 30.21 | 10.15 | 0.65 | 48.57 | 2.43 | 26.0 | -3.55 | 25.98 | PELENGKAP |  |
| q1:j_52w_tinggi | 114805 | 17.09 | 1.572 | 43.62 | 1.81 | 57.4 | 12.08 | 23.38 | 39.71 | 17.09 | 0.92 | 68.05 | 5.05 | 24.0 | -3.958 | 27.18 | PELENGKAP |  |
| rsi_lintas50&q1:j_52w_tinggi | 5651 | 17.36 | 1.597 | 44.84 | 2.0 | 76.9 | 11.65 | 23.48 | 39.66 | 17.36 | 1.03 | 68.18 | 5.03 | 22.0 | -3.941 | 24.63 | PELENGKAP |  |


Taburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. p90 dan % ≥ 100% ialah pembeza, bukan median.


**Lift jatuh besar antara Step 4 dan Step 7** (contoh `rsi_lintas50&q5:julat20`: lift 11.58 dalam populasi peristiwa → lift_tepat 2.04 atas semua hari universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. Angka Step 7 yang lebih dekat dengan dagangan sebenar.


### Penapis Step 7.4
216 kombinasi signal × penapis diuji (0 lulus kriteria "buang ≥ 30% palsu dan ≤ 10% benar").


**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis dipradaftar. Ini keputusan negatif yang bersih.


10 contoh penapis terbaik (ikut % palsu dibuang):


| signal | buang_palsu_pct | buang_benar_pct |
|---|---|---|
| pocket_pivot&q1:lapis | penapis:lapis_ge_3 | 100.0 | 100.0 |
| macd_cross&q1:cerun_ma50 | penapis:lapis_ge_3 | 98.7 | 97.6 |
| macd_cross&q1:j_52w_tinggi | penapis:lapis_ge_3 | 94.4 | 84.6 |
| macd_cross&q1:cerun_ma50 | penapis:harga_atas_ma50 | 91.1 | 90.1 |
| q1:roc20 | penapis:harga_atas_ma50 | 90.2 | 88.5 |
| ema_crossback&q5:cerun_ma50 | penapis:vol_n50_ge_1.5 | 89.8 | 90.2 |
| ema_crossback&q5:rs_spy_6b | penapis:vol_n50_ge_1.5 | 89.4 | 89.5 |
| rsi_lintas50&q5:cerun_ma50 | penapis:vol_n50_ge_1.5 | 89.4 | 89.6 |
| ema_crossback&q5:j_ma200 | penapis:vol_n50_ge_1.5 | 89.1 | 89.6 |
| rsi_lintas50&q5:rs_spy_6b | penapis:vol_n50_ge_1.5 | 88.8 | 88.6 |


## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)

Set kemasukan: gabungan semua kemunculan 25 signal yang lulus Step 7 = 244,702 (ticker, tarikh) unik, disampel berlapis ikut bulan ke **24,000** (benih 42; SPEC §13.9). Grid 18 HOLD × 13 EXIT = **234** sistem.


### TIGA RUJUKAN WAJIB

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_menang | purata_kalah | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 | pct_terpotong_data | siri_kalah_terpanjang |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_jual_hari63 | 24000 | -3.11 | -2.81 | -2.809 | 43.87 | 18.41 | 19.4 | 63.0 | -13.47 | 64.1 | 0.0 | 0.0 | 29 |
| REF_chandelier_4atr | 24000 | -6.92 | -3.42 | -3.418 | 33.06 | 19.17 | 14.57 | 53.2 | -10.0 | 68.8 | 0.1 | 0.0 | 42 |
| REF_pegang_252 | 24000 | -22.41 | -19.13 | -19.134 | 29.1 | 34.09 | 40.98 | 252.0 | -35.52 | 0.0 | 100.0 | 0.0 | 38 |


**Keputusan: 196 / 234 sistem mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = -2.809%, "jual hari ke-63"). Ini berlaku kerana rujukan itu sendiri lemah tahun ini, bukan semestinya kerana sistem itu kuat.


Ukuran mutlak, bukan kedudukan: **0 / 234** sistem berjangkaan positif dan **0 / 234** bermedian pulangan positif. Ambang rujukan NEGATIF tahun ini, jadi "mengalahkan rujukan" boleh bermakna sekadar kurang rugi.

Semuanya masih perlu melalui FDR keluarga SISTEM dalam Step 8 (173/234 lulus q ≤ 0.01).


### 15 sistem terbaik daripada 234

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 |
|---|---|---|---|---|---|---|---|---|---|
| bawah_ema9|X=5%,Y=ema9 | 24000 | -1.26 | -0.52 | -0.522 | 34.8 | 5.2 | -2.16 | 70.7 | 0.0 |
| bawah_ema9|X=7%,Y=ema9 | 24000 | -1.26 | -0.52 | -0.522 | 34.8 | 5.2 | -2.16 | 70.7 | 0.0 |
| bawah_ema9|X=15%,Y=ema9 | 24000 | -1.26 | -0.52 | -0.522 | 34.8 | 5.2 | -2.16 | 70.7 | 0.0 |
| bawah_ema9|X=12%,Y=ema9 | 24000 | -1.26 | -0.52 | -0.522 | 34.8 | 5.2 | -2.16 | 70.7 | 0.0 |
| bawah_ema9|X=10%,Y=ema9 | 24000 | -1.26 | -0.52 | -0.522 | 34.8 | 5.2 | -2.16 | 70.7 | 0.0 |
| bawah_ema9|X=20%,Y=ema9 | 24000 | -1.26 | -0.52 | -0.522 | 34.8 | 5.2 | -2.16 | 70.7 | 0.0 |
| bawah_ema9|X=5%,Y=ema21 | 24000 | -1.44 | -0.62 | -0.621 | 34.04 | 6.4 | -2.46 | 70.6 | 0.0 |
| bawah_ema9|X=7%,Y=ema21 | 24000 | -1.49 | -0.66 | -0.663 | 33.58 | 6.8 | -2.53 | 70.6 | 0.0 |
| bawah_ema9|X=5%,Y=ma50 | 24000 | -1.58 | -0.69 | -0.695 | 34.01 | 7.3 | -2.67 | 70.6 | 0.0 |
| trail_8pct|X=7%,Y=ema21 | 24000 | -4.0 | -0.72 | -0.724 | 34.76 | 22.9 | -6.08 | 69.0 | 0.0 |
| trail_8pct|X=5%,Y=ema21 | 24000 | -4.0 | -0.72 | -0.724 | 34.76 | 22.9 | -6.08 | 69.0 | 0.0 |
| trail_8pct|X=5%,Y=ma50 | 24000 | -4.0 | -0.72 | -0.724 | 34.76 | 22.9 | -6.08 | 69.0 | 0.0 |
| trail_8pct|X=7%,Y=ma50 | 24000 | -4.0 | -0.72 | -0.724 | 34.76 | 22.9 | -6.08 | 69.0 | 0.0 |
| trail_8pct|X=5%,Y=ema9 | 24000 | -4.0 | -0.72 | -0.724 | 34.76 | 22.9 | -6.08 | 69.0 | 0.0 |
| trail_8pct|X=7%,Y=ema9 | 24000 | -4.0 | -0.72 | -0.724 | 34.76 | 22.9 | -6.08 | 69.0 | 0.0 |


Perhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.


## 10. Step 8 — kawalan kebetulan

### Ujian label rawak dan FDR per keluarga

| keluarga | N | lulus_fdr | ambang_p |
|---|---|---|---|
| ENTRY/PADU | 27 | 22 | 0.004995004995004995 |
| ENTRY/SUPER PADU | 27 | 10 | 0.000999000999000999 |
| HOLD | 18 | 10 | 0.004975124378109453 |
| EXIT | 62 | 0 |  |
| SISTEM | 234 | 173 | 0.005 |


Perbandingan yang diminta arahan: **22 signal lulus FDR daripada 27 diuji**, manakala label rawak menghasilkan lift purata yang jauh lebih rendah (lajur `lift_purata_rawak` dalam `kawalan_rawak_bootstrap_2021.csv`).


### Jangkaan atas SEMUA kemunculan + ujian outlier

| signal | n_kemunculan | median_pulangan | jangkaan | jangkaan_tanpa_5pct_teratas | pct_rugi_lebih_10 | siri_kalah_terpanjang | jangkaan_bawah95_blok_ticker | jangkaan_bawah95_blok_minggu |
|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | 5072 | -11.53 | -3.777 | -7.772 | 58.5 | 38 | -4.763 | -5.433 |
| rsi_lintas50&q5:bb_lebar | 4733 | -11.03 | -3.203 | -7.124 | 55.7 | 38 | -4.126 | -5.058 |
| q5:julat20 | 134058 | -10.48 | -3.902 | -7.54 | 52.7 | 334 | -4.457 | -5.073 |
| macd_cross&q5:bb_lebar | 4646 | -10.72 | -4.299 | -7.935 | 53.7 | 28 | -5.008 | -5.809 |
| pocket_pivot&q1:j_52w_tinggi | 5753 | -9.81 | -5.159 | -8.154 | 48.7 | 56 | -5.972 | -6.55 |
| ema_crossback&q5:julat20 | 3357 | -11.14 | -2.687 | -6.75 | 55.6 | 36 | -3.851 | -4.789 |
| ema_crossback&q5:bb_lebar | 3116 | -10.47 | -2.407 | -6.346 | 52.2 | 31 | -3.563 | -4.689 |
| rsi_lintas50&q5:atr_pct | 5284 | -12.64 | -4.54 | -8.68 | 66.7 | 60 | -5.603 | -5.953 |
| q5:j_ema9 | 52861 | -7.97 | -2.715 | -5.783 | 36.4 | 103 | -3.181 | -3.775 |
| q5:bb_lebar | 145950 | -9.24 | -3.408 | -6.835 | 46.0 | 334 | -3.901 | -4.472 |
| q5:atr_pct | 101770 | -12.89 | -5.061 | -9.167 | 66.3 | 336 | -5.831 | -6.407 |
| rsi_lintas50&q5:cerun_ma50 | 4706 | -6.97 | -0.092 | -3.164 | 34.3 | 32 | -0.899 | -2.569 |
| ema_crossback&q5:atr_pct | 3342 | -12.33 | -3.509 | -7.811 | 62.9 | 45 | -4.81 | -5.386 |
| ema_crossback&q5:cerun_ma50 | 5966 | -6.86 | -0.335 | -3.345 | 32.5 | 26 | -0.972 | -2.402 |
| pocket_pivot&q1:cerun_ma50 | 4644 | -8.23 | -4.562 | -7.007 | 38.8 | 48 | -5.218 | -5.287 |
| rsi_lintas50&q5:j_ma200 | 4343 | -8.02 | -0.327 | -4.053 | 38.9 | 27 | -1.363 | -2.468 |
| ema_crossback&q5:j_ma200 | 4932 | -7.65 | -0.381 | -3.765 | 35.8 | 26 | -1.32 | -2.459 |
| pocket_pivot&q5:rs_spy_6b | 11295 | -7.54 | -1.14 | -4.625 | 33.3 | 52 | -1.91 | -2.645 |
| macd_cross&q1:j_52w_tinggi | 4555 | -9.34 | -4.352 | -7.394 | 46.2 | 33 | -4.925 | -5.744 |
| rsi_lintas50&q5:rs_spy_6b | 4762 | -7.95 | -0.897 | -4.495 | 38.7 | 35 | -1.849 | -2.793 |
| q5:j_52w_rendah | 91019 | -8.6 | -0.793 | -4.536 | 42.3 | 241 | -1.573 | -2.007 |
| ema_crossback&q5:rs_spy_6b | 4921 | -7.47 | -0.854 | -4.076 | 34.8 | 30 | -1.669 | -2.612 |
| macd_cross&q1:cerun_ma50 | 4574 | -7.51 | -3.178 | -5.856 | 36.2 | 29 | -3.668 | -4.514 |
| q1:roc20 | 140224 | -6.44 | -1.613 | -4.342 | 31.7 | 258 | -1.978 | -2.551 |
| pocket_pivot&q1:lapis | 3410 | -7.08 | -3.55 | -5.831 | 33.4 | 35 | -4.193 | -4.444 |
| q1:j_52w_tinggi | 114805 | -9.37 | -3.958 | -7.19 | 46.7 | 352 | -4.524 | -5.135 |
| rsi_lintas50&q1:j_52w_tinggi | 5651 | -9.32 | -3.941 | -7.06 | 45.3 | 50 | -4.696 | -5.221 |


### Keputusan gate demi gate

| signal | G1_sah_dalam_tahun | G2_merentas_tahun | G3_nilai_p | G3_fdr | G4_bootstrap | G5_outlier | G6 | step7 | keputusan |
|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2020=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:julat20 | SEBAHAGIAN | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=LANGKA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=LANGKA; 2023=LANGKA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:julat20 | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=LANGKA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=LANGKA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:atr_pct | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=LANGKA; 2022=UNIQUE; 2023=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.68132 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:j_ema9 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q5:bb_lebar | GAGAL | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=SEDERHANA; 2025=TERAS) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:atr_pct | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2022=UNIQUE; 2023=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.25275 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:cerun_ma50 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:atr_pct | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.002 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:cerun_ma50 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:j_ma200 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:j_ma200 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q5:rs_spy_6b | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.01499 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q1:j_52w_tinggi | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=LANGKA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.005 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:rs_spy_6b | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:j_52w_rendah | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=SEDERHANA; 2023=SEDERHANA; 2024=-; 2025=-) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | STATISTIK SAHAJA | LULUS | DITOLAK |
| ema_crossback&q5:rs_spy_6b | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=LANGKA; 2022=TIDAK BERGUNA; 2023=LANGKA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:roc20 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2022=SEDERHANA; 2023=TIDAK BERGUNA; 2024=SEDERHANA; 2025=UNIQUE) | 0.52448 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| pocket_pivot&q1:lapis | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.002 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:j_52w_tinggi | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2022=UNIQUE; 2023=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.08891 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |


**DITERIMA: 0** · **CALON: 0** · **DITOLAK: 27.**


Tiada CALON. Gate yang membunuh semua signal ialah **G4 (bootstrap)** dan **G5 (outlier)**: jangkaan tidak bertahan pada had bawah 95% blok ticker atau blok minggu, dan jatuh ke ≤ 0 apabila 5% pemenang teratas dibuang. Maknanya pulangan signal tahun ini datang daripada beberapa kemunculan melampau, bukan daripada kelebihan yang boleh diulang.


Penapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam ≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada 2021.


## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)

Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. Asas signal ENTRY: **lulus Step 7 sahaja (TIADA signal CALON tahun ini)**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → RS 6 bulan → ticker.


> Angka di bawah **bukan** bukti sistem lulus — tiada signal ENTRY tahun ini lulus Step 8. Ia dilaporkan supaya kriteria akhir ada angka dan baris merentas tahun setara (SPEC §13.10).


| sistem | n_posisi_dibuka | n_dagangan_ditutup | n_posisi_terbuka_hujung_tahun | purata_slot_terisi | pulangan_tahun | median_bulanan | purata_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terbaik | bulan_terburuk | mdd | purata_hari_pegang | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 8 | 0 | 8 | 7.94 | 12.28 | 1.02 | 1.06 | 8.3 | 58.3 | 10.54 | -5.16 | -22.16 |  | 0.7 | 30.51 | -5.11 |
| REF_chandelier_4atr | 46 | 38 | 8 | 7.79 | -2.15 | -0.25 | 0.19 | 25.0 | 50.0 | 12.4 | -13.16 | -33.56 | 49.5 | 3.8 | 30.51 | -5.11 |
| REF_jual_hari63 | 40 | 32 | 8 | 7.81 | 5.24 | 1.71 | 0.97 | 16.7 | 66.7 | 25.91 | -17.18 | -39.51 | 63.0 | 3.3 | 30.51 | -5.11 |
| bawah_ema9|X=5%,Y=ema9 | 415 | 407 | 8 | 6.32 | -34.84 | -4.39 | -3.05 | 8.3 | 25.0 | 17.31 | -17.46 | -52.58 | 5.8 | 34.6 | 30.51 | -5.11 |
| bawah_ema9|X=7%,Y=ema9 | 415 | 407 | 8 | 6.32 | -34.84 | -4.39 | -3.05 | 8.3 | 25.0 | 17.31 | -17.46 | -52.58 | 5.8 | 34.6 | 30.51 | -5.11 |
| bawah_ema9|X=15%,Y=ema9 | 415 | 407 | 8 | 6.32 | -34.84 | -4.39 | -3.05 | 8.3 | 25.0 | 17.31 | -17.46 | -52.58 | 5.8 | 34.6 | 30.51 | -5.11 |
| KAWALAN_RAWAK|pegang_252 | 8 | 0 | 8 | 7.94 | 2.39 | 0.14 | 0.25 | 0.0 | 50.0 | 6.33 | -4.41 | -13.33 |  | 0.7 | 30.51 | -5.11 |
| KAWALAN_RAWAK|chandelier | 44 | 36 | 8 | 7.79 | -0.3 | 0.28 | 0.05 | 0.0 | 58.3 | 6.77 | -6.99 | -19.0 | 51.6 | 3.7 | 30.51 | -5.11 |


### Pulangan bulanan penuh (%)

| tarikh | REF_pegang_252 | REF_chandelier_4atr | REF_jual_hari63 | bawah_ema9|X=5%,Y=ema9 | bawah_ema9|X=7%,Y=ema9 | bawah_ema9|X=15%,Y=ema9 | KAWALAN_RAWAK|pegang_252 | KAWALAN_RAWAK|chandelier |
|---|---|---|---|---|---|---|---|---|
| 2021-01-31 | 10.54 | 10.54 | 10.54 | 7.42 | 7.42 | 7.42 | -0.16 | -0.57 |
| 2021-02-28 | 2.07 | 4.55 | 2.07 | -8.95 | -8.95 | -8.95 | 0.43 | 2.75 |
| 2021-03-31 | -5.16 | -2.84 | -5.16 | -6.81 | -6.81 | -6.81 | 6.33 | 1.94 |
| 2021-04-30 | 1.09 | 0.32 | -17.18 | -17.46 | -17.46 | -17.46 | 1.39 | 6.77 |
| 2021-05-31 | 0.95 | 6.22 | 0.61 | -4.51 | -4.51 | -4.51 | 0.6 | 2.29 |
| 2021-06-30 | 3.92 | 12.4 | 25.91 | 7.4 | 7.4 | 7.4 | -0.59 | -1.97 |
| 2021-07-31 | 3.4 | -11.57 | -13.65 | -15.93 | -15.93 | -15.93 | -1.42 | 0.11 |
| 2021-08-31 | 5.7 | 11.83 | 1.35 | -1.54 | -1.54 | -1.54 | -4.41 | -2.4 |
| 2021-09-30 | -4.59 | -8.08 | 3.28 | -4.26 | -4.26 | -4.26 | -4.25 | -6.99 |
| 2021-10-31 | -2.94 | -0.81 | 2.32 | 17.31 | 17.31 | 17.31 | 3.34 | 4.22 |
| 2021-11-30 | -1.77 | -13.16 | -3.3 | -7.5 | -7.5 | -7.5 | -3.11 | -6.03 |
| 2021-12-31 | -0.48 | -7.08 | 4.83 | -1.77 | -1.77 | -1.77 | 4.82 | 0.46 |


### Jawapan terus kepada sasaran +10% sebulan

**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:


- `REF_pegang_252`: median bulanan **1.02%**, 8.3% bulan ≥ +10%, bulan terburuk -5.16%, MDD -22.16%, pulangan tahun 12.28% (SPY 30.51%, MDD SPY -5.11%)

- `REF_chandelier_4atr`: median bulanan **-0.25%**, 25.0% bulan ≥ +10%, bulan terburuk -13.16%, MDD -33.56%, pulangan tahun -2.15% (SPY 30.51%, MDD SPY -5.11%)

- `REF_jual_hari63`: median bulanan **1.71%**, 16.7% bulan ≥ +10%, bulan terburuk -17.18%, MDD -39.51%, pulangan tahun 5.24% (SPY 30.51%, MDD SPY -5.11%)

- `bawah_ema9|X=5%,Y=ema9`: median bulanan **-4.39%**, 8.3% bulan ≥ +10%, bulan terburuk -17.46%, MDD -52.58%, pulangan tahun -34.84% (SPY 30.51%, MDD SPY -5.11%)

- `bawah_ema9|X=7%,Y=ema9`: median bulanan **-4.39%**, 8.3% bulan ≥ +10%, bulan terburuk -17.46%, MDD -52.58%, pulangan tahun -34.84% (SPY 30.51%, MDD SPY -5.11%)

- `bawah_ema9|X=15%,Y=ema9`: median bulanan **-4.39%**, 8.3% bulan ≥ +10%, bulan terburuk -17.46%, MDD -52.58%, pulangan tahun -34.84% (SPY 30.51%, MDD SPY -5.11%)

- `KAWALAN_RAWAK|pegang_252`: median bulanan **0.14%**, 0.0% bulan ≥ +10%, bulan terburuk -4.41%, MDD -13.33%, pulangan tahun 2.39% (SPY 30.51%, MDD SPY -5.11%)

- `KAWALAN_RAWAK|chandelier`: median bulanan **0.28%**, 0.0% bulan ≥ +10%, bulan terburuk -6.99%, MDD -19.00%, pulangan tahun -0.30% (SPY 30.51%, MDD SPY -5.11%)


**Apa yang menghalang — kapasiti, bukan kadar menang.**

- Sistem terbaik (`REF_pegang_252`) hanya membuka **8 posisi sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh dijadikan asas keputusan.

- Sistem yang pusing ganti mencukupi (Chandelier: 46 posisi, 3.8/bulan) memberi median bulanan hanya -0.25% dengan MDD -33.56% — lebih buruk daripada MDD SPY.

- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.

- KAWALAN RAWAK pegang-252 memberi 2.39% dan Chandelier rawak -0.30% — dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.


### Banding wajib: SPY dan KAWALAN RAWAK

- SPY tempoh sama: **30.51%** (MDD -5.11%). **6/6** sistem kalah kepada SPY.

- KAWALAN RAWAK terbaik: **2.39%** (`KAWALAN_RAWAK|pegang_252`). **4/6** sistem kalah kepada entri rawak.


> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.


## 12. Keputusan akhir (had fasa: CALON)

1. **ENTRY** — TIADA signal CALON pada 2021. Semua gagal G4 (bootstrap) dan/atau G5 (outlier). Pemicu klasik tunggal juga tidak lulus.

2. **HOLD** — 10/18 signal lulus FDR; kelas pullback ialah hasil paling kukuh (SIHAT 89.0% / PASARAN 85.3% menyambung ke puncak baru lawan AMARAN 43.9%).

3. **EXIT** — 0/62 signal lulus FDR; 196/234 sistem mengalahkan ketiga-tiga rujukan dan 173/234 lulus FDR keluarga SISTEM. **Tahun ini exit aktif berbaloi** kerana memegang tanpa jual hampir tidak menguntungkan.

4. **PORTFOLIO** — sasaran +10% sebulan tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila pegangan panjang, bukan kadar menang.

5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam ≥ 2 tahun LAIN; tahun lain yang siap: [2020, 2022, 2023, 2024, 2025]. Lihat `BANDING_TAHUN.md` untuk status merentas tahun.


## 13. Fail output

| Fail | Isi |
|---|---|
| `runs_2021.csv` | 4413 run, 34 lajur |
| `monthly_summary_2021.csv` | ringkasan 12 bulan |
| `skipped_2021.csv` | 17105 calon ditolak + sebab |
| `kohort_masih_naik_2021.csv` | 315 run masih_naik dijejak 252 hari |
| `common_unique_2021.csv` | 3408 baris (213 signal × subset × populasi × kumpulan × keluarga) |
| `taburan_indikator_2021.csv` | median + p25/p75 setiap indikator setiap hasil |
| `hold_exit_2021.csv` | 357 baris CALON HOLD/EXIT |
| `false_signal_2021.csv` | 243 baris (signal + penapis) |
| `hadapan_hold_exit_2021.csv` | 237 sistem (234 + 3 rujukan) |
| `kawalan_rawak_bootstrap_2021.csv` | nilai-p label rawak + had bawah bootstrap |
| `jangkaan_kemunculan_2021.csv` | jangkaan + ujian outlier |
| `keputusan_2021.csv` | keputusan gate demi gate |
| `portfolio_2021.csv`, `portfolio_bulanan_2021.csv` | Step 9 |
| `log_ujian.csv` | setiap signal/kombinasi yang diuji |
| `PANDANG_HADAPAN_2021.md` | imbasan pandang ke hadapan |
| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |
