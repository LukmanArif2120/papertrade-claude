# LAPORAN REVERSE 2020 — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.

> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = **satu rejim pasaran**. Peta sektor bukan titik-masa. Gate 8.1 ada 5 tahun lain ([2021, 2022, 2023, 2024, 2025]); keputusan **maksimum CALON** (SPEC §11.8).

## 0. Jawapan ringkas

1. **4593 run layak** dikenal pasti dalam 2020; setiap 12 bulan ada calon (tiada "TIADA CALON"). 279 SUPER PADU (≥100%), 2976 PADU, 1338 BIASA.

2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada 515 run yang masih naik pada hari ke-63, **54.6% akhirnya melebihi +100%**, dengan median kenaikan penuh **107.2%** lawan 46.5% pada hari ke-63.

3. **Signal entry: 6 CALON daripada 16 yang masuk corong**: `q5:julat20`, `q5:atr_pct`, `q5:bb_lebar`, `rsi_lintas50&q5:atr_pct`, `macd_cross&q1:sektor_1b`, `q1:cerun_ma50`.

4. **Rujukan "pegang tanpa jual hingga hari ke-252" MENANG.** Tiada satu pun daripada 234 sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan. Jangkaan: +60.66% (pegang tanpa jual hingga hari ke-252), +19.61% (Chandelier 4×ATR14), +15.00% (jual hari ke-63). Mengikut arahan Step 7b.4, jawapan kajian tahun ini ialah **"jangan jual"**.

5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan pegang-252 hanya membuka **16 posisi sepanjang tahun** (8 slot terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. Pulangannya 57.40% ialah hasil **16 saham**, bukan sistem.

6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik ialah 3.26% sebulan (median) dengan MDD -54.28%.

7. **Keluarga EXIT dan SISTEM pada FDR:** 0/68 signal EXIT dan 0/234 sistem lulus q ≤ 0.01.

## 1. Semakan kesediaan Step 0

| Semakan | Hasil |
|---|---|
| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, 2009-01-02 → 2026-10-16; semua sha256 sepadan |
| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |
| c. Sumber sektor/industri setiap ticker | **LULUS** — 2115/2131 = 99.2% (2 kelas saham diisi daripada ticker asas; 103 ticker = `Lain-lain`) |
| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 (indeks sektor A02; diluluskan pengguna) |
| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — 0.147 s/ticker; larian penuh 2131 ticker = 313 s |
| f. `semak_hadapan` atas modul indikator | **LULUS** — 14 tarikh potong (≥ 12), 26,950 perbandingan, **0 kegagalan** (`REVERSE/PANDANG_HADAPAN_2020.md`) |

## 2. Step 1–2 — run

Saiz universe 2020 setiap bulan: min **1638**, median **1832**, maks **1940**; 2131 ticker berbeza sepanjang tahun.


> **KAVEAT SAIZ UNIVERSE.** Universe 2020 lebih kecil daripada had 2000 saham (min 1638 sebulan). Jumlah run, peristiwa dan kemunculan tahun ini **tidak setara** dengan tahun yang universenya penuh 2000; bandingkan kadar dan peratusan, bukan bilangan mutlak, dalam `BANDING_TAHUN.md`.

| bulan | n_run | n_super | n_padu | n_biasa | n_bertangga | n_lonjakan | n_stabil | n_entry_sah | n_masih_naik | n_peristiwa | med_naik |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020-01 | 277 | 0 | 23 | 254 | 1 | 169 | 107 | 236 | 6 | 756 | 13.8 |
| 2020-02 | 431 | 1 | 100 | 330 | 0 | 336 | 95 | 189 | 49 | 999 | 14.1 |
| 2020-03 | 1658 | 166 | 1369 | 123 | 94 | 1022 | 542 | 460 | 312 | 1214 | 45.3 |
| 2020-04 | 36 | 7 | 25 | 4 | 12 | 17 | 7 | 29 | 10 | 373 | 51.8 |
| 2020-05 | 70 | 3 | 51 | 16 | 10 | 35 | 25 | 57 | 14 | 1547 | 37.7 |
| 2020-06 | 142 | 5 | 95 | 42 | 19 | 69 | 54 | 76 | 5 | 1036 | 36.9 |
| 2020-07 | 182 | 3 | 66 | 113 | 15 | 115 | 52 | 146 | 27 | 1088 | 24.5 |
| 2020-08 | 141 | 4 | 79 | 58 | 15 | 85 | 41 | 109 | 42 | 980 | 34.4 |
| 2020-09 | 1012 | 39 | 765 | 208 | 230 | 309 | 473 | 874 | 333 | 1407 | 39.1 |
| 2020-10 | 288 | 16 | 176 | 96 | 30 | 104 | 154 | 253 | 34 | 977 | 35.4 |
| 2020-11 | 178 | 16 | 117 | 45 | 49 | 44 | 85 | 154 | 48 | 1652 | 38.2 |
| 2020-12 | 178 | 19 | 110 | 49 | 38 | 56 | 84 | 152 | 22 | 829 | 41.6 |


Jumlah: **4593 run layak**, 2735 (59.5%) dengan `entry_sah = ya` (tiada amaran: syarat 10 hari menolak 40.5% < 50%). Dilangkau: 7785 (6921 "terlalu perlahan").


### Bucket %_naik × tempoh

| bucket_pct | <=21 | <=42 | <=63 |
|---|---|---|---|
| 10%+ | 846 | 0 | 0 |
| 100%+ | 3 | 14 | 216 |
| 20%+ | 128 | 364 | 0 |
| 200%+ | 1 | 2 | 26 |
| 30%+ | 101 | 196 | 1596 |
| 300%+ | 0 | 2 | 15 |
| 50%+ | 20 | 88 | 975 |


### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)

| kumpulan | PANTAS | PERLAHAN | SEDANG |
|---|---|---|---|
| BIASA | 974 | 0 | 364 |
| PADU | 121 | 2571 | 284 |
| SUPER PADU | 4 | 257 | 18 |


Sel SAMPEL KECIL: [('SUPER PADU', 'PANTAS'), ('SUPER PADU', 'SEDANG')]


### Jenis kenaikan

| jenis | n |
|---|---|
| LONJAKAN | 2361 |
| STABIL | 1719 |
| BERTANGGA | 513 |


`graf_menaik = ya` (S3): 1881 (41.0%). `masih_naik = ya`: 902.


### 10 run terbaik setiap bulan (ikut %_naik_rendah)


**2020-01**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| MRNA | Healthcare | 2020-01-07 | 2020-04-03 | 61 | 97.06 | PADU | LONJAKAN | ya | ya |
| IOVA | Healthcare | 2020-01-27 | 2020-03-06 | 28 | 81.71 | PADU | LONJAKAN | ya | tidak |
| PETS | Healthcare | 2020-01-27 | 2020-04-27 | 63 | 66.16 | PADU | LONJAKAN | ya | ya |
| FNGD | Lain-lain | 2020-01-22 | 2020-03-18 | 39 | 65.85 | PADU | LONJAKAN | tidak | tidak |
| CLW | Basic Materials | 2020-01-10 | 2020-02-05 | 17 | 60.73 | PADU | LONJAKAN | ya | tidak |
| DOCU | Technology | 2020-01-27 | 2020-04-27 | 63 | 53.44 | PADU | LONJAKAN | ya | ya |
| BJ | Consumer Defensive | 2020-01-31 | 2020-03-18 | 32 | 47.77 | PADU | LONJAKAN | ya | tidak |
| USNA | Consumer Defensive | 2020-01-31 | 2020-04-30 | 62 | 44.91 | PADU | LONJAKAN | ya | ya |
| QTTB | Healthcare | 2020-01-29 | 2020-03-04 | 24 | 44.81 | PADU | LONJAKAN | ya | tidak |
| WMK | Consumer Defensive | 2020-01-31 | 2020-04-28 | 60 | 41.58 | PADU | STABIL | ya | tidak |


**2020-02**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| W | Consumer Cyclical | 2020-02-28 | 2020-05-11 | 50 | 263.04 | SUPER PADU | STABIL | tidak | tidak |
| TGTX | Healthcare | 2020-02-28 | 2020-05-22 | 59 | 93.45 | PADU | LONJAKAN | tidak | tidak |
| NTLA | Healthcare | 2020-02-27 | 2020-05-22 | 60 | 88.08 | PADU | STABIL | ya | tidak |
| CWH | Consumer Cyclical | 2020-02-28 | 2020-05-26 | 60 | 77.33 | PADU | LONJAKAN | tidak | tidak |
| COHR | Technology | 2020-02-27 | 2020-05-20 | 58 | 74.72 | PADU | LONJAKAN | tidak | tidak |
| WIX | Technology | 2020-02-28 | 2020-05-29 | 63 | 74.36 | PADU | STABIL | ya | ya |
| SA | Basic Materials | 2020-02-28 | 2020-05-19 | 56 | 68.29 | PADU | LONJAKAN | tidak | tidak |
| MRVL | Technology | 2020-02-28 | 2020-05-29 | 63 | 67.75 | PADU | STABIL | ya | ya |
| EBS | Healthcare | 2020-02-28 | 2020-05-18 | 55 | 66.61 | PADU | LONJAKAN | ya | tidak |
| OKTA | Technology | 2020-02-28 | 2020-05-29 | 63 | 64.94 | PADU | STABIL | ya | ya |


**2020-03**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| PENN | Consumer Cyclical | 2020-03-18 | 2020-06-04 | 54 | 896.53 | SUPER PADU | BERTANGGA | tidak | tidak |
| CHEF | Consumer Defensive | 2020-03-18 | 2020-06-08 | 56 | 464.51 | SUPER PADU | STABIL | tidak | tidak |
| SSL | Basic Materials | 2020-03-12 | 2020-06-08 | 60 | 423.33 | SUPER PADU | STABIL | tidak | tidak |
| TPC | Industrials | 2020-03-18 | 2020-06-08 | 56 | 412.64 | SUPER PADU | STABIL | tidak | tidak |
| GCO | Consumer Cyclical | 2020-03-18 | 2020-06-08 | 56 | 408.15 | SUPER PADU | STABIL | tidak | tidak |
| PLAY | Communication Services | 2020-03-18 | 2020-06-08 | 56 | 355.37 | SUPER PADU | LONJAKAN | tidak | tidak |
| TLRY | Healthcare | 2020-03-18 | 2020-05-26 | 47 | 344.86 | SUPER PADU | LONJAKAN | ya | tidak |
| CPRI | Consumer Cyclical | 2020-03-18 | 2020-06-08 | 56 | 329.7 | SUPER PADU | STABIL | tidak | tidak |
| SRG | Real Estate | 2020-03-18 | 2020-06-08 | 56 | 324.8 | SUPER PADU | LONJAKAN | tidak | tidak |
| AER | Industrials | 2020-03-18 | 2020-06-08 | 56 | 284.26 | SUPER PADU | STABIL | tidak | tidak |


**2020-04**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ARCT | Healthcare | 2020-04-03 | 2020-05-22 | 34 | 388.43 | SUPER PADU | STABIL | ya | tidak |
| SHOP | Technology | 2020-04-02 | 2020-07-02 | 63 | 207.87 | SUPER PADU | BERTANGGA | ya | ya |
| EVER | Communication Services | 2020-04-03 | 2020-06-25 | 57 | 185.28 | SUPER PADU | BERTANGGA | ya | tidak |
| PDD | Consumer Cyclical | 2020-04-02 | 2020-07-02 | 63 | 174.34 | SUPER PADU | BERTANGGA | ya | ya |
| SE | Consumer Cyclical | 2020-04-28 | 2020-07-08 | 49 | 135.85 | SUPER PADU | BERTANGGA | ya | tidak |
| CYRX | Industrials | 2020-04-20 | 2020-07-20 | 63 | 120.13 | SUPER PADU | BERTANGGA | ya | ya |
| GOTU | Consumer Defensive | 2020-04-03 | 2020-07-06 | 63 | 105.6 | SUPER PADU | STABIL | ya | ya |
| BILI | Communication Services | 2020-04-08 | 2020-07-09 | 63 | 97.66 | PADU | BERTANGGA | ya | ya |
| BAND | Technology | 2020-04-30 | 2020-07-30 | 63 | 95.73 | PADU | BERTANGGA | ya | ya |
| DDS | Consumer Cyclical | 2020-04-03 | 2020-06-08 | 44 | 66.62 | PADU | LONJAKAN | tidak | tidak |


**2020-05**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| NVAX | Healthcare | 2020-05-01 | 2020-07-28 | 60 | 805.55 | SUPER PADU | BERTANGGA | ya | tidak |
| LAKE | Consumer Cyclical | 2020-05-11 | 2020-07-08 | 40 | 107.32 | SUPER PADU | BERTANGGA | tidak | tidak |
| AAOI | Technology | 2020-05-15 | 2020-08-04 | 55 | 102.22 | SUPER PADU | BERTANGGA | ya | tidak |
| ZM | Technology | 2020-05-27 | 2020-08-20 | 60 | 94.88 | PADU | BERTANGGA | ya | tidak |
| ARCT | Healthcare | 2020-05-27 | 2020-07-27 | 42 | 83.16 | PADU | LONJAKAN | tidak | tidak |
| SPCE | Industrials | 2020-05-21 | 2020-07-22 | 42 | 74.93 | PADU | LONJAKAN | ya | tidak |
| MATX | Industrials | 2020-05-14 | 2020-08-12 | 62 | 71.83 | PADU | LONJAKAN | ya | ya |
| SSTI | Technology | 2020-05-14 | 2020-08-07 | 59 | 64.51 | PADU | LONJAKAN | tidak | tidak |
| BCO | Industrials | 2020-05-13 | 2020-06-08 | 17 | 63.59 | PADU | BERTANGGA | ya | tidak |
| CINF | Financial Services | 2020-05-06 | 2020-07-29 | 58 | 58.79 | PADU | STABIL | tidak | tidak |


**2020-06**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| BBWI | Consumer Cyclical | 2020-06-24 | 2020-09-01 | 48 | 134.67 | SUPER PADU | STABIL | ya | tidak |
| EAT | Consumer Cyclical | 2020-06-26 | 2020-09-02 | 47 | 128.95 | SUPER PADU | BERTANGGA | ya | tidak |
| PENN | Consumer Cyclical | 2020-06-11 | 2020-09-10 | 63 | 126.96 | SUPER PADU | BERTANGGA | ya | ya |
| CODX | Healthcare | 2020-06-08 | 2020-08-03 | 39 | 112.41 | SUPER PADU | LONJAKAN | ya | tidak |
| SGRY | Healthcare | 2020-06-15 | 2020-09-14 | 63 | 103.12 | SUPER PADU | STABIL | ya | ya |
| OSUR | Healthcare | 2020-06-12 | 2020-08-05 | 37 | 94.63 | PADU | STABIL | tidak | tidak |
| RRR | Consumer Cyclical | 2020-06-26 | 2020-09-15 | 55 | 85.13 | PADU | BERTANGGA | tidak | tidak |
| BJRI | Consumer Cyclical | 2020-06-22 | 2020-09-15 | 59 | 83.81 | PADU | STABIL | ya | tidak |
| HOV | Consumer Cyclical | 2020-06-15 | 2020-08-21 | 48 | 83.75 | PADU | LONJAKAN | ya | tidak |
| CAR | Industrials | 2020-06-26 | 2020-09-02 | 47 | 80.0 | PADU | STABIL | ya | tidak |


**2020-07**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| DMRC | Technology | 2020-07-14 | 2020-10-07 | 60 | 122.14 | SUPER PADU | LONJAKAN | tidak | tidak |
| NVCR | Healthcare | 2020-07-21 | 2020-10-09 | 57 | 119.6 | SUPER PADU | BERTANGGA | ya | tidak |
| DKNG | Consumer Cyclical | 2020-07-07 | 2020-10-02 | 62 | 109.46 | SUPER PADU | STABIL | ya | ya |
| HVT | Consumer Cyclical | 2020-07-20 | 2020-10-15 | 62 | 94.96 | PADU | BERTANGGA | tidak | ya |
| CPS | Consumer Cyclical | 2020-07-09 | 2020-08-28 | 36 | 85.9 | PADU | BERTANGGA | ya | tidak |
| BYD | Consumer Cyclical | 2020-07-08 | 2020-10-05 | 62 | 84.91 | PADU | BERTANGGA | ya | ya |
| STOK | Healthcare | 2020-07-14 | 2020-10-12 | 63 | 76.65 | PADU | BERTANGGA | ya | ya |
| APPN | Technology | 2020-07-14 | 2020-10-09 | 62 | 75.31 | PADU | BERTANGGA | ya | ya |
| OMF | Financial Services | 2020-07-09 | 2020-10-07 | 63 | 71.48 | PADU | STABIL | ya | ya |
| SRRK | Healthcare | 2020-07-24 | 2020-09-29 | 46 | 69.76 | PADU | STABIL | ya | tidak |


**2020-08**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| JMIA | Consumer Cyclical | 2020-08-27 | 2020-11-25 | 63 | 327.39 | SUPER PADU | STABIL | tidak | ya |
| VERI | Technology | 2020-08-31 | 2020-11-30 | 63 | 230.97 | SUPER PADU | STABIL | tidak | ya |
| SNAP | Communication Services | 2020-08-27 | 2020-11-25 | 63 | 118.3 | SUPER PADU | STABIL | ya | ya |
| QDEL | Healthcare | 2020-08-27 | 2020-11-06 | 50 | 109.93 | SUPER PADU | STABIL | tidak | tidak |
| CORT | Healthcare | 2020-08-27 | 2020-11-20 | 60 | 96.15 | PADU | LONJAKAN | ya | tidak |
| GRVY | Communication Services | 2020-08-11 | 2020-09-28 | 33 | 90.92 | PADU | STABIL | ya | tidak |
| MMYT | Consumer Cyclical | 2020-08-21 | 2020-11-16 | 60 | 90.75 | PADU | BERTANGGA | ya | tidak |
| FVRR | Communication Services | 2020-08-11 | 2020-11-06 | 62 | 84.54 | PADU | STABIL | ya | ya |
| KURA | Healthcare | 2020-08-25 | 2020-11-16 | 58 | 84.31 | PADU | BERTANGGA | ya | tidak |
| MTLS | Technology | 2020-08-24 | 2020-10-14 | 36 | 75.82 | PADU | LONJAKAN | ya | tidak |


**2020-09**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| JKS | Technology | 2020-09-04 | 2020-10-20 | 31 | 358.38 | SUPER PADU | STABIL | ya | tidak |
| PLUG | Industrials | 2020-09-24 | 2020-12-23 | 63 | 230.95 | SUPER PADU | BERTANGGA | ya | ya |
| NIO | Consumer Cyclical | 2020-09-24 | 2020-11-23 | 42 | 230.63 | SUPER PADU | BERTANGGA | ya | tidak |
| CPS | Consumer Cyclical | 2020-09-24 | 2020-12-04 | 50 | 219.83 | SUPER PADU | BERTANGGA | ya | tidak |
| GRWG | Consumer Cyclical | 2020-09-04 | 2020-11-27 | 58 | 171.47 | SUPER PADU | STABIL | ya | tidak |
| UPWK | Communication Services | 2020-09-04 | 2020-11-20 | 54 | 171.43 | SUPER PADU | LONJAKAN | ya | tidak |
| DQ | Technology | 2020-09-04 | 2020-10-20 | 31 | 165.57 | SUPER PADU | BERTANGGA | ya | tidak |
| NTLA | Healthcare | 2020-09-04 | 2020-12-04 | 63 | 162.64 | SUPER PADU | BERTANGGA | ya | ya |
| MSTR | Technology | 2020-09-04 | 2020-11-30 | 59 | 150.4 | SUPER PADU | BERTANGGA | ya | tidak |
| NET | Technology | 2020-09-14 | 2020-12-10 | 62 | 146.12 | SUPER PADU | BERTANGGA | ya | ya |


**2020-10**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ARVN | Healthcare | 2020-10-22 | 2021-01-19 | 59 | 356.85 | SUPER PADU | LONJAKAN | ya | tidak |
| SRRK | Healthcare | 2020-10-26 | 2021-01-25 | 61 | 355.75 | SUPER PADU | LONJAKAN | ya | ya |
| CLSK | Financial Services | 2020-10-08 | 2021-01-07 | 62 | 343.85 | SUPER PADU | STABIL | tidak | ya |
| INMB | Healthcare | 2020-10-21 | 2021-01-19 | 60 | 239.87 | SUPER PADU | STABIL | tidak | tidak |
| EDIT | Healthcare | 2020-10-02 | 2020-12-28 | 59 | 212.29 | SUPER PADU | LONJAKAN | ya | tidak |
| DQ | Technology | 2020-10-28 | 2021-01-27 | 61 | 211.63 | SUPER PADU | STABIL | ya | ya |
| LAR | Basic Materials | 2020-10-28 | 2021-01-19 | 55 | 190.57 | SUPER PADU | LONJAKAN | ya | tidak |
| COHU | Technology | 2020-10-28 | 2021-01-20 | 56 | 183.97 | SUPER PADU | BERTANGGA | ya | tidak |
| PDD | Consumer Cyclical | 2020-10-05 | 2021-01-05 | 63 | 167.85 | SUPER PADU | BERTANGGA | ya | ya |
| FATE | Healthcare | 2020-10-06 | 2020-12-22 | 54 | 143.96 | SUPER PADU | LONJAKAN | ya | tidak |


**2020-11**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| ARCT | Healthcare | 2020-11-09 | 2020-12-07 | 19 | 276.09 | SUPER PADU | STABIL | ya | tidak |
| BILI | Communication Services | 2020-11-03 | 2021-02-04 | 63 | 232.18 | SUPER PADU | BERTANGGA | ya | ya |
| AGNT | Real Estate | 2020-11-02 | 2021-02-02 | 62 | 193.73 | SUPER PADU | BERTANGGA | ya | ya |
| VIR | Healthcare | 2020-11-03 | 2021-01-27 | 57 | 184.29 | SUPER PADU | LONJAKAN | tidak | tidak |
| ALT | Healthcare | 2020-11-09 | 2021-02-09 | 62 | 176.67 | SUPER PADU | BERTANGGA | tidak | ya |
| CVM | Healthcare | 2020-11-03 | 2021-02-01 | 60 | 156.88 | SUPER PADU | LONJAKAN | ya | tidak |
| LOVE | Consumer Cyclical | 2020-11-02 | 2021-01-26 | 57 | 142.41 | SUPER PADU | BERTANGGA | tidak | tidak |
| MTLS | Technology | 2020-11-02 | 2021-01-19 | 52 | 139.39 | SUPER PADU | BERTANGGA | ya | tidak |
| FVRR | Communication Services | 2020-11-10 | 2021-02-11 | 63 | 134.43 | SUPER PADU | BERTANGGA | ya | ya |
| GOTU | Consumer Defensive | 2020-11-02 | 2021-01-27 | 58 | 125.4 | SUPER PADU | LONJAKAN | tidak | tidak |


**2020-12**

| ticker | sektor | tarikh_mula | tarikh_puncak | hari_ke_puncak | pct_naik_rendah | kumpulan | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|---|---|
| FCEL | Industrials | 2020-12-02 | 2021-02-09 | 46 | 328.83 | SUPER PADU | BERTANGGA | ya | tidak |
| HOV | Consumer Cyclical | 2020-12-14 | 2021-03-17 | 63 | 245.73 | SUPER PADU | STABIL | ya | ya |
| BLNK | Industrials | 2020-12-02 | 2021-01-26 | 36 | 222.81 | SUPER PADU | LONJAKAN | ya | tidak |
| FOSL | Consumer Cyclical | 2020-12-21 | 2021-01-27 | 24 | 168.56 | SUPER PADU | LONJAKAN | ya | tidak |
| JMIA | Consumer Cyclical | 2020-12-02 | 2021-02-10 | 47 | 167.06 | SUPER PADU | STABIL | ya | tidak |
| RICK | Consumer Cyclical | 2020-12-07 | 2021-03-01 | 56 | 158.47 | SUPER PADU | BERTANGGA | ya | tidak |
| TRIP | Consumer Cyclical | 2020-12-22 | 2021-03-17 | 57 | 143.54 | SUPER PADU | BERTANGGA | ya | tidak |
| SIG | Consumer Cyclical | 2020-12-14 | 2021-03-16 | 62 | 140.01 | SUPER PADU | BERTANGGA | ya | ya |
| RVP | Healthcare | 2020-12-07 | 2021-02-01 | 37 | 135.75 | SUPER PADU | LONJAKAN | ya | tidak |
| ACB | Healthcare | 2020-12-29 | 2021-02-10 | 29 | 131.86 | SUPER PADU | BERTANGGA | ya | tidak |


### Semua run SUPER PADU (≥ 100%)

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | jenis_kenaikan | entry_sah | masih_naik |
|---|---|---|---|---|---|---|---|
| PENN | Consumer Cyclical | 2020-03-18 | 54 | 896.53 | BERTANGGA | tidak | tidak |
| NVAX | Healthcare | 2020-05-01 | 60 | 805.55 | BERTANGGA | ya | tidak |
| CHEF | Consumer Defensive | 2020-03-18 | 56 | 464.51 | STABIL | tidak | tidak |
| SSL | Basic Materials | 2020-03-12 | 60 | 423.33 | STABIL | tidak | tidak |
| TPC | Industrials | 2020-03-18 | 56 | 412.64 | STABIL | tidak | tidak |
| GCO | Consumer Cyclical | 2020-03-18 | 56 | 408.15 | STABIL | tidak | tidak |
| ARCT | Healthcare | 2020-04-03 | 34 | 388.43 | STABIL | ya | tidak |
| JKS | Technology | 2020-09-04 | 31 | 358.38 | STABIL | ya | tidak |
| ARVN | Healthcare | 2020-10-22 | 59 | 356.85 | LONJAKAN | ya | tidak |
| SRRK | Healthcare | 2020-10-26 | 61 | 355.75 | LONJAKAN | ya | ya |
| PLAY | Communication Services | 2020-03-18 | 56 | 355.37 | LONJAKAN | tidak | tidak |
| TLRY | Healthcare | 2020-03-18 | 47 | 344.86 | LONJAKAN | ya | tidak |
| CLSK | Financial Services | 2020-10-08 | 62 | 343.85 | STABIL | tidak | ya |
| CPRI | Consumer Cyclical | 2020-03-18 | 56 | 329.7 | STABIL | tidak | tidak |
| FCEL | Industrials | 2020-12-02 | 46 | 328.83 | BERTANGGA | ya | tidak |
| JMIA | Consumer Cyclical | 2020-08-27 | 63 | 327.39 | STABIL | tidak | ya |
| SRG | Real Estate | 2020-03-18 | 56 | 324.8 | LONJAKAN | tidak | tidak |
| AER | Industrials | 2020-03-18 | 56 | 284.26 | STABIL | tidak | tidak |
| MHO | Consumer Cyclical | 2020-03-18 | 62 | 283.94 | STABIL | tidak | ya |
| ARCT | Healthcare | 2020-11-09 | 19 | 276.09 | STABIL | ya | tidak |
| CALY | Consumer Cyclical | 2020-03-18 | 56 | 272.04 | STABIL | tidak | tidak |
| W | Consumer Cyclical | 2020-02-28 | 50 | 263.04 | STABIL | tidak | tidak |
| DBI | Consumer Cyclical | 2020-03-18 | 56 | 259.32 | LONJAKAN | tidak | tidak |
| ACMR | Technology | 2020-03-16 | 45 | 246.28 | STABIL | ya | tidak |
| HOV | Consumer Cyclical | 2020-12-14 | 63 | 245.73 | STABIL | ya | ya |
| CNK | Communication Services | 2020-03-18 | 56 | 244.31 | STABIL | tidak | tidak |
| INMB | Healthcare | 2020-10-21 | 60 | 239.87 | STABIL | tidak | tidak |
| BILI | Communication Services | 2020-11-03 | 63 | 232.18 | BERTANGGA | ya | ya |
| VERI | Technology | 2020-08-31 | 63 | 230.97 | STABIL | tidak | ya |
| PLUG | Industrials | 2020-09-24 | 63 | 230.95 | BERTANGGA | ya | ya |
| NIO | Consumer Cyclical | 2020-09-24 | 42 | 230.63 | BERTANGGA | ya | tidak |
| CCS | Real Estate | 2020-03-18 | 62 | 228.69 | STABIL | tidak | ya |
| AIR | Industrials | 2020-03-18 | 56 | 223.22 | STABIL | tidak | tidak |
| BLNK | Industrials | 2020-12-02 | 36 | 222.81 | LONJAKAN | ya | tidak |
| CPS | Consumer Cyclical | 2020-09-24 | 50 | 219.83 | BERTANGGA | ya | tidak |
| HOV | Consumer Cyclical | 2020-03-12 | 61 | 215.39 | STABIL | tidak | ya |
| HUCK | Technology | 2020-03-12 | 59 | 214.05 | STABIL | tidak | tidak |
| EDIT | Healthcare | 2020-10-02 | 59 | 212.29 | LONJAKAN | ya | tidak |
| DQ | Technology | 2020-10-28 | 61 | 211.63 | STABIL | ya | ya |
| MUR | Energy | 2020-03-12 | 60 | 211.16 | STABIL | tidak | tidak |
| EPRT | Lain-lain | 2020-03-18 | 56 | 211.16 | STABIL | tidak | tidak |
| DKS | Consumer Cyclical | 2020-03-18 | 63 | 210.44 | BERTANGGA | tidak | ya |
| SHOP | Technology | 2020-04-02 | 63 | 207.87 | BERTANGGA | ya | ya |
| ETSY | Consumer Cyclical | 2020-03-20 | 63 | 207.71 | BERTANGGA | tidak | ya |
| OPCH | Healthcare | 2020-03-18 | 56 | 204.88 | STABIL | tidak | tidak |
| USFD | Consumer Defensive | 2020-03-18 | 56 | 203.97 | STABIL | tidak | tidak |
| GLPI | Lain-lain | 2020-03-18 | 56 | 198.16 | STABIL | tidak | tidak |
| GPI | Consumer Cyclical | 2020-03-18 | 55 | 193.95 | STABIL | tidak | tidak |
| AGNT | Real Estate | 2020-11-02 | 62 | 193.73 | BERTANGGA | ya | ya |
| TSLA | Consumer Cyclical | 2020-03-18 | 58 | 192.45 | BERTANGGA | tidak | tidak |
| LAR | Basic Materials | 2020-10-28 | 55 | 190.57 | LONJAKAN | ya | tidak |
| PAAS | Basic Materials | 2020-03-16 | 53 | 187.55 | BERTANGGA | tidak | tidak |
| REZI | Industrials | 2020-03-18 | 63 | 186.72 | STABIL | tidak | ya |
| EVER | Communication Services | 2020-04-03 | 57 | 185.28 | BERTANGGA | ya | tidak |
| VIR | Healthcare | 2020-11-03 | 57 | 184.29 | LONJAKAN | tidak | tidak |
| COHU | Technology | 2020-10-28 | 56 | 183.97 | BERTANGGA | ya | tidak |
| ENPH | Technology | 2020-03-16 | 45 | 182.87 | BERTANGGA | ya | tidak |
| LYFT | Technology | 2020-03-18 | 56 | 181.42 | STABIL | ya | tidak |
| NCLH | Consumer Cyclical | 2020-03-12 | 60 | 179.79 | STABIL | tidak | tidak |
| NSP | Industrials | 2020-03-18 | 55 | 179.73 | STABIL | tidak | tidak |


(dipaparkan 60 teratas daripada 279)


### Run BERTANGGA (S2) — 40 teratas

| ticker | sektor | tarikh_mula | hari_ke_puncak | pct_naik_rendah | bilangan_kaki | pct_hari_atas_ema21 | kumpulan |
|---|---|---|---|---|---|---|---|
| PENN | Consumer Cyclical | 2020-03-18 | 54 | 896.53 | 5 | 63.6 | SUPER PADU |
| NVAX | Healthcare | 2020-05-01 | 60 | 805.55 | 6 | 96.7 | SUPER PADU |
| FCEL | Industrials | 2020-12-02 | 46 | 328.83 | 4 | 100.0 | SUPER PADU |
| BILI | Communication Services | 2020-11-03 | 63 | 232.18 | 6 | 95.2 | SUPER PADU |
| PLUG | Industrials | 2020-09-24 | 63 | 230.95 | 4 | 87.1 | SUPER PADU |
| NIO | Consumer Cyclical | 2020-09-24 | 42 | 230.63 | 4 | 100.0 | SUPER PADU |
| CPS | Consumer Cyclical | 2020-09-24 | 50 | 219.83 | 3 | 93.2 | SUPER PADU |
| DKS | Consumer Cyclical | 2020-03-18 | 63 | 210.44 | 5 | 75.0 | SUPER PADU |
| SHOP | Technology | 2020-04-02 | 63 | 207.87 | 2 | 93.3 | SUPER PADU |
| ETSY | Consumer Cyclical | 2020-03-20 | 63 | 207.71 | 4 | 79.7 | SUPER PADU |
| AGNT | Real Estate | 2020-11-02 | 62 | 193.73 | 3 | 78.3 | SUPER PADU |
| TSLA | Consumer Cyclical | 2020-03-18 | 58 | 192.45 | 3 | 76.3 | SUPER PADU |
| PAAS | Basic Materials | 2020-03-16 | 53 | 187.55 | 4 | 66.7 | SUPER PADU |
| EVER | Communication Services | 2020-04-03 | 57 | 185.28 | 5 | 100.0 | SUPER PADU |
| COHU | Technology | 2020-10-28 | 56 | 183.97 | 2 | 100.0 | SUPER PADU |
| ENPH | Technology | 2020-03-16 | 45 | 182.87 | 4 | 79.5 | SUPER PADU |
| ALT | Healthcare | 2020-11-09 | 62 | 176.67 | 4 | 66.7 | SUPER PADU |
| FUTU | Financial Services | 2020-03-23 | 63 | 175.0 | 5 | 92.9 | SUPER PADU |
| PDD | Consumer Cyclical | 2020-04-02 | 63 | 174.34 | 4 | 100.0 | SUPER PADU |
| UBER | Technology | 2020-03-18 | 55 | 171.41 | 2 | 84.0 | SUPER PADU |
| DECK | Consumer Cyclical | 2020-03-18 | 53 | 170.11 | 4 | 68.8 | SUPER PADU |
| PDD | Consumer Cyclical | 2020-10-05 | 63 | 167.85 | 4 | 96.7 | SUPER PADU |
| DQ | Technology | 2020-09-04 | 31 | 165.57 | 2 | 96.4 | SUPER PADU |
| NTLA | Healthcare | 2020-09-04 | 63 | 162.64 | 3 | 89.8 | SUPER PADU |
| RICK | Consumer Cyclical | 2020-12-07 | 56 | 158.47 | 7 | 94.4 | SUPER PADU |
| WPM | Basic Materials | 2020-03-16 | 45 | 151.17 | 3 | 95.0 | SUPER PADU |
| MSTR | Technology | 2020-09-04 | 59 | 150.4 | 2 | 85.2 | SUPER PADU |
| NET | Technology | 2020-09-14 | 62 | 146.12 | 3 | 96.6 | SUPER PADU |
| TRIP | Consumer Cyclical | 2020-12-22 | 57 | 143.54 | 3 | 98.2 | SUPER PADU |
| CHEF | Consumer Defensive | 2020-10-28 | 62 | 143.48 | 2 | 100.0 | SUPER PADU |
| DNLI | Healthcare | 2020-09-04 | 63 | 142.64 | 4 | 98.4 | SUPER PADU |
| LOVE | Consumer Cyclical | 2020-11-02 | 57 | 142.41 | 3 | 79.3 | SUPER PADU |
| SIG | Consumer Cyclical | 2020-12-14 | 62 | 140.01 | 2 | 91.4 | SUPER PADU |
| MTLS | Technology | 2020-11-02 | 52 | 139.39 | 4 | 89.1 | SUPER PADU |
| LYFT | Technology | 2020-10-28 | 51 | 137.49 | 2 | 100.0 | SUPER PADU |
| SE | Consumer Cyclical | 2020-04-28 | 49 | 135.85 | 2 | 100.0 | SUPER PADU |
| CRNC | Technology | 2020-09-24 | 62 | 135.8 | 4 | 96.3 | SUPER PADU |
| ST | Technology | 2020-03-18 | 56 | 135.56 | 3 | 64.9 | SUPER PADU |
| RUN | Technology | 2020-03-16 | 58 | 135.07 | 3 | 64.4 | SUPER PADU |
| FVRR | Communication Services | 2020-11-10 | 63 | 134.43 | 3 | 87.3 | SUPER PADU |


(daripada 513 run BERTANGGA)


### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)

n peristiwa PADU dalam S2, populasi keputusan (a) = **272** (rujukan: semua peristiwa = 1038). < 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat.


Peristiwa sah: **12858** (populasi keputusan 3646).


## 3. Step 2b — kohort "naik dan naik"

Dijejak 515 run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari tarikh_sah.


| Metrik | Nilai |
|---|---|
| % akhirnya melebihi +100% | **54.6%** |
| median %_naik_penuh | **107.2%** |
| median %_naik pada hari ke-63 | 46.5% |
| median hari ke puncak penuh | 193 |
| median MFE 252 selepas kos | 85.3% |
| median MAE 252 | -5.5% |
| median hari pegang Chandelier 4×ATR | 95 |
| median pulangan Chandelier selepas kos | 30.5% |
| terpotong hujung data | 0.0% |


Exit yang menyala dahulu:


| exit | n |
|---|---|
| bawah_ema9 | 177 |
| bawah_ma50 | 128 |
| hist_neg3 | 68 |
| bawah_ema21 | 60 |
| rsi_70_60 | 41 |
| hari_agihan | 24 |
| macd_bawah | 12 |
| trail_8pct | 4 |
| trail_2atr | 1 |


### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari

| kohort | n | median_naik_63 | pct_bertangga | pct_super | median_hari_ke_puncak |
|---|---|---|---|---|---|
| masih_naik = ya | 515 | 46.5 | 35.0 | 8.3 | 63.0 |
| reda dalam 63 hari | 2220 | 33.4 | 12.1 | 4.1 | 40.0 |


Kohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya diketahui pada hari ke-63.


## 4. Step 3 — populasi kuintil dan dedup

POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **6568** baris. Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **34** daripada 41; dibuang 7.


| buang | kerana | rho |
|---|---|---|
| j_ma150 | j_ma200 | 0.957 |
| cerun_ma200 | j_ma200 | 0.834 |
| roc60 | cerun_ma50 | 0.935 |
| willr14 | stoch_k | 1.0 |
| julat10 | atr_pct | 0.84 |
| bb_pctb | cci20 | 0.926 |
| kelt_pos | j_ema21 | 0.9 |


Signal dibina: **219** (31 binari + 68 hujung kuintil + 120 pemicu × 1 konteks).


## 5. Step 4 — common & unique (ENTRY)

Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. N ujian ENTRY sebenar (populasi a, kumpulan A) = **876** baris (213 signal × 2 subset × 2 keluarga).


### Kelas (S2, kumpulan A, keluarga PADU)

| kelas | n |
|---|---|
| TIDAK BERGUNA | 189 |
| UNIQUE | 10 |
| SEDERHANA | 8 |
| COMMON BIASA | 7 |
| LANGKA | 4 |
| TERAS | 1 |


### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)

| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n | n_industri | n_minggu | purata_pct_naik_rendah | purata_hari_ke_puncak | pct_bertangga | pct_lonjakan | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| macd_cross&q5:bb_lebar | LANGKA | 13.67 | 0.0 | 0.4 | 0.71 | 33.899 | 19.329 | 90.32 | 5.031 | 31 | 21 | 10 | 83.78 | 54.4 | 100.0 | 0.0 |  |
| q5:julat20 | UNIQUE | 30.22 | 0.0 | 2.69 | 29.45 | 11.24 | 1.026 | 75.31 | 4.195 | 81 | 47 | 27 | 82.02 | 51.5 | 100.0 | 0.0 |  |
| q5:atr_pct | UNIQUE | 23.74 | 0.0 | 2.42 | 22.59 | 9.813 | 1.051 | 73.91 | 4.117 | 69 | 38 | 21 | 84.53 | 51.6 | 100.0 | 0.0 |  |
| q5:bb_lebar | UNIQUE | 35.25 | 0.0 | 3.36 | 32.34 | 10.491 | 1.09 | 73.4 | 4.089 | 94 | 53 | 27 | 80.42 | 52.0 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:bb_lebar | UNIQUE | 18.71 | 0.0 | 2.42 | 1.28 | 7.731 | 14.607 | 68.97 | 3.842 | 58 | 38 | 22 | 83.71 | 50.4 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:julat20 | UNIQUE | 15.11 | 0.0 | 2.15 | 1.19 | 7.025 | 12.749 | 68.0 | 3.788 | 50 | 35 | 23 | 85.0 | 49.8 | 100.0 | 0.0 |  |
| q5:j_ema9 | UNIQUE | 25.9 | 0.0 | 3.23 | 10.84 | 8.029 | 2.39 | 67.57 | 3.764 | 74 | 44 | 22 | 80.02 | 52.3 | 100.0 | 0.0 |  |
| rsi_lintas50&q5:atr_pct | LANGKA | 12.23 | 0.0 | 1.88 | 1.45 | 6.499 | 8.42 | 67.44 | 3.757 | 43 | 25 | 18 | 86.28 | 49.0 | 100.0 | 0.0 |  |
| q1:cerun_ema21 | TERAS | 53.24 | 0.0 | 6.45 | 17.13 | 8.252 | 3.109 | 65.71 | 3.661 | 140 | 60 | 33 | 72.7 | 53.5 | 100.0 | 0.0 |  |
| macd_cross&q1:cerun_ma50 | LANGKA | 10.07 | 0.0 | 1.61 | 0.71 | 6.245 | 14.242 | 63.64 | 3.545 | 33 | 25 | 17 | 84.57 | 55.7 | 100.0 | 0.0 |  |
| ema_crossback&q5:bb_lebar | LANGKA | 8.63 | 0.0 | 1.61 | 0.42 | 5.353 | 20.531 | 60.0 | 3.342 | 30 | 22 | 15 | 82.65 | 48.8 | 100.0 | 0.0 |  |
| q1:cerun_ma50 | UNIQUE | 23.74 | 0.0 | 4.97 | 19.15 | 4.774 | 1.24 | 53.16 | 2.962 | 79 | 43 | 29 | 73.82 | 54.5 | 100.0 | 0.0 |  |
| q1:roc20 | UNIQUE | 48.2 | 0.0 | 10.08 | 27.03 | 4.782 | 1.784 | 52.83 | 2.943 | 159 | 63 | 33 | 71.99 | 55.3 | 100.0 | 0.0 |  |
| q1:j_52w_tinggi | UNIQUE | 25.18 | 0.0 | 5.78 | 21.9 | 4.357 | 1.15 | 50.57 | 2.817 | 87 | 45 | 27 | 71.78 | 55.6 | 100.0 | 0.0 |  |
| q5:rs_spy_3b | UNIQUE | 20.86 | 0.0 | 6.05 | 20.78 | 3.449 | 1.004 | 47.06 | 2.621 | 85 | 43 | 27 | 79.17 | 51.6 | 100.0 | 0.0 |  |


### Rujukan S1 (semua run layak)

| signal | kelas | K_padu | lift | presisi | lift_presisi | n | tanda |
|---|---|---|---|---|---|---|---|
| macd_cross&q5:julat20 | UNIQUE | 18.3 | 5.357 | 91.56 | 2.224 | 154 | LONJAKAN BERITA |
| macd_cross&q5:atr_pct | UNIQUE | 16.14 | 5.197 | 90.65 | 2.202 | 139 | LONJAKAN BERITA |
| macd_cross&q5:bb_lebar | UNIQUE | 18.73 | 4.308 | 89.63 | 2.177 | 164 | LONJAKAN BERITA |
| q5:julat20 | UNIQUE | 41.35 | 3.917 | 85.83 | 2.085 | 381 | LONJAKAN BERITA |
| q5:atr_pct | UNIQUE | 36.31 | 3.654 | 85.38 | 2.074 | 342 | LONJAKAN BERITA |
| q5:bb_lebar | UNIQUE | 42.65 | 3.121 | 83.09 | 2.018 | 408 | LONJAKAN BERITA |
| rsi_lintas50&q5:julat20 | UNIQUE | 19.6 | 3.155 | 81.63 | 1.983 | 196 | LONJAKAN BERITA |
| q1:cerun_ema21 | TERAS | 56.05 | 2.099 | 76.16 | 1.85 | 562 | LONJAKAN BERITA |
| q1:roc20 | TERAS | 52.74 | 2.264 | 72.73 | 1.767 | 550 |  |
| q1:sektor_1b | TERAS | 53.17 | 2.167 | 66.11 | 1.606 | 599 |  |


### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja

S3 mengandungi 1616 run; ia **bukan keluarga carian** (tidak menambah N). 20.4% daripadanya BERTANGGA lawan 16.4% keseluruhan.


### Keluarga SUPER PADU (FDR sendiri)

| signal | kelas | K_super | lift | lift_rawak | n | tanda |
|---|---|---|---|---|---|---|
| macd_cross&q5:julat20 | UNIQUE | 33.33 | 124.0 | 48.444 | 27 |  |
| macd_cross&q5:bb_lebar | UNIQUE | 37.5 | 93.0 | 53.027 | 31 |  |
| macd_cross&q5:atr_pct | UNIQUE | 29.17 | 72.333 | 41.243 | 23 |  |
| q5:atr_pct | TERAS | 75.0 | 31.0 | 3.32 | 69 |  |
| q5:julat20 | TERAS | 79.17 | 29.45 | 2.688 | 81 |  |
| rsi_lintas50&q5:atr_pct | TERAS | 50.0 | 26.571 | 34.421 | 43 |  |
| rsi_lintas50&q5:julat20 | TERAS | 54.17 | 25.187 | 45.71 | 50 |  |
| q5:bb_lebar | TERAS | 83.33 | 24.8 | 2.577 | 94 |  |
| rsi_lintas50&q5:bb_lebar | TERAS | 58.33 | 24.111 | 45.552 | 58 |  |
| ema_crossback&q5:atr_pct | UNIQUE | 29.17 | 19.727 | 72.667 | 26 |  |
| macd_cross&q1:cerun_ma50 | UNIQUE | 29.17 | 18.083 | 41.243 | 33 |  |
| q5:j_ema9 | TERAS | 58.33 | 18.083 | 5.383 | 74 |  |
| macd_cross&q1:j_52w_tinggi | UNIQUE | 16.67 | 17.714 | 22.947 | 26 |  |
| ema_crossback&q5:julat20 | UNIQUE | 25.0 | 16.909 | 59.455 | 27 |  |
| ema_crossback&q5:bb_lebar | UNIQUE | 25.0 | 15.5 | 59.455 | 30 |  |
| q1:cerun_ema21 | TERAS | 75.0 | 11.625 | 4.379 | 140 |  |
| macd_cross&q1:sektor_1b | UNIQUE | 29.17 | 9.864 | 36.333 | 48 |  |
| q5:rs_spy_3b | UNIQUE | 45.83 | 7.578 | 2.206 | 85 |  |
| q1:cerun_ma50 | UNIQUE | 37.5 | 7.541 | 1.958 | 79 |  |
| rsi_lintas50&q1:cerun_ma50 | UNIQUE | 16.67 | 7.294 | 10.765 | 32 |  |


### PEMICU YANG TIDAK MEMBEZAKAN

Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.


| signal | kelas | K_padu | K_biasa | K_gagal | K_rawak | lift | lift_rawak | presisi | lift_presisi | n |
|---|---|---|---|---|---|---|---|---|---|---|
| b:donchian20 | TIDAK BERGUNA | 1.44 | 0.0 | 11.96 | 7.09 | 0.12 | 0.203 | 2.2 | 0.122 | 91 |
| b:ema_crossback | TIDAK BERGUNA | 35.97 | 100.0 | 26.48 | 3.27 | 0.36 | 11.006 | 22.66 | 1.262 | 256 |
| b:gap_and_go | TIDAK BERGUNA | 2.88 | 0.0 | 1.21 | 0.48 | 2.379 | 6.022 | 40.0 | 2.228 | 15 |
| b:macd_cross | TIDAK BERGUNA | 26.62 | 0.0 | 22.85 | 3.52 | 1.165 | 7.569 | 21.66 | 1.207 | 217 |
| b:pocket_pivot | TIDAK BERGUNA | 15.83 | 100.0 | 23.25 | 9.19 | 0.158 | 1.722 | 12.12 | 0.675 | 198 |
| b:rsi_lintas50 | COMMON BIASA | 53.96 | 100.0 | 45.16 | 5.87 | 0.54 | 9.196 | 21.63 | 1.205 | 430 |


**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis yang diuji dalam kajian ini, dan ia disokong oleh data 2025.


### Corong ke Step 7
16 signal diteruskan (had 30; layak sebelum had: 16).


## 6. Step 5 — HOLD

> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana berjaya. Semua CALON.


### Kelas pullback

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| AMARAN | 5673 | 70.5 | -14.28 | 9.7 |
| PULLBACK PASARAN | 708 | 87.9 | -8.79 | 6.3 |
| PULLBACK SIHAT | 2065 | 89.1 | -8.56 | 7.5 |


Pullback yang trend sahamnya utuh (SIHAT 89.1%, PASARAN 87.9%) menyambung ke puncak baru jauh lebih kerap daripada pullback AMARAN (70.5%). Ini sokongan paling jelas bagi falsafah "pegang selagi naik".


### Grid 18 peraturan HOLD (deskriptif)

| nama | n | pct_sambung_puncak_baru | purata_kedalaman | purata_hari_pulih |
|---|---|---|---|---|
| X=5%,Y=ema9 | 8 | 87.5 | -5.0 | 4.6 |
| X=5%,Y=ema21 | 3158 | 92.0 | -7.51 | 5.8 |
| X=5%,Y=ma50 | 4539 | 88.4 | -8.8 | 7.2 |
| X=7%,Y=ema9 | 2137 | 93.1 | -5.94 | 4.9 |
| X=7%,Y=ema21 | 3541 | 92.0 | -7.36 | 5.7 |
| X=7%,Y=ma50 | 4874 | 89.0 | -8.61 | 6.9 |
| X=10%,Y=ema9 | 4303 | 90.9 | -7.17 | 6.1 |
| X=10%,Y=ema21 | 4681 | 90.6 | -7.66 | 6.2 |
| X=10%,Y=ma50 | 5451 | 89.0 | -8.61 | 7.0 |
| X=12%,Y=ema9 | 5226 | 89.6 | -7.84 | 6.7 |
| X=12%,Y=ema21 | 5413 | 89.4 | -8.11 | 6.7 |
| X=12%,Y=ma50 | 5880 | 88.2 | -8.79 | 7.2 |
| X=15%,Y=ema9 | 6237 | 87.6 | -8.74 | 7.4 |
| X=15%,Y=ema21 | 6319 | 87.4 | -8.88 | 7.4 |
| X=15%,Y=ma50 | 6539 | 86.7 | -9.26 | 7.6 |
| X=20%,Y=ema9 | 7166 | 85.0 | -9.84 | 8.1 |
| X=20%,Y=ema21 | 7192 | 84.9 | -9.89 | 8.2 |
| X=20%,Y=ma50 | 7268 | 84.4 | -10.07 | 8.2 |


### Common/unique HOLD (lulus FDR)

9 / 18 signal HOLD lulus BH-FDR q ≤ 0.01: `b:macd_atas0`, `b:atas_awan`, `b:tenkan_atas`, `b:outside_day`, `b:nr7`, `b:vcp`, `b:sektor_atas_ma50`, `b:supertrend_naik`, `b:psar_naik`


| nama | subset | n | K_padu | K_gagal | lift | presisi | lift_presisi | kelas |
|---|---|---|---|---|---|---|---|---|
| b:macd_cross | S1 | 2 | 0.03 | 0.0 | 2.614 | 100.0 | 1.307 | TIDAK BERGUNA |
| b:garis_rs_tinggi | S1 | 13 | 0.2 | 0.0 | 16.991 | 100.0 | 1.307 | TIDAK BERGUNA |
| b:vcp | S1 | 481 | 7.15 | 0.96 | 7.466 | 96.05 | 1.255 | LANGKA |
| b:psar_naik | S1 | 2121 | 31.12 | 5.54 | 5.613 | 94.81 | 1.239 | UNIQUE |
| b:atas_ema21 | S1 | 1961 | 28.32 | 6.6 | 4.289 | 93.32 | 1.22 | UNIQUE |
| b:bb_squeeze | S2 | 22 | 1.28 | 0.0 | 26.318 | 100.0 | 1.196 | TIDAK BERGUNA |
| b:macd_cross | S2 | 1 | 0.06 | 0.0 | 1.196 | 100.0 | 1.196 | TIDAK BERGUNA |
| b:garis_rs_tinggi | S2 | 1 | 0.06 | 0.0 | 1.196 | 100.0 | 1.196 | TIDAK BERGUNA |
| b:supertrend_naik | S1 | 4448 | 62.5 | 20.61 | 3.032 | 90.8 | 1.187 | TERAS |
| b:vcp | S2 | 124 | 7.05 | 0.89 | 7.916 | 97.58 | 1.167 | LANGKA |
| b:tenkan_atas | S1 | 4675 | 64.42 | 25.81 | 2.496 | 89.05 | 1.164 | TERAS |
| b:psar_naik | S2 | 620 | 35.06 | 5.34 | 6.564 | 97.1 | 1.162 | UNIQUE |
| b:atas_ma50 | S1 | 3855 | 53.03 | 21.57 | 2.458 | 88.9 | 1.162 | TERAS |
| b:atas_ema21 | S2 | 676 | 37.91 | 7.42 | 5.111 | 96.3 | 1.152 | UNIQUE |
| b:macd_atas0 | S1 | 5025 | 67.87 | 32.21 | 2.107 | 87.28 | 1.141 | TERAS |
| b:atas_awan | S1 | 4224 | 56.9 | 27.57 | 2.064 | 87.05 | 1.138 | TERAS |
| b:hammer | S2 | 51 | 2.8 | 0.89 | 3.14 | 94.12 | 1.126 | TIDAK BERGUNA |
| b:supertrend_naik | S2 | 1334 | 72.45 | 26.71 | 2.713 | 93.25 | 1.116 | TERAS |
| b:pullback_dalam_7pct | S1 | 6098 | 80.21 | 46.12 | 1.739 | 85.0 | 1.111 | SEDERHANA |
| b:nr7 | S2 | 172 | 9.26 | 3.86 | 2.401 | 92.44 | 1.106 | TIDAK BERGUNA |


## 7. Step 6 — EXIT (semua CALON)

> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.


| nama | n | pct_menyala | median_hari_dari_puncak | median_pulangan_exit | median_pct_kekal | kadar_exit_palsu |
|---|---|---|---|---|---|---|
| atr_lonjak_15x | 979 | 37.4 | 4.0 | -2.87 | -10.1 | 63.2 |
| bawah_ema21 | 2616 | 99.9 | -30.5 | -1.66 | -6.7 | 80.9 |
| bawah_ema9 | 2618 | 100.0 | -35.0 | -1.43 | -5.1 | 80.4 |
| bawah_ma50 | 2560 | 97.7 | -28.0 | -1.29 | -5.2 | 77.9 |
| chandelier_4atr | 1814 | 69.3 | 12.0 | -1.23 | -3.6 | 61.4 |
| climax_25_15h | 1294 | 49.4 | -20.0 | 15.37 | 50.2 | 76.9 |
| div_macd | 2394 | 91.4 | -27.0 | 5.79 | 25.4 | 74.6 |
| div_rsi | 2264 | 86.4 | -18.0 | 8.22 | 37.4 | 71.7 |
| gap_besar | 489 | 18.7 | -8.0 | 29.68 | 71.2 | 75.3 |
| hari_agihan | 2153 | 82.2 | 2.0 | 3.92 | 19.3 | 66.7 |
| hist_neg3 | 2608 | 99.6 | -21.0 | -0.06 | 0.3 | 76.9 |
| jauh_ma50_2x | 1438 | 54.9 | -18.0 | 14.44 | 57.5 | 72.8 |
| macd_bawah | 2597 | 99.2 | -19.0 | 1.04 | 6.1 | 76.2 |
| pullback_amaran | 2572 | 98.2 | -17.5 | -5.49 | -21.9 | 87.3 |
| rsi_70_60 | 1969 | 75.2 | -5.0 | 10.49 | 43.8 | 71.8 |
| trail_10pct | 2362 | 90.2 | 2.0 | -2.95 | -11.1 | 74.1 |
| trail_15pct | 1678 | 64.1 | 8.0 | -6.75 | -27.1 | 69.5 |
| trail_2atr | 2608 | 99.6 | -14.0 | -0.18 | 0.2 | 74.8 |
| trail_3atr | 2396 | 91.5 | 5.0 | 0.15 | 2.9 | 68.5 |
| trail_8pct | 2541 | 97.0 | -15.0 | -2.17 | -8.6 | 76.1 |


`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala 28–35 hari sebelum puncak dan mengekalkan hanya -5% hingga -7% keuntungan. Kadar exit palsu 61%–87%.


**Keluarga EXIT: 0 / 68 signal lulus BH-FDR q ≤ 0.01.** Tiada signal EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas kawalan pelbagai ujian.


## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)

Setiap signal corong diimbas atas **semua** hari universe 2020 (538,959 baris (ticker, hari); 460,249 selepas topeng universe). Kadar asas KAWALAN RAWAK (MFE63 ≥ 30%) = 28.91%.


| signal | n_kemunculan | kadar_tepat_mfe30 | lift_tepat | kadar_palsu_bawah10 | kadar_tepat_bertangga | ketulenan_trend_median | mfe63_p50 | mfe63_p75 | mfe63_p90 | pct_mfe63_ge30 | pct_mfe63_ge100 | mfe252_p90 | pct_mfe252_ge100 | median_hari_mfe63 | jangkaan_henti2atr | kadar_menang | kapasiti | tanda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| macd_cross&q5:bb_lebar | 3710 | 54.29 | 1.878 | 12.64 | 5.39 | 74.6 | 32.58 | 51.13 | 80.01 | 54.29 | 6.04 | 232.09 | 42.37 | 49.0 | 18.06 | 65.82 | TULANG BELAKANG |  |
| q5:julat20 | 133238 | 50.29 | 1.74 | 16.95 | 7.25 | 73.5 | 30.17 | 51.06 | 80.15 | 50.29 | 5.82 | 237.76 | 42.07 | 47.0 | 16.523 | 59.2 | TULANG BELAKANG |  |
| q5:atr_pct | 98758 | 57.45 | 1.987 | 11.51 | 7.99 | 71.7 | 34.68 | 56.62 | 88.26 | 57.45 | 7.4 | 269.32 | 49.72 | 45.0 | 20.343 | 65.57 | TULANG BELAKANG |  |
| q5:bb_lebar | 141788 | 48.38 | 1.673 | 18.13 | 7.08 | 75.9 | 28.92 | 49.31 | 78.0 | 48.38 | 5.42 | 226.29 | 39.25 | 48.0 | 15.885 | 58.18 | TULANG BELAKANG |  |
| rsi_lintas50&q5:bb_lebar | 5548 | 43.31 | 1.498 | 15.84 | 6.69 | 80.4 | 26.2 | 43.39 | 67.92 | 43.31 | 4.34 | 217.04 | 40.3 | 40.0 | 15.238 | 62.2 | TULANG BELAKANG | BUNYI LATAR |
| rsi_lintas50&q5:julat20 | 5803 | 42.93 | 1.485 | 15.65 | 6.51 | 80.4 | 26.07 | 42.99 | 67.94 | 42.93 | 4.29 | 223.31 | 41.41 | 40.0 | 14.942 | 61.35 | TULANG BELAKANG | BUNYI LATAR |
| q5:j_ema9 | 49435 | 39.96 | 1.382 | 22.38 | 5.84 | 88.7 | 24.0 | 42.12 | 68.4 | 39.96 | 4.28 | 204.86 | 33.39 | 46.0 | 12.311 | 52.27 | TULANG BELAKANG | BUNYI LATAR |
| rsi_lintas50&q5:atr_pct | 6221 | 45.02 | 1.557 | 14.63 | 7.19 | 80.0 | 27.28 | 44.01 | 69.33 | 45.02 | 4.65 | 231.36 | 43.58 | 40.0 | 15.376 | 61.61 | TULANG BELAKANG |  |
| q1:cerun_ema21 | 75909 | 49.89 | 1.726 | 20.11 | 6.98 | 61.4 | 29.91 | 51.03 | 78.75 | 49.89 | 5.34 | 223.0 | 38.74 | 48.0 | 15.337 | 56.85 | TULANG BELAKANG |  |
| macd_cross&q1:cerun_ma50 | 3485 | 48.41 | 1.674 | 12.17 | 4.73 | 72.0 | 29.02 | 45.74 | 68.05 | 48.41 | 3.53 | 209.32 | 38.28 | 49.0 | 15.846 | 68.06 | TULANG BELAKANG |  |
| ema_crossback&q5:bb_lebar | 1885 | 39.31 | 1.36 | 25.31 | 5.09 | 75.0 | 22.43 | 45.03 | 79.14 | 39.31 | 6.53 | 235.28 | 40.64 | 43.0 | 13.704 | 49.87 | TULANG BELAKANG |  |
| macd_cross&q1:sektor_1b | 3912 | 44.53 | 1.54 | 16.64 | 5.19 | 75.9 | 26.7 | 44.52 | 65.13 | 44.53 | 3.02 | 189.45 | 32.29 | 49.0 | 15.252 | 64.95 | TULANG BELAKANG |  |
| q1:cerun_ma50 | 84524 | 50.47 | 1.746 | 12.91 | 7.01 | 71.0 | 30.25 | 48.91 | 74.37 | 50.47 | 4.56 | 217.95 | 40.53 | 44.0 | 17.251 | 66.01 | TULANG BELAKANG |  |
| q1:roc20 | 122920 | 39.72 | 1.374 | 27.05 | 5.96 | 61.5 | 23.27 | 42.79 | 67.99 | 39.72 | 3.73 | 189.64 | 30.57 | 46.0 | 11.611 | 50.79 | TULANG BELAKANG | BUNYI LATAR |
| q1:j_52w_tinggi | 97312 | 53.68 | 1.857 | 15.52 | 6.97 | 68.9 | 32.28 | 51.7 | 76.73 | 53.68 | 4.82 | 226.56 | 45.55 | 47.0 | 16.167 | 58.5 | TULANG BELAKANG |  |
| q5:rs_spy_3b | 92105 | 39.98 | 1.383 | 22.14 | 7.22 | 85.3 | 24.14 | 41.72 | 67.11 | 39.98 | 3.91 | 194.47 | 29.74 | 49.0 | 12.875 | 52.05 | TULANG BELAKANG | BUNYI LATAR |


Taburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. p90 dan % ≥ 100% ialah pembeza, bukan median.


**Lift jatuh besar antara Step 4 dan Step 7** (contoh `macd_cross&q5:bb_lebar`: lift 33.90 dalam populasi peristiwa → lift_tepat 1.88 atas semua hari universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. Angka Step 7 yang lebih dekat dengan dagangan sebenar.


### Penapis Step 7.4
128 kombinasi signal × penapis diuji (0 lulus kriteria "buang ≥ 30% palsu dan ≤ 10% benar").


**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis dipradaftar. Ini keputusan negatif yang bersih.


10 contoh penapis terbaik (ikut % palsu dibuang):


| signal | buang_palsu_pct | buang_benar_pct |
|---|---|---|
| q1:cerun_ema21 | penapis:harga_atas_ma50 | 98.2 | 98.5 |
| q1:cerun_ema21 | penapis:lapis_ge_3 | 98.2 | 98.1 |
| macd_cross&q1:cerun_ma50 | penapis:lapis_ge_3 | 97.6 | 96.7 |
| q1:j_52w_tinggi | penapis:lapis_ge_3 | 95.7 | 92.1 |
| q1:cerun_ma50 | penapis:lapis_ge_3 | 94.1 | 95.0 |
| q1:roc20 | penapis:harga_atas_ma50 | 92.6 | 92.4 |
| q1:roc20 | penapis:lapis_ge_3 | 88.7 | 91.6 |
| rsi_lintas50&q5:atr_pct | penapis:vol_n50_ge_1.5 | 88.2 | 87.7 |
| ema_crossback&q5:bb_lebar | penapis:vol_n50_ge_1.5 | 87.8 | 86.0 |
| rsi_lintas50&q5:julat20 | penapis:vol_n50_ge_1.5 | 87.2 | 86.7 |


## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)

Set kemasukan: gabungan semua kemunculan 11 signal yang lulus Step 7 = 219,917 (ticker, tarikh) unik, disampel berlapis ikut bulan ke **24,000** (benih 42; SPEC §13.9). Grid 18 HOLD × 13 EXIT = **234** sistem.


### TIGA RUJUKAN WAJIB

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_menang | purata_kalah | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 | pct_terpotong_data | siri_kalah_terpanjang |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 24000 | 45.54 | 60.66 | 60.665 | 81.76 | 80.51 | 28.27 | 252.0 | -12.75 | 0.0 | 100.0 | 0.0 | 9 |
| REF_chandelier_4atr | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 47.78 | 13.88 | 74.8 | -8.59 | 84.4 | 2.3 | 0.0 | 102 |
| REF_jual_hari63 | 24000 | 12.14 | 15.0 | 15.002 | 67.8 | 32.27 | 21.35 | 63.0 | -10.19 | 92.1 | 0.0 | 0.0 | 54 |


**Keputusan: rujukan "pegang tanpa jual hingga hari ke-252" menang, dan 0 / 234 sistem mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = 60.665%). Mengikut arahan Step 7b.4, jawapan kajian ialah **"jangan jual"** — dan itu dilaporkan sebagai penemuan, bukan kegagalan.


### 15 sistem terbaik daripada 234

| sistem | n | median_pulangan | purata_pulangan | jangkaan | kadar_menang | purata_hari_pegang | mae_median | pct_exit_terlalu_awal | pct_terbuka_hari252 |
|---|---|---|---|---|---|---|---|---|---|
| hari_agihan|X=20%,Y=ma50 | 24000 | 4.49 | 22.29 | 22.286 | 57.32 | 86.5 | -8.15 | 79.4 | 6.1 |
| hari_agihan|X=15%,Y=ma50 | 24000 | 4.58 | 21.29 | 21.285 | 57.55 | 83.5 | -8.05 | 80.0 | 5.6 |
| rsi_70_60|X=20%,Y=ma50 | 24000 | 13.08 | 20.95 | 20.945 | 70.92 | 97.7 | -8.25 | 79.5 | 9.3 |
| hari_agihan|X=12%,Y=ma50 | 24000 | 4.62 | 20.05 | 20.045 | 57.67 | 79.9 | -7.99 | 80.8 | 5.1 |
| chandelier_4atr|X=20%,Y=ma50 | 24000 | 3.21 | 19.8 | 19.797 | 54.3 | 76.2 | -8.61 | 84.2 | 2.4 |
| chandelier_4atr|X=15%,Y=ma50 | 24000 | 3.25 | 19.78 | 19.783 | 54.32 | 75.6 | -8.6 | 84.2 | 2.3 |
| chandelier_4atr|X=12%,Y=ma50 | 24000 | 3.22 | 19.68 | 19.676 | 54.3 | 75.1 | -8.59 | 84.3 | 2.3 |
| chandelier_4atr|X=12%,Y=ema21 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=7%,Y=ema9 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=5%,Y=ema9 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=5%,Y=ma50 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=12%,Y=ema9 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=5%,Y=ema21 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=7%,Y=ema21 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |
| chandelier_4atr|X=10%,Y=ema9 | 24000 | 3.22 | 19.61 | 19.608 | 54.31 | 74.8 | -8.59 | 84.4 | 2.3 |


Perhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.


## 10. Step 8 — kawalan kebetulan

### Ujian label rawak dan FDR per keluarga

| keluarga | N | lulus_fdr | ambang_p |
|---|---|---|---|
| ENTRY/PADU | 16 | 16 | 0.002997002997002997 |
| ENTRY/SUPER PADU | 16 | 16 | 0.001998001998001998 |
| HOLD | 18 | 9 | 0.004975124378109453 |
| EXIT | 68 | 0 |  |
| SISTEM | 234 | 0 |  |


Perbandingan yang diminta arahan: **16 signal lulus FDR daripada 16 diuji**, manakala label rawak menghasilkan lift purata yang jauh lebih rendah (lajur `lift_purata_rawak` dalam `kawalan_rawak_bootstrap_2020.csv`).


### Jangkaan atas SEMUA kemunculan + ujian outlier

| signal | n_kemunculan | median_pulangan | jangkaan | jangkaan_tanpa_5pct_teratas | pct_rugi_lebih_10 | siri_kalah_terpanjang | jangkaan_bawah95_blok_ticker | jangkaan_bawah95_blok_minggu |
|---|---|---|---|---|---|---|---|---|
| macd_cross&q5:bb_lebar | 3710 | 12.21 | 18.06 | 11.844 | 24.1 | 8 | 16.825 | 12.848 |
| q5:julat20 | 133238 | 9.44 | 16.523 | 10.346 | 29.9 | 115 | 15.588 | 11.796 |
| q5:atr_pct | 98758 | 14.12 | 20.343 | 13.607 | 28.2 | 127 | 19.18 | 15.387 |
| q5:bb_lebar | 141788 | 8.73 | 15.885 | 9.94 | 27.9 | 111 | 15.048 | 11.289 |
| rsi_lintas50&q5:bb_lebar | 5548 | 8.52 | 15.238 | 9.076 | 27.3 | 15 | 13.737 | 12.258 |
| rsi_lintas50&q5:julat20 | 5803 | 7.96 | 14.942 | 8.609 | 28.5 | 15 | 13.509 | 12.045 |
| q5:j_ema9 | 49435 | 2.95 | 12.311 | 6.77 | 27.7 | 46 | 11.412 | 9.064 |
| rsi_lintas50&q5:atr_pct | 6221 | 8.24 | 15.376 | 9.024 | 29.9 | 21 | 13.785 | 12.421 |
| q1:cerun_ema21 | 75909 | 8.13 | 15.337 | 9.714 | 28.0 | 94 | 14.622 | 6.951 |
| macd_cross&q1:cerun_ma50 | 3485 | 12.06 | 15.846 | 11.125 | 19.3 | 8 | 14.881 | 9.944 |
| ema_crossback&q5:bb_lebar | 1885 | -0.07 | 13.704 | 5.569 | 38.0 | 14 | 10.483 | 8.031 |
| macd_cross&q1:sektor_1b | 3912 | 11.09 | 15.252 | 10.767 | 15.9 | 11 | 14.394 | 6.972 |
| q1:cerun_ma50 | 84524 | 12.83 | 17.251 | 12.058 | 22.4 | 118 | 16.376 | 11.786 |
| q1:roc20 | 122920 | 1.1 | 11.611 | 6.454 | 25.2 | 123 | 11.106 | 5.802 |
| q1:j_52w_tinggi | 97312 | 9.64 | 16.167 | 10.752 | 27.4 | 171 | 15.283 | 10.902 |
| q5:rs_spy_3b | 92105 | 2.92 | 12.875 | 7.314 | 23.2 | 113 | 11.724 | 10.477 |


### Keputusan gate demi gate

| signal | G1_sah_dalam_tahun | G2_merentas_tahun | G3_nilai_p | G3_fdr | G4_bootstrap | G5_outlier | G6 | step7 | keputusan |
|---|---|---|---|---|---|---|---|---|---|
| macd_cross&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2021=LANGKA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | DITOLAK |
| q5:julat20 | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q5:atr_pct | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q5:bb_lebar | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=SEDERHANA; 2025=TERAS) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| rsi_lintas50&q5:bb_lebar | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| rsi_lintas50&q5:julat20 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 4/5; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q5:j_ema9 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2021=UNIQUE; 2022=UNIQUE; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| rsi_lintas50&q5:atr_pct | LULUS | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=UNIQUE; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q1:cerun_ema21 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2021=-; 2022=COMMON BIASA; 2023=-; 2024=-; 2025=-) | 0.001 | LULUS | LULUS | LULUS | STATISTIK SAHAJA | LULUS | DITOLAK |
| macd_cross&q1:cerun_ma50 | GAGAL | BELUM (1/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 2/5; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=LANGKA; 2024=TIDAK BERGUNA; 2025=LANGKA) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | DITOLAK |
| ema_crossback&q5:bb_lebar | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2021=UNIQUE; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=LANGKA; 2025=TIDAK BERGUNA) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | DITOLAK |
| macd_cross&q1:sektor_1b | LULUS | TIDAK BOLEH DINILAI (kelas tahun ini TIDAK BERGUNA, bukan penemuan; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=TIDAK BERGUNA; 2024=TIDAK BERGUNA; 2025=TIDAK BERGUNA) | 0.003 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q1:cerun_ma50 | LULUS | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2021=TIDAK BERGUNA; 2022=TIDAK BERGUNA; 2023=COMMON BIASA; 2024=TIDAK BERGUNA; 2025=TERAS) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | CALON |
| q1:roc20 | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 1/5; 2021=TIDAK BERGUNA; 2022=SEDERHANA; 2023=TIDAK BERGUNA; 2024=SEDERHANA; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | GAGAL (BUNYI LATAR) | DITOLAK |
| q1:j_52w_tinggi | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 3/5; 2021=TIDAK BERGUNA; 2022=UNIQUE; 2023=UNIQUE; 2024=TIDAK BERGUNA; 2025=UNIQUE) | 0.001 | LULUS | LULUS | LULUS | LULUS | LULUS | DITOLAK |
| q5:rs_spy_3b | GAGAL | BELUM (0/5 tahun lain lulus gate keras, perlu >= 2; kelas sama 0/5; 2021=-; 2022=TIDAK BERGUNA; 2023=-; 2024=-; 2025=TIDAK BERGUNA) | 0.002 | LULUS | LULUS | LULUS | STATISTIK SAHAJA | GAGAL (BUNYI LATAR) | DITOLAK |


**DITERIMA: 0** · **CALON: 6** — `q5:julat20`, `q5:atr_pct`, `q5:bb_lebar`, `rsi_lintas50&q5:atr_pct`, `macd_cross&q1:sektor_1b`, `q1:cerun_ma50` · **DITOLAK: 10.**


Penapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam ≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada 2020.


## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)

Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. Asas signal ENTRY: **CALON selepas Step 8**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → RS 6 bulan → ticker.


| sistem | n_posisi_dibuka | n_dagangan_ditutup | n_posisi_terbuka_hujung_tahun | purata_slot_terisi | pulangan_tahun | median_bulanan | purata_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terbaik | bulan_terburuk | mdd | purata_hari_pegang | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF_pegang_252 | 16 | 8 | 8 | 7.91 | 57.4 | 3.26 | 5.19 | 33.3 | 75.0 | 32.54 | -31.61 | -54.28 | 252.0 | 1.3 | 17.24 | -33.72 |
| REF_chandelier_4atr | 44 | 36 | 8 | 7.79 | 82.15 | 2.38 | 5.95 | 25.0 | 66.7 | 44.88 | -10.89 | -29.37 | 45.7 | 3.7 | 17.24 | -33.72 |
| REF_jual_hari63 | 40 | 32 | 8 | 7.81 | 77.59 | 5.42 | 6.41 | 41.7 | 66.7 | 41.9 | -31.61 | -54.28 | 63.0 | 3.3 | 17.24 | -33.72 |
| hari_agihan|X=20%,Y=ma50 | 43 | 35 | 8 | 7.8 | 38.52 | 1.88 | 3.47 | 25.0 | 58.3 | 31.79 | -19.23 | -40.63 | 51.3 | 3.6 | 17.24 | -33.72 |
| hari_agihan|X=15%,Y=ma50 | 45 | 37 | 8 | 7.79 | 93.71 | 6.73 | 6.28 | 33.3 | 75.0 | 22.45 | -19.23 | -40.63 | 45.9 | 3.8 | 17.24 | -33.72 |
| rsi_70_60|X=20%,Y=ma50 | 27 | 19 | 8 | 7.86 | 30.77 | 2.49 | 2.6 | 25.0 | 58.3 | 15.31 | -12.8 | -33.99 | 55.2 | 2.2 | 17.24 | -33.72 |
| KAWALAN_RAWAK|pegang_252 | 15 | 7 | 8 | 7.91 | 102.84 | 7.01 | 6.42 | 41.7 | 83.3 | 15.11 | -13.89 | -28.89 | 252.0 | 1.2 | 17.24 | -33.72 |
| KAWALAN_RAWAK|chandelier | 42 | 34 | 8 | 7.8 | 42.17 | 2.67 | 3.32 | 16.7 | 75.0 | 17.67 | -16.2 | -27.59 | 45.9 | 3.5 | 17.24 | -33.72 |


### Pulangan bulanan penuh (%)

| tarikh | REF_pegang_252 | REF_chandelier_4atr | REF_jual_hari63 | hari_agihan|X=20%,Y=ma50 | hari_agihan|X=15%,Y=ma50 | rsi_70_60|X=20%,Y=ma50 | KAWALAN_RAWAK|pegang_252 | KAWALAN_RAWAK|chandelier |
|---|---|---|---|---|---|---|---|---|
| 2020-01-31 | 13.94 | 13.94 | 13.94 | 10.68 | 10.68 | 13.94 | 3.25 | 3.02 |
| 2020-02-29 | -6.13 | -0.79 | -6.13 | 3.28 | 3.28 | -4.97 | 4.47 | 0.7 |
| 2020-03-31 | -31.61 | -10.89 | -31.61 | -19.23 | -19.23 | -12.8 | -13.89 | -16.2 |
| 2020-04-30 | 29.62 | 14.83 | 4.71 | 8.44 | 8.44 | 15.31 | 12.69 | 17.67 |
| 2020-05-31 | 12.84 | -1.76 | 6.13 | -3.4 | -3.4 | -4.98 | 15.11 | 2.32 |
| 2020-06-30 | 8.72 | 0.42 | 15.51 | 5.79 | 5.79 | 1.87 | 12.78 | 8.45 |
| 2020-07-31 | 2.25 | 2.39 | 15.84 | 0.49 | 7.67 | 6.66 | 14.44 | 13.37 |
| 2020-08-31 | 4.28 | 2.37 | -1.41 | -0.2 | -3.22 | -2.1 | 5.33 | -0.4 |
| 2020-09-30 | 1.55 | 5.98 | 4.64 | -1.69 | 3.68 | 3.1 | 3.1 | 0.41 |
| 2020-10-31 | -6.16 | -9.29 | -8.45 | -9.63 | 19.27 | -3.68 | -3.89 | -2.48 |
| 2020-11-30 | 32.54 | 44.88 | 41.9 | 31.79 | 22.45 | 11.37 | 15.01 | 3.59 |
| 2020-12-31 | 0.47 | 9.35 | 21.84 | 15.29 | 19.98 | 7.43 | 8.68 | 9.34 |


### Jawapan terus kepada sasaran +10% sebulan

**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:


- `REF_pegang_252`: median bulanan **3.26%**, 33.3% bulan ≥ +10%, bulan terburuk -31.61%, MDD -54.28%, pulangan tahun 57.40% (SPY 17.24%, MDD SPY -33.72%)

- `REF_chandelier_4atr`: median bulanan **2.38%**, 25.0% bulan ≥ +10%, bulan terburuk -10.89%, MDD -29.37%, pulangan tahun 82.15% (SPY 17.24%, MDD SPY -33.72%)

- `REF_jual_hari63`: median bulanan **5.42%**, 41.7% bulan ≥ +10%, bulan terburuk -31.61%, MDD -54.28%, pulangan tahun 77.59% (SPY 17.24%, MDD SPY -33.72%)

- `hari_agihan|X=20%,Y=ma50`: median bulanan **1.88%**, 25.0% bulan ≥ +10%, bulan terburuk -19.23%, MDD -40.63%, pulangan tahun 38.52% (SPY 17.24%, MDD SPY -33.72%)

- `hari_agihan|X=15%,Y=ma50`: median bulanan **6.73%**, 33.3% bulan ≥ +10%, bulan terburuk -19.23%, MDD -40.63%, pulangan tahun 93.71% (SPY 17.24%, MDD SPY -33.72%)

- `rsi_70_60|X=20%,Y=ma50`: median bulanan **2.49%**, 25.0% bulan ≥ +10%, bulan terburuk -12.80%, MDD -33.99%, pulangan tahun 30.77% (SPY 17.24%, MDD SPY -33.72%)

- `KAWALAN_RAWAK|pegang_252`: median bulanan **7.01%**, 41.7% bulan ≥ +10%, bulan terburuk -13.89%, MDD -28.89%, pulangan tahun 102.84% (SPY 17.24%, MDD SPY -33.72%)

- `KAWALAN_RAWAK|chandelier`: median bulanan **2.67%**, 16.7% bulan ≥ +10%, bulan terburuk -16.20%, MDD -27.59%, pulangan tahun 42.17% (SPY 17.24%, MDD SPY -33.72%)


**Apa yang menghalang — kapasiti, bukan kadar menang.**

- Sistem terbaik (`REF_pegang_252`) hanya membuka **16 posisi sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh dijadikan asas keputusan.

- Sistem yang pusing ganti mencukupi (Chandelier: 44 posisi, 3.7/bulan) memberi median bulanan hanya 2.38% dengan MDD -29.37% — lebih buruk daripada MDD SPY.

- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.

- KAWALAN RAWAK pegang-252 memberi 102.84% dan Chandelier rawak 42.17% — dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.


### Banding wajib: SPY dan KAWALAN RAWAK

- SPY tempoh sama: **17.24%** (MDD -33.72%). **0/6** sistem kalah kepada SPY.

- KAWALAN RAWAK terbaik: **102.84%** (`KAWALAN_RAWAK|pegang_252`). **6/6** sistem kalah kepada entri rawak.

- **Setiap sistem berasaskan signal kalah kepada entri rawak tahun ini.** Itu bukan bukti signal yang lemah sahaja; ia bukti bahawa pemilihan signal tahun ini memudaratkan portfolio berbanding memilih secara rawak daripada universe yang sama.


> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.


## 12. Keputusan akhir (had fasa: CALON)

1. **ENTRY** — 6 signal CALON: `q5:julat20`, `q5:atr_pct`, `q5:bb_lebar`, `rsi_lintas50&q5:atr_pct`, `macd_cross&q1:sektor_1b`, `q1:cerun_ma50`. Tiada pemicu klasik tunggal lulus. Hipotesis "magnitud ada pada konteks, bukan pemicu" disokong oleh data 2020.

2. **HOLD** — 9/18 signal lulus FDR; kelas pullback ialah hasil paling kukuh (SIHAT 89.1% / PASARAN 87.9% menyambung ke puncak baru lawan AMARAN 70.5%).

3. **EXIT** — 0/68 signal lulus FDR; 0/234 sistem mengalahkan ketiga-tiga rujukan dan 0/234 lulus FDR keluarga SISTEM. **Jawapan kajian tahun ini: jangan jual.**

4. **PORTFOLIO** — sasaran +10% sebulan tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila pegangan panjang, bukan kadar menang.

5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam ≥ 2 tahun LAIN; tahun lain yang siap: [2021, 2022, 2023, 2024, 2025]. Lihat `BANDING_TAHUN.md` untuk status merentas tahun.


## 13. Fail output

| Fail | Isi |
|---|---|
| `runs_2020.csv` | 4593 run, 34 lajur |
| `monthly_summary_2020.csv` | ringkasan 12 bulan |
| `skipped_2020.csv` | 7785 calon ditolak + sebab |
| `kohort_masih_naik_2020.csv` | 515 run masih_naik dijejak 252 hari |
| `common_unique_2020.csv` | 3504 baris (213 signal × subset × populasi × kumpulan × keluarga) |
| `taburan_indikator_2020.csv` | median + p25/p75 setiap indikator setiap hasil |
| `hold_exit_2020.csv` | 369 baris CALON HOLD/EXIT |
| `false_signal_2020.csv` | 144 baris (signal + penapis) |
| `hadapan_hold_exit_2020.csv` | 237 sistem (234 + 3 rujukan) |
| `kawalan_rawak_bootstrap_2020.csv` | nilai-p label rawak + had bawah bootstrap |
| `jangkaan_kemunculan_2020.csv` | jangkaan + ujian outlier |
| `keputusan_2020.csv` | keputusan gate demi gate |
| `portfolio_2020.csv`, `portfolio_bulanan_2020.csv` | Step 9 |
| `log_ujian.csv` | setiap signal/kombinasi yang diuji |
| `PANDANG_HADAPAN_2020.md` | imbasan pandang ke hadapan |
| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |
