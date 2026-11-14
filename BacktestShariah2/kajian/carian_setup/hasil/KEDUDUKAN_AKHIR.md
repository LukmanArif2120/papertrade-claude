# Kedudukan akhir semua setup F (backtest pada saham yang tidak dilihat; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_akhir.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (m), dikomit sebelum dijalankan. **Jangan sunting secara manual.**

## 1. Apa yang dicari, dan cara membaca jadual

Matlamat: setup lengkap (prasyarat → syarat → pegang → keluar, dengan henti rugi) yang paling kerap menangkap saham yang **naik ≥ 5 % pada minggu pertama (lebih baik 10 %), kemudian naik lagi hingga minggu ke-4**. Setiap setup dinilai dengan henti dan keluarnya sendiri pada kumpulan B (saham yang carian tidak lihat), 20100104 – 20260828. Lajur corong = daripada 100 belian, berapa yang sampai ke setiap peringkat; angka dalam kurungan = saham rawak pada hari dan tahap turun-naik yang sama.

- **Pegang minimum (pindaan (p), syarat pengguna 14 Nov 2026):** tiada jualan pada hari beli; indikator keluar hanya boleh menjual mulai buka sesi ke-4 (beli Isnin → paling awal Khamis); henti rugi kekal aktif sejak sesi ke-2. Semua angka di bawah dikira dengan peraturan ini. Lajur "jual awal" = belian yang dijual sebelum sesi ke-4 (henti rugi sahaja).
- Saham rawak (mana-mana hari): naik ≥ 5 % minggu pertama 12.5 %; ≥ 10 % minggu pertama 3.3 %; **naik lagi hingga minggu ke-4 6.3 %**.
- **Dipercayai** = belian ≥ 300 DAN berdagang dalam ≥ 10 tahun DAN mengatasi rawak dalam K1 (2010–19), K2 (2020–24) dan K3 (2025–26). Setup dipercayai disusun dahulu, kemudian ikut lajur "naik lagi".
- **Liputan** = daripada semua 67,638 episod "naik lagi" dalam kumpulan B, berapa peratus yang dibeli setup itu. Tangkapan setahun = bilangan belian setahun yang benar-benar naik lagi.

## 2. Kedudukan (69 setup; 42 dipercayai)

| # | ID | Prasyarat | Pencetus | Penapis saham | Henti · keluar | Belian (setahun) | Naik ≥ 5 % minggu 1 % | ≥ 10 % minggu 1 % | **Naik lagi hingga minggu 4 %** | Tangkap penuh % | Menang % | Rugi ≥ 8 % % | Jual awal % | Tangkapan setahun | Tahun aktif | Liputan % | Dipercayai | Jejak hadapan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `F43` | Januari + tiada earnings dalam 20 sesi akan datang | M105 Supertrend tulen (ditala 2) | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H4 · X00 | 515 (31) | 33.6 (28.9) | 11.1 (9.4) | **25.2** (19.8) | 22.7 (18.8) | 70 | 17 | 0.4 | 7.8 | 16 | 0.19 | **ya** |  |
| 2 | `F63` | QQQ OFF + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H4 · X00 | 431 (26) | 37.8 (29.3) | 22.0 (12.7) | **21.8** (15.9) | 25.5 (17.2) | 61 | 26 | 4.9 | 5.7 | 15 | 0.14 | **ya** |  |
| 3 | `F65` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | P14 RSI14 silang atas 30 | RSI14 < 40 + volum 10 hari > volum 50 hari | H3 · X12 | 428 (26) | 38.1 (29.3) | 17.1 (9.9) | **21.7** (16.0) | 21.7 (14.9) | 63 | 25 | 8.2 | 5.6 | 13 | 0.14 | **ya** |  |
| 4 | `F51` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | MACD > isyarat | H4 · X10 DAN X21 | 733 (44) | 35.7 (30.1) | 16.8 (11.8) | **20.7** (15.5) | 22.0 (15.5) | 65 | 19 | 4.4 | 9.1 | 10 | 0.22 | **ya** |  |
| 5 | `F50` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | H4 · X00 | 707 (43) | 42.0 (34.6) | 25.3 (14.9) | **20.7** (18.1) | 26.7 (19.3) | 58 | 26 | 4.8 | 8.8 | 12 | 0.22 | **ya** |  |
| 6 | `F56` | QQQ >= 10% di bawah puncak | M01 Bollinger Band + RSI (ditala 2) | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H4 · X00 | 1,943 (117) | 34.6 (32.2) | 18.0 (14.7) | **19.0** (16.7) | 22.1 (19.1) | 60 | 23 | 0.7 | 22.2 | 13 | 0.55 | **ya** |  |
| 7 | `F39` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | tutup > MA50 + >= 30% di bawah puncak 52 minggu | H3 · X09 DAN X21 | 501 (30) | 38.5 (23.9) | 20.8 (8.8) | **18.2** (11.0) | 21.4 (10.4) | 51 | 33 | 7.8 | 5.5 | 17 | 0.13 | **ya** |  |
| 8 | `F91` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu | G7 · X00 | 366 (22) | 34.7 (21.3) | 17.2 (8.1) | **18.0** (10.2) | 19.9 (9.9) | 54 | 28 | 2.2 | 4.0 | 16 | 0.10 | **ya** |  |
| 9 | `F40` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (ditala 2) | Supertrend naik + >= 30% di bawah puncak 52 minggu | H3 · X14 DAN X21 | 597 (36) | 39.4 (24.3) | 23.8 (9.6) | **17.9** (10.9) | 21.9 (10.3) | 51 | 32 | 7.5 | 6.4 | 17 | 0.16 | **ya** |  |
| 10 | `F89` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | >= 30% di bawah puncak 52 minggu + hari naik (tutup > buka) | G7 · X00 | 383 (23) | 34.2 (21.3) | 17.0 (8.1) | **17.5** (10.2) | 18.5 (9.9) | 54 | 29 | 2.3 | 4.0 | 16 | 0.10 | **ya** |  |
| 11 | `F90` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M50 Elder Triple Screen | MACD > isyarat + >= 30% di bawah puncak 52 minggu | G7 · X00 | 303 (18) | 36.6 (23.4) | 21.1 (9.2) | **17.2** (10.0) | 19.1 (9.7) | 48 | 31 | 1.3 | 3.1 | 17 | 0.08 | **ya** |  |
| 12 | `F88` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI (ditala 3) | – | G7 · Y08.10 ATAU Y09.4@10 | 461 (28) | 26.7 (16.6) | 12.6 (4.8) | **16.1** (9.6) | 17.8 (8.9) | 60 | 19 | 2.8 | 4.5 | 17 | 0.11 | **ya** |  |
| 13 | `F92` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI | – | G7 · Y08.10 ATAU Y09.4@10 | 377 (23) | 25.5 (17.0) | 10.6 (5.0) | **15.9** (9.8) | 16.2 (9.0) | 59 | 18 | 3.2 | 3.6 | 17 | 0.09 | **ya** |  |
| 14 | `F58` | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | Supertrend naik + >= 30% di bawah puncak 52 minggu | H3 · X12 | 379 (23) | 34.8 (18.1) | 21.4 (6.5) | **15.6** (7.8) | 22.2 (7.4) | 47 | 36 | 6.9 | 3.5 | 17 | 0.09 | **ya** |  |
| 15 | `F41` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | ADX < 20 + ATR% >= 4 | H3 · X12 | 926 (56) | 31.5 (22.0) | 20.2 (8.7) | **15.4** (10.0) | 19.2 (10.0) | 46 | 40 | 6.2 | 8.6 | 16 | 0.21 | **ya** |  |
| 16 | `F45` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | MACD > 0 + ATR% >= 4 | H4 · X12 DAN X19 | 793 (48) | 31.3 (27.2) | 15.5 (11.8) | **14.6** (11.6) | 16.9 (12.1) | 54 | 26 | 0.8 | 7.0 | 17 | 0.17 | **ya** |  |
| 17 | `F27` | – | N73 Tutup bawah jalur bawah BB(20,2) | RS >= 70 + ATR% >= 4 | H4 · X07 DAN X21 | 4,857 (292) | 27.7 (24.6) | 11.7 (9.8) | **14.4** (12.1) | 14.8 (12.5) | 54 | 27 | 1.4 | 42.1 | 17 | 1.03 | **ya** | ya |
| 18 | `F03` | – | M01 Bollinger Band + RSI (ditala 2) | RS >= 70 + >= 30% di bawah puncak 52 minggu | H4 · X20 DAN X21 | 1,249 (75) | 32.7 (26.9) | 16.3 (12.0) | **14.2** (13.7) | 17.6 (14.8) | 54 | 29 | 0.5 | 10.6 | 17 | 0.26 | **ya** |  |
| 19 | `F07` | QQQ OFF | M30 BB Free Bar + Himpitan 50/2.5 | ATR% >= 4 | H4 · X13 | 1,031 (62) | 25.1 (23.6) | 10.8 (8.9) | **14.1** (12.7) | 15.7 (12.4) | 54 | 27 | 0.8 | 8.7 | 17 | 0.21 | **ya** |  |
| 20 | `F11` | QQQ OFF | M01 Bollinger Band + RSI (ditala 2) | >= 30% di bawah puncak 52 minggu | H4 · X04 DAN X12 | 10,261 (617) | 26.4 (23.9) | 11.1 (9.4) | **14.0** (12.6) | 14.7 (13.2) | 56 | 25 | 1.1 | 86.4 | 17 | 2.12 | **ya** |  |
| 21 | `F95` | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K19.011 pecah atas Keltner(30, 1.0) | RSI14 > 60 + RS >= 90 | G7 · X00 | 330 (20) | 28.2 (17.3) | 16.7 (6.8) | **13.6** (7.5) | 16.1 (7.3) | 52 | 25 | 2.7 | 2.7 | 17 | 0.07 | **ya** |  |
| 22 | `F10` | – | P16 RSI2<5 atas MA200 | volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 | H3 · X12 ATAU X19 | 2,374 (143) | 27.7 (22.7) | 11.6 (8.4) | **13.4** (10.4) | 12.1 (9.3) | 45 | 30 | 1.9 | 19.1 | 17 | 0.47 | **ya** |  |
| 23 | `F24` | – | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (ditala 2) | RS >= 90 + ATR% >= 4 | H4 · X11 DAN X22 | 2,486 (150) | 25.9 (21.3) | 11.5 (7.8) | **13.0** (10.4) | 13.0 (9.5) | 47 | 32 | 0.9 | 19.4 | 17 | 0.48 | **ya** | ya |
| 24 | `F93` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M02 MACD + SMA200 | tutup > MA200 + MA50 naik (lawan 20 bar lalu) | G5 · X00 | 363 (22) | 22.3 (12.4) | 9.6 (3.2) | **12.9** (6.6) | 12.4 (5.4) | 49 | 22 | 9.6 | 2.8 | 17 | 0.07 | **ya** |  |
| 25 | `F42` | distribution day QQQ <= 2 dalam 25 sesi + >= 60% saham industri di atas MA50 | M159 Heikin-Ashi Trend (ditala 1) | RS >= 90 + ATR% >= 4 | H3 · X00 | 305 (18) | 24.9 (17.5) | 11.8 (6.0) | **12.8** (8.5) | 15.7 (8.1) | 53 | 29 | 1.3 | 2.3 | 13 | 0.06 | **ya** |  |
| 26 | `F22` | QQQ ON | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | ATR% >= 4 | H2 · X11 ATAU X21 | 2,853 (172) | 26.9 (23.5) | 13.7 (10.2) | **12.7** (10.2) | 12.1 (8.6) | 42 | 26 | 14.3 | 21.8 | 17 | 0.53 | **ya** | ya |
| 27 | `F16` | – | N38 VCP pecah | ATR% >= 4 + tutup dalam 25% teratas julat hari | H4 · X21 DAN X22 | 4,478 (269) | 25.1 (22.1) | 10.3 (8.0) | **12.7** (11.2) | 13.0 (10.8) | 53 | 28 | 0.4 | 34.1 | 17 | 0.84 | **ya** |  |
| 28 | `F02` | QQQ OFF | M111 Sistem Volatiliti Wilder (ditala 2) | >= 30% di bawah puncak 52 minggu | H4 · X08 DAN X22 | 2,029 (122) | 21.5 (19.8) | 7.8 (6.4) | **12.4** (11.4) | 12.9 (10.3) | 56 | 24 | 0.7 | 15.1 | 17 | 0.37 | **ya** |  |
| 29 | `F60` | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | N119 3 tutup turun berturut | RS >= 90 + ATR% >= 4 | H3 · X12 DAN X22 | 3,218 (194) | 25.3 (19.4) | 11.5 (6.9) | **12.3** (9.2) | 13.7 (9.0) | 49 | 33 | 1.4 | 23.8 | 17 | 0.58 | **ya** |  |
| 30 | `F48` | >= 60% saham di atas MA50 + >= 60% saham sektor di atas MA50 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | dalam 15% dari puncak 52 minggu + ATR% >= 4 | H3 · X13 DAN X21 | 1,163 (70) | 25.9 (21.4) | 11.7 (8.4) | **12.3** (9.3) | 14.3 (9.2) | 48 | 35 | 3.2 | 8.6 | 17 | 0.21 | **ya** |  |
| 31 | `F44` | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper (ditala 2) | templat trend Minervini + ATR% >= 4 | H3 · X00 | 615 (37) | 25.2 (20.5) | 11.7 (7.9) | **12.2** (9.9) | 13.8 (10.0) | 48 | 36 | 1.8 | 4.5 | 17 | 0.11 | **ya** |  |
| 32 | `F06` | – | N07 Tiga MA tersusun | ADX < 20 + ATR% >= 4 | H4 · X18 DAN X22 | 5,206 (313) | 24.7 (22.0) | 10.1 (8.2) | **12.1** (10.5) | 12.3 (10.4) | 52 | 29 | 0.6 | 38.0 | 17 | 0.93 | **ya** |  |
| 33 | `F29` | – | P13 RSI14 silang atas 60 | RS >= 90 + ATR% >= 4 | H2 · X21 DAN X22 | 4,605 (277) | 25.3 (21.2) | 11.5 (8.0) | **11.7** (10.0) | 11.9 (9.6) | 40 | 50 | 13.9 | 32.4 | 17 | 0.79 | **ya** |  |
| 34 | `F01` | – | N203 | Supertrend naik + ATR% >= 4 | H4 · X03 DAN X22 | 1,970 (119) | 24.0 (21.3) | 9.3 (7.9) | **11.7** (10.5) | 12.0 (10.2) | 52 | 29 | 0.5 | 13.8 | 17 | 0.34 | **ya** |  |
| 35 | `F25` | – | M57 Landry Trend Knockout (TKO) (ditala 1) | RS >= 90 + ATR% >= 4 | H4 · X22 DAN X24 | 3,273 (197) | 24.7 (21.3) | 10.6 (7.9) | **11.6** (9.9) | 12.1 (9.2) | 44 | 34 | 0.8 | 22.9 | 17 | 0.56 | **ya** |  |
| 36 | `F61` | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | N29 PSAR naik + tutup>MA50 | templat trend Minervini + ATR% >= 4 | H3 · X13 | 1,460 (88) | 23.8 (20.3) | 9.6 (7.7) | **11.4** (9.5) | 12.3 (9.7) | 49 | 35 | 2.5 | 10.0 | 17 | 0.25 | **ya** |  |
| 37 | `F05` | – | P07 MA20 silang atas MA50 | Supertrend naik + ATR% >= 4 | H4 · X14 DAN X22 | 5,549 (334) | 24.1 (21.6) | 9.7 (7.9) | **11.4** (10.5) | 11.7 (10.1) | 51 | 30 | 0.5 | 38.1 | 17 | 0.94 | **ya** |  |
| 38 | `F28` | QQQ OFF | M92 CCI-50 (ditala 2) | >= 30% di bawah puncak 52 minggu | H4 · X20 DAN X21 | 2,739 (165) | 22.0 (20.1) | 8.4 (6.8) | **11.4** (10.8) | 11.5 (10.2) | 52 | 29 | 0.7 | 18.8 | 17 | 0.46 | **ya** | ya |
| 39 | `F09` | – | M140 猎豹出击 (Serangan Cheetah) (ditala 1) | ATR% >= 4 + hari naik (tutup > buka) | H4 · X14 DAN X22 | 2,965 (178) | 24.4 (21.9) | 10.4 (8.1) | **11.3** (10.6) | 11.4 (10.1) | 49 | 30 | 0.5 | 20.2 | 17 | 0.50 | **ya** |  |
| 40 | `F30` | – | N43 Undur EMA8 + penapis MA50 | Supertrend naik + ATR% >= 4 | H4 · X21 DAN X22 | 10,989 (661) | 24.2 (21.6) | 10.3 (8.0) | **11.2** (10.3) | 11.8 (10.1) | 51 | 28 | 0.4 | 73.8 | 17 | 1.81 | **ya** | ya |
| 41 | `F08` | – | N201 | Supertrend naik + ATR% >= 4 | H4 · X18 DAN X22 | 4,977 (299) | 23.6 (21.4) | 9.4 (7.7) | **10.9** (10.4) | 11.1 (10.2) | 50 | 30 | 0.4 | 32.7 | 17 | 0.80 | **ya** |  |
| 42 | `F94` | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | K11.016 Supertrend(20, 1.5) bertukar naik | RS >= 90 + dalam 15% dari puncak 52 minggu | G7 · X00 | 380 (23) | 23.2 (15.5) | 12.6 (5.1) | **10.0** (7.1) | 13.2 (6.7) | 44 | 31 | 3.4 | 2.3 | 17 | 0.06 | **ya** |  |
| 43 | `F62` | QQQ >= 20% di bawah puncak | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 1) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | H3 · X21 | 1,387 (83) | 48.7 (45.7) | 28.9 (26.1) | **26.2** (23.9) | 35.5 (31.2) | 73 | 16 | 1.7 | 21.8 | 5 | 0.54 | tidak |  |
| 44 | `F52` | Januari + tiada earnings dalam 20 sesi akan datang | M159 Heikin-Ashi Trend (ditala 2) | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | H4 · X12 DAN X20 | 696 (42) | 36.8 (32.1) | 15.2 (12.9) | **23.9** (20.9) | 24.0 (20.7) | 64 | 20 | 0.1 | 10.0 | 16 | 0.25 | tidak |  |
| 45 | `F64` | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | M01 Bollinger Band + RSI (ditala 2) | ADX > 25 + >= 30% di bawah puncak 52 minggu | H3 · X00 | 725 (44) | 36.8 (35.2) | 20.7 (19.0) | **22.9** (20.7) | 27.3 (25.8) | 69 | 19 | 3.7 | 10.0 | 7 | 0.25 | tidak |  |
| 46 | `F67` | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | N75 RSI14 < 40 tanpa penapis | MACD > isyarat + >= 30% di bawah puncak 52 minggu | H2 · X20 DAN X21 | 645 (39) | 36.9 (36.7) | 21.1 (18.9) | **22.3** (21.8) | 23.6 (23.0) | 56 | 34 | 15.7 | 8.7 | 7 | 0.21 | tidak |  |
| 47 | `F49` | QQQ >= 10% di bawah puncak + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | MACD > isyarat + ATR% >= 4 | H4 · X12 | 1,069 (64) | 43.2 (38.6) | 27.6 (17.8) | **21.7** (19.9) | 30.3 (23.0) | 65 | 21 | 2.6 | 14.0 | 13 | 0.34 | tidak |  |
| 48 | `F57` | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | ATR% >= 4 | H3 · X12 | 542 (33) | 33.0 (31.8) | 12.5 (11.5) | **21.4** (20.8) | 21.2 (22.0) | 70 | 19 | 1.7 | 7.0 | 6 | 0.17 | tidak |  |
| 49 | `F53` | Januari + tiada earnings dalam 20 sesi akan datang | M79 Radge: 20% Flipper (ditala 2) | RSI14 > 50 + >= 30% di bawah puncak 52 minggu | H3 · X00 | 340 (20) | 31.5 (27.0) | 11.2 (9.2) | **21.2** (17.4) | 20.3 (16.7) | 65 | 21 | 0.6 | 4.3 | 17 | 0.11 | tidak |  |
| 50 | `F55` | turun-naik SPY 21 hari >= 25% setahun + sektor 3 terbawah (pulangan 63 sesi) | N75 RSI14 < 40 tanpa penapis | ADX < 20 + >= 30% di bawah puncak 52 minggu | H4 · X10 DAN X21 | 484 (29) | 38.4 (36.1) | 20.5 (17.4) | **20.5** (21.2) | 24.6 (23.7) | 74 | 12 | 0.2 | 6.0 | 8 | 0.15 | tidak |  |
| 51 | `F54` | breadth thrust Zweig aktif (20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | RSI14 < 40 + >= 30% di bawah puncak 52 minggu | H4 · X12 | 548 (33) | 30.5 (28.0) | 12.8 (10.7) | **19.3** (17.3) | 19.9 (17.3) | 63 | 19 | 0.2 | 6.4 | 14 | 0.16 | tidak |  |
| 52 | `F68` | breadth thrust Zweig aktif (20 sesi) | N73 Tutup bawah jalur bawah BB(20,2) | ADX < 20 + >= 30% di bawah puncak 52 minggu | H3 · X20 DAN X21 | 637 (38) | 28.7 (28.4) | 11.5 (10.9) | **18.5** (18.0) | 18.5 (17.7) | 57 | 28 | 2.2 | 7.1 | 14 | 0.17 | tidak |  |
| 53 | `F69` | turun-naik SPY 21 hari >= 25% setahun | M28 VWAP Separator + Kiss Pivot (ditala 2) | >= 30% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | H3 · X00 | 1,619 (97) | 33.0 (33.3) | 20.4 (18.6) | **15.3** (16.2) | 23.7 (22.6) | 62 | 24 | 6.1 | 14.9 | 8 | 0.37 | tidak |  |
| 54 | `F66` | <= 30% saham di atas MA50 + kejutan untung terkini positif (SUE > 0) | M79 Radge: 20% Flipper (ditala 2) | >= 30% di bawah puncak 52 minggu + tutup dalam 25% teratas julat hari | H3 · X00 | 733 (44) | 31.4 (32.3) | 16.1 (18.0) | **14.2** (15.0) | 22.6 (22.6) | 66 | 22 | 2.3 | 6.3 | 14 | 0.15 | tidak |  |
| 55 | `F15` | QQQ OFF | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 1) | >= 30% di bawah puncak 52 minggu | H4 · X04 DAN X12 | 5,800 (349) | 27.8 (26.6) | 12.2 (11.2) | **14.1** (13.6) | 16.1 (15.0) | 57 | 24 | 0.8 | 49.1 | 17 | 1.21 | tidak |  |
| 56 | `F59` | distribution day QQQ <= 2 dalam 25 sesi | P09 tutup silang atas MA20 | RS >= 70 + ATR% >= 4 | H2 · X01 DAN X12 | 316 (19) | 23.7 (19.7) | 11.7 (7.9) | **13.6** (9.0) | 13.6 (8.8) | 45 | 45 | 10.1 | 2.6 | 13 | 0.06 | tidak |  |
| 57 | `F23` | SPY > SMA200 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 90 | H2 · X12 DAN X16 | 650 (39) | 28.9 (21.7) | 16.6 (7.9) | **13.1** (10.3) | 14.0 (9.9) | 35 | 58 | 24.3 | 5.1 | 17 | 0.13 | tidak |  |
| 58 | `F14` | QQQ OFF | N28 ADX>25 + DI+ > DI- | >= 30% di bawah puncak 52 minggu | H4 · X09 DAN X21 | 6,550 (394) | 26.5 (24.7) | 11.2 (10.1) | **12.7** (12.3) | 14.5 (13.5) | 56 | 24 | 1.0 | 49.9 | 17 | 1.23 | tidak |  |
| 59 | `F12` | QQQ OFF | M88 O'Neil Shakeout +3 (ditala 1) | >= 30% di bawah puncak 52 minggu | H4 · X12 ATAU X13 | 3,182 (191) | 28.4 (26.8) | 13.6 (11.7) | **12.6** (12.8) | 15.4 (15.0) | 58 | 23 | 1.0 | 24.2 | 17 | 0.59 | tidak |  |
| 60 | `F18` | QQQ OFF | N75 RSI14 < 40 tanpa penapis | >= 30% di bawah puncak 52 minggu | H4 · X13 DAN X21 | 11,346 (683) | 24.3 (23.5) | 10.4 (9.1) | **12.5** (12.3) | 13.1 (12.6) | 54 | 27 | 0.7 | 85.5 | 17 | 2.10 | tidak |  |
| 61 | `F17` | QQQ OFF | P14 RSI14 silang atas 30 | >= 30% di bawah puncak 52 minggu | H4 · X13 | 7,473 (450) | 24.6 (23.7) | 9.6 (9.1) | **12.2** (11.9) | 13.2 (12.7) | 57 | 24 | 0.9 | 54.8 | 17 | 1.35 | tidak |  |
| 62 | `F26` | – | M50 Elder Triple Screen (ditala 2) | RS >= 90 + ATR% >= 4 | H4 · X12 ATAU X22 | 3,857 (232) | 25.3 (21.3) | 10.9 (7.9) | **11.3** (9.7) | 12.3 (9.1) | 48 | 29 | 0.9 | 26.2 | 17 | 0.64 | tidak |  |
| 63 | `F46` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | N124 Episodic pivot gap 8-10% | tutup > MA20 + RSI14 > 50 | H3 · X04 DAN X12 | 278 (17) | 21.6 (18.4) | 8.6 (6.6) | **11.2** (9.3) | 11.5 (8.8) | 55 | 26 | 2.9 | 1.9 | 17 | 0.05 | tidak |  |
| 64 | `F04` | QQQ OFF | M79 Radge: 20% Flipper (ditala 1) | volum hari isyarat >= 1.5x purata 50 | H4 · X12 DAN X20 | 2,748 (165) | 23.7 (24.1) | 11.2 (10.5) | **11.0** (11.8) | 13.3 (14.0) | 55 | 26 | 0.9 | 18.2 | 17 | 0.45 | tidak |  |
| 65 | `F21` | – | N40 OBV tinggi baharu + MA50 | tutup > MA200 + >= 30% di bawah puncak 52 minggu | H2 · X09 ATAU X10 | 1,054 (63) | 21.5 (20.0) | 9.7 (7.3) | **9.9** (9.8) | 7.6 (6.0) | 36 | 18 | 12.0 | 6.3 | 17 | 0.15 | tidak | ya |
| 66 | `F47` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | M124 'Last' Stochastic Technique (ChartSchool) (ditala 2) | Supertrend naik + volum hari isyarat >= 1.5x purata 50 | H3 · X04 DAN X12 | 393 (24) | 17.3 (16.9) | 5.6 (5.5) | **8.9** (9.0) | 9.7 (8.0) | 53 | 26 | 5.3 | 2.1 | 17 | 0.05 | tidak |  |
| 67 | `F19` | QQQ OFF | P02 MACD silang naik bawah sifar | RSI14 > 60 | H4 · X14 DAN X23 | 684 (41) | 12.9 (15.4) | 3.7 (4.6) | **7.5** (8.8) | 5.3 (6.8) | 57 | 15 | 0.7 | 3.1 | 17 | 0.08 | tidak |  |
| 68 | `F20` | QQQ OFF | M141 First Thrust (Landry) (ditala 1) | MACD > isyarat | H4 · X18 DAN X22 | 1,144 (69) | 12.8 (15.6) | 2.5 (4.1) | **7.2** (9.0) | 6.6 (7.9) | 58 | 18 | 1.0 | 4.9 | 17 | 0.12 | tidak |  |
| 69 | `F13` | QQQ OFF | M02 MACD + SMA200 | RSI14 > 60 | H4 · X08 DAN X20 | 551 (33) | 12.5 (15.0) | 3.4 (4.4) | **6.7** (8.8) | 5.3 (7.5) | 60 | 16 | 0.5 | 2.2 | 17 | 0.05 | tidak |  |

Tidak dinilai (26): F31, F32, F33, F34, F35, F36, F37, F38, F70, F71, F72, F73, F74, F75, F76, F77, F78, F79, F80, F81, F82, F83, F84, F85, F86, F87 (anak tala `F31`–`F38`, `F70`–`F87`: memerlukan varian tala; tala terbukti tidak menolong).

## 3. Setup dipercayai: sumbangan setiap komponen, mutu pegang, saham Shariah

Komponen: ✓ = membuang komponen itu MENURUNKAN kelebihan "naik lagi" (ia menyumbang); ✗ = tidak; angka = kelebihan setup penuh → tanpa komponen (mata peratus). Mutu pegang = purata untung setiap belian yang naik lagi: dengan keluar setup / jika dipegang sahaja 20 sesi / puncak tutup dalam 20 sesi. Shariah = belian pada saham dalam senarai Shariah semasa.

| ID | Prasyarat pasaran | Prasyarat syarikat | Penapis 1 | Penapis 2 | Pencetus | Mutu pegang: keluar setup / pegang 20 sesi / puncak % | Shariah: belian · naik lagi % (rawak) · tangkap penuh % · menang % |
|---|---|---|---|---|---|---|---|
| `F43` | ✓ +5.4 → +0.0 | ✓ +5.4 → +3.6 | ✓ +5.4 → +4.1 | ✓ +5.4 → +0.4 | ✓ +5.4 → +1.0 | +20.4 / +20.4 / +23.2 | 153 · 28.8 (20.0) · 24.8 · 76 |
| `F63` | ✗ +5.9 → +6.0 | ✓ +5.9 → +1.8 | ✗ +5.9 → +6.0 | ✓ +5.9 → +5.2 | ✓ +5.9 → +5.8 | +25.8 / +25.8 / +30.2 | 125 · 30.4 (15.6) · 32.0 · 67 |
| `F65` | ✓ +5.9 → +5.4 | ✓ +5.9 → +0.1 | ✓ +5.9 → +5.8 | ✗ +5.9 → +5.9 | ✓ +5.9 → +4.9 | +18.4 / +19.1 / +21.3 | 144 · 19.4 (16.3) · 22.9 · 60 |
| `F51` | ✓ +5.2 → +5.0 | ✓ +5.2 → +1.4 | ✗ +5.2 → +6.1 | – | ✓ +5.2 → +5.2 | +21.1 / +22.0 / +26.6 | 213 · 23.5 (14.7) · 24.4 · 63 |
| `F50` | ✗ +2.5 → +4.1 | ✓ +2.5 → +1.1 | ✗ +2.5 → +3.9 | ✗ +2.5 → +4.4 | ✗ +2.5 → +3.6 | +24.4 / +24.4 / +28.4 | 226 · 23.0 (18.2) · 28.8 · 63 |
| `F56` | ✓ +2.2 → +1.6 | – | ✓ +2.2 → +1.2 | ✓ +2.2 → +1.0 | ✓ +2.2 → +0.7 | +24.5 / +24.5 / +29.1 | 668 · 19.2 (16.4) · 22.0 · 59 |
| `F39` | ✓ +7.2 → +5.8 | ✓ +7.2 → +0.5 | ✓ +7.2 → +4.9 | ✓ +7.2 → +5.8 | ✓ +7.2 → +6.7 | +20.9 / +21.1 / +25.6 | 144 · 15.3 (10.9) · 19.4 · 51 |
| `F91` | ✓ +7.8 → +6.4 | ✓ +7.8 → +0.8 | ✓ +7.8 → +5.6 | – | ✓ +7.8 → +5.7 | +27.1 / +27.1 / +33.0 | 96 · 17.7 (9.5) · 17.7 · 59 |
| `F40` | ✓ +7.0 → +6.5 | ✓ +7.0 → +0.9 | ✓ +7.0 → +6.5 | ✓ +7.0 → +5.4 | ✗ +7.0 → +7.2 | +22.8 / +22.8 / +27.6 | 162 · 16.0 (10.6) · 18.5 · 49 |
| `F89` | ✓ +7.3 → +5.8 | ✓ +7.3 → +0.8 | ✓ +7.3 → +5.6 | ✗ +7.3 → +7.8 | ✓ +7.3 → +5.4 | +25.7 / +25.7 / +31.1 | 98 · 18.4 (9.5) · 17.3 · 56 |
| `F90` | ✓ +7.2 → +5.5 | ✓ +7.2 → +1.6 | ✓ +7.2 → +7.0 | ✓ +7.2 → +4.7 | ✓ +7.2 → +5.7 | +22.8 / +22.8 / +27.7 | 93 · 16.1 (9.4) · 18.3 · 45 |
| `F88` | ✓ +6.5 → +4.5 | ✓ +6.5 → +0.1 | – | – | ✓ +6.5 → +5.7 | +17.0 / +19.0 / +22.6 | 148 · 13.5 (8.6) · 16.9 · 56 |
| `F92` | ✓ +6.1 → +4.6 | ✓ +6.1 → +0.4 | – | – | ✓ +6.1 → +5.7 | +16.9 / +18.9 / +22.2 | 122 · 14.8 (9.2) · 16.4 · 57 |
| `F58` | ✓ +7.8 → +7.6 | ✓ +7.8 → +1.2 | ✓ +7.8 → +5.9 | ✓ +7.8 → +5.3 | ✓ +7.8 → +6.1 | +20.3 / +22.9 / +27.3 | 110 · 10.9 (7.4) · 20.9 · 45 |
| `F41` | ✓ +5.5 → +3.7 | ✓ +5.5 → +1.3 | ✓ +5.5 → +5.1 | ✗ +5.5 → +5.8 | ✓ +5.5 → +5.3 | +24.3 / +28.1 / +33.3 | 250 · 18.0 (9.7) · 22.4 · 50 |
| `F45` | ✓ +3.1 → +2.1 | ✓ +3.1 → +1.8 | ✓ +3.1 → +1.7 | ✓ +3.1 → +0.6 | ✓ +3.1 → +1.6 | +25.8 / +26.3 / +33.0 | 233 · 12.9 (11.5) · 14.2 · 56 |
| `F27` | – | – | ✓ +2.2 → +1.4 | ✓ +2.2 → +0.8 | ✓ +2.2 → +1.3 | +23.3 / +23.4 / +27.7 | 1,620 · 15.2 (12.4) · 15.9 · 57 |
| `F03` | – | – | ✗ +0.6 → +1.1 | ✗ +0.6 → +0.9 | ✗ +0.6 → +0.7 | +28.5 / +29.1 / +34.4 | 337 · 17.8 (16.3) · 20.5 · 60 |
| `F07` | – | – | ✓ +1.4 → +0.4 | ✓ +1.4 → +1.1 | ✓ +1.4 → +0.6 | +21.7 / +25.8 / +29.8 | 325 · 15.4 (11.7) · 16.3 · 55 |
| `F11` | – | – | ✓ +1.3 → +0.5 | ✓ +1.3 → +1.1 | ✓ +1.3 → +0.7 | +22.8 / +22.8 / +27.0 | 3,417 · 14.9 (13.2) · 15.4 · 58 |
| `F95` | ✓ +6.1 → +4.3 | ✓ +6.1 → +1.2 | ✓ +6.1 → +4.8 | ✓ +6.1 → +5.0 | ✗ +6.1 → +6.3 | +27.3 / +27.3 / +30.7 | 114 · 14.0 (6.7) · 16.7 · 57 |
| `F10` | – | – | ✓ +3.0 → +2.2 | ✓ +3.0 → +0.9 | ✓ +3.0 → +0.9 | +20.0 / +21.5 / +25.9 | 773 · 15.4 (10.6) · 13.3 · 47 |
| `F24` | – | – | ✓ +2.4 → +1.1 | ✓ +2.4 → +1.5 | ✓ +2.4 → +1.7 | +24.9 / +26.0 / +31.5 | 760 · 13.9 (10.5) · 13.8 · 49 |
| `F93` | ✓ +6.4 → +5.5 | ✓ +6.4 → -0.4 | ✓ +6.4 → +6.3 | ✓ +6.4 → +5.9 | ✓ +6.4 → +5.4 | +21.1 / +21.1 / +23.9 | 106 · 13.2 (7.0) · 14.2 · 50 |
| `F42` | ✓ +4.1 → +1.9 | ✗ +4.1 → +4.6 | ✓ +4.1 → +1.9 | ✓ +4.1 → +1.2 | ✓ +4.1 → +4.0 | +35.8 / +35.8 / +43.6 | 93 · 16.1 (9.5) · 17.2 · 58 |
| `F22` | – | – | ✓ +2.9 → +1.4 | ✓ +2.9 → +2.1 | ✓ +2.9 → +0.9 | +15.1 / +27.0 / +33.3 | 897 · 12.4 (9.4) · 11.1 · 42 |
| `F16` | – | – | ✓ +1.4 → +0.4 | ✓ +1.4 → +1.3 | ✓ +1.4 → +0.6 | +22.9 / +24.6 / +31.0 | 1,241 · 13.8 (11.2) · 13.1 · 56 |
| `F02` | – | – | ✓ +0.9 → -0.2 | ✓ +0.9 → -0.1 | ✓ +0.9 → +0.7 | +20.6 / +20.6 / +25.0 | 657 · 13.4 (11.0) · 13.9 · 58 |
| `F60` | ✗ +2.9 → +3.0 | ✓ +2.9 → +2.4 | ✓ +2.9 → +0.8 | ✓ +2.9 → +1.4 | ✓ +2.9 → +2.3 | +26.6 / +28.5 / +34.2 | 934 · 12.8 (9.0) · 13.4 · 51 |
| `F48` | ✓ +3.1 → +3.0 | ✓ +3.1 → +2.4 | ✗ +3.1 → +3.3 | ✓ +3.1 → +0.7 | ✓ +3.1 → +1.3 | +22.4 / +24.6 / +30.3 | 394 · 12.4 (9.1) · 14.2 · 51 |
| `F44` | ✓ +2.3 → +1.3 | ✓ +2.3 → +2.1 | ✓ +2.3 → +1.0 | ✓ +2.3 → +1.8 | ✓ +2.3 → +1.8 | +28.6 / +28.6 / +35.1 | 207 · 11.6 (9.1) · 12.6 · 49 |
| `F06` | – | – | ✓ +1.6 → +1.0 | ✓ +1.6 → +0.3 | ✓ +1.6 → +1.1 | +24.1 / +24.1 / +29.8 | 1,716 · 13.5 (10.6) · 12.4 · 55 |
| `F29` | – | – | ✓ +1.3 → +0.8 | ✓ +1.3 → +0.5 | ✗ +1.3 → +1.7 | +24.8 / +28.1 / +36.3 | 1,441 · 10.5 (9.5) · 10.9 · 41 |
| `F01` | – | – | ✗ +1.1 → +1.5 | ✓ +1.1 → -0.1 | ✓ +1.1 → +0.8 | +27.2 / +27.2 / +33.1 | 645 · 13.2 (9.8) · 12.4 · 56 |
| `F25` | – | – | ✓ +1.6 → +0.1 | ✓ +1.6 → +0.2 | ✗ +1.6 → +1.7 | +26.8 / +27.3 / +33.1 | 1,029 · 12.0 (9.5) · 12.0 · 45 |
| `F61` | ✓ +1.8 → +1.5 | ✗ +1.8 → +1.9 | ✓ +1.8 → +1.8 | ✓ +1.8 → +0.5 | ✓ +1.8 → +1.8 | +23.4 / +25.5 / +30.7 | 506 · 11.3 (9.5) · 11.1 · 53 |
| `F05` | – | – | ✗ +0.9 → +1.0 | ✓ +0.9 → -0.0 | ✓ +0.9 → +0.8 | +24.6 / +24.8 / +30.5 | 1,699 · 12.6 (10.5) · 11.2 · 54 |
| `F28` | – | – | ✓ +0.8 → +0.1 | ✓ +0.8 → +0.5 | ✓ +0.8 → +0.7 | +22.0 / +22.8 / +28.5 | 845 · 11.5 (10.6) · 11.6 · 53 |
| `F09` | – | – | ✓ +0.7 → +0.5 | ✗ +0.7 → +0.9 | ✓ +0.7 → +0.6 | +22.9 / +23.2 / +28.1 | 888 · 12.2 (10.3) · 11.4 · 52 |
| `F30` | – | – | ✗ +0.8 → +1.0 | ✓ +0.8 → -0.1 | ✓ +0.8 → +0.8 | +22.3 / +23.9 / +30.3 | 3,437 · 12.0 (10.2) · 12.1 · 54 |
| `F08` | – | – | ✗ +0.6 → +0.8 | ✓ +0.6 → -0.1 | ✗ +0.6 → +0.8 | +25.0 / +25.3 / +30.5 | 1,522 · 12.1 (10.3) · 10.9 · 54 |
| `F94` | ✗ +2.9 → +5.2 | ✓ +2.9 → +1.0 | ✗ +2.9 → +4.3 | ✗ +2.9 → +4.1 | ✗ +2.9 → +6.8 | +27.5 / +27.5 / +32.8 | 134 · 9.0 (6.9) · 11.2 · 49 |

## 4. Bacaan

- Dipercayai: 42 daripada 69 setup. Kadar "naik lagi" setup dipercayai: 10.0 % hingga 25.2 % (saham rawak mana-mana hari 6.3 %).
- Kekerapan setup dipercayai: median 66 belian setahun, 9.0 tangkapan setahun; liputan setiap setup 0.06–2.12 %; **semua setup dipercayai bersama menangkap 10.3 % daripada semua episod naik lagi**.
- Komponen yang menyumbang (setup dipercayai): prasyarat pasaran 20 daripada 24; prasyarat syarikat 21 daripada 23; penapis 1 30 daripada 40; penapis 2 31 daripada 38; pencetus 34 daripada 42.
- Mutu pegang (median setup dipercayai): keluar setup +23.3 % lawan pegang 20 sesi +24.6 % setiap pelari; puncak +30.2 %.
- Saham Shariah: 42 setup dipercayai cukup belian (≥ 30); kadar naik lagi pada saham Shariah mengatasi rawak bagi 42 daripadanya (median 13.9 % lawan rawak 10.3 %).

## 5. Kaveat dan apa yang MASIH belum dibuat

- Backtest sahaja; papan ialah pangkat, BUKAN bukti. Kad skor kekal satu-satunya keputusan wang sebenar.
- `F01`–`F10` dicari pada set 431 yang bertindih dengan kumpulan B; kumpulan B sudah dilihat dalam CS05/CS06.
- Tiada saham delist (condong ke atas). Senarai Shariah ialah senarai semasa, bukan titik-masa. Prasyarat earnings memakai tarikh sebenar.
- Belum dibuat: data saham delist; carian automatik berkala ("mesin sentiasa mencari"); peringkat papertrade bagi setup baharu (ditangguh atas arahan pengguna 14 Nov 2026).
