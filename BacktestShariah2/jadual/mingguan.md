# Data Moomoo/SST mingguan (sesi Claude BAHARU; aktif selepas peralihan, lihat `PERALIHAN.md`)

Masa: Ahad 10:47 pagi MYT (pasaran AS tutup; data tutup Jumaat). Model `claude-sonnet-5-5`. Automatik; jangan tanya soalan.
LARANGAN: tiada order (`trading_order_*`, `sim_trade_input/modify/cancel_order`); hook projek menyekatnya.
Keputusan pengguna 17 Okt 2026: data yang hanya Moomoo/SST boleh beri dikumpul SEMINGGU SEKALI; selebihnya GitHub Actions.
Hasil alat besar disimpan ke fail oleh sistem — proses dengan Python; jangan salin data ke dalam jawapan.

Alat (ToolSearch; jika `select:mcp__Moo_Moo__…` gagal, cari ikut nama alat, cth. "quote_stock_screen"):
`select:mcp__Moo_Moo__quote_stock_screen,mcp__Moo_Moo__quote_plate_list,mcp__Moo_Moo__quote_plate_stock,mcp__Moo_Moo__sim_trade_position_list`,
`select:mcp__SST_Terminal__market_events,mcp__SST_Terminal__institutional_flow,mcp__SST_Terminal__unusual_volume`,
`select:ArtifactData,PushNotification`.

1. `git pull --rebase origin main`.
2. Universe Shariah (skrin Moomoo; screen_queries & retrieve_queries sama seperti `jadual/imbas_2002.md` langkah 2, limit 250,
   ulang next_key hingga has_more=false). `python3 BacktestShariah2/kod/parse_screen.py BacktestShariah2/data/harga/univ.csv <fail…>`,
   kemudian tulis semua ticker (tanpa `US.`) ke `BacktestShariah2/data/harga/univ.txt` (Actions mengimbas universe ini dan
   menarik harganya; `univ.csv` memberi nama syarikat). Kurang daripada 800 ticker → jangan tulis; catat ralat.
3. Peta industri: jika `papertrade/peta_industri.csv` lebih 30 hari, bina semula seperti `jadual/kemas_kini_0602.md` 5(b).
4. Sektor seluruh pasaran AS: skrin semua saham AS ≥ USD5 (arahan dalam kepala `standard/sektor_pasaran.py`, ~21 halaman × 300),
   `python3 BacktestShariah2/standard/sektor_pasaran.py --skrin <fail…> --peta BacktestShariah2/papertrade/peta_industri.csv
   --tarikh <tutup Jumaat> --out BacktestShariah2/papertrade/sektor_pasaran.csv --json <scratchpad>/sektor_pasaran.json`.
5. SST: `institutional_flow` dan `unusual_volume` (market US) → simpan JSON di `BacktestShariah2/data/sst/`;
   `market_events` (market US, daysLookahead 40) → `BacktestShariah2/data/pemangkin/market_events.json` (gred QR; dipakai
   Actions sehingga 9 hari). Ralat SST → langkau dan catat.
6. Snapshot sektor dashboard: `ArtifactData get` `sektor/snapshot` dengan out_dir (fail lama), kemudian
   `python3 BacktestShariah2/standard/snapshot_sektor_db.py --pasaran <sektor_pasaran.json> --lama <fail lama>
   --peta BacktestShariah2/papertrade/peta_industri.csv --papertrade BacktestShariah2/papertrade --dibina "<YYYY-MM-DD HH:MM> MYT"
   --out BacktestShariah2/data/db/sektor_snapshot.json` (jana_db.py menolaknya bersama dokumen harian).
7. Akaun simulasi Moomoo (baca sahaja): `sim_trade_position_list` acc_id "4135388", market 100; bandingkan dengan posisi aktif
   `papertrade/moomoo.csv`; catat perbezaan dalam log (jangan ubah CSV, jangan jual).
8. `python3 BacktestShariah2/standard/sahkan.py` → mesti 0. Catatan dalam `standard/binaan_v2_log.md`
   (bilangan universe, sektor_pasaran, SST, perbezaan Moomoo). Commit `Mingguan Moomoo/SST <tarikh>: <ringkas>` + push.
9. Notifikasi (langkah terakhir, juga jika gagal): `PushNotification`, status "proactive", satu baris < 200 aksara:
   `Mingguan <tarikh>: universe <n>, sektor <tarikh>, SST <ok/ralat>, Moomoo <beza>`.
