# CS21: ukuran kedua — "mencapai +10 % sebelum jatuh 8 %" dalam 3 bulan (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_capai21.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (ah). **Jangan sunting secara manual.** Pusingan UKURAN: tiada pemilihan dan tiada kod baharu.

## 1. Ukuran

- **Kena** = selepas beli pada buka esok, dalam 63 sesi (≈ 3 bulan) ada harga TUTUP ≥ +10% sebelum harga menyentuh −8%. Tiada syarat "mesti naik dalam minggu pertama" dan tiada cara pegang.
- **Jatuh dahulu** = menyentuh −8% sebelum mencapai +10%. **Terus naik** (maklumat) = tutup sesi ke-63 masih ≥ +10%.
- Semua angka pada saham yang carian tidak lihat; kurungan = saham rawak yang dibeli pada hari yang sama (tercile ATR % sama).
- **Saham rawak (semua 3,296,000 bar layak hingga 20260720):** kena 40.1 %, jatuh dahulu 47.5 %, tiada kedua-duanya 12.4 %; terus naik 30.7 %. Jadi angka mentah "kena" tinggi bagi SEMUA unit; yang bermakna hanya beza lawan rawak.

## 2. Setiap kumpulan (nilai tengah unit dengan ≥ 300 belian)

| Kumpulan | Unit | **Kena %** (rawak) | Beza (mata) | Jatuh dahulu % (rawak) | Terus naik % (rawak) | Unit lebih baik daripada rawak | …dalam 2010–19 / 2020–24 / 2025–26 | …ketiga-tiga tempoh | Tangkap % ukuran utama (rawak) |
|---|---|---|---|---|---|---|---|---|---|
| isyarat M sahaja | 370 | **39.3** (39.6) | -0.3 | 49.0 (48.3) | 30.1 (30.2) | 22 % | 28 / 23 / 56 % | 3 % | – (–) |
| isyarat N sahaja | 49 | **40.0** (40.2) | -0.2 | 49.5 (49.1) | 31.3 (31.2) | 27 % | 29 / 33 / 69 % | 10 % | – (–) |
| isyarat indikator (P) sahaja | 49 | **39.9** (40.3) | -0.3 | 49.6 (48.9) | 30.5 (31.0) | 27 % | 27 / 29 / 55 % | 8 % | – (–) |
| F senarai utama: bukan laporan | 123 | **41.9** (41.4) | +0.7 | 56.8 (56.7) | 36.3 (36.3) | 63 % | 44 / 59 / 73 % | 20 % | 12.6 (10.4) |
| F senarai utama: laporan kewangan | 1,846 | **39.5** (38.1) | +1.3 | 48.0 (47.7) | 29.6 (28.3) | 82 % | 84 / 61 / 57 % | 29 % | 11.7 (6.1) |
| F sepanjang tahun CS20: kod berdaftar | 748 | **42.1** (41.7) | +0.7 | 55.3 (54.8) | 36.6 (36.1) | 77 % | 59 / 79 / 70 % | 38 % | 11.2 (9.8) |
| F sepanjang tahun CS20: lulus, tiada kod | 495 | **41.9** (40.8) | +1.2 | 54.2 (53.7) | 33.8 (32.5) | 88 % | 72 / 83 / 76 % | 49 % | 9.0 (7.8) |
| kawalan rawak sepanjang tahun (CS20) | 300 | **38.7** (39.0) | -0.3 | 48.8 (48.1) | 29.5 (29.5) | 35 % | 46 / 28 / 54 % | 8 % | 5.6 (5.4) |

- "Beza" positif tetapi "jatuh dahulu" juga lebih tinggi daripada rawak = unit itu memilih saham yang lebih bergerak (naik DAN jatuh), bukan saham yang lebih kerap naik.

## 3. Isyarat beli M dan N sahaja (tanpa syarat, tanpa prasyarat)

- 419 unit dengan ≥ 300 belian; lebih baik daripada rawak dalam ketiga-tiga tempoh: **16**; daripadanya "jatuh dahulu" tidak melebihi rawak: 9.
- 16 teratas antara yang lebih baik dalam ketiga-tiga tempoh, ikut beza lawan rawak (susunan SELEPAS melihat hasil; bukan pemilihan):

| ID | Isyarat beli | Prasyarat | Penapis saham | Belian | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 (mata) | Jatuh dahulu % (rawak) | Terus naik % (rawak) |
|---|---|---|---|---|---|---|---|---|
| `M64.0` | M64 O'Neil Tiga Minggu Ketat (benih M, parameter asal) | – | – | 2,008 | **41.0** (39.7) | +0.6 / +1.0 / +5.4 | 51.5 (49.0) | 31.6 (29.3) |
| `M64.1` | M64 O'Neil Tiga Minggu Ketat (benih M, varian 1: c_ambang_0_2=0.203, concat_tambah_0_1=0.094, piv_kali_0_92=0.753, rolling_50=64, sah=21) | – | – | 2,215 | **40.7** (39.7) | +0.2 / +1.0 / +4.1 | 51.8 (49.1) | 31.7 (29.5) |
| `M121.0` | M121 High 2 bull flag (Brooks) (benih M, parameter asal) | – | – | 3,186 | **37.7** (36.7) | +0.0 / +1.3 / +6.4 | 44.4 (44.9) | 26.5 (26.5) |
| `M118.0` | M118 Expansion Pivot (Cooper) (benih M, parameter asal) | – | – | 12,228 | **40.7** (39.9) | +0.5 / +1.3 / +0.0 | 46.6 (47.9) | 29.7 (30.1) |
| `N16` | N16 RSI2<10 tanpa penapis (benih N) | – | – | 90,134 | **42.5** (41.9) | +0.3 / +0.9 / +1.0 | 49.6 (49.9) | 34.0 (34.0) |
| `M29.0` | M29 EMA3 + RSI75 + Stokastik (benih M, parameter asal) | – | – | 10,634 | **40.7** (40.2) | +0.2 / +0.3 / +2.8 | 45.8 (45.8) | 30.6 (29.9) |
| `M08.1` | M08 SMA20 + SMA200 (benih M, varian 1: l_kali_0_99=0.943, rolling_10=16, rolling_20=38, rolling_6=5, s20_kali_1_05=0.972, sl20_ambang_0_01=0.012) | – | – | 18,512 | **42.3** (41.8) | +0.8 / +0.2 / +0.1 | 51.4 (50.4) | 33.4 (32.5) |
| `N73` | N73 Tutup bawah jalur bawah BB(20,2) (benih N) | – | – | 51,598 | **42.5** (42.1) | +0.1 / +0.5 / +1.6 | 48.9 (49.6) | 34.8 (34.6) |
| `N38` | N38 VCP pecah (benih N) | – | – | 39,772 | **40.6** (40.2) | +0.4 / +0.5 / +0.3 | 48.2 (47.3) | 31.1 (30.4) |
| `N202` | N202 (benih N) | – | – | 33,772 | **40.6** (40.2) | +0.2 / +0.5 / +1.1 | 46.9 (46.7) | 30.7 (30.1) |
| `M118.2` | M118 Expansion Pivot (Cooper) (benih M, varian 2: had_henti=0.811, henti_low=6, keluar_sma=61, rolling_9=18, sma_50=77) | – | – | 5,972 | **40.7** (40.3) | +0.5 / +0.1 / +0.8 | 47.3 (47.8) | 30.2 (30.8) |
| `M134.0` | M134 First Kiss After Daylight (Landry) (benih M, parameter asal) | – | – | 9,550 | **41.2** (40.8) | +0.1 / +0.2 / +1.7 | 46.5 (46.6) | 31.0 (30.9) |
| `M01.2` | M01 Bollinger Band + RSI (benih M, varian 2: r13_ambang_25=38, rolling_30=58, rsi_13=10, sd_kali_2=1.436) | – | – | 42,128 | **43.3** (43.0) | +0.0 / +0.7 / +0.1 | 49.4 (50.3) | 35.7 (35.7) |
| `M38.0` | M38 Darvas Kotak (benih M, parameter asal) | – | – | 3,619 | **38.5** (38.3) | +0.3 / +0.1 / +0.3 | 43.3 (45.5) | 29.2 (28.6) |
| `N119` | N119 3 tutup turun berturut (benih N) | – | – | 123,305 | **41.7** (41.5) | +0.2 / +0.2 / +0.3 | 50.9 (50.9) | 34.1 (34.1) |
| `M55.2` | M55 Guppy GMMA (benih M, varian 2: rolling_3=5, rolling_4=3, shift_10=14) | – | – | 36,336 | **39.5** (39.4) | +0.1 / +0.1 / +0.1 | 48.9 (48.6) | 30.3 (30.2) |

## 4. Setup F sepanjang tahun (CS20, kod berdaftar)

- 748 unit dengan ≥ 300 belian; lebih baik daripada rawak dalam ketiga-tiga tempoh: **284**; daripadanya "jatuh dahulu" tidak melebihi rawak: 177.
- 25 teratas antara yang lebih baik dalam ketiga-tiga tempoh, ikut beza lawan rawak (susunan SELEPAS melihat hasil; bukan pemilihan):

| ID | Isyarat beli | Prasyarat | Penapis saham | Belian | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 (mata) | Jatuh dahulu % (rawak) | Terus naik % (rawak) |
|---|---|---|---|---|---|---|---|---|
| `F2746` | K06.007 5 tutup menurun berturut | hasil suku terkini tumbuh >= 20% | MA20 > MA50 | 6,752 | **44.2** (41.1) | +5.0 / +2.1 / +0.8 | 50.9 (52.5) | 33.4 (32.0) |
| `F2449` | K05.005 tutup silang atas jalur atas BB(20, 1.5) | hasil suku terkini tumbuh >= 20% | MA50 > MA200 + ADX < 20 | 4,643 | **42.1** (39.5) | +3.3 / +2.1 / +2.3 | 51.8 (52.2) | 33.3 (30.6) |
| `F2345` | M12 Parabolic SAR (benih M, varian 2: psar_a0_0_02=0.015, psar_amax_0_2=0.153, psar_da_0_02=0.03, rolling_50=30) | hasil suku terkini tumbuh >= 20% | MA50 naik (lawan 20 bar lalu) + dalam 15% dari puncak 52 minggu | 5,941 | **41.7** (39.1) | +5.0 / +0.8 / +0.1 | 51.6 (51.8) | 33.1 (30.2) |
| `F2341` | K10.001 pecah tinggi 5 hari | hasil suku terkini tumbuh >= 20% | RSI14 > 60 + ADX < 20 | 5,250 | **41.4** (38.9) | +3.1 / +1.5 / +4.8 | 52.6 (53.0) | 31.9 (29.8) |
| `F2735` | N48 Inside day pecah (benih N) | hasil suku terkini tumbuh >= 20% | tutup > MA20 + ADX < 20 | 4,337 | **42.4** (39.9) | +2.4 / +2.4 / +3.4 | 52.1 (52.6) | 33.7 (31.1) |
| `F2466` | K14.001 lonjakan >= 0.0% + volum 1.5x | hasil suku terkini tumbuh >= 20% | tutup > MA50 + MA50 > MA200 | 6,912 | **42.5** (40.1) | +3.8 / +1.7 / +0.6 | 52.2 (52.5) | 33.3 (31.3) |
| `F2731` | N55 BB + RSI + ADX>20 (benih N) | – | templat trend Minervini + RS >= 70 | 6,832 | **43.4** (41.0) | +2.6 / +1.6 / +4.5 | 48.0 (48.2) | 31.6 (30.5) |
| `F2385` | K25.007 pecah julat sempit 10 hari (<= 35%) | hasil suku terkini tumbuh >= 20% | RSI14 > 60 + ADX < 20 | 5,390 | **41.2** (38.8) | +3.2 / +1.5 / +3.6 | 52.8 (53.1) | 31.9 (29.7) |
| `F2776` | M160 Measured Move Up (benih M, varian 2: a_kali_3=1.909, atr_14=22, had_henti=0.478, henti_low=5, keluar_ema=15, tmax=45) | hasil suku terkini tumbuh >= 20% | tutup > MA20 + hari naik (tutup > buka) | 6,514 | **41.7** (39.3) | +3.6 / +1.9 / +0.3 | 53.0 (53.6) | 33.1 (30.9) |
| `F2567` | K25.015 pecah julat sempit 20 hari (<= 35%) | hasil suku terkini tumbuh >= 20% | RSI14 > 60 + ADX < 20 | 5,038 | **41.2** (38.8) | +2.2 / +2.3 / +3.6 | 52.4 (52.7) | 31.8 (29.3) |
| `F2362` | K01.006 RSI(2) < 8 + atas MA200 | hasil suku terkini tumbuh >= 20% | MA20 > MA50 + MACD > 0 | 6,290 | **43.0** (40.6) | +3.5 / +1.5 / +1.6 | 51.1 (51.8) | 34.0 (31.2) |
| `F2574` | K09.013 MACD(10,20,7) silang naik | hasil suku terkini tumbuh >= 20% | MA50 naik (lawan 20 bar lalu) + ADX < 20 | 4,733 | **42.4** (40.0) | +2.8 / +2.1 / +2.2 | 52.2 (52.5) | 33.0 (31.2) |
| `F2791` | K17.043 undur ke ema100 yang naik (tol 1.0%) | sektor 3 teratas (pulangan 63 sesi) | tutup > MA20 + tutup dalam 25% teratas julat hari | 3,447 | **42.3** (39.9) | +1.7 / +4.0 / +0.6 | 45.4 (47.5) | 30.9 (30.7) |
| `F2181` | K24.005 bar pembalikan (buka <= 20%, tutup >= 80% julat) | hasil suku terkini tumbuh >= 20% | tutup > MA50 + ADX < 20 | 7,097 | **41.9** (39.5) | +2.2 / +2.0 / +4.6 | 53.0 (53.7) | 32.5 (30.5) |
| `F2586` | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (benih M, varian 1: rolling_26=37, rolling_52=35, rolling_9=18, shift_26=34) | hasil suku terkini tumbuh >= 20% | tutup > MA200 + Supertrend naik | 5,570 | **41.9** (39.5) | +3.4 / +1.8 / +0.8 | 51.5 (52.3) | 34.0 (31.0) |
| `F2416` | K05.013 tutup silang atas jalur atas BB(50, 1.5) | hasil suku terkini tumbuh >= 20% | ADX < 20 + hari naik (tutup > buka) | 4,965 | **41.2** (38.9) | +2.6 / +1.6 / +4.2 | 52.7 (53.2) | 31.8 (29.9) |
| `F2533` | N40 OBV tinggi baharu + MA50 (benih N) | hasil suku terkini tumbuh >= 20% | tutup > MA200 + MACD > 0 | 4,618 | **41.3** (39.0) | +2.8 / +2.0 / +1.5 | 52.3 (52.0) | 33.1 (30.0) |
| `F2579` | K19.007 pecah atas Keltner(20, 1.5) | hasil suku terkini tumbuh >= 20% | ADX < 20 + hari naik (tutup > buka) | 5,668 | **41.1** (38.8) | +2.4 / +1.8 / +4.1 | 53.1 (53.6) | 31.7 (29.9) |
| `F2446` | K01.045 RSI(4) < 25 | hasil suku terkini tumbuh >= 20% | tutup > MA200 + MACD > 0 | 6,361 | **42.9** (40.6) | +3.1 / +1.7 / +1.6 | 51.4 (52.0) | 33.9 (31.4) |
| `F2471` | N54 Supertrend + RSI>50 (benih N) | hasil suku terkini tumbuh >= 20% | tutup > MA50 + ADX < 20 | 6,593 | **42.3** (40.0) | +2.4 / +1.7 / +4.3 | 52.2 (53.2) | 32.3 (31.0) |
| `F2336` | K05.013 tutup silang atas jalur atas BB(50, 1.5) | hasil suku terkini tumbuh >= 20% | MACD > isyarat + hari naik (tutup > buka) | 7,976 | **41.7** (39.4) | +3.2 / +1.3 / +3.4 | 52.8 (53.0) | 32.8 (30.6) |
| `F2689` | N33 Donchian20 + penapis MA200 (benih N) | hasil suku terkini tumbuh >= 20% | ADX < 20 + Supertrend naik | 4,403 | **41.0** (38.7) | +2.1 / +1.9 / +4.3 | 52.2 (52.6) | 32.5 (29.8) |
| `F2450` | K14.001 lonjakan >= 0.0% + volum 1.5x | hasil suku terkini tumbuh >= 20% | MA50 > MA200 + Supertrend naik | 6,157 | **42.0** (39.7) | +3.7 / +1.1 / +1.5 | 52.6 (52.6) | 32.8 (31.1) |
| `F2559` | K25.015 pecah julat sempit 20 hari (<= 35%) | hasil suku terkini tumbuh >= 20% | MACD > isyarat + ADX < 20 | 5,665 | **41.4** (39.2) | +2.1 / +2.0 / +3.9 | 52.3 (52.8) | 31.7 (29.6) |
| `F2539` | K03.013 tutup < jalur bawah BB(15, 1.5) | hasil suku terkini tumbuh >= 20% | ADX > 25 | 6,404 | **43.3** (41.1) | +2.7 / +1.9 / +1.5 | 52.6 (53.7) | 35.4 (33.8) |

## 5. Setup F senarai utama: bukan laporan kewangan

- 123 unit dengan ≥ 300 belian; lebih baik daripada rawak dalam ketiga-tiga tempoh: **25**; daripadanya "jatuh dahulu" tidak melebihi rawak: 19.
- 25 teratas antara yang lebih baik dalam ketiga-tiga tempoh, ikut beza lawan rawak (susunan SELEPAS melihat hasil; bukan pemilihan):

| ID | Isyarat beli | Prasyarat | Penapis saham | Belian | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 (mata) | Jatuh dahulu % (rawak) | Terus naik % (rawak) |
|---|---|---|---|---|---|---|---|---|
| `F1880` | K18.017 jatuh >= 10% dalam 5 hari | QQQ RSI14 < 35 + 5-19 sesi selepas earnings | tutup > MA200 + ATR% >= 4 | 380 | **55.3** (45.2) | +7.4 / +15.9 / +1.7 | 44.2 (53.5) | 41.1 (39.2) |
| `F1970` | K14.029 lonjakan >= 5.0% + volum 3.0x | 7 hari pertama bulan + 0-4 sesi selepas earnings | MA50 naik (lawan 20 bar lalu) + ATR% >= 4 | 303 | **47.9** (39.2) | +11.7 / +7.4 / +6.7 | 51.5 (59.1) | 38.0 (33.8) |
| `F1723` | K18.030 jatuh >= 8% dalam 20 hari | QQQ RSI14 < 35 + tiada earnings dalam 20 sesi akan datang | tutup > MA200 + ATR% >= 4 | 671 | **52.0** (47.2) | +0.2 / +7.8 / +8.2 | 47.5 (51.7) | 43.5 (40.0) |
| `F1943` | K18.002 jatuh >= 8% dalam 2 hari | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | Supertrend naik + RS >= 70 | 714 | **45.9** (42.4) | +1.1 / +5.2 / +1.7 | 54.1 (56.6) | 34.2 (36.8) |
| `F1984` | K18.003 jatuh >= 10% dalam 2 hari | follow-through day aktif (QQQ, 20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | ATR% >= 4 | 1,102 | **46.9** (43.7) | +7.0 / +1.9 / +5.9 | 52.7 (55.8) | 39.3 (37.7) |
| `F10` | P16 RSI2<5 atas MA200 | tiada | volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 | 2,397 | **44.2** (41.4) | +0.7 / +4.4 / +3.6 | 54.8 (57.0) | 37.2 (34.7) |
| `F1930` | K03.045 tutup < jalur bawah BB(30, 2.5) + RSI14 < 40 | distribution day QQQ >= 5 dalam 25 sesi + tiada earnings dalam 20 sesi akan datang | tutup > MA200 + ATR% >= 4 | 1,056 | **45.2** (42.4) | +1.4 / +3.1 / +5.0 | 53.9 (56.3) | 40.1 (37.6) |
| `F2035` | M140 猎豹出击 (Serangan Cheetah) (benih M, parameter asal) | >= 15% saham dalam 5% dari puncak 52 minggu | MA20 > MA50 + tutup dalam 25% teratas julat hari | 575 | **44.2** (41.4) | +1.4 / +4.9 / +3.0 | 53.4 (54.9) | 33.7 (33.2) |
| `F2029` | M51 O'Neil Cawan & Pemegang (benih M, parameter asal) | >= 15% saham dalam 5% dari puncak 52 minggu + industri 20% teratas (pulangan 21 sesi) | tutup > MA20 + dalam 5% dari puncak 52 minggu | 307 | **40.7** (38.0) | +0.2 / +4.5 / +15.2 | 47.2 (48.9) | 26.1 (26.8) |
| `F1961` | K18.018 jatuh >= 15% dalam 5 hari | QQQ OFF | RS >= 70 + volum 10 hari > volum 50 hari | 1,380 | **45.6** (42.9) | +3.7 / +1.5 / +4.9 | 54.1 (56.4) | 51.2 (46.2) |
| `F2006` | K18.033 jatuh >= 20% dalam 20 hari | turun-naik SPY 21 hari <= 10% setahun + industri 20% terbawah (pulangan 63 sesi) | volum 10 hari > volum 50 hari + ATR% >= 4 | 326 | **42.3** (39.8) | +0.3 / +3.9 / +10.9 | 56.7 (57.6) | 34.0 (31.7) |
| `F1862` | K03.043 tutup < jalur bawah BB(30, 2.5) | saham lain dalam industri sama naik >= 20% dalam 20 sesi | ADX > 25 + ATR% >= 4 | 881 | **42.9** (40.6) | +0.0 / +2.1 / +6.0 | 55.7 (58.2) | 39.0 (38.2) |
| `F2039` | K01.075 RSI(10) < 15 | kejutan untung terkini positif (SUE > 0) | volum 10 hari > volum 50 hari + ATR% >= 4 | 628 | **40.0** (37.9) | +1.8 / +0.6 / +7.4 | 59.6 (61.4) | 45.9 (46.8) |
| `F1979` | K01.068 RSI(7) < 20 + atas MA200 | distribution day QQQ >= 5 dalam 25 sesi + saham lain dalam industri sama naik >= 20% dalam 20 sesi | RSI14 < 40 + ATR% >= 4 | 566 | **43.6** (41.6) | +2.0 / +1.1 / +3.9 | 56.0 (57.2) | 35.5 (36.2) |
| `F1968` | K03.046 tutup < jalur bawah BB(30, 3.0) | SPY atas SMA200 | ADX > 25 + ATR% >= 4 | 788 | **42.9** (41.0) | +0.1 / +3.1 / +5.3 | 55.1 (57.1) | 34.6 (34.5) |
| `F2008` | K03.047 tutup < jalur bawah BB(30, 3.0) + RSI14 < 30 | saham lain dalam industri sama naik >= 20% dalam 20 sesi | ADX > 25 + ATR% >= 4 | 348 | **41.1** (39.3) | +0.9 / +3.1 / +0.4 | 56.9 (59.4) | 34.5 (36.3) |
| `F56` | M01 Bollinger Band + RSI (ditala 2) | QQQ >= 10% di bawah puncak | MACD > isyarat + >= 30% di bawah puncak 52 minggu | 2,078 | **50.3** (48.5) | +2.7 / +1.4 / +1.7 | 49.1 (50.2) | 50.0 (47.5) |
| `F2024` | K18.019 jatuh >= 20% dalam 5 hari | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + 0-4 sesi selepas earnings | >= 30% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | 719 | **41.4** (39.9) | +0.0 / +1.8 / +3.5 | 57.3 (58.4) | 33.7 (34.5) |
| `F1956` | K14.017 lonjakan >= 3.0% + volum 3.0x | >= 15% saham dalam 5% dari puncak 52 minggu + 0-4 sesi selepas earnings | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | 428 | **40.4** (38.8) | +0.9 / +2.1 / +2.0 | 59.3 (59.3) | 29.7 (31.7) |
| `F2037` | K01.075 RSI(10) < 15 | kejutan untung terkini positif (SUE > 0) | >= 30% di bawah puncak 52 minggu + volum 10 hari > volum 50 hari | 710 | **41.3** (39.7) | +0.9 / +0.5 / +6.6 | 57.7 (59.1) | 45.5 (46.0) |
| `F1921` | K23.005 RS silang atas 95 | >= 15% saham dalam 5% dari puncak 52 minggu + industri 20% teratas (pulangan 21 sesi) | ATR% >= 4 + hari naik (tutup > buka) | 541 | **40.3** (39.2) | +0.6 / +1.6 / +1.0 | 59.5 (59.2) | 35.7 (32.7) |
| `F2019` | K16.014 gap-and-go (buka > tinggi semalam + 3.0%) + volum 1.5x | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + sektor 3 terbawah (pulangan 63 sesi) | volum 10 hari > volum 50 hari + ATR% >= 4 | 390 | **41.3** (40.2) | +1.3 / +1.2 / +0.7 | 58.7 (58.2) | 37.7 (35.5) |
| `F02` | M111 Sistem Volatiliti Wilder (ditala 2) | QQQ OFF | >= 30% di bawah puncak 52 minggu | 1,987 | **47.5** (46.4) | +0.6 / +1.4 / +1.2 | 51.4 (50.6) | 40.3 (38.7) |
| `F60` | N119 3 tutup turun berturut | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | RS >= 90 + ATR% >= 4 | 4,248 | **41.1** (40.4) | +0.2 / +0.6 / +1.9 | 58.7 (57.8) | 35.0 (34.7) |
| `F61` | N29 PSAR naik + tutup>MA50 | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | templat trend Minervini + ATR% >= 4 | 1,563 | **41.6** (41.0) | +2.0 / +0.1 / +0.3 | 58.0 (57.3) | 35.2 (34.2) |

## 6. Setup F senarai utama: laporan kewangan

- 1,846 unit dengan ≥ 300 belian; lebih baik daripada rawak dalam ketiga-tiga tempoh: **539**; daripadanya "jatuh dahulu" tidak melebihi rawak: 358.
- 25 teratas antara yang lebih baik dalam ketiga-tiga tempoh, ikut beza lawan rawak (susunan SELEPAS melihat hasil; bukan pemilihan):

| ID | Isyarat beli | Prasyarat | Penapis saham | Belian | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 (mata) | Jatuh dahulu % (rawak) | Terus naik % (rawak) |
|---|---|---|---|---|---|---|---|---|
| `F289` | K02.034 RSI(21) silang atas 50 | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 343 | **49.6** (40.7) | +9.2 / +5.5 / +20.0 | 46.9 (52.8) | 39.1 (32.0) |
| `F1655` | K01.092 RSI(14) < 40 + atas MA200 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | ADX < 20 + dalam 15% dari puncak 52 minggu | 347 | **54.5** (45.8) | +9.1 / +8.3 / +5.6 | 33.1 (39.3) | 45.0 (36.8) |
| `F690` | K14.003 lonjakan >= 0.0% + volum 2.0x | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 naik (lawan 20 bar lalu) + dalam 15% dari puncak 52 minggu | 629 | **44.4** (36.4) | +6.5 / +11.6 / +8.2 | 43.9 (48.2) | 27.7 (26.2) |
| `F440` | K13.003 Stochastic(5) silang naik dari bawah 30 | earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 771 | **47.2** (39.5) | +10.7 / +2.5 / +15.9 | 48.4 (53.1) | 34.2 (31.1) |
| `F557` | K13.003 Stochastic(5) silang naik dari bawah 30 | >= 60% saham di atas MA200 + earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 506 | **45.7** (38.0) | +10.0 / +0.0 / +28.4 | 51.0 (54.3) | 33.6 (29.5) |
| `F1422` | K14.004 lonjakan >= 0.0% + volum 2.0x + tutup 25 % teratas | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | dalam 15% dari puncak 52 minggu + hari naik (tutup > buka) | 466 | **43.8** (36.2) | +7.2 / +10.9 / +2.2 | 43.8 (48.5) | 27.7 (25.4) |
| `F97` | K23.004 RS silang atas 90 | turun-naik SPY menurun (21 hari < 63 hari) + earnings dalam 1-5 sesi akan datang | MA50 naik (lawan 20 bar lalu) + templat trend Minervini | 468 | **44.4** (37.1) | +9.3 / +4.1 / +3.5 | 48.5 (50.3) | 32.1 (27.2) |
| `F527` | K14.003 lonjakan >= 0.0% + volum 2.0x | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 naik (lawan 20 bar lalu) + MACD > isyarat | 524 | **43.1** (36.0) | +6.9 / +6.9 / +10.1 | 47.1 (51.0) | 28.1 (26.3) |
| `F708` | K13.003 Stochastic(5) silang naik dari bawah 30 | QQQ ON + earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 455 | **44.6** (37.5) | +10.0 / +1.4 / +13.3 | 52.3 (55.4) | 30.3 (28.0) |
| `F679` | K14.003 lonjakan >= 0.0% + volum 2.0x | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | tutup > MA20 + MA50 naik (lawan 20 bar lalu) | 661 | **43.1** (36.0) | +6.4 / +8.6 / +6.8 | 46.4 (50.6) | 26.9 (26.1) |
| `F208` | K01.003 RSI(2) < 5 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 > MA200 + ADX < 20 | 515 | **53.2** (46.1) | +7.2 / +7.1 / +6.6 | 37.7 (41.0) | 46.2 (37.9) |
| `F1285` | K04.006 masuk semula atas jalur bawah BB(20, 2.5) | Mei-Okt + earnings dalam 1-5 sesi akan datang | MA50 naik (lawan 20 bar lalu) + RSI14 < 40 | 433 | **48.0** (41.0) | +6.1 / +4.2 / +26.3 | 43.0 (48.0) | 35.1 (31.4) |
| `F1674` | K13.009 Stochastic(14) silang naik dari bawah 10 | Mei-Okt + earnings dalam 1-5 sesi akan datang | RS >= 70 | 425 | **51.5** (44.5) | +10.3 / +1.6 / +17.0 | 42.4 (47.6) | 40.9 (36.3) |
| `F1682` | K10.003 pecah tinggi 5 hari + volum 2.0x | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | tutup > MA200 + MA50 > MA200 | 450 | **44.0** (37.0) | +5.8 / +6.1 / +16.9 | 46.7 (49.9) | 29.8 (27.3) |
| `F500` | K01.003 RSI(2) < 5 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 naik (lawan 20 bar lalu) + ADX < 20 | 428 | **51.9** (44.9) | +6.5 / +9.2 / +0.9 | 39.5 (42.6) | 42.1 (36.1) |
| `F115` | K13.012 Stochastic(14) silang naik dari bawah 40 | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 448 | **44.9** (37.9) | +10.0 / +1.4 / +2.1 | 52.2 (54.4) | 33.5 (28.3) |
| `F1100` | M160 Measured Move Up (benih M, varian 2: a_kali_3=1.909, atr_14=22, had_henti=0.478, henti_low=5, keluar_ema=15, tmax=45) | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | RS >= 70 + tutup dalam 25% teratas julat hari | 653 | **42.0** (35.2) | +7.6 / +2.9 / +19.9 | 50.1 (52.4) | 29.6 (26.7) |
| `F114` | K13.012 Stochastic(14) silang naik dari bawah 40 | earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 626 | **46.6** (40.1) | +9.0 / +3.8 / +2.7 | 50.3 (53.2) | 35.9 (31.5) |
| `F1109` | K01.004 RSI(2) < 5 + atas MA200 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | ADX < 20 | 372 | **52.4** (46.0) | +6.3 / +6.7 / +5.7 | 36.8 (39.7) | 45.4 (36.8) |
| `F1030` | K01.005 RSI(2) < 8 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 > MA200 + ADX < 20 | 758 | **52.4** (46.0) | +7.4 / +4.2 / +12.8 | 37.5 (41.3) | 44.3 (38.1) |
| `F100` | K13.012 Stochastic(14) silang naik dari bawah 40 | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 381 | **44.6** (38.3) | +9.1 / +2.6 / +1.0 | 52.8 (54.8) | 32.5 (28.1) |
| `F806` | K01.025 RSI(3) < 15 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 > MA200 + ADX < 20 | 695 | **51.5** (45.3) | +6.9 / +5.1 / +8.4 | 39.1 (42.6) | 44.9 (38.3) |
| `F263` | K01.007 RSI(2) < 10 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | MA50 > MA200 + ADX < 20 | 875 | **51.0** (44.9) | +7.4 / +4.4 / +7.4 | 38.3 (42.2) | 42.3 (37.0) |
| `F1373` | K03.027 tutup < jalur bawah BB(20, 1.5) + RSI14 < 40 | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | ADX < 20 + ATR% <= 2.5 | 342 | **48.0** (41.9) | +6.0 / +6.2 / +5.1 | 33.3 (37.6) | 37.4 (31.7) |
| `F550` | M156 Single Penetration (DiNapoli) (benih M, varian 2: h_kali_0_382=0.193, h_kali_0_618=0.314, had_henti=0.886, henti_atr=2.999, tmax=11) | >= 60% saham di atas MA200 + earnings dalam 1-5 sesi akan datang | RS >= 90 + dalam 15% dari puncak 52 minggu | 825 | **41.8** (36.0) | +7.1 / +0.3 / +12.3 | 53.6 (54.3) | 35.3 (28.5) |

## 7. Kaveat

- Ukuran ini lebih longgar daripada ukuran utama; pelajaran CS12: carian ikut ukuran longgar lulus pada saham tidak dilihat tetapi gagal pada 2025–26. Lajur 2025–26 di sini wajib dibaca.
- Isyarat M / N di sini ialah isyarat beli sahaja (mod tanpa intai), bukan kaedah penuh dengan keluar masing-masing.
- Tiada saham delist dalam data: "kena" condong ke atas dan "jatuh dahulu" condong ke bawah bagi semua unit, termasuk saham rawak.
- Jadual teratas disusun selepas melihat hasil pada saham yang sama; sebahagian kedudukan ialah nasib. Senarai penuh: `unit.csv.gz`.
- Backtest sahaja; tiada papertrade tanpa keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.
