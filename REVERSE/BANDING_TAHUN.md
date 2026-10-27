# BANDING MERENTAS TAHUN — REVERSE (2023, 2024, 2025)

Dijana `REVERSE/banding_tahun.py`. Kod dan parameter **sama tanpa ubah** bagi setiap tahun; universe ikut bulan tahun berkenaan. Spec: `REVERSE/SPEC.md`.

> **KAVEAT.** Tiada saham delist (survivorship) dalam mana-mana tahun. Gate 8.1 memerlukan kelas yang sama dalam **≥ 2 tahun LAIN**; dengan 3 tahun siap, setiap tahun mempunyai 2 tahun lain, jadi naik taraf ke DITERIMA **mungkin** pada fasa ini. Jumlah signal DITERIMA setakat ini: **2**.

## 1. Run dan peristiwa

| tahun | n_run | n_super | n_padu | n_biasa | pct_bertangga | pct_lonjakan | pct_stabil | pct_entry_sah | pct_graf_menaik | n_masih_naik | median_naik | n_peristiwa_sah | n_padu_s2_keputusan | had_bersyarat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | 4048 | 49 | 1986 | 2013 | 7.0 | 39.6 | 53.5 | 76.4 | 45.2 | 577 | 30.1 | 13642 | 200 | AKTIF |
| 2024 | 3744 | 58 | 1537 | 2149 | 5.5 | 52.8 | 41.7 | 80.4 | 55.6 | 457 | 25.3 | 14151 | 116 | AKTIF |
| 2025 | 4507 | 98 | 2326 | 2083 | 8.9 | 50.7 | 40.4 | 68.6 | 45.5 | 853 | 31.2 | 13998 | 189 | AKTIF |


## 2. Kohort "naik dan naik" (Step 2b)

| tahun | n_kohort | pct_melebihi_100 | median_naik_penuh | median_naik_hari63 | median_hari_chandelier | median_pul_chandelier | pct_terpotong |
|---|---|---|---|---|---|---|---|
| 2023.0 | 420.0 | 31.4 | 77.7 | 39.9 | 92.0 | 20.0 | 0.0 |
| 2024.0 | 374.0 | 22.7 | 65.3 | 37.3 | 73.0 | 14.1 | 0.0 |
| 2025.0 | 470.0 | 39.8 | 87.0 | 39.8 | 82.0 | 18.6 | 32.6 |


Kohort ini lebih kuat pada 2025 daripada 2024, tetapi arahnya sama pada kedua-dua tahun: run yang masih naik pada hari ke-63 pergi jauh lebih tinggi daripada yang reda.


## 3. Signal ENTRY — kekal konsisten lawan tahun tertentu


### KEKAL — kelas TERAS/UNIQUE/LANGKA dalam **semua** 3 tahun (2 signal)

| signal | kelas_2023 | lift_2023 | lift_presisi_2023 | n_2023 | keputusan_2023 | kelas_2024 | lift_2024 | lift_presisi_2024 | n_2024 | keputusan_2024 | kelas_2025 | lift_2025 | lift_presisi_2025 | n_2025 | keputusan_2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q5:atr_pct | UNIQUE | 10.306 | 6.746 | 91 | DITOLAK | UNIQUE | 11.67 | 8.638 | 94 | DITOLAK | UNIQUE | 14.334 | 8.571 | 90 | DITERIMA |
| rsi_lintas50&q5:atr_pct | UNIQUE | 13.024 | 7.895 | 55 | DITOLAK | UNIQUE | 15.148 | 10.044 | 48 | DITOLAK | UNIQUE | 19.602 | 9.909 | 46 | DITERIMA |


### TAHUN TERTENTU — kelas baik dalam sebahagian tahun sahaja (17 signal)

| signal | kelas_2023 | lift_2023 | keputusan_2023 | kelas_2024 | lift_2024 | keputusan_2024 | kelas_2025 | lift_2025 | keputusan_2025 |
|---|---|---|---|---|---|---|---|---|---|
| macd_cross&q1:cerun_ma50 | LANGKA | 5.285 | CALON | TIDAK BERGUNA | 0.079 | - | LANGKA | 5.445 | DITOLAK |
| rsi_lintas50&q1:j_52w_tinggi | UNIQUE | 5.453 | DITOLAK | TIDAK BERGUNA | 0.265 | DITOLAK | UNIQUE | 6.237 | DITOLAK |
| macd_cross&q1:j_52w_tinggi | LANGKA | 5.608 | DITOLAK | TIDAK BERGUNA | 0.587 | - | LANGKA | 8.1 | DITOLAK |
| pocket_pivot&q1:j_52w_tinggi | LANGKA | 6.692 | DITOLAK | TIDAK BERGUNA | 0.238 | - | LANGKA | 5.765 | DITOLAK |
| q1:j_52w_tinggi | UNIQUE | 5.365 | DITOLAK | TIDAK BERGUNA | 0.556 | DITOLAK | UNIQUE | 4.044 | DITOLAK |
| q5:julat20 | TIDAK BERGUNA | 1.194 | DITOLAK | UNIQUE | 9.778 | DITOLAK | UNIQUE | 11.88 | CALON |
| rsi_lintas50&q5:julat20 | TIDAK BERGUNA | 0.694 | DITOLAK | UNIQUE | 9.615 | DITOLAK | UNIQUE | 23.76 | DITOLAK |
| ema_crossback&q5:bb_lebar | TIDAK BERGUNA | 3.874 | - | LANGKA | 7.383 | DITOLAK | TIDAK BERGUNA | 7.92 | - |
| pocket_pivot&q5:atr_pct | TIDAK BERGUNA | 9.369 | - | LANGKA | 8.614 | DITOLAK | TIDAK BERGUNA | 20.048 | - |
| q1:roc20 | TIDAK BERGUNA | 1.056 | - | SEDERHANA | 2.222 | DITOLAK | UNIQUE | 3.545 | DITOLAK |
| q1:j_ma50 | TIDAK BERGUNA | 1.333 | - | TIDAK BERGUNA | 1.111 | - | TERAS | 3.295 | DITOLAK |
| q1:cerun_ma50 | COMMON BIASA | 0.792 | DITOLAK | TIDAK BERGUNA | 0.476 | - | TERAS | 3.24 | DITOLAK |
| q5:bb_lebar | TIDAK BERGUNA | 1.306 | DITOLAK | SEDERHANA | 2.063 | DITOLAK | TERAS | 9.876 | CALON |
| rsi_lintas50&q1:cerun_ma50 | TIDAK BERGUNA | 0.375 | DITOLAK | TIDAK BERGUNA | 0.278 | - | UNIQUE | 4.502 | DITOLAK |
| q5:j_ema9 | TIDAK BERGUNA | 0.472 | DITOLAK | TIDAK BERGUNA | 1.984 | DITOLAK | UNIQUE | 6.93 | DITOLAK |
| rsi_lintas50&q5:bb_lebar | TIDAK BERGUNA | 0.778 | DITOLAK | TIDAK BERGUNA | 1.19 | DITOLAK | UNIQUE | 21.06 | DITOLAK |
| rsi_lintas50&q5:rs_spy_6b | TIDAK BERGUNA | 2.3 | - | UNIQUE | 3.299 | DITOLAK | TIDAK BERGUNA | 3.267 | - |


### Signal berstatus CALON dalam SEMUA tahun (0)

_(tiada baris)_


Inilah satu-satunya senarai yang layak diteruskan ke tahun berikutnya. Gate 8.1 memerlukan ≥ 2 tahun LAIN; selepas satu tahun lagi (2023) senarai ini boleh dinaik taraf ke DITERIMA jika kelasnya kekal.


## 4. HOLD, EXIT dan SISTEM merentas tahun

| tahun | entry_padu | entry_super | hold | exit | sistem |
|---|---|---|---|---|---|
| 2023 | 7/20 | 5/20 | 0/18 | 0/64 | 0/234 |
| 2024 | 12/18 | 6/18 | 0/18 | 0/62 | 0/234 |
| 2025 | 18/19 | 11/19 | 11/18 | 0/62 | 0/234 |


Lulus BH-FDR q ≤ 0.01. **Keluarga EXIT dan SISTEM kosong pada setiap tahun.**


### Kelas pullback (Step 5) — stabil merentas tahun

| tahun | PULLBACK SIHAT | n_PULLBACK SIHAT | PULLBACK PASARAN | n_PULLBACK PASARAN | AMARAN | n_AMARAN |
|---|---|---|---|---|---|---|
| 2023.0 | 91.5 | 1322.0 | 80.0 | 115.0 | 46.2 | 4568.0 |
| 2024.0 | 88.4 | 1034.0 | 82.6 | 408.0 | 47.2 | 4489.0 |
| 2025.0 | 88.9 | 1394.0 | 92.0 | 311.0 | 50.8 | 4790.0 |


Perbezaan SIHAT/PASARAN lawan AMARAN kekal besar pada kedua-dua tahun. Ini hasil HOLD yang paling boleh dipercayai dalam kajian ini.


### HOLD yang lulus FDR dalam semua tahun

0 signal: tiada


## 5. Step 7b — tiga rujukan wajib merentas tahun

| tahun | REF_pegang_252_jangkaan | REF_pegang_252_median | REF_chandelier_4atr_jangkaan | REF_chandelier_4atr_median | REF_jual_hari63_jangkaan | REF_jual_hari63_median | rujukan_menang | n_sistem_mengalahkan_semua |
|---|---|---|---|---|---|---|---|---|
| 2023 | 16.246 | 9.85 | 1.507 | -4.61 | 2.861 | 1.65 | REF_pegang_252 | 0 |
| 2024 | 8.677 | -2.01 | -0.022 | -5.44 | 1.34 | -0.54 | REF_pegang_252 | 0 |
| 2025 | 27.571 | 10.14 | 6.069 | -5.0 | 4.846 | 1.63 | REF_pegang_252 | 0 |


**Rujukan (c) "pegang tanpa jual" menang pada kedua-dua tahun, dan 0/234 sistem mengalahkan ketiga-tiga rujukan pada kedua-dua tahun.** Tetapi perhatikan medianya: positif pada 2025, negatif pada 2024 — jangkaan positif itu dipacu hujung kanan taburan, bukan dagangan biasa.


## 6. Step 9 — prestasi portfolio merentas tahun

| tahun | sistem | n_posisi_dibuka | n_dagangan_ditutup | purata_slot_terisi | pulangan_tahun | median_bulanan | pct_bulan_ge10 | pct_bulan_positif | bulan_terburuk | mdd | pusing_ganti_bulanan | spy_pulangan_tahun | spy_mdd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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

**0 daripada 24 kombinasi (sistem × tahun) mencapai median +10% sebulan.**

- 2023: terbaik `REF_pegang_252` median bulanan **3.44%**, MDD -21.11%, 8 posisi dibuka (SPY 26.71%)

- 2024: terbaik `hari_agihan|X=5%,Y=ema9` median bulanan **2.34%**, MDD -29.40%, 46 posisi dibuka (SPY 25.59%)

- 2025: terbaik `REF_pegang_252` median bulanan **5.65%**, MDD -38.71%, 8 posisi dibuka (SPY 18.01%)


## 7. Kesimpulan merentas tahun

1. **Kelas kekal, keputusan tidak.** 2 signal mengekalkan kelas TERAS/UNIQUE/LANGKA pada semua 3 tahun — kesemuanya konteks pengembangan kemeruapan (ATR%, julat 20 hari, lebar Bollinger pada kuintil tertinggi): `q5:atr_pct`, `rsi_lintas50&q5:atr_pct`. **Tetapi 0 berstatus CALON atau DITERIMA pada semua 3 tahun.** Kelas Step 4 (lift atas populasi peristiwa) konsisten; gate yang keras (G4 bootstrap, G5 outlier) tidak. Itulah jurang paling penting dalam perbandingan ini: kekonsistenan lift **bukan** kekonsistenan kelebihan dagangan.

2. **Konsisten:** pemicu klasik tunggal mencapai kelas TERAS/UNIQUE/LANGKA dalam 0 daripada 18 kombinasi (pemicu × tahun). Hipotesis "magnitud ada pada konteks, bukan pemicu" disokong pada setiap 3 tahun.

3. **Konsisten:** keluarga EXIT kosong dan SISTEM kosong pada FDR setiap tahun; rujukan yang menang Step 7b setiap tahun: 2023=`REF_pegang_252`, 2024=`REF_pegang_252`, 2025=`REF_pegang_252`.

4. **Konsisten:** kelas pullback membezakan sambungan ke puncak baru setiap tahun — 2023: SIHAT 91.5% / PASARAN 80.0% lawan AMARAN 46.2%; 2024: SIHAT 88.4% / PASARAN 82.6% lawan AMARAN 47.2%; 2025: SIHAT 88.9% / PASARAN 92.0% lawan AMARAN 50.8%.

5. **Tidak konsisten:** magnitud mutlak. Median pulangan rujukan pegang-252 +9.8% (2023), -2.0% (2024), +10.1% (2025); kohort masih_naik yang melebihi +100%: 31.4% (2023), 22.7% (2024), 39.8% (2025). Tahun berbeza = rejim berbeza; angka tahun terbaik bukan jangkaan.

6. **Paling penting untuk keputusan dagangan: arah bertukar dari tahun ke tahun.** Portfolio berasaskan signal kalah kepada entri rawak pada 2 daripada 3 tahun.

   - 2023: SPY +26.71%, rawak terbaik +10.72%; **2/6** sistem kalah kepada SPY dan **0/6** kalah kepada entri rawak. Terbaik yang mengalahkan rawak: `REF_chandelier_4atr` (+56.37%) dengan 42 posisi dibuka.

   - 2024: SPY +25.59%, rawak terbaik +20.48%; **6/6** sistem kalah kepada SPY dan **6/6** kalah kepada entri rawak.

   - 2025: SPY +18.01%, rawak terbaik +29.47%; **5/6** sistem kalah kepada SPY dan **5/6** kalah kepada entri rawak. Terbaik yang mengalahkan rawak: `REF_pegang_252` (+128.93%) dengan 8 posisi dibuka.

   Tiga tahun, tiga keputusan berbeza: 2023 signal mengalahkan rawak, 2024 kalah sepenuhnya, 2025 kalah kecuali satu kes 8 posisi. **Itu taburan, bukan kelebihan.** Portfolio 8 slot bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil (lihat `n_posisi_dibuka`).

   Sasaran +10% sebulan (median): **0 daripada 24** kombinasi (sistem × tahun) mencapainya.

7. **2 signal DITERIMA** (gate 8.1 dipenuhi) — tetapi lihat amaran percanggahan di bawah.

   - 2025: `rsi_lintas50&q5:atr_pct` DITERIMA, tetapi DITOLAK pada 2023, 2024 (gagal G4 bootstrap / G5 outlier di sana).

   - 2025: `q5:atr_pct` DITERIMA, tetapi DITOLAK pada 2023, 2024 (gagal G4 bootstrap / G5 outlier di sana).


> **AMARAN.** Gate 8.1 hanya memerlukan **kelas yang sama** dalam ≥ 2 tahun lain, bukan keputusan yang sama. Signal di atas lulus kerana kelas Step 4-nya konsisten, sedangkan tahun yang mengesahkannya menolaknya pada gate keras. Spec tidak diubah selepas melihat hasil; mengetatkan gate 8.1 (memerlukan CALON, bukan sekadar kelas sama) ialah keputusan pengguna.
