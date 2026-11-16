# CS18: "ujian solid" bagi lorong "pegang berbulan-bulan" (T) (backtest; BUKAN bukti)

Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (ab). Dijana `cs_solid18.py`; jangan sunting.

- Lorong ini: beli selepas isyarat, pegang hingga 6 bulan (126 hari dagangan) dengan stop loss longgar (6×ATR14), tiada jualan lain. Tiada tapisan saham Shariah (arahan pengguna).
- Dinilai pada saham yang carian tidak lihat: 5,105 calon CS17 (2,564 berkod `T13`–`T2576`), 12 setup papan lama, 300 peraturan rawak (kawalan), 300 peraturan rawak dengan prasyarat "hasil suku tumbuh ≥ 20 %", dan setiap prasyarat tanpa isyarat beli.
- Semakan pariti: angka sama dengan `hasil/CS17/calon.csv.gz` (beza terbesar 0.000005). Kesemua 12 setup papan lama dipadankan semula (bilangan belian dan kadar naik besar sama dengan papan CS08).

## 1. Takrif SOLID (semua mesti benar; sama bentuk dengan ujian solid setup F)

- S1 cukup belian: ≥ 300 belian, ≥ 10 tahun, ≥ 20 belian pada 2025–26.
- S2 kelebihan jelas: kadar naik besar melebihi saham rawak hari sama sebanyak ≥ 3 mata, dan positif dalam ketiga-tiga tempoh.
- S3 tahun demi tahun: lebih baik daripada rawak dalam ≥ 70 % tahun (tahun dengan ≥ 15 belian; sekurang-kurangnya 8 tahun).
- S4 tiga angka lorong: lebih baik daripada rawak bagi naik besar (≥ +50 % sebelum −15 %), capai +100 % DAN dijual dengan untung ≥ +30 %.
- S5 tidak bergantung pada beberapa hari: selepas 10 hari terbaik dibuang, masih ≥ +1 mata.
- S6 tahan ubah parameter: ≥ 60 % varian parameter lain bagi isyarat beli yang sama masih lebih baik daripada rawak.
- S7 isyarat beli menambah: ≥ +1 mata di atas "prasyarat sahaja".

## 2. Keputusan

- **SOLID: 1,672 daripada 2,576 setup lorong ini** (2 daripada 12 setup papan lama: `T05`, `T10`). Selepas membuang yang serupa (belian bertindih ≥ 50 %): **1,155 setup berbeza**.
- Ujian (B1) takrif boleh dipercayai: peraturan rawak yang lulus SOLID = 14 daripada 300 (4.7 %; perlu ≤ 5 %) → ya. Calon yang lulus: 52.4 %; anggaran bahagian nasib 9 %.
- Ujian (B2) isyarat beli menambah di atas prasyarat "hasil suku tumbuh ≥ 20 %": calon ber-prasyarat itu lulus 57.5 %; peraturan rawak dengan prasyarat yang sama lulus 27.0 % (perlu beza ≥ 10 mata) → ya.
- Berapa peratus lulus setiap syarat (calon · peraturan rawak · rawak + hasil tumbuh): S1 80 · 91 · 79; S2 78 · 8 · 38; S3 65 · 19 · 50; S4 95 · 46 · 84; S5 77 · 10 · 47; S7 94 · 36 · 53.
- Antara 2,576 setup berkod T, bilangan yang GAGAL setiap syarat: S1 386; S2 156; S3 660; S4 66; S5 339; S7 56; S6 3 (antara yang lulus syarat lain). 554 setup solid tidak dapat diuji S6 (kurang daripada 3 varian lain).
- 914 daripada 1,672 setup solid memakai prasyarat "hasil suku tumbuh ≥ 20 %". 33 bergantung pada tarikh laporan kewangan akan datang; boleh dibuat tanpa tarikh tepat: 1,672 (1,155 berbeza).
- Kes MXL (Mac–Jun 2026; satu contoh): 789 setup solid memberi isyarat beli pada MXL.

## 3. Gambaran (nilai tengah; daripada 100 belian; dalam kurungan = saham rawak hari sama yang dipegang dengan cara sama)

| | Naik besar | Capai +100 % | Dijual ≥ +30 % | Menang % | Purata setiap dagangan % | Rugi ≥ 15 % % | Dagangan biasa (nilai tengah) % | Belian |
|---|---|---|---|---|---|---|---|---|
| Solid yang berbeza (1,155) | 21.2 (15.0) | 6.5 (3.6) | 22.7 (18.9) | 46 (46) | +6.8 (+3.9) | 41 (39) | -4.8 | 598 |
| Semua solid (1,672) | 20.3 (13.9) | 6.3 (3.4) | 22.1 (17.9) | 46 (46) | +6.6 (+3.7) | 41 (39) | -4.9 | 610 |
| Tidak solid (904) | 19.3 (13.8) | 5.8 (3.3) | 21.9 (17.7) | 46 (46) | +5.8 (+3.5) | 40 (39) | -4.5 | 336 |
| Semua setup lorong ini (2,576) | 20.0 (13.9) | 6.1 (3.3) | 22.0 (17.8) | 46 (46) | +6.4 (+3.7) | 41 (39) | -4.8 | 510 |

- Solid yang berbeza: lebih baik daripada rawak dalam 87 % tahun (nilai tengah).
- **Rugi besar:** 312 daripada 1,672 setup solid (233 daripada 1,155 yang berbeza) rugi ≥ 15 % TIDAK lebih kerap daripada saham rawak hari sama (lajur `rugi_ok`). Menang ≥ 50 %: 158 solid (121 berbeza). Dua lajur ini maklumat, bukan syarat SOLID.

## 4. Senarai pendek: 1,155 setup SOLID yang berbeza

| ID | Prasyarat | Isyarat beli | Syarat saham | Naik besar (rawak) | Capai +100 % (rawak) | Dijual ≥ +30 % (rawak) | Tahun lebih baik | Menang % (rawak) | Purata % (rawak) | Rugi ≥ 15 % % (rawak) | Belian | Boleh dibuat | MXL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `T15` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s8: a14_kali_0_5=0.688, atr_14=26, np_ambang_2=1, pivot_k_3=2, rolling_20=36, rolling_50=80) | tutup > MA20 + ATR% >= 4 | **34.3** (20.9) | **11.1** (4.8) | **32.3** (26.1) | 8/8 | 57 (57) | +17.3 (+12.5) | 32 (30) | 359 | ya | – |
| `T58` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 2: rolling_50=34, shift_2=3) | MACD > isyarat + ATR% >= 4 | **33.5** (20.6) | **10.3** (4.7) | **32.2** (24.7) | 9/9 | 54 (56) | +15.2 (+11.1) | 33 (31) | 397 | ya | – |
| `T226` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M125 2-Bar Breakout (benih M, varian 1: had_henti=0.799, henti_atr=1.979, shift_2=3, shift_3=6) | RSI14 > 50 + ATR% >= 4 | **32.9** (18.8) | **9.4** (4.3) | **31.8** (23.1) | 9/9 | 52 (53) | +14.1 (+9.3) | 37 (34) | 371 | ya | – |
| `T23` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | RSI14 > 50 + ATR% >= 4 | **32.4** (18.3) | **9.7** (4.0) | **33.0** (22.4) | 9/9 | 54 (52) | +14.6 (+8.4) | 36 (35) | 373 | ya | – |
| `T28` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, varian 1: had_henti=0.732, henti_pct=13.462, hh_kali_0_1=0.119, keluar_sma=19, shift_5=8, tmax=6) | Supertrend naik + ATR% >= 4 | **32.4** (17.8) | **10.9** (3.8) | **31.7** (22.1) | 8/9 | 51 (52) | +13.0 (+8.1) | 37 (35) | 312 | ya | – |
| `T561` | nisbah 4% (10 hari) > 2 + >= 60% saham sektor di atas MA50 | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: rank_ambang_0_8=0.508, shift_21=11) | RS >= 90 + ATR% >= 4 | **32.0** (20.3) | **10.4** (4.4) | **27.1** (24.4) | 9/10 | 54 (56) | +14.1 (+10.4) | 35 (31) | 384 | ya | – |
| `T196` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K05.001 tutup silang atas jalur atas BB(10, 1.5) | RSI14 > 50 + ATR% >= 4 | **31.8** (17.8) | **9.6** (3.9) | **32.2** (22.2) | 8/9 | 53 (52) | +14.5 (+8.3) | 38 (34) | 311 | ya | – |
| `T305` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K07.001 tutup silang atas sma5 | MACD > isyarat + ATR% >= 4 | **31.7** (21.6) | **9.7** (5.1) | **29.8** (25.1) | 6/8 | 53 (55) | +12.9 (+11.6) | 34 (32) | 309 | ya | – |
| `T828` | nisbah 4% (10 hari) > 2 + >= 60% saham industri di atas MA50 | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: rank_ambang_0_8=0.508, shift_21=11) | RS >= 70 + ATR% >= 4 | **31.1** (20.7) | **8.7** (4.3) | **28.3** (25.1) | 7/10 | 60 (59) | +16.3 (+11.9) | 28 (27) | 527 | ya | – |
| `T266` | nisbah 4% (10 hari) > 2 + >= 60% saham sektor di atas MA50 | M84 Jarak purata bergerak MAD 21/200 (benih M, parameter asal) | Supertrend naik + ATR% >= 4 | **31.0** (21.2) | **10.8** (4.6) | **26.0** (25.0) | 7/8 | 50 (57) | +10.9 (+11.3) | 36 (29) | 342 | ya | – |
| `T2063` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham industri di atas MA50 | K08.023 sma50 silang atas sma200 | Supertrend naik + ATR% >= 4 | **30.6** (18.2) | **9.5** (4.4) | **34.4** (25.4) | 8/9 | 58 (56) | +17.7 (+11.0) | 30 (33) | 474 | ya | – |
| `T2521` | SPY bawah SMA200 | K18.012 jatuh >= 20% dalam 3 hari | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | **30.3** (26.6) | **10.3** (9.1) | **39.9** (38.6) | 9/9 | 66 (65) | +24.3 (+23.9) | 23 (25) | 1,184 | ya | – |
| `T1840` | Nov-Apr + hasil suku terkini tumbuh >= 20% | K08.013 sma10 silang atas sma50 | RS >= 70 + ATR% >= 4 | **29.5** (16.9) | **7.9** (4.1) | **29.8** (20.9) | 10/10 | 55 (49) | +15.7 (+5.6) | 34 (38) | 403 | ya | 20260409 |
| `T259` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | K09.021 MACD(3,10,16) silang naik atas sifar | RS >= 90 + ATR% >= 4 | **29.1** (16.1) | **10.2** (4.2) | **28.8** (19.5) | 8/8 | 44 (46) | +9.1 (+3.9) | 45 (42) | 354 | ya | 20260615 |
| `T2325` | industri 20% teratas (pulangan 21 sesi) | K08.022 ema50 silang atas ema150 | MA20 > MA50 + ATR% >= 4 | **29.0** (19.3) | **8.1** (4.9) | **32.1** (24.8) | 7/10 | 59 (54) | +17.2 (+10.3) | 34 (34) | 455 | ya | – |
| `T1284` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + >= 60% saham industri di atas MA50 | M152 Spike & Ledge (benih M, parameter asal) | tutup > MA200 + ATR% >= 4 | **29.0** (18.8) | **9.8** (4.8) | **31.0** (22.5) | 8/9 | 53 (51) | +11.2 (+7.8) | 37 (37) | 407 | ya | – |
| `T569` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: rank_ambang_0_8=0.508, shift_21=11) | Supertrend naik + ATR% >= 4 | **28.8** (19.2) | **10.6** (4.8) | **27.9** (24.0) | 8/10 | 53 (52) | +13.4 (+9.1) | 37 (35) | 444 | ya | 20260529 |
| `T1477` | QQQ SMA10 > SMA20 + hasil suku terkini tumbuh >= 20% | K15.005 gap >= 3.0% | RS >= 70 + ATR% >= 4 | **28.8** (18.0) | **10.4** (4.5) | **28.8** (21.7) | 10/10 | 52 (49) | +14.8 (+6.3) | 38 (39) | 569 | ya | 20260421 |
| `T1407` | turun-naik SPY menurun (21 hari < 63 hari) + sektor 3 teratas (pulangan 63 sesi) | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 2: e_kali_1_1=1.237, rolling_20=40, rolling_250=211, sd250_ambang_20=29, sma20_ambang_10=9, sma20_ambang_5000000=2560294) | RS >= 70 + ATR% >= 4 | **28.8** (16.6) | **5.8** (4.3) | **26.5** (22.6) | 9/9 | 50 (50) | +9.2 (+7.7) | 40 (39) | 344 | ya | – |
| `T1680` | Mei-Okt + sektor 3 teratas (pulangan 63 sesi) | M78 Alvarez Pecahan Mingguan DTAYS (benih M, varian 1: dv21_ambang_15000000_0=8137357.443, k_atr=5, open_kali_0_92=0.549, r20_ambang_0_3=0.258, rolling_19=23, rolling_21=40) | Supertrend naik + ATR% >= 4 | **28.5** (19.3) | **9.2** (5.6) | **30.3** (25.3) | 9/11 | 53 (51) | +16.8 (+10.2) | 40 (39) | 499 | ya | 20260501 |
| `T2372` | – | K02.016 RSI(10) silang atas 25 | RS >= 70 + >= 30% di bawah puncak 52 minggu | **28.4** (22.1) | **12.2** (6.1) | **33.6** (28.9) | 10/12 | 58 (57) | +18.6 (+13.9) | 31 (32) | 559 | ya | – |
| `T622` | Mei-Okt + hasil suku terkini tumbuh >= 20% | K09.006 MACD(8,17,9) silang naik atas sifar | RS >= 90 + ATR% >= 4 | **28.4** (17.6) | **11.5** (4.6) | **27.5** (22.9) | 7/8 | 50 (50) | +14.6 (+7.2) | 41 (39) | 313 | ya | – |
| `T1300` | SPY atas SMA200 + 5-19 sesi selepas earnings | K11.017 Supertrend(20, 2.0) bertukar naik | RS >= 90 + ATR% >= 4 | **28.3** (17.6) | **8.0** (4.7) | **28.3** (21.6) | 11/12 | 48 (48) | +13.0 (+6.2) | 42 (40) | 427 | ya | – |
| `T796` | Mei-Okt + >= 60% saham sektor di atas MA50 | N80 Tinggi sepanjang masa (benih N) | MA20 > MA50 + ATR% >= 4 | **28.3** (17.7) | **8.8** (4.6) | **29.2** (24.5) | 11/13 | 51 (54) | +12.9 (+10.5) | 40 (35) | 456 | ya | 20260501 |
| `T2073` | QQQ ON + >= 60% saham industri di atas MA50 | M107 Golden Cross SMA50/200 (benih M, varian 2: rma_atr_14=16, rma_atr_kali_3=2.729, rolling_200=131, rolling_50=59) | tutup > MA200 + ATR% >= 4 | **28.2** (19.6) | **10.8** (5.1) | **29.6** (25.7) | 9/10 | 53 (54) | +13.6 (+10.5) | 37 (36) | 595 | ya | – |
| `T2118` | >= 60% saham di atas MA50 + industri 20% teratas (pulangan 21 sesi) | K08.020 ema50 silang atas ema100 | Supertrend naik + ATR% >= 4 | **28.1** (18.6) | **6.8** (4.7) | **31.5** (24.4) | 6/8 | 57 (54) | +15.7 (+10.1) | 34 (35) | 413 | ya | – |
| `T1250` | SPY atas SMA200 + 5-19 sesi selepas earnings | N22 BB pecah atas + RSI (benih N) | RS >= 90 + ATR% >= 4 | **27.9** (17.2) | **7.4** (4.4) | **25.1** (21.1) | 11/14 | 48 (49) | +8.7 (+6.2) | 43 (39) | 459 | ya | – |
| `T1366` | Mei-Okt + >= 60% saham sektor di atas MA50 | M149 3-Step Pullback (benih M, parameter asal) | RS >= 70 + ATR% >= 4 | **27.9** (18.9) | **9.4** (4.9) | **30.8** (25.6) | 11/12 | 52 (55) | +14.9 (+10.8) | 39 (35) | 678 | ya | 20260521 |
| `T2289` | SPY atas SMA200 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | K08.021 sma50 silang atas sma150 | tutup > MA200 + ATR% >= 4 | **27.8** (19.6) | **8.5** (5.2) | **30.4** (25.3) | 10/11 | 54 (53) | +12.9 (+10.2) | 36 (36) | 655 | ya | – |
| `T1046` | keluasan naik >= 10 mata dalam 10 sesi + >= 60% saham industri di atas MA50 | M34 Carter TTM Squeeze (benih M, varian 1: a20_kali_1_5=1.392, bahagi_20=29, rolling_10=14, rolling_50=87, sd_kali_2=1.284, shift_5=6) | RS >= 70 + ATR% >= 4 | **27.7** (19.1) | **7.3** (4.7) | **26.2** (23.1) | 12/14 | 50 (52) | +10.5 (+8.1) | 39 (36) | 667 | ya | 20260410 |
| `T1849` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 | K11.009 Supertrend(10, 3.0) bertukar naik | RS >= 90 + ATR% >= 4 | **27.7** (18.4) | **9.8** (5.0) | **24.8** (21.1) | 10/11 | 42 (48) | +5.5 (+6.0) | 45 (39) | 347 | ya | – |
| `T1467` | Mei-Okt + industri 20% teratas (pulangan 63 sesi) | M78 Alvarez Pecahan Mingguan DTAYS (benih M, varian 1: dv21_ambang_15000000_0=8137357.443, k_atr=5, open_kali_0_92=0.549, r20_ambang_0_3=0.258, rolling_19=23, rolling_21=40) | Supertrend naik + ATR% >= 4 | **27.7** (19.5) | **9.8** (5.7) | **29.8** (25.6) | 8/10 | 53 (52) | +18.0 (+10.6) | 38 (38) | 470 | ya | 20260501 |
| `T1599` | SPY atas SMA200 + tiada earnings dalam 20 sesi akan datang | M81 Bensdorp Long Trend High Momentum (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **27.6** (18.1) | **9.6** (5.1) | **25.3** (21.2) | 9/9 | 47 (47) | +8.1 (+5.3) | 42 (41) | 384 | ya | – |
| `T1471` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + tiada earnings dalam 20 sesi akan datang | M13 Garis Trend Action/Safety Line (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **27.6** (16.9) | **10.0** (4.6) | **24.0** (20.9) | 11/13 | 46 (48) | +9.2 (+5.8) | 43 (40) | 442 | ya | – |
| `T568` | Nov-Apr + 5-19 sesi selepas earnings | K05.006 tutup silang atas jalur atas BB(20, 2.0) | RS >= 90 + ATR% >= 4 | **27.6** (16.9) | **7.1** (4.0) | **24.9** (20.4) | 8/9 | 49 (48) | +8.8 (+5.1) | 41 (38) | 337 | ya | – |
| `T2437` | >= 60% saham di atas MA50 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) (benih M, varian 2: atr_14=13, c_ambang_0_75=0.714, o_ambang_0_05=0.056, rolling_20=24, rolling_50=30, run_ambang_0_3=0.412) | MACD > isyarat + RS >= 70 | **27.6** (19.6) | **11.7** (5.4) | **25.1** (23.6) | 7/8 | 44 (49) | +8.9 (+7.9) | 45 (39) | 446 | ya | 20260420 |
| `T942` | turun-naik SPY menurun (21 hari < 63 hari) + industri 20% teratas (pulangan 63 sesi) | M52 Radge Weekend Trend Trader (benih M, varian 1: bo_kali_0_6=0.869, c_kali_0_6=0.441, roc_ambang_0_3=0.325, rolling_10=11, rolling_20=23, rolling_50=63) | ADX > 25 + ATR% >= 4 | **27.5** (18.8) | **9.4** (5.3) | **28.8** (23.6) | 12/13 | 51 (50) | +14.8 (+8.7) | 36 (39) | 597 | ya | 20260501 |
| `T1720` | Nov-Apr | M81 Bensdorp Long Trend High Momentum (benih M, varian 1: a20_kali_3=4.282, close_ambang_5=4, nilai20_ambang_50000000=73581098, rma_atr_20=40, rolling_25=49, tt_kali_0_75=0.539) | RS >= 90 + ATR% >= 4 | **27.5** (17.6) | **11.5** (5.1) | **21.1** (20.3) | 8/9 | 47 (44) | +9.2 (+4.1) | 41 (43) | 375 | ya | 20260424 |
| `T320` | SPY atas SMA200 + hasil suku terkini tumbuh >= 20% | K23.004 RS silang atas 90 | templat trend Minervini + ATR% >= 4 | **27.4** (17.2) | **7.7** (4.6) | **28.3** (20.4) | 8/8 | 47 (45) | +9.4 (+4.5) | 42 (42) | 339 | ya | 20260420 |
| `T1636` | nisbah 4% (10 hari) > 2 + >= 60% saham industri di atas MA50 | K16.005 gap-and-go (buka > tinggi semalam + 1.0%) | RS >= 90 + ATR% >= 4 | **27.4** (19.4) | **8.1** (5.2) | **23.2** (22.0) | 7/8 | 47 (48) | +6.8 (+6.6) | 45 (40) | 383 | ya | 20260421 |
| `T1420` | nisbah 4% (10 hari) > 2 | M80 Radge Saluran Purata Bergerak (MAC) (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **27.3** (20.3) | **8.8** (5.2) | **26.5** (24.1) | 11/12 | 49 (53) | +16.2 (+9.7) | 40 (35) | 535 | ya | – |
| `T478` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | K19.011 pecah atas Keltner(30, 1.0) | RS >= 90 + ATR% >= 4 | **27.2** (17.0) | **10.4** (4.6) | **28.1** (20.3) | 9/9 | 46 (46) | +9.4 (+4.7) | 44 (41) | 345 | ya | – |
| `T1313` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 | M152 Spike & Ledge (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **27.1** (17.1) | **10.3** (4.6) | **26.7** (20.3) | 9/10 | 48 (47) | +9.0 (+5.5) | 40 (40) | 329 | ya | – |
| `T648` | Mei-Okt + hasil suku terkini tumbuh >= 20% | M156 Single Penetration (DiNapoli) (benih M, parameter asal) | MA50 > MA200 + ATR% >= 4 | **27.0** (18.5) | **9.1** (4.8) | **28.5** (24.2) | 10/13 | 52 (52) | +13.7 (+9.1) | 38 (37) | 526 | ya | 20260602 |
| `T2416` | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | K12.020 ADX(20) silang atas 35 & +DI > -DI | RS >= 70 + ATR% >= 4 | **27.0** (18.9) | **11.0** (5.1) | **25.2** (23.0) | 11/12 | 45 (49) | +8.3 (+7.8) | 45 (40) | 489 | ya | 20260429 |
| `T2203` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham industri di atas MA50 | K05.003 tutup silang atas jalur atas BB(10, 2.5) | RS >= 90 + ATR% >= 4 | **26.9** (17.7) | **11.7** (4.8) | **28.3** (22.4) | 12/12 | 48 (49) | +13.7 (+7.3) | 43 (40) | 427 | ya | – |
| `T2498` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham sektor di atas MA50 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) (benih M, varian 1: atr_14=11, c_ambang_0_75=0.98, o_ambang_0_05=0.064, rolling_20=31, rolling_50=83, run_ambang_0_3=0.259) | MA20 > MA50 + ATR% >= 4 | **26.9** (18.9) | **10.3** (5.0) | **26.7** (24.2) | 7/8 | 48 (53) | +8.8 (+9.5) | 41 (35) | 390 | ya | 20260508 |
| `T2082` | Nov-Apr | K18.011 jatuh >= 15% dalam 3 hari | RS >= 90 | **26.9** (17.8) | **10.9** (4.9) | **23.6** (21.8) | 8/8 | 41 (46) | +6.3 (+4.9) | 47 (42) | 432 | ya | – |
| `T1426` | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | M137 Livermore System (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **26.8** (18.3) | **8.2** (5.0) | **26.5** (22.2) | 14/15 | 48 (48) | +9.6 (+7.0) | 41 (40) | 656 | ya | 20260421 |
| `T500` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | K09.010 MACD(6,19,6) silang naik | RS >= 90 + ATR% >= 4 | **26.8** (16.5) | **10.7** (4.5) | **27.7** (20.1) | 10/10 | 45 (46) | +8.2 (+4.3) | 44 (42) | 441 | ya | 20260615 |
| `T771` | keluasan naik >= 10 mata dalam 10 sesi + hasil suku terkini tumbuh >= 20% | N29 PSAR naik + tutup>MA50 (benih N) | RS >= 90 + ATR% >= 4 | **26.7** (15.3) | **8.0** (3.6) | **26.9** (19.6) | 11/11 | 50 (47) | +10.0 (+3.6) | 39 (41) | 412 | ya | – |
| `T1075` | QQQ ON + hasil suku terkini tumbuh >= 20% | K15.001 gap >= 2.0% | RS >= 70 + ATR% >= 4 | **26.7** (17.7) | **10.0** (4.4) | **28.5** (21.8) | 13/14 | 50 (49) | +13.9 (+6.2) | 39 (39) | 723 | ya | 20260417 |
| `T1945` | Nov-Apr + >= 60% saham industri di atas MA50 | K05.016 tutup silang atas jalur atas BB(50, 3.0) | RS >= 90 + ATR% >= 4 | **26.6** (17.5) | **8.3** (4.4) | **22.6** (19.2) | 9/10 | 44 (44) | +5.2 (+3.3) | 44 (43) | 349 | ya | – |
| `T797` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + >= 60% saham sektor di atas MA50 | M116 2/20 EMA Breakout (Landry) (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **26.6** (17.2) | **9.0** (4.5) | **25.2** (20.5) | 11/14 | 46 (47) | +7.4 (+5.4) | 44 (41) | 646 | ya | – |
| `T1839` | SPY atas SMA200 | M107 Golden Cross SMA50/200 (benih M, varian 2: rma_atr_14=16, rma_atr_kali_3=2.729, rolling_200=131, rolling_50=59) | dalam 15% dari puncak 52 minggu + ATR% >= 4 | **26.6** (17.4) | **9.7** (4.1) | **25.6** (23.3) | 7/9 | 53 (53) | +10.8 (+8.1) | 35 (36) | 402 | ya | – |
| `T2502` | – | M107 Golden Cross SMA50/200 (benih M, varian 1: rma_atr_14=16, rma_atr_kali_3=2.481, rolling_200=336, rolling_50=68) | tutup > MA50 + ATR% >= 4 | **26.6** (19.1) | **9.1** (5.1) | **28.9** (24.0) | 10/11 | 54 (51) | +13.5 (+8.8) | 34 (38) | 602 | ya | – |
| `T516` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | K24.004 bar pembalikan (buka <= 20%, tutup >= 70% julat) | RS >= 90 + ATR% >= 4 | **26.6** (16.3) | **10.2** (4.3) | **28.5** (20.2) | 12/12 | 46 (46) | +9.7 (+4.4) | 43 (42) | 527 | ya | 20260519 |
| `T1459` | Mei-Okt + hasil suku terkini tumbuh >= 20% | K09.003 MACD(12,26,9) silang naik atas sifar | dalam 15% dari puncak 52 minggu + ATR% >= 4 | **26.5** (17.7) | **9.1** (4.8) | **27.1** (23.3) | 8/9 | 52 (52) | +14.8 (+8.5) | 38 (37) | 339 | ya | 20260626 |
| `T423` | QQQ ON + hasil suku terkini tumbuh >= 20% | K24.002 bar pembalikan (buka <= 10%, tutup >= 80% julat) | RS >= 90 + ATR% >= 4 | **26.5** (16.0) | **8.8** (4.0) | **25.6** (19.9) | 11/12 | 44 (46) | +7.0 (+3.7) | 45 (43) | 535 | ya | 20260508 |
| `T1865` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 | M13 Garis Trend Action/Safety Line (benih M, varian 2: k=4) | RS >= 90 + ATR% >= 4 | **26.5** (16.9) | **10.1** (4.6) | **21.7** (20.1) | 11/13 | 43 (47) | +4.9 (+4.9) | 44 (41) | 554 | ya | – |
| … | 1095 lagi dalam `solid_t.csv.gz` | | | | | | | | | | | | |

## 5. Setup SOLID lain yang serupa dengan wakil di atas: 517

Senarai penuh dalam `solid_t.csv.gz` (lajur `serupa_dengan`).

## 6. Papan lama `T01`–`T12` (dinilai dengan mekanik yang sama)

| ID | Solid | Gagal syarat | Naik besar (rawak) | Tahun lebih baik | Menang % (rawak) | Rugi ≥ 15 % % (rawak) | Belian | Belian 2025–26 |
|---|---|---|---|---|---|---|---|---|
| `T01` | TIDAK | S3 | 33.1 (19.8) | 6/7 | 54 (55) | 33 (32) | 308 | 57 |
| `T02` | TIDAK | S3 | 33.8 (20.0) | 6/7 | 55 (56) | 33 (31) | 305 | 58 |
| `T03` | TIDAK | S1, S3, S5 | 28.6 (21.3) | 4/5 | 52 (54) | 37 (33) | 203 | 28 |
| `T04` | TIDAK | S1, S3 | 19.6 (13.8) | 4/7 | 37 (41) | 50 (48) | 260 | 26 |
| `T05` | ya | – | 17.3 (12.0) | 9/12 | 41 (43) | 46 (42) | 358 | 44 |
| `T06` | TIDAK | S1, S3 | 19.7 (13.8) | 4/7 | 37 (41) | 49 (48) | 259 | 26 |
| `T07` | TIDAK | S3 | 26.1 (16.5) | 6/7 | 49 (46) | 40 (41) | 330 | 52 |
| `T08` | TIDAK | S1 | 20.5 (14.4) | 7/8 | 38 (41) | 49 (48) | 297 | 51 |
| `T09` | TIDAK | S1, S2, S3 | 20.8 (12.9) | 3/5 | 38 (40) | 50 (48) | 207 | 31 |
| `T10` | ya | – | 17.1 (10.6) | 10/12 | 38 (41) | 44 (43) | 380 | 32 |
| `T11` | TIDAK | S1 | 20.9 (11.3) | 7/9 | 43 (46) | 42 (39) | 249 | 17 |
| `T12` | TIDAK | S1, S3 | 25.2 (17.9) | 3/5 | 47 (50) | 41 (38) | 242 | 43 |

## 7. "Prasyarat sahaja" (tanpa isyarat beli; rujukan)

| Prasyarat | Naik besar (rawak) | Kelebihan (mata) | Capai +100 % (rawak) | Dijual ≥ +30 % (rawak) | Tahun lebih baik | Menang % (rawak) | Rugi ≥ 15 % % (rawak) | Belian | Lulus S1–S5 |
|---|---|---|---|---|---|---|---|---|---|
| distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | 15.0 (10.8) | +4.1 | 3.6 (2.1) | 19.4 (15.2) | 11/13 | 54 (52) | 27 (28) | 2,472 | ya |
| Mei-Okt + hasil suku terkini tumbuh >= 20% | 14.0 (11.3) | +2.7 | 3.2 (2.3) | 17.7 (15.7) | 15/16 | 52 (50) | 29 (31) | 4,593 | TIDAK |
| follow-through day aktif (QQQ, 20 sesi) + hasil suku terkini tumbuh >= 20% | 15.5 (13.1) | +2.4 | 4.2 (3.1) | 19.2 (17.5) | 11/14 | 51 (50) | 32 (32) | 3,747 | TIDAK |
| nisbah 4% (10 hari) > 2 + hasil suku terkini tumbuh >= 20% | 13.0 (10.7) | +2.3 | 3.3 (2.2) | 17.0 (15.1) | 16/17 | 49 (48) | 32 (33) | 5,388 | TIDAK |
| breadth thrust Zweig aktif (20 sesi) + hasil suku terkini tumbuh >= 20% | 15.0 (12.8) | +2.2 | 4.0 (2.9) | 21.3 (19.1) | 11/14 | 56 (55) | 29 (29) | 2,187 | TIDAK |
| turun-naik SPY 21 hari <= 10% setahun + hasil suku terkini tumbuh >= 20% | 11.7 (9.5) | +2.2 | 2.7 (2.0) | 15.6 (13.2) | 13/15 | 47 (45) | 32 (32) | 4,270 | TIDAK |
| QQQ >= 10% di bawah puncak + hasil suku terkini tumbuh >= 20% | 17.6 (15.5) | +2.2 | 4.8 (3.5) | 24.6 (22.1) | 12/14 | 59 (56) | 27 (28) | 3,363 | TIDAK |
| Januari + hasil suku terkini tumbuh >= 20% | 12.6 (10.5) | +2.2 | 2.4 (2.1) | 15.9 (14.1) | 13/16 | 45 (44) | 35 (35) | 2,473 | TIDAK |
| turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | 13.1 (11.0) | +2.2 | 2.8 (2.1) | 17.5 (15.5) | 11/17 | 49 (48) | 32 (32) | 5,821 | TIDAK |
| turun-naik SPY 21 hari >= 25% setahun + hasil suku terkini tumbuh >= 20% | 15.5 (13.4) | +2.1 | 4.8 (3.0) | 21.7 (20.2) | 5/7 | 54 (53) | 31 (31) | 1,912 | TIDAK |
| rejim ON baharu (<= 10 sesi) + hasil suku terkini tumbuh >= 20% | 12.7 (10.7) | +2.0 | 2.9 (2.1) | 17.3 (15.6) | 16/17 | 49 (48) | 33 (33) | 5,276 | TIDAK |
| regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | 11.8 (9.8) | +2.0 | 2.6 (2.0) | 16.1 (13.9) | 14/17 | 47 (46) | 34 (34) | 5,433 | TIDAK |
| QQQ naik >= 3% dalam 5 sesi + hasil suku terkini tumbuh >= 20% | 12.6 (10.6) | +2.0 | 2.9 (2.2) | 17.5 (15.6) | 16/17 | 49 (48) | 32 (33) | 5,922 | TIDAK |
| QQQ RSI14 < 35 + hasil suku terkini tumbuh >= 20% | 12.7 (10.7) | +1.9 | 2.4 (2.0) | 19.1 (16.8) | 14/15 | 53 (51) | 32 (32) | 3,951 | TIDAK |
| SPY bawah SMA200 + hasil suku terkini tumbuh >= 20% | 15.7 (13.8) | +1.9 | 4.0 (2.8) | 22.3 (20.3) | 11/13 | 55 (53) | 31 (32) | 2,957 | TIDAK |

1 daripada 338 gabungan prasyarat lulus S1–S5 tanpa isyarat beli (penuh dalam `prasyarat.csv`).

## 8. Kaveat

- Senarai lorong ini sudah dipilih dengan saham yang sama, jadi "solid" bermaksud "paling tahan uji dalam backtest", BUKAN bukti.
- Ambang disalin daripada ujian solid setup F dan ditetapkan sebelum hasil dilihat. Tiada tapisan Shariah (arahan pengguna).
- Tiada saham delist dalam data: bagi pegang 6 bulan, saham yang gagal hilang dan angka condong ke atas lebih daripada lorong swing.
- 2025–26 pendek (isyarat hingga awal 2026 sahaja, kerana perlu 6 bulan penuh selepas beli).
- "Saham rawak hari sama" bagi menang, purata dan rugi = setiap saham layak pada hari dan kelas turun-naik yang sama, dibeli dan dipegang dengan cara yang sama (tanpa peraturan satu posisi).
- Kod T, `hasil/CS17/`, papan CS08, registry F dan kohort tidak diubah. Bukti hanya datang daripada papertrade (keputusan pengguna).
