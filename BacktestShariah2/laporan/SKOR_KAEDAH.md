# Skor Kaedah 0–100 (pangkat maklumat, BUKAN keputusan)

> **Status keputusan (kad skor, harga 2026-11-17):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana 2026-11-18 oleh `standard/skor_kaedah.py` (Actions `analisis.yml`, selepas kad skor). Harga pada tutup 2026-11-17; 226 kaedah; 23 hari beli langsung (rejim ON 1, OFF 22). Pradaftar 2026-11-09: `standard/SPEC_SKOR_KAEDAH.md` (berat dan sauh dikunci `ujian/test_skor_kaedah.py::TestKunci`). Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Cara membaca

- **Skor** = min geometri berberat empat tiang (Untung 35 · Tahan 30 · Bukti 25 · Konsisten 10), dikecut ke 50 mengikut data: berat data = hari beli ÷ (hari beli + 20). Kaedah dengan 2 hari beli tidak boleh menjauhi 50. 100 = unggul semua segi; 50 = neutral/tiada bukti; < 50 = lebih buruk daripada neutral.
- **Siling** ikut kad skor: NEGATIF ≤ 20, GANTUNG/BERSARA ≤ 30, GAGAL ≤ 40. Tanda ⌈ = siling terpakai.
- **Satu-satunya status yang membenarkan wang sebenar ialah TERBUKTI dalam `laporan/KAD_SKOR.md`.** Skor tinggi dengan status BELUM CUKUP bermaksud "paling menjanjikan setakat ini", bukan "selamat".
- Deflasi ujian berganda (López de Prado): sauh t Bukti C1 = maks(2.0, E[maks 226 normal]) = 2.81.
- **Semakan kebolehramalan:** skor pada 2026-11-10 lawan pulangan lorong T4 sejak itu, 223 kaedah: Spearman ρ = -0.098 (p = 0.145). Belum ada bukti skor meramal pangkat; jangan pilih kaedah dengannya.
- Metrik T4 (A2, B1, B2, D1) dikira atas lorong T4 L1 **dipotong pada sesi LANGSUNG pertama** kaedah itu (Mxx 2026-10-16, Nxx/GB 2026-11-03) dan diasas semula; sesi isian bina semula tidak dikira (pindaan 9 Nov 2026 (a)). Lajur "T4 sesi/pul" di bawah ialah potongan itu, bukan lorong penuh `T4_KAEDAH.md`.

## Semua kaedah, susun ikut Skor

| # | Kaedah | Skor | Untung | Tahan | Bukti | Konsisten | Status kad | Hari beli | Posisi/tutup | Jangkaan % | T4 sesi | T4 pul % | T4 pul/|MDD| | Ulcer | t buku | Lift | WFE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `M146` 3-Bar Momentum Pattern | **59.2** | 69 | 74 | 58 | 85 | BELUM CUKUP | 19 | 79/34 | +0.16 | 23 | +4.81 | +0.78 | 2.6 | +0.87 | – | 1.71 |
| 2 | `M151` Outside Bar Failure | **56.8** | 60 | 79 | 53 | 57 | BELUM CUKUP | 22 | 111/60 | -0.75 | 23 | +7.27 | +4.51 | 0.6 | +0.04 | – | 0.08 |
| 3 | `M133` Bull Hook (Crabel) | **56.0** | 59 | 68 | 58 | 85 | BELUM CUKUP | 16 | 55/36 | -0.56 | 23 | +2.65 | +0.54 | 1.8 | +0.96 | – | 8.61 |
| 4 | `M118` Expansion Pivot (Cooper) | **54.7** | 51 | 72 | 52 | 80 | BELUM CUKUP | 20 | 85/26 | -1.00 | 23 | +6.65 | +1.46 | 1.6 | +0.27 | – | 0.84 |
| 5 | `M25` VWAP Wave (proksi harian) | **54.3** | 56 | 61 | 56 | 64 | BELUM CUKUP | 21 | 192/113 | -0.89 | 23 | +2.86 | +0.47 | 3.4 | +0.24 | – | 1.36 |
| 6 | `M48` Cooper 1-2-3-4 | **53.3** | 53 | 60 | 51 | 79 | BELUM CUKUP | 19 | 64/20 | -1.21 | 23 | +6.48 | +1.19 | 2.2 | +0.34 | – | 0.80 |
| 7 | `M70` Pecahan Hari Dalam | **52.1** | 61 | 68 | 51 | 21 | BELUM CUKUP | 23 | 496/412 | -0.75 | 23 | +2.47 | +0.52 | 2.2 | -0.38 | – | -0.91 |
| 8 | `M159` Heikin-Ashi Trend | **52.0** | 54 | 61 | 46 | 55 | BELUM CUKUP | 23 | 1849/1657 | -0.84 | 23 | +3.76 | +0.61 | 3.5 | -1.01 | – | -5.62 |
| 9 | `M74` Lulus Baharu Trend Template Mi | **51.8** | 53 | 56 | 51 | 52 | BELUM CUKUP | 23 | 102/65 | -1.19 | 23 | +0.61 | +0.12 | 2.7 | -0.20 | – | -0.33 |
| 10 | `M160` Measured Move Up | **51.7** | 40 | 58 | 59 | 85 | BELUM CUKUP | 21 | 120/65 | -1.77 | 23 | +1.01 | +0.22 | 2.2 | +0.76 | – | 5.41 |
| 11 | `M100` Bulkowski Segi Empat & Segi Ti | **51.4** | 56 | 53 | 50 | 55 | BELUM CUKUP | 15 | 60/41 | -0.58 | 23 | +0.36 | +0.08 | 2.4 | -0.03 | – | -0.15 |
| 12 | `M104` High Tight Flag / Power Play | **51.1** | 85 | 90 | 44 | 85 | BELUM CUKUP | 1 | 1/0 | +21.63 | 8 | +2.18 | +10.00 | 0.0 | +1.99 | – | 14.74 |
| 13 | `M23` Breitstein Kapitulasi + Kesina | **50.1** | 51 | 47 | 56 | 46 | BELUM CUKUP | 21 | 127/86 | -1.04 | 23 | -2.31 | -0.40 | 2.7 | +0.32 | – | 1.21 |
| 14 | `M13` Garis Trend Action/Safety Line | **50.1** | 40 | 68 | 46 | 55 | BELUM CUKUP | 23 | 809/549 | -2.07 | 23 | +6.92 | +1.94 | 1.4 | -0.92 | – | -2.24 |
| 15 | `M46` Jurang Naik Boleh Beli (Buyabl | **49.9** | 44 | 60 | 46 | 55 | BELUM CUKUP | 13 | 36/22 | -1.38 | 23 | +0.88 | +0.18 | 1.6 | -0.12 | – | -0.18 |
| 16 | `M33` Supertrend + SMA10 | **49.7** | 35 | 64 | 53 | 67 | BELUM CUKUP | 21 | 221/60 | -1.96 | 23 | +5.95 | +1.43 | 1.7 | +0.08 | – | 0.40 |
| 17 | `M07` Qullamaggie Breakout | **49.3** | 33 | 64 | 27 | 15 | BELUM CUKUP | 1 | 1/1 | -2.53 | 23 | -0.25 | -0.21 | 0.8 | -0.22 | – | -1.12 |
| 18 | `M10` EMA3 + CCI + MACD | **49.0** | 38 | 60 | 50 | 55 | BELUM CUKUP | 21 | 126/64 | -2.59 | 23 | +8.79 | +1.67 | 2.2 | -0.35 | – | -1.07 |
| 19 | `M145` Yum-Yum Continuation | **48.9** | 35 | 64 | 50 | 55 | BELUM CUKUP | 22 | 309/73 | -2.26 | 23 | +3.29 | +1.51 | 1.2 | -0.36 | – | -0.31 |
| 20 | `M77` Undercut & Rally pada Purata B | **48.9** | 48 | 48 | 44 | 55 | BELUM CUKUP | 17 | 54/37 | -1.04 | 23 | -1.39 | -0.36 | 1.8 | -0.66 | – | -0.88 |
| 21 | `M51` O'Neil Cawan & Pemegang | **48.9** | 32 | 48 | 34 | 45 | BELUM CUKUP | 2 | 3/1 | -1.87 | 13 | -0.52 | -0.52 | 0.6 | +0.33 | – | 1.08 |
| 22 | `M45` High 52 Minggu (George & Hwang | **48.9** | 22 | 40 | 28 | 15 | BELUM CUKUP | 1 | 2/1 | -5.27 | 12 | -1.03 | -0.57 | 1.0 | -0.14 | – | -0.45 |
| 23 | `N53X36` Supertrend + ADX>25 → keluar s | **48.7** | 54 | 42 | 47 | 33 | BELUM CUKUP | 10 | 136/37 | -0.64 | 10 | -1.68 | -0.42 | 2.4 | +0.12 | – | – |
| 24 | `M27` Price Action 4 Tiang | **48.6** | 41 | 35 | 38 | 15 | BELUM CUKUP | 2 | 546/462 | -1.32 | 23 | -3.28 | -0.64 | 2.9 | -0.94 | – | -3.13 |
| 25 | `N45X16` Undur EMA21 cerun positif → ke | **48.5** | 32 | 66 | 41 | 70 | BELUM CUKUP | 10 | 161/77 | -2.31 | 10 | +3.58 | +1.08 | 1.4 | -0.85 | – | – |
| 26 | `M84` Jarak purata bergerak MAD 21/2 | **48.5** | 22 | 11 | 30 | 15 | BELUM CUKUP | 1 | 58/40 | -4.71 | 12 | -8.00 | -1.00 | 6.5 | -1.08 | – | -3.11 |
| 27 | `M137` Livermore System | **48.4** | 37 | 56 | 51 | 55 | BELUM CUKUP | 23 | 177/71 | -2.32 | 23 | +3.38 | +0.57 | 2.2 | -0.25 | – | -0.49 |
| 28 | `M129` Wick Play | **48.4** | 37 | 55 | 42 | 55 | BELUM CUKUP | 10 | 26/10 | -2.40 | 23 | +2.50 | +0.74 | 1.3 | -0.14 | – | -0.52 |
| 29 | `M94` Pecutan Momentum (Chen, Yu & W | **48.3** | 17 | 8 | 15 | 15 | BELUM CUKUP | 1 | 33/0 | -10.56 | 12 | -9.95 | -0.84 | 7.3 | -1.34 | – | -4.32 |
| 30 | `M96` Momo India: Ranking Sharpe 3/6 | **48.2** | 20 | 9 | 9 | 15 | BELUM CUKUP | 1 | 6/6 | -13.40 | 12 | -7.68 | -1.00 | 6.4 | -5.74 | – | -15.35 |
| 31 | `M93` Bollinger Kaedah II: %b + MFI | **48.1** | 53 | 40 | 55 | 30 | BELUM CUKUP | 23 | 271/83 | -0.67 | 23 | -1.02 | -0.16 | 3.1 | +0.15 | – | 0.20 |
| 32 | `M132` Ascending Scallop (Bulkowski) | **48.0** | 33 | 59 | 48 | 55 | BELUM CUKUP | 17 | 94/38 | -2.69 | 23 | +2.44 | +0.65 | 2.3 | -0.25 | – | -1.73 |
| 33 | `M158` Doubly Adaptive Profit Targets | **47.9** | 49 | 36 | 58 | 43 | BELUM CUKUP | 23 | 382/142 | -0.72 | 23 | -3.50 | -0.47 | 3.6 | +0.39 | – | 0.93 |
| 34 | `M39` Radge Pecahan Bollinger 100 ha | **47.9** | 33 | 62 | 47 | 55 | BELUM CUKUP | 21 | 240/53 | -3.57 | 23 | +5.54 | +2.31 | 1.2 | -0.56 | – | -1.13 |
| 35 | `N75X17` RSI14 < 40 tanpa penapis → kel | **47.6** | 40 | 42 | 39 | 70 | BELUM CUKUP | 10 | 330/161 | -1.06 | 10 | -2.79 | -0.45 | 3.0 | -1.17 | – | – |
| 36 | `N25X36` Supertrend + EMA + ADX>23 → ke | **47.6** | 36 | 49 | 37 | 70 | BELUM CUKUP | 9 | 133/35 | -2.00 | 10 | -0.57 | -0.13 | 2.1 | -0.98 | – | – |
| 37 | `M78` Alvarez Pecahan Mingguan DTAYS | **47.6** | 20 | 21 | 38 | 15 | BELUM CUKUP | 2 | 73/42 | -3.10 | 22 | -8.60 | -0.78 | 7.4 | -0.40 | – | -1.30 |
| 38 | `M05` MACD Divergence + Pengesahan | **47.5** | 39 | 52 | 40 | 55 | BELUM CUKUP | 15 | 41/12 | -2.31 | 23 | +0.30 | +0.07 | 1.8 | -0.73 | – | -1.24 |
| 39 | `M37` Weinstein Peringkat 2 | **47.5** | 25 | 48 | 21 | 37 | BELUM CUKUP | 3 | 7/0 | -1.88 | 17 | -1.17 | -0.53 | 0.7 | -0.95 | – | -1.10 |
| 40 | `M35` Pocket Pivot Morales & Kacher | **47.1** | 58 | 40 | 54 | 15 | BELUM CUKUP | 22 | 315/248 | -0.40 | 23 | -3.83 | -0.42 | 5.3 | -0.07 | – | -0.34 |
| 41 | `N203X36` Gap 2% lalu MA20 silang MA50 x | **47.1** | 21 | 42 | 21 | 50 | BELUM CUKUP | 3 | 11/0 | -1.89 | 3 | -1.86 | -0.76 | 1.6 | -1.01 | – | – |
| 42 | `N202X36` RSI2<10 dalam trend naik x X36 | **47.1** | 39 | 55 | 6 | 50 | BELUM CUKUP | 3 | 37/0 | -1.29 | 3 | -0.33 | -0.25 | 0.8 | -2.76 | – | – |
| 43 | `N36X36` Pocket pivot → keluar selepas  | **46.7** | 36 | 43 | 35 | 70 | BELUM CUKUP | 10 | 154/76 | -3.04 | 10 | +1.56 | +0.27 | 2.5 | -1.60 | – | – |
| 44 | `M64` O'Neil Tiga Minggu Ketat | **46.6** | 28 | 22 | 25 | 15 | BELUM CUKUP | 3 | 3/3 | -12.60 | 23 | -3.76 | -0.84 | 2.7 | -1.26 | – | -14.58 |
| 45 | `N48X36` Inside day pecah → keluar sele | **46.4** | 38 | 34 | 38 | 70 | BELUM CUKUP | 10 | 325/222 | -0.81 | 10 | -4.33 | -0.51 | 5.2 | -1.27 | – | – |
| 46 | `M21` Marius 3 Persediaan (Pecahan+J | **46.3** | 25 | 45 | 37 | 16 | BELUM CUKUP | 5 | 5/4 | -3.12 | 15 | -1.54 | -0.62 | 1.5 | +0.02 | – | 0.03 |
| 47 | `N201X36` MA20 silang MA50 atas MA50 x X | **46.3** | 29 | 38 | 5 | 50 | BELUM CUKUP | 3 | 21/0 | -1.96 | 3 | -1.53 | -0.97 | 1.2 | -5.45 | – | – |
| 48 | `M124` 'Last' Stochastic Technique (C | **46.1** | 34 | 46 | 50 | 55 | BELUM CUKUP | 23 | 408/237 | -2.30 | 23 | -0.31 | -0.05 | 2.7 | -0.52 | – | -1.39 |
| 49 | `M148` Natural Number Method | **46.1** | 36 | 51 | 40 | 55 | BELUM CUKUP | 23 | 226/190 | -2.53 | 23 | +0.71 | +0.12 | 3.0 | -1.70 | – | -5.68 |
| 50 | `N28X36` ADX>25 + DI+ > DI- → keluar se | **46.1** | 42 | 29 | 42 | 50 | BELUM CUKUP | 10 | 367/245 | -0.67 | 10 | -6.01 | -0.96 | 4.1 | -0.90 | – | – |
| 51 | `M138` 直升机空中加油 (Helikopter isi minyak | **46.1** | 31 | 41 | 15 | 15 | BELUM CUKUP | 4 | 4/0 | -3.30 | 16 | -1.24 | -0.87 | 0.6 | -1.74 | – | -2.73 |
| 52 | `N19X13` Bawah jalur BB + RSI<30 → kelu | **45.9** | 30 | 34 | 25 | 68 | BELUM CUKUP | 6 | 102/0 | -1.50 | 10 | -2.68 | -0.68 | 2.5 | -0.77 | – | – |
| 53 | `M157` Consolidation Pivot Breakout ( | **45.9** | 32 | 35 | 29 | 15 | BELUM CUKUP | 5 | 7/3 | -3.14 | 20 | -2.12 | -0.72 | 1.7 | -0.84 | – | -2.10 |
| 54 | `N41X36` CMF20>0 + tutup>EMA20 → keluar | **45.7** | 31 | 40 | 34 | 70 | BELUM CUKUP | 10 | 248/165 | -2.21 | 10 | -2.34 | -0.47 | 2.7 | -1.75 | – | – |
| 55 | `M111` Sistem Volatiliti Wilder | **45.5** | 34 | 42 | 52 | 48 | BELUM CUKUP | 23 | 271/107 | -2.27 | 23 | +0.40 | +0.06 | 3.8 | -0.25 | – | -0.70 |
| 56 | `M02` MACD + SMA200 | **45.4** | 39 | 38 | 44 | 55 | BELUM CUKUP | 23 | 132/92 | -3.53 | 23 | +1.48 | +0.15 | 3.5 | -1.14 | – | -7.80 |
| 57 | `N08X36` tutup>EMA20 tidak terlalu jauh | **45.4** | 28 | 41 | 34 | 70 | BELUM CUKUP | 10 | 403/282 | -1.97 | 10 | -2.43 | -0.44 | 2.7 | -1.84 | – | – |
| 58 | `N28X16` ADX>25 + DI+ > DI- → keluar bi | **45.3** | 30 | 38 | 33 | 70 | BELUM CUKUP | 10 | 386/258 | -1.35 | 10 | -3.47 | -0.55 | 3.5 | -1.90 | – | – |
| 59 | `M08` SMA20 + SMA200 | **45.1** | 37 | 35 | 49 | 55 | BELUM CUKUP | 21 | 218/129 | -1.62 | 23 | -3.84 | -0.72 | 3.6 | -0.61 | – | -1.58 |
| 60 | `M153` Range Leader | **45.0** | 51 | 36 | 52 | 15 | BELUM CUKUP | 23 | 1354/1234 | -0.34 | 23 | -5.00 | -0.45 | 7.0 | -0.31 | – | -1.82 |
| 61 | `M88` O'Neil Shakeout +3 | **44.8** | 30 | 42 | 45 | 51 | BELUM CUKUP | 17 | 75/40 | -3.86 | 23 | -1.76 | -0.14 | 5.6 | -0.59 | – | -1.09 |
| 62 | `N36X16` Pocket pivot → keluar bila sup | **44.8** | 30 | 34 | 35 | 57 | BELUM CUKUP | 10 | 157/66 | -3.14 | 10 | -0.93 | -0.20 | 2.3 | -1.55 | – | – |
| 63 | `N42X36` Lonjakan volum 2x → keluar sel | **44.7** | 34 | 26 | 40 | 56 | BELUM CUKUP | 10 | 198/106 | -1.24 | 10 | -5.72 | -0.77 | 4.3 | -1.06 | – | – |
| 64 | `N75X14` RSI14 < 40 tanpa penapis → kel | **44.7** | 34 | 26 | 37 | 60 | BELUM CUKUP | 10 | 224/47 | -1.25 | 10 | -5.33 | -0.97 | 3.5 | -1.12 | – | – |
| 65 | `M38` Darvas Kotak | **44.7** | 19 | 26 | 33 | 15 | BELUM CUKUP | 5 | 26/1 | -4.08 | 22 | -4.22 | -0.42 | 5.5 | -0.05 | – | -0.21 |
| 66 | `M41` FW Penyatuan Mingguan | **44.6** | 19 | 22 | 39 | 15 | BELUM CUKUP | 5 | 67/9 | -2.24 | 22 | -7.11 | -0.74 | 5.2 | -0.02 | – | -0.04 |
| 67 | `N07X16` Tiga MA tersusun → keluar bila | **44.5** | 26 | 42 | 32 | 44 | BELUM CUKUP | 10 | 155/25 | -3.39 | 10 | -0.69 | -0.17 | 2.0 | -1.47 | – | – |
| 68 | `M15` Break & Retest + Henti ATR | **44.4** | 48 | 35 | 52 | 15 | BELUM CUKUP | 23 | 311/217 | -0.64 | 23 | -6.19 | -0.62 | 4.8 | -0.28 | – | -0.66 |
| 69 | `N24X36` Supertrend(10,3) + ADX>20 → ke | **44.4** | 32 | 26 | 38 | 63 | BELUM CUKUP | 10 | 164/65 | -2.46 | 10 | -3.45 | -0.76 | 2.7 | -1.17 | – | – |
| 70 | `M117` Landry Pullback (high 2 bulan) | **44.3** | 43 | 31 | 52 | 25 | BELUM CUKUP | 20 | 157/22 | -0.92 | 23 | -7.26 | -0.79 | 4.8 | +0.32 | – | 0.34 |
| 71 | `M142` Pecahan volum dari dasar (底部放量 | **44.3** | 28 | 43 | 40 | 55 | BELUM CUKUP | 16 | 54/7 | -1.92 | 21 | +1.29 | +0.27 | 2.2 | -0.22 | – | -0.39 |
| 72 | `N43X36` Undur EMA8 + penapis MA50 → ke | **44.3** | 32 | 29 | 34 | 51 | BELUM CUKUP | 10 | 185/38 | -2.90 | 10 | -3.18 | -0.76 | 2.5 | -1.44 | – | – |
| 73 | `M144` Screw Bar | **44.3** | 28 | 31 | 32 | 15 | BELUM CUKUP | 7 | 10/7 | -2.72 | 21 | -2.64 | -0.87 | 1.3 | -0.89 | – | -1.75 |
| 74 | `M18` EMA9/21 Pullback | **44.2** | 50 | 32 | 51 | 15 | BELUM CUKUP | 23 | 413/318 | -0.67 | 23 | -6.48 | -1.00 | 4.2 | -0.37 | – | -1.30 |
| 75 | `N37X36` Gap and go → keluar selepas DU | **44.2** | 23 | 25 | 31 | 57 | BELUM CUKUP | 7 | 83/26 | -3.66 | 10 | -2.27 | -0.45 | 3.0 | -1.49 | – | – |
| 76 | `M92` CCI-50 | **44.1** | 44 | 39 | 49 | 15 | BELUM CUKUP | 23 | 570/402 | -1.01 | 23 | -3.85 | -0.45 | 3.6 | -0.58 | – | -1.15 |
| 77 | `M80` Radge Saluran Purata Bergerak  | **44.1** | 41 | 35 | 54 | 20 | BELUM CUKUP | 23 | 304/68 | -1.24 | 23 | -2.84 | -0.36 | 4.5 | +0.11 | – | 0.15 |
| 78 | `N68X36` Bullish engulfing + EMA21 → ke | **44.1** | 26 | 37 | 36 | 30 | BELUM CUKUP | 10 | 85/21 | -2.90 | 10 | -2.59 | -0.42 | 3.3 | -0.88 | – | – |
| 79 | `N37X17` Gap and go → keluar bila adx14 | **44.1** | 22 | 25 | 30 | 55 | BELUM CUKUP | 7 | 83/31 | -3.65 | 10 | -2.43 | -0.44 | 3.0 | -1.61 | – | – |
| 80 | `N33X16` Donchian20 + penapis MA200 → k | **44.0** | 26 | 34 | 25 | 70 | BELUM CUKUP | 9 | 102/15 | -5.28 | 10 | -1.41 | -0.40 | 1.7 | -2.08 | – | – |
| 81 | `M89` Chande 65sma-3cc | **43.9** | 33 | 42 | 50 | 27 | BELUM CUKUP | 23 | 194/94 | -2.62 | 23 | -1.21 | -0.13 | 3.9 | -0.51 | – | -1.64 |
| 82 | `N64X36` Episodic pivot → keluar selepa | **43.9** | 22 | 22 | 31 | 58 | BELUM CUKUP | 7 | 49/7 | -2.63 | 10 | -2.97 | -0.60 | 2.7 | -0.93 | – | – |
| 83 | `M120` Reversal New Highs | **43.8** | 37 | 35 | 42 | 15 | BELUM CUKUP | 13 | 19/12 | -1.94 | 23 | -2.97 | -0.45 | 3.3 | -0.43 | – | -2.37 |
| 84 | `N25X16` Supertrend + EMA + ADX>23 → ke | **43.8** | 25 | 36 | 27 | 46 | BELUM CUKUP | 9 | 119/7 | -3.70 | 10 | -2.63 | -0.55 | 2.7 | -1.56 | – | – |
| 85 | `N64X17` Episodic pivot → keluar bila a | **43.8** | 22 | 22 | 32 | 51 | BELUM CUKUP | 7 | 49/13 | -2.85 | 10 | -3.27 | -0.64 | 2.7 | -1.09 | – | – |
| 86 | `M102` Stockbee SLTB | **43.7** | 41 | 40 | 48 | 15 | BELUM CUKUP | 23 | 410/312 | -1.63 | 23 | -3.28 | -0.31 | 5.7 | -0.69 | – | -1.78 |
| 87 | `N22X36` BB pecah atas + RSI → keluar s | **43.7** | 25 | 32 | 41 | 30 | BELUM CUKUP | 10 | 118/51 | -3.90 | 10 | -2.80 | -0.59 | 2.9 | -0.75 | – | – |
| 88 | `M87` IBD Tapak Menaik | **43.7** | 26 | 30 | 35 | 15 | BELUM CUKUP | 8 | 11/7 | -5.06 | 23 | -5.52 | -0.70 | 4.2 | -0.75 | – | -2.56 |
| 89 | `M115` Bow Tie (Landry) | **43.6** | 30 | 35 | 47 | 15 | BELUM CUKUP | 12 | 37/27 | -2.47 | 23 | -5.20 | -0.59 | 4.8 | -0.10 | – | -0.55 |
| 90 | `N76X36` Tutup > MA50 (penapis trend tu | **43.6** | 30 | 28 | 35 | 34 | BELUM CUKUP | 10 | 182/79 | -2.73 | 10 | -4.87 | -0.89 | 4.0 | -1.58 | – | – |
| 91 | `N76X16` Tutup > MA50 (penapis trend tu | **43.5** | 21 | 36 | 29 | 70 | BELUM CUKUP | 10 | 306/190 | -2.90 | 10 | -1.65 | -0.48 | 1.6 | -2.34 | – | – |
| 92 | `M49` Ichimoku (Tutup Atas Awan + Te | **43.4** | 37 | 45 | 45 | 15 | BELUM CUKUP | 23 | 311/185 | -2.43 | 23 | +0.20 | +0.03 | 3.5 | -1.13 | – | -1.65 |
| 93 | `N09X36` Undur EMA10 + penapis EMA50 →  | **43.4** | 30 | 26 | 34 | 35 | BELUM CUKUP | 10 | 196/58 | -3.01 | 10 | -3.73 | -0.89 | 2.5 | -1.51 | – | – |
| 94 | `N25X17` Supertrend + EMA + ADX>23 → ke | **43.4** | 22 | 34 | 28 | 45 | BELUM CUKUP | 9 | 115/11 | -3.77 | 10 | -2.85 | -0.59 | 2.7 | -1.58 | – | – |
| 95 | `N124X36` Episodic pivot gap 8-10% → kel | **43.4** | 28 | 22 | 33 | 30 | BELUM CUKUP | 8 | 41/13 | -1.72 | 10 | -5.98 | -1.00 | 3.9 | -1.00 | – | – |
| 96 | `M54` IBD Power Trend | **43.3** | 34 | 41 | 48 | 18 | BELUM CUKUP | 21 | 216/115 | -2.36 | 23 | -0.84 | -0.08 | 5.4 | -0.74 | – | -1.59 |
| 97 | `M91` Stochastic Pop (Bernstein/Stec | **43.3** | 30 | 27 | 46 | 55 | BELUM CUKUP | 15 | 38/25 | -4.26 | 23 | -2.75 | -0.18 | 4.8 | -0.19 | – | -0.93 |
| 98 | `M44` Tapak Rata IBD | **43.3** | 30 | 36 | 19 | 15 | BELUM CUKUP | 8 | 9/6 | -4.88 | 23 | -4.29 | -0.85 | 3.1 | -2.56 | – | -33.07 |
| 99 | `N35X36` Pecah 52 minggu tinggi → kelua | **43.3** | 21 | 28 | 23 | 70 | BELUM CUKUP | 8 | 48/2 | -4.70 | 10 | -1.36 | -0.47 | 1.3 | -1.58 | – | – |
| 100 | `M131` Ross Hook (Joe Ross) | **43.2** | 34 | 42 | 52 | 15 | BELUM CUKUP | 23 | 267/128 | -1.84 | 23 | -2.38 | -0.34 | 3.6 | -0.28 | – | -0.66 |
| 101 | `M150` Trend Bar Failure (Brooks) | **43.2** | 43 | 34 | 47 | 15 | BELUM CUKUP | 21 | 107/53 | -1.04 | 23 | -5.94 | -0.82 | 3.5 | -0.62 | – | -2.07 |
| 102 | `M68` Kell Base n' Break | **43.2** | 32 | 40 | 44 | 15 | BELUM CUKUP | 15 | 47/13 | -3.50 | 23 | -1.00 | -0.21 | 2.2 | -0.25 | – | -1.57 |
| 103 | `N42X16` Lonjakan volum 2x → keluar bil | **43.2** | 32 | 21 | 41 | 30 | BELUM CUKUP | 10 | 202/100 | -1.24 | 10 | -6.54 | -1.00 | 4.6 | -1.00 | – | – |
| 104 | `N37X16` Gap and go → keluar bila super | **43.2** | 21 | 20 | 29 | 37 | BELUM CUKUP | 7 | 83/24 | -3.80 | 10 | -2.96 | -0.72 | 2.6 | -1.64 | – | – |
| 105 | `N41X16` CMF20>0 + tutup>EMA20 → keluar | **43.1** | 22 | 34 | 31 | 48 | BELUM CUKUP | 10 | 296/190 | -2.89 | 10 | -2.64 | -0.58 | 2.2 | -2.18 | – | – |
| 106 | `N45X36` Undur EMA21 cerun positif → ke | **43.1** | 25 | 31 | 34 | 30 | BELUM CUKUP | 10 | 133/48 | -3.39 | 10 | -1.86 | -0.48 | 1.9 | -1.46 | – | – |
| 107 | `N08X16` tutup>EMA20 tidak terlalu jauh | **43.1** | 22 | 29 | 31 | 70 | BELUM CUKUP | 10 | 468/333 | -2.23 | 10 | -3.15 | -0.95 | 2.2 | -2.10 | – | – |
| 108 | `M121` High 2 bull flag (Brooks) | **43.1** | 14 | 14 | 20 | 15 | BELUM CUKUP | 5 | 7/4 | -10.63 | 19 | -7.34 | -0.86 | 5.3 | -1.90 | – | -21.57 |
| 109 | `N40X16` OBV tinggi baharu + MA50 → kel | **43.0** | 32 | 18 | 44 | 30 | BELUM CUKUP | 10 | 89/34 | -1.24 | 10 | -10.68 | -0.91 | 4.5 | -0.22 | – | – |
| 110 | `N64X14` Episodic pivot → keluar bila r | **43.0** | 22 | 17 | 29 | 37 | BELUM CUKUP | 7 | 49/3 | -2.75 | 10 | -3.61 | -0.90 | 2.3 | -0.93 | – | – |
| 111 | `M116` 2/20 EMA Breakout (Landry) | **42.9** | 42 | 33 | 50 | 15 | BELUM CUKUP | 23 | 591/457 | -1.06 | 23 | -2.10 | -0.17 | 7.7 | -0.50 | – | -2.35 |
| 112 | `M139` 均线首次粘合向上发散 (MA berhimpun kali  | **42.9** | 29 | 38 | 45 | 42 | BELUM CUKUP | 22 | 89/33 | -3.78 | 23 | -1.36 | -0.15 | 3.7 | -0.64 | – | -2.22 |
| 113 | `N113X16` 80-20 bar (sisi beli) → keluar | **42.9** | 37 | 16 | 39 | 30 | BELUM CUKUP | 10 | 327/240 | -0.57 | 10 | -9.94 | -1.00 | 7.5 | -1.20 | – | – |
| 114 | `N51X36` BB squeeze + Supertrend → kelu | **42.9** | 16 | 33 | 20 | 30 | BELUM CUKUP | 7 | 12/3 | -4.01 | 10 | -4.59 | -0.90 | 2.6 | -2.00 | – | – |
| 115 | `N64X16` Episodic pivot → keluar bila s | **42.9** | 20 | 17 | 31 | 37 | BELUM CUKUP | 7 | 49/6 | -2.57 | 10 | -3.61 | -0.90 | 2.3 | -0.96 | – | – |
| 116 | `N65X14` Gap 4% + volum + hampir 52w →  | **42.9** | 19 | 14 | 22 | 30 | BELUM CUKUP | 6 | 31/1 | -4.79 | 10 | -4.92 | -1.00 | 2.8 | -1.43 | – | – |
| 117 | `N65X36` Gap 4% + volum + hampir 52w →  | **42.8** | 19 | 14 | 22 | 30 | BELUM CUKUP | 6 | 31/1 | -4.87 | 10 | -4.90 | -1.00 | 2.9 | -1.43 | – | – |
| 118 | `M134` First Kiss After Daylight (Lan | **42.7** | 33 | 38 | 47 | 15 | BELUM CUKUP | 18 | 62/23 | -2.49 | 23 | -3.79 | -0.45 | 4.3 | -0.17 | – | -0.22 |
| 119 | `N51X16` BB squeeze + Supertrend → kelu | **42.6** | 16 | 33 | 18 | 30 | BELUM CUKUP | 7 | 12/1 | -4.30 | 10 | -4.89 | -0.91 | 2.8 | -1.99 | – | – |
| 120 | `N07X36` Tiga MA tersusun → keluar sele | **42.5** | 24 | 29 | 30 | 30 | BELUM CUKUP | 10 | 155/15 | -3.80 | 10 | -2.54 | -0.64 | 2.8 | -1.52 | – | – |
| 121 | `N40X36` OBV tinggi baharu + MA50 → kel | **42.5** | 28 | 18 | 42 | 30 | BELUM CUKUP | 10 | 73/18 | -1.59 | 10 | -10.67 | -0.85 | 4.8 | -0.13 | – | – |
| 122 | `N36X14` Pocket pivot → keluar bila rsi | **42.5** | 25 | 21 | 30 | 70 | BELUM CUKUP | 10 | 153/24 | -4.09 | 10 | -4.18 | -0.57 | 4.0 | -1.68 | – | – |
| 123 | `M128` Inventory Retracement Bar (IRB | **42.4** | 40 | 30 | 52 | 15 | BELUM CUKUP | 22 | 156/91 | -1.15 | 23 | -4.97 | -0.45 | 6.8 | -0.26 | – | -1.16 |
| 124 | `N37X14` Gap and go → keluar bila rsi14 | **42.4** | 18 | 18 | 25 | 30 | BELUM CUKUP | 7 | 82/8 | -4.61 | 10 | -4.94 | -0.76 | 3.7 | -1.69 | – | – |
| 125 | `M12` Parabolic SAR | **42.3** | 32 | 37 | 48 | 22 | BELUM CUKUP | 23 | 389/217 | -2.59 | 23 | -2.45 | -0.42 | 3.0 | -0.76 | – | -1.74 |
| 126 | `M30` BB Free Bar + Himpitan 50/2.5 | **42.3** | 31 | 33 | 53 | 20 | BELUM CUKUP | 20 | 229/83 | -1.94 | 23 | -0.99 | -0.12 | 5.0 | -0.01 | – | -0.01 |
| 127 | `N42X15` Lonjakan volum 2x → ekori Chan | **42.3** | 22 | 27 | 25 | 70 | BELUM CUKUP | 10 | 170/0 | -2.50 | 10 | -6.30 | -0.55 | 5.7 | -1.00 | – | – |
| 128 | `N50X14` Mampat + pecah volum 1.5x → ke | **42.3** | 13 | 22 | 26 | 38 | BELUM CUKUP | 7 | 17/3 | -5.64 | 10 | -7.04 | -0.76 | 4.9 | -1.25 | – | – |
| 129 | `N113X36` 80-20 bar (sisi beli) → keluar | **42.2** | 28 | 19 | 36 | 30 | BELUM CUKUP | 10 | 308/233 | -1.18 | 10 | -9.62 | -1.00 | 6.9 | -1.55 | – | – |
| 130 | `N68X16` Bullish engulfing + EMA21 → ke | **42.2** | 17 | 34 | 35 | 30 | BELUM CUKUP | 10 | 85/24 | -3.09 | 10 | -4.43 | -0.51 | 4.4 | -1.10 | – | – |
| 131 | `N38X36` VCP pecah → keluar selepas DUA | **42.1** | 25 | 31 | 22 | 30 | BELUM CUKUP | 10 | 33/12 | -3.39 | 10 | -3.72 | -0.98 | 2.2 | -2.32 | – | – |
| 132 | `M26` Garis Trend Undur 3 Sentuhan + | **42.0** | 35 | 34 | 44 | 15 | BELUM CUKUP | 19 | 76/51 | -1.13 | 23 | -5.09 | -0.64 | 3.9 | -0.85 | – | -1.14 |
| 133 | `N66X36` 52w tinggi + pengesahan 1% → k | **42.0** | 19 | 13 | 26 | 31 | BELUM CUKUP | 7 | 38/2 | -4.34 | 9 | -5.35 | -1.00 | 3.4 | -1.21 | – | – |
| 134 | `N50X17` Mampat + pecah volum 1.5x → ke | **42.0** | 12 | 20 | 27 | 38 | BELUM CUKUP | 7 | 16/3 | -6.24 | 10 | -7.85 | -0.85 | 5.3 | -1.21 | – | – |
| 135 | `M143` 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke | **41.9** | 22 | 40 | 30 | 38 | BELUM CUKUP | 14 | 28/3 | -2.92 | 22 | -2.02 | -0.53 | 1.8 | -1.08 | – | -9.63 |
| 136 | `N119X13` 3 tutup turun berturut → kelua | **41.9** | 17 | 25 | 32 | 70 | BELUM CUKUP | 10 | 231/56 | -2.35 | 10 | -6.50 | -0.79 | 6.0 | -1.73 | – | – |
| 137 | `N22X16` BB pecah atas + RSI → keluar b | **41.9** | 22 | 22 | 36 | 30 | BELUM CUKUP | 10 | 120/29 | -4.96 | 10 | -3.40 | -0.74 | 3.1 | -1.01 | – | – |
| 138 | `N33X36` Donchian20 + penapis MA200 → k | **41.9** | 22 | 21 | 29 | 30 | BELUM CUKUP | 9 | 98/30 | -4.57 | 10 | -4.33 | -1.00 | 2.5 | -1.85 | – | – |
| 139 | `N06X36` Golden cross MA50/MA200 → kelu | **41.8** | 18 | 30 | 24 | 30 | BELUM CUKUP | 9 | 23/2 | -3.30 | 10 | -4.70 | -1.00 | 2.9 | -1.51 | – | – |
| 140 | `N56X36` RSI>50 + ADX>20 → keluar selep | **41.7** | 21 | 22 | 32 | 36 | BELUM CUKUP | 10 | 198/91 | -2.54 | 10 | -6.81 | -0.93 | 5.6 | -1.99 | – | – |
| 141 | `N74X16` MACD atas garis isyarat (keada | **41.7** | 16 | 26 | 32 | 61 | BELUM CUKUP | 10 | 565/414 | -2.07 | 10 | -6.52 | -0.89 | 5.0 | -1.97 | – | – |
| 142 | `N75X13` RSI14 < 40 tanpa penapis → kel | **41.7** | 20 | 28 | 28 | 30 | BELUM CUKUP | 10 | 134/1 | -1.91 | 10 | -5.85 | -0.96 | 2.9 | -0.94 | – | – |
| 143 | `N53X16` Supertrend + ADX>25 → keluar b | **41.7** | 18 | 28 | 33 | 30 | BELUM CUKUP | 10 | 117/9 | -3.18 | 10 | -5.73 | -0.73 | 5.1 | -0.97 | – | – |
| 144 | `N53X17` Supertrend + ADX>25 → keluar b | **41.7** | 18 | 28 | 31 | 30 | BELUM CUKUP | 10 | 109/5 | -3.42 | 10 | -4.91 | -0.69 | 4.8 | -0.95 | – | – |
| 145 | `M20` EMA10/15 Crossover + Sudut | **41.6** | 36 | 35 | 43 | 15 | BELUM CUKUP | 23 | 493/415 | -1.62 | 23 | -5.00 | -0.71 | 3.4 | -1.30 | – | -8.35 |
| 146 | `M105` Supertrend tulen | **41.6** | 30 | 36 | 52 | 15 | BELUM CUKUP | 22 | 370/139 | -2.40 | 23 | -1.99 | -0.21 | 4.4 | -0.25 | – | -0.77 |
| 147 | `M32` Momentum Burst | **41.6** | 36 | 22 | 49 | 15 | BELUM CUKUP | 16 | 59/39 | -1.53 | 23 | -7.39 | -0.58 | 7.8 | -0.09 | – | -0.22 |
| 148 | `N27X16` Ichimoku atas awan → keluar bi | **41.6** | 22 | 24 | 29 | 30 | BELUM CUKUP | 10 | 168/84 | -2.62 | 10 | -3.77 | -1.00 | 2.4 | -2.29 | – | – |
| 149 | `N42X14` Lonjakan volum 2x → keluar bil | **41.6** | 20 | 19 | 34 | 50 | BELUM CUKUP | 10 | 181/16 | -2.46 | 10 | -7.95 | -0.72 | 5.8 | -1.02 | – | – |
| 150 | `N75X15` RSI14 < 40 tanpa penapis → eko | **41.6** | 21 | 28 | 26 | 30 | BELUM CUKUP | 10 | 133/0 | -1.89 | 10 | -5.85 | -0.96 | 2.9 | -0.92 | – | – |
| 151 | `M130` 多方炮 (dua lilin hijau mengapit  | **41.6** | 20 | 17 | 32 | 15 | BELUM CUKUP | 8 | 12/3 | -5.81 | 21 | -6.69 | -0.76 | 3.9 | -0.68 | – | -0.66 |
| 152 | `N124X15` Episodic pivot gap 8-10% → eko | **41.5** | 17 | 17 | 25 | 42 | BELUM CUKUP | 8 | 41/0 | -2.97 | 10 | -5.28 | -0.75 | 4.2 | -0.93 | – | – |
| 153 | `M106` DMI Wilder | **41.4** | 31 | 34 | 48 | 15 | BELUM CUKUP | 20 | 132/83 | -1.92 | 23 | -3.21 | -0.71 | 2.7 | -0.62 | – | -1.54 |
| 154 | `M127` Slingshot Bullish | **41.4** | 29 | 38 | 42 | 15 | BELUM CUKUP | 19 | 108/81 | -2.14 | 23 | -5.62 | -0.72 | 3.6 | -1.28 | – | -1.55 |
| 155 | `N57X36` ADX bangkit daripada <20 → kel | **41.4** | 19 | 24 | 22 | 30 | BELUM CUKUP | 9 | 75/7 | -5.87 | 10 | -2.58 | -0.53 | 2.6 | -2.18 | – | – |
| 156 | `N80X36` Tinggi sepanjang masa → keluar | **41.4** | 17 | 16 | 26 | 30 | BELUM CUKUP | 8 | 39/2 | -4.71 | 10 | -3.94 | -0.98 | 2.3 | -1.18 | – | – |
| 157 | `N119X15` 3 tutup turun berturut → ekori | **41.4** | 15 | 15 | 15 | 46 | BELUM CUKUP | 7 | 53/0 | -4.82 | 10 | -6.14 | -0.91 | 4.9 | -2.04 | – | – |
| 158 | `N16X13` RSI2<10 tanpa penapis → keluar | **41.3** | 16 | 24 | 29 | 57 | BELUM CUKUP | 10 | 188/5 | -2.51 | 10 | -7.45 | -0.83 | 6.0 | -1.26 | – | – |
| 159 | `N56X17` RSI>50 + ADX>20 → keluar bila  | **41.2** | 19 | 20 | 29 | 51 | BELUM CUKUP | 10 | 138/41 | -4.66 | 10 | -4.28 | -0.86 | 2.9 | -2.02 | – | – |
| 160 | `N73X13` Tutup bawah jalur bawah BB(20, | **41.2** | 18 | 26 | 27 | 30 | BELUM CUKUP | 10 | 151/1 | -2.13 | 10 | -6.58 | -0.88 | 4.3 | -1.03 | – | – |
| 161 | `N33X14` Donchian20 + penapis MA200 → k | **41.2** | 21 | 19 | 24 | 30 | BELUM CUKUP | 9 | 110/7 | -5.31 | 10 | -4.43 | -0.92 | 2.8 | -1.93 | – | – |
| 162 | `M119` 180 Bullish (Cooper) | **41.1** | 30 | 34 | 46 | 15 | BELUM CUKUP | 20 | 161/72 | -1.89 | 23 | -4.98 | -0.46 | 5.4 | -0.83 | – | -2.38 |
| 163 | `N24X17` Supertrend(10,3) + ADX>20 → ke | **41.1** | 18 | 19 | 27 | 30 | BELUM CUKUP | 9 | 124/30 | -4.90 | 10 | -4.60 | -0.91 | 2.7 | -2.05 | – | – |
| 164 | `M67` Rayner Teo: Ujian Ketiga pada  | **40.9** | 31 | 29 | 38 | 15 | BELUM CUKUP | 16 | 31/21 | -3.63 | 23 | -6.79 | -0.62 | 6.6 | -1.20 | – | -5.14 |
| 165 | `M126` Hidden Smash Day (beli, Larry  | **40.8** | 18 | 31 | 33 | 15 | BELUM CUKUP | 11 | 21/11 | -3.84 | 22 | -5.12 | -0.70 | 4.6 | -1.04 | – | -1.55 |
| 166 | `N57X16` ADX bangkit daripada <20 → kel | **40.8** | 19 | 24 | 22 | 30 | BELUM CUKUP | 10 | 73/9 | -5.85 | 10 | -2.62 | -0.53 | 2.6 | -2.25 | – | – |
| 167 | `M149` 3-Step Pullback | **40.7** | 28 | 32 | 51 | 15 | BELUM CUKUP | 21 | 225/69 | -2.47 | 23 | -4.43 | -0.41 | 6.0 | -0.20 | – | -0.18 |
| 168 | `N31X36` Turtle sistem 2 → keluar selep | **40.7** | 20 | 16 | 22 | 30 | BELUM CUKUP | 9 | 101/6 | -5.06 | 10 | -5.53 | -0.99 | 3.2 | -2.02 | – | – |
| 169 | `N39X36` NR7 kemudian pecah → keluar se | **40.7** | 4 | 10 | 18 | 30 | BELUM CUKUP | 6 | 30/7 | -7.86 | 9 | -12.90 | -1.00 | 5.0 | -2.40 | – | – |
| 170 | `M136` Short/Intermediate-term Low (L | **40.6** | 29 | 35 | 47 | 15 | BELUM CUKUP | 23 | 800/323 | -3.12 | 23 | -3.41 | -0.57 | 3.0 | -0.84 | – | -0.51 |
| 171 | `N28X14` ADX>25 + DI+ > DI- → keluar bi | **40.6** | 17 | 22 | 27 | 30 | BELUM CUKUP | 10 | 193/14 | -3.74 | 10 | -7.43 | -0.87 | 4.6 | -1.79 | – | – |
| 172 | `N24X16` Supertrend(10,3) + ADX>20 → ke | **40.6** | 17 | 18 | 23 | 30 | BELUM CUKUP | 9 | 119/9 | -5.25 | 10 | -5.28 | -0.98 | 2.7 | -2.09 | – | – |
| 173 | `M34` Carter TTM Squeeze | **40.5** | 30 | 32 | 48 | 15 | BELUM CUKUP | 22 | 107/48 | -2.07 | 23 | -2.65 | -0.31 | 4.4 | -0.44 | – | -1.30 |
| 174 | `N42X17` Lonjakan volum 2x → keluar bil | **40.5** | 16 | 16 | 39 | 30 | BELUM CUKUP | 10 | 195/60 | -2.16 | 10 | -9.07 | -0.93 | 6.1 | -1.04 | – | – |
| 175 | `M06` Minervini VCP Breakout | **40.4** | 28 | 36 | 43 | 15 | BELUM CUKUP | 22 | 88/45 | -3.69 | 23 | -1.93 | -0.30 | 3.2 | -0.98 | – | -2.89 |
| 176 | `N55X13` BB + RSI + ADX>20 → keluar bil | **40.4** | 18 | 26 | 19 | 30 | BELUM CUKUP | 10 | 68/0 | -3.26 | 10 | -4.85 | -0.98 | 3.7 | -1.71 | – | – |
| 177 | `N56X16` RSI>50 + ADX>20 → keluar bila  | **40.4** | 14 | 21 | 33 | 30 | BELUM CUKUP | 10 | 217/107 | -2.92 | 10 | -6.34 | -1.00 | 4.0 | -1.86 | – | – |
| 178 | `M99` Three Line Break | **40.3** | 31 | 31 | 48 | 15 | BELUM CUKUP | 23 | 166/104 | -3.36 | 23 | -3.54 | -0.41 | 4.1 | -0.75 | – | -2.85 |
| 179 | `M140` 猎豹出击 (Serangan Cheetah) | **40.3** | 17 | 26 | 33 | 15 | BELUM CUKUP | 11 | 42/16 | -3.43 | 23 | -7.29 | -0.83 | 4.0 | -1.48 | – | -1.71 |
| 180 | `M135` 3rd Watch | **40.3** | 17 | 16 | 28 | 15 | BELUM CUKUP | 9 | 15/4 | -9.88 | 23 | -6.32 | -0.79 | 4.2 | -1.44 | – | -9.35 |
| 181 | `M14` Walking with the Whales | **40.1** | 35 | 26 | 46 | 15 | BELUM CUKUP | 23 | 996/732 | -1.32 | 23 | -10.69 | -0.80 | 7.2 | -0.99 | – | -1.77 |
| 182 | `M28` VWAP Separator + Kiss Pivot | **40.1** | 32 | 28 | 44 | 15 | BELUM CUKUP | 21 | 122/101 | -1.47 | 23 | -7.99 | -0.94 | 5.7 | -1.16 | – | -9.72 |
| 183 | `N54X36` Supertrend + RSI>50 → keluar s | **40.1** | 19 | 13 | 33 | 30 | BELUM CUKUP | 10 | 168/82 | -3.18 | 10 | -9.41 | -1.00 | 7.2 | -1.87 | – | – |
| 184 | `M36` Turtle 55/20 | **40.0** | 28 | 30 | 50 | 15 | BELUM CUKUP | 23 | 344/178 | -2.32 | 23 | -4.22 | -0.36 | 7.0 | -0.47 | – | -1.08 |
| 185 | `M29` EMA3 + RSI75 + Stokastik | **40.0** | 26 | 26 | 39 | 15 | BELUM CUKUP | 16 | 37/31 | -2.77 | 23 | -9.73 | -0.78 | 7.7 | -1.12 | – | -6.15 |
| 186 | `N22X14` BB pecah atas + RSI → keluar b | **40.0** | 16 | 16 | 29 | 30 | BELUM CUKUP | 10 | 125/15 | -5.23 | 10 | -7.79 | -0.96 | 4.5 | -1.64 | – | – |
| 187 | `N28X17` ADX>25 + DI+ > DI- → keluar bi | **40.0** | 14 | 22 | 22 | 33 | BELUM CUKUP | 10 | 132/3 | -3.89 | 10 | -6.46 | -0.90 | 4.5 | -1.83 | – | – |
| 188 | `N29X36` PSAR naik + tutup>MA50 → kelua | **39.9** | 17 | 16 | 26 | 30 | BELUM CUKUP | 10 | 155/68 | -4.01 | 10 | -10.61 | -1.00 | 8.5 | -2.53 | – | – |
| 189 | `N54X16` Supertrend + RSI>50 → keluar b | **39.8** | 13 | 13 | 23 | 38 | BELUM CUKUP | 9 | 121/16 | -5.88 | 10 | -7.18 | -0.90 | 5.1 | -2.28 | – | – |
| 190 | `N27X36` Ichimoku atas awan → keluar se | **39.7** | 18 | 14 | 24 | 30 | BELUM CUKUP | 10 | 103/16 | -4.29 | 10 | -6.54 | -1.00 | 3.8 | -2.20 | – | – |
| 191 | `M50` Elder Triple Screen | **39.6** | 32 | 26 | 47 | 15 | BELUM CUKUP | 23 | 598/389 | -1.55 | 23 | -9.50 | -0.86 | 6.8 | -0.81 | – | -1.41 |
| 192 | `M156` Single Penetration (DiNapoli) | **39.4** | 30 | 28 | 45 | 15 | BELUM CUKUP | 23 | 249/171 | -1.69 | 23 | -5.96 | -0.46 | 7.1 | -1.06 | – | -3.41 |
| 193 | `M73` ADX(5) > 40 + Julat Terkecil 6 | **39.3** | 31 | 25 | 46 | 15 | BELUM CUKUP | 23 | 1091/844 | -0.75 | 23 | -9.54 | -1.00 | 5.5 | -0.96 | – | -5.99 |
| 194 | `M152` Spike & Ledge | **39.3** | 23 | 34 | 40 | 15 | BELUM CUKUP | 20 | 51/10 | -4.02 | 23 | -3.45 | -0.43 | 3.4 | -0.68 | – | -2.04 |
| 195 | `M19` Sneaky Pivot (proksi harian) | **39.2** | 24 | 31 | 46 | 15 | BELUM CUKUP | 22 | 425/267 | -3.66 | 23 | -4.94 | -0.51 | 4.2 | -0.90 | – | -12.94 |
| 196 | `M107` Golden Cross SMA50/200 | **39.2** | 23 | 33 | 42 | 15 | BELUM CUKUP | 20 | 43/9 | -2.77 | 23 | -4.97 | -0.66 | 2.6 | -0.48 | – | -0.77 |
| 197 | `N29X16` PSAR naik + tutup>MA50 → kelua | **39.2** | 13 | 15 | 28 | 30 | BELUM CUKUP | 10 | 205/96 | -4.47 | 10 | -7.97 | -1.00 | 5.6 | -2.52 | – | – |
| 198 | `M04` BB Squeeze Breakout | **39.1** | 25 | 26 | 50 | 16 | BELUM CUKUP | 21 | 155/61 | -3.54 | 23 | -3.21 | -0.35 | 4.5 | -0.25 | – | -0.46 |
| 199 | `M147` Improved Three-Bar Pullback | **39.1** | 24 | 27 | 32 | 15 | BELUM CUKUP | 16 | 100/36 | -5.25 | 23 | -6.04 | -0.59 | 5.2 | -2.03 | – | -1.60 |
| 200 | `N16X15` RSI2<10 tanpa penapis → ekori  | **39.1** | 12 | 19 | 22 | 31 | BELUM CUKUP | 10 | 180/0 | -2.87 | 10 | -9.69 | -0.83 | 8.3 | -1.35 | – | – |
| 201 | `M141` First Thrust (Landry) | **39.0** | 5 | 12 | 31 | 15 | BELUM CUKUP | 8 | 26/16 | -7.85 | 23 | -14.68 | -0.93 | 4.8 | -1.56 | – | -6.37 |
| 202 | `M155` Market Cycle Strategy | **38.6** | 27 | 26 | 45 | 15 | BELUM CUKUP | 23 | 744/374 | -3.06 | 23 | -5.40 | -0.65 | 4.5 | -1.06 | – | -2.39 |
| 203 | `M59` Anjakan Julat RSI | **38.6** | 18 | 20 | 40 | 15 | BELUM CUKUP | 14 | 36/19 | -6.09 | 23 | -5.41 | -0.63 | 4.6 | -0.80 | – | -2.96 |
| 204 | `M57` Landry Trend Knockout (TKO) | **38.5** | 28 | 27 | 39 | 15 | BELUM CUKUP | 23 | 180/125 | -2.79 | 23 | -6.84 | -0.81 | 4.2 | -1.78 | – | -4.75 |
| 205 | `M95` Nisbah Kebaharuan High 52 Ming | **38.5** | 22 | 28 | 45 | 15 | BELUM CUKUP | 21 | 129/69 | -2.75 | 23 | -8.39 | -0.77 | 5.5 | -0.87 | – | -2.03 |
| 206 | `M125` 2-Bar Breakout | **38.3** | 25 | 27 | 45 | 15 | BELUM CUKUP | 23 | 1135/473 | -3.46 | 23 | -6.58 | -0.67 | 4.3 | -1.14 | – | -0.62 |
| 207 | `N47X16` NR7 + EMA9>EMA21 → keluar bila | **38.3** | 6 | 22 | 26 | 30 | BELUM CUKUP | 10 | 200/47 | -3.46 | 10 | -12.04 | -1.00 | 4.6 | -2.46 | – | – |
| 208 | `M03` BB Break + Divergence RSI | **38.0** | 21 | 30 | 47 | 15 | BELUM CUKUP | 23 | 431/349 | -1.77 | 23 | -6.74 | -0.74 | 3.9 | -0.83 | – | -3.23 |
| 209 | `M66` IBD Undur Pertama ke Purata 50 | **37.9** | 26 | 23 | 47 | 15 | BELUM CUKUP | 23 | 253/158 | -2.47 | 23 | -6.97 | -0.60 | 7.1 | -0.90 | – | -2.35 |
| 210 | `M31` Band Walk (BB 20/2) | **37.9** | 26 | 20 | 52 | 15 | BELUM CUKUP | 22 | 400/115 | -2.14 | 23 | -4.82 | -0.40 | 7.6 | -0.28 | – | -0.53 |
| 211 | `M55` Guppy GMMA | **37.6** | 26 | 21 | 47 | 15 | BELUM CUKUP | 23 | 231/141 | -2.86 | 23 | -8.66 | -0.90 | 5.2 | -0.87 | – | -2.47 |
| 212 | `M01` Bollinger Band + RSI | **37.5** | 35 | 13 | 42 | 15 | BELUM CUKUP | 20 | 112/25 | -0.98 | 23 | -9.18 | -0.85 | 5.0 | -0.77 | – | -2.96 |
| 213 | `M11` NR7 Breakout + Volume | **36.9** | 22 | 22 | 41 | 15 | BELUM CUKUP | 21 | 124/88 | -1.51 | 23 | -10.79 | -0.77 | 8.1 | -1.51 | – | -1.41 |
| 214 | `M101` Bulkowski: Tiga lembah menaik | **36.6** | 17 | 16 | 44 | 15 | BELUM CUKUP | 17 | 46/22 | -4.31 | 23 | -9.43 | -0.67 | 7.8 | -0.51 | – | -1.39 |
| 215 | `N47X36` NR7 + EMA9>EMA21 → keluar sele | **36.5** | 0 | 13 | 21 | 30 | BELUM CUKUP | 9 | 181/34 | -4.35 | 10 | -17.45 | -1.00 | 8.0 | -2.91 | – | – |
| 216 | `M154` HOLP (High of Low Period) | **35.9** | 15 | 16 | 40 | 15 | BELUM CUKUP | 17 | 90/35 | -4.28 | 23 | -11.97 | -0.93 | 7.6 | -1.19 | – | -5.19 |
| 217 | `M47` Holy Grail Raschke | **35.4** | 11 | 16 | 28 | 15 | BELUM CUKUP | 15 | 33/29 | -3.45 | 23 | -11.08 | -0.98 | 6.7 | -2.42 | – | -21.73 |
| 218 | `M79` Radge: 20% Flipper | **34.9** | 15 | 22 | 41 | 15 | BELUM CUKUP | 23 | 385/121 | -5.04 | 23 | -9.88 | -0.74 | 6.4 | -1.52 | – | -3.06 |
| 219 | `M123` CCI Correction (Lambert, Chart | **34.6** | 14 | 26 | 31 | 15 | BELUM CUKUP | 22 | 189/172 | -1.90 | 23 | -12.17 | -1.00 | 7.1 | -2.69 | – | -5.32 |
| 220 | `M122` Moving Momentum (ChartSchool) | **33.6** | 15 | 18 | 34 | 15 | BELUM CUKUP | 23 | 112/64 | -4.71 | 23 | -12.79 | -1.00 | 6.4 | -2.27 | – | -6.62 |
| 221 | `M81` Bensdorp Long Trend High Momen | **33.4** | 3 | 5 | 40 | 15 | BELUM CUKUP | 13 | 431/160 | -5.61 | 23 | -21.46 | -0.93 | 14.6 | -1.47 | – | -4.57 |
| 222 | `M09` Volumatic VIDYA Pivot Retest | **33.1** | 3 | 9 | 28 | 15 | BELUM CUKUP | 14 | 33/21 | -6.17 | 23 | -15.94 | -1.00 | 8.9 | -2.23 | – | -13.10 |
| 223 | `M82` Arthur Hill Rotasi Sasaran 10% | **32.9** | 17 | 9 | 47 | 15 | BELUM CUKUP | 23 | 591/240 | -2.44 | 23 | -10.84 | -0.58 | 10.1 | -0.91 | – | -3.53 |
| 224 | `M76` Undercut & Rally pada Low Pent | **32.9** | 8 | 19 | 37 | 15 | BELUM CUKUP | 21 | 78/62 | -3.08 | 23 | -12.50 | -1.00 | 7.1 | -1.75 | – | -6.66 |
| 225 | `M161` EMA 10/21 + Supertrend (10,3) | **32.0** | 12 | 10 | 48 | 15 | BELUM CUKUP | 23 | 491/247 | -1.78 | 23 | -18.20 | -0.93 | 10.0 | -0.72 | – | -1.66 |
| 226 | `M90` Pring KST | **31.4** | 8 | 13 | 41 | 15 | BELUM CUKUP | 22 | 89/47 | -4.05 | 23 | -14.46 | -0.79 | 11.8 | -1.19 | – | -4.92 |

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

