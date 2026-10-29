# KOORDINATOR — keadaan repo dalam satu halaman

Dijana `BacktestShariah2/standard/koordinator.py` pada 2026-10-29 01:48 (waktu pelayan). Tiada rangkaian, tiada LLM, tiada penalaan — semuanya dibaca daripada fail keadaan repo. **Jangan ubah manual.**

## 0. Salinan kerja

| Cawangan | HEAD | Commit di belakang origin/main | origin/main (fetch terakhir) |
|---|---|---|---|
| claude/wizardly-mendel-qr6j64 | 2026-10-29 | 0 | 2026-10-29 |


Selari dengan `origin/main` pada fetch terakhir — angka kesegaran di bawah boleh dipercayai.


## 1. Perlu keputusan anda (5)

| Dibuka | Perkara | Catatan |
|---|---|---|
| 2026-10-28 | Fasa 2: guna alphalens-reloaded (sudah dalam requirements-kajian.txt) atau tulis sendiri | alphalens memberi rank-IC + pulangan kuintil + turnover terus. REVERSE/ujian_pangkat.py ialah versi tangan. |
| 2026-10-28 | Uji perluasan universe dalam 3260 ticker Release A02 | Lever belum diuji (DIAGNOSIS_FASA1.md §3 item 1). Universe sekarang 2000 teratas ikut nilai dagangan; saham +100% cenderung lebih kecil. Had: A02 hanya simpan 3260 ticker. | 28 Okt: ini universe HARGA REVERSE (2000 teratas ikut nilai dagangan). Berasingan daripada universe SEC yang sudah dilebarkan ke 3260 (data/univ_sec.txt) pada 28 Okt. |
| 2026-10-28 | Nilai semula sasaran pulangan | REVERSE/SASARAN.md (29 Okt 2026) memberi aritmetiknya: +10%/bulan = 3.14x/tahun = 8,994,377x atas 14 tahun (USD 10k -> USD 89.9 bilion). SPY beli-dan-pegang 2012-2025: median 17.62%/tahun, MDD -9.44%, bulanan 1.82%, dan 0% bulan capai +10% dalam 13 daripada 14 tahun. Sasaran = 5.5x median bulanan indeks. Konfigurasi terbaik kajian 17.65%/tahun tetapi MDD -14.55% = TIDAK mengalahkan SPY pada kedua-dua paksi. Keputusan ini bukan teknikal: ia bergantung pada berapa modal boleh hilang. |
| 2026-10-28 | Jalankan step1_run.py untuk 2012-2019 (sejarah peristiwa sah leg SEC) | Cache signals_*.parquet hanya ada 2020-2025. Liputan SUE boleh diguna bermula 2012 (mandat XBRL berperingkat 2009-2011: 89 ticker 2009, 253 pada 2010, 482 pada 2011). 8 tahun tambahan = compute besar (~150MB parquet setiap tahun). Tanpa ini, leg SEC kekal 6 tahun sahaja dan kelebihan sejarah panjang tidak diperoleh. |
| 2026-10-29 | Uji signal PEAD yang bertahan atas universe lebih luas (saham kecil) | Satu lever yang dituju oleh keputusan itu sendiri: q5:pecutan_hasil & sejak_earnings_le5 bertahan SETIAP ujian statistik tetapi magnitudnya ~1.5% median bulanan. Kesusasteraan PEAD menyatakan kesan tertumpu pada saham kecil berspread lebar, dan universe REVERSE (2,000 teratas ikut nilai dagangan) dengan sengaja membuangnya. Data SEC kini meliputi 83% daripada 3,302 ticker. PERLU pradaftar baharu (tembakan §5 untuk universe top-2000 sudah terbelanja) DAN model kos jujur untuk nama tidak cair: slippage di sana melebihi 0.25% tier tertinggi sekarang. Jangkaan priori: kesan lebih kuat, kos lebih tinggi, net tidak pasti. |


Sunting `BacktestShariah2/koordinator/keputusan.csv` — tukar `status` ke `selesai` apabila diputuskan (tambah sahaja; jangan buang baris).


## 2. Kajian REVERSE — signal dan indikator (BUKAN kaedah Mxx)

REVERSE menguji **signal dan indikator** untuk ENTRY/HOLD/EXIT. Ia **tidak** menguji 134 kaedah Mxx repo dan tidak menala parameter. Populasi ujiannya ialah **peristiwa sah** (`REVERSE/SPEC.md` §7: tutup ≥ 5% di atas rendah terendah 20 hari DAN tutup > EMA21, kausal) atas universe A02 — bukan Lejar Penuh, bukan `portfolio_slot/`. Jangan campurkan kedua-dua jejak (`REVERSE/SPEC_FASA2.md` §9).


### Ambang fasa 2 (`SPEC_FASA2.md` §4: ≥ 250 hari dagangan liputan bertindih, ≥ 3,000 peristiwa sah, ≥ 2 suku penuh)

| Sumber | Hari dagangan | Mula | Akhir | Suku (anggaran) | Baris | Cukup? |
|---|---|---|---|---|---|---|
| RS pasaran | 30 | 2026-09-17 | 2026-10-28 | 0.5 |  | tidak |
| Gred kumpulan | 23 | 2026-09-25 | 2026-10-27 | 0.4 |  | tidak |
| SEC EPS/hasil | 4094 | 2009-04-15 | 2026-10-28 | 65.0 | 267951 | ya |
| SEC earnings 8-K | 5447 | 2004-08-23 | 2026-10-28 | 86.5 | 178433 | ya |


Leg **RS/gred**: terbaik **30 / 250** hari dagangan. Peristiwa sah ialah fungsi deterministik stor harga, jadi join peristiwa × data titik-masa boleh dibuat **retrospektif** — yang perlu ditunggu ialah masa, bukan kod.


Leg **SEC** tidak menunggu: nilai pertama difail = titik-masa retrospektif sejak 2009 (`SPEC_FASA2.md` §4.1). Halangannya **liputan ticker**: 2846 daripada 3302 ticker universe ada data EPS/hasil, 0 belum diisi. Universe REVERSE kira-kira 2,300 setahun.


## 3. Operasi repo — 134 kaedah Mxx dan papertrade C

Jejak berasingan daripada §2. Semua di bawah ini dipacu oleh isyarat kaedah **Mxx** melalui Lejar Penuh.


### Lorong portfolio_slot (bacaan adil ≥ 6 bulan, `kajian/KAJIAN_PORTFOLIO.md`)

| Lorong | Ekuiti | Dipegang | Keluar | Sesi terakhir |
|---|---|---|---|---|
| RS_10 | 0.978538 | 10 | 0 | 2026-10-27 |
| RAWAK_10 | 1.003345 | 10 | 0 | 2026-10-27 |
| GABUNGAN_10 | 0.999547 | 6 | 11 | 2026-10-27 |
| TOP1_10 | 0.995651 | 8 | 11 | 2026-10-27 |
| RAWAK_KAEDAH_10 | 0.994292 | 10 | 0 | 2026-10-27 |
| RISIKO_10 | 0.996214 | 10 | 0 | 2026-10-27 |


`RISIKO_10` (sejak 28 Okt 2026) dipasangkan dengan `RS_10`: susunan calon sama, hanya saiz berbeza. **MDD-nya mesti dibaca bersama lajur `tunai`** — pendedahannya lebih rendah, jadi sebahagian kelebihan MDD datang daripada pendedahan, bukan saiz. Ia menguji saiz atas **isyarat Mxx** dan bukan ujian ke hadapan dapatan REVERSE fasa 1b (`REVERSE/SPEC_FASA2.md` §9.2).


### Papan Penganalisis — 134 kaedah Mxx

| Status pantau | Bilangan |
|---|---|
| BELUM CUKUP | 134 |


Semua kaedah masih **BELUM CUKUP** (< 10 hari beli berbeza). Tiada kaedah boleh dinilai ke hadapan lagi; penilaian penuh dijangka 15 Jan 2027 (`WFO/README.md`).


## 4. Kesegaran data

| Sumber | Terakhir | Umur (hari) | Status |
|---|---|---|---|
| Stor harga | 20261027 | 2 | OK |
| Trend D10H2-r2 | 20261027 | 2 | OK |
| Lejar Penuh | 2026-10-27 | 2 | OK |
| portfolio_slot | 2026-10-27 | 2 | OK |
| Papan Penganalisis | 2026-10-29 | 0 | OK |
| RS pasaran | 2026-10-28 | 1 | OK |
| Gred kumpulan | 2026-10-27 | 2 | OK |
| SEC fundamental | fail diubah | 0 | OK |
| Senarai bursa | fail diubah | 1 | OK |


Ambang LEWAT: > 3 hari. Dua sebab biasa **bukan** kerosakan: hujung minggu atau cuti pasaran, dan salinan kerja yang lama (lihat §0). Periksa kedua-duanya, kemudian `penjaga_jadual` dan log workflow, sebelum menganggap saluran rosak.


## 5. Workflow berjadual

| Workflow | Cron | Dijaga penjaga_jadual? |
|---|---|---|
| autotune_suku.yml | 17 3 1-7 1,4,7,10 6 | ya |
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
