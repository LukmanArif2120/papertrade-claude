# Pembinaan dan Penggredan Skor Kekuatan Industri (A–E) untuk Pemilihan Saham AS, Ufuk 10–21 Hari Dagangan

Nota penyelidik (18 Okt 2026). Semua dapatan di bawah diambil daripada abstrak dan ringkasan yang dipaparkan oleh enjin carian. WebFetch gagal (ralat DNS `ENOTFOUND`) bagi setiap domain yang dicuba (ideas.repec.org, duke.edu, ucsd.edu, alphaarchitect.com, msci.com, upenn.edu), jadi tiada teks penuh kertas yang dibaca. Angka yang disebut perlu disemak semula dengan kertas asal sebelum digunakan dalam spec. Istilah teknikal Inggeris dikekalkan dalam kurungan supaya padan dengan literatur.

## 1. Kualiti klasifikasi industri (GICS / SIC / Fama-French / Morningstar / berasaskan teks) dan kesannya pada momentum

### Takeaway
GICS menerangkan pergerakan bersama pulangan (return comovement) jauh lebih baik daripada SIC, NAICS dan Fama-French, dan kelebihannya paling besar bagi firma besar. Bagi momentum, rakan sebaya berasaskan teks yang kurang kelihatan (Hoberg-Phillips TNIC) memberi keuntungan momentum yang besar, manakala rakan sebaya SIC hanya memberi keuntungan kecil dan singkat. Tahap perincian klasifikasi juga mengubah sama ada isyarat itu berkelakuan sebagai momentum atau pembalikan.

### Cited Findings
- Bhojraj, Lee & Oler (2003), "What's My Line? A Comparison of Industry Classification Schemes for Capital Market Research", *Journal of Accounting Research* 41(5): 745–774, membandingkan SIC, NAICS, GICS dan algoritma Fama-French (1997). — [IDEAS/RePEc](https://ideas.repec.org/a/bla/joares/v41y2003i5p745-774.html); [vLex](https://law-journals-books.vlex.com/vid/what-s-my-line-855628061)
- Abstraknya: "GICS classifications are significantly better at explaining stock return comovements, as well as cross-sectional variations in valuation multiples, forecasted and realized growth rates, R&D expenditures, and various key financial ratios." Kelebihan GICS "is consistent from year to year and is most pronounced among large firms". Tiga skim lain "differ little from each other in most applications". — [IDEAS/RePEc](https://ideas.repec.org/a/bla/joares/v41y2003i5p745-774.html)
- Chan, Lakonishok & Swaminathan (2007, *Financial Analysts Journal*), "Industry Classifications and Return Comovement", mendapati pergerakan bersama dalam pulangan dan prestasi operasi yang berpunca daripada kesan industri lebih kuat bagi saham besar berbanding saham kecil. — [CFA Institute RPC](https://rpc.cfainstitute.org/research/financial-analysts-journal/2007/industry-classifications-and-return-comovement)
- Hoberg & Phillips (2018), "Text-Based Industry Momentum", *JFQA* 53(6): 2355–2388. Rakan sebaya dibina daripada huraian produk 10-K, dan hanya pasangan yang tidak berkongsi kod SIC dikekalkan. Kejutan pada rakan sebaya yang "kurang kelihatan" ini menghasilkan keuntungan momentum yang besar, dan dilaporkan mengatasi isyarat pulangan lalu firma itu sendiri. Rakan sebaya SIC tradisional hanya memberi keuntungan "small and short-lived". Penulis mentafsirkannya sebagai kurang perhatian (inattention) pelabur. — [IDEAS/RePEc](https://ideas.repec.org/a/cup/jfinqa/v53y2018i06p2355-2388_00.html); [Cambridge Core](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/textbased-industry-momentum/6E04891A7AD30C24C21CBDE37EC06BF4)
- Data TNIC Hoberg-Phillips (persamaan pasangan firma daripada teks 10-K) meliputi 1989–2023. — [Hoberg-Phillips Data Library](https://hobergphillips.tuck.dartmouth.edu/)
- Sebuah kajian 2022 (*International Journal of Finance & Economics*, "Industry momentum and reversals in stock markets") mendapati klasifikasi pada tahap lebih tinggi (lebih kasar) memberi pulangan momentum positif yang lebih tinggi. Klasifikasi yang terperinci pula memaparkan corak pembalikan jangka pendek dan sederhana. — [IDEAS/RePEc](https://ideas.repec.org/a/wly/ijfiec/v27y2022i3p3093-3138.html) (dapatan daripada ringkasan carian sahaja)
- Hou (2007, *RFS* 20(4): 1113–1138): kesan lead-lag firma besar ke firma kecil kebanyakannya berlaku dalam industri yang sama (intra-industry). Ia didorong oleh pelarasan perlahan terhadap berita negatif, dan lebih kuat dalam industri kecil, kurang kompetitif dan diabaikan. — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html)
- Cen, Chan, Dasgupta & Gao (2013, *Management Science*): kebanyakan peneraju industri juga mempunyai segmen dalam industri lain, jadi resapan maklumat boleh tersalur dan menyebabkan salah harga pada firma kecil yang hanya dalam satu bidang (pure-play). — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2013.1722)

### Inferences
- Morningstar/Moomoo (~145 industri) dari segi kehalusan terletak di antara GICS Industry (~74) dan GICS Sub-Industry (~163). Tiada kajian akademik yang ditemui menilai Morningstar secara langsung. Ia klasifikasi berasaskan aktiviti perniagaan yang diselenggara secara manual, jadi kualitinya munasabah dijangka lebih dekat kepada GICS berbanding SIC (inferens, belum diuji).
- Dapatan 2022 (tahap terperinci cenderung berbalik) dan Bhojraj et al. (kelebihan terutamanya bagi firma besar) mencadangkan risiko pada 145 kumpulan yang dikira sama berat. Kumpulan kecil yang dikuasai saham kecil mungkin berbalik dalam ufuk 1–4 minggu. Satu langkah yang munasabah ialah menguji dua tahap secara selari, iaitu 145 industri dan sektor/kumpulan lebih kasar, lalu pilih tahap yang monotonik pada ufuk 10–21 hari.
- Momentum berasaskan teks memberi isyarat paling kuat tetapi data TNIC tahunan dan tertangguh. Ia tidak sesuai untuk gred harian langsung, dan Moomoo pun tidak menyediakannya.

### Gaps
- Tiada kajian ditemui yang membandingkan Morningstar Industry dengan GICS bagi momentum.
- Angka tepat R² comovement dalam Bhojraj et al. tidak dapat dibaca kerana teks penuh tidak dapat diakses.
- Saiz dan tempoh keuntungan TNIC berbanding SIC dalam Hoberg-Phillips (bps sebulan, tempoh sampel) tidak diperoleh.

## 2. Agregasi: berwajaran nilai vs sama berat vs median; saham kecil/tidak cair; bilangan minimum; nilai luar (outlier)

### Takeaway
Moskowitz & Grinblatt (1999) menggunakan portfolio industri berwajaran nilai, dan kesan industri dilaporkan kekal selepas kawalan mikrostruktur. Kesan lead-lag dan pembalikan jangka pendek pula paling kuat dalam saham kecil, tidak cair dan meruap. Ini memberi alasan untuk mengurangkan pengaruh saham kecil dalam skor industri dengan menggunakan wajaran nilai/kecairan, median, atau sama berat yang dipangkas (trimmed). Tiada kajian ditemui yang menetapkan bilangan minimum ahli secara empirik.

### Cited Findings
- Moskowitz & Grinblatt (1999), "Do Industries Explain Momentum?", *Journal of Finance* 54(4): 1249–1290. Strategi momentum industri kekal menguntungkan selepas kawalan saiz, B/M, momentum saham individu, serakan keratan rentas (cross-sectional dispersion) purata pulangan, dan "potential microstructure influences". Selepas momentum industri dikawal, momentum saham "significantly less profitable". — [IDEAS/RePEc](https://ideas.repec.org/a/bla/jfinan/v54y1999i4p1249-1290.html); [AQR](https://www.aqr.com/Insights/Research/Journal-Article/Do-Industries-Explain-Momentum)
- Grundy & Martin (dipetik oleh Giannikos & Ji 2007): kesan industri tidak dapat menerangkan momentum sepenuhnya. Strategi industri rawak masih mendapat pulangan signifikan dalam bulan selain Januari. Giannikos & Ji juga mendapati keuntungan momentum industri global lebih besar pada bulan Januari. — [hasil carian, dipetik dalam ringkasan IDEAS/kertas susulan](https://ideas.repec.org/p/wop/chispw/352.html) (sumber sekunder)
- Hameed, Huang & Mian ("Industries and Stock Return Reversals"): pembalikan intra-industri lebih kuat bagi saham tidak cair, kecil dan sangat meruap, iaitu risiko kecairan ialah sumber pembalikan jangka pendek. Pembalikan berasaskan industri memberi 1.46% sebulan berbanding 1.05% bagi pembalikan seluruh pasaran (1963–2006). — [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/short-term-reversal-by-industry)
- Asness, Porter & Stevens (AQR working paper, data NYSE/AMEX/NASDAQ 1963–1998): pada ufuk pendek, komponen dalam industri dan merentas industri adalah signifikan dan berlawanan tanda. Kesan kontrarian dalam industri jangka pendek "driven largely by the bid-ask spread". — [AQR](https://www.aqr.com/Insights/Research/Working-Paper/Predicting-Stock-Returns-Using-IndustryRelative-Firm-Characteristics)
- Tesis Nguyen (17 portfolio industri AS, 1985–2018, dipetik dalam ringkasan carian): strategi lihat-belakang 1 bulan sama berat dan 12 bulan berwajaran nilai ialah yang paling menguntungkan. — [hasil carian; sumber tidak dapat dibuka](https://openaccess.nhh.no/nhh-xmlui/handle/11250/2609795) (sumber lemah, tesis)
- Chan, Lakonishok & Swaminathan (2007): kesan industri lebih kuat dalam saham besar. — [CFA Institute RPC](https://rpc.cfainstitute.org/research/financial-analysts-journal/2007/industry-classifications-and-return-comovement)
- Pengkritik amalan breadth/backtest mengingatkan bahawa perubahan ahli secara sejarah mesti diambil kira untuk mengelakkan bias kemandirian (survivorship bias). — [FMP insights](https://site.financialmodelingprep.com/insights/markets/how-market-breadth-can-reveal-risk-hidden-beneath-indexlevel-strength) (sumber pengamal)

### Inferences
- Bagi alam ~6,000 saham dengan harga ≥ USD5 dan ~145 kumpulan, purata ~41 saham sekumpulan, tetapi taburannya pasti condong. Banyak industri Morningstar mempunyai < 10 ahli. Sama berat mentah dalam kumpulan kecil akan dikuasai satu atau dua saham kecil yang melonjak, contohnya selepas laporan pendapatan atau FDA. Cadangan (inferens, belum diuji): gunakan median atau purata terpangkas (trimmed mean, potong 10% atas/bawah) pulangan ahli, atau wajaran punca kuasa dua permodalan pasaran (sqrt-cap). Tetapkan ambang minimum, contohnya ≥ 5–8 ahli, dan cantumkan kumpulan kecil ke sektor induk atau beri gred "tiada data".
- Wajaran nilai penuh menjadikan skor industri seperti Semikonduktor dikuasai NVDA. Ini kurang berguna untuk memilih saham individu bersaiz kecil-sederhana. Gabungan median (lebar penyertaan) dan wajaran nilai (peneraju; disokong Hou 2007, peneraju besar mendahului saham kecil) mungkin lebih bermaklumat.
- Penapis harga ≥ USD5 sudah membuang sebahagian kesan bid-ask yang mendorong pembalikan jangka pendek (Asness et al.), tetapi tidak semuanya.

### Gaps
- Tiada kajian ditemui yang menetapkan bilangan minimum ahli per kumpulan secara statistik.
- Tiada perbandingan langsung median vs purata vs berwajaran nilai bagi momentum industri pada ufuk 2–4 minggu.
- Butiran ujian mikrostruktur Moskowitz-Grinblatt (contohnya kesan bid-ask, lead-lag saham kecil) tidak dapat dibaca.

## 3. Tempoh lihat-belakang: 1M, 3M, 6M, 12-1, gabungan (gaya IBD), langkau minggu/bulan terkini, EWMA, pecutan

### Takeaway
Bagi industri, berbeza dengan saham, bulan terkini mengandungi maklumat (momentum industri 1 bulan paling kuat). Bagi saham individu, bulan terkini cenderung berbalik. Momentum saham juga lebih didorong oleh pulangan 12–7 bulan lalu (Novy-Marx). Jadi skor industri patut memasukkan bulan terkini tanpa langkau, manakala RS saham patut melangkau sekurang-kurangnya seminggu.

### Cited Findings
- Arnott, Clements, Kalesnik & Linnainmaa (memetik Moskowitz & Grinblatt 1999): pulangan industri lalu meramal keratan rentas pulangan industri, "and this predictability is at its strongest at the one-month horizon", tetapi ia berlanjutan sehingga setahun. — [ringkasan carian bagi kertas Wharton/Linnainmaa](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2018/03/Juhani.pdf); [Quantpedia](https://quantpedia.com/strategies/sector-momentum-rotational-system)
- Grobys & Kolari (2019): portfolio industri yang mengatasi pasaran pada bulan sebelumnya kemudiannya memberi pulangan purata yang jauh lebih tinggi, menyokong Moskowitz & Grinblatt. — [Osuva (Univ. Vaasa)](https://osuva.uwasa.fi/bitstream/10024/11757/2/Osuva_Grobys_Kolari_2019.pdf)
- Grobys, Ruotsalainen & Äijö (49 industri FF berwajaran nilai, Jul 1926–Sep 2014): tanpa pengurusan risiko, momentum industri 12-2, 6-2 dan 12-7 memberi purata kasar 1.06%, 0.76% dan 0.77% sebulan. — [ringkasan carian, CXO Advisory](https://www.cxoadvisory.com/volatility-effects/suppressing-industry-momentum-strategy-crashes/)
- Dikhit (2026), 48 industri FF, 1975–2024, membandingkan 12-1 dengan 12-0 long-only: bulan terkini "contains economically meaningful information—not just noise to be filtered out". — [Alpha Architect, "Skip-month mystery"](https://alphaarchitect.com/skip-month-mystery/); [IBKR Quant](https://www.interactivebrokers.com/campus/ibkr-quant-news/the-skip-month-mystery-what-last-months-returns-are-really-telling-you/) (ringkasan carian sahaja; laman tidak dapat dibuka)
- Melangkau seminggu antara pembentukan 1 bulan dan pemegangan menghapuskan kesan pembalikan jangka pendek bagi sampel saham keseluruhan, tetapi tidak bagi kumpulan industri. — [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/short-term-reversal-by-industry)
- Novy-Marx (2012, *JFE*), "Is Momentum Really Momentum?": momentum didorong terutamanya oleh prestasi 12 hingga 7 bulan sebelum pembentukan. Strategi 6-2 menguntungkan tetapi kurang berbanding 12-7, terutamanya bagi saham bermodal besar. Dalam kuintil saham terbesar, strategi 12-7 berwajaran nilai (atas 20% tolak bawah 20%) memberi hampir 10% setahun (1927–2008). — [CXO Advisory](https://www.cxoadvisory.com/?p=5944); [Equitable Growth](https://equitablegrowth.org/must-read-168/)
- Kajian A-share China (double sort pulangan × volum): kedudukan industri mengikut pulangan 6 bulan memberi keuntungan lebih tinggi berbanding 3, 9 dan 12 bulan. — [IJBE](https://ijbe.fcu.edu.tw/past_issues/NO.6-1/pdf/vol_6-1-3.pdf) (bukan AS)
- MSCI membina faktor momentum industri daripada kekuatan relatif berwajaran rakan sebaya sub-industri dalam tempoh enam bulan lepas, dan menyatakan faktor ini mempunyai pusing ganti (turnover) yang agak tinggi. — [MSCI blog](https://www.msci.com/research-and-insights/blog-post/understanding-the-industry-momentum-factor) (ringkasan carian; laman tidak dapat dibuka)
- Rating RS gaya IBD, menurut skrip komuniti TradingView (bukan dokumentasi rasmi IBD): 40% bagi 63 hari terkini dan 20% setiap satu bagi tetingkap 126, 189 dan 252 hari, dinyatakan sebagai persentil 1–99 merentas semua saham. Skrip lain menyebut suku terkini diberi "double weight". — [TradingView RS Rating](https://www.tradingview.com/script/lsLzfQqs-RS-Rating-Multi-Timeframe); [TradingView IBD-style](https://it.tradingview.com/script/SHE1xOMC-Relative-Strength-IBD-Style)

### Inferences
- Untuk ufuk pegangan 10–21 hari, bukti menyebelahi komponen jangka pendek bagi industri (1M, mungkin juga 3M), tanpa langkau. Ini berlawanan dengan RS saham yang patut melangkau 5 hari terkini (pembalikan jangka pendek saham, Asness et al., CXO). Satu cadangan gabungan (belum diuji): skor industri = 0.4·r(1M) + 0.3·r(3M) + 0.3·r(6M), masing-masing dalam pangkat persentil keratan rentas, iaitu mirip pemberat IBD tetapi memendekkan hujung panjang. Pecutan (1M − 3M/3) belum ada bukti akademik yang ditemui. Jika digunakan, ia perlu diuji sebagai komponen tambahan.
- Momentum 12-1 industri kekal menguntungkan (Grobys et al.), tetapi sumbangannya pada ufuk 2–4 minggu kurang jelas. 12-7 (Novy-Marx) dibuktikan bagi saham, bukan industri.

### Gaps
- Tiada sumber ditemui yang menguji EWMA (purata bergerak eksponen) momentum industri secara khusus.
- Tiada bukti ditemui tentang "momentum acceleration" bagi industri AS.
- Kaedah rasmi IBD Industry Group Rank (197 kumpulan) tidak ditemui dalam dokumentasi asal.
- Pemberat sebenar faktor industri-momentum MSCI Barra (separuh hayat, tempoh) tidak dapat disahkan kerana laman tidak dapat dibuka.

## 4. Lebar penyertaan (breadth) sebagai komponen

### Takeaway
Tiada kajian akademik ditemui yang menguji sama ada pecahan ahli industri yang positif atau di atas purata bergerak menambah kuasa ramalan melebihi pulangan industri. Bahan yang ada adalah bahan pengamal tanpa bukti pulangan. "Breadth of ownership" (Chen, Hong & Stein) ialah konsep lain, iaitu pemilikan institusi, bukan penyertaan harga.

### Cited Findings
- Bahan pengamal menerangkan breadth sektor sebagai ukuran sama ada kekuatan indeks disokong merentas pasaran atau tertumpu dalam kumpulan kecil. Ia memberi amaran bahawa bacaan 40% "should not be treated as a universal trigger", dan tiada isyarat tervalidasi dikemukakan. — [FMP insights](https://site.financialmodelingprep.com/insights/markets/how-market-breadth-can-reveal-risk-hidden-beneath-indexlevel-strength)
- Stage Analysis menerbitkan siri peratus saham AS di atas MA 150 hari bagi 11 sektor dan melabelnya sebagai penunjuk "contrarian", tanpa bukti pulangan. — [Stage Analysis](https://www.stageanalysis.net/blog/844063/sector-breadth-percentage-of-us-stocks-above-their-150-day-30-week-moving-averages)
- Yan & Zhao, "Industry herding and momentum" (kertas kerja NJIT Leir Center): momentum industri lebih kuat apabila "herding" pelabur rendah. — [NJIT Leir](https://research.njit.edu/leir/sites/research.leir/files/Yan_Herding_WP5.doc) (kertas kerja; dapatan daripada ringkasan)
- Hou (2007): peneraju besar mendahului saham kecil dalam industri yang sama. — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html)

### Inferences
- Breadth (contohnya pecahan ahli dengan pulangan 1M > 0, atau di atas MA50) secara statistik hampir berkorelasi dengan pulangan median industri. Ia berguna sebagai penapis keteguhan (robustness) terhadap nilai luar dalam kumpulan kecil, tetapi tidak boleh diandaikan menambah alfa tanpa ujian. Dapatan Hou (peneraju besar dahulu, saham kecil menyusul) memberi rasional teori bahawa breadth rendah dengan pulangan berwajaran nilai yang tinggi mungkin meramal susulan saham kecil. Ini hipotesis, bukan dapatan.
- Cadangan: jika breadth dimasukkan, berikan pemberat kecil (≤ 20–25%) dan uji tambahan nilainya melalui regresi Fama-MacBeth pulangan saham 10/21 hari ke hadapan atas pangkat pulangan industri dan pangkat breadth bersama.

### Gaps
- Tiada kertas akademik yang mengkaji "industry breadth" (pecahan ahli naik) sebagai peramal pulangan industri AS ditemui. Rujukan Zarowin dan Bullish Percent Index juga tidak menghasilkan bukti akademik dalam carian ini.
- Tiada bukti tentang Bullish Percent Index bagi industri.

## 5. Penggredan: kuintil keratan rentas vs ambang tetap; kestabilan/pusing ganti; pelicinan

### Takeaway
Tiada kajian khusus tentang pelicinan skor industri ditemui. Bukti kos dagangan (Novy-Marx & Velikov) menunjukkan bahawa julat beli/pegang (buy/hold spread), iaitu histeresis, ialah cara mudah paling berkesan untuk mengurangkan pusing ganti tanpa merosakkan isyarat. Bukti momentum industri 1 bulan (isyarat terkini paling kuat) pula memberi amaran bahawa pelicinan berlebihan melemahkan isyarat pada ufuk pendek.

### Cited Findings
- Novy-Marx & Velikov (2016, *RFS* 29(1): 104–147): memperkenalkan julat beli/pegang (terus memegang saham yang tidak lagi layak untuk dibeli baharu) ialah "the single most effective simple cost mitigation strategy". Kebanyakan anomali dengan pusing ganti sebelah satu bulanan < 50% kekal signifikan selepas kos, dan sedikit sahaja yang berpusing ganti lebih tinggi kekal signifikan. Kos dagangan mengurangkan keuntungan dan signifikan statistik dalam semua kes, lalu meningkatkan kebimbangan data snooping. — [NBER w20721](https://www.nber.org/papers/w20721); [Novy-Marx PDF](https://mysimon.rochester.edu/novy-marx/research/ToAatTC.pdf)
- MSCI: faktor momentum industri "relatively high-turnover". — [MSCI blog](https://www.msci.com/research-and-insights/blog-post/understanding-the-industry-momentum-factor)
- Pulangan industri bulan terkini membawa maklumat (Moskowitz-Grinblatt; Dikhit 2026). — [Quantpedia](https://quantpedia.com/strategies/sector-momentum-rotational-system); [IBKR Quant](https://www.interactivebrokers.com/campus/ibkr-quant-news/the-skip-month-mystery-what-last-months-returns-are-really-telling-you/)

### Inferences
- Kuintil keratan rentas (A = 20% teratas … E = 20% terbawah, ~29 industri setiap gred) lebih sesuai daripada ambang tetap. Ia neutral terhadap regim pasaran (dalam pasaran turun pun tetap ada gred A), selaras dengan cara literatur menilai portfolio susunan (sort). Ambang tetap (contohnya pulangan 3M > +10% = A) menjadikan taburan gred berubah mengikut regim, dan secara efektif mencampurkan isyarat pasaran dengan isyarat industri. Jika isyarat regim diperlukan, pisahkan sebagai penapis pasaran berasingan.
- Kestabilan: gunakan histeresis gaya julat beli/pegang, bukan purata skor. Contohnya, industri masuk A jika pangkat ≥ persentil 80 dan kekal A sehingga jatuh < persentil 70. Pendekatan ini mengurangkan pertukaran gred tanpa melambatkan respons pada perubahan besar. Pelicinan purata 5 hari pada skor mentah 1M mengurangkan bunyi tetapi melewatkan isyarat ~2–3 hari. Pada ufuk 10–21 hari, kelewatan itu mungkin bernilai ketara memandangkan bulan terkini paling bermaklumat. Ini perlu diuji secara empirik (separuh hayat autokorelasi pangkat).
- Diagnostik yang dicadangkan: (a) autokorelasi pangkat Spearman skor dari hari t ke t+5/t+21; (b) matriks peralihan gred (kebarangkalian A→A dalam 5 hari); (c) IC (korelasi pangkat skor vs pulangan 10/21 hari ke hadapan) mengikut ketinggalan (lag) 0, 1, 3 dan 5 hari untuk mengukur kadar pereputan isyarat.

### Gaps
- Tiada kajian ditemui tentang kesan pelicinan (averaging) skor momentum industri pada pereputan isyarat ufuk 2–4 minggu.
- Tiada bukti yang membandingkan kuintil dan ambang tetap bagi penggredan industri.

## 6. Interaksi dengan RS saham: susunan dua hala, momentum residual/terlaras industri, penggredan saham relatif kepada industri

### Takeaway
Momentum saham dan industri bertindih dengan ketara (Moskowitz-Grinblatt), tetapi tidak sepenuhnya (Grundy-Martin). Dalam industri, ada momentum signifikan pada ufuk sederhana dan pembalikan pada ufuk pendek (didorong bid-ask). Momentum residual (selepas faktor) kira-kira menggandakan Sharpe. Bagi ufuk 2–4 minggu, saham "pemenang" 1 bulan dalam industri pemenang mungkin berbalik relatif kepada rakan industrinya. Jadi kombinasi terbaik untuk ufuk pendek ialah industri kuat dengan saham yang mempunyai RS jangka sederhana kuat, bukan yang terlebih lonjak dalam minggu terakhir.

### Cited Findings
- Moskowitz & Grinblatt (1999): selepas momentum industri dikawal, momentum saham "significantly less profitable". — [IDEAS/RePEc](https://ideas.repec.org/a/bla/jfinan/v54y1999i4p1249-1290.html)
- Asness, Porter & Stevens (AQR, 1963–1998): ada kesan momentum dalam industri (within-industry) yang signifikan. Pada ufuk pendek, kesan dalam dan merentas industri signifikan dan berlawanan tanda. Pada ufuk sederhana, kedua-duanya signifikan dan sama tanda. Memecahkan ciri kepada komponen industri dan dalam-industri meningkatkan ramalan. — [AQR](https://www.aqr.com/Insights/Research/Working-Paper/Predicting-Stock-Returns-Using-IndustryRelative-Firm-Characteristics)
- Simpson, Giudici & Emery (1931–2010, bulanan): menjual pendek saham pemenang dalam industri pemenang memberi pulangan negatif. Strategi gabungan "beli saham kalah dalam industri menang" memberi purata kasar 4.08% sebulan, berbanding pembalikan konvensional 3.25% dan momentum industri biasa 1.59% (ringkasan sekunder). — [CXO Advisory](https://cxoadvisory.com/technical-trading/combining-return-reversal-and-industry-momentum)
- Sebuah kajian global melaporkan bahawa momentum industri dan saham adalah bebas (independent), bercanggah dengan dapatan interaksi di atas. — [ringkasan carian; sumber di Springer FIN](https://jfin-swufe.springeropen.com/track/pdf/10.1186/s40854-019-0155-z)
- Pembalikan intra-industri (Australia): saham besar memaparkan pembalikan dalam industri (pemenang industri kalah kepada yang kalah dalam bulan berikutnya) apabila momentum harga dikawal, tetapi momentum industri mendominasi. — [Monash](https://research.monash.edu/en/publications/co-existence-of-short-term-reversals-and-momentum-in-the-australi/)
- Kajian 1968–2010: strategi pembalikan intra-industri mengasingkan pembalikan jangka pendek daripada momentum merentas industri. Pembalikan tanpa syarat dicemari komponen industri. — [NUS](https://web2-bschool.nus.edu.sg/wp-content/uploads/media_rp/publications/BwXb81392625636.pdf) (ringkasan carian)
- Blitz, Huij & Martens (2011): momentum residual (residu regresi FF3 36 bulan, diskalakan dengan volatiliti) memberi Sharpe kasar tahunan 0.90 berbanding 0.45 bagi momentum pulangan total, dan keuntungan terlaras risiko kira-kira dua kali ganda. Huij & Lansdorp (2017, AS 1986–2008): 1.28 berbanding 0.74. Blitz, Hanauer & Vidojevic (Dis 1925–Dis 2015): Sharpe bulanan 0.48 berbanding 0.25. — [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/stripping-risks-from-a-stock-momentum-strategy/); [EUR repub](https://repub.eur.nl/pub/22252); [CXO idiosyncratic](https://www.cxoadvisory.com/momentum-investing/idiosyncratic-pure-or-residual-momentum-as-a-stock-return-predictor) (angka daripada ringkasan sekunder)
- Novy-Marx menyediakan faktor momentum terlaras industri (UMD*) dan dalam-industri (UMDN). — [Novy-Marx data library](https://mysimon.rochester.edu/novy-marx/data_lib/OSoV/index.html); [butiran pembinaan](https://mysimon.rochester.edu/novy-marx/data_lib/OSoV/intra_industry_fact_details.html)

### Inferences
- Bagi sistem ini, yang memilih saham individu untuk 10–21 hari, cadangannya (belum diuji) ialah: (1) gred industri (A–E) sebagai penapis pertama; (2) dalam industri gred A/B, gunakan RS saham relatif kepada industri jangka sederhana (3–6M, langkau 5 hari) atau momentum residual; (3) elak saham yang sudah melonjak jauh di atas industri dalam 5–10 hari terakhir, berdasarkan bukti pembalikan dalam industri ufuk pendek.
- Penilaian wajib: jadual susunan dua hala 5×5 (gred industri × kuintil RS saham) bagi pulangan 10 dan 21 hari ke hadapan, untuk melihat sama ada gred industri menambah nilai dalam setiap kuintil RS saham, dan sebaliknya.
- Percanggahan (Simpson et al. menunjukkan interaksi kuat; kajian global menunjukkan kebebasan) bermakna kesan interaksi mesti diuji dalam data sendiri.

### Gaps
- Tiada kajian AS ditemui yang secara langsung melaporkan susunan dua hala "saham kuat × industri kuat" pada ufuk 2–4 minggu dengan pulangan setiap sel.
- Angka Simpson et al. datang daripada ringkasan sekunder, dan butiran pembinaan tidak diketahui.

## 7. Kebergantungan regim: pasaran menurun, volatiliti tinggi, lantunan (momentum crash)

### Takeaway
Momentum (saham, dan secara umumnya strategi pemenang-tolak-penyalah) mengalami kejatuhan teruk dalam "panic states": selepas pasaran merosot, ketika volatiliti tinggi, dan bertepatan dengan lantunan pasaran. Kejatuhan ini sebahagiannya boleh diramal, dan strategi dinamik menggandakan Sharpe. Kesan ini terutamanya pada kaki pendek (short leg). Bagi strategi long-only, risikonya ialah industri gred A yang beta rendah ketinggalan semasa lantunan.

### Cited Findings
- Daniel & Moskowitz (2016, *JFE* 122(2): 221–247), "Momentum Crashes": kerugian momentum berkelompok dalam keadaan "panic" selepas kejatuhan pasaran, ketika volatiliti tinggi, dan bertepatan dengan lantunan pasaran yang mendadak. Selepas pasaran merosot, portfolio momentum cenderung panjang pada saham beta rendah (pemenang) dan pendek pada saham beta tinggi (penyalah). Strategi yang meramal min dan varians momentum menghasilkan Sharpe tanpa syarat "approximately double" strategi statik. Dapatan ini teguh merentas tempoh, pasaran antarabangsa dan kelas aset. — [NBER w20439](https://www.nber.org/papers/w20439); [Columbia PDF](https://business.columbia.edu/sites/default/files-efs/pubfiles/4607/mom11.pdf)
- Grobys, Ruotsalainen & Äijö: pengurusan risiko (penskalaan volatiliti) bagi momentum industri 49 FF bertujuan meredam kejatuhan strategi momentum industri. Angka tanpa pengurusan risiko: 12-2 = 1.06% sebulan. — [CXO Advisory](https://www.cxoadvisory.com/volatility-effects/suppressing-industry-momentum-strategy-crashes/)
- Grobys & Kolari (2019) melanjutkan analisis mikrostruktur Moskowitz-Grinblatt kepada korelasi bersyarat dari segi risiko ekor dan kesan "optionality" bagi strategi industri jangka pendek. — [Osuva](https://osuva.uwasa.fi/bitstream/10024/11757/2/Osuva_Grobys_Kolari_2019.pdf)
- Yan & Zhao: momentum industri lebih kuat apabila herding rendah. — [NJIT Leir](https://research.njit.edu/leir/sites/research.leir/files/Yan_Herding_WP5.doc)
- Giannikos & Ji (2007): keuntungan momentum industri global lebih besar pada bulan Januari. — [sumber sekunder dalam carian](https://ideas.repec.org/p/wop/chispw/352.html)

### Inferences
- Untuk sistem long-only: dalam regim "panic" (contohnya SPY di bawah MA200 selepas penurunan 2 tahun, atau VIX tinggi lalu lantunan tajam), gred A yang dibina daripada 3–6M cenderung memilih industri defensif beta rendah dan ketinggalan semasa lantunan. Komponen 1M bertindak balas lebih cepat terhadap lantunan. Ini menyokong pemberat lebih tinggi pada 1M, atau memperkecilkan saiz/pengecualian belian baharu dalam keadaan panic. Ini inferens daripada Daniel-Moskowitz, bukan ujian khusus industri.
- Laporkan prestasi gred mengikut regim (pasaran naik/turun, VIX tinggi/rendah) secara berasingan, bukan purata sahaja.

### Gaps
- Tiada bukti khusus ditemui tentang kejatuhan momentum industri jangka pendek (1M) berbanding 12-1 semasa lantunan.
- Angka kejatuhan Daniel-Moskowitz (contohnya 2009) tidak dibaca daripada teks penuh.

## 8. Perangkap penilaian statistik dan cara mengesahkan gred

### Takeaway
Gunakan ambang t > 3.0 (Harvey-Liu-Zhu) kerana banyak varian diuji. Uji monotonik merentas semua gred (Patton-Timmermann), bukan atas-tolak-bawah sahaja. Ambil kira kos dan pusing ganti. Pulangan ufuk 10–21 hari yang dikira setiap hari bertindih dan memerlukan ralat piawai HAC.

### Cited Findings
- Harvey, Liu & Zhu (2016, *RFS*; NBER w20592), "…and the Cross-Section of Expected Returns": faktor baharu perlu melepasi nisbah t > 3.0, bukan ~2.0. Rangka ujian berganda ini membenarkan korelasi antara ujian dan data hilang, serta menyediakan siri masa ambang signifikan sejak 1967. Satu sumber sekunder memetik ambang Bonferroni ~3.75 bagi ujian semasa (kaedah berbeza). — [NBER w20592](https://www.nber.org/papers/w20592); [SSRN 2513152](https://papers.ssrn.com/abstract=2513152); [Advisor Perspectives](https://www.advisorperspectives.com/commentaries/2015/09/17/empirical-finance-meeting-fiduciary-standards-through-skepticism-not-cynicism)
- Patton & Timmermann (2010, *JFE*), "Monotonicity in asset returns: New tests with applications to the term structure, the CAPM, and portfolio sorts": membandingkan purata portfolio atas dan bawah sahaja tidak mencukupi untuk menguji hubungan monotonik. Ujian MR menyemak semua perbezaan bersebelahan. H0: perbezaan bertanda lemah dalam arah bertentangan; H1: semua perbezaan positif. Inferens bootstrap, tak parametrik. — [Patton (Duke) PDF](https://public.econ.duke.edu/~ap172/Patton_Timmermann_sorts_JFE_Dec2010.pdf); [kertas kerja 2009](https://rady.ucsd.edu/_files/faculty-research/timmermann/portfolio_sorts_30apr09_1.pdf)
- Mengikut ringkasan carian bagi versi kertas kerja, inferens ujian-t standard boleh diterbalikkan, dan kesan pembalikan jangka pendek, momentum serta hubungan saiz "are shown not to hold monotonically in post-1963 data". AMARAN: versi terbitan JFE tidak dapat dibaca untuk mengesahkan kenyataan ini. Kenyataan ini mungkin tidak tepat atau berbeza dalam versi akhir. — [ringkasan carian](https://rady.ucsd.edu/_files/faculty-research/timmermann/portfolio_sorts_30apr09_1.pdf)
- Pakej R `monotonicity` (CRAN v1.3.1) melaksanakan ujian ini. `monoRelation` menerima sehingga 15 portfolio dengan pilihan bootstrap. — [CRAN](https://search.r-project.org/CRAN/packages/monotonicity/index.html)
- Kritikan (*Journal of Empirical Finance* 2013): ujian MR pada asasnya hanya menguji arah monotonik. Apabila hubungan tidak monotonik atau meningkat secara lemah, ujian boleh "falsely establish" hubungan meningkat ketat dengan kebarangkalian tinggi. — [UZH PDF](https://uzh.ch/cmsssl/econ/dam/jcr:ffffffff-935a-b0d6-ffff-ffffd419e218/jef_2013.pdf)
- Novy-Marx & Velikov: kos dagangan mengurangkan keuntungan dan signifikan statistik dalam semua kes, lalu meningkatkan kebimbangan data snooping. — [NBER w20721](https://www.nber.org/papers/w20721)
- Ujian breadth/sektor perlu mengambil kira perubahan ahli secara sejarah (survivorship bias). — [FMP insights](https://site.financialmodelingprep.com/insights/markets/how-market-breadth-can-reveal-risk-hidden-beneath-indexlevel-strength)

### Inferences
- Pulangan bertindih: jika gred dikira setiap hari dan pulangan 21 hari ke hadapan dinilai setiap hari, setiap cerapan bertindih 20/21. Ralat piawai biasa akan terlalu kecil (lebih kurang √21 kali ganda). Gunakan Newey-West dengan ketinggalan ≥ h−1 (20 bagi 21 hari, 9 bagi 10 hari), atau sampel tidak bertindih (rebalans setiap 10/21 hari), atau portfolio bertindih gaya Jegadeesh-Titman (purata h portfolio kohort, dengan siri pulangan harian tidak bertindih). Ini amalan standard; rujukan primer tidak dibaca dalam sesi ini.
- Bias pandang ke hadapan (look-ahead) klasifikasi: industri Morningstar/Moomoo yang diambil hari ini ialah klasifikasi semasa. Dalam backtest, saham yang telah bertukar industri (contohnya META, GOOGL dalam penstrukturan GICS 2018) diletakkan dalam kumpulan yang salah secara sejarah. Penyelesaian: simpan petikan (snapshot) klasifikasi harian mulai sekarang. Dalam backtest lama, nyatakan had ini dan uji keteguhan dengan klasifikasi lain.
- Bias kemandirian: alam 6,000 saham semasa tidak termasuk saham yang telah dinyahsenarai. Pulangan industri sejarah akan berat sebelah ke atas, terutamanya dalam industri kecil.
- Pengesahan gred yang dicadangkan:
  1. Pulangan purata ke hadapan 10/21 hari bagi saham dalam setiap gred A–E (sama berat), dengan t Newey-West.
  2. Spread A − E dengan sasaran t > 3.0 (HLZ) kerana pelbagai varian lihat-belakang/agregasi diuji.
  3. Ujian MR Patton-Timmermann merentas 5 gred (bootstrap), dengan amaran kritikan JEF 2013. Laporkan juga semua perbezaan bersebelahan (A−B, B−C, …).
  4. IC Spearman harian dengan purata dan t-stat HAC.
  5. Ulangi mengikut regim dan subtempoh (separuh pertama/kedua).
  6. Bahagikan sampel kepada set pembinaan/ujian (out-of-sample), dan kekalkan rekod semua varian yang diuji (bilangan ujian) untuk pelarasan ujian berganda.

### Gaps
- Status sebenar dapatan Patton-Timmermann bagi portfolio momentum (monotonik atau tidak) dalam versi terbitan tidak dapat disahkan.
- Rujukan primer Newey-West (1987) dan Jegadeesh-Titman (1993) tentang pembinaan portfolio bertindih tidak dibaca dalam sesi ini, walaupun kaedahnya standard.
- Tiada kajian ditemui yang mengukur saiz bias look-ahead klasifikasi industri bagi momentum industri.
