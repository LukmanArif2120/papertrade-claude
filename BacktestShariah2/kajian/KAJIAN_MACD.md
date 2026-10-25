# Kajian "MACD jadi positif" dan gabungan kaedah (25 Okt 2026)

Permintaan pengguna 25 Okt 2026: adakah MACD jadi positif satu isyarat yang baik, bolehkah kaedah digabung atau dicipta,
dan bolehkah sasaran 10% sebulan dicapai? Keutamaan pengguna: **konsisten** (untung dalam kebanyakan bulan; pulangan lebih
rendah diterima), tempoh pegang ikut data. Skrip: `kajian/macd/kaji_macd.py` (`sedia`, `peristiwa`, `sim`, `penapis`, `calon`,
`konsisten`). Hasil: `kajian/macd/*.csv`. Rekod kajian sahaja; tiada peraturan papertrade, Lejar atau dashboard diubah.

## Data dan kaedah
- **D431**: data_mentah set 431 (423 saham selepas 8 saham bermasalah dibuang), Nov 2019 – Okt 2026. Kaedah 134 direka atas
  data ini dan set ialah senarai Shariah hari ini (bias kemandirian): beli-pegang sama rata 24.6% setahun lawan SPY 16.0%.
- **D2000**: data AUTOTUNE (Release `autotune-data`), 2000 saham AS paling cair setiap bulan (titik masa, tutup > USD10),
  tanpa penapis Shariah dan tanpa saham delist. **Tempoh A 2010–2018** belum pernah dilihat semasa kaedah direka, dipakai
  untuk memilih. **Tempoh B Jan 2019 – Okt 2026** dan D431 untuk pengesahan.
- MACD (12, 26, 9), EMA standard. Isyarat pada tutup, beli buka esok, kos 0.1% setiap belah:
  - `Z` = garisan MACD silang ke atas 0 (maksud "MACD jadi positif").
  - `H` = histogram jadi positif (MACD silang ke atas garisan isyarat), di mana-mana; `Hn` = H ketika MACD < 0 (seperti M02
    tanpa SMA200); `Hp` = H ketika MACD > 0 (sambungan trend).
- Penapis pada hari isyarat: `F0` tiada; `FT` tutup > SMA200; `FT2` tutup > SMA50 > SMA200; `FR` RS ≥ 80; `FRT` FR + FT2.
  RS = formula `standard/kajian_rs.py` (D2000: dalam alam 2000 saham; D431: `kajian/rs/rs_pasaran_431.csv.gz`).
- `SEMUA` = kawalan: setiap hari penapis benar ialah calon (tanpa masa MACD). `SEMUA FR` susun ikut RS = cara RS_10.
- Keluar: kaedah (MACD < 0 bagi Z, histogram < 0 bagi H*), Chandelier tutup 4×ATR14 paras naik (lorong 2), atau 21 hari.
- Portfolio: 10 slot × 10% ekuiti (atau 20 × 5%), satu posisi setiap saham, slot diisi ikut RS tertinggi, ATR% terendah atau
  rawak. Enjin sama dengan `kajian/portfolio/kaji_portfolio.py`; semakan: RS_10 lorong 2 tanpa penapis D431 = 71.9% (kajian
  portfolio 72.6%).

## 1. Kajian peristiwa: adakah MACD jadi positif meramal pulangan?
Pulangan hadapan 21 hari dari buka esok. "Lebihan penapis" = purata isyarat tolak purata semua saham yang lulus penapis sama
pada hari sama (nilai tambah masa MACD), t Newey-West.

| Isyarat · penapis | D2000 A: lebihan · t | D2000 B: lebihan · t | D431: lebihan · t |
|---|---|---|---|
| Z · F0 | -0.09% · -1.05 | -0.09% · -0.59 | -0.06% · -0.24 |
| H · F0 | -0.02% · -0.40 | -0.13% · -1.06 | -0.13% · -0.86 |
| Hn · F0 | -0.04% · -0.36 | -0.07% · -0.40 | -0.06% · -0.25 |
| Hp · F0 | -0.19% · -1.87 | -0.32% · -1.73 | -0.12% · -0.49 |
| Z · FT2 | +0.04% · 0.37 | +0.15% · 0.96 | -0.09% · -0.30 |
| Z · FR | +0.21% · 1.02 | +0.10% · 0.31 | -0.29% · -0.58 |
| H · FR | -0.15% · -1.50 | -0.25% · -1.43 | -0.25% · -1.01 |

- Daripada 240 ujian (4 isyarat × 5 penapis × 4 tempoh pegang 5/10/21/63 hari × 3 tempoh data): **tiada satu pun t > 2**;
  11 ujian t < −2 (negatif). Kadar atasi SPY selepas isyarat 43–54%, iaitu seperti lambungan syiling.
- Kesimpulan: MACD jadi positif (garisan atau histogram) **tidak meramal** pulangan saham individu melebihi apa yang sudah
  diberi oleh trend/RS. Selari dengan literatur: MACD pada saham individu lemah selepas kos dan tidak teguh merentas pasaran
  (rujukan di hujung).

## 2. MACD sebagai penapis kepada 134 kaedah sedia ada (D431)
Semua dagangan enjin v1.2 (`kaji_lorong2.py jana`), dibahagi ikut keadaan MACD pada hari isyarat.

| Penapis | Kaedah lebih baik bila ya (L1 / L2) | Beza lebihan SPY, hari sama (L1 · t / L2 · t) | RS_10 L2 CAGR (tiada penapis 71.9%) |
|---|---|---|---|
| Histogram > 0 | 81/114 · 79/114 | +0.60% · 1.84 / +0.29% · 0.49 | 73.4% |
| MACD > 0 | 57/91 · 42/91 | +0.20% · 0.64 / +0.08% · 0.13 | 50.1% |
| MACD naik 5 hari | – | – | 65.8% |

- Histogram > 0 memberi kelebihan kecil setiap dagangan lorong 1 (+0.6%, t 1.84, tidak signifikan, dalam sampel sahaja) dan
  tiada kesan pada portfolio. MACD > 0 tiada kelebihan dan menurunkan CAGR RS_10. **Tidak dicadangkan sebagai penapis.**

## 3. Kaedah MACD sendiri dan gabungan (portfolio 10 slot, susun RS)
Sel: CAGR % · MDD % · Sharpe bulanan · bulan untung · bulan terburuk % · bulan ≥ +10%.

| Konfigurasi | D2000 A (2010–2018) | D2000 B (2019–2026) | D431 (2019–2026) |
|---|---|---|---|
| SPY | 11.6 · -19 · 0.95 · 69% · -9 · 1% | 17.1 · -34 · 1.05 · 67% · -12 · 3% | 16.0 · -34 · 0.97 · 65% · -12 · 4% |
| Sama rata alam | 11.2 · -26 · 0.79 · 67% · -11 · 2% | 11.9 · -42 · 0.65 · 61% · -20 · 4% | 24.6 · -41 · 1.11 · 63% · -20 · 7% |
| Z F0 Chandelier | 18.5 · -27 · 1.00 · 65% · -16 · 4% | 2.5 · -51 · 0.23 · 52% · -18 · 10% | 18.4 · -36 · 0.77 · 64% · -20 · 13% |
| Z FT2 Chandelier | 12.8 · -27 · 0.76 · 63% · -21 · 3% | 9.2 · -39 · 0.43 · 57% · -16 · 11% | 19.3 · -35 · 0.77 · 58% · -14 · 17% |
| Z FR Chandelier | 13.4 · -38 · 0.70 · 65% · -19 · 8% | 14.2 · -49 · 0.56 · 54% · -17 · 17% | 25.6 · -32 · 0.92 · 54% · -17 · 19% |
| Z FR keluar MACD < 0 | 4.7 · -40 · 0.32 · 57% · -17 · 8% | 3.6 · -46 · 0.27 · 50% · -23 · 14% | 19.4 · -36 · 0.76 · 51% · -17 · 14% |
| H F0 Chandelier | 6.6 · -44 · 0.39 · 61% · -20 · 6% | -0.6 · -68 · 0.16 · 54% · -22 · 14% | 26.5 · -39 · 0.84 · 56% · -24 · 18% |
| Hp FT2 Chandelier | 8.9 · -37 · 0.51 · 63% · -15 · 7% | 15.3 · -55 · 0.59 · 59% · -18 · 13% | 32.2 · -36 · 1.07 · 62% · -23 · 18% |
| SEMUA FR Chandelier (= RS_10) | -9.5 · -78 · -0.12 · 52% · -29 · 11% | 6.5 · -76 · 0.36 · 52% · -31 · 29% | 81.1 · -57 · 1.51 · 67% · -28 · 38% |

- Daripada 70 konfigurasi grid, **0 mengatasi SPY dalam kedua-dua tempoh D2000**, dan 0 mempunyai Sharpe bulanan di atas SPY
  dalam tempoh B. Keluar ikut MACD (MACD/histogram < 0) lebih lemah daripada Chandelier dalam 54/60 perbandingan.
- Pilihan pra-daftar (`calon`: Sharpe tertinggi dalam D2000 A, CAGR > SPY, ≥ 20 dagangan setahun) = Z F0 Chandelier. Ia gagal
  pengesahan: D2000 B 2.5% (SPY 17.1%), D431 18.4% (sama rata 24.6%); susunan rawak isyarat sama 7.8% / 5.6% / 14.0%.

## 4. Reka bentuk untuk konsisten
48 konfigurasi (Z dan kawalan SEMUA × F0/FT2/FR × susun RS / ATR% terendah × 10/20 slot × rejim SPY > SMA200), keluar Chandelier.

| Konfigurasi | D2000 A | D2000 B | D431 |
|---|---|---|---|
| SEMUA FR, ATR% rendah, 20 slot (pilihan pra-daftar) | 14.5 · -20 · 1.25 · 67% · -9 · 0% | 8.1 · -30 · 0.61 · 59% · -11 · 0% | 8.8 · -33 · 0.59 · 60% · -13 · 1% |
| Z FT2, ATR% rendah, 20 slot (paling stabil, pasca-hoc) | 11.8 · -16 · 0.99 · 69% · -10 · 0% | 10.6 · -30 · 0.67 · 62% · -17 · 3% | 19.3 · -27 · 1.04 · 68% · -10 · 6% |
| SEMUA F0, ATR% rendah, 10 slot, rejim | 8.0 · -11 · 1.00 · 63% · -6 · 0% | 5.5 · -18 · 0.57 · 59% · -8 · 1% | 9.6 · -20 · 0.72 · 58% · -10 · 2% |
| SEMUA FR, RS, 20 slot | -7.2 · -75 · -0.11 · 56% · -23 · 8% | 3.1 · -70 · 0.28 · 53% · -27 · 20% | 62.9 · -44 · 1.49 · 67% · -23 · 30% |

- Pilihan pra-daftar (Sharpe tertinggi D2000 A dengan CAGR > SPY) gagal pengesahan (B 8.1%, D431 8.8%; susunan rawak 20 benih
  median 10.7% / 31.9%). Daripada 48 konfigurasi, 0 mengatasi SPY dalam kedua-dua tempoh D2000.
- Susun ikut ATR% rendah dan 20 slot menurunkan MDD dan bulan terburuk, tetapi pulangan turun ke bawah SPY. Penapis rejim SPY
  > SMA200 menurunkan CAGR dalam hampir semua konfigurasi (sama dengan kajian portfolio).
- Konfigurasi paling stabil merentas tiga set (Z FT2 ATR% rendah 20 slot: Sharpe 0.99 / 0.67 / 1.04, bulan untung 69 / 62 / 68%)
  dipilih selepas melihat tempoh pengesahan (pasca-hoc), dan masih di bawah SPY dalam tempoh B (10.6% lawan 17.1%).

## 5. Amaran: kelebihan RS_10 bergantung pada set 431
- Dalam D431, purata setiap calon dagangan (semua isyarat) +5.1% hingga +5.6%; dalam D2000 +1.5% hingga +2.5%. Set 431 sendiri
  naik lebih cepat daripada pasaran (bias kemandirian).
- Cara RS_10 (isi slot dengan RS tertinggi, Chandelier) memberi 75–81% setahun dalam D431, tetapi dalam 2000 saham AS:
  −9.5% hingga −11.2% (2010–2018) dan 6.5–10.4% (2019–2026), MDD −71% hingga −82%. Semakan dagangan: kerugian datang daripada
  peristiwa sebenar saham RS 99 dengan ATR ~6% (cth. GSAT −63% Mei 2016, NKTR −40% 2018, PBYI), bukan ralat data.
- D2000 tiada penapis Shariah dan RS dikira dalam alam 2000 saham, jadi ia bukan replika tepat Lejar. Namun alam hadapan Lejar
  (seluruh pasaran Shariah ≥ USD10, termasuk saham yang kemudian gagal) lebih menyerupai D2000 daripada D431. Jejak hadapan
  RS_10 diteruskan sebagai rekod; ia tidak patut dianggap terbukti.

## 6. Sasaran 10% sebulan
- 10% sebulan = ~214% setahun. Tiada konfigurasi dalam kajian ini (118 portfolio) atau kajian portfolio sebelumnya mencapainya
  secara konsisten.
- Bulan ≥ +10% memang berlaku: SPY 1–4% bulan; konfigurasi agresif (RS_10) 11–40% bulan, tetapi disertai bulan −28% hingga
  −35% dan MDD −57% hingga −82%. Posisi papertrade yang naik > 10% (383 daripada 5525 posisi C, 8–23 Okt 2026) ialah ekor kanan
  posisi individu, bukan pulangan portfolio bulanan.
- Bagi keutamaan konsisten, sasaran realistik daripada data: purata ~1–1.5% sebulan dengan ~2/3 bulan untung dan bulan terburuk
  sekitar −9% hingga −17%. Pada ukuran ini SPY (Sharpe bulanan 0.95–1.05, 65–69% bulan untung) tidak dikalahkan oleh mana-mana
  konfigurasi dalam tempoh pengesahan D2000 B.

## Keputusan kajian (rekod; perubahan peraturan memerlukan keputusan pengguna)
1. MACD jadi positif tidak digunakan sebagai pencetus beli atau penapis.
2. Tiada kaedah MACD/gabungan baharu dimasukkan ke Lejar Penuh: pilihan pra-daftar gagal pengesahan (syarat skop 25 Okt 2026:
   masuk Lejar hanya jika lulus).
3. Sebarang kaedah atau portfolio yang dicadang untuk modal sebenar perlu lulus D2000 tempoh A dan B (mengatasi SPY dengan MDD
   setanding), bukan D431 sahaja. Papan Penganalisis sudah menunjukkan 0 kaedah lulus semakan 2000 saham AS.
4. Calon jejak hadapan jika pengguna mahu (pasca-hoc, belum terbukti): Z FT2 (MACD silang atas 0, tutup > SMA50 > SMA200),
   susun ATR% terendah, 20 slot × 5%, keluar Chandelier 4×ATR14.

## Batasan
- D2000 tiada saham delist (keputusan ialah had atas) dan tiada penapis Shariah. D431 berbias kemandirian.
- RS D2000 dikira dalam alam 2000 saham (bukan seluruh pasaran ≥ USD5 seperti `data/rs/`).
- Masuk pada buka, kos 0.1% setiap belah, tiada slippage tambahan.
- Satu set parameter MACD (12, 26, 9); parameter lain tidak ditala untuk mengelak pemadanan lampau.

## Rujukan luar
- [Stock Market Efficiency and the MACD. Evidence from Countries around the World](https://c.mql5.com/forextsd/forum/219/Stock%20Market%20Efficiency%20and%20the%20MACD.%20Evidence%20from%20Countries%20around%20the%20World.pdf): 1336 syarikat 2001–2012; MACD hanya kadang-kadang dan bagi sesetengah syarikat memberi pulangan luar biasa selepas kos.
- [The profitability of MACD and RSI trading rules in the Australian stock market](https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-4-cont-9/the-profitability-of-macd-and-rsi-trading-rules-in-the-australian-stock-market): MACD secara umum lemah, 1996–2014.
- [JRFM 14(1):37](https://doi.org/10.3390/jrfm14010037): ulasan yang menyatakan peraturan MACD (12,26,0), (12,26,9), (8,17,9) tidak teguh terhadap pilihan pasaran.
- [Man Group, "Mo' Momentum, Mo' Problems"](https://www.man.com/insights/mo-momentum-mo-problems) dan [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/time-series-and-dual-momentum-for-individual-stocks/): gabungan momentum siri masa + rentas keratan mengurangkan kejatuhan dalam data aset berbilang; bukti peringkat saham lebih nipis.
