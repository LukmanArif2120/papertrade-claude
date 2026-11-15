# CS10: keluar daripada maklumat baharu pada LORONG TREND `T01`–`T12` (pegang hingga 6 bulan; backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_keluar10.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (s), dikomit sebelum dijalankan. **Jangan sunting secara manual.**

## 1. Apa yang dicari

- CS08 menguji 38 indikator "trend tamat" TUNGGAL daripada harga saham sendiri (tiada yang menolong). Pusingan ini menambah **90 atom baharu**: P = pasaran (22); S = sektor/industri (2); E = peristiwa syarikat (10); R = relatif kepada pasaran (6); K = kemuncak / terlalu panas (24); L = keadaan laluan/saham (26), dan menguji SEMUA pasangan (ATAU, DAN).
- 16,385 peraturan × 3 syarat aktif × 6 henti = **294,930 cara keluar setiap setup**, bagi 12 setup papan CS08, dipilih pada kumpulan A sahaja.
- Ukuran: **dijual dengan untung ≥ +30 %** (sama seperti CS08). Syarat "tidak jual awal": untung terealisasi pada pelari besar (naik ≥ +50 % sebelum jatuh −15 %) mesti ≥ 90% daripada "pegang sahaja 126 sesi". 106,529 cara lulus syarat itu pada A.
- Pegang minimum 3 sesi terpakai; henti rugi kekal aktif.

## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)

**Bacaan 1 — keluar lorong trend ("pegang sampai trend tamat"):**

- Keluar terpilih mengatasi `X00` (pegang sahaja, henti sama): **8 daripada 12** setup; mengatasi keluar CS08: **9 daripada 12**; kedua-duanya: **8 daripada 12** (perlu lebih separuh).
- Nisbah simpan (median): 1.00 (perlu ≥ 0.90). Rugi ≥ 15 %: median beza lawan keluar CS08 -1.5 mata (perlu ≤ +1.0).
- 2025–26 (K3, digabung merentas setup; 805 isyarat): tambahan dijual ≥ +30 % lawan pegang sahaja +0.75 mata (perlu > 0).
- Median dijual ≥ +30 %: pegang sahaja 24.0 % → keluar terpilih **27.0 %**; rugi ≥ 15 % 44.7 % → 44.3 %; untung pada pelari besar +55 % → +53 %.
- **Keputusan bacaan 1: keluar baharu MENOLONG.**

**Bacaan 2 — sisi rugi (adakah keluar baharu mengurangkan rugi tanpa menjual pelari besar):**

- Purata dagangan lebih tinggi DAN rugi ≥ 15 % lebih rendah daripada pegang sahaja (henti sama), tanpa mengurangkan "dijual ≥ +30 %" lebih 0.5 mata: **4 daripada 12** setup (perlu lebih separuh).
- Nisbah simpan (median): 1.00. 2025–26 (digabung): tambahan purata dagangan +0.07 mata (perlu > 0).
- Median merentas setup: purata dagangan pegang sahaja +3.74 % → terpilih **+4.13 %**; rugi ≥ 15 % 47.7 % → **47.7 %**; menang 40 % → 40 %; median dagangan -13.1 % → -13.1 %.
- **Keputusan bacaan 2: potong rugi TIDAK menolong.**

## 3. Keluar sejagat ikut "dijual ≥ +30 %" (senarai T; dipilih pada A, disemak pada B)

Komposisi kelas: K 10.

| # | Henti | Peraturan keluar | Kelas | A: tambahan (mata) | A: nisbah simpan | B: tambahan (mata) | B: % setup lebih baik | B: nisbah simpan | B: beza rugi ≥ 15 % | 2025–26: tambahan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | -20% | tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +2.05 | 0.95 | +2.82 | 100% | 0.90 | -2.4 | +1.86 |
| 2 | 4xATR14 | tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.88 | 0.95 | +2.58 | 92% | 0.90 | -2.4 | +1.74 |
| 3 | -20% | tutup >= 10% di atas SMA10 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.74 | 0.94 | +2.35 | 100% | 0.89 | -2.2 | +2.98 |
| 4 | -15% | tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.69 | 0.94 | +2.65 | 92% | 0.90 | -2.8 | +1.61 |
| 5 | min(-15%, 5xATR14) | tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.64 | 0.94 | +2.54 | 100% | 0.90 | -2.2 | +1.74 |
| 6 | 4xATR14 | tutup >= 10% di atas SMA10 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.60 | 0.95 | +2.14 | 83% | 0.89 | -2.0 | +2.86 |
| 7 | -15% | tutup >= 10% di atas SMA10 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.58 | 0.94 | +2.35 | 100% | 0.89 | -2.5 | +2.73 |
| 8 | -10% | tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.47 | 0.93 | +1.92 | 92% | 0.87 | -0.3 | +0.87 |
| 9 | 6xATR14 | tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.31 | 0.93 | +2.50 | 100% | 0.90 | -1.9 | +1.74 |
| 10 | min(-15%, 5xATR14) | tutup >= 10% di atas SMA10 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | K | +1.29 | 0.94 | +2.07 | 83% | 0.89 | -1.9 | +2.86 |

## 4. Keluar sejagat ikut sisi rugi (senarai R)

Komposisi kelas: P 8, K+P 2.

| # | Henti | Peraturan keluar | Kelas | A: tambahan purata dagangan (mata) | A: tambahan dijual ≥ +30 % | A: nisbah simpan | B: tambahan purata | B: % setup lebih baik | B: beza rugi ≥ 15 % | B: nisbah simpan | 2025–26: tambahan purata |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4xATR14 | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | P | +0.57 | +0.18 | 1.02 | +0.25 | 67% | -1.3 | 1.00 | -0.41 |
| 2 | -15% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 | P | +0.49 | +0.10 | 1.02 | +0.39 | 83% | -3.2 | 1.00 | +0.06 |
| 3 | -15% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | P | +0.47 | +0.28 | 1.02 | +0.37 | 75% | -1.7 | 1.00 | +0.05 |
| 4 | -15% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +10%] | P | +0.47 | +0.12 | 1.02 | +0.42 | 83% | -2.4 | 1.00 | +0.04 |
| 5 | -20% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | P | +0.40 | +0.09 | 1.01 | +0.34 | 67% | -1.8 | 1.00 | -0.10 |
| 6 | -10% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | P | +0.29 | +0.34 | 1.03 | +0.26 | 75% | -0.0 | 1.00 | +0.14 |
| 7 | -10% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +10%] | P | +0.26 | +0.24 | 1.03 | +0.25 | 75% | -0.0 | 1.00 | +0.13 |
| 8 | -10% | pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 | P | +0.25 | +0.19 | 1.03 | +0.26 | 75% | -0.0 | 1.00 | +0.15 |
| 9 | -15% | pasaran: QQQ tutup < rendah 5 hari DAN tutup >= 100% di atas SMA200 [aktif selepas +20%] | K+P | +0.24 | +0.39 | 1.03 | -0.00 | 50% | -1.0 | 0.99 | -1.83 |
| 10 | -10% | pasaran: QQQ tutup < rendah 5 hari DAN tutup >= 100% di atas SMA200 [aktif selepas +20%] | K+P | +0.17 | +0.37 | 1.04 | -0.23 | 42% | -0.0 | 0.97 | -2.32 |

## 5. Setiap kelas maklumat: atom tunggal terbaik (dipilih pada A; maklumat, bukan bacaan)

Plasebo = siri yang sama dianjak 437 sesi (kelas P, S, E sahaja): jika plasebo sama baik, kelas itu tidak membawa maklumat.

| Kelas | Ikut | Atom tunggal terbaik (henti) | A (mata) | B (mata) | B: % setup lebih baik | B: nisbah simpan | B: beza rugi ≥ 15 % | 2025–26 | Plasebo: A / B |
|---|---|---|---|---|---|---|---|---|---|
| P pasaran | dijual ≥ +30 % | pasaran: QQQ RSI14 < 35 [aktif selepas +20%] (-10%) | -4.33 | -2.01 | 0% | 0.82 | -0.2 | -3.11 | – |
| P pasaran | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – | – |
| S sektor/industri | dijual ≥ +30 % | tiada yang lulus syarat | – | – | – | – | – | – | – |
| S sektor/industri | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – | – |
| E peristiwa syarikat | dijual ≥ +30 % | reaksi earnings terakhir (0-5 sesi lalu) <= -10% [aktif selepas +20%] (-10%) | -1.40 | +0.01 | 33% | 0.99 | -0.2 | -1.74 | -1.54 / -0.26 |
| E peristiwa syarikat | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – | – |
| R relatif kepada pasaran | dijual ≥ +30 % | pulangan 60 sesi saham - QQQ <= -30% [aktif selepas +20%] (-10%) | -0.79 | -0.47 | 0% | 1.00 | -0.1 | -0.25 | – |
| R relatif kepada pasaran | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – | – |
| K kemuncak / terlalu panas | dijual ≥ +30 % | (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] (4xATR14) | +0.85 | +2.38 | 92% | 0.87 | -2.4 | +1.86 | – |
| K kemuncak / terlalu panas | purata dagangan | tutup >= 70% di atas SMA50 (-10%) | -0.53 | +0.01 | 67% | 1.00 | +0.0 | -0.73 | – |
| L keadaan laluan/saham | dijual ≥ +30 % | Chandelier 6xATR14 hingga tutup tertinggi >= +50%, kemudian 3xATR14 [aktif selepas +20%] (-10%) | +0.56 | +0.50 | 67% | 0.87 | -0.5 | -0.50 | – |
| L keadaan laluan/saham | purata dagangan | Chandelier 6xATR14 hingga tutup tertinggi >= +50%, kemudian 3xATR14 (-10%) | -3.44 | -1.21 | 8% | 0.87 | -0.5 | -5.02 | – |
| lama atom CS08 (harga saham sendiri) | dijual ≥ +30 % | Chandelier 8.0xATR14 dari tutup tertinggi (-10%) | -0.84 | -0.51 | 0% | 1.00 | -0.1 | -0.87 | – |
| lama atom CS08 (harga saham sendiri) | purata dagangan | tiada yang lulus syarat | – | – | – | – | – | – | – |

## 6. Setiap setup (kumpulan B; semua isyarat, perbandingan berpasangan)

| ID | Isyarat | Keluar terpilih-T | Dijual ≥ +30 %: pegang sahaja → **T** | Untung pada pelari besar: pegang → T | Nisbah simpan | Keluar terpilih-R | Purata %: pegang → R | Median %: pegang → R | Rugi ≥ 15 %: pegang → R | Menang %: pegang → R |
|---|---|---|---|---|---|---|---|---|---|---|
| `T01` | 499 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 32.7 → **32.7** | +68 → +68 | 1.00 | -20% · pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | +16.1 → +16.4 | +0.0 → +0.2 | 44 → 43 | 50 → 50 |
| `T02` | 493 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 34.1 → **34.1** | +70 → +70 | 1.00 | -20% · pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | +17.6 → +17.9 | +0.7 → +1.4 | 43 → 42 | 51 → 52 |
| `T03` | 437 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 26.3 → **26.3** | +66 → +66 | 1.00 | -15% · X00 tiada keluar indikator (henti + 126 sesi) | +9.3 → +9.3 | -15.5 → -15.5 | 61 → 61 | 37 → 37 |
| `T04` | 452 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 25.9 → **27.7** | +52 → +53 | 1.02 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | +3.2 → +3.2 | -12.0 → -12.0 | 47 → 47 | 41 → 41 |
| `T05` | 543 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 18.6 → **21.4** | +55 → +49 | 0.89 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | +2.2 → +2.2 | -14.2 → -14.2 | 48 → 48 | 40 → 40 |
| `T06` | 452 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 25.9 → **27.7** | +52 → +53 | 1.02 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | +3.2 → +3.2 | -12.0 → -12.0 | 47 → 47 | 41 → 41 |
| `T07` | 771 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 23.1 → **27.9** | +52 → +52 | 1.00 | -20% · pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | +4.3 → +5.0 | -20.5 → -20.5 | 55 → 54 | 38 → 40 |
| `T08` | 509 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 21.4 → **23.0** | +55 → +49 | 0.88 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | +0.9 → +0.9 | -21.4 → -21.4 | 52 → 52 | 36 → 36 |
| `T09` | 309 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 20.7 → **23.9** | +34 → +43 | 1.24 | -15% · pasaran: QQQ tutup < rendah 5 hari DAN tutup >= 100% di atas SMA200 [aktif selepas +20%] | -2.7 → -0.6 | -15.5 → -15.5 | 75 → 73 | 22 → 24 |
| `T10` | 1024 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 18.2 → **21.0** | +52 → +46 | 0.88 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | +1.2 → +1.2 | -14.3 → -14.3 | 48 → 48 | 36 → 36 |
| `T11` | 342 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 19.0 → **19.0** | +62 → +62 | 1.00 | -20% · pasaran: turun-naik SPY 21 hari >= 25% setahun DAN pasaran: QQQ tutup < SMA50 [aktif selepas +20%] | +6.5 → +6.4 | -9.3 → -8.1 | 46 → 45 | 42 → 43 |
| `T12` | 426 | 6xATR14 · tutup >= 30% di atas SMA50 DAN (tutup - SMA50) / ATR14 >= 6 [aktif selepas +20%] | 24.9 → **27.7** | +66 → +53 | 0.81 | min(-15%, 5xATR14) · X00 tiada keluar indikator (henti + 126 sesi) | +10.9 → +10.9 | -7.1 → -7.1 | 46 → 46 | 46 → 46 |

## 7. Kaveat

- Pariti dengan CS08: "dijual ≥ +30 %" `X00` setiap setup berbeza paling banyak 0.000 mata daripada `hasil/CS08/papan.csv`; bilangan belian satu posisi sama bagi 12 daripada 12 setup.
- Hanya 12 setup dan beberapa berkongsi pencetus/prasyarat: bukan 12 ujian bebas.
- Kumpulan B berkongsi HARI yang sama dengan kumpulan A: bagi keluar ikut pasaran (kelas P) saham B bukan ujian bebas; 2025–26 pendek (tetingkap 126 sesi berakhir ~April 2026).
- Ratusan ribu calon atas beberapa ratus isyarat setiap setup: angka A melambung, angka B yang dibaca.
- Tiada saham delist — bias LEBIH besar bagi pegangan 6 bulan. Papan `T01`–`T12` tidak diubah. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.
