# CS19: audit bebas senarai utama setup F (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Peraturan: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (ae). Dijana `cs_audit19.py`; jangan sunting.

- Permintaan pengguna 16 Nov 2026: semak satu demi satu setup F teratas sebagai juru audit; "check betul-betul".
- **Urutan sebenar:** audit ini dijalankan dalam chat SEBELUM pindaan (ae) ditulis; takrif gred ditulis sebelum angka setiap setup dilihat tetapi tidak dikomit dahulu. Gred ialah label maklumat, bukan ujian dikunci.
- Kod audit mengira sendiri bar layak, harga beli, label, saham rawak dan cara pegang daripada harga mentah, tanpa kernel enjin. Isyarat beli diambil daripada penjana enjin; bagi 6 setup contoh isyarat pun ditulis semula.

## 1. Yang betul

- **Pariti:** 2,001 daripada 2,001 setup yang diaudit menyamai `hasil/CS13/senarai_utama.csv` (bilangan belian sama tepat; kadar tangkap, kadar menang dan purata dalam 0.05 mata). 300 teratas: 300 daripada 300. Tidak dapat diaudit (pencetus tidak dijana semula): 0. Bar layak: beza 0 antara enjin dan audit.
- **Isyarat ditulis semula secara bebas:** 6 daripada 6 setup contoh sama tepat (`bebas.csv`).
- **Tengok masa depan:** keluarga K (656 ahli) beza –; atom P / penapis / keluar beza –; prasyarat dan label disemak dalam kod (tiada anjakan negatif). Tarikh laporan (8-K butiran 2.02) memakai masa terima: waktu UTC ≥ 20 atau waktu New York ≥ 16:00 memberi hasil yang sama.
- **Data:** 1,587 saham kumpulan B, 1,326 ada data laporan (11.1 % bar layak tanpa data; kadar asas naik ≥ 5 % sama: 12.4 lawan 13.1). Pulangan 5 hari > +100 %: 93 bar daripada 3,324,189 (GME, AMC, RGC dan seumpamanya: benar); bar OHLC tidak konsisten: 1.

## 2. Yang terlepas

1. **Satu idea sahaja.** 276 daripada 300 teratas (1,878 daripada 2,001 semua) = "beli 1–5 sesi sebelum laporan kewangan". Tanpa isyarat beli, prasyarat itu sahaja: 24 naik ≥ 5 % daripada 100 (rawak 13.5).
2. **Jatuh hampir sama banyak.** 300 teratas digabung (41,723 belian unik): naik ≥ 5 % minggu pertama 26 (rawak 18); jatuh ≥ 5 % 22 (rawak 16). Nilai tengah setiap setup: 28 lawan 17; 22 lawan 15.
3. **Menang dan purata hampir sama dengan saham rawak yang dibeli hari sama dan dipegang cara sama.** Gabungan: menang 50 lawan 49; purata +1.6 % lawan +1.4 %. Pada 2025–26: 48 lawan 48; +2.1 % lawan +2.3 %. (Saham rawak mana-mana hari, cara pegang B: menang 47, purata +0.6 %.)
4. **Kedudukan tidak stabil.** Korelasi pangkat kelebihan tangkap antara tempoh (semua setup): 2010–19 lawan 2020–24 0.24; 2010–19 lawan 2025–26 0.15; 2020–24 lawan 2025–26 0.03. Setup yang "baik dahulu" (98 daripada 300) pada 2025–26: arah +1.1, menang lawan rawak +2.8; yang lain: +1.3, +1.0.
5. **2025–26 bukan lagi tempoh tidak dilihat** bagi setup berdaftar: ia syarat lulus CS13 (kelebihan > 0 dalam ketiga-tiga tempoh). Bukti bersih hanya daripada papertrade.
6. **Tiada saham mati.** 0 daripada 1,587 saham berakhir sebelum Ogos 2026. Angka condong ke atas, terutama setup "≥ 30 % di bawah puncak 52 minggu".
7. **Intai buka esok.** 322 setup (28 dalam 300 teratas) memakai pencetus kaedah M yang membaca bar esok. Diukur semula tanpa intai: 264 setup berubah; kadar tangkap nilai tengah -0.02 mata, paling besar 0.8 mata; kadar menang paling besar 2.2 mata. Ujian bar terakhir: – daripada – pencetus benih berbeza; selepas mod tanpa intai – (modul `INTAI_LAIN` tidak dibetulkan mod itu).
8. **Stop loss dan hari laporan.** Nilai tengah 300 teratas: 80 % belian dipegang melalui hari laporan; 21 % dagangan kena stop, 4.4 % harganya melompat melepasi paras (rugi purata -17.8 % lawan -13.7 % bagi stop biasa).
9. **Nama:** "k tutup menurun berturut" (keluarga K06) bermaksud k − 1 hari turun berturut-turut.

## 3. Gred (300 teratas; label maklumat)

| Gred | Bil. | Maksud |
|---|---|---|
| A | 29 | Solid (CS16), arah > 0 dalam ketiga-tiga tempoh, menang dan purata melebihi rawak termasuk 2025–26 |
| B | 104 | Lulus sebahagian |
| C | 112 | Tangkap saham bergerak besar sahaja |
| D | 55 | Rapuh (gagal S1, S3 atau S5 CS16) |

Semua setup yang diaudit: {'A': 54, 'B': 639, 'C': 976, 'D': 332}. **Gred A bukan bukti** (ia memakai 2025–26). Kohort papertrade = 29 setup gred A dalam 300 teratas (sama dengan senarai dikunci pindaan (ae): ya).

## 4. Gabungan belian unik (daripada 100 belian; kurungan = saham rawak hari sama, dipegang cara sama)

| Kumpulan | Tempoh | Belian | Tangkap | Naik ≥ 5 % | Jatuh ≥ 5 % | Menang | Purata % | Rugi ≥ 15 % |
|---|---|---|---|---|---|---|---|---|
| 300 teratas | semua | 41,723 | 13.9 (9.4) | 26.1 (18.2) | 21.8 (15.5) | 49.9 (48.9) | +1.6 (+1.4) | 10.4 (8.7) |
| 300 teratas | 2010-19 | 18,348 | 13.1 (7.8) | 24.1 (14.7) | 18.9 (11.8) | 50.2 (49.5) | +1.1 (+1.0) | 7.1 (5.4) |
| 300 teratas | 2020-24 | 17,667 | 14.2 (10.6) | 27.1 (20.7) | 24.1 (18.9) | 50.0 (48.5) | +2.0 (+1.7) | 13.1 (11.5) |
| 300 teratas | 2025-26 | 5,708 | 15.4 (11.0) | 29.4 (21.5) | 23.8 (17.4) | 47.6 (48.0) | +2.1 (+2.3) | 14.2 (12.1) |
| gred A (300 teratas) | semua | 10,821 | 15.5 (8.6) | 27.5 (15.8) | 21.6 (14.2) | 52.2 (49.8) | +2.1 (+1.5) | 8.2 (6.9) |
| gred A (300 teratas) | 2010-19 | 5,170 | 14.2 (6.7) | 25.0 (12.4) | 18.3 (10.9) | 52.6 (50.6) | +1.6 (+1.0) | 5.2 (4.2) |
| gred A (300 teratas) | 2020-24 | 4,394 | 16.5 (10.7) | 29.2 (18.9) | 24.4 (17.3) | 52.7 (50.3) | +2.8 (+2.4) | 10.6 (9.1) |
| gred A (300 teratas) | 2025-26 | 1,257 | 16.8 (9.1) | 32.2 (19.0) | 25.8 (17.1) | 48.4 (43.4) | +1.5 (+0.0) | 13.4 (11.2) |
| gred B (300 teratas) | semua | 22,827 | 14.9 (8.7) | 27.6 (16.4) | 22.3 (14.2) | 50.9 (49.2) | +1.6 (+1.3) | 8.9 (7.1) |
| gred B (300 teratas) | 2010-19 | 10,562 | 13.6 (6.8) | 25.2 (12.9) | 20.0 (11.5) | 51.0 (49.2) | +1.1 (+0.7) | 6.0 (4.8) |
| gred B (300 teratas) | 2020-24 | 9,279 | 15.8 (10.3) | 28.9 (19.3) | 23.9 (16.7) | 51.3 (49.6) | +2.2 (+1.9) | 11.3 (9.0) |
| gred B (300 teratas) | 2025-26 | 2,986 | 16.8 (10.1) | 32.0 (19.8) | 25.1 (16.0) | 49.2 (47.7) | +1.8 (+1.5) | 12.9 (10.3) |
| gred C (300 teratas) | semua | 25,077 | 14.8 (8.7) | 27.1 (16.6) | 23.2 (14.1) | 50.0 (49.1) | +1.5 (+1.3) | 9.2 (7.2) |
| gred C (300 teratas) | 2010-19 | 11,605 | 13.8 (7.0) | 24.9 (13.1) | 20.8 (11.5) | 50.7 (49.5) | +1.2 (+0.8) | 6.2 (4.7) |
| gred C (300 teratas) | 2020-24 | 10,175 | 15.9 (10.3) | 29.0 (19.9) | 24.0 (16.3) | 50.5 (49.2) | +2.1 (+1.8) | 11.1 (9.1) |
| gred C (300 teratas) | 2025-26 | 3,297 | 15.0 (9.9) | 29.1 (19.3) | 29.0 (16.5) | 45.4 (47.2) | +0.6 (+1.2) | 15.5 (11.2) |
| gred D (300 teratas) | semua | 24,063 | 14.3 (11.4) | 26.5 (21.8) | 21.3 (18.0) | 51.2 (50.3) | +2.3 (+2.1) | 12.9 (11.4) |
| gred D (300 teratas) | 2010-19 | 9,426 | 13.7 (10.0) | 25.0 (18.5) | 17.4 (13.4) | 52.0 (51.4) | +1.6 (+1.5) | 9.3 (7.2) |
| gred D (300 teratas) | 2020-24 | 11,224 | 14.3 (12.1) | 26.8 (23.3) | 24.6 (21.4) | 50.9 (49.5) | +2.6 (+2.2) | 15.4 (14.2) |
| gred D (300 teratas) | 2025-26 | 3,413 | 15.9 (13.2) | 29.9 (25.5) | 21.4 (19.5) | 49.3 (49.7) | +3.3 (+3.6) | 15.5 (14.3) |
| 30 teratas ikut kedudukan | semua | 11,880 | 18.8 (12.2) | 32.6 (22.6) | 21.5 (15.0) | 54.6 (53.1) | +3.3 (+2.7) | 11.2 (9.5) |
| 30 teratas ikut kedudukan | 2010-19 | 4,987 | 18.4 (10.4) | 31.6 (19.5) | 17.9 (11.5) | 54.8 (53.1) | +2.3 (+1.7) | 7.8 (6.6) |
| 30 teratas ikut kedudukan | 2020-24 | 5,340 | 18.9 (13.8) | 33.0 (25.2) | 23.5 (17.5) | 55.4 (53.8) | +4.2 (+3.7) | 12.6 (10.9) |
| 30 teratas ikut kedudukan | 2025-26 | 1,553 | 19.5 (12.6) | 34.7 (23.8) | 25.9 (17.6) | 50.8 (50.4) | +3.1 (+2.9) | 17.9 (14.5) |
| semua setup senarai utama yang diaudit | semua | 71,039 | 11.8 (8.2) | 23.1 (16.3) | 20.7 (14.8) | 47.4 (46.9) | +1.0 (+0.9) | 9.4 (8.1) |
| semua setup senarai utama yang diaudit | 2010-19 | 32,606 | 11.1 (6.6) | 21.1 (12.8) | 17.8 (10.8) | 47.7 (47.5) | +0.7 (+0.6) | 5.9 (4.6) |
| semua setup senarai utama yang diaudit | 2020-24 | 28,580 | 12.2 (9.4) | 24.5 (19.1) | 23.4 (18.5) | 47.5 (46.5) | +1.2 (+1.1) | 12.8 (11.4) |
| semua setup senarai utama yang diaudit | 2025-26 | 9,853 | 12.9 (9.9) | 26.0 (19.8) | 22.3 (17.0) | 45.8 (46.0) | +1.4 (+1.5) | 12.6 (11.4) |
| KAWALAN: semua saham 1-5 sesi sebelum laporan, tiada isyarat beli | semua | 47,390 | 12.6 (7.0) | 24.0 (13.5) | 21.3 (12.1) | 47.6 (46.7) | +0.7 (+0.6) | 7.0 (5.6) |
| KAWALAN: semua saham 1-5 sesi sebelum laporan, tiada isyarat beli | 2010-19 | 24,147 | 11.6 (5.4) | 21.8 (10.5) | 18.8 (9.5) | 47.7 (46.8) | +0.5 (+0.3) | 4.4 (3.4) |
| KAWALAN: semua saham 1-5 sesi sebelum laporan, tiada isyarat beli | 2020-24 | 17,191 | 13.6 (8.7) | 26.2 (16.8) | 23.0 (14.7) | 48.2 (47.1) | +1.2 (+1.1) | 9.4 (7.6) |
| KAWALAN: semua saham 1-5 sesi sebelum laporan, tiada isyarat beli | 2025-26 | 6,052 | 13.4 (8.2) | 26.7 (16.2) | 26.4 (14.7) | 44.5 (44.5) | +0.1 (+0.3) | 11.4 (9.1) |
| KAWALAN: laporan esok (beli selepas laporan keluar) | semua | 46,226 | 10.1 (6.9) | 19.6 (13.6) | 18.1 (12.5) | 47.2 (46.6) | +0.5 (+0.5) | 5.6 (5.4) |
| KAWALAN: laporan esok (beli selepas laporan keluar) | 2010-19 | 23,549 | 9.0 (5.6) | 17.0 (10.4) | 15.0 (10.0) | 48.1 (47.1) | +0.5 (+0.3) | 3.3 (3.4) |
| KAWALAN: laporan esok (beli selepas laporan keluar) | 2020-24 | 16,753 | 11.1 (8.4) | 21.8 (16.7) | 21.1 (15.2) | 46.6 (46.2) | +0.8 (+0.8) | 7.7 (7.4) |
| KAWALAN: laporan esok (beli selepas laporan keluar) | 2025-26 | 5,924 | 11.2 (8.3) | 23.5 (17.3) | 21.9 (14.7) | 44.7 (45.4) | +0.1 (+0.4) | 9.3 (8.3) |
| KAWALAN: laporan 2-5 sesi lagi | semua | 46,997 | 12.6 (6.9) | 24.1 (13.5) | 21.3 (12.1) | 47.6 (46.7) | +0.7 (+0.6) | 6.9 (5.5) |
| KAWALAN: laporan 2-5 sesi lagi | 2010-19 | 23,942 | 11.6 (5.4) | 21.8 (10.4) | 18.8 (9.5) | 47.7 (46.8) | +0.5 (+0.3) | 4.4 (3.4) |
| KAWALAN: laporan 2-5 sesi lagi | 2020-24 | 17,025 | 13.6 (8.7) | 26.3 (16.8) | 23.0 (14.7) | 48.2 (47.2) | +1.2 (+1.1) | 9.4 (7.5) |
| KAWALAN: laporan 2-5 sesi lagi | 2025-26 | 6,030 | 13.4 (8.2) | 26.7 (16.2) | 26.4 (14.7) | 44.6 (44.5) | +0.1 (+0.3) | 11.4 (9.1) |

## 5. 300 teratas satu demi satu

Tangkap = naik ≥ 5 % minggu pertama dan naik lagi hingga minggu ke-4. Naik:Jatuh = berapa naik ≥ 5 % : berapa jatuh ≥ 5 % minggu pertama. Kurungan = saham rawak hari sama (dipegang cara sama). Nota: x bukan setup laporan kewangan · k prasyarat kalendar · i pencetus membaca bar esok · h bergantung beberapa hari · y kalah rawak banyak tahun · t belian terlalu sedikit.

| # | ID | Prasyarat | Isyarat beli | Tangkap (rawak) | Naik:Jatuh | Menang (rawak) | Purata % (rawak) | Gred |
|---|---|---|---|---|---|---|---|---|
| 1 | `F43` | Januari + tiada earnings dalam 20 sesi akan datang | M105 Supertrend tulen (ditala 2) | 25 (20) | 34:13 | 62 (61) | +4.9 (+4.6) | D xkih |
| 2 | `F1674` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.009 Stochastic(14) silang naik dari bawah 10 | 23 (11) | 33:22 | 57 (51) | +6.2 (+2.7) | B k |
| 3 | `F421` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (benih M, parameter asal) | 23 (13) | 38:24 | 64 (59) | +6.1 (+4.6) | A i |
| 4 | `F63` | QQQ OFF + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | 22 (16) | 38:26 | 56 (55) | +4.1 (+3.3) | C |
| 5 | `F65` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | P14 RSI14 silang atas 30 | 22 (16) | 38:20 | 61 (57) | +4.6 (+3.9) | C |
| 6 | `F151` | breadth thrust Zweig aktif (20 sesi) + earnings dalam 1-5 sesi akan datang | M125 2-Bar Breakout (benih M, parameter asal) | 21 (14) | 38:24 | 62 (59) | +6.5 (+5.8) | C |
| 7 | `F51` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | 21 (16) | 36:19 | 60 (59) | +4.3 (+4.2) | C |
| 8 | `F1255` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K13.006 Stochastic(9) silang naik dari bawah 20 | 21 (11) | 32:23 | 50 (51) | +2.3 (+1.8) | C |
| 9 | `F1885` | QQQ RSI14 < 35 + tiada earnings dalam 20 sesi akan datang | K18.031 jatuh >= 10% dalam 20 hari | 21 (16) | 39:19 | 53 (49) | +2.3 (+1.0) | D xh |
| 10 | `F50` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | 21 (18) | 42:26 | 56 (54) | +4.4 (+3.7) | D h |
| 11 | `F1723` | QQQ RSI14 < 35 + tiada earnings dalam 20 sesi akan datang | K18.030 jatuh >= 8% dalam 20 hari | 20 (15) | 37:18 | 53 (49) | +2.8 (+1.2) | D xhy |
| 12 | `F1217` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K02.033 RSI(21) silang atas 40 | 20 (11) | 28:23 | 55 (55) | +2.9 (+3.4) | C |
| 13 | `F56` | QQQ >= 10% di bawah puncak | M01 Bollinger Band + RSI (ditala 2) | 19 (17) | 35:18 | 56 (55) | +5.7 (+5.1) | D xh |
| 14 | `F1452` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K02.017 RSI(10) silang atas 30 | 19 (12) | 31:20 | 54 (55) | +2.8 (+2.4) | D t |
| 15 | `F1057` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.094 RSI(14) < 45 + atas MA200 | 19 (9) | 28:19 | 55 (54) | +4.2 (+2.6) | A |
| 16 | `F962` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K01.043 RSI(4) < 20 | 19 (13) | 35:29 | 52 (51) | +3.1 (+2.9) | B k |
| 17 | `F1719` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K18.031 jatuh >= 10% dalam 20 hari | 19 (11) | 31:22 | 56 (52) | +2.8 (+2.2) | B |
| 18 | `F1413` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K02.017 RSI(10) silang atas 30 | 19 (12) | 31:17 | 56 (55) | +3.7 (+2.6) | D t |
| 19 | `F1033` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.059 RSI(5) < 20 | 18 (9) | 30:21 | 53 (52) | +2.7 (+1.9) | A |
| 20 | `F200` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s4: c_kali_ | 18 (11) | 35:26 | 51 (47) | +3.5 (+1.5) | A i |
| 21 | `F1247` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.082 RSI(10) < 30 + atas MA200 | 18 (9) | 31:19 | 54 (53) | +2.8 (+1.8) | A |
| 22 | `F461` | breadth thrust Zweig aktif (20 sesi) + earnings dalam 1-5 sesi akan datang | K08.005 sma5 silang atas sma20 | 18 (10) | 27:19 | 60 (61) | +3.6 (+3.7) | C |
| 23 | `F631` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.013 RSI(2) < 25 | 18 (12) | 37:29 | 54 (52) | +3.8 (+2.8) | C |
| 24 | `F1448` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K08.018 ema20 silang atas ema100 | 18 (7) | 28:16 | 53 (48) | +2.3 (+0.6) | A |
| 25 | `F39` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M73 ADX(5) > 40 + Julat Terkecil 6 Hari (ditala 2) | 18 (11) | 39:26 | 50 (51) | +2.0 (+2.0) | C |
| 26 | `F1092` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | M15 Break & Retest + Henti ATR (benih M, varian 1: atrw_14=1 | 18 (12) | 31:24 | 61 (60) | +4.2 (+3.9) | B i |
| 27 | `F91` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | 18 (10) | 35:24 | 51 (47) | +4.2 (+1.1) | B i |
| 28 | `F40` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (ditala 2) | 18 (11) | 39:24 | 51 (50) | +2.7 (+1.8) | C i |
| 29 | `F219` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K07.001 tutup silang atas sma5 | 18 (10) | 37:28 | 51 (50) | +3.3 (+2.1) | C |
| 30 | `F1584` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K13.005 Stochastic(9) silang naik dari bawah 10 | 18 (11) | 30:20 | 54 (54) | +3.1 (+3.0) | D t |
| 31 | `F544` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.009 RSI(2) < 15 | 18 (10) | 27:21 | 52 (52) | +2.5 (+2.2) | B |
| 32 | `F1285` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K04.006 masuk semula atas jalur bawah BB(20, 2.5) | 18 (8) | 29:16 | 57 (48) | +3.7 (+1.0) | A k |
| 33 | `F89` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut | 17 (10) | 34:25 | 51 (46) | +3.3 (+1.1) | B i |
| 34 | `F1430` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K18.030 jatuh >= 8% dalam 20 hari | 17 (9) | 29:21 | 54 (52) | +2.1 (+1.9) | C |
| 35 | `F1560` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K13.005 Stochastic(9) silang naik dari bawah 10 | 17 (10) | 26:21 | 57 (54) | +3.7 (+3.2) | D h |
| 36 | `F901` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.081 RSI(10) < 30 | 17 (9) | 29:22 | 53 (52) | +2.7 (+2.0) | B |
| 37 | `F1266` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.070 RSI(7) < 25 + atas MA200 | 17 (10) | 31:19 | 51 (53) | +2.5 (+2.0) | B |
| 38 | `F861` | QQQ OFF + earnings dalam 1-5 sesi akan datang | M01 Bollinger Band + RSI (benih M, varian 2: r13_ambang_25=3 | 17 (12) | 28:21 | 56 (55) | +3.3 (+3.0) | C |
| 39 | `F610` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.6 | 17 (10) | 29:20 | 53 (51) | +2.1 (+1.3) | C |
| 40 | `F254` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K02.007 RSI(5) silang atas 60 | 17 (10) | 37:29 | 53 (51) | +4.2 (+2.6) | B |
| 41 | `F668` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.059 RSI(5) < 20 | 17 (9) | 29:23 | 52 (51) | +2.2 (+1.7) | A |
| 42 | `F833` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.6 | 17 (10) | 30:21 | 52 (51) | +2.2 (+1.7) | A |
| 43 | `F1982` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | M79 Radge: 20% Flipper (benih M, varian 1: a=0.18) | 17 (10) | 29:26 | 51 (50) | +2.0 (+1.7) | C |
| 44 | `F409` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K06.001 2 tutup menurun berturut | 17 (11) | 33:30 | 51 (51) | +2.5 (+2.5) | C k |
| 45 | `F1731` | turun-naik SPY menurun (21 hari < 63 hari) + earnings dalam 1-5 sesi akan datang | K18.009 jatuh >= 8% dalam 3 hari | 17 (11) | 32:27 | 52 (49) | +2.9 (+2.2) | C |
| 46 | `F601` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.073 RSI(7) < 35 | 17 (14) | 31:24 | 52 (53) | +2.9 (+2.7) | D ht |
| 47 | `F90` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M50 Elder Triple Screen | 17 (10) | 37:27 | 50 (49) | +3.3 (+1.4) | C i |
| 48 | `F1218` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K09.020 MACD(3,10,16) silang naik bawah sifar | 17 (12) | 31:23 | 56 (53) | +3.6 (+2.6) | C |
| 49 | `F1269` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K18.008 jatuh >= 5% dalam 3 hari | 17 (11) | 33:22 | 52 (48) | +2.2 (+1.2) | C k |
| 50 | `F987` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K18.008 jatuh >= 5% dalam 3 hari | 17 (11) | 31:23 | 51 (50) | +2.2 (+2.0) | B k |
| 51 | `F1553` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K08.018 ema20 silang atas ema100 | 17 (8) | 25:19 | 54 (52) | +2.5 (+1.4) | B |
| 52 | `F1030` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.005 RSI(2) < 8 | 17 (9) | 26:17 | 57 (53) | +3.6 (+2.7) | A |
| 53 | `F1961` | QQQ OFF | K18.018 jatuh >= 15% dalam 5 hari | 17 (14) | 36:29 | 51 (48) | +3.1 (+1.2) | D xh |
| 54 | `F571` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.028 tutup < jalur bawah BB(20, 2.0) | 17 (9) | 27:23 | 52 (52) | +2.3 (+2.0) | A |
| 55 | `F912` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.6 | 17 (9) | 29:21 | 53 (51) | +2.1 (+1.7) | C |
| 56 | `F771` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K24.003 bar pembalikan (buka <= 10%, tutup >= 90% julat) | 17 (9) | 25:19 | 56 (54) | +3.2 (+1.8) | C |
| 57 | `F1592` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.089 RSI(14) < 35 | 17 (9) | 28:22 | 52 (51) | +2.1 (+1.7) | B |
| 58 | `F178` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | N29 PSAR naik + tutup>MA50 (benih N) | 17 (10) | 35:29 | 50 (46) | +2.3 (+1.0) | B |
| 59 | `F1288` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.027 tutup < jalur bawah BB(20, 1.5) + RSI14 < 40 | 17 (9) | 28:21 | 54 (52) | +3.1 (+2.2) | A |
| 60 | `F526` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.073 RSI(7) < 35 | 17 (13) | 29:23 | 53 (53) | +2.9 (+2.6) | D h |
| 61 | `F203` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.005 4 tutup menurun berturut | 17 (9) | 26:21 | 55 (53) | +3.5 (+2.6) | A |
| 62 | `F322` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, varian 2: c_kali_2= | 17 (10) | 33:24 | 52 (46) | +3.3 (+1.0) | D iy |
| 63 | `F971` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K02.033 RSI(21) silang atas 40 | 17 (9) | 27:19 | 56 (53) | +2.7 (+2.4) | B |
| 64 | `F1048` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M15 Break & Retest + Henti ATR (benih M, varian 2: atrw_14=2 | 17 (9) | 29:21 | 56 (53) | +2.8 (+2.2) | B i |
| 65 | `F479` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | 17 (10) | 27:22 | 53 (53) | +2.5 (+2.3) | A |
| 66 | `F1099` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K02.033 RSI(21) silang atas 40 | 17 (9) | 29:20 | 53 (52) | +2.5 (+2.2) | C |
| 67 | `F879` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.071 RSI(7) < 30 | 17 (9) | 28:20 | 54 (54) | +2.7 (+2.1) | B |
| 68 | `F260` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.004 Stochastic(5) silang naik dari bawah 40 | 17 (11) | 30:28 | 53 (54) | +3.1 (+3.2) | C k |
| 69 | `F694` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.043 RSI(4) < 20 | 17 (9) | 27:23 | 53 (53) | +2.9 (+2.3) | A |
| 70 | `F156` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | 17 (9) | 26:21 | 56 (53) | +2.7 (+2.6) | C |
| 71 | `F493` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K22.002 Holy Grail (ADX > 20, undur EMA20) | 17 (9) | 28:20 | 53 (50) | +2.3 (+1.3) | B k |
| 72 | `F1589` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.009 Stochastic(14) silang naik dari bawah 10 | 17 (9) | 26:20 | 54 (50) | +3.5 (+2.0) | A k |
| 73 | `F170` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M14 Walking with the Whales (benih M, varian 2: rolling_50=3 | 17 (10) | 37:24 | 50 (49) | +2.4 (+1.3) | C i |
| 74 | `F1016` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.043 RSI(4) < 20 | 17 (10) | 27:24 | 53 (52) | +2.8 (+2.2) | B |
| 75 | `F864` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K18.015 jatuh >= 5% dalam 5 hari | 17 (11) | 29:22 | 52 (51) | +2.1 (+2.1) | B k |
| 76 | `F1322` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K18.015 jatuh >= 5% dalam 5 hari | 17 (12) | 31:25 | 52 (51) | +2.5 (+2.5) | B k |
| 77 | `F1994` | keluasan naik >= 10 mata dalam 10 sesi + saham lain dalam industri sama naik >= 20% dalam 20 sesi | K16.013 gap-and-go (buka > tinggi semalam + 3.0%) | 17 (14) | 28:23 | 53 (50) | +3.3 (+3.1) | D xh |
| 78 | `F363` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.005 4 tutup menurun berturut | 17 (9) | 27:22 | 54 (53) | +3.1 (+2.4) | A |
| 79 | `F342` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.015 RSI(2) < 30 | 16 (12) | 38:26 | 50 (50) | +2.5 (+2.0) | C |
| 80 | `F753` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.047 RSI(4) < 30 | 16 (13) | 30:23 | 52 (52) | +2.8 (+2.8) | D ht |
| 81 | `F739` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.047 RSI(4) < 30 | 16 (12) | 30:19 | 54 (54) | +2.9 (+3.1) | C |
| 82 | `F627` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.013 RSI(2) < 25 | 16 (12) | 30:23 | 51 (52) | +2.6 (+2.6) | C |
| 83 | `F617` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.027 RSI(3) < 20 | 16 (12) | 29:19 | 53 (54) | +2.4 (+2.9) | C |
| 84 | `F940` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K21.007 NR10 | 16 (8) | 28:18 | 55 (52) | +2.4 (+1.6) | B |
| 85 | `F436` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.030 tutup < jalur bawah BB(20, 2.0) + RSI14 < 40 | 16 (9) | 26:23 | 52 (51) | +2.2 (+1.8) | C |
| 86 | `F592` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K01.069 RSI(7) < 25 | 16 (11) | 29:23 | 52 (51) | +2.3 (+1.9) | C |
| 87 | `F333` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K07.002 tutup silang atas ema5 | 16 (10) | 37:29 | 53 (49) | +3.1 (+1.9) | C |
| 88 | `F1226` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K03.050 tutup < jalur bawah BB(50, 1.5) + RSI14 < 30 | 16 (12) | 30:23 | 52 (52) | +2.4 (+1.9) | B |
| 89 | `F445` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.003 tutup < jalur bawah BB(10, 1.5) + RSI14 < 40 | 16 (10) | 27:23 | 52 (52) | +2.5 (+2.1) | C |
| 90 | `F816` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.071 RSI(7) < 30 | 16 (9) | 27:21 | 55 (54) | +3.1 (+2.5) | B |
| 91 | `F756` | earnings dalam 1-5 sesi akan datang | M19 Sneaky Pivot (proksi harian) (benih M, varian 1: l_kali_ | 16 (8) | 24:22 | 52 (51) | +2.9 (+1.5) | B i |
| 92 | `F709` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | 16 (9) | 27:20 | 56 (52) | +2.1 (+1.9) | C |
| 93 | `F1340` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K11.004 Supertrend(7, 3.0) bertukar naik | 16 (9) | 28:21 | 60 (57) | +3.3 (+2.3) | D y |
| 94 | `F852` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K01.047 RSI(4) < 30 | 16 (11) | 30:21 | 54 (53) | +2.2 (+3.0) | C |
| 95 | `F946` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.045 RSI(4) < 25 | 16 (9) | 26:22 | 53 (53) | +2.5 (+2.2) | B |
| 96 | `F465` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.025 RSI(3) < 15 | 16 (9) | 27:22 | 54 (53) | +2.6 (+2.2) | B |
| 97 | `F755` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | M01 Bollinger Band + RSI (benih M, varian 2: r13_ambang_25=3 | 16 (12) | 30:22 | 53 (52) | +2.7 (+2.2) | D hyt |
| 98 | `F505` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K09.005 MACD(8,17,9) silang naik bawah sifar | 16 (8) | 29:23 | 52 (52) | +2.4 (+2.0) | B |
| 99 | `F877` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.016 tutup < jalur bawah BB(15, 2.0) | 16 (10) | 27:23 | 52 (53) | +2.6 (+2.1) | C |
| 100 | `F1091` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.027 tutup < jalur bawah BB(20, 1.5) + RSI14 < 40 | 16 (9) | 27:23 | 53 (51) | +2.6 (+2.1) | C |
| 101 | `F1207` | nisbah 4% (10 hari) > 2 + earnings dalam 1-5 sesi akan datang | M79 Radge: 20% Flipper (benih M, parameter asal) | 16 (8) | 29:18 | 58 (51) | +2.2 (+1.4) | A |
| 102 | `F521` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K02.026 RSI(14) silang atas 40 | 16 (11) | 26:26 | 56 (55) | +3.0 (+3.3) | C |
| 103 | `F1512` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.028 RSI(3) < 20 + atas MA200 | 16 (8) | 24:16 | 57 (54) | +3.8 (+2.7) | B |
| 104 | `F829` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.093 RSI(14) < 45 | 16 (8) | 25:16 | 57 (55) | +3.6 (+2.7) | B |
| 105 | `F88` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI (ditala 3) | 16 (10) | 27:23 | 55 (53) | +2.1 (+1.7) | B i |
| 106 | `F963` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.031 RSI(3) < 30 | 16 (13) | 29:22 | 53 (53) | +2.4 (+2.9) | D hyt |
| 107 | `F208` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | 16 (9) | 25:17 | 58 (54) | +3.3 (+2.8) | B |
| 108 | `F1185` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.016 tutup < jalur bawah BB(15, 2.0) | 16 (10) | 27:23 | 52 (53) | +2.6 (+2.2) | C |
| 109 | `F1612` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K03.026 tutup < jalur bawah BB(20, 1.5) + RSI14 < 30 | 16 (11) | 29:24 | 51 (51) | +2.2 (+1.9) | B |
| 110 | `F920` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.061 RSI(5) < 25 | 16 (10) | 26:23 | 54 (52) | +2.6 (+2.2) | B |
| 111 | `F993` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.083 RSI(10) < 35 | 16 (9) | 26:22 | 52 (52) | +2.3 (+2.2) | C |
| 112 | `F1165` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.045 RSI(4) < 25 | 16 (10) | 25:23 | 53 (52) | +2.6 (+2.3) | B |
| 113 | `F1303` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.091 RSI(14) < 40 | 16 (9) | 26:20 | 54 (52) | +2.9 (+2.3) | B |
| 114 | `F563` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.025 RSI(3) < 15 | 16 (9) | 26:20 | 54 (53) | +2.8 (+2.3) | B |
| 115 | `F1655` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.092 RSI(14) < 40 + atas MA200 | 16 (7) | 23:14 | 58 (54) | +3.6 (+2.3) | D t |
| 116 | `F1174` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K11.004 Supertrend(7, 3.0) bertukar naik | 16 (8) | 27:23 | 56 (55) | +2.4 (+2.0) | C |
| 117 | `F691` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M124 'Last' Stochastic Technique (ChartSchool) (benih M, var | 16 (9) | 27:23 | 54 (53) | +2.1 (+2.1) | C |
| 118 | `F890` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K01.029 RSI(3) < 25 | 16 (11) | 28:19 | 53 (54) | +2.7 (+2.9) | C |
| 119 | `F150` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K09.017 MACD(19,39,9) silang naik bawah sifar | 16 (9) | 27:22 | 56 (54) | +2.6 (+2.4) | B |
| 120 | `F967` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M15 Break & Retest + Henti ATR (benih M, varian 1: atrw_14=1 | 16 (9) | 29:22 | 54 (54) | +2.5 (+2.3) | B i |
| 121 | `F103` | earnings dalam 1-5 sesi akan datang | M89 Chande 65sma-3cc (benih M, parameter asal) | 16 (7) | 27:19 | 56 (49) | +2.1 (+0.8) | C |
| 122 | `F1539` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.006 Stochastic(9) silang naik dari bawah 20 | 16 (9) | 27:19 | 52 (50) | +2.7 (+1.9) | A k |
| 123 | `F437` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K07.011 tutup silang atas sma30 | 16 (9) | 25:22 | 54 (53) | +2.1 (+2.2) | C |
| 124 | `F1347` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.005 Stochastic(9) silang naik dari bawah 10 | 16 (9) | 26:21 | 52 (50) | +2.9 (+1.9) | A k |
| 125 | `F733` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.047 RSI(4) < 30 | 16 (8) | 25:19 | 55 (53) | +3.6 (+2.7) | A |
| 126 | `F566` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.007 RSI(2) < 10 | 16 (9) | 26:19 | 53 (53) | +2.8 (+2.4) | B |
| 127 | `F1128` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.037 tutup < jalur bawah BB(30, 1.5) | 16 (9) | 27:21 | 52 (51) | +2.5 (+1.9) | B |
| 128 | `F1209` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.018 tutup < jalur bawah BB(15, 2.0) + RSI14 < 40 | 16 (10) | 27:23 | 52 (51) | +2.5 (+2.0) | B |
| 129 | `F888` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.015 tutup < jalur bawah BB(15, 1.5) + RSI14 < 40 | 16 (9) | 26:24 | 52 (52) | +2.4 (+2.2) | C |
| 130 | `F748` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K01.029 RSI(3) < 25 | 16 (11) | 29:20 | 52 (53) | +2.3 (+2.9) | C |
| 131 | `F323` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K07.008 tutup silang atas ema15 | 16 (10) | 33:23 | 51 (47) | +2.7 (+1.2) | B |
| 132 | `F245` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.005 4 tutup menurun berturut | 16 (8) | 25:19 | 55 (53) | +3.3 (+2.2) | B |
| 133 | `F263` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.007 RSI(2) < 10 | 16 (8) | 25:17 | 56 (52) | +3.3 (+2.4) | A |
| 134 | `F1614` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.028 RSI(3) < 20 + atas MA200 | 16 (9) | 26:19 | 54 (55) | +2.9 (+2.6) | B |
| 135 | `F1089` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.091 RSI(14) < 40 | 16 (9) | 26:22 | 53 (52) | +2.5 (+2.2) | C |
| 136 | `F500` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.003 RSI(2) < 5 | 16 (9) | 27:18 | 56 (52) | +2.3 (+1.9) | C |
| 137 | `F1623` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.013 Stochastic(21) silang naik dari bawah 10 | 16 (9) | 27:20 | 51 (50) | +2.6 (+1.7) | B k |
| 138 | `F432` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.027 RSI(3) < 20 | 16 (9) | 25:20 | 54 (54) | +2.7 (+2.5) | B |
| 139 | `F922` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K11.015 Supertrend(14, 4.0) bertukar naik | 16 (8) | 23:21 | 55 (52) | +2.4 (+1.4) | B |
| 140 | `F652` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.009 RSI(2) < 15 | 15 (9) | 25:20 | 52 (53) | +2.5 (+2.3) | C |
| 141 | `F1641` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.022 RSI(3) < 8 + atas MA200 | 15 (8) | 28:16 | 53 (51) | +2.1 (+1.0) | D t |
| 142 | `F1332` | QQQ OFF + earnings dalam 1-5 sesi akan datang | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (benih  | 15 (7) | 23:19 | 55 (51) | +2.4 (+1.5) | C i |
| 143 | `F722` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.028 tutup < jalur bawah BB(20, 2.0) | 15 (9) | 26:22 | 51 (51) | +2.2 (+2.0) | B |
| 144 | `F427` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K02.006 RSI(5) silang atas 50 | 15 (10) | 34:27 | 52 (50) | +2.4 (+2.0) | C |
| 145 | `F1043` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.037 tutup < jalur bawah BB(30, 1.5) | 15 (9) | 26:22 | 54 (51) | +2.4 (+1.9) | B |
| 146 | `F1408` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.051 tutup < jalur bawah BB(50, 1.5) + RSI14 < 40 | 15 (9) | 26:19 | 53 (51) | +2.3 (+1.8) | B |
| 147 | `F1498` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.051 tutup < jalur bawah BB(50, 1.5) + RSI14 < 40 | 15 (9) | 26:22 | 53 (51) | +2.0 (+1.9) | B |
| 148 | `F1249` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.083 RSI(10) < 35 | 15 (9) | 25:20 | 53 (53) | +2.6 (+2.3) | B |
| 149 | `F404` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K06.001 2 tutup menurun berturut | 15 (8) | 27:21 | 53 (51) | +2.0 (+1.5) | C |
| 150 | `F2051` | tiada earnings dalam 20 sesi akan datang | K18.020 jatuh >= 25% dalam 5 hari | 15 (14) | 34:35 | 51 (51) | +3.5 (+3.8) | D xh |
| 151 | `F1681` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K02.024 RSI(14) silang atas 30 | 15 (10) | 29:22 | 51 (49) | +2.1 (+1.3) | B k |
| 152 | `F383` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.027 RSI(3) < 20 | 15 (8) | 24:18 | 55 (52) | +3.1 (+2.4) | B |
| 153 | `F508` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.003 tutup < jalur bawah BB(10, 1.5) + RSI14 < 40 | 15 (9) | 25:21 | 53 (51) | +2.6 (+2.4) | C |
| 154 | `F799` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.039 tutup < jalur bawah BB(30, 1.5) + RSI14 < 40 | 15 (9) | 26:22 | 53 (51) | +2.2 (+1.9) | B |
| 155 | `F1564` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K13.009 Stochastic(14) silang naik dari bawah 10 | 15 (8) | 24:21 | 52 (48) | +2.1 (+1.0) | A k |
| 156 | `F2049` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K22.012 Holy Grail (ADX > 35, undur EMA30) | 15 (11) | 29:24 | 53 (50) | +2.4 (+1.6) | C |
| 157 | `F1350` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K02.010 RSI(7) silang atas 30 | 15 (8) | 22:15 | 59 (60) | +2.5 (+2.7) | D t |
| 158 | `F2054` | follow-through day aktif (QQQ, 20 sesi) | K18.004 jatuh >= 15% dalam 2 hari | 15 (13) | 32:22 | 51 (49) | +2.6 (+2.2) | D xhy |
| 159 | `F929` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K07.016 tutup silang atas ema100 | 15 (9) | 27:19 | 55 (52) | +2.2 (+1.8) | B |
| 160 | `F1219` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K04.007 masuk semula atas jalur bawah BB(30, 1.5) | 15 (9) | 27:23 | 52 (49) | +3.1 (+1.3) | B k |
| 161 | `F1028` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.091 RSI(14) < 40 | 15 (9) | 25:22 | 53 (51) | +2.6 (+2.3) | C |
| 162 | `F898` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.006 4 tutup menurun berturut + atas MA200 | 15 (8) | 23:17 | 56 (53) | +3.3 (+2.3) | B |
| 163 | `F818` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M111 Sistem Volatiliti Wilder (benih M, varian 2: close_kali | 15 (8) | 25:18 | 59 (57) | +2.8 (+2.0) | D y |
| 164 | `F386` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K07.012 tutup silang atas ema30 | 15 (9) | 25:22 | 54 (53) | +2.0 (+2.0) | B |
| 165 | `F747` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | N28 ADX>25 + DI+ > DI- (benih N) | 15 (9) | 26:17 | 55 (52) | +2.7 (+1.8) | D yt |
| 166 | `F1984` | follow-through day aktif (QQQ, 20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | K18.003 jatuh >= 10% dalam 2 hari | 15 (12) | 33:21 | 52 (50) | +4.2 (+3.0) | D xh |
| 167 | `F304` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K09.016 MACD(19,39,9) silang naik | 15 (8) | 27:22 | 55 (52) | +2.2 (+2.0) | C |
| 168 | `F665` | breadth thrust Zweig aktif (20 sesi) + earnings dalam 1-5 sesi akan datang | M18 EMA9/21 Pullback (benih M, parameter asal) | 15 (8) | 24:16 | 54 (55) | +3.0 (+2.7) | C i |
| 169 | `F1849` | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang | K01.020 RSI(3) < 5 + atas MA200 | 15 (8) | 25:20 | 53 (51) | +2.2 (+1.3) | B |
| 170 | `F1381` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K13.001 Stochastic(5) silang naik dari bawah 10 | 15 (10) | 25:23 | 56 (52) | +3.8 (+2.6) | C |
| 171 | `F471` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K24.006 bar pembalikan (buka <= 20%, tutup >= 90% julat) | 15 (9) | 23:21 | 56 (54) | +2.3 (+1.9) | D y |
| 172 | `F762` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K04.006 masuk semula atas jalur bawah BB(20, 2.5) | 15 (9) | 26:21 | 51 (49) | +2.4 (+1.5) | B k |
| 173 | `F1970` | 7 hari pertama bulan + 0-4 sesi selepas earnings | K14.029 lonjakan >= 5.0% + volum 3.0x | 15 (10) | 29:23 | 53 (43) | +2.6 (-0.1) | D xkh |
| 174 | `F736` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K02.026 RSI(14) silang atas 40 | 14 (9) | 26:25 | 52 (51) | +2.0 (+2.1) | C |
| 175 | `F1585` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K13.005 Stochastic(9) silang naik dari bawah 10 | 14 (8) | 19:15 | 59 (57) | +3.0 (+2.5) | D t |
| 176 | `F594` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K08.014 ema10 silang atas ema50 | 14 (8) | 24:19 | 51 (52) | +2.3 (+1.5) | C |
| 177 | `F1583` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.092 RSI(14) < 40 + atas MA200 | 14 (7) | 23:14 | 57 (54) | +3.0 (+2.0) | A |
| 178 | `F385` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K24.006 bar pembalikan (buka <= 20%, tutup >= 90% julat) | 14 (7) | 24:16 | 56 (52) | +2.0 (+1.4) | B |
| 179 | `F03` | tiada | M01 Bollinger Band + RSI (ditala 2) | 14 (14) | 33:26 | 51 (51) | +5.4 (+3.4) | D xhy |
| 180 | `F1701` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K02.024 RSI(14) silang atas 30 | 14 (10) | 27:22 | 50 (47) | +2.2 (+0.8) | C k |
| 181 | `F806` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.025 RSI(3) < 15 | 14 (9) | 24:17 | 56 (53) | +2.7 (+2.4) | B |
| 182 | `F1590` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K13.005 Stochastic(9) silang naik dari bawah 10 | 14 (7) | 19:13 | 59 (57) | +3.1 (+2.5) | D t |
| 183 | `F1755` | >= 60% saham di atas MA200 + earnings dalam 1-5 sesi akan datang | K06.010 6 tutup menurun berturut + atas MA200 | 14 (7) | 25:17 | 50 (47) | +2.2 (+1.0) | B |
| 184 | `F1319` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K02.016 RSI(10) silang atas 25 | 14 (9) | 27:18 | 52 (48) | +2.3 (+1.0) | B k |
| 185 | `F1489` | hari 90% turun kemudian naik (20 sesi) + earnings dalam 1-5 sesi akan datang | K07.020 tutup silang atas ema200 | 14 (8) | 25:17 | 55 (53) | +2.9 (+2.0) | B |
| 186 | `F1109` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.004 RSI(2) < 5 + atas MA200 | 14 (9) | 24:17 | 59 (55) | +3.1 (+2.7) | B |
| 187 | `F1023` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.006 4 tutup menurun berturut + atas MA200 | 14 (8) | 22:18 | 57 (54) | +3.6 (+2.8) | B |
| 188 | `F1828` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K01.079 RSI(10) < 25 | 14 (9) | 26:23 | 52 (48) | +2.0 (+1.2) | B k |
| 189 | `F425` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.007 RSI(2) < 10 | 14 (7) | 23:19 | 55 (51) | +3.0 (+2.1) | B |
| 190 | `F389` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K21.001 NR4 | 14 (10) | 28:23 | 54 (51) | +2.7 (+2.3) | C |
| 191 | `F11` | QQQ OFF | M01 Bollinger Band + RSI (ditala 2) | 14 (13) | 26:21 | 52 (51) | +3.2 (+2.9) | D xh |
| 192 | `F453` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K08.010 ema10 silang atas ema20 | 14 (7) | 24:22 | 54 (51) | +2.1 (+1.4) | C |
| 193 | `F1258` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K04.006 masuk semula atas jalur bawah BB(20, 2.5) | 14 (9) | 26:21 | 52 (49) | +2.2 (+1.5) | B k |
| 194 | `F745` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K21.002 NR4 + hari dalam | 14 (9) | 29:25 | 52 (48) | +2.2 (+1.0) | B k |
| 195 | `F1827` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K01.058 RSI(5) < 15 + atas MA200 | 14 (8) | 24:17 | 54 (49) | +3.2 (+1.8) | B k |
| 196 | `F419` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K08.010 ema10 silang atas ema20 | 14 (7) | 24:21 | 53 (50) | +2.0 (+1.4) | C |
| 197 | `F95` | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K19.011 pecah atas Keltner(30, 1.0) | 14 (8) | 28:25 | 51 (43) | +4.6 (-0.1) | C |
| 198 | `F885` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K02.008 RSI(7) silang atas 20 | 14 (8) | 25:18 | 54 (47) | +2.5 (+0.5) | B k |
| 199 | `F1395` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K11.004 Supertrend(7, 3.0) bertukar naik | 13 (9) | 24:21 | 54 (55) | +2.4 (+2.2) | C |
| 200 | `F1373` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.027 tutup < jalur bawah BB(20, 1.5) + RSI14 < 40 | 13 (6) | 20:13 | 54 (52) | +2.1 (+1.6) | D t |
| 201 | `F1810` | SPY bawah SMA200 + sektor 3 teratas (pulangan 63 sesi) | K04.009 masuk semula atas jalur bawah BB(30, 2.5) | 13 (11) | 25:24 | 59 (54) | +4.5 (+3.2) | D xhyt |
| 202 | `F1354` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K07.019 tutup silang atas sma200 | 13 (6) | 21:11 | 57 (54) | +2.2 (+1.5) | A |
| 203 | `F377` | breadth thrust Zweig aktif (20 sesi) + earnings dalam 1-5 sesi akan datang | M18 EMA9/21 Pullback (benih M, varian 2: ema_a1_21=26, ema_a | 13 (8) | 22:16 | 54 (54) | +3.2 (+2.4) | C i |
| 204 | `F2031` | distribution day QQQ >= 5 dalam 25 sesi + kejutan untung terkini positif (SUE > 0) | K01.075 RSI(10) < 15 | 13 (11) | 29:27 | 51 (47) | +2.3 (+1.4) | D xhy |
| 205 | `F42` | distribution day QQQ <= 2 dalam 25 sesi + >= 60% saham industri di atas MA50 | M159 Heikin-Ashi Trend (ditala 1) | 12 (8) | 25:19 | 51 (47) | +4.0 (+1.9) | D xh |
| 206 | `F02` | QQQ OFF | M111 Sistem Volatiliti Wilder (ditala 2) | 12 (11) | 22:21 | 53 (52) | +2.0 (+2.2) | D xhy |
| 207 | `F2017` | >= 60% saham di atas MA50 + hasil suku terkini tumbuh >= 20% | K16.017 gap-and-go (buka > tinggi semalam + 5.0%) | 12 (9) | 24:24 | 51 (44) | +2.1 (+0.4) | D xhy |
| 208 | `F401` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K08.008 ema8 silang atas ema21 | 11 (8) | 20:18 | 53 (53) | +2.0 (+1.7) | D h |
| 209 | `F1009` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | M28 VWAP Separator + Kiss Pivot (benih M, varian 2: ambang=1 | 11 (7) | 18:13 | 57 (56) | +2.3 (+2.1) | D iht |
| 210 | `F1797` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M147 Improved Three-Bar Pullback (benih M, varian 1: ema_3=3 | 8 (7) | 22:18 | 53 (51) | +2.2 (+1.8) | D hy |
| 211 | `F1697` | <= 30% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K18.030 jatuh >= 8% dalam 20 hari | 19 (11) | 30:22 | 50 (52) | +1.2 (+1.5) | B |
| 212 | `F1038` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.081 RSI(10) < 30 | 18 (9) | 30:20 | 53 (51) | +1.8 (+1.1) | B |
| 213 | `F1459` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K18.030 jatuh >= 8% dalam 20 hari | 18 (9) | 29:20 | 54 (52) | +2.0 (+1.7) | C |
| 214 | `F551` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.069 RSI(7) < 25 | 18 (10) | 31:22 | 51 (50) | +1.6 (+1.1) | C |
| 215 | `F96` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s1: c_kali_ | 18 (10) | 36:26 | 50 (45) | +2.7 (+0.6) | C i |
| 216 | `F706` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.059 RSI(5) < 20 | 18 (9) | 30:23 | 52 (50) | +1.9 (+1.2) | A |
| 217 | `F869` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K13.004 Stochastic(5) silang naik dari bawah 40 | 18 (11) | 35:27 | 50 (49) | +1.7 (+1.5) | C |
| 218 | `F405` | earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, parameter asal) | 18 (11) | 36:28 | 49 (46) | +2.4 (+1.2) | B i |
| 219 | `F1880` | QQQ RSI14 < 35 + 5-19 sesi selepas earnings | K18.017 jatuh >= 10% dalam 5 hari | 18 (14) | 44:14 | 49 (44) | -0.6 (-1.3) | D xh |
| 220 | `F804` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K02.019 RSI(10) silang atas 40 | 18 (12) | 32:32 | 52 (53) | +1.8 (+3.2) | C |
| 221 | `F418` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.069 RSI(7) < 25 | 18 (9) | 29:25 | 50 (49) | +1.2 (+1.0) | C |
| 222 | `F1150` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K18.008 jatuh >= 5% dalam 3 hari | 17 (11) | 30:25 | 51 (50) | +1.7 (+1.6) | C |
| 223 | `F1815` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K18.031 jatuh >= 10% dalam 20 hari | 17 (11) | 30:24 | 52 (50) | +1.8 (+1.7) | C |
| 224 | `F1416` | 7 hari pertama bulan + earnings dalam 1-5 sesi akan datang | K18.024 jatuh >= 10% dalam 10 hari | 17 (13) | 32:29 | 48 (48) | +1.5 (+1.1) | D kh |
| 225 | `F114` | earnings dalam 1-5 sesi akan datang | K13.012 Stochastic(14) silang naik dari bawah 40 | 17 (9) | 29:23 | 49 (45) | +1.7 (+0.4) | C |
| 226 | `F1788` | <= 30% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K01.090 RSI(14) < 35 + atas MA200 | 17 (11) | 30:17 | 54 (52) | +1.2 (+0.9) | D ht |
| 227 | `F1438` | <= 30% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K01.044 RSI(4) < 20 + atas MA200 | 17 (11) | 25:19 | 55 (54) | +1.7 (+1.7) | B |
| 228 | `F831` | Mei-Okt + earnings dalam 1-5 sesi akan datang | K18.023 jatuh >= 8% dalam 10 hari | 17 (12) | 30:26 | 50 (51) | +3.0 (+2.8) | D ky |
| 229 | `F1714` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K18.031 jatuh >= 10% dalam 20 hari | 17 (10) | 29:25 | 52 (49) | +1.4 (+1.2) | C |
| 230 | `F154` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K06.001 2 tutup menurun berturut | 17 (12) | 39:26 | 49 (49) | +2.5 (+1.4) | C |
| 231 | `F137` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s4: c_kali_ | 17 (10) | 34:26 | 49 (45) | +2.7 (+0.5) | C i |
| 232 | `F2001` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M79 Radge: 20% Flipper (benih M, varian 1: a=0.18) | 17 (7) | 28:20 | 49 (48) | +0.5 (+0.3) | B |
| 233 | `F1444` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: r | 17 (11) | 32:28 | 46 (45) | +1.6 (+0.4) | C |
| 234 | `F110` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI (benih M, varian 3: l_kali_0_9 | 17 (9) | 26:24 | 52 (52) | +1.0 (+1.4) | C i |
| 235 | `F1856` | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang | K18.017 jatuh >= 10% dalam 5 hari | 16 (11) | 32:28 | 47 (44) | +0.6 (-0.2) | C |
| 236 | `F564` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K09.004 MACD(8,17,9) silang naik | 16 (9) | 37:31 | 44 (44) | +0.3 (-0.1) | C |
| 237 | `F621` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | M155 Market Cycle Strategy (benih M, varian 2: had_henti=0.6 | 16 (8) | 33:30 | 47 (42) | -0.4 (-0.8) | B |
| 238 | `F289` | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang | K02.034 RSI(21) silang atas 50 | 16 (8) | 28:25 | 48 (45) | +1.7 (+0.3) | C |
| 239 | `F111` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K17.031 undur ke ema50 yang naik (tol 1.0%) | 16 (9) | 31:27 | 48 (43) | +1.9 (+0.1) | B |
| 240 | `F714` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.081 RSI(10) < 30 | 16 (10) | 28:24 | 51 (51) | +2.0 (+1.9) | B |
| 241 | `F1937` | Mei-Okt + saham lain dalam industri sama naik >= 20% dalam 20 sesi | K18.010 jatuh >= 10% dalam 3 hari | 16 (14) | 31:23 | 48 (50) | +2.3 (+3.0) | D xkhy |
| 242 | `F1124` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.021 RSI(3) < 8 | 16 (9) | 27:19 | 50 (52) | +0.6 (+1.1) | C |
| 243 | `F1050` | nisbah 4% (10 hari) > 2 + earnings dalam 1-5 sesi akan datang | M79 Radge: 20% Flipper (benih M, parameter asal) | 16 (7) | 28:15 | 54 (49) | +1.0 (+0.5) | B |
| 244 | `F1152` | follow-through day aktif (QQQ, 20 sesi) + earnings dalam 1-5 sesi akan datang | K02.033 RSI(21) silang atas 40 | 16 (9) | 25:25 | 50 (51) | +1.6 (+2.1) | C |
| 245 | `F1390` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K01.089 RSI(14) < 35 | 16 (10) | 28:23 | 51 (50) | +1.8 (+1.7) | B |
| 246 | `F1372` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K03.053 tutup < jalur bawah BB(50, 2.0) + RSI14 < 30 | 16 (10) | 29:25 | 50 (49) | +0.9 (+0.7) | B |
| 247 | `F1042` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.057 RSI(5) < 15 | 16 (9) | 27:20 | 51 (51) | +0.9 (+1.0) | B |
| 248 | `F1526` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.021 RSI(3) < 8 | 16 (9) | 28:23 | 50 (49) | +1.0 (+0.8) | C |
| 249 | `F121` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | N29 PSAR naik + tutup>MA50 (benih N) | 16 (9) | 34:29 | 49 (46) | +1.8 (+0.9) | C |
| 250 | `F870` | rejim OFF baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | K03.030 tutup < jalur bawah BB(20, 2.0) + RSI14 < 40 | 16 (9) | 27:20 | 52 (51) | +1.8 (+1.1) | C |
| 251 | `F1293` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K18.008 jatuh >= 5% dalam 3 hari | 16 (10) | 29:26 | 50 (49) | +0.8 (+1.1) | C |
| 252 | `F92` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M03 BB Break + Divergence RSI | 16 (10) | 25:24 | 54 (53) | +1.8 (+1.9) | D iy |
| 253 | `F1653` | 7 hari pertama bulan + earnings dalam 1-5 sesi akan datang | K01.039 RSI(4) < 10 | 16 (9) | 24:27 | 50 (50) | +0.7 (+0.7) | C k |
| 254 | `F1094` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K03.052 tutup < jalur bawah BB(50, 2.0) | 16 (10) | 26:17 | 52 (53) | +1.1 (+1.5) | C |
| 255 | `F1286` | >= 60% saham di atas MA200 + earnings dalam 1-5 sesi akan datang | K03.014 tutup < jalur bawah BB(15, 1.5) + RSI14 < 30 | 16 (11) | 33:23 | 48 (44) | +2.9 (+0.3) | B |
| 256 | `F1432` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | K18.024 jatuh >= 10% dalam 10 hari | 16 (10) | 29:23 | 50 (47) | +1.3 (+0.7) | B |
| 257 | `F1916` | distribution day QQQ >= 5 dalam 25 sesi + 5-19 sesi selepas earnings | K18.017 jatuh >= 10% dalam 5 hari | 16 (12) | 34:27 | 47 (46) | +2.3 (+0.5) | D xh |
| 258 | `F253` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K07.004 tutup silang atas ema8 | 16 (10) | 34:26 | 48 (46) | +2.3 (+0.9) | B |
| 259 | `F689` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | M92 CCI-50 (benih M, varian 1: cci_50=41, rma_atr_14=16, rma | 16 (10) | 33:31 | 49 (46) | +1.4 (+1.0) | C |
| 260 | `F1927` | Mei-Okt + 0-4 sesi selepas earnings | K18.035 jatuh >= 30% dalam 20 hari | 16 (12) | 39:22 | 41 (45) | +0.7 (+0.2) | D xkhy |
| 261 | `F501` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K08.006 ema5 silang atas ema20 | 16 (9) | 26:23 | 53 (53) | +1.9 (+2.1) | C |
| 262 | `F1943` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | K18.002 jatuh >= 8% dalam 2 hari | 16 (11) | 31:24 | 48 (45) | +2.8 (+0.8) | B x |
| 263 | `F1790` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K02.032 RSI(21) silang atas 35 | 16 (11) | 29:23 | 51 (50) | +1.6 (+1.5) | C |
| 264 | `F268` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | K02.007 RSI(5) silang atas 60 | 16 (9) | 27:22 | 51 (51) | +1.6 (+1.6) | C |
| 265 | `F115` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K13.012 Stochastic(14) silang naik dari bawah 40 | 16 (7) | 29:23 | 47 (42) | +1.1 (-0.5) | B |
| 266 | `F100` | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | K13.012 Stochastic(14) silang naik dari bawah 40 | 16 (7) | 28:24 | 48 (43) | +1.0 (-0.2) | B |
| 267 | `F1376` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K04.006 masuk semula atas jalur bawah BB(20, 2.5) | 16 (10) | 28:22 | 53 (50) | +1.4 (+1.0) | C |
| 268 | `F1953` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K03.056 tutup < jalur bawah BB(50, 2.5) + RSI14 < 30 | 16 (10) | 27:24 | 47 (48) | -0.0 (+0.2) | D ht |
| 269 | `F138` | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | M20 EMA10/15 Crossover + Sudut (benih M, varian 0s1: c_kali_ | 16 (9) | 33:30 | 48 (44) | +1.5 (+0.4) | B i |
| 270 | `F1488` | earnings dalam 1-5 sesi akan datang | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: r | 16 (10) | 31:28 | 46 (45) | +1.0 (+0.4) | C |
| 271 | `F1410` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K03.002 tutup < jalur bawah BB(10, 1.5) + RSI14 < 30 | 16 (9) | 26:23 | 52 (52) | +1.4 (+1.1) | C |
| 272 | `F700` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.001 RSI(2) < 3 | 16 (8) | 26:21 | 52 (50) | +1.2 (+1.0) | C |
| 273 | `F58` | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | N16 RSI2<10 tanpa penapis | 16 (8) | 35:27 | 47 (43) | +0.3 (-0.3) | B |
| 274 | `F1440` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K03.002 tutup < jalur bawah BB(10, 1.5) + RSI14 < 30 | 16 (10) | 29:24 | 50 (48) | +1.7 (+0.8) | B |
| 275 | `F657` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K08.002 ema3 silang atas ema10 | 16 (9) | 36:28 | 46 (43) | +1.0 (-0.4) | B |
| 276 | `F1297` | SPY atas SMA200 + earnings dalam 1-5 sesi akan datang | K18.016 jatuh >= 8% dalam 5 hari | 16 (11) | 30:22 | 49 (47) | +1.6 (+0.9) | B |
| 277 | `F742` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K13.015 Stochastic(21) silang naik dari bawah 30 | 16 (8) | 34:28 | 46 (43) | +1.3 (-0.3) | A |
| 278 | `F460` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M13 Garis Trend Action/Safety Line (benih M, varian 2: k=4) | 16 (9) | 27:20 | 54 (53) | +1.7 (+2.0) | C i |
| 279 | `F210` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K07.007 tutup silang atas sma15 | 15 (9) | 34:27 | 46 (43) | +0.7 (-0.3) | B |
| 280 | `F1756` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K03.017 tutup < jalur bawah BB(15, 2.0) + RSI14 < 30 | 15 (10) | 30:27 | 48 (46) | +0.6 (+0.0) | B |
| 281 | `F1613` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | M106 DMI Wilder (benih M, parameter asal) | 15 (8) | 23:23 | 53 (53) | +1.7 (+2.0) | D iy |
| 282 | `F1948` | QQQ OFF + earnings dalam 1-5 sesi akan datang | K03.056 tutup < jalur bawah BB(50, 2.5) + RSI14 < 30 | 15 (11) | 27:22 | 52 (51) | +1.5 (+1.5) | C |
| 283 | `F1335` | <= 30% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | K01.026 RSI(3) < 15 + atas MA200 | 15 (10) | 24:15 | 55 (55) | +1.6 (+1.8) | D hyt |
| 284 | `F41` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | N119 3 tutup turun berturut | 15 (10) | 32:34 | 47 (44) | +0.5 (-0.0) | C |
| 285 | `F557` | >= 60% saham di atas MA200 + earnings dalam 1-5 sesi akan datang | K13.003 Stochastic(5) silang naik dari bawah 30 | 15 (7) | 30:22 | 49 (43) | +1.5 (+0.0) | A |
| 286 | `F1181` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K03.042 tutup < jalur bawah BB(30, 2.0) + RSI14 < 40 | 15 (9) | 26:19 | 51 (51) | +1.1 (+1.0) | C |
| 287 | `F1780` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | K02.032 RSI(21) silang atas 35 | 15 (11) | 28:24 | 51 (51) | +1.8 (+1.8) | C |
| 288 | `F1163` | SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang | M84 Jarak purata bergerak MAD 21/200 (benih M, varian 1: clo | 15 (9) | 29:29 | 46 (44) | +1.2 (+0.2) | C |
| 289 | `F1518` | nisbah 4% (10 hari) < 0.5 + earnings dalam 1-5 sesi akan datang | K01.021 RSI(3) < 8 | 15 (8) | 26:22 | 47 (48) | -0.2 (+0.3) | D ht |
| 290 | `F980` | Nov-Apr + earnings dalam 1-5 sesi akan datang | M84 Jarak purata bergerak MAD 21/200 (benih M, varian 1: clo | 15 (8) | 28:26 | 48 (46) | +0.7 (+0.2) | C k |
| 291 | `F1492` | distribution day QQQ >= 5 dalam 25 sesi + earnings dalam 1-5 sesi akan datang | M28 VWAP Separator + Kiss Pivot (benih M, varian 1: ambang=2 | 15 (10) | 29:23 | 51 (49) | +1.5 (+1.2) | C i |
| 292 | `F577` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | K22.002 Holy Grail (ADX > 20, undur EMA20) | 15 (7) | 23:20 | 49 (50) | +0.5 (+0.7) | C |
| 293 | `F127` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | N41 CMF20>0 + tutup>EMA20 (benih N) | 15 (9) | 24:24 | 49 (52) | +1.4 (+1.6) | C |
| 294 | `F978` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.001 RSI(2) < 3 | 15 (8) | 25:20 | 52 (51) | +1.4 (+1.1) | B |
| 295 | `F1865` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham sektor di atas MA50 | K18.010 jatuh >= 10% dalam 3 hari | 15 (12) | 33:25 | 47 (47) | +4.6 (+2.0) | D xh |
| 296 | `F707` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | N43 Undur EMA8 + penapis MA50 (benih N) | 15 (9) | 34:26 | 48 (44) | +1.2 (-0.0) | A |
| 297 | `F1973` | distribution day QQQ >= 5 dalam 25 sesi + kejutan untung terkini positif (SUE > 0) | K01.053 RSI(5) < 8 | 15 (13) | 27:25 | 49 (48) | +2.2 (+1.8) | D xhy |
| 298 | `F211` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | M13 Garis Trend Action/Safety Line (benih M, varian 1: k=2) | 15 (9) | 28:18 | 53 (53) | +1.4 (+1.7) | B i |
| 299 | `F269` | >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | K09.007 MACD(5,35,5) silang naik | 15 (9) | 37:27 | 46 (44) | +0.5 (-0.1) | B |
| 300 | `F1530` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + earnings dalam 1-5 sesi akan datang | K01.057 RSI(5) < 15 | 15 (9) | 24:18 | 50 (52) | +1.1 (+1.2) | B |

## 6. Fail

- `audit.csv.gz`: satu baris setiap setup senarai utama (semua ukuran, gred, nota, versi tanpa intai `k_*`).
- `gabungan.csv`, `bebas.csv`, `intai.csv`, `bacaan.json`.
