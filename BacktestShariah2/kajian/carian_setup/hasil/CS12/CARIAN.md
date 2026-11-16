# CS12: carian baharu ikut ukuran longgar — setup yang menangkap saham yang naik berterusan, walaupun perlahan (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_cari12.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (u). **Jangan sunting secara manual.**

## 1. Apa yang dicari

- **Ukuran longgar ("naik")**: selepas 4 minggu harga ≥ 2 % di atas harga beli (kira-kira 0.1 % sehari), masih di atas purata 20 harinya (trend naik), dan tidak pernah tutup 10 % di bawah harga beli.
- 1,169 isyarat beli (kaedah M, kaedah N, indikator dan variannya), setiap satu digabung dengan prasyarat pasaran, prasyarat syarikat dan penapis saham; 1,127 cukup isyarat untuk diskor. Skor dikira pada saham carian sahaja.
- **4,715 calon** berskor positif (sehingga 5 peraturan terbaik setiap isyarat beli; tiada had bilangan).
- Setup lengkap setiap calon: beli pada buka esok; stop loss 4xATR14; pegang sekurang-kurangnya hingga hari ke-20; selepas itu jual bila harga tutup di bawah purata 20 hari; paling lama 6 bulan.

## 2. Ujian (ditetapkan dahulu; pada saham yang carian tidak lihat)

- 100 calon teratas ikut skor: **10 % lulus** (perlu > 50 %); kawalan rawak (300 peraturan dipilih rambang daripada ruang yang sama): 10 % lulus (perlu beza ≥ 20 mata).
- Median kelebihan atas saham rawak hari sama: 100 teratas +4.2 mata (perlu ≥ +2); kawalan -0.2 mata.
- Semua calon: 1,368 daripada 4,715 lulus.
- **Keputusan: carian ikut ukuran longgar TIDAK berhasil.**

"Lulus" = belian ≥ 300, ≥ 10 tahun aktif, dan lebih baik daripada saham rawak hari sama dalam ketiga-tiga tempoh (2010–19, 2020–24, 2025–26).

## 3. Banding (nilai tengah setiap kumpulan; saham yang carian tidak lihat; jual hari ke-20)

| Kumpulan | Bilangan | Naik ≥ 5 % minggu 1 % | Ukuran ketat % (rawak) | Ukuran longgar % (rawak) | Naik ≥ 10 % selepas 4 minggu % | Menang % | Purata % |
|---|---|---|---|---|---|---|---|
| Kaedah M asal | 134 | 11 | 6 (6) | 38 (38) | 12 | 50 | +0.2 |
| Kaedah N asal | 49 | 12 | 6 (6) | 38 (38) | 13 | 51 | +0.3 |
| Setup F sedia ada | 69 | 27 | 14 (11) | 39 (39) | 25 | 54 | +2.1 |
| Calon baharu yang lulus | 1368 | 13 | 7 (6) | 41 (38) | 14 | 54 | +0.8 |
| 30 calon lulus teratas | 30 | 12 | 7 (5) | 44 (38) | 17 | 57 | +1.7 |
| Kawalan rawak | 300 | 12 | 6 (6) | 37 (37) | 12 | 50 | +0.1 |

## 4. Kekerapan belian pada senarai Shariah

- 30 calon lulus teratas digabung: 256 belian (saham-hari berbeza) setahun; ada belian dalam 97% bulan.
- Semua 1368 calon lulus digabung: 13511 setahun; ada belian dalam 100% bulan.

## 5. 50 calon lulus teratas (disusun ikut skor pada saham carian; angka pada saham yang carian tidak lihat)

Naik = ukuran longgar; kurungan = saham rawak pada hari yang sama. "Cara pegang B" = pegang hingga harga tutup di bawah purata 20 hari (selepas hari ke-20).

| ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun (senarai Shariah) | Naik % (rawak) | Naik ≥ 10 % / ≥ 20 % | Ketat % (rawak) | Jual hari ke-20: menang · purata | Cara pegang B: menang · purata · rugi ≥ 15 % · hari |
|---|---|---|---|---|---|---|---|---|---|
| `L0002` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, parameter asal) | MA50 > MA200 + MA50 naik (lawan 20 bar lalu) | 42 (25) | **48** (33) | 20 / 7 | 8 (5) | 60 % · +3.2 % | 57 % · +4.0 % · 4 % · 24 |
| `L0006` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, parameter asal) | MA20 > MA50 + MA50 > MA200 | 45 (26) | **47** (34) | 19 / 6 | 8 (5) | 60 % · +2.9 % | 56 % · +3.5 % · 4 % · 24 |
| `L0023` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 1: e_kali_1_1=0.745, rolling_20=23, rolling_250=197, sd250_ambang_20=17, sma20_ambang_10=14, sma20_ambang_5000000=4006468) | MA50 > MA200 + MA50 naik (lawan 20 bar lalu) | 39 (23) | **46** (32) | 17 / 6 | 6 (5) | 59 % · +2.2 % | 56 % · +3.2 % · 4 % · 25 |
| `L0061` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 1: e_kali_1_1=0.745, rolling_20=23, rolling_250=197, sd250_ambang_20=17, sma20_ambang_10=14, sma20_ambang_5000000=4006468) | MA20 > MA50 + MA50 > MA200 | 41 (25) | **46** (33) | 16 / 5 | 6 (5) | 60 % · +2.1 % | 55 % · +2.8 % · 4 % · 24 |
| `L0065` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 1: e_kali_1_1=0.745, rolling_20=23, rolling_250=197, sd250_ambang_20=17, sma20_ambang_10=14, sma20_ambang_5000000=4006468) | ADX > 25 + RS >= 70 | 28 (18) | **49** (33) | 21 / 7 | 8 (5) | 59 % · +2.6 % | 55 % · +3.2 % · 5 % · 25 |
| `L0071` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 2: e_kali_1_1=1.237, rolling_20=40, rolling_250=211, sd250_ambang_20=29, sma20_ambang_10=9, sma20_ambang_5000000=2560294) | MA50 > MA200 + MA50 naik (lawan 20 bar lalu) | 43 (23) | **45** (32) | 19 / 8 | 8 (5) | 56 % · +2.8 % | 54 % · +3.6 % · 7 % · 24 |
| `L0072` | nisbah 4% (10 hari) > 2 + >= 60% saham industri di atas MA50 | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 1: e_kali_1_1=0.745, rolling_20=23, rolling_250=197, sd250_ambang_20=17, sma20_ambang_10=14, sma20_ambang_5000000=4006468) | ADX > 25 + RS >= 70 | 34 (21) | **46** (34) | 18 / 6 | 8 (5) | 58 % · +2.0 % | 54 % · +2.7 % · 5 % · 25 |
| `L0073` | nisbah 4% (10 hari) > 2 + >= 60% saham industri di atas MA50 | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 1: e_kali_1_1=0.745, rolling_20=23, rolling_250=197, sd250_ambang_20=17, sma20_ambang_10=14, sma20_ambang_5000000=4006468) | MA50 > MA200 + RS >= 70 | 47 (28) | **44** (33) | 17 / 5 | 6 (4) | 57 % · +1.9 % | 54 % · +2.6 % · 5 % · 24 |
| `L0077` | nisbah 4% (10 hari) > 2 | M82 Arthur Hill Rotasi Sasaran 10% (benih M, parameter asal) | MA20 > MA50 + MA50 > MA200 | 67 (39) | **44** (34) | 17 / 5 | 7 (5) | 57 % · +2.2 % | 54 % · +2.9 % · 4 % · 23 |
| `L0096` | nisbah 4% (10 hari) > 2 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 2: e_kali_1_1=1.237, rolling_20=40, rolling_250=211, sd250_ambang_20=29, sma20_ambang_10=9, sma20_ambang_5000000=2560294) | MA20 > MA50 + MA50 > MA200 | 47 (25) | **45** (33) | 19 / 8 | 8 (5) | 56 % · +2.6 % | 53 % · +3.2 % · 7 % · 23 |
| `L0101` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | ADX < 20 + Supertrend naik | 35 (26) | **43** (40) | 18 / 5 | 7 (6) | 58 % · +1.8 % | 51 % · +1.6 % · 4 % · 23 |
| `L0139` | nisbah 4% (10 hari) > 2 + tiada earnings dalam 20 sesi akan datang | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 2: e_kali_1_1=1.237, rolling_20=40, rolling_250=211, sd250_ambang_20=29, sma20_ambang_10=9, sma20_ambang_5000000=2560294) | MA50 > MA200 + MA50 naik (lawan 20 bar lalu) | 42 (23) | **44** (33) | 17 / 6 | 6 (5) | 54 % · +2.3 % | 52 % · +3.3 % · 5 % · 24 |
| `L0146` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 1: rolling_50=56, shift_2=4) | MA50 naik (lawan 20 bar lalu) + ADX < 20 | 30 (23) | **43** (38) | 17 / 3 | 8 (5) | 56 % · +1.5 % | 53 % · +1.7 % · 4 % · 22 |
| `L0159` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 1: rolling_50=56, shift_2=4) | tutup > MA200 + ADX < 20 | 33 (24) | **42** (38) | 17 / 3 | 7 (5) | 56 % · +1.6 % | 52 % · +1.7 % · 3 % · 22 |
| `L0171` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N47 NR7 + EMA9>EMA21 (benih N) | RSI14 > 50 + ADX < 20 | 32 (24) | **42** (39) | 20 / 6 | 7 (6) | 54 % · +1.7 % | 51 % · +2.0 % · 5 % · 22 |
| `L0183` | Januari + sektor 3 terbawah (pulangan 63 sesi) | K07.016 tutup silang atas ema100 | tutup > MA50 + ADX < 20 | 30 (21) | **53** (46) | 19 / 5 | 9 (9) | 63 % · +2.7 % | 57 % · +2.4 % · 4 % · 24 |
| `L0199` | QQQ RSI14 < 35 + >= 60% saham sektor di atas MA50 | K06.005 4 tutup menurun berturut | MA50 > MA200 | 27 (17) | **55** (43) | 19 / 4 | 15 (11) | 71 % · +3.7 % | 65 % · +4.0 % · 2 % · 25 |
| `L0201` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N47 NR7 + EMA9>EMA21 (benih N) | ADX < 20 | 32 (24) | **42** (39) | 20 / 6 | 7 (6) | 54 % · +1.7 % | 51 % · +2.0 % · 5 % · 22 |
| `L0202` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 3: rolling_50=70, shift_2=4) | MA50 naik (lawan 20 bar lalu) + ADX < 20 | 33 (24) | **41** (38) | 16 / 3 | 7 (5) | 54 % · +1.0 % | 51 % · +1.3 % · 5 % · 22 |
| `L0205` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 3: rolling_50=70, shift_2=4) | tutup > MA200 + ADX < 20 | 34 (24) | **41** (38) | 17 / 3 | 7 (5) | 55 % · +1.3 % | 51 % · +1.5 % · 3 % · 22 |
| `L0211` | distribution day QQQ >= 5 dalam 25 sesi + harga melompat >= 5% pada hari earnings (20 sesi lalu) | M10 EMA3 + CCI + MACD (benih M, parameter asal) | ADX < 20 + dalam 15% dari puncak 52 minggu | 30 (24) | **44** (39) | 14 / 3 | 8 (8) | 56 % · +1.0 % | 52 % · +2.0 % · 6 % · 23 |
| `L0222` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 1: rolling_50=56, shift_2=4) | MA20 > MA50 + ADX < 20 | 38 (28) | **43** (39) | 16 / 3 | 7 (5) | 58 % · +1.5 % | 51 % · +1.3 % · 4 % · 22 |
| `L0227` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 1: rolling_50=56, shift_2=4) | ADX < 20 | 47 (34) | **43** (39) | 17 / 4 | 8 (6) | 57 % · +1.5 % | 51 % · +1.4 % · 4 % · 22 |
| `L0239` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 3: rolling_50=70, shift_2=4) | MA20 > MA50 + ADX < 20 | 37 (27) | **43** (39) | 16 / 3 | 7 (5) | 58 % · +1.5 % | 51 % · +1.3 % · 4 % · 22 |
| `L0240` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N47 NR7 + EMA9>EMA21 (benih N) | tutup > MA20 + ADX < 20 | 31 (23) | **42** (39) | 21 / 6 | 7 (6) | 54 % · +1.8 % | 51 % · +2.1 % · 5 % · 22 |
| `L0244` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 3: rolling_50=70, shift_2=4) | ADX < 20 | 45 (33) | **42** (39) | 17 / 4 | 8 (6) | 55 % · +1.4 % | 50 % · +1.3 % · 4 % · 22 |
| `L0247` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N47 NR7 + EMA9>EMA21 (benih N) | MACD > 0 + ADX < 20 | 31 (22) | **41** (39) | 19 / 5 | 7 (6) | 53 % · +1.4 % | 50 % · +1.8 % · 5 % · 22 |
| `L0252` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 1: rolling_50=56, shift_2=4) | ADX < 20 + Supertrend naik | 38 (28) | **43** (40) | 16 / 3 | 7 (6) | 58 % · +1.5 % | 53 % · +1.6 % · 4 % · 22 |
| `L0256` | <= 30% saham di atas MA50 + industri 20% teratas (pulangan 21 sesi) | K17.031 undur ke ema50 yang naik (tol 1.0%) | tutup > MA20 + ATR% <= 2.5 | 26 (11) | **53** (50) | 11 / 1 | 5 (6) | 61 % · +1.3 % | 62 % · +2.1 % · 0 % · 26 |
| `L0264` | turun-naik SPY 21 hari <= 10% setahun + hasil suku terkini tumbuh >= 20% | K03.004 tutup < jalur bawah BB(10, 2.0) | RSI14 > 50 + dalam 15% dari puncak 52 minggu | 26 (22) | **38** (35) | 12 / 3 | 5 (5) | 48 % · -0.2 % | 44 % · +0.1 % · 3 % · 21 |
| `L0271` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | RSI14 > 50 + ADX < 20 | 47 (33) | **42** (40) | 19 / 6 | 8 (6) | 57 % · +2.0 % | 51 % · +1.9 % · 4 % · 23 |
| `L0272` | 7 hari pertama bulan + harga melompat >= 5% pada hari earnings (20 sesi lalu) | M46 Jurang Naik Boleh Beli (Buyable Gap Up) (benih M, varian 2: a40_kali_0_75=0.796, atr_40=69, rolling_200=361, rolling_50=53, shift_31=37, vol50_kali_1_5=1.289) | MA50 > MA200 + MACD > 0 | 26 (21) | **39** (37) | 12 / 5 | 10 (8) | 55 % · +1.3 % | 49 % · +1.4 % · 4 % · 22 |
| `L0273` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N47 NR7 + EMA9>EMA21 (benih N) | tutup > MA50 + ADX < 20 | 30 (22) | **42** (39) | 20 / 5 | 7 (6) | 54 % · +1.6 % | 51 % · +1.8 % · 5 % · 22 |
| `L0277` | distribution day QQQ >= 5 dalam 25 sesi + harga melompat >= 5% pada hari earnings (20 sesi lalu) | M123 CCI Correction (Lambert, ChartSchool) (benih M, varian 2: cci_20=19, had_henti=0.939, henti_low=1, keluar_sma=82) | MACD > 0 + RS >= 70 | 26 (19) | **40** (37) | 17 / 4 | 9 (9) | 51 % · +0.7 % | 47 % · +0.7 % · 10 % · 22 |
| `L0278` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, parameter asal) | MA50 naik (lawan 20 bar lalu) + ADX < 20 | 31 (22) | **42** (37) | 15 / 2 | 8 (5) | 57 % · +1.2 % | 51 % · +1.2 % · 4 % · 22 |
| `L0279` | QQQ RSI14 < 35 + >= 60% saham sektor di atas MA50 | K06.005 4 tutup menurun berturut | – | 35 (20) | **53** (43) | 17 / 4 | 12 (10) | 69 % · +3.3 % | 64 % · +3.3 % · 2 % · 24 |
| `L0281` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K21.007 NR10 | RSI14 > 50 + ADX < 20 | 30 (21) | **42** (39) | 20 / 5 | 7 (6) | 55 % · +1.8 % | 51 % · +2.3 % · 5 % · 23 |
| `L0297` | Januari + industri 20% terbawah (pulangan 63 sesi) | K24.001 bar pembalikan (buka <= 10%, tutup >= 70% julat) | RSI14 > 50 + ATR% <= 2.5 | 45 (22) | **48** (41) | 7 / 1 | 3 (3) | 61 % · +1.1 % | 55 % · +1.5 % · 0 % · 24 |
| `L0308` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K21.007 NR10 | ADX < 20 | 43 (30) | **42** (38) | 21 / 7 | 8 (6) | 54 % · +2.1 % | 51 % · +2.6 % · 6 % · 22 |
| `L0311` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 3: rolling_50=70, shift_2=4) | ADX < 20 + Supertrend naik | 36 (26) | **43** (39) | 17 / 4 | 8 (6) | 57 % · +1.6 % | 52 % · +1.6 % · 4 % · 22 |
| `L0315` | QQQ RSI14 < 35 + >= 60% saham sektor di atas MA50 | K06.005 4 tutup menurun berturut | MA50 > MA200 + dalam 15% dari puncak 52 minggu | 20 (13) | **58** (44) | 16 / 3 | 15 (10) | 72 % · +3.6 % | 66 % · +3.7 % · 0 % · 25 |
| `L0320` | QQQ RSI14 < 35 + 5-19 sesi selepas earnings | K03.013 tutup < jalur bawah BB(15, 1.5) | dalam 15% dari puncak 52 minggu + volum 10 hari > volum 50 hari | 51 (29) | **47** (41) | 10 / 1 | 9 (8) | 59 % · +0.6 % | 54 % · +0.4 % · 3 % · 23 |
| `L0322` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K21.005 NR7 | RSI14 > 50 + ADX < 20 | 36 (26) | **42** (38) | 20 / 6 | 7 (6) | 55 % · +1.8 % | 50 % · +2.1 % · 5 % · 22 |
| `L0324` | follow-through day aktif (QQQ, 20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | K03.001 tutup < jalur bawah BB(10, 1.5) | tutup > MA200 + ADX > 25 | 34 (21) | **38** (35) | 15 / 5 | 7 (6) | 49 % · +0.2 % | 49 % · +0.8 % · 7 % · 22 |
| `L0326` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K21.005 NR7 | tutup > MA50 + MA50 > MA200 | 70 (50) | **40** (37) | 15 / 4 | 5 (5) | 51 % · +1.2 % | 48 % · +1.4 % · 3 % · 22 |
| `L0332` | Januari + industri 20% terbawah (pulangan 63 sesi) | K05.006 tutup silang atas jalur atas BB(20, 2.0) | MACD > 0 + ATR% <= 2.5 | 29 (14) | **47** (40) | 6 / 1 | 1 (3) | 60 % · +0.8 % | 54 % · +1.0 % · 0 % · 24 |
| `L0333` | Januari + industri 20% terbawah (pulangan 63 sesi) | N22 BB pecah atas + RSI (benih N) | MACD > 0 + ATR% <= 2.5 | 29 (14) | **47** (40) | 6 / 1 | 1 (3) | 60 % · +0.8 % | 54 % · +1.0 % · 0 % · 24 |
| `L0334` | Januari + industri 20% terbawah (pulangan 63 sesi) | P18 pecah atas jalur atas Bollinger | MACD > 0 + ATR% <= 2.5 | 29 (14) | **47** (40) | 6 / 1 | 1 (3) | 60 % · +0.8 % | 54 % · +1.0 % · 0 % · 24 |
| `L0337` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K17.010 undur ke sma10 yang naik (tol 2.0%) + atas MA200 | MA20 > MA50 + ATR% <= 2.5 | 42 (28) | **42** (40) | 10 / 0 | 3 (3) | 54 % · +0.7 % | 49 % · +0.7 % · 0 % · 22 |
| `L0339` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K17.010 undur ke sma10 yang naik (tol 2.0%) + atas MA200 | MA50 naik (lawan 20 bar lalu) + ATR% <= 2.5 | 40 (26) | **41** (39) | 10 / 0 | 3 (3) | 54 % · +0.6 % | 48 % · +0.6 % · 0 % · 22 |

Senarai penuh 4,715 calon (lulus dan tidak): `hasil/CS12/calon.csv.gz`; kawalan rawak: `kawalan.csv`.

## 6. Mengapa ujian gagal: tahun yang carian tidak lihat (analisis SELEPAS hasil; bukan ditetapkan dahulu)

Saham yang tidak dilihat berkongsi TAHUN yang sama dengan saham carian bagi 2010–2024; hanya 2025–26 yang benar-benar tidak dilihat dari segi masa. Peraturan dengan belian ≥ 300 dan ≥ 10 tahun aktif:

| Kumpulan | Bilangan | Lebih baik daripada rawak: 2010–19 | 2020–24 | **2025–26** | Median kelebihan 2010–19 / 2020–24 / 2025–26 (mata) |
|---|---|---|---|---|---|
| Calon carian | 4,164 | 81% | 87% | **45%** | +2.6 / +3.3 / -0.6 |
| Kawalan rawak | 280 | 50% | 46% | **42%** | +0.0 / -0.3 / -0.7 |
| Calon tanpa prasyarat pasaran | 27 | 37% | 52% | **33%** | -0.5 / +0.6 / -1.8 |
| Setup F sedia ada, ukuran KETAT | 62 | 90% | 85% | **79%** | +2.4 / +1.7 / +1.8 |

- 4,679 daripada 4,715 calon memakai prasyarat pasaran: kelebihan ukuran longgar pada 2010–2024 hampir semuanya datang daripada BILA membeli (keadaan pasaran dan kalendar), dan ia tidak berulang pada 2025–26.
- Prasyarat pasaran paling kerap antara calon, dengan median kelebihan 2025–26: 7 hari pertama bulan (665 calon, -1.1); Januari (464 calon, +0.4); Mei-Okt (380 calon, -0.4); turun-naik SPY 21 hari <= 10% setahun (336 calon, +0.7); QQQ OFF (190 calon, -2.1); distribution day QQQ <= 2 dalam 25 sesi (185 calon, +6.2); <= 30% saham di atas MA50 (171 calon, -23.7); >= 60% saham di atas MA200 (163 calon, -1.1).

## 7. Kaveat

- Beratus-ratus calon disemak pada saham yang tidak dilihat, jadi sebahagian lulus kerana nasib: bandingkan dengan kadar lulus kawalan rawak.
- "Lebih baik daripada rawak hari sama" mengukur PILIHAN saham; angka naik mentah turut mengandungi kesan BILA membeli (keadaan pasaran).
- Saham yang tidak dilihat sudah digunakan dalam pusingan terdahulu; tiada saham delist (lebih penting bagi pegangan hingga 6 bulan). Belum didaftarkan sebagai kod F: itu keputusan pengguna. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.
