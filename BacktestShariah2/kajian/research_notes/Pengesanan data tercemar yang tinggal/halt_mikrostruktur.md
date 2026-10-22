# Peristiwa mikrostruktur pasaran AS yang mengelirukan isian maya dan bar harian — cara mengesan dengan data percuma (hentian, LULD, MWCB, Rule 201, buka rasmi, hari separuh, odd lot, dagangan dibatalkan)

> Nota kaedah (penting untuk penulis laporan): Dalam sesi ini proksi rangkaian MENYEKAT nasdaqtrader.com (semua subdomain), nyse.com, sec.gov, finra.org, luldplan.com (termasuk cdn), ctaplan.com, utpplan.com, nasdaq.com, listingcenter.nasdaq.com, query1.finance.yahoo.com, openapi.futunn.com dan open.moomoo.com (curl: `CONNECT tunnel failed, response 403`; WebFetch: `ENOTFOUND`). Oleh itu dapatan di bawah datang daripada (a) ringkasan enjin carian (WebSearch) atas dokumen asal — fail PDF/halaman TIDAK dibaca penuh; (b) kod sumber `exchange_calendars` 4.13.2 yang dijalankan secara tempatan (PyPI/GitHub boleh dicapai); (c) satu panggilan baca-sahaja `quote_stock_quote` Moomoo (US.AAPL, 21 Okt 2026) untuk melihat medan sebenar. Tuntutan yang hanya daripada pengetahuan latar model ditanda **(belum disahkan)** dan tidak diletak dalam "Cited Findings". Runner GitHub Actions dijangka boleh mencapai nasdaqtrader.com, tetapi ini BELUM diuji dari sesi ini.

## 1. Data hentian (halt) Nasdaq Trader dan NYSE — suapan semasa, arkib sejarah, kod sebab, format, had kadar

### Takeaway
Satu-satunya sumber hentian percuma yang boleh dibaca mesin dan ditemui ialah suapan RSS Nasdaq Trader `rss.aspx?feed=tradehalts`; ia menyokong pertanyaan sejarah `&haltdate=mmddyyyy` dan `&resumedate=mmddyyyy`, jadi hentian semalam boleh diambil pagi esok. Fail sejarah hentian NYSE sendiri (TAQ NYSE Alerts) telah ditamatkan pada 2019 dan penggantinya berbayar; tiada had kadar rasmi ditemui, tetapi ada amaran sekatan jika permintaan berlebihan.

### Cited Findings
- Rentetan pertanyaan rasmi: hentian semasa `http://www.nasdaqtrader.com/rss.aspx?feed=tradehalts`; hentian sejarah `feed=tradehalts&haltdate=mmddyyyy`; "For securities halted for more than one day, the halt date reflected will be the first date it was halted"; parameter `resumedate` juga wujud dan boleh digabung — [Nasdaq Trader snippet "Query String"](https://NASDAQTrader.com/snippets/tradehaltaccordion.html); salinan berlabel "Historical Trade Halts" / "Trade Halts by Resumption Date" — [classic.nasdaqtrader.com](https://classic.nasdaqtrader.com/snippets/tradehaltaccordion.html)
- Medan item (ruang nama `ndaq:`) yang dibaca oleh penghurai pihak ketiga: IssueSymbol, HaltDate, HaltTime, ReasonCode, ResumptionDate, ResumptionTradeTime, PauseThresholdPrice, Market; item hentian yang masih berjalan mempunyai medan penyambungan kosong; item LULD yang telah disambung mempunyai PauseThresholdPrice dan ResumptionTradeTime terisi; suapan semasa boleh mengandungi hentian semasa dan lampau (perlu tapis tarikh); bentuk `?id=tradehalts` memberi 404, `?feed=tradehalts` 200 — [gitea SimplyTrading feed_parser.py](https://gitea.com/infrastructure_SC/SimplyTrading/src/branch/main/backend/halt_monitor/feed_parser.py); [tests.py](https://gitea.com/infrastructure_SC/SimplyTrading/src/branch/main/backend/halt_monitor/tests.py) (sumber tidak rasmi; bukan skema Nasdaq)
- Nasdaq mempunyai dokumen terma dan syarat khusus untuk suapan RSS hentian (kandungan tidak dapat dibaca) — [THRSSFeedTermsCond.pdf](https://m.nasdaqtrader.com/content/administrationsupport/agreementstrading/THRSSFeedTermsCond.pdf); pengumuman pelancaran suapan RSS hentian — [WatersTechnology](https://waterstechnology.com/node/1930135)
- Amaran forum: pelayan "may penalize excessive requests by banning the user" — simpan cache, jangan minta berulang setiap larian — [Wealth-Lab forum](https://wealth-lab.com/Forum/Posts/Stock-that-halted-39382)
- Kod disahkan daripada halaman kod hentian Nasdaq Trader (melalui petikan carian): **IPO1** = "IPO Issue not yet Trading"; **IPOQ** = "IPO security released for quotation" (sekuriti Nasdaq sahaja); **M1** = "Corporate Action"; **T12** = "Trading is halted pending receipt of additional information requested by NASDAQ" — [Nasdaq Trader Trading Halt Codes](https://nasdaqtrader.com/Trader.aspx?id=tradehaltcodes). Spesifikasi lama menamakan T12 "Trading Halted; For Information Requested by Listing Market" — [NQ Level 2 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQLevel2-V1_1.pdf)
- T1 = berita dinanti (material news dijangka dalam waktu pasaran); H10 = penggantungan dagangan SEC sehingga 10 hari; T5 (kod lama) = perubahan harga ≥ 10% dalam tempoh lima minit — [CFI "Stock Halt"](https://corporatefinanceinstitute.com/resources/capital-markets/stock-halt) (sekunder)
- LUDP = jeda dagangan volatiliti LULD; log pihak ketiga juga menggunakan kod **M** untuk jeda volatiliti dan melabelnya tidak konsisten — [Tapeboard 26 Ogos 2026](https://tapeboard.com/blog/trading-halts-2026-08-26); [Channelchek](https://dashboard.channelchek.com/tag/exchanges/) (sekunder)
- Tapeboard menerbitkan halaman hentian harian dengan "JSON data pack" dan menyatakan sumbernya "NASDAQ Trader tradehalts feed" — [Tapeboard halts 2026-10-02](https://tapeboard.com/halts/2026-10-02). Kiraan harian 2026 (semua harga, kebanyakannya LULD & T1): 48 saham pada 15 Okt 2026 — [Tapeboard](https://tapeboard.com/blog/trading-halts-2026-10-15); 50 pada 24 Ogos dan 13 Jul; 44 pada 29 Jun; 38 pada 30 Sep; 36 pada 17 Jul; 35 pada 7 Jul; 33 pada 26 Ogos — [Tapeboard 24 Ogos](https://tapeboard.com/blog/trading-halts-2026-08-24), [13 Jul](https://tapeboard.com/blog/trading-halts-2026-07-13), [29 Jun](https://tapeboard.com/blog/trading-halts-2026-06-29), [30 Sep](https://tapeboard.com/blog/trading-halts-2026-09-30), [17 Jul](https://tapeboard.com/blog/trading-halts-2026-07-17), [7 Jul](https://tapeboard.com/blog/trading-halts-2026-07-07), [26 Ogos](https://tapeboard.com/blog/trading-halts-2026-08-26)
- NYSE "permanently decommissioned the TAQ NYSE Alerts feed on August 21st, 2019" (sejarah 19 Mei 2003 – 21 Ogos 2019); maklumat setara kini dalam TAQ NYSE BBO dan TAQ NYSE Integrated (produk berlesen) — [NYSE TAQ Alerts](https://nyse.com/market-data/historical/taq-alerts)
- Options Analysis Suite mendakwa boleh mencari data hentian sejarah mengikut simbol (terma API tidak disahkan) — [Options Analysis Suite](https://www.optionsanalysissuite.com/trading-halts)
- Moomoo `quote_stock_quote` memulangkan medan `suspension` (boolean) dan `sec_status` (cth. `"NORMAL"`), serta `data_time` (ms, masa bursa) dan `data_date` — panggilan baca-sahaja US.AAPL pada 21 Okt 2026: `"sec_status":"NORMAL","suspension":false,"data_time":1792612800000` (= 16:00 ET 21 Okt 2026); penerangan alat: "security status/suspension/dark-pool status" — [Moomoo OpenAPI, alat `quote_stock_quote` (sesi ini)](https://open.moomoo.com/api/overview/)

### Inferences
- Senarai kod lain yang lazim dalam halaman Nasdaq (T2 berita dikeluarkan, T6 aktiviti luar biasa, T8 ETF, H4 tidak patuh, H9 tidak semasa, H11 kebimbangan kawal selia, LUDS jeda LULD "straddle", MWC1/MWC2/MWC3 pemutus litar seluruh pasaran tahap 1–3, MWC0 bawaan dari hari sebelum, MWCQ penyambungan MWCB, IPOE lanjutan tetingkap penentududukan IPO, M2 sebut harga tiada, O1 hentian operasi, D pemadaman sekuriti, R4/R9/C3/C4/C9/C11 kod penyambungan) — **(belum disahkan)**; penulis perlu menyemak terus `Trader.aspx?id=TradeHaltCodes` dari runner Actions.
- Medan `Market` dan fakta bahawa Tapeboard memaparkan hentian LULD saham tersenarai NYSE daripada suapan ini menunjukkan suapan Nasdaq meliputi hentian semua bursa penyenaraian AS — inferens, belum disahkan secara rasmi.
- Reka bentuk yang disyorkan untuk sistem (Actions, percuma): (1) setiap larian 9:35 NY dan selepas tutup (≈16:15 NY) ambil `feed=tradehalts` dan simpan XML mentah ke repo (arkib sendiri, kerana kedalaman sejarah pelayan tidak diketahui); (2) larian pagi esok ambil `haltdate=<semalam>` dan `resumedate=<hari ini>` untuk menangkap hentian berbilang hari; (3) cantum dengan alam ~2,000 saham mengikut simbol + tarikh; (4) sebagai pemeriksa kedua di 9:35, guna `suspension`/`sec_status` dan `volume`/`data_date` dalam sebut harga Moomoo yang sudah diambil.
- Kesan pada isian: hentian T1/T12/H10/M1/IPO yang meliputi 9:30 bermakna tiada buka biasa — "buka rasmi" hari itu ialah harga lelongan pembukaan semula (atau tiada bar langsung untuk H10 berbilang hari); sebut harga 9:35 akan menunjukkan harga tutup semalam (basi) dengan volum sesi biasa 0.

### Gaps
- Skema rasmi RSS (format HaltTime, zon masa, senarai nilai Market), kedalaman sejarah `haltdate` dan had kadar rasmi — tidak dapat dibaca (domain disekat). Perlu diuji dari runner Actions.
- Sama ada format suapan berubah pada 2025–2026 (kewujudan subdomain `classic.nasdaqtrader.com` membayangkan migrasi laman) — tidak disahkan.
- Halaman hentian semasa percuma NYSE (format JSON/CSV) — tidak ditemui/tidak disahkan.

## 2. Buka rasmi (Nasdaq Opening Cross / lelongan pembukaan NYSE) lawan 'Open' Yahoo lawan cetakan pertama lawan sebut harga 9:35; maksud 'open' kline Moomoo

### Takeaway
Buka rasmi Nasdaq (NOOP) = harga Opening Cross; jika tiada cross, cetakan pertama yang layak "last-sale" pada/selepas 9:30. Vendor berbeza — sebahagian memberi cetakan pertama disatukan (consolidated), sebahagian harga lelongan bursa utama — dan tiada dokumentasi Yahoo ditemui; magnitud dan kekerapan perbezaan tidak diterbitkan, jadi mesti diukur sendiri. Sebut harga 9:35 ialah harga lima minit selepas buka, bukan harga buka.

### Cited Findings
- "The securities' Nasdaq Opening Cross price is the Nasdaq Official Opening Price ('NOOP')"; jika tiada Opening Cross, NOOP = "first last-sale eligible trade reported at or after 9:30 a.m."; jika tiada kepentingan kontra, Nasdaq melaksanakan "null cross" dan NOOP ditetapkan oleh cetakan pertama; julat harga cross = lebih besar antara $0.50 atau 10% (ETP 5%) — [Nasdaq Opening/Closing Cross FAQ](https://www.nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf); [SEC 34-72226](https://www.sec.gov/file/34-72226)
- Pelepasan SEC 2004: NOOP ketika itu sama dengan harga dagangan pertama Nasdaq Market Center — peraturan LAMA, telah digantikan — [SEC 34-50602](https://www.sec.gov/file/34-50602)
- Forum pengamal: buka "rasmi" ialah dagangan lelongan pembukaan bursa utama, tetapi "data providers do not report this trade as they do for settled close"; "all providers, except one, that I know of returns the first full trade" — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/9345/opening-closing-auction-prices-20tb-200m-files-and-640-cores/p1); [Wealth-Lab forum](https://wealth-lab.com/Forum/Posts/GetSessionOpen-returns-exchange-39-s-official-open-40226)
- Perbezaan vendor dikaitkan dengan harga "primary market" lawan "consolidated market" — [Stocks & Commodities Q&A](https://store.traders.com/stcov272qaby1.html)
- Contoh analogi pada penutup (tidak disahkan): dagangan akhir waktu biasa $53.18 lawan lelongan penutup $53.20 — [Elite Trader](https://elitetrader.com/et/threads/question-about-yahoo-vs-google-closing-price.336715/)
- Panduan sekunder menyatakan 'open' Yahoo untuk saham Nasdaq mencerminkan mekanisme open cross; bukan dokumentasi Yahoo — [factually.co](https://factually.co/fact-checks/finance/verify-historical-stock-opening-price-nasdaq-yahoo-finance-step-by-step-0a86c9)
- Yahoo: sebut harga "real-time" untuk banyak bursa tetapi "not all markets will stream in real-time"; semak cap masa pada halaman sebut harga — [Yahoo Help SLN2321](https://help.yahoo.com/kb/SLN2321.html)
- Moomoo/Futu: `get_cur_kline(code, num, ktype=KLType.K_DAY, autype=AuType.QFQ)` memerlukan langganan, `num` ≤ 1000 — [Futu API doc get-kl](https://openapi.futunn.com/futu-api-doc/quote/get-kl.html); rekod tolakan KLINE membawa `open_price` — [Moomoo push data format](https://open.moomoo.com/api/quote/push/data-format). Tiada dokumentasi sama ada pra-pasaran masuk ke 'open'.
- Sebut harga Moomoo memisahkan sesi biasa daripada lanjutan: medan `open_price`/`high_price`/`low_price`/`volume` sesi biasa berasingan daripada objek `pre_market`, `after_market` dan `overnight` (US.AAPL 21 Okt 2026: `open_price` 339.36 manakala `pre_market.high_price` 339.5 / `low_price` 332.71; `prev_close_price` 339.5) — [Moomoo `quote_stock_quote` (panggilan sesi ini)](https://open.moomoo.com/api/overview/)

### Inferences
- Bukti Moomoo di atas menunjukkan `open_price` sebut harga = buka sesi biasa (pra-pasaran dalam sub-objek berasingan). Ini menyokong menggunakan `open_price` sebut harga 9:35 (bukan `last_price`) sebagai harga belian sementara — perlu disahkan untuk kline harian `get_cur_kline`/`request_history_kline`.
- Pada 9:35 buka rasmi biasanya sudah diketahui (cross Nasdaq berlaku 9:30), jadi rekod sementara boleh hampir sama dengan buka rasmi jika medan `open_price` diambil; menggunakan `last_price` 9:35 memasukkan pergerakan 5 minit pertama (paling volatil dalam hari) sebagai ralat.
- Ujian "belum diniaga pada 9:36" patut berdasarkan `volume` sesi biasa > 0 DAN `data_date` = hari ini DAN `suspension` = false, bukan harga (harga basi = tutup semalam).
- Peraturan pengesahan esok pagi yang disyorkan: buka rasmi = 'Open' Yahoo; tanda bar jika |Open Yahoo / open Moomoo − 1| > 0.5% (ambang perlu dikalibrasi daripada data sendiri), atau Open di luar [Low, High], atau Open = tutup semalam dengan volum 0.

### Gaps
- Kekerapan dan magnitud perbezaan 'Open' Yahoo lawan buka rasmi bursa utama — TIADA sumber diterbitkan ditemui; perlu diukur daripada data sistem sendiri (rekod 9:35 lawan buka rasmi lawan open Moomoo).
- Definisi rasmi 'open' kline harian Moomoo untuk saham AS (adakah cetakan pertama disatukan atau harga lelongan) — tidak didokumenkan dalam sumber yang dicapai.
- Pembekal data Yahoo untuk sebut harga AS masa nyata — tidak ditemui.

## 3. Pembukaan lewat (delayed openings, ketidakseimbangan) dan pecahan saham yang belum berdagang pada 9:35

### Takeaway
Pada hari biasa hampir semua saham besar dibuka dalam beberapa saat selepas 9:30, tetapi pada hari volatiliti ekstrem pecahan besar saham NYSE dibuka selepas 9:35 (62% saham S&P 500 tersenarai NYSE pada satu hari Rule 48; 1,954 saham NYSE pada 24 Ogos 2015). Tiada statistik hari biasa yang diterbitkan ditemui.

### Cited Findings
- Analisis Instinet atas satu hari Rule 48 (peruntukan pembukaan lewat NYSE dalam volatiliti ekstrem): 62% nama S&P 500 tersenarai NYSE dibuka selepas 9:35; NYSE berhenti menyebarkan cetakan indikatif pada 9:35 — [Instinet "Man vs Machine"](https://instinet.com/sites/default/files/pdf_articles/Man_vs_Machine.pdf)
- 24 Ogos 2015: 1,954 saham tersenarai NYSE gagal dibuka menjelang 9:35 — [Surat komen SEC 4-631-40](https://www.sec.gov/comments/4-631/4631-40.pdf)
- 19 Okt 1987: 95 saham S&P 500 dan 11 daripada 30 saham DJIA dibuka lewat — [Black Monday (SPARC)](https://scalar.sparcinla.org/great-wall-institute/media/black-monday)
- Citadel Securities (DMM NYSE, satu firma, sampel Mei, tahun artikel tidak disahkan): 89% masa saham dimulakan dalam 3 saat selepas 9:30; "broker holds" menyumbang ~25% kes saham tidak dapat dibuka serta-merta — [Markets Media](https://articles.marketsmedia.com/citadel-kicks-role-nyse-floor-promptness-push)
- Nasdaq: jika tiada kepentingan kontra → "null cross" dan dagangan biasa bermula; NOOP = cetakan pertama — [Nasdaq Cross FAQ](https://www.nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf)

### Inferences
- Bagi alam ≥ $10 yang cair, "belum diniaga pada 9:36" pada hari biasa hampir selalu bermakna salah satu: (a) hentian T1/T12/H10/M1 meliputi pembukaan; (b) pembukaan lewat NYSE oleh DMM kerana ketidakseimbangan (selalunya selepas berita/earnings pra-pasaran — tepat jenis saham yang menjana isyarat jurang); (c) hari volatiliti seluruh pasaran; (d) saham tidak cair (sudah ditapis `tidak_layak.py`). Ini bukan rawak — ia berkorelasi dengan berita, jadi melangkau dalam satu lejar dan membeli pada buka rasmi dalam lejar lain menghasilkan bias pemilihan antara lejar.
- Peraturan disyorkan (satu peraturan untuk semua lejar): jika saham dihentikan pada 9:30 (ada rekod hentian dengan HaltTime ≤ 9:30 dan penyambungan > 9:35, atau `suspension` true pada 9:35) → tanda `buka_lewat`; sama ada (i) langkau di SEMUA lejar, atau (ii) beli pada buka rasmi (harga lelongan pembukaan semula) di SEMUA lejar dengan bendera, tetapi jangan campur. Pilihan (ii) lebih jujur kepada isyarat tetapi tidak boleh dilaksana secara sebenar pada 9:35.

### Gaps
- Pecahan saham ≥ $10 yang belum berdagang pada 9:35 pada hari biasa 2025–2026 — tiada sumber; boleh diukur sendiri daripada bar 1 minit (yfinance/Moomoo) atau daripada `volume` sebut harga 9:35 yang sudah dikumpul.
- Masa pembukaan paling lewat yang dibenarkan peraturan NYSE (Rule 7.35A/Rule 48) dalam 2026 — tidak dapat dibaca.

## 4. LULD (jalur harga, kekerapan jeda) dan pemutus litar seluruh pasaran (MWCB); cara mengesan daripada OHLCV harian; cara mengisi henti rugi semasa jeda

### Takeaway
LULD: jalur ±5% (Tier 1: S&P 500, Russell 1000, ETP terpilih) atau ±10% (Tier 2) bagi harga > $3, sekitar purata harga 5 minit terdahulu; keadaan had 15 saat → jeda 5 minit, dibuka semula melalui lelongan bursa utama dan boleh dilanjutkan dalam tambahan 5 minit. Penggandaan jalur pada pembukaan dihapus sejak Amendment 18 (24 Feb 2020) — dokumen yang menyebut "doubled during the first 15 minutes" sudah lapuk. OHLCV harian tidak boleh membuktikan jeda; gunakan suapan hentian (LUDP + PauseThresholdPrice). MWCB: 7%/13%/20% indeks S&P 500 berbanding tutup semalam.

### Cited Findings
- Tier 1 = semua sekuriti S&P 500, Russell 1000 dan ETP terpilih — [LULD 2025 Annual Report](https://cdn.luldplan.com/reports/LULD-2025-Annual-Report.pdf) (melalui petikan carian)
- Jadual Nasdaq FAQ: Tier 1 5% dan Tier 2 10% bagi tutup sebelumnya > $3.00 (jadual pra-Amendment 18) — [Nasdaq LULD FAQ](https://m.nasdaqtrader.com/content/MarketRegulation/LULD_FAQ.pdf); ringkasan sekunder: ±20% bagi $0.75–$3.00, sehingga ±75% bawah $0.75 — [Tapeboard glossary LULD](https://tapeboard.com/blog/glossary-what-is-a-limit-up-limit-down-rule)
- Harga rujukan selepas buka = purata aritmetik dagangan dalam tetingkap 5 minit terdahulu; keluar keadaan had jika semua sebut harga keadaan had dilaksana/dibatal dalam 15 saat, jika tidak bursa utama mengisytiharkan jeda 5 minit — [NYSE ETF Volatility Fact Sheet](https://www.nyse.com/publicdocs/nyse/products/etp-funds/ETF_NYSE_Volatility_Fact_Sheet.pdf) (dokumen sama menyatakan jalur digandakan pada 15 minit pertama dan 25 minit terakhir — LAPUK, lihat baris seterusnya)
- Amendment 18 (dijangka berkuat kuasa 24 Feb 2020) menghapus penggandaan jalur selepas pembukaan bagi semua sekuriti; antara 3:35–4:00 p.m., Tier 1 dan Tier 2 berharga rujukan ≤ $3.00 masih menggunakan parameter berganda — [Cboe LULD Amendment 18 Update](https://www.cboe.com/document/tech-spec/content/technical-specifications/cboe-limit-updown-faq/luld-amendment-18-update)
- Pembukaan semula Nasdaq: tempoh paparan sahaja 5 minit, kolar lelongan daripada jalur LULD semasa jeda; jeda dilanjutkan dalam tambahan lima minit jika kriteria pembukaan semula tidak dipenuhi, kolar dilebarkan setiap lanjutan; bagi jeda had atas, kolar atas = rujukan + 5% (lantai $0.15 bagi ≤ $3) — [SEC 34-88383 (Nasdaq 2020)](https://www.sec.gov/files/rules/sro/nasdaq/2020/34-88383.pdf); [SEC 34-79876 (Nasdaq 2017)](https://www.sec.gov/files/rules/sro/nasdaq/2017/34-79876.pdf)
- Amendment 12 (diluluskan Jan 2017, pelaksanaan S3 2017): jeda berterusan sehingga bursa penyenaraian utama membuka semula, walaupun melebihi 10 minit; NYSE/NYSE American membuka semula melalui DMM, bukan lelongan elektronik — [NYSE ETF Fact Sheet Amendment 12](https://www.nyse.com/publicdocs/nyse/products/etp-funds/ETF_Fact_Sheet_Amendment_12.pdf)
- DERA (Moise & Flaherty, Mac 2017): berbanding era SSCB, kekerapan jeda MENINGKAT bagi Tier 2 tetapi MENURUN bagi Tier 1 — [SEC DERA white paper](https://www.sec.gov/dera/staff-papers/white-papers/10mar17moiseflahertyluld)
- DERA (Hughes, Dis 2017): kekerapan jeda jatuh > 75% selepas Amendment 10; penurunan terbesar bagi Tier 2 dan dalam 30 minit pertama hari dagangan — [SEC DERA Amendment 10](https://www.sec.gov/dera/staff-papers/white-papers/dera_wp_effect_of_amendment_10_of_luld_pilot_plan)
- 24 Ogos 2015: jeda LULD ETF berpunca daripada lonjakan volum dan penarikan bekalan kecairan — [SEC DERA Feb 2016](https://www.sec.gov/about/divisions-offices/division-economic-risk-analysis/staff-papers-analyses/feb2016-dera-white-paper-etf-volatility)
- Laporan Tahunan LULD 2025 membandingkan keadaan had, jeda dan keadaan straddle dengan tahun sebelum; taburan berkait dengan Tier dan status ETP (angka tidak dapat dibaca) — [LULD 2025 Annual Report](https://cdn.luldplan.com/reports/LULD-2025-Annual-Report.pdf)
- Dagangan odd lot tidak tertakluk kepada LULD dan tidak mencetuskan hentian — [SEC Release 34-70794 (pindaan CTA odd lot)](https://www.sec.gov/file/rel-no-34-70794)
- MWCB: ambang 7% (Tahap 1), 13% (Tahap 2), 20% (Tahap 3) diukur berbanding tutup S&P 500 hari sebelumnya — [Federal Register 2020-06101](https://public-inspection.federalregister.gov/2020-06101.pdf); Tahap 1/2 = hentian 15 minit, tetapi jika dicapai pada/selepas 3:25 p.m. ET dagangan diteruskan; Tahap 3 = hentian untuk baki hari — [Questrade](https://www.questrade.com/learning/markets-economy/market-wide-circuit-breakers); [Nasdaq 2020](https://www.nasdaq.com/articles/where-circuit-breakers-kick-in-today-2020-03-08)

### Inferences
- Jalur 5% (Tier 1) bermakna jeda boleh berlaku hanya dengan pergerakan ~5% dalam < 5 minit — biasa pada saham besar selepas berita; bagi Tier 2 ~10%. Julat harian tidak membuktikan jeda (pergerakan perlahan sepanjang hari tidak mencetuskan). Pengesanan praktikal: tanda calon bar jika |Open/Close semalam − 1| atau (High−Low)/Close semalam ≥ 5% (Tier 1) / 10% (Tier 2), kemudian sahkan dengan rekod LUDP/LUDS dalam suapan hentian hari itu (PauseThresholdPrice = paras jalur ketika jeda).
- Isian henti rugi (posisi beli) yang disyorkan untuk penguji bar harian: (1) jika Open ≤ henti → isi pada Open (jurang menembusi henti, bukan pada harga henti); (2) jika jeda LUDP had bawah berlaku dan henti terletak antara PauseThresholdPrice dan harga pembukaan semula → isi pada harga pembukaan semula (cetakan pertama selepas ResumptionTradeTime, daripada bar 1 minit), bukan pada henti; (3) jika harga pembukaan semula tidak diperoleh → isi konservatif pada min(henti, Low hari) dan tanda `isian_anggaran`. Bar 1 minit percuma yfinance hanya meliputi tempoh terkini (had tepat **belum disahkan**), jadi tangkap bar 1 minit pada malam yang sama bagi setiap posisi yang ada rekod hentian.
- Lorong 2 sistem (Chandelier atas harga tutup, jual pada buka esok) tidak terdedah kepada isian dalam jeda; yang terdedah ialah henti kaedah berasaskan Low harian.
- MWCB Tahap 3 sebelum tutup: tiada lelongan penutup biasa, jadi "keluar masa pada tutup" sebenarnya pada harga terakhir sebelum hentian — **(belum disahkan)**; perlu peraturan khas jika berlaku.

### Gaps
- Kiraan jeda LULD 2024–2025 mengikut Tier dan peratus dalam 15/30 minit pertama — laporan tahunan wujud tetapi tidak dapat dibaca (domain disekat).
- Teks pelan LULD semasa (pindaan selepas Amendment 18, jika ada pada 2023–2026) dan jalur tepat < $3 — tidak disahkan.
- Had sejarah bar 1 minit yfinance pada 2026 — tidak disahkan.

## 5. Rule 201 (Short Sale Restriction / SSR): pencetus, tempoh, senarai harian percuma, kesan pada strategi pantulan

### Takeaway
SSR dicetuskan apabila harga turun ≥ 10% daripada tutup hari sebelumnya (ditentukan pasaran penyenaraian), berkuat kuasa sehingga tutup hari dagangan berikutnya; jualan singkat hanya dibenarkan di atas bida terbaik nasional. Nasdaq Trader mempunyai bahagian "Circuit Breaker List", tetapi nama/format fail harian tidak dapat disahkan; proksi daripada bar harian mudah dibina. SSR tidak menjejaskan isian beli secara langsung — ia ciri keadaan pasaran untuk isyarat pantulan.

### Cited Findings
- Rule 201 ialah pemutus litar jualan singkat yang mengehadkan harga jualan singkat apabila dicetuskan; trading center mesti menyekat jualan singkat pada atau di bawah bida terbaik nasional apabila saham jatuh ≥ 10% daripada tutup hari sebelumnya — [SEC Final Rule 34-61595](https://www.sec.gov/rules/final/34-61595.htm); tarikh pematuhan 28 Feb 2011 — [Nasdaq Trader Reg SHO](https://www.nasdaqtrader.com/Trader.aspx?id=regsho)
- "If the Short Sale Price Test is triggered ... the Short Sale Price Test shall remain in effect until the close of trading on the next trading day"; jika harga jatuh lagi ≥ 10% intrahari pada hari sudah tertakluk, sekatan dicetuskan semula; jika tiada dagangan di bursa pada hari sebelumnya, harga pencetus berdasarkan jualan terakhir hari dagangan terkini — [Nasdaq Reg SHO FAQ (10 Mac 2011)](https://m.nasdaqtrader.com/content/marketregulation/regsho/regshoFAQs.pdf); [SEC 34-63906](https://www.sec.gov/file/34-63906)
- Halaman Reg SHO Nasdaq Trader mempunyai bahagian "Circuit Breaker List" (selain "Pilot List" sejarah) — [Nasdaq Trader Regulation SHO](https://www.nasdaqtrader.com/Trader.aspx?id=regsho)
- Alat masa nyata Nasdaq "Short Sale Monitor" (amaran saham masuk senarai circuit breaker) berbayar $750/MPID/bulan — [Nasdaq SMM factsheet](https://www.nasdaqtrader.com/content/productsservices/trading/smm_factsheet.pdf)
- Nasdaq menerbitkan fail teks harian volum jualan singkat (pipe-delimited, `EEEEshYYYYMMDD.txt`, ftp.nasdaqtrader.com/files/shortsaledata) — data berbeza daripada senarai SSR — [Nasdaq Short Sale File Specifications](https://m.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/ShortSaleFileSpecifications.pdf)
- Dagangan odd lot pada pita "would not trigger short sale restrictions or trading halts" — [SEC Release 34-70794](https://www.sec.gov/file/rel-no-34-70794)
- Kajian kesan Rule 201 (kandungan tidak dibaca) — [EFMA 2011 "Short-Selling: The Impact of SEC Rule 201 of 2010"](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2011-Braga/papers/0393.pdf); [Tesis Erasmus](https://thesis.eur.nl/pub/24842)

### Inferences
- Proksi bar harian: `ssr_cetus(D) = Low(D) ≤ 0.90 × Close_rasmi(D−1)`; SSR aktif pada baki D dan sepanjang D+1. Low vendor yang mengecualikan odd lot selari dengan peraturan pencetus (odd lot tidak mencetus). Isyarat "pantulan" selepas kejatuhan ≥ 10% hampir selalu dijana pada hari SSR dan dibeli pada D+1 ketika SSR masih aktif — rekod `ssr_aktif` sebagai ciri analisis (jangan dijadikan penapis tanpa ujian).
- Kesan pada isian maya: tiada (sistem beli sahaja). Kesan pada isyarat: mungkin mengurangkan tekanan jual pada D+1 — tiada bukti kuantitatif dibaca.

### Gaps
- Nama fail/URL senarai SSR harian percuma Nasdaq (jika masih diterbitkan pada 2026) dan setara NYSE/Cboe — tidak disahkan (laman disekat; carian tidak menemui nama fail).
- Sama ada dagangan pra/pasca-pasaran boleh mencetuskan SSR — tidak disahkan.
- Saiz kesan SSR terhadap pulangan pantulan — kertas tidak dibaca.

## 6. Kalendar cuti dan tutup awal NYSE/Nasdaq 2026 (dan 2027–2028); pengendalian `exchange_calendars`; penutupan tidak berjadual

### Takeaway
2026: 10 cuti penuh, tutup awal 1:00 p.m. ET pada 27 Nov dan 24 Dis 2026 (tiada tutup awal 2 Jul 2026 kerana 4 Jul jatuh Sabtu, cuti diganti Jumaat 3 Jul). `exchange_calendars` 4.13.2 (XNYS = XNAS) sepadan dengan pengumuman NYSE dan mengandungi penutupan ad hoc lalu, tetapi julat lalai kalendar hanya sehingga hari ini + 1 tahun — sesi selepas itu kelihatan "hilang" kecuali `end=` diberi.

### Cited Findings
- NYSE: tutup awal 1:00 p.m. (opsyen layak 1:15 p.m.) pada Jumaat 27 Nov 2026, Jumaat 26 Nov 2027 dan Jumaat 24 Nov 2028 (hari selepas Thanksgiving); Krismas 2027 jatuh Sabtu, maka pasaran tutup Jumaat 24 Dis 2027; Hari Kemerdekaan 2027 diganti Isnin 5 Jul — [Business Wire: NYSE Group Announces 2026, 2027 and 2028 Holiday and Early Closings Calendar (23 Dis 2025)](https://www.businesswire.com/news/home/20251223981478/en/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar); [ICE IR](https://ir.theice.com/press/news-details/2025/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar/); [NYSE Hours & Calendars](https://www.nyse.com/markets/hours-calendars)
- NYSE dan Nasdaq tutup awal pada 27 Nov dan 24 Dis 2026; Thanksgiving Khamis 26 Nov, Krismas Jumaat 25 Dis 2026 — [Fidelity](https://www.fidelity.com/learning-center/smart-money/stock-market-holidays)
- `exchange_calendars` 4.13.2 (keluaran PyPI terkini semasa semakan) dijalankan tempatan, kalendar XNYS — [PyPI exchange-calendars](https://pypi.org/project/exchange-calendars/); [kod sumber XNYS](https://raw.githubusercontent.com/gerrymanoim/exchange_calendars/master/exchange_calendars/exchange_calendar_xnys.py):
  - Cuti hari bekerja 2026: 1 Jan, 19 Jan, 16 Feb, 3 Apr (Good Friday), 25 Mei, 19 Jun, 3 Jul, 7 Sep, 26 Nov, 25 Dis.
  - Tutup awal 2026: 27 Nov dan 24 Dis, 13:00 ET; 2 Jul 2026 = sesi penuh 16:00.
  - 2027: cuti 1 Jan, 18 Jan, 15 Feb, 26 Mac, 31 Mei, 18 Jun, 5 Jul, 6 Sep, 25 Nov, 24 Dis; tutup awal 26 Nov 2027 sahaja.
  - 2028: tutup awal 3 Jul 2028 dan 24 Nov 2028.
  - Sesi 2026 XNAS identik dengan XNYS.
  - Penutupan ad hoc yang ada dalam kalendar: 9 Jan 2025, 5 Dis 2018, 29–30 Okt 2012 ditanda TUTUP; 3 Jul, 28 Nov, 24 Dis 2025 = tutup 13:00.
  - Kod sumber: `regular_early_close = time(13)`; docstring: "Until 1993, the standard early close time for the NYSE was 2:00 PM. From 1993 onward, it has been 1:00 PM"; penutupan khas ditakrif melalui `special_closes` dan `special_closes_adhoc`.
  - `get_calendar('XNYS')` tanpa argumen memberi `last_session` 2027-10-22 (hari ini + 1 tahun) — semua hari bekerja selepas tarikh itu dilaporkan bukan sesi; perlu `get_calendar('XNYS', start=..., end=...)`.

### Inferences
- Sebab penutupan ad hoc (9 Jan 2025 = hari berkabung Presiden Carter; 5 Dis 2018 = Presiden G.H.W. Bush; 29–30 Okt 2012 = Taufan Sandy) — **(belum disahkan dalam sumber dibaca)**, tarikh disahkan oleh kalendar.
- Penutupan tidak berjadual diumumkan dengan notis pendek; `exchange_calendars` hanya mengetahuinya selepas keluaran baharu. Peraturan: Actions memasang versi terkini setiap larian (jangan pin terlalu lama), dan semak silang dengan `quote_trading_days` Moomoo (alat ini wujud dalam senarai alat Moomoo sesi ini) serta kehadiran bar SPY hari itu.
- Pada hari tutup awal: "keluar masa pada tutup" = tutup 13:00; skrip yang menganggap 16:00 ET (cth. tetingkap pengambilan selepas tutup) mesti guna `session_close`. Volum hari separuh lebih rendah — penapis kecairan 20 bar dan ATR14 sedikit terjejas (median tahan lasak).
- Gangguan teknikal bursa (cth. NYSE berhenti beberapa jam pada Jul 2015 — **belum disahkan**) tidak menghapus sesi tetapi boleh mengubah cara harga tutup rasmi ditentukan.

### Gaps
- Tingkah laku Yahoo/Moomoo pada hari cuti/separuh hari (baris rata OHLC = tutup semalam dengan volum 0, atau baris hilang) — tiada sumber ditemui; perlu ujian empirikal (cari bar dengan Open=High=Low=Close dan Volume=0 pada tarikh bukan sesi menurut kalendar).
- `pandas_market_calendars` (versi 5.5.0 di PyPI) tidak diuji; dokumentasi tidak dibaca.

## 7. Dagangan "clearly erroneous" yang dibatalkan (bust) selepas fakta — garis panduan, kekerapan mengubah High/Low, cara mengesan

### Takeaway
Garis panduan berangka (waktu biasa): 10% (≤ $25), 5% ($25–50), 3% (> $50) daripada harga rujukan; digandakan di luar waktu biasa. Sejak 2022 peraturan dijadikan kekal dan semakan semasa waktu biasa dihadkan kerana LULD — dagangan dalam jalur LULD lazimnya kekal; jadi bust yang mengubah High/Low sesi biasa saham ≥ $10 dijangka jarang. Tiada statistik kekerapan semakan semula High/Low vendor ditemui; kesan dengan memuat turun semula dan membanding.

### Cited Findings
- Waktu biasa: dagangan dibatalkan hanya jika harga melebihi harga rujukan (biasanya jualan terakhir disatukan) sebanyak ≥ 10% jika ≤ $25.00, 5% jika > $25 hingga $50, 3% jika > $50 — [SEC 34-95259 Ex.5 (Cboe BZX 2022)](https://www.sec.gov/files/rules/sro/cboebzx/2022/34-95259-ex5.pdf); [SEC 34-82945 Ex.5 (NYSE 2018)](https://www.sec.gov/files/rules/sro/nyse/2018/34-82945-ex5.pdf); [SEC 34-65111 Ex.5 (NYSE 2011)](https://www.sec.gov/files/rules/sro/nyse/2011/34-65111-ex5.pdf)
- Sesi awal/pra-buka/selepas waktu: 20% / 10% / 6% bagi jalur harga yang sama; Multi-Stock Event: 10%; peristiwa ≥ 20 sekuriti: peraturan 30%; ETF berleveraj: garis panduan didarab gandaan leveraj — [SEC 34-95259 Ex.5](https://www.sec.gov/files/rules/sro/cboebzx/2022/34-95259-ex5.pdf); [Federal Register 2010-23076](https://www.federalregister.gov/documents/2010/09/16/2010-23076/self-regulatory-organizations-bats-exchange-inc-nasdaq-omx-bx-inc-chicago-board-options-exchange)
- 1 Sep 2022: SEC meluluskan Cboe BZX menjadikan program perintis Clearly Erroneous Executions kekal, dengan semakan waktu biasa dihadkan kerana Pelan LULD sudah memberi perlindungan serupa; maklum balas industri mahukan kepastian bahawa dagangan dalam Price Bands kekal — [Federal Register 2022-21560](https://public-inspection.federalregister.gov/2022-21560.pdf); [SEC 34-95902](https://www.sec.gov/file/34-95902); bursa lain memfail peraturan serupa — [SR-BX-2022-017](https://listingcenter.nasdaq.com/assets/rulebook/nasdaqtx/filings/SR-BX-2022-017_Notice_Approval.pdf); [MEMX, Federal Register 2022-20144](https://govinfo.gov/content/pkg/FR-2022-09-19/pdf/2022-20144.pdf)
- Fail LTSE: pesanan pelabur "either not executed at clearly erroneous prices or are subsequently busted" — laluan bust masih wujud bagi dagangan di luar jalur — [SEC 34-95883](https://www.sec.gov/file/34-95883)
- DERA menilai kekerapan dagangan clearly erroneous sebelum/selepas LULD (angka tidak dibaca) — [SEC DERA Moise & Flaherty 2017](https://www.sec.gov/dera/staff-papers/white-papers/10mar17moiseflahertyluld)
- Nasdaq mempunyai borang pemfailan Clearly Erroneous dalam talian — [Nasdaq Trader CE Form](https://www.nasdaqtrader.com/EASP/TraderEASP.aspx?id=CEForm)

### Inferences
- Bagi bar sesi biasa yfinance (lalai `prepost=False`), cetakan pra-pasaran yang dibatalkan tidak sepatutnya menyentuh High/Low; risiko lebih besar ialah cetakan salah vendor (tick buruk) yang tidak pernah dibatalkan secara rasmi, dan vendor yang memasukkan dagangan lanjutan dalam bar harian.
- Pengesanan yang disyorkan: simpan petikan bar pertama (tarikan selepas 00:20 UTC) dan muat turun semula pada T+1 dan T+5; bandingkan H/L/O/C/V; tanda jika berubah > 0.1% atau > $0.02; tanda juga jika High/Low Yahoo dan Moomoo berbeza > 0.5%. Henti rugi yang dicetuskan oleh Low yang kemudian disemak semula perlu dinilai semula (versi bar terakhir menang, dengan log).
- Ujian kewarasan bar: Low < min(Open, Close) × (1 − k) dengan k besar dan tanpa rekod hentian → calon tick buruk; sahkan dengan sumber kedua sebelum mencetus henti.

### Gaps
- Kekerapan High/Low harian disemak semula selepas penerbitan pertama (Yahoo atau Moomoo) — TIADA sumber ditemui.
- Nombor peraturan FINRA 11891/11892 dan had masa pemfailan (cth. 30 minit) — tidak dapat disahkan (finra.org disekat).

## 8. Odd lot, syarat dagangan (trade conditions) dan kelayakan High/Low/Last dalam data disatukan (CTA/UTP); perbezaan vendor

### Takeaway
Sejak pindaan CTA/UTP 2013, odd lot dilapor ke pita disatukan dan dikira dalam volum, tetapi TIDAK dikira dalam High/Low dan tidak mencetus LULD/SSR/hentian; dagangan penyelesaian khas juga dikecualikan daripada High/Low/Last. Sejak November 2025 takrif "round lot" berperingkat ikut harga (100/40/10/1 saham), jadi bagi saham > $250 lebih banyak dagangan kecil kini layak mempengaruhi High/Low. Vendor yang membina bar sendiri daripada semua dagangan boleh memberi High lebih tinggi/Low lebih rendah daripada OHLC rasmi.

### Cited Findings
- Pindaan CTA (2013): odd lot dilapor ke pita disatukan sebagai maklumat jualan terakhir, tetapi "would not be included in calculations of high and low prices and would not be subject to the Limit Up-Limit Down Plan; including odd-lot transactions on the consolidated tape would not trigger short sale restrictions or trading halts. However, odd-lot transactions would be included in calculations of daily consolidated volume"; Pelan UTP Nasdaq diubah selari — [SEC Release 34-70794](https://www.sec.gov/file/rel-no-34-70794); [Federal Register 2013-30041](https://www.govinfo.gov/content/pkg/FR-2013-12-18/pdf/2013-30041.pdf); [SEC 34-70899](https://www.sec.gov/file/34-70899)
- Nasdaq last-sale FAQ: dagangan dengan kod penyelesaian khas tidak dimasukkan dalam pengiraan harga tinggi, rendah atau jualan terakhir — [Nasdaq Last Sale FAQ](https://m.nasdaqtrader.com/Content/TechnicalSupport/FAQs/lastsalefaq.pdf)
- SEC Data Highlight tentang kadar odd lot selepas ketelusan (angka tidak dibaca) — [SEC Odd-Lot Rates](https://www.sec.gov/about/odd-lot-rates-post-transparency-world)
- Takrif round lot Rule 600(b)(93) Reg NMS (berdasarkan purata harga tutup di bursa penyenaraian utama): 100 saham bagi ≤ $250.00; 40 bagi $250.01–$1,000.00; 10 bagi $1,000.01–$10,000.00; 1 bagi ≥ $10,000.01; tarikh pematuhan takrif round lot (bersama Rule 610/612) = hari bekerja pertama November 2025; maklumat odd lot (termasuk bida/tawaran odd lot terbaik) = hari bekerja pertama Mei 2026 — [SEC 34-104209 (NYSE 2025)](https://www.sec.gov/files/rules/sro/nyse/2025/34-104209.pdf); [SEC 34-104325](https://www.sec.gov/file/34-104325); [Federal Register 2025-20530](https://public-inspection.federalregister.gov/2025-20530.pdf); [Sidley/Law360](https://www.sidley.com/-/media/publications/law360--peeling-back-the-layers-of-secs-equity-trading-reforms.pdf%3Frev=446cb8f6848c44f0bbd9d8bf05715fd6&sc_lang=en)
- Surat SIFMA 2019 tentang cadangan sebut harga odd lot terbaik pada SIP — [SIFMA via ctaplan.com](https://www.ctaplan.com/publicdocs/SIFMA_CL_on_CTA_and_UTP_Odd_Lot_Proposal_November_26_2019.pdf)

### Inferences
- Untuk alam sistem (≥ $10, termasuk banyak saham > $250), bar harian sebelum dan selepas Nov 2025 mungkin tidak setara sepenuhnya: dagangan 40–99 saham pada saham $250–$1,000 kini round lot dan (jika SIP mengikut takrif baharu untuk kelayakan H/L) boleh menetapkan High/Low — **perlu disahkan** dalam matriks syarat jualan CTA/UTP semasa. Ini boleh menjadikan Low sedikit lebih rendah → henti berasaskan Low lebih kerap dicetus berbanding backtest pra-2025.
- Syarat dagangan lain yang lazimnya tidak mengemas kini High/Low/Last sesi biasa (Form T/extended hours, average price, prior reference price, derivatively priced, odd lot) — **(belum disahkan)**; vendor yang mengagregat tick sendiri mungkin tidak menapis semua.
- Peraturan disyorkan: henti berasaskan Low dicetus hanya jika Low Yahoo DAN Low Moomoo ≤ henti; jika berbeza (satu sahaja menembusi), guna Low yang lebih tinggi dan tanda `low_bercanggah` untuk semakan; jangan guna Low daripada bar 1 minit yang dibina daripada semua tick.

### Gaps
- Matriks kelayakan syarat jualan CTA/UTP semasa (2026) — tidak dapat dibaca (ctaplan.com/utpplan.com disekat).
- Cara Yahoo dan Moomoo membina High/Low harian (dari OHLC rasmi SIP atau dari tick sendiri) — tiada dokumentasi.
- Status pelaksanaan maklumat odd lot Mei 2026 — tidak disahkan.

## 9. Ringkasan untuk penguji kertas bar harian: peristiwa → herotan → sumber pengesanan percuma → peraturan pengendalian

### Takeaway
Hampir semua herotan isian boleh dikesan secara percuma dengan tiga sumber yang sudah/boleh diakses Actions: suapan hentian Nasdaq Trader (semasa + `haltdate`), sebut harga Moomoo 9:35 (`open_price`, `volume`, `suspension`, `data_date`) dan dua set bar harian (Yahoo + Moomoo) dimuat turun dua kali. Peraturan di bawah ialah cadangan (inferens) berasaskan dapatan bahagian 1–8.

### Cited Findings
- Suapan hentian semasa/sejarah dan medannya — [Nasdaq Trader snippet](https://NASDAQTrader.com/snippets/tradehaltaccordion.html); [gitea feed_parser.py](https://gitea.com/infrastructure_SC/SimplyTrading/src/branch/main/backend/halt_monitor/feed_parser.py)
- NOOP = harga Opening Cross; cetakan pertama jika tiada cross — [Nasdaq Cross FAQ](https://www.nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf)
- Jeda LULD 5 minit, lanjutan 5 minit, pembukaan semula oleh bursa utama — [SEC 34-88383](https://www.sec.gov/files/rules/sro/nasdaq/2020/34-88383.pdf); [NYSE Amendment 12 fact sheet](https://www.nyse.com/publicdocs/nyse/products/etp-funds/ETF_Fact_Sheet_Amendment_12.pdf)
- SSR sehingga tutup hari berikutnya — [Nasdaq Reg SHO FAQ](https://m.nasdaqtrader.com/content/marketregulation/regsho/regshoFAQs.pdf)
- Tutup awal 2026: 27 Nov, 24 Dis (13:00 ET) — [Business Wire NYSE 2025](https://www.businesswire.com/news/home/20251223981478/en/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar)
- Odd lot dikecualikan daripada High/Low — [SEC Release 34-70794](https://www.sec.gov/file/rel-no-34-70794)

### Inferences
| Peristiwa | Herotan pada sistem | Pengesanan percuma (masa) | Peraturan disyorkan |
|---|---|---|---|
| Hentian T1/T12/M1 meliputi 9:30 (berita, maklumat diminta, tindakan korporat) | Sebut harga 9:35 = tutup semalam (basi); buka rasmi = harga pembukaan semula (selalu jurang besar); satu lejar langkau, satu lejar beli → bias pemilihan | RSS `feed=tradehalts` pada 9:35 NY; esok `haltdate=` / `resumedate=`; Moomoo `suspension`, `volume` sesi biasa = 0 | Bendera `buka_lewat`; SATU peraturan untuk semua lejar (langkau semua, atau beli pada buka rasmi dengan bendera); jangan guna `last_price` basi |
| Hentian H10 (penggantungan SEC) / IPO1–IPOQ / delist | Tiada bar beberapa hari; harga terakhir basi; isian mustahil | RSS hentian (kod) + tiada bar ≥ N sesi | Posisi: tutup pada cetakan sah pertama selepas penyambungan atau ikut peraturan delist sedia ada (≥ 5 sesi tanpa bar); isyarat: langkau |
| Pembukaan lewat NYSE (ketidakseimbangan, DMM) tanpa hentian rasmi | Sama seperti di atas tetapi tiada rekod RSS | Moomoo 9:35: `volume`=0 / `data_date` ≠ hari ini; bar 1 minit pertama > 9:31 | Bendera `buka_lewat`; peraturan sama seperti hentian |
| Jeda LULD (LUDP/LUDS) | Henti berasaskan Low diisi pada harga henti walaupun harga melompat melepasinya selepas jeda | RSS: LUDP + PauseThresholdPrice + ResumptionTradeTime; bar 1 minit malam itu | Isi henti pada harga pembukaan semula jika henti dalam jurang jeda; jika Open ≤ henti, isi pada Open; tanpa data → min(henti, Low) + bendera |
| MWCB Tahap 1/2/3 | Semua henti dalam tetingkap hentian melompat; Tahap 3 → tiada lelongan tutup | RSS (kod MWC*, belum disahkan); S&P 500 −7% | Rekod hari MWCB; isian henti pada pembukaan semula; keluar masa hari Tahap 3 = cetakan terakhir + bendera |
| Rule 201 SSR | Tiada kesan isian (beli sahaja); mengubah dinamik pantulan | Proksi: Low(D) ≤ 0.9 × Close(D−1) → aktif D dan D+1 | Lajur `ssr_aktif` sebagai ciri analisis; bukan penapis tanpa ujian |
| Buka rasmi lawan 'Open' vendor lawan 9:35 | Harga beli sementara ≠ harga beli akhir; perbezaan vendor | Banding Open Yahoo lawan Moomoo; banding rekod 9:35 lawan buka akhir | Ambil `open_price` (bukan `last_price`) pada 9:35; tanda jika |Yahoo/Moomoo − 1| > ambang dikalibrasi |
| Hari separuh / cuti / penutupan tidak berjadual | Keluar masa "pada tutup" salah masa; bar rata/hilang; tetingkap skrip salah | `exchange_calendars` (dengan `end=` eksplisit, versi terkini) + Moomoo `quote_trading_days` + kehadiran bar SPY | Guna `session_close`; buang bar rata volum 0 pada hari bukan sesi; jangan kira hari bukan sesi dalam "hari" pegangan |
| Dagangan clearly erroneous dibatalkan / tick buruk vendor | Low/High palsu mencetus henti atau menetapkan puncak Chandelier | Muat turun semula T+1 dan T+5, banding; banding Yahoo lawan Moomoo | Versi bar terakhir menang; nilai semula henti jika Low berubah; log perubahan |
| Odd lot / syarat dagangan / takrif round lot baharu (Nov 2025) | Low vendor berbeza; backtest pra-2025 vs hadapan tidak setara bagi saham > $250 | Banding Low dua vendor | Henti dicetus hanya jika kedua-dua vendor ≤ henti; jika tidak, guna Low lebih tinggi + bendera |

### Gaps
- Semua ambang angka dalam jadual (0.5%, 0.1%, k) ialah cadangan permulaan, bukan daripada sumber; perlu dikalibrasi dengan data sistem sendiri (rekod 9:35, bar Yahoo dan Moomoo yang diarkib).
- Kebolehcapaian nasdaqtrader.com dari runner GitHub Actions (IP pusat data) belum diuji; jika disekat, alternatif ialah Tapeboard JSON (pihak ketiga, terma tidak disahkan) atau medan `suspension` Moomoo sahaja.
