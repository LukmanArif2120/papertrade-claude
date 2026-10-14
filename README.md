# Papertrade Claude (Backtest Shariah 2)

Mencari kaedah entry, tempoh pegang dan exit terbaik untuk swing momentum saham Shariah AS, kemudian mengujinya secara papertrade maya (Papertrade C) setiap hari dagangan.

- Mula di sini: `CLAUDE.md`, kemudian `BacktestShariah2/standard/tugasan_v3.md` (peraturan tunggal harian).
- Latar belakang dan keputusan backtest: `BacktestShariah2/00_NOTA_SERAHAN.md`, `BacktestShariah2/laporan/`.
- Tugasan berjadual: `BacktestShariah2/jadual/` (6:02 pagi MYT kemas kini, 8:02 malam MYT imbasan, 9:35 pagi New York belian maya).
- Kod isyarat dan enjin: `BacktestShariah2/kod/`. Data papertrade: `BacktestShariah2/papertrade/` (skema: `SKEMA.md`).
- Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (sumber halaman: `BacktestShariah2/standard/dashboard_v2.html`).

Semakan tempatan:

```
pip install -r requirements.txt
python3 -m unittest discover -s BacktestShariah2/ujian
python3 BacktestShariah2/standard/sahkan.py
```

Tiada order sebenar dan tiada wang sebenar digunakan.
