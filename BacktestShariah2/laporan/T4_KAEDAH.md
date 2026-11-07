# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)

Dijana 2026-11-07 16:28 UTC oleh `standard/portfolio_t4.py` (Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.

Sesi terakhir 2026-11-06. **223 kaedah**, setiap satu dua lorong (L1 = keluar kaedah, L2 = Chandelier 4xATR14). Kawalan: 20 cabutan rawak 10 slot atas seluruh kolam Lejar, diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.

## Gate G6 (dikunci dalam `standard/kad_skor.py`)

Lorong L1 mesti: sesi >= 126; pulangan > SPUS tingkap sama; pulangan > persentil 95 jalur rawak; MDD >= -26.82%. 
**0 lulus.** Lorong paling lama ada 16 sesi; G6 tidak boleh lulus sebelum 126 sesi (anggaran 2027-04-09).

## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)

| Kaedah | Mula | Sesi | Pul % | MDD % | SPUS % | Lebih SPUS | Persentil jalur | T4 80/20 % | T4 70/30 % | T4 50/50 % |
|---|---|---|---|---|---|---|---|---|---|---|
| `N50X14` | 2026-10-16 | 16 | +10.75 | -3.68 | -5.77 | +16.52 | 100 | -2.57 | -0.95 | +2.33 |
| `M118` | 2026-10-16 | 16 | +8.70 | -2.71 | -5.77 | +14.47 | 100 | -2.95 | -1.53 | +1.34 |
| `M33` | 2026-10-16 | 16 | +7.90 | -2.67 | -5.77 | +13.67 | 100 | -3.09 | -1.75 | +0.97 |
| `M02` | 2026-10-16 | 16 | +7.73 | -4.42 | -5.77 | +13.50 | 100 | -3.14 | -1.81 | +0.87 |
| `M10` | 2026-10-16 | 16 | +7.11 | -5.26 | -5.77 | +12.88 | 100 | -3.25 | -1.99 | +0.57 |
| `N57X36` | 2026-10-16 | 16 | +6.81 | -1.53 | -5.77 | +12.58 | 100 | -3.30 | -2.06 | +0.44 |
| `M151` | 2026-10-16 | 16 | +6.36 | -1.22 | -5.77 | +12.13 | 100 | -3.40 | -2.21 | +0.21 |
| `M13` | 2026-10-16 | 16 | +5.94 | -3.56 | -5.77 | +11.70 | 100 | -3.47 | -2.31 | +0.02 |
| `M133` | 2026-10-16 | 16 | +5.43 | -4.15 | -5.77 | +11.20 | 100 | -3.58 | -2.47 | -0.25 |
| `M91` | 2026-10-16 | 16 | +5.31 | -7.84 | -5.77 | +11.08 | 100 | -3.51 | -2.39 | -0.16 |
| `N50X17` | 2026-10-16 | 16 | +4.80 | -3.72 | -5.77 | +10.57 | 95 | -3.70 | -2.66 | -0.56 |
| `M48` | 2026-10-16 | 16 | +4.65 | -5.45 | -5.77 | +10.42 | 95 | -3.73 | -2.70 | -0.62 |
| `N39X36` | 2026-10-16 | 16 | +4.59 | -1.69 | -5.77 | +10.36 | 95 | -3.74 | -2.72 | -0.66 |
| `M25` | 2026-10-16 | 16 | +4.23 | -5.78 | -5.77 | +10.00 | 95 | -3.79 | -2.80 | -0.80 |
| `N57X16` | 2026-10-16 | 16 | +4.11 | -5.29 | -5.77 | +9.88 | 95 | -3.79 | -2.80 | -0.82 |

## Cara membaca

- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).
- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.
- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.

