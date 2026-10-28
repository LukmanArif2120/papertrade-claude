# LAPORAN REVERSE 2022 — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.

> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = **satu rejim pasaran**. Peta sektor bukan titik-masa. Gate 8.1 ada 5 tahun lain ([2020, 2021, 2023, 2024, 2025]); keputusan **maksimum CALON** (SPEC §11.8).

## 0. Jawapan ringkas

1. **5541 run layak** dikenal pasti dalam 2022; setiap 12 bulan ada calon (tiada "TIADA CALON"). 52 SUPER PADU (≥100%), 2363 PADU, 3126 BIASA.

2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada 297 run yang masih naik pada hari ke-63, **18.2% akhirnya melebihi +100%**, dengan median kenaikan penuh **62.7%** lawan 40.0% pada hari ke-63.

3. **Signal entry: TIADA CALON** daripada 21 yang masuk corong. 21 gagal gate bootstrap (G4) dan 21 ditanda BERGANTUNG PADA OUTLIER (G5). Ini keputusan, bukan kegagalan teknikal: tiada signal ENTRY tahun ini bertahan selepas had bawah 95% bootstrap blok dan ujian tanpa 5% pemenang teratas.

4. **14 daripada 234 sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan** — berbeza daripada tahun lain. Rujukan terbaik hanya +0.55% setiap dagangan ("pegang tanpa jual hingga hari ke-252"): +0.55% (pegang tanpa jual hingga hari ke-252), -3.17% (jual hari ke-63), -4.77% (Chandelier 4×ATR14). Apabila memegang tanpa jual tidak lagi menguntungkan, exit aktif baru berbaloi.

5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan pegang-252 hanya membuka **8 posisi sepanjang tahun** (8 slot terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. Pulangannya -16.00% ialah hasil **8 saham**, bukan sistem.

6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik ialah 2.38% sebulan (median) dengan MDD -24.96%.

7. **Keluarga EXIT dan SISTEM pada FDR:** 0/66 signal EXIT dan 0/234 sistem lulus q ≤ 0.01.

## 1. Semakan kesediaan Step 0

| Semakan | Hasil |
|---|---|
| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, 2009-01-02 → 2026-10-16; semua sha256 sepadan |
| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |
| c. Sumber sektor/industri setiap ticker | **LULUS** — 2320/2330 = 99.6% (2 kelas saham diisi daripada ticker asas; 103 ticker = `Lain-lain`) |
| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 (indeks sektor A02; diluluskan pengguna) |
| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — 0.125 s/ticker; larian penuh 2330 ticker = 292 s |
| f. `semak_hadapan` atas modul indikator | **LULUS** — 14 tarikh potong (≥ 12), 26,950 perbandingan, **0 kegagalan** (`REVERSE/PANDANG_HADAPAN_2022.md`) |

## 2. Step 1–2 — run

Saiz universe 2022 setiap bulan: min **2000**, median **2000**, maks **2000**; 2330 ticker berbeza sepanjang tahun.

| bulan | n_run | n_super | n_padu | n_biasa | n_bertangga | n_lonjakan | n_stabil | n_entry_sah | n_masih_naik | n_peristiwa | med_naik |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2022-01 | 659 | 10 | 262 | 387 | 43 | 450 | 166 | 361 | 7 | 868 | 25.0 |
| 2022-02 | 381 | 1 | 105 | 275 | 20 | 190 | 171 | 256 | 14 | 1415 | 22.6 |
| 2022-03 | 523 | 4 | 142 | 377 | 6 | 353 | 164 | 427 | 11 | 1774 | 21.9 |
| 2022-04 | 327 | 0 | 89 | 238 | 4 | 260 | 63 | 171 | 16 | 867 | 18.7 |
| 2022-05 | 675 | 14 | 365 | 296 | 28 | 402 | 245 | 372 | 172 | 1912 | 32.1 |
| 2022-06 | 606 | 2 | 291 | 313 | 28 | 161 | 417 | 330 | 16 | 1228 | 29.6 |
| 2022-07 | 490 | 5 | 114 | 371 | 22 | 159 | 309 | 429 | 4 | 1306 | 21.6 |
| 2022-08 | 104 | 0 | 30 | 74 | 1 | 70 | 33 | 67 | 13 | 635 | 16.7 |
| 2022-09 | 606 | 1 | 330 | 275 | 47 | 365 | 194 | 367 | 40 | 1413 | 31.1 |
| 2022-10 | 434 | 4 | 239 | 191 | 36 | 241 | 157 | 307 | 104 | 2151 | 31.2 |
| 2022-11 | 363 | 5 | 235 | 123 | 28 | 186 | 149 | 279 | 78 | 913 | 33.9 |
| 2022-12 | 373 | 6 | 161 | 206 | 36 | 122 | 215 | 288 | 6 | 958 | 28.2 |


Jumlah: **5541 run layak**, 3654 (65.9%) dengan `entry_sah = ya` (tiada amaran: syarat 10 hari menolak 34.1% < 50%). Dilangkau: 10378 (9178 "terlalu perlahan").


### Bucket %_naik × tempoh

| bucket_pct | <=21 | <=42 | <=63 |
|---|---|---|---|
| 10%+ | 1654 | 0 | 0 |
| 100%+ | 3 | 7 | 40 |
| 20%+ | 440 | 1032 | 0 |
| 200%+ | 0 | 1 | 0 |
| 30%+ | 261 | 586 | 983 |
| 300%+ | 0 | 0 | 1 |
| 50%+ | 36 | 139 | 358 |


### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)

| kumpulan | PANTAS | PERLAHAN | SEDANG |
|---|---|---|---|
| BIASA | 2094 | 0 | 1032 |
| PADU | 297 | 1341 | 725 |
| SUPER PADU | 3 | 41 | 8 |


Sel SAMPEL KECIL: [('SUPER PADU', 'PANTAS'), ('SUPER PADU', 'SEDANG')]


### Jenis kenaikan

| jenis | n |
|---|---|
| LONJAKAN | 2959 |
| STABIL | 2283 |
| BERTANGGA | 299 |


`graf_menaik = ya` (S3): 1227 (22.1%). `masih_naik = ya`: 481.


### 10 run terbaik setiap bulan (ikut %_naik_rendah)


**2022-01**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| HUDI | Basic Materials | 2022-01-11 | 2022-04-06 | 59 | 185.31 | SUPER PADU | STABIL | tidak | tidak |
| LGVN | Healthcare | 2022-01-24 | 2022-04-01 | 48 | 177.76 | SUPER PADU | LONJAKAN | tidak | tidak |
| EQT | Energy | 2022-01-27 | 2022-04-18 | 55 | 138.35 | SUPER PADU | BERTANGGA | ya | tidak |
| BEEM | Technology | 2022-01-21 | 2022-04-05 | 51 | 114.44 | SUPER PADU | STABIL | tidak | tidak |
| GLNG | Energy | 2022-01-24 | 2022-04-14 | 57 | 114.09 | SUPER PADU | BERTANGGA | ya | tidak |
| NKTX | Healthcare | 2022-01-27 | 2022-04-25 | 60 | 113.21 | SUPER PADU | LONJAKAN | tidak | tidak |
| MOS | Basic Materials | 2022-01-24 | 2022-04-18 | 58 | 111.22 | SUPER PADU | STABIL | ya | tidak |
| FULC | Healthcare | 2022-01-24 | 2022-04-04 | 49 | 110.53 | SUPER PADU | STABIL | tidak | tidak |
| CLF | Basic Materials | 2022-01-24 | 2022-03-28 | 44 | 109.17 | SUPER PADU | BERTANGGA | ya | tidak |
| AMC | Communication Services | 2022-01-24 | 2022-03-29 | 45 | 106.89 | SUPER PADU | LONJAKAN | tidak | tidak |


**2022-02**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| LNTH | Healthcare | 2022-02-14 | 2022-05-16 | 63 | 142.85 | SUPER PADU | STABIL | ya | ya |
| ACET | Healthcare | 2022-02-24 | 2022-04-01 | 26 | 79.86 | PADU | LONJAKAN | ya | tidak |
| EPAM | Technology | 2022-02-28 | 2022-05-06 | 48 | 75.03 | PADU | LONJAKAN | tidak | tidak |
| DINO | Energy | 2022-02-25 | 2022-05-25 | 62 | 71.07 | PADU | STABIL | ya | ya |
| MTUS | Basic Materials | 2022-02-24 | 2022-04-20 | 38 | 69.37 | PADU | LONJAKAN | ya | tidak |
| GDYN | Technology | 2022-02-24 | 2022-05-06 | 50 | 65.78 | PADU | LONJAKAN | tidak | tidak |
| LMND | Financial Services | 2022-02-24 | 2022-03-29 | 23 | 65.56 | PADU | LONJAKAN | tidak | tidak |
| CARG | Communication Services | 2022-02-24 | 2022-02-28 | 2 | 63.96 | PADU | LONJAKAN | ya | tidak |
| ANDE | Consumer Defensive | 2022-02-04 | 2022-04-14 | 48 | 61.87 | PADU | BERTANGGA | ya | tidak |
| RXT | Technology | 2022-02-23 | 2022-04-04 | 28 | 61.68 | PADU | STABIL | tidak | tidak |


**2022-03**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| FNGD | Lain-lain | 2022-03-29 | 2022-05-24 | 39 | 153.68 | SUPER PADU | STABIL | ya | tidak |
| GDS | Technology | 2022-03-14 | 2022-04-04 | 15 | 124.26 | SUPER PADU | LONJAKAN | ya | tidak |
| BZUN | Consumer Cyclical | 2022-03-14 | 2022-06-08 | 60 | 115.71 | SUPER PADU | LONJAKAN | tidak | tidak |
| BMBL | Communication Services | 2022-03-08 | 2022-06-07 | 63 | 114.54 | SUPER PADU | LONJAKAN | ya | ya |
| JOYY | Communication Services | 2022-03-15 | 2022-03-23 | 6 | 90.41 | PADU | LONJAKAN | ya | tidak |
| DQ | Technology | 2022-03-14 | 2022-06-07 | 59 | 84.31 | PADU | STABIL | ya | tidak |
| JKS | Technology | 2022-03-15 | 2022-06-06 | 57 | 83.79 | PADU | STABIL | ya | tidak |
| API | Technology | 2022-03-14 | 2022-03-23 | 7 | 79.66 | PADU | LONJAKAN | ya | tidak |
| LI | Consumer Cyclical | 2022-03-14 | 2022-06-08 | 60 | 71.69 | PADU | LONJAKAN | ya | tidak |
| NTRA | Healthcare | 2022-03-09 | 2022-04-04 | 18 | 70.65 | PADU | LONJAKAN | tidak | tidak |


**2022-04**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| TMDX | Healthcare | 2022-04-27 | 2022-07-28 | 63 | 91.15 | PADU | LONJAKAN | ya | ya |
| CVI | Energy | 2022-04-25 | 2022-06-07 | 30 | 85.7 | PADU | STABIL | ya | tidak |
| CMPS | Healthcare | 2022-04-29 | 2022-07-28 | 61 | 78.59 | PADU | STABIL | tidak | ya |
| IDYA | Healthcare | 2022-04-28 | 2022-07-27 | 61 | 76.07 | PADU | STABIL | ya | ya |
| CYRX | Industrials | 2022-04-28 | 2022-07-21 | 57 | 73.21 | PADU | STABIL | tidak | tidak |
| CRSP | Healthcare | 2022-04-28 | 2022-07-19 | 55 | 73.17 | PADU | STABIL | tidak | tidak |
| RCKT | Healthcare | 2022-04-28 | 2022-07-21 | 57 | 73.17 | PADU | STABIL | tidak | tidak |
| QURE | Healthcare | 2022-04-28 | 2022-07-29 | 63 | 71.4 | PADU | LONJAKAN | tidak | ya |
| SKYH | Real Estate | 2022-04-14 | 2022-04-26 | 7 | 69.01 | PADU | LONJAKAN | tidak | tidak |
| BXC | Industrials | 2022-04-07 | 2022-05-04 | 18 | 68.48 | PADU | LONJAKAN | ya | tidak |


**2022-05**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| KRUS | Consumer Cyclical | 2022-05-12 | 2022-08-12 | 63 | 171.83 | SUPER PADU | STABIL | tidak | ya |
| BE | Industrials | 2022-05-12 | 2022-08-12 | 63 | 165.56 | SUPER PADU | STABIL | ya | ya |
| AMC | Communication Services | 2022-05-11 | 2022-08-11 | 63 | 156.91 | SUPER PADU | STABIL | tidak | ya |
| AFRM | Financial Services | 2022-05-11 | 2022-08-11 | 63 | 155.14 | SUPER PADU | STABIL | tidak | ya |
| PLUG | Industrials | 2022-05-12 | 2022-08-12 | 63 | 132.6 | SUPER PADU | LONJAKAN | tidak | ya |
| VERU | Healthcare | 2022-05-10 | 2022-07-15 | 45 | 125.52 | SUPER PADU | LONJAKAN | ya | tidak |
| NRIX | Healthcare | 2022-05-09 | 2022-08-05 | 61 | 123.53 | SUPER PADU | STABIL | tidak | ya |
| IMCR | Healthcare | 2022-05-12 | 2022-08-05 | 58 | 117.51 | SUPER PADU | STABIL | tidak | tidak |
| KYMR | Healthcare | 2022-05-12 | 2022-08-10 | 61 | 116.33 | SUPER PADU | STABIL | tidak | ya |
| PRVA | Healthcare | 2022-05-10 | 2022-08-05 | 60 | 115.94 | SUPER PADU | BERTANGGA | ya | tidak |


**2022-06**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| VRDN | Healthcare | 2022-06-16 | 2022-08-16 | 41 | 159.15 | SUPER PADU | LONJAKAN | ya | tidak |
| LEU | Energy | 2022-06-30 | 2022-09-09 | 49 | 133.18 | SUPER PADU | BERTANGGA | ya | tidak |
| INSW | Energy | 2022-06-23 | 2022-09-19 | 60 | 88.69 | PADU | STABIL | tidak | tidak |
| ASPN | Basic Materials | 2022-06-29 | 2022-08-03 | 24 | 85.88 | PADU | STABIL | tidak | tidak |
| RUN | Technology | 2022-06-16 | 2022-09-12 | 59 | 85.82 | PADU | LONJAKAN | ya | tidak |
| GRBK | Consumer Cyclical | 2022-06-17 | 2022-08-16 | 40 | 82.38 | PADU | STABIL | ya | tidak |
| PCTY | Technology | 2022-06-16 | 2022-08-15 | 40 | 79.09 | PADU | STABIL | ya | tidak |
| TNK | Energy | 2022-06-17 | 2022-09-19 | 63 | 73.34 | PADU | STABIL | tidak | ya |
| FOUR | Technology | 2022-06-16 | 2022-08-16 | 41 | 71.64 | PADU | STABIL | tidak | tidak |
| SAH | Consumer Cyclical | 2022-06-16 | 2022-08-25 | 48 | 70.51 | PADU | STABIL | tidak | tidak |


**2022-07**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| FLNA | Healthcare | 2022-07-27 | 2022-09-22 | 40 | 268.93 | SUPER PADU | LONJAKAN | tidak | tidak |
| MNTK | Basic Materials | 2022-07-05 | 2022-09-14 | 50 | 123.3 | SUPER PADU | STABIL | tidak | tidak |
| SGML | Basic Materials | 2022-07-14 | 2022-10-04 | 57 | 118.55 | SUPER PADU | BERTANGGA | ya | tidak |
| VERU | Healthcare | 2022-07-29 | 2022-08-17 | 13 | 102.73 | SUPER PADU | LONJAKAN | ya | tidak |
| SMCI | Technology | 2022-07-05 | 2022-08-25 | 37 | 100.95 | SUPER PADU | STABIL | ya | tidak |
| CHPT | Consumer Cyclical | 2022-07-15 | 2022-09-15 | 43 | 75.48 | PADU | LONJAKAN | ya | tidak |
| ICHR | Technology | 2022-07-05 | 2022-08-16 | 30 | 74.24 | PADU | BERTANGGA | ya | tidak |
| KRNT | Industrials | 2022-07-06 | 2022-08-11 | 26 | 74.07 | PADU | LONJAKAN | tidak | tidak |
| ON | Technology | 2022-07-05 | 2022-08-25 | 37 | 71.38 | PADU | BERTANGGA | ya | tidak |
| PRCT | Healthcare | 2022-07-01 | 2022-09-09 | 48 | 67.24 | PADU | BERTANGGA | ya | tidak |


**2022-08**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| IDYA | Healthcare | 2022-08-15 | 2022-11-08 | 60 | 89.79 | PADU | STABIL | tidak | tidak |
| QTRX | Healthcare | 2022-08-09 | 2022-10-04 | 39 | 81.62 | PADU | LONJAKAN | tidak | tidak |
| ANF | Consumer Cyclical | 2022-08-31 | 2022-11-28 | 61 | 69.22 | PADU | LONJAKAN | tidak | ya |
| TPL | Energy | 2022-08-16 | 2022-11-07 | 58 | 68.83 | PADU | STABIL | ya | tidak |
| RUM | Communication Services | 2022-08-09 | 2022-09-19 | 28 | 67.93 | PADU | LONJAKAN | tidak | tidak |
| TASK | Technology | 2022-08-24 | 2022-11-14 | 57 | 67.13 | PADU | LONJAKAN | ya | tidak |
| ACET | Healthcare | 2022-08-30 | 2022-11-11 | 52 | 58.73 | PADU | STABIL | ya | tidak |
| CTRN | Consumer Cyclical | 2022-08-31 | 2022-11-30 | 63 | 57.97 | PADU | LONJAKAN | tidak | ya |
| ARCT | Healthcare | 2022-08-22 | 2022-11-04 | 53 | 50.64 | PADU | LONJAKAN | tidak | tidak |
| SIGI | Financial Services | 2022-08-04 | 2022-10-31 | 61 | 47.32 | PADU | STABIL | ya | ya |


**2022-09**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| BBW | Consumer Cyclical | 2022-09-06 | 2022-12-02 | 62 | 102.73 | SUPER PADU | BERTANGGA | tidak | ya |
| FUTU | Financial Services | 2022-09-29 | 2022-12-14 | 53 | 97.5 | PADU | STABIL | tidak | tidak |
| BURL | Consumer Cyclical | 2022-09-30 | 2022-12-29 | 62 | 93.32 | PADU | BERTANGGA | tidak | ya |
| RCKT | Healthcare | 2022-09-23 | 2022-12-14 | 57 | 93.21 | PADU | STABIL | ya | tidak |
| NBR | Energy | 2022-09-23 | 2022-11-15 | 37 | 92.61 | PADU | BERTANGGA | ya | tidak |
| FRPT | Consumer Defensive | 2022-09-08 | 2022-11-11 | 46 | 92.14 | PADU | BERTANGGA | ya | tidak |
| EDU | Consumer Defensive | 2022-09-23 | 2022-12-22 | 63 | 87.8 | PADU | LONJAKAN | ya | ya |
| REPL | Healthcare | 2022-09-22 | 2022-12-14 | 58 | 85.23 | PADU | LONJAKAN | ya | tidak |
| OM | Healthcare | 2022-09-23 | 2022-12-21 | 62 | 84.94 | PADU | STABIL | tidak | ya |
| CAR | Industrials | 2022-09-23 | 2022-10-28 | 25 | 84.59 | PADU | BERTANGGA | ya | tidak |


**2022-10**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| PCVX | Healthcare | 2022-10-21 | 2022-12-30 | 48 | 134.02 | SUPER PADU | LONJAKAN | ya | tidak |
| BABA | Consumer Cyclical | 2022-10-24 | 2023-01-25 | 63 | 107.29 | SUPER PADU | BERTANGGA | tidak | ya |
| VRDN | Healthcare | 2022-10-24 | 2023-01-17 | 57 | 103.14 | SUPER PADU | BERTANGGA | ya | tidak |
| AXSM | Healthcare | 2022-10-12 | 2022-12-14 | 44 | 101.62 | SUPER PADU | LONJAKAN | tidak | tidak |
| GDS | Technology | 2022-10-11 | 2023-01-04 | 58 | 97.46 | PADU | STABIL | tidak | tidak |
| NVCR | Healthcare | 2022-10-24 | 2023-01-05 | 50 | 91.94 | PADU | LONJAKAN | ya | tidak |
| BIDU | Communication Services | 2022-10-24 | 2023-01-13 | 56 | 88.88 | PADU | BERTANGGA | tidak | tidak |
| BEKE | Real Estate | 2022-10-19 | 2023-01-13 | 59 | 88.31 | PADU | STABIL | tidak | tidak |
| ZTO | Industrials | 2022-10-24 | 2023-01-25 | 63 | 77.7 | PADU | STABIL | tidak | ya |
| ALT | Healthcare | 2022-10-12 | 2023-01-12 | 63 | 76.6 | PADU | LONJAKAN | ya | ya |


**2022-11**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| MDGL | Healthcare | 2022-11-09 | 2023-01-20 | 48 | 398.13 | SUPER PADU | LONJAKAN | ya | tidak |
| LUNG | Healthcare | 2022-11-04 | 2023-02-01 | 59 | 131.45 | SUPER PADU | STABIL | tidak | tidak |
| META | Communication Services | 2022-11-04 | 2023-02-07 | 63 | 117.53 | SUPER PADU | BERTANGGA | ya | ya |
| CVNA | Consumer Cyclical | 2022-11-07 | 2023-02-03 | 60 | 116.32 | SUPER PADU | LONJAKAN | tidak | tidak |
| AEHR | Technology | 2022-11-03 | 2023-02-02 | 61 | 108.35 | SUPER PADU | LONJAKAN | ya | ya |
| RPD | Technology | 2022-11-07 | 2023-02-01 | 58 | 97.55 | PADU | LONJAKAN | tidak | tidak |
| CROX | Consumer Cyclical | 2022-11-02 | 2023-01-17 | 50 | 92.27 | PADU | STABIL | ya | tidak |
| KYNB | Healthcare | 2022-11-08 | 2023-02-07 | 61 | 90.47 | PADU | BERTANGGA | ya | ya |
| DLO | Technology | 2022-11-17 | 2023-02-02 | 51 | 89.75 | PADU | STABIL | tidak | tidak |
| MSTR | Technology | 2022-11-11 | 2023-02-02 | 55 | 88.11 | PADU | STABIL | tidak | tidak |


**2022-12**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| AI | Technology | 2022-12-28 | 2023-03-03 | 44 | 180.31 | SUPER PADU | LONJAKAN | ya | tidak |
| TREE | Financial Services | 2022-12-27 | 2023-02-07 | 28 | 161.65 | SUPER PADU | BERTANGGA | ya | tidak |
| NRDS | Communication Services | 2022-12-19 | 2023-03-02 | 49 | 138.72 | SUPER PADU | STABIL | tidak | tidak |
| W | Consumer Cyclical | 2022-12-28 | 2023-02-02 | 24 | 137.14 | SUPER PADU | BERTANGGA | ya | tidak |
| PTON | Consumer Cyclical | 2022-12-30 | 2023-02-02 | 22 | 121.09 | SUPER PADU | STABIL | ya | tidak |
| PLRX | Healthcare | 2022-12-06 | 2023-01-26 | 34 | 120.83 | SUPER PADU | LONJAKAN | ya | tidak |
| TSLA | Consumer Cyclical | 2022-12-28 | 2023-02-15 | 33 | 97.93 | PADU | STABIL | tidak | tidak |
| SMG | Basic Materials | 2022-12-29 | 2023-02-16 | 33 | 87.95 | PADU | BERTANGGA | ya | tidak |
| RELY | Technology | 2022-12-19 | 2023-03-21 | 62 | 87.7 | PADU | STABIL | ya | ya |
| ROKU | Communication Services | 2022-12-28 | 2023-02-17 | 35 | 87.04 | PADU | STABIL | ya | tidak |


### Semua run SUPER PADU (≥ 100%)

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|
| MDGL | Healthcare | 2022-11-09 | 48 | 398.13 | LONJAKAN | ya | tidak |
| FLNA | Healthcare | 2022-07-27 | 40 | 268.93 | LONJAKAN | tidak | tidak |
| HUDI | Basic Materials | 2022-01-11 | 59 | 185.31 | STABIL | tidak | tidak |
| AI | Technology | 2022-12-28 | 44 | 180.31 | LONJAKAN | ya | tidak |
| LGVN | Healthcare | 2022-01-24 | 48 | 177.76 | LONJAKAN | tidak | tidak |
| KRUS | Consumer Cyclical | 2022-05-12 | 63 | 171.83 | STABIL | tidak | ya |
| BE | Industrials | 2022-05-12 | 63 | 165.56 | STABIL | ya | ya |
| TREE | Financial Services | 2022-12-27 | 28 | 161.65 | BERTANGGA | ya | tidak |
| VRDN | Healthcare | 2022-06-16 | 41 | 159.15 | LONJAKAN | ya | tidak |
| AMC | Communication Services | 2022-05-11 | 63 | 156.91 | STABIL | tidak | ya |
| AFRM | Financial Services | 2022-05-11 | 63 | 155.14 | STABIL | tidak | ya |
| FNGD | Lain-lain | 2022-03-29 | 39 | 153.68 | STABIL | ya | tidak |
| LNTH | Healthcare | 2022-02-14 | 63 | 142.85 | STABIL | ya | ya |
| NRDS | Communication Services | 2022-12-19 | 49 | 138.72 | STABIL | tidak | tidak |
| EQT | Energy | 2022-01-27 | 55 | 138.35 | BERTANGGA | ya | tidak |
| W | Consumer Cyclical | 2022-12-28 | 24 | 137.14 | BERTANGGA | ya | tidak |
| PCVX | Healthcare | 2022-10-21 | 48 | 134.02 | LONJAKAN | ya | tidak |
| LEU | Energy | 2022-06-30 | 49 | 133.18 | BERTANGGA | ya | tidak |
| PLUG | Industrials | 2022-05-12 | 63 | 132.6 | LONJAKAN | tidak | ya |
| LUNG | Healthcare | 2022-11-04 | 59 | 131.45 | STABIL | tidak | tidak |
| VERU | Healthcare | 2022-05-10 | 45 | 125.52 | LONJAKAN | ya | tidak |
| GDS | Technology | 2022-03-14 | 15 | 124.26 | LONJAKAN | ya | tidak |
| NRIX | Healthcare | 2022-05-09 | 61 | 123.53 | STABIL | tidak | ya |
| MNTK | Basic Materials | 2022-07-05 | 50 | 123.3 | STABIL | tidak | tidak |
| PTON | Consumer Cyclical | 2022-12-30 | 22 | 121.09 | STABIL | ya | tidak |
| PLRX | Healthcare | 2022-12-06 | 34 | 120.83 | LONJAKAN | ya | tidak |
| SGML | Basic Materials | 2022-07-14 | 57 | 118.55 | BERTANGGA | ya | tidak |
| META | Communication Services | 2022-11-04 | 63 | 117.53 | BERTANGGA | ya | ya |
| IMCR | Healthcare | 2022-05-12 | 58 | 117.51 | STABIL | tidak | tidak |
| KYMR | Healthcare | 2022-05-12 | 61 | 116.33 | STABIL | tidak | ya |
| CVNA | Consumer Cyclical | 2022-11-07 | 60 | 116.32 | LONJAKAN | tidak | tidak |
| PRVA | Healthcare | 2022-05-10 | 60 | 115.94 | BERTANGGA | ya | tidak |
| BZUN | Consumer Cyclical | 2022-03-14 | 60 | 115.71 | LONJAKAN | tidak | tidak |
| BMBL | Communication Services | 2022-03-08 | 63 | 114.54 | LONJAKAN | ya | ya |
| BEEM | Technology | 2022-01-21 | 51 | 114.44 | STABIL | tidak | tidak |
| GLNG | Energy | 2022-01-24 | 57 | 114.09 | BERTANGGA | ya | tidak |
| NKTX | Healthcare | 2022-01-27 | 60 | 113.21 | LONJAKAN | tidak | tidak |
| MOS | Basic Materials | 2022-01-24 | 58 | 111.22 | STABIL | ya | tidak |
| FULC | Healthcare | 2022-01-24 | 49 | 110.53 | STABIL | tidak | tidak |
| CLF | Basic Materials | 2022-01-24 | 44 | 109.17 | BERTANGGA | ya | tidak |
| AEHR | Technology | 2022-11-03 | 61 | 108.35 | LONJAKAN | ya | ya |
| BABA | Consumer Cyclical | 2022-10-24 | 63 | 107.29 | BERTANGGA | tidak | ya |
| MARA | Financial Services | 2022-05-12 | 63 | 107.27 | LONJAKAN | tidak | ya |
| AMC | Communication Services | 2022-01-24 | 45 | 106.89 | LONJAKAN | tidak | tidak |
| UPST | Financial Services | 2022-05-11 | 15 | 103.34 | LONJAKAN | tidak | tidak |
| VRDN | Healthcare | 2022-10-24 | 57 | 103.14 | BERTANGGA | ya | tidak |
| VERU | Healthcare | 2022-07-29 | 13 | 102.73 | LONJAKAN | ya | tidak |
| BBW | Consumer Cyclical | 2022-09-06 | 62 | 102.73 | BERTANGGA | tidak | ya |
| NTRA | Healthcare | 2022-05-12 | 61 | 102.16 | STABIL | ya | ya |
| AXSM | Healthcare | 2022-10-12 | 44 | 101.62 | LONJAKAN | tidak | tidak |
| SMCI | Technology | 2022-07-05 | 37 | 100.95 | STABIL | ya | tidak |
| LMND | Financial Services | 2022-05-12 | 63 | 100.25 | STABIL | ya | ya |


(dipaparkan 60 teratas daripada 52)


### Run BERTANGGA (S2) — 40 teratas

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | bilangan_kaki | pct_hari_atas_ema21 | kumpulan |
|---|---|---|---|---|---|---|---|
| TREE | Financial Services | 2022-12-27 | 28 | 161.65 | 2 | 100.0 | SUPER PADU |
| EQT | Energy | 2022-01-27 | 55 | 138.35 | 2 | 88.7 | SUPER PADU |
| W | Consumer Cyclical | 2022-12-28 | 24 | 137.14 | 3 | 100.0 | SUPER PADU |
| LEU | Energy | 2022-06-30 | 49 | 133.18 | 4 | 91.7 | SUPER PADU |
| SGML | Basic Materials | 2022-07-14 | 57 | 118.55 | 4 | 90.7 | SUPER PADU |
| META | Communication Services | 2022-11-04 | 63 | 117.53 | 2 | 83.3 | SUPER PADU |
| PRVA | Healthcare | 2022-05-10 | 60 | 115.94 | 3 | 91.4 | SUPER PADU |
| GLNG | Energy | 2022-01-24 | 57 | 114.09 | 3 | 100.0 | SUPER PADU |
| CLF | Basic Materials | 2022-01-24 | 44 | 109.17 | 4 | 82.9 | SUPER PADU |
| BABA | Consumer Cyclical | 2022-10-24 | 63 | 107.29 | 4 | 78.1 | SUPER PADU |
| VRDN | Healthcare | 2022-10-24 | 57 | 103.14 | 3 | 83.3 | SUPER PADU |
| BBW | Consumer Cyclical | 2022-09-06 | 62 | 102.73 | 2 | 63.5 | SUPER PADU |
| BURL | Consumer Cyclical | 2022-09-30 | 62 | 93.32 | 3 | 74.6 | PADU |
| NBR | Energy | 2022-09-23 | 37 | 92.61 | 2 | 93.5 | PADU |
| FRPT | Consumer Defensive | 2022-09-08 | 46 | 92.14 | 3 | 100.0 | PADU |
| KYNB | Healthcare | 2022-11-08 | 61 | 90.47 | 3 | 66.7 | PADU |
| ASTH | Healthcare | 2022-05-11 | 57 | 90.01 | 3 | 65.5 | PADU |
| BIDU | Communication Services | 2022-10-24 | 56 | 88.88 | 4 | 73.7 | PADU |
| ACRS | Healthcare | 2022-01-19 | 46 | 88.43 | 3 | 92.1 | PADU |
| SMG | Basic Materials | 2022-12-29 | 33 | 87.95 | 3 | 100.0 | PADU |
| VET | Energy | 2022-01-05 | 42 | 87.86 | 2 | 100.0 | PADU |
| CAR | Industrials | 2022-09-23 | 25 | 84.59 | 2 | 87.0 | PADU |
| FOUR | Technology | 2022-11-07 | 62 | 84.15 | 3 | 88.3 | PADU |
| VRNS | Technology | 2022-11-07 | 63 | 82.96 | 4 | 68.8 | PADU |
| ASO | Consumer Cyclical | 2022-05-24 | 57 | 81.9 | 4 | 80.0 | PADU |
| SMCI | Technology | 2022-09-23 | 44 | 81.81 | 3 | 78.9 | PADU |
| RDNT | Healthcare | 2022-11-09 | 57 | 80.05 | 2 | 79.6 | PADU |
| SNDX | Healthcare | 2022-05-12 | 59 | 79.59 | 3 | 94.0 | PADU |
| PBF | Energy | 2022-09-19 | 41 | 79.42 | 3 | 94.9 | PADU |
| AA | Basic Materials | 2022-01-24 | 42 | 78.68 | 3 | 83.3 | PADU |
| ATKR | Industrials | 2022-09-27 | 54 | 77.84 | 3 | 98.0 | PADU |
| AGNT | Real Estate | 2022-12-27 | 25 | 77.81 | 2 | 90.5 | PADU |
| DFIN | Technology | 2022-05-09 | 61 | 77.2 | 2 | 74.1 | PADU |
| WNC | Industrials | 2022-09-16 | 54 | 75.27 | 2 | 87.2 | PADU |
| PDS | Energy | 2022-09-26 | 34 | 74.99 | 2 | 85.7 | PADU |
| CLB | Energy | 2022-09-26 | 36 | 74.61 | 3 | 96.8 | PADU |
| ICHR | Technology | 2022-07-05 | 30 | 74.24 | 2 | 96.2 | PADU |
| TH | Industrials | 2022-11-07 | 46 | 73.08 | 2 | 91.1 | PADU |
| ATEC | Healthcare | 2022-12-06 | 59 | 72.63 | 2 | 100.0 | PADU |
| PBT | Lain-lain | 2022-09-26 | 63 | 71.69 | 2 | 88.1 | PADU |


(daripada 299 run BERTANGGA)


### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)

n peristiwa PADU dalam S2, populasi keputusan (a) = **171** (rujukan: semua peristiwa = 712). < 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat.


Peristiwa sah: **15440** (populasi keputusan 5273).


## 3. Step 2b — kohort "naik dan naik"

Dijejak 297 run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari tarikh_sah.


| Metrik | Nilai |
|---|---|
| % akhirnya melebihi +100% | **18.2%** |
| median %_naik_penuh | **62.7%** |
| median %_naik pada hari ke-63 | 40.0% |
| median hari ke puncak penuh | 153 |
| median MFE 252 selepas kos | 44.9% |
| median MAE 252 | -9.6% |
| median hari pegang Chandelier 4×ATR | 81 |
| median pulangan Chandelier selepas kos | 11.0% |
| terpotong hujung data | 0.0% |


Exit yang menyala dahulu:


| exit | n |
|---|---|
| bawah_ma50 | 127 |
| bawah_ema9 | 85 |
| bawah_ema21 | 57 |
| hist_neg3 | 10 |
| hari_agihan | 8 |
| rsi_70_60 | 7 |
| macd_bawah | 2 |
| trail_8pct | 1 |


### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari

| kohort | n | median_naik_63 | pct_bertangga | pct_super | median_hari_ke_puncak |
|---|---|---|---|---|---|
| masih_naik = ya | 297 | 40.0 | 20.5 | 2.4 | 63.0 |
| reda dalam 63 hari | 3357 | 24.9 | 6.4 | 0.6 | 23.0 |


Kohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya diketahui pada hari ke-63.


## 4. Step 3 — populasi kuintil dan dedup

POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **7974** baris. Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **33** daripada 41; dibuang 8.


| buang | kerana | rho |
|---|---|---|
| j_ma150 | j_ma200 | 0.957 |
| cerun_ma200 | j_ma200 | 0.819 |
| rsi14 | j_ma50 | 0.819 |
| roc60 | cerun_ma50 | 0.928 |
| willr14 | stoch_k | 1.0 |
| julat10 | atr_pct | 0.847 |
| bb_pctb | cci20 | 0.913 |
| kelt_pos | j_ema21 | 0.925 |


Signal dibina: **217** (31 binari + 66 hujung kuintil + 120 pemicu × 1 konteks).


## 5. Step 4 — common & unique (ENTRY)

Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. N ujian ENTRY sebenar (populasi a, kumpulan A) = **868** baris (213 signal × 2 subset × 2 keluarga).


### Kelas (S2, kumpulan A, keluarga PADU)

| kelas | n |
|---|---|
| TIDAK BERGUNA | 193 |
| UNIQUE | 11 |
| COMMON BIASA | 5 |
| SEDERHANA | 5 |
| LANGKA | 3 |


### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)

| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n | n_industri | n_minggu | purata_pct_naik_rendah | purata_hari_ke_puncak | pct_bertangga | pct_lonjakan | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | UNIQUE | 19.28 | 0.0 | 1.11 | 1.34 | 17.427 | 14.366 | 54.55 | 9.209 | 33 | 23 | 20 | 64.2 | 44.1 | 100.0 | 0.0 |  |
| q5:atr_pct | UNIQUE | 37.35 | 0.0 | 2.88 | 21.63 | 12.986 | 1.727 | 45.83 | 7.738 | 72 | 35 | 30 | 62.51 | 44.6 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:julat20 | UNIQUE | 20.48 | 0.0 | 1.99 | 1.21 | 10.286 | 16.987 | 41.3 | 6.974 | 46 | 32 | 23 | 64.55 | 43.4 | 100.0 | 0.0 |  |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 15.66 | 0.0 | 1.47 | 1.23 | 10.619 | 12.784 | 41.18 | 6.952 | 34 | 25 | 23 | 54.54 | 41.9 | 100.0 | 0.0 |  |
| pocket_pivot&q1:j_52w_tinggi | LANGKA | 13.25 | 0.0 | 1.33 | 1.23 | 9.984 | 10.817 | 40.0 | 6.753 | 30 | 19 | 19 | 53.59 | 41.4 | 100.0 | 0.0 |  |
| q5:julat20 | UNIQUE | 45.78 | 10.0 | 4.72 | 28.74 | 4.578 | 1.593 | 38.1 | 6.432 | 105 | 53 | 32 | 58.14 | 44.9 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:bb_lebar | UNIQUE | 19.28 | 0.0 | 2.29 | 0.99 | 8.432 | 19.436 | 36.73 | 6.202 | 49 | 33 | 22 | 61.81 | 42.7 | 100.0 | 0.0 |  |
| rsi_lintas50&q1:j_ma200 | UNIQUE | 18.07 | 0.0 | 2.21 | 1.24 | 8.169 | 14.52 | 33.33 | 5.628 | 45 | 32 | 22 | 48.93 | 42.9 | 100.0 | 0.0 |  |
| q5:bb_lebar | UNIQUE | 43.37 | 10.0 | 5.9 | 27.58 | 4.337 | 1.573 | 31.93 | 5.391 | 119 | 58 | 31 | 56.28 | 44.8 | 100.0 | 0.0 |  |
| pocket_pivot&q1:j_ma200 | LANGKA | 13.25 | 0.0 | 2.14 | 0.86 | 6.197 | 15.488 | 27.5 | 4.643 | 40 | 26 | 19 | 49.24 | 43.0 | 100.0 | 0.0 |  |
| q1:j_52w_tinggi | UNIQUE | 31.33 | 10.0 | 5.38 | 22.01 | 3.133 | 1.423 | 26.73 | 4.513 | 101 | 39 | 36 | 52.76 | 42.1 | 100.0 | 0.0 |  |
| pocket_pivot&q5:bb_lebar | LANGKA | 8.43 | 0.0 | 1.62 | 2.04 | 5.198 | 4.13 | 26.67 | 4.502 | 30 | 27 | 14 | 60.99 | 44.8 | 100.0 | 0.0 |  |
| q5:j_ema9 | UNIQUE | 37.35 | 0.0 | 6.49 | 7.45 | 5.755 | 5.014 | 26.67 | 4.502 | 120 | 61 | 37 | 54.82 | 46.1 | 100.0 | 0.0 |  |
| q1:j_ma200 | UNIQUE | 40.96 | 10.0 | 8.41 | 24.97 | 4.096 | 1.64 | 22.82 | 3.853 | 149 | 54 | 37 | 47.59 | 45.9 | 100.0 | 0.0 |  |


### Rujukan S1 (semua run layak)

| signal | kelas | K_padu | lift | presisi | lift_presisi | n | tanda |
|---|---|---|---|---|---|---|---|
| gap_and_go&q5:julat20 | LANGKA | 4.51 | 17.582 | 90.32 | 4.177 | 31 | LONJAKAN BERITA |
| gap_and_go&q5:bb_lebar | LANGKA | 4.69 | 7.303 | 80.56 | 3.726 | 36 | LONJAKAN BERITA |
| q5:julat20 | TERAS | 53.3 | 2.185 | 55.44 | 2.564 | 570 | LONJAKAN BERITA |
| q5:j_ema9 | TERAS | 51.04 | 2.173 | 52.71 | 2.437 | 573 | LONJAKAN BERITA |


### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja

S3 mengandungi 1076 run; ia **bukan keluarga carian** (tidak menambah N). 12.1% daripadanya BERTANGGA lawan 7.5% keseluruhan.


### Keluarga SUPER PADU (FDR sendiri)

| signal | kelas | K_super | lift | lift_rawak | n | tanda |
|---|---|---|---|---|---|---|
| ema_crossback&q5:atr_pct | UNIQUE | 33.33 | 75.333 | 77.909 | 15 | SAMPEL KECIL |
| rsi_lintas50&q5:atr_pct | TERAS | 66.67 | 60.267 | 49.681 | 33 |  |
| pocket_pivot&q5:atr_pct | UNIQUE | 33.33 | 50.222 | 27.645 | 17 | SAMPEL KECIL |
| rsi_lintas50&q5:julat20 | TERAS | 66.67 | 33.481 | 55.29 | 46 |  |
| pocket_pivot&q5:julat20 | UNIQUE | 33.33 | 32.286 | 18.042 | 23 |  |
| rsi_lintas50&q5:bb_lebar | TERAS | 66.67 | 29.161 | 67.216 | 49 |  |
| pocket_pivot&q1:j_52w_tinggi | UNIQUE | 33.33 | 25.111 | 27.206 | 30 |  |
| q5:atr_pct | TERAS | 66.67 | 23.179 | 3.083 | 72 |  |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 33.33 | 22.6 | 27.206 | 34 |  |
| pocket_pivot&q5:bb_lebar | UNIQUE | 33.33 | 20.545 | 16.324 | 30 |  |
| ema_crossback&q5:sektor_1b | UNIQUE | 33.33 | 15.586 | 68.56 | 34 |  |
| ema_crossback&q1:vol_n50 | UNIQUE | 33.33 | 10.512 | 57.133 | 44 |  |
| q5:bb_lebar | TERAS | 66.67 | 6.667 | 2.417 | 119 |  |
| rsi_lintas50&q5:sektor_1b | TERAS | 66.67 | 6.667 | 51.164 | 82 |  |
| q5:julat20 | TERAS | 66.67 | 6.667 | 2.319 | 105 |  |
| rsi_lintas50&q5:rs_spy_6b | TERAS | 66.67 | 6.667 | 60.14 | 141 |  |
| q5:j_ema9 | UNIQUE | 33.33 | 5.136 | 4.475 | 120 |  |
| ema_crossback&q5:rs_spy_6b | UNIQUE | 33.33 | 5.022 | 45.105 | 103 |  |
| b:qqq_ma200 | UNIQUE | 33.33 | 4.86 | 4.722 | 100 |  |
| rsi_lintas50&q5:cerun_ma50 | UNIQUE | 33.33 | 4.66 | 22.853 | 110 |  |


### PEMICU YANG TIDAK MEMBEZAKAN

Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.


| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n |
|---|---|---|---|---|---|---|---|---|---|---|
| b:donchian20 | TIDAK BERGUNA | 0.0 | 0.0 | 4.87 | 5.56 | 0.0 | 0.0 | 0.0 | 0.0 | 66 |
| b:ema_crossback | TIDAK BERGUNA | 20.48 | 0.0 | 20.65 | 2.28 | 0.992 | 9.002 | 6.04 | 1.02 | 298 |
| b:gap_and_go | TIDAK BERGUNA | 3.61 | 0.0 | 0.96 | 0.23 | 3.77 | 15.488 | 18.75 | 3.166 | 16 |
| b:macd_cross | TIDAK BERGUNA | 27.71 | 30.0 | 20.28 | 3.81 | 0.924 | 7.27 | 7.64 | 1.29 | 301 |
| b:pocket_pivot | TIDAK BERGUNA | 26.51 | 20.0 | 20.21 | 7.51 | 1.312 | 3.531 | 7.69 | 1.299 | 299 |
| b:rsi_lintas50 | COMMON BIASA | 51.81 | 60.0 | 47.2 | 5.85 | 0.863 | 8.85 | 6.65 | 1.122 | 692 |


**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis yang diuji dalam kajian ini, dan ia disokong oleh data 2025.


### Corong ke Step 7
21 signal diteruskan (had 30; layak sebelum had: 21).


## 6. Step 5 — HOLD

> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana berjaya. Semua CALON.


### Kelas pullback

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| AMARAN | 6502 | 54.0 | -16.43 | 9.6 |
| PULLBACK PASARAN | 417 | 88.7 | -8.01 | 7.4 |
| PULLBACK SIHAT | 223 | 65.0 | -7.96 | 5.6 |


Pullback yang trend sahamnya utuh (SIHAT 65.0%, PASARAN 88.7%) menyambung ke puncak baru jauh lebih kerap daripada pullback AMARAN (54.0%). Ini sokongan paling jelas bagi falsafah "pegang selagi naik".


### Grid 18 peraturan HOLD (deskriptif)

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| X=5%,Y=ema9 | 3 | 100.0 | -5.0 | 5.7 |
| X=5%,Y=ema21 | 1629 | 92.2 | -6.98 | 5.2 |
| X=5%,Y=ma50 | 1996 | 88.3 | -8.0 | 6.7 |
| X=7%,Y=ema9 | 1420 | 93.6 | -5.89 | 4.8 |
| X=7%,Y=ema21 | 2012 | 92.7 | -6.81 | 5.2 |
| X=7%,Y=ma50 | 2434 | 90.1 | -7.63 | 6.2 |
| X=10%,Y=ema9 | 2581 | 92.0 | -6.98 | 5.8 |
| X=10%,Y=ema21 | 2715 | 92.0 | -7.24 | 5.9 |
| X=10%,Y=ma50 | 2949 | 90.5 | -7.78 | 6.3 |
| X=12%,Y=ema9 | 3157 | 89.9 | -7.71 | 6.6 |
| X=12%,Y=ema21 | 3205 | 89.8 | -7.82 | 6.6 |
| X=12%,Y=ma50 | 3335 | 89.1 | -8.16 | 6.8 |
| X=15%,Y=ema9 | 3793 | 86.4 | -8.67 | 7.5 |
| X=15%,Y=ema21 | 3809 | 86.4 | -8.72 | 7.5 |
| X=15%,Y=ma50 | 3868 | 86.1 | -8.9 | 7.6 |
| X=20%,Y=ema9 | 4722 | 78.8 | -10.39 | 8.5 |
| X=20%,Y=ema21 | 4726 | 78.8 | -10.41 | 8.5 |
| X=20%,Y=ma50 | 4749 | 78.5 | -10.48 | 8.6 |


### Common/unique HOLD (lulus FDR)

13 / 18 signal HOLD lulus BH-FDR q ≤ 0.01: `b:macd_atas0`, `b:bb_squeeze`, `b:atas_awan`, `b:tenkan_atas`, `b:inside_day`, `b:nr7`, `b:vcp`, `b:sektor_atas_ma50`, `b:spy_ma50`, `b:spy_ma200`, `b:qqq_ma50`, `b:supertrend_naik`, `b:psar_naik`


| nama | subset | n | K_padu | K_gagal | lift | presisi | lift_presisi | kelas |
|---|---|---|---|---|---|---|---|---|
| b:macd_cross | S1 | 6 | 0.15 | 0.0 | 10.649 | 100.0 | 1.775 | TIDAK BERGUNA |
| b:psar_naik | S1 | 1309 | 30.59 | 2.5 | 12.229 | 94.04 | 1.669 | UNIQUE |
| b:atas_ema21 | S1 | 860 | 19.96 | 1.83 | 10.916 | 93.37 | 1.657 | UNIQUE |
| b:garis_rs_tinggi | S1 | 13 | 0.3 | 0.03 | 9.298 | 92.31 | 1.638 | TIDAK BERGUNA |
| b:supertrend_naik | S1 | 2237 | 51.12 | 5.77 | 8.855 | 91.95 | 1.632 | TERAS |
| b:vcp | S1 | 168 | 3.78 | 0.51 | 7.361 | 90.48 | 1.606 | LANGKA |
| b:atas_ma50 | S1 | 1624 | 35.86 | 5.81 | 6.177 | 88.85 | 1.577 | UNIQUE |
| b:tenkan_atas | S1 | 2356 | 51.81 | 8.69 | 5.961 | 88.5 | 1.571 | TERAS |
| b:macd_atas0 | S1 | 2255 | 48.61 | 9.59 | 5.069 | 86.74 | 1.54 | UNIQUE |
| b:atas_awan | S1 | 1602 | 34.02 | 7.47 | 4.553 | 85.46 | 1.517 | UNIQUE |
| b:pullback_dalam_7pct | S1 | 3202 | 66.97 | 16.26 | 4.119 | 84.17 | 1.494 | TERAS |
| b:bb_squeeze | S1 | 60 | 1.22 | 0.35 | 3.452 | 81.67 | 1.449 | TIDAK BERGUNA |
| b:garis_rs_tinggi | S2 | 4 | 0.53 | 0.0 | 5.31 | 100.0 | 1.328 | TIDAK BERGUNA |
| b:psar_naik | S2 | 262 | 33.96 | 3.27 | 10.399 | 96.95 | 1.287 | UNIQUE |
| b:atas_ema21 | S2 | 224 | 29.01 | 2.86 | 10.154 | 96.88 | 1.286 | UNIQUE |
| b:sektor_atas_ma50 | S1 | 1983 | 35.59 | 17.67 | 2.014 | 72.21 | 1.282 | SEDERHANA |
| b:sektor_naik | S1 | 1983 | 35.59 | 17.67 | 2.014 | 72.21 | 1.282 | SEDERHANA |
| b:supertrend_naik | S2 | 566 | 72.33 | 10.2 | 7.088 | 95.58 | 1.269 | TERAS |
| b:tenkan_atas | S2 | 562 | 71.39 | 11.43 | 6.247 | 95.02 | 1.261 | TERAS |
| b:atas_ma50 | S2 | 438 | 55.48 | 9.39 | 5.91 | 94.75 | 1.258 | TERAS |


## 7. Step 6 — EXIT (semua CALON)

> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.


| nama | n | pct_menyala | median_hari_dari_puncak | median_pulangan_exit | median_pct_kekal | kadar_exit_palsu |
|---|---|---|---|---|---|---|
| atr_lonjak_15x | 582 | 16.7 | 19.5 | -11.77 | -105.3 | 50.5 |
| bawah_ema21 | 3486 | 100.0 | -11.0 | -1.44 | -8.6 | 58.5 |
| bawah_ema9 | 3487 | 100.0 | -14.0 | -1.37 | -7.3 | 60.5 |
| bawah_ma50 | 3481 | 99.8 | -14.0 | -0.74 | -4.7 | 59.8 |
| chandelier_4atr | 3043 | 87.3 | 14.0 | -4.14 | -30.8 | 44.0 |
| climax_25_15h | 926 | 26.6 | -7.0 | 12.79 | 59.9 | 51.8 |
| div_macd | 3112 | 89.2 | -12.0 | 4.0 | 30.2 | 50.5 |
| div_rsi | 2587 | 74.2 | -9.0 | 6.32 | 45.3 | 47.2 |
| gap_besar | 285 | 8.2 | -2.0 | 21.62 | 77.0 | 54.7 |
| hari_agihan | 2586 | 74.2 | 10.0 | -0.89 | -1.8 | 45.7 |
| hist_neg3 | 3449 | 98.9 | 4.0 | -0.28 | 0.4 | 49.6 |
| jauh_ma50_2x | 1545 | 44.3 | -10.0 | 8.79 | 61.0 | 41.2 |
| macd_bawah | 3480 | 99.8 | 2.0 | -0.39 | 2.2 | 48.9 |
| pullback_amaran | 3484 | 99.9 | -1.0 | -7.6 | -51.2 | 74.3 |
| rsi_70_60 | 1819 | 52.2 | 2.0 | 10.55 | 58.5 | 41.3 |
| trail_10pct | 3359 | 96.3 | 7.0 | -3.76 | -23.4 | 49.3 |
| trail_15pct | 2882 | 82.6 | 15.0 | -8.36 | -58.9 | 51.1 |
| trail_2atr | 3486 | 100.0 | 3.0 | -1.32 | -7.5 | 48.7 |
| trail_3atr | 3426 | 98.3 | 8.0 | -2.44 | -16.4 | 45.1 |
| trail_8pct | 3442 | 98.7 | 4.0 | -2.34 | -15.1 | 48.6 |


`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala 11–14 hari sebelum puncak dan mengekalkan hanya -5% hingga -9% keuntungan. Kadar exit palsu 41%–74%.


**Keluarga EXIT: 0 / 66 signal lulus BH-FDR q ≤ 0.01.** Tiada signal EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas kawalan pelbagai ujian.


## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)

Setiap signal corong diimbas atas **semua** hari universe 2022 (584,786 baris (ticker, hari); 502,000 selepas topeng universe). Kadar asas KAWALAN RAWAK (MFE63 ≥ 30%) = 11.61%.


| signal | n_kemunculan | kadar_tepat_mfe30 | lift_tepat | kadar_palsu_bawah10 | kadar_tepat_bertangga | ketulenan_trend_median | mfe63_p50 | mfe63_p75 | mfe63_p90 | pct_mfe63_ge30 | pct_mfe63_ge100 | mfe252_p90 | pct_mfe252_ge100 | median_hari_mfe63 | jangkaan_henti2atr | kadar_menang | kapasiti | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | 5769 | 25.0 | 2.153 | 37.79 | 1.79 | 75.0 | 15.49 | 30.0 | 47.72 | 25.0 | 0.88 | 87.7 | 7.56 | 23.0 | -6.716 | 22.36 | PELENGKAP |  |
| q5:atr_pct | 109463 | 27.92 | 2.405 | 34.17 | 2.26 | 57.1 | 16.93 | 32.28 | 51.38 | 27.92 | 1.13 | 92.79 | 8.53 | 25.0 | -5.128 | 26.61 | PELENGKAP |  |
| rsi_lintas50&q5:julat20 | 5155 | 23.92 | 2.06 | 39.65 | 1.78 | 75.0 | 14.23 | 29.2 | 47.34 | 23.92 | 0.89 | 85.19 | 7.37 | 24.0 | -6.387 | 22.31 | PELENGKAP |  |
| rsi_lintas50&q1:j_52w_tinggi | 5614 | 24.72 | 2.13 | 37.19 | 1.53 | 75.0 | 15.71 | 29.76 | 45.4 | 24.72 | 0.55 | 83.53 | 6.73 | 26.0 | -4.976 | 25.03 | PELENGKAP |  |
| pocket_pivot&q1:j_52w_tinggi | 5390 | 22.0 | 1.895 | 38.81 | 1.15 | 82.9 | 14.34 | 27.77 | 42.3 | 22.0 | 0.22 | 79.63 | 5.77 | 22.0 | -6.123 | 21.86 | PELENGKAP |  |
| q5:julat20 | 145218 | 23.32 | 2.009 | 36.75 | 2.03 | 58.7 | 15.16 | 28.69 | 46.0 | 23.32 | 0.83 | 85.67 | 7.12 | 28.0 | -3.963 | 28.11 | PELENGKAP |  |
| rsi_lintas50&q5:bb_lebar | 4607 | 22.94 | 1.976 | 39.51 | 1.61 | 75.0 | 14.12 | 28.55 | 46.36 | 22.94 | 0.72 | 84.96 | 7.34 | 25.0 | -6.169 | 22.88 | PELENGKAP |  |
| rsi_lintas50&q1:j_ma200 | 5381 | 20.94 | 1.804 | 38.8 | 1.3 | 76.5 | 14.11 | 27.05 | 42.78 | 20.94 | 0.45 | 80.5 | 5.89 | 24.0 | -5.213 | 23.56 | PELENGKAP |  |
| q5:bb_lebar | 140650 | 21.76 | 1.874 | 37.93 | 1.89 | 60.8 | 14.49 | 27.47 | 44.51 | 21.76 | 0.77 | 83.92 | 6.74 | 29.0 | -3.859 | 28.01 | PELENGKAP |  |
| macd_cross&q1:j_ma200 | 4890 | 20.53 | 1.768 | 35.36 | 1.23 | 60.7 | 15.21 | 26.38 | 42.46 | 20.53 | 0.41 | 79.96 | 5.69 | 29.0 | -4.144 | 27.01 | PELENGKAP |  |
| pocket_pivot&q1:j_ma200 | 4487 | 20.75 | 1.787 | 38.78 | 1.18 | 83.3 | 13.93 | 26.61 | 41.69 | 20.75 | 0.22 | 79.51 | 5.55 | 21.0 | -5.557 | 22.24 | PELENGKAP |  |
| macd_cross&q5:bb_lebar | 5435 | 20.63 | 1.777 | 37.9 | 1.51 | 62.5 | 14.31 | 26.4 | 43.18 | 20.63 | 0.59 | 81.93 | 6.16 | 28.0 | -4.491 | 26.59 | PELENGKAP |  |
| q1:j_52w_tinggi | 109065 | 26.52 | 2.284 | 33.73 | 1.96 | 57.6 | 16.95 | 31.08 | 47.92 | 26.52 | 0.88 | 88.81 | 7.58 | 28.0 | -3.922 | 28.21 | PELENGKAP |  |
| q5:j_ema9 | 37832 | 15.91 | 1.37 | 45.54 | 1.39 | 89.4 | 11.45 | 22.57 | 37.39 | 15.91 | 0.33 | 73.5 | 5.2 | 24.0 | -4.716 | 23.56 | PELENGKAP | BUNYI LATAR |
| pocket_pivot&q5:bb_lebar | 9296 | 18.02 | 1.552 | 43.99 | 1.69 | 90.0 | 12.14 | 24.28 | 40.31 | 18.02 | 0.39 | 80.21 | 6.2 | 24.0 | -4.743 | 23.35 | PELENGKAP |  |
| q1:cerun_ema21 | 96411 | 21.38 | 1.842 | 35.14 | 1.88 | 50.9 | 15.27 | 27.31 | 43.49 | 21.38 | 0.74 | 82.1 | 6.16 | 31.0 | -2.587 | 32.09 | PELENGKAP |  |
| macd_cross&q1:rs_spy_6b | 4346 | 19.4 | 1.671 | 41.58 | 1.15 | 59.6 | 13.2 | 25.44 | 41.47 | 19.4 | 0.46 | 77.87 | 5.27 | 26.0 | -5.39 | 22.78 | PELENGKAP |  |
| q1:j_ma200 | 126698 | 22.29 | 1.919 | 34.68 | 1.79 | 56.2 | 15.65 | 27.99 | 43.83 | 22.29 | 0.69 | 82.8 | 6.33 | 29.0 | -3.201 | 29.59 | PELENGKAP |  |
| rsi_lintas50&q1:cerun_ma50 | 5088 | 18.85 | 1.623 | 41.12 | 1.36 | 77.5 | 13.18 | 25.36 | 40.93 | 18.85 | 0.33 | 77.19 | 5.17 | 26.0 | -4.403 | 25.77 | PELENGKAP |  |
| pocket_pivot&q1:rs_spy_6b | 5302 | 16.56 | 1.426 | 46.93 | 0.98 | 80.7 | 10.91 | 22.62 | 37.84 | 16.56 | 0.19 | 72.88 | 4.77 | 21.0 | -6.266 | 18.37 | PELENGKAP | BUNYI LATAR |
| q1:j_ma50 | 187641 | 17.13 | 1.476 | 38.76 | 1.71 | 53.3 | 13.64 | 24.39 | 38.54 | 17.13 | 0.49 | 73.06 | 4.64 | 31.0 | -2.01 | 31.84 | PELENGKAP | BUNYI LATAR |


Taburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. p90 dan % ≥ 100% ialah pembeza, bukan median.


**Lift jatuh besar antara Step 4 dan Step 7** (contoh `rsi_lintas50&q5:atr_pct`: lift 17.43 dalam populasi peristiwa → lift_tepat 2.15 atas semua hari universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. Angka Step 7 yang lebih dekat dengan dagangan sebenar.


### Penapis Step 7.4
168 kombinasi signal × penapis diuji (0 lulus kriteria "buang ≥ 30% palsu dan ≤ 10% benar").


**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis dipradaftar. Ini keputusan negatif yang bersih.


10 contoh penapis terbaik (ikut % palsu dibuang):


| signal | buang_palsu_pct | buang_benar_pct |
|---|---|---|
| q1:j_ma50 | penapis:harga_atas_ma50 | 100.0 | 100.0 |
| macd_cross&q1:j_ma200 | penapis:lapis_ge_3 | 100.0 | 100.0 |
| rsi_lintas50&q1:j_ma200 | penapis:lapis_ge_3 | 99.9 | 99.4 |
| pocket_pivot&q1:j_ma200 | penapis:lapis_ge_3 | 99.8 | 100.0 |
| q1:j_ma200 | penapis:lapis_ge_3 | 99.8 | 99.9 |
| macd_cross&q1:rs_spy_6b | penapis:lapis_ge_3 | 99.6 | 100.0 |
| q1:cerun_ema21 | penapis:lapis_ge_3 | 99.4 | 99.3 |
| q1:cerun_ema21 | penapis:harga_atas_ma50 | 99.1 | 99.2 |
| rsi_lintas50&q1:cerun_ma50 | penapis:lapis_ge_3 | 98.6 | 98.6 |
| rsi_lintas50&q1:j_52w_tinggi | penapis:lapis_ge_3 | 98.2 | 97.9 |


## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)

Set kemasukan: gabungan semua kemunculan 18 signal yang lulus Step 7 = 234,590 (ticker, tarikh) unik, disampel berlapis ikut bulan ke **24,000** (benih 42; SPEC §13.9). Grid 18 HOLD × 13 EXIT = **234** sistem.


### TIGA RUJUKAN WAJIB

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_menang | purata_kalah | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 | pct_terpotong_data | siri_kalah_terpanjang |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 24000 | -3.64 | 0.55 | 0.547 | 46.05 | 36.62 | 30.24 | 252.0 | -28.24 | 0.0 | 100.0 | 0.0 | 18 |
| REF_jual_hari63 | 24000 | -3.81 | -3.17 | -3.171 | 43.2 | 18.27 | 19.47 | 63.0 | -16.09 | 76.7 | 0.0 | 0.0 | 32 |
| REF_chandelier_4atr | 24000 | -8.27 | -4.77 | -4.771 | 32.17 | 18.1 | 15.62 | 50.5 | -11.73 | 79.7 | 0.1 | 0.0 | 56 |


**Keputusan: 14 / 234 sistem mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = 0.547%, "pegang tanpa jual hingga hari ke-252"). Ini berlaku kerana rujukan itu sendiri lemah tahun ini, bukan semestinya kerana sistem itu kuat.


Ukuran mutlak, bukan kedudukan: **18 / 234** sistem berjangkaan positif dan **18 / 234** bermedian pulangan positif. 

Semuanya masih perlu melalui FDR keluarga SISTEM dalam Step 8 (0/234 lulus q ≤ 0.01).


### 15 sistem terbaik daripada 234

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 |
|---|---|---|---|---|---|---|---|---|---|
| rsi_70_60|X=7%,Y=ema9 | 24000 | 2.26 | 0.86 | 0.855 | 54.86 | 102.6 | -15.86 | 59.4 | 8.9 |
| rsi_70_60|X=5%,Y=ema9 | 24000 | 2.26 | 0.85 | 0.854 | 54.87 | 102.6 | -15.86 | 59.4 | 8.9 |
| rsi_70_60|X=15%,Y=ema9 | 24000 | 2.24 | 0.85 | 0.849 | 54.84 | 102.6 | -15.86 | 59.4 | 8.9 |
| rsi_70_60|X=10%,Y=ema9 | 24000 | 2.24 | 0.85 | 0.848 | 54.82 | 102.6 | -15.86 | 59.4 | 8.9 |
| rsi_70_60|X=12%,Y=ema9 | 24000 | 2.23 | 0.84 | 0.842 | 54.81 | 102.6 | -15.86 | 59.5 | 8.9 |
| rsi_70_60|X=20%,Y=ema9 | 24000 | 2.24 | 0.84 | 0.839 | 54.83 | 102.6 | -15.86 | 59.4 | 8.9 |
| rsi_70_60|X=5%,Y=ema21 | 24000 | 2.21 | 0.81 | 0.81 | 54.83 | 103.0 | -15.89 | 59.5 | 8.9 |
| rsi_70_60|X=5%,Y=ma50 | 24000 | 2.21 | 0.8 | 0.797 | 54.84 | 103.1 | -15.92 | 59.5 | 8.9 |
| rsi_70_60|X=7%,Y=ema21 | 24000 | 2.17 | 0.79 | 0.794 | 54.76 | 103.6 | -15.9 | 59.2 | 9.1 |
| rsi_70_60|X=7%,Y=ma50 | 24000 | 2.07 | 0.73 | 0.731 | 54.6 | 103.9 | -15.95 | 59.2 | 9.2 |
| rsi_70_60|X=10%,Y=ema21 | 24000 | 2.03 | 0.67 | 0.671 | 54.54 | 103.8 | -15.91 | 59.3 | 9.1 |
| rsi_70_60|X=12%,Y=ema21 | 24000 | 1.96 | 0.62 | 0.617 | 54.42 | 104.1 | -15.92 | 59.3 | 9.2 |
| rsi_70_60|X=15%,Y=ema21 | 24000 | 1.94 | 0.6 | 0.603 | 54.31 | 104.2 | -15.92 | 59.2 | 9.3 |
| rsi_70_60|X=20%,Y=ema21 | 24000 | 1.96 | 0.58 | 0.58 | 54.33 | 104.4 | -15.92 | 59.2 | 9.4 |
| rsi_70_60|X=10%,Y=ma50 | 24000 | 1.79 | 0.51 | 0.509 | 54.11 | 105.2 | -16.05 | 58.8 | 9.7 |


Perhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.


## 10. Step 8 — kawalan kebetulan

### Ujian label rawak dan FDR per keluarga

| keluarga | N | lulus_fdr | ambang_p |
|---|---|---|---|
| ENTRY/PADU | 21 | 15 | 0.004995004995004995 |
| ENTRY/SUPER PADU | 21 | 7 | 0.002997002997002997 |
| HOLD | 18 | 13 | 0.004975124378109453 |
| EXIT | 66 | 0 |  |
| SISTEM | 234 | 0 |  |


Perbandingan yang diminta arahan: **15 signal lulus FDR daripada 21 diuji**, manakala label rawak menghasilkan lift purata yang jauh lebih rendah (lajur `lift_purata_rawak` dalam `kawalan_rawak_bootstrap_2022.csv`).


### Jangkaan atas SEMUA kemunculan + ujian outlier

| signal | n_kemunculan | median_pulangan | jangkaan | jangkaan_tanpa_5pct_teratas | pct_rugi_lebih_10 | siri_kalah_terpanjang | jangkaan_bawah95_blok_ticker | jangkaan_bawah95_blok_minggu |
|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | 5769 | -14.12 | -6.716 | -10.054 | 72.5 | 52 | -7.453 | -8.573 |
| q5:atr_pct | 109463 | -13.86 | -5.128 | -8.812 | 67.4 | 280 | -5.71 | -7.152 |
| rsi_lintas50&q5:julat20 | 5155 | -13.46 | -6.387 | -9.719 | 68.3 | 53 | -7.145 | -8.249 |
| rsi_lintas50&q1:j_52w_tinggi | 5614 | -12.04 | -4.976 | -7.983 | 60.5 | 44 | -5.692 | -7.158 |
| pocket_pivot&q1:j_52w_tinggi | 5390 | -11.99 | -6.123 | -8.942 | 61.9 | 43 | -6.826 | -8.142 |
| q5:julat20 | 145218 | -11.31 | -3.963 | -7.298 | 56.7 | 274 | -4.427 | -5.743 |
| rsi_lintas50&q5:bb_lebar | 4607 | -12.99 | -6.169 | -9.389 | 65.2 | 60 | -6.928 | -8.185 |
| rsi_lintas50&q1:j_ma200 | 5381 | -11.06 | -5.213 | -8.118 | 55.4 | 43 | -5.862 | -7.332 |
| q5:bb_lebar | 140650 | -10.45 | -3.859 | -7.079 | 52.3 | 233 | -4.283 | -5.548 |
| macd_cross&q1:j_ma200 | 4890 | -10.29 | -4.144 | -7.195 | 51.4 | 28 | -4.688 | -6.405 |
| pocket_pivot&q1:j_ma200 | 4487 | -11.32 | -5.557 | -8.413 | 56.7 | 49 | -6.327 | -7.56 |
| macd_cross&q5:bb_lebar | 5435 | -10.98 | -4.491 | -7.694 | 55.2 | 24 | -5.007 | -6.489 |
| q1:j_52w_tinggi | 109065 | -11.61 | -3.922 | -7.259 | 57.5 | 281 | -4.414 | -6.215 |
| q5:j_ema9 | 37832 | -9.77 | -4.716 | -7.447 | 48.6 | 124 | -5.144 | -6.382 |
| pocket_pivot&q5:bb_lebar | 9296 | -10.32 | -4.743 | -7.712 | 52.2 | 46 | -5.41 | -6.344 |
| q1:cerun_ema21 | 96411 | -9.21 | -2.587 | -5.748 | 46.2 | 178 | -3.003 | -4.675 |
| macd_cross&q1:rs_spy_6b | 4346 | -10.72 | -5.39 | -8.563 | 54.3 | 33 | -5.962 | -7.646 |
| q1:j_ma200 | 126698 | -9.89 | -3.201 | -6.33 | 49.4 | 312 | -3.65 | -5.418 |
| rsi_lintas50&q1:cerun_ma50 | 5088 | -10.26 | -4.403 | -7.228 | 51.7 | 35 | -5.011 | -7.145 |
| pocket_pivot&q1:rs_spy_6b | 5302 | -10.4 | -6.266 | -8.968 | 52.7 | 75 | -6.882 | -8.085 |
| q1:j_ma50 | 187641 | -7.9 | -2.01 | -4.843 | 38.1 | 260 | -2.317 | -4.01 |


### Keputusan gate demi gate

| signal | G1_sah_dalam_tahun | G2_merentas_tahun | G3_nilai_p | G3_fdr | G4_bootstrap | G5_outlier | G6 | step7 | keputusan |
|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=LANGKA; 2021=TIDAK BERGUNA; 2023=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:atr_pct | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2021=TIDAK BERGUNA; 2023=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:julat20 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2020=UNIQUE; 2021=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2023=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2023=LANGKA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:julat20 | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2021=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:bb_lebar | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:j_ma200 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=SEDERHANA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:bb_lebar | GAGAL | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2021=UNIQUE; 2023=TIDAK BERGUNA; 2024=SEDERHANA; 2025=TERAS) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q1:j_ma200 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.43656 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:j_ma200 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.002 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q5:bb_lebar | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=LANGKA; 2021=LANGKA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.46553 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:j_52w_tinggi | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2023=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.005 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:j_ema9 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| pocket_pivot&q5:bb_lebar | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:cerun_ema21 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini COMMON BIASA, bukan penemuan; 2020=TERAS; 2021=-; 2023=-; 2024=-; 2025=-) | 0.48551 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | STATISTIK SAHAJA | LULUS | DITOLAK |
| macd_cross&q1:rs_spy_6b | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.39261 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:j_ma200 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=SEDERHANA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=SEDERHANA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.54645 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:rs_spy_6b | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q1:j_ma50 | GAGAL | TIDAK BOLEH DINILAI (kelas tahun ini COMMON BIASA, bukan penemuan; 2020=SEDERHANA; 2021=SEDERHANA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TERAS) | 0.36763 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |


**DITERIMA: 0** · **CALON: 0** · **DITOLAK: 21.**


Tiada CALON. Gate yang membunuh semua signal ialah **G4 (bootstrap)** dan **G5 (outlier)**: jangkaan tidak bertahan pada had bawah 95% blok ticker atau blok minggu, dan jatuh ke ≤ 0 apabila 5% pemenang teratas dibuang. Maknanya pulangan signal tahun ini datang daripada beberapa kemunculan melampau, bukan daripada kelebihan yang boleh diulang.


Penapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam ≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada 2022.


## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)

Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. Asas signal ENTRY: **lulus Step 7 sahaja (TIADA signal CALON tahun ini)**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → RS 6 bulan → ticker.


> Angka di bawah **bukan** bukti sistem lulus — tiada signal ENTRY tahun ini lulus Step 8. Ia dilaporkan supaya kriteria akhir ada angka dan baris merentas tahun setara (SPEC §13.10).


| sistem | n_posisi_dibuka | n_dagangan_ditutup | n_posisi_terbuka_hujung_tahun | purata_slot_terisi | pulangan_tahun | median_bulanan | purata_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terbaik | bulan_terburuk | mdd | purata_hari_pegang | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 8 | 0 | 8 | 7.94 | -16.0 | 2.38 | -0.75 | 16.7 | 58.3 | 19.22 | -20.97 | -24.96 |  | 0.7 | -18.65 | -24.5 |
| REF_chandelier_4atr | 38 | 30 | 8 | 7.82 | -5.26 | 1.93 | -0.01 | 8.3 | 50.0 | 10.94 | -18.0 | -37.88 | 52.4 | 3.2 | -18.65 | -24.5 |
| REF_jual_hari63 | 40 | 32 | 8 | 7.81 | -20.03 | 1.46 | -1.29 | 16.7 | 50.0 | 11.39 | -20.97 | -34.08 | 63.0 | 3.3 | -18.65 | -24.5 |
| rsi_70_60|X=7%,Y=ema9 | 25 | 17 | 8 | 7.87 | -5.65 | 2.66 | 0.03 | 16.7 | 50.0 | 13.65 | -17.12 | -34.22 | 68.9 | 2.1 | -18.65 | -24.5 |
| rsi_70_60|X=5%,Y=ema9 | 25 | 17 | 8 | 7.87 | -5.65 | 2.66 | 0.03 | 16.7 | 50.0 | 13.65 | -17.12 | -34.22 | 68.9 | 2.1 | -18.65 | -24.5 |
| rsi_70_60|X=15%,Y=ema9 | 25 | 17 | 8 | 7.87 | -5.65 | 2.66 | 0.03 | 16.7 | 50.0 | 13.65 | -17.12 | -34.22 | 68.9 | 2.1 | -18.65 | -24.5 |
| KAWALAN_RAWAK|pegang_252 | 8 | 0 | 8 | 7.94 | -36.92 | -0.88 | -3.4 | 0.0 | 50.0 | 8.58 | -15.75 | -38.78 |  | 0.7 | -18.65 | -24.5 |
| KAWALAN_RAWAK|chandelier | 56 | 48 | 8 | 7.75 | -36.9 | -3.8 | -3.47 | 0.0 | 33.3 | 9.01 | -14.63 | -39.48 | 36.6 | 4.7 | -18.65 | -24.5 |


### Pulangan bulanan penuh (%)

| tarikh | REF_pegang_252 | REF_chandelier_4atr | REF_jual_hari63 | rsi_70_60|X=7%,Y=ema9 | rsi_70_60|X=5%,Y=ema9 | rsi_70_60|X=15%,Y=ema9 | KAWALAN_RAWAK|pegang_252 | KAWALAN_RAWAK|chandelier |
|---|---|---|---|---|---|---|---|---|
| 2022-01-31 | -20.97 | -18.0 | -20.97 | -17.12 | -17.12 | -17.12 | -10.29 | -9.98 |
| 2022-02-28 | 6.13 | 9.46 | 6.13 | 6.49 | 6.49 | 6.49 | 1.58 | -2.66 |
| 2022-03-31 | 3.01 | 4.25 | 3.01 | -0.76 | -0.76 | -0.76 | -1.93 | -7.46 |
| 2022-04-30 | -0.98 | -0.39 | -17.38 | -14.01 | -14.01 | -14.01 | -9.87 | -13.1 |
| 2022-05-31 | 1.75 | 10.94 | 7.83 | 6.08 | 6.08 | 6.08 | 0.17 | 6.8 |
| 2022-06-30 | -10.25 | -15.76 | -0.1 | -7.15 | -7.15 | -7.15 | -15.75 | -14.63 |
| 2022-07-31 | 19.22 | 8.13 | 4.76 | 10.16 | 10.16 | 10.16 | 8.58 | 4.69 |
| 2022-08-31 | 4.04 | 7.77 | -3.75 | 13.65 | 13.65 | 13.65 | 2.52 | -1.31 |
| 2022-09-30 | -10.01 | -3.8 | -9.72 | -11.84 | -11.84 | -11.84 | -15.3 | -4.94 |
| 2022-10-31 | 7.37 | -1.64 | 10.16 | 8.74 | 8.74 | 8.74 | 4.69 | 9.01 |
| 2022-11-30 | 10.64 | 5.26 | -6.91 | 8.41 | 8.41 | 8.41 | 6.65 | 1.72 |
| 2022-12-31 | -18.9 | -6.3 | 11.39 | -2.25 | -2.25 | -2.25 | -11.87 | -9.82 |


### Jawapan terus kepada sasaran +10% sebulan

**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:


- `REF_pegang_252`: median bulanan **2.38%**, 16.7% bulan ≥ +10%, bulan terburuk -20.97%, MDD -24.96%, pulangan tahun -16.00% (SPY -18.65%, MDD SPY -24.50%)

- `REF_chandelier_4atr`: median bulanan **1.93%**, 8.3% bulan ≥ +10%, bulan terburuk -18.00%, MDD -37.88%, pulangan tahun -5.26% (SPY -18.65%, MDD SPY -24.50%)

- `REF_jual_hari63`: median bulanan **1.46%**, 16.7% bulan ≥ +10%, bulan terburuk -20.97%, MDD -34.08%, pulangan tahun -20.03% (SPY -18.65%, MDD SPY -24.50%)

- `rsi_70_60|X=7%,Y=ema9`: median bulanan **2.66%**, 16.7% bulan ≥ +10%, bulan terburuk -17.12%, MDD -34.22%, pulangan tahun -5.65% (SPY -18.65%, MDD SPY -24.50%)

- `rsi_70_60|X=5%,Y=ema9`: median bulanan **2.66%**, 16.7% bulan ≥ +10%, bulan terburuk -17.12%, MDD -34.22%, pulangan tahun -5.65% (SPY -18.65%, MDD SPY -24.50%)

- `rsi_70_60|X=15%,Y=ema9`: median bulanan **2.66%**, 16.7% bulan ≥ +10%, bulan terburuk -17.12%, MDD -34.22%, pulangan tahun -5.65% (SPY -18.65%, MDD SPY -24.50%)

- `KAWALAN_RAWAK|pegang_252`: median bulanan **-0.88%**, 0.0% bulan ≥ +10%, bulan terburuk -15.75%, MDD -38.78%, pulangan tahun -36.92% (SPY -18.65%, MDD SPY -24.50%)

- `KAWALAN_RAWAK|chandelier`: median bulanan **-3.80%**, 0.0% bulan ≥ +10%, bulan terburuk -14.63%, MDD -39.48%, pulangan tahun -36.90% (SPY -18.65%, MDD SPY -24.50%)


**Apa yang menghalang — kapasiti, bukan kadar menang.**

- Sistem terbaik (`REF_pegang_252`) hanya membuka **8 posisi sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh dijadikan asas keputusan.

- Sistem yang pusing ganti mencukupi (Chandelier: 38 posisi, 3.2/bulan) memberi median bulanan hanya 1.93% dengan MDD -37.88% — lebih buruk daripada MDD SPY.

- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.

- KAWALAN RAWAK pegang-252 memberi -36.92% dan Chandelier rawak -36.90% — dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.


### Banding wajib: SPY dan KAWALAN RAWAK

- SPY tempoh sama: **-18.65%** (MDD -24.50%). **1/6** sistem kalah kepada SPY.

- KAWALAN RAWAK terbaik: **-36.90%** (`KAWALAN_RAWAK|chandelier`). **0/6** sistem kalah kepada entri rawak.


> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.


## 12. Keputusan akhir (had fasa: CALON)

1. **ENTRY** — TIADA signal CALON pada 2022. Semua gagal G4 (bootstrap) dan/atau G5 (outlier). Pemicu klasik tunggal juga tidak lulus.

2. **HOLD** — 13/18 signal lulus FDR; kelas pullback ialah hasil paling kukuh (SIHAT 65.0% / PASARAN 88.7% menyambung ke puncak baru lawan AMARAN 54.0%).

3. **EXIT** — 0/66 signal lulus FDR; 14/234 sistem mengalahkan ketiga-tiga rujukan dan 0/234 lulus FDR keluarga SISTEM. **Tahun ini exit aktif berbaloi** kerana memegang tanpa jual hampir tidak menguntungkan.

4. **PORTFOLIO** — sasaran +10% sebulan tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila pegangan panjang, bukan kadar menang.

5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam ≥ 2 tahun LAIN; tahun lain yang siap: [2020, 2021, 2023, 2024, 2025]. Lihat `BANDING_TAHUN.md` untuk status merentas tahun.


## 13. Fail output

| Fail | Isi |
|---|---|
| `runs_2022.csv` | 5541 run, 34 lajur |
| `monthly_summary_2022.csv` | ringkasan 12 bulan |
| `skipped_2022.csv` | 10378 calon ditolak + sebab |
| `kohort_masih_naik_2022.csv` | 297 run masih_naik dijejak 252 hari |
| `common_unique_2022.csv` | 3472 baris (213 signal × subset × populasi × kumpulan × keluarga) |
| `taburan_indikator_2022.csv` | median + p25/p75 setiap indikator setiap hasil |
| `hold_exit_2022.csv` | 364 baris CALON HOLD/EXIT |
| `false_signal_2022.csv` | 189 baris (signal + penapis) |
| `hadapan_hold_exit_2022.csv` | 237 sistem (234 + 3 rujukan) |
| `kawalan_rawak_bootstrap_2022.csv` | nilai-p label rawak + had bawah bootstrap |
| `jangkaan_kemunculan_2022.csv` | jangkaan + ujian outlier |
| `keputusan_2022.csv` | keputusan gate demi gate |
| `portfolio_2022.csv`, `portfolio_bulanan_2022.csv` | Step 9 |
| `log_ujian.csv` | setiap signal/kombinasi yang diuji |
| `PANDANG_HADAPAN_2022.md` | imbasan pandang ke hadapan |
| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |
