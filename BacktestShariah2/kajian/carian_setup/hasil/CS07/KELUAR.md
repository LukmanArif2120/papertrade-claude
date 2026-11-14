# CS07 (b): cari dan tala KELUAR — "indikator yang memberitahu kenaikan sudah tamat" (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_keluar7.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(b) dan penjelasan (n)-1, dikomit sebelum dijalankan. **Jangan sunting secara manual.**

## 1. Apa yang dicari

- 97 atom keluar berparameter (MA, EMA, MACD, RSI, Supertrend, rendah k hari, Stochastic, volum, Chandelier, ekor, "tiada kemajuan") → 9,410 peraturan (tunggal, ATAU, DAN) × 3 syarat aktif (sentiasa / selepas +5 % / selepas +10 %) × 8 henti = **225,840 cara keluar setiap setup**, bagi 73 setup, pada kumpulan A sahaja.
- Ukuran: **tangkap penuh** = naik ≥ 5 % minggu pertama DAN dijual dengan untung ≥ 10 %. Syarat "tidak jual awal": untung pada saham yang terus naik mesti ≥ 90% daripada "pegang sahaja 20 sesi".
- 80,496 daripada 225,840 cara keluar lulus syarat itu pada kumpulan A. Tanpa syarat, keluar terbaik menaikkan tangkap penuh +1.9 mata tetapi dengan menjual saham yang masih naik.

## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)

- Keluar terpilih mengatasi `X00` (pegang sahaja, henti sama): **23 daripada 73** setup; mengatasi keluar lama: **41 daripada 61**; mengatasi kedua-duanya: **20 daripada 61**.
- Syarat "tidak jual awal" kekal pada B: 63 daripada 73 setup (median nisbah 1.00).
- Rugi ≥ 8 %: median beza lawan keluar lama -1.7 mata.
- Median tangkap penuh (semua isyarat): keluar lama 14.7 % → pegang sahaja 14.7 % → keluar terpilih **15.1 %**. Median kekurangan dari puncak: lama 10.4 → terpilih 10.0 mata.
- **Keputusan: keluar TIDAK menolong** mengikut bacaan yang dikunci.

## 3. Keluar sejagat (10 teratas daripada 30; dipilih pada A, disemak pada B)

| # | Henti | Peraturan keluar | A: tambahan tangkap penuh (mata) | A: nisbah simpan | B: tambahan (mata) | B: % setup lebih baik | B: nisbah simpan |
|---|---|---|---|---|---|---|---|
| 1 | 4xATR14 | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.92 | 79% | 0.92 |
| 2 | min(-10%, 4xATR14) | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.92 | 79% | 0.92 |
| 3 | 5xATR14 | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.91 | 79% | 0.92 |
| 4 | 3xATR14 | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.92 | 79% | 0.92 |
| 5 | -8% | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.92 | 78% | 0.92 |
| 6 | -15% | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.92 | 79% | 0.92 |
| 7 | -12% | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.93 | 78% | 0.92 |
| 8 | -10% | RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.52 | 0.93 | +0.92 | 78% | 0.92 |
| 9 | -8% | RSI14 > 80 ATAU RSI7 > 85 [aktif selepas +10%] | +0.51 | 0.93 | +0.94 | 81% | 0.92 |
| 10 | 3xATR14 | RSI7 > 85 [aktif selepas +10%] | +0.51 | 0.94 | +0.93 | 82% | 0.92 |

## 4. Setiap setup (kumpulan B; semua isyarat, perbandingan berpasangan)

| ID | Keluar lama | Keluar terpilih | Tangkap penuh %: lama / pegang sahaja / **terpilih** | 2025–26: lama / pegang / terpilih | Nisbah simpan | Rugi ≥ 8 %: lama → terpilih | Menang %: lama → terpilih | Kurang dari puncak: lama → terpilih | Pegang (sesi) |
|---|---|---|---|---|---|---|---|---|---|
| `F43` | H4 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 22.6 / 22.6 / **22.6** | 11.5 / 11.5 / 11.5 | 1.00 | 17 → 16 | 69 → 69 | 7.1 → 7.2 | 19 → 20 |
| `F63` | H4 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 25.0 / 25.0 / **25.0** | 20.8 / 20.8 / 20.8 | 1.00 | 27 → 26 | 60 → 61 | 10.1 → 10.1 | 18 → 19 |
| `F65` | H3 · X12 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 21.3 / 21.3 / **21.3** | 21.2 / 21.2 / 21.2 | 1.00 | 25 → 20 | 62 → 65 | 8.2 → 7.7 | 17 → 19 |
| `F51` | H4 · X10 DAN X21 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 21.6 / 22.0 / **22.2** | 24.2 / 25.8 / 25.8 | 0.98 | 18 → 17 | 65 → 65 | 8.4 → 8.2 | 18 → 19 |
| `F50` | H4 · X00 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 27.5 / 27.5 / **27.5** | 34.3 / 34.3 / 34.3 | 0.98 | 26 → 25 | 58 → 59 | 11.3 → 11.5 | 18 → 18 |
| `F56` | H4 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 21.5 / 21.5 / **21.5** | 16.7 / 16.7 / 16.7 | 1.00 | 23 → 21 | 60 → 60 | 9.4 → 9.1 | 19 → 20 |
| `F39` | H3 · X09 DAN X21 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 21.0 / 20.7 / **22.5** | 23.1 / 23.1 / 24.8 | 0.84 | 33 → 29 | 51 → 54 | 10.6 → 10.7 | 16 → 16 |
| `F40` | H3 · X14 DAN X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 21.5 / 21.6 / **21.6** | 25.7 / 26.4 / 26.4 | 1.00 | 32 → 27 | 50 → 53 | 10.6 → 10.6 | 16 → 18 |
| `F58` | H3 · X12 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 22.3 / 19.9 / **20.5** | 28.6 / 26.5 / 26.5 | 0.96 | 36 → 29 | 47 → 49 | 11.0 → 10.7 | 15 → 18 |
| `F41` | H3 · X12 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 18.9 / 17.6 / **17.6** | 14.6 / 13.8 / 13.8 | 1.00 | 40 → 32 | 46 → 49 | 12.6 → 11.3 | 15 → 19 |
| `F45` | H4 · X12 DAN X19 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 16.2 / 16.2 / **16.2** | 17.5 / 18.0 / 18.0 | 1.00 | 27 → 26 | 54 → 54 | 11.2 → 11.0 | 19 → 20 |
| `F27` | H4 · X07 DAN X21 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 15.6 / 15.7 / **15.7** | 17.7 / 17.6 / 17.7 | 0.99 | 27 → 25 | 54 → 55 | 10.1 → 9.9 | 19 → 19 |
| `F03` | H4 · X20 DAN X21 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 18.1 / 17.7 / **17.7** | 20.3 / 19.4 / 19.4 | 0.98 | 28 → 28 | 54 → 54 | 12.1 → 12.0 | 19 → 19 |
| `F07` | H4 · X13 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 15.7 / 14.2 / **14.2** | 17.6 / 17.2 / 17.2 | 1.00 | 28 → 27 | 54 → 54 | 10.3 → 10.0 | 17 → 19 |
| `F11` | H4 · X04 DAN X12 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 15.2 / 15.2 / **15.3** | 16.8 / 16.8 / 16.8 | 0.99 | 25 → 23 | 56 → 57 | 9.4 → 9.3 | 19 → 19 |
| `F10` | H3 · X12 ATAU X19 | 4xATR14 · RSI14 > 75 ATAU RSI7 > 85 [aktif selepas +10%] | 12.1 / 13.5 / **13.5** | 10.9 / 13.3 / 13.3 | 0.98 | 30 → 27 | 45 → 51 | 10.2 → 9.9 | 15 → 19 |
| `F24` | H4 · X11 DAN X22 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.1 / 13.8 / **13.8** | 14.6 / 14.8 / 14.8 | 1.00 | 32 → 32 | 45 → 49 | 11.9 → 11.9 | 17 → 19 |
| `F42` | H3 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 15.1 / 15.1 / **15.1** | 11.5 / 11.5 / 11.5 | 1.00 | 31 → 27 | 52 → 54 | 10.8 → 10.3 | 18 → 20 |
| `F22` | H2 · X11 ATAU X21 | 4xATR14 · RSI7 > 85 [aktif selepas +10%] | 12.1 / 14.5 / **15.8** | 11.7 / 14.0 / 15.5 | 0.89 | 26 → 35 | 42 → 47 | 13.5 → 13.4 | 6 → 18 |
| `F16` | H4 · X21 DAN X22 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 13.3 / 13.5 / **15.1** | 16.2 / 16.6 / 19.2 | 0.89 | 28 → 28 | 53 → 54 | 11.3 → 11.1 | 18 → 18 |
| `F02` | H4 · X08 DAN X22 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.8 / 12.9 / **12.9** | 14.5 / 14.5 / 14.5 | 1.00 | 24 → 22 | 56 → 57 | 8.8 → 8.6 | 18 → 19 |
| `F60` | H3 · X12 DAN X22 | 5xATR14 · RSI14 > 80 ATAU RSI7 > 85 [aktif selepas +10%] | 13.2 / 13.1 / **13.8** | 14.5 / 14.8 / 15.7 | 0.87 | 35 → 31 | 48 → 49 | 13.1 → 13.0 | 17 → 19 |
| `F48` | H3 · X13 DAN X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.8 / 13.5 / **13.5** | 22.4 / 21.6 / 21.6 | 1.00 | 36 → 30 | 48 → 50 | 11.2 → 10.6 | 17 → 19 |
| `F44` | H3 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.4 / 13.4 / **13.4** | 14.7 / 14.7 / 14.7 | 1.00 | 37 → 32 | 47 → 48 | 14.1 → 13.9 | 18 → 20 |
| `F06` | H4 · X18 DAN X22 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 11.9 / 12.1 / **13.5** | 13.9 / 14.0 / 15.5 | 0.87 | 29 → 27 | 51 → 53 | 10.5 → 10.4 | 19 → 18 |
| `F29` | H2 · X21 DAN X22 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.9 / 12.8 / **12.8** | 11.3 / 11.5 / 11.5 | 1.00 | 51 → 33 | 39 → 49 | 12.9 → 12.4 | 13 → 19 |
| `F01` | H4 · X03 DAN X22 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.0 / 12.1 / **12.1** | 13.6 / 13.6 / 13.6 | 1.00 | 29 → 26 | 52 → 54 | 10.3 → 10.0 | 18 → 20 |
| `F25` | H4 · X22 DAN X24 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.4 / 12.9 / **12.9** | 13.0 / 13.5 / 13.5 | 1.00 | 35 → 33 | 45 → 48 | 12.7 → 12.4 | 17 → 19 |
| `F61` | H3 · X13 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.1 / 12.1 / **12.1** | 12.9 / 13.1 / 13.1 | 1.00 | 35 → 30 | 49 → 50 | 11.1 → 10.9 | 17 → 19 |
| `F05` | H4 · X14 DAN X22 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.7 / 11.9 / **11.9** | 12.9 / 12.9 / 12.9 | 1.00 | 30 → 28 | 51 → 52 | 10.5 → 10.4 | 18 → 19 |
| `F28` | H4 · X20 DAN X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.9 / 12.1 / **12.1** | 12.7 / 12.5 / 12.5 | 1.00 | 29 → 28 | 52 → 53 | 9.9 → 9.8 | 18 → 19 |
| `F09` | H4 · X14 DAN X22 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 11.8 / 12.1 / **14.0** | 14.3 / 14.7 / 17.2 | 0.91 | 30 → 28 | 49 → 52 | 11.3 → 11.1 | 18 → 18 |
| `F30` | H4 · X21 DAN X22 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 12.0 / 11.9 / **12.9** | 12.8 / 12.7 / 13.9 | 0.92 | 29 → 28 | 51 → 51 | 10.8 → 10.7 | 18 → 19 |
| `F08` | H4 · X18 DAN X22 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.2 / 11.4 / **11.4** | 12.9 / 12.9 / 12.9 | 1.00 | 30 → 28 | 51 → 51 | 10.5 → 10.5 | 19 → 19 |
| `F62` | H3 · X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 34.6 / 34.7 / **34.7** | 41.7 / 41.7 / 41.7 | 1.00 | 17 → 16 | 71 → 69 | 11.0 → 10.5 | 16 → 20 |
| `F52` | H4 · X12 DAN X20 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 20.0 / 19.9 / **19.9** | 6.5 / 6.5 / 6.5 | 1.00 | 21 → 20 | 61 → 61 | 9.2 → 9.0 | 19 → 20 |
| `F64` | H3 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 27.9 / 27.9 / **27.9** | 34.5 / 34.5 / 34.5 | 1.00 | 20 → 16 | 69 → 70 | 8.5 → 8.2 | 18 → 19 |
| `F67` | H2 · X20 DAN X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 24.6 / 27.8 / **27.8** | 39.1 / 43.6 / 43.6 | 1.00 | 34 → 16 | 57 → 70 | 11.9 → 8.5 | 15 → 20 |
| `F49` | H4 · X12 | 4xATR14 · RSI14 > 75 ATAU RSI7 > 85 [aktif selepas +10%] | 30.5 / 29.6 / **30.6** | 32.8 / 33.3 / 35.1 | 0.95 | 21 → 22 | 65 → 64 | 10.5 → 10.3 | 17 → 18 |
| `F57` | H3 · X12 | 4xATR14 · RSI14 > 75 ATAU RSI7 > 85 [aktif selepas +10%] | 21.2 / 21.8 / **22.9** | 11.8 / 13.7 / 13.7 | 0.95 | 19 → 18 | 70 → 70 | 7.6 → 7.7 | 17 → 19 |
| `F53` | H3 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 20.1 / 20.1 / **20.1** | 8.3 / 8.3 / 8.3 | 1.00 | 22 → 18 | 65 → 65 | 8.4 → 8.4 | 19 → 20 |
| `F55` | H4 · X10 DAN X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 24.9 / 24.9 / **24.9** | 33.0 / 34.0 / 34.0 | 1.00 | 12 → 10 | 73 → 74 | 8.3 → 8.0 | 19 → 20 |
| `F54` | H4 · X12 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 23.4 / 23.4 / **23.4** | 15.4 / 15.4 / 15.4 | 1.00 | 18 → 16 | 66 → 67 | 8.0 → 7.5 | 19 → 20 |
| `F68` | H3 · X20 DAN X21 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 19.7 / 19.9 / **19.9** | 16.7 / 16.7 / 16.7 | 1.00 | 28 → 21 | 58 → 60 | 9.0 → 8.6 | 18 → 19 |
| `F69` | H3 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 24.7 / 24.8 / **24.8** | 22.7 / 22.7 / 22.7 | 1.00 | 23 → 17 | 64 → 67 | 10.4 → 9.6 | 18 → 19 |
| `F66` | H3 · X00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 22.9 / 22.9 / **22.9** | 10.1 / 10.1 / 10.1 | 1.00 | 20 → 17 | 66 → 68 | 10.7 → 9.7 | 19 → 20 |
| `F15` | H4 · X04 DAN X12 | min(-10%, 4xATR14) · RSI14 > 75 ATAU RSI7 > 85 [aktif selepas +10%] | 16.0 / 16.1 / **16.3** | 10.8 / 10.8 / 11.2 | 0.99 | 25 → 25 | 56 → 56 | 10.0 → 10.0 | 19 → 19 |
| `F59` | H2 · X01 DAN X12 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 14.1 / 14.3 / **14.3** | 0.0 / 0.0 / 0.0 | 1.00 | 46 → 28 | 44 → 51 | 10.7 → 10.0 | 15 → 20 |
| `F23` | H2 · X12 DAN X16 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.5 / 14.7 / **14.7** | 9.5 / 11.2 / 11.2 | 1.00 | 58 → 37 | 34 → 46 | 15.9 → 14.7 | 11 → 19 |
| `F14` | H4 · X09 DAN X21 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 14.7 / 14.7 / **15.0** | 12.9 / 12.9 / 13.2 | 0.99 | 24 → 23 | 56 → 57 | 9.5 → 9.4 | 19 → 19 |
| `F12` | H4 · X12 ATAU X13 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 16.1 / 16.1 / **16.1** | 8.3 / 8.3 / 8.3 | 1.00 | 23 → 22 | 58 → 58 | 10.3 → 10.1 | 19 → 20 |
| `F18` | H4 · X13 DAN X21 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 14.2 / 14.2 / **14.3** | 14.2 / 14.2 / 14.3 | 0.99 | 26 → 24 | 55 → 55 | 9.6 → 9.4 | 19 → 19 |
| `F17` | H4 · X13 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 13.9 / 13.9 / **14.0** | 8.6 / 8.6 / 8.7 | 0.99 | 24 → 22 | 57 → 58 | 9.3 → 9.1 | 19 → 19 |
| `F26` | H4 · X12 ATAU X22 | 4xATR14 · RSI14 > 75 ATAU RSI7 > 85 [aktif selepas +10%] | 12.9 / 12.7 / **14.1** | 13.3 / 11.8 / 13.8 | 0.86 | 30 → 34 | 47 → 48 | 12.8 → 12.7 | 14 → 18 |
| `F46` | H3 · X04 DAN X12 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.4 / 11.7 / **11.7** | 18.6 / 18.6 / 18.6 | 1.00 | 26 → 22 | 55 → 57 | 8.3 → 8.0 | 18 → 20 |
| `F04` | H4 · X12 DAN X20 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 13.6 / 13.8 / **14.5** | 10.5 / 10.7 / 12.2 | 0.84 | 26 → 24 | 55 → 56 | 10.2 → 10.2 | 19 → 19 |
| `F21` | H2 · X09 ATAU X10 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 7.9 / 10.1 / **10.1** | 10.5 / 15.5 / 15.5 | 1.00 | 17 → 33 | 36 → 47 | 11.8 → 11.6 | 6 → 19 |
| `F47` | H3 · X04 DAN X12 | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 9.8 / 10.1 / **10.1** | 11.5 / 11.5 / 11.5 | 1.00 | 26 → 24 | 54 → 54 | 7.4 → 7.6 | 17 → 19 |
| `F19` | H4 · X14 DAN X23 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 5.3 / 5.6 / **5.6** | 6.3 / 7.9 / 7.9 | 1.00 | 15 → 15 | 57 → 60 | 5.6 → 5.5 | 18 → 19 |
| `F20` | H4 · X18 DAN X22 | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 6.5 / 6.5 / **6.8** | 4.9 / 4.9 / 6.3 | 0.85 | 18 → 17 | 58 → 60 | 6.0 → 6.0 | 19 → 19 |
| `F13` | H4 · X08 DAN X20 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 5.3 / 5.3 / **5.3** | 8.3 / 8.3 / 8.3 | 1.00 | 16 → 14 | 60 → 61 | 5.4 → 5.3 | 18 → 19 |
| `C01` | – | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | – / 17.4 / **18.5** | – / 20.0 / 20.0 | 0.89 | – → 18 | – → 60 | – → 7.1 | nan → 17 |
| `C02` | – | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 18.4 / **18.4** | – / 30.0 / 30.0 | 1.00 | – → 30 | – → 49 | – → 10.7 | nan → 19 |
| `C03` | – | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 18.5 / **18.5** | – / 20.2 / 20.2 | 1.00 | – → 28 | – → 53 | – → 10.8 | nan → 18 |
| `C04` | – | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 19.6 / **19.6** | – / 29.7 / 29.7 | 1.00 | – → 30 | – → 50 | – → 10.7 | nan → 19 |
| `C05` | – | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 20.0 / **20.0** | – / 21.7 / 21.7 | 1.00 | – → 27 | – → 54 | – → 10.7 | nan → 18 |
| `C06` | – | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | – / 15.7 / **16.5** | – / 21.4 / 21.4 | 0.88 | – → 18 | – → 59 | – → 7.0 | nan → 18 |
| `C07` | – | -15% · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | – / 14.6 / **14.6** | – / 12.0 / 12.0 | 0.95 | – → 20 | – → 54 | – → 6.5 | nan → 18 |
| `C08` | – | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 12.6 / **12.6** | – / 16.7 / 16.7 | 1.00 | – → 22 | – → 49 | – → 6.5 | nan → 16 |
| `C09` | – | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 13.1 / **13.1** | – / 20.8 / 20.8 | 1.00 | – → 32 | – → 44 | – → 10.2 | nan → 18 |
| `C10` | – | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 16.6 / **16.6** | – / 19.4 / 19.4 | 1.00 | – → 25 | – → 52 | – → 8.7 | nan → 18 |
| `C11` | – | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | – / 12.9 / **12.9** | – / 0.0 / 0.0 | 1.00 | – → 20 | – → 55 | – → 6.1 | nan → 16 |
| `C12` | – | -15% · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | – / 14.6 / **14.6** | – / 12.5 / 12.5 | 0.96 | – → 20 | – → 54 | – → 6.4 | nan → 18 |

## 5. Kaveat

- Keluar dipilih pada kumpulan A daripada ratusan ribu calon; angka A melambung, angka B yang dibaca. Kumpulan B sudah dilihat dalam pusingan terdahulu.
- Henti yang lebih longgar menaikkan tangkap penuh kerana lebih sedikit dagangan terhenti sebelum sampai +10 %, tetapi rugi besar setiap dagangan yang gagal turut lebih besar.
- Tiada saham delist. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.
