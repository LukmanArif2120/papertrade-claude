# Papertrade Claude (Backtest Shariah 2)

Repo ini menggantikan Project claude.ai "Backtest Shariah 2" sebagai stor utama mulai 14 Okt 2026. Baca `BacktestShariah2/00_NOTA_SERAHAN.md` dan `BacktestShariah2/standard/tugasan_v2.md` dahulu.

## Struktur
- `BacktestShariah2/standard/` — peraturan (tugasan_v2.md, papertrade_harian.md, dashboard.md), log (binaan_v2_log.md, binaan_v2_log_tambahan.md), skrip harian dan enjin P01/P02, sumber halaman dashboard_v2.html.
- `BacktestShariah2/papertrade/` — moomoo.csv, claude.csv, claude_2.csv (… claude_N.csv), senarai_beli.csv, watchlist.csv, sektor.csv.
- `BacktestShariah2/spec/SPEC_SEMUA_KAEDAH.md` — semua spec (cari tanda `FAIL ASAL`).
- `BacktestShariah2/laporan/`, `BacktestShariah2/data/` (registry gabungan, P01/P02), `BacktestShariah2/uji_kertas/log.csv`.
- `data_mentah/` — dataset_S1–S4.csv, index_benchmark.csv (data backtest).

Laluan lama dalam dokumen (`standard/x`, `papertrade/x`, `spec/`) = `BacktestShariah2/standard/x`, `BacktestShariah2/papertrade/x`, `BacktestShariah2/spec/SPEC_SEMUA_KAEDAH.md`.

## Peraturan
- Dashboard: artifact sedia ada https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (db melalui ArtifactData). Jangan cipta artifact baharu. Kod kaedah, stor harga dan status harian kekal dalam aset/db dashboard.
- Papertrade C (Claude, maya) sahaja untuk belian baharu sejak 13 Okt 2026. Tiada order Moomoo, tiada wang sebenar.
- "Kalau tak beli, cakap tak beli." Data mesti betul; jangan reka.
- Penerangan teknikal dalam Bahasa Melayu baku.
- Setiap larian berjadual: `git pull --rebase` dahulu, tulis fail di repo ini, kemudian commit dan push ke `main`. Jangan tulis lagi ke Project claude.ai (salinan di sana dibekukan pada 14 Okt 2026).
