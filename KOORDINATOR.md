# KOORDINATOR — keadaan repo dalam satu halaman

Dijana `BacktestShariah2/standard/koordinator.py` pada 2026-11-05 09:58 (waktu pelayan). Tiada rangkaian, tiada LLM, tiada penalaan — semuanya dibaca daripada fail keadaan repo. **Jangan ubah manual.**

## 0. Salinan kerja

| Cawangan | HEAD | Commit di belakang origin/main | origin/main (fetch terakhir) |
|---|---|---|---|
| main | 2026-11-05 | 0 | 2026-11-05 |


Selari dengan `origin/main` pada fetch terakhir — angka kesegaran di bawah boleh dipercayai.


## 1. Perlu keputusan anda (0)

Tiada. (`BacktestShariah2/koordinator/keputusan.csv` tiada baris `terbuka`.)


## 2. Kajian REVERSE — signal dan indikator (BUKAN kaedah Mxx)

REVERSE menguji **signal dan indikator** untuk ENTRY/HOLD/EXIT. Ia **tidak** menguji 134 kaedah Mxx repo dan tidak menala parameter. Populasi ujiannya ialah **peristiwa sah** (`REVERSE/SPEC.md` §7: tutup ≥ 5% di atas rendah terendah 20 hari DAN tutup > EMA21, kausal) atas universe A02 — bukan Lejar Penuh, bukan `portfolio_slot/`. Jangan campurkan kedua-dua jejak (`REVERSE/SPEC_FASA2.md` §9).


### Ambang fasa 2 (`SPEC_FASA2.md` §4: ≥ 250 hari dagangan liputan bertindih, ≥ 3,000 peristiwa sah, ≥ 2 suku penuh)

| Sumber | Hari dagangan | Mula | Akhir | Suku (anggaran) | Baris | Cukup? |
|---|---|---|---|---|---|---|
| RS pasaran | 30 | 2026-09-24 | 2026-11-04 | 0.5 |  | tidak |
| Gred kumpulan | 29 | 2026-09-25 | 2026-11-04 | 0.5 |  | tidak |
| SEC EPS/hasil | 4099 | 2009-04-15 | 2026-11-04 | 65.1 | 269728 | ya |
| SEC earnings 8-K | 5452 | 2004-08-23 | 2026-11-04 | 86.5 | 179342 | ya |


Leg **RS/gred**: terbaik **30 / 250** hari dagangan. Peristiwa sah ialah fungsi deterministik stor harga, jadi join peristiwa × data titik-masa boleh dibuat **retrospektif** — yang perlu ditunggu ialah masa, bukan kod.


Leg **SEC** tidak menunggu: nilai pertama difail = titik-masa retrospektif sejak 2009 (`SPEC_FASA2.md` §4.1). Halangannya **liputan ticker**: 2847 daripada 3302 ticker universe ada data EPS/hasil, 0 belum diisi. Universe REVERSE kira-kira 2,300 setahun.


## 3. Operasi repo — 134 kaedah Mxx dan papertrade C

Jejak berasingan daripada §2. Semua di bawah ini dipacu oleh isyarat kaedah **Mxx** melalui Lejar Penuh.


### Lorong portfolio_slot (bacaan adil ≥ 6 bulan, `kajian/KAJIAN_PORTFOLIO.md`)

| Lorong | Ekuiti | Dipegang | Keluar | Sesi terakhir |
|---|---|---|---|---|
| RS_10 | 0.810341 | 10 | 2 | 2026-11-04 |
| RAWAK_10 | 0.956952 | 10 | 2 | 2026-11-04 |
| GABUNGAN_10 | 1.025026 | 7 | 22 | 2026-11-04 |
| TOP1_10 | 1.012464 | 9 | 24 | 2026-11-04 |
| RAWAK_KAEDAH_10 | 0.978849 | 10 | 1 | 2026-11-04 |
| RISIKO_10 | 0.943928 | 10 | 2 | 2026-11-04 |


`RISIKO_10` (sejak 28 Okt 2026) dipasangkan dengan `RS_10`: susunan calon sama, hanya saiz berbeza. **MDD-nya mesti dibaca bersama lajur `tunai`** — pendedahannya lebih rendah, jadi sebahagian kelebihan MDD datang daripada pendedahan, bukan saiz. Ia menguji saiz atas **isyarat Mxx** dan bukan ujian ke hadapan dapatan REVERSE fasa 1b (`REVERSE/SPEC_FASA2.md` §9.2).


### Papan Penganalisis — 228 kaedah Mxx

| Status pantau | Bilangan |
|---|---|
| BELUM CUKUP | 221 |
| OK | 7 |


## 4. Kesegaran data

| Sumber | Terakhir | Umur (hari) | Status |
|---|---|---|---|
| Stor harga | 20261104 | 1 | OK |
| Trend D10H2-r2 | 20261104 | 1 | OK |
| Lejar Penuh | 2026-11-04 | 1 | OK |
| portfolio_slot | 2026-11-04 | 1 | OK |
| Papan Penganalisis | 2026-11-05 | 0 | OK |
| RS pasaran | 2026-11-04 | 1 | OK |
| Gred kumpulan | 2026-11-04 | 1 | OK |
| SEC fundamental | fail diubah | 0 | OK |
| Senarai bursa | fail diubah | 0 | OK |


Ambang LEWAT: > 3 hari. Dua sebab biasa **bukan** kerosakan: hujung minggu atau cuti pasaran, dan salinan kerja yang lama (lihat §0). Periksa kedua-duanya, kemudian `penjaga_jadual` dan log workflow, sebelum menganggap saluran rosak.


## 5. Workflow berjadual

| Workflow | Cron | Dijaga penjaga_jadual? |
|---|---|---|
| autotune_suku.yml | 17 3 1-7 1,4,7,10 6 | ya |
| beli.yml | 40 13 * * 1-5, 40 14 * * 1-5, 25 16 * * 1-5, 25 17 * * 1-5, 25 19 * * 1-5, 25 20 * * 1-5 | ya |
| edgar.yml | 17 23 * * 1-5, 47 3 * * 2-6 | ya |
| fundamental_sec.yml | 41 23 * * 1-5, 11 4 * * 2-6 | ya |
| gred_kumpulan.yml | 17 4 * * 2-6, 17 8 * * 2-6 | ya |
| harga_harian.yml | 37 21 * * 1-5, 23 0 * * 2-6 | ya |
| harian.yml | 7 5 * * 2-6, 7 7 * * 2-6, 7 9 * * 2-6, 7 11 * * 2-6 | ya |
| lejar.yml | 17 6 * * 2-6, 17 10 * * 2-6 | ya |
| pengawal.yml | 35 12 * * 1-5, 0 16 * * 1-5 | ya |
| penjaga_jadual.yml | 23 * * * *, 53 * * * * | **tidak** |
| petang.yml | 47 11 * * 1-5, 17 12 * * 1-5 | ya |
| rs_pasaran.yml | 41 22 * * 1-5, 17 3 * * 2-6 | ya |
| sandaran.yml | 19 2 * * 6 | ya |
| senarai_bursa.yml | 53 23 * * 1-5, 23 4 * * 2-6 | ya |
| skrin_tv.yml | 47 21 * * 1-5 | ya |


Workflow berjadual baharu **mesti** ditambah ke `JAGA` dalam `standard/penjaga_jadual.py`; lajur "tidak" di atas bermakna cetusan yang hilang tidak akan dipulihkan.


## 6. Status kajian

| Kajian | Status | Hasil |
|---|---|---|
| AUTOTUNE A02 (penalaan Optuna) | DITUTUP | 38400 konfigurasi diuji -> LULUS 0, CALON 0, TIDAK LULUS 40 |
| REVERSE fasa 1 (2020–2025) | DITUTUP — DITOLAK | DITERIMA 0, CALON 11, DITOLAK 110; sasaran +10%/bulan 0 daripada 36 sistem-tahun |
| REVERSE fasa 1b (saiz berskala risiko) | DITUTUP — DITOLAK | pulangan ditolak; MDD bertambah baik 6/6 tahun -> diuji hadapan sebagai lorong RISIKO_10 |
| REVERSE fasa 2 leg RS/gred | SPEC DIKUNCI — menunggu masa | RS/gred dikira harian, tiada sejarah; anggaran ~Okt 2027 |
| REVERSE fasa 2 leg SEC | SPEC DIKUNCI — menunggu liputan ticker | data titik-masa sejak 2009 (§4.1); menunggu isian awal 3,335 ticker, bukan masa |


## 7. Jangan ulangi — sudah diukur, ruang kosong

- **Penalaan parameter indikator.** AUTOTUNE A02: 38,400 konfigurasi dengan Optuna TPE, walk-forward, DSR dan PBO → LULUS 0, CALON 0. Setiap konfigurasi tambahan menaikkan ambang yang hasilnya mesti lepasi, bukan peluang menemui sesuatu.
- **Signal entry berasaskan indikator harga.** REVERSE fasa 1: 6 tahun, 4 rejim, 20,640 ujian ENTRY → tiada signal lulus gate keras dalam lebih daripada satu tahun; portfolio signal kalah kepada entri rawak pada 3 daripada 5 tahun yang diuji.
- **Signal EXIT berasaskan indikator.** FDR 0 pada setiap satu daripada enam tahun.
- Baca `REVERSE/KEPUTUSAN_FASA1.md` dan `REVERSE/DIAGNOSIS_FASA1.md` sebelum mencadangkan kajian indikator baharu.
