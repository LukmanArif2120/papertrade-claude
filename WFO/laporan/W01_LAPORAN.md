# Laporan W01 — WFO stop/exit/tempoh pegangan bagi setiap kaedah (Fasa C)

Spec: `spec/SPEC_WFO_SISTEM_SWING.md`. Enjin v1.2 (beku). Alam 423 saham. Luar sampel: 1 Jan 2023 – 2 Okt 2026 (16 suku). Optuna 150 (13 kaedah), 100 (17 kaedah), 60 (55 kaedah) percubaan setiap suku (ikut kaedah), latih 3 tahun. Objektif: CAGR maks, MDD ≥ −35%.

## 1. Ringkasan

- Kaedah diuji: 85 siap; 2 tidak layak; 0 ralat.
- Penanda aras luar sampel: EW 423 32.6%, SPY 22.1%, QQQ 32.4%, M96 V1 beku 37.0%.
- Versi WFO mengalahkan varian beku sendiri: 23/85 kaedah.
- LULUS semua kriteria §7: 0 kaedah.
- LULUS jika kriteria subset diketepikan (lihat §6): 5 kaedah (M96, M102, M52, M79, M111).
- Deflated Sharpe: SR* (jangkaan maksimum nasib, 84 kaedah) = 0.92 tahunan. DSR ≥ 0.95 = kebarangkalian tinggi bukan nasib.

## 2. W01 gabungan (entry turut dipilih)

Entry calon: M96, M30, M79, M111, M74, M05, M80, M37, M04. CAGR 23.4%, MDD -32.1%, menang 36.5%, Hit10 34.8%, n 1560, subset 0/4. **DITOLAK** ≤M96 ≤EW subset 0/4

Pilihan paling kerap: entry M79 (5/16), stop ATR1.5 (3/16), exit ASAL (7/16), tmax 42 (6/16).

## 3. Semua kaedah (luar sampel, susun ikut CAGR WFO)

| # | ID | Kaedah | CAGR WFO | MDD | Menang | Hit10 | n | Hari | CAGR beku | MDD beku | Subset | DSR | Keputusan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M73 | ADX(5) > 40 + Julat Terkecil 6 Hari | 85.7% | -46.0% | 41.5% | 18.8% | 13461 | 11 | 28.2% | -27.0% | 1/4 | 0.86 | DITOLAK: MDD subset 1/4 |
| 2 | M96 | Momo India: Ranking Sharpe 3/6/12 bulan | 69.8% | -21.3% | 49.2% | 49.6% | 242 | 28 | 37.0% | -42.0% | 0/4 | 0.95 | DITOLAK: subset 0/4 |
| 3 | M21 | Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | 62.3% | -39.1% | 34.0% | 50.3% | 191 | 25 | 38.3% | -14.4% | 1/4 | 0.73 | DITOLAK: MDD subset 1/4 tumpuan |
| 4 | M81 | Bensdorp Long Trend High Momentum | 51.2% | -36.7% | 36.3% | 13.6% | 19814 | 8 | 24.5% | -20.8% | 0/4 | 0.84 | DITOLAK: MDD subset 0/4 |
| 5 | M102 | Stockbee SLTB | 46.4% | -28.4% | 36.0% | 23.7% | 7592 | 12 | 55.2% | -38.3% | 0/4 | 0.82 | DITOLAK: subset 0/4 |
| 6 | M52 | Radge Weekend Trend Trader | 42.3% | -27.8% | 38.4% | 39.2% | 2013 | 22 | 42.6% | -24.3% | 1/4 | 0.73 | DITOLAK: subset 1/4 |
| 7 | M79 | Radge: 20% Flipper | 39.7% | -25.3% | 37.7% | 34.8% | 3427 | 16 | 46.4% | -23.1% | 1/4 | 0.82 | DITOLAK: subset 1/4 |
| 8 | M111 | Sistem Volatiliti Wilder | 37.3% | -24.5% | 38.7% | 42.8% | 4451 | 29 | 31.1% | -23.5% | 1/4 | 0.77 | DITOLAK: subset 1/4 |
| 9 | M66 | IBD Undur Pertama ke Purata 50 Hari | 36.2% | -33.7% | 34.0% | 30.8% | 5362 | 18 | 95.4% | -31.1% | 0/4 | 0.79 | DITOLAK: ≤M96 subset 0/4 |
| 10 | M38 | Darvas Kotak | 36.1% | -13.6% | 37.8% | 37.5% | 389 | 25 | 22.6% | -22.9% | 0/4 | 0.89 | DITOLAK: ≤M96 subset 0/4 |
| 11 | M07 | Qullamaggie Breakout | 34.2% | -32.0% | 34.0% | 51.7% | 412 | 34 | 20.0% | -19.4% | 0/4 | 0.62 | DITOLAK: ≤M96 subset 0/4 |
| 12 | M41 | FW Penyatuan Mingguan | 34.0% | -31.6% | 40.4% | 48.9% | 1027 | 46 | 6.1% | -23.0% | 0/4 | 0.68 | DITOLAK: ≤M96 subset 0/4 tumpuan |
| 13 | M11 | NR7 Breakout + Volume | 32.6% | -37.1% | 36.0% | 36.8% | 1819 | 27 | 39.1% | -28.1% | 1/4 | 0.73 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 tumpuan |
| 14 | M12 | Parabolic SAR | 32.2% | -20.5% | 34.8% | 36.3% | 6437 | 23 | 21.5% | -31.5% | 0/4 | 0.65 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 15 | M32 | Momentum Burst | 31.9% | -24.2% | 38.1% | 48.4% | 1152 | 30 | 84.0% | -36.8% | 1/4 | 0.72 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 16 | M107 | Golden Cross SMA50/200 | 31.5% | -24.7% | 35.5% | 42.9% | 1186 | 60 | 45.9% | -31.6% | 0/4 | 0.68 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 17 | M39 | Radge Pecahan Bollinger 100 hari | 31.2% | -35.2% | 38.9% | 38.1% | 3329 | 30 | 29.6% | -25.6% | 1/4 | 0.62 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 |
| 18 | M23 | Breitstein Kapitulasi + Kesinambungan | 30.4% | -22.1% | 38.7% | 35.4% | 1665 | 22 | 31.3% | -25.2% | 0/4 | 0.63 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 19 | M90 | Pring KST | 28.2% | -27.2% | 34.6% | 35.3% | 2904 | 22 | 57.8% | -30.3% | 0/4 | 0.62 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 20 | M20 | EMA10/15 Crossover + Sudut | 27.2% | -20.9% | 31.9% | 26.4% | 8435 | 15 | 20.3% | -17.6% | 0/4 | 0.68 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 21 | M29 | EMA3 + RSI75 + Stokastik | 27.2% | -26.1% | 34.8% | 39.1% | 1027 | 32 | 16.7% | -26.5% | 0/4 | 0.61 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 22 | M35 | Pocket Pivot Morales & Kacher | 27.0% | -28.2% | 38.0% | 36.4% | 4365 | 24 | 33.5% | -22.9% | 0/4 | 0.60 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 23 | M30 | BB Free Bar + Himpitan 50/2.5 | 26.4% | -33.9% | 31.0% | 36.6% | 2308 | 27 | 75.8% | -35.6% | 0/4 | 0.63 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 24 | M19 | Sneaky Pivot (proksi harian) | 25.4% | -18.0% | 40.7% | 21.5% | 5762 | 12 | 28.1% | -19.1% | 0/4 | 0.64 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 25 | M36 | Turtle 55/20 | 25.3% | -31.2% | 36.0% | 37.5% | 4364 | 25 | 30.0% | -35.3% | 1/4 | 0.59 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 26 | M76 | Undercut & Rally pada Low Penting | 24.6% | -18.6% | 37.6% | 28.1% | 963 | 17 | 1.9% | -23.7% | 0/4 | 0.71 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 27 | M74 | Lulus Baharu Trend Template Minervini | 24.3% | -18.7% | 31.7% | 32.2% | 1551 | 20 | 39.9% | -22.4% | 0/4 | 0.61 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 28 | M09 | Volumatic VIDYA Pivot Retest | 24.1% | -16.7% | 31.4% | 39.0% | 770 | 28 | 19.0% | -24.4% | 0/4 | 0.73 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 29 | M24 | Rotasi Momentum ROC12 + SMA200 | 23.0% | -13.6% | 35.3% | 48.5% | 68 | 14 | 36.4% | -48.8% | 0/4 | 0.79 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 30 | M02 | MACD + SMA200 | 22.6% | -45.8% | 37.3% | 36.0% | 2484 | 31 | 5.6% | -38.5% | 1/4 | 0.36 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 |
| 31 | M54 | IBD Power Trend | 22.4% | -30.4% | 37.9% | 33.5% | 3631 | 22 | 43.0% | -26.8% | 1/4 | 0.48 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 32 | M14 | Walking with the Whales | 22.2% | -19.1% | 37.0% | 26.7% | 13188 | 14 | 13.0% | -25.7% | 0/4 | 0.54 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 33 | M10 | EMA3 + CCI + MACD | 21.6% | -25.9% | 35.7% | 35.3% | 1831 | 29 | 32.8% | -29.4% | 0/4 | 0.44 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 34 | M91 | Stochastic Pop (Bernstein/Steckler) | 21.5% | -20.5% | 37.2% | 31.9% | 862 | 18 | 32.8% | -22.1% | 0/4 | 0.62 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 35 | M99 | Three Line Break | 20.9% | -25.3% | 33.1% | 31.0% | 3588 | 21 | 30.3% | -23.7% | 0/4 | 0.54 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 36 | M37 | Weinstein Peringkat 2 | 20.8% | -23.0% | 43.4% | 49.3% | 373 | 29 | 46.9% | -25.3% | 0/4 | 0.51 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 37 | M89 | Chande 65sma-3cc | 20.7% | -23.1% | 36.8% | 33.1% | 2823 | 21 | 20.8% | -23.1% | 1/4 | 0.50 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 38 | M93 | Bollinger Kaedah II: %b + MFI | 20.3% | -29.6% | 35.5% | 35.4% | 4479 | 23 | 27.4% | -33.0% | 0/4 | 0.50 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 39 | M55 | Guppy GMMA | 20.0% | -24.6% | 31.0% | 26.9% | 5776 | 15 | 26.1% | -24.3% | 0/4 | 0.42 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 40 | M15 | Break & Retest + Henti ATR | 19.7% | -25.1% | 32.2% | 34.9% | 3991 | 21 | 18.8% | -30.6% | 0/4 | 0.46 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 41 | M04 | BB Squeeze Breakout | 19.7% | -25.2% | 35.6% | 40.2% | 1944 | 27 | 82.2% | -37.9% | 0/4 | 0.47 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 42 | M84 | Jarak purata bergerak MAD 21/200 | 18.7% | -33.3% | 37.5% | 40.3% | 982 | 23 | 44.2% | -43.3% | 0/4 | 0.32 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 43 | M28 | VWAP Separator + Kiss Pivot | 17.1% | -22.8% | 48.0% | 33.1% | 1611 | 20 | 0.2% | -24.7% | 0/4 | 0.48 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 44 | M34 | Carter TTM Squeeze | 16.6% | -25.9% | 37.7% | 38.9% | 2170 | 27 | 14.9% | -23.6% | 0/4 | 0.39 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 45 | M92 | CCI-50 | 16.4% | -32.1% | 35.9% | 27.0% | 8616 | 14 | 23.7% | -25.9% | 0/4 | 0.37 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 46 | M51 | O'Neil Cawan & Pemegang | 16.2% | -11.1% | 38.1% | 39.7% | 189 | 27 | 24.0% | -18.6% | 0/4 | 0.67 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 47 | M08 | SMA20 + SMA200 | 16.1% | -34.4% | 31.0% | 33.1% | 3393 | 19 | 13.6% | -35.8% | 0/4 | 0.33 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 48 | M105 | Supertrend tulen | 15.9% | -23.6% | 38.0% | 36.7% | 5749 | 21 | 29.5% | -23.9% | 0/4 | 0.34 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 49 | M78 | Alvarez Pecahan Mingguan DTAYS | 15.7% | -28.5% | 32.3% | 38.9% | 1886 | 24 | 27.0% | -22.0% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 50 | M18 | EMA9/21 Pullback | 15.6% | -25.5% | 42.6% | 22.1% | 7603 | 11 | 12.4% | -39.6% | 0/4 | 0.35 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 51 | M50 | Elder Triple Screen | 15.0% | -28.6% | 38.8% | 30.8% | 6986 | 20 | 19.6% | -22.3% | 0/4 | 0.34 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 52 | M56 | Gray & Vogel Momentum Lancar (FIP) | 14.3% | -22.2% | 35.4% | 36.3% | 113 | 12 | 63.5% | -52.5% | 0/4 | 0.37 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 53 | M05 | MACD Divergence + Pengesahan | 14.1% | -31.7% | 40.2% | 41.7% | 420 | 36 | 19.1% | -20.2% | 0/4 | 0.31 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 54 | M47 | Holy Grail Raschke | 13.3% | -19.4% | 40.1% | 25.7% | 755 | 19 | 6.9% | -16.9% | 0/4 | 0.31 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 55 | M88 | O'Neil Shakeout +3 | 13.1% | -16.7% | 35.6% | 28.0% | 786 | 10 | 14.7% | -19.1% | 0/4 | 0.33 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 56 | M03 | BB Break + Divergence RSI | 13.0% | -23.7% | 38.1% | 32.6% | 4295 | 20 | 7.0% | -29.5% | 0/4 | 0.31 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 57 | M57 | Landry Trend Knockout (TKO) | 12.8% | -32.4% | 37.9% | 40.4% | 2830 | 25 | 41.1% | -43.4% | 0/4 | 0.25 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 58 | M06 | Minervini VCP Breakout | 12.2% | -29.2% | 40.7% | 38.1% | 1414 | 22 | 46.8% | -32.0% | 0/4 | 0.25 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 59 | M59 | Anjakan Julat RSI | 12.0% | -19.1% | 38.6% | 29.8% | 1629 | 18 | 12.5% | -24.3% | 0/4 | 0.29 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 60 | M48 | Cooper 1-2-3-4 | 11.6% | -41.7% | 41.5% | 43.0% | 1170 | 29 | 22.5% | -21.0% | 1/4 | 0.24 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 |
| 61 | M68 | Kell Base n' Break | 11.4% | -22.1% | 39.7% | 37.7% | 1348 | 25 | 17.0% | -22.9% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 62 | M31 | Band Walk (BB 20/2) | 11.4% | -26.3% | 39.5% | 40.1% | 4714 | 27 | 16.3% | -34.6% | 1/4 | 0.25 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 63 | M13 | Garis Trend Action/Safety Line | 11.4% | -36.7% | 38.4% | 25.3% | 11893 | 13 | 34.3% | -27.3% | 0/4 | 0.24 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 64 | M101 | Bulkowski: Tiga lembah menaik | 11.2% | -20.4% | 32.7% | 32.5% | 878 | 22 | 47.5% | -42.2% | 0/4 | 0.25 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 65 | M77 | Undercut & Rally pada Purata Bergerak (MAU&R) | 11.2% | -31.1% | 42.5% | 39.0% | 1099 | 23 | 65.7% | -33.0% | 0/4 | 0.26 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 66 | M33 | Supertrend + SMA10 | 10.9% | -35.1% | 40.4% | 38.7% | 3158 | 25 | 26.3% | -26.2% | 0/4 | 0.26 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 67 | M70 | Pecahan Hari Dalam | 10.7% | -36.1% | 38.3% | 31.3% | 5528 | 19 | 72.5% | -30.0% | 0/4 | 0.22 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 tumpuan |
| 68 | M46 | Jurang Naik Boleh Beli (Buyable Gap Up) | 9.3% | -31.4% | 44.5% | 37.7% | 685 | 26 | 32.0% | -20.6% | 0/4 | 0.22 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 69 | M100 | Bulkowski Segi Empat & Segi Tiga Menaik | 9.2% | -20.2% | 40.3% | 28.8% | 1057 | 25 | 12.8% | -21.6% | 0/4 | 0.26 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 70 | M27 | Price Action 4 Tiang | 7.8% | -38.0% | 35.3% | 19.0% | 16490 | 11 | 25.8% | -28.2% | 0/4 | 0.18 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 71 | M95 | Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | 7.6% | -22.9% | 42.1% | 43.5% | 1955 | 32 | 56.9% | -28.5% | 0/4 | 0.18 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 72 | M106 | DMI Wilder | 7.1% | -29.7% | 34.4% | 30.8% | 2040 | 20 | 18.6% | -21.8% | 0/4 | 0.17 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 73 | M67 | Rayner Teo: Ujian Ketiga pada Purata 50 | 6.8% | -26.9% | 33.6% | 38.1% | 877 | 27 | 9.7% | -27.2% | 0/4 | 0.16 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 74 | M01 | Bollinger Band + RSI | 6.3% | -20.4% | 54.0% | 30.9% | 1424 | 12 | 10.6% | -29.5% | 0/4 | 0.16 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 75 | M94 | Pecutan Momentum (Chen, Yu & Wang) | 6.1% | -44.0% | 33.9% | 28.5% | 569 | 14 | 68.4% | -39.8% | 0/4 | 0.14 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 76 | M44 | Tapak Rata IBD | 5.3% | -20.4% | 33.7% | 31.0% | 303 | 22 | 12.6% | -15.1% | 0/4 | 0.16 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 77 | M49 | Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | 4.8% | -34.9% | 37.8% | 37.2% | 4901 | 24 | 11.8% | -28.1% | 1/4 | 0.12 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 78 | M80 | Radge Saluran Purata Bergerak (MAC) | 4.7% | -48.3% | 37.7% | 32.1% | 5519 | 20 | 5.3% | -40.5% | 0/4 | 0.12 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 79 | M82 | Arthur Hill Rotasi Sasaran 10% | 4.5% | -39.6% | 38.0% | 16.7% | 17154 | 11 | 33.4% | -26.5% | 0/4 | 0.12 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 80 | M26 | Garis Trend Undur 3 Sentuhan + Pecahan | 4.2% | -44.4% | 38.1% | 25.3% | 1323 | 16 | 9.3% | -31.9% | 0/4 | 0.11 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 81 | M25 | VWAP Wave (proksi harian) | 3.4% | -23.9% | 36.9% | 42.6% | 2814 | 30 | 10.3% | -32.8% | 1/4 | 0.10 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 82 | M87 | IBD Tapak Menaik | -0.3% | -24.7% | 34.6% | 42.4% | 191 | 28 | 20.7% | -18.7% | 0/4 | 0.05 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 83 | M104 | High Tight Flag / Power Play | -0.8% | -20.1% | 32.2% | 48.3% | 87 | 19 | 2.5% | -21.6% | 0/4 | 0.04 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 84 | M64 | O'Neil Tiga Minggu Ketat | -1.3% | -29.3% | 31.7% | 31.3% | 268 | 19 | 2.4% | -26.4% | 0/4 | 0.04 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 85 | M22 | Qullamaggie Episodic Pivot |  |  |  |  | 0 |  | 2.9% | -5.8% | 0/4 |  | DITOLAK: tiada dagangan |

## 4. Gabungan paling kerap dipilih (10 teratas)

| ID | Stop | Exit | Tmax |
|---|---|---|---|
| M73 | LOW10 (3/16) | CHAN4 (8/16) | 21 (5/16) |
| M96 | ATR2.5 (4/16) | ASAL (7/16) | 42 (6/16) |
| M21 | ATR3 (3/16) | TIADA (5/16) | 0 (6/16) |
| M81 | LOW1 (4/16) | CHAN4 (4/16) | 63 (8/16) |
| M102 | ATR3.5 (5/16) | SMA20 (14/16) | 63 (5/16) |
| M52 | ASAL (3/16) | CHAN4 (7/16) | 21 (6/16) |
| M79 | ATR3 (2/16) | CHAN4 (7/16) | 42 (5/16) |
| M111 | PCT15 (3/16) | ASAL (5/16) | 63 (6/16) |
| M66 | ATR3.5 (3/16) | CHAN4 (6/16) | 21 (5/16) |
| M38 | LOW10 (5/16) | SMA20 (6/16) | 63 (7/16) |

## 5. Tidak layak / ralat

- M40: isyarat bergantung pada pra-simulasi 8 slot kaedah sendiri
- M45: isyarat bergantung pada pra-simulasi 8 slot kaedah sendiri

## 6. Nota tafsiran

- CAGR beku = varian registry dengan stop/exit asal, dagangan masuk ≥ 1 Jan 2023, portfolio sama. Ia BUKAN luar sampel tulen (varian dipilih dengan melihat data 2019–2026).
- CAGR WFO ialah luar sampel tulen: setiap suku memakai gabungan yang dipilih atas 3 tahun sebelumnya sahaja.
- Subset: gabungan terpilih yang sama dinilai atas S1–S4 (tidak ditala semula); bilangan subset yang mengalahkan EW subset. **Kelemahan reka bentuk:** dagangan ditapis kepada ~105 saham tetapi portfolio kekal 8 slot, jadi slot banyak kosong (tunai) berbanding EW subset yang sentiasa melabur penuh; bagi kaedah merentas saham (cth. M96) hanya ~2 daripada 8 pilihan jatuh dalam setiap subset. Ujian ini berat sebelah menentang semua kaedah dan tidak setara dengan gate subset projek (yang menjalankan semula kaedah atas alam subset). Oleh itu senarai "LULUS tanpa subset" turut dilaporkan.
- n = semua dagangan calon yang dijana (konvensyen `enjin.metrik`), bukan hanya yang diambil oleh 8 slot.
- M22: tiada gabungan sah dalam mana-mana tetingkap latihan (< 30 dagangan), jadi tiada dagangan luar sampel.
- Kriteria LULUS (§7): CAGR > M96 V1 beku dan > EW; MDD ≥ −35%; n ≥ 60; subset ≥ 3/4; tiada saham > 25% keuntungan.
