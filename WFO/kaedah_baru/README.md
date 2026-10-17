# Calon K145+ (M115–M161) — modul WFO sahaja

Sumber: `BacktestShariah2/spec/KATALOG_K145.md` dan `CADANGAN_SARINGAN_K145.md` (47 sesuai → M115–M161).
Folder ini SENGAJA di luar `BacktestShariah2/kod/kaedah/` kerana `scanner.py` harian mengimbas semua `kaedah/M*.py`;
calon belum diuji tidak boleh masuk imbasan Papertrade C.

- Modul mentakrif ENTRY sahaja (`sig`, `rank`) serta henti/exit asal jika katalog menyatakannya. Stop/exit/tempoh pegang ditala oleh WFO.
- Pencetus "beli tembus paras X" = tutup hari i > X, masuk buka hari i+1 (mekanikal pada tutup harian).
- Setiap andaian ditulis dalam baris `# Sumber:` modul. Modul lulus semakan pandang ke hadapan `wfo.semak_kaedah`.

## STEP-2 Rangka R dan lapisan (17 Okt 2026)
Skrip backtest (bukan modul imbasan): `_rangka_r.py` (Rangka R, menghasilkan semula M114 V4), `_resid.py` (RESID M162),
`step2_M162.py` … `step2_M167.py`, `step2_L01.py` (penapis rejim), `step2_L02.py` / `step2_L02B.py` (meta-label),
`jejak_M166.py` (jejak kertas M166 V1 → `BacktestShariah2/uji_kertas/jejak_M166.csv`, tiada belian).
Laporan: `BacktestShariah2/laporan/M162–M167.md`, `L01_penapis_rejim.md`; `WFO/laporan/L02_meta_label.md`, `L02B_V2_rank.md`.
