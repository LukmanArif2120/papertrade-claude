# Gabungan 3–4 Kaedah dan Pemantauan Jangka Panjang (Inkubasi, Pemantauan, Persaraan)

Nota kaedah kerja: alat WebFetch dan curl disekat oleh proksi sesi ini (qoppac.blogspot.com, robotwealth.com, strategyquant.com dan papers.ssrn.com semuanya ditolak). Oleh itu, semua dapatan di bawah diambil daripada ringkasan hasil WebSearch yang memetik halaman sumber, bukan bacaan teks penuh. Angka yang perlu disemak dengan teks asal ditandakan "(perlu semak teks asal)". Pengiraan matematik dalam bahagian Inferences ialah kiraan saya sendiri.

## 1. Cara mengukur kepelbagaian antara kaedah: korelasi pulangan, pertindihan saham, atau pertindihan masa isyarat; ambang yang digunakan; bilangan kaedah yang mencukupi

### Takeaway
Amalan rujukan (StrategyQuant, Build Alpha, Carver) mengukur kepelbagaian dengan korelasi siri untung/rugi (P/L) atau pulangan mark-to-market harian/mingguan bagi setiap strategi. Pertindihan saham ialah proksi kasar yang terlepas pandang beta pasaran yang dikongsi. Tiada sumber primer yang ditemui menetapkan ambang 0.5 atau 0.7. Bagi kaedah long-only, faedah kepelbagaian 3–4 kaedah adalah kecil apabila korelasinya ≥ 0.5.

### Cited Findings
- StrategyQuant (ciri "Fit strategy to existing portfolio", sejak Build 130): pengguna menetapkan "maximum allowed correlation", dan strategi baharu dibuang jika korelasinya dengan mana-mana strategi dalam databank "Existing portfolio" melebihi had itu. Pengguna memilih jenis korelasi, iaitu P/L harian, bulanan, dan sebagainya. Nilai had ditentukan pengguna, bukan nilai lalai yang disyorkan. — [StrategyQuant doc](https://strategyquant.com/doc/strategyquant/fit-strategy-to-existing-portfolio/)
- QuantAnalyzer (StrategyQuant) mengira korelasi atas P/L, iaitu jumlah untung/rugi semua dagangan yang ditutup dalam satu tempoh. Ia juga boleh mengira korelasi atas bilangan posisi dan bilangan dagangan, dan ada pilihan untuk mengabaikan hari bernilai sifar semasa mengira korelasi. Pilihan ini penting bagi strategi yang jarang berdagang. — [StrategyQuant QuantAnalyzer](https://strategyquant.com/doc/quantanalyzer/portfolio-correlation-explained/)
- Build Alpha memaparkan matriks korelasi antara strategi menggunakan pulangan harian mark-to-market untuk membina portfolio strategi yang tidak berkorelasi. Tiada penapis ambang automatik yang didokumenkan. — [Build Alpha Features](https://www.buildalpha.com/buildalpha-features/)
- Carver: pengganda kepelbagaian (diversification multiplier, DM) dikira daripada matriks korelasi pulangan dan pemberat. Contoh: dua aset dengan volatiliti 10% dan korelasi 0.5 menghasilkan volatiliti portfolio 8.66%, manakala korelasi 0 menghasilkan 7.07%. Carver mengesyorkan DM dihadkan pada 2.5. — [qoppac: Correlations, Weights, Multipliers](https://qoppac.blogspot.com/2016/01/correlations-weights-multipliers.html) (melalui ringkasan carian)
- Carver: purata korelasi antara peraturan dagangan yang berbeza pada instrumen yang sama lebih tinggi daripada korelasi antara instrumen berbeza yang memakai peraturan yang sama. Implikasinya, kepelbagaian datang terutamanya daripada sumber pulangan/aset yang berbeza, bukan daripada variasi peraturan. — [qoppac 2016](https://qoppac.blogspot.com/2016/01/correlations-weights-multipliers.html) (ringkasan carian; perlu semak teks asal)
- Carver: korelasi boleh dianggarkan daripada backtest subsistem dagangan atau daripada "rules of thumb". Anggaran sisihan piawai dan korelasi jauh lebih stabil berbanding anggaran Sharpe. — [CXO Advisory, nota Systematic Trading](https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading)
- Dalio ("Holy Grail"): 15 aliran pulangan yang baik dan tidak berkorelasi menghapuskan kira-kira 80% risiko, iaitu nisbah pulangan/risiko meningkat kira-kira 5 kali. Sumber lain memetik 10–15 atau 15–20 aliran. Andaian asasnya ialah aliran itu benar-benar tidak berkorelasi. — [Yahoo Finance](https://finance.yahoo.com/news/billionaire-ray-dalio-offers-fresh-tips-on-how-to-be-a-better-investor-161649242.html); [Summify, video Dalio](https://summify.io/discover/ray-dalio-the-one-rule-that-cuts-investment-risk-by-80-Uprafh/)
- Korelasi antara aset cenderung meningkat semasa krisis, lalu kepelbagaian tradisional menjadi kurang berkesan. — [Daily Maverick](https://www.dailymaverick.co.za/opinionista/2019-04-26-benefits-and-problems-of-a-diversified-portfolio/)
- Carian khusus tidak menemui sumber Build Alpha atau StrategyQuant yang mengesyorkan ambang 0.5 atau 0.7. — (hasil carian negatif; lihat Gaps)

### Inferences
- Kiraan saya untuk portfolio N kaedah berpemberat sama, risiko sama dan purata korelasi ρ. Formulanya σ_p/σ = √(1/N + (1−1/N)ρ) dan DM = 1/(σ_p/σ). Sharpe gabungan ≈ Sharpe individu × DM jika Sharpe setiap kaedah sama.
  - ρ = 0: N=2 → DM 1.41; N=3 → 1.73; N=4 → 2.00
  - ρ = 0.3: N=2 → 1.24; N=3 → 1.37; N=4 → 1.45; N=10 → 1.64; N tak terhingga → 1.83
  - ρ = 0.5: N=2 → 1.15; N=3 → 1.22; N=4 → 1.26; N=10 → 1.35; N tak terhingga → 1.41
  - ρ = 0.7: N=2 → 1.08; N=4 → 1.14; N tak terhingga → 1.19
  - ρ = 0.8: N=4 → 1.08
  - Pada ρ = 0.5, 4 kaedah sudah mencapai kira-kira 71% daripada pengurangan volatiliti maksimum yang mungkin, iaitu (1−0.791)/(1−0.707). Kaedah ke-5 dan seterusnya menambah sangat sedikit. Pada ρ ≥ 0.7, gabungan hampir tidak mengurangkan risiko, dan nilai gabungan hanya datang daripada purata alpha.
- Semua kaedah long-only saham AS berkongsi beta pasaran. Korelasi pulangan harian mark-to-market antara kaedah swing long-only dijangka tinggi (anggaran 0.5–0.9; perlu diukur dengan data Lejar Penuh). Akibatnya, ambang "korelasi < 0.5" mungkin sukar dicapai. Pilihan praktikal ialah mengira korelasi atas pulangan berlebihan terhadap SPY (pulangan − β×SPY) di samping korelasi mentah.
- Peraturan semasa "pertindihan saham ≤ 20% dalam ±5 hari" mengukur pertindihan nama, bukan pertindihan risiko. Dua kaedah boleh membeli saham berbeza tetapi kedua-duanya membeli selepas penurunan pasaran yang sama (masa isyarat bertindih), lalu pulangan hariannya sangat berkorelasi. Cadangan:
  - Ukuran A: korelasi pulangan harian/mingguan bagi portfolio maya setiap kaedah (Lejar Penuh, pemberat sama per posisi terbuka).
  - Ukuran B: korelasi kiraan isyarat harian, iaitu bilangan belian per hari.
  - Ukuran C: pertindihan saham yang sedia ada.
  - Gunakan A sebagai kriteria utama, dan B dan C sebagai pemeriksaan sekunder.
- Kerana hari tanpa dagangan memberi nilai sifar, korelasi P/L harian bagi kaedah yang jarang berisyarat boleh terherot. Ini sebab QuantAnalyzer menyediakan pilihan "ignore zero days". Korelasi mingguan lebih stabil bagi kaedah swing dengan pegangan 3–30 hari.

### Gaps
- Tiada sumber primer ditemui yang memberi ambang korelasi piawai (0.5 / 0.7) bagi portfolio strategi. Ambang dalam StrategyQuant ditentukan pengguna.
- Tiada data empirikal ditemui tentang korelasi tipikal antara strategi swing long-only saham AS.
- Jadual DM Carver mengikut bilangan peraturan dalam buku (Systematic Trading) tidak dapat dibaca terus.

## 2. Algoritma pemilihan dan peruntukan: greedy ikut skor dengan had korelasi, HRP, kelemahan mean-variance, pemberat sama vs risk parity, kaedah handcrafting Carver

### Takeaway
Bukti akademik yang kukuh (DeMiguel et al. 2009, "forecast combination puzzle") menunjukkan pemberat optimum hasil anggaran jarang mengalahkan pemberat sama di luar sampel kerana ralat anggaran. Carver juga mengesyorkan pemberat sama atau handcrafting berasaskan korelasi, bukan pengoptimuman Sharpe. HRP mengurangkan varians luar sampel berbanding pengoptimum kuadratik, tetapi tidak semestinya meningkatkan pulangan. Bagi 3–4 kaedah, pemberat sama (atau pemberat sama risiko) ialah pilihan lalai yang munasabah.

### Cited Findings
- DeMiguel, Garlappi dan Uppal (RFS 2009) menguji 14 model atas 7 set data. Tiada model yang secara konsisten mengalahkan peraturan 1/N dari segi Sharpe, certainty-equivalent atau turnover, kerana ralat anggaran menghapuskan faedah pengoptimuman. Bagi 25 aset, tetingkap anggaran yang diperlukan supaya mean-variance menang adalah kira-kira 3000 bulan, dan kira-kira 6000 bulan bagi 50 aset. — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rfinst/v22y2009i5p1915-1953.html); [LBS](https://london.edu/faculty-and-research/academic-research/o/optimal-versus-naive-diversification-how-inefficient-is-the-1n-portfolio-strategy-p7805)
- "Forecast combination puzzle" (istilah Stock dan Watson 2004): purata berpemberat sama kerap mengalahkan pemberat "optimum" yang dianggarkan. Smith dan Wallis (2009) menjelaskannya dengan ralat anggaran sampel terhingga bagi pemberat. Apabila pesaing banyak, purata menukar sedikit bias dengan varians anggaran yang jauh lebih kecil. — [Lee & Lee, UCR WP](https://webarchive.ucr.edu/economics.ucr.edu/repec/ucr/wpaper/202514.pdf); [Chan et al., MODSIM 2015](https://www.mssanz.org.au/modsim2015/E5/chan.pdf)
- Elliott dan Liao: keuntungan daripada gabungan optimum boleh jadi kecil dalam keadaan realistik. Apabila keuntungannya besar, membuang sebahagian ramalan lalu mengambil purata yang selebihnya berprestasi lebih baik. — [Elliott & Liao, UCSD](https://econweb.ucsd.edu/~gelliott/Combination.pdf)
- Qian, Rolling, Cheng dan Yang (Econometrics 2019): punca teka-teki itu termasuk varians tinggi dalam anggaran pemberat dan penapisan model calon sebelum digabungkan. — [DOAJ](https://doaj.org/article/f822f1fec1fd4fa8910b85bbb692dd52)
- Handcrafting Carver ialah proses bawah ke atas:
  1. Kumpulkan aset/strategi yang serupa (berkorelasi tinggi dalam kumpulan, rendah antara kumpulan).
  2. Peruntukan dalam kumpulan.
  3. Peruntukan antara kumpulan.
  4. Darabkan kedua-dua pemberat itu.
  Pemberat diambil daripada jadual hasil eksperimen bootstrap. — [GitHub awesome-quant-ai, ringkasan buku](https://github.com/leoncuhk/awesome-quant-ai/blob/main/book/Systematic%20Trading%20A%20unique%20new%20method%20for%20designing%20trading%20and%20investing%20systems.md); [CXO Advisory](https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading)
- Contoh handcrafting: kumpulan diberi pemberat sama, kemudian dibahagi sama rata dalam kumpulan (50% bon AS, 25% saham UK, 25% saham AS). Ini pemberat risiko, bukan pemberat tunai. — [7 Circles](https://the7circles.uk/systematic-trading-2-fitting-and-allocation/)
- Carver (pendekatan matriks calon, 3 aset): bagi korelasi 0.5 pada satu pasangan dan 0 pada dua pasangan lain, pemberat mentah ialah kira-kira 0.286 / 0.428 / 0.286. Aset yang tidak berkorelasi dengan kedua-dua aset lain mendapat pemberat lebih. — [qoppac 2020: Improving the use of correlations in handcrafting](https://qoppac.blogspot.com/2020/11/improving-use-of-correlations-in.html) (perlu semak teks asal; susunan lajur tidak pasti)
- Dalam Smart Portfolios, Carver mengandaikan pulangan larasan risiko yang sama bagi semua aset, menskala posisi ikut volatiliti, dan menggunakan handcrafting untuk korelasi. Sebabnya, anggaran Sharpe sangat bising manakala anggaran sisihan piawai dan korelasi lebih pasti. Bagi pedagang separa automatik, Carver mencadangkan pemberat instrumen yang sama dengan ambang imbang semula 10%. — [CXO Advisory](https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading)
- Carver menetapkan pemberat ramalan (forecast weights) berdasarkan ketidakpastian anggaran Sharpe. Peraturan yang lemah mendapat pemberat lebih rendah tetapi jarang dikeluarkan sepenuhnya. Pemberat berjumlah 1 dan tiada yang negatif. — [Thread ReformedTrader, ringkasan Systematic Trading](https://threadreaderapp.com/thread/1234306875379683328.html) (sumber sekunder)
- HRP (López de Prado, JPM 2016) diperkenalkan untuk menangani ketidakstabilan, penumpuan dan prestasi lemah pengoptimum kuadratik ("Markowitz's curse"). Dalam eksperimen Monte Carlo, HRP memberi varians luar sampel lebih rendah berbanding CLA (critical line algorithm), walaupun varians minimum ialah objektif CLA sendiri, dan portfolionya kurang berisiko berbanding risk parity tradisional. — [SSRN 2708678](https://papers.ssrn.com/abstract=2708678); [Wikipedia: HRP](https://en.wikipedia.org/wiki/Hierarchical_Risk_Parity)
- Tesis CBS: HRP mencapai varians luar sampel lebih rendah dalam Monte Carlo berbanding min-variance, ERC, IVP dan 1/N. Namun HRP kurang teguh terhadap salah spesifikasi matriks kovarians sampel. — [Tesis CBS](https://research-api.cbs.dk/ws/portalfiles/portal/76452070/1332322_Master_Thesis_Hierarchical_Risk_Parity.pdf)
- Ujian bebas di pasaran Brazil: HRP bukan yang terbaik, dan setara dengan kaedah lain pada sesetengah ukuran (walaupun mengalahkan indeks). Perkataan "outperform" dalam tajuk kertas asal merujuk terutamanya kepada risiko dan kestabilan. — [RBFin (FGV)](https://periodicos.fgv.br/rbfin/article/download/89848/84802/201368)
- Memilih isyarat terbaik daripada banyak calon meninggikan prestasi backtest melalui overfitting dan bias pemilihan. — [NBER w21329, Backtesting strategies based on multiple signals](https://www.nber.org/system/files/working_papers/w21329/w21329.pdf)

### Inferences
- Dengan hanya 3–4 kaedah, struktur hierarki HRP hampir tidak bermakna (pokok kelompok terlalu kecil). Kelebihan HRP muncul dengan banyak aset. Pilihan praktikal ialah 1/N, atau pemberat sama risiko (songsang volatiliti) jika volatiliti pulangan kaedah sangat berbeza.
- Algoritma greedy semasa (skor ≥ 55%, had pertindihan, maksimum 4) serupa dengan "had korelasi + pemilihan ikut skor" dalam StrategyQuant. Risikonya ialah bias pemilihan: kaedah berskor tertinggi daripada 123 kaedah dipilih atas backtest yang sama (lihat Bahagian 6). Pembaikan yang selaras dengan sumber:
  - (a) Gunakan korelasi pulangan, bukan sekadar pertindihan saham.
  - (b) Beri pemberat sama kepada kaedah terpilih, bukan pemberat ikut skor.
  - (c) Gunakan "membuang beberapa, kemudian purata yang selebihnya" (Elliott & Liao) sebagai justifikasi falsafah untuk memilih subset kecil dan memberinya pemberat sama.
- Variasi handcrafting yang praktikal untuk 123 kaedah: kumpulkan kaedah mengikut keluarga isyarat, contohnya momentum/breakout, mean-reversion/pullback dan RS (berdasarkan korelasi pulangan Lejar Penuh). Pilih 1 kaedah terbaik setiap kumpulan supaya 3–4 kaedah datang daripada kumpulan berbeza. Ini setara dengan "group first, then allocate".

### Gaps
- Jadual pemberat handcrafting penuh Carver (Table 8 dalam Systematic Trading) tidak dapat dibaca.
- Angka varians luar sampel HRP/CLA/IVP dalam kertas asal tidak dapat disahkan (laman SSRN disekat).
- Tiada kajian ditemui yang membandingkan secara khusus pemberat sama vs HRP untuk portfolio strategi dagangan (berbanding portfolio aset).

## 3. Inkubasi / ujian hadapan: tempoh dan bilangan dagangan sebelum "live"; mengelak bias pandangan belakang dengan membekukan pilihan

### Takeaway
Kevin Davey menginkubasi strategi dalam dagangan kertas masa nyata selama 6–12 bulan menurut kebanyakan ringkasan (ada sumber menyebut 3–6 atau 6–9 bulan). Peraturan berhenti ditulis sebelum strategi dijalankan. Bagi kaedah swing, kiraan bilangan dagangan atau hari belian berbeza lebih bermakna daripada tempoh kalendar. Ketidakpastian Sharpe bermakna inkubasi hanya menapis kegagalan besar, bukan membuktikan kelebihan.

### Cited Findings
- Davey: selepas lulus walk-forward dan Monte Carlo, strategi dipantau dalam pasaran sebenar tanpa wang selama 6–12 bulan untuk mendedahkan slippage, komisen dan anomali data yang tidak ditangkap backtest. Menurut ringkasan yang sama, 85–90% pelajarnya mengatakan inkubasi membantu mengelak strategi buruk atau mengesahkan strategi baik. — [Algo Advantage 036, Kevin Davey Part I](https://algoadvantage.substack.com/p/036-kevin-davey-part-i-its-all-about)
- Ringkasan lain menyebut dagangan kertas masa nyata "sering 6 hingga 9 bulan". — [Algo Advantage 037, Kevin Davey II](https://algoadvantage.substack.com/p/037-kevin-davey-ii-selecting-optimal)
- Satu lagi ringkasan menyebut inkubasi lazimnya 3 atau 6 bulan dan bersifat wajib. — [FinancialWisdomTV](https://www.financialwisdomtv.com/post/building-winning-algorithmic-trading-systems-kevin-davey-s-complete-framework-for-trading-success)
- Davey mengesyorkan walk-forward sekali sahaja. Menguji semula parameter in-sample berulang kali ialah overfitting yang merosakkan keputusan luar sampel. — [Algo Advantage 036/037](https://algoadvantage.substack.com/p/037-kevin-davey-ii-selecting-optimal) (ringkasan carian)
- Garis panduan dagangan kertas am: sasarkan bilangan dagangan tertutup, bukan minggu (sering disebut 30–100 dagangan bergantung pada varians strategi). Ada sumber yang menuntut sekurang-kurangnya 100 dagangan berjurnal bagi satu setup. Isian (fill) kertas cenderung optimistik. — [LuxAlgo: forward/paper-trading confirmation](https://www.luxalgo.com/library/concept/forward-paper-trading-confirmation/); [Tradingsim](https://www.tradingsim.com/blog/how-long-to-paper-trade) (sumber vendor/pendidikan, lemah; atribusi angka antara kedua-duanya daripada ringkasan carian)
- Ernie Chan mencari Sharpe > 1 sebelum berdagang secara live. Maksimum drawdown kurang penting kerana bergantung pada leveraj. — [epchan blog: Life and death of a strategy](http://epchan.blogspot.com/2012/04/life-and-death-of-strategy.html) (komen Chan di blog; melalui ringkasan carian)
- Carver: dua peraturan tidak berkorelasi dengan Sharpe 0.05 dan 0.30 pada satu instrumen memerlukan kira-kira 45 tahun data untuk dibezakan secara statistik. Pada portfolio instrumen (Sharpe 0.13 vs 1.13), kira-kira 11 tahun diperlukan. — [Thread ReformedTrader, petikan Systematic Trading](https://threadreaderapp.com/thread/1234306875379683328.html)
- Carver: walaupun dengan 20 tahun data, Sharpe 0.5 belum cukup bukti statistik untuk dikatakan positif. — [ReSolve: Rob Carver, Uncertainty Principles](https://investresolve.com/podcasts/rob-carver-uncertainty-principles/)
- Kedudukan dana ikut Sharpe 1–2 tahun sering menghasilkan prestasi buruk selepas itu (Sharpe tidak berterusan). — [The Hedge Fund Journal: The Myth of Persistent Sharpe Ratio](https://thehedgefundjournal.com/the-myth-of-persistent-sharpe-ratio/)
- McLean dan Pontiff (97 peramal pulangan): pulangan portfolio 26% lebih rendah di luar sampel dan 58% lebih rendah selepas penerbitan. — [SSRN 2156623](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623)
- Harvey dan Liu ("Backtesting"): potongan Sharpe 50% ialah rule of thumb industri. Kertas mereka membangunkan kaedah analitik di mana potongan bergantung pada bilangan ujian ("semakin banyak strategi dicuba, semakin besar potongannya"). — [Harvey & Liu, Duke](https://people.duke.edu/~charvey/Media/2016/Practical_applications_backtesting.pdf); [Harvey, Evaluating Trading Strategies](https://www.stat.berkeley.edu/~aldous/157/Papers/harvey.pdf)

### Inferences
- Kiraan saya (ralat piawai jangkaan per dagangan = sd/√n; sasaran t ≈ 2): jika pulangan per dagangan swing mempunyai sd ≈ 8% dan jangkaan 1%, kira-kira 256 dagangan bebas diperlukan. Pada jangkaan 0.5%, kira-kira 1,000 dagangan diperlukan. Pada sd 6% dan jangkaan 1%, kira-kira 144 dagangan.
- Isyarat yang dibeli pada hari yang sama tidak bebas (beta pasaran dikongsi). Maka "n berkesan" lebih hampir kepada bilangan hari belian berbeza atau minggu. Ini selaras dengan peraturan papan semasa (BELUM CUKUP < 10 hari belian berbeza), tetapi 10 hari jauh daripada cukup untuk pembuktian. 10 hari hanya sesuai sebagai lantai paparan, bukan kriteria pemilihan.
- Cadangan protokol inkubasi gabungan:
  - (1) Bekukan set 3–4 kaedah yang dipilih pada tarikh T, beserta peraturan pemberat, peraturan slot dan peraturan berhenti, dan rekodkan dalam fail bertarikh (commit).
  - (2) Jejaki portfolio gabungan beku itu ke hadapan, serupa dengan `portfolio_slot/` RS_10 vs RAWAK_10 sedia ada. Bandingkan dengan (a) kaedah tunggal berskor tertinggi, (b) gabungan rawak 4 kaedah daripada kaedah yang lulus skor ≥ 55%, dan (c) SPY.
  - (3) Tempoh minimum kira-kira 6 bulan atau kira-kira 100–250 dagangan dengan ≥ 40–60 hari belian berbeza, mana-mana yang lebih lewat. Tujuannya mengesan kegagalan besar dan masalah pelaksanaan, bukan membuktikan alpha.
- Jangkakan prestasi hadapan lebih rendah daripada backtest. Potongan 26% (McLean-Pontiff, luar sampel) hingga 50% (rule of thumb Harvey-Liu) sesuai sebagai "band jangkaan". Bias pemilihan daripada 123 kaedah menuntut potongan di hujung atas julat ini.

### Gaps
- Teks asal buku Davey tentang bilangan dagangan minimum semasa inkubasi tidak dapat dibaca. Ringkasan sekunder memberi julat bulan yang bercanggah (3–6, 6–9, 6–12).
- Tempoh dagangan kertas minimum menurut Ernie Chan tidak ditemui.
- Tiada sumber yang khusus untuk inkubasi kaedah swing saham (kebanyakan sumber berasaskan niaga hadapan).

## 4. Pemantauan dan persaraan: jangkaan bergulir vs band keyakinan backtest, kill switch berasaskan drawdown, CUSUM/SPRT, kesedaran rejim (SPY vs MA200), kekerapan rotasi

### Takeaway
Pengamal bersetuju bahawa peraturan berhenti mesti ditulis lebih awal. Bentuk yang biasa ialah drawdown melebihi ambang Monte Carlo atau melebihi 1.2–1.5× DD maksimum backtest, jangka masa drawdown melebihi maksimum backtest (Chan), dan ekuiti jatuh di bawah kon kebarangkalian (Davey). Ujian statistik seperti t-test lambat. CUSUM ialah pengesan perubahan terpantas pada kadar penggera palsu tetap, tetapi masih memerlukan berpuluh bulan. Penapis rejim MA200 terutamanya mengurangkan drawdown, bukan meningkatkan pulangan.

### Cited Findings
- Davey: idealnya, keputusan bila hendak berhenti ditentukan semasa memutuskan untuk mendagangkan sistem. Pencetus berhenti termasuk drawdown maksimum, bilangan kerugian berturut-turut, dan jumlah rugi seminggu/sebulan/setahun. Syarat tepat yang dipilih kurang penting berbanding menulisnya dan mematuhinya. — [kjtradingsystems: How and when to quit an algo trading system](https://kjtradingsystems.com/when-to-quit-trading.html)
- Davey: gunakan simulasi Monte Carlo, iaitu mengocok hasil dagangan beribu kali, dan tetapkan kriteria berhenti berdasarkan hasil terburuk taburan itu, bukan satu drawdown sejarah. Jika lengkung ekuiti jatuh di bawah jalur bawah kon kebarangkalian, sistem mungkin rosak atau pasaran berubah, dan mungkin wajar berhenti. Pedagang konservatif berhenti pada garisan putus-putus merah yang lebih tinggi. — [kjtradingsystems: Monte Carlo probability cones](https://kjtradingsystems.com/monte-carlo-probability-cones.html)
- Davey: penimbal seperti 1.5× atau 1.2× drawdown maksimum backtest sebelum menilai semula atau berhenti. Davey: "I'd rather quit too early than quit too late." — [kjtradingsystems: when to quit](https://kjtradingsystems.com/when-to-quit-trading.html) (daripada transkrip video; atribusi halaman tepat melalui ringkasan carian)
- Davey (BST Live, Okt 2020): satu lengkung ekuiti memberi gambaran tidak lengkap. Anggarkan julat prestasi masa depan, dan gunakan kawalan proses statistik (SPC) dan kon kebarangkalian untuk mengesan sistem yang rosak. — [Better System Trader ep. 170](https://sites.libsyn.com/66295/170-how-to-detect-when-a-trading-strategy-is-failing-kevin-davey)
- Ernie Chan: jika tiada sebab yang jelas untuk penurunan, dan drawdown lebih lama daripada jangka masa drawdown maksimum dalam backtest, kurangkan leveraj secara drastik. — [epchan: Life and death of a strategy](http://epchan.blogspot.com/2012/04/life-and-death-of-strategy.html)
- Chan mengesyorkan henti rugi peringkat sistem bagi strategi mean-reversion, ditetapkan melebihi drawdown sejarah maksimum backtest. — [Better System Trader 012, Ernie Chan](https://bettersystemtrader.com/012-ernest-chan/)
- Robot Wealth: t-test ialah alat yang lemah untuk memutuskan sama ada strategi berhenti berfungsi. Satu tempoh buruk yang singkat tidak dapat membuktikan secara statistik bahawa kelebihan sudah hilang (simulasi strategi 10% setahun yang jatuh ke sifar selama sebulan). — [IBKR Quant / Robot Wealth](https://www.interactivebrokers.com/campus/ibkr-quant-news/why-you-cant-tell-if-your-strategy-stopped-working-statistically-speaking/)
- Euan Sinclair: menunggu keertian statistik sebelum bertindak atas perubahan rejim sering bermakna bertindak terlalu lewat. — [Robot Wealth Edge Alchemy: Statistically Significant and Chronically Late](https://edgealchemy.robotwealth.com/p/statistically-significant-and-chronically)
- Philips ("Monitoring Active Portfolios: The CUSUM Approach"): CUSUM boleh mengesan prestasi yang mendatar berbanding penanda aras dalam kira-kira 40 bulan, dan prestasi lebih buruk dengan lebih cepat. Pada kadar penggera palsu tetap, CUSUM ialah cara terpantas mengesan perubahan prestasi (Moustakides 1986). Kuasanya serupa dengan ujian berjujukan Wald (SPRT) apabila pulangan berlebihan malar. Premisnya, alpha dan tracking error sukar dipisahkan daripada nasib dan tidak pegun. — [Philips, Northern Information (PDF)](https://www.northinfo.com/Documents/144.pdf)
- Pengamal menggandingkan CUSUM (sesuai untuk hanyutan beransur) dengan regresi alpha bergulir, t-test dua sampel backtest vs live, dan ujian nisbah varians. — [Breaking Alpha](https://breakingalpha.io/insights/alpha-decay-detection-purchased-trading-strategies) (sumber gambaran am, bukan kajian)
- StrategyQuant menyediakan snippet "what-if" yang menghentikan dagangan apabila ambang drawdown yang diukur dalam data validasi dicapai. — [StrategyQuant blog](https://strategyquant.com/ja/blog/evaluating-the-trading-performance-of-strategies/) (melalui ringkasan carian)
- Faber (10-month SMA, S&P 500 1900–2005): pulangan setara ekuiti dengan risiko lebih rendah berbanding beli-dan-pegang, dengan pelaburan kira-kira 70% masa. — [Faber, SSRN 962461 (PDF)](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf)
- Ujian semula peraturan 10 bulan Faber pada SPY (33 tahun, 23 dagangan) memberi 9.2%/tahun selepas kos vs 10.8% beli-dan-pegang, dengan DD terburuk 25.6% vs 55.2%. Kemasukan rawak dengan tempoh pegangan sama hampir menyamai pulangannya (p = 0.32). — [Empiricalab Substack](https://empiricalab.substack.com/p/faber-10-month-average)
- SPY di atas MA200: volatiliti tahunan 13.81% vs 29.93% di bawahnya, dan pulangan tahunan kira-kira 11% vs 8.6%. — [Free Market Speculator](https://freemarketspeculator.substack.com/p/the-200-day-line-in-the-sand)
- Strategi MA200 pada S&P 500: CAGR 6.75% vs 7% beli-dan-pegang, DD maksimum 28% vs 56%. — [QuantifiedStrategies](https://www.quantifiedstrategies.com/200-day-moving-average/)

### Inferences
- Peraturan persaraan berlapis untuk kaedah dalam gabungan (cadangan; ditulis dan dibekukan sebelum bermula):
  - (1) Amaran: jangkaan bergulir (contohnya 60 dagangan atau 20 hari belian terakhir) jatuh di bawah persentil ke-5 taburan bootstrap jangkaan backtest bagi saiz sampel yang sama. Ini versi kon kebarangkalian Davey.
  - (2) Gantung (tiada belian baharu, kekal dalam jejak kertas): DD kaedah > 1.5× DD maksimum backtest atau > persentil ke-95 DD Monte Carlo, ATAU jangka masa DD > jangka masa DD maksimum backtest (Chan).
  - (3) Bersara: CUSUM satu hala atas pulangan per dagangan (sasaran = jangkaan backtest selepas potongan kira-kira 50%; penurunan = jangkaan sifar) melepasi ambang h yang ditetapkan untuk kadar penggera palsu kira-kira 1 kali/2 tahun.
  - Kaedah yang digantung terus dijejaki dalam Lejar Penuh supaya boleh dipulihkan jika prestasi kembali.
- Kerana ujian statistik lambat (Robot Wealth, Philips kira-kira 40 bulan), peraturan drawdown/jangka masa berfungsi sebagai brek risiko, bukan bukti. Kombinasi "lambat untuk masuk, cepat untuk gantung" selaras dengan Davey ("quit too early").
- Kesedaran rejim: bukti MA200 kebanyakannya pada indeks, dan manfaatnya ialah DD lebih kecil dengan pulangan hampir sama atau sedikit lebih rendah. Bagi gabungan swing, rejim lebih sesuai digunakan sebagai pemboleh ubah pelaporan, iaitu prestasi setiap kaedah dipecahkan kepada SPY > MA200 vs < MA200, dan bukan sebagai penapis tambahan. Ini kerana penapis tambahan menambah satu lagi darjah kebebasan yang boleh overfit. Jika digunakan, pilih satu peraturan tetap (contohnya SPY tutup < MA200 → separuh saiz/slot) dan bekukan.
- Kekerapan rotasi: Sharpe 1–2 tahun tidak berterusan (Hedge Fund Journal), dan perbezaan Sharpe kecil memerlukan berpuluh tahun untuk dibuktikan (Carver). Maka penilaian semula set gabungan wajar dibuat jarang, contohnya suku tahunan, dengan histeresis: kaedah baharu hanya menggantikan kaedah sedia ada jika skornya lebih tinggi dengan margin besar DAN kaedah sedia ada mencetuskan peraturan gantung/bersara. Pertukaran setiap minggu atau bulan berdasarkan skor akan mengejar bunyi rawak.

### Gaps
- Nilai ambang h CUSUM yang khusus untuk pulangan dagangan swing tidak ditemui. Ia perlu dikalibrasi melalui simulasi atas data Lejar Penuh.
- Tiada sumber yang menguji penapis MA200 pada strategi swing saham individu long-only (semua bukti di peringkat indeks, dan kebanyakannya blog).
- Kandungan "6 ways to detect a failing trading strategy" (Davey) tidak dapat dibaca sepenuhnya.

## 5. Kapasiti dan pelaksanaan: apabila gabungan kaedah menghasilkan terlalu banyak isyarat untuk modal terhad

### Takeaway
Sumber pengamal hanya bersetuju bahawa backtest berbilang strategi dengan slot terhad mesti mempunyai peraturan eksplisit tentang isyarat mana yang mendapat slot. Andaian modal tanpa had meninggikan keputusan. Tiada algoritma piawai ditemui.

### Cited Findings
- MultiCharts: isyarat perlu diberi keutamaan kerana wang dalam akaun tidak cukup untuk semua order. Contoh peraturan keutamaan ialah membeli instrumen termurah dahulu atau mengisi order saham sebelum niaga hadapan. — [MultiCharts Portfolio Trader](https://www.multicharts.com/features/portfolio-trading/)
- Apabila dua strategi mahu posisi pada masa yang sama, tentukan lebih awal cara modal dibahagikan. Backtest yang mengandaikan modal tanpa had bagi setiap strategi melebih-lebihkan keputusan. — [TradersJournal: Portfolio backtesting](https://tradersjournal.app/blog/portfolio-backtesting)
- Pendekatan biasa dalam portfolio berbilang saham ialah peruntukan berasaskan kedudukan (ranking): skor numerik menentukan susunan dan saiz dana. — [arXiv 2408.06361 (tinjauan LLM trading agents)](https://arxiv.org/pdf/2408.06361)
- Forum AmiBroker membincangkan backtest beberapa sistem berkongsi modal dan bilangan posisi maksimum, tetapi tiada penyelesaian muktamad (kira-kira 9 tahun lalu). — [AmiBroker forum](https://forum.amibroker.com/t/backtesting-two-or-more-strategies-simultaneously/795)
- Carver (pedagang separa automatik): pemberat instrumen yang sama dengan ambang imbang semula 10%. — [CXO Advisory](https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading)

### Inferences
- Bagi kira-kira 150 isyarat seminggu dan slot terhad, pilihan paling selaras dengan prinsip pemberat sama ialah kuota slot setiap kaedah (contohnya 10 slot ÷ 4 kaedah ≈ 2–3 slot setiap kaedah, dengan slot yang tidak digunakan dikongsi). Kuota ini menghalang satu kaedah yang paling kerap berisyarat daripada memonopoli modal, iaitu bentuk pemberat tersirat yang tidak dirancang.
- Dalam kuota setiap kaedah, susunan isyarat boleh mengikut RS pasaran (seperti RS_10 dalam `portfolio_slot/`). Kawalan RAWAK_10 sedia ada ialah reka bentuk yang betul untuk menguji sama ada peraturan keutamaan menambah nilai.
- Portfolio slot terhad hanya mengambil sebahagian kecil isyarat. Maka jangkaan hadapan portfolio sebenar akan berbeza daripada jangkaan "semua isyarat" Lejar Penuh. Pemantauan Bahagian 4 perlu dijalankan pada kedua-dua peringkat: kaedah (Lejar Penuh) dan portfolio gabungan (slot).

### Gaps
- Tiada sumber akademik atau pengamal utama yang ditemui tentang peruntukan slot optimum merentas strategi untuk saham swing.

## 6. Bukti: adakah gabungan kaedah berskor tertinggi mengalahkan kaedah tunggal terbaik di luar sampel?

### Takeaway
Bukti langsung yang khusus bercampur, tetapi bukti tidak langsung kuat menyokong gabungan. Pemenang in-sample tunggal kerap merosot di luar sampel (PBO, McLean-Pontiff, kajian 6,406 peraturan). Purata berpemberat sama kerap mengalahkan pemilihan atau pemberat optimum (forecast combination puzzle, DeMiguel). Gabungan dijangka mengurangkan varians dan risiko kegagalan satu kaedah, dan tidak semestinya memberi pulangan purata tertinggi.

### Cited Findings
- Bailey, Borwein, López de Prado dan Zhu memperkenalkan "Probability of Backtest Overfitting" (PBO) melalui CSCV untuk menganggarkan kebarangkalian strategi terbaik in-sample berada di bawah median di luar sampel. Teknik hold-out biasa tidak boleh dipercayai untuk backtest pelaburan. — [SSRN 2326253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)
- Varian "optimum" in-sample yang dipilih daripada banyak percubaan sering berprestasi sangat buruk di luar sampel kerana parameternya overfit. Prestasi tinggi boleh dicapai selepas menguji bilangan konfigurasi yang agak kecil. — [Bailey et al., Pseudo-Mathematics and Financial Charlatanism (PDF)](https://obj.portfolioconstructionforum.edu.au/articles_perspectives/Pseudo-mathematics-and-financial-charlatanism.pdf)
- Kajian 6,406 peraturan teknikal merentas 41 pasaran ekuiti: peraturan yang berprestasi terbaik baru-baru ini berprestasi jauh lebih buruk daripada beli-dan-pegang pada masa hadapan. — [ResearchGate: predictive ability of technical trading rules](https://www.researchgate.net/publication/374779667_The_predictive_ability_of_technical_trading_rules_an_empirical_analysis_of_developed_and_emerging_equity_markets)
- Hsu dan Kuan: strategi gabungan (learning, voting, fractional position) tidak memberi penambahbaikan signifikan berbanding peraturan mudah. Kertas PSO kemudian mendakwa gabungannya mengalahkan semua peraturan komponen dalam tempoh ujian. — [ScienceDirect: Combining technical trading rules using PSO](https://www.sciencedirect.com/science/article/abs/pii/S095741741300849X)
- Kajian bitcoin: pilih peraturan teratas dengan ujian hipotesis berganda, kemudian gabungkan menjadi portfolio. Gabungan itu mengalahkan beli-dan-pegang di luar sampel, terutamanya atas asas risiko-pulangan. Ia dibandingkan dengan beli-dan-pegang, bukan dengan peraturan tunggal terbaik. — [IDEAS/RePEc, Rev. Econ. & Fin. 2024](https://ideas.repec.org/a/eee/reveco/v93y2024ipbp858-874.html)
- Nardari dan Schüssler ("Ensembles of Portfolio Rules"): keuntungan utiliti yang besar berbanding peraturan individu dan kaedah gabungan terdahulu sepanjang empat dekad penilaian luar sampel. Ini untuk peraturan pilihan portfolio, bukan peraturan dagangan teknikal. — [EFMA 2023 (PDF)](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2023-UK/papers/EFMA%202023_stage-4455_question-Full%20Paper_id-263.pdf)
- DeMiguel et al.: tiada daripada 14 model optimum yang secara konsisten mengalahkan 1/N di luar sampel. — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rfinst/v22y2009i5p1915-1953.html)
- McLean-Pontiff: pulangan 26% lebih rendah di luar sampel. Jacobs dan Müller (241 anomali, 39 pasaran): AS satu-satunya negara dengan penurunan pasca penerbitan yang boleh dipercayai. — [SSRN 2156623](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623); [JFE, Jacobs & Müller](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19301618)

### Inferences
- Dalam konteks 123 kaedah, "kaedah tunggal terbaik" mengikut skor KPI adalah calon yang paling terdedah kepada bias pemilihan (pemenang daripada banyak percubaan). Gabungan 3–4 kaedah berpemberat sama daripada kumpulan isyarat berbeza ialah lindung nilai terhadap kemungkinan kaedah teratas itu sebenarnya bertuah. Kos jangkaannya ialah sedikit pulangan purata yang dilepaskan jika kaedah teratas benar-benar terbaik.
- Ujian langsung yang boleh dibuat dengan data sedia ada: jejaki ke hadapan (beku) tiga portfolio dalam tempoh yang sama, iaitu (a) kaedah #1 sahaja, (b) gabungan greedy 4 kaedah, dan (c) 4 kaedah rawak daripada yang lulus ambang. Bandingkan jumlah pulangan, DD maksimum dan Sharpe mingguan. Pendekatan sama (RS_10 vs RAWAK_10) sudah wujud dalam `portfolio_slot/` dan boleh diperluas.
- Kerana matlamat pengguna ialah kaedah "mampan" dengan untung maksimum, kriteria gabungan wajar mengutamakan pulangan selepas potongan bias pemilihan (contohnya skor dikurangkan mengikut bilangan kaedah yang diuji, ala Harvey-Liu atau Deflated Sharpe). Skor backtest mentah tidak sesuai.

### Gaps
- Tiada kajian ditemui yang secara langsung membandingkan "gabungan N strategi berskor tertinggi" vs "strategi tunggal terbaik" bagi strategi swing saham dengan reka bentuk luar sampel yang ketat.
- Definisi PBO yang tepat (logit kedudukan relatif OOS pemenang IS) tidak dapat disahkan daripada teks asal kerana SSRN disekat.
