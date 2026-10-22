# Rombak papan kepada empat jawapan pantas

Papan Backtest Shariah versi 102 patut dirombak menjadi **empat tab (Hari Ini, Kaedah, Posisi, Lagi)**, dengan laman pembuka yang menjawab empat soalan pemilik dalam tiga blok dan satu lampu sistem, **satu ranking kaedah sahaja** (skor sebulan Papan Penganalisis atas Lejar Penuh matang, akhirnya diukur lawan EW), dan satu kosa kata status lima keadaan. Masalah terasnya bukan susun atur tetapi jawapan yang bercanggah: pada 22 Okt 2026 soalan "kaedah mana terbaik?" mendapat sekurang-kurangnya empat jawapan (M21 di Analisis, M70 di Ringkasan dan Prestasi, M48 dalam jadual Untung×Selamat, pingat backtest di podium) daripada enam ranking dan sembilan set label, dengan AMARAN, PERHATI dan BELUM CUKUP masing-masing membawa dua atau tiga makna. Jawapan jujur hari ini ialah **"belum ada kaedah terbukti"** — 0 daripada 7,161 posisi hadapan sudah matang, semua 134 kaedah berstatus BELUM CUKUP, dan kaedah pertama dijangka cukup data pada 26 Okt 2026 — tetapi tiada satu skrin pun menyatakannya. Dua syarat kejayaan pemilik tidak diukur langsung: **EW saham Shariah tidak dijejak ke hadapan** (semua perbandingan hadapan memakai SPY) dan **sasaran 10% sebulan tidak dipapar di mana-mana**, walaupun CAGR backtest tertinggi (58.15% setahun, kira-kira 3.9% sebulan) jauh di bawahnya. Lampu "Data n/8" pula hanya menguji tarikh, jadi ralat larian, kegagalan CI, mod bayang dan langkah yang gagal senyap tidak kelihatan, sementara papan memuat kira-kira 4 MiB data setiap kali dibuka tanpa mengira tab. Sebelum membina semula, saluran data perlu dibaiki dahulu: `papan.json` belum mempunyai medan pantau, portfolio 10 slot tidak maju ke sesi 21 Okt walaupun Lejar sudah, Analisis ketinggalan satu sesi setiap pagi tanpa label, `MOD_ACTIONS` masih `bayang`, dan beberapa dokumen peraturan bercanggah. Sembilan perubahan memerlukan kelulusan jelas pemilik; enam menterbalikkan keputusan terdahulu, yang terbesar ialah persaraan label TERUSKAN/PERHATI/HENTIKAN (tugasan_v3 §7, 14 Okt 2026).

> **Nota data dan tanda.** Semua angka menggambarkan keadaan **22 Okt 2026**. Db dashboard dibaca secara baca sahaja pada pagi 22 Okt (`analisis/papan` versi 5 dibina 21 Okt 23:15 MYT dengan data 20 Okt; `papertrade/ringkas_c` versi 4 dibina 06:30 MYT dengan harga tutup 21 Okt; `harian/status` versi 34), dan repo dibaca pada commit `8bcab4f` (07:40 UTC) dengan semakan susulan penyelidik pada 07:42 UTC. Angka tanpa tanda dibaca terus daripada repo atau db. Angka bertanda **[anggaran]** ialah kiraan semula penyelidik (contohnya label §7 yang dikira semula daripada CSV, kiraan panel daripada kod, dan anggaran muatan) dan boleh berbeza sedikit daripada halaman langsung. `H:n` bermaksud `BacktestShariah2/standard/dashboard_v2.html` baris n (versi 102). Sumber luar tentang amalan reka bentuk disahkan melalui ringkasan carian dan abstrak kerana proksi menyekat teks penuh beberapa laman (NN/g, Material, Darwinex); heuristik "5 saat" dan "3–5 KPI" ialah konvensyen industri, bukan dapatan kajian terkawal.

## Lapan tab memberi empat jawapan berbeza kepada satu soalan

### Kira-kira 53 panel dan 389 dokumen dimuat setiap kali dibuka

Papan versi 102 mempunyai **lapan tab** ([H:591](../BacktestShariah2/standard/dashboard_v2.html#L591)) dan kira-kira **53 panel** [anggaran, dikira daripada kod]. Tiga tab keputusan sahaja sudah padat. Ringkasan memuatkan 7 panel, jalur status 8 cip dan 4 KPI ([H:3028](../BacktestShariah2/standard/dashboard_v2.html#L3028)); Analisis memuatkan 4 panel dan satu jadual 134 kaedah dalam 6 atau 16 lajur ([H:3090](../BacktestShariah2/standard/dashboard_v2.html#L3090)); dan Prestasi memuatkan **22 panel** dengan kira-kira 15 carta, 7 jadual dan sekurang-kurangnya 12 kumpulan togol ([H:1702](../BacktestShariah2/standard/dashboard_v2.html#L1702)), termasuk jadual "Skor kaedah swing" 35 lajur yang lebih rumit daripada seluruh tab Analisis ([H:2776](../BacktestShariah2/standard/dashboard_v2.html#L2776)). Lima tab lain menambah kira-kira 20 panel lagi: Posisi menawarkan empat pandangan jadual (8, 19, 11 dan 10 lajur) atas **4,240 posisi Papertrade C** dan tiga akaun ([H:1342](../BacktestShariah2/standard/dashboard_v2.html#L1342), [H:2946](../BacktestShariah2/standard/dashboard_v2.html#L2946)), Backtest mempunyai 19 kombinasi set × sub-paparan ([H:610](../BacktestShariah2/standard/dashboard_v2.html#L610), [H:1940](../BacktestShariah2/standard/dashboard_v2.html#L1940)), manakala Watchlist, Kaedah dan Sektor masing-masing memapar 212, 134 dan 149 baris ([db](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)). Glosari `TIPS` mengandungi **162 istilah** ([H:3197](../BacktestShariah2/standard/dashboard_v2.html#L3197)), satu ukuran kasar bilangan konsep yang perlu difahami pemilik sebelum dapat membaca papan dengan yakin.

Navigasinya berlapis empat — 8 tab, subbar (akaun, Keputusan/Butiran, set saham), seg ketiga Butiran, dan tab sisi di dalam tab dengan butang Papar senarai, Lipat semua dan Buka semua ([H:601](../BacktestShariah2/standard/dashboard_v2.html#L601), [H:3403](../BacktestShariah2/standard/dashboard_v2.html#L3403)). Di skrin ≤ 520px, lapan tab dibalut menjadi dua baris dalam pengepala melekit ([H:303](../BacktestShariah2/standard/dashboard_v2.html#L303)), dan tab sisi menyembunyikan tajuk, KPI dan jalur status di sebalik cip "Gambaran" ([H:3436](../BacktestShariah2/standard/dashboard_v2.html#L3436)). Akibatnya, **skrin pertama Ringkasan di telefon hanya menunjukkan "3 perkara utama"** — dua atau tiga ayat panjang — manakala Esok, Berubah, KPI dan status data memerlukan ketikan tambahan. Papan juga dibuka semula pada tab terakhir yang dilawati, bukan Ringkasan ([H:646](../BacktestShariah2/standard/dashboard_v2.html#L646), [H:724](../BacktestShariah2/standard/dashboard_v2.html#L724)), jadi "10 saat pertama" boleh bermula di Prestasi. Dikira daripada kod, soalan (1) memerlukan 2–3 klik serta kefahaman kira-kira 30 konsep statistik; soalan (2) memerlukan 1–2 ketikan di telefon; soalan (3) memerlukan sekurang-kurangnya 4 ketikan, kerana tab Posisi tiada penapis "hampir paras keluar" dan lalainya menyusun posisi terbaik dahulu ([H:1367](../BacktestShariah2/standard/dashboard_v2.html#L1367), [H:2324](../BacktestShariah2/standard/dashboard_v2.html#L2324)); dan soalan (4) satu ketikan, tetapi hanya menunjukkan tarikh.

Muatan juga mahal. Fungsi `connect()` melanggan **389 dokumen db, kira-kira 3.97 MiB JSON padat**, tanpa mengira tab yang dibuka ([H:3457](../BacktestShariah2/standard/dashboard_v2.html#L3457); saiz diukur daripada [db](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)). Registry backtest sahaja 1,337.9 KiB dan posisi C 1,432.3 KiB — lebih besar daripada 3.6 MB yang direkod selepas versi 90 ([dashboard.md:3](../BacktestShariah2/standard/dashboard.md#L3)). Setiap dokumen yang tiba melukis semula tab semasa ([H:671](../BacktestShariah2/standard/dashboard_v2.html#L671)), fail HTML sendiri 490,841 bait, dan pada versi 85 ketinggian halaman di 390px sudah 8,093px bagi Prestasi dan 5,862px bagi Sektor ([binaan_v2_log_tambahan.md:201](../BacktestShariah2/standard/binaan_v2_log_tambahan.md#L201)). Dengan 79–819 belian C sehari, jadual satu-baris-satu-posisi akan melepasi 10,000 baris dalam beberapa minggu [anggaran], jadi reka bentuk sekarang bertambah perlahan setiap hari.

### Enam ranking atas tiga asas data menobatkan kaedah berbeza

Sekurang-kurangnya enam ranking "kaedah terbaik" wujud serentak, setiap satu dengan formula, asas data dan pintu sampel sendiri, dan pada data 20–22 Okt masing-masing menobatkan kaedah yang berbeza.

| Ranking | Tempat | Asas data dan pintu | Teratas |
|---|---|---|---|
| Terbaik ikut papertrade (label §7, skor U×S) | Ringkasan ([H:3014](../BacktestShariah2/standard/dashboard_v2.html#L3014)) | C, semua dagangan termasuk yang dipegang, tanpa kos; label selepas ≥ 20 tutup | M70: PERHATI, U×S 42, +3.07%, 29 tutup [anggaran] |
| Terbaik ikut % untung | Prestasi: tajuk, KPI, panel ([H:1718](../BacktestShariah2/standard/dashboard_v2.html#L1718), [H:2879](../BacktestShariah2/standard/dashboard_v2.html#L2879)) | C, purata semua dagangan, ≥ 20 selesai | M70 [anggaran] |
| Kedudukan kaedah · Skor U×S | Prestasi ([H:1734](../BacktestShariah2/standard/dashboard_v2.html#L1734)) | C, semua kaedah termasuk BELUM CUKUP DATA | M48 (skor 60, belum cukup data) [anggaran] |
| Skor kaedah swing v2 dan gabungan beku | Prestasi ([H:2566](../BacktestShariah2/standard/dashboard_v2.html#L2566)) | C; matang jika cukup, jika tidak semua posisi; lorong terbaik; bersih kos | M70 84% (beku #1) ([gabungan_beku.json](../BacktestShariah2/data/analisis/gabungan_beku.json)) |
| Kedudukan kaedah (Papan Penganalisis) | Analisis ([H:3132](../BacktestShariah2/standard/dashboard_v2.html#L3132)) | Lejar dan C pra-Lejar, matang sahaja, bersih kos, dikecutkan ke jangkaan backtest | M21 +3.40% sebulan ([PENGANALISIS.md:7](../BacktestShariah2/laporan/PENGANALISIS.md#L7)) |
| Podium backtest | Ringkasan, Backtest ([H:805](../BacktestShariah2/standard/dashboard_v2.html#L805)) | Enjin v1.2, pingat varian aktif | 2 Emas daripada 44 berpingat [anggaran] |

Percanggahan ini bukan kes tepi. Tiga kaedah gabungan beku yang dipilih skor swing v2 (M70, M03, M18) berada di kedudukan **#35, #40 dan #53 daripada 75** kaedah swing dalam Papan Penganalisis, dan M03 berstatus DITOLAK dalam backtest. Kaedah #1 Penganalisis (M21) juga DITOLAK dan hanya mempunyai satu posisi C, manakala ketiga-tiga kaedah GUNA backtest (M96, M30, M79) langsung tidak muncul dalam senarai swing kerana pegangannya melebihi 30 hari ([papan.json](../BacktestShariah2/data/analisis/papan.json)).

| Kaedah | Skor swing v2 (C) | Penganalisis: kedudukan / 75, skor sebulan | Label §7 (C) [anggaran] | Status backtest |
|---|---|---|---|---|
| M70 | 84%, beku #1 | #35, +0.43% | PERHATI (29 tutup, +3.07%) | SIMPAN |
| M03 | 76%, beku | #40, +0.39% | PERHATI (56 tutup) | **DITOLAK** |
| M18 | 74%, beku | #53, +0.29% | PERHATI | UJI KERTAS |
| M21 | tidak layak (1 posisi C) | **#1**, +3.40% | BELUM CUKUP | **DITOLAK** |
| M140 | tidak layak | #2, +2.25% | BELUM CUKUP | DITOLAK |
| M96, M30, M79 | di luar pintu swing | tiada kedudukan swing | – | **GUNA** |

Puncanya tiga perbezaan. Pertama, **asas data**: label §7, "% untung" dan skor v2 memakai Papertrade C termasuk posisi yang masih dipegang, manakala Penganalisis memakai Lejar Penuh (semua isyarat) dan posisi matang sahaja ([H:1437](../BacktestShariah2/standard/dashboard_v2.html#L1437), [tugasan_v3.md:113](../BacktestShariah2/standard/tugasan_v3.md#L113)); kod sendiri mengakui konflik ini dalam nota `notaAsas` ([H:1498](../BacktestShariah2/standard/dashboard_v2.html#L1498)). Kedua, **pemberat bukti hadapan**: skor v2 memberi data C yang belum matang kira-kira 64% wajaran, berbanding kira-kira 25% dalam Penganalisis ([Skor KPI pemilihan kaedah swing.md:42](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L42)). Ketiga, **penapis backtest**: tiada ranking hadapan memakai status DITOLAK, jadi kaedah yang gagal backtest boleh menduduki tempat pertama. Label §7 dan "Terbaik ikut % untung" juga menyebelahi kaedah yang keluar cepat, kerana ambang 20 dagangan tertutup dicapai dahulu oleh kaedah yang kena henti awal ([Skor KPI pemilihan kaedah swing.md:48](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L48)). Laporan skor projek sendiri sudah menyimpulkan bahawa pembaikan paling murah dan paling besar kesannya ialah **menyatukan dua papan** supaya kedua-duanya berkongsi satu prior, satu takrif matang dan satu n berkesan ([Skor KPI pemilihan kaedah swing.md:93](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L93)).

### Sembilan set label, dengan perkataan sama membawa makna berbeza

Dalam tiga tab keputusan sahaja, pemilik bertemu sekurang-kurangnya **sembilan set label**: TERUSKAN/PERHATI/HENTIKAN/BELUM CUKUP DATA ([H:1446](../BacktestShariah2/standard/dashboard_v2.html#L1446)); "Terlalu awal hingga <tarikh>" ([H:1485](../BacktestShariah2/standard/dashboard_v2.html#L1485)); keyakinan rendah/sederhana/tinggi ([H:1479](../BacktestShariah2/standard/dashboard_v2.html#L1479)); pingat GUNA/UJI KERTAS/SIMPAN ([H:805](../BacktestShariah2/standard/dashboard_v2.html#L805)); KUAT/PERHATI/LEMAH/AMARAN/BELUM CUKUP ([H:3077](../BacktestShariah2/standard/dashboard_v2.html#L3077)); Teras/Calon/Calon (awal)/Pantau/Belum layak/Gantung/Bersara ([H:2586](../BacktestShariah2/standard/dashboard_v2.html#L2586)); pantau BERSARA/GANTUNG/AMARAN/OK ([H:2742](../BacktestShariah2/standard/dashboard_v2.html#L2742)); "⚠ AMARAN" dalam Paling Teruk ([H:1451](../BacktestShariah2/standard/dashboard_v2.html#L1451)); dan untung bergerak di bawah/dalam/atas julat ([H:2399](../BacktestShariah2/standard/dashboard_v2.html#L2399)). Tab Backtest menambah lagi kosa kata AUTOTUNE, daripada TINGGI hingga BELUM DITALA, LULUS/CALON dan MENANG/HAMPIR ([H:1853](../BacktestShariah2/standard/dashboard_v2.html#L1853), [H:1941](../BacktestShariah2/standard/dashboard_v2.html#L1941)).

Yang paling mengelirukan ialah perkataan sama dengan makna berbeza. **AMARAN** bermaksud t < −2 lawan jangkaan dalam Analisis, satu amaran CUSUM dalam lajur Pantau, dan ambang kadar gagal atau kerugian dalam Paling Teruk ([H:3356](../BacktestShariah2/standard/dashboard_v2.html#L3356), [H:2816](../BacktestShariah2/standard/dashboard_v2.html#L2816)). **PERHATI** bermaksud skor U×S 25–55 di satu tempat dan julat 95% merentas sifar di tempat lain ([H:3320](../BacktestShariah2/standard/dashboard_v2.html#L3320)). "BELUM CUKUP DATA" (< 20 tutup), "BELUM CUKUP" (< 20 matang atau < 10 hari beli) dan "Belum layak" ialah tiga pintu berbeza; nombor "20" membawa lima makna; dan perkataan "Skor" merujuk kepada empat skala — U×S 0–100, skor swing 0–100%, skor sebulan dalam % pulangan, dan skor enjin backtest.

### Barang warisan dan teks lapuk masih memandu skrin utama

Beberapa elemen bercanggah dengan peraturan semasa. KPI Ringkasan masih memapar "USD1,000 setiap belian" dan podium backtest "RM10,000 → RM…", walaupun pemilik meminta prestasi dalam % sahaja pada versi 95 ([H:3036](../BacktestShariah2/standard/dashboard_v2.html#L3036), [H:808](../BacktestShariah2/standard/dashboard_v2.html#L808), [dashboard.md:3](../BacktestShariah2/standard/dashboard.md#L3)); tugasan_v3 §7 sendiri masih mewajibkan metrik USD1,000 ([tugasan_v3.md:77](../BacktestShariah2/standard/tugasan_v3.md#L77)). Label §7 masih label utama Ringkasan, dan strip "Cara baca" masih mengarahkan "pilih kaedah yang TERUSKAN" ([H:1761](../BacktestShariah2/standard/dashboard_v2.html#L1761)), walaupun log binaan sudah menanda keputusan Prestasi sebagai "terlalu awal untuk wang sebenar" ([binaan_v2_log.md:202](../BacktestShariah2/standard/binaan_v2_log.md#L202)). Akaun Moomoo lama, yang tiada belian baharu sejak 13 Okt, masih satu daripada tiga pilihan akaun, dan dokumennya (65.7 KiB) dimuat setiap kali papan dibuka ([H:641](../BacktestShariah2/standard/dashboard_v2.html#L641), [H:3493](../BacktestShariah2/standard/dashboard_v2.html#L3493)).

Tab Sektor masih memapar fasa rotasi di empat tempat ([H:1134](../BacktestShariah2/standard/dashboard_v2.html#L1134)), walaupun kalibrasi menyatakan skor panas dan fasa tidak meramal pulangan 1–3 bulan dan "TIDAK digunakan sebagai penapis" ([dashboard.md:21](../BacktestShariah2/standard/dashboard.md#L21)); data SST di dalamnya pula basi sejak 19 Okt ([binaan_v2_log_tambahan.md:212](../BacktestShariah2/standard/binaan_v2_log_tambahan.md#L212)). Tujuh lajur gred dengan sel kaya kekal dalam jadual utama Posisi dan Watchlist ([H:1333](../BacktestShariah2/standard/dashboard_v2.html#L1333)), walaupun gred ialah "rekod dan uji dahulu, bukan penapis" ([tugasan_v3.md:80](../BacktestShariah2/standard/tugasan_v3.md#L80)). Jalur "Tindakan seterusnya: Pantau dalam papertrade: <3 kaedah>" sudah tidak bermakna kerana C membeli semua kaedah aktif ([H:901](../BacktestShariah2/standard/dashboard_v2.html#L901)), dan teks "Langsung · ujian terkini" memapar tarikh registry backtest (17 Okt), bukan tarikh data harian ([H:3466](../BacktestShariah2/standard/dashboard_v2.html#L3466)).

Tab Analisis tidak memapar label pantau langsung — `renderAnalisis` mempunyai sifar rujukan `pantau` — dan teks "Cara skor dikira" masih memakai takrif lama BELUM CUKUP dan n mentah ([H:3134](../BacktestShariah2/standard/dashboard_v2.html#L3134), berbanding [tugasan_v3.md:118](../BacktestShariah2/standard/tugasan_v3.md#L118)). Dokumentasi papan pula masih merujuk tugasan_v2 yang terbatal dan menerangkan struktur Prestasi yang lama ([dashboard.md:4](../BacktestShariah2/standard/dashboard.md#L4), [dashboard.md:10](../BacktestShariah2/standard/dashboard.md#L10), [dashboard.md:28](../BacktestShariah2/standard/dashboard.md#L28)).

### Dua syarat kejayaan pemilik tidak diukur ke hadapan

Matlamat pemilik jelas: untung minimum 10% sebulan dengan pegangan kira-kira sebulan, peluang menang tertinggi diutamakan, dan kaedah hanya berjaya jika mengalahkan EW semua saham Shariah ([00_NOTA_SERAHAN.md:9](../BacktestShariah2/00_NOTA_SERAHAN.md#L9), [00_NOTA_SERAHAN.md:11](../BacktestShariah2/00_NOTA_SERAHAN.md#L11)). Papan tidak mengukur mana-mana syarat ini ke hadapan.

**EW hanya wujud sebagai angka backtest**: EW 431 (21.9% setahun) dan EW 423 (32.6% setahun) dalam panel Rujukan Analisis ([H:3110](../BacktestShariah2/standard/dashboard_v2.html#L3110), [penganalisis.py:146](../BacktestShariah2/standard/penganalisis.py#L146)). Semua perbandingan hadapan — untung terkumpul, grid harian "Lawan SPY", lajur "Lebih SPY", portfolio 10 slot — memakai SPY ([H:1534](../BacktestShariah2/standard/dashboard_v2.html#L1534), [H:2441](../BacktestShariah2/standard/dashboard_v2.html#L2441), [H:2795](../BacktestShariah2/standard/dashboard_v2.html#L2795)), dan "penanda aras dalaman" skor swing ialah purata isyarat pada hari yang sama, bukan EW alam Shariah ([H:2570](../BacktestShariah2/standard/dashboard_v2.html#L2570)). Malah langkah 2 corong backtest menguji "untung lebih daripada SPY" ([H:755](../BacktestShariah2/standard/dashboard_v2.html#L755)).

**Sasaran 10% sebulan tidak muncul di mana-mana.** Perkataan "sebulan" hanya muncul pada skor sebulan Analisis, yang tertingginya +3.40% ([H:3117](../BacktestShariah2/standard/dashboard_v2.html#L3117)). Konteksnya penting: 10% sebulan bersamaan kira-kira **+214% setahun** jika dikompaun (aritmetik), sedangkan CAGR tertinggi daripada 633 varian set 431 hanya **58.15%** (kira-kira 3.9% sebulan), median peratus bulan yang portfolio naik ≥ 10% hanya 10.8%, dan hanya 27.6% varian mengalahkan EW [anggaran: kiraan penyelidik atas [registry_M_gabung.csv](../BacktestShariah2/data/registry_M_gabung.csv)]. EW 431 backtest (21.9% setahun) pula bersamaan kira-kira **1.7% sebulan** (aritmetik) — itulah palang kejayaan sebenar pemilik, dan papan tidak menunjukkannya.

Kajian portfolio projek menambah dapatan yang mengubah soalan itu sendiri. Pada peringkat portfolio 10 slot, isyarat rawak (CAGR 23.8–24.5%) tidak mengatasi EW 423 (26.3%); nilai datang daripada cara memilih saham, dan gabungan RS dengan keluar lorong 2 kekal 30.7% berbanding 17.6% bagi rawak selepas 40 pemenang dibuang ([KAJIAN_PORTFOLIO.md:34](../BacktestShariah2/kajian/KAJIAN_PORTFOLIO.md#L34), [KAJIAN_PORTFOLIO.md:79](../BacktestShariah2/kajian/KAJIAN_PORTFOLIO.md#L79)). Saiz portfolio juga tidak seragam antara dokumen: matlamat memakai 8 slot × 12.5%, jejak hadapan 10 slot, dan metrik Prestasi menganggap USD1,000 setiap posisi tanpa had ([00_NOTA_SERAHAN.md:11](../BacktestShariah2/00_NOTA_SERAHAN.md#L11), [portfolio_slot.py:1](../BacktestShariah2/standard/portfolio_slot.py#L1), [tugasan_v3.md:77](../BacktestShariah2/standard/tugasan_v3.md#L77)).

### Lampu "Data n/8" menguji tarikh, bukan kejayaan larian

Papan hanya memapar dua isyarat kesihatan: "Kemas kini terakhir", yang menjadi merah selepas 30 jam, dan butang "Data n/8", yang membandingkan tarikh lapan saluran dengan sesi dijangka tanpa kalendar cuti NYSE ([H:729](../BacktestShariah2/standard/dashboard_v2.html#L729), [H:2300](../BacktestShariah2/standard/dashboard_v2.html#L2300), [H:2313](../BacktestShariah2/standard/dashboard_v2.html#L2313)). Kedua-duanya menguji **tarikh, bukan kejayaan**. `jana_db.py` sudah menulis ralat kaedah, belian direkod/dilangkau, keluar baharu dan `gred_pada` ke `harian/status`, tetapi halaman tidak membacanya langsung ([jana_db.py:510](../BacktestShariah2/standard/jana_db.py#L510)). Pada 22 Okt nilainya ialah 730 belian dirancang, 703 direkod, 27 dilangkau, `ralat` kosong dan **`gred_pada` kosong** ([db](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)).

Banyak isyarat lain langsung tidak kelihatan: mod `MOD_ACTIONS` (masih `bayang`), keputusan larian GitHub Actions, keputusan CI `semak_data.yml` dan `sahkan.py`, 4 saham tanpa bar sesi terakhir (ATKR, BLFS, QRVO, WLYB), laporan banding bayang, dan lapisan yang dilangkau senyap seperti EDGAR tanpa rahsia `SEC_USER_AGENT` ([MOD_ACTIONS](../BacktestShariah2/MOD_ACTIONS), [data/harga/status.json](../BacktestShariah2/data/harga/status.json), [CLAUDE.md](../CLAUDE.md)). Kajian data tercemar projek sendiri merekod dua kegagalan yang lampu tarikh tidak akan tangkap — CI merah yang menggendalakan Lejar dan Analisis, dan 89 posisi palsu yang kembali "Pegang" ([KAJIAN_DATA_TERCEMAR.md:49](../BacktestShariah2/kajian/KAJIAN_DATA_TERCEMAR.md#L49)). Pengguna juga tidak dapat membezakan "lewat ikut jadual" daripada "gagal". Rutin 6:02 MYT mengemas kini posisi C ke sesi baharu setiap pagi, tetapi Lejar, Penganalisis dan portfolio kekal pada sesi sebelumnya sehingga `lejar.yml` berjalan pada 06:17 UTC (14:17 MYT) atau pada larian sandaran 10:17 UTC — jurang kira-kira 8–9 jam setiap pagi hari dagangan [anggaran daripada jadual] ([db](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e), [lejar.yml](../.github/workflows/lejar.yml)).

## Empat tab dan laman Hari Ini yang dibaca dalam 10 saat

### Satu skrin untuk memantau, butiran atas permintaan

Reka bentuk sasaran berpegang pada prinsip yang mantap. Dashboard ialah paparan sekali pandang bagi maklumat paling penting untuk satu matlamat, dan kesilapan #1 ialah melebihi satu skrin ([Few 2004](https://support.itrsgroup.com/hc/en-us/article_attachments/115004392393), [Few 2007](https://blogs.ischool.berkeley.edu/i247s13/files/2013/02/WhyMostDashboardsFail.pdf)). NN/g membezakan dashboard operasi (tugas sensitif masa) daripada dashboard analitik ([NN/g](https://www.nngroup.com/articles/dashboards-preattentive/)); empat soalan pemilik ialah tugas operasi, manakala skor, kalibrasi dan backtest ialah analitik yang patut dipisahkan. Urutan "gambaran dahulu, zum dan tapis, butiran atas permintaan" ([Shneiderman 1996](https://drum.lib.umd.edu/handle/1903/5784)) dan pendedahan berperingkat ([NN/g](https://nngroup.com/articles/progressive-disclosure/)) memberi cara memindahkan butiran tanpa membuangnya. Untuk navigasi, Material dan Apple sama-sama mengesyorkan **3–5 destinasi** ([Material](https://material.io/components/bottom-navigation), [Apple HIG](https://developer-rno.apple.com/design/human-interface-guidelines/components/navigation-and-search/tab-bars)) — lapan tab sekarang melebihi had ini.

### Empat tab, satu lampu, laman Hari Ini sebagai pintu masuk

Cadangan tunggalnya ialah empat tab yang sama di telefon (bar bawah satu baris) dan di desktop (bar atas): **Hari Ini · Kaedah · Posisi · Lagi**, ditambah **lampu sistem** dalam pengepala setiap skrin yang membuka halaman Sistem. Sistem tidak diberi tab sendiri kerana ia hanya memerlukan perhatian apabila lampu bukan hijau, mengikut reka bentuk berasaskan pengecualian. Papan sentiasa dibuka pada Hari Ini, menggantikan tingkah laku "buka tab terakhir", manakala pautan hash seperti `#kaedah` kekal berfungsi. Notifikasi telefon rutin berjadual patut memaut terus ke Hari Ini supaya mesej dan papan bercakap tentang perkara yang sama.

Laman Hari Ini mempunyai tiga blok di bawah lampu, mengikut nombor soalan pemilik. **Blok 1** menjawab "kaedah mana terbaik atau terbukti" dengan satu ayat keputusan, kemajuan bukti, tiga calon teratas daripada ranking utama berserta lencana status, dan satu baris "lawan matlamat". **Blok 2** menjawab "apa berlaku hari ini dan esok" dengan menggabungkan panel Esok dan Berubah sedia ada: jualan pada buka esok (berserta lorong dan sebab), belian pada buka esok, posisi hampir paras keluar, earnings ≤ 5 hari, dan ringkasan sesi lalu (dibeli, dilangkau, keluar); jika tiada belian, blok ini menulis "Tiada belian esok". **Blok 3** menjawab "posisi saya OK?" dengan ekuiti portfolio beku, kejatuhan semasa lawan had GANTUNG, bilangan posisi hampir paras keluar dan earnings, serta ringkasan C. Lampu menjawab soalan (4). Rupanya di telefon ditunjukkan di bawah; nombor `n` ialah ilustrasi, nombor lain dibaca daripada `PENGANALISIS.md`, `harian/status` dan `ringkas_c` pada 22 Okt, dan warna lampu ialah penilaian penyelidik.

```
┌──────────────────────────────────────────┐
│ Papan Kaedah Shariah          ● KUNING   │ ← ketik: halaman Sistem
│ Data sesi Rab 21 Okt · 2 jam lalu · bayang│
├──────────────────────────────────────────┤
│ 1  KAEDAH TERBAIK?                       │
│ Belum ada kaedah terbukti.               │
│ Cukup data: 0/75 swing · pertama ±26 Okt │
│ Calon (belum terbukti):                  │
│   M21   +3.40%/bln  ⚑ ditolak backtest   │
│   M140  +2.25%/bln  ⚑ ditolak backtest   │
│   M144  +1.72%/bln                       │
│ Matlamat 10%/bln · EW hadapan n%/bln     │
│ Dipilih daripada 134 kaedah: nasib turut │
│ menyumbang. TERBUKTI paling awal ±akhir Nov│
├──────────────────────────────────────────┤
│ 2  BUKA NY, Kha 22 Okt                   │
│ JUAL n · BELI n · hampir paras keluar n  │
│ Earnings ≤ 5 hari: n                     │
│ Sesi lalu: dibeli 703 · dilangkau 27     │
├──────────────────────────────────────────┤
│ 3  POSISI SAYA                           │
│ Portfolio beku: n% · jatuh n% (had n%)   │
│ C: 3,253 dipegang · n% sedang untung     │
├──────────────────────────────────────────┤
│  Hari Ini │ Kaedah │ Posisi │ Lagi       │
└──────────────────────────────────────────┘
```

Di desktop, blok yang sama disusun dalam grid 2 × 2 di atas lipatan: Kaedah di atas kiri (kedudukan paling penting), Esok di atas kanan, Posisi di bawah kiri, dan carta kecil Lawan matlamat (portfolio beku lawan EW, SPY dan garis 10%) di bawah kanan. Tiada tab sisi dan tiada butang Lipat semua atau Buka semua, kerana halaman yang pendek tidak memerlukan alat untuk memendekkannya.

**Tab Kaedah** menggabungkan Analisis, bahagian "setiap kaedah" dalam Prestasi, Backtest Keputusan dan tab Kaedah ke dalam tiga lapisan. Di atas terletak panel "Lawan matlamat" — portfolio beku dan kawalannya lawan EW, SPY dan 10% sebulan, serta tangga tarikh bukti — diikuti "3 penemuan utama" automatik daripada `penganalisis.py`. Di tengah terletak **satu jadual ranking**: di telefon tiga lajur (kaedah dengan lencana status, skor sebulan dengan julat, bar kemajuan bukti), dan di desktop lapan hingga sembilan lajur dengan tambahan lebihan atas EW, kadar menang matang dengan batas bawah Wilson, jangkaan backtest dipotong, semakan luar sampel x/3, lorong pra-komit dan latar backtest (GUNA hingga DITOLAK), berserta penapis Swing/Semua dan "Bermasalah" (pantau). Ketik mana-mana baris untuk membuka **Profil kaedah**, satu halaman yang menggantikan helaian Analisis, `openKaedah`, `openDetail` dan semua panel setiap kaedah dalam Prestasi. Profil itu memapar hadapan lawan jalur jangkaan backtest, taburan hasil sebagai dotplot 20 titik, untung bulanan lawan 10%, perbandingan dua lorong dan sebab keluar, diagnostik skor v2, rekod backtest (corong 7 langkah, pingat, S1–S4, WFO, AUTOTUNE), serta peraturan kaedah dan posisi terbukanya.

**Tab Posisi** dibuka dengan portfolio beku 10 slot — paling banyak 10 baris dengan % sejak beli, jarak ke paras keluar, hari dipegang dan earnings — kemudian "Papertrade semua isyarat (C)" sebagai ringkasan ikut status dan kaedah. Jadual penuh 4,000+ baris hanya dimuat apabila diminta; lalainya "Dipegang", disusun **ikut risiko** (paling hampir paras keluar dahulu), dengan dua pandangan (Ringkas dan Risiko) dan gred dipapar dalam helaian posisi. **Tab Lagi** menyimpan semua yang bersifat analitik atau arkib: Sistem penuh; Backtest (podium, corong, jadual penuh, data mentah S1–S4/2000 AS, dengan indikator I tersembunyi secara lalai); Analisis dagangan C (kalendar, MFE, R, grid harian, neraca, sebab keluar agregat); Eksperimen (dua lorong agregat, gred A–E, ujian ramalan skor); Konteks pasaran yang menggantikan tab Sektor; Arkib Moomoo lama; dan Panduan.

### Setiap tab dan panel: kekal, gabung, pindah atau buang

Lajur terakhir merujuk kepada keputusan pemilik dalam bahagian seterusnya (D1–D9).

| Tab asal | Panel atau elemen | Tindakan | Destinasi baharu | Keputusan |
|---|---|---|---|---|
| Global | Lapan tab, subbar, tab sisi, Lipat/Buka semua | GANTI | Empat tab; tiada tab sisi | D7 |
| Global | "Kemas kini terakhir" dan butang Data n/8 | GABUNG | Lampu sistem 7 semakan dalam pengepala | – |
| Global | Teks "Langsung · ujian terkini" | BUANG | Umur data dalam lampu | – |
| Global | Buka tab terakhir (`pbs3_tab`) | UBAH | Sentiasa buka Hari Ini | – |
| Global | Panduan dan 162 istilah TIPS | KEKAL, pangkas | Lagi › Panduan; istilah yang masih dipapar sahaja | – |
| Global | Tajuk "Papan Backtest Shariah" | UBAH | "Papan Kaedah Shariah" | – |
| Ringkasan | Tajuk ringkas, 3 perkara utama | GABUNG | Ayat jawapan blok 1–3 | – |
| Ringkasan | Jalur status 8 cip | GABUNG | Lampu sistem | – |
| Ringkasan | 4 KPI (termasuk USD1,000) | GABUNG | Blok 3, % sahaja | D1 |
| Ringkasan | Esok | KEKAL (teras) | Blok 2, dibaca daripada dokumen pra-kira | – |
| Ringkasan | Berubah sejak sesi lalu | GABUNG | Blok 2, baris "Sesi lalu" | – |
| Ringkasan | Terbaik ikut papertrade | BERSARA | Blok 1 (ranking utama) | D1 |
| Ringkasan | Untung lawan risiko | BUANG | Pendua Prestasi; kuadran label §7 | D1 |
| Ringkasan | Terbaik ikut backtest (podium RM) | PINDAH | Lagi › Backtest; satu baris dalam Profil | – |
| Ringkasan | Eksperimen: portfolio 10 slot | NAIK TARAF | Kaedah › Lawan matlamat; ringkasan dalam blok 1 dan 3 | D5 |
| Ringkasan | Eksperimen: dua lorong, gred | PINDAH | Lagi › Eksperimen; lorong setiap kaedah dalam Profil | – |
| Ringkasan | Cara baca, kaki Moomoo | PINDAH | Panduan; Arkib | D6 |
| Analisis | Tajuk dan 4 KPI (tersembunyi secara lalai) | GABUNG | Baris status di atas jadual Kaedah | – |
| Analisis | 3 penemuan utama | KEKAL | Kaedah, di bawah Lawan matlamat | – |
| Analisis | Kedudukan kaedah | KEKAL, naik taraf | Ranking tunggal tab Kaedah | D4 |
| Analisis | Helaian baris (`openAnl`) | GABUNG | Profil kaedah | – |
| Analisis | Rujukan (EW/SPY backtest, portfolio) | GABUNG | Lawan matlamat | – |
| Analisis | Cara skor dikira | PINDAH, betulkan | Panduan, teks ikut tugasan_v3:118–122 | – |
| Prestasi | Sub-tab akaun C / Moomoo lama / Gabung | BUANG | C sahaja; Moomoo ke Arkib; Gabung dibuang | D6 |
| Prestasi | Gambaran: tajuk dan 7 KPI | BUANG | Pendua; angka ke blok 3 | – |
| Prestasi | Aliran isyarat (Sankey) | BUANG | Kiraan isyarat → dibeli → dilangkau dalam Sistem | – |
| Prestasi | Neraca untung & rugi; Sebab keluar | PINDAH | Profil (setiap kaedah); agregat ke Lagi › Analisis dagangan | – |
| Prestasi | Untung terkumpul lawan SPY; Kejatuhan dari puncak | GANTI | Lawan matlamat (EW, SPY, 10%, had GANTUNG) | D4, D5 |
| Prestasi | Kalendar harian, MFE, unit risiko R, grid prestasi harian | PINDAH | Lagi › Analisis dagangan C | – |
| Prestasi | Taburan untung; plot kotak | GABUNG | Dotplot 20 titik dalam Profil | – |
| Prestasi | Skor kaedah swing (jadual 35 lajur, gabungan cadangan) | TURUN | Diagnostik dalam Profil, dikira atas Lejar matang | D2 |
| Prestasi | Strip gabungan beku | PINDAH | Lawan matlamat, dilabel SEMENTARA | D3 |
| Prestasi | Ujian ramalan skor; diagnostik skor | PINDAH | Lagi › Eksperimen | D2 |
| Prestasi | Tapisan minimum dagangan | BUANG | Diganti pintu status | – |
| Prestasi | Untung lawan risiko; bar untung purata; bar kadar menang; Terbaik ikut % untung | BUANG | Lajur dalam jadual Kaedah | D1 |
| Prestasi | Kedudukan kaedah · Skor U×S | BERSARA | Rekod sejarah dalam Lagi | D1 |
| Prestasi | Untung bergerak lawan backtest | PINDAH | Profil (jalur jangkaan); amaran melalui pantau | – |
| Prestasi | Untung bulanan setiap kaedah | PINDAH | Profil (lawan 10%); peta haba agregat ke Lagi | – |
| Prestasi | Paling Teruk | GABUNG | Penapis "Bermasalah" (pantau) dalam jadual Kaedah | – |
| Prestasi | Banding dua lorong | GABUNG | Lajur Lorong dan Profil; agregat ke Lagi › Eksperimen | – |
| Prestasi | Prestasi ikut gred | PINDAH | Lagi › Eksperimen | – |
| Posisi | 4 KPI; peta portfolio | GABUNG | Ringkasan atas tab Posisi; peta untuk portfolio beku (dilipat) | – |
| Posisi | Posisi & keputusan (4 pandangan) | KEKAL, ubah lalai | Dipegang, susun ikut risiko; Ringkas dan Risiko; dimuat atas permintaan | D5 |
| Posisi | 7 lajur gred | PINDAH | Helaian posisi (data kekal) | D7 |
| Posisi | Isyarat tidak dibeli | PINDAH | Sistem (rekod audit "kalau tak beli, cakap tak beli") | – |
| Posisi | Helaian posisi | KEKAL | – | – |
| Watchlist | Hampir Signal dan KPI | PINDAH | Hari Ini › butiran Esok, bahagian "Hampir isyarat" | – |
| Watchlist | Isyarat lengkap dalam watchlist | GABUNG | Blok 2, "Beli pada buka" | – |
| Backtest | Keputusan (podium, corong 7 langkah, Semua kaedah) | PINDAH | Lagi › Backtest; status corong satu baris dalam Profil | – |
| Backtest | Butiran (431/S1–S4/2000 AS × Papan penuh, Carta & gaya, Banding, AUTOTUNE) | PINDAH | Lagi › Backtest mentah, dimuat atas permintaan; indikator I tersembunyi | – |
| Backtest | Jalur "Tindakan seterusnya" | BUANG | – | – |
| Backtest | Helaian varian (`openDetail`) | GABUNG | Profil › Backtest | – |
| Kaedah | Jadual Semua kaedah; KPI teks tetap | GABUNG / BUANG | Carian dalam jadual Kaedah; KPI teks dibuang | – |
| Kaedah | Helaian `openKaedah` | GABUNG | Profil › Cara kaedah berfungsi | – |
| Sektor | Peta haba, ranking, 10 industri terkuat, aliran institusi | PINDAH, ringkaskan | Lagi › Konteks pasaran, dengan tarikh SST | – |
| Sektor | Fasa rotasi, KPI dan lajur Fasa, skor panas | BUANG | Diganti gred kumpulan v2 (Weinstein, sudah disahkan) | – |

## Satu ranking: skor sebulan Penganalisis, diukur lawan EW

### Skor sebulan Penganalisis paling boleh dipertahankan

Ranking utama yang dicadangkan ialah **skor sebulan Papan Penganalisis**, dengan status dan label pantau sebagai pintu. Hanya ranking ini yang serentak memakai asas adil — Lejar Penuh membeli semua isyarat tanpa had atau keutamaan dan boleh dihasilkan semula tanpa LLM ([tugasan_v3.md:92](../BacktestShariah2/standard/tugasan_v3.md#L92)) — posisi matang sahaja untuk mengelak bias keluar awal ([H:3355](../BacktestShariah2/standard/dashboard_v2.html#L3355)), n berkesan ikut hari beli, dan pengecutan ke jangkaan backtest khusus setiap kaedah ([tugasan_v3.md:113](../BacktestShariah2/standard/tugasan_v3.md#L113)). Cara ini selari dengan amalan menyusun ikut anggaran konservatif dan bukan purata mentah, yang menghalang item dengan sedikit data daripada melonjak ke atas ([Evan Miller](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html)), dan dengan produk yang mempermudah penarafan kepada satu skor yang diterangkan ([Darwinex D-Score](https://help.darwinex.com/d-score)).

Dua pembaikan diperlukan sebelum ranking ini dipapar sebagai jawapan utama. Kaedah yang DITOLAK dalam backtest mesti diberi bendera yang kelihatan (⚑), kerana hari ini #1 dan #2 (M21, M140) kedua-duanya DITOLAK. Selepas EW hadapan wujud, skor pula dikira atas **lebihan atas EW**, bukan pulangan mutlak, supaya ranking mengukur syarat kejayaan pemilik. Kemudian, potongan backtest khusus kaedah gaya Harvey–Liu (item 16 laporan skor) patut menggantikan pemalar "25% + 25% setiap semakan lulus", yang memberi pengekalan median kira-kira 26% secara seragam kepada semua kaedah ([Skor KPI pemilihan kaedah swing.md:44](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L44), [Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)).

Skor lain diturunkan atau dibersarakan. Skor kaedah swing v2 menjadi **diagnostik** dalam Profil kaedah: sub-skornya (CVaR, MAE/ATR, Wilson hari beli, P(4 teratas) Monte Carlo, korelasi pasangan) kekal, tetapi dikira semula atas Lejar matang dengan lorong yang dipra-komit, bukan atas C "awal" dengan lorong terbaik yang dipilih selepas melihat data ([Skor KPI pemilihan kaedah swing.md:46](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L46)). Label §7 TERUSKAN/PERHATI/HENTIKAN dengan skor U×S, "Terbaik ikut % untung" dan podium backtest di laman utama **dibersarakan sebagai alat pemilihan**, dengan nilai sejarahnya disimpan dalam Lagi. Status backtest (GUNA, UJI KERTAS, SIMPAN, DITOLAK) menjadi atribut "latar backtest" dalam jadual dan Profil, bukan keadaan hadapan.

### Lima keadaan menggantikan sembilan kosa kata

| Keadaan baharu | Maksud mudah | Syarat | Menggantikan |
|---|---|---|---|
| BELUM CUKUP | "Terlalu awal; cukup ±<tarikh>" dengan bar kemajuan | < 20 posisi matang atau < 10 hari beli berbeza (sama dengan Penganalisis kini) | BELUM CUKUP DATA, BELUM CUKUP, Belum layak, Calon (awal), keyakinan rendah, "Terlalu awal hingga" |
| MENJANJIKAN | "Nampak baik, belum pasti" | Cukup data; anggaran lebihan atas EW > 0 tetapi julat 95% merentas sifar | PERHATI (dua makna), Calon |
| TERBUKTI | "Mengalahkan EW dengan yakin" | ≥ 20 hari beli matang; julat 95% lebihan atas EW > 0 dengan nilai kritikal dilaras kelompok; tiada brek pantau | TERUSKAN, KUAT, Teras |
| LEMAH | "Tidak mengalahkan EW" | Cukup data; julat 95% lebihan di bawah sifar | HENTIKAN, LEMAH |
| DIGANTUNG atau BERSARA | "Brek dipicu" | Peraturan pantau `penganalisis.py` ([penganalisis.py:24](../BacktestShariah2/standard/penganalisis.py#L24)) | Gantung/Bersara, ⚠ AMARAN Paling Teruk, "di bawah julat" |
| Lencana AMARAN | "Perhatikan" | Satu amaran CUSUM | AMARAN pantau; AMARAN t < −2 dibuang |

Sehingga EW hadapan wujud, MENJANJIKAN, TERBUKTI dan LEMAH dikira lawan sifar dengan nota "belum lawan EW". Keadaan TERBUKTI ditahan sehingga sekurang-kurangnya 20 hari beli matang, sama seperti Morningstar yang tidak memberi bintang kepada dana di bawah 3 tahun dan Darwinex yang memberi skor Experience penuh hanya selepas 12 D-Period ([Morningstar melalui ICMA-RC](https://www.icmarc.org/x3150.xml), [Darwinex](https://help.darwinex.com/experience-attribute)).

### Sembilan keputusan yang perlu dibuat pemilik

Enam keputusan di bawah menterbalikkan keputusan atau permintaan terdahulu (D1–D4, D6, D7), manakala tiga lagi ialah keputusan baharu (D5, D8, D9).

| # | Keputusan | Keputusan atau permintaan terdahulu yang terjejas | Cadangan |
|---|---|---|---|
| D1 | Bersarakan label TERUSKAN/PERHATI/HENTIKAN, Skor U×S, "Terbaik ikut % untung" dan metrik USD1,000 | tugasan_v3 §7, keputusan pemilik 14 Okt ([tugasan_v3.md:76](../BacktestShariah2/standard/tugasan_v3.md#L76)); versi 95 mengekalkan label | Ya; sejarah disimpan dalam Lagi; §7 ditulis semula |
| D2 | Turunkan Skor kaedah swing v2 menjadi diagnostik | Permintaan versi 96–97; Fasa 1–4 laporan skor (versi 98–102) ([dashboard.md:3](../BacktestShariah2/standard/dashboard.md#L3)) | Ya; dikira semula atas Lejar matang dengan lorong pra-komit |
| D3 | Labelkan gabungan beku sebagai SEMENTARA dan bekukan semula pada akhir Nov | [CLAUDE.md](../CLAUDE.md): `gabungan_beku.json` "jangan ubah tanpa keputusan pengguna" | Fail kekal beku sekarang; dibekukan semula ikut ranking utama |
| D4 | TERBUKTI bermaksud lebihan atas EW > 0; pilih universe EW | Peraturan Papan Penganalisis, 20 dan 22 Okt ([tugasan_v3.md:109](../BacktestShariah2/standard/tugasan_v3.md#L109)) | Ya; universe set 431 dahulu |
| D5 | "Posisi saya" bermaksud portfolio beku 10 slot; tetapkan saiz 8 atau 10 slot | Tiada keputusan terdahulu; matlamat menyebut 8 slot | Portfolio beku sebagai lalai; selaraskan saiz |
| D6 | Arkibkan Moomoo lama; buang pilihan "Gabung" | Versi 73: Moomoo digabung sebagai pilihan akaun ([binaan_v2_log_tambahan.md:163](../BacktestShariah2/standard/binaan_v2_log_tambahan.md#L163)) | Ya |
| D7 | Buang tab sisi; pindahkan lajur gred ke helaian | Permintaan versi 93; lajur gred versi 34 (15 Okt) dan gred kewangan (20 Okt) | Ya; data gred kekal dalam helaian |
| D8 | Tukar `MOD_ACTIONS` ke `rasmi` | Keputusan peralihan 17 Okt dengan mod selari 3 hari ([tugasan_v3.md:97](../BacktestShariah2/standard/tugasan_v3.md#L97)) | Bukti 19–21 Okt kini direkod ([PERALIHAN.md:34](../BacktestShariah2/jadual/PERALIHAN.md#L34)); menunggu persetujuan pemilik |
| D9 | Sasaran 10% sebulan: kekal sebagai sasaran, atau jadi garis aspirasi | Matlamat dalam [00_NOTA_SERAHAN.md:9](../BacktestShariah2/00_NOTA_SERAHAN.md#L9) | Papan memapar jurangnya; keputusan pada pemilik |

Untuk D3, cadangannya ialah **jangan ubah fail beku sekarang**, tetapi labelkan ia di papan sebagai "SEMENTARA: dipilih atas data C yang belum matang; bercanggah dengan ranking utama", kemudian bekukan semula pada akhir Nov 2026 apabila ≥ 20 hari beli matang sudah tersedia, mengikut protokol laporan skor ([Skor KPI pemilihan kaedah swing.md:3](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L3), [Skor KPI pemilihan kaedah swing.md:81](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L81)).

## Lima naik taraf menutup jurang matlamat dan titik buta

### EW hadapan menjadi garis kejayaan, menggantikan SPY

Naik taraf paling penting ialah indeks **EW hadapan**: pulangan harian sama berat bagi universe set 431, dikira oleh Actions daripada stor harga yang sudah merangkumi set itu ([tugasan_v3.md:67](../BacktestShariah2/standard/tugasan_v3.md#L67)). Indeks berterusan sejak 8 Okt (mula C) dan 16 Okt (mula Lejar) dipakai untuk membanding portfolio beku. Bagi setiap posisi Lejar pula, pulangan EW dikira bagi tempoh pegangan yang sama — dari buka hari beli hingga hari keluar atau hari ini — supaya setiap posisi mempunyai "lebihan atas EW" yang padan masa. Penganalisis kemudian mengira skor, julat dan status atas lebihan ini, dan SPY menjadi rujukan sekunder. Universe EW yang tepat ialah keputusan pemilik (D4): set 431 tersedia hari ini dan setanding dengan EW backtest 21.9%, manakala "semua saham Shariah" dalam saringan Moomoo jauh lebih besar dan belum ada dalam stor. Cadangannya: mula dengan 431, dan semak semula selepas universe Shariah mingguan stabil.

### Penjejak matlamat menunjukkan jarak ke 10% sebulan secara jujur

Panel Lawan matlamat merangkumi setiap portfolio beku (GABUNGAN_10, TOP1_10, RS_10) dan kawalannya (RAWAK_KAEDAH_10, RAWAK_10). Bagi setiap satu, panel ini memapar pulangan setiap bulan (21 sesi) sebagai bar lawan garis 10%, keluk terkumpul lawan EW hadapan dan SPY, kejatuhan semasa lawan had GANTUNG iaitu 1.5 × kejatuhan maksimum backtest ([penganalisis.py:24](../BacktestShariah2/standard/penganalisis.py#L24)), kadar menang matang dengan batas bawah Wilson kerana pemilik mengutamakan peluang menang, dan "bulan berlalu x/6". Ayat ringkasnya jujur tentang jarak: "Sasaran 10% sebulan. Tertinggi dalam backtest: kira-kira 3.9% sebulan. Palang EW backtest: kira-kira 1.7% sebulan." Papan tidak menukar sasaran — itu keputusan matlamat pemilik (D9) — tetapi menjadikan jurang itu kelihatan setiap hari, supaya keputusan wang sebenar tidak dibuat atas sasaran yang belum pernah dicapai, walaupun dalam sampel. Sebelum GABUNGAN_10 wujud, panel memapar RS_10 lawan RAWAK_10 sahaja dengan nota "terlalu awal"; dalam 3 sesi pertama, RS_10 −5.06% dan RAWAK_10 +2.43% ([portfolio_slot/RINGKASAN.md:5](../BacktestShariah2/portfolio_slot/RINGKASAN.md#L5)).

### Lampu status menggulung tujuh semakan berasaskan simptom

Lampu tunggal mengambil keadaan **paling teruk** daripada tujuh semakan, seperti Statuspage ([Atlassian](https://support.atlassian.com/statuspage/docs/what-is-a-component)), dan setiap komponen mempunyai ambang amaran dan ralat gaya dbt ([dbt](https://docs.getdbt.com/reference/commands/freshness)). Umur data dikira dalam pelayar daripada cap masa db, bukan daripada teks yang ditulis semasa jana, untuk mengelak perangkap Power BI — muat semula yang gagal meninggalkan cap masa lama tanpa amaran ([Microsoft Learn](https://learn.microsoft.com/power-bi/consumer/end-user-fresh)). Keadaan keempat, **"menunggu jadual"** (kelabu, bukan kuning), membezakan ketinggalan normal Lejar sebelum 06:17 UTC daripada kegagalan sebenar, dan mod (`bayang` atau `rasmi`) dipapar sebagai pil di sebelah lampu.

| # | Semakan | Sumber | Hijau | Kuning | Merah | Dipapar kini? |
|---|---|---|---|---|---|---|
| 1 | Harga segar | `data/harga/status.json` | Sesi = sesi NYSE terakhir; saham tanpa bar ≤ 1% (kini 4 daripada 931) | Lewat 1 sesi atau tanpa bar > 1% | Lewat ≥ 2 sesi atau `tiada_data` tidak kosong | Separa (tarikh sahaja) |
| 2 | Kerja harian C | `harian/status` | Sesi tutup = sesi dijangka; `ralat` kosong; belian selepas 9:45 NY | `gred_pada` kosong; dilangkau > 5% dirancang [ambang cadangan] | `ralat` tidak kosong; tiada belian pada hari dagangan | Medan ada, tidak dibaca |
| 3 | Rantai Lejar → Penganalisis → portfolio | `lejar/status.json`, `papan.json`, `portfolio_slot/status.json` | Ketiga-tiga = sesi harga; ralat larian terakhir kosong | Satu output ketinggalan selepas masa dijangka | Ketinggalan ≥ 2 sesi atau ada ralat | Separa |
| 4 | Integriti CI | Larian terakhir `semak_data.yml` pada `main` (ujian unit dan `sahkan.py`) | Lulus | – | Gagal | Tiada; perlu sumber baharu |
| 5 | Ketekalan | `bayang/BANDING_*` sebelum rasmi; C lawan Lejar selepas rasmi | ≥ 99% keluar sama | 95–99% [ambang cadangan] | < 95% | Tiada |
| 6 | Skema output | Medan wajib versi papan (pantau dalam `papan.json`, `beku` dalam portfolio) | Lengkap | Medan tiada | – | Tiada |
| 7 | Lapisan dilangkau senyap | EDGAR tanpa rahsia, SST basi, `faktor_calon` belum sah, langkah `continue-on-error` | Tiada | ≥ 1 lapisan dilangkau | – | Tiada |

Jika lampu ini dibina hari ini, warnanya **kuning** [penilaian penyelidik], kerana `gred_pada` kosong, `papan.json` tiada medan pantau, portfolio 10 slot masih pada sesi 20 Okt, dan EDGAR serta SST dilangkau — tiga daripada empat sebab ini tidak ditangkap butang "Data n/8" sekarang. Semakan 1–3 boleh dibina dalam Fasa 1 kerana medannya sudah ada. Semakan 4–7 memerlukan satu dokumen db baharu (cadangan: `sistem/status`) yang ditulis oleh langkah Actions, kerana halaman tidak dapat memanggil API GitHub sendiri; calon penulis terbaik ialah `penjaga_jadual.py`, yang sudah memantau 9 workflow ([penjaga_jadual.py:1](../BacktestShariah2/standard/penjaga_jadual.py#L1)).

### Keadaan "terlalu awal" diberi bar kemajuan dan tarikh

Optimizely tidak memapar "tiada keputusan"; ia memapar "more visitors needed" bersama anggaran masa menunggu ([Optimizely](https://support.optimizely.com/hc/en-us/articles/4410284017421)). Papan patut berbuat sama pada dua peringkat: bagi setiap kaedah, contohnya "7/10 hari beli · 12/20 matang · cukup ±26 Okt", dan bagi keseluruhan projek, satu tangga tarikh dalam panel Lawan matlamat seperti di bawah.

| Tarikh | Peristiwa | Sumber |
|---|---|---|
| 26 Okt 2026 | Kaedah pertama mencapai 20 posisi matang; status pertama selain BELUM CUKUP menjadi mungkin | [PENGANALISIS.md:8](../BacktestShariah2/laporan/PENGANALISIS.md#L8) |
| ±akhir Nov 2026 | ≥ 20 hari beli matang; TERBUKTI paling awal; gabungan dibekukan semula | [Skor KPI pemilihan kaedah swing.md:81](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L81) |
| 15 Jan 2027 | Penilaian Lejar pertama | [lejar/RINGKASAN.md:5](../BacktestShariah2/lejar/RINGKASAN.md#L5) |
| ±Apr–Jun 2027 | 6 bulan inkubasi dengan 40–60 hari beli; keputusan wang sebenar paling awal | [Skor KPI pemilihan kaedah swing.md:3](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L3), [portfolio_slot/RINGKASAN.md:42](../BacktestShariah2/portfolio_slot/RINGKASAN.md#L42) |

Cara memapar ketidakpastian juga penting. Julat ditulis sebagai angka dalam ayat, contohnya "+1.8%, kemungkinan sebenar −0.4% hingga +3.9%" (ilustrasi), bersama garis julat mendatar dan bukan carta bar dengan bar ralat yang kerap disalah baca ([Correll & Gleicher](https://pmc.ncbi.nlm.nih.gov/articles/PMC6214189)). Dalam Profil, dotplot 20 titik ("4 daripada 20 hasil di bawah sifar") membantu bukan pakar membuat keputusan lebih baik berbanding paparan ketumpatan ([Fernandes et al. CHI 2018](https://mucollective.northwestern.edu/project/uncertainty-bus)), dan menyatakan ketidakpastian dengan angka hanya menjejaskan kepercayaan sedikit, kurang daripada penyataan verbal ([van der Bles et al. 2020](https://research.rug.nl/en/publications/the-effects-of-communicating-uncertainty-on-public-trust-in-facts/)).

### Setiap "terbaik" membawa kiraan cubaan dan amaran nasib

Memilih yang terbaik daripada 134 kaedah ialah satu ujian berganda. Kajian 888 algoritma Quantopian mendapati Sharpe backtest hampir tidak meramal prestasi luar sampel (R² < 0.025), dan jurangnya membesar apabila lebih banyak backtest dibuat ([Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/)); potongan Harvey–Liu paling berat menghukum strategi yang marginal ([Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)), dan Deflated Sharpe Ratio menaikkan palang mengikut bilangan cubaan ([Bailey & López de Prado](https://papers.ssrn.com/abstract=2460551)). Dalam projek ini, kaedah teratas daripada 123 dijangka mencapai t ≈ 2.6 melalui nasib semata-mata, dan dengan 10 hari beli nilai kritikal patut 2.262, bukan 1.96 ([Skor KPI pemilihan kaedah swing.md:46](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L46), [Skor KPI pemilihan kaedah swing.md:38](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L38)). Bilangan cubaan berkesan juga lebih kecil daripada bilangan kaedah, kerana 59% posisi Lejar berada dalam kluster ≥ 5 kaedah dan 62% dibeli pada satu hari ([KAJIAN_DATA_TERCEMAR.md:51](../BacktestShariah2/kajian/KAJIAN_DATA_TERCEMAR.md#L51)).

Oleh itu papan patut memapar satu baris tetap di sebelah setiap "terbaik": "Dipilih daripada 134 kaedah. Yang teratas daripada sebanyak ini kelihatan baik sebahagiannya kerana nasib. TERBUKTI hanya selepas ≥ 20 hari beli matang." Papan juga patut memapar kiraan kaedah DIGANTUNG dan BERSARA berserta pautan, supaya senarai terbaik tidak hanya menunjukkan kaedah yang terselamat, dan membuang AMARAN t < −2 yang memberi kira-kira 2.8 amaran palsu setiap semakan atas 123 kaedah ([Skor KPI pemilihan kaedah swing.md:85](Skor%20KPI%20pemilihan%20kaedah%20swing.md#L85)).

### Laman utama dimuat daripada ringkasan pra-kira

Muatan dipecahkan ikut tab. Satu dokumen pra-kira baharu (cadangan: `harian/hari_ini`) ditulis oleh `harian_c.py` atau `jana_db.py`, mengandungi senarai jual dan beli esok, posisi hampir paras keluar, earnings, kiraan sesi lalu dan ringkasan posisi, supaya Hari Ini tidak perlu lagi memuat 1.4 MiB posisi C untuk mengira `statusPos` dalam pelayar ([H:2237](../BacktestShariah2/standard/dashboard_v2.html#L2237)). Laman utama kemudian hanya memerlukan `harian/status`, `hari_ini`, `analisis/papan` (119.5 KiB) dan `prestasi/portfolio_slot` (5.9 KiB) — kira-kira 0.2–0.3 MiB, lebih kurang 6% muatan kini [anggaran]. Registry dan autotune (1.5 MiB) dimuat hanya untuk Profil kaedah dan Lagi › Backtest, posisi C penuh hanya untuk jadual Posisi, data sektor hanya untuk Konteks pasaran, dan Moomoo lama hanya untuk Arkib. "Belian esok" patut dibaca terus daripada sumber belian sebenar, bukan diterbitkan semula daripada watchlist, kerana kedua-dua sumber itu boleh berbeza ([H:2321](../BacktestShariah2/standard/dashboard_v2.html#L2321)).

## Baiki saluran data dahulu, kemudian bina dalam empat fasa

Urutan kerja disusun ikut nilai lawan usaha, dengan satu syarat keras: papan baharu yang lebih jelas tetapi atas data yang salah lebih berbahaya daripada papan lama yang padat. Oleh itu Fasa 0 membaiki saluran data dahulu.

| Isu Fasa 0 | Bukti | Tindakan |
|---|---|---|
| P0.1 `papan.json` tiada medan pantau; lajur Pantau versi 101–102 kosong | Dibina 21 Okt 23:15 MYT, sebelum commit pantau `326493c` (22 Okt 06:58 UTC). Pada 07:42 UTC, 134 daripada 134 baris masih tiada `pantau`, dan belum ada commit Penganalisis selepas Lejar sesi 21 Okt ([papan.json](../BacktestShariah2/data/analisis/papan.json)) | Pastikan `analisis.yml` siap selepas Lejar; tambah semakan skema (lampu #6) |
| P0.2 Portfolio 10 slot tidak maju | Commit Lejar sesi 21 Okt (`42faa89`, 07:25 UTC) tidak menyentuh `portfolio_slot/`; `status.json` kekal 20 Okt dengan RS_10 dan RAWAK_10 sahaja; langkah ini berjalan dengan `continue-on-error: true` ([lejar.yml:45](../.github/workflows/lejar.yml#L45), [portfolio_slot/status.json](../BacktestShariah2/portfolio_slot/status.json)) [semakan penyelidik; log Actions belum dibaca] | Baca log larian; tulis ralat ke fail status supaya kegagalan kelihatan (lampu #3 dan #7); mungkin berkait dengan P0.1 |
| P0.3 Ketinggalan satu sesi tanpa label | Pagi 22 Okt, `analisis/papan` dan portfolio pada sesi 20 Okt, manakala `ringkas_c` pada 21 Okt ([db](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)); Lejar mencapai 21 Okt hanya pada 15:25 MYT ([lejar/status.json](../BacktestShariah2/lejar/status.json)) | Papar "menunggu jadual" dengan masa dijangka; tidak dikira sebagai kegagalan |
| P0.4 `gred_pada` kosong | `harian/status` versi 34 ([db](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)) | Semak langkah gred harian |
| P0.5 `MOD_ACTIONS` masih `bayang` | Fail [MOD_ACTIONS](../BacktestShariah2/MOD_ACTIONS); mod selari dirancang 3 hari dagangan sejak 17 Okt ([tugasan_v3.md:97](../BacktestShariah2/standard/tugasan_v3.md#L97)) | Keputusan D8; papar mod dalam pengepala |
| P0.6 EDGAR dilangkau senyap | Rahsia `SEC_USER_AGENT` belum ditetapkan ([CLAUDE.md](../CLAUDE.md)) | Tetapkan rahsia; lampu #7 |
| P0.7 SST basi sejak 19 Okt | [binaan_v2_log_tambahan.md:212](../BacktestShariah2/standard/binaan_v2_log_tambahan.md#L212) | Tanda tarikh pada Konteks pasaran |
| P0.8 Dokumen bercanggah | dashboard.md merujuk tugasan_v2 dan struktur lama ([dashboard.md:4](../BacktestShariah2/standard/dashboard.md#L4), [dashboard.md:28](../BacktestShariah2/standard/dashboard.md#L28)); tugasan_v3 §7 masih memakai USD, bercanggah dengan versi 95 ([tugasan_v3.md:77](../BacktestShariah2/standard/tugasan_v3.md#L77)); BANDING_C menyebut "had 10 sekaedah", bercanggah dengan "tiada had slot" ([BANDING_C.md:3](../BacktestShariah2/lejar/BANDING_C.md#L3), [tugasan_v3.md:41](../BacktestShariah2/standard/tugasan_v3.md#L41)); teks formula Analisis lapuk ([H:3134](../BacktestShariah2/standard/dashboard_v2.html#L3134)); log binaan tidak merekod versi 87–102 | Kemas kini sebelum Fasa 1 supaya spesifikasi baharu bermula bersih |
| P0.9 47 kaedah K145+ tiada watchlist | Kaedah M115–M161 tiada `hampir()` ([tugasan_v3.md:23](../BacktestShariah2/standard/tugasan_v3.md#L23)) | Papar sebagai had yang diketahui dalam butiran Esok |

| Fasa | Kerja | Nilai | Usaha [anggaran] | Prasyarat |
|---|---|---|---|---|
| 0 | Baiki P0.1–P0.9 | Tinggi: papan baharu bergantung padanya | Rendah | – |
| 1 (versi 103) | Laman Hari Ini 3 blok dengan lampu (semakan 1–3 dan medan `harian/status`); 4 tab, dengan tab lama sementara di bawah Lagi supaya tiada yang hilang; sentiasa buka Hari Ini; buang pendua (KPI ×2, scatter ×2, status ×2, podium di laman utama), USD dan RM; bendera DITOLAK; baris amaran ujian berganda; pil mod | Sangat tinggi: menjawab empat soalan | Rendah–sederhana (HTML sahaja) | Fasa 0 |
| 2 | Saluran data: indeks EW hadapan dan lebihan padan masa (`lejar.py`, `penganalisis.py`); lima keadaan bersatu; bar kemajuan dan tarikh; dokumen `sistem/status` (semakan 4–7) dan `harian/hari_ini`; muat ikut tab | Tinggi: mengukur syarat kejayaan | Sederhana (Python dan Actions) | D1, D4 |
| 3 | Tab Kaedah dengan Profil kaedah (gabungan Analisis, Prestasi setiap kaedah, Backtest Keputusan, Kaedah); skor v2 sebagai diagnostik atas Lejar matang; panel Lawan matlamat; Posisi ikut risiko dengan portfolio beku; Watchlist ke butiran Esok | Tinggi | Sederhana–tinggi | D2, D3, D5; GABUNGAN_10 wujud |
| 4 | Lagi: Backtest mentah atas permintaan, Konteks pasaran (gred kumpulan v2, tanpa fasa), Arkib Moomoo, Analisis dagangan C, Eksperimen; pangkas TIPS; tulis semula dashboard.md dan tugasan_v3 §7; tukar nama papan | Sederhana | Rendah | D6, D7 |

Setiap fasa ialah satu versi papan dengan pratonton untuk pemilik, seperti amalan versi 89 dan 91. Lima permintaan eksplisit pemilik dikekalkan dalam setiap fasa — ukuran % sahaja (versi 95), satu jadual kaedah × metrik dengan skor (versi 96), label hanya selepas sampel cukup (14 Okt), kad telefon yang mudah dibaca (versi 79–86), dan panel Esok, Berubah dan status data (pratonton yang disetujui pada versi 89) ([dashboard.md:3](../BacktestShariah2/standard/dashboard.md#L3)). Fasa 1 sengaja menyimpan semua tab lama di bawah Lagi: jika laman baharu tersilap, tiada maklumat yang hilang, dan pemilik boleh membandingkan kedua-duanya selama seminggu sebelum Fasa 3 membuang pendua secara kekal.

## Kesimpulan

Papan ini tidak kekurangan data; ia kekurangan pendirian. Antara 15 dan 22 Okt, setiap soalan baharu dijawab dengan panel baharu — versi 93 hingga 102 sahaja ditambah dalam kira-kira dua hari — sehingga papan menyimpan setiap jawapan yang pernah diberi, termasuk jawapan yang sudah digantikan. Perubahan yang paling bernilai bukan visual. Ia ialah keputusan untuk mempunyai satu ranking, satu kosa kata, satu asas data dan satu garis kejayaan (EW), dan untuk membenarkan papan berkata "belum" dengan yakin sambil menunjukkan bila "ya" boleh mula dikatakan. Dua pembaikan termurah memberi kesan terbesar minggu ini: membaca medan `harian/status` yang sudah ditulis, dan memapar ayat jujur "belum ada kaedah terbukti; pertama cukup data ±26 Okt".

Rombakan ini juga mengalihkan unit keputusan wang sebenar. Bukti projek sendiri menunjukkan nilai datang daripada cara memilih dan memegang saham dalam portfolio terhad, bukan daripada pangkat satu kaedah; jadi soalan "kaedah mana layak wang sebenar?" akhirnya dijawab oleh keluk portfolio beku lawan EW selepas kira-kira enam bulan, manakala ranking kaedah hanya membina senarai calon. Apabila EW hadapan dan garis 10% berada di skrin yang sama setiap hari, pemilik akan berdepan soalan yang lebih besar lebih awal: sama ada sasaran 10% sebulan — kira-kira 2.5 kali kadar bulanan terbaik dalam backtest — patut kekal sebagai sasaran, atau menjadi garis aspirasi dengan "mengalahkan EW secara konsisten" sebagai ukuran kejayaan yang sebenar.
