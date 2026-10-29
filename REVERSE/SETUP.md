# Setup gaya pedagang: jalur tengah, urutan, 3 syarat

Dijana 2026-10-29 12:22 UTC oleh `REVERSE/step15_setup.py`. Pradaftar `REVERSE/SPEC_SETUP.md` (dikomit sebelum larian ini).

## Keputusan Gate A: **DITOLAK**

Tiga perkara yang fasa 1 **tidak** uji, diuji di sini: jalur **tengah** (RSI 45–60, bukan kuintil hujung), **urutan** masa (MACD silang dahulu kemudian golden cross), dan **3** syarat serentak. Populasi juga lebih luas: setiap bar dalam alam, bukan peristiwa sah sahaja.

**Pecahan masa mengawal pemilihan:** 672 setup dinilai pada LATIH 2012–2019, 10 teratas dipilih, dan **hanya** 10 itu diuji pada TAHAN 2020–2025. Keluarga ujian tahan ialah 10, bukan 672.

## 10 setup terpilih, diuji pada tahan 2020–2025

| Setup | n | Menang | Untung purata | Rugi purata | Jangkaan | Tanpa 5% teratas | p | Tahun + | Gate A |
|---|---|---|---|---|---|---|---|---|---|
| `hari_macd_cross<=5 & stoch_k[20,50] & vol_n50>=1.2` | 29,074 | 34.7% | +23.16% | -8.65% | **+2.375%** | -1.103% | 0.0010 | 4/6 | tidak |
| `hari_macd_cross<=5 & rsi14[40,55] & vol_n50>=1.2` | 59,843 | 33.5% | +20.92% | -8.18% | **+1.557%** | -1.452% | 0.0010 | 4/6 | tidak |
| `hari_macd_cross<=3 & rsi14[40,55] & vol_n50>=1.2` | 42,007 | 33.4% | +21.09% | -8.27% | **+1.538%** | -1.494% | 0.0010 | 4/6 | tidak |
| `hari_macd_cross<=5 & stoch_k[20,50] & tiada` | 131,175 | 32.4% | +22.50% | -8.57% | **+1.505%** | -1.748% | 0.0010 | 4/6 | tidak |
| `macd_cross & stoch_k[40,70] & tiada` | 42,368 | 32.3% | +20.91% | -8.15% | **+1.226%** | -1.717% | 0.0080 | 4/6 | tidak |
| `macd_cross & rsi14[40,55] & tiada` | 55,006 | 32.0% | +20.47% | -8.07% | **+1.057%** | -1.816% | 0.0090 | 4/6 | tidak |
| `macd_cross & stoch_k[20,50] & tiada` | 22,664 | 31.9% | +22.47% | -9.00% | **+1.029%** | -2.124% | 0.0020 | 4/6 | tidak |
| `macd_cross & bb_pctb[40,70] & tiada` | 45,505 | 31.4% | +20.06% | -7.95% | **+0.848%** | -1.974% | 0.7572 | 4/6 | tidak |
| `ema_crossback & stoch_k[40,70] & vol_n50>=1.2` | 11,347 | 30.0% | +20.10% | -7.44% | **+0.817%** | -2.001% | 0.6703 | 4/6 | tidak |
| `ema_crossback & rsi14[40,55] & vol_n50>=1.2` | 12,145 | 30.0% | +19.77% | -7.45% | **+0.723%** | -2.073% | 0.7982 | 4/6 | tidak |

## Lift atas "beli setiap bar" — dan kesilapan reka bentuk saya

**Spec §4 memilih 10 teratas ikut jangkaan MUTLAK. Itu kesilapan saya.** Jangkaan mutlak bukan ukuran kelebihan: setup mesti dibanding dengan alternatifnya, iaitu **tidak memilih sama sekali**.

| Tingkap | Beli SETIAP bar | Menang | Median dagangan | Tanpa 5% teratas |
|---|---|---|---|---|
| LATIH 2012–2019 (4,517,324 bar) | **+1.472%** | 33.2% | -3.80% | -1.608% |
| TAHAN 2020–2025 (4,593,112 bar) | **+3.032%** | 30.9% | -5.19% | -2.410% |

Lift setiap setup = jangkaannya − +1.472%. Merentas **598 setup** dengan n ≥ 500 pada tingkap LATIH:

- lift maksimum: **-0.134 mata** · median -0.832 · minimum -1.849
- setup dengan lift **POSITIF**: **0 daripada 598**

**Tiada satu pun daripada 672 setup mengalahkan "beli setiap bar" — bahkan pada tingkap latihan tempat ia dipilih.** Setup terbaik masih 0.134 mata DI BAWAH entri rawak.

Itu bermakna kesilapan reka bentuk saya **tidak mengubah keputusan** — ia menjadikannya lebih jelas. Memilih ikut lift tidak akan memberi calon yang lebih baik kerana senarai lift tidak mempunyai satu pun entri positif. Tiada larian semula diperlukan.

Sebabnya boleh dinyatakan terus: **setiap setup ialah PENAPIS**, dan setiap penapis membuang bar. Taburan pulangan saham tunggal sangat terpencong kanan (dagangan median -5.19% tetapi min +3.032%), jadi membuang bar terutamanya membuang **peluang pada ekor**. Menapis mengurangkan pendedahan anda kepada satu-satunya bahagian yang membayar.

### Adakah gate "tanpa 5% teratas" itu adil? Indeks lulus dengan mudah.

| Instrumen | Jangkaan 63 sesi | Menang | Tanpa 5% teratas |
|---|---|---|---|
| Saham tunggal, semua bar | +3.032% | 30.9% | **-2.410%** |
| SPY (indeks) | +4.131% | 76.7% | **+3.356%** |
| QQQ (indeks) | +5.534% | 74.8% | **+4.419%** |

Gate itu **tidak** salah tentukur. Indeks melepasinya dengan mudah dan kadar menangnya ~77% berbanding ~31% bagi saham tunggal. Sebabnya: **indeks ITULAH kepelbagaian merentas ekor**. Ia tidak perlu menangkap pemenang 5% teratas kerana ia memegang kesemuanya.

## Kadar menang BUKAN keuntungan — ini buktinya daripada 672 setup

Merentas **598 setup** yang mempunyai ≥ 500 dagangan pada tingkap latih, korelasi antara **kadar menang** dan **jangkaan** ialah Spearman rho **+0.859** (p 0.0000).

- Kadar menang tertinggi: **36.1%**, jangkaannya +1.228%
- 50 setup dengan kadar menang TERTINGGI: jangkaan median **+1.057%**, dan **0 daripada 50 adalah NEGATIF**
- Jangkaan tertinggi: +1.339%, kadar menangnya 36.1%

Premis "70% menang, 30% gagal ditampung henti" separuh betul. Kadar menang 70% pada +1% dengan 30% rugi pada −4% memberi jangkaan **−0.5%**. Jadual di atas memaparkan untung purata dan rugi purata bersebelahan supaya ini boleh dilihat terus — perhatikan bahawa setup dengan kadar menang tinggi mempunyai **untung purata kecil**, dan itulah yang memakannya.

## Tafsiran

**Tiada setup lulus Gate A.** Tetapi bacaan yang betul lebih halus daripada "setup tidak berfungsi", dan ia penting:

1. **Setup itu BERTAHAN di luar sampel.** Jangkaan latih +1.14% hingga +1.34%; jangkaan tahan **+0.723% hingga +2.375%**. Kesepuluh positif, dan beberapa LEBIH TINGGI daripada latih. Jangkaan priori saya dalam spec §7 menjangka ia reput; ia tidak.
2. **Tetapi liftnya negatif pada kedua-dua tingkap.** Setup positif tetapi kurang positif daripada tidak menapis sama sekali.
3. Gate A gagal pada SATU syarat: jangkaan selepas membuang 5% pemenang teratas. Kesepuluh negatif di sana, dan begitu juga asas.

- lulus `FDR`: **5** daripada 10
- lulus `n ≥ 200`: **10** daripada 10
- lulus `jangkaan tanpa 5% teratas > 0`: **0** daripada 10
- lulus `bootstrap blok`: **8** daripada 10
- lulus `≥ 4/6 tahun positif`: **10** daripada 10

Maksudnya setup yang nampak terbaik pada 8 tahun latihan **tidak kekal** pada 6 tahun seterusnya. Itu tandatangan pemilihan atas hingar, bukan kelebihan: menilai 672 setup menghasilkan pemenang latih walaupun tiada satu pun mempunyai kelebihan sebenar.

Ini **bukan** kerana syaratnya terlalu ketat. Jalur yang diuji di sini ialah yang paling longgar dalam keseluruhan kajian: julat tengah selebar 15 mata RSI, penapis trend ringkas, dan pilihan "tiada penapis" sebagai kawalan.

## Had

- Alam Release `autotune-data-a02`, **bukan** ditapis Syariah.
- `ETRAIL` diimbas maksimum 126 sesi; jika Chandelier tidak tercetus, posisi ditutup pada hujung tingkap itu. Keputusan Gate A dinilai pada `E63S` (keluaran yang dipakai seluruh kajian), bukan `ETRAIL`.
- Ambang jalur dan penapis ditetapkan dalam spec §3 sebelum larian dan **tidak ditala**. Menala ambang akan memerlukan pradaftar baharu dan akan melanggar larangan penalaan dalam `ARAHAN`.
- Lajur indikator daripada cache `signals_*.parquet` fasa 1 (dikira step1 tanpa pandang hadapan), jadi ia tepat lajur yang sama yang fasa 1 nilai.

**Ia tidak mencapai +10%/bulan.** Lihat `SASARAN.md`.
