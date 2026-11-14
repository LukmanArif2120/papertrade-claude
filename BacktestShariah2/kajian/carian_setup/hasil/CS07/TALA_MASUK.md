# CS07 (a): tala parameter masuk SEMUA kaedah (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_tala7.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(a), dikomit sebelum dijalankan. **Jangan sunting secara manual.**

## 1. Apa yang dicuba

- Kaedah M: 1,072 varian rawak julat penuh (8 setiap kaedah, 134 kaedah) + 400 varian setempat ±25 % di sekitar varian terbaik 50 kaedah teratas; 1,367 cukup isyarat untuk diskor.
- Indikator dan kaedah N: 25 keluarga berparameter, 656 varian grid penuh; 649 cukup isyarat. 41 takrif asal (`P`/`N`) ada dalam keluarga sebagai induk.
- Bersama 500 pencetus sedia ada, setiap satu diskor atas 544 gabungan prasyarat × 379 gabungan penapis saham pada kumpulan A. Sasaran: kadar **"naik lagi"** (naik ≥ 5 % minggu pertama DAN naik lagi hingga minggu ke-4 tanpa kena henti −8 %) lawan saham rawak hari sama.

## 2. Bacaan dikunci: adakah tala menolong pada saham yang tidak dilihat?

- Induk yang ditala: 156 (131 kaedah M, 25 keluarga indikator). Anak berbeza daripada ibu pada kumpulan A: 135 daripada 151 (selebihnya, takrif asal sudah yang terbaik).
- Pada kumpulan B, anak mengatasi ibu (kelebihan "naik lagi"): **83 daripada 135** pasangan; median beza +0.35 mata; dalam 2025–26 (K3) median beza +0.10 mata (69 daripada 135).
- **Keputusan: tala MENOLONG** mengikut bacaan yang dikunci (lebih separuh pasangan DAN median beza K3 > 0).

## 3. 20 pencetus teratas ikut skor A, dinilai pada kumpulan B

| | Bilangan varian baharu | Purata skor A (mata) | Purata "naik lagi" B % | Purata kelebihan B (mata) | Purata kelebihan 2025–26 | Bertahan K1, K2 DAN K3 |
|---|---|---|---|---|---|---|
| Tanpa varian baharu | 0 | +6.63 | 14.0 | +6.87 | +4.88 | 13 daripada 20 |
| Dengan varian baharu | 17 | +7.32 | 14.7 | +6.43 | +5.85 | 13 daripada 20 |

## 4. Papan masuk baharu CS07 (12 setup; maks 2 setiap induk, 3 setiap pasangan prasyarat)

| ID | Pencetus (parameter) | Prasyarat | Penapis saham | Skor A (mata) | Belian B | Naik lagi B % (rawak) | Kelebihan K1 / K2 / K3 | Dipercayai |
|---|---|---|---|---|---|---|---|---|
| `C01` | M03 BB Break + Divergence RSI (benih M, varian 3: l_kali_0_99=0.805, rolling_20=33, rsi_14=28, sd_kali_2=1.748) | QA11 QQQ naik >= 3% dalam 5 sesi DAN QF01 earnings dalam 1-5 sesi akan datang | tiada | +8.15 | 461 | 16.1 (9.6) | +9.9 / +4.2 / +6.1 | **ya** |
| `C02` | M50 Elder Triple Screen (benih M, varian 0s6: ewm_span_12=13, ewm_span_2=2, ewm_span_26=23, ewm_span_9=8, rolling_50=54) | QA08 rejim ON baharu (<= 10 sesi) DAN QF01 earnings dalam 1-5 sesi akan datang | F11 MACD > isyarat DAN F20 >= 30% di bawah puncak 52 minggu | +8.11 | 288 | 16.7 (9.9) | +11.1 / -0.5 / +15.5 | tidak |
| `C03` | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s1: c_kali_2=2.002, ema_a1_10=9, ema_a1_15=15, l_kali_0_99=0.981, tmax=17) | QA05 QQQ dalam 3% dari puncak 52 minggu DAN QF01 earnings dalam 1-5 sesi akan datang | F20 >= 30% di bawah puncak 52 minggu DAN F30 hari naik (tutup > buka) | +8.06 | 383 | 17.5 (10.2) | +6.5 / +7.6 / +7.7 | **ya** |
| `C04` | M50 Elder Triple Screen (benih M, varian 0s7: ewm_span_12=11, ewm_span_2=2, ewm_span_26=22, ewm_span_9=7, rolling_50=51) | QA08 rejim ON baharu (<= 10 sesi) DAN QF01 earnings dalam 1-5 sesi akan datang | F11 MACD > isyarat DAN F20 >= 30% di bawah puncak 52 minggu | +7.85 | 303 | 17.2 (10.0) | +10.4 / +0.9 / +15.2 | **ya** |
| `C05` | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s4: c_kali_2=2.371, ema_a1_10=9, ema_a1_15=18, l_kali_0_99=0.99, tmax=21) | QA05 QQQ dalam 3% dari puncak 52 minggu DAN QF01 earnings dalam 1-5 sesi akan datang | F20 >= 30% di bawah puncak 52 minggu | +7.73 | 366 | 18.0 (10.2) | +6.8 / +8.2 / +8.4 | **ya** |
| `C06` | M03 BB Break + Divergence RSI (benih M, varian 3s1: l_kali_0_99=0.83, rolling_20=40, rsi_14=28, sd_kali_2=1.734) | QA11 QQQ naik >= 3% dalam 5 sesi DAN QF01 earnings dalam 1-5 sesi akan datang | tiada | +7.56 | 377 | 15.9 (9.8) | +7.0 / +5.1 / +9.9 | **ya** |
| `C07` | K17.047 undur ke ema100 yang naik (tol 2.0%) | QC03 keluasan naik >= 10 mata dalam 10 sesi DAN QF01 earnings dalam 1-5 sesi akan datang | F14 ADX < 20 DAN F16 RS >= 70 | +7.41 | 360 | 15.0 (8.8) | +4.4 / +9.3 / -1.9 | tidak |
| `C08` | M02 MACD + SMA200 (benih M, varian 1s1: ewm_span_12=16, ewm_span_9=6, r=3.585, rolling_200=209, s200_kali_0_99=0.495, tmax=10) | QC03 keluasan naik >= 10 mata dalam 10 sesi DAN QF01 earnings dalam 1-5 sesi akan datang | F03 tutup > MA200 DAN F06 MA50 naik (lawan 20 bar lalu) | +7.26 | 363 | 12.9 (6.6) | +5.5 / +7.3 / +7.8 | **ya** |
| `C09` | K11.016 Supertrend(20, 1.5) bertukar naik | QH08 QQQ SMA10 > SMA20 DAN QF01 earnings dalam 1-5 sesi akan datang | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +7.16 | 380 | 10.0 (7.1) | +3.0 / +2.1 / +4.6 | **ya** |
| `C10` | K19.011 pecah atas Keltner(30, 1.0) | QC01 >= 60% saham di atas MA50 DAN QF01 earnings dalam 1-5 sesi akan datang | F09 RSI14 > 60 DAN F17 RS >= 90 | +7.11 | 330 | 13.6 (7.5) | +4.8 / +8.1 / +6.8 | **ya** |
| `C11` | M124 'Last' Stochastic Technique (ChartSchool) (benih M, varian 8s2: henti_atr=1.577, keluar_chan=4.5, keluar_chan_atr=25, keluar_chan_tinggi=17, stoch_k_39=45, stoch_k_d_3=3) | QH07 regangan turun-naik SPY (proksi VIX) + SPY > SMA200 DAN QF01 earnings dalam 1-5 sesi akan datang | F11 MACD > isyarat DAN F22 volum 10 hari > volum 50 hari | +7.02 | 349 | 14.0 (7.3) | +10.3 / +2.8 / -6.3 | tidak |
| `C12` | K17.048 undur ke ema100 yang naik (tol 2.0%) + atas MA200 | QC03 keluasan naik >= 10 mata dalam 10 sesi DAN QF01 earnings dalam 1-5 sesi akan datang | F14 ADX < 20 DAN F16 RS >= 70 | +7.02 | 355 | 14.6 (8.7) | +4.5 / +8.3 / -1.6 | tidak |

## 5. Setiap keluarga indikator: takrif asal lawan parameter terbaik

| Keluarga | Varian | Ibu (takrif asal terbaik) | Skor A ibu | Anak (parameter terbaik) | Skor A anak | Kelebihan B: ibu → anak | 2025–26: ibu → anak |
|---|---|---|---|---|---|---|---|
| `K01` | 92 | K01.007 RSI(2) < 10 | +5.56 | K01.003 RSI(2) < 5 | +5.96 | +7.6 → +7.2 | +12.6 → +2.6 |
| `K02` | 35 | K02.028 RSI(14) silang atas 60 | +5.48 | K02.014 RSI(7) silang atas 60 | +5.93 | +5.8 → +5.3 | +4.5 → +5.9 |
| `K03` | 57 | K03.028 tutup < jalur bawah BB(20, 2.0) | +4.95 | K03.030 tutup < jalur bawah BB(20, 2.0) + RSI14 < 40 | +5.19 | +7.5 → +7.0 | +7.1 → +4.8 |
| `K04` | 9 | – (keluarga baharu) | – | K04.008 masuk semula atas jalur bawah BB(30, 2.0) | +4.96 | – → +5.7 | – → +1.3 |
| `K05` | 15 | K05.006 tutup silang atas jalur atas BB(20, 2.0) | +3.82 | K05.009 tutup silang atas jalur atas BB(30, 1.5) | +5.60 | +5.3 → +7.7 | +9.6 → +25.1 |
| `K06` | 12 | K06.003 3 tutup menurun berturut | +5.63 | K06.001 2 tutup menurun berturut | +5.99 | +7.0 → +5.1 | +4.5 → +2.8 |
| `K07` | 20 | K07.013 tutup silang atas sma50 | +6.23 | K07.007 tutup silang atas sma15 | +6.25 | +7.0 → +5.1 | +5.3 → +6.7 |
| `K08` | 26 | K08.013 sma10 silang atas sma50 | +5.46 | K08.004 ema5 silang atas ema10 | +6.28 | +6.2 → +5.2 | +10.7 → +1.5 |
| `K09` | 24 | K09.002 MACD(12,26,9) silang naik bawah sifar | +6.28 | K09.007 MACD(5,35,5) silang naik | +6.29 | +7.7 → +5.0 | +8.1 → +2.5 |
| `K10` | 40 | K10.009 pecah tinggi 20 hari | +5.37 | K10.001 pecah tinggi 5 hari | +6.34 | +7.9 → +7.3 | +14.9 → +12.9 |
| `K11` | 20 | K11.009 Supertrend(10, 3.0) bertukar naik | +4.41 | K11.016 Supertrend(20, 1.5) bertukar naik | +7.16 | +4.1 → +2.9 | +6.7 → +4.6 |
| `K12` | 20 | K12.013 ADX(14) silang atas 25 & +DI > -DI | +4.32 | K12.007 ADX(10) silang atas 20 & +DI > -DI | +5.22 | +4.4 → +4.9 | +1.0 → +4.5 |
| `K13` | 16 | K13.010 Stochastic(14) silang naik dari bawah 20 | +5.47 | K13.012 Stochastic(14) silang naik dari bawah 40 | +6.82 | +8.3 → +8.5 | +5.3 → +12.4 |
| `K14` | 42 | K14.022 lonjakan >= 4.0% + volum 2.0x + tutup 25 % teratas | +2.26 | K14.003 lonjakan >= 0.0% + volum 2.0x | +5.01 | +2.6 → +5.9 | +4.5 → +3.5 |
| `K15` | 24 | K15.016 gap >= 8.0% + volum 3.0x | -0.73 | K15.005 gap >= 3.0% | +4.56 | +2.1 → +1.5 | -1.1 → +3.5 |
| `K16` | 20 | K16.010 gap-and-go (buka > tinggi semalam + 2.0%) + volum 1.5x | +1.96 | K16.009 gap-and-go (buka > tinggi semalam + 2.0%) | +5.41 | +0.8 → +1.9 | -0.4 → -1.7 |
| `K17` | 48 | K17.030 undur ke sma50 yang naik (tol 1.0%) + atas MA200 | +5.44 | K17.047 undur ke ema100 yang naik (tol 2.0%) | +7.41 | +4.8 → +6.2 | +0.5 → -1.9 |
| `K18` | 35 | – (keluarga baharu) | – | K18.023 jatuh >= 8% dalam 10 hari | +4.90 | – → +4.9 | – → +1.6 |
| `K19` | 15 | K19.008 pecah atas Keltner(20, 2.0) | +4.32 | K19.011 pecah atas Keltner(30, 1.0) | +7.11 | +5.0 → +6.1 | +11.0 → +6.8 |
| `K20` | 9 | K20.005 squeeze lepas ke atas (BB 2.0, KC 1.5) | +3.72 | K20.002 squeeze lepas ke atas (BB 1.5, KC 1.5) | +5.19 | +5.3 → +6.2 | +5.8 → +8.6 |
| `K21` | 10 | K21.006 NR7 + hari dalam | +5.01 | K21.004 NR5 + hari dalam | +5.83 | +3.9 → +4.4 | +2.7 → +4.4 |
| `K22` | 15 | K22.008 Holy Grail (ADX > 30, undur EMA20) | +2.57 | K22.002 Holy Grail (ADX > 20, undur EMA20) | +5.42 | +5.4 → +7.0 | +3.4 → +3.5 |
| `K23` | 5 | K23.004 RS silang atas 90 | +7.01 | K23.004 RS silang atas 90 | +7.01 | +5.3 → +5.3 | +2.7 → +2.7 |
| `K24` | 9 | K24.005 bar pembalikan (buka <= 20%, tutup >= 80% julat) | +6.21 | K24.007 bar pembalikan (buka <= 30%, tutup >= 70% julat) | +6.22 | +5.7 → +6.0 | +3.3 → +11.7 |
| `K25` | 31 | K25.032 pecah julat sempit 60 hari (<= 35%) + volum 1.5x | +1.82 | K25.007 pecah julat sempit 10 hari (<= 35%) | +5.95 | +3.2 → +7.6 | +8.7 → +14.9 |

## 6. Kaedah M: 30 teratas ikut skor A anak (kesemua 131 dalam `tala_masuk.csv`)

| Kaedah | Varian | Skor A: parameter asal → anak | Anak | Kelebihan B: asal → anak | 2025–26: asal → anak |
|---|---|---|---|---|---|
| `M03` | 19 | +5.36 → +8.15 | M03 BB Break + Divergence RSI (benih M, varian 3: l_kali_0_99=0.805, rolling_20=33, rsi_14=28, sd_kali_2=1.748) | +6.0 → +6.5 | +11.6 → +6.1 |
| `M50` | 19 | +7.69 → +8.11 | M50 Elder Triple Screen (benih M, varian 0s6: ewm_span_12=13, ewm_span_2=2, ewm_span_26=23, ewm_span_9=8, rolling_50=54) | +6.3 → +6.8 | +12.7 → +15.5 |
| `M20` | 19 | +6.85 → +8.06 | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s1: c_kali_2=2.002, ema_a1_10=9, ema_a1_15=15, l_kali_0_99=0.981, tmax=17) | +7.0 → +7.3 | +7.6 → +7.7 |
| `M02` | 19 | +6.57 → +7.26 | M02 MACD + SMA200 (benih M, varian 1s1: ewm_span_12=16, ewm_span_9=6, r=3.585, rolling_200=209, s200_kali_0_99=0.495, tmax=10) | +7.7 → +6.4 | +9.9 → +7.8 |
| `M124` | 19 | +6.20 → +7.02 | M124 'Last' Stochastic Technique (ChartSchool) (benih M, varian 8s2: henti_atr=1.577, keluar_chan=4.5, keluar_chan_atr=25, keluar_chan_tinggi=17, stoch_k_39=45, stoch_k_d_3=3) | +8.9 → +6.7 | -6.0 → -6.3 |
| `M19` | 19 | +2.85 → +6.96 | M19 Sneaky Pivot (proksi harian) (benih M, varian 3s4: l_kali_0_99=0.661, rolling_20=33, shift_2=4, shift_3=6, tmax=29) | +6.1 → +5.0 | +1.8 → +8.0 |
| `M27` | 19 | +5.13 → +6.96 | M27 Price Action 4 Tiang (benih M, varian 9: a14_kali_0_5=0.638, atr_14=26, np_ambang_2=1, pivot_k_3=2, rolling_20=32, rolling_50=70) | +2.5 → +5.3 | -0.5 → +2.6 |
| `M155` | 19 | +5.04 → +6.94 | M155 Market Cycle Strategy (benih M, varian 9: had_henti=0.824, henti_atr=3.514, stoch_k_13=17, stoch_k_21=39, stoch_k_d_8=8, tmax=28) | +5.5 → +10.5 | +7.9 → +10.9 |
| `M159` | 19 | +6.84 → +6.88 | M159 Heikin-Ashi Trend (benih M, varian 0s5: had_henti=0.877, henti_pct=18.569, hh_kali_0_1=0.095, keluar_sma=18, shift_5=5, tmax=11) | +5.9 → +5.9 | -3.8 → -3.8 |
| `M105` | 19 | +4.56 → +6.76 | M105 Supertrend tulen (benih M, varian 9s3: close_kali_0_88=0.44, m=3.474, n=15) | +4.0 → +10.6 | +5.6 → -1.9 |
| `M89` | 17 | +6.57 → +6.72 | M89 Chande 65sma-3cc (benih M, varian 1: rma_atr_14=13, rma_atr_kali_2=1.684, rolling_14=9, rolling_65=109, shift_10=9, shift_3=6) | +9.2 → +8.8 | +1.7 → +5.6 |
| `M14` | 19 | +5.53 → +6.64 | M14 Walking with the Whales (benih M, varian 1s7: rolling_50=57, shift_2=4) | +6.9 → +7.3 | +5.4 → +3.7 |
| `M31` | 18 | +3.58 → +6.58 | M31 Band Walk (BB 20/2) (benih M, varian 10s8: rolling_10=9, rolling_20=37, sd_kali_2=1.475, shift_5=10) | +5.2 → +5.1 | +3.9 → +4.2 |
| `M125` | 19 | +6.51 → +6.51 | (parameter asal kekal terbaik) | +5.8 → +5.8 | -3.6 → -3.6 |
| `M106` | 13 | +3.36 → +6.45 | M106 DMI Wilder (benih M, varian 3s1: a14_kali_2=1.197, adx_ambang_25=35, adx_kali_13=14.367, dmi_14=9) | +2.9 → +7.1 | +0.7 → +6.8 |
| `M52` | 19 | +5.12 → +6.26 | M52 Radge Weekend Trend Trader (benih M, varian 10s2: bo_kali_0_6=0.576, c_kali_0_6=0.474, roc_ambang_0_3=0.272, rolling_10=16, rolling_20=20, rolling_50=41) | +4.9 → +5.8 | +3.9 → +8.6 |
| `M35` | 10 | +5.78 → +6.21 | M35 Pocket Pivot Morales & Kacher (benih M, varian 0s7: rolling_10=9, rolling_200=211, rolling_50=53, s10_kali_1_02=1.047) | +5.0 → +5.1 | +5.9 → +5.0 |
| `M161` | 19 | +6.09 → +6.21 | M161 EMA 10/21 + Supertrend (10,3) (benih M, varian 0s1: ema_21=20, had_henti=0.99, henti_pct=11.47, rolling_10=8, rolling_5=5, supertrend_hijau_10=11) | +6.5 → +6.3 | +19.4 → +13.4 |
| `M13` | 19 | +6.12 → +6.12 | (parameter asal kekal terbaik) | +3.8 → +3.8 | +1.6 → +1.6 |
| `M73` | 19 | +4.46 → +6.11 | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (benih M, varian 4s5: adx_5=5, adx_ambang_40=23, rolling_5=5) | +6.2 → +5.3 | +6.5 → +4.7 |
| `M18` | 19 | +4.80 → +6.10 | M18 EMA9/21 Pullback (benih M, varian 1s5: ema_a1_21=36, ema_a1_9=16, rr_ambang_2=3) | +6.3 → +4.0 | +7.7 → -0.2 |
| `M118` | 19 | +5.32 → +6.10 | M118 Expansion Pivot (Cooper) (benih M, varian 3s5: had_henti=0.503, henti_low=8, keluar_sma=61, rolling_9=4, sma_50=38) | +4.3 → +6.3 | +1.3 → +9.7 |
| `M79` | 19 | +4.31 → +6.08 | M79 Radge: 20% Flipper (benih M, varian 2s6: a=0.113) | +9.6 → +4.1 | +7.9 → +1.3 |
| `M32` | 19 | +1.88 → +6.02 | M32 Momentum Burst (benih M, varian 4s2: h_kali_0_8=0.615, r_ambang_0_02=0.01, r_ambang_0_04=0.027, rolling_20=15, rolling_3=6, rolling_50=26) | +1.6 → +4.1 | -0.4 → +0.8 |
| `M39` | 19 | +3.57 → +5.99 | M39 Radge Pecahan Bollinger 100 hari (benih M, varian 1s4: c_kali_0_85=0.531, sd_kali_2=1.227) | +3.2 → +6.2 | +3.1 → +6.9 |
| `M102` | 19 | +4.47 → +5.98 | M102 Stockbee SLTB (benih M, varian 7s2: r_ambang_0_02=0.026, rolling_3=5, rolling_50=49, rolling_65=81, rolling_7=4, ti65_ambang_1_05=0.926) | +6.3 → +7.1 | +20.5 → -4.6 |
| `M78` | 19 | +4.42 → +5.79 | M78 Alvarez Pecahan Mingguan DTAYS (benih M, varian 5s2: dv21_ambang_15000000_0=11664236.123, k_atr=5, open_kali_0_92=0.46, r20_ambang_0_3=0.203, rolling_19=17, rolling_21=30) | +6.0 → +6.0 | +7.5 → +7.1 |
| `M12` | 19 | +4.31 → +5.79 | M12 Parabolic SAR (benih M, varian 7s1: psar_a0_0_02=0.023, psar_amax_0_2=0.3, psar_da_0_02=0.012, rolling_50=38) | +5.8 → +3.9 | +2.1 → +4.1 |
| `M137` | 19 | +3.62 → +5.75 | M137 Livermore System (benih M, varian 2s3: a_kali_4=2.219, atr_kali_6=3.234, henti_atr=2.47, keluar_chan=2.88, keluar_chan_atr=25, keluar_chan_tinggi=35) | +4.5 → +5.5 | +9.1 → +7.6 |
| `M66` | 16 | +5.54 → +5.66 | M66 IBD Undur Pertama ke Purata 50 Hari (benih M, varian 1: akhir_999=775, rolling_4=7, rolling_50=58, s50_kali_1_02=1.306, shift_10=9) | +3.9 → +4.5 | +2.4 → +2.3 |

## 7. Baki yang BELUM ditala (untuk mesin)

Corak berbilang syarat tanpa keluarga berparameter dalam pusingan ini (58): `P23`, `P33`, `P36`, `P37`, `P38`, `P39`, `P40`, `P41`, `P42`, `P43`, `P45`, `P46`, `P48`, `P49`, `N06`, `N07`, `N08`, `N09`, `N124`, `N19`, `N201`, `N202`, `N203`, `N204`, `N22`, `N24`, `N25`, `N27`, `N28`, `N29`, `N31`, `N33`, `N35`, `N36`, `N37`, `N38`, `N39`, `N40`, `N41`, `N42`, `N43`, `N45`, `N47`, `N48`, `N50`, `N51`, `N53`, `N54`, `N55`, `N56`, `N57`, `N64`, `N65`, `N66`, `N68`, `N74`, `N76`, `N80`. Ia kekal pada takrif asal dan tetap diskor bersama.

## 8. Kaveat

- Skor A melambung apabila lebih banyak varian dicuba; hanya angka kumpulan B dan 2025–26 yang dibaca. Kumpulan B sudah dilihat dalam pusingan terdahulu (bukan tahanan bersih).
- Hampir semua skor tertinggi memakai prasyarat earnings 1–5 sesi akan datang (tarikh sebenar, bukan kalendar awal).
- Tiada saham delist. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.
