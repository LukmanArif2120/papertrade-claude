# SPEC SEMUA N — kombinasi daripada pakar, forum dan platform sosial

**Dijana oleh `BacktestShariah2/standard/registry_n.py`. Jangan sunting fail ini secara manual** — sunting senarai dalam skrip itu, kemudian jalankan semula.

## Mengapa dua keluarga

`Mxx` = kaedah lengkap daripada pedagang bernama, sudah dikodkan dalam `BacktestShariah2/kod/kaedah/`. Spec: `SPEC_SEMUA_KAEDAH.md`.

`Nxx` = **kombinasi indikator** yang dikumpul daripada sumber awam (TradingView, babypips, MQL5, LuxAlgo, StockSharp, Fmz, Stockezee, Tradezella, Quantified Strategies, YouTube, X/Twitter, blog pedagang, buku). Didaftar DAHULU, diuji KEMUDIAN. Pendaftaran dahulu ialah disiplin pradaftar yang sama seperti REVERSE: senarai penuh dikomit sebelum keputusan dilihat, supaya bilangan ujian diketahui dan FDR boleh dikira.

**Dapatan carian web yang penting:** peraturan pedagang **TIDAK diseragamkan**. Setiap sumber memberi versi berbeza bagi setup yang sama (ambang gap 3%-5%, pengganda volum 1.5x-2x, ADX 20-25, henti bawah rendah undur lawan bawah EMA). Jadi setiap baris di bawah ialah **satu versi tertentu daripada satu sumber tertentu**, bukan "peraturan rasmi" setup itu.

## Kesilapan struktur dalam registry ini, dan pembetulannya

**Kesemua 147 baris MASUK ialah syarat `DAN`.** Setiap satu ialah penapis. Dan `SETUP.md` sudah mengukur apa yang berlaku kepada penapis: **0 daripada 598 mempunyai lift positif**, dan sebabnya **struktur, bukan pemilihan** — setiap penapis membuang bar, dan kerana taburan saham tunggal terpencong kanan (dagangan median −5.19% tetapi min +3.03%), menapis terutamanya membuang peluang pada **ekor kanan**, satu-satunya bahagian yang membayar.

Maka menambah baris MASUK ke-148 ialah variasi ke-148 bagi sesuatu yang **sudah diukur gagal**. Enam sapuan sumber menambah baris pada paksi yang salah.

Pembetulannya bukan signal lain. Ia **operasi lain**:

- `GB02` **ATAU (kesatuan)** — menambah bar, bukan membuang. Jika masalahnya "menapis membuang ekor", maka operasi yang betul ialah kesatuan. **Belum pernah diuji.**
- `GB04` **agregat pangkat** — menukar n penapis menjadi satu skor berterusan, dan `SISTEM.md` mengukur urutan skor berterusan mempunyai sebaran benih **0.00** lawan SD 4.15 mata/tahun (ambang 95% 9.7 mata).
- `GB08` **penapis terbalik** — buang yang terbukti rugi. Pada taburan terpencong kanan, membuang ekor KIRI tidak menyentuh ekor KANAN. `KAEDAH_TERBAIK.md` sudah mengenal pasti **25 kaedah Mxx terbukti NEGATIF** pada BH-FDR q ≤ 0.05 — senarai buang itu sudah ada dan belum pernah diguna.
- `SZ10` **berat sama rata atas kolam PENUH** — `KOLAM_EKOR.md` sudah mengukur kolam penuh +1.64%/bulan lawan saham median +0.82%. Memegang **semua** mengalahkan memilih 10 dengan 0.82 mata sebulan, **tanpa apa-apa signal**.
- `IS02` **putaran ETF sektor** — `SETUP.md` mendapati SPY +3.356% dan QQQ +4.419% melepasi syarat ekor dengan mudah kerana **indeks itulah kepelbagaian merentas ekor**. ETF sektor ialah titik tengah antara saham tunggal dan SPUS, dan belum diuji.

Kelima-lima ini mengikut terus daripada ukuran yang repo **sudah** ada. Tiada satu pun memerlukan sumber baharu, data baharu, atau domain yang disekat.

## Status

- `DIUJI` — sudah ada hasil terukur; nota memberi angkanya dan fail laporan.
- `SEDIA` — semua indikator yang diperlukan sudah dikira oleh kod repo (`REVERSE/teras/ind.py` atau `REVERSE/step15_setup.py` / `step17_kombinasi.py`); boleh diuji tanpa kod indikator baharu.
- `PERLU:<x>` — perlu indikator baharu `<x>` dahulu.

Masuk: 147 (78 DIUJI, 0 SEDIA, 69 PERLU). Keluar: 45 (32 DIUJI, 1 SEDIA, 12 PERLU). Cara: 12 (6 DIUJI, 3 SEDIA, 3 PERLU). Urutan: 14 (8 DIUJI, 1 SEDIA, 5 PERLU).

Tujuh paksi baharu (30 Okt 2026): GABUNGAN 8 · SAIZ 10 · ALAM 8 · PEGANG 6 · IMBANG 5 · KORELASI 4 · INSTRUMEN 4. Jumlah semua paksi: 263 baris.

Indikator baharu yang diperlukan: `adr_pct`, `alligator`, `alphatrend`, `arxiv`, `atrts`, `bar_mingguan`, `chop`, `coppock`, `crsi`, `darvas`, `data_13f`, `data_buyback`, `data_form4`, `data_keluasan`, `data_putcall`, `data_semakan`, `data_sentimen`, `data_short`, `donchian10`, `donchian50`, `efi`, `eri`, `fib_ayunan`, `fisher`, `ftd`, `gabung_sec`, `gmma`, `gtja191`, `harmonik`, `htf`, `huggingface`, `intraday`, `isi_tutup`, `kalendar_cuti`, `kalendar_dagangan`, `kapitalisasi`, `keanggotaan`, `kelly`, `korelasi_signal`, `kst`, `kvo`, `ma5`, `matriks_kovarians`, `momentum_pinball`, `optimal_f`, `paksi_urutan`, `pgo`, `pivot_lantai`, `qqe`, `rwi`, `sejarah_stage`, `squeeze_ttm`, `stc`, `strat_bar`, `supertrend3`, `talib_cdl`, `tarikh_ipo`, `td_seq`, `tinggi_swing`, `tmo`, `tsv`, `turtle_soup`, `vhf`, `vol_portfolio`, `vortex`, `vwap20`, `vwap_ankor`, `wyckoff_spring`.

## Peraturan masuk

### MA

**N01 MA10 silang MA20 + volum** — `ma10 silang naik ma20 DAN vol_n50 >= 1.2` · permintaan pengguna (pengguna) · DIUJI · lift +0.123 latih / +0.392 tahan; TERBAIK daripada 40 (KOMBINASI.md)

**N02 MA20 silang MA50** — `ma20 silang naik ma50` · klasik (umum) · DIUJI · lift negatif pada kedua-dua tingkap

**N03 MA20 silang MA200** — `ma20 silang naik ma200` · skrip MA+ATR (TradingView) · DIUJI · lift -0.342 latih / +0.209 tahan — tidak konsisten

**N04 EMA20>EMA50 + RSI 50-70** — `ema20 > ema50 DAN 50 <= rsi14 <= 70` · skrip awam (TradingView) · DIUJI · lift negatif

**N05 tutup>EMA20>SMA100 + volum** — `tutup > ema20 DAN ema20 > sma100 DAN vol_n50 >= 1.2` · pedagang forum (babypips) · DIUJI · lift negatif

**N06 Golden cross MA50/MA200** — `ma50 silang naik ma200` · klasik (umum) · DIUJI · hari_gc sudah ada | DIUJI (NXX.md): lift terbaik X3 -0.552 latih / +0.142 tahan, n 13,422, gate1 gagal, gate2 gagal, gate3 gagal

**N07 Tiga MA tersusun** — `hari pertama ma10 > ma20 > ma50` · triple-MA klasik (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.043 latih / -0.113 tahan, n 85,712, gate1 gagal, gate2 gagal, gate3 gagal

**N08 tutup>EMA20 tidak terlalu jauh** — `tutup > ema20 DAN (tutup - ema20) <= 1.5 x atr14` · pedagang forum (babypips) · DIUJI · sumber menegaskan LANGKAU jika terlalu jauh dari EMA20 | DIUJI (NXX.md): lift terbaik X1 -0.066 latih / -0.074 tahan, n 1,596,759, gate1 gagal, gate2 gagal, gate3 gagal

**N09 Undur EMA10 + penapis EMA50** — `tutup > ema10 DAN tutup[-1] < ema10[-1] DAN tutup > ema50` · skrip 10ema (TradingView) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.100 latih / -0.093 tahan, n 229,340, gate1 gagal, gate2 gagal, gate3 gagal

**N76 Tutup > MA50 (penapis trend tunggal)** — `tutup > ma50` · QuantJourney O04 (quantjourney-bt) · DIUJI · berguna sebagai ASAS penapis tunggal untuk mengira lift | DIUJI (NXX.md): lift terbaik X1 -0.085 latih / -0.118 tahan, n 2,296,233, gate1 gagal, gate2 gagal, gate3 gagal

**N140 Guppy GMMA: kumpulan pendek atas kumpulan panjang** — `EMA(3,5,8,10,12,15) kesemuanya atas EMA(30,35,40,45,50,60)` · Daryl Guppy (buku/TTR/StockSharp) · PERLU:gmma · tiada set peraturan berangka formal dalam mana-mana sumber - hanya tafsiran persilangan kumpulan

### RSI

**N10 RSI14 silang SMA14(RSI)** — `rsi14 silang naik SMA14(rsi14)` · skrip sumber terbuka (TradingView) · DIUJI · lift +0.016 / +0.006 — hampir sifar

**N11 RSI 40-50 + tutup>MA50** — `40 <= rsi14 <= 50 DAN tutup > ma50` · pedagang forum (forum) · DIUJI · lift negatif

**N12 RSI 40-60 + EMA20 + MA50 naik** — `tutup > ema20 DAN cerun_ma50 > 0 DAN 40 <= rsi14 <= 60` · konsensus blog (blog) · DIUJI · lift negatif

**N13 RSI<=30 + EMA + MACD + volum** — `ema20 > ema50 DAN rsi14 <= 30 DAN macd > 0 DAN vol_n50 >= 1.5` · skrip awam (TradingView) · DIUJI · lift negatif

**N14 Connors RSI2<5 + SMA200** — `rsi2 < 5 DAN tutup > ma200` · Connors (varian 200-hari) (buku/blog) · PERLU:ma5 · keluar asal: tutup > SMA5 ATAU tutup < SMA200

**N15 Connors RSI2<10 + SMA200** — `rsi2 < 10 DAN tutup > ma200` · EA MQL5 (MQL5) · DIUJI · keluar asal rsi2 > 65 | DIUJI (NXX.md): lift terbaik X1 +0.072 latih / +0.101 tahan, n 211,655, gate1 LULUS, gate2 gagal, gate3 gagal

**N16 RSI2<10 tanpa penapis** — `rsi2 < 10` · Quantified Strategies (YouTube/Substack) · DIUJI · keluar asal rsi2 > 60; pegang 1-10 hari | DIUJI (NXX.md): lift terbaik X4 +0.284 latih / +0.518 tahan, n 567,422, gate1 LULUS, gate2 LULUS, gate3 gagal

**N17 RSI14 silang naik 30** — `rsi14 silang naik 30` · klasik terlebih jual (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X3 +0.886 latih / +1.544 tahan, n 54,073, gate1 LULUS, gate2 LULUS, gate3 gagal

**N18 RSI 30-50 pullback** — `30 <= rsi14 <= 50 DAN tutup > ma200` · Quantified Strategies (YouTube/Substack) · DIUJI · sumber lapor CAGR 5.3%, 196 dagangan, menang 81% pada S&P 500 | DIUJI (NXX.md): lift terbaik X1 +0.062 latih / -0.062 tahan, n 665,910, gate1 gagal, gate2 gagal, gate3 gagal

**N75 RSI14 < 40 tanpa penapis** — `rsi14 < 40` · QuantJourney O03 (quantjourney-bt) · DIUJI · sumber pasangkan dengan buy-limit 1.5% bawah tutup (C03) | DIUJI (NXX.md): lift terbaik X3 +0.647 latih / +1.587 tahan, n 861,071, gate1 LULUS, gate2 LULUS, gate3 gagal

**N82 Connors RSI penuh < 10** — `crsi = purata(RSI(3), RSI(2) atas panjang streak, pangkat peratus ROC(1) 100 hari) < 10` · Larry Connors (pandas_ta) · PERLU:crsi · TIGA komponen; N14-N16 hanya guna rsi2 = versi ringkas sahaja

**N117 3 hari turun + atas MA200 + bawah SMA5** — `tutup > ma200 DAN tutup < SMA5 DAN rendah < rendah[-1] DAN tinggi < tinggi[-1] bagi 3 sesi berturut` · Connors & Alvarez, High Probability ETF Trading (buku) · PERLU:ma5 · sumber sendiri kata ia direka untuk ETF kerana ETF tidak mungkin ke sifar; saham tunggal lebih lemah

**N118 4 daripada 5 sesi terakhir turun** — `tutup > ma200 DAN 4 daripada 5 sesi terakhir tutup lebih rendah` · Connors & Alvarez (buku) · DIUJI · bab berasingan dalam sumber; juga direka untuk ETF | DIUJI (NXX.md): lift terbaik X1 +0.045 latih / +0.072 tahan, n 300,593, gate1 LULUS, gate2 gagal, gate3 gagal

**N119 3 tutup turun berturut** — `tutup[-2] > tutup[-1] DAN tutup[-1] > tutup` · Connors & Alvarez, Short-Term Trading Strategies That Work (2009) (buku) · DIUJI · sumber lapor pasaran naik > 4x purata mingguan dalam 5 sesi berikut; tidak disahkan | DIUJI (NXX.md): lift terbaik X2 +0.092 latih / +0.237 tahan, n 1,051,604, gate1 LULUS, gate2 gagal, gate3 gagal

### BB

**N19 Bawah jalur BB + RSI<30** — `bb_pctb < 0 DAN rsi14 < 30` · LuxAlgo (LuxAlgo) · DIUJI · keluar asal rsi14 > 70 | DIUJI (NXX.md): lift terbaik X3 +0.873 latih / +3.618 tahan, n 73,769, gate1 LULUS, gate2 gagal, gate3 gagal. Satu daripada DUA kes dalam kajian yang memperbaiki jangkaan terpangkas-ekor (+1.08 mata atas asasnya), jadi kelebihannya tidak hidup sepenuhnya dalam ekor kanan. Kaki pembalikan min dalam GB02_atau3 | PRODUKSI 1 Nov 2026: modul kod/kaedah/N19.py berjalan setiap malam dalam Papertrade C; pradaftar jejak REVERSE/SPEC_JEJAK_N.md

**N20 Kembali masuk jalur + RSI silang 30** — `bb_pctb[-1] < 0 DAN bb_pctb > 0 DAN rsi14 silang naik 30` · therighttrader (blog) · DIUJI · henti pada ekstrem luar; keluar jalur tengah | DIUJI (NXX.md): lift terbaik X3 +0.936 latih / +1.614 tahan, n 19,208, gate1 LULUS, gate2 gagal, gate3 gagal. Kaki KEEMPAT GB02_atau4; atau4 dan atau3 hampir sama (jangkaan +4.944% lawan +5.025%) | PRODUKSI 1 Nov 2026: modul kod/kaedah/N20.py berjalan setiap malam dalam Papertrade C; pradaftar jejak REVERSE/SPEC_JEJAK_N.md

**N21 BB + RSI 40/60** — `bb_pctb < 20 DAN rsi14 > 40` · Fmz (Fmz) · DIUJI · sasaran untung 2% tetap | DIUJI (NXX.md): lift terbaik X1 +0.040 latih / -0.053 tahan, n 266,924, gate1 gagal, gate2 gagal, gate3 gagal

**N22 BB pecah atas + RSI** — `bb_pctb > 100 DAN rsi14 > 50` · StockSharp (StockSharp) · DIUJI · keluar jalur tengah | DIUJI (NXX.md): lift terbaik X1 -0.145 latih / -0.268 tahan, n 288,864, gate1 gagal, gate2 gagal, gate3 gagal

**N23 BB squeeze kemudian pecah** — `bb_squeeze[-1] DAN tutup > ema20` · klasik (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.061 latih / -0.199 tahan, n 56,608, gate1 gagal, gate2 gagal, gate3 gagal

**N73 Tutup bawah jalur bawah BB(20,2)** — `tutup < SMA20 - 2 x SD20` · QuantJourney W21 (quantjourney-bt) · DIUJI · keluar asal: tutup > jalur tengah SMA20 | DIUJI (NXX.md): lift terbaik X3 +0.425 latih / +0.889 tahan, n 240,838, gate1 LULUS, gate2 gagal, gate3 gagal

### TREND

**N24 Supertrend(10,3) + ADX>20** — `supertrend > 0 DAN adx14 > 20` · therighttrader (blog) · DIUJI · sumber: ATR 10, pengganda 3, ADX Wilder 14, ambang 20 | DIUJI (NXX.md): lift terbaik X1 -0.091 latih / -0.081 tahan, n 1,359,653, gate1 gagal, gate2 gagal, gate3 gagal

**N25 Supertrend + EMA + ADX>23** — `supertrend > 0 DAN tutup > ema20 DAN adx14 > 23` · skrip awam (TradingView) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.118 latih / -0.132 tahan, n 948,243, gate1 gagal, gate2 gagal, gate3 gagal

**N26 Tiga Supertrend + EMA + ADX** — `ketiga supertrend > 0 DAN tutup > ema20 DAN adx14 > ambang` · LuxAlgo (LuxAlgo) · PERLU:supertrend3 · tiga pengganda ATR berbeza

**N27 Ichimoku atas awan** — `atas_awan DAN tenkan_atas` · klasik (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.090 latih / -0.126 tahan, n 1,562,663, gate1 gagal, gate2 gagal, gate3 gagal

**N28 ADX>25 + DI+ > DI-** — `adx14 > 25 DAN mdi < adx14` · Wilder (buku) · DIUJI · proksi DI daripada lajur sedia ada | DIUJI (NXX.md): lift terbaik X3 -0.094 latih / +0.914 tahan, n 1,404,045, gate1 gagal, gate2 gagal, gate3 gagal

**N29 PSAR naik + tutup>MA50** — `psar_arah > 0 DAN tutup > ma50` · klasik (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.093 latih / -0.138 tahan, n 1,557,048, gate1 gagal, gate2 gagal, gate3 gagal

**N74 MACD atas garis isyarat (keadaan, bukan silang)** — `macd > macd_sig` · QuantJourney W22 (quantjourney-bt) · DIUJI · BERBEZA daripada macd_cross: keadaan berterusan, bukan peristiwa silang | DIUJI (NXX.md): lift terbaik X3 -0.096 latih / +0.133 tahan, n 2,255,263, gate1 gagal, gate2 gagal, gate3 gagal

**N83 AlphaTrend menaik** — `alphatrend > alphatrend[-2]` · KivancOzbilgic (TradingView / pandas_ta) · PERLU:alphatrend · ATR + MFI (atau RSI) memilih jalur

**N86 Vortex VI+ silang naik VI-** — `vtxp silang naik vtxm` · Botes & Siepman (TASC Jan 2010) (pandas_ta) · PERLU:vortex

**N87 VHF > 0.35 + tutup > MA50** — `vhf(28) > 0.35 DAN tutup > ma50` · Adam White (pandas_ta) · PERLU:vhf · Vertical Horizontal Filter: tinggi = trend, rendah = sisi

**N92 Alligator mulut terbuka menaik** — `jaw(13) < teeth(8) DAN teeth(8) < lips(5) DAN tutup > lips` · Bill Williams (pandas_ta) · PERLU:alligator

**N95 Choppiness Index < 38.2 + tutup > MA50** — `chop(14) < 38.2 DAN tutup > ma50` · E.W. Dreiss (pandas_ta) · PERLU:chop · rendah = trend, tinggi = sisi; 38.2 ialah paras Fibonacci yang sumber guna

**N96 Random Walk Index tinggi > 1** — `rwi_tinggi > 1 DAN rwi_tinggi > rwi_rendah` · Michael Poulos (pandas_ta) · PERLU:rwi · > 1 bermakna gerakan melebihi apa yang jalan rawak boleh terangkan

**N99 ATR Trailing Stop naik dan tutup di atasnya** — `atrts > atrts[-1] DAN tutup > atrts` · pandas_ta (atrts) (pandas_ta) · PERLU:atrts · serupa lorong 2 Chandelier repo tetapi pengangkaan berbeza

**N141 Elder Triple Screen** — `histogram MACD mingguan menaik DAN osilator harian terlebih jual DAN beli-stop 1 mata atas tinggi bar isyarat` · Elder, Trading for a Living (buku) · PERLU:bar_mingguan · satu pengkritik lapor histogram MACD tradisional memberi hanya ~5 dagangan setahun. MACD sendiri karya Gerald Appel, bukan Elder.

### PECAH

**N30 Turtle sistem 1** — `donchian20 pecah` · Dennis/Eckhardt (buku) · PERLU:donchian10 · henti 2xATR20; keluar Donchian10 bertentangan

**N31 Turtle sistem 2** — `donchian55 pecah` · Dennis/Eckhardt (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.153 latih / -0.287 tahan, n 176,582, gate1 gagal, gate2 gagal, gate3 gagal

**N32 Donchian50 (Darvas ringkas)** — `donchian50 pecah` · EA Darvas (MQL5) · PERLU:donchian50

**N33 Donchian20 + penapis MA200** — `donchian20 pecah DAN j_ma200 > 0` · skrip awam (TradingView) · DIUJI · henti pada jalur bertentangan | DIUJI (NXX.md): lift terbaik X1 -0.128 latih / -0.219 tahan, n 223,348, gate1 gagal, gate2 gagal, gate3 gagal

**N34 Darvas Box** — `pecah atas kotak Darvas` · Darvas (buku) · PERLU:darvas · tiada peraturan berangka standard; henti bawah kotak

**N35 Pecah 52 minggu tinggi** — `breakout_52w` · klasik (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.097 latih / -0.223 tahan, n 182,300, gate1 gagal, gate2 gagal, gate3 gagal

**N36 Pocket pivot** — `pocket_pivot` · Morales/Kacher (buku) · DIUJI · juga M35 dalam keluarga Mxx | DIUJI (NXX.md): lift terbaik X1 -0.143 latih / -0.228 tahan, n 386,797, gate1 gagal, gate2 gagal, gate3 gagal

**N37 Gap and go** — `gap_and_go` · klasik intraday (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X3 +0.323 latih / +2.099 tahan, n 19,652, gate1 LULUS, gate2 gagal, gate3 gagal. Kaki MOMENTUM dalam GB02_atau3; pegang median 4 hari jadi kohort ini matang jauh lebih awal daripada tiga kaki yang lain | PRODUKSI 1 Nov 2026: modul kod/kaedah/N37.py berjalan setiap malam dalam Papertrade C; pradaftar jejak REVERSE/SPEC_JEJAK_N.md

**N38 VCP pecah** — `vcp` · Minervini (buku) · DIUJI · juga M06 | DIUJI (NXX.md): lift terbaik X3 -0.289 latih / +0.234 tahan, n 452,952, gate1 gagal, gate2 gagal, gate3 gagal

**N39 NR7 kemudian pecah** — `nr7[-1] DAN donchian20` · Crabel (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.088 latih / -0.221 tahan, n 36,881, gate1 gagal, gate2 gagal, gate3 gagal

**N80 Tinggi sepanjang masa** — `tutup >= tutup tertinggi sepanjang masa` · Wilcox & Crittenden (2005); Zarattini, Pagani & Wilcox (2025) (Quantpedia) · DIUJI · SAMA dengan K195 dalam katalog K; henti ekor asal 10 x ATR, pegangan purata ~305 hari (kedudukan, bukan swing) | DIUJI (NXX.md): lift terbaik X1 -0.055 latih / -0.099 tahan, n 110,082, gate1 gagal, gate2 gagal, gate3 gagal

**N130 Opening Range Breakout 5 minit** — `arah lilin 5 minit pertama menentukan sisi; masuk pada pecah julatnya dari buka lilin kedua` · Zarattini, Barbon & Aziz (SSRN/akademik) · PERLU:intraday · repo TIADA bar intrahari. Replikasi bebas pada 5 indeks lapor kelebihan KASAR berulang tetapi pulangan BERSIH hampir SIFAR selepas kos. Saiz asal: syer = risiko$/(masuk - rendah).

### VOLUM

**N40 OBV tinggi baharu + MA50** — `obv_tinggi_baru DAN tutup > ma50` · klasik (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.065 latih / -0.181 tahan, n 132,453, gate1 gagal, gate2 gagal, gate3 gagal

**N41 CMF20>0 + tutup>EMA20** — `cmf20 > 0 DAN tutup > ema20` · Chaikin (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.096 latih / -0.110 tahan, n 1,536,991, gate1 gagal, gate2 gagal, gate3 gagal

**N42 Lonjakan volum 2x** — `vol_n50 >= 2.0 DAN tutup > tutup[-1]` · umum (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X3 +0.270 latih / +1.093 tahan, n 130,675, gate1 LULUS, gate2 gagal, gate3 gagal

**N88 Elder Force Index > 0 + tutup > EMA21** — `efi(13) > 0 DAN tutup > ema21` · Alexander Elder (pandas_ta) · PERLU:efi

**N89 Elder Ray: bull power > 0 dan bear power menaik** — `eri_bull > 0 DAN eri_bear > eri_bear[-1]` · Alexander Elder (pandas_ta) · PERLU:eri

**N90 Klinger Volume Oscillator silang naik 0** — `kvo silang naik 0` · Stephen Klinger (pandas_ta) · PERLU:kvo

**N91 Time Segmented Volume > 0 + tutup > MA50** — `tsv(18) > 0 DAN tutup > ma50` · Worden Brothers (pandas_ta) · PERLU:tsv

### UNDUR

**N43 Undur EMA8 + penapis MA50** — `tutup[-1] < ema9[-1] DAN tutup > ema9 DAN tutup > ma50` · Morpheus Trading (Deel) (blog) · DIUJI · sumber guna EMA8; repo ada ema9 — proksi terdekat | DIUJI (NXX.md): lift terbaik X1 -0.096 latih / -0.074 tahan, n 233,028, gate1 gagal, gate2 gagal, gate3 gagal

**N44 Undur EMA21 + EMA21>MA50** — `tutup > ema21 DAN tutup[-1] < ema21[-1] DAN ema21 > ma50` · panduan 8/21 EMA (blog) · DIUJI · sumber: 21 EMA atas 50 EMA dan harga atas kedua-duanya | DIUJI (NXX.md): lift terbaik X1 -0.069 latih / -0.067 tahan, n 128,080, gate1 gagal, gate2 gagal, gate3 gagal

**N45 Undur EMA21 cerun positif** — `tutup > ema21 DAN cerun_ema21 > 0 DAN julat10 < julat20` · panduan 8/21 EMA (blog) · DIUJI · sumber syarat "EMA 45 darjah" — proksi cerun; elak EMA rata | DIUJI (NXX.md): lift terbaik X1 -0.094 latih / -0.125 tahan, n 1,649,671, gate1 gagal, gate2 gagal, gate3 gagal

**N46 Pecah tinggi bar penolakan** — `rendah[-1] <= ema21[-1] DAN tutup > tinggi[-1]` · journalplus/kotakneo (blog) · DIUJI · sumber TEGAS: masuk pada pecah tinggi lilin penolakan, BUKAN pada undur itu sendiri | DIUJI (NXX.md): lift terbaik X2 +0.138 latih / +0.011 tahan, n 665,113, gate1 LULUS, gate2 gagal, gate3 gagal

### KETAT

**N47 NR7 + EMA9>EMA21** — `nr7 DAN ema9 > ema21 DAN tutup > ema21` · Stockezee (screener) · DIUJI · sumber asal 10EMA>20EMA pasaran India; ema9/ema21 proksi | DIUJI (NXX.md): lift terbaik X1 -0.083 latih / -0.123 tahan, n 303,256, gate1 gagal, gate2 gagal, gate3 gagal

**N48 Inside day pecah** — `inside_day[-1] DAN tutup > tinggi[-1]` · Crabel (buku) · DIUJI · order henti atas tinggi inside day — tidak meramal arah | DIUJI (NXX.md): lift terbaik X1 -0.021 latih / -0.080 tahan, n 158,573, gate1 gagal, gate2 gagal, gate3 gagal

**N49 NR7 + inside day serentak** — `nr7 DAN inside_day` · Crabel (buku) · DIUJI · Crabel: gabungan dua ini paling mampat | DIUJI (NXX.md): lift terbaik X3 +0.015 latih / +0.712 tahan, n 209,101, gate1 LULUS, gate2 gagal, gate3 gagal

**N50 Mampat + pecah volum 1.5x** — `julat10 < 0.5 x julat20 DAN vol_n50 >= 1.5 DAN tutup > tinggi[-1]` · Stockezee (screener) · DIUJI · sumber tolak pecah bervolum lemah (< 1.5x) dan langkau 5 hari sebelum earnings | DIUJI (NXX.md): lift terbaik X3 -0.273 latih / +1.875 tahan, n 14,857, gate1 gagal, gate2 gagal, gate3 gagal

**N51 BB squeeze + Supertrend** — `bb_squeeze DAN supertrend > 0` · Squeeze Momentum (LazyBear) (YouTube) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.082 latih / -0.178 tahan, n 59,912, gate1 gagal, gate2 gagal, gate3 gagal

**N52 Squeeze lepas + atas MA200** — `bb_squeeze[-1] DAN bb_lebar > bb_lebar[-1] DAN j_ma200 > 0` · Squeeze + EMA200 (YouTube) · DIUJI · video guna EMA200 sebagai penapis trend | DIUJI (NXX.md): lift terbaik X1 -0.068 latih / -0.200 tahan, n 27,526, gate1 gagal, gate2 gagal, gate3 gagal

**N81 TTM Squeeze lepas + momentum naik** — `squeeze OFF pada bar ini DAN ON pada bar sebelum DAN momentum squeeze > 0` · John Carter (pandas_ta / Simpler Trading) · PERLU:squeeze_ttm · BERBEZA daripada bb_squeeze repo (lebar BB): TTM = BB(20,2) berada DALAM KC(20,1.5,ATR)

**N116 ID/NR4** — `inside_day DAN julat hari ini terkecil dalam 4 hari; beli-stop atas tinggi` · Connors & Raschke, Street Smarts (1995) (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X3 +0.026 latih / +0.532 tahan, n 323,670, gate1 LULUS, gate2 gagal, gate3 gagal

### ADX

**N53 Supertrend + ADX>25** — `supertrend > 0 DAN adx14 > 25` · StockSharp (StockSharp) · DIUJI · keluar asal: supertrend berbalik (dipakai sebagai henti ekor) | DIUJI (NXX.md): lift terbaik X3 -0.386 latih / +0.062 tahan, n 913,085, gate1 gagal, gate2 gagal, gate3 gagal

**N54 Supertrend + RSI>50** — `supertrend > 0 DAN rsi14 > 50` · skrip posisional (TradingView) · DIUJI · ADX pilihan dalam sumber | DIUJI (NXX.md): lift terbaik X1 -0.090 latih / -0.106 tahan, n 1,820,574, gate1 gagal, gate2 gagal, gate3 gagal

**N55 BB + RSI + ADX>20** — `bb_pctb < 20 DAN rsi14 > 40 DAN adx14 > 20` · "Super Swing Strategy" (TradingView) · DIUJI · DIUJI (NXX.md): lift terbaik X1 +0.077 latih / -0.073 tahan, n 113,407, gate1 gagal, gate2 gagal, gate3 gagal

**N56 RSI>50 + ADX>20** — `rsi14 > 50 DAN adx14 > 20` · MTF RSI-ADX-ATR (TradingView) · DIUJI · henti ATR dalam sumber | DIUJI (NXX.md): lift terbaik X1 -0.103 latih / -0.140 tahan, n 1,384,407, gate1 gagal, gate2 gagal, gate3 gagal

**N57 ADX bangkit daripada <20** — `adx14 > 20 DAN adx14[-1] <= 20 DAN tutup > ma50` · Wilder (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.111 latih / -0.223 tahan, n 45,009, gate1 gagal, gate2 gagal, gate3 gagal

**N58 DI+ silang DI- + ADX>20** — `pdi silang naik mdi DAN adx14 > 20` · Wilder (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X2 -0.053 latih / +0.190 tahan, n 62,725, gate1 gagal, gate2 gagal, gate3 gagal

**N115 Holy Grail (Raschke)** — `adx14 > 30 DAN undur menyentuh ema20 DAN tutup > tinggi bar sebelum` · Linda Raschke (buku/blog) · DIUJI · repo ada adx14 dan ema21; ema20 tepat perlu dikira | DIUJI (NXX.md): lift terbaik X3 +0.452 latih / +1.750 tahan, n 104,014, gate1 LULUS, gate2 LULUS, gate3 gagal. SATU-SATUNYA peraturan MASUK Nxx yang melepasi gate1 DAN gate2 (bertahan BH-FDR), dan memperbaiki jangkaan terpangkas-ekor +0.70 mata. Kaki momentum kedua GB02_atau3 | PRODUKSI 1 Nov 2026: modul kod/kaedah/N115.py berjalan setiap malam dalam Papertrade C; pradaftar jejak REVERSE/SPEC_JEJAK_N.md

### VWAP

**N59 tutup>VWAP + ADX>25** — `tutup > vwap20 DAN adx14 > 25` · StockSharp (StockSharp) · PERLU:vwap20 · sumber lapor ~157%/tahun tetapi pada KRIPTO, bukan saham; keluar bila adx14 < 20

**N60 VWAP + ADX + nisbah volum** — `tutup > vwap20 DAN adx14 > 20 DAN vol_n50 >= 1.5` · SwingTrade ADX v6 (TradingView) · PERLU:vwap20

**N61 VWAP berankor** — `tutup > vwap_ankor sejak pecah terakhir` · pedagang X (X/Twitter) · PERLU:vwap_ankor · tiada definisi standard bagi titik ankor

### POLA

**N62 Flat base pecah** — `julat20 <= 0.08 x tutup DAN tutup > tinggi20[-1]` · Tradezella/O’Neil (blog) · DIUJI · sumber: MA mengetat dan julat harian mengecil | DIUJI (NXX.md): lift terbaik X1 -0.030 latih / -0.030 tahan, n 35,685, gate1 gagal, gate2 gagal, gate3 gagal

**N63 High tight flag** — `gap >= 3% DAN vol_n50 >= 2.0 pada hari gap DAN sisi 3-8 hari DAN tutup > tinggi bendera` · skrip gaya Minervini (TradingView) · PERLU:htf

**N64 Episodic pivot** — `gap_and_go DAN vol_n50 >= 2.0` · Qullamaggie/Tradezella (blog/YouTube) · DIUJI · sumber tawar "high-volume close" sebagai masuk kedua | DIUJI (NXX.md): lift terbaik X3 +0.290 latih / +1.572 tahan, n 13,667, gate1 LULUS, gate2 gagal, gate3 gagal

**N65 Gap 4% + volum + hampir 52w** — `gap_and_go DAN vol_n50 >= 1.5 DAN j_52w_tinggi >= -0.05` · pemeriksa pramasa (blog) · DIUJI · sumber: gap 4%, volum pramasa > 100k, pemangkin dalam 24 jam | DIUJI (NXX.md): lift terbaik X1 -0.008 latih / -0.110 tahan, n 6,537, gate1 gagal, gate2 gagal, gate3 gagal

**N66 52w tinggi + pengesahan 1%** — `tutup > 1.01 x tinggi_52w[-1]` · panduan amaran pecah (blog) · DIUJI · sumber: cetus 1-2% ATAS paras untuk tapis pecah palsu; elak saham tipis | DIUJI (NXX.md): lift terbaik X1 -0.184 latih / -0.308 tahan, n 43,179, gate1 gagal, gate2 gagal, gate3 gagal

**N67 Hammer di MA50** — `hammer DAN rendah <= ma50 DAN tutup > ma50` · klasik lilin (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.153 latih / -0.119 tahan, n 20,900, gate1 gagal, gate2 gagal, gate3 gagal

**N68 Bullish engulfing + EMA21** — `bullish_engulfing DAN tutup > ema21` · klasik lilin (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.090 latih / -0.108 tahan, n 106,476, gate1 gagal, gate2 gagal, gate3 gagal

**N111 Turtle Soup** — `rendah 20 hari baharu yang ekstrem 20 hari sebelumnya berlaku >= 4 sesi lalu` · Connors & Raschke, Street Smarts (1995) (buku) · PERLU:turtle_soup · sumber sekunder TIDAK SEPAKAT: umur ekstrem 3 atau 4 bar; ofset masuk 5-10 tik atau 1/8 mata. Teks buku belum dibaca.

**N112 Turtle Soup Plus One** — `syarat Turtle Soup tetapi masuk satu sesi kemudian` · Connors & Raschke, Street Smarts (1995) (buku) · PERLU:turtle_soup

**N113 80-20 bar (sisi beli)** — `buka dalam 20% BAWAH julat hari DAN tutup dalam 20% ATAS julat hari` · Connors & Raschke, Street Smarts (1995) (buku) · DIUJI · sumber BERCANGGAH pada rangka: satu kata fade, satu lagi kata ikut; ini bacaan sisi beli | DIUJI (NXX.md): lift terbaik X1 -0.014 latih / -0.061 tahan, n 389,109, gate1 gagal, gate2 gagal, gate3 gagal

**N123 Power Earnings Gap** — `gap earnings DAN vol_n50 >= 3.0 DAN tutup dalam 25% atas julat hari` · therighttrader (blog) · PERLU:gabung_sec · keluar asal: henti bawah rendah hari gap; gagal jika tutup < buka hari gap. DIBETULKAN 30 Okt 2026 (SPEC_NXX §10): perlu tarikh earnings titik-masa; data/sec/ ada tetapi penyertaannya tugas data berasingan. DIBETULKAN LAGI 2 Nov 2026 (AUDIT_PERLU.md): token lama `tarikh_earnings` SALAH kerana ia menyiratkan data yang hilang. Data ADA dan dijejak git — data/sec/earnings_8k.csv 178,726 baris 8-K Item 2.02 merentas 2,795 saham 2004-2026. Yang tiada ialah PAIP yang menggabungkannya ke panel, bukan data; liputan terhadap 3,180 nama panel 83.6%, jadi pengecualian mesti eksplisit atau N123 jadi penapis liputan tersembunyi.

**N124 Episodic pivot gap 8-10%** — `gap >= 8% DAN vol_n50 >= 2.0` · Qullamaggie/Bonde melalui Tradingsim (blog) · DIUJI · lebih tegas daripada N64 yang hanya guna gap_and_go | DIUJI (NXX.md): lift terbaik X3 -0.132 latih / +7.066 tahan, n 12,728, gate1 gagal, gate2 gagal, gate3 gagal

**N125 Undur Fibonacci 38.2-61.8 + bar penolakan** — `undur ke zon 38.2%-61.8% ayunan terakhir DAN bar penolakan DAN tutup > tinggi bar penolakan` · konsensus blog (LuxAlgo, therighttrader, kotakneo) (blog) · PERLU:fib_ayunan · henti asal di 78.6%. Sumber mengakui 50% BUKAN nisbah Fibonacci, hanya titik tengah psikologi.

**N126 Floor trader pivot: tutup silang naik P** — `P = (tinggi[-1] + rendah[-1] + tutup[-1])/3; tutup silang naik P` · pivot pedagang lantai (TradingView/QuantShare) · PERLU:pivot_lantai · sumber syorkan versi MINGGUAN untuk ufuk swing, dan beramaran JANGAN masuk pada sentuhan

**N127 Wyckoff spring** — `rendah < rendah julat 20 hari kemudian tutup kembali DALAM julat` · Wyckoff (buku/blog) · PERLU:wyckoff_spring · sumber BERCANGGAH pada volum: satu kata volum RENDAH pada spring, satu lagi guna spring bervolum TINGGI yang gagal pulih sebagai isyarat BEARISH. Satu sumber mengaku tiada kadar menang terbitan bagi membeli setiap spring.

**N132 The Strat 2-1-2** — `bar arah (2), kemudian inside bar (1), kemudian pecah tinggi inside bar` · Rob Smith (TradingView/X) · PERLU:strat_bar · sumber TIDAK SEPAKAT sama ada ia pembalikan atau penerusan; bahan Rob Smith sendiri tidak ditemui

**N133 The Strat 3-1-2** — `outside bar (3), kemudian inside bar (1), kemudian pecah tinggi inside bar` · Rob Smith (TradingView/X) · PERLU:strat_bar · sumber umumnya anggap ini pembalikan

**N136 Harmonik Gartley** — `XA->AB 0.618, AB->BC 0.382-0.886, BC->CD 1.27-1.618, XA->AD 0.786` · Gartley / Carney (blog/capital.com) · PERLU:harmonik · corak PENGUNDURAN: D kekal antara X dan A

**N137 Harmonik Bat** — `XA->AB 0.382-0.50, AB->BC 0.382-0.886, BC->CD 1.618-2.618, XA->AD 0.886` · Scott Carney (blog/capital.com) · PERLU:harmonik · satu sumber kata titik B biasanya 0.382 tepat, jadual lain benarkan 0.382-0.50

**N138 Harmonik Butterfly** — `XA->AB 0.786, AB->BC 0.382-0.886, BC->CD 1.618-2.618, XA->AD 1.27-1.618` · Gilmore / Carney (blog/capital.com) · PERLU:harmonik · corak PELANJUTAN: D melepasi X. Sumber BERCANGGAH siapa menciptanya (Bryce Gilmore lawan Carney)

**N139 Harmonik Crab** — `XA->AB 0.382-0.618, AB->BC 0.382-0.886, BC->CD 2.618-3.618, XA->AD 1.618` · Scott Carney (blog/capital.com) · PERLU:harmonik · Carney sendiri kata ini paling tepat antara harmonik

### KEKUATAN

**N69 RS kuintil 5 + sektor atas MA50** — `rs_spy_6b dalam kuintil teratas DAN sektor_atas_ma50` · O’Neil/Minervini (buku) · DIUJI · dua daripada tiga tiang yang DITINGGALKAN daripada grid 672 setup | DIUJI (NXX.md): lift terbaik X3 -0.075 latih / +0.392 tahan, n 582,620, gate1 gagal, gate2 gagal, gate3 gagal

**N70 Garis RS tinggi baharu** — `garis_rs_tinggi` · Minervini (buku) · DIUJI · DIUJI (NXX.md): lift terbaik X1 -0.065 latih / -0.175 tahan, n 98,946, gate1 gagal, gate2 gagal, gate3 gagal

**N71 RS + pecah + rejim SPY** — `rs_spy_6b kuintil teratas DAN sektor_atas_ma50 DAN donchian20 DAN spy > ma50 DAN spy > ma200` · pakej Sistem A (buku) · DIUJI · Sistem A penuh: CAGR -1.03%, MDD -40.65%, sebaran benih 4.01 (SISTEM.md)

**N72 Momentum Clenow 90 hari** — `skor = (exp(cerun regresi log 90 hari x 252) - 1) x R^2; ambil 20 teratas, imbang bulanan` · Clenow (buku) · DIUJI · Sistem B: CAGR +6.38%, MDD -11.59%, sebaran benih 0.00; pendedahan hanya 35.4%

**N77 Pulangan 252 hari dalam 3 teratas alam** — `pangkat keratan rentas pulangan 252 hari, ambil 3 teratas, imbang bulanan` · QuantJourney W15 / Jegadeesh-Titman (quantjourney-bt) · PERLU:paksi_urutan · DIBETULKAN 30 Okt 2026 (SPEC_NXX §10): ini peraturan URUTAN bukan penapis. Sumbernya guna alam 9 ETF sektor; alam repo 2,800 saham jadi "3 teratas" = 0.1%, bukan peraturan sama. Padanannya U11. Dikeluarkan daripada bahagian A.

**N78 Pulangan 21 hari dalam 3 terbawah alam (pembalikan)** — `pangkat keratan rentas pulangan 21 hari, ambil 3 TERBAWAH, imbang mingguan` · QuantJourney W16 (quantjourney-bt) · PERLU:paksi_urutan · PEMBALIKAN - bertentangan momentum. DIBETULKAN 30 Okt 2026 (SPEC_NXX §10): peraturan URUTAN, alam sumber 9 ETF lawan 2,800 saham repo. Dikeluarkan daripada bahagian A.

**N79 Momentum ganda (relatif + mutlak)** — `pulangan 252 hari dalam 2 teratas alam DAN pulangan 252 hari > 0` · QuantJourney W04 / Antonacci (quantjourney-bt) · PERLU:paksi_urutan · syarat mutlak ialah penapis rejim terbina dalam. DIBETULKAN 30 Okt 2026 (SPEC_NXX §10): bahagian "2 teratas alam" ialah URUTAN; alam sumber 9 ETF lawan 2,800 saham repo.

**N120 Trend Template Minervini (8 syarat)** — `tutup > ma150 DAN tutup > ma200 DAN ma150 > ma200 DAN ma200 menaik >= 1 bulan DAN ma50 > ma150 DAN ma50 > ma200 DAN tutup > ma50 DAN tutup >= 1.30 x rendah_52w DAN tutup >= 0.75 x tinggi_52w DAN RS >= 70` · Minervini, Trade Like a Stock Market Wizard (buku) · DIUJI · sumber sekunder TIDAK SEPAKAT pada ambang rendah 52w: 25% lawan 30%; saya guna 30% kerana skrip ProRealCode mengiranya Close/Lowest[252] > 1.3. Teks buku belum dibaca. | DIUJI (NXX.md): lift terbaik X1 -0.087 latih / -0.097 tahan, n 627,861, gate1 gagal, gate2 gagal, gate3 gagal

**N121 Weinstein Stage 2** — `stage dalam (2A, 2) daripada data/stage/status.json` · Weinstein, Secrets for Profiting in Bull and Bear Markets (buku) · PERLU:sejarah_stage · DIBETULKAN 30 Okt 2026 selepas audit: data/stage/status.json ialah PETIKAN harian (7 commit sahaja), tiada sejarah titik-masa, jadi ia tidak boleh diuji pada 2012-2025. Ia BOLEH dikira semula daripada stor harga oleh standard/stage.py (bar mingguan + MA 30 minggu), tetapi itu larian berasingan. Dikeluarkan daripada pradaftar SPEC_NXX.md §3.

**N122 Kriteria imbasan Qullamaggie** — `pulangan 1 atau 3 atau 6 bulan >= 30% DAN adr_pct > 5 DAN nilai dolar harian > USD10 juta` · Qullamaggie (sumber sekunder) (blog/screener) · PERLU:adr_pct · adr_pct (julat purata) BUKAN atr_pct repo. PEMBETULAN: saya sangka ambang $20 juta; ia TIDAK muncul dalam mana-mana sumber - angka paling konsisten ialah $10 juta. Satu sumber juga sebut "50x saiz akaun" yang peraturan berbeza sama sekali.

**N128 Short float tinggi + hari untuk tutup** — `short_float > 0.20 DAN hari_untuk_tutup > 5` · konsensus screener (blog/screener) · PERLU:data_short · AMARAN: satu kajian vendor (2,269 saham) dapati short interest > 30% BUKAN isyarat boleh dipercayai - hanya 35% mengatasi pasaran. FINRA terbit dua kali sebulan jadi perlu pengendalian titik-masa.

**N129 Belian dalaman berkelompok** — `pembelian pasaran terbuka oleh >= 2 orang dalaman dalam 30 hari` · konsensus (blog) · PERLU:data_form4 · perlu data Form 4; tiada sumber memberi backtest gabungan ini

**N142 CANSLIM (7 syarat O’Neil)** — `EPS suku semasa >= 25% DAN EPS tahunan >= 25% selama 3 tahun DAN produk/pengurusan baharu DAN volum menyokong DAN RS >= 80 DAN sokongan institusi DAN arah pasaran menaik` · O’Neil, How to Make Money in Stocks (buku/IBD) · PERLU:gabung_sec · sumber TIDAK SEPAKAT: EPS suku 18%, 20% atau 25%; dalam 15% atau 5% daripada tinggi 52w; RS >= 70 atau >= 80. Composite Rating IBD tidak dapat disahkan dalam carian. DIBETULKAN 2 Nov 2026 (AUDIT_PERLU.md): token lama `data_eps_suku` SALAH. EPS suku titik-masa ADA dan dijejak git — data/sec/eps_hasil.csv 142,635 baris metrik=eps merentas 2,846 saham, dan sue.csv sudah mengira pasangan tahun-ke-tahun. Kaki EPS tidak perlukan data baharu. Kaki yang KEKAL tersekat ialah RS titik-masa (data/rs/ tiada sejarah sebelum Sep 2026) dan sokongan institusi (13F).

**N145 Keluasan semakan analis > +0.5** — `nisbah (analis semak naik - semak turun) / jumlah > +0.5` · konsensus praktisi (blog/FMP) · PERLU:data_semakan · satu sumber anggar sebaran panjang-pendek 4-6% atas 3-6 bulan; itu anggaran blog, BUKAN hasil disahkan. Sumber lain kata momentum semakan ialah KADAR PERUBAHAN semakan, bukan jumlah perubahan.

**N146 Pemfailan 13F: belian pertama >= 3 dana besar suku sama** — `pembelian pertama kali oleh >= 3 dana besar dalam suku yang sama` · konsensus (blog) · PERLU:data_13f · 13F ada LAG 45 HARI - pada masa data dilihat, posisi mungkin sudah berubah. Satu sumber petik alfa 1.3-2.4%/tahun bagi strategi copycat.

**N147 Pengumuman belian balik saham + atas MA50** — `pengumuman buyback dalam 5 sesi DAN tutup > ma50` · umum (blog) · PERLU:data_buyback · carian TIDAK menemui bukti kajian peristiwa pulangan luar biasa - satu-satunya sumber mengakui data reaksi harga tidak tersedia. Repo ADA alat Moomoo quote_corporate_actions_buybacks.

### OSILATOR

**N84 Schaff Trend Cycle silang naik 25** — `stc silang naik 25` · Doug Schaff (pandas_ta) · PERLU:stc · MACD melalui dua lapisan stokastik

**N85 QQE silang naik** — `qqe garis cepat silang naik garis perlahan` · QQE (Quantitative Qualitative Estimation) (pandas_ta) · PERLU:qqe

**N93 Fisher Transform silang naik 0** — `fisher silang naik 0` · John Ehlers (pandas_ta) · PERLU:fisher

**N94 Pretty Good Oscillator > 3** — `pgo(14) > 3` · Mark Johnson (pandas_ta) · PERLU:pgo · sumber: > 3 bermakna pecah kuat, < -3 jual kuat

**N97 Coppock Curve silang naik 0** — `coppock silang naik 0` · Edwin Coppock (Barron’s 1962) (pandas_ta) · PERLU:coppock · JUJUR: direka untuk isyarat BULANAN pada indeks, bukan swing saham harian

**N98 KST silang naik garis isyarat** — `kst silang naik kst_sig` · Martin Pring (pandas_ta) · PERLU:kst

**N100 True Momentum Oscillator silang naik garis isyarat** — `tmo silang naik tmo_sig` · pandas_ta (tmo) (pandas_ta) · PERLU:tmo

**N114 Momentum Pinball (LBR/RSI3)** — `RSI(3) bagi ROC 1 hari < 30; beli-stop atas tinggi hari ini` · Connors & Raschke, Street Smarts (1995) (buku) · PERLU:momentum_pinball

**N134 TD Sequential buy setup 9** — `9 bar berturut dengan tutup < tutup 4 bar lalu` · DeMark (buku/pustaka) · PERLU:td_seq · parameter kanonik: setup_lookback 4, setup_target 9

**N135 TD Sequential buy countdown 13** — `selepas setup 9 selesai, kira hingga 13 bar dengan tutup <= rendah 2 bar lalu (tidak perlu berturut)` · DeMark (buku/pustaka) · PERLU:td_seq · satu pustaka menambah syarat bar 13 mesti melalui tutup bar countdown 8; itu pilihan pengekodan, BUKAN peraturan asal DeMark

### KALENDAR

**N101 Turn of the month (versi 5 hari)** — `beli pada tutup 5 hari dagangan sebelum akhir bulan` · Quantified Strategies (YouTube/Substack) · PERLU:kalendar_dagangan · keluar asal: tutup hari dagangan ke-3 bulan berikut (pegang ~7 hari)

**N102 Turn of the month (versi 2 hari)** — `beli pada tutup 2 hari dagangan sebelum akhir bulan` · Honestcowboy (TradingView) · PERLU:kalendar_dagangan · penulis lapor dalam pasaran ~25% masa sahaja; bandingkan pulangan/unit pendedahan

**N103 Pra-cuti bursa** — `beli pada tutup sesi sebelum cuti bursa` · kesan pra-cuti klasik (umum) · PERLU:kalendar_cuti

**N104 Kesan hari minggu** — `beli pada tutup hari minggu tertentu` · kesan hari minggu (akademik/umum) · DIUJI · JUJUR: 5 hari = 5 ujian; mesti dikira dalam FDR | DIUJI (NXX.md): lift terbaik X3 -0.052 latih / +0.144 tahan, n 824,568, gate1 LULUS, gate2 gagal, gate3 gagal

**N105 Santa Claus rally** — `beli pada tutup 5 sesi terakhir Disember` · klasik seasonality (umum) · PERLU:kalendar_dagangan

**N106 Sell in May songsang (pegang Nov-Apr)** — `dalam pasaran hanya November hingga April` · klasik seasonality (umum) · DIUJI · DIUJI (NXX.md): lift terbaik X1 +0.066 latih / -0.073 tahan, n 2,170,276, gate1 gagal, gate2 gagal, gate3 gagal

### REJIM

**N107 Follow-through day (O’Neil)** — `indeks naik >= 1.25% pada volum lebih tinggi daripada sesi sebelum, pada hari ke-4 atau lebih percubaan rali` · O’Neil / IBD (buku/IBD) · PERLU:ftd · ambang berubah ikut era: asal 1%, IBD 1.7% pertengahan 2000-an, kini ~1.25%. Ia BUKAN isyarat beli indeks - ia MEMBENARKAN beli peneraju yang pecah asas. Banyak gagal.

**N108 Zweig Breadth Thrust** — `EMA10 bagi naik/(naik+turun) bangkit daripada < 0.400 ke > 0.615 dalam 10 sesi` · Martin Zweig (buku) · PERLU:data_keluasan · jarang: satu sumber lapor 6 kali sejak 2010 pada alamnya

**N109 Peratus saham atas MA200 > 50%** — `keluasan_atas_ma200 > 0.50` · konsensus keluasan (umum) · PERLU:data_keluasan

**N110 SPY atas MA50 dan MA200** — `spy > spy_ma50 DAN spy > spy_ma200` · pakej Sistem A (buku) · DIUJI · sebagai pintu TUNGGAL belum diuji; sebagai bahagian Sistem A: CAGR -1.03% (SISTEM.md)

**N143 Nisbah put/call purata 10 hari > 0.85** — `purata 10 hari nisbah put/call ekuiti > 0.85` · konsensus sentimen (StockCharts/blog) · PERLU:data_putcall · repo ADA akses melalui Alpha Vantage HISTORICAL_PUT_CALL_RATIO. Ambang TIDAK diseragamkan: > 1.0, > 0.85, atau < 0.60 bergantung sumber; dan sumber berbeza pada total lawan ekuiti-sahaja. Satu sumber beramaran nisbah tinggi boleh KEKAL tinggi sepanjang penurunan.

**N144 AAII bearish > 45% + put/call > 1.0** — `AAII bearish > 0.45 DAN purata 10 hari put/call > 1.0` · konsensus sentimen (blog) · PERLU:data_sentimen · sumber kata isyarat lebih kuat bila beberapa bacaan takut sejajar

### LILIN

**N131 Keluarga penuh pola lilin TA-Lib (62 pola)** — `mana-mana daripada 62 pola lilin TA-Lib (senarai penuh dalam nota)` · TA-Lib / Nison / Morris (pandas_ta cdl_pattern) · PERLU:talib_cdl · AMARAN FDR: ini 62 UJIAN BERASINGAN, bukan satu - FDR mesti mengira 62. Repo kini ada DUA sahaja (hammer, bullish_engulfing). Senarai: 2crows 3blackcrows 3inside 3linestrike 3outside 3starsinsouth 3whitesoldiers abandonedbaby advanceblock belthold breakaway closingmarubozu concealbabyswall counterattack darkcloudcover doji dojistar dragonflydoji engulfing eveningdojistar eveningstar gapsidesidewhite gravestonedoji hammer hangingman harami haramicross highwave hikkake hikkakemod homingpigeon identical3crows inneck inside invertedhammer kicking kickingbylength ladderbottom longleggeddoji longline marubozu matchinglow mathold morningdojistar morningstar onneck piercing rickshawman risefall3methods separatinglines shootingstar shortline spinningtop stalledpattern sticksandwich takuri tasukigap thrusting tristar unique3river upsidegap2crows xsidegap3methods

## Peraturan keluar

Keluar diuji **bersilang** dengan masuk, kerana `KOMBINASI.md` menunjukkan keluar mengubah tanda jangkaan: asas tanpa sasaran +2.595% lawan sasaran 1xATR **-0.281%** pada tingkap tahan yang sama. Lift mesti dikira lawan asas **keluar yang sama**.

**X01** — `henti 1.5 x ATR14, sasaran 1 x ATR14` · pedagang forum (babypips) · DIUJI · asas tahan -0.281% — MENUKAR ASAS JADI NEGATIF; kadar menang 61.1%

**X02** — `henti 2 x ATR14, sasaran 4 x ATR14` · pelbagai (umum) · DIUJI · asas tahan +0.953%

**X03** — `henti 2 x ATR14, pegang 63 sesi` · asas kajian (repo) · DIUJI · asas tahan +2.595% — TERBAIK; kadar menang 30.2%

**X04** — `ekori 2 x ATR14` · pelbagai (umum) · DIUJI · asas tahan +1.156%

**X05** — `keluar pada jalur tengah BB(20)` · therighttrader/StockSharp (blog) · SEDIA

**X06** — `keluar bila tutup < SMA5` · Connors (buku) · PERLU:ma5

**X07** — `keluar bila rsi2 > 60` · Quantified Strategies (YouTube/Substack) · SEDIA

**X08** — `keluar bila rsi2 > 80` · Connors (buku) · SEDIA · sumber lapor CAGR 9% pada SPY 1993+, melabur hanya ~28% masa

**X09** — `keluar bila rsi2 > 65` · EA MQL5 (MQL5) · SEDIA

**X10** — `sasaran untung 2% tetap` · Fmz (Fmz) · SEDIA

**X11** — `keluar Donchian10 bertentangan` · Turtle (buku) · PERLU:donchian10

**X12** — `henti pada ekstrem luar jalur BB` · therighttrader (blog) · SEDIA

**X13** — `keluar bila rsi14 > 70` · LuxAlgo (LuxAlgo) · SEDIA

**X14** — `keluar bila rsi14 silang naik 50` · skrip awam (TradingView) · SEDIA

**X15** — `ekori Chandelier 4 x ATR14` · lorong 2 repo (repo) · SEDIA · sudah dipakai Papertrade C

**X16** — `keluar bila supertrend berbalik (henti ekor)` · StockSharp (StockSharp) · SEDIA

**X17** — `keluar bila adx14 < 20` · StockSharp VWAP+ADX (StockSharp) · SEDIA

**X18** — `keluar Donchian20 bertentangan` · Turtle sistem 2 (buku) · SEDIA

**X19** — `ekori EMA21 (jual bila tutup < ema21)` · panduan 8/21 EMA (blog) · SEDIA

**X20** — `separa 1/3 pada 2R, ekori baki dengan EMA20` · panduan 8/21 EMA (blog) · SEDIA · sumber: ambil separa pada 2R atau tinggi swing terdahulu

**X21** — `jual 1/3 pada +10% atau hari-5, ekori MA20` · Minervini/Qullamaggie (buku) · DIUJI · komponen Sistem A (SISTEM.md)

**X22** — `henti keras -8% daripada harga masuk` · O’Neil (buku) · DIUJI · komponen Sistem A

**X23** — `keluar bila jatuh keluar 20 teratas pangkat momentum; imbang bulanan` · Clenow (buku) · DIUJI · komponen Sistem B; sebaran benih 0.00

**X24** — `keluar pada tinggi swing terdahulu` · umum (blog) · PERLU:tinggi_swing

**X25** — `henti 1% bawah EMA21 atau bawah rendah undur, mana lebih ketat` · panduan 8/21 EMA (blog) · SEDIA

**X26** — `ekori 4% (peratus tetap, bukan ATR)` · QuantJourney O09 (quantjourney-bt) · SEDIA · ekor diurus enjin isi, bukan dikemas kini strategi

**X27** — `sasaran limit +3% atas harga masuk purata` · QuantJourney O03 (quantjourney-bt) · SEDIA · bandingkan dengan dapatan KOMBINASI.md: sasaran kecil merugikan

**X28** — `sasaran limit +4%; keluar pasaran jika tutup < MA50` · QuantJourney O04 (quantjourney-bt) · SEDIA · sasaran DAN kegagalan trend sebagai dua keluar berasingan

**X29** — `pegang tetap 10 bar kemudian keluar pasaran` · QuantJourney O05/O14 (quantjourney-bt) · SEDIA

**X30** — `keluar bila macd < macd_sig` · QuantJourney W22 (quantjourney-bt) · SEDIA

**X31** — `keluar bila jatuh keluar 3 teratas pangkat 252 hari; imbang bulanan` · QuantJourney W15 (quantjourney-bt) · SEDIA

**X32** — `imbang semula berkala sahaja, tiada syarat keluar lain` · QuantJourney W04 (quantjourney-bt) · SEDIA · keluar hanya berlaku apabila pangkat berubah pada tarikh imbang

**X33** — `keluar pada tutup sesi masuk` · Connors & Raschke (80-20) (buku) · SEDIA · pegang satu sesi sahaja

**X34** — `keluar bila tutup silang naik SMA5` · Connors & Alvarez (buku) · PERLU:ma5

**X35** — `keluar pada tutup hari dagangan ke-3 bulan berikut` · Quantified Strategies (YouTube/Substack) · PERLU:kalendar_dagangan · pasangan keluar bagi N101

**X36** — `keluar selepas DUA tutup di bawah MA rujukan` · Deepvue (blog) · SEDIA · sumber TEGAS: jangan bertindak atas satu hari merah sahaja

**X37** — `henti bawah rendah hari gap; gagal jika tutup < buka hari gap` · therighttrader (PEG) (blog) · SEDIA

**X38** — `biar henti sampai +2R, kemudian ekori bawah rendah ayunan harian terakhir` · therighttrader (PEG) (blog) · PERLU:tinggi_swing

**X39** — `henti pada paras undur Fibonacci 78.6%` · konsensus blog (blog) · PERLU:fib_ayunan

**X40** — `henti bawah rendah shakeout` · Wyckoff (buku/blog) · PERLU:wyckoff_spring

**X41** — `henti pada rendah hari masuk` · Zarattini, Barbon & Aziz (ORB) (SSRN/akademik) · SEDIA · saiz asal: syer = risiko$ / (harga masuk - rendah hari)

**X42** — `keluar bila histogram MACD mingguan tutup bawah garis isyarat` · Elder, Trading for a Living (buku) · PERLU:bar_mingguan · sumber lain kata ekori henti ke rendah semalam dan keluar bila stokastik terlebih beli

**X43** — `keluar pada TD Sequential sell countdown 13` · DeMark (buku/pustaka) · PERLU:td_seq

**X44** — `keluar pada zon D harmonik (sasaran 0.382 kemudian 0.618 CD)` · Scott Carney (blog) · PERLU:harmonik

**X45** — `keluar bila kumpulan pendek GMMA silang turun kumpulan panjang` · Daryl Guppy (buku/TTR) · PERLU:gmma

## Cara masuk diisi (paksi ketiga)

**Repo hanya pernah menguji `C01`.** Setiap keputusan dalam REVERSE, setiap kedudukan dalam Papan Penganalisis dan setiap baris Lejar Penuh menganggap belian berlaku pada **buka sesi berikutnya**, tanpa syarat. Itu bukan satu-satunya pilihan, dan ia PUNCA kecacatan yang sudah diukur: `KOLAM_EKOR.md` §4a mendapati 421 daripada 1,770 posisi C ditutup dibeli DAN dihentikan pada hari masuk dengan kadar menang **0.00%**. Pesanan buy-stop atau buy-limit mengubah tepat perkara itu, kerana harga isi tidak lagi ditetapkan oleh buka tanpa mengira apa yang bar itu buat.

**C01** — `beli pada buka sesi berikutnya` · asas repo (repo) · DIUJI · asas SEMUA keputusan kajian setakat ini; juga PUNCA kecacatan henti hari-0 (KOLAM_EKOR.md §4a: 421/1,770 posisi C dibeli dan dihentikan pada hari masuk, menang 0.00%)

**C02** — `buy-stop pada tinggi 20 hari x 1.002; luput selepas 5 bar` · QuantJourney O05 (quantjourney-bt) · SEDIA · pengesahan harga: tiada isi bermakna tiada dagangan, jadi ia MENAPIS pecah palsu pada peringkat pelaksanaan, bukan peringkat isyarat

**C03** — `buy-limit 1.5% bawah tutup isyarat; luput selepas 3 bar` · QuantJourney O03 (quantjourney-bt) · SEDIA · isi pasif; sumber pasangkan dengan rsi14 < 40 (N75)

**C04** — `buy-limit 1% bawah tutup isyarat` · QuantJourney O04 (quantjourney-bt) · SEDIA · sumber syaratkan tutup > ma50 (N76) sebelum meletakkan limit

**C05** — `OCO: buy-limit -2% lawan buy-stop +2%; yang isi dahulu batalkan yang lain` · QuantJourney O14 (quantjourney-bt) · SEDIA · menguji undur lawan pecah pada saham yang SAMA tanpa memilih dahulu

**C06** — `bracket: masuk pasaran + sasaran +6% + henti -3% sebagai pasangan OCO` · QuantJourney O12 (quantjourney-bt) · SEDIA · henti dan sasaran aktif serentak sejak bar masuk

**C07** — `buy-stop 1% atas tinggi semalam` · panduan pecah (blog) · SEDIA

**C08** — `beli pada tutup hari isyarat` · umum (umum) · PERLU:isi_tutup · TIDAK boleh dilaksanakan dalam papertrade repo kerana isyarat dikira SELEPAS tutup; didaftar hanya sebagai siling teori

**C09** — `buy-stop sedikit atas rendah 20 hari (5-10 tik atau 1/8 mata)` · Connors & Raschke (Turtle Soup) (buku) · SEDIA · sumber sekunder beri dua ofset berbeza

**C10** — `masuk pada buka lilin kedua selepas lilin 5 minit pertama` · Zarattini, Barbon & Aziz (SSRN/akademik) · PERLU:intraday

**C11** — `beli-stop 1 mata atas tinggi bar isyarat, dipindah naik setiap bar` · Elder (trailing buy stop) (buku) · SEDIA · jika tidak tercetus dalam bar semasa, pindahkan ke tinggi berikut

**C12** — `beli-stop atas tinggi inside bar` · Rob Smith (The Strat) (TradingView/X) · PERLU:strat_bar · henti di sisi bertentangan inside bar; sasaran pertama ekstrem bar sebelum

## Urutan alam (paksi keempat)

Bila isyarat melebihi slot, sesuatu mesti menentukan siapa dibeli. Itu **bukan** penapis: penapis MEMBUANG bar, urutan MENYUSUN bar. Perbezaan itu penting kerana `SETUP.md` mengukur bahawa setiap penapis merugikan (0 daripada 598 dengan lift positif) **dan sebabnya struktur** — menapis membuang peluang pada ekor kanan, satu-satunya bahagian yang membayar. Menyusun tidak membuang apa-apa.

Dan `SISTEM.md` mengukur sesuatu yang lebih kuat: urutan ikut **skor berterusan** mempunyai sebaran 20 benih **0.00 mata**, manakala susunan sewenang-wenang mempunyai hingar pemilihan **17.3 mata peratus setahun** (`KEPEKATAN_BENIH.md`). Jadi keputusan atas skor berterusan boleh dipercayai pada sampel jauh lebih kecil. Itu satu-satunya struktur dalam seluruh kajian yang mempunyai sifat itu.

**U01** — `rawak berbenih` · kawalan repo (repo) · DIUJI · hingar pemilihan SD 4.15 mata/tahun pada 8 slot, ambang 95% 9.7 mata (KEPEKATAN_BENIH.md); jalur 20 cabutan dalam portfolio_slot/rawak_jalur_ekuiti.csv

**U02** — `RS pasaran tertinggi` · repo (repo) · DIUJI · lorong RS_10; 29 Okt 2026 -2.15%, persentil 0 dalam jalur rawak (BANDING_SPUS.md)

**U03** — `skor momentum Clenow: (exp(cerun regresi log 90 hari x 252) - 1) x R^2` · Clenow (buku) · DIUJI · Sistem B; sebaran 20 benih 0.00 = TIADA hingar pemilihan (SISTEM.md). Ini satu-satunya struktur dalam seluruh kajian yang keputusannya boleh dipercayai pada sampel kecil.

**U04** — `gabungan kaedah beku dengan kuota slot` · repo (repo) · DIUJI · lorong GABUNGAN_10 / TOP1_10 / RAWAK_KAEDAH_10

**U05** — `skor gabungan Papan Penganalisis (backtest dipotong)` · repo (repo) · DIUJI · KAEDAH_TERBAIK.md: pangkat backtest TIADA kuasa ramalan yang boleh diukur - rho +0.16, p = 0.105 selepas mengawal hari pegang. JANGAN guna sebagai urutan.

**U06** — `101 alfa formula harga-volum (rank, ts_rank, scale -> satu skor)` · Kakushadze, Lauprete & Tulchinsky, arXiv:1601.00991 Appendix A (arXiv) · PERLU:arxiv · arxiv.org DISEKAT DNS dalam sesi ini. Formula TIDAK boleh ditulis daripada ingatan - mesti dibaca daripada Appendix A. Alfa proprietari WorldQuant LLC, diterbitkan dengan kebenaran: daftar rujukan dan laksana sendiri, JANGAN salin pukal ke repo. Inputnya hampir semuanya harga-volum harian (buka, tinggi, rendah, tutup, volum, vwap) = sepadan dengan alam repo.

**U07** — `212 peramal keratan rentas + SignalDoc (status replikasi setiap satu)` · Chen & Zimmermann, Critical Finance Review 2022 (openassetpricing.com / Hugging Face) · PERLU:huggingface · Pakej PyPI openassetpricing 0.1.0 SUDAH dimuat turun dan dibaca, tetapi datanya di huggingface.co yang DISEKAT proksi (403 CONNECT tunnel). Nilainya bukan peramal baharu: ia memberitahu peramal mana yang SUDAH diukur dan mana yang bertahan, jadi ia menghentikan repo mengukur semula ruang yang sudah diukur.

**U08** — `ATR% songsang sebagai URUTAN (bukan sebagai saiz)` · belum diuji (repo) · SEDIA · RISIKO_10 guna ATR untuk SAIZ atas susunan RS_10; ini akan guna ATR untuk URUTAN. Belum pernah diuji dan boleh dijalankan dengan lajur yang sudah ada.

**U09** — `ADR% tertinggi (julat purata, bukan ATR)` · Qullamaggie (blog/screener) · PERLU:adr_pct · ADR% ialah julat purata; atr_pct repo ialah julat BENAR - bukan sama

**U10** — `nilai dolar harian tertinggi` · Qullamaggie (blog/screener) · SEDIA · lajur nilai20 sudah ada; sumber beri ambang $10 juta, bukan urutan - ini versi urutan

**U11** — `pulangan gabungan 1 + 3 + 6 bulan tertinggi` · Qullamaggie (blog/screener) · SEDIA · sumber guna sebagai penapis 30%; ini versi urutan

**U12** — `191 alfa formula GTJA (harga, volum, volatiliti, VWAP)` · Guotai Junan Securities (2017) (laporan/arXiv) · PERLU:gtja191 · DAPATAN TERKUAT SAPUAN KEENAM: satu kertas 2026 melapor 17 daripada 191 MASIH menambah kuasa penerangan bagi pulangan saham AS selepas mengawal 151 faktor fundamental lain. Itu bukti kuantitatif LUARAN pertama bagi kemandirian mana-mana katalog dalam registry ini. Direka untuk A-share China; keluarga sama seperti U06 (skor peringkat, bukan penapis). Formula BELUM dibaca - laporan asal 2017 tidak ditemui dalam carian.

**U13** — `skor keluasan semakan analis` · konsensus praktisi (blog/FMP) · PERLU:data_semakan · versi urutan bagi N145

**U14** — `momentum 12-1 bulan (pulangan 12 bulan tolak bulan terakhir)` · Jegadeesh & Titman; standard akademik (akademik) · SEDIA · diperkenalkan dalam SPEC_INSTRUMEN.md E3 sebagai urutan bakul sektor

## Sapuan sumber: kadar pulangan sudah boleh diukur, dan ia berkurangan

Enam sapuan dijalankan 30 Okt 2026. Pertambahan masuk setiap kali: **42 → +30 → +8 → +20 → +30 → +17**.

Tetapi bilangan bukan ukuran yang betul. Yang betul ialah **berapa banyak boleh diuji dengan apa yang repo ada**:

- Sapuan 1-5 menghasilkan 71 baris berstatus `SEDIA` (boleh diuji serta-merta).
- **Sapuan 6 menghasilkan 17 baris dan SIFAR berstatus `SEDIA`.** Kesemua 17 memerlukan indikator atau data yang repo tidak ada: `talib_cdl`, `strat_bar`, `td_seq`, `harmonik`, `gmma`, `bar_mingguan`, `data_eps_suku`, `data_putcall`, `data_sentimen`, `data_semakan`, `data_13f`, `data_buyback`.

Maknanya **kekangan sudah berpindah**. Dahulu ia "cari peraturan"; sekarang ia "ada data". Mencari lebih banyak peraturan gaya pedagang pada bar harian tidak lagi menghasilkan apa-apa yang boleh diuji tanpa kerja data dahulu. Itu bukti berangka bahawa ruang peraturan hampir habis, bukan pendapat.

## AMARAN: pintu KALENDAR dan REJIM ialah peruntukan tunai yang disamarkan

`N101`-`N110` (kalendar dan rejim) berbeza daripada setiap baris lain dalam fail ini: ia tidak memilih SAHAM, ia memilih MASA. Ia menutup kedudukan pada tempoh tertentu dan membukanya pada tempoh lain.

Secara matematik itu ialah **peruntukan tunai**. Dan peruntukan tunai sudah diukur: `SISTEM.md` bahagian "Ujian penguasaan" mendapati campuran SPUS + tunai 0% diimbang bulanan memberi nisbah `CAGR / abs(MDD)` yang hampir **pemalar 0.642-0.669 merentas setiap berat** (100%, 60%, 40%, 35.4%, 30%). Pada pendedahan yang **sama**, SPUS mengalahkan sistem momentum Clenow pada **kedua-dua** paksi.

Maka pintu rejim dijangka **mengurangkan pulangan dan MDD bersama-sama** mengikut nisbah yang sama, bukan menambah alfa. Supaya ia bermakna, pintu rejim mesti menunjukkan nisbah `CAGR / abs(MDD)` yang **lebih tinggi daripada 0.669** - bukan sekadar MDD lebih cetek. Itu syarat lulusnya, dan ia mesti ditulis dalam pradaftar sebelum ujian dijalankan. Sistem B Clenow gagal tepat di sini: MDD-nya lulus dengan lega tetapi hanya kerana pendedahannya 35.4%.

## Tujuh paksi yang tidak pernah dienumerasi

MASUK, CARA, KELUAR dan URUTAN semuanya menjawab soalan **"saham mana dan bila"**. Tujuh paksi di bawah menjawab soalan yang berbeza, dan sebelum 30 Okt 2026 tiada satu pun pernah disenaraikan sebagai pilihan yang boleh diuji — walaupun beberapa daripadanya sudah **diukur secara kebetulan** dalam kajian lain.

Awalan dua aksara supaya tiada kolisi dengan M, N, K, X, C, U, S, P, L, I, A dan W yang sudah bermakna dalam repo ini.

### Gabungan signal (paksi KELIMA) — paksi yang paling penting

**GB01** — `DAN (persilangan): semua syarat mesti benar` · asas semua 147 MASUK (repo) · DIUJI · INI yang SETUP.md ukur: 0 daripada 598 lift positif, sebab STRUKTUR bukan pemilihan. Setiap syarat tambahan membuang lebih banyak bar, dan bar yang dibuang termasuk ekor kanan.

**GB02** — `ATAU (kesatuan): mana-mana satu syarat benar` · akibat logik SETUP.md (repo) · DIUJI · BELUM PERNAH DIUJI, dan ia secara struktur BERTENTANGAN dengan kegagalan yang diukur: kesatuan MENAMBAH bar, bukan membuang. Jika masalahnya "menapis membuang ekor", maka operasi yang betul ialah kesatuan, bukan persilangan. Ini teknik yang saya tertinggal. | DIUJI: terbaik GB02_atau2: lift +0.793 latih / +3.299 tahan, jangkaan +5.893%, n 93,416; 2/6 lulus gate3. KONFIGURASI UTAMA JEJAK HADAPAN: GB02_atau3 = N19 u N37 u N115 dengan keluar X13 memberi jangkaan tahan +8.541%, lift +4.191 tahan / +1.818 latih, menang 64.2%, untung +25.68%, rugi -22.14%, n 195,681, p 0.0068, dan tanpa5 = +2.858% iaitu POSITIF SECARA MUTLAK lawan asas X13 +0.912% - satu-satunya konfigurasi dalam seluruh kajian yang kelebihannya BERTAHAN selepas buang 5% pemenang teratas, halangan yang SETUP.md dapati 598/598 setup gagal. Gate0-gate3 LULUS kesemuanya (REVERSE/silang_akhir.csv). Dengan keluar X13 ia juga MENGALAHKAN kawalan RAWAK pada peringkat portfolio (16.12 lawan 14.23 pada 8 slot; 14.74 lawan 4.30 pada 40 slot), jadi dapatan "isyarat memusnahkan pemeringkat" E4/E5 khusus kepada keluar X15/X32, bukan am. HAD: portfolio TIDAK mengalahkan SPUS (CAGR 9.3-16.1%, MDD -22% hingga -63% lawan +17.95%/-26.82%, 0/36 lulus), jadi ia kohort setiap dagangan bukan peruntukan modal | PRODUKSI 1 Nov 2026: modul kod/kaedah/GB02.py berjalan setiap malam dalam Papertrade C; pradaftar jejak REVERSE/SPEC_JEJAK_N.md

**GB03** — `Undi k-daripada-n syarat benar` · ensemble klasik (umum) · DIUJI · k=1 ialah GB02, k=n ialah GB01; k di antaranya belum pernah diuji | DIUJI: terbaik GB03_undi4: lift +0.858 latih / +3.036 tahan, jangkaan +5.630%, n 85,575; 0/3 lulus gate3

**GB04** — `Agregat pangkat: purata pangkat merentas n signal -> satu skor` · ensemble klasik (umum) · DIUJI · menukar penapis menjadi URUTAN. SISTEM.md ukur urutan skor BERTERUSAN mempunyai sebaran benih 0.00 lawan SD 4.15 mata/tahun bagi susunan sewenang-wenang - jadi ini juga membaiki kebolehpercayaan keputusan, bukan hanya pulangan. | DIUJI: terbaik GB04_pangkat1: lift +0.023 latih / +1.813 tahan, jangkaan +4.407%, n 36,401; 0/4 lulus gate3

**GB05** — `Jumlah berpemberat sama bagi skor ternormal` · ensemble klasik (umum) · SEDIA

**GB06** — `Berat songsang-korelasi antara signal` · ensemble klasik (umum) · PERLU:korelasi_signal

**GB07** — `Hierarki: signal A tentukan ALAM, signal B tentukan URUTAN` · struktur (repo) · DIUJI · bukan penapis bertindan - setiap signal buat kerja BERBEZA, jadi ia tidak menambah pembuangan bar | DIUJI: hierarki signal A = ALAM, signal B = URUTAN (alam AL04 titik-masa 500): T1 0, T3 0, P2 0/60 - tetapi E6a LULUS, 19/48 sel mengalahkan asas pada KEDUA-DUA paksi. Saringan BERDIRI memperbaiki kedua-dua paksi (A1 tutup>ma200 +1.67/+1.47; A2 rs>=50 +4.26/+0.94; A3 rs>=80 +6.29/+0.23) sedangkan pintu masuk HARIAN memusnahkan pemeringkat (jurang 37.6 mata, E5). Bezanya KEKERAPAN bukan jenis: pintu harian beri 7.7-21.8 calon/sesi (kolam < slot), saringan berdiri beri 102-326 (kolam 13-41x slot). PERATURAN: kekalkan kolam calon >= ~10x bilangan slot. A4 (separuh ATR% rendah) beri lever MDD TERBESAR dalam kajian, +22.09 mata lebih cetek, tetapi -17.47 mata CAGR. Terbaik A2 x U14 x 8 slot x had 2: +53.15%/-57.56%, satu cabutan, BUKAN boleh didagang. SEMAKAN LUAR SAMPEL 1 Nov 2026 (SEMAKAN_LATIH.md): DISAHKAN tetapi magnitud RUNTUH - A2 +4.26 -> +0.64 mata CAGR dalam latih; yang bertahan ialah ARAH dan peraturan kolam, bukan nombor. A4 BUKAN pertukaran tulen di luar 2020-2025: dalam latih ia beri +18.62 mata MDD pada kos +0.16 mata CAGR, pada 100% sel. SEMAKAN SEMULA 1 Nov 2026 (semak_latih.py, ujian tanda berpasangan + BH-FDR): A3 dilapor 0.00/0.00 ialah ARTIFAK PENCAIRAN - 4 daripada 12 sel ialah A3 x U02 yang degenerat ikut binaan dan beri delta 0.00 TEPAT; pada 8 sel bukan-degenerat A3 beri +1.33 CAGR tetapi -1.74 MDD, jadi ia gagal R1 kerana TANDA BERTENTANGAN bukan kerana hilang (verdict tidak berubah). A4 ialah lever paling KUKUH dalam baris gilir: MDD mencetek pada 12/12 sel dalam KEDUA-DUA tingkap, p=0.0005 setiap satu, melepasi FDR; kos CAGR latih TEPAT NOL (6/12, p=1.000). A2 MDD latih juga melepasi FDR (+0.64, 8/8, p=0.0078)

**GB08** — `Penapis TERBALIK: buang yang terbukti rugi, bukan pilih yang terbukti untung` · akibat logik KOLAM_EKOR.md (repo) · DIUJI · pada taburan terpencong kanan, membuang ekor KIRI tidak menyentuh ekor KANAN. Itu operasi BERBEZA daripada memilih. KAEDAH_TERBAIK.md sudah kenal pasti 25 kaedah Mxx terbukti NEGATIF pada BH-FDR q <= 0.05 - senarai buang itu SUDAH ADA dan belum pernah diguna. | DIUJI: terbaik GB08_buang_buruk: lift +0.170 latih / +0.098 tahan, jangkaan +2.692%, n 3,167,080; 0/1 lulus gate3

### Saiz posisi (paksi KEENAM)

**SZ01** — `berat sama rata merentas slot` · asas repo (repo) · DIUJI · asas setiap lorong portfolio_slot kecuali RISIKO_10

**SZ02** — `pariti risiko Clenow: nilai = 0.001 x ekuiti / ATR%` · Clenow (buku) · DIUJI · Sistem B; memberi pendedahan 35.4% sahaja kerana ATR peneraju 5-6% (SISTEM.md)

**SZ03** — `risiko 1% / (4 x ATR14%), had 2-25%` · repo fasa 1b (repo) · DIUJI · RISIKO_10; DITOLAK untuk pulangan tetapi memperbaiki MDD 6/6 tahun (KEPUTUSAN_1B.md)

**SZ04** — `pecahan tetap f% ekuiti setiap posisi` · klasik (umum) · SEDIA

**SZ05** — `Kelly pecahan (f* x 0.25)` · Kelly / Thorp (buku) · PERLU:kelly · Kelly perlu anggaran kebarangkalian DAN nisbah untung/rugi. KOMBINASI.md ukur nisbah itu bergantung pada KELUAR (untung purata +4.06% dengan sasaran lawan +31.03% tanpa), jadi f* Kelly berubah dengan keluar BUKAN dengan masuk.

**SZ06** — `sasaran volatiliti portfolio (skala pendedahan ke vol sasaran)` · konsensus institusi (umum) · PERLU:vol_portfolio · AMARAN: ini mengubah PENDEDAHAN, jadi ia tertakluk kepada ujian penguasaan SISTEM.md - nisbah CAGR/abs(MDD) mesti melepasi 0.669

**SZ07** — `sumbangan risiko sama (ERC)` · Maillard, Roncalli & Teiletche (akademik) · PERLU:matriks_kovarians

**SZ08** — `Optimal f (Vince)` · Ralph Vince (buku) · PERLU:optimal_f · Vince sendiri beramaran ia memaksimumkan pertumbuhan geometri tetapi dengan drawdown melampau; pada sasaran MDD repo ia hampir pasti gagal

**SZ09** — `saiz berkadar dengan skor urutan` · struktur (repo) · SEDIA · menyambung paksi URUTAN kepada paksi SAIZ: skor tinggi dapat berat lebih besar

**SZ10** — `berat sama rata atas KOLAM PENUH, bukan 8-10 slot` · akibat logik KOLAM_EKOR.md (repo) · DIUJI · KOLAM_EKOR.md SUDAH ukur: kolam berat sama rata SELURUH memberi +1.64%/bulan manakala saham MEDIAN kolam memberi +0.82% dan SPY +1.82%. Jadi memegang SEMUA mengalahkan memilih 10 dengan 0.82 mata sebulan, tanpa apa-apa signal. Ini BELUM pernah diuji sebagai lorong ke hadapan, dan ia satu-satunya pembinaan yang menangkap ekor secara struktur. | DIUJI: berat sama rata kolam penuh diukur pada slot 1280 (melepasi kapasiti 753 bagi lorong berhad): CAGR 9.19-16.71%, MDD -37% hingga -43%. Lengkung slot memuncak pada 80-160 dan MEROSOT selepas itu, jadi kolam penuh BUKAN jawapannya

### Definisi alam (paksi KETUJUH)

**AL01** — `Release autotune-data-a02` · repo (repo) · DIUJI · SATU-SATUNYA alam yang pernah diguna dalam seluruh kajian. TIADA saham delist = bias survivorship (SPEC.md). Larangan A01 kekal: ia membuang saham meruap.

**AL02** — `konstituen skrin Syariah SPUS sahaja` · repo data/skrin/etf_shariah.csv (repo) · DIUJI · JURANG YANG PENTING: repo menapis belian melalui SPUS tetapi seluruh kajian REVERSE guna A02 penuh. Alam kajian dan alam dagangan BUKAN sama. | DIUJI: alam SPUS 214 ticker (SPTE dibuang - ETF global): T1 0, T3 0, tetapi isyarat mengalahkan kawalan rawak pada 46.2% sel. CAGR +2.69 mata dan MDD +6.19 mata lebih cetek daripada AL01 pada sel sepadan. Dapatan utama: tanpa5 = +2.682% (POSITIF buat kali pertama dalam kajian) lawan -0.081% pada AL01, dan 5% teratas membawa 47.9% jumlah pulangan lawan 101.7% - masalah EKOR ialah sifat alam a02, bukan hukum pasaran. HAD: keahlian SPUS semasa ditolak ke belakang, bias itu menghasilkan tepat kesan ini, jadi ia petunjuk bukan ukuran

**AL03** — `had harga minimum USD3` · konsensus screener (umum) · SEDIA

**AL04** — `N teratas ikut nilai dolar harian` · Qullamaggie / konsensus (blog) · DIUJI · lajur nilai20 sudah ada | DIUJI: N teratas ikut nilai dagangan 20 hari, TITIK-MASA (diagnostik pemalsuan E4, bukan sel grid dipradaftar): konfigurasi sama yang memberi +47.44%/-37.94% pada AL02 memberi +34.78%/-68.80% pada 214 teratas titik-masa dan +9.65%/-91.50% pada alam penuh. PULANGAN separa bertahan (kesan kausal nyata) tetapi RISIKO tidak: 30.9 mata kelebihan MDD AL02 hilang apabila keahlian dijadikan kausal. Setiap nombor AL02 dalam kajian ini menyanjung paksi risiko

**AL05** — `jalur permodalan pasaran (kecil / sederhana / besar)` · akademik faktor saiz (akademik) · PERLU:kapitalisasi · KOLAM_EKOR.md menunjukkan kadar asas kolam ialah pengikat; jalur saiz ialah cara paling terus mengubahnya

**AL06** — `keanggotaan indeks titik-masa (S&P 500 / Russell 1000 / 2000)` · konsensus (umum) · PERLU:keanggotaan

**AL07** — `umur IPO > 1 tahun (atau < 5 tahun untuk peneraju baharu)` · O’Neil / Minervini (buku) · PERLU:tarikh_ipo · sumber BERCANGGAH arah: beberapa pakar ELAK IPO baharu, yang lain MENCARI mereka

**AL08** — `had pendedahan sektor maksimum` · konsensus pengurusan risiko (umum) · SEDIA

### Tempoh pegang (paksi KELAPAN)

**PG01** — `5 sesi` · swing pendek (umum) · SEDIA

**PG02** — `10 sesi` · swing (umum) · DIUJI · KAEDAH_TERBAIK.md: hanya kumpulan <= 10 hari hampir matang (53% terbuka)

**PG03** — `21 sesi (~1 bulan)` · swing panjang (umum) · DIUJI · DIUJI: had 21 bar: CAGR terbaik +30.49% (80 slot), MDD -45.6%, kos 7.2 mata/tahun; T1/T3 gagal

**PG04** — `63 sesi (~3 bulan)` · asas kajian (repo) · DIUJI · asas SETUP.md dan KOMBINASI.md; keluar X03

**PG05** — `126 sesi (~6 bulan)` · momentum akademik (akademik) · SEDIA

**PG06** — `252 sesi (~1 tahun)` · kedudukan (umum) · SEDIA · K195 lapor pegangan purata ~305 hari = kedudukan, bukan swing

### Kekerapan imbang (paksi KESEMBILAN)

**IB01** — `pada isyarat sahaja (tiada imbang berkala)` · asas repo (repo) · DIUJI · asas Lejar Penuh dan setiap lorong portfolio_slot: posisi dibuka pada isyarat dan ditutup pada keluar, tanpa imbang berat di antaranya

**IB02** — `harian` · konsensus (umum) · SEDIA · kos dagangan paling tinggi

**IB03** — `mingguan` · konsensus (umum) · SEDIA

**IB04** — `bulanan` · Clenow / konsensus (buku) · DIUJI · Sistem B dan ujian penguasaan SPUS+tunai kedua-duanya bulanan

**IB05** — `jalur hanyut (imbang hanya bila berat tersasar > X%)` · QuantJourney W02/W12 (quantjourney-bt) · SEDIA · mengurangkan kos berbanding imbang berkala tetap

### Had kepekatan dan korelasi (paksi KESEPULUH)

**KR01** — `tiada had korelasi` · asas repo (repo) · DIUJI · 8-10 slot yang semuanya dalam satu industri = secara berkesan 2-3 slot. Belum pernah diukur dalam repo ini.

**KR02** — `had korelasi berpasangan maksimum antara pegangan` · konsensus pengurusan risiko (umum) · PERLU:matriks_kovarians

**KR03** — `had bilangan maksimum setiap industri` · konsensus (umum) · DIUJI · lajur industri sudah ada | DIUJI: had bilangan pegangan setiap industri, alam AL04 TITIK-MASA: T1 0, T3 0, P2 0/96 - tetapi E5a LULUS kedua-dua bahagian. Had 1 memperbaiki KEDUA-DUA paksi serentak: median +1.65 mata CAGR DAN +1.60 mata MDD lebih cetek lawan tiada had (had 2: +0.76/+0.02; had 3: +0.47/+0.00). DIPALSUKAN SEPARA 1 Nov 2026 oleh SEMAKAN_LATIH.md: kaki CAGR TIDAK bertahan dalam latih 2012-2019 (+1.65 -> -0.19) jadi ia artifak tingkap; kaki MDD BERTAHAN (+1.12, mencetek pada 83.3% sel latih). Rumusan betul: had industri ialah lever RISIKO yang hampir percuma, bukan lever dwi-arah. SEMAKAN SEMULA 1 Nov 2026 (semak_latih.py, ujian tanda berpasangan): +1.65 itu TIDAK PERNAH signifikan walaupun dalam tingkapnya sendiri - 16/24 sel, p=0.152 - jadi ia bukan kesan yang hilang luar sampel, ia kesan yang tidak pernah ada; kaki MDD sebaliknya MELEPASI BH-FDR pada tingkap luar sampel (+1.12, 20/23 sel, p=0.0005). Mekanisme: tanpa had, 6 daripada 8 slot boleh berada dalam SATU industri, jadi "8 slot" sebenarnya ~3 taruhan. Saiznya kecil jadi ia komponen bukan penyelesaian. MDD paling cetek dalam baris gilir muncul di sini: -28.97%, 2.15 mata daripada SPUS, tetapi CAGR cuma +10.41%

**KR04** — `kluster korelasi: satu pegangan setiap kluster` · konsensus (akademik) · PERLU:matriks_kovarians

### Instrumen (paksi KESEBELAS)

**IS01** — `saham tunggal` · asas repo (repo) · DIUJI · SETUP.md: dagangan median -5.19% tetapi min +3.03% = terpencong kanan teruk

**IS02** — `putaran ETF sektor` · konsensus (umum) · DIUJI · TITIK TENGAH yang belum diuji: SETUP.md mendapati SPY +3.356% dan QQQ +4.419% melepasi syarat ekor dengan mudah (menang ~77% lawan ~31%) kerana INDEKS ITULAH kepelbagaian merentas ekor. ETF sektor terletak antara saham tunggal (ekor teruk) dan SPUS (ekor baik). | DIUJI: putaran 11 bakul sektor sintetik berat sama rata (alam AL02): T1 0, T3 0. P1 26/40 tetapi P2 0/40 - MDD gagal pada SETIAP sel, paling cetek -31.61% lawan SPUS -26.82%. Pegang-semua k=11 beri +19.66%/-35.54%. HIPOTESIS SETUP.md DISAHKAN: tanpa5 bakul POSITIF pada 8/8 sel (+0.55% hingga +4.77%) lawan 0/598 setup saham - kepelbagaian merentas ekor memang membetulkan masalah ekor, tetapi masalah berpindah kepada DRAWDOWN. Bakul sintetik bukan ETF boleh dagang: tiada yuran, tiada ralat penjejakan

**IS03** — `SPUS + tunai diimbang bulanan` · ujian penguasaan SISTEM.md (repo) · DIUJI · INI YANG MENANG setakat ini: pada pendedahan sama ia mengalahkan Clenow pada KEDUA-DUA paksi. Nisbah CAGR/abs(MDD) hampir pemalar 0.642-0.669 merentas berat.

**IS04** — `campuran saham + ETF teras` · konsensus (umum) · SEDIA · teras ETF menangkap ekor, satelit saham menguji signal - belum pernah diuji

## Saluran rangkaian: apa yang boleh dicapai dalam sesi awan

Diuji 30 Okt 2026. Ini menentukan sumber mana yang boleh digunakan sekarang dan mana yang perlu dibenarkan dahulu.

**BERFUNGSI:** PyPI (`pip download` bagi mana-mana pakej), carian web.

**DISEKAT:** `arxiv.org` (DNS), `huggingface.co` (proksi 403 CONNECT tunnel), `quants.md` (DNS), `www.quantifiedstrategies.com` (DNS), `quantifiedstrategies.substack.com` (DNS).

Akibatnya **PyPI ialah saluran sumber yang paling boleh dipercayai**: pakej yang **membenamkan** definisinya dalam kod boleh dibaca, pakej yang **mengambil** datanya dari hos lain tidak. Itu sebab `openassetpricing` 0.1.0 dapat dimuat turun tetapi datanya tidak (`U07`), manakala `pandas_ta` dapat dibaca sepenuhnya.

## Sumber: apa yang setiap satu sebenarnya beri

**QuantJourney Backtester** (`quantjourney-bt` 0.12.5, Apache 2.0, PyPI) — ia sebuah **rangka kerja**, bukan katalog kelebihan. 50 contoh strateginya berjalan pada 3 ETF (SPY/QQQ/IWM) atau 9 ETF sektor, dan logik isyaratnya mudah (silang SMA, pembalikan RSI, Donchian, MACD, Bollinger). Nilai sebenarnya kepada repo ini ialah **mekanik pelaksanaan**: ia memodelkan MARKET, LIMIT, STOP, STOP_TRAIL, STOP_LIMIT, BRACKET dan OCO dengan luput-selepas-N-bar — kesemuanya `C02`-`C06` dan `X26`-`X29` di atas. Ia juga ada walk-forward dengan **purge + embargo** (`example_wf_03`), yang WFO repo tiada. **`example_wf_05` guna Optuna: JANGAN guna** — arahan kajian melarang Optuna dan apa-apa pengoptimum. Ia TIDAK ditambah sebagai kebergantungan repo: repo sudah ada enjinnya sendiri, dan dua enjin bermakna dua sumber kebenaran.

**pandas_ta** (`pandas-ta` 0.4.71b0, MIT, Kevin Johnson) — ~150 indikator terkod dalam 8 kategori (candle · momentum · trend · volatility · volume · overlap · cycle · statistics). Ia memberi `N81`-`N100`: TTM Squeeze Carter yang betul (BB dalam KC, bukan lebar BB), Connors RSI **tiga komponen** (repo hanya ada `rsi2`), AlphaTrend, Schaff Trend Cycle, QQE, Vortex, VHF, Elder Force Index, Elder Ray, Klinger, Time Segmented Volume, Alligator, Fisher Transform, Pretty Good Oscillator, Choppiness, Random Walk Index, Coppock, KST, ATR Trailing Stop, TMO. **JANGAN pasang sebagai kebergantungan:** ia memerlukan `numba==0.61.2` yang memaksa `numpy<2.3`, sedangkan persekitaran repo ialah numpy 2.5.3 + pandas 3.0.5 — pemasangan akan MENURUNKAN taraf numpy dan berisiko merosakkan workflow malam. Guna ia sebagai **rujukan spesifikasi** (lesen MIT membenarkan, dengan atribusi) dan laksanakan indikator yang diperlukan terus dalam `REVERSE/teras/ind.py`, sama seperti 71 lajur yang lain.

**AMARAN STRUKTUR tentang N81-N100.** Kedua puluh ini ialah **penapis**, dan ruang penapis sudah diukur: `SETUP.md` mendapati **0 daripada 598** setup mempunyai lift positif, dengan sebab **struktur** bukan pemilihan. Menambah 20 penapis lagi dijangka gagal dengan cara yang sama. Ia didaftar supaya ia tidak dicari lagi, bukan kerana saya menjangka ia lulus. **Yang berbeza secara jenis ialah `U06`-`U08` (urutan) dan `C02`-`C06` (cara) — bukan indikator lagi.**

**GTJA 191 Alphas** (Guotai Junan Securities, 2017) — `U12`, dan **dapatan terkuat sapuan keenam**. 191 formula eksplisit daripada harga, volum, volatiliti dan VWAP, keluarga yang sama seperti `U06` (skor peringkat, bukan penapis boolean). Sebabnya ia terkuat: satu kertas 2026 melaporkan **17 daripada 191 masih menambah kuasa penerangan bagi pulangan saham AS selepas mengawal 151 faktor fundamental lain**. Itu bukti kuantitatif **luaran** pertama bagi kemandirian mana-mana katalog dalam fail ini — setiap sumber lain hanya mendakwa. Ia direka untuk A-share China, dan laporan asal 2017 tidak ditemui dalam carian, jadi formula **belum dibaca**.

**TA-Lib / pandas_ta candlestick** — `N131`. 62 pola lilin bernama dan terkod; repo kini ada **dua** (`hammer`, `bullish_engulfing`). Didaftar sebagai SATU baris kerana metadatanya sama, tetapi **ia 62 ujian berasingan dan FDR mesti mengira 62** — nota barisnya menyenaraikan kesemuanya.

**Data yang repo SUDAH ada aksesnya tetapi belum guna** — `N143` nisbah put/call (Alpha Vantage `HISTORICAL_PUT_CALL_RATIO`), `N147` belian balik (Moomoo `quote_corporate_actions_buybacks`), `N146` 13F (alat pemegang institusi Moomoo), `N145` semakan analis (FMP `analyst`). Ini bukan masalah akses, ia masalah belum dikumpul sebagai siri titik-masa.

**Buku dengan peraturan harian yang tepat** (sapuan 30 Okt 2026) — `Street Smarts` (Connors & Raschke 1995) memberi `N111`-`N116` dan `X33`: Turtle Soup, Turtle Soup Plus One, 80-20, Momentum Pinball, Holy Grail, ID/NR4. `Short-Term Trading Strategies That Work` dan `High Probability ETF Trading` (Connors & Alvarez) memberi `N117`-`N119` dan `X34`. `Trade Like a Stock Market Wizard` (Minervini) memberi `N120` (Trend Template, 8 syarat). Weinstein memberi `N121`. **Teks buku belum dibaca dalam sesi ini** - semuanya daripada ringkasan dan skrip pihak ketiga, dan sumber sekunder bercanggah pada beberapa ambang (umur ekstrem Turtle Soup 3 atau 4 bar; rendah 52w Minervini 25% atau 30%). Setiap percanggahan direkod dalam nota barisnya.

**Qullamaggie** — `N122`, `N124`, `U09`-`U11`. **Pembetulan:** saya menyangka ambang nilai dolar $20 juta; angka itu TIDAK muncul dalam mana-mana sumber. Yang paling konsisten ialah **$10 juta**, dan satu sumber memberi peraturan berbeza sama sekali ("50x saiz akaun"). ADR% yang ia guna ialah **julat purata**, bukan `atr_pct` repo yang julat BENAR - dua perkara berbeza.

**Zarattini, Barbon & Aziz (ORB)** — `N130`, `C10`, `X41`. Repo **tiada bar intrahari**, jadi ia tidak boleh diuji di sini. Lebih penting: replikasi bebas pada lima indeks melaporkan kelebihan **kasar** berulang tetapi pulangan **bersih hampir SIFAR** selepas kos dagangan. Didaftar dengan amaran itu.

**Quantpedia** — sudah menjadi sumber dalam repo ini sejak Okt 2026: `spec/KATALOG_K145.md` memetiknya bagi K195, K241, K242 dan K270. Populasinya ialah **strategi faktor/portfolio akademik**, kebanyakannya pangkat keratan rentas yang diimbang bulanan atau suku tahunan. Itu paksi **pembinaan**, yang `REVERSE/PEMBINAAN.md` sudah ukur dan tolak lawan SPUS. Jadi Quantpedia akan menambah banyak strategi, tetapi kebanyakannya dalam paksi yang sudah ditutup. Yang berasaskan bar OHLCV harian masuk ke sini (contoh `N80`); yang berasaskan faktor bulanan kekal dalam katalog K.

**Quantified Strategies** — `www.quantifiedstrategies.com` dan `quantifiedstrategies.substack.com` KEDUA-DUANYA tidak dapat diselesaikan (DNS) dalam sesi awan ini. `N16`, `N18` dan `X07` didaftar daripada ringkasan carian web, BUKAN daripada teks penuh sumber. Untuk peraturan penuh, domain itu perlu dibenarkan dalam tetapan rangkaian sesi.

**quants.md** — tidak dapat diselesaikan (DNS) dalam sesi ini; belum dinilai. Perlu dibenarkan dalam tetapan rangkaian sesi sebelum apa-apa daripadanya boleh didaftar.

## Sempadan K / M / N

Tiga katalog, tiga populasi berbeza. Jangan campur.

- **K1-K397** (`spec/KATALOG_K145.md`) — calon kaedah daripada kajian dalam talian dan akademik, termasuk Quantpedia. 47 daripadanya menjadi M115-M161.
- **Mxx** (`spec/SPEC_SEMUA_KAEDAH.md`, `kod/kaedah/`) — kaedah lengkap yang sudah dikodkan dan dijalankan setiap malam dalam Lejar Penuh.
- **Nxx** (fail ini) — kombinasi indikator gaya pedagang pada bar harian, didaftar dahulu dan diuji kemudian, dengan paksi `CARA` yang K dan M tiada.

## Cara menguji

1. Pradaftar: tulis `REVERSE/SPEC_<nama>.md` dengan senarai id yang akan diuji, pecahan LATIH/TAHAN, dan jangkaan priori. Komit sebelum larian.
2. Kira lift lawan asas keluar yang sama (bukan jangkaan mutlak — kesilapan `SPEC_SETUP.md` §4).
3. Syarat lulus: lift positif pada KEDUA-DUA tingkap, BH-FDR q <= 0.05 merentas bilangan ujian yang dipradaftar, dan jangkaan selepas buang 5% teratas kekal positif.
4. Setakat ini hanya `N01` (MA10 silang MA20 + volum >= 1.2x) mencapai syarat 1 dan 2; tiada satu pun mencapai syarat 3.
