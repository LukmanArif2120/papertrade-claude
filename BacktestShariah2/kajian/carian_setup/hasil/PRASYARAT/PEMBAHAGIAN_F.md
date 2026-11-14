# Setup F: prasyarat (pasaran) lawan syarat (saham itu sendiri)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_ringkas.py` daripada `data/registry_F.csv` dan `jejak_f/kohort.json`. **Jangan sunting secara manual.**

Prasyarat = isyarat yang BUKAN daripada saham itu sendiri. Ruang carian CS01–CS04 hanya ada tiga: **QQQ ON** (QQQ di atas SMA50 dan SMA10 di atas SMA20), **QQQ OFF** (selain itu) dan **SPY > SMA200**. CS05 (pindaan (i)) menambah 33 prasyarat pasaran dan 15 prasyarat kumpulan/syarikat (`cs_lapis.py`). RS diletak di bawah syarat saham (dikira daripada harga saham itu, dipangkatkan lawan saham lain).

Bilangan (CS01–CS04): – = 20 · QQQ OFF = 14 · QQQ ON = 2 · SPY > SMA200 = 2 · QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang = 2 · QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang = 2 · rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang = 1 · keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang = 1 · QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang = 1 · >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang = 1 (jumlah 46); CS05: 19 setup; CS06: 30 setup.

| ID | Pusingan | Prasyarat (pasaran) | Syarat saham: pencetus | Syarat saham: penapis | Henti | Keluar | Jejak hadapan |
|---|---|---|---|---|---|---|---|
| F01 | CS01 | – | N203 | Supertrend naik + ATR% >= 4 | H4 4xATR14 | X03 tutup < MA50 DAN X22 hari turun dengan volum >= 1.5x |  |
| F02 | CS01 | QQQ OFF | M111 Sistem Volatiliti Wilder (ditala 2) | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X08 MA10 < MA20 DAN X22 hari turun dengan volum >= 1.5x |  |
| F03 | CS01 | – | M01 Bollinger Band + RSI (ditala 2) | RS >= 70 + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X20 tutup < 92% tutup tertinggi sejak beli DAN X21 Stochastic silang turun di atas 80 |  |
| F04 | CS01 | QQQ OFF | M79 Radge: 20% Flipper (ditala 1) | volum hari isyarat >= 1.5x purata 50 | H4 4xATR14 | X12 RSI14 silang turun bawah 70 DAN X20 tutup < 92% tutup tertinggi sejak beli |  |
| F05 | CS01 | – | P07 MA20 silang atas MA50 | Supertrend naik + ATR% >= 4 | H4 4xATR14 | X14 Supertrend turun DAN X22 hari turun dengan volum >= 1.5x |  |
| F06 | CS01 | – | N07 Tiga MA tersusun | ADX < 20 + ATR% >= 4 | H4 4xATR14 | X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli) DAN X22 hari turun dengan volum >= 1.5x |  |
| F07 | CS01 | QQQ OFF | M30 BB Free Bar + Himpitan 50/2.5 | ATR% >= 4 | H4 4xATR14 | X13 RSI14 > 80 |  |
| F08 | CS01 | – | N201 | Supertrend naik + ATR% >= 4 | H4 4xATR14 | X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli) DAN X22 hari turun dengan volum >= 1.5x |  |
| F09 | CS01 | – | M140 猎豹出击 (Serangan Cheetah) (ditala 1) | ATR% >= 4 + hari naik (tutup > buka) | H4 4xATR14 | X14 Supertrend turun DAN X22 hari turun dengan volum >= 1.5x |  |
| F10 | CS01 | – | P16 RSI2<5 atas MA200 | volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 ATAU X19 Chandelier 2xATR14 |  |
| F11 | CS02 | QQQ OFF | M01 Bollinger Band + RSI (ditala 2) | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X04 tutup < EMA10 DAN X12 RSI14 silang turun bawah 70 |  |
| F12 | CS02 | QQQ OFF | M88 O'Neil Shakeout +3 (ditala 1) | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X12 RSI14 silang turun bawah 70 ATAU X13 RSI14 > 80 |  |
| F13 | CS02 | QQQ OFF | M02 MACD + SMA200 | RSI14 > 60 | H4 4xATR14 | X08 MA10 < MA20 DAN X20 tutup < 92% tutup tertinggi sejak beli |  |
| F14 | CS02 | QQQ OFF | N28 ADX>25 + DI+ > DI- | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X09 MACD < isyarat DAN X21 Stochastic silang turun di atas 80 |  |
| F15 | CS02 | QQQ OFF | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 1) | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X04 tutup < EMA10 DAN X12 RSI14 silang turun bawah 70 |  |
| F16 | CS02 | – | N38 VCP pecah | ATR% >= 4 + tutup dalam 25% teratas julat hari | H4 4xATR14 | X21 Stochastic silang turun di atas 80 DAN X22 hari turun dengan volum >= 1.5x |  |
| F17 | CS02 | QQQ OFF | P14 RSI14 silang atas 30 | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X13 RSI14 > 80 |  |
| F18 | CS02 | QQQ OFF | N75 RSI14 < 40 tanpa penapis | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X13 RSI14 > 80 DAN X21 Stochastic silang turun di atas 80 |  |
| F19 | CS02 | QQQ OFF | P02 MACD silang naik bawah sifar | RSI14 > 60 | H4 4xATR14 | X14 Supertrend turun DAN X23 tutup < buka dan < rendah semalam |  |
| F20 | CS02 | QQQ OFF | M141 First Thrust (Landry) (ditala 1) | MACD > isyarat | H4 4xATR14 | X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli) DAN X22 hari turun dengan volum >= 1.5x |  |
| F21 | CS03 | – | N40 OBV tinggi baharu + MA50 | tutup > MA200 + >= 30% di bawah puncak 52 minggu | H2 -10% | X09 MACD < isyarat ATAU X10 histogram MACD turun 3 hari | ya |
| F22 | CS03 | QQQ ON | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | ATR% >= 4 | H2 -10% | X11 RSI14 < 50 ATAU X21 Stochastic silang turun di atas 80 | ya |
| F23 | CS03 | SPY > SMA200 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 90 | H2 -10% | X12 RSI14 silang turun bawah 70 DAN X16 tutup < rendah 5 hari |  |
| F24 | CS03 | – | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (ditala 2) | RS >= 90 + ATR% >= 4 | H4 4xATR14 | X11 RSI14 < 50 DAN X22 hari turun dengan volum >= 1.5x | ya |
| F25 | CS03 | – | M57 Landry Trend Knockout (TKO) (ditala 1) | RS >= 90 + ATR% >= 4 | H4 4xATR14 | X22 hari turun dengan volum >= 1.5x DAN X24 +DI < -DI |  |
| F26 | CS03 | – | M50 Elder Triple Screen (ditala 2) | RS >= 90 + ATR% >= 4 | H4 4xATR14 | X12 RSI14 silang turun bawah 70 ATAU X22 hari turun dengan volum >= 1.5x |  |
| F27 | CS03 | – | N73 Tutup bawah jalur bawah BB(20,2) | RS >= 70 + ATR% >= 4 | H4 4xATR14 | X07 dua tutup berturut < MA20 DAN X21 Stochastic silang turun di atas 80 | ya |
| F28 | CS03 | QQQ OFF | M92 CCI-50 (ditala 2) | >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X20 tutup < 92% tutup tertinggi sejak beli DAN X21 Stochastic silang turun di atas 80 | ya |
| F29 | CS03 | – | P13 RSI14 silang atas 60 | RS >= 90 + ATR% >= 4 | H2 -10% | X21 Stochastic silang turun di atas 80 DAN X22 hari turun dengan volum >= 1.5x |  |
| F30 | CS03 | – | N43 Undur EMA8 + penapis MA50 | Supertrend naik + ATR% >= 4 | H4 4xATR14 | X21 Stochastic silang turun di atas 80 DAN X22 hari turun dengan volum >= 1.5x | ya |
| F31 | CS04 | – | N40 OBV tinggi baharu + MA50 | tutup > MA200 + >= 20% di bawah puncak 52 minggu | H2 -10% | X09 MACD < isyarat ATAU X10 histogram MACD turun 3 hari |  |
| F32 | CS04 | QQQ ON | M84 Jarak purata bergerak MAD 21/200 | ATR% >= 4 | H3 3xATR14 | X11 RSI14 < 50 ATAU X21 Stochastic silang turun di atas 80 |  |
| F33 | CS04 | SPY > SMA200 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 95 | H2 -10% | X13 RSI14 > 80 ATAU X21 Stochastic silang turun di atas 80 |  |
| F34 | CS04 | – | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) | RS >= 95 + ATR% >= 4 | H4 4xATR14 | X21 Stochastic silang turun di atas 80 ATAU X22 hari turun dengan volum >= 1.5x | ya |
| F35 | CS04 | – | M57 Landry Trend Knockout (TKO) | RS >= 95 + ATR% >= 4 | H4 4xATR14 | X08 MA10 < MA20 DAN X24 +DI < -DI |  |
| F36 | CS04 | – | M50 Elder Triple Screen (ditala 2) | RS >= 95 + ATR% >= 6 | H4 4xATR14 | X12 RSI14 silang turun bawah 70 ATAU X21 Stochastic silang turun di atas 80 |  |
| F37 | CS04 | QQQ OFF | M92 CCI-50 (ditala 2) | >= 20% di bawah puncak 52 minggu | H4 4xATR14 | X20 tutup < 92% tutup tertinggi sejak beli DAN X21 Stochastic silang turun di atas 80 |  |
| F38 | CS04 | – | P13 RSI14 silang atas 60 [tala daripada F29] | RS >= 95 + ATR% >= 4 | H2 -10% | X14 Supertrend turun ATAU X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli) | ya |
| F39 | CS05 | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | tutup > MA50 + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X09 MACD < isyarat DAN X21 Stochastic silang turun di atas 80 |  |
| F40 | CS05 | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (ditala 2) | Supertrend naik + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X14 Supertrend turun DAN X21 Stochastic silang turun di atas 80 |  |
| F41 | CS05 | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | ADX < 20 + ATR% >= 4 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F42 | CS05 | distribution day QQQ <= 2 dalam 25 sesi + >= 60% saham industri di atas MA50 | M159 Heikin-Ashi Trend (ditala 1) | RS >= 90 + ATR% >= 4 | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F43 | CS05 | Januari + tiada earnings dalam 20 sesi akan datang | M105 Supertrend tulen (ditala 2) | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F44 | CS05 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper (ditala 2) | templat trend Minervini + ATR% >= 4 | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F45 | CS05 | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | MACD > 0 + ATR% >= 4 | H4 4xATR14 | X12 RSI14 silang turun bawah 70 DAN X19 Chandelier 2xATR14 |  |
| F46 | CS05 | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | N124 Episodic pivot gap 8-10% | tutup > MA20 + RSI14 > 50 | H3 3xATR14 | X04 tutup < EMA10 DAN X12 RSI14 silang turun bawah 70 |  |
| F47 | CS05 | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | M124 'Last' Stochastic Technique (ChartSchool) (ditala 2) | Supertrend naik + volum hari isyarat >= 1.5x purata 50 | H3 3xATR14 | X04 tutup < EMA10 DAN X12 RSI14 silang turun bawah 70 |  |
| F48 | CS05 | >= 60% saham di atas MA50 + >= 60% saham sektor di atas MA50 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | dalam 15% dari puncak 52 minggu + ATR% >= 4 | H3 3xATR14 | X13 RSI14 > 80 DAN X21 Stochastic silang turun di atas 80 |  |
| F49 | CS05 | QQQ >= 10% di bawah puncak + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | MACD > isyarat + ATR% >= 4 | H4 4xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F50 | CS05 | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F51 | CS05 | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat | H4 4xATR14 | X10 histogram MACD turun 3 hari DAN X21 Stochastic silang turun di atas 80 |  |
| F52 | CS05 | Januari + tiada earnings dalam 20 sesi akan datang | M159 Heikin-Ashi Trend (ditala 2) | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | H4 4xATR14 | X12 RSI14 silang turun bawah 70 DAN X20 tutup < 92% tutup tertinggi sejak beli |  |
| F53 | CS05 | Januari + tiada earnings dalam 20 sesi akan datang | M79 Radge: 20% Flipper (ditala 2) | RSI14 > 50 + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F54 | CS05 | breadth thrust Zweig aktif (20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F55 | CS05 | turun-naik SPY 21 hari >= 25% setahun + sektor 3 terbawah (pulangan 63 sesi) | N75 RSI14 < 40 tanpa penapis | ADX < 20 + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X10 histogram MACD turun 3 hari DAN X21 Stochastic silang turun di atas 80 |  |
| F56 | CS05 | QQQ >= 10% di bawah puncak | M01 Bollinger Band + RSI (ditala 2) | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F57 | CS05 | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | ATR% >= 4 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F58 | CS06 | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | Supertrend naik + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F59 | CS06 | distribution day QQQ <= 2 dalam 25 sesi | P09 tutup silang atas MA20 | RS >= 70 + ATR% >= 4 | H2 -10% | X01 tutup < MA10 DAN X12 RSI14 silang turun bawah 70 |  |
| F60 | CS06 | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | N119 3 tutup turun berturut | RS >= 90 + ATR% >= 4 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 DAN X22 hari turun dengan volum >= 1.5x |  |
| F61 | CS06 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | N29 PSAR naik + tutup>MA50 | templat trend Minervini + ATR% >= 4 | H3 3xATR14 | X13 RSI14 > 80 |  |
| F62 | CS06 | QQQ >= 20% di bawah puncak | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 1) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X21 Stochastic silang turun di atas 80 |  |
| F63 | CS06 | QQQ OFF + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H4 4xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F64 | CS06 | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | M01 Bollinger Band + RSI (ditala 2) | ADX > 25 + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F65 | CS06 | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | P14 RSI14 silang atas 30 | RSI14 < 40 + volum 10 hari > volum 50 hari | H3 3xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F66 | CS06 | <= 30% saham di atas MA50 + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper (ditala 2) | >= 30% di bawah puncak 52 minggu + tutup dalam 25% teratas julat hari | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F67 | CS06 | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | N75 RSI14 < 40 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H2 -10% | X20 tutup < 92% tutup tertinggi sejak beli DAN X21 Stochastic silang turun di atas 80 |  |
| F68 | CS06 | breadth thrust Zweig aktif (20 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | ADX < 20 + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X20 tutup < 92% tutup tertinggi sejak beli DAN X21 Stochastic silang turun di atas 80 |  |
| F69 | CS06 | turun-naik SPY 21 hari >= 25% setahun | M28 VWAP Separator + Kiss Pivot (ditala 2) | >= 30% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F70 | CS06 | rejim ON baharu (<= 30 sesi) + earnings dalam 1-3 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari | tutup > MA50 + >= 20% di bawah puncak 52 minggu | H2 -10% | X13 RSI14 > 80 ATAU X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli) |  |
| F71 | CS06 | rejim ON baharu (<= 30 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales | Supertrend naik + >= 40% di bawah puncak 52 minggu | H3 3xATR14 | X12 RSI14 silang turun bawah 70 DAN X23 tutup < buka dan < rendah semalam |  |
| F72 | CS06 | >= 50% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | Supertrend naik + >= 20% di bawah puncak 52 minggu | H4 4xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F73 | CS06 | distribution day QQQ <= 3 dalam 25 sesi + >= 50% saham industri di atas MA50 | M159 Heikin-Ashi Trend | RS >= 80 + ATR% >= 5 | H3 3xATR14 | X13 RSI14 > 80 |  |
| F74 | CS06 | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) | MACD > 0 + ATR% >= 4 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 DAN X15 tutup < rendah 3 hari |  |
| F75 | CS06 | distribution day QQQ <= 3 dalam 25 sesi | P09 tutup silang atas MA20 | RS >= 70 + ATR% >= 5 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 DAN X23 tutup < buka dan < rendah semalam |  |
| F76 | CS06 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper | templat trend Minervini + ATR% >= 4 | H2 -10% | X09 MACD < isyarat DAN X21 Stochastic silang turun di atas 80 |  |
| F77 | CS06 | SPY atas SMA200 + >= 70% saham sektor di atas MA50 | N119 3 tutup turun berturut | RS >= 95 + ATR% >= 5 | H3 3xATR14 | X12 RSI14 silang turun bawah 70 ATAU X13 RSI14 > 80 |  |
| F78 | CS06 | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 10% | M124 'Last' Stochastic Technique (ChartSchool) | Supertrend naik + volum hari isyarat >= 1.5x purata 50 | H2 -10% | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F79 | CS06 | QQQ >= 20% di bawah puncak | M73 ADX(5) > 40 + Julat Terkecil 6 Hari | RSI14 < 40 + >= 20% di bawah puncak 52 minggu | H3 3xATR14 | X21 Stochastic silang turun di atas 80 |  |
| F80 | CS06 | QQQ >= 7.5% di bawah puncak + earnings dalam 1-7 sesi akan datang | N119 3 tutup turun berturut | MACD > isyarat + ATR% >= 5 | H2 -10% | X10 histogram MACD turun 3 hari DAN X21 Stochastic silang turun di atas 80 |  |
| F81 | CS06 | QQQ OFF + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat + >= 20% di bawah puncak 52 minggu | H3 3xATR14 | X08 MA10 < MA20 DAN X21 Stochastic silang turun di atas 80 |  |
| F82 | CS06 | Januari + tiada earnings dalam 20 sesi akan datang | M105 Supertrend tulen | MACD > isyarat + >= 40% di bawah puncak 52 minggu | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F83 | CS06 | turun-naik SPY 21 hari >= 20% setahun + kejutan untung terkini positif (SUE > 0) | M01 Bollinger Band + RSI | ADX > 25 + >= 40% di bawah puncak 52 minggu | H3 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F84 | CS06 | <= 40% saham di atas MA50 + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper | >= 40% di bawah puncak 52 minggu + tutup dalam 25% teratas julat hari | H3 3xATR14 | X12 RSI14 silang turun bawah 70 DAN X22 hari turun dengan volum >= 1.5x |  |
| F85 | CS06 | turun-naik SPY 21 hari >= 20% setahun + kejutan untung terkini positif (SUE > 0) | N75 RSI14 < 40 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H3 3xATR14 | X12 RSI14 silang turun bawah 70 |  |
| F86 | CS06 | breadth thrust Zweig aktif (20 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | ADX < 20 + >= 20% di bawah puncak 52 minggu | H3 3xATR14 | X21 Stochastic silang turun di atas 80 |  |
| F87 | CS06 | turun-naik SPY 21 hari >= 20% setahun | M28 VWAP Separator + Kiss Pivot | >= 50% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | H3 3xATR14 | X21 Stochastic silang turun di atas 80 |  |
| F88 | CS07 | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI (ditala 3) | tiada | G7 5xATR14 | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] |  |
| F89 | CS07 | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu + hari naik (tutup > buka) | G7 5xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F90 | CS07 | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M50 Elder Triple Screen | MACD > isyarat + >= 30% di bawah puncak 52 minggu | G7 5xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F91 | CS07 | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu | G7 5xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F92 | CS07 | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI | tiada | G7 5xATR14 | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] |  |
| F93 | CS07 | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M02 MACD + SMA200 | tutup > MA200 + MA50 naik (lawan 20 bar lalu) | G5 3xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F94 | CS07 | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | K11.016 Supertrend(20, 1.5) bertukar naik | RS >= 90 + dalam 15% dari puncak 52 minggu | G7 5xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |
| F95 | CS07 | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K19.011 pecah atas Keltner(30, 1.0) | RSI14 > 60 + RS >= 90 | G7 5xATR14 | X00 tiada keluar indikator (henti + 20 sesi) |  |

## Kaveat

- `F23`/`F33` (benih M21) memakai harga SPY di dalam peraturan kaedah itu sendiri, selain prasyarat SPY > SMA200. Kaedah M lain belum diperiksa satu per satu pada tahap ini.
- Prasyarat lain (keluasan, turun-naik, sektor, industri, earnings, kalendar, takrif pakar) masuk ruang carian mulai CS05 (`hasil/CS05/LAPORAN.md`); tinjauan asalnya dalam `LAPORAN.md` folder ini (pindaan (h)).
