# Kajian "MACD jadi positif", MA10 silang MA20 dan gabungan kaedah (25–26 Okt 2026)

Permintaan pengguna 25 Okt 2026: adakah MACD jadi positif satu isyarat yang baik, bolehkah kaedah digabung atau dicipta,
dan bolehkah sasaran 10% sebulan dicapai? Keutamaan pengguna: **konsisten** (untung dalam kebanyakan bulan; pulangan lebih
rendah diterima), tempoh pegang ikut data. Skrip: `kajian/macd/kaji_macd.py` (`sedia`, `peristiwa`, `sim`, `penapis`, `calon`,
`konsisten`, `ma`, `pakej`). Hasil: `kajian/macd/*.csv`. Rekod kajian sahaja; tiada peraturan papertrade, Lejar atau dashboard diubah.

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

## 7. MA10 silang MA20 (permintaan pengguna 25 Okt 2026)
Rangka sama (`kaji_macd.py ma`; `ma_peristiwa.csv`, `ma_grid.csv`, `ma_calon.csv`). `XS` = SMA10 silang ke atas SMA20, `XE` =
EMA10 silang ke atas EMA20. Keluar kaedah = MA10 silang ke bawah MA20 (jual buka esok). Kaedah sedia ada yang hampir sama:
M20 EMA10/15 + sudut dan M161 EMA10/21 + Supertrend (kedua-duanya gagal semakan 2000 saham AS dalam Papan Penganalisis).

- Kajian peristiwa (120 ujian): **tiada t > 2**, 4 ujian t < −2; kadar atasi SPY 43–51%. Contoh 21 hari, lebihan atas penapis:
  XS F0 −0.04% / −0.13% / −0.02% (t −0.42 / −1.13 / −0.11); XE F0 −0.06% / −0.12% / +0.16% (t −0.74 / −0.94 / 0.75)
  bagi D2000 A / D2000 B / D431.
- Portfolio (40 konfigurasi; sel seperti §3):

| Konfigurasi | D2000 A | D2000 B | D431 |
|---|---|---|---|
| XS F0, keluar MA10 < MA20, RS 10 slot | 0.7 · -44 · 0.14 · 46% · -15 · 5% | -2.3 · -58 · 0.10 · 48% · -24 · 16% | 21.9 · -34 · 0.84 · 61% · -22 · 13% |
| XE F0, keluar MA10 < MA20, RS 10 slot | 2.8 · -49 · 0.24 · 58% · -18 · 5% | -1.3 · -60 · 0.11 · 56% · -21 · 12% | 34.0 · -29 · 1.19 · 60% · -16 · 14% |
| XS F0 Chandelier, RS 10 slot | 16.8 · -40 · 0.79 · 65% · -17 · 11% | 3.1 · -59 · 0.26 · 52% · -32 · 11% | 28.5 · -41 · 0.93 · 62% · -17 · 18% |
| XE FR Chandelier, RS 10 slot | 7.4 · -42 · 0.43 · 57% · -17 · 9% | 6.8 · -60 · 0.36 · 56% · -25 · 20% | 41.7 · -27 · 1.29 · 61% · -15 · 24% |
| XS FRT Chandelier, ATR% rendah 20 slot (pilihan pra-daftar) | 12.5 · -26 · 0.86 · 65% · -11 · 0% | 9.0 · -35 · 0.52 · 56% · -18 · 9% | 22.3 · -23 · 0.95 · 58% · -20 · 14% |
| XE FT2 Chandelier, ATR% rendah 20 slot (paling stabil, pasca-hoc) | 9.2 · -23 · 0.80 · 64% · -10 · 0% | 11.1 · -33 · 0.73 · 64% · -19 · 2% | 19.7 · -23 · 0.97 · 63% · -12 · 8% |

- **0/40 mengatasi SPY dalam kedua-dua tempoh D2000**; 0 mengatasi SPY dalam tempoh B. Silang MA klasik (masuk silang naik,
  keluar silang turun): kadar menang 33–39%, purata +0.7% setiap dagangan dalam D2000, pegang ~21 hari, ~115 dagangan setahun;
  hanya D431 yang menunjukkan untung (bias set). Chandelier lebih baik daripada keluar MA dalam 22/30 perbandingan.
- Pilihan pra-daftar (XS FRT, ATR% rendah, 20 slot) gagal pengesahan: D2000 B 9.0% (SPY 17.1%), D431 22.3% (sama rata 24.6%);
  susunan rawak 20 benih median 10.3% / 25.0%, iaitu susunan tidak menambah nilai.
- Konfigurasi paling stabil (XE FT2 ATR% rendah 20 slot) hampir sama dengan calon MACD Z FT2 (§4): kestabilan datang daripada
  penapis trend + ATR% rendah + 20 slot + Chandelier, bukan daripada pencetus (MACD atau MA).

## 8. Pakej konsisten: momentum dipelbagai + RSI(2) pullback + gabungan 50/50 (keputusan pengguna 26 Okt 2026)
`kaji_macd.py pakej` (`pakej.csv`, `pakej_pilih.json`). Reka bentuk dan peraturan lulus ditetapkan sebelum larian:
- MOM: pada buka hari dagangan pertama setiap bulan, pegang 30 atau 50 saham RS tertinggi sama berat; dengan/tanpa rejim
  (SPY < SMA200 pada tutup semalam -> tunai). Kos 0.1% setiap belah atas bahagian yang bertukar.
- RSI2 (Connors): RSI(2) < 5 atau < 10 dan tutup > SMA200; jual buka esok selepas tutup > SMA5, maksimum 10 hari; 10 atau 20
  slot; susun RSI(2) terendah atau RS tertinggi.
- Setiap bahagian dipilih ikut Sharpe bulanan tertinggi dalam D2000 A; gabungan 50/50 diseimbang setiap hari. LULUS jika
  Sharpe bulanan gabungan > SPY dalam D2000 B dan D431.

| Konfigurasi | D2000 A | D2000 B | D431 |
|---|---|---|---|
| SPY | 11.6 · -19 · 0.95 · 69% · -9 · 1% | 17.1 · -34 · 1.05 · 67% · -12 · 3% | 16.0 · -34 · 0.97 · 65% · -12 · 4% |
| Sama rata alam | 11.2 · -26 · 0.79 · 67% · -11 · 2% | 11.9 · -42 · 0.65 · 61% · -20 · 4% | 24.6 · -41 · 1.11 · 63% · -20 · 7% |
| MOM 50 saham | 5.8 · -41 · 0.36 · 60% · -19 · 6% | 12.4 · -61 · 0.50 · 55% · -23 · 17% | 44.8 · -36 · 1.41 · 68% · -25 · 20% |
| MOM 50 saham rejim (terpilih) | 8.5 · -39 · 0.52 · 56% · -19 · 4% | -1.8 · -67 · 0.09 · 46% · -23 · 10% | 29.6 · -33 · 1.18 · 57% · -25 · 12% |
| RSI2 < 5, 20 slot, susun RS (terpilih) | 2.5 · -32 · 0.24 · 61% · -14 · 0% | -0.3 · -49 · 0.12 · 51% · -30 · 9% | 14.4 · -33 · 0.84 · 68% · -18 · 1% |
| Z FT2 ATR% rendah 20 slot (§4) | 11.7 · -16 · 0.99 · 69% · -10 · 0% | 10.6 · -30 · 0.67 · 62% · -17 · 3% | 19.3 · -27 · 1.04 · 68% · -10 · 6% |
| Gabungan MOM + RSI2 (pra-daftar) | 5.8 · -32 · 0.43 · 57% · -16 · 1% | -0.0 · -53 · 0.12 · 52% · -18 · 5% | 22.7 · -20 · 1.24 · 68% · -9 · 6% |
| Gabungan Z FT2 + RSI2 | 7.3 · -19 · 0.63 · 66% · -11 · 0% | 5.9 · -35 · 0.39 · 57% · -23 · 1% | 17.4 · -25 · 1.08 · 68% · -13 · 1% |
| Gabungan MOM + Z FT2 | 10.6 · -28 · 0.78 · 67% · -14 · 0% | 5.7 · -41 · 0.37 · 53% · -13 · 4% | 25.1 · -22 · 1.26 · 69% · -15 · 8% |

- **Gabungan pra-daftar GAGAL**: Sharpe bulanan 0.12 (D2000 B) dan 1.24 (D431) lawan SPY 1.05 dan 0.97.
- MOM 30–50 saham (1.5–2.5% teratas alam) lemah dalam D2000 (2.5–12.4% setahun, MDD −39% hingga −74%). Kajian RS seluruh pasaran
  (§15 `kajian/rs/RINGKASAN.md`) menunjukkan 10% teratas (~300 saham) mengatasi purata pasaran; hujung paling atas tidak.
  Rejim SPY > SMA200 membantu 2010–2018 tetapi merosakkan 2019–2026 (pemulihan pantas 2020).
- RSI2: kadar menang 60–63% (sama dengan literatur), tetapi purata setiap dagangan −0.05% hingga +0.16% dalam D2000 selepas kos
  0.2% pergi-balik, dengan 560–1220 dagangan setahun. Kelebihan yang pernah dilaporkan tidak kekal selepas kos.
- Korelasi bulanan antara bahagian 0.36–0.65: semuanya beli saham sahaja, jadi faedah kepelbagaian terhad.
- Penanda aras yang adil bagi pemilihan sama berat ialah "sama rata alam" (D2000 B: 11.9%, MDD −42%), bukan SPY yang berwajaran
  modal pasaran (17.1%; syarikat gergasi mendahului 2019–2026). Berbanding sama rata alam, Z FT2 ATR% rendah 20 slot memberi
  pulangan hampir sama dengan MDD lebih kecil (−16% / −30% / −27% lawan −26% / −42% / −41%), Sharpe bulanan lebih tinggi
  dalam D2000 A dan B (0.99 / 0.67 lawan 0.79 / 0.65), hampir sama dalam D431 (1.04 lawan 1.11), dan 62–69% bulan untung. Ini ciri paling
  konsisten yang ditemui; ia masih di bawah SPY.

## Keputusan kajian (rekod; perubahan peraturan memerlukan keputusan pengguna)
1. MACD jadi positif dan MA10 silang MA20 (SMA atau EMA) tidak digunakan sebagai pencetus beli atau penapis. Momentum
   30–50 saham dan RSI(2) pullback juga gagal (§8).
2. Tiada kaedah MACD/MA/gabungan baharu dimasukkan ke Lejar Penuh: pilihan pra-daftar gagal pengesahan (syarat skop 25 Okt 2026:
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
