# WFO — Walk-forward optimization kaedah M (W01)

Kerja kajian berasingan daripada rutin harian Papertrade C. Tiada fail dalam `BacktestShariah2/` diubah; enjin v1.2 dan modul kaedah dibaca sahaja.

- `spec/SPEC_WFO_SISTEM_SWING.md` — spec W01.
- `kod/wfo.py` — larian WFO (`python3 WFO/kod/wfo.py senarai | kelompok 5 | jalan Mxx | w01`).
- `kod/wfo_laporan.py` — laporan Fasa C → `laporan/W01_LAPORAN.md`.
- `kod/enjin_laju.py` — salinan numba `trades()`/`portfolio()` enjin v1.2, setara bait demi bait (termasuk penjumlahan `sum()` Python). Lalai dalam `wfo.py`; `WFO_ENJIN=asal` memakai enjin v1.2 asal. Perlu pakej `numba`.
- `kod/sahkan_enjin.py` — sahkan enjin laju lawan v1.2 bagi semua kaedah → `laporan/ENJIN_LAJU_SAHKAN.md`. Jalankan semula setiap kali `enjin_laju.py` atau modul kaedah berubah.
- `ujian/` — `python3 -m unittest discover -s WFO/ujian`.
- `data/hasil/` — keputusan setiap kaedah (`<id>.json`, `_pilihan.csv`, `_dagangan_oos.csv`, `_ekuiti.csv`).
- Data input: `data_mentah/dataset_S1–S4.csv`, `index_benchmark.csv`.

## Otak penalaan (sejak 16 Okt 2026)
- `kod/analisis_sebenar.py` — prestasi sebenar Papertrade C lawan jangkaan (posisi matang sahaja) → `laporan/ANALISIS_SEBENAR.md`. Jadual: `jadual/analisis_mingguan.md`.
- `kod/tala_semula.py` — data terkini → WFO 3 benih → `cadangan/<label>.md`. Jadual: `jadual/tala_suku.md`. Tiada perubahan tanpa kelulusan pengguna.

## Tempoh pengumpulan data (keputusan pengguna 16 Okt 2026: "maintain dahulu, kumpul data terbaik"; ujian ke hadapan bagi SEMUA kaedah, bukan 8 sahaja)
Ditetapkan SEBELUM data dikumpul supaya kriteria tidak berubah mengikut keputusan.
- Tempoh: 16 Okt 2026 – 15 Jan 2027. Semua 134 kaedah Papertrade C diuji ke hadapan; tiada kaedah dibuang dan tetapan TIDAK diubah, kecuali pembetulan ralat kod atau keputusan pengguna. Cadangan tala semula 1 Jan 2027 hanya dicatat, belum diguna.
- Data: posisi `papertrade/claude*.csv`; SEMUA isyarat 100% setiap malam dengan rank (`BacktestShariah2/data/isyarat/`); stor harga harian; analisis mingguan (`laporan/ANALISIS_SEBENAR.md`).
- Penilaian 15 Jan 2027, bagi SETIAP kaedah:
  1. Dagangan hadapan = Lejar Penuh (`BacktestShariah2/lejar/`, sejak 16 Okt 2026): semua isyarat dibeli pada buka esok dan dikeluarkan dengan enjin v1.2 setiap malam (bukan hanya yang dibeli Papertrade C; isyarat semasa saham sama masih dipegang diabaikan, seperti backtest). >= 30 dagangan matang: menang/purata lawan jangkaan (z, t < −2 = gagal). < 30: tidak dinilai, pengumpulan diteruskan hingga 15 Apr 2027.
  2. Portfolio 8 slot × 12.5% kaedah itu sendiri (isyaratnya ikut rank, enjin v1.2) lawan EW tempoh sama.
  3. DSR merentas semua kaedah yang dinilai (dengan 134 ujian, kira-kira 3 kaedah akan kelihatan lulus atau gagal secara kebetulan).
- Portfolio berbilang kaedah hanya dibina daripada kaedah yang lulus 1–3; tiada senarai kaedah teras ditetapkan lebih awal.
