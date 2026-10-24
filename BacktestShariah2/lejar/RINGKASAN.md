# Lejar Penuh — ringkasan setiap kaedah

Dijana oleh `standard/lejar.py ringkas`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-23. 10268 posisi (2159 tutup lorong 1, 8109 terbuka). Semua isyarat setiap kaedah dibeli pada buka rasmi esok dengan peraturan sama (tiada had sekaedah). Jangkaan = registry set 431 varian modul (dalam sampel).

Nota: data awal didominasi posisi yang tutup cepat (kebanyakan kena henti); nilai hanya selepas posisi matang (lihat `WFO/README.md`, penilaian 15 Jan 2027).

Dua lorong keluar (sejak 17 Okt 2026): Tutup/Menang/Purata tutup = lorong 1 (peraturan kaedah); Selagi naik = lorong 2 (pegang selagi naik, sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14, paras hanya naik, tanpa henti kaedah). n = bilangan keluar.

| Kaedah | Posisi | Tutup | Terbuka | Menang % | Purata tutup % | Hari | Purata terbuka % | Selagi naik n | Purata selagi naik % | Menang jangka % | Purata jangka % | Hari jangka |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M159 Heikin-Ashi Trend | 630 | 225 | 405 | 12 | -2.85 | 2 | 2.90 | 3 | -15.89 | 40 | 0.17 | 6 |
| M125 2-Bar Breakout | 514 | 26 | 488 | 0 | -8.64 | 3 | 2.02 | 3 | -15.89 | 30 | 166.86 | 443 |
| M153 Range Leader | 474 | 145 | 329 | 20 | -2.16 | 2 | 3.00 | 2 | -17.00 | 43 | 0.18 | 6 |
| M14 Walking with the Whales | 423 | 160 | 263 | 4 | -3.03 | 2 | 3.77 | 3 | -13.63 | 21 | 1.52 | 15 |
| M82 Arthur Hill Rotasi Sasaran 10% | 372 | 34 | 338 | 53 | 2.29 | 5 | 0.78 | 4 | -19.51 | 61 | 1.84 | 38 |
| M155 Market Cycle Strategy | 344 | 14 | 330 | 0 | -9.32 | 4 | 1.08 | 2 | -20.34 | 49 | 1.56 | 17 |
| M136 Short/Intermediate-term Low (Larry Williams) | 323 | 26 | 297 | 0 | -7.61 | 2 | 1.10 | 1 | -17.01 | 24 | 112.90 | 343 |
| M13 Garis Trend Action/Safety Line | 308 | 89 | 219 | 0 | -3.14 | 2 | 2.00 | 1 | -18.18 | 34 | 0.97 | 11 |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | 297 | 168 | 129 | 80 | 1.35 | 3 | -3.89 | 2 | -23.88 | 63 | 0.18 | 5 |
| M116 2/20 EMA Breakout (Landry) | 256 | 4 | 252 | 0 | -8.74 | 3 | 2.48 | 1 | -16.98 | 50 | 0.40 | 9 |
| M31 Band Walk (BB 20/2) | 209 | 0 | 209 |  |  |  | 2.11 | 0 |  | 43 | 3.30 | 32 |
| M92 CCI-50 | 208 | 28 | 180 | 4 | -4.91 | 3 | 1.93 | 0 |  | 49 | 1.17 | 13 |
| M27 Price Action 4 Tiang | 207 | 117 | 90 | 20 | -2.24 | 3 | 4.21 | 1 | -12.52 | 35 | 0.36 | 7 |
| M50 Elder Triple Screen | 201 | 65 | 136 | 0 | -3.13 | 2 | 2.60 | 0 |  | 23 | 1.80 | 18 |
| M161 EMA 10/21 + Supertrend (10,3) | 200 | 15 | 185 | 0 | -5.23 | 4 | 1.93 | 1 | -15.97 | 35 | 1.43 | 18 |
| M81 Bensdorp Long Trend High Momentum | 199 | 6 | 193 | 0 | -11.85 | 5 | -0.14 | 1 | -12.37 | 32 | 8.56 | 105 |
| M03 BB Break + Divergence RSI | 171 | 107 | 64 | 57 | -0.18 | 3 | -0.32 | 1 | -12.52 | 56 | 0.58 | 8 |
| M20 EMA10/15 Crossover + Sudut | 167 | 77 | 90 | 22 | -1.66 | 3 | 1.81 | 0 |  | 39 | 0.22 | 7 |
| M158 Doubly Adaptive Profit Targets | 162 | 17 | 145 | 24 | -2.54 | 2 | 4.95 | 1 | -16.32 | 34 | 2.94 | 30 |
| M105 Supertrend tulen | 153 | 4 | 149 | 0 | -10.86 | 4 | 2.03 | 1 | -13.22 | 39 | 2.44 | 32 |
| M102 Stockbee SLTB | 143 | 55 | 88 | 0 | -3.02 | 2 | 4.14 | 0 |  | 18 | 1.34 | 16 |
| M36 Turtle 55/20 | 139 | 5 | 134 | 0 | -5.34 | 4 | 2.69 | 0 |  | 32 | 2.65 | 30 |
| M70 Pecahan Hari Dalam | 131 | 70 | 61 | 0 | -1.37 | 1 | 5.69 | 0 |  | 11 | 0.84 | 10 |
| M93 Bollinger Kaedah II: %b + MFI | 128 | 11 | 117 | 0 | -5.82 | 2 | 3.08 | 1 | -13.22 | 36 | 8.20 | 62 |
| M124 'Last' Stochastic Technique (ChartSchool) | 127 | 10 | 117 | 0 | -6.79 | 3 | 2.18 | 1 | -13.22 | 36 | 1.74 | 20 |
| M15 Break & Retest + Henti ATR | 126 | 30 | 96 | 0 | -4.26 | 3 | 2.69 | 1 | -12.52 | 33 | 1.08 | 12 |
| M145 Yum-Yum Continuation | 124 | 0 | 124 |  |  |  | 2.55 | 0 |  | 25 | 80.48 | 356 |
| M35 Pocket Pivot Morales & Kacher | 119 | 42 | 77 | 0 | -2.72 | 2 | 3.32 | 1 | -16.98 | 28 | 0.29 | 9 |
| M18 EMA9/21 Pullback | 116 | 51 | 65 | 14 | -2.60 | 2 | 3.40 | 1 | -15.97 | 26 | 0.40 | 7 |
| M80 Radge Saluran Purata Bergerak (MAC) | 113 | 1 | 112 | 0 | -8.41 | 2 | 2.06 | 0 |  | 36 | 8.91 | 66 |
| M30 BB Free Bar + Himpitan 50/2.5 | 112 | 8 | 104 | 0 | -3.93 | 3 | 2.74 | 1 | -16.98 | 37 | 3.80 | 34 |
| M131 Ross Hook (Joe Ross) | 111 | 6 | 105 | 0 | -6.00 | 2 | 2.22 | 0 |  | 30 | 2.35 | 30 |
| M111 Sistem Volatiliti Wilder | 100 | 2 | 98 | 0 | -8.93 | 2 | 2.06 | 1 | -13.22 | 39 | 2.39 | 30 |
| M54 IBD Power Trend | 96 | 3 | 93 | 0 | -6.09 | 4 | 2.57 | 0 |  | 30 | 3.37 | 37 |
| M66 IBD Undur Pertama ke Purata 50 Hari | 96 | 27 | 69 | 4 | -3.19 | 2 | 3.18 | 0 |  | 28 | 1.71 | 19 |
| M19 Sneaky Pivot (proksi harian) | 95 | 36 | 59 | 25 | -3.55 | 4 | 0.79 | 1 | -17.01 | 44 | 0.27 | 11 |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | 95 | 29 | 66 | 0 | -1.86 | 2 | 2.76 | 0 |  | 23 | 3.99 | 34 |
| M39 Radge Pecahan Bollinger 100 hari | 91 | 2 | 89 | 0 | -8.99 | 2 | 2.00 | 0 |  | 37 | 9.11 | 96 |
| M33 Supertrend + SMA10 | 90 | 3 | 87 | 0 | -11.20 | 4 | 2.18 | 1 | -13.22 | 40 | 1.65 | 33 |
| M55 Guppy GMMA | 84 | 21 | 63 | 0 | -4.18 | 2 | 3.03 | 0 |  | 26 | 2.71 | 28 |
| M12 Parabolic SAR | 72 | 20 | 52 | 0 | -3.64 | 3 | 3.17 | 0 |  | 29 | 2.04 | 23 |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | 72 | 7 | 65 | 14 | -3.49 | 2 | 2.48 | 0 |  | 34 | 0.55 | 12 |
| M156 Single Penetration (DiNapoli) | 69 | 2 | 67 | 0 | -8.63 | 2 | 2.65 | 2 | -13.21 | 52 | 0.69 | 9 |
| M123 CCI Correction (Lambert, ChartSchool) | 68 | 53 | 15 | 9 | -1.61 | 2 | 2.63 | 0 |  | 28 | 0.92 | 10 |
| M137 Livermore System | 67 | 1 | 66 | 0 | -1.03 | 1 | 2.93 | 0 |  | 35 | 4.22 | 37 |
| M79 Radge: 20% Flipper | 66 | 2 | 64 | 0 | -9.74 | 3 | 1.15 | 0 |  | 40 | 6.25 | 60 |
| M89 Chande 65sma-3cc | 66 | 10 | 56 | 0 | -4.94 | 2 | 2.14 | 0 |  | 34 | 1.83 | 26 |
| M148 Natural Number Method | 64 | 12 | 52 | 0 | -3.90 | 2 | 2.21 | 0 |  | 35 | 0.50 | 10 |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | 58 | 1 | 57 | 0 | -5.54 | 2 | 2.86 | 0 |  | 32 | 2.68 | 29 |
| M99 Three Line Break | 53 | 15 | 38 | 0 | -4.95 | 2 | 4.68 | 1 | -18.18 | 40 | 1.17 | 16 |
| M25 VWAP Wave (proksi harian) | 52 | 13 | 39 | 0 | -3.49 | 2 | 4.38 | 1 | -15.97 | 30 | 0.42 | 10 |
| M34 Carter TTM Squeeze | 52 | 2 | 50 | 50 | -1.73 | 4 | 3.41 | 0 |  | 34 | 2.38 | 30 |
| M57 Landry Trend Knockout (TKO) | 52 | 19 | 33 | 0 | -3.61 | 2 | 3.40 | 0 |  | 21 | 1.55 | 18 |
| M119 180 Bullish (Cooper) | 51 | 8 | 43 | 0 | -3.67 | 2 | 3.69 | 0 |  | 27 | 1.17 | 18 |
| M08 SMA20 + SMA200 | 50 | 22 | 28 | 14 | -3.97 | 3 | 3.00 | 0 |  | 32 | 1.07 | 12 |
| M132 Ascending Scallop (Bulkowski) | 49 | 0 | 49 |  |  |  | 3.06 | 0 |  | 42 | 0.98 | 29 |
| M02 MACD + SMA200 | 47 | 15 | 32 | 20 | -0.00 | 2 | 0.15 | 1 | -17.01 | 44 | 0.66 | 14 |
| M106 DMI Wilder | 45 | 11 | 34 | 0 | -2.63 | 3 | 1.97 | 0 |  | 32 | 1.01 | 12 |
| M150 Trend Bar Failure (Brooks) | 45 | 2 | 43 | 0 | -4.83 | 5 | 2.35 | 0 |  | 37 | 0.54 | 13 |
| M04 BB Squeeze Breakout | 43 | 3 | 40 | 33 | 0.88 | 2 | 2.90 | 0 |  | 36 | 4.96 | 32 |
| M147 Improved Three-Bar Pullback | 43 | 0 | 43 |  |  |  | -0.76 | 0 |  | 31 | 91.01 | 442 |
| M10 EMA3 + CCI + MACD | 42 | 2 | 40 | 0 | -5.36 | 1 | 2.37 | 0 |  | 33 | 4.70 | 54 |
| M127 Slingshot Bullish | 42 | 11 | 31 | 0 | -1.95 | 2 | 2.85 | 0 |  | 19 | 2.60 | 16 |
| M11 NR7 Breakout + Volume | 41 | 20 | 21 | 35 | -0.75 | 2 | 2.38 | 0 |  | 36 | 2.86 | 20 |
| M28 VWAP Separator + Kiss Pivot | 40 | 32 | 8 | 6 | -5.01 | 2 | -1.62 | 0 |  | 43 | 0.22 | 5 |
| M149 3-Step Pullback | 40 | 0 | 40 |  |  |  | 2.33 | 0 |  | 19 | 59.37 | 273 |
| M151 Outside Bar Failure | 34 | 4 | 30 | 0 | -3.64 | 2 | 2.93 | 0 |  | 27 | 1.93 | 26 |
| M122 Moving Momentum (ChartSchool) | 33 | 14 | 19 | 0 | -5.18 | 3 | 1.85 | 0 |  | 35 | 1.79 | 24 |
| M01 Bollinger Band + RSI | 32 | 0 | 32 |  |  |  | -0.09 | 0 |  | 67 | 2.22 | 22 |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | 32 | 1 | 31 | 0 | -7.45 | 2 | 2.11 | 0 |  | 46 | 1.32 | 29 |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | 32 | 0 | 32 |  |  |  | 2.33 | 0 |  | 51 | 1.31 | 19 |
| M74 Lulus Baharu Trend Template Minervini | 31 | 15 | 16 | 0 | -1.84 | 2 | 5.20 | 0 |  | 24 | 2.72 | 20 |
| M78 Alvarez Pecahan Mingguan DTAYS | 30 | 1 | 29 | 0 | -8.00 | 4 | 5.67 | 0 |  | 32 | 3.17 | 40 |
| M160 Measured Move Up | 30 | 18 | 12 | 6 | -2.26 | 2 | 5.16 | 0 |  | 32 | 0.44 | 8 |
| M23 Breitstein Kapitulasi + Kesinambungan | 29 | 9 | 20 | 0 | -1.90 | 1 | 2.99 | 0 |  | 22 | 0.55 | 10 |
| M146 3-Bar Momentum Pattern | 29 | 2 | 27 | 0 | -5.78 | 2 | 2.49 | 0 |  | 27 | 2.66 | 26 |
| M06 Minervini VCP Breakout | 28 | 1 | 27 | 0 | -7.08 | 3 | 2.34 | 0 |  | 33 | 2.49 | 29 |
| M154 HOLP (High of Low Period) | 28 | 5 | 23 | 0 | -8.41 | 2 | 0.49 | 0 |  | 39 | 1.93 | 27 |
| M90 Pring KST | 27 | 2 | 25 | 0 | -5.75 | 2 | 2.90 | 0 |  | 30 | 1.95 | 26 |
| M101 Bulkowski: Tiga lembah menaik | 27 | 0 | 27 |  |  |  | 2.93 | 0 |  | 35 | 3.46 | 33 |
| M32 Momentum Burst | 25 | 6 | 19 | 0 | -4.73 | 2 | 9.00 | 0 |  | 25 | 3.57 | 22 |
| M117 Landry Pullback (high 2 bulan) | 24 | 0 | 24 |  |  |  | 0.89 | 0 |  | 21 | 45.52 | 287 |
| M133 Bull Hook (Crabel) | 21 | 3 | 18 | 0 | -4.75 | 3 | 4.10 | 0 |  | 41 | 0.68 | 10 |
| M152 Spike & Ledge | 21 | 0 | 21 |  |  |  | 3.60 | 0 |  | 52 | 3.20 | 36 |
| M76 Undercut & Rally pada Low Penting | 20 | 14 | 6 | 14 | -2.53 | 3 | 1.42 | 0 |  | 37 | 0.67 | 9 |
| M29 EMA3 + RSI75 + Stokastik | 18 | 11 | 7 | 0 | -2.04 | 1 | 2.43 | 0 |  | 18 | 3.22 | 35 |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | 17 | 9 | 8 | 56 | -0.73 | 2 | 1.61 | 0 |  | 50 | 5.17 | 39 |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | 17 | 6 | 11 | 0 | -3.80 | 2 | 1.32 | 0 |  | 25 | 2.69 | 15 |
| M05 MACD Divergence + Pengesahan | 16 | 1 | 15 | 0 | -6.65 | 6 | 1.14 | 0 |  | 35 | 10.85 | 108 |
| M118 Expansion Pivot (Cooper) | 16 | 2 | 14 | 0 | -3.79 | 2 | 2.86 | 0 |  | 33 | 1.56 | 27 |
| M115 Bow Tie (Landry) | 15 | 1 | 14 | 0 | -2.66 | 3 | 2.23 | 0 |  | 27 | 1.06 | 18 |
| M134 First Kiss After Daylight (Landry) | 15 | 0 | 15 |  |  |  | 2.63 | 0 |  | 34 | 5.41 | 35 |
| M129 Wick Play | 14 | 0 | 14 |  |  |  | 2.79 | 0 |  | 38 | 2.60 | 38 |
| M91 Stochastic Pop (Bernstein/Steckler) | 13 | 0 | 13 |  |  |  | 2.44 | 0 |  | 42 | 1.63 | 18 |
| M59 Anjakan Julat RSI | 12 | 1 | 11 | 0 | -6.92 | 3 | 3.56 | 0 |  | 34 | 3.10 | 37 |
| M09 Volumatic VIDYA Pivot Retest | 11 | 4 | 7 | 25 | -3.91 | 3 | 1.78 | 0 |  | 23 | 1.85 | 30 |
| M68 Kell Base n' Break | 11 | 1 | 10 | 0 | -0.12 | 1 | 2.33 | 0 |  | 36 | 1.35 | 35 |
| M88 O'Neil Shakeout +3 | 11 | 2 | 9 | 0 | -8.00 | 6 | 5.09 | 0 |  | 32 | 5.56 | 32 |
| M48 Cooper 1-2-3-4 | 10 | 0 | 10 |  |  |  | 0.78 | 0 |  | 34 | 2.79 | 30 |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | 10 | 1 | 9 | 0 | -9.63 | 5 | 5.34 | 0 |  | 30 | 1.90 | 24 |
| M141 First Thrust (Landry) | 10 | 0 | 10 |  |  |  | 0.69 | 0 |  | 39 | 4.05 | 37 |
| M107 Golden Cross SMA50/200 | 9 | 0 | 9 |  |  |  | 3.01 | 0 |  | 32 | 15.43 | 110 |
| M126 Hidden Smash Day (beli, Larry Williams) | 9 | 0 | 9 |  |  |  | 2.22 | 0 |  | 35 | 5.15 | 33 |
| M120 Reversal New Highs | 7 | 0 | 7 |  |  |  | 2.60 | 0 |  | 27 | 1.15 | 28 |
| M140 猎豹出击 (Serangan Cheetah) | 7 | 1 | 6 | 0 | -7.20 | 2 | 1.00 | 0 |  | 36 | 5.31 | 25 |
| M44 Tapak Rata IBD | 6 | 0 | 6 |  |  |  | 1.29 | 0 |  | 30 | 0.39 | 28 |
| M87 IBD Tapak Menaik | 6 | 0 | 6 |  |  |  | 3.12 | 0 |  | 32 | 3.49 | 30 |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | 5 | 0 | 5 |  |  |  | -0.93 | 0 |  | 25 | 92.22 | 261 |
| M121 High 2 bull flag (Brooks) | 4 | 0 | 4 |  |  |  | 1.47 | 0 |  | 47 | 2.47 | 49 |
| M38 Darvas Kotak | 3 | 0 | 3 |  |  |  | 6.00 | 0 |  | 49 | 18.79 | 210 |
| M41 FW Penyatuan Mingguan | 3 | 0 | 3 |  |  |  | 2.80 | 0 |  | 36 | 15.03 | 117 |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | 3 | 0 | 3 |  |  |  | 1.75 | 0 |  | 23 | 2.81 | 22 |
| M142 Pecahan volum dari dasar (底部放量) | 3 | 0 | 3 |  |  |  | 0.17 | 0 |  | 41 | 6.85 | 44 |
| M47 Holy Grail Raschke | 2 | 1 | 1 | 0 | -16.97 | 2 | -2.70 | 0 |  | 51 | 0.25 | 5 |
| M64 O'Neil Tiga Minggu Ketat | 2 | 0 | 2 |  |  |  | 2.34 | 0 |  | 34 | 1.68 | 31 |
| M135 3rd Watch | 2 | 0 | 2 |  |  |  | 2.78 | 0 |  | 39 | 2.05 | 35 |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | 2 | 0 | 2 |  |  |  | 1.11 | 0 |  | 52 | 0.83 | 18 |
| M07 Qullamaggie Breakout | 1 | 0 | 1 |  |  |  | -0.47 | 0 |  | 20 | 1.05 | 8 |
| M144 Screw Bar | 1 | 1 | 0 | 100 | 4.10 | 2 |  | 0 |  | 41 | 7.68 | 23 |
| M157 Consolidation Pivot Breakout (versi angka) | 1 | 0 | 1 |  |  |  | -1.64 | 0 |  | 14 | 32.05 | 179 |
| M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | 0 | 0 | 0 |  |  |  |  | 0 |  | 26 | 2.57 | 8 |
| M22 Qullamaggie Episodic Pivot | 0 | 0 | 0 |  |  |  |  | 0 |  | 40 | 3.35 | 8 |
| M24 Rotasi Momentum ROC12 + SMA200 | 0 | 0 | 0 |  |  |  |  | 0 |  | 54 | 28.88 | 65 |
| M37 Weinstein Peringkat 2 | 0 | 0 | 0 |  |  |  |  | 0 |  | 41 | 5.49 | 42 |
| M40 Clenow Stocks on the Move | 0 | 0 | 0 |  |  |  |  | 0 |  | 38 | 4.80 | 35 |
| M45 High 52 Minggu (George & Hwang) | 0 | 0 | 0 |  |  |  |  | 0 |  | 32 | 12.81 | 61 |
| M51 O'Neil Cawan & Pemegang | 0 | 0 | 0 |  |  |  |  | 0 |  | 39 | 3.12 | 35 |
| M52 Radge Weekend Trend Trader | 0 | 0 | 0 |  |  |  |  | 0 |  | 37 | 5.19 | 37 |
| M56 Gray & Vogel Momentum Lancar (FIP) | 0 | 0 | 0 |  |  |  |  | 0 |  | 43 | 19.93 | 72 |
| M84 Jarak purata bergerak MAD 21/200 | 0 | 0 | 0 |  |  |  |  | 0 |  | 37 | 3.71 | 26 |
| M94 Pecutan Momentum (Chen, Yu & Wang) | 0 | 0 | 0 |  |  |  |  | 0 |  | 63 | 24.04 | 121 |
| M96 Momo India: Ranking Sharpe 3/6/12 bulan | 0 | 0 | 0 |  |  |  |  | 0 |  | 43 | 12.18 | 54 |
| M104 High Tight Flag / Power Play | 0 | 0 | 0 |  |  |  |  | 0 |  | 35 | 5.62 | 33 |
| M138 直升机空中加油 (Helikopter isi minyak di udara) | 0 | 0 | 0 |  |  |  |  | 0 |  | 45 | 4.60 | 46 |
