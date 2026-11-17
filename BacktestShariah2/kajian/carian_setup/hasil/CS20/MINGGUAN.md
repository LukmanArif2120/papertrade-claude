# CS20: setup "sepanjang tahun" — membeli hampir setiap minggu (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_mingguan20.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (ag). **Jangan sunting secara manual.**

## 1. Apa yang dibuat

- Carian yang sama dengan CS13 (kayu ukur = KADAR TANGKAP: naik ≥ 5 % minggu pertama, naik lagi hingga minggu ke-4, −8 % tidak disentuh), dengan dua had: prasyarat yang bergantung pada tarikh laporan kewangan atau pada kalendar TIDAK dibenarkan, dan setiap setup mesti membeli dalam ≥ 80% minggu (≥ 50% minggu pada tahun paling teruk), diukur pada separuh saham.
- 1,156 isyarat beli (kaedah M dan N dalam mod tanpa intai, indikator dan variannya; 1,116 cukup isyarat) × prasyarat yang dibenarkan × penapis saham. 93,528 peraturan ditinjau mengikut susunan skor; **1,691 calon** (sehingga 5 setiap isyarat beli) menepati syarat kekerapan pada saham carian.
- Setup lengkap: beli pada buka esok; stop loss 4xATR14; pegang sekurang-kurangnya 20 hari, kemudian jual bila tutup di bawah purata 20 hari; paling lama 6 bulan (cara pegang B).
- "Lulus" = pada saham yang carian tidak lihat: belian ≥ 300, ≥ 10 tahun aktif, dan kadar tangkap melebihi saham rawak hari sama dalam KETIGA-TIGA tempoh (2010–19, 2020–24, 2025–26).

## 2. Ujian (ditetapkan dahulu)

- Kawalan = 300 peraturan rawak daripada ruang yang SAMA yang juga membeli hampir setiap minggu (dicuba 37,316).
- **B1** kadar lulus: calon **74 %** lawan kawalan 23 % (perlu beza ≥ 20 mata) → lulus.
- **B2** lebih baik daripada rawak pada 2025–26: calon **81 %** lawan kawalan 67 % (perlu ≥ 60 % dan beza ≥ 10 mata) → lulus.
- **Keputusan: carian setup sepanjang tahun BERHASIL — kod F didaftarkan.**
- Semakan ikut tahun (dilaporkan, bukan syarat): calon lulus lebih baik daripada rawak dalam 76 % tahun (nilai tengah); kawalan 53 %.

## 3. Berapa yang lulus dan didaftarkan

- Lulus: **1,243** daripada 1,691 calon; 1,201 daripadanya juga membeli hampir setiap minggu pada saham yang carian tidak lihat.
- Kembar setup lain (pertindihan belian ≥ 80%; termasuk kembar kod F sedia ada): 453 (3 kembar kod F sedia ada) — tidak diberi kod.
- **Setup berlainan yang lulus: 748** → didaftarkan sebagai **`F2055`–`F2802`** (748 kod baharu).
- Anggaran bahagian yang lulus kerana nasib (kadar lulus kawalan ÷ kadar lulus calon): kira-kira 31 %.

## 4. Ikut tempoh (peraturan yang cukup belian; saham yang carian tidak lihat)

| Kumpulan | Bilangan | Lebih baik daripada rawak: 2010–19 | 2020–24 | **2025–26** | Median kelebihan tangkap 2010–19 / 2020–24 / 2025–26 (mata) | Lulus |
|---|---|---|---|---|---|---|
| Calon | 1,691 | 96% | 94% | **81%** | +1.2 / +1.1 / +0.9 | 74% |
| Kawalan rawak (ruang sama) | 300 | 56% | 52% | **67%** | +0.1 / +0.0 / +0.4 | 23% |
| Kod F sepanjang tahun sedia ada | 112 | 95% | 92% | **89%** | +2.2 / +1.3 / +1.5 | 84% |
| Kod baharu | 748 | 100% | 100% | **100%** | +1.4 / +1.2 / +1.2 | 100% |

## 5. Mutu (nilai tengah setiap kumpulan; saham yang carian tidak lihat; kurungan = saham rawak hari sama)

| Kumpulan | Bilangan | Tangkap % | Naik ≥ 5 % minggu 1 | JATUH ≥ 5 % minggu 1 | Menang % cara B (rawak dipegang sama) | Purata % cara B (rawak dipegang sama) | Rugi ≥ 15 % | Minggu ada belian |
|---|---|---|---|---|---|---|---|---|
| Kod baharu | 748 | 11.2 (9.8) | 23 (20) | 21 (19) | 46 (46) | +1.1 (+0.7) | 15 (12) | 91 % |
| Calon lulus | 1,243 | 10.3 (9.1) | 21 (19) | 20 (17) | 46 (46) | +1.0 (+0.6) | 14 (11) | 91 % |
| Kawalan rawak (ruang sama) | 300 | 5.6 (5.4) | 11 (11) | 11 (11) | 46 (45) | +0.3 (+0.2) | 5 (4) | 93 % |
| Kod F sepanjang tahun sedia ada | 112 | 12.3 (10.3) | 25 (21) | 24 (20) | 47 (45) | +1.5 (+0.7) | 18 (14) | 31 % |

## 6. Kod baharu: pecahan

- Dengan prasyarat pasaran: 0; dengan prasyarat kumpulan / syarikat: 288; tanpa apa-apa prasyarat: 460.
- Prasyarat paling kerap: tiada (460); hasil suku terkini tumbuh >= 20% (200); >= 60% saham industri di atas MA50 (26); >= 60% saham sektor di atas MA50 (22); industri 20% teratas (pulangan 63 sesi) (16); sektor 3 teratas (pulangan 63 sesi) (16); industri 20% teratas (pulangan 21 sesi) (3); industri 20% terbawah (pulangan 63 sesi) (3).
- Penapis saham paling kerap: MA50 > MA200 + ATR% >= 4 (53); ADX < 20 + >= 30% di bawah puncak 52 minggu (48); RS >= 70 + ATR% >= 4 (44); RS >= 90 + ATR% >= 4 (36); ATR% >= 4 (31); MA50 naik (lawan 20 bar lalu) + ATR% >= 4 (30); volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 (25); volum 10 hari > volum 50 hari + ATR% >= 4 (22).
- Isyarat beli: 81 kaedah / keluarga berbeza; paling kerap K01 (143), K03 (101), K18 (47), K09 (36), K13 (34), K07 (33), K02 (26), K17 (24).
- Kelebihan tangkap > 0 pada 2025–26: 748 daripada 748 (syarat lulus, jadi bukan bukti di luar sampel).
- `arah` > 0 (tambahan naik melebihi tambahan jatuh): 531 daripada 748; menang cara B melebihi saham rawak yang dipegang sama: 569; purata melebihi: 655.
- Jualan pada hari beli: 0 (mesti 0).

## 7. Kod baharu (teratas 60 ikut kelebihan tangkap; senarai penuh `mingguan.csv`)

| # | ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun (semua saham) | Minggu ada belian | **Tangkap %** (rawak) | Naik ≥ 5 % (rawak) | Jatuh ≥ 5 % (rawak) | Menang % (rawak) | Purata % (rawak) | 2025–26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `F2125` | – | K18.016 jatuh >= 8% dalam 5 hari | RS >= 90 + ATR% >= 4 | 460 | 91 % | **14.3** (10.9) | 30 (23) | 25 (21) | 47 (46) | +2.7 (+1.0) | +4.2 |
| 2 | `F2212` | industri 20% teratas (pulangan 63 sesi) | K01.010 RSI(2) < 15 + atas MA200 | ATR% >= 4 | 454 | 92 % | **13.4** (10.4) | 26 (22) | 21 (20) | 47 (45) | +2.0 (+0.7) | +2.2 |
| 3 | `F2339` | – | K01.061 RSI(5) < 25 | RS >= 70 + ATR% >= 4 | 737 | 94 % | **14.3** (11.5) | 28 (24) | 24 (22) | 47 (47) | +2.2 (+1.2) | +3.3 |
| 4 | `F2193` | – | K03.001 tutup < jalur bawah BB(10, 1.5) | RS >= 90 + ATR% >= 4 | 501 | 93 % | **13.5** (10.7) | 28 (23) | 25 (21) | 46 (46) | +1.8 (+0.8) | +1.4 |
| 5 | `F2141` | – | K01.062 RSI(5) < 25 + atas MA200 | MACD > 0 + ATR% >= 4 | 545 | 90 % | **13.5** (10.7) | 27 (23) | 22 (20) | 46 (46) | +1.6 (+0.9) | +2.2 |
| 6 | `F2135` | – | K01.043 RSI(4) < 20 | RS >= 70 + ATR% >= 4 | 730 | 94 % | **14.1** (11.5) | 28 (24) | 24 (21) | 48 (47) | +2.4 (+1.2) | +2.7 |
| 7 | `F2098` | – | K01.072 RSI(7) < 30 + atas MA200 | RS >= 70 + ATR% >= 4 | 545 | 92 % | **13.8** (11.2) | 28 (23) | 23 (20) | 46 (46) | +1.9 (+0.8) | +2.0 |
| 8 | `F2154` | industri 20% teratas (pulangan 63 sesi) | K17.024 undur ke ema20 yang naik (tol 2.0%) + atas MA200 | MA20 > MA50 + ATR% >= 4 | 391 | 92 % | **12.3** (9.8) | 25 (21) | 23 (20) | 47 (45) | +2.0 (+0.6) | +2.6 |
| 9 | `F2068` | – | K18.015 jatuh >= 5% dalam 5 hari | Supertrend naik + RS >= 90 | 622 | 94 % | **12.4** (9.9) | 25 (21) | 21 (18) | 46 (46) | +1.5 (+0.9) | +2.6 |
| 10 | `F2087` | – | K18.016 jatuh >= 8% dalam 5 hari | ADX > 25 + RS >= 70 | 701 | 92 % | **13.2** (10.7) | 27 (22) | 20 (18) | 48 (47) | +1.8 (+0.8) | +2.0 |
| 11 | `F2253` | – | K01.025 RSI(3) < 15 | RS >= 70 + ATR% >= 4 | 802 | 95 % | **14.0** (11.5) | 28 (24) | 24 (21) | 48 (47) | +2.4 (+1.2) | +2.3 |
| 12 | `F2340` | – | K01.007 RSI(2) < 10 | RS >= 70 + ATR% >= 4 | 1037 | 98 % | **13.8** (11.4) | 28 (23) | 23 (21) | 48 (47) | +2.2 (+1.3) | +1.9 |
| 13 | `F2611` | – | K01.004 RSI(2) < 5 + atas MA200 | MACD > 0 + ATR% >= 4 | 554 | 91 % | **13.2** (10.8) | 27 (23) | 21 (20) | 47 (46) | +1.5 (+0.9) | +1.7 |
| 14 | `F2373` | – | M161 EMA 10/21 + Supertrend (10,3) (benih M, varian 2: ema_21=33, had_henti=0.931, henti_pct=10.323, rolling_10=19, rolling_5=2, supertrend_hijau_10=11) | RS >= 90 + ATR% >= 4 | 586 | 98 % | **12.3** (9.9) | 26 (21) | 25 (20) | 46 (45) | +1.5 (+0.8) | +1.4 |
| 15 | `F2119` | – | K01.046 RSI(4) < 25 + atas MA200 | RSI14 < 40 + ATR% >= 4 | 523 | 92 % | **13.7** (11.3) | 27 (23) | 22 (20) | 46 (46) | +1.6 (+0.8) | +2.6 |
| 16 | `F2218` | – | M39 Radge Pecahan Bollinger 100 hari (benih M, varian 1: c_kali_0_85=0.658, sd_kali_2=1.284) | RS >= 90 + ATR% >= 4 | 364 | 95 % | **12.4** (10.0) | 26 (21) | 26 (20) | 45 (45) | +1.1 (+0.6) | +0.3 |
| 17 | `F2059` | – | K18.016 jatuh >= 8% dalam 5 hari | RS >= 70 + ATR% >= 4 | 940 | 96 % | **14.1** (11.7) | 29 (24) | 23 (21) | 49 (47) | +2.8 (+1.3) | +1.9 |
| 18 | `F2083` | – | K18.015 jatuh >= 5% dalam 5 hari | MACD > 0 + RS >= 90 | 751 | 96 % | **12.1** (9.8) | 25 (20) | 20 (18) | 46 (46) | +1.5 (+0.7) | +3.2 |
| 19 | `F2074` | – | K01.044 RSI(4) < 20 + atas MA200 | MA50 > MA200 + ATR% >= 4 | 854 | 96 % | **13.3** (11.0) | 27 (23) | 22 (20) | 47 (46) | +2.0 (+0.9) | +1.8 |
| 20 | `F2335` | >= 60% saham industri di atas MA50 | K07.001 tutup silang atas sma5 | RS >= 90 + ATR% >= 4 | 431 | 92 % | **11.8** (9.5) | 26 (21) | 25 (21) | 45 (44) | +1.4 (+0.6) | +1.9 |
| 21 | `F2067` | >= 60% saham sektor di atas MA50 | K01.031 RSI(3) < 30 | RS >= 90 | 664 | 85 % | **9.9** (7.6) | 20 (16) | 16 (15) | 45 (45) | +0.9 (+0.3) | +4.0 |
| 22 | `F2711` | – | N47 NR7 + EMA9>EMA21 (benih N) | RS >= 90 + ATR% >= 4 | 530 | 97 % | **12.2** (9.9) | 26 (21) | 24 (20) | 46 (45) | +1.3 (+0.6) | +2.1 |
| 23 | `F2185` | – | K01.026 RSI(3) < 15 + atas MA200 | MA50 naik (lawan 20 bar lalu) + ATR% >= 4 | 835 | 95 % | **13.0** (10.7) | 26 (23) | 22 (20) | 47 (46) | +1.8 (+0.8) | +0.8 |
| 24 | `F2208` | >= 60% saham industri di atas MA50 | N08 tutup>EMA20 tidak terlalu jauh (benih N) | RS >= 90 + ATR% >= 4 | 417 | 92 % | **11.9** (9.6) | 25 (20) | 25 (20) | 45 (44) | +1.8 (+0.6) | +2.3 |
| 25 | `F2058` | – | K18.015 jatuh >= 5% dalam 5 hari | RSI14 > 50 + RS >= 90 | 418 | 92 % | **12.0** (9.7) | 26 (21) | 21 (18) | 45 (45) | +1.4 (+0.6) | +0.9 |
| 26 | `F2057` | industri 20% teratas (pulangan 63 sesi) | K01.031 RSI(3) < 30 | tutup > MA200 + ATR% >= 4 | 481 | 93 % | **12.7** (10.4) | 26 (22) | 21 (20) | 46 (45) | +1.8 (+0.7) | +1.8 |
| 27 | `F2102` | sektor 3 teratas (pulangan 63 sesi) | K01.030 RSI(3) < 25 + atas MA200 | ATR% >= 4 | 499 | 92 % | **12.5** (10.2) | 26 (22) | 21 (20) | 47 (45) | +1.2 (+0.5) | +0.7 |
| 28 | `F2396` | >= 60% saham industri di atas MA50 | M161 EMA 10/21 + Supertrend (10,3) (benih M, varian 2: ema_21=33, had_henti=0.931, henti_pct=10.323, rolling_10=19, rolling_5=2, supertrend_hijau_10=11) | RS >= 90 + ATR% >= 4 | 405 | 89 % | **12.0** (9.7) | 26 (21) | 24 (20) | 46 (45) | +1.9 (+0.9) | +2.3 |
| 29 | `F2092` | – | K01.024 RSI(3) < 10 + atas MA200 | MA50 > MA200 + ATR% >= 4 | 601 | 91 % | **13.4** (11.1) | 27 (24) | 22 (20) | 47 (46) | +1.7 (+0.9) | +0.7 |
| 30 | `F2062` | – | K18.017 jatuh >= 10% dalam 5 hari | RS >= 70 + ATR% >= 4 | 741 | 93 % | **14.3** (12.1) | 30 (25) | 25 (21) | 48 (47) | +2.6 (+1.3) | +1.8 |
| 31 | `F2413` | – | K01.004 RSI(2) < 5 + atas MA200 | MA50 naik (lawan 20 bar lalu) + ATR% >= 4 | 711 | 94 % | **13.1** (10.9) | 27 (23) | 21 (20) | 47 (46) | +1.6 (+0.8) | +1.2 |
| 32 | `F2423` | – | K08.011 sma10 silang atas sma30 | ADX < 20 + RS >= 90 | 313 | 93 % | **10.5** (8.3) | 20 (17) | 18 (16) | 48 (47) | +1.6 (+0.7) | +2.3 |
| 33 | `F2090` | – | K01.062 RSI(5) < 25 + atas MA200 | ATR% >= 4 | 885 | 96 % | **13.2** (11.0) | 27 (23) | 22 (20) | 47 (46) | +1.9 (+0.9) | +1.5 |
| 34 | `F2099` | – | K01.044 RSI(4) < 20 + atas MA200 | MA20 > MA50 + ATR% >= 4 | 692 | 92 % | **13.1** (11.0) | 26 (23) | 21 (20) | 47 (46) | +1.9 (+0.9) | +2.1 |
| 35 | `F2206` | – | K01.074 RSI(7) < 35 + atas MA200 | MACD > 0 + ATR% >= 4 | 698 | 92 % | **12.9** (10.7) | 26 (23) | 22 (20) | 46 (46) | +1.7 (+0.9) | +1.5 |
| 36 | `F2436` | – | K21.010 NR14 + hari dalam | RS >= 90 + ATR% >= 4 | 304 | 93 % | **11.8** (9.7) | 26 (21) | 25 (20) | 45 (44) | +1.2 (+0.5) | +0.6 |
| 37 | `F2145` | – | K18.015 jatuh >= 5% dalam 5 hari | RS >= 90 + dalam 15% dari puncak 52 minggu | 600 | 96 % | **11.6** (9.4) | 23 (19) | 17 (17) | 48 (47) | +1.4 (+0.7) | +3.0 |
| 38 | `F2653` | – | K01.067 RSI(7) < 20 | volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 | 700 | 95 % | **14.4** (12.3) | 29 (25) | 24 (23) | 49 (47) | +2.1 (+1.6) | +1.4 |
| 39 | `F2290` | – | K01.006 RSI(2) < 8 + atas MA200 | tutup > MA50 + RS >= 90 | 596 | 96 % | **10.3** (8.2) | 21 (17) | 17 (15) | 48 (46) | +1.1 (+0.5) | +4.2 |
| 40 | `F2108` | sektor 3 teratas (pulangan 63 sesi) | K01.029 RSI(3) < 25 | MA50 naik (lawan 20 bar lalu) + ATR% >= 4 | 646 | 92 % | **12.3** (10.1) | 25 (21) | 22 (21) | 46 (44) | +1.2 (+0.4) | +1.6 |
| 41 | `F2080` | – | K01.027 RSI(3) < 20 | templat trend Minervini + RS >= 90 | 555 | 94 % | **10.2** (8.1) | 20 (17) | 16 (15) | 47 (46) | +1.0 (+0.5) | +5.0 |
| 42 | `F2576` | – | K01.060 RSI(5) < 20 + atas MA200 | ATR% >= 4 | 591 | 91 % | **13.4** (11.3) | 28 (24) | 22 (20) | 47 (46) | +1.8 (+1.0) | +0.1 |
| 43 | `F2273` | – | K01.026 RSI(3) < 15 + atas MA200 | MACD > 0 + ATR% >= 4 | 655 | 92 % | **12.8** (10.7) | 26 (23) | 22 (20) | 46 (46) | +1.7 (+0.9) | +1.2 |
| 44 | `F2482` | – | K03.016 tutup < jalur bawah BB(15, 2.0) | RS >= 70 + ATR% >= 4 | 630 | 92 % | **13.8** (11.7) | 28 (24) | 24 (22) | 48 (47) | +1.9 (+1.2) | +1.9 |
| 45 | `F2100` | industri 20% teratas (pulangan 63 sesi) | K01.029 RSI(3) < 25 | MA50 > MA200 + ATR% >= 4 | 472 | 93 % | **12.8** (10.7) | 26 (23) | 22 (20) | 47 (45) | +1.7 (+0.6) | +0.9 |
| 46 | `F2763` | – | K01.079 RSI(10) < 25 | ADX > 25 + ATR% >= 4 | 706 | 91 % | **14.5** (12.4) | 29 (26) | 24 (24) | 49 (48) | +1.5 (+1.5) | +2.4 |
| 47 | `F2658` | – | K03.037 tutup < jalur bawah BB(30, 1.5) | RS >= 70 + ATR% >= 4 | 611 | 92 % | **14.1** (12.0) | 27 (24) | 23 (22) | 49 (47) | +2.5 (+1.3) | +3.3 |
| 48 | `F2331` | – | M20 EMA10/15 Crossover + Sudut (benih M, varian 1: c_kali_2=2.193, ema_a1_10=18, ema_a1_15=24, l_kali_0_99=0.587, tmax=22) | RS >= 90 + ATR% >= 4 | 425 | 94 % | **12.1** (10.0) | 25 (21) | 27 (21) | 45 (45) | +1.5 (+0.6) | +2.2 |
| 49 | `F2324` | – | K18.008 jatuh >= 5% dalam 3 hari | ADX > 25 + RS >= 90 | 536 | 95 % | **12.1** (10.0) | 26 (21) | 21 (18) | 45 (46) | +1.3 (+0.7) | +1.7 |
| 50 | `F2670` | – | K01.083 RSI(10) < 35 | RS >= 70 + ATR% >= 4 | 614 | 93 % | **14.0** (11.9) | 28 (24) | 24 (22) | 48 (47) | +2.3 (+1.2) | +2.2 |
| 51 | `F2417` | – | K21.004 NR5 + hari dalam | RS >= 90 + ATR% >= 4 | 551 | 98 % | **12.2** (10.2) | 26 (21) | 25 (20) | 45 (45) | +1.9 (+0.7) | +1.6 |
| 52 | `F2133` | – | K21.006 NR7 + hari dalam | RS >= 90 + ATR% >= 4 | 471 | 98 % | **12.1** (10.0) | 27 (21) | 24 (20) | 45 (45) | +1.9 (+0.7) | +0.1 |
| 53 | `F2105` | – | K18.017 jatuh >= 10% dalam 5 hari | MA50 naik (lawan 20 bar lalu) + RS >= 70 | 752 | 93 % | **12.8** (10.8) | 27 (23) | 22 (19) | 47 (46) | +1.6 (+0.6) | +2.1 |
| 54 | `F2374` | – | K17.005 undur ke sma10 yang naik (tol 1.0%) | RS >= 90 + ATR% >= 4 | 527 | 97 % | **11.8** (9.8) | 25 (21) | 25 (21) | 44 (45) | +1.2 (+0.6) | +1.0 |
| 55 | `F2247` | >= 60% saham industri di atas MA50 | K17.008 undur ke ema10 yang naik (tol 1.0%) + atas MA200 | RS >= 90 + ATR% >= 4 | 370 | 89 % | **11.7** (9.7) | 26 (20) | 25 (20) | 45 (45) | +1.5 (+0.7) | +1.2 |
| 56 | `F2176` | – | K01.047 RSI(4) < 30 | templat trend Minervini + RS >= 90 | 622 | 95 % | **10.2** (8.2) | 20 (17) | 16 (15) | 47 (46) | +1.0 (+0.5) | +4.2 |
| 57 | `F2597` | – | K01.001 RSI(2) < 3 | >= 30% di bawah puncak 52 minggu + volum hari isyarat >= 1.5x purata 50 | 615 | 95 % | **13.6** (11.6) | 28 (24) | 23 (21) | 48 (47) | +1.7 (+1.4) | +1.2 |
| 58 | `F2620` | sektor 3 teratas (pulangan 63 sesi) | K02.011 RSI(7) silang atas 35 | ATR% >= 4 | 713 | 94 % | **12.9** (10.9) | 25 (22) | 24 (21) | 46 (46) | +1.2 (+1.1) | +0.4 |
| 59 | `F2420` | – | N202 (benih N) | Supertrend naik + RS >= 90 | 656 | 96 % | **10.2** (8.2) | 20 (16) | 16 (15) | 47 (46) | +1.2 (+0.6) | +5.0 |
| 60 | `F2121` | sektor 3 teratas (pulangan 63 sesi) | K01.029 RSI(3) < 25 | ATR% >= 4 | 965 | 97 % | **13.0** (10.9) | 26 (22) | 22 (21) | 46 (46) | +1.4 (+1.0) | +1.7 |

## 8. Kaveat

- Kelebihan setup sepanjang tahun kecil berbanding setup "laporan kewangan" (senarai utama CS13: tangkap kira-kira dua kali rawak).
- 2025–26 ialah syarat lulus, bukan tempoh di luar sampel; bukti bersih hanya papertrade.
- Beribu calon disemak pada saham yang sama, jadi sebahagian lulus kerana nasib (anggaran di §3).
- "Minggu ada belian" pada lajur jadual §7 = semua saham (2010–2024); syarat kekerapan diukur pada separuh saham.
- Tiada saham delist dalam data (condong ke atas). Backtest sahaja; tiada papertrade tanpa keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.
