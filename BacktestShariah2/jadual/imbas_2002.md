# Imbas pasaran 8:02 malam MYT (Isnin–Jumaat)

Automatik; jangan tanya soalan. Peraturan: `standard/tugasan_v3.md`, skema: `papertrade/SKEMA.md`, kod: `kod/` (`scanner.py`, `kaedah/Mxx.py`).
Tugasan belian bermula 9:35 pagi New York: siapkan `senarai_beli.csv` dahulu (sasaran < 30 minit) dan push sebelum watchlist.

Alat: `select:mcp__Moo_Moo__quote_market_state,mcp__Moo_Moo__quote_trading_days,mcp__Moo_Moo__quote_stock_screen,mcp__Moo_Moo__quote_history_kline,mcp__Moo_Moo__quote_stock_quote` dan `select:ArtifactData`.

0. `git pull --rebase origin main`. Pasaran AS hari ini (waktu New York) tidak dibuka → catat "cuti" dalam `standard/binaan_v2_log.md`, commit + push, berhenti.
1. Baca `papertrade/moomoo.csv`, semua `papertrade/claude*.csv`, `papertrade/watchlist.csv`.
2. Data pasaran: `quote_stock_screen`
   - screen_queries = [{"simple_field_query":{"simple_field":1,"screen_value_list":[2]}},{"simple_field_query":{"simple_field":10,"screen_value_list":[1]}},{"simple_property_query":{"property":{"name":2201},"lower":{"value":10000,"includes":true}}}]
   - retrieve_queries = [{"basic_property":{"name":1101}},{"simple_property":{"name":2202}},{"simple_property":{"name":2204}},{"simple_property":{"name":2205}},{"simple_property":{"name":2201}},{"cumulative_property":{"name":3104,"days":1}},{"financial_property":{"name":4903,"term":10}}]
   - limit 250, ulang dengan next_key sehingga has_more=false. Tulis semua ticker skrin (tanpa `US.`, satu baris setiap satu) ke `data/harga/univ.txt` supaya Actions harga harian meliputi universe Shariah. Kemudian kline US.SPY dan US.QQQ (num 370). Kline saham hanya untuk calon yang perlu (maks 24).
3. Semak semula watchlist (tugasan_v3 §3): 90–99% kekal (kemas kini); 100% dan sah → senarai beli (keluarkan dari watchlist); terkeluar signal → BUANG.
4. Imbas 87 kaedah: isyarat 100% dan sah (§3 a, b) → `papertrade/senarai_beli.csv` (lajur ikut SKEMA, destinasi = Claude, tarikh_imbasan = hari ini MYT). Calon baharu 90–99% → watchlist (maks 5 setiap kaedah).
5. Sektor & industri wajib bagi setiap baris.
5b. GRED (tugasan_v3 §8) — selepas senarai_beli.csv ditulis dan di-push (belian tidak boleh tertangguh kerana gred):
   - Alat tambahan: `select:mcp__SST_Terminal__market_events,mcp__SST_Terminal__search_news,mcp__SST_Terminal__institutional_flow,mcp__Moo_Moo__quote_news_search,mcp__Moo_Moo__quote_financials_earnings_price_history`.
   - `market_events` (market US, daysLookahead 30) → simpan fail JSON.
   - Peringkat 1 (S, I, R, Q; wajib): `python3 BacktestShariah2/standard/gred.py tambah --csv BacktestShariah2/papertrade/senarai_beli.csv --harga <folder stor harga> --sektor BacktestShariah2/papertrade/sektor.csv --pasaran BacktestShariah2/papertrade/sektor_pasaran.csv --peta BacktestShariah2/papertrade/peta_industri.csv --acara <market_events.json> --tarikh <hari ini>`; ulang untuk `watchlist.csv`. Commit + push serta-merta.
   - Peringkat 2 (P, pemangkin): bagi saham unik senarai beli, keutamaan RS tertinggi, MAKS 40 saham, dan BERHENTI mengumpul pada 9:10 malam MYT (belian 9:35 NY menyalin gred): `quote_news_search` (symbol = ticker, size 10, sort_type 2, lang en; simpan tajuk, hari_lalu DAN url artikel) dan `quote_financials_earnings_price_history` (US.ticker; ringkaskan dengan `python3 BacktestShariah2/standard/gred.py earnings <fail> --tarikh <hari ini>`). `institutional_flow` sekali. Bina `pemangkin.json` = {ticker: {berita: [{tajuk, hari_lalu, url}], earnings_lalu_hari, earnings_gerak_pct, earnings_anggaran, institusi: 'kumpul'|'agih'|null}} dengan Python (url diambil tepat daripada hasil alat; jangan reka). Jalankan semula `gred.py tambah` untuk senarai_beli.csv dengan `--pemangkin pemangkin.json` (mengisi gred_pemangkin, pemangkin dan pemangkin_url); commit + push sebelum 9:25 malam MYT. Saham yang tidak sempat → gred_pemangkin "–" (catat bilangan dalam log).
6. `python3 BacktestShariah2/standard/sahkan.py` → mesti 0.
7. Tulis CSV; tolak `papertrade/senarai_beli` dan `papertrade/watchlist` ke db dashboard (setiap baris db WAJIB membawa semua lajur gred yang berisi, dengan nama sama seperti CSV: sektor_us, industri_us, gred_sektor, skor_sektor, gred_industri, skor_industri, rs_rating, gred_rs, gred_pemangkin, mata_pemangkin, pemangkin, pemangkin_url, tarikh_earnings, hari_ke_earnings, sumber_earnings, gred_qr, gred_keseluruhan, gred_pada; medan kosong boleh ditinggalkan, medan berisi tidak boleh dibuang untuk jimat ruang; halaman memaparkan lajur S, I, R, P, Q dan Gred keseluruhan, satu lajur setiap satu).
8. Catatan dalam `standard/binaan_v2_log.md`: masa siap, bilangan senarai beli, watchlist dibuang/baharu, isyarat mingguan ditolak. Commit `Imbas 8:02 malam <tarikh>: <ringkas>` + push (push selepas setiap fail penting juga).
