# Imbas pasaran 8:02 malam MYT (Isnin–Jumaat)

Automatik; jangan tanya soalan. Peraturan: `standard/tugasan_v3.md`, skema: `papertrade/SKEMA.md`, kod: `kod/` (`scanner.py`, `kaedah/Mxx.py`).
Tugasan belian bermula 9:35 pagi New York: siapkan `senarai_beli.csv` dahulu (sasaran < 30 minit) dan push sebelum watchlist.

Alat: `select:mcp__Moo_Moo__quote_market_state,mcp__Moo_Moo__quote_trading_days,mcp__Moo_Moo__quote_stock_screen,mcp__Moo_Moo__quote_history_kline,mcp__Moo_Moo__quote_stock_quote` dan `select:ArtifactData`.

0. `git pull --rebase origin main`. Pasaran AS hari ini (waktu New York) tidak dibuka → catat "cuti" dalam `standard/binaan_v2_log.md`, commit + push, berhenti.
1. Baca `papertrade/moomoo.csv`, semua `papertrade/claude*.csv`, `papertrade/watchlist.csv`.
2. Data pasaran: `quote_stock_screen`
   - screen_queries = [{"simple_field_query":{"simple_field":1,"screen_value_list":[2]}},{"simple_field_query":{"simple_field":10,"screen_value_list":[1]}},{"simple_property_query":{"property":{"name":2201},"lower":{"value":10000,"includes":true}}}]
   - retrieve_queries = [{"basic_property":{"name":1101}},{"simple_property":{"name":2202}},{"simple_property":{"name":2204}},{"simple_property":{"name":2205}},{"simple_property":{"name":2201}},{"cumulative_property":{"name":3104,"days":1}},{"financial_property":{"name":4903,"term":10}}]
   - limit 250, ulang dengan next_key sehingga has_more=false. Kemudian kline US.SPY dan US.QQQ (num 370). Kline saham hanya untuk calon yang perlu (maks 24).
3. Semak semula watchlist (tugasan_v3 §3): 90–99% kekal (kemas kini); 100% dan sah → senarai beli (keluarkan dari watchlist); terkeluar signal → BUANG.
4. Imbas 87 kaedah: isyarat 100% dan sah (§3 a, b) → `papertrade/senarai_beli.csv` (lajur ikut SKEMA, destinasi = Claude, tarikh_imbasan = hari ini MYT). Calon baharu 90–99% → watchlist (maks 5 setiap kaedah).
5. Sektor & industri wajib bagi setiap baris.
5b. GRED (tugasan_v3 §8) — selepas senarai_beli.csv ditulis dan di-push (belian tidak boleh tertangguh kerana gred):
   - Alat tambahan: `select:mcp__SST_Terminal__market_events,mcp__SST_Terminal__search_news,mcp__SST_Terminal__institutional_flow,mcp__Moo_Moo__quote_news_search,mcp__Moo_Moo__quote_financials_earnings_price_history`.
   - `market_events` (market US, daysLookahead 30) → simpan fail JSON.
   - Bagi saham unik senarai beli (maks 80, keutamaan RS tertinggi): `quote_news_search` (symbol = ticker, size 10, sort_type 2, lang en) dan `quote_financials_earnings_price_history` (US.ticker; ringkaskan dengan `python3 BacktestShariah2/standard/gred.py earnings <fail> --tarikh <hari ini>`). `institutional_flow` sekali. Bina `pemangkin.json` = {ticker: {berita: [{tajuk, hari_lalu}], earnings_lalu_hari, earnings_gerak_pct, earnings_anggaran, institusi: 'kumpul'|'agih'|null}} dengan Python. Baki > 80 → gred_pemangkin "–" (catat).
   - `python3 BacktestShariah2/standard/gred.py tambah --csv BacktestShariah2/papertrade/senarai_beli.csv --harga <folder stor harga> --sektor BacktestShariah2/papertrade/sektor.csv --pasaran BacktestShariah2/papertrade/sektor_pasaran.csv --peta BacktestShariah2/papertrade/peta_industri.csv --acara <market_events.json> --pemangkin <pemangkin.json> --tarikh <hari ini>`; ulang untuk `watchlist.csv` (tanpa --pemangkin). Commit + push semula.
6. `python3 BacktestShariah2/standard/sahkan.py` → mesti 0.
7. Tulis CSV; tolak `papertrade/senarai_beli` dan `papertrade/watchlist` ke db dashboard (setiap baris db membawa lajur gred dengan nama yang sama seperti CSV; halaman memaparkan lajur S, I, R, P, Q dan Gred keseluruhan, satu lajur setiap satu).
8. Catatan dalam `standard/binaan_v2_log.md`: masa siap, bilangan senarai beli, watchlist dibuang/baharu, isyarat mingguan ditolak. Commit `Imbas 8:02 malam <tarikh>: <ringkas>` + push (push selepas setiap fail penting juga).
