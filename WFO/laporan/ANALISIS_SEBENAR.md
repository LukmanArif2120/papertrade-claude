# Analisis prestasi sebenar Papertrade C lawan jangkaan backtest

Dijana oleh `WFO/kod/analisis_sebenar.py`. Sumber: semua `papertrade/claude*.csv` (1669 posisi sah; 436 tutup, 1233 terbuka; 2026-10-08 hingga 2026-10-15). Jangkaan = registry set 431 bagi varian modul (dalam sampel bagi M115–M161).

Ujian hanya atas posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan dan >= 14 hari lalu; tutup = untung akhir, terbuka = untung semasa) untuk elak bias pemilihan (yang tutup awal kebanyakannya kena henti). Ambang: >= 10 posisi matang. AMARAN = kadar menang (z) atau purata (t) < −2 berbanding jangkaan.

**Ringkasan:** 0 AMARAN, 0 SELARI, 71 data belum cukup.

| Kaedah | Status | n | Matang | Menang matang | Menang jangka | Purata matang % | Purata jangka % | Hari jangka | Tutup (awal) | Purata tutup % | Terbuka purata % | z | t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M14 Walking with the Whales | DATA BELUM CUKUP | 37 | 0 |  | 21% |  | 1.52 | 15 | 25 | -2.18 | 4.38 |  |  |
| M03 BB Break + Divergence RSI | DATA BELUM CUKUP | 45 | 0 |  | 56% |  | 0.58 | 8 | 24 | 1.86 | 1.20 |  |  |
| M08 SMA20 + SMA200 | DATA BELUM CUKUP | 36 | 0 |  | 32% |  | 1.07 | 12 | 23 | -4.55 | 2.95 |  |  |
| M102 Stockbee SLTB | DATA BELUM CUKUP | 43 | 0 |  | 18% |  | 1.34 | 16 | 23 | -3.56 | 4.82 |  |  |
| M18 EMA9/21 Pullback | DATA BELUM CUKUP | 49 | 0 |  | 26% |  | 0.40 | 7 | 22 | -1.81 | 3.25 |  |  |
| M20 EMA10/15 Crossover + Sudut | DATA BELUM CUKUP | 38 | 0 |  | 39% |  | 0.22 | 7 | 22 | -1.78 | 2.19 |  |  |
| M70 Pecahan Hari Dalam | DATA BELUM CUKUP | 41 | 0 |  | 11% |  | 0.84 | 10 | 19 | -2.06 | 3.86 |  |  |
| M35 Pocket Pivot Morales & Kacher | DATA BELUM CUKUP | 42 | 0 |  | 28% |  | 0.29 | 9 | 17 | -2.68 | 2.59 |  |  |
| M50 Elder Triple Screen | DATA BELUM CUKUP | 26 | 0 |  | 23% |  | 1.80 | 18 | 17 | -4.66 | 2.91 |  |  |
| M73 ADX(5) > 40 + Julat Terkecil 6 Hari | DATA BELUM CUKUP | 46 | 0 |  | 63% |  | 0.18 | 5 | 15 | 1.37 | -1.34 |  |  |
| M27 Price Action 4 Tiang | DATA BELUM CUKUP | 45 | 0 |  | 35% |  | 0.36 | 7 | 14 | -2.99 | 2.84 |  |  |
| M66 IBD Undur Pertama ke Purata 50 Hari | DATA BELUM CUKUP | 38 | 0 |  | 28% |  | 1.71 | 19 | 14 | -3.28 | 2.13 |  |  |
| M19 Sneaky Pivot (proksi harian) | DATA BELUM CUKUP | 30 | 0 |  | 44% |  | 0.27 | 11 | 13 | -4.36 | 1.35 |  |  |
| M15 Break & Retest + Henti ATR | DATA BELUM CUKUP | 46 | 0 |  | 33% |  | 1.08 | 12 | 12 | -4.98 | 1.62 |  |  |
| M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | DATA BELUM CUKUP | 43 | 0 |  | 23% |  | 3.99 | 34 | 12 | -4.68 | 1.58 |  |  |
| M55 Guppy GMMA | DATA BELUM CUKUP | 34 | 0 |  | 26% |  | 2.71 | 28 | 11 | -5.98 | 2.74 |  |  |
| M57 Landry Trend Knockout (TKO) | DATA BELUM CUKUP | 23 | 0 |  | 21% |  | 1.55 | 18 | 11 | -6.25 | 1.12 |  |  |
| M25 VWAP Wave (proksi harian) | DATA BELUM CUKUP | 30 | 0 |  | 30% |  | 0.42 | 10 | 10 | -3.33 | 1.40 |  |  |
| M11 NR7 Breakout + Volume | DATA BELUM CUKUP | 17 | 0 |  | 36% |  | 2.86 | 20 | 9 | 0.32 | 1.03 |  |  |
| M13 Garis Trend Action/Safety Line | DATA BELUM CUKUP | 42 | 0 |  | 34% |  | 0.97 | 11 | 9 | -4.86 | 2.20 |  |  |
| M81 Bensdorp Long Trend High Momentum | DATA BELUM CUKUP | 44 | 0 |  | 32% |  | 8.56 | 105 | 9 | -13.91 | -1.04 |  |  |
| M12 Parabolic SAR | DATA BELUM CUKUP | 32 | 0 |  | 29% |  | 2.04 | 23 | 8 | -4.23 | 2.87 |  |  |
| M76 Undercut & Rally pada Low Penting | DATA BELUM CUKUP | 11 | 0 |  | 37% |  | 0.67 | 9 | 8 | -5.06 | -0.97 |  |  |
| M90 Pring KST | DATA BELUM CUKUP | 29 | 0 |  | 30% |  | 1.95 | 26 | 7 | -6.04 | 0.37 |  |  |
| M92 CCI-50 | DATA BELUM CUKUP | 51 | 0 |  | 49% |  | 1.17 | 13 | 7 | -2.59 | 2.27 |  |  |
| M54 IBD Power Trend | DATA BELUM CUKUP | 36 | 0 |  | 30% |  | 3.37 | 37 | 6 | -7.09 | 1.23 |  |  |
| M74 Lulus Baharu Trend Template Minervini | DATA BELUM CUKUP | 16 | 0 |  | 24% |  | 2.72 | 20 | 6 | -3.48 | 0.82 |  |  |
| M95 Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | DATA BELUM CUKUP | 31 | 0 |  | 32% |  | 2.68 | 29 | 6 | -6.34 | -0.66 |  |  |
| M36 Turtle 55/20 | DATA BELUM CUKUP | 36 | 0 |  | 32% |  | 2.65 | 30 | 5 | -7.57 | 1.28 |  |  |
| M02 MACD + SMA200 | DATA BELUM CUKUP | 37 | 0 |  | 44% |  | 0.66 | 14 | 4 | -0.64 | 0.83 |  |  |
| M78 Alvarez Pecahan Mingguan DTAYS | DATA BELUM CUKUP | 10 | 0 |  | 32% |  | 3.17 | 40 | 4 | -8.52 | 1.05 |  |  |
| M82 Arthur Hill Rotasi Sasaran 10% | DATA BELUM CUKUP | 49 | 0 |  | 61% |  | 1.84 | 38 | 4 | 0.57 | 0.70 |  |  |
| M89 Chande 65sma-3cc | DATA BELUM CUKUP | 31 | 0 |  | 34% |  | 1.83 | 26 | 4 | -5.96 | 0.96 |  |  |
| M47 Holy Grail Raschke | DATA BELUM CUKUP | 4 | 0 |  | 51% |  | 0.25 | 5 | 3 | -0.69 | 7.66 |  |  |
| M10 EMA3 + CCI + MACD | DATA BELUM CUKUP | 33 | 0 |  | 33% |  | 4.70 | 54 | 2 | -4.65 | 0.18 |  |  |
| M106 DMI Wilder | DATA BELUM CUKUP | 15 | 0 |  | 32% |  | 1.01 | 12 | 2 | -5.05 | 1.27 |  |  |
| M30 BB Free Bar + Himpitan 50/2.5 | DATA BELUM CUKUP | 19 | 0 |  | 37% |  | 3.80 | 34 | 2 | -0.51 | 0.56 |  |  |
| M32 Momentum Burst | DATA BELUM CUKUP | 5 | 0 |  | 25% |  | 3.57 | 22 | 2 | -2.55 | 2.41 |  |  |
| M34 Carter TTM Squeeze | DATA BELUM CUKUP | 23 | 0 |  | 34% |  | 2.38 | 30 | 2 | -3.92 | 1.51 |  |  |
| M52 Radge Weekend Trend Trader | DATA BELUM CUKUP | 10 | 0 |  | 37% |  | 5.19 | 37 | 2 | -11.25 | -2.36 |  |  |
| M77 Undercut & Rally pada Purata Bergerak (MAU&R) | DATA BELUM CUKUP | 4 | 0 |  | 25% |  | 2.69 | 15 | 2 | -2.12 | 3.44 |  |  |
| M80 Radge Saluran Purata Bergerak (MAC) | DATA BELUM CUKUP | 52 | 0 |  | 36% |  | 8.91 | 66 | 2 | -18.52 | -0.10 |  |  |
| M99 Three Line Break | DATA BELUM CUKUP | 33 | 0 |  | 40% |  | 1.17 | 16 | 2 | -3.15 | 1.13 |  |  |
| M06 Minervini VCP Breakout | DATA BELUM CUKUP | 7 | 0 |  | 33% |  | 2.49 | 29 | 1 | -8.82 | -1.79 |  |  |
| M07 Qullamaggie Breakout | DATA BELUM CUKUP | 1 | 0 |  | 20% |  | 1.05 | 8 | 1 | -3.74 |  |  |  |
| M101 Bulkowski: Tiga lembah menaik | DATA BELUM CUKUP | 16 | 0 |  | 35% |  | 3.46 | 33 | 1 | -8.64 | -1.47 |  |  |
| M105 Supertrend tulen | DATA BELUM CUKUP | 44 | 0 |  | 39% |  | 2.44 | 32 | 1 | -8.64 | 1.65 |  |  |
| M111 Sistem Volatiliti Wilder | DATA BELUM CUKUP | 40 | 0 |  | 39% |  | 2.39 | 30 | 1 | -4.37 | 1.31 |  |  |
| M23 Breitstein Kapitulasi + Kesinambungan | DATA BELUM CUKUP | 1 | 0 |  | 22% |  | 0.55 | 10 | 1 | -4.09 |  |  |  |
| M26 Garis Trend Undur 3 Sentuhan + Pecahan | DATA BELUM CUKUP | 4 | 0 |  | 50% |  | 5.17 | 39 | 1 | -8.64 | -3.03 |  |  |
| M28 VWAP Separator + Kiss Pivot | DATA BELUM CUKUP | 5 | 0 |  | 43% |  | 0.22 | 5 | 1 | -3.36 | 2.45 |  |  |
| M29 EMA3 + RSI75 + Stokastik | DATA BELUM CUKUP | 1 | 0 |  | 18% |  | 3.22 | 35 | 1 | -1.67 |  |  |  |
| M39 Radge Pecahan Bollinger 100 hari | DATA BELUM CUKUP | 32 | 0 |  | 37% |  | 9.11 | 96 | 1 | -14.83 | -0.83 |  |  |
| M44 Tapak Rata IBD | DATA BELUM CUKUP | 3 | 0 |  | 30% |  | 0.39 | 28 | 1 | -8.00 | 3.00 |  |  |
| M48 Cooper 1-2-3-4 | DATA BELUM CUKUP | 4 | 0 |  | 34% |  | 2.79 | 30 | 1 | -19.56 | 2.99 |  |  |
| M79 Radge: 20% Flipper | DATA BELUM CUKUP | 8 | 0 |  | 40% |  | 6.25 | 60 | 1 | -4.55 | 2.02 |  |  |
| M88 O'Neil Shakeout +3 | DATA BELUM CUKUP | 6 | 0 |  | 32% |  | 5.56 | 32 | 1 | -8.00 | 0.89 |  |  |
| M93 Bollinger Kaedah II: %b + MFI | DATA BELUM CUKUP | 49 | 0 |  | 36% |  | 8.20 | 62 | 1 | -5.09 | -0.04 |  |  |
| M01 Bollinger Band + RSI | DATA BELUM CUKUP | 10 | 0 |  | 67% |  | 2.22 | 22 | 0 |  | 2.42 |  |  |
| M04 BB Squeeze Breakout | DATA BELUM CUKUP | 4 | 0 |  | 36% |  | 4.96 | 32 | 0 |  | -3.25 |  |  |
| M05 MACD Divergence + Pengesahan | DATA BELUM CUKUP | 3 | 0 |  | 35% |  | 10.85 | 108 | 0 |  | 3.14 |  |  |
| M09 Volumatic VIDYA Pivot Retest | DATA BELUM CUKUP | 2 | 0 |  | 23% |  | 1.85 | 30 | 0 |  | 1.69 |  |  |
| M100 Bulkowski Segi Empat & Segi Tiga Menaik | DATA BELUM CUKUP | 6 | 0 |  | 46% |  | 1.32 | 29 | 0 |  | 0.62 |  |  |
| M107 Golden Cross SMA50/200 | DATA BELUM CUKUP | 1 | 0 |  | 32% |  | 15.43 | 110 | 0 |  | 8.69 |  |  |
| M31 Band Walk (BB 20/2) | DATA BELUM CUKUP | 32 | 0 |  | 43% |  | 3.30 | 32 | 0 |  | -0.98 |  |  |
| M33 Supertrend + SMA10 | DATA BELUM CUKUP | 14 | 0 |  | 40% |  | 1.65 | 33 | 0 |  | 0.69 |  |  |
| M59 Anjakan Julat RSI | DATA BELUM CUKUP | 3 | 0 |  | 34% |  | 3.10 | 37 | 0 |  | 1.77 |  |  |
| M64 O'Neil Tiga Minggu Ketat | DATA BELUM CUKUP | 3 | 0 |  | 34% |  | 1.68 | 31 | 0 |  | 3.65 |  |  |
| M68 Kell Base n' Break | DATA BELUM CUKUP | 3 | 0 |  | 36% |  | 1.35 | 35 | 0 |  | -0.36 |  |  |
| M87 IBD Tapak Menaik | DATA BELUM CUKUP | 2 | 0 |  | 32% |  | 3.49 | 30 | 0 |  | 2.62 |  |  |
| M91 Stochastic Pop (Bernstein/Steckler) | DATA BELUM CUKUP | 3 | 0 |  | 42% |  | 1.63 | 18 | 0 |  | 0.77 |  |  |

Nota: lajur "Tutup (awal)" dan "Purata tutup" ialah maklumat sahaja (berat sebelah ke arah kena henti), tidak dipakai dalam ujian.
