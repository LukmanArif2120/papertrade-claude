# Carian empirik takrif status Bullish/Bearish yang benar-benar berfungsi (trend5, 23 Okt 2026)

Kajian ini menyambung larian trend5 yang terhenti. Pradaftar asal dikekalkan, dan pindaan bertarikh ditambah di hujungnya (G, H). Set pemilihan ialah IS 2020–2022, manakala OOS 2023 – Okt 2026 dijalankan sekali sahaja selepas senarai dibekukan. Data terdiri daripada panel 431 saham Shariah (S1–S4, 1,949 tarikh, 2019-01-02 hingga 2026-10-02) dan 125,770 dagangan enjin v1.2 bagi 19 kaedah (54,350 IS, 71,420 OOS).

**Kesimpulan ringkas:** tiada takrif status (34 ciri, 3 model ML dan HMM) yang meramal pulangan atau arah halangan ±8% bagi senarai pantau. Tiada peraturan jual atau penapis masuk berasaskan status yang menambah nilai dalam kedua-dua tempoh. "Sambungan trend naik" kelihatan boleh diramal, tetapi kebolehramalan itu dihasilkan semula sepenuhnya oleh siri tanpa arah. Hanya dua maklumat lulus OOS, dan kedua-duanya maklumat **risiko/peristiwa**, bukan arah:

1. Status trend menambah 3–7 mata kepada kebarangkalian keluar lorong 2 dalam 10 sesi, melebihi jarak ke paras Chandelier.
2. Lonjakan 5 hari menambah 1–5 mata kepada risiko jatuh > 8% melebihi ATR%.

Kedua-duanya tidak memberi masa jual yang lebih baik.

Lokasi kerja ialah `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/`, iaitu scratchpad sesi yang mungkin tidak kekal. Dalam nota ini, laluan sumber ditulis penuh.

## 1. Apakah maksud "berfungsi", dan bagaimana kajian dijalankan dengan disiplin dan memori terhad?

### Takeaway
"Berfungsi" ditakrif sebelum ujian (pradaftar A). Sesuatu calon mesti memenuhi semua syarat berikut:
- |t| Newey-West ≥ 3 dan BH q ≤ 0.05 atas keluarga IS;
- tanda sama dalam dua sub-tempoh, dan mengatasi persentil ke-95 pilih atur ticker;
- mengatasi garis dasar jalan rawak (dan, selepas pindaan G, garis dasar terbalik tanda);
- saiz ekonomi minimum;
- dalam OOS: tanda sama, |t| ≥ 2 dan Holm ≤ 0.05 atas senarai beku;
- dalam dagangan: Δ purata log ≥ +0.30 mata (masuk) atau ≥ +0.20 mata (jual, selepas kos 10–20 bps), dengan kadar menang dan p5 tidak lebih buruk.

Larian terdahulu terhenti kerana beberapa skrip berat berjalan serentak, bukan kerana satu fail. Selepas reka bentuk semula, setiap langkah kekal di bawah 2 GB.

### Cited Findings
**Pradaftar dan pembekuan:**
- Pradaftar (A–F asal; G = garis dasar terbalik tanda, ditulis selepas IS dilihat dan hanya menyekat; H = log selepas pembekuan) — [00_prapendaftaran.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/00_prapendaftaran.md)
- Senarai beku ditulis sebelum OOS calon dikira: 7 panel, 18 posisi, 4 ML dan 22 pasangan ekonomi — [10_beku.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/10_beku.md); [beku.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/beku.py)

**Bilangan varian:**

| Kumpulan | Bilangan |
|---|---|
| Keluarga IS | **351** (panel 203 = 34 ciri × 6 sasaran − 1; posisi 134; ML 14) |
| Garis dasar | 200 pilih atur ticker × 203; 3 panel jalan rawak; 2 panel terbalik tanda |
| Diuji dalam OOS | 29 calon beku |
| Ujian ekonomi | 22 pasangan × 6 ujian × 2 tempoh = 264 |
| Tambahan (dikira) | semakan P2 tidak linear 15 × 2; kontras diskret v_j8 8 × 4; ML atas panel terbalik tanda (2 sasaran); portfolio 2 varian × 19 kaedah; jadual deskriptif |

**Ukuran ralat dan statistik:**
- Persentil ke-95 |t| di bawah pilih atur ticker ialah 1.71–3.95 (median 2.27). Ambang |t| = 3 bukan konservatif secara automatik — [perm_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/perm_IS.csv)
- SE: Newey-West dengan lag = ufuk (semakan lag 60) bagi panel; kluster bulan bagi posisi dan dagangan. White Reality Check dan Hansen SPA (bootstrap pegun, 1000 ulangan) dipakai setiap sasaran — [alat.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/alat.py); kaedah ujian mengikut [Sullivan, Timmermann & White 1999](https://www.fmg.ac.uk/publications/discussion-papers/data-snooping-technical-trading-rule-performance-and-bootstrap)

**Memori dan simpanan:**
- Empat pickle "lebar" (4 × 430 MB, float64) ditukar kepada direktori .npy float32 yang dimuat malas. Setiap muatan pickle hanya memuncak ≈ 0.5 GB, jadi punca kehabisan memori yang munasabah ialah beberapa skrip berat serentak (uji_posisi ≈ 1.5–2 GB setiap satu).

| Langkah | Puncak RSS |
|---|---|
| siri_panel | 0.15 GB |
| perm_panel | 0.15 GB |
| uji_posisi | 0.8–2.0 GB |
| ml | 0.64–0.79 GB |
| ekonomi | 0.45 GB |
| p2_kukuh | 1.2–1.6 GB |
| sedia (sintetik) | 1.7 GB, ≈ 16 s |

- Selepas siri IC disimpan, direktori sintetik dipadam. Saiz direktori kerja turun daripada 1.7 GB kepada 277 MB — [ubah_npy.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ubah_npy.py); [alat.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/alat.py); [siri_panel.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/siri_panel.py)

**Garis dasar sintetik:**
- **Jalan rawak (kocok tarikh):** susunan tarikh pulangan dikocok dengan pilih atur yang sama bagi semua saham. Ia mengekalkan drift setiap saham dan korelasi keratan rentas. Momentum boleh timbul semata-mata daripada beza purata pulangan antara saham ([Conrad & Kaul 1998](https://ideas.repec.org/a/oup/rfinst/v11y1998i3p489-519.html); dipertikai oleh [Jegadeesh & Titman 2002](https://ideas.repec.org/a/oup/rfinst/v15y2002i1p143-157.html)), jadi garis dasar ini mengawal kesan itu. Random walk juga menghasilkan "pasaran bull/bear" ([Pagan & Sossounov 2003](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.664)).
- **Terbalik tanda (pindaan G):** bar pada tarikh rawak dicerminkan dalam ruang log, dengan tanda yang sama bagi semua saham dan drift dikekalkan. Ia mengekalkan pengelompokan turun naik, julat dan volum, tetapi membuang arah dan kesan leverage — [sedia.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/sedia.py)

### Inferences
- Kerana pilih atur rawak sendiri mencapai |t| ≈ 4, dan model ML atas data tanpa arah mencapai IC t = 2.58 bagi pulangan 10 sesi (bahagian 5), mana-mana |t| 2–3 dalam data ini wajar dibaca sebagai hingar.
- Pindaan G ditulis selepas IS dilihat. Oleh itu kesimpulan dilapor di bawah **kedua-dua** kriteria. Keputusan akhir tidak bergantung pada G, kerana calon U10 juga gagal saiz ekonomi berbanding jalan rawak dalam OOS.

### Gaps
- Scratchpad tidak dijamin kekal, dan skrip serta output tidak disalin ke repo (larangan ubah repo).
- Hiperparameter ML tetap dan tidak ditala (hanya logistik dan LightGBM), jadi model yang lebih baik tidak dapat ditolak sepenuhnya; HMM hanya 2 keadaan atas pulangan harian.

## 2. Bagi senarai pantau: adakah mana-mana takrif meramal pulangan lebihan 5/10/21 sesi atau P(+8% sebelum −8%)?

### Takeaway
**Tidak.** Daripada 34 ciri, tiada satu pun mencapai |t| ≥ 3 dalam IS atau OOS bagi empat sasaran pulangan/halangan. Reality Check p ≥ 0.10. Korelasi t ciri antara IS dan OOS ialah −0.20 hingga +0.25, iaitu tiada kestabilan. Ini merangkumi keluarga yang disokong literatur: jarak MA pendek/panjang, MAD, faktor trend, 52 minggu, momentum residual, pembalikan relatif industri, FIP, volum dan GHM.

### Cited Findings
Panel IS/OOS (34 ciri; IC Spearman keratan rentas setiap tarikh; 725 tarikh IS, 936 tarikh OOS) — [stat_panel_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/stat_panel_IS.csv); [stat_panel_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/stat_panel_OOS.csv); [rc_panel_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/rc_panel_IS.csv); [rc_panel_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/rc_panel_OOS.csv)

| Sasaran | maks \|t\| IS (ciri) | RC p IS | maks \|t\| OOS (ciri) | RC p OOS | kor. t IS–OOS | lulus IS |
|---|---|---|---|---|---|---|
| x_f5 | 2.15 (HMM, −) | 0.29 | 2.63 (FIP, +) | 0.14 | +0.25 | 0 |
| x_f10 | 2.43 (HMM, −) | 0.18 | 2.21 (FIP, +) | 0.32 | −0.01 | 0 |
| x_f21 | 2.53 (HMM, −) | 0.15 | 1.85 (FIP, +) | 0.46 | −0.20 | 0 |
| B21 (±8%/21) | 2.56 (HMM, −) | 0.10 | 1.85 (RS industri, −) | 0.50 | −0.14 | 0 |

Ciri pilihan literatur bagi x_f10 (IC, t; Q5−Q1 dalam mata %):

| Ciri | IS | OOS |
|---|---|---|
| F09 MAD 21/200 | +0.021, t 0.95; +0.30 | +0.009, t 0.60; +0.27 |
| F12 faktor trend Han-Zhou-Zhu | −0.042, t −2.13; −1.32 | +0.005, t 0.41; +0.11 |
| F13 C/tinggi 52 minggu | +0.017, t 0.74; −0.36 | −0.003, t −0.18; −0.54 |
| F19 momentum residual | −0.001, t −0.08 | +0.002, t 0.16 |
| F20 r21 relatif kumpulan (pembalikan industri) | −0.005, t −0.64 | −0.002, t −0.39 |
| F21 r5 / F22 r21 (pembalikan) | t −0.32 / +0.46 | t −0.53 / +0.30 |
| F30 D10+H2 (status papan sekarang) | +0.020, t 1.16 | +0.011, t 0.85 |
| F34 HMM (P keadaan meruap) | −0.027, t −2.43 | +0.013, t 1.33 (tanda terbalik) |

**Ujian dagangan (penapis masuk):** penapis masuk dinilai pada hari isyarat bagi 22 pasangan beku.
- IS: 3 pasangan lulus, semuanya pada asas L2. F12 TF atas dibuang: +0.79 mata. F08 % industri > SMA50 bawah dibuang: +0.31. F17 FIP atas dibuang: +0.30.
- OOS: ketiga-tiganya merosot kepada +0.19, +0.10 dan −0.08 mata. Tiada pasangan mencapai +0.30 dalam OOS; yang terbaik ialah F16 bawah, +0.27 (t −1.8), yang negatif dalam IS — [ekonomi_IS_beku.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ekonomi_IS_beku.csv); [ekonomi_OOS_beku.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ekonomi_OOS_beku.csv)
- Portfolio 8 slot dengan penapis "TF atas": median Δ CAGR −0.29 mata (H1) dan −2.88 mata (H2), lebih baik bagi 7/19 kaedah dalam H2 — [portfolio5.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/portfolio5.csv)

**Literatur:** literatur meramalkan isyarat ini berfungsi sebagai kedudukan keratan rentas bulanan merentas ribuan saham, dengan pereputan selepas penerbitan. Rujukan:
- [Han, Zhou & Zhu 2016](https://ideas.repec.org/a/eee/jfinec/v122y2016i2p352-375.html)
- [Avramov, Kaplanski & Subrahmanyam 2021](https://onlinelibrary.wiley.com/doi/abs/10.1002/rfe.1118)
- [Da, Gurun & Warachka 2014](https://econpapers.repec.org/RePEc:oup:rfinst:v:27:y:2014:i:7:p:2171-2218.)
- [Blitz, Huij & Martens](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2947044)
- [Hameed & Mian 2015](https://ideas.repec.org/a/cup/jfinqa/v50y2015i1-2p89-117_00.html)
- pembalikan jangka pendek melemah selepas 2000: [Blitz et al. 2023](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4575689)

### Inferences
- Dengan 431 saham besar Shariah dan ufuk 5–21 sesi, kesan keratan rentas yang dilapor dalam literatur (≈ 0.5–1.6% sebulan, kebanyakannya berwajaran sama dan saham kecil) terlalu kecil untuk dikesan dengan stabil, atau memang tiada dalam sampel ini.
- Tiada asas untuk menyusun Watchlist mengikut status trend, RS, jarak MA atau skor ML.
- Tanda "faktor trend" dan HMM bertukar antara tempoh. Itu corak hingar, bukan rejim yang boleh dipercayai.

### Gaps
- Saham yang dinyahsenarai tiada dalam panel (bias kemandirian). Garis dasar jalan rawak mengekalkan drift setiap saham, jadi kesannya terkawal secara relatif, tetapi tidak dibuang.
- Earnings, beta dan saiz tidak dikawal secara berasingan bagi sasaran pulangan.

## 3. Bolehkah "sambungan trend naik" (dari mana/bila mula naik) diramal secara tulen?

### Takeaway
**Nampak boleh, tetapi tidak tulen.** Bagi sasaran sambungan kaki naik zigzag (U10, 3×ATR), banyak ciri trend memberi IC 0.07–0.20 (t sehingga 27). Tujuh ciri jangka panjang mengatasi jalan rawak dalam IS: RS126, garis RS ÷ maks 252, MAD, C/SMA200, C/tinggi 52 minggu, t cerun 126 dan D10+H2. Dalam OOS, beza berbanding jalan rawak jatuh di bawah saiz ekonomi (0.003–0.039 < 0.04). Berbanding siri terbalik tanda (pengelompokan turun naik dikekalkan, arah dibuang), bezanya sifar (t −1.5 hingga +0.05). Model ML (L1) atas data tanpa arah memberi IC U10 yang hampir sama dengan data sebenar: 0.2007 lawan 0.2029. "Trend berterusan" dalam label zigzag ialah artifak mekanik dan turun naik, bukan maklumat arah.

### Cited Findings
Tujuh calon U10 (IC sebenar; IC jalan rawak; IC terbalik tanda; t beza sebenar − rawak; t beza sebenar − terbalik) — [stat_panel_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/stat_panel_IS.csv); [stat_panel_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/stat_panel_OOS.csv); siri [siri_lebar.npz](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/siri_lebar.npz)

| Ciri | IS: IC / rawak / terbalik; t_rw; t_tb | OOS: IC / rawak / terbalik; t_rw; t_tb; Δsaiz rawak |
|---|---|---|
| F02 RS126 | .104/.044/.088; 3.1; 0.8 | .094/.065/.093; 2.0; 0.05; .033 |
| F05 garis RS ÷ maks | .153/.078/.111; 4.1; 2.1 | .115/.085/.120; 2.5; −0.4; .037 |
| F09 MAD | .081/.005/.048; 3.8; 1.5 | .049/.016/.057; 2.4; −0.5; .034 |
| F11 C/SMA200 | .143/.077/.113; 3.4; 1.4 | .121/.086/.120; 2.7; 0.02; .034 |
| F13 C/tinggi 52 mg | .177/.094/.114; 4.2; 2.8 | .130/.104/.148; 2.1; −1.2; .032 |
| F16 t cerun 126 | .070/.003/.050; 3.6; 1.1 | .022/.016/.051; 0.4; −1.5; .003 |
| F30 D10+H2 | .128/.060/.096; 4.2; 1.8 | .104/.072/.106; 2.5; −0.1; .039 |

- Status: lulus kriteria asal IS 7/34, lulus G IS 0/34, lulus OOS 0/7 di bawah kedua-dua kriteria.
- Ciri pantas (r5, r21, Supertrend, C/SMA50, GHM) mempunyai IC U10 yang besar dalam data sebenar, tetapi garis dasar jalan rawak sudah sebesar itu. Contohnya F21 r5 memberi IC 0.205 lawan 0.212 bagi jalan rawak — "kebolehramalan" mekanik semata-mata.
- ML U10 (OOS): data sebenar memberi IC 0.203, AUC dalam tarikh 0.626; panel terbalik tanda memberi IC 0.201, AUC dalam tarikh 0.630 — [ml_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ml_OOS.csv); [ml_OOS_lebar_sf1.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ml_OOS_lebar_sf1.csv)
- Tiada pula ciri yang meramal halangan B21 (bahagian 2). "Kaki naik berterusan" tidak diterjemah kepada kebarangkalian +8% sebelum −8%.
- Literatur juga menunjukkan bahawa fasa bull/bear wujud dalam random walk ([Pagan & Sossounov 2003](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.664)).

### Inferences
- Paparan "sejak bila Bullish" dan "titik mula" (laporan terdahulu) kekal sah sebagai **sejarah deskriptif**. Namun tiada label "mula naik" atau "trend kuat akan berterusan" yang mempunyai kandungan ramalan melebihi siri tanpa arah.
- Label kaki zigzag ex-post tidak sesuai sebagai sasaran latihan atau bukti keberkesanan. Sebarang dakwaan "penanda kami mengesan trend naik dengan ketepatan X%" perlu dibanding dengan garis dasar terbalik tanda.

### Gaps
- Garis dasar terbalik tanda turut membuang kesan leverage, yang merupakan sifat sebenar data. Oleh itu sebahagian kecil "sambungan" mungkin berpunca daripada hubungan turun naik–pulangan yang tulen tetapi tidak berarah.
- Kepekaan zigzag 4×ATR tidak dikira (seperti dalam pradaftar).

## 4. Adakah status memberi maklumat risiko melebihi ATR%?

### Takeaway
**Hampir tiada.** Pada peringkat panel (jatuh > 8% dalam 10 sesi, dinyahmin dalam tarikh × desil ATR%), tiada ciri lulus kriteria IS. Model logistik 27 ciri pula tidak mengatasi model ATR sahaja dalam tarikh yang sama, sama ada dalam IS mahupun OOS. Ada dua pengecualian kecil:
- **lonjakan 5 hari** bagi posisi (P3) lulus OOS, iaitu kesan pembalikan jangka pendek;
- **Bearish lama** konsisten dari segi tanda, tetapi lemah dalam panel (t ≈ 2).

### Cited Findings
**Panel v_j8:** tiada ciri yang lulus. Sembilan ciri dengan |t| ≥ 3 dalam IS semuanya gagal garis dasar jalan rawak (contohnya F20 r21 relatif kumpulan: t 4.98, t_rw 1.03). Kontras keadaan diskret dibetulkan selaras pradaftar D — [stat_panel_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/stat_panel_IS.csv); [vj8_diskret.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/vj8_diskret.csv)

| Kontras keadaan (risiko jatuh melebihi desil ATR%) | IS | OOS |
|---|---|---|
| D10 Bullish − Bearish | −1.0 mata (t −0.6) | +0.4 (t 0.4) |
| Supertrend Bull − Bear | +1.7 (t 2.3) | +2.1 (t 3.5; ISb +0.2) |
| GHM252 Bull − Bear | +2.0 (t 1.6) | +2.2 (t 2.7) |
| Bearish lama (> 60 sesi) − lain | **+4.8 (t 2.3)** | **+3.8 (t 2.1)** |
| Tarik balik dalam trend (F28) − lain | −2.8 (t −3.0) | −1.9 (t −3.2) |

**Posisi P3** (jatuh > 8% dalam 10 sesi, kawalan log ATR%, sel kaedah × umur × bulan; 0.85 juta hari-posisi IS, 1.18 juta OOS):
- F21 r5 tinggi: q **+4.8 mata (t 3.1)** dalam IS dan **+4.4 mata (t 3.7)** dalam OOS; lulus OOS (Holm 0.0015).
- Bearish lama (deskriptif): ≈ +11 mata (t 2.4) IS dan ≈ +8 mata (t 4.6) OOS (anggaran daripada cerun persentil binari).
- Sumber: [posisi_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_IS.csv); [posisi_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_OOS.csv)

**Kadar mentah P(jatuh > 8%/10 sesi)** posisi, mengikut kuintil ATR% (r5 kuintil atas lawan lain) — [desk.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/desk.csv)

| ATR% | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| IS: r5 atas / lain | 11.3 / 9.3 | 15.6 / 15.0 | 22.9 / 21.4 | 31.0 / 26.4 | 41.6 / 37.7 |
| OOS: r5 atas / lain | 7.6 / 6.5 | 12.8 / 11.1 | 17.9 / 15.5 | 21.9 / 20.5 | 35.7 / 30.6 |

**ML lawan model ATR sahaja.** Lajur ATR menunjukkan IC dan AUC dalam tarikh model ATR sahaja; BSS ialah Brier skill L1 berbanding model itu — [ml_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ml_IS.csv); [ml_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ml_OOS.csv)

| Sasaran | IS: L1 IC / AUC dlm tarikh; ATR; BSS | OOS: L1 IC / AUC dlm tarikh; ATR; BSS; kalibrasi L1 |
|---|---|---|
| jatuh > 8% (j8) | .317/.725; .323/.729; +.002 | .281/.7125; .277/.7097; +.005; 0.89 |
| −8% dahulu | .165/.606; .191/.622; +.0005 | .181/.619; .183/.6205; −.005; 0.81 |
| +8% dahulu | .139/.588; .164/.604; +.0045 | .1846/.6142; .1845/.6141; +.006; 1.11 |

- Model LightGBM (L2) gugur kerana kecerunan kalibrasinya 0.26–0.40 dalam IS. Model ATR sahaja mengatasi atau menyamai model 27 ciri dalam tarikh yang sama. Beza kecil OOS bagi j8 (+0.003 AUC) terbalik dalam IS.
- Literatur: risiko diramal oleh turun naik lalu, bukan label ([Barroso & Santa-Clara 2015](https://econpapers.repec.org/RePEc:eee:jfinec:v:116:y:2015:i:1:p:111-120)). Pembalikan jangka pendek tertumpu pada pergerakan tanpa berita dan pusing ganti ([Medhat & Schmeling 2022](https://academic.oup.com/rfs/article-abstract/35/3/1480/6286969)).

### Inferences
- **ATR14% ialah status risiko yang berfungsi.** Kadar jatuh > 8% naik daripada ≈ 7–11% (Q1) kepada ≈ 31–42% (Q5). Status trend tidak menambah maklumat risiko yang boleh dipercayai di atasnya.
- **"Lonjakan 5 hari"** (r5 dalam 20% teratas pasaran) menambah 1–5 mata dalam setiap kuintil ATR. Ia kecil tetapi tahan OOS. Tanda ini sepadan dengan pembalikan, bukan trend: "Bullish pantas" bermaksud risiko lebih tinggi, sama seperti dapatan laporan terdahulu.
- **Bearish lama:** tanda konsisten, tetapi dengan kawalan desil ATR (lebih halus daripada kuintil dalam laporan terdahulu) t panel hanya ≈ 2. Laporan terdahulu (+3.9, t 3.1 / +6.5, t 4.1) kelihatan sedikit melebih-lebihkan kekuatannya. Kesan dalam posisi lebih kuat dalam OOS. Wajar dikekalkan sebagai amaran deskriptif, bukan isyarat.

### Gaps
- Panel tidak mengandungi saham dinyahsenarai, jadi risiko ekor bagi Bearish lama berkemungkinan dipandang rendah.
- Earnings tidak dikawal; lonjakan 5 hari mungkin bertindih dengan reaksi earnings.

## 5. Bagi posisi terbuka: adakah status membantu keputusan pegang atau jual?

### Takeaway
Status meramal **peristiwa** keluar lorong 2 dengan stabil. Kelima belas ciri trend lulus OOS dan kekal selepas kawalan jarak Chandelier tidak linear. Namun status **tidak** meramal baki pulangan dengan stabil, dan **kesemua 44 peraturan jual berasaskan ciri beku menurunkan purata log dalam OOS** (43/44 dalam IS). Peraturan jual itu memperbaiki p5 kira-kira 1–2.6 mata tetapi memotong ekor kanan. Jual apabila D10 jatuh ke kuintil bawah hampir tidak mengubah kejatuhan portfolio (+0.3 / +0.05 mata) dan menurunkan CAGR.

### Cited Findings
**Posisi IS/OOS** (WLS berat kaedah sama, nyahmin sel kaedah × baldi umur × bulan, SE kluster bulan) — [posisi_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_IS.csv); [posisi_ISa.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_ISa.csv); [posisi_ISb.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_ISb.csv); [posisi_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_OOS.csv)

| Sasaran posisi | Calon beku (IS) | OOS | Kor. t IS–OOS (34 ciri) |
|---|---|---|---|
| P1 baki log ke keluar kaedah | F17 FIP −2.3 mata (t −3.2) | **+1.3 (t +2.4), tanda terbalik** | 0.29 |
| P1b baki log ke lorong 2 | F12 TF −3.2 (t −3.2) | +1.4 (t +1.4), terbalik | 0.40 |
| P2 lorong 2 dalam 10 sesi (kawal jarak + log ATR%) | 15 ciri, \|t\| 3.0–7.7 | **15/15 lulus** (Holm ≤ 0.045) | **0.81** |
| P3 jatuh > 8% dalam 10 sesi (kawal log ATR%) | F21 r5 +4.8 (t 3.1) | **+4.4 (t 3.7) lulus** | 0.60 |

Calon P2 terkuat dalam OOS (beza Q5−Q1 dalam kebarangkalian, asas 22%):
- C/SMA50: −13.4 mata (t −6.5)
- Supertrend: −9.1 (t −6.6)
- r21: −9.1 (t −5.5)
- GHM126: −8.6 (t −6.6)
- D10+H2: −5.8 (t −5.0)

Dengan dummy desil jarak dalam sel, kesemua 15 kekal sama tanda dan |t| ≥ 2.97 dalam OOS; contohnya C/SMA50 −13.5 (t −6.8) — [p2_kukuh_IS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/p2_kukuh_IS.csv); [p2_kukuh_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/p2_kukuh_OOS.csv)

**Kadar mentah P(isyarat lorong 2 dalam 10 sesi)** mengikut jarak ke paras Chandelier (unit ATR14), C>SMA50 lawan tidak — [desk.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/desk.csv)

| Jarak | IS: C>SMA50 / tidak | OOS: C>SMA50 / tidak | OOS: Supertrend Bull / Bear |
|---|---|---|---|
| < 1 ATR | 61.2 / 65.2 | 61.8 / 67.0 | 61.8 / 66.5 |
| 1–2 ATR | 36.6 / 39.5 | 36.2 / 43.1 | 37.9 / 38.9 |
| 2–3 ATR | 19.3 / 22.1 | 20.0 / 23.4 | 20.2 / 21.0 |
| ≥ 3 ATR | 11.0 / 10.8 | 10.6 / 10.4 | 10.4 / 11.8 |

**Nilai ekonomi** (22 pasangan; jual buka esok apabila ciri masuk kuintil buruk; kos tambahan 10/20 bps) — [ekonomi.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ekonomi.py); [ekonomi_OOS_beku.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ekonomi_OOS_beku.csv)

| Ujian (OOS) | Asas: purata log / menang / p5 | Δ purata log (min / median / maks) | Δ>0 | Δ p5 median | Bahagian tercetus |
|---|---|---|---|---|---|
| jual 10 bps, asas keluar kaedah | 1.39% / 35.1% / −12.3% | −1.35 / −0.32 / −0.09 | 0/22 | +1.0 | 19% |
| jual 10 bps, asas lorong 2 | 3.13% / 42.2% / −22.1% | −2.93 / −0.88 / −0.38 | 0/22 | +2.6 | 36% |
| jual 20 bps, lorong 2 | — | −3.02 / −0.91 / −0.43 | 0/22 | +2.6 | 36% |
| IS jual 10 bps, lorong 2 | 2.20% / 43.5% / −22.4% | −2.18 / −0.66 / +0.20 | 1/22 | +2.6 | 37% |

- Peraturan jual yang mengikut calon terbaik P2 dan P3 juga merugikan. Dalam OOS (keluar kaedah / lorong 2): C/SMA50 bawah −0.14 / −0.38; Supertrend bawah −0.29 / −0.98; r5 atas −1.35 / −2.93.

**Portfolio 8 slot, 19 kaedah, jual apabila D10 dalam kuintil bawah (berbanding L2):**
- median Δ CAGR −0.84 mata (2019-11..2022) dan −0.43 mata (2023..2026), lebih baik bagi 8/19 kaedah;
- median Δ MDD +0.31 dan +0.05 mata, lebih baik bagi 12/19.
- Sumber: [portfolio5.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/portfolio5.csv)

**Literatur:** hentian/jualan hanya menambah nilai jika pulangan berautokorelasi positif ([Kaminski & Lo](https://dspace.mit.edu/handle/1721.1/114876)), dan pada saham individu hentian ketat kalah ([Lo & Remorov 2017](https://dspace.mit.edu/handle/1721.1/107017)).

**Deskriptif (bukan calon):** log ATR% berkait positif dengan baki pulangan dalam OOS (P1 t 2.7; P1b t 3.3), iaitu premium risiko dan bukan isyarat status.

### Inferences
- Maklumat yang berfungsi bagi posisi ialah **jarak ke paras lorong 2 dalam unit ATR**. Ia memacu P(keluar dalam 10 sesi) daripada ≈ 10% kepada ≈ 59–67%. Status trend hanya menambah 3–7 mata apabila harga dekat paras itu.
- Ini berguna untuk menjangka posisi mana yang akan tertutup, merancang slot dan menetapkan jangkaan. Ia **tidak** berguna untuk menjual lebih awal: jualan awal sentiasa mengurangkan purata dan hanya memperbaiki p5.
- Mengapa ramalan peristiwa yang stabil tidak menjadi nilai? Posisi yang lebih mungkin terkena lorong 2 tidak mempunyai baki pulangan yang lebih buruk secara stabil (P1/P1b terbalik tanda). Menjual awal hanya mendahului jualan yang sama dengan kos tambahan dan kehilangan pantulan.

### Gaps
- Ujian dagangan hanya memakai peraturan "kuintil buruk" (ambang 0.2 tetap). Ambang lain tidak diuji, sengaja, untuk mengelak carian.
- Lejar Penuh hadapan (sejak 16 Okt 2026) terlalu pendek untuk disahkan.

## 6. Cadangan berperingkat dan status akhir yang ringkas

### Takeaway
Berdasarkan semua ujian di atas, **tiada takrif Bullish/Bearish yang berfungsi sebagai peramal arah atau pencetus keputusan.** Yang berfungsi, dan tahan OOS, ialah status **risiko/peristiwa**. Cadangan disusun daripada bukti paling kuat ke paling lemah.

### Cited Findings
Ringkasan keputusan dan bukti — [10_beku.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/10_beku.md); [stat_panel_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/stat_panel_OOS.csv); [posisi_OOS.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/posisi_OOS.csv); [ekonomi_OOS_beku.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/ekonomi_OOS_beku.csv); [desk.csv](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend5/desk.csv)

| # | Cadangan | Bukti | Status |
|---|---|---|---|
| 1 | **Posisi:** paparkan "Jarak lorong 2 = X ATR" dan jalur risiko keluar dalam 10 sesi: < 1 ATR ≈ 59–67%, 1–2 ≈ 36–43%, 2–3 ≈ 19–23%, ≥ 3 ≈ 10–12%. Tambah "trend lemah (C < SMA50)" sebagai pengubah (+3–7 mata dekat paras). Teks tetap: "maklumat, bukan isyarat jual". | P2 15/15 lulus OOS; kekal dengan kawalan jarak tidak linear; kor. t 0.81 | Berfungsi (deskriptif/peristiwa) |
| 2 | **Risiko:** ATR14% (kuintil) sebagai status risiko utama, bersama pill trend. | Q1→Q5: ≈ 7–11% → 31–42% jatuh > 8%/10 sesi; ML 27 ciri tidak mengatasinya dalam tarikh | Berfungsi (risiko) |
| 3 | **Bendera "lonjakan 5 hari"** (r5 dalam 20% teratas pasaran): "risiko pembalikan sedikit lebih tinggi". | P3 +4.8 (t 3.1) IS / +4.4 (t 3.7) OOS; +1–5 mata dalam kuintil ATR | Lulus, kesan kecil; pilihan |
| 4 | **Bearish lama** (> 60 sesi): kekalkan amaran deskriptif sahaja. | Panel +4.8 (t 2.3) / +3.8 (t 2.1); posisi ≈ +11 (t 2.4) / ≈ +8 (t 4.6) | Konsisten tetapi di bawah ambang IS |
| 5 | **Watchlist:** jangan susun atau tapis mengikut status trend, RS, MAD, faktor trend, 52 minggu, HMM atau skor ML. Pill D10+H2 kekal sebagai perbendaharaan kata. | 0/34 ciri, 0 ML; kor. t IS–OOS ≈ 0; penapis masuk 0/22 lulus OOS | Tidak berfungsi |
| 6 | **Jangan bina:** label "Mula naik", "trend akan berterusan", status ML/HMM, atau jualan automatik apabila status bertukar. | U10 dihasilkan semula oleh siri tanpa arah; 44/44 peraturan jual negatif OOS | Ditolak |

### Inferences
- Status akhir yang ringkas, boleh diterangkan dan disokong data bagi **Posisi**:

  ```
  [Pill D10+H2 · umur] · ATR14% (Qk) · Jarak lorong 2: d ATR → Risiko keluar 10 sesi: Rendah (≥3) / Sederhana (2–3) / Tinggi (1–2) / Sangat tinggi (<1)
  ```

  Tambah "· trend lemah" jika C < SMA50, dan "· lonjakan 5 hari" jika r5 berada dalam kuintil teratas. Sertakan teks tetap "bukan isyarat jual".
- Bagi **Watchlist**, cukup paparkan pill D10+H2, umur, titik mula (deskriptif) dan ATR%. Jangan paparkan ramalan.
- Soalan "dari mana/bila mula naik" dijawab secara jujur sebagai sejarah, iaitu tarikh pengesahan dan paras rendah 63 sesi yang dibekukan seperti dalam laporan terdahulu. Data tidak menyokong sebarang dakwaan bahawa permulaan itu meramal kesinambungan.
- Pengesahan hadapan yang wajar dalam Lejar Penuh ialah hipotesis 1 (kalibrasi jalur jarak lorong 2) dan hipotesis 4 (Bearish lama). Kedua-duanya mudah diaudit dan tidak memerlukan carian baharu.

### Gaps
- Hanya dua rejim diliputi: IS (COVID, 2022) dan OOS (kebanyakannya pasaran naik).
- Panel 431 saham yang masih wujud. Dagangan 19 kaedah enjin v1.2 sahaja; kaedah pantulan kurang diwakili.
- Kumulatif projek: trend2–trend5 sudah menguji lebih 500 varian. Satu-satunya pertahanan ialah OOS yang dijalankan sekali bagi senarai beku, dan pengesahan hadapan.
