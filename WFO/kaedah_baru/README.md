# Calon K145+ (M115–M161) — modul WFO sahaja

Sumber: `BacktestShariah2/spec/KATALOG_K145.md` dan `CADANGAN_SARINGAN_K145.md` (47 sesuai → M115–M161).
Folder ini SENGAJA di luar `BacktestShariah2/kod/kaedah/` kerana `scanner.py` harian mengimbas semua `kaedah/M*.py`;
calon belum diuji tidak boleh masuk imbasan Papertrade C.

- Modul mentakrif ENTRY sahaja (`sig`, `rank`) serta henti/exit asal jika katalog menyatakannya. Stop/exit/tempoh pegang ditala oleh WFO.
- Pencetus "beli tembus paras X" = tutup hari i > X, masuk buka hari i+1 (mekanikal pada tutup harian).
- Setiap andaian ditulis dalam baris `# Sumber:` modul. Modul lulus semakan pandang ke hadapan `wfo.semak_kaedah`.
