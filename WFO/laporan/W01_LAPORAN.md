# Laporan W01 — WFO stop/exit/tempoh pegangan bagi setiap kaedah (Fasa C)

Spec: `spec/SPEC_WFO_SISTEM_SWING.md`. Enjin v1.2 (beku) melalui salinan laju yang disahkan setara (`laporan/ENJIN_LAJU_SAHKAN.md`). Alam 423 saham. Luar sampel: 1 Jan 2023 – 2 Okt 2026 (16 suku). Optuna 150 (132 kaedah) percubaan setiap suku (ikut kaedah), latih 3 tahun. Objektif: CAGR maks, MDD ≥ −35%.

## 1. Ringkasan

- Kaedah diuji: 132 siap; 2 tidak layak; 0 ralat.
- Penanda aras luar sampel: EW 423 32.6%, SPY 22.1%, QQQ 32.4%, M96 V1 beku 37.0%.
- Versi WFO mengalahkan varian beku sendiri: 52/132 kaedah.
- LULUS semua kriteria §7: 0 kaedah.
- LULUS jika kriteria subset diketepikan (lihat §7): 8 kaedah (M81, M96, M119, M54, M73, M32, M30, M137).
- Deflated Sharpe: SR* (jangkaan maksimum nasib, 131 kaedah) = 0.95 tahunan. DSR ≥ 0.95 = kebarangkalian tinggi bukan nasib.

## 2. W01 gabungan (entry turut dipilih)

Entry calon: M96, M30, M79, M111, M74, M05, M80, M37, M04. CAGR 27.7%, MDD -36.8%, menang 35.7%, Hit10 30.4%, n 2030, subset 0/4. **DITOLAK** ≤M96 ≤EW MDD subset 0/4

Pilihan paling kerap: entry M79 (7/16), stop ATR1.5 (5/16), exit CHAN2 (4/16), tmax 42 (7/16).

## 3. Semua kaedah (luar sampel, susun ikut CAGR WFO)

| # | ID | Kaedah | CAGR WFO | MDD | Menang | Hit10 | n | Hari | CAGR beku | MDD beku | Subset | DSR | Keputusan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M21 | Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | 62.1% | -38.9% | 34.2% | 51.1% | 190 | 26 | 38.3% | -14.4% | 1/4 | 0.70 | DITOLAK: MDD subset 1/4 tumpuan |
| 2 | M81 | Bensdorp Long Trend High Momentum | 61.8% | -31.8% | 35.3% | 14.4% | 18856 | 9 | 24.5% | -20.8% | 2/4 | 0.90 | DITOLAK: subset 2/4 |
| 3 | M140 | 猎豹出击 (Serangan Cheetah) | 58.9% | -44.0% | 39.2% | 52.0% | 475 | 50 | 38.7% | -33.1% | 2/4 | 0.71 | DITOLAK: MDD subset 2/4 tumpuan |
| 4 | M96 | Momo India: Ranking Sharpe 3/6/12 bulan | 53.9% | -22.6% | 48.2% | 54.4% | 228 | 29 | 37.0% | -42.0% | 0/4 | 0.86 | DITOLAK: subset 0/4 |
| 5 | M136 | Short/Intermediate-term Low (Larry Williams) | 51.2% | -42.6% | 34.7% | 20.8% | 14013 | 13 | 6.2% | -42.1% | 1/4 | 0.79 | DITOLAK: MDD subset 1/4 |
| 6 | M125 | 2-Bar Breakout | 48.6% | -40.0% | 38.1% | 27.2% | 16276 | 16 | 14.4% | -37.7% | 1/4 | 0.86 | DITOLAK: MDD subset 1/4 |
| 7 | M119 | 180 Bullish (Cooper) | 42.6% | -30.0% | 40.0% | 37.8% | 3047 | 29 | 37.4% | -48.5% | 1/4 | 0.70 | DITOLAK: subset 1/4 |
| 8 | M54 | IBD Power Trend | 41.8% | -28.4% | 36.5% | 34.5% | 3323 | 24 | 43.0% | -26.8% | 0/4 | 0.74 | DITOLAK: subset 0/4 |
| 9 | M73 | ADX(5) > 40 + Julat Terkecil 6 Hari | 41.1% | -20.0% | 41.9% | 19.7% | 13734 | 11 | 28.2% | -27.0% | 0/4 | 0.79 | DITOLAK: subset 0/4 |
| 10 | M32 | Momentum Burst | 41.1% | -25.0% | 37.1% | 48.4% | 1152 | 30 | 84.0% | -36.8% | 0/4 | 0.83 | DITOLAK: subset 0/4 |
| 11 | M30 | BB Free Bar + Himpitan 50/2.5 | 40.0% | -34.0% | 32.9% | 40.3% | 2273 | 31 | 75.8% | -35.6% | 2/4 | 0.80 | DITOLAK: subset 2/4 |
| 12 | M41 | FW Penyatuan Mingguan | 39.1% | -33.6% | 40.0% | 49.9% | 1026 | 48 | 6.1% | -23.0% | 0/4 | 0.74 | DITOLAK: subset 0/4 tumpuan |
| 13 | M137 | Livermore System | 37.6% | -26.7% | 34.9% | 38.4% | 2735 | 34 | 24.7% | -33.1% | 0/4 | 0.72 | DITOLAK: subset 0/4 |
| 14 | M55 | Guppy GMMA | 36.5% | -29.6% | 31.1% | 30.0% | 5118 | 19 | 26.1% | -24.3% | 0/4 | 0.71 | DITOLAK: ≤M96 subset 0/4 |
| 15 | M102 | Stockbee SLTB | 36.1% | -25.7% | 36.4% | 26.2% | 7020 | 13 | 55.2% | -38.3% | 0/4 | 0.72 | DITOLAK: ≤M96 subset 0/4 |
| 16 | M145 | Yum-Yum Continuation | 35.7% | -27.6% | 37.1% | 41.5% | 3327 | 33 | 8.4% | -25.0% | 0/4 | 0.66 | DITOLAK: ≤M96 subset 0/4 tumpuan |
| 17 | M38 | Darvas Kotak | 35.7% | -20.0% | 38.6% | 41.9% | 389 | 38 | 22.6% | -22.9% | 0/4 | 0.76 | DITOLAK: ≤M96 subset 0/4 |
| 18 | M84 | Jarak purata bergerak MAD 21/200 | 35.6% | -31.8% | 40.7% | 43.8% | 959 | 24 | 44.2% | -43.3% | 0/4 | 0.57 | DITOLAK: ≤M96 subset 0/4 |
| 19 | M39 | Radge Pecahan Bollinger 100 hari | 35.5% | -34.5% | 41.8% | 34.7% | 3493 | 25 | 29.6% | -25.6% | 0/4 | 0.66 | DITOLAK: ≤M96 subset 0/4 |
| 20 | M111 | Sistem Volatiliti Wilder | 34.5% | -27.5% | 37.5% | 41.8% | 4592 | 28 | 31.1% | -23.5% | 1/4 | 0.70 | DITOLAK: ≤M96 subset 1/4 |
| 21 | M07 | Qullamaggie Breakout | 34.2% | -32.0% | 34.0% | 51.7% | 412 | 34 | 20.0% | -19.4% | 0/4 | 0.59 | DITOLAK: ≤M96 subset 0/4 |
| 22 | M149 | 3-Step Pullback | 33.2% | -31.7% | 40.7% | 26.3% | 2976 | 23 | 23.7% | -21.4% | 0/4 | 0.56 | DITOLAK: ≤M96 subset 0/4 |
| 23 | M11 | NR7 Breakout + Volume | 32.6% | -37.1% | 36.0% | 36.8% | 1819 | 27 | 39.1% | -28.1% | 1/4 | 0.70 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 tumpuan |
| 24 | M12 | Parabolic SAR | 32.2% | -20.5% | 34.8% | 36.3% | 6437 | 23 | 21.5% | -31.5% | 0/4 | 0.63 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 25 | M144 | Screw Bar | 32.0% | -36.1% | 33.7% | 40.4% | 104 | 32 | 8.1% | -17.5% | 0/4 | 0.70 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 tumpuan |
| 26 | M52 | Radge Weekend Trend Trader | 31.2% | -30.2% | 38.2% | 42.2% | 1785 | 26 | 42.6% | -24.3% | 1/4 | 0.55 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 27 | M59 | Anjakan Julat RSI | 31.1% | -18.1% | 40.5% | 32.7% | 1623 | 22 | 12.5% | -24.3% | 0/4 | 0.77 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 28 | M134 | First Kiss After Daylight (Landry) | 31.0% | -22.4% | 40.1% | 48.7% | 1086 | 39 | 28.8% | -41.4% | 0/4 | 0.84 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 29 | M79 | Radge: 20% Flipper | 29.7% | -33.2% | 39.8% | 36.5% | 3368 | 17 | 46.4% | -23.1% | 1/4 | 0.61 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 30 | M153 | Range Leader | 29.1% | -30.9% | 38.6% | 29.1% | 12533 | 18 | 80.2% | -40.7% | 0/4 | 0.68 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 31 | M161 | EMA 10/21 + Supertrend (10,3) | 28.8% | -23.9% | 35.4% | 30.2% | 8121 | 17 | 18.9% | -39.8% | 0/4 | 0.57 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 32 | M78 | Alvarez Pecahan Mingguan DTAYS | 28.8% | -21.7% | 34.2% | 41.9% | 1791 | 28 | 27.0% | -22.0% | 0/4 | 0.48 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 33 | M160 | Measured Move Up | 28.6% | -35.6% | 35.0% | 36.8% | 3132 | 29 | 28.5% | -48.2% | 1/4 | 0.52 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 |
| 34 | M159 | Heikin-Ashi Trend | 28.6% | -25.5% | 39.3% | 18.1% | 25073 | 9 | 13.6% | -33.3% | 1/4 | 0.56 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 35 | M107 | Golden Cross SMA50/200 | 28.1% | -24.9% | 27.4% | 34.7% | 1186 | 41 | 45.9% | -31.6% | 0/4 | 0.59 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 36 | M156 | Single Penetration (DiNapoli) | 27.4% | -24.8% | 47.0% | 22.7% | 5095 | 14 | 29.3% | -28.3% | 1/4 | 0.51 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 37 | M37 | Weinstein Peringkat 2 | 26.8% | -23.8% | 41.5% | 52.0% | 369 | 34 | 46.9% | -25.3% | 0/4 | 0.59 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 38 | M66 | IBD Undur Pertama ke Purata 50 Hari | 26.8% | -42.8% | 33.0% | 29.5% | 5440 | 18 | 95.4% | -31.1% | 0/4 | 0.59 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 39 | M35 | Pocket Pivot Morales & Kacher | 26.6% | -24.9% | 36.7% | 36.7% | 4407 | 24 | 33.5% | -22.9% | 0/4 | 0.57 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 40 | M90 | Pring KST | 26.3% | -26.3% | 30.9% | 31.1% | 2977 | 20 | 57.8% | -30.3% | 0/4 | 0.58 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 41 | M147 | Improved Three-Bar Pullback | 26.1% | -25.0% | 41.1% | 37.6% | 1861 | 27 | 35.5% | -55.4% | 0/4 | 0.67 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 42 | M92 | CCI-50 | 26.0% | -23.0% | 39.0% | 27.4% | 8157 | 15 | 23.7% | -25.9% | 0/4 | 0.60 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 43 | M20 | EMA10/15 Crossover + Sudut | 25.5% | -20.8% | 32.9% | 25.2% | 8514 | 15 | 20.3% | -17.6% | 0/4 | 0.61 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 44 | M123 | CCI Correction (Lambert, ChartSchool) | 25.2% | -25.9% | 30.2% | 23.3% | 4725 | 14 | 16.3% | -23.3% | 0/4 | 0.60 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 45 | M105 | Supertrend tulen | 24.3% | -25.4% | 38.6% | 40.7% | 5581 | 25 | 29.5% | -23.9% | 1/4 | 0.56 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 46 | M09 | Volumatic VIDYA Pivot Retest | 24.1% | -16.7% | 31.4% | 39.0% | 770 | 28 | 19.0% | -24.4% | 0/4 | 0.71 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 47 | M150 | Trend Bar Failure (Brooks) | 23.9% | -30.7% | 37.7% | 41.1% | 1622 | 42 | 23.2% | -22.4% | 1/4 | 0.49 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 48 | M77 | Undercut & Rally pada Purata Bergerak (MAU&R) | 23.5% | -28.4% | 45.1% | 41.1% | 1098 | 24 | 65.7% | -33.0% | 0/4 | 0.52 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 49 | M142 | Pecahan volum dari dasar (底部放量) | 23.4% | -20.1% | 44.9% | 45.4% | 757 | 29 | 11.8% | -28.2% | 1/4 | 0.52 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 50 | M131 | Ross Hook (Joe Ross) | 23.1% | -19.1% | 42.0% | 43.2% | 3695 | 31 | 20.2% | -31.7% | 0/4 | 0.54 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 51 | M02 | MACD + SMA200 | 22.6% | -45.8% | 37.3% | 36.0% | 2484 | 31 | 5.6% | -38.5% | 1/4 | 0.34 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 |
| 52 | M74 | Lulus Baharu Trend Template Minervini | 21.8% | -19.2% | 33.1% | 31.1% | 1554 | 19 | 39.9% | -22.4% | 0/4 | 0.53 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 53 | M10 | EMA3 + CCI + MACD | 21.6% | -25.9% | 35.7% | 35.3% | 1831 | 29 | 32.8% | -29.4% | 0/4 | 0.41 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 54 | M36 | Turtle 55/20 | 21.3% | -36.8% | 39.8% | 40.9% | 4164 | 28 | 30.0% | -35.3% | 1/4 | 0.46 | DITOLAK: ≤M96 ≤EW MDD subset 1/4 |
| 55 | M18 | EMA9/21 Pullback | 21.1% | -25.1% | 42.5% | 22.1% | 7591 | 11 | 12.4% | -39.6% | 0/4 | 0.43 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 56 | M51 | O'Neil Cawan & Pemegang | 20.9% | -10.6% | 40.4% | 43.1% | 188 | 30 | 24.0% | -18.6% | 0/4 | 0.76 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 57 | M89 | Chande 65sma-3cc | 20.9% | -22.5% | 38.7% | 36.3% | 2735 | 22 | 20.8% | -23.1% | 1/4 | 0.48 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 58 | M56 | Gray & Vogel Momentum Lancar (FIP) | 20.8% | -33.3% | 36.9% | 36.9% | 111 | 15 | 63.5% | -52.5% | 0/4 | 0.35 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 59 | M19 | Sneaky Pivot (proksi harian) | 20.4% | -23.3% | 38.8% | 20.8% | 5795 | 12 | 28.1% | -19.1% | 0/4 | 0.52 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 60 | M23 | Breitstein Kapitulasi + Kesinambungan | 20.3% | -26.6% | 39.3% | 35.3% | 1670 | 22 | 31.3% | -25.2% | 0/4 | 0.46 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 61 | M15 | Break & Retest + Henti ATR | 19.7% | -25.1% | 32.2% | 34.9% | 3991 | 21 | 18.8% | -30.6% | 0/4 | 0.44 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 62 | M04 | BB Squeeze Breakout | 19.7% | -25.2% | 35.6% | 40.2% | 1944 | 27 | 82.2% | -37.9% | 0/4 | 0.44 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 63 | M99 | Three Line Break | 19.5% | -33.9% | 31.6% | 30.9% | 3575 | 21 | 30.3% | -23.7% | 0/4 | 0.41 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 64 | M129 | Wick Play | 19.4% | -26.7% | 32.6% | 35.4% | 820 | 37 | 27.7% | -48.1% | 0/4 | 0.41 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 65 | M93 | Bollinger Kaedah II: %b + MFI | 19.1% | -28.3% | 37.7% | 37.8% | 4436 | 24 | 27.4% | -33.0% | 0/4 | 0.40 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 66 | M139 | 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | 18.9% | -15.3% | 30.6% | 33.3% | 1970 | 26 | 52.9% | -48.2% | 1/4 | 0.47 | DITOLAK: ≤M96 ≤EW subset 1/4 tumpuan |
| 67 | M91 | Stochastic Pop (Bernstein/Steckler) | 18.4% | -20.3% | 37.4% | 36.0% | 855 | 21 | 32.8% | -22.1% | 0/4 | 0.51 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 68 | M155 | Market Cycle Strategy | 18.1% | -38.5% | 41.1% | 28.4% | 10395 | 16 | 3.3% | -27.9% | 0/4 | 0.37 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 69 | M76 | Undercut & Rally pada Low Penting | 18.0% | -19.0% | 35.6% | 33.2% | 946 | 22 | 1.9% | -23.7% | 0/4 | 0.49 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 70 | M130 | 多方炮 (dua lilin hijau mengapit satu merah) | 17.7% | -22.0% | 38.6% | 43.8% | 210 | 43 | 63.0% | -44.5% | 0/4 | 0.40 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 71 | M33 | Supertrend + SMA10 | 17.7% | -33.3% | 40.0% | 39.3% | 3158 | 25 | 26.3% | -26.2% | 0/4 | 0.44 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 72 | M80 | Radge Saluran Purata Bergerak (MAC) | 17.7% | -32.3% | 35.2% | 30.3% | 5349 | 19 | 5.3% | -40.5% | 0/4 | 0.34 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 73 | M24 | Rotasi Momentum ROC12 + SMA200 | 17.6% | -13.9% | 38.2% | 48.5% | 68 | 13 | 36.4% | -48.8% | 0/4 | 0.61 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 74 | M48 | Cooper 1-2-3-4 | 16.8% | -41.6% | 40.5% | 41.5% | 1179 | 28 | 22.5% | -21.0% | 0/4 | 0.32 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 75 | M70 | Pecahan Hari Dalam | 16.6% | -34.7% | 38.7% | 34.8% | 5237 | 22 | 72.5% | -30.0% | 0/4 | 0.32 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 76 | M120 | Reversal New Highs | 16.5% | -19.7% | 35.1% | 37.7% | 308 | 46 | 2.0% | -25.5% | 0/4 | 0.44 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 77 | M08 | SMA20 + SMA200 | 16.1% | -34.4% | 31.0% | 33.1% | 3393 | 19 | 13.6% | -35.8% | 0/4 | 0.31 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 78 | M135 | 3rd Watch | 14.7% | -21.0% | 49.4% | 35.0% | 360 | 26 | 8.5% | -25.1% | 0/4 | 0.40 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 79 | M29 | EMA3 + RSI75 + Stokastik | 14.7% | -22.6% | 34.6% | 38.2% | 1050 | 29 | 16.7% | -26.5% | 0/4 | 0.32 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 80 | M141 | First Thrust (Landry) | 14.4% | -21.8% | 31.1% | 53.7% | 244 | 115 | 13.5% | -29.0% | 0/4 | 0.37 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 81 | M128 | Inventory Retracement Bar (IRB, Rob Hoffman) | 14.4% | -26.6% | 36.6% | 33.6% | 3560 | 21 | 6.2% | -25.5% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 82 | M05 | MACD Divergence + Pengesahan | 14.1% | -31.7% | 40.2% | 41.7% | 420 | 36 | 19.1% | -20.2% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 83 | M126 | Hidden Smash Day (beli, Larry Williams) | 14.0% | -32.4% | 31.4% | 30.5% | 596 | 24 | 34.0% | -52.8% | 0/4 | 0.33 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 84 | M25 | VWAP Wave (proksi harian) | 14.0% | -25.4% | 36.3% | 43.1% | 2803 | 31 | 10.3% | -32.8% | 0/4 | 0.32 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 85 | M13 | Garis Trend Action/Safety Line | 13.9% | -38.3% | 39.1% | 25.9% | 11826 | 13 | 34.3% | -27.3% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 86 | M118 | Expansion Pivot (Cooper) | 13.8% | -34.6% | 34.4% | 39.3% | 1510 | 31 | 23.2% | -25.1% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 87 | M88 | O'Neil Shakeout +3 | 13.7% | -20.3% | 35.1% | 28.3% | 784 | 12 | 14.7% | -19.1% | 0/4 | 0.34 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 88 | M148 | Natural Number Method | 13.6% | -26.3% | 38.0% | 35.8% | 2875 | 23 | 15.5% | -30.1% | 0/4 | 0.30 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 89 | M152 | Spike & Ledge | 13.2% | -39.5% | 30.2% | 39.1% | 1340 | 38 | 13.4% | -39.3% | 0/4 | 0.24 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 90 | M101 | Bulkowski: Tiga lembah menaik | 13.1% | -20.5% | 33.4% | 33.9% | 885 | 25 | 47.5% | -42.2% | 0/4 | 0.28 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 91 | M03 | BB Break + Divergence RSI | 13.0% | -23.7% | 38.1% | 32.6% | 4295 | 20 | 7.0% | -29.5% | 0/4 | 0.29 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 92 | M157 | Consolidation Pivot Breakout (versi angka) | 12.5% | -26.1% | 28.4% | 35.1% | 461 | 59 | 37.0% | -44.4% | 1/4 | 0.34 | DITOLAK: ≤M96 ≤EW subset 1/4 tumpuan |
| 93 | M151 | Outside Bar Failure | 12.4% | -36.3% | 39.5% | 40.6% | 1778 | 35 | 31.8% | -37.7% | 0/4 | 0.24 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 94 | M82 | Arthur Hill Rotasi Sasaran 10% | 12.2% | -34.5% | 38.4% | 15.3% | 19081 | 9 | 33.4% | -26.5% | 0/4 | 0.24 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 95 | M06 | Minervini VCP Breakout | 12.2% | -29.2% | 40.7% | 38.1% | 1414 | 22 | 46.8% | -32.0% | 0/4 | 0.23 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 96 | M57 | Landry Trend Knockout (TKO) | 11.8% | -27.9% | 32.9% | 36.7% | 3010 | 22 | 41.1% | -43.4% | 0/4 | 0.22 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 97 | M106 | DMI Wilder | 11.7% | -29.5% | 35.7% | 29.6% | 2072 | 19 | 18.6% | -21.8% | 0/4 | 0.24 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 98 | M27 | Price Action 4 Tiang | 11.7% | -30.2% | 35.8% | 20.4% | 15759 | 12 | 25.8% | -28.2% | 1/4 | 0.24 | DITOLAK: ≤M96 ≤EW subset 1/4 |
| 99 | M116 | 2/20 EMA Breakout (Landry) | 11.6% | -37.8% | 32.6% | 37.2% | 6258 | 25 | 33.3% | -26.1% | 0/4 | 0.23 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 100 | M28 | VWAP Separator + Kiss Pivot | 11.2% | -22.5% | 47.9% | 33.9% | 1604 | 19 | 0.2% | -24.7% | 0/4 | 0.29 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 101 | M46 | Jurang Naik Boleh Beli (Buyable Gap Up) | 11.1% | -24.7% | 37.8% | 39.3% | 672 | 29 | 32.0% | -20.6% | 0/4 | 0.25 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 102 | M94 | Pecutan Momentum (Chen, Yu & Wang) | 11.1% | -40.2% | 36.8% | 30.7% | 576 | 14 | 68.4% | -39.8% | 0/4 | 0.19 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 103 | M100 | Bulkowski Segi Empat & Segi Tiga Menaik | 10.6% | -20.5% | 40.9% | 35.5% | 1013 | 31 | 12.8% | -21.6% | 0/4 | 0.29 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 104 | M117 | Landry Pullback (high 2 bulan) | 10.5% | -33.6% | 37.6% | 36.2% | 2237 | 39 | 34.9% | -50.5% | 0/4 | 0.22 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 105 | M31 | Band Walk (BB 20/2) | 10.4% | -28.9% | 38.8% | 38.4% | 4841 | 26 | 16.3% | -34.6% | 0/4 | 0.21 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 106 | M122 | Moving Momentum (ChartSchool) | 9.8% | -30.4% | 31.0% | 23.1% | 3799 | 14 | 7.6% | -42.9% | 0/4 | 0.20 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 107 | M34 | Carter TTM Squeeze | 9.8% | -28.4% | 36.2% | 38.4% | 2174 | 27 | 14.9% | -23.6% | 0/4 | 0.20 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 108 | M154 | HOLP (High of Low Period) | 9.4% | -25.3% | 39.3% | 39.7% | 2010 | 31 | 31.9% | -31.6% | 0/4 | 0.18 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 109 | M50 | Elder Triple Screen | 9.4% | -34.9% | 41.2% | 36.2% | 6467 | 24 | 19.6% | -22.3% | 0/4 | 0.18 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 110 | M143 | 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | 9.2% | -20.8% | 49.3% | 42.5% | 426 | 35 | -0.2% | -9.9% | 0/4 | 0.26 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 111 | M49 | Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | 8.9% | -41.7% | 36.6% | 39.6% | 4827 | 29 | 11.8% | -28.1% | 0/4 | 0.17 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 tumpuan |
| 112 | M14 | Walking with the Whales | 8.7% | -27.0% | 35.5% | 28.8% | 11922 | 16 | 13.0% | -25.7% | 0/4 | 0.18 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 113 | M146 | 3-Bar Momentum Pattern | 8.5% | -30.5% | 34.3% | 40.7% | 1150 | 54 | 12.6% | -28.6% | 2/4 | 0.17 | DITOLAK: ≤M96 ≤EW subset 2/4 tumpuan |
| 114 | M47 | Holy Grail Raschke | 7.6% | -22.7% | 41.4% | 28.5% | 748 | 21 | 6.9% | -16.9% | 0/4 | 0.17 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 115 | M26 | Garis Trend Undur 3 Sentuhan + Pecahan | 7.5% | -40.2% | 40.0% | 26.3% | 1294 | 18 | 9.3% | -31.9% | 0/4 | 0.15 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 116 | M121 | High 2 bull flag (Brooks) | 6.7% | -31.8% | 25.8% | 41.7% | 271 | 64 | 47.8% | -38.0% | 0/4 | 0.15 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 117 | M01 | Bollinger Band + RSI | 6.3% | -20.4% | 54.0% | 30.9% | 1424 | 12 | 10.6% | -29.5% | 0/4 | 0.14 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 118 | M44 | Tapak Rata IBD | 6.2% | -15.8% | 28.6% | 32.2% | 304 | 25 | 12.6% | -15.1% | 0/4 | 0.17 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 119 | M158 | Doubly Adaptive Profit Targets | 5.7% | -39.3% | 34.5% | 34.9% | 5212 | 24 | 1.4% | -40.1% | 0/4 | 0.12 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 120 | M138 | 直升机空中加油 (Helikopter isi minyak di udara) | 4.2% | -8.1% | 32.9% | 24.7% | 85 | 10 | 16.4% | -29.0% | 0/4 | 0.30 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 121 | M95 | Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | 4.0% | -24.4% | 40.3% | 43.6% | 2077 | 30 | 56.9% | -28.5% | 0/4 | 0.10 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 122 | M124 | 'Last' Stochastic Technique (ChartSchool) | 3.0% | -30.3% | 39.6% | 25.5% | 5946 | 14 | 12.5% | -27.7% | 0/4 | 0.09 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 123 | M133 | Bull Hook (Crabel) | 2.4% | -27.7% | 36.8% | 23.6% | 1001 | 28 | 23.4% | -39.7% | 0/4 | 0.08 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 124 | M87 | IBD Tapak Menaik | 2.4% | -31.6% | 33.7% | 43.2% | 190 | 30 | 20.7% | -18.7% | 0/4 | 0.08 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 125 | M67 | Rayner Teo: Ujian Ketiga pada Purata 50 | 1.4% | -28.9% | 33.8% | 37.5% | 880 | 27 | 9.7% | -27.2% | 0/4 | 0.07 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 126 | M132 | Ascending Scallop (Bulkowski) | 0.9% | -36.6% | 34.9% | 41.2% | 1149 | 37 | 7.0% | -25.0% | 0/4 | 0.06 | DITOLAK: ≤M96 ≤EW MDD subset 0/4 |
| 127 | M127 | Slingshot Bullish | -0.8% | -45.3% | 38.2% | 25.8% | 1441 | 33 | -7.7% | -41.2% | 2/4 | 0.05 | DITOLAK: ≤M96 ≤EW MDD subset 2/4 |
| 128 | M64 | O'Neil Tiga Minggu Ketat | -1.7% | -32.9% | 34.7% | 35.8% | 265 | 23 | 2.4% | -26.4% | 0/4 | 0.03 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 129 | M104 | High Tight Flag / Power Play | -2.4% | -23.0% | 29.9% | 47.1% | 87 | 20 | 2.5% | -21.6% | 0/4 | 0.02 | DITOLAK: ≤M96 ≤EW subset 0/4 tumpuan |
| 130 | M115 | Bow Tie (Landry) | -3.4% | -27.8% | 36.0% | 40.7% | 322 | 34 | 20.6% | -37.3% | 0/4 | 0.01 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 131 | M68 | Kell Base n' Break | -3.8% | -26.2% | 37.6% | 39.1% | 1336 | 29 | 17.0% | -22.9% | 0/4 | 0.02 | DITOLAK: ≤M96 ≤EW subset 0/4 |
| 132 | M22 | Qullamaggie Episodic Pivot |  |  |  |  | 0 |  | 2.9% | -5.8% | 0/4 |  | DITOLAK: tiada dagangan |

## 4. Gabungan paling kerap dipilih (10 teratas)

| ID | Stop | Exit | Tmax |
|---|---|---|---|
| M21 | ATR3 (2/16) | TIADA (6/16) | 63 (7/16) |
| M81 | LOW1 (5/16) | ASAL (6/16) | 42 (6/16) |
| M140 | ATR2.5 (3/16) | ASAL (7/16) | 0 (10/16) |
| M96 | ATR2.5 (5/16) | ASAL (7/16) | 42 (7/16) |
| M136 | ASAL (4/16) | CHAN3 (8/16) | 0 (9/16) |
| M125 | ATR1.5 (3/16) | CHAN4 (6/16) | 42 (7/16) |
| M119 | ATR3 (5/16) | CHAN4 (5/16) | 63 (6/16) |
| M54 | ATR2 (3/16) | ASAL (8/16) | 0 (11/16) |
| M73 | LOW10 (4/16) | CHAN4 (8/16) | 21 (7/16) |
| M32 | PCT15 (4/16) | CHAN4 (8/16) | 63 (9/16) |

## 5. Kestabilan: banding larian 15 Okt (commit 18e0db0)

- 13 kaedah yang dahulu sudah 150 percubaan (enjin v1.2 asal): metrik luar sampel sama tepat — bukti hujung ke hujung enjin laju setara.
- 71 kaedah yang dahulu 60/100 percubaan: korelasi kedudukan (Spearman) CAGR WFO lama lawan baru = 0.79; beza mutlak median 5.4%. Beza besar = pilihan Optuna sensitif kepada bajet carian (tanda keputusan WFO kaedah itu kurang stabil).

| ID | Percubaan lama | CAGR lama | CAGR baru | Beza |
|---|---|---|---|---|
| M73 | 60 | 85.7% | 41.1% | -44.6% |
| M54 | 60 | 22.4% | 41.8% | 19.4% |
| M59 | 60 | 12.0% | 31.1% | 19.1% |
| M84 | 60 | 18.7% | 35.6% | 16.9% |
| M55 | 60 | 20.0% | 36.5% | 16.5% |
| M96 | 60 | 69.8% | 53.9% | -15.9% |
| M68 | 60 | 11.4% | -3.8% | -15.2% |
| M30 | 100 | 26.4% | 40.0% | 13.6% |
| M14 | 100 | 22.2% | 8.7% | -13.5% |
| M78 | 60 | 15.7% | 28.8% | 13.1% |
| M80 | 60 | 4.7% | 17.7% | 13.0% |
| M29 | 100 | 27.2% | 14.7% | -12.5% |
| M77 | 60 | 11.2% | 23.5% | 12.3% |
| M52 | 60 | 42.3% | 31.2% | -11.1% |
| M81 | 60 | 51.2% | 61.8% | 10.5% |

## 6. Tidak layak / ralat

- M40: isyarat bergantung pada pra-simulasi 8 slot kaedah sendiri
- M45: isyarat bergantung pada pra-simulasi 8 slot kaedah sendiri

## 7. Nota tafsiran

- CAGR beku = varian registry dengan stop/exit asal, dagangan masuk ≥ 1 Jan 2023, portfolio sama. Ia BUKAN luar sampel tulen (varian dipilih dengan melihat data 2019–2026).
- CAGR WFO ialah luar sampel tulen: setiap suku memakai gabungan yang dipilih atas 3 tahun sebelumnya sahaja.
- Subset: gabungan terpilih yang sama dinilai atas S1–S4 (tidak ditala semula); bilangan subset yang mengalahkan EW subset. **Kelemahan reka bentuk:** dagangan ditapis kepada ~105 saham tetapi portfolio kekal 8 slot, jadi slot banyak kosong (tunai) berbanding EW subset yang sentiasa melabur penuh; bagi kaedah merentas saham (cth. M96) hanya ~2 daripada 8 pilihan jatuh dalam setiap subset. Ujian ini berat sebelah menentang semua kaedah dan tidak setara dengan gate subset projek (yang menjalankan semula kaedah atas alam subset). Oleh itu senarai "LULUS tanpa subset" turut dilaporkan.
- n = semua dagangan calon yang dijana (konvensyen `enjin.metrik`), bukan hanya yang diambil oleh 8 slot.
- M22: tiada gabungan sah dalam mana-mana tetingkap latihan (< 30 dagangan), jadi tiada dagangan luar sampel.
- Kriteria LULUS (§7): CAGR > M96 V1 beku dan > EW; MDD ≥ −35%; n ≥ 60; subset ≥ 3/4; tiada saham > 25% keuntungan.
