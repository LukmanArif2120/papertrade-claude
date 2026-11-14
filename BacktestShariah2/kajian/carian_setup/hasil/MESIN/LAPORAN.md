# Mesin carian setup — papan terkumpul (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_mesin.py` (workflow `mesin_carian.yml`). Peraturan dikunci dalam `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (n)(c). **Jangan sunting secara manual; `papan.csv` tambah-sahaja.**

- Larian setakat ini: **1** (terakhir 2026-11-14); varian berskor terkumpul: **409** (118 kaedah M, 291 keluarga indikator).
- Skor A > 0: 358. Dinilai pada saham tidak dilihat (15 terbaik setiap larian): 15; mengatasi rawak dalam K1, K2 DAN K3 dengan belian ≥ 300: **12**.
- Skor A = min dua era carian bagi [kelebihan kadar "naik lagi" atas saham rawak hari sama − 2 ralat piawai]. Semakin banyak varian dicuba, semakin melambung skor A terbaik; lajur B yang dibaca.

## 30 teratas ikut skor A (maks 2 setiap induk)

| # | Larian | Pencetus | Prasyarat | Penapis saham | Skor A (mata) | Belian B | Naik lagi B % (rawak) | Kelebihan K1 / K2 / K3 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | `M50.1001` kaedah M50 (varian rawak) | QA08+QF01 | F08 RSI14 > 50 DAN F20 >= 30% di bawah puncak 52 minggu | +8.4 | 421 | 17.8 (10.5) | +11.2 / +3.2 / +8.7 |
| 2 | 1 | `K09.r1_5` MACD(13,28,6) silang naik bawah sifar | QC03+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F08 RSI14 > 50 | +8.2 | 300 | 13.3 (6.6) | +5.1 / +8.9 / +8.7 |
| 3 | 1 | `K13.r1_8` Stochastic(14) silang naik dari bawah 37 | QH08+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +7.5 | 344 | 16.9 (7.2) | +11.8 / +4.8 / +14.3 |
| 4 | 1 | `K13.r1_10` Stochastic(14) silang naik dari bawah 40 | QH08+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +6.8 | 382 | 15.7 (7.2) | +10.2 / +4.2 / +12.4 |
| 5 | 1 | `K19.r1_6` pecah atas Keltner(34, 1.4) | QC01+QF01 | F17 RS >= 90 DAN F19 dalam 5% dari puncak 52 minggu | +6.5 | 444 | 11.3 (6.1) | +2.6 / +8.3 / +13.0 |
| 6 | 1 | `K05.r1_6` tutup silang atas jalur atas BB(11, 1.27) | QH02+QF01 | F18 dalam 15% dari puncak 52 minggu DAN F29 tutup dalam 25% teratas julat hari | +6.3 | 752 | 9.8 (4.2) | +5.8 / +5.5 / -2.6 |
| 7 | 1 | `K17.r1_9` undur ke ema52 yang naik (tol 2.6%) | QA05+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.3 | 310 | 15.5 (9.3) | +6.0 / +7.5 / +4.5 |
| 8 | 1 | `K02.r1_9` RSI(7) silang atas 64 | QH02+QF01 | F11 MACD > isyarat DAN F30 hari naik (tutup > buka) | +6.2 | 856 | 13.1 (5.6) | +7.4 / +8.5 / +7.0 |
| 9 | 1 | `K07.r1_3` tutup silang atas sma50 | QC03+QF01 | F06 MA50 naik (lawan 20 bar lalu) | +6.2 | 882 | 13.5 (6.5) | +5.9 / +8.9 / +5.3 |
| 10 | 1 | `M125.1001` kaedah M125 (varian rawak) | QH02+QF01 | F14 ADX < 20 | +6.2 | 751 | 13.8 (5.0) | +8.9 / +9.7 / -4.8 |
| 11 | 1 | `K19.r1_5` pecah atas Keltner(12, 1.3) | QH02+QF01 | F02 tutup > MA50 DAN F11 MACD > isyarat | +6.1 | 836 | 12.1 (5.1) | +6.5 / +7.7 / +20.7 |
| 12 | 1 | `K05.r1_2` tutup silang atas jalur atas BB(10, 1.03) | QH02+QF01 | F15 Supertrend naik DAN F29 tutup dalam 25% teratas julat hari | +6.1 | 896 | 9.8 (5.1) | +4.8 / +3.9 / +12.4 |
| 13 | 1 | `K02.r1_12` RSI(23) silang atas 51 | QA05+QF01 | F20 >= 30% di bawah puncak 52 minggu DAN F30 hari naik (tutup > buka) | +6.1 | 659 | 15.6 (9.0) | +8.3 / +5.9 / +4.0 |
| 14 | 1 | `M159.1001` kaedah M159 (varian rawak) | QH02+QF01 | F14 ADX < 20 DAN F30 hari naik (tutup > buka) | +6.0 | 678 | 11.2 (5.2) | +5.9 / +7.0 / -3.8 |
| 15 | 1 | `K06.r1_3` 2 tutup menurun berturut | QA08+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.0 | – | – | – |
| 16 | 1 | `K06.r1_5` 2 tutup menurun berturut | QA08+QF01 | F14 ADX < 20 DAN F20 >= 30% di bawah puncak 52 minggu | +6.0 | – | – | – |
| 17 | 1 | `M20.1001` kaedah M20 (varian rawak) | QA11+QF01 | F16 RS >= 70 DAN F18 dalam 15% dari puncak 52 minggu | +6.0 | – | – | – |
| 18 | 1 | `K21.r1_7` NR3 | QH02+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F11 MACD > isyarat | +6.0 | – | – | – |
| 19 | 1 | `K21.r1_9` NR3 | QH02+QF01 | F06 MA50 naik (lawan 20 bar lalu) DAN F11 MACD > isyarat | +6.0 | – | – | – |
| 20 | 1 | `K10.r1_6` pecah tinggi 10 hari | QH02+QF01 | F02 tutup > MA50 DAN F11 MACD > isyarat | +5.9 | – | – | – |
| 21 | 1 | `K24.r1_12` bar pembalikan (buka <= 16%, tutup >= 78% julat) | QC05+QF01 | F07 templat trend Minervini DAN F17 RS >= 90 | +5.9 | – | – | – |
| 22 | 1 | `K24.r1_8` bar pembalikan (buka <= 13%, tutup >= 82% julat) | QC01+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +5.9 | – | – | – |
| 23 | 1 | `M14.1001` kaedah M14 (varian rawak) | QC04+QF01 | F07 templat trend Minervini DAN F17 RS >= 90 | +5.8 | – | – | – |
| 24 | 1 | `K17.r1_2` undur ke ema52 yang naik (tol 1.7%) + atas MA200 | QA03+QF01 | F16 RS >= 70 DAN F18 dalam 15% dari puncak 52 minggu | +5.8 | – | – | – |
| 25 | 1 | `M78.1001` kaedah M78 (varian rawak) | QC04+QF01 | F09 RSI14 > 60 DAN F17 RS >= 90 | +5.7 | – | – | – |
| 26 | 1 | `K11.r1_12` Supertrend(12, 1.2) bertukar naik | QC05+QF01 | F17 RS >= 90 DAN F18 dalam 15% dari puncak 52 minggu | +5.7 | – | – | – |
| 27 | 1 | `K22.r1_11` Holy Grail (ADX > 24, undur EMA18) | QG02+QF01 | F25 squeeze hidup | +5.7 | – | – | – |
| 28 | 1 | `M02.1001` kaedah M02 (varian rawak) | QC03+QF01 | F05 MA50 > MA200 DAN F14 ADX < 20 | +5.7 | – | – | – |
| 29 | 1 | `K09.r1_2` MACD(20,45,18) silang naik | QG01+QF01 | F07 templat trend Minervini DAN F12 MACD > 0 | +5.7 | – | – | – |
| 30 | 1 | `M18.1001` kaedah M18 (varian rawak) | QA09+QF01 | F04 MA20 > MA50 DAN F25 squeeze hidup | +5.7 | – | – | – |

## Setiap larian

| Larian | Tarikh | Varian berskor | Skor A > 0 | Skor A terbaik | Dinilai pada B | Bertahan K1–K3 |
|---|---|---|---|---|---|---|
| 1 | 2026-11-14 | 409 | 358 | +8.4 | 15 | 12 |

Kaveat: kumpulan B sudah dilihat berkali-kali (bukan tahanan bersih); tiada saham delist; setup di sini BUKAN calon papertrade tanpa keputusan pengguna berasingan.
