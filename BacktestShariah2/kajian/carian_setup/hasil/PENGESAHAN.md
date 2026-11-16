# Analisis pengesahan: "tunggu confirmation, contohnya higher high, baru entry" (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_sahkan.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (ac) [asalnya (r) di cawangan lama], dikomit sebelum dijalankan. **Jangan sunting secara manual.** Amalan pakar dan sumber: `kajian/KAJIAN_PENGESAHAN.md`.

## 1. Gaya masuk yang mana lebih kerap menangkap? (pencetus SAHAJA, tanpa prasyarat atau penapis; kumpulan B)

Setiap baris = median merentas semua varian parameter keluarga dalam gaya itu. Kelebihan = kadar tangkap pencetus tolak saham rawak hari sama (mata peratus). Swing = naik ≥ 5 % minggu pertama dan naik lagi hingga minggu ke-4; trend = naik ≥ 50 % sebelum jatuh 15 % dalam 6 bulan.

| Gaya masuk | Varian | Swing: kelebihan median | Swing: % varian > 0 | Trend: kelebihan median | Trend: % varian > 0 |
|---|---|---|---|---|---|
| beli semasa lemah (tiada pengesahan) | 201 | +0.32 | 92% | -0.26 | 32% |
| pengesahan pembalikan (lemah lalu berpatah naik) | 69 | -0.00 | 49% | -0.23 | 26% |
| undur dalam uptrend | 63 | +0.03 | 62% | +0.15 | 60% |
| pengesahan kekuatan / higher high (pecah tinggi, silang naik, gap) | 313 | +0.06 | 65% | +0.02 | 55% |
| lain (julat sempit) | 10 | -0.22 | 0% | +0.08 | 80% |

- Keluarga `K10` (pecah tinggi n hari = "higher high" paling terus, 40 varian): swing kelebihan median +0.28 mata (88% varian > 0); trend +0.20 mata (80% > 0).
- Lima varian terbaik setiap label:

  - swing: jatuh >= 30% dalam 10 hari (+3.1); jatuh >= 30% dalam 5 hari (+3.0); jatuh >= 25% dalam 3 hari (+3.0); jatuh >= 30% dalam 2 hari (+2.9); gap >= 15.0% + volum 3.0x (+2.5)
  - trend: gap >= 15.0% + volum 3.0x (+5.1); RS silang atas 95 (+4.4); gap >= 15.0% + volum 2.0x (+4.3); gap >= 15.0% + volum 1.5x (+3.9); jatuh >= 30% dalam 5 hari (+3.9)

## 2. Lapisan pengesahan atas setup F (69 setup; kumpulan B; isyarat yang sama bagi ketiga-tiga cara)

- **V0** = beli pada buka esok (cara sekarang). **S1** = tunggu satu TUTUP di atas tinggi hari isyarat dalam 3 sesi, beli pada buka berikutnya. **S2** = letak buy-stop pada tinggi hari isyarat; dibeli sebaik harga melepasinya dalam 3 sesi. Jika tiada pengesahan, tiada belian. Semua kadar diukur dari harga beli sebenar; henti dan keluar setup sendiri.

Median 42 setup dipercayai:

| Cara | % isyarat dibeli | Harga beli lawan V0 | Naik ≥ 5 % minggu 1 % | **Naik lagi hingga minggu 4 %** | Tangkap penuh % | Menang % | Rugi ≥ 8 % % | Purata % |
|---|---|---|---|---|---|---|---|---|
| V0 beli buka esok | 100 | – | 26.0 | **13.5** | 14.5 | 52 | 28.9 | +1.72 |
| S1 tutup sahkan | 52 | +4.1 % | 24.8 | **12.4** | 12.0 | 52 | 28.5 | +1.44 |
| S2 pecah tinggi (buy-stop) | 74 | +1.6 % | 25.3 | **12.7** | 14.0 | 52 | 28.6 | +1.67 |

- **Bacaan dikunci** (kadar "naik lagi" DAN tangkap penuh lebih tinggi daripada V0 bagi lebih separuh setup dipercayai): S1 2 daripada 42 → **TIDAK menolong**; S2 5 daripada 42 → **TIDAK menolong**.
- Bilangan tangkapan mutlak (kadar × belian), median lawan V0: S1 -57 %, S2 -28 %.
- Adakah pengesahan memisahkan yang jadi daripada yang gagal? Isyarat yang SAMA, dibeli cara V0: yang kemudian memecah tinggi hari isyarat → "naik lagi" 17.5 %, purata +3.46 %; yang tidak → 4.0 %, purata -2.86 %.

## 3. Setiap setup dipercayai

| # | ID | Dibeli S1 / S2 % | Naik lagi %: V0 / S1 / S2 | Tangkap penuh %: V0 / S1 / S2 | Menang %: V0 / S1 / S2 | Rugi ≥ 8 %: V0 / S1 / S2 | Purata %: V0 / S1 / S2 |
|---|---|---|---|---|---|---|---|
| 1 | `F43` | 71 / 87 | 25.3 / 21.4 / 23.9 | 22.8 / 18.1 / 21.0 | 70 / 72 / 71 | 16 / 13 / 14 | +5.83 / +5.68 / +5.89 |
| 2 | `F63` | 43 / 59 | 21.8 / 15.5 / 21.9 | 25.5 / 17.1 / 22.7 | 61 / 62 / 61 | 26 / 22 / 25 | +4.48 / +3.74 / +4.16 |
| 3 | `F65` | 67 / 84 | 21.8 / 17.1 / 20.1 | 21.8 / 14.0 / 18.9 | 63 / 62 / 60 | 25 / 26 / 24 | +2.86 / +1.60 / +2.30 |
| 4 | `F51` | 49 / 62 | 20.8 / 14.2 / 21.2 | 22.0 / 14.8 / 18.8 | 64 / 66 / 65 | 19 / 15 / 16 | +4.84 / +4.32 / +4.71 |
| 5 | `F50` | 57 / 73 | 20.5 / 16.0 / 22.1 | 26.6 / 19.5 / 26.4 | 58 / 60 / 60 | 26 / 22 / 25 | +3.90 / +3.32 / +3.80 |
| 6 | `F56` | 37 / 51 | 18.7 / 17.3 / 18.0 | 21.8 / 16.6 / 20.7 | 59 / 58 / 61 | 23 / 22 / 24 | +4.83 / +3.44 / +4.03 |
| 7 | `F39` | 64 / 81 | 18.2 / 12.2 / 15.0 | 21.4 / 12.2 / 17.2 | 51 / 42 / 46 | 33 / 34 / 35 | +1.83 / -0.78 / +0.12 |
| 8 | `F91` | 64 / 83 | 17.8 / 8.6 / 17.8 | 19.7 / 9.5 / 18.1 | 54 / 53 / 58 | 28 / 25 / 26 | +2.80 / +1.31 / +2.87 |
| 9 | `F40` | 61 / 79 | 17.9 / 15.5 / 17.1 | 21.9 / 17.4 / 20.0 | 51 / 48 / 49 | 32 / 31 / 32 | +2.15 / +0.93 / +1.84 |
| 10 | `F89` | 63 / 84 | 17.3 / 8.7 / 17.2 | 18.3 / 9.9 / 16.9 | 53 / 52 / 56 | 29 / 26 / 27 | +1.94 / +0.81 / +2.06 |
| 11 | `F90` | 67 / 84 | 17.2 / 15.3 / 17.3 | 19.1 / 16.3 / 17.6 | 48 / 49 / 49 | 31 / 31 / 32 | +0.58 / -0.37 / +0.48 |
| 12 | `F88` | 65 / 82 | 16.1 / 15.0 / 14.5 | 17.8 / 15.0 / 16.9 | 60 / 62 / 61 | 19 / 16 / 17 | +2.42 / +2.71 / +2.74 |
| 13 | `F92` | 66 / 82 | 15.9 / 15.3 / 14.9 | 16.2 / 15.3 / 15.6 | 59 / 61 / 61 | 18 / 17 / 17 | +2.25 / +2.60 / +2.65 |
| 14 | `F58` | 45 / 57 | 15.6 / 12.4 / 17.1 | 22.2 / 11.8 / 20.4 | 47 / 47 / 50 | 36 / 28 / 36 | +0.70 / +0.98 / +1.28 |
| 15 | `F41` | 43 / 60 | 15.5 / 15.5 / 18.0 | 19.2 / 17.8 / 19.4 | 46 / 51 / 49 | 40 / 29 / 36 | -0.16 / +1.38 / +1.37 |
| 16 | `F45` | 51 / 69 | 14.5 / 13.3 / 13.9 | 16.1 / 13.6 / 15.8 | 55 / 52 / 53 | 26 / 28 / 29 | +3.25 / +1.84 / +2.70 |
| 17 | `F27` | 25 / 38 | 14.1 / 12.3 / 12.2 | 14.5 / 11.8 / 12.4 | 53 / 55 / 53 | 27 / 26 / 28 | +1.63 / +1.74 / +0.97 |
| 18 | `F03` | 28 / 42 | 14.3 / 15.9 / 15.2 | 17.7 / 16.2 / 16.0 | 54 / 55 / 53 | 29 / 30 / 31 | +2.82 / +3.62 / +2.68 |
| 19 | `F07` | 50 / 75 | 14.1 / 10.9 / 13.7 | 15.8 / 13.0 / 14.5 | 54 / 54 / 54 | 27 / 25 / 28 | +1.90 / +1.82 / +1.85 |
| 20 | `F11` | 29 / 43 | 13.7 / 13.8 / 12.8 | 14.5 / 13.0 / 13.0 | 56 / 57 / 56 | 25 / 24 / 25 | +2.40 / +2.39 / +2.03 |
| 21 | `F95` | 59 / 80 | 13.6 / 15.4 / 15.2 | 16.1 / 15.9 / 16.3 | 52 / 52 / 54 | 25 / 29 / 25 | +1.69 / +2.25 / +2.33 |
| 22 | `F10` | 26 / 38 | 13.3 / 10.0 / 10.4 | 12.0 / 9.5 / 9.6 | 45 / 44 / 43 | 30 / 29 / 32 | +0.83 / -0.05 / -0.13 |
| 23 | `F24` | 55 / 78 | 12.8 / 12.4 / 12.5 | 13.0 / 12.6 / 12.1 | 47 / 46 / 46 | 32 / 30 / 31 | +1.03 / +1.14 / +1.00 |
| 24 | `F93` | 57 / 79 | 12.9 / 13.0 / 13.7 | 12.4 / 11.5 / 12.6 | 49 / 52 / 50 | 22 / 22 / 22 | +0.99 / +0.84 / +1.24 |
| 25 | `F42` | 57 / 78 | 12.6 / 7.0 / 12.7 | 15.6 / 10.5 / 14.8 | 53 / 53 / 53 | 29 / 32 / 31 | +3.60 / +4.20 / +4.28 |
| 26 | `F22` | 47 / 67 | 12.7 / 10.3 / 12.1 | 11.8 / 10.4 / 11.4 | 42 / 42 / 42 | 25 / 27 / 26 | +0.19 / -0.29 / -0.01 |
| 27 | `F16` | 63 / 87 | 12.8 / 12.2 / 12.5 | 13.1 / 11.7 / 13.0 | 53 / 50 / 52 | 28 / 30 / 28 | +2.04 / +1.00 / +1.55 |
| 28 | `F02` | 55 / 76 | 12.2 / 12.4 / 11.5 | 12.6 / 11.3 / 11.2 | 55 / 60 / 57 | 25 / 21 / 23 | +2.04 / +2.80 / +2.27 |
| 29 | `F60` | 37 / 56 | 11.9 / 11.2 / 11.0 | 13.3 / 11.4 / 11.8 | 49 / 48 / 49 | 33 / 35 / 35 | +1.43 / +0.53 / +1.01 |
| 30 | `F48` | 50 / 68 | 12.1 / 10.5 / 11.4 | 13.3 / 11.9 / 12.9 | 47 / 44 / 48 | 36 / 39 / 35 | +0.73 / -0.55 / +0.73 |
| 31 | `F44` | 53 / 78 | 12.3 / 12.1 / 11.8 | 14.0 / 14.0 / 13.5 | 48 / 50 / 49 | 35 / 33 / 34 | +1.35 / +1.33 / +1.69 |
| 32 | `F06` | 48 / 68 | 12.0 / 10.3 / 11.6 | 12.2 / 10.1 / 11.5 | 52 / 52 / 51 | 29 / 29 / 29 | +1.75 / +1.59 / +1.56 |
| 33 | `F29` | 54 / 77 | 11.5 / 11.3 / 11.9 | 11.7 / 11.4 / 11.6 | 40 / 40 / 41 | 49 / 49 / 48 | +0.10 / +0.21 / +0.41 |
| 34 | `F01` | 47 / 65 | 11.7 / 9.6 / 11.7 | 12.0 / 10.6 / 11.3 | 52 / 52 / 53 | 29 / 28 / 26 | +2.52 / +2.51 / +3.06 |
| 35 | `F25` | 48 / 71 | 11.4 / 11.8 / 11.5 | 12.0 / 11.7 / 12.4 | 44 / 47 / 45 | 34 / 32 / 34 | +0.12 / +0.70 / +0.17 |
| 36 | `F61` | 48 / 70 | 11.3 / 9.7 / 10.7 | 11.9 / 11.4 / 12.1 | 49 / 50 / 49 | 35 / 36 / 36 | +0.59 / +0.71 / +0.73 |
| 37 | `F05` | 48 / 67 | 11.5 / 10.1 / 11.1 | 11.7 / 10.6 / 10.9 | 51 / 52 / 51 | 30 / 28 / 29 | +1.63 / +1.81 / +1.87 |
| 38 | `F28` | 51 / 73 | 11.2 / 14.1 / 12.1 | 11.3 / 13.2 / 11.3 | 51 / 54 / 52 | 29 / 26 / 28 | +1.09 / +1.49 / +0.99 |
| 39 | `F09` | 57 / 81 | 11.2 / 10.7 / 11.1 | 11.2 / 10.5 / 10.7 | 49 / 48 / 49 | 30 / 31 / 30 | +0.80 / +0.30 / +0.63 |
| 40 | `F30` | 56 / 78 | 11.3 / 10.9 / 11.4 | 12.0 / 10.9 / 12.0 | 51 / 50 / 51 | 28 / 29 / 28 | +1.01 / +0.82 / +0.96 |
| 41 | `F08` | 48 / 68 | 10.9 / 9.8 / 10.7 | 11.1 / 10.3 / 10.5 | 51 / 51 / 51 | 30 / 29 / 29 | +1.47 / +1.55 / +1.66 |
| 42 | `F94` | 57 / 77 | 10.0 / 12.6 / 11.6 | 13.2 / 14.4 / 15.0 | 45 / 50 / 45 | 31 / 31 / 30 | -0.38 / +0.08 / +0.02 |

Kaveat: kumpulan B sudah dilihat; tiada saham delist; S2 mengandaikan pesanan buy-stop terisi pada harga pencetus (tiada gelinciran); prasyarat (cth. earnings 1–5 sesi) dinilai pada hari isyarat, jadi belian yang ditangguh boleh jatuh selepas tarikh earnings. Backtest sahaja.
