# Papan Kedudukan Kaedah M (set 431, varian skor tertinggi)

Jana daripada data/registry_M_gabung.csv. 88 kaedah, 550 varian diuji atas 431 saham. Status terbaik setiap kaedah: DITOLAK 31, SIMPAN 30, UJI KERTAS 23, GUNA 4.

Skor kosong = gagal gate (DITOLAK).

| # | ID | Kaedah | Varian terbaik | Keputusan | Skor | CAGR | MDD | Win | Purata/dagangan | Hit10 | Menang EW |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M96 | Momo India: Ranking Sharpe 3/6/12 bulan | V1 Dikunci (+henti tutup-3xATR14) | GUNA | 80.3 | 40.0% | -42.0% | 42.5% | 12.2% | 63.3% | Ya |
| 2 | M114 | RS Peneraju Pasaran Naik | V4 Kolam 10% | GUNA | 77.4 | 49.6% | -38.8% | 38.1% | 4.0% | 56.1% | Ya |
| 3 | M30 | BB Free Bar + Himpitan 50/2.5 | V3 V1 tetapi BB20/2 | GUNA | 76.2 | 52.0% | -36.8% | 36.6% | 3.8% | 45.1% | Ya |
| 4 | M79 | Radge: 20% Flipper | V3 V1 dengan A=0.15 (masuk/keluar/henti 15%) | GUNA | 75.9 | 35.5% | -39.9% | 40.4% | 6.2% | 63.5% | Ya |
| 5 | M111 | Sistem Volatiliti Wilder | V5 V1 henti maks(tutup-3xATR7; 0.88xtutup) | UJI KERTAS | 74.2 | 43.0% | -34.9% | 38.6% | 2.4% | 45.3% | Ya |
| 6 | M74 | Lulus Baharu Trend Template Minervini | V2 V1 tanpa S8 (7 syarat harga) | UJI KERTAS | 73.2 | 37.1% | -33.4% | 24.0% | 2.7% | 28.8% | Ya |
| 7 | M05 | MACD Divergence + Pengesahan | V3 V1+close>SMA200 | UJI KERTAS | 71.8 | 28.4% | -25.7% | 34.9% | 10.8% | 54.8% | Ya |
| 8 | M80 | Radge Saluran Purata Bergerak (MAC) | V2 V1 dengan henti tutup-3xATR14 | UJI KERTAS | 71.6 | 38.1% | -38.6% | 35.6% | 8.9% | 53.6% | Ya |
| 9 | M12 | Parabolic SAR | V5 V1 keluar close<SMA50 | UJI KERTAS | 69.5 | 31.1% | -28.8% | 29.5% | 2.0% | 33.6% | Ya |
| 10 | M46 | Jurang Naik Boleh Beli (Buyable Gap Up) | V2 V1 dengan jurang ketat (low>high semalam+0.75xATR40) | UJI KERTAS | 69.5 | 26.3% | -20.6% | 22.7% | 2.8% | 29.6% | Ya |
| 11 | M40 | Clenow Stocks on the Move | V4 V1 tanpa penapis pasaran | UJI KERTAS | 68.9 | 25.6% | -35.8% | 38.3% | 4.8% | 51.8% | Ya |
| 12 | M37 | Weinstein Peringkat 2 | V2 V1 keluar tutup harian<SMA50 + tutup>SMA50 | UJI KERTAS | 67.7 | 29.5% | -31.2% | 41.3% | 5.5% | 55.4% | Ya |
| 13 | M04 | BB Squeeze Breakout | U2 asas V2 + E1 volume>=1.5xSMA20 | UJI KERTAS | 67.5 | 46.4% | -41.1% | 35.6% | 5.0% | 42.6% | Ya |
| 14 | M66 | IBD Undur Pertama ke Purata 50 Hari | V0 Sumber tulen (UNDUR+NAIK50+PUSING+BARU; tanpa PERTAMA/HIGHBARU/NIPIS) | UJI KERTAS | 66.7 | 51.1% | -30.9% | 28.1% | 1.7% | 28.5% | Ya |
| 15 | M52 | Radge Weekend Trend Trader | V3 V1 keluar tutup<SMA50 harian | UJI KERTAS | 66.7 | 28.2% | -30.8% | 37.2% | 5.2% | 49.3% | Ya |
| 16 | M18 | EMA9/21 Pullback | V2 V1 Model A sahaja | UJI KERTAS | 66.0 | 44.3% | -44.5% | 25.7% | 0.4% | 16.9% | Ya |
| 17 | M105 | Supertrend tulen | V1 Dikunci (V0 + had henti 12%) | UJI KERTAS | 65.3 | 29.6% | -33.1% | 38.9% | 2.4% | 46.8% | Ya |
| 18 | M13 | Garis Trend Action/Safety Line | V1 Spesifikasi dikunci | UJI KERTAS | 65.2 | 52.1% | -37.5% | 34.4% | 1.0% | 26.1% | Ya |
| 19 | M10 | EMA3 + CCI + MACD | V4 V1 pencetus CCI>+100 | UJI KERTAS | 65.0 | 28.5% | -29.3% | 32.5% | 4.7% | 45.5% | Ya |
| 20 | M45 | High 52 Minggu (George & Hwang) | V4 V1 + high 52 minggu dicapai dalam 21 hari | UJI KERTAS | 64.7 | 30.7% | -40.5% | 32.3% | 12.8% | 54.3% | Ya |
| 21 | M77 | Undercut & Rally pada Purata Bergerak (MAU&R) | V2 V1 henti=low hari isyarat | UJI KERTAS | 63.4 | 42.4% | -33.8% | 24.7% | 2.7% | 23.6% | Ya |
| 22 | M84 | Jarak purata bergerak MAD 21/200 | V5 V1 + SMA50 | UJI KERTAS | 63.3 | 33.0% | -44.4% | 37.2% | 3.7% | 45.9% | Ya |
| 23 | M54 | IBD Power Trend | V4 V1 sig=PT benar & tutup>high 20 hari | UJI KERTAS | 63.1 | 31.0% | -38.7% | 29.6% | 3.4% | 40.6% | Ya |
| 24 | M32 | Momentum Burst | V2 V1 keluar close<SMA50 | UJI KERTAS | 62.7 | 43.3% | -36.8% | 24.6% | 3.6% | 36.6% | Ya |
| 25 | M55 | Guppy GMMA | V4 Undur ke kumpulan panjang lalu lantun (Persediaan 2) | UJI KERTAS | 60.9 | 29.0% | -31.0% | 25.6% | 2.7% | 34.9% | Ya |
| 26 | M57 | Landry Trend Knockout (TKO) | V1 Dikunci (keluar tutup<SMA50) | UJI KERTAS | 60.8 | 33.1% | -43.9% | 21.2% | 1.6% | 27.1% | Ya |
| 27 | M41 | FW Penyatuan Mingguan | V0 Sumber sahaja (tanpa had julat 25%) | UJI KERTAS | 60.5 | 27.3% | -34.6% | 35.7% | 15.0% | 58.3% | Ya |
| 28 | M90 | Pring KST | V3 V1 + tutup>SMA50, keluar tutup<SMA50 | SIMPAN | 59.9 | 35.4% | -42.2% | 29.5% | 1.9% | 36.9% | Ya |
| 29 | M102 | Stockbee SLTB | V5 V1 + volum hari ini > semalam | SIMPAN | 58.6 | 37.3% | -38.3% | 18.1% | 1.3% | 24.1% | Ya |
| 30 | M91 | Stochastic Pop (Bernstein/Steckler) | V2 V1 + tutup>HH20 (pecah keluar) | SIMPAN | 58.5 | 25.1% | -20.8% | 41.8% | 1.6% | 35.6% | Ya |
| 31 | M11 | NR7 Breakout + Volume | V3 V1+NR7 hari dalam (NR7-ID) | SIMPAN | 57.9 | 29.9% | -28.3% | 36.1% | 2.9% | 28.9% | Ya |
| 32 | M92 | CCI-50 | V2 V1 isyarat silang atas sifar (NAIK0) | SIMPAN | 57.9 | 28.1% | -31.8% | 48.7% | 1.2% | 29.5% | Ya |
| 33 | M81 | Bensdorp Long Trend High Momentum | V4 V1 henti awal 3xATR20 | SIMPAN | 57.1 | 28.0% | -40.7% | 31.9% | 8.6% | 59.3% | Ya |
| 34 | M89 | Chande 65sma-3cc | V5 V1+SMA65 naik (>SMA65 10h lalu) | SIMPAN | 56.3 | 25.9% | -31.0% | 34.2% | 1.8% | 39.8% | Ya |
| 35 | M27 | Price Action 4 Tiang | V2 Persediaan A sahaja (flip & hold) | SIMPAN | 55.5 | 32.2% | -39.2% | 35.2% | 0.4% | 14.5% | Ya |
| 36 | M39 | Radge Pecahan Bollinger 100 hari | V4 V1 jalur atas 2 SD | SIMPAN | 54.7 | 23.4% | -26.4% | 37.3% | 9.1% | 59.5% | Ya |
| 37 | M70 | Pecahan Hari Dalam | V5 V1 masuk awal tanpa pengesahan | SIMPAN | 54.5 | 37.9% | -37.2% | 11.5% | 0.8% | 15.0% | Ya |
| 38 | M09 | Volumatic VIDYA Pivot Retest | V2 V1 tanpa sasaran | SIMPAN | 54.3 | 23.9% | -24.5% | 23.5% | 1.8% | 35.2% | Ya |
| 39 | M88 | O'Neil Shakeout +3 | V1 Dikunci (BELI 1.10xL1; vol>VOL50; henti max(L2;0.92x masuk); keluar tutup<low20) | SIMPAN | 52.8 | 22.0% | -39.3% | 32.3% | 5.6% | 46.6% | Ya |
| 40 | M78 | Alvarez Pecahan Mingguan DTAYS | V2 V1 henti mengekor 5xATR100 | SIMPAN | 51.5 | 21.9% | -39.0% | 32.0% | 3.2% | 47.8% | Tidak |
| 41 | M29 | EMA3 + RSI75 + Stokastik | V4 V1 EMA 50/110/250 | SIMPAN | 51.2 | 22.1% | -24.4% | 18.0% | 3.2% | 28.6% | Ya |
| 42 | M19 | Sneaky Pivot (proksi harian) | V1 Spesifikasi dikunci | SIMPAN | 48.6 | 25.8% | -37.0% | 44.0% | 0.3% | 25.3% | Ya |
| 43 | M48 | Cooper 1-2-3-4 | V3 V1 henti low hari 3 - 1xATR14 | SIMPAN | 48.6 | 23.3% | -38.2% | 34.1% | 2.8% | 41.4% | Ya |
| 44 | M95 | Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur) | V1 Dikunci: PECAH20+PTH>=0.85+HSHP<=21+tutup>SMA50 | SIMPAN | 48.1 | 27.1% | -32.8% | 32.2% | 2.7% | 37.9% | Ya |
| 45 | M93 | Bollinger Kaedah II: %b + MFI | V2 V1, keluar LEMAH (%b<0.20 & MFI10<20) | SIMPAN | 47.9 | 23.9% | -38.5% | 36.2% | 8.2% | 52.6% | Ya |
| 46 | M99 | Three Line Break | V4 V1 + close>SMA200 | SIMPAN | 47.9 | 22.1% | -29.3% | 39.6% | 1.2% | 30.7% | Ya |
| 47 | M33 | Supertrend + SMA10 | V5 V1 + volum>VOL20 | SIMPAN | 47.9 | 21.2% | -29.4% | 40.1% | 1.7% | 47.0% | Tidak |
| 48 | M08 | SMA20 + SMA200 | V1 Spesifikasi dikunci | SIMPAN | 46.0 | 23.0% | -34.0% | 31.7% | 1.1% | 26.8% | Ya |
| 49 | M06 | Minervini VCP Breakout | V5 V1 tanpa VCP | SIMPAN | 40.1 | 23.0% | -31.4% | 33.1% | 2.5% | 42.7% | Ya |
| 50 | M20 | EMA10/15 Crossover + Sudut | V3 V1 tanpa syarat sudut | SIMPAN | 39.7 | 19.7% | -22.4% | 39.2% | 0.2% | 13.5% | Tidak |
| 51 | M107 | Golden Cross SMA50/200 | V5 V1 + SPY>SMA200 | SIMPAN | 39.5 | 16.8% | -24.4% | 31.7% | 15.4% | 52.0% | Tidak |
| 52 | M106 | DMI Wilder | V5 V1 dengan henti tutup-2xATR14 | SIMPAN | 37.3 | 18.2% | -34.8% | 32.1% | 1.0% | 22.5% | Tidak |
| 53 | M15 | Break & Retest + Henti ATR | V2 Ekori SMA20 tanpa sasaran | SIMPAN | 37.1 | 18.7% | -33.0% | 33.2% | 1.1% | 27.5% | Tidak |
| 54 | M14 | Walking with the Whales | V3 V1 pegang ikut SMA50 | SIMPAN | 35.6 | 21.6% | -33.4% | 21.2% | 1.5% | 23.6% | Tidak |
| 55 | M67 | Rayner Teo: Ujian Ketiga pada Purata 50 | V6 Versi Financial Wisdom: zon EMA20-EMA50, henti 2xATR | SIMPAN | 34.6 | 17.5% | -30.6% | 30.3% | 1.9% | 35.7% | Tidak |
| 56 | M101 | Bulkowski: Tiga lembah menaik | V3 V1 + corak sambungan (tutup_a>tutup_a-63) | SIMPAN | 33.8 | 21.9% | -42.2% | 34.5% | 3.5% | 41.4% | Tidak |
| 57 | M26 | Garis Trend Undur 3 Sentuhan + Pecahan | V0 Sumber tulen (henti 0.99x low kotak, sasaran swing high kiri) | SIMPAN | 33.3 | 20.9% | -37.3% | 49.5% | 5.2% | 16.7% | Tidak |
| 58 | M24 | Rotasi Momentum ROC12 + SMA200 | V0 Sumber tulen (K=2, tiada henti) | DITOLAK |  | 57.7% | -65.6% | 53.8% | 28.9% | 86.5% | Ya |
| 59 | M94 | Pecutan Momentum (Chen, Yu & Wang) | V0 Rotasi sumber (bulanan, langkau 21h, pegang 126h) | DITOLAK |  | 40.4% | -37.6% | 63.0% | 24.0% | 85.0% | Ya |
| 60 | M56 | Gray & Vogel Momentum Lancar (FIP) | V0 Sumber tulen (tiada henti) | DITOLAK |  | 28.1% | -31.9% | 56.9% | 12.8% | 70.5% | Ya |
| 61 | M82 | Arthur Hill Rotasi Sasaran 10% | V0 Sumber tulen (sasaran 10% tutup / EMA25<EMA125, tiada henti) | DITOLAK |  | 20.8% | -33.0% | 61.1% | 1.8% | 63.4% | Tidak |
| 62 | M73 | ADX(5) > 40 + Julat Terkecil 6 Hari | V0 Sumber tulen (ADX5>40 + NR6; tiada henti; keluar tutup>high semalam) | DITOLAK |  | 20.6% | -45.1% | 63.5% | 0.2% | 5.7% | Tidak |
| 63 | M100 | Bulkowski Segi Empat & Segi Tiga Menaik | V0 Sumber tulen (proksi): sasaran T+tinggi, tiada exitc | DITOLAK |  | 14.9% | -25.5% | 46.4% | 1.3% | 36.1% | Tidak |
| 64 | M31 | Band Walk (BB 20/2) | V0 Peraturan pengguna (henti tutup<LOWER isyarat, keluar MID turun) | DITOLAK |  | 14.7% | -32.3% | 42.9% | 3.3% | 46.5% | Tidak |
| 65 | M03 | BB Break + Divergence RSI | V0 Sumber tulen (tgt BBU, tiada henti) | DITOLAK |  | 13.9% | -48.4% | 73.2% | 1.4% | 16.5% | Tidak |
| 66 | M01 | Bollinger Band + RSI | V0 Video tulen | DITOLAK |  | 12.8% | -46.4% | 66.5% | 2.2% | 37.6% | Tidak |
| 67 | M87 | IBD Tapak Menaik | V0 Sumber tulen (tiada henti/keluar; had masa 60h) | DITOLAK |  | 12.3% | -22.8% | 57.4% | 6.1% | 66.4% | Tidak |
| 68 | M38 | Darvas Kotak | V0 Sumber tulen (Bulkowski; kotak tetap) | DITOLAK |  | 9.6% | -46.9% | 25.2% | 38.8% | 59.1% | Tidak |
| 69 | M35 | Pocket Pivot Morales & Kacher | V0 Sumber bernombor sahaja | DITOLAK |  | 9.6% | -49.3% | 26.9% | 0.3% | 19.2% | Tidak |
| 70 | M02 | MACD + SMA200 | V0 Sumber tulen | DITOLAK |  | 9.5% | -32.8% | 47.5% | 2.9% | 43.9% | Tidak |
| 71 | M76 | Undercut & Rally pada Low Penting | V0 Sumber tulen (UR sahaja; tanpa CLV/SMA200) | DITOLAK |  | 7.5% | -69.1% | 30.6% | 1.6% | 19.0% | Tidak |
| 72 | M59 | Anjakan Julat RSI | V0 Sumber tulen (tiada henti; keluar RSI14<40) | DITOLAK |  | 5.1% | -38.0% | 33.6% | 3.1% | 44.0% | Tidak |
| 73 | M49 | Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | V0 Peraturan teras (silang TK di atas awan) | DITOLAK |  | 5.0% | -34.2% | 24.1% | 3.5% | 36.9% | Tidak |
| 74 | M21 | Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | V0 Sumber tulen (BO|EP|MC, henti low_i, keluar <SMA10 atau merah hari masuk) | DITOLAK |  | 4.1% | -48.2% | 25.4% | 0.2% | 22.1% | Tidak |
| 75 | M44 | Tapak Rata IBD | V0 Sumber tulen (henti 8%, sasaran +20%) | DITOLAK |  | 3.9% | -20.9% | 34.6% | 1.2% | 47.6% | Tidak |
| 76 | M64 | O'Neil Tiga Minggu Ketat | V0 Sumber tulen: KETAT 1.5% tanpa NAIK, henti 0.92xPIVOT, keluar tutup<SMA50 | DITOLAK |  | 3.3% | -32.9% | 33.6% | 0.9% | 36.3% | Tidak |
| 77 | M68 | Kell Base n' Break | V0 Sumber tulen (pecah pangsi 10h + tutup>EMA10>EMA20 semalam; henti low bar pecahan) | DITOLAK |  | 2.6% | -58.4% | 23.1% | 0.4% | 21.6% | Tidak |
| 78 | M51 | O'Neil Cawan & Pemegang | V0 Sumber tulen (henti 8%, sasaran pangsi+kedalaman cawan, tiada keluar lain) | DITOLAK |  | 2.5% | -25.9% | 34.5% | 1.3% | 49.4% | Tidak |
| 79 | M22 | Qullamaggie Episodic Pivot | V0 Sumber tulen (QQQ EMA, jurang>=10%, vol>=3x, henti low hari jurang, keluar<SMA10) | DITOLAK |  | 2.5% | -8.7% | 40.5% | 3.4% | 42.9% | Tidak |
| 80 | M36 | Turtle 55/20 | V0 Sumber sehampir mungkin (Sistem 2, tanpa ranking) | DITOLAK |  | 1.0% | -50.5% | 31.5% | 2.9% | 40.6% | Tidak |
| 81 | M47 | Holy Grail Raschke | V0 Versi SMA20 (bukan versi pengarang) | DITOLAK |  | 0.9% | -5.0% | 56.9% | 0.7% | 13.9% | Tidak |
| 82 | M104 | High Tight Flag / Power Play | V0 Sumber tulen (L 15-30, henti low rehat tanpa had) | DITOLAK |  | -0.1% | -10.2% | 33.3% | -0.6% | 66.7% | Tidak |
| 83 | M07 | Qullamaggie Breakout | V0 Sumber tulen (henti low hari pecahan, keluar close<SMA10) | DITOLAK |  | -0.8% | -57.0% | 21.9% | -0.2% | 16.0% | Tidak |
| 84 | M34 | Carter TTM Squeeze | V0 Sumber tulen (tanpa ALIRAN; keluar MOM turun 1 bar) | DITOLAK |  | -1.9% | -54.9% | 38.7% | 0.3% | 17.0% | Tidak |
| 85 | M25 | VWAP Wave (proksi harian) | V0 Sumber tulen (henti 0.99x low, 1.5R, tiada exitc/tmax/volume) | DITOLAK |  | -2.0% | -35.3% | 41.1% | 0.2% | 12.3% | Tidak |
| 86 | M28 | VWAP Separator + Kiss Pivot | V0 Sumber tulen (Separator, tiada had masa) | DITOLAK |  | -2.1% | -50.1% | 47.0% | 0.2% | 9.1% | Tidak |
| 87 | M50 | Elder Triple Screen | V0 Sumber tulen (sasaran 2R) | DITOLAK |  | -3.5% | -67.4% | 35.8% | 0.4% | 14.2% | Tidak |
| 88 | M23 | Breitstein Kapitulasi + Kesinambungan | V0 Kapitulasi tulen (henti low V, keluar close<low semalam) | DITOLAK |  | -5.8% | -41.7% | 34.5% | -0.5% | 32.3% | Tidak |
