# SPEC AUTOTUNE A02

Ditetapkan 18 Okt 2026 sebelum sebarang larian A02, berdasarkan audit bebas A01 (dilaporkan kepada pengguna 18 Okt 2026). A01 (`SPEC.md`, `hasil/`) kekal tidak diubah sebagai rekod. Output A02 di `hasil_a02/`; data di Release `autotune-data-a02`.

## 1. Data dan universe (baiki audit #1–#3)
- Harga tetap yfinance `auto_adjust=True` untuk backtest. Tambahan: peristiwa split (`actions=True`) untuk membina harga tidak dilaras: `tutup_mentah(t) = tutup_split_dilaras(t) × hasil darab nisbah split selepas t`.
- Universe bulanan (titik masa): tutup_mentah hujung bulan > USD10, median 60 hari (tutup_mentah × volum_mentah) ≥ USD1 juta, ≥ 200 bar; 2000 teratas ikut median nilai dagangan; berkuat kuasa bulan berikutnya. Kumpulan A/B ikut md5 seperti A01.
- QC peringkat bar, titik masa: bar dibuang hanya jika |r_t| > 40% DAN pulangan esok berbalik arah dengan |r_t+1| > 40% (lonjakan data), atau harga ≤ 0 / NaN / high < low. Tiada ticker dibuang kerana kemeruapan.
- Kaveat kekal: tiada saham delist (survivorship); dilaporkan sebagai had atas.

## 2. Enjin dan objektif (baiki audit #7, #8, #17)
- Dua lorong: `had60` (had pegang 60 hari, seperti A01) dan `asal` (tiada had enjin; TMAX asal kaedah).
- Metrik n, hari pegang, kadar menang dikira daripada dagangan yang benar-benar dipegang portfolio 8 slot × 12.5%.
- Objektif latih: CAGR portfolio tolak CAGR SPY tempoh sama (pulangan berlebihan). Kekangan: MDD ≥ MDD SPY tempoh sama − 10 mata peratus; ≥ 30 dagangan portfolio. Pelanggar: −1 + lebihan − 2 × lebihan MDD.
- Kos, slippage, gap hari pertama dan topeng universe seperti A01. Pemanasan latih = maksimum(400 hari, 1.6 × tetingkap terpanjang dalam julat atas + WARM bar).

## 3. Reka bentuk ujian (baiki audit #12)
- Tempoh bersih (kaedah tidak pernah direka atas data ini): 2010-01-01 – 2018-12-31.
- Peringkat 1 (saringan): semua 134 kaedah × 2 lorong, PARAM asal, tempoh 2013-01-01 – 2018-12-31, kumpulan A dan B. Skor = min(lebihan A, lebihan B) atas SPY. Pilih 20 teratas setiap lorong (maks 40 kaedah-lorong).
- Peringkat 2 (tala): bagi yang terpilih, walk-forward tetingkap ujian 2013…2018 (6, latih 3 tahun sebelum), AKHIR (latih 2016-01-01 – 2018-12-31; diuji atas 2019-01-01 – hujung data, A+B = pengesahan), SEMASA (latih 3 tahun terakhir). Optuna TPE 120 percubaan, benih 42 + kajian, percubaan pertama = PARAM asal.
- Holdout sebenar: ujian ke hadapan sejak 16 Okt 2026 (Lejar Penuh); tidak dinilai dalam A02.

## 4. Pengesahan dan label
- OOS bersih = gabungan tetingkap 2013–2018 (A dan B). Pengesahan = 2019 – hujung data (parameter AKHIR, A+B).
- DSR atas pulangan berlebihan harian (strategi − SPY), N = bilangan kaedah-lorong dalam saringan (268). PBO dilaporkan sahaja.
- Imbasan pandang ke hadapan atas parameter AKHIR dan SEMASA setiap kaedah terpilih, ≥ 12 tarikh potong.
- Label: LULUS jika lebihan OOS bersih > 0 pada A dan B, lebihan pengesahan > 0, MDD OOS ≥ MDD SPY − 10 mata peratus, DSR ≥ 0.90 dan imbasan bersih. CALON jika tiga syarat pertama sahaja. TIDAK LULUS selain itu. PANDANG HADAPAN jika imbasan gagal.
- Portfolio gabungan daripada LULUS (jika tiada, CALON), peraturan tamak seperti A01 §6 atas OOS bersih A.

## 5. Output
`hasil_a02/saringan.csv`, `hasil_a02/tala/<ID>_<lorong>/kNN.json`, `hasil_a02/parameter_sedia.csv`, `hasil_a02/gabungan.json`, `hasil_a02/LAPORAN.md`, db dashboard (koleksi `autotune`, ditanda A02). Parameter SEMASA ialah cadangan sahaja; tiada dagangan wang sebenar.
