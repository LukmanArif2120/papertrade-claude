# Analisis mingguan prestasi sebenar (Sabtu 9:52 pagi MYT)

Automatik; jangan tanya soalan. Tiada order. Tidak mengubah kaedah atau tetapan Papertrade C.

1. `git pull --rebase origin main`.
2. `python3 WFO/kod/analisis_sebenar.py` → `WFO/laporan/ANALISIS_SEBENAR.md` dan `WFO/data/analisis_sebenar.json`.
3. db dashboard (https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e, `select:ArtifactData`): baca `analisis/sebenar` (jika wujud, guna `if_version`), kemudian `set` dengan `{"dijana": "<tarikh>", "rows": <isi analisis_sebenar.json>}`.
4. Catat satu baris dalam `standard/binaan_v2_log.md` (`BacktestShariah2/standard/`): bilangan AMARAN / SELARI / data belum cukup, dan senarai kaedah AMARAN.
5. `python3 BacktestShariah2/standard/sahkan.py --betulkan` (mesti 0), commit `Analisis mingguan <tarikh>: <ringkas>` dan push ke `main`.
6. PushNotification (status proactive, < 200 aksara): bilangan AMARAN dan 3 kaedah AMARAN terburuk, atau "tiada amaran".
