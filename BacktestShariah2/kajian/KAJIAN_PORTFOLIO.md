# Kajian portfolio modal terhad 10 slot (19 Okt 2026)

Permintaan pengguna 19 Okt 2026: Papertrade C membeli setiap isyarat (~800 sehari, 1 unit). Dengan modal sebenar 10 slot
(10% ekuiti setiap satu), isyarat mana patut diambil apabila isyarat lebih banyak daripada slot kosong?
Skrip: `kajian/portfolio/kaji_portfolio.py` (`sedia`, `semak`, `sim`, `ringkas`, `tahan`). Hasil: `kajian/portfolio/keputusan.csv`,
`ketahanan.csv`, `tahunan.csv`. Kajian ini rekod sahaja; tiada peraturan papertrade diubah.

## Data dan kaedah
- Calon: 763,327 dagangan enjin v1.2 bagi 134 kaedah (set 431, `data_mentah`; dijana `kajian/lorong2/kaji_lorong2.py jana`,
  bilangan sama dengan kajian lorong 2). Lapan saham dengan peristiwa korporat tidak terlaras dibuang (ASST, FCEL, MTDR, OVV, PR,
  SM, VAL, XENE; LAPORAN_UTAMA §10), jadi alam ujian ialah 423 saham. Larian pertama yang belum membuang lapan saham ini
  meletakkan ASST, FCEL dan PR antara penyumbang untung teratas.
- Tempoh portfolio: masuk 2 Nov 2020 – 2 Okt 2026. Dagangan sejak Nov 2019 hanya digunakan sebagai sejarah skor kaedah
  walk-forward. H1 = Nov 2020 – Okt 2023, H2 = Nov 2023 – Okt 2026.
- Portfolio: 10 slot. Saiz posisi = min(tunai, ekuiti semalam × 10%). Satu posisi sahaja bagi setiap saham. Masuk pada buka
  hari selepas isyarat. Kos 0.1% setiap belah. Logik sama dengan `enjin.portfolio` v1.2; semakan (`semak`, 8 slot, M03/M27/M119)
  menunjukkan beza CAGR ≤ 0.5 mata.
- Cara keluar: L1 = peraturan kaedah (enjin). L2 = Chandelier tutup 4×ATR14, paras hanya naik, tanpa henti kaedah (lorong 2 semasa).
- Peraturan pemilihan: setiap pagi, isyarat disusun ikut skor tertinggi. Semua skor diambil pada tutup hari isyarat (tiada
  pandang hadapan), kecuali yang ditanda rujukan.
  - Konsensus: bilangan kaedah yang memberi isyarat bagi saham dan tarikh sama.
  - RS pasaran: `kajian/rs/rs_pasaran_431.csv.gz`, RS lawan seluruh pasaran AS.
  - RS disahkan dahulu: RS ≥ 80 dan disahkan diutamakan; syarat sah ikut `gred.py`, iaitu naik 12 bulan, Mansfield > 0 dan
    SPY > SMA200.
  - Industri v2: skor `gred_kumpulan.py` dibina semula daripada `kumpulan_harian.csv.gz`, cawangan `kajian-gred`.
  - Kaedah walk-forward: purata lebihan SPY dagangan kaedah itu yang sudah keluar dalam 12 bulan sebelum isyarat (≥ 10 dagangan).
  - Momentum 6 bulan.
  - ATR14% rendah atau tinggi.
  - Gabungan: purata pangkat persentil kaedah walk-forward, RS, Industri dan konsensus.
  - Kaedah statik (rujukan sahaja, ada pandang hadapan): purata lebihan kaedah atas seluruh tempoh.
- Rawak: susunan rawak, 30 benih. Persentil sesuatu peraturan = % benih rawak yang dikalahkannya bagi CAGR, H1 dan H2.
- Penanda aras dalam tempoh sama: SPY CAGR 16.9% (MDD −24.5%). Beli dan pegang sama rata 423 saham CAGR 26.3% (MDD −27.6%).

## Keputusan (10 slot, tanpa penapis rejim; persentil lawan rawak CAGR/H1/H2)
| Peraturan | L1 CAGR % | L1 MDD % | L1 persentil | L2 CAGR % | L2 MDD % | L2 persentil |
|---|---|---|---|---|---|---|
| Rawak (median 30 benih) | 23.8 | −30.9 | – | 24.5 | −30.5 | – |
| Konsensus kaedah | 25.0 | −32.0 | 53/13/80 | 21.2 | −31.4 | 33/37/33 |
| RS pasaran | 78.0 | −45.4 | 100/100/100 | 72.6 | −48.6 | 100/100/100 |
| RS disahkan dahulu | 75.9 | −50.3 | 100/100/100 | 78.3 | −46.5 | 100/100/100 |
| Industri v2 | 22.1 | −38.5 | 37/67/37 | 32.0 | −35.8 | 80/77/80 |
| Kaedah walk-forward 12 bulan | 31.5 | −37.1 | 87/3/97 | 23.3 | −27.5 | 43/73/33 |
| Momentum 6 bulan | 54.0 | −48.0 | 100/97/100 | 58.6 | −42.1 | 100/97/93 |
| Volatiliti rendah | 7.2 | −19.8 | 0/33/0 | 7.5 | −20.2 | 0/7/10 |
| Volatiliti tinggi | 74.3 | −56.8 | 100/93/100 | 78.0 | −58.3 | 100/97/100 |
| Gabungan | 25.2 | −33.3 | 53/80/40 | 26.7 | −27.9 | 63/83/40 |
| Kaedah statik (pandang hadapan, rujukan) | 33.1 | −31.5 | 87/93/63 | 40.1 | −39.9 | 93/70/93 |

- Isyarat yang dipilih secara rawak (23.8–24.5%) tidak mengatasi beli dan pegang sama rata 423 saham (26.3%), dan MDD-nya lebih
  dalam. Pada peringkat portfolio 10 slot, isyarat kaedah sendiri tidak menambah nilai. Nilai hanya datang daripada cara memilih.
- Memilih kaedah "terbaik" bukan sumber nilai utama. Kaedah statik, yang melihat keputusan masa depan, hanya mencapai 33–40%.
  Kaedah walk-forward tidak stabil: persentil H1 3 lawan H2 97 (L1).
- Penapis rejim SPY > SMA200 (larian berasingan) menurunkan CAGR rawak (L2 24.5% → 14.6%; L1 23.8% → 15.5%) tanpa mengurangkan
  MDD (L2 −33.7% lawan −30.5%), jadi ia tidak dicadangkan.
- Bilangan slot (L2): dengan 5 slot hasil sangat bergantung nasib (rawak p5–p95 6.9–52.7%). Dengan 20 slot hasil lebih stabil
  (rawak 25.8%, MDD −28.3%; RS 57.1%, MDD −42.5%).

## Ketahanan: bias set 431
Set 431 ialah senarai Shariah hari ini. Saham yang jatuh teruk atau dinyahsenarai sejak 2019 tiada dalam set, dan pemenang
besarnya sudah diketahui. Kajian RS seluruh pasaran (`kajian/rs/RINGKASAN.md` §11) menunjukkan lebihan RS 95–99 dalam set 431
= +2.05% setiap 21 hari (t 4.65), lawan +0.39% (t 1.15) bagi saham lain, iaitu kira-kira 5 kali ganda. Ujian `tahan` membuang
20 atau 40 saham dengan pulangan tertinggi 2020–2026 (dipilih dengan pandang hadapan: AEHR, CLS, SNDK, WFRD, MOD, BE, MU, DELL,
BTU, SMCI, NVDA …), kemudian mengulang simulasi (rawak 20 benih).

| Peraturan (CAGR %; persentil CAGR/H1/H2) | L2 buang 0 | L2 buang 20 | L2 buang 40 | L1 buang 0 | L1 buang 20 | L1 buang 40 |
|---|---|---|---|---|---|---|
| Beli dan pegang sama rata | 26.3 | 19.4 | 16.4 | 26.3 | 19.4 | 16.4 |
| Rawak (median) | 24.8 | 19.0 | 17.6 | 24.9 | 15.3 | 16.3 |
| **RS pasaran** | 72.6 (100/100/100) | 36.8 (100/95/95) | **30.7 (100/100/100)** | 78.0 (100/100/100) | 25.3 (90/95/80) | 17.1 (50/45/60) |
| Momentum 6 bulan | 58.6 (100/95/90) | 29.6 (90/95/85) | 16.8 (45/35/60) | 54.0 (100/100/100) | 23.9 (90/100/40) | 10.0 (15/10/20) |
| Volatiliti tinggi | 78.0 (100/95/100) | 45.8 (100/80/100) | 35.1 (100/60/100) | 74.3 (100/95/100) | 23.7 (90/30/95) | 36.6 (100/95/100) |
| Industri v2 | 32.0 (75/75/80) | 25.6 (85/90/60) | 21.7 (85/95/60) | 22.1 (35/70/35) | 22.6 (85/50/85) | 27.5 (100/95/90) |
| Kaedah walk-forward | 23.3 (40/70/30) | 18.9 (50/90/30) | 17.7 (50/80/35) | 31.5 (85/5/95) | 19.6 (65/95/30) | 17.6 (50/5/95) |
| Gabungan | 26.7 (60/80/35) | 31.1 (95/95/85) | 28.8 (100/100/95) | 25.2 (50/85/40) | 19.1 (65/65/75) | 19.4 (65/75/60) |

MDD (buang 40): RS L2 −33.1%, rawak L2 −30.6%, volatiliti tinggi L2 −51.9%, Gabungan L2 −31.2%. Tumpuan untung: 5 saham
teratas menyumbang 37–89% untung bersih dalam kebanyakan larian (RS L2 66% tanpa buang; volatiliti tinggi 89%).

- **RS dengan keluar L1**: kelebihan hilang sepenuhnya selepas 40 pemenang dibuang (17.1% lawan rawak 16.3%, persentil 50).
  Hasil ini bergantung pada pemenang yang sudah diketahui.
- **RS dengan keluar L2 (Chandelier)**: kekal 30.7% selepas 40 pemenang dibuang, lawan rawak 17.6% dan sama rata 16.4%, dengan
  persentil 100 dalam H1 dan H2, dan MDD hampir sama dengan rawak (−33% lawan −31%). Ini satu-satunya gabungan yang kekal jelas
  di atas rawak dalam semua ujian. Ia sepadan dengan dua kajian lain: kajian RS seluruh pasaran (kelebihan RS 90+ wujud tetapi
  kecil) dan kajian lorong 2 (Chandelier membiarkan trend berkembang).
- Momentum 6 bulan runtuh selepas 40 pemenang dibuang (bias).
- Volatiliti tinggi kekal tinggi tetapi MDD −52% hingga −58%. Ia paling terdedah kepada bias, kerana saham volatil yang gagal
  tiada dalam set. Tidak sesuai untuk modal sebenar.
- Industri v2 dan Gabungan sederhana dan tidak konsisten antara ujian.

## Cadangan (rekod sahaja; perlu bukti hadapan sebelum modal sebenar)
**10 slot RS + Chandelier:**
- Setiap pagi, daripada senarai beli (isyarat 100% semua kaedah), isi slot kosong dengan saham yang RS pasarannya tertinggi.
- Satu posisi bagi setiap saham, saiz 10% ekuiti.
- Keluar ikut lorong 2 (Chandelier tutup 4×ATR14, paras naik, tanpa henti kaedah). Tiada penapis rejim.
- Dalam set penuh: ~55 belian setahun (~1 seminggu), pegang purata 47 hari, kadar menang 48%, purata +14.8% setiap dagangan.
- Jangkaan realistik jauh di bawah CAGR backtest 72.6%. Selepas 40 pemenang dibuang, CAGR 30.7% dan MDD −33%, dan bias
  kemandirian baki set masih ada. Bersedia untuk MDD −35% hingga −50%.
- Langkah seterusnya ialah jejak hadapan dalam papertrade, yang mengimbas seluruh pasaran AS secara langsung dan oleh itu
  tiada bias kemandirian. Rekod dua portfolio maya 10 slot: RS + Chandelier, dan rawak sebagai kawalan. Nilai selepas
  sekurang-kurangnya 6–12 bulan.

## Batasan
- Bias kemandirian set 431: ujian buang pemenang hanya mengurangkannya, tidak menghapuskannya.
- Kaedah sendiri dibina dan ditapis dengan melihat data 2019–2026 (dalam sampel).
- Peta industri ialah peta semasa (`papertrade/peta_industri.csv`), bukan peta sejarah. RS dan industri tiada data bagi ~4% calon
  (diisi neutral 50).
- Tiada had kecairan atau slippage selain kos 0.1%. Masuk pada harga buka.
- Satu tempoh sahaja (Nov 2020 – Okt 2026), yang termasuk ledakan semikonduktor/AI 2023–2026. Persentil rawak bersifat kasar
  (30 benih; 10 bagi 5/20 slot; 20 dalam ujian ketahanan).
