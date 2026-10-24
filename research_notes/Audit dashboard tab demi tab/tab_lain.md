# Audit tab sekunder dashboard: Watchlist, Backtest, Kaedah, Sektor (24 Okt 2026)

Skop: ketepatan data, kesegaran dan kegunaan bagi tab Watchlist, Backtest, Kaedah dan Sektor dalam `BacktestShariah2/standard/dashboard_v2.html` (v103, masih 8 tab; reka semula 4 tab dalam laporan audit awal belum dilaksanakan). Sesi AS terkini: Jumaat 2026-10-23. Audit baca sahaja: dokumen db diambil melalui ArtifactData ke scratchpad, repo tidak diubah.

Bukti semakan semula (skrip scratchpad, boleh dijalankan semula):
- `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/audit_lain/skrip/semak_watch.py` (kira semula `hampir()` atas stor harga repo ditambah bar 2026-10-23 daripada `data/harga/terkini.csv`)
- `.../skrip/semak_lengkap.py` (kira semula `sig` bagi baris "isyarat lengkap")
- `.../skrip/semak_kat.py`, `semak_kat2.py` (katalog lawan modul `kod/kaedah/M*.py` dan registry)
- `.../skrip/semak_bt.py` (replika corong 7 langkah `kpM()` dalam Python, kemudian banding dengan `analisis/papan`)
- Salinan db: `.../audit_lain/db/` (papertrade/watchlist v29 + watchlist_2 v20, sektor/snapshot v16, kaedah/katalog v4, meta/info v1, registry 173 dokumen, autotune 194 dokumen, analisis/papan v9, harian/status v41)

## Soalan 1: Nilai mana yang salah atau lapuk? (contoh tepat dan punca)

### Takeaway
Nombor teras dalam keempat-empat tab sepadan dengan sumber. Watchlist: 32/32 baris yang dikira semula sepadan, dan semua 19 isyarat lengkap yang boleh disemak disahkan. Registry: 1,589/1,589 baris sama dengan CSV. Prestasi sektor: 7/7 baris sepadan. Gred S/I watchlist: 358/358 sepadan. Masalah sebenar ada di tempat lain: (a) medan SST dalam tab Sektor dibeku sejak ≤ 14 Okt tetapi masih dipapar sebagai "hari ini"; (b) lajur/togol 1H Sektor sentiasa kosong; (c) gred S/I/R watchlist ketinggalan satu sesi (data 22 Okt) walaupun dilabel 23 Okt; (d) label dan KPI kecil dalam Watchlist; (e) Backtest, katalog Kaedah dan AUTOTUNE ialah data beku (17–18 Okt) yang dilabel "Langsung".

### Cited Findings

**Watchlist: semakan nilai (betul)**
- db `papertrade/watchlist` + `_2` mengandungi 179 baris dengan `tarikh_data` 2026-10-23, `dibina` "2026-10-24 06:30 MYT". Set (saham, kaedah) sama dengan `papertrade/watchlist.csv`: 0 baris hanya dalam db, 0 baris hanya dalam CSV. — [papertrade/watchlist.csv](BacktestShariah2/papertrade/watchlist.csv); [db papertrade/watchlist](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)
- Saya mengira semula `hampir()` bagi 32 baris (satu bagi setiap kaedah, rawak). Harga, pencetus, paras, jarak, % hampir dan syarat_dipenuhi sama tepat bagi 30 baris. Dua baris berbeza sedikit pada paras: M106 LZB 30.3307 lawan 30.3257 (0.02%) dan M111 TOL 142.2132 lawan 142.1575 (0.04%). % hampir kedua-duanya sama (98.8, dan 98.3 lawan 98.4). Puncanya mungkin bar 23 Okt Moomoo (rutin) lawan yfinance (semakan saya). Contoh yang tepat: KT M01 paras 17.1625 jarak 0.91; LNTH M33 100.9931/1.2; XOM M06 183.75/0.29; FAST M23 52.91/1.94; APD M37 312.822/1.85. — [kod/scanner.py:322](BacktestShariah2/kod/scanner.py); skrip `semak_watch.py`
- 92/179 baris (51%) ialah "isyarat lengkap" (`syarat_belum` = "Tiada (isyarat sah)", `sebab` "Isyarat lengkap pada tutup 23 Okt"). Saya mengira semula `sig` bagi sampel 20 baris: 19 benar pada 2026-10-23 dan palsu pada 2026-10-22 (contoh LAUR M20, ADP M78, MSFT M67, PBR M68, TENB M12, TWLO M59). Baris ke-20 (STNG M55) tidak dapat disemak kerana tiada bar 23 Okt dalam `terkini.csv` repo. — [jadual/kemas_kini_0602.md:26](BacktestShariah2/jadual/kemas_kini_0602.md); skrip `semak_lengkap.py`
- Gred S/I dalam watchlist sepadan 358/358 dengan `data/kumpulan/gred_kumpulan.csv`. Fail itu bertarikh **2026-10-22** (dibina 2026-10-23 17:49 MYT). RS rating sepadan 171/179 dengan `data/rs/rs_pasaran.csv` sesi **2026-10-22**, dan 0/179 dengan sesi 23 Okt (fail 23 Okt hanya ada 5 ticker; `status.json` `saham_ditulis` 5). — [gred_kumpulan.csv](BacktestShariah2/data/kumpulan/gred_kumpulan.csv); [data/rs/status.json](BacktestShariah2/data/rs/status.json)

**Watchlist: lapuk atau label salah**
- Semua 179 baris membawa `gred_pada` "2026-10-23". Tetapi gred S/I/R dikira daripada data 22 Okt: `snapshot_kumpulan()` memakai snapshot terkini bagi baris tanpa tarikh, dan rutin 6:02 "membawa gred hari sebelumnya". Jadi harga dan % hampir adalah untuk 23 Okt, manakala gred tertinggal satu sesi. Label `gred_pada` ialah tarikh larian, bukan tarikh data. — [standard/gred.py:205-213](BacktestShariah2/standard/gred.py); [standard/harian_c.py:612-613](BacktestShariah2/standard/harian_c.py)
- 101 baris ada `pct_dipenuhi` = 100: 92 isyarat lengkap ditambah 9 baris "paras disentuh" (ETD M02, IOVA M08, ASST/CAH/COR M102, WWW M34, CVX/DHR M35, PSX M67). Ini bercanggah dengan takrif dalam dokumen sendiri ("maks 99.9") dan dengan `pct_hampir()` dalam harian_c (had 99.9). Halaman menutup masalah ini dengan `wPill` ("Paras disentuh", `min(99.9, …)`). Namun KPI "≥ 99% hampir" (`n99`) masih mengira 9 baris sentuh itu bersama calon sebenar ≥ 99%. Bagi M102, jarak 0 ialah andaian kod ("jika R hari ini <= 0 … jarak_pct = 0"), bukan paras yang benar-benar disentuh. — [dashboard_v2.html:1293-1294,1331](BacktestShariah2/standard/dashboard_v2.html); [harian_c.py:544-545](BacktestShariah2/standard/harian_c.py); [kod/kaedah/M102.py:74-75](BacktestShariah2/kod/kaedah/M102.py)
- 3 baris LNTH (M105, M30, M33) sudah 12 hari dalam watchlist (masuk 2026-10-07). `scanner.py` menetapkan `TAMAT_WATCH = 10`, tetapi tugasan_v3 §3 tidak menyebut had umur. Peraturan ini tidak jelas. — [kod/scanner.py:19](BacktestShariah2/kod/scanner.py); [tugasan_v3.md:34](BacktestShariah2/standard/tugasan_v3.md)

**Sektor: semakan nilai (betul)**
- Prestasi kumpulan dalam `sektor/snapshot` (dibina 2026-10-24 06:35 MYT, `tarikh_harga` 20261023) sepadan tepat dengan `papertrade/sektor_pasaran.csv` 2026-10-23 bagi 7 baris yang disemak. Contohnya Utilities 1W +1.32 / 1M +7.07 / 3M −4.97 / breadth 78.9 / Improving / skor 80; Energy 1M +3.98; Basic Materials 1M −8.44; Technology 1M −1.52; Oil & Gas Integrated 1M +12.79; Insurance Brokers +12.43; Consulting Services +12.45. — [papertrade/sektor_pasaran.csv](BacktestShariah2/papertrade/sektor_pasaran.csv)

**Sektor: lapuk atau kosong**
- Medan SST setiap kumpulan (RS, volum relatif, aliran institusi) disalin daripada snapshot lama setiap hari (`SST_MEDAN`). Nilainya sama dalam `sektor.csv` bagi 14, 15, 16, 19 dan 20 Okt: Utilities RS 52.66 / VR 0.83 / aliran −1; Technology 61.15 / 0.86 / +5; Energy 67.13 / 0.84 / −2. `sektor.csv` tidak bertambah selepas 20 Okt kerana SST tidak tersedia. Log menyebut "aliran institusi SST tidak berubah" dan "Medan SST per kumpulan tidak dikira semula". — [snapshot_sektor_db.py:13,69](BacktestShariah2/standard/snapshot_sektor_db.py); [binaan_v2_log_tambahan.md:113,133,194,212,278,307](BacktestShariah2/standard/binaan_v2_log_tambahan.md)
- RS, VR dan aliran kosong bagi 4/11 sektor (Basic Materials, Consumer Cyclical, Consumer Defensive, Industrials) dan 121–122/138 industri. — db `sektor/snapshot` v16
- Senarai "Volum luar biasa **hari ini**" (9 saham, contoh RAMP 6.52×) dan A/D pasaran 403/342 datang daripada larian yang dilog "volum luar biasa (9) dikemas kini; A/D 403/342". Log seterusnya menyebut SST tidak tersedia, jadi data ini berumur ≥ 3–4 sesi tetapi tajuknya masih "hari ini". — [dashboard_v2.html:1257](BacktestShariah2/standard/dashboard_v2.html); [binaan_v2_log_tambahan.md:194](BacktestShariah2/standard/binaan_v2_log_tambahan.md)
- `prestasi_1d` = null bagi 149/149 baris kerana kod menetapkannya None secara terus. Akibatnya lajur "1H" dan togol peta haba "1H" sentiasa "–". — [snapshot_sektor_db.py:66](BacktestShariah2/standard/snapshot_sektor_db.py); [dashboard_v2.html:1161](BacktestShariah2/standard/dashboard_v2.html)
- Senarai "teratas" dalam 10 industri terkuat memaparkan kelas berganda bersama: BF.A dan BF.B, PBR dan PBR.A. Ini tidak selaras dengan polisi kelas berganda (paparan sahaja). — db `sektor/snapshot`; [CLAUDE.md](CLAUDE.md) (kelas berganda 22 Okt)

**Backtest: semakan nilai (betul)**
- 173 dokumen `registry` (141 M + 32 I) membawa 1,589 baris M. Baris ini sama dengan `data/registry_M_gabung.csv` (1,589 baris) tanpa sebarang beza pada cagr, mdd, skor, n, win, avg, days, h1, h2, keputusan dan gate_gagal. Semua baris `kod/registry/M*.csv` juga ada dalam fail gabung. — [data/registry_M_gabung.csv](BacktestShariah2/data/registry_M_gabung.csv); skrip semakan dalam nota ini
- `meta/info`: EW 431 21.91%, SPY 15.86%, EW MDD −40.29%. Nilai ini sama dengan `analisis/papan.rujukan` (`is_ew` 0.2191, `is_spy` 0.1586). — db `meta/info`, `analisis/papan`

**Backtest: lapuk atau label mengelirukan**
- Pengepala memaparkan "Langsung · ujian terkini 2026-10-17", iaitu tarikh registry terbaharu (tarikh: 05 Okt 428, 06 Okt 453, 07 Okt 315, 10 Okt 26, 16 Okt 235, 17 Okt 132 baris). Backtest ini beku, bukan data langsung. — [dashboard_v2.html:3783](BacktestShariah2/standard/dashboard_v2.html)
- Dokumen AUTOTUNE dibina 2026-10-18 (A01 05:10Z, A02 11:40Z, A03 13:57Z). Data ini beku dan status tala sudah siap 100%. Fail repo `AUTOTUNE/hasil*` tidak berubah sejak itu (hanya dialihkan dalam commit 577883c). — db `autotune/status`, `a02_status`, `a03_status`

**Kaedah: kesegaran**
- `kaedah/katalog` dibina 2026-10-17 dan sama dengan `standard/katalog_kaedah.json` (0 beza pada varian_kod, masuk, keluar, pegang, henti). Tiada skrip yang menolaknya ke db secara automatik. Kod berubah selepas itu: tidak_layak (21 Okt), dagangan.py replika bagi 13 kaedah (22 Okt), M31 `HENTI_TUTUP` (23 Okt, commit 6432264). Perubahan ini tidak mengubah peraturan masuk/keluar. — [standard/katalog_kaedah.json](BacktestShariah2/standard/katalog_kaedah.json); `git log --since=2026-10-17 -- BacktestShariah2/kod/kaedah`

### Inferences
- Tiada nilai harga atau isyarat yang salah dalam Watchlist. Yang lemah ialah label (gred "23 Okt" sebenarnya data 22 Okt) dan KPI ≥ 99% yang bercampur dengan kes "paras disentuh".
- Tab Sektor paling banyak memaparkan data lapuk sebagai data semasa. Tiga lajur jadual dan seluruh panel "Aliran institusi & volum" bergantung pada SST yang tidak dikemas kini sejak ~14–20 Okt.
- Backtest, Kaedah dan AUTOTUNE ialah data beku. Mereka tidak perlu dimuat atau dilabel sebagai "langsung".

### Gaps
- Tidak dapat menyemak STNG M55 (tiada bar 23 Okt dalam `data/harga/terkini.csv`) dan 66 ticker stor lain tanpa bar 23 Okt.
- Tidak menjalankan `git fetch`, jadi larian `gred_kumpulan.yml` / `rs_pasaran.yml` bagi data 23 Okt yang mungkin sudah di origin tidak disemak.
- Jumlah pasaran (3,829 saham, ≥ USD5) daripada skrin Moomoo tidak boleh dikira semula daripada stor repo (~947 ticker).

## Soalan 2: Adakah katalog Kaedah menerangkan varian yang benar-benar didagang (masuk/keluar/henti/pegang) dengan betul?

### Takeaway
Ya, bagi 134/134 kaedah aktif dari segi varian, had masa dan ada atau tiada henti. Hanya ada satu salah paparan (M31 dilabel "⚠ Tiada henti" walaupun kod ada henti tutup) dan satu percanggahan ayat (4 kaedah K145+ menyebut "pegang sehingga isyarat keluar" sedangkan mereka tiada isyarat keluar). Jalur "Sama untuk semua" tidak menyebut peraturan 19–22 Okt: penapis tidak layak, kelas berganda dan belian semula.

### Cited Findings
- Semakan program atas 134 modul `kod/kaedah/M*.py`:
  - `varian_kod` katalog = `VARIAN` kod: 134/134.
  - TMAX dalam teks "pegang": 134/134. Kaedah dengan TMAX menyebut nombornya; kaedah tanpa TMAX tidak menyebut "maks".
  - `ADA_HENTI` lawan teks henti: 133/134.
  - Varian kod = pilihan peraturan registry tugasan_v3 (skor tertinggi bukan DITOLAK, jika tiada, CAGR tertinggi): 134/134.
  - Varian dalam `analisis/papan`: 134/134.
  - Katalog dan modul masing-masing ada 134 kaedah, tiada yang tertinggal.
  — [tugasan_v3.md:23](BacktestShariah2/standard/tugasan_v3.md); skrip `semak_kat.py`
- 47 kaedah K145+ (M115–M161): `HENTI_KOD`, `KELUAR_KOD` dan TMAX sepadan dengan teks katalog. Contoh: M150 PCT12/SMA20/21 = "Tetap 12%… SMA20… Maks 21 hari"; M153 PCT12/CHAN2/10 = "Chandelier … 2×ATR22 … Maks 10 hari"; M158 ASAL dengan `exitc=c < s50` = "Tutup di bawah SMA50"; M161 `exitc=(c<e21)&(c.shift()<e21.shift())` = "2 tutup berturut di bawah EMA21". — [kod/kaedah/M158.py:26](BacktestShariah2/kod/kaedah/M158.py); [kod/kaedah/M161.py:28](BacktestShariah2/kod/kaedah/M161.py); skrip `semak_kat2.py`
- Semakan makna secara manual: M36 (pecah high 55 hari + tutup > SMA50; henti buka masuk − 2N; keluar tutup < SMA50), M02 (TMAX 20, sasaran 3R), M20 (TMAX 20, 2R), M78, M81, M40/M45 (8 slot, rentas saham) sepadan dengan kod. — [kod/kaedah/M36.py](BacktestShariah2/kod/kaedah/M36.py); [kod/kaedah/M02.py](BacktestShariah2/kod/kaedah/M02.py)
- **Ketidakpadanan 1, M31**: teks henti katalog bermula "Tiada henti harga; henti tutup di bawah band bawah…". Halaman memadankan `/^tiada henti/` lalu memaparkan pil merah "⚠ Tiada henti". Tetapi kod ada `ADA_HENTI = True` dan, sejak 23 Okt, `HENTI_TUTUP = '_lo'` (henti ikut tutup = LOWER BB hari isyarat). — [kod/kaedah/M31.py:7-10](BacktestShariah2/kod/kaedah/M31.py); [dashboard_v2.html:1898](BacktestShariah2/standard/dashboard_v2.html)
- **Ketidakpadanan 2, ayat pegang**: M117, M125, M130 dan M136 tertulis "Tiada had masa; pegang sehingga isyarat keluar atau henti". Tetapi teks keluar katalog ialah "Tiada; hanya henti/had masa", dan kod memanggil `siap_lajur(..., stop)` tanpa `exitc`. Maknanya posisi hanya keluar apabila kena henti. M145, M147, M149 dan M157 pula ditulis dengan betul ("tiada isyarat keluar; pegang sehingga kena henti"). Dalam backtest, M130 dan M149 dipegang purata 261 dan 272 hari. — [kod/kaedah/M117.py:31](BacktestShariah2/kod/kaedah/M117.py); db `kaedah/katalog`; registry 431
- **Teks umum tidak lengkap**: jalur "Sama untuk semua" menerangkan belian buka esok, urutan keluar dan lorong 2. Ia tidak menyebut peraturan berikut:
  - penapis tidak layak (ambil alih, tidak cair, kelas berganda; 21–22 Okt)
  - belian semula selepas lorong kaedah keluar (19 Okt)
  - had 10 isyarat setiap kaedah setiap malam (`MAKS_KAEDAH`)
  - kaedah mingguan dibeli hujung minggu sahaja
  - 47 kaedah K145+ tiada watchlist (`hampir()` memulangkan None)
  — [dashboard_v2.html:1960](BacktestShariah2/standard/dashboard_v2.html); [kod/kaedah/M140.py:41-43](BacktestShariah2/kod/kaedah/M140.py); [CLAUDE.md](CLAUDE.md)
- Kaedah replika (`REPLIKA`, 13 modul) menilai posisi hadapan ikut dagangan sendiri sejak 22 Okt. Ini mengubah pelaksanaan, bukan peraturan, jadi teks katalog kekal betul. — [kod/dagangan.py](BacktestShariah2/kod/dagangan.py)

### Inferences
- Katalog boleh dipercayai sebagai sumber "cara kaedah berfungsi". Ia hanya perlu (a) dibetulkan pada M31 dan 4 ayat pegang, dan (b) dijaga oleh ujian unit (varian_kod == VARIAN, TMAX, ADA_HENTI) supaya tidak terpisah daripada kod. Kini tiada penulis automatik `kaedah/katalog`.
- Bagi pemilihan kaedah dengan wang sebenar, maklumat "tiada isyarat keluar, tiada had masa" (8 kaedah) patut ditanda dengan jelas. Ia mempengaruhi tempoh pegang dan modal yang terikat.

### Gaps
- Teks syarat masuk 87 kaedah asal tidak disemak baris demi baris dengan setiap baris kod `sedia()`. Saya hanya menyemak makna 8 kaedah secara manual; selebihnya disemak secara program pada varian, TMAX, henti dan kod K145+.

## Soalan 3: Adakah tab Backtest konsisten dengan Analisis (jangkaan backtest sama)?

### Takeaway
Angka mentahnya sama (CAGR dan purata setiap dagangan bagi varian aktif: 0 beza dalam 134 kaedah). Tetapi keputusannya bercanggah. Tab Backtest memberi pingat kepada 44 kaedah, dengan podium M30, M79 dan M111. Analisis pula: 0 kaedah lulus ujian 2000 saham AS, hanya 6 lulus S1–S4, dan tiada satu pun pemenang Emas berada dalam kedudukan Analisis. Puncanya: ujian 2 datang daripada set data berbeza, ambang langkah 6–7 berbeza, dan takrif "swing" berbeza.

### Cited Findings
- Corong `kpM()` yang direplika: 141 kaedah dalam registry 431 (134 aktif; M114 dan M162–M167 tidak aktif). Bilangan yang lulus setiap langkah: 139 → 108 → 99 → 95 → 91 → 84 → **44**. Pingat: 2 Emas (M30, M79), 21 Perak, 21 Gangsa. — [dashboard_v2.html:869-876,881-899](BacktestShariah2/standard/dashboard_v2.html); skrip `semak_bt.py`
- Angka sama: `bt_cagr` dan `bt_purata` Analisis = cagr dan avg×100 baris registry varian aktif, dengan 0 beza dalam 134 kaedah (contoh M30 52.02% dan 3.8%; M79 35.52% dan 6.25%). — db `analisis/papan`; registry
- **Langkah 6** (Backtest) lulus jika CAGR S1–S4 semuanya > 0: **123** kaedah lulus. Analisis memerlukan varian sama mengatasi EW dalam ≥ 3/4 subset: hanya **6** kaedah lulus (`lulus_subset`). — [penganalisis.py:10,117,175](BacktestShariah2/standard/penganalisis.py)
- **Langkah 7** (Backtest) memakai `autotune/a02_saringan` (A02, PARAM asal, 2013–2018), mengambil lorong terbaik antara asal dan had60, dan lulus jika min(cA, cB) > 0: **70** kaedah lulus. Daripada 70 itu, 68 mempunyai CAGR di bawah SPY tempoh sama (12.04%). Contoh yang "lulus": M26 0.05%/thn, M74 0.07%, M88 0.08%. Analisis memakai **A01** (`AUTOTUNE/hasil/papan.json`, 2013 – Sep 2024) dengan syarat CAGR > SPY dalam kumpulan A **dan** B: **0** kaedah lulus (`lulus_at`). Label A02 sendiri: 0 LULUS / 40 TIDAK LULUS. Label A01: 0 TINGGI, 0 SEDERHANA, 70 RENDAH, 64 GAGAL. — [penganalisis.py:11,47,165-179](BacktestShariah2/standard/penganalisis.py); [AUTOTUNE/hasil_a02/ringkasan.json](AUTOTUNE/hasil_a02/ringkasan.json); [AUTOTUNE/hasil/ringkasan.json](AUTOTUNE/hasil/ringkasan.json)
- Podium Backtest dibandingkan dengan Analisis:
  - **M30** (Emas, skor 76.2, "RM10k → ~RM180k"): Analisis skor 1.9, subset 1/4 gagal, A01 RENDAH gagal, kekal 0.5, bukan swing (pegang 33.7 hari), tiada kedudukan.
  - **M79** (Emas): subset 4/4 lulus, WFO gagal, A01 GAGAL, bukan swing (59.8 hari), tiada kedudukan.
  - **M111** (Perak): kedudukan Analisis #10.
  
  24/44 kaedah berpingat bukan swing (> 30 hari), jadi tiada kedudukan dalam Analisis. — db `analisis/papan`; [CLAUDE.md](CLAUDE.md) ("Swing = pegang 3–30 hari")
- Analisis #1 **M21** dan #2 **M140** adalah DITOLAK dalam registry dan tidak mendapat pingat (lulus 5/7). #3 M144, #4 M32, #7 M55 dan #8 M77 berpingat Perak. — db `analisis/papan` (`kedudukan`)
- "Carta & gaya", KPI "Terbaik gaya anda": `bestBy(..., 'avg')` memilih varian terbaik merentas **semua** varian, termasuk DITOLAK dan bukan aktif. Yang tertinggi ialah **M24 V4 ROC6** (DITOLAK, bukan varian aktif, +10.07% setiap entry). Penapis "gaya" juga memakai pegang ≤ 40 hari, sedangkan swing Analisis 3–30 hari. — [dashboard_v2.html:984-987](BacktestShariah2/standard/dashboard_v2.html)
- Lajur "Papertrade C" dalam Backtest/Kaedah memakai `prStats()`: kasar, campur posisi terbuka dan tertutup, harga terkini, label TERUSKAN/PERHATI/HENTIKAN daripada skor U×S yang sudah bersara. Analisis `c_purata` bersih 0.1% setiap belah dan dinilai pada 22 Okt. Akibatnya kaedah sama menunjukkan nombor berbeza: M30 +3.24 lawan +2.86; M111 +3.63 lawan +3.13; M21 −0.34 lawan +2.77 (M21 C n=1, terbuka). — [dashboard_v2.html:1552-1564](BacktestShariah2/standard/dashboard_v2.html); [penganalisis.py:80,102,530](BacktestShariah2/standard/penganalisis.py)
- Kos muat: koleksi `registry` (~2.0 MB, termasuk 32 dokumen indikator I ~0.31 MB yang "tidak digunakan") dan `autotune` (~0.24 MB) dilanggan setiap kali halaman dibuka, walau tab mana yang dipilih. — [dashboard_v2.html:3778-3836](BacktestShariah2/standard/dashboard_v2.html); [tugasan_v3.md:23](BacktestShariah2/standard/tugasan_v3.md)

### Inferences
- Pemilik melihat dua jawapan bercanggah kepada "kaedah mana yang terbukti". Tab Backtest berkata 44 kaedah lulus 7 langkah termasuk ujian 2000 saham. Analisis berkata tiada kaedah lulus ujian 2000 saham dan hanya 6 lulus S1–S4. Ambang ">0" dalam langkah 6–7 terlalu longgar untuk wang sebenar, dan langkah 7 memakai data A02 yang tidak dipakai Analisis.
- Podium "Terbaik ikut backtest" dan "RM10k →" ialah nombor dalam sampel, selepas pemilihan varian, tanpa potongan "kekal". Ia tidak patut dipapar setara dengan ranking Analisis.

### Gaps
- Tidak disemak sama ada A03 (fokus kadar menang) atau WFO W01 memberi gambaran ketiga. Analisis memakai WFO (22 kaedah lulus); tab Backtest tidak memaparkan WFO langsung.

## Soalan 4: Cadangan setiap panel (kekal / gabung / naik taraf / buang) dan kegunaan

### Takeaway
Bagi operasi harian, hanya Watchlist (calon hampir) yang benar-benar dipakai. Itu pun separuh kandungannya ialah isyarat lengkap yang menduplikasi senarai beli. Backtest dan Kaedah patut disatukan ke Profil kaedah dan "Lagi › Backtest". Kriteria langkah 6–7 Backtest perlu diselaraskan dengan Analisis atau dibuang. Sektor perlu memaparkan gred kumpulan v2 yang sudah disahkan, dan membuang medan SST yang beku. Cadangan ini selari dengan laporan audit awal dan menambah pembetulan data.

### Cited Findings
- Laporan audit awal sudah mencadangkan Watchlist ke Hari Ini, Backtest ke Lagi, Kaedah ke Profil, dan Sektor ke Lagi › Konteks pasaran, serta membuang fasa rotasi dan skor panas. Halaman masih 8 tab (v103). — [reports/Audit dan reka semula dashboard.md:120-182](reports/Audit%20dan%20reka%20semula%20dashboard.md); [dashboard_v2.html:707-714,753](BacktestShariah2/standard/dashboard_v2.html)
- Gred kumpulan v2 (Weinstein; satu-satunya definisi yang tersusun A→E dan signifikan; A +0.03% … E −1.21% setiap dagangan) dipakai dalam gred watchlist dan posisi. Tab Sektor tidak memaparkannya; ia memaparkan fasa dan skor panas yang, menurut nota halaman sendiri, "tidak meramal". — [tugasan_v3.md:83](BacktestShariah2/standard/tugasan_v3.md); [dashboard_v2.html:1268](BacktestShariah2/standard/dashboard_v2.html)
- 47/134 kaedah (K145+) tiada watchlist. Daripada 20 kaedah teratas Analisis, hanya 9 ada baris watchlist (28/179 baris). Antara yang tiada: #1 M21, #2 M140, #3 M144. — skrip; db `analisis/papan`
- `sektor/snapshot` sudah membawa `posisi_c`, `untung_c` dan `posisi_m` bagi 109 kumpulan (pendedahan posisi), tetapi tiada panel memaparkannya. — db `sektor/snapshot`; [dashboard_v2.html:1204-1285](BacktestShariah2/standard/dashboard_v2.html)

**Jadual cadangan panel**

| Tab | Panel | Cadangan | Sebab / cara |
|---|---|---|---|
| Watchlist | Headline + KPI "Calon", "≥ 99% hampir" | GABUNG ke Hari Ini › Esok "Hampir isyarat" | KPI ≥ 99% dipisah menjadi "≥ 99%" dan "paras disentuh" (9 baris kini bercampur); paparkan "harga 23 Okt · gred 22 Okt" |
| Watchlist | KPI "Sektor terbanyak" | BUANG | Tiada keputusan bergantung padanya |
| Watchlist | Jadual Hampir Signal | KEKAL, NAIK TARAF | Tambah lajur status/kedudukan Analisis dan susun ikut kedudukan; tanda "tiada watchlist" bagi 47 kaedah K145+; tulis 99.9, bukan 100, di sumber (rutin 6:02), atau label "disentuh"; jelaskan had umur (LNTH 12 hari lawan `TAMAT_WATCH` 10); `gred_pada` = tarikh data |
| Watchlist | Isyarat lengkap dalam watchlist (92 baris) | GABUNG ke Hari Ini "Beli pada buka" | Ia pratonton senarai beli esok (19/19 disahkan); jejak "tidak dibeli" ke Sistem |
| Backtest › Keputusan | Podium "Terbaik ikut backtest" + RM10k → | BUANG (atau turunkan ke Lagi dengan label "dalam sampel") | Bercanggah dengan Analisis: M30/M79 bukan swing, tiada kedudukan |
| Backtest › Keputusan | Corong 7 langkah + pingat | NAIK TARAF atau BUANG langkah 6–7 | Selaraskan dengan Analisis (S1–S4 atasi EW ≥ 3/4; A01 > SPY A dan B; tambah WFO) atau papar faktor "kekal". Kini 123 lawan 6 dan 70 lawan 0 |
| Backtest › Keputusan | Jadual Semua kaedah | GABUNG ke Profil kaedah › Backtest | Angka sama dengan Analisis `bt_*` |
| Backtest | Lajur/podium "Papertrade C" | BUANG | Pendua dan tidak konsisten dengan Analisis `c_purata` dan `h_purata`; label U×S bersara |
| Backtest › Butiran | Papan penuh (665 varian, 32 indikator I) | PINDAH ke Lagi › Backtest mentah, dimuat atas permintaan | Buang langganan dokumen I (tidak digunakan); jimat ~2 MB setiap buka |
| Backtest › Butiran | Carta & gaya (KPI "Terbaik gaya anda") | BUANG KPI atau hadkan ke varian aktif dan swing 3–30 hari | Kini menobatkan M24 V4 (DITOLAK, tidak didagang) |
| Backtest › Butiran | Banding varian | KEKAL dalam Lagi (penyelidikan) | Berguna semasa memilih varian; bukan operasi harian |
| Backtest › Butiran | AUTOTUNE (Semua lorong A/B, A02, A03, A01) | PINDAH ke Lagi; KEKAL A01 sahaja di depan | A01 ialah sumber Analisis; label A02 "PARAM asal 2013–2018 · SPY 12.0%"; buang paparan kemajuan tala (siap 18 Okt) |
| Global | "Langsung · ujian terkini 2026-10-17" | UBAH | "Backtest beku 17 Okt · AUTOTUNE 18 Okt" |
| Kaedah | Jadual katalog (masuk/keluar/pegang/henti) | KEKAL, GABUNG ke Profil › Cara kaedah berfungsi | Betul bagi 134/134; betulkan pil M31; betulkan ayat pegang M117/M125/M130/M136; tanda 8 kaedah "tiada keluar, tiada had masa"; tambah ujian unit penyegerakan katalog dengan kod |
| Kaedah | Jalur "Sama untuk semua" | NAIK TARAF, PINDAH ke Panduan | Tambah penapis tidak layak, kelas berganda, belian semula, had 10, kaedah mingguan, "K145+ tiada watchlist" |
| Kaedah | KPI teks (pencipta, had masa, buka esok) | BUANG (kecuali "Dua lorong" ke Panduan) | Teks tetap, tiada keputusan |
| Kaedah | Lajur Backtest (set 431) | GABUNG (pendua tab Backtest) | Satu sumber dalam Profil |
| Kaedah | Lajur Papertrade C (TERUSKAN/PERHATI/HENTIKAN) | BUANG atau GANTI dengan label pantau Analisis + `h_purata` | Label lama bercanggah dengan BERSARA/GANTUNG/AMARAN/OK |
| Sektor | Peta haba | PINDAH ke Lagi › Konteks pasaran | Buang togol 1H (sentiasa kosong) |
| Sektor | Jadual ranking sektor & industri | NAIK TARAF | Tambah gred v2 (A–E, skor, tiga syarat Weinstein, `m1m_med`) daripada `data/kumpulan`; buang 1H; buang atau kelabukan RS/VR/aliran SST (beku ≤ 14 Okt; 121/138 kosong) atau paparkan tarikhnya |
| Sektor | Fasa rotasi + KPI Fasa + lajur Fasa | BUANG | Tidak meramal (nota halaman); diganti gred v2 |
| Sektor | Aliran institusi & volum ("hari ini") | BUANG, atau KEKAL dengan cap tarikh hanya jika SST dipulihkan | Data ≥ 3–4 sesi dilabel "hari ini" |
| Sektor | 10 industri 1M terkuat | NAIK TARAF | Jadikan "industri gred A/B + calon watchlist/posisi di dalamnya"; buang kelas berganda pendua (BF.A/BF.B, PBR/PBR.A) |
| Sektor | Nota kalibrasi | PINDAH ke Panduan | – |
| (tiada) | Pendedahan posisi C ikut sektor/industri | TAMBAH dalam Posisi/Risiko | Medan `posisi_c`/`untung_c` sudah ada dalam doc tetapi tidak dipapar; penting untuk risiko tumpuan |

### Inferences
- Untuk memilih kaedah dengan wang sebenar, hanya katalog (cara berfungsi) dan angka backtest yang sama dengan Analisis berguna. Pingat, podium dan "Terbaik gaya" mengelirukan kerana menobatkan kaedah bukan swing atau varian yang tidak didagang.
- Untuk operasi harian, keperluan utama ialah calon hampir yang disusun ikut kaedah berstatus baik dalam Analisis. Watchlist kini disusun ikut % hampir dan 51% kandungannya pendua senarai beli.
- Keperluan yang tiada: cap tarikh data setiap panel (gred, SST, backtest), status Analisis pada setiap baris watchlist, dan pendedahan sektor bagi posisi terbuka.

### Gaps
- Tiada data penggunaan sebenar (klik atau masa dalam tab), jadi anggaran "panel tidak pernah digunakan" dibuat berdasarkan kandungan, bukan telemetri.
- Saya tidak menyemak sama ada SST Terminal sudah boleh disambung semula (jika ya, medan SST boleh disegarkan dan tidak perlu dibuang).
