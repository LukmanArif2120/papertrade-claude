# REVERSE — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Kajian **signal dan indikator**, bukan kaedah Mxx repo dan bukan penalaan parameter. Tiada Optuna.
Arah terbalik daripada backtest: **hasil dahulu, signal kemudian**.

- **Keputusan penutup fasa 1: `KEPUTUSAN_FASA1.md`** (dijana `jana_keputusan_fasa1.py`) — baca ini dahulu.
- Spec dikunci sebelum larian pertama: **`SPEC.md`** (12 pindaan bertarikh).
- Laporan setiap tahun: **`LAPORAN_2025.md`**, **`LAPORAN_2024.md`**, **`LAPORAN_2023.md`**, **`LAPORAN_2022.md`**, **`LAPORAN_2021.md`**, **`LAPORAN_2020.md`** (dijana `jana_laporan.py`).
- Setiap signal/kombinasi yang diuji: `log_ujian.csv`.
- Imbasan pandang ke hadapan: `PANDANG_HADAPAN_<TAHUN>.md` (14 tarikh potong setiap tahun, 0 kegagalan).
- Perbandingan merentas tahun: **`BANDING_TAHUN.md`** (dijana `banding_tahun.py`).
- Jadual keputusan satu baris setiap tahun: **`JADUAL_KEPUTUSAN.csv`** (dijana `jadual_keputusan.py`).

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
bertarikh. Siap setakat ini: **2025, 2024, 2023, 2022, 2021, 2020**. Universe 2021-2025 ialah 2000 saham sebulan; **2020 lebih kecil (1638/1832/1940 min/median/maks)**, jadi bilangan mutlaknya tidak setara dan laporan 2020 membawa kaveat saiz universe.

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

Gate 8.1 diketatkan atas keputusan pengguna 28 Okt 2026 (pindaan §13.12): naik taraf ke DITERIMA
memerlukan signal **lulus gate keras** dalam ≥ 2 tahun LAIN, bukan sekadar kelas yang sama.
Hasilnya: **0 DITERIMA** merentas enam tahun; 11 CALON (6 pada 2020, 1 pada 2023, 4 pada 2025).
Empat signal lulus gate keras dalam tepat 2 tahun (2020 dan 2025) — satu tahun pendek daripada
syarat.

**Fasa 1 ditutup 28 Okt 2026.** Hipotesis ditolak: tiada signal entry berasaskan indikator harga
menunjukkan kelebihan berulang. Sasaran +10% sebulan: 0 daripada 36 sistem-tahun. Portfolio
berasaskan signal memberi pulangan lebih rendah daripada entri rawak (+12.76% lawan +13.94%
setahun) dengan drawdown 10 mata peratus lebih dalam. Butiran penuh: `KEPUTUSAN_FASA1.md`.
Mengetatkan gate 8.1 ialah keputusan pengguna, bukan perubahan spec selepas melihat hasil.
