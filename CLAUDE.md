# Papertrade Claude (Backtest Shariah 2)

Repo ini menggantikan Project claude.ai "Backtest Shariah 2" sebagai stor utama mulai 14 Okt 2026. Baca `BacktestShariah2/00_NOTA_SERAHAN.md` (latar belakang) dan `BacktestShariah2/standard/tugasan_v3.md` (peraturan tunggal harian) dahulu. `tugasan_v2.md` dan `papertrade_harian.md` TERBATAL.

## Struktur
- `BacktestShariah2/standard/` — peraturan (tugasan_v3.md; dashboard.md), log (binaan_v2_log.md, binaan_v2_log_tambahan.md), skrip harian, `sahkan.py` (semakan data), `bungkus_kod.py`, enjin P01/P02, sumber halaman dashboard_v2.html.
- `BacktestShariah2/jadual/` — prosedur tiga tugasan berjadual (6:02 pagi, 7:47 malam, 9:35 NY).
- `BacktestShariah2/kod/` — kod teras (scanner, enjin v1.2, kaedah/Mxx.py). Sumber kebenaran; aset kod dashboard hanya salinan.
- `BacktestShariah2/ujian/` — ujian unit: `python3 -m unittest discover -s BacktestShariah2/ujian`.
- `BacktestShariah2/papertrade/` — moomoo.csv, claude.csv, claude_2.csv (… claude_N.csv), senarai_beli.csv, watchlist.csv, sektor.csv. Skema: `papertrade/SKEMA.md`.
- `BacktestShariah2/spec/SPEC_SEMUA_KAEDAH.md` — semua spec (cari tanda `FAIL ASAL`).
- `BacktestShariah2/laporan/`, `BacktestShariah2/data/` (registry gabungan, P01/P02), `BacktestShariah2/uji_kertas/log.csv`.
- `data_mentah/` — dataset_S1–S4.csv, index_benchmark.csv (data backtest).

Laluan lama dalam dokumen (`standard/x`, `papertrade/x`, `spec/`) = `BacktestShariah2/standard/x`, `BacktestShariah2/papertrade/x`, `BacktestShariah2/spec/SPEC_SEMUA_KAEDAH.md`.

## Peraturan
- Dashboard: artifact sedia ada https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (db melalui ArtifactData). Jangan cipta artifact baharu. Stor harga dan status harian kekal dalam aset/db dashboard. Kod kaedah: sumber di `BacktestShariah2/kod/`, aset kod dashboard ialah salinan (lihat `kod/README.md`).
- Papertrade C (Claude, maya) sahaja untuk belian baharu sejak 13 Okt 2026. Tiada order Moomoo, tiada wang sebenar.
- "Kalau tak beli, cakap tak beli." Data mesti betul; jangan reka.
- Penerangan teknikal dalam Bahasa Melayu baku.
- Setiap larian berjadual: `git pull --rebase` dahulu, tulis fail di repo ini, kemudian commit dan push ke `main`. Jangan tulis lagi ke Project claude.ai (salinan di sana dibekukan pada 14 Okt 2026).
- Sebelum push data: `python3 BacktestShariah2/standard/sahkan.py --betulkan` mesti keluar 0.
- Automasi (sejak 16 Okt 2026): `.claude/settings.json` menyekat semua alat order (hook PreToolUse) dan memasang `requirements.txt` dalam sesi awan (SessionStart); `.github/workflows/semak_data.yml` menjalankan ujian unit dan `sahkan.py` pada setiap push ke `main`. Jangan buang atau longgarkan.
- Notifikasi telefon (permintaan pengguna 16 Okt 2026): dalam SETIAP sesi/chat, pada akhir setiap giliran yang menyiapkan tugasan atau memerlukan keputusan pengguna, muatkan `select:PushNotification` (ToolSearch) dan hantar satu baris < 200 aksara, status "proactive", yang menyatakan hasil atau apa yang perlu pengguna buat. Abaikan jika keputusan alat "not sent".
- Tugasan berjadual guna model Sonnet 5.5 sahaja.
- Rutin berjadual (sejak 14 Okt 2026) menembak ke sesi Sonnet yang sudah dilampirkan repo ini; jangan guna `add_repo`. Dalam sesi itu alat Moomoo/SST mungkin berawalan lain (cth. `mcp__da8be8b4-…__quote_stock_quote`, bukan `mcp__Moo_Moo__…`): jika `select:mcp__Moo_Moo__…` gagal, cari dengan ToolSearch kata kunci nama alat (cth. "quote_stock_quote") dan guna alat yang ditemui. Larangan order terpakai tanpa mengira awalan.
