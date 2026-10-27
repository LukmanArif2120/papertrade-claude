# BANDING MERENTAS TAHUN — REVERSE (2021, 2022, 2023, 2024, 2025)

Dijana `REVERSE/banding_tahun.py`. Kod dan parameter **sama tanpa ubah** bagi setiap tahun; universe ikut bulan tahun berkenaan. Spec: `REVERSE/SPEC.md`.

> **KAVEAT.** Tiada saham delist (survivorship) dalam mana-mana tahun. Gate 8.1 memerlukan kelas yang sama dalam **≥ 2 tahun LAIN**; dengan 5 tahun siap, setiap tahun mempunyai 4 tahun lain, jadi naik taraf ke DITERIMA **mungkin** pada fasa ini. Jumlah signal DITERIMA setakat ini: **3**.

## 1. Run dan peristiwa

| tahun | n_run | n_super | n_padu | n_biasa | pct_bertangga | pct_lonjakan | pct_stabil | pct_entry_sah | pct_graf_menaik | n_masih_naik | median_naik | n_peristiwa_sah | n_padu_s2_keputusan | had_bersyarat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | 4413 | 44 | 1598 | 2771 | 5.1 | 50.1 | 44.9 | 75.0 | 57.7 | 399 | 23.5 | 15259 | 128 | AKTIF |
| 2022 | 5541 | 52 | 2363 | 3126 | 5.4 | 53.4 | 41.2 | 65.9 | 22.1 | 481 | 27.0 | 15440 | 171 | AKTIF |
| 2023 | 4048 | 49 | 1986 | 2013 | 7.0 | 39.6 | 53.5 | 76.4 | 45.2 | 577 | 30.1 | 13642 | 200 | AKTIF |
| 2024 | 3744 | 58 | 1537 | 2149 | 5.5 | 52.8 | 41.7 | 80.4 | 55.6 | 457 | 25.3 | 14151 | 116 | AKTIF |
| 2025 | 4507 | 98 | 2326 | 2083 | 8.9 | 50.7 | 40.4 | 68.6 | 45.5 | 853 | 31.2 | 13998 | 189 | AKTIF |


## 2. Kohort "naik dan naik" (Step 2b)

| tahun | n_kohort | pct_melebihi_100 | median_naik_penuh | median_naik_hari63 | median_hari_chandelier | median_pul_chandelier | pct_terpotong |
|---|---|---|---|---|---|---|---|
| 2021.0 | 315.0 | 15.6 | 59.9 | 37.6 | 85.0 | 18.3 | 0.0 |
| 2022.0 | 297.0 | 18.2 | 62.7 | 40.0 | 81.0 | 11.0 | 0.0 |
| 2023.0 | 420.0 | 31.4 | 77.7 | 39.9 | 92.0 | 20.0 | 0.0 |
| 2024.0 | 374.0 | 22.7 | 65.3 | 37.3 | 73.0 | 14.1 | 0.0 |
| 2025.0 | 470.0 | 39.8 | 87.0 | 39.8 | 82.0 | 18.6 | 32.6 |


Kohort ini lebih kuat pada 2025 daripada 2024, tetapi arahnya sama pada kedua-dua tahun: run yang masih naik pada hari ke-63 pergi jauh lebih tinggi daripada yang reda.


## 3. Signal ENTRY — kekal konsisten lawan tahun tertentu


### KEKAL — kelas TERAS/UNIQUE/LANGKA dalam **semua** 5 tahun (0 signal)

_(tiada baris)_


### TAHUN TERTENTU — kelas baik dalam sebahagian tahun sahaja (32 signal)

| signal | kelas_2021 | lift_2021 | keputusan_2021 | kelas_2022 | lift_2022 | keputusan_2022 | kelas_2023 | lift_2023 | keputusan_2023 | kelas_2024 | lift_2024 | keputusan_2024 | kelas_2025 | lift_2025 | keputusan_2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pocket_pivot&q1:j_52w_tinggi | UNIQUE | 9.707 | DITOLAK | LANGKA | 9.984 | DITOLAK | LANGKA | 6.692 | DITOLAK | TIDAK BERGUNA | 0.238 | - | LANGKA | 5.765 | DITOLAK |
| rsi_lintas50&q5:atr_pct | TIDAK BERGUNA | 0.789 | DITOLAK | UNIQUE | 17.427 | DITOLAK | UNIQUE | 13.024 | DITOLAK | UNIQUE | 15.148 | DITOLAK | UNIQUE | 19.602 | DITERIMA |
| q5:julat20 | UNIQUE | 9.484 | DITOLAK | UNIQUE | 4.578 | DITOLAK | TIDAK BERGUNA | 1.194 | DITOLAK | UNIQUE | 9.778 | DITOLAK | UNIQUE | 11.88 | DITERIMA |
| rsi_lintas50&q5:julat20 | UNIQUE | 11.582 | DITOLAK | UNIQUE | 10.286 | DITOLAK | TIDAK BERGUNA | 0.694 | DITOLAK | UNIQUE | 9.615 | DITOLAK | UNIQUE | 23.76 | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 3.422 | DITOLAK | UNIQUE | 10.619 | DITOLAK | UNIQUE | 5.453 | DITOLAK | TIDAK BERGUNA | 0.265 | DITOLAK | UNIQUE | 6.237 | DITOLAK |
| q5:atr_pct | TIDAK BERGUNA | 1.465 | DITOLAK | UNIQUE | 12.986 | DITOLAK | UNIQUE | 10.306 | DITOLAK | UNIQUE | 11.67 | DITOLAK | UNIQUE | 14.334 | DITERIMA |
| rsi_lintas50&q5:bb_lebar | UNIQUE | 10.327 | DITOLAK | UNIQUE | 8.432 | DITOLAK | TIDAK BERGUNA | 0.778 | DITOLAK | TIDAK BERGUNA | 1.19 | DITOLAK | UNIQUE | 21.06 | DITOLAK |
| q1:j_52w_tinggi | TIDAK BERGUNA | 1.352 | DITOLAK | UNIQUE | 3.133 | DITOLAK | UNIQUE | 5.365 | DITOLAK | TIDAK BERGUNA | 0.556 | DITOLAK | UNIQUE | 4.044 | DITOLAK |
| q5:bb_lebar | UNIQUE | 7.523 | DITOLAK | UNIQUE | 4.337 | DITOLAK | TIDAK BERGUNA | 1.306 | DITOLAK | SEDERHANA | 2.063 | DITOLAK | TERAS | 9.876 | CALON |
| q5:j_ema9 | UNIQUE | 7.64 | DITOLAK | UNIQUE | 5.755 | DITOLAK | TIDAK BERGUNA | 0.472 | DITOLAK | TIDAK BERGUNA | 1.984 | DITOLAK | UNIQUE | 6.93 | DITOLAK |
| ema_crossback&q5:bb_lebar | UNIQUE | 9.279 | DITOLAK | TIDAK BERGUNA | 10.396 | - | TIDAK BERGUNA | 3.874 | - | LANGKA | 7.383 | DITOLAK | TIDAK BERGUNA | 7.92 | - |
| macd_cross&q1:j_52w_tinggi | TIDAK BERGUNA | 3.677 | DITOLAK | TIDAK BERGUNA | 1.084 | - | LANGKA | 5.608 | DITOLAK | TIDAK BERGUNA | 0.587 | - | LANGKA | 8.1 | DITOLAK |
| macd_cross&q1:cerun_ma50 | TIDAK BERGUNA | 3.033 | DITOLAK | TIDAK BERGUNA | 0.361 | - | LANGKA | 5.285 | CALON | TIDAK BERGUNA | 0.079 | - | LANGKA | 5.445 | DITOLAK |
| rsi_lintas50&q5:rs_spy_6b | UNIQUE | 4.283 | DITOLAK | TIDAK BERGUNA | 1.807 | - | TIDAK BERGUNA | 2.3 | - | UNIQUE | 3.299 | DITOLAK | TIDAK BERGUNA | 3.267 | - |
| ema_crossback&q5:j_ma200 | UNIQUE | 5.021 | DITOLAK | TIDAK BERGUNA | 1.762 | - | TIDAK BERGUNA | 2.366 | - | TIDAK BERGUNA | 2.385 | - | TIDAK BERGUNA | 0.056 | - |
| ema_crossback&q5:cerun_ma50 | LANGKA | 5.778 | DITOLAK | TIDAK BERGUNA | 1.8 | - | TIDAK BERGUNA | 2.342 | - | TIDAK BERGUNA | 0.0 | - | TIDAK BERGUNA | 0.045 | - |
| q1:j_ma200 | TIDAK BERGUNA | 0.958 | - | UNIQUE | 4.096 | DITOLAK | TIDAK BERGUNA | 0.639 | - | TIDAK BERGUNA | 0.529 | - | SEDERHANA | 2.236 | - |
| q1:cerun_ma50 | TIDAK BERGUNA | 1.867 | - | TIDAK BERGUNA | 1.124 | - | COMMON BIASA | 0.792 | DITOLAK | TIDAK BERGUNA | 0.476 | - | TERAS | 3.24 | DITOLAK |
| pocket_pivot&q5:bb_lebar | TIDAK BERGUNA | 16.801 | - | LANGKA | 5.198 | DITOLAK | TIDAK BERGUNA | 0.444 | DITOLAK | TIDAK BERGUNA | 9.12 | - | TIDAK BERGUNA | 7.92 | - |
| pocket_pivot&q5:atr_pct | TIDAK BERGUNA | 15.443 | - | TIDAK BERGUNA | 12.707 | - | TIDAK BERGUNA | 9.369 | - | LANGKA | 8.614 | DITOLAK | TIDAK BERGUNA | 20.048 | - |
| macd_cross&q5:bb_lebar | LANGKA | 7.722 | DITOLAK | TIDAK BERGUNA | 1.205 | DITOLAK | TIDAK BERGUNA | 0.306 | - | TIDAK BERGUNA | 0.397 | - | TIDAK BERGUNA | 10.024 | - |
| pocket_pivot&q1:j_ma200 | TIDAK BERGUNA | 2.734 | - | LANGKA | 6.197 | DITOLAK | TIDAK BERGUNA | 0.361 | DITOLAK | TIDAK BERGUNA | 1.723 | - | TIDAK BERGUNA | 3.439 | - |
| ema_crossback&q5:rs_spy_6b | UNIQUE | 3.993 | DITOLAK | TIDAK BERGUNA | 2.178 | - | TIDAK BERGUNA | 2.375 | - | TIDAK BERGUNA | 2.802 | - | TIDAK BERGUNA | 1.747 | - |
| ema_crossback&q5:julat20 | UNIQUE | 9.279 | DITOLAK | TIDAK BERGUNA | 18.38 | - | TIDAK BERGUNA | 3.272 | - | TIDAK BERGUNA | 8.16 | - | TIDAK BERGUNA | 7.128 | - |
| ema_crossback&q5:atr_pct | LANGKA | 6.24 | DITOLAK | TIDAK BERGUNA | 21.783 | - | TIDAK BERGUNA | 6.692 | - | TIDAK BERGUNA | 19.381 | - | TIDAK BERGUNA | 8.91 | - |


### Signal berstatus CALON dalam SEMUA tahun (0)

_(tiada baris)_


Inilah satu-satunya senarai yang layak diteruskan ke tahun berikutnya. Gate 8.1 memerlukan ≥ 2 tahun LAIN; selepas satu tahun lagi (2023) senarai ini boleh dinaik taraf ke DITERIMA jika kelasnya kekal.


## 4. HOLD, EXIT dan SISTEM merentas tahun

| tahun | entry_padu | entry_super | hold | exit | sistem |
|---|---|---|---|---|---|
| 2021 | 22/27 | 10/27 | 10/18 | 0/62 | 173/234 |
| 2022 | 15/21 | 7/21 | 13/18 | 0/66 | 0/234 |
| 2023 | 7/20 | 5/20 | 0/18 | 0/64 | 0/234 |
| 2024 | 12/18 | 6/18 | 0/18 | 0/62 | 0/234 |
| 2025 | 18/19 | 11/19 | 11/18 | 0/62 | 0/234 |


Lulus BH-FDR q ≤ 0.01. **Keluarga EXIT dan SISTEM kosong pada setiap tahun.**


### Kelas pullback (Step 5) — stabil merentas tahun

| tahun | PULLBACK SIHAT | n_PULLBACK SIHAT | PULLBACK PASARAN | n_PULLBACK PASARAN | AMARAN | n_AMARAN |
|---|---|---|---|---|---|---|
| 2021.0 | 89.0 | 798.0 | 85.3 | 394.0 | 43.9 | 4778.0 |
| 2022.0 | 65.0 | 223.0 | 88.7 | 417.0 | 54.0 | 6502.0 |
| 2023.0 | 91.5 | 1322.0 | 80.0 | 115.0 | 46.2 | 4568.0 |
| 2024.0 | 88.4 | 1034.0 | 82.6 | 408.0 | 47.2 | 4489.0 |
| 2025.0 | 88.9 | 1394.0 | 92.0 | 311.0 | 50.8 | 4790.0 |


Perbezaan SIHAT/PASARAN lawan AMARAN kekal besar pada kedua-dua tahun. Ini hasil HOLD yang paling boleh dipercayai dalam kajian ini.


### HOLD yang lulus FDR dalam semua tahun

0 signal: tiada


## 5. Step 7b — tiga rujukan wajib merentas tahun

| tahun | REF_pegang_252_jangkaan | REF_pegang_252_median | REF_chandelier_4atr_jangkaan | REF_chandelier_4atr_median | REF_jual_hari63_jangkaan | REF_jual_hari63_median | rujukan_menang | n_sistem_mengalahkan_semua |
|---|---|---|---|---|---|---|---|---|
| 2021 | -19.134 | -22.41 | -3.418 | -6.92 | -2.809 | -3.11 | REF_jual_hari63 | 196 |
| 2022 | 0.547 | -3.64 | -4.771 | -8.27 | -3.171 | -3.81 | REF_pegang_252 | 14 |
| 2023 | 16.246 | 9.85 | 1.507 | -4.61 | 2.861 | 1.65 | REF_pegang_252 | 0 |
| 2024 | 8.677 | -2.01 | -0.022 | -5.44 | 1.34 | -0.54 | REF_pegang_252 | 0 |
| 2025 | 27.571 | 10.14 | 6.069 | -5.0 | 4.846 | 1.63 | REF_pegang_252 | 0 |


**Rujukan (c) "pegang tanpa jual" menang pada kedua-dua tahun, dan 0/234 sistem mengalahkan ketiga-tiga rujukan pada kedua-dua tahun.** Tetapi perhatikan medianya: positif pada 2025, negatif pada 2024 — jangkaan positif itu dipacu hujung kanan taburan, bukan dagangan biasa.


## 6. Step 9 — prestasi portfolio merentas tahun

| tahun | sistem | n_posisi_dibuka | n_dagangan_ditutup | purata_slot_terisi | pulangan_tahun | median_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terburuk | mdd | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | REF_pegang_252 | 8 | 0 | 7.94 | 12.28 | 1.02 | 8.3 | 58.3 | -5.16 | -22.16 | 0.7 | 30.51 | -5.11 |
| 2021 | REF_chandelier_4atr | 46 | 38 | 7.79 | -2.15 | -0.25 | 25.0 | 50.0 | -13.16 | -33.56 | 3.8 | 30.51 | -5.11 |
| 2021 | REF_jual_hari63 | 40 | 32 | 7.81 | 5.24 | 1.71 | 16.7 | 66.7 | -17.18 | -39.51 | 3.3 | 30.51 | -5.11 |
| 2021 | bawah_ema9|X=5%,Y=ema9 | 415 | 407 | 6.32 | -34.84 | -4.39 | 8.3 | 25.0 | -17.46 | -52.58 | 34.6 | 30.51 | -5.11 |
| 2021 | bawah_ema9|X=7%,Y=ema9 | 415 | 407 | 6.32 | -34.84 | -4.39 | 8.3 | 25.0 | -17.46 | -52.58 | 34.6 | 30.51 | -5.11 |
| 2021 | bawah_ema9|X=15%,Y=ema9 | 415 | 407 | 6.32 | -34.84 | -4.39 | 8.3 | 25.0 | -17.46 | -52.58 | 34.6 | 30.51 | -5.11 |
| 2021 | KAWALAN_RAWAK|pegang_252 | 8 | 0 | 7.94 | 2.39 | 0.14 | 0.0 | 50.0 | -4.41 | -13.33 | 0.7 | 30.51 | -5.11 |
| 2021 | KAWALAN_RAWAK|chandelier | 44 | 36 | 7.79 | -0.3 | 0.28 | 0.0 | 58.3 | -6.99 | -19.0 | 3.7 | 30.51 | -5.11 |
| 2022 | REF_pegang_252 | 8 | 0 | 7.94 | -16.0 | 2.38 | 16.7 | 58.3 | -20.97 | -24.96 | 0.7 | -18.65 | -24.5 |
| 2022 | REF_chandelier_4atr | 38 | 30 | 7.82 | -5.26 | 1.93 | 8.3 | 50.0 | -18.0 | -37.88 | 3.2 | -18.65 | -24.5 |
| 2022 | REF_jual_hari63 | 40 | 32 | 7.81 | -20.03 | 1.46 | 16.7 | 50.0 | -20.97 | -34.08 | 3.3 | -18.65 | -24.5 |
| 2022 | rsi_70_60|X=7%,Y=ema9 | 25 | 17 | 7.87 | -5.65 | 2.66 | 16.7 | 50.0 | -17.12 | -34.22 | 2.1 | -18.65 | -24.5 |
| 2022 | rsi_70_60|X=5%,Y=ema9 | 25 | 17 | 7.87 | -5.65 | 2.66 | 16.7 | 50.0 | -17.12 | -34.22 | 2.1 | -18.65 | -24.5 |
| 2022 | rsi_70_60|X=15%,Y=ema9 | 25 | 17 | 7.87 | -5.65 | 2.66 | 16.7 | 50.0 | -17.12 | -34.22 | 2.1 | -18.65 | -24.5 |
| 2022 | KAWALAN_RAWAK|pegang_252 | 8 | 0 | 7.94 | -36.92 | -0.88 | 0.0 | 50.0 | -15.75 | -38.78 | 0.7 | -18.65 | -24.5 |
| 2022 | KAWALAN_RAWAK|chandelier | 56 | 48 | 7.75 | -36.9 | -3.8 | 0.0 | 33.3 | -14.63 | -39.48 | 4.7 | -18.65 | -24.5 |
| 2023 | REF_pegang_252 | 8 | 0 | 7.94 | 24.72 | 3.44 | 25.0 | 58.3 | -8.39 | -21.11 | 0.7 | 26.71 | -9.97 |
| 2023 | REF_chandelier_4atr | 42 | 34 | 7.8 | 56.37 | 2.58 | 25.0 | 66.7 | -9.81 | -21.52 | 3.5 | 26.71 | -9.97 |
| 2023 | REF_jual_hari63 | 35 | 32 | 7.81 | 21.14 | 1.78 | 25.0 | 58.3 | -10.08 | -21.76 | 2.9 | 26.71 | -9.97 |
| 2023 | rsi_70_60|X=12%,Y=ma50 | 19 | 11 | 7.89 | 35.22 | 0.88 | 25.0 | 50.0 | -6.2 | -17.24 | 1.6 | 26.71 | -9.97 |
| 2023 | rsi_70_60|X=20%,Y=ma50 | 21 | 13 | 7.88 | 31.84 | 2.22 | 25.0 | 50.0 | -7.51 | -18.1 | 1.8 | 26.71 | -9.97 |
| 2023 | rsi_70_60|X=10%,Y=ma50 | 19 | 11 | 7.89 | 35.22 | 0.88 | 25.0 | 50.0 | -6.2 | -17.24 | 1.6 | 26.71 | -9.97 |
| 2023 | KAWALAN_RAWAK|pegang_252 | 8 | 0 | 7.94 | 9.22 | -1.06 | 16.7 | 50.0 | -8.99 | -26.75 | 0.7 | 26.71 | -9.97 |
| 2023 | KAWALAN_RAWAK|chandelier | 42 | 34 | 7.8 | 10.72 | -0.59 | 16.7 | 50.0 | -11.18 | -23.6 | 3.5 | 26.71 | -9.97 |
| 2024 | REF_pegang_252 | 8 | 0 | 7.94 | -0.43 | -2.02 | 25.0 | 41.7 | -24.73 | -25.26 | 0.7 | 25.59 | -8.41 |
| 2024 | REF_chandelier_4atr | 41 | 33 | 7.81 | -46.69 | -5.98 | 0.0 | 25.0 | -14.33 | -50.33 | 3.4 | 25.59 | -8.41 |
| 2024 | REF_jual_hari63 | 40 | 32 | 7.81 | -30.42 | -3.11 | 16.7 | 33.3 | -15.94 | -41.61 | 3.3 | 25.59 | -8.41 |
| 2024 | hari_agihan|X=5%,Y=ema9 | 46 | 38 | 7.79 | 10.98 | 2.34 | 16.7 | 66.7 | -11.68 | -29.4 | 3.8 | 25.59 | -8.41 |
| 2024 | hari_agihan|X=5%,Y=ma50 | 48 | 40 | 7.78 | 0.29 | 1.69 | 16.7 | 58.3 | -14.12 | -31.55 | 4.0 | 25.59 | -8.41 |
| 2024 | hari_agihan|X=5%,Y=ema21 | 46 | 38 | 7.79 | 9.29 | 2.01 | 25.0 | 66.7 | -11.46 | -28.32 | 3.8 | 25.59 | -8.41 |
| 2024 | KAWALAN_RAWAK|pegang_252 | 8 | 0 | 7.94 | 20.48 | 1.85 | 8.3 | 83.3 | -10.34 | -10.36 | 0.7 | 25.59 | -8.41 |
| 2024 | KAWALAN_RAWAK|chandelier | 44 | 36 | 7.79 | 14.65 | 1.2 | 8.3 | 50.0 | -8.17 | -13.84 | 3.7 | 25.59 | -8.41 |
| 2025 | REF_pegang_252 | 8 | 0 | 7.94 | 128.93 | 5.65 | 41.7 | 66.7 | -16.56 | -38.71 | 0.7 | 18.01 | -18.76 |
| 2025 | REF_chandelier_4atr | 42 | 34 | 7.8 | 14.93 | 0.93 | 16.7 | 58.3 | -20.31 | -43.39 | 3.5 | 18.01 | -18.76 |
| 2025 | REF_jual_hari63 | 40 | 32 | 7.81 | -24.5 | -2.27 | 8.3 | 33.3 | -16.76 | -47.62 | 3.3 | 18.01 | -18.76 |
| 2025 | rsi_70_60|X=20%,Y=ma50 | 30 | 22 | 7.85 | -14.19 | -2.36 | 0.0 | 41.7 | -10.85 | -26.98 | 2.5 | 18.01 | -18.76 |
| 2025 | rsi_70_60|X=15%,Y=ma50 | 37 | 29 | 7.82 | 5.54 | 1.31 | 8.3 | 50.0 | -14.19 | -30.59 | 3.1 | 18.01 | -18.76 |
| 2025 | hari_agihan|X=20%,Y=ma50 | 44 | 36 | 7.79 | -31.79 | -2.52 | 25.0 | 33.3 | -23.49 | -47.73 | 3.7 | 18.01 | -18.76 |
| 2025 | KAWALAN_RAWAK|pegang_252 | 8 | 0 | 7.94 | 9.51 | 2.39 | 0.0 | 58.3 | -6.73 | -27.62 | 0.7 | 18.01 | -18.76 |
| 2025 | KAWALAN_RAWAK|chandelier | 40 | 32 | 7.81 | 29.47 | 1.62 | 8.3 | 75.0 | -9.29 | -28.45 | 3.3 | 18.01 | -18.76 |


### Sasaran +10% sebulan (median) merentas tahun

**0 daripada 40 kombinasi (sistem × tahun) mencapai median +10% sebulan.**

- 2021: terbaik `REF_jual_hari63` median bulanan **1.71%**, MDD -39.51%, 40 posisi dibuka (SPY 30.51%)

- 2022: terbaik `rsi_70_60|X=7%,Y=ema9` median bulanan **2.66%**, MDD -34.22%, 25 posisi dibuka (SPY -18.65%)

- 2023: terbaik `REF_pegang_252` median bulanan **3.44%**, MDD -21.11%, 8 posisi dibuka (SPY 26.71%)

- 2024: terbaik `hari_agihan|X=5%,Y=ema9` median bulanan **2.34%**, MDD -29.40%, 46 posisi dibuka (SPY 25.59%)

- 2025: terbaik `REF_pegang_252` median bulanan **5.65%**, MDD -38.71%, 8 posisi dibuka (SPY 18.01%)


## 7. Kesimpulan merentas tahun

1. **Tiada signal konsisten merentas 5 tahun — malah kelasnya pun tidak.** **0** signal mengekalkan kelas TERAS/UNIQUE/LANGKA pada semua 5 tahun; yang terbaik hanya 4/5 tahun (6 signal: `pocket_pivot&q1:j_52w_tinggi`, `q5:atr_pct`, `q5:julat20`, `rsi_lintas50&q1:j_52w_tinggi`, `rsi_lintas50&q5:atr_pct`, `rsi_lintas50&q5:julat20`). **0 berstatus CALON atau DITERIMA pada lebih daripada satu tahun.**

   Ini perubahan penting berbanding empat tahun. Dengan 2022-2025 sahaja, `q5:atr_pct` dan `rsi_lintas50&q5:atr_pct` kekal UNIQUE keempat-empat tahun dan kelihatan seperti keluarga signal yang stabil. Menambah 2021 mematahkannya: kedua-duanya **TIDAK BERGUNA** pada 2021. Apa yang kelihatan konsisten merentas empat tahun sebenarnya konsisten merentas satu rejim sahaja.

2. **Konsisten:** pemicu klasik tunggal mencapai kelas TERAS/UNIQUE/LANGKA dalam 0 daripada 30 kombinasi (pemicu × tahun). Hipotesis "magnitud ada pada konteks, bukan pemicu" disokong pada setiap 5 tahun.

3. **Keluarga EXIT kosong pada FDR setiap tahun; keluarga SISTEM TIDAK kosong setiap tahun.**

   - 2021: rujukan menang `REF_jual_hari63` (ambang -2.81%); 196/234 sistem mengalahkan ketiga-tiga rujukan, 173/234 lulus FDR, **0/234 berjangkaan POSITIF**.

   - 2022: rujukan menang `REF_pegang_252` (ambang +0.55%); 14/234 sistem mengalahkan ketiga-tiga rujukan, 0/234 lulus FDR, **18/234 berjangkaan POSITIF**.

   - 2023: rujukan menang `REF_pegang_252` (ambang +16.25%); 0/234 sistem mengalahkan ketiga-tiga rujukan, 0/234 lulus FDR, **190/234 berjangkaan POSITIF**.

   - 2024: rujukan menang `REF_pegang_252` (ambang +8.68%); 0/234 sistem mengalahkan ketiga-tiga rujukan, 0/234 lulus FDR, **99/234 berjangkaan POSITIF**.

   - 2025: rujukan menang `REF_pegang_252` (ambang +27.57%); 0/234 sistem mengalahkan ketiga-tiga rujukan, 0/234 lulus FDR, **228/234 berjangkaan POSITIF**.

   Lajur terakhir itu yang penting. Pada tahun yang rujukannya sendiri merugikan, ramai sistem "mengalahkan rujukan" dan lulus FDR sambil masih kehilangan wang: pada 2021, 196/234 mengalahkan rujukan dan 173 lulus FDR, tetapi **0/234 berjangkaan positif**. Kedudukan berbanding rujukan bukan ukuran keuntungan.

4. **Konsisten:** kelas pullback membezakan sambungan ke puncak baru setiap tahun — 2021: SIHAT 89.0% / PASARAN 85.3% lawan AMARAN 43.9%; 2022: SIHAT 65.0% / PASARAN 88.7% lawan AMARAN 54.0%; 2023: SIHAT 91.5% / PASARAN 80.0% lawan AMARAN 46.2%; 2024: SIHAT 88.4% / PASARAN 82.6% lawan AMARAN 47.2%; 2025: SIHAT 88.9% / PASARAN 92.0% lawan AMARAN 50.8%.

5. **Tidak konsisten:** magnitud mutlak. Median pulangan rujukan pegang-252 -22.4% (2021), -3.6% (2022), +9.8% (2023), -2.0% (2024), +10.1% (2025); kohort masih_naik yang melebihi +100%: 15.6% (2021), 18.2% (2022), 31.4% (2023), 22.7% (2024), 39.8% (2025). Tahun berbeza = rejim berbeza; angka tahun terbaik bukan jangkaan.

6. **Paling penting untuk keputusan dagangan: arah bertukar dari tahun ke tahun.** Portfolio berasaskan signal kalah kepada entri rawak pada 3 daripada 5 tahun.

   - 2021: SPY +30.51%, rawak terbaik +2.39%; **6/6** sistem kalah kepada SPY dan **4/6** kalah kepada entri rawak. Terbaik yang mengalahkan rawak: `REF_pegang_252` (+12.28%) dengan 8 posisi dibuka.

   - 2022: SPY -18.65%, rawak terbaik -36.90%; **1/6** sistem kalah kepada SPY dan **0/6** kalah kepada entri rawak. Terbaik yang mengalahkan rawak: `REF_chandelier_4atr` (-5.26%) dengan 38 posisi dibuka.

   - 2023: SPY +26.71%, rawak terbaik +10.72%; **2/6** sistem kalah kepada SPY dan **0/6** kalah kepada entri rawak. Terbaik yang mengalahkan rawak: `REF_chandelier_4atr` (+56.37%) dengan 42 posisi dibuka.

   - 2024: SPY +25.59%, rawak terbaik +20.48%; **6/6** sistem kalah kepada SPY dan **6/6** kalah kepada entri rawak.

   - 2025: SPY +18.01%, rawak terbaik +29.47%; **5/6** sistem kalah kepada SPY dan **5/6** kalah kepada entri rawak. Terbaik yang mengalahkan rawak: `REF_pegang_252` (+128.93%) dengan 8 posisi dibuka.

   Tiga tahun, tiga keputusan berbeza: 2023 signal mengalahkan rawak, 2024 kalah sepenuhnya, 2025 kalah kecuali satu kes 8 posisi. **Itu taburan, bukan kelebihan.** Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil (lihat `n_posisi_dibuka`).

   Sasaran +10% sebulan (median): **0 daripada 40** kombinasi (sistem × tahun) mencapainya.

7. **3 signal DITERIMA** (gate 8.1 dipenuhi) — tetapi lihat amaran percanggahan di bawah.

   - 2025: `rsi_lintas50&q5:atr_pct` DITERIMA, tetapi DITOLAK pada 2021, 2022, 2023, 2024 (gagal G4 bootstrap / G5 outlier di sana).

   - 2025: `q5:atr_pct` DITERIMA, tetapi DITOLAK pada 2021, 2022, 2023, 2024 (gagal G4 bootstrap / G5 outlier di sana).

   - 2025: `q5:julat20` DITERIMA, tetapi DITOLAK pada 2021, 2022, 2023, 2024 (gagal G4 bootstrap / G5 outlier di sana).


> **AMARAN.** Gate 8.1 hanya memerlukan **kelas yang sama** dalam ≥ 2 tahun lain, bukan keputusan yang sama. Signal di atas lulus kerana kelas Step 4-nya konsisten, sedangkan tahun yang mengesahkannya menolaknya pada gate keras. Spec tidak diubah selepas melihat hasil; mengetatkan gate 8.1 (memerlukan CALON, bukan sekadar kelas sama) ialah keputusan pengguna.
