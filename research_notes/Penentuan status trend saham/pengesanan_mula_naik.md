# Pengesanan "mula naik" / "mula turun" dan kawalan whipsaw bagi saham individu (ufuk swing 3–30 hari)

Disediakan 23 Okt 2026. Nota ini menyambung `nota_amalan_trend.md` (scratchpad `trend/`), yang meliputi definisi label 3 keadaan, amalan platform dan bukti kuasa ramalan trend. Isi nota itu tidak diulang di sini. Fokus nota ini ialah **bila** sesuatu keadaan bermula, berapa **lewat** peraturan mengesannya, berapa kerap ia **palsu**, dan **tarikh mana** yang patut dipaparkan sebagai "sejak".

**Tanda jenis sumber** (sama seperti nota terdahulu, dengan dua tambahan):
- **[PR]** kajian bersemak rakan.
- **[KK]** kertas kerja / pracetak / ringkasan pihak ketiga tentang kajian.
- **[AP]** amalan pengamal atau platform (konvensyen, bukan bukti).
- **[UV]** ujian balik vendor/blog: angka ada, tetapi metodologi tidak dapat disemak.
- **[TB]** terbitan matematik oleh penulis nota (model ringkas tanpa hingar). Bukan bukti empirikal.
- **[IN]** inferens atau pendapat penulis nota.

**Had kaedah.** WebFetch gagal (`getaddrinfo ENOTFOUND chartschool.stockcharts.com`), dan curl melalui proksi ditolak (`CONNECT tunnel failed, response 403`). Semua butiran diambil daripada ringkasan enjin carian (abstrak, halaman bantuan, blog) dan daripada nota terdahulu. Angka bertanda *(ingatan; sahkan)* belum disahkan daripada teks penuh. Butiran yang hanya datang daripada satu blog ditanda [UV].

**Konteks papan.** Label semasa: Bullish = C > SMA50 > SMA150 > SMA200, Bearish = susunan terbalik, selain itu Neutral, dengan pengesahan 2 tutup. Keluar lorong 2: Chandelier tutup (tutup tertinggi sejak beli − 4×ATR14). Dalam nota ini, ATR bermaksud ATR14 seperti `keluar_lorong.atr` (purata mudah 14 julat sebenar), dan C ialah harga tutup terlaras.

---

## 1. Onset berasaskan tembusan (Donchian 20/55, pangsi asas O'Neil/Minervini VCP, penguncupan → ekspansi, NR7, paras tertinggi 52 minggu)

### Takeaway
Tembusan memberi **tarikh onset yang semula jadi**, iaitu bar tembusan. Namun kadar kegagalan yang didokumenkan tinggi dan meningkat sejak 1990-an. Bulkowski melaporkan bahawa kegagalan 10% bagi tembusan menaik berganda daripada 14% (1990-an) kepada 28% (2003–2007). Sistem Donchian/Turtle lazimnya hanya menang 30–45% dagangan. Oleh itu tembusan perlu dianggap "calon onset" yang memerlukan syarat gagal yang jelas, bukan pengesahan trend.

### Cited Findings
- **Takrif kegagalan Bulkowski:** corak dianggap gagal jika harga tidak bergerak lebih 5% dari harga tembusan sebelum berbalik arah. Kajian beliau juga memakai ambang 10%. [AP/UV] — [thepatternsite: Failure Rates](https://thepatternsite.com/FailureRates.html); [Traders.com 2009](https://www.traders.com/Documentation/FEEDbk_docs/2009/05/Bulkowski.html)
- **Kegagalan meningkat mengikut masa** (~14,000 corak, 1991–2008):
  - Kadar gagal-10% bagi tembusan **menaik** naik daripada 14% (pasaran bull 1990-an) kepada 28% (2003–2007).
  - Bagi tembusan **menurun**, kadar itu naik daripada 26% kepada 49%.
  - [AP/UV] — [Traders.com 2009](https://www.traders.com/Documentation/FEEDbk_docs/2009/05/Bulkowski.html); [thepatternsite](https://thepatternsite.com/FailureRates.html)
- **Volum tembusan (arah dapatan meragukan):** ringkasan carian menyebut kadar gagal-10% tembusan menaik ialah 14% dengan volum tembusan di atas purata, berbanding 5% dengan volum di bawah purata. Ini **berlawanan** dengan konvensyen O'Neil/Minervini, yang mahukan volum tinggi semasa tembusan. Halaman asal tidak dapat dibaca untuk mengesahkan arah dapatan ini. — [thepatternsite: Volume Study](https://thepatternsite.com/VolumeStudy.html); bandingkan dengan konvensyen volum ≥ 40% di atas purata dalam [MarketInOut: Minervini buy signal](https://www.marketinout.com/stock-screener/minervini-buy-signal)
- **Takrif kegagalan berbeza antara pengkaji:** antaranya tutup kembali ke dalam corak, kerugian setara jarak hentian, atau sasaran ukuran tidak tercapai. Kadar yang diterbitkan hanya sesuai sebagai anggaran awal kasar, kerana ia diukur pada pasaran dan era tertentu. [AP] — [LuxAlgo: pattern failure statistics](https://www.luxalgo.com/library/concept/pattern-failure-statistics/)
- **Donchian / Turtle:**
  - Konvensyen: masuk pada tembusan 20 hari atau 55 hari; keluar 10/20 hari. [AP] — nota terdahulu §1.1
  - 20 hari memberi isyarat lebih cepat dan lebih kerap, tetapi lebih banyak whipsaw dalam pasaran mendatar. 55 hari menapis tembusan kecil. [AP] — [Altrady: Turtle rules](https://www.altrady.com/blog/crypto-trading-strategies/turtle-trading-strategy-rules); [Altrady: Donchian](https://www.altrady.com/blog/crypto-trading-strategies/donchian-channel-strategy)
  - Kadar menang tipikal sistem 20/55 dilaporkan **30–40%**, dengan purata untung 3–5× purata rugi (BTC harian). [UV] — [Altrady](https://www.altrady.com/blog/crypto-trading-strategies/donchian-channel-strategy)
  - Emas: 55 hari long menang 48% (25 dagangan) dan 20 hari long 43% (56 dagangan). Sampel kecil. [UV] — [Arxum: Turtle 55-day](https://arxum.com/turtle-trading-strategy/)
  - **Tiada kajian kadar tembusan palsu Donchian bagi saham AS individu ditemui.**
- **Pangsi VCP Minervini** (tafsiran saringan pihak ketiga, bukan petikan buku):
  - pangsi = harga tertinggi 20 bar lepas, dan asas mestilah ketat (dalam 6% daripada pangsi);
  - volum tembusan ≥ 40% di atas purata 50 hari;
  - volum mengering tepat di bawah pangsi;
  - tutup pada separuh atas julat hari itu, dan tidak lebih 5% di atas pangsi;
  - kesemua 8 syarat Trend Template mesti dipenuhi, dan RS ≥ 80.
  - [AP] — [MarketInOut: Minervini buy signal](https://www.marketinout.com/stock-screener/minervini-buy-signal); [MarketInOut: breakout trigger](https://www.marketinout.com/stock-screener/minervini-breakout-trigger/uk)
  - Senarai semak lain memakai RS > 70 tanpa angka volum. Dakwaannya bahawa kadar menang "bertambah 40%" tidak boleh disahkan. — [Finer Market Points: VCP checklist](https://www.finermarketpoints.com/post/vcp-criteria-complete-checklist)
- **Kiraan asas O'Neil/IBD:**
  - Asas pertama selepas paras terendah utama = peringkat 1. Asas berikutnya yang terbentuk ≥ ~20% di atas asas sebelumnya menambah kiraan. Penembusan di bawah paras terendah asas sebelumnya menetapkan semula kiraan kepada 1.
  - Kajian IBD yang dipetik: tembusan daripada asas **peringkat 3** berjaya ~67%, dan kadar gagal naik kepada ~80% bagi asas **peringkat 4**. [AP] — [IBD via Yahoo: Counting Bases](https://news.yahoo.com/counting-bases-helps-assess-buying-risk.html); [LuxAlgo: O'Neil base analysis](https://www.luxalgo.com/library/concept/oneil-base-analysis/)
  - Panjang asas dikira dalam minggu, daripada minggu pertama yang tutup menurun hingga minggu sebelum tembusan. [AP] — [IBD via Yahoo: count the weeks](https://finance.yahoo.com/news/looking-great-chart-sure-count-203400677.html)
- **NR7 (Crabel):**
  - Takrif: julat tinggi−rendah hari ini ialah yang paling sempit dalam 7 bar terakhir.
  - Amalan lazim: letak order hentian di paras tinggi dan rendah bar NR.
  - Kelemahan: penanda binari ini tidak mengambil kira kesempitan relatif kepada volatiliti biasa, jadi sesetengah pengamal menambah semakan ATR.
  - **Statistik tembusan Crabel tidak dapat disahkan.** [AP] — [LuxAlgo: NR4/NR7](https://www.luxalgo.com/library/concept/nr4-nr7-narrow-range-bars.md)
- **Bollinger squeeze:**
  - BandWidth = (jalur atas − jalur bawah) / jalur tengah, dengan Bollinger (20, 2).
  - Garis panduan Bollinger: squeeze = bacaan terendah dalam ~6 bulan (~125 bar harian). Varian lain memakai persentil atau ujian Keltner.
  - Squeeze **tidak memberi arah**, hanya kebarangkalian ekspansi.
  - Dakwaan bahawa squeeze harian lazimnya berlangsung 2–8 minggu adalah anekdot vendor. [AP] — [LuxAlgo: Bollinger squeeze](https://www.luxalgo.com/library/concept/bollinger-squeeze/); [QuestDB: BandWidth](https://questdb.com/docs/cookbook/sql/finance/bollinger-bandwidth/)
- **Paras tertinggi 52 minggu:** kedekatan dengan paras tertinggi 52 minggu meramal pulangan lebih baik daripada pulangan lalu, dan kesannya tidak berbalik dalam jangka panjang (George & Hwang 2004). [PR] — [CXO: 52-week high](https://cxoadvisory.com/technical-trading/the-52-week-high-as-a-momentum-indicator-for-individual-stocks)

### Inferences
- **[TB] Kelewatan Donchian dalam model V simetri.** Andaikan harga jatuh dan kemudian naik dengan cerun mutlak yang sama (V simetri, tanpa hingar).
  - Tutup melepasi tutup tertinggi N hari lepas pada lebih kurang **N/2 bar selepas dasar**: 20 hari → ~10 bar; 55 hari → ~27 bar.
  - Kelewatan ini **tidak bergantung pada kelajuan** kenaikan, kerana model ini berskala bebas.
  - Bagi dasar bulat atau asas mendatar, kelewatan dari "dasar" lebih panjang tetapi jarak harga yang perlu dilalui lebih kecil.
- **[IN] Pilih versi tutup.** Bagi papan EOD, tembusan berasaskan **tutup** (C_t > max C_{t−N..t−1}) lebih konsisten dengan label semasa dan Chandelier tutup berbanding tembusan intrahari (tinggi > tinggi N hari). Versi tutup juga tidak "repaint" dalam hari dagangan.
- **[IN] Calon peraturan (untuk diuji):**
  - **O1 Donchian-tutup 20:** `C_t > max(C_{t−20}…C_{t−1})`. Varian O1b: N = 50 atau 55.
  - **O2 Pangsi VCP-ringkas:** pangsi = `max(H_{t−20}…H_{t−1})`; `(pangsi − min(L_{t−20}…L_{t−1}))/pangsi ≤ 0.15` (asas) dan julat 10 hari terakhir ≤ 0.06 (ketat); `C_t > pangsi`; `V_t ≥ 1.4 × purataV50`; `(C_t − L_t)/(H_t − L_t) ≥ 0.5`. Dianggap "terlanjur" jika `C_t > 1.05 × pangsi`.
  - **O3 Squeeze → ekspansi:** BandWidth(20, 2) berada pada paras minimum 125 sesi pada sebarang hari dalam 10 sesi lepas, **dan** `C_t > max(C_{t−20}…C_{t−1})`. Arah ditentukan oleh tembusan; squeeze sahaja bukan onset.
  - **O4 Paras tertinggi 52 minggu baharu:** `C_t ≥ max(C_{t−252}…C_{t−1})`. Ini onset rejim "paras tertinggi baharu", bukan onset dari dasar.
  - **Syarat gagal wajib bagi O1–O4 (gaya Bulkowski / 2B):** onset dibatalkan jika dalam 10 sesi `C < aras tembusan − 0.5×ATR`, atau `C <` sauh dasar (lihat §7).
- **[IN] Kiraan asas IBD (peringkat 1/2 berbanding 3/4) ialah analog terdekat** kepada "berapa lama/berapa kali trend ini sudah naik". Bukti IBD (peringkat lewat lebih kerap gagal) menyokong paparan "berapa jauh sudah naik sejak dasar", bukan hanya "berapa hari".

### Gaps
- Tiada kadar tembusan palsu Donchian 20/55 yang boleh dipercayai bagi saham AS individu. Sumber yang ditemui ialah kripto, emas atau FX dengan sampel kecil.
- Arah kesan volum dalam kajian Bulkowski bercanggah dengan konvensyen O'Neil, dan halaman asal tidak dapat dibaca.
- Statistik NR7 Crabel dan kadar kejayaan Bollinger squeeze tidak disahkan.
- Peraturan volum O'Neil yang tepat (sering disebut "40–50% di atas purata") dan "buy point = tinggi pemegang + 0.10" tidak disahkan daripada sumber primer *(ingatan; sahkan)*.

---

## 2. Onset berasaskan purata bergerak (harga > SMA50/EMA50 yang naik, EMA10>EMA20, 20>50, cerun MA, golden cross)

### Takeaway
Semua isyarat MA ialah purata berwajaran pulangan lalu, jadi kelewatannya boleh dikira. Dalam model V simetri, "harga > SMA50 yang sedang naik" berlaku ~25–30 bar selepas dasar, dan golden cross 50/200 ~78 bar. Kedua-duanya **sama atau melebihi ufuk swing 30 hari**. Contoh S&P 500 2022–23 juga menunjukkan golden cross 77 sesi selepas paras terendah. Bagi "mula naik" pada ufuk swing, hanya MA pendek (10/20) atau harga lawan SMA20/50 tanpa syarat cerun yang cukup pantas. Isyarat ini pula paling kerap whipsaw.

### Cited Findings
- **Anatomi MA:** setiap peraturan MA (harga lawan MA, silang MA, cerun MA, tanda momentum) boleh ditulis sebagai purata berwajaran perubahan harga. Yang berbeza hanyalah bentuk pemberat, dan oleh itu kelewatan serta kekerapan isyarat palsu (Zakamulin). [PR/KK] — [SSRN 2677212](https://papers.ssrn.com/abstract=2677212)
- **Peraturan MA memberi isyarat lebih awal daripada TSMOM** dan kedua-duanya berkait rapat (Marshall, Nguyen & Visaltanachoti 2017). [PR] — [Quantitative Finance 17(3)](https://ideas.repec.org/a/taf/quantf/v17y2017i3p405-421.html)
- **Golden cross S&P 500:**
  - Paras terendah tutup Okt 2022 → golden cross 2 Feb 2023 = **77 sesi** dagangan kemudian.
  - 38 golden cross dari 1950 hingga Okt 2026 (~1 setiap 2 tahun).
  - Peraturan SMA 50/200 (dagang sesi berikutnya) memberi 7.21% setahun dengan kejatuhan maksimum −33.9%, berbanding beli-dan-pegang 8.16% dan −56.8%.
  - Kes 2015–2016 disebut sebagai golden cross yang gagal dengan cepat.
  - [UV] — [Kagels Trading: Golden Cross](https://kagels-trading.com/blog/golden-cross/)
- **Harga lawan SMA200 jauh lebih kerap whipsaw daripada silang 50/200:** SPX bersilang dengan SMA200 sebanyak 165 kali sejak 2000. StockCharts mencadangkan penapis 2% + 3 hari. [AP] — [StockCharts mailbag 2011](https://stockcharts.com/articles/mailbag/2011/02/how-can-i-reduce-indicator-whipsaws-using-the-percentage-price-oscillator-to-filter-moving-average-s.html); [StockCharts 2022](https://articles.stockcharts.com/article/articles-chartwatchers-2022-02-reduce-whipsaws-and-improve-pe-590/)
- **Templat Minervini** memerlukan SMA200 naik ≥ 1 bulan (sebaiknya 4–5 bulan) dan C > SMA50 > SMA150 > SMA200. [AP] — [TradingView: trend template](https://www.tradingview.com/scripts/trend-template/)
  - Ini definisi **keadaan trend matang**, bukan onset. Label Bullish papan semasa mewarisi sifat ini.
- **Penapis cerun Weinstein:** SMA 30 minggu (≈ 150 hari) mesti naik untuk Peringkat 2. [AP] — [LuxAlgo: Weinstein](https://www.luxalgo.com/library/concept/weinstein-stage-analysis.md)
- Peraturan "N tutup di atas SMA200" (N = 2) **mengurangkan bilangan dagangan hampir separuh** dan mengurangkan kejatuhan. [UV] — [Alvarez Quant Trading](https://alvarezquanttrading.com/blog/reducing-whipsaws-when-using-200-day-moving-average-for-market-timing/)

### Inferences
- **[TB] Purata umur pemberat ("kelewatan") MA pada trend linear:** SMA_n dan EMA_n (α = 2/(n+1)) sama-sama mempunyai purata umur pemberat **(n−1)/2 bar**. Pada trend linear, MA mengekori harga tepat sebanyak itu.

  | MA | Kelewatan pada trend linear (bar) |
  |---|---|
  | 10 | 4.5 |
  | 20 | 9.5 |
  | 50 | 24.5 |
  | 150 | 74.5 |
  | 200 | 99.5 |

- **[TB] Model V simetri** (harga = a·|s|, dasar pada s = 0, tanpa hingar). Bar selepas dasar sehingga isyarat pertama:

  | Isyarat | Formula | Contoh |
  |---|---|---|
  | Harga > SMA_n | 0.293·n | SMA10 ≈ 3; SMA20 ≈ 6; **SMA50 ≈ 15**; SMA200 ≈ 59 |
  | Cerun SMA_n bertukar positif | n/2 | **SMA50 = 25** |
  | Cerun berasaskan `SMA_t − SMA_{t−k} > 0` | ≈ n/2 + k/2 | SMA50, k = 10 → ~30 |
  | Harga > SMA_n **yang sedang naik** | ≈ n/2 | SMA50 ≈ 25–30 |
  | SMA_m > SMA_n (n ≤ 2m) | √(m·n/2) | **10/20 ≈ 10** |
  | SMA_m > SMA_n (n > 2m) | n − 0.707·√(n(n−m)) | **20/50 ≈ 23**; **50/200 ≈ 78**; analog SMA bagi MACD 12/26 ≈ 12.5 |
  | Tembusan Donchian N | N/2 | 20 → 10; 55 → 27 |

  - Angka 50/200 ≈ 78 bar kebetulan sepadan dengan 77 sesi SPX 2022–23. Ini konsisten dari segi tertib magnitud, tetapi bukan bukti.
  - EMA memberi pemberat lebih kepada data terkini, jadi silang EMA dijangka **lebih awal sedikit** daripada analog SMA. Nilai tepatnya tidak dikira.
  - Semua kelewatan MA ini **tidak bergantung pada kelajuan** kenaikan dalam V simetri. Kelewatan ATR (§4) pula bergantung pada kelajuan.
- **[IN] Implikasi bagi label semasa (C > SMA50 > SMA150 > SMA200).** Selepas aliran turun, SMA50 perlu melintasi SMA150, kemudian SMA150 melintasi SMA200. Dalam V simetri, silang 50/150 ≈ 150 − 0.707·√(150·100) ≈ 63 bar, dan 150/200 lebih lama lagi.
  - Jadi label Bullish semasa lazimnya muncul **2–4+ bulan selepas dasar**, iaitu selepas sebahagian besar pergerakan swing 3–30 hari selesai.
  - Ia sesuai sebagai label **keadaan** (konteks), tetapi tidak sesuai untuk **onset**. "Mula naik" perlu lapisan berasingan yang lebih pantas.
- **[IN] Calon peraturan:**
  - **O5 (K1 nota terdahulu):** `z = (C_t − SMA50_t)/ATR_t ≥ +0.5` dan `SMA50_t − SMA50_{t−10} > 0`. Kelewatan ~25–30 bar dari dasar V, jadi lebih sesuai untuk "naik disahkan", bukan "mula naik".
  - **O5a (pantas):** `C_t > SMA50_t + 0.5·ATR_t` **tanpa** syarat cerun, dari keadaan Bearish/Neutral. Kelewatan ~15 bar.
  - **O6:** `EMA10_t > EMA20_t` (silang dari bawah) **dan** `C_t > SMA50_t`. Kelewatan ~10–15 bar; whipsaw tinggi.
- **[IN] Kekerapan whipsaw:** isyarat harga lawan MA lebih kerap whipsaw daripada silang dua MA, berdasarkan perbandingan 165 silang SPX/SMA200 sejak 2000 berbanding ~38 golden cross sejak 1950. Silang dua MA lebih stabil tetapi jauh lebih lewat. Ini pertukaran asas kelewatan lawan kebisingan.

### Gaps
- Tiada kajian bersemak rakan yang ditemui yang melaporkan **kelewatan dalam hari** dan **kadar whipsaw** silang EMA10/20 atau 20/50 bagi saham AS individu.
- Dakwaan bahawa "~30% golden cross diikuti death cross dalam 6 bulan" muncul dalam satu blog tanpa data atau kaedah, jadi tidak dipakai.
- Kajian "StockCharts SystemTrader: reducing MA whipsaws with smoothing and quantifying filters" (Arthur Hill 2018) ditemui tetapi tidak dapat dibaca — [StockCharts](https://stockcharts.com/articles/arthurhill/2018/10/systemtrader---reducing-moving-average-whipsaws-with-smoothing-and-quantifying-filters-.html)

---

## 3. Onset berasaskan struktur ayunan (HH+HL Dow, zigzag/fractal ATR atau %, 2B dan 1-2-3)

### Takeaway
Struktur ayunan memberi **sauh onset yang paling bermakna**, iaitu dasar pangsi. Namun pangsi hanya diketahui selepas harga berbalik sejauh ambang, dan kaki terakhir zigzag sentiasa "repaint". Peraturan yang sah masa nyata mesti: (a) mengesahkan pangsi hanya selepas pergerakan balas ≥ ambang (cth. k×ATR) atau ≥ 2 bar di kanan (fractal), dan (b) menetapkan tarikh onset pada **bar pengesahan**, sambil memaparkan tarikh pangsi sebagai maklumat.

### Cited Findings
- **Zigzag:**
  - Pangsi terbaharu hanya disahkan selepas harga berbalik sejauh ambang penuh. Kaki terakhir memanjang atau beralih apabila bar baharu tiba, manakala pangsi terdahulu yang sudah disahkan kekal.
  - Sesetengah versi menambah jarak minimum dalam bar antara pangsi.
  - Amaran boleh dicetus pada **bar pengesahan**, iaitu saat pertama pangsi diketahui, bukan pada bar ekstrem. Pilihan "bar tertutup sahaja" disediakan untuk mengelak repaint.
  - [AP] — [LuxAlgo: Zigzag structure](https://www.luxalgo.com/library/concept/zigzag-structure.md)
- **Williams fractal:**
  - Klasik: 2 bar di setiap sisi, jadi penanda muncul dengan kelewatan 2 bar. Fractal pada bar hidup bersifat sementara.
  - Selepas bar kanan ditutup, fractal yang dikod dengan betul tidak berubah. Kosnya ialah kelewatan, bukan repaint.
  - Versi lebih lebar disahkan lebih lewat, tetapi menghasilkan fractal yang lebih sedikit dan lebih bermakna.
  - [AP] — [LuxAlgo: Williams fractal](https://www.luxalgo.com/library/concept/williams-fractal.md)
- **Sperandeo 1-2-3** (perubahan trend), tiga langkah:
  1. garis trend yang dilukis dengan betul dipecahkan;
  2. harga menguji semula ekstrem tetapi gagal membuat ekstrem baharu;
  3. harga memecahkan titik ayunan terakhir.
  - Pecahan garis trend sahaja dianggap lemah, kecuali dengan gap atau volum besar.
  - [AP] — [RoboForex: Sperandeo 1-2-3 dan 2B](https://blog.roboforex.com/blog/2020/02/11/trading-like-sperandeo-1-2-3-reversal-and-2b-pattern/); [stockjock2: Sperandeo analysis](http://stockjock2.blogspot.com/2007/08/sperandeo-analysis.html)
- **2B:** tembusan palsu, iaitu harga membuat paras tinggi/rendah baharu, gagal mengekalkannya dan tutup kembali melepasi ekstrem sebelumnya. [AP] — [RoboForex](https://blog.roboforex.com/blog/2020/02/11/trading-like-sperandeo-1-2-3-reversal-and-2b-pattern/)
- **Teori Dow:** rekod Hamilton (1902–1929) diuji semula oleh Brown, Goetzmann & Kumar (1998), yang mendapati nilai pemasaan. [PR] — [Yale SOM WP](https://ideas.repec.org/p/ysm/somwrk/ysm30.html)
- **Pentarikhan titik pusingan berasaskan peraturan:**
  - **Pagan & Sossounov:** mengenakan tempoh minimum bagi fasa bull dan bear.
  - **Lunde & Timmermann:** mengenakan perubahan harga minimum sejak puncak/lembah terakhir sebelum titik pusingan baharu diterima. Ini secara konsep ialah zigzag % ambang.
  - [PR] — [Kole & van Dijk 2017, J. Applied Econometrics](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.2511); [ERIM WP](https://www.erim.eur.nl/fileadmin/erim_content/documents/BullBear3.pdf)
- **Kole & van Dijk (2017):** model penukaran rejim mendapat skor **ketepatan statistik** luar sampel tertinggi, tetapi algoritma Lunde & Timmermann memberi **prestasi pelaburan terbaik**. [PR] — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.2511)

### Inferences
- **[TB] Kelewatan pengesahan pangsi** = ambang ÷ kelajuan pergerakan balas.
  - Ambang k×ATR dan kenaikan a ATR/hari memberi kelewatan ≈ k/a bar.
  - k = 3: kenaikan kuat (0.5 ATR/hari) ≈ 6 bar; sederhana (0.25 ATR/hari) ≈ 12 bar.
  - Berbeza dengan MA/Donchian, pergerakan pantas disahkan lebih cepat.
- **[IN] Sauh tanpa look-ahead.** Pada hari pengesahan t, dasar pangsi ialah `argmin C` antara pangsi tinggi terakhir yang disahkan dan t. Ia terletak sepenuhnya di masa lalu, jadi **tiada look-ahead** jika dikira pada t dan tidak diubah selepas itu. Repaint hanya berlaku jika sauh dibenarkan bergerak ke paras rendah baharu selepas pengesahan.
  - Peraturan: selepas disahkan, sauh dibekukan. Jika C jatuh di bawah sauh, onset diisytiharkan **gagal** (gaya 2B), bukan disauh semula.
- **[IN] Calon peraturan:**
  - **O7 Dow / 1-2-3 dengan zigzag ATR-tutup:** pangsi disahkan apabila C bergerak ≥ 3×ATR14 dari ekstrem tutup sejak pangsi lawan terakhir. "Mula naik" pada hari pertama syarat (a) dan (b) dipenuhi:
    - (a) pangsi rendah terakhir yang disahkan > pangsi rendah sebelumnya (HL); dan
    - (b) `C_t >` pangsi tinggi terakhir yang disahkan (HH).
    - Sauh = tarikh pangsi rendah (HL), atau lembah terendah sebelumnya (titik "1") jika mahu memaparkan permulaan sebenar.
    - Varian O7b: k = 2.5 atau 4 (4 = cermin Chandelier lorong 2).
  - **O7c 2B dasar:** `L_t` atau `C_t` di bawah pangsi rendah terakhir, kemudian dalam ≤ 3 sesi `C >` pangsi rendah itu + 0.25×ATR. Sangat awal, dan dijangka paling banyak isyarat palsu. Sesuai untuk kaedah pantulan, bukan label umum.
- **[IN] Rujukan "onset sebenar" untuk ujian:** zigzag dengan look-ahead pada sampel penuh (ambang 4×ATR atau 15%, gaya Lunde–Timmermann) boleh dijadikan **kebenaran ex post**. Ukur kelewatan setiap calon (tarikh pengesahan − tarikh lembah ex post) dan peratus pergerakan yang sudah terlepas. Tidak boleh dipakai untuk paparan langsung.

### Gaps
- Ambang tepat Lunde & Timmermann (2004) bagi bull/bear (sering diingati sebagai 20%/15%–10%) *(ingatan; sahkan)*, dan tempoh minimum Pagan–Sossounov (fasa ≥ 4 bulan, kitaran ≥ 16 bulan) *(ingatan; sahkan)*.
- Tiada statistik kadar kejayaan 1-2-3 atau 2B yang bersemak rakan ditemui. Sumber hanyalah blog pengamal.
- Kelewatan pentarikhan masa nyata Kole & van Dijk tidak diperoleh daripada teks penuh.

---

## 4. Pembalikan penunjuk (Supertrend, Chandelier, PSAR, ADX/DI, MACD, Ichimoku, regresi linear, Kaufman ER)

### Takeaway
Supertrend, Chandelier dan PSAR ialah **hentian mengekor yang bertukar arah**, iaitu sentiasa di pasaran. Tarikh "flip" mudah dipaparkan, tetapi kadar menangnya ~40–43% pada saham harian (Nifty 500, Supertrend), dengan whipsaw sebagai sumber kerugian utama. ADX 20/25, MACD 12/26/9, Ichimoku 9/26/52 dan KER 0.3 ialah **konvensyen**, tanpa bukti bersemak rakan bagi saham AS yang ditemui. Calon paling serasi dengan papan ini ialah **Chandelier songsang 4×ATR14 berasaskan tutup**, iaitu cermin tepat kepada keluar lorong 2.

### Cited Findings
- **Supertrend:**
  - Lalai (10, 3) dicadangkan oleh pencipta, Olivier Seban. [AP] — [Quantified Strategies](https://quantifiedstrategies.substack.com/p/the-supertrend-indicator-backtested)
  - **Nifty 500 harian 2012–2025** (tempoh 3–21, gandaan 1–3): kadar menang kekal sempit, ~40.7% pada (3, 1) hingga ~43.2% pada (21, 3). Gandaan lebih penting daripada tempoh, dan jangkaan nilai setiap dagangan, bukan kadar menang, yang membezakan tetapan. [UV] — [Share.Market: 200,000 dagangan](https://www.share.market/buzz/insights/i-backtested-200000-trades-using-the-supertrend-indicator-here-is-what-actually-works)
  - S&P 500 mingguan sejak 1960: 68% menang tetapi hanya 41 dagangan, kejatuhan maksimum 25%. [UV] — [Quantified Strategies](https://quantifiedstrategies.substack.com/p/the-supertrend-indicator-backtested)
  - Lemah dalam pasaran mendatar/berombak. [UV] — sumber yang sama
  - Pine: `ta.supertrend()` memulangkan arah, dengan arah < 0 = naik. Flip dikesan dengan `ta.change(arah)`. Skrip "bar-close confirmed" hanya menerima flip selepas bar ditutup. [AP] — [PineConnector](https://www.pineconnector.com/blogs/pico-blog/ppine-script-ta-supertrend-v5-guide); [TradingView: bar-close confirmed](https://kr.tradingview.com/scripts/bar-close-confirmed)
- **Chandelier:** lazimnya 22 hari dengan 3×ATR (LeBeau). Papan ini memakai tutup tertinggi sejak beli − 4×ATR14. [AP] — nota terdahulu §1.1; [LuxAlgo: Supertrend](https://www.luxalgo.com/library/concept/supertrend.md)
- **Parabolic SAR:**
  - Wilder (1978); faktor pecutan bermula 0.02, langkah 0.02, maksimum 0.20. Sentiasa di pasaran (stop-and-reverse).
  - Wikipedia menyatakan AF 0.01 lebih sesuai untuk **saham**, supaya tidak terlalu sensitif kepada penurunan tempatan. [AP] — [Wikipedia: Parabolic SAR](https://en.wikipedia.org/wiki/Parabolic_SAR)
  - Barchart memakai "Parabolic 50" dalam ufuk sederhana. [AP] — [Barchart help](https://www.barchart.com/trader/help/technical_opinion/opinions.php)
- **ADX/DMI:** 14 hari; ADX < 20 = tiada trend, > 25 = trend kuat; +DI > −DI = arah naik. Ini konvensyen Wilder, dan tiada bukti bersemak rakan bagi saham AS ditemui (nota terdahulu §3.5). [AP] — [Fidelity: DMI](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/DMI)
- **Kaufman Efficiency Ratio (ER):**
  - Formula: |perubahan bersih N bar| ÷ Σ|perubahan bar-ke-bar| dalam tetingkap yang sama, dengan julat 0–1. [AP] — [LuxAlgo: KER](https://www.luxalgo.com/library/concept/kaufman-efficiency-ratio/)
  - Ambang tidak seragam antara sumber:
    - 0.3 lazim sebagai penapis (> 0.3 = pergerakan bermakna); 0.3–0.4 sebagai syarat kegigihan trend. [AP] — [Trading Literacy](https://tradingliteracy.com/kaufman-efficiency-ratio/); [StrategyQuant](https://strategyquant.com/codebase/kaufmans-efficiency-ratio-ker/)
    - > 0.5 = trend kuat. [AP] — [Trading Literacy](https://tradingliteracy.com/kaufman-efficiency-ratio/)
    - > ~0.6 = trend, dan julat yang hanyut boleh memberi 0.3–0.4 tanpa trend sebenar. [AP] — [Quantum Algo](https://www.quantum-algo.com/blog/guides/kaufman-adaptive-moving-average/)
- **Regresi linear (Clenow):** cerun regresi eksponen 90 hari × R², disetahunkan. [AP] — [Wealth-Lab](https://wealth-lab.com/Discussion/Volatility-adjusted-momentum-indicator-by-Clenow-9220)
- **Ichimoku (9, 26, 52)** termasuk dalam kumpulan MA TradingView Technical Ratings. [AP] — [TradingView: Technical Ratings](https://tradingview.com/support/solutions/43000614331-technical-ratings)

### Inferences
- **[TB] Kelewatan flip hentian ATR** ≈ (jarak hentian) ÷ (kelajuan pergerakan balas).
  - Chandelier songsang k = 4: kenaikan 0.5 ATR/hari ≈ 8 bar; 0.25 ATR/hari ≈ 16 bar.
  - k = 3: 6 dan 12 bar.
  - Supertrend (10, 3) memakai HL2 ± 3×ATR10, jadi jaraknya ≈ 3 ATR + separuh julat bar, iaitu kelewatan setara k ≈ 3.5.
- **[TB] Analog MACD 12/26:** analog SMA bagi silang garis sifar ≈ 12.5 bar selepas dasar V (§2). Silang garis isyarat (EMA9 bagi MACD) lebih awal tetapi lebih bising.
- **[IN] Calon peraturan:**
  - **O8 Chandelier songsang (cermin lorong 2):**
    - Dari keadaan "turun"/neutral, **mula naik** apabila `C_t ≥ LLC + 4×ATR_t`, dengan LLC = tutup terendah sejak keadaan turun bermula (atau dalam 60 sesi).
    - **Mula turun** apabila `C_t ≤ HHC − 4×ATR_t`, dengan HHC = tutup tertinggi sejak keadaan naik bermula. Bagi posisi, syarat ini **sama** dengan pencetus lorong 2.
    - Varian O8b: k = 3 (lebih pantas, lebih bising).
    - Kelebihan: satu konsep untuk masuk/keluar, berskala volatiliti, dan sauh (LLC/HHC) ditakrif secara automatik tanpa look-ahead.
  - **O9 Supertrend (10, 3) flip disahkan tutup:** flip naik apabila `C_t >` jalur atas terakhir. Varian ATR14 (konsisten dengan papan).
  - **O11 ADX "bangkit":** `ADX14_t ≥ 20 > ADX14_{t−3}` dan `+DI > −DI`. Konvensyen sahaja; uji sebagai penapis, bukan pencetus.
  - **O12 Penapis kualiti:** `ER20 ≥ 0.3` dan perubahan bersih 20 hari > 0. Gunakan sebagai syarat tambahan kepada O1/O5a/O8 untuk menolak "mula naik" dalam julat berombak, bukan sebagai pencetus.
- **[IN] PSAR AF 0.02** pada saham meruap mungkin terlalu sensitif (rujuk cadangan AF 0.01 di Wikipedia). PSAR juga tidak berskala ATR, jadi kurang konsisten dengan Chandelier papan. Tidak disyorkan sebagai calon utama.
- **[IN] Kadar menang Supertrend ~40–43%** pada saham harian ialah anggaran awal yang realistik bagi **sebarang** flip hentian ATR: lebih separuh "onset" akan diterbalikkan sebelum pergerakan bermakna. Ini selari dengan §5 (had statistik).

### Gaps
- Tiada kajian Supertrend, PSAR, ADX atau Ichimoku pada **saham AS individu harian** dengan metodologi yang boleh disemak.
- Konvensyen MACD (12, 26, 9; Appel) dan butiran awan Ichimoku (Senkou A/B dianjak 26 ke hadapan) tidak disahkan dalam sesi ini *(ingatan; sahkan)*.
- Tiada ambang KER yang diuji secara empirikal ditemui.

---

## 5. Pendekatan rejim / titik perubahan masa nyata (CUSUM, BOCPD, HMM, model lompat, laju perlahan/pantas)

### Takeaway
Teori pengesanan terpantas (Page/Lorden/Moustakides) memberi pertukaran tepat: **kelewatan ≈ log(ARL penggera palsu) ÷ maklumat KL setiap bar**. Bagi drift saham individu pada skala swing, maklumat setiap hari sangat kecil, jadi pengesanan statistik "ketat" mengambil masa **berpuluh hingga beratus sesi**. Kajian aplikasi melaporkan kelewatan ~2 minggu (model lompat, COVID) hingga ≤ 4 minggu (bull, mingguan). Dapatan paling berguna untuk papan ialah Goulding, Harvey & Mazzoleni (JFE 2023): **percanggahan isyarat laju perlahan dan pantas menandakan titik pusingan** (Rebound / Correction).

### Cited Findings
- **CUSUM (Page 1954)** meminimumkan kelewatan kes terburuk (ukuran Lorden 1971) antara semua peraturan henti yang ARL ke penggera palsu ≥ B (Moustakides 1986). [PR] — [arXiv 0710.5935](https://arxiv.org/pdf/0710.5935); [arXiv 2403.18782 (Lorden)](https://arxiv.org/pdf/2403.18782)
- **Shiryaev–Roberts:**
  - Minimaks secara asimptot. Simulasi menunjukkan CUSUM lebih baik di bawah ukuran Lorden, manakala SR lebih baik bagi kelewatan purata bersepadu relatif.
  - Kedua-duanya optimum secara asimptot apabila kadar penggera palsu rendah.
  - [PR] — [arXiv 0710.5935](https://arxiv.org/pdf/0710.5935)
- Bagi famili komposit sebelum/selepas perubahan (seperti drift tidak diketahui), hujah nisbah kebolehjadian ringkas bagi CUSUM/SR **tidak terpakai terus**. Ram & Ramdas menerbitkan had bawah kelewatan untuk pengesan berkalibrasi ARL. [KK] — [arXiv 2602.05272](https://arxiv.org/abs/2602.05272v1)
- **BOCPD (Adams & MacKay 2007):** algoritma dalam talian yang menjejak taburan posterior **panjang larian (run length)**, iaitu masa sejak titik perubahan terakhir. Ia membuat inferens tepat bagi titik perubahan terbaharu, dan kewangan disebut sebagai bidang aplikasi. [KK] — [arXiv 0710.3742](https://arxiv.org/pdf/0710.3742)
  - Sensitiviti BOCPD asal merosot jika data berayun jauh daripada garis dasar asal (anjakan garis dasar). [KK] — [arXiv 2201.02325](https://www.arxiv.org/pdf/2201.02325)
  - Lanjutan autoregresif dengan parameter berubah masa untuk siri kewangan masa nyata (Tsaknaki, Lillo & Mazzarisi 2024). [KK] — [arXiv 2407.16376](https://arxiv.org/html/2407.16376v1)
  - Habibi (2021) menguji BOCPD pada siri kewangan **simulasi** sahaja. [PR] — [FIQF](https://journals.wsiz.edu.pl/fiq/article/view/525)
- **Model lompat statistik (S&P 500):**
  - Kelewatan ~**setengah bulan** untuk mengesan permulaan dan pengakhiran kejatuhan COVID-19.
  - Selepas bear bermula, model memerlukan beberapa hari pulangan negatif untuk mengesahkan anjakan, dan ini menghadkan penggera palsu.
  - [KK] — [arXiv 2402.05272](https://arxiv.org/pdf/2402.05272)
- **Inferens dalam talian gaya Nystrup et al. (2020):** anjakan rejim masa nyata berlaku **~2× lebih kerap** berbanding dalam sampel latihan. Ralat anggaran paling tinggi pada beberapa keadaan pertama dan terakhir dalam tetingkap, kerana tiada konteks lalu atau hadapan. [KK] — [arXiv 2410.14841](https://arxiv.org/pdf/2410.14841)
  - Kerja asal Nystrup (2016) mengesan titik perubahan VIX/S&P 500 untuk peruntukan dinamik. [PR] — [J. Asset Management 17(5)](https://ideas.repec.org/a/pal/assmgt/v17y2016i5d10.1057_jam.2016.12.html)
- **Bull/bear pasaran (mingguan):** model terbaik tidak pernah melebihi kelewatan **4 minggu** untuk mengklasifikasi peralihan ke pasaran bull. Kebenaran asas ialah pentarikhan Lunde–Timmermann pada sampel penuh. [KK] — [Uni Trier WP 2020-01](https://www.uni-trier.de/fileadmin/fb4/prof/VWL/EWF/Research_Papers/2020-01.pdf)
  - Lanjutan multivariat: model Markov hierarki dengan satu keadaan diskret sepunya bagi semua aset. [PR] — [Liu 2024, JAE](https://onlinelibrary.wiley.com/doi/10.1002/jae.3048)
- **Goulding, Harvey & Mazzoleni, "Momentum Turning Points", JFE 149 (2023) 378–406:**
  - Momentum siri masa perlahan dan pantas membahagikan pasaran kepada 4 keadaan: **Bull** (kedua-dua +), **Correction** (perlahan +, pantas −), **Bear** (kedua-dua −), **Rebound** (perlahan −, pantas +).
  - Isyarat perlahan menapis hingar tetapi lewat di titik pusingan. Isyarat pantas cepat tetapi memberi penggera palsu, iaitu pertukaran ralat Jenis II lawan Jenis I.
  - **Percanggahan** isyarat bermakna kebarangkalian titik pusingan lebih tinggi, manakala **kesepakatan** lebih dipercayai sebagai trend.
  - Mereka membina portfolio laju pertengahan dan peraturan pemilihan laju dinamik dengan prestasi luar sampel yang baik merentas pasaran ekuiti domestik dan antarabangsa.
  - Kertas kerja 2021 memakai 12 bulan (perlahan) dan 1 bulan (pantas) sebagai contoh.
  - [PR] — [EconBiz record](https://econbiz.de/Record/momentum-turning-points-goulding-christian/10014419608); [AEA 2021](https://benny.aeaweb.org/conference/2021/preliminary/paper/492Ds6fk); [IBKR Quant ringkasan](https://www.interactivebrokers.com/campus/ibkr-quant-news/trend-following-and-momentum-turning-points/); [Alpha Architect](https://alphaarchitect.com/?p=87070)
  - Kajian ini pada **indeks/pasaran**, bukan saham individu.

### Inferences
- **[TB] Tertib magnitud kelewatan CUSUM bagi drift saham.**
  - Andaikan σ harian = 2.5%, dan perubahan min harian dari 0 kepada Δμ. Maklumat KL setiap hari ≈ (Δμ/σ)²/2, dan kelewatan ≈ ln(ARL)/KL (asimptot Lorden; kasar bagi ambang kecil).

    | Δμ sehari (≈ pergerakan 20 hari) | KL sehari | Kelewatan, ARL = 63 sesi (1 penggera palsu/suku) | Kelewatan, ARL = 21 sesi |
    |---|---|---|---|
    | 0.25% (≈ 5%) | 0.005 | ~830 sesi | ~610 sesi |
    | 0.5% (≈ 10%) | 0.02 | ~210 sesi | ~150 sesi |
    | 1.0% (≈ 20%) | 0.08 | ~52 sesi | ~38 sesi |

  - **Kesimpulan:** pada ufuk 3–30 hari, drift swing **tidak boleh dikesan secara statistik dengan kadar penggera palsu rendah** sebelum swing itu selesai.
  - Semua peraturan onset praktikal (tembusan, flip ATR, silang EMA pendek) pada hakikatnya ialah **pengesan berpenggera palsu tinggi**. Nilainya datang daripada pembayaran tidak simetri (rugi kecil dipotong, untung besar dibiar), bukan ketepatan pengesanan. Ini konsisten dengan kadar menang 30–45% dalam §1 dan §4.
  - Implikasi paparan: "mula naik" mesti dibaca sebagai **"calon"**, dengan syarat gagal yang jelas.
- **[IN] CUSUM memberi sauh secara semula jadi.** Anggaran titik perubahan lazim ialah hari terakhir statistik CUSUM bernilai 0 sebelum melepasi ambang h *(sifat piawai Page; ingatan; sahkan)*. Ini setara dengan "dasar" tanpa look-ahead.
  - **O13 (untuk diuji):** `S_t = max(0, S_{t−1} + r_t/σ_t − k)`, dengan k = 0.25 (sasaran δ = 0.5σ) dan h = 4. "Mula naik" apabila S_t > h. Sauh = hari terakhir S = 0. Cermin bagi turun.
- **[IN] BOCPD** memberi "sejak bila" secara langsung (panjang larian MAP), tetapi lebih berat, sensitif kepada prior kadar bahaya (hazard), dan belum diuji pada saham. Tidak disyorkan untuk versi pertama papan.
- **[IN] Pemetaan Goulding et al. kepada papan (O10):**
  - perlahan = tanda r_63 (atau r_126); pantas = tanda r_10 atau r_21;
  - zon mati ±0.5·σ·√n (seperti K3 nota terdahulu);
  - **Rebound = "mula naik"**, **Correction = "mula turun"/pembetulan**, Bull/Bear = trend yang disepakati.
  - Ini satu-satunya takrif "mula naik" dengan sandaran bersemak rakan (walaupun pada indeks). Ia juga terus selari dengan label perlahan papan sebagai paksi "perlahan".
- **[IN] HMM/model lompat masa nyata ~2× lebih kerap bertukar** berbanding dalam sampel. Ini bukti langsung bahawa label masa nyata perlu **histeresis/penalti lompat**, dan bahawa backtest label yang dipadankan dalam sampel akan memperkecil whipsaw sebenar.

### Gaps
- Tiada kajian kelewatan BOCPD pada pulangan saham sebenar ditemui.
- Angka kelewatan Kole & van Dijk tidak diperoleh. Pengarang kertas kerja Trier 2020 tidak dapat disahkan daripada hasil carian.
- Spesifikasi tepat laju perlahan/pantas dalam versi jurnal Goulding et al. (2023) berbanding kertas kerja 2021 tidak disahkan.
- Tiada pengesahan bahawa keputusan Goulding et al. terpakai pada **saham individu**.

---

## 6. Kawalan whipsaw (pengesahan N tutup, jalur ATR/%, tempoh diam minimum, histeresis, penjajaran berbilang ufuk)

### Takeaway
Bukti kuantitatif perbandingan teknik penapis adalah **lemah dan bercampur**:
- Brock et al. memakai jalur 1%.
- Pada saham internet, jalur 1% dan kelewatan 1 hari **tiada kesan sistematik** ke atas keuntungan.
- Ujian pengamal menunjukkan N = 2 tutup mengurangkan dagangan ~50%, tetapi whipsaw mungkin hanya dialih, bukan dihapuskan.

Dua dapatan yang lebih kukuh ialah (a) inferens masa nyata bertukar ~2× lebih kerap tanpa penalti kegigihan, dan (b) kesepakatan isyarat perlahan + pantas lebih dipercayai. Oleh itu histeresis wajar dipilih untuk **kestabilan paparan**, dan diuji dari segi kelewatan, bukan alfa.

### Cited Findings
- **Jalur 1%** dalam Brock, Lakonishok & LeBaron (1992) bagi menapis isyarat MA. [PR] — [J. Finance 47(5)](https://ideas.repec.org/a/bla/jfinan/v47y1992i5p1731-64.html)
- **Saham internet:** jalur 1% dan kelewatan dagangan 1 hari **tiada kesan sistematik** ke atas keuntungan peraturan MA rekursif. Jalur digambarkan sebagai penapis lazim untuk mengesahkan trend sebelum masuk. (Fong & Yong 2005 *(ingatan; sahkan)*) [PR] — [ResearchGate: Chasing trends](https://www.researchgate.net/publication/222309209_Chasing_trends_Recursive_moving_average_trading_rules_and_internet_stocks)
- **Pasaran China:** jalur dan "tetingkap kesahan isyarat" ialah parameter berasingan yang diuji dalam grid. Jalur mengurangkan isyarat bising dalam keadaan bergolak, tetapi tiada perbandingan langsung dilaporkan. [KK] — [arXiv 1504.06397](https://arxiv.org/pdf/1504.06397)
- **N tutup berturut-turut di atas/bawah SMA200:** N = 2 mengurangkan bilangan dagangan hampir separuh dan juga kejatuhan. Pilihan N ialah soal berapa lama sanggup menunggu pengesahan. [UV] — [Alvarez Quant Trading](https://alvarezquanttrading.com/blog/reducing-whipsaws-when-using-200-day-moving-average-for-market-timing/)
- **Contoh satu tempoh:** masuk tertunda mengurangkan whipsaw daripada 8 kepada 0, manakala sistem jalur mengurangkannya daripada 8 kepada 2. Ilustrasi, bukan ujian formal. [UV] — [EasyLanguage Mastery](https://easylanguagemastery.com/building-strategies/improving-the-moving-average-crossover-system/)
- **Kerugian whipsaw bersifat struktur:** penapis terutamanya mengalihkan kerugian, bukan menghapuskannya. [UV] — [Halleytech](https://halleytech.substack.com/p/moving-averages-honest-backtest)
- **StockCharts:** jalur 2% + 3 hari bagi silang SMA. [AP] — [StockCharts mailbag 2011](https://stockcharts.com/articles/mailbag/2011/02/how-can-i-reduce-indicator-whipsaws-using-the-percentage-price-oscillator-to-filter-moving-average-s.html)
- **Kegigihan / penalti lompat:** model lompat statistik memerlukan beberapa hari pulangan negatif untuk mengesahkan anjakan. Ini menghadkan penggera palsu dengan kos kelewatan ~setengah bulan. [KK] — [arXiv 2402.05272](https://arxiv.org/pdf/2402.05272)
- **Inferens masa nyata ~2× lebih kerap bertukar** berbanding dalam sampel. [KK] — [arXiv 2410.14841](https://arxiv.org/pdf/2410.14841)
- **Penjajaran berbilang ufuk:**
  - Kesepakatan isyarat perlahan dan pantas lebih dipercayai sebagai trend; percanggahan menandakan titik pusingan (Goulding, Harvey & Mazzoleni 2023). [PR] — [IBKR Quant](https://www.interactivebrokers.com/campus/ibkr-quant-news/trend-following-and-momentum-turning-points/)
  - Elder Triple Screen: tempoh trend = 4–5× tempoh dagangan. [AP] — [TakeProfit: Triple Screen](https://takeprofitapp.com/en/learn/triple-screen-trading-system)
- **Tempoh minimum fasa (Pagan–Sossounov)** berbanding **perubahan harga minimum (Lunde–Timmermann)** ialah dua cara pentarikhan yang berbeza. Lunde–Timmermann memberi prestasi pelaburan terbaik dalam Kole & van Dijk. [PR] — [Kole & van Dijk 2017](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.2511)

### Inferences
- **[IN] Perbandingan teknik** (kesan dinilai secara kualitatif):

  | Teknik | Parameter cadangan | Kesan kelewatan | Kesan whipsaw | Catatan |
  |---|---|---|---|---|
  | **H1 N tutup** | N = 2 (semasa); uji 3 | +1 hingga +2 bar | Kurang ~separuh (ujian SMA200) | Ringkas; sudah dipakai papan |
  | **H2 Jalur ATR (masuk)** | +0.5×ATR (≈ 1–2% saham biasa; setara jalur 1% Brock / 2% StockCharts) | Bergantung kelajuan: 0.5/a bar | Menolak silang kecil | Berskala volatiliti; adil bagi saham meruap |
  | **H3 Histeresis Schmitt** (ambang masuk ≠ ambang keluar) | Masuk z ≥ +0.5 ATR; kekal sehingga z < −0.25 ATR (atau < 0) | Tiada tambahan semasa keluar | Mengelak ulang-alik di sekitar satu ambang | Paling berkesan untuk label keadaan |
  | **H4 Tempoh diam minimum** | Label onset kekal ≥ 5 sesi, **kecuali** syarat gagal | Tiada kesan ke atas masuk | Mengurangkan kelipan paparan | Mesti ada pengecualian gagal, kalau tidak label menipu |
  | **H5 Syarat gagal (gaya 2B)** | Batal jika C < sauh, atau C < aras pencetus − 0.5×ATR dalam 10 sesi | — | Menjadikan onset palsu kelihatan cepat | Bukan penapis, tetapi pembetulan jujur |
  | **H6 Penjajaran ufuk** | "Mula naik" dinaik taraf ke "Naik" hanya apabila label perlahan (SMA50/150/200) bersetuju | Tiada kesan ke atas onset | Memisahkan "calon" daripada "disahkan" | Selari dengan Goulding et al. |

- **[IN] Jangan tindan semua penapis.** Setiap penapis menambah kelewatan. Dengan swing 3–30 hari dan kelewatan asas pencetus ~6–15 bar, gabungan N = 3 + jalur 1 ATR + cerun boleh menyebabkan onset dilapor selepas pergerakan selesai. Cadangan: **satu pencetus + H1 (N = 2) + H5**. H3 hanya bagi label keadaan perlahan.
- **[IN] Sasaran operasi** (dibawa dari nota terdahulu, untuk diuji):
  - median tempoh label keadaan ≥ 10 sesi;
  - label onset "gagal" ≤ 50%;
  - kelewatan median dari dasar ex post ≤ 10 sesi;
  - median pergerakan yang sudah terlepas pada pengesahan ≤ 1/3 daripada pergerakan dasar→puncak ex post.

### Gaps
- Tiada kajian bersemak rakan yang membandingkan secara langsung jalur %, jalur ATR, N-tutup, tempoh diam dan histeresis Schmitt pada **saham AS individu** pada ufuk swing.
- Butiran ujian Arthur Hill (StockCharts 2018) tidak dapat dibaca.

---

## 7. Konvensyen paparan dan sauh tarikh "sejak" (TradingView, StockCharts, SST, Moomoo, IBD, Finviz)

### Takeaway
Platform yang diperhatikan memaparkan **keadaan semasa tanpa tarikh onset**: SST `trend`, moomoo Technical Sentiment dan TradingView Technical Ratings. Pengecualian:
- penunjuk flip (Supertrend/PSAR/zigzag), yang menandakan **bar flip/pengesahan** pada carta;
- IBD, yang mengira **minggu dalam asas** dan **peringkat asas**.

Tiada piawai industri ditemui untuk "sejak bila". Cadangan: paparkan **dua tarikh**:
1. **tarikh pengesahan** (tiada look-ahead; asas kiraan "N sesi" dan sebarang pengukuran pulangan);
2. **tarikh pangsi/dasar** (bermula pergerakan sebenar), beserta % pergerakan sejak pangsi. Ini menunjukkan kelewatan dan sejauh mana harga sudah terlanjur.

### Cited Findings
- **Zigzag:** amaran boleh dicetus pada **bar pengesahan** (saat pangsi diketahui) atau pada ekstrem. Kaki terakhir repaint, dan pilihan bar tertutup disediakan. [AP] — [LuxAlgo: Zigzag](https://www.luxalgo.com/library/concept/zigzag-structure.md)
- **TradingView Pine Supertrend:** arah < 0 = naik; flip dikesan pada bar perubahan tanda (`ta.change`). Skrip pengesahan tutup bar mengelak flip intrabar. [AP] — [PineConnector](https://www.pineconnector.com/blogs/pico-blog/ppine-script-ta-supertrend-v5-guide); [TradingView scripts](https://kr.tradingview.com/scripts/bar-close-confirmed)
- **IBD:**
  - Kiraan peringkat asas (1, 2, 3, 4; tetap semula jika asas memecah paras rendah asas sebelumnya).
  - Panjang asas dalam **minggu** dikira dari minggu pertama tutup menurun hingga minggu sebelum tembusan.
  - Kegagalan meningkat pada peringkat lewat (~67% berjaya pada peringkat 3; ~80% gagal pada peringkat 4).
  - [AP] — [IBD via Yahoo](https://news.yahoo.com/counting-bases-helps-assess-buying-risk.html); [IBD via Yahoo: weeks](https://finance.yahoo.com/news/looking-great-chart-sure-count-203400677.html)
  - Skrip TradingView "Stage 2 Bases" meniru logik ini: kiraan bertambah apabila pergerakan dari asas > 20% (boleh diubah), dan ditetapkan semula ke 1 apabila asas memecah asas sebelumnya. [AP] — [TradingView: Stage 2 Bases](https://www.tradingview.com/script/xmsOHmVA-Stage-2-Bases/)
- **Bulkowski** mengukur prestasi/kegagalan dari **harga tembusan** (pengesahan), bukan dari dasar. [AP] — [thepatternsite](https://thepatternsite.com/FailureRates.html)
- **Minervini (tafsiran saringan):** belian dianggap **terlanjur** jika > 5% di atas pangsi. Ini konvensyen yang memaparkan jarak dari pangsi, bukan hari. [AP] — [MarketInOut](https://www.marketinout.com/stock-screener/minervini-buy-signal)
- **BOCPD** secara langsung menganggar "masa sejak titik perubahan terakhir" (panjang larian). [KK] — [arXiv 0710.3742](https://arxiv.org/pdf/0710.3742)
- **SST Terminal:** `technical_analysis` memulangkan `trend` (Uptrend / Constructive / Neutral / Downtrend) **tanpa medan tarikh onset atau tempoh**. [PS, nota terdahulu §2.10]
- **moomoo Technical Sentiment:** 3 label tanpa tarikh, dengan ambang tidak diterbitkan. [AP] — [moomoo manual](https://www.moomoo.com/us/manual/topic-14-60)
- **Weinstein:** peringkat 1–4 dilabel sebagai keadaan. Peralihan Peringkat 1 → 2 (tembusan atas SMA 30 minggu yang naik) dianggap titik onset. [AP] — [LuxAlgo: Weinstein](https://www.luxalgo.com/library/concept/weinstein-stage-analysis.md)
- **Contoh perbezaan sauh:** paras terendah SPX 2022 berbanding golden cross Feb 2023 = 77 sesi. Tarikh pengesahan dan tarikh pangsi boleh berbeza berbulan-bulan. [UV] — [Kagels Trading](https://kagels-trading.com/blog/golden-cross/)

### Inferences
- **[IN] Sauh yang disyorkan:**
  1. **Tarikh pengesahan (utama):** hari tutup t di mana syarat onset + H1 dipenuhi.
     - Dipakai untuk "sejak N sesi", untuk pengiraan pulangan/ujian (buka t+1), dan tidak pernah berubah selepas ditetapkan.
     - Konsisten dengan Bulkowski (ukur dari tembusan) dan amaran zigzag "pada pengesahan".
  2. **Tarikh pangsi (maklumat):**
     - bagi mula naik, `argmin C` dalam tetingkap dari tamat keadaan lawan terakhir (atau maksimum 60 sesi) hingga t;
     - bagi mula turun, `argmax C`.
     - Dikira pada t daripada data ≤ t, jadi tiada look-ahead. Dibekukan selepas itu.
     - Paparkan "+x% dari dasar" atau "x ATR dari dasar" untuk menunjukkan kelewatan dan sejauh mana harga terlanjur (analog peraturan 5% Minervini dan kiraan peringkat IBD).
  3. **Jangan sauh semula.** Jika C < pangsi selepas pengesahan, status menjadi "gagal" dan tarikh lama kekal dalam sejarah. Ini mengelak "repaint" tarikh onset yang mengelirukan pengguna dan backtest.
- **[IN] Format paparan (cadangan):**
  - Watchlist: `↗ Mula naik · 6 sesi (sah 17 Okt) · dasar 9 Okt, +8.2% / 2.6 ATR`
  - Selepas dinaik taraf: `Bullish · sejak 3 Sep (34 sesi)`
  - Selepas gagal: `✕ Mula naik gagal 21 Okt`
  - Posisi: label keadaan perlahan + lencana onset jika ada + jarak ke Chandelier (ATR), selaras dengan nota terdahulu §4.6. "Mula turun" bagi posisi dengan k = 4 **sama** dengan pencetus lorong 2, jadi paparkannya sebagai "lorong 2 tercetus", bukan label baharu.
  - "Sejak" bagi label keadaan perlahan (Bullish/Bearish/Neutral) = tarikh pengesahan larian semasa **selepas** histeresis. Kelipan yang ditapis H1/H3 tidak menetapkan semula kiraan.
- **[IN] Senibina label yang disyorkan:** kekalkan pill 3 keadaan (nota terdahulu §4.1) dan tambah **lencana onset sementara**. Jangan tambah tahap ke-4 atau ke-5.
  - Lencana "↗ Mula naik" aktif sehingga: (a) dinaik taraf apabila label perlahan menjadi Bullish; (b) gagal (H5); atau (c) tamat selepas 20 sesi tanpa naik taraf, ketika itu label kembali kepada keadaan perlahan.
  - Lencana "↘ Mula turun" adalah cermin.
  - Bagi kaedah pantulan (`kod/jenis_kaedah.csv`), "Mula naik" ialah pengesahan lantunan yang dijangka, dan "Bearish" semasa beli tidak diwarnakan sebagai amaran.
- **[IN] Pencetus lalai sementara untuk lencana** (sebelum ujian; pilih pemenang selepas ujian):
  - **Mula naik** jika semua syarat berikut benar pada 2 tutup berturut-turut (H1), dari keadaan bukan Bullish:
    - `C_t > max(C_{t−20}…C_{t−1})` (O1);
    - `C_t ≥ LLC_40 + 2.5×ATR_t` (LLC_40 = tutup terendah 40 sesi; pergerakan minimum, menolak tembusan julat sempit); dan
    - `ER20 ≥ 0.3` (O12; pilihan, uji dengan dan tanpa).
    - Sauh = tarikh LLC_40.
    - Gagal jika `C < LLC_40` atau `C < max(C_{t−20…t−1}) − 0.5×ATR` dalam 10 sesi.
  - **Mula turun** ialah cermin: `C_t < min(C_{t−20}…C_{t−1})` dan `C_t ≤ HHC_40 − 2.5×ATR_t`.
  - Alasan:
    - kelewatan dalam V simetri ~10 bar (Donchian 20), atau lebih cepat apabila pergerakan pantas melepasi 2.5 ATR;
    - komponen ATR menapis julat sempit;
    - sauh terbina dalam;
    - pergerakan 2.5 ATR < 4 ATR lorong 2, jadi onset muncul sebelum pergerakan setara satu hentian penuh.
  - Calon pesaing utama: **O8** (Chandelier songsang 4×ATR / 3×ATR), **O10** (Rebound Goulding: perlahan r_63 −, pantas r_10 +, zon mati 0.5σ√n), **O7** (1-2-3 zigzag 3×ATR), **O5a** (C > SMA50 + 0.5 ATR) dan **O13** (CUSUM k = 0.25, h = 4).
- **[IN] Protokol ujian ringkas** (melengkapkan protokol nota terdahulu §5):
  - (a) Kebenaran ex post = zigzag sampel penuh 4×ATR (atau 15%).
  - (b) Bagi setiap calon, laporkan:
    - kelewatan median (sesi) dari lembah ex post;
    - % pergerakan lembah→puncak yang sudah berlaku pada pengesahan;
    - kadar gagal dalam 10/20 sesi;
    - pulangan hadapan h = 5/10/21 dari buka t+1;
    - bilangan onset setiap 100 sesi;
    - P(lorong 2 tercetus dalam 10 sesi).
  - (c) Garis dasar: onset rawak dengan kekerapan sama.
  - (d) Pecahan: momentum lawan pantulan; ±5 hari earnings; rejim SPY > SMA200.
  - (e) Set S1–S4.
  - (f) Kunci senarai calon dan parameter **sebelum** melihat keputusan, untuk kawalan data snooping.

### Gaps
- Paparan "hari dalam trend" / "sejak" pada **Finviz, StockCharts dan Moomoo** tidak dapat disahkan, kerana domain tidak dapat dicapai dan carian tidak memberi hasil.
- Tandatangan rasmi `ta.barssince` / `ta.valuewhen` Pine tidak disahkan daripada rujukan rasmi. Dari pengetahuan umum, `ta.barssince(cond)` memulangkan bilangan bar sejak cond terakhir benar *(ingatan; sahkan)*.
- Tiada kajian empirikal ditemui tentang sauh mana (pengesahan atau pangsi) yang lebih membantu keputusan pengguna. Cadangan dua tarikh adalah inferens reka bentuk.
