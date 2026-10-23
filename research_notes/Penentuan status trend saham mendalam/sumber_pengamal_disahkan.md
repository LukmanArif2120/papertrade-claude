# Pengesahan peraturan rangka trend pengamal dan label trend platform (sumber primer / hampir primer)

Disediakan 23 Okt 2026. Nota ini mengesahkan atau membetulkan butiran bertanda *(ingatan; sahkan)* atau "belum disahkan" dalam tiga nota terdahulu:
- `research_notes/Penentuan status trend saham/rangka_pengamal.md` (selepas ini "RP");
- `research_notes/Penentuan status trend saham/pengesanan_mula_naik.md` ("PMN");
- `scratchpad/trend/nota_amalan_trend.md` ("NAT").

Konteks: papan swing saham AS patuh Syariah (pegangan 3–30 sesi). Status trend dipaparkan pada Posisi dan Watchlist untuk membantu keputusan pegang/jual.

**Had kaedah (penting).**
- WebFetch gagal bagi semua domain luar (`getaddrinfo ENOTFOUND`). `curl` melalui proksi ditolak bagi semua hos kecuali `raw.githubusercontent.com`, `github.com` (git clone) dan `pypi.org`. API carian GitHub disekat ("sessions are bound to their configured repositories").
- Carian WebSearch tidak dibenarkan untuk domain `investors.com`. Halaman IBD tidak dapat dibaca langsung.
- Oleh itu bukti datang daripada tiga saluran:
  - (a) petikan WebSearch "extended" atas halaman rasmi (StockCharts help/ChartSchool, Barchart, moomoo, thepatternsite, Quantifiable Edges);
  - (b) kod sumber terbuka yang dibaca terus daripada GitHub dan disimpan di `scratchpad/sumber/` (tidak dilaksanakan);
  - (c) pemerhatian langsung alat SST Terminal (baca sahaja, 23 Okt 2026 03:31–03:39 UTC).
- Petikan buku Weinstein tentang volum pecahan ke bawah dikesan oleh enjin carian dalam salinan PDF tidak rasmi buku 1988. URL salinan itu sengaja **tidak** dipautkan. Rujukan diberi kepada buku itu sendiri, dan teks tepat perlu disemak pada edisi berlesen.

**Label bukti (diminta pemanggil):**
- **[ASAL-PETIK]**: petikan kata-kata pengarang atau dokumen rasmi platform (termasuk melalui petikan enjin carian; dinyatakan jika melalui salinan atau agregator).
- **[ASAL-KOD]**: pelaksanaan setia (port berlesen daripada kod asal platform, atau kod yang menyatakan sumber asalnya).
- **[SEKUNDER]**: sumber kedua sahaja.
- **[TIDAK DISAHKAN]**: tiada bukti boleh dipercayai dalam sesi ini.
- **[IN]**: inferens penulis nota.

Fail sumber yang dibaca (dalam `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/sumber/`):
- `obrii/python/tv_rules.py` (port TradingView TechnicalRating v3, MPL-2.0);
- `raw/tvta_technicals.py` (python-tradingview-ta, "Rewritten from tradingview.com/static/bundles/technicals…js");
- `raw/agena_tt.cs` (teks Trend Template Minervini dalam komen kod 2016);
- `raw/talib_adxr.c` (TA-Lib);
- `raw/sctr_tos.ts` (replikasi SCTR ThinkOrSwim 2015);
- `rosskevin_pine-scripts/` dan `shravanmateti_weinstein-stage-analysis/` (pelaksanaan Weinstein).

---

## 1. Weinstein Stage Analysis: takrif Peringkat 1–4, peraturan cerun MA 30 minggu, gandaan volum tembusan, RS Mansfield, setara harian

### Takeaway
- Kerangka empat peringkat disahkan secara konsisten. Weinstein **tidak** memberi ambang angka bagi "cerun rata", jadi pelaksana memilih sendiri, contohnya ±0.5% atau ±2% perubahan MA dalam 4 minggu.
- **Volum tembusan:** sokongan terkuat ialah **≥ 2×**, melalui Bulkowski yang membaca dan menguji peraturan buku: lonjakan satu minggu ≥ 2× purata 4 minggu sebelumnya, atau timbunan volum 3–4 minggu ≥ 2× tahap sebelumnya. Angka 1.5× ialah ambang pengarang lain. Satu sumber sekunder pula mempertikaikan bahawa "2× purata 4 minggu" ialah perkataan Weinstein sendiri.
- **Pecahan ke Peringkat 4:** buku menyatakan pecahan ini **tidak semestinya** memerlukan lonjakan volum besar.
- **RS Mansfield > 0** tidak ditemui sebagai peraturan keras daripada buku. Buku mentakrif RS sebagai harga saham ÷ purata pasaran. Garis sifar Mansfield (MA 52 minggu) datang daripada carta Mansfield yang dipakai Weinstein.
- **Setara harian 150 hari** datang daripada Minervini dan pelaksana, bukan daripada Weinstein.
- **Bukti empirikal baharu** (praterbit 2026): Peringkat 1 dan Peringkat 3 tidak dapat dibezakan secara statistik. Peringkat 2 ≈ penapis MA naik (+2.3%/tahun lebihan, t = 2.7). Strategi "Weinstein penuh" mempunyai Sharpe sama dengan penapis MA satu baris.

### Cited Findings
**Takrif peringkat [SEKUNDER, konsisten merentas sumber]**
- **Peringkat 1:** MA 30 minggu berhenti jatuh dan mendatar selepas penurunan, dan harga berulang-alik merentasinya di dalam asas.
- **Peringkat 2:** bermula apabila harga pecah di atas asas dengan volum kuat dan kekal di atas purata yang sudah berpusing naik.
- **Peringkat 3:** cerminan Peringkat 1 di puncak (purata mendatar, harga berayun merentasinya).
- **Peringkat 4:** bermula dengan pecahan di bawah sokongan puncak, dengan harga di bawah purata yang menurun. "The falling average is a ceiling and rallies die at it."
- — [MQL5](https://www.mql5.com/en/articles/22746); [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/); [EBC](https://www.ebc.com/forex/stan-weinstein-stage-analysis); [tradecraft.academy](https://www.tradecraft.academy/learn/stage-analysis)

**Larangan beli di bawah MA 30 minggu [SEKUNDER]**
- Satu laman menyatakan saham di bawah purata 30 minggu, terutamanya jika purata itu jatuh, "should never be considered for purchase". Ini **tidak** dapat disahkan sebagai petikan buku. — [tradeyourplan.pro](https://tradeyourplan.pro/know/stage-analysis/); [stage2stocks.com](https://www.stage2stocks.com/stan-weinstein)

**Volum tembusan (Peringkat 1→2)**
- [SEKUNDER kuat] Halaman "Trading Weinstein" Bulkowski menguji peraturan beli:
  - "a one-week volume spike that is at least twice the average of the prior four weeks";
  - jika tiada lonjakan, "a build-up of volume over the past four weeks that is at least twice as high as the prior three *months*", dengan volum minggu tembusan lebih tinggi daripada minggu sebelumnya;
  - Bulkowski mencatat: "In his book, he uses three 'weeks' instead of 'months' but testing shows there's no difference".
  - Reka bentuk ujian: dalam sampel 2000–2011, luar sampel 2011–Okt 2023, 451–452 saham. Angka keputusan tidak dapat dibaca.
  - — [thepatternsite: Trading Weinstein](https://thepatternsite.com/TradingWeinstein.html)
- [SEKUNDER] Ulasan buku menyatakan dua laluan: (a) lonjakan satu minggu ≥ 2× purata beberapa minggu lalu; atau (b) timbunan 3–4 minggu ≥ 2× purata beberapa minggu sebelumnya, "coupled with at least some increase in the breakout week". — [whatheheckaboom (ulasan buku)](https://whatheheckaboom.wordpress.com/2012/01/01/book-review-of-stan-weinsteins-secrets-for-profiting-in-bull-and-bear-markets/)
- **Bercanggah:** Kagels Trading menulis bahawa "at least twice the average of the four prior weeks" ialah "a modern rule of thumb from websites such as stageanalysis.net; we could not confirm it as Weinstein's own wording". — [Kagels Trading](https://kagels-trading.com/blog/stage-analysis/)
  - Senarai semak stageanalysis.net memang menggunakan "at least two times the four week average". — [stageanalysis.net checklist](https://www.stageanalysis.net/blog/4372/stage-analysis-breakout-quality-checklist)
- **Gandaan lain bukan daripada Weinstein:** "1.5 times the 50-week average" dan "2–3× average daily volume" ialah ambang laman lain. Edgestacker menyatakan: "Stan Weinstein describes this setup without exact numbers; this is our stated formalization". — [edgestacker](https://www.edgestacker.com/tools/library/scans/weinstein/stage-2-breakout/); [thierryvonarvy substack](https://thierryvonarvy.substack.com/p/stan-weinsteins-secrets-for-profiting)

**Volum pecahan ke bawah (Peringkat 3→4)**
- [ASAL-PETIK, melalui petikan enjin carian daripada salinan tidak rasmi buku; perlu semak edisi berlesen] Pecahan ke Peringkat 4, tidak seperti tembusan menaik, "doesn't necessarily need such a huge increase in volume to be considered valid". Saham boleh "fall of their own weight", tetapi sepatutnya ada sedikit peningkatan volum, dan peningkatan volum pada pecahan adalah lebih bearish. — Weinstein (1988), *Stan Weinstein's Secrets for Profiting in Bull and Bear Markets*, McGraw-Hill ([Goodreads, maklumat buku](https://www.goodreads.com/book/show/116948.Secrets_For_Profiting_in_Bull_and_Bear_Markets))
- Disokong ringkasan berasingan ("shares can fall under their own weight (there does not have to be an increase in volume)"). [SEKUNDER] — [Trade2win](https://www.trade2win.com/threads/stage-analysis-finding-the-breakout-shares.22134/)
- Bulkowski (pandangan beliau sendiri): volum bukan kunci Peringkat 4 kerana boleh berat atau ringan semasa harga jatuh. — [thepatternsite: Stages](https://www.thepatternsite.com/Stages.html)

**Cerun MA 30 minggu: tiada ambang daripada Weinstein [TIDAK DISAHKAN sebagai angka Weinstein]**
- Pelaksana memilih ambang sendiri:
  - [ASAL-KOD] `shravanmateti/weinstein-stage-analysis`:
    - `MA_LEN, FAST_LEN, SLOPE_LEN, FLAT = 30, 10, 4, 0.5`;
    - cerun = % perubahan MA 30 minggu dalam 4 minggu; naik jika > +0.5%, turun jika < −0.5%;
    - `VOL_LEN, VOL_MULT = 30, 2.0`;
    - `confirmWeeks = 2` ("Weeks MA must stop rising/falling to change stage");
    - mesin keadaan: "Each stage can only move to the stages that are allowed to follow it".
    - — [GitHub shravanmateti/weinstein-stage-analysis](https://github.com/shravanmateti/weinstein-stage-analysis)
  - [SEKUNDER] `sowmiyanm/Research_SM`: cerun WMA 30 minggu = (WMA − WMA 4 minggu lalu)/WMA 4 minggu lalu × 100, dengan ambang ±2%. — [GitHub sowmiyanm/Research_SM](https://github.com/sowmiyanm/Research_SM)

**RS Mansfield**
- [ASAL-PETIK melalui laman pengamal] Buku (hlm. 18) mentakrif relative strength sebagai harga saham (atau purata kumpulan) dibahagi harga purata pasaran. — [stageanalysis.net](https://www.stageanalysis.net/blog/4266/how-to-create-the-mansfield-relative-performance-indicator)
- [SEKUNDER] Garis sifar Mansfield ialah "the 52 week MA of the Relative Strength line, that's been flattened". Dalam versi asal, garis RS dibahagi dengan MA 52 minggunya dan garis mendatar diletak pada sifar. — [stageanalysis.net](https://www.stageanalysis.net/blog/489325/how-to-setup-the-mansfield-relative-strength-indicator-in-tradingview); [TradingView, Mansfield RS Original](https://kr.tradingview.com/script/NzUBDDtb-Mansfield-Relative-Strength-Original-Version-by-stageanalysis)
- [TIDAK DISAHKAN] "RS > 0 / never buy when RS is negative" sebagai peraturan buku. Sumber terdekat hanya menyatakan RS "positive or turning positive" bagi calon beli. — [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)
- [ASAL-KOD; varian] Skrip `mansfield.pine` (rosskevin) menggunakan `rsm = (rsd/sma(rsd, 50) - 1) * 100` pada data harian dengan indeks bursa (IXIC/NYA). Ini MA 50 hari, bukan 52 minggu. Pelaksanaan RS Mansfield berbeza-beza. — [GitHub rosskevin/pine-scripts](https://github.com/rosskevin/pine-scripts)

**Setara harian**
- [ASAL-KOD] README rosskevin: "In a weekly chart, it's the 10, 30, and 40 period moving averages. In all other interval sizes it's the 50, 150, and 200 period moving averages." — [GitHub rosskevin/pine-scripts](https://github.com/rosskevin/pine-scripts)
- [ASAL-KOD] Skrip shravanmateti: `"Stage MA (30-week = 150-day)"` dengan penukaran ×5 pada carta harian. — [GitHub shravanmateti](https://github.com/shravanmateti/weinstein-stage-analysis)
- Teks Minervini (lihat §2) menulis "the 150-day (30-week) and the 200-day (40-week)". Weinstein sendiri menggunakan carta mingguan; tiada petikan beliau tentang 150 hari ditemui.

**Bukti empirikal [SEKUNDER-akademik; praterbit tanpa semakan rakan]**
- Roskill (SSRN, Sep 2026): 901,533 minggu-saham bebas bias kemandirian (ahli S&P 500 titik-masa, 1992–2026).
  - Di antara minggu dengan MA 30 minggu rata, Peringkat 1 lawan Peringkat 3 tidak berbeza: beza 13 minggu ≈ −0.6%/tahun (t = −0.5), merentas 12 spesifikasi pengelas.
  - Hanya Peringkat 2 memberi pulangan lebihan pasaran positif (+2.3%/tahun, t = 2.7), "essentially a rising moving-average trend filter by construction".
  - Strategi "full Weinstein" dan penapis MA satu baris: Sharpe 0.85 lawan 0.85; MAR 0.32 lawan 0.32.
  - — [SSRN 7429238](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7429238)
- [ASAL-KOD; bias pemilihan diakui] Backtest shravanmateti (594 saham NSE, mingguan 2016–2026): kadar menang 32.8%, faktor untung 3.33, median dagangan −4.2%. Senarai saham dipilih daripada saham Peringkat 2 pada 2026-10-01 ("mostly today's winners. The results are optimistic"). — [GitHub shravanmateti](https://github.com/shravanmateti/weinstein-stage-analysis)

### Inferences
- **[IN] Pembetulan RP §1:**
  - (a) "≥ 2×" ialah tafsiran terbaik peraturan volum Weinstein (Bulkowski), manakala "≥ 1.5×" bukan daripada Weinstein;
  - (b) gap "volum tidak diperlukan untuk pecahan ke bawah" kini disokong petikan buku (kualifikasi: "not necessarily … huge", tetapi "some increase");
  - (c) "RS Mansfield > 0" kekal sebagai tambahan pengamal.
- **[IN]** Dapatan Roskill menyokong kesimpulan RP: label yang hanya melihat MA tidak boleh membezakan Peringkat 1 daripada 3, dan maklumat ramalan datang daripada "MA naik + harga di atasnya". Bagi papan, susunan MA + cerun memberi hampir semua manfaat Weinstein. Tiada keperluan untuk keadaan "asas" lawan "puncak" berasingan.
- **[IN]** Jika papan mahu "Peringkat 2 awal" versi harian, ambang yang boleh dipertahankan ialah:
  - cerun SMA150 dalam 20 sesi > +0.5% (setara pelaksana 4 minggu);
  - tembusan julat 50 hari dengan volum ≥ 2× purata 20 sesi.
  - Kedua-dua ambang ialah pilihan reka bentuk, bukan "peraturan Weinstein".

### Gaps
- Teks buku tentang volum tembusan (perkataan tepat dan tempoh asas) tidak dapat dibaca. Pernyataan Bulkowski dan Kagels bercanggah tentang sama ada "2× purata 4 minggu" ialah perkataan Weinstein.
- Angka keputusan ujian Bulkowski "Trading Weinstein" (pulangan, kadar menang) tidak diperoleh.
- Sub-peringkat (2A/2B) dan peraturan "continuation buy" tidak dapat disahkan daripada buku. Ulasan menyebut "Ideal Buy for Investor" lawan "Ideal Buy for Trader", tetapi tanpa petikan. — [whatheheckaboom](https://whatheheckaboom.wordpress.com/2012/01/01/book-review-of-stan-weinsteins-secrets-for-profiting-in-bull-and-bear-markets/)

---

## 2. Templat Trend Minervini (8 syarat, angka tepat) dan VCP

### Takeaway
- Teks lapan syarat yang beredar disalin **verbatim dan konsisten** oleh sekurang-kurangnya tiga sumber bebas (komen kod AgenaTrader 2016 yang memetik StockFetcher, ProRealCode, ChartMill). Ayat syarat 3 yang tepat ialah **"trending up for at least 1 month (preferably 4–5 months minimum in most cases)"**. Kedua-dua perkataan "preferably" dan "minimum" ada; pertikaian dalam RP/NAT sudah selesai.
- Minervini sendiri (rantaian tweet) menyatakan saham mesti memenuhi **kesemua lapan** syarat untuk dianggap "confirmed stage 2 uptrend".
- Takrif VCP kekal sekunder: 2–6 kecutan (lazimnya 2–4), setiap satu lebih kecil daripada sebelumnya, volum mengering. Notasi "T" ialah konvensyen ChartMill/pengamal.

### Cited Findings
**Teks lapan syarat** [ASAL-PETIK melalui salinan; teks sama dalam sumber bebas] — [AgenaTrader, TrendTemplate_MarkMinervini_Indicator.cs](https://github.com/simonpucher/AgenaTrader/blob/master/Indicator/TrendTemplate_MarkMinervini_Indicator.cs); [ProRealCode](https://www.prorealcode.com/prorealtime-market-screeners/trend-template-mark-minervini/); [StockFetcher](https://www.stockfetcher.com/forums/Filter-Exchange/Trend-Template-by-Mark-Minervini/125969)

> 1. "The current stock price is above both the 150-day (30-week) and the 200-day (40-week) moving average price lines."
> 2. "The 150-day moving average is above the 200-day moving average."
> 3. "The 200-day moving average line is trending up for at least 1 month (preferably 4–5 months minimum in most cases)."
> 4. "The 50-day (10-week) moving average is above both the 150-day and 200-day moving averages."
> 5. "The current stock price is trading above the 50-day moving average."
> 6. "The current stock price is at least 30 percent above its 52-week low. (Many of the best selections will be 100 percent, 300 percent, or greater above their 52-week low …)"
> 7. "The current stock price is within at least 25 percent of its 52-week high (the closer to a new high the better)."
> 8. "The relative strength ranking (as reported in Investor's Business Daily) is no less than 70, and preferably in the 80s or 90s …"

**Kata-kata Minervini sendiri** [ASAL-PETIK melalui agregator tweet]
- Rantaian tweet @markminervini: saham mesti memenuhi kesemua lapan syarat untuk dianggap dalam "confirmed stage 2 uptrend". — [buzzchronicles (koleksi tweet)](https://buzzchronicles.com/b/screeners/22604/)
- Senarai ini juga dikaitkan dengan buku *Think & Trade Like a Champion*. — [TradingView TwP Trend Template](https://in.tradingview.com/script/88aL78Qh-TwP-Mark-Minervini-Trend-Template-Criteria/)

**Penterjemahan kuantitatif oleh pelaksana**
- [ASAL-KOD] StockFetcher (dalam komen AgenaTrader):
  - `MA(200) is increasing for 1 month`;
  - `Close divided by 260 day low is above 1.3`;
  - `Close divided by 260 day high is above 0.75`;
  - proksi RS `Relative strength(^SPX,90) is above 1.0`.
  - Kod AgenaTrader sendiri: `close > SMA50 > SMA150 > SMA200 && IsSeriesRising(SMA200) && close/LowestLow(260) > 1.3 && close/HighestHigh(260) > 0.75`.
  - — [AgenaTrader](https://github.com/simonpucher/AgenaTrader/blob/master/Indicator/TrendTemplate_MarkMinervini_Indicator.cs)
- [SEKUNDER] MQL5: SMA200 hari ini > SMA200 20 sesi lalu. ChartMill: penyaring mereka **tidak** memasukkan syarat cerun SMA200. — [MQL5](https://www.mql5.com/en/articles/22790); [ChartMill](https://www.chartmill.com/documentation/stock-screener/fundamental-analysis-investing-strategies/464-Mark-Minervini-Strategy-Think-and-Trade-Like-a-Champion-Part-1)

**VCP [SEKUNDER]**
- "Each contraction must be smaller than the one before it", contohnya ~20% → 10% → 5% atau 25% → 12% → 6%.
- Lazimnya 2–4 kecutan, kadang-kadang 5–6.
- Volum mengecut semasa tarikan semula dan paling kering di sisi kanan; tembusan dijangka dengan volum lebih berat.
- — [LuxAlgo VCP](https://www.luxalgo.com/library/concept/volatility-contraction-pattern/); [Trading Momentum substack](https://tradingmomentum.substack.com/p/the-volatility-contraction-pattern-b57)
- Notasi jejak ChartMill "19W 19/7 4T" = asas 19 minggu, kecutan terbesar 19% hingga terkecil 7%, 4 kecutan. — [ChartMill](https://www.chartmill.com/documentation/stock-screener/fundamental-analysis-investing-strategies/465-Mark-Minervini-Strategy-Think-and-Trade-Like-a-Champion-Trading-Strategy)
- "VCP is not measured by a single formula", jadi pengesan automatik berbeza-beza. — [LuxAlgo](https://www.luxalgo.com/library/concept/volatility-contraction-pattern/)

### Inferences
- **[IN] Pembetulan RP §2:**
  - jadual RP betul tentang angka (30%, 25%, RS ≥ 70);
  - perkataan syarat 3 ialah "at least 1 month (preferably 4–5 months minimum in most cases)", jadi tafsiran ketat "≥ 1 bulan" dan longgar "4–5 bulan" kedua-duanya sah;
  - syarat 7 berbunyi "within at least 25 percent of its 52-week high" (iaitu C ≥ 0.75 × tertinggi 52 minggu).
- **[IN]** Minervini sendiri menamakan lulus 8/8 sebagai "confirmed stage 2 uptrend". Ini menyokong tafsiran bahawa takrif Bullish papan (C > 50 > 150 > 200) ialah subset Peringkat 2 tanpa syarat umur (3), jarak (6–7) dan RS (8).

### Gaps
- Teks VCP dalam *Trade Like a Stock Market Wizard* (bab 10) tidak diperoleh. Bilangan kecutan dan nisbah "separuh" kekal sekunder.
- Laman minervini.com tidak muncul dalam carian.

---

## 3. IBD / O'Neil: follow-through day, ambang mengikut era, distribution day, keadaan pasaran, kiraan peringkat asas

### Takeaway
- **FTD** = hari ke-4 atau kemudian dalam cubaan pulih: satu indeks utama naik dengan peratus ambang, pada volum lebih tinggi daripada sesi sebelumnya. Petikan O'Neil (Goodreads) menyokong "starting on the fourth day … a booming gain on heavier volume than the day before".
- **Ambang mengikut era:** 1% (asal) → 1.7% (IBD menaikkan kerana volatiliti; dilapor Hanna 2008) → kini 1.2% atau 1.25% (sumber sekunder bercanggah; dokumen IBD tidak dapat dibaca).
- **Distribution day** = indeks jatuh ≥ 0.2% dengan volum lebih tinggi. Luput selepas 25 sesi atau apabila indeks naik 5% di atas tutup hari itu. Ini disahkan oleh halaman sokongan MarketSmith (rakan O'Neil).
- **Ujian bebas (Hanna):** kadar kejayaan FTD ≈ 55% (longgar) atau 45% (ketat) sejak 1971, jauh di bawah dakwaan IBD 70–80%.

### Cited Findings
**Takrif FTD**
- [ASAL-PETIK melalui petikan Goodreads] "starting on the fourth day of the attempted rally, look for one of the major average to follow through with a booming gain on heavier volume than the day before". — [Goodreads: How to Make Money in Stocks](https://www.goodreads.com/book/show/72151.How_to_Make_Money_in_Stocks)
- [ASAL-PETIK lemah; OCR edisi lama] Follow-through muncul "anywhere from its third to tenth day", dengan indeks naik "1% or more". — rujukan buku O'Neil edisi awal ([Internet Archive katalog](https://archive.org/details/howtomakemoneyin00mcgr); salinan OCR tidak dapat dibuka)
- [SEKUNDER] Ringkasan buku: FTD terkuat pada hari 4–7. Kadang-kadang hari ke-3 jika kenaikan sangat kuat (1.5–2%). — [Shortform](https://www.shortform.com/pdf/how-to-make-money-in-stocks-pdf-william-j-oneil)

**Ambang mengikut era**
- [SEKUNDER kuat; penyelidik kuantitatif] Rob Hanna (2008): "Investors Business Daily originally stated a Follow Through Day should be a rise of at least 1% … A few years ago this number was changed to 1.7%. Their explanation was that volatility had increased". — [Quantifiable Edges](https://quantifiableedges.com/ibd-follow-through-days-pt-1-are-they-predictive/)
- [SEKUNDER] Dakwaan IBD menggunakan 2% seketika sekitar 2000. — [aistockselection glossary](https://www.aistockselection.com/en/glossary/follow-through-day)
- [SEKUNDER, bercanggah] Ambang semasa:
  - 1.2%: skrip TradingView "Distribution & Follow-Through Day Marker" yang mendakwa mengikut IBD ("the gain must be at least 1.2%; the volume is higher than prior trading day"; distribution "at least −0.2%");
  - 1.25%: LuxAlgo dan penjelas Jepun;
  - 1.5%: satu glosari;
  - 1.6%: lalai satu skrip lain.
  - — [TradingView FTD marker](https://www.tradingview.com/script/mrsKTQdQ-Distribution-Follow-Through-Day-Marker); [LuxAlgo FTD](https://www.luxalgo.com/library/concept/follow-through-day/); [note.com erinaomi](https://note.com/erinaomi/n/nb7d40bb55c5a?hl=en)

**Prestasi FTD [SEKUNDER kuat: ujian Hanna]**
- Kadar kejayaan ≈ 55% sejak 1971 dengan andaian "extremely generous", dan 45% dengan takrif lebih ketat. IBD mendakwa 70–80%.
- Dengan peraturan 1%, setiap rali sejak 1971 didahului FTD. Selepas ambang dinaikkan ke 1.7%, "several substantial rallies occur without FTD's".
- Kejayaan menurun mengikut kedalaman kejatuhan sebelumnya:
  - kejatuhan ≥ 5%: 63.5% (n = 115);
  - kejatuhan ≥ 8%: 54.7% (n = 64);
  - kejatuhan ≥ 12%: 44.4% (n = 36).
- FTD selepas hari ke-10: 7 daripada 8 berjaya (sampel kecil).
- Jika tutup hari ke-3 selepas FTD < tutup FTD, hanya 35% berjaya (12/34).
- — [Quantifiable Edges ringkasan 4 bahagian](https://quantifiableedges.com/follow-through-days-quantified/); [Hari > 10](http://quantifiableedges.blogspot.com/2008/02/are-ibd-follow-through-days-after-day.html); [2012 update](https://quantifiableedges.blogspot.com/2012/06/new-look-at-short-term-strength-after.html)

**Distribution day dan keadaan pasaran**
- [ASAL-PETIK, MarketSmith India, rakan O'Neil] "A distribution day is indicated by a major market index such as the Sensex closing down 0.2% or more on higher volume than the previous day". Hari pengagihan digugurkan jika indeks naik ≥ 5% dari tutup hari itu. — [MarketSmith India support](https://marketsmithindia.com/support); [MarketSmith India: distribution days](https://marketsmithindia.com/post/how-to-track-weakness-in-the-market-distribution-days)
- [SEKUNDER] Versi IBD AS: Nasdaq atau S&P 500 turun ≥ 0.2% dengan volum lebih tinggi; luput selepas 25 sesi atau apabila indeks naik 5% di atas tutup hari itu.
- [SEKUNDER, bercanggah] Status bergerak Confirmed uptrend → Uptrend under pressure → Market in correction apabila kiraan bertambah. Pencetus disebut "four or five" (LuxAlgo) atau "five or six" (sumber lain); ambang rasmi IBD tidak ditemui.
- — [LuxAlgo distribution days](https://www.luxalgo.com/library/concept/distribution-days/)

**Kiraan peringkat asas** [SEKUNDER-rasmi afiliasi; tidak disemak semula dalam sesi ini]
- Peringkat naik secara angka jika pergerakan ≥ 20% dari pivot sebelumnya, dan diset semula apabila paras terendah asas sebelumnya dilanggar. — [MarketSmith India blog](https://blog.marketsmithindia.com/?p=5476) (dipetik dalam RP §2)

### Inferences
- **[IN] Pembetulan RP §2 dan PMN:**
  - "~1.25%" ialah salah satu daripada dua angka semasa yang bersaing (1.2% dan 1.25%);
  - sejarah 1% → (2%?) → 1.7% disokong Hanna;
  - kadar kejayaan "separuh hingga dua pertiga" dalam RP kini disahkan oleh ujian Hanna (45–64% bergantung pada takrif dan kedalaman kejatuhan).
- **[IN]** Untuk saham swing, logik FTD (minimum 4 hari dari paras terendah + hari kenaikan berkuasa dengan volum) ialah templat "pengesahan onset". Bukti Hanna menunjukkan kadar penggera palsu ~45–55%. Mana-mana adaptasi pada saham individu perlu syarat gagal (seperti "paras terendah Hari 1 dilanggar → kiraan semula").
- **[IN]** Hari ke-3 selepas FTD ditutup di bawah tutup FTD menurunkan kejayaan kepada ~35%. Ini sokongan empirikal untuk peraturan "batal onset jika tutup kembali di bawah aras pencetus dalam beberapa sesi" (PMN H5).

### Gaps
- Dokumen IBD semasa (ambang FTD, ambang kiraan "under pressure") tidak dapat dibaca kerana domain disekat untuk carian dan fetch.
- Petikan O'Neil dengan "1.7%" (edisi ke-4, 2009) tidak ditemui.

---

## 4. Wilder ADX/ADXR, jalur 25/20 Kaufman, Elder Impulse dan Triple Screen

### Takeaway
- **Formula ADXR** disahkan melalui kod TA-Lib: ADXR = (ADX_t + ADX_{t−(n−1)})/2.
- **Ambang 25/20:** StockCharts mengaitkannya dengan ADX ("Wilder suggests … ADX above 25 … below 20"). Dakwaan bahawa Wilder memakainya pada **ADXR** hanya disokong sumber sekunder. Teks Wilder 1978 tidak diperoleh, jadi isu ADX lawan ADXR **kekal tidak disahkan**.
- **Jalur Kaufman 25-masuk / 20-keluar** tidak dapat disahkan semula dalam sesi ini.
- **Elder:** skrin pertama asal Triple Screen ialah **cerun histogram MACD mingguan**. Dalam *Come Into My Trading Room* Elder membenarkan **EMA 26 minggu, cerun histogram MACD mingguan, atau kedua-duanya**. "EMA 13 minggu" kurang disokong.
- **Elder Impulse:** EMA13 + histogram MACD(12,26,9); hijau = kedua-duanya naik, merah = kedua-duanya turun, biru = selainnya. Fungsinya penapis ("censorship").

### Cited Findings
**ADX/ADXR**
- [ASAL-KOD] TA-Lib `ta_ADXR.c`: "ADXR[k] = (ADX[k] + ADX[k-(period-1)]) / 2", tempoh lalai 14. — [TA-Lib ta_ADXR.c](https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_ADXR.c)
- [SEKUNDER] LuxAlgo mentakrif ADXR = (ADX hari ini + ADX n tempoh lalu)/2, berbeza sedikit daripada lag n−1 TA-Lib. — [LuxAlgo ADX/DMI](https://www.luxalgo.com/library/concept/adx-dmi-system/)
- [SEKUNDER; tafsiran platform] "Wilder suggests that a strong trend is present when ADX is above 25 and no trend is present when ADX is below 20. There appears to be a gray zone between 20 and 25." — [StockCharts ChartSchool ADX](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/average-directional-index-adx)
- [SEKUNDER] Gerbang ADXR: "use trend-following only when ADXR exceeds 25 … avoid it when ADXR falls below 20". Ada juga dakwaan bahawa ambang 25 diperoleh Wilder daripada pemerhatian carta komoditi 1970-an. — [LuxAlgo ADX/DMI](https://www.luxalgo.com/library/concept/adx-dmi-system/); [MQL5 Meta-Labeling ADX](https://www.mql5.com/en/articles/22754)
- [SEKUNDER] Skrip "ADX w/ Wilder's DI/DX/ADXR/Equilibrium Point" (dipetik RP) mengaitkan 25/20 dengan ADXR dan menerangkan Extreme Point Rule. — [TradingView](https://de.tradingview.com/script/R3YRg9EF-adx-w-wilders-di-di-dx-adxr-equilibrium-point)
- [ASAL-KOD] TradingView Technical Ratings v3 menggunakan "adx > 20 and adx > adx[1] and diP > diN" sebagai beli (lihat §5). Ini contoh platform yang memakai **20 + ADX naik**, bukan 25.
- Buku: *New Concepts in Technical Trading Systems* (Trend Research, 1978); bahagian Directional Movement bermula sekitar hlm. 45. — [Google Books](https://books.google.com.ni/books/about/New_Concepts_in_Technical_Trading_System.html?id=WesJAQAAMAAJ&redir_esc=y)

**Kaufman [TIDAK DISAHKAN semula]**
- Carian tidak menemui teks *Trading Systems and Methods* atau artikel Kaufman di traders.com. Sumber am hanya menyebut "rise from below 20 to above 25 as the potential beginning of a new trend" dan zon neutral 20–25. — [ChartGuys ADX](https://www.chartguys.com/articles/adx-indicator); rujukan RP kepada [Traders.com art=8229](https://technical.traders.com/tradersonline/display.asp?art=8229) tidak dapat disemak.

**Elder Impulse [SEKUNDER konsisten; dokumen platform]**
- Bar hijau apabila EMA 13 hari dan histogram MACD kedua-duanya naik; merah apabila kedua-duanya jatuh; biru apabila syarat hijau/merah tidak dipenuhi. MACD-H berasaskan MACD(12,26,9). — [StockCharts ChartSchool Elder Impulse](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/elder-impulse-system); [StockDoctor help](https://help.stockdoctor.com.au/hc/en-us/articles/360000099256-Elder-Impulse-System)
- Penapisan: hijau melarang short, merah melarang beli, biru membenarkan kedua-duanya atau berdiri di tepi. Keluar apabila salah satu penunjuk berpusing turun (histogram biasanya dahulu). — [LuxAlgo Elder Impulse](https://www.luxalgo.com/library/concept/elder-impulse-system/); [QuantifiedStrategies](https://www.quantifiedstrategies.com/elder-impulse-system/)

**Elder Triple Screen: skrin pertama**
- [SEKUNDER] "Dr Alexander Elder, in Trading for a Living, uses an MACD Histogram as the first screen". — [Incredible Charts](https://www.incrediblecharts.com/technical/macd_and_histogram.php)
- [SEKUNDER-petik buku] Blog 2012 yang memetik *Come Into My Trading Room*: carta mingguan boleh menggunakan EMA 26 minggu, cerun histogram MACD mingguan, atau kedua-duanya. — [stock-market-observations.com 2012](https://stock-market-observations.com/2012/01/30/elder-impulse-system-013012/)
- [SEKUNDER, bercanggah] Sumber lain menyebut cerun EMA 13 minggu sebagai alternatif, dan menegaskan bahawa yang dikira ialah **cerun** histogram (minggu ini lawan minggu lalu), bukan tanda (+/−). — [TakeProfit](https://takeprofitapp.com/en/learn/triple-screen-trading-system); [therighttrader](https://therighttrader.com/learn/trend-analysis/triple-screen-trading-system)

### Inferences
- **[IN] Pembetulan RP §3/NAT:**
  - skrin pertama Elder yang paling disokong ialah **cerun histogram MACD mingguan**, dengan **EMA 26 minggu** sebagai alternatif atau tambahan (2002); "EMA 13 minggu" dalam NAT patut ditanda lemah;
  - isu ADX lawan ADXR bagi 25/20 kekal terbuka;
  - formula ADXR disahkan.
- **[IN]** Untuk papan: penapis ADX bukan penentu arah. Jika digunakan, versi TradingView (ADX > 20 dan naik) dan versi StockCharts (25/20 dengan zon kelabu) kedua-duanya didokumen. Pilihan perlu diuji, bukan dipilih kerana "Wilder".

### Gaps
- Teks Wilder 1978 (sama ada 25/20 untuk ADX atau ADXR) dan Kaufman tidak diperoleh. Arkib Internet disekat.
- Laman elder.com tidak muncul dalam carian.

---

## 5. Label platform: TradingView, Barchart, StockCharts (SCTR, Trend Composite), Trading Central, moomoo, SST

### Takeaway
- **TradingView Technical Ratings** kini disahkan pada tahap kod melalui port berlesen MPL-2.0 pustaka rasmi `TechnicalRating` v3 (2024-11-29). Strukturnya:
  - 15 penunjuk kumpulan MA (12 SMA/EMA, HMA9, VWMA20 dan Ichimoku), setiap satu `sign(close − MA)`;
  - 11 oscillator dengan peraturan kebanyakannya kontrarian;
  - purata kumpulan, kemudian (MA + Osc)/2, kemudian jalur ±0.1/±0.5.
- **Barchart Opinion:** 13 penunjuk dengan purata keseluruhan dalam %, kekuatan 7 tahap (Maximum…Minimum) dan arah 3 hari. Petikan "% → Weak/Strong Buy" **tidak** didokumenkan dan kekal tidak disahkan.
- **SCTR:** pemberat 30/30/15/15/5/5 disahkan (EMA dalam versi semasa, SMA dalam arkib 2014).
- **Trend Composite Hill:** lima komponen 125 hari disahkan, termasuk "TIP Moving Average Trend (125,5)".
- **moomoo:** 15 penunjuk dengan kiraan bullish/bearish; ambang tidak diterbitkan.
- **SST:** enum rasmi mempunyai **6 nilai** (Breakout, Uptrend, Constructive, Neutral, Downtrend, Unknown). Peraturan yang diperhatikan (23 saham) **membetulkan** NAT §2.10 (lihat §8).

### Cited Findings
**TradingView Technical Ratings** [ASAL-KOD] — [GitHub all-in0/obrii-tv-rules (port TechnicalRating v3, MPL-2.0)](https://github.com/all-in0/obrii-tv-rules); [TradingView TechnicalRating library](https://www.tradingview.com/script/jDWyb5PG-TechnicalRating/); [python-tradingview-ta technicals.py](https://github.com/brian-the-dev/python-tradingview-ta/blob/main/tradingview_ta/technicals.py)
- **Kumpulan MA:** setiap MA `math.sign(src - ma)`.
- **Ichimoku:** beli jika `lead1[26] > lead2[26] and base > lead1[26] and con > base and close > con`, jual sebaliknya.
- **Oscillator** (beli / jual):

| Penunjuk | Beli | Jual |
|---|---|---|
| RSI(14) | `rsi < 30 and rsi[1] < rsi` | `rsi > 70 and rsi[1] > rsi` |
| Stoch(14,3,3) | `k<20 and d<20 and k>d` | `k>80 and d>80 and k<d` |
| CCI(20) | `cci < -100 and cci > cci[1]` | `cci > 100 and cci < cci[1]` |
| ADX(14,14) | `adx > 20 and adx > adx[1] and diP > diN` | `adx > 20 and adx > adx[1] and diP < diN` |
| AO | silang 0, atau "saucer" | cerminan |
| Momentum(10) | `mom > mom[1]` | `mom < mom[1]` |
| MACD(12,26,9) | `macd > signal` | `macd < signal` |
| StochRSI(14,14,3,3) | hanya jika `close < EMA50` dan `k,d < 20 and k > d` | hanya jika `close > EMA50` dan `k,d > 80 and k < d` |
| Williams %R(14) | `wr < -80 and wr > wr[1]` | `wr > -20 and wr < wr[1]` |
| Bull Bear Power | hanya jika aliran naik (`close > EMA50`) dan `bearPower < 0` serta naik | hanya jika aliran turun dan `bullPower > 0` serta turun |
| Ultimate Osc(7,14,28) | `uo > 70` | `uo < 30` |

- **Pengiraan dan label:**
  - setiap kumpulan = purata (`array.avg`); keseluruhan = `(ratingMA + ratingOther) / 2`;
  - `ratingStatus()`: > 0.5 Strong Buy; > 0.1 Buy; [−0.1, 0.1] Neutral; < −0.1 Sell; < −0.5 Strong Sell.
- **Versi lebih lama** (python-tradingview-ta, ditulis semula daripada bundle JS TradingView) sedikit berbeza:
  - ADX beli = `adx > 20` dan +DI **melintas** −DI (`adxpdi1 < adxndi1 and adxpdi > adxndi`);
  - Stoch memerlukan silang K/D;
  - jalur skor sama: Strong Sell [−1, −0.5), Sell [−0.5, −0.1), Neutral [−0.1, 0.1], Buy (0.1, 0.5], Strong Buy (0.5, 1].

**Barchart Opinion** [ASAL-PETIK melalui petikan halaman Barchart]
- "The Opinions takes up to 5 years' worth of historical data and runs these prices through thirteen different technical indicators. After each calculation, the program assigns a buy, sell or hold value for each study."
- "Overall Average Signal calculated from all 13 indicators", contohnya "64% Buy", "72% Sell". 100% Buy/Sell bermakna semua 13 sepakat. Setiap Opinion memerlukan ≥ 201 hari dagangan.
- "Signal Strength is a long-term measurement of the historical strength of the Signal, while Signal Direction is a short-term (3-Day) measurement of the movement of the Signal."
- Overall Opinion Strength: Maximum, Strong, Good, Average, Soft, Weak, Minimum.
- Halaman memaparkan Opinion sesi sebelumnya, 1 minggu lalu dan 1 bulan lalu; dikemas kini setiap 20 minit.
- Bullish hold = isyarat sedang menuju konfigurasi beli.
- — [Barchart AAPL Opinion](https://www.barchart.com/stocks/quotes/aapl/opinion); [Barchart $NASX Opinion](https://www.barchart.com/stocks/quotes/$NASX/opinion); [100% Buy Signal](https://www.barchart.com/stocks/signals/100-percent-buys); [Barchart getSignal API](https://www.barchart.com/ondemand/api/getSignal)
- **Set penunjuk:**
  - halaman semasa menyenaraikan "20 Day Moving Average vs Price", "20 Day Bollinger Bands" (pendek), "40 Day Commodity Channel Index", "50 Day Parabolic Time/Price" (sederhana);
  - halaman saham semasa menggunakan "20 - 50 Day MA Crossover", manakala laman legacy menggunakan "20 - 50 Day MACD Oscillator";
  - "7 Day Average Directional Indicator" dan "10 - 8 Day Moving Average Hilo Channel" ialah penunjuk pendek; Trend Seeker® ialah penunjuk komposit.
  - — [Barchart AAPL opinion-legacy](https://www.barchart.com/stocks/quotes/AAPL/opinion-legacy/20-Day-Bollinger-Bands/strategy-charts); [Barchart getSignal API](https://www.barchart.com/ondemand/api/getSignal)
- **Trend Seeker** [ASAL-PETIK, bahan pendidikan Barchart]:
  - gabungan "price velocity, market momentum, and volatility";
  - isyarat masuk apabila harga menembusi titik trend bertentangan;
  - selepas keluar, sistem "resets and assumes a neutral trend for at least one day";
  - satu titik di bawah harga = trend bullish; dua titik (atas dan bawah) = neutral/hold;
  - penyaring "Made New Trend Seeker® Signal" wujud.
  - — [Barchart Trend Seeker PDF](https://www.barchart.com/media/education/pdf/Unlock%20the%20Power%20of%20Trend%20Seeker%20-%20The%20Ultimate%20Trend%20Trading%20Strategy.pdf); [Barchart news](https://www.barchart.com/story/news/17361808/simplify-your-screening-with-the-power-of-trendseeker)

**StockCharts SCTR**
- [ASAL-PETIK melalui ChartSchool] Pemberat:
  - jangka panjang: % atas/bawah EMA 200 hari (30%) dan ROC 125 hari (30%);
  - jangka sederhana: % dari EMA 50 hari (15%) dan ROC 20 hari (15%);
  - jangka pendek: cerun 3 hari histogram PPO(12,26,9) dibahagi tiga (5%) dan RSI 14 (5%).
  - Contoh: "A stock 15% above its 200-day moving average contributes 4.5 points (15 x .30)".
  - Arkib ChartSchool 2014 menggunakan SMA 200, bukan EMA.
  - — [StockCharts ChartSchool SCTR](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/stockcharts-technical-rank-sctr); [arkib 2014 (PDF)](https://community.portfolio123.com/uploads/short-url/cAyPPbhAQJ76A89fIQ40X0Xn4p6.pdf)
- [ASAL-KOD; replikasi 2015] `LT_WEIGHT = .30, MD_WEIGHT = .15, SH_WEIGHT = .05`, dengan SMA200/SMA50 mengikut versi lama. — [GitHub hwrdprkns/ThinkOrSwim SCTRSTUDY.ts](https://github.com/hwrdprkns/ThinkOrSwim/blob/master/SCTRSTUDY.ts)
- [SEKUNDER bercanggah, ditolak] brokerspecs.com memberi 20%/10% untuk blok jangka panjang, bercanggah dengan StockCharts. — [brokerspecs](https://brokerspecs.com/education/stockcharts)

**Trend Composite (Arthur Hill, TrendInvestorPro)** [ASAL-PETIK melalui halaman bantuan StockCharts]
- "TIP Moving Average Trend, TIP CCI Close, Bollinger Bands, Keltner Channels, and TIP StochClose". Setiap satu +1 (isyarat bull) atau −1 (bear); komposit +5 hingga −5, "always an odd number".
- Butiran komponen:
  - Moving Average Trend (125,5): SMA 125 dengan ROC 5 tempoh; melintas atas sifar = bull, bawah sifar = bear;
  - Bollinger (125,1);
  - Keltner (125,125,2);
  - StochClose (125,5): > 60 bullish, < 40 bearish;
  - CCI Close (125).
  - Isyarat jalur: tutup di atas jalur atas = bull, tutup di bawah jalur bawah = bear.
- — [StockCharts help: Trend Investor Pro Indicator Edge](https://help.stockcharts.com/charts-and-tools/stockchartsacp/stockchartsacp-plug-ins/trend-investor-pro-indicator-edge); [StockCharts ChartWatchers 2022](https://articles.stockcharts.com/article/articles-chartwatchers-2022-05-a-key-factor-in-the-trading-pu-608/)
- [SEKUNDER] Hill lebih suka 200 tempoh bagi saham ("fewer whipsaws and longer trends"). — [StockCharts Arthur Hill](https://articles.stockcharts.com/article/articles-arthurhill-2022-11-trendfollowers-get-the-whip-wh-325/)

**Trading Central** [SEKUNDER, bercanggah]
- Tiga ufuk (pendek, pertengahan, panjang) disahkan oleh halaman produk. Julat "2–6 minggu / 6–39 minggu / 9 bulan+" hanya ditemui dalam isu GitHub pihak ketiga dan RP. Profil Fidelity lama: "up to 3 weeks" / "up to 3 months". — [Trading Central Technical Events](https://investor.tradingcentral.com/about-us/technical-events); [GitHub issue investor-dashboard #191](https://github.com/ram290476/investor-dashboard/issues/191); [Fidelity](https://research2.fidelity.com/fidelity/research/reports/release2/Research/TradingCentral.asp)
- IBKR: tab menunjukkan "Short-term, Intermediate-term and Long-term interpretation"; kotak akhir mencadangkan "Stop Price … based on the balance of recent bullish and bearish patterns and signals". — [IBKR Campus](https://www.interactivebrokers.com/campus/trading-lessons/discover-tool-technical-insight/)

**moomoo Technical Sentiment** [ASAL-PETIK melalui petikan halaman bantuan]
- Sentimen keseluruhan (bullish, bearish atau neutral) "based on the number of bullish and bearish signals".
- Isyarat datang daripada "15 common oversold and overbought indicators and technical patterns".
- Kerangka masa: Daily, 1m dan 60m. Kelabu = "unclear trend".
- Penunjuk jenis corak (MACD, KDJ, BOLL, MA) dinilai melalui silang atau susunan; penunjuk angka (RSI, CCI, BIAS) melalui ambang overbought/oversold.
- Ambang neutral dan pemberat tidak diterbitkan.
- — [moomoo manual Technical Sentiment](https://www.moomoo.com/us/manual/topic-14-60); [moomoo learn](https://www.moomoo.com/us/learn/what-is-technical-indicator-sentiment-feature); [moomoo AU help](https://www.moomoo.com/au/support/topic3_601)

**SST Terminal** [ASAL-PETIK skema alat; pemerhatian langsung]
- Skema `screen_stocks` menyenaraikan `trend` enum: "Breakout", "Uptrend", "Constructive", "Neutral", "Downtrend", "Unknown". Tiada dokumentasi takrif.
- Peraturan yang diperhatikan dan jadual sampel ada dalam §8.

### Inferences
- **[IN] Pembetulan NAT §2.1:**
  - ADX dalam penarafan TradingView kini (v3) = ADX > 20 **dan naik** + susunan DI, bukan silang;
  - StochRSI dan Bull Bear Power **dikondisikan oleh trend EMA50**;
  - Ultimate Oscillator > 70 = **beli** (ikut trend), bertentangan dengan RSI > 70 = jual. Ini menambah sebab untuk tidak menyamakan "Strong Buy" dengan "trend kuat".
- **[IN] Pembetulan RP §4/NAT §2.3:** label tujuh tahap "Strong/Weak Buy" dengan ambang 33%/66% tidak dapat disahkan. Yang **didokumenkan** Barchart ialah:
  - (a) % purata 13 penunjuk;
  - (b) kekuatan 7 tahap berbanding sejarah sendiri;
  - (c) arah 3 hari;
  - (d) syot kilat semalam/minggu lalu/bulan lalu.
  - Penamaan "20 − 50 Day MA Crossover" (semasa) lawan "MACD Oscillator" (legacy) menunjukkan set semasa ≠ legacy.
- **[IN]** Hill dan Barchart Trend Seeker ialah dua contoh terdokumen reka bentuk berbeza:
  - Hill: ganjil, tiada neutral;
  - Trend Seeker: SAR dengan **neutral sekurang-kurangnya 1 hari selepas keluar**, iaitu tempoh bertenang selepas isyarat keluar sebelum isyarat arah baharu.

### Gaps
- Pemetaan % → label Barchart dan senarai penuh 13 penunjuk semasa tidak dapat dibaca terus.
- Julat ufuk Trading Central tidak disahkan daripada dokumen rasmi.
- moomoo tidak menerbitkan senarai 15 penunjuk atau ambang neutral dalam petikan yang ditemui.
- SST tidak mendokumenkan takrif label.

---

## 6. Bulkowski: kadar kegagalan tembusan mengikut era dan dapatan volum

### Takeaway
- Kadar "gagal 10%" bagi tembusan menaik meningkat daripada **14% (1990-an) kepada 28% (2003–2007)**, dengan siri tahunan dari 11% (1991) memuncak 44% (2007), dan 32% pada 2008. Ini disahkan daripada halaman kajian Bulkowski.
- **Dapatan volum bercanggah di dalam laman Bulkowski sendiri:**
  - "Volume Study": volum tembusan tinggi meningkatkan prestasi sedikit (+1.8 mata peratusan), tetapi "failures triple";
  - halaman lain: kegagalan menurun apabila volum hari tembusan meningkat (tembusan menaik);
  - trend volum meningkat 3 minggu sebelum tembusan mengurangkan kegagalan ~31%.

### Cited Findings
**Kadar kegagalan** [ASAL-PETIK melalui petikan thepatternsite]
- Kajian ~14,000 corak, 1991–2008. Bagi tembusan menaik, kadar gagal-naik-10%: "the 1990s rate was 14%, and during 2003 to 2007 it had doubled to 28%".
- Siri tahunan: "1991 at 11%, peaking at 44% in 2007", turun ke 32% pada 2008.
- Tembusan menurun: 26% (1990-an) → 49% (2003–2007).
- — [thepatternsite: Failure Rate Study](https://thepatternsite.com/FailureRates.html)
- **Takrif:**
  - "breakeven failure rate" = corak yang gagal naik/turun sekurang-kurangnya 5%;
  - pasaran bull = semua tempoh selain Mac 2000–Okt 2002 dan Okt 2007–Mac 2009.
  - — [thepatternsite: Glossary](https://www.thepatternsite.com/glossary.html)

**Volum** [ASAL-PETIK; bercanggah dalaman]
- "performance gets a boost from a high volume breakout, but failures triple". Tembusan menaik dengan volum atas purata menaikkan prestasi "by just 1.8 percentage points".
- Volum "heavy" = melebihi purata volum 30 hari kalendar.
- Untuk tembusan menaik, throwback berlaku 74% apabila volum tembusan atas purata.
- — [thepatternsite: Volume Study](https://thepatternsite.com/VolumeStudy.html)
- "For upward breakouts, as breakout day volume increases, the number of stocks failing to rise at least 10% after the breakout drops."
- Memilih corak dengan trend volum meningkat dalam 3 minggu sebelum tembusan "could cut failures by 31%, on average".
- — [thepatternsite: Bulkowski on Volume](https://thepatternsite.com/Volume.html)
- Ringkasan "Study of Studies": volum tembusan atas purata membantu dalam 79% kajian (menaik) dan 67% (menurun). — [thepatternsite: Study of Studies](https://thepatternsite.com/studystudy.html)

### Inferences
- **[IN] Pengesahan PMN §1:** angka 14% → 28% disahkan, dengan konteks 10% = gagal naik ≥ 10% (bukan 5%).
- **[IN] Pembetulan PMN:** dapatan "14% gagal dengan volum atas purata lawan 5% dengan volum bawah purata" **tidak** dapat disahkan semula. Laman Bulkowski sendiri memberi isyarat bercampur (failures triple lawan failures drop). Kesimpulan selamat: volum tembusan tinggi memberi kesan kecil kepada purata prestasi. Trend volum 3 minggu sebelum tembusan lebih berguna daripada volum satu hari.
- **[IN]** Throwback 74% selepas tembusan bervolum tinggi bermakna syarat gagal onset yang terlalu ketat (cth. "tutup di bawah aras tembusan = gagal") akan menandakan banyak onset sah sebagai gagal. Penimbal ATR (PMN H5: C < aras − 0.5×ATR) lebih munasabah.

### Gaps
- Jadual penuh kajian volum (kadar gagal mengikut kuintil volum) tidak dapat dibaca.
- Data selepas 2008 tidak diliputi kajian kadar kegagalan.

---

## 7. Platform yang mendokumenkan "hari dalam trend" / tarikh mula trend

### Takeaway
- Tiada platform arus perdana (TradingView Technical Ratings, Barchart, StockCharts, moomoo, SST, Trading Central) yang ditemui mendokumenkan medan "hari dalam trend" atau "tarikh mula" bagi **label trend saham**.
- Yang **didokumenkan** ialah:
  - (a) syot kilat sejarah label (Barchart: semalam/1 minggu/1 bulan);
  - (b) arah perubahan 3 hari (Barchart);
  - (c) penapis "isyarat baharu" (Barchart "Made New Trend Seeker Signal");
  - (d) kiraan IBD (hari cubaan pulih, hari pengagihan dalam 25 sesi);
  - (e) penunjuk berasaskan masa: Aroon (Chande), yang mengukur bilangan tempoh sejak paras tertinggi/terendah n tempoh.
- Hanya skrip komuniti TradingView (cth. "Power Trend Detector Pro") memaparkan "days in trend" dan "% change since it started".

### Cited Findings
- [ASAL-PETIK] Barchart memaparkan Opinion sesi sebelumnya, 1 minggu lalu dan 1 bulan lalu, serta Signal Direction "(3-Day)". — [Barchart AAPL Opinion](https://www.barchart.com/stocks/quotes/aapl/opinion)
- [ASAL-PETIK] Penapis "Made New Trend Seeker® Signal" untuk saham yang baru menjana isyarat baharu. Trend Seeker kembali neutral sekurang-kurangnya satu hari selepas keluar. — [Barchart Trend Seeker PDF](https://www.barchart.com/media/education/pdf/Unlock%20the%20Power%20of%20Trend%20Seeker%20-%20The%20Ultimate%20Trend%20Trading%20Strategy.pdf)
- [SEKUNDER konsisten] **Aroon** (Chande):
  - "measure the number of periods since price recorded an x-day high or low";
  - Aroon-Up = [(n − tempoh sejak tertinggi tertinggi dalam n)/n] × 100;
  - tetapan Chande lazim 25;
  - Aroon-Up kekal 70–100 dengan Aroon-Down 0–30 = "a new uptrend is underway".
  - — [Fidelity: Aroon](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/aroon-indicator); [TTR R docs](https://search.r-project.org/CRAN/refmans/TTR/html/aroon.html)
- [SEKUNDER] Skrip komuniti "Power Trend Detector Pro [LevelUp]": jadual statistik "days in the trend, % change since it started, % off the recent high"; boleh disaring dalam Pine Screener. — [TradingView](https://www.tradingview.com/script/CzyVIdMM-Power-Trend-Detector-Pro-LevelUp/)
- [ASAL-KOD] Pelaksanaan Weinstein shravanmateti melabel "S# start" dan "S# end" pada carta dan menyimpan `stage_start` (indeks bar permulaan peringkat). Ini model "tarikh mula keadaan" dalam mesin keadaan. — [GitHub shravanmateti](https://github.com/shravanmateti/weinstein-stage-analysis)
- [PEMERHATIAN] SST `technical_analysis` tidak memulangkan medan tarikh mula atau tempoh (§8).

### Inferences
- **[IN]** Tiada konvensyen platform yang boleh disalin untuk "sejak bila". Papan perlu mentakrifkannya sendiri. Dua model terdokumen paling dekat:
  - (a) **mesin keadaan dengan `stage_start`** (pelaksanaan Weinstein): tarikh = bar keadaan bertukar selepas pengesahan;
  - (b) **Aroon / masa sejak ekstrem**: umur = sesi sejak tertinggi n hari terakhir. Ini memberi "kesegaran" trend tanpa label baharu.
- **[IN]** Paparan Barchart (semalam / minggu lalu / bulan lalu) ialah cara murah untuk menunjukkan perubahan tanpa tarikh tepat. Contoh: "Bullish (minggu lalu: Neutral)".

### Gaps
- Rujukan rasmi Pine `ta.barssince` tidak dapat dibaca (domain TradingView disekat).
- Jadual isyarat TrendInvestorPro (sama ada memaparkan tarikh isyarat) tidak ditemui.

---

## 8. SST Terminal: bagaimana SST melabel trend (pemerhatian langsung, 23 saham) dan sama ada peraturannya didokumenkan

### Takeaway
- SST **tidak mendokumenkan** peraturan label. Enum skema mempunyai 6 nilai.
- Pemerhatian 23 saham AS (17 dalam sesi ini, 6 daripada NAT) konsisten **100%** dengan peraturan ini:
  - **Uptrend** ⇔ `trendTemplate = true`;
  - **Constructive** ⇔ C > SMA50 **dan** C > SMA200 tetapi templat gagal (susunan MA **tidak** diperlukan);
  - **Neutral** ⇔ C di antara SMA50 dan SMA200;
  - **Downtrend** ⇔ C < SMA50 **dan** C < SMA200 (susunan MA tidak diperlukan).
- Peraturan ini **membetulkan** NAT §2.10, yang mendakwa Uptrend ⇔ SMA20 > SMA50 dan Downtrend ⇔ C < SMA50 < SMA200.
- `explain_stock` menerangkan Uptrend sebagai "strong uptrend", Downtrend sebagai "downtrend", dan **kedua-dua Constructive dan Neutral** sebagai "neutral/consolidation phase".

### Cited Findings
[PEMERHATIAN LANGSUNG, `mcp__SST_Terminal__technical_analysis` dan `screen_stocks`, 23 Okt 2026 03:31–03:39 UTC; tt = `breakoutStatus.trendTemplate`; Y = ya, T = tidak]

| Ticker | C | SMA20 | SMA50 | SMA200 | C>50 | C>200 | 50>200 | 20>50 | tt | Label SST |
|---|---|---|---|---|---|---|---|---|---|---|
| AAPL | 348.22 | 338.57 | 328.62 | 293.98 | Y | Y | Y | Y | true | Uptrend |
| CRM | 250.29 | 234.80 | 234.04 | 198.75 | Y | Y | Y | Y | true | Uptrend |
| LSPD | 11.21 | 10.37 | 10.26 | 9.87 | Y | Y | Y | Y | true | Uptrend |
| MASI | 179.95 | 178.78 | 178.55 | 155.90 | Y | Y | Y | Y | true | Uptrend (rs = null) |
| MRK | 147.24 | 145.37 | 146.45 | 125.68 | Y | Y | Y | T | false | Constructive |
| **PFE** | 30.42 | 28.72 | 28.23 | 26.66 | Y | Y | Y | **Y** | false | **Constructive** |
| ADBE | 270.55 | 242.65 | 255.92 | 252.61 | Y | Y | Y | T | false | Constructive |
| **CWST** | 96.89 | 84.79 | 88.50 | 90.30 | Y | Y | **T** | T | false | **Constructive** |
| NVDA | 212.21 | 226.25 | 222.77 | 203.56 | T | Y | Y | Y | false | Neutral |
| HRMY | 36.03 | 38.85 | 39.86 | 34.68 | T | Y | Y | T | false | Neutral |
| NKE | 38.32 | 35.80 | 37.25 | 46.87 | Y | T | T | T | false | Neutral |
| LEN | 84.45 | 78.38 | 81.27 | 92.18 | Y | T | T | T | false | Neutral |
| GSK | 51.21 | 48.24 | 49.56 | 52.36 | Y | T | T | T | false | Neutral |
| LULU | 104.06 | 96.43 | 104.65 | 136.90 | T | T | T | T | false | Downtrend |
| **INTC** | 85.49 | 105.89 | 102.46 | 85.59 | T | T | **Y** | Y | false | **Downtrend** |
| LRCX | 230.15 | 304.19 | 304.53 | 283.29 | T | T | Y | T | false | Downtrend |
| BLD | 339.06 | 404.97 | 419.35 | 427.83 | T | T | T | T | false | Downtrend |

- Sampel NAT (22–23 Okt) juga konsisten: MSFT dan LLY (tt true) = Uptrend; JNJ (C > 50, C > 200, tt false) = Constructive; AMD (C < 50, C > 200) = Neutral; PEP dan TSLA (C > 50, C < 200) = Neutral.
- **Kes penentu:**
  - **PFE** mempunyai susunan penuh C > SMA20 > SMA50 > SMA200 dan dekat paras tertinggi 52 minggu, tetapi tt = false, jadi Constructive. SMA20 > SMA50 bukan syarat Uptrend.
  - **CWST** (SMA50 < SMA200) tetap Constructive. Susunan MA tidak diperlukan untuk Constructive.
  - **INTC** (SMA50 > SMA200 tetapi C di bawah kedua-duanya) ialah Downtrend. Susunan MA tidak diperlukan untuk Downtrend.
  - **MASI** (rs = null) tetap tt = true / Uptrend. Templat SST mungkin tidak mensyaratkan RS, atau menganggap null sebagai lulus.
- `screen_stocks trend=Breakout` (AS) memulangkan 0 baris. Takrif "Breakout" (mungkin berkaitan `highVolumeBreakout`) tidak dapat diperhatikan.
- Teks `explain_stock`:
  - AAPL: "the stock is in a strong uptrend";
  - LULU: "the stock is in a downtrend", dengan risiko "Price trading below the 200-day moving average, signaling … a prevailing downtrend";
  - MRK (Constructive) dan NVDA (Neutral): kedua-duanya "the stock is in a neutral/consolidation phase".
- **Kaveat kualiti data SST:** `explain_stock` LULU menyatakan "Revenue growth of 2032.5%" dan "RS score of 7", bercanggah dengan `rs` 23.32 dalam `technical_analysis`. Medan teks SST tidak boleh dipercayai tanpa semakan.

### Inferences
- **[IN] SST ialah label 4 aras** (selain Breakout/Unknown) berpaksi **kedudukan harga berbanding SMA50 dan SMA200**, dengan Uptrend = lulus templat Minervini versi SST:
  - di atas kedua-duanya = sihat (Uptrend jika templat lulus, jika tidak Constructive);
  - di antara = Neutral;
  - di bawah kedua-duanya = Downtrend.
- **[IN] Perbandingan dengan takrif papan** (Bullish = C > SMA50 > SMA150 > SMA200):
  - Bullish papan ≈ "Constructive dengan susunan MA" + sebahagian Uptrend SST;
  - Bearish papan (susunan terbalik penuh) lebih ketat daripada Downtrend SST (cukup C di bawah SMA50 dan SMA200).
  - Contoh: INTC dan LRCX = Downtrend SST tetapi Neutral di papan.
- **[IN]** Peraturan SST "harga lawan dua MA" bertukar lebih cepat daripada susunan MA penuh. Ia memberi Downtrend lebih awal selepas kejatuhan tajam (INTC: C −16.6% di bawah SMA50, masih SMA50 > SMA200). Ini satu reka bentuk yang boleh diuji sebagai pilihan "Bearish awal".

### Gaps
- Komponen tepat `trendTemplate` SST tidak diketahui. PFE gagal walaupun lulus semua syarat MA yang kelihatan dan RS 78.9; kemungkinan syarat 3 (cerun SMA200) atau 6 (30% atas paras terendah), tetapi data tidak cukup untuk memastikan.
- Takrif "Breakout" dan "Unknown" tidak diperhatikan.
- Sampel 23 saham, satu hari. Peraturan disimpulkan, bukan didokumenkan.

---

## 9. Jadual peraturan disahkan (ringkasan untuk penulis laporan)

### Takeaway
Jadual di bawah merumus status pengesahan setiap peraturan selepas sesi ini. Lajur "Status" menggunakan label pemanggil.

### Cited Findings
| # | Rangka / platform | Peraturan | Status | Sumber utama |
|---|---|---|---|---|
| 1 | Weinstein | 4 peringkat ditentukan oleh cerun MA 30 minggu + kedudukan harga; Peringkat 1/3 sama bentuk | [SEKUNDER] konsisten | [LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/); [MQL5](https://www.mql5.com/en/articles/22746) |
| 2 | Weinstein | Ambang angka "MA rata" | [TIDAK DISAHKAN] sebagai Weinstein; pelaksana ±0.5%/4 mgg atau ±2%/4 mgg | [GitHub shravanmateti](https://github.com/shravanmateti/weinstein-stage-analysis) |
| 3 | Weinstein | Volum tembusan ≥ 2× (lonjakan 1 minggu lawan purata 4 minggu; atau timbunan 3–4 minggu ≥ 2×) + minggu tembusan > minggu sebelum | [SEKUNDER kuat] (Bulkowski uji buku); dipertikai Kagels | [thepatternsite](https://thepatternsite.com/TradingWeinstein.html); [Kagels](https://kagels-trading.com/blog/stage-analysis/) |
| 4 | Weinstein | ≥ 1.5× | Bukan Weinstein (pengarang lain) | [edgestacker](https://www.edgestacker.com/tools/library/scans/weinstein/stage-2-breakout/) |
| 5 | Weinstein | Pecahan Peringkat 4 tidak semestinya perlu volum besar ("fall of their own weight") | [ASAL-PETIK] melalui salinan tidak rasmi; perlu semak edisi | Weinstein 1988 ([Goodreads](https://www.goodreads.com/book/show/116948.Secrets_For_Profiting_in_Bull_and_Bear_Markets)) |
| 6 | Weinstein | RS = harga saham ÷ purata pasaran | [ASAL-PETIK] melalui stageanalysis.net (hlm. 18) | [stageanalysis.net](https://www.stageanalysis.net/blog/4266/how-to-create-the-mansfield-relative-performance-indicator) |
| 7 | Weinstein | "RS Mansfield > 0" sebagai syarat beli keras | [TIDAK DISAHKAN] (tambahan pengamal) | — |
| 8 | Weinstein → harian | 30 mgg ≈ 150 hari; 10/30/40 mgg ≈ 50/150/200 hari | [ASAL-KOD] pelaksana + teks Minervini | [GitHub rosskevin](https://github.com/rosskevin/pine-scripts) |
| 9 | Weinstein (empirikal) | Peringkat 1 ≈ 3 (t = −0.5); Peringkat 2 +2.3%/thn (t = 2.7); Sharpe sama penapis MA | [SEKUNDER-akademik] praterbit | [SSRN 7429238](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7429238) |
| 10 | Minervini | 8 syarat; SMA200 naik "at least 1 month (preferably 4–5 months minimum in most cases)"; ≥ 30% atas paras terendah 52 mgg; "within at least 25 percent" dari tertinggi; RS IBD ≥ 70 (80–90 lebih baik) | [ASAL-PETIK] melalui salinan teks (3 sumber bebas) | [AgenaTrader](https://github.com/simonpucher/AgenaTrader/blob/master/Indicator/TrendTemplate_MarkMinervini_Indicator.cs); [ProRealCode](https://www.prorealcode.com/prorealtime-market-screeners/trend-template-mark-minervini/) |
| 11 | Minervini | Lulus 8/8 = "confirmed stage 2 uptrend" | [ASAL-PETIK] melalui agregator tweet | [buzzchronicles](https://buzzchronicles.com/b/screeners/22604/) |
| 12 | Minervini | VCP: 2–6 kecutan (lazim 2–4) mengecil, volum mengering | [SEKUNDER] | [LuxAlgo](https://www.luxalgo.com/library/concept/volatility-contraction-pattern/) |
| 13 | IBD | FTD hari ≥ 4, "booming gain on heavier volume than the day before" | [ASAL-PETIK] (Goodreads) | [Goodreads](https://www.goodreads.com/book/show/72151.How_to_Make_Money_in_Stocks) |
| 14 | IBD | Ambang 1% → 1.7% (volatiliti) → kini 1.2% atau 1.25% | [SEKUNDER] (Hanna kuat; semasa bercanggah) | [Quantifiable Edges](https://quantifiableedges.com/ibd-follow-through-days-pt-1-are-they-predictive/) |
| 15 | IBD | Kadar kejayaan FTD 45–55% (bukan 70–80%) | [SEKUNDER kuat] ujian bebas | [Quantifiable Edges](https://quantifiableedges.com/follow-through-days-quantified/) |
| 16 | IBD | Distribution day: jatuh ≥ 0.2% + volum lebih tinggi; luput 25 sesi atau +5% | [ASAL-PETIK] MarketSmith (afiliasi) | [MarketSmith India](https://marketsmithindia.com/support) |
| 17 | IBD | Ambang kiraan "Uptrend under pressure" | [TIDAK DISAHKAN] (4–5 lawan 5–6) | [LuxAlgo](https://www.luxalgo.com/library/concept/distribution-days/) |
| 18 | Wilder | ADXR = (ADX_t + ADX_{t−(n−1)})/2 | [ASAL-KOD] TA-Lib | [TA-Lib](https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_ADXR.c) |
| 19 | Wilder | 25/20 pada ADX (StockCharts) lawan ADXR (skrip/LuxAlgo) | [TIDAK DISAHKAN] daripada buku | [StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/average-directional-index-adx) |
| 20 | Kaufman | Masuk > 25 / keluar < 20 | [TIDAK DISAHKAN] semula | — |
| 21 | Elder Impulse | EMA13 + MACD-H(12,26,9); hijau/merah/biru; penapisan | [SEKUNDER] konsisten (dokumen platform) | [StockCharts](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/elder-impulse-system) |
| 22 | Elder Triple Screen | Skrin 1 = cerun MACD-H mingguan (1993); EMA 26 mgg dan/atau MACD-H (2002); EMA 13 mgg lemah | [SEKUNDER] | [Incredible Charts](https://www.incrediblecharts.com/technical/macd_and_histogram.php); [blog 2012](https://stock-market-observations.com/2012/01/30/elder-impulse-system-013012/) |
| 23 | TradingView | 26 penunjuk; peraturan setiap penunjuk; (MA + Osc)/2; ±0.1/±0.5 | [ASAL-KOD] port TechnicalRating v3 | [obrii-tv-rules](https://github.com/all-in0/obrii-tv-rules) |
| 24 | Barchart | 13 penunjuk, purata %, kekuatan 7 tahap, arah 3 hari, syot kilat 1 hari/1 mgg/1 bln | [ASAL-PETIK] | [Barchart](https://www.barchart.com/stocks/quotes/aapl/opinion) |
| 25 | Barchart | Pemetaan % → Weak/Buy/Strong (33%/66%) | [TIDAK DISAHKAN] | — |
| 26 | StockCharts SCTR | 30/30/15/15/5/5 (EMA200, ROC125, EMA50, ROC20, cerun PPO-H 3 hari, RSI14) | [ASAL-PETIK] + [ASAL-KOD] | [ChartSchool](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/stockcharts-technical-rank-sctr) |
| 27 | Trend Composite (Hill) | 5 × ±1 (MA Trend 125/5, CCI 125, BB 125/1, KC 125/2, StochClose 125/5); julat ganjil −5..+5 | [ASAL-PETIK] | [StockCharts help](https://help.stockcharts.com/charts-and-tools/stockchartsacp/stockchartsacp-plug-ins/trend-investor-pro-indicator-edge) |
| 28 | Trading Central | 3 ufuk; julat 2–6 mgg / 6–39 mgg / 9 bln+ | [SEKUNDER] bercanggah (Fidelity lama ≤ 3 mgg / ≤ 3 bln) | [GitHub issue](https://github.com/ram290476/investor-dashboard/issues/191); [Fidelity](https://research2.fidelity.com/fidelity/research/reports/release2/Research/TradingCentral.asp) |
| 29 | moomoo | Kiraan isyarat bullish/bearish daripada 15 penunjuk; Daily/60m/1m; ambang tidak diterbitkan | [ASAL-PETIK] | [moomoo manual](https://www.moomoo.com/us/manual/topic-14-60) |
| 30 | SST | Enum 6 nilai; Uptrend ⇔ trendTemplate; Constructive ⇔ C > 50 & C > 200; Neutral ⇔ di antara; Downtrend ⇔ C < 50 & C < 200 | Enum [ASAL-PETIK skema]; peraturan [PEMERHATIAN, n = 23] | §8 |
| 31 | Bulkowski | Gagal-10% tembusan menaik 14% (1990-an) → 28% (2003–07); 11% (1991) → 44% (2007) | [ASAL-PETIK] | [thepatternsite](https://thepatternsite.com/FailureRates.html) |
| 32 | Bulkowski | Volum tembusan: prestasi +1.8 mp tetapi "failures triple" lawan "failures drop"; trend volum 3 mgg −31% kegagalan | [ASAL-PETIK] bercanggah dalaman | [VolumeStudy](https://thepatternsite.com/VolumeStudy.html); [Volume](https://thepatternsite.com/Volume.html) |
| 33 | "Hari dalam trend" | Tiada platform arus perdana; Barchart syot kilat + arah 3 hari; Aroon; skrip komuniti | [ASAL-PETIK] Barchart; [SEKUNDER] lain | §7 |

### Inferences
- **[IN] Senarai pembetulan kepada nota terdahulu:**
  1. Peraturan SST dalam NAT §2.10 salah (lihat §8). SST juga mempunyai label "Breakout" dan "Unknown".
  2. Syarat 3 Minervini mengandungi kedua-dua "preferably" dan "minimum".
  3. Skrin pertama Elder: cerun MACD-H mingguan / EMA 26 minggu, bukan EMA 13 minggu.
  4. Peraturan ADX TradingView semasa = ADX > 20 dan naik (bukan silang DI). StochRSI/BBP dikondisikan EMA50. UO > 70 = beli.
  5. SCTR semasa menggunakan EMA; versi 2014 menggunakan SMA.
  6. Barchart: pemetaan % → label tidak didokumenkan; set semasa ≠ legacy.
  7. FTD: ambang semasa 1.2% lawan 1.25% tidak dapat diputuskan; kadar kejayaan 45–55% (Hanna).
  8. Volum Weinstein: 2× paling disokong; 1.5× bukan Weinstein; volum tidak wajib untuk pecahan ke bawah.
  9. Dapatan volum Bulkowski bercanggah dalaman; angka "14% lawan 5%" PMN tidak disahkan semula.
- **[IN] Implikasi untuk keputusan Bullish/Bearish/Neutral papan (swing 3–30 sesi):**
  - Sumber primer yang disahkan **tidak** memberi satu takrif "betul". Setiap rangka memilih paksi dan pengesahan sendiri:
    - Minervini: 8/8 syarat;
    - SST: harga lawan SMA50/SMA200 + templat;
    - TradingView/Barchart: undian penunjuk dengan jalur neutral ±0.1 atau purata %;
    - Weinstein: cerun MA 30 minggu + tembusan.
  - Satu-satunya bukti empirikal bebas yang ditemui (Roskill; Hanna; Bulkowski) menunjukkan bahawa:
    - (a) nilai ramalan datang daripada "harga di atas MA yang naik";
    - (b) pengesahan onset (FTD, tembusan) mempunyai kadar penggera palsu ~45–55%.
  - Ini menyokong cadangan RP/PMN: label keadaan perlahan berpaksi MA + lencana onset dengan syarat gagal jelas.

### Gaps
- Sumber primer penuh (buku Weinstein, Minervini, O'Neil, Wilder, Elder, Kaufman; dokumen IBD dan Barchart) tidak dapat dibaca kerana sekatan rangkaian. Status [ASAL-PETIK] dalam nota ini bergantung pada petikan enjin carian, agregator atau salinan teks dalam kod. Semakan terakhir pada edisi berlesen disyorkan bagi item 3, 5, 10, 13 dan 19.
