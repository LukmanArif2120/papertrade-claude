# Lejar Penuh — ringkasan setiap kaedah

Dijana oleh `standard/lejar.py ringkas`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-27. 12394 posisi (3037 tutup lorong 1, 9357 terbuka). Semua isyarat setiap kaedah dibeli pada buka rasmi esok dengan peraturan sama (tiada had sekaedah). Jangkaan = registry set 431 varian modul (dalam sampel).

Nota: data awal didominasi posisi yang tutup cepat (kebanyakan kena henti); nilai hanya selepas posisi matang (lihat `WFO/README.md`, penilaian 15 Jan 2027).

Dua lorong keluar (sejak 17 Okt 2026): Tutup/Menang/Purata tutup = lorong 1 (peraturan kaedah); Selagi naik = lorong 2 (pegang selagi naik, sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14, paras hanya naik, tanpa henti kaedah). n = bilangan keluar.

| Kaedah | Posisi | Tutup | Terbuka | Menang % | Purata tutup % | Hari | Purata terbuka % | Selagi naik n | Purata selagi naik % | Menang jangka % | Purata jangka % | Hari jangka |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M159 Heikin-Ashi Trend | 756 | 277 | 479 | 13 | -3.14 | 3 | 2.47 | 13 | -13.85 | 40 | 0.17 | 6 |
| M125 2-Bar Breakout | 575 | 47 | 528 | 0 | -9.63 | 4 | 2.36 | 11 | -13.95 | 30 | 166.86 | 443 |
| M153 Range Leader | 573 | 177 | 396 | 23 | -2.09 | 3 | 2.32 | 8 | -14.04 | 43 | 0.18 | 6 |
| M14 Walking with the Whales | 498 | 220 | 278 | 4 | -2.86 | 2 | 3.50 | 7 | -18.41 | 21 | 1.52 | 15 |
| M155 Market Cycle Strategy | 398 | 23 | 375 | 0 | -11.98 | 4 | 1.41 | 7 | -19.03 | 49 | 1.56 | 17 |
| M82 Arthur Hill Rotasi Sasaran 10% | 392 | 60 | 332 | 57 | 3.07 | 6 | 0.75 | 8 | -15.98 | 61 | 1.84 | 38 |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | 388 | 251 | 137 | 76 | 1.01 | 3 | -0.61 | 4 | -17.84 | 63 | 0.18 | 5 |
| M136 Short/Intermediate-term Low (Larry Williams) | 385 | 35 | 350 | 0 | -8.86 | 3 | 2.20 | 5 | -15.61 | 24 | 112.90 | 343 |
| M13 Garis Trend Action/Safety Line | 367 | 118 | 249 | 3 | -3.34 | 3 | 2.17 | 6 | -14.71 | 34 | 0.97 | 11 |
| M116 2/20 EMA Breakout (Landry) | 279 | 14 | 265 | 0 | -13.28 | 4 | 1.49 | 7 | -15.19 | 50 | 0.40 | 9 |
| M92 CCI-50 | 254 | 47 | 207 | 13 | -4.29 | 4 | 2.09 | 2 | -10.32 | 49 | 1.17 | 13 |
| M50 Elder Triple Screen | 249 | 95 | 154 | 0 | -3.06 | 3 | 2.59 | 4 | -17.82 | 23 | 1.80 | 18 |
| M31 Band Walk (BB 20/2) | 235 | 1 | 234 | 0 | -30.46 | 7 | 1.16 | 1 | -2.85 | 43 | 3.30 | 32 |
| M161 EMA 10/21 + Supertrend (10,3) | 229 | 34 | 195 | 0 | -6.80 | 4 | 2.13 | 5 | -16.77 | 35 | 1.43 | 18 |
| M81 Bensdorp Long Trend High Momentum | 221 | 12 | 209 | 0 | -14.39 | 6 | 1.68 | 3 | -16.58 | 32 | 8.56 | 105 |
| M03 BB Break + Divergence RSI | 208 | 134 | 74 | 62 | 0.29 | 3 | 1.15 | 4 | -11.94 | 56 | 0.58 | 8 |
| M20 EMA10/15 Crossover + Sudut | 208 | 98 | 110 | 26 | -0.84 | 3 | 1.98 | 2 | -9.17 | 39 | 0.22 | 7 |
| M27 Price Action 4 Tiang | 205 | 122 | 83 | 18 | -2.53 | 3 | 3.98 | 7 | -12.37 | 35 | 0.36 | 7 |
| M70 Pecahan Hari Dalam | 202 | 127 | 75 | 0 | -1.26 | 2 | 3.87 | 2 | -14.12 | 11 | 0.84 | 10 |
| M158 Doubly Adaptive Profit Targets | 180 | 20 | 160 | 20 | -2.95 | 3 | 3.37 | 2 | -9.33 | 34 | 2.94 | 30 |
| M105 Supertrend tulen | 171 | 10 | 161 | 0 | -9.55 | 4 | 1.33 | 2 | -8.04 | 39 | 2.44 | 32 |
| M145 Yum-Yum Continuation | 171 | 2 | 169 | 0 | -15.34 | 4 | 0.82 | 2 | -15.47 | 25 | 80.48 | 356 |
| M102 Stockbee SLTB | 170 | 78 | 92 | 0 | -3.14 | 2 | 3.87 | 3 | -22.81 | 18 | 1.34 | 16 |
| M19 Sneaky Pivot (proksi harian) | 165 | 41 | 124 | 29 | -2.07 | 4 | 2.13 | 2 | -14.95 | 44 | 0.27 | 11 |
| M15 Break & Retest + Henti ATR | 160 | 46 | 114 | 0 | -4.24 | 3 | 2.40 | 3 | -9.87 | 33 | 1.08 | 12 |
| M124 'Last' Stochastic Technique (ChartSchool) | 160 | 19 | 141 | 0 | -6.43 | 3 | 1.38 | 2 | -11.46 | 36 | 1.74 | 20 |
| M36 Turtle 55/20 | 157 | 14 | 143 | 0 | -5.74 | 5 | 1.73 | 2 | -9.26 | 32 | 2.65 | 30 |
| M93 Bollinger Kaedah II: %b + MFI | 150 | 15 | 135 | 0 | -7.16 | 3 | 1.81 | 3 | -14.61 | 36 | 8.20 | 62 |
| M35 Pocket Pivot Morales & Kacher | 139 | 59 | 80 | 0 | -2.59 | 2 | 3.24 | 1 | -16.98 | 28 | 0.29 | 9 |
| M80 Radge Saluran Purata Bergerak (MAC) | 136 | 1 | 135 | 0 | -8.41 | 2 | 0.65 | 1 | -2.85 | 36 | 8.91 | 66 |
| M18 EMA9/21 Pullback | 134 | 76 | 58 | 13 | -2.29 | 2 | 4.43 | 3 | -22.77 | 26 | 0.40 | 7 |
| M131 Ross Hook (Joe Ross) | 124 | 19 | 105 | 0 | -5.03 | 3 | 1.59 | 0 |  | 30 | 2.35 | 30 |
| M30 BB Free Bar + Himpitan 50/2.5 | 123 | 15 | 108 | 20 | -2.47 | 3 | 1.12 | 2 | -9.91 | 37 | 3.80 | 34 |
| M66 IBD Undur Pertama ke Purata 50 Hari | 119 | 38 | 81 | 8 | -3.15 | 2 | 2.70 | 2 | -18.96 | 28 | 1.71 | 19 |
| M111 Sistem Volatiliti Wilder | 117 | 4 | 113 | 0 | -8.45 | 3 | 1.09 | 1 | -13.22 | 39 | 2.39 | 30 |
| M12 Parabolic SAR | 115 | 27 | 88 | 4 | -3.02 | 3 | 2.20 | 0 |  | 29 | 2.04 | 23 |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | 115 | 36 | 79 | 0 | -2.76 | 2 | 1.79 | 2 | -16.61 | 23 | 3.99 | 34 |
| M54 IBD Power Trend | 115 | 14 | 101 | 0 | -5.52 | 4 | 1.73 | 1 | -12.74 | 30 | 3.37 | 37 |
| M55 Guppy GMMA | 109 | 30 | 79 | 0 | -3.97 | 3 | 3.65 | 0 |  | 26 | 2.71 | 28 |
| M39 Radge Pecahan Bollinger 100 hari | 108 | 2 | 106 | 0 | -8.99 | 2 | 0.70 | 0 |  | 37 | 9.11 | 96 |
| M33 Supertrend + SMA10 | 98 | 6 | 92 | 0 | -11.12 | 4 | 1.33 | 1 | -13.22 | 40 | 1.65 | 33 |
| M123 CCI Correction (Lambert, ChartSchool) | 86 | 65 | 21 | 17 | -1.41 | 2 | 2.65 | 0 |  | 28 | 0.92 | 10 |
| M79 Radge: 20% Flipper | 85 | 4 | 81 | 0 | -11.31 | 4 | 0.30 | 1 | -9.56 | 40 | 6.25 | 60 |
| M156 Single Penetration (DiNapoli) | 85 | 2 | 83 | 0 | -8.63 | 2 | 1.95 | 2 | -13.21 | 52 | 0.69 | 9 |
| M89 Chande 65sma-3cc | 83 | 13 | 70 | 0 | -5.08 | 2 | 2.04 | 0 |  | 34 | 1.83 | 26 |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | 79 | 10 | 69 | 10 | -4.32 | 3 | 2.04 | 1 | -5.77 | 34 | 0.55 | 12 |
| M148 Natural Number Method | 79 | 27 | 52 | 0 | -4.94 | 3 | 1.69 | 2 | -19.04 | 35 | 0.50 | 10 |
| M137 Livermore System | 78 | 4 | 74 | 0 | -4.70 | 3 | 1.39 | 1 | -5.77 | 35 | 4.22 | 37 |
| M78 Alvarez Pecahan Mingguan DTAYS | 73 | 5 | 68 | 0 | -9.64 | 6 | 1.30 | 1 | -12.74 | 32 | 3.17 | 40 |
| M119 180 Bullish (Cooper) | 70 | 17 | 53 | 0 | -4.32 | 3 | 1.96 | 1 | -8.63 | 27 | 1.17 | 18 |
| M25 VWAP Wave (proksi harian) | 67 | 21 | 46 | 0 | -3.42 | 2 | 3.69 | 2 | -13.30 | 30 | 0.42 | 10 |
| M28 VWAP Separator + Kiss Pivot | 67 | 35 | 32 | 9 | -4.63 | 3 | 5.29 | 0 |  | 43 | 0.22 | 5 |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | 66 | 6 | 60 | 0 | -6.09 | 5 | 1.80 | 1 | -12.74 | 32 | 2.68 | 29 |
| M99 Three Line Break | 66 | 16 | 50 | 0 | -4.66 | 2 | 3.61 | 1 | -18.18 | 40 | 1.17 | 16 |
| M34 Carter TTM Squeeze | 64 | 4 | 60 | 25 | -2.73 | 4 | 1.58 | 0 |  | 34 | 2.38 | 30 |
| M57 Landry Trend Knockout (TKO) | 63 | 24 | 39 | 0 | -3.54 | 2 | 2.85 | 1 | -12.74 | 21 | 1.55 | 18 |
| M132 Ascending Scallop (Bulkowski) | 62 | 1 | 61 | 0 | -5.77 | 5 | 1.17 | 1 | -5.77 | 42 | 0.98 | 29 |
| M08 SMA20 + SMA200 | 61 | 26 | 35 | 12 | -3.93 | 3 | 4.67 | 0 |  | 32 | 1.07 | 12 |
| M02 MACD + SMA200 | 58 | 18 | 40 | 22 | 0.18 | 2 | 1.04 | 2 | -12.68 | 44 | 0.66 | 14 |
| M147 Improved Three-Bar Pullback | 57 | 1 | 56 | 0 | -15.34 | 7 | 0.01 | 0 |  | 31 | 91.01 | 442 |
| M11 NR7 Breakout + Volume | 53 | 26 | 27 | 38 | -0.95 | 2 | 1.23 | 1 | -8.34 | 36 | 2.86 | 20 |
| M10 EMA3 + CCI + MACD | 52 | 2 | 50 | 0 | -5.36 | 1 | 2.29 | 0 |  | 33 | 4.70 | 54 |
| M149 3-Step Pullback | 52 | 5 | 47 | 0 | -17.41 | 4 | 1.82 | 3 | -20.23 | 19 | 59.37 | 273 |
| M04 BB Squeeze Breakout | 51 | 8 | 43 | 12 | -2.66 | 3 | 1.30 | 0 |  | 36 | 4.96 | 32 |
| M150 Trend Bar Failure (Brooks) | 51 | 3 | 48 | 0 | -3.71 | 6 | 1.21 | 0 |  | 37 | 0.54 | 13 |
| M106 DMI Wilder | 50 | 17 | 33 | 6 | -2.50 | 4 | 1.95 | 0 |  | 32 | 1.01 | 12 |
| M127 Slingshot Bullish | 47 | 20 | 27 | 0 | -2.19 | 2 | 2.25 | 1 | -12.74 | 19 | 2.60 | 16 |
| M122 Moving Momentum (ChartSchool) | 46 | 15 | 31 | 0 | -5.29 | 3 | 2.09 | 0 |  | 35 | 1.79 | 24 |
| M01 Bollinger Band + RSI | 42 | 1 | 41 | 100 | 20.39 | 3 | 2.73 | 0 |  | 67 | 2.22 | 22 |
| M151 Outside Bar Failure | 41 | 5 | 36 | 0 | -3.67 | 2 | 1.66 | 0 |  | 27 | 1.93 | 26 |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | 40 | 0 | 40 |  |  |  | 2.12 | 0 |  | 51 | 1.31 | 19 |
| M74 Lulus Baharu Trend Template Minervini | 39 | 20 | 19 | 0 | -1.89 | 2 | 4.62 | 0 |  | 24 | 2.72 | 20 |
| M160 Measured Move Up | 38 | 22 | 16 | 14 | -1.79 | 2 | 3.12 | 0 |  | 32 | 0.44 | 8 |
| M154 HOLP (High of Low Period) | 37 | 5 | 32 | 0 | -8.41 | 2 | 2.34 | 0 |  | 39 | 1.93 | 27 |
| M146 3-Bar Momentum Pattern | 36 | 5 | 31 | 0 | -5.00 | 2 | 2.47 | 0 |  | 27 | 2.66 | 26 |
| M06 Minervini VCP Breakout | 35 | 1 | 34 | 0 | -7.08 | 3 | 0.80 | 0 |  | 33 | 2.49 | 29 |
| M23 Breitstein Kapitulasi + Kesinambungan | 34 | 16 | 18 | 0 | -1.78 | 2 | 2.68 | 0 |  | 22 | 0.55 | 10 |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | 33 | 3 | 30 | 67 | 1.55 | 4 | 0.85 | 1 | -5.77 | 46 | 1.32 | 29 |
| M118 Expansion Pivot (Cooper) | 32 | 3 | 29 | 0 | -4.21 | 2 | 1.17 | 0 |  | 33 | 1.56 | 27 |
| M90 Pring KST | 31 | 6 | 25 | 0 | -5.61 | 5 | 2.61 | 1 | -6.97 | 30 | 1.95 | 26 |
| M101 Bulkowski: Tiga lembah menaik | 30 | 0 | 30 |  |  |  | 1.67 | 0 |  | 35 | 3.46 | 33 |
| M32 Momentum Burst | 29 | 7 | 22 | 0 | -4.47 | 2 | 6.22 | 1 | -28.69 | 25 | 3.57 | 22 |
| M76 Undercut & Rally pada Low Penting | 29 | 15 | 14 | 13 | -3.27 | 3 | 3.76 | 0 |  | 37 | 0.67 | 9 |
| M117 Landry Pullback (high 2 bulan) | 28 | 1 | 27 | 0 | -5.92 | 5 | 1.51 | 0 |  | 21 | 45.52 | 287 |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | 26 | 12 | 14 | 58 | 0.11 | 2 | 1.04 | 0 |  | 50 | 5.17 | 39 |
| M152 Spike & Ledge | 23 | 0 | 23 |  |  |  | 2.64 | 0 |  | 52 | 3.20 | 36 |
| M59 Anjakan Julat RSI | 22 | 1 | 21 | 0 | -6.92 | 3 | 0.72 | 0 |  | 34 | 3.10 | 37 |
| M133 Bull Hook (Crabel) | 22 | 7 | 15 | 29 | -1.87 | 2 | 2.74 | 0 |  | 41 | 0.68 | 10 |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | 21 | 9 | 12 | 0 | -3.79 | 3 | 2.57 | 0 |  | 25 | 2.69 | 15 |
| M05 MACD Divergence + Pengesahan | 20 | 1 | 19 | 0 | -6.65 | 6 | 0.03 | 0 |  | 35 | 10.85 | 108 |
| M41 FW Penyatuan Mingguan | 20 | 0 | 20 |  |  |  | -0.76 | 0 |  | 36 | 15.03 | 117 |
| M129 Wick Play | 20 | 0 | 20 |  |  |  | 1.25 | 0 |  | 38 | 2.60 | 38 |
| M29 EMA3 + RSI75 + Stokastik | 19 | 12 | 7 | 0 | -2.14 | 1 | 5.83 | 0 |  | 18 | 3.22 | 35 |
| M134 First Kiss After Daylight (Landry) | 19 | 2 | 17 | 0 | -13.60 | 4 | 2.61 | 1 | -27.34 | 34 | 5.41 | 35 |
| M91 Stochastic Pop (Bernstein/Steckler) | 17 | 1 | 16 | 0 | -7.95 | 3 | 1.76 | 0 |  | 42 | 1.63 | 18 |
| M115 Bow Tie (Landry) | 16 | 2 | 14 | 0 | -2.61 | 2 | 3.62 | 0 |  | 27 | 1.06 | 18 |
| M09 Volumatic VIDYA Pivot Retest | 15 | 7 | 8 | 14 | -6.81 | 3 | 4.60 | 1 | -27.00 | 23 | 1.85 | 30 |
| M88 O'Neil Shakeout +3 | 15 | 3 | 12 | 0 | -8.00 | 4 | 3.30 | 0 |  | 32 | 5.56 | 32 |
| M48 Cooper 1-2-3-4 | 14 | 0 | 14 |  |  |  | 3.04 | 0 |  | 34 | 2.79 | 30 |
| M68 Kell Base n' Break | 14 | 1 | 13 | 0 | -0.12 | 1 | 1.64 | 0 |  | 36 | 1.35 | 35 |
| M107 Golden Cross SMA50/200 | 13 | 0 | 13 |  |  |  | 1.33 | 0 |  | 32 | 15.43 | 110 |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | 12 | 2 | 10 | 0 | -7.99 | 3 | 4.73 | 0 |  | 30 | 1.90 | 24 |
| M141 First Thrust (Landry) | 11 | 0 | 11 |  |  |  | 0.93 | 0 |  | 39 | 4.05 | 37 |
| M38 Darvas Kotak | 10 | 0 | 10 |  |  |  | 1.93 | 0 |  | 49 | 18.79 | 210 |
| M126 Hidden Smash Day (beli, Larry Williams) | 10 | 0 | 10 |  |  |  | 0.06 | 0 |  | 35 | 5.15 | 33 |
| M120 Reversal New Highs | 9 | 0 | 9 |  |  |  | 0.41 | 0 |  | 27 | 1.15 | 28 |
| M44 Tapak Rata IBD | 7 | 0 | 7 |  |  |  | -0.58 | 0 |  | 30 | 0.39 | 28 |
| M47 Holy Grail Raschke | 7 | 1 | 6 | 0 | -16.97 | 2 | 2.06 | 0 |  | 51 | 0.25 | 5 |
| M87 IBD Tapak Menaik | 7 | 0 | 7 |  |  |  | 1.69 | 0 |  | 32 | 3.49 | 30 |
| M140 猎豹出击 (Serangan Cheetah) | 7 | 3 | 4 | 0 | -10.14 | 3 | 2.87 | 0 |  | 36 | 5.31 | 25 |
| M142 Pecahan volum dari dasar (底部放量) | 7 | 0 | 7 |  |  |  | -1.48 | 0 |  | 41 | 6.85 | 44 |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | 6 | 0 | 6 |  |  |  | -1.92 | 1 | -3.61 | 25 | 92.22 | 261 |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | 5 | 2 | 3 | 0 | -3.10 | 4 | -2.19 | 0 |  | 23 | 2.81 | 22 |
| M121 High 2 bull flag (Brooks) | 5 | 0 | 5 |  |  |  | 2.57 | 0 |  | 47 | 2.47 | 49 |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | 3 | 1 | 2 | 0 | -16.18 | 6 | -1.05 | 1 | -12.74 | 52 | 0.83 | 18 |
| M64 O'Neil Tiga Minggu Ketat | 2 | 0 | 2 |  |  |  | 3.12 | 0 |  | 34 | 1.68 | 31 |
| M135 3rd Watch | 2 | 0 | 2 |  |  |  | 1.05 | 0 |  | 39 | 2.05 | 35 |
| M07 Qullamaggie Breakout | 1 | 0 | 1 |  |  |  | 4.10 | 0 |  | 20 | 1.05 | 8 |
| M37 Weinstein Peringkat 2 | 1 | 0 | 1 |  |  |  | -0.50 | 0 |  | 41 | 5.49 | 42 |
| M138 直升机空中加油 (Helikopter isi minyak di udara) | 1 | 0 | 1 |  |  |  | -0.30 | 0 |  | 45 | 4.60 | 46 |
| M144 Screw Bar | 1 | 1 | 0 | 100 | 4.10 | 2 |  | 0 |  | 41 | 7.68 | 23 |
| M157 Consolidation Pivot Breakout (versi angka) | 1 | 0 | 1 |  |  |  | -0.91 | 0 |  | 14 | 32.05 | 179 |
| M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | 0 | 0 | 0 |  |  |  |  | 0 |  | 26 | 2.57 | 8 |
| M22 Qullamaggie Episodic Pivot | 0 | 0 | 0 |  |  |  |  | 0 |  | 40 | 3.35 | 8 |
| M24 Rotasi Momentum ROC12 + SMA200 | 0 | 0 | 0 |  |  |  |  | 0 |  | 54 | 28.88 | 65 |
| M40 Clenow Stocks on the Move | 0 | 0 | 0 |  |  |  |  | 0 |  | 38 | 4.80 | 35 |
| M45 High 52 Minggu (George & Hwang) | 0 | 0 | 0 |  |  |  |  | 0 |  | 32 | 12.81 | 61 |
| M51 O'Neil Cawan & Pemegang | 0 | 0 | 0 |  |  |  |  | 0 |  | 39 | 3.12 | 35 |
| M52 Radge Weekend Trend Trader | 0 | 0 | 0 |  |  |  |  | 0 |  | 37 | 5.19 | 37 |
| M56 Gray & Vogel Momentum Lancar (FIP) | 0 | 0 | 0 |  |  |  |  | 0 |  | 43 | 19.93 | 72 |
| M84 Jarak purata bergerak MAD 21/200 | 0 | 0 | 0 |  |  |  |  | 0 |  | 37 | 3.71 | 26 |
| M94 Pecutan Momentum (Chen, Yu & Wang) | 0 | 0 | 0 |  |  |  |  | 0 |  | 63 | 24.04 | 121 |
| M96 Momo India: Ranking Sharpe 3/6/12 bulan | 0 | 0 | 0 |  |  |  |  | 0 |  | 43 | 12.18 | 54 |
| M104 High Tight Flag / Power Play | 0 | 0 | 0 |  |  |  |  | 0 |  | 35 | 5.62 | 33 |
