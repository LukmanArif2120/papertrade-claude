# SPEC FASA 2 — data titik-masa (RS, gred kumpulan, earnings)

Dikunci **28 Okt 2026**, **sebelum datanya cukup untuk diuji**. Itu tujuannya: ujian dipradaftar
ketika hasilnya masih tidak diketahui, supaya ia tidak boleh dilenturkan kemudian.

Fasa 1 (`SPEC.md`, `KEPUTUSAN_FASA1.md`) dan 1b (`SPEC_1B.md`, `KEPUTUSAN_1B.md`) ditutup dan
tidak disentuh.

## 1. Satu hipotesis

Fasa 1 menguji 77 lajur indikator **harga** merentas enam tahun dan menolaknya. `DIAGNOSIS_FASA1.md`
menunjukkan mengapa: korelasi pangkat indikator harga terhadap **pulangan yang boleh didagangkan**
≈ 0 (1/30 konsisten, −0.027), walaupun terhadap puncak run bersyarat-hindsight ia sampai 0.124.

Hipotesis fasa 2, satu sahaja: **data titik-masa yang dikeluarkan daripada fasa 1 membawa kuasa
pemangkatan yang indikator harga tidak ada.**

## 2. Lajur yang diuji (dikunci; tiada tambahan separuh jalan)

| Kumpulan | Sumber | Liputan bermula |
|---|---|---|
| RS rating lawan seluruh pasaran AS | `BacktestShariah2/data/rs/rs_pasaran.csv` | 2026-09-15 |
| Gred sektor dan industri v2 | `BacktestShariah2/data/kumpulan/gred_kumpulan_sejarah.csv` | 2026-09-25 |
| EPS/hasil suku point-in-time, SUE, pecutan hasil | `BacktestShariah2/data/sec/eps_hasil.csv`, `sue.csv` | 2026-10-27 |
| Tarikh earnings 8-K Item 2.02 (jarak ke earnings, ±5 hari) | `BacktestShariah2/data/sec/earnings_8k.csv` | 2026-10-27 |

Tetapan standard sahaja. **Tiada penalaan parameter. Tiada Optuna.** Indikator berterusan diuji
pada dua hujung kuintil, atas populasi kuintil yang dibekukan pada larian pertama, seperti fasa 1.

## 3. Sasaran — pembetulan penting daripada fasa 1

Sasaran utama ialah **pulangan yang boleh didagangkan**: masuk buka esok, kos penuh (SPEC §3.1),
henti dan exit dinyatakan, ufuk dinyatakan. **Bukan** puncak run.

Fasa 1 mengukur lift terhadap hasil run yang bersyarat pada hindsight (hanya 15–18% peristiwa
menjadi run), dan itu menghasilkan lift 10–24 kali yang hilang sepenuhnya dalam dagangan. Fasa 2
tidak mengulangi kesilapan itu: setiap keputusan dibuat atas pulangan selepas kos.

## 4. Ambang data minimum sebelum penilaian PERTAMA (dikunci)

Penilaian **tidak boleh** dijalankan sebelum **kesemua** dipenuhi:

- **≥ 250 hari dagangan** liputan bertindih antara lajur yang diuji dan Lejar Penuh
- **≥ 3,000 peristiwa sah** dengan nilai lajur itu tidak kosong
- **≥ 2 suku kalendar penuh** data

Pada 28 Okt 2026: RS ≈ 30 hari dagangan, gred ≈ 23, SEC ≈ 1. **Belum cukup.** Anggaran penilaian
pertama: sekitar **Okt 2027**.

## 5. Ujian (dipradaftar)

1. **Pemangkatan** — Spearman antara setiap lajur dan pulangan boleh didagangkan, dikira
   **setiap suku**. Lajur diteruskan hanya jika tandanya konsisten dalam **≥ 4 daripada 6** suku
   pertama dan |rho| purata ≥ 0.05.
2. **Kehadiran** — metrik Step 4 fasa 1 (K_padu, lift, presisi, lift_presisi) atas populasi
   keputusan, dengan KAWALAN RAWAK yang sama.
3. **Kawalan kebetulan** — label rawak 1000×, bootstrap blok 1000× (blok ticker **dan** blok
   minggu), BH-FDR q ≤ 0.01 dalam keluarga **`FASA2`** sendiri. Tolak jika had bawah 95% jangkaan
   ≤ 0 dalam mana-mana skema blok, atau jika jangkaan ≤ 0 tanpa 5% pemenang teratas.
4. **Portfolio** — 10 slot (selari `portfolio_slot/`), kos penuh, dua saiz: tetap 10% dan berskala
   risiko (SPEC_1B, k = 4, risiko 1.0%).

## 6. Ambang penerimaan (dikunci sekarang, tidak boleh diubah selepas melihat hasil)

Fasa 2 diterima sebagai penemuan hanya jika lajur yang sama:

1. lulus §5.1 **dan** §5.3; **dan**
2. mengalahkan **asas harga-sahaja** (fungsi pangkat indikator harga terbaik fasa 1, yang
   |rho|-nya ≈ 0) pada pulangan boleh didagangkan; **dan**
3. mengalahkan **KAWALAN RAWAK** dalam portfolio §5.4 pada pulangan **dan** MDD.

Jika tidak: fasa 2 **DITOLAK** dan dilaporkan sebagai ditolak, sama seperti fasa 1 dan 1b.

## 7. Had yang diakui lebih awal

- Tempoh ujian bermula 2026 — **satu rejim pasaran sahaja**. Keputusan tertinggi fasa 2 ialah
  **CALON** sehingga dua tempoh bebas disahkan.
- Lejar Penuh **tiada bias survivorship** (ia jejak hadapan sebenar) — ini **lebih baik** daripada
  data A02 fasa 1, dan satu sebab fasa 2 berbaloi walaupun fasa 1 ditolak.
- Saiz sampel akan kecil pada mulanya; §4 ada untuk mengelak kesimpulan awal.

## 8. Apa yang fasa 2 BUKAN

Bukan percubaan kedua pada indikator harga. Jika seseorang mahu menguji indikator harga lagi,
`KEPUTUSAN_FASA1.md` dan `DIAGNOSIS_FASA1.md` ialah jawapannya: enam tahun, empat rejim,
20,640 ujian ENTRY, 108 ujian 1b — ruang itu kosong.
