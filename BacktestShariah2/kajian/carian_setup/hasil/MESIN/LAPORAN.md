# Mesin carian setup — papan terkumpul (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_mesin.py` (workflow `mesin_carian.yml`). Peraturan dikunci dalam `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(c). **Jangan sunting secara manual; `papan.csv` tambah-sahaja.**

- Larian setakat ini: **4** (terakhir 2026-11-15); varian berskor terkumpul: **1,654** (484 kaedah M, 1,170 keluarga indikator).
- Skor A > 0: 1,468. Dinilai pada saham tidak dilihat (15 terbaik setiap larian): 60; mengatasi rawak dalam K1, K2 DAN K3 dengan belian ≥ 300: **54**.
- Skor A = min dua era carian bagi [kelebihan kadar "naik lagi" atas saham rawak hari sama − 2 ralat piawai]. Semakin banyak varian dicuba, semakin melambung skor A terbaik; lajur B yang dibaca.

## 30 teratas ikut skor A (maks 2 setiap induk)

| # | Larian | Pencetus | Prasyarat | Penapis saham | Skor A (mata) | Belian B | Naik lagi B % (rawak) | Kelebihan K1 / K2 / K3 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | `M50.1001` kaedah M50 (varian rawak) | QA08+QF01 | F08 RSI14 > 50 DAN F20 >= 30% di bawah puncak 52 minggu | +8.4 | 421 | 17.8 (10.5) | +11.2 / +3.2 / +8.7 |
| 2 | 1 | `K09.r1_5` MACD(13,28,6) silang naik bawah sifar | QC03+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F08 RSI14 > 50 | +8.2 | 300 | 13.3 (6.6) | +5.1 / +8.9 / +8.7 |
| 3 | 1 | `K13.r1_8` Stochastic(14) silang naik dari bawah 37 | QH08+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +7.5 | 344 | 16.9 (7.2) | +11.8 / +4.8 / +14.3 |
| 4 | 4 | `K11.r4_2` Supertrend(22, 1.6) bertukar naik | QA01+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +7.1 | 327 | 10.4 (7.2) | +3.7 / +2.1 / +4.0 |
| 5 | 3 | `M111.1003` kaedah M111 (varian rawak) | QA05+QF01 | F17 RS >= 90 DAN F30 hari naik (tutup > buka) | +7.0 | 394 | 12.2 (7.5) | +4.7 / +3.6 / +8.0 |
| 6 | 4 | `K11.r4_6` Supertrend(7, 1.1) bertukar naik | QA01+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.9 | 550 | 11.6 (6.9) | +4.0 / +4.4 / +9.0 |
| 7 | 2 | `K13.r2_10` Stochastic(12) silang naik dari bawah 39 | QA01+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.9 | 395 | 14.9 (6.9) | +10.5 / +1.7 / +11.9 |
| 8 | 3 | `K19.r3_4` pecah atas Keltner(30, 1.2) | QG03+QF01 | F15 Supertrend naik DAN F17 RS >= 90 | +6.8 | 378 | 14.3 (9.4) | +5.3 / +5.2 / +1.7 |
| 9 | 3 | `K02.r3_3` RSI(5) silang atas 56 | QA05+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F20 >= 30% di bawah puncak 52 minggu | +6.7 | 498 | 13.9 (9.5) | +6.7 / +3.5 / +3.2 |
| 10 | 4 | `K19.r4_6` pecah atas Keltner(33, 1.0) | QG03+QF01 | F15 Supertrend naik DAN F17 RS >= 90 | +6.7 | 340 | 15.3 (10.2) | +5.2 / +5.2 / +4.6 |
| 11 | 3 | `K05.r3_7` tutup silang atas jalur atas BB(10, 1.9) | QC03+QF01 | F17 RS >= 90 DAN F29 tutup dalam 25% teratas julat hari | +6.7 | 371 | 10.5 (7.3) | +0.7 / +5.1 / +11.4 |
| 12 | 4 | `K09.r4_9` MACD(11,30,15) silang naik | QC05+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.6 | 359 | 14.8 (9.1) | +6.9 / +6.4 / +1.3 |
| 13 | 4 | `K24.r4_3` bar pembalikan (buka <= 13%, tutup >= 79% julat) | QC05+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.6 | 851 | 11.2 (6.5) | +4.3 / +5.7 / +3.7 |
| 14 | 3 | `K02.r3_11` RSI(3) silang atas 65 | QH02+QF01 | F11 MACD > isyarat DAN F15 Supertrend naik | +6.6 | 888 | 10.9 (5.4) | +5.3 / +5.6 / +22.2 |
| 15 | 3 | `M14.1003` kaedah M14 (varian rawak) | QC04+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.6 | 1,952 | 14.1 (6.7) | +8.4 / +6.7 / +4.0 |
| 16 | 4 | `M125.1004` kaedah M125 (varian rawak) | QH02+QF01 | F09 RSI14 > 60 DAN F11 MACD > isyarat | +6.5 | 899 | 10.6 (4.7) | +6.0 / +5.4 / -3.6 |
| 17 | 2 | `K17.r2_1` undur ke ema48 yang naik (tol 1.9%) | QC05+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.5 | 545 | 13.2 (7.1) | +6.8 / +2.0 / +14.2 |
| 18 | 3 | `K05.r3_10` tutup silang atas jalur atas BB(59, 1.33) | QB03+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.5 | 599 | 13.5 (7.0) | +6.5 / +8.1 / +1.4 |
| 19 | 4 | `K17.r4_7` undur ke ema107 yang naik (tol 2.5%) | QC03+QF01 | F14 ADX < 20 DAN F16 RS >= 70 | +6.4 | 398 | 15.1 (8.7) | +4.2 / +9.5 / +1.6 |
| 20 | 3 | `K24.r3_9` bar pembalikan (buka <= 11%, tutup >= 85% julat) | QC01+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.4 | 447 | 10.1 (6.4) | +1.4 / +7.3 / +5.6 |
| 21 | 2 | `K07.r2_5` tutup silang atas ema35 | QC05+QF01 | F17 RS >= 90 DAN F29 tutup dalam 25% teratas julat hari | +6.4 | 377 | 15.1 (8.3) | +6.4 / +5.6 / +13.0 |
| 22 | 3 | `K07.r3_3` tutup silang atas ema33 | QC05+QF01 | F02 tutup > MA50 DAN F17 RS >= 90 | +6.3 | 457 | 13.8 (7.9) | +5.2 / +6.6 / +7.1 |
| 23 | 4 | `K01.r4_8` RSI(3) < 21 | QA09+QF01 | F05 MA50 > MA200 DAN F14 ADX < 20 | +6.3 | 966 | 15.3 (8.2) | +6.5 / +7.2 / +11.5 |
| 24 | 4 | `K01.r4_10` RSI(12) < 43 | QA09+QF01 | F15 Supertrend naik DAN F18 dalam 15% dari puncak 52 minggu | +6.3 | 367 | 16.3 (7.6) | +7.0 / +9.9 / +17.4 |
| 25 | 3 | `M159.1003` kaedah M159 (varian rawak) | QH02+QF01 | F14 ADX < 20 DAN F30 hari naik (tutup > buka) | +6.3 | 659 | 10.3 (5.2) | +5.3 / +4.9 / -3.8 |
| 26 | 1 | `M125.1001` kaedah M125 (varian rawak) | QH02+QF01 | F14 ADX < 20 | +6.2 | 751 | 13.8 (5.0) | +8.9 / +9.7 / -4.8 |
| 27 | 3 | `M13.1003` kaedah M13 (varian rawak) | QC03+QF01 | F09 RSI14 > 60 DAN F18 dalam 15% dari puncak 52 minggu | +6.1 | – | – | – |
| 28 | 4 | `M13.1004` kaedah M13 (varian rawak) | QC03+QF01 | F09 RSI14 > 60 DAN F18 dalam 15% dari puncak 52 minggu | +6.1 | – | – | – |
| 29 | 3 | `M02.1003` kaedah M02 (varian rawak) | QC03+QF01 | F18 dalam 15% dari puncak 52 minggu DAN F30 hari naik (tutup > buka) | +6.1 | – | – | – |
| 30 | 2 | `M18.1002` kaedah M18 (varian rawak) | QH04+QF01 | F08 RSI14 > 50 DAN F11 MACD > isyarat | +6.1 | 637 | 15.5 (8.8) | +7.0 / +3.7 / +9.9 |

## Setiap larian

| Larian | Tarikh | Varian berskor | Skor A > 0 | Skor A terbaik | Dinilai pada B | Bertahan K1–K3 |
|---|---|---|---|---|---|---|
| 1 | 2026-11-14 | 409 | 358 | +8.4 | 15 | 12 |
| 2 | 2026-11-14 | 408 | 366 | +6.9 | 15 | 14 |
| 3 | 2026-11-15 | 419 | 370 | +7.0 | 15 | 14 |
| 4 | 2026-11-15 | 418 | 374 | +7.1 | 15 | 14 |

Kaveat: kumpulan B sudah dilihat berkali-kali (bukan tahanan bersih); tiada saham delist; setup di sini BUKAN calon papertrade tanpa keputusan pengguna berasingan.
