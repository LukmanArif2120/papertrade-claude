# LAPORAN REVERSE 2023 — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.

> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = **satu rejim pasaran**. Peta sektor bukan titik-masa. Gate 8.1 ada 5 tahun lain ([2020, 2021, 2022, 2024, 2025]); keputusan **maksimum CALON** (SPEC §11.8).

## 0. Jawapan ringkas

1. **4048 run layak** dikenal pasti dalam 2023; setiap 12 bulan ada calon (tiada "TIADA CALON"). 49 SUPER PADU (≥100%), 1986 PADU, 2013 BIASA.

2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada 420 run yang masih naik pada hari ke-63, **31.4% akhirnya melebihi +100%**, dengan median kenaikan penuh **77.7%** lawan 39.9% pada hari ke-63.

3. **Signal entry: 1 CALON daripada 20 yang masuk corong**: `macd_cross&q1:cerun_ma50`.

4. **Rujukan "pegang tanpa jual hingga hari ke-252" MENANG.** Tiada satu pun daripada 234 sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan. Jangkaan: +16.25% (pegang tanpa jual hingga hari ke-252), +2.86% (jual hari ke-63), +1.51% (Chandelier 4×ATR14). Mengikut arahan Step 7b.4, jawapan kajian tahun ini ialah **"jangan jual"**.

5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan pegang-252 hanya membuka **8 posisi sepanjang tahun** (8 slot terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. Pulangannya 24.72% ialah hasil **8 saham**, bukan sistem.

6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik ialah 3.44% sebulan (median) dengan MDD -21.11%.

7. **Keluarga EXIT dan SISTEM pada FDR:** 0/64 signal EXIT dan 0/234 sistem lulus q ≤ 0.01.

## 1. Semakan kesediaan Step 0

| Semakan | Hasil |
|---|---|
| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, 2009-01-02 → 2026-10-16; semua sha256 sepadan |
| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |
| c. Sumber sektor/industri setiap ticker | **LULUS** — 2259/2268 = 99.6% (3 kelas saham diisi daripada ticker asas; 99 ticker = `Lain-lain`) |
| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 (indeks sektor A02; diluluskan pengguna) |
| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — 0.121 s/ticker; larian penuh 2268 ticker = 274 s |
| f. `semak_hadapan` atas modul indikator | **LULUS** — 14 tarikh potong (≥ 12), 26,950 perbandingan, **0 kegagalan** (`REVERSE/PANDANG_HADAPAN_2023.md`) |

## 2. Step 1–2 — run

Saiz universe 2023 setiap bulan: min **2000**, median **2000**, maks **2000**; 2268 ticker berbeza sepanjang tahun.

| bulan | n_run | n_super | n_padu | n_biasa | n_bertangga | n_lonjakan | n_stabil | n_entry_sah | n_masih_naik | n_peristiwa | med_naik |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023-01 | 304 | 1 | 54 | 249 | 10 | 146 | 148 | 276 | 8 | 1340 | 15.8 |
| 2023-02 | 124 | 2 | 37 | 85 | 2 | 92 | 30 | 94 | 8 | 769 | 18.1 |
| 2023-03 | 578 | 13 | 226 | 339 | 23 | 272 | 283 | 370 | 82 | 1724 | 23.9 |
| 2023-04 | 206 | 3 | 133 | 70 | 30 | 90 | 86 | 145 | 48 | 592 | 33.9 |
| 2023-05 | 578 | 6 | 348 | 224 | 73 | 183 | 322 | 459 | 89 | 1175 | 33.0 |
| 2023-06 | 301 | 5 | 76 | 220 | 16 | 102 | 183 | 266 | 20 | 1230 | 22.6 |
| 2023-07 | 186 | 0 | 22 | 164 | 0 | 106 | 80 | 166 | 4 | 1261 | 14.9 |
| 2023-08 | 215 | 1 | 41 | 173 | 2 | 137 | 76 | 143 | 12 | 1133 | 17.3 |
| 2023-09 | 181 | 3 | 126 | 52 | 8 | 91 | 82 | 116 | 73 | 778 | 37.0 |
| 2023-10 | 803 | 12 | 608 | 183 | 65 | 204 | 534 | 591 | 140 | 1297 | 36.5 |
| 2023-11 | 445 | 2 | 258 | 185 | 46 | 140 | 259 | 361 | 68 | 1508 | 31.7 |
| 2023-12 | 127 | 1 | 57 | 69 | 8 | 38 | 81 | 106 | 25 | 835 | 26.0 |


Jumlah: **4048 run layak**, 3093 (76.4%) dengan `entry_sah = ya` (tiada amaran: syarat 10 hari menolak 23.6% < 50%). Dilangkau: 14960 (14259 "terlalu perlahan").


### Bucket %_naik × tempoh

| bucket_pct | <=21 | <=42 | <=63 |
|---|---|---|---|
| 10%+ | 1196 | 0 | 0 |
| 100%+ | 3 | 6 | 35 |
| 20%+ | 193 | 624 | 0 |
| 200%+ | 0 | 0 | 3 |
| 30%+ | 67 | 340 | 1122 |
| 300%+ | 0 | 0 | 2 |
| 50%+ | 19 | 87 | 351 |


### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)

| kumpulan | PANTAS | PERLAHAN | SEDANG |
|---|---|---|---|
| BIASA | 1389 | 0 | 624 |
| PADU | 86 | 1473 | 427 |
| SUPER PADU | 3 | 40 | 6 |


Sel SAMPEL KECIL: [('SUPER PADU', 'PANTAS'), ('SUPER PADU', 'SEDANG')]


### Jenis kenaikan

| jenis | n |
|---|---|
| STABIL | 2164 |
| LONJAKAN | 1601 |
| BERTANGGA | 283 |


`graf_menaik = ya` (S3): 1829 (45.2%). `masih_naik = ya`: 577.


### 10 run terbaik setiap bulan (ikut %_naik_rendah)


**2023-01**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ENVX | Industrials | 2023-01-04 | 2023-03-31 | 60 | 129.38 | SUPER PADU | STABIL | tidak | tidak |
| VERX | Technology | 2023-01-20 | 2023-04-13 | 57 | 90.6 | PADU | STABIL | ya | tidak |
| TNK | Energy | 2023-01-09 | 2023-03-02 | 36 | 80.34 | PADU | STABIL | ya | tidak |
| VERA | Healthcare | 2023-01-06 | 2023-01-24 | 11 | 75.77 | PADU | STABIL | tidak | tidak |
| FATE | Healthcare | 2023-01-06 | 2023-02-03 | 19 | 70.9 | PADU | LONJAKAN | tidak | tidak |
| ALGN | Healthcare | 2023-01-06 | 2023-02-02 | 18 | 69.06 | PADU | LONJAKAN | ya | tidak |
| TRMD | Energy | 2023-01-26 | 2023-04-18 | 56 | 67.81 | PADU | STABIL | ya | tidak |
| PCOR | Technology | 2023-01-06 | 2023-02-23 | 32 | 62.7 | PADU | BERTANGGA | ya | tidak |
| INSW | Energy | 2023-01-04 | 2023-03-03 | 40 | 60.05 | PADU | BERTANGGA | ya | tidak |
| HUBS | Technology | 2023-01-06 | 2023-03-31 | 58 | 59.99 | PADU | STABIL | ya | tidak |


**2023-02**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| TGTX | Healthcare | 2023-02-28 | 2023-05-04 | 46 | 144.76 | SUPER PADU | STABIL | ya | tidak |
| GFI | Basic Materials | 2023-02-24 | 2023-05-04 | 48 | 100.17 | SUPER PADU | STABIL | tidak | tidak |
| AU | Basic Materials | 2023-02-24 | 2023-05-04 | 48 | 78.04 | PADU | STABIL | tidak | tidak |
| CVNA | Consumer Cyclical | 2023-02-24 | 2023-05-10 | 52 | 74.17 | PADU | LONJAKAN | ya | tidak |
| ONON | Consumer Cyclical | 2023-02-24 | 2023-05-08 | 50 | 69.23 | PADU | LONJAKAN | ya | tidak |
| GSHD | Financial Services | 2023-02-21 | 2023-05-10 | 55 | 65.75 | PADU | STABIL | ya | tidak |
| COIN | Financial Services | 2023-02-13 | 2023-03-21 | 25 | 56.52 | PADU | LONJAKAN | ya | tidak |
| CELH | Consumer Defensive | 2023-02-22 | 2023-05-18 | 60 | 56.38 | PADU | LONJAKAN | ya | tidak |
| SA | Basic Materials | 2023-02-24 | 2023-05-09 | 51 | 54.27 | PADU | BERTANGGA | tidak | tidak |
| NABL | Technology | 2023-02-17 | 2023-05-19 | 63 | 52.68 | PADU | LONJAKAN | ya | ya |


**2023-03**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| WAL | Financial Services | 2023-03-13 | 2023-06-08 | 61 | 453.77 | SUPER PADU | STABIL | tidak | ya |
| CUBI | Financial Services | 2023-03-13 | 2023-06-07 | 60 | 335.23 | SUPER PADU | STABIL | tidak | tidak |
| SMCI | Technology | 2023-03-15 | 2023-06-09 | 60 | 199.9 | SUPER PADU | STABIL | ya | tidak |
| MCB | Financial Services | 2023-03-13 | 2023-03-16 | 3 | 184.62 | SUPER PADU | LONJAKAN | tidak | tidak |
| FCNCA | Financial Services | 2023-03-17 | 2023-05-18 | 43 | 161.17 | SUPER PADU | STABIL | ya | tidak |
| UPST | Financial Services | 2023-03-13 | 2023-06-12 | 63 | 135.54 | SUPER PADU | STABIL | tidak | ya |
| CRDO | Technology | 2023-03-17 | 2023-06-16 | 63 | 129.92 | SUPER PADU | STABIL | ya | ya |
| APP | Communication Services | 2023-03-13 | 2023-06-05 | 58 | 118.99 | SUPER PADU | STABIL | ya | tidak |
| AI | Technology | 2023-03-15 | 2023-05-30 | 52 | 118.01 | SUPER PADU | LONJAKAN | ya | tidak |
| ARCT | Healthcare | 2023-03-02 | 2023-05-11 | 49 | 110.81 | SUPER PADU | STABIL | tidak | tidak |


**2023-04**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ENVX | Industrials | 2023-04-27 | 2023-07-18 | 55 | 145.14 | SUPER PADU | BERTANGGA | ya | tidak |
| RIVN | Consumer Cyclical | 2023-04-26 | 2023-07-26 | 62 | 132.45 | SUPER PADU | STABIL | ya | ya |
| AEHR | Technology | 2023-04-27 | 2023-07-17 | 54 | 125.75 | SUPER PADU | BERTANGGA | ya | tidak |
| TSLA | Consumer Cyclical | 2023-04-27 | 2023-07-18 | 55 | 92.52 | PADU | STABIL | ya | tidak |
| NXH | Consumer Cyclical | 2023-04-06 | 2023-06-30 | 58 | 80.64 | PADU | LONJAKAN | ya | tidak |
| COHR | Technology | 2023-04-06 | 2023-06-20 | 50 | 74.98 | PADU | STABIL | tidak | tidak |
| ACLS | Technology | 2023-04-27 | 2023-07-28 | 63 | 73.71 | PADU | BERTANGGA | ya | ya |
| GFF | Industrials | 2023-04-20 | 2023-07-14 | 58 | 72.97 | PADU | STABIL | ya | tidak |
| IMVT | Healthcare | 2023-04-10 | 2023-05-22 | 30 | 69.04 | PADU | LONJAKAN | ya | tidak |
| HELE | Consumer Defensive | 2023-04-26 | 2023-07-27 | 63 | 68.95 | PADU | LONJAKAN | ya | ya |


**2023-05**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| BBIO | Healthcare | 2023-05-25 | 2023-07-31 | 44 | 174.59 | SUPER PADU | LONJAKAN | ya | tidak |
| SYM | Industrials | 2023-05-16 | 2023-07-31 | 51 | 169.47 | SUPER PADU | LONJAKAN | ya | tidak |
| SDGR | Healthcare | 2023-05-05 | 2023-07-19 | 50 | 120.07 | SUPER PADU | BERTANGGA | ya | tidak |
| CLS | Technology | 2023-05-02 | 2023-07-31 | 61 | 109.33 | SUPER PADU | STABIL | tidak | ya |
| SPHR | Communication Services | 2023-05-16 | 2023-07-28 | 50 | 108.17 | SUPER PADU | BERTANGGA | tidak | tidak |
| ATLX | Basic Materials | 2023-05-05 | 2023-08-07 | 63 | 101.49 | SUPER PADU | LONJAKAN | ya | ya |
| ZION | Financial Services | 2023-05-02 | 2023-07-28 | 60 | 92.89 | PADU | STABIL | tidak | tidak |
| MDB | Technology | 2023-05-04 | 2023-07-19 | 51 | 90.72 | PADU | BERTANGGA | ya | tidak |
| LOB | Financial Services | 2023-05-04 | 2023-07-31 | 59 | 90.07 | PADU | BERTANGGA | ya | tidak |
| BOH | Financial Services | 2023-05-12 | 2023-07-26 | 50 | 89.8 | PADU | STABIL | tidak | tidak |


**2023-06**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| MLTX | Healthcare | 2023-06-13 | 2023-07-28 | 31 | 152.0 | SUPER PADU | LONJAKAN | ya | tidak |
| DLO | Technology | 2023-06-05 | 2023-08-30 | 60 | 138.87 | SUPER PADU | LONJAKAN | ya | tidak |
| CSTL | Healthcare | 2023-06-05 | 2023-07-07 | 22 | 119.22 | SUPER PADU | LONJAKAN | tidak | tidak |
| RIOT | Financial Services | 2023-06-15 | 2023-07-13 | 18 | 115.46 | SUPER PADU | STABIL | ya | tidak |
| W | Consumer Cyclical | 2023-06-05 | 2023-08-03 | 41 | 101.97 | SUPER PADU | BERTANGGA | ya | tidak |
| GCO | Consumer Cyclical | 2023-06-01 | 2023-08-31 | 63 | 95.66 | PADU | STABIL | ya | ya |
| CTRN | Consumer Cyclical | 2023-06-01 | 2023-08-23 | 57 | 76.14 | PADU | BERTANGGA | ya | tidak |
| HPK | Energy | 2023-06-27 | 2023-09-25 | 62 | 71.56 | PADU | STABIL | ya | ya |
| CAL | Consumer Cyclical | 2023-06-01 | 2023-08-31 | 63 | 70.67 | PADU | BERTANGGA | ya | ya |
| STRL | Industrials | 2023-06-06 | 2023-09-01 | 61 | 67.84 | PADU | STABIL | ya | ya |


**2023-07**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| AFRM | Financial Services | 2023-07-06 | 2023-09-18 | 51 | 95.24 | PADU | STABIL | ya | tidak |
| RYTM | Healthcare | 2023-07-06 | 2023-09-01 | 41 | 79.35 | PADU | LONJAKAN | ya | tidak |
| PDS | Energy | 2023-07-06 | 2023-09-15 | 50 | 56.82 | PADU | STABIL | ya | tidak |
| RCKT | Healthcare | 2023-07-27 | 2023-09-14 | 34 | 42.65 | PADU | LONJAKAN | tidak | tidak |
| STNG | Energy | 2023-07-21 | 2023-10-17 | 61 | 41.0 | PADU | STABIL | ya | ya |
| TRNS | Industrials | 2023-07-06 | 2023-09-15 | 50 | 40.88 | PADU | STABIL | ya | tidak |
| LRN | Consumer Defensive | 2023-07-27 | 2023-10-25 | 63 | 40.02 | PADU | LONJAKAN | ya | ya |
| MPC | Energy | 2023-07-06 | 2023-09-18 | 51 | 39.28 | PADU | STABIL | ya | tidak |
| PKX | Basic Materials | 2023-07-18 | 2023-07-25 | 5 | 38.2 | PADU | LONJAKAN | ya | tidak |
| HP | Energy | 2023-07-06 | 2023-09-14 | 49 | 38.0 | PADU | STABIL | ya | tidak |


**2023-08**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| IMVT | Healthcare | 2023-08-25 | 2023-09-26 | 21 | 102.74 | SUPER PADU | LONJAKAN | ya | tidak |
| MNSO | Consumer Cyclical | 2023-08-11 | 2023-09-14 | 23 | 61.76 | PADU | STABIL | ya | tidak |
| MSTR | Technology | 2023-08-18 | 2023-11-10 | 59 | 57.99 | PADU | STABIL | ya | tidak |
| ASLE | Industrials | 2023-08-09 | 2023-09-11 | 22 | 57.65 | PADU | STABIL | ya | tidak |
| CVNA | Consumer Cyclical | 2023-08-17 | 2023-09-14 | 19 | 53.38 | PADU | LONJAKAN | ya | tidak |
| ARRY | Technology | 2023-08-08 | 2023-09-14 | 26 | 52.4 | PADU | LONJAKAN | ya | tidak |
| RBLX | Communication Services | 2023-08-24 | 2023-11-15 | 58 | 51.52 | PADU | STABIL | tidak | tidak |
| HE | Utilities | 2023-08-17 | 2023-09-01 | 11 | 49.75 | PADU | LONJAKAN | tidak | tidak |
| NSSC | Industrials | 2023-08-21 | 2023-11-17 | 63 | 43.02 | PADU | LONJAKAN | tidak | ya |
| KD | Technology | 2023-08-03 | 2023-09-08 | 25 | 41.95 | PADU | LONJAKAN | ya | tidak |


**2023-09**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| MARA | Financial Services | 2023-09-27 | 2023-12-27 | 63 | 292.79 | SUPER PADU | STABIL | tidak | ya |
| AAOI | Technology | 2023-09-13 | 2023-12-08 | 61 | 124.09 | SUPER PADU | STABIL | tidak | ya |
| RIOT | Financial Services | 2023-09-27 | 2023-12-27 | 63 | 111.11 | SUPER PADU | STABIL | ya | ya |
| BHVN | Healthcare | 2023-09-05 | 2023-12-04 | 63 | 95.96 | PADU | LONJAKAN | ya | ya |
| M | Consumer Cyclical | 2023-09-21 | 2023-12-11 | 56 | 94.84 | PADU | STABIL | ya | tidak |
| CUBI | Financial Services | 2023-09-27 | 2023-12-27 | 63 | 89.25 | PADU | BERTANGGA | ya | ya |
| ANF | Consumer Cyclical | 2023-09-21 | 2023-12-19 | 62 | 84.73 | PADU | BERTANGGA | ya | ya |
| STNE | Technology | 2023-09-27 | 2023-12-27 | 63 | 83.65 | PADU | STABIL | tidak | ya |
| UPST | Financial Services | 2023-09-25 | 2023-12-19 | 60 | 83.02 | PADU | LONJAKAN | tidak | tidak |
| PI | Technology | 2023-09-26 | 2023-12-26 | 63 | 76.2 | PADU | STABIL | ya | ya |


**2023-10**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| CYTK | Healthcare | 2023-10-04 | 2024-01-04 | 63 | 239.65 | SUPER PADU | LONJAKAN | ya | ya |
| AFRM | Financial Services | 2023-10-05 | 2023-12-28 | 58 | 202.47 | SUPER PADU | STABIL | ya | tidak |
| XMTR | Industrials | 2023-10-30 | 2023-12-28 | 41 | 180.38 | SUPER PADU | BERTANGGA | ya | tidak |
| COIN | Financial Services | 2023-10-27 | 2023-12-28 | 42 | 164.64 | SUPER PADU | STABIL | ya | tidak |
| FLNA | Healthcare | 2023-10-13 | 2023-12-14 | 43 | 144.4 | SUPER PADU | BERTANGGA | ya | tidak |
| ARVN | Healthcare | 2023-10-04 | 2023-12-27 | 58 | 138.48 | SUPER PADU | STABIL | tidak | tidak |
| SRPT | Healthcare | 2023-10-31 | 2024-02-01 | 63 | 122.32 | SUPER PADU | STABIL | tidak | ya |
| HASI | Financial Services | 2023-10-06 | 2023-12-14 | 48 | 122.24 | SUPER PADU | STABIL | tidak | tidak |
| TWST | Healthcare | 2023-10-04 | 2023-12-26 | 57 | 116.67 | SUPER PADU | STABIL | tidak | tidak |
| VSXY | Consumer Cyclical | 2023-10-06 | 2023-12-26 | 55 | 111.6 | SUPER PADU | BERTANGGA | ya | tidak |


**2023-11**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| CABA | Healthcare | 2023-11-28 | 2024-02-08 | 49 | 165.76 | SUPER PADU | STABIL | ya | tidak |
| GRPN | Communication Services | 2023-11-10 | 2024-02-12 | 62 | 109.65 | SUPER PADU | STABIL | tidak | ya |
| ARCT | Healthcare | 2023-11-02 | 2024-02-05 | 63 | 92.06 | PADU | STABIL | ya | ya |
| ARWR | Healthcare | 2023-11-30 | 2024-01-08 | 25 | 86.58 | PADU | BERTANGGA | ya | tidak |
| SYM | Industrials | 2023-11-01 | 2023-11-27 | 17 | 83.62 | PADU | LONJAKAN | ya | tidak |
| SLAB | Technology | 2023-11-01 | 2023-12-27 | 38 | 81.97 | PADU | STABIL | ya | tidak |
| TRUP | Financial Services | 2023-11-01 | 2023-12-14 | 30 | 81.76 | PADU | BERTANGGA | ya | tidak |
| CELH | Consumer Defensive | 2023-11-30 | 2024-03-04 | 63 | 79.79 | PADU | LONJAKAN | tidak | ya |
| MKSI | Technology | 2023-11-01 | 2024-01-25 | 57 | 79.61 | PADU | STABIL | ya | tidak |
| XENE | Healthcare | 2023-11-13 | 2024-02-09 | 60 | 78.81 | PADU | STABIL | ya | tidak |


**2023-12**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| DJT | Communication Services | 2023-12-08 | 2024-01-23 | 29 | 199.41 | SUPER PADU | LONJAKAN | ya | tidak |
| BMEA | Healthcare | 2023-12-11 | 2024-02-01 | 35 | 88.13 | PADU | STABIL | ya | tidak |
| COHR | Technology | 2023-12-01 | 2024-03-04 | 62 | 85.34 | PADU | BERTANGGA | ya | ya |
| GPCR | Healthcare | 2023-12-18 | 2024-01-09 | 14 | 84.67 | PADU | STABIL | tidak | tidak |
| STRL | Industrials | 2023-12-04 | 2024-03-04 | 61 | 77.69 | PADU | STABIL | ya | ya |
| XPOF | Consumer Cyclical | 2023-12-11 | 2024-03-12 | 62 | 77.03 | PADU | LONJAKAN | tidak | ya |
| VST | Utilities | 2023-12-07 | 2024-03-07 | 61 | 71.5 | PADU | STABIL | ya | ya |
| KNSL | Financial Services | 2023-12-07 | 2024-03-06 | 60 | 68.65 | PADU | STABIL | ya | tidak |
| RYTM | Healthcare | 2023-12-04 | 2024-02-12 | 47 | 60.66 | PADU | STABIL | ya | tidak |
| PSFE | Technology | 2023-12-01 | 2024-01-29 | 38 | 59.22 | PADU | BERTANGGA | ya | tidak |


### Semua run SUPER PADU (≥ 100%)

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|
| WAL | Financial Services | 2023-03-13 | 61 | 453.77 | STABIL | tidak | ya |
| CUBI | Financial Services | 2023-03-13 | 60 | 335.23 | STABIL | tidak | tidak |
| MARA | Financial Services | 2023-09-27 | 63 | 292.79 | STABIL | tidak | ya |
| CYTK | Healthcare | 2023-10-04 | 63 | 239.65 | LONJAKAN | ya | ya |
| AFRM | Financial Services | 2023-10-05 | 58 | 202.47 | STABIL | ya | tidak |
| SMCI | Technology | 2023-03-15 | 60 | 199.9 | STABIL | ya | tidak |
| DJT | Communication Services | 2023-12-08 | 29 | 199.41 | LONJAKAN | ya | tidak |
| MCB | Financial Services | 2023-03-13 | 3 | 184.62 | LONJAKAN | tidak | tidak |
| XMTR | Industrials | 2023-10-30 | 41 | 180.38 | BERTANGGA | ya | tidak |
| BBIO | Healthcare | 2023-05-25 | 44 | 174.59 | LONJAKAN | ya | tidak |
| SYM | Industrials | 2023-05-16 | 51 | 169.47 | LONJAKAN | ya | tidak |
| CABA | Healthcare | 2023-11-28 | 49 | 165.76 | STABIL | ya | tidak |
| COIN | Financial Services | 2023-10-27 | 42 | 164.64 | STABIL | ya | tidak |
| FCNCA | Financial Services | 2023-03-17 | 43 | 161.17 | STABIL | ya | tidak |
| MLTX | Healthcare | 2023-06-13 | 31 | 152.0 | LONJAKAN | ya | tidak |
| ENVX | Industrials | 2023-04-27 | 55 | 145.14 | BERTANGGA | ya | tidak |
| TGTX | Healthcare | 2023-02-28 | 46 | 144.76 | STABIL | ya | tidak |
| FLNA | Healthcare | 2023-10-13 | 43 | 144.4 | BERTANGGA | ya | tidak |
| DLO | Technology | 2023-06-05 | 60 | 138.87 | LONJAKAN | ya | tidak |
| ARVN | Healthcare | 2023-10-04 | 58 | 138.48 | STABIL | tidak | tidak |
| UPST | Financial Services | 2023-03-13 | 63 | 135.54 | STABIL | tidak | ya |
| RIVN | Consumer Cyclical | 2023-04-26 | 62 | 132.45 | STABIL | ya | ya |
| CRDO | Technology | 2023-03-17 | 63 | 129.92 | STABIL | ya | ya |
| ENVX | Industrials | 2023-01-04 | 60 | 129.38 | STABIL | tidak | tidak |
| AEHR | Technology | 2023-04-27 | 54 | 125.75 | BERTANGGA | ya | tidak |
| AAOI | Technology | 2023-09-13 | 61 | 124.09 | STABIL | tidak | ya |
| SRPT | Healthcare | 2023-10-31 | 63 | 122.32 | STABIL | tidak | ya |
| HASI | Financial Services | 2023-10-06 | 48 | 122.24 | STABIL | tidak | tidak |
| SDGR | Healthcare | 2023-05-05 | 50 | 120.07 | BERTANGGA | ya | tidak |
| CSTL | Healthcare | 2023-06-05 | 22 | 119.22 | LONJAKAN | tidak | tidak |
| APP | Communication Services | 2023-03-13 | 58 | 118.99 | STABIL | ya | tidak |
| AI | Technology | 2023-03-15 | 52 | 118.01 | LONJAKAN | ya | tidak |
| TWST | Healthcare | 2023-10-04 | 57 | 116.67 | STABIL | tidak | tidak |
| RIOT | Financial Services | 2023-06-15 | 18 | 115.46 | STABIL | ya | tidak |
| VSXY | Consumer Cyclical | 2023-10-06 | 55 | 111.6 | BERTANGGA | ya | tidak |
| RIOT | Financial Services | 2023-09-27 | 63 | 111.11 | STABIL | ya | ya |
| ARCT | Healthcare | 2023-03-02 | 49 | 110.81 | STABIL | tidak | tidak |
| GRPN | Communication Services | 2023-11-10 | 62 | 109.65 | STABIL | tidak | ya |
| RUN | Technology | 2023-10-04 | 58 | 109.48 | LONJAKAN | tidak | tidak |
| CLS | Technology | 2023-05-02 | 61 | 109.33 | STABIL | tidak | ya |
| SPHR | Communication Services | 2023-05-16 | 50 | 108.17 | BERTANGGA | tidak | tidak |
| KYMR | Healthcare | 2023-10-02 | 59 | 107.42 | STABIL | tidak | tidak |
| QTRX | Healthcare | 2023-03-01 | 59 | 102.88 | LONJAKAN | ya | tidak |
| VKTX | Healthcare | 2023-03-28 | 50 | 102.86 | STABIL | ya | tidak |
| IMVT | Healthcare | 2023-08-25 | 21 | 102.74 | LONJAKAN | ya | tidak |
| W | Consumer Cyclical | 2023-06-05 | 41 | 101.97 | BERTANGGA | ya | tidak |
| ATLX | Basic Materials | 2023-05-05 | 63 | 101.49 | LONJAKAN | ya | ya |
| AFRM | Financial Services | 2023-03-13 | 61 | 100.32 | STABIL | tidak | ya |
| GFI | Basic Materials | 2023-02-24 | 48 | 100.17 | STABIL | tidak | tidak |


(dipaparkan 60 teratas daripada 49)


### Run BERTANGGA (S2) — 40 teratas

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | bilangan_kaki | pct_hari_atas_ema21 | kumpulan |
|---|---|---|---|---|---|---|---|
| XMTR | Industrials | 2023-10-30 | 41 | 180.38 | 3 | 94.7 | SUPER PADU |
| ENVX | Industrials | 2023-04-27 | 55 | 145.14 | 3 | 82.0 | SUPER PADU |
| FLNA | Healthcare | 2023-10-13 | 43 | 144.4 | 3 | 80.6 | SUPER PADU |
| AEHR | Technology | 2023-04-27 | 54 | 125.75 | 3 | 89.4 | SUPER PADU |
| SDGR | Healthcare | 2023-05-05 | 50 | 120.07 | 4 | 100.0 | SUPER PADU |
| VSXY | Consumer Cyclical | 2023-10-06 | 55 | 111.6 | 4 | 98.0 | SUPER PADU |
| SPHR | Communication Services | 2023-05-16 | 50 | 108.17 | 2 | 68.6 | SUPER PADU |
| W | Consumer Cyclical | 2023-06-05 | 41 | 101.97 | 3 | 100.0 | SUPER PADU |
| RCKT | Healthcare | 2023-10-19 | 47 | 92.99 | 2 | 92.7 | PADU |
| PTGX | Healthcare | 2023-10-25 | 52 | 90.96 | 3 | 95.7 | PADU |
| MDB | Technology | 2023-05-04 | 51 | 90.72 | 3 | 100.0 | PADU |
| LOB | Financial Services | 2023-05-04 | 59 | 90.07 | 4 | 94.1 | PADU |
| CUBI | Financial Services | 2023-09-27 | 63 | 89.25 | 3 | 74.2 | PADU |
| ARWR | Healthcare | 2023-11-30 | 25 | 86.58 | 2 | 100.0 | PADU |
| CCL | Consumer Cyclical | 2023-03-15 | 63 | 86.38 | 4 | 77.8 | PADU |
| CSTL | Healthcare | 2023-10-13 | 52 | 85.83 | 2 | 79.2 | PADU |
| COHR | Technology | 2023-12-01 | 62 | 85.34 | 2 | 91.9 | PADU |
| ANF | Consumer Cyclical | 2023-09-21 | 62 | 84.73 | 2 | 98.4 | PADU |
| FNKO | Consumer Cyclical | 2023-03-14 | 63 | 82.65 | 4 | 73.4 | PADU |
| TRUP | Financial Services | 2023-11-01 | 30 | 81.76 | 2 | 79.3 | PADU |
| FG | Financial Services | 2023-10-04 | 49 | 81.55 | 2 | 98.0 | PADU |
| NVDA | Technology | 2023-03-16 | 62 | 79.97 | 2 | 98.4 | PADU |
| TARS | Healthcare | 2023-10-13 | 63 | 78.59 | 4 | 68.8 | PADU |
| FRSH | Technology | 2023-05-04 | 61 | 76.84 | 4 | 85.7 | PADU |
| CTRN | Consumer Cyclical | 2023-06-01 | 57 | 76.14 | 2 | 90.7 | PADU |
| PODD | Healthcare | 2023-10-12 | 52 | 75.98 | 2 | 69.8 | PADU |
| RGEN | Healthcare | 2023-10-30 | 62 | 75.18 | 2 | 86.4 | PADU |
| LOB | Financial Services | 2023-10-04 | 59 | 75.14 | 4 | 86.3 | PADU |
| BRZE | Technology | 2023-05-04 | 59 | 74.08 | 4 | 98.0 | PADU |
| UCTT | Technology | 2023-10-23 | 62 | 74.0 | 2 | 87.0 | PADU |
| ACLS | Technology | 2023-04-27 | 63 | 73.71 | 4 | 90.9 | PADU |
| AX | Financial Services | 2023-10-27 | 62 | 70.91 | 2 | 88.3 | PADU |
| CAL | Consumer Cyclical | 2023-06-01 | 63 | 70.67 | 2 | 82.0 | PADU |
| PUBM | Technology | 2023-05-04 | 59 | 70.42 | 2 | 85.7 | PADU |
| BURL | Consumer Cyclical | 2023-10-13 | 52 | 70.37 | 2 | 71.7 | PADU |
| LUNG | Healthcare | 2023-10-13 | 43 | 69.55 | 2 | 70.5 | PADU |
| WRLD | Financial Services | 2023-03-15 | 63 | 68.87 | 5 | 71.9 | PADU |
| MTZ | Industrials | 2023-11-01 | 40 | 68.27 | 2 | 63.4 | PADU |
| DAVA | Technology | 2023-11-01 | 54 | 67.44 | 2 | 96.2 | PADU |
| SLM | Financial Services | 2023-10-26 | 63 | 65.73 | 2 | 96.7 | PADU |


(daripada 283 run BERTANGGA)


### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)

n peristiwa PADU dalam S2, populasi keputusan (a) = **200** (rujukan: semua peristiwa = 943). < 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat.


Peristiwa sah: **13642** (populasi keputusan 5436).


## 3. Step 2b — kohort "naik dan naik"

Dijejak 420 run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari tarikh_sah.


| Metrik | Nilai |
|---|---|
| % akhirnya melebihi +100% | **31.4%** |
| median %_naik_penuh | **77.7%** |
| median %_naik pada hari ke-63 | 39.9% |
| median hari ke puncak penuh | 210 |
| median MFE 252 selepas kos | 60.7% |
| median MAE 252 | -4.9% |
| median hari pegang Chandelier 4×ATR | 92 |
| median pulangan Chandelier selepas kos | 20.0% |
| terpotong hujung data | 0.0% |


Exit yang menyala dahulu:


| exit | n |
|---|---|
| bawah_ma50 | 170 |
| bawah_ema9 | 136 |
| bawah_ema21 | 31 |
| hist_neg3 | 28 |
| hari_agihan | 22 |
| macd_bawah | 17 |
| rsi_70_60 | 16 |


### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari

| kohort | n | median_naik_63 | pct_bertangga | pct_super | median_hari_ke_puncak |
|---|---|---|---|---|---|
| masih_naik = ya | 420 | 39.9 | 21.0 | 1.2 | 63.0 |
| reda dalam 63 hari | 2673 | 24.7 | 6.1 | 0.9 | 30.0 |


Kohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya diketahui pada hari ke-63.


## 4. Step 3 — populasi kuintil dan dedup

POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **6880** baris. Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **32** daripada 41; dibuang 9.


| buang | kerana | rho |
|---|---|---|
| j_ma150 | j_ma200 | 0.96 |
| cerun_ema21 | j_ma50 | 0.812 |
| cerun_ma200 | j_ma200 | 0.806 |
| rsi14 | j_ma50 | 0.834 |
| roc60 | cerun_ma50 | 0.931 |
| willr14 | stoch_k | 1.0 |
| bb_pctb | cci20 | 0.915 |
| kelt_pos | j_ema21 | 0.928 |
| rs_spy_3b | cerun_ma50 | 0.839 |


Signal dibina: **215** (31 binari + 64 hujung kuintil + 120 pemicu × 1 konteks).


## 5. Step 4 — common & unique (ENTRY)

Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. N ujian ENTRY sebenar (populasi a, kumpulan A) = **860** baris (213 signal × 2 subset × 2 keluarga).


### Kelas (S2, kumpulan A, keluarga PADU)

| kelas | n |
|---|---|
| TIDAK BERGUNA | 194 |
| COMMON BIASA | 9 |
| SEDERHANA | 5 |
| UNIQUE | 4 |
| LANGKA | 3 |


### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)

| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n | n_industri | n_minggu | purata_pct_naik_rendah | purata_hari_ke_puncak | pct_bertangga | pct_lonjakan | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | UNIQUE | 21.3 | 0.0 | 1.64 | 1.06 | 13.024 | 20.121 | 52.73 | 7.895 | 55 | 26 | 25 | 75.71 | 49.8 | 100.0 | 0.0 |  |
| q5:atr_pct | UNIQUE | 32.41 | 0.0 | 3.14 | 18.56 | 10.306 | 1.746 | 45.05 | 6.746 | 91 | 39 | 31 | 67.01 | 50.4 | 100.0 | 0.0 |  |
| pocket_pivot&q1:j_52w_tinggi | LANGKA | 13.89 | 0.0 | 2.08 | 1.29 | 6.692 | 10.737 | 32.65 | 4.889 | 49 | 32 | 27 | 55.68 | 51.9 | 100.0 | 0.0 |  |
| macd_cross&q1:j_52w_tinggi | LANGKA | 7.41 | 0.0 | 1.32 | 0.78 | 5.608 | 9.448 | 32.26 | 4.83 | 31 | 18 | 18 | 70.03 | 45.4 | 100.0 | 0.0 |  |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 18.52 | 0.0 | 3.4 | 1.06 | 5.453 | 17.497 | 30.77 | 4.607 | 78 | 36 | 31 | 71.15 | 47.6 | 100.0 | 0.0 |  |
| q1:j_52w_tinggi | UNIQUE | 39.81 | 0.0 | 7.42 | 20.25 | 5.365 | 1.966 | 28.48 | 4.265 | 165 | 60 | 47 | 59.0 | 50.3 | 100.0 | 0.0 |  |
| macd_cross&q1:cerun_ma50 | LANGKA | 12.96 | 0.0 | 2.45 | 0.61 | 5.285 | 21.335 | 27.78 | 4.159 | 54 | 33 | 17 | 50.19 | 51.3 | 100.0 | 0.0 |  |


### Rujukan S1 (semua run layak)

_(tiada baris)_


### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja

S3 mengandungi 1639 run; ia **bukan keluarga carian** (tidak menambah N). 9.2% daripadanya BERTANGGA lawan 8.1% keseluruhan.


### Keluarga SUPER PADU (FDR sendiri)

| signal | kelas | K_super | lift | lift_rawak | n | tanda |
|---|---|---|---|---|---|---|
| ema_crossback&q5:atr_pct | TERAS | 50.0 | 72.273 | 110.913 | 19 | SAMPEL KECIL |
| rsi_lintas50&q5:atr_pct | TERAS | 100.0 | 61.154 | 94.481 | 55 |  |
| macd_cross&q5:atr_pct | UNIQUE | 33.33 | 58.889 | 47.241 | 19 | SAMPEL KECIL |
| ema_crossback&q1:j_ma200 | UNIQUE | 16.67 | 53.0 | 212.583 | 6 | SAMPEL KECIL |
| ema_crossback&q5:julat20 | TERAS | 50.0 | 44.167 | 121.476 | 25 |  |
| ema_crossback&q1:j_52w_tinggi | UNIQUE | 33.33 | 44.167 | 106.292 | 14 | SAMPEL KECIL |
| q5:atr_pct | TERAS | 100.0 | 31.8 | 5.388 | 91 |  |
| ema_crossback&q1:rs_spy_6b | UNIQUE | 16.67 | 29.444 | 94.481 | 12 | SAMPEL KECIL |
| ema_crossback&q5:bb_lebar | UNIQUE | 33.33 | 27.895 | 106.292 | 26 |  |
| macd_cross&q1:j_52w_tinggi | UNIQUE | 33.33 | 25.238 | 42.517 | 31 |  |
| pocket_pivot&q5:atr_pct | UNIQUE | 16.67 | 24.091 | 13.286 | 19 | SAMPEL KECIL |
| rsi_lintas50&q1:j_52w_tinggi | TERAS | 66.67 | 19.63 | 62.988 | 78 |  |
| rsi_lintas50&q5:cerun_ma50 | UNIQUE | 33.33 | 14.324 | 36.184 | 45 |  |
| ema_crossback&q5:cerun_ma50 | UNIQUE | 33.33 | 12.045 | 27.43 | 53 |  |
| macd_cross&q5:rs_spy_6b | UNIQUE | 16.67 | 9.815 | 26.573 | 33 |  |
| ema_crossback&q1:lapis | UNIQUE | 33.33 | 9.138 | 130.821 | 68 |  |
| q1:j_52w_tinggi | TERAS | 66.67 | 8.983 | 3.293 | 165 |  |
| rsi_lintas50&q5:j_ma200 | UNIQUE | 33.33 | 8.548 | 40.492 | 74 |  |
| rsi_lintas50&q5:rs_spy_6b | TERAS | 50.0 | 8.281 | 52.061 | 114 |  |
| pocket_pivot&q1:j_52w_tinggi | UNIQUE | 16.67 | 8.03 | 12.884 | 49 |  |


### PEMICU YANG TIDAK MEMBEZAKAN

Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.


| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n |
|---|---|---|---|---|---|---|---|---|---|---|
| b:donchian20 | TIDAK BERGUNA | 3.7 | 0.0 | 9.81 | 8.49 | 0.377 | 0.436 | 2.5 | 0.374 | 160 |
| b:ema_crossback | TIDAK BERGUNA | 20.37 | 0.0 | 15.97 | 2.82 | 1.275 | 7.217 | 8.96 | 1.342 | 279 |
| b:gap_and_go | TIDAK BERGUNA | 5.56 | 0.0 | 1.51 | 0.45 | 3.681 | 12.324 | 20.0 | 2.995 | 30 |
| b:macd_cross | TIDAK BERGUNA | 24.07 | 33.33 | 22.33 | 3.35 | 0.722 | 7.183 | 7.29 | 1.092 | 384 |
| b:pocket_pivot | TIDAK BERGUNA | 33.33 | 66.67 | 25.79 | 9.25 | 0.5 | 3.603 | 8.24 | 1.234 | 449 |
| b:rsi_lintas50 | COMMON BIASA | 62.04 | 100.0 | 44.21 | 5.39 | 0.62 | 11.51 | 9.37 | 1.403 | 779 |


**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis yang diuji dalam kajian ini, dan ia disokong oleh data 2025.


### Corong ke Step 7
20 signal diteruskan (had 30; layak sebelum had: 20).


## 6. Step 5 — HOLD

> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana berjaya. Semua CALON.


### Kelas pullback

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| AMARAN | 4568 | 46.2 | -15.23 | 10.4 |
| PULLBACK PASARAN | 115 | 80.0 | -7.82 | 8.4 |
| PULLBACK SIHAT | 1322 | 91.5 | -7.6 | 8.1 |


Pullback yang trend sahamnya utuh (SIHAT 91.5%, PASARAN 80.0%) menyambung ke puncak baru jauh lebih kerap daripada pullback AMARAN (46.2%). Ini sokongan paling jelas bagi falsafah "pegang selagi naik".


### Grid 18 peraturan HOLD (deskriptif)

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| X=5%,Y=ema9 | 8 | 100.0 | -5.0 | 5.6 |
| X=5%,Y=ema21 | 1553 | 93.0 | -6.81 | 6.4 |
| X=5%,Y=ma50 | 2229 | 89.4 | -7.78 | 8.0 |
| X=7%,Y=ema9 | 1445 | 94.4 | -5.93 | 6.0 |
| X=7%,Y=ema21 | 1937 | 93.0 | -6.68 | 6.4 |
| X=7%,Y=ma50 | 2535 | 90.2 | -7.57 | 7.6 |
| X=10%,Y=ema9 | 2728 | 88.2 | -7.07 | 7.3 |
| X=10%,Y=ema21 | 2814 | 88.1 | -7.25 | 7.4 |
| X=10%,Y=ma50 | 3049 | 87.0 | -7.73 | 7.8 |
| X=12%,Y=ema9 | 3261 | 84.2 | -7.72 | 8.0 |
| X=12%,Y=ema21 | 3297 | 84.2 | -7.8 | 8.0 |
| X=12%,Y=ma50 | 3424 | 83.4 | -8.09 | 8.2 |
| X=15%,Y=ema9 | 3941 | 78.2 | -8.71 | 8.8 |
| X=15%,Y=ema21 | 3953 | 78.2 | -8.74 | 8.8 |
| X=15%,Y=ma50 | 3999 | 77.9 | -8.87 | 8.8 |
| X=20%,Y=ema9 | 4758 | 69.5 | -10.19 | 9.2 |
| X=20%,Y=ema21 | 4764 | 69.5 | -10.21 | 9.2 |
| X=20%,Y=ma50 | 4779 | 69.4 | -10.25 | 9.2 |


### Common/unique HOLD (lulus FDR)

0 / 18 signal HOLD lulus BH-FDR q ≤ 0.01: 


| nama | subset | n | K_padu | K_gagal | lift | presisi | lift_presisi | kelas |
|---|---|---|---|---|---|---|---|---|
| b:macd_cross | S1 | 1 | 0.03 | 0.0 | 1.76 | 100.0 | 1.76 | TIDAK BERGUNA |
| b:vcp | S1 | 245 | 6.89 | 0.39 | 17.871 | 95.92 | 1.689 | LANGKA |
| b:atas_ema21 | S1 | 729 | 20.43 | 1.23 | 16.564 | 95.61 | 1.683 | UNIQUE |
| b:supertrend_naik | S1 | 2017 | 54.71 | 5.82 | 9.398 | 92.51 | 1.629 | TERAS |
| b:psar_naik | S1 | 863 | 23.39 | 2.51 | 9.336 | 92.47 | 1.628 | UNIQUE |
| b:atas_ma50 | S1 | 1793 | 47.73 | 6.36 | 7.503 | 90.8 | 1.598 | UNIQUE |
| b:tenkan_atas | S1 | 2201 | 58.31 | 8.17 | 7.135 | 90.37 | 1.591 | TERAS |
| b:macd_atas0 | S1 | 2343 | 60.57 | 10.68 | 5.672 | 88.18 | 1.552 | TERAS |
| b:atas_awan | S1 | 1853 | 47.61 | 8.83 | 5.393 | 87.64 | 1.543 | UNIQUE |
| b:bb_squeeze | S1 | 61 | 1.52 | 0.35 | 4.394 | 85.25 | 1.501 | TIDAK BERGUNA |
| b:pullback_dalam_7pct | S1 | 3670 | 82.62 | 32.85 | 2.515 | 76.78 | 1.352 | TERAS |
| b:sektor_atas_ma50 | S1 | 2497 | 54.88 | 24.09 | 2.278 | 74.97 | 1.32 | TERAS |
| b:sektor_naik | S1 | 2497 | 54.88 | 24.09 | 2.278 | 74.97 | 1.32 | TERAS |
| b:vcp | S2 | 65 | 9.12 | 0.0 | 85.694 | 100.0 | 1.318 | LANGKA |
| b:psar_naik | S2 | 225 | 31.14 | 1.32 | 23.56 | 98.67 | 1.301 | UNIQUE |
| b:atas_ema21 | S2 | 214 | 29.59 | 1.32 | 22.392 | 98.6 | 1.3 | UNIQUE |
| b:supertrend_naik | S2 | 547 | 74.61 | 6.61 | 11.292 | 97.26 | 1.282 | TERAS |
| b:tenkan_atas | S2 | 559 | 75.74 | 8.37 | 9.048 | 96.6 | 1.274 | TERAS |
| b:atas_ma50 | S2 | 449 | 60.31 | 8.37 | 7.205 | 95.77 | 1.263 | TERAS |
| b:macd_atas0 | S2 | 568 | 75.46 | 13.22 | 5.709 | 94.72 | 1.249 | TERAS |


## 7. Step 6 — EXIT (semua CALON)

> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.


| nama | n | pct_menyala | median_hari_dari_puncak | median_pulangan_exit | median_pct_kekal | kadar_exit_palsu |
|---|---|---|---|---|---|---|
| atr_lonjak_15x | 513 | 17.0 | 22.0 | -6.39 | -41.9 | 39.0 |
| bawah_ema21 | 3016 | 100.0 | -13.0 | -0.78 | -4.0 | 60.3 |
| bawah_ema9 | 3017 | 100.0 | -20.0 | -0.47 | -2.3 | 64.3 |
| bawah_ma50 | 2985 | 98.9 | -13.0 | -0.63 | -3.4 | 58.7 |
| chandelier_4atr | 2677 | 88.7 | 16.0 | -0.36 | 1.6 | 34.7 |
| climax_25_15h | 645 | 21.4 | -13.0 | 17.62 | 63.7 | 62.9 |
| div_macd | 2793 | 92.6 | -20.0 | 3.64 | 23.4 | 60.9 |
| div_rsi | 2566 | 85.1 | -16.0 | 5.74 | 35.5 | 57.6 |
| gap_besar | 241 | 8.0 | -2.0 | 27.96 | 86.2 | 56.8 |
| hari_agihan | 2631 | 87.2 | 2.0 | 2.6 | 20.1 | 45.6 |
| hist_neg3 | 3005 | 99.6 | -6.0 | 1.81 | 14.9 | 52.0 |
| jauh_ma50_2x | 1477 | 49.0 | -10.0 | 11.28 | 63.4 | 47.5 |
| macd_bawah | 3010 | 99.8 | -8.0 | 2.24 | 18.4 | 53.8 |
| pullback_amaran | 2944 | 97.6 | 24.0 | -5.34 | -29.1 | 62.1 |
| rsi_70_60 | 2113 | 70.0 | 2.0 | 11.32 | 59.4 | 46.8 |
| trail_10pct | 2626 | 87.0 | 13.0 | -1.01 | -3.8 | 39.9 |
| trail_15pct | 1886 | 62.5 | 23.0 | -5.78 | -32.1 | 36.2 |
| trail_2atr | 3017 | 100.0 | 3.0 | 1.3 | 11.4 | 49.7 |
| trail_3atr | 2949 | 97.7 | 9.0 | 1.29 | 11.4 | 40.5 |
| trail_8pct | 2852 | 94.5 | 7.0 | 0.14 | 3.0 | 42.8 |


`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala 13–20 hari sebelum puncak dan mengekalkan hanya -2% hingga -4% keuntungan. Kadar exit palsu 35%–64%.


**Keluarga EXIT: 0 / 64 signal lulus BH-FDR q ≤ 0.01.** Tiada signal EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas kawalan pelbagai ujian.


## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)

Setiap signal corong diimbas atas **semua** hari universe 2023 (566,920 baris (ticker, hari); 499,999 selepas topeng universe). Kadar asas KAWALAN RAWAK (MFE63 ≥ 30%) = 12.13%.


| signal | n_kemunculan | kadar_tepat_mfe30 | lift_tepat | kadar_palsu_bawah10 | kadar_tepat_bertangga | ketulenan_trend_median | mfe63_p50 | mfe63_p75 | mfe63_p90 | pct_mfe63_ge30 | pct_mfe63_ge100 | mfe252_p90 | pct_mfe252_ge100 | median_hari_mfe63 | jangkaan_henti2atr | kadar_menang | kapasiti | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | 4738 | 28.7 | 2.366 | 35.08 | 3.57 | 79.6 | 16.8 | 33.04 | 53.61 | 28.7 | 2.2 | 122.18 | 14.96 | 29.0 | 1.542 | 33.28 | TULANG BELAKANG |  |
| rsi_lintas50&q5:julat20 | 4358 | 26.5 | 2.185 | 35.61 | 2.94 | 81.0 | 16.08 | 31.05 | 50.44 | 26.5 | 2.16 | 115.13 | 13.15 | 30.0 | 2.317 | 35.73 | TULANG BELAKANG |  |
| q5:atr_pct | 95479 | 27.57 | 2.273 | 35.99 | 3.11 | 65.0 | 16.1 | 32.24 | 52.85 | 27.57 | 1.88 | 125.18 | 15.47 | 31.0 | 1.526 | 34.07 | TULANG BELAKANG |  |
| rsi_lintas50&q5:bb_lebar | 3936 | 26.8 | 2.21 | 35.62 | 3.0 | 82.3 | 16.39 | 31.39 | 50.3 | 26.8 | 2.06 | 112.38 | 12.6 | 31.0 | 2.874 | 37.63 | TULANG BELAKANG |  |
| pocket_pivot&q5:bb_lebar | 14434 | 17.74 | 1.462 | 41.37 | 2.13 | 94.5 | 12.84 | 24.19 | 40.02 | 17.74 | 0.85 | 104.77 | 10.99 | 29.0 | 1.099 | 34.7 | TULANG BELAKANG | BUNYI LATAR |
| q5:julat10 | 117747 | 22.46 | 1.851 | 38.84 | 2.67 | 70.0 | 14.25 | 28.0 | 46.18 | 22.46 | 1.41 | 111.13 | 12.31 | 33.0 | 1.888 | 36.13 | TULANG BELAKANG |  |
| pocket_pivot&q5:julat20 | 12028 | 20.01 | 1.65 | 39.76 | 2.24 | 93.9 | 13.48 | 26.02 | 42.77 | 20.01 | 1.11 | 112.6 | 12.55 | 28.0 | 0.921 | 33.87 | TULANG BELAKANG |  |
| q5:julat20 | 141295 | 21.6 | 1.78 | 39.54 | 2.48 | 69.4 | 13.92 | 27.34 | 45.14 | 21.6 | 1.22 | 109.0 | 11.88 | 33.0 | 1.59 | 35.24 | TULANG BELAKANG |  |
| q5:bb_lebar | 151040 | 19.56 | 1.613 | 40.97 | 2.32 | 73.9 | 13.2 | 25.66 | 42.55 | 19.56 | 1.05 | 103.14 | 10.62 | 32.0 | 1.585 | 35.42 | TULANG BELAKANG |  |
| q5:j_ema9 | 45994 | 16.93 | 1.396 | 41.73 | 2.15 | 94.2 | 12.71 | 23.69 | 38.82 | 16.93 | 0.95 | 100.33 | 10.06 | 31.0 | 1.299 | 35.22 | TULANG BELAKANG | BUNYI LATAR |
| pocket_pivot&q1:j_52w_tinggi | 6461 | 21.19 | 1.747 | 36.28 | 2.06 | 90.7 | 14.75 | 27.22 | 43.49 | 21.19 | 1.15 | 99.03 | 9.95 | 24.0 | 0.844 | 33.17 | TULANG BELAKANG |  |
| macd_cross&q1:j_52w_tinggi | 3897 | 26.69 | 2.2 | 32.85 | 2.98 | 71.2 | 17.16 | 30.98 | 48.59 | 26.69 | 1.18 | 101.78 | 10.44 | 36.0 | 2.871 | 37.41 | TULANG BELAKANG |  |
| rsi_lintas50&q1:j_52w_tinggi | 5047 | 24.43 | 2.014 | 32.83 | 2.4 | 82.7 | 16.14 | 29.51 | 44.94 | 24.43 | 1.21 | 95.71 | 9.07 | 30.0 | 1.897 | 36.85 | TULANG BELAKANG |  |
| q1:j_52w_tinggi | 101976 | 24.2 | 1.995 | 35.25 | 2.5 | 66.7 | 15.75 | 29.42 | 46.16 | 24.2 | 1.15 | 100.55 | 10.11 | 34.0 | 1.902 | 35.54 | TULANG BELAKANG |  |
| macd_cross&q1:cerun_ma50 | 4082 | 26.11 | 2.153 | 31.26 | 2.69 | 67.6 | 17.71 | 30.79 | 46.22 | 26.11 | 0.98 | 96.53 | 9.33 | 45.0 | 4.586 | 41.89 | TULANG BELAKANG |  |
| pocket_pivot&q1:cerun_ma50 | 4553 | 24.75 | 2.041 | 31.28 | 2.92 | 86.9 | 17.22 | 29.87 | 45.11 | 24.75 | 1.05 | 104.28 | 10.96 | 39.0 | 4.735 | 42.28 | TULANG BELAKANG |  |
| rsi_lintas50&q1:cerun_ma50 | 4755 | 23.87 | 1.968 | 30.81 | 2.48 | 83.3 | 16.89 | 28.93 | 44.22 | 23.87 | 0.9 | 92.04 | 8.05 | 40.0 | 4.33 | 42.78 | TULANG BELAKANG |  |
| q1:cerun_ma50 | 83552 | 25.88 | 2.134 | 31.26 | 2.78 | 66.7 | 17.49 | 30.62 | 46.51 | 25.88 | 0.97 | 98.62 | 9.69 | 44.0 | 4.53 | 42.0 | TULANG BELAKANG |  |
| macd_cross&q1:j_ma200 | 4334 | 22.87 | 1.885 | 32.97 | 2.49 | 68.8 | 16.07 | 28.35 | 43.51 | 22.87 | 0.72 | 89.65 | 7.66 | 41.0 | 3.335 | 40.19 | TULANG BELAKANG |  |
| pocket_pivot&q1:j_ma200 | 4820 | 20.31 | 1.674 | 33.82 | 2.1 | 88.4 | 15.31 | 26.59 | 40.89 | 20.31 | 0.77 | 90.36 | 7.88 | 33.0 | 2.128 | 38.59 | TULANG BELAKANG |  |


Taburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. p90 dan % ≥ 100% ialah pembeza, bukan median.


**Lift jatuh besar antara Step 4 dan Step 7** (contoh `rsi_lintas50&q5:atr_pct`: lift 13.02 dalam populasi peristiwa → lift_tepat 2.37 atas semua hari universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. Angka Step 7 yang lebih dekat dengan dagangan sebenar.


### Penapis Step 7.4
160 kombinasi signal × penapis diuji (0 lulus kriteria "buang ≥ 30% palsu dan ≤ 10% benar").


**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis dipradaftar. Ini keputusan negatif yang bersih.


10 contoh penapis terbaik (ikut % palsu dibuang):


| signal | buang_palsu_pct | buang_benar_pct |
|---|---|---|
| macd_cross&q1:j_ma200 | penapis:lapis_ge_3 | 99.5 | 99.8 |
| macd_cross&q1:cerun_ma50 | penapis:lapis_ge_3 | 99.1 | 99.3 |
| pocket_pivot&q1:j_ma200 | penapis:lapis_ge_3 | 98.0 | 99.0 |
| q1:cerun_ma50 | penapis:lapis_ge_3 | 96.8 | 97.5 |
| rsi_lintas50&q1:cerun_ma50 | penapis:lapis_ge_3 | 96.6 | 97.0 |
| macd_cross&q1:cerun_ma50 | penapis:harga_atas_ma50 | 94.2 | 93.3 |
| macd_cross&q1:j_52w_tinggi | penapis:lapis_ge_3 | 92.2 | 96.5 |
| pocket_pivot&q1:cerun_ma50 | penapis:lapis_ge_3 | 91.4 | 91.6 |
| rsi_lintas50&q1:j_52w_tinggi | penapis:lapis_ge_3 | 91.3 | 95.1 |
| q1:j_52w_tinggi | penapis:lapis_ge_3 | 91.1 | 94.7 |


## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)

Set kemasukan: gabungan semua kemunculan 18 signal yang lulus Step 7 = 247,287 (ticker, tarikh) unik, disampel berlapis ikut bulan ke **24,000** (benih 42; SPEC §13.9). Grid 18 HOLD × 13 EXIT = **234** sistem.


### TIGA RUJUKAN WAJIB

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_menang | purata_kalah | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 | pct_terpotong_data | siri_kalah_terpanjang |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 24000 | 9.85 | 16.25 | 16.246 | 59.28 | 45.98 | 27.05 | 252.0 | -19.65 | 0.0 | 100.0 | 0.0 | 10 |
| REF_jual_hari63 | 24000 | 1.65 | 2.86 | 2.861 | 53.31 | 19.43 | 16.06 | 63.0 | -10.82 | 79.5 | 0.0 | 0.0 | 25 |
| REF_chandelier_4atr | 24000 | -4.61 | 1.51 | 1.507 | 39.39 | 22.02 | 11.82 | 54.7 | -8.18 | 80.1 | 0.5 | 0.0 | 33 |


**Keputusan: rujukan "pegang tanpa jual hingga hari ke-252" menang, dan 0 / 234 sistem mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = 16.246%). Mengikut arahan Step 7b.4, jawapan kajian ialah **"jangan jual"** — dan itu dilaporkan sebagai penemuan, bukan kegagalan.


### 15 sistem terbaik daripada 234

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 |
|---|---|---|---|---|---|---|---|---|---|
| rsi_70_60|X=12%,Y=ma50 | 24000 | 3.21 | 6.06 | 6.061 | 58.18 | 101.4 | -8.77 | 65.0 | 9.7 |
| rsi_70_60|X=20%,Y=ma50 | 24000 | 2.82 | 5.99 | 5.995 | 57.27 | 109.1 | -9.14 | 62.9 | 12.1 |
| rsi_70_60|X=10%,Y=ma50 | 24000 | 3.44 | 5.98 | 5.976 | 58.8 | 96.2 | -8.48 | 66.4 | 8.3 |
| rsi_70_60|X=15%,Y=ma50 | 24000 | 2.91 | 5.91 | 5.912 | 57.46 | 106.0 | -9.01 | 63.7 | 11.0 |
| rsi_70_60|X=7%,Y=ma50 | 24000 | 3.93 | 5.32 | 5.316 | 59.95 | 85.2 | -7.69 | 68.9 | 6.2 |
| rsi_70_60|X=20%,Y=ema21 | 24000 | 3.6 | 5.04 | 5.045 | 59.7 | 78.3 | -7.0 | 69.8 | 4.9 |
| rsi_70_60|X=5%,Y=ma50 | 24000 | 4.19 | 5.02 | 5.024 | 60.82 | 77.4 | -7.1 | 70.2 | 5.0 |
| rsi_70_60|X=10%,Y=ema21 | 24000 | 3.63 | 4.99 | 4.988 | 59.77 | 77.3 | -6.95 | 70.0 | 4.8 |
| rsi_70_60|X=12%,Y=ema21 | 24000 | 3.59 | 4.98 | 4.977 | 59.68 | 77.7 | -6.99 | 70.1 | 4.9 |
| rsi_70_60|X=15%,Y=ema21 | 24000 | 3.58 | 4.96 | 4.961 | 59.62 | 78.1 | -7.0 | 69.8 | 4.9 |
| rsi_70_60|X=7%,Y=ema21 | 24000 | 3.71 | 4.92 | 4.915 | 60.09 | 76.0 | -6.85 | 70.3 | 4.7 |
| rsi_70_60|X=5%,Y=ema21 | 24000 | 3.93 | 4.89 | 4.888 | 60.68 | 74.3 | -6.66 | 70.4 | 4.6 |
| rsi_70_60|X=5%,Y=ema9 | 24000 | 3.82 | 4.85 | 4.854 | 60.78 | 71.5 | -6.25 | 70.7 | 4.5 |
| rsi_70_60|X=7%,Y=ema9 | 24000 | 3.79 | 4.85 | 4.852 | 60.76 | 71.7 | -6.25 | 70.7 | 4.5 |
| rsi_70_60|X=20%,Y=ema9 | 24000 | 3.77 | 4.85 | 4.847 | 60.74 | 71.7 | -6.25 | 70.7 | 4.6 |


Perhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.


## 10. Step 8 — kawalan kebetulan

### Ujian label rawak dan FDR per keluarga

| keluarga | N | lulus_fdr | ambang_p |
|---|---|---|---|
| ENTRY/PADU | 20 | 7 | 0.000999000999000999 |
| ENTRY/SUPER PADU | 20 | 5 | 0.001998001998001998 |
| HOLD | 18 | 0 |  |
| EXIT | 64 | 0 |  |
| SISTEM | 234 | 0 |  |


Perbandingan yang diminta arahan: **7 signal lulus FDR daripada 20 diuji**, manakala label rawak menghasilkan lift purata yang jauh lebih rendah (lajur `lift_purata_rawak` dalam `kawalan_rawak_bootstrap_2023.csv`).


### Jangkaan atas SEMUA kemunculan + ujian outlier

| signal | n_kemunculan | median_pulangan | jangkaan | jangkaan_tanpa_5pct_teratas | pct_rugi_lebih_10 | siri_kalah_terpanjang | jangkaan_bawah95_blok_ticker | jangkaan_bawah95_blok_minggu |
|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | 4738 | -9.92 | 1.542 | -2.746 | 49.3 | 33 | 0.517 | -0.601 |
| rsi_lintas50&q5:julat20 | 4358 | -8.67 | 2.317 | -1.925 | 41.0 | 27 | 1.271 | 0.054 |
| q5:atr_pct | 95479 | -9.95 | 1.526 | -2.682 | 49.6 | 203 | 0.857 | -0.615 |
| rsi_lintas50&q5:bb_lebar | 3936 | -7.89 | 2.874 | -1.305 | 37.1 | 17 | 1.835 | 0.347 |
| pocket_pivot&q5:bb_lebar | 14434 | -6.56 | 1.099 | -2.013 | 25.5 | 51 | 0.518 | -1.025 |
| q5:julat10 | 117747 | -7.7 | 1.888 | -1.875 | 35.4 | 155 | 1.336 | -0.284 |
| pocket_pivot&q5:julat20 | 12028 | -7.43 | 0.921 | -2.435 | 30.6 | 48 | 0.228 | -1.291 |
| q5:julat20 | 141295 | -7.64 | 1.59 | -2.056 | 33.9 | 233 | 1.074 | -0.371 |
| q5:bb_lebar | 151040 | -6.82 | 1.585 | -1.881 | 29.2 | 166 | 1.131 | -0.368 |
| q5:j_ema9 | 45994 | -6.36 | 1.299 | -1.875 | 23.9 | 85 | 0.821 | -0.65 |
| pocket_pivot&q1:j_52w_tinggi | 6461 | -7.6 | 0.844 | -2.685 | 31.9 | 51 | -0.124 | -1.241 |
| macd_cross&q1:j_52w_tinggi | 3897 | -7.09 | 2.871 | -0.744 | 31.2 | 18 | 2.185 | 0.387 |
| rsi_lintas50&q1:j_52w_tinggi | 5047 | -6.99 | 1.897 | -1.553 | 29.9 | 34 | 1.048 | -0.008 |
| q1:j_52w_tinggi | 101976 | -7.43 | 1.902 | -1.709 | 32.6 | 325 | 1.314 | -0.142 |
| macd_cross&q1:cerun_ma50 | 4082 | -5.24 | 4.586 | 1.24 | 21.9 | 15 | 3.966 | 1.232 |
| pocket_pivot&q1:cerun_ma50 | 4553 | -5.21 | 4.735 | 1.267 | 21.5 | 26 | 3.783 | 1.896 |
| rsi_lintas50&q1:cerun_ma50 | 4755 | -4.9 | 4.33 | 1.146 | 19.1 | 19 | 3.592 | 1.943 |
| q1:cerun_ma50 | 83552 | -5.35 | 4.53 | 1.091 | 23.2 | 180 | 3.997 | 2.036 |
| macd_cross&q1:j_ma200 | 4334 | -5.37 | 3.335 | 0.202 | 22.7 | 18 | 2.802 | 0.525 |
| pocket_pivot&q1:j_ma200 | 4820 | -5.91 | 2.128 | -0.89 | 23.4 | 30 | 1.247 | -0.095 |


### Keputusan gate demi gate

| signal | G1_sah_dalam_tahun | G2_merentas_tahun | G3_nilai_p | G3_fdr | G4_bootstrap | G5_outlier | G6 | step7 | keputusan |
|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:atr_pct | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=LANGKA; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:julat20 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.66633 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:atr_pct | LULUS | LULUS (2/5 tahun lain LULUS GATE KERAS: [2020, 2025]; kelas: 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:bb_lebar | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.64835 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q5:bb_lebar | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=LANGKA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.80519 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q5:julat10 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=-; 2021=-; 2022=-; 2024=SEDERHANA; 2025=-) | 0.51548 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | STATISTIK SAHAJA | LULUS | DITOLAK |
| pocket_pivot&q5:julat20 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.87113 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:julat20 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.47952 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:bb_lebar | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2024=SEDERHANA; 2025=TERAS) | 0.33966 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:j_ema9 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.66533 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| pocket_pivot&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=LANGKA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q1:j_52w_tinggi | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | LULUS | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q1:cerun_ma50 | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2020=LANGKA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| pocket_pivot&q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.8042 | GAGAL | GAGAL | LULUS | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.71329 | GAGAL | GAGAL | LULUS | LULUS | LULUS | DITOLAK |
| q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini COMMON BIASA, bukan penemuan; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TERAS) | 0.47153 | GAGAL | GAGAL | LULUS | LULUS | LULUS | DITOLAK |
| macd_cross&q1:j_ma200 | SEBAHAGIAN | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.79221 | GAGAL | GAGAL | LULUS | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:j_ma200 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=LANGKA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.85215 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |


**DITERIMA: 0** · **CALON: 1** — `macd_cross&q1:cerun_ma50` · **DITOLAK: 19.**


Penapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam ≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada 2023.


## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)

Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. Asas signal ENTRY: **CALON selepas Step 8**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → RS 6 bulan → ticker.


| sistem | n_posisi_dibuka | n_dagangan_ditutup | n_posisi_terbuka_hujung_tahun | purata_slot_terisi | pulangan_tahun | median_bulanan | purata_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terbaik | bulan_terburuk | mdd | purata_hari_pegang | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 8 | 0 | 8 | 7.94 | 24.72 | 3.44 | 2.1 | 25.0 | 58.3 | 12.13 | -8.39 | -21.11 |  | 0.7 | 26.71 | -9.97 |
| REF_chandelier_4atr | 42 | 34 | 8 | 7.8 | 56.37 | 2.58 | 4.42 | 25.0 | 66.7 | 28.32 | -9.81 | -21.52 | 48.6 | 3.5 | 26.71 | -9.97 |
| REF_jual_hari63 | 35 | 32 | 3 | 7.81 | 21.14 | 1.78 | 1.91 | 25.0 | 58.3 | 14.01 | -10.08 | -21.76 | 63.0 | 2.9 | 26.71 | -9.97 |
| rsi_70_60|X=12%,Y=ma50 | 19 | 11 | 8 | 7.89 | 35.22 | 0.88 | 2.81 | 25.0 | 50.0 | 15.9 | -6.2 | -17.24 | 94.9 | 1.6 | 26.71 | -9.97 |
| rsi_70_60|X=20%,Y=ma50 | 21 | 13 | 8 | 7.88 | 31.84 | 2.22 | 2.61 | 25.0 | 50.0 | 13.43 | -7.51 | -18.1 | 85.1 | 1.8 | 26.71 | -9.97 |
| rsi_70_60|X=10%,Y=ma50 | 19 | 11 | 8 | 7.89 | 35.22 | 0.88 | 2.81 | 25.0 | 50.0 | 15.9 | -6.2 | -17.24 | 94.9 | 1.6 | 26.71 | -9.97 |
| KAWALAN_RAWAK|pegang_252 | 8 | 0 | 8 | 7.94 | 9.22 | -1.06 | 1.05 | 16.7 | 50.0 | 16.1 | -8.99 | -26.75 |  | 0.7 | 26.71 | -9.97 |
| KAWALAN_RAWAK|chandelier | 42 | 34 | 8 | 7.8 | 10.72 | -0.59 | 1.13 | 16.7 | 50.0 | 12.93 | -11.18 | -23.6 | 47.9 | 3.5 | 26.71 | -9.97 |


### Pulangan bulanan penuh (%)

| tarikh | REF_pegang_252 | REF_chandelier_4atr | REF_jual_hari63 | rsi_70_60|X=12%,Y=ma50 | rsi_70_60|X=20%,Y=ma50 | rsi_70_60|X=10%,Y=ma50 | KAWALAN_RAWAK|pegang_252 | KAWALAN_RAWAK|chandelier |
|---|---|---|---|---|---|---|---|---|
| 2023-01-31 | 11.5 | 11.14 | 11.5 | 11.5 | 11.5 | 11.5 | 11.8 | 11.8 |
| 2023-02-28 | -5.88 | -7.24 | -5.88 | -5.91 | -6.51 | -5.91 | -5.38 | -6.25 |
| 2023-03-31 | 1.54 | 4.17 | 1.54 | -1.34 | -0.43 | -1.34 | -3.1 | -1.53 |
| 2023-04-30 | -0.38 | 0.2 | -4.02 | 3.09 | 4.87 | 3.09 | 3.95 | 0.34 |
| 2023-05-31 | 5.33 | 0.99 | 2.02 | -2.64 | -3.08 | -2.64 | -7.88 | -2.63 |
| 2023-06-30 | 10.1 | 9.5 | 6.39 | 8.24 | 8.45 | 8.24 | 7.39 | 7.0 |
| 2023-07-31 | 5.6 | 4.25 | 3.11 | 4.45 | 5.83 | 4.45 | 0.98 | 6.89 |
| 2023-08-31 | -6.05 | -9.81 | -4.23 | -3.5 | -6.49 | -3.5 | -8.99 | -5.06 |
| 2023-09-30 | -8.39 | -6.54 | -5.26 | -6.2 | -7.51 | -6.2 | -4.28 | -6.43 |
| 2023-10-31 | -5.89 | -6.21 | -10.08 | -2.8 | -2.0 | -2.8 | -6.79 | -11.18 |
| 2023-11-30 | 5.62 | 28.32 | 13.76 | 15.9 | 13.25 | 15.9 | 16.1 | 7.73 |
| 2023-12-31 | 12.13 | 24.24 | 14.01 | 12.9 | 13.43 | 12.9 | 8.84 | 12.93 |


### Jawapan terus kepada sasaran +10% sebulan

**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:


- `REF_pegang_252`: median bulanan **3.44%**, 25.0% bulan ≥ +10%, bulan terburuk -8.39%, MDD -21.11%, pulangan tahun 24.72% (SPY 26.71%, MDD SPY -9.97%)

- `REF_chandelier_4atr`: median bulanan **2.58%**, 25.0% bulan ≥ +10%, bulan terburuk -9.81%, MDD -21.52%, pulangan tahun 56.37% (SPY 26.71%, MDD SPY -9.97%)

- `REF_jual_hari63`: median bulanan **1.78%**, 25.0% bulan ≥ +10%, bulan terburuk -10.08%, MDD -21.76%, pulangan tahun 21.14% (SPY 26.71%, MDD SPY -9.97%)

- `rsi_70_60|X=12%,Y=ma50`: median bulanan **0.88%**, 25.0% bulan ≥ +10%, bulan terburuk -6.20%, MDD -17.24%, pulangan tahun 35.22% (SPY 26.71%, MDD SPY -9.97%)

- `rsi_70_60|X=20%,Y=ma50`: median bulanan **2.22%**, 25.0% bulan ≥ +10%, bulan terburuk -7.51%, MDD -18.10%, pulangan tahun 31.84% (SPY 26.71%, MDD SPY -9.97%)

- `rsi_70_60|X=10%,Y=ma50`: median bulanan **0.88%**, 25.0% bulan ≥ +10%, bulan terburuk -6.20%, MDD -17.24%, pulangan tahun 35.22% (SPY 26.71%, MDD SPY -9.97%)

- `KAWALAN_RAWAK|pegang_252`: median bulanan **-1.06%**, 16.7% bulan ≥ +10%, bulan terburuk -8.99%, MDD -26.75%, pulangan tahun 9.22% (SPY 26.71%, MDD SPY -9.97%)

- `KAWALAN_RAWAK|chandelier`: median bulanan **-0.59%**, 16.7% bulan ≥ +10%, bulan terburuk -11.18%, MDD -23.60%, pulangan tahun 10.72% (SPY 26.71%, MDD SPY -9.97%)


**Apa yang menghalang — kapasiti, bukan kadar menang.**

- Sistem terbaik (`REF_pegang_252`) hanya membuka **8 posisi sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh dijadikan asas keputusan.

- Sistem yang pusing ganti mencukupi (Chandelier: 42 posisi, 3.5/bulan) memberi median bulanan hanya 2.58% dengan MDD -21.52% — lebih buruk daripada MDD SPY.

- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.

- KAWALAN RAWAK pegang-252 memberi 9.22% dan Chandelier rawak 10.72% — dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.


### Banding wajib: SPY dan KAWALAN RAWAK

- SPY tempoh sama: **26.71%** (MDD -9.97%). **2/6** sistem kalah kepada SPY.

- KAWALAN RAWAK terbaik: **10.72%** (`KAWALAN_RAWAK|chandelier`). **0/6** sistem kalah kepada entri rawak.


> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.


## 12. Keputusan akhir (had fasa: CALON)

1. **ENTRY** — 1 signal CALON: `macd_cross&q1:cerun_ma50`. Tiada pemicu klasik tunggal lulus. Hipotesis "magnitud ada pada konteks, bukan pemicu" disokong oleh data 2023.

2. **HOLD** — 0/18 signal lulus FDR; kelas pullback ialah hasil paling kukuh (SIHAT 91.5% / PASARAN 80.0% menyambung ke puncak baru lawan AMARAN 46.2%).

3. **EXIT** — 0/64 signal lulus FDR; 0/234 sistem mengalahkan ketiga-tiga rujukan dan 0/234 lulus FDR keluarga SISTEM. **Jawapan kajian tahun ini: jangan jual.**

4. **PORTFOLIO** — sasaran +10% sebulan tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila pegangan panjang, bukan kadar menang.

5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam ≥ 2 tahun LAIN; tahun lain yang siap: [2020, 2021, 2022, 2024, 2025]. Lihat `BANDING_TAHUN.md` untuk status merentas tahun.


## 13. Fail output

| Fail | Isi |
|---|---|
| `runs_2023.csv` | 4048 run, 34 lajur |
| `monthly_summary_2023.csv` | ringkasan 12 bulan |
| `skipped_2023.csv` | 14960 calon ditolak + sebab |
| `kohort_masih_naik_2023.csv` | 420 run masih_naik dijejak 252 hari |
| `common_unique_2023.csv` | 3440 baris (213 signal × subset × populasi × kumpulan × keluarga) |
| `taburan_indikator_2023.csv` | median + p25/p75 setiap indikator setiap hasil |
| `hold_exit_2023.csv` | 361 baris CALON HOLD/EXIT |
| `false_signal_2023.csv` | 180 baris (signal + penapis) |
| `hadapan_hold_exit_2023.csv` | 237 sistem (234 + 3 rujukan) |
| `kawalan_rawak_bootstrap_2023.csv` | nilai-p label rawak + had bawah bootstrap |
| `jangkaan_kemunculan_2023.csv` | jangkaan + ujian outlier |
| `keputusan_2023.csv` | keputusan gate demi gate |
| `portfolio_2023.csv`, `portfolio_bulanan_2023.csv` | Step 9 |
| `log_ujian.csv` | setiap signal/kombinasi yang diuji |
| `PANDANG_HADAPAN_2023.md` | imbasan pandang ke hadapan |
| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |
