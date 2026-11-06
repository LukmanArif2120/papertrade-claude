# Kad skor keputusan (satu jawapan)

Dijana 2026-11-06 oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate dipradaftar 2026-11-06 dalam `standard/SPEC_KAD_SKOR.md`. Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Tiada kaedah lulus. Keputusan paling awal: lift 2 mata ~2027-01-06, portfolio lawan SPUS ~2027-04-09

Penyebut: 62,018 posisi Lejar Penuh lorong 1 merentas 222 kaedah, 15 hari beli, yang terbuka ditanda-ke-pasaran pada tutup 2026-11-05.

| Status | Bilangan |
|---|---|
| NEGATIF | 10 |
| GAGAL | 0 |
| BELUM CUKUP | 212 |
| CALON | 0 |
| TERBUKTI | 0 |

## Kematangan (G1)

SD setiap posisi (median dalam-kaedah) 8.82 mata → **610** posisi ditutup untuk beza 1 mata; ATAU **59** hari beli untuk lift 2 mata (ada 15); DAN hari beli ≥ 20. Lorong T4 paling lama: 15 / 126 sesi.

## 20 kaedah teratas ikut lift (calon, BUKAN pangkat sehingga status berubah)

| Kaedah | Status | n / tutup | Hari beli | Jangkaan % [95%] | Lift | Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 vs SPUS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `M133` Bull Hook (Crabel) | BELUM CUKUP | 38 / 18 | 11 | +2.32 [-0.90, +5.54] | +2.59 | 58 | 1.91 | +0.93 | 1 | 15 | +11.67 |
| `M15` Break & Retest + Henti ATR | BELUM CUKUP | 249 / 120 | 15 | +0.95 [-0.56, +2.46] | +2.52 | 45 | 1.68 | -0.18 | 4 | 15 | +3.34 |
| `M33` Supertrend + SMA10 | BELUM CUKUP | 186 / 31 | 15 | +1.58 [-0.82, +3.98] | +2.40 | 55 | 1.28 | +0.33 | 1 | 15 | +15.60 |
| `M80` Radge Saluran Purata Bergera | BELUM CUKUP | 223 / 38 | 15 | +1.40 [-0.70, +3.50] | +2.26 | 56 | 1.15 | +0.30 | 0 | 15 | +4.38 |
| `M18` EMA9/21 Pullback | BELUM CUKUP | 269 / 193 | 15 | +0.30 [-0.86, +1.47] | +2.25 | 32 | 2.36 | -0.76 | 60 | 15 | -0.91 |
| `M118` Expansion Pivot (Cooper) | BELUM CUKUP | 63 / 15 | 15 | +0.38 [-2.60, +3.36] | +2.25 | 46 | 1.32 | -0.92 | 1 | 15 | +14.84 |
| `M73` ADX(5) > 40 + Julat Terkecil | BELUM CUKUP | 641 / 547 | 15 | -0.79 [-2.46, +0.88] | +2.22 | 62 | 0.44 | -1.46 | 0 | 15 | -2.36 |
| `M146` 3-Bar Momentum Pattern | BELUM CUKUP | 72 / 23 | 15 | +1.57 [-0.25, +3.40] | +2.17 | 57 | 1.27 | +0.44 | 4 | 15 | +10.64 |
| `M158` Doubly Adaptive Profit Targe | BELUM CUKUP | 297 / 87 | 15 | +0.77 [-1.21, +2.76] | +2.10 | 46 | 1.42 | -0.67 | 1 | 15 | +4.90 |
| `M92` CCI-50 | BELUM CUKUP | 447 / 230 | 15 | -0.12 [-1.65, +1.41] | +1.93 | 43 | 1.30 | -1.29 | 15 | 15 | +6.49 |
| `M153` Range Leader | BELUM CUKUP | 1035 / 740 | 15 | -0.13 [-1.44, +1.18] | +1.84 | 44 | 1.23 | -1.14 | 6 | 15 | +1.29 |
| `M124` 'Last' Stochastic Technique  | BELUM CUKUP | 317 / 134 | 15 | +0.04 [-2.20, +2.28] | +1.72 | 43 | 1.33 | -1.15 | 16 | 15 | +8.34 |
| `M91` Stochastic Pop (Bernstein/St | BELUM CUKUP | 33 / 9 | 11 | +0.27 [-6.45, +6.99] | +1.71 | 36 | 1.87 | -1.52 | 1 | 15 | +13.74 |
| `M32` Momentum Burst | BELUM CUKUP | 51 / 28 | 11 | -0.11 [-5.49, +5.27] | +1.67 | 31 | 2.12 | -2.40 | 9 | 15 | +0.96 |
| `M115` Bow Tie (Landry) | BELUM CUKUP | 31 / 13 | 8 | +0.05 [-2.85, +2.96] | +1.66 | 29 | 2.51 | -0.98 | 3 | 15 | +5.76 |
| `M151` Outside Bar Failure | BELUM CUKUP | 80 / 36 | 14 | +0.22 [-2.43, +2.87] | +1.64 | 36 | 1.91 | -0.98 | 11 | 15 | +11.43 |
| `M106` DMI Wilder | BELUM CUKUP | 91 / 41 | 13 | -0.57 [-3.31, +2.17] | +1.63 | 40 | 1.25 | -1.81 | 0 | 15 | +2.47 |
| `M35` Pocket Pivot Morales & Kache | BELUM CUKUP | 276 / 169 | 15 | -0.13 [-1.48, +1.22] | +1.54 | 27 | 2.57 | -1.20 | 66 | 15 | -0.21 |
| `M88` O'Neil Shakeout +3 | BELUM CUKUP | 47 / 23 | 12 | -1.22 [-8.38, +5.95] | +1.53 | 28 | 1.95 | -3.16 | 6 | 15 | +12.59 |
| `M105` Supertrend tulen | BELUM CUKUP | 298 / 76 | 15 | +0.75 [-1.51, +3.00] | +1.50 | 51 | 1.16 | -0.47 | 5 | 15 | +12.15 |

## Cara membaca

- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.** CALON bermaksud setiap dagangan lulus tetapi portfolio belum terbukti mengalahkan SPUS; `REVERSE/KEPUTUSAN_AKHIR.md` mengukur bahawa kohort setiap dagangan yang lulus pernah gagal 0/36 sebagai portfolio.
- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif; `X3` menang 30.2% dengan jangkaan +2.595% (`REVERSE/KOMBINASI.md`).
- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan (`REVERSE/KOLAM_EKOR.md`) dan memerlukan banyak posisi untuk ditangkap.
- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.

