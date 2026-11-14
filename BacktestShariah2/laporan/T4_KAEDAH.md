# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)

Dijana 2026-11-14 13:37 UTC oleh `standard/portfolio_t4.py` (Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Sesi terakhir 2026-11-13. **226 kaedah**, setiap satu dua lorong (L1 = keluar kaedah, L2 = Chandelier 4xATR14). Kawalan: 20 cabutan rawak 10 slot atas seluruh kolam Lejar, diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.

## Gate G6 (dikunci dalam `standard/kad_skor.py`)

Lorong L1 mesti (pindaan 7 Nov 2026): sesi >= 126; pulangan > 0; pulangan pada MDD -10% > SPUS pada MDD sama; nisbah pulangan/|MDD| > maksimum jalur rawak. 
**0 lulus.** Lorong paling lama ada 21 sesi; G6 tidak boleh lulus sebelum 126 sesi (anggaran 2027-04-09).

## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)

| Kaedah | Mula | Sesi | Pul % | MDD % | Berat utk MDD -10% | Pul pada MDD -10% | SPUS pada MDD -10% | Nisbah pul/MDD | Maks jalur | T4 70/30 % |
|---|---|---|---|---|---|---|---|---|---|---|
| `M10` | 2026-10-16 | 21 | +10.16 | -5.26 | 1.00 | +10.16 | -5.15 | 1.93 | 3.69 | -0.68 |
| `M118` | 2026-10-16 | 21 | +9.42 | -2.71 | 1.00 | +9.42 | -5.15 | 3.48 | 3.69 | -0.89 |
| `M33` | 2026-10-16 | 21 | +9.07 | -2.67 | 1.00 | +9.07 | -5.15 | 3.39 | 3.69 | -0.97 |
| `M13` | 2026-10-16 | 21 | +8.79 | -3.56 | 1.00 | +8.79 | -5.15 | 2.47 | 3.69 | -1.06 |
| `M48` | 2026-10-16 | 21 | +8.46 | -5.45 | 1.00 | +8.46 | -5.15 | 1.55 | 3.69 | -1.15 |
| `M151` | 2026-10-16 | 21 | +8.29 | -1.61 | 1.00 | +8.29 | -5.15 | 5.14 | 3.69 | -1.21 |
| `M39` | 2026-10-16 | 21 | +7.97 | -2.40 | 1.00 | +7.97 | -5.15 | 3.33 | 3.69 | -1.30 |
| `M133` | 2026-10-16 | 21 | +6.60 | -4.15 | 1.00 | +6.60 | -5.15 | 1.59 | 3.69 | -1.69 |
| `M91` | 2026-10-16 | 21 | +6.14 | -7.84 | 1.00 | +6.14 | -5.15 | 0.78 | 3.69 | -1.71 |
| `N45X16` | 2026-11-04 | 8 | +5.83 | -1.43 | 1.00 | +5.83 | -3.06 | 4.09 | 1.94 | -0.39 |
| `M146` | 2026-10-16 | 21 | +5.75 | -6.15 | 1.00 | +5.75 | -5.15 | 0.93 | 3.69 | -1.90 |
| `M159` | 2026-10-16 | 21 | +5.07 | -6.13 | 1.00 | +5.07 | -5.15 | 0.83 | 3.69 | -2.13 |
| `M02` | 2026-10-16 | 21 | +5.05 | -6.80 | 1.00 | +5.05 | -5.15 | 0.74 | 3.69 | -2.14 |
| `M137` | 2026-10-16 | 21 | +4.97 | -5.91 | 1.00 | +4.97 | -5.15 | 0.84 | 3.69 | -2.17 |
| `M145` | 2026-10-16 | 21 | +4.92 | -2.18 | 1.00 | +4.92 | -5.15 | 2.26 | 3.69 | -2.17 |

## Cara membaca

- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).
- "Pada MDD -10%" = pulangan jika pendedahan dikecilkan (baki tunai) sehingga MDD tepat -10%, toleransi pengguna. Membanding pada MDD yang sama ialah satu-satunya bandingan adil dengan SPUS.
- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.
- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.

