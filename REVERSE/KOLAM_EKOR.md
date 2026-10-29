# Kolam dan ekor: dua soalan struktur yang tidak pernah ditanya

Dijana 2026-10-29 06:36 UTC oleh `REVERSE/kolam_ekor.py`. Alam: Release `autotune-data-a02` (~3,300 ticker AS). Deskriptif — tiada signal, tiada parameter ditala, tiada pradaftar dibelanjakan.

## 1. Kolam: adakah kita memancing di kolam yang salah?

Setiap sauh = hujung bulan kalendar; pulangan = 21 sesi ke hadapan dari tutup hari itu. Penapis kecairan = median nilai 20 bar ≥ USD 100,000 (ambang repo sendiri, `kod/tidak_layak.py`).

**410,728 sauh saham-bulan cair** merentas 14 tahun (2012–2025), 3,246 ticker.

| Ukuran bulanan | Nilai | Maksudnya |
|---|---|---|
| Median saham-bulan | **+0.82%** | tempat portfolio 8–10 slot mendarat |
| Portfolio berat sama rata SELURUH kolam | **+1.64%** | memegang semua ~3,246 nama |
| SPY (berat permodalan) | **+1.82%** | penanda aras pasif |
| Min saham-bulan | +1.52% | dipacu ekor kanan |
| % saham-bulan positif | 53.6% | lawan SPY 69.9% |

**Tiga baris pertama ialah tiga perkara berbeza dan mencampurkannya adalah kesilapan.** Memegang seluruh kolam memberi MIN rentas-keratan; memilih 8 nama memberi cabutan daripada taburan yang medianya lebih rendah. Itulah sebabnya `KEPEKATAN_BENIH.md` mendapati sebaran 17.3 mata: 8 slot ialah sampel kecil daripada taburan terpencong.

**Jurang saham median lawan SPY: -1.00 mata peratus sebulan** = +10.3%/tahun bagi kolam lawan +24.2%/tahun bagi SPY.

Min melebihi median kerana taburan pulangan saham **terpencong kanan**: beberapa saham naik berganda, majoriti tidak. Portfolio berat sama rata 8–10 slot ialah sampel kecil daripada taburan itu, jadi ia mendarat dekat MEDIAN, bukan min — melainkan ia menangkap ekor kanan.

### Median setiap tahun

| Tahun | Median kolam | Median SPY | Jurang |
|---|---|---|---|
| 2012 | +1.99% | +2.78% | -0.79 |
| 2013 | +2.21% | +2.64% | -0.43 |
| 2014 | +1.01% | +0.79% | +0.22 |
| 2015 | -0.64% | +0.14% | -0.78 |
| 2016 | +1.93% | +1.77% | +0.16 |
| 2017 | +1.42% | +2.07% | -0.65 |
| 2018 | -0.10% | +0.73% | -0.83 |
| 2019 | +1.27% | +2.40% | -1.13 |
| 2020 | +2.44% | +2.62% | -0.18 |
| 2021 | +0.34% | +2.79% | -2.45 |
| 2022 | -0.19% | -1.02% | +0.83 |
| 2023 | -0.98% | +1.31% | -2.29 |
| 2024 | +0.51% | +1.70% | -1.19 |
| 2025 | +0.56% | +2.02% | -1.46 |

Kolam di bawah SPY dalam **11 daripada 14 tahun**.

**Arah bias:** sauh yang tidak mempunyai bar penuh ke hadapan (saham delist atau berhenti didagangkan dalam tingkap) DIBUANG. Itu membuang kegagalan dan mengekalkan yang terselamat, jadi median kolam yang sebenar **lebih rendah** daripada yang dilaporkan di sini. Bias itu menguatkan dapatan, bukan melemahkannya.

## 2. Ekor: adakah henti -2×ATR memotong tempat pulangan berada?

Ufuk 252 sesi (satu tahun) dari bar pertama setiap tahun sauh, 33,622 saham-tahun cair. Henti = sentuhan pertama tutup − 2×ATR14, dinilai pada paras henti. Inilah henti yang dipakai SELURUH kajian (`pul_henti2atr`).

- 1% teratas menyumbang **28.2%** daripada jumlah pulangan kolam
- 5% teratas menyumbang **63.7%** daripada jumlah pulangan kolam
- 10% teratas menyumbang **88.2%** daripada jumlah pulangan kolam

| Ukuran tahunan | Tanpa henti | Dengan henti −2×ATR | Beza |
|---|---|---|---|
| Min | +16.29% | +6.50% | **-9.79** |
| Median | +8.72% | -4.88% | -13.60 |
| Persentil 95 | +98.98% | +66.38% | -32.60 |
| Persentil 5 | -54.67% | -15.58% | +39.09 |

Henti itu tercetus pada **45.7%** daripada semua saham-tahun.

Perhatikan arah kedua hujung: henti menaikkan persentil 5 (ia MEMANG mengurangkan kerugian terburuk) tetapi menurunkan persentil 95 dan min. Itu tandatangan pemotongan ekor kanan: henti mengeluarkan posisi SEBELUM pergerakan besar selesai, dan dalam taburan terpencong kanan, min adalah milik pergerakan besar itu.

### Beza min setiap tahun (dengan henti − tanpa henti)

| Tahun | Tanpa henti | Dengan henti | Beza |
|---|---|---|---|
| 2012 | +21.78% | +12.91% | -8.87 |
| 2013 | +39.81% | +23.48% | -16.33 |
| 2014 | +9.83% | +3.17% | -6.66 |
| 2015 | -4.61% | -1.76% | +2.85 |
| 2016 | +24.64% | -4.72% | -29.36 |
| 2017 | +24.05% | +12.18% | -11.87 |
| 2018 | -9.23% | -1.57% | +7.66 |
| 2019 | +29.80% | +25.84% | -3.96 |
| 2020 | +31.26% | -3.37% | -34.63 |
| 2021 | +25.90% | +22.42% | -3.48 |
| 2022 | -18.11% | -5.97% | +12.14 |
| 2023 | +17.75% | +11.12% | -6.63 |
| 2024 | +21.20% | +4.08% | -17.12 |
| 2025 | +20.98% | -0.90% | -21.88 |

Henti merugikan min dalam **11 daripada 14 tahun**.

## 3. Apa maksudnya bagi matlamat

1. **Kolam kita median +0.82% sebulan; SPY median +1.82%.** Portfolio berat sama rata 8–10 slot mendarat dekat median kolam. Untuk mengalahkan penanda aras, signal entry mesti menambah sekurang-kurangnya 1.00 mata sebulan HANYA untuk seri — sebelum menambah apa-apa. Fasa 1 mengukur kelebihan signal terbaik jauh di bawah paras itu.
2. **Pulangan kolam tertumpu pada ekor:** 63.7% daripada jumlah datang daripada 5% teratas. Sistem yang memotong pada −2×ATR membuang hak untuk berada dalam 5% itu.
3. **Henti −2×ATR mengurangkan min 9.79 mata setahun** pada asas tanpa signal. Seluruh kajian menilai signal MELALUI henti itu, jadi setiap angka pulangan dalam kajian ini mengandungi beban itu.

**Ini bukan dapatan signal dan bukan cadangan membuang henti.** Membuang henti menaikkan min tetapi memperdalam drawdown — itu pertukaran yang sama yang diukur oleh fasa 1b dan `KEPEKATAN.md`, dan kedua-duanya menunjukkan nisbah tidak bertambah baik. Yang ditunjukkan di sini ialah **di mana kekurangan itu bermula**: pada kolam dan pada pemotongan ekor, bukan pada kekuatan pemicu.

## 4. Pemeriksaan pada data hadapan sebenar (Papertrade C)

1,770 posisi sudah ditutup, 577 saham, 103 kaedah. Alam BERBEZA daripada bahagian 1–2 (ditapis Syariah, dipilih pengimbas Mxx), jadi ini pemeriksaan bebas, bukan pengesahan.

### 4a. 421 dagangan yang tidak pernah berpeluang

**421 posisi dibeli dan dihentikan pada HARI YANG SAMA**, kadar menang **0.00%**, purata -2.47%. Kadar menang sifar merentas 421 dagangan bukan hasil pasaran — ia mekanikal: paras henti kaedah terletak DALAM julat intrabar hari masuk, jadi ia disentuh dengan hampir kepastian.

Jarak henti median bagi kematian hari-0 itu: **1.93%** daripada harga masuk. Bagi yang terselamat melepasi hari 0: **5.33%**.

Nilainya jika dibetulkan: jumlah kerugian direalisasi turun **19.5%**. Tetapi perhatikan — purata baki 1,349 posisi ialah -3.18%, **lebih buruk** daripada purata keseluruhan -3.01%. Membetulkan kecacatan ini mengurangkan kerosakan; ia **tidak** menukar tanda.

### 4b. Hasil ikut lebar henti — dan apa yang ia betul-betul kata

| Jarak henti | n | Purata | Kadar menang | Mati hari-0 |
|---|---|---|---|---|
| <1.5% | 212 | -0.74% | 3.3% | 76% |
| 1.5–2.5% | 218 | -1.47% | 8.7% | 43% |
| 2.5–4% | 313 | -2.45% | 11.8% | 27% |
| 4–6% | 356 | -3.65% | 14.0% | 15% |
| 6–9% | 345 | -4.68% | 17.7% | 9% |
| >9% | 211 | -6.52% | 19.4% | 0% |

**Saya perlu membetulkan tafsiran pertama saya sendiri di sini.** Melihat kematian hari-0 itu, hipotesis yang jelas ialah "henti terlalu rapat". Jadual ini menolaknya: baldi paling RAPAT mempunyai purata paling BAIK (-0.74%) dan baldi paling LEBAR paling buruk (-6.52%). Henti rapat mati kerap tetapi murah.

Yang sebenarnya ditunjukkan jadual itu lebih serius. Kadar menang naik 5.9× dari baldi paling rapat ke paling lebar, tetapi kerugian purata naik 8.8× — lebih cepat. Jangkaan kekal **negatif pada setiap lebar henti** dan menjadi lebih negatif apabila henti dilebarkan. Itu tandatangan masuk **tanpa kelebihan**: apabila tiada kelebihan, melebarkan henti hanya meningkatkan kerugian yang diambil ketika salah tanpa kenaikan kadar menang yang mencukupi.

Jadi tiada tetapan henti yang menyelamatkan buku ini. Itu mengesahkan keputusan fasa 1 pada data HADAPAN, bukan pada backtest.

**Had:** 1,770 posisi merentas kurang sebulan, dan 76% posisi masih terbuka. Baca semula selepas 6 bulan.

## 5. Sintesis: satu kenyataan, bukan empat

Bahagian 2 berkata henti −2×ATR memotong ekor kanan kolam. Bahagian 4b berkata tiada lebar henti menyelamatkan buku hadapan. Itu **bukan percanggahan** — kedua-duanya betul dan bersama-sama ia satu kenyataan:

> Pulangan dalam kolam ini hidup dalam ekor kanan yang nipis (63.7% daripada jumlah datang daripada 5% teratas). Pembinaan kita — 8–10 slot berat sama rata, dipotong pada −2×ATR, daripada kolam yang saham mediannya +0.82%/bulan lawan SPY +1.82% — menjauhkan diri daripada ekor itu secara struktur (9.79 mata setahun hanya daripada henti). Dan pemicu yang sepatutnya membayar kembali kekurangan itu tidak mempunyai kelebihan pada mana-mana lebar henti.

Dua masalah berbeza, dan hanya satu daripadanya pernah dikaji selama ini.

| | Masalah | Pernah dikaji? |
|---|---|---|
| 1 | Pemicu tiada kelebihan | **Ya** — fasa 1, 1b, 2 SEC: semuanya DITOLAK |
| 2 | Pembinaan portfolio menjauhi ekor kanan kolam | **Tidak** — ini pengukuran pertama |

Itu mengubah soalan. Lima kajian bertanya "pemicu mana yang berfungsi?" dan jawapannya tetap tiada. Soalan yang belum ditanya ialah **"bolehkah pembinaan yang menerima ekor kanan mengalahkan penanda aras tanpa pemicu sama sekali?"** — iaitu kolam yang lebih baik, slot lebih banyak, tiada henti keras, dan membiarkan pemenang berjalan.

**Ia mungkin juga kalah.** Bahagian 2 menunjukkan membuang henti memperdalam persentil 5 daripada −15.58% kepada −54.67% setiap saham-tahun, dan `KEPEKATAN.md` menunjukkan menambah slot membeli MDD dengan pulangan. Perbezaannya ialah ini **belum** diukur sebagai satu pembinaan, manakala ruang pemicu sudah diukur dan kosong. Itu menjadikannya satu-satunya arah yang tinggal yang mempunyai maklumat baharu di dalamnya.

**Ia tidak akan mencapai +10%/bulan.** Tiada apa-apa dalam mana-mana nombor di atas menghampiri 3.14×/tahun. Lihat `SASARAN.md`.
