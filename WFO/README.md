# WFO — Walk-forward optimization kaedah M (W01)

Kerja kajian berasingan daripada rutin harian Papertrade C. Tiada fail dalam `BacktestShariah2/` diubah; enjin v1.2 dan modul kaedah dibaca sahaja.

- `spec/SPEC_WFO_SISTEM_SWING.md` — spec W01.
- `kod/wfo.py` — larian WFO (`python3 WFO/kod/wfo.py senarai | kelompok 5 | jalan Mxx | w01`).
- `kod/wfo_laporan.py` — laporan Fasa C → `laporan/W01_LAPORAN.md`.
- `ujian/` — `python3 -m unittest discover -s WFO/ujian`.
- `data/hasil/` — keputusan setiap kaedah (`<id>.json`, `_pilihan.csv`, `_dagangan_oos.csv`, `_ekuiti.csv`).
- Data input: `data_mentah/dataset_S1–S4.csv`, `index_benchmark.csv`.
