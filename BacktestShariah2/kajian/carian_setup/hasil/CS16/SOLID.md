# CS16: "ujian solid" bagi setup F (backtest; BUKAN bukti)

Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (z). Dijana `cs_solid16.py`; jangan sunting.

- Permintaan pengguna 16 Nov 2026: beberapa setup F yang betul-betul solid, diukur dengan "5 % seminggu, 10 % seminggu, 10 % dua minggu". Tiada tapisan saham Shariah dalam pusingan ini (arahan pengguna).
- Dinilai pada saham yang carian tidak lihat: 4,923 calon CS13, setup lama yang dipercayai, 300 peraturan rawak (kawalan), 300 peraturan rawak dengan prasyarat "laporan kewangan dalam 1–5 hari", dan setiap prasyarat tanpa isyarat beli.
- Semakan pariti: angka sama dengan senarai utama (beza terbesar 0.000005).

## 1. Takrif SOLID (semua mesti benar)

- S1 cukup belian: ≥ 300 belian, ≥ 10 tahun, ≥ 20 belian pada 2025–26.
- S2 kelebihan jelas: kadar tangkap melebihi saham rawak hari sama sebanyak ≥ 3 mata, dan positif dalam ketiga-tiga tempoh.
- S3 tahun demi tahun: lebih baik daripada rawak dalam ≥ 70 % tahun (tahun dengan ≥ 15 belian; sekurang-kurangnya 8 tahun).
- S4 tiga angka pengguna: lebih baik daripada rawak bagi 5 % seminggu, 10 % seminggu DAN 10 % dua minggu.
- S5 tidak bergantung pada beberapa hari: selepas 10 hari terbaik dibuang, masih ≥ +1 mata.
- S6 tahan ubah parameter: ≥ 60 % varian parameter lain bagi isyarat beli yang sama masih lebih baik daripada rawak.
- S7 isyarat beli menambah: ≥ +1 mata di atas "prasyarat sahaja".

## 2. Keputusan

- **SOLID: 290 daripada 2,001 setup senarai utama** (4 setup lama). Selepas membuang yang serupa (belian bertindih ≥ 50 %): **224 setup berbeza**.
- **Boleh dibuat tanpa mengetahui tarikh laporan dengan tepat: 277 daripada 290 yang solid** (213 berbeza); 284 setup solid bergantung pada tarikh laporan kewangan akan datang.
- Ujian (B1) takrif boleh dipercayai: peraturan rawak yang lulus SOLID = 2 daripada 300 (0.7 %; perlu ≤ 5 %) → ya. Calon yang lulus: 10.6 %; anggaran bahagian nasib 6 %.
- Ujian (B2) isyarat beli menambah di atas prasyarat laporan kewangan: calon ber-prasyarat itu lulus 11.6 %; peraturan rawak dengan prasyarat yang sama lulus 2.3 % (perlu beza ≥ 10 mata) → TIDAK. **Yang solid ialah PRASYARAT itu, bukan setiap setup secara berasingan.**
- Berapa peratus lulus setiap syarat (calon · peraturan rawak · rawak + laporan kewangan): S1 90 · 92 · 63; S2 77 · 5 · 66; S3 84 · 12 · 58; S4 98 · 35 · 94; S5 80 · 5 · 59; S7 19 · 13 · 10.

## 3. Tarikh laporan kewangan: sebenar lawan diteka

- Tekaan = tarikh laporan suku sama tahun lepas + 364 hari. Daripada 71,664 laporan: 50 % diteka dalam ±2 hari dagangan, 65 % dalam ±5. Hari "1–5 hari sebelum laporan" yang sebenar ditangkap oleh tekaan: 51 %; tekaan yang betul: 75 %.
- 1,887 setup senarai utama memakai tarikh akan datang. Nilai tengah kelebihan kadar tangkap: tarikh sebenar +5.4 mata → tarikh diteka +4.2 mata; 100 % masih positif; 94 % mengekalkan sekurang-kurangnya separuh.
- Ini ujian paling keras (tanpa kalendar). Dalam dunia sebenar kebanyakan syarikat mengumumkan tarikh lebih awal, jadi keadaan sebenar berada di antara dua angka itu.

## 4. Senarai pendek: 224 setup SOLID yang berbeza (daripada 100 belian; dalam kurungan = saham rawak hari sama)

| ID | Prasyarat | Isyarat beli | Syarat saham | 5 % seminggu (rawak) | 10 % seminggu (rawak) | 10 % dua minggu (rawak) | Naik lagi hingga minggu 4 (rawak) | Tahun lebih baik | Menang % | Purata % | Rugi ≥ 8 % % | Belian | Boleh dibuat | Tarikh diteka: kelebihan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `F1674` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.009 Stochastic(14) silang naik dari bawah 10 | RS >= 70 | **33** (18) | **16** (6) | **22** (13) | **23** (11) | 12/13 | 60 | +4.1 | 23 | 444 | ya | +9.7 |
| `F421` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (benih M, parameter asal) | ADX < 20 + >= 30% di bawah puncak 52 minggu | **38** (24) | **21** (9) | **30** (19) | **23** (13) | 8/8 | 67 | +5.9 | 18 | 481 | ya | +8.5 |
| `F1255` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K13.006 Stochastic(9) silang naik dari bawah 20 | RSI14 < 40 + RS >= 70 | **32** (20) | **15** (7) | **20** (13) | **21** (11) | 13/13 | 56 | +2.1 | 28 | 545 | ya | +8.4 |
| `F1697` | <= 30% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K18.030 jatuh >= 8% dalam 20 hari | MA50 > MA200 + RSI14 < 40 | **30** (19) | **10** (5) | **17** (11) | **19** (11) | 7/9 | 53 | +0.8 | 29 | 511 | ya | +5.8 |
| `F1719` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K18.031 jatuh >= 10% dalam 20 hari | ADX > 25 | **31** (19) | **15** (6) | **21** (14) | **19** (11) | 15/16 | 59 | +2.5 | 23 | 1,063 | ya | +4.4 |
| `F1038` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.081 RSI(10) < 30 | MA50 > MA200 + MA50 naik (lawan 20 bar lalu) | **30** (17) | **11** (5) | **14** (10) | **18** (9) | 12/15 | 57 | +1.6 | 24 | 607 | ya | +9.1 |
| `F1033` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.059 RSI(5) < 20 | MA50 > MA200 | **30** (16) | **11** (4) | **16** (11) | **18** (9) | 13/16 | 56 | +1.9 | 24 | 1,190 | ya | +7.4 |
| `F200` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s4: c_kali_2=2.371, ema_a1_10=9, ema_a1_15=18, l_kali_0_99=0.99, tmax=21) | ADX < 20 + >= 30% di bawah puncak 52 minggu | **35** (22) | **18** (8) | **25** (15) | **18** (11) | 8/9 | 54 | +2.4 | 30 | 392 | ya | +4.8 |
| `F1459` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K18.030 jatuh >= 8% dalam 20 hari | RSI14 < 40 + ADX > 25 | **29** (15) | **11** (4) | **16** (10) | **18** (9) | 10/11 | 58 | +1.8 | 23 | 426 | ya | +5.9 |
| `F551` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.069 RSI(7) < 25 | MA50 > MA200 + RSI14 < 40 | **31** (17) | **10** (5) | **16** (12) | **18** (10) | 12/14 | 56 | +1.2 | 26 | 827 | ya | +7.7 |
| `F1448` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K08.018 ema20 silang atas ema100 | MACD > isyarat + ADX < 20 | **28** (13) | **9** (3) | **15** (9) | **18** (7) | 12/13 | 55 | +1.9 | 21 | 411 | ya | +6.8 |
| `F706` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.059 RSI(5) < 20 | – | **30** (17) | **11** (5) | **18** (12) | **18** (9) | 14/15 | 56 | +1.3 | 26 | 1,438 | ya | +8.1 |
| `F869` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K13.004 Stochastic(5) silang naik dari bawah 40 | tutup > MA20 + >= 30% di bawah puncak 52 minggu | **35** (23) | **17** (8) | **24** (15) | **18** (11) | 13/14 | 53 | +1.7 | 32 | 709 | ya | +7.3 |
| `F219` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K07.001 tutup silang atas sma5 | RSI14 > 50 + >= 30% di bawah puncak 52 minggu | **37** (23) | **21** (9) | **24** (16) | **18** (10) | 8/11 | 50 | +1.1 | 33 | 535 | ya | +8.1 |
| `F544` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.009 RSI(2) < 15 | RS >= 70 | **27** (17) | **12** (5) | **18** (12) | **18** (10) | 14/16 | 54 | +2.2 | 25 | 1,141 | ya | +6.1 |
| `F1285` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K04.006 masuk semula atas jalur bawah BB(20, 2.5) | MA50 naik (lawan 20 bar lalu) + RSI14 < 40 | **29** (15) | **12** (4) | **16** (10) | **18** (8) | 14/15 | 60 | +3.2 | 18 | 439 | ya | +10.7 |
| `F89` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu + hari naik (tutup > buka) | **34** (21) | **17** (8) | **23** (14) | **17** (10) | 7/9 | 53 | +2.2 | 30 | 383 | ya | +6.4 |
| `F1266` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.070 RSI(7) < 25 + atas MA200 | – | **31** (17) | **11** (5) | **14** (11) | **17** (10) | 12/14 | 55 | +1.5 | 24 | 628 | ya | +6.9 |
| `F610` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.695, henti_atr=3.886, stoch_k_13=6, stoch_k_21=30, stoch_k_d_8=11, tmax=26) | ADX < 20 + tutup dalam 25% teratas julat hari | **29** (18) | **13** (5) | **18** (11) | **17** (10) | 11/13 | 53 | +1.6 | 22 | 479 | ya | +4.8 |
| `F254` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K02.007 RSI(5) silang atas 60 | MACD > isyarat + >= 30% di bawah puncak 52 minggu | **37** (22) | **21** (8) | **26** (17) | **17** (10) | 13/14 | 54 | +2.4 | 30 | 716 | ya | +5.8 |
| `F114` | earnings dalam 1-5 sesi akan datang | K13.012 Stochastic(14) silang naik dari bawah 40 | RS >= 90 + dalam 15% dari puncak 52 minggu | **29** (17) | **15** (6) | **19** (11) | **17** (9) | 17/17 | 51 | +1.2 | 30 | 640 | ya | +5.3 |
| `F90` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M50 Elder Triple Screen | MACD > isyarat + >= 30% di bawah puncak 52 minggu | **37** (23) | **21** (9) | **26** (16) | **17** (10) | 7/8 | 48 | +0.8 | 33 | 303 | ya | +5.7 |
| `F1553` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K08.018 ema20 silang atas ema100 | tutup > MA20 + tutup > MA200 | **25** (13) | **8** (4) | **15** (9) | **17** (8) | 8/10 | 56 | +1.6 | 23 | 389 | ya | +7.1 |
| `F1030` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.005 RSI(2) < 8 | MA50 > MA200 + ADX < 20 | **26** (15) | **10** (4) | **17** (11) | **17** (9) | 14/15 | 60 | +2.8 | 19 | 762 | ya | +6.7 |
| `F571` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.028 tutup < jalur bawah BB(20, 2.0) | – | **27** (16) | **11** (5) | **16** (11) | **17** (9) | 16/17 | 55 | +1.7 | 26 | 1,898 | ya | +6.5 |
| `F912` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.695, henti_atr=3.886, stoch_k_13=6, stoch_k_21=30, stoch_k_d_8=11, tmax=26) | ADX < 20 | **29** (17) | **12** (5) | **17** (12) | **17** (9) | 13/15 | 54 | +1.7 | 22 | 996 | ya | +6.4 |
| `F771` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K24.003 bar pembalikan (buka <= 10%, tutup >= 90% julat) | MACD > isyarat + volum 10 hari > volum 50 hari | **25** (15) | **9** (4) | **14** (10) | **17** (9) | 8/10 | 61 | +2.7 | 18 | 356 | ya | +9.9 |
| `F1592` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.089 RSI(14) < 35 | MA50 > MA200 + RSI14 < 40 | **28** (16) | **11** (5) | **15** (11) | **17** (9) | 13/16 | 56 | +1.6 | 25 | 926 | ya | +5.7 |
| `F178` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | N29 PSAR naik + tutup>MA50 (benih N) | ADX < 20 + >= 30% di bawah puncak 52 minggu | **35** (19) | **18** (7) | **22** (13) | **17** (10) | 12/13 | 52 | +1.6 | 33 | 696 | ya | +5.8 |
| `F1288` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.027 tutup < jalur bawah BB(20, 1.5) + RSI14 < 40 | MA50 > MA200 | **28** (15) | **12** (4) | **16** (11) | **17** (9) | 15/17 | 57 | +2.2 | 24 | 1,446 | ya | +6.2 |
| `F2001` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M79 Radge: 20% Flipper (benih M, varian 1: a=0.18) | RSI14 > 60 + MACD > isyarat | **28** (14) | **9** (4) | **17** (10) | **17** (7) | 11/11 | 51 | +1.0 | 24 | 488 | ya | +6.2 |
| `F203` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.005 4 tutup menurun berturut | ADX < 20 | **26** (15) | **11** (4) | **18** (11) | **17** (9) | 14/16 | 57 | +2.5 | 22 | 1,204 | ya | +8.1 |
| `F971` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K02.033 RSI(21) silang atas 40 | volum 10 hari > volum 50 hari | **27** (17) | **10** (5) | **16** (12) | **17** (9) | 11/14 | 60 | +2.5 | 22 | 622 | ya | +5.5 |
| `F1048` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M15 Break & Retest + Henti ATR (benih M, varian 2: atrw_14=21, h_kali_0_382=0.452, rolling_20=20) | ADX < 20 + tutup dalam 25% teratas julat hari | **29** (17) | **12** (6) | **17** (12) | **17** (9) | 12/14 | 57 | +2.3 | 21 | 790 | ya | +5.3 |
| `F479` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | – | **27** (17) | **11** (5) | **16** (11) | **17** (10) | 14/17 | 56 | +1.8 | 24 | 2,027 | ya | +6.9 |
| `F879` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.071 RSI(7) < 30 | MA20 > MA50 + MA50 > MA200 | **28** (16) | **11** (4) | **17** (11) | **17** (9) | 13/16 | 57 | +1.9 | 24 | 960 | ya | +4.8 |
| `F694` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.043 RSI(4) < 20 | – | **27** (16) | **11** (5) | **17** (12) | **17** (9) | 15/17 | 57 | +2.2 | 24 | 2,443 | ya | +6.5 |
| `F156` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | ADX < 20 | **26** (16) | **10** (4) | **16** (11) | **17** (9) | 12/15 | 59 | +2.2 | 23 | 831 | ya | +7.4 |
| `F493` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K22.002 Holy Grail (ADX > 20, undur EMA20) | ADX > 25 + squeeze hidup | **28** (16) | **13** (5) | **17** (10) | **17** (9) | 12/14 | 56 | +2.1 | 20 | 494 | ya | +4.5 |
| `F1589` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.009 Stochastic(14) silang naik dari bawah 10 | MA50 > MA200 | **26** (16) | **12** (5) | **17** (11) | **17** (9) | 16/17 | 57 | +2.6 | 21 | 1,235 | ya | +7.0 |
| `F110` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI (benih M, varian 3: l_kali_0_99=0.805, rolling_20=33, rsi_14=28, sd_kali_2=1.748) | tutup dalam 25% teratas julat hari | **26** (16) | **11** (5) | **15** (11) | **17** (9) | 8/9 | 58 | +1.7 | 24 | 308 | ya | +6.8 |
| `F363` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.005 4 tutup menurun berturut | – | **27** (16) | **11** (5) | **18** (11) | **17** (9) | 14/17 | 56 | +2.1 | 23 | 2,769 | ya | +6.8 |
| `F564` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K09.004 MACD(8,17,9) silang naik | ADX < 20 + >= 30% di bawah puncak 52 minggu | **37** (20) | **18** (7) | **21** (13) | **16** (9) | 13/13 | 47 | +0.5 | 35 | 578 | ya | +6.1 |
| `F940` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K21.007 NR10 | MACD > isyarat + ADX < 20 | **28** (15) | **11** (4) | **16** (10) | **16** (8) | 14/16 | 59 | +2.3 | 20 | 986 | ya | +7.6 |
| `F289` | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang | K02.034 RSI(21) silang atas 50 | RS >= 90 + dalam 15% dari puncak 52 minggu | **28** (16) | **15** (5) | **20** (11) | **16** (8) | 10/11 | 50 | +1.2 | 30 | 348 | ya | +8.1 |
| `F621` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.695, henti_atr=3.886, stoch_k_13=6, stoch_k_21=30, stoch_k_d_8=11, tmax=26) | Supertrend naik + >= 30% di bawah puncak 52 minggu | **33** (18) | **20** (6) | **23** (11) | **16** (8) | 11/12 | 47 | +0.5 | 33 | 348 | ya | +4.8 |
| `F111` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K17.031 undur ke ema50 yang naik (tol 1.0%) | >= 30% di bawah puncak 52 minggu + hari naik (tutup > buka) | **31** (19) | **15** (7) | **17** (12) | **16** (9) | 7/9 | 49 | +0.4 | 35 | 330 | ya | +5.6 |
| `F756` | earnings dalam 1-5 sesi akan datang | M19 Sneaky Pivot (proksi harian) (benih M, varian 1: l_kali_0_99=0.497, rolling_20=40, shift_2=4, shift_3=2, tmax=20) | MA50 > MA200 + tutup dalam 25% teratas julat hari | **24** (14) | **9** (4) | **13** (9) | **16** (8) | 12/13 | 56 | +1.7 | 22 | 381 | ya | +5.8 |
| `F1124` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.021 RSI(3) < 8 | MA20 > MA50 + RSI14 < 40 | **27** (16) | **9** (5) | **12** (9) | **16** (9) | 10/11 | 52 | +0.3 | 25 | 425 | ya | +6.9 |
| `F1050` | nisbah 4% (10 hari) > 2 + earnings dalam 1-5 sesi akan datang | M79 Radge: 20% Flipper (benih M, parameter asal) | MACD > isyarat + MACD > 0 | **28** (12) | **10** (3) | **18** (9) | **16** (7) | 11/11 | 55 | +1.6 | 19 | 345 | ya | +8.7 |
| `F505` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K09.005 MACD(8,17,9) silang naik bawah sifar | – | **29** (16) | **12** (5) | **18** (12) | **16** (8) | 12/13 | 55 | +1.9 | 24 | 1,081 | ya | +5.1 |
| `F1512` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.028 RSI(3) < 20 + atas MA200 | MACD > 0 + ADX < 20 | **24** (14) | **9** (3) | **14** (9) | **16** (8) | 10/11 | 62 | +2.8 | 17 | 372 | ya | +4.2 |
| `F829` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.093 RSI(14) < 45 | Supertrend naik + dalam 15% dari puncak 52 minggu | **25** (13) | **8** (3) | **11** (8) | **16** (8) | 9/11 | 58 | +2.5 | 16 | 385 | ya | +4.4 |
| `F1042` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.057 RSI(5) < 15 | – | **27** (16) | **9** (4) | **14** (10) | **16** (9) | 13/15 | 54 | +0.8 | 24 | 808 | ya | +5.2 |
| `F1653` | 7 hari pertama bulan + earnings dalam 1-5 sesi akan datang | K01.039 RSI(4) < 10 | MA20 > MA50 | **24** (16) | **8** (5) | **14** (10) | **16** (9) | 12/13 | 52 | +0.2 | 28 | 371 | ya | +7.2 |
| `F1174` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K11.004 Supertrend(7, 3.0) bertukar naik | Supertrend naik + hari naik (tutup > buka) | **27** (16) | **10** (4) | **14** (11) | **16** (8) | 12/12 | 59 | +1.7 | 23 | 1,080 | ya | +6.5 |
| `F691` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M124 'Last' Stochastic Technique (ChartSchool) (benih M, varian 2: henti_atr=1.526, keluar_chan=1.891, keluar_chan_atr=38, keluar_chan_tinggi=30, stoch_k_39=36, stoch_k_d_3=2) | tutup > MA20 + hari naik (tutup > buka) | **27** (15) | **9** (4) | **16** (11) | **16** (9) | 14/15 | 57 | +2.0 | 21 | 1,157 | ya | +5.7 |
| `F1943` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | K18.002 jatuh >= 8% dalam 2 hari | Supertrend naik + RS >= 70 | **31** (23) | **17** (9) | **25** (16) | **16** (11) | 9/11 | 49 | +1.9 | 34 | 640 | ya | tidak berkenaan |
| `F103` | earnings dalam 1-5 sesi akan datang | M89 Chande 65sma-3cc (benih M, parameter asal) | MACD > isyarat + volum 10 hari > volum 50 hari | **27** (12) | **12** (3) | **17** (8) | **16** (7) | 15/17 | 57 | +1.9 | 20 | 602 | ya | +6.9 |
| `F1539` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.006 Stochastic(9) silang naik dari bawah 20 | MA50 > MA200 + RSI14 < 40 | **27** (17) | **12** (5) | **17** (11) | **16** (9) | 16/17 | 57 | +2.4 | 21 | 1,122 | ya | +6.0 |
| … | 164 lagi dalam `solid.csv.gz` | | | | | | | | | | | | | |

## 5. Setup SOLID lain yang serupa dengan wakil di atas: 66

Senarai penuh dalam `solid.csv.gz` (lajur `serupa_dengan`).

## 6. "Prasyarat sahaja" (tanpa isyarat beli; rujukan)

| Prasyarat | 5 % seminggu (rawak) | 10 % seminggu (rawak) | 10 % dua minggu (rawak) | Naik lagi hingga minggu 4 (rawak) | Kelebihan (mata) | Tahun lebih baik | Belian | Lulus S1–S5 |
|---|---|---|---|---|---|---|---|---|
| breadth thrust Zweig aktif (20 sesi) + earnings dalam 1-5 sesi akan datang | 25 (15) | 10 (4) | 17 (11) | 16 (9) | +7.3 | 14/14 | 6,133 | ya |
| distribution day QQQ <= 2 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | 24 (11) | 10 (3) | 12 (7) | 12 (6) | +6.8 | 12/13 | 4,495 | ya |
| nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | 27 (17) | 11 (5) | 17 (12) | 16 (10) | +6.3 | 17/17 | 7,069 | ya |
| Januari + earnings dalam 1-5 sesi akan datang | 23 (13) | 9 (3) | 13 (8) | 13 (7) | +6.2 | 17/17 | 5,539 | ya |
| rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | 23 (12) | 9 (3) | 13 (9) | 13 (6) | +6.2 | 17/17 | 15,718 | ya |
| rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | 24 (13) | 10 (4) | 13 (8) | 13 (7) | +6.1 | 17/17 | 13,227 | ya |
| QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | 24 (14) | 10 (4) | 15 (10) | 13 (7) | +6.0 | 17/17 | 16,271 | ya |
| keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | 24 (13) | 10 (4) | 14 (9) | 13 (7) | +6.0 | 17/17 | 19,888 | ya |
| <= 30% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | 31 (22) | 14 (7) | 19 (13) | 19 (13) | +6.0 | 15/15 | 6,876 | ya |
| follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | 26 (17) | 12 (5) | 17 (12) | 15 (9) | +5.9 | 15/15 | 12,138 | ya |
| nisbah 4% (10 hari) > 2 + earnings dalam 1-5 sesi akan datang | 24 (13) | 10 (3) | 14 (9) | 12 (7) | +5.9 | 17/17 | 11,946 | ya |
| turun-naik SPY 21 hari >= 25% setahun + earnings dalam 1-5 sesi akan datang | 29 (21) | 15 (7) | 21 (15) | 18 (12) | +5.9 | 8/8 | 4,233 | TIDAK |
| hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | 25 (15) | 11 (5) | 15 (10) | 14 (9) | +5.9 | 15/15 | 15,390 | ya |
| SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | 30 (21) | 14 (7) | 20 (14) | 17 (12) | +5.8 | 13/13 | 9,024 | ya |
| QQQ ON + earnings dalam 1-5 sesi akan datang | 23 (12) | 10 (3) | 13 (8) | 12 (6) | +5.8 | 17/17 | 34,049 | ya |

## 7. Kaveat

- Senarai utama sudah dipilih dengan saham yang sama, jadi "solid" bermaksud "paling tahan uji dalam backtest", BUKAN bukti.
- Semua ambang ditetapkan oleh Claude sebelum hasil dilihat. Tiada saham delist. Tiada tapisan Shariah (arahan pengguna).
- "Boleh dibuat" diukur dengan tekaan tarikh yang kasar; kalendar sebenar lebih tepat.
- Registry, kohort dan susunan senarai utama tidak diubah. Bukti hanya datang daripada papertrade (keputusan pengguna).
