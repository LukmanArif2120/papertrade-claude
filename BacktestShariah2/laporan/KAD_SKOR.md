# Kad skor keputusan (satu jawapan)

Dijana 2026-11-07 oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate dipradaftar 2026-11-06 dalam `standard/SPEC_KAD_SKOR.md`. Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Tiada kaedah lulus. Keputusan paling awal: lift 2 mata ~2026-12-31, portfolio lawan SPUS ~2027-04-09

Penyebut: 64,010 posisi Lejar Penuh lorong 1 merentas 223 kaedah, 16 hari beli, yang terbuka ditanda-ke-pasaran pada tutup 2026-11-06.

| Status | Bilangan |
|---|---|
| NEGATIF | 8 |
| GAGAL | 0 |
| BELUM CUKUP | 215 |
| CALON | 0 |
| TERBUKTI | 0 |

## Kematangan (G1)

SD setiap posisi (median dalam-kaedah) 8.72 mata → **597** posisi ditutup untuk beza 1 mata; ATAU **55** hari beli untuk lift 2 mata (ada 16); DAN hari beli ≥ 20. Lorong T4 paling lama: 16 / 126 sesi.

## 20 kaedah teratas ikut lift (calon, BUKAN pangkat sehingga status berubah)

| Kaedah | Status | n / tutup | Hari beli | Jangkaan % [95%] | Lift | Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 vs SPUS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `M15` Break & Retest + Henti ATR | BELUM CUKUP | 254 / 138 | 16 | +0.59 [-0.69, +1.86] | +2.47 | 44 | 1.57 | -0.53 | 4 | 16 | +2.30 |
| `M153` Range Leader | BELUM CUKUP | 1040 / 855 | 16 | -0.35 [-1.56, +0.87] | +2.38 | 43 | 1.16 | -1.40 | 6 | 16 | +2.14 |
| `M73` ADX(5) > 40 + Julat Terkecil | BELUM CUKUP | 644 / 550 | 16 | -0.64 [-2.11, +0.82] | +2.38 | 62 | 0.46 | -1.30 | 0 | 16 | -2.23 |
| `M133` Bull Hook (Crabel) | BELUM CUKUP | 38 / 19 | 11 | +1.69 [-1.33, +4.70] | +2.37 | 53 | 1.85 | +0.56 | 1 | 16 | +11.20 |
| `M100` Bulkowski Segi Empat & Segi  | BELUM CUKUP | 58 / 37 | 14 | -0.36 [-4.22, +3.50] | +2.34 | 40 | 1.36 | -1.03 | 0 | 16 | +8.72 |
| `M159` Heikin-Ashi Trend | BELUM CUKUP | 1397 / 1103 | 16 | -0.67 [-1.67, +0.32] | +2.10 | 39 | 1.17 | -1.63 | 13 | 16 | +8.64 |
| `M18` EMA9/21 Pullback | BELUM CUKUP | 271 / 202 | 16 | -0.12 [-1.14, +0.91] | +2.08 | 31 | 2.12 | -1.12 | 60 | 16 | -0.25 |
| `M33` Supertrend + SMA10 | BELUM CUKUP | 195 / 35 | 16 | +0.93 [-1.24, +3.10] | +2.07 | 53 | 1.14 | -0.24 | 1 | 16 | +13.67 |
| `M03` BB Break + Divergence RSI | BELUM CUKUP | 324 / 282 | 16 | -1.01 [-2.54, +0.52] | +2.01 | 52 | 0.59 | -1.78 | 11 | 16 | +3.27 |
| `M92` CCI-50 | BELUM CUKUP | 458 / 264 | 16 | -0.54 [-1.92, +0.85] | +1.91 | 42 | 1.18 | -1.72 | 15 | 16 | +4.79 |
| `M116` 2/20 EMA Breakout (Landry) | BELUM CUKUP | 508 / 318 | 16 | -0.52 [-2.04, +1.00] | +1.86 | 48 | 0.92 | -1.53 | 5 | 16 | +1.90 |
| `M118` Expansion Pivot (Cooper) | BELUM CUKUP | 69 / 19 | 16 | -0.19 [-2.90, +2.53] | +1.79 | 46 | 1.08 | -1.39 | 1 | 16 | +14.47 |
| `M106` DMI Wilder | BELUM CUKUP | 100 / 50 | 14 | -0.69 [-3.10, +1.71] | +1.68 | 42 | 1.07 | -1.67 | 0 | 16 | +2.28 |
| `M146` 3-Bar Momentum Pattern | BELUM CUKUP | 76 / 27 | 16 | +0.70 [-0.73, +2.13] | +1.68 | 57 | 1.00 | -0.20 | 4 | 16 | +9.05 |
| `M124` 'Last' Stochastic Technique  | BELUM CUKUP | 328 / 156 | 16 | -0.42 [-2.43, +1.58] | +1.62 | 42 | 1.22 | -1.63 | 16 | 16 | +9.12 |
| `M151` Outside Bar Failure | BELUM CUKUP | 81 / 44 | 15 | -0.43 [-2.91, +2.05] | +1.54 | 32 | 1.80 | -1.88 | 11 | 16 | +12.13 |
| `M35` Pocket Pivot Morales & Kache | BELUM CUKUP | 281 / 191 | 16 | -0.59 [-1.86, +0.68] | +1.51 | 26 | 2.24 | -1.73 | 68 | 16 | +0.81 |
| `M158` Doubly Adaptive Profit Targe | BELUM CUKUP | 330 / 111 | 16 | +0.12 [-1.60, +1.84] | +1.44 | 43 | 1.36 | -1.25 | 2 | 16 | +3.67 |
| `M20` EMA10/15 Crossover + Sudut | BELUM CUKUP | 369 / 316 | 16 | -1.57 [-2.89, -0.24] | +1.42 | 29 | 1.37 | -2.42 | 66 | 16 | +2.04 |
| `M117` Landry Pullback (high 2 bula | BELUM CUKUP | 81 / 17 | 14 | -0.00 [-3.62, +3.61] | +1.38 | 41 | 1.45 | -1.70 | 1 | 16 | -0.14 |

## Cara membaca

- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.** CALON bermaksud setiap dagangan lulus tetapi portfolio belum terbukti mengalahkan SPUS; `REVERSE/KEPUTUSAN_AKHIR.md` mengukur bahawa kohort setiap dagangan yang lulus pernah gagal 0/36 sebagai portfolio.
- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif; `X3` menang 30.2% dengan jangkaan +2.595% (`REVERSE/KOMBINASI.md`).
- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan (`REVERSE/KOLAM_EKOR.md`) dan memerlukan banyak posisi untuk ditangkap.
- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.

