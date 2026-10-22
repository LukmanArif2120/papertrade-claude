# Pengesanan Tindakan Korporat yang Mencemarkan Isyarat Bar Harian (Saham AS, Data Percuma): dividen khas/besar, spin-off, terbitan hak, pecahan dan pecahan songsang, dividen saham, tukar ticker/CUSIP, domisil semula

> **Nota kaedah (baca dahulu).** Tarikh kajian: 22 Okt 2026. Dalam sesi ini WebFetch hanya dapat mencapai `github.com` dan `raw.githubusercontent.com`. Domain lain gagal DNS (`finra.org`, `sec.gov`, `quantconnect.com`, `nasdaqtrader.com`, `openapi.moomoo.com`, `open.moomoo.com`, `ranaroussi.github.io`), dan `curl` disekat proksi (403). Maka teks peraturan FINRA, dokumen SEC, QuantConnect, Nasdaq dan Moomoo datang daripada **ringkasan enjin carian**, bukan bacaan teks penuh. Semak teks asal sebelum menjadikannya spec.
> Tiga jenis bukti **primer** diperoleh terus dalam sesi ini:
> (a) **Ujian langsung alat MCP Moomoo** pada 22 Okt 2026: `quote_corporate_actions_rehab` untuk US.GE, US.DD dan US.COST, `quote_corporate_actions_dividends` untuk US.COST, dan `quote_history_kline` untuk DD dan COST dengan `autype` 0 dan 1. Ia ditanda **[Ujian Moomoo 22-10-2026]**.
> (b) **Bacaan kod repo**: `BacktestShariah2/kod/stor.py` dan `BacktestShariah2/standard/harga_yf.py`.
> (c) **Analisis stor harga repo** `BacktestShariah2/data/harga/stor/harga_A.csv` dan `harga_B.csv`: 946 ticker, 412,482 baris, 9 Sep 2024 hingga 21 Okt 2026. Ia ditanda **[Stor repo]**.
> Istilah teknikal Inggeris dikekalkan dalam kurungan.

---

## 1. Sumber percuma yang memberi data tindakan korporat secara berprogram: ketepatan masa dan kebolehpercayaan (yfinance, Nasdaq Daily List / Nasdaq Trader, SEC EDGAR, Moomoo OpenAPI, notis bursa, peraturan tarikh-ex)

### Takeaway
Sumber percuma berstruktur terbaik yang sudah ada dalam sistem ialah **Moomoo `quote_corporate_actions_rehab`**. Ia memulangkan jenis peristiwa (DIVIDEND, SPECIALDIVIDEND, SPLIT, JOIN, SPINOFF), tarikh-ex, nisbah, dan faktor pelarasan hadapan/belakang. Dividen yang sudah diumumkan muncul sebelum tarikh-ex. Kelemahannya: label tidak konsisten dan medan amaun kadang-kadang 0. yfinance (`actions`, dan `repair=True` dalam ≥1.1.0, terkini 1.7.0) sesuai sebagai pendapat kedua. SEC EDGAR (Form 10-12B, 8-K Item 3.03/5.03, pengganti Rule 12g-3) memberi amaran awal beberapa hari hingga bulan sebelum peristiwa. Nasdaq Daily List **tidak percuma**, kerana ia produk berlesen ~USD3,500/bulan.

### Cited Findings

**Peraturan tarikh-ex (asas penentuan masa)**
- FINRA Rule 11140 dipinda berkuat kuasa 28 Mei 2024 (T+1). Bagi pengagihan < 25% nilai sekuriti, tarikh-ex = tarikh rekod (jika hari perniagaan). Bagi "cash dividends or distributions, stock dividends and/or splits, and the distribution of warrants, which are 25 percent or greater of the value of the subject security, the ex-dividend date shall be the first business day following the payable date" — [FINRA Rule 11140 (ringkasan carian)](https://www.finra.org/rules-guidance/rulebooks/finra-rules/11140). Peraturan lama (tarikh-ex = dua hari perniagaan sebelum tarikh rekod) kini terbatal — [NASD NTM 00-54](https://www.finra.org/rules-guidance/notices/00-54). Satu filing penerbit 2024 menggunakan peraturan ini untuk dividen khas USD0.50: penjual sebelum atau pada tarikh bayar tidak menerima dividen — [ringkasan carian, filing SEC](https://investors.clearone.com/node/17686/html).
- Nasdaq mewajibkan syarikat yang membuat pecahan songsang menghantar Company Event Notification Form **10 hari kalendar** sebelum tarikh berkesan pasaran. Ia operatif sejak 30 Jan 2025, sebelum itu 5 hari perniagaan (diluluskan Nov 2023), dan diselaraskan dengan notis 10 hari SEC Rule 10b-17. Pendedahan awam mesti dibuat **sekurang-kurangnya 2 hari perniagaan** sebelum tarikh berkesan, sebelum 12 tengah hari ET — [AFS Law](https://www.afslaw.com/perspectives/alerts/nasdaq-rule-change-lengthens-reverse-stock-split-notice-period); [TheCorporateCounsel (Issuer Alert 2025-01)](https://www.thecorporatecounsel.net/blog/2025/02/nasdaq-issuer-alert-reminder-on-reverse-stock-split-notices.html); [Cooley PubCo](https://cooleypubco.com/2024/11/26/nasdaq-amend-deadline-notification-reverse-split/).
- FINRA Rule 5330 mewajibkan broker melaraskan harga pesanan terbuka (open orders) pada tarikh-ex. Bagi dividen tunai, harga dikurangkan dengan amaun dividen melainkan pesanan ditanda "Do Not Reduce". Dividen < USD0.01 dikecualikan. Bagi dividen saham dan pecahan, harga dikurangkan dan saiz pesanan ditambah melainkan ditanda "Do Not Increase" — [FINRA Rule 5330 (ringkasan carian)](https://finra.org/rules-guidance/rulebooks/finra-rules/5330); [NTM 93-61](https://www.finra.org/rules-guidance/notices/93-61).

**Nasdaq Daily List / Nasdaq Trader**
- Daily List merangkumi "corporate actions of issuers (such as dividends, stock splits, and mergers and acquisitions), execution of corporate actions by the Exchange (such as execution dates and symbol changes), and information about issuer status". Set Dividends merangkumi dividen tunai, dividen saham dan pecahan. Set "Next Day Ex-Date summarizes the securities with dividend adjustments to be applied to the previous closing price on the next business day" — [Federal Register 2024-14377](https://www.federalregister.gov/documents/2024/07/01/2024-14377/self-regulatory-organizations-the-nasdaq-stock-market-llc-notice-of-filing-and-immediate); [spesifikasi Daily List (PDF)](https://m.nasdaqtrader.com/content/technicalSupport/specifications/dataproducts/dlcompletespec.pdf).
- Yuran lesen Daily List dicadang naik daripada USD1,750 kepada USD3,500 sebulan (2024). Spesifikasinya berlabel untuk kegunaan dalaman Nasdaq dan pihak ketiga berlesen — [SR-NASDAQ-2024-027](https://listingcenter.nasdaq.com/assets/rulebook/nasdaq/filings/SR-NASDAQ-2024-027.pdf); [ringkasan carian Federal Register](https://www.federalregister.gov/documents/2024/07/01/2024-14377/self-regulatory-organizations-the-nasdaq-stock-market-llc-notice-of-filing-and-immediate).
- Fail direktori simbol percuma `nasdaqlisted.txt` (http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt) mempunyai lajur Symbol, Security Name, Market Category, Test Issue, Financial Status, Round Lot Size. `otherlisted.txt` (ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt) meliputi sekuriti NYSE/lain — [DataHub nasdaq-listings](https://datahub.io/core/nasdaq-listings); [velog (contoh skrip)](https://velog.io/@24331/Python-미국-주식-종목코드). Kod Financial Status ialah: D Deficient, E Delinquent, Q Bankrupt, G/H/J/K gabungan — [spesifikasi QBBO Nasdaq](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/qbbospec.pdf).
- Nasdaq tidak menerbitkan API kalendar dividen/pecahan awam yang disokong. Pembalut PyPI tidak rasmi bagi "NASDAQ Public API" kali terakhir dikemas kini Ogos 2021 — [PyPI rojito](https://pypi.org/user/rojito/) (ringkasan carian).

**SEC EDGAR**
- Had kadar rasmi ialah **10 permintaan/saat**, dan klien automatik mesti mengisytiharkan User-Agent (nama + e-mel). SEC berhak mengehadkan kadar — [SEC Accessing EDGAR Data](https://www.sec.gov/os/accessing-edgar-data). Klien tanpa User-Agent dilaporkan menerima 403 — [arkolith (sekunder)](https://arkolith.com/blog/sec-edgar-api-guide); [edgartools compliance](https://edgartools.readthedocs.io/en/stable/resources/sec-compliance/).
- `company_tickers.json` memetakan ticker ↔ CIK ↔ nama EDGAR. SEC mengemas kininya secara berkala dan tidak menjamin ketepatan atau skop. Sejarah filing boleh dibaca melalui `data.sec.gov/submissions/CIK{cik}.json` tanpa kunci API — [SEC Accessing EDGAR Data (ringkasan carian)](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm).
- Pecahan songsang biasanya dilaporkan dalam 8-K **Item 3.03** (Material Modification to Rights of Security Holders) yang merujuk **Item 5.03** (pindaan piagam) — contoh [VirnetX 2023 (1-for-20)](https://ir.virnetx.com/node/10796/html), [Atlas Financial 2013](https://www.sec.gov/Archives/edgar/data/1539894/000153989413000033/form8-krestocksplit.htm), [BankGuam 2022 (1-for-500)](https://bankofguam.com/uploads/investor-relations/As-filed-8-K-11.3.2022.pdf).
- Spin-off didaftar dengan **Form 10-12B**. Lampiran 99.1 (information statement) menerangkan dagangan when-issued, ex-distribution dan due bill — contoh [Kraft Foods Group 10-12B (2012)](https://www.sec.gov/Archives/edgar/data/0001545158/000119312512146220/d317589dex991.htm), [SAIC Gemini 10-12B (2013)](https://www.sec.gov/Archives/edgar/data/0001571123/000119312513095961/d491894dex991.htm).
- Penyusunan semula syarikat induk (holding company reorganization) menjadikan syarikat induk baharu "successor issuer" di bawah Rule 12g-3(a), dan sahamnya dianggap berdaftar di bawah Seksyen 12(b) — [Cannagistics 8-K 2021](https://docoh.com/filing/1304741/0001663577-21-000256/CNGT-8K); [ZoomInfo](https://ir.zoominfo.com/node/10731/html).

**Moomoo OpenAPI**
- Antara muka `get_rehab` (SDK) dan `/corporate-actions/rehab` (REST) memulangkan jadual faktor pelarasan setiap saham dengan `ex_div_date`, `split_ratio`, `spin_off_ratio`, dan faktor hadapan/belakang. Versi REST disusun menaik mengikut `ex_div_date`, meliputi semua peristiwa sejak penyenaraian tanpa parameter tetingkap masa, dan faktor diskalakan 1e-9 — [Moomoo Rehabilitation Factor (ringkasan carian)](https://open.moomoo.com/api/quote/basic-data/rehab); [Futu get-rehab](https://openapi.futunn.com/futu-api-doc/en/quote/get-rehab.html).
- **[Ujian Moomoo 22-10-2026] Medan sebenar** setiap rekod: `action_types`, `ex_div_date`, `per_cash_div`, `special_dividend`, `split_base/split_ert/split_ratio`, `join_base/join_ert`, `spin_off_base/spin_off_ert/spin_off_ratio`, `allotment_ratio`, `allot_base/allot_ert` (terbitan hak), `bonus_base/bonus_ert`, `per_share_div_ratio`, `per_share_trans_ratio`, `stk_spo_ratio`, `add_base/add_ert`, `transfer_base/transfer_ert`, `forward_adj_factorA/B`, `backward_adj_factorA/B`, `cum_forward_adj_factorA/B`, `cum_backward_adj_factorA/B`, dan `desc_sc` (teks Cina, contoh "公司分立，比例…"). Parameter `divi_mode` = `exclude_divi` (konvensyen Yahoo/Bloomberg), `include_divi` (lalai, konvensyen Futu) atau `compat`.
- **[Ujian Moomoo 22-10-2026] US.GE**: 124 rekod, iaitu DIVIDEND 119, SPLIT 2, SPINOFF 2 dan JOIN 1. Rekod tersebut: JOIN 8→1 pada 2021-08-02; SPINOFF 2023-01-04 `spin_off_ratio` 0.7803407 (GE HealthCare); SPINOFF 2024-04-02 `spin_off_ratio` 0.7975308 (GE Vernova). Pertukaran Synchrony 2015 (exchange offer, bukan pro-rata) tidak muncul sebagai SPINOFF.
- **[Ujian Moomoo 22-10-2026] US.DD**:
  - SPINOFF 2025-11-03 `spin_off_ratio` 0.41824862 (Qnity).
  - JOIN 3→1 pada 2026-06-24.
  - Peristiwa era DowDuPont dikodkan sebagai **SPLIT** dengan nisbah bukan integer: 2017-09-01 (1.28918), 2019-04-01 (1.02492) dan 2019-04-02 (1.48742). Maksudnya, cantuman dan spin-off kadang-kadang disamarkan sebagai "split".
  - Rekod dividen 2026-11-30 (masa depan) sudah tersenarai.
- **[Ujian Moomoo 22-10-2026] US.COST**:
  - Dividen khas 2020-12-01 (USD10) dan 2023-12-27 (USD15) berlabel `SPECIALDIVIDEND` dengan medan `special_dividend`.
  - Dividen khas 2012-12-06 (USD7), 2015-02-05 (USD5) dan 2017-05-08 (USD7) berlabel `DIVIDEND` biasa. Label tidak konsisten.
  - Dalam `quote_corporate_actions_dividends`, `dividend_per_share` = **0** bagi dividen khas USD10 (2020) dan USD15 (2023). Amaun hanya ada dalam teks `statement` ("Cash Dividend: 15 USD Per Share").
  - Dividen ex 2026-10-30 (pub_date 2026-10-15) sudah tersenarai pada 22 Okt, iaitu kira-kira 2 minggu lebih awal.
- Alat `quote_corporate_actions_stock_splits` menyatakan "HK only (cmd 9415)… for US / A-share use the basic variant". Oleh itu, untuk AS gunakan rehab — [deskripsi alat MCP Moomoo, sesi ini].
- `quote_history_kline` mempunyai `autype` lalai **1 = Forward** (0 = None, 2 = Backward) — [skema alat MCP Moomoo, sesi ini]. Huraian alat rehab menyatakan konvensyen Futu lalai **termasuk dividen tunai** (`include_divi`).

**yfinance / Yahoo**
- `repair=True` membaiki: pelarasan pecahan yang hilang ("stock split in data but preceding price data is not adjusted"), pelarasan dividen yang hilang, ralat 100x, bar hilang, dan (baharu) ralat dividen. Pembaikan pecahan "Requires date range include 1 day after stock split for calibration" kerana "sometimes Yahoo fails to adjust prices on stock split day" — [dokumen yfinance price_repair.rst](https://github.com/ranaroussi/yfinance/blob/main/doc/source/advanced/price_repair.rst); [wiki Price repair](https://github.com/ranaroussi/yfinance/wiki/Price-repair).
- Pengarang menulis: "Only US market data appears perfect". Ini pemerhatian tidak formal, bukan jaminan — [price_repair.rst](https://github.com/ranaroussi/yfinance/blob/main/doc/source/advanced/price_repair.rst).
- Isu #1531 (Mei 2023): "Yahoo sometimes fails to apply stock split to past prices", contohnya CNE.L. Isu ditutup Jun 2023 dengan pembaikan di bawah `repair`. Halaman isu turut merujuk komit bertarikh 5 Okt 2026, "Price repair: fix split-like level shift that has no matching split", iaitu anjakan aras seperti pecahan tanpa rekod pecahan — [yfinance #1531](https://github.com/ranaroussi/yfinance/issues/1531).
- Isu #2660 (Jan 2026, yfinance 1.0): `repair=True` tersalah menggunakan pecahan 4:1 pada GME untuk 2002–2021. Puncanya, lonjakan 27 Jan 2021 disangka pecahan 2022-07-22 yang tidak dilaras. Kes serupa berlaku pada NVDA 3:2 sebelum 2004-08-06. Pembaikan PR #2668 menambah semakan kemeruapan dan volum — [yfinance #2660](https://github.com/ranaroussi/yfinance/issues/2660).
- CHANGELOG yang berkaitan:
  - 0.2.21 "Price repair update: fix Yahoo messing up dividend and split adjustments #1543" dan "Fix merge future div/split into prices #1567".
  - 0.2.39 "Improve 'sudden change' repair for splits & currency".
  - 0.2.42 "price repair extended to dividends & adjust".
  - 1.1.0 "Improve stock-split repair false-positives #2668".
  - 1.4.0 "Simplify phantom-dividend repair branch".
  - 1.5.1 "Handle premarket silly games creating false-positive bad-dividend".
  - **1.7.0 (terkini dalam CHANGELOG) "Fix bug in volume-validation of stock-split-repair #2958"**.

  Sumber: [CHANGELOG yfinance](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst). CHANGELOG tidak mencatat tarikh versi.
- Bagi spin-off, forum pengguna melaporkan bahawa sejarah Yahoo sebelum spin-off kadang-kadang dilaras ke bawah secara retroaktif ([Fund Manager, BGCP/Newmark 2018](https://www.fundmanagersoftware.com/forum/viewtopic.php?p=19443)). Kadang-kadang pula spin-off direkod sebagai "split" dengan nisbah ganjil. Dalam kes MRO/MPC 2011, nisbahnya 16/77, dan "a $0.00 Yahoo dividend in conjunction with a split" menandakan spin-off atau M&A ([Wealth-Lab MRO](https://wealth-lab.com/Forum/Posts/Yahoo-Data-MRO-and-NOC-split-adjustments-not-applied-34260)). Bukti ini lama dan tidak rasmi.

### Inferences
- **Susunan sumber yang dicadangkan.** Dahulukan **Moomoo rehab**, kerana ia sudah disahkan dalam sistem, berstruktur, dan mempunyai faktor sedia guna. Gunakan **yfinance `Ticker.actions`** sebagai pendapat kedua. Gunakan **EDGAR** untuk amaran awal spin-off, pecahan songsang dan penyusunan semula. Peraturan **OHLCV** (Bahagian 4) menjadi jaring keselamatan terakhir. Nasdaq Daily List tidak sesuai kerana berbayar.
- **Masa.** Dividen biasa diumumkan kira-kira 2 minggu sebelum tarikh-ex (COST: diterbitkan 15 Okt, ex 30 Okt) dan muncul di Moomoo sebelum tarikh-ex. Pecahan songsang Nasdaq mesti diumumkan ≥ 2 hari perniagaan sebelum berkesan. Spin-off mempunyai Form 10-12B berbulan lebih awal. Oleh itu, **hampir semua peristiwa boleh diketahui sebelum bar tarikh-ex**, jika sumber disemak setiap malam.
- **Kos panggilan Moomoo rehab.** Satu panggilan memulangkan ~70–95 ribu aksara sejarah penuh (GE 124 rekod). Memanggil 2,000 ticker setiap malam berat dan had kadarnya tidak diketahui. Pilihan praktikal ialah memanggil rehab hanya untuk (a) calon isyarat malam itu, (b) posisi terbuka, dan (c) ticker yang dibenderakan peraturan OHLCV. Simpan cache dan muat semula mingguan untuk semua.
- **Normalisasi Moomoo yang perlu dibuat:**
  - Amaun dividen ialah `per_cash_div` atau `special_dividend`. Jika kedua-duanya 0 (endpoint dividends), hurai teks `statement`/`desc_sc`.
  - "SPLIT" dengan nisbah bukan nombor bulat lazim (bukan 2, 3, 4, 3/2, 5, 10…) perlu dianggap **peristiwa bukan-pecahan** (cantuman/spin) dan disekat.
  - Faktor yang perlu digunakan untuk pelarasan ialah `forward_adj_factorA` dari mod `exclude_divi`, iaitu konvensyen Yahoo: pecahan dan spin sahaja.
- **Penemuan sistem: konvensyen pelarasan stor bercampur.** Bukti terperinci ada di Bahagian 4. Ringkasnya, bar lama dalam stor repo sepadan tepat dengan kline Moomoo `autype=1` (hadapan, termasuk dividen). Ini bercanggah dengan docstring `harga_yf.py`, yang menyatakan "split dilaras oleh Yahoo, dividen tidak".

### Gaps
- Teks penuh FINRA 11140/5330, halaman API SEC dan dokumen Moomoo tidak dapat dibaca (DNS). Kandungan diambil daripada ringkasan carian.
- Had kadar Moomoo untuk rehab/dividends tidak ditemui.
- Tidak diuji sama ada Moomoo rehab menyenaraikan **pecahan/spin-off** sebelum tarikh-ex (hanya dividen terbukti muncul lebih awal).
- Endpoint carian teks penuh EDGAR (`efts.sec.gov/LATEST/search-index`), indeks harian EDGAR (`/Archives/edgar/daily-index/`) dan Form 8-K12B tidak dapat disahkan dalam sesi ini.
- Tiada statistik awam tentang kekerapan Yahoo lewat melaras pecahan atau tempoh pembetulannya.
- Tiada sumber percuma rasmi Nasdaq/NYSE untuk kalendar tindakan korporat yang dapat disahkan (API `api.nasdaq.com/api/calendar/...` tidak rasmi dan tidak diuji kerana proksi menyekat).

---

## 2. Saiz dividen yang patut dianggap mencemarkan isyarat swing, dan cara pengamal (QuantConnect, Zipline/Quantopian, CRSP, Norgate) melaras atau membenderakannya

### Takeaway
Dividen suku tahunan biasa jauh lebih kecil daripada hingar harian. Median ATR14 stor ialah 3.4% harga, dan jatuhan harga-ex purata hanya 42–85% daripada dividen. Kebanyakan pengamal hanya **melaras** dividen (faktor 1 − D/P), tidak menyekatnya. Pencemaran sebenar bermula apabila dividen ≥ ~1–2% harga atau ≥ ~0.5×ATR14. Dividen khas (Morningstar: ≥ 5% ialah "special"; Moomoo: `SPECIALDIVIDEND`) dan apa-apa ≥ 25% (peraturan tarikh-ex berbeza) patut dilayan sebagai peristiwa: laraskan sejarah dan sekat isyarat. Perlindungan paling murah ialah meniru FINRA 5330: turunkan paras henti (stop) sebanyak D pada tarikh-ex.

### Cited Findings
- **Norgate**: dividen biasa, dividen khas dan pulangan modal dilaras dengan cara yang sama, iaitu faktor = (harga dijangka selepas pengagihan) / tutup sebelumnya, dikenakan pada semua harga lebih awal. Contohnya, tutup USD100 dengan pengagihan USD10 memberi faktor 0.9 — [thechartist.com.au memetik Norgate](https://thechartist.com.au/?p=101961). Pengguna boleh memilih untuk melaras **hanya "Capital reconstructions and special dividends"**. Pelarasan dividen biasa menurunkan harga lampau dan mengherotkan penapis berasaskan harga — [Wealth-Lab](https://wealth-lab.com/Discussion/Price-adjustment-to-not-apply-to-regular-cash-dividends-Wealth-Data-8593). RealTest mempunyai pilihan "CapitalSpecial" yang hanya menukar penyusunan semula modal dan dividen khas kepada pelarasan seperti pecahan — [RealTest User Guide](https://mhptrading.com/docs/topics/idh-topic1390.htm).
- **Morningstar Indexes**: pengagihan tunai bukan biasa ≥ **5%** daripada harga pasaran dianggap dividen khas, manakala yang lebih kecil dianggap biasa — [Morningstar index methodology](https://indexes.morningstar.com/api/docs/6883c000fb8ee1d878f734a6).
- **QuantConnect (LEAN)**:
  - Mod normalisasi: Raw, Adjusted (lalai; "fully adjust for splits and dividends"), SplitAdjusted (harga berterusan, dividen dibayar tunai), TotalReturn dan ScaledRaw.
  - Dalam mod Raw atau dagangan langsung, "LEAN automatically adjusts your positions based on the SplitFactor" dan dividen dibayar tunai.
  - ScaledRaw dicadangkan untuk memanaskan semula penunjuk selepas pecahan.
  - Objek Split diterima "when a split is in the near future and when it occurs".

  Sumber: [QuantConnect US Equity corporate actions](https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/us-equity/corporate-actions); [forum QC #508](https://www.quantconnect.com/forum/discussion/508/update-dividends-splits-and-custom-price-normalization/p1).
- **Zipline**: pangkalan pelarasan SQLite mempunyai jadual `splits`, `dividends`, `mergers` (lajur `ratio`, `effective_date`, `sid`), serta `stock_dividend_payouts` (`sid`, `payment_sid`, `ratio`, `pay_date`) — [kod sumber zipline.data.adjustments](https://zipline.ml4trading.io/_modules/zipline/data/adjustments.html). Satu kes pecahan NVDA dikenakan dua kali dalam bundle diselesaikan dengan "drop and re-ingest" — [QuantRocket forum](https://support.quantrocket.com/t/split-adjustment-issue-in-usstock-daily/1698).
- **CRSP**: harga dilaras dengan A(t) = P(t)/C(t), dengan C ialah faktor kumulatif. Bagi spin-off, pengagihan bukan-akhir dan hak (rights), "Factor to Adjust Price is not equal to Factor to Adjust Shares Outstanding". Faktor harga = amaun setara tunai / harga pada tarikh ex-distribution. Spin-off dilayan sebagai peristiwa jenis pecahan pada tarikh ex — [CRSP Calculations and Index Methodologies](https://crsp.org/wp-content/uploads/guides/CRSP_Calculations_and_Index_Methodologies.pdf); [U. Michigan, CRSP factor adjustment](https://leiq.bus.umich.edu/docs/crsp_factor_adjustment.pdf). Satu kertas melaporkan harga yang dilaras dengan faktor CRSP "inaccurate in the presence of property dividend, spin-off and rights offering events" — [Accounting Research Journal (IDEAS)](https://ideas.repec.org/a/eme/arjpps/arj-06-2016-0065.html). CRSP juga membetulkan faktor spin-off secara retroaktif ("CHANGED FACTOR TO ADJUST PRICE TO 0 FROM 0.2773 FOR TWO SPIN OFFS ON EX-DATE 19941216") — [CRSP release notes Mac 2020](https://crsp.org/crsp_pdf/march-2020-monthly-release-notes-0).
- **Nisbah jatuhan harga (PDR) pada hari ex**: purata 42% (Nasdaq) dan 85% (NYSE), dengan median 37% / 91% bagi 1983–2011 (Paudel & Silveri) — [CXO Advisory](https://www.cxoadvisory.com/fundamental-valuation/nasdaq-vs-nyse-dividend-capture). PDR peringkat firma "so noisy as to prohibit sensible estimates" — [Ainsworth, Lee & Walter](https://ro.uow.edu.au/buspapers/1408). Bagi dividen khas di Australia, nisbah jatuhan dikaitkan dengan reaksi pengumuman, DRP, saiz firma dan DPS — [Balachandran, Faff & Nguyen 2008](https://research.bond.edu.au/en/publications/the-ex-date-impact-of-special-dividend-announcements-a-note/).
- **Hingar berbanding dividen kecil**: pembaikan dividen yfinance boleh menghasilkan positif palsu "with tiny dividends (~0.5%)" kerana kemeruapan biasa menyerupai jatuhan ex-dividen — [wiki Price repair](https://github.com/ranaroussi/yfinance/wiki/Price-repair).
- **FINRA 5330**: harga pesanan terbuka dikurangkan sebanyak dividen pada tarikh-ex — [FINRA 5330](https://finra.org/rules-guidance/rulebooks/finra-rules/5330). Bursa juga melaras tutup sebelumnya untuk dividen pada hari-ex ("Next Day Ex-Date… dividend adjustments to be applied to the previous closing price") — [Federal Register 2024-14377](https://www.federalregister.gov/documents/2024/07/01/2024-14377/self-regulatory-organizations-the-nasdaq-stock-market-llc-notice-of-filing-and-immediate).
- **[Stor repo] Hingar harian**: bagi 946 ticker, ATR14/tutup pada bar terakhir mempunyai median **3.37%**, P10 2.13% dan P90 6.22% (dikira dalam sesi ini).
- **[Ujian Moomoo 22-10-2026] Contoh dividen khas**: COST USD15, ex 2023-12-27 (rekod 2023-12-28, bayar 2024-01-12), dan USD10, ex 2020-12-01.

### Inferences
- **Ambang yang dicadangkan.** Ini heuristik saya, bukan nilai bersumber; tentukur dengan data sendiri. Tandakan D = amaun tunai sesaham, P = tutup sebelum tarikh-ex, dan A = ATR14/P.
  - **Tahap 0 (abaikan isyarat, tetapi laraskan henti):** D/P < 0.5% **dan** D < 0.25·A·P. Ini kebanyakan dividen suku tahunan, kerana dengan median A ≈ 3.4%, dividen 0.5% ≈ 0.15 ATR.
  - **Tahap 1 (laras sejarah untuk penunjuk; tiada sekatan):** 0.5% ≤ D/P < 2%, atau 0.25–0.75 ATR. Darab bar sebelum tarikh-ex dengan (1 − D/P), cara Norgate/CRSP.
  - **Tahap 2 (laras + sekat isyarat baharu):** D/P ≥ 2%, atau ≥ 0.75 ATR, atau jenis `SPECIALDIVIDEND`, atau teks "special". Sekat jika bar pencetus ialah bar tarikh-ex atau 1–2 bar selepasnya, dan laraskan henti posisi terbuka sebanyak D. Ambang 5% Morningstar menjadi batas atas "pasti khas".
  - **Tahap 3 (≥ 25%):** tarikh-ex jatuh **selepas** tarikh bayar (FINRA 11140), dan saham berdagang dengan due bill antara tarikh rekod dan tarikh-ex. Layan seperti pecahan/spin-off: laraskan sejarah dengan faktor, sekat ≥ 5 bar, dan semak semula posisi.
- **Kenapa melaras, bukan menyekat, untuk dividen kecil.** PDR < 1 (terutamanya Nasdaq 42%) bermaksud jatuhan sebenar lebih kecil daripada D. Melaras dengan D penuh boleh terlebih membetulkan jurang kecil, tetapi magnitudnya jauh di bawah ATR. Kesan sebenar dividen kecil hanyalah henti yang terlalu ketat tercetus. FINRA 5330 menyelesaikannya dengan mengurangkan henti sebanyak D.
- **Konsistensi dengan Lejar/Papertrade C.** Jika posisi maya tidak dikreditkan dividen tunai, jualan pada henti yang tercetus oleh jatuhan ex mengurangkan pulangan secara buatan. Pilih satu: (a) kreditkan D kepada posisi yang dipegang melepasi tarikh-ex (seperti mod Raw QuantConnect), atau (b) gunakan siri dilaras dividen untuk keputusan dan kira P&L dengan jumlah pulangan. Jangan campur kedua-duanya.

### Gaps
- Tiada sumber khusus tentang PDR dividen khas yang besar di AS selepas 2010 (kajian ditemui hanya untuk Australia).
- Ambang Norgate untuk "special" tidak diterbitkan dalam hasil carian.
- Teks QuantConnect tentang dividend warning / masa peristiwa dividen tidak dapat dibaca (DNS).
- Tiada kajian ditemui yang mengukur kesan dividen pada isyarat teknikal swing secara langsung. Ambang di atas ialah inferens.

---

## 3. Mengesan spin-off dan dagangan when-issued; layanan syarikat induk dan syarikat baharu dalam penjanaan isyarat

### Takeaway
Spin-off ialah pencemar paling besar yang tidak ditangani oleh Yahoo split-only. Contohnya, DD jatuh −57.5% pada buka 3 Nov 2025 dalam data mentah. Spin-off boleh dikesan **berbulan lebih awal** (Form 10-12B dengan CIK baharu, dan siaran akhbar when-issued). Pada tarikh-ex ia boleh disahkan melalui Moomoo rehab `SPINOFF` (`spin_off_ratio` = faktor harga) dan peraturan OHLCV (jurang besar + nilai dagangan melonjak + simbol baharu muncul). Untuk syarikat induk: laraskan sejarah dengan faktor (cara CRSP/Moomoo), atau sekat isyarat beberapa bar. Untuk syarikat baharu (SpinCo): abaikan bar when-issued dan jangan jana isyarat sehingga cukup bar regular-way. Kesusasteraan juga menunjukkan tekanan jualan institusi dalam ~30 hari pertama.

### Cited Findings
- **Mekanik when-issued**:
  - Dagangan when-issued ialah urus niaga bersyarat ke atas sekuriti yang diluluskan tetapi belum diterbitkan. Ia tamat pada hari dagangan pertama selepas pengagihan, apabila dagangan regular-way bermula. Jika spin-off gagal, "all when-issued trading will be null and void".
  - Saham induk berdagang dalam dua pasaran: regular-way (membawa hak ke atas saham SpinCo) dan ex-distribution (tanpa hak).
  - Due bill digunakan kerana tarikh-ex selalunya **selepas** tarikh pengagihan. Penjual regular-way dalam tempoh itu menjual saham **dan** hak (due bill).

  Sumber: [Kraft Foods Group 10-12B](https://www.sec.gov/Archives/edgar/data/0001545158/000119312512146220/d317589dex991.htm); [SAIC Gemini 10-12B/A](https://www.sec.gov/Archives/edgar/data/0001571123/000119312513361420/d491894dex991.htm); [Pfizer](https://pfizer.com/print/pdf/node/530196).
- **Contoh garis masa (Costamare 2025)**: when-issued SpinCo dan ex-distribution induk bermula 1 Mei 2025; hari terakhir due-bill, when-issued dan ex-distribution ialah 6 Mei 2025; regular-way SpinCo bermula 7 Mei 2025 — [National Law Review](https://natlawreview.com/node/298364/printable/print). Siaran akhbar Liberty mengumumkan simbol when-issued dan tarikh-ex secara berasingan — [Liberty/CommerceHub](https://investors.qvcgrp.com/news-media/press-releases/detail/292/liberty-announces-when-issued-trading-ex-dividend-date-and); [Liberty Media](https://www.libertymedia.com/news/detail/235/liberty-media-corp-announces-when-issued-trading-and).
- **[Ujian Moomoo 22-10-2026] DD mentah (`autype=0`)**: tutup 31 Okt 2025 = 81.65 → buka 3 Nov 2025 = 33.69, tutup 34.69 (`change_rate` −57.51%). Volum 20.5 juta berbanding 3.4–4.0 juta tiga hari sebelumnya (~5×), dan turnover USD708 juta berbanding ~USD283–328 juta (~2.3×). Dengan `autype=1` (hadapan) siri itu berterusan: 100.68 → 102.27 (+1.58%).
- **[Ujian Moomoo 22-10-2026] Faktor spin-off**: GE 2023-01-04 = 0.7803407 dan 2024-04-02 = 0.7975308; DD 2025-11-03 = 0.41824862. Ini faktor harga gaya CRSP, iaitu bahagian nilai yang kekal pada induk, bukan nisbah saham diagihkan.
- **CRSP**: spin-off dilayan sebagai peristiwa pecahan pada tarikh ex, dengan faktor harga = nilai setara tunai / harga ex. Jika tiada sebut harga hari itu, harga sehingga 10 tempoh kemudian digunakan — [CRSP methodology](https://crsp.org/wp-content/uploads/guides/CRSP_Calculations_and_Index_Methodologies.pdf).
- **Kesan harga selepas spin-off**:
  - Cusatis, Miles & Woolridge (1993) mendapati pulangan lebihan positif besar bagi spin-off 1965–88 dalam 36 bulan.
  - Satu kertas NYU melaporkan "an initial decline in returns experienced by the spinoffs in approximately the first 30 trading days after the distribution", yang berbalik selepas ~3 bulan. Brown & Brooke melaporkan penurunan ~4% akibat institusi menjual.
  - McConnell, Ozbilgin & Wahal (1989–1995) mendapati strategi itu "at best… break-even" berbanding penanda aras saiz/industri.
  - McConnell & Ovtchinnikov (2004) mendapati SpinCo mengatasi penanda aras 36 bulan (1965–2000).

  Sumber: [NYU (Low)](https://archive.nyu.edu/jspui/bitstream/2451/25967/2/Low.pdf); [McConnell et al. 2001](https://business.purdue.edu/faculty/mcconnell/publications/spinoffs-ex-ante-2001-vol74.pdf); [CNBC](https://www.cnbc.com/id/100978215).
- Kajian JSE mendapati "initial illiquidity in some of the spin-offs caused dramatic share price movements in the first few days" — [Urquhart Partners](https://urquhartpartners.substack.com/p/past-present-and-future-of-spin-offs).
- Yahoo kadang-kadang melaras sejarah induk secara retroaktif, kadang-kadang merekodnya sebagai "split" ganjil, dan dividen USD0.00 menandakan spin/M&A — [Fund Manager](https://www.fundmanagersoftware.com/forum/viewtopic.php?p=19443); [Wealth-Lab MRO](https://wealth-lab.com/Forum/Posts/Yahoo-Data-MRO-and-NOC-split-adjustments-not-applied-34260).

### Inferences
- **Amaran awal (T−bulan hingga T−hari)**:
  - Imbas EDGAR setiap malam untuk Form **10-12B / 10-12B/A** (CIK baharu). Nama SpinCo dan induk ada dalam information statement.
  - Petakan induk melalui teks atau 8-K induk (Item 8.01/2.01 lazimnya, belum disahkan).
  - Tandakan induk dalam senarai pemerhatian "spin belum selesai" dari pemfailan pertama hingga tarikh-ex + N.
- **Pengesahan pada tarikh-ex (malam T)**:
  - Panggil Moomoo rehab untuk ticker yang mempunyai jurang |open/close₋₁ − 1| > max(15%, 3·A) tanpa pecahan. Jika `SPINOFF` wujud bagi `ex_div_date` = T, faktor = `spin_off_ratio`.
  - Jika Moomoo belum ada rekod, tanda "tidak diketahui" dan sekat.
  - Tanda tambahan: ticker baharu dalam `nasdaqlisted.txt`/`otherlisted.txt`, atau `company_tickers.json` dengan CIK baru didaftar beberapa bulan sebelumnya.
- **Syarikat induk.** Pilihan A (lebih baik) ialah melaras semua bar sebelum T dengan `spin_off_ratio`. Penunjuk kemudiannya berterusan, dan siri hadapan Moomoo `autype=1` melakukannya secara automatik. Pilihan B ialah menyekat isyarat bagi bar T hingga T+5 dan memanaskan semula penunjuk (gaya ScaledRaw QuantConnect). Posisi terbuka yang melepasi T dengan siri mentah akan "tercetus henti" palsu. Nilai sebenar posisi maya = harga induk + (nisbah agihan × harga SpinCo), maka sama ada (i) laraskan henti dengan faktor, atau (ii) tutup pada tutup T−1 dengan sebab_keluar `spin_off` dan rekodkan berasingan daripada keluar kaedah.
- **Syarikat baharu (SpinCo).** Abaikan bar when-issued, kerana ia bersyarat, boleh dibatalkan dan nipis. Kebanyakan kaedah memerlukan sejarah (contohnya 50/200 MA), jadi syarat bar minimum sedia ada akan menapisnya. Tambah peraturan eksplisit "tiada isyarat sebelum 20 bar regular-way" kerana ~30 hari pertama mempunyai tekanan jualan institusi dan ketidakcairan.
- **Kesan pada stor repo.** Siri DD dalam stor sudah berterusan (dilaras hadapan, lihat Bahagian 4). Oleh itu backtest atau isyarat yang dikira **semula hari ini** tidak melihat jurang. Tetapi isyarat yang dijana **pada malam 3 Nov 2025** daripada data Yahoo mentah mungkin melihat −57%. Pencemaran sejarah hadapan hanya boleh diukur daripada arkib harian, bukan daripada stor semasa.

### Gaps
- Tidak disahkan sama ada Moomoo rehab menyenaraikan SPINOFF **sebelum** tarikh-ex, atau hanya selepas.
- Kelakuan Yahoo/yfinance terkini (2025–2026) untuk spin-off (laras atau tidak, dan bila) tidak dapat diuji kerana Yahoo tidak boleh dicapai dari sesi ini.
- Konvensyen akhiran simbol when-issued ("WI") dan cara Yahoo/Moomoo memaparkannya tidak disahkan.
- Item 8-K yang digunakan induk untuk mengumumkan spin-off (2.01/8.01) belum disahkan dengan sumber.

---

## 4. Mengesan pecahan dan pecahan songsang yang tidak dilaras atau lewat dilaras dalam data yfinance (ujian nisbah, ujian volum, perbandingan muat turun semula); kekerapan Yahoo tersilap

### Takeaway
Yahoo biasanya melaras pecahan AS, tetapi didokumenkan kadang-kadang (a) gagal melaras bar hari pecahan, (b) gagal melaras bar lama, dan (c) menunjukkan anjakan aras seperti pecahan tanpa rekod pecahan. Pembaikan yfinance sendiri pernah memberi positif palsu (GME, NVDA) sehingga semakan volum ditambah (1.1.0 hingga 1.7.0). Tiada statistik kekerapan awam. Ujian percuma paling kuat ialah: **jurang ≈ nisbah pecahan lazim + nilai dagangan (harga×volum) TIDAK melonjak + perbandingan dengan Moomoo mentah/rehab**. Pecahan songsang paling kerap berlaku pada saham bermasalah (rekod 93 dalam S1 2025), tetapi kebanyakannya di bawah USD10 sebelum pecahan.

### Cited Findings
- Kegagalan Yahoo yang didokumenkan dan positif palsu pembaikan ada dalam Bahagian 1 ([#1531](https://github.com/ranaroussi/yfinance/issues/1531), [#2660](https://github.com/ranaroussi/yfinance/issues/2660), [price_repair.rst](https://github.com/ranaroussi/yfinance/blob/main/doc/source/advanced/price_repair.rst), [CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst)). Pembaikan pecahan memerlukan julat tarikh yang merangkumi 1 hari selepas pecahan untuk kalibrasi. Versi 1.1.0 menambah semakan kemeruapan sekitar tarikh dan volum hari itu dan selepasnya. Versi 1.7.0 membaiki pepijat "volume-validation of stock-split-repair".
- Vendor lain juga tersilap: pecahan NVDA dikenakan dua kali dalam bundle QuantRocket "usstock" — [QuantRocket](https://support.quantrocket.com/t/split-adjustment-issue-in-usstock-daily/1698).
- Kekerapan pecahan songsang: S1 2025 mencatat 93, tertinggi dalam hampir 10 tahun (Wall Street Horizon). April 2025 mencatat 37 pengumuman, kemudian trend menurun — [Interactive Brokers / WSH](https://www.interactivebrokers.com/campus/traders-insight/securities/stocks/reverse-splits-start-to-moderate-after-hitting-a-record-high-in-q1-2025/). "In 2025, 145 companies have effectuated reverse stock splits" (snapshot pertengahan tahun) — [Sheppard Mullin](https://www.sheppard.com/insights/blogs/navigating-nasdaq-and-nyse-essential-insights-for-companies).
- Notis pecahan songsang Nasdaq: 10 hari kalendar kepada Nasdaq dan pendedahan awam ≥ 2 hari perniagaan sebelum berkesan (Bahagian 1). Pecahan hadapan dan dividen saham ≥ 25% mempunyai tarikh-ex = hari perniagaan pertama selepas tarikh bayar (FINRA 11140).
- **[Kod repo] Mekanisme stor sedia ada**: `kod/stor.py::gabung_kline` membandingkan bar bertindih lama dan baharu. Jika median nisbah tutup |r − 1| > 0.3%, semua bar lama didarab r (volum dibahagi r) — [`BacktestShariah2/kod/stor.py`](../../../kod/stor.py). `standard/harga_yf.py semak` membandingkan Yahoo dengan kline Moomoo dan keluar 1 jika beza > 0.5%, dan docstringnya menyatakan "Moomoo menang jika berbeza" — [`BacktestShariah2/standard/harga_yf.py`](../../../standard/harga_yf.py).
- **[Stor repo + Ujian Moomoo 22-10-2026] Konvensyen stor bercampur**:
  - DD dalam stor (30 Okt 2025 = 100.457, 31 Okt = 100.679, 3 Nov = 102.271, 4 Nov = 111.322; volum 2,763,830) sepadan **tepat** dengan Moomoo `autype=1` (100.456919, 100.678869, 102.270863, 111.321643; volum 2,763,833). Ia tidak sepadan dengan mentah (81.47, 81.65, 34.69, 37.76).
  - COST dalam stor, 31 Okt 2025: tutup 907.445 berbanding mentah Moomoo 911.45, iaitu nisbah 0.99561. Ini konsisten dengan pelarasan hadapan untuk dividen selepas tarikh itu (1.30 + 1.47 + 1.47 = 4.24 pada harga ~950 ≈ 0.45%).
  - Kesimpulan: bar lama stor dilaras **hadapan termasuk dividen dan spin-off** (konvensyen Futu), bukan "split sahaja" seperti docstring.
- **[Stor repo] Imbasan jurang**: bagi 946 ticker (Sep 2024 – Okt 2026) terdapat 85 jurang buka/tutup₋₁ > 40% (naik atau turun). Setiap satu yang mempunyai ≥ 20 bar sejarah menunjukkan nilai dagangan hari itu ≥ 2.5× median 20 hari (contohnya BRZE 20261020: volum 35.9×, nilai 64.0×; SMCI 20241030: 6.4×, 4.4×). Tiada yang berciri pecahan tidak dilaras (nilai dagangan ~1×). Ini dijangka kerana stor dilaras semula secara retroaktif, jadi ia tidak membuktikan data pada malam isyarat bersih.

### Inferences
- **Ujian nisbah (pada setiap bar baharu, sebelum imbasan kaedah).** Kira g = open_t / close_{t−1}, dan juga close_t / close_{t−1}. Tandakan "syak pecahan" jika |ln g| > ln(1.25) **dan** wujud R dalam {2, 3, 4, 5, 6, 8, 10, 15, 20, 3/2, 5/4} (pecahan hadapan, g ≈ 1/R) atau R dalam {2, 3, 4, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 100} (pecahan songsang, g ≈ R) sehingga |g·R^{±1} − 1| < max(4%, 1.5·A).
- **Ujian invarian nilai dagangan.** Pecahan tidak dilaras mengubah harga dengan 1/R dan volum dengan R, maka **nilai dagangan (P×V) kekal ~1×** median 20 hari, misalnya dalam 0.3× hingga 3×. Kejutan sebenar (keputusan suku, berita, spin-off) melonjakkan nilai dagangan ≥ 2.5×, seperti 85/85 jurang dalam stor. Julat intrahari (H−L)/C juga kekal normal bagi pecahan.
- **Ujian rujukan silang (pengesah):**
  - (i) Moomoo rehab: wujud `SPLIT`/`JOIN` dengan `ex_div_date` = t dan nisbah ≈ R.
  - (ii) Moomoo kline `autype=0` untuk t−1 dan t: jika mentah Moomoo menunjukkan jurang yang sama, ia peristiwa sebenar. Jika tidak, Yahoo silap.
  - (iii) yfinance `Ticker.splits` untuk tarikh t.
- **Ujian lewat-laras (muat turun semula).** Esoknya (t+1), muat turun semula tetingkap 10 hari. Jika bar t−1 kini berbeza dengan nisbah ≈ R, Yahoo baru melaras. Mekanisme `gabung_kline` sudah mengesan ini (ambang 0.3%) dan melaras stor, tetapi **isyarat yang dijana pada malam t sudah tercemar**. Perlu ada log "pelarasan stor" (ticker, tarikh, r) supaya isyarat/posisi dalam tetingkap itu boleh dibatalkan.
- **Risiko median nisbah dalam `gabung_kline`.** Jika tetingkap bertindih separuh dilaras (Yahoo melaras hanya sebahagian bar, seperti isu #1531), median boleh memilih r yang salah. Lebih selamat ialah memeriksa nisbah **setiap** bar bertindih. Jika nisbah tidak seragam (contohnya dua kelompok), tolak gabungan dan bendera ticker untuk semakan Moomoo.
- **Konvensyen bercampur dalam stor (penemuan penting).** Bar lama datang daripada Moomoo `autype=1` (laras dividen hadapan), manakala bar baharu daripada Yahoo (split sahaja). Siri yang sama itu separuh dilaras dividen dan separuh tidak. Pada setiap tarikh-ex selepas peralihan, jurang dividen kekal dalam bar baharu, sedangkan bar lama sudah "berlaras". Bagi DD, jika kline Moomoo `autype=1` digabung selepas pecahan songsang 2026-06-24, seluruh sejarah berubah ~3×. `gabung_kline` membetulkan ini hanya jika tetingkap bertindih. Cadangan: tetapkan **satu** konvensyen, iaitu Moomoo `autype=0` (mentah) + faktor rehab `exclude_divi` untuk pecahan/spin, atau Yahoo split-only + faktor spin. Tetapkan `autype` secara eksplisit dalam semua panggilan `quote_history_kline` dalam prosedur jadual, kerana lalai = 1.
- **Saham ≥ USD10 dan pecahan songsang.** Kebanyakan pecahan songsang berlaku pada saham bawah USD1–5. Selepas pecahan, harga boleh melepasi USD10 dan saham **memasuki** universe dengan sejarah yang dilaras secara songsang. Volum lama dibahagi R, dan saham ini biasanya bermasalah. Tambahkan peraturan "JOIN dalam 120 hari terakhir → tidak layak" dalam `kod/tidak_layak.py` (inferens; ambang perlu dikaji).

### Gaps
- Tiada statistik awam tentang kadar Yahoo terlepas atau lewat melaras pecahan AS (pengarang yfinance hanya menulis "US data appears perfect").
- Masa purata Yahoo membetulkan pecahan tidak diketahui.
- Saiz nisbah pecahan songsang lazim 2025–2026 tidak dikumpul.
- Bilangan pecahan songsang yang menghasilkan harga ≥ USD10 tidak diketahui.
- Tidak dapat menjalankan yfinance dari sesi ini untuk menguji kes sebenar (Yahoo disekat).

---

## 5. Mengesan pertukaran ticker / penggunaan semula simbol supaya sejarah tidak terpisah atau tersambung salah (termasuk tukar CUSIP dan domisil semula)

### Takeaway
Jangan gunakan ticker sebagai kunci kekal. Gunakan **CIK SEC** (percuma, stabil merentas tukar nama dan ticker) atau ID sekuriti Moomoo sebagai kunci, dan simpan peta ticker→CIK harian. Banding peta setiap malam (`company_tickers.json` + `nasdaqlisted.txt`/`otherlisted.txt`):
- ticker hilang dan ticker baharu muncul dengan CIK sama = **tukar ticker** (sambung sejarah);
- ticker sama dengan CIK berbeza = **guna semula simbol** atau **successor issuer** (putuskan sejarah, atau sahkan kesinambungan).

QuantConnect menyelesaikan masalah ini dengan "map files" dan Security Master. Domisil semula atau penyusunan induk biasanya tidak menghasilkan jurang harga, tetapi boleh menukar CIK/CUSIP.

### Cited Findings
- QuantConnect US Equity Security Master "tracks US Equity corporate actions, including splits, dividends, delistings, mergers, and ticker changes through history" — [QuantConnect Security Master](https://quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-equity-security-master).
- Daily List Nasdaq (berbayar) merangkumi "symbol changes", penyenaraian baharu dan penyahsenaraian — [Federal Register 2024-14377](https://www.federalregister.gov/documents/2024/07/01/2024-14377/self-regulatory-organizations-the-nasdaq-stock-market-llc-notice-of-filing-and-immediate).
- `company_tickers.json` SEC memetakan ticker ↔ CIK ↔ nama. Ia dikemas kini berkala tanpa jaminan ketepatan. Satu panduan memberi amaran supaya peta ticker tidak digunakan selama-lamanya kerana ticker dan identiti syarikat berubah — [SEC Accessing EDGAR Data](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm) (ringkasan carian).
- Successor issuer: syarikat induk baharu menjadi entiti awam di bawah Rule 12g-3(a) — [Cannagistics 8-K](https://docoh.com/filing/1304741/0001663577-21-000256/CNGT-8K); [ZoomInfo](https://ir.zoominfo.com/node/10731/html).
- Contoh sejarah tukar simbol Nasdaq (CYTI → MSHK, 1991) dalam notis FINRA/NASD — [NASD NTM 91-15](https://www.finra.org/rules-guidance/notices/91-15). Ini hanya ilustrasi, kerana notis sedemikian tidak lagi diterbitkan.
- Carian isu yfinance untuk "ticker changed / renamed" tidak menemui isu khusus yang mendokumenkan cara Yahoo menyambung sejarah selepas tukar ticker (carian GitHub dalam sesi ini, 229 hasil tidak berkaitan langsung) — [isu yfinance](https://github.com/ranaroussi/yfinance/issues).

### Inferences
- **Algoritma harian (percuma)**:
  1. Muat `company_tickers.json` (SEC, ≤ 10 req/s, dengan User-Agent) dan direktori simbol Nasdaq.
  2. Bina `peta[t] = (CIK, nama, bursa)` dan simpan dalam repo, misalnya `data/peta_cik/YYYYMMDD.csv`.
  3. Bandingkan dengan semalam. Peraturan:
     - (a) ticker A hilang, ticker B baharu, CIK(B) = CIK(A) lama → **tukar ticker**: alihkan sejarah stor A ke B dan kemas kini posisi papertrade.
     - (b) ticker sama, CIK berubah → **simbol diguna semula** (syarikat lain) atau **successor issuer** (domisil semula / induk baharu). Semak nama dan 8-K12B/8-K yang menyebut "successor issuer". Jika nama berubah sepenuhnya dan tiada pengganti, **putuskan sejarah**: mula semula dengan sifar bar, dan tutup posisi sebagai `tidak_sah`.
     - (c) ticker hilang tanpa pengganti → laluan delist sedia ada (`tidak_layak.py posisi`).
  4. Pengesahan harga: sejarah yang disambung mesti berterusan (|ln(close_B,t / close_A,t−1)| < 3·A). Jika tidak, ada peristiwa lain (pecahan/spin) serentak.
- **Ujian OHLCV untuk sambungan salah.** Jika satu ticker menunjukkan jurang aras + perubahan rejim volum kekal (median 60 hari selepas berbeza > 5× sebelum), serta tempoh tanpa bar ≥ 5 sesi sebelumnya, syaki guna semula simbol. Data Yahoo untuk ticker yang diguna semula boleh menyambung syarikat lama dengan syarikat baharu.
- **Domisil semula / tukar CUSIP.** Pertukaran biasanya saham-untuk-saham 1:1, jadi harga berterusan. Risiko utamanya ialah ticker atau CIK berubah dan Yahoo memulakan siri baharu (sejarah pendek → kaedah tidak cukup bar → isyarat hilang, bukan palsu). Kes yang menukar nisbah (contohnya holdco dengan nisbah bukan 1:1) akan dikesan oleh ujian nisbah Bahagian 4.
- Moomoo menyimpan pengenal sekuriti dalaman (`stock_id`, disebut dalam deskripsi alat dividends). Ia mungkin stabil merentas tukar ticker, tetapi ini tidak disahkan.

### Gaps
- Tidak disahkan sama ada JSON `submissions` SEC mengandungi medan `tickers`, `exchanges` dan `formerNames` (dari ingatan ya, tetapi tidak dibaca dalam sesi ini).
- Tiada sumber tentang cara Yahoo mengendalikan sejarah selepas tukar ticker atau guna semula simbol.
- Tiada sumber percuma rasmi yang ditemui untuk sejarah tukar simbol Nasdaq/NYSE moden (halaman nasdaq.com "symbol change history" tidak muncul dalam carian).
- Kekerapan guna semula simbol dalam universe ≥ USD10 tidak diketahui.
- Peranan Form 8-K12B tidak disahkan dengan sumber.

---

## 6. Peraturan konkrit yang patut digunakan sistem: sekat isyarat N hari sekitar peristiwa, laras sejarah, atau keluarkan posisi

### Takeaway
Gunakan pendekatan berlapis: **(1) kalendar awal** (Moomoo dividends/rehab + EDGAR), **(2) pelarasan sejarah** bagi pengiraan penunjuk dengan satu konvensyen sahaja (split + spin + dividen besar; dividen kecil pilihan), **(3) tetingkap sekatan** untuk peristiwa besar atau yang tidak diketahui, dan **(4) pelarasan posisi** (henti dikurangkan dengan D atau faktor; kuantiti dilaras untuk pecahan; spin-off ditutup atau digabung nilai). Pengamal utama memilih *melaras* berbanding *menyekat*: QuantConnect (mod Raw + SplitFactor + ScaledRaw), CRSP dan Norgate (faktor), dan FINRA 5330 (pesanan dikurangkan D). Sekatan hanya untuk peristiwa yang faktornya tidak pasti.

### Cited Findings
- QuantConnect Raw: "dividends paid as cash and splits adjusting the quantity of your holdings". ScaledRaw digunakan untuk "reset and warm-up" penunjuk selepas pecahan. Peristiwa Split dihantar "when a split is in the near future and when it occurs" — [QuantConnect forum #508](https://www.quantconnect.com/forum/discussion/508/update-dividends-splits-and-custom-price-normalization/p1); [QC corporate actions](https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/us-equity/corporate-actions).
- FINRA 5330: pesanan terbuka dikurangkan dengan dividen pada tarikh-ex. Untuk pecahan dan dividen saham, harga dan saiz pesanan dilaras — [FINRA 5330](https://finra.org/rules-guidance/rulebooks/finra-rules/5330).
- Norgate/RealTest: pilihan melaras hanya "capital reconstructions and special dividends" — [Wealth-Lab](https://wealth-lab.com/Discussion/Price-adjustment-to-not-apply-to-regular-cash-dividends-Wealth-Data-8593); [RealTest](https://mhptrading.com/docs/topics/idh-topic1390.htm). Morningstar menetapkan ambang dividen khas 5% — [Morningstar](https://indexes.morningstar.com/api/docs/6883c000fb8ee1d878f734a6).
- CRSP melayan spin-off dan hak sebagai peristiwa berfaktor harga (FACPR ≠ FACSHR) — [CRSP](https://crsp.org/wp-content/uploads/guides/CRSP_Calculations_and_Index_Methodologies.pdf).
- Peraturan tarikh-ex ≥ 25% (selepas tarikh bayar) dan notis pecahan songsang ≥ 2 hari perniagaan — [FINRA 11140](https://www.finra.org/rules-guidance/rulebooks/finra-rules/11140); [AFS Law](https://www.afslaw.com/perspectives/alerts/nasdaq-rule-change-lengthens-reverse-stock-split-notice-period).
- SpinCo menunjukkan penurunan awal ~30 hari dagangan selepas pengagihan — [NYU (Low)](https://archive.nyu.edu/jspui/bitstream/2451/25967/2/Low.pdf).

### Inferences
**Jadual peraturan yang dicadangkan.** Semua nilai N dan ambang ialah cadangan reka bentuk, bukan nilai bersumber; uji dengan Lejar Penuh.

| Peristiwa | Kesan awal / sumber | Sejarah (penunjuk) | Isyarat baharu | Posisi terbuka |
|---|---|---|---|---|
| Dividen biasa D/P < 0.5% | Moomoo dividends (≈2 minggu awal) | Tiada pelarasan (pilihan: laras) | Tiada sekatan | Henti dikurangkan D pada tarikh-ex (FINRA 5330); kreditkan D jika dipegang melepasi ex |
| Dividen 0.5–2% / 0.25–0.75 ATR | Sama | Laras bar < ex dengan (1 − D/P) | Tiada sekatan | Sama |
| Dividen ≥ 2% / ≥ 0.75 ATR / `SPECIALDIVIDEND` / "special" | Moomoo rehab + teks `statement` | Laras (1 − D/P) | Sekat jika bar pencetus = ex hingga ex+2 | Henti − D; tanda `peristiwa=dividen_khas` |
| Pengagihan ≥ 25% (tunai/saham) | FINRA 11140: ex = hari selepas bayar; due bill | Laras dengan faktor | Sekat dari pengumuman hingga ex+5 | Laras henti dengan faktor, atau tutup pada tutup ex−1 (`sebab_keluar=tindakan_korporat`) |
| Pecahan hadapan / dividen saham | Moomoo rehab SPLIT; yfinance splits; ujian nisbah + nilai dagangan | Laras dengan R (volum ×R) | Sekat ex hingga ex+1 jika Yahoo belum laras (semak t+1) | Kuantiti ×R, harga beli dan henti ÷R (mod Raw QC) |
| Pecahan songsang (JOIN) | 8-K 3.03/5.03; notis ≥ 2 hari; Moomoo JOIN | Laras ÷R | Sekat ex hingga ex+5; **tidak layak 120 hari** (cadangan) | Kuantiti ÷R, harga ×R |
| Spin-off | Form 10-12B (berbulan), when-issued; Moomoo SPINOFF `spin_off_ratio` | Laras induk dengan faktor | Induk: sekat ex hingga ex+5 jika faktor tidak diketahui. SpinCo: abaikan WI, tiada isyarat < 20 bar regular-way | Tutup pada tutup ex−1 atau nilai = induk + SpinCo; henti × faktor |
| Terbitan hak (rights) | 424B/S-1/S-3, Moomoo `allotment_ratio`/`allot_price` | Laras ikut faktor CRSP (jika ada) | Sekat dari pengumuman hingga tamat langganan | Tanda; pertimbang tutup |
| Tukar ticker / CIK | Diff `company_tickers.json` + SymDir | Sambung (CIK sama) / putus (CIK beza) | Sekat 1 bar selepas sambungan untuk pengesahan | Alih posisi ke ticker baharu atau `tidak_sah` |
| Jurang tidak diterangkan (> max(25%, 3·A), nilai dagangan ~1×) | Peraturan OHLCV | **Kuarantin**: jangan laras secara automatik | Sekat sehingga disahkan (Moomoo mentah/rehab) | Jangan cetus henti/keluar daripada bar itu; semak semula esok |

Langkah pelaksanaan dalam sistem (cadangan):
1. Langkah baharu dalam `harian_c.py malam` dan `lejar.py` sebelum imbasan:
   - `peristiwa_korporat.py` membina `data/peristiwa/YYYYMMDD.csv` (ticker, jenis, ex, faktor, D, sumber, status).
   - Sumber: Moomoo rehab/dividends untuk calon dan posisi, yfinance actions, diff peta CIK, dan imbasan OHLCV.
2. Satu pintu sekatan, seperti `kod/tidak_layak.py`, ditambah `kod/peristiwa.py` dengan fungsi `sekat(ticker, tarikh)` dan `faktor(ticker, tarikh)`. Fungsi ini dipanggil oleh scanner, Lejar Penuh, senarai beli dan watchlist. Peraturan ini mengikut corak satu pintu yang sudah digunakan untuk ambil alih dan tidak cair.
3. Log pelarasan stor: setiap kali `gabung_kline` melaras (|r − 1| > 0.3%), tulis (ticker, tarikh, r) dan batalkan isyarat yang dijana dari bar yang kemudiannya dilaras.
4. Seragamkan konvensyen harga: nyatakan `autype` secara eksplisit dalam semua panggilan kline Moomoo, dan pilih satu (mentah + faktor, atau hadapan tanpa dividen). Ini membetulkan stor bercampur yang ditemui di Bahagian 4.
5. Lorong 2 (Chandelier) menggunakan tutup tertinggi sejak beli. Selepas pecahan/spin, laraskan tutup tertinggi dan ATR dengan faktor yang sama. Jika tidak, paras Chandelier tercetus palsu.

### Gaps
- Tiada sumber pengamal yang menyatakan nilai N (hari sekatan) secara eksplisit. Semua nilai N di atas ialah cadangan.
- Tiada kajian ditemui tentang kekerapan setiap jenis peristiwa dalam universe Shariah ≥ USD10 (≈2,000 saham). Ini boleh diukur dengan memanggil Moomoo rehab untuk seluruh universe sekali (kos panggilan perlu dinilai).
- Mekanik terbitan hak di pasaran AS (kekerapan, contoh 2024–2026, cara Yahoo/Moomoo merekodnya) tidak dikaji kerana masa terhad. Hanya medan `allotment_ratio`/`allot_base`/`allot_ert` Moomoo dan layanan CRSP (FACPR ≠ FACSHR) yang dikenal pasti.
- Kesan dividen tunai pada P&L Papertrade C/Lejar (dikreditkan atau tidak) perlu disemak dalam kod `lejar.py` / `keluar_lorong.py`. Ia tidak diperiksa dalam kajian ini.
