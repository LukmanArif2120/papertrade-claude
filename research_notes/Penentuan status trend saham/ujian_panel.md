# Penentuan status trend saham: ujian empirikal panel 431 saham Shariah AS (2019–2026), termasuk keadaan "mula naik"

Disediakan 23 Okt 2026. Semua angka dalam nota ini datang daripada skrip dan output dalam folder kerja
`/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/` (ringkasnya **T2**). Tiada fail repo diubah selain nota ini.
Tatanama: **mata** = mata peratusan; nombor dalam kurungan = statistik t; **IS** = dalam sampel 2020–2022; **OOS** = luar sampel 2023–2026.
Tanda beza dalam jadual = keadaan paling bullish − keadaan paling bearish (Bull − Bear; bagi W4 = P2 − P4; bagi G5 = Naik kukuh − Turun).

## S1. Bagaimana ujian dijalankan: data, tanpa pandang depan, IS/OOS dan bilangan varian?

### Takeaway
Universe "set 431" = gabungan dataset S1–S4 (108+108+107+108 saham). Label dikira pada tutup t, dan hasil diukur dari **buka t+1**. Keputusan ialah purata keratan rentas setiap tarikh, kemudian purata siri masa, dengan t Newey-West (lag = ufuk; diuji semula pada lag 60 dan 120). Sebanyak 37 takrif keadaan dan 14 peristiwa "mula naik/turun" diuji. Kriteria pemilihan direkod sebelum IS dilihat, dan pilihan IS direkod sebelum OOS dijalankan.

### Cited Findings
- **Universe.** S1 108, S2 108, S3 107, S4 108 ticker. Jumlahnya 431 ticker unik dan 772,590 baris harian, 2019-01-02 hingga 2026-10-02, tanpa pendua. Semua 431 saham berakhir pada 2026-10-02. Sebanyak 80 saham bermula selepas Feb 2019 (IPO/penyenaraian lewat). — [sedia2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sedia2.py); [dataset_S1.csv](/home/user/papertrade-claude/data_mentah/dataset_S1.csv); fungsi `s431()` dalam [scanner.py](/home/user/papertrade-claude/BacktestShariah2/kod/scanner.py)
- **Kualiti data.** Tiada NaN, tiada harga ≤ 0, tiada high < low, dan tiada buka/tutup di luar julat high–low. Terdapat 51 pergerakan harian > 50%. Ia dikekalkan, tetapi pulangan hadapan dipangkas pada [−90%, +300%] dan MFE dipangkas pada +200%. — [sedia2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sedia2.py); [nilai.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/nilai.py)
- **Tempoh.** Label IS dari 2020-01-02 hingga 2022-11-15. Embargo 30 hari memastikan semua hasil IS tamat sebelum 2023. Label OOS dari 2023-01-03 hingga 2026-10-02. Setiap saham mesti mempunyai ≥ 252 bar sejarah supaya semua takrif sah. Sampel IS: 267,319 baris, 394 saham. Sampel OOS: 384,821 baris, 426 saham. — [nilai.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/nilai.py); [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Hasil hadapan.** Semuanya bermula dari buka t+1:
  - pulangan f_h = tutup(t+h)/buka(t+1) − 1 bagi h = 3, 5, 10, 21, 30;
  - **x_** = lebihan atas purata sama berat (EW) semua saham panel pada tarikh sama;
  - **s_** = lebihan atas SPY bagi tempoh sama (buka t+1 → tutup t+h);
  - **j8** = P(rendah intrahari dalam 10 sesi < buka t+1 × 0.92); **n8** = P(tinggi intrahari > +8%); **asim** = n8 − j8;
  - MAE/MFE 10 dan 21 sesi (rendah/tinggi intrahari berbanding buka t+1);
  - vol21 = sisihan piawai pulangan log t+1..t+21, dinisbahkan kepada median hari sama (vr21);
  - **v_** = versi "neutral-volatiliti": hasil tolak purata sel (tarikh × kuintil ATR14% pada t);
  - j8c = takrif kajian lalu (tutup minimum 10 sesi lawan tutup t).
  
  — [sedia2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sedia2.py)
- **Kadar asas.** IS: P(jatuh > 8% dalam 10 sesi) 30.8%, P(naik > 8%) 33.5%, f21 purata +1.97%, MAE21 −9.7%, MFE21 +11.8%. OOS: masing-masing 22.8%, 28.2%, +1.93%, −8.0% dan +10.4%. — [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Statistik.** Untuk setiap takrif, purata hasil dikira bagi setiap tarikh × keadaan (minimum 5 saham), kemudian dipuratakan merentas tarikh. Beza atas − bawah diuji dengan t Newey-West, lag = ufuk; ini mengendalikan pertindihan ufuk dan korelasi keratan rentas pada tarikh sama. Kepekaan lag 60 dan 120 juga dilapor. Peristiwa diuji dengan t berkelompok bulan (NW lag 1 atas jumlah baki bulanan). — [nilai.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/nilai.py); [teguh.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.py)
- **ATR14.** Purata mudah 14 bar julat sebenar, sama seperti `keluar_lorong.atr` (Chandelier). Supertrend menggunakan RMA(10), dan ADX/DMI menggunakan Wilder 14. — [keluar_lorong.py](/home/user/papertrade-claude/BacktestShariah2/standard/keluar_lorong.py); [sedia2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sedia2.py)
- **Kawalan *data snooping*.**
  - Senarai calon tetap ditulis dalam takrif.py sebelum keputusan IS atau OOS dilihat.
  - Kriteria pemilihan dipradaftar dalam [kriteria_prapendaftaran.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kriteria_prapendaftaran.md).
  - Pilihan IS dan 7 hipotesis untuk OOS direkod dalam [pilihan_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/pilihan_IS.json) sebelum `jalan.py OOS` dijalankan.
  
  — [takrif.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/takrif.py); [jalan.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jalan.py)
- **Bilangan varian yang diuji:**
  - 37 takrif keadaan: 29 takrif 3 keadaan (termasuk varian +H2 dan 1 garis dasar rawak); 1 takrif 2 keadaan (Supertrend); 2 takrif 4 peringkat Weinstein; 5 varian G5 (G5a, G5a+H2, G5b, G5c, G5d).
  - 14 peristiwa (7 mula naik, 7 mula turun).
  - 6 analisis umur keadaan × 4 baldi.
  - 3 kontras umur × 3 takrif.
  - 12 label × 3 tetingkap untuk analisis kelewatan, dan 4 sauh tarikh.
  - Kajian terdahulu menambah 10 takrif (D1–D10) dan 3 varian risiko.
  - Lebih kurang 29 hasil diukur bagi setiap takrif.
  - Dengan bilangan ujian sebesar ini, |t| ≈ 3 patut dianggap ambang "bererti" yang munasabah, bukan 2. Garis dasar rawak sendiri mencapai t = +2.5 sekali dalam OOS (lihat S3).
  
  — [takrif.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/takrif.py); [kajian lalu: uji.py, risiko2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend/uji.py)
- **Takrif calon** (semuanya ada dalam takrif.py; SMA/EMA atas tutup terlaras):

  | Kod | Bull | Bear |
  |---|---|---|
  | D10 | C>SMA50>SMA150>SMA200 | C<SMA50<SMA150<SMA200 |
  | TT-penuh | 8 syarat Minervini: C>SMA150 & SMA200; SMA150>SMA200; SMA200 naik 20 sesi; SMA50>SMA150 & SMA200; C>SMA50; C≥1.30×rendah 52 mgg; C≥0.75×tinggi 52 mgg; RS≥70 (persentil dalam universe) | cermin (RS≤30) |
  | TT-ringkas | D10 + SMA200 naik 20 sesi | cermin |
  | W4 | P2: C>SMA150 dan perubahan SMA150 20 sesi > +1% | P4: C<SMA150 dan perubahan < −1%; selainnya P3 (jika peringkat pasti terakhir P2) atau P1 (jika P4) |
  | EMA20/50 | C>EMA20>EMA50, EMA50 naik 5 sesi | cermin |
  | ZZ2 / ZZ3 | HH+HL; pivot disahkan apabila tutup berbalik 2/3×ATR14; ekstrem berjalan yang melepasi pivot terakhir dikira serta-merta | LH+LL |
  | ADX20/25 | +DI>−DI & ADX≥20/25 | −DI>+DI & ADX≥20/25 |
  | ST(10,3) | Supertrend naik (2 keadaan) | Supertrend turun |
  | DON55/20 | tutup > tinggi 55 sesi sebelum → Bull sehingga tutup < rendah 20 sesi | cermin |
  | DONP55 | kedudukan dalam saluran 55 sesi ≥ 2/3 | ≤ 1/3 |
  | LR20/LR50/LR20&50 | t cerun regresi log tutup > 2 | < −2 |
  | K1 | C ≥ SMA50+0.5ATR & SMA50 naik 10 sesi | cermin |
  | K3/K3b TSMOM | jumlah tanda r_n dengan zon mati 0.5σ√n, n={10,21,63} / {21,63,126}, ≥ +2 | ≤ −2 |
  | K4 MAD | SMA21/SMA200 ≥ 1.03 | ≤ 0.97 |
  | K5 SST | C>SMA50>SMA200 & SMA20>SMA50 | C<SMA50<SMA200 |
  | RS70/30 | RS ala IBD (0.4r63+0.2r126+0.2r189+0.2r252) persentil ≥ 70 | ≤ 30 |
  | Rawak | siri D10 saham lain (dipadan rawak, tarikh sama) | — |
  | G5x | 5 keadaan: Naik kukuh (L=+1, S≠−1); Mula naik (L≠+1, S=+1); Mendatar (L=0, S=0); Mula turun (L≠−1, S=−1); Turun (L=−1, S≠+1). G5a L=D10, S=EMA20/50; G5b L=W4-3, S=ST; G5c L=D10, S=ZZ2; G5d L=D10, S=K1 | |
  | +H2 | pengesahan 2 tutup: keadaan baharu diterima hanya jika keadaan mentah sama bertahan 2 sesi berturut-turut | |

  — [takrif.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/takrif.py)
- **Sumber templat luar.** Templat Minervini lazimnya memerlukan harga di atas SMA150/200, SMA150>SMA200, SMA200 naik sekurang-kurangnya sebulan (lebih baik 4–5 bulan), SMA50 di atas kedua-duanya, dan harga di atas SMA50. Ambang 52 minggu yang lazim ialah ≥ 25% di atas rendah dan dalam lingkungan 25% daripada tinggi. Buku Minervini dilaporkan menggunakan 30% bagi ujian rendah (ujian ini menggunakan 30%). RS ≥ 70 ialah angka vendor. — [TradingView "trend template"](https://www.tradingview.com/scripts/trend-template/); [sharpely](https://sharpely.in/blogs/minervini-trend-template-for-stage2-stocks/)
- **Peringkat Weinstein.** Peringkat 1 = dasar di sekitar MA 30 minggu yang mendatar selepas kejatuhan. Peringkat 2 = harga di atas MA 30 minggu yang naik. Peringkat 3 = MA mendatar selepas kenaikan (agihan). Peringkat 4 = harga di bawah MA yang turun. Ujian ini menggunakan SMA150 harian sebagai proksi MA 30 minggu. — [LuxAlgo: Weinstein Stage Analysis](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/)

### Inferences
- Reka bentuk ini menguji label secara keratan rentas: beza berbanding saham lain pada tarikh yang sama. Arah pasaran tidak dinilai. Bagi papan yang memilih antara saham (tahan atau jual satu posisi lawan saham lain), inilah ukuran yang relevan.
- Kerana hasil diukur dari buka t+1, angka ini boleh dicapai dalam praktik. Tiada kos dagangan dimasukkan.

### Gaps
- **Bias kemandirian.** Universe ialah saham yang masih wujud dan lulus saringan Shariah pada 2026. Saham yang dinyahsenarai atau gagal tiada. Ini berkemungkinan meremehkan risiko dan pulangan buruk keadaan Bear, dan senarai keahlian itu sendiri berpandangan depan.
- Hanya 2 rejim. IS merangkumi kejatuhan COVID dan pasaran menurun 2022, manakala OOS kebanyakannya pasaran menaik. Kepekaan rejim hanya diuji melalui SPY > SMA200 (S4).
- RS di sini ialah persentil dalam 431 saham, bukan RS seluruh pasaran AS seperti `data/rs/` dalam repo.

## S2. Takrif keadaan manakah yang paling memisahkan hasil hadapan pada 3–30 hari?

### Takeaway
**Tiada takrif yang meramal pulangan purata** (lebihan 5–30 hari) dalam mana-mana tempoh. Takrif struktur jangka panjang (D10, TT-ringkas, W4, K4 MAD, G5b; semuanya berpaksi SMA50/150/200) memisahkan **risiko mentah** secara konsisten dalam IS dan OOS. Bull mempunyai P(jatuh > 8% dalam 10 sesi) lebih rendah sebanyak 4–7.5 mata (t −3 hingga −3.6) dan volatiliti hadapan yang lebih rendah. Pemisahan ini tidak bertahan selepas volatiliti semasa dikawal (S3). Takrif jangka pendek (ADX, TSMOM, LR20, Supertrend, EMA20/50, ZZ2) tidak memisahkan risiko mentah. Selepas kawalan volatiliti, kesannya **terbalik**.

### Cited Findings
- **Jadual perbandingan penuh.** Larian = tempoh purata keadaan (sesi), IS / OOS. Bahagian = OOS. Beza = Bull − Bear dalam mata % (v_vr21 dalam nisbah), dengan t NW lag ufuk. — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md); [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)

| Takrif | Larian (h) | Tukar/thn | Bahagian B/N/Br % | x_f21 IS | x_f21 OOS | x_j8 IS | x_j8 OOS | v_j8 IS | v_j8 OOS | v_vr21 IS | v_vr21 OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D10 | 17 / 18 | 14.7 / 14.0 | 28/59/13 | -0.32 (-0.2) | +0.69 (+0.9) | -7.2 (-3.5) | -4.0 (-3.0) | -1.1 (-0.7) | +0.5 (+0.4) | -0.045 (-2.1) | -0.028 (-1.8) |
| D10+H2 | 28 / 28 | 8.8 / 8.6 | 28/59/13 | -0.25 (-0.2) | +0.68 (+0.9) | -7.2 (-3.3) | -4.1 (-3.1) | -1.3 (-0.8) | +0.2 (+0.2) | -0.050 (-2.3) | -0.032 (-2.1) |
| TT-penuh | 23 / 22 | 10.8 / 11.1 | 19/71/10 | -0.19 (-0.1) | +1.12 (+1.3) | -6.6 (-2.6) | -2.3 (-1.5) | -0.3 (-0.1) | +1.2 (+0.9) | -0.050 (-2.1) | -0.008 (-0.4) |
| TT-ringkas | 17 / 19 | 14.1 / 13.3 | 27/61/12 | -0.27 (-0.2) | +0.75 (+1.0) | -7.5 (-3.5) | -4.1 (-3.0) | -1.1 (-0.7) | +0.5 (+0.4) | -0.045 (-2.1) | -0.030 (-1.9) |
| TT-ringkas+H2 | 28 / 30 | 8.5 / 8.2 | 27/61/12 | -0.20 (-0.1) | +0.76 (+1.0) | -7.5 (-3.4) | -4.1 (-3.0) | -1.4 (-0.8) | +0.3 (+0.3) | -0.049 (-2.3) | -0.034 (-2.2) |
| W4 (4 peringkat) | 26 / 26 | 9.2 / 9.3 | 44/15/20/21 | -0.07 (-0.1) | +0.34 (+0.6) | -6.1 (-3.5) | -3.8 (-3.6) | -1.1 (-0.8) | -0.1 (-0.1) | -0.055 (-2.9) | -0.036 (-3.0) |
| W4(0.5%) | 23 / 23 | 10.4 / 10.9 | 47/12/16/25 | +0.06 (+0.1) | +0.32 (+0.5) | -5.1 (-3.1) | -3.1 (-3.1) | -0.8 (-0.6) | +0.2 (+0.2) | -0.045 (-2.6) | -0.029 (-2.6) |
| EMA20/50 | 7 / 7 | 37.0 / 36.1 | 40/32/28 | -0.31 (-0.4) | +0.26 (+0.5) | -3.4 (-2.3) | -0.9 (-0.9) | +2.1 (+2.0) | +2.2 (+2.8) | +0.011 (+0.7) | +0.033 (+2.7) |
| EMA20/50+H2 | 11 / 11 | 21.8 / 21.8 | 41/31/29 | -0.31 (-0.4) | +0.24 (+0.5) | -3.3 (-2.2) | -1.0 (-1.0) | +1.8 (+1.7) | +1.9 (+2.4) | +0.004 (+0.2) | +0.025 (+2.1) |
| ZZ2 | 25 / 25 | 9.9 / 9.7 | 37/34/29 | -0.51 (-0.8) | -0.06 (-0.1) | +0.7 (+0.6) | -0.3 (-0.3) | +2.5 (+2.7) | +1.4 (+1.9) | +0.002 (+0.2) | +0.001 (+0.1) |
| ZZ3 | 46 / 46 | 5.1 / 5.2 | 40/34/26 | +0.12 (+0.2) | -0.03 (-0.1) | -2.8 (-2.4) | -0.9 (-1.0) | +0.2 (+0.2) | +0.6 (+0.7) | -0.031 (-2.4) | -0.012 (-1.1) |
| ADX20 | 14 / 15 | 17.3 / 17.1 | 34/41/25 | -0.38 (-0.6) | +0.57 (+1.4) | -0.6 (-0.4) | +1.1 (+1.2) | +3.5 (+3.5) | +3.0 (+4.1) | +0.035 (+2.6) | +0.059 (+4.8) |
| ADX20+H2 | 18 / 18 | 13.6 / 13.6 | 34/41/25 | -0.42 (-0.6) | +0.63 (+1.5) | -0.9 (-0.7) | +1.0 (+1.0) | +2.9 (+3.0) | +2.7 (+3.5) | +0.030 (+2.2) | +0.054 (+4.5) |
| ADX25 | 21 / 21 | 11.7 / 11.8 | 23/62/15 | -0.55 (-0.7) | +0.70 (+1.4) | -0.6 (-0.3) | +1.4 (+1.2) | +4.0 (+3.1) | +3.4 (+3.7) | +0.040 (+2.6) | +0.067 (+4.6) |
| ST(10,3) | 32 / 31 | 7.6 / 7.8 | 53/47 | -0.01 (-0.0) | +0.10 (+0.3) | -1.5 (-1.4) | -0.1 (-0.1) | +1.6 (+2.1) | +2.0 (+3.4) | +0.011 (+1.1) | +0.019 (+2.2) |
| DON55/20 | 33 / 34 | 7.3 / 7.2 | 38/36/26 | -0.22 (-0.3) | +0.29 (+0.5) | -1.6 (-1.0) | -0.8 (-0.7) | +1.8 (+1.5) | +1.5 (+1.7) | +0.000 (+0.0) | +0.015 (+1.2) |
| DONP55 | 7 / 8 | 34.2 / 32.5 | 41/28/31 | -0.65 (-0.8) | +0.35 (+0.7) | -5.0 (-3.3) | -1.9 (-2.0) | +1.4 (+1.3) | +1.6 (+2.1) | -0.008 (-0.3) | +0.019 (+1.5) |
| DONP55+H2 | 13 / 14 | 18.8 / 18.3 | 41/28/31 | -0.55 (-0.6) | +0.36 (+0.7) | -4.9 (-3.1) | -1.9 (-2.0) | +1.1 (+1.1) | +1.3 (+1.7) | -0.015 (-0.7) | +0.011 (+0.9) |
| LR20 | 10 / 10 | 24.1 / 24.5 | 40/28/32 | -0.39 (-0.6) | +0.32 (+0.8) | -1.4 (-1.0) | -0.1 (-0.1) | +2.9 (+3.2) | +2.4 (+2.9) | +0.023 (+1.7) | +0.037 (+3.0) |
| LR20+H2 | 11 / 11 | 22.5 / 22.9 | 40/28/32 | -0.40 (-0.6) | +0.37 (+0.9) | -1.4 (-1.0) | +0.1 (+0.1) | +2.6 (+2.7) | +2.3 (+2.7) | +0.016 (+1.2) | +0.031 (+2.6) |
| LR50 | 24 / 25 | 10.0 / 9.9 | 47/17/35 | -0.99 (-1.1) | +0.24 (+0.5) | -0.5 (-0.4) | -0.7 (-0.8) | +1.4 (+1.3) | +0.5 (+0.6) | -0.016 (-0.9) | -0.004 (-0.4) |
| LR20&50 | 16 / 16 | 15.6 / 15.6 | 27/55/18 | -1.30 (-1.2) | +0.43 (+0.7) | -1.0 (-0.6) | -0.6 (-0.5) | +3.9 (+3.2) | +2.2 (+2.3) | +0.018 (+0.8) | +0.024 (+1.4) |
| K1 | 10 / 10 | 25.1 / 24.6 | 41/30/29 | -0.55 (-0.6) | +0.26 (+0.5) | -1.5 (-1.0) | -1.0 (-1.0) | +2.5 (+2.2) | +1.4 (+1.8) | +0.009 (+0.5) | +0.020 (+1.7) |
| K1+H2 | 16 / 16 | 15.4 / 15.3 | 41/29/29 | -0.51 (-0.6) | +0.24 (+0.5) | -1.4 (-0.9) | -1.1 (-1.1) | +2.3 (+1.9) | +1.1 (+1.4) | +0.005 (+0.3) | +0.014 (+1.2) |
| K3 TSMOM | 6 / 6 | 43.7 / 42.7 | 31/49/20 | -0.29 (-0.4) | +0.44 (+0.8) | -1.4 (-0.9) | +0.2 (+0.2) | +4.4 (+3.8) | +3.7 (+3.9) | +0.054 (+3.2) | +0.063 (+4.3) |
| K3b TSMOM | 9 / 9 | 28.4 / 28.6 | 35/48/17 | -0.14 (-0.1) | +0.33 (+0.5) | -2.5 (-1.3) | -0.9 (-0.7) | +2.8 (+1.9) | +2.5 (+2.6) | +0.004 (+0.2) | +0.026 (+1.8) |
| K4 MAD | 56 / 53 | 4.1 / 4.5 | 54/15/31 | +0.52 (+0.6) | +0.11 (+0.2) | -5.0 (-3.1) | -2.9 (-3.2) | -1.2 (-0.9) | -0.2 (-0.3) | -0.038 (-2.7) | -0.036 (-3.5) |
| K4 MAD+H2 | 57 / 54 | 4.1 / 4.4 | 54/15/31 | +0.53 (+0.6) | +0.10 (+0.2) | -5.0 (-3.1) | -2.9 (-3.2) | -1.3 (-1.0) | -0.3 (-0.3) | -0.038 (-2.7) | -0.037 (-3.6) |
| K5 SST | 15 / 15 | 16.7 / 16.1 | 33/47/20 | +0.16 (+0.1) | +0.32 (+0.5) | -5.1 (-2.7) | -2.8 (-2.4) | +0.0 (+0.0) | +0.7 (+0.7) | -0.028 (-1.4) | -0.010 (-0.8) |
| RS70/30 | 16 / 17 | 15.1 / 14.7 | 29/40/30 | +0.50 (+0.5) | +0.60 (+0.9) | +0.5 (+0.2) | +2.9 (+2.4) | +0.1 (+0.1) | +2.0 (+2.3) | +0.004 (+0.2) | +0.035 (+2.4) |
| Rawak (D10 saham lain) | 17 / 18 | 14.7 / 13.9 | 28/59/13 | -0.13 (-0.3) | -0.10 (-0.4) | -1.3 (-1.4) | +1.4 (+2.5) | +0.6 (+0.9) | +0.4 (+0.9) | -0.010 (-0.9) | +0.010 (+1.0) |
| G5a L=D10 S=EMA20/50 | 8 / 8 | 33.1 / 33.2 | 28/18/23/19/13 | -0.32 (-0.2) | +0.69 (+0.9) | -7.3 (-3.5) | -4.0 (-3.0) | -1.1 (-0.7) | +0.5 (+0.4) | -0.045 (-2.1) | -0.028 (-1.8) |
| G5a+H2 | 12 / 12 | 20.2 / 20.7 | 28/18/22/19/13 | -0.26 (-0.2) | +0.69 (+0.9) | -7.2 (-3.3) | -4.1 (-3.1) | -1.3 (-0.8) | +0.2 (+0.2) | -0.050 (-2.3) | -0.032 (-2.1) |
| G5b L=W4-3 S=ST | 22 / 22 | 10.9 / 11.1 | 29/23/33/15 | +0.12 (+0.1) | +0.29 (+0.4) | -6.9 (-3.7) | -3.7 (-3.0) | -0.4 (-0.3) | +1.0 (+0.9) | -0.050 (-2.2) | -0.021 (-1.4) |
| G5c L=D10 S=ZZ2 | 14 / 14 | 18.0 / 17.8 | 27/19/22/21/12 | -0.45 (-0.3) | +0.66 (+0.9) | -6.7 (-3.2) | -4.0 (-2.9) | -0.6 (-0.4) | +0.6 (+0.5) | -0.046 (-2.1) | -0.031 (-1.9) |
| G5d L=D10 S=K1 | 9 / 9 | 26.5 / 26.6 | 28/18/22/19/13 | -0.32 (-0.2) | +0.69 (+0.9) | -7.2 (-3.5) | -4.0 (-3.0) | -1.1 (-0.7) | +0.5 (+0.4) | -0.045 (-2.1) | -0.028 (-1.8) |

- **Pulangan lebihan.** Bagi semua 37 takrif, beza Bull − Bear x_f21 berada dalam |t| ≤ 1.2 (IS) dan |t| ≤ 1.5 (OOS). Merentas x_f3, x_f5, x_f10, x_f21 dan x_f30, |t| maksimum ialah 1.28 dalam IS (ZZ2 x_f3) dan 1.75 dalam OOS (ADX20 x_f30) (lihat hasil_*.json). Tandanya juga cenderung bertukar: D10+H2 −0.25% (IS) lawan +0.68% (OOS). — [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Kriteria pradaftar.** Kriteria utama yang dipradaftar ialah beza v_j8 Bull − Bear dengan t ≤ −2 dalam IS. **Tiada takrif yang lulus.** Pilihan seterusnya (D10+H2) ditanda **post-hoc**. Ia berdasarkan risiko mentah (x_j8), v_vr21, kestabilan dan keringkasan, dan direkod sebelum OOS. — [pilihan_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/pilihan_IS.json); [kriteria_prapendaftaran.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kriteria_prapendaftaran.md)
- **Keputusan hipotesis OOS** yang direkod sebelum OOS:

  | Hipotesis | Keputusan | Bukti OOS |
  |---|---|---|
  | H1: D10+H2 x_j8 < 0, t ≤ −2 | DISAHKAN | −4.08 mata (t −3.1; NW lag 60: −2.3) |
  | H2: v_j8 D10+H2 tidak bererti | DISAHKAN | +0.25 (t +0.2) |
  | H3: v_vr21 < 0 | DISAHKAN tetapi lemah | −0.032 (t −2.1; lag 60: −1.9; lag 120: −1.7) |
  | H4: x_f21 tidak bererti bagi semua takrif | DISAHKAN | — |
  | H5: takrif jangka pendek v_j8 > 0 | DISAHKAN | ADX20 +3.0 (t 4.1); K3 +3.7 (t 3.9); LR20 +2.4 (t 2.9); ST +2.0 (t 3.4); ZZ2 +1.4 (t 1.9) |
  | H6: N4 x_f21 > 0 | GAGAL, tanda terbalik | −0.67% (t −2.7) |
  | H7: Bull baharu > Bull tua pada v_asim | TIDAK bererti | — |

  — [pilihan_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/pilihan_IS.json); [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json)
- **Kesinambungan dengan kajian terdahulu.** Dengan takrif lama j8c (tutup min 10 sesi lawan tutup t), D10+H2 memberi Bull − Bear −6.70 mata (t −3.7) dalam IS dan −3.73 (t −3.0) dalam OOS. Ini selaras dengan dapatan lalu (+6.0 mata, t 3.7 IS; +3.7, t 3.0 OOS untuk bear − bull). — [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [risiko2.py (kajian lalu)](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend/risiko2.py)
- **Takrif yang hanya bererti dalam satu tempoh:**
  - TT-penuh x_j8: −6.6 (t −2.6) IS, tetapi −2.3 (t −1.5) OOS.
  - DONP55 x_j8: −5.0 (t −3.3) IS, tetapi −1.9 (t −2.0) OOS.
  - ZZ3 x_j8 dan v_vr21: bererti dalam IS sahaja.
  - EMA20/50 x_j8: −3.4 (t −2.3) IS, −0.9 OOS.
  - RS70/30: v_j8 +2.0 (t 2.3) dan x_j8 +2.9 (t 2.4) dalam OOS sahaja.
  
  — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)

### Inferences
- Dari segi "memisahkan hasil hadapan", keluarga D10/TT-ringkas/W4/K4 MAD paling kukuh. Pemisahannya hanya pada risiko dan volatiliti, bukan pulangan. Dalam keluarga ini, beza |t| kurang daripada 1. Oleh itu, mengikut kriteria keringkasan, D10+H2 dipilih: 3 SMA, tanpa ambang, dan larian 28 sesi (lebih kurang satu tempoh pegangan).
- Skema 5 keadaan (G5a/c/d) mewarisi pemisahan D10 tetapi menggandakan kekerapan tukar (20–33 kali setahun lawan 8.6), tanpa menambah pemisahan pada mana-mana hasil.

### Gaps
- Tiada ujian berasingan bagi set S1–S4 (4 subset universe). Kestabilan merentas subset belum dinilai.
- Semua keputusan berwajaran sama setiap tarikh. Wajaran nilai pasaran atau kecairan tidak diuji.

## S3. Adakah pemisahan risiko itu hanya proksi volatiliti? Dan apa yang berlaku pada label jangka pendek?

### Takeaway
Ya. Selepas dikawal dengan ATR14% (kuintil atau desil) atau dengan regresi Fama-MacBeth (log ATR% + log volatiliti 21 hari), beza risiko Bear − Bull bagi D10+H2, W4 dan K4 MAD **hilang** (|t| < 1 dalam IS dan OOS). Label trend jangka panjang menandakan saham yang lebih meruap. Ia tidak menambah maklumat risiko yang belum ada dalam ATR%. Sebaliknya, label jangka pendek "Bear" meramal risiko jatuh neutral-volatiliti yang **lebih rendah** dalam kedua-dua tempoh. Bagi ADX/DMI dan TSMOM 10/21/63 dalam regresi FM: −3.4 hingga −5.4 mata, t −4.1 hingga −4.5. Bagi LR20 dan Supertrend dalam kawalan kuintil: t 2.1–3.4. Ini kesan pembalikan jangka pendek.

### Cited Findings
- **Kawalan volatiliti** ([kawal_vol.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol.py); output [IS](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol_IS.txt), [OOS](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol_OOS.txt)). P(jatuh > 8% dalam 10 sesi), mata %:

  | Takrif | Tempoh | Bull − Bear mentah | dikawal kuintil ATR% | dikawal desil ATR% | FM Bear − Bull (log ATR% + log RV21) |
  |---|---|---|---|---|---|
  | D10+H2 | IS | −7.18 (−3.3) | −1.34 (−0.8) | −0.89 (−0.5) | +0.36 (+0.2) |
  | D10+H2 | OOS | −4.08 (−3.1) | +0.25 (+0.2) | +0.48 (+0.4) | −0.90 (−0.8) |
  | W4-3 | IS | −6.09 (−3.5) | −1.09 (−0.8) | −0.75 (−0.5) | +0.62 (+0.4) |
  | W4-3 | OOS | −3.83 (−3.6) | −0.06 (−0.1) | +0.07 (+0.1) | −0.35 (−0.4) |
  | K4 MAD | IS | −4.97 (−3.1) | −1.21 (−0.9) | −0.99 (−0.8) | +0.82 (+0.6) |
  | K4 MAD | OOS | −2.91 (−3.2) | −0.20 (−0.3) | −0.13 (−0.2) | −0.08 (−0.1) |
  | ADX20 | IS | −0.60 (−0.4) | +3.49 (+3.5) | +3.70 (+3.8) | −3.99 (−4.1) |
  | ADX20 | OOS | +1.07 (+1.2) | +3.02 (+4.1) | +3.12 (+4.2) | −3.43 (−4.4) |
  | K3 TSMOM | IS | −1.44 (−0.9) | +4.38 (+3.8) | +4.73 (+4.2) | −5.44 (−4.4) |
  | K3 TSMOM | OOS | +0.17 (+0.2) | +3.66 (+3.9) | +3.84 (+4.1) | −4.39 (−4.5) |

- **Kuasa penjelasan ATR%.** Dalam regresi FM, pekali log ATR% ialah +29 hingga +31 mata bagi setiap unit log (t 15–23). Inilah peramal utama risiko jatuh 10 hari. — [kawal_vol_IS.txt](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol_IS.txt); [kawal_vol_OOS.txt](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol_OOS.txt)
- **Volatiliti hadapan.** Selepas kuintil ATR% dikawal, D10+H2/W4/K4 Bull masih mempunyai volatiliti 21 sesi hadapan yang sedikit lebih rendah: −0.03 hingga −0.05 nisbah median (t −2.1 hingga −3.6). Untuk D10+H2 OOS, nilai t jatuh kepada −1.9/−1.7 pada lag NW 60/120. W4 dan K4 kekal ≤ −2.4 pada lag 120. Takrif jangka pendek pula menunjukkan arah sebaliknya: ADX20 OOS +0.059 (t 4.8), K3 +0.063 (t 4.3). — [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json); [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)
- **Kepekaan lag NW** (t pada lag ufuk / 60 / 120):
  - D10+H2 x_j8: IS −3.3/−3.1/−2.8, OOS −3.1/−2.3/−2.3.
  - W4-3 x_j8: OOS −3.6/−2.8/−2.6.
  - ADX20 v_j8: OOS +4.1/+4.3/+4.4.
  - Garis dasar Rawak x_j8: OOS +2.5/+1.7/+1.5.
  
  Garis dasar rawak memberi t 2.5 pada lag pendek. Ini bermakna t lag-pendek sedikit terlebih yakin bagi label yang berterusan. Gunakan t lag 60. — [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json)
- **Pulangan 21 hari neutral-volatiliti** (desil ATR%), Bull − Bear:
  - D10+H2: IS +0.58% (t 0.6), OOS +1.26% (t 1.9).
  - ADX20: IS −0.04, OOS +0.82 (t 2.2).
  - K3: IS +0.25, OOS +0.97 (t 2.0).
  
  Kesan ini hanya hampir bererti dalam OOS, jadi ia ditanda "satu tempoh sahaja". — [kawal_vol_IS.txt](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol_IS.txt); [kawal_vol_OOS.txt](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/kawal_vol_OOS.txt)

### Inferences
- Bagi keputusan tahan/jual, label D10 "Bear" sudah dijangka meningkatkan risiko jatuh mentah, tetapi hanya kerana saham Bear lebih meruap. Hentian berskala ATR (Chandelier 4×ATR, lorong 2) sudah mengambil kira hal itu. Label ini tidak patut menjadi isyarat jual tambahan.
- Bagi posisi yang sudah dipegang, label jangka pendek yang bertukar "Bear" (Supertrend turun, −DI > +DI, TSMOM negatif) dikaitkan dengan risiko jatuh 10 hari yang **lebih rendah** selepas volatiliti dikawal. Menjual hanya kerana label jangka pendek bertukar Bear tidak disokong data.

### Gaps
- Kawalan hanya menggunakan ATR14% dan RV21. Kawalan beta, saiz, sektor dan earnings belum dibuat. Sebahagian kesan pembalikan mungkin berpunca daripada hari earnings.
- Tiada ujian dengan kos dagangan atau dengan peraturan jual sebenar (contoh: "jual apabila Bear" lawan Chandelier sahaja).

## S4. Profil setiap keadaan bagi calon utama (D10+H2, W4, G5a+H2): monotonik, kestabilan dan rejim

### Takeaway
D10+H2 adalah monotonik dari segi risiko mentah dan volatiliti (Bull < Neutral < Bear) dalam kedua-dua tempoh, tetapi tidak dari segi pulangan. Keadaan bertahan kira-kira 28 sesi, dengan 8.6 tukar setahun dan bahagian OOS 28/59/13%. W4 memberi 4 peringkat, tetapi "P3 puncak" mempunyai risiko jatuh **terendah**, bukan tertinggi. G5 "Mula naik" dan "Mula turun" tidak membawa pulangan lebih baik atau lebih buruk secara bererti.

### Cited Findings
- **D10+H2** (purata keadaan; % atau nisbah). — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)

| Hasil | Bull IS | Neutral IS | Bear IS | Bull OOS | Neutral OOS | Bear OOS |
|---|---|---|---|---|---|---|
| Pulangan 21h mentah % | 1.85 | 1.93 | 1.98 | 1.87 | 1.90 | 1.19 |
| Lebihan atas SPY 21h % | 1.15 | 1.04 | 1.20 | 0.23 | 0.26 | -0.42 |
| Lebihan EW 5h % | 0.06 | -0.01 | 0.08 | -0.02 | -0.01 | -0.17 |
| Lebihan EW 10h % | 0.15 | 0.00 | 0.06 | -0.06 | -0.04 | -0.34 |
| Lebihan EW 21h % | 0.12 | -0.04 | 0.31 | -0.10 | -0.07 | -0.78 |
| Lebihan EW 30h % | 0.18 | -0.12 | 0.54 | -0.24 | -0.04 | -1.20 |
| P(jatuh>8%, 10h) % | 28.18 | 30.55 | 36.34 | 22.26 | 22.32 | 26.34 |
| P(naik>8%, 10h) % | 31.88 | 33.59 | 36.23 | 26.34 | 27.75 | 30.70 |
| P(jatuh) neutral-vol, mata | -0.55 | -0.49 | 0.89 | 0.96 | -0.50 | 0.71 |
| P(naik)−P(jatuh) neutral-vol, mata | 1.15 | 0.36 | -2.04 | -0.56 | -0.05 | -1.48 |
| MAE 10h % | -6.42 | -6.76 | -7.91 | -5.44 | -5.49 | -6.20 |
| MFE 10h % | 7.16 | 7.65 | 8.91 | 6.39 | 6.59 | 7.20 |
| MAE 21h % | -9.17 | -9.65 | -11.38 | -7.71 | -7.84 | -9.03 |
| MFE 21h % | 11.00 | 11.76 | 13.78 | 9.92 | 10.26 | 11.05 |
| Vol hadapan 21h / median hari | 1.04 | 1.10 | 1.27 | 1.09 | 1.12 | 1.26 |
| Vol hadapan / median kuintil ATR% | 1.04 | 1.04 | 1.09 | 1.09 | 1.07 | 1.12 |

- **W4 (Weinstein harian).** — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)

| Hasil | P2 naik IS | P1 dasar IS | P3 puncak IS | P4 turun IS | P2 OOS | P1 OOS | P3 OOS | P4 OOS |
|---|---|---|---|---|---|---|---|---|
| Bahagian % | 43.4 | 12.1 | 17.8 | 26.7 | 43.6 | 14.9 | 20.1 | 21.4 |
| Lebihan EW 21h % | 0.18 | -0.15 | 0.17 | 0.25 | 0.03 | -0.45 | -0.21 | -0.31 |
| P(jatuh>8%, 10h) % | 29.75 | 28.23 | 25.90 | 35.83 | 22.95 | 21.42 | 19.15 | 26.78 |
| P(naik>8%, 10h) % | 33.26 | 29.88 | 29.93 | 38.41 | 27.70 | 25.51 | 24.33 | 32.23 |
| P(jatuh) neutral-vol, mata | -0.36 | 0.22 | -2.42 | 0.73 | 0.69 | -0.16 | -1.84 | 0.75 |
| MAE 21h % | -9.40 | -9.18 | -8.53 | -11.21 | -7.88 | -7.65 | -7.22 | -8.97 |
| Vol hadapan / median hari | 1.07 | 1.01 | 0.99 | 1.28 | 1.13 | 1.08 | 1.02 | 1.28 |

- **G5a+H2 (5 keadaan).** Lebihan EW 21 hari (IS / OOS):
  - Naik kukuh +0.12 / −0.10
  - Mula naik −0.20 / −0.37
  - Mendatar +0.19 / −0.09
  - Mula turun −0.07 / −0.36
  - Turun +0.31 / −0.78
  
  "Mula turun" (yang kebanyakannya tarik balik dalam trend naik) mempunyai P(jatuh) neutral-vol yang paling rendah: −2.92 (IS) dan −1.60 (OOS). Larian 12 sesi, 20.7 tukar setahun. — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)
- **Monotonik (rho Spearman tertib keadaan lawan purata).**
  - D10+H2: |rho| = 1.0 (monotonik penuh, arah dijangka) bagi x_j8, MAE, MFE dan vr21 dalam kedua-dua tempoh. Bagi x_f21: −0.5 (IS) dan +0.5 (OOS), jadi tidak konsisten.
  - W4: −0.2 bagi x_j8, kerana P3 < P1 < P2 < P4.
  
  — [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Rejim SPY > SMA200 lawan < SMA200.** Bagi D10+H2, beza x_f21 ialah +0.32 (0.2) / −1.35 (−0.6) dalam IS dan +0.82 (1.1) / −0.95 (−0.3) dalam OOS. Beza v_j8 tidak bererti dalam mana-mana rejim. — [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Subset momentum** (ret60 30% teratas, iaitu proksi saham yang dibeli kaedah momentum). Bagi D10+H2, beza tidak bererti dalam IS: x_f21 −1.1 (t −0.4), v_j8 +1.7 (t 0.4). Dalam OOS, sel Bear terlalu jarang dalam subset ini sehingga t tidak dapat dikira. — [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Pengesahan 2 tutup (H2).** H2 tidak mengubah pemisahan: D10 x_j8 −7.2 (−3.5) menjadi −7.2 (−3.3) dalam IS. Ia menaikkan larian purata daripada 17 kepada 28 sesi dan menurunkan tukar setahun daripada 14.0–14.7 kepada 8.6–8.8. — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)

### Inferences
- "P3 puncak" Weinstein, yang dalam teori ialah fasa agihan, tidak menandakan risiko lebih tinggi dalam 10–21 sesi pada data ini. Label 4 peringkat boleh mengelirukan jika diwarnakan sebagai amaran.
- Ketiadaan perbezaan pulangan dalam subset momentum dan dalam kedua-dua rejim menyokong penggunaan label sebagai konteks, bukan isyarat.

### Gaps
- Subset momentum dalam OOS terlalu nipis bagi Bear. Ujian pada posisi sebenar (dagangan kaedah dalam Lejar) belum dibuat.
- Tiada pecahan mengikut sektor atau pusing ganti.

## S5. "Mula naik" / "mula turun": adakah peristiwa permulaan meramal apa-apa, dan berapa lewat ia?

### Takeaway
Daripada 7 calon "mula naik", tiada yang meramal pulangan lebihan positif secara konsisten. Calon terbaik IS (N4: EMA10 > EMA20 ketika SMA50 naik, x_f21 +0.60%) **berbalik** dalam OOS kepada −0.67% (t −2.7). Dalam OOS, kebanyakan peristiwa mula naik diikuti risiko jatuh neutral-volatiliti yang **lebih tinggi**, dan peristiwa mula turun diikuti risiko yang **lebih rendah** (pembalikan). Kadar gagal (tutup di bawah rendah 21 bar sebelum peristiwa) sama dengan jangkaan yang dipadan pada jarak ATR. Label mula naik juga lewat: median 23–60 sesi selepas rendah 63 sesi, apabila harga sudah naik kira-kira 15–30%.

### Cited Findings
- **Jadual peristiwa.** x_ dalam %, v_ dalam mata; t berkelompok bulan. "gagal21 sebenar/padan" = % peristiwa yang tutup di bawah rendah 21 bar sebelum peristiwa (bagi T*: di atas tinggi) dalam 21 sesi, lawan jangkaan berdasarkan jarak ke paras itu dalam unit ATR. "capai" = % yang mencapai D10 Bull (N*) atau D10 Bear (T*) dalam 10 dan 21 sesi. — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md); [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json)

| Peristiwa | n IS/OOS | /saham/thn | x_f10 IS | x_f10 OOS | x_f21 IS | x_f21 OOS | v_j8 IS | v_j8 OOS | v_asim IS | v_asim OOS | gagal21 IS | gagal21 OOS | capai IS | capai OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N1 P1→P2 | 500/882 | 0.58 | -0.29 (-0.5) | -0.27 (-0.9) | -0.01 (-0.0) | -0.41 (-0.7) | +3.20 (+1.4) | +3.03 (+2.0) | -4.11 (-1.1) | -3.23 (-1.5) | 17/20 | 20/19 | 14, 49 | 17, 45 |
| N2 lintas SMA50 naik (≥10 tutup di bawah, SMA50 naik) | 334/581 | 0.38 | +0.52 (+0.9) | +0.19 (+0.6) | +0.74 (+0.9) | -0.22 (-0.6) | +1.31 (+0.6) | -1.61 (-1.0) | -1.82 (-0.5) | +5.18 (+2.1) | 26/25 | 25/24 | 6, 14 | 11, 20 |
| N3 pecah tinggi 20h selepas dasar (julat ≤5 ATR, SMA50 rata/naik) | 6106/8848 | 5.79 | -0.19 (-0.8) | -0.12 (-0.8) | -0.12 (-0.3) | -0.22 (-0.7) | +2.17 (+2.6) | +1.31 (+1.9) | -1.60 (-1.3) | -0.73 (-0.7) | 17/16 | 15/15 | 14, 27 | 15, 28 |
| N4 EMA10>EMA20 + SMA50 naik | 2228/3456 | 2.26 | +0.35 (+1.6) | -0.44 (-3.1) | +0.60 (+1.5) | -0.67 (-2.7) | -1.63 (-2.3) | +1.68 (+2.7) | +3.40 (+2.6) | -1.29 (-1.1) | 29/29 | 30/28 | 14, 24 | 15, 26 |
| N5 HH+HL pertama selepas LH/LL | 2140/3127 | 2.05 | +0.06 (+0.3) | -0.25 (-1.4) | +0.31 (+0.7) | -0.06 (-0.2) | +2.00 (+2.2) | +2.56 (+3.4) | +0.79 (+0.4) | -1.85 (-1.4) | 24/22 | 23/22 | 8, 15 | 10, 18 |
| N6 Supertrend naik | 4046/5928 | 3.88 | -0.15 (-0.5) | -0.03 (-0.2) | +0.00 (+0.0) | -0.32 (-1.2) | +1.95 (+1.6) | +1.01 (+1.1) | -1.84 (-0.9) | +0.74 (+0.6) | 17/18 | 17/17 | 8, 13 | 9, 16 |
| N7 D10 jadi Bull | 4776/7000 | 4.58 | +0.31 (+1.0) | -0.20 (-1.4) | +0.32 (+0.6) | -0.20 (-0.7) | -1.07 (-1.1) | +1.14 (+2.1) | +1.71 (+0.9) | -0.75 (-0.8) | 31/32 | 33/32 | — | — |
| T1 P3→P4 | 630/818 | 0.54 | +0.26 (+0.9) | +0.12 (+0.4) | +0.43 (+0.9) | +0.14 (+0.3) | -1.69 (-1.3) | -3.91 (-3.0) | +3.49 (+1.8) | +4.02 (+1.9) | 22/25 | 27/26 | 18, 45 | 18, 46 |
| T2 lintas SMA50 turun | 275/396 | 0.26 | -0.02 (-0.0) | -0.02 (-0.1) | -0.21 (-0.4) | +0.84 (+1.1) | +2.29 (+0.7) | -2.44 (-1.3) | -3.30 (-0.6) | +3.09 (+0.9) | 29/28 | 34/31 | 6, 15 | 5, 6 |
| T3 pecah rendah 20h selepas dasar | 3989/5832 | 3.82 | -0.11 (-0.4) | -0.08 (-0.4) | -0.43 (-1.2) | +0.09 (+0.2) | -3.16 (-3.4) | -2.57 (-3.2) | +2.20 (+1.6) | -0.15 (-0.1) | 16/17 | 19/20 | 10, 20 | 9, 16 |
| T4 EMA10<EMA20 + SMA50 turun | 1815/2610 | 1.71 | +0.54 (+2.0) | -0.27 (-1.4) | +0.98 (+2.4) | -0.11 (-0.3) | -0.32 (-0.3) | +0.34 (+0.5) | +0.29 (+0.1) | -2.34 (-1.6) | 38/35 | 35/35 | 10, 17 | 8, 15 |
| T5 LH+LL pertama | 2202/3151 | 2.06 | +0.50 (+1.4) | -0.31 (-2.1) | +0.62 (+1.3) | -0.29 (-1.1) | -0.33 (-0.4) | -1.48 (-2.2) | +0.84 (+0.5) | +1.03 (+0.9) | 27/26 | 29/29 | 5, 11 | 5, 10 |
| T6 Supertrend turun | 4023/5938 | 3.89 | -0.15 (-0.5) | +0.22 (+1.5) | -0.23 (-0.5) | +0.31 (+1.4) | -0.26 (-0.2) | -1.82 (-2.8) | -1.96 (-1.0) | +0.10 (+0.1) | 21/22 | 24/24 | 6, 11 | 4, 7 |
| T7 D10 jadi Bear | 2987/3711 | 2.43 | -0.23 (-0.7) | -0.14 (-0.5) | -0.40 (-0.7) | -0.11 (-0.2) | +1.47 (+1.6) | -1.13 (-1.3) | -2.15 (-1.2) | +0.82 (+0.6) | 35/38 | 38/39 | — | — |

- **Garis dasar "capai".** Saham bukan Bull mencapai D10 Bull dalam 10/21 sesi pada kadar 13/20% (IS) dan 14/23% (OOS). Saham bukan Bear mencapai D10 Bear pada 8/13% (IS) dan 7/11% (OOS). Hanya N1 (P1→P2, 45–49% dalam 21 sesi) dan T1 (P3→P4, 45–46%) jelas melebihi kadar asas, dan ini sebahagiannya mekanikal kerana kedua-dua takrif berkongsi SMA150. Bagi N7, peluang mencapai W4 P2 dalam 21 sesi ialah 49–50%, dan peluang mencapai ZZ2 Bull 41–43%. — [hasil_IS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_IS.json); [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json)
- **Kadar gagal mentah lawan dipadan.** Kadar gagal mentah peristiwa N* (17–33%) kelihatan lebih rendah daripada garis dasar semua hari (37%). Namun selepas dipadan pada jarak (tutup − rendah 21 bar)/ATR, beza sebenar − jangkaan berada dalam ±3 mata bagi semua peristiwa dalam kedua-dua tempoh. — [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json)
- **Kelewatan berbanding rendah kitaran.** L_w = rendah terendah dalam [t−w, t], tanpa pandang depan. "pram" = % kes di mana rendah lebih rendah berlaku dalam 21 sesi selepas label (ex-post). — [sauh2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sauh2.py); [sauh2.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sauh2.json)

| Label (tukar ke) | n IS/OOS | lag 63 IS (p25–p75) | gerak 63 IS | pram IS | lag 63 OOS | gerak 63 OOS | pram OOS | lag 126 OOS | gerak 126 OOS |
|---|---|---|---|---|---|---|---|---|---|
| D10+H2 Bull | 2771/4229 | 49 (24–61) | +20.8% | 13% | 48 (25–60) | +18.7% | 15% | 109 | +36.0% |
| W4 P2 | 2700/4236 | 27 (9–52) | +16.1% | 29% | 31 (11–52) | +14.7% | 25% | 100 | +25.8% |
| ST(10,3) Bull | 4046/5928 | 23 (11–54) | +21.1% | 14% | 26 (10–55) | +18.0% | 14% | 80 | +25.6% |
| ZZ2 Bull | 2849/4168 | 36 (25–53) | +23.8% | 13% | 37 (25–54) | +20.2% | 12% | 75 | +27.8% |
| EMA20/50+H2 Bull | 6170/9254 | 49 (30–60) | +24.9% | 10% | 48 (29–59) | +21.2% | 10% | 91 | +32.2% |
| K4 MAD Bull | 1051/1795 | 36 (24–54) | +30.0% | 8% | 38 (25–55) | +25.7% | 6% | 68 | +31.5% |
| G5a+H2 Mula naik | 3368/5320 | 43 (26–58) | +25.6% | 11% | 42 (25–57) | +21.0% | 10% | 66 | +27.7% |
| N4 | 2228/3456 | 58 (49–62) | +23.4% | 12% | 57 (48–61) | +20.6% | 11% | 96 | +33.7% |
| N2 | 334/581 | 60 (54–62) | +19.0% | 18% | 57 (51–61) | +17.0% | 15% | 100 | +30.7% |
| D10+H2 Bear | 1837/2324 | 45 (22–59) | -18.5% | 12% | 46 (24–59) | -15.7% | 17% | 107 | -24.6% |
| W4 P4 | 2111/2864 | 35 (16–53) | -15.0% | 23% | 34 (14–52) | -13.1% | 28% | 96 | -19.6% |
| ST(10,3) Bear | 4023/5938 | 12 (6–39) | -13.3% | 20% | 14 (7–40) | -12.6% | 23% | 26 | -14.5% |

- **Tetingkap 252 sesi.** Tukar D10+H2 ke Bull berlaku median 201–210 sesi selepas rendah 52 minggu, apabila harga sudah naik +59% (OOS) hingga +86% (IS) daripada rendah itu. — [sauh2.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sauh2.json)

### Inferences
- Tiada "mula naik" yang mempunyai kelebihan ramalan yang tahan merentas tempoh. Pembalikan N4 menunjukkan bahaya memilih peristiwa berdasarkan satu tempoh. Dalam OOS, isyarat mula naik cenderung diikuti oleh **kenaikan risiko** jatuh 10 hari selepas volatiliti dikawal (N1, N3, N4, N5, N7: v_j8 +1.1 hingga +3.0, t 1.9–3.4). Ini selaras dengan pembalikan jangka pendek dalam S3.
- Supertrend ialah label "naik" terawal (median 23–26 sesi selepas rendah 63 sesi), tetapi 14% kes ialah pramatang. W4 P2 kelihatan awal (27–31 sesi), tetapi 25–29% kes pramatang. D10+H2 paling lewat (48 sesi; gerak +19–21%), tetapi pramatangnya hanya 13–15%.
- Oleh itu, "mula naik" lebih jujur dipaparkan sebagai fakta deskriptif ("baru bertukar Bull") daripada sebagai keadaan ramalan.

### Gaps
- Ambang peristiwa dipilih sekali sahaja (N=10 tutup, julat dasar ≤ 5 ATR, pivot 2 ATR). Kepekaan parameter tidak diuji supaya tidak menambah *snooping*.
- Lag diukur berbanding rendah terendah dalam tetingkap tetap, bukan pivot kitaran ex-post sebenar (contoh: zigzag 20%). Lag median D10 juga dipotong oleh tepi tetingkap (13–16% kes di tepi bagi w = 63).

## S6. Umur keadaan dan sauh "sejak bila / dari mana"

### Takeaway
Umur keadaan lebih bermaklumat daripada keadaan itu sendiri, dan konsisten dalam kedua-dua tempoh:
- **Bear lama (> 60 sesi)** ialah kumpulan paling berisiko: P(jatuh > 8% dalam 10 sesi) +11 hingga +14 mata berbanding Bear ≤ 60 sesi (t ≈ 5); +3.9 hingga +8.0 mata selepas volatiliti dikawal.
- **Bear baharu (≤ 20 sesi)** kurang berisiko berbanding Bear yang lebih tua.
- **Bull lama (> 60 sesi)** mempunyai risiko neutral-volatiliti +2.5 hingga +3.1 mata lebih tinggi berbanding Bull yang lebih muda.

Bagi sauh tarikh, "sejak" yang stabil ialah tarikh tukar yang disahkan. "Titik mula" yang boleh dipaparkan tanpa pandang depan ialah rendah 63 sesi sebelum tukar. Rendah ini bukan rendah kitaran 6–12 bulan.

### Cited Findings
- **Kontras umur** (beza mata %; t NW lag ufuk; t lag 60). — [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json); [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)

| Takrif | Keadaan | Kontras | Hasil | IS | OOS |
|---|---|---|---|---|---|
| D10+H2 | Bear | > 60 lawan ≤ 60 sesi | x_j8 | +11.26 (+5.1; +4.9) | +12.47 (+5.6; +5.4) |
| D10+H2 | Bear | > 60 lawan ≤ 60 | v_j8 | +3.92 (+2.3; +3.1) | +6.49 (+3.2; +4.1) |
| D10+H2 | Bear | ≤ 20 lawan > 20 | x_j8 | -4.11 (-2.6; -2.1) | -3.66 (-4.4; -4.5) |
| D10+H2 | Bear | ≤ 20 lawan > 20 | v_j8 | -1.59 (-1.2; -1.0) | -2.87 (-3.8; -4.0) |
| D10+H2 | Bull | > 60 lawan ≤ 60 | x_j8 | +2.95 (+1.8; +1.2) | +4.06 (+3.0; +2.2) |
| D10+H2 | Bull | > 60 lawan ≤ 60 | v_j8 | +2.70 (+2.2; +1.7) | +2.72 (+2.7; +2.5) |
| D10+H2 | Bull | > 60 lawan ≤ 60 | v_asim | -5.22 (-2.6; -2.5) | -2.58 (-1.6; -1.3) |
| D10+H2 | Bull | ≤ 20 lawan > 20 | v_j8 | -0.86 (-0.8; -0.8) | -1.83 (-2.2; -2.4) |
| D10+H2 | Bull | ≤ 20 lawan > 20 | x_f21 | +0.59 (+1.2; +1.2) | +0.42 (+1.3; +1.4) |
| D10+H2 | Bull | ≤ 5 lawan > 5 | v_asim | +1.72 (+1.1; +1.1) | +0.64 (+0.5; +0.6) |
| W4 | P4 | > 60 lawan ≤ 60 | x_j8 | +9.24 (+6.7; +5.5) | +6.88 (+7.7; +6.5) |
| W4 | P4 | ≤ 5 lawan > 5 | v_j8 | -3.18 (-3.3; -2.7) | -3.78 (-5.2; -5.6) |
| TT-ringkas+H2 | Bear | > 60 lawan ≤ 60 | v_j8 | +3.92 (+2.3; +3.0) | +8.03 (+4.1; +4.1) |
| TT-ringkas+H2 | Bull | > 60 lawan ≤ 60 | v_j8 | +3.11 (+2.2; +1.8) | +2.51 (+2.3; +2.2) |

- **Bahagian sampel OOS.** D10+H2 Bear > 60 sesi meliputi 1.0% cerapan; Bear 21–60 sesi 4.4%; Bull > 60 sesi 3.8%. Bagi D10+H2, tiada kontras umur yang bererti pada pulangan lebihan 21 hari (|t| ≤ 1.4). TT-ringkas+H2 Bull > 60 sesi mencatat −1.19% (t −1.7) dalam IS sahaja. — [hasil_OOS.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/hasil_OOS.json); [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json)
- **Sauh tarikh** bagi tukar D10+H2 (ex-post "sebenar" = ekstrem dalam [t−126, t+21]):
  - Tarikh tukar (A) berlaku median 105–109 sesi selepas titik itu, dan harga sudah +36–42% (Bull) atau −25 hingga −29% (Bear).
  - Sauh B (ekstrem 63 sesi lalu) tepat ±2 sesi dalam 15–17% kes.
  - Sauh C (pivot ZZ2 disahkan terakhir) tepat 4–5%.
  - Sauh D (mula larian tutup di atas SMA50) tepat 0.3–1.2%.
  - Titik sebenar berlaku selepas tukar hanya dalam 2.8–4.6% kes.
  
  — [teguh.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/teguh.json)
- **Kebolehpercayaan rendah 63 sesi.** Rendah 63 sesi sebelum tukar D10+H2 ke Bull tidak ditembusi dalam 21 sesi berikutnya dalam 85–87% kes. Bagi rendah 126 sesi, kadarnya 95–97%; bagi rendah 252 sesi, 98–99.5%. — [sauh2.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sauh2.json)

### Inferences
- **Soalan "sejak bila Bullish"** paling jujur dijawab dengan tarikh tukar yang disahkan, iaitu tarikh tutup kedua H2. Ia stabil: hanya 8.6 tukar setahun, dan titik ekstrem sebenar jarang berlaku selepasnya.
- **Soalan "dari mana ia mula naik"** ialah konsep yang bergantung pada tetingkap. Untuk papan swing, rendah 63 sesi sebelum tukar memberi titik yang mudah difahami: median 48 sesi sebelum tukar dan +19–21% di bawah harga semasa, dengan 85% kebolehpercayaan. Rendah 126 sesi pula menggambarkan permulaan trend jangka sederhana (+36–41%).
- **Umur boleh menjadi penanda risiko sebenar.** Dalam keluarga label jangka panjang, "Bear lama" (D10+H2 Bear > 60 sesi atau W4 P4 > 60 sesi) ialah satu-satunya penanda yang menambah risiko jatuh melebihi volatiliti secara konsisten, dengan t ≥ 3 pada lag 60 dalam kedua-dua tempoh. Ia boleh dipaparkan sebagai amaran. "Bear baharu" pula tidak patut diwarnakan lebih teruk daripada Bear biasa.

### Gaps
- Kontras umur ditulis selepas jadual baldi umur IS dilihat (baldi itu sendiri dipradaftar). Kontras tersebut perlu dianggap eksploratori walaupun konsisten dalam OOS.
- Mekanisme kesan "Bear lama" (kesusahan kewangan? kecairan?) belum diuji. Kesannya mungkin lebih besar dalam universe sebenar yang mempunyai saham dinyahsenarai.

## S7. Cadangan takrif: bilangan keadaan, peraturan tepat, pengesahan dan sauh tarikh

### Takeaway
Gunakan **3 keadaan D10 dengan pengesahan 2 tutup (D10+H2)**, ditambah **umur keadaan** dan dua sauh tarikh. Jangan tambah keadaan "Mula naik/Mula turun" sebagai keadaan ramalan. Jika perlu dipaparkan, gunakan sub-label deskriptif "Bull baharu" / "Bear baharu" (≤ 20 sesi), dan amaran "Bear lama" (> 60 sesi). Label ini ialah konteks risiko dan volatiliti, bukan isyarat beli atau jual.

### Cited Findings
- **Peraturan yang disyorkan** (semua atas tutup terlaras, SMA = purata mudah; memerlukan ≥ 200 bar):

  ```
  mentah_t = Bull    jika C_t > SMA50_t > SMA150_t > SMA200_t
             Bear    jika C_t < SMA50_t < SMA150_t < SMA200_t
             Neutral selainnya
  keadaan_t: kekal keadaan_{t-1} kecuali mentah_t = mentah_{t-1} = X ≠ keadaan_{t-1}  → keadaan_t = X   (H2)
  umur_t   = bilangan sesi berturut-turut keadaan_t (1 = tutup pengesahan)
  sub-label: "baharu" umur ≤ 20; "matang" 21–60; "lama" > 60
  "sejak"  = tarikh tutup pengesahan (umur = 1); papar juga perubahan % sejak tarikh itu
  "titik mula" (Bull) = rendah terendah dalam 63 sesi hingga tarikh pengesahan (tarikh + harga);
             (Bear)  = tinggi tertinggi dalam 63 sesi; kemas kini jika ditembusi semasa keadaan sama
  ```

  Sifat diukur: larian purata 28 sesi; 8.6 tukar/saham/tahun; bahagian OOS Bull 28%, Neutral 59%, Bear 13%. Bull − Bear P(jatuh > 8% dalam 10 sesi): −7.2 mata (t −3.3) IS dan −4.1 (t −3.1) OOS. MAE21 Bull −7.7% lawan Bear −9.0% (OOS). Volatiliti hadapan Bull 1.09 lawan Bear 1.26 × median (OOS). — [takrif.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/takrif.py); [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)
- **Alternatif yang setara secara statistik:**
  - **TT-ringkas+H2**: D10 + SMA200 naik 20 sesi. Pemisahan hampir sama (x_j8 −7.5/−4.1), tetapi ada satu parameter lebih.
  - **W4** (4 peringkat Weinstein, SMA150 + cerun 20 sesi ±1%). x_j8 −6.1/−3.8, v_vr21 paling kukuh (t −2.9/−3.0), dan P4 > 60 sesi ialah amaran yang kuat (x_j8 +9.2/+6.9, t 6.7/7.7). Namun P3 bukan amaran, dan 25–29% tukar ke P2 pramatang.
  - **K4 MAD** (SMA21/SMA200 ±3%): paling stabil (4.1–4.5 tukar setahun), sesuai untuk watchlist, tetapi pemisahannya lebih kecil (x_j8 −5.0/−2.9).
  
  — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md); [sauh2.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/sauh2.json)
- **Tidak disyorkan sebagai label utama:**
  - Takrif jangka pendek (EMA20/50, ADX, TSMOM, LR20, K1, DONP55, Supertrend). Tiada pemisahan risiko mentah, dan selepas volatiliti dikawal Bull mempunyai risiko jatuh yang lebih tinggi (t 2–4.4).
  - Skema 5 keadaan G5. Tiada pemisahan tambahan dan 20–33 tukar setahun.
  - TT-penuh dan DONP55. Kedua-duanya hanya bererti dalam IS.
  
  — [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/jadual.md)
- **Senarai fail.** Skrip: sedia2.py (panel), takrif.py (calon tetap), nilai.py (statistik), jalan.py IS|OOS, kawal_vol.py, teguh.py, sauh2.py, jadual.py, lapor.py/lapor2.py/lapor3.py (cetakan). Output: panel2.pkl, hasil_IS.json, hasil_OOS.json, teguh.json, sauh2.json, kawal_vol_IS.txt, kawal_vol_OOS.txt, jadual.md, kriteria_prapendaftaran.md, pilihan_IS.json. — [folder T2](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend2/)

### Inferences
- **Bilangan keadaan.** 3 keadaan sudah mencukupi. Data tidak menyokong pembahagian yang lebih halus untuk tujuan ramalan. Yang menambah maklumat ialah dimensi **umur**, bukan keadaan tambahan.
- **Kegunaan dalam Positions.** Paparkan "Bull · 12 sesi (sejak 3 Okt, +6.1%) · titik mula 14 Ogos @ 41.20". Jangan jadikan Bear sebagai isyarat jual, kerana keluar kekal melalui kaedah dan Chandelier. "Bear lama" boleh diwarnakan sebagai amaran risiko. Bagi kaedah pantulan, label Bear memang dijangka dan tidak patut diwarnakan.
- **Kegunaan dalam Watchlist.** "Bull baharu" ialah penanda deskriptif "mula naik" yang paling stabil. Jangkakan ia lewat kira-kira 48 sesi dan +19–21% dari rendah 63 sesi. Ia tidak meramal pulangan lebih baik.
- **Pengesahan.** H2 dikekalkan. Ia mengurangkan tukar sebanyak 40% tanpa kehilangan pemisahan.

### Gaps
- Belum diuji pada posisi sebenar Papertrade C atau Lejar Penuh, contohnya pulangan baki hingga keluar mengikut keadaan dan umur, atau peraturan maya "jual apabila Bear lama".
- Belum diuji pada universe tanpa bias kemandirian atau pada data sebelum 2019.
- Kos dagangan, earnings dan sektor tidak dikawal. Keputusan neutral-volatiliti bergantung pada ATR14% sebagai proksi risiko.
