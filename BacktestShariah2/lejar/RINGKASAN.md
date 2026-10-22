# Lejar Penuh — ringkasan setiap kaedah

Dijana oleh `standard/lejar.py ringkas`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-21. 7179 posisi (1040 tutup lorong 1, 6139 terbuka). Semua isyarat setiap kaedah dibeli pada buka rasmi esok dengan peraturan sama (tiada had sekaedah). Jangkaan = registry set 431 varian modul (dalam sampel).

Nota: data awal didominasi posisi yang tutup cepat (kebanyakan kena henti); nilai hanya selepas posisi matang (lihat `WFO/README.md`, penilaian 15 Jan 2027).

Dua lorong keluar (sejak 17 Okt 2026): Tutup/Menang/Purata tutup = lorong 1 (peraturan kaedah); Selagi naik = lorong 2 (pegang selagi naik, sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14, paras hanya naik, tanpa henti kaedah). n = bilangan keluar.

| Kaedah | Posisi | Tutup | Terbuka | Menang % | Purata tutup % | Hari | Purata terbuka % | Selagi naik n | Purata selagi naik % | Menang jangka % | Purata jangka % | Hari jangka |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M159 Heikin-Ashi Trend | 457 | 104 | 353 | 12 | -2.05 | 2 | 0.77 | 0 |  | 40 | 0.17 | 6 |
| M125 2-Bar Breakout | 389 | 8 | 381 | 0 | -8.85 | 3 | 0.97 | 0 |  | 30 | 166.86 | 443 |
| M153 Range Leader | 375 | 86 | 289 | 24 | -1.46 | 2 | 0.95 | 0 |  | 43 | 0.18 | 6 |
| M82 Arthur Hill Rotasi Sasaran 10% | 352 | 14 | 338 | 57 | 3.53 | 3 | 0.63 | 0 |  | 61 | 1.84 | 38 |
| M14 Walking with the Whales | 337 | 97 | 240 | 6 | -2.91 | 2 | 2.15 | 0 |  | 21 | 1.52 | 15 |
| M155 Market Cycle Strategy | 247 | 3 | 244 | 0 | -9.16 | 3 | 0.45 | 0 |  | 49 | 1.56 | 17 |
| M27 Price Action 4 Tiang | 207 | 101 | 106 | 21 | -1.90 | 2 | 1.77 | 0 |  | 35 | 0.36 | 7 |
| M136 Short/Intermediate-term Low (Larry Williams) | 204 | 1 | 203 | 0 | -7.80 | 3 | 0.24 | 0 |  | 24 | 112.90 | 343 |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | 190 | 61 | 129 | 85 | 1.78 | 2 | 0.48 | 0 |  | 63 | 0.18 | 5 |
| M116 2/20 EMA Breakout (Landry) | 187 | 2 | 185 | 0 | -9.16 | 4 | 1.01 | 0 |  | 50 | 0.40 | 9 |
| M13 Garis Trend Action/Safety Line | 181 | 41 | 140 | 0 | -2.59 | 2 | 0.76 | 0 |  | 34 | 0.97 | 11 |
| M81 Bensdorp Long Trend High Momentum | 180 | 0 | 180 |  |  |  | 0.85 | 0 |  | 32 | 8.56 | 105 |
| M50 Elder Triple Screen | 149 | 35 | 114 | 0 | -3.63 | 2 | 1.05 | 0 |  | 23 | 1.80 | 18 |
| M31 Band Walk (BB 20/2) | 140 | 0 | 140 |  |  |  | 0.52 | 0 |  | 43 | 3.30 | 32 |
| M92 CCI-50 | 139 | 8 | 131 | 0 | -3.76 | 3 | 0.36 | 0 |  | 49 | 1.17 | 13 |
| M158 Doubly Adaptive Profit Targets | 136 | 10 | 126 | 30 | -1.51 | 2 | 3.15 | 0 |  | 34 | 2.94 | 30 |
| M03 BB Break + Divergence RSI | 130 | 57 | 73 | 60 | 0.42 | 3 | -0.76 | 0 |  | 56 | 0.58 | 8 |
| M161 EMA 10/21 + Supertrend (10,3) | 130 | 9 | 121 | 0 | -4.03 | 3 | 1.36 | 0 |  | 35 | 1.43 | 18 |
| M20 EMA10/15 Crossover + Sudut | 113 | 31 | 82 | 16 | -2.30 | 2 | 1.10 | 0 |  | 39 | 0.22 | 7 |
| M102 Stockbee SLTB | 102 | 34 | 68 | 0 | -3.35 | 2 | 2.55 | 0 |  | 18 | 1.34 | 16 |
| M15 Break & Retest + Henti ATR | 92 | 16 | 76 | 0 | -3.96 | 3 | 0.56 | 0 |  | 33 | 1.08 | 12 |
| M70 Pecahan Hari Dalam | 90 | 31 | 59 | 0 | -1.16 | 1 | 3.24 | 0 |  | 11 | 0.84 | 10 |
| M105 Supertrend tulen | 87 | 1 | 86 | 0 | -9.85 | 3 | 0.48 | 0 |  | 39 | 2.44 | 32 |
| M145 Yum-Yum Continuation | 87 | 0 | 87 |  |  |  | 0.83 | 0 |  | 25 | 80.48 | 356 |
| M93 Bollinger Kaedah II: %b + MFI | 84 | 7 | 77 | 0 | -4.37 | 2 | 1.84 | 0 |  | 36 | 8.20 | 62 |
| M36 Turtle 55/20 | 83 | 1 | 82 | 0 | -5.61 | 4 | 1.18 | 0 |  | 32 | 2.65 | 30 |
| M124 'Last' Stochastic Technique (ChartSchool) | 79 | 2 | 77 | 0 | -6.15 | 4 | 0.83 | 0 |  | 36 | 1.74 | 20 |
| M35 Pocket Pivot Morales & Kacher | 77 | 24 | 53 | 0 | -2.22 | 2 | 2.10 | 0 |  | 28 | 0.29 | 9 |
| M19 Sneaky Pivot (proksi harian) | 71 | 7 | 64 | 43 | -2.10 | 3 | 0.01 | 0 |  | 44 | 0.27 | 11 |
| M18 EMA9/21 Pullback | 68 | 22 | 46 | 23 | -3.54 | 2 | 2.63 | 0 |  | 26 | 0.40 | 7 |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | 64 | 17 | 47 | 0 | -1.62 | 1 | 1.51 | 0 |  | 23 | 3.99 | 34 |
| M30 BB Free Bar + Himpitan 50/2.5 | 63 | 5 | 58 | 0 | -2.60 | 2 | 1.42 | 0 |  | 37 | 3.80 | 34 |
| M111 Sistem Volatiliti Wilder | 62 | 0 | 62 |  |  |  | 0.98 | 0 |  | 39 | 2.39 | 30 |
| M131 Ross Hook (Joe Ross) | 62 | 3 | 59 | 0 | -8.04 | 2 | 0.65 | 0 |  | 30 | 2.35 | 30 |
| M80 Radge Saluran Purata Bergerak (MAC) | 59 | 1 | 58 | 0 | -8.41 | 2 | 0.91 | 0 |  | 36 | 8.91 | 66 |
| M54 IBD Power Trend | 56 | 1 | 55 | 0 | -5.61 | 4 | 1.29 | 0 |  | 30 | 3.37 | 37 |
| M66 IBD Undur Pertama ke Purata 50 Hari | 56 | 8 | 48 | 0 | -3.22 | 2 | 2.17 | 0 |  | 28 | 1.71 | 19 |
| M55 Guppy GMMA | 55 | 6 | 49 | 0 | -3.65 | 2 | 1.74 | 0 |  | 26 | 2.71 | 28 |
| M156 Single Penetration (DiNapoli) | 54 | 0 | 54 |  |  |  | 1.95 | 0 |  | 52 | 0.69 | 9 |
| M33 Supertrend + SMA10 | 52 | 0 | 52 |  |  |  | 0.64 | 0 |  | 40 | 1.65 | 33 |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | 47 | 2 | 45 | 0 | -3.10 | 2 | 1.54 | 0 |  | 34 | 0.55 | 12 |
| M137 Livermore System | 47 | 0 | 47 |  |  |  | 1.60 | 0 |  | 35 | 4.22 | 37 |
| M123 CCI Correction (Lambert, ChartSchool) | 46 | 32 | 14 | 3 | -1.72 | 2 | 0.21 | 0 |  | 28 | 0.92 | 10 |
| M39 Radge Pecahan Bollinger 100 hari | 44 | 0 | 44 |  |  |  | 0.95 | 0 |  | 37 | 9.11 | 96 |
| M148 Natural Number Method | 44 | 3 | 41 | 0 | -4.16 | 1 | 0.73 | 0 |  | 35 | 0.50 | 10 |
| M12 Parabolic SAR | 43 | 8 | 35 | 0 | -3.49 | 3 | 0.96 | 0 |  | 29 | 2.04 | 23 |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | 41 | 0 | 41 |  |  |  | 0.80 | 0 |  | 32 | 2.68 | 29 |
| M150 Trend Bar Failure (Brooks) | 40 | 0 | 40 |  |  |  | 0.01 | 0 |  | 37 | 0.54 | 13 |
| M28 VWAP Separator + Kiss Pivot | 39 | 19 | 20 | 5 | -4.56 | 2 | 1.74 | 0 |  | 43 | 0.22 | 5 |
| M89 Chande 65sma-3cc | 39 | 1 | 38 | 0 | -5.68 | 2 | 1.73 | 0 |  | 34 | 1.83 | 26 |
| M34 Carter TTM Squeeze | 38 | 0 | 38 |  |  |  | 1.67 | 0 |  | 34 | 2.38 | 30 |
| M57 Landry Trend Knockout (TKO) | 36 | 9 | 27 | 0 | -4.74 | 2 | 2.31 | 0 |  | 21 | 1.55 | 18 |
| M99 Three Line Break | 36 | 5 | 31 | 0 | -3.90 | 1 | 1.96 | 0 |  | 40 | 1.17 | 16 |
| M119 180 Bullish (Cooper) | 36 | 1 | 35 | 0 | -2.33 | 1 | 0.79 | 0 |  | 27 | 1.17 | 18 |
| M08 SMA20 + SMA200 | 35 | 12 | 23 | 17 | -4.20 | 2 | 2.21 | 0 |  | 32 | 1.07 | 12 |
| M79 Radge: 20% Flipper | 35 | 0 | 35 |  |  |  | 0.17 | 0 |  | 40 | 6.25 | 60 |
| M147 Improved Three-Bar Pullback | 35 | 0 | 35 |  |  |  | -0.37 | 0 |  | 31 | 91.01 | 442 |
| M132 Ascending Scallop (Bulkowski) | 33 | 0 | 33 |  |  |  | 1.48 | 0 |  | 42 | 0.98 | 29 |
| M11 NR7 Breakout + Volume | 32 | 11 | 21 | 36 | -0.51 | 2 | 1.21 | 0 |  | 36 | 2.86 | 20 |
| M02 MACD + SMA200 | 31 | 6 | 25 | 0 | -2.66 | 2 | -0.10 | 0 |  | 44 | 0.66 | 14 |
| M78 Alvarez Pecahan Mingguan DTAYS | 30 | 0 | 30 |  |  |  | 2.91 | 0 |  | 32 | 3.17 | 40 |
| M106 DMI Wilder | 28 | 7 | 21 | 0 | -2.36 | 3 | 0.51 | 0 |  | 32 | 1.01 | 12 |
| M122 Moving Momentum (ChartSchool) | 26 | 6 | 20 | 0 | -3.57 | 2 | -0.31 | 0 |  | 35 | 1.79 | 24 |
| M127 Slingshot Bullish | 26 | 7 | 19 | 0 | -1.81 | 1 | 1.09 | 0 |  | 19 | 2.60 | 16 |
| M10 EMA3 + CCI + MACD | 24 | 0 | 24 |  |  |  | 1.01 | 0 |  | 33 | 4.70 | 54 |
| M32 Momentum Burst | 24 | 5 | 19 | 0 | -4.65 | 2 | 4.87 | 0 |  | 25 | 3.57 | 22 |
| M25 VWAP Wave (proksi harian) | 23 | 0 | 23 |  |  |  | 3.60 | 0 |  | 30 | 0.42 | 10 |
| M149 3-Step Pullback | 23 | 0 | 23 |  |  |  | 0.85 | 0 |  | 19 | 59.37 | 273 |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | 22 | 0 | 22 |  |  |  | 0.80 | 0 |  | 51 | 1.31 | 19 |
| M74 Lulus Baharu Trend Template Minervini | 21 | 7 | 14 | 0 | -1.89 | 1 | 2.02 | 0 |  | 24 | 2.72 | 20 |
| M04 BB Squeeze Breakout | 20 | 1 | 19 | 0 | 0.00 | 2 | 1.80 | 0 |  | 36 | 4.96 | 32 |
| M151 Outside Bar Failure | 19 | 1 | 18 | 0 | -7.15 | 2 | 0.48 | 0 |  | 27 | 1.93 | 26 |
| M152 Spike & Ledge | 18 | 0 | 18 |  |  |  | 1.46 | 0 |  | 52 | 3.20 | 36 |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | 17 | 0 | 17 |  |  |  | 1.34 | 0 |  | 46 | 1.32 | 29 |
| M06 Minervini VCP Breakout | 16 | 0 | 16 |  |  |  | 0.58 | 0 |  | 33 | 2.49 | 29 |
| M76 Undercut & Rally pada Low Penting | 16 | 7 | 9 | 0 | -2.85 | 2 | 0.56 | 0 |  | 37 | 0.67 | 9 |
| M90 Pring KST | 16 | 1 | 15 | 0 | -3.11 | 3 | 2.34 | 0 |  | 30 | 1.95 | 26 |
| M23 Breitstein Kapitulasi + Kesinambungan | 14 | 7 | 7 | 0 | -2.14 | 1 | 2.16 | 0 |  | 22 | 0.55 | 10 |
| M154 HOLP (High of Low Period) | 14 | 1 | 13 | 0 | -7.00 | 4 | 1.03 | 0 |  | 39 | 1.93 | 27 |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | 13 | 2 | 11 | 0 | -3.93 | 1 | -0.08 | 0 |  | 25 | 2.69 | 15 |
| M101 Bulkowski: Tiga lembah menaik | 13 | 0 | 13 |  |  |  | 1.56 | 0 |  | 35 | 3.46 | 33 |
| M117 Landry Pullback (high 2 bulan) | 13 | 0 | 13 |  |  |  | 0.05 | 0 |  | 21 | 45.52 | 287 |
| M146 3-Bar Momentum Pattern | 13 | 0 | 13 |  |  |  | 2.06 | 0 |  | 27 | 2.66 | 26 |
| M01 Bollinger Band + RSI | 12 | 0 | 12 |  |  |  | -0.31 | 0 |  | 67 | 2.22 | 22 |
| M133 Bull Hook (Crabel) | 12 | 1 | 11 | 0 | -2.31 | 2 | 4.12 | 0 |  | 41 | 0.68 | 10 |
| M160 Measured Move Up | 12 | 4 | 8 | 0 | -3.25 | 2 | 5.87 | 0 |  | 32 | 0.44 | 8 |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | 11 | 5 | 6 | 80 | 0.76 | 3 | 0.80 | 0 |  | 50 | 5.17 | 39 |
| M134 First Kiss After Daylight (Landry) | 11 | 0 | 11 |  |  |  | 0.72 | 0 |  | 34 | 5.41 | 35 |
| M115 Bow Tie (Landry) | 10 | 0 | 10 |  |  |  | 0.72 | 0 |  | 27 | 1.06 | 18 |
| M141 First Thrust (Landry) | 10 | 0 | 10 |  |  |  | -0.18 | 0 |  | 39 | 4.05 | 37 |
| M59 Anjakan Julat RSI | 9 | 0 | 9 |  |  |  | 1.36 | 0 |  | 34 | 3.10 | 37 |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | 9 | 0 | 9 |  |  |  | 3.73 | 0 |  | 30 | 1.90 | 24 |
| M09 Volumatic VIDYA Pivot Retest | 8 | 3 | 5 | 33 | -3.57 | 2 | -0.26 | 0 |  | 23 | 1.85 | 30 |
| M29 EMA3 + RSI75 + Stokastik | 8 | 7 | 1 | 0 | -1.94 | 1 | 1.57 | 0 |  | 18 | 3.22 | 35 |
| M88 O'Neil Shakeout +3 | 8 | 0 | 8 |  |  |  | 0.15 | 0 |  | 32 | 5.56 | 32 |
| M118 Expansion Pivot (Cooper) | 8 | 1 | 7 | 0 | -3.83 | 2 | 1.64 | 0 |  | 33 | 1.56 | 27 |
| M05 MACD Divergence + Pengesahan | 7 | 0 | 7 |  |  |  | -1.68 | 0 |  | 35 | 10.85 | 108 |
| M107 Golden Cross SMA50/200 | 7 | 0 | 7 |  |  |  | 2.95 | 0 |  | 32 | 15.43 | 110 |
| M129 Wick Play | 7 | 0 | 7 |  |  |  | 2.15 | 0 |  | 38 | 2.60 | 38 |
| M48 Cooper 1-2-3-4 | 6 | 0 | 6 |  |  |  | 2.64 | 0 |  | 34 | 2.79 | 30 |
| M68 Kell Base n' Break | 6 | 1 | 5 | 0 | -0.12 | 1 | 1.76 | 0 |  | 36 | 1.35 | 35 |
| M91 Stochastic Pop (Bernstein/Steckler) | 6 | 0 | 6 |  |  |  | 1.96 | 0 |  | 42 | 1.63 | 18 |
| M126 Hidden Smash Day (beli, Larry Williams) | 6 | 0 | 6 |  |  |  | 0.54 | 0 |  | 35 | 5.15 | 33 |
| M87 IBD Tapak Menaik | 5 | 0 | 5 |  |  |  | 1.40 | 0 |  | 32 | 3.49 | 30 |
| M120 Reversal New Highs | 5 | 0 | 5 |  |  |  | 1.24 | 0 |  | 27 | 1.15 | 28 |
| M38 Darvas Kotak | 3 | 0 | 3 |  |  |  | 1.89 | 0 |  | 49 | 18.79 | 210 |
| M41 FW Penyatuan Mingguan | 3 | 0 | 3 |  |  |  | 1.67 | 0 |  | 36 | 15.03 | 117 |
| M44 Tapak Rata IBD | 3 | 0 | 3 |  |  |  | -1.78 | 0 |  | 30 | 0.39 | 28 |
| M47 Holy Grail Raschke | 2 | 1 | 1 | 0 | -16.97 | 2 | -0.09 | 0 |  | 51 | 0.25 | 5 |
| M135 3rd Watch | 2 | 0 | 2 |  |  |  | 1.17 | 0 |  | 39 | 2.05 | 35 |
| M140 猎豹出击 (Serangan Cheetah) | 2 | 1 | 1 | 0 | -7.20 | 2 | -1.32 | 0 |  | 36 | 5.31 | 25 |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | 2 | 0 | 2 |  |  |  | -0.90 | 0 |  | 52 | 0.83 | 18 |
| M07 Qullamaggie Breakout | 1 | 0 | 1 |  |  |  | 2.61 | 0 |  | 20 | 1.05 | 8 |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | 1 | 0 | 1 |  |  |  | -0.66 | 0 |  | 23 | 2.81 | 22 |
| M64 O'Neil Tiga Minggu Ketat | 1 | 0 | 1 |  |  |  | 0.79 | 0 |  | 34 | 1.68 | 31 |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | 1 | 0 | 1 |  |  |  | 2.43 | 0 |  | 25 | 92.22 | 261 |
| M142 Pecahan volum dari dasar (底部放量) | 1 | 0 | 1 |  |  |  | -2.20 | 0 |  | 41 | 6.85 | 44 |
| M144 Screw Bar | 1 | 1 | 0 | 100 | 4.10 | 2 |  | 0 |  | 41 | 7.68 | 23 |
| M157 Consolidation Pivot Breakout (versi angka) | 1 | 0 | 1 |  |  |  | -3.25 | 0 |  | 14 | 32.05 | 179 |
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
| M121 High 2 bull flag (Brooks) | 0 | 0 | 0 |  |  |  |  | 0 |  | 47 | 2.47 | 49 |
| M138 直升机空中加油 (Helikopter isi minyak di udara) | 0 | 0 | 0 |  |  |  |  | 0 |  | 45 | 4.60 | 46 |
