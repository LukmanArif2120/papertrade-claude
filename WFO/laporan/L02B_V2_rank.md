# L02B — Ujian semula L02 V2 (rank = p meta-label, tanpa penapis) dengan kriteria pra-daftar

**Status:** kriteria ditetapkan 17 Okt 2026 SEBELUM larian (commit ini), selepas pemerhatian L02 V2 menaikkan CAGR 4/6 kaedah dalam data luar sampel yang sama. Oleh itu ujian mesti memakai data yang belum dilihat bagi soalan ini.

## Kriteria pra-daftar
| Ujian | Data | Syarat lulus |
|---|---|---|
| A | 6 kaedah BAHARU yang tidak dipakai dalam L02: M74 V2, M05 V3, M80 V2, M12 V5, M46 V2, M40 V4 (enam teratas papan selepas set L02, modul asal M01–M114). Prosedur sama: logistik L2 λ = 1, label halangan tiga, ciri sama, latih semula setiap suku (purge 20 + embargo 5), model gabungan enam kaedah baharu; luar sampel 1 Jan 2023 – 2 Okt 2026 | CAGR V2 ≥ asas bagi ≥ 4/6 kaedah DAN median ΔCAGR > 0 |
| B | 6 kaedah asal L02, subset S1–S4 (p daripada larian L02; persentil ciri atas 431) | Bagi ≥ 4/6 kaedah: CAGR V2 ≥ asas dalam ≥ 3/4 subset |

V2 diterima sebagai calon jejak kertas hanya jika A DAN B lulus. Tiada perubahan pada rutin harian atau Papertrade C dalam apa jua keadaan tanpa keputusan pengguna.

## Hasil
### Ujian A — 6 kaedah baharu (431, luar sampel 2023 – Okt 2026)
| Kaedah | CAGR asas | CAGR V2 | ΔCAGR | MDD asas | MDD V2 | Dagangan | V2 ≥ asas |
|---|---|---|---|---|---|---|---|
| M74 V2 | 39.4% | 52.3% | +12.9 | -22.6% | -28.2% | 1579 | Ya |
| M05 V3 | 22.5% | 30.6% | +8.1 | -20.0% | -23.2% | 396 | Ya |
| M80 V2 | 10.7% | -0.5% | -11.2 | -43.4% | -36.2% | 3552 | Tidak |
| M12 V5 | 27.4% | 27.2% | -0.2 | -29.8% | -27.3% | 6411 | Tidak |
| M46 V2 | 33.3% | 32.0% | -1.3 | -20.6% | -23.2% | 696 | Tidak |
| M40 V4 | 26.2% | 25.4% | -0.8 | -36.3% | -38.3% | 204 | Tidak |

**A: 2/6 (perlu ≥ 4/6), median ΔCAGR -0.49 mata (perlu > 0) → GAGAL.**

### Ujian B — 6 kaedah asal L02, subset S1–S4 (CAGR asas → V2)
| Kaedah | S1 | S2 | S3 | S4 | Subset V2 ≥ asas |
|---|---|---|---|---|---|
| M96 | 10.1% → 10.1% | 26.9% → 26.9% | 20.0% → 22.2% | 8.2% → 8.2% | 3/4 |
| M30 | 26.2% → 28.7% | 24.2% → 28.0% | 29.6% → 31.3% | 20.9% → 32.0% | 4/4 |
| M79 | 21.9% → 14.9% | 30.2% → 39.1% | 20.8% → 18.2% | 25.3% → 32.2% | 2/4 |
| M111 | 16.7% → 5.1% | 10.9% → 12.6% | 8.7% → 2.4% | 39.6% → 43.1% | 2/4 |
| M114 | 40.2% → 39.2% | 47.0% → 53.7% | 42.1% → 31.9% | 36.4% → 31.3% | 1/4 |
| M81 | 31.6% → 16.7% | 18.0% → 44.3% | 17.6% → 30.6% | 12.8% → 18.0% | 3/4 |

**B: 3/6 kaedah lulus ≥ 3/4 subset (perlu ≥ 4/6) → GAGAL.** (M96 sama di S1, S2, S4 kerana ≤ 8 isyarat sebulan: susunan tidak mengubah pilihan.)

## Verdict
**L02B DITOLAK: Ujian A 2/6 (median ΔCAGR −0.5 mata) dan Ujian B 3/6. Kenaikan CAGR L02 V2 dalam data asal tidak berulang pada kaedah baharu atau subset; ia kesan laluan portfolio (path dependence), bukan kelebihan. Contoh: M30 V2 −33.9 mata di 431 tetapi naik dalam keempat-empat subset. Tiada jejak kertas, tiada perubahan rutin.**

## Batasan
- Kaedah baharu dilatih dengan model gabungan sendiri (6 kaedah); ciri dan prosedur sama seperti L02.
- Ujian B memakai p yang sama dengan L02 (bukan dilatih semula dalam subset); persentil ciri atas 431.
- Luar sampel satu rejim (2023–2026); bias kemandirian; harga terlaras.
- Skrip: `WFO/kaedah_baru/step2_L02B.py`; hasil: `WFO/data/hasil/L02B_ringkasan.csv`.
