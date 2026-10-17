# Analisis prestasi sebenar Papertrade C lawan jangkaan backtest

Dijana oleh `WFO/kod/analisis_sebenar.py`. Sumber: semua `papertrade/claude*.csv` (2488 posisi sah; 561 tutup, 1927 terbuka; 2026-10-08 hingga 2026-10-16). Jangkaan = registry set 431 bagi varian modul (dalam sampel bagi M115–M161).

Ujian hanya atas posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan dan >= 14 hari lalu; tutup = untung akhir, terbuka = untung semasa) untuk elak bias pemilihan (yang tutup awal kebanyakannya kena henti). Ambang: >= 10 posisi matang. AMARAN = kadar menang (z) atau purata (t) < −2 berbanding jangkaan.

**Ringkasan:** 0 AMARAN, 0 SELARI, 111 data belum cukup.

| Kaedah | Status | n | Matang | Menang matang | Menang jangka | Purata matang % | Purata jangka % | Hari jangka | Tutup (awal) | Purata tutup % | Terbuka purata % | z | t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M03 BB Break + Divergence RSI | DATA BELUM CUKUP | 57 | 0 |  | 56% |  | 0.58 | 8 | 36 | 1.86 | -0.25 |  |  |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | DATA BELUM CUKUP | 56 | 0 |  | 63% |  | 0.18 | 5 | 31 | 1.41 | -4.91 |  |  |
| M14 Walking with the Whales | DATA BELUM CUKUP | 50 | 0 |  | 21% |  | 1.52 | 15 | 30 | -2.15 | 1.73 |  |  |
| M20 EMA10/15 Crossover + Sudut | DATA BELUM CUKUP | 49 | 0 |  | 39% |  | 0.22 | 7 | 29 | -1.07 | -1.26 |  |  |
| M18 EMA9/21 Pullback | DATA BELUM CUKUP | 59 | 0 |  | 26% |  | 0.40 | 7 | 27 | -1.96 | 1.19 |  |  |
| M102 Stockbee SLTB | DATA BELUM CUKUP | 54 | 0 |  | 18% |  | 1.34 | 16 | 25 | -3.78 | 1.13 |  |  |
| M08 SMA20 + SMA200 | DATA BELUM CUKUP | 42 | 0 |  | 32% |  | 1.07 | 12 | 23 | -4.55 | 0.05 |  |  |
| M35 Pocket Pivot Morales & Kacher | DATA BELUM CUKUP | 52 | 0 |  | 28% |  | 0.29 | 9 | 21 | -2.68 | 1.06 |  |  |
| M70 Pecahan Hari Dalam | DATA BELUM CUKUP | 45 | 0 |  | 11% |  | 0.84 | 10 | 21 | -1.91 | 2.86 |  |  |
| M50 Elder Triple Screen | DATA BELUM CUKUP | 26 | 0 |  | 23% |  | 1.80 | 18 | 19 | -4.98 | 2.94 |  |  |
| M27 Price Action 4 Tiang | DATA BELUM CUKUP | 56 | 0 |  | 35% |  | 0.36 | 7 | 18 | -2.71 | 1.81 |  |  |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | DATA BELUM CUKUP | 50 | 0 |  | 23% |  | 3.99 | 34 | 16 | -3.98 | 1.94 |  |  |
| M66 IBD Undur Pertama ke Purata 50 Hari | DATA BELUM CUKUP | 49 | 0 |  | 28% |  | 1.71 | 19 | 15 | -3.09 | 1.30 |  |  |
| M57 Landry Trend Knockout (TKO) | DATA BELUM CUKUP | 30 | 0 |  | 21% |  | 1.55 | 18 | 14 | -5.91 | -1.69 |  |  |
| M81 Bensdorp Long Trend High Momentum | DATA BELUM CUKUP | 54 | 0 |  | 32% |  | 8.56 | 105 | 14 | -13.26 | -2.48 |  |  |
| M19 Sneaky Pivot (proksi harian) | DATA BELUM CUKUP | 41 | 0 |  | 44% |  | 0.27 | 11 | 13 | -4.36 | -0.10 |  |  |
| M74 Lulus Baharu Trend Template Minervini | DATA BELUM CUKUP | 25 | 0 |  | 24% |  | 2.72 | 20 | 13 | -2.69 | -0.07 |  |  |
| M15 Break & Retest + Henti ATR | DATA BELUM CUKUP | 56 | 0 |  | 33% |  | 1.08 | 12 | 12 | -4.98 | 0.81 |  |  |
| M55 Guppy GMMA | DATA BELUM CUKUP | 43 | 0 |  | 26% |  | 2.71 | 28 | 12 | -5.51 | 0.59 |  |  |
| M76 Undercut & Rally pada Low Penting | DATA BELUM CUKUP | 19 | 0 |  | 37% |  | 0.67 | 9 | 12 | -4.52 | -0.24 |  |  |
| M13 Garis Trend Action/Safety Line | DATA BELUM CUKUP | 54 | 0 |  | 34% |  | 0.97 | 11 | 11 | -4.12 | 1.41 |  |  |
| M25 VWAP Wave (proksi harian) | DATA BELUM CUKUP | 35 | 0 |  | 30% |  | 0.42 | 10 | 11 | -3.25 | 0.26 |  |  |
| M11 NR7 Breakout + Volume | DATA BELUM CUKUP | 26 | 0 |  | 36% |  | 2.86 | 20 | 9 | 0.32 | 0.51 |  |  |
| M12 Parabolic SAR | DATA BELUM CUKUP | 44 | 0 |  | 29% |  | 2.04 | 23 | 9 | -3.93 | 0.58 |  |  |
| M90 Pring KST | DATA BELUM CUKUP | 37 | 0 |  | 30% |  | 1.95 | 26 | 8 | -5.64 | 0.77 |  |  |
| M92 CCI-50 | DATA BELUM CUKUP | 63 | 0 |  | 49% |  | 1.17 | 13 | 8 | -1.60 | 1.40 |  |  |
| M54 IBD Power Trend | DATA BELUM CUKUP | 46 | 0 |  | 30% |  | 3.37 | 37 | 7 | -7.08 | 0.44 |  |  |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | DATA BELUM CUKUP | 39 | 0 |  | 32% |  | 2.68 | 29 | 7 | -6.16 | 0.08 |  |  |
| M36 Turtle 55/20 | DATA BELUM CUKUP | 46 | 0 |  | 32% |  | 2.65 | 30 | 6 | -7.23 | 0.72 |  |  |
| M99 Three Line Break | DATA BELUM CUKUP | 43 | 0 |  | 40% |  | 1.17 | 16 | 6 | -3.96 | 0.58 |  |  |
| M23 Breitstein Kapitulasi + Kesinambungan | DATA BELUM CUKUP | 8 | 0 |  | 22% |  | 0.55 | 10 | 5 | -3.09 | 0.86 |  |  |
| M89 Chande 65sma-3cc | DATA BELUM CUKUP | 39 | 0 |  | 34% |  | 1.83 | 26 | 5 | -6.31 | 1.26 |  |  |
| M02 MACD + SMA200 | DATA BELUM CUKUP | 46 | 0 |  | 44% |  | 0.66 | 14 | 4 | -0.64 | 0.45 |  |  |
| M28 VWAP Separator + Kiss Pivot | DATA BELUM CUKUP | 15 | 0 |  | 43% |  | 0.22 | 5 | 4 | -5.87 | -1.39 |  |  |
| M78 Alvarez Pecahan Mingguan DTAYS | DATA BELUM CUKUP | 10 | 0 |  | 32% |  | 3.17 | 40 | 4 | -8.52 | -0.34 |  |  |
| M80 Radge Saluran Purata Bergerak (MAC) | DATA BELUM CUKUP | 65 | 0 |  | 36% |  | 8.91 | 66 | 4 | -12.27 | 0.91 |  |  |
| M82 Arthur Hill Rotasi Sasaran 10% | DATA BELUM CUKUP | 59 | 0 |  | 61% |  | 1.84 | 38 | 4 | 0.57 | -2.33 |  |  |
| M106 DMI Wilder | DATA BELUM CUKUP | 25 | 0 |  | 32% |  | 1.01 | 12 | 3 | -4.09 | 0.19 |  |  |
| M32 Momentum Burst | DATA BELUM CUKUP | 15 | 0 |  | 25% |  | 3.57 | 22 | 3 | -3.36 | -2.13 |  |  |
| M34 Carter TTM Squeeze | DATA BELUM CUKUP | 33 | 0 |  | 34% |  | 2.38 | 30 | 3 | -4.57 | 0.59 |  |  |
| M47 Holy Grail Raschke | DATA BELUM CUKUP | 6 | 0 |  | 51% |  | 0.25 | 5 | 3 | -0.69 | -4.36 |  |  |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | DATA BELUM CUKUP | 11 | 0 |  | 25% |  | 2.69 | 15 | 3 | -3.87 | -1.11 |  |  |
| M06 Minervini VCP Breakout | DATA BELUM CUKUP | 13 | 0 |  | 33% |  | 2.49 | 29 | 2 | -7.05 | -0.34 |  |  |
| M10 EMA3 + CCI + MACD | DATA BELUM CUKUP | 43 | 0 |  | 33% |  | 4.70 | 54 | 2 | -4.65 | 0.97 |  |  |
| M105 Supertrend tulen | DATA BELUM CUKUP | 56 | 0 |  | 39% |  | 2.44 | 32 | 2 | -10.32 | 1.75 |  |  |
| M123 CCI Correction (Lambert, ChartSchool) | DATA BELUM CUKUP | 10 | 0 |  | 28% |  | 0.92 | 10 | 2 | -2.97 | -2.05 |  |  |
| M29 EMA3 + RSI75 + Stokastik | DATA BELUM CUKUP | 3 | 0 |  | 18% |  | 3.22 | 35 | 2 | -3.48 | -3.63 |  |  |
| M30 BB Free Bar + Himpitan 50/2.5 | DATA BELUM CUKUP | 29 | 0 |  | 37% |  | 3.80 | 34 | 2 | -0.51 | 0.15 |  |  |
| M39 Radge Pecahan Bollinger 100 hari | DATA BELUM CUKUP | 42 | 0 |  | 37% |  | 9.11 | 96 | 2 | -15.66 | -0.44 |  |  |
| M52 Radge Weekend Trend Trader | DATA BELUM CUKUP | 10 | 0 |  | 37% |  | 5.19 | 37 | 2 | -11.25 | -4.74 |  |  |
| M93 Bollinger Kaedah II: %b + MFI | DATA BELUM CUKUP | 59 | 0 |  | 36% |  | 8.20 | 62 | 2 | -4.88 | 0.04 |  |  |
| M04 BB Squeeze Breakout | DATA BELUM CUKUP | 14 | 0 |  | 36% |  | 4.96 | 32 | 1 | -2.72 | -2.63 |  |  |
| M07 Qullamaggie Breakout | DATA BELUM CUKUP | 2 | 0 |  | 20% |  | 1.05 | 8 | 1 | -3.74 | -0.47 |  |  |
| M09 Volumatic VIDYA Pivot Retest | DATA BELUM CUKUP | 9 | 0 |  | 23% |  | 1.85 | 30 | 1 | -7.84 | -2.24 |  |  |
| M101 Bulkowski: Tiga lembah menaik | DATA BELUM CUKUP | 19 | 0 |  | 35% |  | 3.46 | 33 | 1 | -8.64 | -0.93 |  |  |
| M111 Sistem Volatiliti Wilder | DATA BELUM CUKUP | 52 | 0 |  | 39% |  | 2.39 | 30 | 1 | -4.37 | 1.59 |  |  |
| M119 180 Bullish (Cooper) | DATA BELUM CUKUP | 8 | 0 |  | 27% |  | 1.17 | 18 | 1 | -2.33 | -2.96 |  |  |
| M127 Slingshot Bullish | DATA BELUM CUKUP | 9 | 0 |  | 19% |  | 2.60 | 16 | 1 | -2.50 | -1.49 |  |  |
| M131 Ross Hook (Joe Ross) | DATA BELUM CUKUP | 10 | 0 |  | 30% |  | 2.35 | 30 | 1 | -6.36 | -0.59 |  |  |
| M148 Natural Number Method | DATA BELUM CUKUP | 9 | 0 |  | 35% |  | 0.50 | 10 | 1 | -6.83 | -1.93 |  |  |
| M160 Measured Move Up | DATA BELUM CUKUP | 3 | 0 |  | 32% |  | 0.44 | 8 | 1 | -7.59 | -2.00 |  |  |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | DATA BELUM CUKUP | 10 | 0 |  | 50% |  | 5.17 | 39 | 1 | -8.64 | -1.91 |  |  |
| M44 Tapak Rata IBD | DATA BELUM CUKUP | 4 | 0 |  | 30% |  | 0.39 | 28 | 1 | -8.00 | 0.13 |  |  |
| M48 Cooper 1-2-3-4 | DATA BELUM CUKUP | 6 | 0 |  | 34% |  | 2.79 | 30 | 1 | -19.56 | 0.55 |  |  |
| M79 Radge: 20% Flipper | DATA BELUM CUKUP | 19 | 0 |  | 40% |  | 6.25 | 60 | 1 | -4.55 | -0.71 |  |  |
| M88 O'Neil Shakeout +3 | DATA BELUM CUKUP | 9 | 0 |  | 32% |  | 5.56 | 32 | 1 | -8.00 | -0.89 |  |  |
| M01 Bollinger Band + RSI | DATA BELUM CUKUP | 13 | 0 |  | 67% |  | 2.22 | 22 | 0 |  | -1.46 |  |  |
| M05 MACD Divergence + Pengesahan | DATA BELUM CUKUP | 9 | 0 |  | 35% |  | 10.85 | 108 | 0 |  | -0.05 |  |  |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | DATA BELUM CUKUP | 16 | 0 |  | 46% |  | 1.32 | 29 | 0 |  | -0.24 |  |  |
| M107 Golden Cross SMA50/200 | DATA BELUM CUKUP | 3 | 0 |  | 32% |  | 15.43 | 110 | 0 |  | 1.14 |  |  |
| M115 Bow Tie (Landry) | DATA BELUM CUKUP | 5 | 0 |  | 27% |  | 1.06 | 18 | 0 |  | -0.72 |  |  |
| M116 2/20 EMA Breakout (Landry) | DATA BELUM CUKUP | 10 | 0 |  | 50% |  | 0.40 | 9 | 0 |  | -2.58 |  |  |
| M117 Landry Pullback (high 2 bulan) | DATA BELUM CUKUP | 6 | 0 |  | 21% |  | 45.52 | 287 | 0 |  | -2.17 |  |  |
| M118 Expansion Pivot (Cooper) | DATA BELUM CUKUP | 1 | 0 |  | 33% |  | 1.56 | 27 | 0 |  | -0.69 |  |  |
| M120 Reversal New Highs | DATA BELUM CUKUP | 1 | 0 |  | 27% |  | 1.15 | 28 | 0 |  | -1.65 |  |  |
| M122 Moving Momentum (ChartSchool) | DATA BELUM CUKUP | 9 | 0 |  | 35% |  | 1.79 | 24 | 0 |  | -2.48 |  |  |
| M124 'Last' Stochastic Technique (ChartSchool) | DATA BELUM CUKUP | 10 | 0 |  | 36% |  | 1.74 | 20 | 0 |  | -1.55 |  |  |
| M125 2-Bar Breakout | DATA BELUM CUKUP | 10 | 0 |  | 30% |  | 166.86 | 443 | 0 |  | -1.06 |  |  |
| M128 Inventory Retracement Bar (IRB, Rob Hoffman) | DATA BELUM CUKUP | 10 | 0 |  | 34% |  | 0.55 | 12 | 0 |  | -3.47 |  |  |
| M129 Wick Play | DATA BELUM CUKUP | 3 | 0 |  | 38% |  | 2.60 | 38 | 0 |  | 0.34 |  |  |
| M132 Ascending Scallop (Bulkowski) | DATA BELUM CUKUP | 10 | 0 |  | 42% |  | 0.98 | 29 | 0 |  | -0.79 |  |  |
| M134 First Kiss After Daylight (Landry) | DATA BELUM CUKUP | 6 | 0 |  | 34% |  | 5.41 | 35 | 0 |  | -0.55 |  |  |
| M135 3rd Watch | DATA BELUM CUKUP | 1 | 0 |  | 39% |  | 2.05 | 35 | 0 |  | -1.28 |  |  |
| M136 Short/Intermediate-term Low (Larry Williams) | DATA BELUM CUKUP | 10 | 0 |  | 24% |  | 112.90 | 343 | 0 |  | -1.47 |  |  |
| M137 Livermore System | DATA BELUM CUKUP | 10 | 0 |  | 35% |  | 4.22 | 37 | 0 |  | -1.13 |  |  |
| M139 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | DATA BELUM CUKUP | 5 | 0 |  | 51% |  | 1.31 | 19 | 0 |  | -0.26 |  |  |
| M140 猎豹出击 (Serangan Cheetah) | DATA BELUM CUKUP | 1 | 0 |  | 36% |  | 5.31 | 25 | 0 |  | -6.23 |  |  |
| M141 First Thrust (Landry) | DATA BELUM CUKUP | 2 | 0 |  | 39% |  | 4.05 | 37 | 0 |  | -2.16 |  |  |
| M145 Yum-Yum Continuation | DATA BELUM CUKUP | 10 | 0 |  | 25% |  | 80.48 | 356 | 0 |  | -1.39 |  |  |
| M146 3-Bar Momentum Pattern | DATA BELUM CUKUP | 7 | 0 |  | 27% |  | 2.66 | 26 | 0 |  | -0.68 |  |  |
| M147 Improved Three-Bar Pullback | DATA BELUM CUKUP | 10 | 0 |  | 31% |  | 91.01 | 442 | 0 |  | 0.01 |  |  |
| M149 3-Step Pullback | DATA BELUM CUKUP | 3 | 0 |  | 19% |  | 59.37 | 273 | 0 |  | -3.28 |  |  |
| M150 Trend Bar Failure (Brooks) | DATA BELUM CUKUP | 5 | 0 |  | 37% |  | 0.54 | 13 | 0 |  | -1.85 |  |  |
| M151 Outside Bar Failure | DATA BELUM CUKUP | 7 | 0 |  | 27% |  | 1.93 | 26 | 0 |  | -1.87 |  |  |
| M152 Spike & Ledge | DATA BELUM CUKUP | 10 | 0 |  | 52% |  | 3.20 | 36 | 0 |  | -1.31 |  |  |
| M153 Range Leader | DATA BELUM CUKUP | 9 | 0 |  | 43% |  | 0.18 | 6 | 0 |  | -1.76 |  |  |
| M154 HOLP (High of Low Period) | DATA BELUM CUKUP | 6 | 0 |  | 39% |  | 1.93 | 27 | 0 |  | -2.69 |  |  |
| M155 Market Cycle Strategy | DATA BELUM CUKUP | 10 | 0 |  | 49% |  | 1.56 | 17 | 0 |  | -1.93 |  |  |
| M156 Single Penetration (DiNapoli) | DATA BELUM CUKUP | 10 | 0 |  | 52% |  | 0.69 | 9 | 0 |  | -3.93 |  |  |
| M158 Doubly Adaptive Profit Targets | DATA BELUM CUKUP | 10 | 0 |  | 34% |  | 2.94 | 30 | 0 |  | 0.19 |  |  |
| M159 Heikin-Ashi Trend | DATA BELUM CUKUP | 10 | 0 |  | 40% |  | 0.17 | 6 | 0 |  | -1.59 |  |  |
| M161 EMA 10/21 + Supertrend (10,3) | DATA BELUM CUKUP | 10 | 0 |  | 35% |  | 1.43 | 18 | 0 |  | -5.21 |  |  |
| M31 Band Walk (BB 20/2) | DATA BELUM CUKUP | 43 | 0 |  | 43% |  | 3.30 | 32 | 0 |  | -1.93 |  |  |
| M33 Supertrend + SMA10 | DATA BELUM CUKUP | 24 | 0 |  | 40% |  | 1.65 | 33 | 0 |  | 0.40 |  |  |
| M46 Jurang Naik Boleh Beli (Buyable Gap Up) | DATA BELUM CUKUP | 1 | 0 |  | 23% |  | 2.81 | 22 | 0 |  | -0.16 |  |  |
| M59 Anjakan Julat RSI | DATA BELUM CUKUP | 5 | 0 |  | 34% |  | 3.10 | 37 | 0 |  | -0.78 |  |  |
| M64 O'Neil Tiga Minggu Ketat | DATA BELUM CUKUP | 3 | 0 |  | 34% |  | 1.68 | 31 | 0 |  | 4.21 |  |  |
| M67 Rayner Teo: Ujian Ketiga pada Purata 50 | DATA BELUM CUKUP | 1 | 0 |  | 30% |  | 1.90 | 24 | 0 |  | -2.97 |  |  |
| M68 Kell Base n' Break | DATA BELUM CUKUP | 6 | 0 |  | 36% |  | 1.35 | 35 | 0 |  | -0.35 |  |  |
| M87 IBD Tapak Menaik | DATA BELUM CUKUP | 5 | 0 |  | 32% |  | 3.49 | 30 | 0 |  | -1.39 |  |  |
| M91 Stochastic Pop (Bernstein/Steckler) | DATA BELUM CUKUP | 6 | 0 |  | 42% |  | 1.63 | 18 | 0 |  | 0.60 |  |  |

Nota: lajur "Tutup (awal)" dan "Purata tutup" ialah maklumat sahaja (berat sebelah ke arah kena henti), tidak dipakai dalam ujian.
