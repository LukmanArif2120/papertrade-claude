# Logik keputusan dan konsistensi metrik dashboard (audit, 22 Okt 2026)

Skop: nombor dan label mana yang sepatutnya memandu keputusan pengguna ("kaedah mana layak wang sebenar"), di mana ia bercanggah, dan apa yang tiada berbanding matlamat (`00_NOTA_SERAHAN.md` §1). Semua sumber ialah fail repo tempatan (laluan relatif dari akar repo; `:N` = nombor baris). Semakan data dibuat dengan Python baca-sahaja pada keadaan repo 22 Okt 2026 (commit terakhir `077f6d2`). Tiada fail repo lain diubah.

Matlamat rujukan: untung minimum 10% sebulan, pegang kira-kira sebulan, kebarangkalian menang tertinggi diutamakan, dan kaedah hanya berjaya jika mengalahkan EW (beli semua saham Shariah sama berat); portfolio backtest 8 slot × 12.5% — [00_NOTA_SERAHAN.md:5-9](BacktestShariah2/00_NOTA_SERAHAN.md#L5).

## S1. Senarai semua sistem penilaian kaedah, peraturannya, asas sampel, dan sama ada ia bercanggah

### Takeaway
Sekurang-kurangnya lapan permukaan menilai atau menyusun kaedah, dengan lima takrif "cukup data" dan tiga asas sampel berbeza (Papertrade C, Lejar Penuh, backtest). Hari ini ia memberi jawapan bertentangan tentang kaedah teratas: gabungan beku (M70, M03, M18) dipilih oleh Skor swing v2 atas data C yang belum matang. Ketiga-tiganya berada di kedudukan #35, #40 dan #53 daripada 75 dalam Papan Penganalisis, dan M03 berstatus DITOLAK dalam backtest. Kaedah #1 Penganalisis (M21) juga DITOLAK dalam backtest. Ketiga-tiga kaedah GUNA (M96, M30, M79) pula terkeluar daripada senarai swing kerana pegangannya lebih 30 hari.

### Cited Findings

**(a) Label tugasan_v3 §7: TERUSKAN / PERHATI / HENTIKAN (skor Untung×Selamat)**
- Peraturannya: < 20 dagangan tertutup = `BELUM CUKUP DATA`. Selepas ≥ 20: HENTIKAN jika untung purata ≤ −3%, kadar gagal ≥ 75% atau skor < 25; TERUSKAN jika skor ≥ 55 dan purata > 0; selainnya PERHATI. Metrik portfolio menganggap USD1,000 setiap posisi — [tugasan_v3.md:74-77](BacktestShariah2/standard/tugasan_v3.md#L74)
- Formula halaman: U = 0.6·clamp((purata+5)/15) + 0.4·kadar menang; S = 0.6·clamp(1+MAE purata/10) + 0.4·clamp(1+terburuk/20); skor = 100·U·S·min(1, n/5). Pemalar `PR_MIN_N=5, PR_MIN_TUTUP=20` — [dashboard_v2.html:1424](BacktestShariah2/standard/dashboard_v2.html#L1424), [dashboard_v2.html:1436-1448](BacktestShariah2/standard/dashboard_v2.html#L1436)
- Salinan Python yang sama (rekod `prestasi/ringkasan`): [harian_prestasi.py:30-38](BacktestShariah2/standard/harian_prestasi.py#L30)
- Asasnya ialah akaun Papertrade C, Moomoo atau Gabung. Label memakai asas (semua) = posisi selesai + posisi dipegang pada harga semasa, tanpa had umur — [dashboard.md:32](BacktestShariah2/standard/dashboard.md#L32); [dashboard_v2.html:1431-1433](BacktestShariah2/standard/dashboard_v2.html#L1431)
- "Tarikh adil" = hari dagangan ke-N selepas belian pertama, dengan N = purata hari pegang backtest — [dashboard.md:33](BacktestShariah2/standard/dashboard.md#L33)
- Kiraan semula baca-sahaja atas `papertrade/claude*.csv`: 4,289 baris, 4,118 sah, dibeli 8–21 Okt 2026 (10 hari beli berbeza). Hasilnya kira-kira 0 TERUSKAN, 13 PERHATI, 4 HENTIKAN (M08, M123 dan dua lagi) dan 103 BELUM CUKUP DATA. Nota: MAE dianggar dengan min(untung, 0) kerana `prestasi/mae` tidak dibaca, jadi skor U×S sedikit terlebih — kiraan sendiri daripada [papertrade/](BacktestShariah2/papertrade/)
- Kaedah yang mencapai 20 tutup dahulu ialah kaedah yang keluar cepat (cth. M03: 56 tutup, pegang backtest 7.8 hari). Laporan KPI menamakan ini bias keluar awal dan penapisan kanan — [Skor KPI…md:48](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L48)

**(b) "Terbaik ikut % untung" (Prestasi, v95)**
- Kaedah dengan ≥ 20 dagangan selesai disusun ikut untung purata % semua dagangan (15 teratas). Ia menggantikan air terjun USD, manakala label TERUSKAN/PERHATI/HENTIKAN tidak berubah — [dashboard.md:3](BacktestShariah2/standard/dashboard.md#L3) (perenggan versi 95)

**(c) Skor kaedah swing v2 (Prestasi › Setiap kaedah; v96–v102): Teras / Calon / Pantau, Monte Carlo, gabungan cadangan**
- Ada 9 metrik dalam 4 tunjang U40 K20 R25 B15, digabung secara geometrik (lantai 5). Julat beku = persentil 5–95 merentas 75 kaedah swing backtest 431. Pintunya: ≥ 20 selesai (atau matang), ≥ 10 hari beli, swing 3–30 dan untung dilaras > 0 — [dashboard.md:3](BacktestShariah2/standard/dashboard.md#L3) (versi 99); `SKW_W={U:40,K:20,R:25,B:15}` [dashboard_v2.html:2574](BacktestShariah2/standard/dashboard_v2.html#L2574)
- Asasnya ialah posisi matang jika ≥ 20 matang dan ≥ 10 hari beli; jika tidak, SEMUA posisi ("awal"). Lorong dipilih ikut purata hadapan yang lebih tinggi (kaedah atau henti/lorong 2), dengan penalti SE·√((1−ρ)/π). Ia dikecutkan ke `jangkaan` dan `n0` Papan Penganalisis (`mu0=an.jangkaan`) — [dashboard_v2.html:2612-2669](BacktestShariah2/standard/dashboard_v2.html#L2612)
- "Stabil" = P(4 teratas) ≥ 50% dalam 1,000 simulasi Monte Carlo (`skwMC`), dan menjadi syarat Teras — [dashboard_v2.html:2670-2680](BacktestShariah2/standard/dashboard_v2.html#L2670); [dashboard.md:3](BacktestShariah2/standard/dashboard.md#L3) (versi 100)
- Teras memerlukan skor ≥ 70%, ≥ 20 hari beli dan P(untung > 0) ≥ 90%. Selainnya "Calon (awal)" — [dashboard.md:3](BacktestShariah2/standard/dashboard.md#L3) (versi 98)
- Gabungan beku SEMENTARA 22 Okt 2026 (akaun Papertrade C, data hingga 21 Okt): M70 (skor 84%, P(4 teratas) 0.95, lorong kaedah, 4 slot), M03 (76%, 0.88, lorong henti, 3 slot) dan M18 (74%, 0.81, lorong kaedah, 3 slot). M35 tidak dipilih kerana pertindihan 24%; M13 kerana P(4 teratas) 49% — [gabungan_beku.json](BacktestShariah2/data/analisis/gabungan_beku.json)

**(d) Papan Penganalisis (tab Analisis; tugasan_v3 §11): skor pengecutan, status, pantau**
- Skor = (n0·jangkaan + n·purata matang)/(n0+n). Jangkaan = purata set 431 × (25% + 25% bagi setiap semakan luar sampel lulus: S1–S4, WFO W01, AUTOTUNE). n0 = 1/(1/30 + 1/dagangan backtest). Bukti hadapan = Lejar Penuh + kohort C pra-Lejar. Matang = umur ≥ maks(14 hari, 1.5 × hari pegang backtest) — [tugasan_v3.md:113-117](BacktestShariah2/standard/tugasan_v3.md#L113)
- Sejak 22 Okt: n berkesan ikut hari beli dan purata matang PENUH; purata dipangkas 5% hanya sebagai semakan — [tugasan_v3.md:118-121](BacktestShariah2/standard/tugasan_v3.md#L118)
- Status BELUM CUKUP (< 20 matang atau < 10 hari beli), AMARAN (≥ 10 matang, t < −2), KUAT/LEMAH (julat 95% > 0 / < 0) atau PERHATI. Kedudukan ikut skor sebulan = skor ÷ hari pegang × 21 — [tugasan_v3.md:122-123](BacktestShariah2/standard/tugasan_v3.md#L122); [penganalisis.py:470-479](BacktestShariah2/standard/penganalisis.py#L470)
- Pantau (label sahaja): BERSARA = P(μ ≤ 0) > 0.9 dengan ≥ 20 hari beli, atau ≥ 2 amaran CUSUM. GANTUNG = kejatuhan kohort > 1.5× maks backtest, tempoh di bawah puncak > maks backtest, atau purata 20 hari beli < p5 bergulir. Lorong 1 sahaja — [penganalisis.py:24-33](BacktestShariah2/standard/penganalisis.py#L24), [penganalisis.py:70-77](BacktestShariah2/standard/penganalisis.py#L70), [penganalisis.py:390-449](BacktestShariah2/standard/penganalisis.py#L390)
- Output semasa (`papan.json` dibina 21 Okt 23:15 MYT, data hingga 20 Okt): 134 baris, SEMUA `BELUM CUKUP`, 75 swing. Rows TIDAK mempunyai medan `pantau` kerana fail dijana sebelum commit `326493c` (22 Okt 06:58) yang menambah pantau — semakan sendiri atas [papan.json](BacktestShariah2/data/analisis/papan.json); log git
- "0 posisi matang daripada 7161. Kedudukan kini = backtest dipotong. Kaedah pertama dengan 20 posisi matang dijangka 26 Okt 2026" — [PENGANALISIS.md:8](BacktestShariah2/laporan/PENGANALISIS.md#L8)
- 5 swing teratas (skor sebulan): M21 +3.40%, M140 +2.25%, M144 +1.72%, M32 +1.69% dan M84 +1.53% — [PENGANALISIS.md:30-34](BacktestShariah2/laporan/PENGANALISIS.md#L30)

**(e) Status backtest GUNA / UJI KERTAS / SIMPAN / DITOLAK (tab Backtest: 7 langkah saringan dan pingat; podium Ringkasan)**
- 88 kaedah M: GUNA 4, UJI KERTAS 23, SIMPAN 30, DITOLAK 31. Lima teratas ikut skor ialah M96, M114, M30, M79 dan M111 — [00_NOTA_SERAHAN.md:14-36](BacktestShariah2/00_NOTA_SERAHAN.md#L14)
- Tab Backtest "Keputusan" = 7 langkah saringan + pingat bagi varian yang digunakan; Ringkasan memapar "Terbaik ikut backtest (podium)" — [dashboard.md:11](BacktestShariah2/standard/dashboard.md#L11), [dashboard.md:15](BacktestShariah2/standard/dashboard.md#L15)
- Dalam `papan.json` (134 kaedah aktif): SIMPAN 52, DITOLAK 50, UJI KERTAS 29, GUNA 3. Ketiga-tiga GUNA (M96 53.7 hari, M30 33.7 hari, M79 59.8 hari) bukan swing, jadi tiada nombor kedudukan swing — semakan sendiri atas [papan.json](BacktestShariah2/data/analisis/papan.json)

**(f) Eksperimen portfolio_slot (RS_10, RAWAK_10, GABUNGAN_10, TOP1_10, RAWAK_KAEDAH_10)**
- RS_10 = slot diisi saham RS pasaran tertinggi; RAWAK_10 = kawalan. GABUNGAN_10 = kaedah beku dengan kuota slot dan lorong setiap kaedah. TOP1_10 = kaedah #1 sahaja. RAWAK_KAEDAH_10 = kaedah rawak beku. Dibina semula daripada Lejar setiap malam, dengan log gantung daripada pantau — [portfolio_slot.py:3-12](BacktestShariah2/standard/portfolio_slot.py#L3), [portfolio_slot.py:36-38](BacktestShariah2/standard/portfolio_slot.py#L36)
- Keadaan repo: hanya fail RS_10 dan RAWAK_10 wujud. Tiada fail GABUNGAN_10/TOP1_10/RAWAK_KAEDAH_10 dan tiada `gantung.csv`, kerana `mula_jejak` = 22 Okt 2026 — [portfolio_slot/](BacktestShariah2/portfolio_slot/), [gabungan_beku.json](BacktestShariah2/data/analisis/gabungan_beku.json)
- 16–20 Okt (3 sesi): RS_10 −5.06% (MDD −6.04%), RAWAK_10 +2.43%, SPY −0.54%. Tiada dagangan keluar. Posisi SVRN dalam RS_10 −36.65% — [portfolio_slot/RINGKASAN.md:5-25](BacktestShariah2/portfolio_slot/RINGKASAN.md#L5)

**(g) Gred calon A–E (Sektor, Industri v2, RS, Pemangkin, QR)**
- Gred direkod pada hari isyarat dan tidak menapis. Gred keseluruhan = purata mata Industri, Pemangkin dan QR. Prestasi setiap gred hanya dinilai selepas ≥ 20 dagangan tertutup, dan gred v1 (sebelum 19 Okt) tidak boleh dicampur — [tugasan_v3.md:80-90](BacktestShariah2/standard/tugasan_v3.md#L80)
- Gred ialah penilaian calon/saham, bukan kaedah. Paparannya ialah panel "Prestasi ikut gred" (dilipat) — [dashboard.md:12](BacktestShariah2/standard/dashboard.md#L12)

**(h) Grid prestasi harian setiap kaedah lawan SPY (Prestasi, v92)**
- Baris = kaedah, lajur = hari; terkumpul lawan SPY, ✓/✕ dan "Selesai/20" — [dashboard.md:12](BacktestShariah2/standard/dashboard.md#L12); db `prestasi/harian_kaedah` [dashboard.md:45](BacktestShariah2/standard/dashboard.md#L45)

**Percanggahan nyata bagi kaedah yang sama (keadaan 20–21 Okt)**

| Kaedah | Skor swing v2 (C) | Penganalisis (Lejar), # / 75 swing, skor sebulan | Label §7 (C, anggaran) | Status backtest |
|---|---|---|---|---|
| M70 | 84%, beku #1, TOP1_10 | #35, +0.43% (jangkaan +0.21%/dagangan) | PERHATI (66 posisi, 29 tutup, purata +3.07%) | SIMPAN |
| M03 | 76%, beku | #40, +0.39% | PERHATI (85 posisi, 56 tutup) | **DITOLAK** |
| M18 | 74%, beku | #53, +0.29% | PERHATI | UJI KERTAS |
| M21 | tidak layak (1 posisi C) | **#1**, +3.40% | BELUM | **DITOLAK** |
| M140 | tidak layak | #2, +2.25% | BELUM (1 posisi, −7.20%) | DITOLAK |
| M32 | tidak layak | #4, +1.69% | BELUM (24 posisi, 6 tutup) | UJI KERTAS |
| M96 / M30 / M79 | di luar pintu swing | tiada kedudukan (bukan swing) | – | **GUNA** |

Sumber jadual: [gabungan_beku.json](BacktestShariah2/data/analisis/gabungan_beku.json); [papan.json](BacktestShariah2/data/analisis/papan.json) (`kedudukan`, `skor_bulan`, `jangkaan`, `bt_keputusan`); kiraan §7 sendiri atas `papertrade/claude*.csv`.

**Lima takrif "cukup data"**
- §7: ≥ 20 dagangan **tertutup** — [tugasan_v3.md:76](BacktestShariah2/standard/tugasan_v3.md#L76)
- Gred: ≥ 20 tertutup setiap gred — [tugasan_v3.md:90](BacktestShariah2/standard/tugasan_v3.md#L90)
- Penganalisis: ≥ 20 **matang** dan ≥ 10 hari beli — [penganalisis.py:61-77](BacktestShariah2/standard/penganalisis.py#L61)
- Skor v2: ≥ 20 selesai ATAU matang dan ≥ 10 hari beli; Teras ≥ 20 hari beli — [dashboard.md:3](BacktestShariah2/standard/dashboard.md#L3)
- Pantau BERSARA: ≥ 20 hari beli matang — [penganalisis.py:72](BacktestShariah2/standard/penganalisis.py#L72)
- Portfolio: 6–12 bulan — [portfolio_slot/RINGKASAN.md:42](BacktestShariah2/portfolio_slot/RINGKASAN.md#L42)

### Inferences
- Percanggahan utama berpunca daripada tiga perkara. **Asas** berbeza: C dengan semua posisi awal, lawan Lejar matang sahaja. **Pemberat bukti hadapan** berbeza: skor v2 membenarkan C yang belum matang menguasai, manakala Penganalisis hampir 100% backtest dipotong apabila 0 matang. **Penapis backtest** berbeza: Penganalisis dan skor v2 tidak memakai status DITOLAK, jadi kaedah DITOLAK boleh menduduki #1.
- Kaedah gabungan beku (M70/M03/M18) mempunyai purata C tinggi, tetapi jangkaan backtest dipotongnya antara yang terendah (+0.10% hingga +0.21% setiap dagangan) dan tiada satu pun semakan luar sampel lulus (`lulus` = 0). Pilihan itu bersandar hampir sepenuhnya pada 10 hari beli C semasa musim earnings Oktober. Laporan KPI sendiri menyatakan susunan seperti ini "belum dapat dibezakan daripada nasib dan regim pasaran dua minggu" ([Skor KPI…md:3](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L3)).
- Label §7 dan "Terbaik ikut % untung" menyebelahi kaedah yang keluar cepat, kerana ambang "20 tertutup" dicapai dahulu oleh kaedah yang cepat kena henti. Kedua-duanya mengukur perkara yang bertindih dengan skor v2 (purata, kadar menang, terburuk).
- Paparan dashboard v101–v102 (lajur dan pil Pantau, tahap Gantung/Bersara) kini tidak dapat diisi, kerana `papan.json` dalam repo belum mempunyai medan `pantau` (kemungkinan selesai selepas larian `analisis.yml` seterusnya).

### Gaps
- Nilai sebenar skor v2 setiap kaedah pada hari ini (dikira dalam pelayar daripada db) tidak dapat dibaca kerana arahan melarang ArtifactData. Hanya nilai yang dibekukan dalam `gabungan_beku.json` disahkan.
- Label §7 sebenar memerlukan `prestasi/mae`. Kiraan di atas ialah anggaran (MAE ≈ min(untung, 0)).
- Butiran 7 langkah saringan dan pingat tab Backtest tidak diaudit baris demi baris (penyelidik lain mengaudit UI).

## S2. Ranking utama yang paling boleh dipertahankan, dan yang patut jadi sekunder, diagnostik atau dibersarakan

### Takeaway
Ranking utama yang paling boleh dipertahankan secara statistik ialah skor sebulan Papan Penganalisis atas Lejar Penuh. Ia memakai posisi matang sahaja, n berkesan ikut hari beli, dan pengecutan ke jangkaan backtest khusus setiap kaedah. Statusnya (KUAT/BELUM CUKUP) dan Pantau berfungsi sebagai pintu. Skor swing v2 patut menjadi alat diagnostik/MC kepada papan yang sama, bukan ranking kedua yang berasingan. Label §7 U×S dan "Terbaik ikut % untung" patut dibersarakan sebagai alat pemilihan. Kajian projek sendiri juga menunjukkan bahawa pada peringkat portfolio, cara memilih saham (RS + Chandelier) menambah lebih banyak nilai daripada memilih kaedah. Oleh itu, keputusan wang sebenar akhirnya patut bergantung pada keluk ekuiti portfolio beku hadapan lawan kawalan, bukan pada pangkat kaedah.

### Cited Findings
- Laporan KPI: "Pembaikan paling murah juga yang paling besar kesannya, iaitu menyatukan dua papan… berkongsi satu prior, satu takrif matang dan satu n berkesan" — [Skor KPI…md:93](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L93)
- Laporan KPI: skor swing (v97) mengecut ke min global dengan n mentah (36 dagangan = 64% wajaran). Papan Penganalisis mengecut ke jangkaan khusus kaedah dengan n0 ≈ 30 dan n berkesan (10 hari beli = 25%). Pada 20 Okt, 0 posisi matang, jadi "sebarang susunan hadapan sekarang sebenarnya susunan backtest yang dipotong" — [Skor KPI…md:42](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L42)
- Kesan reka bentuk berkelompok (DEFF): dengan G = 10 hari beli, nilai kritikal patut 2.262 dan bukan 1.96. Ambang "≥ 20 dagangan" hanya ambang paparan, bukan ambang kebolehpercayaan — [Skor KPI…md:38-40](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L38)
- Kaedah teratas daripada 123 dijangka mencapai t ≈ 2.6 melalui nasib. Memilih lorong terbaik selepas melihat data juga satu pemilihan; lorong patut dipra-komit — [Skor KPI…md:46](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L46)
- Pemalar "25% + 25% bagi setiap semakan lulus" memberi median pengekalan ±26% (median backtest 2.47% → jangkaan 0.65%). Laporan mencadangkan potongan Harvey–Liu yang khusus bagi setiap kaedah (item 16) — [Skor KPI…md:44](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L44), [Skor KPI…md:136](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L136)
- Protokol yang disyorkan: guna skor sekarang untuk menyingkir kaedah lemah dan membina senarai pendek 15–20. Tahan "Teras" sehingga ≥ 20 hari beli matang (paling awal akhir Nov 2026). Bekukan, kemudian nilai semula selepas ±6 bulan dengan 40–60 hari beli (sekitar Mei–Jun 2027) — [Skor KPI…md:3](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L3), [Skor KPI…md:81](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L81)
- Ujian paling penting ialah sama ada skor itu meramal (Spearman mingguan). Jangan tala wajaran sebelum 8–12 minggu — [Skor KPI…md:83](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L83), [Skor KPI…md:134](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L134)
- AMARAN t < −2 atas 123 kaedah memberi ±2.8 amaran palsu setiap semakan. Brek bertulis (gantung/bersara) lebih sesuai — [Skor KPI…md:85](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L85)
- Kaedah #1 daripada 123 paling terdedah kepada kutukan pemenang. Gabungan 3–4 kaedah sama berat daripada kelompok berbeza lebih mungkin mampan — [Skor KPI…md:93](reports/Skor%20KPI%20pemilihan%20kaedah%20swing.md#L93)
- Kajian portfolio 10 slot (backtest): isyarat rawak (23.8–24.5% CAGR) tidak mengatasi EW 423 saham (26.3%). "Pada peringkat portfolio 10 slot, isyarat kaedah sendiri tidak menambah nilai. Nilai hanya datang daripada cara memilih." Kaedah statik dengan pandang hadapan hanya 33–40%, dan kaedah walk-forward tidak stabil (persentil H1 3 lawan H2 97) — [KAJIAN_PORTFOLIO.md:34-51](BacktestShariah2/kajian/KAJIAN_PORTFOLIO.md#L34)
- RS + keluar L2 (Chandelier) ialah satu-satunya gabungan yang kekal jelas di atas rawak selepas 40 pemenang dibuang (30.7% lawan rawak 17.6% dan sama rata 16.4%) — [KAJIAN_PORTFOLIO.md:79-83](BacktestShariah2/kajian/KAJIAN_PORTFOLIO.md#L79)
- Lorong 2 Chandelier 4×ATR14 dipilih atas 30+ calon. Lebihannya tertumpu pada tahun trend kuat (2020, 2025); tanpa kedua-dua tahun itu, ia sedikit di bawah SPY — [KAJIAN_LORONG2.md:3](BacktestShariah2/kajian/KAJIAN_LORONG2.md#L3), [KAJIAN_LORONG2.md:41](BacktestShariah2/kajian/KAJIAN_LORONG2.md#L41)
- Bias kluster dan ekor: 59% posisi Lejar berada dalam kluster ≥ 5 kaedah, dan 62% dibeli pada satu hari. 37% belian berlaku ≤ 10 hari sebelum earnings — [KAJIAN_DATA_TERCEMAR.md:51-53](BacktestShariah2/kajian/KAJIAN_DATA_TERCEMAR.md#L51)

### Inferences
- **Utama (satu jadual "Kaedah"):** skor sebulan Penganalisis (Lejar, matang, n berkesan, pengecutan ke jangkaan). Status KUAT/LEMAH/BELUM CUKUP dan Pantau BERSARA/GANTUNG/AMARAN/OK dipapar sebagai pintu dan lencana. Alasannya: asas adil (semua isyarat), tiada bias keluar awal, julat jujur, dan selari dengan cadangan laporan KPI. Dua pembaikan patut diambil dahulu daripada laporan: potongan khusus kaedah (item 16), dan penanda yang jelas bahawa kaedah DITOLAK dalam backtest muncul dalam ranking.
- **Diagnostik (dilipat di bawah jadual utama):** sub-skor v2 (CVaR, MAE/ATR, PF, Wilson hari beli), P(4 teratas) MC, korelasi/pertindihan pasangan dan ujian ramalan Spearman. Skor v2 patut dikira atas Lejar matang dan lorong yang dipra-komit, bukan C "awal" dengan lorong terbaik.
- **Bersarakan sebagai alat pemilihan:** label §7 TERUSKAN/PERHATI/HENTIKAN (U×S, asas semua, n/5), "Terbaik ikut % untung" dan podium backtest di Ringkasan. Kekalkannya di tab Backtest/Prestasi sebagai sejarah sahaja. Label §7 adalah keputusan pengguna (14 Okt) dalam tugasan_v3, jadi persaraannya perlu kelulusan pengguna.
- **Keputusan wang sebenar:** kajian portfolio menunjukkan nilai datang daripada cara memilih saham dalam portfolio terhad, bukan daripada kaedah. Jadi soalan "layak wang sebenar" paling tepat dijawab oleh keluk ekuiti hadapan portfolio beku (GABUNGAN_10, TOP1_10, RS_10) lawan kawalannya (RAWAK_KAEDAH_10, RAWAK_10), EW dan SPY. Ia dinilai selepas 6–12 bulan, manakala ranking kaedah hanya memilih calon.
- Gabungan beku semasa wajar dilabel jelas sebagai "SEMENTARA — dipilih atas data C belum matang; bercanggah dengan Penganalisis". Ini selaras dengan protokol laporan KPI, yang membekukan hanya pada ±akhir Nov 2026.

### Gaps
- Belum ada bukti hadapan bahawa mana-mana skor meramal: ujian Spearman memerlukan 8–12 minggu, dan `skwRamal` baru dipasang 22 Okt.
- Regresi "purata hadapan matang ke atas backtest" (μ₀ = a + b·backtest) yang disyorkan laporan KPI belum boleh dibuat (0 matang), jadi kekuatan prior sebenar tidak diketahui.

## S3. Jurang penjejakan matlamat (10% sebulan, kalahkan EW, kadar menang)

### Takeaway
Tiada panel yang mengukur kemajuan hadapan terhadap matlamat sebenar. Tiada pulangan bulanan hadapan lawan sasaran 10%, dan **EW semua saham Shariah tidak dijejak ke hadapan langsung**: EW hanya angka backtest, dan semua perbandingan hadapan memakai SPY. Sasaran 10% sebulan (≈ 214% setahun) juga jauh melebihi CAGR backtest tertinggi set 431 (58.2% ≈ 3.9% sebulan) dan skor sebulan Penganalisis tertinggi (+3.40%).

### Cited Findings
- EW muncul dalam kod hanya sebagai rujukan backtest: `is_ew` (EW 431 21.9% setahun) dan `wfo_ew` (EW 423 32.6%) dalam `rujukan()`, serta semakan "atasi EW" S1–S4/WFO — [penganalisis.py:146-176](BacktestShariah2/standard/penganalisis.py#L146), [penganalisis.py:572-577](BacktestShariah2/standard/penganalisis.py#L572); dipapar di [dashboard_v2.html:3110-3111](BacktestShariah2/standard/dashboard_v2.html#L3110); [PENGANALISIS.md:21-22](BacktestShariah2/laporan/PENGANALISIS.md#L21)
- Carian `EW` dalam `standard/*.py` dan `kod/*.py` tidak menemui sebarang pengiraan EW hadapan. Penanda aras hadapan yang wujud ialah SPY (`spy_pct` portfolio_slot, "lebih SPY", grid lawan SPY), serta "penanda aras dalaman" u3 = purata semua posisi semua kaedah yang dibeli pada hari sama — semakan grep sendiri; [dashboard_v2.html:2615-2618](BacktestShariah2/standard/dashboard_v2.html#L2615); [dashboard.md:40](BacktestShariah2/standard/dashboard.md#L40)
- Universe stor harga sudah merangkumi set 431 (+ semua saham papertrade + `univ.txt` + SPY/QQQ), jadi bahan untuk mengira EW 431 hadapan sudah ada — [tugasan_v3.md:67-68](BacktestShariah2/standard/tugasan_v3.md#L67)
- Kajian portfolio memakai EW 423 saham (26.3% CAGR) sebagai garis yang tidak diatasi oleh isyarat rawak — [KAJIAN_PORTFOLIO.md:49-50](BacktestShariah2/kajian/KAJIAN_PORTFOLIO.md#L49)
- Set 431 dalam registry: 633 varian; CAGR maks 58.15%, p90 34.3%; EW 21.9%. Median `bulan10` (% bulan portfolio naik ≥ 10%) = 10.8%, maks 36.1%. 27.6% varian `menang_ew` — kiraan sendiri atas [registry_M_gabung.csv](BacktestShariah2/data/registry_M_gabung.csv); 1.10¹² − 1 = 213.8% (aritmetik)
- Metrik matlamat backtest wujud dalam tab Backtest ("Tutup ≥ +10%", "Sentuh +10%", "Bulan ≥ +10%", "Atasi beli semua") — [dashboard_v2.html:934](BacktestShariah2/standard/dashboard_v2.html#L934), [dashboard_v2.html:991](BacktestShariah2/standard/dashboard_v2.html#L991). Tiada padanan hadapannya.
- Skor sebulan Penganalisis = untung setiap posisi jika modal dipusing semula sebaik keluar (skor ÷ hari × 21). Ia proksi paling hampir kepada "% sebulan", tetapi pada peringkat posisi, bukan portfolio — [PENGANALISIS.md:15](BacktestShariah2/laporan/PENGANALISIS.md#L15)
- Portfolio maya ialah satu-satunya pulangan hadapan peringkat portfolio. Ia memapar pulangan %, MDD dan kadar menang lawan SPY, bukan EW atau sasaran bulanan — [portfolio_slot/RINGKASAN.md:5-10](BacktestShariah2/portfolio_slot/RINGKASAN.md#L5); bentuk db `prestasi/portfolio_slot` [dashboard.md:40](BacktestShariah2/standard/dashboard.md#L40)
- Kadar menang hadapan dipapar dengan pelbagai asas, (semua) lawan (selesai), dan label memakai (semua) — [dashboard.md:32](BacktestShariah2/standard/dashboard.md#L32). Penganalisis melapor `h_menang` matang — [papan.json](BacktestShariah2/data/analisis/papan.json)
- Saiz portfolio berbeza antara dokumen: matlamat 8 slot × 12.5% ([00_NOTA_SERAHAN.md:9](BacktestShariah2/00_NOTA_SERAHAN.md#L9)), jejak hadapan 10 slot ([portfolio_slot.py:36](BacktestShariah2/standard/portfolio_slot.py#L36)), dan metrik Prestasi menganggap USD1,000 setiap posisi tanpa had ([tugasan_v3.md:77](BacktestShariah2/standard/tugasan_v3.md#L77))

### Inferences
- Panel "Matlamat" yang hilang patut memapar, bagi setiap portfolio beku dan bagi kaedah utama: (1) pulangan bulanan hadapan lawan garis 10%; (2) lebihan atas **EW 431 hadapan** (indeks sama berat stor yang sama, tempoh sama), dengan SPY sebagai rujukan sekunder; (3) kadar menang matang dengan selang Wilson; (4) bulan berlalu lawan 6–12 bulan yang diperlukan.
- Dashboard patut jujur bahawa sasaran 10% sebulan tidak dicapai oleh mana-mana kaedah walaupun dalam backtest dalam sampel. Unjuran yang paling mungkin ialah 1–4% sebulan setiap posisi. Ini keputusan matlamat untuk pengguna, bukan isu paparan.
- Takrif "berjaya" dalam matlamat (kalahkan EW) patut menjadi syarat label utama, contohnya "KUAT lawan EW" = julat 95% lebihan atas EW hadapan > 0, bukan julat purata mutlak > 0 (status KUAT Penganalisis kini membandingkan dengan 0, bukan EW).

### Gaps
- Tiada data EW Shariah hadapan untuk dilapor, kerana ia tidak dikira. Sama ada stor `harga_A/B` lengkap bagi semua 431 saham setiap sesi tidak disemak.
- "Semua saham Shariah" dalam matlamat (screener Moomoo, beribu saham) tidak sama dengan EW 431/423 backtest. Universe EW yang tepat perlu keputusan pengguna.

## S4. Kekeliruan asas data: Papertrade C, Lejar Penuh, Moomoo lama, bayang/

### Takeaway
Empat asas wujud serentak. Papertrade C (rasmi untuk belian maya, harga Moomoo, dipapar di Posisi/Prestasi/skor v2). Lejar Penuh (semua isyarat, tanpa LLM, asas Penganalisis dan portfolio_slot). Moomoo lama (harga sahaja). `bayang/` (Actions mod selari; `MOD_ACTIONS` masih `bayang`). Penilaian kaedah patut lalai kepada Lejar Penuh (matang). "Posisi saya" patut lalai kepada portfolio maya beku 10 slot, atau C dengan label yang jelas. Moomoo lama dan bayang tidak patut berada dalam aliran keputusan.

### Cited Findings
- C SAHAJA untuk belian baharu sejak 13 Okt 2026; tiada order Moomoo — [tugasan_v3.md:6-7](BacktestShariah2/standard/tugasan_v3.md#L6). Posisi Moomoo lama hanya dikemas kini harganya — [tugasan_v3.md:9](BacktestShariah2/standard/tugasan_v3.md#L9)
- Belian C: semua baris senarai_beli (tiada had slot) — [tugasan_v3.md:41](BacktestShariah2/standard/tugasan_v3.md#L41). Namun BANDING_C menulis "had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat)" — [lejar/BANDING_C.md](BacktestShariah2/lejar/BANDING_C.md) (baris pengenalan; tidak diselaraskan dengan §4)
- Lejar: SEMUA isyarat setiap kaedah dibeli pada buka rasmi esok, tanpa had dan tanpa keutamaan 431. Harga stor yfinance. Dijalankan `lejar.yml` tanpa LLM — [tugasan_v3.md:92-95](BacktestShariah2/standard/tugasan_v3.md#L92)
- Saiz relatif: posisi C (isyarat ≥ 15 Okt) 2,577 lawan Lejar 5,789 (2.2×). Harga beli berbeza > 0.5%: 52 daripada 1,767 pasangan. Status keluar sama: 1,764/1,767 — [lejar/BANDING_C.md](BacktestShariah2/lejar/BANDING_C.md)
- RCA R1: buka yfinance muktamad = buka rasmi Moomoo bagi 1,363/1,365 pasangan saham-hari 13–21 Okt, jadi "beza vendor" bukan punca sebenar — [KAJIAN_DATA_TERCEMAR.md:47](BacktestShariah2/kajian/KAJIAN_DATA_TERCEMAR.md#L47)
- Lejar "data awal didominasi posisi yang tutup cepat (kebanyakan kena henti); nilai hanya selepas posisi matang… penilaian 15 Jan 2027" — [lejar/RINGKASAN.md:3-5](BacktestShariah2/lejar/RINGKASAN.md#L3)
- Penganalisis: bukti hadapan = Lejar + kohort C pra-Lejar (1,669 posisi; 297 posisi Lejar bertindih dibuang). C selepas Lejar = lajur semakan sahaja — [PENGANALISIS.md:14](BacktestShariah2/laporan/PENGANALISIS.md#L14)
- Skor swing v2 dan gabungan beku memakai akaun Papertrade C — [gabungan_beku.json](BacktestShariah2/data/analisis/gabungan_beku.json) (`formula.akaun`)
- `MOD_ACTIONS` = `bayang`: Actions menulis ke `bayang/` sahaja, manakala rutin Claude kekal rasmi. `rasmi` memindahkan penulisan ke `papertrade/` — [tugasan_v3.md:105-107](BacktestShariah2/standard/tugasan_v3.md#L105); fail [MOD_ACTIONS](BacktestShariah2/MOD_ACTIONS)
- Mod selari dirancang 3 hari dagangan sejak 17 Okt — [tugasan_v3.md:97](BacktestShariah2/standard/tugasan_v3.md#L97). Pada 22 Okt mod masih `bayang`, dan BANDING harian 16, 17, 19, 20 dan 21 Okt sudah wujud — [bayang/](BacktestShariah2/bayang/)
- Banding 21 Okt (sesi 20 Okt): harga_beli_sama 3,749/3,750, keluar_sama 3,676/3,750. 74 beza keluar berpunca daripada Actions menutup posisi ambil alih (RAMP, ATKR), sedangkan rutin Claude masih "Pegang" — [bayang/BANDING_2026-10-21.md](BacktestShariah2/bayang/BANDING_2026-10-21.md)
- Dashboard: Prestasi dan Posisi mempunyai butang akaun Papertrade C · Moomoo lama · Gabung — [dashboard.md:12-13](BacktestShariah2/standard/dashboard.md#L12)

### Inferences
- **Penilaian kaedah (S1/S2) → Lejar Penuh matang.** Ia adil (tiada had/keutamaan), lengkap, boleh dihasilkan semula tanpa LLM, dan sama dengan enjin. Asas inilah yang dipakai Penganalisis dan portfolio_slot. C ialah subset (±45%) dengan peraturan pemilihan yang berubah-ubah (dedup, belian semula, `tidak_sah`), jadi purata C per kaedah bukan anggaran adil kaedah itu.
- **Posisi saya (S6) → portfolio maya beku 10 slot** (GABUNGAN_10 atau yang dipilih). Ia satu-satunya objek yang menyerupai portfolio wang sebenar (10 posisi, saiz, tunai). C dengan ±4,000 posisi dalam 10 hari bukan portfolio yang boleh dipegang manusia. Jika C kekal dipapar, labelkan "papertrade semua isyarat (C)".
- **Moomoo lama:** pindahkan ke arkib; butang "Gabung" mencampur asas yang tidak setanding.
- **bayang/:** status peralihan, bukan data keputusan. Paparkannya hanya sebagai satu titik kesihatan ("Actions selari: n% padanan").
- Satu nyatakan mod di pengepala dashboard (Rasmi: rutin Claude / Actions) akan mengelakkan kekeliruan tentang sumber mana yang sedang ditulis.

### Gaps
- Sama ada C masih dihad 10 setiap kaedah selepas 16 Okt tidak dapat disahkan: §4 dan BANDING_C bercanggah, dan kod `harian_c.py`/`scanner.py` tidak dibaca untuk perkara ini.
- Bila `MOD_ACTIONS` akan ditukar ke `rasmi` (keputusan pengguna) tidak dinyatakan dalam fail yang dibaca selain `jadual/PERALIHAN.md` (tidak dibaca).

## S5. Kesihatan sistem: semua isyarat OK/rosak, dan set minimum bagi "lampu status"

### Takeaway
Isyarat kesihatan tersebar dalam sekurang-kurangnya 10 tempat. Dashboard kini hanya meringkaskan **kesegaran** 8 saluran (butang "Data n/8"). Ia tidak melihat ralat larian, CI `semak_data.yml`, ketekalan C/Lejar/bayang, output basi berbanding versi kod, atau lapisan yang dilangkau senyap (EDGAR tanpa rahsia). Contoh semasa: Lejar dan Penganalisis masih pada sesi 20 Okt, sedangkan stor harga sudah sesi 21 Okt, dan `papan.json` tidak mempunyai medan `pantau` yang dijangka dashboard v102.

### Cited Findings
- `saluran()` dashboard: 8 saluran (Harga & posisi, Belian 9:35 NY, Watchlist, Harga tinggi/rendah, Lejar Penuh, Penganalisis, Portfolio 10 slot, Sektor mingguan). Statusnya ok / lewat 1 sesi / basi / tiada, ikut tarikh data lawan sesi yang dijangka. Pengepala menunjuk keadaan terburuk — [dashboard_v2.html:2300-2311](BacktestShariah2/standard/dashboard_v2.html#L2300)
- `harian/status` (db): `harga_tutup_pada`, `kemaskini_pagi`, `scan_malam`, `beli_pada`, `beli_ringkas{direkod, dilangkau}`, `gred_pada` dan `ralat` (≤ 20 ralat kaedah) — [jana_db.py:510-520](BacktestShariah2/standard/jana_db.py#L510)
- `pengawas()`: mengesan `harian.yml` atau `beli.yml` yang sepatutnya sudah siap, untuk dicetus oleh sesi tolak db — [jana_db.py:349-367](BacktestShariah2/standard/jana_db.py#L349)
- `penjaga_jadual.py`: mencetus workflow_dispatch jika cetusan cron hilang atau lewat > 30 minit, dalam had masa (buka < 13:00 UTC; petang < 9:15 NY; beli < 16:45 NY). JAGA = 9 workflow (harga_harian, skrin_tv, rs_pasaran, gred_kumpulan, lejar, harian, petang, beli, edgar) — [penjaga_jadual.py:1-12](BacktestShariah2/standard/penjaga_jadual.py#L1), [penjaga_jadual.py:21-25](BacktestShariah2/standard/penjaga_jadual.py#L21). Ia dicetus dari luar oleh tugasan berjadual Claude — [CLAUDE.md](CLAUDE.md) (perenggan Automasi)
- Pencetus workflow: harga_harian 21:37/00:23 UTC; harian 05:07 (+3 sandaran); beli 13:40/14:40/16:25/19:25 UTC; lejar 06:17/10:17 UTC; analisis = `workflow_run` selepas "Lejar penuh"; semak_data = push; penjaga = :23/:53 setiap jam + workflow_run — fail [.github/workflows/](.github/workflows/) (grep `cron`/`workflow_run`)
- `sahkan.py`: kod keluar 0 = lulus, 1 = RALAT (jangan push data), 2 = fail tiada — [sahkan.py:1-4](BacktestShariah2/standard/sahkan.py#L1); wajib sebelum push — [tugasan_v3.md:59](BacktestShariah2/standard/tugasan_v3.md#L59). `semak_data.yml` menjalankan ujian unit + `sahkan.py` pada setiap push — [CLAUDE.md](CLAUDE.md) (Automasi)
- `data/harga/status.json`: `terkini.sesi` 20261021 (dijana 22 Okt 06:22 UTC), `tiada_data` [], `tiada_bar_sesi` 4 (ATKR, BLFS, QRVO, WLYB), `dividen_baharu` 1 — [data/harga/status.json](BacktestShariah2/data/harga/status.json)
- `lejar/status.json`: `sesi_terakhir` 2026-10-20, `kemaskini` 21 Okt 16:54 MYT, dan `larian[]` dengan `ralat` serta `nota` setiap sesi — [lejar/status.json](BacktestShariah2/lejar/status.json). Lejar ditangguh jika data yfinance belum muktamad — [tugasan_v3.md:94](BacktestShariah2/standard/tugasan_v3.md#L94)
- `papan.json`: `dibina` 21 Okt 23:15 MYT, `kini` 20 Okt; tiada medan `pantau` — [papan.json](BacktestShariah2/data/analisis/papan.json). Kod pantau ditambah dalam commit `326493c` (22 Okt) — log git
- `portfolio_slot/status.json`: `sesi_terakhir` 2026-10-20 (RS_10, RAWAK_10 sahaja) — [portfolio_slot/status.json](BacktestShariah2/portfolio_slot/status.json)
- EDGAR: commit "EDGAR: langkau tanpa ralat sehingga rahsia SEC_USER_AGENT ditetapkan (SEC 403 tanpa e-mel hubungan)", 22 Okt — log git; rahsia diperlukan — [CLAUDE.md](CLAUDE.md) (Saham tidak layak)
- Ketekalan: bayang (padanan keluar 3,676/3,750) — [bayang/BANDING_2026-10-21.md](BacktestShariah2/bayang/BANDING_2026-10-21.md); C lawan Lejar (harga beli beza > 0.5%: 52/1,767) — [lejar/BANDING_C.md](BacktestShariah2/lejar/BANDING_C.md)
- RCA mencatat kegagalan yang tidak kelihatan pada lampu kesegaran: R3 (CI merah apabila posisi delist pertama ditutup → lejar.yml/analisis tergendala) dan R4 (89 posisi palsu kembali "Pegang") — [KAJIAN_DATA_TERCEMAR.md:49-50](BacktestShariah2/kajian/KAJIAN_DATA_TERCEMAR.md#L49)
- Log teks: `standard/binaan_v2_log.md` (imbasan) dan `binaan_v2_log_tambahan.md` (kemas kini dan belian) — [tugasan_v3.md:66](BacktestShariah2/standard/tugasan_v3.md#L66)

### Inferences
Lampu status minimum (hijau/kuning/merah = terburuk antara 7 semakan; ketik untuk butiran):
1. **Harga segar:** `data/harga/status.json terkini.sesi` = sesi NYSE terakhir; `tiada_data` kosong; `tiada_bar_sesi` ≤ ambang (cth. 1%).
2. **Kerja harian C:** `harian/status.harga_tutup_pada` = sesi dijangka, `ralat` kosong; `beli_pada` = hari ini selepas 9:45 NY pada hari dagangan.
3. **Lejar → Penganalisis → portfolio_slot berantai:** ketiga-tiga `sesi_terakhir`/`kini` sama dengan sesi harga, dan `larian[-1].ralat` kosong.
4. **Integriti:** larian terakhir `semak_data.yml` hijau pada commit terakhir `main` (ujian unit + `sahkan.py` = 0). Lampu ini memerlukan sumber baharu, contohnya fail status yang ditulis CI atau `penjaga_jadual` yang merekod kesimpulan larian.
5. **Ketekalan:** padanan bayang ≥ 99% (atau, selepas `rasmi`, C lawan Lejar: keluar sama ≥ 99%, harga beli beza > 0.5% ≤ 5%).
6. **Skema/versi output:** output mempunyai medan yang dijangka versi dashboard (cth. `pantau` dalam `papan.json`), supaya data lama dikesan walaupun tarikhnya kelihatan segar.
7. **Lapisan dilangkau senyap:** EDGAR (rahsia), stor laras `anomali`, `faktor_calon.csv` belum disahkan. Paparkan sebagai kuning, bukan senyap.
- `saluran()` sedia ada sudah meliputi semakan 1–3 secara separa (kesegaran sahaja). Semakan 4–7 tiada.

### Gaps
- Status larian GitHub Actions sebenar (berjaya/gagal) tidak dapat dibaca secara tempatan. Alat GitHub tidak dipakai kerana kekangan baca-sahaja, dan pelayan MCP GitHub gagal bersambung. Sama ada Lejar 21 Okt gagal atau hanya menunggu sandaran 10:17 UTC tidak dapat disahkan.
- Kandungan sebenar db `harian/status` hari ini tidak dibaca (ArtifactData dilarang).

## S6. Hari ini/esok dan posisi: data yang wujud dan tempat ia dikira

### Takeaway
Data untuk "apa berlaku esok" sudah dikira, tetapi tersebar. Panel Esok di Ringkasan menggabung jualan pada buka esok (lorong kaedah dan lorong 2), belian menunggu, posisi hampir paras keluar, dan earnings ≤ 5 hari. Semuanya dikira di pelayar daripada lajur `claude*.csv` yang ditulis `harian_c.py` dan `keluar_lorong.py`. Belian esok diambil daripada watchlist "isyarat lengkap", bukan `senarai_beli` (tidak ditolak ke db sejak 19 Okt). Semuanya berasas C, bukan portfolio beku.

### Cited Findings
- `panelEsok()`: (1) **jual** = posisi C dengan `isyarat_keluar` atau `status_henti` mengandungi "menunggu" → jual pada buka sesi seterusnya (lorong kaedah dan/atau lorong selagi naik); (2) **beli** = baris watchlist lengkap dengan status belian "tunggu"; (3) **hampir** = statusPos 'h'; (4) **earnings ≤ 5 hari** (`hariKeEarn`, tidak termasuk `tutup_semua`). Satu cip setiap saham — [dashboard_v2.html:2318-2330](BacktestShariah2/standard/dashboard_v2.html#L2318)
- `statusPos()`: 'k' = kedua-dua lorong tutup; 'm' = jual esok; 'h' = hampir paras keluar jika lorong 2 berada < 25% julat di atas paras (`l2Info`: paras = puncak − 4×ATR14 daripada teks `status_henti`) atau henti kaedah < 2% di bawah harga; 'j' = selamat — [dashboard_v2.html:2237-2249](BacktestShariah2/standard/dashboard_v2.html#L2237)
- `hariKeEarn` mengira hari dagangan ke `tarikh_earnings` dari tarikh data — [dashboard_v2.html:2251](BacktestShariah2/standard/dashboard_v2.html#L2251)
- Panel "Berubah sejak sesi lalu" (`panelBerubah`) — [dashboard_v2.html:2335](BacktestShariah2/standard/dashboard_v2.html#L2335); dihuraikan dalam versi 89 — [dashboard.md:3](BacktestShariah2/standard/dashboard.md#L3)
- Lorong 1: henti dari hari masuk, sasaran dari hari selepasnya, isyarat keluar → jual buka esok, had masa → tutup (`harian_nilai_keluar.py keluar()`; kaedah replika ikut `dagangan.py`). Lorong 2: tutup < tutup tertinggi − 4×ATR14 → jual buka esok (`keluar_lorong.py`) — [tugasan_v3.md:49-57](BacktestShariah2/standard/tugasan_v3.md#L49)
- Kemas kini posisi dan imbasan tanpa LLM: `harian_c.py` (`kemas`, `imbas`, `cmd_malam`, `cmd_gred`) melalui `harian.yml`/`beli.yml`/`petang.yml` — [harian_c.py](BacktestShariah2/standard/harian_c.py) (fungsi `kemas` baris 424, `imbas` 541); [tugasan_v3.md:98-102](BacktestShariah2/standard/tugasan_v3.md#L98)
- QR = hari dagangan ke laporan suku seterusnya (SST `market_events`, kemudian kalendar Nasdaq `earnings_nasdaq.json`, kemudian anggaran +91 hari); dikira `gred.py` dan direkod pada setiap belian — [tugasan_v3.md:88](BacktestShariah2/standard/tugasan_v3.md#L88); lajur `sumber_earnings`, `gred_qr` dalam skema `harian_c.py` — [harian_c.py:57](BacktestShariah2/standard/harian_c.py#L57)
- Senarai beli: CSV sahaja sejak 19 Okt (halaman tidak membacanya); watchlist ditolak ke db — [dashboard.md:51](BacktestShariah2/standard/dashboard.md#L51). Panel watchlist "Isyarat lengkap" memapar status belian C (menunggu, dibeli, dilangkau, tidak dibeli) — [dashboard.md:14](BacktestShariah2/standard/dashboard.md#L14)
- Saham tidak layak (ambil alih, tidak cair, kelas berganda, delist) ditapis daripada senarai beli, watchlist dan Lejar. Posisi berkenaan ditutup oleh `tidak_layak.py posisi` — [CLAUDE.md](CLAUDE.md) (Saham tidak layak); [tugasan_v3.md:29-33](BacktestShariah2/standard/tugasan_v3.md#L29)
- Portfolio RS_10 menunjukkan posisi −36.65% (SVRN), tetapi tiada panel "posisi portfolio beku hampir keluar" — [portfolio_slot/RINGKASAN.md:25](BacktestShariah2/portfolio_slot/RINGKASAN.md#L25)

### Inferences
- Bagi soalan 10 saat (2) dan (3), panel Esok + statusPos sudah menjadi jawapan teras. Ia perlu ditukar ke **asas yang sama dengan keputusan**, iaitu posisi portfolio beku (10 slot), supaya "posisi saya OK?" bermaksud ≤ 10 baris dan bukan ribuan posisi C.
- "Belian esok" patut dibaca terus daripada sumber belian sebenar (`senarai_beli` atau keputusan kuota GABUNGAN_10), bukan diterbitkan daripada watchlist. Kini ia bergantung pada `wLengkap`/`wBeli`, yang boleh berbeza daripada senarai beli rasmi.
- Risiko earnings (QR/`tarikh_earnings`) dan amaran "hampir paras" sudah ada. Yang tiada ialah ringkasan risiko peringkat portfolio: kejatuhan ekuiti semasa lawan had GANTUNG (1.5× MDD backtest), tunai dan bilangan slot kosong.

### Gaps
- Logik `wLengkap`/`wBeli` (penentu "beli esok") tidak dibaca baris demi baris, jadi ketepatannya berbanding `senarai_beli.csv` tidak disahkan.
- Sama ada `tarikh_earnings` diisi bagi semua posisi C (liputan) tidak dikira.
