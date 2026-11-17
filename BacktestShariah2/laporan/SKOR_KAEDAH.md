# Skor Kaedah 0–100 (pangkat maklumat, BUKAN keputusan)

> **Status keputusan (kad skor, harga 2026-11-16):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana 2026-11-17 oleh `standard/skor_kaedah.py` (Actions `analisis.yml`, selepas kad skor). Harga pada tutup 2026-11-16; 226 kaedah; 22 hari beli langsung (rejim ON 1, OFF 21). Pradaftar 2026-11-09: `standard/SPEC_SKOR_KAEDAH.md` (berat dan sauh dikunci `ujian/test_skor_kaedah.py::TestKunci`). Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Cara membaca

- **Skor** = min geometri berberat empat tiang (Untung 35 · Tahan 30 · Bukti 25 · Konsisten 10), dikecut ke 50 mengikut data: berat data = hari beli ÷ (hari beli + 20). Kaedah dengan 2 hari beli tidak boleh menjauhi 50. 100 = unggul semua segi; 50 = neutral/tiada bukti; < 50 = lebih buruk daripada neutral.
- **Siling** ikut kad skor: NEGATIF ≤ 20, GANTUNG/BERSARA ≤ 30, GAGAL ≤ 40. Tanda ⌈ = siling terpakai.
- **Satu-satunya status yang membenarkan wang sebenar ialah TERBUKTI dalam `laporan/KAD_SKOR.md`.** Skor tinggi dengan status BELUM CUKUP bermaksud "paling menjanjikan setakat ini", bukan "selamat".
- Deflasi ujian berganda (López de Prado): sauh t Bukti C1 = maks(2.0, E[maks 226 normal]) = 2.81.
- **Semakan kebolehramalan:** skor pada 2026-11-09 lawan pulangan lorong T4 sejak itu, 223 kaedah: Spearman ρ = -0.103 (p = 0.127). Belum ada bukti skor meramal pangkat; jangan pilih kaedah dengannya.
- Metrik T4 (A2, B1, B2, D1) dikira atas lorong T4 L1 **dipotong pada sesi LANGSUNG pertama** kaedah itu (Mxx 2026-10-16, Nxx/GB 2026-11-03) dan diasas semula; sesi isian bina semula tidak dikira (pindaan 9 Nov 2026 (a)). Lajur "T4 sesi/pul" di bawah ialah potongan itu, bukan lorong penuh `T4_KAEDAH.md`.

## Semua kaedah, susun ikut Skor

| # | Kaedah | Skor | Untung | Tahan | Bukti | Konsisten | Status kad | Hari beli | Posisi/tutup | Jangkaan % | T4 sesi | T4 pul % | T4 pul/|MDD| | Ulcer | t buku | Lift | WFE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `M146` 3-Bar Momentum Pattern | **64.6** | 88 | 84 | 64 | 85 | BELUM CUKUP | 19 | 79/31 | +1.45 | 22 | +6.00 | +0.97 | 2.5 | +1.68 | – | 2.66 |
| 2 | `M151` Outside Bar Failure | **60.5** | 70 | 81 | 57 | 81 | BELUM CUKUP | 21 | 108/56 | -0.09 | 22 | +8.38 | +5.20 | 0.6 | +0.53 | – | 0.88 |
| 3 | `M133` Bull Hook (Crabel) | **60.0** | 74 | 81 | 58 | 85 | BELUM CUKUP | 16 | 55/28 | +0.32 | 22 | +5.76 | +1.39 | 1.5 | +1.14 | – | 10.18 |
| 4 | `M118` Expansion Pivot (Cooper) | **59.2** | 68 | 77 | 55 | 85 | BELUM CUKUP | 20 | 85/24 | -0.01 | 22 | +8.63 | +3.11 | 1.3 | +0.73 | – | 1.94 |
| 5 | `M25` VWAP Wave (proksi harian) | **57.6** | 64 | 71 | 58 | 71 | BELUM CUKUP | 20 | 187/105 | -0.26 | 22 | +4.57 | +0.79 | 3.2 | +0.54 | – | 2.85 |
| 6 | `M33` Supertrend + SMA10 | **57.1** | 60 | 70 | 56 | 85 | BELUM CUKUP | 21 | 221/47 | -0.32 | 22 | +9.14 | +3.42 | 1.4 | +0.54 | – | 2.28 |
| 7 | `M142` Pecahan volum dari dasar (底部放量 | **56.4** | 72 | 75 | 44 | 70 | BELUM CUKUP | 16 | 54/5 | +0.67 | 20 | +2.96 | +0.62 | 1.9 | +0.37 | – | 0.49 |
| 8 | `M74` Lulus Baharu Trend Template Mi | **56.3** | 64 | 66 | 54 | 63 | BELUM CUKUP | 22 | 100/60 | -0.41 | 22 | +2.53 | +0.54 | 2.5 | +0.18 | – | 0.28 |
| 9 | `M48` Cooper 1-2-3-4 | **56.1** | 69 | 58 | 54 | 85 | BELUM CUKUP | 18 | 60/19 | +0.04 | 22 | +7.68 | +1.41 | 2.1 | +0.75 | – | 1.66 |
| 10 | `M160` Measured Move Up | **55.7** | 53 | 66 | 61 | 85 | BELUM CUKUP | 20 | 117/56 | -0.82 | 22 | +2.29 | +0.49 | 2.1 | +1.05 | – | 7.19 |
| 11 | `M137` Livermore System | **55.0** | 55 | 66 | 55 | 69 | BELUM CUKUP | 22 | 176/68 | -0.76 | 22 | +4.87 | +0.82 | 2.2 | +0.29 | – | 0.47 |
| 12 | `M93` Bollinger Kaedah II: %b + MFI | **54.9** | 70 | 51 | 59 | 56 | BELUM CUKUP | 22 | 270/77 | +0.45 | 22 | +1.07 | +0.17 | 2.8 | +0.65 | – | 0.73 |
| 13 | `M100` Bulkowski Segi Empat & Segi Ti | **54.1** | 59 | 62 | 51 | 79 | BELUM CUKUP | 15 | 60/41 | -0.29 | 22 | +1.83 | +0.40 | 2.3 | +0.18 | – | 0.79 |
| 14 | `M145` Yum-Yum Continuation | **53.9** | 53 | 67 | 53 | 57 | BELUM CUKUP | 21 | 308/67 | -0.74 | 22 | +4.85 | +2.23 | 1.2 | +0.09 | – | 0.06 |
| 15 | `M159` Heikin-Ashi Trend | **53.8** | 57 | 68 | 47 | 55 | BELUM CUKUP | 22 | 1817/1574 | -0.65 | 22 | +5.72 | +0.93 | 3.5 | -0.80 | – | -3.80 |
| 16 | `M46` Jurang Naik Boleh Beli (Buyabl | **53.5** | 57 | 69 | 49 | 66 | BELUM CUKUP | 13 | 36/21 | -0.69 | 22 | +2.60 | +0.53 | 1.5 | +0.27 | – | 0.38 |
| 17 | `M23` Breitstein Kapitulasi + Kesina | **53.5** | 58 | 53 | 60 | 58 | BELUM CUKUP | 21 | 127/84 | -0.50 | 22 | -1.21 | -0.24 | 2.5 | +0.76 | – | 2.56 |
| 18 | `M77` Undercut & Rally pada Purata B | **53.3** | 61 | 64 | 47 | 55 | BELUM CUKUP | 17 | 54/35 | -0.35 | 22 | +0.89 | +0.28 | 1.6 | -0.36 | – | -0.46 |
| 19 | `M10` EMA3 + CCI + MACD | **53.2** | 50 | 67 | 53 | 59 | BELUM CUKUP | 21 | 126/60 | -1.28 | 22 | +9.89 | +1.88 | 2.1 | +0.05 | – | 0.13 |
| 20 | `M158` Doubly Adaptive Profit Targets | **53.1** | 66 | 46 | 61 | 45 | BELUM CUKUP | 22 | 377/134 | +0.37 | 22 | -1.58 | -0.26 | 3.3 | +0.78 | – | 1.70 |
| 21 | `M35` Pocket Pivot Morales & Kacher | **52.2** | 64 | 46 | 57 | 45 | BELUM CUKUP | 21 | 311/235 | +0.02 | 22 | -2.25 | -0.24 | 5.2 | +0.39 | – | 1.74 |
| 22 | `M70` Pecahan Hari Dalam | **52.2** | 63 | 67 | 54 | 17 | BELUM CUKUP | 22 | 494/393 | -0.42 | 22 | +1.96 | +0.41 | 2.2 | -0.05 | – | -0.10 |
| 23 | `M111` Sistem Volatiliti Wilder | **52.1** | 49 | 56 | 55 | 64 | BELUM CUKUP | 22 | 269/97 | -1.08 | 22 | +4.01 | +0.60 | 3.5 | +0.13 | – | 0.29 |
| 24 | `M124` 'Last' Stochastic Technique (C | **52.0** | 47 | 64 | 52 | 55 | BELUM CUKUP | 22 | 407/211 | -1.36 | 22 | +3.34 | +0.73 | 2.4 | -0.21 | – | -0.46 |
| 25 | `N45X16` Undur EMA21 cerun positif → ke | **51.8** | 48 | 74 | 45 | 70 | BELUM CUKUP | 9 | 159/68 | -1.05 | 9 | +5.21 | +2.91 | 0.9 | -0.31 | – | – |
| 26 | `N53X36` Supertrend + ADX>25 → keluar s | **51.7** | 64 | 51 | 50 | 57 | BELUM CUKUP | 9 | 130/33 | +0.04 | 9 | -0.14 | -0.03 | 2.2 | +0.51 | – | – |
| 27 | `M13` Garis Trend Action/Safety Line | **51.7** | 45 | 70 | 48 | 55 | BELUM CUKUP | 22 | 782/516 | -1.65 | 22 | +7.72 | +2.17 | 1.3 | -0.78 | – | -1.65 |
| 28 | `M104` High Tight Flag / Power Play | **51.1** | 82 | 90 | 45 | 85 | BELUM CUKUP | 1 | 1/0 | +20.90 | 7 | +2.11 | +10.00 | 0.0 | +2.14 | – | 16.34 |
| 29 | `M80` Radge Saluran Purata Bergerak  | **51.1** | 60 | 46 | 57 | 36 | BELUM CUKUP | 22 | 299/61 | +0.06 | 22 | -0.36 | -0.05 | 4.3 | +0.57 | – | 0.69 |
| 30 | `M132` Ascending Scallop (Bulkowski) | **51.0** | 41 | 66 | 50 | 68 | BELUM CUKUP | 17 | 94/38 | -1.65 | 22 | +4.05 | +1.08 | 2.2 | +0.06 | – | 0.42 |
| 31 | `M30` BB Free Bar + Himpitan 50/2.5 | **50.7** | 54 | 44 | 57 | 53 | BELUM CUKUP | 19 | 228/77 | -0.55 | 22 | +1.23 | +0.16 | 4.8 | +0.47 | – | 0.81 |
| 32 | `M129` Wick Play | **50.6** | 46 | 61 | 45 | 69 | BELUM CUKUP | 10 | 26/10 | -1.40 | 22 | +4.04 | +1.43 | 1.1 | +0.14 | – | 0.47 |
| 33 | `M91` Stochastic Pop (Bernstein/Stec | **50.5** | 42 | 55 | 50 | 85 | BELUM CUKUP | 15 | 38/19 | -2.00 | 22 | +4.99 | +0.61 | 3.7 | +0.30 | – | 1.20 |
| 34 | `N202X36` RSI2<10 dalam trend naik x X36 | **50.4** | 59 | 85 | 28 | 50 | BELUM CUKUP | 2 | 17/0 | -0.29 | 2 | +1.01 | +10.00 | 0.0 | – | – | – |
| 35 | `M05` MACD Divergence + Pengesahan | **50.4** | 47 | 64 | 42 | 55 | BELUM CUKUP | 15 | 41/12 | -1.23 | 22 | +2.15 | +0.63 | 1.5 | -0.44 | – | -0.63 |
| 36 | `N40X16` OBV tinggi baharu + MA50 → kel | **50.2** | 58 | 41 | 48 | 70 | BELUM CUKUP | 9 | 85/32 | +0.11 | 9 | -2.33 | -0.44 | 2.6 | +0.40 | – | – |
| 37 | `N75X17` RSI14 < 40 tanpa penapis → kel | **49.9** | 50 | 52 | 41 | 70 | BELUM CUKUP | 9 | 296/150 | -0.36 | 9 | -1.30 | -0.27 | 2.4 | -0.95 | – | – |
| 38 | `M51` O'Neil Cawan & Pemegang | **49.9** | 54 | 57 | 35 | 56 | BELUM CUKUP | 2 | 3/0 | -0.57 | 12 | -0.11 | -0.11 | 0.5 | +0.82 | – | 2.40 |
| 39 | `N40X36` OBV tinggi baharu + MA50 → kel | **49.8** | 59 | 39 | 46 | 67 | BELUM CUKUP | 9 | 69/14 | +0.03 | 9 | -2.59 | -0.54 | 2.9 | +0.45 | – | – |
| 40 | `N64X36` Episodic pivot → keluar selepa | **49.6** | 54 | 49 | 35 | 70 | BELUM CUKUP | 7 | 49/7 | -0.01 | 9 | -1.71 | -0.43 | 2.3 | -0.48 | – | – |
| 41 | `M89` Chande 65sma-3cc | **49.5** | 46 | 51 | 54 | 43 | BELUM CUKUP | 22 | 190/90 | -1.25 | 22 | +0.80 | +0.11 | 3.4 | -0.04 | – | -0.10 |
| 42 | `N25X36` Supertrend + EMA + ADX>23 → ke | **49.5** | 46 | 55 | 39 | 70 | BELUM CUKUP | 9 | 134/30 | -1.18 | 9 | +0.42 | +0.10 | 2.2 | -0.69 | – | – |
| 43 | `N203X36` Gap 2% lalu MA20 silang MA50 x | **49.3** | 48 | 50 | 28 | 50 | BELUM CUKUP | 2 | 9/0 | -0.94 | 2 | -0.67 | -0.52 | 0.9 | – | – | – |
| 44 | `M07` Qullamaggie Breakout | **49.3** | 30 | 64 | 27 | 15 | BELUM CUKUP | 1 | 1/1 | -2.53 | 22 | -0.25 | -0.21 | 0.8 | -0.22 | – | -1.12 |
| 45 | `M117` Landry Pullback (high 2 bulan) | **49.2** | 59 | 37 | 55 | 38 | BELUM CUKUP | 19 | 155/19 | +0.31 | 22 | -6.21 | -0.76 | 4.5 | +0.85 | – | 0.75 |
| 46 | `M37` Weinstein Peringkat 2 | **49.2** | 47 | 62 | 24 | 55 | BELUM CUKUP | 3 | 7/0 | -0.32 | 16 | -0.09 | -0.08 | 0.4 | -0.60 | – | -0.43 |
| 47 | `N48X36` Inside day pecah → keluar sele | **49.0** | 49 | 43 | 41 | 70 | BELUM CUKUP | 9 | 317/209 | -0.14 | 9 | -3.44 | -0.41 | 5.2 | -0.93 | – | – |
| 48 | `N64X16` Episodic pivot → keluar bila s | **49.0** | 53 | 46 | 35 | 61 | BELUM CUKUP | 7 | 49/6 | +0.01 | 9 | -2.33 | -0.58 | 2.1 | -0.50 | – | – |
| 49 | `M27` Price Action 4 Tiang | **49.0** | 47 | 40 | 42 | 15 | BELUM CUKUP | 2 | 546/454 | -0.89 | 22 | -2.73 | -0.53 | 2.9 | -0.46 | – | -1.20 |
| 50 | `M39` Radge Pecahan Bollinger 100 ha | **48.9** | 34 | 65 | 50 | 55 | BELUM CUKUP | 21 | 240/51 | -2.11 | 22 | +7.47 | +3.12 | 1.1 | -0.17 | – | -0.31 |
| 51 | `N201X36` MA20 silang MA50 atas MA50 x X | **48.9** | 40 | 40 | 28 | 50 | BELUM CUKUP | 2 | 17/0 | -1.39 | 2 | -1.43 | -0.97 | 1.0 | – | – | – |
| 52 | `M45` High 52 Minggu (George & Hwang | **48.9** | 20 | 40 | 28 | 15 | BELUM CUKUP | 1 | 2/1 | -5.23 | 11 | -1.02 | -0.57 | 0.9 | -0.13 | – | -0.45 |
| 53 | `N64X14` Episodic pivot → keluar bila r | **48.8** | 53 | 46 | 33 | 61 | BELUM CUKUP | 7 | 49/3 | -0.06 | 9 | -2.33 | -0.58 | 2.1 | -0.49 | – | – |
| 54 | `N64X17` Episodic pivot → keluar bila a | **48.8** | 48 | 45 | 35 | 70 | BELUM CUKUP | 7 | 49/12 | -0.43 | 9 | -2.01 | -0.50 | 2.3 | -0.67 | – | – |
| 55 | `M08` SMA20 + SMA200 | **48.7** | 47 | 43 | 51 | 55 | BELUM CUKUP | 20 | 214/117 | -0.88 | 22 | -1.68 | -0.31 | 3.6 | -0.34 | – | -0.83 |
| 56 | `M84` Jarak purata bergerak MAD 21/2 | **48.6** | 20 | 14 | 33 | 15 | BELUM CUKUP | 1 | 58/39 | -3.94 | 11 | -7.11 | -0.91 | 6.3 | -0.72 | – | -2.03 |
| 57 | `N75X14` RSI14 < 40 tanpa penapis → kel | **48.4** | 48 | 41 | 38 | 70 | BELUM CUKUP | 9 | 204/46 | -0.26 | 9 | -3.73 | -0.68 | 3.2 | -0.91 | – | – |
| 58 | `M131` Ross Hook (Joe Ross) | **48.3** | 48 | 51 | 55 | 21 | BELUM CUKUP | 22 | 262/117 | -0.99 | 22 | +0.23 | +0.04 | 3.4 | +0.10 | – | 0.21 |
| 59 | `M94` Pecutan Momentum (Chen, Yu & W | **48.3** | 18 | 10 | 17 | 24 | BELUM CUKUP | 1 | 33/0 | -9.21 | 11 | -9.39 | -0.80 | 7.0 | -1.17 | – | -4.04 |
| 60 | `N28X36` ADX>25 + DI+ > DI- → keluar se | **48.2** | 48 | 35 | 44 | 70 | BELUM CUKUP | 9 | 341/216 | -0.20 | 9 | -5.15 | -0.82 | 3.8 | -0.56 | – | – |
| 61 | `N42X36` Lonjakan volum 2x → keluar sel | **48.2** | 48 | 36 | 42 | 70 | BELUM CUKUP | 9 | 198/96 | -0.29 | 9 | -4.10 | -0.55 | 4.1 | -0.79 | – | – |
| 62 | `M96` Momo India: Ranking Sharpe 3/6 | **48.2** | 17 | 8 | 9 | 15 | BELUM CUKUP | 1 | 6/6 | -13.40 | 11 | -8.03 | -1.00 | 6.6 | -5.94 | – | -15.34 |
| 63 | `N36X36` Pocket pivot → keluar selepas  | **47.8** | 35 | 52 | 36 | 70 | BELUM CUKUP | 9 | 151/68 | -2.07 | 9 | +2.69 | +0.46 | 2.5 | -1.35 | – | – |
| 64 | `N19X13` Bawah jalur BB + RSI<30 → kelu | **47.8** | 43 | 41 | 25 | 70 | BELUM CUKUP | 5 | 101/0 | -0.71 | 9 | -1.52 | -0.46 | 2.3 | -0.67 | – | – |
| 65 | `M78` Alvarez Pecahan Mingguan DTAYS | **47.6** | 19 | 22 | 40 | 15 | BELUM CUKUP | 2 | 73/41 | -2.24 | 21 | -8.40 | -0.78 | 7.2 | -0.08 | – | -0.27 |
| 66 | `N28X16` ADX>25 + DI+ > DI- → keluar bi | **47.4** | 38 | 43 | 36 | 70 | BELUM CUKUP | 9 | 360/227 | -0.83 | 9 | -2.62 | -0.42 | 3.5 | -1.50 | – | – |
| 67 | `N24X36` Supertrend(10,3) + ADX>20 → ke | **47.3** | 39 | 39 | 39 | 70 | BELUM CUKUP | 9 | 162/51 | -1.37 | 9 | -2.10 | -0.46 | 2.6 | -0.89 | – | – |
| 68 | `N42X16` Lonjakan volum 2x → keluar bil | **47.3** | 47 | 33 | 42 | 49 | BELUM CUKUP | 9 | 202/93 | -0.26 | 9 | -4.81 | -0.74 | 4.3 | -0.73 | – | – |
| 69 | `M153` Range Leader | **47.2** | 52 | 39 | 55 | 24 | BELUM CUKUP | 22 | 1342/1186 | -0.16 | 22 | -4.35 | -0.42 | 6.8 | +0.06 | – | 0.30 |
| 70 | `M105` Supertrend tulen | **47.1** | 44 | 46 | 55 | 24 | BELUM CUKUP | 22 | 371/120 | -1.15 | 22 | +0.78 | +0.11 | 4.0 | +0.10 | – | 0.27 |
| 71 | `M41` FW Penyatuan Mingguan | **47.1** | 39 | 29 | 42 | 32 | BELUM CUKUP | 5 | 67/9 | -0.78 | 21 | -4.47 | -0.54 | 4.9 | +0.35 | – | 0.57 |
| 72 | `N65X14` Gap 4% + volum + hampir 52w →  | **47.0** | 40 | 40 | 26 | 56 | BELUM CUKUP | 6 | 31/1 | -0.92 | 9 | -2.81 | -0.67 | 2.4 | -0.93 | – | – |
| 73 | `M21` Marius 3 Persediaan (Pecahan+J | **47.0** | 31 | 45 | 37 | 21 | BELUM CUKUP | 5 | 5/3 | -2.82 | 14 | -1.38 | -0.59 | 1.4 | +0.11 | – | 0.20 |
| 74 | `M02` MACD + SMA200 | **46.9** | 38 | 48 | 45 | 55 | BELUM CUKUP | 22 | 131/83 | -2.60 | 22 | +2.56 | +0.28 | 2.9 | -1.02 | – | -5.55 |
| 75 | `M54` IBD Power Trend | **46.9** | 44 | 47 | 51 | 23 | BELUM CUKUP | 20 | 209/108 | -1.45 | 22 | +2.31 | +0.22 | 5.3 | -0.37 | – | -0.74 |
| 76 | `N66X36` 52w tinggi + pengesahan 1% → k | **46.9** | 38 | 34 | 30 | 65 | BELUM CUKUP | 6 | 37/2 | -0.91 | 8 | -3.53 | -0.80 | 3.1 | -0.62 | – | – |
| 77 | `M138` 直升机空中加油 (Helikopter isi minyak | **46.9** | 29 | 42 | 16 | 15 | BELUM CUKUP | 3 | 3/0 | -3.32 | 15 | -0.93 | -0.83 | 0.5 | -1.56 | – | -2.38 |
| 78 | `M148` Natural Number Method | **46.8** | 35 | 56 | 41 | 55 | BELUM CUKUP | 22 | 225/171 | -2.28 | 22 | +1.72 | +0.33 | 2.7 | -1.57 | – | -4.98 |
| 79 | `M18` EMA9/21 Pullback | **46.8** | 57 | 40 | 54 | 15 | BELUM CUKUP | 22 | 406/289 | -0.24 | 22 | -4.52 | -0.75 | 4.1 | -0.06 | – | -0.20 |
| 80 | `M15` Break & Retest + Henti ATR | **46.8** | 56 | 40 | 54 | 15 | BELUM CUKUP | 22 | 306/192 | -0.18 | 22 | -4.23 | -0.52 | 4.4 | -0.04 | – | -0.10 |
| 81 | `N75X15` RSI14 < 40 tanpa penapis → eko | **46.7** | 46 | 40 | 27 | 56 | BELUM CUKUP | 9 | 131/0 | -0.37 | 9 | -3.12 | -0.84 | 2.2 | -0.66 | – | – |
| 82 | `N75X13` RSI14 < 40 tanpa penapis → kel | **46.7** | 44 | 39 | 29 | 56 | BELUM CUKUP | 9 | 132/1 | -0.49 | 9 | -3.12 | -0.84 | 2.2 | -0.70 | – | – |
| 83 | `N35X36` Pecah 52 minggu tinggi → kelua | **46.7** | 31 | 58 | 26 | 70 | BELUM CUKUP | 8 | 48/2 | -1.67 | 9 | +0.42 | +0.23 | 0.9 | -1.27 | – | – |
| 84 | `N36X16` Pocket pivot → keluar bila sup | **46.6** | 30 | 47 | 36 | 70 | BELUM CUKUP | 9 | 155/62 | -2.07 | 9 | +0.46 | +0.13 | 1.8 | -1.31 | – | – |
| 85 | `M64` O'Neil Tiga Minggu Ketat | **46.5** | 25 | 22 | 25 | 15 | BELUM CUKUP | 3 | 3/3 | -12.60 | 22 | -3.76 | -0.84 | 2.6 | -1.26 | – | -14.58 |
| 86 | `N08X36` tutup>EMA20 tidak terlalu jauh | **46.4** | 31 | 44 | 35 | 70 | BELUM CUKUP | 9 | 393/247 | -1.69 | 9 | -1.78 | -0.32 | 2.7 | -1.65 | – | – |
| 87 | `N43X36` Undur EMA8 + penapis MA50 → ke | **46.4** | 34 | 38 | 36 | 70 | BELUM CUKUP | 9 | 180/34 | -1.48 | 9 | -2.48 | -0.59 | 2.3 | -1.07 | – | – |
| 88 | `N65X36` Gap 4% + volum + hampir 52w →  | **46.4** | 38 | 36 | 26 | 44 | BELUM CUKUP | 6 | 31/1 | -1.03 | 9 | -3.31 | -0.79 | 2.6 | -0.95 | – | – |
| 89 | `N07X16` Tiga MA tersusun → keluar bila | **46.3** | 29 | 52 | 34 | 51 | BELUM CUKUP | 9 | 146/20 | -1.78 | 9 | -0.03 | -0.01 | 2.0 | -1.17 | – | – |
| 90 | `M157` Consolidation Pivot Breakout ( | **46.3** | 26 | 36 | 28 | 15 | BELUM CUKUP | 4 | 4/3 | -4.79 | 19 | -1.90 | -0.65 | 1.6 | -0.77 | – | -2.03 |
| 91 | `M128` Inventory Retracement Bar (IRB | **46.2** | 50 | 35 | 54 | 23 | BELUM CUKUP | 21 | 154/86 | -0.47 | 22 | -3.28 | -0.30 | 6.6 | +0.06 | – | 0.26 |
| 92 | `M88` O'Neil Shakeout +3 | **46.2** | 33 | 46 | 46 | 55 | BELUM CUKUP | 17 | 75/37 | -3.18 | 22 | +0.43 | +0.04 | 5.1 | -0.45 | – | -0.79 |
| 93 | `N119X13` 3 tutup turun berturut → kelua | **46.2** | 34 | 37 | 35 | 70 | BELUM CUKUP | 9 | 226/47 | -0.94 | 9 | -5.27 | -0.64 | 6.0 | -1.37 | – | – |
| 94 | `N41X36` CMF20>0 + tutup>EMA20 → keluar | **46.1** | 29 | 43 | 36 | 70 | BELUM CUKUP | 9 | 238/145 | -1.95 | 9 | -1.68 | -0.34 | 2.7 | -1.56 | – | – |
| 95 | `M92` CCI-50 | **46.0** | 50 | 42 | 51 | 15 | BELUM CUKUP | 22 | 564/381 | -0.60 | 22 | -2.34 | -0.33 | 3.2 | -0.34 | – | -0.59 |
| 96 | `M102` Stockbee SLTB | **45.9** | 48 | 44 | 51 | 15 | BELUM CUKUP | 22 | 399/286 | -1.13 | 22 | -1.32 | -0.12 | 5.6 | -0.40 | – | -0.99 |
| 97 | `N42X14` Lonjakan volum 2x → keluar bil | **45.8** | 37 | 29 | 36 | 68 | BELUM CUKUP | 9 | 181/17 | -0.81 | 9 | -6.68 | -0.60 | 5.5 | -0.79 | – | – |
| 98 | `M38` Darvas Kotak | **45.8** | 23 | 32 | 34 | 32 | BELUM CUKUP | 5 | 26/1 | -2.67 | 21 | -2.21 | -0.22 | 5.2 | +0.12 | – | 0.58 |
| 99 | `M116` 2/20 EMA Breakout (Landry) | **45.7** | 50 | 39 | 54 | 15 | BELUM CUKUP | 22 | 576/433 | -0.53 | 22 | -0.69 | -0.06 | 7.6 | -0.08 | – | -0.31 |
| 100 | `N124X36` Episodic pivot gap 8-10% → kel | **45.7** | 44 | 30 | 36 | 30 | BELUM CUKUP | 9 | 42/13 | -0.49 | 9 | -4.35 | -0.83 | 3.6 | -0.71 | – | – |
| 101 | `N37X36` Gap and go → keluar selepas DU | **45.7** | 25 | 37 | 33 | 70 | BELUM CUKUP | 7 | 83/24 | -1.85 | 9 | -1.92 | -0.41 | 2.7 | -1.15 | – | – |
| 102 | `N76X16` Tutup > MA50 (penapis trend tu | **45.6** | 24 | 53 | 31 | 70 | BELUM CUKUP | 9 | 293/171 | -2.14 | 9 | +0.50 | +0.14 | 1.6 | -2.08 | – | – |
| 103 | `N37X17` Gap and go → keluar bila adx14 | **45.6** | 24 | 37 | 33 | 70 | BELUM CUKUP | 7 | 83/29 | -1.91 | 9 | -1.64 | -0.34 | 2.6 | -1.30 | – | – |
| 104 | `M120` Reversal New Highs | **45.5** | 44 | 40 | 45 | 15 | BELUM CUKUP | 13 | 19/12 | -1.08 | 22 | -1.35 | -0.21 | 3.2 | -0.02 | – | -0.11 |
| 105 | `N45X36` Undur EMA21 cerun positif → ke | **45.5** | 29 | 49 | 35 | 30 | BELUM CUKUP | 9 | 130/42 | -1.95 | 9 | -0.04 | -0.02 | 1.6 | -1.29 | – | – |
| 106 | `M134` First Kiss After Daylight (Lan | **45.4** | 40 | 40 | 49 | 24 | BELUM CUKUP | 17 | 57/17 | -1.28 | 22 | -2.34 | -0.33 | 4.0 | +0.25 | – | 0.29 |
| 107 | `M68` Kell Base n' Break | **45.4** | 32 | 48 | 46 | 28 | BELUM CUKUP | 14 | 43/13 | -2.70 | 22 | +0.55 | +0.12 | 2.0 | +0.01 | – | 0.04 |
| 108 | `M115` Bow Tie (Landry) | **45.4** | 30 | 38 | 48 | 38 | BELUM CUKUP | 11 | 36/25 | -1.93 | 22 | -4.09 | -0.50 | 4.5 | +0.14 | – | 0.78 |
| 109 | `M12` Parabolic SAR | **45.3** | 36 | 46 | 50 | 30 | BELUM CUKUP | 22 | 386/201 | -1.81 | 22 | -0.20 | -0.03 | 2.9 | -0.47 | – | -0.99 |
| 110 | `M49` Ichimoku (Tutup Atas Awan + Te | **45.3** | 41 | 50 | 47 | 15 | BELUM CUKUP | 22 | 306/175 | -1.63 | 22 | +0.99 | +0.15 | 3.4 | -0.82 | – | -1.01 |
| 111 | `M150` Trend Bar Failure (Brooks) | **45.1** | 49 | 38 | 48 | 15 | BELUM CUKUP | 20 | 104/48 | -0.41 | 22 | -5.46 | -0.81 | 3.3 | -0.33 | – | -0.97 |
| 112 | `N09X36` Undur EMA10 + penapis EMA50 →  | **45.1** | 29 | 34 | 36 | 54 | BELUM CUKUP | 9 | 190/50 | -1.75 | 9 | -3.24 | -0.77 | 2.3 | -1.20 | – | – |
| 113 | `M106` DMI Wilder | **45.0** | 42 | 43 | 50 | 15 | BELUM CUKUP | 20 | 130/76 | -1.23 | 22 | -1.10 | -0.24 | 2.6 | -0.34 | – | -0.68 |
| 114 | `N41X16` CMF20>0 + tutup>EMA20 → keluar | **45.0** | 23 | 45 | 31 | 70 | BELUM CUKUP | 9 | 281/165 | -2.25 | 9 | -0.70 | -0.26 | 1.7 | -2.13 | – | – |
| 115 | `N33X16` Donchian20 + penapis MA200 → k | **45.0** | 24 | 48 | 24 | 70 | BELUM CUKUP | 8 | 98/11 | -3.61 | 9 | -0.37 | -0.10 | 1.7 | -2.04 | – | – |
| 116 | `M149` 3-Step Pullback | **44.9** | 42 | 36 | 54 | 21 | BELUM CUKUP | 20 | 217/59 | -1.06 | 22 | -2.15 | -0.20 | 5.8 | +0.26 | – | 0.21 |
| 117 | `M32` Momentum Burst | **44.9** | 49 | 26 | 50 | 24 | BELUM CUKUP | 15 | 58/37 | -0.77 | 22 | -4.71 | -0.42 | 7.5 | +0.13 | – | 0.31 |
| 118 | `N68X36` Bullish engulfing + EMA21 → ke | **44.9** | 26 | 41 | 38 | 30 | BELUM CUKUP | 9 | 81/20 | -1.97 | 9 | -1.82 | -0.33 | 2.8 | -0.59 | – | – |
| 119 | `M143` 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke | **44.8** | 32 | 50 | 29 | 51 | BELUM CUKUP | 14 | 28/1 | -1.58 | 21 | -0.35 | -0.12 | 1.7 | -0.93 | – | -8.62 |
| 120 | `N08X16` tutup>EMA20 tidak terlalu jauh | **44.8** | 26 | 36 | 33 | 70 | BELUM CUKUP | 9 | 453/294 | -1.73 | 9 | -2.29 | -0.73 | 2.1 | -1.91 | – | – |
| 121 | `M144` Screw Bar | **44.8** | 31 | 34 | 33 | 15 | BELUM CUKUP | 7 | 10/7 | -2.07 | 20 | -2.00 | -0.76 | 1.2 | -0.68 | – | -1.38 |
| 122 | `N42X15` Lonjakan volum 2x → ekori Chan | **44.7** | 33 | 32 | 26 | 70 | BELUM CUKUP | 9 | 170/0 | -1.18 | 9 | -5.20 | -0.45 | 5.5 | -0.83 | – | – |
| 123 | `N76X36` Tutup > MA50 (penapis trend tu | **44.7** | 28 | 32 | 36 | 51 | BELUM CUKUP | 9 | 178/65 | -2.25 | 9 | -3.83 | -0.70 | 3.9 | -1.40 | – | – |
| 124 | `N42X17` Lonjakan volum 2x → keluar bil | **44.6** | 32 | 24 | 40 | 46 | BELUM CUKUP | 9 | 194/59 | -0.92 | 9 | -8.35 | -0.86 | 5.7 | -0.79 | – | – |
| 125 | `N80X36` Tinggi sepanjang masa → keluar | **44.5** | 28 | 36 | 30 | 30 | BELUM CUKUP | 8 | 39/2 | -1.50 | 9 | -2.41 | -0.70 | 2.0 | -0.80 | – | – |
| 126 | `N22X36` BB pecah atas + RSI → keluar s | **44.4** | 23 | 34 | 41 | 43 | BELUM CUKUP | 9 | 117/44 | -3.26 | 9 | -2.50 | -0.56 | 2.7 | -0.55 | – | – |
| 127 | `N16X13` RSI2<10 tanpa penapis → keluar | **44.3** | 28 | 29 | 30 | 70 | BELUM CUKUP | 9 | 154/4 | -1.34 | 9 | -6.14 | -0.68 | 5.8 | -0.98 | – | – |
| 128 | `N25X16` Supertrend + EMA + ADX>23 → ke | **44.3** | 24 | 41 | 27 | 59 | BELUM CUKUP | 9 | 120/4 | -2.40 | 9 | -1.83 | -0.38 | 2.6 | -1.37 | – | – |
| 129 | `N37X16` Gap and go → keluar bila super | **44.3** | 20 | 31 | 31 | 53 | BELUM CUKUP | 7 | 83/21 | -2.07 | 9 | -2.72 | -0.71 | 2.3 | -1.35 | – | – |
| 130 | `M26` Garis Trend Undur 3 Sentuhan + | **44.2** | 41 | 40 | 46 | 15 | BELUM CUKUP | 18 | 75/49 | -0.76 | 22 | -3.32 | -0.42 | 3.7 | -0.61 | – | -0.82 |
| 131 | `M31` Band Walk (BB 20/2) | **44.1** | 46 | 27 | 56 | 23 | BELUM CUKUP | 21 | 399/107 | -0.73 | 22 | -2.13 | -0.19 | 7.3 | +0.17 | – | 0.26 |
| 132 | `M36` Turtle 55/20 | **44.0** | 41 | 38 | 54 | 15 | BELUM CUKUP | 22 | 342/166 | -1.27 | 22 | -1.74 | -0.15 | 6.8 | -0.06 | – | -0.12 |
| 133 | `N25X17` Supertrend + EMA + ADX>23 → ke | **44.0** | 22 | 39 | 27 | 60 | BELUM CUKUP | 9 | 116/5 | -2.63 | 9 | -2.32 | -0.48 | 2.5 | -1.40 | – | – |
| 134 | `N113X16` 80-20 bar (sisi beli) → keluar | **44.0** | 40 | 18 | 40 | 30 | BELUM CUKUP | 9 | 317/218 | -0.35 | 9 | -8.67 | -0.99 | 7.2 | -1.08 | – | – |
| 135 | `N51X36` BB squeeze + Supertrend → kelu | **44.0** | 18 | 31 | 24 | 30 | BELUM CUKUP | 6 | 10/3 | -2.42 | 9 | -2.27 | -0.81 | 2.2 | -1.40 | – | – |
| 136 | `N07X36` Tiga MA tersusun → keluar sele | **43.9** | 24 | 41 | 30 | 30 | BELUM CUKUP | 9 | 146/10 | -2.06 | 9 | -1.85 | -0.46 | 2.6 | -1.28 | – | – |
| 137 | `N27X16` Ichimoku atas awan → keluar bi | **43.9** | 25 | 35 | 32 | 30 | BELUM CUKUP | 9 | 164/72 | -1.63 | 9 | -2.50 | -0.79 | 2.2 | -1.79 | – | – |
| 138 | `N36X14` Pocket pivot → keluar bila rsi | **43.9** | 25 | 28 | 32 | 70 | BELUM CUKUP | 9 | 149/24 | -2.72 | 9 | -3.03 | -0.41 | 4.0 | -1.43 | – | – |
| 139 | `M04` BB Squeeze Breakout | **43.8** | 30 | 38 | 53 | 36 | BELUM CUKUP | 20 | 154/57 | -1.98 | 22 | -0.42 | -0.05 | 4.2 | +0.15 | – | 0.23 |
| 140 | `N38X36` VCP pecah → keluar selepas DUA | **43.8** | 26 | 40 | 22 | 43 | BELUM CUKUP | 9 | 31/11 | -2.31 | 9 | -2.04 | -0.63 | 2.0 | -2.30 | – | – |
| 141 | `M139` 均线首次粘合向上发散 (MA berhimpun kali  | **43.7** | 28 | 40 | 46 | 55 | BELUM CUKUP | 22 | 89/28 | -2.91 | 22 | -0.58 | -0.07 | 3.3 | -0.46 | – | -1.47 |
| 142 | `N74X16` MACD atas garis isyarat (keada | **43.7** | 20 | 31 | 34 | 70 | BELUM CUKUP | 9 | 518/351 | -1.76 | 9 | -5.25 | -0.72 | 4.8 | -1.80 | – | – |
| 143 | `M44` Tapak Rata IBD | **43.7** | 31 | 38 | 22 | 15 | BELUM CUKUP | 8 | 9/5 | -4.28 | 22 | -3.75 | -0.79 | 3.0 | -2.24 | – | -30.14 |
| 144 | `N51X16` BB squeeze + Supertrend → kelu | **43.7** | 17 | 31 | 21 | 30 | BELUM CUKUP | 6 | 10/1 | -2.93 | 9 | -2.75 | -0.84 | 2.3 | -1.51 | – | – |
| 145 | `N39X36` NR7 kemudian pecah → keluar se | **43.7** | 15 | 22 | 17 | 30 | BELUM CUKUP | 5 | 29/7 | -4.39 | 8 | -3.66 | -0.99 | 2.6 | -2.50 | – | – |
| 146 | `M06` Minervini VCP Breakout | **43.6** | 32 | 52 | 46 | 15 | BELUM CUKUP | 21 | 84/41 | -2.12 | 22 | -0.17 | -0.03 | 3.0 | -0.59 | – | -1.41 |
| 147 | `N56X36` RSI>50 + ADX>20 → keluar selep | **43.6** | 22 | 29 | 33 | 56 | BELUM CUKUP | 9 | 198/81 | -1.91 | 9 | -5.22 | -0.71 | 5.5 | -1.75 | – | – |
| 148 | `M87` IBD Tapak Menaik | **43.6** | 24 | 32 | 37 | 15 | BELUM CUKUP | 8 | 11/6 | -3.99 | 22 | -4.35 | -0.65 | 3.9 | -0.55 | – | -1.78 |
| 149 | `N113X36` 80-20 bar (sisi beli) → keluar | **43.5** | 32 | 21 | 37 | 30 | BELUM CUKUP | 9 | 299/211 | -0.88 | 9 | -7.83 | -1.00 | 6.5 | -1.35 | – | – |
| 150 | `N73X13` Tutup bawah jalur bawah BB(20, | **43.5** | 29 | 29 | 28 | 30 | BELUM CUKUP | 9 | 143/1 | -1.19 | 9 | -5.60 | -0.86 | 3.8 | -0.84 | – | – |
| 151 | `N119X15` 3 tutup turun berturut → ekori | **43.4** | 18 | 32 | 19 | 64 | BELUM CUKUP | 7 | 53/0 | -2.07 | 9 | -5.44 | -0.80 | 4.7 | -1.58 | – | – |
| 152 | `N33X36` Donchian20 + penapis MA200 → k | **43.3** | 20 | 33 | 29 | 30 | BELUM CUKUP | 8 | 96/25 | -3.00 | 9 | -3.28 | -0.90 | 2.2 | -1.78 | – | – |
| 153 | `N37X14` Gap and go → keluar bila rsi14 | **43.3** | 18 | 27 | 27 | 30 | BELUM CUKUP | 7 | 82/8 | -2.63 | 9 | -4.14 | -0.72 | 3.2 | -1.46 | – | – |
| 154 | `N50X14` Mampat + pecah volum 1.5x → ke | **43.3** | 12 | 25 | 27 | 55 | BELUM CUKUP | 6 | 16/3 | -4.92 | 9 | -6.45 | -0.70 | 4.6 | -1.11 | – | – |
| 155 | `M34` Carter TTM Squeeze | **43.2** | 40 | 35 | 50 | 15 | BELUM CUKUP | 21 | 106/47 | -1.30 | 22 | -1.15 | -0.16 | 4.1 | -0.21 | – | -0.60 |
| 156 | `M107` Golden Cross SMA50/200 | **43.2** | 37 | 39 | 44 | 15 | BELUM CUKUP | 19 | 41/8 | -1.16 | 22 | -1.93 | -0.42 | 2.1 | -0.11 | – | -0.15 |
| 157 | `N68X16` Bullish engulfing + EMA21 → ke | **43.2** | 18 | 37 | 36 | 30 | BELUM CUKUP | 9 | 81/20 | -2.34 | 9 | -3.15 | -0.42 | 3.6 | -0.85 | – | – |
| 158 | `N22X16` BB pecah atas + RSI → keluar b | **43.2** | 20 | 32 | 38 | 30 | BELUM CUKUP | 9 | 119/25 | -3.43 | 9 | -3.07 | -0.72 | 2.9 | -0.74 | – | – |
| 159 | `N06X36` Golden cross MA50/MA200 → kelu | **43.2** | 20 | 36 | 26 | 30 | BELUM CUKUP | 8 | 21/2 | -1.76 | 9 | -3.17 | -0.78 | 2.7 | -1.19 | – | – |
| 160 | `N50X17` Mampat + pecah volum 1.5x → ke | **43.2** | 11 | 23 | 27 | 60 | BELUM CUKUP | 6 | 15/3 | -5.51 | 9 | -6.83 | -0.74 | 4.8 | -1.06 | – | – |
| 161 | `N56X17` RSI>50 + ADX>20 → keluar bila  | **43.1** | 19 | 31 | 28 | 70 | BELUM CUKUP | 9 | 138/30 | -3.20 | 9 | -3.64 | -0.73 | 2.6 | -1.93 | – | – |
| 162 | `N124X15` Episodic pivot gap 8-10% → eko | **43.0** | 24 | 26 | 27 | 62 | BELUM CUKUP | 9 | 42/0 | -1.50 | 9 | -4.39 | -0.64 | 3.8 | -0.75 | – | – |
| 163 | `M121` High 2 bull flag (Brooks) | **43.0** | 12 | 14 | 21 | 15 | BELUM CUKUP | 5 | 7/4 | -10.20 | 18 | -7.06 | -0.86 | 5.0 | -1.81 | – | -21.66 |
| 164 | `N33X14` Donchian20 + penapis MA200 → k | **42.9** | 20 | 32 | 24 | 35 | BELUM CUKUP | 8 | 107/7 | -3.68 | 9 | -3.26 | -0.79 | 2.5 | -1.87 | – | – |
| 165 | `N53X16` Supertrend + ADX>25 → keluar b | **42.8** | 19 | 31 | 34 | 30 | BELUM CUKUP | 9 | 114/7 | -2.07 | 9 | -4.62 | -0.68 | 4.7 | -0.66 | – | – |
| 166 | `N55X13` BB + RSI + ADX>20 → keluar bil | **42.8** | 24 | 33 | 21 | 45 | BELUM CUKUP | 9 | 66/0 | -1.68 | 9 | -3.79 | -0.77 | 3.6 | -1.39 | – | – |
| 167 | `M20` EMA10/15 Crossover + Sudut | **42.6** | 39 | 37 | 45 | 15 | BELUM CUKUP | 22 | 490/387 | -1.31 | 22 | -3.97 | -0.66 | 3.2 | -1.11 | – | -6.72 |
| 168 | `N57X36` ADX bangkit daripada <20 → kel | **42.6** | 19 | 40 | 22 | 30 | BELUM CUKUP | 9 | 75/7 | -3.46 | 9 | -1.32 | -0.36 | 2.3 | -2.07 | – | – |
| 169 | `M119` 180 Bullish (Cooper) | **42.5** | 36 | 33 | 48 | 15 | BELUM CUKUP | 19 | 151/68 | -1.21 | 22 | -5.17 | -0.48 | 5.3 | -0.56 | – | -1.61 |
| 170 | `M127` Slingshot Bullish | **42.5** | 31 | 42 | 43 | 15 | BELUM CUKUP | 18 | 107/78 | -1.82 | 22 | -4.06 | -0.59 | 3.3 | -1.08 | – | -1.28 |
| 171 | `N57X16` ADX bangkit daripada <20 → kel | **42.5** | 19 | 40 | 22 | 30 | BELUM CUKUP | 9 | 72/6 | -3.58 | 9 | -1.23 | -0.34 | 2.2 | -2.10 | – | – |
| 172 | `N53X17` Supertrend + ADX>25 → keluar b | **42.5** | 19 | 31 | 30 | 30 | BELUM CUKUP | 9 | 106/1 | -2.39 | 9 | -4.57 | -0.68 | 4.4 | -0.69 | – | – |
| 173 | `N56X16` RSI>50 + ADX>20 → keluar bila  | **42.5** | 17 | 27 | 33 | 52 | BELUM CUKUP | 9 | 216/91 | -1.85 | 9 | -5.17 | -1.00 | 3.6 | -1.81 | – | – |
| 174 | `N47X16` NR7 + EMA9>EMA21 → keluar bila | **42.4** | 18 | 36 | 27 | 30 | BELUM CUKUP | 9 | 195/36 | -1.95 | 9 | -3.48 | -0.80 | 2.8 | -2.21 | – | – |
| 175 | `N28X14` ADX>25 + DI+ > DI- → keluar bi | **42.4** | 19 | 25 | 29 | 50 | BELUM CUKUP | 9 | 188/15 | -2.71 | 9 | -6.07 | -0.85 | 3.9 | -1.55 | – | – |
| 176 | `N31X36` Turtle sistem 2 → keluar selep | **42.3** | 19 | 25 | 24 | 30 | BELUM CUKUP | 8 | 100/6 | -3.05 | 9 | -4.83 | -0.99 | 2.8 | -1.74 | – | – |
| 177 | `M14` Walking with the Whales | **42.2** | 43 | 29 | 48 | 15 | BELUM CUKUP | 22 | 974/680 | -0.77 | 22 | -8.90 | -0.77 | 6.8 | -0.71 | – | -1.08 |
| 178 | `M50` Elder Triple Screen | **42.2** | 41 | 29 | 50 | 15 | BELUM CUKUP | 22 | 589/357 | -0.92 | 22 | -7.92 | -0.72 | 6.6 | -0.51 | – | -0.77 |
| 179 | `M130` 多方炮 (dua lilin hijau mengapit  | **42.2** | 23 | 19 | 33 | 15 | BELUM CUKUP | 8 | 12/3 | -4.61 | 20 | -5.25 | -0.71 | 3.5 | -0.51 | – | -0.46 |
| 180 | `N24X17` Supertrend(10,3) + ADX>20 → ke | **42.1** | 18 | 29 | 26 | 42 | BELUM CUKUP | 9 | 125/21 | -3.22 | 9 | -3.66 | -0.89 | 2.2 | -2.07 | – | – |
| 181 | `M141` First Thrust (Landry) | **41.9** | 16 | 29 | 28 | 15 | BELUM CUKUP | 8 | 26/13 | -3.78 | 22 | -5.52 | -0.81 | 3.6 | -1.80 | – | -3.28 |
| 182 | `M67` Rayner Teo: Ujian Ketiga pada  | **41.8** | 31 | 32 | 39 | 15 | BELUM CUKUP | 15 | 30/19 | -2.90 | 22 | -4.85 | -0.45 | 6.3 | -0.94 | – | -4.20 |
| 183 | `N29X16` PSAR naik + tutup>MA50 → kelua | **41.8** | 15 | 25 | 30 | 48 | BELUM CUKUP | 9 | 198/85 | -3.41 | 9 | -5.91 | -0.80 | 5.3 | -2.19 | – | – |
| 184 | `N54X16` Supertrend + RSI>50 → keluar b | **41.8** | 16 | 27 | 24 | 65 | BELUM CUKUP | 9 | 122/9 | -4.04 | 9 | -4.85 | -0.61 | 4.8 | -2.04 | – | – |
| 185 | `N28X17` ADX>25 + DI+ > DI- → keluar bi | **41.7** | 17 | 27 | 22 | 53 | BELUM CUKUP | 9 | 128/1 | -2.94 | 9 | -5.24 | -0.73 | 4.1 | -1.55 | – | – |
| 186 | `N16X15` RSI2<10 tanpa penapis → ekori  | **41.7** | 19 | 23 | 24 | 41 | BELUM CUKUP | 9 | 147/0 | -1.64 | 9 | -8.22 | -0.70 | 8.2 | -1.06 | – | – |
| 187 | `N27X36` Ichimoku atas awan → keluar se | **41.7** | 18 | 24 | 27 | 30 | BELUM CUKUP | 9 | 100/15 | -2.63 | 9 | -4.71 | -1.00 | 3.3 | -1.83 | – | – |
| 188 | `N54X36` Supertrend + RSI>50 → keluar s | **41.6** | 19 | 19 | 34 | 30 | BELUM CUKUP | 9 | 168/70 | -2.15 | 9 | -8.18 | -1.00 | 6.9 | -1.62 | – | – |
| 189 | `M136` Short/Intermediate-term Low (L | **41.5** | 29 | 39 | 49 | 15 | BELUM CUKUP | 22 | 792/301 | -2.13 | 22 | -2.00 | -0.43 | 2.8 | -0.62 | – | -0.31 |
| 190 | `M135` 3rd Watch | **41.5** | 16 | 30 | 32 | 15 | BELUM CUKUP | 9 | 15/3 | -4.41 | 22 | -5.45 | -0.69 | 4.0 | -0.88 | – | -4.35 |
| 191 | `M156` Single Penetration (DiNapoli) | **41.4** | 36 | 30 | 48 | 15 | BELUM CUKUP | 22 | 245/157 | -1.10 | 22 | -4.92 | -0.38 | 6.8 | -0.79 | – | -2.58 |
| 192 | `M99` Three Line Break | **41.2** | 31 | 34 | 49 | 15 | BELUM CUKUP | 22 | 165/97 | -2.74 | 22 | -2.24 | -0.30 | 3.8 | -0.55 | – | -2.05 |
| 193 | `N24X16` Supertrend(10,3) + ADX>20 → ke | **41.2** | 17 | 27 | 21 | 30 | BELUM CUKUP | 9 | 120/4 | -3.33 | 9 | -4.01 | -0.97 | 2.3 | -2.08 | – | – |
| 194 | `M152` Spike & Ledge | **41.0** | 25 | 41 | 42 | 15 | BELUM CUKUP | 19 | 50/8 | -2.15 | 22 | -0.48 | -0.09 | 3.0 | -0.35 | – | -0.97 |
| 195 | `M28` VWAP Separator + Kiss Pivot | **40.9** | 33 | 29 | 45 | 15 | BELUM CUKUP | 20 | 120/97 | -1.27 | 22 | -7.29 | -0.86 | 5.5 | -1.03 | – | -9.01 |
| 196 | `N22X14` BB pecah atas + RSI → keluar b | **40.9** | 14 | 21 | 30 | 30 | BELUM CUKUP | 9 | 123/14 | -4.27 | 9 | -7.27 | -0.96 | 3.9 | -1.49 | – | – |
| 197 | `M66` IBD Undur Pertama ke Purata 50 | **40.7** | 33 | 29 | 49 | 15 | BELUM CUKUP | 22 | 250/147 | -1.63 | 22 | -5.82 | -0.50 | 6.8 | -0.60 | – | -1.45 |
| 198 | `M126` Hidden Smash Day (beli, Larry  | **40.7** | 16 | 32 | 35 | 15 | BELUM CUKUP | 11 | 21/11 | -3.35 | 21 | -4.80 | -0.65 | 4.4 | -0.83 | – | -1.31 |
| 199 | `M140` 猎豹出击 (Serangan Cheetah) | **40.6** | 18 | 28 | 34 | 15 | BELUM CUKUP | 11 | 42/13 | -2.07 | 22 | -6.00 | -0.80 | 3.7 | -1.25 | – | -1.38 |
| 200 | `M73` ADX(5) > 40 + Julat Terkecil 6 | **40.5** | 34 | 27 | 47 | 15 | BELUM CUKUP | 22 | 1066/823 | -0.49 | 22 | -9.08 | -1.00 | 5.2 | -0.81 | – | -4.98 |
| 201 | `M19` Sneaky Pivot (proksi harian) | **40.5** | 26 | 36 | 47 | 15 | BELUM CUKUP | 21 | 424/248 | -3.25 | 22 | -2.40 | -0.32 | 3.7 | -0.80 | – | -11.61 |
| 202 | `N47X36` NR7 + EMA9>EMA21 → keluar sele | **40.5** | 9 | 24 | 23 | 30 | BELUM CUKUP | 8 | 177/27 | -2.75 | 9 | -8.60 | -1.00 | 6.0 | -2.51 | – | – |
| 203 | `M29` EMA3 + RSI75 + Stokastik | **40.4** | 26 | 29 | 41 | 15 | BELUM CUKUP | 16 | 37/30 | -2.36 | 22 | -8.29 | -0.66 | 7.4 | -0.94 | – | -5.40 |
| 204 | `N29X36` PSAR naik + tutup>MA50 → kelua | **40.4** | 14 | 17 | 28 | 30 | BELUM CUKUP | 9 | 152/57 | -3.43 | 9 | -9.89 | -1.00 | 8.2 | -2.28 | – | – |
| 205 | `M01` Bollinger Band + RSI | **39.9** | 49 | 15 | 44 | 15 | BELUM CUKUP | 20 | 113/26 | +0.06 | 22 | -9.15 | -0.85 | 4.8 | -0.63 | – | -2.47 |
| 206 | `M11` NR7 Breakout + Volume | **39.8** | 31 | 25 | 45 | 15 | BELUM CUKUP | 20 | 118/85 | -0.98 | 22 | -9.10 | -0.72 | 7.7 | -1.01 | – | -0.91 |
| 207 | `M95` Nisbah Kebaharuan High 52 Ming | **39.7** | 24 | 30 | 48 | 15 | BELUM CUKUP | 20 | 127/64 | -1.87 | 22 | -6.52 | -0.72 | 5.1 | -0.54 | – | -1.21 |
| 208 | `M55` Guppy GMMA | **39.6** | 29 | 27 | 49 | 15 | BELUM CUKUP | 22 | 229/131 | -1.86 | 22 | -7.16 | -0.82 | 4.9 | -0.57 | – | -1.51 |
| 209 | `M57` Landry Trend Knockout (TKO) | **39.3** | 27 | 31 | 41 | 15 | BELUM CUKUP | 22 | 176/115 | -2.10 | 22 | -5.45 | -0.65 | 4.1 | -1.50 | – | -3.93 |
| 210 | `M59` Anjakan Julat RSI | **39.3** | 18 | 24 | 42 | 15 | BELUM CUKUP | 14 | 36/18 | -5.06 | 22 | -3.64 | -0.45 | 4.3 | -0.53 | – | -1.99 |
| 211 | `M125` 2-Bar Breakout | **39.2** | 26 | 30 | 46 | 15 | BELUM CUKUP | 22 | 1132/451 | -2.58 | 22 | -4.96 | -0.60 | 3.8 | -0.99 | – | -0.47 |
| 212 | `M155` Market Cycle Strategy | **39.1** | 26 | 29 | 46 | 15 | BELUM CUKUP | 22 | 741/330 | -2.37 | 22 | -4.60 | -0.61 | 4.3 | -0.95 | – | -1.88 |
| 213 | `M147` Improved Three-Bar Pullback | **39.1** | 22 | 29 | 33 | 16 | BELUM CUKUP | 16 | 100/35 | -4.34 | 22 | -5.34 | -0.55 | 4.9 | -1.97 | – | -1.37 |
| 214 | `M03` BB Break + Divergence RSI | **38.9** | 23 | 31 | 48 | 15 | BELUM CUKUP | 22 | 429/335 | -1.55 | 22 | -6.46 | -0.74 | 3.5 | -0.73 | – | -2.74 |
| 215 | `M161` EMA 10/21 + Supertrend (10,3) | **38.1** | 34 | 15 | 51 | 15 | BELUM CUKUP | 22 | 484/237 | -0.80 | 22 | -11.10 | -0.80 | 9.3 | -0.35 | – | -0.69 |
| 216 | `M101` Bulkowski: Tiga lembah menaik | **38.1** | 19 | 19 | 46 | 15 | BELUM CUKUP | 16 | 45/21 | -3.47 | 22 | -7.91 | -0.62 | 7.4 | -0.26 | – | -0.73 |
| 217 | `M154` HOLP (High of Low Period) | **36.9** | 15 | 19 | 41 | 15 | BELUM CUKUP | 16 | 87/33 | -3.27 | 22 | -10.47 | -0.81 | 7.3 | -0.98 | – | -4.34 |
| 218 | `M82` Arthur Hill Rotasi Sasaran 10% | **36.4** | 26 | 14 | 49 | 15 | BELUM CUKUP | 22 | 586/229 | -1.48 | 22 | -7.96 | -0.49 | 9.5 | -0.62 | – | -2.14 |
| 219 | `M79` Radge: 20% Flipper | **36.0** | 17 | 24 | 42 | 15 | BELUM CUKUP | 22 | 384/104 | -4.29 | 22 | -8.26 | -0.70 | 5.8 | -1.43 | – | -2.73 |
| 220 | `M123` CCI Correction (Lambert, Chart | **35.6** | 17 | 26 | 32 | 15 | BELUM CUKUP | 22 | 189/168 | -1.73 | 22 | -10.80 | -1.00 | 6.8 | -2.57 | – | -4.84 |
| 221 | `M47` Holy Grail Raschke | **35.6** | 10 | 18 | 30 | 15 | BELUM CUKUP | 15 | 33/25 | -2.93 | 22 | -9.46 | -0.91 | 6.4 | -2.15 | – | -20.51 |
| 222 | `M122` Moving Momentum (ChartSchool) | **34.3** | 15 | 19 | 34 | 15 | BELUM CUKUP | 22 | 111/62 | -4.28 | 22 | -11.54 | -1.00 | 6.0 | -2.18 | – | -6.28 |
| 223 | `M81` Bensdorp Long Trend High Momen | **33.9** | 3 | 8 | 42 | 15 | BELUM CUKUP | 13 | 431/151 | -4.43 | 22 | -19.96 | -0.87 | 14.2 | -1.23 | – | -3.75 |
| 224 | `M76` Undercut & Rally pada Low Pent | **33.1** | 9 | 20 | 38 | 15 | BELUM CUKUP | 21 | 78/54 | -2.78 | 22 | -11.41 | -1.00 | 6.8 | -1.64 | – | -6.31 |
| 225 | `M09` Volumatic VIDYA Pivot Retest | **33.0** | 3 | 10 | 30 | 15 | BELUM CUKUP | 14 | 33/20 | -5.48 | 22 | -14.63 | -1.00 | 8.4 | -2.06 | – | -12.39 |
| 226 | `M90` Pring KST | **31.7** | 6 | 14 | 43 | 15 | BELUM CUKUP | 21 | 86/43 | -3.45 | 22 | -13.53 | -0.74 | 11.5 | -1.00 | – | -4.32 |

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

