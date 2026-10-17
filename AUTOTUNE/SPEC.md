# SPEC AUTOTUNE (A01)

Ditetapkan 17 Okt 2026, 22:00 MYT, SEBELUM sebarang larian. Keputusan pengguna 17 Okt 2026: universe 2000 saham tanpa penapis Shariah, data percuma (yfinance), objektif CAGR maksimum dengan MDD ≤ 30%, portfolio 8 slot × 12.5%, hasil = setup terbaik setiap kaedah + portfolio gabungan, gaya swing. Projek ini berasingan daripada Papertrade C, Lejar Penuh, WFO W01 dan ujian ke hadapan (16 Okt 2026 – 15 Jan 2027); tiada fail di luar `AUTOTUNE/` dan `.github/workflows/autotune_*.yml` diubah.

## 1. Data
- Calon: `nasdaqlisted.txt` + `otherlisted.txt` (nasdaqtrader.com SymDir), saham biasa sahaja: buang ETF, Test Issue, waran, unit, hak (rights), saham keutamaan, nota, dan nama "Acquisition Corp/Corporation" (SPAC). ADR dikekalkan. Ditambah semua ticker dalam `data_mentah/dataset_S*.csv`. Penanda aras: SPY, QQQ.
- Harga: yfinance, `auto_adjust=True` (dilaras split + dividen), 2009-01-01 hingga terkini (2009 = pemanasan). Dimuat turun di GitHub Actions (sesi Claude disekat daripada Yahoo), 10 job matrix, jeda antara kelompok, cuba semula 3 kali.
- Format: parquet satu fail setiap tahun `harga_YYYY.parquet` (lajur ticker, date, open, high, low, close, volume; harga float32), `idx.parquet` (SPY, QQQ), `universe.parquet`, `qc.csv`. Disimpan sebagai aset GitHub Release tag `autotune-data`. Dalam git hanya `AUTOTUNE/data/manifest.json` (fail, saiz, sha256, tarikh tarikan, bilangan ticker) dan `AUTOTUNE/data/QC.md`.
- Semakan kualiti: buang bar dengan harga ≤ 0, NaN, atau high < low; tanda ticker dengan > 5 hari |pulangan harian| > 50% (kemungkinan data rosak) dan keluarkan ticker itu daripada universe; laporan dalam `QC.md`.
- Universe bulanan (titik masa, tanpa pandang ke hadapan): pada tutup hari dagangan terakhir bulan m, saham layak jika harga tutup > USD10, median nilai dagangan (close × volume) 60 hari ≥ USD1 juta, dan ≥ 200 bar sejarah. Ambil 2000 teratas ikut median nilai dagangan 60 hari. Senarai ini berkuat kuasa untuk semua hari dagangan bulan m+1. Lajur: bulan (YYYY-MM berkuat kuasa), ticker, kedudukan.
- Kumpulan: A jika `int(md5(ticker).hexdigest(), 16) % 2 == 0`, selain itu B (tetap walaupun universe berubah). A = tala; B = semakan merentas saham.
- Kelemahan diakui: tiada saham delist (bias survivorship); semua keputusan ialah had atas.

## 2. Modul kaedah
- Benih: 134 modul `BacktestShariah2/kod/kaedah/M*.py` (dibaca sahaja). Salinan berparameter di `AUTOTUNE/kaedah/Mxx.py` (dan `_k145.py`).
- Antara muka salinan: `PARAM` (dict nama → nilai asal), `JULAT` (dict nama → ('int'|'float', bawah, atas)), `TALA` (senarai ≤ 6 nama yang ditala; selebihnya beku), `sedia(fr, idx, P=None)` (P digabung atas PARAM), serta pemalar asal ID, NAMA, VARIAN, TMAX, WARM, ADA_HENTI, SILANG, PERLU_BAR. `hampir()` tidak diperlukan.
- Kesetaraan wajib: `sedia(fr, idx)` dengan PARAM asal mesti menghasilkan lajur sig, stop, tgt, exitc, rank yang SAMA bait demi bait dengan modul asal pada data 431. Modul yang gagal dilabel BELUM DITALA dan tidak menahan kaedah lain.
- Julat lalai: tempoh/tetingkap (int) 0.5×–2× nilai asal (minimum 2); pengganda/ambang (float) 0.5×–1.5× nilai asal; pemalar struktur (252, 100, 0.5 sebagai median, peratusan tetap kalendar) dibekukan. Pilih ≤ 6 parameter: utamakan henti/sasaran/keluar dan tetingkap isyarat utama.

## 3. Enjin autotune (`AUTOTUNE/teras/enjin_at.py`)
- Asas: logik `WFO/kod/enjin_laju.py` (setara enjin v1.2), dengan perbezaan berikut sahaja:
  1. Gap hari pertama: jika buka hari masuk ≤ henti, dagangan keluar pada buka itu juga (sebab 'henti').
  2. Kos setiap sisi = komisen 0.1% + slippage ikut median nilai dagangan 20 hari pada hari isyarat: ≥ USD50 juta 0.05%; USD10–50 juta 0.10%; < USD10 juta 0.25%.
  3. Had swing: pegangan maksimum 60 hari dagangan untuk semua kaedah (TMAX asal dikekalkan jika lebih pendek).
  4. Isyarat sah hanya jika ticker dalam universe bulan itu dan dalam kumpulan yang diuji.
  5. Tetingkap [mula, akhir]: hanya kemasukan dalam tetingkap; posisi yang masih terbuka ditutup pada tutup hari terakhir tetingkap.
- Portfolio: 8 slot × 12.5% ekuiti, susunan ikut lajur rank (tertinggi dahulu), satu posisi setiap ticker, seperti v1.2.

## 4. Penalaan
- Walk-forward: tetingkap ujian 2013, 2014, …, 2023 (tahun penuh) dan 2024-01-01–2024-09-30 (12 tetingkap). Latih = 3 tahun sebelum mula ujian. Dua kajian tambahan: AKHIR (latih 2021-10-01–2024-09-30; ujian = tempoh kunci) dan SEMASA (latih 3 tahun terakhir data; parameter untuk diguna sekarang). Jumlah 14 kajian setiap kaedah.
- Optuna TPE, 120 percubaan setiap kajian, benih 42 + nombor tetingkap; percubaan pertama = PARAM asal.
- Objektif (data latih, kumpulan A): CAGR portfolio. Kekangan: MDD ≥ −30%, ≥ 30 dagangan, purata hari pegang 2–60. Percubaan yang melanggar diberi skor = −1 + CAGR − 2 × (lebihan MDD).
- Pilihan teguh: antara 10 percubaan teratas yang lulus kekangan, pilih yang pulangan tahun kalendar terburuknya dalam tempoh latih paling tinggi.
- Pengiraan: `sedia()` hanya atas data [mula latih − 400 hari kalendar, akhir ujian]; kaedah SILANG dikira atas A+B (rank merentas 2000 saham), lain-lain atas kumpulan yang diuji sahaja.

## 5. Pengesahan (selepas tala; peraturan ini dikunci sekarang)
- OOS-A: gabungan tetingkap ujian 2013 – Sep 2024, setiap tetingkap dengan parameternya sendiri, kumpulan A.
- OOS-B: sama, kumpulan B.
- Ujian bersih: 2013–2018 dengan PARAM asal, A+B (kaedah tidak pernah direka atas data sebelum 2019).
- Kepekaan: parameter AKHIR, setiap parameter TALA diubah ±10% dan ±25% atas data latih AKHIR; nisbah dataran = median CAGR jiran ÷ CAGR pilihan.
- DSR: N = jumlah semua percubaan semua kaedah; pulangan harian OOS-A.
- PBO (CSCV, 8 blok): 50 percubaan teratas kajian AKHIR, pulangan harian latih.
- Tempoh kunci: parameter AKHIR atas 2024-10-01 – hujung data, A+B. Dibuka sekali sahaja.
- Penanda aras: SPY bagi tempoh yang sama.
- Label:
  - BUKAN SWING: purata hari pegang OOS-A < 2 atau > 60.
  - TINGGI: CAGR OOS-A > SPY, CAGR OOS-B > SPY, MDD OOS-A ≥ −30%, CAGR tempoh kunci > SPY, DSR ≥ 0.95, PBO ≤ 0.30.
  - SEDERHANA: CAGR OOS-A > SPY, CAGR OOS-B > SPY, MDD OOS-A ≥ −30% (syarat lain tidak semua dipenuhi).
  - RENDAH: CAGR OOS-A > 0 tetapi bukan SEDERHANA.
  - GAGAL: selain itu. BELUM DITALA: modul gagal kesetaraan.

## 6. Portfolio gabungan
- Calon: kaedah TINGGI dan SEDERHANA. Isyarat semua kaedah dikongsi dalam satu portfolio 8 slot × 12.5%; rank = persentil rank dalam kaedah sendiri pada hari itu.
- Pemilihan tamak atas OOS-A: mula dengan CAGR OOS-A tertinggi; tambah kaedah seterusnya hanya jika CAGR OOS-A gabungan naik dan MDD ≥ −30%; langkau kaedah yang korelasi pulangan harian > 0.7 dengan mana-mana kaedah terpilih; maksimum 6 kaedah.
- Gabungan akhir dinilai atas OOS-B dan tempoh kunci; parameter SEMASA digunakan untuk cadangan dagangan.

## 7. Output (`AUTOTUNE/hasil/`)
- `tala/Mxx.json` (setiap kajian: parameter terbaik, metrik latih/ujian), `parameter_sedia.csv`, `gabungan.json`, `LAPORAN.md` (dijana skrip), kemudian dashboard (terakhir).
- Tala semula setiap suku (Actions cron): kajian SEMASA sahaja; cadangan, bukan perubahan automatik.
