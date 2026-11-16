# CS11: semak semula setup F dengan ukuran longgar ("naik perlahan pun kira"), pegang selepas 4 minggu, kekerapan, dan banding M / N / F (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_semak11.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (t). **Jangan sunting secara manual.**

## 1. Dua ukuran

- **Ketat (`terus`)**: naik ≥ 5 % dalam minggu pertama DAN naik lagi hingga minggu ke-4.
- **Longgar (`naik`)**: selepas 4 minggu harga ≥ 2 % di atas harga beli (kira-kira 0.1 % sehari), masih di atas purata 20 harinya (trend naik), dan tidak pernah tutup 10 % di bawah harga beli.
- Saham rawak pada mana-mana hari (saham yang carian tidak lihat): ketat 6.3 %, longgar 38.6 % (naik ≥ 10 %: 13.6 %; naik ≥ 20 %: 3.6 %).

## 2. Banding kaedah M asal, N asal dan setup F (ukuran sama, cara pegang sama; median setiap kumpulan)

| Kumpulan | Bilangan | Beli setahun | Naik ≥ 5 % minggu 1 % | Ketat % (rawak) | Longgar % (rawak) | Naik ≥ 10 % selepas 4 minggu % | Menang % | Purata % | Lulus ukuran longgar |
|---|---|---|---|---|---|---|---|---|---|
| M asal | 134 | 1042 | 11 | 6 (6) | 38 (38) | 12 | 50 | +0.2 | 10 daripada 134 |
| N asal | 49 | 2898 | 12 | 6 (6) | 38 (38) | 13 | 51 | +0.3 | 3 daripada 49 |
| F | 69 | 54 | 27 | 14 (11) | 39 (39) | 25 | 54 | +2.1 | 4 daripada 69 |
| F yang menepati semua | 4 | 37 | 20 | 12 (9) | 47 (44) | 20 | 60 | +2.1 | 4 daripada 4 |

"Lulus ukuran longgar" = belian ≥ 300, ≥ 10 tahun aktif dan lebih baik daripada saham rawak hari sama dalam ketiga-tiga tempoh (2010–19, 2020–24, 2025–26). Kaedah M dan N asal dipegang dengan cara yang sama (20 hari, stop loss 4xATR14) supaya adil; dalam papertrade sebenar kaedah M menjual 11 % dagangan pada hari beli (`hasil/PEGANG_MIN.md`), setup F tiada.

## 3. Pegang selepas 4 minggu (semua isyarat dengan data 6 bulan lengkap; berpasangan)

Cara terpilih pada saham carian: **P-126** (pegang 6 bulan (stop loss sahaja)).

| Cara pegang | Saham carian: tambahan purata lawan jual hari ke-20 (mata) | Saham tidak dilihat: purata % | Menang % | Rugi ≥ 15 % % | Median hari pegang | Untung pada saham yang naik % |
|---|---|---|---|---|---|---|
| J20: jual pada hari ke-20 (cara sekarang) | +0.00 | +2.1 | 54 | 13 | 20 | +16.7 |
| P-MA20: pegang hingga tutup di bawah purata 20 hari | +0.20 | +2.7 | 51 | 14 | 22 | +17.7 |
| P-MA20x2: pegang hingga dua tutup berturut di bawah purata 20 hari | +0.47 | +2.8 | 49 | 14 | 23 | +17.8 |
| P-MA50: pegang hingga tutup di bawah purata 50 hari | +0.86 | +3.1 | 43 | 14 | 25 | +18.6 |
| P-R10: pegang hingga tutup di bawah paras terendah 10 hari | +0.89 | +3.0 | 47 | 17 | 30 | +18.1 |
| P-CH4: pegang hingga jatuh 4xATR14 dari tutup tertinggi | +2.70 | +4.2 | 41 | 20 | 42 | +20.0 |
| P-126: pegang 6 bulan (stop loss sahaja) | +5.23 | +6.7 | 44 | 34 | 126 | +24.0 |

- Ujian (ditetapkan dahulu): purata untung cara terpilih lebih tinggi daripada jual hari ke-20 bagi **64 daripada 69** setup (perlu lebih separuh); beza kadar menang -9.8 mata (perlu ≥ −2); beza rugi ≥ 15 % +21.7 mata (perlu ≤ +2).
- **Keputusan: pegang selepas 4 minggu TIDAK menolong.**

## 4. Kekerapan belian pada senarai Shariah

- Saham Shariah dalam data: 839 (senarai semasa).
- 4 setup F yang menepati semua, digabung: **145 belian setahun** (121 saham-hari berbeza; ada belian dalam 70% bulan). Tafsiran "beberapa kali sebulan" = ≥ 24 setahun: **LULUS**.
- Setiap setup sendirian: 2 daripada 4 membeli ≥ 24 kali setahun pada senarai Shariah.

## 5. Setiap setup F (saham yang carian tidak lihat; jual hari ke-20 + stop loss sendiri)

| ID | Prasyarat | Stop loss | Beli setahun (senarai Shariah) | Ketat % (rawak) | Longgar % (rawak) | Naik ≥ 10 % / ≥ 20 % selepas 4 minggu | Menang · purata | Menepati semua? | Kekurangan |
|---|---|---|---|---|---|---|---|---|---|
| `F13` | QQQ OFF | 4xATR14 | 33 (23) | 7 (9) | **48** (44) | 15 / 4 | 60 % · +1.6 % | **Ya** | – |
| `F19` | QQQ OFF | 4xATR14 | 41 (30) | 7 (9) | **48** (43) | 15 / 4 | 60 % · +1.4 % | **Ya** | – |
| `F88` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | 5xATR14 | 28 (17) | 16 (10) | **46** (45) | 25 / 8 | 59 % · +2.6 % | **Ya** | – |
| `F56` | QQQ >= 10% di bawah puncak | 4xATR14 | 117 (74) | 19 (17) | **43** (43) | 32 / 16 | 60 % · +4.9 % | **Ya** | – |
| `F43` | Januari + tiada earnings dalam 20 sesi akan datang | 4xATR14 | 31 (17) | 25 (20) | **57** (54) | 36 / 13 | 70 % · +5.8 % | Belum | tidak lulus ukuran longgar |
| `F57` | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | 3xATR14 | 33 (24) | 21 (21) | **54** (53) | 39 / 18 | 68 % · +6.7 % | Belum | tidak lulus ukuran longgar |
| `F53` | Januari + tiada earnings dalam 20 sesi akan datang | 3xATR14 | 20 (11) | 21 (17) | **53** (50) | 34 / 12 | 65 % · +4.9 % | Belum | tidak lulus ukuran longgar |
| `F64` | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | 3xATR14 | 44 (29) | 23 (21) | **53** (52) | 40 / 23 | 69 % · +9.1 % | Belum | tidak lulus ukuran longgar |
| `F52` | Januari + tiada earnings dalam 20 sesi akan datang | 4xATR14 | 42 (21) | 24 (21) | **52** (49) | 36 / 15 | 64 % · +5.4 % | Belum | tidak lulus ukuran longgar |
| `F55` | turun-naik SPY 21 hari >= 25% setahun + sektor 3 terbawah (pulangan 63 sesi) | 4xATR14 | 29 (21) | 20 (21) | **52** (52) | 37 / 15 | 74 % · +7.9 % | Belum | tidak lulus ukuran longgar |
| `F67` | turun-naik SPY 21 hari >= 25% setahun + kejutan untung terkini positif (SUE > 0) | -10% | 39 (25) | 22 (22) | **52** (52) | 40 / 20 | 56 % · +5.4 % | Belum | tidak lulus ukuran longgar |
| `F62` | QQQ >= 20% di bawah puncak | 3xATR14 | 83 (50) | 26 (24) | **49** (48) | 40 / 24 | 71 % · +10.3 % | Belum | tidak lulus ukuran longgar |
| `F65` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | 3xATR14 | 26 (18) | 22 (16) | **49** (48) | 30 / 8 | 63 % · +3.0 % | Belum | tidak lulus ukuran longgar |
| `F54` | breadth thrust Zweig aktif (20 sesi) + sektor 3 terbawah (pulangan 63 sesi) | 4xATR14 | 33 (28) | 19 (17) | **48** (48) | 34 / 16 | 63 % · +5.5 % | Belum | tidak lulus ukuran longgar |
| `F92` | QQQ naik >= 3% dalam 5 sesi + earnings dalam 1-5 sesi akan datang | 5xATR14 | 23 (14) | 16 (10) | **47** (46) | 25 / 7 | 59 % · +2.5 % | Belum | tidak lulus ukuran longgar |
| `F20` | QQQ OFF | 4xATR14 | 69 (47) | 7 (9) | **46** (46) | 18 / 4 | 59 % · +1.7 % | Belum | tidak lulus ukuran longgar |
| `F66` | <= 30% saham di atas MA50 + kejutan untung terkini positif (SUE > 0) | 3xATR14 | 44 (28) | 14 (15) | **46** (45) | 34 / 18 | 66 % · +6.1 % | Belum | tidak lulus ukuran longgar |
| `F68` | breadth thrust Zweig aktif (20 sesi) | 3xATR14 | 38 (26) | 19 (18) | **45** (48) | 33 / 22 | 57 % · +5.4 % | Belum | tidak lulus ukuran longgar |
| `F51` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | 4xATR14 | 44 (26) | 21 (16) | **44** (46) | 27 / 13 | 64 % · +4.9 % | Belum | tidak lulus ukuran longgar |
| `F49` | QQQ >= 10% di bawah puncak + earnings dalam 1-5 sesi akan datang | 4xATR14 | 64 (38) | 22 (20) | **44** (46) | 32 / 17 | 64 % · +5.1 % | Belum | tidak lulus ukuran longgar |
| `F69` | turun-naik SPY 21 hari >= 25% setahun | 3xATR14 | 97 (59) | 15 (16) | **44** (44) | 32 / 17 | 62 % · +5.3 % | Belum | tidak lulus ukuran longgar |
| `F46` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | 3xATR14 | 17 (10) | 11 (9) | **44** (38) | 19 / 7 | 57 % · +1.4 % | Belum | belian < 300 |
| `F02` | QQQ OFF | 4xATR14 | 122 (76) | 12 (11) | **43** (43) | 27 / 10 | 56 % · +2.2 % | Belum | tidak lulus ukuran longgar |
| `F63` | QQQ OFF + earnings dalam 1-5 sesi akan datang | 4xATR14 | 26 (15) | 22 (16) | **43** (45) | 30 / 17 | 61 % · +4.5 % | Belum | tidak lulus ukuran longgar |
| `F17` | QQQ OFF | 4xATR14 | 449 (284) | 12 (12) | **41** (41) | 25 / 10 | 57 % · +2.4 % | Belum | tidak lulus ukuran longgar |
| `F11` | QQQ OFF | 4xATR14 | 616 (387) | 14 (13) | **41** (41) | 26 / 11 | 56 % · +2.5 % | Belum | tidak lulus ukuran longgar |
| `F15` | QQQ OFF | 4xATR14 | 348 (213) | 14 (14) | **41** (41) | 26 / 11 | 57 % · +2.9 % | Belum | tidak lulus ukuran longgar |
| `F12` | QQQ OFF | 4xATR14 | 191 (118) | 13 (13) | **41** (41) | 28 / 12 | 58 % · +3.4 % | Belum | tidak lulus ukuran longgar |
| `F14` | QQQ OFF | 4xATR14 | 393 (240) | 13 (12) | **40** (41) | 26 / 11 | 56 % · +2.4 % | Belum | tidak lulus ukuran longgar |
| `F50` | SPY bawah SMA200 + earnings dalam 1-5 sesi akan datang | 4xATR14 | 42 (26) | 21 (18) | **40** (43) | 30 / 15 | 58 % · +4.0 % | Belum | tidak lulus ukuran longgar |
| `F47` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | 3xATR14 | 24 (15) | 9 (9) | **40** (40) | 19 / 6 | 53 % · +0.7 % | Belum | tidak lulus ukuran longgar |
| `F18` | QQQ OFF | 4xATR14 | 682 (414) | 13 (12) | **40** (41) | 25 / 11 | 54 % · +1.8 % | Belum | tidak lulus ukuran longgar |
| `F28` | QQQ OFF | 4xATR14 | 164 (97) | 11 (11) | **39** (40) | 25 / 10 | 52 % · +1.3 % | Belum | tidak lulus ukuran longgar |
| `F93` | keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang | 3xATR14 | 22 (13) | 13 (7) | **39** (38) | 16 / 6 | 49 % · +1.0 % | Belum | tidak lulus ukuran longgar |
| `F45` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | 4xATR14 | 47 (26) | 15 (12) | **39** (37) | 27 / 13 | 54 % · +3.4 % | Belum | tidak lulus ukuran longgar |
| `F07` | QQQ OFF | 4xATR14 | 62 (35) | 14 (13) | **39** (40) | 26 / 12 | 53 % · +2.2 % | Belum | tidak lulus ukuran longgar |
| `F27` | tiada | 4xATR14 | 292 (184) | 14 (12) | **39** (37) | 26 / 12 | 53 % · +1.9 % | Belum | tidak lulus ukuran longgar |
| `F42` | distribution day QQQ <= 2 dalam 25 sesi + >= 60% saham industri di atas MA50 | 3xATR14 | 18 (10) | 13 (8) | **38** (39) | 25 / 15 | 53 % · +3.5 % | Belum | tidak lulus ukuran longgar |
| `F59` | distribution day QQQ <= 2 dalam 25 sesi | -10% | 19 (11) | 14 (9) | **38** (39) | 28 / 11 | 44 % · +1.7 % | Belum | tidak lulus ukuran longgar |
| `F16` | tiada | 4xATR14 | 268 (147) | 13 (11) | **38** (39) | 27 / 13 | 53 % · +2.1 % | Belum | tidak lulus ukuran longgar |
| `F04` | QQQ OFF | 4xATR14 | 165 (95) | 11 (12) | **37** (41) | 22 / 10 | 55 % · +2.5 % | Belum | tidak lulus ukuran longgar |
| `F06` | tiada | 4xATR14 | 312 (200) | 12 (11) | **37** (37) | 24 / 11 | 52 % · +1.8 % | Belum | tidak lulus ukuran longgar |
| `F01` | tiada | 4xATR14 | 118 (75) | 12 (11) | **37** (38) | 25 / 12 | 53 % · +2.6 % | Belum | tidak lulus ukuran longgar |
| `F91` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | 5xATR14 | 22 (11) | 18 (10) | **37** (37) | 25 / 13 | 54 % · +2.8 % | Belum | tidak lulus ukuran longgar |
| `F48` | >= 60% saham di atas MA50 + >= 60% saham sektor di atas MA50 | 3xATR14 | 70 (46) | 12 (9) | **37** (35) | 24 / 12 | 48 % · +1.1 % | Belum | tidak lulus ukuran longgar |
| `F05` | tiada | 4xATR14 | 333 (201) | 11 (11) | **37** (38) | 24 / 11 | 52 % · +1.6 % | Belum | tidak lulus ukuran longgar |
| `F61` | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | 3xATR14 | 87 (57) | 11 (9) | **37** (36) | 23 / 10 | 48 % · +0.7 % | Belum | tidak lulus ukuran longgar |
| `F60` | SPY atas SMA200 + >= 60% saham sektor di atas MA50 | 3xATR14 | 190 (102) | 12 (9) | **36** (35) | 24 / 12 | 49 % · +1.3 % | Belum | tidak lulus ukuran longgar |
| `F89` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | 5xATR14 | 23 (11) | 17 (10) | **36** (37) | 24 / 11 | 54 % · +2.0 % | Belum | tidak lulus ukuran longgar |
| `F08` | tiada | 4xATR14 | 299 (180) | 11 (10) | **36** (37) | 24 / 11 | 51 % · +1.4 % | Belum | tidak lulus ukuran longgar |
| `F10` | tiada | 3xATR14 | 141 (89) | 13 (10) | **36** (35) | 22 / 10 | 50 % · +1.0 % | Belum | tidak lulus ukuran longgar |
| `F30` | tiada | 4xATR14 | 645 (382) | 11 (10) | **36** (37) | 23 / 10 | 51 % · +1.1 % | Belum | tidak lulus ukuran longgar |
| `F44` | turun-naik SPY menurun (21 hari < 63 hari) + kejutan untung terkini positif (SUE > 0) | 3xATR14 | 37 (23) | 12 (10) | **36** (37) | 23 / 10 | 48 % · +1.1 % | Belum | tidak lulus ukuran longgar |
| `F09` | tiada | 4xATR14 | 177 (103) | 11 (11) | **36** (37) | 23 / 10 | 50 % · +0.9 % | Belum | tidak lulus ukuran longgar |
| `F40` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | 3xATR14 | 36 (21) | 18 (11) | **35** (38) | 24 / 11 | 51 % · +2.1 % | Belum | tidak lulus ukuran longgar |
| `F03` | tiada | 4xATR14 | 75 (39) | 14 (14) | **35** (39) | 27 / 16 | 54 % · +3.0 % | Belum | tidak lulus ukuran longgar |
| `F24` | tiada | 4xATR14 | 145 (87) | 13 (10) | **35** (36) | 24 / 11 | 50 % · +0.9 % | Belum | tidak lulus ukuran longgar |
| `F95` | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | 5xATR14 | 20 (12) | 14 (8) | **34** (34) | 20 / 11 | 52 % · +1.7 % | Belum | tidak lulus ukuran longgar |
| `F29` | tiada | -10% | 268 (156) | 12 (10) | **34** (36) | 23 / 11 | 38 % · +0.2 % | Belum | tidak lulus ukuran longgar |
| `F21` | tiada | -10% | 54 (26) | 10 (10) | **34** (37) | 21 / 9 | 39 % · -0.4 % | Belum | tidak lulus ukuran longgar |
| `F26` | tiada | 4xATR14 | 204 (120) | 11 (10) | **34** (35) | 23 / 11 | 49 % · +0.9 % | Belum | tidak lulus ukuran longgar |
| `F25` | tiada | 4xATR14 | 192 (112) | 12 (10) | **33** (35) | 22 / 11 | 47 % · +0.2 % | Belum | tidak lulus ukuran longgar |
| `F41` | QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang | 3xATR14 | 56 (27) | 15 (10) | **33** (35) | 24 / 13 | 46 % · +0.4 % | Belum | tidak lulus ukuran longgar |
| `F39` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | 3xATR14 | 30 (17) | 18 (11) | **33** (39) | 23 / 11 | 52 % · +1.8 % | Belum | tidak lulus ukuran longgar |
| `F22` | QQQ ON | -10% | 157 (89) | 13 (10) | **33** (34) | 23 / 12 | 37 % · +0.3 % | Belum | tidak lulus ukuran longgar |
| `F58` | >= 60% saham di atas MA50 + earnings dalam 1-5 sesi akan datang | 3xATR14 | 23 (13) | 16 (8) | **32** (34) | 24 / 12 | 45 % · +0.4 % | Belum | tidak lulus ukuran longgar |
| `F94` | QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang | 5xATR14 | 23 (15) | 10 (7) | **31** (35) | 17 / 6 | 44 % · -0.4 % | Belum | tidak lulus ukuran longgar |
| `F23` | SPY > SMA200 | -10% | 39 (14) | 13 (10) | **30** (36) | 22 / 13 | 35 % · -0.0 % | Belum | tidak lulus ukuran longgar |
| `F90` | rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang | 5xATR14 | 18 (11) | 17 (10) | **28** (36) | 19 / 9 | 48 % · +0.6 % | Belum | tidak lulus ukuran longgar |

## 6. Kaveat

- Setup F dipilih dahulu ikut ukuran ketat; ini penilaian semula, bukan carian baharu ikut ukuran longgar.
- Saham yang carian tidak lihat sudah digunakan dalam pusingan terdahulu; tiada saham delist; backtest sahaja. Kad skor kekal satu-satunya keputusan wang sebenar.
