# Skor komposit (0–100%) untuk menyusun kaedah dagangan: normalisasi, wajaran, agregasi, kepekaan dan contoh sistem penarafan sebenar

> Nota kaedah kerja: akses rangkaian sesi ini menyekat pengambilan halaman penuh (WebFetch/curl ke oecd.org, morningstar.com, darwinex.com, europa.eu ditolak proksi, 22 Okt 2026). Semua dapatan di bawah diambil daripada petikan/ringkasan enjin carian bagi sumber yang dinamakan, bukan bacaan teks penuh. Angka yang kritikal (cth. formula MRAR, had Quantopian) patut disemak semula dengan dokumen asal sebelum dijadikan peraturan.
>
> Konteks reka bentuk yang dinilai ("Skor kaedah swing"): 13 metrik dipetakan linear ke 0–100 pada julat tetap (cth. purata pulangan −3% → 0, +6% → 100; kadar menang 30% → 0, 70% → 100; profit factor 0.8 → 2.5; purata MAE −10% → 0), wajaran tunjang Untung 40 / Konsisten 25 / Risiko 20 / Bukti 15; metrik hilang digugurkan dan wajaran dinormal semula; peringkat Teras ≥ 70, Calon 55–69, Pantau < 55; lencana "stabil" jika kekal 4 teratas di bawah 3 set wajaran. Data: ~123 kaedah, ~4,400 dagangan, ~2 minggu.

## 1. Normalisasi: julat tetap linear lwn skor-z lwn pangkat persentil lwn logistik; kestabilan masa, pencilan dan had (capping)

### Takeaway
Buku Panduan OECD/JRC tidak menetapkan satu kaedah "terbaik": min-max/julat tetap mudah difahami tetapi peka pencilan dan boleh membesarkan pengaruh metrik yang julatnya sempit; skor-z memberi pencilan pengaruh lebih besar; pangkat kebal pencilan tetapi membuang magnitud. Untuk papan yang mahu ambang mutlak (Teras ≥ 70) dan perbandingan antara minggu, julat tetap ("goalposts") yang dibekukan + had eksplisit ialah pilihan yang wajar — tetapi lebar julat itu sendiri ialah wajaran tersembunyi dan mesti diperiksa.

### Cited Findings
- Buku Panduan rasmi: *Handbook on Constructing Composite Indicators: Methodology and User Guide* (OECD/JRC, 2008; Nardo, Saisana, Saltelli, Tarantola [JRC], Hoffmann, Giovannini [OECD]; ISBN 978-92-64-04345-9) — [JRC repository JRC47008](https://publications.jrc.ec.europa.eu/repository/handle/JRC47008); PDF: [OECD 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Min-max menormalkan setiap penunjuk kepada julat seragam [0,1] dengan menolak nilai minimum dan membahagi dengan julat; nilai ekstrem/pencilan boleh memesongkan penunjuk yang ditransformasi; ia juga boleh melebarkan penunjuk yang terletak dalam selang sempit sehingga pengaruhnya lebih besar daripada di bawah skor-z — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Skor-z (piawaian) menukar penunjuk ke skala sepunya min 0, sisihan piawai 1; penunjuk dengan nilai ekstrem mempunyai kesan lebih besar pada komposit; Buku Panduan mencadangkan pembetulan seperti mengecualikan skor terbaik/terburuk (trimming) atau wajaran berbeza — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Pangkat (ranking) mengelak herotan pencilan tetapi membuang magnitud perbezaan — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf); [Mazziotta & Pareto, Istat 2013](https://www.istat.it/en/files/2013/12/Rivista2013_Mazziotta_Pareto.pdf)
- Mazziotta & Pareto mencadangkan transformasi pangkat, skor-z atau min-max untuk perbandingan relatif dengan wajaran subjektif (sama atau berbeza), dan menyatakan skor-z hanya menyokong perbandingan relatif dari masa ke masa (bukan mutlak) — [Mazziotta & Pareto, "Methods for constructing composite indices", Istat 2013](https://www.istat.it/en/files/2013/12/Rivista2013_Mazziotta_Pareto.pdf)
- Buku Panduan menasihatkan nilai ekstrem diperiksa kerana ia boleh menjadi penanda aras yang tidak disengajakan — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Laporan JRC 2005 *Tools for Composite Indicators Building* (EUR 21682) merangkumi langkah yang sama: kaedah wajaran dan agregasi, data hilang, membawa penunjuk ke skala sepunya, dan ujian keteguhan melalui analisis ketidakpastian/kepekaan — [JRC31473](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC31473/EUR%2021682%20EN.pdf)
- Contoh dunia sebenar normalisasi relatif: Morningstar memberi bintang mengikut jalur persentil dalam kategori (10% teratas 5★, 22.5% seterusnya 4★, 35% tengah 3★, 22.5% 2★, 10% terbawah 1★) — [Morningstar Disclosure Statement](https://profile.morningstar.com/ISR/MorningstarDisclosure.html); [Morningstar: Rating for Funds](https://www.morningstar.com/investing-terms/morningstar-rating-for-funds)
- Contoh normalisasi "kestabilan relatif": atribut Risk Stability Darwinex mengukur kestabilan VaR, bukan paras mutlaknya — VaR yang berayun antara 8% dan 16% mendapat skor lebih rendah daripada yang berayun antara 40% dan 44% — [Darwinex: Risk Stability](https://help.darwinex.com/risk-stability-attribute)
- Contoh had bawah penyebut: kod komuniti skor peraduan Quantopian meletakkan lantai turun naik 2% (supaya pulangan/turun naik tidak meletup apabila turun naik sangat kecil); seorang pengulas forum menyatakan ia tidak sepadan dengan definisi 63 hari dalam peraturan rasmi — [Quantopian archive: contest score computation](https://quantopian-archive.netlify.app/forum/threads/context-score-computation.html)

### Inferences
- Perbandingan ringkas untuk papan pelayar:
  | Kaedah | Kestabilan dari minggu ke minggu | Pencilan | Ambang mutlak (≥70) bermakna? | Catatan |
  |---|---|---|---|---|
  | Julat tetap linear + had (semasa) | Tinggi: skor kaedah A tidak berubah kerana kaedah B masuk/keluar | Dihad oleh "clip" pada 0/100 | Ya | Julat arbitrari; tepu di hujung (+6% dan +15% kedua-duanya 100) |
  | Skor-z | Rendah: min/sd sampel berubah setiap minggu | Pencilan mendominasi kecuali dipangkas/winsorize | Tidak | Perlu winsorize ±3σ |
  | Pangkat persentil | Rendah–sederhana: relatif kepada set kaedah semasa | Kebal | Tidak (sentiasa ~30% kaedah ≥ persentil ke-70) | Sesuai untuk jalur gaya Morningstar |
  | Logistik / "soft clip" | Tinggi jika parameter dibekukan | Tepu lembut, kekal membeza di hujung | Ya | Lebih sukar diterangkan; tiada sumber khusus ditemui |
- Lebar julat = wajaran tersembunyi. Dalam julat tetap, sumbangan berkesan metrik i kepada variasi skor lebih kurang wᵢ × sd(sub-skorᵢ merentas 123 kaedah) (ditambah kesan korelasi). Jika julat kadar menang 30–70% terlalu lebar berbanding taburan sebenar (cth. kebanyakan kaedah 45–55%), sub-skor itu hampir malar dan wajarannya "hilang"; jika julat purata MAE terlalu sempit, ia mendominasi. Ini selari dengan amaran Buku Panduan tentang min-max dan selang sempit. Semakan mudah di papan: paparkan sd setiap sub-skor dan "wajaran berkesan" = wᵢ·sdᵢ / Σ(w·sd).
- Cara praktikal menetapkan julat: ambil persentil ke-5 dan ke-95 taburan merentas kaedah (atau taburan backtest set 431 yang lebih besar) dalam satu tempoh kalibrasi, bekukan, dan semak semula hanya pada jadual tetap (cth. suku tahunan) — ini mengekalkan kestabilan masa gaya "goalpost" tetapi julatnya berasaskan data, bukan tekaan.
- Had (capping) dua hala sudah dibuat secara tersirat oleh peta 0–100; tambah pelaporan berapa kaedah tepu pada 0 atau 100 bagi setiap metrik. Jika > ~20% tepu di 100, julat terlalu sempit untuk membezakan kaedah terbaik — isu utama kerana matlamat ialah memilih 3–4 terbaik, bukan menapis yang buruk.
- Paparkan pangkat persentil di sebelah skor mutlak: skor mutlak untuk peringkat Teras/Calon/Pantau, persentil untuk perbandingan relatif.

### Gaps
- Tiada sumber berwibawa ditemui yang membandingkan normalisasi logistik/sigmoid khusus untuk skor strategi dagangan.
- Teks penuh Bab normalisasi Buku Panduan (termasuk jadual pro/kontra lengkap dan nombor halaman) tidak dapat dibaca kerana sekatan rangkaian; dapatan bergantung pada petikan carian.

## 2. Wajaran: sama rata lwn pakar lwn berasaskan data (kuasa ramalan luar sampel, PCA, entropi, AHP); risiko kejuruteraan berlebihan; kiraan berganda metrik berkorelasi

### Takeaway
Bukti psikometrik dan ramalan menunjukkan wajaran sama rata atau "kasar" sering meramal luar sampel sama baik atau lebih baik daripada wajaran yang dipadankan pada data, terutamanya apabila sampel kecil — tepat seperti keadaan 2 minggu data. Wajaran berasaskan data (regresi, PCA, entropi) belum wajar sekarang; yang lebih penting ialah menghapuskan kiraan berganda: purata pulangan, profit factor, kadar menang dan jangkaan (expectancy) berkait secara mekanikal dan secara tersirat menaikkan wajaran tunjang Untung.

### Cited Findings
- Kebanyakan penunjuk komposit menggunakan wajaran sama rata; ini bermaksud semua pemboleh ubah "bernilai" sama, tetapi ia juga boleh menyembunyikan ketiadaan asas statistik/empirik bagi wajaran — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Buku Panduan menasihatkan analisis keteguhan terhadap mekanisme memasukkan/mengecualikan penunjuk tunggal, skema normalisasi, imputasi data hilang dan pilihan wajaran — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Dawes (1979) mentakrif model linear "tidak wajar" (improper) sebagai model yang wajarannya diperoleh secara tidak optimum (sama rata, rawak, intuitif) dan berhujah wajaran unit sangat teguh untuk meramal kriteria berangka; dalam contoh kemasukan siswazah, gabungan sama rata GRE, GPA dan selektiviti berkorelasi 0.48 dengan penilaian fakulti kemudian, lebih tinggi daripada pertimbangan jawatankuasa (0.19) dan lebih tinggi daripada wajaran regresi yang disahkan silang — [Dawes 1979, American Psychologist 34(7):571–582](https://www.researchgate.net/publication/232597503_The_robust_beauty_of_improper_linear_models_in_decision_making)
- "Flat maximum effect" (Wainer 1976): menggantikan wajaran optimum dengan wajaran sama hanya merugikan sedikit varians terjelas jika peramal diarahkan dengan betul (tanda betul); ruang wajaran hampir optimum adalah luas — [ringkasan literatur dalam Dawes/kajian berkaitan](https://www.researchgate.net/publication/232597503_The_robust_beauty_of_improper_linear_models_in_decision_making)
- Ujian moden: regresi wajaran sama rata kerap mengatasi regresi berganda biasa dan model regresi lain, terutamanya dengan set latihan kecil, tetapi tiada satu model ringkas yang terbaik pada semua set data; penulis juga mengkritik Dawes kerana menilai dengan korelasi, bukan fungsi kerugian regresi — [Lichtenberg & Şimşek, PMLR 58](http://proceedings.mlr.press/v58/lichtenberg17a/lichtenberg17a.pdf)
- Analisis teori: model "tidak wajar" boleh dirumus semula sebagai penganggar wajar satu peramal dengan had atas ralat kuasa dua min dan varians lebih rendah daripada OLS — [Psychometrika, "A Constrained Linear Estimator for Multiple Regression"](https://link.springer.com/article/10.1007/s11336-010-9162-8)
- Wajaran entropi: kebarangkalian pembalikan pangkat (rank reversal) meningkat apabila entropi wajaran meningkat (simulasi dalam konteks AHP) — [Fedrizzi & Predella, ODS 2017](https://iris.unitn.it/retrieve/e3835194-37ee-72ef-e053-3705fe0ad821/Fedrizzi-Predella-ODS2017.pdf)
- Kaedah hibrid entropi + AHP + TOPSIS dicadangkan kerana wajaran TOPSIS mesti ditentukan secara subjektif oleh pembuat keputusan — [Entropy 22(2):259, 2020](https://www.doi.org/10.3390/E22020259)
- Pembalikan pangkat berlaku untuk hampir setiap kaedah MCDM dan implikasinya masih dibahaskan — [arXiv 2312.03006, Multi-Weight Ranking](https://arxiv.org/pdf/2312.03006); ulasan kaedah pembetulan untuk TOPSIS/AHP — [Informatica 2024](https://puffbird.ijs.si/index.php/informatica/article/view/4144/2743)
- Darwinex mereka 12 Atribut Boleh Labur (setiap satu 0–10) supaya bebas antara satu sama lain, dan menyatakan tiada atribut yang dianalisis secara berasingan menentukan kualiti strategi — [Darwinex: What are investable attributes](https://help.darwinex.com/what-are-investable-attributes)
- Morningstar mewajarkan tempoh mengikut panjang rekod (bukti): 36–59 bulan = 100% penarafan 3 tahun; 60–119 bulan = 60% 5 tahun / 40% 3 tahun; ≥ 120 bulan = 50% 10 tahun / 30% 5 tahun / 20% 3 tahun — [Morningstar Disclosure Statement](https://profile.morningstar.com/ISR/MorningstarDisclosure.html)

### Inferences
- Kiraan berganda dalam reka bentuk semasa: profit factor = (kadar menang × purata menang) / ((1 − kadar menang) × purata rugi) dan jangkaan = kadar menang × purata menang − (1 − kadar menang) × purata rugi; jadi kadar menang, PF, purata pulangan dan jangkaan adalah fungsi pemboleh ubah yang sama. Jika ketiga-tiga/empat berada dalam tunjang berbeza (cth. kadar menang dalam "Konsisten"), wajaran berkesan Untung jauh melebihi 40. Semakan wajib: matriks korelasi Spearman antara 13 sub-skor merentas 123 kaedah; jika |ρ| > ~0.8, gabungkan (purata kumpulan) atau simpan satu wakil sahaja. Ini versi ringan "statistical coherence" JRC dan prinsip "atribut bebas" Darwinex.
- Dengan ~2 minggu data, sebarang wajaran berasaskan ramalan (regresi pulangan hadapan ke atas metrik, atau wajaran ikut kuasa ramalan luar sampel) akan terlebih padan (overfit): belum wujud tempoh luar sampel bebas. Tunggu sekurang-kurangnya beberapa tetingkap bebas (cth. ≥ 8–12 minggu, atau beberapa regim pasaran) sebelum mencuba.
- Wajaran entropi menghadiahkan metrik yang paling berserak, bukan yang paling meramal; ia juga menukar wajaran setiap minggu (tidak stabil) dan meningkatkan risiko pembalikan pangkat — tidak disyorkan.
- AHP (perbandingan berpasangan) hanya memformalkan wajaran pakar; untuk 4 tunjang ia menambah kerumitan tanpa bukti ketepatan tambahan. Wajaran pakar mudah (40/25/20/15) + analisis kepekaan (Bahagian 4) sudah memadai dan konsisten dengan dapatan "flat maximum".
- PCA/analisis faktor berguna sebagai alat diagnostik (berapa dimensi bebas sebenarnya wujud dalam 13 metrik) dan bukan untuk menetapkan wajaran; dengan 123 kaedah dan 13 metrik ia boleh dibuat sekali di luar papan.
- Pelajaran Morningstar: biar "Bukti" mengawal berapa banyak skor dipercayai (pengganda/pengecutan), bukan sekadar 15% tambahan secara aditif — lihat Bahagian 3 dan 6.

### Gaps
- Tiada sumber utama ditemui yang menguji secara empirik wajaran PCA/entropi/AHP lwn wajaran sama untuk memilih strategi dagangan atau dana dengan ukuran ramalan luar sampel.
- Kesimpulan penuh Fedrizzi & Predella hanya dibaca daripada petikan; perlu semakan teks penuh.

## 3. Agregasi: jumlah berwajaran aditif lwn geometri/multiplikatif, pintu/halangan minimum lwn pampasan, susunan leksikografi

### Takeaway
Jumlah berwajaran aditif adalah "pampasan sepenuhnya" — kelemahan teruk pada satu tunjang (cth. MAE dalam) boleh ditebus oleh untung tinggi. Amalan sebenar (Quantopian, ZuluTrade, StrategyQuant) menggabungkan pintu wajib dahulu, kemudian satu skor penyusun; HDI PBB beralih kepada min geometri pada 2010 khusus untuk menghukum ketidakseimbangan antara dimensi.

### Cited Findings
- HDI edisi 2010 menggantikan min aritmetik dengan min geometri untuk menggabungkan tiga indeks dimensi; pencapaian rendah dalam satu dimensi tidak lagi diimbangi secara linear oleh pencapaian tinggi dalam dimensi lain; perubahan ini menurunkan nilai indeks, paling ketara bagi negara dengan pembangunan tidak seimbang, tetapi kesannya pada pangkat sederhana — [UN HDR Technical Notes](https://data.un.org/_Docs/HDR%20Technical%20Notes.pdf)
- Min geometri menghapuskan kebolehgantian sempurna tetapi masih membenarkan sebahagian pampasan — [Aggregating the Human Development Index (VU)](https://vuir.vu.edu.au/48574/1/Aggregating_the_Human_Development_Index.pdf)
- Paruolo, Saisana & Saltelli mendapati HDI 2010 akan tetap seimbang walaupun di bawah agregasi linear, sambil mengakui rayuan konsep kebolehgantian tidak sempurna — [arXiv 1104.3009, "Ratings and rankings: Voodoo or Science?"](https://arxiv.org/pdf/1104.3009)
- Dalam konteks AHP, jika min geometri berwajaran digunakan, pembalikan pangkat tidak boleh berlaku; dengan min aritmetik berwajaran hasilnya berbeza — [Fedrizzi & Predella, ODS 2017](https://iris.unitn.it/retrieve/e3835194-37ee-72ef-e053-3705fe0ad821/Fedrizzi-Predella-ODS2017.pdf)
- Quantopian: algoritma yang memenuhi SEMUA kriteria struktur sahaja disusun setiap hari mengikut skor; kriteria termasuk pulangan positif, leveraj 0.8x–1.1x, tumpuan posisi rendah, beta rendah terhadap SPY, pusing ganti harian purata 5%–65% (tetingkap bergolek 63 hari), dedahan bersih sektor ±20% dan gaya ±40% — [Quantopian Contest tutorial](https://www.quantopian.com/tutorials/contest); [Quantopian: A New Contest is Coming](https://www.quantopian.com/posts/a-new-contest-is-coming-more-winners-and-a-new-scoring-system)
- ZuluTrade (pelabur EU): tapisan minimum masa dagangan ≥ 8 minggu, kejatuhan maksimum ≤ 30% daripada jumlah untung, ambang purata pip/pulangan minimum, dan hanya 1,000 "Leaders" teratas tersedia — [ZuluTrade: ZuluRanking](https://www.zulutrade.com/zuluranking); [ZuluTrade UK: How ZuluTrade Ranks Traders](https://www.zulutrade.co.uk/zuluranking)
- StrategyQuant membolehkan ujian Monte Carlo dimasukkan terus ke aliran kerja binaan dan menolak automatik strategi yang gagal ujian Monte Carlo (pintu keteguhan) — [StrategyQuant Features](https://strategyquant.com/features/); Monte Carlo menjalankan sejumlah ujian strategi dengan perubahan rawak tertentu — [StrategyQuant User's Guide](https://strategyquant.com/downloads/StrategyQuant_Help.pdf)
- Quantiacs (pertandingan niaga hadapan) menyusun sistem menggunakan minimum prestasi (Sharpe) antara dua selang — tempoh latihan dan tempoh langsung (sumber sekunder) — [Montague, CS229 2014](https://cs229.stanford.edu/proj2014/David%20Montague,%20Algorithmic%20Trading%20of%20Futures%20via%20Machine%20Learning.pdf)

### Inferences
- Reka bentuk disyorkan untuk papan (mudah dalam JS):
  1. Pintu (lulus/gagal, bukan skor): n dagangan matang ≥ N_min; hari beli berbeza ≥ 10 (selaras dengan tanda "BELUM CUKUP < 10 hari beli berbeza" Papan Penganalisis); PF ≥ 1.0 (atau purata pulangan > kos); purata MAE tidak lebih teruk daripada had (cth. −8%); tiada metrik teras hilang. Kaedah gagal pintu dipaparkan "Pantau/Belum layak" tanpa mengira skor.
  2. Dalam pintu: skor komposit untuk menyusun.
  3. Pemutus seri leksikografi: Bukti (n berkesan) kemudian Risiko.
- Pilihan agregasi tunjang: min geometri berwajaran ∏ Pₖ^{wₖ} bagi 4 skor tunjang (Untung, Konsisten, Risiko, Bukti) dengan lantai kecil (cth. P ≥ 5) supaya satu sifar tidak memadamkan semuanya. Ini mengekalkan 0–100, mudah dikira (exp(Σ w·ln P)), dan menghukum kaedah "untung tinggi tetapi risiko buruk" — selaras dengan matlamat "mampan". Agregasi aritmetik boleh dikekalkan di dalam setiap tunjang (metrik dalam tunjang yang sama memang boleh saling mengganti).
- Jangan biarkan "Bukti" menjadi tunjang aditif: secara aditif, kaedah bertuah dengan n kecil masih boleh mencapai ≥ 70 melalui Untung 40% sahaja. Lebih munasabah: pintu n minimum + pengecutan metrik ke arah purata keseluruhan dengan faktor n/(n+k) (empirical Bayes), atau gunakan had bawah selang keyakinan (cth. had bawah Wilson untuk kadar menang) — lihat Bahagian 6.
- Pelajaran Quantiacs ("minimum dua tempoh"): Papan Penganalisis sudah ada skor backtest dipotong dan posisi hadapan; skor pilihan akhir boleh diambil sebagai min(skor_backtest_dipotong, skor_hadapan) atau min geometri kedua-duanya, supaya kaedah mesti baik pada KEDUA-DUA bukti.
- Peraturan "metrik hilang digugurkan dan wajaran dinormal semula" secara tersirat mengimput metrik hilang dengan purata metrik lain kaedah itu — boleh menguntungkan kaedah yang tiada data risiko. Lebih selamat: metrik teras hilang = gagal pintu; metrik sekunder hilang = imput konservatif (cth. persentil ke-25 merentas kaedah), dan paparkan "liputan %".

### Gaps
- Tiada sumber ditemui yang membandingkan secara empirik agregasi aditif lwn geometri dari segi ramalan prestasi strategi dagangan.
- Formula dalaman ZuluRank (wajaran faktor) tidak didedahkan; senarai faktor pihak ketiga berbeza-beza.

## 4. Analisis kepekaan pangkat terhadap wajaran (gangguan wajaran Monte Carlo, kestabilan pangkat, Kendall tau) dan panduan OECD/JRC

### Takeaway
Amalan JRC ialah analisis ketidakpastian Monte Carlo: sampel pilihan pemodelan (wajaran, normalisasi, agregasi, imputasi), kira semula pangkat beribu kali, dan laporkan pangkat median dengan selang persentil ke-5–95 bagi setiap unit. Lencana "stabil" semasa (3 set wajaran tetap) ialah versi sangat kecil kaedah ini dan set wajarannya terlalu serupa untuk menjadi ujian yang bermakna.

### Cited Findings
- Saisana, Saltelli & Tarantola (2005, JRSS A) mencadangkan analisis ketidakpastian dan kepekaan sebagai alat menilai kualiti penunjuk komposit, diuji pada Technology Achievement Index PBB; keraguan tentang keteguhan pangkat dan mesej dasar boleh ditangani dengan kaedah ini — [Saisana, Saltelli & Tarantola 2005](https://www.andreasaltelli.eu/file/repository/JRSS_2005.pdf)
- Persembahan hasil: pangkat asal di sebelah pangkat median serta persentil ke-5 dan ke-95 taburan indeks berasaskan Monte Carlo (72 negara) — [JRC, Tools for Composite Indicators Building (EUR 21682)](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC31473/EUR%2021682%20EN.pdf)
- Bagi model tidak linear di mana kaedah normalisasi, skema wajaran dan wajaran semuanya disampel, analisis kepekaan berasaskan varians ialah pendekatan paling sesuai — [Saisana et al. 2005](https://www.andreasaltelli.eu/file/repository/JRSS_2005.pdf); [ResearchGate: Uncertainty and sensitivity analysis techniques...](https://www.researchgate.net/publication/4993166_Uncertainty_and_Sensitivity_Techniques_as_Tools_for_the_Analysis_and_Validation_of_Composite_Indicators)
- Audit statistik JRC-COIN bagi Global Innovation Index menambah selang keyakinan pada pangkat negara untuk menunjukkan kestabilan pangkat di bawah kaedah pengiraan berbeza; audit 2026 ialah tahun ke-16 berturut-turut dan mengikut Buku Panduan OECD/JRC 2008 — [WIPO GII 2026, Appendix II: JRC statistical audit](https://www.wipo.int/web-publications/global-innovation-index-2026/en/appendix-ii-joint-research-centre-jrc-statistical-audit-of-the-2026-global-innovation-index.html)
- Buku Panduan meletakkan keteguhan dan kepekaan sebagai langkah wajib (mekanisme masuk/keluar penunjuk, normalisasi, imputasi, wajaran) — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Pembalikan pangkat berlaku dalam hampir setiap kaedah MCDM; pendekatan "multi-weight ranking" dicadangkan untuk menyusun di bawah pelbagai vektor wajaran — [arXiv 2312.03006](https://arxiv.org/pdf/2312.03006)

### Inferences
- Kelemahan ujian "stabil" semasa: ketiga-tiga set (40/25/20/15, 30/25/25/20, 25/25/35/15) mengekalkan Konsisten = 25 dan Bukti 15–20; hanya paksi Untung↔Risiko yang benar-benar diuji, dan dengan 3 titik sahaja. Ia juga tidak menguji pilihan normalisasi, julat, atau agregasi.
- Ganti dengan Monte Carlo ringan (≈ 123 kaedah × 1,000 lelaran — remeh untuk JS pelayar):
  1. Setiap lelaran: wⱼ' = wⱼ × U(0.5, 1.5) bagi setiap tunjang, normal semula ke 100 (atau sampel Dirichlet sekitar wajaran asas).
  2. Secara pilihan, togol juga: julat normalisasi ±20% lebar, agregasi aritmetik/geometri, dan keluarkan satu metrik secara rawak (ujian "masuk/keluar penunjuk" JRC).
  3. Simpan pangkat setiap kaedah. Laporkan: pangkat median, julat persentil ke-5–95, dan P(4 teratas).
  4. Lencana "stabil" = P(4 teratas) ≥ 50% (atau persentil ke-95 pangkat ≤ 10); "rapuh" = julat 5–95 > 30 pangkat.
- Kendall tau (τ = (pasangan sependapat − pasangan bercanggah) / (n(n−1)/2)) atau Spearman ρ antara pangkat asas dan setiap pangkat terganggu memberi satu nombor keteguhan keseluruhan; untuk keputusan "pilih 3–4", lebih relevan ialah tau/pertindihan pada 10–20 teratas sahaja (pertindihan set teratas, cth. Jaccard bagi 4 teratas).
- Kestabilan masa (lebih penting daripada kestabilan wajaran untuk "mampan"): kira Spearman antara pangkat minggu ini dan minggu lalu, dan antara pangkat backtest dan pangkat hadapan. Jika korelasi pangkat antara tempoh hampir sifar, skor itu mengukur hingar, tanpa mengira wajaran.
- Analisis kepekaan berasaskan varians (indeks Sobol) terlalu berat untuk papan; versi "satu faktor pada satu masa" + Monte Carlo di atas sudah mencukupi.

### Gaps
- Definisi tepat "average shift in ranks" dan kegunaan Kendall tau dalam audit JRC tidak disahkan daripada teks penuh (sekatan rangkaian); COINr (pakej R JRC) tidak muncul dalam hasil carian.

## 5. Contoh dunia sebenar: Morningstar, Darwinex, Quantopian/QuantConnect, ZuluTrade/Collective2/myfxbook/FXBlue, StrategyQuant, kad skor pemilihan pengurus

### Takeaway
Sistem yang berpengaruh cenderung kepada (a) SATU ukuran pulangan terlaras risiko yang berasaskan teori (Morningstar MRAR, Quantopian VADR, QuantConnect PSR) dan bukannya banyak metrik bertindih, (b) pintu kelayakan dan rekod minimum yang panjang, (c) penyusunan relatif dalam kumpulan setara, dan (d) normalisasi risiko sebelum membanding pulangan (Darwinex). Platform salin-dagang (ZuluTrade, Collective2) kebanyakannya proprietari dan legap.

### Cited Findings
**Morningstar Rating for Funds**
- Penarafan berasaskan Morningstar Risk-Adjusted Return (MRAR), yang menghukum turun naik ke bawah lebih berat dan menghadiahkan konsistensi — [Morningstar Rating for Funds Fact Sheet](https://advisor.morningstar.com/enterprise/MorningstarRatingForFunds_FactSheet.pdf); [Morningstar Disclosure](https://profile.morningstar.com/ISR/MorningstarDisclosure.html)
- MRAR didorong oleh teori utiliti jangkaan (pelabur menyusun portfolio mengikut nilai jangkaan fungsi utiliti kekayaan akhir); parameter penghindaran risiko γ = 2 — [Morningstar Rating for Funds Methodology, Ogos 2021](https://www.morningstar.com/content/dam/marketing/shared/research/methodology/771945_Morningstar_Rating_for_Funds_Methodology.pdf)
- Definisi semasa sebagai setara-kepastian utiliti kuasa: ambil pulangan lebihan geometri bulanan atas kadar bebas risiko, ER_t = (1+TR_t)/(1+RF_t) − 1, kemudian MRAR(γ) = [ (1/T) Σ (1+ER_t)^(−γ) ]^(−12/γ) − 1; Morningstar menetapkan γ = 2 kerana menghasilkan pangkat yang konsisten dengan toleransi risiko pelabur runcit biasa — [AEA 2021, "Do Mutual Funds Manipulate Star Ratings?"](https://www.aeaweb.org/conference/2021/preliminary/paper/F4zh4AeG); [Morningstar Methodology 2021](https://www.morningstar.com/content/dam/marketing/shared/research/methodology/771945_Morningstar_Rating_for_Funds_Methodology.pdf) (bentuk formula diambil daripada ringkasan sekunder — semak teks asal)
- Pandangan ringkas: MRAR = Morningstar Return − Morningstar Risk; Morningstar Risk mewajarkan variasi ke bawah lebih berat daripada sisihan piawai — [Morningstar Direct Custom Calculation Data Points](https://morningstardirect.morningstar.com/clientcomm/customcalculations.pdf)
- Untuk γ dan penanda aras tertentu, MRAR menyusun dua dana sama seperti utiliti kuasa jangkaan — [Univ. of Toronto/Fields, "The Ratings Game"](https://www.fields.utoronto.ca/programs/cim/financial_math/ifid/personal_risk/02-03/RatingsGame.pdf)
- Bintang diberi dalam kategori setara: 10% / 22.5% / 35% / 22.5% / 10%; penarafan keseluruhan ialah gabungan 3/5/10 tahun dengan wajaran ikut panjang rekod (minimum 36 bulan) — [Morningstar Disclosure](https://profile.morningstar.com/ISR/MorningstarDisclosure.html); [Morningstar investing terms](https://www.morningstar.com/investing-terms/morningstar-rating-for-funds)
- Percanggahan: Fact Sheet menyatakan metodologi baharu mengambil kira caj jualan/yuran tebus, manakala Disclosure Statement menyatakan tiada pelarasan caj jualan — [Fact Sheet](https://advisor.morningstar.com/enterprise/MorningstarRatingForFunds_FactSheet.pdf) lwn [Disclosure](https://profile.morningstar.com/ISR/MorningstarDisclosure.html)

**Darwinex (DARWIN, Atribut Boleh Labur, D-Score)**
- 12 Atribut Boleh Labur, setiap satu 0–10; semua strategi didagang pada sasaran risiko yang sama (VaR bulanan maksimum 6.5%); atribut direka bebas — [Darwinex: Investable attributes](https://help.darwinex.com/what-are-investable-attributes)
- Kod atribut dalam data mentah: EX (Experience), MC (Market Correlation), RS (Risk Stability), RA (Risk Adjustment/Aversion), OS (Open Strategy), CS (Close Strategy), PF (Performance), LA (Loss Aversion), R+, R−, DC (Duration Consistency), CP (Capacity) — [Darwinex: Raw DARWIN Data User Guide](https://help.darwinex.com/raw-darwin-data-user-guide)
- Experience (Ex): mengukur sejauh mana rekod mewakili secara statistik, dengan mengira bilangan keputusan representatif; satu-satunya atribut yang tidak boleh turun; skor 10 = 12 D-Period pengalaman terkumpul — [Darwinex: Experience](https://help.darwinex.com/experience-attribute)
- Risk Stability (Rs): 0–10 menggunakan 12 D-Period terakhir dengan tempoh terkini diberi wajaran lebih; bergantung pada kestabilan VaR, bukan parasnya — [Darwinex: Risk Stability](https://help.darwinex.com/risk-stability-attribute)
- Risk Adjustment (Ra): 0–10 atas 12 D-Period terakhir; menilai pengurusan risiko per posisi (Rs pula risiko akaun keseluruhan) — [Darwinex: Risk Adjustment](https://help.darwinex.com/risk-adjustment-attribute)
- Kebanyakan atribut guna 12 D-Period terakhir; Loss Aversion serta konsistensi pulangan/tempoh guna 3 D-Period terakhir — [Darwinex: D-Period](https://help.darwinex.com/d-period)
- D-Score ialah metrik proprietari yang mengukur kualiti lengkung pulangan DARWIN sepanjang 5 tahun terakhir; menurut satu sumber, sejak 2020 pengiraannya dipermudah dan hanya menggunakan data sebut harga DARWIN (versi lama berasaskan gred dan wajaran atribut) — [Darwinex: D-Score](https://help.darwinex.com/d-score)

**Quantopian / QuantConnect / Quantiacs**
- Skor peraduan Quantopian: setiap hari, pulangan harian dibahagi turun naik 63 hari dagangan terkini = pulangan harian terlaras turun naik (VADR); skor = jumlah VADR; selepas > 63 hari, skor = jumlah 63 VADR terkini (tetingkap bergolek); hanya algoritma yang lulus semua kriteria struktur disusun — [Quantopian Contest tutorial](https://www.quantopian.com/tutorials/contest); [Quantopian: A New Contest is Coming](https://www.quantopian.com/posts/a-new-contest-is-coming-more-winners-and-a-new-scoring-system)
- Kod komuniti meletakkan lantai turun naik 2%; peraturan tidak jelas sama ada turun naik pulangan atau ekuiti — [Quantopian archive](https://quantopian-archive.netlify.app/forum/threads/context-score-computation.html)
- QuantConnect Alpha Streams (forum, bukan dokumentasi rasmi): PSR digunakan sebagai keyakinan bahawa Sharpe sebenar dalam dagangan langsung > 1.0 — [QuantConnect forum 7062](https://www.quantconnect.com/forum/discussion/7062)
- Quantiacs menyusun mengikut minimum prestasi antara tempoh latihan dan tempoh langsung (sekunder) — [Montague, CS229 2014](https://cs229.stanford.edu/proj2014/David%20Montague,%20Algorithmic%20Trading%20of%20Futures%20via%20Machine%20Learning.pdf)

**Platform salin-dagang**
- ZuluRank: sistem proprietari, dijana komputer sepenuhnya, menimbang kematangan (berapa lama sistem berjalan), dedahan (berapa banyak posisi boleh dibuka serentak) dan kejatuhan; bertujuan menapis strategi yang praktikal diikuti, bukan sekadar pulangan tertinggi — [ZuluTrade: ZuluRanking](https://www.zulutrade.com/zuluranking)
- Senarai faktor pihak ketiga berbeza: Sharpe, aktiviti dagangan, kejatuhan lwn untung, tempoh dagangan, kekerapan log masuk — [Forex-Central](https://www.forex-central.net/ZuluTrade-choosing-best-signal-providers.php); umur akaun, sejarah kejatuhan, purata tempoh dagangan, nisbah menang/kalah, konsistensi — [BrokerSpecs](https://brokerspecs.com/education/zulutrade)
- Collective2: C2 Score digambarkan (dipetik dalam forum) sebagai kaedah proprietari menyusun strategi berdasarkan "pelbagai faktor risiko dan pulangan", tanpa formula; anekdot: strategi dengan pulangan kumulatif 242.2% berada di kedudukan #236 — [Elite Trader thread](https://elitetrader.com/et/threads/unhappy-with-collective2.378715/)

**StrategyQuant**
- Walk-Forward Matrix untuk menyemak sama ada wujud kelompok parameter "optimum" yang stabil; Monte Carlo dengan penolakan automatik strategi yang gagal — [StrategyQuant Features](https://strategyquant.com/features/)
- Ulasan 2026: strategi yang kelihatan sempurna dalam SQX kerap merosot atau gagal apabila didagang secara langsung; perlukan disiplin dan literasi statistik — [StrategyQuant X Review 2026](https://newyorkcityservers.com/blog/strategyquant-review) (sumber ulasan pihak ketiga)

### Inferences
- Pelajaran 1 (Morningstar/Quantopian/QuantConnect): satu metrik teras terlaras risiko yang berasaskan teori lebih sukar "dimainkan" dan kurang bertindih daripada 13 metrik. Adaptasi untuk dagangan swing: setara-kepastian per dagangan CE_γ = [mean((1+rᵢ)^(−γ))]^(−1/γ) − 1 dengan γ = 2 (rᵢ = pulangan bersih dagangan). Ia secara automatik menghukum kerugian besar dan ketidakkonsistenan; boleh menggantikan sebahagian besar tunjang Untung + Konsisten. Catatan: (1+r)^(−2) meletup jika r → −100%; untuk saham dengan henti rugi ini tidak menjadi isu.
- Pelajaran 2 (Morningstar): rekod minimum yang panjang (36 bulan) dan wajaran lebih kepada tempoh lebih panjang. Dua minggu forward jauh di bawah sebarang standard industri; ZuluTrade sendiri menetapkan ≥ 8 minggu untuk EU. Skor forward 2 minggu patut dilabel "awal".
- Pelajaran 3 (Morningstar): kumpulan setara. Kaedah swing boleh dikumpulkan ikut keluarga (momentum/breakout/pullback) atau tempoh pegang; peringkat dalam kumpulan mengelakkan satu regim pasaran (cth. 2 minggu momentum kuat) memenangkan seluruh satu keluarga.
- Pelajaran 4 (Darwinex): normalkan risiko dahulu (semua strategi pada sasaran VaR sama) sebelum membanding pulangan; "Experience" dikira ikut keputusan representatif, bukan kiraan dagangan mentah — selaras dengan "n berkesan ikut hari beli" yang sudah digunakan Papan Penganalisis; recency weighting dalam tetingkap tetap.
- Pelajaran 5 (Quantopian): tetingkap bergolek (63 hari) supaya skor mencerminkan prestasi semasa; lantai pada penyebut (turun naik 2%) — analog: had PF (2.5 sudah dibuat) dan had atas pada nisbah lain apabila kerugian sangat sedikit.
- Pelajaran 6 (Collective2/StrategyQuant): skor legap dan pengoptimuman pada backtest tidak menjamin prestasi langsung — papan semasa yang telus (formula diterbitkan) ialah kelebihan; kekalkan.

### Gaps
- myfxbook dan FXBlue: tiada sumber tentang kriteria/formula penyusunan leaderboard ditemui.
- Darwinex: formula D-Score semasa dan halaman "the formula of the DarwinIA rating" (https://help.darwinex.com/the-formula-of-the-darwinia-rating) tidak dapat dibaca; wajaran atribut tidak disahkan.
- Collective2: tiada dokumentasi rasmi C2 Score ditemui.
- Kad skor pemilihan pengurus dana lindung nilai (hedge fund manager selection scorecards): tiada sumber primer ditemui dalam sesi ini.
- QuantConnect Alpha Streams: hanya sumber forum; dokumentasi rasmi tidak ditemui.

## 6. Bukti: pendekatan komposit mana yang paling baik meramal prestasi masa hadapan?

### Takeaway
Bukti bercampur dan sederhana: penarafan seperti bintang Morningstar paling boleh dipercayai untuk mengenal pasti yang LEMAH (rating rendah cenderung kekal rendah), kurang untuk memisahkan yang terbaik. Bagi memilih 3–4 terbaik daripada 123, berat sebelah pemilihan (multiple testing) dan saiz sampel kecil adalah risiko utama; kaedah statistik seperti PSR, MinTRL dan Deflated Sharpe Ratio dibina khusus untuk ini.

### Cited Findings
- Blake & Morey (2000): penarafan rendah cenderung berterusan dalam tempoh 3 dan 5 tahun berikutnya, tetapi dana 5 bintang tidak menunjukkan prestasi lebih baik secara signifikan berbanding 3 atau 4 bintang (dipetik oleh kajian dana bon Eropah) — [International Review of Economics & Finance 2022](https://www.sciencedirect.com/science/article/abs/pii/S1059056022001873)
- Dana bon Eropah: bukti kuat kegigihan prestasi dan kegigihan penarafan — [IREF 2022](https://www.sciencedirect.com/science/article/abs/pii/S1059056022001873)
- Morey & Gottesman: dengan metodologi baharu Morningstar, penarafan boleh meramal prestasi dana AS (sampel Julai 2002–Jun 2005) — dipetik dalam [Journal of Property Research 28(3), 2011](https://www.tandfonline.com/doi/full/10.1080/09599916.2011.577902)
- Dana hartanah: bukti lemah bahawa Morningstar meramal prestasi relatif dalam pulangan mentah; selepas pelarasan Fama–French tiga faktor + momentum, tiada bukti penarafan memberi panduan boleh dipercayai — [Journal of Property Research 2011](https://www.tandfonline.com/doi/full/10.1080/09599916.2011.577902)
- Satu kajian menyimpulkan prestasi ramalan sistem penarafan Morningstar tidak mengatasi random walk — [ResearchGate: The Predictive Performance of Morningstar's Mutual Fund Ratings](https://www.researchgate.net/publication/251393863_The_Predictive_Performance_of_Morningstar's_Mutual_Fund_Ratings)
- Kajian Morningstar sendiri: penarafan bintang ramalan secara sederhana; dana berpenarafan tinggi lebih berkemungkinan bertahan dan mengatasi, dana berpenarafan rendah lebih berkemungkinan ketinggalan atau ditutup (kajian dalaman — ada konflik kepentingan) — [Morningstar: Does the Star Rating Predict Future Performance?](https://www.morningstar.com/funds/does-star-rating-funds-predict-future-performance)
- Probabilistic Sharpe Ratio (Bailey & López de Prado, 2012, Journal of Risk): kebarangkalian Sharpe yang dianggar melebihi ambang dengan pulangan tidak normal; juga memberi panjang rekod minimum (MinTRL) untuk menolak hipotesis Sharpe di bawah ambang pada tahap keyakinan tertentu; kecondongan negatif dan kurtosis berlebihan memanjangkan rekod yang diperlukan — [Journal of Risk: The Sharpe Ratio Efficient Frontier](https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier); [PortfolioOptimizer: PSR & MinTRL](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/)
- Deflated Sharpe Ratio (Bailey & López de Prado, 2014, Journal of Portfolio Management) membetulkan dua sumber inflasi prestasi: berat sebelah pemilihan di bawah ujian berganda dan pulangan tidak normal; ambang signifikan dinaikkan mengikut bilangan percubaan — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551); [Wikipedia: Deflated Sharpe ratio](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- Wajaran sama/kasar meramal luar sampel setanding atau lebih baik daripada wajaran dipadankan apabila sampel kecil — [Dawes 1979](https://www.researchgate.net/publication/232597503_The_robust_beauty_of_improper_linear_models_in_decision_making); [Lichtenberg & Şimşek, PMLR 58](http://proceedings.mlr.press/v58/lichtenberg17a/lichtenberg17a.pdf)

### Inferences
- Saiz sampel semasa: ~4,400 dagangan / 123 kaedah ≈ 36 dagangan sekaedah secara purata, semuanya dalam ~10 hari dagangan dan satu regim pasaran (dagangan berkelompok → n berkesan jauh lebih kecil). Contoh kira: pada n = 36 dan kadar menang sebenar 50%, ralat piawai ≈ √(0.25/36) ≈ 8.3 mata peratus → selang 95% ≈ ±16 mata; dengan peta 30%→0, 70%→100 (2.5 mata skor per mata peratus), ini ≈ ±41 mata pada sub-skor kadar menang. Andaian ilustrasi: jika sisihan piawai pulangan per dagangan ≈ 7%, ralat piawai purata ≈ 1.2% → selang 95% ≈ ±2.3% → ≈ ±26 mata pada sub-skor purata pulangan (julat −3..+6%). Maknanya kebanyakan perbezaan skor antara kaedah sekarang berada dalam hingar.
- Berat sebelah pemilihan: memilih 4 teratas daripada 123 menjamin skor teratas terlebih anggar (regresi ke min dijangka). Pembetulan praktikal yang mudah dalam pelayar: (a) pengecutan setiap metrik: m_kecut = (n·m + k·m_semua)/(n + k) dengan k ≈ 20–30 dagangan (atau ikut hari beli); (b) gunakan had bawah selang keyakinan (Wilson untuk kadar menang; purata − 1.0×SE untuk pulangan) dan bukannya anggaran titik; (c) laporkan PSR/DSR untuk metrik teras.
- Kerana penarafan paling dipercayai untuk menolak yang lemah, gunakan skor sekarang terutamanya untuk MENGELUARKAN kaedah lemah dan menyempitkan senarai calon (cth. 15–20), bukan untuk menobatkan 3–4 "Teras" muktamad. Pilihan akhir patut menunggu tempoh pengesahan luar sampel: pilih calon pada minggu 1–2, sahkan pada minggu 3–8 tanpa mengubah formula/wajaran (bekukan versi formula dan tarikhnya).
- Ujian ramalan skor itu sendiri (mudah dan paling penting): setiap minggu, kira korelasi Spearman antara skor komposit pada akhir minggu t dan pulangan hadapan minggu t+1…t+k bagi kaedah yang sama. Jika ρ tidak positif secara konsisten, sebarang penalaan wajaran tidak bermakna. Jika ρ positif, baru wajaran boleh dinilai semula (cth. bandingkan ρ bagi setiap tunjang secara berasingan).

### Gaps
- Tiada kajian ditemui yang membandingkan secara langsung komposit aditif lwn geometri lwn metrik tunggal (MRAR/Sharpe) dari segi ramalan prestasi strategi dagangan runcit.
- Kertas asal Blake & Morey (2000) tidak dibaca; dapatan dipetik secara sekunder.
- Kajian dana pasaran membangun 2025 ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0890838925001386)) muncul dalam carian tetapi dapatannya tidak dapat diekstrak.

## 7. Objektif: implikasi keseluruhan untuk menilai dan menambah baik "Skor kaedah swing"

### Takeaway
Struktur semasa (julat tetap, 4 tunjang, peringkat mutlak, ujian berbilang set wajaran) selari dengan amalan asas OECD/JRC dan wajar dikekalkan sebagai rangka; kelemahan utama ialah (1) kiraan berganda metrik untung, (2) agregasi aditif sepenuhnya tanpa pintu, (3) "Bukti" sebagai tunjang aditif dan bukan pengecut/pintu, (4) ujian kestabilan yang terlalu sempit, dan (5) tiada ujian sama ada skor itu meramal prestasi hadapan.

### Cited Findings
- Buku Panduan OECD/JRC menekankan analisis keteguhan terhadap pilihan penunjuk, normalisasi, imputasi dan wajaran — [OECD/JRC Handbook 2008](https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf)
- Sistem praktikal menggunakan pintu kelayakan sebelum penyusunan (Quantopian, ZuluTrade, StrategyQuant) — [Quantopian Contest](https://www.quantopian.com/tutorials/contest); [ZuluTrade](https://www.zulutrade.com/zuluranking); [StrategyQuant](https://strategyquant.com/features/)
- Min geometri digunakan HDI untuk mengelak pampasan linear antara dimensi — [UN HDR Technical Notes](https://data.un.org/_Docs/HDR%20Technical%20Notes.pdf)
- Ujian berganda dan saiz sampel kecil membesarkan prestasi yang kelihatan — [SSRN 2460551 (DSR)](https://papers.ssrn.com/abstract=2460551); [Journal of Risk (PSR/MinTRL)](https://www.risk.net/journal-risk/2223785/sharpe-ratio-efficient-frontier)

### Inferences
- Senarai tindakan bertingkat (semua boleh dibuat dalam JS pelayar tanpa pustaka luar):
  1. Diagnostik (tanpa mengubah skor): matriks korelasi Spearman 13 sub-skor; sd setiap sub-skor dan "wajaran berkesan"; peratus kaedah tepu pada 0/100 bagi setiap metrik.
  2. Buang kiraan berganda: satu wakil per kumpulan |ρ| > 0.8 (cth. simpan purata pulangan atau jangkaan, buang salah satu PF/kadar menang daripada tunjang lain atau gabungkan).
  3. Pintu: n/hari beli minimum, PF ≥ 1, had MAE, metrik teras wujud.
  4. Pengecutan Bukti: metrik dikecutkan ke arah purata keseluruhan ikut n berkesan (atau had bawah selang keyakinan); keluarkan Bukti sebagai tunjang aditif, atau kekalkan dengan wajaran kecil sahaja.
  5. Agregasi tunjang secara geometri berwajaran (dengan lantai), aritmetik dalam tunjang.
  6. Monte Carlo kepekaan (1,000 gangguan wajaran ± togol normalisasi/agregasi) → pangkat median, julat 5–95, P(4 teratas); ganti lencana "stabil".
  7. Ujian ramalan skor mingguan (Spearman skor-t lwn pulangan hadapan) dan bekukan versi formula sebelum tempoh pengesahan.
  8. Pertimbangkan satu metrik teras gaya MRAR (setara-kepastian γ = 2 per dagangan) sebagai paksi Untung+Konsisten, dan min(backtest dipotong, hadapan) gaya Quantiacs untuk pilihan akhir.
- Matlamat "untung maksimum tetapi mampan" lebih sesuai dengan skor yang menghukum kelemahan (geometri/pintu) dan kestabilan merentas masa, berbanding menambah wajaran Untung; kekalkan Untung sebagai tunjang terbesar tetapi pastikan wajaran berkesannya (selepas korelasi) tidak melebihi niat.

### Gaps
- Tiada data empirik daripada repo ini dibaca dalam tugasan penyelidikan ini (korelasi sebenar antara 13 metrik, taburan sub-skor, kadar tepu) — perlu dikira daripada `BacktestShariah2/lejar/` / data papan sebelum memuktamadkan perubahan.
