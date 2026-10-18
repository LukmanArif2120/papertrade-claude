# Kajian gred Sektor dan Industri (18 Okt 2026)

Keputusan pengguna 18 Okt 2026: laksanakan gred Industri **Weinstein + 1 bulan** dan gred Sektor **% saham > SMA200** (paparan sahaja), rekod sahaja, bukan penapis. Pelaksanaan: `standard/gred_kumpulan.py`, `.github/workflows/gred_kumpulan.yml`, `standard/gred.py tambah --kumpulan` (tugasan_v3 §8).

Data dan skrip kajian: cawangan `kajian-gred` (`BacktestShariah2/kajian/gred_pasaran.py`, `kajian/data/kumpulan_harian.csv.gz`, `panel_20sesi.csv.gz`, `meta_saham.csv`; workflow `kajian_gred.yml`).

## Data
- 5,546 / 5,634 ticker `papertrade/peta_industri.csv` (yfinance, Jun 2017–16 Okt 2026; 88 gagal). Industri = plate Moomoo (141 industri ≥ 3 saham), sektor = 11 sektor Morningstar (`SEKTOR_INDUSTRI`). Saham layak: tutup semalam ≥ USD5.
- Indeks kumpulan = purata sama rata pulangan harian ahli layak (dipotong −50% … +100%).
- Bias diketahui: saham yang dinyahsenarai tiada (survivorship). Indeks sama rata, bukan nilai pasaran.

## Tiga ujian bebas
1. **Dagangan kaedah**: semua dagangan enjin v1.2 134 kaedah, set 431, isyarat Nov 2019–2026 (~759 ribu). Pulangan relatif = pulangan dagangan − purata semua dagangan tarikh isyarat sama. Kaedah momentum (119) / pantulan (15) ikut median pulangan 20 hari sebelum isyarat (`kod/jenis_kaedah.csv`). t = t-stat beza atas 20% − bawah 20% ikut bulan.
2. **Panel pasaran**: semua saham layak setiap 20 sesi (tidak bertindih; ~238 ribu pemerhatian, nilai dagangan ≥ USD2 juta), pulangan 20 sesi relatif purata tarikh.
3. **Indeks kumpulan**: pulangan hadapan indeks industri/sektor itu sendiri (5, 21, 63 sesi, tidak bertindih), relatif purata kumpulan. Juga ikut H1 (2019–2022) / H2 (2023–2026) dan rejim (SPY > / < SMA200).

## Pandangan pakar yang diuji (peringkat industri; t dagangan kaedah momentum / panel / indeks 21 sesi)
| Pakar / definisi | Dagangan | Panel | Indeks 21 | Nota |
|---|---|---|---|---|
| v1 sekarang (1W/1M/3M + breadth) | 1.21 | 1.10 | 1.78 | 1 minggu sendiri t 0.3 (pembalikan jangka pendek) |
| Moskowitz–Grinblatt / Arnott: 1 bulan | 2.59 | 1.00 | 2.15 | tersusun A→E dalam dagangan |
| Weinstein Peringkat 2 | 2.77 | 1.62 | 2.35 (5 sesi) | kukuh H1 dan H2 |
| Moskowitz–Grinblatt: 12−1 bulan | 0.77 | – | 3.69 | menyusun indeks, lemah untuk dagangan |
| IBD median RS / 3-6-9-12 | 1.57 | – | 2.83 | |
| % saham > SMA200 | 1.32 | – | 3.26 | |
| O'Neil % saham RS ≥ 80 | 3.48 | 0.49 | 1.83 | |
| O'Neil RS 3 pemimpin | 2.39 | −0.30 | – | |
| O'Neil volum naik/turun | 1.59 | 0.47 | 1.25 | |
| de Kempenaer RRG | 2.35 | 1.04 | −0.81 | |
| George–Hwang / Hong–Jordan–Liu: dekat 52 minggu | −0.02 | 0.76 | 2.25 | |
| Minervini % saham di paras 52 minggu | −2.18 | 1.69 | 0.83 | terbalik untuk dagangan |
| Novy-Marx 12−7 bulan | 0.72 | 0.82 | – | |
| Pring / Stovall kitaran ekonomi | – | – | – | tidak diuji; Molchanov & Stangl (2023): tidak terbukti |

## Calon gabungan (t: dagangan / panel / indeks 21 / indeks 63)
| Definisi | t | Susunan dagangan A..E (% relatif) |
|---|---|---|
| **Weinstein + 1 bulan (dipilih)** | 2.72 / 2.09 / 2.67 / 3.90 | +0.17 +0.05 −0.30 −0.72 −1.04 |
| Weinstein + 1 bulan + 12−1 | 3.02 / 2.17 / 3.37 / 5.31 | +0.02 −0.39 +0.08 −0.21 −1.17 |
| Weinstein + 1 bulan + median RS | 3.18 / 2.33 / 2.72 / 4.33 | +0.10 −0.19 −0.05 −0.39 −1.30 |

Gabungan dengan komponen jangka panjang lebih kuat untuk indeks, tetapi B–D bercampur dalam dagangan. Weinstein + 1 bulan sahaja tersusun A→E dalam ketiga-tiga ujian. Pelicinan skor (purata 5–21 hari) melemahkan kesan dagangan, jadi tidak dilicinkan (gred bertukar purata setiap ~3 hari; direkod pada hari isyarat sahaja).

## Kalibrasi Weinstein + 1 bulan (purata, julat keyakinan 95%)
- Dagangan kaedah momentum: A +0.03 [−0.67, +0.73], B −0.18, C −0.40, D −0.89 [−1.66, −0.13], E −1.21 [−2.09, −0.34]. Kadar menang A 37.0% … E 35.7%.
- Panel 20 sesi: A +0.65 [+0.12, +1.18], B +0.27, C −0.15, D −0.16, E −0.44.
- Indeks industri 21 sesi: A +0.62 [+0.10, +1.13], B −0.03, C +0.02, D −0.14, E −0.69 [−1.24, −0.15].
- Bacaan: A = kuat, B–D = neutral, E = lemah. Semasa pasaran beruang (SPY < SMA200) kesan 21 sesi hampir sifar; pada 63 sesi kekal.
- Kaedah pantulan: arah kesan tidak konsisten → gred industri tidak terpakai.

## Sektor
Gred sektor menyusun pulangan indeks sektor (% > SMA200 t 3.2 pada 21 sesi; Weinstein t 2.6) tetapi tidak membantu memilih saham (semua definisi t < 2 atau bertukar arah H1/H2 dalam dagangan dan panel). Selaras dengan O'Neil (37% pergerakan saham daripada industri, 12% daripada sektor) dan Arnott et al. (momentum industri ialah momentum faktor). Gred Sektor v2 = % > SMA200, paparan sahaja.

## Sumber
Moskowitz & Grinblatt (1999) Do Industries Explain Momentum?; Arnott, Clements, Kalesnik & Linnainmaa, Factor Momentum; Weinstein (1988) Secrets for Profiting in Bull and Bear Markets; IBD/O'Neil 197 kumpulan industri; Bulkowski Industry RS; de Kempenaer Relative Rotation Graphs; George & Hwang (2004) 52-Week High; Hong, Jordan & Liu (2015) industri 52 minggu; Novy-Marx (2012); Daniel & Moskowitz (2016) Momentum Crashes; Hou (2007) lead-lag industri; Moskowitz, Ooi & Pedersen (2012) Time Series Momentum; Molchanov & Stangl (2023) The Myth of Business Cycle Sector Rotation; kajian pembalikan dalam industri (NUS; CXO Advisory).

## Pengesahan bebas 2005–2026 (18 Okt 2026, `kajian/industri/RINGKASAN.md`)
Data berasingan: 3,855 saham AS (yfinance, Jan 2005–16 Okt 2026, tutup ≥ USD5, nilai dagangan 50 hari ≥ USD1 juta; industri Moomoo), sampel setiap 5 hari, pulangan buka esok → tutup hari ke-21 lawan purata semua saham. Varian W1 = definisi gred v2 (Weinstein + median 1 bulan, indeks sama rata). Gred v2 TIDAK diubah.
- Semua saham: A +0.22, B +0.05, C +0.05, D −0.03, E −0.17 (% lebihan 21 hari); A−E +0.40%, t 1.49, tersusun (monotonik 1.0), positif 67% tahun. Lebih baik daripada v1 (A−E +0.28%, t 1.10).
- Peringkat industri: A−E +0.46%, t 1.81, tersusun.
- Ikut saiz: saham kecil A−E +0.87% (t 2.95), saham besar +0.13% (t 0.43) — kesan terutamanya pada saham kecil (selaras Hou 2007).
- Set 431 (Shariah): A−E +0.15% (t 0.44), tidak tersusun pada 2005–2012 (−0.55%), positif 2020–kini (+0.76%). Untuk set 431, Weinstein sahaja (+0.56%, t 1.58) dan 12−1 bulan (+0.68%, t 1.79) lebih kuat daripada W1.
- Rejim: SPY > SMA200 → semua saham A−E +0.60% (t 2.34), set 431 +0.58% (t 1.63); SPY < SMA200 → terbalik (set 431 −1.26%, E terbaik). Selaras dengan nota "pasaran beruang hampir sifar" di atas, tetapi bagi set 431 kesannya negatif.
- Kekekalan: gred A kekal A selepas ~20 hari hanya 34% (12−1 bulan: 78%).
- Bacaan: v2 menyusun A→E dengan betul untuk pasaran luas dan kekal positif sejak 2020; untuk saham Shariah sederhana–besar kesannya kecil dan bergantung rejim. Cadangan pemantauan: nilai prestasi gred Industri berasingan bagi SPY > / < SMA200.
