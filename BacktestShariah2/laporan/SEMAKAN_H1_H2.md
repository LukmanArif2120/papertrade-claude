# Semakan Keteguhan H1 lawan H2 (Kaedah M, set 431)

Dijana oleh `standard/semak_h1_h2.py` daripada `data/registry_M_gabung.csv` (enjin v1.2, tanpa larian semula). H1 = 2019-11-01 hingga 2022-12-31; H2 = 2023-01-01 hingga hujung data. CAGR portfolio 8 slot × 12.5%.

## Penanda aras

- EW (sama rata 431): H1 16.4%, H2 27.4%, penuh 21.9%
- SPY: H1 9.1%, H2 22.1%, penuh 15.9%
- QQQ: H1 10.4%, H2 32.4%, penuh 21.7%

## Takrif label

- **TEGUH**: CAGR mengalahkan EW dalam H1 DAN H2, dan menang EW dalam ≥ 3/4 subset S1–S4.
- **TEGUH (subset lemah)**: menang EW dalam kedua-dua separuh tetapi < 3/4 subset.
- **SATU SEPARUH**: menang EW dalam satu separuh sahaja (kemungkinan bergantung pada rejim pasaran).
- **LEMAH**: kalah EW dalam kedua-dua separuh.
- Kedudukan: bilangan separuh menang, kemudian lebihan minimum atas EW (separuh yang lebih lemah).

## Ringkasan

- SATU SEPARUH: 70 kaedah
- LEMAH: 31 kaedah
- TEGUH (subset lemah): 30 kaedah
- TEGUH: 9 kaedah
- Korelasi kedudukan (Spearman) H1 lawan H2: 0.31 (550 varian), 0.06 (88 varian dipilih). Hampir 0 = prestasi H1 tidak meramal H2; ≥ 0.5 = konsisten.
- 10 kaedah teratas ikut H1 sahaja: 7/10 mengalahkan EW dalam H2; median H2 50.2% (EW 27.4%).
- Bias pemilihan varian: median H2 varian dipilih (data penuh) 32.8% lawan varian dipilih ikut H1 sahaja 25.1%; 43/88 kaedah memilih varian berbeza, dan bagi kaedah itu purata H2 jatuh 23.5%. Beza positif = sebahagian prestasi H2 datang daripada memilih varian selepas melihat H2.

## Kedudukan semua kaedah

| # | ID | Kaedah | Keputusan | Skor | H1 | H2 | H1−EW | H2−EW | Subset menang EW | Label | H2 jika pilih ikut H1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M167 | Momentum Semalaman (Lou, Polk & Skouras) | GUNA | 83.1 | 44.8% | 55.3% | 28.4% | 27.9% | 3/4 | TEGUH | 55.3% |
| 2 | M166 | Titik Pusing Momentum (Goulding, Harvey & Mazzoleni) | GUNA | 83.0 | 41.5% | 73.4% | 25.2% | 46.0% | 4/4 | TEGUH | 22.0% |
| 3 | M24 | Rotasi Momentum ROC12 + SMA200 | DITOLAK (G1 G2 G4) |  | 40.6% | 76.0% | 24.2% | 48.6% | 4/4 | TEGUH | 76.0% |
| 4 | M114 | RS Peneraju Pasaran Naik | GUNA | 77.4 | 35.9% | 64.7% | 19.5% | 37.3% | 4/4 | TEGUH | 64.7% |
| 5 | M125 | 2-Bar Breakout | DITOLAK (G1 G4) |  | 34.2% | 57.6% | 17.8% | 30.2% | 1/4 | TEGUH (subset lemah) | 57.6% |
| 6 | M18 | EMA9/21 Pullback | UJI KERTAS | 66.0 | 43.5% | 45.0% | 27.2% | 17.6% | 1/4 | TEGUH (subset lemah) | 45.0% |
| 7 | M30 | BB Free Bar + Himpitan 50/2.5 | GUNA | 76.2 | 32.4% | 71.9% | 16.0% | 44.5% | 1/4 | TEGUH (subset lemah) | 71.9% |
| 8 | M111 | Sistem Volatiliti Wilder | UJI KERTAS | 74.2 | 31.2% | 54.1% | 14.8% | 26.7% | 1/4 | TEGUH (subset lemah) | 54.1% |
| 9 | M74 | Lulus Baharu Trend Template Minervini | UJI KERTAS | 73.2 | 34.0% | 39.9% | 17.6% | 12.5% | 2/4 | TEGUH (subset lemah) | 39.9% |
| 10 | M13 | Garis Trend Action/Safety Line | UJI KERTAS | 65.2 | 28.7% | 76.9% | 12.3% | 49.5% | 2/4 | TEGUH (subset lemah) | 22.4% |
| 11 | M79 | Radge: 20% Flipper | GUNA | 75.9 | 27.9% | 43.2% | 11.5% | 15.8% | 4/4 | TEGUH | 43.2% |
| 12 | M162 | Momentum Residual (Blitz, Huij & Martens) | UJI KERTAS | 72.1 | 27.5% | 50.3% | 11.1% | 22.9% | 4/4 | TEGUH | 50.3% |
| 13 | M54 | IBD Power Trend | UJI KERTAS | 63.1 | 24.7% | 37.9% | 8.4% | 10.5% | 1/4 | TEGUH (subset lemah) | 37.9% |
| 14 | M12 | Parabolic SAR | UJI KERTAS | 69.5 | 24.5% | 37.7% | 8.1% | 10.3% | 2/4 | TEGUH (subset lemah) | 37.7% |
| 15 | M140 | 猎豹出击 (Serangan Cheetah) | DITOLAK (G4) |  | 24.0% | 50.2% | 7.6% | 22.8% | 2/4 | TEGUH (subset lemah) | 50.2% |
| 16 | M04 | BB Squeeze Breakout | UJI KERTAS | 67.5 | 23.2% | 69.9% | 6.8% | 42.5% | 3/4 | TEGUH | 69.9% |
| 17 | M84 | Jarak purata bergerak MAD 21/200 | UJI KERTAS | 63.3 | 22.8% | 42.7% | 6.5% | 15.3% | 2/4 | TEGUH (subset lemah) | 42.7% |
| 18 | M55 | Guppy GMMA | UJI KERTAS | 60.9 | 24.4% | 33.7% | 8.1% | 6.3% | 1/4 | TEGUH (subset lemah) | 33.7% |
| 19 | M160 | Measured Move Up | UJI KERTAS | 64.5 | 22.5% | 51.7% | 6.1% | 24.3% | 0/4 | TEGUH (subset lemah) | 51.7% |
| 20 | M96 | Momo India: Ranking Sharpe 3/6/12 bulan | GUNA | 80.3 | 22.5% | 57.7% | 6.1% | 30.3% | 2/4 | TEGUH (subset lemah) | 47.1% |
| 21 | M57 | Landry Trend Knockout (TKO) | UJI KERTAS | 60.8 | 22.5% | 43.4% | 6.1% | 16.0% | 0/4 | TEGUH (subset lemah) | 22.7% |
| 22 | M56 | Gray & Vogel Momentum Lancar (FIP) | DITOLAK (G1 G4) |  | 21.9% | 61.8% | 5.5% | 34.4% | 3/4 | TEGUH | 11.7% |
| 23 | M80 | Radge Saluran Purata Bergerak (MAC) | UJI KERTAS | 71.6 | 46.3% | 32.7% | 30.0% | 5.3% | 2/4 | TEGUH (subset lemah) | 32.7% |
| 24 | M151 | Outside Bar Failure | UJI KERTAS | 67.3 | 21.7% | 39.9% | 5.3% | 12.5% | 0/4 | TEGUH (subset lemah) | 39.9% |
| 25 | M41 | FW Penyatuan Mingguan | UJI KERTAS | 60.5 | 20.2% | 34.7% | 3.9% | 7.3% | 2/4 | TEGUH (subset lemah) | 34.7% |
| 26 | M144 | Screw Bar | UJI KERTAS | 71.9 | 20.2% | 32.2% | 3.8% | 4.8% | 0/4 | TEGUH (subset lemah) | 32.2% |
| 27 | M77 | Undercut & Rally pada Purata Bergerak (MAU&R) | UJI KERTAS | 63.4 | 19.9% | 64.5% | 3.5% | 37.1% | 1/4 | TEGUH (subset lemah) | 64.5% |
| 28 | M27 | Price Action 4 Tiang | SIMPAN | 55.5 | 19.8% | 43.5% | 3.4% | 16.1% | 1/4 | TEGUH (subset lemah) | 43.5% |
| 29 | M137 | Livermore System | SIMPAN | 59.2 | 19.7% | 33.6% | 3.4% | 6.1% | 2/4 | TEGUH (subset lemah) | 33.6% |
| 30 | M163 | Kekuatan Mutlak (Gulen & Petkova) | UJI KERTAS | 71.6 | 19.5% | 56.9% | 3.1% | 29.5% | 3/4 | TEGUH | 56.9% |
| 31 | M46 | Jurang Naik Boleh Beli (Buyable Gap Up) | UJI KERTAS | 69.5 | 19.0% | 33.2% | 2.6% | 5.8% | 0/4 | TEGUH (subset lemah) | 25.2% |
| 32 | M139 | 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | SIMPAN | 56.9 | 18.7% | 30.6% | 2.3% | 3.1% | 0/4 | TEGUH (subset lemah) | 30.6% |
| 33 | M102 | Stockbee SLTB | SIMPAN | 58.6 | 18.3% | 56.9% | 1.9% | 29.5% | 1/4 | TEGUH (subset lemah) | 20.8% |
| 34 | M165 | Momentum Industri (Moskowitz & Grinblatt) | SIMPAN | 51.5 | 20.4% | 29.3% | 4.0% | 1.9% | 1/4 | TEGUH (subset lemah) | 29.3% |
| 35 | M19 | Sneaky Pivot (proksi harian) | SIMPAN | 48.6 | 18.2% | 33.2% | 1.8% | 5.8% | 0/4 | TEGUH (subset lemah) | 33.2% |
| 36 | M05 | MACD Divergence + Pengesahan | UJI KERTAS | 71.8 | 18.1% | 38.2% | 1.7% | 10.8% | 1/4 | TEGUH (subset lemah) | 24.9% |
| 37 | M52 | Radge Weekend Trend Trader | UJI KERTAS | 66.7 | 18.1% | 38.1% | 1.7% | 10.7% | 2/4 | TEGUH (subset lemah) | 38.1% |
| 38 | M81 | Bensdorp Long Trend High Momentum | SIMPAN | 57.1 | 17.8% | 38.9% | 1.4% | 11.5% | 1/4 | TEGUH (subset lemah) | 38.9% |
| 39 | M91 | Stochastic Pop (Bernstein/Steckler) | SIMPAN | 58.5 | 17.6% | 32.5% | 1.3% | 5.1% | 0/4 | TEGUH (subset lemah) | 32.5% |
| 40 | M40 | Clenow Stocks on the Move | UJI KERTAS | 68.9 | 25.9% | 26.6% | 9.5% | -0.8% | 1/4 | SATU SEPARUH | 26.6% |
| 41 | M39 | Radge Pecahan Bollinger 100 hari | SIMPAN | 54.7 | 21.8% | 25.5% | 5.4% | -1.9% | 0/4 | SATU SEPARUH | 25.5% |
| 42 | M152 | Spike & Ledge | SIMPAN | 50.8 | 14.3% | 27.9% | -2.0% | 0.5% | 0/4 | SATU SEPARUH | 27.9% |
| 43 | M99 | Three Line Break | SIMPAN | 47.9 | 13.6% | 30.5% | -2.8% | 3.1% | 0/4 | SATU SEPARUH | 30.5% |
| 44 | M118 | Expansion Pivot (Cooper) | SIMPAN | 48.2 | 13.5% | 35.2% | -2.9% | 7.8% | 0/4 | SATU SEPARUH | 35.2% |
| 45 | M158 | Doubly Adaptive Profit Targets | UJI KERTAS | 65.8 | 13.4% | 62.4% | -3.0% | 35.0% | 0/4 | SATU SEPARUH | 62.4% |
| 46 | M156 | Single Penetration (DiNapoli) | DITOLAK (G4) |  | 13.3% | 35.3% | -3.1% | 7.9% | 0/4 | SATU SEPARUH | 35.3% |
| 47 | M105 | Supertrend tulen | UJI KERTAS | 65.3 | 36.0% | 24.3% | 19.7% | -3.1% | 0/4 | SATU SEPARUH | 24.3% |
| 48 | M146 | 3-Bar Momentum Pattern | SIMPAN | 58.9 | 12.7% | 59.7% | -3.7% | 32.3% | 0/4 | SATU SEPARUH | 59.7% |
| 49 | M29 | EMA3 + RSI75 + Stokastik | SIMPAN | 51.2 | 21.3% | 23.6% | 4.9% | -3.8% | 0/4 | SATU SEPARUH | 13.0% |
| 50 | M48 | Cooper 1-2-3-4 | SIMPAN | 48.6 | 23.7% | 23.4% | 7.3% | -4.0% | 0/4 | SATU SEPARUH | 23.4% |
| 51 | M134 | First Kiss After Daylight (Landry) | SIMPAN | 46.1 | 11.8% | 30.3% | -4.5% | 2.9% | 1/4 | SATU SEPARUH | 30.3% |
| 52 | M73 | ADX(5) > 40 + Julat Terkecil 6 Hari | DITOLAK (G1 G4) |  | 11.7% | 29.4% | -4.7% | 2.0% | 0/4 | SATU SEPARUH | 16.1% |
| 53 | M93 | Bollinger Kaedah II: %b + MFI | SIMPAN | 47.9 | 11.6% | 35.1% | -4.8% | 7.7% | 2/4 | SATU SEPARUH | 35.1% |
| 54 | M10 | EMA3 + CCI + MACD | UJI KERTAS | 65.0 | 10.6% | 47.0% | -5.8% | 19.6% | 0/4 | SATU SEPARUH | 24.1% |
| 55 | M92 | CCI-50 | SIMPAN | 57.9 | 36.7% | 21.5% | 20.3% | -5.9% | 2/4 | SATU SEPARUH | 21.5% |
| 56 | M129 | Wick Play | SIMPAN | 50.8 | 17.5% | 21.3% | 1.1% | -6.1% | 0/4 | SATU SEPARUH | 21.3% |
| 57 | M37 | Weinstein Peringkat 2 | UJI KERTAS | 67.7 | 10.2% | 48.9% | -6.2% | 21.5% | 0/4 | SATU SEPARUH | 38.0% |
| 58 | M128 | Inventory Retracement Bar (IRB, Rob Hoffman) | SIMPAN | 52.0 | 10.0% | 44.0% | -6.4% | 16.6% | 1/4 | SATU SEPARUH | 44.0% |
| 59 | M11 | NR7 Breakout + Volume | SIMPAN | 57.9 | 9.8% | 49.9% | -6.6% | 22.5% | 1/4 | SATU SEPARUH | 14.0% |
| 60 | M89 | Chande 65sma-3cc | SIMPAN | 56.3 | 33.7% | 20.8% | 17.3% | -6.6% | 0/4 | SATU SEPARUH | 20.8% |
| 61 | M20 | EMA10/15 Crossover + Sudut | SIMPAN | 39.7 | 18.6% | 20.7% | 2.2% | -6.7% | 0/4 | SATU SEPARUH | 8.2% |
| 62 | M147 | Improved Three-Bar Pullback | DITOLAK (G1) |  | 9.1% | 40.1% | -7.3% | 12.7% | 2/4 | SATU SEPARUH | 40.1% |
| 63 | M78 | Alvarez Pecahan Mingguan DTAYS | SIMPAN | 51.5 | 24.3% | 20.1% | 7.9% | -7.3% | 1/4 | SATU SEPARUH | 20.1% |
| 64 | M124 | 'Last' Stochastic Technique (ChartSchool) | SIMPAN | 44.4 | 25.1% | 20.1% | 8.7% | -7.4% | 0/4 | SATU SEPARUH | 20.1% |
| 65 | M88 | O'Neil Shakeout +3 | SIMPAN | 52.8 | 25.2% | 20.0% | 8.9% | -7.4% | 2/4 | SATU SEPARUH | 20.0% |
| 66 | M148 | Natural Number Method | SIMPAN | 34.7 | 8.9% | 30.6% | -7.5% | 3.2% | 0/4 | SATU SEPARUH | 30.6% |
| 67 | M149 | 3-Step Pullback | SIMPAN | 41.0 | 8.8% | 35.8% | -7.6% | 8.3% | 1/4 | SATU SEPARUH | 35.8% |
| 68 | M82 | Arthur Hill Rotasi Sasaran 10% | DITOLAK (G1) |  | 8.8% | 32.2% | -7.6% | 4.8% | 0/4 | SATU SEPARUH | 22.5% |
| 69 | M90 | Pring KST | SIMPAN | 59.9 | 8.6% | 63.9% | -7.7% | 36.5% | 0/4 | SATU SEPARUH | 13.1% |
| 70 | M09 | Volumatic VIDYA Pivot Retest | SIMPAN | 54.3 | 30.7% | 19.4% | 14.3% | -8.0% | 0/4 | SATU SEPARUH | 19.4% |
| 71 | M123 | CCI Correction (Lambert, ChartSchool) | SIMPAN | 55.1 | 8.3% | 74.4% | -8.1% | 47.0% | 1/4 | SATU SEPARUH | 74.4% |
| 72 | M119 | 180 Bullish (Cooper) | SIMPAN | 40.7 | 8.0% | 36.5% | -8.4% | 9.1% | 1/4 | SATU SEPARUH | 36.5% |
| 73 | M66 | IBD Undur Pertama ke Purata 50 Hari | UJI KERTAS | 66.7 | 7.9% | 101.2% | -8.5% | 73.8% | 0/4 | SATU SEPARUH | 101.2% |
| 74 | M94 | Pecutan Momentum (Chen, Yu & Wang) | DITOLAK (G1) |  | 7.7% | 77.2% | -8.7% | 49.8% | 4/4 | SATU SEPARUH | 19.2% |
| 75 | M106 | DMI Wilder | SIMPAN | 37.3 | 18.7% | 18.0% | 2.3% | -9.4% | 0/4 | SATU SEPARUH | 4.8% |
| 76 | M161 | EMA 10/21 + Supertrend (10,3) | SIMPAN | 42.5 | 23.6% | 17.6% | 7.2% | -9.8% | 0/4 | SATU SEPARUH | 17.6% |
| 77 | M45 | High 52 Minggu (George & Hwang) | UJI KERTAS | 64.7 | 6.6% | 55.6% | -9.8% | 28.2% | 1/4 | SATU SEPARUH | 18.9% |
| 78 | M08 | SMA20 + SMA200 | SIMPAN | 46.0 | 30.5% | 17.3% | 14.1% | -10.1% | 1/4 | SATU SEPARUH | 5.2% |
| 79 | M130 | 多方炮 (dua lilin hijau mengapit satu merah) | UJI KERTAS | 67.6 | 4.8% | 69.6% | -11.6% | 42.2% | 3/4 | SATU SEPARUH | 69.6% |
| 80 | M132 | Ascending Scallop (Bulkowski) | SIMPAN | 34.1 | 4.7% | 30.5% | -11.7% | 3.1% | 0/4 | SATU SEPARUH | 30.5% |
| 81 | M116 | 2/20 EMA Breakout (Landry) | SIMPAN | 23.0 | 4.5% | 32.8% | -11.9% | 5.4% | 0/4 | SATU SEPARUH | 32.8% |
| 82 | M154 | HOLP (High of Low Period) | SIMPAN | 40.6 | 4.2% | 38.2% | -12.1% | 10.8% | 0/4 | SATU SEPARUH | 38.2% |
| 83 | M32 | Momentum Burst | UJI KERTAS | 62.7 | 4.2% | 88.1% | -12.2% | 60.7% | 2/4 | SATU SEPARUH | 31.0% |
| 84 | M142 | Pecahan volum dari dasar (底部放量) | UJI KERTAS | 72.7 | 3.9% | 63.3% | -12.4% | 35.9% | 2/4 | SATU SEPARUH | 63.3% |
| 85 | M136 | Short/Intermediate-term Low (Larry Williams) | DITOLAK (G4) |  | 3.8% | 40.1% | -12.5% | 12.7% | 0/4 | SATU SEPARUH | 40.1% |
| 86 | M70 | Pecahan Hari Dalam | SIMPAN | 54.5 | 3.6% | 76.0% | -12.7% | 48.6% | 0/4 | SATU SEPARUH | 7.6% |
| 87 | M131 | Ross Hook (Joe Ross) | DITOLAK (G4) |  | 3.5% | 42.4% | -12.8% | 15.0% | 1/4 | SATU SEPARUH | 42.4% |
| 88 | M95 | Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | SIMPAN | 48.1 | 2.8% | 53.5% | -13.5% | 26.1% | 0/4 | SATU SEPARUH | 19.4% |
| 89 | M26 | Garis Trend Undur 3 Sentuhan + Pecahan | SIMPAN | 33.3 | 2.8% | 39.0% | -13.6% | 11.6% | 0/4 | SATU SEPARUH | 11.5% |
| 90 | M122 | Moving Momentum (ChartSchool) | SIMPAN | 29.7 | 2.4% | 31.2% | -14.0% | 3.8% | 0/4 | SATU SEPARUH | 31.2% |
| 91 | M150 | Trend Bar Failure (Brooks) | SIMPAN | 39.4 | 1.7% | 40.0% | -14.7% | 12.6% | 0/4 | SATU SEPARUH | 40.0% |
| 92 | M06 | Minervini VCP Breakout | SIMPAN | 40.1 | 1.0% | 45.9% | -15.3% | 18.5% | 0/4 | SATU SEPARUH | 1.7% |
| 93 | M100 | Bulkowski Segi Empat & Segi Tiga Menaik | DITOLAK (G3) |  | 18.8% | 12.0% | 2.4% | -15.4% | 0/4 | SATU SEPARUH | 12.0% |
| 94 | M49 | Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | DITOLAK (G3) |  | 19.6% | 11.7% | 3.3% | -15.7% | 2/4 | SATU SEPARUH | 11.7% |
| 95 | M153 | Range Leader | SIMPAN | 23.4 | 0.5% | 37.0% | -15.9% | 9.6% | 0/4 | SATU SEPARUH | 37.0% |
| 96 | M101 | Bulkowski: Tiga lembah menaik | SIMPAN | 33.8 | 0.5% | 43.8% | -15.9% | 16.3% | 0/4 | SATU SEPARUH | 2.3% |
| 97 | M14 | Walking with the Whales | SIMPAN | 35.6 | 36.3% | 10.6% | 19.9% | -16.8% | 1/4 | SATU SEPARUH | 10.6% |
| 98 | M35 | Pocket Pivot Morales & Kacher | DITOLAK (G3 G5) |  | -1.6% | 31.2% | -17.9% | 3.8% | 0/4 | SATU SEPARUH | 31.2% |
| 99 | M127 | Slingshot Bullish | DITOLAK (G4 G5) |  | -1.6% | 53.1% | -18.0% | 25.7% | 0/4 | SATU SEPARUH | 53.1% |
| 100 | M23 | Breitstein Kapitulasi + Kesinambungan | DITOLAK (G5) |  | -2.2% | 36.2% | -18.6% | 8.8% | 0/4 | SATU SEPARUH | -3.5% |
| 101 | M67 | Rayner Teo: Ujian Ketiga pada Purata 50 | SIMPAN | 34.6 | 30.4% | 8.5% | 14.1% | -19.0% | 0/4 | SATU SEPARUH | 8.5% |
| 102 | M03 | BB Break + Divergence RSI | DITOLAK (G3 G4) |  | 23.4% | 8.3% | 7.1% | -19.1% | 0/4 | SATU SEPARUH | 3.8% |
| 103 | M126 | Hidden Smash Day (beli, Larry Williams) | DITOLAK (G5) |  | -3.6% | 67.9% | -19.9% | 40.5% | 0/4 | SATU SEPARUH | 67.9% |
| 104 | M21 | Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | DITOLAK (G5) |  | -4.2% | 44.5% | -20.6% | 17.1% | 0/4 | SATU SEPARUH | 6.5% |
| 105 | M141 | First Thrust (Landry) | DITOLAK (G3 G5) |  | -5.4% | 29.3% | -21.8% | 1.9% | 0/4 | SATU SEPARUH | 29.3% |
| 106 | M02 | MACD + SMA200 | DITOLAK (G3) |  | 30.3% | 4.8% | 13.9% | -22.6% | 0/4 | SATU SEPARUH | 0.5% |
| 107 | M159 | Heikin-Ashi Trend | DITOLAK (G5) |  | -6.2% | 45.9% | -22.6% | 18.5% | 0/4 | SATU SEPARUH | 45.9% |
| 108 | M104 | High Tight Flag / Power Play | DITOLAK (G3) |  | 28.5% | 3.6% | 12.2% | -23.8% | 0/4 | SATU SEPARUH | 3.6% |
| 109 | M76 | Undercut & Rally pada Low Penting | DITOLAK (G3) |  | 18.1% | 1.1% | 1.8% | -26.3% | 0/4 | SATU SEPARUH | 1.1% |
| 110 | M33 | Supertrend + SMA10 | SIMPAN | 47.9 | 16.0% | 26.2% | -0.4% | -1.2% | 0/4 | LEMAH | 15.2% |
| 111 | M133 | Bull Hook (Crabel) | SIMPAN | 40.3 | 14.1% | 26.0% | -2.3% | -1.4% | 0/4 | LEMAH | 26.0% |
| 112 | M155 | Market Cycle Strategy | DITOLAK (G4) |  | 12.2% | 27.2% | -4.2% | -0.2% | 1/4 | LEMAH | 27.2% |
| 113 | M15 | Break & Retest + Henti ATR | SIMPAN | 37.1 | 11.8% | 25.6% | -4.6% | -1.8% | 1/4 | LEMAH | 25.6% |
| 114 | M121 | High 2 bull flag (Brooks) | DITOLAK (G1) |  | 11.7% | 23.5% | -4.7% | -3.9% | 0/4 | LEMAH | 23.5% |
| 115 | M87 | IBD Tapak Menaik | DITOLAK (G3) |  | 10.8% | 20.6% | -5.5% | -6.8% | 0/4 | LEMAH | 20.6% |
| 116 | M135 | 3rd Watch | SIMPAN | 43.2 | 9.5% | 22.1% | -6.8% | -5.3% | 0/4 | LEMAH | 22.1% |
| 117 | M34 | Carter TTM Squeeze | DITOLAK (G3) |  | 8.8% | 20.5% | -7.6% | -6.9% | 1/4 | LEMAH | 3.5% |
| 118 | M50 | Elder Triple Screen | DITOLAK (G3) |  | 8.5% | 21.4% | -7.9% | -6.0% | 0/4 | LEMAH | 16.2% |
| 119 | M31 | Band Walk (BB 20/2) | DITOLAK (G3) |  | 10.9% | 18.5% | -5.5% | -8.9% | 1/4 | LEMAH | 18.5% |
| 120 | M107 | Golden Cross SMA50/200 | SIMPAN | 39.5 | 16.3% | 17.5% | -0.1% | -9.9% | 0/4 | LEMAH | 17.5% |
| 121 | M38 | Darvas Kotak | DITOLAK (G1 G3) |  | 5.9% | 23.7% | -10.5% | -3.7% | 0/4 | LEMAH | 8.7% |
| 122 | M01 | Bollinger Band + RSI | DITOLAK (G1 G3 G4) |  | 11.7% | 14.2% | -4.6% | -13.2% | 0/4 | LEMAH | 9.3% |
| 123 | M157 | Consolidation Pivot Breakout (versi angka) | DITOLAK (G3) |  | 3.5% | 13.9% | -12.8% | -13.5% | 1/4 | LEMAH | 13.9% |
| 124 | M07 | Qullamaggie Breakout | DITOLAK (G3) |  | 2.9% | 19.9% | -13.5% | -7.6% | 0/4 | LEMAH | 16.7% |
| 125 | M44 | Tapak Rata IBD | DITOLAK (G3) |  | 2.0% | 13.9% | -14.4% | -13.5% | 0/4 | LEMAH | 3.6% |
| 126 | M120 | Reversal New Highs | DITOLAK (G3) |  | 1.8% | 19.0% | -14.5% | -8.4% | 0/4 | LEMAH | 19.0% |
| 127 | M25 | VWAP Wave (proksi harian) | DITOLAK (G3) |  | 3.1% | 11.9% | -13.3% | -15.5% | 0/4 | LEMAH | 0.8% |
| 128 | M59 | Anjakan Julat RSI | DITOLAK (G3 G4) |  | 8.1% | 11.6% | -8.2% | -15.8% | 0/4 | LEMAH | 3.0% |
| 129 | M115 | Bow Tie (Landry) | DITOLAK (G3 G5) |  | -0.4% | 16.3% | -16.8% | -11.1% | 0/4 | LEMAH | 16.3% |
| 130 | M145 | Yum-Yum Continuation | DITOLAK (G1 G3) |  | 12.9% | 9.9% | -3.5% | -17.5% | 0/4 | LEMAH | 9.9% |
| 131 | M143 | 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | DITOLAK (G3 G5) |  | -1.2% | 13.5% | -17.5% | -13.9% | 0/4 | LEMAH | 13.5% |
| 132 | M36 | Turtle 55/20 | DITOLAK (G3 G5) |  | -2.6% | 27.1% | -18.9% | -0.3% | 1/4 | LEMAH | 17.0% |
| 133 | M51 | O'Neil Cawan & Pemegang | DITOLAK (G3 G5) |  | -2.7% | 23.4% | -19.1% | -4.0% | 0/4 | LEMAH | 23.4% |
| 134 | M117 | Landry Pullback (high 2 bulan) | DITOLAK (G3 G5) |  | -0.7% | 8.1% | -17.1% | -19.3% | 0/4 | LEMAH | 8.1% |
| 135 | M68 | Kell Base n' Break | DITOLAK (G3 G5) |  | -3.6% | 18.6% | -19.9% | -8.8% | 0/4 | LEMAH | -0.2% |
| 136 | M47 | Holy Grail Raschke | DITOLAK (G3) |  | 5.2% | 6.5% | -11.2% | -20.9% | 0/4 | LEMAH | 3.2% |
| 137 | M138 | 直升机空中加油 (Helikopter isi minyak di udara) | DITOLAK (G1 G3 G5) |  | -5.5% | 18.7% | -21.9% | -8.7% | 0/4 | LEMAH | 18.7% |
| 138 | M64 | O'Neil Tiga Minggu Ketat | DITOLAK (G3) |  | 7.6% | 3.4% | -8.7% | -24.0% | 0/4 | LEMAH | 0.0% |
| 139 | M28 | VWAP Separator + Kiss Pivot | DITOLAK (G3) |  | 2.0% | 2.9% | -14.4% | -24.6% | 0/4 | LEMAH | 2.9% |
| 140 | M22 | Qullamaggie Episodic Pivot | DITOLAK (G2 G3) |  | 2.5% | 2.5% | -13.9% | -24.9% | 0/4 | LEMAH | 2.5% |

## Had

- Bias survivorship: set 431 ialah senarai Shariah semasa; saham delist atau dahulu bukan Shariah tiada. Ia menaikkan CAGR semua kaedah dan EW, jadi perbandingan relatif lawan EW kurang terjejas.
- H1 dan H2 bukan ujian luar sampel sebenar: spec kaedah dan varian disusun selepas data 2019–2026 dilihat.
- Subset S1–S4 hanya ada bagi satu varian setiap kaedah; "–" = tiada baris subset bagi varian dipilih.
