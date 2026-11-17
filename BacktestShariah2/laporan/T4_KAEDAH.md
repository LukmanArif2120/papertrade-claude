# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)

Dijana 2026-11-17 12:07 UTC oleh `standard/portfolio_t4.py` (Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.

> **Status keputusan (kad skor, harga 2026-11-16):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Sesi terakhir 2026-11-16. **226 kaedah**, setiap satu dua lorong (L1 = keluar kaedah, L2 = Chandelier 4xATR14). Kawalan: 20 cabutan rawak 10 slot atas seluruh kolam Lejar, diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.

## Gate G6 (dikunci dalam `standard/kad_skor.py`)

Lorong L1 mesti (pindaan 7 Nov 2026): sesi >= 126; pulangan > 0; pulangan pada MDD -10% > SPUS pada MDD sama; nisbah pulangan/|MDD| > maksimum jalur rawak. 
**0 lulus.** Lorong paling lama ada 22 sesi; G6 tidak boleh lulus sebelum 126 sesi (anggaran 2027-04-09).

## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)

| Kaedah | Mula | Sesi | Pul % | MDD % | Berat utk MDD -10% | Pul pada MDD -10% | SPUS pada MDD -10% | Nisbah pul/MDD | Maks jalur | T4 70/30 % |
|---|---|---|---|---|---|---|---|---|---|---|
| `M10` | 2026-10-16 | 22 | +9.89 | -5.26 | 1.00 | +9.89 | -5.15 | 1.88 | 3.25 | -0.75 |
| `M33` | 2026-10-16 | 22 | +9.14 | -2.67 | 1.00 | +9.14 | -5.15 | 3.42 | 3.25 | -0.95 |
| `M118` | 2026-10-16 | 22 | +8.63 | -2.77 | 1.00 | +8.63 | -5.15 | 3.11 | 3.25 | -1.11 |
| `M151` | 2026-10-16 | 22 | +8.38 | -1.61 | 1.00 | +8.38 | -5.15 | 5.20 | 3.25 | -1.18 |
| `M13` | 2026-10-16 | 22 | +7.72 | -3.56 | 1.00 | +7.72 | -5.15 | 2.17 | 3.25 | -1.36 |
| `M48` | 2026-10-16 | 22 | +7.68 | -5.45 | 1.00 | +7.68 | -5.15 | 1.41 | 3.25 | -1.38 |
| `M39` | 2026-10-16 | 22 | +7.48 | -2.40 | 1.00 | +7.48 | -5.15 | 3.12 | 3.25 | -1.44 |
| `M146` | 2026-10-16 | 22 | +6.00 | -6.15 | 1.00 | +6.00 | -5.15 | 0.97 | 3.25 | -1.83 |
| `M133` | 2026-10-16 | 22 | +5.76 | -4.15 | 1.00 | +5.76 | -5.15 | 1.39 | 3.25 | -1.94 |
| `M159` | 2026-10-16 | 22 | +5.72 | -6.13 | 1.00 | +5.72 | -5.15 | 0.93 | 3.25 | -1.94 |
| `N45X16` | 2026-11-04 | 9 | +5.22 | -1.79 | 1.00 | +5.22 | -3.06 | 2.91 | 1.36 | -0.57 |
| `M91` | 2026-10-16 | 22 | +4.99 | -8.12 | 1.00 | +4.99 | -5.15 | 0.61 | 3.25 | -2.02 |
| `M137` | 2026-10-16 | 22 | +4.87 | -5.91 | 1.00 | +4.87 | -5.15 | 0.82 | 3.25 | -2.19 |
| `M145` | 2026-10-16 | 22 | +4.85 | -2.18 | 1.00 | +4.85 | -5.15 | 2.23 | 3.25 | -2.19 |
| `M25` | 2026-10-16 | 22 | +4.57 | -5.78 | 1.00 | +4.57 | -5.15 | 0.79 | 3.25 | -2.26 |

## Cara membaca

- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).
- "Pada MDD -10%" = pulangan jika pendedahan dikecilkan (baki tunai) sehingga MDD tepat -10%, toleransi pengguna. Membanding pada MDD yang sama ialah satu-satunya bandingan adil dengan SPUS.
- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.
- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.

