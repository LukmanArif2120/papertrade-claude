# KEPUTUSAN FASA 1 — REVERSE (2020–2025)

Dijana `REVERSE/jana_keputusan_fasa1.py`; semua angka dikira daripada CSV yang dicommit.

Fasa 1 menguji **indikator harga sahaja** (77 lajur, tetapan standard, tiada penalaan parameter). Spec dikunci sebelum larian pertama: `REVERSE/SPEC.md` (12 pindaan bertarikh).

## 1. Keputusan penutup

**Sasaran pengguna +10% sebulan (median) TIDAK TERCAPAI: 0 daripada 36 sistem-tahun.** Yang terbaik ialah **6.73%** (`hari_agihan|X=15%,Y=ma50`, 2020, 45 posisi dibuka).


**Hipotesis fasa 1 ditolak.** Tiada signal entry berasaskan indikator harga menunjukkan kelebihan yang berulang merentas 6 tahun. Purata merentas 36 sistem-tahun:


| | Pulangan/tahun | Median bulanan | MDD |
|---|---|---|---|
| Sistem berasaskan signal | **+12.76%** | +0.91% | **-35.12%** |
| Entri RAWAK (universe sama) | **+13.94%** | +0.90% | -24.81% |
| SPY | **+16.57%** | — | -16.75% |


Sistem berasaskan signal memberi pulangan **lebih rendah** daripada entri rawak dengan drawdown **10.3 mata peratus lebih dalam**, dan kalah kepada SPY pada kedua-dua ukuran. Mengalahkan SPY: **16/36** sistem-tahun; mengalahkan entri rawak: **15/36**.


> Kaveat dua arah: data A02 **tiada saham delist** (survivorship), jadi angka sebenar **lebih buruk** daripada yang dilaporkan di atas, bukan lebih baik.


## 2. Skop yang dilindungi

|   tahun |   universe_min |   universe_median |   universe_maks |   n_run |   n_peristiwa_sah |   n_signal_diuji | spy    |
|--------:|---------------:|------------------:|----------------:|--------:|------------------:|-----------------:|:-------|
|    2020 |           1638 |              1832 |            1940 |    4593 |             12858 |              219 | +17.2% |
|    2021 |           1989 |              2000 |            2000 |    4413 |             15259 |              213 | +30.5% |
|    2022 |           2000 |              2000 |            2000 |    5541 |             15440 |              217 | -18.6% |
|    2023 |           2000 |              2000 |            2000 |    4048 |             13642 |              215 | +26.7% |
|    2024 |           2000 |              2000 |            2000 |    3744 |             14151 |              213 | +25.6% |
|    2025 |           2000 |              2000 |            2000 |    4507 |             13998 |              213 | +18.0% |


Jumlah baris ujian ENTRY direkod: **20,640** (setiap signal × subset × populasi × kumpulan data × keluarga), ditambah 6 × 234 ujian SISTEM dan keluarga HOLD/EXIT. Setiap satu dicatat dalam `log_ujian.csv`.


Empat rejim pasaran berbeza dilindungi: lonjakan selepas COVID (2020), puncak dan penguncupan (2021), pasaran menurun (2022, SPY -18.6%), dan tiga tahun menaik (2023–2025).


## 3. Jawapan kepada tiga soalan arahan

**(a) ARAH — adakah saham ini akan naik?** Sedikit, dan tidak boleh dipercayai. Pemicu klasik tunggal (MACD cross, RSI lintas 50, EMA crossback, Donchian 20, pocket pivot, gap and go) mencapai kelas TERAS/UNIQUE/LANGKA dalam **0 daripada 36** kombinasi (pemicu × tahun). Dalam imbasan seluruh universe (Step 7), lift arah signan terbaik hanya 1.2–2.5 kali kadar asas.


**(b) MAGNITUD — naik setinggi mana, secepat mana?** Konteks membawa maklumat magnitud, pemicu tidak — hipotesis arahan **disokong**. Tetapi tiada konteks kekal: signal terbaik mengekalkan kelas penemuan dalam **5/6** tahun sahaja (4 signal), dan **0** dalam kesemua 6 tahun. Kesemua yang terbaik ialah konteks pengembangan kemeruapan (ATR%, julat 20 hari, lebar Bollinger pada kuintil tertinggi) — iaitu kohort yang paling dicemari oleh ketiadaan saham delist.


**(c) KAPASITI — cukup untuk mengisi portfolio?** Signal: ya, berlebihan (180–250 ribu kemunculan setahun). Portfolio: **tidak**. Dengan pegangan panjang, 8 slot terisi awal dan tidak pernah kosong — rujukan pegang-252 hanya membuka 8–16 posisi setahun berbanding ~130 yang diperlukan. **Kapasiti slot yang mengikat, bukan kadar menang.**


## 4. Mengapa +10% sebulan tidak boleh dicapai dengan reka bentuk ini

Portfolio 8 slot × 12.5% yang penuh = 100% dilabur, jadi pulangan bulanan ≈ jangkaan setiap dagangan ÷ tempoh pegangan dalam bulan. Jangkaan yang **diperlukan**:


| Tempoh pegangan | Jangkaan setiap dagangan diperlukan |
|---|---|
| 15 hari dagangan | **+7.1%** |
| 30 hari dagangan | **+14.3%** |
| 60 hari dagangan | **+28.6%** |


Jangkaan bulanan tersirat yang **terbaik** diukur setiap tahun (atas 234 sistem):


|   tahun | sistem                        | jangkaan_dagangan   |   hari_pegang | bulanan_tersirat   |   n_sistem_bulanan_ge10 |
|--------:|:------------------------------|:--------------------|--------------:|:-------------------|------------------------:|
|    2020 | chandelier_4atr|X=12%,Y=ema21 | +19.61%             |          74.8 | +5.50%             |                       0 |
|    2021 | trail_15pct|X=20%,Y=ema9      | -1.66%              |          57.2 | -0.61%             |                       0 |
|    2022 | rsi_70_60|X=7%,Y=ema9         | +0.85%              |         102.6 | +0.18%             |                       0 |
|    2023 | rsi_70_60|X=5%,Y=ema9         | +4.85%              |          71.5 | +1.43%             |                       0 |
|    2024 | hari_agihan|X=5%,Y=ema9       | +1.74%              |          54.4 | +0.67%             |                       0 |
|    2025 | bawah_ma50|X=15%,Y=ma50       | +2.27%              |          17.1 | +2.78%             |                       0 |


**0 daripada 1,404 sistem-tahun** mencapai 10% bulanan tersirat. Jurangnya bukan 10–20%; ia 2–5 kali. Mencapai +10% sebulan secara median memerlukan jangkaan setiap dagangan ~3 kali yang terbaik pernah diukur, **secara konsisten merentas rejim** — sedangkan yang diukur bertukar tanda dari tahun ke tahun.


## 5. Dapatan yang kukuh merentas semua tahun

1. **Kelas pullback ialah satu-satunya hasil yang berulang 6/6 tahun.** Pullback yang trend sahamnya utuh menyambung ke puncak baru jauh lebih kerap daripada pullback yang trendnya rosak — 2020: SIHAT 89.1% / PASARAN 87.9% lawan AMARAN 70.5%; 2021: SIHAT 89.0% / PASARAN 85.3% lawan AMARAN 43.9%; 2022: SIHAT 65.0% / PASARAN 88.7% lawan AMARAN 54.0%; 2023: SIHAT 91.5% / PASARAN 80.0% lawan AMARAN 46.2%; 2024: SIHAT 88.4% / PASARAN 82.6% lawan AMARAN 47.2%; 2025: SIHAT 88.9% / PASARAN 92.0% lawan AMARAN 50.8%. Ini peraturan **pegangan**, bukan peraturan masuk.


2. **Tiada signal EXIT bertahan, pada mana-mana tahun** (BH-FDR q ≤ 0.01): 2020: 0/68; 2021: 0/62; 2022: 0/66; 2023: 0/64; 2024: 0/62; 2025: 0/62. Exit berasaskan MA menyala 12–19 hari **sebelum** puncak dengan kadar palsu 46–74%. Tiada signal membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa".


3. **"Jangan jual" ialah artifak rejim, bukan penemuan.** Jangkaan rujukan terbaik Step 7b berayun mengikut arah 12 bulan selepas kemasukan: 2020: +60.66%; 2021: -2.81%; 2022: +0.55%; 2023: +16.25%; 2024: +8.68%; 2025: +27.57%. Bilangan sistem yang "mengalahkan ketiga-tiga rujukan" bertentangan arah dengan bilangan yang berjangkaan positif — pada 2021, 196/234 mengalahkan rujukan sedangkan **0/234** berjangkaan positif. Kedudukan berbanding rujukan bukan ukuran keuntungan.


4. **Kohort "naik dan naik" ialah kesan sebenar tetapi bukan signal.** Run yang masih naik pada hari ke-63 pergi jauh lebih tinggi (2020: 54.6%; 2021: 15.6%; 2022: 18.2%; 2023: 31.4%; 2024: 22.7%; 2025: 39.8% akhirnya melebihi +100%), tetapi `masih_naik` ialah **label hasil** yang hanya diketahui pada hari ke-63 — ia tidak boleh didagangkan. Julat 15.6%–54.6% itu juga menunjukkan betapa ia bergantung pada rejim.


## 6. Apa yang boleh diguna sekarang, dan apa yang tidak

**Boleh diguna:** kelas pullback sebagai peraturan pegangan — jangan jual pada pullback yang trend saham (tutup > MA50, MA50 menaik, higher low kekal) dan trend pasaran masih utuh; layan pullback yang memecahkan struktur itu secara berbeza. Ini selari dengan falsafah lorong 2 repo dan disokong 6/6 tahun.


**TIDAK boleh diguna:** mana-mana signal entry dalam kajian ini sebagai asas belian. Tiada satu pun lulus gate keras dalam lebih daripada satu tahun, dan portfolio yang dibina atasnya kalah kepada entri rawak daripada universe yang sama.


## 7. Apa yang fasa 1 TIDAK uji

Dikeluarkan atas sebab tiada data titik-masa (SPEC §10), bukan kerana dianggap tidak penting:

- **RS rating lawan seluruh pasaran** (`data/rs/` bermula 2026-09-15)
- **Gred sektor/industri** (`gred_kumpulan_sejarah.csv` bermula 2026-09-25)
- **Earnings**: kejutan EPS, power earnings gap, jarak ke tarikh earnings (`data/sec/` bermula 2026-10-27)

RS lawan SPY dan garisan RS **dikira sendiri** daripada harga dan kekal dalam kajian; ia antara yang gagal gate keras.


Kerana liputan sejarahnya 0% bagi 2020–2025, dimensi ini hanya boleh diuji **ke hadapan**, bukan dengan backtest. Hasil bermakna memerlukan 1–2 tahun pengumpulan.


## 8. Had kajian ini

1. **Tiada saham delist** (survivorship) pada setiap tahun: run dipandang tinggi DAN kadar signal palsu dipandang rendah.
2. **Peta sektor bukan titik-masa** (petikan 2026).
3. **Universe 2020 lebih kecil** daripada 2000 saham sebulan, jadi bilangan mutlaknya tidak setara dengan 2021–2025.
4. **Indeks sektor menggantikan ETF SPDR** (SPEC §13.1) kerana endpoint sejarah tidak dapat diakses.
5. **Portfolio 8 slot** bermakna setiap angka tahunan bergantung pada bilangan posisi yang kecil (8–415); varians tinggi.
6. **Step 7b disampel** 24,000 kemasukan sebulan-berlapis daripada 220–250 ribu (SPEC §13.9).


## 9. Status keputusan setiap tahun (selepas gate 8.1 diketatkan, SPEC §13.12)

|   tahun |   diterima |   calon |   ditolak |   lulus_gate_keras |
|--------:|-----------:|--------:|----------:|-------------------:|
|    2020 |          0 |       6 |        10 |                  6 |
|    2021 |          0 |       0 |        27 |                  0 |
|    2022 |          0 |       0 |        21 |                  0 |
|    2023 |          0 |       1 |        19 |                  1 |
|    2024 |          0 |       0 |        18 |                  0 |
|    2025 |          0 |       4 |        15 |                  4 |


Signal yang lulus gate keras dalam **≥ 2 tahun**: **4** (`q5:atr_pct`, `q5:bb_lebar`, `q5:julat20`, `rsi_lintas50&q5:atr_pct`). Signal yang lulus dalam **≥ 3 tahun**: **0**.


Gate 8.1 menuntut ≥ 2 tahun **LAIN**, jadi satu signal perlu lulus gate keras dalam **≥ 3 tahun** untuk dinaik taraf. Keempat-empat signal di atas lulus dalam tepat 2 tahun (2020 dan 2025) — satu tahun pendek. Itulah sebab gate yang diketatkan menghasilkan **0 DITERIMA**.


## 10. Fail

Setiap tahun: `LAPORAN_<TAHUN>.md`, `runs_`, `monthly_summary_`, `skipped_`, `kohort_masih_naik_`, `common_unique_`, `taburan_indikator_`, `hold_exit_`, `false_signal_`, `hadapan_hold_exit_`, `kawalan_rawak_bootstrap_`, `jangkaan_kemunculan_`, `keputusan_`, `portfolio_`, `portfolio_bulanan_`, `PANDANG_HADAPAN_<TAHUN>.md`.

Merentas tahun: `BANDING_TAHUN.md`, `banding_tahun.csv`, `JADUAL_KEPUTUSAN.csv`, `log_ujian.csv`, `SPEC.md`, dan dokumen ini.
