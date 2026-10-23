# Ujian kawalan status trend (trend4): sektor/industri, earnings, rejim pasaran, kos, kemandirian dan posisi hadapan

Nota ini menguji semula empat dakwaan laporan [Penentuan status trend saham](../../reports/Penentuan%20status%20trend%20saham.md) (dan nota [ujian_panel.md](../Penentuan%20status%20trend%20saham/ujian_panel.md), [ujian_dagangan.md](../Penentuan%20status%20trend%20saham/ujian_dagangan.md)) dengan kawalan yang sebelum ini tiada. Semua ujian dipradaftar pada 23 Okt 2026 sebelum mana-mana skrip trend4 dijalankan.

Singkatan: **T4** = `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4` (scratchpad sesi, tidak kekal; repo tidak diubah selain nota ini). **j8** = P(rendah intrahari jatuh > 8% di bawah buka t+1 dalam 10 sesi). **f_h** = pulangan h sesi dari buka t+1. **mata** = mata peratusan. Angka dalam kurungan = t Newey-West (lag = ufuk; 10 bagi j8) dan, selepas koma bertitik, t lag 60. **BearL/BearLama** = D10+H2 Bear dengan umur > 60 sesi; **BullL** = Bull umur > 60. Model: A = Bull, Bear; B = A + log ATR14% + log RV21; C = A + FE sektor + earnings (tanpa vol); D = B + FE sektor + earnings; E = D + BullL + BearL; F = E + r252 + jarak dari tinggi 52 minggu + log harga + log nilai dagangan + beta 126 hari; G = F + keadaan industri (IndBull, IndBear, IndBearL).

## S0. Reka bentuk, data dan lokasi skrip: bagaimana ujian dijalankan?

### Takeaway
Semua langkah berat larian terdahulu sudah siap sebelum bekas dimulakan semula; tiada ujian dijalankan semula. Larian ini hanya menambah pengiraan ringan (`akhir4.py`), membina semula skrip daftar Holm/BH (`daftar4.py`, padanan tepat dengan fail asal) dan menulis nota.

### Cited Findings
- Pradaftar (hipotesis H1–H5, kriteria, model A–G, keluarga Holm) ditulis sebelum skrip dijalankan; tiga pindaan bertarikh di hujung fail (penguraian model F selepas IS; semakan alam harga ≥ USD10/USD5 selepas OOS; sambung semula). Semua bertanda EKSPLORATORI, kriteria tidak diubah — [T4/prapendaftaran.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/prapendaftaran.md)
- Panel: 431 saham Shariah S1–S4 (trend2/panel2.pkl), syarat ≥ 252 bar. IS: 267,319 cerapan, 394 saham, 725 tarikh (2020-01-02..2022-11-15). OOS: 384,821 cerapan, 426 saham, 941 tarikh (2023-01-03..2026-10-02) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Sektor (FE sektor × tarikh): Technology 29%, Healthcare 14.5%, Industrials 14%, Energy 13–14%, Basic Materials 11%, Consumer Cyclical 9–10%, Communication 4%, Consumer Defensive 2.4%, "Lain" (Financial + Real Estate + Utilities) 1.5–2.1%; 89 (IS) / 92 (OOS) industri plate Moomoo; keadaan industri tersedia bagi 100% cerapan — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log); sumber peta [peta_industri.csv](../../BacktestShariah2/papertrade/peta_industri.csv), indeks [industri_harian.csv.gz](../../BacktestShariah2/kajian/industri/industri_harian.csv.gz)
- Earnings: 20,500 hari reaksi daripada [tarikh_pendapatan.csv](../../BacktestShariah2/data/pemangkin/tarikh_pendapatan.csv); liputan "diketahui" 97.2% (IS) dan 97.5% (OOS); 17.6% / 17.2% cerapan ada hari reaksi dalam 10 sesi hadapan — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log)
- Rejim: SPY D10+H2 — IS 333 tarikh Bull / 322 Neutral / 70 Bear; OOS 612 / 323 / 2. Ambang tertil RV21 SPY (dari IS sahaja, dipakai juga dalam OOS): 14.0% dan 21.8% setahun. Tetingkap krisis: 19 Feb–30 Jun 2020 dan seluruh 2022 — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log); [T4/uji_panel4.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/uji_panel4.py)
- Statistik: regresi keratan rentas setiap tarikh (Fama-MacBeth), FE sektor = nyahmin dalam sel sektor × tarikh, t Newey-West atas siri pekali harian; semakan regresi gabungan dengan SE kelompok dua hala (bulan, saham) — [T4/enjin4.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/enjin4.py)
- Dagangan: 19 kaedah enjin v1.2 (trend3/dag.pkl), 54,350 dagangan IS dan 71,420 OOS, berwajaran 1/n setiap kaedah, SE kelompok bulan; kos dinilai semula pada 10/20/30/50 bps pergi-balik; "adj" = beza log dilaras masa (modal yang dibebaskan dikreditkan pada kadar log harian purata asas) — [T4/keluar4.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/keluar4.py); [T4/keluar4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/keluar4.log)
- Posisi hadapan: Papertrade C 4,950 baris → 4,765 sah → 4,708 dipadan; Lejar 7,179 (semua terbuka; tiada `lejar/tutup/`); Moomoo 208 → 200 → 196; uji_kertas 62 → 61. Jumlah 12,144 posisi = 3,583 unik saham + tarikh beli (1–22 Okt 2026). Harga: stor dilaras + `terkini.csv` — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log); [T4/nyata4.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/nyata4.py)
- Ujian berganda: 770 ujian berdaftar (BH atas semua), 486 kontras (BH khusus kontras, tanpa pekali kawalan ATR%/earnings), 54 ujian utama (Holm atas 54, dan Holm dalam dua kumpulan: dakwaan "kehadiran kesan" H2a+H3* = 12 ujian; dakwaan "ketiadaan kesan" H1+H2b+H5 = 42 ujian). `daftar4.py` membina semula ketiga-tiga fail dengan beza maksimum < 1e-14 — [T4/daftar4.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar4.py)

| Langkah | Skrip (T4/) | Output (T4/) | Status |
|---|---|---|---|
| Pradaftar | — | prapendaftaran.md | siap + 3 pindaan bertarikh |
| Panel + kawalan | sedia4.py | panel4.pkl (295 MB) | siap |
| Ujian panel H1–H3 | uji_panel4.py, enjin4.py | panel4_IS/OOS.pkl, daftar_panel_IS/OOS.csv | siap |
| Keluar + kos H5 | keluar4.py | keluar4.pkl, dag_bl.pkl, daftar_keluar.csv, keluar4.log | siap |
| Portfolio 8 slot | porto4.py (`kod/enjin.py`) | porto4.pkl, porto4.log | siap |
| Posisi hadapan | nyata4.py | nyata4.pkl, nyata4_posisi.pkl | siap |
| Semakan eksploratori | tambahan4.py | tambahan4.pkl, daftar_tambahan.csv | siap |
| Ringkasan panel | lapor4.py | lapor4.log | siap |
| Daftar Holm/BH | daftar4.py (baharu; ganti sel inline asal) | daftar_ujian.csv, daftar_kontras_bh.csv, daftar_utama_holm.csv | disahkan sama |
| Pengiraan akhir | akhir4.py (baharu) | akhir4.log | siap |

Jalankan semula (satu demi satu, < 4 GB): `python3 sedia4.py; python3 uji_panel4.py IS; python3 uji_panel4.py OOS; python3 keluar4.py; python3 porto4.py; python3 nyata4.py; python3 tambahan4.py; python3 daftar4.py --tulis; python3 akhir4.py; python3 lapor4.py IS OOS`.

### Inferences
- "OOS" bagi kontras mentah dan kawalan ATR% sudah dilihat dalam trend2/trend3; yang benar-benar baharu ialah kawalan (sektor, earnings, rejim, kawalan tambahan, kos) dan posisi hadapan Okt 2026. Bukti OOS di sini lebih lemah daripada data dara.
- Kriteria "IS DAN OOS" ialah ujian kesatuan-persilangan; ia sudah konservatif tanpa pelarasan, tetapi p Holm tetap dilapor.

### Gaps
- Sel asal yang membina daftar Holm/BH tidak disimpan sebagai skrip; `daftar4.py` ialah binaan semula (hasil sama).
- Kawalan earnings menganggap hari reaksi = d0 dan d0+1 jika masa pengumuman tidak diberi (konservatif, menambah hingar).

## S1. Dakwaan 1: adakah status meramal pulangan lebihan 3–30 hari selepas kawalan sektor, earnings dan rejim? (H1)

### Takeaway
Dakwaan 1 **bertahan** mengikut kriteria pradaftar: tiada takrif (D10+H2 dan 5 wakil keluarga lain) bererti dengan tanda sama dalam IS dan OOS. Tetapi kawalan baharu mendedahkan corak yang dahulu tersembunyi: dalam OOS 2023–2026 terdapat condong momentum kecil (+1.5 mata / 21 sesi, t 2.2) yang bertanda terbalik dalam IS dan terbalik kuat semasa SPY Bear atau turun naik tinggi.

### Cited Findings
Model D (vol + FE sektor + earnings), kontras Bull − Bear, mata — [T4/daftar_utama_holm.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_utama_holm.csv); [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

| Takrif, hasil | IS | OOS | p Holm (54) |
|---|---|---|---|
| D10+H2 f5 | −0.57 (−1.7) | +0.34 (+2.1) | 1.00 |
| D10+H2 f10 | −0.68 (−1.3) | +0.70 (+2.2) | 1.00 |
| D10+H2 f21 | −1.19 (−1.3) | +1.54 (+2.2; +1.9) | 1.00 |
| Weinstein W4 f21 | −0.02 (−0.0) | +1.32 (+2.1) | 1.00 |
| MAD 21/200 f21 | +0.23 (+0.5) | +0.99 (+1.9) | 1.00 |
| Supertrend f21 | −0.14 (−0.5) | +0.19 (+0.8) | 1.00 |
| ADX20 f21 | −0.21 (−0.5) | +0.78 (+2.4) | 0.80 |
| TSMOM K3 f21 | −0.20 (−0.4) | +1.11 (+2.4) | 0.80 |

- Tangga model bagi D10+H2 f21 (IS / OOS): A −0.80 (−0.6) / +0.68 (+0.9); B −0.10 (−0.1) / +1.33 (+1.9); C −1.54 (−1.5) / +0.98 (+1.3); D −1.19 (−1.3) / +1.54 (+2.2); F −1.19 (−1.4) / +1.10 (+3.2); G −1.13 (−1.3) / +0.97 (+3.0); sampel bersih earnings D −0.75 (−0.8) / +1.52 (+2.3) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Relatif industri: f21 dinyahmin dalam sel industri × tarikh (model B) +0.08 (+0.2) IS, +0.91 (+2.8) OOS; pulangan lebihan atas indeks industri (model D) −1.33 (−1.5) IS, +0.79 (+2.0) OOS — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Rejim (model D f21, IS / OOS): SPY Bull −1.63 (−1.0) / +1.34 (+1.5); SPY Neutral −0.24 (−0.2) / +1.96 (+2.4); **SPY Bear −3.43 (−5.2; −6.4)** / tiada data (2 tarikh); vol rendah −0.93 (−0.6) / **+2.16 (+3.1)**; vol sederhana −1.43 (−1.0) / +0.59 (+0.5); **vol tinggi** −1.21 (−1.0) / **−3.08 (−1.9; −3.2)** — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Mengikut tahun (model D f21): 2020 −2.89 (−1.2), 2021 −0.26, 2022 −0.38, 2023 +0.80 (+1.3), 2024 +1.62 (+2.2), 2025 +1.12 (+1.3), 2026 +3.15 (+1.0) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- BH atas 486 kontras: OOS ADX dan K3 f21 lulus q = 0.05 (p_BH 0.041), tetapi IS kedua-duanya bertanda negatif — [T4/daftar_kontras_bh.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_kontras_bh.csv)
- Kehancuran momentum berlaku dalam keadaan "panik" — selepas kejatuhan pasaran, ketika turun naik pasaran tinggi dan serentak dengan lantunan — [Daniel & Moskowitz 2016, JFE (EconPapers)](https://econpapers.repec.org/RePEc:eee:jfinec:v:122:y:2016:i:2:p:221-247)

### Inferences
- Tanda kesan bergantung pada rejim: positif (trend berterusan) dalam pasaran tenang/naik 2023–2026, negatif (pembalikan) dalam SPY Bear dan turun naik tinggi. Ini selari dengan corak kehancuran momentum Daniel & Moskowitz, dan menerangkan mengapa purata IS (berat dengan 2020 dan 2022) negatif manakala OOS (65% tarikh SPY Bull) positif.
- Kawalan vol menguatkan, bukan melemahkan, condong OOS (A +0.68 → D +1.54): saham Bear lebih meruap, jadi tanpa kawalan, premium turun naik menyorok beza arah.
- Saiz kesan OOS (≈ 1.5 mata sebulan) kecil berbanding sebaran pulangan saham individu dan tidak stabil merentas rejim; ia tidak mewajarkan label "Bullish = beli/pegang" pada papan. Dakwaan "tidak meramal pulangan" patut diperhalus kepada "tiada ramalan yang stabil merentas rejim".

### Gaps
- OOS hampir tiada SPY Bear (2 tarikh), jadi pembalikan dalam pasaran bear hanya dilihat dalam IS.
- Kesan f21 bagi model F/G (t 3.0–3.2 OOS) mempunyai konfigurasi kawalan yang dipilih untuk risiko, bukan untuk pulangan; tidak diuji sebagai hipotesis.

## S2. Dakwaan 2: adakah pemisahan risiko D10 tahan FE sektor + earnings, dan hilang selepas kawalan ATR%? (H2a, H2b)

### Takeaway
Kedua-dua bahagian **bertahan**: pemisahan mentah Bull − Bear bagi j8 tahan FE sektor + earnings (IS −4.1, OOS −3.7 mata) dan hilang selepas ATR%/RV21 dikawal (IS +2.0, OOS +0.9, t < 2). Tiga perhalusan baharu: pemisahan mentah hilang dalam SPY Bear/vol tinggi dan pada 2025–2026; earnings dalam tetingkap menaikkan j8 2–3 kali lebih banyak daripada label; dan selepas jarak dari tinggi 52 minggu dikawal, label Bull malah menandakan risiko **lebih tinggi**.

### Cited Findings
Tangga model, D10+H2, y = j8, mata — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log); [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log)

| Model | Bull − Bear IS | Bull − Bear OOS | Nota |
|---|---|---|---|
| A (mentah) | −6.57 (−3.0; −2.4) | −4.08 (−3.1; −2.3) | |
| C (+ FE sektor + earnings) — **H2a** | −4.05 (−2.6; −2.1) | −3.74 (−3.0; −2.3) | susut 38% (IS), 8% (OOS) daripada A |
| B (+ ATR%, RV21) | −0.27 (−0.2) | +0.90 (+0.8) | log ATR%: +29.3 (15.9) / +30.5 (23.2) |
| D (B + FE sektor + earnings) — **H2b** | +1.99 (+1.5; +1.7) | +0.89 (+0.8; +0.7) | earnings: +6.5 (7.5) / +13.9 (17.4) |
| F (+ r252, jarak52, harga, cair, beta) | +2.95 (+2.6) | +2.39 (+3.0) | Bull lebih berisiko |
| E + jarak52 sahaja | +4.37 (+3.8) | +3.37 (+3.9) | pemacu tanda terbalik |
| Gabungan 2 hala (bulan, saham), F | +3.41 (+2.3) | +2.19 (+2.3) | semakan SE |

- p Holm atas 54: H2a IS 0.54, OOS 0.12; Holm dalam kumpulan "kehadiran" (12): IS 0.086, OOS 0.025 — [T4/daftar_utama_holm.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_utama_holm.csv)
- Sampel bersih earnings (tiada hari reaksi dalam 10 sesi hadapan atau 5 sesi lalu): C −3.45 (−2.2) / −4.21 (−3.3); D +2.76 (+2.2) / +0.36 (+0.3) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Kadar j8 purata: IS 30.8% (dengan earnings dalam 10 sesi 34.3%, tanpa 30.0%); OOS 22.8% (33.2% lawan 20.7%) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

Rejim dan tahun, Bull − Bear j8 — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

| Sampel | C IS | C OOS | D IS | D OOS |
|---|---|---|---|---|
| SPY Bull | −3.21 (−1.3) | −3.52 (−2.2) | +2.67 (+1.5) | +1.06 (+0.8) |
| SPY Neutral | −6.20 (−2.6) | −4.20 (−2.8) | +0.47 (+0.2) | +0.53 (+0.4) |
| SPY Bear | +1.83 (+0.8) | — | **+5.77 (+2.5; +4.6)** | — |
| Vol SPY rendah | −4.06 (−1.3) | −4.62 (−3.2) | +2.66 (+1.1) | +0.16 (+0.1) |
| Vol SPY sederhana | −3.59 (−1.6) | −2.50 (−1.1) | +0.70 (+0.4) | +1.61 (+0.9) |
| Vol SPY tinggi | −4.50 (−1.9) | +4.03 (+0.9; +2.3) | +2.65 (+1.2) | **+10.10 (+2.5; +6.2)** |
| Tanpa krisis | −1.69 (−0.8) | −3.74 (−3.0) | +3.00 (+1.8) | +0.89 (+0.8) |

- Model C mengikut tahun: 2020 −4.86 (−1.6), 2021 −2.11 (−0.7), 2022 −5.37 (−2.9), 2023 −4.65 (−3.8), 2024 −8.16 (−4.8), **2025 −1.34 (−0.6), 2026 +0.41 (+0.1)** — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Takrif lain, model D j8 (IS / OOS): ADX +4.19 (+6.4) / +3.22 (+5.1); K3 TSMOM +6.72 (+7.1) / +4.23 (+5.2); Supertrend +2.55 (+4.6) / +2.44 (+4.9); W4 +0.88 / +0.28; MAD +0.52 / −0.16 — label pantas "Bull" = risiko neutral-vol lebih tinggi dalam kedua-dua tempoh — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

### Inferences
- Sektor dan earnings bukan punca pemisahan mentah: dalam OOS kedua-duanya hanya menyerap 8% beza. Pemacunya tetap turun naik semasa.
- Dalam pasaran tertekan (SPY Bear 2020/2022, vol tinggi OOS), saham Bull mempunyai risiko jatuh neutral-vol yang jelas **lebih tinggi** daripada Bear (+5.8 hingga +10.1 mata). Label "Bullish" tidak boleh dibaca sebagai "lebih selamat" dalam rejim itu.
- Pemisahan mentah sendiri lemah pada 2025–2026; jika diteruskan, warna risiko berasaskan label Bear (tanpa umur) tidak membawa maklumat mentah terkini.
- Selepas jarak dari tinggi 52 minggu dan ATR% diketahui, label D10 tidak menambah maklumat "selamat". Paparan ATR% (dan tarikh earnings) di sebelah pill lebih berinformasi daripada warna label.
- Kesan earnings dalam tetingkap (+6.5 hingga +13.9 mata) ialah 2–3 kali ganda kesan BearLama (S3); lencana "earnings ≤ 10 sesi" ialah amaran risiko yang lebih kuat daripada mana-mana status trend.

### Gaps
- Tiada data OOS dalam SPY Bear untuk mereplikasi pembalikan dalam pasaran bear.
- Jarak52 dan r252 berkorelasi dengan label secara pembinaan; pekali bersyarat F/G tidak boleh ditafsir sebagai "kesan sebab-akibat" label.

## S3. Dakwaan 3: adakah umur keadaan (BearLama, BullLama) bermaklumat selepas kawalan tambahan? (H3a–H3e)

### Takeaway
Dakwaan 3 **dilemahkan**. BearLama kekal positif dan bererti dalam **semua** spesifikasi OOS (t 2.2–3.8), tetapi dalam IS ia gagal setiap kriteria pradaftar sebaik kawalan tambahan dimasukkan (t 0.2–1.8): sebahagian besarnya ialah "jauh di bawah tinggi 52 minggu", isyarat IS tertumpu pada 2022 dan terbalik pada 2020. BullLama gagal H3b (diserap pulangan 12 bulan). Kesimpulan lama "satu-satunya maklumat bebas yang tahan dalam kedua-dua tempoh" tidak lagi tepat.

### Cited Findings
Hipotesis utama, y = j8, mata — [T4/daftar_utama_holm.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_utama_holm.csv)

| Hipotesis | Spesifikasi | IS | OOS | Keputusan |
|---|---|---|---|---|
| (rujukan) E | vol + sektor + earnings | BearL +4.80 (+2.4; +2.6) | +5.39 (+3.3; +2.9) | lulus kedua-dua |
| H3a | F, BearL | +3.56 (+1.8; +1.8) | +4.74 (+3.0; +2.6) | **gagal (IS)** |
| H3b | F, BullL | +2.50 (+2.0; +1.5) | +1.42 (+1.5; +1.5) | **gagal (OOS)** |
| H3c | F, bersih earnings, BearL | +1.87 (+0.9; +1.0) | +4.88 (+2.7; +2.6) | **gagal (IS)** |
| H3d | IS tanpa krisis / OOS SPY Bull | +1.03 (+0.2; +0.3), 55 tarikh | +4.15 (+2.2; +1.9) | **gagal (IS)** |
| H3e | G (+ keadaan industri), BearL | +3.38 (+1.7; +1.7) | +4.90 (+3.2; +2.8) | **gagal (IS)** |

- Holm: tiada p Holm (54) < 0.05 (terkecil OOS H3e 0.087, OOS H3 BearL 0.13); Holm kumpulan "kehadiran": OOS H3 BearL 0.025, OOS H3e 0.019, OOS H3c 0.067 — [T4/daftar_utama_holm.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_utama_holm.csv)
- BullL model E: IS +3.59 (+3.1; +2.4), OOS +2.35 (+2.6; +2.6) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

Penguraian (EKSPLORATORI, pindaan selepas IS): model E + satu kawalan — [T4/daftar_kontras_bh.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_kontras_bh.csv)

| Kawalan ditambah | BearL IS | BearL OOS | BullL IS | BullL OOS |
|---|---|---|---|---|
| r252 | +4.43 (+2.2) | +5.94 (+3.6) | +2.57 (+2.1) | +1.81 (+2.0) |
| jarak52 | **+3.34 (+1.7)** | +4.31 (+2.6) | +3.56 (+3.0) | +2.39 (+2.7) |
| log harga | +4.77 (+2.3) | +5.22 (+3.2) | +3.55 (+3.1) | +2.21 (+2.4) |
| log nilai dagangan | +4.60 (+2.3) | +5.29 (+3.2) | +3.46 (+3.1) | +2.24 (+2.4) |
| beta | +5.21 (+2.6) | +5.97 (+3.8) | +3.70 (+3.2) | +2.48 (+2.8) |

- Profil median BearL lawan Bear ≤ 60 (IS): ATR% 5.7 lawan 4.4; r252 −57% lawan −29%; jarak52 −62% lawan −42%; harga USD19.2 lawan 30.2; beta 1.46 lawan 1.22. OOS: ATR% 4.5 lawan 3.5; r252 −48% lawan −23%; jarak52 −54% lawan −37%; harga USD25.3 lawan 39.6. BearL di bawah USD10: 28% (IS), 17% (OOS); di bawah USD5: 13%, 9% — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Kadar j8 mentah (purata harian): BearL 53.2% lawan Bear 34.8% (IS); 36.0% lawan 26.3% (OOS) — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log)
- Taburan masa BearL: IS 2020 = 870 cerapan, 2021 = 65, 2022 = 2,131 (410 tarikh berisi BearL); OOS 2023 = 709, 2024 = 801, 2025 = 1,304, 2026 = 1,022 (865 tarikh) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- BearL model F mengikut tahun: **2020 −3.38 (−1.4; −2.6)**, 2022 +5.36 (+2.3; +2.6), 2023 +1.37 (+0.5), 2024 +4.59 (+1.3), 2025 +3.48 (+1.5), 2026 +10.19 (+3.1; +4.6). Mengikut rejim: SPY Neutral IS +4.74 (+2.1), OOS +6.00 (+2.4); SPY Bear IS +0.19 (+0.1); vol tinggi IS +0.66 (+0.4), OOS +12.44 (+6.8) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Semakan EKSPLORATORI alam harga (Lejar hanya mengimbas tutup ≥ USD10): ≥ USD10, model F BearL IS +5.35 (+2.4; +2.3), OOS +5.27 (+3.4; +3.1) — lulus kedua-dua tempoh; ≥ USD5: IS +4.37 (+1.9), OOS +5.51 (+3.7); BullL F ≥ USD10: IS +2.20 (+1.8), OOS +1.95 (+2.1) — [T4/daftar_tambahan.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_tambahan.csv)
- Regresi gabungan (SE dua hala bulan × saham), F: BearL IS +1.59 (+0.8), OOS +3.78 (+2.4); BullL IS +2.53 (+1.8), OOS +2.28 (+2.1) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)
- Relatif industri (j8 dinyahmin dalam industri × tarikh, model E): BearL IS +5.79 (+3.1), OOS +4.51 (+2.9) — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

### Inferences
- BearLama sebahagiannya ialah proksi "jauh di bawah tinggi 52 minggu" (jarak52 menurunkan t IS daripada 2.4 kepada 1.7) dan sebahagian lagi ialah saham murah < USD10 dalam IS. Dalam alam yang benar-benar diimbas Lejar (≥ USD10), kesan +5.3 mata tahan kedua-dua tempoh, jadi amaran BearLama masih relevan untuk papan ini, tetapi sebagai bukti eksploratori sederhana, bukan dapatan pradaftar yang lulus.
- Pembalikan 2020 (BearL −3.4 mata) ialah corak lantunan selepas panik; amaran BearLama berkemungkinan salah arah tepat selepas kejatuhan pasaran.
- BullLama hampir hilang selepas r252: ia terutamanya menandakan "sudah naik banyak dalam 12 bulan", bukan umur sebagai maklumat bebas. Sub-label "Bullish lama" boleh kekal deskriptif, tanpa warna amaran.
- Saiz kesan BearL (+4.7 mata OOS atas asas ≈ 26%) sederhana; earnings (+13.9 mata OOS) dan ATR% (+29 mata setiap unit log) jauh lebih besar.

### Gaps
- IS hanya mempunyai 55 tarikh BearL di luar tetingkap krisis; H3d IS hampir tiada kuasa.
- Pindaan ≥ USD10 dibuat selepas melihat IS dan OOS; perlu disahkan secara hadapan.

## S4. Dakwaan 4: adakah peraturan keluar berasaskan status mengatasi keluar kaedah atau Chandelier selepas kos? (H5)

### Takeaway
Dakwaan 4 **bertahan**. Tiada satu pun daripada 6 peraturan (K/L2 × hilang Bull, masuk Bear, BearLama) mempunyai beza log positif bererti dalam IS dan OOS pada 10–50 bps. Calon terbaik (L2 + hilang Bull, dilaras masa) lulus dalam IS (t 2.45) tetapi tidak dalam OOS (t 0.45), dan dalam portfolio 8 slot ia menurunkan CAGR median separuh kedua 4.7 mata.

### Cited Findings
Setiap dagangan, berwajaran kaedah, IS / OOS; dlog dan adj dalam mata log setiap dagangan — [T4/keluar4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/keluar4.log); [T4/daftar_utama_holm.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_utama_holm.csv)

| Peraturan | Terkena % | dlog (t) | adj 10 bps | adj 30 bps | adj 50 bps |
|---|---|---|---|---|---|
| K + hilang Bull | 5.2 / 5.6 | −0.03 (−1.2) / −0.15 (−1.8) | −0.01 / −0.08 | −0.02 (−0.7) / −0.09 (−1.1) | −0.02 / −0.10 |
| K + masuk Bear | 2.2 / 1.8 | −0.06 (−1.7) / −0.02 (−2.0) | −0.05 / −0.00 | −0.05 (−1.6) / −0.01 (−0.6) | −0.05 / −0.01 |
| K + BearLama | 0.45 / 0.56 | −0.00 (−0.1) / −0.00 (−0.3) | 0.00 / 0.00 | −0.00 (−0.0) / +0.00 (+0.2) | −0.00 / 0.00 |
| L2 + hilang Bull | 39.8 / 38.4 | −0.09 (−0.6) / −0.44 (−1.9) | +0.33 (+2.8) / +0.13 (+0.6) | **+0.30 (+2.45)** / +0.09 (+0.45) | +0.26 (+2.1) / +0.06 (+0.3) |
| L2 + masuk Bear | 11.9 / 9.7 | −0.13 (−0.8) / −0.31 (−1.6) | +0.02 / −0.11 | +0.00 (+0.0) / −0.13 (−0.75) | −0.01 / −0.14 |
| L2 + BearLama | 0.75 / 0.77 | −0.06 (−1.6) / −0.09 (−0.9) | −0.05 / −0.06 | −0.05 (−1.3) / −0.06 (−0.7) | −0.05 / −0.06 |

- L2 + hilang Bull: membantu 54.8% / 59.0% posisi terkena; persentil ke-5 bertambah baik −20.0% → −18.7% (IS), −19.8% → −18.1% (OOS); purata log 2.20 → 2.11 (IS), 3.13 → 2.69 (OOS) — [T4/keluar4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/keluar4.log)
- Mengikut rejim SPY pada hari peristiwa (dlog posisi terkena): L2 + masuk Bear dalam SPY Bear IS **−3.83 (−3.2)**; K + masuk Bear dalam SPY Bear IS **−2.45 (−4.3)**; L2 + hilang Bull dalam SPY Bear IS +1.40 (+1.9), dalam SPY Neutral OOS **−4.09 (−3.3)**; L2 + BearLama dalam SPY Neutral OOS −30.8 (−2.0, n 157) — [T4/keluar4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/keluar4.log)
- Dagangan yang dimasuki ketika saham sudah BearLama: 0.82% (IS), 0.81% (OOS), terutamanya M92, M73, M111, M12, M140, M01 — [T4/keluar4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/keluar4.log)

Portfolio 8 slot (`kod/enjin.py` v1.2; h1 = Nov 2019–2022, h2 = 2023–), median 19 kaedah, % — [T4/porto4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/porto4.log)

| Kos | Varian | CAGR h1 | CAGR h2 | MDD h1 | MDD h2 |
|---|---|---|---|---|---|
| 20 bps | L2 | 19.9 | 33.9 | −32.0 | −32.9 |
| 20 bps | L2 + hilang Bull | 17.0 | 28.5 | −34.1 | −32.8 |
| 20 bps | L2 + BearLama | 19.9 | 35.3 | −32.6 | −32.9 |
| 20 bps | K / K + BearLama | 18.3 / 18.3 | 42.7 / 42.7 | −31.4 / −31.4 | −29.3 / −29.3 |
| 50 bps | L2 | 18.4 | 32.1 | −33.2 | −35.2 |
| 50 bps | L2 + hilang Bull | 15.9 | 25.5 | −34.8 | −33.9 |

- Beza berpasangan L2 + hilang Bull lawan L2: CAGR h2 median −4.65 mata (lebih baik bagi 7/19 kaedah) pada 20 bps, −5.12 (6/19) pada 50 bps; MDD h1 +1.3 mata (11/19), MDD h2 −1.9 (7/19). BearLama: beza median 0.00 (hanya 1–5 kaedah terkesan) — [T4/porto4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/porto4.log)

### Inferences
- Kos hampir tidak mengubah keputusan kerana peraturan keluar tidak menambah bilangan dagangan; kesan kos hanya melalui pelarasan masa (modal dibebaskan lebih awal). Kesimpulan lama tidak bergantung pada andaian kos.
- Menjual apabila status bertukar ke Bear ketika pasaran sendiri Bear ialah tindakan paling merugikan (menjual sebelum lantunan), selari dengan corak S1/S2.
- Peraturan BearLama terlalu jarang (< 1% dagangan) untuk mengubah portfolio; nilainya, jika ada, hanya sebagai maklumat, bukan isyarat jual.

### Gaps
- Hanya peraturan berasaskan D10 diuji semula dengan kos; 37 peraturan lain trend3 tidak dijalankan semula (semuanya negatif sebelum kos dan kos tidak menambah dagangan).
- Kos tergelincir harga semasa jualan buka esok dalam saham berisiko tinggi tidak dimodelkan berasingan.

## S5. Keadaan industri/sektor: adakah ia menambah maklumat melebihi keadaan saham?

### Takeaway
Untuk **risiko**, keadaan industri tidak menambah maklumat selepas keadaan saham dan turun naik dikawal. Untuk **pulangan**, keadaan industri menunjukkan corak yang sama seperti keadaan saham: positif dalam OOS, negatif dalam IS. Jadual mentah 3 × 3 menunjukkan "saham Bear dalam industri Bear" sebagai sel paling berisiko, tetapi kebanyakannya ialah turun naik.

### Cited Findings
- Model G, IndBull − IndBear (IS / OOS): j8 +1.02 (+0.7) / −1.53 (−1.7); IndBearL j8 +0.29 (+0.1) / −1.75 (−1.0); f5 −0.06 (−0.2) / +0.36 (+2.8); f10 −0.14 (−0.3) / +0.75 (+2.8); f21 −0.87 (−1.2) / **+1.42 (+3.1)**, p_BH OOS 0.019–0.037 — [T4/daftar_kontras_bh.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_kontras_bh.csv)
- Interaksi (model D + interaksi, FE sektor), j8, saham Bull − Bear bersyarat industri (IS / OOS): industri Bull +2.55 (+1.1) / +0.29 (+0.1); Neutral +1.04 (+0.8) / +0.78 (+0.8); **industri Bear +6.18 (+3.1) / +2.66 (+1.7)**; industri Bull − Bear bagi saham Neutral +0.31 (+0.2) / −1.20 (−1.2). Versi sektor: semua |t| ≤ 1.8 bagi j8; f21 sektor Bull − Bear bagi saham Neutral +3.67 (+2.0) IS lawan −0.87 (−0.9) OOS — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

Jadual mentah 3 × 3 (D10+H2 saham × industri): kadar j8 %, lebihan j8 atas purata tarikh (t), n — [T4/lapor4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/lapor4.log)

| Saham / industri | IS j8 | IS lebihan | OOS j8 | OOS lebihan |
|---|---|---|---|---|
| Bull / Bull | 29.8 | −0.5 (−0.3) | 22.5 | −0.3 (−0.3) |
| Bull / Bear | 34.1 | −0.3 (−0.1) | 20.4 | −2.4 (−2.2) |
| Neutral / Neutral | 31.6 | +0.8 (+1.1) | 22.3 | −0.5 (−1.4) |
| Bear / Bull | 27.2 | −2.2 (−1.0) | 27.5 | +4.3 (+1.9) |
| Bear / Neutral | 33.9 | +3.1 (+2.1) | 25.5 | +2.8 (+2.9) |
| Bear / Bear | 43.1 | **+10.6 (+5.0)** | 26.6 | +3.9 (+2.9) |

### Inferences
- Paparan keadaan industri di sebelah keadaan saham tidak dijangka membantu keputusan risiko; ia hanya mengulang maklumat turun naik.
- Keadaan industri untuk pulangan OOS (+1.4 mata / 21 sesi) ialah momentum industri yang bertukar tanda antara tempoh, sama seperti keadaan saham; tidak stabil untuk dijadikan isyarat.

### Gaps
- Indeks industri dibina daripada data yfinance seluruh pasaran AS yang juga berkemungkinan berbias kemandirian.
- Sel 3 × 3 tidak dikawal untuk turun naik; hanya untuk deskripsi.

## S6. Posisi hadapan sebenar (Papertrade C, Lejar Penuh, Moomoo, uji_kertas): adakah ia mengesahkan dapatan panel?

### Takeaway
Tidak boleh mengesahkan atau menolak. Data hadapan hanya meliputi 1–22 Okt 2026 (median 4–5 sesi dipegang), 21 posisi unik BearLama daripada **6 saham** pada 6 tarikh, dan kesan minimum boleh dikesan (16.7 mata) ialah 3.5 kali kesan panel (4.7 mata). Arah sementara: BearLama setakat ini **lebih baik** (bertentangan dengan panel), BullLama lebih lemah (selari dengan panel).

### Cited Findings
Unik saham + tarikh beli, semua sumber; status pada tutup sebelum hari beli — [T4/nyata4.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/nyata4.pkl) (dicetak dalam larian ini)

| Kumpulan | n | Tarikh | Saham | Pulangan kini | MAE | Jatuh > 8% setakat ini | Jatuh > 8% dalam 5 sesi (n) | ATR% median |
|---|---|---|---|---|---|---|---|---|
| Bear ≤ 60 | 363 | 12 | 152 | +1.87% | −3.51% | 8.8% | 9.1% (175) | 3.15 |
| Bear lama | 21 | 6 | 6 | +4.64% | −2.75% | 4.8% | 10.0% (10) | 3.28 |
| Bull ≤ 60 | 876 | 13 | 207 | −0.09% | −4.79% | 17.1% | 23.5% (473) | 2.98 |
| Bull lama | 169 | 12 | 31 | −1.34% | −4.79% | 17.2% | 20.2% (89) | 3.19 |
| Neutral | 2,149 | 14 | 649 | +0.91% | −4.27% | 15.0% | 17.1% (1,074) | 3.24 |

- Mengikut sumber, jatuh > 8% dalam 5 sesi: C — Bull ≤ 60 23.5%, Neutral 15.8%, Bear ≤ 60 7.6%; Lejar — Bull ≤ 60 14.5%, Neutral 19.2%, Bear ≤ 60 12.2%; Moomoo + uji_kertas (1–8 Okt) — Bull ≤ 60 30.9% (n 55), Neutral 12.5% (n 120) — [T4/nyata4.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/nyata4.pkl)
- Regresi (kelompok tarikh beli, 10–14 kelompok), dengan kawalan log ATR%: jatuh > 8% dalam 5 sesi — BearLama lawan Neutral −5.1 mata (t −0.85), BullLama +1.3 (t 0.27); pulangan kini — BearLama +3.5 mata (t 5.1), BullLama −2.2 (t −4.1); jatuh > 8% setakat ini — BearLama −8.5 (t −2.1), BullLama +2.0 (t 0.8) — [T4/nyata4.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/nyata4.pkl)
- BearLama hadapan = NKE, ROL, BLDR, TTD, MLM, PNR (beli 8–21 Okt) — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log)
- Kuasa: SE BearLama (dengan ATR%) 5.97 mata → MDE (α 5% dua hujung, kuasa 80%) = 16.7 mata; kesan panel OOS (model F) 4.7 mata → perlu ≈ 12.4 kali sampel ≈ 260 posisi unik BearLama; pada kadar 1.5 (semua sumber) hingga 2.5 (Lejar) BearLama unik setiap tarikh beli → ≈ 104–174 tarikh beli (≈ 5–8 bulan dagangan) — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log)
- Rejim tetingkap hadapan: SPY D10+H2 Bull sepanjang 25 Sep–16 Okt, Neutral 19–20 Okt, Bull semula 21 Okt; RV21 SPY 8.8–10.8% setahun (di bawah ambang tertil rendah IS 14.0%). Alam stor pada 22 Okt (818 saham): BearL 0.6%, Bear 14.4%, Bull 21.5% — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log); [T4/nyata4.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/nyata4.pkl)

### Inferences
- Pradaftar menetapkan data hadapan sebagai deskriptif sahaja; t yang besar (5.1, −4.1) datang daripada 10–14 kelompok tarikh dan 6 saham, jadi tidak boleh dipercayai sebagai inferens.
- Tetingkap hadapan ialah rejim "SPY Bull, vol rendah"; dalam panel OOS, BearL model F tetap positif dalam rejim ini (SPY Bull +4.15, t 2.2; vol SPY rendah +4.39, t 2.1), jadi keputusan hadapan yang bertentangan setakat ini lebih mungkin hingar sampel kecil.
- Ujian hadapan yang jujur memerlukan rekod `status`, `umur` dan `ATR%` pada hari isyarat bagi setiap posisi Lejar, dan penilaian selepas ≈ 260 posisi unik BearLama, dengan hasil j8 10 sesi penuh (bukan 5 sesi).

### Gaps
- Lejar baru bermula 16 Okt 2026 (4 tarikh beli); tiada posisi Lejar ditutup lagi.
- Status dikira daripada stor (~520 bar), jadi umur Bull/Bear yang sangat panjang terhad, tetapi > 60 sesi tetap boleh dikenal pasti.

## S7. Bias kemandirian: bolehkah saham yang dinyahsenarai membalikkan dakwaan?

### Takeaway
Harga saham delist tidak dapat diperoleh, jadi hanya batas analitik dikira. Bias kemandirian **tidak munasabah** membalikkan dakwaan 1 dan 4; ia berkemungkinan **memperkecil** kesan BearLama (dakwaan 3); dakwaan 2b (hilang selepas vol) ialah yang paling terdedah.

### Cited Findings
- Panel ialah 431 saham Shariah yang masih wujud dan lulus saringan pada 2026; saham delist tiada — [ujian_panel.md](../Penentuan%20status%20trend%20saham/ujian_panel.md)
- FMP: harga sejarah saham delist memerlukan pelan lebih tinggi (ACCESS DENIED); Moomoo: simbol delist tidak wujud — [T4/prapendaftaran.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/prapendaftaran.md)
- Pulangan delist berkaitan prestasi yang hilang dalam CRSP adalah besar dan negatif; −55% membetulkan bias bagi Nasdaq — [Shumway & Warther 1999, JF (IDEAS)](https://ideas.repec.org/a/bla/jfinan/v54y1999i6p2361-2379.html); masalah pertama didokumenkan oleh [Shumway 1997, JF (IDEAS)](https://ideas.repec.org/a/bla/jfinan/v52y1997i1p327-40.html); konvensyen imputasi −30% bagi NYSE/Amex dipakai oleh pusat data SAFE — [SAFE, Data Description CRSP Shumway](https://datacenter.safe-frankfurt.de/documents/Data_Description_CRSP_Shumway_20250317.pdf)

Kadar delist "pulang modal" (bahagian cerapan Bear yang perlu delist dalam setiap 21 sesi dengan pulangan −30% / −55%) — [T4/akhir4.log](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/akhir4.log)

| Dakwaan | Kesan yang perlu dibalikkan | Kadar diperlukan (−30% / −55%) | Penilaian |
|---|---|---|---|
| 1 (IS) | f21 Bear +2.79% lawan Bull +1.98% (Bear +0.81 mata) | hapus: 2.5% / 1.4% setiap 21 sesi (≈ 26% / 16% setahun) | — |
| 1 (IS → menggagalkan H1) | model D f21 Bull − Bear dari t −1.3 ke t +2 | 9.4% / 5.4% setiap 21 sesi (≈ 70% / 48% setahun) | tidak munasabah |
| 1 (OOS) | f21 Bull +1.87% > Bear +1.19% | bias menguatkan condong OOS sedia ada | — |
| 2b | model D j8 Bull − Bear ke t ≤ −2 | Bear j8 +4.6 (IS) / +3.1 (OOS) mata = 7.1% / 4.2% cerapan Bear ialah bakal-delist dengan j8 = 1 yang tidak diterangkan ATR% | tidak boleh ditolak |
| 3 | BearL | bakal-delist kebanyakannya Bear lama (BearL < USD5: 13% IS, 9% OOS lawan 4.6% / 1.4% semua) → bias ke arah sifar | kesan dipandang rendah |
| 4 | L2 + hilang Bull OOS (−0.44 mata setiap dagangan, 38.4% terkena = −1.15 mata setiap posisi terkena) | 3.8% / 2.1% posisi terkena delist dalam baki pegangan ≤ 30 sesi | tidak munasabah |
| 4 | L2 + masuk Bear OOS (−3.2 mata setiap posisi terkena) | 10.7% / 5.8% | tidak munasabah |

### Inferences
- Batas di atas hanya mengambil kira pulangan peristiwa delist; laluan harga saham delist pada bulan-bulan sebelum delist juga hilang daripada panel. Laluan itu hampir pasti Bear lama dan meruap, jadi ia akan menambah kekuatan BearL dan ATR%, bukan label.
- Saringan Shariah (nisbah hutang kepada nilai pasaran) cenderung menyingkirkan saham tertekan sebelum delist; jadi dalam operasi sebenar papan, sebahagian bias ini juga wujud dalam alam yang diimbas (inferens, tidak diuji).
- Kadar delist "pulang modal" bagi dakwaan 1 dan 4 (≈ 16–70% setahun dalam kumpulan Bear, atau 2–11% posisi dalam satu tempoh pegangan) jauh melebihi kadar yang munasabah bagi saham bermodal sederhana; ini inferens kerana kadar asas tidak dapat disahkan dalam sesi ini.

### Gaps
- Kadar asas delist berkaitan prestasi bagi saham AS tidak dapat diambil (WebFetch gagal DNS bagi NBER/ECGI/HLS); Doidge, Karolyi & Stulz (JFE 2017) dikenal pasti sebagai sumber tetapi angkanya tidak disahkan — [Hedge Fund Alpha, ringkasan](https://hedgefundalpha.com/news/the-u-s-listing-gap/)
- Sampel delist sebenar (harga) memerlukan pelan FMP lebih tinggi atau CRSP.

## S8. Ujian berganda dan keputusan keseluruhan: dakwaan mana yang bertahan?

### Takeaway
Dakwaan 1 dan 4 bertahan (dengan perhalusan rejim bagi 1). Dakwaan 2 bertahan, tetapi kini jelas bergantung pada rejim dan lemah pada 2025–2026. Dakwaan 3 dilemahkan: BearLama ialah bukti OOS yang kukuh tetapi gagal semua kriteria IS selepas kawalan tambahan; BullLama gagal. Tiada ujian utama lulus Holm atas 54 ujian.

### Cited Findings
- Holm atas 54 ujian utama: tiada p < 0.05; terkecil OOS H3e BearL 0.087, OOS H2a 0.12, OOS H3 BearL 0.13. Holm dalam kumpulan "kehadiran" (12 ujian): OOS H3e 0.019, OOS H2a 0.025, OOS H3 BearL 0.025, OOS H3c 0.067, IS H2a 0.086 — [T4/daftar_utama_holm.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_utama_holm.csv)
- BH atas 486 kontras (q 0.05; ambang p ≈ 0.0083): 82 bererti (26 IS, 56 OOS); BearL 1 IS / 16 OOS; BullL 10 / 3; Bull − Bear 12 / 31; peraturan keluar 3 IS / 1 OOS (semuanya pecahan rejim atau adj IS, tiada yang konsisten) — [T4/daftar_kontras_bh.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend4/daftar_kontras_bh.csv)

| Dakwaan asal | Ujian trend4 | Keputusan | Rumusan baharu |
|---|---|---|---|
| 1. Tiada takrif meramal pulangan lebihan 3–30 hari | H1: 0/6 takrif bererti tanda sama dalam IS dan OOS; OOS D10 f21 +1.54 (t 2.2), IS −1.19 (t −1.3); SPY Bear IS −3.43 (t −5.2) | **BERTAHAN** | Tiada ramalan yang stabil; tanda bergantung pada rejim (momentum dalam pasaran tenang, pembalikan dalam tekanan) |
| 2a. D10 memisahkan P(jatuh > 8%/10 sesi) | H2a: −4.05 (t −2.6) / −3.74 (t −3.0) selepas FE sektor + earnings | **BERTAHAN** | Tetapi hilang dalam SPY Bear/vol tinggi dan pada 2025–2026 |
| 2b. Beza hilang selepas ATR14% | H2b: +1.99 (t 1.5) / +0.89 (t 0.8) | **BERTAHAN** | Selepas jarak52 dikawal, Bull lebih berisiko (t 2.6–3.9); paling terdedah kepada bias kemandirian |
| 3a. Bearish > 60 sesi lebih berisiko selepas kawalan vol | E lulus (t 2.4 / 3.3); H3a, H3c, H3d, H3e gagal dalam IS (t 0.2–1.8); OOS lulus semua (t 2.2–3.2); ≥ USD10 lulus kedua-dua (t 2.4 / 3.4) | **DILEMAHKAN** | Bukti sederhana, kebanyakannya OOS; sebahagian ialah "jauh di bawah tinggi 52 minggu"; terbalik selepas panik 2020 |
| 3b. Bullish > 60 sedikit lebih lemah | E lulus (t 3.1 / 2.6); H3b gagal (OOS t 1.5) | **DILEMAHKAN** | Kebanyakannya pulangan 12 bulan tinggi; deskriptif sahaja |
| 4. Tiada keluar berasaskan status mengatasi kaedah/lorong 2 | H5: 0/6 lulus pada 10–50 bps; L2 + hilang Bull −4.7 mata CAGR h2 | **BERTAHAN** | Menjual pada Bear dalam pasaran Bear paling merugikan |
| Posisi hadapan | MDE 16.7 mata lawan kesan 4.7 | **TIDAK MUKTAMAD** | Perlu ≈ 260 posisi unik BearLama (≈ 5–8 bulan) |

### Inferences
- Implikasi papan (inferens): kekalkan pill D10+H2 sebagai deskriptif; turunkan amaran "Bearish lama" daripada "satu-satunya amaran yang tahan" kepada "lebih kerap jatuh tajam (bukti sederhana, 2023–2026)"; paparkan ATR14% dan lencana "earnings dalam 10 sesi" di sebelah pill kerana kedua-duanya membawa maklumat risiko jauh lebih besar; jangan bayangkan "Bullish = lebih selamat" apabila SPY Bear atau turun naik pasaran tinggi; kekalkan larangan keluar automatik berasaskan status.
- Hipotesis hadapan yang dipradaftar dalam laporan asal (BearLama → j8 lebih tinggi daripada sebaya) patut dinilai dengan kawalan ATR%, earnings dan jarak dari tinggi 52 minggu, dalam alam ≥ USD10, selepas ≈ 260 posisi unik BearLama.

### Gaps
- OOS bukan data dara bagi kontras mentah; hanya kawalan baharu yang belum pernah dilihat.
- Tiada SPY Bear dalam OOS; tiada data delist; posisi hadapan < 4 minggu.
