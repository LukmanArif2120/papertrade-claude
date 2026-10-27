# REVERSE — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Kajian **signal dan indikator**, bukan kaedah Mxx repo dan bukan penalaan parameter. Tiada Optuna.
Arah terbalik daripada backtest: **hasil dahulu, signal kemudian**.

- Spec dikunci sebelum larian pertama: **`SPEC.md`** (termasuk 9 pindaan bertarikh 27 Okt 2026).
- Laporan setiap tahun: **`LAPORAN_2025.md`**, **`LAPORAN_2024.md`** (dijana `jana_laporan.py`).
- Setiap signal/kombinasi yang diuji: `log_ujian.csv`.
- Imbasan pandang ke hadapan: `PANDANG_HADAPAN_<TAHUN>.md` (14 tarikh potong setiap tahun, 0 kegagalan).
- Perbandingan merentas tahun: **`BANDING_TAHUN.md`** (dijana `banding_tahun.py`).

## Jalankan semula (urutan)

```
python3 REVERSE/semak_hadapan.py 2025             # kesediaan 0.3f
python3 REVERSE/step1_run.py 2025                 # Step 1-2 + cache indikator  (~270 s)
python3 REVERSE/step2b_kohort.py 2025             # Step 2b                     (~30 s)
python3 REVERSE/step3_signal.py 2025              # kuintil dibeku + dedup      (~7 s)
python3 REVERSE/step4_common.py 2025              # Step 4 + corong             (~10 s)
python3 REVERSE/step5_6_hold_exit.py 2025         # Step 5-6 (CALON)            (~215 s)
python3 REVERSE/step7_false.py 2025               # Step 7                      (~40 s)
python3 REVERSE/step7b_hadapan.py 2025            # Step 7b, 234 sistem         (~25 s)
python3 REVERSE/step8_kawalan.py 2025             # Step 8                      (~105 s)
python3 REVERSE/step9_portfolio.py 2025           # Step 9 (kriteria akhir)      (~20 s)
python3 REVERSE/jana_laporan.py 2025
python3 REVERSE/banding_tahun.py                  # selepas >= 2 tahun siap
```

Tahun lain: kod dan parameter **sama tanpa ubah**, universe ikut bulan tahun itu —
tukar sahaja argumen tahun pada setiap skrip. Jangan ubah `SPEC.md` kecuali sebagai pindaan
bertarikh. Siap setakat ini: **2025, 2024**.

## Data

Harga: Release GitHub `autotune-data-a02` melalui `AUTOTUNE/teras/data.py` `ambil()` — **jangan**
guna Release `autotune-data` (A01 membuang saham meruap). Cache tempatan `REVERSE/.cache/`
(dalam `.gitignore`; parquet dan fail per-hari TIDAK dicommit).

## Teras

| Modul | Isi |
|---|---|
| `teras/data.py` | universe titik-masa, harga A02, sektor/industri, indeks sektor berpemberat sama |
| `teras/ind.py` | 77 lajur indikator, tetapan standard, semua kausal |
| `teras/run.py` | definisi run, tarikh sah, kaki, jenis kenaikan, peristiwa sah kausal |
| `teras/keluar.py` | 13 signal EXIT grid sistem + 18 peraturan HOLD sebagai veto |
| `teras/signal.py` | binaan signal, dedup Spearman, senarai keutamaan tetap |
| `teras/stat.py` | lift/presisi, kelas, BH-FDR, permutasi label, bootstrap blok |
| `teras/kos.py` | komisen 0.1% + slippage ikut median nilai dagangan 20 hari |

## Had fasa

Gate 8.1 memerlukan kelas yang sama dalam **≥ 2 tahun LAIN**. Dengan 2025 dan 2024 siap,
setiap tahun hanya mempunyai satu tahun lain, jadi keputusan **tertinggi** kekal **CALON**.
Tiada signal boleh dilabel DITERIMA sebelum sekurang-kurangnya satu tahun lagi disahkan.
