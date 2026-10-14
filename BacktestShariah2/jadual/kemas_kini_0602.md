# Kemas kini 6:02 pagi MYT (Selasa–Sabtu)

Automatik; jangan tanya soalan. Peraturan: `standard/tugasan_v3.md` (baca dahulu), skema: `papertrade/SKEMA.md`.

Alat (ToolSearch, satu panggilan setiap kumpulan):
- `select:mcp__Moo_Moo__quote_market_state,mcp__Moo_Moo__quote_trading_days,mcp__Moo_Moo__sim_trade_position_list,mcp__Moo_Moo__quote_stock_quote,mcp__Moo_Moo__quote_history_kline,mcp__Moo_Moo__quote_stock_screen,mcp__Moo_Moo__quote_owner_plate`
- `select:mcp__SST_Terminal__sector_rotation,mcp__SST_Terminal__industry_rotation,mcp__SST_Terminal__market_heatmap,mcp__SST_Terminal__sector_summary,mcp__SST_Terminal__get_stock`
- `select:ArtifactData`

0. `git pull --rebase origin main`. Semak kalendar NYSE: sesi AS semalam cuti → catat dalam `standard/binaan_v2_log.md`, commit + push, berhenti.
1. Baca `papertrade/moomoo.csv`, semua `papertrade/claude*.csv`, `papertrade/sektor.csv`, `papertrade/watchlist.csv`. `sim_trade_position_list` acc_id "4135388", market 100: selaraskan dengan moomoo.csv (perbezaan dan qty > 1 dicatat dalam log, bukan dalam CSV). Jangan ubah posisi Moomoo.
2. Posisi BELUM keluar yang dibeli (M dan semua claude*; langkau tidak_dibeli): harga tutup terkini, untung %, hari dipegang, nilai keluar (tugasan_v3 §5.3). Keluar → isi tarikh/harga keluar, untung akhir, keluar=True (dibekukan). Isi harga keluar baris "menunggu" semalam (= buka hari ini). Semakan kesahihan belian semalam (§5.4). Betulkan harga beli sementara (§5.2).
3. Posisi sudah keluar: tidak dikemas kini (kecuali sektor/industri kosong).
4. Watchlist: muat stor harga (aset dashboard `harian/status` → `harga_aset` A/B/idx) dan tambah bar tutup semalam (`kod/scanner.py harga` dengan skrin Moomoo; kline untuk calon yang perlu, maks 24). Nilai semula setiap baris:
   - 90–99% → kekal, kemas kini % hampir, harga, paras pencetus;
   - 100% → kekal (dipindah oleh imbasan 8:02 malam);
   - terkeluar signal → BUANG.
   Tiada calon baharu pada 6:02. Data tidak dapat diambil → kekalkan baris dan catat; jangan reka.
5. Sektor & industri: isi yang kosong (§5.6); snapshot hari ini (SST sector_rotation, industry_rotation, market_heatmap, sector_summary) → tambah ke `papertrade/sektor.csv`; pendedahan posisi aktif sah mengikut sektor/industri bagi M, C, Combine.
6. Prestasi (tugasan_v3 §7).
7. `python3 BacktestShariah2/standard/sahkan.py --betulkan` → mesti 0 (§5.5).
8. Tulis CSV ke laluan sama; tolak ke db dashboard: `papertrade/moomoo`, `papertrade/claude` … `_6`, `papertrade/watchlist`, `sektor/snapshot`, `prestasi/mae`, `prestasi/ringkasan`, `harian/status` (kemaskini_pagi).
9. Catatan dalam `standard/binaan_v2_log_tambahan.md`: keluar baharu, tidak dibeli baharu, watchlist dibuang, keputusan sahkan.py. Commit `Kemas kini 6:02 pagi <tarikh>: <ringkas>` + push.
