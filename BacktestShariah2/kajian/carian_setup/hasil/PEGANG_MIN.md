# Analisis pegang minimum: "tak mahu beli dan jual hari yang sama; pegang sekurang-kurangnya 3 hari"

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_pegang.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (o). **Jangan sunting secara manual.**

## 1. Papertrade langsung: dari mana datangnya "beli dan jual hari sama"?

- Lejar (semua kaedah, 14,168 dagangan ditutup, beli 2026-10-16 hingga 2026-11-09): dijual **pada hari beli 2.7 %**, esoknya 21.5 %, hari ke-3 5.9 %. Semua jualan hari sama berpunca daripada henti (352), delist (28); purata hasilnya -2.4 %.
- Papertrade C: 1,071 daripada 9,676 dagangan ditutup (11%) dijual pada hari beli; paling banyak M14 (111), M70 (109), M102 (57), M18 (48), M35 (42), M123 (38), M49 (35), M20 (34).
- 69 daripada 117 kaedah (≥ 30 dagangan) tiada langsung jualan hari sama. Puncanya kaedah M tertentu yang henti ruginya ketat dan aktif pada hari beli:

| Kaedah | Dagangan | Dijual hari sama % | Dijual dalam < 3 hari % | Purata % |
|---|---|---|---|---|
| `M70` | 126 | 56 | 79 | -2.2 |
| `M123` | 37 | 35 | 86 | -2.2 |
| `M49` | 65 | 22 | 43 | -5.9 |
| `M102` | 88 | 20 | 45 | -5.1 |
| `M35` | 64 | 20 | 48 | -4.3 |
| `M18` | 75 | 17 | 61 | -3.0 |
| `M14` | 241 | 15 | 42 | -4.2 |
| `M13` | 167 | 14 | 35 | -6.6 |
| `M28` | 31 | 13 | 52 | -3.8 |
| `M57` | 39 | 13 | 38 | -6.5 |

## 2. Setup F (61 setup kedudukan akhir; kumpulan B)

- **Jualan pada hari beli: 0 dalam semua setup F.** Mekanik F (sejak pindaan asal, syarat wajib "tiada jual hari beli"): beli pada buka; henti rugi tidak aktif pada hari beli; indikator keluar dinilai pada tutup dan dijual pada buka esok.
- Tetapi jualan AWAL memang berlaku. Median setup dipercayai: dijual pada hari ke-2 1.2 %, hari ke-3 1.3 % daripada belian; punca: henti rugi 1.2 %, indikator keluar 0.3 %. Purata hasil dagangan yang dijual sebelum hari ke-4: -14.5 %.

## 3. Tiga mekanik pada setup yang sama (median 34 setup dipercayai)

| Mekanik | Dijual sebelum hari ke-4 % | Tangkap penuh % | Menang % | Rugi ≥ 8 % % | Rugi ≥ 15 % % | Purata % | Pegang (sesi) |
|---|---|---|---|---|---|---|---|
| V0 sedia ada | 2.5 | 14.1 | 51 | 29.0 | 15.3 | +1.79 | 17.9 |
| V1 indikator mulai hari ke-4; henti kekal aktif | 1.2 | 14.0 | 52 | 29.0 | 15.4 | +1.79 | 18.0 |
| V2 indikator DAN henti mulai hari ke-4 | 0.0 | 14.0 | 52 | 28.9 | 15.1 | +1.75 | 18.0 |

- V1 lawan V0: tangkap penuh lebih tinggi bagi 12 daripada 34 setup dipercayai, purata lebih tinggi bagi 11, rugi ≥ 8 % lebih tinggi bagi 13.
- V2 lawan V0: tangkap penuh lebih tinggi bagi 16, purata lebih tinggi bagi 22, rugi ≥ 15 % lebih tinggi bagi 19.

## 4. Setiap setup dipercayai

| # | ID | Keluar | Dijual hari ke-2 / ke-3 % (V0) | Tangkap penuh %: V0 / V1 / V2 | Menang %: V0 / V1 / V2 | Rugi ≥ 8 %: V0 / V1 / V2 | Rugi ≥ 15 %: V0 / V1 / V2 | Purata %: V0 / V1 / V2 |
|---|---|---|---|---|---|---|---|---|
| 1 | `F43` | H4 · X00 | 0.0 / 0.4 | 22.7 / 22.7 / 22.7 | 70 / 70 / 70 | 17 / 17 / 17 | 8 / 8 / 8 | +5.78 / +5.78 / +5.78 |
| 2 | `F63` | H4 · X00 | 1.9 / 3.0 | 25.5 / 25.5 / 25.5 | 61 / 61 / 61 | 26 / 26 / 26 | 15 / 15 / 15 | +4.48 / +4.48 / +4.48 |
| 3 | `F65` | H3 · X12 | 3.5 / 4.7 | 21.7 / 21.7 / 21.7 | 63 / 63 / 63 | 25 / 25 / 24 | 10 / 10 / 10 | +2.82 / +2.82 / +2.87 |
| 4 | `F51` | H4 · X10 DAN X21 | 2.3 / 2.0 | 22.0 / 22.0 / 22.0 | 65 / 65 / 65 | 19 / 19 / 18 | 7 / 7 / 7 | +4.84 / +4.84 / +4.97 |
| 5 | `F50` | H4 · X00 | 2.5 / 2.3 | 26.7 / 26.7 / 26.6 | 58 / 58 / 58 | 26 / 26 / 26 | 16 / 16 / 16 | +3.99 / +3.99 / +3.93 |
| 6 | `F56` | H4 · X00 | 0.3 / 0.5 | 22.1 / 22.1 / 22.1 | 60 / 60 / 60 | 23 / 23 / 23 | 13 / 13 / 12 | +4.90 / +4.90 / +4.92 |
| 7 | `F39` | H3 · X09 DAN X21 | 3.4 / 4.8 | 21.4 / 21.4 / 21.4 | 51 / 51 / 52 | 33 / 33 / 33 | 9 / 9 / 10 | +1.82 / +1.83 / +1.75 |
| 8 | `F40` | H3 · X14 DAN X21 | 3.7 / 3.9 | 21.9 / 21.9 / 21.9 | 51 / 51 / 52 | 32 / 32 / 31 | 9 / 9 / 11 | +2.15 / +2.15 / +2.12 |
| 9 | `F58` | H3 · X12 | 4.2 / 3.2 | 22.1 / 22.2 / 22.2 | 47 / 47 / 48 | 36 / 36 / 35 | 14 / 14 / 14 | +0.73 / +0.70 / +0.89 |
| 10 | `F41` | H3 · X12 | 2.8 / 3.6 | 19.3 / 19.2 / 19.2 | 46 / 46 / 47 | 40 / 40 / 39 | 19 / 19 / 21 | -0.17 / -0.18 / -0.19 |
| 11 | `F45` | H4 · X12 DAN X19 | 0.4 / 0.4 | 16.9 / 16.9 / 16.9 | 54 / 54 / 54 | 26 / 26 / 26 | 15 / 15 / 15 | +3.28 / +3.28 / +3.33 |
| 12 | `F27` | H4 · X07 DAN X21 | 0.6 / 0.8 | 14.8 / 14.8 / 14.8 | 54 / 54 / 54 | 27 / 27 / 27 | 17 / 17 / 17 | +1.85 / +1.85 / +1.86 |
| 13 | `F03` | H4 · X20 DAN X21 | 0.2 / 0.2 | 17.6 / 17.6 / 17.6 | 54 / 54 / 54 | 29 / 29 / 29 | 17 / 17 / 17 | +3.00 / +3.00 / +3.05 |
| 14 | `F07` | H4 · X13 | 2.4 / 1.5 | 15.3 / 15.7 / 15.7 | 55 / 54 / 54 | 27 / 27 / 27 | 19 / 19 / 19 | +1.88 / +1.90 / +1.88 |
| 15 | `F11` | H4 · X04 DAN X12 | 0.5 / 0.6 | 14.7 / 14.7 / 14.7 | 56 / 56 / 56 | 25 / 25 / 25 | 13 / 13 / 13 | +2.53 / +2.53 / +2.55 |
| 16 | `F10` | H3 · X12 ATAU X19 | 0.9 / 1.5 | 12.1 / 12.1 / 12.1 | 45 / 45 / 45 | 30 / 30 / 30 | 9 / 9 / 9 | +0.88 / +0.88 / +0.88 |
| 17 | `F24` | H4 · X11 DAN X22 | 2.1 / 2.1 | 12.7 / 13.0 / 13.0 | 46 / 47 / 47 | 32 / 32 / 32 | 16 / 17 / 17 | +0.91 / +0.98 / +0.95 |
| 18 | `F42` | H3 · X00 | 1.3 / 0.0 | 15.7 / 15.7 / 15.8 | 53 / 53 / 53 | 29 / 29 / 29 | 15 / 15 / 15 | +3.53 / +3.53 / +3.59 |
| 19 | `F22` | H2 · X11 ATAU X21 | 35.5 / 11.7 | 9.6 / 12.1 / 12.3 | 40 / 42 / 42 | 17 / 26 / 23 | 1 / 1 / 4 | +0.10 / +0.14 / +0.21 |
| 20 | `F16` | H4 · X21 DAN X22 | 0.3 / 0.8 | 13.0 / 13.0 / 13.0 | 53 / 53 / 53 | 28 / 28 / 28 | 17 / 18 / 18 | +2.03 / +2.02 / +2.04 |
| 21 | `F02` | H4 · X08 DAN X22 | 3.4 / 0.8 | 12.4 / 12.9 / 12.9 | 55 / 56 / 56 | 24 / 24 / 24 | 12 / 13 / 13 | +1.98 / +2.10 / +2.11 |
| 22 | `F60` | H3 · X12 DAN X22 | 1.2 / 1.5 | 13.7 / 13.7 / 13.7 | 49 / 49 / 49 | 34 / 33 / 33 | 17 / 17 / 17 | +1.30 / +1.34 / +1.39 |
| 23 | `F48` | H3 · X13 DAN X21 | 1.0 / 2.5 | 14.4 / 14.3 / 14.3 | 48 / 48 / 49 | 35 / 35 / 34 | 14 / 14 / 13 | +1.02 / +1.00 / +1.18 |
| 24 | `F44` | H3 · X00 | 0.7 / 1.1 | 13.8 / 13.8 / 13.8 | 48 / 48 / 48 | 36 / 36 / 35 | 19 / 19 / 19 | +1.13 / +1.13 / +1.17 |
| 25 | `F06` | H4 · X18 DAN X22 | 0.2 / 0.3 | 12.3 / 12.3 / 12.2 | 52 / 52 / 52 | 29 / 29 / 29 | 16 / 16 / 16 | +1.75 / +1.75 / +1.75 |
| 26 | `F01` | H4 · X03 DAN X22 | 0.9 / 0.7 | 11.9 / 12.0 / 12.0 | 52 / 52 / 52 | 28 / 29 / 29 | 14 / 15 / 15 | +2.51 / +2.51 / +2.50 |
| 27 | `F29` | H2 · X21 DAN X22 | 8.9 / 6.0 | 11.8 / 11.9 / 12.3 | 39 / 40 / 41 | 49 / 50 / 49 | 2 / 2 / 4 | +0.05 / +0.03 / +0.07 |
| 28 | `F25` | H4 · X22 DAN X24 | 1.5 / 2.0 | 12.0 / 12.1 / 12.1 | 43 / 44 / 44 | 34 / 34 / 34 | 18 / 19 / 19 | +0.14 / +0.15 / +0.14 |
| 29 | `F61` | H3 · X13 | 2.5 / 1.6 | 12.3 / 12.3 / 12.3 | 49 / 49 / 49 | 35 / 35 / 35 | 15 / 15 / 15 | +0.57 / +0.58 / +0.64 |
| 30 | `F05` | H4 · X14 DAN X22 | 0.7 / 0.6 | 11.7 / 11.7 / 11.7 | 51 / 51 / 51 | 30 / 30 / 30 | 15 / 16 / 16 | +1.63 / +1.60 / +1.59 |
| 31 | `F28` | H4 · X20 DAN X21 | 0.4 / 0.7 | 11.5 / 11.5 / 11.5 | 51 / 52 / 52 | 29 / 29 / 29 | 14 / 14 / 14 | +1.13 / +1.19 / +1.19 |
| 32 | `F09` | H4 · X14 DAN X22 | 1.1 / 1.0 | 11.3 / 11.4 / 11.4 | 49 / 49 / 49 | 29 / 30 / 30 | 16 / 16 / 16 | +0.93 / +0.88 / +0.88 |
| 33 | `F30` | H4 · X21 DAN X22 | 0.2 / 0.3 | 11.8 / 11.8 / 11.8 | 51 / 51 / 51 | 28 / 28 / 28 | 18 / 18 / 18 | +1.00 / +1.00 / +0.99 |
| 34 | `F08` | H4 · X18 DAN X22 | 0.3 / 0.2 | 11.1 / 11.1 / 11.1 | 50 / 50 / 51 | 30 / 30 / 30 | 17 / 17 / 17 | +1.45 / +1.45 / +1.44 |

Kaveat: kumpulan B sudah dilihat; tiada saham delist; backtest sahaja. Baris V0 disahkan sama dengan enjin lama.
