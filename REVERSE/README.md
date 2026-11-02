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

## SEBELUM MEMULAKAN KAJIAN BAHARU — baca ini dahulu

Dua kali pada 1 Nov 2026 satu kajian dimulakan di sini untuk soalan yang repo **sudah** jawab,
kerana jawapannya berada di luar `REVERSE/` dan tidak dirujuk dari sini. Senarai silang:

- **Ukuran momentum pakar sudah dikod dan diukur** — `BacktestShariah2/kajian/rs/RINGKASAN.md`
  §14–16 (dijana `standard/kajian_rs.py`; 3,830 saham, 2005-01-03 hingga 2026-10-16, 1,034 tarikh
  sampel, 1,780,970 pemerhatian; kelayakan tutup ≥ USD5 **dan** nilai 50 hari ≥ USD1 juta).
  Sudah ada: 12-1 akademik (`m12_1`), gema Novy-Marx 12-7, 6-2, **formula Clenow penuh**
  (`exp(cerun×252)−1` × R² atas 90 bar log), normalisasi turun naik Barroso–Santa-Clara (`rs_vol`),
  **momentum residual Blitz–Huij–Martens** (`res_mom`), frog-in-the-pan (`id_fip`), MAX
  Bali–Cakici–Whitelaw (`max21`), momentum industri (`rs_industri`), Mansfield RP, jarak tinggi 52w.
  Portfolio bulanan desil teratas **selepas kos** lawan alam layak 9.38%: `m12_1` 11.70%,
  `rs` 11.55%, `m12_7` 10.94%, `m6_2` 10.64%, `clenow` 9.74%, `rs_vol` 9.69%. Margin momentum
  panjang-sahaja terbaik yang pernah diukur di sini ialah **+2.32 mata/tahun**.
- **Siling ramalan ARAH** — `REVERSE/SILING_ARAH.md`: 51.55% luar sampel lawan asas 50.50%, dan
  pilihan paling yakin memperoleh KURANG daripada membeli semua bar. Jangan uji semula.
- **Ramalan MAGNITUD kenaikan** — `REVERSE/MOMENTUM_PEGANG.md` §2c: tertile ATR% teratas +23.72
  mata, terbawah −23.90 mata (hampir simetri) = sasaran mengukur turun naik, bukan arah;
  normalisasi menukar tanda 8/8. Pradaftar pendua yang ditarik balik: `SPEC_EKOR_RAMAL.md`.
- **Ruang yang sudah ditutup**: pemicu harga (fasa 1), fundamental SEC (fasa 2), silang-keluarga
  (`SILANG.md`), penapis setup (`SETUP.md` 0/598), pembinaan portfolio (`PEMBINAAN.md`),
  masuk Nxx (`NXX.md` gate3 0/280).

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
