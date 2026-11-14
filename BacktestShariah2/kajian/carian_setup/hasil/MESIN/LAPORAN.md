# Mesin carian setup — papan terkumpul (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_mesin.py` (workflow `mesin_carian.yml`). Peraturan dikunci dalam `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(c). **Jangan sunting secara manual; `papan.csv` tambah-sahaja.**

- Larian setakat ini: **2** (terakhir 2026-11-14); varian berskor terkumpul: **817** (235 kaedah M, 582 keluarga indikator).
- Skor A > 0: 724. Dinilai pada saham tidak dilihat (15 terbaik setiap larian): 30; mengatasi rawak dalam K1, K2 DAN K3 dengan belian ≥ 300: **26**.
- Skor A = min dua era carian bagi [kelebihan kadar "naik lagi" atas saham rawak hari sama − 2 ralat piawai]. Semakin banyak varian dicuba, semakin melambung skor A terbaik; lajur B yang dibaca.

## 30 teratas ikut skor A (maks 2 setiap induk)

| # | Larian | Pencetus | Prasyarat | Penapis saham | Skor A (mata) | Belian B | Naik lagi B % (rawak) | Kelebihan K1 / K2 / K3 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | `M50.1001` kaedah M50 (varian rawak) | QA08+QF01 | F08 RSI14 > 50 DAN F20 >= 30% di bawah puncak 52 minggu | +8.4 | 421 | 17.8 (10.5) | +11.2 / +3.2 / +8.7 |
| 2 | 1 | `K09.r1_5` MACD(13,28,6) silang naik bawah sifar | QC03+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F08 RSI14 > 50 | +8.2 | 300 | 13.3 (6.6) | +5.1 / +8.9 / +8.7 |
| 3 | 1 | `K13.r1_8` Stochastic(14) silang naik dari bawah 37 | QH08+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +7.5 | 344 | 16.9 (7.2) | +11.8 / +4.8 / +14.3 |
| 4 | 2 | `K13.r2_10` Stochastic(12) silang naik dari bawah 39 | QA01+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.9 | 395 | 14.9 (6.9) | +10.5 / +1.7 / +11.9 |
| 5 | 1 | `K19.r1_6` pecah atas Keltner(34, 1.4) | QC01+QF01 | F17 RS >= 90 DAN F19 dalam 5% dari puncak 52 minggu | +6.5 | 444 | 11.3 (6.1) | +2.6 / +8.3 / +13.0 |
| 6 | 2 | `K17.r2_1` undur ke ema48 yang naik (tol 1.9%) | QC05+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.5 | 545 | 13.2 (7.1) | +6.8 / +2.0 / +14.2 |
| 7 | 2 | `K05.r2_10` tutup silang atas jalur atas BB(9, 1.87) | QC03+QF01 | F17 RS >= 90 DAN F29 tutup dalam 25% teratas julat hari | +6.4 | 379 | 11.6 (7.2) | +1.4 / +5.9 / +18.5 |
| 8 | 2 | `K07.r2_5` tutup silang atas ema35 | QC05+QF01 | F17 RS >= 90 DAN F29 tutup dalam 25% teratas julat hari | +6.4 | 377 | 15.1 (8.3) | +6.4 / +5.6 / +13.0 |
| 9 | 1 | `K05.r1_6` tutup silang atas jalur atas BB(11, 1.27) | QH02+QF01 | F18 dalam 15% dari puncak 52 minggu DAN F29 tutup dalam 25% teratas julat hari | +6.3 | 752 | 9.8 (4.2) | +5.8 / +5.5 / -2.6 |
| 10 | 1 | `K17.r1_9` undur ke ema52 yang naik (tol 2.6%) | QA05+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.3 | 310 | 15.5 (9.3) | +6.0 / +7.5 / +4.5 |
| 11 | 2 | `K19.r2_1` pecah atas Keltner(35, 1.0) | QG03+QF01 | F15 Supertrend naik DAN F17 RS >= 90 | +6.3 | 331 | 15.7 (10.0) | +5.6 / +5.4 / +7.9 |
| 12 | 1 | `K02.r1_9` RSI(7) silang atas 64 | QH02+QF01 | F11 MACD > isyarat DAN F30 hari naik (tutup > buka) | +6.2 | 856 | 13.1 (5.6) | +7.4 / +8.5 / +7.0 |
| 13 | 1 | `K07.r1_3` tutup silang atas sma50 | QC03+QF01 | F06 MA50 naik (lawan 20 bar lalu) | +6.2 | 882 | 13.5 (6.5) | +5.9 / +8.9 / +5.3 |
| 14 | 1 | `M125.1001` kaedah M125 (varian rawak) | QH02+QF01 | F14 ADX < 20 | +6.2 | 751 | 13.8 (5.0) | +8.9 / +9.7 / -4.8 |
| 15 | 2 | `K02.r2_9` RSI(6) silang atas 60 | QA03+QF01 | F02 tutup > MA50 DAN F20 >= 30% di bawah puncak 52 minggu | +6.2 | 1,150 | 13.8 (9.3) | +5.2 / +4.1 / +4.2 |
| 16 | 2 | `K24.r2_4` bar pembalikan (buka <= 21%, tutup >= 83% julat) | QA11+QF01 | F11 MACD > isyarat DAN F22 volum 10 hari > volum 50 hari | +6.1 | 872 | 14.3 (8.8) | +7.6 / +1.7 / +15.0 |
| 17 | 2 | `M18.1002` kaedah M18 (varian rawak) | QH04+QF01 | F08 RSI14 > 50 DAN F11 MACD > isyarat | +6.1 | 637 | 15.5 (8.8) | +7.0 / +3.7 / +9.9 |
| 18 | 1 | `M159.1001` kaedah M159 (varian rawak) | QH02+QF01 | F14 ADX < 20 DAN F30 hari naik (tutup > buka) | +6.0 | 678 | 11.2 (5.2) | +5.9 / +7.0 / -3.8 |
| 19 | 1 | `K06.r1_3` 2 tutup menurun berturut | QA08+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.0 | – | – | – |
| 20 | 1 | `K06.r1_5` 2 tutup menurun berturut | QA08+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.0 | – | – | – |
| 21 | 1 | `M20.1001` kaedah M20 (varian rawak) | QA11+QF01 | F16 RS >= 70 DAN F18 dalam 15% dari puncak 52 minggu | +6.0 | – | – | – |
| 22 | 1 | `K21.r1_7` NR3 | QH02+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F11 MACD > isyarat | +6.0 | – | – | – |
| 23 | 1 | `K21.r1_9` NR3 | QH02+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F11 MACD > isyarat | +6.0 | – | – | – |
| 24 | 1 | `K10.r1_6` pecah tinggi 10 hari | QH02+QF01 | F02 tutup > MA50 DAN F11 MACD > isyarat | +5.9 | – | – | – |
| 25 | 1 | `K24.r1_12` bar pembalikan (buka <= 16%, tutup >= 78% julat) | QC05+QF01 | F07 templat trend Minervini DAN F17 RS >= 90 | +5.9 | – | – | – |
| 26 | 2 | `M124.1002` kaedah M124 (varian rawak) | QA11+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F30 hari naik (tutup > buka) | +5.9 | 363 | 12.1 (6.0) | +6.9 / +6.1 / +3.1 |
| 27 | 2 | `M14.1002` kaedah M14 (varian rawak) | QC04+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +5.9 | 1,954 | 13.5 (6.7) | +7.6 / +5.7 / +5.1 |
| 28 | 1 | `M14.1001` kaedah M14 (varian rawak) | QC04+QF01 | F07 templat trend Minervini DAN F17 RS >= 90 | +5.8 | – | – | – |
| 29 | 2 | `M102.1002` kaedah M102 (varian rawak) | QH09+QF01 | F14 ADX < 20 DAN F16 RS >= 70 | +5.8 | – | – | – |
| 30 | 2 | `M161.1002` kaedah M161 (varian rawak) | QH02+QF01 | F04 MA20 > MA50 DAN F12 MACD > 0 | +5.7 | – | – | – |

## Setiap larian

| Larian | Tarikh | Varian berskor | Skor A > 0 | Skor A terbaik | Dinilai pada B | Bertahan K1–K3 |
|---|---|---|---|---|---|---|
| 1 | 2026-11-14 | 409 | 358 | +8.4 | 15 | 12 |
| 2 | 2026-11-14 | 408 | 366 | +6.9 | 15 | 14 |

Kaveat: kumpulan B sudah dilihat berkali-kali (bukan tahanan bersih); tiada saham delist; setup di sini BUKAN calon papertrade tanpa keputusan pengguna berasingan.
