# Pangkas metrik, kecutkan hingar, bekukan pilihan kaedah

Skor kaedah swing yang paling boleh dipercayai bukan skor yang menambah metrik, tetapi skor yang lebih kecil dan lebih jujur. Ia mengira setiap metrik **bersih kos pada posisi matang dengan n berkesan ikut hari beli**, dan menggantikan 13 metrik yang bertindih dengan **sembilan metrik yang mengukur perkara berbeza**. Kelebihan setiap kaedah dikecutkan secara Bayes empirik ke arah jangkaan backtest yang dipotong secara tidak linear. Kaedah ditapis dengan pintu lulus/gagal sebelum tunjang digabungkan secara geometrik, dan 3–4 kaedah dipilih ikut **kebarangkalian kekal dalam 4 teratas**, daripada kelompok korelasi berbeza, dengan peruntukan sama, lalu dibekukan dan dipantau dengan peraturan persaraan bertulis. Ini mendesak kerana data sekarang terlalu nipis untuk menyokong susunan semasa. Dengan kira-kira 10 hari beli berbeza, n berkesan setiap kaedah hanya sekitar 10, sub-skor kadar menang berayun ±41 mata pada 36 dagangan, dan kaedah teratas daripada 123 dijangka mencapai **t ≈ 2.6 melalui nasib semata-mata**. Reka bentuk semasa memberi data hadapan wajaran kira-kira 64% (36 dagangan mentah lawan 20 dagangan setara), sedangkan model Papan Penganalisis sendiri hanya memberi kira-kira 25%. Maka susunan M03, M70, M12 dan M66 belum dapat dibezakan daripada nasib dan regim pasaran dua minggu. Rangka sedia ada (julat tetap, empat tunjang, formula telus, pengecutan, had pertindihan) selaras dengan amalan OECD/JRC dan wajar dikekalkan. Langkah praktikalnya: guna skor sekarang untuk menyingkir kaedah lemah dan menyempitkan senarai kepada 15–20 calon, tahan label "Teras" sehingga ≥ 20 hari beli matang (paling awal sekitar akhir November 2026), pilih gabungan sementara pada titik itu, bekukan, dan anggap ia muktamad hanya selepas inkubasi kira-kira 6 bulan dengan sekurang-kurangnya 40–60 hari beli tanpa mencetus peraturan gantung.

> **Nota sumber.** Proksi sesi penyelidikan menyekat teks penuh, jadi **semua dapatan luar dalam laporan ini diambil daripada ringkasan enjin carian, abstrak dan dokumentasi yang dipetik, bukan bacaan teks penuh**. Tanda **†** menandakan dakwaan yang nota penyelidik sendiri labelkan sebagai sekunder, belum disemak dengan teks asal, atau bercanggah antara sumber; senarai lengkapnya ada dalam bahagian "Dakwaan yang hanya bersandar pada ringkasan carian" sebelum senarai perubahan. Fakta tentang kod dan data repo dibaca terus daripada fail. Contoh berangka ialah aritmetik sendiri daripada formula yang dipetik, dan semua kod JavaScript dalam laporan ini telah dijalankan dalam Node 22 dengan data sintetik.

## Tiga belas metrik sebenarnya mengukur kira-kira empat perkara

Masalah terbesar skor semasa bukan wajarannya, tetapi kiraan berganda. Kadar menang, nisbah bayaran, faktor untung (PF) dan jangkaan ialah satu keluarga algebra: **PF = W/(1 − W) × P**, dengan W kadar menang dan P nisbah bayaran ([NexusFi](https://nexusfi.com/a/risk-management/trading-performance-metrics)). Jangkaan pula hanyalah gabungan kadar menang dan nisbah bayaran menjadi hasil purata setiap dagangan ([LuxAlgo](https://www.luxalgo.com/library/concept/expectancy/)), manakala Omega pada ambang 0 sama dengan nisbah untung–rugi Bernardo–Ledoit, iaitu PF bagi dagangan berwajaran sama ([Wikipedia: Omega ratio](https://en.wikipedia.org/wiki/Omega_ratio)). Dalam skor v97, sekurang-kurangnya sembilan daripada 13 metrik (untung dilaras, lebih SPY, kadar menang, PF, median, tanpa 3 terbaik, rugi purata, kerugian terbesar dan had bawah 95%) ialah fungsi taburan pulangan setiap dagangan yang sama ([dashboard_v2.html](../BacktestShariah2/standard/dashboard_v2.html)). Akibatnya, wajaran berkesan "purata pulangan" jauh melebihi 40 yang dinyatakan. "Had bawah 95% purata" juga hampir sama maklumatnya dengan SQN Van Tharp, iaitu jangkaan ÷ SD × √N, yang pada dasarnya statistik-t ([Tradervue](https://www.tradervue.com/help/reports/report_stats)). Darwinex mengambil jalan sebaliknya: 12 atribut boleh labur mereka direka supaya bebas antara satu sama lain ([Darwinex](https://help.darwinex.com/what-are-investable-attributes)). Prinsip yang sama patut dipakai di sini, iaitu satu wakil bagi setiap keluarga, disahkan dengan matriks korelasi Spearman antara sub-skor merentas 123 kaedah (|ρ| > 0.8 bermaksud kiraan berganda).

Dua metrik semasa juga menghukum atau menolong kaedah mengikut saiz sampel, bukan kualiti. "Kerugian terbesar" ialah statistik tertib ekstrem: kaedah dengan 200 dagangan hampir pasti mempunyai dagangan terburuk yang lebih teruk daripada kaedah dengan 20 dagangan. "Tanpa 3 terbaik" pula membuang 15% sampel pada n = 20 tetapi hanya 1.5% pada n = 200. Penggantinya ialah ukuran berkadar: purata dipangkas 5% (sudah dipakai Papan Penganalisis) dan CVaR, iaitu purata ekor terburuk. Median juga patut keluar daripada skor kerana kaedah swing ikut trend memperoleh untung daripada ekor kanan, dan strategi ikut trend memang dijangka mempunyai nisbah ekor > 1 ([wraquant](https://wraquant.readthedocs.io/en/latest/_modules/wraquant/risk/tail.html)). Median akan menghukum kaedah sihat yang kadar menangnya di bawah 50%.

Bukti tentang metrik mana yang benar-benar meramal juga menyokong pemangkasan ini. Kajian Quantopian ke atas **888 algoritma** dengan sekurang-kurangnya 6 bulan luar sampel mendapati Sharpe backtest hampir tiada nilai ramalan (**R² < 0.025**). Volatiliti, kejatuhan maksimum dan ciri pembinaan portfolio pula menunjukkan nilai ramalan signifikan, dan semakin banyak backtest dijalankan, semakin besar jurang dalam sampel–luar sampel ([Wiecki et al., Journal of Investing](https://www.pm-research.com/content/iijinvest/25/3/69); [Quantpedia](https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/))†. Indeks strategi 17 bank pelaburan mengalami **median kemerosotan Sharpe 73%** dari backtest ke langsung, lebih teruk bagi strategi yang lebih kompleks ([Alpha Architect](https://alphaarchitect.com/looking-at-alternatives-avoid-complexity-and-magical-backtests/)). Implikasinya, tunjang Risiko patut diberi wajaran sebenar dan purata pulangan mentah tidak patut menguasai skor. Satu alternatif yang lebih teoretikal ialah setara-kepastian ala-Morningstar MRAR dengan γ = 2, yang menghukum kerugian besar secara automatik dan boleh menggantikan sebahagian besar tunjang Untung dan Konsisten dengan satu nombor ([Morningstar Methodology 2021](https://www.morningstar.com/content/dam/marketing/shared/research/methodology/771945_Morningstar_Rating_for_Funds_Methodology.pdf); [AEA 2021](https://www.aeaweb.org/conference/2021/preliminary/paper/F4zh4AeG))†. Versi dagangan ialah CE = [purata((1 + rᵢ)^−2)]^(−1/2) − 1.

Kecekapan modal ialah satu dimensi yang benar-benar berbeza dan relevan kerana slot terhad. Ada tiga takrif "untung sehari". Purata(r/d) meletup bagi dagangan satu hari. Penahunan setiap dagangan pula tidak masuk akal: 2% dalam sehari bersamaan +14,600% setahun. Takrif yang betul ialah **Σr ÷ Σd**, sama dengan konsep pulangan ÷ pendedahan AmiBroker ([AmiBroker](https://www.amibroker.com/guide/h_report.html)). Kod semasa sudah memakai bentuk nisbah purata ini (`uh = shr / hr`). Yang perlu diubah ialah inputnya (posisi matang, bersih kos, posterior) dan unitnya, iaitu % setiap 21 hari dagangan supaya sepadan dengan skor sebulan Papan Penganalisis. Kepentingannya besar: gabungan teratas menjana kira-kira 149 isyarat seminggu, sedangkan portfolio 10 slot dengan pegangan purata sekitar 7 hari (andaian ilustrasi) hanya membuka kira-kira 7 posisi baharu seminggu. Maka pulangan setiap slot-hari lebih menentukan untung sebenar daripada purata setiap isyarat.

Kos mesti ditolak sebelum sebarang metrik dikira. Novy-Marx dan Velikov mendapati anomali dengan pusing ganti sehala bulanan **< 50%** kebanyakannya kekal signifikan selepas kos, tetapi sedikit sahaja yang pusing gantinya lebih tinggi ([Novy-Marx & Velikov](https://mysimon.rochester.edu/novy-marx/research/ToAatTC.pdf); [NBER w20721](https://www.nber.org/papers/w20721)). Swing yang dipegang purata 5 hari berpusing kira-kira 400% sebulan, jauh dalam zon berbahaya itu. Data pelaksanaan AQR menunjukkan kos institusi sebenar "satu tertib magnitud lebih kecil" daripada anggaran akademik, tetapi balikan jangka pendek tetap paling terhad oleh kos ([Frazzini, Israel & Moskowitz](https://papers.ssrn.com/abstract=3229719)). Penyelidik tidak menemui angka bps sumber primer bagi peruncit AS. Oleh itu kos perlu diuji pada tiga tahap, dan kaedah yang kekal dalam 4 teratas pada ketiga-tiganya lebih mampan. Akhir sekali, purata MAE mentah meningkat dengan tempoh pegang dan volatiliti saham, jadi ia menghukum lorong 2 dan saham volatil. Sweeney sendiri memakai MAE terutamanya untuk mendiagnosis peletakan henti, iaitu membanding MAE pemenang dengan MAE pengalah ([NexusFi MAE](https://nexusfi.com/a/risk-management/maximum-adverse-excursion-mae)). Untuk skor, MAE patut dinormalkan dengan ATR14 semasa masuk.

| Metrik v97 (wajaran) | Masalah | Keputusan |
|---|---|---|
| u1 Untung purata dilaras (25) | Dikecut ke min global dengan n mentah; termasuk posisi belum matang | **UBAH**: posterior Bayes empirik, bersih kos, matang, n berkesan |
| u2 Untung sehari (10) | Bentuk Σr/Σd betul, input belum matang | **UBAH** input; unit % setiap 21 hari |
| u3 Lebih SPY (5) | Hampir anjakan malar u1 dalam tempoh sama | **UBAH**: lebihan atas penanda aras dalaman hari sama |
| k1 Kadar menang (8) | Keluarga PF; ±41 mata hingar pada n = 36 | **BUANG** daripada skor (papar sahaja) |
| k2 Faktor untung (7) | Wakil keluarga; jadi 99 jika tiada rugi | **KEKAL**, dihad 3 |
| k3 Median (5) | Bertindih; menghukum ekor kanan | **BUANG** |
| k4 Tanpa 3 terbaik (5) | Bergantung n | **BUANG** (purata dipangkas dalam u1) |
| r1 Penurunan maks purata (10) | Naik dengan tempoh pegang dan volatiliti | **UBAH**: MAE ÷ ATR14 |
| r2 Rugi purata (5) | Keluarga PF/jangkaan | **BUANG** |
| r3 Kerugian terbesar (5) | Statistik tertib, bergantung n | **UBAH** → CVaR 10% |
| b1 Untung minimum 95% (5) | n mentah; ≈ statistik-t; berkorelasi dengan u1 | **UBAH** → bahagian bukti hadapan (pemberat pengecutan B) |
| b2 Sebenar ÷ backtest (5) | Mengukur regim dua minggu | **BUANG** daripada skor; masuk kalibrasi prior |
| b3 Semakan luar sampel (5) | Berguna walaupun tidak bebas sepenuhnya | **KEKAL**; juga input prior |
| (baharu) Hari beli positif | Konsistensi merentas masa | **TAMBAH**: had bawah Wilson atas G |

## Sepuluh hari beli tidak cukup untuk membezakan juara daripada nasib

Dagangan yang dibeli pada hari yang sama berkongsi kejutan pasaran, jadi ia bukan cerapan bebas. Kesan reka bentuk Kish ialah **DEFF = 1 + (m − 1)ρ**. Dengan 30 dagangan sehari dan korelasi intrakelompok 0.2, DEFF = 6.8, dan apabila ρ menghampiri 1, n berkesan jatuh kepada bilangan hari beli berbeza, G ([MetricGate](https://metricgate.com/docs/design-effect-cluster/))†. Ralat piawai lalai boleh sangat melebih-lebihkan ketepatan apabila ralat berkorelasi dalam kelompok ([Cameron & Miller, JHR](https://jhr.uwpress.org/content/50/2/317)). Bagi kelompok yang sedikit, nilai kritikal t(G − 1) jauh lebih tepat dan konservatif berbanding taburan normal ([MacKinnon, Nielsen & Webb](https://arxiv.org/pdf/2205.03285)), dan bootstrap-t kelompok liar ialah pembetulan yang disyorkan ([World Bank](https://blogs.worldbank.org/en/impactevaluations/beware-of-studies-with-a-small-number-of-clusters)). Peraturan "cukup kelompok" berbeza antara 10, 20 dan 50+ ([Statalist](https://www.statalist.org/forums/forum/general-stata-discussion/general/1440015-reghdfe-and-t-statistics)). Papan Penganalisis sudah mengira n berkesan secara CR1 ikut hari beli ([penganalisis.py](../BacktestShariah2/standard/penganalisis.py)). Skor swing pula masih memakai n mentah pada tiga tempat: had bawah 95%, pengecutan dan kelayakan "≥ 20 dagangan tutup". Dengan G = 10, nilai kritikal sepatutnya **2.262, bukan 1.96**, dan ralat piawai sepatutnya √(n/n berkesan) kali lebih lebar.

Saiz sampel yang diperlukan untuk bukti sebenar jauh di luar jangkauan dua minggu. Formula n = (z·s/δ)² memberi **256 dagangan bebas** untuk mengesan kelebihan 1% dengan SD 8% pada t = 2, dan 576 pada t = 3. Panjang rekod minimum (MinTRL) Bailey dan López de Prado memanjang lagi apabila kepencongan negatif atau kurtosis tinggi ([Journal of Risk](https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier); [SLCG](https://www.slcg.com/files/practice-notes/sharpe-ratio.pdf))†. Kadar menang lebih murah dianggar, tetapi selang Wilson bagi 11/20 masih **[34%, 74%]**. Selang Wilson dipilih kerana ia tidak runtuh di sempadan seperti selang Wald ([Brown, Cai & DasGupta](https://projecteuclid.org/download/pdf_1/euclid.ss/1009213286)). Pada n = 36, separuh lebar selang ialah ±16 mata peratus, bersamaan **±41 mata** pada sub-skor kadar menang semasa (julat 30–70%). Untuk purata pulangan, dengan SD 7% andaian, ia bersamaan ±26 mata. Ambang "≥ 20 dagangan" hanyalah ambang paparan, bukan ambang kebolehpercayaan.

Pengecutan ialah jawapan yang betul, dan kekuatannya boleh dianggar daripada data, bukan ditetapkan. Contoh klasik Efron dan Morris menunjukkan penganggar James–Stein, yang menarik purata setiap pemain ke arah purata besar, meramal lebih baik daripada purata individu. Roberto Clemente yang memukul .400 selepas 45 pukulan diramal .290 ([Efron & Morris 1977](https://www.gwern.net/doc/statistics/bayes/1977-efron.pdf)). Dalam model normal–normal, ketepatan prior dan data dijumlahkan, jadi kekuatan prior bersamaan **n₀ = σ²/τ²** cerapan tambahan ([CRAN glmbayes](https://cran.r-project.org/web/packages/glmbayes/vignettes/Chapter-02-S02.html)). Maka "+20 dagangan setara" dalam v97 secara tersirat mendakwa sisihan piawai kelebihan sebenar antara kaedah ialah τ ≈ 8%/√20 ≈ 1.8% setiap dagangan. Lebih penting, dua papan dalam projek yang sama kini bercanggah. Skor swing mengecut ke arah **min global lorong** dengan n mentah, jadi 36 dagangan mendapat wajaran 36/56 = 64%. Papan Penganalisis pula mengecut ke arah **jangkaan backtest khusus kaedah** dengan n₀ ≈ 30 dan n berkesan, jadi 10 hari beli mendapat wajaran 10/40 = 25% ([penganalisis.py](../BacktestShariah2/standard/penganalisis.py)). Cara yang lebih baik ialah menganggar τ̂² merentas 123 kaedah dengan kaedah momen, menetapkan lantai pada s²/30, dan akhirnya meregres purata hadapan matang ke atas backtest (μ₀ = a + b·backtest). Jika b ≈ 0, kecut ke min global; jika b ≈ 0.25–0.5, ia selaras dengan amalan potongan; jika b ≈ 1, backtest boleh dipercayai. Hari ini persoalan ini masih akademik: papan.json pada 20 Okt 2026 mencatat **0 posisi matang bagi setiap kaedah** daripada 5,789 posisi Lejar ([papan.json](../BacktestShariah2/data/analisis/papan.json)). Jadi sebarang susunan "hadapan" sekarang sebenarnya susunan backtest yang dipotong.

Potongan backtest itu sendiri patut tidak linear dan khusus bagi setiap kaedah. Harvey dan Liu menunjukkan potongan Sharpe tetap 50% ialah "kesilapan serius" sebagai peraturan. Kaedah mereka menukar Sharpe kepada statistik-t, melaras nilai-p untuk bilangan ujian, lalu menukarnya semula; hasilnya, strategi kuat dipotong sedikit dan strategi marginal dipotong teruk ([Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF); [Man Institute](https://www.man.com/insights/backtesting))†. Dengan Bonferroni atas 431 set yang pernah diuji, kiraan sendiri memberi **pecahan dikekalkan 0.94 pada t = 10, 0.82 pada t = 6, 0.73 pada t = 5, 0.55 pada t = 4, 0.45 pada t = 3.68 dan 0 pada t = 3**. Formula ini boleh menggantikan pemalar "25% + 25% bagi setiap semakan lulus" dalam Papan Penganalisis, yang kini memberi median pengekalan hanya kira-kira 26% (median backtest 2.47% → median jangkaan 0.65% setiap dagangan; [papan.json](../BacktestShariah2/data/analisis/papan.json)). Sebagai jalur kewarasan, pulangan anomali turun kira-kira 26% di luar sampel dan 58% selepas penerbitan ([McLean & Pontiff, SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623))†.

Berat sebelah pemilihan ialah risiko terbesar apabila memilih 4 daripada 123. Jangkaan maksimum N skor-z nol, iaitu halangan dalam Deflated Sharpe Ratio, ialah **2.60 bagi N = 123 dan 3.01 bagi N = 431**; ambang Bonferroni 5% sehala pula 3.35 dan 3.68. Kaedah teratas dengan t ≈ 2.6 tepat seperti hasil yang dijangka daripada nasib, dan Harvey, Liu dan Zhu menuntut t > 3 untuk penemuan baharu ([NBER w20592](https://www.nber.org/papers/w20592)). DSR membetulkan kedua-dua ujian berbilang dan ketidaknormalan ([SSRN 2460551](https://papers.ssrn.com/abstract=2460551); [Wikipedia: DSR](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio))†. Satu sumber berat sebelah lagi tersembunyi dalam kod: v97 memilih lorong (kaedah atau selagi naik) yang purata hadapannya lebih tinggi, dan itu sendiri ialah pemilihan daripada dua. Bagi dua anggaran dengan min sama, ralat piawai SE dan korelasi ρ, **E[maks] − maks(E) = SE·√((1 − ρ)/π)**, iaitu 0.25 SE pada ρ = 0.8 dan 0.56 SE pada ρ = 0 (terbitan sendiri). Lorong patut dipra-komit, atau penalti ini ditolak. Min posterior Bayes empirik secara semula jadi membetulkan kutukan pemenang bagi anggaran ([arXiv 2603.12867](https://arxiv.org/html/2603.12867)). Untuk keputusan memilih, kebarangkalian setiap kaedah berada dalam 4 teratas, P(4 teratas), boleh dikira melalui Monte Carlo daripada taburan posterior.

Akhir sekali, skor semasa terdedah kepada bias keluar awal. Posisi yang masih terbuka ialah cerapan tertapis kanan, dan kaedah yang mengabaikan penapisan memberi anggaran berbias ([MedCalc: Kaplan–Meier](https://www.medcalc.org/en/book/kaplan-meier.php); [Tian et al., Biostatistics](https://pmc.ncbi.nlm.nih.gov/articles/PMC3944973)). Fungsi `hasilL` dalam v97 memasukkan **setiap** posisi terbuka pada harga semasa tanpa mengira umur, manakala kelayakan pula memerlukan 20 keluar lorong kaedah. Gabungan ini menyebelahi kaedah yang keluar cepat dan mencampurkan posisi berumur sehari (hampir semuanya hingar) dengan posisi yang sudah selesai. Penyelesaian paling ringkas ialah takrif matang Papan Penganalisis: umur ≥ maks(14 hari, 1.5 × hari pegang backtest), dengan posisi tutup dinilai pada untung akhir dan posisi terbuka pada untung semasa. Alternatifnya ialah pulangan ufuk tetap R_H. Papan juga patut melaporkan "% masih terbuka dalam set matang" dan beza antara purata tutup-sahaja dengan purata matang sebagai ukuran saiz bias.

## Julat tetap boleh kekal, tetapi pampasan dan wajaran tersembunyi perlu dibuang

Pilihan normalisasi semasa boleh dipertahankan. Buku Panduan OECD/JRC tidak menetapkan satu kaedah terbaik. Min-max peka pencilan dan membesarkan penunjuk yang terletak dalam selang sempit; skor-z memberi nilai ekstrem pengaruh lebih besar; pangkat membuang magnitud ([OECD/JRC Handbook](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)). Skor-z juga hanya menyokong perbandingan relatif dari masa ke masa ([Mazziotta & Pareto, Istat](https://www.istat.it/en/files/2013/12/Rivista2013_Mazziotta_Pareto.pdf)). Papan yang mahukan ambang mutlak (Teras ≥ 70) dan perbandingan antara minggu memerlukan julat tetap yang dibekukan, jadi kekalkan pendekatan itu. Namun **lebar julat ialah wajaran tersembunyi**: sumbangan berkesan metrik i lebih kurang wᵢ × sd(sub-skorᵢ) merentas kaedah. Jika hampir semua kaedah mempunyai kadar menang 45–55%, julat 30–70% menjadikan sub-skor itu hampir malar dan wajarannya hilang. Jika ramai kaedah tepu pada 100, julat terlalu sempit untuk membezakan yang terbaik, padahal itulah tujuan memilih 3–4 kaedah. Julat patut dikalibrasi pada persentil ke-5 dan ke-95 set backtest 431, dibekukan bersama versi dan tarikh, dan disemak suku tahunan. Papan juga patut memaparkan "wajaran berkesan" dan kadar tepu setiap metrik. Pangkat persentil boleh dipaparkan di sebelah skor sebagai rujukan relatif, seperti jalur 10/22.5/35/22.5/10% bintang Morningstar ([Morningstar Disclosure](https://profile.morningstar.com/ISR/MorningstarDisclosure.html)).

Wajaran pakar yang kasar memadai; menala wajaran dengan data dua minggu akan merosakkan skor. Dawes menunjukkan gabungan wajaran sama bagi GRE, GPA dan selektiviti berkorelasi **0.48** dengan penilaian fakulti kemudian, mengatasi pertimbangan jawatankuasa (0.19) dan regresi yang disahkan silang ([Dawes 1979](https://www.researchgate.net/publication/232597503_The_robust_beauty_of_improper_linear_models_in_decision_making)). Ujian moden mengesahkan bahawa regresi wajaran sama kerap mengatasi OLS, terutamanya dengan set latihan kecil, walaupun tiada satu model ringkas yang terbaik pada semua data ([Lichtenberg & Şimşek, PMLR](http://proceedings.mlr.press/v58/lichtenberg17a/lichtenberg17a.pdf)). Wajaran entropi menghadiahkan metrik yang paling berserak, bukan yang paling meramal, dan kebarangkalian pembalikan pangkat meningkat dengan entropi wajaran ([Fedrizzi & Predella](https://iris.unitn.it/retrieve/e3835194-37ee-72ef-e053-3705fe0ad821/Fedrizzi-Predella-ODS2017.pdf))†. Jadi kekalkan wajaran pakar. Tunjang Risiko dinaikkan sedikit (20 → 25) kerana metrik risiko lebih stabil antara dalam sampel dan luar sampel, dan tunjang Konsisten diturunkan (25 → 20) kerana kebanyakan isinya kiraan berganda. Wajaran berasaskan data hanya patut dicuba selepas sekurang-kurangnya 8–12 minggu tetingkap bebas, dan hanya jika ujian ramalan tunjang demi tunjang menunjukkan perbezaan.

Agregasi aditif sepenuhnya membenarkan pampasan penuh: kaedah dengan untung tinggi boleh menebus MAE yang teruk. HDI PBB beralih kepada min geometri pada 2010 khusus supaya pencapaian rendah dalam satu dimensi tidak lagi diimbangi secara linear ([UN HDR Technical Notes](https://data.un.org/_Docs/HDR%20Technical%20Notes.pdf)). Min geometri masih membenarkan sebahagian pampasan ([VU](https://vuir.vu.edu.au/48574/1/Aggregating_the_Human_Development_Index.pdf)), dan kesannya pada pangkat sederhana ([Paruolo, Saisana & Saltelli](https://arxiv.org/pdf/1104.3009)). Sistem penyusunan sebenar pula meletakkan pintu wajib sebelum skor. Quantopian hanya menyusun algoritma yang lulus semua kriteria struktur ([Quantopian Contest](https://www.quantopian.com/tutorials/contest)). ZuluTrade (EU) menuntut sekurang-kurangnya 8 minggu dagangan dan kejatuhan ≤ 30% daripada jumlah untung ([ZuluTrade](https://www.zulutrade.com/zuluranking)). StrategyQuant menolak secara automatik strategi yang gagal ujian Monte Carlo ([StrategyQuant](https://strategyquant.com/features/)). Reka bentuk yang disyorkan ialah **pintu → aritmetik dalam tunjang → geometrik berwajaran antara tunjang (lantai 5)**. Contohnya, kaedah dengan tunjang U 90, K 80, R 20, B 60 mendapat 66 secara aritmetik (Calon) tetapi **57** secara geometrik, sekali gus jatuh ke sempadan bawah Calon kerana risikonya buruk. Oleh sebab skor geometrik ≤ skor aritmetik, ambang 70/55 perlu dikalibrasi semula pada taburan baharu. Peraturan v97 "metrik hilang digugurkan dan wajaran dinormal semula" juga secara tersirat mengimput metrik yang hilang dengan purata metrik lain kaedah itu, jadi kaedah tanpa data backtest atau MAE diuntungkan. Metrik teras yang hilang patut menyebabkan kaedah gagal pintu, manakala metrik sekunder yang hilang diimput pada persentil ke-25 dan liputannya dipaparkan.

Ujian "stabil" semasa terlalu sempit untuk bermakna. Amalan JRC ialah analisis ketidakpastian Monte Carlo: sampel pilihan pemodelan (wajaran, normalisasi, agregasi), kira semula pangkat beribu kali, dan laporkan pangkat median bersama persentil ke-5 hingga ke-95 ([Saisana, Saltelli & Tarantola 2005](https://www.andreasaltelli.eu/file/repository/JRSS_2005.pdf); [JRC EUR 21682](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC31473/EUR%2021682%20EN.pdf)). Audit JRC terhadap Global Innovation Index masih melakukannya pada tahun ke-16 ([WIPO GII 2026](https://www.wipo.int/web-publications/global-innovation-index-2026/en/appendix-ii-joint-research-centre-jrc-statistical-audit-of-the-2026-global-innovation-index.html)). Ketiga-tiga set wajaran v97 mengekalkan Konsisten pada 25 dan Bukti pada 15–20, jadi hanya paksi Untung↔Risiko yang diuji, dengan tiga titik sahaja, dan tanpa sebarang hingar data. Gantikannya dengan 1,000 lelaran yang serentak (a) menarik u1 daripada posterior setiap kaedah, (b) mendarab wajaran tunjang dengan U(0.5, 1.5), dan (c) menogol agregasi aritmetik/geometrik. Lencana "stabil" diberi jika P(4 teratas) ≥ 0.5, dan "rapuh" jika julat persentil ke-5 hingga ke-95 melebihi 30 pangkat. Kos pengiraannya remeh bagi pelayar.

Ada satu lagi sebab untuk merendahkan cita-cita skor dalam fasa ini: bukti dunia sebenar menunjukkan penarafan lebih baik menyingkir yang lemah daripada menobatkan yang terbaik. Blake dan Morey mendapati penarafan Morningstar yang rendah cenderung berterusan, tetapi dana 5 bintang tidak mengatasi dana 3 atau 4 bintang secara signifikan ([dipetik dalam IREF 2022](https://www.sciencedirect.com/science/article/abs/pii/S1059056022001873))†. Bagi dana hartanah, penarafan tidak lagi memberi panduan selepas pelarasan Fama–French dan momentum ([Journal of Property Research](https://www.tandfonline.com/doi/full/10.1080/09599916.2011.577902)). Kajian Morningstar sendiri, yang mempunyai konflik kepentingan, hanya mendakwa daya ramalan sederhana ([Morningstar](https://www.morningstar.com/funds/does-star-rating-funds-predict-future-performance)).

## Empat kaedah berkorelasi 0.5 hanya memberi pengganda kepelbagaian 1.26

Faedah gabungan bergantung hampir sepenuhnya pada korelasi pulangan, bukan pada bilangan kaedah. Pengganda kepelbagaian Carver dikira daripada matriks korelasi dan pemberat ([qoppac](https://qoppac.blogspot.com/2016/01/correlations-weights-multipliers.html))†. Bagi N kaedah berpemberat sama dengan korelasi purata ρ, nilainya ialah DM = 1/√(1/N + (1 − 1/N)ρ). Kiraan sendiri memberi jadual berikut. Pada ρ = 0.5, empat kaedah sudah mencapai kira-kira 71% pengurangan volatiliti maksimum yang mungkin, jadi kaedah kelima hampir tiada nilai tambah. Pada ρ ≥ 0.7, nilai gabungan hanya datang daripada purata alpha. Semua kaedah long-only saham AS berkongsi beta pasaran, jadi korelasi mentah dijangka tinggi (perlu diukur daripada Lejar Penuh). Carver juga memerhatikan bahawa korelasi antara peraturan berbeza pada instrumen yang sama lebih tinggi daripada korelasi peraturan sama pada instrumen berbeza†. Maknanya, kepelbagaian datang daripada keluarga isyarat yang berbeza, bukan daripada varian peraturan.

| ρ purata | N = 2 | N = 3 | N = 4 | N = 10 | N → ∞ |
|---|---|---|---|---|---|
| 0.0 | 1.41 | 1.73 | 2.00 | 3.16 | ∞ |
| 0.3 | 1.24 | 1.37 | 1.45 | 1.64 | 1.83 |
| 0.5 | 1.15 | 1.22 | **1.26** | 1.35 | 1.41 |
| 0.7 | 1.08 | 1.12 | 1.14 | 1.17 | 1.20 |

Pertindihan saham dalam ±5 hari, iaitu kriteria v97, mengukur pertindihan nama, bukan pertindihan risiko. Dua kaedah yang membeli saham berbeza selepas penurunan pasaran yang sama akan mempunyai pulangan yang sangat berkorelasi. Rujukan amalan mengukur korelasi siri P/L. StrategyQuant membuang strategi yang korelasinya dengan portfolio sedia ada melebihi had yang ditetapkan pengguna, tanpa nilai lalai yang disyorkan ([StrategyQuant](https://strategyquant.com/doc/strategyquant/fit-strategy-to-existing-portfolio/)). QuantAnalyzer menyediakan pilihan "abaikan hari sifar" bagi strategi yang jarang berdagang ([QuantAnalyzer](https://strategyquant.com/doc/quantanalyzer/portfolio-correlation-explained/)). Build Alpha memakai pulangan harian tanda-ke-pasaran ([Build Alpha](https://www.buildalpha.com/buildalpha-features/)). Penyelidik tidak menemui sumber primer bagi ambang 0.5 atau 0.7. Ukuran utama yang disyorkan ialah korelasi pulangan **lebihan** mingguan portfolio maya setiap kaedah dalam Lejar Penuh (mingguan lebih stabil bagi pegangan 3–30 hari), dengan pertindihan saham sebagai semakan sekunder.

Selepas calon dipilih, peruntukkan secara sama rata dan jangan ikut skor. DeMiguel, Garlappi dan Uppal menguji 14 model atas 7 set data dan mendapati tiada yang secara konsisten mengalahkan 1/N. Mean-variance memerlukan tetingkap anggaran kira-kira 3,000 bulan bagi 25 aset sebelum ia menang ([DeMiguel et al., RFS](https://ideas.repec.org/a/oup/rfinst/v22y2009i5p1915-1953.html)). "Teka-teki gabungan ramalan" (forecast combination puzzle) menunjukkan purata sama kerap mengalahkan pemberat optimum yang dianggar ([UCR WP](https://webarchive.ucr.edu/economics.ucr.edu/repec/ucr/wpaper/202514.pdf)). Elliott dan Liao pula mendapati bahawa apabila keuntungan gabungan optimum besar, membuang sebahagian ramalan lalu mengambil purata yang selebihnya berprestasi lebih baik ([Elliott & Liao](https://econweb.ucsd.edu/~gelliott/Combination.pdf)). Itulah falsafah "pilih subset kecil, beri pemberat sama". HRP mengurangkan varians luar sampel bagi banyak aset ([López de Prado, SSRN](https://papers.ssrn.com/abstract=2708678)), tetapi pokok kelompoknya tidak bermakna bagi 3–4 kaedah. Pendekatan handcrafting Carver, iaitu kumpulkan dahulu kemudian peruntukkan ([CXO Advisory](https://www.cxoadvisory.com/big-ideas/a-few-notes-on-systematic-trading))†, boleh disesuaikan dengan memilih satu kaedah terbaik daripada setiap kelompok korelasi atau keluarga isyarat. Kod v97 juga melaporkan purata gabungan sebagai purata semua dagangan yang dihimpun (`pil.flatMap(x => x.v)`). Ini secara tersirat memberi wajaran ikut kekerapan isyarat, jadi kaedah yang paling kerap berisyarat menguasai angka itu. Laporkan purata sama-berat bagi posterior kaedah, dan laksanakan kuota slot (10 slot ÷ 4 ≈ 2–3 slot setiap kaedah, dengan slot tidak terpakai dikongsi) supaya satu kaedah tidak memonopoli modal.

Bukti langsung bahawa gabungan berskor tertinggi mengalahkan kaedah tunggal terbaik di luar sampel adalah bercampur, tetapi bukti tidak langsung kuat. Dalam kajian 6,406 peraturan teknikal merentas 41 pasaran, peraturan yang paling baik baru-baru ini berprestasi jauh lebih buruk daripada beli-dan-pegang pada masa hadapan ([ResearchGate](https://www.researchgate.net/publication/374779667_The_predictive_ability_of_technical_trading_rules_an_empirical_analysis_of_developed_and_emerging_equity_markets)). Kaedah hold-out biasa juga tidak boleh dipercayai untuk memilih strategi ([PBO, SSRN 2326253](https://papers.ssrn.com/abstract=2326253)). Sebaliknya, Hsu dan Kuan mendapati strategi gabungan (pembelajaran, undian, posisi pecahan) tidak memberi penambahbaikan signifikan berbanding peraturan mudah, walaupun kertas PSO yang memetik mereka mendakwa sebaliknya bagi gabungannya sendiri ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S095741741300849X))†. Jadi gabungan ialah lindung nilai terhadap kemungkinan kaedah #1 sebenarnya bertuah, dengan kos sedikit pulangan yang dilepaskan jika #1 memang terbaik. Ujian yang menjawab persoalan ini untuk projek ini boleh dibuat dengan struktur sedia ada: jejaki gabungan beku, kaedah #1 sahaja, 4 kaedah rawak daripada yang lulus ambang, dan SPY, sama seperti RS_10 lawan RAWAK_10 dalam `portfolio_slot/`.

## Bekukan pilihan, kemudian biar peraturan bertulis memutuskan persaraan

Inkubasi menapis kegagalan besar, tetapi tidak membuktikan alpha. Kevin Davey memantau strategi dalam dagangan kertas masa nyata selama 6–12 bulan menurut satu ringkasan ([Algo Advantage 036](https://algoadvantage.substack.com/p/036-kevin-davey-part-i-its-all-about))†. Ringkasan lain menyebut 6–9 bulan atau 3–6 bulan ([Algo Advantage 037](https://algoadvantage.substack.com/p/037-kevin-davey-ii-selecting-optimal); [FinancialWisdomTV](https://www.financialwisdomtv.com/post/building-winning-algorithmic-trading-systems-kevin-davey-s-complete-framework-for-trading-success))†. Carver menganggarkan kira-kira **45 tahun** data diperlukan untuk membezakan dua peraturan dengan Sharpe 0.05 dan 0.30 pada satu instrumen ([ReformedTrader](https://threadreaderapp.com/thread/1234306875379683328.html))†, dan Sharpe 1–2 tahun tidak berterusan ([The Hedge Fund Journal](https://thehedgefundjournal.com/the-myth-of-persistent-sharpe-ratio/)). Protokol yang konsisten dengan sumber-sumber ini ada tiga langkah. Pertama, commit fail bertarikh yang merekod versi formula, set 3–4 kaedah, peraturan pemberat, slot dan berhenti. Kedua, jejaki gabungan beku itu tanpa mengubah formula. Ketiga, nilai semula hanya selepas kira-kira 6 bulan dari tarikh beku, dan hanya jika tempoh itu sudah mengandungi 40–60 hari beli dan 100–250 dagangan, mana-mana yang lebih lewat. G bertambah kira-kira lima hari seminggu, jadi syarat hari beli dipenuhi lebih awal; jika pembekuan dibuat pada akhir November 2026 apabila G matang mencapai 20, penilaian semula jatuh sekitar Mei–Jun 2027. Dalam tempoh itu, senarai pendek 15–20 calon terus dijejaki dalam Lejar Penuh tanpa menukar formula.

Ujian paling penting tidak pernah dijalankan oleh mana-mana papan: adakah skor itu sendiri meramal? Setiap minggu, kira korelasi Spearman antara skor kaedah pada akhir minggu t dengan pulangan hadapannya pada minggu t+1 dan seterusnya. Jika ρ tidak positif secara konsisten, sebarang penalaan wajaran tidak bermakna. Jika ρ positif, ρ bagi setiap tunjang boleh dibanding untuk memutuskan tunjang mana yang patut diberi wajaran lebih. Ujian ini menggantikan "trend sejak sesi lalu" sebagai bukti kualiti. Trend harian masih berguna sebagai paparan, tetapi ia mengukur pergerakan hingar.

Pemantauan perlu dilaras untuk ujian berbilang. AMARAN Papan Penganalisis (t < −2 lawan jangkaan) memberi P ≈ 0.023 bagi setiap kaedah, jadi **123 kaedah menghasilkan kira-kira 2.8 amaran palsu pada setiap semakan** walaupun tiada satu kaedah pun merosot. CUSUM ialah pengesan perubahan terpantas pada kadar penggera palsu tetap, tetapi ia masih memerlukan kira-kira 40 bulan untuk mengesan prestasi mendatar berbanding penanda aras ([Philips, CUSUM](https://www.northinfo.com/Documents/144.pdf); [IBM Research](https://research.ibm.com/publications/using-statistical-process-control-to-monitor-active-managers))†. Ujian-t juga lemah untuk membuktikan strategi sudah berhenti berfungsi ([Robot Wealth/IBKR](https://www.interactivebrokers.com/campus/ibkr-quant-news/why-you-cant-tell-if-your-strategy-stopped-working-statistically-speaking/)), dan menunggu keertian sering bermakna bertindak terlalu lewat ([Sinclair, Robot Wealth](https://edgealchemy.robotwealth.com/p/statistically-significant-and-chronically)). Oleh itu pengamal memakai brek risiko yang ditulis lebih awal. Davey menggunakan kon kebarangkalian Monte Carlo dan penimbal 1.2–1.5× kejatuhan maksimum backtest ([kjtradingsystems](https://kjtradingsystems.com/when-to-quit-trading.html); [kon Monte Carlo](https://kjtradingsystems.com/monte-carlo-probability-cones.html))†. Chan mengurangkan leveraj apabila tempoh kejatuhan melebihi tempoh kejatuhan maksimum backtest ([epchan](http://epchan.blogspot.com/2012/04/life-and-death-of-strategy.html))†. Peraturan berlapis yang disyorkan ada tiga peringkat. **Amaran** dicetus apabila jangkaan bergulir jatuh di bawah persentil ke-5 jalur bootstrap backtest bagi saiz sampel yang sama. **Gantung** (tiada belian baharu, kekal dijejaki dalam Lejar) dicetus apabila kejatuhan melebihi 1.5× kejatuhan maksimum backtest, atau tempoh kejatuhan melebihi maksimum backtest. **Bersara** dicetus apabila P(μ ≤ 0 | data) > 0.9 dengan G ≥ 20, atau CUSUM beramaran dua kali berturut-turut. CUSUM dikira atas purata harian kohort, bukan setiap dagangan, kerana dagangan berkelompok. Ambang h dikalibrasi dengan bootstrap supaya amaran palsu kira-kira sekali dalam dua tahun; nilai lazim k = 0.5 dan h ≈ 4–5 tidak disahkan daripada sumber.

Penilaian semula set gabungan patut dibuat jarang, iaitu suku tahunan, dengan histeresis. Kaedah baharu hanya menggantikan kaedah sedia ada jika skornya lebih tinggi dengan margin besar **dan** kaedah sedia ada sudah mencetuskan peraturan gantung atau bersara. Rejim pasaran (SPY di atas atau di bawah MA200) lebih sesuai dijadikan pemboleh ubah pelaporan daripada penapis tambahan. Bukti MA200 kebanyakannya pada peringkat indeks, dan manfaatnya ialah kejatuhan yang lebih kecil, bukan pulangan yang lebih tinggi ([Faber, SSRN](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf)). Satu ujian semula pada SPY malah mendapati kemasukan rawak dengan tempoh pegangan sama hampir menyamai pulangannya (p = 0.32) ([Empiricalab](https://empiricalab.substack.com/p/faber-10-month-average)). Menambah penapis rejim sekarang menambah satu lagi darjah kebebasan yang boleh terlebih padan.

## Kesimpulan

Peranan skor berubah mengikut umur data, dan papan perlu jujur tentang fasa semasa. Sehingga sekitar akhir November 2026, skor sebenarnya ialah susunan backtest yang dipotong, dibungkus sebagai prestasi hadapan. Fungsi yang sah dalam fasa ini ialah menyingkir kaedah lemah dan membina senarai pendek, bukan menobatkan "Teras". "Mampan" pula patut ditakrif secara operasi sebagai **kekal dalam kumpulan teratas walaupun data diganggu, wajaran diubah dan masa berlalu**. P(4 teratas) Monte Carlo, ujian ramalan mingguan dan inkubasi beku mengukur ketiga-tiga perkara ini secara langsung, jadi ketiga-tiganya lebih bernilai daripada sebarang metrik keuntungan tambahan.

Pembaikan paling murah juga yang paling besar kesannya, iaitu menyatukan dua papan. Skor swing dan Papan Penganalisis patut berkongsi satu prior, satu takrif matang dan satu n berkesan supaya kedua-duanya tidak lagi memberi jawapan bercanggah tentang kaedah yang sama. Untung maksimum yang mampan lebih mungkin dicapai melalui 3–4 kaedah sama-berat daripada kelompok korelasi berbeza berbanding melalui kaedah #1. Kaedah #1 daripada 123 ialah calon yang paling terdedah kepada kutukan pemenang.

## Dakwaan yang hanya bersandar pada ringkasan carian

Semua sumber luar dibaca melalui ringkasan carian. Jadual ini menyenaraikan dakwaan yang mempengaruhi cadangan secara langsung dan perlu disemak dengan teks asal sebelum dijadikan peraturan tetap.

| Dakwaan | Digunakan untuk | Status |
|---|---|---|
| Formula MRAR dan γ = 2 (Morningstar) | Alternatif metrik setara-kepastian | Bentuk formula daripada ringkasan sekunder AEA; dokumen metodologi tidak dibaca penuh |
| Formula PSR, MinTRL dan DSR (Bailey & López de Prado) | Label KUAT, halangan E[maks] | Wikipedia, Quantt dan nota SLCG; kertas asal tidak dibaca; satu sumber mentakrif V tersalah |
| Jadual potongan Harvey–Liu | `kekalHL` | Hanya kesimpulan "tidak linear" disahkan; angka contoh ialah kiraan sendiri dengan Bonferroni |
| McLean–Pontiff 26% / 58% | Jalur jangkaan | Satu nota memetik SSRN, nota lain menyatakan angka tidak disahkan |
| Wiecki et al.: R² < 0.025; volatiliti/kejatuhan meramal | Wajaran Risiko | Abstrak dan ringkasan; nilai R² bagi volatiliti/kejatuhan tidak disahkan |
| Blake & Morey (2000) | Guna skor untuk menyingkir | Dipetik secara sekunder melalui IREF 2022 |
| Davey: inkubasi 3–12 bulan, 1.2–1.5× DD, kon Monte Carlo | Protokol inkubasi dan gantung | Ringkasan saling bercanggah; buku tidak dibaca |
| Philips: CUSUM ~40 bulan; k = 0.5, h ≈ 4–5 | Pemantauan | Ringkasan PDF; k dan h tanpa sumber |
| Carver: DM, 45 tahun, korelasi peraturan lwn instrumen, handcrafting | Gabungan | Ringkasan blog/buku; jadual buku tidak dibaca |
| Kish DEFF, selang Wilson (MetricGate) | n berkesan, k2 | Sumber pendidikan sekunder; formula standard |
| Quantiacs "minimum dua tempoh", QuantConnect PSR, lantai Quantopian 2% | Contoh amalan | Projek pelajar CS229 dan forum |
| Fedrizzi & Predella (entropi dan pembalikan pangkat) | Menolak wajaran entropi | Petikan sahaja |
| Ambang korelasi 0.5/0.7, kos bps, julat tiang | Parameter kod | **Tiada sumber**: tempat letak yang mesti dikalibrasi |

## Senarai perubahan berprioriti

Keutamaan disusun ikut kesan terhadap kesahihan skor, bukan ikut usaha. P1 membetulkan perkara yang menjadikan skor semasa mengelirukan, P2 membina semula struktur, P3 membaiki pemilihan dan gabungan, dan P4 memasang pemantauan. Semua formula ada dalam kod di bawah.

| # | Keutamaan | Tindakan | Perkara | Butiran / formula |
|---|---|---|---|---|
| 1 | P1 | UBAH | Data asas | Hanya posisi matang: umur ≥ maks(14, 1.5 × hari pegang backtest); x = hasil − KOS_PUSINGAN; uji kos 0.10/0.25/0.50% (`asasKaedah`) |
| 2 | P1 | UBAH | n | Semua n → n berkesan CR1 ikut hari beli dan G (lalai atas pulangan bersih; pilihan atas pulangan lebihan untuk perbandingan relatif); julat guna t(G − 1) (`nBerkesan`, `tKrit`) |
| 3 | P1 | UBAH | Pengecutan u1 | Ke arah prior khusus kaedah μ₀ (jangkaan Papan Penganalisis); B = τ̂²/(τ̂² + s²/n_eff), τ̂² ≥ s²/30; post = μ₀ + B(x̄_pangkas − μ₀) (`ebKecut`). Buang SKW_K = 20 ke min global |
| 4 | P1 | UBAH | Lorong | Pra-komit lorong ikut backtest/KAJIAN_LORONG2; jika dipilih ikut data hadapan, tolak SE·√((1 − ρ)/π) (`penaltiLorong`) |
| 5 | P1 | UBAH | Peringkat | Teras memerlukan skor ≥ 70, G ≥ 20, P(μ > 0) ≥ 0.9 dan P(4 teratas) ≥ 0.5; jika G < 20, maksimum "Calon (awal)" (`tahap`) |
| 6 | P2 | BUANG | Metrik bertindih | Kadar menang, median, tanpa 3 terbaik, rugi purata, kerugian terbesar dan sebenar ÷ backtest keluar daripada skor (kekal dipapar) |
| 7 | P2 | TAMBAH | Risiko dan konsistensi | r1 = CVaR 10% (≥ 3 dagangan) [15]; k2 = had bawah Wilson pecahan hari beli berpurata positif [10] |
| 8 | P2 | UBAH | Metrik dikekalkan | u1 posterior [25]; u2 = 21 × post ÷ hari purata [10]; u3 = lebihan atas penanda aras dalaman [5]; k1 = PF dihad 3 [10]; r2 = MAE ÷ ATR14 (atau ÷ √hari) [10]; b1 = B (bahagian bukti hadapan) [10]; b2 = semakan luar sampel 0–3 [5] |
| 9 | P2 | TAMBAH | Pintu dan agregasi | Pintu: G ≥ 10, matang ≥ 20, swing 3–30, metrik teras wujud, post > 0. Skor = exp(Σ wₖ ln maks(5, Pₖ)) dengan U40/K20/R25/B15; metrik sekunder hilang → persentil ke-25 + liputan % (`pintu`, `agregat`) |
| 10 | P2 | UBAH | Julat | Kalibrasi p5–p95 set backtest 431, bekukan dengan versi + tarikh; papar wajaran berkesan wᵢ·sdᵢ/Σw·sd, % tepu, korelasi sub-skor (`kalibrasiTiang`, `diagnostik`) |
| 11 | P3 | UBAH | "Stabil" | Monte Carlo 1,000 lelaran: u1 ~ posterior, wajaran × U(0.5, 1.5), togol aritmetik/geometrik → pangkat median, p5–p95, P(4 teratas); stabil jika ≥ 0.5 (`mcStabil`) |
| 12 | P3 | UBAH | Gabungan | Korelasi pulangan lebihan mingguan ≤ ρ_maks (tempat letak 0.7) DAN pertindihan ≤ 20%; satu kaedah setiap kelompok; pemberat 1/N; lapor purata sama-berat dan DM; kuota slot (`gabungan`) |
| 13 | P4 | TAMBAH | Pembekuan | Commit bertarikh: versi formula, set terpilih, peraturan slot/berhenti; jejaki gabungan beku lwn #1 sahaja lwn 4 rawak lwn SPY dalam `portfolio_slot/` |
| 14 | P4 | TAMBAH | Ujian ramalan skor | Spearman(skor_t, pulangan hadapan t+1…t+k) setiap minggu; jangan tala wajaran sebelum 8–12 minggu (`spearman`) |
| 15 | P4 | TAMBAH | Amaran, gantung, bersara | CUSUM bawah atas purata kohort harian, h dikalibrasi bootstrap; gantung pada 1.5× DD backtest atau tempoh DD > maks backtest; bersara jika P(μ ≤ 0) > 0.9 dengan G ≥ 20 (`cusumBawah`) |
| 16 | P4 | TAMBAH (kemudian) | Bukti kuat | DSR setiap dagangan ≥ 0.95 sebagai label KUAT selepas G ≥ 20; ganti "25% + 25% × lulus" dalam penganalisis.py dengan `kekalHL(t_bt, 431)`; PBO/CSCV ke atas matriks backtest harian dalam Python |
| — | — | KEKAL | Rangka | Julat tetap beku, empat tunjang, formula telus, arah pengecutan, had swing 3–30, pertindihan saham (sebagai semakan sekunder), maksimum 4 kaedah, isyarat seminggu dan trend sesi lalu (paparan) |

### Kod 1: fungsi statistik (diuji dalam Node 22)

Semakan yang telah dijalankan: Q(1.96) = 0.0250, Q(10) = 7.62e-24; EMAKS(123) = 2.60 dan EMAKS(431) = 3.01 (sepadan dengan scipy); `kekalHL(5, 431)` = 0.73; Wilson 11/20 → 0.342; DM(4, 0.5) = 1.26. Dalam contoh nota (n₀ = 30, μ₀ = 0.65%, n_eff = 10, x̄ = 3%, s = 8%), `ebKecut` memberi B = 0.25 dan posterior 1.24%, sama dengan formula Papan Penganalisis.

```javascript
/* ===== Skor kaedah swing v2: fungsi bantu (JS pelayar, tanpa pustaka) ===== */
const purata = a => a.reduce((s, x) => s + x, 0) / a.length;
const sisihan = a => { const m = purata(a); return Math.sqrt(a.reduce((s, x) => s + (x - m) ** 2, 0) / (a.length - 1)); };

/* (1) Taburan normal: ekor atas Q(x) = 1 − Φ(x), ralat pecahan < 1.2e-7 (erfc Chebyshev) */
function erfc(x) {
  const z = Math.abs(x), t = 1 / (1 + 0.5 * z);
  const r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 +
    t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
  return x >= 0 ? r : 2 - r;
}
const Q = x => 0.5 * erfc(x / Math.SQRT2);
const Phi = x => 1 - Q(x);
function QInv(p) { let lo = -40, hi = 40; for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (Q(m) > p) lo = m; else hi = m; } return (lo + hi) / 2; }
const randn = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };

/* (2) Nilai kritikal t dua hala 95% bagi darjah kebebasan G − 1 */
const T975 = [, 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131,
  2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042];
const tKrit = df => df < 1 ? Infinity : df <= 30 ? T975[df] : 1.96 + 2.4 / df;

/* (3) n berkesan berkelompok ikut hari beli (sama seperti penganalisis.py) */
function nBerkesan(tr) { // tr = [{x: pulangan bersih %, hari: 'YYYY-MM-DD'}]
  const n = tr.length; if (n < 2) return { n, G: n, neff: n };
  const m = purata(tr.map(t => t.x)), s2 = tr.reduce((s, t) => s + (t.x - m) ** 2, 0) / (n - 1);
  const g = new Map(); tr.forEach(t => g.set(t.hari, (g.get(t.hari) || 0) + (t.x - m)));
  const G = g.size; if (G < 5) return { n, G, neff: Math.min(n, G) };
  let ss = 0; g.forEach(v => { ss += v * v; });
  const Vcl = G / (G - 1) * ss / (n * n), Vind = s2 / n;
  return { n, G, neff: Math.min(n, n / Math.max(1, Vcl / Vind)) };
}

/* (4) Potongan backtest tidak linear gaya Harvey–Liu (Bonferroni atas M percubaan) */
function kekalHL(tBt, M) {
  if (!(tBt > 0)) return 0;
  const pAdj = Math.min(1, M * Q(tBt)); if (pAdj >= 0.5) return 0;
  return Math.min(1, QInv(pAdj) / tBt);
}

/* (5) Bayes empirik normal–normal. K = [{xbar, mu0, s2, neff}]; neff = 0 → posterior = prior.
   τ² dianggar merentas kaedah (kaedah momen) tetapi tidak dibenar di bawah s²/n0Maks (n0Maks = 30 = tetapan Papan Penganalisis) */
function ebKecut(K, n0Maks = 30) {
  K.forEach(k => { k.d = k.neff > 0 ? k.xbar - k.mu0 : 0; k.v = k.neff > 0 ? k.s2 / k.neff : Infinity; });
  const ada = K.filter(k => isFinite(k.v)), s2 = K.map(k => k.s2).sort((a, b) => a - b)[K.length >> 1];
  const tau2 = Math.max(s2 / n0Maks, ada.length ? purata(ada.map(k => k.d * k.d - k.v)) : 0);
  K.forEach(k => { k.B = isFinite(k.v) ? tau2 / (tau2 + k.v) : 0; k.post = k.mu0 + k.B * k.d;
    k.Vpost = isFinite(k.v) ? tau2 * k.v / (tau2 + k.v) : tau2; k.pPos = Phi(k.post / Math.sqrt(k.Vpost)); });
  return tau2;
}

/* (6) Penalti pilih lorong terbaik daripada dua: E[maks] − maks(E) = SE·√((1 − ρ)/π) */
const penaltiLorong = (se, rho) => se * Math.sqrt(Math.max(0, 1 - rho) / Math.PI);

/* (7) Jangkaan maksimum N skor-z nol (halangan DSR) */
const EMAKS = N => 0.4227843 * QInv(1 / N) + 0.5772157 * QInv(1 / (N * Math.E));

/* (8) Deflated Sharpe Ratio setiap dagangan */
function dsr(x, neff, SRbintang) {
  const n = x.length, m = purata(x), s = sisihan(x), SR = m / s;
  const g3 = x.reduce((t, v) => t + ((v - m) / s) ** 3, 0) / n, g4 = x.reduce((t, v) => t + ((v - m) / s) ** 4, 0) / n;
  return Phi((SR - SRbintang) * Math.sqrt(Math.max(1, neff - 1)) / Math.sqrt(Math.max(1e-9, 1 - g3 * SR + (g4 - 1) / 4 * SR * SR)));
}

/* (9) Wilson had bawah; CVaR; kecekapan modal */
function wilsonBawah(k, n, z = 1.96) { if (!n) return null; const p = k / n, d = 1 + z * z / n;
  return (p + z * z / (2 * n) - z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d; }
function cvar(x, a = 0.10, kMin = 3) { const s = [...x].sort((p, q) => p - q), k = Math.min(s.length, Math.max(kMin, Math.ceil(a * s.length)));
  return purata(s.slice(0, k)); }
const ekorModal = (post, hariPurata) => 21 * post / Math.max(1, hariPurata); // % setiap 21 hari dagangan setiap slot

/* (10) Peta julat beku dan agregasi tunjang */
const lin = (v, a, b) => v == null || isNaN(v) ? null : Math.min(1, Math.max(0, (v - a) / (b - a))) * 100;
function agregat(P, W, geo = true) { // P = {U,K,R,B} 0–100, W = wajaran tunjang
  let tw = 0, s = 0; for (const k in W) { if (P[k] == null) return null; tw += W[k]; }
  for (const k in W) s += geo ? W[k] / tw * Math.log(Math.max(5, P[k])) : W[k] / tw * P[k];
  return geo ? Math.exp(s) : s;
}

/* (11) Monte Carlo: hingar data (posterior u1) + gangguan wajaran + togol agregasi → P(4 teratas) */
function mcStabil(rows, W, kiraTunjang, B = 1000, top = 4) {
  // rows[i] = {post, Vpost, ...}; kiraTunjang(row, u1) → {U,K,R,B}
  const rk = rows.map(() => []);
  for (let b = 0; b < B; b++) {
    const w = {}; for (const k in W) w[k] = W[k] * (0.5 + Math.random());
    const geo = Math.random() < 0.5;
    rows.map((r, i) => [agregat(kiraTunjang(r, r.post + Math.sqrt(r.Vpost) * randn()), w, geo), i])
      .sort((p, q) => q[0] - p[0]).forEach(([, i], j) => rk[i].push(j + 1));
  }
  return rk.map(a => { a.sort((x, y) => x - y);
    return { med: a[a.length >> 1], p5: a[Math.floor(0.05 * a.length)], p95: a[Math.floor(0.95 * a.length)], pTop: a.filter(x => x <= top).length / a.length }; });
}

/* (12) Spearman (ujian ramalan skor), pengganda kepelbagaian, CUSUM bawah */
function spearman(a, b) { const rk = v => { const r = []; v.map((x, i) => [x, i]).sort((p, q) => p[0] - q[0]).forEach(([, i], j) => { r[i] = j + 1; }); return r; };
  const ra = rk(a), rb = rk(b), n = a.length; return 1 - 6 * ra.reduce((s, x, i) => s + (x - rb[i]) ** 2, 0) / (n * (n * n - 1)); }
const pengganda = (N, rho) => 1 / Math.sqrt(1 / N + (1 - 1 / N) * rho);
function cusumBawah(z, k = 0.5, h = 4) { let S = 0; const amaran = []; z.forEach((v, t) => { S = Math.max(0, S - v - k); if (S > h) { amaran.push(t); S = 0; } }); return amaran; }
```

### Kod 2: pendawaian skor v2 ke dashboard

Fungsi ini memakai `hariAntara`, `hasilL` dan `hariL` yang sudah wujud dalam `dashboard_v2.html`. Medan `atr14_pct` dan `tandaAras(r)` perlu disediakan: penanda aras dalaman ialah purata pulangan semua isyarat Lejar yang dibeli pada hari sama bagi tetingkap pegang yang sama. Semua nilai `TIANG_V2`, `KOS_PUSINGAN` dan `rhoMaks` ialah **tempat letak tanpa sumber** dan mesti dikalibrasi. Kalibrasi ini dibuat sekali di luar papan (Python atas set backtest 431), kemudian dibekukan dalam kod bersama nombor versi.

```javascript
/* ===== Skor kaedah swing v2: pendawaian (guna hariAntara, hasilL, hariL sedia ada dalam dashboard_v2.html) ===== */
const KOS_PUSINGAN = 0.25;   // % setiap pusingan — TEMPAT LETAK tanpa sumber; uji juga 0.10 dan 0.50
const N_PERCUBAAN = 431;     // set backtest yang pernah diuji (untuk potongan Harvey–Liu dan DSR)
const W_TUNJANG = { U: 40, K: 20, R: 25, B: 15 };
const W_V2 = { U: { u1: 25, u2: 10, u3: 5 }, K: { k1: 10, k2: 10 }, R: { r1: 15, r2: 10 }, B: { b1: 10, b2: 5 } };
/* TIANG: TEMPAT LETAK sahaja — ganti dengan kalibrasiTiang() atas set backtest 431, kemudian bekukan bersama versi + tarikh */
let TIANG_V2 = { u1: [0, 2.5], u2: [0, 6], u3: [-1, 1.5], k1: [1, 2.2], k2: [0.3, 0.7], r1: [-15, -4], r2: [-3, -0.5], b1: [0, 0.5], b2: [0, 3] };

function purataPangkas(x, a = 0.05) { const s = [...x].sort((p, q) => p - q), k = Math.floor(a * s.length); return purata(s.slice(k, s.length - k)); }

/* (A) Posisi matang sahaja (takrif Papan Penganalisis), bersih kos, pada lorong yang DIPRA-KOMIT */
function asasKaedah(rows, lor, btHari, hariIni, tandaAras) {
  // tandaAras(r): purata pulangan semua isyarat Lejar yang dibeli pada hari sama, tetingkap pegang sama
  const umurMin = Math.max(14, 1.5 * btHari);
  return rows.filter(r => hariAntara(r.tarikh_beli, hariIni) >= umurMin).map(r => {
    const u = hasilL(r, lor);
    return { x: u - KOS_PUSINGAN, lebih: u - tandaAras(r), hari: r.tarikh_beli, d: hariL(r, lor), mae: r.mae, atrPct: r.atr14_pct };
  }).filter(t => Number.isFinite(t.x));
}

/* (B) Metrik mentah satu kaedah. bt = {sd, hari, mu0, lulus}; mu0 = jangkaan Papan Penganalisis atau bt.avg × kekalHL(bt.t, N_PERCUBAAN) */
function metrikKaedah(M, bt) {
  const xs = M.map(t => t.x), ne = nBerkesan(M.map(t => ({ x: t.x, hari: t.hari }))); // konservatif; t.lebih → n berkesan lebih besar untuk perbandingan relatif
  const sw = xs.filter(v => v > 0).reduce((s, v) => s + v, 0), sl = -xs.filter(v => v < 0).reduce((s, v) => s + v, 0);
  const ikutHari = new Map(); M.forEach(t => { if (!ikutHari.has(t.hari)) ikutHari.set(t.hari, []); ikutHari.get(t.hari).push(t.x); });
  const hariPos = [...ikutHari.values()].filter(g => purata(g) > 0).length;
  const sd = xs.length >= 20 ? Math.max(5, sisihan(xs)) : Math.max(5, bt.sd || 8);
  const mae = M.filter(t => t.mae != null).map(t => t.atrPct ? t.mae / t.atrPct : t.mae / Math.sqrt(Math.max(1, t.d)));
  return { nMatang: M.length, G: ne.G, neff: ne.neff, xbar: xs.length ? purataPangkas(xs) : null, s2: sd * sd,
    hari: M.length ? purata(M.map(t => t.d)) : bt.hari, pf: xs.length ? (sl > 0 ? Math.min(3, sw / sl) : 3) : null,
    hariPositif: wilsonBawah(hariPos, ikutHari.size), cvar10: xs.length >= 3 ? cvar(xs) : null, maeAtr: mae.length ? purata(mae) : null,
    lebihDalaman: M.length ? purata(M.map(t => t.lebih)) : null, mu0: bt.mu0, btHari: bt.hari, lulus: bt.lulus };
}

/* (C) Sub-skor dan tunjang. Metrik sekunder hilang → imput persentil ke-25 merentas kaedah SEBELUM fungsi ini */
function subSkor(m, u1 = m.post) {
  const T = TIANG_V2;
  return { u1: lin(u1, ...T.u1), u2: lin(ekorModal(u1, m.hari), ...T.u2), u3: lin(m.lebihDalaman, ...T.u3),
    k1: lin(m.pf, ...T.k1), k2: lin(m.hariPositif, ...T.k2), r1: lin(m.cvar10, ...T.r1), r2: lin(m.maeAtr, ...T.r2),
    b1: lin(m.B, ...T.b1), b2: lin(m.lulus, ...T.b2) };   // b1 = bahagian anggaran daripada data hadapan sendiri (bebas daripada purata)
}
function tunjang(m, u1 = m.post) {
  const s = subSkor(m, u1), P = {};
  for (const g in W_V2) { let w = 0, t = 0; for (const id in W_V2[g]) { if (s[id] == null) continue; w += W_V2[g][id]; t += W_V2[g][id] * s[id]; } P[g] = w ? t / w : null; }
  return P;
}

/* (D) Pintu lulus/gagal dan peringkat */
function pintu(m) {
  const s = [];
  if (m.G < 10 || m.nMatang < 20) s.push(`BELUM CUKUP: ${m.G} hari beli, ${m.nMatang} matang`);
  if (!(m.btHari >= 3 && m.btHari <= 30)) s.push('bukan swing 3–30 hari');
  if (m.post == null || m.cvar10 == null || m.pPos == null) s.push('metrik teras tiada');
  else if (m.post <= 0) s.push('jangkaan bersih ≤ 0');
  return s;
}
function tahap(m) {
  if (pintu(m).length) return 'Belum layak';
  if (m.skor >= 70 && m.G >= 20 && m.pPos >= 0.9 && m.mc.pTop >= 0.5) return 'Teras';
  return m.skor >= 55 ? (m.G < 20 ? 'Calon (awal)' : 'Calon') : 'Pantau';
}

/* (E) Kira semua: kecut → skor geometrik → Monte Carlo kestabilan */
function kiraSkorV2(semua) { // semua = [metrikKaedah(...) + {kaedah}]
  ebKecut(semua);
  semua.forEach(m => { m.s = subSkor(m); m.P = tunjang(m); m.skor = agregat(m.P, W_TUNJANG); m.sebab = pintu(m); });
  const L = semua.filter(m => !m.sebab.length && m.skor != null);
  mcStabil(L, W_TUNJANG, tunjang, 1000).forEach((r, i) => { L[i].mc = r; });
  L.sort((a, b) => b.skor - a.skor).forEach((m, i) => { m.rk = i + 1; m.tahap = tahap(m); });
  return L;
}

/* (F) Diagnostik: wajaran berkesan, kadar tepu, korelasi sub-skor (|ρ| > 0.8 = kiraan berganda) */
function diagnostik(L) {
  const W = {}; for (const g in W_V2) Object.assign(W, W_V2[g]);
  const ids = Object.keys(W), out = {}; let jum = 0;
  ids.forEach(id => { const v = L.map(m => m.s[id]).filter(x => x != null), sd = v.length > 1 ? sisihan(v) : 0;
    out[id] = { sd, tepu0: v.filter(x => x <= 0).length / v.length, tepu100: v.filter(x => x >= 100).length / v.length, wsd: W[id] * sd }; jum += W[id] * sd; });
  ids.forEach(id => { out[id].wBerkesan = jum ? out[id].wsd / jum : null; });
  const kor = {}; ids.forEach((a, i) => ids.slice(i + 1).forEach(b => { const p = L.filter(m => m.s[a] != null && m.s[b] != null);
    if (p.length > 5) kor[a + '|' + b] = spearman(p.map(m => m.s[a]), p.map(m => m.s[b])); }));
  return { metrik: out, kor };
}
function kalibrasiTiang(nilaiBacktest) { // {u1: [nilai merentas 431 set], ...} → p5/p95
  const T = {}; for (const id in nilaiBacktest) { const s = nilaiBacktest[id].filter(Number.isFinite).sort((a, b) => a - b);
    T[id] = [s[Math.round(0.05 * (s.length - 1))], s[Math.round(0.95 * (s.length - 1))]]; } return T;
}

/* (G) Gabungan: calon diisih ikut skor; kor(a,b) = korelasi pulangan LEBIHAN mingguan portfolio maya setiap kaedah (Lejar Penuh) */
function pearson(a, b) { const n = Math.min(a.length, b.length); if (n < 3) return null;
  const ma = purata(a.slice(0, n)), mb = purata(b.slice(0, n)); let sab = 0, saa = 0, sbb = 0;
  for (let i = 0; i < n; i++) { const x = a[i] - ma, y = b[i] - mb; sab += x * y; saa += x * x; sbb += y * y; }
  return sab / Math.sqrt(saa * sbb); }
function gabungan(calon, kor, tindih, maks = 4, rhoMaks = 0.7, tindihMaks = 20) { // rhoMaks: TEMPAT LETAK tanpa sumber
  const pil = [];
  for (const x of calon) { if (pil.length >= maks) break;
    if (pil.every(y => kor(x.kaedah, y.kaedah) <= rhoMaks && tindih(x.kaedah, y.kaedah) <= tindihMaks)) pil.push(x); }
  const pas = pil.flatMap((x, i) => pil.slice(i + 1).map(y => kor(x.kaedah, y.kaedah))), rho = pas.length ? purata(pas) : 1;
  return { pil, pemberat: pil.map(() => 1 / pil.length), jangkaanSamaBerat: pil.length ? purata(pil.map(x => x.post)) : null, rho, DM: pengganda(pil.length || 1, rho) };
}
```

Urutan pelaksanaan yang disyorkan bermula dengan item 1–5 bersama `diagnostik()` sahaja, tanpa mengubah wajaran. Langkah ini mendedahkan berapa banyak susunan sekarang berubah apabila hanya posisi matang, n berkesan dan prior bersama dipakai. Selepas itu, item 6–10 dibuat sebagai satu versi baharu (v2) yang dipaparkan selari dengan v97 selama dua minggu sebelum v97 dibuang. Item 11–16 menyusul apabila G ≥ 20.
