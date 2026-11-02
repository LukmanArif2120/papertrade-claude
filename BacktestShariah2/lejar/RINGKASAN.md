# Lejar Penuh — ringkasan setiap kaedah

Dijana oleh `standard/lejar.py ringkas`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-30. 16629 posisi (6079 tutup lorong 1, 10550 terbuka). Semua isyarat setiap kaedah dibeli pada buka rasmi esok dengan peraturan sama (tiada had sekaedah). Jangkaan = registry set 431 varian modul (dalam sampel).

Nota: data awal didominasi posisi yang tutup cepat (kebanyakan kena henti); nilai hanya selepas posisi matang (lihat `WFO/README.md`, penilaian 15 Jan 2027).

Dua lorong keluar (sejak 17 Okt 2026): Tutup/Menang/Purata tutup = lorong 1 (peraturan kaedah); Selagi naik = lorong 2 (pegang selagi naik, sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14, paras hanya naik, tanpa henti kaedah). n = bilangan keluar.

| Kaedah | Posisi | Tutup | Terbuka | Menang % | Purata tutup % | Hari | Purata terbuka % | Selagi naik n | Purata selagi naik % | Menang jangka % | Purata jangka % | Hari jangka |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M159 Heikin-Ashi Trend | 981 | 674 | 307 | 37 | -0.83 | 5 | 2.29 | 38 | -14.24 | 40 | 0.17 | 6 |
| M125 2-Bar Breakout | 778 | 132 | 646 | 0 | -9.36 | 5 | 1.81 | 28 | -13.18 | 30 | 166.86 | 443 |
| M153 Range Leader | 747 | 521 | 226 | 47 | 0.28 | 5 | 2.21 | 24 | -13.62 | 43 | 0.18 | 6 |
| M14 Walking with the Whales | 629 | 330 | 299 | 3 | -2.96 | 3 | 4.45 | 21 | -17.64 | 21 | 1.52 | 15 |
| M27 Price Action 4 Tiang | 547 | 282 | 265 | 14 | -3.25 | 3 | 2.53 | 12 | -13.23 | 35 | 0.36 | 7 |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | 531 | 407 | 124 | 76 | 1.62 | 3 | -2.30 | 16 | -14.85 | 63 | 0.18 | 5 |
| M155 Market Cycle Strategy | 501 | 79 | 422 | 0 | -10.78 | 6 | 2.46 | 21 | -15.57 | 49 | 1.56 | 17 |
| M136 Short/Intermediate-term Low (Larry Williams) | 492 | 81 | 411 | 0 | -9.67 | 5 | 1.90 | 12 | -14.90 | 24 | 112.90 | 343 |
| M13 Garis Trend Action/Safety Line | 491 | 207 | 284 | 3 | -4.23 | 3 | 3.02 | 17 | -16.94 | 34 | 0.97 | 11 |
| M82 Arthur Hill Rotasi Sasaran 10% | 431 | 91 | 340 | 63 | 4.79 | 7 | -0.08 | 16 | -14.41 | 61 | 1.84 | 38 |
| M116 2/20 EMA Breakout (Landry) | 347 | 158 | 189 | 60 | 0.59 | 9 | 1.59 | 18 | -14.93 | 50 | 0.40 | 9 |
| M50 Elder Triple Screen | 341 | 136 | 205 | 0 | -3.10 | 3 | 3.16 | 11 | -16.86 | 23 | 1.80 | 18 |
| M92 CCI-50 | 336 | 115 | 221 | 23 | -3.96 | 5 | 2.74 | 9 | -10.30 | 49 | 1.17 | 13 |
| M161 EMA 10/21 + Supertrend (10,3) | 318 | 67 | 251 | 1 | -7.19 | 5 | 2.97 | 12 | -18.95 | 35 | 1.43 | 18 |
| M31 Band Walk (BB 20/2) | 280 | 9 | 271 | 0 | -12.99 | 8 | 2.13 | 10 | -11.03 | 43 | 3.30 | 32 |
| M70 Pecahan Hari Dalam | 274 | 195 | 79 | 0 | -1.43 | 2 | 4.98 | 7 | -13.65 | 11 | 0.84 | 10 |
| M20 EMA10/15 Crossover + Sudut | 273 | 177 | 96 | 26 | -1.31 | 4 | 0.86 | 7 | -21.49 | 39 | 0.22 | 7 |
| M03 BB Break + Divergence RSI | 267 | 190 | 77 | 60 | -0.26 | 4 | -1.25 | 11 | -12.39 | 56 | 0.58 | 8 |
| M81 Bensdorp Long Trend High Momentum | 255 | 39 | 216 | 0 | -14.11 | 8 | 0.75 | 6 | -22.83 | 32 | 8.56 | 105 |
| M19 Sneaky Pivot (proksi harian) | 239 | 109 | 130 | 28 | -3.53 | 4 | -1.10 | 5 | -11.79 | 44 | 0.27 | 11 |
| M124 'Last' Stochastic Technique (ChartSchool) | 239 | 56 | 183 | 2 | -6.46 | 4 | 2.79 | 6 | -11.59 | 36 | 1.74 | 20 |
| M105 Supertrend tulen | 226 | 23 | 203 | 0 | -9.85 | 5 | 2.54 | 8 | -12.54 | 39 | 2.44 | 32 |
| M18 EMA9/21 Pullback | 225 | 133 | 92 | 13 | -1.77 | 3 | 3.74 | 7 | -18.34 | 26 | 0.40 | 7 |
| M158 Doubly Adaptive Profit Targets | 222 | 31 | 191 | 13 | -4.17 | 4 | 3.80 | 7 | -11.21 | 34 | 2.94 | 30 |
| M102 Stockbee SLTB | 220 | 116 | 104 | 0 | -3.71 | 3 | 5.03 | 12 | -21.51 | 18 | 1.34 | 16 |
| M15 Break & Retest + Henti ATR | 212 | 75 | 137 | 0 | -4.66 | 4 | 4.04 | 9 | -10.30 | 33 | 1.08 | 12 |
| M145 Yum-Yum Continuation | 206 | 13 | 193 | 0 | -13.31 | 5 | 2.12 | 10 | -14.71 | 25 | 80.48 | 356 |
| M35 Pocket Pivot Morales & Kacher | 200 | 99 | 101 | 1 | -3.07 | 3 | 4.43 | 6 | -14.23 | 28 | 0.29 | 9 |
| M36 Turtle 55/20 | 190 | 36 | 154 | 0 | -6.72 | 5 | 3.35 | 8 | -14.04 | 32 | 2.65 | 30 |
| M12 Parabolic SAR | 189 | 56 | 133 | 7 | -4.15 | 3 | 1.79 | 4 | -16.02 | 29 | 2.04 | 23 |
| M93 Bollinger Kaedah II: %b + MFI | 186 | 21 | 165 | 0 | -7.91 | 4 | 3.00 | 10 | -10.76 | 36 | 8.20 | 62 |
| M80 Radge Saluran Purata Bergerak (MAC) | 185 | 10 | 175 | 0 | -11.22 | 5 | 2.50 | 8 | -13.99 | 36 | 8.91 | 66 |
| M111 Sistem Volatiliti Wilder | 161 | 17 | 144 | 0 | -9.55 | 5 | 2.33 | 7 | -12.79 | 39 | 2.39 | 30 |
| M131 Ross Hook (Joe Ross) | 161 | 37 | 124 | 0 | -5.58 | 4 | 2.58 | 7 | -15.18 | 30 | 2.35 | 30 |
| M79 Radge: 20% Flipper | 158 | 19 | 139 | 0 | -13.29 | 4 | 0.14 | 6 | -13.87 | 40 | 6.25 | 60 |
| M30 BB Free Bar + Himpitan 50/2.5 | 150 | 26 | 124 | 15 | -4.58 | 4 | 2.40 | 7 | -14.00 | 37 | 3.80 | 34 |
| M66 IBD Undur Pertama ke Purata 50 Hari | 148 | 61 | 87 | 7 | -4.20 | 3 | 4.13 | 3 | -17.96 | 28 | 1.71 | 19 |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | 146 | 60 | 86 | 0 | -3.30 | 3 | 3.12 | 7 | -16.20 | 23 | 3.99 | 34 |
| M39 Radge Pecahan Bollinger 100 hari | 144 | 6 | 138 | 0 | -16.38 | 4 | 1.53 | 4 | -24.97 | 37 | 9.11 | 96 |
| M54 IBD Power Trend | 141 | 31 | 110 | 0 | -5.82 | 5 | 2.56 | 4 | -17.02 | 30 | 3.37 | 37 |
| M55 Guppy GMMA | 135 | 56 | 79 | 0 | -4.80 | 4 | 4.64 | 1 | -21.69 | 26 | 2.71 | 28 |
| M33 Supertrend + SMA10 | 125 | 10 | 115 | 0 | -10.52 | 4 | 3.10 | 4 | -14.00 | 40 | 1.65 | 33 |
| M148 Natural Number Method | 120 | 50 | 70 | 4 | -5.01 | 4 | 2.16 | 5 | -15.09 | 35 | 0.50 | 10 |
| M89 Chande 65sma-3cc | 118 | 30 | 88 | 0 | -6.07 | 3 | 3.14 | 2 | -12.80 | 34 | 1.83 | 26 |
| M156 Single Penetration (DiNapoli) | 117 | 39 | 78 | 51 | 0.83 | 9 | 1.37 | 5 | -20.80 | 52 | 0.69 | 9 |
| M123 CCI Correction (Lambert, ChartSchool) | 114 | 93 | 21 | 15 | -1.92 | 2 | 2.13 | 0 |  | 28 | 0.92 | 10 |
| M99 Three Line Break | 107 | 38 | 69 | 0 | -6.93 | 3 | 2.66 | 1 | -18.18 | 40 | 1.17 | 16 |
| M25 VWAP Wave (proksi harian) | 105 | 39 | 66 | 0 | -3.51 | 3 | 3.39 | 5 | -10.75 | 30 | 0.42 | 10 |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | 104 | 22 | 82 | 14 | -4.83 | 5 | 3.31 | 4 | -20.24 | 34 | 0.55 | 12 |
| M137 Livermore System | 99 | 9 | 90 | 0 | -7.75 | 6 | 2.91 | 4 | -12.99 | 35 | 4.22 | 37 |
| M08 SMA20 + SMA200 | 96 | 43 | 53 | 7 | -4.60 | 3 | 3.47 | 2 | -28.77 | 32 | 1.07 | 12 |
| M149 3-Step Pullback | 91 | 11 | 80 | 0 | -11.56 | 5 | 1.73 | 4 | -20.66 | 19 | 59.37 | 273 |
| M02 MACD + SMA200 | 90 | 23 | 67 | 17 | -1.14 | 2 | 1.03 | 3 | -18.84 | 44 | 0.66 | 14 |
| M119 180 Bullish (Cooper) | 87 | 33 | 54 | 0 | -5.02 | 4 | 2.13 | 5 | -15.09 | 27 | 1.17 | 18 |
| M34 Carter TTM Squeeze | 83 | 13 | 70 | 8 | -6.61 | 5 | 2.72 | 2 | -15.92 | 34 | 2.38 | 30 |
| M57 Landry Trend Knockout (TKO) | 83 | 38 | 45 | 0 | -3.86 | 3 | 2.76 | 2 | -24.45 | 21 | 1.55 | 18 |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | 82 | 14 | 68 | 0 | -6.34 | 5 | 2.67 | 2 | -11.04 | 32 | 2.68 | 29 |
| M147 Improved Three-Bar Pullback | 80 | 6 | 74 | 0 | -14.75 | 9 | -0.01 | 0 |  | 31 | 91.01 | 442 |
| M04 BB Squeeze Breakout | 79 | 14 | 65 | 14 | -4.53 | 4 | 1.73 | 3 | -18.34 | 36 | 4.96 | 32 |
| M122 Moving Momentum (ChartSchool) | 77 | 26 | 51 | 0 | -5.48 | 3 | 0.66 | 0 |  | 35 | 1.79 | 24 |
| M10 EMA3 + CCI + MACD | 75 | 9 | 66 | 0 | -5.94 | 3 | 2.76 | 0 |  | 33 | 4.70 | 54 |
| M78 Alvarez Pecahan Mingguan DTAYS | 73 | 19 | 54 | 0 | -9.51 | 5 | 3.11 | 4 | -16.02 | 32 | 3.17 | 40 |
| M132 Ascending Scallop (Bulkowski) | 72 | 5 | 67 | 0 | -11.17 | 6 | 2.21 | 4 | -11.03 | 42 | 0.98 | 29 |
| M28 VWAP Separator + Kiss Pivot | 71 | 57 | 14 | 23 | -1.81 | 4 | 1.97 | 0 |  | 43 | 0.22 | 5 |
| M11 NR7 Breakout + Volume | 70 | 42 | 28 | 38 | -2.02 | 2 | 2.00 | 2 | -14.86 | 36 | 2.86 | 20 |
| M106 DMI Wilder | 65 | 26 | 39 | 19 | -2.86 | 5 | 2.72 | 3 | -13.61 | 32 | 1.01 | 12 |
| M150 Trend Bar Failure (Brooks) | 61 | 9 | 52 | 0 | -3.89 | 7 | 2.49 | 0 |  | 37 | 0.54 | 13 |
| M117 Landry Pullback (high 2 bulan) | 56 | 4 | 52 | 0 | -6.64 | 8 | 1.36 | 1 | -11.01 | 21 | 45.52 | 287 |
| M74 Lulus Baharu Trend Template Minervini | 53 | 29 | 24 | 0 | -2.48 | 2 | 5.10 | 1 | -9.82 | 24 | 2.72 | 20 |
| M127 Slingshot Bullish | 53 | 28 | 25 | 0 | -2.51 | 3 | 3.52 | 2 | -14.69 | 19 | 2.60 | 16 |
| M151 Outside Bar Failure | 53 | 19 | 34 | 0 | -4.14 | 4 | 4.17 | 1 | -21.98 | 27 | 1.93 | 26 |
| M01 Bollinger Band + RSI | 50 | 5 | 45 | 100 | 13.82 | 7 | -0.02 | 0 |  | 67 | 2.22 | 22 |
| M23 Breitstein Kapitulasi + Kesinambungan | 50 | 25 | 25 | 0 | -1.90 | 2 | 2.98 | 0 |  | 22 | 0.55 | 10 |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | 50 | 5 | 45 | 0 | -15.97 | 6 | 2.14 | 2 | -18.07 | 51 | 1.31 | 19 |
| M146 3-Bar Momentum Pattern | 49 | 7 | 42 | 0 | -5.46 | 2 | 3.75 | 0 |  | 27 | 2.66 | 26 |
| M160 Measured Move Up | 49 | 25 | 24 | 12 | -2.13 | 2 | 3.34 | 1 | -21.34 | 32 | 0.44 | 8 |
| M90 Pring KST | 48 | 16 | 32 | 0 | -7.01 | 6 | 1.38 | 2 | -17.57 | 30 | 1.95 | 26 |
| M154 HOLP (High of Low Period) | 46 | 13 | 33 | 0 | -11.02 | 4 | 0.80 | 0 |  | 39 | 1.93 | 27 |
| M06 Minervini VCP Breakout | 45 | 5 | 40 | 20 | -5.73 | 6 | 2.88 | 1 | -11.01 | 33 | 2.49 | 29 |
| M118 Expansion Pivot (Cooper) | 44 | 9 | 35 | 0 | -6.16 | 3 | 2.62 | 1 | -10.63 | 33 | 1.56 | 27 |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | 41 | 10 | 31 | 60 | 3.71 | 5 | 0.39 | 2 | -5.27 | 46 | 1.32 | 29 |
| M101 Bulkowski: Tiga lembah menaik | 38 | 1 | 37 | 0 | -9.35 | 10 | 1.81 | 1 | -9.35 | 35 | 3.46 | 33 |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | 36 | 23 | 13 | 61 | 0.63 | 2 | -1.16 | 1 | -21.98 | 50 | 5.17 | 39 |
| M32 Momentum Burst | 35 | 11 | 24 | 0 | -8.61 | 4 | 6.75 | 4 | -25.87 | 25 | 3.57 | 22 |
| M76 Undercut & Rally pada Low Penting | 34 | 27 | 7 | 15 | -4.30 | 4 | 1.87 | 1 | -32.57 | 37 | 0.67 | 9 |
| M152 Spike & Ledge | 32 | 0 | 32 |  |  |  | 0.50 | 1 | -4.77 | 52 | 3.20 | 36 |
| M134 First Kiss After Daylight (Landry) | 30 | 5 | 25 | 0 | -8.52 | 4 | 3.44 | 1 | -27.34 | 34 | 5.41 | 35 |
| M48 Cooper 1-2-3-4 | 29 | 3 | 26 | 0 | -12.15 | 5 | 0.71 | 1 | -36.15 | 34 | 2.79 | 30 |
| M88 O'Neil Shakeout +3 | 29 | 10 | 19 | 0 | -8.48 | 3 | 4.38 | 0 |  | 32 | 5.56 | 32 |
| M05 MACD Divergence + Pengesahan | 28 | 4 | 24 | 0 | -8.01 | 5 | 1.65 | 1 | -10.63 | 35 | 10.85 | 108 |
| M59 Anjakan Julat RSI | 28 | 5 | 23 | 0 | -17.08 | 5 | 1.52 | 1 | -31.17 | 34 | 3.10 | 37 |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | 27 | 14 | 13 | 0 | -4.53 | 3 | 4.13 | 0 |  | 25 | 2.69 | 15 |
| M133 Bull Hook (Crabel) | 26 | 12 | 14 | 25 | -2.01 | 3 | 4.64 | 1 | -8.71 | 41 | 0.68 | 10 |
| M29 EMA3 + RSI75 + Stokastik | 22 | 15 | 7 | 0 | -2.41 | 2 | 2.33 | 2 | -10.08 | 18 | 3.22 | 35 |
| M115 Bow Tie (Landry) | 22 | 7 | 15 | 0 | -2.63 | 3 | 4.63 | 0 |  | 27 | 1.06 | 18 |
| M129 Wick Play | 22 | 0 | 22 |  |  |  | 3.42 | 1 | -4.77 | 38 | 2.60 | 38 |
| M41 FW Penyatuan Mingguan | 20 | 0 | 20 |  |  |  | 2.63 | 0 |  | 36 | 15.03 | 117 |
| M91 Stochastic Pop (Bernstein/Steckler) | 20 | 3 | 17 | 0 | -9.77 | 4 | 8.58 | 0 |  | 42 | 1.63 | 18 |
| M68 Kell Base n' Break | 19 | 1 | 18 | 0 | -0.12 | 1 | 1.34 | 0 |  | 36 | 1.35 | 35 |
| M09 Volumatic VIDYA Pivot Retest | 17 | 10 | 7 | 10 | -8.49 | 4 | -0.58 | 2 | -31.57 | 23 | 1.85 | 30 |
| M107 Golden Cross SMA50/200 | 17 | 1 | 16 | 0 | -13.84 | 7 | 2.26 | 0 |  | 32 | 15.43 | 110 |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | 14 | 5 | 9 | 0 | -6.88 | 7 | 4.42 | 0 |  | 30 | 1.90 | 24 |
| M126 Hidden Smash Day (beli, Larry Williams) | 14 | 1 | 13 | 0 | -1.81 | 5 | 1.22 | 0 |  | 35 | 5.15 | 33 |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | 13 | 4 | 9 | 0 | -1.82 | 3 | 0.68 | 0 |  | 23 | 2.81 | 22 |
| M47 Holy Grail Raschke | 13 | 4 | 9 | 50 | -9.80 | 2 | -0.43 | 1 | -36.15 | 51 | 0.25 | 5 |
| M141 First Thrust (Landry) | 13 | 2 | 11 | 0 | -6.37 | 8 | 2.36 | 0 |  | 39 | 4.05 | 37 |
| M140 猎豹出击 (Serangan Cheetah) | 12 | 4 | 8 | 0 | -9.62 | 2 | 0.87 | 1 | -14.41 | 36 | 5.31 | 25 |
| M142 Pecahan volum dari dasar (底部放量) | 12 | 0 | 12 |  |  |  | 1.79 | 0 |  | 41 | 6.85 | 44 |
| M120 Reversal New Highs | 11 | 1 | 10 | 0 | -4.27 | 3 | 1.45 | 0 |  | 27 | 1.15 | 28 |
| M38 Darvas Kotak | 10 | 0 | 10 |  |  |  | 6.27 | 0 |  | 49 | 18.79 | 210 |
| M87 IBD Tapak Menaik | 9 | 1 | 8 | 0 | -8.99 | 5 | 1.30 | 0 |  | 32 | 3.49 | 30 |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | 8 | 0 | 8 |  |  |  | -1.61 | 1 | -3.61 | 25 | 92.22 | 261 |
| M44 Tapak Rata IBD | 7 | 2 | 5 | 0 | -8.00 | 8 | -0.05 | 0 |  | 30 | 0.39 | 28 |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | 6 | 1 | 5 | 0 | -16.18 | 6 | -0.30 | 1 | -12.74 | 52 | 0.83 | 18 |
| M121 High 2 bull flag (Brooks) | 5 | 0 | 5 |  |  |  | 1.13 | 0 |  | 47 | 2.47 | 49 |
| M135 3rd Watch | 4 | 0 | 4 |  |  |  | 0.87 | 0 |  | 39 | 2.05 | 35 |
| M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | 3 | 0 | 3 |  |  |  | 0.12 | 0 |  | 26 | 2.57 | 8 |
| M157 Consolidation Pivot Breakout (versi angka) | 3 | 0 | 3 |  |  |  | 2.03 | 0 |  | 14 | 32.05 | 179 |
| M64 O'Neil Tiga Minggu Ketat | 2 | 1 | 1 | 0 | -20.41 | 10 | 3.92 | 1 | -28.17 | 34 | 1.68 | 31 |
| M144 Screw Bar | 2 | 2 | 0 | 50 | 1.41 | 2 |  | 0 |  | 41 | 7.68 | 23 |
| M07 Qullamaggie Breakout | 1 | 0 | 1 |  |  |  | 6.34 | 0 |  | 20 | 1.05 | 8 |
| M37 Weinstein Peringkat 2 | 1 | 0 | 1 |  |  |  | -0.40 | 0 |  | 41 | 5.49 | 42 |
| M51 O'Neil Cawan & Pemegang | 1 | 0 | 1 |  |  |  | -0.91 | 0 |  | 39 | 3.12 | 35 |
| M138 直升机空中加油 (Helikopter isi minyak di udara) | 1 | 0 | 1 |  |  |  | -0.20 | 0 |  | 45 | 4.60 | 46 |
| M22 Qullamaggie Episodic Pivot | 0 | 0 | 0 |  |  |  |  | 0 |  | 40 | 3.35 | 8 |
| M24 Rotasi Momentum ROC12 + SMA200 | 0 | 0 | 0 |  |  |  |  | 0 |  | 54 | 28.88 | 65 |
| M40 Clenow Stocks on the Move | 0 | 0 | 0 |  |  |  |  | 0 |  | 38 | 4.80 | 35 |
| M45 High 52 Minggu (George & Hwang) | 0 | 0 | 0 |  |  |  |  | 0 |  | 32 | 12.81 | 61 |
| M52 Radge Weekend Trend Trader | 0 | 0 | 0 |  |  |  |  | 0 |  | 37 | 5.19 | 37 |
| M56 Gray & Vogel Momentum Lancar (FIP) | 0 | 0 | 0 |  |  |  |  | 0 |  | 43 | 19.93 | 72 |
| M84 Jarak purata bergerak MAD 21/200 | 0 | 0 | 0 |  |  |  |  | 0 |  | 37 | 3.71 | 26 |
| M94 Pecutan Momentum (Chen, Yu & Wang) | 0 | 0 | 0 |  |  |  |  | 0 |  | 63 | 24.04 | 121 |
| M96 Momo India: Ranking Sharpe 3/6/12 bulan | 0 | 0 | 0 |  |  |  |  | 0 |  | 43 | 12.18 | 54 |
| M104 High Tight Flag / Power Play | 0 | 0 | 0 |  |  |  |  | 0 |  | 35 | 5.62 | 33 |
