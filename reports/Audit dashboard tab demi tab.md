# Papan mengira tepat, tetapi belum boleh memilih

Hampir setiap nombor dalam papan versi 103 dikira dengan betul: kad KPI Ringkasan dan skor Prestasi berbeza **0.000** daripada kiraan semula bebas, skor Penganalisis padan bagi 134/134 kaedah, dan **5,711 baris posisi C** dalam db sama medan demi medan dengan CSV repo. Namun papan ini **belum boleh dipakai untuk memilih kaedah bagi wang sebenar**, atas tiga sebab. Pertama, ada lima ralat data hulu yang sudah dibekukan dan tidak ditangkap oleh `sahkan.py`: harga beli DAC M80/M90, ambil alih ACA yang tidak ditanda, keluar lorong 2 VIAV/LITE, ikon 📅 daripada tarikh lama, dan sasaran statik M01/M03/M28. Selain itu, satu pepijat statistik mematikan pengecutan skor swing, kerana τ̂² dikira atas semua kaedah termasuk kaedah bukan swing. Kedua, **sembilan panel menobatkan lapan kaedah berbeza** sebagai "terbaik", dan semuanya bersandar pada data yang belum matang. Hanya **10 daripada 9,810** posisi hadapan sudah matang. Ranking Analisis masih 100% backtest dipotong, dengan peluang #1 benar-benar #1 hanya **29%**. Ujian ramalan skor swing pula memberi **ρ = 0.01**. Ketiga, Posisi dan KPI segar setiap pagi, tetapi Analisis dan portfolio 10 slot sentiasa lewat satu sesi, belian hari itu tidak kelihatan kira-kira sembilan jam, dan dokumen `prestasi/mae` dijangka **melepasi had 262,144 bait sekitar tolakan sesi 30 Okt**. Jika itu berlaku, semua tolakan db akan terhenti. Status sebenar paling awal bagi mana-mana kaedah ialah **4 Nov** (M20 dan M73, kedudukan #55 dan #74), dan bagi 5 teratas Analisis antara pertengahan November dan akhir Disember. Cadangannya: baiki lapan perkara segera minggu ini, kemudian rampingkan lapan tab kepada empat (Hari Ini, Kaedah, Posisi, Lagi) dengan satu ranking sahaja, iaitu daripada kira-kira 38 panel dalam empat tab keputusan kepada kira-kira 11. Hari ini tiada kaedah yang wajar dipilih untuk wang sebenar, dan papan patut menyatakannya pada skrin pertama.

> **Nota bukti.** Audit ini baca sahaja dan dibuat pada 24 Okt 2026 (~02:10 UTC). Ia meliputi halaman langsung versi 103 (versi terbit `1792744352-da38`, sama bait demi bait dengan `dashboard_v2.html`) dan db artifact. Kebanyakan dokumen db dibina pada 24 Okt 06:30 MYT dengan harga tutup **Jumaat 23 Okt**. Dua pengecualian ialah `analisis/papan` v9 dan `prestasi/portfolio_slot` v7, yang memakai data 22 Okt. Halaman dijalankan dalam Chromium dengan salinan db. Angka dikira semula dalam Python terus daripada CSV repo, registry, Lejar dan stor harga, dan enam saham disemak dengan kline Moomoo. Angka bertanda **[kiraan audit]** ialah kiraan semula, bukan bacaan halaman. Skrip dan output disimpan di `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/` (`audit_kpi`, `audit_posisi`, `audit_analisis`, `audit_aliran`, `audit_lain`). `H:n` bermaksud `BacktestShariah2/standard/dashboard_v2.html` baris n. Sumber luar tentang statistik dan reka bentuk dibaca melalui ringkasan carian dan abstrak, kerana proksi menyekat teks penuh. Audit ini tidak mengubah sebarang fail repo, db atau artifact.

## Lapan tab: angka betul, tetapi asas dan label salah

Cadangan rombakan 22 Okt (empat tab dan satu ranking) belum dilaksanakan, dan versi 103 masih mempunyai lapan tab ([H:707](../BacktestShariah2/standard/dashboard_v2.html#L707)). Jadual di bawah meringkaskan jawapan bagi empat soalan audit untuk setiap tab. Butirannya dihuraikan dalam bahagian seterusnya.

| Tab | (1) Tepat? | (2) Terkini? | (3) Aliran kerja | (4) Berguna untuk keputusan? | Keputusan |
|---|---|---|---|---|---|
| Ringkasan | Aritmetik tepat (beza 0.000); purata mencampur dagangan selesai dengan untung belum direalisasi | Tutup 23 Okt; slot 22 Okt | Segar setiap pagi; belian 9:35 NY tidak kelihatan ~9 jam | Separuh: Esok/Berubah berguna; label §7, scatter dan podium mengelirukan | NAIK TARAF → Hari Ini |
| Analisis | Skor 134/134 tepat; label semakan luar sampel salah; susunan ikut nilai dibundar | Data 22 Okt (−1 sesi; −3 hari merentas hujung minggu) | Cron Lejar ~5 jam lewat; rantai ke Analisis belum diuji | Rendah buat masa ini: 100% backtest, P(#1) 29% | KEKAL sebagai ranking tunggal, NAIK TARAF |
| Prestasi | Aritmetik tepat; pepijat τ̂²; "kejatuhan" bukan ekuiti; label "menang 43%" salah | Tutup 23 Okt bercampur prior 22 Okt | Segar | Rendah: 22 panel, enam kedudukan bercanggah | BUBAR; skor swing jadi diagnostik |
| Posisi | Baris tepat (0 beza db–CSV); ralat DAC, ACA, VIAV/LITE, 📅 pada 146 posisi | Tutup 23 Okt; 2 bar sintetik | Belian tidak kelihatan ~9 jam | Tinggi untuk operasi; KPI kepala mengelirukan untuk pemilihan kaedah | KEKAL, NAIK TARAF |
| Watchlist | 32/32 tepat; KPI ≥ 99% bercampur kes "paras disentuh" | Harga 23 Okt; gred data 22 Okt tetapi dilabel 23 Okt | Segar | Tinggi untuk esok; 51% pendua senarai beli | GABUNG → Hari Ini |
| Backtest | Registry 1,589/1,589 tepat; langkah 6–7 corong terlalu longgar | Beku 17–18 Okt tetapi dilabel "Langsung" | Tiada penulis automatik; ~2 MB dimuat setiap kali dibuka | Rendah; podium bercanggah dengan Analisis | PINDAH → Lagi, betulkan |
| Kaedah | 134/134 tepat; pil M31 "Tiada henti" salah; 4 ayat pegang salah | Katalog 17 Okt (peraturan tidak berubah) | Tiada ujian penyegerakan dengan kod | Sederhana (rujukan) | GABUNG → Profil kaedah |
| Sektor | Prestasi kumpulan tepat; medan SST beku; lajur 1H sentiasa kosong | SST ≤ 14–20 Okt tetapi dilabel "hari ini" | SST tidak tersedia sejak 20 Okt | Rendah; gred kumpulan v2 yang sudah disahkan tidak dipapar | PINDAH → Lagi › Konteks pasaran |

## Lima ralat data lolos kerana tiada semakan yang mencarinya

Logik halaman boleh dipercayai. Db `papertrade/ringkas_c` dan `ringkas_m` sama medan demi medan dengan CSV pada HEAD `c0adf74` ([jana_db.py:217](../BacktestShariah2/standard/jana_db.py#L217)). Semakan lain [kiraan audit] juga sepadan:
- Harga terkini posisi terbuka sama dengan tutup yfinance 23 Okt (beza ≤ 0.005) bagi setiap saham yang ada bar.
- Daripada 390 keluar isyarat, 388 sepadan dengan bar hari keluar. Daripada 946 keluar henti, 944 sepadan. Empat pengecualian itu disahkan betul oleh kline Moomoo.
- Tiada satu pun daripada 4,073 posisi terbuka yang harga rendahnya sudah melepasi henti.
- Susunan SMA trend sama 100% bagi 886 saham.

Di luar Posisi, Lejar Penuh lulus semakan populasi bagi 8,528 posisi, dan 26 daripada 29 posisi rawak dihasilkan semula daripada kod kaedah tanpa pandang depan ([lejar/terbuka.csv](../BacktestShariah2/lejar/terbuka.csv)). Skor Penganalisis padan bagi 134/134 kaedah, registry bagi 1,589/1,589 baris, dan watchlist bagi 32/32 baris [kiraan audit]. Jadi ralat yang tinggal semuanya **di hulu**. Ia ialah nilai salah yang sudah dibekukan dalam CSV, dan tiada semakan automatik yang membandingkannya dengan kebenaran luar seperti bar rasmi atau tindakan korporat.

**DAC M80/M90** direkod dengan harga beli **164.162**, sedangkan buka rasmi 12 Okt ialah **170.19** dan harga rendah hari itu 169.25. Ini bermakna harga 164.162 tidak pernah didagangkan (kline Moomoo dan stor yfinance sepakat). Kesannya: untung akhir M80 sebenarnya −7.66%, bukan −4.27%; M90 −5.32%, bukan −1.84%; dan lorong 2 −6.96%, bukan −3.55%. Untung kedua-dua baris ini terlebih kira-kira 3.4–3.5 mata, kesan yang besar bagi kaedah dengan n kecil [kiraan audit]. Ralat ini lolos kerana `sahkan.py` tidak menyemak harga beli lawan buka bar hari beli, dan `keluar_lorong.py` hanya melangkau beza melebihi 15% ([sahkan.py:119](../BacktestShariah2/standard/sahkan.py#L119), [keluar_lorong.py:30](../BacktestShariah2/standard/keluar_lorong.py#L30)). Asal nilai 164.162 tidak dapat dijejak kerana sejarah git cetek.

**ACA (Arcosa) telah diambil alih** oleh CRH pada USD150 tunai. Perjanjian dibuat pada 21 Jun 2026, diluluskan pemegang saham pada 4 Sep, dan penggabungan selesai pada **23 Okt 2026** ([SEC 8-K pengumuman](https://www.sec.gov/Archives/edgar/data/0001739445/000173944526000112/exh991-crhtoacquirearcos.htm), [Arcosa IR](https://ir.arcosa.com/news-events/press-releases/news-details/2026/Arcosa-Stockholders-Approve-Acquisition-by-CRH/default.aspx), [SEC 8-K penutupan](https://www.sec.gov/Archives/edgar/data/0001739445/000114036126040596/ef20084131_8k.htm)). Lapan posisi C dibeli selepas pengumuman: M95 dan M54 pada 12 Okt @147.01, serta M06, M23, M46, M100, M101 dan M120 pada 22 Okt @148.90. Kesemuanya masih dikira sah, sedangkan CLAUDE.md menetapkan posisi seperti ini sebagai `tidak_sah` dan mesti ditutup ([CLAUDE.md](../CLAUDE.md)). Bar 23 Okt ACA ialah bar rata sintetik 149.15. Papan memaparkan "Bullish lama · ATR 0.35%" dan R +2.65 bagi untung +1.46%, iaitu dagangan berisiko hampir sifar yang menaikkan kadar menang dan R kaedah. Pengesan corak harga terlepas kes ini kerana jurang hari pengumuman hanya +6.74%, di bawah `JURANG_MIN` 10%. ACA juga tiada dalam `data/ambil_alih.csv`, folder `data/edgar/` belum wujud, dan lapisan EDGAR hanya menulis "calon" bagi penggabungan tunai melalui undian ([ambil_alih.py:32](../BacktestShariah2/kod/ambil_alih.py#L32), [tawaran_edgar.py](../BacktestShariah2/standard/tawaran_edgar.py)).

**Keluar lorong 2 VIAV dan LITE** (Moomoo lama, strategi luar S04V2) direkod seminggu lewat. VIAV direkod keluar 22 Okt @33.40 (−27.53%), sedangkan kiraan semula memberi 15 Okt @36.88 (−19.98%). LITE direkod keluar 22 Okt @804.06 (−22.93%), sedangkan yang betul ialah 16 Okt @853.485 (−18.19%). Carta lilin dalam helaian yang sama sudah menunjukkan tarikh yang betul, jadi helaian itu bercanggah dengan dirinya sendiri. Puncanya ialah ATR yang dikira daripada stor kerja tanpa sejarah sebelum tarikh beli. Nilai salah itu kemudian dibekukan oleh `kemas_baris` ([keluar_lorong.py:140](../BacktestShariah2/standard/keluar_lorong.py#L140)). Ralat ini menjejaskan akaun M dan Gabung, bukan C.

**Ikon 📅** memakai tarikh earnings yang direkod pada hari isyarat, bukan tarikh sebenar `earn_seb` yang sudah ada dalam db ([H:2371](../BacktestShariah2/standard/dashboard_v2.html#L2371), [jana_db.py:52](../BacktestShariah2/standard/jana_db.py#L52)). Akibatnya, **114 posisi (26 saham) tiada ikon** walaupun earnings sebenar jatuh dalam ≤ 10 hari, contohnya FRD dan GRAL pada 4 Nov serta CRSR pada 5 Nov. **32 posisi (4 saham) pula diberi ikon palsu**, contohnya PSO dengan tarikh 25 Okt yang jatuh pada hari Ahad, sedangkan earnings sebenar 25 Feb 2027 [kiraan audit].

**Lajur `sasaran`** bagi M01, M03 dan M28 menyimpan paras hari isyarat, sedangkan kaedah ini memakai sasaran dinamik. Akibatnya, 37 keluar "capai sasaran" tidak sepadan dengan sasaran yang direkod. Contohnya, KBH M01 keluar @45.91 sedangkan "sasaran"nya 47.98. Kad dan teks "Pegang (henti X, sasaran Y)" juga memaparkan sasaran statik bagi 58 posisi terbuka ([H:2167](../BacktestShariah2/standard/dashboard_v2.html#L2167)). Lejar mempunyai kes serupa bagi kaedah replika: VRTX M02 menyimpan sasaran 684.45, sedangkan keluar memakai 636.08 ([lejar.py:422](../BacktestShariah2/standard/lejar.py#L422)). Untung dan rugi tidak terjejas.

Beberapa **label** juga salah, dan ini lebih mengelirukan daripada salah kira:
- Semua baris C yang `tidak_sah` (ambil alih, tidak cair, kelas berganda) dipaparkan sebagai pil "Luar peraturan", iaitu istilah Moomoo.
- Subtajuk KPI sentiasa menulis "122 dibeli luar peraturan", kerana `all.some(r=>r.tidak_dibeli)` sentiasa palsu ([H:1475](../BacktestShariah2/standard/dashboard_v2.html#L1475)).
- Tooltip `harga_beli` ("harga isian purata") salah bagi C ([H:3586](../BacktestShariah2/standard/dashboard_v2.html#L3586)).
- Tujuh keluar lorong 1 yang dibuka semula sejak 21 Okt (RMR M99 akibat faktor dividen; DT, PSX dan DHT M82; TRMB M20; DELL dan UMC M81) tidak diberi sebarang tanda pada halaman.
- `harian/status` mencatat 186 keluar baharu C, tetapi hanya 175 keluar lorong 1 pada 23 Okt dapat dipadankan. Punca beza ini belum diketahui.

## Sembilan panel menobatkan lapan kaedah, dan tiada yang layak wang sebenar

### Kad KPI Ringkasan tepat, tetapi +1.77% bukan ukuran prestasi

Setiap kad sepadan dengan kiraan semula: "Dagangan selesai" −2.84% (1,366 dagangan, menang 17%), "Masih dipegang" +3.28% (4,159 posisi), "Keseluruhan" +1.77%, dan "Aktiviti terkini" 760 dibeli dan 175 keluar ([H:3347](../BacktestShariah2/standard/dashboard_v2.html#L3347)). Masalahnya ialah takrif, bukan aritmetik. Angka +1.77% mencampur **untung belum direalisasi** posisi berumur median 3 hari (hanya 114 posisi berumur ≥ 10 hari) dengan dagangan selesai yang **65% keluar kerana henti rugi** (55.6% dalam ≤ 1 hari). Dagangan rugi keluar dahulu, manakala dagangan untung masih dipegang. Purata seperti ini ialah anggaran berbias bagi cerapan tertapis kanan ([MedCalc: Kaplan–Meier](https://www.medcalc.org/en/book/kaplan-meier.php)). Panel "Dua lorong" pula mengisytiharkan "Lebih untung setakat ini: pegang selagi naik", walaupun beza +0.10 mata hanya t ≈ 0.81 (SE berkelompok 0.13, G = 12), dan 98% posisi lorong 2 masih terbuka [kiraan audit] ([H:3330](../BacktestShariah2/standard/dashboard_v2.html#L3330)). Metrik "USD1,000 setiap belian" juga masih dipaparkan, walaupun pengguna sudah meminta ukuran % sahaja pada versi 95 ([dashboard.md:3](../BacktestShariah2/standard/dashboard.md#L3)).

### Empat asas data menghasilkan lapan juara

Pada data 23 Okt, sekurang-kurangnya sembilan panel menobatkan lapan kaedah berbeza:
- **M92**: label §7, Ringkasan.
- **M70**: % untung, KPI dan tajuk Prestasi.
- **M120**: jadual U×S dan bar kadar menang.
- **M87**: bar untung purata.
- **M107**: median sebaran.
- **M99**: skor swing.
- **M21**: Analisis.
- **M30**: podium backtest.

Sumbernya ialah teks halaman yang dijalankan dalam Chromium [kiraan audit] ([H:3327](../BacktestShariah2/standard/dashboard_v2.html#L3327), [H:1594](../BacktestShariah2/standard/dashboard_v2.html#L1594), [db analisis/papan](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)). Punca utama ialah empat asas data yang berbeza:
1. Semua posisi termasuk yang belum direalisasi, dikira kasar (§7, % untung, U×S).
2. Semua posisi pada lorong terpilih, dikira bersih kos tetapi hampir tanpa pengecutan (skor swing).
3. Posisi matang yang dikecutkan ke jangkaan backtest. Hari ini ini hampir 100% backtest (Analisis).
4. Backtest sahaja (podium).

Korelasi Spearman antara "purata semua" dengan "purata selesai" hanya **0.08** [kiraan audit]. Satu kaedah juga boleh menerima label yang bertentangan. Contohnya, M55 ialah HENTIKAN dalam §7, "Calon (awal) 66%" dalam skor swing, dan #7 dalam Analisis.

Kes paling berbahaya untuk wang sebenar ialah **M70**. KPI Prestasi "Kaedah terbaik (% untung)" memaparkan M70 +2.85% dengan "menang 43%". Hakikatnya, **0 daripada 43 dagangan selesai M70 menang**: semuanya kena henti, dengan median pegangan 0 hari. Angka 43% itu ialah kadar menang semua posisi, kebanyakannya belum direalisasi ([H:1714](../BacktestShariah2/standard/dashboard_v2.html#L1714)). Label §7 pula hampir mustahil mencapai TERUSKAN. Skor U×S tertinggi bagi kaedah dengan ≥ 20 dagangan selesai ialah 38, sedangkan ambang TERUSKAN ialah 55, dan korelasi Spearman antara bilangan selesai dengan U×S ialah −0.44 ([H:1561](../BacktestShariah2/standard/dashboard_v2.html#L1561)). Strip "Cara baca" Prestasi masih mengarahkan pengguna supaya "Pilih kaedah yang TERUSKAN" ([H:1877](../BacktestShariah2/standard/dashboard_v2.html#L1877)).

### Skor swing tidak mengecut kerana τ̂² dikira atas kaedah bukan swing

Aritmetik skor swing sepadan dengan spec: kos 0.1% setiap belah, tunjang U40/K20/R25/B15, Wilson ikut hari beli, CVaR dan penalti lorong ([TIPS H:3630](../BacktestShariah2/standard/dashboard_v2.html#L3630)). Tetapi ada satu baris yang mematikan rangka Bayes empirik: `const ok=all.filter(x=>x.xadj!=null&&x.neff>=2)` mengira τ̂² atas **semua** kaedah, termasuk kaedah pegang panjang yang jangkaannya 23–83% setiap dagangan ([H:2771](../BacktestShariah2/standard/dashboard_v2.html#L2771)). Hasilnya τ̂² = **126.6** dan median bahagian bukti hadapan B = **0.989**, jadi pengecutan ke arah jangkaan backtest hampir tidak berlaku. Jika τ̂² dikira atas kaedah swing sahaja, nilainya 0.646 dan B jatuh kepada 0.49–0.77 [kiraan audit].

Tiga kelemahan lain menambah keyakinan palsu:
- n berkesan hampir sama dengan n mentah, bukan dengan bilangan hari beli G. Contohnya M12: n_eff 80 berbanding G 11 ([H:2720](../BacktestShariah2/standard/dashboard_v2.html#L2720)).
- Pintu "≥ 20 selesai" diukur pada lorong 1, tetapi skor dikira pada lorong terpilih. M03 lulus pintu dengan 81 keluar lorong 1, tetapi diskor pada lorong 2 yang mempunyai 0 keluar ([H:2785](../BacktestShariah2/standard/dashboard_v2.html#L2785)).
- 15 daripada 16 kaedah layak mempunyai **0 posisi matang**, jadi seluruh jadual dikira atas sandaran "semua posisi (awal)" ([H:2748](../BacktestShariah2/standard/dashboard_v2.html#L2748)).

Akibatnya, P(untung > 0) 98–100% dan label "stabil" tidak bermakna. Kedudukan teratas bertukar setiap sesi: M70 (21 Okt), M03 (22 Okt), M99 (23 Okt). P(4 teratas) bagi M18 jatuh daripada 0.81 kepada 0.17 dalam dua sesi. Ujian ramalan dalam halaman sendiri memberi ρ = 0.02 dan −0.00 ([H:2830](../BacktestShariah2/standard/dashboard_v2.html#L2830)). Pembaikan juga mengubah susunan: τ̂² atas kaedah swing sahaja meletakkan M92 di atas M99, manakala n_eff = G menjadikan M55 #1 dan menjatuhkan M03 ke #9 [kiraan audit]. Selang berkelompok yang dikira dengan bilangan kelompok yang sedikit sememangnya terlalu sempit ([Cameron & Miller](https://jhr.uwpress.org/content/50/2/317)).

### Kedudukan Analisis ialah backtest dipotong, dengan peluang #1 hanya 29%

Penganalisis dilaksanakan seperti didokumenkan, dan larian semula menghasilkan papan yang sama ([penganalisis.py:500](../BacktestShariah2/standard/penganalisis.py#L500)). Tetapi hanya 10 posisi hadapan yang matang (M20 dan M73, semuanya dibeli 8 Okt), jadi susunan ini ialah **susunan backtest dipotong** ([PENGANALISIS.md](../BacktestShariah2/laporan/PENGANALISIS.md)). Kaedah #1, **M21**, mempunyai profil berikut:
- Berstatus DITOLAK dalam registry.
- 0 posisi Lejar dan 1 posisi C.
- Median dagangan backtest −2.6%.
- 1% dagangan terbaik menyumbang 53% jumlah untung.
- Purata dipangkas 5% ialah −0.51%.

M21 berada di tempat teratas kerana dua andaian rapuh. Pertama, skor sebulan didarab 21/7.94 bagi kaedah pegang pendek, jadi julatnya juga menjadi paling lebar. Kedua, M21 menerima kredit +25% kerana "lulus WFO". Kredit semakan luar sampel itu sendiri lemah:
- **S1–S4 ialah partisi tanpa pertindihan bagi 431 saham yang sama** dalam tempoh yang sama, walaupun tooltip menulis "di luar data backtest asal" ([H:3669](../BacktestShariah2/standard/dashboard_v2.html#L3669)).
- WFO memakai versi yang ditala semula dengan Optuna dalam tempoh 2023–2026, iaitu di dalam tempoh pemilihan varian ([W01_LAPORAN.md](../WFO/laporan/W01_LAPORAN.md)).
- AUTOTUNE, satu-satunya semakan yang benar-benar di luar data (2000 saham AS lain), **gagal bagi 134/134 kaedah** ([AUTOTUNE/hasil/papan.json](../AUTOTUNE/hasil/papan.json)).

Jika satu andaian diubah, kedudukan berubah. Tanpa kredit WFO, M144 menjadi #1. Jika purata dipangkas 5% dipakai, M21 jatuh ke #72 daripada 74. Simulasi Monte Carlo daripada julat halaman sendiri memberi **P(M21 benar-benar #1) = 28.6%**, dengan selang pangkat 90% merentas 1–74 [kiraan audit].

Bukti backtest 12 teratas juga lemah. Nilai t berkelompok bulanan ialah 1.37–3.08, sedangkan halangan ujian berbilang bagi 633 varian ialah ≈ 3.6–3.8. Harvey, Liu dan Zhu menuntut t > 3.0 bagi penemuan baharu ([NBER w20592](https://www.nber.org/papers/w20592)), dan DSR menaikkan palang ini mengikut bilangan cubaan ([SSRN 2460551](https://papers.ssrn.com/abstract=2460551)). Purata 2022 negatif bagi 11 daripada 12 kaedah teratas, dan korelasi antara beberapa kaedah teratas sehingga 0.84 (M32 dengan M102 dan M127). Ada juga tiga pepijat kecil:
- Susunan dibuat atas `skor_bulan` yang sudah dibundar, jadi 14 pasangan di #14–#74 tertukar ([penganalisis.py:535](../BacktestShariah2/standard/penganalisis.py#L535)).
- KPI "20 matang pertama 26 Okt" mengabaikan syarat ≥ 10 hari beli.
- `harga_akhir()` mengambil tarikh `terkini.csv`, bukan sesi Lejar, jadi larian semula boleh mencampur vintaj data.

Mengikut syarat ≥ 20 matang dan ≥ 10 hari beli, status sebenar paling awal ialah **4 Nov** bagi M20 (#55) dan M73 (#74), diikuti M18 (6 Nov), M03 (7 Nov) dan M70 (12 Nov). Bagi 10 teratas, M21 paling awal ≥ 15 Nov, manakala M140, M144 dan M84 ≥ 21–22 Dis [kiraan audit].

### Label pantau buta terhadap kerugian berterusan

Semua 134 kaedah betul berlabel BELUM CUKUP pada masa ini, tetapi kalibrasi akan menjadikan pantau hampir buta apabila data cukup. Sasaran CUSUM mencampur purata winsor dengan purata mentah, sehingga sasaran itu **negatif bagi 68 daripada 75 kaedah swing**. Ambang GANTUNG bergulir pula −5% hingga −8.7% setiap hari beli ([penganalisis.py:416](../BacktestShariah2/standard/penganalisis.py#L416), [kalibrasi_skor.json](../BacktestShariah2/data/analisis/kalibrasi_skor.json)). Ujian sintetik dengan parameter sebenar menunjukkan kesannya [kiraan audit]:
- M32 dengan **25 hari beli berturut-turut rugi purata −5% masih "OK"**.
- M84 dengan hanya 4 kohort −10% terus BERSARA, kerana semakan BERSARA dibuat sebelum pengawal BELUM CUKUP ([penganalisis.py:435](../BacktestShariah2/standard/penganalisis.py#L435)).

Tab Analisis juga tidak memaparkan lajur pantau langsung. Gabungan beku M70/M03/M18 berada di #35, #39 dan #52 dalam Analisis, dan halaman tidak menerangkan percanggahan ini ([gabungan_beku.json](../BacktestShariah2/data/analisis/gabungan_beku.json)).

## Posisi tepat setiap baris, tetapi mengelirukan sebagai purata

Tab Posisi ialah buku besar operasi yang baik. Setiap baris memaparkan apa yang ada dalam CSV dan db dengan tepat, dan helaiannya (carta lilin dan ulang tayang lorong 2) cukup jelas sehingga dapat mendedahkan ralat VIAV sendiri. Masalahnya ialah tab ini tidak sesuai sebagai alat pemilihan kaedah:
- **KPI kepala dan Peta tidak mengikut tapisan.** Jika satu kaedah dipilih, hanya jadual yang berubah, manakala kad KPI dan Peta kekal bagi semua 122 kaedah ([H:1517](../BacktestShariah2/standard/dashboard_v2.html#L1517)).
- **Purata +1.77% mencampur dagangan selesai dengan untung belum direalisasi**, sama seperti Ringkasan.
- **Peta mengira posisi, bukan saham.** 4,159 posisi terbuka sebenarnya hanya dalam 605 saham (BIIB 34 posisi), dan 73.6% posisi C berkongsi saham dan hari beli dengan kaedah lain. Jadi saiz kotak menggambarkan pertindihan isyarat, bukan pendedahan sebenar ([H:3037](../BacktestShariah2/standard/dashboard_v2.html#L3037)).
- **Segmen "Dipegang" hanya bermaksud lorong 1.** 1,268 posisi C yang masih dipegang dalam lorong 2 berada dalam "Sudah keluar" dan tiada dalam Peta.
- **MAE dan MFE berhenti pada keluar lorong 1**, jadi tempoh pegangan lorong 2 bagi 1,348 posisi tidak diliputi ([jana_db.py:252](../BacktestShariah2/standard/jana_db.py#L252)).
- **Akaun Gabung tidak mengira dua kali, tetapi mencampur dua populasi yang tidak serasi.** M memakai harga isian sim, C memakai buka rasmi. M juga mengandungi 11 posisi strategi luar, 50 posisi warisan v1 dan 15 baris dengan unit > 1, dan tempoh pasarannya berbeza. Tanpa strategi luar, purata M berubah daripada +0.86% kepada +1.27%.

Pengecualian `tidak_sah` dan `tidak_dibeli` dibuat secara konsisten dalam KPI, Peta dan semua dokumen prestasi. Kelemahannya ada pada liputan dan label:
- Posisi tidak cair dan kelas berganda dibiarkan "Dipegang" tanpa had masa. Contohnya, lorong 2 BKHA M76 memaparkan paras keluar −0.06 dengan untung −49.77%, dan 14 baris FOX (pelbagai kaedah) masih terbuka.
- Segmen "Semua 5,647" termasuk 122 baris `tidak_sah`, sedangkan KPI "5,525" tidak.
- Panel "Isyarat tidak dibeli" hanya memaparkan 64 baris, sedangkan log rutin mencatat kira-kira **159 langkauan semasa belian 9:35 NY** (14–23 Okt) yang tidak pernah direkod sebagai baris. Contohnya, NSIT M08 dilangkau kerana buka > buka_maks dan SSNC M23 kerana buka ≤ henti ([binaan_v2_log_tambahan.md](../BacktestShariah2/standard/binaan_v2_log_tambahan.md), [H:1531](../BacktestShariah2/standard/dashboard_v2.html#L1531)). Kadar isyarat yang tidak boleh dilaksanakan ini penting apabila menilai sesuatu kaedah untuk wang sebenar.

Pandangan Penuh pula dipenuhi rekod hari isyarat yang projek sendiri sudah nyatakan sebagai tidak meramal: 7 lajur gred, Trend, Pemangkin dan Kewangan ([TIPS H:3642](../BacktestShariah2/standard/dashboard_v2.html#L3642), [CLAUDE.md](../CLAUDE.md)). Halaman juga memakai empat takrif "hampir paras keluar" yang berbeza ([H:2362](../BacktestShariah2/standard/dashboard_v2.html#L2362)). Susunan lalainya untung menurun, jadi posisi yang paling memerlukan tindakan berada paling bawah ([H:1484](../BacktestShariah2/standard/dashboard_v2.html#L1484)). Elemen yang benar-benar berguna untuk menilai kaedah (beza lawan SPY, MAE/MFE, hari lawan had masa, dua lorong) sudah ada pada setiap posisi, tetapi tidak diagregat mengikut kaedah yang ditapis.

## Saluran harian segar, tetapi satu dokumen boleh menghentikan semua tolakan

Dari segi kesegaran harian, aliran kerja berfungsi. Rutin Claude 6:02 MYT commit posisi rasmi antara 22:08 dan 22:12 UTC dan menolak db penuh kira-kira 22:30 UTC. Kesemua 7 sesi antara 15 dan 23 Okt segar, dan tiada sesi yang tertinggal ([log commit](https://github.com/pedagangsenja/papertrade-claude/commits/main)). Namun lima kelemahan reka bentuk menjejaskan tab KPI dan Posisi secara langsung.

**Had saiz db ialah risiko paling hampir.** `prestasi/mae` belum dibahagi. Saiznya kini 172,773 bait dan bertambah kira-kira 14–22 KB setiap hari belian (491–761 belian sehari). Baki ruangnya cukup untuk kira-kira 4–5 hari belian, jadi ia dijangka melepasi had **262,144 bait sekitar tolakan sesi Jumaat 30 Okt** (anggaran). Apabila satu dokumen melebihi had, `jana_db.py` menjalankan `raise SystemExit` **sebelum sebarang batch ditulis**, jadi semua 108 dokumen tidak ditolak ([jana_db.py:578](../BacktestShariah2/standard/jana_db.py#L578)). Selepas peralihan ke Actions, kegagalan yang sama akan turut menghalang commit Papertrade C dalam `harian.yml` ([harian.yml:97](../.github/workflows/harian.yml#L97)). Preseden sudah ada: pada 22 Okt, `prestasi/mae` mencecah 301 KB dan lajur atr terpaksa digugurkan. Dokumen lain yang tidak dibahagi juga hampir dengan had: `papertrade/moomoo` 238,253 bait, `papertrade/claude` 208,857 bait dan `analisis/papan` 167,074 bait.

**Ketinggalan yang sudah dijangka, tetapi tidak dilabel.** Lejar sesi D hanya muktamad kira-kira 07:00 UTC hari berikutnya, jadi `analisis/papan` dan `prestasi/portfolio_slot` sentiasa lewat satu sesi. Merentas hujung minggu, data sesi 23 Okt hanya akan sampai ke db pada Selasa 27 Okt 06:02 MYT. Skor swing juga mencampur data C 23 Okt dengan prior Analisis 22 Okt ([H:2747](../BacktestShariah2/standard/dashboard_v2.html#L2747)). Belian 9:35 NY pula tidak kelihatan dalam Posisi dan KPI dari 13:41 hingga 22:30 UTC setiap hari, kerana rutin beli menolak `claude_N`, sedangkan halaman membaca `ringkas_c`. Dalam tempoh yang sama, cip "Belian 9:35 NY" tetap hijau ([beli_0935.md](../BacktestShariah2/jadual/beli_0935.md), [H:3809](../BacktestShariah2/standard/dashboard_v2.html#L3809)). Lencana "Kemas kini terakhir" hanya mengukur masa tolakan, bukan sama ada tarikh data ialah sesi yang dijangka ([H:844](../BacktestShariah2/standard/dashboard_v2.html#L844)).

**Kegagalan senyap.** Pada 22 Okt, langkah portfolio_slot gagal dengan kod keluar 1, tetapi larian dilaporkan "success" kerana langkah itu `continue-on-error: true` ([run 39737312472](https://github.com/pedagangsenja/papertrade-claude/actions/runs/39737312472), [lejar.yml:47](../.github/workflows/lejar.yml#L47)). `jana_db.py` membungkus `harian/trend` dan `posisi/lorong2` dalam `try/except` yang hanya mencetak ke stderr ([jana_db.py:540](../BacktestShariah2/standard/jana_db.py#L540)). Notifikasi Telegram telah dibuang, jadi satu-satunya amaran ialah e-mel GitHub. Amalan yang baik ialah mengikat amaran kepada kesan sebenar dan mengelak keletihan amaran ([AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/ops_workload_observability_create_alerts.html)).

**Titik kegagalan tunggal dan label sumber yang salah.** `MOD_ACTIONS` masih `bayang`, jadi tiga sesi rutin Claude ialah satu-satunya penulis data rasmi dan db. Pengawas rutin pula dimatikan sejak 19 Okt ([jadual/README.md](../BacktestShariah2/jadual/README.md)). Sudah ada preseden kegagalan kerana had penggunaan pada 12 Okt, dan SST tidak tersedia sejak 20 Okt. `jana_db.py` pula menulis "bar harian yfinance muktamad; GitHub Actions" tanpa mengira penulis sebenar ([jana_db.py:446](../BacktestShariah2/standard/jana_db.py#L446)). Hakikatnya, data rasmi datang daripada rutin Claude: tarikan yfinance pada 22:04 UTC ditambah skrin Moomoo bagi 31 saham tanpa bar, sedangkan Lejar sendiri menunggu sehingga 00:20 UTC kerana data Yahoo awal kurang muktamad ([lejar.py:523](../BacktestShariah2/standard/lejar.py#L523)).

**Pembaziran dan prosedur lapuk.**
- Tolakan harian berjumlah kira-kira 14.2 MB, dan 61% daripadanya (`claude_N`) tidak dibaca halaman.
- Langkah 8 prosedur aktif `kemas_kini_0602.md` masih menyenaraikan lapan jenis dokumen lama dan tidak menyebut `jana_db`, `ringkas_c` atau `posisi/lorong2` ([kemas_kini_0602.md:37](../BacktestShariah2/jadual/kemas_kini_0602.md#L37)).
- Cron GitHub tiba 2.5–6 jam lewat setiap hari, jadi penjaga jadual sebenarnya bertindak sebagai penjadual utama. Rantai Lejar → Analisis yang dibaiki pada 23 Okt belum diuji dalam produksi.
- Apabila mod ditukar ke `rasmi`, nombor KPI akan beranjak, kerana 77 dan 84 baris berbeza antara rasmi dan bayang, dan 28 harga keluar berbeza melebihi 0.1% ([bayang/BANDING_2026-10-22.md](../BacktestShariah2/bayang/BANDING_2026-10-22.md)).
- DST AS tamat pada Ahad 1 Nov. Tugasan Claude yang mencetus penjaga berjalan pada jam UTC tetap, jadi cetusan 14:20 UTC akan jatuh sebelum pasaran NY dibuka.

## Watchlist berguna; Backtest dan Sektor menyesatkan

**Watchlist** tepat: 32/32 baris yang dikira semula sepadan, dan 19 daripada 19 "isyarat lengkap" yang boleh disemak disahkan benar pada 23 Okt dan palsu pada 22 Okt ([kod/scanner.py:322](../BacktestShariah2/kod/scanner.py#L322)). Kelemahannya pada label:
- Gred S/I/R dikira daripada data 22 Okt tetapi dilabel `gred_pada` 23 Okt ([gred.py:205](../BacktestShariah2/standard/gred.py#L205)).
- KPI "≥ 99% hampir" turut mengira 9 baris "paras disentuh" yang bernilai 100. Bagi M102, jarak 0 ialah andaian kod, bukan paras yang benar-benar disentuh ([H:1331](../BacktestShariah2/standard/dashboard_v2.html#L1331)).
- Tiga baris LNTH sudah 12 hari dalam watchlist, melebihi `TAMAT_WATCH = 10` ([scanner.py:19](../BacktestShariah2/kod/scanner.py#L19)).
- 51% baris ialah isyarat lengkap yang menduplikasi senarai beli esok.
- 47 kaedah K145+ tiada watchlist. Ini termasuk #1–#3 Analisis (M21, M140, M144).

**Backtest** menyalin registry dengan tepat, tetapi keputusannya bercanggah dengan Analisis:
- Corong 7 langkah memberi pingat kepada 44 kaedah ([H:869](../BacktestShariah2/standard/dashboard_v2.html#L869)). Langkah 6 meluluskan **123** kaedah (CAGR S1–S4 > 0), sedangkan Analisis hanya meluluskan **6** (mengatasi EW dalam ≥ 3/4 subset). Langkah 7 meluluskan **70** kaedah berdasarkan A02, sedangkan Analisis meluluskan **0** berdasarkan A01. 68 daripada 70 kaedah yang lulus itu pun berada di bawah SPY.
- Pingat Emas M30 dan M79 bukan kaedah swing, jadi kedua-duanya tiada kedudukan dalam Analisis.
- KPI "Terbaik gaya anda" menobatkan M24 V4, varian DITOLAK yang tidak pernah didagangkan ([H:984](../BacktestShariah2/standard/dashboard_v2.html#L984)).
- Pengepala memaparkan "Langsung · ujian terkini 2026-10-17" bagi data yang sebenarnya beku ([H:3783](../BacktestShariah2/standard/dashboard_v2.html#L3783)).
- Kira-kira 2 MB registry dimuat setiap kali papan dibuka, termasuk 32 dokumen indikator yang tidak digunakan.

**Kaedah** menerangkan 134/134 varian dengan betul (varian, TMAX, henti, kod K145+). Ada tiga kesilapan:
- Pil "⚠ Tiada henti" bagi M31 salah. Kod M31 mempunyai `ADA_HENTI = True` dan `HENTI_TUTUP` ([M31.py:7](../BacktestShariah2/kod/kaedah/M31.py#L7)).
- Ayat pegang bagi M117, M125, M130 dan M136 menyebut "isyarat keluar", walhal kaedah itu tiada isyarat keluar.
- Jalur "Sama untuk semua" tidak menyebut penapis tidak layak, kelas berganda, belian semula, had 10 isyarat atau kaedah mingguan ([H:1960](../BacktestShariah2/standard/dashboard_v2.html#L1960)).

**Sektor** paling banyak memaparkan data lapuk sebagai data semasa:
- Medan SST (RS, volum relatif, aliran institusi) disalin daripada snapshot lama setiap hari. Nilainya sama sejak 14 Okt, dan kosong bagi 121–122 daripada 138 industri ([snapshot_sektor_db.py:69](../BacktestShariah2/standard/snapshot_sektor_db.py#L69)).
- Senarai "Volum luar biasa hari ini" berumur ≥ 3–4 sesi.
- Lajur 1H sentiasa "–" kerana `prestasi_1d` ditetapkan None ([snapshot_sektor_db.py:66](../BacktestShariah2/standard/snapshot_sektor_db.py#L66)).
- Fasa rotasi masih dipaparkan walaupun nota halaman sendiri menyatakan ia tidak meramal. Sebaliknya, gred kumpulan v2 yang sudah disahkan tidak dipaparkan ([H:1268](../BacktestShariah2/standard/dashboard_v2.html#L1268)).

## Keputusan setiap bahagian: kekal, naik taraf, gabung atau buang

Prinsip yang dipakai ialah satu keputusan utama bagi setiap paparan, pengecualian diserlahkan, dan butiran dibuka atas permintaan ([kesilapan dashboard Few](https://www.thedataschool.co.uk/anh-vu/are-you-making-these-13-dashboard-design-mistakes/), [progressive disclosure](https://en.wikipedia.org/wiki/Progressive_disclosure)). Selagi bukti masih nipis, jadual liga tanpa selang perlu digantikan dengan kebarangkalian kedudukan atau plot corong ([Spiegelhalter, arXiv 1810.12719](https://arxiv.org/pdf/1810.12719)). Nombor dalam kurungan merujuk kepada senarai tindakan di hujung laporan.

**Ringkasan → Hari Ini**
- NAIK TARAF: tajuk, "Kemas kini terakhir" dan jalur 8 cip digantikan dengan **satu lampu sistem**. Lampu ini membanding tarikh data dengan `jangkaSesi`, membaca `harian/status.ralat`, memaparkan mod `bayang`/`rasmi` dan keadaan "menunggu jadual" bagi Lejar, Analisis dan slot (12).
- GANTI: "3 perkara utama" digantikan dengan **banner fasa bukti**: "Belum ada kaedah terbukti · 10/9,810 posisi hadapan matang · status sebenar pertama ±4 Nov; 5 teratas pertengahan Nov–Dis" (6).
- NAIK TARAF: kad KPI. "Aktiviti terkini" dikekalkan dan ditambah bilangan dilangkau daripada `beli_ringkas`. Kad Selesai, Dipegang dan Keseluruhan digantikan dengan satu kad **matang sahaja** yang memaparkan % masih terbuka dan selang 95% berkelompok hari beli. USD1,000 dibuang (19).
- KEKAL: Esok dan Berubah, digabung menjadi satu blok. Ikon earnings memakai `earn_seb` (9).
- BUANG: "Terbaik ikut papertrade" (label §7 dan U×S) dan scatter "Untung lawan risiko". Gantinya ialah 3 calon teratas daripada ranking tunggal, lengkap dengan status dan bendera (16).
- PINDAH: podium "Terbaik ikut backtest" ke Lagi › Backtest dengan label "dalam sampel" (26).
- NAIK TARAF: Eksperimen › portfolio 10 slot menjadi blok "Posisi saya" dengan tarikh sesi. Panel dua lorong memaparkan beza ± SE dengan nota "belum signifikan". Panel gred dipindah ke Lagi › Eksperimen (19).
- PINDAH: strip "Cara baca" ke Panduan, dan kaki Moomoo ke Arkib.

**Analisis → Kaedah › ranking tunggal**
- GANTI: KPI "Swing teratas" dan "Kaedah KUAT" (yang akan kekal 0 sekurang-kurangnya hingga 4 Nov) digantikan dengan banner fasa. Tarikh "20 matang pertama" dibetulkan supaya mengambil kira syarat 10 hari beli (6).
- KEKAL: 3 penemuan utama, dan helaian kaedah yang menjadi Profil kaedah.
- NAIK TARAF: jadual kedudukan (17):
  - "#" digantikan dengan P(5 teratas) dan selang pangkat 90%, dengan susunan lalai ikut had bawah julat.
  - Tambah meter bukti: hari beli matang/10, nb lawan nb diperlukan, dan tarikh status sebenar.
  - Tambah bendera ⚑ DITOLAK dan "0 posisi Lejar".
  - Tambah lajur Pantau, penunjuk ekor (median, purata dipangkas 5%, % untung daripada 1% teratas) dan kelompok korelasi.
  - Sembunyikan lajur C dan Lorong 2 sehingga ada data matang.
- BETULKAN: label semakan ditulis semula sebagai "S1–S4 = kestabilan dalam sampel" dan "WFO = dalam tempoh pemilihan, versi ditala". Tooltip `anl_bulan` dan teks "Cara skor dikira" dibetulkan supaya menyebut nb dan syarat 10 hari beli (6).
- GABUNG: Rujukan EW/SPY digabung ke panel Lawan matlamat.

**Prestasi → dibubarkan**
- BUANG (21):
  - KPI dan tajuk "Kaedah terbaik ikut % untung".
  - Baris 7 KPI pendua.
  - Jadual "Kedudukan kaedah · Skor U×S".
  - Bar "Untung purata" dan "Kadar menang setiap kaedah".
  - Scatter kedua "Untung lawan risiko".
  - "Sebaran untung setiap kaedah".
  - "Kalendar untung harian": 12 daripada 12 hari merah kerana hanya keluar yang dipaparkan.
  - "Kejatuhan dari puncak": nilai akhirnya sama dengan purata, bukan kejatuhan ekuiti ([H:1583](../BacktestShariah2/standard/dashboard_v2.html#L1583)).
  - "Paling Teruk": 87 daripada 122 kaedah beramaran. Digantikan dengan penapis "Bermasalah" ikut pantau.
  - Tapisan minimum dagangan.
  - Strip "pilih TERUSKAN".
- TURUN: "Skor kaedah swing" (35 lajur) dijadikan diagnostik dalam Profil kaedah selepas τ̂², n_eff dan pintu dibaiki. ρ ujian ramalan dipaparkan di sebelah ranking tunggal (5).
- NAIK TARAF: "Untung terkumpul lawan SPY" menjadi panel Lawan matlamat, iaitu portfolio beku lawan kawalan rawak dan SPY, kemudian lawan EW.
- PINDAH ke Profil kaedah: neraca untung & rugi, sebab keluar, untung bergerak lawan backtest, untung bulanan dan dua lorong setiap kaedah.
- PINDAH ke Lagi: MFE, unit R, grid harian, prestasi ikut gred, dan aliran isyarat (ke Sistem).
- BUANG: akaun Gabung. Moomoo lama dipindah ke Arkib (23).
- BETULKAN: TIPS `portfolio_slot` (kini lima portfolio) dan `kejatuhan`.

**Posisi → Posisi**
- NAIK TARAF: KPI kepala mengikut tapisan, mengasingkan untung direalisasi daripada belum direalisasi, dan memakai penyebut yang sama dengan segmen (22).
- TAMBAH: ringkasan kaedah yang ditapis. Isinya n, n matang, purata direalisasi lawan belum direalisasi, lorong 1 lawan lorong 2, beza SPY, kadar kena henti dan kadar dilangkau, serta pautan ke Profil (22).
- KEKAL, NAIK TARAF: jadual (24):
  - Lalai "Dipegang", disusun ikut risiko.
  - Satu takrif "hampir keluar" dalam unit ATR.
  - Gred, Trend, Pemangkin dan Kewangan dipindah ke helaian.
  - Bendera kualiti data: bar Moomoo sahaja, bar sintetik, harga beli ≠ buka, dan keluar dibuka semula.
  - Label `tidak_sah` ikut sebab (10).
  - Sasaran dinamik ditanda (15).
- KEKAL: kad telefon (dengan `hari` diselaraskan dengan jadual), dan helaian dengan carta lilin dan ulang tayang lorong 2.
- NAIK TARAF: Peta mengira saham, bukan posisi, dan memasukkan pegangan lorong 2. Ia dipindah ke pandangan Risiko bersama pendedahan sektor `posisi_c` (24).
- PINDAH: "Isyarat tidak dibeli" ke Sistem, lengkap dengan langkauan 9:35 (14).

**Watchlist → Hari Ini › Esok**
- KEKAL, NAIK TARAF: Hampir Signal (25):
  - Tambah lajur status dan kedudukan Analisis.
  - `gred_pada` diisi dengan tarikh data.
  - Nilai 100 ditulis 99.9, atau dilabel "disentuh".
  - Tanda "tiada watchlist" bagi K145+.
  - Had umur `TAMAT_WATCH` diperjelas.
- GABUNG: isyarat lengkap ke "Beli pada buka".
- BUANG: KPI "Sektor terbanyak". KPI ≥ 99% dipisahkan daripada kes disentuh.

**Backtest → Lagi › Backtest** (26)
- UBAH: label "Langsung" menjadi "Backtest beku 17 Okt · AUTOTUNE 18 Okt".
- NAIK TARAF atau BUANG: langkah 6–7 corong diselaraskan dengan Analisis.
- BUANG: lajur dan podium Papertrade C.
- Hadkan "Terbaik gaya anda" kepada varian aktif swing 3–30 hari.
- Muat papan penuh atas permintaan, tanpa 32 dokumen indikator.

**Kaedah → Profil kaedah › Cara kaedah berfungsi** (27)
- KEKAL: katalog. Betulkan pil M31 dan empat ayat pegang. Tanda lapan kaedah yang "tiada keluar, tiada had masa". Tambah ujian unit penyegerakan katalog dengan kod.
- NAIK TARAF: jalur "Sama untuk semua" dan pindahkan ke Panduan.
- GANTI: lajur Papertrade C dengan label pantau Analisis.

**Sektor → Lagi › Konteks pasaran** (28)
- NAIK TARAF: tambah gred kumpulan v2.
- BUANG: medan SST beku (atau paparkan tarikhnya), togol 1H, fasa rotasi, KPI fasa dan pendua kelas berganda (BF.A/BF.B, PBR/PBR.A).
- PINDAH: pendedahan posisi ke Posisi › Risiko.

## Struktur ramping: empat tab, kira-kira sebelas panel

Empat tab keputusan sekarang (Ringkasan, Analisis, Prestasi, Posisi) memuatkan kira-kira 38 panel, dan 22 daripadanya dalam Prestasi sahaja. Struktur di bawah mengekalkan artifact yang sama (CLAUDE.md melarang artifact baharu) dan menurunkan tiga tab utama kepada kira-kira 11 panel. Semua butiran lain dipindah ke Lagi, yang dimuat hanya atas permintaan.

```
Hari Ini   (sentiasa dibuka dahulu)
  ├ Lampu sistem + mod bayang/rasmi
  ├ Banner fasa bukti: "Belum ada kaedah terbukti" + tarikh status sebenar
  ├ Esok: jual · beli pada buka · hampir paras keluar · earnings ≤ 5 hari · sesi lalu
  └ Posisi saya: portfolio 10 slot lawan kawalan rawak dan SPY · C matang sahaja
Kaedah
  ├ Lawan matlamat + 3 penemuan
  ├ Ranking tunggal (Penganalisis dibaiki; P(5 teratas), meter bukti, pantau, ⚑)
  └ Profil kaedah (helaian): hadapan lawan jalur backtest · dua lorong · skor swing
     diagnostik · backtest (corong, S1–S4, WFO, AUTOTUNE) · cara berfungsi · posisi
Posisi
  ├ KPI ikut tapisan + ringkasan kaedah ditapis
  ├ Jadual C (Ringkas/Risiko), ikut risiko, bendera kualiti
  └ Helaian posisi + carta lilin lorong 2
Lagi   (dimuat atas permintaan)
  Sistem (saluran, ralat, isyarat tidak dibeli) · Backtest beku · Konteks pasaran
  · Analisis dagangan C · Eksperimen · Arkib Moomoo/Gabung · Panduan + makmal
```

Hari Ini hanya memerlukan `harian/status`, `analisis/papan`, `prestasi/portfolio_slot` dan satu dokumen pra-kira `harian/hari_ini`. Registry (~2 MB), autotune, Moomoo dan sektor tidak lagi dimuat setiap kali papan dibuka. Bagi mengurangkan risiko, Fasa 1 menyimpan tab lama di bawah Lagi selama seminggu supaya pengguna boleh membandingkan kedua-duanya sebelum pendua dibuang.

## Kesimpulan

Audit ini mengubah diagnosis. Papan ini tidak lemah dari segi pengiraan. Ia lemah kerana menjawab soalan "kaedah mana?" dengan data yang belum mampu menjawabnya. Setiap ranking yang dipaparkan sama ada backtest dipotong yang bergantung pada andaian rapuh, atau purata posisi muda yang didominasi oleh kelajuan kena henti. Sebab itu sembilan panel boleh betul dari segi aritmetik tetapi tetap bercanggah antara satu sama lain. Perubahan yang paling bernilai ialah membenarkan papan berkata **"belum"** dengan yakin, sambil memaparkan tarikh "ya" boleh mula dikatakan: 4 Nov bagi kaedah pertama, dan Disember bagi kebanyakan calon teratas. Inkubasi berbilang bulan seperti Darwinex GOLD (> 8 bulan) pula diperlukan sebelum saiz penuh ([Darwinex](https://help.darwinex.com/darwinia)).

Kelas ralat data yang ditemui juga menunjukkan jurang semakan yang khusus. `sahkan.py` dan CI menyemak konsistensi dalaman (bentuk, untung lawan harga), tetapi tidak menyemak sama ada data **sepadan dengan dunia luar**: buka rasmi pada hari beli, tindakan korporat yang sudah selesai, dan tarikh earnings semasa. Semakan "kebenaran luar" yang murah, iaitu harga beli lawan bar, imbasan corak harga terkunci dan `earn_seb`, akan menangkap tiga daripada empat ralat C (DAC, ACA dan 📅) sebelum ia mencemari purata kaedah. Ini lebih penting daripada sebarang rombakan visual, kerana apabila wang sebenar terlibat, satu harga beli yang salah boleh menukar kaedah yang dipilih.

## Senarai tindakan berprioriti untuk diluluskan

Tanda: **[SEGERA]** = sebelum tolakan sesi 30 Okt atau minggu ini; **[keputusan]** = menterbalikkan keputusan terdahulu atau menyentuh fail yang dilindungi CLAUDE.md, jadi perlu kelulusan jelas. Usaha: R = rendah, S = sederhana, T = tinggi.

**A. Segera: integriti data dan amaran pada nombor keputusan**

1. **[SEGERA] Bahagi `prestasi/mae` dan jadikan kegagalan jana_db per dokumen.** Tambah `mae` ke senarai bahagi `jana_db.py:578`, dan tukar pembaca halaman kepada `subBhg`. Gantikan `raise SystemExit` dengan "langkau dokumen + catat dalam `harian/status.ralat`". Tambah amaran pada 80% had (~210 KB) dan semak juga `papertrade/moomoo` (238 KB). *Sebab:* had dijangka dilepasi sekitar 30 Okt, dan ketika itu semua tolakan db akan terhenti. R.
2. **[SEGERA] Betulkan harga beli DAC M80/M90** kepada 170.19 (buka rasmi), kemudian kira semula untung akhir (−7.66%, −5.32%) dan lorong 2 (−6.96%). Tambah semakan dalam `sahkan.py`: harga beli C lawan buka bar hari beli, dengan toleransi 0.3% (M dikecualikan kerana memakai harga isian). R.
3. **[SEGERA] Tanda ACA sebagai ambil alih.** Tambah ACA ke `data/ambil_alih.csv` supaya `tidak_layak.py` menanda 8 posisi C sebagai `tidak_sah` dan menutupnya pada USD150, kemudian sahkan Lejar ikut serta. Imbas posisi terbuka untuk corak terkunci (median julat 10 bar ≤ 0.6% dan ATR Q1 < 0.5%). Kaji semula `JURANG_MIN` 10%, dan aktifkan EDGAR dengan menetapkan rahsia `SEC_USER_AGENT`. R–S.
4. **[SEGERA] Betulkan keluar lorong 2 VIAV dan LITE** (M, S04V2) dengan `keluar_lorong.py --semula henti`. Betulkan juga punca ATR yang dikira tanpa sejarah sebelum beli bagi ticker yang diambil melalui kline sahaja. R.
5. **[SEGERA] Baiki skor swing.** Kira τ̂² atas kaedah swing sahaja dengan penganggar teguh. Hadkan n_eff ke arah G (guna G apabila G < 20). Nilai pintu "≥ 20 selesai" pada lorong yang diskor. Sementara belum dibaiki, kelabukan P(untung > 0) dan "stabil", dan paparkan "0 posisi matang" serta ρ ujian ramalan di sebelah skor. S.
6. **[SEGERA] Letakkan amaran fasa pada ranking Analisis.** Banner "Kedudukan = backtest dipotong; 0 kaedah ada bukti hadapan; status sebenar pertama ±4 Nov". Betulkan label S1–S4 dan WFO serta tarikh "20 matang" (perlu 10 hari beli). Tambah bendera ⚑ DITOLAK dan "0 posisi Lejar". Susun ikut `skor_bulan` yang belum dibundar. R.
7. **[SEGERA] Buang KPI "Kaedah terbaik ikut % untung"** (M70: 0/43 dagangan selesai menang) daripada tajuk dan KPI Prestasi, serta kedua-dua strip "Cara baca … pilih TERUSKAN". Betulkan label "menang 43%" kepada "menang (semua, termasuk belum direalisasi)". R.
8. **[SEGERA] Semak jadual untuk tamat DST (1 Nov).** Tambah cetusan penjaga 15:20 UTC kepada `trig_01N3Qx…`. Sahkan bahawa tugasan beli 9:35 NY (`trig_018pfWtxtyMaC6aaThn7UDCo`) memakai zon waktu New York, bukan UTC tetap. Semak juga masa `beli.yml` dan `jangkaSesi(15)`. R.

**B. Data dan kesegaran (1–2 minggu)**

9. **Ikon 📅 memakai `earn_seb`** (atau tarikh akan datang yang paling hampir) dalam `earnH`, `statusPos` dan panel earnings ≤ 10 hari. *Sebab:* 114 posisi tiada ikon dan 32 posisi diberi ikon palsu. R.
10. **Label dan pengendalian `tidak_sah`.** Gantikan pil "Luar peraturan" dengan "Isyarat palsu (ambil alih)", "Tidak cair" atau "Kelas berganda". Betulkan subtajuk KPI dan selaraskan penyebut segmen. Pindahkan baris tidak cair dan kelas berganda ke segmen sendiri, atau tutup selepas N sesi. **[keputusan]** bagi penutupan, kerana ia mengubah peraturan `tidak_layak.py posisi`. R.
11. **Belian kelihatan pada hari yang sama.** Rutin beli menjalankan `jana_db.py` dan menolak `ringkas_c*`, bukan `claude_N`. Hentikan tolakan harian `claude_N` dan `papertrade/moomoo` (−8.9 MB sehari). Padam dokumen mati `senarai_beli*`, `papertrade/log` dan `moomoo_peta` — **[keputusan]** bagi pemadaman. R–S.
12. **Lampu sistem dan amaran kegagalan senyap.** Lampu ini:
    - menambah `ringkas_c.dibina`, `harian/trend.tarikh`, `posisi/lorong2.harga_hingga` dan tarikh SST;
    - membanding tarikh data dengan sesi NYSE yang dijangka (dengan kalendar cuti);
    - memaparkan keadaan "menunggu jadual".

    Langkah `continue-on-error` dan `try/except` perlu menulis ke `harian/status.ralat`, dan sesi tolak db menghantar PushNotification apabila `ralat` tidak kosong. S.
13. **Label sumber yang jujur dan bar boleh dihasilkan semula.** Tambah pilihan `--sumber` dan masa tarikan pada `jana_db`. Simpan bar Moomoo yang dipakai dalam repo (cth. `terkini_moomoo.csv`). Kemas kini langkah 8 `kemas_kini_0602.md` kepada "jalankan `jana_db.py` dan tolak semua batch". R.
14. **Rekod langkauan 9:35 NY sebagai baris** (~159 sejak 14 Okt), supaya "Isyarat tidak dibeli" lengkap dan kadar isyarat yang tidak boleh dilaksanakan bagi setiap kaedah dapat dikira. S.
15. **Sasaran dan MAE/MFE yang betul.** Tanda sasaran dinamik M01/M03/M28 (atau paparkan paras semasa). Simpan sasaran dagangan replika dalam Lejar dan C. Lanjutkan MAE/MFE ke tempoh lorong 2. Siasat juga beza 186 lawan 175 keluar baharu pada 23 Okt. S.

**C. KPI dan ranking (memerlukan keputusan pengguna)**

16. **[keputusan] Satu ranking sahaja.** Penganalisis yang dibaiki menjadi ranking tunggal. Bersarakan label §7 TERUSKAN/PERHATI/HENTIKAN, Skor U×S, "Terbaik ikut papertrade", "Kedudukan U×S" dan metrik USD1,000, dengan sejarahnya disimpan dalam Arkib. Ini menterbalikkan tugasan_v3 §7 (14 Okt). R.
17. **Naik taraf paparan ranking.** Gantikan "#" dengan P(5 teratas) dan selang pangkat 90%. Tambah meter bukti dan tarikh status sebenar, lajur Pantau, penunjuk ekor dan kelompok korelasi. Lajur C dan Lorong 2 disembunyikan sehingga ada data matang. S.
18. **Baiki kalibrasi pantau.** Jadikan sasaran CUSUM konsisten (winsor dengan winsor), guna bootstrap blok, letakkan pengawal bukti minimum sebelum BERSARA/AMARAN, dan paparkan sasaran serta ambang dalam %. S.
19. **KPI Ringkasan yang jujur.** Satu baris KPI sahaja: matang sahaja + % masih terbuka + selang 95% t(G−1) berkelompok hari beli + Wilson bagi kadar menang. Panel dua lorong memaparkan beza ± SE. Portfolio 10 slot dipaparkan dengan tarikh sesinya. R–S.
20. **[keputusan] Label gabungan beku sebagai SEMENTARA.** Tambah nota "dipilih atas data C belum matang; kini #35/#39/#52 dalam Analisis; P(4 teratas) M18 0.17". Fail beku tidak diubah. Bekukan semula selepas ≥ 20 hari beli matang (paling awal akhir Nov). R.
21. **Bubarkan Prestasi** mengikut senarai BUANG/TURUN/PINDAH di atas, dan betulkan TIPS `portfolio_slot` dan `kejatuhan`. S.

**D. Posisi**

22. **KPI dan Peta mengikut tapisan, ditambah ringkasan kaedah yang ditapis** (realisasi lawan belum, matang, dua lorong, beza SPY, kadar henti dan langkau). S.
23. **[keputusan] Buang akaun Gabung daripada KPI purata.** Pindahkan Moomoo lama ke Arkib, dan kecualikan `sumber=luar` serta warisan v1 daripada purata M. R.
24. **Kemas jadual Posisi.** Lalai "Dipegang" disusun ikut risiko. Guna satu takrif "hampir keluar" (ATR). Pindahkan gred, trend, pemangkin dan kewangan ke helaian **[keputusan]** (permintaan versi 34 dan 93). Tambah bendera kualiti data. Peta mengira saham, bukan posisi, dan memaparkan pendedahan sektor (`posisi_c`). S.

**E. Tab sekunder**

25. **Watchlist:** `gred_pada` = tarikh data; 99.9 atau label "disentuh"; KPI ≥ 99% dipisahkan; lajur status Analisis; tanda K145+; perjelas `TAMAT_WATCH`; isyarat lengkap digabung ke Hari Ini. R.
26. **Backtest:** label "beku"; podium dipindah dari Ringkasan dan dilabel "dalam sampel"; langkah 6–7 diselaraskan dengan Analisis atau dibuang; buang lajur dan podium Papertrade C; "Terbaik gaya" dihadkan kepada swing aktif; registry dimuat atas permintaan tanpa dokumen I. S.
27. **Kaedah:** betulkan pil M31 dan empat ayat pegang; tanda lapan kaedah "tiada keluar, tiada had masa"; kemas kini "Sama untuk semua"; tambah ujian unit katalog lawan kod; lajur Papertrade C diganti dengan label pantau Analisis. R.
28. **Sektor:** tambah gred kumpulan v2; buang medan SST beku (atau paparkan tarikhnya), 1H, fasa rotasi dan pendua kelas berganda. R.

**F. Struktur dan aliran kerja**

29. **[keputusan] Rombak lapan tab kepada empat** (Hari Ini, Kaedah, Posisi, Lagi) dalam artifact yang sama. Tab lama disimpan di bawah Lagi selama seminggu, kemudian pendua dibuang. T.
30. **[keputusan] Satu tolakan db selepas semua penghasil siap.** Selepas peralihan, `tolak_db` menunggu `beli.yml`, Lejar/Analisis sesi terakhir dan `harian.yml`. Rantai workflow melalui dispatch, dan tetapkan satu penulis `data/harga/stor`. Tukar `MOD_ACTIONS` ke `rasmi` hanya selepas pengguna dimaklumkan anjakan KPI yang dijangka (77/84 baris, 28 harga keluar). S.
31. **[keputusan] Pengawas ringan bagi tiga rutin Claude.** Rutin ini kini titik kegagalan tunggal, dan pengawas dimatikan sejak 19 Okt untuk menjimatkan token. Cadangan: satu semakan murah selepas setiap rutin, yang menyemak commit wujud dan `harian/status` maju, dan memberi notifikasi jika gagal. R.
