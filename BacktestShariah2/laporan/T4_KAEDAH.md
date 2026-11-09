# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)

Dijana 2026-11-09 03:08 UTC oleh `standard/portfolio_t4.py` (Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.

> **Status keputusan (kad skor, harga 2026-11-06):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Sesi terakhir 2026-11-06. **223 kaedah**, setiap satu dua lorong (L1 = keluar kaedah, L2 = Chandelier 4xATR14). Kawalan: 20 cabutan rawak 10 slot atas seluruh kolam Lejar, diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.

## Gate G6 (dikunci dalam `standard/kad_skor.py`)

Lorong L1 mesti (pindaan 7 Nov 2026): sesi >= 126; pulangan > 0; pulangan pada MDD -10% > SPUS pada MDD sama; nisbah pulangan/|MDD| > maksimum jalur rawak. 
**0 lulus.** Lorong paling lama ada 16 sesi; G6 tidak boleh lulus sebelum 126 sesi (anggaran 2027-04-09).

## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)

| Kaedah | Mula | Sesi | Pul % | MDD % | Berat utk MDD -10% | Pul pada MDD -10% | SPUS pada MDD -10% | Nisbah pul/MDD | Maks jalur | T4 70/30 % |
|---|---|---|---|---|---|---|---|---|---|---|
| `M118` | 2026-10-16 | 16 | +8.70 | -2.71 | 1.00 | +8.70 | -5.77 | 3.22 | 5.23 | -1.53 |
| `M33` | 2026-10-16 | 16 | +7.90 | -2.67 | 1.00 | +7.90 | -5.77 | 2.96 | 5.23 | -1.75 |
| `M02` | 2026-10-16 | 16 | +7.73 | -4.42 | 1.00 | +7.73 | -5.77 | 1.75 | 5.23 | -1.81 |
| `M10` | 2026-10-16 | 16 | +7.11 | -5.26 | 1.00 | +7.11 | -5.77 | 1.35 | 5.23 | -1.99 |
| `M151` | 2026-10-16 | 16 | +6.36 | -1.22 | 1.00 | +6.36 | -5.77 | 5.23 | 5.23 | -2.21 |
| `M13` | 2026-10-16 | 16 | +5.94 | -3.56 | 1.00 | +5.94 | -5.77 | 1.67 | 5.23 | -2.31 |
| `M133` | 2026-10-16 | 16 | +5.43 | -4.15 | 1.00 | +5.43 | -5.77 | 1.31 | 5.23 | -2.47 |
| `M91` | 2026-10-16 | 16 | +5.31 | -7.84 | 1.00 | +5.31 | -5.77 | 0.68 | 5.23 | -2.39 |
| `M48` | 2026-10-16 | 16 | +4.65 | -5.45 | 1.00 | +4.65 | -5.77 | 0.85 | 5.23 | -2.70 |
| `M25` | 2026-10-16 | 16 | +4.23 | -5.78 | 1.00 | +4.23 | -5.77 | 0.73 | 5.23 | -2.80 |
| `M39` | 2026-10-16 | 16 | +3.98 | -2.40 | 1.00 | +3.98 | -5.77 | 1.66 | 5.23 | -2.89 |
| `N45X16` | 2026-11-04 | 3 | +3.61 | 0.00 | 1.00 | +3.61 | -3.69 | 3613700.00 | 2.40 | -1.50 |
| `M129` | 2026-10-16 | 16 | +3.56 | -2.82 | 1.00 | +3.56 | -5.77 | 1.26 | 5.23 | -3.01 |
| `M89` | 2026-10-16 | 16 | +3.50 | -4.76 | 1.00 | +3.50 | -5.77 | 0.73 | 5.23 | -3.02 |
| `M124` | 2026-10-16 | 16 | +3.35 | -4.58 | 1.00 | +3.35 | -5.77 | 0.73 | 5.23 | -3.07 |

## Cara membaca

- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).
- "Pada MDD -10%" = pulangan jika pendedahan dikecilkan (baki tunai) sehingga MDD tepat -10%, toleransi pengguna. Membanding pada MDD yang sama ialah satu-satunya bandingan adil dengan SPUS.
- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.
- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.

