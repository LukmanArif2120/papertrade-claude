# Analisis prestasi sebenar Papertrade C lawan jangkaan backtest

Dijana oleh `WFO/kod/analisis_sebenar.py`. Sumber: semua `papertrade/claude*.csv` (8748 posisi sah; 2404 tutup, 6344 terbuka; 2026-10-08 hingga 2026-10-30). Jangkaan = registry set 431 bagi varian modul (dalam sampel bagi M115–M161).

Ujian hanya atas posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan dan >= 14 hari lalu; tutup = untung akhir, terbuka = untung semasa) untuk elak bias pemilihan (yang tutup awal kebanyakannya kena henti). Ambang: >= 10 posisi matang. AMARAN = kadar menang (z) atau purata (t) < −2 berbanding jangkaan.

**Ringkasan:** 0 AMARAN, 9 SELARI, 116 data belum cukup.

| Kaedah | Status | n | Matang | Menang matang | Menang jangka | Purata matang % | Purata jangka % | Hari jangka | Tutup (awal) | Purata tutup % | Terbuka purata % | z | t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M14 Walking with the Whales | DATA BELUM CUKUP | 155 | 0 |  | 21% |  | 1.52 | 15 | 95 | -2.16 | 5.78 |  |  |
| M70 Pecahan Hari Dalam | DATA BELUM CUKUP | 127 | 3 | 0% | 11% | -0.54 | 0.84 | 10 | 79 | -1.81 | 6.93 |  |  |
| M102 Stockbee SLTB | DATA BELUM CUKUP | 147 | 0 |  | 18% |  | 1.34 | 16 | 72 | -3.52 | 5.27 |  |  |
| M123 CCI Correction (Lambert, ChartSchool) | DATA BELUM CUKUP | 91 | 0 |  | 28% |  | 0.92 | 10 | 62 | -1.59 | 2.53 |  |  |
| M15 Break & Retest + Henti ATR | DATA BELUM CUKUP | 157 | 0 |  | 33% |  | 1.08 | 12 | 59 | -3.64 | 4.53 |  |  |
| M19 Sneaky Pivot (proksi harian) | DATA BELUM CUKUP | 132 | 0 |  | 44% |  | 0.27 | 11 | 59 | -1.30 | 1.81 |  |  |
| M92 CCI-50 | DATA BELUM CUKUP | 166 | 0 |  | 49% |  | 1.17 | 13 | 59 | -1.46 | 3.64 |  |  |
| M13 Garis Trend Action/Safety Line | DATA BELUM CUKUP | 152 | 0 |  | 34% |  | 0.97 | 11 | 55 | -3.42 | 3.77 |  |  |
| M08 SMA20 + SMA200 | DATA BELUM CUKUP | 107 | 0 |  | 32% |  | 1.07 | 12 | 53 | -3.95 | 5.30 |  |  |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | DATA BELUM CUKUP | 137 | 0 |  | 23% |  | 3.99 | 34 | 50 | -4.48 | 4.08 |  |  |
| M66 IBD Undur Pertama ke Purata 50 Hari | DATA BELUM CUKUP | 129 | 0 |  | 28% |  | 1.71 | 19 | 43 | -3.29 | 3.60 |  |  |
| M57 Landry Trend Knockout (TKO) | DATA BELUM CUKUP | 94 | 0 |  | 21% |  | 1.55 | 18 | 41 | -5.13 | 3.22 |  |  |
| M55 Guppy GMMA | DATA BELUM CUKUP | 127 | 0 |  | 26% |  | 2.71 | 28 | 38 | -4.84 | 5.02 |  |  |
| M99 Three Line Break | DATA BELUM CUKUP | 115 | 0 |  | 40% |  | 1.17 | 16 | 38 | -3.67 | 4.14 |  |  |
| M11 NR7 Breakout + Volume | DATA BELUM CUKUP | 71 | 0 |  | 36% |  | 2.86 | 20 | 37 | -2.00 | 2.86 |  |  |
| M74 Lulus Baharu Trend Template Minervini | DATA BELUM CUKUP | 67 | 0 |  | 24% |  | 2.72 | 20 | 35 | -2.47 | 5.29 |  |  |
| M12 Parabolic SAR | DATA BELUM CUKUP | 131 | 0 |  | 29% |  | 2.04 | 23 | 34 | -4.66 | 4.35 |  |  |
| M106 DMI Wilder | DATA BELUM CUKUP | 72 | 0 |  | 32% |  | 1.01 | 12 | 32 | -2.32 | 2.35 |  |  |
| M54 IBD Power Trend | DATA BELUM CUKUP | 125 | 0 |  | 30% |  | 3.37 | 37 | 30 | -6.54 | 3.03 |  |  |
| M148 Natural Number Method | DATA BELUM CUKUP | 88 | 0 |  | 35% |  | 0.50 | 10 | 29 | -4.05 | 1.11 |  |  |
| M153 Range Leader | DATA BELUM CUKUP | 86 | 9 | 56% | 43% | 1.11 | 0.18 | 6 | 27 | -1.99 | 1.91 |  |  |
| M36 Turtle 55/20 | DATA BELUM CUKUP | 141 | 0 |  | 32% |  | 2.65 | 30 | 27 | -7.10 | 3.36 |  |  |
| M02 MACD + SMA200 | DATA BELUM CUKUP | 106 | 0 |  | 44% |  | 0.66 | 14 | 26 | -0.43 | 2.59 |  |  |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | DATA BELUM CUKUP | 40 | 0 |  | 50% |  | 5.17 | 39 | 26 | -0.71 | 0.73 |  |  |
| M50 Elder Triple Screen | DATA BELUM CUKUP | 46 | 0 |  | 23% |  | 1.80 | 18 | 26 | -5.71 | 4.11 |  |  |
| M89 Chande 65sma-3cc | DATA BELUM CUKUP | 127 | 0 |  | 34% |  | 1.83 | 26 | 26 | -5.63 | 3.20 |  |  |
| M127 Slingshot Bullish | DATA BELUM CUKUP | 48 | 0 |  | 19% |  | 2.60 | 16 | 23 | -2.44 | 3.31 |  |  |
| M76 Undercut & Rally pada Low Penting | DATA BELUM CUKUP | 40 | 1 | 0% | 37% | -3.23 | 0.67 | 9 | 23 | -3.40 | 3.73 |  |  |
| M81 Bensdorp Long Trend High Momentum | DATA BELUM CUKUP | 155 | 0 |  | 32% |  | 8.56 | 105 | 23 | -13.85 | 2.18 |  |  |
| M82 Arthur Hill Rotasi Sasaran 10% | DATA BELUM CUKUP | 164 | 0 |  | 61% |  | 1.84 | 38 | 23 | 10.70 | 0.26 |  |  |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | DATA BELUM CUKUP | 94 | 0 |  | 32% |  | 2.68 | 29 | 22 | -6.44 | 2.59 |  |  |
| M119 180 Bullish (Cooper) | DATA BELUM CUKUP | 70 | 0 |  | 27% |  | 1.17 | 18 | 21 | -5.74 | 2.31 |  |  |
| M160 Measured Move Up | DATA BELUM CUKUP | 45 | 0 |  | 32% |  | 0.44 | 8 | 21 | -2.05 | 4.23 |  |  |
| M90 Pring KST | DATA BELUM CUKUP | 77 | 0 |  | 30% |  | 1.95 | 26 | 21 | -6.43 | 3.63 |  |  |
| M23 Breitstein Kapitulasi + Kesinambungan | DATA BELUM CUKUP | 48 | 0 |  | 22% |  | 0.55 | 10 | 20 | -2.03 | 2.79 |  |  |
| M93 Bollinger Kaedah II: %b + MFI | DATA BELUM CUKUP | 155 | 0 |  | 36% |  | 8.20 | 62 | 19 | -9.00 | 3.77 |  |  |
| M124 'Last' Stochastic Technique (ChartSchool) | DATA BELUM CUKUP | 103 | 0 |  | 36% |  | 1.74 | 20 | 17 | -5.89 | 2.90 |  |  |
| M29 EMA3 + RSI75 + Stokastik | DATA BELUM CUKUP | 24 | 0 |  | 18% |  | 3.22 | 35 | 16 | -2.16 | 6.24 |  |  |
| M122 Moving Momentum (ChartSchool) | DATA BELUM CUKUP | 72 | 0 |  | 35% |  | 1.79 | 24 | 15 | -4.83 | 1.97 |  |  |
| M156 Single Penetration (DiNapoli) | DATA BELUM CUKUP | 93 | 0 |  | 52% |  | 0.69 | 9 | 15 | -0.43 | 2.00 |  |  |
| M105 Supertrend tulen | DATA BELUM CUKUP | 150 | 0 |  | 39% |  | 2.44 | 32 | 13 | -5.39 | 3.34 |  |  |
| M111 Sistem Volatiliti Wilder | DATA BELUM CUKUP | 137 | 0 |  | 39% |  | 2.39 | 30 | 13 | -6.73 | 3.25 |  |  |
| M116 2/20 EMA Breakout (Landry) | DATA BELUM CUKUP | 105 | 0 |  | 50% |  | 0.40 | 9 | 13 | -4.24 | 1.45 |  |  |
| M131 Ross Hook (Joe Ross) | DATA BELUM CUKUP | 90 | 0 |  | 30% |  | 2.35 | 30 | 13 | -6.25 | 2.33 |  |  |
| M151 Outside Bar Failure | DATA BELUM CUKUP | 54 | 0 |  | 27% |  | 1.93 | 26 | 13 | -4.16 | 3.00 |  |  |
| M34 Carter TTM Squeeze | DATA BELUM CUKUP | 101 | 0 |  | 34% |  | 2.38 | 30 | 13 | -4.94 | 3.25 |  |  |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | DATA BELUM CUKUP | 32 | 0 |  | 25% |  | 2.69 | 15 | 13 | -3.36 | 3.67 |  |  |
| M04 BB Squeeze Breakout | DATA BELUM CUKUP | 66 | 0 |  | 36% |  | 4.96 | 32 | 12 | -5.46 | 1.17 |  |  |
| M161 EMA 10/21 + Supertrend (10,3) | DATA BELUM CUKUP | 108 | 0 |  | 35% |  | 1.43 | 18 | 12 | -11.01 | 2.87 |  |  |
| M32 Momentum Burst | DATA BELUM CUKUP | 37 | 0 |  | 25% |  | 3.57 | 22 | 12 | -7.61 | 5.47 |  |  |
| M39 Radge Pecahan Bollinger 100 hari | DATA BELUM CUKUP | 126 | 0 |  | 37% |  | 9.11 | 96 | 11 | -19.25 | 2.67 |  |  |
| M10 EMA3 + CCI + MACD | DATA BELUM CUKUP | 102 | 0 |  | 33% |  | 4.70 | 54 | 10 | -4.65 | 3.92 |  |  |
| M133 Bull Hook (Crabel) | DATA BELUM CUKUP | 24 | 0 |  | 41% |  | 0.68 | 10 | 10 | -0.54 | 3.36 |  |  |
| M30 BB Free Bar + Himpitan 50/2.5 | DATA BELUM CUKUP | 88 | 0 |  | 37% |  | 3.80 | 34 | 10 | -5.01 | 2.55 |  |  |
| M80 Radge Saluran Purata Bergerak (MAC) | DATA BELUM CUKUP | 155 | 0 |  | 36% |  | 8.91 | 66 | 10 | -15.89 | 3.01 |  |  |
| M09 Volumatic VIDYA Pivot Retest | DATA BELUM CUKUP | 19 | 0 |  | 23% |  | 1.85 | 30 | 9 | -8.53 | 3.28 |  |  |
| M78 Alvarez Pecahan Mingguan DTAYS | DATA BELUM CUKUP | 33 | 0 |  | 32% |  | 3.17 | 40 | 9 | -9.14 | 2.71 |  |  |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | DATA BELUM CUKUP | 45 | 0 |  | 46% |  | 1.32 | 29 | 8 | 2.22 | 1.70 |  |  |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | DATA BELUM CUKUP | 78 | 0 |  | 34% |  | 0.55 | 12 | 8 | -5.72 | 2.10 |  |  |
| M136 Short/Intermediate-term Low (Larry Williams) | DATA BELUM CUKUP | 103 | 0 |  | 24% |  | 112.90 | 343 | 8 | -7.63 | 2.38 |  |  |
| M149 3-Step Pullback | DATA BELUM CUKUP | 60 | 0 |  | 19% |  | 59.37 | 273 | 8 | -7.38 | 2.87 |  |  |
| M01 Bollinger Band + RSI | DATA BELUM CUKUP | 56 | 0 |  | 67% |  | 2.22 | 22 | 7 | 9.49 | 2.60 |  |  |
| M125 2-Bar Breakout | DATA BELUM CUKUP | 104 | 0 |  | 30% |  | 166.86 | 443 | 7 | -10.82 | 2.19 |  |  |
| M155 Market Cycle Strategy | DATA BELUM CUKUP | 108 | 0 |  | 49% |  | 1.56 | 17 | 7 | -13.56 | 1.73 |  |  |
| M31 Band Walk (BB 20/2) | DATA BELUM CUKUP | 147 | 0 |  | 43% |  | 3.30 | 32 | 7 | -18.10 | 2.04 |  |  |
| M47 Holy Grail Raschke | DATA BELUM CUKUP | 16 | 5 | 60% | 51% | 0.71 | 0.25 | 5 | 7 | -2.64 | 2.02 |  |  |
| M06 Minervini VCP Breakout | DATA BELUM CUKUP | 50 | 0 |  | 33% |  | 2.49 | 29 | 6 | -5.92 | 2.72 |  |  |
| M115 Bow Tie (Landry) | DATA BELUM CUKUP | 21 | 0 |  | 27% |  | 1.06 | 18 | 6 | -2.68 | 4.36 |  |  |
| M118 Expansion Pivot (Cooper) | DATA BELUM CUKUP | 43 | 0 |  | 33% |  | 1.56 | 27 | 6 | -4.60 | 2.59 |  |  |
| M146 3-Bar Momentum Pattern | DATA BELUM CUKUP | 45 | 0 |  | 27% |  | 2.66 | 26 | 6 | -5.47 | 2.96 |  |  |
| M158 Doubly Adaptive Profit Targets | DATA BELUM CUKUP | 100 | 0 |  | 34% |  | 2.94 | 30 | 6 | -7.44 | 2.36 |  |  |
| M79 Radge: 20% Flipper | DATA BELUM CUKUP | 104 | 0 |  | 40% |  | 6.25 | 60 | 6 | -11.19 | 1.37 |  |  |
| M137 Livermore System | DATA BELUM CUKUP | 78 | 0 |  | 35% |  | 4.22 | 37 | 5 | -8.74 | 2.22 |  |  |
| M150 Trend Bar Failure (Brooks) | DATA BELUM CUKUP | 46 | 0 |  | 37% |  | 0.54 | 13 | 5 | -4.25 | 1.51 |  |  |
| M33 Supertrend + SMA10 | DATA BELUM CUKUP | 88 | 0 |  | 40% |  | 1.65 | 33 | 5 | -10.76 | 2.44 |  |  |
| M05 MACD Divergence + Pengesahan | DATA BELUM CUKUP | 31 | 0 |  | 35% |  | 10.85 | 108 | 4 | -8.01 | 1.74 |  |  |
| M101 Bulkowski: Tiga lembah menaik | DATA BELUM CUKUP | 45 | 0 |  | 35% |  | 3.46 | 33 | 4 | -9.74 | 2.22 |  |  |
| M134 First Kiss After Daylight (Landry) | DATA BELUM CUKUP | 30 | 0 |  | 34% |  | 5.41 | 35 | 4 | -9.20 | 3.34 |  |  |
| M154 HOLP (High of Low Period) | DATA BELUM CUKUP | 43 | 0 |  | 39% |  | 1.93 | 27 | 4 | -9.63 | 3.29 |  |  |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | DATA BELUM CUKUP | 15 | 0 |  | 30% |  | 1.90 | 24 | 4 | -7.16 | 5.87 |  |  |
| M132 Ascending Scallop (Bulkowski) | DATA BELUM CUKUP | 64 | 0 |  | 42% |  | 0.98 | 29 | 3 | -11.60 | 1.58 |  |  |
| M140 猎豹出击 (Serangan Cheetah) | DATA BELUM CUKUP | 11 | 0 |  | 36% |  | 5.31 | 25 | 3 | -10.14 | 0.04 |  |  |
| M145 Yum-Yum Continuation | DATA BELUM CUKUP | 109 | 0 |  | 25% |  | 80.48 | 356 | 3 | -13.77 | 1.12 |  |  |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | DATA BELUM CUKUP | 13 | 0 |  | 23% |  | 2.81 | 22 | 3 | -2.13 | 0.09 |  |  |
| M52 Radge Weekend Trend Trader | DATA BELUM CUKUP | 9 | 0 |  | 37% |  | 5.19 | 37 | 3 | -13.07 | -2.48 |  |  |
| M59 Anjakan Julat RSI | DATA BELUM CUKUP | 30 | 0 |  | 34% |  | 3.10 | 37 | 3 | -10.68 | 1.18 |  |  |
| M88 O'Neil Shakeout +3 | DATA BELUM CUKUP | 30 | 0 |  | 32% |  | 5.56 | 32 | 3 | -8.00 | 4.17 |  |  |
| M91 Stochastic Pop (Bernstein/Steckler) | DATA BELUM CUKUP | 23 | 0 |  | 42% |  | 1.63 | 18 | 3 | -7.69 | 6.26 |  |  |
| M117 Landry Pullback (high 2 bulan) | DATA BELUM CUKUP | 46 | 0 |  | 21% |  | 45.52 | 287 | 2 | -6.05 | 2.55 |  |  |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | DATA BELUM CUKUP | 48 | 0 |  | 51% |  | 1.31 | 19 | 2 | -15.07 | 2.63 |  |  |
| M144 Screw Bar | DATA BELUM CUKUP | 2 | 0 |  | 41% |  | 7.68 | 23 | 2 | 1.40 |  |  |  |
| M44 Tapak Rata IBD | DATA BELUM CUKUP | 10 | 0 |  | 30% |  | 0.39 | 28 | 2 | -8.00 | 1.10 |  |  |
| M68 Kell Base n' Break | DATA BELUM CUKUP | 20 | 0 |  | 36% |  | 1.35 | 35 | 2 | -9.03 | 2.68 |  |  |
| M07 Qullamaggie Breakout | DATA BELUM CUKUP | 2 | 0 |  | 20% |  | 1.05 | 8 | 1 | -3.74 | 9.51 |  |  |
| M120 Reversal New Highs | DATA BELUM CUKUP | 11 | 0 |  | 27% |  | 1.15 | 28 | 1 | -4.27 | 0.69 |  |  |
| M126 Hidden Smash Day (beli, Larry Williams) | DATA BELUM CUKUP | 14 | 0 |  | 35% |  | 5.15 | 33 | 1 | -1.81 | 1.35 |  |  |
| M141 First Thrust (Landry) | DATA BELUM CUKUP | 13 | 0 |  | 39% |  | 4.05 | 37 | 1 | -5.06 | 1.29 |  |  |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | DATA BELUM CUKUP | 6 | 0 |  | 52% |  | 0.83 | 18 | 1 | -16.18 | 0.32 |  |  |
| M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | DATA BELUM CUKUP | 4 | 0 |  | 26% |  | 2.57 | 8 | 1 | 2.42 | 3.23 |  |  |
| M48 Cooper 1-2-3-4 | DATA BELUM CUKUP | 28 | 0 |  | 34% |  | 2.79 | 30 | 1 | -25.17 | 2.58 |  |  |
| M87 IBD Tapak Menaik | DATA BELUM CUKUP | 11 | 0 |  | 32% |  | 3.49 | 30 | 1 | -8.99 | 5.00 |  |  |
| M107 Golden Cross SMA50/200 | DATA BELUM CUKUP | 18 | 0 |  | 32% |  | 15.43 | 110 | 0 |  | 2.02 |  |  |
| M121 High 2 bull flag (Brooks) | DATA BELUM CUKUP | 5 | 0 |  | 47% |  | 2.47 | 49 | 0 |  | 3.34 |  |  |
| M129 Wick Play | DATA BELUM CUKUP | 22 | 0 |  | 38% |  | 2.60 | 38 | 0 |  | 4.23 |  |  |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | DATA BELUM CUKUP | 8 | 0 |  | 25% |  | 92.22 | 261 | 0 |  | -1.27 |  |  |
| M135 3rd Watch | DATA BELUM CUKUP | 4 | 0 |  | 39% |  | 2.05 | 35 | 0 |  | 1.39 |  |  |
| M138 直升机空中加油 (Helikopter isi minyak di udara) | DATA BELUM CUKUP | 1 | 0 |  | 45% |  | 4.60 | 46 | 0 |  | 0.04 |  |  |
| M142 Pecahan volum dari dasar (底部放量) | DATA BELUM CUKUP | 12 | 0 |  | 41% |  | 6.85 | 44 | 0 |  | 0.19 |  |  |
| M147 Improved Three-Bar Pullback | DATA BELUM CUKUP | 57 | 0 |  | 31% |  | 91.01 | 442 | 0 |  | 0.25 |  |  |
| M152 Spike & Ledge | DATA BELUM CUKUP | 32 | 0 |  | 52% |  | 3.20 | 36 | 0 |  | 2.31 |  |  |
| M157 Consolidation Pivot Breakout (versi angka) | DATA BELUM CUKUP | 3 | 0 |  | 14% |  | 32.05 | 179 | 0 |  | 0.95 |  |  |
| M37 Weinstein Peringkat 2 | DATA BELUM CUKUP | 1 | 0 |  | 41% |  | 5.49 | 42 | 0 |  | -0.16 |  |  |
| M38 Darvas Kotak | DATA BELUM CUKUP | 10 | 0 |  | 49% |  | 18.79 | 210 | 0 |  | 3.52 |  |  |
| M41 FW Penyatuan Mingguan | DATA BELUM CUKUP | 9 | 0 |  | 36% |  | 15.03 | 117 | 0 |  | -0.63 |  |  |
| M51 O'Neil Cawan & Pemegang | DATA BELUM CUKUP | 1 | 0 |  | 39% |  | 3.12 | 35 | 0 |  | 0.00 |  |  |
| M64 O'Neil Tiga Minggu Ketat | DATA BELUM CUKUP | 3 | 0 |  | 34% |  | 1.68 | 31 | 0 |  | 9.97 |  |  |
| M03 BB Break + Divergence RSI | SELARI | 156 | 26 | 88% | 56% | 1.52 | 0.58 | 8 | 110 | 1.23 | 0.15 | 3.3 | 1.5 |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | SELARI | 152 | 54 | 61% | 63% | -0.70 | 0.18 | 5 | 109 | -0.04 | 0.01 | -0.4 | -1.4 |
| M18 EMA9/21 Pullback | SELARI | 140 | 34 | 21% | 26% | 0.05 | 0.40 | 7 | 90 | -1.78 | 5.58 | -0.7 | -0.3 |
| M20 EMA10/15 Crossover + Sudut | SELARI | 142 | 48 | 48% | 39% | 0.61 | 0.22 | 7 | 88 | 0.57 | 1.32 | 1.2 | 0.5 |
| M35 Pocket Pivot Morales & Kacher | SELARI | 138 | 18 | 44% | 28% | 3.08 | 0.29 | 9 | 67 | -2.18 | 4.82 | 1.5 | 1.5 |
| M25 VWAP Wave (proksi harian) | SELARI | 103 | 10 | 30% | 30% | 0.63 | 0.42 | 10 | 38 | -3.33 | 4.35 | 0.0 | 0.1 |
| M27 Price Action 4 Tiang | SELARI | 65 | 45 | 42% | 35% | 1.07 | 0.36 | 7 | 33 | -2.26 | 5.54 | 1.0 | 0.7 |
| M28 VWAP Separator + Kiss Pivot | SELARI | 47 | 15 | 20% | 43% | -1.75 | 0.22 | 5 | 30 | -1.58 | 3.60 | -1.8 | -1.1 |
| M159 Heikin-Ashi Trend | SELARI | 108 | 10 | 70% | 40% | 2.08 | 0.17 | 6 | 26 | -1.49 | 2.30 | 1.9 | 0.9 |

Nota: lajur "Tutup (awal)" dan "Purata tutup" ialah maklumat sahaja (berat sebelah ke arah kena henti), tidak dipakai dalam ujian.
