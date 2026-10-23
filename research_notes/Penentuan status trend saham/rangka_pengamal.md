# Rangka pengamal dan platform untuk status trend saham: Bullish / Neutral / Bearish dan skema peringkat

Disediakan 23 Okt 2026. Nota ini melanjutkan dan membetulkan `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend/nota_amalan_trend.md` (selepas ini "nota sebelum"). Bukti akademik dalam §3 nota sebelum (Brock et al., MAD, TSMOM, pembalikan jangka pendek, hentian) tidak diulang di sini. Konteks: papan swing saham AS patuh Syariah (pegangan 3–30 sesi). Takrif semasa papan: Bullish = C > SMA50 > SMA150 > SMA200, Bearish = susunan terbalik, selainnya Neutral, bertukar selepas 2 tutup berturut-turut.

**Had kaedah:** WebFetch gagal (`getaddrinfo ENOTFOUND`) dan `curl` melalui proksi ditolak (`CONNECT tunnel failed, response 403`) bagi semua domain luar, termasuk chartschool.stockcharts.com. Semua butiran diambil daripada ringkasan WebSearch atas halaman yang dipautkan. Teks penuh buku asal (Weinstein 1988, Minervini 2013, O'Neil, Elder, Wilder 1978) tidak dapat dibaca. Oleh itu angka daripada buku hanya datang melalui petikan pihak ketiga, dan ditanda sedemikian.

**Tanda jenis sumber:**
- **[DR]** dokumen rasmi pengarang atau platform (halaman bantuan, laman pengarang sendiri).
- **[SK]** sumber sekunder yang menerangkan peraturan pengarang (LuxAlgo, MQL5, TraderLion, forum, skrip TradingView pihak ketiga).
- **[KP]** konvensyen pengamal (tiada sumber asal tunggal).
- **[BK]** bukti empirikal (statistik atau kajian).
- **[IN]** inferens penulis nota.

Butiran daripada ingatan penulis yang belum disahkan diletakkan dalam bahagian *Gaps*, bukan *Cited Findings*.

---

## 1. Analisis Peringkat Weinstein: peraturan tepat Peringkat 1–4, titik mula naik (1→2) dan mula turun (3→4), dan setara carta harian

### Takeaway
Weinstein menggunakan 4 peringkat berdasarkan bar mingguan, cerun SMA 30 minggu, kedudukan harga berbanding MA itu, RS berbanding pasaran, dan trend sebelumnya (Peringkat 1 dan 3 serupa bentuknya, dan hanya dibezakan oleh trend sebelumnya). Peringkat 2 bermula pada minggu harga menembusi rintangan asas Peringkat 1 dengan volum tinggi, ketika MA 30 minggu berhenti menurun atau mula naik. Peringkat 4 bermula apabila harga pecah di bawah sokongan kawasan puncak dan berada di bawah MA yang menurun. Setara harian ialah SMA150. Ambang volum "≥ 2× purata" dan syarat "RS Mansfield > 0" hanya disokong sumber sekunder, dan belum disahkan daripada buku.

### Cited Findings
**Kerangka umum [SK]**
- Empat peringkat dibaca pada bar mingguan melalui cerun MA 30 minggu, kedudukan harga berbanding MA, dan RS berbanding pasaran. Kaedah ini diterbitkan dalam buku 1988, dengan peraturan teras: beli dalam Peringkat 2, jual atau short dalam Peringkat 4, dan berdiri di tepi dalam Peringkat 1 dan 3. Analisis dibuat dari atas ke bawah: peringkat pasaran, kemudian sektor, kemudian saham. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/); [MQL5](https://www.mql5.com/en/articles/22746)

**Peringkat 1 hingga 4 [SK]**
- **Peringkat 1 (asas):** MA 30 minggu mendatar selepas penurunan, dan harga mula bergerak mendatar di atas atau di sekitar MA. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/); [MQL5](https://www.mql5.com/en/articles/22746)
- **Peringkat 2 (naik):** harga berada di atas MA 30 minggu yang sedang naik. MA berpusing naik ketika tembusan berlaku, dan inilah satu-satunya peringkat untuk membeli. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/); senarai semak pengamal yang mensyaratkan SMA 30 minggu naik: [TradingView DIVISLAB](https://in.tradingview.com/chart/DIVISLAB/jofJTfN1-DIVISLAB-Stage-2-Breakout/)
- **Volum tembusan (sumber bercanggah):**
  - MQL5: tutup di atas rintangan Peringkat 1 dengan volum **≥ 2× purata baru-baru ini**. — [MQL5](https://www.mql5.com/en/articles/22746)
  - Sumber lain: tutup mingguan di atas siling asas dengan **≥ 1.5× median volum**, iaitu ambang rangka pengarang lain.
  - Ada juga sumber yang hanya menyebut "volum lebih tinggi daripada biasa". — [Incredible Charts, Breakout Model](https://www.incrediblecharts.com/technical/breakout_model.php)
  - Ringkasan carian menyimpulkan bahawa "2×" ialah ambang seorang pengamal, bukan piawai sejagat.
- **Peringkat 3 (puncak):** harga kembali mendatar dan MA 30 minggu menjadi rata selepas kenaikan. Ini menandakan pengagihan dan kehilangan momentum. Tanda pertama Peringkat 3, iaitu harga pecah di bawah MA 30 minggu dengan volum tinggi atau MA mula rata selepas kenaikan panjang, dijadikan isyarat keluar. — [MQL5](https://www.mql5.com/en/articles/22746); [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)
- **Peringkat 4 (turun):** "disahkan apabila harga pecah di bawah sokongan kawasan puncak dan kekal di bawah MA 30 minggu yang menurun". Short dimasuki pada pecahan sokongan Peringkat 3 dan dikeluarkan apabila Peringkat 1 mula terbentuk. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/); [MQL5](https://www.mql5.com/en/articles/22746)
- Ringkasan buku: potong rugi dengan cepat apabila saham jatuh di bawah sokongan utama atau MA. — [TrendSpider blog](https://trendspider.com/blog/master-market-trends-with-ai-powered-weinstein-stage-analysis/)

**RS Mansfield [SK]**
- Weinstein menggunakan bentuk Mansfield: nisbah saham/indeks yang dinormalkan dengan purata 52 minggunya sendiri, supaya berayun di sekitar sifar. Calon beli sepatutnya positif atau sedang bertukar positif. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)
- Skrip "Mansfield RS (Original Version) by stageanalysis":
  - garis sifar = MA 52 minggu bagi garis RS, yang "diratakan" menjadi oscillator;
  - lintasan ke atas garis sifar = mengatasi indeks;
  - satu versi mengira harga harian saham ÷ tutup mingguan SPX, dinormalkan dengan SMA 52 minggu nisbah itu.
  — [TradingView](https://www.tradingview.com/script/NzUBDDtb-Mansfield-Relative-Strength-Original-Version-by-stageanalysis)
- Ringkasan carian lain mendapati syarat "Mansfield RS > 0" muncul dalam senarai semak TradingView, tetapi tiada sumber yang mengaitkannya dengan buku. Syarat itu mungkin tambahan pengamal kemudian. — [MQL5](https://www.mql5.com/en/articles/22746); [TradingView DIVISLAB](https://in.tradingview.com/chart/DIVISLAB/jofJTfN1-DIVISLAB-Stage-2-Breakout/)

**Setara harian dan kaveat**
- Minervini menulis "the 150-day (30-week) and the 200-day (40-week) moving average". Ini konvensyen bahawa SMA150 harian ≈ SMA 30 minggu. [SK] — [ProRealCode, Trend Template](https://www.prorealcode.com/prorealtime-market-screeners/trend-template-mark-minervini/?pnum=12)
- Kaveat: kaedah ini deskriptif dan lambat secara reka bentuk. Tembusan Peringkat 2 boleh gagal dan kembali ke asas. Nilainya pada disiplin (menjauhkan modal daripada carta menurun), bukan ketepatan di titik pusingan. [SK] — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)

### Inferences
- **[IN] Takrif papan sekarang ≈ "Peringkat 2 matang", bukan "mula naik".** Selepas tembusan Peringkat 1→2, SMA50 perlu melintasi SMA150 dahulu, kemudian SMA150 perlu melintasi SMA200. Kedua-dua lintasan ini mengambil masa berminggu hingga berbulan. Akibatnya, saham pada Peringkat 2 awal kebanyakannya kekal **Neutral** di bawah takrif semasa. Hal yang sama berlaku pada Bearish, yang hanya muncul dalam Peringkat 4 matang.
- **[IN] Peringkat 1 dan 3 tidak boleh dibezakan tanpa ingatan laluan.** Kedua-duanya mempunyai MA rata dan harga bersilang-silang. Label yang hanya melihat bar hari ini tidak dapat memisahkannya. Peraturan Weinstein memerlukan mesin keadaan (keadaan sebelumnya menentukan nama keadaan sekarang).
- **[IN] Ufuk:** perubahan peringkat mingguan jarang berlaku dalam 3–30 sesi. Weinstein lebih sesuai sebagai konteks atau penapis watchlist berbanding pencetus pegang/jual harian.
- **[IN] Versi harian untuk diuji (bukan peraturan Weinstein):**
  - MA = SMA150, cerun = SMA150_t − SMA150_{t−20}, dan "rata" = |cerun| / ATR14 < ambang;
  - tembusan = C > tertinggi kawasan asas (50–150 hari) dengan volum ≥ 1.5–2× purata 50 hari;
  - Peringkat 4 = C < terendah kawasan puncak dengan cerun SMA150 < 0.

### Gaps
- Teks asal *Secrets for Profiting in Bull and Bear Markets* tidak dapat dibaca. Tiga perkara belum disahkan: (a) ambang volum tepat; (b) sama ada RS Mansfield sebahagian peraturan asal; (c) takrif kuantitatif "rata".
- Daripada ingatan (belum disahkan dalam sesi ini):
  - Weinstein membezakan *initial buy* (tembusan 1→2) dan *continuation buy* (tarikan semula dalam Peringkat 2 ke paras di atas MA).
  - Beliau menyatakan volum **tidak diperlukan** untuk mengesahkan pecahan ke bawah (Peringkat 4).
  - Beliau melarang membeli saham di bawah MA 30 minggu yang menurun.
- Sub-peringkat (cth. 1A/1B, 2A/2B) yang digunakan sesetengah laman pengamal tidak ditemui. Carian "stageanalysis.net stage 2A" hanya memulangkan hasil perubatan.

---

## 2. Templat Trend Minervini, O'Neil/IBD, Teori Dow dan Wyckoff: peraturan, titik mula dan titik tamat trend

### Takeaway
- **Minervini:** binari (8 syarat lulus/gagal). Takrif papan semasa sama dengan syarat MA 1, 2, 4 dan 5 templat ini, tanpa cerun SMA200, jarak 52 minggu dan RS.
- **IBD:** mentakrif titik mula trend **pasaran** sebagai *follow-through day* (hari ke-4 atau kemudian dalam cubaan pulih, naik ≥ ~1.25% dengan volum lebih tinggi). Trend dilemahkan oleh kiraan *distribution day* dalam 25 sesi. Pada peringkat saham, IBD mengira "peringkat asas" untuk mengukur umur trend.
- **Teori Dow:** trend = puncak dan lembah lebih tinggi. Pembalikan memerlukan sekurang-kurangnya satu puncak lebih rendah **dan** satu lembah lebih rendah, disahkan oleh dua purata.
- **Wyckoff:** fasa A–E dengan peristiwa bernama (SC, AR, ST, Spring, SOS, LPS), tetapi tanpa ambang angka.

### Cited Findings
**Minervini Trend Template** (diterangkan sumber sekunder yang menyalin senarai buku *Trade Like a Stock Market Wizard*) [SK]

| # | Syarat |
|---|---|
| 1 | C > SMA150 dan C > SMA200 |
| 2 | SMA150 > SMA200 |
| 3 | SMA200 naik sekurang-kurangnya 1 bulan (sebaiknya ≥ 4–5 bulan) |
| 4 | SMA50 > SMA150 dan SMA50 > SMA200 |
| 5 | C > SMA50 |
| 6 | C ≥ 30% di atas paras terendah 52 minggu |
| 7 | C dalam lingkungan 25% daripada paras tertinggi 52 minggu ("lebih dekat lebih baik") |
| 8 | Ranking RS IBD ≥ 70, sebaiknya 80-an atau 90-an |

- Sumber syarat 1–6: [ProRealCode](https://www.prorealcode.com/prorealtime-market-screeners/trend-template-mark-minervini/?pnum=12); [TradingView Trend Template](https://www.tradingview.com/script/22JWROvE-Mark-Minervini-s-Trend-Template)
- Sumber syarat 7–8: [EliteTrader](https://elitetrader.com/et/threads/mark-minervinis-trend-template-question.359356/post-5400734); [Action Alerts](https://actionalerts.substack.com/p/using-mark-minervinis-trend-template)
- Varian skrip: sesetengah skrip menggunakan 25% (bukan 30%) untuk syarat 6 dan "RS > 70" (ketat, bukan ≥). — [TradingView "Stage 2 with RS"](https://kr.tradingview.com/script/8qRq62fU-Raj-Mark-Minervini-Stage-2-with-RS)
- **Pembetulan nota sebelum:** jadual §1.1 menulis "C ≥ 25–30% di atas paras terendah 52 minggu". Senarai yang memetik buku menyatakan **30%**, manakala 25% ialah varian skrip.

**O'Neil / IBD: follow-through day (FTD) dan keadaan pasaran** [SK]
- **Cubaan pulih:**
  - Hari 1 = sesi pertama indeks ditutup lebih tinggi selepas paras terendah pembetulan yang baharu.
  - Cubaan kekal sah selagi indeks tidak melanggar paras terendah Hari 1. Jika dilanggar, kiraan bermula semula.
- **FTD:**
  - Mulai Hari 4: kenaikan ≥ ambang pada Nasdaq Composite atau S&P 500 (satu indeks memadai), dengan volum melebihi sesi sebelumnya.
  - O'Neil mendapati FTD terkuat berlaku pada hari 4–7.
- **Ambang kenaikan (sumber bercanggah):** asalnya 1%, kemudian dinaikkan; IBD menggunakan 1.7% sekitar pertengahan 2000-an; huraian terkini lazimnya ~1.25%. Semak kriteria semasa IBD.
- **Kadar kejayaan [BK lemah]:** IBD menyatakan tidak semua FTD membawa kepada trend naik, tetapi tiada rali besar yang bermula tanpa FTD. Satu ringkasan kajian menyatakan "separuh hingga dua pertiga" FTD membawa kepada trend naik berterusan. Metodologi kajian tidak dilihat.
- Sumber FTD: [LuxAlgo, Follow-through Day](https://www.luxalgo.com/library/concept/follow-through-day/); [StockCharts, "A Proven Technique That's Identified Every Market Bottom"](https://articles.stockcharts.com/article/a-proven-technique-that-identifies-every-market-bottom/); [Seeking Alpha](https://seekingalpha.com/instablog/195752-joshua-hayes/73173-a-quick-reminder-about-follow-through-days); [TradingView, Distribution & Follow-Through Days](https://www.tradingview.com/chart/SPY/6bvzu45q-Distribution-Follow-Through-Days)
- **Distribution day:**
  - Hari pengagihan gugur daripada kiraan selepas **25 sesi**, atau selepas indeks naik **5%** di atas tutup hari itu.
  - Kiraan 2–3 dianggap biasa dalam *Confirmed Uptrend*. Kiraan 5–6 bermakna perlu bersedia memangkas posisi. — [MarketSmith India blog](https://blog.marketsmithindia.com/?p=4789)
  - Sumber ini blog tentang Nifty 50, bukan dokumen IBD AS.
- **Kitaran keadaan:** *Uptrend under pressure* ialah keadaan berhati-hati. Hari pengagihan sama ada luput mengikut masa atau terkumpul sehingga IBD mengisytiharkan *Market in correction* secara rasmi. Selepas itu kiraan tidak digunakan sehingga FTD baharu. — [Motley Fool forum](https://discussion.fool.com/t/ot-ibd-uptrend-under-pressure/37892); [useThinkScript](https://usethinkscript.com/threads/ibd-distribution-days-study-for-thinkorswim.748/post-39978)
- **Peringkat asas saham (MarketSmith/IBD):**
  - Peringkat bermula pada 1 dan bertambah dengan setiap asas baharu.
  - Jika pergerakan dari titik pivot asas sebelumnya ke puncak sisi kiri asas baharu ≥ 20%, peringkat naik secara angka (1 → 2). Jika < 20%, peringkat naik secara huruf (1a → 1b).
  - Kiraan diset semula ke 1 apabila paras terendah intrahari melanggar paras terendah asas sebelumnya.
  - — [MarketSmith India blog](https://blog.marketsmithindia.com/?p=5476)
- **Titik beli:** forum menyebut IBD menganggap titik beli tidak sah jika saham gagal sehingga 7–8% di bawah pivot. "Jangan kejar > 5% di atas pivot" dan "volum tembusan ≥ 40–50% di atas purata" hanya ditemui dalam sumber berkualiti rendah. — [Motley Fool forum "Trading IBD Stocks"](https://discussion.fool.com/t/trading-ibd-stocks/104584?page=18)

**Teori Dow** [SK]
- Trend naik ialah siri puncak dan lembah lebih tinggi. Untuk berbalik, mesti ada sekurang-kurangnya **satu puncak lebih rendah dan satu lembah lebih rendah** (sebaliknya bagi trend turun). — [ThisMatter](https://thismatter.com/money/technical-analysis/dow-theory.htm); [BabyPips](https://www.babypips.com/forexpedia/dow-theory)
- Trend primer hanya sah jika disahkan oleh DJIA **dan** Dow Jones Transportation Average yang bergerak sehala. Dow mengabaikan pergerakan satu purata yang tidak disahkan purata satu lagi. Kini sesetengah pengamal menggunakan S&P 500 dan Russell 2000. — [ThisMatter](https://thismatter.com/money/technical-analysis/dow-theory.htm)
- Volum hanya untuk mengesahkan situasi tidak jelas, dan dianggap kurang penting daripada trend primer serta pengesahan dua purata. — [BabyPips](https://www.babypips.com/forexpedia/dow-theory); [Bookmap](https://bookmap.com/blog/understanding-dow-theory-the-foundation-of-modern-market-analysis)
- Kelemahan: pengesahan trend lewat berbanding permulaan sebenar pergerakan. Semakin lama trend berterusan, semakin kecil kebarangkalian ia kekal. — [ThisMatter](https://thismatter.com/money/technical-analysis/dow-theory.htm)

**Wyckoff** [SK]
- **Fasa A:** menghentikan penurunan dan mentakrif julat dagangan melalui PS (*preliminary support*), SC (*selling climax*), AR (*automatic rally*) dan ST (*secondary test*).
- **Fasa B:** pembinaan julat.
- **Fasa C:** ujian terakhir, sama ada *spring* (paras terendah baharu kecil) atau LPS dengan lembah lebih tinggi sebelum markup.
- **Fasa D:**
  - SOS (*sign of strength*): kenaikan dengan julat bar melebar dan volum relatif lebih tinggi, menembusi sementara puncak terdahulu atau rintangan;
  - LPS (*last point of support*): lembah tarikan semula selepas SOS, termasuk *back-up* selepas tembusan.
- **Fasa E:** markup, iaitu trend keluar dari julat.
- — [LuxAlgo, Wyckoff Accumulation Schematic](https://www.luxalgo.com/library/concept/wyckoff-accumulation-schematic/); [StockCharts, Wyckoff Buy Strategies](https://articles.stockcharts.com/article/articles-wyckoff-2016-04-wyckoff-buy-strategies/); [LuxAlgo blog](https://www.luxalgo.com/blog/wyckoff-accumulation-a-pattern-essentials-guide)
- Skema ini ialah "urutan dan kosa kata, bukan templat yang mesti dipatuhi harga". Julat sebenar sering berbeza daripada buku teks. — [LuxAlgo](https://www.luxalgo.com/library/concept/wyckoff-accumulation-schematic/)

### Inferences
- **[IN] Takrif papan Bullish ≡ syarat 1, 2, 4 dan 5 Minervini.** Susunan C > 50 > 150 > 200 secara automatik memenuhi C > 150, C > 200 dan 50 > 200. Takrif ini tidak memasukkan syarat 3 (cerun SMA200, iaitu syarat "umur"), syarat 6–7 (kedudukan dalam julat 52 minggu) dan syarat 8 (RS). Papan sudah mempunyai RS pasaran (`data/rs/`), jadi syarat 8 boleh diuji sebagai lapisan berasingan.
- **[IN] "Mula naik" ditakrif oleh peristiwa, bukan susunan MA.** Weinstein (tembusan 1→2), Wyckoff (SOS Fasa D), IBD (FTD, tembusan asas) dan Dow (puncak lebih tinggi pertama selepas lembah lebih tinggi) semuanya menetapkan permulaan trend pada **peristiwa tembusan struktur**. Susunan MA penuh dicapai jauh lebih lewat.
- **[IN] Logik FTD boleh disesuaikan kepada saham sebagai templat "pengesahan":** kira dari paras terendah baharu, tunggu minimum 4 hari, kemudian syaratkan kenaikan ≥ k×ATR dengan volum lebih tinggi. Perlu ujian sendiri. IBD hanya mendokumenkannya untuk indeks.
- **[IN] Kesesuaian swing (3–30 hari):**
  - Templat Minervini ialah penapis perlahan (SMA200 naik ≥ 22 sesi), sesuai untuk watchlist.
  - FTD/distribution ialah lapisan rejim pasaran (beberapa hari hingga minggu).
  - Struktur Dow dengan pivot ayunan harian (cth. pivot 5 bar) dan peringkat asas IBD sesuai untuk ufuk swing.
  - Wyckoff terlalu budi bicara untuk label automatik.

### Gaps
- Teks buku Minervini, O'Neil dan Hamilton/Rhea tidak dibaca terus. Ketiga-tiga perkara berikut belum disahkan daripada dokumen IBD rasmi:
  - takrif tepat distribution day (lazimnya disebut: indeks jatuh ≥ 0.2% dengan volum lebih tinggi daripada sesi sebelumnya; ini daripada pengetahuan umum yang ditanda ringkasan carian sebagai tidak disahkan);
  - ambang FTD semasa;
  - peraturan 5% titik beli.
- Daripada ingatan (belum disahkan):
  - Teori Dow mempunyai tiga darjah trend (primer berbulan–bertahun; sekunder 3 minggu–3 bulan yang mengunjur balik 1/3–2/3; minor < 3 minggu) dan tiga fasa trend primer (pengumpulan, penyertaan awam, pengagihan).
  - O'Neil menyatakan asas peringkat lewat (ke-3/ke-4) lebih kerap gagal.
- Tiada sumber IBD rasmi ditemui yang menerangkan label trend **saham individu** (selain peringkat asas dan RS).

---

## 3. Sistem Elder (Impulse, Triple Screen), Ichimoku, ADX/DMI, Supertrend, susunan MA dan rangka swing 10/20 EMA

### Takeaway
- **Rangka asli swing** menggunakan tetingkap 10–26 hari. Contohnya Elder Impulse (EMA13 + histogram MACD), Supertrend (ATR10 × 3), Ichimoku harian (9/26/52), kitaran harga Kell (EMA 10/20) dan Qullamaggie (SMA 10/20 sebagai hentian ekor). Kebanyakannya berubah dengan cepat, jadi digunakan sebagai **penapis atau penapis arah** (Elder: "censorship") atau **hentian ekor**, bukan label konteks yang stabil.
- **ADX/DMI** memisahkan arah (+DI lawan −DI) daripada kekuatan (ADX 20/25). Ambang itu konvensyen, dan sumber bercanggah sama ada Wilder memakainya pada ADX atau ADXR.

### Cited Findings
**Elder Impulse System [DR/SK]**
- EMA 13 tempoh (inersia) dan histogram MACD(12,26,9) (momentum), setiap satu dibanding dengan bar sebelumnya:
  - **Hijau** = kedua-duanya naik;
  - **Merah** = kedua-duanya turun;
  - **Biru** = selainnya (bercanggah).
  — [Barchart, Elder Impulse System](https://barchartsolutions.atlassian.net/wiki/x/k4E5QQ); [StockCharts ChartWatchers 2012](https://articles.stockcharts.com/article/articles-chartwatchers-2012-01-digging-deeper-into-elders-impulse-system/)
- Fungsinya penapis ("censorship"): hijau melarang short baharu, merah melarang belian baharu, biru membenarkan kedua-dua arah. Penapisan Elder paling baik digunakan pada kerangka masa lebih tinggi. — [TradingView, Elder Unified/Triple Screen scripts](https://www.tradingview.com/scripts/triplescreen/); [LuxAlgo](https://www.luxalgo.com/library/indicator/elder-impulse-system/)

**Elder Triple Screen [SK, bercanggah]**
- **Skrin pertama ("tide", kerangka lebih panjang):** sumber tidak sepakat tentang penunjuknya:
  - cerun EMA 13 minggu (atau EMA 26 minggu sebagai alternatif);
  - atau cerun histogram MACD mingguan.
  - Cerun naik = long sahaja, turun = short sahaja, rata = tiada dagangan.
- **Skrin kedua ("wave"):** oscillator harian untuk tarikan semula, seperti Force Index (EMA 2 hari), Elder-Ray atau Stochastic 13.
- **Skrin ketiga ("ripple"):** pencetus masuk.
- MACD mingguan lebih boleh dipercayai tetapi lewat.
- — [TakeProfit](https://takeprofitapp.com/en/learn/triple-screen-trading-system); [RoboForex](https://roboforex.com/blog/education/triple-screen-trading-system-how-to/); [Incredible Charts, MACD Histogram](https://www.incrediblecharts.com/technical/macd_and_histogram.php)
- **Pembetulan nota sebelum:** nota itu menulis "Elder: EMA 13 minggu". Sumber yang ditemui menyebut sama ada EMA 13 minggu, EMA 26 minggu atau cerun histogram MACD mingguan, dan perkara ini belum dapat dipastikan daripada buku.

**Ichimoku [SK; tafsiran lazim, bukan piawai]**
- Lalai 9/26/52.
- Kedudukan harga berbanding awan:
  - di atas awan = bullish;
  - di bawah awan = bearish;
  - di dalam awan = tidak pasti, peralihan atau mendatar.
- Warna awan: Senkou A > Senkou B = momentum naik.
- Silang Tenkan/Kijun paling kuat jika berlaku di atas awan (bullish) atau di bawah awan (bearish). Tembusan menembusi awan dianggap lebih kuat daripada silang sahaja.
- Chikou di atas harga 26 tempoh lalu menyokong bullish.
- — [Capital.com](https://capital.com/en-gb/learn/technical-analysis/ichimoku-cloud-strategy); [TradingView, TradingFinder Ichimoku](https://kr.tradingview.com/script/nGMFfXHI-Ichimoku-Cloud-Indicator-TradingFinder-Kinko-Hyo-Cross-Alerts)

**ADX/DMI (Wilder; tempoh lalai 14) [SK, bercanggah]**
- **Arah:** positif apabila +DI > −DI. Silang +DI di atas −DI = isyarat beli atau kemungkinan perubahan trend.
- **Kekuatan:** ADX tidak berarah. ADX > 25 = trend kuat; sesetengah pedagang guna 20 untuk isyarat lebih cepat; ADX melintas ke atas 20 = "trend baharu muncul"; ADX < 20 = trend lemah. — [Fidelity](https://www.fidelity.com/viewpoints/active-investor/average-directional-index-adx); [Interactive Brokers](https://www.interactivebrokers.com/campus/trading-lessons/adx-dmi/); [BabyPips](https://www.babypips.com/learn/forex/average-directional-index)
- **Kaufman:** "ADX melintas ke atas 25 = pasaran trending; melintas ke bawah 20 = konsolidasi". Ini mewujudkan jalur histeresis 20–25. — [Technical Analysis of Stocks & Commodities (petikan Kaufman)](https://technical.traders.com/tradersonline/display.asp?art=8229)
- **Dakwaan sekunder tentang buku Wilder 1978:** ambang 25/20 sepatutnya dipakai pada **ADXR**, bukan ADX. Sistem trend menguntungkan pada ADXR > 25 dan perlu berhenti pada ADXR < 20, serta berhenti apabila kedua-dua DI berada di atas ADX. *Extreme Point Rule*: pada silang DI, paras tinggi/rendah bar silang dijadikan titik pembalikan, dan pembalikan hanya berlaku jika paras itu ditembusi. — [TradingView, "ADX w/ Wilder's DI/DX/ADXR/Equilibrium Point"](https://de.tradingview.com/script/R3YRg9EF-adx-w-wilders-di-di-dx-adxr-equilibrium-point)
- **Pembetulan/penambahan nota sebelum:** nota itu menulis "Wilder menganggap trend berkembang pada ADX 25". Status ADX lawan ADXR dalam buku asal **belum disahkan**.

**Supertrend [SK]**
- Lalai ATR 10 dan gandaan 3. ATR menggunakan pelicinan RMA (Wilder) dalam pelaksanaan TradingView, dengan SMA sebagai alternatif.
- Jalur = (H+L)/2 ± gandaan × ATR.
- — [TradingView Supertrend script](https://www.tradingview.com/script/r6dAP7yi); [StockSharp](https://doc.stocksharp.com/ja/api-examples/0010_Super_Trend); [contoh kod](https://glama.ai/mcp/servers/@kea0811/ig-trading-mcp/blob/96c81c5c64e1fc9dc850e3d8a8fc6a1c90203e0f/src/indicators/supertrend.js)
- Hanya 2 keadaan, tiada neutral (nota sebelum §1.1).

**Kitaran harga Oliver Kell (EMA 10 dan 20 hari) [SK]**
1. **Reversal Extension:** kapitulasi jauh di bawah MA dengan volum berat; tanda kemungkinan pembalikan.
2. **Wedge Pop:** titik pertama harga kembali melepasi MA dan menembusi rintangan jangka pendek; risiko jelas.
3. **EMA Crossback:** ujian semula EMA 10/20 selepas Wedge Pop.
4. **Base n' Break:** tarikan semula singkat ke MA ketika harga sudah di atas MA dan dekat paras tinggi, kemudian tembusan pivot.
5. **Exhaustion Extension:** "selepas dua Base n' Break, anda lewat dalam kitaran jangka sederhana".
6. **Wedge Drop:** cerminan Wedge Pop di sisi bawah.

— [TraderLion, Cycle of Price Action](https://traderlion.com/technical-analysis/chart-patterns/cycle-of-price-action-by-oliver-kell/); [TraderLion, EMA Crossback](https://traderlion.com/technical-analysis/chart-patterns/ema-crossback/); [TraderLion, Base n' Break](https://traderlion.com/technical-analysis/chart-patterns/base-n-break-how-to-catch-breakouts/)

- Tiada ambang angka "exhaustion" yang diterbitkan oleh Kell. Skrip pihak ketiga mengukurnya sebagai % jarak dari EMA10 bersama puncak volum. — [TradingView, Oliver Kell Cycle of Price Action](https://vn.tradingview.com/script/xHyBTcMq-Oliver-Kell-Cycle-of-Price-Action)

**Qullamaggie (Kristjan Kullamägi) [SK]**
- **Pemilihan calon:** 1–2% teratas prestasi 1, 3 dan 6 bulan, dengan pergerakan 30–100%+ dalam 1–3 bulan lalu.
- **Bentuk tarikan semula:** teratur, dengan lembah lebih tinggi dan julat mengetat, harga "meluncur" di atas SMA 10/20 hari (kadang-kadang 50). Konsolidasi berlangsung 2 minggu hingga 2 bulan.
- **Masuk:** tembusan.
- **Hentian:** paras rendah hari itu, tidak melebihi ATR/ADR.
- **Keluar:** jual sebahagian selepas beberapa hari, dan baki diekor dengan SMA10 (saham pantas) atau SMA20 (lebih perlahan). Keluar apabila tutup di bawah MA itu.
- — [Substack, Qullamaggie Swing Trading Setups](https://tikamalma.substack.com/p/qullamaggie-swing-trading-setups)
- Skrip pihak ketiga menambah ADR ≥ 6%, SMA10 > SMA21, harga dalam ±3% SMA10, dan "jangan beli di bawah MA50". — [TradingView, Qullamaggie Trading System Pro](https://fr.tradingview.com/script/iQtlXxO8-Qullamaggie-Trading-System-Pro)

**Trend Composite Arthur Hill (TrendInvestorPro; plugin StockCharts ACP) [DR]**
- Lima penunjuk, setiap satu ±1: Bollinger Bands(125,1), Keltner Channels(125,2), ROC 5 hari bagi SMA125, StochClose(125,5) dan CCI-Close(125).
- Julat −5 hingga +5, **sentiasa ganjil**, jadi tiada nilai 0 dan tiada neutral.
- — [TrendInvestorPro](https://trendinvestorpro.com/trend-composite-signal-table-for-sp-500-stocks-free/print/)
- Skrip TradingView yang menggunakan nama yang sama mempunyai komponen berbeza (harga lawan SMA100/200, 50 lawan 200, cerun SMA200, dan MACD). Skrip itu bukan definisi Hill. — [TradingView "Trend Composite (Auto 125d)"](https://jp.tradingview.com/script/uLmwZjmG-Trend-Composite-Auto-125d-Daily-Overlay)

### Inferences
- **[IN] Dua keluarga rangka:**
  - *Rangka konteks* (Weinstein, Minervini, SST, Hill 125 hari, SCTR) menggunakan 50–200 hari, jarang bertukar, dan sesuai untuk watchlist serta "trend masih menyokong?".
  - *Rangka swing* (Elder Impulse harian, Supertrend 10×3, Kell 10/20 EMA, Qullamaggie SMA10/20) digunakan pengamal sendiri sebagai **hentian ekor** atau **penapis arah**, bukan label konteks.
  - Papan sudah mempunyai hentian ekor sendiri (Chandelier 4×ATR14). Oleh itu label swing pantas akan bertindih dengan lorong 2 dan menambah *flip-flop*.
- **[IN] Jalur histeresis Kaufman** (masuk > 25, keluar < 20) dan **peraturan Extreme Point Wilder** (pembalikan hanya jika paras bar silang ditembusi) ialah dua contoh terdokumen pengesahan bukan berasaskan bilangan hari. Kedua-duanya boleh dibanding dengan peraturan "2 tutup berturut-turut" papan.
- **[IN] Hill memilih bilangan penunjuk ganjil** supaya label sentiasa membuat keputusan (tiada neutral). Ini pilihan reka bentuk bertentangan dengan pendekatan jalur neutral.
- **[IN] Kesesuaian swing 3–30 hari:**
  - Elder Impulse harian (EMA13 ≈ 2.5 minggu): sesuai, tetapi berubah setiap bar.
  - Ichimoku harian (Kijun 26 ≈ 5 minggu): sesuai.
  - ADX14: sesuai tetapi lewat.
  - Supertrend 10×3: sesuai sebagai hentian.
  - Kell dan Qullamaggie: direka khusus untuk swing (beberapa hari hingga beberapa minggu).
  - Triple Screen: kerangka trend 4–5× kerangka dagangan (nota sebelum). Bagi pegangan ~10 hari, ini ≈ 40–65 hari, iaitu paksi 50 hari.

### Gaps
- Butiran logik flip Supertrend tidak disahkan daripada sumber dalam sesi ini. Daripada pengetahuan umum: jalur akhir hanya mengetat ke arah trend, dan trend bertukar apabila tutup melintasi jalur akhir yang bertentangan.
- Klasifikasi klasik silang TK "kuat / neutral / lemah" (di atas / di dalam / di bawah awan) hanya disokong sebahagian oleh sumber yang ditemui.
- Teks Wilder 1978 dan buku Elder (*Come Into My Trading Room*) tidak dibaca. Isu ADX lawan ADXR dan penunjuk skrin pertama Triple Screen masih terbuka.
- ChartSchool StockCharts (ADX, Ichimoku, Elder Impulse, Weinstein) tidak dapat diakses kerana domain disekat.

---

## 4. Label platform: komponen dan tetingkap bagi TradingView, StockCharts, Barchart, Finviz, Morningstar/Trading Central, IBD dan lain-lain

### Takeaway
- **Platform runcit** menerbitkan dua jenis label:
  - (a) **penarafan gabungan undi** 5–7 tahap (TradingView 26 penunjuk; Barchart 13 penunjuk dengan tiga ufuk ~20/~50/100–200 hari);
  - (b) **label peristiwa atau ufuk** 3 keadaan (Trading Central: 2–6 minggu / 6–39 minggu / 9 bulan–2+ tahun; moomoo).
- **Barchart** ialah satu-satunya yang ditemui yang menerbitkan **arah perubahan** label: Signal Direction 3 sesi, termasuk "Rising/Falling" dalam keadaan Hold. Ini sebenarnya keadaan "mula naik / mula turun" di dalam neutral.
- **Finviz:** tiada pengesahan dalam sesi ini.
- **Morningstar:** tiada label trend teknikal (fundamental sahaja; nota sebelum).

### Cited Findings
**TradingView Technical Ratings [DR]** — mengesahkan nota sebelum.
- Skor kepada kategori:

| Kategori | Julat skor |
|---|---|
| Strong Sell | < −0.5 |
| Sell | [−0.5, −0.1) |
| Neutral | [−0.1, 0.1] |
| Buy | (0.1, 0.5] |
| Strong Buy | > 0.5 |

- Skor ialah agregat 26 penunjuk. MA dikira "beli" apabila nilai MA < harga.
- Tiga paparan: All, MAs dan Oscillators; keseluruhan dipaparkan secara lalai.
- — [TradingView Help Center](https://in.tradingview.com/support/solutions/43000614331)
- Skrip komuniti yang memberi pemberat berbeza kepada MAs/Oscillators tidak selalu sepadan dengan tolok "Technicals" rasmi. — [TradingView Technical Ratings script](https://de.tradingview.com/script/Jdw7wW2g-Technical-Ratings); [TechnicalRating library](https://www.tradingview.com/script/jDWyb5PG-TechnicalRating/)

**Barchart Opinion [DR]**
- **Pengiraan:** sehingga 5 tahun sejarah harga melalui 13 penunjuk. Setiap penunjuk memberi Buy = +1, Sell = −1 atau Hold = 0, dan isyarat utama ialah purata. Kumpulan ditandakan sebagai:
  - pendek ≈ 20 hari terakhir;
  - sederhana ≈ 50 hari;
  - panjang ≈ 100–200 hari;
  - Trend Seeker® dalam kumpulan sendiri sebagai komposit pergerakan harga.
  — [Barchart Opinion](https://www.barchart.com/stocks/quotes/Q/opinion)
- **Versi "legacy"** menggunakan set 13 penunjuk yang berbeza: 5 pendek, 4 sederhana dan 3 panjang. Ia masih boleh dicapai bagi saham, ETF, forex dan dana. — [Barchart Opinion Legacy](https://www.barchart.com/stocks/quotes/J/opinion-legacy)
- **Signal Strength:**
  - bacaan jangka panjang yang membanding isyarat semasa dengan sejarahnya sendiri (Minimum…Maximum);
  - isyarat lebih kuat lebih jarang bertukar;
  - Hold tiada kekuatan.
  — [Barchart Signals Direction](https://barchart.com/stocks/signals/direction)
- **Signal Direction:**
  - ukuran jangka pendek **3 sesi**: perbezaan semasa dibanding dengan tiga sesi dagangan terdekat (melebar = menguat; menyempit = melemah);
  - label Buy/Sell: Strongest, Strengthening, Average, Weakening, Weakest;
  - label **Hold: Bullish, Rising, Steady, Falling, Bearish**, yang menunjukkan sama ada Hold sedang hanyut ke arah Buy atau Sell.
  — [Barchart Signals Direction](https://www.barchart.com/au/stocks/signals/direction); [Barchart opinion page](https://www.barchart.com/crypto/quotes/^BTCUSD/opinion); [About Barchart Opinions](https://www.barchart.com/trader/help/technical_opinion/opinions.php)
- **Pembetulan nota sebelum §2.3:** senarai komponen di sana (ADX 7 hari, HiLo MA 10-8, MACD 20-50, dan lain-lain) diambil daripada tangkapan forum. Pengelompokan 5/4/3 itu sepadan dengan set **legacy**, bukan set semasa. Pemetaan peratus kepada 7 label (≈ 33%/66%) juga **belum disahkan** daripada dokumen rasmi.

**Trading Central Technical Insight** (Fidelity, IBKR, Webull) [DR]
- **Ufuk semasa:** pendek ≈ 2–6 minggu, pertengahan ≈ 6–39 minggu, panjang 9 bulan hingga 2+ tahun. Profil Fidelity lama menggunakan "pendek ≤ 3 minggu, sederhana ≤ 3 bulan". — [Trading Central](https://investor.tradingcentral.com/technical-insight); [Fidelity](https://research2.fidelity.com/fidelity/research/reports/release2/Research/TradingCentral.asp)
- **Peristiwa teknikal:** "saat penunjuk mencetus isyarat atau corak carta terbentuk". Peristiwa bullish ditanda titik hijau dan bearish ditanda segi empat merah. — [Webull FAQ](https://www.webull.com/help/faq/10689-An-Overall-Description-of-TC); [Trading Central](https://investor.tradingcentral.com/technical-insight)
- Peristiwa **gagal** apabila harga selepasnya bergerak kuat ke arah bertentangan, dan penganalisis lazimnya mengabaikan corak yang gagal. FAQ menasihatkan semak ketiga-tiga ufuk; "ketiga-tiganya sejajar adalah terbaik". — [Trading Central](https://investor.tradingcentral.com/technical-insight); [IBKR webinar PDF](https://www.interactivebrokers.com/campus/wp-content/uploads/sites/2/2023/01/2021-WB-3812-Trading-Central-August-4-2021-v3.pdf)

**StockCharts [DR/SK]**
- **SCTR:** pangkat 0–99.9 dengan pemberat 60/30/10 (jangka panjang/sederhana/pendek); lihat nota sebelum §2.4.
- **Trend Composite Hill:** tersedia sebagai plugin TIP untuk StockCharts ACP (lihat §3). — [TrendInvestorPro](https://trendinvestorpro.com/trend-composite-signal-table-for-sp-500-stocks-free/print/)
- **Elder Impulse:** dipaparkan sebagai warna bar dalam carta StockCharts. — [StockCharts ChartWatchers](https://articles.stockcharts.com/article/articles-chartwatchers-2012-01-digging-deeper-into-elders-impulse-system/)
- Tiada "pill trend" tunggal StockCharts ditemui.

**Relative Rotation Graph (RRG; Julius de Kempenaer; tersedia di StockCharts/Optuma/TradingView) [SK]**
- **Paksi:** paksi-x JdK RS-Ratio, paksi-y JdK RS-Momentum (kadar perubahan nisbah). Kedua-duanya dinormalkan di sekitar 100.
- **Empat kuadran:** Leading, Weakening, Lagging dan **Improving**.
- **Putaran:** lazimnya ikut arah jam (Improving → Leading → Weakening → Lagging), tetapi ini "kecenderungan, bukan peraturan".
- **Perbandingan:** nilai RS-Ratio hanya boleh dibanding jika penanda aras sama. "Leading" bersifat relatif dan tidak bermakna harga sedang naik.
- — [LuxAlgo, Relative Rotation Graphs](https://www.luxalgo.com/library/concept/relative-rotation-graphs/); [PGAM](https://pgam.it.com/pages/academicinfo?id=200); [TradingView RRG script](https://www.tradingview.com/script/11vu1lHA-Relative-Rotation-RRG-JdK-RS-Ratio-RS-Momentum)

**Finviz [tiada pengesahan]**
- Tiada dokumentasi Finviz ditemui.
- Perbezaan takrif yang relevan: Trendlyne mentakrif "golden cross" sebagai **lintasan baru-baru ini** SMA50 di atas SMA200 (peristiwa), berbeza daripada tapisan "SMA50 di atas SMA200" (keadaan). — [Trendlyne](https://trendlyne.com/fundamentals/back-tests/4896)

**IBD [SK]**
- Market Pulse: 3 keadaan (lihat §2 dan nota sebelum §2.7).
- Pada peringkat saham, IBD menyediakan peringkat asas (§2) dan RS Rating. Garis RS gaya IBD dikira atas 12 bulan (dakwaan forum). — [Motley Fool forum](https://discussion.fool.com/t/trading-ibd-stocks/104584?page=18)

### Inferences
- **[IN] "Strong Buy" pada TradingView dan Barchart ≠ "trend kuat"**, kerana oscillator kontrarian turut diundi. Ini disahkan semula untuk TradingView. Bagi Barchart, Signal Strength (berbanding sejarah sendiri) ialah cara yang lebih dekat untuk mengukur "kekuatan".
- **[IN] Barchart Hold "Rising/Falling"** dan **RRG "Improving/Weakening"** ialah dua contoh platform yang secara eksplisit mempunyai **keadaan peralihan**. Kedua-duanya ditakrif melalui **perubahan** skor (arah 3 sesi; momentum RS), bukan melalui aras skor. Ini model yang paling sesuai jika papan mahu "mula naik" tanpa mengubah 3 label aras.
- **[IN] Trading Central:** ufuk pendek 2–6 minggu ≈ 10–30 sesi, iaitu ufuk papan. Gabungan ufuk (pendek bullish + pertengahan bearish) secara tidak langsung memberi "mula naik".

### Gaps
- Halaman metodologi rasmi Barchart (ambang 7 label, senarai penunjuk semasa), Finviz, Investing.com dan dokumen IBD tidak dapat dibaca kerana domain disekat dan carian tidak memulangkan teks.
- Morningstar: tiada label teknikal ditemui (selaras dengan nota sebelum). Tidak diketahui sama ada Morningstar Investor memaparkan Trading Central.
- Formula tepat JdK RS-Ratio dan RS-Momentum tidak diterbitkan (skrip TradingView dilindungi).

---

## 5. Bilangan keadaan: rasional setiap rangka, dan pandangan pengamal tentang keadaan eksplisit "awal naik / mula naik" berbanding 3 keadaan

### Takeaway
- **Label trend tulen** menggunakan 2–4 keadaan:
  - 2: Supertrend, Minervini, Hill;
  - 3: Elder Impulse, Ichimoku, IBD pasaran, Trading Central per ufuk, moomoo;
  - 4: Weinstein, Wyckoff, RRG, SST.
- **Rangka yang mempunyai keadaan "awal"** mentakrifkannya melalui **peristiwa atau perubahan** (tembusan Peringkat 1→2, SOS Wyckoff, FTD, Wedge Pop, kuadran Improving, Hold-Rising), bukan melalui aras penunjuk yang sama dengan Bullish.
- Tiada kajian ditemui yang membuktikan label 4 keadaan meramal lebih baik daripada 3 keadaan.

### Cited Findings
| Rangka | Bil. keadaan | Keadaan "awal" eksplisit? | Paksi masa | Rasional yang dinyatakan | Sumber |
|---|---|---|---|---|---|
| Weinstein | 4 (1 asas, 2 naik, 3 puncak, 4 turun) | Tidak sebagai label. Peralihan 1→2 (tembusan + MA berpusing naik) ialah titik beli | Mingguan, MA 30 minggu | Tindakan berbeza setiap peringkat: beli hanya dalam 2, jual/short dalam 4, tunggu dalam 1/3 [SK] | [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/) |
| Wyckoff | 4 kitaran (pengumpulan, markup, pengagihan, markdown) + fasa A–E | Ya: Fasa D (SOS, LPS) sebelum markup Fasa E | Budi bicara | Urutan peristiwa; skema ialah "kosa kata, bukan templat" [SK] | [LuxAlgo](https://www.luxalgo.com/library/concept/wyckoff-accumulation-schematic/) |
| Teori Dow | 2 arah primer + pergerakan sekunder | Tidak; trend dianggap berterusan sehingga isyarat pembalikan pasti | Ayunan | Pengesahan dua purata; lewat secara reka bentuk [SK] | [ThisMatter](https://thismatter.com/money/technical-analysis/dow-theory.htm) |
| IBD Market Pulse | 3 (Confirmed uptrend / Under pressure / Correction) + "rally attempt" | Ya, secara tidak langsung: cubaan pulih (Hari 1–3) sebelum FTD | Harian, indeks | "Under pressure" = keadaan berhati-hati, bukan "tiada arah" [SK] | [LuxAlgo FTD](https://www.luxalgo.com/library/concept/follow-through-day/); [Fool forum](https://discussion.fool.com/t/ot-ibd-uptrend-under-pressure/37892) |
| Peringkat asas IBD | Kiraan 1, 1a, 1b, 2… | Ya: peringkat 1 = awal; set semula apabila asas dilanggar | Asas (minggu) | Mengukur umur trend [SK] | [MarketSmith India](https://blog.marketsmithindia.com/?p=5476) |
| Templat Minervini | 2 (lulus/gagal) | Tidak; syarat SMA200 naik ≥ 1 bulan memerlukan trend sedia ada | 50/150/200 hari | Prasyarat Peringkat 2 [SK] | [ProRealCode](https://www.prorealcode.com/prorealtime-market-screeners/trend-template-mark-minervini/?pnum=12) |
| Elder Impulse | 3 (hijau/merah/biru) | Tidak | EMA13 + MACD-H, bar ke bar | Penapisan: setiap warna melarang satu arah; biru membenarkan kedua-duanya [DR/SK] | [Barchart](https://barchartsolutions.atlassian.net/wiki/x/k4E5QQ) |
| Triple Screen (skrin 1) | 3 (naik / turun / rata = tiada dagangan) | Tidak | Mingguan | Dagang hanya searah "tide" [SK] | [TakeProfit](https://takeprofitapp.com/en/learn/triple-screen-trading-system) |
| Ichimoku | 3 (atas / dalam / bawah awan) | "Dalam awan" = peralihan | 9/26/52 | Kedudukan berbanding awan [SK] | [Capital.com](https://capital.com/en-gb/learn/technical-analysis/ichimoku-cloud-strategy) |
| ADX/DMI | Arah 2 × kekuatan 2–3 | "ADX melintas ke atas 20 = trend baharu muncul" | 14 | Arah dan kekuatan dipisahkan [SK] | [Fidelity](https://www.fidelity.com/viewpoints/active-investor/average-directional-index-adx) |
| Supertrend | 2 | Tidak | ATR10 × 3 | Sentiasa dalam trend [SK] | [TradingView](https://www.tradingview.com/script/r6dAP7yi) |
| Trend Composite Hill | 6 nilai ganjil (−5, −3, −1, +1, +3, +5) | Tidak | 125 hari | Ganjil supaya tiada 0 [DR] | [TrendInvestorPro](https://trendinvestorpro.com/trend-composite-signal-table-for-sp-500-stocks-free/print/) |
| Kitaran Kell | 6 langkah | Ya: Wedge Pop (kembali melepasi EMA 10/20) | EMA 10/20 harian | Kedudukan dalam kitaran; selepas 2 Base n' Break = lewat [SK] | [TraderLion](https://traderlion.com/technical-analysis/chart-patterns/cycle-of-price-action-by-oliver-kell/) |
| RRG | 4 kuadran | Ya: Improving | Mingguan/harian, relatif | Putaran ikut jam ialah kecenderungan [SK] | [LuxAlgo](https://www.luxalgo.com/library/concept/relative-rotation-graphs/) |
| TradingView | 5 | Tidak | Pilihan pengguna | Jalur skor ±0.1 / ±0.5 [DR] | [TradingView](https://in.tradingview.com/support/solutions/43000614331) |
| Barchart | 7 aras + 5 arah | Ya: Hold "Rising/Falling" | 20/50/100–200 hari; arah 3 sesi | Arah menunjukkan hanyutan Hold ke Buy/Sell [DR] | [Barchart](https://www.barchart.com/crypto/quotes/^BTCUSD/opinion) |
| Trading Central | 3 × 3 ufuk | Secara tidak langsung (gabungan ufuk) | 2–6 mgg / 6–39 mgg / 9 bln+ | "Ketiga-tiga sejajar adalah terbaik" [DR] | [Trading Central](https://investor.tradingcentral.com/technical-insight) |
| moomoo, SST | 3; 4 (Uptrend / Constructive / Neutral / Downtrend) | SST: "Constructive" | SST: 20/50/200 | Lihat nota sebelum §2.6, §2.10 | nota sebelum |

- **Bukti tentang keadaan "awal":**
  - IBD: "separuh hingga dua pertiga" FTD membawa kepada trend naik berterusan. — [LuxAlgo FTD](https://www.luxalgo.com/library/concept/follow-through-day/)
  - Weinstein: tembusan Peringkat 2 boleh gagal kembali ke asas. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)
  - Kell: dua Base n' Break = lewat dalam kitaran. — [TraderLion](https://traderlion.com/technical-analysis/chart-patterns/cycle-of-price-action-by-oliver-kell/)
  - Ketiga-tiganya pernyataan pengamal, bukan ujian statistik bebas.

### Inferences
- **[IN] Tiga corak reka bentuk "mula naik" dalam amalan:**
  - (a) **Peristiwa + tetingkap:** keadaan "Mula naik" bermula pada peristiwa tembusan atau pengesahan dan berlangsung N hari atau sehingga susunan penuh tercapai (Weinstein 1→2, FTD, Wedge Pop).
  - (b) **Arah perubahan di dalam Neutral:** Barchart Hold-Rising, RRG Improving.
  - (c) **Kiraan umur:** peringkat asas IBD, kiraan Base n' Break Kell, syarat SMA200 naik ≥ 1 bulan Minervini.
  - Corak (b) dan (c) tidak menambah sempadan aras baharu. Oleh itu ia tidak menambah *flip-flop* label utama. Ini selaras dengan cadangan nota sebelum §4.1: kekalkan 3 label dan tambah penunjuk sekunder kecil.
- **[IN] Dengan takrif semasa (susunan 50/150/200),** "Mula naik" yang paling bermakna ialah saham yang **sudah** melepasi SMA50 dengan SMA50 berpusing naik, tetapi susunan 50 > 150 > 200 **belum** lengkap. Contoh takrif calon untuk ujian empirikal (belum diuji):
  - **A1 (Weinstein harian):** dalam 30 sesi terakhir, C menembusi tertinggi 50 hari dengan volum ≥ 1.5× purata 50 hari, dan cerun 20 hari SMA150 ≥ 0, sementara susunan Bullish belum lengkap.
  - **A2 (Kell/Elder):** C > EMA10 > EMA20 dengan EMA20 naik, selepas C < SMA50 dalam 20 sesi lalu.
  - **A3 (gaya RRG mutlak):** ROC21 bertukar positif dan bertambah dalam keadaan Neutral (anak panah "↗" di sebelah Neutral, bukan label baharu).
  - Ujian perlu mengukur sama ada A1–A3 memisahkan pulangan hadapan 5/10/21 hari daripada Neutral biasa. Protokolnya sama seperti nota sebelum §5.
- **[IN] Untuk posisi swing,** keadaan Weinstein/Minervini jarang berubah dalam tempoh pegangan, jadi maklumatnya untuk keputusan pegang/jual adalah kecil. Rangka swing (10/20 EMA) pula bertindih dengan Chandelier. Ini menyokong label konteks berpaksi 50 hari (nota sebelum) bersama penanda peralihan.

### Gaps
- Tiada kajian bersemak rakan atau ujian vendor ditemui yang membanding ketepatan ramalan label 3 keadaan dengan 4 keadaan (dengan keadaan "awal naik" eksplisit) bagi saham AS.
- Dakwaan O'Neil bahawa asas peringkat awal lebih berjaya daripada asas peringkat lewat tidak disahkan dalam sesi ini.
- Takrif "Constructive" SST masih disimpulkan daripada sampel (nota sebelum §2.10), bukan dokumen.

---

## 6. Takrif titik mula trend dan cara rangka/platform memaparkan "sejak bila" (tarikh mula, hari dalam keadaan)

### Takeaway
Terdapat dua konvensyen:
- (a) **tarikh peristiwa pencetus:** bar pertama syarat dipenuhi (Supertrend flip, bar warna Elder, peristiwa Trading Central, minggu tembusan Weinstein);
- (b) **tarikh pengesahan:** selepas tempoh atau syarat kedua (FTD pada Hari ≥ 4, pengesahan dua purata Dow, penapis 2% + 3 hari StockCharts).

Kiraan umur atau kiraan hari dipaparkan oleh IBD (hari cubaan pulih, kiraan hari pengagihan 25 sesi, peringkat asas) dan Kell (bilangan Base n' Break). Barchart pula memaparkan arah 3 sesi. Tiada platform yang ditemui mendokumenkan medan "hari dalam trend" bagi label trend saham.

### Cited Findings
**Konvensyen (a): tarikh peristiwa pencetus**
- **Weinstein:** Peringkat 2 bermula pada tutup (mingguan) di atas rintangan Peringkat 1 dengan volum tinggi. Peringkat 4 bermula pada pecahan di bawah sokongan puncak dengan harga di bawah MA yang menurun. [SK] — [MQL5](https://www.mql5.com/en/articles/22746); [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)
- **Elder Impulse:** warna ditentukan setiap bar berbanding bar sebelumnya. Permulaan = bar pertama warna baharu. [DR] — [Barchart](https://barchartsolutions.atlassian.net/wiki/x/k4E5QQ)
- **Trading Central:** peristiwa bertarikh pada saat penunjuk mencetus atau corak terbentuk, dan ditanda pada carta. Peristiwa "gagal" jika harga bergerak kuat bertentangan. [DR] — [Webull FAQ](https://www.webull.com/help/faq/10689-An-Overall-Description-of-TC); [Trading Central](https://investor.tradingcentral.com/technical-insight)

**Konvensyen (b): tarikh pengesahan**
- **IBD:** Hari 1 cubaan pulih = tutup naik pertama selepas paras terendah baharu. Kiraan hari diteruskan dan diset semula jika Hari 1 dilanggar. Tarikh FTD (Hari ≥ 4) = permulaan "Confirmed uptrend". Hari pengagihan dikira dalam tetingkap 25 sesi. [SK] — [LuxAlgo FTD](https://www.luxalgo.com/library/concept/follow-through-day/); [MarketSmith India](https://blog.marketsmithindia.com/?p=4789)
- **Teori Dow:** pembalikan disahkan hanya apabila wujud puncak lebih rendah **dan** lembah lebih rendah, serta disahkan oleh kedua-dua purata. [SK] — [ThisMatter](https://thismatter.com/money/technical-analysis/dow-theory.htm)
- **ADX (Kaufman):** "trending" bermula apabila ADX melintas ke atas 25 dan tamat apabila melintas ke bawah 20. [SK] — [Traders.com](https://technical.traders.com/tradersonline/display.asp?art=8229)
- **Wilder Extreme Point Rule:** pembalikan pada silang DI hanya berkuat kuasa jika paras tinggi/rendah bar silang ditembusi. Jika tidak, posisi lama kekal. [SK] — [TradingView](https://de.tradingview.com/script/R3YRg9EF-adx-w-wilders-di-di-dx-adxr-equilibrium-point)
- **StockCharts:** penapis jalur 2% + 3 hari untuk silang MA (nota sebelum §1). [AP] — [StockCharts](https://articles.stockcharts.com/article/articles-chartwatchers-2022-02-reduce-whipsaws-and-improve-pe-590/)

**Kiraan umur dan arah**
- **IBD peringkat asas:** kiraan asas sejak trend bermula, diset semula apabila asas dilanggar. [SK] — [MarketSmith India](https://blog.marketsmithindia.com/?p=5476)
- **Kell:** kiraan Base n' Break. ≥ 2 = lewat dalam kitaran. [SK] — [TraderLion](https://traderlion.com/technical-analysis/chart-patterns/cycle-of-price-action-by-oliver-kell/)
- **Minervini:** syarat umur SMA200 naik ≥ 1 bulan (sebaiknya 4–5 bulan). [SK] — [ProRealCode](https://www.prorealcode.com/prorealtime-market-screeners/trend-template-mark-minervini/?pnum=12)
- **Barchart:** Signal Direction membanding perbezaan isyarat dengan 3 sesi terdekat (Strengthening/Weakening; Hold: Rising/Falling). Signal Strength membanding dengan sejarah isyarat sendiri. [DR] — [Barchart](https://barchart.com/stocks/signals/direction)
- **RRG:** kedudukan dan kuadran dipaparkan bersama ekor laluan (arah putaran). [SK] — [LuxAlgo RRG](https://www.luxalgo.com/library/concept/relative-rotation-graphs/)

### Inferences
- **[IN] Peraturan papan "2 tutup berturut-turut"** ialah konvensyen (b) dengan tempoh pengesahan pendek. Untuk ketelusan, simpan dua tarikh:
  - `tarikh_isyarat`: tutup pertama yang memenuhi syarat;
  - `tarikh_sah`: tutup kedua, iaitu tarikh label bertukar.
  - Paparkan "Bullish sejak DD Mmm (n sesi)" berdasarkan `tarikh_sah`. Pilihan lain ialah berdasarkan `tarikh_isyarat`, seperti Supertrend/Elder yang menandakan bar pencetus. Mana-mana pilihan perlu konsisten dan dinyatakan dalam tooltip.
- **[IN] Cadangan medan sekunder** yang meniru amalan di atas, semuanya tanpa menambah label aras:
  - kiraan sesi dalam keadaan (gaya IBD);
  - keadaan semasa beli → keadaan sekarang (gaya peristiwa Trading Central);
  - arah 3–5 sesi skor asas (gaya Barchart);
  - bilangan pertukaran dalam 60 sesi (penunjuk *whipsaw*).
- **[IN] Bagi takrif susunan 50/150/200,** "tarikh mula Bullish" sering jauh selepas permulaan sebenar kenaikan (lihat §1). Oleh itu "n sesi dalam Bullish" akan kecil walaupun saham sudah naik berminggu-minggu. Pertimbangkan juga memaparkan "sesi sejak C > SMA50 kali terakhir bermula" sebagai umur trend jangka sederhana.

### Gaps
- Tiada dokumentasi platform ditemui yang menerangkan medan "hari dalam trend" atau "tarikh mula trend" bagi label trend saham (TradingView, Barchart, Finviz, StockCharts). Sejarah Opinion Barchart (hari/minggu/bulan lalu) tidak dapat disahkan.
- Panjang ekor lalai RRG dan jadual isyarat TrendInvestorPro (sama ada memaparkan tarikh isyarat terakhir) tidak disahkan.
- Logik flip Supertrend (tarikh mula = bar tutup melintasi jalur akhir bertentangan) daripada pengetahuan umum; tidak disahkan dalam sesi ini.
