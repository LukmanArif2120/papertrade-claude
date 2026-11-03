# KOORDINATOR — keadaan repo dalam satu halaman

Dijana `BacktestShariah2/standard/koordinator.py` pada 2026-11-03 17:02 (waktu pelayan). Tiada rangkaian, tiada LLM, tiada penalaan — semuanya dibaca daripada fail keadaan repo. **Jangan ubah manual.**

## 0. Salinan kerja

| Cawangan | HEAD | Commit di belakang origin/main | origin/main (fetch terakhir) |
|---|---|---|---|
| main | 2026-11-03 | 0 | 2026-11-03 |


Selari dengan `origin/main` pada fetch terakhir — angka kesegaran di bawah boleh dipercayai.


## 1. Perlu keputusan anda (14)

| Dibuka | Perkara | Catatan |
|---|---|---|
| 2026-10-28 | Fasa 2: guna alphalens-reloaded (sudah dalam requirements-kajian.txt) atau tulis sendiri | alphalens memberi rank-IC + pulangan kuintil + turnover terus. REVERSE/ujian_pangkat.py ialah versi tangan. |
| 2026-10-28 | Uji perluasan universe dalam 3260 ticker Release A02 | Lever belum diuji (DIAGNOSIS_FASA1.md §3 item 1). Universe sekarang 2000 teratas ikut nilai dagangan; saham +100% cenderung lebih kecil. Had: A02 hanya simpan 3260 ticker. | 28 Okt: ini universe HARGA REVERSE (2000 teratas ikut nilai dagangan). Berasingan daripada universe SEC yang sudah dilebarkan ke 3260 (data/univ_sec.txt) pada 28 Okt. |
| 2026-10-28 | Jalankan step1_run.py untuk 2012-2019 (sejarah peristiwa sah leg SEC) | Cache signals_*.parquet hanya ada 2020-2025. Liputan SUE boleh diguna bermula 2012 (mandat XBRL berperingkat 2009-2011: 89 ticker 2009, 253 pada 2010, 482 pada 2011). 8 tahun tambahan = compute besar (~150MB parquet setiap tahun). Tanpa ini, leg SEC kekal 6 tahun sahaja dan kelebihan sejarah panjang tidak diperoleh. |
| 2026-10-29 | Uji signal PEAD yang bertahan atas universe lebih luas (saham kecil) | Satu lever yang dituju oleh keputusan itu sendiri: q5:pecutan_hasil & sejak_earnings_le5 bertahan SETIAP ujian statistik tetapi magnitudnya ~1.5% median bulanan. Kesusasteraan PEAD menyatakan kesan tertumpu pada saham kecil berspread lebar, dan universe REVERSE (2,000 teratas ikut nilai dagangan) dengan sengaja membuangnya. Data SEC kini meliputi 83% daripada 3,302 ticker. PERLU pradaftar baharu (tembakan §5 untuk universe top-2000 sudah terbelanja) DAN model kos jujur untuk nama tidak cair: slippage di sana melebihi 0.25% tier tertinggi sekarang. Jangkaan priori: kesan lebih kuat, kos lebih tinggi, net tidak pasti. |
| 2026-10-29 | Pembinaan yang menerima ekor kanan, tanpa pemicu — satu-satunya arah yang tinggal | Daripada KOLAM_EKOR.md §5. Soalan: bolehkah pembinaan (kolam lebih baik, slot lebih banyak, tiada henti keras, biarkan pemenang berjalan) mengalahkan penanda aras TANPA pemicu sama sekali? Ia mungkin kalah: membuang henti memperdalam persentil 5 daripada -15.58% ke -54.67% setiap saham-tahun, dan KEPEKATAN.md menunjukkan 8->60 slot membeli MDD 3.48 mata dengan pulangan -5.97 mata. PERLU pradaftar baharu. Penanda aras WAJIB SPUS (26.09%/tahun, MDD -10.14%), bukan SPY. Apa-apa jurang < 17.3 mata/tahun adalah hingar pemilihan (KEPEKATAN_BENIH.md) jadi ia MESTI diukur dengan jalur benih, bukan satu lorong. JANGAN jalankan sebagai penalaan parameter. |
| 2026-10-29 | Kecacatan mekanikal: 421 posisi C dihentikan pada hari masuk, kadar menang 0.00% | KOLAM_EKOR.md §4a. 421 daripada 1,770 posisi C ditutup (23.8%) dibeli dan dihentikan pada hari yang sama, purata -2.47%, kadar menang 0.00% merentas 421 dagangan — mekanikal, bukan hasil pasaran: paras henti kaedah terletak DALAM julat intrabar hari masuk (jarak henti median 1.93% lawan 5.33% bagi yang terselamat). Membetulkannya (jangan masuk bila henti < ~2% daripada harga masuk dirancang) mengurangkan jumlah kerugian direalisasi 19.5%. TETAPI purata baki 1,349 posisi ialah -3.18%, LEBIH BURUK daripada -3.01% keseluruhan: ia tidak menukar tanda. §4b: jangkaan negatif pada SETIAP lebar henti dan makin negatif bila dilebarkan (kadar menang naik 5.9x, kerugian purata naik 8.8x) = masuk tanpa kelebihan, mengesahkan fasa 1 pada data HADAPAN. Keputusan pengguna diperlukan: betulkan sebagai kebersihan sistem atau biarkan. |
| 2026-10-29 | Sambung spus_harian.csv ke lejar.yml supaya RINGKASAN.md melapor SPUS setiap malam | data/penanda_aras/spus_harian.csv kini disegarkan MANUAL (banding_spus.py --kemas-kini, guna yfinance). Ia TIDAK dipasang ke workflow malam dengan sengaja: yfinance tiada dalam sesi ini jadi laluan kemas kini belum diuji, dan kod belum diuji dalam kerja berjadual adalah liabiliti. portfolio_slot/RINGKASAN.md masih melapor SPY sahaja kerana hanya SPY+QQQ ada dalam harga_idx.csv. Pilihan: (a) tambah SPUS ke stor indeks (kod/stor.py, pengambil idx) supaya portfolio_slot.py boleh membacanya terus - paling bersih; (b) jalankan banding_spus.py dalam lejar.yml selepas portfolio_slot; (c) biar manual. Keputusan pengguna diperlukan kerana (a) dan (b) mengubah aliran data malam. |
| 2026-10-29 | Uji PEAD x konteks harga pada alam lebih luas ATAU slot lebih banyak | Daripada SILANG_GATE_C.md. Dapatan silang adalah NYATA (Gate A+B lulus, p=0.0010, bertahan FDR + dua bootstrap blok + 1000 permutasi) tetapi gagal portfolio kerana bentuk taburan: kelebihan hidup dalam ekor kanan nipis dan 8 posisi tidak cukup menangkapnya. Dua lever yang dituju oleh diagnosis itu sendiri: (a) lebih banyak slot - tetapi KEPEKATAN.md menunjukkan 8->60 slot mengorbankan pulangan 5.97 mata pada entri DIPILIH, walaupun PEMBINAAN.md menunjukkan ia MEMBANTU pada entri rawak, jadi arahnya tidak diketahui untuk entri signal; (b) alam lebih luas supaya n naik daripada 541-751 - bergabung dengan keputusan terbuka PEAD saham kecil, dan PERLU model kos saham tidak cair (slippage melebihi tier 0.25% tertinggi sekarang). PERLU pradaftar baharu; tembakan SPEC_SILANG sudah terbelanja. JANGAN jalankan sebagai penalaan parameter atau pelebaran grid 48. |
| 2026-11-02 | papertrade/moomoo pada 92.0% had dokumen db dan dibaca melalui sub(), bukan subBhg() | Didedahkan oleh amaran >= 85% yang ditambah kepada jana_db.py 2 Nov. kaedah_n/papan (88.8%) sudah ditukar kepada subBhg() dalam terbitan #172, tetapi papertrade/moomoo LEBIH HAMPIR (241,271 daripada 262,144) dan ia dibaca melalui pembalut lazy subRingkas(...)->sub(...), bukan sub() biasa, jadi penukaran itu bukan satu baris. Ia dokumen posisi Moomoo LAMA (beku sejak 13 Okt) jadi ia hanya tumbuh melalui medan penilaian harian - perlahan, tetapi apabila ia melepasi had ia menghentikan tolakan db MALAM, bukan sesi kerja. Urutan WAJIB: tukar pembaca halaman kepada subBhg() dan TERBITKAN dahulu, baru tambah ke jana_db.PECAH - sebaliknya halaman kehilangan baris secara senyap. |
| 2026-11-02 | semak_dashboard.js: 10 kegagalan "Untung center/right" dan hanya 22 jadual diaudit (dahulu 44) | Diukur 2 Nov dan DIATRIBUSIKAN: menjalankan pemeriksa pada badan versi hidup 1793607248-b31f SAHAJA (tanpa suntingan saya) memberi 10/22 yang sama, jadi ia datang daripada v143-v146 (rel kiri bersarang) yang diterbitkan oleh sesi lain, bukan daripada terbitan #172. Dua perkara berasingan: (1) jajaran tajuk lajur Untung lawan selnya - mungkin artifak indeks pemeriksa jika baris pertama ada colspan, perlu disemak sebelum menukar CSS; (2) liputan jatuh separuh kerana rel bersarang menukar panel mana yang dicapai pemeriksa. Yang (2) lebih penting: pemeriksa yang mengaudit separuh jadual memberi keyakinan palsu. |
| 2026-11-03 | Gred tiada bagi 1,448 posisi yang dibeli 2026-11-02 (613 M + 835 N) | BUKAN masalah Nxx: kedua-dua keluarga terjejas sama rata, kerana larian kejar melangkau langkah gred (kesan baru=tidak, dibetulkan f17c917) DAN kerana menggredkan isyarat 10-30 dengan berita hari ini ialah maklumat masa hadapan. cmd_gred tiada tapisan awalan, jadi posisi yang dibeli mulai 2026-11-03 akan bergred seperti biasa. Keputusan yang diperlukan: biarkan 1,448 baris itu tanpa gred (jujur, dan jurangnya kelihatan), atau isi semula dengan nilai hari ini dan terima bahawa medan gred tidak lagi titik-masa. Saya cadang biarkan. |
| 2026-11-03 | papertrade/claude pada 91.6% had dokumen db dan dibaca melalui sub(), bukan subBhg() | 240,261 daripada 262,144 bait. Sama kelas dengan papertrade/moomoo (92.6%) yang sudah dilog 2 Nov. Dengan Nxx menambah sehingga ~900 posisi sesi, ini akan dilanggar. Apabila ia berlaku, tolak db malam berhenti - data papertrade tetap dikomit (pembetulan 845dbbc), tetapi dashboard berhenti dikemas kini. Urutan WAJIB sama seperti moomoo: tukar pembaca halaman kepada subBhg() dan TERBITKAN dahulu, baru tambah ke jana_db.PECAH. |
| 2026-11-03 | lejar.tambah_bulan menambah tanpa menyahduplikasi: sesi separa ditulis akan menduakan baris | Ditemui semasa menilai sama ada if: always() boleh ditambah kepada langkah commit lejar.yml. Dalam gelung setiap sesi, CSV ditulis DAHULU dan status.json (sesi_terakhir) ditulis LEPAS, jadi kemalangan antara keduanya meninggalkan baris sesi S dalam tutup/langkau sementara status masih S-1 - dan larian berikutnya memproses S semula, menambah baris yang sama sekali lagi. Selagi ini benar, commit bersyarat-kejayaan ialah perlindungan, bukan kekurangan. Pembaikan sebenar: kunci nyahduplikasi (id_kaedah+saham+tarikh) dalam tambah_bulan, ATAU penanda 'sesi sedang diproses' yang dibersihkan pada larian berikutnya. Selepas itu barulah if: always() selamat dan lejar boleh menyimpan kemajuan separa. |
| 2026-11-03 | Kohort Nxx mengira indikator 94 kali setiap ticker: lejar 5.5 minit -> ~2 jam sesesi | DIUKUR, bukan dianggar. Larian lejar sebelum Nxx: 309-336 saat sesesi dengan 134 kaedah (status.json 'larian' bagi sesi 10-28, 10-29, 10-30). Larian 3 Nov dengan 228 kaedah: >2 jam dan masih berjalan - 21x lebih lama, bukan 1.7x yang nisbah bilangan kaedah cadangkan. Puncanya _nxx.indikator() TIADA cache: setiap satu daripada 94 modul Nxx memanggilnya semula bagi SETIAP ticker dalam sedia(). Diukur 29.1 ms/ticker, jadi 94 modul x 947 ticker = 43 minit CPU satu teras sesesi, berbanding 0.5 minit jika dikira sekali. Alam lejar lebih besar daripada 947 jadi angka sebenar lebih tinggi. Kesan: had masa lejar sudah dinaikkan 150->330 minit sebagai perlindungan, tetapi DUA sesi tertinggal kini mendekati had itu dan TIGA melepasinya - margin yang sama yang kita baru sahaja baiki telah dimakan semula oleh kohort baharu. Pembaikan: memo indikator per (ticker, bil_bar, tarikh akhir) dalam proses pekerja; satu pekerja memproses banyak kaedah berturut-turut, jadi cache peringkat modul dalam _nxx akan digunakan semula merentas 94 modul. Anggaran memori: ~25 lajur x ~300 baris x 8 bait x 3,000 ticker = ~180 MB setiap pekerja, 4 pekerja pada runner 7 GB - perlu diukur sebelum dilaksana, dan kemungkinan --proses perlu diturunkan serentak. JANGAN laksana tanpa mengesahkan keputusan imbasan tidak berubah: bandingkan senarai_beli dan isyarat sebelum/selepas pada sesi yang sama. |


Sunting `BacktestShariah2/koordinator/keputusan.csv` — tukar `status` ke `selesai` apabila diputuskan (tambah sahaja; jangan buang baris).


## 2. Kajian REVERSE — signal dan indikator (BUKAN kaedah Mxx)

REVERSE menguji **signal dan indikator** untuk ENTRY/HOLD/EXIT. Ia **tidak** menguji 134 kaedah Mxx repo dan tidak menala parameter. Populasi ujiannya ialah **peristiwa sah** (`REVERSE/SPEC.md` §7: tutup ≥ 5% di atas rendah terendah 20 hari DAN tutup > EMA21, kausal) atas universe A02 — bukan Lejar Penuh, bukan `portfolio_slot/`. Jangan campurkan kedua-dua jejak (`REVERSE/SPEC_FASA2.md` §9).


### Ambang fasa 2 (`SPEC_FASA2.md` §4: ≥ 250 hari dagangan liputan bertindih, ≥ 3,000 peristiwa sah, ≥ 2 suku penuh)

| Sumber | Hari dagangan | Mula | Akhir | Suku (anggaran) | Baris | Cukup? |
|---|---|---|---|---|---|---|
| RS pasaran | 30 | 2026-09-22 | 2026-11-02 | 0.5 |  | tidak |
| Gred kumpulan | 27 | 2026-09-25 | 2026-11-02 | 0.4 |  | tidak |
| SEC EPS/hasil | 4097 | 2009-04-15 | 2026-11-02 | 65.0 | 268765 | ya |
| SEC earnings 8-K | 5450 | 2004-08-23 | 2026-11-02 | 86.5 | 178831 | ya |


Leg **RS/gred**: terbaik **30 / 250** hari dagangan. Peristiwa sah ialah fungsi deterministik stor harga, jadi join peristiwa × data titik-masa boleh dibuat **retrospektif** — yang perlu ditunggu ialah masa, bukan kod.


Leg **SEC** tidak menunggu: nilai pertama difail = titik-masa retrospektif sejak 2009 (`SPEC_FASA2.md` §4.1). Halangannya **liputan ticker**: 2846 daripada 3302 ticker universe ada data EPS/hasil, 0 belum diisi. Universe REVERSE kira-kira 2,300 setahun.


## 3. Operasi repo — 134 kaedah Mxx dan papertrade C

Jejak berasingan daripada §2. Semua di bawah ini dipacu oleh isyarat kaedah **Mxx** melalui Lejar Penuh.


### Lorong portfolio_slot (bacaan adil ≥ 6 bulan, `kajian/KAJIAN_PORTFOLIO.md`)

| Lorong | Ekuiti | Dipegang | Keluar | Sesi terakhir |
|---|---|---|---|---|
| RS_10 | 0.802281 | 10 | 2 | 2026-11-02 |
| RAWAK_10 | 0.971055 | 10 | 2 | 2026-11-02 |
| GABUNGAN_10 | 1.000874 | 7 | 18 | 2026-11-02 |
| TOP1_10 | 0.982475 | 6 | 20 | 2026-11-02 |
| RAWAK_KAEDAH_10 | 0.986192 | 10 | 1 | 2026-11-02 |
| RISIKO_10 | 0.94169 | 10 | 2 | 2026-11-02 |


`RISIKO_10` (sejak 28 Okt 2026) dipasangkan dengan `RS_10`: susunan calon sama, hanya saiz berbeza. **MDD-nya mesti dibaca bersama lajur `tunai`** — pendedahannya lebih rendah, jadi sebahagian kelebihan MDD datang daripada pendedahan, bukan saiz. Ia menguji saiz atas **isyarat Mxx** dan bukan ujian ke hadapan dapatan REVERSE fasa 1b (`REVERSE/SPEC_FASA2.md` §9.2).


### Papan Penganalisis — 228 kaedah Mxx

| Status pantau | Bilangan |
|---|---|
| BELUM CUKUP | 222 |
| OK | 6 |


## 4. Kesegaran data

| Sumber | Terakhir | Umur (hari) | Status |
|---|---|---|---|
| Stor harga | 20261102 | 1 | OK |
| Trend D10H2-r2 | 20261102 | 1 | OK |
| Lejar Penuh | 2026-11-02 | 1 | OK |
| portfolio_slot | 2026-11-02 | 1 | OK |
| Papan Penganalisis | 2026-11-03 | 0 | OK |
| RS pasaran | 2026-11-02 | 1 | OK |
| Gred kumpulan | 2026-11-02 | 1 | OK |
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
| pengawal.yml | 35 12 * * 1-5 | ya |
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
