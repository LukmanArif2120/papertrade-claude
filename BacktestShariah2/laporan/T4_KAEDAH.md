# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)

Dijana 2026-11-18 18:54 UTC oleh `standard/portfolio_t4.py` (Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.

> **Status keputusan (kad skor, harga 2026-11-17):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Sesi terakhir 2026-11-17. **226 kaedah**, setiap satu dua lorong (L1 = keluar kaedah, L2 = Chandelier 4xATR14). Kawalan: 20 cabutan rawak 10 slot atas seluruh kolam Lejar, diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.

## Gate G6 (dikunci dalam `standard/kad_skor.py`)

Lorong L1 mesti (pindaan 7 Nov 2026): sesi >= 126; pulangan > 0; pulangan pada MDD -10% > SPUS pada MDD sama; nisbah pulangan/|MDD| > maksimum jalur rawak. 
**0 lulus.** Lorong paling lama ada 23 sesi; G6 tidak boleh lulus sebelum 126 sesi (anggaran 2027-04-09).

## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)

| Kaedah | Mula | Sesi | Pul % | MDD % | Berat utk MDD -10% | Pul pada MDD -10% | SPUS pada MDD -10% | Nisbah pul/MDD | Maks jalur | T4 70/30 % |
|---|---|---|---|---|---|---|---|---|---|---|
| `M10` | 2026-10-16 | 23 | +8.79 | -5.26 | 1.00 | +8.79 | -8.18 | 1.67 | 1.81 | -3.24 |
| `M151` | 2026-10-16 | 23 | +7.27 | -1.61 | 1.00 | +7.27 | -8.18 | 4.51 | 1.81 | -3.67 |
| `M13` | 2026-10-16 | 23 | +6.91 | -3.56 | 1.00 | +6.91 | -8.18 | 1.94 | 1.81 | -3.77 |
| `M118` | 2026-10-16 | 23 | +6.65 | -4.54 | 1.00 | +6.65 | -8.18 | 1.46 | 1.81 | -3.85 |
| `M48` | 2026-10-16 | 23 | +6.48 | -5.45 | 1.00 | +6.48 | -8.18 | 1.19 | 1.81 | -3.88 |
| `M33` | 2026-10-16 | 23 | +5.95 | -4.17 | 1.00 | +5.95 | -8.18 | 1.43 | 1.81 | -4.03 |
| `M39` | 2026-10-16 | 23 | +5.54 | -2.40 | 1.00 | +5.54 | -8.18 | 2.31 | 1.81 | -4.16 |
| `M146` | 2026-10-16 | 23 | +4.81 | -6.15 | 1.00 | +4.81 | -8.18 | 0.78 | 1.81 | -4.35 |
| `M159` | 2026-10-16 | 23 | +3.76 | -6.13 | 1.00 | +3.76 | -8.18 | 0.61 | 1.81 | -4.66 |
| `N45X16` | 2026-11-04 | 10 | +3.58 | -3.32 | 1.00 | +3.58 | -6.15 | 1.08 | 0.37 | -3.23 |
| `M137` | 2026-10-16 | 23 | +3.38 | -5.91 | 1.00 | +3.38 | -8.18 | 0.57 | 1.81 | -4.78 |
| `M145` | 2026-10-16 | 23 | +3.29 | -2.18 | 1.00 | +3.29 | -8.18 | 1.51 | 1.81 | -4.79 |
| `M25` | 2026-10-16 | 23 | +2.86 | -6.06 | 1.00 | +2.86 | -8.18 | 0.47 | 1.81 | -4.92 |
| `M133` | 2026-10-16 | 23 | +2.65 | -4.90 | 1.00 | +2.65 | -8.18 | 0.54 | 1.81 | -4.99 |
| `M129` | 2026-10-16 | 23 | +2.50 | -3.39 | 1.00 | +2.50 | -8.18 | 0.74 | 1.81 | -5.04 |

## Cara membaca

- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).
- "Pada MDD -10%" = pulangan jika pendedahan dikecilkan (baki tunai) sehingga MDD tepat -10%, toleransi pengguna. Membanding pada MDD yang sama ialah satu-satunya bandingan adil dengan SPUS.
- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.
- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.

