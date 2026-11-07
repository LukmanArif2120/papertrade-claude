# Analisis prestasi sebenar Papertrade C lawan jangkaan backtest

Dijana oleh `WFO/kod/analisis_sebenar.py`. Sumber: semua `papertrade/claude*.csv` (15939 posisi sah; 6221 tutup, 9718 terbuka; 2026-10-08 hingga 2026-11-06). Jangkaan = registry set 431 bagi varian modul (dalam sampel bagi M115–M161).

Ujian hanya atas posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan dan >= 14 hari lalu; tutup = untung akhir, terbuka = untung semasa) untuk elak bias pemilihan (yang tutup awal kebanyakannya kena henti). Ambang: >= 10 posisi matang. AMARAN = kadar menang (z) atau purata (t) < −2 berbanding jangkaan.

**Ringkasan:** 2 AMARAN, 15 SELARI, 207 data belum cukup.

| Kaedah | Status | n | Matang | Menang matang | Menang jangka | Purata matang % | Purata jangka % | Hari jangka | Tutup (awal) | Purata tutup % | Terbuka purata % | z | t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M28 VWAP Separator + Kiss Pivot | AMARAN | 66 | 26 | 23% | 43% | -2.29 | 0.22 | 5 | 57 | -2.52 | -1.69 | -2.0 | -1.8 |
| M76 Undercut & Rally pada Low Penting | AMARAN | 52 | 17 | 12% | 37% | -2.03 | 0.67 | 9 | 41 | -3.27 | 1.57 | -2.1 | -2.1 |
| M14 Walking with the Whales | DATA BELUM CUKUP | 203 | 0 |  | 21% |  | 1.52 | 15 | 149 | -2.32 | 5.32 |  |  |
| M102 Stockbee SLTB | DATA BELUM CUKUP | 185 | 0 |  | 18% |  | 1.34 | 16 | 134 | -3.70 | 6.02 |  |  |
| M92 CCI-50 | DATA BELUM CUKUP | 216 | 8 | 100% | 49% | 6.18 | 1.17 | 13 | 127 | -2.71 | 3.91 |  |  |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | DATA BELUM CUKUP | 176 | 0 |  | 23% |  | 3.99 | 34 | 104 | -5.41 | 4.83 |  |  |
| M123 CCI Correction (Lambert, ChartSchool) | DATA BELUM CUKUP | 123 | 9 | 11% | 28% | -1.09 | 0.92 | 10 | 101 | -2.08 | 0.94 |  |  |
| M66 IBD Undur Pertama ke Purata 50 Hari | DATA BELUM CUKUP | 161 | 0 |  | 28% |  | 1.71 | 19 | 100 | -4.60 | 3.75 |  |  |
| M81 Bensdorp Long Trend High Momentum | DATA BELUM CUKUP | 165 | 0 |  | 32% |  | 8.56 | 105 | 99 | -12.99 | -2.26 |  |  |
| M55 Guppy GMMA | DATA BELUM CUKUP | 155 | 0 |  | 26% |  | 2.71 | 28 | 96 | -5.70 | 3.84 |  |  |
| M15 Break & Retest + Henti ATR | DATA BELUM CUKUP | 197 | 9 | 44% | 33% | -0.72 | 1.08 | 12 | 95 | -3.60 | 5.85 |  |  |
| M36 Turtle 55/20 | DATA BELUM CUKUP | 193 | 0 |  | 32% |  | 2.65 | 30 | 89 | -7.11 | 3.84 |  |  |
| M12 Parabolic SAR | DATA BELUM CUKUP | 179 | 0 |  | 29% |  | 2.04 | 23 | 88 | -6.26 | 3.22 |  |  |
| M99 Three Line Break | DATA BELUM CUKUP | 135 | 0 |  | 40% |  | 1.17 | 16 | 87 | -5.92 | 5.67 |  |  |
| M57 Landry Trend Knockout (TKO) | DATA BELUM CUKUP | 128 | 0 |  | 21% |  | 1.55 | 18 | 82 | -4.94 | 2.67 |  |  |
| M89 Chande 65sma-3cc | DATA BELUM CUKUP | 155 | 0 |  | 34% |  | 1.83 | 26 | 79 | -6.32 | 4.86 |  |  |
| M54 IBD Power Trend | DATA BELUM CUKUP | 162 | 0 |  | 30% |  | 3.37 | 37 | 76 | -6.67 | 3.95 |  |  |
| M111 Sistem Volatiliti Wilder | DATA BELUM CUKUP | 181 | 0 |  | 39% |  | 2.39 | 30 | 72 | -7.92 | 4.26 |  |  |
| M148 Natural Number Method | DATA BELUM CUKUP | 123 | 9 | 44% | 35% | 5.33 | 0.50 | 10 | 72 | -4.97 | 2.74 |  |  |
| M02 MACD + SMA200 | DATA BELUM CUKUP | 119 | 0 |  | 44% |  | 0.66 | 14 | 63 | -2.94 | -0.31 |  |  |
| M105 Supertrend tulen | DATA BELUM CUKUP | 199 | 0 |  | 39% |  | 2.44 | 32 | 62 | -7.38 | 4.31 |  |  |
| M11 NR7 Breakout + Volume | DATA BELUM CUKUP | 92 | 0 |  | 36% |  | 2.86 | 20 | 62 | -2.80 | 4.38 |  |  |
| M136 Short/Intermediate-term Low (Larry Williams) | DATA BELUM CUKUP | 146 | 0 |  | 24% |  | 112.90 | 343 | 62 | -9.25 | 1.57 |  |  |
| M124 'Last' Stochastic Technique (ChartSchool) | DATA BELUM CUKUP | 151 | 0 |  | 36% |  | 1.74 | 20 | 61 | -6.94 | 5.07 |  |  |
| M125 2-Bar Breakout | DATA BELUM CUKUP | 151 | 0 |  | 30% |  | 166.86 | 443 | 60 | -10.14 | 1.70 |  |  |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | DATA BELUM CUKUP | 118 | 0 |  | 32% |  | 2.68 | 29 | 60 | -6.39 | 1.67 |  |  |
| M90 Pring KST | DATA BELUM CUKUP | 93 | 0 |  | 30% |  | 1.95 | 26 | 55 | -7.75 | 1.67 |  |  |
| M10 EMA3 + CCI + MACD | DATA BELUM CUKUP | 125 | 0 |  | 33% |  | 4.70 | 54 | 54 | -7.65 | 4.03 |  |  |
| M155 Market Cycle Strategy | DATA BELUM CUKUP | 157 | 0 |  | 49% |  | 1.56 | 17 | 54 | -11.02 | 2.66 |  |  |
| M74 Lulus Baharu Trend Template Minervini | DATA BELUM CUKUP | 90 | 0 |  | 24% |  | 2.72 | 20 | 54 | -3.17 | 4.16 |  |  |
| M122 Moving Momentum (ChartSchool) | DATA BELUM CUKUP | 87 | 0 |  | 35% |  | 1.79 | 24 | 53 | -8.14 | 2.61 |  |  |
| M93 Bollinger Kaedah II: %b + MFI | DATA BELUM CUKUP | 195 | 0 |  | 36% |  | 8.20 | 62 | 51 | -10.19 | 3.51 |  |  |
| M106 DMI Wilder | DATA BELUM CUKUP | 104 | 0 |  | 32% |  | 1.01 | 12 | 50 | -3.87 | 2.59 |  |  |
| M161 EMA 10/21 + Supertrend (10,3) | DATA BELUM CUKUP | 154 | 0 |  | 35% |  | 1.43 | 18 | 50 | -9.61 | 1.28 |  |  |
| M34 Carter TTM Squeeze | DATA BELUM CUKUP | 112 | 0 |  | 34% |  | 2.38 | 30 | 48 | -8.31 | 5.54 |  |  |
| M50 Elder Triple Screen | DATA BELUM CUKUP | 57 | 0 |  | 23% |  | 1.80 | 18 | 47 | -5.07 | 6.92 |  |  |
| M82 Arthur Hill Rotasi Sasaran 10% | DATA BELUM CUKUP | 219 | 0 |  | 61% |  | 1.84 | 38 | 47 | 9.83 | -5.59 |  |  |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | DATA BELUM CUKUP | 101 | 0 |  | 34% |  | 0.55 | 12 | 46 | -5.30 | 1.43 |  |  |
| M131 Ross Hook (Joe Ross) | DATA BELUM CUKUP | 122 | 0 |  | 30% |  | 2.35 | 30 | 46 | -6.04 | 3.33 |  |  |
| M119 180 Bullish (Cooper) | DATA BELUM CUKUP | 96 | 0 |  | 27% |  | 1.17 | 18 | 44 | -6.31 | 2.89 |  |  |
| M127 Slingshot Bullish | DATA BELUM CUKUP | 67 | 0 |  | 19% |  | 2.60 | 16 | 43 | -3.07 | 3.02 |  |  |
| M80 Radge Saluran Purata Bergerak (MAC) | DATA BELUM CUKUP | 197 | 0 |  | 36% |  | 8.91 | 66 | 43 | -11.76 | 3.81 |  |  |
| M79 Radge: 20% Flipper | DATA BELUM CUKUP | 150 | 0 |  | 40% |  | 6.25 | 60 | 42 | -12.61 | 1.73 |  |  |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | DATA BELUM CUKUP | 58 | 0 |  | 50% |  | 5.17 | 39 | 41 | -1.95 | -0.65 |  |  |
| M23 Breitstein Kapitulasi + Kesinambungan | DATA BELUM CUKUP | 76 | 1 | 0% | 22% | -4.09 | 0.55 | 10 | 39 | -2.34 | 1.52 |  |  |
| M39 Radge Pecahan Bollinger 100 hari | DATA BELUM CUKUP | 165 | 0 |  | 37% |  | 9.11 | 96 | 37 | -16.46 | 1.18 |  |  |
| M137 Livermore System | DATA BELUM CUKUP | 112 | 0 |  | 35% |  | 4.22 | 37 | 36 | -7.61 | 2.75 |  |  |
| M151 Outside Bar Failure | DATA BELUM CUKUP | 77 | 0 |  | 27% |  | 1.93 | 26 | 36 | -4.22 | 4.88 |  |  |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | DATA BELUM CUKUP | 62 | 0 |  | 46% |  | 1.32 | 29 | 35 | 1.04 | -2.73 |  |  |
| M149 3-Step Pullback | DATA BELUM CUKUP | 90 | 0 |  | 19% |  | 59.37 | 273 | 34 | -7.01 | 4.51 |  |  |
| M158 Doubly Adaptive Profit Targets | DATA BELUM CUKUP | 150 | 0 |  | 34% |  | 2.94 | 30 | 33 | -9.17 | 1.85 |  |  |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | DATA BELUM CUKUP | 49 | 0 |  | 25% |  | 2.69 | 15 | 32 | -3.44 | 1.82 |  |  |
| M160 Measured Move Up | DATA BELUM CUKUP | 67 | 3 | 0% | 32% | -3.34 | 0.44 | 8 | 31 | -2.32 | 1.07 |  |  |
| M32 Momentum Burst | DATA BELUM CUKUP | 52 | 0 |  | 25% |  | 3.57 | 22 | 29 | -5.56 | 5.27 |  |  |
| M29 EMA3 + RSI75 + Stokastik | DATA BELUM CUKUP | 33 | 0 |  | 18% |  | 3.22 | 35 | 28 | -3.43 | -2.24 |  |  |
| M06 Minervini VCP Breakout | DATA BELUM CUKUP | 71 | 0 |  | 33% |  | 2.49 | 29 | 27 | -7.03 | 1.58 |  |  |
| M04 BB Squeeze Breakout | DATA BELUM CUKUP | 103 | 0 |  | 36% |  | 4.96 | 32 | 26 | -8.43 | 1.13 |  |  |
| M145 Yum-Yum Continuation | DATA BELUM CUKUP | 159 | 0 |  | 25% |  | 80.48 | 356 | 25 | -13.01 | 1.52 |  |  |
| M150 Trend Bar Failure (Brooks) | DATA BELUM CUKUP | 66 | 0 |  | 37% |  | 0.54 | 13 | 25 | -4.60 | 2.94 |  |  |
| M30 BB Free Bar + Himpitan 50/2.5 | DATA BELUM CUKUP | 124 | 0 |  | 37% |  | 3.80 | 34 | 25 | -7.10 | 1.50 |  |  |
| M33 Supertrend + SMA10 | DATA BELUM CUKUP | 132 | 0 |  | 40% |  | 1.65 | 33 | 25 | -10.09 | 2.98 |  |  |
| M132 Ascending Scallop (Bulkowski) | DATA BELUM CUKUP | 81 | 0 |  | 42% |  | 0.98 | 29 | 24 | -10.27 | 2.13 |  |  |
| M154 HOLP (High of Low Period) | DATA BELUM CUKUP | 58 | 0 |  | 39% |  | 1.93 | 27 | 24 | -11.39 | -1.61 |  |  |
| M88 O'Neil Shakeout +3 | DATA BELUM CUKUP | 49 | 0 |  | 32% |  | 5.56 | 32 | 24 | -8.14 | 5.23 |  |  |
| M146 3-Bar Momentum Pattern | DATA BELUM CUKUP | 68 | 0 |  | 27% |  | 2.66 | 26 | 22 | -5.56 | 4.52 |  |  |
| M31 Band Walk (BB 20/2) | DATA BELUM CUKUP | 193 | 0 |  | 43% |  | 3.30 | 32 | 22 | -14.41 | -0.34 |  |  |
| N113X16  | DATA BELUM CUKUP | 45 | 0 |  |  |  |  |  | 22 | -2.97 | -2.00 |  |  |
| N74X16  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 21 | -4.69 | -2.70 |  |  |
| N76X16  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 21 | -5.00 | -3.52 |  |  |
| M47 Holy Grail Raschke | DATA BELUM CUKUP | 24 | 5 | 60% | 51% | 0.04 | 0.25 | 5 | 20 | -2.65 | -2.38 |  |  |
| N08X16  | DATA BELUM CUKUP | 52 | 0 |  |  |  |  |  | 20 | -5.86 | -3.61 |  |  |
| N28X16  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 20 | -5.09 | -2.77 |  |  |
| M101 Bulkowski: Tiga lembah menaik | DATA BELUM CUKUP | 50 | 0 |  | 35% |  | 3.46 | 33 | 19 | -10.82 | 0.14 |  |  |
| M147 Improved Three-Bar Pullback | DATA BELUM CUKUP | 73 | 0 |  | 31% |  | 91.01 | 442 | 18 | -14.04 | 0.82 |  |  |
| M78 Alvarez Pecahan Mingguan DTAYS | DATA BELUM CUKUP | 33 | 0 |  | 32% |  | 3.17 | 40 | 18 | -8.96 | 2.99 |  |  |
| N27X16  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 18 | -4.46 | -3.16 |  |  |
| M01 Bollinger Band + RSI | DATA BELUM CUKUP | 85 | 0 |  | 67% |  | 2.22 | 22 | 17 | 10.53 | -6.27 |  |  |
| M133 Bull Hook (Crabel) | DATA BELUM CUKUP | 37 | 0 |  | 41% |  | 0.68 | 10 | 17 | -1.25 | 5.88 |  |  |
| N42X16  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 16 | -2.72 | -1.10 |  |  |
| M118 Expansion Pivot (Cooper) | DATA BELUM CUKUP | 68 | 0 |  | 33% |  | 1.56 | 27 | 15 | -6.40 | 2.38 |  |  |
| M134 First Kiss After Daylight (Landry) | DATA BELUM CUKUP | 38 | 0 |  | 34% |  | 5.41 | 35 | 15 | -7.61 | 4.93 |  |  |
| N24X16  | DATA BELUM CUKUP | 56 | 0 |  |  |  |  |  | 15 | -5.80 | -1.86 |  |  |
| N56X16  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 15 | -5.64 | -1.95 |  |  |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | DATA BELUM CUKUP | 62 | 0 |  | 51% |  | 1.31 | 19 | 14 | -15.45 | 2.51 |  |  |
| M59 Anjakan Julat RSI | DATA BELUM CUKUP | 37 | 0 |  | 34% |  | 3.10 | 37 | 14 | -13.44 | 0.75 |  |  |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | DATA BELUM CUKUP | 26 | 0 |  | 30% |  | 1.90 | 24 | 14 | -7.16 | 0.39 |  |  |
| N113X36  | DATA BELUM CUKUP | 45 | 0 |  |  |  |  |  | 14 | -2.40 | -2.92 |  |  |
| N48X36  | DATA BELUM CUKUP | 41 | 0 |  |  |  |  |  | 14 | -1.54 | -3.32 |  |  |
| N53X16  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 14 | -5.23 | -2.27 |  |  |
| M05 MACD Divergence + Pengesahan | DATA BELUM CUKUP | 41 | 0 |  | 35% |  | 10.85 | 108 | 13 | -9.54 | 2.35 |  |  |
| M09 Volumatic VIDYA Pivot Retest | DATA BELUM CUKUP | 25 | 0 |  | 23% |  | 1.85 | 30 | 13 | -8.39 | -0.83 |  |  |
| N25X16  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 13 | -5.43 | -2.52 |  |  |
| N36X16  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 13 | -6.57 | -3.32 |  |  |
| N41X16  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 13 | -6.53 | -3.27 |  |  |
| N42X36  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 13 | -2.81 | -1.34 |  |  |
| N45X16  | DATA BELUM CUKUP | 51 | 0 |  |  |  |  |  | 13 | -4.92 | -2.48 |  |  |
| N47X16  | DATA BELUM CUKUP | 39 | 0 |  |  |  |  |  | 13 | -5.96 | -0.77 |  |  |
| N54X16  | DATA BELUM CUKUP | 51 | 0 |  |  |  |  |  | 13 | -6.07 | -3.12 |  |  |
| M115 Bow Tie (Landry) | DATA BELUM CUKUP | 30 | 0 |  | 27% |  | 1.06 | 18 | 12 | -3.49 | 2.89 |  |  |
| M117 Landry Pullback (high 2 bulan) | DATA BELUM CUKUP | 65 | 0 |  | 21% |  | 45.52 | 287 | 12 | -8.35 | 1.82 |  |  |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | DATA BELUM CUKUP | 30 | 0 |  | 23% |  | 2.81 | 22 | 12 | -2.71 | -0.57 |  |  |
| M48 Cooper 1-2-3-4 | DATA BELUM CUKUP | 44 | 0 |  | 34% |  | 2.79 | 30 | 12 | -11.11 | 4.03 |  |  |
| N29X16  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 12 | -6.32 | -3.48 |  |  |
| M120 Reversal New Highs | DATA BELUM CUKUP | 18 | 0 |  | 27% |  | 1.15 | 28 | 11 | -5.27 | 4.86 |  |  |
| N33X16  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 11 | -8.44 | -2.01 |  |  |
| M91 Stochastic Pop (Bernstein/Steckler) | DATA BELUM CUKUP | 36 | 0 |  | 42% |  | 1.63 | 18 | 10 | -8.17 | 3.35 |  |  |
| N40X16  | DATA BELUM CUKUP | 43 | 0 |  |  |  |  |  | 10 | -3.73 | -0.87 |  |  |
| N42X17  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 10 | -0.43 | -3.29 |  |  |
| M126 Hidden Smash Day (beli, Larry Williams) | DATA BELUM CUKUP | 18 | 0 |  | 35% |  | 5.15 | 33 | 9 | -7.40 | -0.88 |  |  |
| M129 Wick Play | DATA BELUM CUKUP | 23 | 0 |  | 38% |  | 2.60 | 38 | 9 | -14.00 | 6.42 |  |  |
| N22X16  | DATA BELUM CUKUP | 52 | 0 |  |  |  |  |  | 9 | -5.39 | -1.85 |  |  |
| M68 Kell Base n' Break | DATA BELUM CUKUP | 37 | 0 |  | 36% |  | 1.35 | 35 | 8 | -8.30 | 0.81 |  |  |
| N08X36  | DATA BELUM CUKUP | 52 | 0 |  |  |  |  |  | 8 | -8.94 | -5.41 |  |  |
| M140 猎豹出击 (Serangan Cheetah) | DATA BELUM CUKUP | 33 | 0 |  | 36% |  | 5.31 | 25 | 7 | -9.82 | 0.05 |  |  |
| M141 First Thrust (Landry) | DATA BELUM CUKUP | 20 | 0 |  | 39% |  | 4.05 | 37 | 7 | -8.16 | -0.11 |  |  |
| N28X36  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 7 | -4.33 | -5.05 |  |  |
| M152 Spike & Ledge | DATA BELUM CUKUP | 39 | 0 |  | 52% |  | 3.20 | 36 | 6 | -15.81 | 0.08 |  |  |
| M87 IBD Tapak Menaik | DATA BELUM CUKUP | 12 | 0 |  | 32% |  | 3.49 | 30 | 6 | -9.53 | 5.14 |  |  |
| N07X16  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 6 | -8.88 | -2.49 |  |  |
| N42X14  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 6 | 5.95 | -3.61 |  |  |
| N68X16  | DATA BELUM CUKUP | 30 | 0 |  |  |  |  |  | 6 | -0.73 | 0.04 |  |  |
| M107 Golden Cross SMA50/200 | DATA BELUM CUKUP | 29 | 0 |  | 32% |  | 15.43 | 110 | 5 | -11.12 | 1.11 |  |  |
| M44 Tapak Rata IBD | DATA BELUM CUKUP | 12 | 0 |  | 30% |  | 0.39 | 28 | 5 | -8.00 | 1.18 |  |  |
| M52 Radge Weekend Trend Trader | DATA BELUM CUKUP | 9 | 0 |  | 37% |  | 5.19 | 37 | 5 | -18.99 | -1.94 |  |  |
| N33X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 5 | -8.39 | -3.16 |  |  |
| M84 Jarak purata bergerak MAD 21/200 | DATA BELUM CUKUP | 10 | 0 |  | 37% |  | 3.71 | 26 | 4 | -3.80 | -6.97 |  |  |
| N07X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 4 | -8.93 | -3.04 |  |  |
| N22X36  | DATA BELUM CUKUP | 52 | 0 |  |  |  |  |  | 4 | -8.44 | -2.15 |  |  |
| N24X36  | DATA BELUM CUKUP | 56 | 0 |  |  |  |  |  | 4 | -3.91 | -3.83 |  |  |
| N47X36  | DATA BELUM CUKUP | 39 | 0 |  |  |  |  |  | 4 | -7.54 | -2.94 |  |  |
| M130 多方炮 (dua lilin hijau mengapit satu merah) | DATA BELUM CUKUP | 9 | 0 |  | 25% |  | 92.22 | 261 | 3 | -18.49 | 3.76 |  |  |
| M142 Pecahan volum dari dasar (底部放量) | DATA BELUM CUKUP | 34 | 0 |  | 41% |  | 6.85 | 44 | 3 | -11.76 | 0.69 |  |  |
| M144 Screw Bar | DATA BELUM CUKUP | 8 | 0 |  | 41% |  | 7.68 | 23 | 3 | -4.04 | -1.17 |  |  |
| M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | DATA BELUM CUKUP | 6 | 0 |  | 26% |  | 2.57 | 8 | 3 | -1.66 | 0.61 |  |  |
| M41 FW Penyatuan Mingguan | DATA BELUM CUKUP | 15 | 0 |  | 36% |  | 15.03 | 117 | 3 | -16.25 | 2.83 |  |  |
| M96 Momo India: Ranking Sharpe 3/6/12 bulan | DATA BELUM CUKUP | 6 | 0 |  | 43% |  | 12.18 | 54 | 3 | -11.22 | -5.51 |  |  |
| N09X36  | DATA BELUM CUKUP | 43 | 0 |  |  |  |  |  | 3 | -3.46 | -2.82 |  |  |
| N124X36  | DATA BELUM CUKUP | 29 | 0 |  |  |  |  |  | 3 | -6.24 | -2.33 |  |  |
| N27X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 3 | -1.90 | -5.19 |  |  |
| N36X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 3 | -12.25 | -4.81 |  |  |
| N38X36  | DATA BELUM CUKUP | 41 | 0 |  |  |  |  |  | 3 | -10.10 | -1.55 |  |  |
| N41X36  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 3 | -6.53 | -4.65 |  |  |
| N51X16  | DATA BELUM CUKUP | 13 | 0 |  |  |  |  |  | 3 | -0.13 | -3.22 |  |  |
| N51X36  | DATA BELUM CUKUP | 13 | 0 |  |  |  |  |  | 3 | -0.10 | -2.28 |  |  |
| N53X36  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 3 | -5.47 | -3.92 |  |  |
| N75X17  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 3 | -1.75 | -12.43 |  |  |
| N76X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 3 | -8.43 | -5.68 |  |  |
| M07 Qullamaggie Breakout | DATA BELUM CUKUP | 2 | 2 | 0% | 20% | -3.04 | 1.05 | 8 | 2 | -3.04 |  |  |  |
| M121 High 2 bull flag (Brooks) | DATA BELUM CUKUP | 5 | 0 |  | 47% |  | 2.47 | 49 | 2 | -14.55 | -1.89 |  |  |
| M135 3rd Watch | DATA BELUM CUKUP | 12 | 0 |  | 39% |  | 2.05 | 35 | 2 | -14.60 | -3.21 |  |  |
| M157 Consolidation Pivot Breakout (versi angka) | DATA BELUM CUKUP | 4 | 0 |  | 14% |  | 32.05 | 179 | 2 | -6.35 | 4.98 |  |  |
| M45 High 52 Minggu (George & Hwang) | DATA BELUM CUKUP | 8 | 0 |  | 32% |  | 12.81 | 61 | 2 | -9.78 | 0.67 |  |  |
| N29X36  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 2 | -9.54 | -5.03 |  |  |
| N31X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 2 | -10.79 | -3.68 |  |  |
| N35X36  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 2 | -10.09 | -3.18 |  |  |
| N37X17  | DATA BELUM CUKUP | 34 | 0 |  |  |  |  |  | 2 | 6.99 | -1.62 |  |  |
| N39X36  | DATA BELUM CUKUP | 25 | 0 |  |  |  |  |  | 2 | -12.25 | -3.18 |  |  |
| N43X36  | DATA BELUM CUKUP | 44 | 0 |  |  |  |  |  | 2 | -5.26 | -4.29 |  |  |
| N45X36  | DATA BELUM CUKUP | 51 | 0 |  |  |  |  |  | 2 | -2.46 | -4.13 |  |  |
| N50X14  | DATA BELUM CUKUP | 19 | 0 |  |  |  |  |  | 2 | 6.47 | -6.53 |  |  |
| N64X17  | DATA BELUM CUKUP | 32 | 0 |  |  |  |  |  | 2 | 6.99 | -1.56 |  |  |
| N68X36  | DATA BELUM CUKUP | 30 | 0 |  |  |  |  |  | 2 | 2.10 | -0.24 |  |  |
| N80X36  | DATA BELUM CUKUP | 48 | 0 |  |  |  |  |  | 2 | -10.09 | -3.02 |  |  |
| M143 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | DATA BELUM CUKUP | 10 | 0 |  | 52% |  | 0.83 | 18 | 1 | -16.18 | 1.24 |  |  |
| M38 Darvas Kotak | DATA BELUM CUKUP | 15 | 0 |  | 49% |  | 18.79 | 210 | 1 | -9.28 | -2.93 |  |  |
| N06X36  | DATA BELUM CUKUP | 11 | 0 |  |  |  |  |  | 1 | -3.17 | -4.79 |  |  |
| N119X13  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 1 | 10.99 | -11.55 |  |  |
| N24X17  | DATA BELUM CUKUP | 56 | 0 |  |  |  |  |  | 1 | 0.32 | -4.58 |  |  |
| N28X14  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 1 | 2.87 | -6.10 |  |  |
| N36X14  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 1 | 8.87 | -5.89 |  |  |
| N37X36  | DATA BELUM CUKUP | 34 | 0 |  |  |  |  |  | 1 | 2.09 | -1.34 |  |  |
| N40X36  | DATA BELUM CUKUP | 42 | 0 |  |  |  |  |  | 1 | -5.95 | -2.52 |  |  |
| N50X17  | DATA BELUM CUKUP | 19 | 0 |  |  |  |  |  | 1 | -2.97 | -5.93 |  |  |
| N54X36  | DATA BELUM CUKUP | 51 | 0 |  |  |  |  |  | 1 | -7.06 | -4.77 |  |  |
| N56X17  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 1 | 0.32 | -4.07 |  |  |
| N56X36  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 1 | -7.06 | -3.87 |  |  |
| N57X16  | DATA BELUM CUKUP | 46 | 0 |  |  |  |  |  | 1 | -6.85 | -1.32 |  |  |
| N64X36  | DATA BELUM CUKUP | 32 | 0 |  |  |  |  |  | 1 | 2.09 | -1.27 |  |  |
| N75X14  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 1 | 6.70 | -12.23 |  |  |
| M104 High Tight Flag / Power Play | DATA BELUM CUKUP | 1 | 0 |  | 35% |  | 5.62 | 33 | 0 |  | 0.00 |  |  |
| M138 直升机空中加油 (Helikopter isi minyak di udara) | DATA BELUM CUKUP | 2 | 0 |  | 45% |  | 4.60 | 46 | 0 |  | -0.65 |  |  |
| M37 Weinstein Peringkat 2 | DATA BELUM CUKUP | 3 | 0 |  | 41% |  | 5.49 | 42 | 0 |  | -0.71 |  |  |
| M51 O'Neil Cawan & Pemegang | DATA BELUM CUKUP | 3 | 0 |  | 39% |  | 3.12 | 35 | 0 |  | -1.87 |  |  |
| M64 O'Neil Tiga Minggu Ketat | DATA BELUM CUKUP | 3 | 0 |  | 34% |  | 1.68 | 31 | 0 |  | 11.77 |  |  |
| M94 Pecutan Momentum (Chen, Yu & Wang) | DATA BELUM CUKUP | 12 | 0 |  | 63% |  | 24.04 | 121 | 0 |  | -13.31 |  |  |
| N119X15  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 0 |  | -11.30 |  |  |
| N124X15  | DATA BELUM CUKUP | 29 | 0 |  |  |  |  |  | 0 |  | -3.43 |  |  |
| N16X13  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 0 |  | -10.83 |  |  |
| N16X15  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 0 |  | -10.83 |  |  |
| N19X13  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 0 |  | -2.04 |  |  |
| N22X14  | DATA BELUM CUKUP | 52 | 0 |  |  |  |  |  | 0 |  | -3.03 |  |  |
| N25X17  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 0 |  | -4.22 |  |  |
| N25X36  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 0 |  | -4.22 |  |  |
| N28X17  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 0 |  | -6.14 |  |  |
| N33X14  | DATA BELUM CUKUP | 50 | 0 |  |  |  |  |  | 0 |  | -4.25 |  |  |
| N37X14  | DATA BELUM CUKUP | 34 | 0 |  |  |  |  |  | 0 |  | -1.33 |  |  |
| N37X16  | DATA BELUM CUKUP | 34 | 0 |  |  |  |  |  | 0 |  | -1.33 |  |  |
| N42X15  | DATA BELUM CUKUP | 53 | 0 |  |  |  |  |  | 0 |  | -3.27 |  |  |
| N53X17  | DATA BELUM CUKUP | 55 | 0 |  |  |  |  |  | 0 |  | -4.59 |  |  |
| N55X13  | DATA BELUM CUKUP | 43 | 0 |  |  |  |  |  | 0 |  | -4.13 |  |  |
| N57X36  | DATA BELUM CUKUP | 46 | 0 |  |  |  |  |  | 0 |  | -1.47 |  |  |
| N64X14  | DATA BELUM CUKUP | 32 | 0 |  |  |  |  |  | 0 |  | -1.26 |  |  |
| N64X16  | DATA BELUM CUKUP | 32 | 0 |  |  |  |  |  | 0 |  | -1.26 |  |  |
| N65X14  | DATA BELUM CUKUP | 21 | 0 |  |  |  |  |  | 0 |  | -2.17 |  |  |
| N65X36  | DATA BELUM CUKUP | 21 | 0 |  |  |  |  |  | 0 |  | -2.17 |  |  |
| N66X36  | DATA BELUM CUKUP | 34 | 0 |  |  |  |  |  | 0 |  | -3.31 |  |  |
| N73X13  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 0 |  | -2.94 |  |  |
| N75X13  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 0 |  | -11.92 |  |  |
| N75X15  | DATA BELUM CUKUP | 49 | 0 |  |  |  |  |  | 0 |  | -11.92 |  |  |
| M03 BB Break + Divergence RSI | SELARI | 203 | 74 | 66% | 56% | 0.60 | 0.58 | 8 | 172 | 0.25 | -1.44 | 1.7 | 0.1 |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | SELARI | 195 | 102 | 67% | 63% | -0.22 | 0.18 | 5 | 166 | 0.18 | -7.14 | 0.7 | -0.8 |
| M20 EMA10/15 Crossover + Sudut | SELARI | 181 | 95 | 44% | 39% | 0.92 | 0.22 | 7 | 161 | -0.07 | -0.48 | 1.0 | 1.0 |
| M70 Pecahan Hari Dalam | SELARI | 167 | 40 | 32% | 11% | 2.97 | 0.84 | 10 | 131 | -1.88 | 8.60 | 4.2 | 1.1 |
| M18 EMA9/21 Pullback | SELARI | 172 | 79 | 30% | 26% | 0.93 | 0.40 | 7 | 129 | -1.74 | 7.04 | 1.0 | 0.5 |
| M13 Garis Trend Action/Safety Line | SELARI | 199 | 22 | 41% | 34% | 1.84 | 0.97 | 11 | 128 | -3.69 | 5.82 | 0.6 | 0.5 |
| M19 Sneaky Pivot (proksi harian) | SELARI | 159 | 29 | 45% | 44% | -0.16 | 0.27 | 11 | 122 | -2.55 | 0.00 | 0.1 | -0.3 |
| M35 Pocket Pivot Morales & Kacher | SELARI | 174 | 58 | 29% | 28% | 0.46 | 0.29 | 9 | 117 | -2.27 | 4.95 | 0.2 | 0.1 |
| M159 Heikin-Ashi Trend | SELARI | 158 | 59 | 49% | 40% | 0.58 | 0.17 | 6 | 103 | -1.56 | -0.46 | 1.4 | 0.3 |
| M08 SMA20 + SMA200 | SELARI | 134 | 10 | 30% | 32% | -1.86 | 1.07 | 12 | 90 | -3.94 | 4.74 | -0.1 | -2.0 |
| M116 2/20 EMA Breakout (Landry) | SELARI | 154 | 10 | 50% | 50% | -1.90 | 0.40 | 9 | 83 | -3.14 | -0.44 | -0.0 | -0.7 |
| M153 Range Leader | SELARI | 104 | 46 | 57% | 43% | -0.17 | 0.18 | 6 | 77 | -1.73 | -0.68 | 1.8 | -0.3 |
| M156 Single Penetration (DiNapoli) | SELARI | 140 | 10 | 80% | 52% | 5.82 | 0.69 | 9 | 75 | -4.05 | -0.46 | 1.8 | 3.8 |
| M25 VWAP Wave (proksi harian) | SELARI | 133 | 35 | 34% | 30% | 3.58 | 0.42 | 10 | 72 | -3.47 | 5.77 | 0.6 | 1.4 |
| M27 Price Action 4 Tiang | SELARI | 65 | 56 | 34% | 35% | 0.92 | 0.36 | 7 | 57 | -2.19 | 16.74 | -0.2 | 0.5 |

Nota: lajur "Tutup (awal)" dan "Purata tutup" ialah maklumat sahaja (berat sebelah ke arah kena henti), tidak dipakai dalam ujian.
