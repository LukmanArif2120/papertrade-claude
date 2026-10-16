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
