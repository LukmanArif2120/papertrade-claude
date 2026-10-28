# LAPORAN REVERSE 2025 — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.

> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = **satu rejim pasaran**. Peta sektor bukan titik-masa. Gate 8.1 ada 5 tahun lain ([2020, 2021, 2022, 2023, 2024]); keputusan **maksimum CALON** (SPEC §11.8).

## 0. Jawapan ringkas

1. **4507 run layak** dikenal pasti dalam 2025; setiap 12 bulan ada calon (tiada "TIADA CALON"). 98 SUPER PADU (≥100%), 2326 PADU, 2083 BIASA.

2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada 470 run yang masih naik pada hari ke-63, **39.8% akhirnya melebihi +100%**, dengan median kenaikan penuh **87.0%** lawan 39.8% pada hari ke-63.

3. **Signal entry: 4 CALON daripada 19 yang masuk corong** — dan kesemuanya konteks **pengembangan kemeruapan**, bukan pemicu: `rsi_lintas50&q5:atr_pct`, `q5:atr_pct`, `q5:julat20`, `q5:bb_lebar`.

4. **Rujukan "pegang tanpa jual hingga hari ke-252" MENANG.** Tiada satu pun daripada 234 sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan. Jangkaan: +27.57% (pegang tanpa jual hingga hari ke-252), +6.07% (Chandelier 4×ATR14), +4.85% (jual hari ke-63). Mengikut arahan Step 7b.4, jawapan kajian tahun ini ialah **"jangan jual"**.

5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan pegang-252 hanya membuka **8 posisi sepanjang tahun** (8 slot terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. Pulangannya 128.93% ialah hasil **8 saham**, bukan sistem.

6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik ialah 5.65% sebulan (median) dengan MDD -38.71%.

7. **Keluarga EXIT dan SISTEM pada FDR:** 0/62 signal EXIT dan 0/234 sistem lulus q ≤ 0.01.

## 1. Semakan kesediaan Step 0

| Semakan | Hasil |
|---|---|
| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, 2009-01-02 → 2026-10-16; semua sha256 sepadan |
| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |
| c. Sumber sektor/industri setiap ticker | **LULUS** — 2314/2321 = 99.7% (4 kelas saham diisi daripada ticker asas; 96 ticker = `Lain-lain`) |
| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 (indeks sektor A02; diluluskan pengguna) |
| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — 0.111 s/ticker; larian penuh 2321 ticker = 257 s |
| f. `semak_hadapan` atas modul indikator | **LULUS** — 14 tarikh potong (≥ 12), 26,950 perbandingan, **0 kegagalan** (`REVERSE/PANDANG_HADAPAN_2025.md`) |

## 2. Step 1–2 — run

Saiz universe 2025 setiap bulan: min **2000**, median **2000**, maks **2000**; 2321 ticker berbeza sepanjang tahun.

| bulan | n_run | n_super | n_padu | n_biasa | n_bertangga | n_lonjakan | n_stabil | n_entry_sah | n_masih_naik | n_peristiwa | med_naik |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025-01 | 438 | 2 | 100 | 336 | 11 | 232 | 195 | 383 | 6 | 1711 | 19.1 |
| 2025-02 | 306 | 2 | 107 | 197 | 7 | 203 | 96 | 199 | 39 | 922 | 19.8 |
| 2025-03 | 483 | 10 | 233 | 240 | 6 | 338 | 139 | 280 | 109 | 1213 | 30.1 |
| 2025-04 | 947 | 16 | 696 | 235 | 175 | 394 | 378 | 419 | 333 | 1370 | 37.1 |
| 2025-05 | 138 | 5 | 71 | 62 | 13 | 68 | 57 | 101 | 38 | 610 | 31.9 |
| 2025-06 | 169 | 5 | 75 | 89 | 9 | 92 | 68 | 148 | 25 | 1267 | 26.6 |
| 2025-07 | 136 | 2 | 65 | 69 | 4 | 64 | 68 | 105 | 19 | 1151 | 29.3 |
| 2025-08 | 334 | 13 | 128 | 193 | 24 | 183 | 127 | 259 | 23 | 1337 | 25.0 |
| 2025-09 | 259 | 18 | 124 | 117 | 23 | 141 | 95 | 223 | 27 | 810 | 32.8 |
| 2025-10 | 459 | 8 | 228 | 223 | 41 | 223 | 195 | 385 | 102 | 1482 | 30.3 |
| 2025-11 | 616 | 15 | 407 | 194 | 73 | 227 | 316 | 421 | 111 | 1279 | 34.9 |
| 2025-12 | 222 | 2 | 92 | 128 | 15 | 119 | 88 | 169 | 21 | 846 | 25.0 |


Jumlah: **4507 run layak**, 3092 (68.6%) dengan `entry_sah = ya` (tiada amaran: syarat 10 hari menolak 31.4% < 50%). Dilangkau: 13507 (12580 "terlalu perlahan").


### Bucket %_naik × tempoh

| bucket_pct | <=21 | <=42 | <=63 |
|---|---|---|---|
| 10%+ | 1277 | 0 | 0 |
| 100%+ | 5 | 18 | 65 |
| 20%+ | 267 | 539 | 0 |
| 200%+ | 0 | 1 | 4 |
| 30%+ | 125 | 274 | 1260 |
| 300%+ | 0 | 2 | 3 |
| 50%+ | 38 | 104 | 525 |


### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)

| kumpulan | PANTAS | PERLAHAN | SEDANG |
|---|---|---|---|
| BIASA | 1544 | 0 | 539 |
| PADU | 163 | 1785 | 378 |
| SUPER PADU | 5 | 72 | 21 |


Sel SAMPEL KECIL: [('SUPER PADU', 'PANTAS')]


### Jenis kenaikan

| jenis | n |
|---|---|
| LONJAKAN | 2284 |
| STABIL | 1822 |
| BERTANGGA | 401 |


`graf_menaik = ya` (S3): 2050 (45.5%). `masih_naik = ya`: 853.


### 10 run terbaik setiap bulan (ikut %_naik_rendah)


**2025-01**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| HIMS | Healthcare | 2025-01-27 | 2025-02-19 | 16 | 136.22 | SUPER PADU | LONJAKAN | ya | tidak |
| RGTI | Technology | 2025-01-13 | 2025-01-21 | 5 | 134.96 | SUPER PADU | LONJAKAN | ya | tidak |
| BABA | Consumer Cyclical | 2025-01-13 | 2025-03-17 | 43 | 84.32 | PADU | STABIL | ya | tidak |
| QUBT | Technology | 2025-01-13 | 2025-01-15 | 2 | 80.19 | PADU | LONJAKAN | tidak | tidak |
| ASTS | Technology | 2025-01-13 | 2025-03-05 | 35 | 76.5 | PADU | LONJAKAN | ya | tidak |
| FUTU | Financial Services | 2025-01-13 | 2025-02-18 | 24 | 68.34 | PADU | STABIL | ya | tidak |
| TAL | Consumer Defensive | 2025-01-07 | 2025-02-13 | 25 | 65.99 | PADU | BERTANGGA | ya | tidak |
| RKT | Financial Services | 2025-01-13 | 2025-04-04 | 57 | 61.77 | PADU | STABIL | ya | tidak |
| DRUG | Healthcare | 2025-01-27 | 2025-02-10 | 10 | 61.23 | PADU | STABIL | ya | tidak |
| UPST | Financial Services | 2025-01-13 | 2025-02-12 | 21 | 60.82 | PADU | LONJAKAN | ya | tidak |


**2025-02**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| SMR | Industrials | 2025-02-25 | 2025-05-27 | 63 | 116.59 | SUPER PADU | LONJAKAN | tidak | ya |
| SMMT | Healthcare | 2025-02-25 | 2025-04-24 | 41 | 107.34 | SUPER PADU | STABIL | ya | tidak |
| WGS | Healthcare | 2025-02-07 | 2025-04-29 | 55 | 99.54 | PADU | LONJAKAN | ya | tidak |
| ROOT | Financial Services | 2025-02-24 | 2025-03-24 | 20 | 93.16 | PADU | BERTANGGA | ya | tidak |
| CMP | Basic Materials | 2025-02-11 | 2025-05-13 | 63 | 81.51 | PADU | LONJAKAN | ya | ya |
| QUBT | Technology | 2025-02-18 | 2025-05-16 | 62 | 80.76 | PADU | LONJAKAN | tidak | ya |
| OKLO | Utilities | 2025-02-25 | 2025-05-27 | 63 | 80.75 | PADU | LONJAKAN | tidak | ya |
| HIMS | Healthcare | 2025-02-25 | 2025-05-16 | 57 | 79.48 | PADU | LONJAKAN | tidak | tidak |
| AGX | Industrials | 2025-02-25 | 2025-05-27 | 63 | 77.12 | PADU | STABIL | tidak | ya |
| RGTI | Technology | 2025-02-27 | 2025-05-27 | 61 | 76.71 | PADU | LONJAKAN | tidak | ya |


**2025-03**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| SEZL | Financial Services | 2025-03-06 | 2025-06-05 | 63 | 236.44 | SUPER PADU | STABIL | tidak | ya |
| DAVE | Technology | 2025-03-07 | 2025-06-06 | 63 | 186.59 | SUPER PADU | STABIL | ya | ya |
| GRPN | Communication Services | 2025-03-12 | 2025-06-06 | 60 | 172.46 | SUPER PADU | LONJAKAN | ya | tidak |
| CAR | Industrials | 2025-03-13 | 2025-06-11 | 62 | 134.89 | SUPER PADU | BERTANGGA | ya | ya |
| LEU | Energy | 2025-03-13 | 2025-06-12 | 63 | 123.19 | SUPER PADU | STABIL | tidak | ya |
| LTBR | Industrials | 2025-03-10 | 2025-05-28 | 55 | 122.34 | SUPER PADU | LONJAKAN | ya | tidak |
| CVNA | Consumer Cyclical | 2025-03-10 | 2025-06-04 | 60 | 107.9 | SUPER PADU | STABIL | ya | tidak |
| TTMI | Technology | 2025-03-31 | 2025-06-30 | 62 | 103.69 | SUPER PADU | STABIL | tidak | ya |
| LUNR | Industrials | 2025-03-11 | 2025-05-27 | 53 | 101.92 | SUPER PADU | LONJAKAN | tidak | tidak |
| NRG | Utilities | 2025-03-10 | 2025-05-19 | 49 | 100.11 | SUPER PADU | LONJAKAN | ya | tidak |


**2025-04**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| TNXP | Healthcare | 2025-04-07 | 2025-05-29 | 36 | 195.71 | SUPER PADU | BERTANGGA | ya | tidak |
| AAOI | Technology | 2025-04-04 | 2025-07-03 | 61 | 180.16 | SUPER PADU | STABIL | tidak | ya |
| FWRD | Industrials | 2025-04-08 | 2025-07-10 | 63 | 176.74 | SUPER PADU | BERTANGGA | tidak | ya |
| ELF | Consumer Defensive | 2025-04-04 | 2025-07-03 | 61 | 162.48 | SUPER PADU | STABIL | tidak | ya |
| TPC | Industrials | 2025-04-04 | 2025-07-03 | 61 | 156.69 | SUPER PADU | STABIL | tidak | ya |
| STX | Technology | 2025-04-04 | 2025-07-02 | 60 | 138.85 | SUPER PADU | STABIL | tidak | tidak |
| ATI | Industrials | 2025-04-07 | 2025-07-08 | 62 | 123.88 | SUPER PADU | STABIL | tidak | ya |
| LIF | Technology | 2025-04-07 | 2025-07-03 | 60 | 121.4 | SUPER PADU | BERTANGGA | ya | tidak |
| VSAT | Technology | 2025-04-08 | 2025-07-03 | 59 | 117.94 | SUPER PADU | BERTANGGA | tidak | tidak |
| RBLX | Communication Services | 2025-04-07 | 2025-07-07 | 61 | 115.09 | SUPER PADU | STABIL | ya | ya |


**2025-05**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| MP | Basic Materials | 2025-05-28 | 2025-08-14 | 54 | 310.84 | SUPER PADU | BERTANGGA | ya | tidak |
| URGN | Healthcare | 2025-05-16 | 2025-08-05 | 54 | 220.74 | SUPER PADU | STABIL | tidak | tidak |
| SEDG | Technology | 2025-05-22 | 2025-08-22 | 63 | 136.55 | SUPER PADU | STABIL | ya | ya |
| INSM | Healthcare | 2025-05-22 | 2025-08-21 | 62 | 104.47 | SUPER PADU | STABIL | ya | ya |
| LQDA | Healthcare | 2025-05-29 | 2025-08-27 | 62 | 100.86 | SUPER PADU | STABIL | ya | ya |
| QURE | Healthcare | 2025-05-07 | 2025-06-06 | 21 | 71.84 | PADU | LONJAKAN | ya | tidak |
| GH | Healthcare | 2025-05-23 | 2025-08-25 | 63 | 70.19 | PADU | STABIL | ya | ya |
| IBP | Consumer Cyclical | 2025-05-08 | 2025-08-08 | 63 | 68.36 | PADU | LONJAKAN | ya | ya |
| WGS | Healthcare | 2025-05-01 | 2025-07-30 | 61 | 67.93 | PADU | LONJAKAN | tidak | ya |
| MEDP | Healthcare | 2025-05-15 | 2025-07-22 | 45 | 67.93 | PADU | LONJAKAN | ya | tidak |


**2025-06**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| DFDV | Financial Services | 2025-06-06 | 2025-06-12 | 4 | 132.92 | SUPER PADU | LONJAKAN | ya | tidak |
| AEO | Consumer Cyclical | 2025-06-13 | 2025-09-15 | 63 | 114.41 | SUPER PADU | LONJAKAN | tidak | ya |
| WLDN | Industrials | 2025-06-20 | 2025-08-14 | 38 | 109.92 | SUPER PADU | STABIL | ya | tidak |
| QBTS | Technology | 2025-06-27 | 2025-09-24 | 61 | 104.27 | SUPER PADU | STABIL | ya | ya |
| SSRM | Basic Materials | 2025-06-27 | 2025-09-26 | 63 | 100.42 | SUPER PADU | STABIL | ya | ya |
| DFDV | Financial Services | 2025-06-27 | 2025-07-16 | 12 | 89.16 | PADU | LONJAKAN | ya | tidak |
| VEON | Communication Services | 2025-06-13 | 2025-08-19 | 45 | 81.53 | PADU | STABIL | ya | tidak |
| BTDR | Technology | 2025-06-23 | 2025-09-22 | 63 | 71.37 | PADU | LONJAKAN | ya | ya |
| AMR | Basic Materials | 2025-06-25 | 2025-08-13 | 34 | 70.95 | PADU | LONJAKAN | ya | tidak |
| POWL | Industrials | 2025-06-24 | 2025-09-18 | 60 | 67.33 | PADU | BERTANGGA | ya | tidak |


**2025-07**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| RGC | Healthcare | 2025-07-02 | 2025-07-03 | 1 | 144.83 | SUPER PADU | LONJAKAN | ya | tidak |
| DRD | Basic Materials | 2025-07-08 | 2025-10-06 | 63 | 126.12 | SUPER PADU | BERTANGGA | ya | ya |
| LTBR | Industrials | 2025-07-10 | 2025-10-07 | 62 | 98.88 | PADU | LONJAKAN | ya | ya |
| SRPT | Healthcare | 2025-07-21 | 2025-10-08 | 56 | 85.56 | PADU | STABIL | ya | tidak |
| B | Basic Materials | 2025-07-17 | 2025-09-22 | 46 | 73.31 | PADU | STABIL | ya | tidak |
| NTGR | Technology | 2025-07-31 | 2025-10-09 | 49 | 66.79 | PADU | STABIL | tidak | tidak |
| MIRM | Healthcare | 2025-07-02 | 2025-09-09 | 47 | 62.23 | PADU | STABIL | ya | tidak |
| NEM | Basic Materials | 2025-07-15 | 2025-10-13 | 63 | 62.0 | PADU | STABIL | ya | ya |
| VCYT | Healthcare | 2025-07-18 | 2025-10-01 | 52 | 60.15 | PADU | BERTANGGA | tidak | tidak |
| RXST | Healthcare | 2025-07-09 | 2025-09-10 | 44 | 58.54 | PADU | STABIL | tidak | tidak |


**2025-08**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| IREN | Financial Services | 2025-08-22 | 2025-11-05 | 52 | 304.93 | SUPER PADU | STABIL | ya | tidak |
| RGTI | Technology | 2025-08-26 | 2025-10-15 | 35 | 292.07 | SUPER PADU | BERTANGGA | ya | tidak |
| MLYS | Healthcare | 2025-08-21 | 2025-11-12 | 58 | 231.21 | SUPER PADU | LONJAKAN | ya | tidak |
| GRAL | Healthcare | 2025-08-01 | 2025-10-20 | 55 | 191.49 | SUPER PADU | STABIL | tidak | tidak |
| HUT | Financial Services | 2025-08-20 | 2025-11-03 | 52 | 165.83 | SUPER PADU | STABIL | ya | tidak |
| INOD | Technology | 2025-08-20 | 2025-10-08 | 34 | 156.51 | SUPER PADU | BERTANGGA | ya | tidak |
| BTU | Energy | 2025-08-21 | 2025-10-14 | 37 | 122.59 | SUPER PADU | STABIL | ya | tidak |
| GPCR | Healthcare | 2025-08-06 | 2025-11-04 | 63 | 115.25 | SUPER PADU | BERTANGGA | ya | ya |
| ARQQ | Technology | 2025-08-20 | 2025-10-13 | 37 | 113.52 | SUPER PADU | LONJAKAN | tidak | tidak |
| IONQ | Technology | 2025-08-26 | 2025-10-13 | 33 | 112.06 | SUPER PADU | BERTANGGA | ya | tidak |


**2025-09**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| QURE | Healthcare | 2025-09-17 | 2025-10-29 | 30 | 403.14 | SUPER PADU | LONJAKAN | ya | tidak |
| PRAX | Healthcare | 2025-09-03 | 2025-10-30 | 41 | 355.47 | SUPER PADU | LONJAKAN | tidak | tidak |
| NEGG | Consumer Cyclical | 2025-09-03 | 2025-11-11 | 49 | 210.14 | SUPER PADU | STABIL | tidak | tidak |
| USAR | Basic Materials | 2025-09-08 | 2025-10-13 | 25 | 190.17 | SUPER PADU | BERTANGGA | ya | tidak |
| APLD | Technology | 2025-09-08 | 2025-10-15 | 27 | 186.93 | SUPER PADU | STABIL | ya | tidak |
| LITE | Technology | 2025-09-25 | 2025-12-24 | 63 | 173.96 | SUPER PADU | BERTANGGA | ya | ya |
| ANAB | Healthcare | 2025-09-16 | 2025-12-11 | 61 | 167.63 | SUPER PADU | STABIL | ya | ya |
| OKLO | Utilities | 2025-09-05 | 2025-10-14 | 27 | 163.05 | SUPER PADU | LONJAKAN | ya | tidak |
| MLTX | Healthcare | 2025-09-29 | 2025-12-16 | 55 | 157.82 | SUPER PADU | STABIL | tidak | tidak |
| UUUU | Energy | 2025-09-02 | 2025-10-14 | 30 | 146.29 | SUPER PADU | BERTANGGA | ya | tidak |


**2025-10**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| COGT | Healthcare | 2025-10-22 | 2025-12-12 | 36 | 196.55 | SUPER PADU | LONJAKAN | ya | tidak |
| VICR | Technology | 2025-10-21 | 2026-01-22 | 63 | 173.63 | SUPER PADU | STABIL | ya | ya |
| CSIQ | Technology | 2025-10-01 | 2025-11-14 | 32 | 155.75 | SUPER PADU | STABIL | ya | tidak |
| PL | Industrials | 2025-10-22 | 2026-01-16 | 59 | 140.43 | SUPER PADU | STABIL | ya | tidak |
| AG | Basic Materials | 2025-10-27 | 2026-01-28 | 63 | 119.13 | SUPER PADU | STABIL | ya | ya |
| ARWR | Healthcare | 2025-10-14 | 2025-12-11 | 41 | 104.62 | SUPER PADU | BERTANGGA | ya | tidak |
| FLNC | Utilities | 2025-10-02 | 2025-12-11 | 49 | 103.71 | SUPER PADU | LONJAKAN | ya | tidak |
| AEO | Consumer Cyclical | 2025-10-10 | 2026-01-06 | 59 | 100.5 | SUPER PADU | BERTANGGA | ya | tidak |
| ANF | Consumer Cyclical | 2025-10-20 | 2026-01-08 | 55 | 95.15 | PADU | LONJAKAN | tidak | tidak |
| AA | Basic Materials | 2025-10-10 | 2026-01-12 | 63 | 88.08 | PADU | STABIL | ya | ya |


**2025-11**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| SOC | Energy | 2025-11-06 | 2026-01-22 | 51 | 158.87 | SUPER PADU | LONJAKAN | tidak | tidak |
| LUNR | Industrials | 2025-11-07 | 2026-01-28 | 54 | 155.29 | SUPER PADU | STABIL | tidak | tidak |
| AAOI | Technology | 2025-11-13 | 2026-02-10 | 59 | 143.42 | SUPER PADU | LONJAKAN | ya | tidak |
| BE | Industrials | 2025-11-21 | 2026-02-25 | 63 | 129.96 | SUPER PADU | STABIL | ya | ya |
| ALB | Basic Materials | 2025-11-04 | 2026-01-27 | 56 | 121.3 | SUPER PADU | BERTANGGA | ya | tidak |
| ICHR | Technology | 2025-11-04 | 2026-01-29 | 58 | 119.25 | SUPER PADU | STABIL | tidak | tidak |
| TWST | Healthcare | 2025-11-19 | 2026-02-18 | 60 | 117.68 | SUPER PADU | BERTANGGA | ya | tidak |
| RKLB | Industrials | 2025-11-07 | 2026-01-16 | 47 | 107.94 | SUPER PADU | STABIL | tidak | tidak |
| GLW | Technology | 2025-11-21 | 2026-02-25 | 63 | 107.3 | SUPER PADU | BERTANGGA | ya | ya |
| CRML | Basic Materials | 2025-11-06 | 2026-01-23 | 52 | 106.82 | SUPER PADU | LONJAKAN | tidak | tidak |


**2025-12**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| HYMC | Basic Materials | 2025-12-11 | 2026-03-02 | 53 | 386.81 | SUPER PADU | STABIL | ya | tidak |
| ACHC | Healthcare | 2025-12-03 | 2026-03-06 | 63 | 102.85 | SUPER PADU | STABIL | tidak | ya |
| PBF | Energy | 2025-12-18 | 2026-03-20 | 62 | 94.03 | PADU | BERTANGGA | ya | ya |
| POWL | Industrials | 2025-12-17 | 2026-02-12 | 38 | 90.64 | PADU | STABIL | ya | tidak |
| NKTR | Healthcare | 2025-12-18 | 2026-03-17 | 59 | 76.11 | PADU | LONJAKAN | tidak | tidak |
| FLNC | Utilities | 2025-12-17 | 2026-02-03 | 31 | 74.4 | PADU | BERTANGGA | ya | tidak |
| MIRM | Healthcare | 2025-12-15 | 2026-02-25 | 48 | 71.78 | PADU | BERTANGGA | ya | tidak |
| SEI | Energy | 2025-12-17 | 2026-03-18 | 61 | 70.2 | PADU | STABIL | ya | ya |
| SKM | Communication Services | 2025-12-22 | 2026-02-17 | 37 | 70.04 | PADU | STABIL | ya | tidak |
| CHRD | Energy | 2025-12-26 | 2026-03-30 | 63 | 65.76 | PADU | STABIL | ya | ya |


### Semua run SUPER PADU (≥ 100%)

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|
| QURE | Healthcare | 2025-09-17 | 30 | 403.14 | LONJAKAN | ya | tidak |
| HYMC | Basic Materials | 2025-12-11 | 53 | 386.81 | STABIL | ya | tidak |
| PRAX | Healthcare | 2025-09-03 | 41 | 355.47 | LONJAKAN | tidak | tidak |
| MP | Basic Materials | 2025-05-28 | 54 | 310.84 | BERTANGGA | ya | tidak |
| IREN | Financial Services | 2025-08-22 | 52 | 304.93 | STABIL | ya | tidak |
| RGTI | Technology | 2025-08-26 | 35 | 292.07 | BERTANGGA | ya | tidak |
| SEZL | Financial Services | 2025-03-06 | 63 | 236.44 | STABIL | tidak | ya |
| MLYS | Healthcare | 2025-08-21 | 58 | 231.21 | LONJAKAN | ya | tidak |
| URGN | Healthcare | 2025-05-16 | 54 | 220.74 | STABIL | tidak | tidak |
| NEGG | Consumer Cyclical | 2025-09-03 | 49 | 210.14 | STABIL | tidak | tidak |
| COGT | Healthcare | 2025-10-22 | 36 | 196.55 | LONJAKAN | ya | tidak |
| TNXP | Healthcare | 2025-04-07 | 36 | 195.71 | BERTANGGA | ya | tidak |
| GRAL | Healthcare | 2025-08-01 | 55 | 191.49 | STABIL | tidak | tidak |
| USAR | Basic Materials | 2025-09-08 | 25 | 190.17 | BERTANGGA | ya | tidak |
| APLD | Technology | 2025-09-08 | 27 | 186.93 | STABIL | ya | tidak |
| DAVE | Technology | 2025-03-07 | 63 | 186.59 | STABIL | ya | ya |
| AAOI | Technology | 2025-04-04 | 61 | 180.16 | STABIL | tidak | ya |
| FWRD | Industrials | 2025-04-08 | 63 | 176.74 | BERTANGGA | tidak | ya |
| LITE | Technology | 2025-09-25 | 63 | 173.96 | BERTANGGA | ya | ya |
| VICR | Technology | 2025-10-21 | 63 | 173.63 | STABIL | ya | ya |
| GRPN | Communication Services | 2025-03-12 | 60 | 172.46 | LONJAKAN | ya | tidak |
| ANAB | Healthcare | 2025-09-16 | 61 | 167.63 | STABIL | ya | ya |
| HUT | Financial Services | 2025-08-20 | 52 | 165.83 | STABIL | ya | tidak |
| OKLO | Utilities | 2025-09-05 | 27 | 163.05 | LONJAKAN | ya | tidak |
| ELF | Consumer Defensive | 2025-04-04 | 61 | 162.48 | STABIL | tidak | ya |
| SOC | Energy | 2025-11-06 | 51 | 158.87 | LONJAKAN | tidak | tidak |
| MLTX | Healthcare | 2025-09-29 | 55 | 157.82 | STABIL | tidak | tidak |
| TPC | Industrials | 2025-04-04 | 61 | 156.69 | STABIL | tidak | ya |
| INOD | Technology | 2025-08-20 | 34 | 156.51 | BERTANGGA | ya | tidak |
| CSIQ | Technology | 2025-10-01 | 32 | 155.75 | STABIL | ya | tidak |
| LUNR | Industrials | 2025-11-07 | 54 | 155.29 | STABIL | tidak | tidak |
| UUUU | Energy | 2025-09-02 | 30 | 146.29 | BERTANGGA | ya | tidak |
| RGC | Healthcare | 2025-07-02 | 1 | 144.83 | LONJAKAN | ya | tidak |
| AAOI | Technology | 2025-11-13 | 59 | 143.42 | LONJAKAN | ya | tidak |
| PL | Industrials | 2025-10-22 | 59 | 140.43 | STABIL | ya | tidak |
| SYRE | Healthcare | 2025-09-22 | 56 | 138.95 | STABIL | ya | tidak |
| STX | Technology | 2025-04-04 | 60 | 138.85 | STABIL | tidak | tidak |
| SEDG | Technology | 2025-05-22 | 63 | 136.55 | STABIL | ya | ya |
| HIMS | Healthcare | 2025-01-27 | 16 | 136.22 | LONJAKAN | ya | tidak |
| RGTI | Technology | 2025-01-13 | 5 | 134.96 | LONJAKAN | ya | tidak |
| CAR | Industrials | 2025-03-13 | 62 | 134.89 | BERTANGGA | ya | ya |
| DFDV | Financial Services | 2025-06-06 | 4 | 132.92 | LONJAKAN | ya | tidak |
| BE | Industrials | 2025-11-21 | 63 | 129.96 | STABIL | ya | ya |
| ASTS | Technology | 2025-09-19 | 18 | 128.54 | BERTANGGA | ya | tidak |
| SEI | Energy | 2025-09-09 | 62 | 126.16 | STABIL | ya | ya |
| DRD | Basic Materials | 2025-07-08 | 63 | 126.12 | BERTANGGA | ya | ya |
| ATI | Industrials | 2025-04-07 | 62 | 123.88 | STABIL | tidak | ya |
| LEU | Energy | 2025-03-13 | 63 | 123.19 | STABIL | tidak | ya |
| BTU | Energy | 2025-08-21 | 37 | 122.59 | STABIL | ya | tidak |
| LTBR | Industrials | 2025-03-10 | 55 | 122.34 | LONJAKAN | ya | tidak |
| LIF | Technology | 2025-04-07 | 60 | 121.4 | BERTANGGA | ya | tidak |
| ALB | Basic Materials | 2025-11-04 | 56 | 121.3 | BERTANGGA | ya | tidak |
| ICHR | Technology | 2025-11-04 | 58 | 119.25 | STABIL | tidak | tidak |
| AG | Basic Materials | 2025-10-27 | 63 | 119.13 | STABIL | ya | ya |
| VSAT | Technology | 2025-04-08 | 59 | 117.94 | BERTANGGA | tidak | tidak |
| TWST | Healthcare | 2025-11-19 | 60 | 117.68 | BERTANGGA | ya | tidak |
| SMR | Industrials | 2025-02-25 | 63 | 116.59 | LONJAKAN | tidak | ya |
| GPCR | Healthcare | 2025-08-06 | 63 | 115.25 | BERTANGGA | ya | ya |
| RBLX | Communication Services | 2025-04-07 | 61 | 115.09 | STABIL | ya | ya |
| AEO | Consumer Cyclical | 2025-06-13 | 63 | 114.41 | LONJAKAN | tidak | ya |


(dipaparkan 60 teratas daripada 98)


### Run BERTANGGA (S2) — 40 teratas

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | bilangan_kaki | pct_hari_atas_ema21 | kumpulan |
|---|---|---|---|---|---|---|---|
| MP | Basic Materials | 2025-05-28 | 54 | 310.84 | 5 | 92.5 | SUPER PADU |
| RGTI | Technology | 2025-08-26 | 35 | 292.07 | 3 | 85.7 | SUPER PADU |
| TNXP | Healthcare | 2025-04-07 | 36 | 195.71 | 3 | 66.7 | SUPER PADU |
| USAR | Basic Materials | 2025-09-08 | 25 | 190.17 | 3 | 100.0 | SUPER PADU |
| FWRD | Industrials | 2025-04-08 | 63 | 176.74 | 4 | 60.9 | SUPER PADU |
| LITE | Technology | 2025-09-25 | 63 | 173.96 | 6 | 92.1 | SUPER PADU |
| INOD | Technology | 2025-08-20 | 34 | 156.51 | 2 | 100.0 | SUPER PADU |
| UUUU | Energy | 2025-09-02 | 30 | 146.29 | 2 | 100.0 | SUPER PADU |
| CAR | Industrials | 2025-03-13 | 62 | 134.89 | 3 | 90.6 | SUPER PADU |
| ASTS | Technology | 2025-09-19 | 18 | 128.54 | 2 | 100.0 | SUPER PADU |
| DRD | Basic Materials | 2025-07-08 | 63 | 126.12 | 2 | 90.9 | SUPER PADU |
| LIF | Technology | 2025-04-07 | 60 | 121.4 | 2 | 96.2 | SUPER PADU |
| ALB | Basic Materials | 2025-11-04 | 56 | 121.3 | 4 | 100.0 | SUPER PADU |
| VSAT | Technology | 2025-04-08 | 59 | 117.94 | 2 | 63.3 | SUPER PADU |
| TWST | Healthcare | 2025-11-19 | 60 | 117.68 | 5 | 93.1 | SUPER PADU |
| GPCR | Healthcare | 2025-08-06 | 63 | 115.25 | 4 | 91.7 | SUPER PADU |
| IONQ | Technology | 2025-08-26 | 33 | 112.06 | 3 | 93.9 | SUPER PADU |
| NXT | Technology | 2025-08-15 | 57 | 108.0 | 3 | 98.2 | SUPER PADU |
| UI | Technology | 2025-08-20 | 51 | 107.47 | 2 | 100.0 | SUPER PADU |
| GLW | Technology | 2025-11-21 | 63 | 107.3 | 2 | 88.5 | SUPER PADU |
| BKSY | Industrials | 2025-09-10 | 25 | 105.79 | 3 | 100.0 | SUPER PADU |
| ARWR | Healthcare | 2025-10-14 | 41 | 104.62 | 4 | 92.7 | SUPER PADU |
| CVI | Energy | 2025-04-07 | 63 | 104.5 | 2 | 96.4 | SUPER PADU |
| ESTA | Healthcare | 2025-08-12 | 63 | 102.97 | 2 | 71.9 | SUPER PADU |
| ENTG | Technology | 2025-11-20 | 55 | 102.89 | 2 | 83.7 | SUPER PADU |
| IAG | Basic Materials | 2025-11-04 | 57 | 102.67 | 2 | 96.4 | SUPER PADU |
| AEO | Consumer Cyclical | 2025-10-10 | 59 | 100.5 | 3 | 98.0 | SUPER PADU |
| MU | Technology | 2025-04-04 | 54 | 100.3 | 2 | 76.4 | SUPER PADU |
| LEU | Energy | 2025-09-12 | 23 | 98.27 | 2 | 100.0 | PADU |
| ARWR | Healthcare | 2025-04-07 | 63 | 97.28 | 5 | 65.6 | PADU |
| BEAM | Healthcare | 2025-08-21 | 41 | 96.28 | 2 | 100.0 | PADU |
| MUX | Basic Materials | 2025-11-07 | 54 | 94.57 | 2 | 85.1 | PADU |
| PBF | Energy | 2025-12-18 | 62 | 94.03 | 4 | 92.5 | PADU |
| FUTU | Financial Services | 2025-04-08 | 63 | 93.91 | 5 | 78.1 | PADU |
| ROOT | Financial Services | 2025-02-24 | 20 | 93.16 | 2 | 100.0 | PADU |
| STM | Technology | 2025-04-08 | 63 | 92.71 | 3 | 100.0 | PADU |
| AS | Consumer Cyclical | 2025-04-08 | 55 | 92.38 | 2 | 80.4 | PADU |
| PBF | Energy | 2025-04-07 | 63 | 91.81 | 3 | 62.5 | PADU |
| COHR | Technology | 2025-09-04 | 63 | 89.96 | 4 | 93.7 | PADU |
| CDE | Basic Materials | 2025-11-04 | 54 | 89.48 | 3 | 67.3 | PADU |


(daripada 401 run BERTANGGA)


### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)

n peristiwa PADU dalam S2, populasi keputusan (a) = **189** (rujukan: semua peristiwa = 995). < 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat.


Peristiwa sah: **13998** (populasi keputusan 5354).


## 3. Step 2b — kohort "naik dan naik"

Dijejak 470 run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari tarikh_sah.


| Metrik | Nilai |
|---|---|
| % akhirnya melebihi +100% | **39.8%** |
| median %_naik_penuh | **87.0%** |
| median %_naik pada hari ke-63 | 39.8% |
| median hari ke puncak penuh | 180 |
| median MFE 252 selepas kos | 67.9% |
| median MAE 252 | -5.4% |
| median hari pegang Chandelier 4×ATR | 82 |
| median pulangan Chandelier selepas kos | 18.6% |
| terpotong hujung data | 32.6% |


Exit yang menyala dahulu:


| exit | n |
|---|---|
| bawah_ma50 | 172 |
| bawah_ema9 | 132 |
| bawah_ema21 | 67 |
| hist_neg3 | 53 |
| rsi_70_60 | 24 |
| hari_agihan | 15 |
| macd_bawah | 6 |
| trail_8pct | 1 |


### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari

| kohort | n | median_naik_63 | pct_bertangga | pct_super | median_hari_ke_puncak |
|---|---|---|---|---|---|
| masih_naik = ya | 470 | 39.8 | 23.0 | 4.5 | 63.0 |
| reda dalam 63 hari | 2622 | 24.4 | 6.8 | 1.7 | 22.0 |


Kohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya diketahui pada hari ke-63.


## 4. Step 3 — populasi kuintil dan dedup

POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **7158** baris. Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **31** daripada 41; dibuang 10.


| buang | kerana | rho |
|---|---|---|
| j_ma150 | j_ma200 | 0.96 |
| cerun_ema21 | j_ma50 | 0.818 |
| cerun_ma200 | j_ma200 | 0.837 |
| rsi14 | j_ma50 | 0.831 |
| roc60 | cerun_ma50 | 0.926 |
| willr14 | stoch_k | 1.0 |
| julat10 | atr_pct | 0.836 |
| bb_pctb | cci20 | 0.909 |
| kelt_pos | j_ema21 | 0.911 |
| j_52w_rendah | j_ma200 | 0.807 |


Signal dibina: **213** (31 binari + 62 hujung kuintil + 120 pemicu × 1 konteks).


## 5. Step 4 — common & unique (ENTRY)

Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. N ujian ENTRY sebenar (populasi a, kumpulan A) = **852** baris (213 signal × 2 subset × 2 keluarga).


### Kelas (S2, kumpulan A, keluarga PADU)

| kelas | n |
|---|---|
| TIDAK BERGUNA | 181 |
| UNIQUE | 10 |
| SEDERHANA | 9 |
| COMMON BIASA | 7 |
| LANGKA | 3 |
| TERAS | 3 |


### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)

| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n | n_industri | n_minggu | purata_pct_naik_rendah | purata_hari_ke_puncak | pct_bertangga | pct_lonjakan | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | UNIQUE | 26.97 | 0.0 | 1.13 | 0.88 | 23.76 | 30.742 | 60.87 | 10.671 | 46 | 26 | 25 | 74.26 | 52.5 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:bb_lebar | UNIQUE | 29.21 | 0.0 | 1.39 | 0.78 | 21.06 | 37.573 | 57.69 | 10.114 | 52 | 30 | 28 | 70.65 | 52.9 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:atr_pct | UNIQUE | 24.72 | 0.0 | 1.26 | 0.82 | 19.602 | 30.242 | 56.52 | 9.909 | 46 | 27 | 26 | 79.2 | 52.2 | 100.0 | 0.0 |  |
| q5:atr_pct | UNIQUE | 41.57 | 0.0 | 2.9 | 20.59 | 14.334 | 2.019 | 48.89 | 8.571 | 90 | 40 | 32 | 70.37 | 51.3 | 100.0 | 0.0 |  |
| q5:julat20 | UNIQUE | 47.19 | 0.0 | 3.97 | 28.03 | 11.88 | 1.684 | 43.75 | 7.67 | 112 | 52 | 31 | 66.72 | 51.6 | 100.0 | 0.0 |  |
| q5:bb_lebar | TERAS | 51.69 | 0.0 | 5.23 | 29.9 | 9.876 | 1.728 | 38.97 | 6.832 | 136 | 61 | 40 | 63.8 | 52.0 | 100.0 | 0.0 |  |
| macd_cross&q1:j_52w_tinggi | LANGKA | 11.24 | 0.0 | 1.39 | 0.94 | 8.1 | 11.991 | 35.29 | 6.188 | 34 | 22 | 24 | 66.55 | 50.8 | 100.0 | 0.0 |  |
| q5:j_ema9 | UNIQUE | 39.33 | 0.0 | 5.67 | 10.03 | 6.93 | 3.922 | 31.3 | 5.487 | 131 | 66 | 42 | 68.72 | 50.6 | 100.0 | 0.0 |  |
| macd_cross&q1:cerun_ma50 | LANGKA | 12.36 | 0.0 | 2.27 | 0.92 | 5.445 | 13.477 | 28.0 | 4.909 | 50 | 37 | 24 | 82.78 | 51.8 | 100.0 | 0.0 |  |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 23.6 | 0.0 | 3.78 | 1.14 | 6.237 | 20.764 | 26.83 | 4.704 | 82 | 43 | 39 | 60.19 | 52.4 | 100.0 | 0.0 |  |
| pocket_pivot&q1:j_52w_tinggi | LANGKA | 12.36 | 0.0 | 2.14 | 0.98 | 5.765 | 12.652 | 26.09 | 4.573 | 46 | 31 | 29 | 59.18 | 46.1 | 100.0 | 0.0 |  |
| rsi_lintas50&q1:cerun_ma50 | UNIQUE | 26.97 | 0.0 | 5.99 | 1.12 | 4.502 | 24.154 | 21.49 | 3.767 | 121 | 60 | 44 | 62.75 | 54.3 | 100.0 | 0.0 |  |
| q1:j_52w_tinggi | UNIQUE | 35.96 | 0.0 | 8.89 | 23.07 | 4.044 | 1.559 | 19.89 | 3.486 | 176 | 64 | 47 | 59.85 | 51.1 | 100.0 | 0.0 |  |
| q1:roc20 | UNIQUE | 42.7 | 0.0 | 12.04 | 29.65 | 3.545 | 1.44 | 19.07 | 3.343 | 236 | 81 | 44 | 65.95 | 53.2 | 100.0 | 0.0 |  |
| q1:cerun_ma50 | TERAS | 53.93 | 0.0 | 16.65 | 19.98 | 3.24 | 2.7 | 16.46 | 2.885 | 316 | 89 | 50 | 56.89 | 52.9 | 100.0 | 0.0 |  |
| q1:j_ma50 | TERAS | 55.06 | 0.0 | 16.71 | 33.17 | 3.295 | 1.66 | 16.4 | 2.876 | 317 | 94 | 47 | 55.88 | 52.7 | 100.0 | 0.0 |  |


### Rujukan S1 (semua run layak)

_(tiada baris)_


### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja

S3 mengandungi 1719 run; ia **bukan keluarga carian** (tidak menambah N). 11.2% daripadanya BERTANGGA lawan 9.2% keseluruhan.


### Keluarga SUPER PADU (FDR sendiri)

| signal | kelas | K_super | lift | lift_rawak | n | tanda |
|---|---|---|---|---|---|---|
| ema_crossback&q5:atr_pct | UNIQUE | 42.86 | 84.964 | 119.429 | 15 | SAMPEL KECIL |
| pocket_pivot&q5:atr_pct | UNIQUE | 42.86 | 84.964 | 39.81 | 20 |  |
| macd_cross&q5:atr_pct | TERAS | 57.14 | 82.39 | 75.429 | 24 |  |
| ema_crossback&q5:bb_lebar | UNIQUE | 42.86 | 75.524 | 153.551 | 16 | SAMPEL KECIL |
| pocket_pivot&q5:julat20 | UNIQUE | 42.86 | 75.524 | 24.997 | 20 |  |
| ema_crossback&q5:julat20 | UNIQUE | 42.86 | 67.971 | 119.429 | 17 | SAMPEL KECIL |
| macd_cross&q5:julat20 | TERAS | 57.14 | 64.735 | 68.245 | 26 |  |
| macd_cross&q5:bb_lebar | TERAS | 57.14 | 56.643 | 62.311 | 29 |  |
| rsi_lintas50&q5:julat20 | TERAS | 57.14 | 50.349 | 65.143 | 46 |  |
| rsi_lintas50&q5:atr_pct | TERAS | 57.14 | 45.314 | 69.909 | 46 |  |
| rsi_lintas50&q5:bb_lebar | TERAS | 57.14 | 41.195 | 73.495 | 52 |  |
| pocket_pivot&q5:bb_lebar | UNIQUE | 42.86 | 37.762 | 21.497 | 29 |  |
| q5:atr_pct | TERAS | 100.0 | 34.478 | 4.856 | 90 |  |
| q5:julat20 | TERAS | 100.0 | 25.175 | 3.568 | 112 |  |
| macd_cross&q1:j_52w_tinggi | UNIQUE | 28.57 | 20.597 | 30.492 | 34 |  |
| q5:bb_lebar | TERAS | 100.0 | 19.108 | 3.344 | 136 |  |
| macd_cross&q1:cerun_ma50 | UNIQUE | 42.86 | 18.881 | 46.733 | 50 |  |
| q5:j_ema9 | TERAS | 85.71 | 15.105 | 8.548 | 131 |  |
| q1:roc20 | TERAS | 100.0 | 8.304 | 3.373 | 236 |  |
| macd_cross&q5:rs_spy_6b | LANGKA | 14.29 | 7.813 | 23.115 | 34 |  |


### PEMICU YANG TIDAK MEMBEZAKAN

Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.


| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n |
|---|---|---|---|---|---|---|---|---|---|---|
| b:donchian20 | TIDAK BERGUNA | 2.25 | 0.0 | 10.15 | 7.0 | 0.221 | 0.321 | 1.23 | 0.215 | 163 |
| b:ema_crossback | TIDAK BERGUNA | 14.61 | 100.0 | 16.39 | 3.07 | 0.146 | 4.758 | 5.78 | 1.013 | 277 |
| b:gap_and_go | TIDAK BERGUNA | 1.12 | 0.0 | 1.7 | 0.2 | 0.66 | 5.636 | 3.57 | 0.626 | 28 |
| b:macd_cross | TIDAK BERGUNA | 24.72 | 0.0 | 22.01 | 3.53 | 1.123 | 7.005 | 6.93 | 1.215 | 375 |
| b:pocket_pivot | TIDAK BERGUNA | 24.72 | 0.0 | 22.57 | 8.21 | 1.095 | 3.009 | 6.53 | 1.144 | 383 |
| b:rsi_lintas50 | COMMON BIASA | 62.92 | 100.0 | 42.5 | 5.62 | 0.629 | 11.192 | 8.16 | 1.431 | 735 |


**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis yang diuji dalam kajian ini, dan ia disokong oleh data 2025.


### Corong ke Step 7
19 signal diteruskan (had 30; layak sebelum had: 19).


## 6. Step 5 — HOLD

> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana berjaya. Semua CALON.


### Kelas pullback

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| AMARAN | 4790 | 50.8 | -16.69 | 10.9 |
| PULLBACK PASARAN | 311 | 92.0 | -9.1 | 7.1 |
| PULLBACK SIHAT | 1394 | 88.9 | -8.1 | 6.0 |


Pullback yang trend sahamnya utuh (SIHAT 88.9%, PASARAN 92.0%) menyambung ke puncak baru jauh lebih kerap daripada pullback AMARAN (50.8%). Ini sokongan paling jelas bagi falsafah "pegang selagi naik".


### Grid 18 peraturan HOLD (deskriptif)

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| X=5%,Y=ema9 | 4 | 100.0 | -5.0 | 6.2 |
| X=5%,Y=ema21 | 1890 | 91.6 | -7.28 | 5.4 |
| X=5%,Y=ma50 | 2705 | 88.8 | -8.61 | 6.7 |
| X=7%,Y=ema9 | 1494 | 93.6 | -5.92 | 5.3 |
| X=7%,Y=ema21 | 2251 | 91.7 | -7.1 | 5.6 |
| X=7%,Y=ma50 | 2969 | 89.4 | -8.39 | 6.6 |
| X=10%,Y=ema9 | 2752 | 90.0 | -7.02 | 6.2 |
| X=10%,Y=ema21 | 2964 | 89.6 | -7.44 | 6.3 |
| X=10%,Y=ma50 | 3381 | 88.2 | -8.41 | 6.9 |
| X=12%,Y=ema9 | 3300 | 87.8 | -7.67 | 6.8 |
| X=12%,Y=ema21 | 3399 | 87.6 | -7.89 | 6.8 |
| X=12%,Y=ma50 | 3668 | 86.6 | -8.61 | 7.2 |
| X=15%,Y=ema9 | 3912 | 84.0 | -8.57 | 7.5 |
| X=15%,Y=ema21 | 3950 | 83.9 | -8.66 | 7.5 |
| X=15%,Y=ma50 | 4112 | 83.2 | -9.13 | 7.7 |
| X=20%,Y=ema9 | 4750 | 77.8 | -10.13 | 8.4 |
| X=20%,Y=ema21 | 4757 | 77.7 | -10.16 | 8.4 |
| X=20%,Y=ma50 | 4826 | 77.3 | -10.38 | 8.5 |


### Common/unique HOLD (lulus FDR)

11 / 18 signal HOLD lulus BH-FDR q ≤ 0.01: `b:macd_atas0`, `b:bb_squeeze`, `b:atas_awan`, `b:tenkan_atas`, `b:inside_day`, `b:outside_day`, `b:vcp`, `b:sektor_atas_ma50`, `b:supertrend_naik`, `b:psar_naik`, `b:spy_ma50_menaik`


| nama | subset | n | K_padu | K_gagal | lift | presisi | lift_presisi | kelas |
|---|---|---|---|---|---|---|---|---|
| b:macd_cross | S1 | 2 | 0.05 | 0.0 | 3.28 | 100.0 | 1.64 | TIDAK BERGUNA |
| b:vcp | S1 | 272 | 6.54 | 0.51 | 12.754 | 95.22 | 1.562 | LANGKA |
| b:atas_ema21 | S1 | 1034 | 24.47 | 2.56 | 9.543 | 93.71 | 1.537 | UNIQUE |
| b:psar_naik | S1 | 1150 | 27.07 | 3.08 | 8.798 | 93.22 | 1.529 | UNIQUE |
| b:supertrend_naik | S1 | 2461 | 56.97 | 8.09 | 7.045 | 91.67 | 1.504 | TERAS |
| b:atas_ma50 | S1 | 2265 | 51.16 | 9.43 | 5.427 | 89.45 | 1.467 | TERAS |
| b:tenkan_atas | S1 | 2718 | 61.24 | 11.56 | 5.298 | 89.22 | 1.463 | TERAS |
| b:atas_awan | S1 | 2414 | 53.33 | 11.91 | 4.477 | 87.49 | 1.435 | TERAS |
| b:macd_atas0 | S1 | 2905 | 63.96 | 14.67 | 4.359 | 87.19 | 1.43 | TERAS |
| b:bb_squeeze | S1 | 56 | 1.21 | 0.32 | 3.841 | 85.71 | 1.406 | TIDAK BERGUNA |
| b:pullback_dalam_7pct | S1 | 3858 | 79.95 | 27.3 | 2.929 | 82.06 | 1.346 | TERAS |
| b:ad_tinggi_baru | S2 | 25 | 2.83 | 0.0 | 31.222 | 100.0 | 1.249 | TIDAK BERGUNA |
| b:macd_cross | S2 | 1 | 0.11 | 0.0 | 1.249 | 100.0 | 1.249 | TIDAK BERGUNA |
| b:garis_rs_tinggi | S2 | 1 | 0.11 | 0.0 | 1.249 | 100.0 | 1.249 | TIDAK BERGUNA |
| b:atas_ema21 | S2 | 294 | 32.58 | 2.73 | 11.946 | 97.96 | 1.223 | UNIQUE |
| b:vcp | S2 | 78 | 8.6 | 0.91 | 9.457 | 97.44 | 1.217 | LANGKA |
| b:psar_naik | S2 | 296 | 32.47 | 4.09 | 7.936 | 96.96 | 1.211 | UNIQUE |
| b:supertrend_naik | S2 | 668 | 72.51 | 12.27 | 5.908 | 95.96 | 1.198 | TERAS |
| b:tenkan_atas | S2 | 711 | 75.34 | 20.45 | 3.683 | 93.67 | 1.17 | TERAS |
| b:atas_ma50 | S2 | 612 | 64.82 | 17.73 | 3.656 | 93.63 | 1.169 | TERAS |


## 7. Step 6 — EXIT (semua CALON)

> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.


| nama | n | pct_menyala | median_hari_dari_puncak | median_pulangan_exit | median_pct_kekal | kadar_exit_palsu |
|---|---|---|---|---|---|---|
| atr_lonjak_15x | 1438 | 48.3 | 13.0 | -3.7 | -16.6 | 61.1 |
| bawah_ema21 | 2974 | 99.9 | -13.0 | -1.08 | -4.9 | 60.5 |
| bawah_ema9 | 2977 | 100.0 | -19.0 | -0.73 | -3.1 | 62.4 |
| bawah_ma50 | 2934 | 98.6 | -12.0 | -0.76 | -4.1 | 59.9 |
| chandelier_4atr | 2537 | 85.2 | 14.0 | -3.01 | -16.7 | 46.3 |
| climax_25_15h | 844 | 28.4 | -12.0 | 17.98 | 61.4 | 68.1 |
| div_macd | 2669 | 89.7 | -17.0 | 4.17 | 27.9 | 58.2 |
| div_rsi | 2372 | 79.7 | -14.0 | 6.33 | 39.3 | 57.6 |
| gap_besar | 424 | 14.2 | -4.0 | 26.65 | 76.4 | 64.6 |
| hari_agihan | 2481 | 83.3 | 5.0 | 1.12 | 11.0 | 48.5 |
| hist_neg3 | 2945 | 98.9 | -10.0 | 0.39 | 3.8 | 58.2 |
| jauh_ma50_2x | 1407 | 47.3 | -13.0 | 10.63 | 58.8 | 52.5 |
| macd_bawah | 2963 | 99.5 | -9.0 | 0.59 | 6.3 | 57.9 |
| pullback_amaran | 2908 | 97.7 | 13.0 | -6.44 | -35.5 | 74.3 |
| rsi_70_60 | 1963 | 65.9 | -1.0 | 9.72 | 48.2 | 57.5 |
| trail_10pct | 2727 | 91.6 | 8.0 | -2.82 | -11.7 | 51.6 |
| trail_15pct | 2222 | 74.6 | 14.0 | -6.92 | -36.2 | 54.0 |
| trail_2atr | 2966 | 99.6 | 2.0 | -0.06 | 2.9 | 54.3 |
| trail_3atr | 2870 | 96.4 | 8.0 | -1.02 | -3.7 | 48.6 |
| trail_8pct | 2865 | 96.2 | 5.0 | -1.57 | -5.9 | 51.2 |


`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala 12–19 hari sebelum puncak dan mengekalkan hanya -3% hingga -5% keuntungan. Kadar exit palsu 46%–74%.


**Keluarga EXIT: 0 / 62 signal lulus BH-FDR q ≤ 0.01.** Tiada signal EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas kawalan pelbagai ujian.


## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)

Setiap signal corong diimbas atas **semua** hari universe 2025 (580,075 baris (ticker, hari); 499,999 selepas topeng universe). Kadar asas KAWALAN RAWAK (MFE63 ≥ 30%) = 16.37%.


| signal | n_kemunculan | kadar_tepat_mfe30 | lift_tepat | kadar_palsu_bawah10 | kadar_tepat_bertangga | ketulenan_trend_median | mfe63_p50 | mfe63_p75 | mfe63_p90 | pct_mfe63_ge30 | pct_mfe63_ge100 | mfe252_p90 | pct_mfe252_ge100 | median_hari_mfe63 | jangkaan_henti2atr | kadar_menang | kapasiti | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | 4962 | 36.09 | 2.205 | 29.24 | 4.86 | 81.1 | 20.95 | 40.53 | 66.31 | 36.09 | 3.77 | 220.67 | 29.67 | 41.0 | 6.237 | 41.78 | TULANG BELAKANG |  |
| rsi_lintas50&q5:bb_lebar | 4530 | 34.77 | 2.124 | 30.68 | 4.99 | 81.4 | 20.0 | 39.46 | 65.71 | 34.77 | 3.77 | 218.26 | 28.74 | 40.0 | 5.904 | 41.21 | TULANG BELAKANG |  |
| rsi_lintas50&q5:atr_pct | 5109 | 40.14 | 2.452 | 26.25 | 5.13 | 81.0 | 23.42 | 43.53 | 70.72 | 40.14 | 4.15 | 232.48 | 31.96 | 40.0 | 6.872 | 41.97 | TULANG BELAKANG |  |
| q5:atr_pct | 101490 | 39.02 | 2.384 | 26.77 | 4.65 | 67.7 | 22.81 | 42.61 | 69.38 | 39.02 | 4.13 | 220.55 | 30.85 | 40.0 | 6.987 | 42.45 | TULANG BELAKANG |  |
| q5:julat20 | 141160 | 32.01 | 1.955 | 31.2 | 3.88 | 69.8 | 18.69 | 36.12 | 59.87 | 32.01 | 2.92 | 191.9 | 25.59 | 41.0 | 5.423 | 41.07 | TULANG BELAKANG |  |
| q5:bb_lebar | 148303 | 29.53 | 1.804 | 33.23 | 3.66 | 72.4 | 17.27 | 33.99 | 57.13 | 29.53 | 2.64 | 183.07 | 23.87 | 41.0 | 4.95 | 40.34 | TULANG BELAKANG |  |
| macd_cross&q1:j_52w_tinggi | 4434 | 26.75 | 1.634 | 35.61 | 3.45 | 68.8 | 16.25 | 31.34 | 51.38 | 26.75 | 1.78 | 170.04 | 21.79 | 38.0 | 3.365 | 37.21 | TULANG BELAKANG |  |
| q5:j_ema9 | 47638 | 27.19 | 1.661 | 36.2 | 3.3 | 91.5 | 15.93 | 32.12 | 55.22 | 27.19 | 2.55 | 185.03 | 23.5 | 40.0 | 4.502 | 37.29 | TULANG BELAKANG |  |
| macd_cross&q1:cerun_ma50 | 4630 | 22.22 | 1.358 | 38.16 | 3.24 | 65.3 | 14.65 | 28.01 | 46.09 | 22.22 | 1.17 | 137.57 | 17.39 | 40.0 | 4.126 | 41.34 | TULANG BELAKANG |  |
| rsi_lintas50&q1:j_52w_tinggi | 5774 | 26.32 | 1.608 | 34.86 | 3.55 | 79.5 | 16.33 | 31.09 | 51.59 | 26.32 | 2.03 | 181.67 | 21.91 | 37.0 | 3.875 | 37.34 | TULANG BELAKANG |  |
| pocket_pivot&q1:j_52w_tinggi | 5918 | 27.59 | 1.686 | 35.16 | 3.7 | 85.0 | 16.46 | 32.17 | 55.08 | 27.59 | 2.79 | 193.69 | 23.39 | 37.0 | 4.052 | 35.5 | TULANG BELAKANG |  |
| rsi_lintas50&q1:cerun_ma50 | 5322 | 21.59 | 1.319 | 37.88 | 3.08 | 83.3 | 14.54 | 27.27 | 44.37 | 21.59 | 1.37 | 144.27 | 17.53 | 40.0 | 4.325 | 41.56 | TULANG BELAKANG | BUNYI LATAR |
| macd_cross&q1:j_ma200 | 4830 | 19.9 | 1.215 | 40.52 | 3.06 | 66.7 | 13.28 | 26.21 | 42.96 | 19.9 | 0.79 | 129.96 | 16.0 | 39.0 | 2.955 | 38.24 | TULANG BELAKANG |  |
| rsi_lintas50&q5:j_ma200 | 4314 | 26.59 | 1.624 | 36.9 | 3.52 | 77.4 | 15.48 | 31.47 | 54.61 | 26.59 | 2.39 | 162.39 | 20.93 | 34.0 | 0.882 | 31.46 | TULANG BELAKANG |  |
| q1:j_52w_tinggi | 111881 | 27.24 | 1.664 | 34.98 | 3.41 | 65.0 | 16.52 | 31.82 | 53.34 | 27.24 | 2.2 | 173.76 | 22.18 | 37.0 | 3.732 | 37.64 | TULANG BELAKANG |  |
| q1:roc20 | 147844 | 20.08 | 1.227 | 41.31 | 2.62 | 56.7 | 12.97 | 25.81 | 44.21 | 20.08 | 1.37 | 126.57 | 14.85 | 39.0 | 2.433 | 36.8 | TULANG BELAKANG | BUNYI LATAR |
| pocket_pivot&q1:cerun_ma50 | 5423 | 22.92 | 1.4 | 36.66 | 3.58 | 87.3 | 14.87 | 28.09 | 48.65 | 22.92 | 2.03 | 159.29 | 19.42 | 40.0 | 5.408 | 41.31 | TULANG BELAKANG | BUNYI LATAR |
| q1:cerun_ma50 | 96855 | 23.07 | 1.409 | 37.71 | 3.09 | 64.7 | 14.84 | 28.51 | 46.67 | 23.07 | 1.39 | 142.45 | 17.95 | 40.0 | 3.87 | 40.29 | TULANG BELAKANG | BUNYI LATAR |
| q1:j_ma50 | 166293 | 19.28 | 1.178 | 42.24 | 2.5 | 57.1 | 12.67 | 25.12 | 42.87 | 19.28 | 1.19 | 122.91 | 14.23 | 38.0 | 2.199 | 36.54 | TULANG BELAKANG | BUNYI LATAR |


Taburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. p90 dan % ≥ 100% ialah pembeza, bukan median.


**Lift jatuh besar antara Step 4 dan Step 7** (contoh `rsi_lintas50&q5:julat20`: lift 23.76 dalam populasi peristiwa → lift_tepat 2.21 atas semua hari universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. Angka Step 7 yang lebih dekat dengan dagangan sebenar.


### Penapis Step 7.4
152 kombinasi signal × penapis diuji (0 lulus kriteria "buang ≥ 30% palsu dan ≤ 10% benar").


**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis dipradaftar. Ini keputusan negatif yang bersih.


10 contoh penapis terbaik (ikut % palsu dibuang):


| signal | buang_palsu_pct | buang_benar_pct |
|---|---|---|
| q1:j_ma50 | penapis:harga_atas_ma50 | 100.0 | 100.0 |
| macd_cross&q1:j_ma200 | penapis:lapis_ge_3 | 99.6 | 99.2 |
| macd_cross&q1:cerun_ma50 | penapis:lapis_ge_3 | 99.4 | 99.3 |
| rsi_lintas50&q1:cerun_ma50 | penapis:lapis_ge_3 | 98.1 | 94.9 |
| q1:cerun_ma50 | penapis:lapis_ge_3 | 97.1 | 95.0 |
| q1:j_ma50 | penapis:lapis_ge_3 | 96.3 | 94.9 |
| macd_cross&q1:j_52w_tinggi | penapis:lapis_ge_3 | 96.0 | 93.7 |
| rsi_lintas50&q1:j_52w_tinggi | penapis:lapis_ge_3 | 95.4 | 88.9 |
| macd_cross&q1:cerun_ma50 | penapis:harga_atas_ma50 | 95.1 | 93.7 |
| q1:roc20 | penapis:harga_atas_ma50 | 94.9 | 92.5 |


## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)

Set kemasukan: gabungan semua kemunculan 14 signal yang lulus Step 7 = 0 (ticker, tarikh) unik, disampel berlapis ikut bulan ke **0** (benih 42; SPEC §13.9). Grid 18 HOLD × 13 EXIT = **234** sistem.


### TIGA RUJUKAN WAJIB

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_menang | purata_kalah | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 | pct_terpotong_data | siri_kalah_terpanjang |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 24000 | 10.14 | 27.57 | 27.571 | 57.97 | 68.96 | 29.51 | 246.4 | -22.73 | 0.0 | 100.0 | 21.1 | 12 |
| REF_chandelier_4atr | 24000 | -5.0 | 6.07 | 6.069 | 40.21 | 36.06 | 14.1 | 58.9 | -9.14 | 80.5 | 0.8 | 21.1 | 39 |
| REF_jual_hari63 | 24000 | 1.63 | 4.85 | 4.846 | 52.55 | 25.49 | 18.02 | 63.0 | -12.4 | 81.6 | 0.0 | 0.0 | 38 |


**Keputusan: rujukan "pegang tanpa jual hingga hari ke-252" menang, dan 0 / 234 sistem mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = 27.571%). Mengikut arahan Step 7b.4, jawapan kajian ialah **"jangan jual"** — dan itu dilaporkan sebagai penemuan, bukan kegagalan.


### 15 sistem terbaik daripada 234

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 |
|---|---|---|---|---|---|---|---|---|---|
| rsi_70_60|X=20%,Y=ma50 | 24000 | 3.2 | 9.94 | 9.94 | 56.55 | 106.3 | -10.5 | 68.5 | 10.5 |
| rsi_70_60|X=15%,Y=ma50 | 24000 | 3.31 | 9.1 | 9.098 | 56.77 | 102.7 | -10.27 | 69.5 | 9.6 |
| hari_agihan|X=20%,Y=ma50 | 24000 | -2.54 | 8.51 | 8.512 | 43.29 | 70.5 | -8.9 | 76.2 | 2.8 |
| hari_agihan|X=15%,Y=ma50 | 24000 | -2.48 | 8.28 | 8.284 | 43.53 | 68.6 | -8.82 | 76.7 | 2.3 |
| rsi_70_60|X=12%,Y=ma50 | 24000 | 3.29 | 8.19 | 8.192 | 56.94 | 98.8 | -9.98 | 71.0 | 8.7 |
| hari_agihan|X=12%,Y=ma50 | 24000 | -2.4 | 8.04 | 8.041 | 43.72 | 67.1 | -8.76 | 77.1 | 2.1 |
| hari_agihan|X=10%,Y=ma50 | 24000 | -2.33 | 7.56 | 7.559 | 43.89 | 65.9 | -8.69 | 77.4 | 1.9 |
| hari_agihan|X=20%,Y=ema21 | 24000 | -2.09 | 7.46 | 7.457 | 44.35 | 62.8 | -8.4 | 77.6 | 1.8 |
| rsi_70_60|X=10%,Y=ma50 | 24000 | 3.27 | 7.34 | 7.343 | 57.15 | 94.7 | -9.6 | 71.9 | 8.0 |
| hari_agihan|X=15%,Y=ema21 | 24000 | -2.07 | 7.29 | 7.289 | 44.42 | 62.0 | -8.38 | 77.9 | 1.6 |
| hari_agihan|X=12%,Y=ema21 | 24000 | -2.06 | 7.14 | 7.14 | 44.44 | 61.6 | -8.37 | 78.1 | 1.6 |
| hari_agihan|X=7%,Y=ma50 | 24000 | -2.06 | 6.91 | 6.905 | 44.57 | 61.8 | -8.47 | 78.1 | 1.6 |
| hari_agihan|X=10%,Y=ema21 | 24000 | -2.04 | 6.86 | 6.865 | 44.51 | 61.1 | -8.34 | 78.2 | 1.5 |
| hari_agihan|X=5%,Y=ma50 | 24000 | -1.89 | 6.62 | 6.617 | 45.01 | 58.9 | -8.28 | 78.5 | 1.4 |
| hari_agihan|X=7%,Y=ema21 | 24000 | -1.96 | 6.51 | 6.512 | 44.78 | 59.3 | -8.28 | 78.7 | 1.4 |


Perhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.


## 10. Step 8 — kawalan kebetulan

### Ujian label rawak dan FDR per keluarga

| keluarga | N | lulus_fdr | ambang_p |
|---|---|---|---|
| ENTRY/PADU | 19 | 18 | 0.001998001998001998 |
| ENTRY/SUPER PADU | 19 | 11 | 0.000999000999000999 |
| HOLD | 18 | 11 | 0.004975124378109453 |
| EXIT | 62 | 0 |  |
| SISTEM | 234 | 0 |  |


Perbandingan yang diminta arahan: **18 signal lulus FDR daripada 19 diuji**, manakala label rawak menghasilkan lift purata yang jauh lebih rendah (lajur `lift_purata_rawak` dalam `kawalan_rawak_bootstrap_2025.csv`).


### Jangkaan atas SEMUA kemunculan + ujian outlier

| signal | n_kemunculan | median_pulangan | jangkaan | jangkaan_tanpa_5pct_teratas | pct_rugi_lebih_10 | siri_kalah_terpanjang | jangkaan_bawah95_blok_ticker | jangkaan_bawah95_blok_minggu |
|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | 4962 | -8.43 | 6.237 | 0.657 | 44.3 | 23 | 5.114 | 1.229 |
| rsi_lintas50&q5:bb_lebar | 4530 | -8.3 | 5.904 | 0.319 | 43.7 | 19 | 4.778 | 0.65 |
| rsi_lintas50&q5:atr_pct | 5109 | -10.01 | 6.872 | 1.137 | 50.0 | 25 | 5.688 | 2.176 |
| q5:atr_pct | 101490 | -9.88 | 6.987 | 1.299 | 49.6 | 207 | 6.069 | 3.26 |
| q5:julat20 | 141160 | -7.68 | 5.423 | 0.453 | 40.2 | 174 | 4.785 | 2.257 |
| q5:bb_lebar | 148303 | -6.94 | 4.95 | 0.156 | 36.5 | 178 | 4.3 | 2.085 |
| macd_cross&q1:j_52w_tinggi | 4434 | -7.65 | 3.365 | -1.038 | 36.0 | 22 | 2.486 | -0.936 |
| q5:j_ema9 | 47638 | -6.63 | 4.502 | -0.258 | 30.4 | 77 | 3.698 | 2.183 |
| macd_cross&q1:cerun_ma50 | 4630 | -6.01 | 4.126 | 0.185 | 31.5 | 16 | 3.437 | -1.756 |
| rsi_lintas50&q1:j_52w_tinggi | 5774 | -7.29 | 3.875 | -0.789 | 33.7 | 32 | 2.947 | 0.837 |
| pocket_pivot&q1:j_52w_tinggi | 5918 | -7.69 | 4.052 | -0.98 | 34.5 | 64 | 2.731 | 1.082 |
| rsi_lintas50&q1:cerun_ma50 | 5322 | -5.64 | 4.325 | 0.223 | 27.4 | 21 | 3.546 | -0.24 |
| macd_cross&q1:j_ma200 | 4830 | -6.17 | 2.955 | -0.638 | 29.0 | 18 | 2.313 | -1.611 |
| rsi_lintas50&q5:j_ma200 | 4314 | -7.63 | 0.882 | -3.411 | 36.7 | 28 | -0.219 | -1.582 |
| q1:j_52w_tinggi | 111881 | -7.54 | 3.732 | -0.938 | 37.1 | 230 | 3.02 | 0.802 |
| q1:roc20 | 147844 | -6.15 | 2.433 | -1.427 | 30.5 | 200 | 2.052 | -0.474 |
| pocket_pivot&q1:cerun_ma50 | 5423 | -5.87 | 5.408 | 0.756 | 27.1 | 22 | 4.259 | 0.673 |
| q1:cerun_ma50 | 96855 | -6.23 | 3.87 | -0.233 | 31.8 | 223 | 3.269 | -0.267 |
| q1:j_ma50 | 166293 | -6.13 | 2.199 | -1.563 | 29.8 | 249 | 1.84 | -0.66 |


### Keputusan gate demi gate

| signal | G1_sah_dalam_tahun | G2_merentas_tahun | G3_nilai_p | G3_fdr | G4_bootstrap | G5_outlier | G6 | step7 | keputusan |
|---|---|---|---|---|---|---|---|---|---|
| rsi_lintas50&q5:julat20 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:atr_pct | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=LANGKA; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q5:atr_pct | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q5:julat20 | SEBAHAGIAN | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q5:bb_lebar | SEBAHAGIAN | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=SEDERHANA) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| macd_cross&q1:j_52w_tinggi | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=LANGKA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q5:j_ema9 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| macd_cross&q1:cerun_ma50 | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2020=LANGKA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=LANGKA; 2024=TIDAK BERGUNA) | 0.002 | LULUS | GAGAL | LULUS | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=UNIQUE; 2023=UNIQUE; 2024=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| pocket_pivot&q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=LANGKA; 2023=LANGKA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q1:cerun_ma50 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | LULUS | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| macd_cross&q1:j_ma200 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| rsi_lintas50&q5:j_ma200 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=UNIQUE; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.94106 | GAGAL | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:j_52w_tinggi | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | BERGANTUNG PADA OUTLIER | LULUS | LULUS | DITOLAK |
| q1:roc20 | SEBAHAGIAN | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=SEDERHANA; 2023=TIDAK BERGUNA; 2024=SEDERHANA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| pocket_pivot&q1:cerun_ma50 | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2020=TIDAK BERGUNA; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.002 | LULUS | LULUS | LULUS | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q1:cerun_ma50 | GAGAL | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=UNIQUE; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=COMMON BIASA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q1:j_ma50 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2020=SEDERHANA; 2021=SEDERHANA; 2022=COMMON BIASA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA) | 0.001 | LULUS | GAGAL | BERGANTUNG PADA OUTLIER | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |


**DITERIMA: 0** · **CALON: 4** — `rsi_lintas50&q5:atr_pct`, `q5:atr_pct`, `q5:julat20`, `q5:bb_lebar` · **DITOLAK: 15.**


Kesemua CALON ialah **konteks pengembangan kemeruapan** (ATR% tinggi, lebar Bollinger tinggi, julat 20 hari luas). Ini perlu dibaca bersama kaveat survivorship: kohort kemeruapan tinggi ialah tempat ketiadaan saham delist paling memihak kepada hasil. Pengesahan merentas tahun (gate 8.1) adalah penentu sebenar.


Penapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam ≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada 2025.


## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)

Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. Asas signal ENTRY: **CALON selepas Step 8**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → RS 6 bulan → ticker.


| sistem | n_posisi_dibuka | n_dagangan_ditutup | n_posisi_terbuka_hujung_tahun | purata_slot_terisi | pulangan_tahun | median_bulanan | purata_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terbaik | bulan_terburuk | mdd | purata_hari_pegang | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 8 | 0 | 8 | 7.94 | 128.93 | 5.65 | 8.19 | 41.7 | 66.7 | 38.73 | -16.56 | -38.71 |  | 0.7 | 18.01 | -18.76 |
| REF_chandelier_4atr | 42 | 34 | 8 | 7.8 | 14.93 | 0.93 | 2.15 | 16.7 | 58.3 | 39.1 | -20.31 | -43.39 | 49.1 | 3.5 | 18.01 | -18.76 |
| REF_jual_hari63 | 40 | 32 | 8 | 7.81 | -24.5 | -2.27 | -1.94 | 8.3 | 33.3 | 17.14 | -16.76 | -47.62 | 63.0 | 3.3 | 18.01 | -18.76 |
| rsi_70_60|X=20%,Y=ma50 | 30 | 22 | 8 | 7.85 | -14.19 | -2.36 | -1.08 | 0.0 | 41.7 | 7.99 | -10.85 | -26.98 | 61.8 | 2.5 | 18.01 | -18.76 |
| rsi_70_60|X=15%,Y=ma50 | 37 | 29 | 8 | 7.82 | 5.54 | 1.31 | 0.83 | 8.3 | 50.0 | 18.11 | -14.19 | -30.59 | 55.7 | 3.1 | 18.01 | -18.76 |
| hari_agihan|X=20%,Y=ma50 | 44 | 36 | 8 | 7.79 | -31.79 | -2.52 | -2.41 | 25.0 | 33.3 | 17.09 | -23.49 | -47.73 | 33.5 | 3.7 | 18.01 | -18.76 |
| KAWALAN_RAWAK|pegang_252 | 8 | 0 | 8 | 7.94 | 9.51 | 2.39 | 0.89 | 0.0 | 58.3 | 9.84 | -6.73 | -27.62 |  | 0.7 | 18.01 | -18.76 |
| KAWALAN_RAWAK|chandelier | 40 | 32 | 8 | 7.81 | 29.47 | 1.62 | 2.34 | 8.3 | 75.0 | 10.18 | -9.29 | -28.45 | 46.2 | 3.3 | 18.01 | -18.76 |


### Pulangan bulanan penuh (%)

| tarikh | REF_pegang_252 | REF_chandelier_4atr | REF_jual_hari63 | rsi_70_60|X=20%,Y=ma50 | rsi_70_60|X=15%,Y=ma50 | hari_agihan|X=20%,Y=ma50 | KAWALAN_RAWAK|pegang_252 | KAWALAN_RAWAK|chandelier |
|---|---|---|---|---|---|---|---|---|
| 2025-01-31 | 1.8 | -1.32 | 1.8 | 3.14 | 3.14 | -2.62 | 1.93 | 1.27 |
| 2025-02-28 | -3.66 | -4.4 | -3.66 | -1.64 | -0.52 | -10.4 | -6.73 | -4.88 |
| 2025-03-31 | -16.56 | -20.31 | -16.56 | -9.85 | -14.19 | -12.8 | -5.73 | -9.29 |
| 2025-04-30 | 7.87 | 1.59 | -16.76 | 4.18 | 5.47 | -15.11 | -3.82 | 0.03 |
| 2025-05-31 | 24.29 | 8.22 | -3.29 | -5.09 | -3.25 | -2.41 | 6.3 | 8.76 |
| 2025-06-30 | 23.19 | 11.5 | 5.34 | -5.0 | 3.16 | 3.54 | 4.26 | 8.45 |
| 2025-07-31 | 14.12 | -8.15 | -2.58 | -3.09 | -2.17 | -0.51 | 2.85 | 10.18 |
| 2025-08-31 | 3.43 | 8.25 | -2.72 | 6.74 | 9.14 | 13.48 | 5.07 | 1.97 |
| 2025-09-30 | 38.73 | 39.1 | 17.14 | 4.97 | 18.11 | 17.09 | 3.86 | 9.71 |
| 2025-10-31 | 15.93 | 6.78 | -1.97 | 7.99 | 8.33 | 11.96 | 9.84 | 2.87 |
| 2025-11-30 | -9.58 | 0.26 | -1.42 | -10.85 | -5.57 | -23.49 | -3.84 | -1.59 |
| 2025-12-31 | -1.31 | -15.77 | 1.41 | -4.45 | -11.73 | -7.7 | -3.29 | 0.64 |


### Jawapan terus kepada sasaran +10% sebulan

**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:


- `REF_pegang_252`: median bulanan **5.65%**, 41.7% bulan ≥ +10%, bulan terburuk -16.56%, MDD -38.71%, pulangan tahun 128.93% (SPY 18.01%, MDD SPY -18.76%)

- `REF_chandelier_4atr`: median bulanan **0.93%**, 16.7% bulan ≥ +10%, bulan terburuk -20.31%, MDD -43.39%, pulangan tahun 14.93% (SPY 18.01%, MDD SPY -18.76%)

- `REF_jual_hari63`: median bulanan **-2.27%**, 8.3% bulan ≥ +10%, bulan terburuk -16.76%, MDD -47.62%, pulangan tahun -24.50% (SPY 18.01%, MDD SPY -18.76%)

- `rsi_70_60|X=20%,Y=ma50`: median bulanan **-2.36%**, 0.0% bulan ≥ +10%, bulan terburuk -10.85%, MDD -26.98%, pulangan tahun -14.19% (SPY 18.01%, MDD SPY -18.76%)

- `rsi_70_60|X=15%,Y=ma50`: median bulanan **1.31%**, 8.3% bulan ≥ +10%, bulan terburuk -14.19%, MDD -30.59%, pulangan tahun 5.54% (SPY 18.01%, MDD SPY -18.76%)

- `hari_agihan|X=20%,Y=ma50`: median bulanan **-2.52%**, 25.0% bulan ≥ +10%, bulan terburuk -23.49%, MDD -47.73%, pulangan tahun -31.79% (SPY 18.01%, MDD SPY -18.76%)

- `KAWALAN_RAWAK|pegang_252`: median bulanan **2.39%**, 0.0% bulan ≥ +10%, bulan terburuk -6.73%, MDD -27.62%, pulangan tahun 9.51% (SPY 18.01%, MDD SPY -18.76%)

- `KAWALAN_RAWAK|chandelier`: median bulanan **1.62%**, 8.3% bulan ≥ +10%, bulan terburuk -9.29%, MDD -28.45%, pulangan tahun 29.47% (SPY 18.01%, MDD SPY -18.76%)


**Apa yang menghalang — kapasiti, bukan kadar menang.**

- Sistem terbaik (`REF_pegang_252`) hanya membuka **8 posisi sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh dijadikan asas keputusan.

- Sistem yang pusing ganti mencukupi (Chandelier: 42 posisi, 3.5/bulan) memberi median bulanan hanya 0.93% dengan MDD -43.39% — lebih buruk daripada MDD SPY.

- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.

- KAWALAN RAWAK pegang-252 memberi 9.51% dan Chandelier rawak 29.47% — dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.


### Banding wajib: SPY dan KAWALAN RAWAK

- SPY tempoh sama: **18.01%** (MDD -18.76%). **5/6** sistem kalah kepada SPY.

- KAWALAN RAWAK terbaik: **29.47%** (`KAWALAN_RAWAK|chandelier`). **5/6** sistem kalah kepada entri rawak.


> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.


## 12. Keputusan akhir (had fasa: CALON)

1. **ENTRY** — 4 signal CALON: `rsi_lintas50&q5:atr_pct`, `q5:atr_pct`, `q5:julat20`, `q5:bb_lebar`. Tiada pemicu klasik tunggal lulus. Hipotesis "magnitud ada pada konteks, bukan pemicu" disokong oleh data 2025.

2. **HOLD** — 11/18 signal lulus FDR; kelas pullback ialah hasil paling kukuh (SIHAT 88.9% / PASARAN 92.0% menyambung ke puncak baru lawan AMARAN 50.8%).

3. **EXIT** — 0/62 signal lulus FDR; 0/234 sistem mengalahkan ketiga-tiga rujukan dan 0/234 lulus FDR keluarga SISTEM. **Jawapan kajian tahun ini: jangan jual.**

4. **PORTFOLIO** — sasaran +10% sebulan tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila pegangan panjang, bukan kadar menang.

5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam ≥ 2 tahun LAIN; tahun lain yang siap: [2020, 2021, 2022, 2023, 2024]. Lihat `BANDING_TAHUN.md` untuk status merentas tahun.


## 13. Fail output

| Fail | Isi |
|---|---|
| `runs_2025.csv` | 4507 run, 34 lajur |
| `monthly_summary_2025.csv` | ringkasan 12 bulan |
| `skipped_2025.csv` | 13507 calon ditolak + sebab |
| `kohort_masih_naik_2025.csv` | 470 run masih_naik dijejak 252 hari |
| `common_unique_2025.csv` | 3408 baris (213 signal × subset × populasi × kumpulan × keluarga) |
| `taburan_indikator_2025.csv` | median + p25/p75 setiap indikator setiap hasil |
| `hold_exit_2025.csv` | 357 baris CALON HOLD/EXIT |
| `false_signal_2025.csv` | 171 baris (signal + penapis) |
| `hadapan_hold_exit_2025.csv` | 237 sistem (234 + 3 rujukan) |
| `kawalan_rawak_bootstrap_2025.csv` | nilai-p label rawak + had bawah bootstrap |
| `jangkaan_kemunculan_2025.csv` | jangkaan + ujian outlier |
| `keputusan_2025.csv` | keputusan gate demi gate |
| `portfolio_2025.csv`, `portfolio_bulanan_2025.csv` | Step 9 |
| `log_ujian.csv` | setiap signal/kombinasi yang diuji |
| `PANDANG_HADAPAN_2025.md` | imbasan pandang ke hadapan |
| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |
