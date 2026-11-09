# Skor Kaedah 0–100 (pangkat maklumat, BUKAN keputusan)

> **Status keputusan (kad skor, harga 2026-11-06):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana 2026-11-09 oleh `standard/skor_kaedah.py` (Actions `analisis.yml`, selepas kad skor). Harga pada tutup 2026-11-06; 223 kaedah; 16 hari beli langsung (rejim ON 1, OFF 15). Pradaftar 2026-11-09: `standard/SPEC_SKOR_KAEDAH.md` (berat dan sauh dikunci `ujian/test_skor_kaedah.py::TestKunci`). Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Cara membaca

- **Skor** = min geometri berberat empat tiang (Untung 35 · Tahan 30 · Bukti 25 · Konsisten 10), dikecut ke 50 mengikut data: berat data = hari beli ÷ (hari beli + 20). Kaedah dengan 2 hari beli tidak boleh menjauhi 50. 100 = unggul semua segi; 50 = neutral/tiada bukti; < 50 = lebih buruk daripada neutral.
- **Siling** ikut kad skor: NEGATIF ≤ 20, GANTUNG/BERSARA ≤ 30, GAGAL ≤ 40. Tanda ⌈ = siling terpakai.
- **Satu-satunya status yang membenarkan wang sebenar ialah TERBUKTI dalam `laporan/KAD_SKOR.md`.** Skor tinggi dengan status BELUM CUKUP bermaksud "paling menjanjikan setakat ini", bukan "selamat".
- Deflasi ujian berganda (López de Prado): sauh t Bukti C1 = maks(2.0, E[maks 223 normal]) = 2.80.
- **Semakan kebolehramalan:** belum ada snapshot skor ≥ 7 hari lalu (sejarah bermula 2026-11-06); skor dipercayai sebagai pangkat hanya selepas 8–12 minggu semakan positif.
- Metrik T4 (A2, B1, B2, D1) dikira atas lorong T4 L1 **dipotong pada sesi LANGSUNG pertama** kaedah itu (Mxx 2026-10-16, Nxx/GB 2026-11-03) dan diasas semula; sesi isian bina semula tidak dikira (pindaan 9 Nov 2026 (a)). Lajur "T4 sesi/pul" di bawah ialah potongan itu, bukan lorong penuh `T4_KAEDAH.md`.

## Semua kaedah, susun ikut Skor

| # | Kaedah | Skor | Untung | Tahan | Bukti | Konsisten | Status kad | Hari beli | Posisi/tutup | Jangkaan % | T4 sesi | T4 pul % | T4 pul/|MDD| | Ulcer | t buku | Lift | WFE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `M133` Bull Hook (Crabel) | **61.1** | 94 | 89 | 58 | 85 | BELUM CUKUP | 11 | 38/19 | +1.69 | 16 | +5.43 | +1.31 | 1.6 | +1.39 | – | 15.39 |
| 2 | `M33` Supertrend + SMA10 | **60.5** | 79 | 78 | 59 | 85 | BELUM CUKUP | 16 | 195/35 | +0.93 | 16 | +7.90 | +2.96 | 1.4 | +1.15 | – | 4.53 |
| 3 | `M146` 3-Bar Momentum Pattern | **59.2** | 73 | 73 | 60 | 85 | BELUM CUKUP | 16 | 76/27 | +0.70 | 16 | +3.28 | +0.53 | 1.9 | +1.38 | – | 2.92 |
| 4 | `M118` Expansion Pivot (Cooper) | **57.1** | 62 | 79 | 52 | 85 | BELUM CUKUP | 16 | 69/19 | -0.19 | 16 | +8.71 | +3.22 | 0.9 | +0.59 | – | 2.00 |
| 5 | `M25` VWAP Wave (proksi harian) | **56.5** | 64 | 69 | 57 | 80 | BELUM CUKUP | 15 | 138/81 | -0.34 | 16 | +4.24 | +0.73 | 2.9 | +0.54 | – | 3.77 |
| 6 | `M151` Outside Bar Failure | **56.4** | 64 | 80 | 51 | 67 | BELUM CUKUP | 15 | 81/44 | -0.43 | 16 | +6.36 | +5.23 | 0.5 | +0.16 | – | 0.41 |
| 7 | `M124` 'Last' Stochastic Technique (C | **54.8** | 59 | 66 | 55 | 69 | BELUM CUKUP | 16 | 328/156 | -0.42 | 16 | +3.35 | +0.73 | 2.5 | +0.21 | – | 0.48 |
| 8 | `M100` Bulkowski Segi Empat & Segi Ti | **54.5** | 60 | 66 | 50 | 81 | BELUM CUKUP | 14 | 58/37 | -0.36 | 16 | +2.95 | +0.67 | 2.2 | +0.15 | – | 0.87 |
| 9 | `M105` Supertrend tulen | **53.9** | 59 | 53 | 57 | 85 | BELUM CUKUP | 16 | 307/85 | +0.01 | 16 | +0.59 | +0.08 | 2.5 | +0.50 | – | 1.40 |
| 10 | `M111` Sistem Volatiliti Wilder | **53.7** | 58 | 54 | 55 | 85 | BELUM CUKUP | 16 | 223/70 | -0.30 | 16 | +2.73 | +0.41 | 3.5 | +0.42 | – | 1.08 |
| 11 | `M74` Lulus Baharu Trend Template Mi | **53.3** | 57 | 64 | 51 | 58 | BELUM CUKUP | 16 | 76/48 | -0.68 | 16 | +1.83 | +0.44 | 2.2 | +0.05 | – | 0.11 |
| 12 | `M13` Garis Trend Action/Safety Line | **53.2** | 55 | 70 | 49 | 55 | BELUM CUKUP | 16 | 650/399 | -0.95 | 16 | +5.94 | +1.67 | 1.3 | -0.52 | – | -1.07 |
| 13 | `M91` Stochastic Pop (Bernstein/Stec | **52.9** | 54 | 64 | 50 | 85 | BELUM CUKUP | 11 | 33/10 | -0.93 | 16 | +5.31 | +0.68 | 2.3 | +0.68 | – | 3.16 |
| 14 | `M160` Measured Move Up | **52.4** | 47 | 58 | 58 | 85 | BELUM CUKUP | 14 | 81/39 | -1.31 | 16 | +0.85 | +0.18 | 2.2 | +1.01 | – | 9.08 |
| 15 | `M15` Break & Retest + Henti ATR | **52.3** | 66 | 49 | 56 | 42 | BELUM CUKUP | 16 | 254/138 | +0.59 | 16 | -3.47 | -0.47 | 2.7 | +0.32 | – | 0.69 |
| 16 | `M145` Yum-Yum Continuation | **52.3** | 49 | 67 | 51 | 56 | BELUM CUKUP | 16 | 276/53 | -0.87 | 16 | +2.21 | +1.01 | 1.4 | +0.02 | – | 0.02 |
| 17 | `M89` Chande 65sma-3cc | **52.2** | 48 | 67 | 51 | 55 | BELUM CUKUP | 16 | 148/77 | -1.24 | 16 | +3.50 | +0.73 | 1.8 | -0.09 | – | -0.30 |
| 18 | `M10` EMA3 + CCI + MACD | **52.0** | 48 | 67 | 50 | 55 | BELUM CUKUP | 16 | 99/46 | -1.19 | 16 | +7.11 | +1.35 | 1.7 | +0.00 | – | 0.01 |
| 19 | `M142` Pecahan volum dari dasar (底部放量 | **51.7** | 61 | 63 | 40 | 55 | BELUM CUKUP | 12 | 37/4 | +0.04 | 14 | +1.26 | +0.26 | 1.8 | -0.00 | – | -0.00 |
| 20 | `M158` Doubly Adaptive Profit Targets | **51.6** | 60 | 46 | 59 | 47 | BELUM CUKUP | 16 | 330/111 | +0.12 | 16 | -2.10 | -0.34 | 2.2 | +0.67 | – | 2.02 |
| 21 | `M93` Bollinger Kaedah II: %b + MFI | **51.5** | 55 | 46 | 54 | 70 | BELUM CUKUP | 16 | 239/69 | -0.17 | 16 | -0.86 | -0.14 | 2.0 | +0.31 | – | 0.52 |
| 22 | `M21` Marius 3 Persediaan (Pecahan+J | **51.3** | 69 | 60 | 44 | 45 | BELUM CUKUP | 5 | 5/2 | +0.33 | 8 | +0.21 | +0.10 | 1.2 | +1.09 | – | 2.36 |
| 23 | `M137` Livermore System | **51.2** | 47 | 60 | 51 | 59 | BELUM CUKUP | 16 | 148/52 | -1.40 | 16 | +3.27 | +0.55 | 2.5 | +0.05 | – | 0.13 |
| 24 | `M129` Wick Play | **51.0** | 48 | 61 | 44 | 77 | BELUM CUKUP | 9 | 23/9 | -1.19 | 16 | +3.56 | +1.26 | 1.0 | +0.14 | – | 0.74 |
| 25 | `M80` Radge Saluran Purata Bergerak  | **50.9** | 60 | 45 | 56 | 43 | BELUM CUKUP | 16 | 241/46 | +0.29 | 16 | -2.04 | -0.29 | 3.2 | +0.61 | – | 0.93 |
| 26 | `M48` Cooper 1-2-3-4 | **50.5** | 46 | 53 | 48 | 80 | BELUM CUKUP | 14 | 45/15 | -1.36 | 16 | +4.65 | +0.85 | 2.2 | +0.27 | – | 0.82 |
| 27 | `M23` Breitstein Kapitulasi + Kesina | **50.5** | 44 | 50 | 54 | 77 | BELUM CUKUP | 16 | 107/65 | -1.22 | 16 | -1.58 | -0.31 | 2.1 | +0.34 | – | 1.62 |
| 28 | `M104` High Tight Flag / Power Play | **50.4** | 79 | 80 | 27 | 50 | BELUM CUKUP | 1 | 1/0 | +10.02 | 1 | +1.02 | +10.00 | – | – | – | – |
| 29 | `M30` BB Free Bar + Himpitan 50/2.5 | **50.4** | 52 | 44 | 56 | 56 | BELUM CUKUP | 16 | 212/57 | -0.51 | 16 | +0.10 | +0.01 | 4.6 | +0.54 | – | 1.17 |
| 30 | `M92` CCI-50 | **50.2** | 50 | 49 | 50 | 55 | BELUM CUKUP | 16 | 458/264 | -0.54 | 16 | -0.98 | -0.17 | 2.1 | -0.29 | – | -0.69 |
| 31 | `M70` Pecahan Hari Dalam | **50.0** | 59 | 60 | 52 | 15 | BELUM CUKUP | 16 | 352/289 | -0.50 | 16 | +0.50 | +0.10 | 2.4 | -0.14 | – | -0.46 |
| 32 | `N68X16` Bullish engulfing + EMA21 → ke | **49.9** | 47 | 66 | 38 | 50 | BELUM CUKUP | 3 | 15/5 | -0.58 | 3 | +1.05 | +0.51 | 1.5 | +0.26 | – | – |
| 33 | `N68X36` Bullish engulfing + EMA21 → ke | **49.8** | 50 | 58 | 38 | 50 | BELUM CUKUP | 3 | 14/3 | -0.42 | 3 | -0.12 | -0.05 | 1.7 | +0.45 | – | – |
| 34 | `N45X16` Undur EMA21 cerun positif → ke | **49.6** | 37 | 75 | 36 | 50 | BELUM CUKUP | 3 | 61/23 | -1.64 | 3 | +3.61 | +10.00 | 0.0 | -0.52 | – | – |
| 35 | `M02` MACD + SMA200 | **49.4** | 40 | 65 | 44 | 55 | BELUM CUKUP | 16 | 102/52 | -1.92 | 16 | +7.73 | +1.75 | 1.7 | -0.78 | – | -4.61 |
| 36 | `M159` Heikin-Ashi Trend | **49.4** | 54 | 58 | 46 | 23 | BELUM CUKUP | 16 | 1396/1102 | -0.67 | 16 | +2.87 | +0.47 | 3.9 | -0.83 | – | -5.38 |
| 37 | `M07` Qullamaggie Breakout | **49.2** | 29 | 65 | 27 | 15 | BELUM CUKUP | 1 | 1/1 | -2.53 | 16 | -0.25 | -0.21 | 0.6 | -0.22 | – | -1.12 |
| 38 | `M37` Weinstein Peringkat 2 | **48.8** | 45 | 58 | 20 | 25 | BELUM CUKUP | 2 | 3/0 | -0.78 | 10 | -0.17 | -0.34 | 0.2 | -1.01 | – | -0.76 |
| 39 | `M27` Price Action 4 Tiang | **48.8** | 42 | 39 | 41 | 15 | BELUM CUKUP | 2 | 547/427 | -1.09 | 16 | -2.75 | -0.53 | 2.8 | -0.66 | – | -2.65 |
| 40 | `N39X36` NR7 kemudian pecah → keluar se | **48.8** | 21 | 22 | 27 | 50 | BELUM CUKUP | 1 | 16/0 | -5.64 | 2 | -3.62 | -1.00 | 3.2 | – | – | – |
| 41 | `M39` Radge Pecahan Bollinger 100 ha | **48.7** | 34 | 65 | 47 | 55 | BELUM CUKUP | 16 | 213/44 | -3.29 | 16 | +3.98 | +1.66 | 1.3 | -0.42 | – | -1.25 |
| 42 | `M51` O'Neil Cawan & Pemegang | **48.7** | 27 | 48 | 32 | 45 | BELUM CUKUP | 2 | 3/0 | -2.03 | 6 | -0.55 | -0.55 | 0.6 | +0.45 | – | 1.93 |
| 43 | `M05` MACD Divergence + Pengesahan | **48.6** | 41 | 58 | 39 | 55 | BELUM CUKUP | 13 | 38/12 | -1.57 | 16 | +1.29 | +0.38 | 1.4 | -0.77 | – | -1.27 |
| 44 | `M45` High 52 Minggu (George & Hwang | **48.6** | 25 | 35 | 9 | 15 | BELUM CUKUP | 1 | 2/1 | -7.63 | 5 | -1.50 | -0.83 | 1.1 | -2.31 | – | -5.78 |
| 45 | `M84` Jarak purata bergerak MAD 21/2 | **48.4** | 17 | 15 | 15 | 15 | BELUM CUKUP | 1 | 58/35 | -4.85 | 5 | -7.85 | -1.00 | 5.3 | -3.06 | – | -7.55 |
| 46 | `M134` First Kiss After Daylight (Lan | **48.3** | 45 | 41 | 49 | 55 | BELUM CUKUP | 13 | 38/16 | -0.79 | 16 | -2.29 | -0.33 | 2.6 | +0.33 | – | 0.51 |
| 47 | `M132` Ascending Scallop (Bulkowski) | **48.2** | 34 | 58 | 48 | 55 | BELUM CUKUP | 15 | 88/32 | -2.32 | 16 | +2.20 | +0.59 | 2.1 | -0.11 | – | -1.09 |
| 48 | `M88` O'Neil Shakeout +3 | **48.2** | 37 | 54 | 45 | 55 | BELUM CUKUP | 13 | 48/27 | -2.55 | 16 | +2.65 | +0.32 | 2.7 | -0.34 | – | -0.82 |
| 49 | `M96` Momo India: Ranking Sharpe 3/6 | **48.2** | 17 | 12 | 9 | 15 | BELUM CUKUP | 1 | 6/5 | -12.54 | 5 | -7.49 | -1.00 | 4.5 | -3.78 | – | -16.54 |
| 50 | `M131` Ross Hook (Joe Ross) | **48.0** | 42 | 46 | 53 | 39 | BELUM CUKUP | 16 | 241/102 | -1.12 | 16 | -1.81 | -0.28 | 2.5 | +0.04 | – | 0.12 |
| 51 | `M138` 直升机空中加油 (Helikopter isi minyak | **48.0** | 28 | 45 | 19 | 15 | BELUM CUKUP | 2 | 2/0 | -2.53 | 9 | -0.47 | -0.72 | 0.2 | -1.09 | – | -2.67 |
| 52 | `M94` Pecutan Momentum (Chen, Yu & W | **47.9** | 12 | 4 | 3 | 15 | BELUM CUKUP | 1 | 33/0 | -11.42 | 5 | -11.78 | -1.00 | 7.8 | -3.54 | – | -11.60 |
| 53 | `M139` 均线首次粘合向上发散 (MA berhimpun kali  | **47.7** | 34 | 56 | 46 | 55 | BELUM CUKUP | 16 | 65/16 | -1.70 | 16 | +2.96 | +0.59 | 1.7 | -0.05 | – | -0.19 |
| 54 | `N45X36` Undur EMA21 cerun positif → ke | **47.7** | 25 | 46 | 26 | 50 | BELUM CUKUP | 3 | 53/7 | -2.18 | 3 | -0.39 | -0.19 | 1.6 | -1.29 | – | – |
| 55 | `N53X36` Supertrend + ADX>25 → keluar s | **47.6** | 22 | 43 | 30 | 50 | BELUM CUKUP | 3 | 65/8 | -2.14 | 3 | -1.68 | -0.42 | 3.1 | -0.88 | – | – |
| 56 | `M78` Alvarez Pecahan Mingguan DTAYS | **47.6** | 18 | 25 | 40 | 15 | BELUM CUKUP | 2 | 73/38 | -2.41 | 15 | -7.87 | -0.76 | 5.5 | -0.14 | – | -0.65 |
| 57 | `N66X36` 52w tinggi + pengesahan 1% → k | **47.6** | 14 | 28 | 28 | 50 | BELUM CUKUP | 2 | 27/0 | -2.81 | 2 | -4.15 | -1.00 | 4.0 | – | – | – |
| 58 | `N53X16` Supertrend + ADX>25 → keluar b | **47.5** | 23 | 46 | 26 | 50 | BELUM CUKUP | 3 | 58/1 | -1.96 | 3 | -1.30 | -0.35 | 3.0 | -0.69 | – | – |
| 59 | `N36X16` Pocket pivot → keluar bila sup | **47.5** | 21 | 67 | 17 | 50 | BELUM CUKUP | 3 | 98/31 | -3.08 | 3 | +0.74 | +1.07 | 0.5 | -6.14 | – | – |
| 60 | `M117` Landry Pullback (high 2 bulan) | **47.4** | 53 | 36 | 50 | 28 | BELUM CUKUP | 14 | 81/17 | -0.00 | 16 | -5.90 | -0.75 | 3.0 | +0.38 | – | 0.45 |
| 61 | `N22X36` BB pecah atas + RSI → keluar s | **47.4** | 20 | 38 | 35 | 50 | BELUM CUKUP | 3 | 62/5 | -2.74 | 3 | -2.12 | -0.56 | 2.9 | -0.10 | – | – |
| 62 | `N53X17` Supertrend + ADX>25 → keluar b | **47.4** | 23 | 44 | 23 | 50 | BELUM CUKUP | 3 | 54/0 | -1.99 | 3 | -1.55 | -0.41 | 3.1 | -0.70 | – | – |
| 63 | `N22X16` BB pecah atas + RSI → keluar b | **47.4** | 19 | 38 | 35 | 50 | BELUM CUKUP | 3 | 59/14 | -2.59 | 3 | -2.40 | -0.67 | 2.7 | -0.47 | – | – |
| 64 | `M148` Natural Number Method | **47.2** | 33 | 58 | 42 | 55 | BELUM CUKUP | 16 | 176/114 | -2.22 | 16 | +1.86 | +0.37 | 1.7 | -1.24 | – | -5.56 |
| 65 | `M41` FW Penyatuan Mingguan | **47.2** | 23 | 26 | 39 | 37 | BELUM CUKUP | 3 | 33/6 | -1.73 | 15 | -5.79 | -0.70 | 3.6 | +0.32 | – | 0.74 |
| 66 | `N41X16` CMF20>0 + tutup>EMA20 → keluar | **47.2** | 23 | 43 | 20 | 50 | BELUM CUKUP | 3 | 112/57 | -2.68 | 3 | -0.74 | -0.35 | 1.6 | -5.44 | – | – |
| 67 | `N07X16` Tiga MA tersusun → keluar bila | **47.1** | 20 | 38 | 24 | 50 | BELUM CUKUP | 3 | 56/5 | -2.19 | 3 | -2.58 | -0.64 | 2.6 | -1.37 | – | – |
| 68 | `N50X17` Mampat + pecah volum 1.5x → ke | **47.1** | 18 | 23 | 8 | 50 | BELUM CUKUP | 2 | 11/1 | -6.09 | 3 | -6.14 | -0.67 | 6.5 | -2.59 | – | – |
| 69 | `N40X36` OBV tinggi baharu + MA50 → kel | **47.0** | 21 | 34 | 22 | 50 | BELUM CUKUP | 3 | 23/3 | -2.67 | 3 | -3.76 | -0.78 | 3.7 | -1.46 | – | – |
| 70 | `N50X14` Mampat + pecah volum 1.5x → ke | **47.0** | 18 | 23 | 7 | 50 | BELUM CUKUP | 2 | 11/0 | -5.94 | 3 | -5.95 | -0.65 | 6.4 | -2.47 | – | – |
| 71 | `M115` Bow Tie (Landry) | **46.9** | 31 | 42 | 46 | 50 | BELUM CUKUP | 8 | 31/18 | -2.29 | 16 | -4.22 | -0.54 | 2.7 | +0.13 | – | 0.98 |
| 72 | `N40X16` OBV tinggi baharu + MA50 → kel | **46.9** | 22 | 33 | 20 | 50 | BELUM CUKUP | 3 | 30/13 | -2.56 | 3 | -4.26 | -0.80 | 3.9 | -2.14 | – | – |
| 73 | `N75X17` RSI14 < 40 tanpa penapis → kel | **46.9** | 24 | 34 | 18 | 50 | BELUM CUKUP | 3 | 193/32 | -1.56 | 3 | -3.99 | -1.00 | 3.0 | -4.61 | – | – |
| 74 | `N07X36` Tiga MA tersusun → keluar sele | **46.9** | 20 | 36 | 21 | 50 | BELUM CUKUP | 3 | 58/2 | -2.36 | 3 | -2.54 | -0.64 | 2.5 | -1.45 | – | – |
| 75 | `N57X16` ADX bangkit daripada <20 → kel | **46.9** | 20 | 39 | 19 | 50 | BELUM CUKUP | 3 | 37/2 | -3.66 | 3 | -1.01 | -0.30 | 2.5 | -1.70 | – | – |
| 76 | `N08X16` tutup>EMA20 tidak terlalu jauh | **46.7** | 19 | 32 | 21 | 50 | BELUM CUKUP | 3 | 161/86 | -2.47 | 3 | -2.50 | -0.80 | 2.9 | -5.76 | – | – |
| 77 | `N57X36` ADX bangkit daripada <20 → kel | **46.7** | 20 | 39 | 15 | 50 | BELUM CUKUP | 3 | 39/0 | -3.64 | 3 | -1.01 | -0.30 | 2.5 | -1.65 | – | – |
| 78 | `N76X16` Tutup > MA50 (penapis trend tu | **46.7** | 19 | 34 | 19 | 50 | BELUM CUKUP | 3 | 103/47 | -2.98 | 3 | -2.19 | -0.63 | 2.6 | -5.12 | – | – |
| 79 | `N51X16` BB squeeze + Supertrend → kelu | **46.7** | 17 | 37 | 18 | 50 | BELUM CUKUP | 3 | 4/1 | -3.94 | 3 | -1.52 | -0.59 | 1.9 | -1.55 | – | – |
| 80 | `M38` Darvas Kotak | **46.7** | 16 | 29 | 32 | 35 | BELUM CUKUP | 3 | 15/1 | -6.14 | 15 | -4.29 | -0.43 | 3.3 | -0.02 | – | -0.13 |
| 81 | `N08X36` tutup>EMA20 tidak terlalu jauh | **46.7** | 18 | 33 | 20 | 50 | BELUM CUKUP | 3 | 141/60 | -2.82 | 3 | -3.27 | -0.60 | 4.1 | -6.45 | – | – |
| 82 | `N41X36` CMF20>0 + tutup>EMA20 → keluar | **46.7** | 20 | 31 | 18 | 50 | BELUM CUKUP | 3 | 94/42 | -3.11 | 3 | -3.10 | -0.63 | 3.6 | -4.86 | – | – |
| 83 | `N47X36` NR7 + EMA9>EMA21 → keluar sele | **46.7** | 10 | 23 | 8 | 50 | BELUM CUKUP | 2 | 21/2 | -6.32 | 3 | -6.92 | -1.00 | 5.4 | -4.02 | – | – |
| 84 | `M46` Jurang Naik Boleh Beli (Buyabl | **46.6** | 33 | 52 | 43 | 30 | BELUM CUKUP | 10 | 33/16 | -1.73 | 16 | -1.08 | -0.22 | 1.7 | -0.30 | – | -0.51 |
| 85 | `M64` O'Neil Tiga Minggu Ketat | **46.6** | 25 | 25 | 27 | 15 | BELUM CUKUP | 3 | 3/1 | -10.28 | 16 | -3.03 | -0.80 | 1.8 | -0.78 | – | -11.82 |
| 86 | `N64X17` Episodic pivot → keluar bila a | **46.6** | 22 | 38 | 12 | 50 | BELUM CUKUP | 3 | 36/5 | -1.89 | 3 | -3.30 | -0.82 | 3.0 | -3.62 | – | – |
| 87 | `N124X15` Episodic pivot gap 8-10% → eko | **46.5** | 22 | 35 | 11 | 50 | BELUM CUKUP | 3 | 28/0 | -2.01 | 3 | -4.32 | -0.65 | 4.6 | -2.13 | – | – |
| 88 | `N124X36` Episodic pivot gap 8-10% → kel | **46.5** | 22 | 31 | 12 | 50 | BELUM CUKUP | 3 | 28/5 | -2.19 | 3 | -4.94 | -1.00 | 3.9 | -2.69 | – | – |
| 89 | `N25X36` Supertrend + EMA + ADX>23 → ke | **46.5** | 16 | 34 | 18 | 50 | BELUM CUKUP | 3 | 60/8 | -2.57 | 3 | -3.79 | -0.85 | 3.6 | -2.25 | – | – |
| 90 | `N51X36` BB squeeze + Supertrend → kelu | **46.5** | 17 | 35 | 15 | 50 | BELUM CUKUP | 3 | 4/0 | -4.20 | 3 | -1.61 | -0.63 | 1.9 | -1.65 | – | – |
| 91 | `N28X16` ADX>25 + DI+ > DI- → keluar bi | **46.4** | 18 | 29 | 18 | 50 | BELUM CUKUP | 3 | 118/35 | -1.84 | 3 | -5.06 | -0.81 | 4.9 | -5.28 | – | – |
| 92 | `N64X16` Episodic pivot → keluar bila s | **46.4** | 22 | 39 | 9 | 50 | BELUM CUKUP | 3 | 36/2 | -2.00 | 3 | -3.10 | -0.77 | 2.9 | -3.87 | – | – |
| 93 | `N22X14` BB pecah atas + RSI → keluar b | **46.4** | 17 | 29 | 17 | 50 | BELUM CUKUP | 3 | 64/0 | -3.08 | 3 | -3.82 | -0.84 | 3.5 | -1.48 | – | – |
| 94 | `N74X16` MACD atas garis isyarat (keada | **46.4** | 17 | 25 | 21 | 50 | BELUM CUKUP | 3 | 170/80 | -1.66 | 3 | -6.88 | -0.94 | 6.3 | -2.92 | – | – |
| 95 | `N64X36` Episodic pivot → keluar selepa | **46.4** | 22 | 36 | 9 | 50 | BELUM CUKUP | 3 | 36/2 | -2.17 | 3 | -3.59 | -0.90 | 3.1 | -4.29 | – | – |
| 96 | `N36X36` Pocket pivot → keluar selepas  | **46.4** | 17 | 30 | 16 | 50 | BELUM CUKUP | 3 | 98/19 | -3.37 | 3 | -2.73 | -0.52 | 3.6 | -6.20 | – | – |
| 97 | `N27X16` Ichimoku atas awan → keluar bi | **46.3** | 16 | 33 | 15 | 50 | BELUM CUKUP | 3 | 67/15 | -3.30 | 3 | -2.46 | -0.84 | 2.3 | -7.89 | – | – |
| 98 | `N80X36` Tinggi sepanjang masa → keluar | **46.3** | 22 | 32 | 10 | 50 | BELUM CUKUP | 3 | 23/0 | -1.84 | 3 | -3.17 | -0.92 | 2.4 | -2.23 | – | – |
| 99 | `N25X16` Supertrend + EMA + ADX>23 → ke | **46.3** | 16 | 35 | 13 | 50 | BELUM CUKUP | 3 | 57/1 | -2.52 | 3 | -3.75 | -0.78 | 3.8 | -2.19 | – | – |
| 100 | `M153` Range Leader | **46.2** | 49 | 40 | 52 | 15 | BELUM CUKUP | 16 | 1040/855 | -0.35 | 16 | -3.63 | -0.37 | 5.8 | -0.12 | – | -0.90 |
| 101 | `M35` Pocket Pivot Morales & Kacher | **46.2** | 50 | 39 | 52 | 15 | BELUM CUKUP | 16 | 281/191 | -0.59 | 16 | -4.96 | -0.54 | 4.8 | -0.10 | – | -0.67 |
| 102 | `N37X17` Gap and go → keluar bila adx14 | **46.2** | 17 | 28 | 14 | 50 | BELUM CUKUP | 3 | 57/12 | -3.27 | 3 | -2.67 | -0.72 | 2.6 | -9.27 | – | – |
| 103 | `N76X36` Tutup > MA50 (penapis trend tu | **46.2** | 18 | 28 | 13 | 50 | BELUM CUKUP | 3 | 63/8 | -2.99 | 3 | -4.65 | -0.85 | 4.4 | -4.31 | – | – |
| 104 | `N56X16` RSI>50 + ADX>20 → keluar bila  | **46.2** | 17 | 25 | 16 | 50 | BELUM CUKUP | 3 | 80/23 | -1.90 | 3 | -5.10 | -1.00 | 4.4 | -4.11 | – | – |
| 105 | `N25X17` Supertrend + EMA + ADX>23 → ke | **46.2** | 16 | 35 | 11 | 50 | BELUM CUKUP | 3 | 55/0 | -2.37 | 3 | -3.76 | -0.78 | 3.8 | -2.11 | – | – |
| 106 | `N28X36` ADX>25 + DI+ > DI- → keluar se | **46.2** | 14 | 27 | 18 | 50 | BELUM CUKUP | 3 | 114/32 | -1.96 | 3 | -5.32 | -0.85 | 5.0 | -5.12 | – | – |
| 107 | `N24X36` Supertrend(10,3) + ADX>20 → ke | **46.2** | 17 | 25 | 15 | 50 | BELUM CUKUP | 3 | 66/15 | -3.27 | 3 | -4.14 | -0.91 | 3.6 | -4.14 | – | – |
| 108 | `N09X36` Undur EMA10 + penapis EMA50 →  | **46.1** | 15 | 29 | 15 | 50 | BELUM CUKUP | 3 | 72/14 | -4.31 | 3 | -3.31 | -0.85 | 3.0 | -4.92 | – | – |
| 109 | `M121` High 2 bull flag (Brooks) | **46.1** | 20 | 19 | 24 | 15 | BELUM CUKUP | 3 | 5/3 | -11.65 | 12 | -5.79 | -0.79 | 3.1 | -1.20 | – | -24.49 |
| 110 | `N19X13` Bawah jalur BB + RSI<30 → kelu | **46.1** | 23 | 37 | 5 | 50 | BELUM CUKUP | 3 | 87/0 | -1.62 | 3 | -2.91 | -0.88 | 2.6 | -4.95 | – | – |
| 111 | `N33X16` Donchian20 + penapis MA200 → k | **46.1** | 15 | 36 | 10 | 50 | BELUM CUKUP | 3 | 46/3 | -3.02 | 3 | -2.89 | -0.82 | 2.6 | -4.14 | – | – |
| 112 | `N37X16` Gap and go → keluar bila super | **46.1** | 17 | 26 | 13 | 50 | BELUM CUKUP | 3 | 58/7 | -3.32 | 3 | -3.06 | -0.83 | 2.8 | -9.33 | – | – |
| 113 | `N24X16` Supertrend(10,3) + ADX>20 → ke | **46.1** | 19 | 30 | 9 | 50 | BELUM CUKUP | 3 | 50/2 | -2.37 | 3 | -2.96 | -0.87 | 2.6 | -3.25 | – | – |
| 114 | `N37X36` Gap and go → keluar selepas DU | **46.1** | 18 | 23 | 13 | 50 | BELUM CUKUP | 3 | 58/9 | -3.61 | 3 | -3.55 | -0.96 | 3.0 | -11.07 | – | – |
| 115 | `N42X16` Lonjakan volum 2x → keluar bil | **46.1** | 13 | 26 | 17 | 50 | BELUM CUKUP | 3 | 104/31 | -2.58 | 3 | -5.59 | -0.86 | 5.1 | -3.87 | – | – |
| 116 | `N64X14` Episodic pivot → keluar bila r | **46.1** | 22 | 39 | 5 | 50 | BELUM CUKUP | 3 | 36/0 | -1.91 | 3 | -3.10 | -0.77 | 2.9 | -3.63 | – | – |
| 117 | `M18` EMA9/21 Pullback | **46.0** | 55 | 33 | 53 | 15 | BELUM CUKUP | 16 | 271/202 | -0.12 | 16 | -6.02 | -1.00 | 4.2 | -0.04 | – | -0.18 |
| 118 | `M150` Trend Bar Failure (Brooks) | **46.0** | 49 | 42 | 46 | 15 | BELUM CUKUP | 15 | 79/33 | -0.39 | 16 | -4.24 | -0.76 | 2.1 | -0.41 | – | -1.75 |
| 119 | `N37X14` Gap and go → keluar bila rsi14 | **46.0** | 18 | 31 | 9 | 50 | BELUM CUKUP | 3 | 58/2 | -3.10 | 3 | -2.33 | -0.63 | 2.5 | -7.98 | – | – |
| 120 | `N24X17` Supertrend(10,3) + ADX>20 → ke | **46.0** | 18 | 33 | 8 | 50 | BELUM CUKUP | 3 | 58/1 | -2.30 | 3 | -2.87 | -0.77 | 2.8 | -2.78 | – | – |
| 121 | `N56X17` RSI>50 + ADX>20 → keluar bila  | **46.0** | 16 | 30 | 11 | 50 | BELUM CUKUP | 3 | 60/4 | -2.39 | 3 | -4.04 | -0.81 | 3.8 | -4.17 | – | – |
| 122 | `N47X16` NR7 + EMA9>EMA21 → keluar bila | **46.0** | 13 | 31 | 13 | 50 | BELUM CUKUP | 3 | 23/7 | -4.46 | 3 | -4.36 | -1.00 | 3.3 | -4.25 | – | – |
| 123 | `N42X36` Lonjakan volum 2x → keluar sel | **46.0** | 12 | 25 | 17 | 50 | BELUM CUKUP | 3 | 102/27 | -2.62 | 3 | -6.16 | -0.83 | 5.7 | -3.86 | – | – |
| 124 | `N48X36` Inside day pecah → keluar sele | **45.9** | 17 | 18 | 17 | 50 | BELUM CUKUP | 3 | 75/26 | -4.17 | 3 | -8.00 | -0.95 | 7.0 | -7.95 | – | – |
| 125 | `N35X36` Pecah 52 minggu tinggi → kelua | **45.9** | 18 | 36 | 5 | 50 | BELUM CUKUP | 3 | 30/0 | -2.43 | 3 | -1.27 | -0.71 | 1.4 | -2.86 | – | – |
| 126 | `M32` Momentum Burst | **45.8** | 47 | 28 | 49 | 24 | BELUM CUKUP | 11 | 51/32 | -0.77 | 16 | -5.06 | -0.46 | 6.1 | +0.10 | – | 0.31 |
| 127 | `N38X36` VCP pecah → keluar selepas DUA | **45.8** | 15 | 32 | 8 | 50 | BELUM CUKUP | 3 | 11/1 | -2.93 | 3 | -3.15 | -0.97 | 2.5 | -3.63 | – | – |
| 128 | `N113X36` 80-20 bar (sisi beli) → keluar | **45.8** | 16 | 14 | 18 | 50 | BELUM CUKUP | 3 | 74/43 | -4.38 | 3 | -6.52 | -0.95 | 6.1 | -4.70 | – | – |
| 129 | `N29X16` PSAR naik + tutup>MA50 → kelua | **45.8** | 10 | 22 | 18 | 50 | BELUM CUKUP | 3 | 86/38 | -3.96 | 3 | -6.42 | -0.87 | 5.9 | -5.07 | – | – |
| 130 | `M68` Kell Base n' Break | **45.7** | 28 | 43 | 43 | 55 | BELUM CUKUP | 11 | 40/10 | -3.52 | 16 | -0.64 | -0.14 | 1.5 | -0.14 | – | -1.31 |
| 131 | `M157` Consolidation Pivot Breakout ( | **45.7** | 19 | 35 | 27 | 15 | BELUM CUKUP | 4 | 4/3 | -5.75 | 13 | -2.28 | -0.78 | 0.9 | -0.91 | – | -4.55 |
| 132 | `N75X14` RSI14 < 40 tanpa penapis → kel | **45.7** | 14 | 32 | 8 | 50 | BELUM CUKUP | 3 | 153/1 | -2.03 | 3 | -4.93 | -0.90 | 4.5 | -4.70 | – | – |
| 133 | `N33X36` Donchian20 + penapis MA200 → k | **45.7** | 16 | 35 | 5 | 50 | BELUM CUKUP | 3 | 46/0 | -2.97 | 3 | -2.96 | -0.81 | 2.7 | -3.99 | – | – |
| 134 | `N65X14` Gap 4% + volum + hampir 52w →  | **45.7** | 17 | 33 | 5 | 50 | BELUM CUKUP | 3 | 24/0 | -2.63 | 3 | -4.17 | -1.00 | 3.4 | -4.02 | – | – |
| 135 | `N65X36` Gap 4% + volum + hampir 52w →  | **45.7** | 17 | 33 | 5 | 50 | BELUM CUKUP | 3 | 24/0 | -2.63 | 3 | -4.17 | -1.00 | 3.4 | -4.02 | – | – |
| 136 | `N28X14` ADX>25 + DI+ > DI- → keluar bi | **45.7** | 15 | 27 | 8 | 50 | BELUM CUKUP | 3 | 74/1 | -2.50 | 3 | -5.39 | -0.88 | 4.7 | -3.20 | – | – |
| 137 | `N33X14` Donchian20 + penapis MA200 → k | **45.7** | 15 | 34 | 5 | 50 | BELUM CUKUP | 3 | 53/0 | -3.23 | 3 | -3.31 | -0.80 | 3.2 | -2.85 | – | – |
| 138 | `N43X36` Undur EMA8 + penapis MA50 → ke | **45.7** | 14 | 22 | 10 | 50 | BELUM CUKUP | 3 | 60/3 | -4.83 | 3 | -3.90 | -1.00 | 3.0 | -4.13 | – | – |
| 139 | `N75X13` RSI14 < 40 tanpa penapis → kel | **45.7** | 16 | 33 | 5 | 50 | BELUM CUKUP | 3 | 100/0 | -2.18 | 3 | -3.73 | -1.00 | 2.9 | -4.43 | – | – |
| 140 | `N75X15` RSI14 < 40 tanpa penapis → eko | **45.7** | 16 | 33 | 5 | 50 | BELUM CUKUP | 3 | 100/0 | -2.18 | 3 | -3.73 | -1.00 | 2.9 | -4.43 | – | – |
| 141 | `N31X36` Turtle sistem 2 → keluar selep | **45.7** | 18 | 28 | 5 | 50 | BELUM CUKUP | 3 | 65/0 | -3.83 | 3 | -3.53 | -0.97 | 2.9 | -5.00 | – | – |
| 142 | `N42X17` Lonjakan volum 2x → keluar bil | **45.7** | 10 | 22 | 17 | 50 | BELUM CUKUP | 3 | 108/24 | -2.88 | 3 | -7.80 | -0.80 | 7.3 | -3.74 | – | – |
| 143 | `N56X36` RSI>50 + ADX>20 → keluar selep | **45.7** | 11 | 19 | 16 | 50 | BELUM CUKUP | 3 | 74/20 | -3.04 | 3 | -6.79 | -0.93 | 6.1 | -7.27 | – | – |
| 144 | `N54X16` Supertrend + RSI>50 → keluar b | **45.6** | 12 | 24 | 10 | 50 | BELUM CUKUP | 3 | 57/3 | -2.38 | 3 | -5.43 | -0.68 | 5.9 | -3.11 | – | – |
| 145 | `N27X36` Ichimoku atas awan → keluar se | **45.6** | 13 | 24 | 9 | 50 | BELUM CUKUP | 3 | 50/2 | -3.96 | 3 | -4.37 | -1.00 | 3.4 | -6.86 | – | – |
| 146 | `N113X16` 80-20 bar (sisi beli) → keluar | **45.6** | 14 | 12 | 19 | 50 | BELUM CUKUP | 3 | 72/47 | -5.07 | 3 | -6.80 | -0.97 | 6.3 | -6.64 | – | – |
| 147 | `N06X36` Golden cross MA50/MA200 → kelu | **45.6** | 15 | 29 | 5 | 50 | BELUM CUKUP | 3 | 8/0 | -4.44 | 3 | -3.40 | -0.83 | 3.1 | -3.83 | – | – |
| 148 | `N55X13` BB + RSI + ADX>20 → keluar bil | **45.5** | 13 | 31 | 5 | 50 | BELUM CUKUP | 3 | 32/0 | -2.29 | 3 | -4.51 | -0.98 | 3.7 | -3.36 | – | – |
| 149 | `N36X14` Pocket pivot → keluar bila rsi | **45.5** | 12 | 21 | 9 | 50 | BELUM CUKUP | 3 | 96/2 | -3.84 | 3 | -5.14 | -0.76 | 4.9 | -5.09 | – | – |
| 150 | `N54X36` Supertrend + RSI>50 → keluar s | **45.4** | 9 | 17 | 15 | 50 | BELUM CUKUP | 3 | 74/14 | -3.27 | 3 | -7.60 | -0.94 | 6.6 | -5.13 | – | – |
| 151 | `N73X13` Tutup bawah jalur bawah BB(20, | **45.4** | 12 | 31 | 5 | 50 | BELUM CUKUP | 3 | 114/0 | -2.36 | 3 | -5.45 | -0.86 | 4.0 | -3.68 | – | – |
| 152 | `N28X17` ADX>25 + DI+ > DI- → keluar bi | **45.4** | 14 | 24 | 5 | 50 | BELUM CUKUP | 3 | 50/0 | -2.56 | 3 | -6.13 | -0.85 | 5.5 | -3.62 | – | – |
| 153 | `M04` BB Squeeze Breakout | **45.3** | 30 | 39 | 52 | 48 | BELUM CUKUP | 15 | 138/38 | -1.83 | 16 | -0.46 | -0.06 | 4.0 | +0.25 | – | 0.52 |
| 154 | `M107` Golden Cross SMA50/200 | **45.3** | 35 | 49 | 42 | 21 | BELUM CUKUP | 14 | 28/7 | -1.35 | 16 | -0.40 | -0.11 | 1.5 | -0.16 | – | -0.32 |
| 155 | `M143` 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke | **45.3** | 31 | 46 | 27 | 29 | BELUM CUKUP | 8 | 11/1 | -1.23 | 15 | -1.16 | -0.39 | 1.6 | -0.94 | – | -11.52 |
| 156 | `N29X36` PSAR naik + tutup>MA50 → kelua | **45.3** | 8 | 20 | 12 | 50 | BELUM CUKUP | 3 | 68/6 | -3.58 | 3 | -8.44 | -0.87 | 7.5 | -4.63 | – | – |
| 157 | `N119X13` 3 tutup turun berturut → kelua | **45.3** | 8 | 18 | 12 | 50 | BELUM CUKUP | 3 | 36/5 | -4.79 | 3 | -7.86 | -0.95 | 7.2 | -4.45 | – | – |
| 158 | `N119X15` 3 tutup turun berturut → ekori | **45.2** | 10 | 24 | 5 | 50 | BELUM CUKUP | 3 | 14/0 | -4.84 | 3 | -6.59 | -0.97 | 5.6 | -4.91 | – | – |
| 159 | `M116` 2/20 EMA Breakout (Landry) | **45.1** | 44 | 36 | 52 | 15 | BELUM CUKUP | 16 | 508/318 | -0.52 | 16 | -3.87 | -0.31 | 6.4 | -0.06 | – | -0.32 |
| 160 | `M87` IBD Tapak Menaik | **45.1** | 31 | 33 | 38 | 15 | BELUM CUKUP | 7 | 10/6 | -3.32 | 16 | -3.30 | -0.57 | 3.1 | -0.30 | – | -1.24 |
| 161 | `M144` Screw Bar | **45.1** | 24 | 32 | 26 | 15 | BELUM CUKUP | 5 | 8/6 | -2.88 | 14 | -2.25 | -0.86 | 1.0 | -1.33 | – | -4.71 |
| 162 | `N42X14` Lonjakan volum 2x → keluar bil | **45.1** | 10 | 22 | 5 | 50 | BELUM CUKUP | 3 | 100/0 | -2.62 | 3 | -7.96 | -0.72 | 8.0 | -3.13 | – | – |
| 163 | `N16X13` RSI2<10 tanpa penapis → keluar | **45.1** | 7 | 19 | 10 | 50 | BELUM CUKUP | 3 | 90/3 | -3.24 | 3 | -9.00 | -1.00 | 6.5 | -6.63 | – | – |
| 164 | `N42X15` Lonjakan volum 2x → ekori Chan | **45.1** | 10 | 21 | 5 | 50 | BELUM CUKUP | 3 | 96/0 | -2.69 | 3 | -8.04 | -0.70 | 8.2 | -3.18 | – | – |
| 165 | `M106` DMI Wilder | **44.8** | 44 | 34 | 49 | 15 | BELUM CUKUP | 14 | 99/49 | -0.69 | 16 | -3.49 | -0.77 | 2.4 | -0.10 | – | -0.22 |
| 166 | `M152` Spike & Ledge | **44.7** | 24 | 48 | 40 | 55 | BELUM CUKUP | 13 | 39/6 | -2.91 | 16 | +0.67 | +0.16 | 2.1 | -0.41 | – | -1.65 |
| 167 | `M77` Undercut & Rally pada Purata B | **44.6** | 29 | 44 | 37 | 55 | BELUM CUKUP | 14 | 44/32 | -2.12 | 16 | -1.60 | -0.51 | 1.7 | -1.40 | – | -2.04 |
| 168 | `N16X15` RSI2<10 tanpa penapis → ekori  | **44.4** | 3 | 15 | 5 | 50 | BELUM CUKUP | 3 | 88/0 | -3.64 | 3 | -11.69 | -1.00 | 7.8 | -8.19 | – | – |
| 169 | `M127` Slingshot Bullish | **44.2** | 32 | 47 | 43 | 15 | BELUM CUKUP | 14 | 91/68 | -1.95 | 16 | -2.51 | -0.37 | 3.0 | -1.00 | – | -1.79 |
| 170 | `M34` Carter TTM Squeeze | **44.1** | 29 | 37 | 46 | 50 | BELUM CUKUP | 16 | 94/44 | -2.18 | 16 | -1.12 | -0.16 | 3.0 | -0.47 | – | -2.05 |
| 171 | `M06` Minervini VCP Breakout | **44.1** | 26 | 46 | 44 | 36 | BELUM CUKUP | 16 | 70/31 | -2.51 | 16 | -2.30 | -0.36 | 2.2 | -0.57 | – | -2.09 |
| 172 | `M08` SMA20 + SMA200 | **44.0** | 36 | 28 | 48 | 32 | BELUM CUKUP | 14 | 128/84 | -1.32 | 16 | -4.80 | -0.90 | 4.0 | -0.43 | – | -1.51 |
| 173 | `M14` Walking with the Whales | **43.8** | 42 | 32 | 48 | 15 | BELUM CUKUP | 16 | 774/536 | -0.79 | 16 | -7.95 | -0.75 | 5.2 | -0.61 | – | -1.38 |
| 174 | `M49` Ichimoku (Tutup Atas Awan + Te | **43.7** | 30 | 42 | 46 | 24 | BELUM CUKUP | 16 | 241/134 | -2.03 | 16 | -2.07 | -0.31 | 2.9 | -0.76 | – | -1.59 |
| 175 | `M03` BB Break + Divergence RSI | **43.7** | 34 | 41 | 46 | 15 | BELUM CUKUP | 16 | 323/281 | -1.01 | 16 | -2.50 | -0.40 | 2.7 | -0.81 | – | -2.78 |
| 176 | `M102` Stockbee SLTB | **43.6** | 36 | 36 | 48 | 15 | BELUM CUKUP | 16 | 313/236 | -1.57 | 16 | -5.10 | -0.47 | 5.0 | -0.54 | – | -2.03 |
| 177 | `M130` 多方炮 (dua lilin hijau mengapit  | **43.6** | 17 | 24 | 34 | 15 | BELUM CUKUP | 6 | 9/3 | -3.73 | 14 | -3.15 | -0.58 | 2.4 | -0.22 | – | -0.25 |
| 178 | `M20` EMA10/15 Crossover + Sudut | **43.5** | 33 | 37 | 41 | 26 | BELUM CUKUP | 16 | 369/316 | -1.57 | 16 | -3.73 | -0.64 | 2.6 | -1.39 | – | -10.80 |
| 179 | `M99` Three Line Break | **43.5** | 32 | 37 | 47 | 22 | BELUM CUKUP | 16 | 129/84 | -3.19 | 16 | -0.90 | -0.15 | 3.1 | -0.58 | – | -3.17 |
| 180 | `M155` Market Cycle Strategy | **43.3** | 38 | 33 | 47 | 15 | BELUM CUKUP | 16 | 591/211 | -1.19 | 16 | -3.00 | -0.50 | 3.2 | -0.72 | – | -1.35 |
| 181 | `M141` First Thrust (Landry) | **43.3** | 18 | 34 | 30 | 15 | BELUM CUKUP | 7 | 20/8 | -3.61 | 16 | -3.94 | -0.77 | 1.8 | -1.34 | – | -3.66 |
| 182 | `M136` Short/Intermediate-term Low (L | **43.1** | 31 | 40 | 48 | 15 | BELUM CUKUP | 16 | 625/236 | -1.79 | 16 | -2.02 | -0.43 | 2.3 | -0.54 | – | -0.36 |
| 183 | `M44` Tapak Rata IBD | **43.1** | 26 | 38 | 20 | 15 | BELUM CUKUP | 8 | 9/4 | -4.57 | 16 | -3.99 | -0.84 | 2.3 | -2.36 | – | -42.45 |
| 184 | `M54` IBD Power Trend | **43.0** | 29 | 39 | 48 | 15 | BELUM CUKUP | 15 | 193/100 | -1.93 | 16 | -1.90 | -0.18 | 5.3 | -0.51 | – | -1.56 |
| 185 | `M147` Improved Three-Bar Pullback | **43.0** | 28 | 46 | 35 | 18 | BELUM CUKUP | 14 | 95/27 | -3.15 | 16 | +1.83 | +0.22 | 4.0 | -1.49 | – | -1.27 |
| 186 | `M149` 3-Step Pullback | **43.0** | 31 | 30 | 51 | 19 | BELUM CUKUP | 14 | 150/50 | -1.39 | 16 | -5.90 | -0.55 | 4.6 | +0.13 | – | 0.14 |
| 187 | `M120` Reversal New Highs | **43.0** | 32 | 34 | 38 | 15 | BELUM CUKUP | 12 | 18/12 | -2.49 | 16 | -3.72 | -0.56 | 2.9 | -0.79 | – | -5.15 |
| 188 | `M31` Band Walk (BB 20/2) | **42.8** | 36 | 27 | 51 | 20 | BELUM CUKUP | 16 | 369/47 | -1.10 | 16 | -3.89 | -0.35 | 6.2 | +0.07 | – | 0.17 |
| 189 | `M19` Sneaky Pivot (proksi harian) | **42.6** | 24 | 37 | 41 | 41 | BELUM CUKUP | 15 | 265/215 | -4.35 | 16 | -2.02 | -0.27 | 2.9 | -1.36 | – | -22.43 |
| 190 | `M67` Rayner Teo: Ujian Ketiga pada  | **42.5** | 26 | 34 | 36 | 15 | BELUM CUKUP | 11 | 25/16 | -4.15 | 16 | -6.55 | -0.59 | 4.8 | -1.10 | – | -7.15 |
| 191 | `M140` 猎豹出击 (Serangan Cheetah) | **42.5** | 18 | 32 | 29 | 15 | BELUM CUKUP | 8 | 37/11 | -2.59 | 16 | -4.73 | -0.76 | 2.5 | -1.66 | – | -2.10 |
| 192 | `M36` Turtle 55/20 | **42.3** | 29 | 34 | 51 | 15 | BELUM CUKUP | 16 | 297/144 | -1.70 | 16 | -4.80 | -0.40 | 6.1 | -0.20 | – | -0.64 |
| 193 | `M135` 3rd Watch | **42.2** | 12 | 28 | 30 | 15 | BELUM CUKUP | 7 | 12/2 | -6.23 | 16 | -7.22 | -0.91 | 2.7 | -0.95 | – | -7.18 |
| 194 | `M125` 2-Bar Breakout | **41.8** | 26 | 36 | 46 | 15 | BELUM CUKUP | 16 | 872/400 | -2.09 | 16 | -2.34 | -0.37 | 2.4 | -0.77 | – | -0.49 |
| 195 | `M128` Inventory Retracement Bar (IRB | **41.7** | 32 | 27 | 49 | 15 | BELUM CUKUP | 16 | 126/70 | -1.33 | 16 | -6.97 | -0.63 | 5.6 | -0.28 | – | -1.92 |
| 196 | `M12` Parabolic SAR | **41.4** | 25 | 33 | 48 | 15 | BELUM CUKUP | 16 | 325/164 | -2.35 | 16 | -3.54 | -0.61 | 3.0 | -0.54 | – | -1.75 |
| 197 | `M156` Single Penetration (DiNapoli) | **41.4** | 20 | 31 | 46 | 48 | BELUM CUKUP | 16 | 196/115 | -2.09 | 16 | -6.85 | -0.53 | 5.0 | -0.88 | – | -4.39 |
| 198 | `M26` Garis Trend Undur 3 Sentuhan + | **41.4** | 24 | 31 | 42 | 15 | BELUM CUKUP | 13 | 54/39 | -1.44 | 16 | -6.78 | -0.84 | 3.0 | -0.89 | – | -1.86 |
| 199 | `M126` Hidden Smash Day (beli, Larry  | **41.2** | 16 | 32 | 33 | 15 | BELUM CUKUP | 10 | 18/11 | -4.64 | 15 | -5.36 | -0.74 | 3.1 | -1.07 | – | -2.62 |
| 200 | `M50` Elder Triple Screen | **41.1** | 31 | 24 | 48 | 15 | BELUM CUKUP | 16 | 478/295 | -1.17 | 16 | -11.05 | -1.00 | 6.1 | -0.57 | – | -1.36 |
| 201 | `M55` Guppy GMMA | **40.5** | 26 | 27 | 47 | 15 | BELUM CUKUP | 16 | 177/110 | -2.64 | 16 | -7.08 | -0.81 | 4.2 | -0.72 | – | -2.90 |
| 202 | `M73` ADX(5) > 40 + Julat Terkecil 6 | **40.5** | 30 | 23 | 45 | 15 | BELUM CUKUP | 16 | 643/549 | -0.65 | 16 | -8.00 | -1.00 | 4.4 | -0.97 | – | -8.27 |
| 203 | `M66` IBD Undur Pertama ke Purata 50 | **40.3** | 24 | 27 | 47 | 15 | BELUM CUKUP | 16 | 193/125 | -2.08 | 16 | -7.24 | -0.63 | 5.6 | -0.68 | – | -2.52 |
| 204 | `M95` Nisbah Kebaharuan High 52 Ming | **40.3** | 20 | 33 | 44 | 15 | BELUM CUKUP | 15 | 110/60 | -2.85 | 16 | -5.90 | -0.70 | 3.7 | -0.77 | – | -2.80 |
| 205 | `M28` VWAP Separator + Kiss Pivot | **40.0** | 21 | 27 | 40 | 15 | BELUM CUKUP | 14 | 88/82 | -2.02 | 16 | -8.46 | -1.00 | 5.2 | -1.37 | – | -16.12 |
| 206 | `M29` EMA3 + RSI75 + Stokastik | **40.0** | 16 | 30 | 36 | 15 | BELUM CUKUP | 12 | 31/26 | -3.30 | 16 | -9.94 | -0.79 | 5.9 | -1.32 | – | -9.59 |
| 207 | `M57` Landry Trend Knockout (TKO) | **39.6** | 24 | 26 | 40 | 15 | BELUM CUKUP | 16 | 140/99 | -2.77 | 16 | -6.95 | -0.82 | 4.0 | -1.52 | – | -6.10 |
| 208 | `M119` 180 Bullish (Cooper) | **39.6** | 19 | 28 | 44 | 15 | BELUM CUKUP | 15 | 113/57 | -2.09 | 16 | -8.27 | -0.77 | 4.0 | -0.82 | – | -3.58 |
| 209 | `M11` NR7 Breakout + Volume | **39.3** | 19 | 27 | 40 | 15 | BELUM CUKUP | 15 | 95/68 | -1.70 | 16 | -8.64 | -0.72 | 5.3 | -1.30 | – | -1.96 |
| 210 | `M59` Anjakan Julat RSI | **39.2** | 16 | 24 | 41 | 15 | BELUM CUKUP | 13 | 35/15 | -5.66 | 16 | -4.78 | -0.60 | 2.7 | -0.61 | – | -3.35 |
| 211 | `M79` Radge: 20% Flipper | **39.1** | 18 | 30 | 41 | 15 | BELUM CUKUP | 16 | 254/71 | -3.60 | 16 | -5.48 | -0.60 | 3.9 | -1.25 | – | -2.86 |
| 212 | `M82` Arthur Hill Rotasi Sasaran 10% | **38.8** | 18 | 20 | 47 | 32 | BELUM CUKUP | 16 | 507/172 | -2.21 | 16 | -7.45 | -0.47 | 6.4 | -0.72 | – | -3.87 |
| 213 | `M101` Bulkowski: Tiga lembah menaik | **38.6** | 14 | 25 | 43 | 15 | BELUM CUKUP | 14 | 43/17 | -4.56 | 16 | -7.69 | -0.62 | 4.5 | -0.45 | – | -1.92 |
| 214 | `M47` Holy Grail Raschke | **38.4** | 9 | 18 | 27 | 15 | BELUM CUKUP | 10 | 21/18 | -4.70 | 16 | -9.71 | -0.98 | 4.5 | -2.16 | – | -27.83 |
| 215 | `M09` Volumatic VIDYA Pivot Retest | **38.3** | 6 | 12 | 29 | 15 | BELUM CUKUP | 9 | 23/14 | -5.47 | 16 | -11.73 | -1.00 | 6.4 | -1.76 | – | -14.83 |
| 216 | `M161` EMA 10/21 + Supertrend (10,3) | **38.0** | 23 | 14 | 49 | 15 | BELUM CUKUP | 16 | 393/168 | -1.28 | 16 | -12.39 | -0.89 | 8.2 | -0.44 | – | -1.35 |
| 217 | `M122` Moving Momentum (ChartSchool) | **37.2** | 17 | 22 | 33 | 15 | BELUM CUKUP | 16 | 92/56 | -3.86 | 16 | -8.57 | -1.00 | 4.7 | -2.11 | – | -7.38 |
| 218 | `M154` HOLP (High of Low Period) | **37.1** | 8 | 18 | 35 | 15 | BELUM CUKUP | 12 | 63/30 | -5.92 | 16 | -12.69 | -0.98 | 5.8 | -1.47 | – | -8.51 |
| 219 | `M01` Bollinger Band + RSI | **37.0** | 17 | 18 | 38 | 15 | BELUM CUKUP | 16 | 101/12 | -2.45 | 16 | -7.21 | -0.67 | 4.4 | -0.96 | – | -5.04 |
| 220 | `M123` CCI Correction (Lambert, Chart | **36.5** | 11 | 28 | 31 | 15 | BELUM CUKUP | 16 | 154/139 | -1.91 | 16 | -10.77 | -1.00 | 5.8 | -2.59 | – | -6.56 |
| 221 | `M76` Undercut & Rally pada Low Pent | **35.9** | 9 | 21 | 34 | 15 | BELUM CUKUP | 15 | 46/42 | -3.11 | 16 | -10.93 | -1.00 | 5.7 | -1.81 | – | -8.33 |
| 222 | `M81` Bensdorp Long Trend High Momen | **34.0** | 2 | 5 | 41 | 15 | BELUM CUKUP | 12 | 331/131 | -5.64 | 16 | -22.09 | -0.96 | 11.9 | -1.25 | – | -5.77 |
| 223 | `M90` Pring KST | **33.1** | 4 | 12 | 40 | 15 | BELUM CUKUP | 15 | 64/38 | -5.20 | 16 | -15.34 | -0.83 | 9.1 | -1.17 | – | -7.32 |

## Metrik dan sauh (0 · 50 · 100)

| Metrik | Berat | Apa | Sauh | Pakar |
|---|---|---|---|---|
| A1 | 20 | Jangkaan % setiap posisi, ditanda-ke-pasaran, kos ditolak | (-2.0, 0.0, 2.0) | Tharp, Minervini, Radge |
| A2 | 10 | Lebihan mata lorong T4 L1 (potongan LANGSUNG) lawan SPUS, tingkap sama | (-10.0, 0.0, 10.0) | Penanda aras SPUS (repo) |
| A3 | 5 | Payoff untung purata ÷ rugi purata | (0.5, 1.0, 2.0) | Minervini 2:1 |
| B1 | 12 | Pulangan ÷ |MDD| lorong T4 L1 (MAR) | (-1.0, 0.0, 1.0) | Schwager, Radge, Faith |
| B2 | 6 | Ulcer Index ekuiti T4 L1 (%) — kecil lebih baik | (10.0, 5.0, 0.0) | Martin |
| B3 | 6 | CVaR10: purata 10% posisi terburuk (%) | (-24.0, -16.0, -8.0) | Ekor kiri |
| B4 | 6 | tanpa5: jangkaan tanpa 5% posisi terbaik | (-2.0, 0.0, 2.0) | Davey (buang pemenang terbesar) |
| C1 | 12 | t Newey-West buku harian ÷ sauh t (≥ 2.0, dideflasi N ujian) | 0 → 50, sauh → 100 | Carver, Harvey-Liu, López de Prado |
| C2 | 8 | ½ log-skala hari beli (penuh 60) + ½ log-skala posisi ditutup (penuh 100) | – | Tharp 100 dagangan, Radge |
| C3 | 5 | min(hari beli ON, OFF) ÷ 10 | – | Clenow; rejim QQQ (repo) |
| D1 | 4 | K-ratio: t cerun log-ekuiti T4 ÷ √n | (-0.2, 0.0, 0.2) | Kestner |
| D2 | 3 | Lift masuk (lulus BH-FDR → 100/0; selain itu ±4 mata) | – | Plasebo gate (repo) |
| D3 | 3 | Kecekapan jalan-ke-depan: purata harian hadapan ÷ backtest | (0.0, 0.5, 1.0) | Pardo ≥ 50%, Davey |

Metrik tiada data = 50 (neutral). Kadar menang, median, rugi purata dan rugi terbesar sengaja TIDAK dimasukkan (pengiraan dua kali; pelajaran laporan KPI lama). Jangan ubah berat atau sauh selepas melihat data: dikunci oleh ujian unit dan memerlukan pradaftar bertarikh baharu.

