# CS09: KELUAR daripada maklumat yang belum dicuba — pasaran, sektor, earnings, relatif, kemuncak, laluan (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_keluar9.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (r), dikomit sebelum dijalankan. **Jangan sunting secara manual.**

## 1. Apa yang dicari

- CS07 mencari keluar daripada harga/volum saham itu sendiri sahaja (97 atom). Pusingan ini menambah **80 atom baharu dalam enam kelas**: P = pasaran (22); S = sektor/industri (2); E = peristiwa earnings (10); R = relatif kepada pasaran (5); K = kemuncak / terlalu panas (17); L = keadaan laluan sejak beli (24).
- 21,922 peraturan (atom baharu tunggal, pasangan baharu × baharu, pasangan baharu × lama, dan penanda aras CS07) × 3 syarat aktif × 8 henti = **526,128 cara keluar setiap setup**, bagi 69 setup, dipilih pada kumpulan A sahaja.
- Ukuran sama seperti CS07: **tangkap penuh** = naik ≥ 5 % minggu pertama DAN dijual dengan untung ≥ 10 %; syarat "tidak jual awal" (untung pada saham yang terus naik ≥ 90% daripada "pegang sahaja 20 sesi"). 240,968 cara lulus syarat itu pada A.
- Pegang minimum 3 sesi terpakai: indikator keluar menjual paling awal pada buka sesi ke-4; henti rugi kekal aktif.

## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)

**Bacaan 1 — item 4 matlamat ("indikator yang memberitahu kenaikan sudah tamat"):**

- Keluar terpilih mengatasi `X00` (pegang sahaja, henti sama): **33 daripada 69** setup; mengatasi keluar terbaik CS07: **25 daripada 69**; mengatasi kedua-duanya: **25 daripada 69** (perlu lebih separuh).
- Nisbah simpan (median): 0.97 (perlu ≥ 0.90). Rugi ≥ 8 %: median beza lawan keluar terbaik CS07 +0.0 mata (perlu ≤ +1.0).
- 2025–26 (K3, tahun yang carian tidak lihat; 64 setup dengan ≥ 30 isyarat): median tambahan tangkap penuh lawan pegang sahaja +0.00 mata (perlu > 0).
- Median tangkap penuh: pegang sahaja 15.1 % → keluar terbaik CS07 15.3 % → keluar terpilih CS09 **15.8 %**.
- **Keputusan bacaan 1: keluar baharu TIDAK menolong.**

**Bacaan 2 — sisi rugi (BUKAN item 4; adakah keluar baharu mengurangkan rugi tanpa menjual pelari):**

- Purata dagangan lebih tinggi DAN rugi ≥ 8 % lebih rendah daripada pegang sahaja (henti sama), tanpa mengurangkan tangkap penuh lebih 0.5 mata: **2 daripada 69** setup (perlu lebih separuh).
- Nisbah simpan (median): 1.00. 2025–26: median tambahan purata dagangan +0.00 mata (perlu > 0).
- Median merentas setup: purata dagangan pegang sahaja +2.04 % → terpilih **+2.04 %**; rugi ≥ 8 % 26.2 % → **26.2 %**; menang 54 % → 54 %.
- **Keputusan bacaan 2: potong rugi TIDAK menolong.**

## 3. Keluar sejagat ikut tangkap penuh (senarai T; 10 teratas daripada 30; dipilih pada A, disemak pada B)

Komposisi kelas 30 teratas: K+lama 22, K 8. Penanda aras CS07 (5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%]): A +0.47 mata, B +0.95 mata (83% setup lebih baik), 2025–26 +1.15.

| # | Henti | Peraturan keluar | Kelas | A: tambahan tangkap penuh (mata) | A: nisbah simpan | B: tambahan (mata) | B: % setup lebih baik | B: nisbah simpan | 2025–26: tambahan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.72 | 0.91 | +1.33 | 90% | 0.89 | +1.54 |
| 2 | min(-10%, 4xATR14) | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.72 | 0.91 | +1.33 | 90% | 0.89 | +1.54 |
| 3 | 5xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.72 | 0.91 | +1.33 | 90% | 0.89 | +1.54 |
| 4 | 3xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.72 | 0.91 | +1.33 | 90% | 0.89 | +1.54 |
| 5 | -15% | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.72 | 0.91 | +1.33 | 90% | 0.89 | +1.54 |
| 6 | -10% | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.71 | 0.91 | +1.33 | 91% | 0.89 | +1.59 |
| 7 | -12% | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.71 | 0.91 | +1.34 | 91% | 0.89 | +1.58 |
| 8 | -8% | (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | K+lama | +0.71 | 0.91 | +1.33 | 91% | 0.89 | +1.59 |
| 9 | -15% | tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | K+lama | +0.65 | 0.92 | +1.30 | 94% | 0.91 | +1.57 |
| 10 | 4xATR14 | tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | K+lama | +0.65 | 0.92 | +1.30 | 94% | 0.91 | +1.58 |

## 4. Keluar sejagat ikut sisi rugi (senarai R; 10 teratas daripada 30)

Komposisi kelas 30 teratas: K+lama 30.

| # | Henti | Peraturan keluar | Kelas | A: tambahan purata dagangan (mata) | A: tambahan tangkap penuh | A: nisbah simpan | B: tambahan purata | B: % setup lebih baik | B: beza rugi ≥ 8 % | B: nisbah simpan | 2025–26: tambahan purata |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 5xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 2 | 5xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli [aktif selepas +5%] | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 3 | 5xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli [aktif selepas +10%] | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 4 | 4xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 5 | 4xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli [aktif selepas +5%] | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 6 | 4xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli [aktif selepas +10%] | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 7 | min(-10%, 4xATR14) | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 8 | min(-10%, 4xATR14) | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli [aktif selepas +5%] | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 9 | min(-10%, 4xATR14) | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli [aktif selepas +10%] | K+lama | +0.01 | +0.00 | 1.00 | +0.02 | 29% | -0.0 | 1.00 | +0.01 |
| 10 | 3xATR14 | (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | K+lama | +0.01 | +0.00 | 1.00 | +0.03 | 29% | -0.0 | 1.00 | +0.01 |

## 5. Setiap kelas maklumat: atom tunggal terbaik (dipilih pada A; maklumat, bukan bacaan)

Plasebo = siri yang sama dianjak 437 sesi (kelas P, S, E sahaja): jika plasebo sama baik, kelas itu tidak membawa maklumat.

| Kelas | Ikut | Atom tunggal terbaik (henti) | A (mata) | B (mata) | B: % setup lebih baik | B: nisbah simpan | 2025–26 | Plasebo: A / B |
|---|---|---|---|---|---|---|---|---|
| P pasaran | tangkap penuh | pasaran: QQQ RSI14 < 35 [aktif selepas +10%] (-8%) | -0.62 | -0.32 | 13% | 0.96 | -0.06 | +0.06 / +0.50 |
| P pasaran | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – |
| S sektor/industri | tangkap penuh | tiada yang lulus syarat | – | – | – | – | – | – |
| S sektor/industri | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – |
| E peristiwa earnings | tangkap penuh | reaksi earnings terakhir (0-5 sesi lalu) <= -5% [aktif selepas +10%] (-8%) | -0.15 | -0.01 | 30% | 0.98 | -0.01 | -0.14 / +0.14 |
| E peristiwa earnings | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – |
| R relatif kepada pasaran | tangkap penuh | pulangan 10 sesi saham - QQQ <= -15% [aktif selepas +10%] (-8%) | -0.38 | -0.19 | 12% | 0.97 | -0.08 | – |
| R relatif kepada pasaran | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – |
| K kemuncak / terlalu panas | tangkap penuh | 6 tutup naik berturut [aktif selepas +10%] (-10%) | +0.21 | +0.79 | 93% | 0.93 | +0.70 | – |
| K kemuncak / terlalu panas | purata dagangan | (tutup - SMA20) / ATR14 >= 6 [aktif selepas +10%] (-12%) | -0.02 | +0.04 | 42% | 1.01 | -0.10 | – |
| L keadaan laluan sejak beli | tangkap penuh | distribution day saham sejak beli >= 4 [aktif selepas +10%] (-8%) | -0.32 | -0.15 | 13% | 0.99 | -0.10 | – |
| L keadaan laluan sejak beli | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – |

## 6. Setiap setup (kumpulan B; semua isyarat, perbandingan berpasangan)

| ID | Keluar terpilih-T | Tangkap penuh %: pegang sahaja / CS07 / **CS09** | 2025–26: pegang / CS09 | Nisbah simpan | Keluar terpilih-R | Purata %: pegang → R | Rugi ≥ 8 %: pegang → R | Menang %: pegang → R |
|---|---|---|---|---|---|---|---|---|
| `F43` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 22.6 / 22.6 / **22.6** | 11.5 / 11.5 | 1.00 | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +5.66 → +5.66 | 17 → 17 | 69 → 69 |
| `F63` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 25.0 / 25.0 / **25.9** | 20.8 / 20.8 | 0.94 | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +4.33 → +4.33 | 27 → 27 | 60 → 60 |
| `F65` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | 21.3 / 21.3 / **22.2** | 21.2 / 21.2 | 0.91 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +3.17 → +3.17 | 20 → 20 | 65 → 65 |
| `F51` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 22.0 / 22.2 / **22.8** | 25.8 / 25.8 | 0.95 | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +4.85 → +4.85 | 18 → 18 | 64 → 64 |
| `F50` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 27.5 / 27.5 / **28.0** | 34.3 / 35.7 | 0.91 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +4.47 → +4.47 | 25 → 25 | 59 → 59 |
| `F56` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | 21.5 / 21.5 / **21.5** | 16.7 / 16.7 | 0.97 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +5.17 → +5.17 | 21 → 21 | 60 → 60 |
| `F39` | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 20.7 / 22.5 / **22.5** | 23.1 / 24.8 | 0.84 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.74 → +1.74 | 29 → 29 | 53 → 53 |
| `F91` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 20.0 / 20.0 / **20.0** | 21.7 / 21.7 | 1.00 | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.72 → +2.72 | 31 → 31 | 51 → 51 |
| `F40` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 21.6 / 21.6 / **21.6** | 26.4 / 26.4 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.04 → +2.04 | 27 → 27 | 53 → 53 |
| `F89` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 18.5 / 18.5 / **18.5** | 20.2 / 20.2 | 1.00 | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.87 → +1.87 | 32 → 32 | 50 → 50 |
| `F90` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 19.6 / 19.6 / **19.6** | 29.7 / 29.7 | 1.00 | -8% · X00 tiada keluar indikator (henti + 20 sesi) | +1.71 → +1.71 | 45 → 45 | 43 → 43 |
| `F88` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 17.4 / 18.5 / **18.3** | 20.0 / 20.0 | 0.83 | min(-10%, 4xATR14) · X00 tiada keluar indikator (henti + 20 sesi) | +2.66 → +2.66 | 21 → 21 | 59 → 59 |
| `F92` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 15.7 / 16.5 / **16.2** | 21.4 / 21.4 | 0.84 | -12% · X00 tiada keluar indikator (henti + 20 sesi) | +1.99 → +1.99 | 25 → 25 | 57 → 57 |
| `F58` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup >= 10% di atas SMA10 [aktif selepas +10%] | 19.9 / 20.5 / **22.3** | 26.5 / 28.6 | 0.95 | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +0.70 → +0.70 | 37 → 37 | 46 → 46 |
| `F41` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | 17.6 / 17.6 / **19.8** | 13.8 / 17.0 | 0.86 | -12% · X00 tiada keluar indikator (henti + 20 sesi) | +0.14 → +0.14 | 48 → 48 | 43 → 43 |
| `F45` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 16.2 / 16.2 / **16.2** | 18.0 / 18.0 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +3.18 → +3.18 | 26 → 26 | 54 → 54 |
| `F27` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 15.7 / 15.7 / **16.1** | 17.6 / 18.1 | 0.95 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.42 → +2.42 | 25 → 25 | 55 → 55 |
| `F03` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 17.7 / 17.7 / **17.9** | 19.4 / 19.1 | 0.92 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +3.35 → +3.35 | 28 → 28 | 54 → 54 |
| `F07` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 14.2 / 14.2 / **14.2** | 17.2 / 17.2 | 1.00 | -15% · X00 tiada keluar indikator (henti + 20 sesi) | +2.03 → +2.03 | 33 → 33 | 50 → 50 |
| `F11` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 15.2 / 15.3 / **15.8** | 16.8 / 16.9 | 0.94 | 5xATR14 · tutup >= 15% di atas SMA10 DAN Chandelier 2.0xATR14 dari tutup tertinggi [aktif selepas +10%] | +2.74 → +2.74 | 23 → 23 | 57 → 57 |
| `F95` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 16.6 / 16.6 / **16.6** | 19.4 / 19.4 | 1.00 | -8% · X00 tiada keluar indikator (henti + 20 sesi) | +1.21 → +1.21 | 49 → 49 | 41 → 41 |
| `F10` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 13.5 / 13.5 / **14.4** | 13.3 / 13.5 | 0.94 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.24 → +1.24 | 27 → 27 | 51 → 51 |
| `F24` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.8 / 13.8 / **13.8** | 14.8 / 14.8 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +0.79 → +0.79 | 32 → 32 | 49 → 49 |
| `F93` | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.6 / 12.6 / **12.6** | 16.7 / 16.7 | 1.00 | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.00 → +1.00 | 22 → 22 | 50 → 50 |
| `F42` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 15.1 / 15.1 / **15.1** | 11.5 / 11.5 | 1.00 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +3.90 → +3.97 | 27 → 27 | 54 → 54 |
| `F22` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 14.6 / 15.8 / **14.6** | 14.0 / 14.0 | 1.00 | -10% · X00 tiada keluar indikator (henti + 20 sesi) | +0.34 → +0.34 | 54 → 54 | 38 → 38 |
| `F16` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | 13.5 / 15.1 / **16.2** | 16.6 / 20.4 | 0.86 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.02 → +2.02 | 28 → 28 | 53 → 53 |
| `F02` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.9 / 12.9 / **12.9** | 14.5 / 14.5 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.30 → +2.30 | 22 → 22 | 57 → 57 |
| `F60` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 13.1 / 13.8 / **14.1** | 14.8 / 16.2 | 0.85 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +1.50 → +1.73 | 31 → 31 | 49 → 49 |
| `F48` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.5 / 13.5 / **13.5** | 21.6 / 21.6 | 1.00 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +1.46 → +1.46 | 30 → 30 | 50 → 50 |
| `F44` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.4 / 13.4 / **13.4** | 14.7 / 14.7 | 1.00 | -10% · X00 tiada keluar indikator (henti + 20 sesi) | +0.67 → +0.67 | 52 → 52 | 38 → 38 |
| `F06` | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 12.1 / 13.5 / **13.5** | 14.0 / 15.5 | 0.87 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.53 → +1.53 | 28 → 28 | 52 → 52 |
| `F29` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.8 / 12.8 / **12.8** | 11.5 / 11.5 | 1.00 | -10% · X00 tiada keluar indikator (henti + 20 sesi) | +0.09 → +0.09 | 54 → 54 | 38 → 38 |
| `F01` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.1 / 12.1 / **12.1** | 13.6 / 13.6 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.74 → +2.74 | 26 → 26 | 54 → 54 |
| `F25` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.9 / 12.9 / **12.9** | 13.5 / 13.5 | 1.00 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +0.68 → +0.74 | 33 → 33 | 48 → 48 |
| `F61` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.1 / 12.1 / **12.1** | 13.1 / 13.1 | 1.00 | -15% · X00 tiada keluar indikator (henti + 20 sesi) | +0.80 → +0.80 | 36 → 36 | 47 → 47 |
| `F05` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.9 / 11.9 / **11.9** | 12.9 / 12.9 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.58 → +1.58 | 28 → 28 | 52 → 52 |
| `F28` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 12.1 / 12.1 / **12.1** | 12.5 / 12.5 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.17 → +1.17 | 28 → 28 | 53 → 53 |
| `F09` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 12.1 / 14.0 / **14.3** | 14.7 / 17.7 | 0.88 | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +0.78 → +0.78 | 34 → 34 | 49 → 49 |
| `F30` | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 11.9 / 12.9 / **12.9** | 12.7 / 13.9 | 0.92 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +0.90 → +0.95 | 29 → 29 | 50 → 50 |
| `F08` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.4 / 11.4 / **11.4** | 12.9 / 12.9 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.45 → +1.45 | 28 → 28 | 51 → 51 |
| `F94` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 13.1 / 13.1 / **13.1** | 20.8 / 20.8 | 1.00 | -10% · X00 tiada keluar indikator (henti + 20 sesi) | -0.18 → -0.18 | 44 → 44 | 41 → 41 |
| `F62` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 34.7 / 34.7 / **35.1** | 41.7 / 41.7 | 0.95 | 5xATR14 · tutup >= 15% di atas SMA10 DAN Chandelier 2.0xATR14 dari tutup tertinggi [aktif selepas +10%] | +9.78 → +9.77 | 16 → 16 | 69 → 69 |
| `F52` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 19.9 / 19.9 / **19.9** | 6.5 / 6.5 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +4.12 → +4.12 | 20 → 20 | 61 → 61 |
| `F64` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 27.9 / 27.9 / **27.7** | 34.5 / 31.0 | 0.95 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +9.21 → +9.21 | 16 → 16 | 70 → 70 |
| `F67` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 27.8 / 27.8 / **28.1** | 43.6 / 44.5 | 0.97 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +8.48 → +8.48 | 16 → 16 | 70 → 70 |
| `F49` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | 29.6 / 30.6 / **31.3** | 33.3 / 34.5 | 0.91 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +5.46 → +5.46 | 21 → 21 | 64 → 64 |
| `F57` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN RSI2 > 95 [aktif selepas +10%] | 21.8 / 22.9 / **22.7** | 13.7 / 13.7 | 0.94 | -12% · X00 tiada keluar indikator (henti + 20 sesi) | +5.44 → +5.44 | 28 → 28 | 61 → 61 |
| `F53` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 20.1 / 20.1 / **20.1** | 8.3 / 8.3 | 1.00 | -12% · X00 tiada keluar indikator (henti + 20 sesi) | +4.56 → +4.56 | 26 → 26 | 62 → 62 |
| `F55` | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup >= 10% di atas SMA10 [aktif selepas +10%] | 24.9 / 24.9 / **24.9** | 34.0 / 34.0 | 1.10 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +8.16 → +8.16 | 10 → 10 | 74 → 74 |
| `F54` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 23.4 / 23.4 / **23.7** | 15.4 / 15.4 | 0.97 | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +7.17 → +7.17 | 18 → 18 | 66 → 66 |
| `F68` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 19.9 / 19.9 / **20.4** | 16.7 / 16.7 | 0.91 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +6.03 → +6.03 | 21 → 21 | 60 → 60 |
| `F69` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 24.8 / 24.8 / **24.6** | 22.7 / 22.1 | 0.95 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +6.79 → +6.79 | 17 → 17 | 67 → 67 |
| `F66` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 22.9 / 22.9 / **22.9** | 10.1 / 10.1 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +7.35 → +7.35 | 17 → 17 | 68 → 68 |
| `F15` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 16.1 / 16.3 / **16.8** | 10.8 / 12.4 | 0.94 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.72 → +2.72 | 24 → 24 | 56 → 56 |
| `F59` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 14.3 / 14.3 / **14.3** | 0.0 / 0.0 | 1.00 | 5xATR14 · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | +2.08 → +2.08 | 28 → 28 | 51 → 51 |
| `F23` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 14.7 / 14.7 / **14.7** | 11.2 / 11.2 | 1.00 | -12% · (tutup - SMA20) / ATR14 >= 3 DAN tutup < 85% tutup tertinggi sejak beli | -0.58 → -0.34 | 55 → 55 | 37 → 37 |
| `F14` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 14.7 / 15.0 / **15.4** | 12.9 / 13.6 | 0.93 | 5xATR14 · tutup >= 15% di atas SMA10 DAN Chandelier 2.0xATR14 dari tutup tertinggi [aktif selepas +10%] | +2.63 → +2.63 | 23 → 23 | 57 → 57 |
| `F12` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 16.1 / 16.1 / **16.9** | 8.3 / 9.4 | 0.92 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +3.68 → +3.68 | 22 → 22 | 58 → 58 |
| `F18` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 14.2 / 14.3 / **14.9** | 14.2 / 15.0 | 0.94 | 5xATR14 · tutup >= 15% di atas SMA10 DAN Chandelier 2.0xATR14 dari tutup tertinggi [aktif selepas +10%] | +2.25 → +2.25 | 24 → 24 | 55 → 55 |
| `F17` | 4xATR14 · 6 tutup naik berturut ATAU RSI7 > 85 [aktif selepas +10%] | 13.9 / 14.0 / **14.5** | 8.6 / 9.1 | 0.92 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.65 → +2.65 | 22 → 22 | 58 → 58 |
| `F26` | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 12.7 / 14.1 / **13.7** | 11.8 / 13.1 | 0.88 | 5xATR14 · (tutup - SMA20) / ATR14 >= 4 DAN tutup < 88% tutup tertinggi sejak beli [aktif selepas +10%] | +0.48 → +0.53 | 33 → 33 | 48 → 48 |
| `F46` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 11.7 / 11.7 / **11.7** | 18.6 / 18.6 | 1.00 | 3xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.25 → +1.25 | 25 → 25 | 56 → 56 |
| `F04` | 5xATR14 · tutup > jalur atas Bollinger(20, 3.0) ATAU RSI7 > 85 [aktif selepas +10%] | 13.8 / 14.5 / **14.5** | 10.7 / 12.5 | 0.84 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +2.89 → +2.89 | 25 → 25 | 55 → 55 |
| `F21` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 10.1 / 10.1 / **10.1** | 15.5 / 15.5 | 1.00 | -12% · X00 tiada keluar indikator (henti + 20 sesi) | -0.66 → -0.66 | 44 → 44 | 41 → 41 |
| `F47` | 4xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 10.1 / 10.1 / **10.1** | 11.5 / 11.5 | 1.00 | min(-10%, 4xATR14) · X00 tiada keluar indikator (henti + 20 sesi) | +0.58 → +0.58 | 24 → 24 | 54 → 54 |
| `F19` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 5.6 / 5.6 / **5.6** | 7.9 / 7.9 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.39 → +1.39 | 15 → 15 | 60 → 60 |
| `F20` | 5xATR14 · RSI14 silang turun bawah 80 ATAU RSI7 > 85 [aktif selepas +10%] | 6.5 / 6.8 / **6.8** | 4.9 / 6.3 | 0.85 | -15% · X00 tiada keluar indikator (henti + 20 sesi) | +1.52 → +1.52 | 19 → 19 | 58 → 58 |
| `F13` | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | 5.3 / 5.3 / **5.3** | 8.3 / 8.3 | 1.00 | 5xATR14 · X00 tiada keluar indikator (henti + 20 sesi) | +1.62 → +1.62 | 14 → 14 | 61 → 61 |

## 7. Kaveat

- Kumpulan B berkongsi HARI yang sama dengan kumpulan A: bagi keluar ikut pasaran (kelas P), saham B bukan ujian bebas; hanya 2025–26 (K3) yang tidak dilihat dari segi masa, dan ia pendek.
- Keluar dipilih pada A daripada ratusan ribu calon: angka A melambung, angka B dan K3 yang dibaca. Kumpulan B sudah dilihat dalam pusingan terdahulu.
- Tarikh earnings = tarikh pemfailan 8-K sebenar; "earnings pada sesi berikutnya" mengandaikan tarikh diumumkan lebih awal.
- Tiada saham delist. Registry F, kedudukan akhir dan kohort jejak TIDAK diubah oleh pusingan ini. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.
