# SATELIT — GB02_atau3 × Chandelier 15% akaun di atas teras indeks 35% + tunai

Dijana 2026-11-09 14:23 UTC oleh `REVERSE/step41_satelit.py`. Pradaftar `REVERSE/SPEC_SATELIT.md` (dikomit sebelum larian). Alam A02 cair, kos penuh, teras SPY (proksi, spec §2), tahan 2020–2025, latih 2012–2019. Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Keputusan sel utama `S1` slot 8: **GAGAL** — P1 ✗ · P2 ✗ · P3 ✗ · P4 ✓ · P5 ✗
Slot 10: P1 ✗ · P2 ✗ · P3 ✗ · P4 ✓ · P5 ✗ · LULUS ✗

Gate (spec §4): P1 CAGR > `K1` dua tingkap · P2 MDD tahan ≥ -10% dan ≥ `K1` − 1 mata dua tingkap · P3 CAGR > p95 `R1` dan > `R2` · P4 nisbah > `K1` dua tingkap · P5 purata dagangan > 0 dua tingkap dan > `R1`.

## Jadual lengan (median benih; tahan 2020–2025 | latih 2012–2019)

| Lengan | Slot | Benih | CAGR % | p5–p95 | MDD % | Nisbah | Pada MDD -10% | CAGR latih % | MDD latih % | Dedah satelit % | Dagangan | Pul/dagangan % | Menang % | Untung % | Rugi % | Payoff | tanpa5 % | Pegang bar | Pusing/slot/thn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `K0` | 8 | 1 | +5.34 | – | -12.56 | 0.43 | +4.25 | +5.04 | -6.84 | 0.0 | 0 | +nan | nan | +nan | +nan | nan | +nan | nan | 0.0 |
| `K1` | 8 | 1 | +7.59 | – | -17.66 | 0.43 | +4.30 | +7.23 | -9.72 | 0.0 | 0 | +nan | nan | +nan | +nan | nan | +nan | nan | 0.0 |
| `R1` | 8 | 20 | +7.82 | +5.2–+9.7 | -14.86 | 0.53 | +5.26 | +6.76 | -8.93 | 13.3 | 187 | +4.39 | 44.4 | +24.22 | -12.16 | 1.97 | -0.85 | 52.6 | 3.9 |
| `R1` | 10 | 20 | +7.39 | +5.7–+9.2 | -14.57 | 0.51 | +5.07 | +6.53 | -8.42 | 13.4 | 234 | +4.00 | 43.0 | +24.90 | -12.27 | 2.12 | -1.35 | 53.3 | 3.9 |
| `R2` | 8 | 1 | +7.12 | – | -12.84 | 0.55 | +5.55 | +6.88 | -7.57 | 13.5 | 191 | +2.85 | 52.9 | +8.82 | -3.85 | 2.29 | +0.83 | 54.5 | 4.0 |
| `R2` | 10 | 1 | +6.99 | – | -13.14 | 0.53 | +5.32 | +6.78 | -7.48 | 13.3 | 250 | +2.54 | 48.0 | +9.69 | -4.05 | 2.39 | +0.41 | 51.5 | 4.2 |
| `S1` | 8 | 1 | +6.12 | – | -13.66 | 0.45 | +4.48 | +5.95 | -7.44 | 12.9 | 189 | +1.38 | 42.3 | +10.35 | -5.20 | 1.99 | -0.31 | 52.1 | 3.9 |
| `S1` | 10 | 1 | +6.15 | – | -13.76 | 0.45 | +4.47 | +6.00 | -7.44 | 13.0 | 235 | +1.52 | 43.8 | +11.00 | -5.88 | 1.87 | -0.16 | 52.6 | 3.9 |
| `S2` | 8 | 1 | +6.19 | – | -16.34 | 0.38 | +3.79 | +6.74 | -8.69 | 15.4 | 252 | +1.29 | 46.0 | +10.40 | -6.47 | 1.61 | -0.57 | 46.7 | 5.3 |
| `S2` | 10 | 1 | +6.15 | – | -16.64 | 0.37 | +3.70 | +6.87 | -8.85 | 15.5 | 313 | +1.23 | 44.7 | +10.78 | -6.50 | 1.66 | -0.73 | 47.1 | 5.2 |
| `S3` | 8 | 20 | +7.75 | +4.7–+12.0 | -15.22 | 0.51 | +5.09 | +6.76 | -9.41 | 13.7 | 174 | +4.87 | 42.7 | +29.74 | -14.75 | 2.13 | -1.40 | 58.4 | 3.6 |
| `S3` | 10 | 20 | +7.40 | +6.6–+10.2 | -14.91 | 0.50 | +4.96 | +6.42 | -9.30 | 13.8 | 220 | +4.35 | 43.7 | +29.98 | -14.55 | 2.02 | -1.37 | 57.2 | 3.7 |
| `S4` | 8 | 1 | +6.45 | – | -13.55 | 0.48 | +4.76 | +6.05 | -7.34 | 12.8 | 183 | +2.01 | 45.9 | +10.60 | -5.27 | 2.01 | -0.05 | 53.5 | 3.8 |
| `S4` | 10 | 1 | +6.66 | – | -13.76 | 0.48 | +4.84 | +5.95 | -7.40 | 12.9 | 228 | +2.40 | 47.8 | +10.91 | -5.40 | 2.02 | +0.28 | 54.2 | 3.8 |

## Rujukan pasif

- `K0` teras SPY 35% + tunai: CAGR +5.34% / MDD -12.56% (tahan); +5.04% / -6.84% (latih).
- `K1` teras SPY 50% + tunai: CAGR +7.59% / MDD -17.66% (tahan); +7.23% / -9.72% (latih).
- SPUS bulanan + tunai 2020–2025 (maklumat, konvensyen `SISTEM.md`): 35% → +6.33% / -9.88%; 50% → +9.03% / -13.96%.

## Dagangan satelit ikut rejim pada hari masuk (`S2`, tanpa penapis rejim, slot 8, tahan)

| Rejim | Dagangan | Pul/dagangan % | Menang % | Untung % | Rugi % | Pegang bar |
|---|---|---|---|---|---|---|
| ON | 106 | +1.71 | 43.4 | +11.53 | -5.82 | 44.5 |
| OFF | 146 | +0.99 | 47.9 | +9.66 | -6.99 | 48.3 |

## Jangkaan priori (spec §7) lawan keputusan

- P2 lulus nipis: **salah**; P1 gagal latih: **betul**; P3 lulus: **salah**; P5 lulus: **salah**; keseluruhan GAGAL: **betul**.

## Had

- Alam A02 tiada saham delist: CAGR satelit condong ke atas. Kolam GB02 dan keluar X15 dipilih daripada data yang sama. Teras SPY ialah proksi SPUS (SPUS tiada 2012–2019 dan tiada harian dalam repo); SPUS mengalahkan SPY 2020–2025, jadi alternatif pasif sebenar lebih kuat daripada `K1` di sini. `CARA` kekal `C01`. Tiada impak pasaran dalam kos. Tiada dakwaan +10%/bulan.
