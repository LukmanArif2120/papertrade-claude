# Papan Kedudukan Kaedah M (set 431, varian skor tertinggi)

Jana daripada data/registry_M_gabung.csv oleh `standard/jana_papan.py`. 140 kaedah, 627 varian diuji atas 431 saham. Status terbaik setiap kaedah: DITOLAK 50, SIMPAN 53, UJI KERTAS 31, GUNA 6.

Skor kosong = gagal gate (DITOLAK); bagi kaedah yang semua variannya DITOLAK, varian CAGR tertinggi dipaparkan (sebelum 17 Okt 2026: V0). Angka DALAM SAMPEL (1 Nov 2019 – 2 Okt 2026).

| # | ID | Kaedah | Varian terbaik | Keputusan | Skor | CAGR | MDD | Win | Purata/dagangan | Hit10 | Menang EW |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M167 | Momentum Semalaman (Lou, Polk & Skouras) | V2 V1 kunci OVN252 | GUNA | 83.1 | 49.6% | -36.4% | 35.2% | 4.1% | 53.6% | Ya |
| 2 | M166 | Titik Pusing Momentum (Goulding, Harvey & Mazzoleni) | V1 Dikunci (keadaan SPY, Bear dilarang) | GUNA | 83.0 | 58.1% | -40.4% | 39.6% | 4.6% | 57.5% | Ya |
| 3 | M96 | Momo India: Ranking Sharpe 3/6/12 bulan | V1 Dikunci (+henti tutup-3xATR14) | GUNA | 80.3 | 40.0% | -42.0% | 42.5% | 12.2% | 63.3% | Ya |
| 4 | M114 | RS Peneraju Pasaran Naik | V4 Kolam 10% | GUNA | 77.4 | 49.6% | -38.8% | 38.1% | 4.0% | 56.1% | Ya |
| 5 | M30 | BB Free Bar + Himpitan 50/2.5 | V3 V1 tetapi BB20/2 | GUNA | 76.2 | 52.0% | -36.8% | 36.6% | 3.8% | 45.1% | Ya |
| 6 | M79 | Radge: 20% Flipper | V3 V1 dengan A=0.15 (masuk/keluar/henti 15%) | GUNA | 75.9 | 35.5% | -39.9% | 40.4% | 6.2% | 63.5% | Ya |
| 7 | M111 | Sistem Volatiliti Wilder | V5 V1 henti maks(tutup-3xATR7; 0.88xtutup) | UJI KERTAS | 74.2 | 43.0% | -34.9% | 38.6% | 2.4% | 45.3% | Ya |
| 8 | M74 | Lulus Baharu Trend Template Minervini | V2 V1 tanpa S8 (7 syarat harga) | UJI KERTAS | 73.2 | 37.1% | -33.4% | 24.0% | 2.7% | 28.8% | Ya |
| 9 | M142 | Pecahan volum dari dasar (底部放量) | V1 WFO beku: henti ATR3.5, keluar CHAN4, tmax tiada | UJI KERTAS | 72.7 | 32.3% | -27.6% | 40.9% | 6.9% | 54.0% | Ya |
| 10 | M162 | Momentum Residual (Blitz, Huij & Martens) | V2 V1 tanpa penapis SPY | UJI KERTAS | 72.1 | 38.5% | -36.6% | 41.9% | 4.2% | 53.6% | Ya |
| 11 | M144 | Screw Bar | V1 WFO beku: henti ATR4, keluar SMA50, tmax tiada | UJI KERTAS | 71.9 | 26.5% | -21.9% | 41.0% | 7.7% | 37.2% | Ya |
| 12 | M05 | MACD Divergence + Pengesahan | V3 V1+close>SMA200 | UJI KERTAS | 71.8 | 28.4% | -25.7% | 34.9% | 10.8% | 54.8% | Ya |
| 13 | M80 | Radge Saluran Purata Bergerak (MAC) | V2 V1 dengan henti tutup-3xATR14 | UJI KERTAS | 71.6 | 38.1% | -38.6% | 35.6% | 8.9% | 53.6% | Ya |
| 14 | M163 | Kekuatan Mutlak (Gulen & Petkova) | V1 Dikunci (AS>=BP90, Rangka R) | UJI KERTAS | 71.6 | 37.7% | -31.8% | 40.3% | 3.9% | 57.7% | Ya |
| 15 | M46 | Jurang Naik Boleh Beli (Buyable Gap Up) | V2 V1 dengan jurang ketat (low>high semalam+0.75xATR40) | UJI KERTAS | 69.5 | 26.3% | -20.6% | 22.7% | 2.8% | 29.6% | Ya |
| 16 | M12 | Parabolic SAR | V5 V1 keluar close<SMA50 | UJI KERTAS | 69.5 | 31.1% | -28.8% | 29.5% | 2.0% | 33.6% | Ya |
| 17 | M40 | Clenow Stocks on the Move | V4 V1 tanpa penapis pasaran | UJI KERTAS | 68.9 | 25.6% | -35.8% | 38.3% | 4.8% | 51.8% | Ya |
| 18 | M37 | Weinstein Peringkat 2 | V2 V1 keluar tutup harian<SMA50 + tutup>SMA50 | UJI KERTAS | 67.7 | 29.5% | -31.2% | 41.3% | 5.5% | 55.4% | Ya |
| 19 | M130 | 多方炮 (dua lilin hijau mengapit satu merah) | V1 WFO beku: henti ATR3.5, keluar ASAL, tmax tiada | UJI KERTAS | 67.6 | 35.7% | -43.9% | 24.9% | 92.2% | 52.7% | Ya |
| 20 | M04 | BB Squeeze Breakout | U2 asas V2 + E1 volume>=1.5xSMA20 | UJI KERTAS | 67.5 | 46.4% | -41.1% | 35.6% | 5.0% | 42.6% | Ya |
| 21 | M151 | Outside Bar Failure | V1 WFO beku: henti ATR1.5, keluar CHAN4, tmax tiada | UJI KERTAS | 67.3 | 31.1% | -26.2% | 26.7% | 1.9% | 35.1% | Ya |
| 22 | M52 | Radge Weekend Trend Trader | V3 V1 keluar tutup<SMA50 harian | UJI KERTAS | 66.7 | 28.2% | -30.8% | 37.2% | 5.2% | 49.3% | Ya |
| 23 | M66 | IBD Undur Pertama ke Purata 50 Hari | V0 Sumber tulen (UNDUR+NAIK50+PUSING+BARU; tanpa PERTAMA/HIGHBARU/NIPIS) | UJI KERTAS | 66.7 | 51.1% | -30.9% | 28.1% | 1.7% | 28.5% | Ya |
| 24 | M18 | EMA9/21 Pullback | V2 V1 Model A sahaja | UJI KERTAS | 66.0 | 44.3% | -44.5% | 25.7% | 0.4% | 16.9% | Ya |
| 25 | M158 | Doubly Adaptive Profit Targets | V1 WFO beku: henti PCT12, keluar ASAL, tmax tiada | UJI KERTAS | 65.8 | 37.5% | -29.3% | 34.5% | 2.9% | 40.9% | Ya |
| 26 | M105 | Supertrend tulen | V1 Dikunci (V0 + had henti 12%) | UJI KERTAS | 65.3 | 29.6% | -33.1% | 38.9% | 2.4% | 46.8% | Ya |
| 27 | M13 | Garis Trend Action/Safety Line | V1 Spesifikasi dikunci | UJI KERTAS | 65.2 | 52.1% | -37.5% | 34.4% | 1.0% | 26.1% | Ya |
| 28 | M10 | EMA3 + CCI + MACD | V4 V1 pencetus CCI>+100 | UJI KERTAS | 65.0 | 28.5% | -29.3% | 32.5% | 4.7% | 45.5% | Ya |
| 29 | M45 | High 52 Minggu (George & Hwang) | V4 V1 + high 52 minggu dicapai dalam 21 hari | UJI KERTAS | 64.7 | 30.7% | -40.5% | 32.3% | 12.8% | 54.3% | Ya |
| 30 | M160 | Measured Move Up | V1 WFO beku: henti LOW10, keluar EMA21, tmax 42 | UJI KERTAS | 64.5 | 37.5% | -29.1% | 32.2% | 0.4% | 17.2% | Ya |
| 31 | M77 | Undercut & Rally pada Purata Bergerak (MAU&R) | V2 V1 henti=low hari isyarat | UJI KERTAS | 63.4 | 42.4% | -33.8% | 24.7% | 2.7% | 23.6% | Ya |
| 32 | M84 | Jarak purata bergerak MAD 21/200 | V5 V1 + SMA50 | UJI KERTAS | 63.3 | 33.0% | -44.4% | 37.2% | 3.7% | 45.9% | Ya |
| 33 | M54 | IBD Power Trend | V4 V1 sig=PT benar & tutup>high 20 hari | UJI KERTAS | 63.1 | 31.0% | -38.7% | 29.6% | 3.4% | 40.6% | Ya |
| 34 | M32 | Momentum Burst | V2 V1 keluar close<SMA50 | UJI KERTAS | 62.7 | 43.3% | -36.8% | 24.6% | 3.6% | 36.6% | Ya |
| 35 | M55 | Guppy GMMA | V4 Undur ke kumpulan panjang lalu lantun (Persediaan 2) | UJI KERTAS | 60.9 | 29.0% | -31.0% | 25.6% | 2.7% | 34.9% | Ya |
| 36 | M57 | Landry Trend Knockout (TKO) | V1 Dikunci (keluar tutup<SMA50) | UJI KERTAS | 60.8 | 33.1% | -43.9% | 21.2% | 1.6% | 27.1% | Ya |
| 37 | M41 | FW Penyatuan Mingguan | V0 Sumber sahaja (tanpa had julat 25%) | UJI KERTAS | 60.5 | 27.3% | -34.6% | 35.7% | 15.0% | 58.3% | Ya |
| 38 | M90 | Pring KST | V3 V1 + tutup>SMA50, keluar tutup<SMA50 | SIMPAN | 59.9 | 35.4% | -42.2% | 29.5% | 1.9% | 36.9% | Ya |
| 39 | M137 | Livermore System | V1 WFO beku: henti ATR2.5, keluar CHAN4, tmax tiada | SIMPAN | 59.2 | 26.6% | -35.3% | 35.2% | 4.2% | 44.4% | Ya |
| 40 | M146 | 3-Bar Momentum Pattern | V1 WFO beku: henti PCT6, keluar SMA50, tmax tiada | SIMPAN | 58.9 | 35.8% | -40.6% | 27.3% | 2.7% | 34.8% | Ya |
| 41 | M102 | Stockbee SLTB | V5 V1 + volum hari ini > semalam | SIMPAN | 58.6 | 37.3% | -38.3% | 18.1% | 1.3% | 24.1% | Ya |
| 42 | M91 | Stochastic Pop (Bernstein/Steckler) | V2 V1 + tutup>HH20 (pecah keluar) | SIMPAN | 58.5 | 25.1% | -20.8% | 41.8% | 1.6% | 35.6% | Ya |
| 43 | M92 | CCI-50 | V2 V1 isyarat silang atas sifar (NAIK0) | SIMPAN | 57.9 | 28.1% | -31.8% | 48.7% | 1.2% | 29.5% | Ya |
| 44 | M11 | NR7 Breakout + Volume | V3 V1+NR7 hari dalam (NR7-ID) | SIMPAN | 57.9 | 29.9% | -28.3% | 36.1% | 2.9% | 28.9% | Ya |
| 45 | M81 | Bensdorp Long Trend High Momentum | V4 V1 henti awal 3xATR20 | SIMPAN | 57.1 | 28.0% | -40.7% | 31.9% | 8.6% | 59.3% | Ya |
| 46 | M139 | 均线首次粘合向上发散 (MA berhimpun kali pertama, berkipas naik) | V1 WFO beku: henti PCT15, keluar TIADA, tmax 21 | SIMPAN | 56.9 | 24.8% | -24.9% | 51.1% | 1.3% | 37.3% | Ya |
| 47 | M89 | Chande 65sma-3cc | V5 V1+SMA65 naik (>SMA65 10h lalu) | SIMPAN | 56.3 | 25.9% | -31.0% | 34.2% | 1.8% | 39.8% | Ya |
| 48 | M27 | Price Action 4 Tiang | V2 Persediaan A sahaja (flip & hold) | SIMPAN | 55.5 | 32.2% | -39.2% | 35.2% | 0.4% | 14.5% | Ya |
| 49 | M123 | CCI Correction (Lambert, ChartSchool) | V1 WFO beku: henti LOW1, keluar SMA50, tmax tiada | SIMPAN | 55.1 | 39.7% | -33.1% | 27.6% | 0.9% | 14.6% | Ya |
| 50 | M39 | Radge Pecahan Bollinger 100 hari | V4 V1 jalur atas 2 SD | SIMPAN | 54.7 | 23.4% | -26.4% | 37.3% | 9.1% | 59.5% | Ya |
| 51 | M70 | Pecahan Hari Dalam | V5 V1 masuk awal tanpa pengesahan | SIMPAN | 54.5 | 37.9% | -37.2% | 11.5% | 0.8% | 15.0% | Ya |
| 52 | M09 | Volumatic VIDYA Pivot Retest | V2 V1 tanpa sasaran | SIMPAN | 54.3 | 23.9% | -24.5% | 23.5% | 1.8% | 35.2% | Ya |
| 53 | M88 | O'Neil Shakeout +3 | V1 Dikunci (BELI 1.10xL1; vol>VOL50; henti max(L2;0.92x masuk); keluar tutup<low20) | SIMPAN | 52.8 | 22.0% | -39.3% | 32.3% | 5.6% | 46.6% | Ya |
| 54 | M128 | Inventory Retracement Bar (IRB, Rob Hoffman) | V1 WFO beku: henti PCT10, keluar SMA20, tmax 42 | SIMPAN | 52.0 | 27.3% | -24.6% | 33.7% | 0.5% | 24.2% | Ya |
| 55 | M165 | Momentum Industri (Moskowitz & Grinblatt) | V3 V1 tanpa syarat RS saham | SIMPAN | 51.5 | 24.4% | -37.8% | 37.0% | 2.5% | 47.8% | Ya |
| 56 | M78 | Alvarez Pecahan Mingguan DTAYS | V2 V1 henti mengekor 5xATR100 | SIMPAN | 51.5 | 21.9% | -39.0% | 32.0% | 3.2% | 47.8% | Tidak |
| 57 | M29 | EMA3 + RSI75 + Stokastik | V4 V1 EMA 50/110/250 | SIMPAN | 51.2 | 22.1% | -24.4% | 18.0% | 3.2% | 28.6% | Ya |
| 58 | M129 | Wick Play | V1 WFO beku: henti LOW10, keluar TIADA, tmax 63 | SIMPAN | 50.8 | 19.2% | -24.9% | 37.8% | 2.6% | 46.7% | Tidak |
| 59 | M152 | Spike & Ledge | V1 WFO beku: henti PCT15, keluar ASAL, tmax 42 | SIMPAN | 50.8 | 21.5% | -36.1% | 52.4% | 3.2% | 50.1% | Tidak |
| 60 | M48 | Cooper 1-2-3-4 | V3 V1 henti low hari 3 - 1xATR14 | SIMPAN | 48.6 | 23.3% | -38.2% | 34.1% | 2.8% | 41.4% | Ya |
| 61 | M19 | Sneaky Pivot (proksi harian) | V1 Spesifikasi dikunci | SIMPAN | 48.6 | 25.8% | -37.0% | 44.0% | 0.3% | 25.3% | Ya |
| 62 | M118 | Expansion Pivot (Cooper) | V1 WFO beku: henti LOW5, keluar SMA50, tmax tiada | SIMPAN | 48.2 | 24.7% | -25.0% | 32.6% | 1.6% | 40.8% | Ya |
| 63 | M95 | Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | V1 Dikunci: PECAH20+PTH>=0.85+HSHP<=21+tutup>SMA50 | SIMPAN | 48.1 | 27.1% | -32.8% | 32.2% | 2.7% | 37.9% | Ya |
| 64 | M33 | Supertrend + SMA10 | V5 V1 + volum>VOL20 | SIMPAN | 47.9 | 21.2% | -29.4% | 40.1% | 1.7% | 47.0% | Tidak |
| 65 | M99 | Three Line Break | V4 V1 + close>SMA200 | SIMPAN | 47.9 | 22.1% | -29.3% | 39.6% | 1.2% | 30.7% | Ya |
| 66 | M93 | Bollinger Kaedah II: %b + MFI | V2 V1, keluar LEMAH (%b<0.20 & MFI10<20) | SIMPAN | 47.9 | 23.9% | -38.5% | 36.2% | 8.2% | 52.6% | Ya |
| 67 | M134 | First Kiss After Daylight (Landry) | V1 WFO beku: henti ATR2, keluar CHAN4, tmax tiada | SIMPAN | 46.1 | 21.2% | -31.5% | 34.3% | 5.4% | 43.8% | Tidak |
| 68 | M08 | SMA20 + SMA200 | V1 Spesifikasi dikunci | SIMPAN | 46.0 | 23.0% | -34.0% | 31.7% | 1.1% | 26.8% | Ya |
| 69 | M124 | 'Last' Stochastic Technique (ChartSchool) | V1 WFO beku: henti ATR2, keluar CHAN3, tmax 63 | SIMPAN | 44.4 | 21.8% | -32.0% | 35.9% | 1.7% | 38.4% | Tidak |
| 70 | M135 | 3rd Watch | V1 WFO beku: henti LOW10, keluar SMA50, tmax 63 | SIMPAN | 43.2 | 16.1% | -19.6% | 38.7% | 2.1% | 46.2% | Tidak |
| 71 | M161 | EMA 10/21 + Supertrend (10,3) | V1 WFO beku: henti PCT15, keluar ASAL, tmax tiada | SIMPAN | 42.5 | 20.2% | -39.6% | 34.7% | 1.4% | 33.2% | Tidak |
| 72 | M149 | 3-Step Pullback | V1 WFO beku: henti ASAL, keluar ASAL, tmax tiada | SIMPAN | 41.0 | 22.2% | -44.4% | 19.4% | 59.4% | 54.6% | Ya |
| 73 | M119 | 180 Bullish (Cooper) | V1 WFO beku: henti ASAL, keluar CHAN4, tmax 42 | SIMPAN | 40.7 | 22.5% | -27.3% | 27.3% | 1.2% | 32.5% | Ya |
| 74 | M154 | HOLP (High of Low Period) | V1 WFO beku: henti ATR2.5, keluar ASAL, tmax 42 | SIMPAN | 40.6 | 20.9% | -35.1% | 39.2% | 1.9% | 44.4% | Tidak |
| 75 | M133 | Bull Hook (Crabel) | V1 WFO beku: henti ATR2, keluar SMA50, tmax 21 | SIMPAN | 40.3 | 20.3% | -26.4% | 41.1% | 0.7% | 22.8% | Tidak |
| 76 | M06 | Minervini VCP Breakout | V5 V1 tanpa VCP | SIMPAN | 40.1 | 23.0% | -31.4% | 33.1% | 2.5% | 42.7% | Ya |
| 77 | M20 | EMA10/15 Crossover + Sudut | V3 V1 tanpa syarat sudut | SIMPAN | 39.7 | 19.7% | -22.4% | 39.2% | 0.2% | 13.5% | Tidak |
| 78 | M107 | Golden Cross SMA50/200 | V5 V1 + SPY>SMA200 | SIMPAN | 39.5 | 16.8% | -24.4% | 31.7% | 15.4% | 52.0% | Tidak |
| 79 | M150 | Trend Bar Failure (Brooks) | V1 WFO beku: henti PCT12, keluar SMA20, tmax 21 | SIMPAN | 39.4 | 20.8% | -20.5% | 37.0% | 0.5% | 27.1% | Tidak |
| 80 | M106 | DMI Wilder | V5 V1 dengan henti tutup-2xATR14 | SIMPAN | 37.3 | 18.2% | -34.8% | 32.1% | 1.0% | 22.5% | Tidak |
| 81 | M15 | Break & Retest + Henti ATR | V2 Ekori SMA20 tanpa sasaran | SIMPAN | 37.1 | 18.7% | -33.0% | 33.2% | 1.1% | 27.5% | Tidak |
| 82 | M14 | Walking with the Whales | V3 V1 pegang ikut SMA50 | SIMPAN | 35.6 | 21.6% | -33.4% | 21.2% | 1.5% | 23.6% | Tidak |
| 83 | M148 | Natural Number Method | V1 WFO beku: henti PCT6, keluar EMA10, tmax 42 | SIMPAN | 34.7 | 19.9% | -29.4% | 35.1% | 0.5% | 22.7% | Tidak |
| 84 | M67 | Rayner Teo: Ujian Ketiga pada Purata 50 | V6 Versi Financial Wisdom: zon EMA20-EMA50, henti 2xATR | SIMPAN | 34.6 | 17.5% | -30.6% | 30.3% | 1.9% | 35.7% | Tidak |
| 85 | M132 | Ascending Scallop (Bulkowski) | V1 WFO beku: henti ATR4, keluar CHAN4, tmax 42 | SIMPAN | 34.1 | 17.8% | -22.8% | 42.0% | 1.0% | 44.4% | Tidak |
| 86 | M101 | Bulkowski: Tiga lembah menaik | V3 V1 + corak sambungan (tutup_a>tutup_a-63) | SIMPAN | 33.8 | 21.9% | -42.2% | 34.5% | 3.5% | 41.4% | Tidak |
| 87 | M26 | Garis Trend Undur 3 Sentuhan + Pecahan | V0 Sumber tulen (henti 0.99x low kotak, sasaran swing high kiri) | SIMPAN | 33.3 | 20.9% | -37.3% | 49.5% | 5.2% | 16.7% | Tidak |
| 88 | M122 | Moving Momentum (ChartSchool) | V1 WFO beku: henti LOW5, keluar TIADA, tmax 42 | SIMPAN | 29.7 | 16.2% | -35.4% | 35.0% | 1.8% | 39.6% | Tidak |
| 89 | M153 | Range Leader | V1 WFO beku: henti PCT12, keluar CHAN2, tmax 10 | SIMPAN | 23.4 | 18.6% | -38.0% | 43.1% | 0.2% | 13.9% | Tidak |
| 90 | M116 | 2/20 EMA Breakout (Landry) | V1 WFO beku: henti PCT10, keluar TIADA, tmax 10 | SIMPAN | 23.0 | 18.6% | -41.5% | 50.1% | 0.4% | 18.1% | Tidak |
| 91 | M24 | Rotasi Momentum ROC12 + SMA200 | V0 Sumber tulen (K=2, tiada henti) | DITOLAK |  | 57.7% | -65.6% | 53.8% | 28.9% | 86.5% | Ya |
| 92 | M125 | 2-Bar Breakout | V1 WFO beku: henti ATR2.5, keluar ASAL, tmax tiada | DITOLAK |  | 45.8% | -92.6% | 29.7% | 166.9% | 63.8% | Ya |
| 93 | M56 | Gray & Vogel Momentum Lancar (FIP) | V4 V1 tanpa FIP (8 MOM tertinggi) | DITOLAK |  | 40.9% | -52.5% | 42.7% | 19.9% | 69.9% | Ya |
| 94 | M94 | Pecutan Momentum (Chen, Yu & Wang) | V0 Rotasi sumber (bulanan, langkau 21h, pegang 126h) | DITOLAK |  | 40.4% | -37.6% | 63.0% | 24.0% | 85.0% | Ya |
| 95 | M140 | 猎豹出击 (Serangan Cheetah) | V1 WFO beku: henti ATR3, keluar SMA50, tmax 63 | DITOLAK |  | 37.6% | -46.3% | 36.1% | 5.3% | 49.0% | Ya |
| 96 | M126 | Hidden Smash Day (beli, Larry Williams) | V1 WFO beku: henti ATR3, keluar SMA50, tmax tiada | DITOLAK |  | 30.4% | -32.2% | 35.4% | 5.1% | 42.0% | Ya |
| 97 | M127 | Slingshot Bullish | V1 WFO beku: henti LOW1, keluar CHAN4, tmax tiada | DITOLAK |  | 25.1% | -49.9% | 19.2% | 2.6% | 20.3% | Ya |
| 98 | M147 | Improved Three-Bar Pullback | V1 WFO beku: henti PCT15, keluar ASAL, tmax tiada | DITOLAK |  | 24.7% | -38.3% | 30.6% | 91.0% | 69.9% | Ya |
| 99 | M156 | Single Penetration (DiNapoli) | V1 WFO beku: henti ATR3, keluar TIADA, tmax 10 | DITOLAK |  | 24.1% | -47.3% | 51.8% | 0.7% | 21.2% | Ya |
| 100 | M131 | Ross Hook (Joe Ross) | V1 WFO beku: henti ATR2, keluar TIADA, tmax 63 | DITOLAK |  | 22.9% | -47.3% | 29.7% | 2.4% | 42.1% | Ya |
| 101 | M136 | Short/Intermediate-term Low (Larry Williams) | V1 WFO beku: henti PCT10, keluar ASAL, tmax tiada | DITOLAK |  | 22.1% | -60.1% | 24.0% | 112.9% | 60.4% | Ya |
| 102 | M82 | Arthur Hill Rotasi Sasaran 10% | V0 Sumber tulen (sasaran 10% tutup / EMA25<EMA125, tiada henti) | DITOLAK |  | 20.8% | -33.0% | 61.1% | 1.8% | 63.4% | Tidak |
| 103 | M73 | ADX(5) > 40 + Julat Terkecil 6 Hari | V0 Sumber tulen (ADX5>40 + NR6; tiada henti; keluar tutup>high semalam) | DITOLAK |  | 20.6% | -45.1% | 63.5% | 0.2% | 5.7% | Tidak |
| 104 | M155 | Market Cycle Strategy | V1 WFO beku: henti ATR3, keluar TIADA, tmax 21 | DITOLAK |  | 19.9% | -46.0% | 49.1% | 1.6% | 38.2% | Tidak |
| 105 | M21 | Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | V5 V1 keluar close<SMA20 | DITOLAK |  | 19.5% | -21.5% | 25.8% | 2.6% | 28.4% | Tidak |
| 106 | M159 | Heikin-Ashi Trend | V1 WFO beku: henti PCT15, keluar SMA20, tmax 10 | DITOLAK |  | 18.7% | -40.5% | 40.1% | 0.2% | 14.3% | Tidak |
| 107 | M121 | High 2 bull flag (Brooks) | V1 WFO beku: henti PCT15, keluar ASAL, tmax 63 | DITOLAK |  | 17.5% | -31.6% | 46.7% | 2.5% | 57.4% | Tidak |
| 108 | M23 | Breitstein Kapitulasi + Kesinambungan | V5 V4 keluar close<SMA20 | DITOLAK |  | 16.8% | -40.8% | 22.1% | 0.5% | 21.4% | Tidak |
| 109 | M87 | IBD Tapak Menaik | V4 V1 tanpa DAHULU | DITOLAK |  | 15.8% | -30.7% | 32.1% | 3.5% | 43.0% | Tidak |
| 110 | M02 | MACD + SMA200 | V5 V1+sasaran 3R | DITOLAK |  | 15.0% | -39.5% | 43.6% | 0.7% | 29.6% | Tidak |
| 111 | M35 | Pocket Pivot Morales & Kacher | V3 V1 DEKAT10 sahaja | DITOLAK |  | 14.9% | -36.4% | 28.2% | 0.3% | 18.9% | Tidak |
| 112 | M100 | Bulkowski Segi Empat & Segi Tiga Menaik | V0 Sumber tulen (proksi): sasaran T+tinggi, tiada exitc | DITOLAK |  | 14.9% | -25.5% | 46.4% | 1.3% | 36.1% | Tidak |
| 113 | M50 | Elder Triple Screen | V2 V1 keluar tutup<SMA50 + tutup>SMA50 | DITOLAK |  | 14.9% | -38.7% | 22.9% | 1.8% | 28.0% | Tidak |
| 114 | M49 | Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | V4 V1 + awan hadapan hijau (RA>RB) | DITOLAK |  | 14.8% | -41.3% | 23.4% | 4.0% | 35.9% | Tidak |
| 115 | M31 | Band Walk (BB 20/2) | V0 Peraturan pengguna (henti tutup<LOWER isyarat, keluar MID turun) | DITOLAK |  | 14.7% | -32.3% | 42.9% | 3.3% | 46.5% | Tidak |
| 116 | M34 | Carter TTM Squeeze | V2 V1 keluar close<SMA50 | DITOLAK |  | 14.6% | -24.3% | 33.7% | 2.4% | 40.4% | Tidak |
| 117 | M03 | BB Break + Divergence RSI | V1 Spesifikasi dikunci | DITOLAK |  | 14.6% | -49.4% | 56.2% | 0.6% | 16.0% | Tidak |
| 118 | M38 | Darvas Kotak | V4 V1 atas bar mingguan | DITOLAK |  | 14.5% | -33.8% | 49.4% | 18.8% | 75.5% | Tidak |
| 119 | M104 | High Tight Flag / Power Play | V2 V1 + tiang >=50% | DITOLAK |  | 14.1% | -26.3% | 34.6% | 5.6% | 54.9% | Tidak |
| 120 | M01 | Bollinger Band + RSI | V0 Video tulen | DITOLAK |  | 12.8% | -46.4% | 66.5% | 2.2% | 37.6% | Tidak |
| 121 | M36 | Turtle 55/20 | V2 V1 keluar tutup<SMA50 + sig tutup>SMA50 | DITOLAK |  | 12.5% | -35.3% | 32.1% | 2.6% | 39.8% | Tidak |
| 122 | M141 | First Thrust (Landry) | V1 WFO beku: henti ATR2.5, keluar ASAL, tmax 63 | DITOLAK |  | 12.3% | -32.8% | 38.8% | 4.0% | 50.8% | Tidak |
| 123 | M07 | Qullamaggie Breakout | V11 V7 keluar close<SMA20 | DITOLAK |  | 11.7% | -41.3% | 20.4% | 1.1% | 26.0% | Tidak |
| 124 | M145 | Yum-Yum Continuation | V1 WFO beku: henti LOW10, keluar ASAL, tmax tiada | DITOLAK |  | 10.9% | -44.1% | 24.6% | 80.5% | 63.2% | Tidak |
| 125 | M120 | Reversal New Highs | V1 WFO beku: henti ASAL, keluar SMA50, tmax tiada | DITOLAK |  | 10.7% | -20.3% | 26.9% | 1.1% | 32.0% | Tidak |
| 126 | M51 | O'Neil Cawan & Pemegang | V3 V1 kedalaman cawan 12-50% | DITOLAK |  | 10.5% | -24.3% | 38.9% | 3.1% | 43.7% | Tidak |
| 127 | M59 | Anjakan Julat RSI | V3 V1 LB65 ambang 39/69 (imbasan Hill 2019) | DITOLAK |  | 9.8% | -52.0% | 34.1% | 3.1% | 44.0% | Tidak |
| 128 | M157 | Consolidation Pivot Breakout (versi angka) | V1 WFO beku: henti PCT6, keluar ASAL, tmax tiada | DITOLAK |  | 9.1% | -19.3% | 14.3% | 32.0% | 41.2% | Tidak |
| 129 | M76 | Undercut & Rally pada Low Penting | V1 Dikunci (UR + CLV>0.60 + tutup>SMA200) | DITOLAK |  | 8.6% | -26.5% | 36.8% | 0.7% | 22.4% | Tidak |
| 130 | M115 | Bow Tie (Landry) | V1 WFO beku: henti ASAL, keluar ASAL, tmax 42 | DITOLAK |  | 8.3% | -17.4% | 27.3% | 1.1% | 33.2% | Tidak |
| 131 | M44 | Tapak Rata IBD | V3 V1 tanpa syarat volum | DITOLAK |  | 8.2% | -18.9% | 30.3% | 0.4% | 37.7% | Tidak |
| 132 | M25 | VWAP Wave (proksi harian) | V2 V1 tanpa sasaran | DITOLAK |  | 7.8% | -44.6% | 29.8% | 0.4% | 23.5% | Tidak |
| 133 | M68 | Kell Base n' Break | V3 V1 keluar close<SMA50 (+tutup>SMA50) | DITOLAK |  | 7.6% | -35.6% | 35.7% | 1.4% | 42.2% | Tidak |
| 134 | M138 | 直升机空中加油 (Helikopter isi minyak di udara) | V1 WFO beku: henti ATR4, keluar TIADA, tmax 63 | DITOLAK |  | 6.8% | -36.4% | 44.6% | 4.6% | 56.0% | Tidak |
| 135 | M143 | 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | V1 WFO beku: henti ATR3.5, keluar CHAN4, tmax 21 | DITOLAK |  | 6.5% | -23.3% | 52.2% | 0.8% | 27.9% | Tidak |
| 136 | M47 | Holy Grail Raschke | V3 V1 tanpa syarat ADX naik | DITOLAK |  | 6.0% | -18.6% | 51.2% | 0.2% | 10.8% | Tidak |
| 137 | M64 | O'Neil Tiga Minggu Ketat | V5 V1 henti 0.92xPIVOT | DITOLAK |  | 5.1% | -41.2% | 33.8% | 1.7% | 42.5% | Tidak |
| 138 | M117 | Landry Pullback (high 2 bulan) | V1 WFO beku: henti ATR3, keluar ASAL, tmax tiada | DITOLAK |  | 3.8% | -40.2% | 21.0% | 45.5% | 56.4% | Tidak |
| 139 | M22 | Qullamaggie Episodic Pivot | V0 Sumber tulen (QQQ EMA, jurang>=10%, vol>=3x, henti low hari jurang, keluar<SMA10) | DITOLAK |  | 2.5% | -8.7% | 40.5% | 3.4% | 42.9% | Tidak |
| 140 | M28 | VWAP Separator + Kiss Pivot | V2 Pemisahan ≥3 ATR | DITOLAK |  | 2.4% | -39.1% | 42.8% | 0.2% | 12.8% | Tidak |
