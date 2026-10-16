# Katalog Calon Kaedah K145+ (kajian dalam talian)

Dikemas kini: 15 Okt 2026 (K397 ditambah). Sambungan kepada K1–K144 (lihat `BacktestShariah2/spec/SPEC_SEMUA_KAEDAH.md`) dan I01–I32.

**Ringkasan:** 253 calon baharu (K145–K397) + 9 peraturan keluar (X01–X09).

| Pusingan | Nombor | Bil. | A sedia | B pembalikan | C separa |
|---|---|---|---|---|---|
| Kajian petang | K145–K195 | 51 | 25 | 7 | 19 |
| Pusingan 1 (18:05–18:32) | K196–K283 | 88 | 51 | 6 | 31 |
| Pusingan 2 (18:36–19:10) | K284–K366 | 83 | 48 | 12 | 23 |
| Pusingan 3 (19:15–19:26) | K367–K396 | 30 | 17 | 7 | 6 |
| Tambahan pengguna (15 Okt) | K397 | 1 | 1 | 0 | 0 |
| **Jumlah** | | **253** | **142** | **32** | **79** |

Jumlah keseluruhan katalog projek kini K1–K397.

**Saringan muktamad (15 Okt 2026):** 47 sesuai → M115–M161; 105 varian kaedah sedia ada; 86 buang; 15 pendua. Lihat `CADANGAN_SARINGAN_K145.md`.
Skop: kaedah momentum swing (beli sahaja) yang boleh dikira daripada data OHLCV harian/mingguan.
Status: CALON SAHAJA — belum ada spec STEP-1, belum diuji. Pilihan untuk STEP-1 dibuat oleh Azim.

Petunjuk lajur:
- **Kump.** A = sedia untuk backtest OHLCV; B = pembalikan/kontra-aliran (kurang selaras momentum); C = separa (perlu takrif atau data tambahan).
- **≈** = hampir sama dengan kaedah sedia ada.
- *(andaian)* = inferens, bukan kata sumber.
- Henti "1 mata"/"10 sen" ialah angka asal sumber dalam dolar; tukar ke ATR atau % semasa STEP-1.

Liputan: Reddit dan cerminnya disekat semasa kajian; kandungan YouTube dibaca melalui transkrip/ringkasan.

## Kumpulan A — sedia untuk backtest OHLCV

| K | Kaedah | Pencipta | Masuk | Keluar | ≈ | Sumber |
|---|---|---|---|---|---|---|
| K145 | Bow Tie | Dave Landry | SMA10>EMA20>EMA30 berkipas dalam 3–5 bar; ≥2 bar naik, kemudian 1 bar undur; beli tembus high bar undur | Henti bawah bar persediaan; sasaran 1 = julat bar persediaan, kemudian henti ke titik pulang modal untuk separuh baki | | capital.com/it-it/learn/technical-analysis/il-bow-tie-di-dave-landry ; scan.stockcharts.com/discussion/comment/6140 |
| K146 | 2/20 EMA Breakout | Dave Landry (S&C Dis 1996) | Low semalam dan hari ini kedua-duanya > EMA20; beli henti atas high 2 hari | Henti pada EMA20, mengekor setiap hari | | traders.com/Documentation/FEEDbk_docs/1996/12/Abstracts1296/2_20DaySdbar.html |
| K147 | Landry Pullback (high 2 bulan) | Dave Landry | High baharu 2 bulan, kemudian 2–7 hari high menurun; beli 10 sen atas bar pertama yang buat high lebih tinggi | Henti bawah low bar itu (risiko maks 4%); keluar untung tidak dinyatakan — perlu pilih | | scan.stockcharts.com/discussion/comment/5575 |
| K148 | Stockbee Anticipation | Pradeep Bonde | Saham dalam senarai TI65/MDT/Double Trouble; perubahan hari ini −1% hingga +1%; 3–10 hari undur sempit, volum rendah; tiada hari turun ≥4%, tiada 3 hari naik berturut | *(andaian)* jual dalam 3–5 hari, henti jika rugi >8% | K63/K78 (berbeza: masuk sebelum pecah) | tikamalma.substack.com/p/systems-setups-and-process-of-swing |
| K149 | Boomer / Extended Level Boomer | Jeff Cooper | ADX>30, +DI>−DI, 2 hari dalam (inside day) berturut; beli atas high hari kedua. Varian: hari 1 high 60 hari + 2 hari dalam | Henti bawah low hari kedua; varian guna henti mengekor | M70 | swingtradebot.com/stock-screens/definitions ; prorealcode.com/prorealtime-market-screeners/boomer-pattern/ |
| K150 | Expansion Pivot | Jeff Cooper | Julat hari ini > setiap 9 hari sebelumnya; harga ≤SMA50 semalam/hari ini dan pecah naik; beli atas high hari itu keesokannya | Henti bawah low hari itu; keluar untung tidak dinyatakan — perlu pilih | | elibook.vn/2020/02/03/expansion-pivot-mot-phuong-phap-danh-cua-jeff-cooper-gan-voi-pk-technique-cua-trend-trader/ ; swingtradebot.com |
| K151 | 180 Bullish | Jeff Cooper (menurut swingtradebot; satu sumber tidak namakan pencipta) | Semalam tutup di 25% bawah julat; hari ini tutup di 25% atas julat dan > MA10 dan MA50; beli 10 sen atas high | Henti 1 mata; keluar untung tidak dinyatakan | | swingtradebot.com/stock-screens/definitions |
| K152 | Reversal New Highs | Tidak dinamakan | Harga >$30; hari luar (tembus bawah low semalam lalu atas high semalam), julat terbesar 5 hari, high baharu 60 hari; beli 5 sen atas high | Henti 1 mata, kemudian mengekor | | swingtradebot.com/stock-screens/Bullish |
| K153 | High 2 (H2) bull flag | Al Brooks | Harga atas EMA20 yang naik; undur dua kaki (high lebih rendah); bar isyarat tutup dekat high; beli 1 tik atasnya | Henti pada low bar isyarat atau low undur; sasaran 2R atau swing high sebelumnya | | luxalgo.com/library/concept/bar-counting-h1-h2.md ; ar.tradingview.com/script/TIyW8vKv/ |
| K154 | Traders' Action Zone | marketcalls / NexusFi | SMA10>EMA30; harga undur ke zon antara keduanya dan buat low lebih tinggi; beli henti atas bar itu | Henti pada low bar; ambil ½ untung pada 1.5R, alih henti ke +0.5R, ekor baki | | marketcalls.in/nifty-technicals/nifty-and-swing-traders.html ; nexusfi.com/trading-journals/21698-swing-trading-strategies-eod-papertrading.html |
| K155 | Moving Momentum | StockCharts ChartSchool | SMA20>SMA150; Stokastik jatuh <20; kemudian histogram MACD jadi positif | *(andaian daripada peraturan jual)* SMA20<SMA150 atau histogram negatif | | chartschool.stockcharts.com (Trading Strategies → Moving Momentum) |
| K156 | CCI Correction | StockCharts ChartSchool (Lambert) | CCI mingguan >+100 tetapkan bias naik (kekal sehingga <−100); CCI harian jatuh <−100 lalu silang semula atas 0 | Tidak dinyatakan; *(andaian)* keluar asal Lambert: CCI jatuh <+100 | | chartschool.stockcharts.com (Trading Strategies → CCI Correction) |
| K157 | 'Last' Stochastic Technique | StockCharts ChartSchool | Stokastik perlahan(39,3) %K silang atas 50 DAN tutup > tutup tertinggi minggu lepas | *(andaian)* %K silang bawah 50 dan tutup < tutup terendah minggu lepas | | chartschool.stockcharts.com (The 'Last' Stochastic Technique) |
| K158 | 260-day High + VPN | Cesar Alvarez | Tutup tertinggi 260 hari, tiada high sedemikian dalam 15 hari sebelumnya; harga >$5; S&P500 > SMA200; VPN(10)>40; beli harga buka esok | Jual buka esok jika tutup −15%, +25%, atau selepas 60 hari | | alvarezquanttrading.com/blog/volume-positive-negative-indicator-for-breakouts/ (perlu index_benchmark) |
| K159 | Vortex crossover | Botes & Siepman | +VI(14) silang atas −VI (versi ketat: −VI <0.90, kemudian +VI >1.10) | −VI silang atas +VI | | chartschool.stockcharts.com (Vortex Indicator) |
| K160 | AlphaTrend | Kıvanç Özbilgiç | Garis AlphaTrend (1×ATR14, bertukar ikut MFI14) silang atas nilainya sendiri 2 bar lalu | Silang ke bawah; guna bar tertutup sahaja | | tradingview.com/script/o50NYLAZ-AlphaTrend |
| K161 | 44 MA | Siddharth Bhanushali (India); varian MA44 oleh manjunath_bn | SMA44 naik; lilin hijau dengan low ≤ SMA44 dan buka ≥ SMA44; beli atas high | Henti bawah low corak; sasaran 1:2 hingga 1:3 R | | chartink.com/screener/swing-intd-buy-sid-bhanushali-44-sma-strategy ; tradingview.com/script/XjolfZRy-MA44-Strategy |
| K162 | 5 EMA Alert Candle (beli) | Subashish Pani (Power of Stocks) | Lilin amaran sepenuhnya di bawah EMA5 tanpa sentuh; beli apabila harga tembus high lilin amaran | Henti pada low lilin amaran; sasaran ≥3R (asal intrahari; sumber kata peraturan sama untuk semua tempoh) | | my.tradingview.com/script/0cUu6m0O-PowerOfStocks-5EMA |
| K163 | 2-Bar Breakout | "sunilsenapati" (TradingView; tidak pasti Sunil Gurjar) | High semalam > high 2 bar sebelumnya; tutup hari ini > tutup semalam | Henti pada low semalam sahaja | | vn.tradingview.com/script/AT04nhBx-Sunil-2-Bar-Breakout-Strategy |
| K164 | Hidden Smash Day (beli) | Larry Williams | Dalam aliran naik, hari dengan high baharu tetapi tutup di 25% bawah julat; beli apabila harga tembus high hari itu | Henti bawah low hari itu; keluar untung tidak dinyatakan; takrif aliran perlu ditetapkan | | roboforex.com/blog/education/catch-your-smash-day-with-larry-williams/ |
| K165 | TPS | Larry Connors | Harga >SMA200, RSI(2)<25 dua hari berturut; beli 10%, tambah 20/30/40% pada setiap tutup lebih rendah | RSI(2)>70 | | wl6.wealth-lab.com/Forum/Posts/Connors-TPS-Strategy-40197 |
| K166 | Double 7s | Larry Connors & Cesar Alvarez | Tutup >SMA200 dan tutup terendah 7 hari | Tutup tertinggi 7 hari; tiada henti | K105 | strategyquant.com/fr/blog/larry-connors-double-7-strategy-tested-on-spy-and-8-other-markets/ |
| K167 | HV6/HV100 + Inside Day/NR4 | Connors & Raschke | Nisbah turun naik 6 hari / 100 hari <0.50 DAN hari dalam yang juga julat tersempit 4 hari; beli henti atas high keesokannya | Tidak dinyatakan | M11 | cryptodatadownload.com/blog/posts/inside-contraction-historical-volatility-strategy/ |
| K168 | Jack-in-the-Box | swingtradebot | Hari pecahan julat besar, kemudian hari dalam; beli 5 sen atas high hari pecahan | Henti 1 mata; pegang semalaman jika tutup kuat | K53 | swingtradebot.com/stock-screens/Bullish |
| K169 | The Strat 2-1-2 / 3-1-2 naik | Rob Smith | Bar naik atau bar luar, kemudian bar dalam; beli tembus high bar dalam; lilin bulanan, mingguan dan harian hijau | Henti pada low bar dalam; sasaran high bar sebelumnya | M70 | luxalgo.com/library/concept/the-strat.md |

## Kumpulan B — pembalikan / kontra-aliran

| K | Kaedah | Pencipta | Masuk | Keluar | Sumber |
|---|---|---|---|---|---|
| K170 | Smash Day (beli) | Larry Williams | Tutup bawah low semalam (ideal terendah 3–8 hari); keesokannya beli jika harga tembus high hari itu | Buka pertama yang untung, atau isyarat bertentangan (versi yang diuji blog) | prorealcode.com/topic/larry-williams-smash-day/ ; roguequant.substack.com/p/i-backtested-larry-williams-trading |
| K171 | Lizard (bullish) | Jeff Cooper | Low 10 hari baharu; buka dan tutup dalam 25% atas julat; beli atas high keesokannya sahaja | Henti 1 mata; keluar pada tutup jika tidak kena henti | money.it/Il-segnale-di-trading-lizard-di ; swingtradebot.com |
| K172 | Turtle Soup / Turtle Soup Plus One | Raschke & Connors | Low 20 hari baharu, dengan low 20 hari sebelumnya ≥4 hari lalu; beli henti atas low lama (hari sama, atau esok untuk Plus One) | Henti bawah low baharu, kemudian mengekor | luxalgo.com/library/concept/turtle-soup.md ; articles.stockcharts.com |
| K173 | Twin Tower | Oliver Velez | Kejatuhan bawah MA20 yang menurun; bar merah besar; kemudian bar hijau lebih besar tutup atas high bar merah; beli atas high bar merah | Henti bawah low 2 bar; setelah harga atas MA20, ekor dengan MA20 | moneyshow.com/articles/videotranstr-25463 |
| K174 | Bullish Kicker + T-line | Stephen Bigalow | Selepas hari merah, harga buka jurang ≥ harga buka semalam dan bentuk lilin bullish | Isyarat lilin jual + tutup bawah T-line (EMA8) | news.cqg.com/blogs/commentary/2023/05/kicker-signal-one-most-powerful-candlestick-reversal-signals ; elitetrader.com/et/threads/t-line.347201/post-5147419 |
| K175 | ADX Gapper | Connors & Raschke (Street Smarts) | ADX(12)>30, +DI(28)>−DI(28); harga buka bawah low semalam; beli henti di low semalam | Tidak dinyatakan (separa) | cryptodatadownload.com/blog/posts/adx-gapper-trading-strategy-filtered-python/ |
| K176 | Hikkake | Dan Chesler | Bar dalam, kemudian bar dengan high dan low lebih rendah; beli henti di high bar dalam; batal selepas 3 bar | Tiada henti atau sasaran (separa) | tradingsetupsreview.com/hikkake/ |

## Kumpulan C — separa (perlu takrif atau data tambahan)

| K | Kaedah | Pencipta | Ringkasan | Apa yang kurang | Sumber |
|---|---|---|---|---|---|
| K177 | Slingshot Bullish (bukan K93 EMA4) | Gaya Cooper | Semalam high 2 bulan; low hari ini ≥10 sen bawah low semalam; beli 10 sen atas high semalam; henti 2 mata | Tiada keluar untung | swingtradebot.com |
| K178 | The Anti | Linda Raschke | Stokastik (7,10,3): garis perlahan naik ≥4 bar; garis pantas undur lalu bengkok semula tanpa silang; beli atas high bar bengkok | Keluar asal = tutup hari sama; keluar swing perlu dipilih | roboforex.com (strategi Raschke) ; futures.io/thinkorswim/23724-anti-strategy-linda-bradford-rasche-2.html |
| K179 | Inventory Retracement Bar (IRB) | Rob Hoffman | Dalam aliran naik, bar buka dan tutup ≥45% bawah high-nya; beli atas high | Takrif aliran, henti dan keluar tiada | whselfinvest.de/en-de/trading-platform/trader-tools/technical-analysis/13-rob-hoffman-irb-inventory-retracement-bar |
| K180 | Wick Play | Oliver Kell | Saham kuat tinggalkan sumbu atas; esok buka dalam sumbu dan kekal atas badan sebelumnya; hari ke-3 beli atas high | Tiada henti atau keluar | in.tradingview.com/script/TGp7b78L-TAPLOT-Wick-Play |
| K181 | 10EMA Basic Swing | RealLifeTrading | Semalam tutup bawah EMA10, hari ini tutup atas; harga > EMA50; beli pada tutup | Tiada keluar | tr.tradingview.com/scripts/reallifetrading |
| K182 | Consolidation Pivot | Ross Haber (TraderLion) | Tembus swing high sebelumnya di separuh bawah tapak, volum naik, atas garis trend puncak menurun, MA berhimpun; henti pada MA yang dihormati | Takrif tapak dan garis trend perlu dikod; tiada keluar | traderlion.com/profile/ross-haber/consolidation-pivot/ |
| K183 | Elephant Bar / Bull 180 | Oliver Velez (penerangan pihak ketiga) | Harga > SMA20 > SMA200; bar gajah atau bar menelan "180"; beli atas high; henti low bar | Tiada ambang saiz bar gajah; tiada keluar untung | id.tradingview.com/script/MTQNwtFZ |
| K184 | Oversold Bounce Trade | Deron Wagner (Morpheus) | Lantunan tajam dari bawah, rehat ketat 2–3 hari atas EMA10; beli atas high semalam | Tiada henti atau keluar | morpheustrading.com/blog/bounce-trade/ |
| K185 | RMV Pivot | Richard Moglen (Deepvue) | RMV <10 membentuk julat, <5 = ketat; beli tembus high pivot | Formula RMV milik Deepvue, tidak didedahkan; tiada keluar | en.rattibha.com/thread/1804201351540588679 ; tradingengineered.substack.com/p/how-i-use-relative-measured-volatility |
| K186 | Pullback Reclaim | Martin Luk | Naik ≥30% dalam 1/3/6 bulan; celup bawah zon sokongan (EMA9/21/50 atau paras mendatar) lalu tutup kuat semula di atas; henti 1–4%; ekor EMA9; potong 10–15% pada ≥3R | Zon sokongan ikut pertimbangan; sebahagian guna AVWAP. ≈ M77 | financialwisdomtv.com/post/martin-luk-s-pullback-trading-strategy-how-the-2025-u-s-investing-champion-finds-low-risk-high-re |
| K187 | Parabolic Long | Qullamaggie | Selepas jatuh 50–60%+ dalam beberapa hari, beli high julat pembukaan atau lilin 5 minit hijau pertama | Masuk intrahari; tiada henti atau keluar | qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/ |
| K188 | Peraturan pecahan Dan Zanger | Dan Zanger | Beli pecahan corak dengan volum naik, maks 5% atas titik pecah; jual bawah titik pecah (5–7%); jual 20–30% pada untung 15–20% | Corak dipilih secara mata kasar; "berhenti naik" kabur | financialwisdomtv.com/post/dan-zanger |
| K189 | 多方炮 (dua lilin hijau mengapit satu merah) | Peruncit China | Lilin hijau besar, lilin merah kecil volum rendah atas harga buka lilin pertama, lilin hijau volum tinggi menelan lilin merah; MA tersusun naik | Tiada ambang angka, henti atau keluar | caifuhao.eastmoney.com/news/20260314193143500151850 |
| K190 | 龙回头 ("naga menoleh") | Peruncit China | Naik >40% termasuk hari had-naik, undur volum rendah ke MA10 atau 0.382; beli hari had-naik pertama selepas undur | Hari had-naik tiada di AS (*andaian* ganti hari +10%) | finance.ifeng.com/c/7chqkxF3Xtq |
| K191 | OTT (Optimized Trend Tracker) | Anıl Özekşi | Harga atau garis sokongan silang atas garis OTT; keluar silang bawah | Panjang dan peratus lalai tiada; formula perlu diambil dari kod | tradingview.com/script/zVhoDQME/ |
| K192 | Ross Hook | Joe Ross | Selepas 1-2-3 naik, beli henti atas cangkuk (pivot high sebelumnya) | Takrif pivot perlu dikod; tiada keluar | prorealcode.com/prorealtime-indicators/ross-hook-pattern-indicator/ |
| K193 | Ascending Scallop | Tom Bulkowski | Dalam aliran naik, bentuk J (dua puncak, lembah bulat, puncak kanan lebih tinggi); beli tutup atas puncak tertinggi; henti bawah lembah; sasaran = puncak + 62% × (puncak − lembah) | Corak perlu dikesan dengan kod | thepatternsite.com/ascscallop.html |
| K194 | Hot IPO Pullback | swingtradebot | ≥15% atas harga tawaran IPO dalam 5 hari pertama, undur 2–4 hari; beli atas high semalam; henti low semalam; keluar 1–5 hari dengan henti mengekor | Harga tawaran IPO tiada dalam OHLCV | swingtradebot.com/stock-screens/Bullish |
| K195 | All-Time-High Trend Following | Wilcox & Crittenden (2005); Zarattini, Pagani & Wilcox (2025) | Tutup ≥ tutup tertinggi sepanjang masa; beli buka esok; henti mengekor 10×ATR | Data sebelum 2019 tiada; pegangan purata ~305 hari (kedudukan, bukan swing) | cis.upenn.edu/~mkearns/finread/trend.pdf ; quantpedia.com/strategies/trend-following-effect-in-stocks |

## Peraturan keluar sahaja (boleh dipasang pada mana-mana kaedah masuk)

| X | Peraturan | Pencipta | Ringkasan | Sumber |
|---|---|---|---|---|
| X01 | 7-Week Rule | Gil Morales | Selepas ≥35 hari di atas MA10, jual apabila tutup bawah MA10 dan harga keesokannya tembus low hari itu | tradingview.com/script/kDC1dFjU-7-Week-Rule/ |
| X02 | ATRx (regangan) | Formula Jeff Sun; ambang oleh Kyna | ATRx = ((tutup − SMA50)/SMA50) ÷ (ATR14/purata tutup 14 hari); 4–7.5 jangan masuk baharu, 7.5–10 potong, ≥10 jual sebahagian. Jeff Sun sendiri: elak masuk >4×ATR% atas SMA50 atau bawah SMA200 menurun; ambil untung separa 7.5–8× | tradingresourcehub.substack.com/p/how-leverage-ai-to-customise-charts-atrx-case-study ; thestratlab.substack.com/p/backtesting-jeff-suns-50-sma-atr |
| X03 | Squat & Reversal / Tennis Ball Action | Mark Minervini | Peraturan pegang/jual selepas pecahan (pertimbangan, bukan mekanikal): jual jika pembalikan kena henti; jual saham yang tidak melantun cepat dari undur ke paras pecahan | rgarg333.wordpress.com/minerbook2/ |
| X04 | MA Violation | Morales & Kacher | Tutup bawah MA N hari, kemudian harga tembus low hari itu keesokannya (umum bagi X01) | edgerater.com/blog/morales-and-kacher-signals-template |
| X05 | Double-close 21-SMA | Ross Haber | Jual pada tutup ke-2 berturut bawah SMA21 (tutup semula di atas = kira semula); peneraju awal jual ⅓–½, saham matang jual semua; baki keluar pada 2 tutup bawah SMA50; jangan guna jika ADR 20 hari ≥10% | traderlion.com/profile/ross-haber/21-day-moving-average-sell-rule/ |
| X06 | Quick / Quicksand / Grateful Dead | Mike Webster | Hanya selepas untung ≥10%: garis RS mingguan silang bawah SMA8 → jual sebahagian; jatuh lagi → jual lagi; pecah SMA21 → jual baki (perlu data SPY) | deepvue.com/indicators/mike-webster-indicators/ |
| X07 | Tangga jual defensif | Deepvue | Tutup bawah EMA10 jual ⅓; pecah EMA20 jual ⅓; SMA50 keluar semua; >25% atas EMA20 ambil sebahagian untung | deepvue.com/technical-analysis/selling-with-moving-averages/ |
| X08 | Distribution Cluster | Deepvue Market Navigator | 3 hari agihan (julat tutup <50% dengan volum > bar sebelum) dalam 7 bar = isyarat jual | deepvue.com/indicators/when-to-sell-stocks-market-navigator/ |

---

# Tambahan Pusingan 1 (14 Okt 2026, 18:05–18:32)

Sumber: buku asal (Street Smarts, Hit & Run, Landry, Pristine, Farley, Minervini, Williams, Crabel), pustaka skrip (TradingView, ProRealCode, Wealth-Lab, QuantConnect, GitHub sofus-nl), komuniti Jepun/China/Korea/Taiwan/Indonesia/Thai/Turki, kajian akademik, Deepvue/TraderLion/fintwits.
Digugurkan sebagai varian remeh: "Simple share breakout" ProRealCode (≈ Donchian), 20일 신고가 매매 (≈ Donchian + MA), Webby RSI sebagai keluar (≈ K119), 50-SMA ATR% Jeff Sun (= X02), Cooper Extended Level Boomer (= K149), Landry Persistent Pullback (≈ TKO), Crabel 2-Bar NR (≈ NR7), Lee & Swaminathan (perlu saham terbitan).
Masih tiada akses: Reddit (disekat sepenuhnya), stockbee.blogspot.com (robots.txt), pustaka AmiBroker (perlu log masuk), Elite Trader. Had carian web (200) habis kira-kira 18:15.

## Kumpulan A — sedia untuk backtest OHLCV

| K | Kaedah | Pencipta | Masuk | Keluar | ≈ | Sumber |
|---|---|---|---|---|---|---|
| K196 | Bull Hook | Toby Crabel | Buka atas high semalam, tutup bawah tutup semalam, julat lebih sempit; beli henti di Buka + Stretch (Stretch = 2 × SMA10 bagi min(H−O, O−L)) | Henti entry − 6×ATR20; keluar masa pada tutup hari ke-n (1–40) | | oxfordstrat.com/trading-strategies/pattern-bull-hook/ |
| K197 | Pristine Buy Setup (PBS) | Oliver Velez / Pristine | Aliran naik (HH/HL, MA20 & MA40 naik); ≥3 high menurun berturut atau ≥3 bar merah; beli $0.01 atas high semalam (atau atas +COG / bottoming tail / bar sempit) | Henti bawah low bar semasa/sebelum; sasaran min = pivot high sebelumnya; selepas 2 bar menguntungkan, ekor bawah setiap low | EMA9/21 pullback | pdfcoffee.com/trading-the-pristine-method-3-pdf-free.html |
| K198 | Explosion Gap Pivot | Dave Landry | Jurang naik ke high ≥20 hari; low kemudian uji jurang tanpa menutupnya; low lebih tinggi; beli hari pertama atas high sisi kanan pivot | Henti $0.25–1.00 bawah low ujian; keluar Landry (½ pada 1R, henti ke pulang modal, ekor low 2–3 bar) | K40 jurang naik | pdfcoffee.com/davelandrys10best-swing-trading-patterns-and-stratigies-pdf-free.html |
| K199 | Kiss MA Goodbye | Dave Landry | ≥10 hari atas SMA10; pembetulan menyentuh SMA10; beli atas high sebelumnya | Keluar Landry | K181 | whatheheckaboom.wordpress.com/2014/01/11/book-review-of-the-laymans-guide-to-trading-stocks-by-dave-landry/ |
| K200 | First Kiss After Daylight | Dave Landry | Selepas low utama baharu, ≥5 bar rali dengan low atas SMA10; undur menyentuh SMA10; beli apabila aliran sambung *(andaian: atas high sebelumnya)* | Keluar Landry | | sama seperti K199 |
| K201 | 3C (Cup Completion Cheat) | Mark Minervini | Naik 25–100%+ dalam 3–36 bulan, atas SMA200 naik; rehat 5–10% di sepertiga tengah cawan; beli atas high rehat dengan volum ≥125% purata 50 hari | Henti bawah low rehat atau tutup bawah MA20; keluar untung tidak dinyatakan | K97 Low Cheat | nodeadcow.blogspot.com/2018/04/minervini-3c-pattern.html ; profitvisionlab.com/en/sepa-e05-handle-cheat |
| K202 | 3rd Watch | Alan Farley | Pecahan puncak tiga kali ke high 6 bulan; tiada high baharu dalam 4 minggu sebelumnya; volum bar pecahan ≥150% purata; masuk pada bar sempit dekat high atau undur pertama | Tidak dinyatakan | K45 cawan & pemegang | fliphtml5.com/vvba/eeop/The_Master_Swing_Trader/306 |
| K203 | Three-Bar High/Low | Larry Williams | Aliran titik ayun naik; beli pada SMA3 bagi low | Ambil untung pada SMA3 bagi high | | it.tradingview.com/script/x2LaBQWu-Larry-Williams-Strategies-Indicator |
| K204 | Short/Intermediate-term Low | Larry Williams | Low jangka pendek = low dengan low lebih tinggi di kedua-dua sisi; low pertengahan = low jangka pendek diapit low jangka pendek lebih tinggi; beli atas high semalam (tafsiran penulis skrip) | Henti mengekor di low jangka pendek terkini; sasaran = high pertengahan terakhir + (high itu − low terendah) | | sama seperti K203 |
| K205 | Chande Kroll Trend | PineIndicators | Tutup silang atas hentian bawah (low terendah 21 bar + 3×ATR10) dan tutup > SMA21 | Tutup < hentian atas (high tertinggi 21 bar − 3×ATR10) | Supertrend | kr.tradingview.com/script/GoHLj2XP-Chande-Kroll-Trend-Strategy-SPX-1H-PINEINDICATORS |
| K206 | NRTR (Nick Rypock Trailing Reverse) | Nick Rypock (AFL Marketcalls) | Garis NW < harga (Revers = 2×WMA(H−L,20); NW naik berperingkat) | NW > harga | Supertrend | marketcalls.in/2009/07/nick-rypock-trailing-reverse-trading-systemnrtr.html |
| K207 | Coral Trend | LazyBear (THV) | Garis Coral (EMA 6 peringkat, sm=21, cd=0.4) bertukar hijau *(andaian)* | Bertukar merah *(andaian)* | KAMA | marketcalls.in/amibroker/coral-trend-indicator-amibroker-afl-code.html |
| K208 | Gann HiLo Activator | Robert Krausz | Tutup > SMA3 bagi high (bar sebelumnya) | Tutup < SMA3 bagi low | SSL | tradingview.com/script/PyFdxzcj-Gann-HiLo-Activator-Strategy/ |
| K209 | Aberration | Keith Fitschen (1986) | Tutup > band atas BB(20,2) dan ATR20 antara 0.8× hingga 2.0× median 50 bar | Harga kembali ke band tengah (SMA20) | M39 BB100 | il.tradingview.com/script/MHCzo0OZ-Aberration-Trend-Following-Strategy |
| K210 | Bollinger Bandit | (ProRealCode; pencipta tidak dinamakan) | Tutup − tutup[29] > 0, kemudian beli henti di band atas (SMA50 + 1.25 SD) | Jual henti di purata liqDays (mula 50, turun 1 setiap bar, minimum 10) selagi bawah band atas | M39 BB100 | prorealcode.com/topic/bollinger-bandit |
| K211 | Dynamic Breakout II | George Pruitt | N menyesuai ikut turun naik (N × (1 + Δσ/σ), had 20–60); beli apabila tutup semalam > band atas BB(N,2) dan harga > high N hari | Harga < SMA(N) | Donchian | quantconnect.com/tutorials/dynamic-breakout-ii-strategy/ |
| K212 | Livermore System | Perry Kaufman (Oxfordstrat) | Beli harga buka selepas harga tembus dua pivot bekalan terkini (pivot = ayunan ≥4×ATR) | Tembus pivot permintaan terkini, atau henti entry − 6×ATR20 | | oxfordstrat.com/trading-strategies/livermore-system-1/ |
| K213 | Following the Trend | Andreas Clenow | SMA50 > SMA100 dan tutup tertinggi 50 hari | Ekor 3×ATR bawah tutup tertinggi sejak masuk | Turtle | wl6.wealth-lab.com/Forum/Posts/Strategy-from-the-book-quot-Following-the-Trend-quot-33426 |
| K214 | 52 Weeks High Strategy | gabri (ProRealCode) | Tutup silang atas 1.03 × (high tertinggi 254 hari − 1.5×SD tutup 254 hari) | Tutup silang bawah SAR Wilder ARC(7,3), atau bawah 0.97× paras itu selepas 10 bar; henti keras 15% | K37 | prorealcode.com/prorealtime-trading-strategies/52-weeks-high-strategy-long/ |
| K215 | Gaussian Channel + StochRSI | cs_lev (atas saluran DonovanWall) | Saluran naik (4 kutub, tempoh 144, TR×1.414), tutup > band atas, StochRSI %K >80 atau <15 | Tutup kembali bawah band atas atau saluran merah; ekor di band bawah | Keltner | kr.tradingview.com/script/d1JxXpid-TRADLEWARE-Gaussian-Channel-StochRSI-BTC/ |
| K216 | Rahul Mohindar Oscillator (RMO) | Rahul Mohindar | SwingTrd2 (EMA30) silang atas SwingTrd3 sementara RMO (EMA81) > 0 | *(andaian)* silang bertentangan | MACD cross | luxalgo.com/library/indicator/rahul-mohindar-oscillator/ |
| K217 | ROC Breakout | sofus-nl (gabungan idea Bulkowski) | Tutup > high 20 hari; ROC21 > 0 dan > nilainya 5 bar lalu; volum > 1.4× purata 50 hari; tutup > SMA50; pangkat RS > 70 (dikira dalam universe) | Henti 1.5×ATR atau bawah paras pecah; jual 50% pada +2×ATR, ekor low ayun; keluar jika ROC < 0 | Donchian | raw.githubusercontent.com/sofus-nl/swing-trading-strategies/main/strategies/18-roc-breakout.md |
| K218 | Proximity Pullback | sofus-nl | Dalam 5% dari high 52 minggu; undur 3–10% dalam 3–10 bar dengan volum menurun, kekal atas EMA21/SMA50 naik; bar lantun tutup separuh atas dengan volum > purata 20 hari | Henti low undur atau 1.5×ATR; sasaran 1 = high sebelumnya, sasaran 2 = 2× kedalaman undur | M66 | raw.githubusercontent.com/sofus-nl/swing-trading-strategies/main/strategies/21-proximity-pullback.md |
| K219 | Bull Flag | Bulkowski (melalui sofus-nl) | Tiang ≥10% dalam 1–3 minggu; bendera 5–15 bar, undur <50%; tutup > EMA21; volum pecah ≥1.5× purata; RSI 50–70 | Henti low bendera atau 1.5×ATR; sasaran 1 = panjang tiang, sasaran 2 = 1.5× tiang | M104 HTF | raw.githubusercontent.com/sofus-nl/swing-trading-strategies/main/strategies/08-bull-flag.md |
| K220 | ADX dip + CMF channel breakout | Pendergast (TASC) | ADX10 jatuh bawah 20 lalu naik semula, CMF21 > 0, pecahan saluran 20/55 baharu | Ekor di saluran bawah 20 minggu | Donchian | technical.traders.com/tradersonline/display.asp?art=7973 |
| K221 | Price Compression Scanner | sripathi_venkatesh86 (logik Chartink) | High 10 hari menurun dan low 10 hari menaik; beli tembus high julat | Tidak dinyatakan | M11 / M06 | in.tradingview.com/script/R6pJWRad-Price-Compression-Scanner-Chartink-Logic |
| K222 | 移動平均線大循環分析 (Kitaran Besar MA) | 小次郎講師 (Jepun) | MA 5/20/40 (EMA atau SMA — sumber bercanggah); masuk Peringkat 1 (5>20>40, semua naik); masuk awal Peringkat 6 (5>40>20) | Peringkat 2 (20>5>40) jangan tambah; Peringkat 3 tutup semua | Susunan MA | go.sbisec.co.jp/media/report/fo_technical_analysis/fo_technical_analysis_04.html ; kabu.com/kabuyomu/money/263.html |
| K223 | パーフェクトオーダー押し目買い (Perfect Order dip-buy) | crexgroup (Jepun) | SMA 25>75>200 semua naik (mingguan 13/26/52); undur ke SMA25 atau SMA75 dengan lilin lantun bullish | Henti apabila pecah jelas bawah MA yang dilantun; keluar apabila SMA25 silang bawah SMA75 | Susunan MA + undur | crexgroup.com/ja/sec/stock-investment/stock-perfect-order-guide/ |
| K224 | 直升机空中加油 (Helikopter isi minyak di udara) | Eastmoney (China) | ≥5 lilin naik berturut dengan volum naik; kemudian lilin turun kecil dengan volum < separuh purata lilin-lilin itu; beli dekat tutup hari itu atau pagi esok | Jual pada hari volum sangat besar atau untung >10% | | caifuhao.eastmoney.com/news/20180920080755755024420 |
| K225 | 均线首次粘合向上发散 (MA berhimpun kali pertama, kemudian berkipas naik) | ifeng; forum TBQuant | MA 5/10/20 berhimpun (sebaran ketiga-tiga MA ≤0.5×ATR14 pada bar sebelumnya); beli apabila tutup atas MA tertinggi; kecil jika MA60 menurun | Tidak dinyatakan | K72 Launchpad | finance.ifeng.com/c/7fENritoUcq ; bbs.tbquant.net/thread/20250320141635791539 |
| K226 | 银山谷 / 金山谷 (Lembah Perak / Emas) | Eastmoney, ifeng | Lembah perak: MA pendek silang atas MA tengah dan panjang, MA tengah silang atas MA panjang (segi tiga naik); lembah emas: lembah kedua ≥ lembah pertama (lebih dipercayai) | Pecah bawah MA terpanjang | Golden Cross | caifuhao.eastmoney.com/news/20240706094516670950890 *(tempoh MA tidak dinyatakan; andaian 5/10/20)* |
| K227 | 蚂蚁上树 (Semut memanjat pokok) | ifeng / Eastmoney | Selepas tapak, ≥5 lilin naik kecil dengan volum rendah menunggang MA5; beli pada pecahan volum, atau celup bawah MA5 yang bertahan dekat MA10 dengan sumbu bawah | Tidak dinyatakan | | finance.ifeng.com/a/20151102/14052198_0.shtml |
| K228 | 苦尽甘来 (Pahit kemudian manis) | ifeng | Dalam aliran naik: lilin naik besar, 3 lilin turun kecil dengan volum mengecut, kemudian lilin naik lebih besar dengan volum tinggi menutup ketiga-tiganya | Tidak dinyatakan | Rising Three Methods | finance.ifeng.com/a/20151102/14052198_0.shtml |
| K229 | 猎豹出击 (Serangan Cheetah) | Eastmoney | Selepas kejatuhan panjang dengan volum kering, tutup silang atas MA60 dan >4.5% atas tutup semalam | Tidak dinyatakan | | caifuhao.eastmoney.com/news/20180920080755755024420 |
| K230 | W 매매 기법 (Teknik W) | 성경호 (Korea) | MA 5/15/200 semua naik dan tersusun; beli berperingkat apabila harga silang atas MA20 | Ambil untung di high sebelumnya | Rampas semula MA | tilnote.io/pages/689afd5adf13c4ef330d9a51 |
| K231 | MOST (Moving Stop Loss) | Anıl Özekşi | EMA silang atas garis MOST | Silang bertentangan | K191 OTT | id.tradingview.com/script/kZdhvAxZ-MOST-STRATEGY |
| K232 | PMax (Profit Maximizer) | Kıvanç Özbilgiç | MA silang atas garis PMax | Silang bertentangan | Supertrend | tr.tradingview.com/script/7yn5dteO-Profit-Maximizer-Strategy |
| K233 | Trend Factor | Han, Zhou & Zhu (JFE 2016) | Nisbah MA L hari / tutup untuk L = 3…1000 hari; regresi keratan rentas bulanan; skor = beta terlicin × nisbah hari ini; beli kuintil teratas | Imbang semula bulanan | M84 MAD | profiles.wustl.edu (Trend Factor) ; wrds-www.wharton.upenn.edu/documents/1119/WARSP_TrendChina.pdf |
| K234 | Momentum Semalaman (Overnight persistence) | Lou, Polk & Skouras (JFE 2019) | Pangkat saham ikut pulangan semalaman bulan lepas (tutup semalam → buka; kertas guna VWAP 9:30–10:00, harga buka harian = proksi); beli desil teratas | Pegang 1 bulan | | personal.lse.ac.uk/polk/research/TugOfWar.pdf |
| K235 | Time-series + Dual Momentum saham tunggal | D'Souza et al. (2016) | Beli jika pulangan 12-1 > 0; versi dual: kuintil teratas antara yang positif | Bulanan (dual lemah sejak ~2000) | I01 12-1 | cxoadvisory.com/momentum-investing/time-series-and-dual-momentum-for-individual-stocks/ |
| K236 | GRJMOM (momentum terlaras risiko umum) | Fan, Kearney, Li & Liu (JEDC 2022) | Skor = R(12-1) / σ^N (σ harian; N optimum ~2.3–2.8) | Bulanan | M96 Sharpe | pureadmin.qub.ac.uk/ws/files/380981888/Momentum_and_the_cross_section_of_stock_volatility.pdf |
| K237 | Continuing Overreaction (CO) | Byun, Lim & Yun (JFQA 2016) | Volum bertanda (+ jika pulangan bulan > 0, − jika < 0); jumlah berwajaran 12 bulan (12 untuk terkini … 1 terlama) ÷ purata volum bulanan; beli desil teratas | Langkau 1 bulan, pegang 3–12 bulan (6 dalam jadual utama) | | cambridge.org (abstrak) ; kertas kerja 2012 |
| K238 | High-Volume Return Premium | Gervais, Kaniel & Mingelgrin (JF 2001) | Hari pembentukan: volum dolar dalam 5 teratas daripada 50 hari (atau minggu teratas daripada 10) | Pegang 20 hari dagangan | K81 HVE | rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf |
| K239 | Price-Path Convexity (penapis) | Gulen & Woeppel (JFQA) | Kecembungan = [(P1+PN)/2 − purata P] / [(P1+PN)/2] atas 1 bulan (atau 5/10 hari); pilih laluan cekung | Pegang 1 bulan / 10 / 5 hari | M56 FIP | jfqa.org/wp-content/uploads/2025/05/25822_Price-path-convexity.pdf |
| K240 | MAX / Lottery (penapis) | Bali, Cakici & Whitelaw (JFE 2011) | MAX = pulangan harian terbesar bulan lepas; elak desil MAX tertinggi | Bulanan | | alphaarchitect.com/hot-off-the-jfe-press-maxing-out-your-returns/ |
| K241 | Momentum × Turun Naik | Arena, Haggard & Yan (2008); Wei | Momentum 6/6 dalam saham turun naik tinggi (turun naik jumlah ≈ sama berkesan); Wei: saham saiz > median, kuintil turun naik 6 bulan tertinggi, beli kuintil pulangan 6 bulan teratas | Pegang 6 bulan; ganti 1/6 portfolio setiap bulan | I01 | quantpedia.com/strategies/momentum-and-reversal-combined-with-volatility-effect-in-stocks |
| K242 | Consistent Momentum | Chen, Chou & Hsieh (SSRN 2652592) | Beli hanya saham dalam desil teratas bagi tetingkap t−7..t−1 DAN t−6..t | Langkau 1 bulan, pegang 6 bulan | I01 | quantpedia.com/strategies/consistent-momentum-strategy |
| K243 | Breakout 1M / 3M Base | Stockbee (imbasan) | Tutup semalam ≤10% atas low 21 hari (atau 63 hari); tutup hari ini ≥90% high 21 (63) hari; naik ≥4%; volum > semalam; tutup di 30% atas julat; purata nilai dagangan > $2J | *(andaian)* keluar momentum burst: 3–5 hari, henti jika rugi >8% | M32 | tikamalma.substack.com/p/systems-setups-and-process-of-swing ; fintwits-most-popular-stock-market-scans.onrender.com (Stockbee) |
| K244 | Declining-tops trendline → pengesahan Weinstein | Ross Haber | Pecah garis trend puncak menurun = kedudukan permulaan kecil; belian penuh pada tutup mingguan atas MA30 minggu dan atas puncak tapak, MA30 rata/naik, volum ~2× minggu sebelumnya | Henti "ketat" (paras tidak dinyatakan) | M37 | traderlion.com/profile/ross-haber/declining-tops-trendline/ |
| K245 | Range Breakout | Richard Moglen | Hari dalam ketat di bawah paras utama, atas EMA21 dan SMA50; beli tembus pivot | Henti low hari pecah; pulang modal selepas hari susulan kuat; jual 25–50% ketika kuat; batal jika harga tembus dan tutup semula bawah paras pecah | K182 | traderlion.com/profile/richard-moglen/trade-opportunity-case-study-of-the-week-ttan-range-breakout-april-2025/ |
| K246 | Open = Low Day | Deepvue (Moglen) | Harga buka = low hari itu; low hari = titik risiko | Henti bawah low hari itu; keluar untung tidak dinyatakan | | deepvue.com/screener/find-strong-stocks-on-down-days/ |

## Kumpulan B — pembalikan / kontra-aliran

| K | Kaedah | Pencipta | Masuk | Keluar | Sumber |
|---|---|---|---|---|---|
| K247 | Gilligan's Island (beli) | Jeff Cooper | Jurang turun ke low baharu ≥2 bulan; tutup ≥ buka dan di separuh atas julat; esok beli atas high hari itu | *(andaian)* henti dekat bar corak; pulang modal apabila untung; pegang "beberapa hari" | traderpedia.it/wiki/index.php/Gilligan's_Island |
| K248 | Whiplash | Connors & Raschke | Buka jurang bawah low semalam; tutup > buka dan di 50% atas julat; beli pada tutup | Keluar segera jika buka esok < tutup; jika tidak, ekor henti (cara tidak dinyatakan) | thechartist.com.au/wp-content/uploads/2024/12/504/StreetSmarts(LaurenceConnors).pdf |
| K249 | Three-Day Unfilled Gap Reversal | Connors & Raschke | Jurang turun yang tidak ditutup pada hari jurang; beli henti 1 tik atas high hari jurang selama 3 sesi, kemudian batal | Henti di low hari jurang; henti mengekor | sama seperti K248 |
| K250 | Reversal Gap | Dave Landry | Low ≥2 bulan; jurang naik dalam ~1 hari; undur sehari (high & low lebih rendah); beli atas high undur; batal jika jurang ditutup | Henti bawah low undur; keluar Landry | pdfcoffee.com/davelandrys10best-swing-trading-patterns-and-stratigies-pdf-free.html |
| K251 | Key Reversal Bar | Deepvue Market Navigator | Buka bawah low bar sebelumnya, tutup atas high bar sebelumnya | Tidak dinyatakan | deepvue.com/indicators/when-to-buy-stocks-market-navigator/ |
| K252 | Nearness to 52-week Low | Chen & Yu (2016) | LOW = harga / low 12 bulan; beli 10% saham paling hampir low (gabung 50/50 dengan momentum naikkan Sharpe 0.66 → 0.98) | Pegang 1 bulan; kesan berbalik negatif menjelang bulan ke-3 | cxoadvisory.com/technical-trading/implications-of-52-week-highs-and-lows-for-stock-returns/ |

## Kumpulan C — separa

| K | Kaedah | Pencipta | Ringkasan | Apa yang kurang | Sumber |
|---|---|---|---|---|---|
| K253 | Wolfe Wave (beli) | Connors & Raschke (Street Smarts) | Pivot 1–4 (3 bawah 1); garis 1→3 unjur titik 5; beli apabila harga kembali atas garis itu; henti bawah low titik 5; sasaran garis 1→4 | Pemilihan pivot subjektif | thechartist.com.au (Street Smarts PDF) |
| K254 | Fakeout-Shakeout | Connors & Raschke | Selepas pecah turun dari para/segi tiga, harga kembali ke titik pecah; beli henti tepat atasnya | Buku sendiri kata peraturan tepat sukar diberi; ≈ K172 | sama |
| K255 | Pause That Refreshes / Pristine Breakout | Pristine | Tapak sempit volum ringan dekat MA20 naik, kemudian pecah rintangan utama; jual ke dalam pecahan ke-2 | "Rintangan utama" tidak ditakrif | pdfcoffee.com/trading-the-pristine-method-3-pdf-free.html |
| K256 | First Thrust | Dave Landry | Low utama baharu, rali tajam, kemudian undur satu bar pertama; beli atas high-nya | "Utama" dan "tajam" tidak ditakrif | pdfcoffee.com (Landry 10 Best) |
| K257 | Witch Hat (beli, dicerminkan daripada peraturan jual) | Dave Landry | Aliran naik; pivot low; aliran sambung; undur tajam dekat pivot low; beli $0.10 atas high bar undur | Versi beli ialah cerminan *(andaian)*; ≈ M76 | sama |
| K258 | Six-Out Rule (bendera ketat) | Alan Farley | Selepas tujahan pecah tajam, kira bar kesesakan; beli pada bar 4 atau 5 dengan had dalam corak; keluar jika tiada kaki baharu menjelang bar 6 | Tiada sasaran; ≈ M104 | fliphtml5.com/vvba/eeop/The_Master_Swing_Trader/330 |
| K259 | RSI3M3 Cycle Buy | Walter Bressert | RSI3M3 jatuh <40 lalu naik; beli atas high hari naik; keluar apabila turun dari >60 dan harga pecah low hari turun | Formula RSI3M3 dan takrif low kitaran tidak diberi | cn.tradingview.com/script/FNk3wGex-RSI3M3-v-1-8 |
| K260 | RSI Pullback | sofus-nl (dikaitkan Connors/Alvarez) | Tutup > SMA200; RSI14 jatuh ke 40–50 selepas >70 dalam 10 bar; atas EMA21 naik; ADX > 20; volum ringan; bar lantun tutup 60% atas; keluar +1.5×ATR atau RSI >70 | Perlu penapis tarikh pendapatan; ≈ M59 | raw.githubusercontent.com/sofus-nl/swing-trading-strategies/main/strategies/04-rsi-pullback.md |
| K261 | Granville's 8 Laws (set) | Joseph Granville (pelbagai broker Jepun) | Hukum beli 1–3 pada MA200 (MA naik + harga silang atas; celup bawah MA naik lalu silang semula; jatuh ke MA naik tanpa pecah lalu naik); hukum jual 5–6 sebagai keluar *(andaian)* | "Jauh atas MA" tiada angka; hukum 2–3 ≈ undur ke MA | matsui.co.jp/fx/study/article/analysis/granville/ |
| K262 | 空中加油 (Isi minyak di udara) | ifeng / Eastmoney | Versi A: pecah tapak panjang + 2–3 hari had-naik, undur volum mengecut; versi B: undur ke MA20 yang bertahan; keluar tutup bawah MA5 atau MA5 silang bawah MA10 | Versi A perlu hari had-naik; versi B ≈ M08 | finance.ifeng.com/a/20180716/16386870_0.shtml |
| K263 | 美人肩 (Bahu jelita) | 163.com | Harga atas MA60; MA5/10 bersilang semasa terbentuk; volum mengecut ketika undur, mengembang ketika pecah; beli apabila harga terus naik selepas low kedua | Bentuk subjektif; keluar *(andaian)* tutup bawah MA20 | c.m.163.com/news/a/KPLRDTF5055247PY.html |
| K264 | Pecahan volum dari dasar (底部放量, tanpa nama) | Soal jawab cofool.com | Volum ≥2× purata 20 hari; tutup >3% atas high sebelumnya; atas MA250 naik; beli pada undur yang mengekalkan paras pecah; henti bawah low hari pecah / MA250 / −5%; sasaran +15–20% | Penapis kadar pusing ganti perlu data saham terapung; sumber ialah jawapan penasihat | licai.cofool.com/ask/qa_5619109.html |
| K265 | 盤整跳空法人買超股 (Jurang naik dari penyatuan + belian institusi) | Blog XQ (Taiwan) | High 12 bar < 1.045× low 12 bar dan buka > 1.015× high semalam; henti −7%, sasaran +7% | Perlu data belian bersih institusi dan modal saham | xq.com.tw/xstrader/?p=17928 |
| K266 | 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas lilin naik panjang) | 남석관 (Korea) | Selepas mendatar, lilin naik panjang pertama dengan volum (satu nota: lonjakan 30%+); beli 20% pada sentuhan pertama MA5; tambah selagi MA5/MA10 bertahan; keluar pecah MA5 | Perlu pemangkin berita | tilnote.io/pages/689b098ddf13c4ef330ed575 |
| K267 | 종가베팅 (Taruhan harga tutup) | 다아시 (Korea) | Pecah ke high baharu/sebelumnya dengan lilin naik panjang dan lonjakan volum; beli pada lelongan tutup; jual buka esok pada +1–3% | Pegangan semalaman sahaja; guna data aliran pelabur | tilnote.io/pages/68d6a687b01224c872324853 |
| K268 | BSJP (Beli Sore Jual Pagi) | Stockbit (Indonesia) | Tutup ≥1.05× tutup semalam; volum ≥2× purata 20 hari dan ≥ volum semalam; tutup ≥ MA5 dan ≥ buka; nilai dagangan > Rp5 bilion; jual pagi esok | Pegangan semalaman sahaja; tiada henti | stockbit.com/post/23061847 |
| K269 | CDC ActionZone | Piriya (Thailand) | Berasaskan EMA12/EMA26; bar hijau = beli, biru = pra-beli; merah = jual | Formula zon tepat tidak disahkan | th.tradingview.com/scripts/actionzone/ |
| K270 | Residual Momentum | Blitz, Huij & Martens (2011) | Regresi pulangan 36 bulan atas faktor Fama-French 3; jumlah residual 12-1 ÷ SD residual; beli desil teratas, bulanan | Perlu data faktor FF3 | quantpedia.com/strategies/residual-momentum-factor |
| K271 | SMAD (jarak MA jangka pendek) | Ko, Wang & Yang (FAJ 2025) | Jarak harga akhir bulan dari MA10; SMAD tinggi meramal pulangan lebih rendah | Formula tepat tidak di halaman | rpc.cfainstitute.org/research/financial-analysts-journal/2025/short-term-moving-average-distance |
| K272 | MAR (nisbah MA, "anchoring") | Park (Financial Review 2010) | MA pendek ÷ MA panjang; bersama jarak ke high 52 minggu menerangkan kebanyakan untung momentum | Panjang MA tidak diberi | ideas.repec.org/a/bla/finrev/v45y2010i2p415-447.html |
| K273 | Penapis rejim / crash momentum | Daniel & Moskowitz (2016); Barroso & Santa-Clara (2015) | Bendera bear = pulangan pasaran 24 bulan < 0; skala pendedahan ikut ramalan min/varians, atau sasaran turun naik 12% | Perlu siri pulangan portfolio momentum (boleh dibina daripada universe + indeks) | nber.org/system/files/working_papers/w20439/w20439.pdf |
| K274 | Screw Bar | Clement Ang | Semalam tutup di low; esok jurang semula atas high semalam dan tembus julatnya; tunggu ~30 minit; senarai semak: <4×ATR dari SMA50, ADR ≥4% | Masuk intrahari (beli harga buka = *andaian*); keluar umum: ½ pada 3R, ekor MA10/MA20 | traderlion.com/profile/clement-ang/clement-ang-qa/ |
| K275 | Low Tight Flag | Leif Soreide | Naik 60–90% dalam 40 hari; bendera ≤25% dalam (≤15% lebih baik); harga >$10 | Pencetus pivot *(andaian)*; tiada keluar | deepvue.com/screener/leif-soreide-screens/ |
| K276 | Rocket Base | Leif Soreide | Naik ≥80% dalam 40 hari; 25–50% bawah high 52 minggu; tapak 6–10 minggu; atas SMA50 & SMA200; SMA200 > sebulan lalu; SMA50>150>200; purata volum 50 hari >200K | Pencetus pivot *(andaian)*; tiada keluar | sama seperti K275 |
| K277 | Continuation Base | Kristjan Kullamägi (Deepvue) | Naik ≥25% sebulan lalu; volum minggu ini ≥50% lebih rendah daripada minggu lepas; harga dalam ±2% dari SMA10 | Imbasan pra-pecah sahaja; tiada pencetus/keluar; ≈ M07 | deepvue.com/screener/qullamaggie-screens/ |
| K278 | Mini Coil | Matt Caruso | High dan low 2 hari terakhir berada dalam julat hari sebelumnya | Pecahan julat *(andaian)*; tiada keluar; ≈ M70 | deepvue.com/screener/matt-caruso-screens/ |
| K279 | Power of 3 | Ben (@PatternProfits) | Tutup dalam −1.5% hingga +1% dari EMA10, EMA21 dan SMA50 serentak; pangkat RS IBD ≥70; harga >$4 | Tiada pencetus/keluar; ≈ K96 | fintwits-most-popular-stock-market-scans.onrender.com (Ben → Power of 3) |
| K280 | "Quite and Tight" | Vo (@LignoL23) | Naik ≥75% dari low 63 hari; ADR20 >5 dan menurun dalam 10 hari; volum <0.75× purata 50 hari; trend intensity >1 | Dua istilah tidak ditakrif; tiada keluar | fintwits-most-popular-stock-market-scans.onrender.com (Vo) |
| K281 | Down Days Tell | Mike Webster | Harga >$20; >2% atas SMA200; ≤1% bawah SMA50; julat tutup >75% pada hari pasaran turun *(andaian)* | Perlu data indeks; tiada keluar; ≈ K91 | deepvue.com/screener/mike-webster-screens/ |
| K282 | Cross Fire | Mike Webster | Naik >1.5% hari ini; julat tutup >80%; dalam 20% dari high 52 minggu; >1% atas SMA21; RS 3 & 12 bulan >80; purata nilai dagangan >$5J | Perlu pangkat RS; tiada keluar | sama seperti K281 |
| K283 | Hard Tape | Mike Webster | Turun ≤1% hari ini dan minggu ini; julat tutup harian & mingguan >60%; nisbah volum naik/turun 50 hari >1.1; dalam 15% dari high 52 minggu; RS 3M & 6M >70, 12M >50 | Perlu pangkat RS; tiada keluar | sama seperti K281 |

---

# Tambahan Pusingan 2 (14 Okt 2026, 18:36–19:10)

Sumber: halaman indeks sahaja (had carian habis) — swingtradebot, tradingsetupsreview, oxfordstrat, luxalgo, Traderpedia, PDF Street Smarts / Landry 10 Best / Pristine, flipbook Farley, fintwits scans, Deepvue, sofus-nl, ProRealCode, Marketcalls, Zerodha Varsity.
Digugurkan sebagai varian: High Trend Intensity, Small Stock Momo, Biggest Gainers (Qullamaggie), Velocity (Ben), RSNHBP (Ray), Mo Scan & Darvas Scan (Vo), Swing Trading List (Webster), RSI Reversion (sofus), HHV Breakout, Trend Pullback, EMA 9/21 Crossover, ADX Trend, MA Stack, Multi-Period Strength, Power Earnings Gap (sofus), Honest Guide screener (≈ Donchian), High Percentage Trading System (≈ Williams volatility breakout), Key Buy (≈ K197), TS Cooper's System (≈ K42), IDNR4-ATR (≈ K167), Accelerating Momentum (≈ K52), M2B (≈ K153), Floor Trader 9/18 (≈ M18), Resting near 52-week high (≈ K37), Modified Sharpe (≈ K136), Freebars on Keltner (≈ M30), Kumo Break (≈ M49), Supertrend high-low (≈ K56). Luar skop (fundamental): Recession Proof, Ben Focus, MAGNA 53+, Caruso Sales 40/40.
Tidak dapat dibaca: Chartink, TradingQnA (kebenaran tamat masa), Street Smarts bab 18–25, pustaka AmiBroker.

## Kumpulan A — sedia untuk backtest OHLCV

| K | Kaedah | Pencipta | Masuk | Keluar | ≈ | Sumber |
|---|---|---|---|---|---|---|
| K284 | Popgun | Jeffrey Kennedy | Bar dalam, kemudian bar luar bullish; beli pada tutup bar luar | *(andaian)* henti low bar luar; keluar di rintangan berhampiran | | tradingsetupsreview.com (popgun-bar-pattern-trading-setup) |
| K285 | Yum-Yum Continuation | Hill, Pruitt & Hill | Aliran naik (EMA20); bar julat lebar (> purata julat 10 bar) tembus swing high tertinggi, tutup dekat high dan atas buka; beli tembus high-nya dalam 1–3 bar | Henti low bar itu; ekor bawah bar bullish | K53 | tradingsetupsreview.com (yum-yum) |
| K286 | 3-Bar Momentum Pattern | J.R. Hill (1977) | 3 bar dengan TR naik, tutup naik, low naik, semua tutup > buka, pecutan kenaikan tutup & high; penapis high > high N bar; beli buka esok | Henti 1 tik bawah low corak; keluar masa | | oxfordstrat.com (3-bar-momentum-pattern) |
| K287 | Three-Bar Inside Bar | Johnan Prathap (S&C 2012) | Tutup lebih tinggi, kemudian bar dalam, kemudian tutup lebih tinggi; beli pada tutup bar ke-3 | Tidak dinyatakan | K76 | tradingsetupsreview.com (three-bar-inside-bar-pattern) |
| K288 | Improved Three-Bar Pullback | Lee Leibfarth | TRIX(9) > isyarat(3), kemudian 3 tutup menurun; beli henti atas bar terakhir | Tidak dinyatakan | | tradingsetupsreview.com (improved-three-bar-pullback-pattern) |
| K289 | Natural Number Method | George Kleinman | Tutup atas WMA180, kemudian harga melebihi high bar persediaan; beli henti di nombor bulat seterusnya | Henti di nombor bulat di bawah; ekor nombor bulat; batal jika tutup bawah WMA180 | | tradingsetupsreview.com (natural-number-trading-method) |
| K290 | 3-Step Pullback | Richard Deutsch | Tutup atas Keltner atas (EMA15, 2×ATR15); undur 3–15 bar sebanyak 20–80% lebar saluran; beli pada bar momentum naik atau pin bar | Henti ≥2.5×ATR; sasaran 1:1 | | tradingsetupsreview.com (3-step-pullback-trading-method) |
| K291 | Acceleration Bands Breakout | Price Headley | 2 tutup berturut atas band atas; Atas = SMA20(H) × (1 + 4(H−L)/(H+L)) | Tutup kembali dalam band; henti tidak dinyatakan | K112 | luxalgo.com/library/concept/acceleration-bands.md |
| K292 | Wise Man 3 | Bill Williams | Beli henti atas fraktal naik yang berada atas garis "gigi" Alligator | Ekor bawah low atau Alligator | | luxalgo.com/library/concept/bill-williams-profitunity.md |
| K293 | Long Equity Trading System | Bruce Babcock | Mom(11) naik, buka > (H+L+C)/3 semalam; beli henti di tutup semalam + TR | Keluar pada buka pertama yang untung | | oxfordstrat.com (long-equity-trading-system) |
| K294 | Conquistador MTF | Babcock / Freeburg | Tutup > SMA10, SMA10 > nilainya 10 hari lalu, tutup > tutup 40 hari lalu; beli pada tutup | Keluar masa; henti ATR | | oxfordstrat.com (multiple-time-frames-1) |
| K295 | RSI-2 | Connors & Alvarez | Tutup > SMA200, RSI(2) < 10 | Tutup > SMA5; tiada henti | K165 / K260 | luxalgo.com/library/concept/rsi-2.md |
| K296 | ConnorsRSI | Connors Research | Atas SMA200, CRSI < 10 (tranche ke-2 < 5) | Keluar apabila CRSI kembali sekitar 50 | K165 | luxalgo.com/library/concept/connors-rsi.md |
| K297 | Trend Bar Failure | Galen Woods | EMA20 naik; low bar aliran turun (badan > 50% julat) ditembus; beli henti di high-nya, sah 1 bar | Tidak dinyatakan | | tradingsetupsreview.com (simple-effective-price-action-trading-setup) |
| K298 | Outside Bar Failure | Galen Woods | SMA20 naik; bar luar bearish, low-nya ditembus; beli henti atas bar bullish berikutnya | Batal jika high bar < low bar luar; tiada henti | K176 | tradingsetupsreview.com (swing-trading-outside-bar-failure) |
| K299 | Consecutive Down Days | Galen Woods | ≥4 bar tutup bawah buka, swing low terakhir tidak pecah; beli 1 tik atas bar bullish berikutnya | Tidak dinyatakan | | tradingsetupsreview.com (trading-consecutive-updown-days-lower-risk) |
| K300 | MACD + Inside Bar | Sunil Mangwani | MACD > 0; beli 1 tik atas bar dalam | Tidak dinyatakan (tetapan MACD tidak diberi) | M70 | tradingsetupsreview.com (trading-macd-inside-bar) |
| K301 | Gap Pattern Type A | Dahlquist & Bauer | Low > high semalam dan high > high N bar; beli buka esok | Henti 1 tik bawah jurang; keluar masa | K40 | oxfordstrat.com (gap-pattern) |
| K302 | Trend Pivot / Second-Entry Pullback | Dave Landry | High baharu, undur 2–5 bar, rali pertama gagal atas high sebelumnya; beli henti atas high rali palsu | Tidak dinyatakan | K153 | pdfcoffee.com (Landry 10 Best, bab 5) |
| K303 | Spike & Ledge | Connors & Raschke (Street Smarts bab 14) | Aliran naik; hari lonjakan menduga low dan tutup dekat high; para 4–10 bar yang kekal atas low lonjakan; beli atas tutup tertinggi para | Henti bawah para, ke pulang modal, kemudian ekor | | thechartist.com.au (Street Smarts PDF) ; traderpedia.it/wiki/index.php/Spike_&_Ledge |
| K304 | Range Leader | Charlie F. Wright (Trading as a Business) | Julat > julat semalam dan titik tengah > high semalam; beli buka esok (langkau jika buka bawah titik tengah) | Henti low bar (atau titik tengah); pulang modal secepat mungkin; sasaran 2× risiko | | traderpedia.it/wiki/index.php/Range_leader |
| K305 | HOLP | John Carter (Mastering the Trade) | Aliran naik, pembetulan 20 bar; beli pada tutup pertama atas high bar low terendah | Henti low pembetulan; ekor low 2 bar lalu | | traderpedia.it/wiki/index.php/HOLP |
| K306 | 3L-R | Michael Harris | L[1]<L[2]<L[3] dan H>H[3]; beli buka esok | Henti/sasaran % (nilai tidak diberi) | | traderpedia.it/wiki/index.php/3L-R |
| K307 | Gap-2H | Michael Harris | L[1]>H[2], L>L[1], L<H[1], H>H[1]; beli buka esok | Tidak dinyatakan | | traderpedia.it/wiki/index.php/Gap-2H |
| K308 | Gamma Pattern | Michael Harris | C[2]>C[1]>C[0]>C[3]; beli buka esok | Henti/sasaran % (nilai tidak diberi) | | traderpedia.it/wiki/index.php/Gamma_Pattern |
| K309 | N-V Pattern | Michael Harris | C>C[2]>C[3]>C[1]; beli buka esok | Henti/sasaran % (tanda formula di halaman nampak terbalik) | | traderpedia.it/wiki/index.php/N-V_Pattern |
| K310 | Obb Pattern | Michael Harris | H>H[1]>H[2]>L, L>L[2]>L[1]; beli pada tutup | Tidak dinyatakan | | traderpedia.it/wiki/index.php/Obb_Pattern |
| K311 | Shark-32 | S&C Okt 1998 | Dua bar dalam, titik tengah bar tengah ≥28% dari kedua-dua hujung bar luar; beli pada tutup jika C > H[3] | Keluar tutup bawah low mengekor; keluar masa 78 bar | K149 (tanpa ADX) | traderpedia.it/wiki/index.php/TS_Shark_32 |
| K312 | Williams 19 | Larry Williams | PH = 2×(H+L+C)/3 − L; beli henti di PH tertinggi 16 bar + 1 mata | Tidak dinyatakan | | traderpedia.it/wiki/index.php/TS_Williams_19 |
| K313 | FVE Breakout | Markos Katsanos (Detecting Breakouts) | FVE(22) silang atas −5, cerun FVE 35 bar > 0, cerun harga 35 bar < 0; beli buka esok | Keluar apabila cerun FVE 25 bar < 0 atau selepas 70 hari | | traderpedia.it/wiki/index.php/TS_Finite_Volume_Element_(FVE)_System |
| K314 | RS Phase | Deepvue | Garis RS atas EMA21nya | Keluar apabila garis RS tutup bawah EMA21 (perlu index_benchmark) | I03 | deepvue.com/indicators/relative-strength-stocks/ |
| K315 | Volume-Weighted Trend | sofus-nl | Atas VWAP 21 hari yang naik; volum naik > 1.5× volum turun dalam 21 bar; > SMA50; pangkat RS > 70 (dalam universe) | Henti 1.5×ATR atau bawah VWAP; 2 tutup bawah VWAP = keluar | K103 | raw.githubusercontent.com/sofus-nl/swing-trading-strategies/main/strategies/17-volume-weighted-trend.md |
| K316 | Triple Momentum (diubah suai) | Gerald Appel (2005); ubah suai Rajandran R | ROC5+ROC15+ROC25 silang atas +4% | Silang bawah 0 (asal Appel: bawah 4%); tiada henti | K129 KST | marketcalls.in/amibroker/modified-triple-momentum-strategy-amibroker-afl-code.html |
| K317 | ALMA Long-Only | Rajandran R | ALMA(5, sigma 2, offset 0.85) naik DAN tutup > EMA20 DAN RSI14 > 50 | Keluar apabila ALMA turun; tiada henti | | marketcalls.in/amibroker/alma-long-only-trading-system-amibroker-afl-code.html |
| K318 | 5-EMA High-Low (mingguan) | Rajandran R | Mingguan: tutup silang atas EMA5 bagi high | Tutup silang bawah EMA5 bagi low | K93 | marketcalls.in/afl-code/simple-afl-code-for-5-emahigh-low.html |
| K319 | EMA 13/34 Crossover High-Low Breakout | Rajandran R | Selepas silang EMA13/34 bullish, beli tembus high bar silang itu | Keluar apabila tembus low bar silang bearish | | marketcalls.in/amibroker/ema-crossover-high-low-breakout-strategy-amibroker-afl-code.html |
| K320 | SDA2 Trend | Rajandran R (varian AFBI Channel) | D = WMA3((H+L)/2 + (O−C)); beli apabila tutup silang atas D + SD(D,7) + ATR2/1.5 | Tutup silang bawah D − SD(D,7) − ATR2 | K112 | marketcalls.in/afl-code/sda2-trend-trading-system-afl-code.html |
| K321 | Pivot Reversal | TradingView (strategi terbina) | Beli henti 1 tik atas pivot high terkini (4 bar kiri / 2 kanan) | Tidak dinyatakan (versi dua arah berbalik di pivot low) | K245 | marketcalls.in/amibroker/pivot-reversal-strategy-tradingview-pinescript-to-amibroker-afl-conversion.html |
| K322 | Williams Alligator | Bill Williams (melalui Zerodha Varsity) | Tutup > SMA5 > SMA8 > SMA13 (dianjak), garis berpisah | Tidak dinyatakan; elak apabila garis berselirat | K92 | zerodha.com/varsity/chapter/supplementary-notes-1/ |
| K323 | Bullish Marubozu | Zerodha Varsity (Karthik Rangappa) | Bar naik berbadan penuh dengan julat 1–10%; beli dekat tutup atau hari naik esok | Henti low bar | K62 | zerodha.com/varsity/chapter/single-candlestick-patterns-part-1/ |
| K324 | Going Bullish (Passage Haussier) | Doctrading (ProRealCode) | Dalam 3 bar terakhir: tutup silang atas EMA30, EMA30 naik, EMA30 > EMA150, RSI14 silang 50, MACD silang 0 (asal H4; komen kata harian berfungsi) | Tidak dinyatakan | M02 | prorealcode.com/prorealtime-market-screeners/screener-going-bullish/ |
| K325 | W+D Value Zone | Per (ProRealCode) | Mingguan: EMA10 > EMA50 (5 bar lalu) dan tutup ≤ EMA20; harian: MACD(7,14,3) ≥ EMA3nya | Tidak dinyatakan | K44 | prorealcode.com/prorealtime-market-screeners/trading-trend-wd-screening-zone-entries/ |
| K326 | Daily Kijun Throwback dalam aliran naik mingguan | tasciccac (ProRealCode) | Mingguan: SpanA > SpanB, 0 < (Tenkan−Kijun)/(SpanA−SpanB) < 100, tutup > High[26]; harian: Tenkan > Kijun dan tutup silang atas Kijun | Tidak dinyatakan | M49 | prorealcode.com/prorealtime-market-screeners/daily-throwback-kijun-weekly-uptrend-ichimoku-kinko-hyo/ |
| K327 | 50-Week MA Touch | odin (kod M. Schöppl) | Mingguan: MA50 > MA100 > MA200; low < MA50 dalam 4 bar terakhir; bar naik tutup > MA50 | Tidak dinyatakan | K68 | prorealcode.com/prorealtime-market-screeners/50-weeks-touch-ema-or-sma-with-long-term-up-trend/ |
| K328 | SQN Trend + RSI2 Oversold | odin (ProRealCode) | SQN Van Tharp mingguan (100–200 bar) > 2.5 DAN RSI2 < 10; harga > 5; varian: tutup > SMA50 naik | Tidak dinyatakan | K105 | prorealcode.com/prorealtime-market-screeners/solid-trendfollowing-stocks-with-oversold-condition/ |
| K329 | Ordered Trend-Following | Vivien René (ProRealCode) | Tutup > Supertrend(3,10); kecerunan harga sepanjang larian hijau > 3%/bar; pangkat ikut kecerunan | Tidak dinyatakan | K56 / I06 | prorealcode.com/prorealtime-market-screeners/ordered-trend-following-stocks-screener/ |
| K330 | Volatility Compression Breakout | jacquesgermain (ProRealCode) | High > tengah Keltner20 + 1.5×ATR14 + SD20 DAN tutup silang atas EMA50 | Tidak dinyatakan | K112 | prorealcode.com/prorealtime-market-screeners/volatility-compression-breakout-screener/ |
| K331 | Market Cycle Strategy | Thibauld Robin (ProRealCode) | Harian, beli sahaja: Stoch(13,8) > Stoch(21,13) > Stoch(34,21); (S1−S3)/S3 > 10%; (kedua-dua naik ATAU volum/purata21 > 1.2) | Keluar apabila susunan hilang atau S1 berpusing turun; tiada henti | | prorealcode.com/prorealtime-trading-strategies/market-cycle-strategy/ |

## Kumpulan B — pembalikan / kontra-aliran

| K | Kaedah | Pencipta | Masuk | Keluar | Sumber |
|---|---|---|---|---|---|
| K332 | Wise Man 1 | Bill Williams | Bar low lebih rendah, tutup di separuh atas, bawah Alligator, AO menurun; beli henti atas high-nya | Pecah low WM1 = batal; ekor bawah low atau Alligator | luxalgo.com/library/concept/bill-williams-profitunity.md |
| K333 | TD Sequential Buy | Tom DeMark | 9 tutup < tutup[4], ujian persilangan, kemudian kiraan 13 tutup < low[2]; masuk apabila tutup > tutup[4] | Henti = low corak − (tutup masuk − low); keluar pada persediaan baharu | oxfordstrat.com (td-sequential-1) |
| K334 | Bottom Reversal | Wyckoff / Crabel (Oxfordstrat) | Dalam 5 bar selepas pecah pivot permintaan (saiz 5): tutup atas 2 tutup sebelum, pivot, buka dan titik tengah bar; julat > julat sebelumnya; beli buka esok | Henti 1 tik bawah low bar persediaan; sasaran 2R | oxfordstrat.com (reversal-patterns-1, -2) |
| K335 | Gatekeeper (cerminan beli) | Dave Landry | Low baharu 2 bulan, rali tajam, undur 61.8–78.6% dalam ~10–11 hari; beli di high bar itu *(andaian: cerminan; teks kata belian "diterbalikkan")* | Henti 0.25–1.00 melepasi paras 78.6%; untung separa di kawasan high/low lama | pdfcoffee.com (Landry 10 Best, bab 11) |
| K336 | Down-5C | Michael Harris | 5 tutup menurun berturut; beli pada tutup | Tidak dinyatakan (≈ Connors 3-day low yang ditolak) | traderpedia.it/wiki/index.php/Down-5C |
| K337 | V4-C | Tidak dinamakan | Low menurun A>B>C; bar D bullish dengan low atas low B dan C, high atas high C; beli atas high C | Henti bawah low corak | traderpedia.it/wiki/index.php/V4-C |
| K338 | Pin bar dalam bar luar | Tidak dinamakan ("Un setup controtrend") | Aliran; pin bar dalam dengan sumbu bawah ≥7× badan; beli di high pin | Henti bawah low bar luar; sasaran high bar luar; R:R ≥1:3 | traderpedia.it/wiki/index.php/Un_setup_controtrend |
| K339 | 2B Bottom | Victor Sperandeo | Aliran turun; low baharu selepas rali gagal, tiada susulan; beli apabila bar kemudian melebihi high bar pecah | Tidak dinyatakan (≈ K94 / K172) | traderpedia.it/wiki/index.php/2B_Bottom |
| K340 | Conner 19 | Michael Conner | 4 tutup berturut ≤ tutup sebelumnya; beli henti di high terendah 4 bar terakhir | Henti low bar masuk − 2 mata; henti wang $1000 | traderpedia.it/wiki/index.php/TS_Conner_19 |
| K341 | Low or High 3 | Tidak dinamakan | L < low terendah 3 bar yang berakhir 3 bar lalu; beli henti di high 3 bar | Tidak dinyatakan | traderpedia.it/wiki/index.php/TS_Low_or_High_3 |
| K342 | Finger Finder (bull) | Alan Farley (Master Swing Trader bab 10) | Hammer/doji julat atas purata, tutup ≈ buka, selepas kejatuhan beberapa sesi, sumbu menembusi Bollinger bawah; beli di dasar doji | Henti tepat di luar julat bar | fliphtml5.com/vvba/eeop/The_Master_Swing_Trader/251 |
| K343 | Triple RSI Divergence | Andrew Cardwell (melalui sofus-nl) | 3 low harga menurun lawan 3 low RSI14 menaik; dekat sokongan; volum menurun; lilin bullish; RSI > 30 | Henti bawah low corak; 50% keluar di rintangan pertama, baki pada 2×ATR; ekor 5% (≈ M03 / M05) | raw.githubusercontent.com/sofus-nl/swing-trading-strategies/main/strategies/10-triple-rsi-divergence.md |

## Kumpulan C — separa

| K | Kaedah | Pencipta | Ringkasan | Apa yang kurang | Sumber |
|---|---|---|---|---|---|
| K344 | Gimmee Bar | Joe Ross | Dalam julat mendatar, bar sentuh BB bawah dan tutup atas buka; beli 1 tik atas high | Tetapan BB tidak diberi (luxalgo guna 20/2); henti tidak dinyatakan; pembalikan purata dalam julat | tradingsetupsreview.com/gimmee-bar/ |
| K345 | 1-2-3 Low / 1-2-3 Reversal | Victor Sperandeo; Joe Ross | Garis trend turun pecah, low lebih tinggi (titik 2), beli tembus titik 3 (atau atas titik 2); henti bawah titik 1/3 | Takrif pivot dan garis trend tidak diberi; ≈ K192 | traderpedia.it/wiki/index.php/123_Low ; luxalgo.com/library/concept/1-2-3-reversal.md |
| K346 | Single Penetration | Joe DiNapoli | Undur pertama ke 38.2% tujahan baharu dalam aliran naik; henti melepasi 61.8%; sasaran COP/XOP | Penapis aliran DMA tidak diberi | luxalgo.com/library/concept/dinapoli-levels.md |
| K347 | Calm After Storm | swingtradebot | Bar julat lebar, kemudian bar mengecut; beli atas high bar mengecut; henti low bar itu | Tiada ambang; ≈ M11 | swingtradebot.com/events/59 |
| K348 | VSA Test Bar | Tom Williams | Bar sempit volum rendah tutup tengah–atas julat ke dalam bekalan lama; beli bar naik berikutnya yang tutup kukuh dengan volum naik; henti bawah low bar ujian | Tiada ambang | luxalgo.com/library/concept/vsa-test-bar.md |
| K349 | Three Little Indians (cerminan bull) | Connors & Raschke | Tiga lembah; beli pada pembalikan dari lembah ke-3 | Subjektif; paras henti tidak dinyatakan | thechartist.com.au (Street Smarts PDF) |
| K350 | Triangle Coil | Alan Farley (bab 9) | Segi tiga undur ≤50%, 3 sentuhan setiap garis, NR7 dekat garis tengah; beli atas julat kesesakan 5 hari; henti bawah low NR7 pertama | Garis trend perlu dikod; ≈ M11 | fliphtml5.com/vvba/eeop/The_Master_Swing_Trader/242 |
| K351 | Power Spike (long) | Alan Farley (bab 12) | Tapak panjang, kemudian bar jurang lebar atas tapak dengan volum sangat tinggi tutup atas titik tengah; beli apabila undur merampas semula 62% atau menutup jurang | Henti hanya dari contoh; ≈ K40 / M22 | fliphtml5.com/vvba/eeop/The_Master_Swing_Trader/285 |
| K352 | Momentum scan | Qullamaggie (fintwits) | Tutup > high semalam; ADR(1)/ADR(20) > 1; purata volum 50 hari > 200K; nilai dagangan > $2J; susun ikut ROC | Tiada keluar; ≈ K53 | fintwits-most-popular-stock-market-scans.onrender.com (Kristjan Kullamägi → Momentum) |
| K353 | Combo ($0.90 breakout ATAU hari 4%) | Stockbee (fintwits) | Tutup − buka > $0.90 ATAU (naik ≥4%, tutup semalam/tutup 2 hari lalu ≤1.02, volum > semalam, tutup di 30% atas julat) | Satu operator hilang di halaman; tiada keluar; ≈ M32 | fintwits (Stockbee → Combo) |
| K354 | Ants scan (Stockbee) | Pradeep Bonde | Tutup > 4; volum minimum 3 hari > 100K; ti > 1.04; perubahan hari ini dalam ±1% | Imbasan sahaja; "ti" tidak ditakrif (mungkin SMA7/SMA65); berbeza daripada K61 | fintwits (Stockbee → Ants) |
| K355 | Strength | Blake Davis | Tutup > 7; RS IBD > 70; RS industri > 50; tutup di 30% atas julat; hari naik | Imbasan sahaja; perlu pangkat RS & industri | fintwits (Blake Davis → Strength) |
| K356 | 9 Million EP | Pradeep Bonde | Hari pertama dengan ≥9 juta saham selepas peristiwa besar; masuk dekat pecahan; henti bawah low hari itu | Perlu sejarah volum penuh dan "peristiwa"; ≈ M22 / K81 | deepvue.com/screener/pradeep-bonde-screens/ |
| K357 | Bull Snort | Oliver Kell | Naik >3% dengan volum ≥3× biasa; senaraikan, kemudian dagang di EMA10/20 | Pencetus tidak mekanikal; ≈ K62 | deepvue.com/screener/stock-screener-by-trader/ |
| K358 | Consolidation Pivot Breakout (versi angka) | Deepvue | Naik >15% dalam 4 minggu atau >25% dalam 8 minggu; dalam 15% dari high; > EMA10/21; EMA10 > EMA21; EMA21 naik 5 hari; ADR 5 hari < 3%; julat hari ini < 2%; volum 5 hari < 80% purata 50 hari | Masuk pada pusingan-U intrahari; ≈ K182 | deepvue.com/screener/stocks-breaking-out/ |
| K359 | Traditional Basing Breakout | Deepvue | > $12.50; nilai pasaran > $1B; naik >15% dalam 4 minggu; dalam 15% dari high 52 minggu; RS > 85; > EMA10/21; ADR 5 hari < 3%; volum 5 hari < 80% purata 50 hari | Perlu EPS / nilai pasaran; tiada keluar; ≈ K124 | deepvue.com/screener/stocks-breaking-out/ |
| K360 | High Relative Volume | Deepvue | Naik dari buka, dalam 15 kumpulan industri teratas; beli atas high hari volum dalam 1–2 sesi berikut; henti low hari volum | Perlu pangkat kumpulan industri; ≈ K62 | deepvue.com/screener/stock-screener-by-strategy/technical-stock-screener/ |
| K361 | ROAR | Alan Hull (Active Investing) | Carta mingguan, saham blue-chip; ROAR (kenaikan harga tahunan ÷ harga × 100) > 10%; keluar apabila ROAR < had | Formula tepat tiada di halaman; ≈ K39 | marketcalls.in/amibroker/hull-roar-rate-annual-return-amibroker-afl-code.html |
| K362 | Coppock (versi harian) | IncredibleCharts (menurut halaman) | WMA210 bagi (ROC294 + ROC231) berpusing naik atas 0 *(andaian)* | Keluar tidak dinyatakan; ≈ K129 | marketcalls.in/amibroker/coppock-nifty-and-the-afl-code.html |
| K363 | Explosive Stocks | Doctrading (ProRealCode) | Volum > 2.5× purata 20; badan naik > 5× purata badan; tutup > BB20 atas; tutup > SMA150 naik; purata lebar BB 15 < 0.8× purata 50; masuk pada pecah garis trend dilukis tangan; henti low ayun terakhir | Garis trend manual; ≈ M32 / M04 | prorealcode.com/prorealtime-market-screeners/explosive-stocks-screener/ |
| K364 | BUY Stock | Doctrading (ProRealCode) | SMA50 > SMA200, tutup > SMA50, bar naik, volum > 2× purata 10 dan > setiap 3 bar sebelum, Force Index > 10K, RSI70 > 51 | Pecah rintangan manual; tiada keluar; ≈ K62 | prorealcode.com/prorealtime-market-screeners/buy-stock-screener/ |
| K365 | Bullish Swing Setup | Nicolas (ProRealCode) | SMA10 > SMA20 untuk semua 20 bar terakhir; tutup > SMA20; tutup < SMA10; tutup ≥ 0.85× high 20 bar | Imbasan sahaja; ≈ M18 | prorealcode.com/prorealtime-market-screeners/bullish-swing-setup/ |
| K366 | Smoothed Bollinger% Daily | ALE (ProRealCode) | Tutup > MA220 DAN %b(17) bagi TEMA8 penutup Heikin-Ashi < 30; ekor 9×ATR200; henti 5%; sasaran 10%; keluar selepas 16 bar jika rugi | Kod ada pepijat nama pemboleh ubah (menurut komen) | prorealcode.com/prorealtime-trading-strategies/smoothed-bollinger-strategy-daily/ |

## Peraturan keluar tambahan

| X | Peraturan | Pencipta | Ringkasan | Sumber |
|---|---|---|---|---|
| X09 | Relative Measured Extension (RME) | Deepvue | Regangan dari MA diskala −100 hingga +100 terhadap julatnya sendiri (swing: 50/100 bar, SMA10–20); dekat −70 = zon lantun, +70 = potong/jual. Formula tidak diberi (≈ X02) | deepvue.com/indicators/relative-measured-extension/ |

---

# Tambahan Pusingan 3 (14 Okt 2026, 19:15–19:26)

Sumber: indeks konsep LuxAlgo (llms-full.txt), halaman sistem Traderpedia, indeks Oxfordstrat (/resources/). Nota: Oxfordstrat menguji semua strategi pada 42 niaga hadapan; henti 6×ATR20 ialah henti generik laman itu, bukan peraturan pencipta.

## Kumpulan A — sedia untuk backtest OHLCV

| K | Kaedah | Pencipta | Masuk | Keluar | ≈ | Sumber |
|---|---|---|---|---|---|---|
| K367 | Pretty Good Oscillator | Mark Johnson | PGO = (C − SMA(C,n)) / EMA(TR,n) naik atas +3.0 (n = 89 versi jangka panjang; 14 atau 21 juga lazim) | PGO kembali melalui 0; tiada henti | | luxalgo.com/library/concept/pretty-good-oscillator.md |
| K368 | Elder Ray Pullback | Alexander Elder | EMA13 naik dan Bear Power (low − EMA13) negatif, berhenti mendalam dan berpusing naik | Tidak dinyatakan | K69 / K44 | luxalgo.com/library/concept/elder-ray.md |
| K369 | Traders Dynamic Index | Dean Malone | Garis harga (2) silang atas garis isyarat (7) pada RSI(13); "biasanya" kedua-dua garis atas 50 | Tidak dinyatakan | | luxalgo.com/library/concept/traders-dynamic-index.md |
| K370 | Random Walk Index Cross | Michael Poulos | RWI high silang atas RWI low; abaikan silang di bawah 1; tempoh 8–64 bar | Tidak dinyatakan | K113 Aroon | luxalgo.com/library/concept/random-walk-index.md |
| K371 | Double Bollinger Zones | Kathy Lien | Tutup berturut di antara band atas 1-SD dan 2-SD (20 tempoh) | *(andaian)* tutup kembali ke zon neutral | M31 | luxalgo.com/library/concept/double-bollinger-zones.md |
| K372 | Upside Tasuki Gap | Tradisi lilin (Steve Nison) | Lilin putih, lilin putih jurang naik, lilin hitam buka dalam badan kedua; masuk selepas lilin ketiga mengekalkan jurang | Henti melepasi tepi jauh jurang | K67 | luxalgo.com/library/concept/upside-downside-tasuki-gap.md |
| K373 | Moving Average with Support/Resistance | Dennis Tilley | Tutup silang atas SMA10 sementara tutup < R/1.08, atau tutup silang atas R (R = high bar beli terakhir); beli buka esok | Tutup silang bawah SMA10 sementara tutup > S×1.08, atau bawah S (S = low bar jual terakhir) | K86 | traderpedia.it/wiki/index.php/TS_Moving_average_with_resistance_and_support_system |
| K374 | TrueContrarian | Tidak dinamakan | Tutup silang atas SMA10 dan >10 silangan SMA10 dalam 40 bar terakhir; beli buka esok | Tutup silang bawah SMA10 | M08 | traderpedia.it/wiki/index.php/TS_TrueContrarian |
| K375 | Long Trends | Tidak dinamakan | High tertinggi 21 hari silang atas SMA21nya sementara low terendah 21 hari > SMA-nya; beli pada tutup | Sasaran/henti ±2×(high − low 22 hari) | K86 | traderpedia.it/wiki/index.php/TS_Long_Trends |
| K376 | DiNapoli 5 | Tidak dinamakan | SMA3 > SMA7 > SMA25 sekarang tetapi tidak tersusun pada lag [3]/[5]; beli had di SMA3[3] | Tidak dinyatakan | K92 | traderpedia.it/wiki/index.php/TS_DiNapoli_5 |
| K377 | MACD Momentum | Barbara Star (S&C Feb 1994) | Purata 3 bar bagi momentum 10 bar (MACD − isyarat) > 0 dan (MACD − isyarat) silang atas 0; beli pada tutup | Penapis itu silang bawah 0 | M02 / I13 | traderpedia.it/wiki/index.php/TS_Macd_Momentum_System |
| K378 | TRIX System | S&C Jun 1997 ("Playing TRIX") | TRIX(ln tutup, 3) silang atas 0 atau atas LinReg(TRIX, 8); beli pada tutup | Silang bertentangan | | traderpedia.it/wiki/index.php/TS_TRIX_System_S%26C |
| K379 | Doubly Adaptive Profit Targets | Chuck LeBeau | Tutup > SMA50, buka esok > high hari ini, ADX14 naik; beli had di high itu | Sasaran/henti entry ± ATR20×4 (×2 jika ADX tidak naik); keluar tutup < SMA50 | K40 | traderpedia.it/wiki/index.php/TS_Doubly_Adaptive_Profit_Targets |
| K380 | Dow Theory – Multiple Time Frames | Charles Dow (Oxfordstrat) | Aliran utama high/low menaik; undur sekunder; beli henti atas high-lebih-rendah sekunder terendah | Henti bawah pivot low-lebih-tinggi sekunder | K192 | oxfordstrat.com/trading-strategies/dow-theory-trend-2/ |
| K381 | Heikin-Ashi Trend | Oxfordstrat R&D | Bar HA sebelumnya bullish dengan bayang bawah kecil, tutup > tutup[n]; beli buka | Bar HA bearish pertama → jual buka | | oxfordstrat.com/trading-strategies/heikin-ashi-2/ |
| K382 | Doji Pattern – Trend | Oxfordstrat R&D | Bar sebelumnya doji (badan/julat ≤0.05) dan tutup > tutup[n]; beli henti 1 tik atas high doji | Keluar masa 20 hari; henti cepat bawah min(low masuk, low sebelum) | M11 / K76 | oxfordstrat.com/trading-strategies/doji-trend-1/ |
| K383 | FRAMA Bands | John Ehlers (Oxfordstrat) | Tutup > FRAMA((H+L)/2) + k×ATR; beli buka | Tutup < FRAMA − 0.5k×ATR | K114 KAMA | oxfordstrat.com/trading-strategies/fractal-adaptive-moving-average/ |

## Kumpulan B — pembalikan / kontra-aliran

| K | Kaedah | Pencipta | Masuk | Keluar | Sumber |
|---|---|---|---|---|---|
| K384 | RSI Failure Swing (dasar) | J. Welles Wilder | RSI14 jatuh bawah 30, lantun ke puncak sementara ("titik gagal"), undur, kemudian silang atas puncak itu | Henti bawah low ayun harga sepadan | luxalgo.com/library/concept/rsi-failure-swing.md |
| K385 | Pipe Bottom | Tom Bulkowski | Bar mingguan selepas kejatuhan: dua bar bersebelahan dengan lonjakan turun luar biasa panjang dan sama dalam; masuk pada tutup atas high kedua-dua bar | Henti low lonjakan ("luar biasa panjang" tidak diukur — separa) | luxalgo.com/library/concept/rare-reversal-patterns.md |
| K386 | Island Bottom | Edwards & Magee | Jurang turun, terhenti, kemudian jurang naik; masuk pada atau selepas jurang kedua | Henti bawah low pulau | luxalgo.com/library/concept/island-reversal.md |
| K387 | Three Outside Up / Three Inside Up | Nama oleh Gregory Morris | Corak menelan (Outside) atau harami (Inside), diikuti lilin ketiga yang mengesahkan; masuk pada tutup lilin ketiga | Outside: henti bawah low lilin menelan; Inside: bawah low lilin pertama | luxalgo.com/library/concept/three-outside-up-down.md ; …/three-inside-up-down.md |
| K388 | Sideways | Tidak dinamakan (Traderpedia) | LinReg(C,4) silang atas purata (high tertinggi/low terendah 3 hari); beli pada tutup (kod kabur) | Sasaran entry + 2×julat3; henti entry − 2×julat3 | traderpedia.it/wiki/index.php/TS_Sideways |
| K389 | Turbo MA | Tidak dinamakan (Traderpedia) | Tutup < TurboMA(9) dan TurboMA turun; beli henti di high 2 bar | Tutup < TurboMA; henti entry×0.96 (separa: AvgPrice tidak ditakrif) | traderpedia.it/wiki/index.php/TS_Volume-Weighted_Average |
| K390 | Dow Theory – Trend | Charles Dow (Oxfordstrat) | Selepas low dan high menurun, beli henti 1 tik atas pivot high-lebih-rendah terendah | Henti entry − 6×ATR20; keluar masa n hari (≈ K345) | oxfordstrat.com/trading-strategies/dow-theory-trend/ |

## Kumpulan C — separa

| K | Kaedah | Pencipta | Ringkasan | Apa yang kurang | Sumber |
|---|---|---|---|---|---|
| K391 | Wise Man 2 (tambah kedudukan) | Bill Williams | Selepas masuk, tunggu 3 bar Awesome Oscillator naik berturut; beli tembus high bar ketiga; ekor bawah low atau Alligator | Hanya untuk tambah kedudukan sedia ada (piramid), bukan masuk baharu | luxalgo.com/library/concept/bill-williams-profitunity.md |
| K392 | Zero-Line Reject | Ken Wood (Woodies CCI) | Aliran = CCI14 ≥6 bar atas 0; CCI undur ke arah 0, tidak silang "bermakna", lalu bengkok naik | "Bermakna" tidak diukur; tiada keluar; ≈ K156 / K131 | luxalgo.com/library/concept/woodies-cci-conventions.md |
| K393 | Force Index Dip | Alexander Elder | Dalam aliran naik, Force Index 2 tempoh jatuh bawah 0; masuk apabila berpusing naik | Penapis aliran tidak ditakrif; tiada keluar; ≈ K44 | luxalgo.com/library/concept/force-index.md |
| K394 | Double-Bottom Base | William O'Neil | Tapak bentuk W ≥7 minggu; low kedua tembus bawah low pertama; beli tembus puncak tengah + sedikit dengan volum jauh atas purata | Henti % tetap (nilai tidak diberi); ≈ K124 / K82 | luxalgo.com/library/concept/double-bottom-base.md |
| K395 | Measured Move Up | Tom Bulkowski | Beli pusingan naik pada low ayun yang menamatkan pembetulan; henti low pembetulan; sasaran kaki kedua = kaki pertama | Perlu pengesanan ayunan | luxalgo.com/library/concept/measured-move-up-down.md |
| K396 | Confluence | Dale Legan (senarai Omega 1998) | Confluence (Harmonic 4) mula ≥1; beli henti di high + Trigger; keadaan tamat → henti di low − Trigger | Kod fungsi tidak disemak; lalai ditala pada SPX 30 minit | traderpedia.it/wiki/index.php/TS_Confluence |

## Belum diproses (ditemui tetapi tidak sempat dibaca terperinci)

Hull MA (Alan Hull), ZLMA (Ehlers & Way), Normalized LR Slope (Kaufman), MACD RS Ratio (Gilbert Raff; perlu siri penanda aras), Stochastic S&C, WSO/WRO S&R, Recursive Moving Trendline, Wide Range (Crabel), weekly ORB, Bullish Engulfing Type A — semua di Traderpedia/Oxfordstrat. Lilin generik dengan peraturan masuk & henti (Two-bar reversal, Three-bar reversal, Morning Star, Hammer, Abandoned Baby) — di LuxAlgo.
Sumber yang belum dapat dicapai: Reddit, stockbee.blogspot.com, Chartink, TradingQnA, pustaka AmiBroker, Street Smarts bab 18–25, Elite Trader.

---

# Tambahan 15 Okt 2026 (daripada pengguna)

| K | Kaedah | Pencipta | Masuk | Keluar | ≈ | Sumber |
|---|---|---|---|---|---|---|
| K397 | EMA 10/21 + Supertrend (10,3) | @apoorvsinghasr (X) | EMA10 > EMA21; (A) harga undur menguji EMA10/EMA21 + lilin pengesahan naik, ATAU (B) pecah atas julat sempit 3–5 hari; Supertrend(10,3) hijau sebagai penapis (sumber bercanggah: hantaran kata "bukan isyarat masuk") | Henti bawah swing low terkini; jual 25% pada 4R, 25% pada 2 tutup berturut < EMA10, 25% pada 2 tutup berturut < EMA21, baki selepas EMA10 < EMA21 + lower high disahkan; tambah semula 4×25% apabila tutup semula atas EMA10/EMA21, higher low, atau pecah pivot high | M18 (EMA9/21 pullback), M33 (Supertrend 10/3) — baharu pada gabungan + keluar/tambah berperingkat | Hantaran X "My Final Trading Strategy: 10/21 EMA + Supertrend (10,3)" (tangkapan skrin + infografik; tiada URL). Kad Spesifikasi Mesin V0–V5 ada dalam lampiran pengguna 15 Okt 2026 |

---

# Semakan Pendua (15 Okt 2026)

K145–K397 disemak sesama sendiri dan terhadap K32–K144, M01–M114 dan I01–I32. Nombor K tidak dipadam; status di bawah menentukan sama ada calon dibawa ke STEP-1.

## Tahap 1 — PENDUA (peraturan teras sama; jangan bawa ke STEP-1 secara berasingan)

| K | Pendua kepada | Sebab |
|---|---|---|
| K228 苦尽甘来 | K189 多方炮 | Lilin naik besar → lilin turun kecil volum rendah → lilin naik volum tinggi menelan (bentuk Rising Three Methods) |
| K231 MOST | K191 OTT | Pencipta sama (Özekşi), garis henti mengekor yang sama; beza hanya jenis MA |
| K248 Whiplash | K247 Gilligan's Island | Jurang turun ke low, tutup separuh atas julat, beli; beza hanya masa masuk |
| K268 BSJP | K267 종가베팅 | Beli pada tutup hari pecah volum tinggi, jual pagi esok |
| K272 MAR (nisbah MA) | M84 MAD 21/200 | Nisbah MA pendek ÷ MA panjang = MAD |
| K314 RS Phase | I03 Garis RS vs indeks | Garis RS atas EMA21nya — penapis garis RS yang sama |
| K323 Bullish Marubozu | K151 180 Bullish (melalui K183) | Bar naik berbadan penuh, beli atas high, henti low bar |
| K339 2B Bottom | K172 Turtle Soup | Low baharu palsu, kemudian harga kembali atas — konsep sama |
| K340 Conner 19 | K336 Down-5C | Siri tutup menurun berturut (4 lawan 5), beli lantunan |
| K347 Calm After Storm | K168 Jack-in-the-Box | Bar julat lebar, kemudian bar mengecut/dalam, beli atas high |
| K182 Consolidation Pivot (Haber) | K358 versi angka Deepvue | K358 menakrif "berhimpun/ketat" dengan angka; K182 tiada ambang (kecacatan sama seperti M43) |
| K183 Elephant Bar / Bull 180 | K151 180 Bullish | Corak "Bull 180" yang sama |
| K371 Double Bollinger Zones | M31 Band Walk | Tutup berturut dalam zon atas Bollinger |
| K390 Dow Theory – Trend | K345 1-2-3 Low | Beli tembus pivot high-lebih-rendah terakhir selepas aliran turun |
| K393 Force Index Dip | M50 Elder Triple Screen | Force Index(2) < 0 dalam aliran naik ialah saringan kedua M50 |

## Tahap 2 — VARIAN DEKAT (berbeza pada parameter/penapis; boleh diuji sebagai varian V kaedah induk)

| K | Induk | Beza utama |
|---|---|---|
| K153 H2, K302 Trend Pivot, K197 PBS | sesama sendiri; M18 | Kiraan bar undur berbeza |
| K165 TPS, K295 RSI-2, K296 ConnorsRSI, K166 Double 7s, K328 SQN+RSI2 | K105 RSI<30 dalam saham momentum | Semua beli oversold atas SMA200 (Connors); beza indikator & keluar |
| K168 Jack-in-the-Box, K285 Yum-Yum, K352 Momentum scan | K53 Cooper Expansion Breakout | Bar julat lebar + susulan |
| K149 Boomer, K311 Shark-32, K278 Mini Coil, K287 3-Bar Inside, K300 MACD+Inside, K169 Strat | M70 Pecahan Hari Dalam | Penapis ADX/MACD/bilangan bar dalam |
| K167 HV+NR4, K221 Price Compression, K382 Doji Trend | M11 NR7 | Ukuran mengecut berbeza |
| K181 10EMA Basic, K199 Kiss MA Goodbye, K200 First Kiss, K365 Bullish Swing, K374 TrueContrarian | M18 / M08 | Tempoh MA 10 lawan 9/20 |
| K209 Aberration, K210 Bollinger Bandit, K291 Acceleration Bands | M04 / M39 | Pecahan band atas; band & keluar berbeza |
| K211 Dynamic Breakout II, K213 Following the Trend, K217 ROC Breakout, K375 Long Trends, K220 ADX+CMF | M36 Turtle / Donchian | Tempoh saluran & penapis |
| K214 52 Weeks High, K158 260-day High | K37 / M45 | Takrif paras 52 minggu & penapis volum |
| K160 AlphaTrend, K205 Chande Kroll, K206 NRTR, K208 Gann HiLo, K232 PMax, K329 Ordered TF | M105 Supertrend | Formula garis mengekor berbeza |
| K222 Kitaran MA, K223 Perfect Order, K322 Alligator, K376 DiNapoli 5 | K92 Susunan MA | Tempoh MA & peringkat |
| K225 MA berhimpun | K72 Launchpad | Ambang ATR diberi |
| K226 Lembah Perak/Emas | M107 Golden Cross | Tiga MA, bukan dua |
| K235 Dual momentum, K242 Consistent momentum, K241 Momentum×Volatiliti | I01 12-1 | Penapis tambahan |
| K236 GRJMOM | M96 Sharpe | N=1 ialah ranking Sharpe |
| K238 HVRP, K357 Bull Snort, K360 High RVOL, K364 BUY Stock, K264 底部放量 | K81 HVE / K62 HVC | Peristiwa volum tinggi |
| K243 Breakout 1M/3M Base, K353 Combo, K363 Explosive Stocks | M32 Momentum Burst | Penapis tapak / BB |
| K198 Explosion Gap Pivot, K301 Gap Type A, K351 Power Spike, K379 LeBeau | K40 / M46 Jurang Boleh Beli | Ujian jurang & masa masuk |
| K201 3C | K97 Low Cheat | Rehat di sepertiga tengah, bukan bawah |
| K202 3rd Watch, K359 Traditional Basing | K45 / K124 | Tapak O'Neil |
| K218 Proximity Pullback, K327 50-Week MA Touch | M66 Undur ke MA50 | Jarak high 52 minggu / versi mingguan |
| K219 Bull Flag, K258 Six-Out, K275 Low Tight Flag | M104 HTF | Tiang lebih pendek (10–90%) |
| K186 Luk Reclaim, K230 Teknik W | M77 Undercut & Rally MA | Penapis kenaikan ≥30% / susunan MA |
| K257 Witch Hat | M76 Undercut & Rally low | Versi cerminan |
| K251 Key Reversal Bar, K152 Reversal New Highs | K94 Oops | Hari luar bullish; K152 tambah high 60 hari |
| K254 Fakeout-Shakeout, K341 Low or High 3 | K172 Turtle Soup | Pecah palsu |
| K192 Ross Hook, K380 Dow MTF | K345 1-2-3 Low | Pivot selepas 1-2-3 |
| K260 RSI Pullback, K366 Smoothed BB% | M59 / M01 | Oversold dalam aliran naik |
| K262 空中加油, K190 龙回头 | sesama sendiri; M08 | Undur volum rendah selepas lonjakan |
| K269 CDC ActionZone, K324 Going Bullish, K377 MACD Momentum, K216 RMO | I12 MACD / M02 | Silang EMA12/26 + penapis |
| K316 Triple Momentum, K362 Coppock | M90 KST | Jumlah ROC berbilang tempoh |
| K318 5-EMA High-Low | K93 SlingShot (EMA4 high) | EMA5 lawan EMA4 |
| K320 SDA2, K330 Vol Compression, K290 3-Step Pullback, K215 Gaussian | K112 Keltner | Saluran ATR berbeza |
| K325 W+D Value Zone, K368 Elder Ray | M50 Elder Triple Screen | Mingguan aliran + osilator harian |
| K326 Kijun Throwback | M49 Ichimoku | Tambah penapis mingguan |
| K342 Finger Finder, K344 Gimmee Bar | M01 BB+RSI | Sentuh BB bawah |
| K343 Triple RSI Divergence | M03 / M05 | Tiga divergence, bukan satu |
| K349 Three Little Indians | K142 Tiga lembah menaik | Tiga lembah |
| K350 Triangle Coil | K141 Segi tiga menaik | Tambah NR7 |
| K361 ROAR | K39 Clenow | Ranking kenaikan tahunan |
| K370 RWI, K159 Vortex | M106 DMI | Garis +/− arah |
| K373 Tilley | K86 Radge MAC | Silang SMA10 + paras S/R |
| K383 FRAMA Bands | K114 KAMA | MA adaptif lain |
| K392 Zero-Line Reject | K131 CCI-50 / K156 | Lantun CCI di 0 |
| K394 Double-Bottom Base | M88 Shakeout +3 | Tapak W O'Neil |
| K397 EMA10/21 + Supertrend | M18 / M33 | Gabungan + keluar/tambah berperingkat |
| K277 Continuation Base | M07 Qullamaggie | Imbasan pra-pecahan |
| K280 Quite and Tight | M06 VCP | ADR mengecut |
| K315 Volume-Weighted Trend | K103 VWAP 21 hari | Tambah nisbah volum naik/turun |
| K356 9 Million EP | M22 Episodic Pivot | Ambang 9 juta saham |

## Ringkasan selepas semakan

| Status | Bil. |
|---|---|
| Pendua (Tahap 1) | 15 |
| Varian dekat (Tahap 2) | 118 |
| Unik | 119 |
| **Jumlah K145–K397** | **253** |
| **Calon bersih (tanpa pendua)** | **237** |


Semakan semula 15 Okt (14:45): K148 dan K279 dikeluarkan daripada senarai pendua. Induk mereka (K78→M72 dan K96) ditolak dahulu kerana tiada pencetus atau perlu data intrahari, manakala K148 dan K279 memberi pencetus harian yang jelas.

Semakan ke-3 (15 Okt, 16:30): K195 dan K281 dipindah daripada pendua kepada cadangan buang (induk mereka sendiri ditolak); K182 kini pendua K358; K183 pendua K151. Status penuh dalam `CADANGAN_SARINGAN_K145.md`.
