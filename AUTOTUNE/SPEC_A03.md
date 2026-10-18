# SPEC AUTOTUNE A03 — sistem pakar lebih lengkap

Ditetapkan 18 Okt 2026 sebelum sebarang larian A03, atas permintaan pengguna selepas A02 (tiada kaedah lulus). Tujuan: menguji kaedah pakar (Minervini, O'Neil/IBD, Weinstein, Darvas, dll.) dengan unsur yang tiada dalam versi harga sahaja: fundamental EPS, arah pasaran, penumpuan dan had rugi. A01/A02 tidak diubah. Output `hasil_a03/`.

## 1. Data
- Harga dan universe: Release `autotune-data-a02` (SPEC_A02 §1).
- Fundamental: EPS sebenar setiap suku dan tarikh/masa laporan bagi semua ticker yang pernah dalam universe A02, daripada Yahoo (`yfinance` `get_earnings_dates`, had terbesar yang dibenarkan), dimuat turun di GitHub Actions → Release `autotune-fundamental-a03`. Titik masa: data suku tersedia mulai hari dagangan laporan jika dilapor sebelum buka, selain itu (selepas tutup atau masa tidak diketahui) mulai hari dagangan berikutnya.
- Liputan dilaporkan setiap tahun (peratus ticker universe yang ada EPS). Jika liputan < 70% bagi mana-mana tahun 2013–2018, keputusan ditanda "liputan rendah".

## 2. Sistem utama (satu sahaja, untuk pemilihan)
- F (fundamental, ala CAN SLIM "C"): pada hari isyarat, suku terkini yang sudah tersedia mempunyai EPS > 0 dan pertumbuhan EPS tahun ke tahun ≥ 25% berbanding suku yang sama tahun lepas (EPS tahun lepas > 0). Tiada data → tidak layak.
- M (arah pasaran): tutup SPY > SMA50 dan SMA50 > SMA200 pada hari isyarat.
- Portfolio: 5 slot × 20%, susunan rank kaedah; had rugi enjin −8% daripada harga masuk (henti = maksimum(henti kaedah, 0.92 × harga masuk)).
- Lain-lain (kos, slippage, gap, topeng universe, dua lorong `had60`/`asal`, metrik dagangan portfolio) seperti A02.
- Ablasi (dilaporkan sahaja, tidak untuk pemilihan): F sahaja, M sahaja, tanpa F/M dengan 5 slot.

## 3. Kaedah
- 14 kaedah pakar: M06, M28, M35, M37, M38, M44, M51, M54, M64, M66, M74, M87, M88, M104.
- 6 kaedah lain teratas dalam saringan A02 lorong `asal` (min lebihan A/B), selain 14 di atas.
- Jumlah 20 kaedah × 2 lorong = 40 sistem.

## 4. Reka bentuk ujian
- Peringkat 1: 40 sistem, PARAM asal, tempoh bersih 2013-01-01 – 2018-12-31, kumpulan A dan B. Skor = min(lebihan A, lebihan B) atas SPY.
- Peringkat 2: 10 sistem teratas ditala (walk-forward 2013…2018, AKHIR latih 2016–2018 diuji 2019 – hujung data, SEMASA), TPE 120 percubaan, objektif dan kekangan seperti SPEC_A02 §2.
- Label seperti SPEC_A02 §4; DSR atas pulangan berlebihan, N = 308 (268 A02 + 40 A03, kumulatif). Imbasan pandang ke hadapan ≥ 12 tarikh potong termasuk lajur fundamental.

## 5. Kaveat dikunci
- Tiada saham delist; Yahoo EPS mungkin tidak lengkap bagi tahun awal; EPS Yahoo ialah EPS dilaporkan/dilaras penganalisis, bukan GAAP.
- Pemangkin, pegangan institusi dan pyramiding tidak dimodelkan.
