# L01 — Keputusan Ujian: Penapis Rejim Crash (lapisan, enjin v1.2)

**Tarikh:** 17 Okt 2026 · **Data:** `data_mentah/dataset_S1–S4` (431 saham) + `index_benchmark` · **Tempoh:** 1 Nov 2019 – 2 Okt 2026 · **Portfolio:** 8 slot × 12.5% · **Spec:** `SPEC_SEMUA_KAEDAH.md` (`FAIL ASAL: spec/L01`) · **Skrip:** `WFO/kaedah_baru/step2_L01.py` · **Output:** `data/lapisan/L01.csv` (lajur LAJUR2; 6 kaedah × 4 versi × 5 set = 120 baris; BUKAN dalam `registry_M_gabung.csv`)

**Verdict ringkas:** DITOLAK. Tiada bendera (A, B, C) lulus kriteria penerimaan bagi mana-mana kaedah daripada 5 (0/5 bagi ketiga-tiganya). Lapisan tidak menambah baik MDD ≥ 3 mata peratus pada mana-mana kaedah.

## 1. Cara ujian
| Perkara | Takrif |
|---|---|
| Lapisan | sig_L = sig DAN BUKAN bendera_i (tutup hari i). Posisi sedia ada ikut peraturan keluar asal. Penapis dipasang selepas `sedia()` modul (exitc modul tidak bergantung pada sig). Bagi M114 V4 dan M166 V1 (Rangka R), exitc dikira semula selepas penapis (kerana Rangka R bergantung pada sig) |
| Bendera A | SPY C_i ÷ C_{i−252} − 1 < 0 (282 hari dalam sampel) |
| Bendera B | SPY C_i ÷ C_{i−504} − 1 < 0 (29 hari) |
| Bendera C | A DAN turun naik SPY 63 hari (SD harian × √252) > persentil ke-80 terkumpul (min 252 hari) (160 hari) |
| Kaedah | M96 V1, M30 V3, M79 V3, M111 V5 (modul `kod/kaedah/`), M114 V4 (Rangka R, kolam RS12 10%). Tambahan maklumat: M166 V1 (lulus STEP-2); tidak dikira dalam kriteria 5 kaedah |
| Pengesahan asas | Semua lima asas dihasilkan semula tepat daripada registry: M96 40.04%/−42.05%/294, M30 52.02%/−36.75%/3859, M79 35.52%/−39.87%/7146, M111 43.03%/−34.88%/8538, M114 49.64%/−38.80%/2619 |
| Kriteria (ditetapkan sebelum ujian) | Lulus bagi kaedah: MDD bertambah baik ≥ 3 mata DAN CAGR tidak turun > 2 mata, DAN arah sama dalam ≥ 3/4 subset. Lapisan diterima jika ≥ 3/5 kaedah lulus |

**Andaian saya:** "arah sama" dalam subset = MDD subset tidak lebih buruk DAN CAGR subset tidak turun > 2 mata berbanding asas subset; isyarat dikira atas 431 saham dan subset hanya menapis saham; persentil turun naik terkumpul termasuk hari i (tiada pandang ke hadapan); `cari()` enjin dihalakan ke `data_mentah/`, enjin tidak diubah.

## 2. Hasil (set 431)
| Kaedah | Bendera | CAGR asas → L01 | MDD asas → L01 | Dagangan | ΔMDD | ΔCAGR | Subset: MDD tidak lebih buruk & CAGR tidak turun >2 mata | Lulus |
|---|---|---|---|---|---|---|---|---|
| M96 V1 | A | 40.0% → 30.3% | -42.0% → -42.0% | 294 → 263 | +0.0 | -9.7 | 2/4 | Tidak |
| M30 V3 | A | 52.0% → 45.8% | -36.8% → -36.0% | 3859 → 3382 | +0.7 | -6.2 | 3/4 | Tidak |
| M79 V3 | A | 35.5% → 25.9% | -39.9% → -40.3% | 7146 → 5422 | -0.4 | -9.6 | 0/4 | Tidak |
| M111 V5 | A | 43.0% → 35.2% | -34.9% → -36.2% | 8538 → 7335 | -1.3 | -7.8 | 0/4 | Tidak |
| M114 V4 | A | 49.6% → 55.2% | -38.8% → -38.0% | 2619 → 2398 | +0.8 | +5.6 | 4/4 | Tidak |
| M166 V1 (tambahan) | A | 58.1% → 60.6% | -40.4% → -41.1% | 3276 → 2552 | -0.7 | +2.5 | 2/4 | Tidak |
| M96 V1 | B | 40.0% → 39.6% | -42.0% → -42.0% | 294 → 293 | +0.0 | -0.4 | 4/4 | Tidak |
| M30 V3 | B | 52.0% → 48.9% | -36.8% → -37.1% | 3859 → 3825 | -0.3 | -3.1 | 1/4 | Tidak |
| M79 V3 | B | 35.5% → 33.0% | -39.9% → -39.9% | 7146 → 7006 | +0.0 | -2.5 | 3/4 | Tidak |
| M111 V5 | B | 43.0% → 42.7% | -34.9% → -36.2% | 8538 → 8376 | -1.4 | -0.4 | 2/4 | Tidak |
| M114 V4 | B | 49.6% → 49.3% | -38.8% → -38.2% | 2619 → 2606 | +0.6 | -0.4 | 1/4 | Tidak |
| M166 V1 (tambahan) | B | 58.1% → 55.9% | -40.4% → -40.4% | 3276 → 3261 | +0.0 | -2.3 | 3/4 | Tidak |
| M96 V1 | C | 40.0% → 31.4% | -42.0% → -42.0% | 294 → 282 | +0.0 | -8.6 | 3/4 | Tidak |
| M30 V3 | C | 52.0% → 46.7% | -36.8% → -36.7% | 3859 → 3620 | +0.0 | -5.3 | 2/4 | Tidak |
| M79 V3 | C | 35.5% → 38.8% | -39.9% → -39.9% | 7146 → 6215 | +0.0 | +3.3 | 2/4 | Tidak |
| M111 V5 | C | 43.0% → 47.1% | -34.9% → -36.2% | 8538 → 7926 | -1.3 | +4.0 | 1/4 | Tidak |
| M114 V4 | C | 49.6% → 53.7% | -38.8% → -38.8% | 2619 → 2530 | +0.0 | +4.0 | 4/4 | Tidak |
| M166 V1 (tambahan) | C | 58.1% → 57.7% | -40.4% → -41.1% | 3276 → 2851 | -0.7 | -0.5 | 1/4 | Tidak |

Lulus mengikut bendera: A 0/5, B 0/5, C 0/5.

## 3. Penemuan penting
1. MDD hampir tidak berubah: perubahan terbesar ialah +0.8 mata (M114 A); daripada 15 pasangan kaedah×bendera (5 kaedah × 3), 3 memperbaiki MDD, 7 tidak berubah dan 5 memburukkannya. Pembaikan maksimum 0.8 mata, jauh di bawah ambang 3 mata. Titik terburuk portfolio berlaku di luar hari bendera, atau portfolio sudah ke tunai kerana penapis SPY/syarat kaedah sendiri.
2. Bendera A merosakkan CAGR kaedah yang tidak mempunyai penapis SPY: M96 −9.7, M79 −9.6, M111 −7.8, M30 −6.2 mata. Hanya M114 V4 (+5.6) dan M166 V1 (+2.5) dipertingkat, tetapi MDD mereka tidak bertambah baik.
3. Bendera B (504 hari) hampir tiada kesan (29 hari), sebagaimana dijangka dalam spec.
4. Bendera C menambah CAGR M79 (+3.3), M111 (+4.0), M114 (+4.0), tetapi MDD tidak bertambah baik; ia memburukkan M96 (−8.6) dan M30 (−5.3).
5. Sampel hanya satu-dua episod bear (2020, 2022, awal 2025); ujian tidak boleh membezakan hasil sebenar daripada kebetulan.

## 4. Verdict
**L01 DITOLAK: 0/5 kaedah lulus bagi setiap bendera (MDD tidak bertambah baik ≥ 3 mata pada mana-mana kaedah). Bendera A kekal paling ringkas tetapi mengurangkan CAGR 6–10 mata pada empat kaedah. Tiada perubahan pada rutin harian atau Papertrade C.**

## 5. Batasan
- Skala turun naik (Barroso & Santa-Clara; Daniel & Moskowitz) tidak boleh diuji kerana `portfolio()` enjin v1.2 beku (saiz posisi tetap).
- Senarai Shariah ialah senarai hari ini (bias kemandirian); harga terlaras.
- Tetingkap 36 bulan (Cooper) diganti 504 hari kerana data bermula 2019.
- Pertindihan dengan penapis SPY > SMA200 dalam M114 dan Rangka R.
- 2026 separa (hingga 2 Okt 2026).
- Andaian dalam Bahagian 1.

`data/lapisan/L01.csv` disimpan (120 baris); tidak ditambah ke `registry_M_gabung.csv`.
