# Kadar menang setiap setup F (backtest pada saham yang tidak dilihat; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_ringkas.py` daripada `data/registry_F.csv` dan fail hasil setiap pusingan. **Jangan sunting secara manual.**

**Kadar menang** = daripada semua dagangan setup itu (dengan henti dan cara keluarnya sendiri), berapa peratus dijual dengan UNTUNG selepas kos 0.5 %; selebihnya rugi. Lajur "daripada 10 dagangan" ialah angka yang sama dibundarkan. Angka daripada saham Kunci (yang carian tidak lihat): CS01 = 1,000 saham lain; CS02–CS06 = kumpulan B; 2010 – Ogo 2026.

**Baca bersama purata setiap dagangan.** Kadar menang sahaja tidak menunjukkan saiz untung dan rugi: setup yang menang 4 daripada 10 masih boleh untung jika untungnya besar, dan setup yang menang 6 daripada 10 boleh rugi jika ruginya besar (`CLAUDE.md`: kadar menang sahaja bukan ukuran).

Ringkasan: 95 setup; median kadar menang 52 %; 61 setup menang ≥ 50 %; 61 setup menang ≥ 50 % DAN purata positif; 24 setup menang < 50 % tetapi purata positif.

Kadar menang tertinggi (≥ 300 belian): `F55` 74 % (purata +7.7 %, 484 belian); `F62` 73 % (purata +9.9 %, 1,387 belian); `F79` 73 % (purata +10.1 %, 1,205 belian); `F43` 70 % (purata +5.8 %, 515 belian); `F57` 70 % (purata +6.7 %, 542 belian).

| ID | Pusingan | Prasyarat | Pencetus | Penapis saham | Belian | **Menang %** | Daripada 10 dagangan: untung / rugi | Purata setiap dagangan % | Dijual ≥ +10 % % | Menang % K1 / K2 / K3 | Jejak hadapan |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `F01` | CS01 | – | N203 | Supertrend naik + ATR% >= 4 | 1,127 | **52** | 5 / 5 | +2.54 | 29 | 46 / 53 / – |  |
| `F02` | CS01 | QQQ OFF | M111 Sistem Volatiliti Wilder (ditala 2) | >= 30% di bawah puncak 52 minggu | 1,184 | **54** | 5 / 5 | +1.74 | 27 | 58 / 52 / – |  |
| `F03` | CS01 | – | M01 Bollinger Band + RSI (ditala 2) | RS >= 70 + >= 30% di bawah puncak 52 minggu | 759 | **52** | 5 / 5 | +2.49 | 33 | 48 / 53 / – |  |
| `F04` | CS01 | QQQ OFF | M79 Radge: 20% Flipper (ditala 1) | volum hari isyarat >= 1.5x purata 50 | 1,540 | **55** | 6 / 4 | +2.13 | 26 | 54 / 55 / – |  |
| `F05` | CS01 | – | P07 MA20 silang atas MA50 | Supertrend naik + ATR% >= 4 | 3,098 | **50** | 5 / 5 | +1.40 | 26 | 47 / 50 / – |  |
| `F06` | CS01 | – | N07 Tiga MA tersusun | ADX < 20 + ATR% >= 4 | 2,941 | **51** | 5 / 5 | +1.58 | 27 | 50 / 52 / – |  |
| `F07` | CS01 | QQQ OFF | M30 BB Free Bar + Himpitan 50/2.5 | ATR% >= 4 | 578 | **52** | 5 / 5 | +1.03 | 28 | 48 / 54 / – |  |
| `F08` | CS01 | – | N201 | Supertrend naik + ATR% >= 4 | 2,765 | **50** | 5 / 5 | +1.21 | 26 | 47 / 51 / – |  |
| `F09` | CS01 | – | M140 猎豹出击 (Serangan Cheetah) (ditala 1) | ATR% >= 4 + hari naik (tutup > buka) | 1,764 | **50** | 5 / 5 | +1.46 | 25 | 50 / 50 / – |  |
| `F10` | CS01 | – | P16 RSI2<5 atas MA200 | volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 | 1,303 | **44** | 4 / 6 | +0.39 | 21 | 42 / 45 / – |  |
| `F11` | CS02 | QQQ OFF | M01 Bollinger Band + RSI (ditala 2) | >= 30% di bawah puncak 52 minggu | 10,261 | **56** | 6 / 4 | +2.53 | 28 | 56 / 56 / 57 |  |
| `F12` | CS02 | QQQ OFF | M88 O'Neil Shakeout +3 (ditala 1) | >= 30% di bawah puncak 52 minggu | 3,182 | **58** | 6 / 4 | +3.31 | 32 | 58 / 58 / 57 |  |
| `F13` | CS02 | QQQ OFF | M02 MACD + SMA200 | RSI14 > 60 | 551 | **60** | 6 / 4 | +1.43 | 15 | 60 / 59 / 62 |  |
| `F14` | CS02 | QQQ OFF | N28 ADX>25 + DI+ > DI- | >= 30% di bawah puncak 52 minggu | 6,550 | **56** | 6 / 4 | +2.44 | 28 | 58 / 56 / 54 |  |
| `F15` | CS02 | QQQ OFF | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 1) | >= 30% di bawah puncak 52 minggu | 5,800 | **57** | 6 / 4 | +2.89 | 29 | 58 / 57 / 51 |  |
| `F16` | CS02 | – | N38 VCP pecah | ATR% >= 4 + tutup dalam 25% teratas julat hari | 4,483 | **53** | 5 / 5 | +2.03 | 29 | 55 / 53 / 49 |  |
| `F17` | CS02 | QQQ OFF | P14 RSI14 silang atas 30 | >= 30% di bawah puncak 52 minggu | 7,473 | **57** | 6 / 4 | +2.37 | 28 | 58 / 56 / 54 |  |
| `F18` | CS02 | QQQ OFF | N75 RSI14 < 40 tanpa penapis | >= 30% di bawah puncak 52 minggu | 11,346 | **54** | 5 / 5 | +1.84 | 27 | 55 / 53 / 53 |  |
| `F19` | CS02 | QQQ OFF | P02 MACD silang naik bawah sifar | RSI14 > 60 | 684 | **57** | 6 / 4 | +1.31 | 15 | 58 / 56 / 54 |  |
| `F20` | CS02 | QQQ OFF | M141 First Thrust (Landry) (ditala 1) | MACD > isyarat | 1,144 | **58** | 6 / 4 | +1.68 | 18 | 63 / 53 / 52 |  |
| `F21` | CS03 | – | N40 OBV tinggi baharu + MA50 | tutup > MA200 + >= 30% di bawah puncak 52 minggu | 1,114 | **36** | 4 / 6 | -0.72 | 6 | 36 / 35 / 40 | ya |
| `F22` | CS03 | QQQ ON | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | ATR% >= 4 | 2,854 | **40** | 4 / 6 | +0.10 | 11 | 38 / 39 / 43 | ya |
| `F23` | CS03 | SPY > SMA200 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 90 | 650 | **35** | 4 / 6 | -0.14 | 20 | 36 / 37 / 30 |  |
| `F24` | CS03 | – | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (ditala 2) | RS >= 90 + ATR% >= 4 | 2,514 | **46** | 5 / 5 | +0.91 | 25 | 47 / 46 / 43 | ya |
| `F25` | CS03 | – | M57 Landry Trend Knockout (TKO) (ditala 1) | RS >= 90 + ATR% >= 4 | 3,291 | **43** | 4 / 6 | +0.14 | 22 | 41 / 45 / 43 |  |
| `F26` | CS03 | – | M50 Elder Triple Screen (ditala 2) | RS >= 90 + ATR% >= 4 | 3,971 | **46** | 5 / 5 | -0.07 | 21 | 47 / 46 / 43 |  |
| `F27` | CS03 | – | N73 Tutup bawah jalur bawah BB(20,2) | RS >= 70 + ATR% >= 4 | 4,857 | **54** | 5 / 5 | +1.85 | 28 | 53 / 53 / 56 | ya |
| `F28` | CS03 | QQQ OFF | M92 CCI-50 (ditala 2) | >= 30% di bawah puncak 52 minggu | 2,744 | **51** | 5 / 5 | +1.13 | 25 | 52 / 53 / 45 | ya |
| `F29` | CS03 | – | P13 RSI14 silang atas 60 | RS >= 90 + ATR% >= 4 | 4,619 | **39** | 4 / 6 | +0.05 | 20 | 43 / 38 / 37 |  |
| `F30` | CS03 | – | N43 Undur EMA8 + penapis MA50 | Supertrend naik + ATR% >= 4 | 10,991 | **51** | 5 / 5 | +1.00 | 25 | 50 / 52 / 52 | ya |
| `F31` | CS04 | – | N40 OBV tinggi baharu + MA50 | tutup > MA200 + >= 20% di bawah puncak 52 minggu | 3,278 | **37** | 4 / 6 | -0.44 | 6 | 37 / 36 / 37 |  |
| `F32` | CS04 | QQQ ON | M84 Jarak purata bergerak MAD 21/200 | ATR% >= 4 | 2,924 | **40** | 4 / 6 | +0.31 | 12 | 38 / 40 / 44 |  |
| `F33` | CS04 | SPY > SMA200 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 95 | 550 | **44** | 4 / 6 | -0.34 | 11 | 48 / 43 / 40 |  |
| `F34` | CS04 | – | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | RS >= 95 + ATR% >= 4 | 1,813 | **46** | 5 / 5 | -0.45 | 15 | 48 / 45 / 44 | ya |
| `F35` | CS04 | – | M57 Landry Trend Knockout (TKO) | RS >= 95 + ATR% >= 4 | 2,192 | **38** | 4 / 6 | +0.03 | 20 | 37 / 39 / 39 |  |
| `F36` | CS04 | – | M50 Elder Triple Screen (ditala 2) | RS >= 95 + ATR% >= 6 | 1,013 | **50** | 5 / 5 | -0.36 | 28 | 51 / 52 / 43 |  |
| `F37` | CS04 | QQQ OFF | M92 CCI-50 (ditala 2) | >= 20% di bawah puncak 52 minggu | 5,770 | **51** | 5 / 5 | +0.83 | 22 | 53 / 52 / 46 |  |
| `F38` | CS04 | – | P13 RSI14 silang atas 60 [tala daripada F29] | RS >= 95 + ATR% >= 4 | 2,960 | **37** | 4 / 6 | +0.32 | 19 | 38 / 36 / 34 | ya |
| `F39` | CS05 | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | tutup > MA50 + >= 30% di bawah puncak 52 minggu | 501 | **52** | 5 / 5 | +1.82 | 27 | 53 / 52 / 48 |  |
| `F40` | CS05 | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (ditala 2) | Supertrend naik + >= 30% di bawah puncak 52 minggu | 597 | **51** | 5 / 5 | +2.15 | 28 | 51 / 51 / 49 |  |
| `F41` | CS05 | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | ADX < 20 + ATR% >= 4 | 926 | **46** | 5 / 5 | -0.17 | 27 | 47 / 51 / 39 |  |
| `F42` | CS05 | distribution day QQQ <= 2 dalam 25 sesi + >= 60% saham industri di atas MA50 | M159 Heikin-Ashi Trend (ditala 1) | RS >= 90 + ATR% >= 4 | 305 | **53** | 5 / 5 | +3.53 | 28 | 47 / 63 / 50 |  |
| `F43` | CS05 | Januari + tiada earnings dalam 20 sesi akan datang | M105 Supertrend tulen (ditala 2) | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 515 | **70** | 7 / 3 | +5.78 | 37 | 79 / 78 / 32 |  |
| `F44` | CS05 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper (ditala 2) | templat trend Minervini + ATR% >= 4 | 615 | **48** | 5 / 5 | +1.13 | 26 | 52 / 48 / 45 |  |
| `F45` | CS05 | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | MACD > 0 + ATR% >= 4 | 793 | **54** | 5 / 5 | +3.28 | 29 | 47 / 58 / 53 |  |
| `F46` | CS05 | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | N124 Episodic pivot gap 8-10% | tutup > MA20 + RSI14 > 50 | 278 | **55** | 6 / 4 | +1.13 | 22 | 51 / 61 / 51 |  |
| `F47` | CS05 | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | M124 'Last' Stochastic Technique (ChartSchool) (ditala 2) | Supertrend naik + volum hari isyarat >= 1.5x purata 50 | 393 | **53** | 5 / 5 | +0.69 | 20 | 51 / 56 / 50 |  |
| `F48` | CS05 | >= 60% saham di atas MA50 + >= 60% saham sektor di atas MA50 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | dalam 15% dari puncak 52 minggu + ATR% >= 4 | 1,163 | **48** | 5 / 5 | +1.02 | 26 | 45 / 50 / 53 |  |
| `F49` | CS05 | QQQ >= 10% di bawah puncak + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | MACD > isyarat + ATR% >= 4 | 1,069 | **65** | 6 / 4 | +5.10 | 39 | 69 / 63 / 70 |  |
| `F50` | CS05 | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | 707 | **58** | 6 / 4 | +3.99 | 35 | 65 / 55 / 53 |  |
| `F51` | CS05 | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat | 733 | **65** | 6 / 4 | +4.84 | 30 | 63 / 65 / 63 |  |
| `F52` | CS05 | Januari + tiada earnings dalam 20 sesi akan datang | M159 Heikin-Ashi Trend (ditala 2) | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | 696 | **64** | 6 / 4 | +5.22 | 37 | 72 / 67 / 40 |  |
| `F53` | CS05 | Januari + tiada earnings dalam 20 sesi akan datang | M79 Radge: 20% Flipper (ditala 2) | RSI14 > 50 + >= 30% di bawah puncak 52 minggu | 340 | **65** | 6 / 4 | +4.93 | 35 | 69 / 72 / 37 |  |
| `F54` | CS05 | breadth thrust Zweig aktif (20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | 548 | **63** | 6 / 4 | +5.32 | 36 | 64 / 60 / 65 |  |
| `F55` | CS05 | turun-naik SPY 21 hari >= 25% setahun + sektor 3 terbawah (pulangan 63 sesi) | N75 RSI14 < 40 tanpa penapis | ADX < 20 + >= 30% di bawah puncak 52 minggu | 484 | **74** | 7 / 3 | +7.72 | 42 | 76 / 69 / 87 |  |
| `F56` | CS05 | QQQ >= 10% di bawah puncak | M01 Bollinger Band + RSI (ditala 2) | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 1,943 | **60** | 6 / 4 | +4.90 | 36 | 57 / 63 / 52 |  |
| `F57` | CS05 | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | ATR% >= 4 | 542 | **70** | 7 / 3 | +6.68 | 41 | 52 / 73 / 76 |  |
| `F58` | CS06 | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | Supertrend naik + >= 30% di bawah puncak 52 minggu | 380 | **47** | 5 / 5 | +0.73 | 30 | 51 / 41 / 51 |  |
| `F59` | CS06 | distribution day QQQ <= 2 dalam 25 sesi | P09 tutup silang atas MA20 | RS >= 70 + ATR% >= 4 | 316 | **45** | 4 / 6 | +1.78 | 26 | 44 / 46 / 44 |  |
| `F60` | CS06 | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | N119 3 tutup turun berturut | RS >= 90 + ATR% >= 4 | 3,236 | **49** | 5 / 5 | +1.30 | 27 | 47 / 48 / 52 |  |
| `F61` | CS06 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | N29 PSAR naik + tutup>MA50 | templat trend Minervini + ATR% >= 4 | 1,460 | **49** | 5 / 5 | +0.57 | 24 | 50 / 50 / 46 |  |
| `F62` | CS06 | QQQ >= 20% di bawah puncak | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 1) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | 1,387 | **73** | 7 / 3 | +9.89 | 48 | 98 / 70 / 92 |  |
| `F63` | CS06 | QQQ OFF + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 431 | **61** | 6 / 4 | +4.48 | 34 | 67 / 59 / 55 |  |
| `F64` | CS06 | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | M01 Bollinger Band + RSI (ditala 2) | ADX > 25 + >= 30% di bawah puncak 52 minggu | 725 | **69** | 7 / 3 | +9.12 | 46 | 64 / 66 / 85 |  |
| `F65` | CS06 | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | P14 RSI14 silang atas 30 | RSI14 < 40 + volum 10 hari > volum 50 hari | 428 | **63** | 6 / 4 | +2.82 | 29 | 64 / 60 / 71 |  |
| `F66` | CS06 | <= 30% saham di atas MA50 + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper (ditala 2) | >= 30% di bawah puncak 52 minggu + tutup dalam 25% teratas julat hari | 733 | **66** | 7 / 3 | +6.05 | 42 | 57 / 66 / 79 |  |
| `F67` | CS06 | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | N75 RSI14 < 40 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 645 | **56** | 6 / 4 | +5.10 | 36 | 48 / 55 / 70 |  |
| `F68` | CS06 | breadth thrust Zweig aktif (20 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | ADX < 20 + >= 30% di bawah puncak 52 minggu | 637 | **57** | 6 / 4 | +5.24 | 35 | 54 / 59 / 60 |  |
| `F69` | CS06 | turun-naik SPY 21 hari >= 25% setahun | M28 VWAP Separator + Kiss Pivot (ditala 2) | >= 30% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | 1,619 | **62** | 6 / 4 | +5.26 | 39 | 55 / 59 / 83 |  |
| `F70` | CS06 | rejim ON baharu (<= 30 sesi) + earnings dalam 1-3 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari | tutup > MA50 + >= 20% di bawah puncak 52 minggu | 1,177 | **44** | 4 / 6 | -0.04 | 21 | 48 / 41 / 40 |  |
| `F71` | CS06 | rejim ON baharu (<= 30 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales | Supertrend naik + >= 40% di bawah puncak 52 minggu | 645 | **49** | 5 / 5 | +0.72 | 29 | 57 / 45 / 46 |  |
| `F72` | CS06 | >= 50% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | Supertrend naik + >= 20% di bawah puncak 52 minggu | 1,131 | **52** | 5 / 5 | +1.45 | 28 | 50 / 53 / 53 |  |
| `F73` | CS06 | distribution day QQQ <= 3 dalam 25 sesi + >= 50% saham industri di atas MA50 | M159 Heikin-Ashi Trend | RS >= 80 + ATR% >= 5 | 638 | **50** | 5 / 5 | +1.14 | 28 | 43 / 56 / 42 |  |
| `F74` | CS06 | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) | MACD > 0 + ATR% >= 4 | 773 | **52** | 5 / 5 | +2.90 | 28 | 46 / 56 / 49 |  |
| `F75` | CS06 | distribution day QQQ <= 3 dalam 25 sesi | P09 tutup silang atas MA20 | RS >= 70 + ATR% >= 5 | 464 | **48** | 5 / 5 | +0.87 | 27 | 47 / 51 / 36 |  |
| `F76` | CS06 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper | templat trend Minervini + ATR% >= 4 | 675 | **39** | 4 / 6 | +0.75 | 23 | 43 / 39 / 38 |  |
| `F77` | CS06 | SPY atas SMA200 + >= 70% saham sektor di atas MA50 | N119 3 tutup turun berturut | RS >= 95 + ATR% >= 5 | 972 | **49** | 5 / 5 | +1.65 | 29 | 46 / 49 / 53 |  |
| `F78` | CS06 | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 10% | M124 'Last' Stochastic Technique (ChartSchool) | Supertrend naik + volum hari isyarat >= 1.5x purata 50 | 715 | **52** | 5 / 5 | +0.58 | 16 | 55 / 52 / 45 |  |
| `F79` | CS06 | QQQ >= 20% di bawah puncak | M73 ADX(5) > 40 + Julat Terkecil 6 Hari | RSI14 < 40 + >= 20% di bawah puncak 52 minggu | 1,205 | **73** | 7 / 3 | +10.14 | 47 | 97 / 70 / 100 |  |
| `F80` | CS06 | QQQ >= 7.5% di bawah puncak + earnings dalam 1-7 sesi akan datang | N119 3 tutup turun berturut | MACD > isyarat + ATR% >= 5 | 1,077 | **45** | 4 / 6 | +2.42 | 32 | 38 / 43 / 61 |  |
| `F81` | CS06 | QQQ OFF + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat + >= 20% di bawah puncak 52 minggu | 681 | **60** | 6 / 4 | +3.20 | 30 | 63 / 58 / 60 |  |
| `F82` | CS06 | Januari + tiada earnings dalam 20 sesi akan datang | M105 Supertrend tulen | MACD > isyarat + >= 40% di bawah puncak 52 minggu | 294 | **67** | 7 / 3 | +5.50 | 36 | 74 / 74 / 37 |  |
| `F83` | CS06 | turun-naik SPY 21 hari >= 20% setahun + kejutan untung terkini positif (SUE > 0) | M01 Bollinger Band + RSI | ADX > 25 + >= 40% di bawah puncak 52 minggu | 617 | **63** | 6 / 4 | +6.99 | 44 | 59 / 63 / 67 |  |
| `F84` | CS06 | <= 40% saham di atas MA50 + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper | >= 40% di bawah puncak 52 minggu + tutup dalam 25% teratas julat hari | 670 | **58** | 6 / 4 | +3.98 | 39 | 53 / 60 / 60 |  |
| `F85` | CS06 | turun-naik SPY 21 hari >= 20% setahun + kejutan untung terkini positif (SUE > 0) | N75 RSI14 < 40 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 1,024 | **59** | 6 / 4 | +4.24 | 33 | 54 / 63 / 52 |  |
| `F86` | CS06 | breadth thrust Zweig aktif (20 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | ADX < 20 + >= 20% di bawah puncak 52 minggu | 1,203 | **59** | 6 / 4 | +3.23 | 29 | 58 / 60 / 67 |  |
| `F87` | CS06 | turun-naik SPY 21 hari >= 20% setahun | M28 VWAP Separator + Kiss Pivot | >= 50% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | 740 | **64** | 6 / 4 | +6.54 | 43 | 65 / 61 / 79 |  |
| `F88` | CS07 | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI (ditala 3) | – | 461 | **60** | 6 / 4 | +2.42 | 27 | 62 / 56 / 71 |  |
| `F89` | CS07 | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu + hari naik (tutup > buka) | 383 | **54** | 5 / 5 | +1.99 | 26 | 45 / 57 / 56 |  |
| `F90` | CS07 | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M50 Elder Triple Screen | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 303 | **48** | 5 / 5 | +0.58 | 23 | 48 / 50 / 42 |  |
| `F91` | CS07 | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu | 366 | **54** | 5 / 5 | +2.85 | 28 | 47 / 57 / 57 |  |
| `F92` | CS07 | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI | – | 377 | **59** | 6 / 4 | +2.25 | 25 | 57 / 59 / 67 |  |
| `F93` | CS07 | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M02 MACD + SMA200 | tutup > MA200 + MA50 naik (lawan 20 bar lalu) | 363 | **49** | 5 / 5 | +0.99 | 16 | 49 / 47 / 57 |  |
| `F94` | CS07 | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | K11.016 Supertrend(20, 1.5) bertukar naik | RS >= 90 + dalam 15% dari puncak 52 minggu | 380 | **44** | 4 / 6 | -0.44 | 19 | 48 / 40 / 44 |  |
| `F95` | CS07 | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K19.011 pecah atas Keltner(30, 1.0) | RSI14 > 60 + RS >= 90 | 330 | **52** | 5 / 5 | +1.69 | 24 | 52 / 54 / 45 |  |

- K1 = 2010–2019, K2 = 2020–2024 (CS01: 2020 – Ogo 2026), K3 = 2025 – Ogo 2026 (tiada bagi CS01).
- Cara pegang dan keluar setiap setup: lajur `henti` dan `keluar` dalam `KADAR_MENANG.csv` dan `data/registry_F.csv`.
- Tiada saham delist dalam data (condong ke atas); backtest sahaja. Kad skor kekal satu-satunya keputusan wang sebenar.
