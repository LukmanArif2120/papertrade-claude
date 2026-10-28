# LAPORAN REVERSE 2024 — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.

> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = **satu rejim pasaran**. Peta sektor bukan titik-masa. Gate 8.1 ada 5 tahun lain ([2020, 2021, 2022, 2023, 2025]); keputusan **maksimum CALON** (SPEC §11.8).

## 0. Jawapan ringkas

1. **3744 run layak** dikenal pasti dalam 2024; setiap 12 bulan ada calon (tiada "TIADA CALON"). 58 SUPER PADU (≥100%), 1537 PADU, 2149 BIASA.

2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada 374 run yang masih naik pada hari ke-63, **22.7% akhirnya melebihi +100%**, dengan median kenaikan penuh **65.3%** lawan 37.3% pada hari ke-63.

3. **Signal entry: TIADA CALON** daripada 18 yang masuk corong. 18 gagal gate bootstrap (G4) dan 18 ditanda BERGANTUNG PADA OUTLIER (G5). Ini keputusan, bukan kegagalan teknikal: tiada signal ENTRY tahun ini bertahan selepas had bawah 95% bootstrap blok dan ujian tanpa 5% pemenang teratas.

4. **Rujukan "pegang tanpa jual hingga hari ke-252" MENANG.** Tiada satu pun daripada 234 sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan. Jangkaan: +8.68% (pegang tanpa jual hingga hari ke-252), +1.34% (jual hari ke-63), -0.02% (Chandelier 4×ATR14). Mengikut arahan Step 7b.4, jawapan kajian tahun ini ialah **"jangan jual"**.

5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan pegang-252 hanya membuka **8 posisi sepanjang tahun** (8 slot terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. Pulangannya -0.43% ialah hasil **8 saham**, bukan sistem.

6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik ialah -2.02% sebulan (median) dengan MDD -25.26%.

7. **Keluarga EXIT dan SISTEM pada FDR:** 0/62 signal EXIT dan 0/234 sistem lulus q ≤ 0.01.

## 1. Semakan kesediaan Step 0

| Semakan | Hasil |
|---|---|
| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, 2009-01-02 → 2026-10-16; semua sha256 sepadan |
| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |
| c. Sumber sektor/industri setiap ticker | **LULUS** — 2256/2264 = 99.6% (3 kelas saham diisi daripada ticker asas; 97 ticker = `Lain-lain`) |
| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 (indeks sektor A02; diluluskan pengguna) |
| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — 0.115 s/ticker; larian penuh 2264 ticker = 261 s |
| f. `semak_hadapan` atas modul indikator | **LULUS** — 14 tarikh potong (≥ 12), 26,950 perbandingan, **0 kegagalan** (`REVERSE/PANDANG_HADAPAN_2024.md`) |

## 2. Step 1–2 — run

Saiz universe 2024 setiap bulan: min **2000**, median **2000**, maks **2000**; 2264 ticker berbeza sepanjang tahun.

| bulan | n_run | n_super | n_padu | n_biasa | n_bertangga | n_lonjakan | n_stabil | n_entry_sah | n_masih_naik | n_peristiwa | med_naik |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2024-01 | 174 | 5 | 73 | 96 | 6 | 88 | 80 | 131 | 5 | 1311 | 26.8 |
| 2024-02 | 207 | 6 | 79 | 122 | 14 | 109 | 84 | 165 | 35 | 1219 | 24.8 |
| 2024-03 | 152 | 0 | 62 | 90 | 4 | 101 | 47 | 114 | 13 | 959 | 23.4 |
| 2024-04 | 503 | 11 | 269 | 223 | 33 | 227 | 243 | 427 | 118 | 1287 | 31.1 |
| 2024-05 | 301 | 4 | 141 | 156 | 19 | 142 | 140 | 242 | 45 | 911 | 28.6 |
| 2024-06 | 365 | 3 | 133 | 229 | 18 | 167 | 180 | 260 | 42 | 1149 | 25.1 |
| 2024-07 | 302 | 2 | 118 | 182 | 21 | 155 | 126 | 265 | 36 | 1197 | 23.9 |
| 2024-08 | 431 | 14 | 235 | 182 | 32 | 178 | 221 | 320 | 79 | 1412 | 32.3 |
| 2024-09 | 274 | 7 | 134 | 133 | 22 | 138 | 114 | 245 | 30 | 1431 | 30.6 |
| 2024-10 | 441 | 3 | 135 | 303 | 19 | 310 | 112 | 384 | 31 | 1188 | 22.9 |
| 2024-11 | 376 | 3 | 89 | 284 | 12 | 237 | 127 | 308 | 20 | 1457 | 18.2 |
| 2024-12 | 218 | 0 | 69 | 149 | 6 | 126 | 86 | 150 | 3 | 630 | 23.3 |


Jumlah: **3744 run layak**, 3011 (80.4%) dengan `entry_sah = ya` (tiada amaran: syarat 10 hari menolak 19.6% < 50%). Dilangkau: 15566 (14828 "terlalu perlahan").


### Bucket %_naik × tempoh

| bucket_pct | <=21 | <=42 | <=63 |
|---|---|---|---|
| 10%+ | 1219 | 0 | 0 |
| 100%+ | 6 | 5 | 40 |
| 20%+ | 341 | 589 | 0 |
| 200%+ | 0 | 1 | 6 |
| 30%+ | 121 | 252 | 836 |
| 50%+ | 18 | 69 | 241 |


### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)

| kumpulan | PANTAS | PERLAHAN | SEDANG |
|---|---|---|---|
| BIASA | 1560 | 0 | 589 |
| PADU | 139 | 1077 | 321 |
| SUPER PADU | 6 | 46 | 6 |


Sel SAMPEL KECIL: [('SUPER PADU', 'PANTAS'), ('SUPER PADU', 'SEDANG')]


### Jenis kenaikan

| jenis | n |
|---|---|
| LONJAKAN | 1978 |
| STABIL | 1560 |
| BERTANGGA | 206 |


`graf_menaik = ya` (S3): 2080 (55.6%). `masih_naik = ya`: 457.


### 10 run terbaik setiap bulan (ikut %_naik_rendah)


**2024-01**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| NRIX | Healthcare | 2024-01-24 | 2024-04-09 | 52 | 127.16 | SUPER PADU | LONJAKAN | ya | tidak |
| CVNA | Consumer Cyclical | 2024-01-17 | 2024-03-26 | 48 | 123.12 | SUPER PADU | LONJAKAN | ya | tidak |
| COIN | Financial Services | 2024-01-16 | 2024-03-25 | 48 | 120.45 | SUPER PADU | STABIL | tidak | tidak |
| MARA | Financial Services | 2024-01-19 | 2024-02-28 | 27 | 112.24 | SUPER PADU | LONJAKAN | tidak | tidak |
| DJT | Communication Services | 2024-01-25 | 2024-03-27 | 43 | 107.46 | SUPER PADU | LONJAKAN | ya | tidak |
| RGNX | Healthcare | 2024-01-08 | 2024-03-05 | 39 | 92.87 | PADU | LONJAKAN | tidak | tidak |
| RIOT | Financial Services | 2024-01-19 | 2024-02-14 | 18 | 82.87 | PADU | STABIL | tidak | tidak |
| EH | Industrials | 2024-01-22 | 2024-03-28 | 47 | 79.81 | PADU | STABIL | tidak | tidak |
| HUT | Financial Services | 2024-01-19 | 2024-03-28 | 48 | 78.64 | PADU | LONJAKAN | tidak | tidak |
| SE | Consumer Cyclical | 2024-01-17 | 2024-03-14 | 40 | 76.86 | PADU | STABIL | ya | tidak |


**2024-02**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| GME | Consumer Cyclical | 2024-02-23 | 2024-05-14 | 56 | 271.57 | SUPER PADU | LONJAKAN | ya | tidak |
| MSTR | Technology | 2024-02-13 | 2024-03-27 | 30 | 192.76 | SUPER PADU | STABIL | ya | tidak |
| RILY | Financial Services | 2024-02-07 | 2024-04-29 | 56 | 130.43 | SUPER PADU | LONJAKAN | ya | tidak |
| ASPN | Basic Materials | 2024-02-09 | 2024-05-10 | 63 | 128.12 | SUPER PADU | LONJAKAN | ya | ya |
| ACMR | Technology | 2024-02-05 | 2024-03-01 | 18 | 115.99 | SUPER PADU | LONJAKAN | ya | tidak |
| BE | Industrials | 2024-02-23 | 2024-05-22 | 62 | 102.09 | SUPER PADU | BERTANGGA | ya | ya |
| CC | Basic Materials | 2024-02-29 | 2024-05-15 | 53 | 94.61 | PADU | STABIL | ya | tidak |
| SA | Basic Materials | 2024-02-14 | 2024-04-03 | 33 | 78.84 | PADU | BERTANGGA | ya | tidak |
| AA | Basic Materials | 2024-02-26 | 2024-05-21 | 60 | 78.43 | PADU | STABIL | ya | tidak |
| STAA | Healthcare | 2024-02-21 | 2024-04-09 | 33 | 76.4 | PADU | STABIL | ya | tidak |


**2024-03**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| CHWY | Consumer Cyclical | 2024-03-26 | 2024-06-25 | 62 | 98.87 | PADU | LONJAKAN | ya | ya |
| SMTC | Technology | 2024-03-20 | 2024-05-08 | 34 | 89.47 | PADU | STABIL | ya | tidak |
| GH | Healthcare | 2024-03-26 | 2024-06-12 | 54 | 88.18 | PADU | STABIL | ya | tidak |
| DELL | Technology | 2024-03-18 | 2024-05-29 | 50 | 71.9 | PADU | STABIL | ya | tidak |
| GPCR | Healthcare | 2024-03-14 | 2024-06-05 | 57 | 67.31 | PADU | LONJAKAN | ya | tidak |
| EAT | Consumer Cyclical | 2024-03-21 | 2024-06-05 | 52 | 63.36 | PADU | STABIL | ya | tidak |
| ALXO | Healthcare | 2024-03-18 | 2024-05-07 | 35 | 62.89 | PADU | STABIL | tidak | tidak |
| AOSL | Technology | 2024-03-20 | 2024-06-20 | 63 | 59.82 | PADU | STABIL | ya | ya |
| RUN | Technology | 2024-03-14 | 2024-06-05 | 57 | 59.61 | PADU | LONJAKAN | ya | tidak |
| PHAT | Healthcare | 2024-03-14 | 2024-04-09 | 17 | 59.6 | PADU | LONJAKAN | ya | tidak |


**2024-04**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| INSM | Healthcare | 2024-04-19 | 2024-07-16 | 59 | 231.41 | SUPER PADU | LONJAKAN | tidak | tidak |
| HUT | Financial Services | 2024-04-16 | 2024-07-16 | 62 | 201.15 | SUPER PADU | BERTANGGA | ya | ya |
| HROW | Healthcare | 2024-04-25 | 2024-07-22 | 59 | 156.39 | SUPER PADU | BERTANGGA | tidak | tidak |
| DJT | Communication Services | 2024-04-16 | 2024-05-09 | 17 | 141.2 | SUPER PADU | BERTANGGA | ya | tidak |
| CDNA | Healthcare | 2024-04-16 | 2024-07-16 | 62 | 136.86 | SUPER PADU | LONJAKAN | tidak | ya |
| AMSC | Industrials | 2024-04-10 | 2024-07-11 | 63 | 135.77 | SUPER PADU | STABIL | tidak | ya |
| GL | Financial Services | 2024-04-11 | 2024-05-08 | 19 | 129.76 | SUPER PADU | STABIL | tidak | tidak |
| RIVN | Consumer Cyclical | 2024-04-16 | 2024-07-12 | 60 | 119.25 | SUPER PADU | BERTANGGA | tidak | tidak |
| NVCR | Healthcare | 2024-04-22 | 2024-05-20 | 20 | 105.56 | SUPER PADU | STABIL | ya | tidak |
| CRDO | Technology | 2024-04-19 | 2024-07-16 | 59 | 101.13 | SUPER PADU | BERTANGGA | tidak | tidak |


**2024-05**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| GME | Consumer Cyclical | 2024-05-24 | 2024-06-06 | 8 | 162.99 | SUPER PADU | LONJAKAN | ya | tidak |
| XPOF | Consumer Cyclical | 2024-05-10 | 2024-07-17 | 45 | 145.79 | SUPER PADU | BERTANGGA | tidak | tidak |
| TMCI | Healthcare | 2024-05-08 | 2024-07-16 | 46 | 115.56 | SUPER PADU | STABIL | tidak | tidak |
| FWRD | Industrials | 2024-05-09 | 2024-07-25 | 52 | 115.33 | SUPER PADU | STABIL | tidak | tidak |
| ZETA | Technology | 2024-05-01 | 2024-08-01 | 63 | 95.68 | PADU | BERTANGGA | ya | ya |
| ALNY | Healthcare | 2024-05-30 | 2024-08-29 | 63 | 95.52 | PADU | LONJAKAN | ya | ya |
| MGNX | Healthcare | 2024-05-10 | 2024-07-26 | 52 | 76.75 | PADU | LONJAKAN | tidak | tidak |
| S | Technology | 2024-05-31 | 2024-08-23 | 58 | 76.27 | PADU | BERTANGGA | tidak | tidak |
| ANAB | Healthcare | 2024-05-29 | 2024-08-21 | 58 | 65.27 | PADU | BERTANGGA | ya | tidak |
| DMRC | Technology | 2024-05-01 | 2024-07-16 | 51 | 64.19 | PADU | STABIL | ya | tidak |


**2024-06**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| PLCE | Consumer Cyclical | 2024-06-20 | 2024-09-17 | 61 | 159.31 | SUPER PADU | LONJAKAN | tidak | ya |
| BMEA | Healthcare | 2024-06-07 | 2024-08-27 | 55 | 117.17 | SUPER PADU | STABIL | tidak | tidak |
| AEHR | Technology | 2024-06-26 | 2024-07-17 | 14 | 109.66 | SUPER PADU | LONJAKAN | ya | tidak |
| ALAR | Technology | 2024-06-18 | 2024-07-03 | 10 | 99.39 | PADU | LONJAKAN | ya | tidak |
| FLNA | Healthcare | 2024-06-11 | 2024-08-05 | 37 | 87.9 | PADU | LONJAKAN | tidak | tidak |
| VSAT | Technology | 2024-06-14 | 2024-08-08 | 37 | 86.09 | PADU | LONJAKAN | tidak | tidak |
| XMTR | Industrials | 2024-06-25 | 2024-08-26 | 43 | 75.79 | PADU | LONJAKAN | tidak | tidak |
| NBR | Energy | 2024-06-17 | 2024-07-31 | 30 | 71.67 | PADU | BERTANGGA | ya | tidak |
| RVLV | Consumer Cyclical | 2024-06-20 | 2024-09-19 | 63 | 70.79 | PADU | LONJAKAN | tidak | ya |
| MLAB | Technology | 2024-06-27 | 2024-08-27 | 42 | 68.33 | PADU | STABIL | ya | tidak |


**2024-07**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| RUN | Technology | 2024-07-02 | 2024-08-23 | 37 | 103.79 | SUPER PADU | BERTANGGA | ya | tidak |
| VST | Utilities | 2024-07-30 | 2024-10-04 | 47 | 101.83 | SUPER PADU | BERTANGGA | ya | tidak |
| CSTL | Healthcare | 2024-07-05 | 2024-09-20 | 54 | 85.5 | PADU | STABIL | tidak | tidak |
| YOU | Technology | 2024-07-01 | 2024-09-30 | 63 | 80.41 | PADU | BERTANGGA | ya | ya |
| DUOL | Technology | 2024-07-25 | 2024-10-09 | 53 | 80.07 | PADU | STABIL | ya | tidak |
| HOV | Consumer Cyclical | 2024-07-02 | 2024-08-22 | 36 | 78.22 | PADU | LONJAKAN | ya | tidak |
| VSXY | Consumer Cyclical | 2024-07-02 | 2024-09-24 | 58 | 72.26 | PADU | STABIL | ya | tidak |
| YUMC | Consumer Cyclical | 2024-07-09 | 2024-10-02 | 60 | 69.31 | PADU | STABIL | ya | tidak |
| FUTU | Financial Services | 2024-07-02 | 2024-10-01 | 63 | 69.06 | PADU | STABIL | ya | ya |
| SG | Consumer Cyclical | 2024-07-10 | 2024-10-08 | 63 | 68.21 | PADU | LONJAKAN | tidak | ya |


**2024-08**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| LEU | Energy | 2024-08-05 | 2024-11-01 | 63 | 226.86 | SUPER PADU | BERTANGGA | ya | ya |
| SMR | Industrials | 2024-08-02 | 2024-10-28 | 60 | 175.0 | SUPER PADU | LONJAKAN | ya | tidak |
| MSTR | Technology | 2024-08-05 | 2024-10-29 | 60 | 152.18 | SUPER PADU | STABIL | tidak | tidak |
| EWTX | Healthcare | 2024-08-05 | 2024-10-18 | 53 | 136.82 | SUPER PADU | LONJAKAN | ya | tidak |
| BILI | Communication Services | 2024-08-12 | 2024-10-02 | 36 | 123.34 | SUPER PADU | STABIL | ya | tidak |
| LMND | Financial Services | 2024-08-14 | 2024-11-11 | 62 | 118.23 | SUPER PADU | LONJAKAN | ya | ya |
| UAL | Industrials | 2024-08-05 | 2024-11-01 | 63 | 117.34 | SUPER PADU | STABIL | tidak | ya |
| AGX | Industrials | 2024-08-05 | 2024-11-01 | 63 | 116.1 | SUPER PADU | BERTANGGA | ya | ya |
| UI | Technology | 2024-08-23 | 2024-11-12 | 56 | 111.82 | SUPER PADU | BERTANGGA | ya | tidak |
| TPC | Industrials | 2024-08-02 | 2024-10-21 | 55 | 111.45 | SUPER PADU | BERTANGGA | tidak | tidak |


**2024-09**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| INOD | Technology | 2024-09-06 | 2024-11-21 | 54 | 232.59 | SUPER PADU | LONJAKAN | tidak | tidak |
| UPST | Financial Services | 2024-09-10 | 2024-11-08 | 43 | 153.76 | SUPER PADU | LONJAKAN | ya | tidak |
| WGS | Healthcare | 2024-09-25 | 2024-10-29 | 24 | 134.17 | SUPER PADU | LONJAKAN | ya | tidak |
| ASAN | Technology | 2024-09-10 | 2024-12-09 | 63 | 125.17 | SUPER PADU | LONJAKAN | ya | ya |
| TPL | Energy | 2024-09-12 | 2024-11-22 | 51 | 119.22 | SUPER PADU | STABIL | ya | tidak |
| UNFI | Consumer Defensive | 2024-09-11 | 2024-12-10 | 63 | 114.02 | SUPER PADU | LONJAKAN | ya | ya |
| AI | Technology | 2024-09-05 | 2024-11-25 | 57 | 100.85 | SUPER PADU | BERTANGGA | ya | tidak |
| TWLO | Technology | 2024-09-10 | 2024-12-06 | 62 | 99.51 | PADU | STABIL | ya | ya |
| DOCU | Technology | 2024-09-11 | 2024-12-06 | 61 | 96.98 | PADU | LONJAKAN | ya | ya |
| EAT | Consumer Cyclical | 2024-09-10 | 2024-11-29 | 57 | 93.24 | PADU | STABIL | ya | tidak |


**2024-10**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| SEZL | Financial Services | 2024-10-10 | 2024-11-25 | 32 | 201.42 | SUPER PADU | LONJAKAN | ya | tidak |
| NVCR | Healthcare | 2024-10-08 | 2024-12-13 | 47 | 135.78 | SUPER PADU | LONJAKAN | ya | tidak |
| DAN | Consumer Cyclical | 2024-10-31 | 2025-01-30 | 60 | 119.79 | SUPER PADU | BERTANGGA | tidak | tidak |
| MNSO | Consumer Cyclical | 2024-10-17 | 2025-01-03 | 53 | 83.98 | PADU | BERTANGGA | ya | tidak |
| SRAD | Technology | 2024-10-24 | 2025-01-28 | 63 | 73.77 | PADU | STABIL | ya | ya |
| MDGL | Healthcare | 2024-10-03 | 2024-11-07 | 25 | 73.45 | PADU | LONJAKAN | tidak | tidak |
| RBLX | Communication Services | 2024-10-29 | 2025-01-30 | 62 | 72.0 | PADU | BERTANGGA | ya | ya |
| WSM | Consumer Cyclical | 2024-10-29 | 2025-01-30 | 62 | 70.35 | PADU | LONJAKAN | tidak | ya |
| PRLB | Industrials | 2024-10-24 | 2024-12-16 | 36 | 69.26 | PADU | LONJAKAN | ya | tidak |
| FRSH | Technology | 2024-10-23 | 2025-01-24 | 62 | 68.43 | PADU | LONJAKAN | ya | ya |


**2024-11**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| OKLO | Utilities | 2024-11-15 | 2025-02-07 | 55 | 220.47 | SUPER PADU | BERTANGGA | ya | tidak |
| EH | Industrials | 2024-11-21 | 2025-02-19 | 58 | 120.14 | SUPER PADU | STABIL | tidak | tidak |
| PGY | Technology | 2024-11-19 | 2025-02-18 | 59 | 106.71 | SUPER PADU | LONJAKAN | ya | tidak |
| CXW | Industrials | 2024-11-04 | 2024-11-11 | 5 | 89.1 | PADU | LONJAKAN | ya | tidak |
| NGNE | Healthcare | 2024-11-21 | 2024-11-26 | 3 | 86.08 | PADU | LONJAKAN | tidak | tidak |
| SMCI | Technology | 2024-11-04 | 2024-12-09 | 24 | 84.77 | PADU | LONJAKAN | tidak | tidak |
| ZETA | Technology | 2024-11-14 | 2024-12-04 | 13 | 62.86 | PADU | LONJAKAN | tidak | tidak |
| NVMI | Technology | 2024-11-27 | 2025-02-20 | 55 | 62.86 | PADU | BERTANGGA | ya | tidak |
| VITL | Consumer Defensive | 2024-11-13 | 2025-01-23 | 46 | 61.66 | PADU | STABIL | ya | tidak |
| DJT | Communication Services | 2024-11-08 | 2025-01-13 | 42 | 60.71 | PADU | LONJAKAN | ya | tidak |


**2024-12**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| SMCI | Technology | 2024-12-20 | 2025-02-19 | 38 | 97.48 | PADU | STABIL | ya | tidak |
| LUNR | Industrials | 2024-12-20 | 2025-01-24 | 21 | 91.77 | PADU | LONJAKAN | ya | tidak |
| INOD | Technology | 2024-12-13 | 2025-02-26 | 48 | 87.58 | PADU | LONJAKAN | ya | tidak |
| PTLO | Consumer Cyclical | 2024-12-23 | 2025-02-13 | 34 | 83.65 | PADU | BERTANGGA | ya | tidak |
| PLTR | Technology | 2024-12-11 | 2025-02-18 | 44 | 83.08 | PADU | LONJAKAN | ya | tidak |
| AXSM | Healthcare | 2024-12-30 | 2025-02-21 | 35 | 82.31 | PADU | BERTANGGA | ya | tidak |
| ACMR | Technology | 2024-12-02 | 2025-02-26 | 57 | 79.22 | PADU | LONJAKAN | tidak | tidak |
| ALHC | Healthcare | 2024-12-20 | 2025-03-21 | 60 | 72.99 | PADU | LONJAKAN | ya | tidak |
| PGNY | Healthcare | 2024-12-20 | 2025-02-20 | 39 | 71.06 | PADU | STABIL | ya | tidak |
| APP | Communication Services | 2024-12-18 | 2025-02-14 | 38 | 65.56 | PADU | LONJAKAN | ya | tidak |


### Semua run SUPER PADU (≥ 100%)

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|
| GME | Consumer Cyclical | 2024-02-23 | 56 | 271.57 | LONJAKAN | ya | tidak |
| INOD | Technology | 2024-09-06 | 54 | 232.59 | LONJAKAN | tidak | tidak |
| INSM | Healthcare | 2024-04-19 | 59 | 231.41 | LONJAKAN | tidak | tidak |
| LEU | Energy | 2024-08-05 | 63 | 226.86 | BERTANGGA | ya | ya |
| OKLO | Utilities | 2024-11-15 | 55 | 220.47 | BERTANGGA | ya | tidak |
| SEZL | Financial Services | 2024-10-10 | 32 | 201.42 | LONJAKAN | ya | tidak |
| HUT | Financial Services | 2024-04-16 | 62 | 201.15 | BERTANGGA | ya | ya |
| MSTR | Technology | 2024-02-13 | 30 | 192.76 | STABIL | ya | tidak |
| SMR | Industrials | 2024-08-02 | 60 | 175.0 | LONJAKAN | ya | tidak |
| GME | Consumer Cyclical | 2024-05-24 | 8 | 162.99 | LONJAKAN | ya | tidak |
| PLCE | Consumer Cyclical | 2024-06-20 | 61 | 159.31 | LONJAKAN | tidak | ya |
| HROW | Healthcare | 2024-04-25 | 59 | 156.39 | BERTANGGA | tidak | tidak |
| UPST | Financial Services | 2024-09-10 | 43 | 153.76 | LONJAKAN | ya | tidak |
| MSTR | Technology | 2024-08-05 | 60 | 152.18 | STABIL | tidak | tidak |
| XPOF | Consumer Cyclical | 2024-05-10 | 45 | 145.79 | BERTANGGA | tidak | tidak |
| DJT | Communication Services | 2024-04-16 | 17 | 141.2 | BERTANGGA | ya | tidak |
| CDNA | Healthcare | 2024-04-16 | 62 | 136.86 | LONJAKAN | tidak | ya |
| EWTX | Healthcare | 2024-08-05 | 53 | 136.82 | LONJAKAN | ya | tidak |
| NVCR | Healthcare | 2024-10-08 | 47 | 135.78 | LONJAKAN | ya | tidak |
| AMSC | Industrials | 2024-04-10 | 63 | 135.77 | STABIL | tidak | ya |
| WGS | Healthcare | 2024-09-25 | 24 | 134.17 | LONJAKAN | ya | tidak |
| RILY | Financial Services | 2024-02-07 | 56 | 130.43 | LONJAKAN | ya | tidak |
| GL | Financial Services | 2024-04-11 | 19 | 129.76 | STABIL | tidak | tidak |
| ASPN | Basic Materials | 2024-02-09 | 63 | 128.12 | LONJAKAN | ya | ya |
| NRIX | Healthcare | 2024-01-24 | 52 | 127.16 | LONJAKAN | ya | tidak |
| ASAN | Technology | 2024-09-10 | 63 | 125.17 | LONJAKAN | ya | ya |
| BILI | Communication Services | 2024-08-12 | 36 | 123.34 | STABIL | ya | tidak |
| CVNA | Consumer Cyclical | 2024-01-17 | 48 | 123.12 | LONJAKAN | ya | tidak |
| COIN | Financial Services | 2024-01-16 | 48 | 120.45 | STABIL | tidak | tidak |
| EH | Industrials | 2024-11-21 | 58 | 120.14 | STABIL | tidak | tidak |
| DAN | Consumer Cyclical | 2024-10-31 | 60 | 119.79 | BERTANGGA | tidak | tidak |
| RIVN | Consumer Cyclical | 2024-04-16 | 60 | 119.25 | BERTANGGA | tidak | tidak |
| TPL | Energy | 2024-09-12 | 51 | 119.22 | STABIL | ya | tidak |
| LMND | Financial Services | 2024-08-14 | 62 | 118.23 | LONJAKAN | ya | ya |
| UAL | Industrials | 2024-08-05 | 63 | 117.34 | STABIL | tidak | ya |
| BMEA | Healthcare | 2024-06-07 | 55 | 117.17 | STABIL | tidak | tidak |
| AGX | Industrials | 2024-08-05 | 63 | 116.1 | BERTANGGA | ya | ya |
| ACMR | Technology | 2024-02-05 | 18 | 115.99 | LONJAKAN | ya | tidak |
| TMCI | Healthcare | 2024-05-08 | 46 | 115.56 | STABIL | tidak | tidak |
| FWRD | Industrials | 2024-05-09 | 52 | 115.33 | STABIL | tidak | tidak |
| UNFI | Consumer Defensive | 2024-09-11 | 63 | 114.02 | LONJAKAN | ya | ya |
| MARA | Financial Services | 2024-01-19 | 27 | 112.24 | LONJAKAN | tidak | tidak |
| UI | Technology | 2024-08-23 | 56 | 111.82 | BERTANGGA | ya | tidak |
| TPC | Industrials | 2024-08-02 | 55 | 111.45 | BERTANGGA | tidak | tidak |
| AEHR | Technology | 2024-06-26 | 14 | 109.66 | LONJAKAN | ya | tidak |
| DJT | Communication Services | 2024-01-25 | 43 | 107.46 | LONJAKAN | ya | tidak |
| ZLAB | Healthcare | 2024-08-15 | 49 | 106.99 | BERTANGGA | ya | tidak |
| PGY | Technology | 2024-11-19 | 59 | 106.71 | LONJAKAN | ya | tidak |
| NVCR | Healthcare | 2024-04-22 | 20 | 105.56 | STABIL | ya | tidak |
| EH | Industrials | 2024-08-05 | 44 | 104.52 | LONJAKAN | tidak | tidak |
| RUN | Technology | 2024-07-02 | 37 | 103.79 | BERTANGGA | ya | tidak |
| BE | Industrials | 2024-02-23 | 62 | 102.09 | BERTANGGA | ya | ya |
| VST | Utilities | 2024-07-30 | 47 | 101.83 | BERTANGGA | ya | tidak |
| HOOD | Financial Services | 2024-08-05 | 61 | 101.79 | BERTANGGA | ya | ya |
| CRDO | Technology | 2024-04-19 | 59 | 101.13 | BERTANGGA | tidak | tidak |
| AI | Technology | 2024-09-05 | 57 | 100.85 | BERTANGGA | ya | tidak |
| COHR | Technology | 2024-08-05 | 48 | 100.65 | STABIL | ya | tidak |
| NRIX | Healthcare | 2024-04-30 | 50 | 100.17 | BERTANGGA | ya | tidak |


(dipaparkan 60 teratas daripada 58)


### Run BERTANGGA (S2) — 40 teratas

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | bilangan_kaki | pct_hari_atas_ema21 | kumpulan |
|---|---|---|---|---|---|---|---|
| LEU | Energy | 2024-08-05 | 63 | 226.86 | 3 | 66.1 | SUPER PADU |
| OKLO | Utilities | 2024-11-15 | 55 | 220.47 | 4 | 74.5 | SUPER PADU |
| HUT | Financial Services | 2024-04-16 | 62 | 201.15 | 5 | 79.7 | SUPER PADU |
| HROW | Healthcare | 2024-04-25 | 59 | 156.39 | 2 | 81.7 | SUPER PADU |
| XPOF | Consumer Cyclical | 2024-05-10 | 45 | 145.79 | 3 | 60.9 | SUPER PADU |
| DJT | Communication Services | 2024-04-16 | 17 | 141.2 | 2 | 100.0 | SUPER PADU |
| DAN | Consumer Cyclical | 2024-10-31 | 60 | 119.79 | 2 | 62.3 | SUPER PADU |
| RIVN | Consumer Cyclical | 2024-04-16 | 60 | 119.25 | 5 | 70.5 | SUPER PADU |
| AGX | Industrials | 2024-08-05 | 63 | 116.1 | 3 | 91.1 | SUPER PADU |
| UI | Technology | 2024-08-23 | 56 | 111.82 | 2 | 100.0 | SUPER PADU |
| TPC | Industrials | 2024-08-02 | 55 | 111.45 | 2 | 73.2 | SUPER PADU |
| ZLAB | Healthcare | 2024-08-15 | 49 | 106.99 | 2 | 100.0 | SUPER PADU |
| RUN | Technology | 2024-07-02 | 37 | 103.79 | 4 | 100.0 | SUPER PADU |
| BE | Industrials | 2024-02-23 | 62 | 102.09 | 4 | 70.4 | SUPER PADU |
| VST | Utilities | 2024-07-30 | 47 | 101.83 | 2 | 85.4 | SUPER PADU |
| HOOD | Financial Services | 2024-08-05 | 61 | 101.79 | 2 | 86.8 | SUPER PADU |
| CRDO | Technology | 2024-04-19 | 59 | 101.13 | 3 | 70.0 | SUPER PADU |
| AI | Technology | 2024-09-05 | 57 | 100.85 | 3 | 78.4 | SUPER PADU |
| NRIX | Healthcare | 2024-04-30 | 50 | 100.17 | 3 | 91.3 | SUPER PADU |
| AMRC | Industrials | 2024-04-18 | 31 | 99.51 | 2 | 93.1 | PADU |
| ZETA | Technology | 2024-05-01 | 63 | 95.68 | 2 | 85.2 | PADU |
| BMA | Financial Services | 2024-08-05 | 58 | 93.92 | 3 | 83.9 | PADU |
| VITL | Consumer Defensive | 2024-04-09 | 56 | 93.91 | 2 | 100.0 | PADU |
| GDS | Technology | 2024-08-20 | 56 | 91.89 | 3 | 94.6 | PADU |
| MP | Basic Materials | 2024-08-05 | 51 | 89.62 | 2 | 95.5 | PADU |
| CAMT | Technology | 2024-04-22 | 52 | 87.85 | 2 | 98.0 | PADU |
| MNSO | Consumer Cyclical | 2024-10-17 | 53 | 83.98 | 2 | 76.5 | PADU |
| PTLO | Consumer Cyclical | 2024-12-23 | 34 | 83.65 | 2 | 96.3 | PADU |
| AXSM | Healthcare | 2024-12-30 | 35 | 82.31 | 3 | 96.4 | PADU |
| LITE | Technology | 2024-08-05 | 52 | 81.85 | 2 | 91.1 | PADU |
| YOU | Technology | 2024-07-01 | 63 | 80.41 | 2 | 96.7 | PADU |
| SA | Basic Materials | 2024-02-14 | 33 | 78.84 | 2 | 100.0 | PADU |
| S | Technology | 2024-05-31 | 58 | 76.27 | 3 | 61.0 | PADU |
| NCLH | Consumer Cyclical | 2024-08-07 | 63 | 74.8 | 3 | 76.6 | PADU |
| TGTX | Healthcare | 2024-04-30 | 52 | 74.17 | 2 | 84.6 | PADU |
| CEG | Utilities | 2024-02-15 | 62 | 73.68 | 2 | 94.6 | PADU |
| RBLX | Communication Services | 2024-10-29 | 62 | 72.0 | 3 | 91.8 | PADU |
| NBR | Energy | 2024-06-17 | 30 | 71.67 | 2 | 96.3 | PADU |
| PAAS | Basic Materials | 2024-02-13 | 60 | 71.03 | 3 | 80.3 | PADU |
| MDGL | Healthcare | 2024-02-08 | 26 | 67.54 | 4 | 92.0 | PADU |


(daripada 206 run BERTANGGA)


### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)

n peristiwa PADU dalam S2, populasi keputusan (a) = **116** (rujukan: semua peristiwa = 853). < 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat.


Peristiwa sah: **14151** (populasi keputusan 5192).


## 3. Step 2b — kohort "naik dan naik"

Dijejak 374 run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari tarikh_sah.


| Metrik | Nilai |
|---|---|
| % akhirnya melebihi +100% | **22.7%** |
| median %_naik_penuh | **65.3%** |
| median %_naik pada hari ke-63 | 37.3% |
| median hari ke puncak penuh | 152 |
| median MFE 252 selepas kos | 51.5% |
| median MAE 252 | -6.0% |
| median hari pegang Chandelier 4×ATR | 73 |
| median pulangan Chandelier selepas kos | 14.1% |
| terpotong hujung data | 0.0% |


Exit yang menyala dahulu:


| exit | n |
|---|---|
| bawah_ema9 | 126 |
| bawah_ma50 | 119 |
| hist_neg3 | 29 |
| macd_bawah | 26 |
| bawah_ema21 | 25 |
| hari_agihan | 23 |
| rsi_70_60 | 21 |
| trail_2atr | 4 |
| trail_8pct | 1 |


### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari

| kohort | n | median_naik_63 | pct_bertangga | pct_super | median_hari_ke_puncak |
|---|---|---|---|---|---|
| masih_naik = ya | 374 | 37.3 | 15.8 | 2.4 | 63.0 |
| reda dalam 63 hari | 2637 | 22.8 | 4.9 | 1.1 | 21.0 |


Kohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya diketahui pada hari ke-63.


## 4. Step 3 — populasi kuintil dan dedup

POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **7192** baris. Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **31** daripada 41; dibuang 10.


| buang | kerana | rho |
|---|---|---|
| j_ma150 | j_ma200 | 0.963 |
| cerun_ema21 | j_ma50 | 0.805 |
| cerun_ma200 | j_ma200 | 0.845 |
| rsi14 | j_ma50 | 0.807 |
| roc60 | cerun_ma50 | 0.929 |
| willr14 | stoch_k | 1.0 |
| bb_pctb | cci20 | 0.93 |
| kelt_pos | j_ema21 | 0.92 |
| j_52w_rendah | j_ma200 | 0.808 |
| rs_spy_3b | cerun_ma50 | 0.872 |


Signal dibina: **213** (31 binari + 62 hujung kuintil + 120 pemicu × 1 konteks).


## 5. Step 4 — common & unique (ENTRY)

Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. N ujian ENTRY sebenar (populasi a, kumpulan A) = **852** baris (213 signal × 2 subset × 2 keluarga).


### Kelas (S2, kumpulan A, keluarga PADU)

| kelas | n |
|---|---|
| TIDAK BERGUNA | 193 |
| COMMON BIASA | 7 |
| SEDERHANA | 6 |
| UNIQUE | 5 |
| LANGKA | 2 |


### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)

| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n | n_industri | n_minggu | purata_pct_naik_rendah | purata_hari_ke_puncak | pct_bertangga | pct_lonjakan | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | UNIQUE | 26.98 | 0.0 | 1.78 | 1.11 | 15.148 | 24.339 | 39.58 | 10.044 | 48 | 25 | 26 | 62.49 | 49.7 | 100.0 | 0.0 |  |
| q5:atr_pct | UNIQUE | 44.44 | 0.0 | 3.81 | 19.66 | 11.67 | 2.261 | 34.04 | 8.638 | 94 | 38 | 37 | 63.76 | 50.4 | 100.0 | 0.0 |  |
| q5:julat20 | UNIQUE | 44.44 | 0.0 | 4.55 | 27.22 | 9.778 | 1.633 | 30.19 | 7.66 | 106 | 52 | 34 | 62.72 | 51.5 | 100.0 | 0.0 |  |
| pocket_pivot&q5:atr_pct | LANGKA | 11.11 | 0.0 | 1.29 | 1.27 | 8.614 | 8.769 | 30.0 | 7.612 | 30 | 21 | 21 | 80.02 | 57.3 | 100.0 | 0.0 |  |
| ema_crossback&q5:bb_lebar | LANGKA | 9.52 | 0.0 | 1.29 | 0.34 | 7.383 | 28.297 | 30.0 | 7.612 | 30 | 21 | 20 | 73.75 | 52.2 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:julat20 | UNIQUE | 25.4 | 0.0 | 2.64 | 0.87 | 9.615 | 29.154 | 29.51 | 7.487 | 61 | 39 | 25 | 61.38 | 51.0 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:rs_spy_6b | UNIQUE | 19.05 | 0.0 | 5.77 | 0.65 | 3.299 | 29.154 | 12.15 | 3.083 | 107 | 58 | 31 | 52.51 | 52.5 | 100.0 | 0.0 |  |


### Rujukan S1 (semua run layak)

_(tiada baris)_


### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja

S3 mengandungi 1889 run; ia **bukan keluarga carian** (tidak menambah N). 7.6% daripadanya BERTANGGA lawan 6.3% keseluruhan.


### Keluarga SUPER PADU (FDR sendiri)

| signal | kelas | K_super | lift | lift_rawak | n | tanda |
|---|---|---|---|---|---|---|
| ema_crossback&q5:atr_pct | TERAS | 75.0 | 101.75 | 164.707 | 24 |  |
| pocket_pivot&q5:julat20 | TERAS | 50.0 | 67.833 | 22.35 | 19 | SAMPEL KECIL |
| ema_crossback&q5:julat20 | TERAS | 75.0 | 64.263 | 189.412 | 28 |  |
| ema_crossback&q5:bb_lebar | TERAS | 75.0 | 58.143 | 222.838 | 30 |  |
| pocket_pivot&q5:bb_lebar | TERAS | 50.0 | 47.882 | 20.044 | 25 |  |
| pocket_pivot&q5:atr_pct | TERAS | 50.0 | 38.762 | 39.461 | 30 |  |
| ema_crossback&q1:j_ma200 | UNIQUE | 25.0 | 29.071 | 140.306 | 18 | SAMPEL KECIL |
| rsi_lintas50&q5:atr_pct | TERAS | 50.0 | 28.069 | 45.098 | 48 |  |
| q5:atr_pct | TERAS | 100.0 | 26.258 | 5.087 | 94 |  |
| ema_crossback&q5:cerun_ma50 | TERAS | 50.0 | 26.258 | 43.543 | 33 |  |
| ema_crossback&q1:rs_spy_6b | UNIQUE | 25.0 | 23.941 | 84.183 | 20 |  |
| macd_cross&q5:julat20 | UNIQUE | 25.0 | 23.941 | 31.569 | 22 |  |
| q5:julat20 | TERAS | 100.0 | 22.0 | 3.673 | 106 |  |
| rsi_lintas50&q5:cerun_ma50 | UNIQUE | 25.0 | 20.35 | 28.699 | 21 |  |
| macd_cross&q5:atr_pct | UNIQUE | 25.0 | 20.35 | 46.769 | 28 |  |
| rsi_lintas50&q5:julat20 | TERAS | 50.0 | 18.93 | 57.398 | 61 |  |
| pocket_pivot&q1:j_ma200 | TERAS | 50.0 | 10.853 | 57.398 | 82 |  |
| macd_cross&q1:j_52w_tinggi | UNIQUE | 25.0 | 9.25 | 36.079 | 46 |  |
| ema_crossback&q1:vol_n50 | UNIQUE | 25.0 | 7.98 | 30.799 | 58 |  |
| ema_crossback&q1:lapis | UNIQUE | 25.0 | 7.14 | 90.196 | 64 |  |


### PEMICU YANG TIDAK MEMBEZAKAN

Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.


| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n |
|---|---|---|---|---|---|---|---|---|---|---|
| b:donchian20 | TIDAK BERGUNA | 1.59 | 0.0 | 14.0 | 6.87 | 0.113 | 0.231 | 0.44 | 0.111 | 229 |
| b:ema_crossback | TIDAK BERGUNA | 31.75 | 20.0 | 20.76 | 3.58 | 1.529 | 8.859 | 6.35 | 1.612 | 362 |
| b:gap_and_go | TIDAK BERGUNA | 11.11 | 0.0 | 2.58 | 0.57 | 4.307 | 19.352 | 14.29 | 3.625 | 49 |
| b:macd_cross | TIDAK BERGUNA | 23.81 | 20.0 | 22.54 | 4.02 | 1.056 | 5.924 | 4.17 | 1.057 | 384 |
| b:pocket_pivot | TIDAK BERGUNA | 20.63 | 20.0 | 27.58 | 9.42 | 0.748 | 2.19 | 3.23 | 0.818 | 465 |
| b:rsi_lintas50 | COMMON BIASA | 71.43 | 100.0 | 39.62 | 5.64 | 0.714 | 12.659 | 6.74 | 1.711 | 697 |


**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis yang diuji dalam kajian ini, dan ia disokong oleh data 2025.


### Corong ke Step 7
18 signal diteruskan (had 30; layak sebelum had: 18).


## 6. Step 5 — HOLD

> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana berjaya. Semua CALON.


### Kelas pullback

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| AMARAN | 4489 | 47.2 | -16.56 | 11.4 |
| PULLBACK PASARAN | 408 | 82.6 | -9.03 | 10.4 |
| PULLBACK SIHAT | 1034 | 88.4 | -8.12 | 6.8 |


Pullback yang trend sahamnya utuh (SIHAT 88.4%, PASARAN 82.6%) menyambung ke puncak baru jauh lebih kerap daripada pullback AMARAN (47.2%). Ini sokongan paling jelas bagi falsafah "pegang selagi naik".


### Grid 18 peraturan HOLD (deskriptif)

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| X=5%,Y=ema9 | 4 | 100.0 | -5.0 | 5.8 |
| X=5%,Y=ema21 | 1477 | 92.0 | -7.26 | 6.5 |
| X=5%,Y=ma50 | 2207 | 87.7 | -8.47 | 8.3 |
| X=7%,Y=ema9 | 1180 | 92.5 | -5.91 | 5.6 |
| X=7%,Y=ema21 | 1774 | 91.9 | -7.07 | 6.5 |
| X=7%,Y=ma50 | 2421 | 88.6 | -8.25 | 8.0 |
| X=10%,Y=ema9 | 2345 | 89.0 | -7.15 | 7.3 |
| X=10%,Y=ema21 | 2493 | 89.0 | -7.52 | 7.5 |
| X=10%,Y=ma50 | 2842 | 87.6 | -8.3 | 8.3 |
| X=12%,Y=ema9 | 2878 | 86.8 | -7.86 | 8.2 |
| X=12%,Y=ema21 | 2951 | 86.7 | -8.06 | 8.2 |
| X=12%,Y=ma50 | 3156 | 85.7 | -8.57 | 8.6 |
| X=15%,Y=ema9 | 3589 | 81.7 | -8.97 | 9.1 |
| X=15%,Y=ema21 | 3614 | 81.6 | -9.05 | 9.2 |
| X=15%,Y=ma50 | 3693 | 81.0 | -9.29 | 9.2 |
| X=20%,Y=ema9 | 4383 | 73.4 | -10.47 | 9.8 |
| X=20%,Y=ema21 | 4396 | 73.4 | -10.52 | 9.8 |
| X=20%,Y=ma50 | 4426 | 73.0 | -10.62 | 9.8 |


### Common/unique HOLD (lulus FDR)

0 / 18 signal HOLD lulus BH-FDR q ≤ 0.01: 


| nama | subset | n | K_padu | K_gagal | lift | presisi | lift_presisi | kelas |
|---|---|---|---|---|---|---|---|---|
| b:atas_ema21 | S1 | 769 | 21.47 | 1.79 | 11.961 | 94.02 | 1.656 | UNIQUE |
| b:psar_naik | S1 | 901 | 24.58 | 2.85 | 8.631 | 91.9 | 1.618 | UNIQUE |
| b:supertrend_naik | S1 | 1819 | 49.17 | 6.36 | 7.731 | 91.04 | 1.603 | UNIQUE |
| b:vcp | S1 | 179 | 4.75 | 0.74 | 6.408 | 89.39 | 1.574 | LANGKA |
| b:atas_ma50 | S1 | 1800 | 47.18 | 8.23 | 5.731 | 88.28 | 1.555 | UNIQUE |
| b:tenkan_atas | S1 | 2191 | 56.74 | 10.92 | 5.194 | 87.22 | 1.536 | TERAS |
| b:bb_squeeze | S1 | 29 | 0.74 | 0.16 | 4.756 | 86.21 | 1.518 | TIDAK BERGUNA |
| b:atas_awan | S1 | 1887 | 47.92 | 10.65 | 4.499 | 85.53 | 1.506 | UNIQUE |
| b:macd_atas0 | S1 | 2394 | 60.72 | 13.62 | 4.459 | 85.42 | 1.504 | TERAS |
| b:pullback_dalam_7pct | S1 | 3459 | 82.3 | 26.8 | 3.071 | 80.14 | 1.411 | TERAS |
| b:garis_rs_tinggi | S2 | 1 | 0.18 | 0.0 | 1.307 | 100.0 | 1.307 | TIDAK BERGUNA |
| b:bb_squeeze | S2 | 5 | 0.9 | 0.0 | 6.535 | 100.0 | 1.307 | TIDAK BERGUNA |
| b:atas_ema21 | S2 | 177 | 31.06 | 2.34 | 13.278 | 97.74 | 1.277 | UNIQUE |
| b:supertrend_naik | S2 | 395 | 68.4 | 8.19 | 8.355 | 96.46 | 1.261 | TERAS |
| b:psar_naik | S2 | 165 | 28.19 | 4.68 | 6.025 | 95.15 | 1.244 | UNIQUE |
| b:tenkan_atas | S2 | 433 | 73.79 | 12.87 | 5.735 | 94.92 | 1.241 | TERAS |
| b:atas_ma50 | S2 | 378 | 64.45 | 11.11 | 5.801 | 94.97 | 1.241 | TERAS |
| b:macd_atas0 | S2 | 469 | 78.82 | 17.54 | 4.492 | 93.6 | 1.223 | TERAS |
| b:sektor_atas_ma50 | S1 | 1973 | 40.59 | 23.64 | 1.717 | 69.29 | 1.22 | TIDAK BERGUNA |
| b:sektor_naik | S1 | 1973 | 40.59 | 23.64 | 1.717 | 69.29 | 1.22 | TIDAK BERGUNA |


## 7. Step 6 — EXIT (semua CALON)

> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.


| nama | n | pct_menyala | median_hari_dari_puncak | median_pulangan_exit | median_pct_kekal | kadar_exit_palsu |
|---|---|---|---|---|---|---|
| atr_lonjak_15x | 1119 | 38.3 | 14.0 | -3.12 | -16.2 | 47.0 |
| bawah_ema21 | 2919 | 100.0 | -11.0 | -0.83 | -3.9 | 57.9 |
| bawah_ema9 | 2920 | 100.0 | -15.0 | -0.18 | 0.3 | 59.4 |
| bawah_ma50 | 2881 | 98.7 | -7.0 | -0.79 | -4.1 | 55.8 |
| chandelier_4atr | 2646 | 90.6 | 14.0 | -2.55 | -16.4 | 44.2 |
| climax_25_15h | 747 | 25.6 | -7.0 | 19.48 | 71.3 | 55.6 |
| div_macd | 2626 | 89.9 | -12.0 | 4.43 | 32.1 | 50.1 |
| div_rsi | 2345 | 80.3 | -11.0 | 5.96 | 42.3 | 49.9 |
| gap_besar | 374 | 12.8 | -4.0 | 24.99 | 81.0 | 51.3 |
| hari_agihan | 2481 | 85.0 | 5.0 | 0.9 | 8.6 | 44.9 |
| hist_neg3 | 2897 | 99.2 | -8.0 | 0.37 | 4.4 | 54.5 |
| jauh_ma50_2x | 1329 | 45.5 | -12.0 | 10.03 | 61.2 | 49.7 |
| macd_bawah | 2910 | 99.7 | -5.0 | 0.94 | 9.3 | 53.1 |
| pullback_amaran | 2860 | 97.9 | 18.0 | -6.52 | -40.0 | 68.9 |
| rsi_70_60 | 2092 | 71.6 | 1.0 | 6.67 | 42.8 | 51.1 |
| trail_10pct | 2678 | 91.7 | 9.0 | -2.73 | -13.3 | 48.7 |
| trail_15pct | 2071 | 70.9 | 18.0 | -7.28 | -45.1 | 46.4 |
| trail_2atr | 2919 | 100.0 | 2.0 | 0.14 | 3.6 | 52.4 |
| trail_3atr | 2874 | 98.4 | 8.0 | -0.99 | -3.3 | 47.1 |
| trail_8pct | 2831 | 97.0 | 5.0 | -1.52 | -5.9 | 49.9 |


`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala 7–15 hari sebelum puncak dan mengekalkan hanya 0% hingga -4% keuntungan. Kadar exit palsu 44%–69%.


**Keluarga EXIT: 0 / 62 signal lulus BH-FDR q ≤ 0.01.** Tiada signal EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas kawalan pelbagai ujian.


## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)

Setiap signal corong diimbas atas **semua** hari universe 2024 (570,377 baris (ticker, hari); 503,999 selepas topeng universe). Kadar asas KAWALAN RAWAK (MFE63 ≥ 30%) = 11.91%.


| signal | n_kemunculan | kadar_tepat_mfe30 | lift_tepat | kadar_palsu_bawah10 | kadar_tepat_bertangga | ketulenan_trend_median | mfe63_p50 | mfe63_p75 | mfe63_p90 | pct_mfe63_ge30 | pct_mfe63_ge100 | mfe252_p90 | pct_mfe252_ge100 | median_hari_mfe63 | jangkaan_henti2atr | kadar_menang | kapasiti | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | 4924 | 27.46 | 2.305 | 35.72 | 2.34 | 74.6 | 15.87 | 32.17 | 56.06 | 27.46 | 2.32 | 136.35 | 17.1 | 30.0 | 0.02 | 29.29 | TULANG BELAKANG |  |
| q5:atr_pct | 94579 | 27.08 | 2.274 | 35.56 | 2.35 | 61.1 | 16.06 | 31.77 | 54.4 | 27.08 | 2.37 | 140.08 | 17.4 | 30.0 | 0.189 | 31.2 | TULANG BELAKANG |  |
| q5:julat20 | 134813 | 21.32 | 1.79 | 39.68 | 1.93 | 65.6 | 13.76 | 26.88 | 46.42 | 21.32 | 1.67 | 117.05 | 13.22 | 33.0 | 0.382 | 32.08 | TULANG BELAKANG |  |
| ema_crossback&q5:bb_lebar | 2593 | 23.45 | 1.969 | 36.64 | 2.24 | 74.6 | 14.95 | 28.87 | 50.22 | 23.45 | 2.39 | 126.03 | 14.77 | 34.0 | 0.746 | 32.51 | TULANG BELAKANG |  |
| pocket_pivot&q5:atr_pct | 6296 | 28.22 | 2.37 | 37.37 | 2.38 | 86.8 | 15.81 | 33.19 | 57.6 | 28.22 | 3.29 | 151.62 | 18.73 | 27.0 | -0.679 | 26.29 | PELENGKAP |  |
| rsi_lintas50&q5:julat20 | 4720 | 24.98 | 2.097 | 36.55 | 2.12 | 73.9 | 15.27 | 29.99 | 53.16 | 24.98 | 2.22 | 128.09 | 15.19 | 35.0 | 0.562 | 31.1 | TULANG BELAKANG |  |
| q5:julat10 | 106429 | 22.09 | 1.855 | 38.43 | 2.12 | 66.1 | 14.19 | 27.52 | 47.88 | 22.09 | 1.86 | 121.46 | 13.93 | 32.0 | 0.623 | 33.45 | TULANG BELAKANG |  |
| rsi_lintas50&q5:bb_lebar | 4340 | 23.96 | 2.012 | 37.6 | 1.89 | 75.0 | 14.7 | 28.9 | 50.38 | 23.96 | 2.17 | 123.39 | 14.24 | 34.0 | 0.403 | 30.69 | TULANG BELAKANG |  |
| q5:bb_lebar | 142551 | 19.05 | 1.6 | 41.82 | 1.76 | 68.4 | 12.83 | 25.08 | 43.35 | 19.05 | 1.47 | 109.26 | 11.66 | 33.0 | 0.187 | 31.51 | TULANG BELAKANG |  |
| q5:j_ema9 | 43812 | 17.05 | 1.432 | 44.86 | 1.65 | 90.0 | 11.72 | 23.19 | 40.87 | 17.05 | 1.43 | 105.06 | 10.79 | 34.0 | -0.274 | 28.94 | PELENGKAP | BUNYI LATAR |
| gap_and_go&q5:vol_n50 | 2363 | 14.09 | 1.183 | 47.74 | 1.57 | 92.3 | 10.72 | 20.69 | 37.32 | 14.09 | 1.1 | 93.87 | 8.97 | 30.0 | 0.12 | 32.04 | TULANG BELAKANG |  |
| b:gap_and_go | 2363 | 14.09 | 1.183 | 47.74 | 1.57 | 92.3 | 10.72 | 20.69 | 37.32 | 14.09 | 1.1 | 93.87 | 8.97 | 30.0 | 0.12 | 32.04 | TULANG BELAKANG |  |
| rsi_lintas50&q1:j_52w_tinggi | 5182 | 19.36 | 1.625 | 41.9 | 1.6 | 74.6 | 12.57 | 25.12 | 42.97 | 19.36 | 1.1 | 102.43 | 10.52 | 29.0 | -1.333 | 26.9 | PELENGKAP |  |
| rsi_lintas50&q5:j_ma200 | 3754 | 19.21 | 1.613 | 37.96 | 2.37 | 74.2 | 13.89 | 25.89 | 42.08 | 19.21 | 1.62 | 115.6 | 13.27 | 36.0 | 1.152 | 32.9 | TULANG BELAKANG |  |
| q1:roc20 | 144952 | 14.46 | 1.214 | 43.46 | 1.51 | 53.6 | 11.95 | 22.02 | 35.7 | 14.46 | 0.76 | 86.83 | 7.6 | 34.0 | 1.166 | 36.13 | TULANG BELAKANG | BUNYI LATAR |
| q1:j_52w_tinggi | 101276 | 19.67 | 1.651 | 40.55 | 1.61 | 57.4 | 13.26 | 25.65 | 43.6 | 19.67 | 1.23 | 105.81 | 11.09 | 30.0 | -0.417 | 30.66 | PELENGKAP |  |
| rsi_lintas50&q5:rs_spy_6b | 4226 | 19.29 | 1.619 | 38.26 | 2.32 | 74.1 | 13.91 | 26.05 | 41.47 | 19.29 | 1.42 | 110.67 | 12.38 | 37.0 | 1.548 | 33.53 | TULANG BELAKANG |  |
| ema_crossback&q1:vol_n50 | 5347 | 12.53 | 1.052 | 43.44 | 1.46 | 75.0 | 11.81 | 21.12 | 32.89 | 12.53 | 0.64 | 78.25 | 5.97 | 35.0 | 1.552 | 35.25 | TULANG BELAKANG | BUNYI LATAR |


Taburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. p90 dan % ≥ 100% ialah pembeza, bukan median.


**Lift jatuh besar antara Step 4 dan Step 7** (contoh `rsi_lintas50&q5:atr_pct`: lift 15.15 dalam populasi peristiwa → lift_tepat 2.31 atas semua hari universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. Angka Step 7 yang lebih dekat dengan dagangan sebenar.


### Penapis Step 7.4
144 kombinasi signal × penapis diuji (0 lulus kriteria "buang ≥ 30% palsu dan ≤ 10% benar").


**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis dipradaftar. Ini keputusan negatif yang bersih.


10 contoh penapis terbaik (ikut % palsu dibuang):


| signal | buang_palsu_pct | buang_benar_pct |
|---|---|---|
| ema_crossback&q1:vol_n50 | penapis:vol_n50_ge_1.5 | 100.0 | 100.0 |
| rsi_lintas50&q1:j_52w_tinggi | penapis:lapis_ge_3 | 93.1 | 91.2 |
| q1:j_52w_tinggi | penapis:lapis_ge_3 | 92.1 | 90.0 |
| q1:roc20 | penapis:harga_atas_ma50 | 89.2 | 87.7 |
| q1:j_52w_tinggi | penapis:vol_n50_ge_1.5 | 87.6 | 88.1 |
| q1:roc20 | penapis:vol_n50_ge_1.5 | 86.2 | 88.1 |
| q5:bb_lebar | penapis:vol_n50_ge_1.5 | 85.2 | 85.8 |
| ema_crossback&q5:bb_lebar | penapis:vol_n50_ge_1.5 | 85.2 | 83.6 |
| rsi_lintas50&q1:j_52w_tinggi | penapis:vol_n50_ge_1.5 | 85.1 | 82.9 |
| rsi_lintas50&q5:rs_spy_6b | penapis:vol_n50_ge_1.5 | 84.3 | 87.2 |


## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)

Set kemasukan: gabungan semua kemunculan 15 signal yang lulus Step 7 = 220,238 (ticker, tarikh) unik, disampel berlapis ikut bulan ke **24,000** (benih 42; SPEC §13.9). Grid 18 HOLD × 13 EXIT = **234** sistem.


### TIGA RUJUKAN WAJIB

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_menang | purata_kalah | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 | pct_terpotong_data | siri_kalah_terpanjang |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 24000 | -2.01 | 8.68 | 8.677 | 47.97 | 50.11 | 29.52 | 252.0 | -27.56 | 0.0 | 100.0 | 0.0 | 18 |
| REF_jual_hari63 | 24000 | -0.54 | 1.34 | 1.34 | 48.9 | 20.32 | 16.83 | 63.0 | -11.41 | 74.8 | 0.0 | 0.0 | 21 |
| REF_chandelier_4atr | 24000 | -5.44 | -0.02 | -0.022 | 35.68 | 21.87 | 12.16 | 52.3 | -8.56 | 75.9 | 0.1 | 0.0 | 30 |


**Keputusan: rujukan "pegang tanpa jual hingga hari ke-252" menang, dan 0 / 234 sistem mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = 8.677%). Mengikut arahan Step 7b.4, jawapan kajian ialah **"jangan jual"** — dan itu dilaporkan sebagai penemuan, bukan kegagalan.


### 15 sistem terbaik daripada 234

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 |
|---|---|---|---|---|---|---|---|---|---|
| hari_agihan|X=5%,Y=ema9 | 24000 | -2.87 | 1.74 | 1.739 | 41.06 | 54.4 | -8.23 | 74.2 | 0.8 |
| hari_agihan|X=5%,Y=ma50 | 24000 | -3.14 | 1.68 | 1.678 | 40.56 | 56.8 | -8.43 | 74.0 | 1.1 |
| hari_agihan|X=5%,Y=ema21 | 24000 | -3.08 | 1.67 | 1.668 | 40.58 | 55.9 | -8.35 | 73.9 | 1.0 |
| hari_agihan|X=7%,Y=ema9 | 24000 | -2.93 | 1.67 | 1.667 | 40.83 | 55.2 | -8.27 | 74.0 | 0.9 |
| hari_agihan|X=10%,Y=ema9 | 24000 | -3.0 | 1.6 | 1.601 | 40.63 | 55.7 | -8.28 | 73.9 | 0.9 |
| hari_agihan|X=12%,Y=ema9 | 24000 | -3.02 | 1.59 | 1.593 | 40.55 | 55.9 | -8.29 | 73.8 | 0.9 |
| hari_agihan|X=7%,Y=ema21 | 24000 | -3.2 | 1.58 | 1.582 | 40.11 | 57.6 | -8.43 | 73.6 | 1.2 |
| hari_agihan|X=7%,Y=ma50 | 24000 | -3.34 | 1.56 | 1.563 | 39.98 | 59.5 | -8.58 | 73.6 | 1.3 |
| hari_agihan|X=15%,Y=ema9 | 24000 | -3.02 | 1.56 | 1.559 | 40.54 | 56.0 | -8.29 | 73.8 | 0.9 |
| hari_agihan|X=20%,Y=ema21 | 24000 | -3.37 | 1.53 | 1.528 | 39.5 | 59.6 | -8.48 | 73.2 | 1.3 |
| hari_agihan|X=15%,Y=ema21 | 24000 | -3.35 | 1.53 | 1.528 | 39.55 | 59.3 | -8.48 | 73.3 | 1.2 |
| hari_agihan|X=12%,Y=ema21 | 24000 | -3.34 | 1.51 | 1.511 | 39.59 | 58.9 | -8.47 | 73.4 | 1.2 |
| hari_agihan|X=20%,Y=ema9 | 24000 | -3.04 | 1.51 | 1.509 | 40.48 | 56.2 | -8.29 | 73.7 | 1.0 |
| rsi_70_60|X=20%,Y=ma50 | 24000 | -0.17 | 1.5 | 1.501 | 49.51 | 99.9 | -10.34 | 64.0 | 12.1 |
| hari_agihan|X=10%,Y=ema21 | 24000 | -3.32 | 1.46 | 1.46 | 39.7 | 58.5 | -8.47 | 73.5 | 1.2 |


Perhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.


## 10. Step 8 — kawalan kebetulan

### Ujian label rawak dan FDR per keluarga

| keluarga | N | lulus_fdr | ambang_p |
|---|---|---|---|
| ENTRY/PADU | 18 | 12 | 0.004995004995004995 |
| ENTRY/SUPER PADU | 18 | 6 | 0.000999000999000999 |
| HOLD | 18 | 0 |  |
| EXIT | 62 | 0 |  |
| SISTEM | 234 | 0 |  |


Perbandingan yang diminta arahan: **12 signal lulus FDR daripada 18 diuji**, manakala label rawak menghasilkan lift purata yang jauh lebih rendah (lajur `lift_purata_rawak` dalam `kawalan_rawak_bootstrap_2024.csv`).


### Jangkaan atas SEMUA kemunculan + ujian outlier

| signal | n_kemunculan | median_pulangan | jangkaan | jangkaan_tanpa_5pct_teratas | pct_rugi_lebih_10 | siri_kalah_terpanjang | jangkaan_bawah95_blok_ticker | jangkaan_bawah95_blok_minggu |
|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | 4924 | -10.14 | 0.02 | -4.356 | 51.2 | 56 | -0.979 | -2.051 |
| q5:atr_pct | 94579 | -10.09 | 0.189 | -4.232 | 50.7 | 214 | -0.597 | -1.472 |
| q5:julat20 | 134813 | -7.94 | 0.382 | -3.496 | 36.2 | 231 | -0.189 | -0.986 |
| ema_crossback&q5:bb_lebar | 2593 | -8.19 | 0.746 | -3.459 | 39.4 | 23 | -0.487 | -1.321 |
| pocket_pivot&q5:atr_pct | 6296 | -10.46 | -0.679 | -5.46 | 54.3 | 72 | -2.044 | -2.462 |
| rsi_lintas50&q5:julat20 | 4720 | -8.99 | 0.562 | -3.703 | 42.7 | 36 | -0.362 | -1.654 |
| q5:julat10 | 106429 | -8.11 | 0.623 | -3.374 | 38.5 | 204 | 0.052 | -1.03 |
| rsi_lintas50&q5:bb_lebar | 4340 | -8.57 | 0.403 | -3.857 | 40.9 | 38 | -0.594 | -1.724 |
| q5:bb_lebar | 142551 | -7.21 | 0.187 | -3.508 | 32.2 | 235 | -0.298 | -1.062 |
| q5:j_ema9 | 43812 | -6.8 | -0.274 | -3.75 | 27.5 | 121 | -0.917 | -1.385 |
| gap_and_go&q5:vol_n50 | 2363 | -6.13 | 0.12 | -2.958 | 22.1 | 22 | -0.604 | -1.044 |
| b:gap_and_go | 2363 | -6.13 | 0.12 | -2.958 | 22.1 | 22 | -0.604 | -1.044 |
| rsi_lintas50&q1:j_52w_tinggi | 5182 | -7.93 | -1.333 | -4.777 | 34.0 | 42 | -2.11 | -2.408 |
| rsi_lintas50&q5:j_ma200 | 3754 | -6.6 | 1.152 | -2.644 | 28.6 | 37 | 0.193 | -0.55 |
| q1:roc20 | 144952 | -5.45 | 1.166 | -1.778 | 21.5 | 176 | 0.834 | 0.086 |
| q1:j_52w_tinggi | 101276 | -7.68 | -0.417 | -4.041 | 34.5 | 301 | -1.043 | -1.49 |
| rsi_lintas50&q5:rs_spy_6b | 4226 | -6.39 | 1.548 | -2.045 | 26.5 | 30 | 0.637 | -0.434 |
| ema_crossback&q1:vol_n50 | 5347 | -4.79 | 1.552 | -1.097 | 14.9 | 24 | 1.038 | 0.352 |


### Keputusan gate demi gate

| signal | G1_sah_dalam_tahun | G2_merentas_tahun | G3_nilai_p | G3_fdr | G4_bootstrap | G5_outlier | G6 | step7 | keputusan |
|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=LANGKA; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:atr_pct | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:julat20 | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=LANGKA; 2021=UNIQUE; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q5:atr_pct | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:julat20 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:julat10 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini SEDERHANA, bukan penemuan; 2020=-; 2021=-; 2022=-; 2023=TIDAK BERGUNA; 2025=-) | 0.0989 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | STATISTIK SAHAJA | LULUS | DITOLAK |
| rsi_lintas50&q5:bb_lebar | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2025=UNIQUE) | 0.54046 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:bb_lebar | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini SEDERHANA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2025=TERAS) | 0.08392 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:j_ema9 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2025=UNIQUE) | 0.005 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| gap_and_go&q5:vol_n50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| b:gap_and_go | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=UNIQUE; 2023=UNIQUE; 2025=UNIQUE) | 0.82717 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:j_ma200 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:roc20 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini SEDERHANA, bukan penemuan; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=SEDERHANA; 2023=TIDAK BERGUNA; 2025=UNIQUE) | 0.003 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q1:j_52w_tinggi | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2025=UNIQUE) | 0.69031 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:rs_spy_6b | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.002 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| ema_crossback&q1:vol_n50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.02498 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |


**DITERIMA: 0** · **CALON: 0** · **DITOLAK: 18.**


Tiada CALON. Gate yang membunuh semua signal ialah **G4 (bootstrap)** dan **G5 (outlier)**: jangkaan tidak bertahan pada had bawah 95% blok ticker atau blok minggu, dan jatuh ke ≤ 0 apabila 5% pemenang teratas dibuang. Maknanya pulangan signal tahun ini datang daripada beberapa kemunculan melampau, bukan daripada kelebihan yang boleh diulang.


Penapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam ≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada 2024.


## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)

Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. Asas signal ENTRY: **lulus Step 7 sahaja (TIADA signal CALON tahun ini)**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → RS 6 bulan → ticker.


> Angka di bawah **bukan** bukti sistem lulus — tiada signal ENTRY tahun ini lulus Step 8. Ia dilaporkan supaya kriteria akhir ada angka dan baris merentas tahun setara (SPEC §13.10).


| sistem | n_posisi_dibuka | n_dagangan_ditutup | n_posisi_terbuka_hujung_tahun | purata_slot_terisi | pulangan_tahun | median_bulanan | purata_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terbaik | bulan_terburuk | mdd | purata_hari_pegang | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 8 | 0 | 8 | 7.94 | -0.43 | -2.02 | 1.61 | 25.0 | 41.7 | 58.77 | -24.73 | -25.26 |  | 0.7 | 25.59 | -8.41 |
| REF_chandelier_4atr | 41 | 33 | 8 | 7.81 | -46.69 | -5.98 | -4.85 | 0.0 | 25.0 | 9.6 | -14.33 | -50.33 | 49.3 | 3.4 | 25.59 | -8.41 |
| REF_jual_hari63 | 40 | 32 | 8 | 7.81 | -30.42 | -3.11 | -2.6 | 16.7 | 33.3 | 13.68 | -15.94 | -41.61 | 63.0 | 3.3 | 25.59 | -8.41 |
| hari_agihan|X=5%,Y=ema9 | 46 | 38 | 8 | 7.79 | 10.98 | 2.34 | 1.3 | 16.7 | 66.7 | 17.48 | -11.68 | -29.4 | 46.0 | 3.8 | 25.59 | -8.41 |
| hari_agihan|X=5%,Y=ma50 | 48 | 40 | 8 | 7.78 | 0.29 | 1.69 | 0.46 | 16.7 | 58.3 | 15.29 | -14.12 | -31.55 | 44.0 | 4.0 | 25.59 | -8.41 |
| hari_agihan|X=5%,Y=ema21 | 46 | 38 | 8 | 7.79 | 9.29 | 2.01 | 1.15 | 25.0 | 66.7 | 14.73 | -11.46 | -28.32 | 46.6 | 3.8 | 25.59 | -8.41 |
| KAWALAN_RAWAK|pegang_252 | 8 | 0 | 8 | 7.94 | 20.48 | 1.85 | 1.7 | 8.3 | 83.3 | 10.3 | -10.34 | -10.36 |  | 0.7 | 25.59 | -8.41 |
| KAWALAN_RAWAK|chandelier | 44 | 36 | 8 | 7.79 | 14.65 | 1.2 | 1.34 | 8.3 | 50.0 | 11.75 | -8.17 | -13.84 | 44.3 | 3.7 | 25.59 | -8.41 |


### Pulangan bulanan penuh (%)

| tarikh | REF_pegang_252 | REF_chandelier_4atr | REF_jual_hari63 | hari_agihan|X=5%,Y=ema9 | hari_agihan|X=5%,Y=ma50 | hari_agihan|X=5%,Y=ema21 | KAWALAN_RAWAK|pegang_252 | KAWALAN_RAWAK|chandelier |
|---|---|---|---|---|---|---|---|---|
| 2024-01-31 | -14.28 | -12.47 | -14.28 | -11.68 | -11.46 | -11.46 | 0.05 | -1.07 |
| 2024-02-29 | 11.11 | 6.22 | 11.11 | 17.48 | 14.73 | 14.73 | 3.38 | 3.46 |
| 2024-03-31 | -6.26 | -4.03 | -6.26 | -11.22 | -14.12 | -11.41 | 5.25 | 5.83 |
| 2024-04-30 | 0.39 | -14.33 | -8.59 | -6.43 | -7.04 | -6.1 | -10.34 | -6.11 |
| 2024-05-31 | -1.16 | -8.68 | 3.02 | 1.08 | -0.12 | 1.18 | 6.44 | 6.09 |
| 2024-06-30 | -2.88 | -8.32 | -2.25 | 0.5 | 1.9 | 0.63 | -4.43 | -8.17 |
| 2024-07-31 | 10.18 | 9.6 | -0.26 | 14.54 | 15.29 | 14.59 | 10.3 | 9.34 |
| 2024-08-31 | -12.6 | 1.44 | -15.94 | 4.33 | 1.53 | 3.85 | 2.55 | -5.89 |
| 2024-09-30 | -4.84 | -12.27 | 0.54 | -10.19 | -10.33 | -10.35 | 0.63 | 6.25 |
| 2024-10-31 | 5.67 | -6.36 | -3.97 | 4.07 | 3.8 | 3.92 | 1.15 | -3.24 |
| 2024-11-30 | 58.77 | -5.6 | 13.68 | 3.61 | 1.86 | 2.85 | 4.8 | 11.75 |
| 2024-12-31 | -24.73 | -3.39 | -8.0 | 9.53 | 9.48 | 11.41 | 0.56 | -2.11 |


### Jawapan terus kepada sasaran +10% sebulan

**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:


- `REF_pegang_252`: median bulanan **-2.02%**, 25.0% bulan ≥ +10%, bulan terburuk -24.73%, MDD -25.26%, pulangan tahun -0.43% (SPY 25.59%, MDD SPY -8.41%)

- `REF_chandelier_4atr`: median bulanan **-5.98%**, 0.0% bulan ≥ +10%, bulan terburuk -14.33%, MDD -50.33%, pulangan tahun -46.69% (SPY 25.59%, MDD SPY -8.41%)

- `REF_jual_hari63`: median bulanan **-3.11%**, 16.7% bulan ≥ +10%, bulan terburuk -15.94%, MDD -41.61%, pulangan tahun -30.42% (SPY 25.59%, MDD SPY -8.41%)

- `hari_agihan|X=5%,Y=ema9`: median bulanan **2.34%**, 16.7% bulan ≥ +10%, bulan terburuk -11.68%, MDD -29.40%, pulangan tahun 10.98% (SPY 25.59%, MDD SPY -8.41%)

- `hari_agihan|X=5%,Y=ma50`: median bulanan **1.69%**, 16.7% bulan ≥ +10%, bulan terburuk -14.12%, MDD -31.55%, pulangan tahun 0.29% (SPY 25.59%, MDD SPY -8.41%)

- `hari_agihan|X=5%,Y=ema21`: median bulanan **2.01%**, 25.0% bulan ≥ +10%, bulan terburuk -11.46%, MDD -28.32%, pulangan tahun 9.29% (SPY 25.59%, MDD SPY -8.41%)

- `KAWALAN_RAWAK|pegang_252`: median bulanan **1.85%**, 8.3% bulan ≥ +10%, bulan terburuk -10.34%, MDD -10.36%, pulangan tahun 20.48% (SPY 25.59%, MDD SPY -8.41%)

- `KAWALAN_RAWAK|chandelier`: median bulanan **1.20%**, 8.3% bulan ≥ +10%, bulan terburuk -8.17%, MDD -13.84%, pulangan tahun 14.65% (SPY 25.59%, MDD SPY -8.41%)


**Apa yang menghalang — kapasiti, bukan kadar menang.**

- Sistem terbaik (`REF_pegang_252`) hanya membuka **8 posisi sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh dijadikan asas keputusan.

- Sistem yang pusing ganti mencukupi (Chandelier: 41 posisi, 3.4/bulan) memberi median bulanan hanya -5.98% dengan MDD -50.33% — lebih buruk daripada MDD SPY.

- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.

- KAWALAN RAWAK pegang-252 memberi 20.48% dan Chandelier rawak 14.65% — dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.


### Banding wajib: SPY dan KAWALAN RAWAK

- SPY tempoh sama: **25.59%** (MDD -8.41%). **6/6** sistem kalah kepada SPY.

- KAWALAN RAWAK terbaik: **20.48%** (`KAWALAN_RAWAK|pegang_252`). **6/6** sistem kalah kepada entri rawak.

- **Setiap sistem berasaskan signal kalah kepada entri rawak tahun ini.** Itu bukan bukti signal yang lemah sahaja; ia bukti bahawa pemilihan signal tahun ini memudaratkan portfolio berbanding memilih secara rawak daripada universe yang sama.


> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.


## 12. Keputusan akhir (had fasa: CALON)

1. **ENTRY** — TIADA signal CALON pada 2024. Semua gagal G4 (bootstrap) dan/atau G5 (outlier). Pemicu klasik tunggal juga tidak lulus.

2. **HOLD** — 0/18 signal lulus FDR; kelas pullback ialah hasil paling kukuh (SIHAT 88.4% / PASARAN 82.6% menyambung ke puncak baru lawan AMARAN 47.2%).

3. **EXIT** — 0/62 signal lulus FDR; 0/234 sistem mengalahkan ketiga-tiga rujukan dan 0/234 lulus FDR keluarga SISTEM. **Jawapan kajian tahun ini: jangan jual.**

4. **PORTFOLIO** — sasaran +10% sebulan tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila pegangan panjang, bukan kadar menang.

5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam ≥ 2 tahun LAIN; tahun lain yang siap: [2020, 2021, 2022, 2023, 2025]. Lihat `BANDING_TAHUN.md` untuk status merentas tahun.


## 13. Fail output

| Fail | Isi |
|---|---|
| `runs_2024.csv` | 3744 run, 34 lajur |
| `monthly_summary_2024.csv` | ringkasan 12 bulan |
| `skipped_2024.csv` | 15566 calon ditolak + sebab |
| `kohort_masih_naik_2024.csv` | 374 run masih_naik dijejak 252 hari |
| `common_unique_2024.csv` | 3408 baris (213 signal × subset × populasi × kumpulan × keluarga) |
| `taburan_indikator_2024.csv` | median + p25/p75 setiap indikator setiap hasil |
| `hold_exit_2024.csv` | 357 baris CALON HOLD/EXIT |
| `false_signal_2024.csv` | 162 baris (signal + penapis) |
| `hadapan_hold_exit_2024.csv` | 237 sistem (234 + 3 rujukan) |
| `kawalan_rawak_bootstrap_2024.csv` | nilai-p label rawak + had bawah bootstrap |
| `jangkaan_kemunculan_2024.csv` | jangkaan + ujian outlier |
| `keputusan_2024.csv` | keputusan gate demi gate |
| `portfolio_2024.csv`, `portfolio_bulanan_2024.csv` | Step 9 |
| `log_ujian.csv` | setiap signal/kombinasi yang diuji |
| `PANDANG_HADAPAN_2024.md` | imbasan pandang ke hadapan |
| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |
