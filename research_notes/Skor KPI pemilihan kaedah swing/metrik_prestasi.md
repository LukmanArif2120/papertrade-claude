# Metrik prestasi untuk menilai dan menyusun kaedah swing (pegang 3–30 hari)

Nota kaedah: dalam sesi ini WebFetch dan curl disekat oleh proksi (DNS/403), jadi semua dapatan di bawah diambil daripada ringkasan hasil WebSearch (abstrak, dokumentasi platform, glosari). Teks penuh kertas Wiecki et al. (2016), Lo (2002), Bailey & López de Prado tidak dapat dibaca terus; angka yang tidak disahkan ditanda. Istilah teknikal Inggeris dikekalkan dalam kurungan supaya padan dengan sumber.

## S1. Apa yang diukur oleh setiap metrik, formula, ambang "baik" dan kelemahan

### Takeaway
Hampir semua metrik peringkat dagangan (jangkaan, faktor untung, kadar menang, nisbah bayaran, Omega, nisbah ekor, SQN) ialah fungsi taburan pulangan setiap dagangan yang sama; metrik peringkat strategi (Sharpe/Sortino tahunan, MAR/Calmar, Ulcer/UPI, K-ratio) memerlukan siri ekuiti mengikut masa dan tidak bermakna untuk 2 minggu data hadapan. SQN Van Tharp pada asasnya statistik-t purata R dengan N dihadkan 100, dan ia satu-satunya metrik "gred" yang secara langsung menggabungkan saiz kelebihan, kebisingan dan saiz sampel.

### Cited Findings
**Jangkaan (expectancy) dan R-multiple**
- R = risiko awal dagangan (jarak masuk ke henti × saiz posisi); R-multiple = untung/rugi dagangan ÷ 1R; dagangan yang kena henti awal = −1R — [NexusFi R-multiples](https://nexusfi.com/a/risk-management/r-multiples); [LuxAlgo R-multiple](https://www.luxalgo.com/library/concept/r-multiple-framework/)
- Tharp mentakrif jangkaan sistem sebagai purata R-multiple; disyorkan sekurang-kurangnya kira-kira 30–100 contoh sebelum purata bermakna — [vantharp.com](https://vantharp.com/?p=10928); [Bear Bull Traders "Trading to the power of R"](https://members.bearbulltraders.com/trading-to-the-power-of-r/)
- Jangkaan = kadar menang × purata menang − kadar rugi × purata rugi; patut dikira bersih kos kerana jangkaan kasar "selalu bertukar tanda selepas kos realistik"; contoh: menang 70%, purata menang $40, purata rugi $120 → −$8 setiap dagangan — [LuxAlgo Expectancy](https://www.luxalgo.com/library/concept/expectancy/)
- Kritikan: R tidak sentiasa sama nilai dolar antara dagangan, dan dagangan boleh rugi > 1R jika henti tergelincir/dipegang melebihi keluar yang dirancang — [NexusFi R-multiples](https://nexusfi.com/a/risk-management/r-multiples)

**SQN (System Quality Number, Van Tharp)**
- SQN = (jangkaan dalam R ÷ SD R-multiple) × √N, N = min(bilangan dagangan, 100) — [Tradervue report stats](https://www.tradervue.com/help/reports/report_stats); [NexusFi SQN](https://nexusfi.com/a/risk-management/system-quality-number-sqn)
- Skala yang dipetik kepada Tharp: 1.6–1.9 bawah purata tetapi boleh didagang; 2.0–2.4 purata; 2.5–2.9 baik; 3.0–5.0 cemerlang; 5.1–6.9 hebat; ≥ 7.0 "mungkin Holy Grail" — [QuantShare SQN indicator](https://www.quantshare.com/item-1541-system-quality-number-indicator); [StrategyQuant forum](https://strategyquant.com/forum/topic/3112-sqn-system-quality-number-error-calculation/). Sempadan berbeza sedikit: Tradervue guna 3.0–4.9 / 5.0–6.9 / 7.0+; Edgewonk guna 2.01–3.00 "Good", ≥ 7.01 "Holy Grail" — [Tradervue](https://www.tradervue.com/help/reports/report_stats); [Edgewonk](https://edgewonk.zendesk.com/hc/en-us/articles/360010061840-SQN-by-setup-System-Quality-Number)
- Tradervue: SQN secara umum tidak boleh dipercayai dengan < 30 dagangan — [Tradervue](https://www.tradervue.com/help/reports/report_stats)
- Tanpa had N, SQN boleh mencapai 40, 100 atau 1000 (kerana banyak dagangan); StrategyQuant mempunyai varian "SQN Score" = SQN × dagangan setahun ÷ 100 (ubahsuai platform, bukan formula Tharp) — [StrategyQuant forum](https://strategyquant.com/forum/topic/3112-sqn-system-quality-number-error-calculation/)
- Ulasan moden: SQN > 7.0 pada data backtest ialah tanda amaran pemadanan lengkung (curve-fitting), bukan bukti Holy Grail (gloss sekunder, bukan Tharp) — [QuantMonitor SQN](https://quantmonitor.net/system-quality-number-sqn/)

**Faktor untung (profit factor), nisbah bayaran (payoff), kadar menang**
- Faktor untung = untung kasar ÷ rugi kasar; tidak memberitahu urutan keputusan dan boleh dipesongkan oleh satu dagangan menang besar — [LuxAlgo Profit Factor](https://www.luxalgo.com/library/concept/profit-factor.md); [NexusFi Profit Factor](https://nexusfi.com/a/risk-management/profit-factor)
- Hubungan tepat: PF = (W ÷ (1 − W)) × P, W = kadar menang, P = nisbah bayaran (purata menang ÷ purata rugi); kadar menang pulang modal = 1 ÷ (1 + P); contoh W 60%, P 1:1 → PF 1.5 — [NexusFi trading performance metrics](https://nexusfi.com/a/risk-management/trading-performance-metrics)
- Sampel kecil boleh memaparkan PF 2.5 pada sistem pulang modal; jangkaan daripada 30 dagangan tidak boleh dipercayai — [NexusFi Profit Factor](https://nexusfi.com/a/risk-management/profit-factor); [LuxAlgo Expectancy](https://www.luxalgo.com/library/concept/expectancy/)

**Sharpe, PSR, DSR, Sortino**
- Lo (2002): Sharpe bulanan tidak boleh ditahunkan dengan ×√12 kecuali dalam keadaan sangat khas; korelasi bersiri boleh melebih-lebihkan Sharpe tahunan > 65% (dan mengurangkannya jika korelasi negatif) — [CFA Institute FAJ abstract](https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios); [IDEAS/RePEc](https://ideas.repec.org/a/taf/ufajxx/v58y2002i4p36-52.html)
- Probabilistic Sharpe Ratio (PSR, Bailey & López de Prado 2012) memberi kebarangkalian Sharpe sebenar melebihi ambang bila pulangan tidak normal, dan menerbitkan panjang rekod minimum (MinTRL) yang dikaitkan dengan kecondongan dan kurtosis — [Journal of Risk, "The Sharpe ratio efficient frontier"](https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier); [PortfolioOptimizer PSR/MinTRL](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/). Formula yang lazim dipetik: PSR(SR*) = Φ[(SR̂ − SR*)·√(n − 1) ÷ √(1 − γ₃·SR̂ + ((γ₄ − 1)/4)·SR̂²)] (γ₃ kecondongan, γ₄ kurtosis; diturunkan daripada kertas asal mengikut ingatan, teks penuh tidak dibaca dalam sesi ini)
- Untuk taburan pulangan dana lindung nilai biasa, MinTRL mudah melebihi beberapa tahun data bulanan (sumber sekunder) — [PortfolioOptimizer](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/)
- Deflated Sharpe Ratio (DSR, 2014, JPM) membetulkan dua punca inflasi: bias pemilihan di bawah ujian berbilang dan pulangan tidak normal — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551); [Wikipedia DSR](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- Sortino = pulangan melebihi pulangan minimum boleh terima (MAR) ÷ sisihan menurun (downside deviation; semivarians bawah MAR); sesetengah kertas syor MAR = kadar bebas risiko bila membanding banyak pelaburan — [PerformanceAnalytics SortinoRatio](https://www.rdocumentation.org/packages/PerformanceAnalytics/versions/2.0.8/topics/SortinoRatio)

**MAR / Calmar**
- Calmar (Terry Young, 1991, majalah *Futures*; CALifornia Managed Accounts Reports) = pulangan tahunan purata 36 bulan terakhir ÷ kejatuhan maksimum 36 bulan terakhir (dikira bulanan); MAR = pulangan tahunan ÷ kejatuhan maksimum sejak mula — [Wikipedia Calmar ratio](https://en.wikipedia.org/wiki/Calmar_ratio); [Business Professor MAR ratio](https://thebusinessprofessor.com/mar-ratio-explained/)

**Ulcer Index / UPI (Peter Martin)**
- Ulcer Index (Martin 1987; buku Martin & McCann 1989) = punca kuasa dua purata kuasa dua peratus kejatuhan daripada puncak berjalan; kuasa dua memberi berat lebih kepada kejatuhan dalam, dan ia menangkap kedalaman serta tempoh kejatuhan — [StockCharts ChartSchool](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ulcer-index); [Wikipedia Ulcer index](https://en.wikipedia.org/wiki/Ulcer_index)
- AmiBroker: UPI = (untung tahunan − untung Treasury) ÷ Ulcer Index, dengan untung Treasury dikod keras 5.4 — [AmiBroker "Reading backtest report"](https://www.amibroker.com/guide/h_report.html)

**K-ratio (Lars Kestner)**
- K-ratio = cerun regresi garis lurus lengkung ekuiti log ÷ ralat piawai cerun; versi 1996, 2003 (penyebut tambah n) dan 2013 (× √(cerapan setahun) ÷ n) memberi nilai sangat berbeza pada lengkung sama: 1.65 / 0.0953 / 1.51 dalam satu contoh — [The Systematic Trader](https://thesystematictrader.com/2013/04/coding-lars-kestners-k-ratio-in-excel/); [MetricGate K-ratio](https://metricgate.com/docs/kestner-k-ratio/)
- AmiBroker: K-ratio mengesan ketidakkonsistenan pulangan; panduannya ≥ 1.0 — [AmiBroker guide](https://www.amibroker.com/guide/h_report.html). (Ada dakwaan pihak ketiga bahawa AmiBroker guna versi 2003 sehingga > 1 hampir mustahil — tidak disahkan.)

**Omega dan nisbah ekor (tail ratio)**
- Omega (Keating & Shadwick 2002, "A Universal Performance Measure") = nisbah berwajaran kebarangkalian untung lawan rugi berbanding ambang θ; pada θ = 0 ia menjadi nisbah untung-rugi Bernardo & Ledoit — [Keating & Shadwick (salinan Duke)](https://people.duke.edu/~charvey/Teaching/BA453_2006/Keating_An_introduction_to.pdf); [Wikipedia Omega ratio](https://en.wikipedia.org/wiki/Omega_ratio); [arXiv 1911.10254](https://arxiv.org/pdf/1911.10254)
- Nisbah ekor = persentil ke-95 pulangan ÷ |persentil ke-5|; > 1 bermaksud ekor atas lebih besar — [TradesViz tail ratio](https://www.tradesviz.com/glossary/tail-ratio/); [fynance tail_ratio](https://fynance.readthedocs.io/en/stable/generated/fynance.features.stats.tail_ratio.html)
- Ikut gaya: ikut-trend sepatutnya nisbah ekor > 1 (untung besar, rugi kecil kerap); balikan-min dan jual-volatiliti biasanya < 1 — [wraquant risk.tail](https://wraquant.readthedocs.io/en/latest/_modules/wraquant/risk/tail.html)

**Pulangan dilaras pendedahan (exposure)**
- AmiBroker "Risk Adjusted Return %" = pulangan tahunan ÷ pendedahan (exposure), iaitu pulangan kompaun setara jika sistem dilaburkan 100% masa; "Net RAR" = untung bersih % ÷ pendedahan % — [AmiBroker guide](https://www.amibroker.com/guide/h_report.html)

### Inferences
- SQN = √N × purata ÷ SD = statistik-t purata (dengan N dihadkan 100). Jadi "had bawah 95% purata > 0" dalam KPI semasa bersamaan dengan SQN/t > 1.96 — dua metrik ini hampir sama maklumat.
- Sharpe setiap dagangan (purata ÷ SD dagangan) = SQN ÷ √N; ia ukuran kualiti kelebihan bebas saiz sampel, manakala SQN mencampur kualiti + bukti. Untuk penyusunan adil antara kaedah yang bilangan dagangannya berbeza, Sharpe setiap dagangan (atau SQN dengan N tetap, cth. 100) lebih adil daripada SQN mentah.
- Metrik peringkat strategi (Sharpe tahunan, MAR/Calmar, Ulcer, K-ratio) hanya bermakna pada siri ekuiti harian/mingguan yang panjang — guna pada backtest 2019–2026 (atau portfolio maya 10 slot), bukan pada 2 minggu Lejar Penuh.
- Contoh aritmetik (ilustrasi, bukan data): purata 1%, SD 8% setiap dagangan → Sharpe dagangan 0.125; untuk had bawah 95% > 0 perlu N ≈ (1.96 ÷ 0.125)² ≈ 246 cerapan bebas. Dengan dagangan berkelompok, cerapan bebas jauh lebih sedikit daripada bilangan dagangan.

### Gaps
- Jadual SQN asal daripada buku Tharp (*Definitive Guide to Position Sizing*) tidak dapat dibaca; skala di atas daripada sumber sekunder yang konsisten tetapi sempadannya berbeza sedikit.
- Ambang "baik" bagi faktor untung, Sharpe tahunan, Sortino, MAR yang berwibawa (bukan blog) tidak ditemui dalam carian ini.
- Formula tepat empyrical/pyfolio `tail_ratio` dan formula PSR/DSR tidak dapat disahkan terhadap teks asal (WebFetch disekat).

## S2. Metrik yang bertindih (jangan dikira dua kali)

### Takeaway
Kadar menang, nisbah bayaran, faktor untung, Omega(0) dan jangkaan ialah satu keluarga: PF = W/(1−W) × P dan Omega pada ambang 0 untuk pulangan dagangan = PF; had bawah 95% purata ≈ SQN/statistik-t. KPI semasa memberi berat ~25–30% kepada maklumat yang sama dalam bentuk berbeza, dan dua metrik risikonya (terburuk, tanpa 3 terbaik) bergantung pada saiz sampel.

### Cited Findings
- PF = (W ÷ (1 − W)) × P (hubungan algebra tepat) — [NexusFi trading performance metrics](https://nexusfi.com/a/risk-management/trading-performance-metrics)
- Kadar menang, purata R-multiple dan PF "saling berkait; tidak boleh dinilai secara berasingan" — [NexusFi trading performance metrics](https://nexusfi.com/a/risk-management/trading-performance-metrics)
- Jangkaan menggabungkan nisbah bayaran dengan kadar menang menjadi hasil purata setiap dagangan — [LuxAlgo Expectancy](https://www.luxalgo.com/library/concept/expectancy/)
- Omega pada θ = 0 = nisbah untung-rugi Bernardo–Ledoit — [Wikipedia Omega ratio](https://en.wikipedia.org/wiki/Omega_ratio); [arXiv 1911.10254](https://arxiv.org/pdf/1911.10254)
- Calmar dan MAR sama formula, beza tetingkap (36 bulan lawan sejak mula) — [Business Professor](https://thebusinessprofessor.com/mar-ratio-explained/)
- Ulcer Index menangkap kedalaman dan tempoh kejatuhan (jadi bertindih dengan kejatuhan maksimum, tetapi lebih stabil kerana guna semua titik) — [StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/ulcer-index)

### Inferences
- Dalam KPI semasa: "kadar menang (8) + faktor untung (7)" bersama "purata rugi (5)" dan "untung purata (25)" sudah menentukan semula jangkaan; kadar menang + PF + purata rugi secara efektif mengira nisbah bayaran dua kali. Cadangan: simpan SATU daripada {PF, Omega(0)} untuk bentuk taburan, buang kadar menang daripada skor (papar sahaja sebagai maklumat psikologi).
- Untuk pulangan dagangan berwajaran sama, Omega(0) = Σ untung ÷ Σ |rugi| = PF (identiti, terbitan daripada takrif). Jangan masukkan kedua-duanya.
- "Had bawah 95% purata" (Bukti 5) bertindih dengan "untung purata dikecutkan" (Untung 25) dan SQN; ketiga-tiganya bergerak bersama purata dan √n. Pilih satu ukuran keyakinan.
- "Terburuk" (statistik tertib ekstrem) dan "purata tanpa 3 terbaik" bergantung pada n: kaedah dengan 200 dagangan hampir pasti mempunyai dagangan terburuk lebih teruk daripada kaedah dengan 20 dagangan, dan membuang 3 daripada 20 (15%) jauh lebih berat daripada 3 daripada 200 (1.5%). Kedua-duanya menghukum/menolong kaedah ikut saiz sampel, bukan kualiti. Ganti dengan ukuran berkadar: purata dipangkas 5% (sudah digunakan dalam Papan Penganalisis) dan CVaR 5% (purata 5% dagangan terburuk) atau persentil ke-5.
- Median dan purata dipangkas bertindih separa; median kurang cekap untuk taburan pulangan berekor kanan (strategi swing ikut-trend memperoleh untung daripada ekor kanan), jadi median boleh menghukum kaedah yang sihat bila kadar menang < 50%.
- MAE purata dan purata rugi/terburuk sangat berkorelasi bagi kaedah tanpa henti ketat (dagangan yang rugi besar semestinya MAE besar).

### Gaps
- Tiada kajian empirikal ditemui yang mengukur korelasi silang metrik-metrik ini pada populasi strategi (cth. matriks korelasi PF, Sharpe, SQN merentas ratusan sistem). Boleh dikira terus daripada Lejar Penuh/registry repo.

## S3. Kecekapan modal dan masa dalam dagangan untuk swing

### Takeaway
Untuk portfolio slot terhad, metrik yang betul ialah pulangan setiap hari-modal = Σ pulangan ÷ Σ hari dipegang (nisbah jumlah), atau pulangan tahunan ÷ pendedahan (konsep RAR AmiBroker) — bukan purata (r_i ÷ d_i) dan bukan pulangan dagangan yang ditahunkan. Pada awal tempoh papertrade, "pulangan sehari" berat sebelah teruk kerana penapisan kanan (dagangan yang sudah selesai hanyalah yang keluar cepat).

### Cited Findings
- AmiBroker RAR = pulangan tahunan ÷ pendedahan; menunjukkan pulangan kompaun setara jika dilabur 100% masa — [AmiBroker guide](https://www.amibroker.com/guide/h_report.html)
- Lo (2002): penahunan dengan √q salah apabila pulangan berkorelasi bersiri; Sharpe tahunan boleh terlebih > 65% — [IDEAS/RePEc](https://ideas.repec.org/a/taf/ufajxx/v58y2002i4p36-52.html)
- Hubungan K-ratio dan metrik lain hanya boleh dibanding pada kekerapan pulangan yang sama — [MetricGate K-ratio](https://metricgate.com/docs/kestner-k-ratio/)
- Novy-Marx & Velikov: kebanyakan anomali dengan pusing ganti sehala bulanan < 50% kekal signifikan selepas kos; sedikit sahaja yang pusing gantinya lebih tinggi — [Novy-Marx & Velikov (Rochester PDF)](https://mysimon.rochester.edu/novy-marx/research/ToAatTC.pdf); [NBER w20721](https://www.nber.org/papers/w20721)

### Inferences
- Tiga takrif "pulangan sehari" memberi susunan berbeza:
  (a) purata(r_i ÷ d_i) — meletup bagi dagangan 1 hari (r = 3% dalam 1 hari = 3%/hari) dan membuat kaedah yang keluar cepat kelihatan hebat;
  (b) purata(r) ÷ purata(d) = Σr ÷ Σd — pulangan setiap hari-slot, stabil, sesuai untuk portfolio 10 slot;
  (c) penahunan setiap dagangan (1 + r)^(252/d) − 1 — tidak masuk akal untuk d kecil: 2% dalam 1 hari → 1.02^252 − 1 ≈ +14,600% setahun.
  Cadangan: guna (b), dinyatakan sebagai % setiap 21 hari dagangan (sebulan) — konsisten dengan "skor sebulan" Papan Penganalisis.
- Penapisan kanan (right-censoring): selepas 2 minggu, dagangan selesai ialah yang d ≤ ~10; kaedah dengan keluar pantas (henti ketat, sasaran kecil) mempunyai banyak dagangan selesai, kaedah ikut-trend/lorong 2 Chandelier kebanyakannya masih dipegang. Menyusun hanya dagangan selesai berat sebelah kepada kaedah cepat. Pembetulan: (1) masukkan posisi terbuka pada harga tanda pasaran (mark-to-market) dalam Σr dan hari dipegang setakat ini dalam Σd; atau (2) hanya bandingkan kohort yang sudah matang (beli ≥ purata hari pegang backtest yang lalu — selari dengan "tarikh adil" dashboard); atau (3) gunakan hari pegang backtest sebagai penyebut sehingga kohort matang.
- Dalam reka bentuk "beli setiap isyarat 1 unit", tiada kekangan modal, jadi pulangan purata setiap dagangan tidak menghukum kaedah yang memegang lama. Untuk matlamat "3–4 kaedah, untung maksimum" dengan slot terhad, Σr ÷ Σd (atau pulangan portfolio slot sebenar) lebih relevan daripada purata dagangan.
- Pulangan sehari mesti dikira bersih kos: kos tetap setiap pusingan menghukum dagangan pendek lebih berat secara relatif (kos 0.2% atas pegang 2 hari = 0.1%/hari; atas 20 hari = 0.01%/hari).
- Swing 3–30 hari bersamaan pusing ganti bulanan jauh > 50% (pegang purata 5 hari ≈ 4 pusingan sebulan ≈ 400%), iaitu zon yang Novy-Marx & Velikov dapati jarang selamat selepas kos.

### Gaps
- Tiada sumber berwibawa ditemui yang secara khusus membincangkan "pulangan sehari dipegang" sebagai metrik strategi swing atau pembetulan penapisan dalam papertrade awal; cadangan di atas ialah inferens.

## S4. MAE/MFE (John Sweeney) untuk menilai risiko dan kecekapan keluar

### Takeaway
MAE/MFE paling berguna sebagai alat diagnosis taburan (MAE pemenang lawan pengalah untuk meletak henti; dagangan selesai ÷ MFE untuk kecekapan keluar), bukan sebagai purata mentah dalam skor — purata MAE meningkat dengan tempoh pegang dan volatiliti saham, jadi ia menghukum kaedah/lorong yang memegang lebih lama.

### Cited Findings
- MAE = kerugian terapung terbesar sebelum dagangan ditutup; MFE = untung terbuka terbaik; dagangan boleh mempunyai MAE besar dan masih menang — [NexusFi MAE](https://nexusfi.com/a/risk-management/maximum-adverse-excursion-mae); [LuxAlgo MAE/MFE distributions](https://www.luxalgo.com/library/concept/mae-mfe-distributions.md)
- Sweeney memperkenalkan MAE dalam buku *Maximum Adverse Excursion* (tarikh 1996 atau Jan 1997 — sumber bercanggah); dengan menganalisis MAE sesiri dagangan, paras henti optimum boleh ditentukan secara statistik — [NexusFi MAE](https://nexusfi.com/a/risk-management/maximum-adverse-excursion-mae); [rekod buku (ACS)](https://now.acs.org/book/virtual-library/HomePages/Maximum_Adverse_Excursion_Analyzing_Price_Fluctuations_For_Trading_Management.pdf)
- Takrif long: MFE = harga tertinggi semasa terbuka − harga masuk; MAE = harga masuk − harga terendah semasa terbuka; kedua-duanya dilantai pada 0 — [PineConnector MAE/MFE](https://www.pineconnector.com/blogs/pico-blog/mae-mfe-trade-excursion)
- Kecekapan keluar = pergerakan yang direalisasi ÷ pergerakan MFE (boleh negatif bagi keluar rugi) — [Spreadsheets Hub](https://spreadsheetshub.com/blogs/articles/how-to-track-mfe-and-mae-to-improve-your-exit-analysis)
- Satu takrif pihak ketiga kecekapan masuk = MFE ÷ (MFE + MAE) — [MQL5 article 23905](https://www.mql5.com/en/articles/23905)
- Kecekapan dikira atas pulangan kasar atau bersih ikut tetapan, manakala MFE/MAE kasar, jadi mod bersih menunjukkan kecekapan lebih rendah — [TraderSync](https://tradersync.com/support/how-do-mfe-mae-and-efficiency-work/)
- Dakwaan "henti boleh diletak untuk mengekalkan 75–85% dagangan menang" datang daripada catatan pengguna TradingView tanpa sumber — tidak boleh dipercayai — [TradingView post](https://kr.tradingview.com/chart/BTCUSD/vvTceYm2-Adverse-excursion-a-key-concept-for-risk-management)

### Inferences
- Untuk skor risiko, normalkan MAE: MAE ÷ ATR14 semasa masuk (unit R berasaskan volatiliti, selaras dengan idea R-multiple Tharp), atau MAE ÷ √(hari dipegang). Purata MAE mentah dalam % menghukum kaedah saham volatil dan lorong 2 (pegang lebih lama → lebih banyak masa untuk lawatan buruk).
- Untuk Chandelier 4×ATR14, MAE dalam unit ATR hampir terhad oleh reka bentuk (selepas puncak), jadi MAE lebih berguna menilai lorong kaedah.
- Kegunaan Sweeney yang paling bernilai bagi sistem ini: plot MAE (unit ATR) pemenang lawan pengalah setiap kaedah; jika hampir semua pemenang tidak pernah melebihi k×ATR, henti pada k×ATR mengurangkan rugi tanpa mengorbankan pemenang. Ini diagnosis reka bentuk keluar, bukan metrik penyusunan.
- Kecekapan keluar (r ÷ MFE) membanding dua lorong secara langsung: jika lorong kaedah mempunyai kecekapan rendah (memberi balik banyak MFE), lorong 2 mungkin lebih baik — sedia ada data untuk ini (`prestasi/mfe`).

### Gaps
- Formula rasmi TradeStation bagi "entry/exit/total efficiency" tidak ditemui; teks buku Sweeney tidak boleh dicapai. Tiada kajian bersemak rakan sebaya yang mengesahkan dakwaan peletakan henti berasaskan MAE ditemui.

## S5. Memasukkan kos dagangan/gelinciran sebelum menyusun

### Takeaway
Kos mesti ditolak setiap dagangan sebelum sebarang metrik dikira, kerana ia menurunkan keuntungan dan kesignifikanan dalam semua kes dan paling menghukum strategi pusing ganti tinggi (swing pendek, balikan jangka pendek) serta saham kecil/kurang cair; susunan kaedah boleh berubah selepas kos.

### Cited Findings
- Kos dagangan mengurangkan keuntungan dan kesignifikanan statistik dalam semua kes, menambah kebimbangan data-snooping; anomali pusing ganti sehala bulanan < 50% kebanyakannya kekal signifikan, sedikit yang lebih tinggi; julat beli/pegang (buy/hold spread — terus memegang saham yang tidak akan dibeli baharu) ialah teknik mitigasi ringkas paling berkesan — [Novy-Marx & Velikov, RFS 2016 (PDF)](https://mysimon.rochester.edu/novy-marx/research/ToAatTC.pdf); [NBER w20721](https://www.nber.org/papers/w20721)
- Anggaran kos mereka guna spread bid-ask efektif Hasbrouck (2009), yang tidak merangkumi kesan harga dagangan besar — sesuai untuk "pengambil kecairan kecil" (seperti peruncit) — [Alpha Architect](https://alphaarchitect.com/2017/05/trading-costs-destroy-factor-investing/)
- Strategi berwajaran sama terjejas lebih teruk kerana tertumpu pada saham kecil kurang cair (sekunder, tidak disahkan pada teks asal) — [Alpha Architect](https://alphaarchitect.com/2017/05/trading-costs-destroy-factor-investing/)
- Frazzini, Israel & Moskowitz: data pelaksanaan langsung $1.7 trilion (AQR, 21 pasaran, 1998–2016) menunjukkan kos sebenar institusi "satu tertib magnitud lebih kecil" daripada kajian terdahulu; versi NBER 2012 mendapati balikan jangka pendek (short-term reversal) paling terhad oleh kos — [SSRN 3229719](https://papers.ssrn.com/abstract=3229719); [NBER draft](https://conference.nber.org/conf_papers/f68262/f68262.pdf)
- Jangkaan kasar selalunya bertukar tanda selepas kos realistik; kira bersih kos — [LuxAlgo Expectancy](https://www.luxalgo.com/library/concept/expectancy/)

### Inferences
- Model kos ringkas untuk "beli pada buka esok, jual pada buka/tutup": kos pusingan = spread efektif (½ spread × 2) + gelinciran lelong buka + yuran kawal selia. Dalam papertrade, gunakan sekurang-kurangnya kos tetap setiap pusingan dan uji sensitiviti (cth. 2–3 tahap) — nilai bps tepat TIDAK disahkan dalam carian ini; guna ujian sensitiviti dan semak sama ada 4 kaedah teratas kekal teratas.
- Kos berskala dengan kecairan: kos lebih tinggi untuk saham harga rendah/nilai dagangan rendah (selari dengan penapis "tidak cair" repo: median nilai < USD100 ribu sudah dibuang). Model kos berasaskan kelompok nilai dagangan median 20 hari lebih adil daripada kos rata.
- Kos tetap setiap dagangan bermakna kaedah dengan purata untung kecil tetapi kadar menang tinggi (balikan jangka pendek) paling mudah jatuh susunan; inilah kumpulan yang Frazzini et al. sebut paling terhad.
- Belian semula kaedah+saham sama selepas keluar lorong kaedah (sejak 19 Okt 2026) menambah pusing ganti; idea julat beli/pegang Novy-Marx & Velikov menyokong untuk tidak keluar-masuk saham yang sama secara berulang.

### Gaps
- Tiada angka bps kos pusingan untuk peruncit AS (broker tanpa komisen, pesanan pada lelong buka) ditemui daripada sumber primer dalam sesi ini; angka spread efektif mengikut saiz syarikat daripada Novy-Marx & Velikov / Frazzini et al. tidak dapat dibaca (teks penuh disekat).

## S6. Bukti metrik dalam-sampel mana yang meramal prestasi luar-sampel

### Takeaway
Sharpe/pulangan backtest hampir tidak meramal prestasi hadapan (Quantopian: R² < 0.025); volatiliti, kejatuhan maksimum dan ciri bentuk taburan lebih stabil; semakin banyak percubaan/varian diuji, semakin besar jurang. Prestasi langsung biasanya separuh atau kurang daripada backtest (rule of thumb 50%; indeks bank median −73% Sharpe), dan potongan sepatutnya tidak linear: lebih besar bagi keputusan marginal dan bagi carian yang lebih luas (123 kaedah × 2 lorong).

### Cited Findings
- Wiecki, Campbell, Lent & Stauth (Quantopian, *Journal of Investing* 25(3):69–80, 2016): 888 algoritma ekuiti AS dengan ≥ 6 bulan luar sampel; metrik backtest biasa seperti Sharpe hampir tiada nilai meramal (R² < 0.025); momen tinggi (volatiliti, kejatuhan maksimum) dan ciri pembinaan portfolio (lindung nilai) menunjukkan nilai ramalan signifikan; lebih banyak backtest yang dijalankan → jurang IS–OOS lebih besar; pengelas tidak linear atas ciri tingkah laku backtest mencapai R² = 0.17 pada data simpanan, dan portfolio yang dipilih model itu jauh lebih baik OOS berbanding portfolio Sharpe backtest tertinggi — [pm-research (JoI)](https://www.pm-research.com/content/iijinvest/25/3/69); [Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/); [HedgeFundAlpha](https://hedgefundalpha.com/strategies/comparing-backtest-sample-performance-large-cohort-trading-algorithms/); [Semantic Scholar](https://www.semanticscholar.org/paper/All-That-Glitters-Is-Not-Gold:-Comparing-Backtest-a-Wiecki-Campbell/b028c2d0b2145e85d543fb21ad3fcf896c932ab5)
- Volatiliti tahunan dalam sampel berkorelasi positif dan signifikan dengan kekurangan Sharpe (Sharpe shortfall) — sumber sekunder — [CXO Advisory](https://www.cxoadvisory.com/big-ideas/in-sample-vs-out-of-sample-performance-of-888-trading-strategies)
- Penapis sampel: buang Sharpe < −1, backtest < 500 hari, dll.; regresi kekurangan Sharpe atas pusing ganti gagal menolak hipotesis nol (p = 0.074) — [kertas kerja (SSRN 2745220, salinan Portfolio123)](https://community.portfolio123.com/uploads/short-url/3WHpAUOzhCG8QAUez71HpoWnA62.pdf)
- Catatan forum Wealth-Lab (2016) mendakwa nisbah ekor ialah faktor paling penting dalam kertas Quantopian; seorang pengulas skeptikal — dakwaan forum, tidak disahkan — [Wealth-Lab forum](https://wealth-lab.com/Forum/Posts/Factors-to-predict-Out-of-Sample-Performance-38345)
- Harvey & Liu ("Backtesting", JPM 2015): amalan biasa ialah memotong Sharpe backtest 50%, tetapi itu "kesilapan serius" sebagai peraturan tetap; potongan ujian berbilang tidak linear — Sharpe tertinggi dipotong sederhana, Sharpe marginal dipotong teruk; input: saiz sampel, autokorelasi, bilangan ujian, korelasi antara ujian; contoh t = 3.0 yang kelihatan sangat signifikan mungkin tidak signifikan selepas mengambil kira ujian berbilang — [Harvey & Liu PDF (Duke)](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF); [Man Institute](https://www.man.com/insights/backtesting); [slaid Harvey (Wharton)](https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2015/05/3-Campbell-Harvey.pdf)
- Harvey, Liu & Zhu (2015) mendokumen sekurang-kurangnya 316 faktor diuji untuk pulangan keratan rentas — [rdocumentation profit.hurdle](https://www.rdocumentation.org/link/profit.hurdle)
- Basilico & Johnsen: ~215 indeks strategi daripada 17 bank pelaburan; potongan ≥ 50% bagi semua kelas aset, ≥ 60% bagi semua kumpulan strategi; median kemerosotan Sharpe backtest → langsung 73%; kemerosotan lebih besar bagi strategi lebih kompleks — [Alpha Architect](https://alphaarchitect.com/looking-at-alternatives-avoid-complexity-and-magical-backtests/)
- McLean & Pontiff (2016): pulangan anomali selepas penerbitan ~50% lebih kecil daripada dalam sampel; menurun ~25% tiga tahun selepas sampel dan ~40% lima tahun selepas sampel; direplikasi berkali-kali — [arXiv 2209.13623 (Publication Bias in Asset Pricing)](https://arxiv.org/pdf/2209.13623). (Angka asal 26% luar sampel / 58% selepas penerbitan tidak disahkan dalam sesi ini.)
- Probability of Backtest Overfitting (Bailey, Borwein, López de Prado, Zhu; *J. Computational Finance*): kaedah hold-out biasa tidak boleh dipercayai untuk pemilihan strategi; CSCV (combinatorially symmetric cross-validation) memberi anggaran PBO yang munasabah tanpa model — [SSRN 2326253](https://papers.ssrn.com/abstract=2326253); [eScholarship PDF](https://escholarship.org/content/qt4w1110bb/qt4w1110bb.pdf); pakej R `pbo` menyokong Omega sebagai metrik — [CRAN pbo README](https://packages.oit.ncsu.edu/cran/web/packages/pbo/readme/README.html)
- DSR membetulkan bias pemilihan di bawah ujian berbilang dan ketidaknormalan — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551)
- Pengecutan empirical Bayes "meminjam kekuatan" merentas banyak eksperimen untuk mengurangkan bias ke atas akibat pemilihan pemenang (winner's curse); risiko jika prior salah spesifikasi — [arXiv 2603.12867](https://arxiv.org/html/2603.12867); [Atticus Li (blog, bukan bersemak)](https://atticusli.com/replication-crisis/ab-testing-winners-curse/)
- Pertindihan/kelompok cerapan: ralat piawai yang mengabaikan korelasi dalam kelompok terlalu kecil; bilangan unit bebas efektif mengikut bilangan kelompok; ralat piawai kelompok-teguh lemah bila kelompok sedikit (gunakan wild cluster bootstrap) — [Cameron & Miller, "A Practitioner's Guide to Cluster-Robust Inference"](https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015_February.pdf); contoh praktik: statistik-t jatuh 2.4 → 1.4 bila tetingkap bertindih dibuang — [DEV Community](https://dev.to/michaelhairetis/overlapping-windows-will-manufacture-statistical-significance-in-your-backtest-jjj)

### Inferences
- Implikasi untuk KPI: (1) jangan beri berat besar kepada purata pulangan backtest/CAGR mentah; (2) beri berat kepada metrik yang stabil antara IS–OOS (volatiliti/SD dagangan, kejatuhan, bentuk ekor) dan kepada semakan luar sampel sebenar (S1–S4, WFO, AUTOTUNE — sudah ada); (3) potong Sharpe/purata secara tidak linear mengikut bilangan percubaan.
- Memilih "lorong yang lebih baik" setiap kaedah ialah ujian berbilang (2 percubaan setiap kaedah): E[maks(A, B)] > maks(E[A], E[B]), jadi skor setiap kaedah condong ke atas. Pilih lorong secara pra-komit (ikut backtest, atau satu lorong untuk semua) atau kenakan potongan ala-DSR dengan N = 2.
- Memilih 3–4 teratas daripada ~123 kaedah ialah keadaan winner's curse klasik; skor teratas dijangka merosot. Pengecutan sedia ada (+20 dagangan setara ke arah min global) betul dari segi arah, tetapi k = 20 tetap; empirical Bayes yang betul menganggar k = σ²_dalam ÷ τ²_antara daripada data (varians dalam-kaedah lawan varians sebenar antara kaedah), dan n sepatutnya n efektif (hari beli berbeza, bukan bilangan dagangan) kerana isyarat berkelompok pada hari sama.
- Dengan ~4,400 dagangan dalam ~10 sesi, n efektif setiap kaedah ≤ 10 hari beli; mana-mana ukuran keyakinan berasaskan bilangan dagangan (had bawah 95%, SQN mentah) terlebih yakin. Papan Penganalisis sudah guna n berkesan ikut hari beli; KPI "Skor kaedah swing" patut sejajar.
- Data hadapan 2 minggu hampir keseluruhannya satu rejim pasaran; nisbah sebenar/backtest pada peringkat ini kebanyakannya mengukur rejim (beta), bukan kemahiran kaedah. Lebihan SPY tempoh sama membantu, tetapi beta saham pilihan (selalunya > 1) masih mencemar; pertimbangkan lebihan berbanding purata berwajaran sama semua isyarat Lejar hari sama (penanda aras dalaman).

### Gaps
- Nilai R² khusus untuk volatiliti dan kejatuhan maksimum dalam Wiecki et al., dan kepentingan ciri model ML (termasuk nisbah ekor/kurtosis), tidak dapat disahkan — teks penuh disekat.
- Tiada kajian ditemui tentang kegigihan metrik peringkat dagangan (PF, kadar menang, SQN) khusus untuk strategi swing ekuiti peruncit.
- Kertas "Inference on Winners" (Andrews, Kitagawa, McCloskey) disebut secara tidak langsung oleh hasil carian tetapi URL/teks tidak diperoleh.

## S7. Ambang dan skala konkrit untuk memeta metrik kepada skor

### Takeaway
Ambang yang mempunyai sandaran sumber: SQN (1.6 / 2.0 / 2.5 / 3.0 / 5.0 / ≥ 7 curiga), statistik-t ≥ 2 untuk satu ujian dan ~3 bila banyak ujian, PSR/DSR ≥ 0.95, K-ratio ≥ 1 (versi 1996), nisbah ekor dan Omega > 1, ≥ 30 dagangan minimum (lebih baik ~100). Skor sebaiknya dibina daripada sedikit metrik tidak bertindih, dikira bersih kos, dengan n efektif, dan dipeta secara berterusan (bukan dipotong pada julat tetap yang tepu).

### Cited Findings
- SQN: 1.6–1.9 bawah purata; 2.0–2.4 purata; 2.5–2.9 baik; 3.0–5.0 cemerlang; 5.1–6.9 hebat; ≥ 7 Holy Grail — [QuantShare](https://www.quantshare.com/item-1541-system-quality-number-indicator); [Tradervue](https://www.tradervue.com/help/reports/report_stats); > 7 pada backtest = amaran curve-fit — [QuantMonitor](https://quantmonitor.net/system-quality-number-sqn/)
- SQN tidak boleh dipercayai < 30 dagangan; N dihadkan 100 — [Tradervue](https://www.tradervue.com/help/reports/report_stats)
- Tharp: 30–100 contoh sebelum jangkaan bermakna — [Bear Bull Traders](https://members.bearbulltraders.com/trading-to-the-power-of-r/)
- Harvey & Liu: p-nilai terlaras 0.05 ≈ t terlaras 2.0 dalam contoh mereka; t = 3.0 mungkin tidak mencukupi selepas ujian berbilang — [Harvey & Liu PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF); [Man Institute](https://www.man.com/insights/backtesting)
- K-ratio ≥ 1.0 (panduan AmiBroker) tetapi nilai bergantung versi formula — [AmiBroker guide](https://www.amibroker.com/guide/h_report.html); [The Systematic Trader](https://thesystematictrader.com/2013/04/coding-lars-kestners-k-ratio-in-excel/)
- Nisbah ekor > 1 baik — [TradesViz](https://www.tradesviz.com/glossary/tail-ratio/); Omega > 1 bermaksud untung berwajaran kebarangkalian melebihi rugi pada ambang θ — [Wikipedia Omega ratio](https://en.wikipedia.org/wiki/Omega_ratio)
- Kadar menang pulang modal = 1 ÷ (1 + nisbah bayaran) — [NexusFi](https://nexusfi.com/a/risk-management/trading-performance-metrics)

### Inferences
Cadangan set metrik dan skala (inferens penyelidik; perlu diuji pada data repo):
- **Kelebihan bersih (≈35%)**: purata pulangan % setiap dagangan BERSIH KOS, dikecutkan empirical Bayes ke arah min semua kaedah dengan k dianggar daripada data dan n = n efektif (hari beli berbeza); gabung dengan backtest sebagai prior (sudah dibuat dalam Papan Penganalisis). Skala: 0 mata pada ≤ 0%, penuh pada purata kaedah swing persentil ke-90 backtest (contoh, bukan angka bersumber).
- **Kecekapan modal (≈15%)**: Σr ÷ Σd × 21 (% sebulan setiap slot), termasuk posisi terbuka pada harga pasaran, atau guna hari pegang backtest sehingga matang. Ganti "untung sehari" semasa jika ia purata(r/d).
- **Keyakinan/kualiti (≈15%)**: satu sahaja — statistik-t kelompok-teguh (kelompok = tarikh beli) atau SQN dengan N = min(n efektif, 100); skala Tharp: 0 pada ≤ 1.0, 50 pada 2.0, 80 pada 3.0, 100 pada ≥ 5.0; tanda amaran (bukan bonus) jika > 7 pada backtest. Buang "had bawah 95%" sebagai metrik berasingan (bertindih).
- **Bentuk taburan (≈10%)**: SATU daripada PF/Omega(0) (skala 0 pada 1.0, penuh pada ~2.0 — ambang inferens) ATAU nisbah ekor (0 pada 0.8, penuh pada 1.5 — inferens). Buang kadar menang dan median daripada skor (papar sahaja).
- **Risiko laluan (≈15%)**: CVaR 5% dagangan (purata 5% terburuk) menggantikan "terburuk"; MAE purata dalam unit ATR14 menggantikan MAE %; untuk peringkat strategi gunakan Ulcer Index/MAR daripada backtest 2019–2026 (bukan 2 minggu hadapan).
- **Kekukuhan luar sampel (≈10%)**: bilangan semakan OOS lulus (S1–S4, WFO, AUTOTUNE) + nisbah sebenar/backtest hanya selepas kohort matang; tambah potongan pemilihan (ala-DSR) untuk pemilihan lorong terbaik dan untuk saiz carian 123 kaedah.
- Pemetaan: julat linear tetap yang dipotong (clip) tepu pada hujung dan menjadikan perbezaan kecil berhampiran sempadan besar; alternatif lebih stabil ialah pangkat persentil merentas kaedah layak atau z-skor dilaras (winsorise 5%/95%), yang tidak memerlukan pemilihan julat sewenang-wenang. Berat yang dijumlahkan pada metrik berkorelasi tinggi secara tersirat menggandakan berat faktor asas — semak matriks korelasi metrik merentas 123 kaedah sebelum memuktamadkan berat.
- Peraturan kelayakan: ≥ 20 dagangan selesai (semasa) terlalu rendah apabila dagangan berkelompok; tambah syarat ≥ 10 hari beli berbeza (sudah ada dalam Papan Penganalisis) dan lebih baik ≥ 30 dagangan matang sebelum skor "Teras".

### Gaps
- Ambang PF, nisbah ekor, Omega, CVaR dan pulangan sehari yang dicadang di atas TIDAK bersumber; ia titik permulaan untuk kalibrasi pada data backtest repo (cth. persentil merentas 431 set kaedah).
- Tiada sumber primer yang menetapkan berat optimum untuk skor komposit; berat di atas ialah inferens berdasarkan bukti S6 (Sharpe/purata lemah meramal; risiko dan OOS lebih stabil).
