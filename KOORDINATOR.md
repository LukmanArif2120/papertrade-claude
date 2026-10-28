# KOORDINATOR — keadaan repo dalam satu halaman

Dijana `BacktestShariah2/standard/koordinator.py` pada 2026-10-28 12:58 (waktu pelayan). Tiada rangkaian, tiada LLM, tiada penalaan — semuanya dibaca daripada fail keadaan repo. **Jangan ubah manual.**

## 0. Salinan kerja

| Cawangan | HEAD | Commit di belakang origin/main | origin/main (fetch terakhir) |
|---|---|---|---|
| claude/wizardly-mendel-qr6j64 | 2026-10-28 | 0 | 2026-10-28 |


Selari dengan `origin/main` pada fetch terakhir — angka kesegaran di bawah boleh dipercayai.


## 1. Perlu keputusan anda (4)

| Dibuka | Perkara | Catatan |
|---|---|---|
| 2026-10-28 | Wayar standard/koordinator.py ke satu workflow supaya KOORDINATOR.md segar sendiri | Cadangan: langkah tambahan dalam semak_data.yml (setiap push) atau harian.yml (sekali sehari). Sekarang dijalankan manual. |
| 2026-10-28 | Fasa 2: guna alphalens-reloaded (sudah dalam requirements-kajian.txt) atau tulis sendiri | alphalens memberi rank-IC + pulangan kuintil + turnover terus. REVERSE/ujian_pangkat.py ialah versi tangan. |
| 2026-10-28 | Uji perluasan universe dalam 3260 ticker Release A02 | Lever belum diuji (DIAGNOSIS_FASA1.md §3 item 1). Universe sekarang 2000 teratas ikut nilai dagangan; saham +100% cenderung lebih kecil. Had: A02 hanya simpan 3260 ticker. |
| 2026-10-28 | Nilai semula sasaran pulangan | +10%/bulan = 78% daripada siling pandangan sempurna (12.89%/bulan). 0 daripada 36 sistem-tahun mencapainya. Siling dikira REVERSE/siling_pandangan_sempurna.py. |


Sunting `BacktestShariah2/koordinator/keputusan.csv` — tukar `status` ke `selesai` apabila diputuskan (tambah sahaja; jangan buang baris).


## 2. Menunggu masa — ambang yang belum dicapai


### Fasa 2 REVERSE (ambang `SPEC_FASA2.md` §4: ≥ 250 hari dagangan bertindih, ≥ 3,000 peristiwa sah, ≥ 2 suku penuh)

| Sumber | Hari dagangan | Mula | Akhir | Suku (anggaran) | Baris | Cukup? |
|---|---|---|---|---|---|---|
| RS pasaran | 30 | 2026-09-16 | 2026-10-27 | 0.5 |  | tidak |
| Gred kumpulan | 23 | 2026-09-25 | 2026-10-27 | 0.4 |  | tidak |
| SEC EPS/hasil |  |  |  |  | 80575 | tidak |
| SEC earnings 8-K |  |  |  |  | 54109 | tidak |


Terbaik setakat ini: **30 / 250** hari dagangan. Kiraan peristiwa sah memerlukan join dengan Lejar Penuh — itu langkah pertama fasa 2, bukan kerja koordinator.


### Lorong portfolio_slot (bacaan adil ≥ 6 bulan, `kajian/KAJIAN_PORTFOLIO.md`)

| Lorong | Ekuiti | Dipegang | Keluar | Sesi terakhir |
|---|---|---|---|---|
| RS_10 | 0.978538 | 10 | 0 | 2026-10-27 |
| RAWAK_10 | 1.003345 | 10 | 0 | 2026-10-27 |
| GABUNGAN_10 | 0.999547 | 6 | 11 | 2026-10-27 |
| TOP1_10 | 0.995651 | 8 | 11 | 2026-10-27 |
| RAWAK_KAEDAH_10 | 0.994292 | 10 | 0 | 2026-10-27 |


`RISIKO_10` (sejak 28 Okt 2026) dipasangkan dengan `RS_10`: susunan calon sama, hanya saiz berbeza. **MDD-nya mesti dibaca bersama lajur `tunai`** — pendedahannya lebih rendah, jadi sebahagian kelebihan MDD datang daripada pendedahan, bukan saiz.


### Papan Penganalisis — 134 kaedah

| Status pantau | Bilangan |
|---|---|
| BELUM CUKUP | 134 |


Semua kaedah masih **BELUM CUKUP** (< 10 hari beli berbeza). Tiada kaedah boleh dinilai ke hadapan lagi; penilaian penuh dijangka 15 Jan 2027 (`WFO/README.md`).


## 3. Kesegaran data

| Sumber | Terakhir | Umur (hari) | Status |
|---|---|---|---|
| Stor harga | 20261027 | 1 | OK |
| Trend D10H2-r2 | 20261027 | 1 | OK |
| Lejar Penuh | 2026-10-27 | 1 | OK |
| portfolio_slot | 2026-10-27 | 1 | OK |
| Papan Penganalisis | 2026-10-28 | 0 | OK |
| RS pasaran | 2026-10-27 | 1 | OK |
| Gred kumpulan | 2026-10-27 | 1 | OK |
| SEC fundamental | fail diubah | 0 | OK |
| Senarai bursa | fail diubah | 0 | OK |


Ambang LEWAT: > 3 hari. Dua sebab biasa **bukan** kerosakan: hujung minggu atau cuti pasaran, dan salinan kerja yang lama (lihat §0). Periksa kedua-duanya, kemudian `penjaga_jadual` dan log workflow, sebelum menganggap saluran rosak.


## 4. Workflow berjadual

| Workflow | Cron | Dijaga penjaga_jadual? |
|---|---|---|
| autotune_suku.yml | 17 3 1-7 1,4,7,10 6 | **tidak** |
| beli.yml | 40 13 * * 1-5, 40 14 * * 1-5, 25 16 * * 1-5, 25 19 * * 1-5 | ya |
| edgar.yml | 17 23 * * 1-5, 47 3 * * 2-6 | ya |
| fundamental_sec.yml | 41 23 * * 1-5, 11 4 * * 2-6 | ya |
| gred_kumpulan.yml | 17 4 * * 2-6, 17 8 * * 2-6 | ya |
| harga_harian.yml | 37 21 * * 1-5, 23 0 * * 2-6 | ya |
| harian.yml | 7 5 * * 2-6, 7 7 * * 2-6, 7 9 * * 2-6, 7 11 * * 2-6 | ya |
| lejar.yml | 17 6 * * 2-6, 17 10 * * 2-6 | ya |
| penjaga_jadual.yml | 23 * * * *, 53 * * * * | **tidak** |
| petang.yml | 47 11 * * 1-5, 17 12 * * 1-5 | ya |
| rs_pasaran.yml | 41 22 * * 1-5, 17 3 * * 2-6 | ya |
| senarai_bursa.yml | 53 23 * * 1-5, 23 4 * * 2-6 | ya |
| skrin_tv.yml | 47 21 * * 1-5 | ya |


Workflow berjadual baharu **mesti** ditambah ke `JAGA` dalam `standard/penjaga_jadual.py`; lajur "tidak" di atas bermakna cetusan yang hilang tidak akan dipulihkan.


## 5. Status kajian

| Kajian | Status | Hasil |
|---|---|---|
| AUTOTUNE A02 (penalaan Optuna) | DITUTUP | 38400 konfigurasi diuji -> LULUS 0, CALON 0, TIDAK LULUS 40 |
| REVERSE fasa 1 (2020–2025) | DITUTUP — DITOLAK | DITERIMA 0, CALON 11, DITOLAK 110; sasaran +10%/bulan 0 daripada 36 sistem-tahun |
| REVERSE fasa 1b (saiz berskala risiko) | DITUTUP — DITOLAK | pulangan ditolak; MDD bertambah baik 6/6 tahun -> diuji hadapan sebagai lorong RISIKO_10 |
| REVERSE fasa 2 (data titik-masa) | SPEC DIKUNCI — menunggu data | lihat jadual ambang di atas |


## 6. Jangan ulangi — sudah diukur, ruang kosong

- **Penalaan parameter indikator.** AUTOTUNE A02: 38,400 konfigurasi dengan Optuna TPE, walk-forward, DSR dan PBO → LULUS 0, CALON 0. Setiap konfigurasi tambahan menaikkan ambang yang hasilnya mesti lepasi, bukan peluang menemui sesuatu.
- **Signal entry berasaskan indikator harga.** REVERSE fasa 1: 6 tahun, 4 rejim, 20,640 ujian ENTRY → tiada signal lulus gate keras dalam lebih daripada satu tahun; portfolio signal kalah kepada entri rawak pada 3 daripada 5 tahun yang diuji.
- **Signal EXIT berasaskan indikator.** FDR 0 pada setiap satu daripada enam tahun.
- Baca `REVERSE/KEPUTUSAN_FASA1.md` dan `REVERSE/DIAGNOSIS_FASA1.md` sebelum mencadangkan kajian indikator baharu.
