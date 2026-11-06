# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)

Dijana 2026-11-06 17:32 UTC oleh `standard/portfolio_t4.py` (Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.

Sesi terakhir 2026-11-05. **222 kaedah**, setiap satu dua lorong (L1 = keluar kaedah, L2 = Chandelier 4xATR14). Kawalan: 20 cabutan rawak 10 slot atas seluruh kolam Lejar, diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.

## Gate G6 (dikunci dalam `standard/kad_skor.py`)

Lorong L1 mesti: sesi >= 126; pulangan > SPUS tingkap sama; pulangan > persentil 95 jalur rawak; MDD >= -26.82%. 
**0 lulus.** Lorong paling lama ada 15 sesi; G6 tidak boleh lulus sebelum 126 sesi (anggaran 2027-04-09).

## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)

| Kaedah | Mula | Sesi | Pul % | MDD % | SPUS % | Lebih SPUS | Persentil jalur | T4 80/20 % | T4 70/30 % | T4 50/50 % |
|---|---|---|---|---|---|---|---|---|---|---|
| `M33` | 2026-10-16 | 15 | +10.56 | -2.67 | -5.04 | +15.60 | 100 | -2.01 | -0.47 | +2.63 |
| `M118` | 2026-10-16 | 15 | +9.80 | -1.72 | -5.04 | +14.84 | 100 | -2.16 | -0.70 | +2.25 |
| `M10` | 2026-10-16 | 15 | +9.45 | -3.19 | -5.04 | +14.49 | 100 | -2.22 | -0.80 | +2.08 |
| `M91` | 2026-10-16 | 15 | +8.70 | -4.88 | -5.04 | +13.74 | 100 | -2.30 | -0.93 | +1.82 |
| `M02` | 2026-10-16 | 15 | +8.53 | -3.71 | -5.04 | +13.57 | 100 | -2.40 | -1.06 | +1.63 |
| `N57X36` | 2026-10-16 | 15 | +7.88 | -1.36 | -5.04 | +12.91 | 100 | -2.51 | -1.24 | +1.33 |
| `M88` | 2026-10-16 | 15 | +7.55 | -4.01 | -5.04 | +12.59 | 100 | -2.58 | -1.34 | +1.16 |
| `M13` | 2026-10-16 | 15 | +7.40 | -3.56 | -5.04 | +12.44 | 100 | -2.60 | -1.38 | +1.10 |
| `N50X14` | 2026-10-16 | 15 | +7.23 | -3.68 | -5.04 | +12.27 | 100 | -2.63 | -1.42 | +1.02 |
| `M148` | 2026-10-16 | 15 | +7.19 | -2.67 | -5.04 | +12.23 | 100 | -2.65 | -1.45 | +0.98 |
| `M105` | 2026-10-16 | 15 | +7.11 | -3.51 | -5.04 | +12.15 | 100 | -2.66 | -1.46 | +0.96 |
| `N57X16` | 2026-10-16 | 15 | +7.06 | -2.60 | -5.04 | +12.10 | 100 | -2.65 | -1.45 | +0.96 |
| `M133` | 2026-10-16 | 15 | +6.64 | -4.15 | -5.04 | +11.67 | 100 | -2.76 | -1.61 | +0.71 |
| `M151` | 2026-10-16 | 15 | +6.39 | -1.22 | -5.04 | +11.43 | 100 | -2.81 | -1.68 | +0.60 |
| `M39` | 2026-10-16 | 15 | +6.00 | -2.40 | -5.04 | +11.04 | 100 | -2.88 | -1.79 | +0.41 |

## Cara membaca

- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).
- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.
- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.

