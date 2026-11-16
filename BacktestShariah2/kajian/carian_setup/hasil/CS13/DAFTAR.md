# CS13: semua setup "naik laju" yang lulus didaftarkan sebagai kod F (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_daftar13.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (v). **Jangan sunting secara manual.**

## 1. Apa yang dibuat

- **Ukuran ketat ("naik laju")**: saham naik ≥ 5 % pada minggu pertama, naik lagi hingga minggu ke-4, dan tidak menyentuh −8 %.
- 1,169 isyarat beli (kaedah M, kaedah N, indikator dan variannya) × prasyarat pasaran × prasyarat syarikat × penapis saham; skor dikira pada saham carian sahaja. **4,923 calon** berskor positif (sehingga 5 peraturan terbaik setiap isyarat beli; tiada had bilangan).
- Setup lengkap setiap calon: beli pada buka esok; stop loss 4xATR14; pegang sekurang-kurangnya hingga hari ke-20; selepas itu jual bila harga tutup di bawah purata 20 hari; paling lama 6 bulan (cara pegang B pilihan pengguna).
- "Lulus" = pada saham yang carian tidak lihat: belian ≥ 300, ≥ 10 tahun aktif, dan lebih kerap menangkap saham naik laju daripada saham rawak pada hari yang sama dalam KETIGA-TIGA tempoh (2010–19, 2020–24, 2025–26).

## 2. Ujian (ditetapkan dahulu)

- Peraturan yang cukup belian untuk dinilai: 4,711 calon dan 288 kawalan rawak.
- **B1** kadar lulus: calon **84 %** lawan kawalan rawak 18 % (perlu beza ≥ 20 mata) → lulus.
- **B2** lebih baik daripada rawak pada 2025–26 (tahun yang carian tidak lihat): calon **90 %** lawan kawalan 52 % (perlu ≥ 60 % dan beza ≥ 10 mata) → lulus.
- **Keputusan: carian naik laju BERHASIL — kod F didaftarkan.**

## 3. Berapa yang lulus dan didaftarkan

- Lulus: **3,976** daripada 4,923 calon.
- Daripada yang lulus, 2,017 ialah kembar setup lain (membeli saham yang sama pada hari yang sama, pertindihan ≥ 80%; 25 daripadanya kembar setup F lama) dan tidak diberi kod sendiri; ia direkod dalam `calon.csv.gz` (lajur `kembar_kepada`).
- **Setup berlainan yang lulus: 1,959** → didaftarkan sebagai **`F96`–`F2054`** (1,959 kod baharu; `F01`–`F95` tidak diubah).
- Anggaran bahagian yang lulus kerana nasib (kadar lulus kawalan ÷ kadar lulus calon): kira-kira 21 %.

## 4. Ikut tempoh (peraturan yang cukup belian; saham yang carian tidak lihat)

| Kumpulan | Bilangan | Lebih baik daripada rawak: 2010–19 | 2020–24 | **2025–26** | Median kelebihan 2010–19 / 2020–24 / 2025–26 (mata) | Lulus |
|---|---|---|---|---|---|---|
| Calon carian | 4,711 | 99% | 94% | **90%** | +5.4 / +4.7 / +4.9 | 84% |
| Kawalan rawak | 288 | 53% | 46% | **52%** | +0.0 / -0.1 / +0.1 | 18% |
| Calon tanpa prasyarat pasaran | 263 | 98% | 86% | **85%** | +4.5 / +3.2 / +2.8 | 73% |
| Setup F lama (69) | 62 | 89% | 85% | **77%** | +2.4 / +1.7 / +1.9 | 66% |
| Kod baharu | 1,959 | 100% | 100% | **100%** | +5.6 / +5.0 / +5.2 | 100% |

## 5. Banding (nilai tengah setiap kumpulan; saham yang carian tidak lihat)

| Kumpulan | Bilangan | Naik ≥ 5 % minggu 1 % (rawak) | Naik laju % (rawak) | Jual hari ke-20: menang · purata | Cara pegang B: menang · purata · rugi ≥ 15 % · hari |
|---|---|---|---|---|---|
| Setup F lama yang dipercayai | 42 | 26 (22) | 13 (10) | 53 % · +1.8 % | 49 % · +2.1 % · 16 % · 22 |
| Kod baharu | 1,959 | 23 (13) | 12 (6) | 50 % · +0.3 % | 47 % · +0.4 % · 6 % · 21 |
| Kawalan rawak | 288 | 11 (12) | 6 (6) | 50 % · +0.2 % | 46 % · +0.3 % · 4 % · 22 |

## 6. Kod baharu: pecahan

- Dengan prasyarat pasaran: 1,854; dengan prasyarat syarikat/kumpulan: 1,945; tanpa apa-apa prasyarat: 0.
- Prasyarat paling kerap: >= 15% saham dalam 5% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang (235); Mei-Okt + earnings dalam 1-5 sesi akan datang (157); keluasan naik >= 10 mata dalam 10 sesi + earnings dalam 1-5 sesi akan datang (136); SPY atas SMA200 + earnings dalam 1-5 sesi akan datang (126); turun-naik SPY menurun (21 hari < 63 hari) + earnings dalam 1-5 sesi akan datang (120); QQQ SMA10 > SMA20 + earnings dalam 1-5 sesi akan datang (97); QQQ dalam 3% dari puncak 52 minggu + earnings dalam 1-5 sesi akan datang (93); SPY Peringkat 2 Weinstein (atas SMA150 yang naik) + earnings dalam 1-5 sesi akan datang (89).
- Isyarat beli: 169 kaedah/keluarga berbeza; paling kerap K01 (195), K03 (109), K02 (91), K17 (87), K09 (77), K18 (70), K07 (69), K13 (61).
- Kekerapan pada senarai Shariah: 30 setup teratas senarai utama digabung = 604 belian setahun (ada belian dalam 96% bulan); semua 2,001 setup senarai utama = 11072 setahun (100% bulan).
- Jualan pada hari beli: 0 (mesti 0).

## 6b. Sifat kod baharu (analisis SELEPAS hasil; bukan ditetapkan dahulu)

- **1,862 daripada 1,959 kod baharu memakai SATU prasyarat yang sama: laporan kewangan (earnings) dalam 1–5 hari akan datang.** Harga bergerak besar selepas laporan kewangan, jadi belian begini lebih kerap menangkap saham naik laju — dan juga lebih kerap jatuh.
- Kadar tangkap kod baharu kira-kira dua kali saham rawak, tetapi **kadar menang dan purata setiap dagangan hampir sama dengan peraturan rawak** (jadual di bawah). Setup F lama yang dipercayai mempunyai purata yang jauh lebih tinggi.

| Kumpulan | Bilangan | Tangkap % (rawak) | Cara pegang B: menang % | Purata % | Rugi ≥ 15 % % | Beli setahun (nilai tengah) |
|---|---|---|---|---|---|---|
| Kod baharu: laporan kewangan dalam 1–5 hari | 1,862 | 12 (6) | 47 | +0.4 | 6 | 57 |
| Kod baharu: prasyarat lain | 97 | 13 (10) | 46 | +1.3 | 18 | 38 |
| Setup F lama yang dipercayai | 42 | 13 (10) | 49 | +2.1 | 16 | 66 |
| Kawalan rawak | 288 | 6 (6) | 46 | +0.3 | 4 | 105 |

- Dalam senarai utama (2,001 setup): 467 menang ≥ 50 %; 251 purata ≥ +2 % setiap dagangan; **210 kedua-duanya** (17 lama, 193 baharu). Ini paparan pada saham yang sudah dilihat, bukan pemilihan.


## 7. Kaveat

- Beribu calon disemak pada saham yang tidak dilihat, jadi sebahagian lulus kerana nasib (anggaran di §3); kumpulan saham itu sudah digunakan dalam pusingan terdahulu.
- 2025–26 pendek (kira-kira 20 bulan) dan belian di dalamnya sedikit bagi kebanyakan setup.
- "Lebih baik daripada rawak hari sama" mengukur PILIHAN saham; kadar mentah turut mengandungi kesan BILA membeli (keadaan pasaran).
- Tiada saham delist dalam data (condong ke atas, lebih-lebih lagi bagi pegangan hingga 6 bulan). Backtest sahaja; tiada papertrade tanpa keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.
