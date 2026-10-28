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

- **≥ 250 hari dagangan** liputan bertindih antara lajur yang diuji dan populasi peristiwa sah ~~dan Lejar Penuh~~ (**dibetulkan §9.1**)
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
4. **Portfolio** — **8 slot × 12.5%** seperti REVERSE Step 9 ~~10 slot (selari `portfolio_slot/`)~~
   (**dibetulkan §9.1**), kos penuh, dua saiz: tetap 12.5% dan berskala risiko (SPEC_1B, k = 4,
   risiko 1.0%).

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


---

## 9. Pindaan bertarikh

### 9.1 — 28 Okt 2026: populasi peristiwa dan saiz portfolio dibetulkan (bukan Lejar, bukan 10 slot)

**Kesilapan penulis spec, ditemui oleh pengguna.** Draf pertama SPEC_FASA2 menetapkan populasi
ujian sebagai **Lejar Penuh** (§4) dan portfolio **10 slot selari `portfolio_slot/`** (§5.4).
Kedua-duanya salah: Lejar Penuh dan `portfolio_slot/` ialah rekod isyarat **134 kaedah Mxx**.

Arahan asal kajian ini menyatakannya tanpa kekaburan:

> *"Kajian ini menguji signal dan indikator sahaja — BUKAN kaedah Mxx dalam repo, dan BUKAN
> penalaan parameter."*

Menguji RS/gred/earnings atas belian Mxx menjawab soalan yang **berbeza** — sama ada data itu
menambah kuasa pemangkatan **dalam kalangan isyarat kaedah Mxx** — bukan soalan kajian ini, iaitu
sama ada data itu menambah kuasa yang indikator harga tidak ada, atas populasi peristiwa yang sama
seperti fasa 1.

**Dibetulkan:**

| Perkara | Draf pertama (salah) | Dikunci sekarang |
|---|---|---|
| Populasi ujian | belian Lejar Penuh (isyarat Mxx) | **peristiwa sah `SPEC.md` §7**: tutup ≥ 5% di atas rendah terendah 20 hari DAN tutup > EMA21, hari pertama dalam ≤ 10 hari dagangan — kausal, bebas kaedah |
| Portfolio §5.4 | 10 slot × 10% (`portfolio_slot/`) | **8 slot × 12.5%** seperti REVERSE Step 9, supaya setanding fasa 1 |
| Universe | tidak dinyatakan | universe A02 titik-masa, sama seperti fasa 1 |
| Kawalan | tidak dinyatakan | KAWALAN RAWAK dan asas harga-sahaja, sama seperti fasa 1 |

**Mengapa pembetulan ini sah:** pada tarikh ini fasa 2 berada pada **30 / 250** hari dagangan —
**tiada data dinilai, tiada hasil dilihat**. Itulah satu-satunya keadaan di mana spec yang dikunci
boleh dibetulkan tanpa menjejaskan integriti pradaftar. Draf pertama dikekalkan dalam sejarah git.

**Tiada infrastruktur baharu diperlukan.** Peristiwa sah ialah fungsi deterministik stor harga
(`BacktestShariah2/data/harga/stor/`), yang dipelihara setiap hari, dan RS/gred/SEC direkod setiap
hari. Maka join peristiwa × data titik-masa boleh dibuat **secara retrospektif** pada Okt 2027
dengan menjalankan semula pengesan peristiwa REVERSE atas stor. Yang perlu ditunggu ialah **masa**,
bukan kod.

### 9.2 — 28 Okt 2026: lorong `RISIKO_10` bukan ujian ke hadapan fasa 1b

Lorong `RISIKO_10` yang ditambah ke `standard/portfolio_slot.py` pada 28 Okt 2026 pada mulanya
diterangkan sebagai "ujian ke hadapan bagi dapatan fasa 1b". **Itu terlebih-dakwa.**
`portfolio_slot/` membeli daripada Lejar Penuh, iaitu isyarat **kaedah Mxx** — populasi kemasukan
yang sama sekali berbeza daripada signal REVERSE yang menghasilkan dapatan 1b.

Apa yang `RISIKO_10` sebenarnya uji: sama ada saiz berskala risiko memperbaiki drawdown **atas
isyarat Mxx**. Mekanisme saiz itu umum, jadi hasilnya tetap bermaklumat — tetapi ia **bukan**
pengesahan atau penafian dapatan 1b. Ujian ke hadapan yang betul bagi 1b memerlukan lorong yang
kemasukannya daripada peristiwa sah REVERSE, bukan daripada Lejar.
