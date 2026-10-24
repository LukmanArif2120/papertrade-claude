# Analisis prestasi sebenar Papertrade C lawan jangkaan backtest

Dijana oleh `WFO/kod/analisis_sebenar.py`. Sumber: semua `papertrade/claude*.csv` (5525 posisi sah; 1366 tutup, 4159 terbuka; 2026-10-08 hingga 2026-10-23). Jangkaan = registry set 431 bagi varian modul (dalam sampel bagi M115–M161).

Ujian hanya atas posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan dan >= 14 hari lalu; tutup = untung akhir, terbuka = untung semasa) untuk elak bias pemilihan (yang tutup awal kebanyakannya kena henti). Ambang: >= 10 posisi matang. AMARAN = kadar menang (z) atau purata (t) < −2 berbanding jangkaan.

**Ringkasan:** 0 AMARAN, 1 SELARI, 121 data belum cukup.

| Kaedah | Status | n | Matang | Menang matang | Menang jangka | Purata matang % | Purata jangka % | Hari jangka | Tutup (awal) | Purata tutup % | Terbuka purata % | z | t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M03 BB Break + Divergence RSI | DATA BELUM CUKUP | 105 | 0 |  | 56% |  | 0.58 | 8 | 81 | 0.97 | -0.70 |  |  |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | DATA BELUM CUKUP | 102 | 9 | 22% | 63% | -3.55 | 0.18 | 5 | 80 | 0.58 | -4.15 |  |  |
| M14 Walking with the Whales | DATA BELUM CUKUP | 103 | 0 |  | 21% |  | 1.52 | 15 | 60 | -2.24 | 5.42 |  |  |
| M18 EMA9/21 Pullback | DATA BELUM CUKUP | 99 | 0 |  | 26% |  | 0.40 | 7 | 54 | -1.58 | 5.57 |  |  |
| M102 Stockbee SLTB | DATA BELUM CUKUP | 101 | 0 |  | 18% |  | 1.34 | 16 | 45 | -3.05 | 6.42 |  |  |
| M08 SMA20 + SMA200 | DATA BELUM CUKUP | 73 | 0 |  | 32% |  | 1.07 | 12 | 43 | -3.39 | 3.89 |  |  |
| M70 Pecahan Hari Dalam | DATA BELUM CUKUP | 82 | 0 |  | 11% |  | 0.84 | 10 | 43 | -1.80 | 7.98 |  |  |
| M19 Sneaky Pivot (proksi harian) | DATA BELUM CUKUP | 84 | 0 |  | 44% |  | 0.27 | 11 | 39 | -3.72 | 1.75 |  |  |
| M35 Pocket Pivot Morales & Kacher | DATA BELUM CUKUP | 90 | 0 |  | 28% |  | 0.29 | 9 | 37 | -2.46 | 5.31 |  |  |
| M13 Garis Trend Action/Safety Line | DATA BELUM CUKUP | 104 | 0 |  | 34% |  | 0.97 | 11 | 34 | -3.70 | 4.13 |  |  |
| M123 CCI Correction (Lambert, ChartSchool) | DATA BELUM CUKUP | 47 | 0 |  | 28% |  | 0.92 | 10 | 33 | -1.76 | 2.66 |  |  |
| M15 Break & Retest + Henti ATR | DATA BELUM CUKUP | 106 | 0 |  | 33% |  | 1.08 | 12 | 32 | -3.79 | 3.39 |  |  |
| M27 Price Action 4 Tiang | DATA BELUM CUKUP | 56 | 5 | 40% | 35% | 0.70 | 0.36 | 7 | 30 | -1.85 | 7.58 |  |  |
| M66 IBD Undur Pertama ke Purata 50 Hari | DATA BELUM CUKUP | 87 | 0 |  | 28% |  | 1.71 | 19 | 30 | -3.13 | 4.79 |  |  |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | DATA BELUM CUKUP | 94 | 0 |  | 23% |  | 3.99 | 34 | 29 | -3.21 | 5.43 |  |  |
| M57 Landry Trend Knockout (TKO) | DATA BELUM CUKUP | 65 | 0 |  | 21% |  | 1.55 | 18 | 29 | -4.93 | 2.73 |  |  |
| M55 Guppy GMMA | DATA BELUM CUKUP | 84 | 0 |  | 26% |  | 2.71 | 28 | 25 | -5.31 | 4.69 |  |  |
| M99 Three Line Break | DATA BELUM CUKUP | 73 | 0 |  | 40% |  | 1.17 | 16 | 25 | -3.09 | 5.65 |  |  |
| M12 Parabolic SAR | DATA BELUM CUKUP | 80 | 0 |  | 29% |  | 2.04 | 23 | 23 | -4.00 | 5.16 |  |  |
| M50 Elder Triple Screen | DATA BELUM CUKUP | 37 | 0 |  | 23% |  | 1.80 | 18 | 23 | -4.71 | 5.96 |  |  |
| M74 Lulus Baharu Trend Template Minervini | DATA BELUM CUKUP | 45 | 0 |  | 24% |  | 2.72 | 20 | 23 | -2.34 | 5.51 |  |  |
| M92 CCI-50 | DATA BELUM CUKUP | 114 | 0 |  | 49% |  | 1.17 | 13 | 23 | -1.90 | 3.69 |  |  |
| M02 MACD + SMA200 | DATA BELUM CUKUP | 74 | 0 |  | 44% |  | 0.66 | 14 | 22 | -1.03 | 2.44 |  |  |
| M28 VWAP Separator + Kiss Pivot | DATA BELUM CUKUP | 26 | 0 |  | 43% |  | 0.22 | 5 | 22 | -3.71 | 0.72 |  |  |
| M11 NR7 Breakout + Volume | DATA BELUM CUKUP | 44 | 0 |  | 36% |  | 2.86 | 20 | 21 | -0.64 | 2.59 |  |  |
| M25 VWAP Wave (proksi harian) | DATA BELUM CUKUP | 64 | 0 |  | 30% |  | 0.42 | 10 | 20 | -3.53 | 5.58 |  |  |
| M76 Undercut & Rally pada Low Penting | DATA BELUM CUKUP | 26 | 0 |  | 37% |  | 0.67 | 9 | 20 | -3.13 | 2.69 |  |  |
| M81 Bensdorp Long Trend High Momentum | DATA BELUM CUKUP | 104 | 0 |  | 32% |  | 8.56 | 105 | 19 | -13.68 | 0.21 |  |  |
| M89 Chande 65sma-3cc | DATA BELUM CUKUP | 83 | 0 |  | 34% |  | 1.83 | 26 | 19 | -6.06 | 3.48 |  |  |
| M106 DMI Wilder | DATA BELUM CUKUP | 52 | 0 |  | 32% |  | 1.01 | 12 | 15 | -2.90 | 2.52 |  |  |
| M160 Measured Move Up | DATA BELUM CUKUP | 26 | 0 |  | 32% |  | 0.44 | 8 | 15 | -2.24 | 4.25 |  |  |
| M36 Turtle 55/20 | DATA BELUM CUKUP | 90 | 0 |  | 32% |  | 2.65 | 30 | 15 | -6.46 | 3.77 |  |  |
| M54 IBD Power Trend | DATA BELUM CUKUP | 88 | 0 |  | 30% |  | 3.37 | 37 | 14 | -6.89 | 4.00 |  |  |
| M90 Pring KST | DATA BELUM CUKUP | 56 | 0 |  | 30% |  | 1.95 | 26 | 14 | -5.81 | 4.88 |  |  |
| M122 Moving Momentum (ChartSchool) | DATA BELUM CUKUP | 31 | 0 |  | 35% |  | 1.79 | 24 | 13 | -4.32 | 2.04 |  |  |
| M82 Arthur Hill Rotasi Sasaran 10% | DATA BELUM CUKUP | 112 | 0 |  | 61% |  | 1.84 | 38 | 13 | 11.37 | 1.18 |  |  |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | DATA BELUM CUKUP | 21 | 0 |  | 50% |  | 5.17 | 39 | 12 | -3.30 | 1.35 |  |  |
| M29 EMA3 + RSI75 + Stokastik | DATA BELUM CUKUP | 19 | 0 |  | 18% |  | 3.22 | 35 | 12 | -2.01 | 2.43 |  |  |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | DATA BELUM CUKUP | 71 | 0 |  | 32% |  | 2.68 | 29 | 11 | -6.72 | 3.03 |  |  |
| M127 Slingshot Bullish | DATA BELUM CUKUP | 37 | 0 |  | 19% |  | 2.60 | 16 | 10 | -2.01 | 3.30 |  |  |
| M93 Bollinger Kaedah II: %b + MFI | DATA BELUM CUKUP | 107 | 0 |  | 36% |  | 8.20 | 62 | 10 | -5.02 | 4.17 |  |  |
| M148 Natural Number Method | DATA BELUM CUKUP | 43 | 0 |  | 35% |  | 0.50 | 10 | 9 | -3.68 | 1.76 |  |  |
| M23 Breitstein Kapitulasi + Kesinambungan | DATA BELUM CUKUP | 27 | 0 |  | 22% |  | 0.55 | 10 | 9 | -2.33 | 3.22 |  |  |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | DATA BELUM CUKUP | 21 | 0 |  | 25% |  | 2.69 | 15 | 9 | -3.29 | 1.57 |  |  |
| M32 Momentum Burst | DATA BELUM CUKUP | 25 | 0 |  | 25% |  | 3.57 | 22 | 7 | -3.56 | 9.37 |  |  |
| M119 180 Bullish (Cooper) | DATA BELUM CUKUP | 35 | 0 |  | 27% |  | 1.17 | 18 | 6 | -3.46 | 3.12 |  |  |
| M80 Radge Saluran Purata Bergerak (MAC) | DATA BELUM CUKUP | 110 | 0 |  | 36% |  | 8.91 | 66 | 6 | -11.70 | 4.17 |  |  |
| M04 BB Squeeze Breakout | DATA BELUM CUKUP | 36 | 0 |  | 36% |  | 4.96 | 32 | 5 | -1.64 | 2.58 |  |  |
| M10 EMA3 + CCI + MACD | DATA BELUM CUKUP | 70 | 0 |  | 33% |  | 4.70 | 54 | 5 | -5.37 | 3.79 |  |  |
| M153 Range Leader | DATA BELUM CUKUP | 46 | 0 |  | 43% |  | 0.18 | 6 | 5 | -3.14 | 3.05 |  |  |
| M159 Heikin-Ashi Trend | DATA BELUM CUKUP | 59 | 0 |  | 40% |  | 0.17 | 6 | 5 | -0.95 | 3.90 |  |  |
| M30 BB Free Bar + Himpitan 50/2.5 | DATA BELUM CUKUP | 60 | 0 |  | 37% |  | 3.80 | 34 | 5 | -1.70 | 3.69 |  |  |
| M34 Carter TTM Squeeze | DATA BELUM CUKUP | 71 | 0 |  | 34% |  | 2.38 | 30 | 5 | -3.43 | 4.98 |  |  |
| M39 Radge Pecahan Bollinger 100 hari | DATA BELUM CUKUP | 85 | 0 |  | 37% |  | 9.11 | 96 | 5 | -14.63 | 2.36 |  |  |
| M78 Alvarez Pecahan Mingguan DTAYS | DATA BELUM CUKUP | 19 | 0 |  | 32% |  | 3.17 | 40 | 5 | -8.41 | 4.12 |  |  |
| M06 Minervini VCP Breakout | DATA BELUM CUKUP | 33 | 0 |  | 33% |  | 2.49 | 29 | 4 | -7.30 | 3.09 |  |  |
| M09 Volumatic VIDYA Pivot Retest | DATA BELUM CUKUP | 12 | 0 |  | 23% |  | 1.85 | 30 | 4 | -3.90 | 2.14 |  |  |
| M124 'Last' Stochastic Technique (ChartSchool) | DATA BELUM CUKUP | 53 | 0 |  | 36% |  | 1.74 | 20 | 4 | -7.92 | 3.41 |  |  |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | DATA BELUM CUKUP | 44 | 0 |  | 34% |  | 0.55 | 12 | 4 | -3.32 | 1.88 |  |  |
| M131 Ross Hook (Joe Ross) | DATA BELUM CUKUP | 47 | 0 |  | 30% |  | 2.35 | 30 | 4 | -4.57 | 2.97 |  |  |
| M136 Short/Intermediate-term Low (Larry Williams) | DATA BELUM CUKUP | 57 | 0 |  | 24% |  | 112.90 | 343 | 4 | -6.09 | 2.08 |  |  |
| M151 Outside Bar Failure | DATA BELUM CUKUP | 34 | 0 |  | 27% |  | 1.93 | 26 | 4 | -3.63 | 2.93 |  |  |
| M01 Bollinger Band + RSI | DATA BELUM CUKUP | 34 | 0 |  | 67% |  | 2.22 | 22 | 3 | 9.12 | -0.84 |  |  |
| M105 Supertrend tulen | DATA BELUM CUKUP | 102 | 0 |  | 39% |  | 2.44 | 32 | 3 | -10.27 | 4.55 |  |  |
| M111 Sistem Volatiliti Wilder | DATA BELUM CUKUP | 92 | 0 |  | 39% |  | 2.39 | 30 | 3 | -10.83 | 4.12 |  |  |
| M158 Doubly Adaptive Profit Targets | DATA BELUM CUKUP | 53 | 0 |  | 34% |  | 2.94 | 30 | 3 | -2.85 | 4.32 |  |  |
| M31 Band Walk (BB 20/2) | DATA BELUM CUKUP | 95 | 0 |  | 43% |  | 3.30 | 32 | 3 | -15.36 | 2.39 |  |  |
| M47 Holy Grail Raschke | DATA BELUM CUKUP | 5 | 0 |  | 51% |  | 0.25 | 5 | 3 | -2.60 | 2.89 |  |  |
| M52 Radge Weekend Trend Trader | DATA BELUM CUKUP | 9 | 0 |  | 37% |  | 5.19 | 37 | 3 | -13.07 | 2.89 |  |  |
| M118 Expansion Pivot (Cooper) | DATA BELUM CUKUP | 16 | 0 |  | 33% |  | 1.56 | 27 | 2 | -3.79 | 2.86 |  |  |
| M133 Bull Hook (Crabel) | DATA BELUM CUKUP | 19 | 0 |  | 41% |  | 0.68 | 10 | 2 | -1.21 | 3.69 |  |  |
| M146 3-Bar Momentum Pattern | DATA BELUM CUKUP | 25 | 0 |  | 27% |  | 2.66 | 26 | 2 | -5.76 | 2.65 |  |  |
| M150 Trend Bar Failure (Brooks) | DATA BELUM CUKUP | 30 | 0 |  | 37% |  | 0.54 | 13 | 2 | -4.83 | 2.33 |  |  |
| M154 HOLP (High of Low Period) | DATA BELUM CUKUP | 23 | 0 |  | 39% |  | 1.93 | 27 | 2 | -7.33 | 0.75 |  |  |
| M33 Supertrend + SMA10 | DATA BELUM CUKUP | 59 | 0 |  | 40% |  | 1.65 | 33 | 2 | -12.14 | 2.79 |  |  |
| M59 Anjakan Julat RSI | DATA BELUM CUKUP | 14 | 0 |  | 34% |  | 3.10 | 37 | 2 | -4.16 | 3.51 |  |  |
| M68 Kell Base n' Break | DATA BELUM CUKUP | 12 | 0 |  | 36% |  | 1.35 | 35 | 2 | -9.03 | 3.28 |  |  |
| M79 Radge: 20% Flipper | DATA BELUM CUKUP | 54 | 0 |  | 40% |  | 6.25 | 60 | 2 | -6.11 | 1.46 |  |  |
| M88 O'Neil Shakeout +3 | DATA BELUM CUKUP | 13 | 0 |  | 32% |  | 5.56 | 32 | 2 | -8.00 | 4.22 |  |  |
| M05 MACD Divergence + Pengesahan | DATA BELUM CUKUP | 19 | 0 |  | 35% |  | 10.85 | 108 | 1 | -6.65 | 1.55 |  |  |
| M07 Qullamaggie Breakout | DATA BELUM CUKUP | 2 | 0 |  | 20% |  | 1.05 | 8 | 1 | -3.74 | -0.47 |  |  |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | DATA BELUM CUKUP | 36 | 0 |  | 46% |  | 1.32 | 29 | 1 | -7.45 | 1.98 |  |  |
| M101 Bulkowski: Tiga lembah menaik | DATA BELUM CUKUP | 35 | 0 |  | 35% |  | 3.46 | 33 | 1 | -8.64 | 2.24 |  |  |
| M115 Bow Tie (Landry) | DATA BELUM CUKUP | 14 | 0 |  | 27% |  | 1.06 | 18 | 1 | -2.66 | 2.56 |  |  |
| M125 2-Bar Breakout | DATA BELUM CUKUP | 56 | 0 |  | 30% |  | 166.86 | 443 | 1 | -4.72 | 3.73 |  |  |
| M137 Livermore System | DATA BELUM CUKUP | 48 | 0 |  | 35% |  | 4.22 | 37 | 1 | -1.03 | 3.02 |  |  |
| M140 猎豹出击 (Serangan Cheetah) | DATA BELUM CUKUP | 6 | 0 |  | 36% |  | 5.31 | 25 | 1 | -7.20 | 1.03 |  |  |
| M144 Screw Bar | DATA BELUM CUKUP | 1 | 0 |  | 41% |  | 7.68 | 23 | 1 | 4.10 |  |  |  |
| M156 Single Penetration (DiNapoli) | DATA BELUM CUKUP | 51 | 0 |  | 52% |  | 0.69 | 9 | 1 | -9.97 | 2.21 |  |  |
| M161 EMA 10/21 + Supertrend (10,3) | DATA BELUM CUKUP | 58 | 0 |  | 35% |  | 1.43 | 18 | 1 | -6.26 | 1.86 |  |  |
| M44 Tapak Rata IBD | DATA BELUM CUKUP | 9 | 0 |  | 30% |  | 0.39 | 28 | 1 | -8.00 | 2.61 |  |  |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | DATA BELUM CUKUP | 11 | 0 |  | 30% |  | 1.90 | 24 | 1 | -9.63 | 4.71 |  |  |
| M91 Stochastic Pop (Bernstein/Steckler) | DATA BELUM CUKUP | 16 | 0 |  | 42% |  | 1.63 | 18 | 1 | -10.18 | 2.64 |  |  |
| M107 Golden Cross SMA50/200 | DATA BELUM CUKUP | 10 | 0 |  | 32% |  | 15.43 | 110 | 0 |  | 4.37 |  |  |
| M116 2/20 EMA Breakout (Landry) | DATA BELUM CUKUP | 58 | 0 |  | 50% |  | 0.40 | 9 | 0 |  | 2.55 |  |  |
| M117 Landry Pullback (high 2 bulan) | DATA BELUM CUKUP | 25 | 0 |  | 21% |  | 45.52 | 287 | 0 |  | 0.81 |  |  |
| M120 Reversal New Highs | DATA BELUM CUKUP | 7 | 0 |  | 27% |  | 1.15 | 28 | 0 |  | 2.60 |  |  |
| M121 High 2 bull flag (Brooks) | DATA BELUM CUKUP | 4 | 0 |  | 47% |  | 2.47 | 49 | 0 |  | 1.48 |  |  |
| M126 Hidden Smash Day (beli, Larry Williams) | DATA BELUM CUKUP | 9 | 0 |  | 35% |  | 5.15 | 33 | 0 |  | 2.22 |  |  |
| M129 Wick Play | DATA BELUM CUKUP | 14 | 0 |  | 38% |  | 2.60 | 38 | 0 |  | 2.79 |  |  |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | DATA BELUM CUKUP | 5 | 0 |  | 25% |  | 92.22 | 261 | 0 |  | -0.93 |  |  |
| M132 Ascending Scallop (Bulkowski) | DATA BELUM CUKUP | 40 | 0 |  | 42% |  | 0.98 | 29 | 0 |  | 3.13 |  |  |
| M134 First Kiss After Daylight (Landry) | DATA BELUM CUKUP | 15 | 0 |  | 34% |  | 5.41 | 35 | 0 |  | 2.62 |  |  |
| M135 3rd Watch | DATA BELUM CUKUP | 2 | 0 |  | 39% |  | 2.05 | 35 | 0 |  | 2.78 |  |  |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | DATA BELUM CUKUP | 30 | 0 |  | 51% |  | 1.31 | 19 | 0 |  | 2.43 |  |  |
| M141 First Thrust (Landry) | DATA BELUM CUKUP | 10 | 0 |  | 39% |  | 4.05 | 37 | 0 |  | 0.69 |  |  |
| M142 Pecahan volum dari dasar (底部放量) | DATA BELUM CUKUP | 3 | 0 |  | 41% |  | 6.85 | 44 | 0 |  | 0.17 |  |  |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | DATA BELUM CUKUP | 2 | 0 |  | 52% |  | 0.83 | 18 | 0 |  | 1.11 |  |  |
| M145 Yum-Yum Continuation | DATA BELUM CUKUP | 59 | 0 |  | 25% |  | 80.48 | 356 | 0 |  | 2.37 |  |  |
| M147 Improved Three-Bar Pullback | DATA BELUM CUKUP | 26 | 0 |  | 31% |  | 91.01 | 442 | 0 |  | -1.14 |  |  |
| M149 3-Step Pullback | DATA BELUM CUKUP | 31 | 0 |  | 19% |  | 59.37 | 273 | 0 |  | 2.25 |  |  |
| M152 Spike & Ledge | DATA BELUM CUKUP | 21 | 0 |  | 52% |  | 3.20 | 36 | 0 |  | 3.66 |  |  |
| M155 Market Cycle Strategy | DATA BELUM CUKUP | 58 | 0 |  | 49% |  | 1.56 | 17 | 0 |  | 1.45 |  |  |
| M157 Consolidation Pivot Breakout (versi angka) | DATA BELUM CUKUP | 1 | 0 |  | 14% |  | 32.05 | 179 | 0 |  | -1.64 |  |  |
| M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | DATA BELUM CUKUP | 1 | 0 |  | 26% |  | 2.57 | 8 | 0 |  | -0.34 |  |  |
| M38 Darvas Kotak | DATA BELUM CUKUP | 3 | 0 |  | 49% |  | 18.79 | 210 | 0 |  | 6.00 |  |  |
| M41 FW Penyatuan Mingguan | DATA BELUM CUKUP | 3 | 0 |  | 36% |  | 15.03 | 117 | 0 |  | 2.80 |  |  |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | DATA BELUM CUKUP | 3 | 0 |  | 23% |  | 2.81 | 22 | 0 |  | 1.75 |  |  |
| M48 Cooper 1-2-3-4 | DATA BELUM CUKUP | 13 | 0 |  | 34% |  | 2.79 | 30 | 0 |  | 0.84 |  |  |
| M64 O'Neil Tiga Minggu Ketat | DATA BELUM CUKUP | 3 | 0 |  | 34% |  | 1.68 | 31 | 0 |  | 9.38 |  |  |
| M87 IBD Tapak Menaik | DATA BELUM CUKUP | 8 | 0 |  | 32% |  | 3.49 | 30 | 0 |  | 5.97 |  |  |
| M20 EMA10/15 Crossover + Sudut | SELARI | 95 | 10 | 70% | 39% | 2.88 | 0.22 | 7 | 59 | -0.24 | 2.21 | 2.0 | 1.6 |

Nota: lajur "Tutup (awal)" dan "Purata tutup" ialah maklumat sahaja (berat sebelah ke arah kena henti), tidak dipakai dalam ujian.
