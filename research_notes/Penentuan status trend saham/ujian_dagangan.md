# Ujian dagangan backtest: adakah label status trend membantu keputusan PEGANG/JUAL posisi swing (3–30 hari)?

Kajian empirikal 23 Okt 2026 atas dagangan enjin v1.2 projek sendiri. Semua skrip dan output: `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/` (baca sahaja repo; tiada fail repo diubah selain nota ini). Sumber dalam nota ini ialah skrip/output tempatan dan fail repo (bukan web). Istilah: **IS** = masuk 1 Nov 2019 – 31 Dis 2022; **OOS** = masuk 1 Jan 2023 – 2 Okt 2026; **K** = keluar kaedah (lorong 1); **L2** = lorong 2 Chandelier tutup 4×ATR14; **t** = statistik t dengan ralat piawai berkelompok ikut bulan; berat = setiap kaedah sama berat dalam setiap tempoh; "log" = ln(1+pulangan).

## 1. Data, kaedah dan senarai calon: apa sebenarnya yang diuji?

### Takeaway
Dagangan sebenar enjin v1.2 bagi 19 kaedah (125,770 dagangan, set 431) berjaya dijana semula dan sepadan tepat dengan registry; 9 definisi status (dibekukan sebelum OOS) dilekatkan pada hari isyarat dan setiap hari pegangan (2.08 juta hari-posisi asas K, 5.41 juta asas L2), lalu 9 ujian status masuk dan 43 peraturan keluar/amaran dibanding IS lawan OOS.

### Cited Findings
- **Set 431** = gabungan `data_mentah/dataset_S1–S4.csv` (108 + 108 + 107 + 108 saham; 2 Jan 2019 – 2 Okt 2026); pemuat yang sama dipakai registry ([WFO/kod/wfo.py](/home/user/papertrade-claude/WFO/kod/wfo.py) `muat_data`, `WFO/kod/registry_baru.py`). Enjin v1.2 tidak diubah: isyarat pada tutup, beli buka esok, kos 0.1% setiap belah ([kod/enjin.py](/home/user/papertrade-claude/BacktestShariah2/kod/enjin.py)).
- **Pemilihan kaedah (dibekukan dahulu, [calon.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/calon.md))**: 10 teratas jadual swing Papan Penganalisis 22 Okt 2026 (M21, M140, M144, M32, M84, M07, M55, M77, M102, M111) + 5 UJI KERTAS/SIMPAN swing (M11, M74, M158, M66, M12) + keluasan: M01 (pantulan BB+RSI), M92 (CCI-50), M73 (pegang pendek 4.8 hari) dan M36 (Turtle) ([data/analisis/papan.json](/home/user/papertrade-claude/BacktestShariah2/data/analisis/papan.json)). Tiada kaedah swing berstatus GUNA (tiga GUNA, M96/M30/M79, pegang > 30 hari). Klasifikasi projek ([kod/jenis_kaedah.csv](/home/user/papertrade-claude/BacktestShariah2/kod/jenis_kaedah.csv)) meletakkan hanya M01 sebagai "pantulan"; 18 lagi "momentum".
- **Pengesahan data**: bilangan dagangan masuk ≥ 1 Nov 2019 sama tepat dengan `bt_n` registry bagi semua 19 kaedah (cth. M21 454, M140 1,269, M32 2,254, M73 30,599); purata/menang/hari sepadan ([jana.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/jana.py), [data/registry_M_gabung.csv](/home/user/papertrade-claude/BacktestShariah2/data/registry_M_gabung.csv)). Lorong 2 dalam kajian ini sama dengan `lorong_henti()` repo bagi 400/400 dagangan rawak ([bina.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/bina.py), [standard/keluar_lorong.py](/home/user/papertrade-claude/BacktestShariah2/standard/keluar_lorong.py)). Purata lorong 2 semua dagangan +5.07%, median −2.70% (kajian lorong 2 repo: +5.1%, median −2.8%) ([kajian/KAJIAN_LORONG2.md](/home/user/papertrade-claude/BacktestShariah2/kajian/KAJIAN_LORONG2.md)).

| Kaedah | Nama ringkas | Keputusan | Kedudukan swing | Dagangan IS / OOS | Hari pegang | Purata % (kaedah) | Purata % (lorong 2) |
|---|---|---|---|---|---|---|---|
| M01 | Bollinger Band + RSI | DITOLAK | 18 | 846 / 1150 | 22.3 | +2.22 | +6.03 |
| M07 | Qullamaggie Breakout | DITOLAK | 6 | 709 / 509 | 8.2 | +1.05 | +17.17 |
| M102 | Stockbee SLTB | SIMPAN | 9 | 5322 / 6312 | 15.6 | +1.34 | +4.14 |
| M11 | NR7 Breakout + Volume | SIMPAN | 12 | 1447 / 1897 | 19.9 | +2.86 | +5.45 |
| M111 | Sistem Volatiliti Wilder | UJI KERTAS | 10 | 3598 / 4940 | 29.9 | +2.39 | +4.96 |
| M12 | Parabolic SAR | UJI KERTAS | 29 | 5135 / 6334 | 23.2 | +2.04 | +4.80 |
| M140 | 猎豹出击 (Serangan Cheetah) | DITOLAK | 2 | 654 / 615 | 24.8 | +5.31 | +17.12 |
| M144 | Screw Bar | UJI KERTAS | 3 | 151 / 110 | 23.4 | +7.68 | +17.79 |
| M158 | Doubly Adaptive Profit Targets | UJI KERTAS | 20 | 3767 / 4700 | 29.7 | +2.94 | +5.07 |
| M21 | Marius 3 Persediaan (Pecahan+Jurang+Ke | DITOLAK | 1 | 231 / 223 | 7.9 | +2.57 | +28.78 |
| M32 | Momentum Burst | UJI KERTAS | 4 | 1020 / 1234 | 22.2 | +3.57 | +8.08 |
| M36 | Turtle 55/20 | DITOLAK | 25 | 3074 / 3943 | 29.6 | +2.65 | +4.32 |
| M55 | Guppy GMMA | UJI KERTAS | 7 | 2966 / 3956 | 28.2 | +2.71 | +3.79 |
| M66 | IBD Undur Pertama ke Purata 50 Hari | UJI KERTAS | 26 | 3755 / 5619 | 19.0 | +1.71 | +4.08 |
| M73 | ADX(5) > 40 + Julat Terkecil 6 Hari | DITOLAK | 39 | 12831 / 17768 | 4.8 | +0.18 | +4.66 |
| M74 | Lulus Baharu Trend Template Minervini | UJI KERTAS | 13 | 945 / 1581 | 20.3 | +2.72 | +5.78 |
| M77 | Undercut & Rally pada Purata Bergerak  | UJI KERTAS | 8 | 975 / 1308 | 14.8 | +2.69 | +4.30 |
| M84 | Jarak purata bergerak MAD 21/200 | UJI KERTAS | 5 | 643 / 905 | 25.5 | +3.71 | +6.30 |
| M92 | CCI-50 | SIMPAN | 31 | 6281 / 8316 | 13.2 | +1.17 | +4.68 |
| Jumlah | 19 kaedah | | | 54350 / 71420 | 17.6 | +1.69 | +5.07 |

- **Definisi status (label pada tutup t, tiada pandang hadapan; [status.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/status.py))**. Bahagian dan purata panjang larian dikira atas semua bar 431 saham yang statusnya diketahui:

| Kod | Takrif | Bull / Neutral / Bear % | Larian purata (hari) |
|---|---|---|---|
| D10 | Bull C>SMA50>SMA150>SMA200; Bear terbalik; pengesahan 2 tutup | 28.6 / 57.7 / 13.7 | 31.7 |
| D10m | D10 tanpa pengesahan | 28.6 / 57.8 / 13.7 | 19.4 |
| MTT | Templat Minervini ringkas (8 syarat harga, tanpa RS; tinggi/rendah 252 hari tutup, min 200 bar); Bear = C<SMA150 & C<SMA200 & SMA200 turun 21 hari | 26.8 / 46.8 / 26.4 | 20.8 |
| WST | Weinstein harian: Bull = C>SMA150 & cerun SMA150 20 hari > +1%; Bear = C<SMA150 & cerun < −1%; lain = peringkat 1/3 | 43.2 / 33.1 / 23.8 | 29.1 |
| EMA | C>EMA20>EMA50 Bull; C<EMA20<EMA50 Bear | 40.9 / 30.5 / 28.6 | 6.8 |
| HHHL | Zigzag 2×ATR14, pivot disahkan oleh tutup sahaja; Bull = PH dan PL lebih tinggi & C>PL terakhir; Bear = PH dan PL lebih rendah & C<PH terakhir | 32.5 / 43.7 / 23.7 | 19.1 |
| ST | Supertrend(10,3), ATR Wilder; binari | 53.6 / 0 / 46.4 | 32.4 |
| ADX | +DI>−DI & ADX14≥20 Bull; −DI>+DI & ADX≥20 Bear; ADX<20 Neutral | 33.8 / 40.7 / 25.5 | 14.6 |
| MULA | "Mula naik/turun": Naik = C>EMA20 & EMA20 > EMA20 5 hari lalu; Turun = terbalik; pengesahan 2 tutup | 49.5 / 11.4 / 39.1 | 10.6 |

- **Ujian** ([bina.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/bina.py), [hari.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hari.py), [analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py)): (1) status pada hari isyarat → lebihan log atas indeks EW 431 (tutup isyarat → tutup keluar), kadar menang, MAE, kadar henti terlompat (keluar `henti` pada buka di bawah paras henti), hari pegang; regresi dengan kesan tetap kaedah (perbandingan dalam kaedah sama). (2) Setiap hari-posisi (tutup d, posisi masih terbuka): baki pulangan jika pegang hingga keluar asas berbanding jual pada buka d+1 (R = harga keluar ÷ buka d+1 − 1), dan P(tutup minimum 10 sesi seterusnya < −8%); dinyahmin dalam sel kaedah × umur posisi × bulan kalendar, jadi yang dibanding ialah posisi sebaya pada bulan yang sama. (3) Peraturan keluar: keluar asas ATAU peristiwa pertama (jual buka esok); peristiwa = "hb" hilang Bull (Bull → bukan Bull) atau "mb" masuk Bear; asas K atau L2; serta "ketat" = L2 dengan gandaan Chandelier 4× → 2×ATR selepas masuk Bear pertama.
- **Bilangan varian**: 9 status × ujian masuk; 9 × 2 asas × 7 statistik hari-posisi (126); 43 peraturan keluar (9 × 2 peristiwa × 2 asas − 2 pendua ST + 9 ketat). Jumlah perbandingan utama 52 (9 + 43). Satu senarai calon sahaja, dibekukan dalam [calon.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/calon.md) sebelum OOS dijalankan; pilihan sementara daripada IS juga ditulis di situ sebelum OOS.
- **Urutan analisis (jujur)**: [analisis.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis.py) (purata aritmetik) dijalankan atas IS dahulu; kesan tetap kaedah ditambah pada ujian (1) selepas melihat IS (komposisi kaedah mengelirukan kadar menang/MAE), sebelum OOS. Selepas OOS dilihat, versi log teguh [analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py) ditambah kerana ekor sangat berat: AXTI naik daripada 1.41 (Mac 2025) ke 85.87 (Okt 2026) dan memberi dagangan lorong 2 sehingga +4,971% ([hasil_IS.txt / hasil_OOS.txt](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil_OOS.txt)). Kedua-dua versi memberi tanda kesimpulan yang sama; nota ini memakai versi log sebagai utama dan menyebut aritmetik apabila berbeza.

### Inferences
- Data dagangan ialah dagangan enjin sebenar projek, bukan proksi; jadi keputusan terus berkaitan dengan posisi Papertrade C/Lejar (yang memakai peraturan kaedah dan lorong 2 yang sama).
- Pengesahan 2 tutup mengubah D10 dengan ketara (larian 19.4 → 31.7 hari), tetapi definisi jangka pendek (EMA 6.8 hari, MULA 10.6 hari) bertukar terlalu kerap untuk label papan 3–30 hari.

### Gaps
- Hanya satu kaedah "pantulan" mengikut klasifikasi projek; keputusan bagi kaedah pantulan murni (M02, M03, …) tidak diuji.
- Bias penyintas: 431 saham Shariah semasa; saham yang dinyahsenarai tiada. Ini menyebelahi pegangan lebih lama (tiada keruntuhan delist), jadi boleh merendahkan nilai keluar awal.
- Kluster bulan tidak menangkap sepenuhnya pertindihan pegangan merentas bulan; t ±2 perlu dibaca sebagai anggaran, dan konsistensi IS/OOS serta merentas kaedah lebih bermakna. Dengan ~180 statistik, beberapa |t| > 2 dijangka secara kebetulan.
- Posisi lorong 2 yang masih terbuka pada 2 Okt 2026 (4% dagangan OOS) dinilai pada tutup terakhir.

## 2. Adakah status pada hari isyarat meramal hasil dagangan (pulangan, menang, MAE, henti terlompat)?

### Takeaway
Tidak secara konsisten: tiada definisi memberi beza lebihan Bull−Bear yang sama tanda dan signifikan dalam IS dan OOS (calon IS WST +1.08% t 2.2 menjadi −0.88% t −1.4 dalam OOS). Yang stabil hanyalah kesan sampingan: masuk ketika status jangka pendek Bull bermakna pegang lebih lama, MAE lebih dalam dan henti terlompat lebih kerap; dan masuk ketika D10 sudah Bull > 60 hari (+76–97% sejak bertukar) memberi lebihan lebih rendah ~1.3% berbanding purata kaedah.

### Cited Findings
- Status masuk (Δ = Bull − Bear dalam kaedah sama, regresi kesan tetap kaedah; mata = mata peratusan; MAE bernilai negatif, jadi Δ MAE negatif = Bull lebih dalam; t dalam kurungan; [analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py), [hasil2_IS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_IS.pkl), [hasil2_OOS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_OOS.pkl), [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/jadual.md)):

| Status | Bull / Bear (% isyarat, OOS) | Δ lebihan log Bull−Bear IS (t) | OOS (t) | Kaedah Bull>Bear IS · OOS | Δ menang mata IS / OOS | Δ MAE mata IS / OOS | Δ henti terlompat mata IS (t) / OOS (t) | Δ hari pegang IS / OOS | Δ lebihan log lorong 2 IS (t) / OOS (t) |
|---|---|---|---|---|---|---|---|---|---|
| D10 | 32 / 8 | -0.33 (-0.5) | -0.84 (-0.9) | 5/7 · 3/8 | -1.4 / -3.0 | -0.23 / -0.54 | +0.09 (0.1) / +1.45 (2.2) | +5.5 / +1.3 | -1.38 (-0.9) / -3.23 (-1.0) |
| D10m | 45 / 3 | +0.04 (0.1) | +0.01 (0.0) | 2/5 · 1/4 | -6.5 / -1.4 | -1.18 / -0.70 | -0.06 (-0.2) / +0.83 (1.7) | +11.3 / +6.8 | -0.44 (-0.3) / -2.98 (-1.1) |
| MTT | 42 / 16 | +0.36 (0.5) | -0.76 (-1.0) | 11/13 · 7/14 | -0.4 / -2.1 | +0.84 / -0.36 | -0.68 (-0.7) / -0.32 (-0.5) | +2.8 / +0.3 | -0.51 (-0.4) / -2.29 (-1.2) |
| WST | 53 / 15 | +1.08 (2.2) | -0.88 (-1.4) | 13/16 · 7/15 | +1.5 / -1.5 | +0.58 / -0.08 | -0.48 (-0.5) / -0.22 (-0.4) | +4.2 / -0.3 | +1.24 (1.3) / -1.96 (-1.0) |
| EMA | 62 / 9 | +0.71 (1.2) | -1.18 (-1.0) | 4/6 · 1/7 | -7.6 / -6.8 | -1.50 / -2.23 | +1.34 (3.3) / +1.71 (5.2) | +15.6 / +14.5 | +1.89 (1.7) / +1.87 (0.9) |
| HHHL | 36 / 16 | -0.71 (-1.5) | -2.43 (-3.0) | 6/18 · 1/18 | -2.3 / -5.4 | -1.15 / -1.16 | +0.33 (0.6) / +0.40 (0.8) | +5.1 / +0.7 | -0.62 (-0.8) / -4.14 (-2.9) |
| ST | 68 / 32 | +0.47 (1.5) | -0.09 (-0.2) | 7/16 · 6/16 | +2.6 / +2.1 | -0.97 / -0.94 | +1.41 (3.6) / +1.30 (3.7) | +8.4 / +7.5 | +1.04 (2.4) / -0.72 (-1.1) |
| ADX | 42 / 12 | +0.28 (0.5) | -0.43 (-0.6) | 6/13 · 6/13 | -1.4 / -1.5 | -0.93 / -1.48 | +1.31 (2.4) / +2.11 (4.0) | +10.4 / +9.3 | +1.00 (1.1) / +1.23 (1.0) |
| MULA | 57 / 31 | +0.31 (0.6) | +0.15 (0.2) | 10/16 · 9/17 | +0.5 / +0.4 | -0.83 / -0.91 | +1.97 (5.0) / +2.12 (5.6) | +8.5 / +7.3 | +1.34 (2.2) / +1.07 (1.4) |

- Umur status Bull semasa isyarat (lebihan log relatif purata kaedah; baris tebal = regresi umur > 60 lawan ≤ 60 dengan kesan tetap kaedah):

| Status | Umur Bull semasa isyarat (hari) | Bahagian IS / OOS | Jarak dari tutup hari bertukar Bull % IS / OOS | Lebihan log relatif purata kaedah % IS / OOS | Menang % IS / OOS |
|---|---|---|---|---|---|
| D10 | 1-5 | 22 / 24 | +3.1 / +2.9 | -0.84 / +0.28 | 31.4 / 32.8 |
| D10 | 6-20 | 38 / 38 | +8.9 / +10.4 | -0.16 / -0.29 | 30.3 / 31.2 |
| D10 | 21-60 | 32 / 29 | +26.1 / +25.7 | +0.29 / -0.89 | 30.5 / 30.5 |
| D10 | 61- | 8 / 9 | +75.8 / +96.6 | -1.40 / -2.02 | 26.1 / 26.5 |
| D10 | **>60 lawan ≤60 (kesan tetap kaedah)** | n 1310 / 1653 | | **-1.25 (t -2.2) / -1.31 (t -1.8)** | |
| ST | 1-5 | 25 / 28 | +2.0 / +1.7 | -0.05 / +0.63 | 34.6 / 36.3 |
| ST | 6-20 | 32 / 33 | +8.6 / +9.3 | +0.05 / -0.11 | 31.1 / 32.7 |
| ST | 21-60 | 34 / 31 | +23.2 / +21.1 | +0.36 / -0.27 | 30.1 / 30.1 |
| ST | 61- | 9 / 8 | +79.3 / +59.4 | -0.10 / -1.07 | 31.1 / 29.2 |
| ST | **>60 lawan ≤60 (kesan tetap kaedah)** | n 2675 / 3025 | | **-0.27 (t -0.6) / -1.22 (t -2.2)** | |

- Kadar henti terlompat (keluar pada buka di bawah paras henti) purata, daripada dagangan yang mempunyai henti: 4.7% (IS), 5.4% (OOS); M01 dan M73 tiada henti ([hasil2_IS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_IS.pkl), [hasil2_OOS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_OOS.pkl)).

### Inferences
- Status trend pada hari isyarat bukan penapis beli yang berguna di atas peraturan kaedah sendiri; HHHL malah berpusing tanda (struktur LH/LL lebih baik dalam OOS, 1/18 kaedah Bull>Bear), konsisten dengan kesan pembalikan jangka pendek.
- Henti terlompat dan MAE lebih buruk bagi masuk "Bull jangka pendek" sebahagian besarnya kerana posisi itu dipegang lebih lama (+7 hingga +15 hari), bukan bukti risiko per hari lebih tinggi.
- Maklumat "sejak bila Bullish" berguna sebagai konteks: Bull D10 > 60 hari ≈ trend lewat (harga ~+76% hingga +97% daripada tutup hari bertukar), purata lebih lemah dalam kedua-dua tempoh.

### Gaps
- Kesan umur > 60 hari hanya t −2.2 (IS) dan −1.8 (OOS) bagi D10; ST hanya OOS. Belum diuji sama ada ambang 60 hari optimum (tidak dicuba ambang lain, untuk elak pemilihan).

## 3. Adakah status atau perubahan status semasa memegang meramal baki pulangan dan risiko posisi terbuka?

### Takeaway
Baki pulangan: tiada definisi meramal secara konsisten (tanda berubah antara IS dan OOS). Risiko: status jangka panjang (D10, MTT, WST) Bull berbanding Bear menurunkan P(jatuh > 8% dalam 10 sesi) sebanyak 1.4–3.8 mata bagi posisi sebaya pada bulan sama (asas K: D10 −2.6 t −2.1 / −2.4 t −3.2; WST −3.8 t −3.0 / −2.1 t −3.9), manakala status jangka pendek (EMA, ST, ADX, MULA) bertanda terbalik. Peristiwa flip (hilang Bull, masuk Bear, "mula turun") tidak diikuti baki pulangan lebih rendah, dan risiko jatuh selepas flip lebih RENDAH daripada biasa.

### Cited Findings
- Asas keluar kaedah: hari-posisi IS 913,172 / OOS 1,171,495; median baki pulangan -1.71% / -1.35%; P(jatuh >8% dalam 10 sesi) 23.6% / 19.6%. ([analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py), [hasil2_IS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_IS.pkl), [hasil2_OOS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_OOS.pkl))

| Status | Δ baki log Bull−Bear IS (t) | OOS (t) | Δ P(jatuh>8%/10s) mata Bull−Bear IS (t) | OOS (t) | P(jatuh) mentah Bull / Bear IS | OOS |
|---|---|---|---|---|---|---|
| D10 | -0.15 (-0.3) | +0.23 (0.9) | -2.6 (-2.1) | -2.4 (-3.2) | 22.0 / 33.3 | 20.1 / 19.5 |
| D10m | -0.21 (-0.4) | +0.22 (0.8) | -2.1 (-1.8) | -1.9 (-2.6) | 22.0 / 33.0 | 20.1 / 19.5 |
| MTT | +0.39 (0.7) | +0.08 (0.3) | -3.6 (-3.0) | -1.4 (-2.5) | 22.2 / 31.8 | 20.1 / 19.4 |
| WST | +0.60 (1.3) | +0.34 (1.1) | -3.8 (-3.0) | -2.1 (-3.9) | 22.7 / 32.3 | 20.4 / 20.8 |
| EMA | -0.42 (-3.5) | -0.07 (-0.4) | +1.1 (2.0) | +0.8 (2.9) | 22.8 / 31.1 | 19.9 / 17.4 |
| HHHL | -0.03 (-0.1) | -0.85 (-2.3) | +0.5 (0.7) | +0.3 (0.4) | 23.7 / 27.9 | 20.9 / 17.9 |
| ST | -0.30 (-1.5) | -0.40 (-1.3) | +1.6 (2.6) | +1.6 (3.3) | 23.0 / 26.2 | 19.9 / 18.4 |
| ADX | -0.53 (-2.7) | +0.38 (1.3) | +2.9 (2.7) | +2.4 (5.4) | 24.1 / 28.3 | 20.2 / 17.4 |
| MULA | -0.32 (-1.9) | +0.23 (0.9) | +1.5 (1.9) | +0.8 (1.9) | 23.0 / 27.2 | 19.9 / 18.3 |

| Status | Peristiwa | n IS / OOS | Median baki pulangan % IS / OOS | Δ baki log (lawan sel) IS (t) | OOS (t) | Δ P(jatuh>8%/10s) mata IS (t) | OOS (t) |
|---|---|---|---|---|---|---|---|
| D10 | hilang Bull | 4346 / 5915 | -0.46 / -0.97 | +0.69 (1.6) | +0.17 (0.4) | -3.1 (-2.1) | -0.4 (-0.2) |
| D10 | masuk Bear | 1522 / 1803 | +0.08 / +0.28 | +0.23 (0.6) | +0.21 (0.8) | +1.5 (1.0) | -0.3 (-0.2) |
| D10m | hilang Bull | 18660 / 23738 | +0.00 / +0.00 | +0.91 (1.9) | -0.46 (-0.9) | -4.0 (-2.5) | -2.1 (-2.1) |
| D10m | masuk Bear | 5546 / 5951 | +0.00 / +0.00 | +0.21 (0.3) | -0.12 (-0.3) | -0.1 (-0.1) | -0.7 (-0.5) |
| MTT | hilang Bull | 18382 / 23557 | +0.00 / +0.00 | +1.10 (2.3) | +0.27 (0.6) | -3.5 (-2.1) | -1.5 (-1.5) |
| MTT | masuk Bear | 5739 / 7188 | -0.32 / -0.00 | +1.11 (2.7) | -0.48 (-1.2) | +0.2 (0.2) | +1.0 (0.6) |
| WST | hilang Bull | 2995 / 4668 | +0.00 / +0.00 | -0.54 (-0.7) | +0.15 (0.2) | -0.1 (-0.1) | -1.3 (-1.2) |
| WST | masuk Bear | 5349 / 5797 | -0.78 / -0.30 | +1.17 (3.2) | -0.68 (-1.4) | +1.9 (1.3) | +1.4 (0.7) |
| EMA | hilang Bull | 59749 / 73957 | -1.32 / -1.24 | +0.73 (3.7) | -0.20 (-0.7) | -2.8 (-2.6) | -1.5 (-2.1) |
| EMA | masuk Bear | 6979 / 8504 | +0.00 / +0.00 | -0.19 (-0.4) | -0.35 (-0.5) | -0.6 (-0.6) | -0.9 (-0.9) |
| HHHL | hilang Bull | 9899 / 12898 | +0.00 / +0.00 | +0.99 (2.3) | +0.33 (0.6) | -2.0 (-1.6) | -2.7 (-2.0) |
| HHHL | masuk Bear | 5463 / 7357 | -0.00 / +0.00 | -0.08 (-0.2) | +0.40 (1.1) | -0.2 (-0.1) | -1.5 (-1.2) |
| ST | flip ke Bear | 13709 / 17760 | +0.00 / +0.00 | +1.36 (3.1) | +0.83 (2.0) | -5.4 (-2.1) | -5.3 (-4.3) |
| ADX | hilang Bull | 29745 / 37545 | -1.44 / -0.82 | +0.56 (2.2) | -0.28 (-0.9) | -3.2 (-1.9) | -2.1 (-2.9) |
| ADX | masuk Bear | 20769 / 27001 | -0.99 / -0.17 | +0.81 (2.6) | -0.24 (-0.7) | -3.7 (-1.8) | -2.5 (-2.7) |
| MULA | hilang Bull | 26898 / 34409 | -1.25 / -1.14 | +1.12 (3.7) | +0.10 (0.3) | -3.0 (-2.4) | -2.2 (-2.7) |
| MULA | masuk Bear | 16057 / 20936 | -0.83 / -0.54 | +0.46 (1.3) | -0.07 (-0.2) | -2.3 (-1.6) | -2.4 (-3.3) |

- Asas lorong 2: hari-posisi IS 2,405,883 / OOS 3,004,675; median baki pulangan -3.09% / -2.95%; P(jatuh >8% dalam 10 sesi) 23.1% / 20.6%. ([analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py), [hasil2_IS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_IS.pkl), [hasil2_OOS.pkl](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil2_OOS.pkl))

| Status | Δ baki log Bull−Bear IS (t) | OOS (t) | Δ P(jatuh>8%/10s) mata Bull−Bear IS (t) | OOS (t) | P(jatuh) mentah Bull / Bear IS | OOS |
|---|---|---|---|---|---|---|
| D10 | -1.79 (-4.1) | -0.54 (-0.7) | -1.5 (-0.9) | -1.5 (-1.7) | 22.2 / 29.3 | 21.4 / 20.6 |
| D10m | -1.92 (-4.4) | -0.53 (-0.7) | -0.6 (-0.3) | -1.0 (-1.0) | 22.1 / 28.9 | 21.4 / 20.6 |
| MTT | -1.19 (-2.3) | -0.44 (-0.8) | -2.2 (-1.9) | -1.0 (-1.4) | 22.3 / 29.0 | 21.4 / 19.9 |
| WST | -0.56 (-1.3) | -0.31 (-0.5) | -3.0 (-2.6) | -1.8 (-2.7) | 22.7 / 30.0 | 21.7 / 21.1 |
| EMA | -1.04 (-2.8) | -0.03 (-0.1) | +1.8 (1.6) | +1.1 (1.6) | 22.4 / 26.8 | 20.4 / 20.5 |
| HHHL | -0.52 (-1.1) | -1.26 (-1.8) | +0.6 (0.5) | +0.5 (0.6) | 23.4 / 25.2 | 21.7 / 19.7 |
| ST | -0.13 (-0.3) | -0.63 (-1.1) | +1.4 (1.6) | +1.4 (2.1) | 22.7 / 24.6 | 20.5 / 21.1 |
| ADX | -0.74 (-1.9) | +1.00 (1.5) | +3.1 (2.1) | +2.5 (3.8) | 23.6 / 26.5 | 20.8 / 20.7 |
| MULA | -0.88 (-3.1) | +0.63 (1.0) | +1.9 (1.7) | +0.8 (1.1) | 22.6 / 24.6 | 20.2 / 21.5 |

| Status | Peristiwa | n IS / OOS | Median baki pulangan % IS / OOS | Δ baki log (lawan sel) IS (t) | OOS (t) | Δ P(jatuh>8%/10s) mata IS (t) | OOS (t) |
|---|---|---|---|---|---|---|---|
| D10 | hilang Bull | 30589 / 37513 | -1.52 / -1.59 | +0.38 (0.7) | -0.78 (-1.0) | -3.5 (-2.1) | -1.8 (-1.3) |
| D10 | masuk Bear | 9333 / 10394 | -1.74 / -1.78 | +1.42 (2.8) | +1.17 (1.3) | -3.2 (-1.3) | -0.9 (-0.7) |
| D10m | hilang Bull | 61088 / 74921 | -1.26 / -1.49 | +0.70 (1.7) | -1.03 (-1.5) | -3.5 (-2.7) | -1.4 (-1.1) |
| D10m | masuk Bear | 17600 / 19564 | -1.95 / -1.48 | +1.09 (2.6) | +0.14 (0.2) | -0.5 (-0.3) | -0.3 (-0.2) |
| MTT | hilang Bull | 59777 / 72654 | -1.32 / -1.63 | +0.72 (1.6) | +0.06 (0.1) | -3.0 (-2.2) | -0.8 (-0.6) |
| MTT | masuk Bear | 16550 / 22272 | -2.07 / -1.73 | +0.90 (1.5) | -1.45 (-2.2) | +0.9 (0.7) | -0.8 (-0.6) |
| WST | hilang Bull | 15075 / 21682 | -0.07 / -0.44 | +0.90 (1.7) | +0.58 (0.6) | -0.9 (-0.7) | -2.4 (-2.1) |
| WST | masuk Bear | 13765 / 16259 | -2.56 / -2.09 | +0.95 (1.5) | -1.49 (-1.3) | +2.6 (2.0) | +0.8 (0.5) |
| EMA | hilang Bull | 165002 / 199546 | -3.07 / -2.99 | +0.63 (3.1) | -0.45 (-1.0) | -2.0 (-2.2) | -1.3 (-2.0) |
| EMA | masuk Bear | 33780 / 43256 | -2.37 / -2.11 | +0.81 (2.4) | +0.16 (0.3) | -0.2 (-0.2) | -0.5 (-0.6) |
| HHHL | hilang Bull | 36891 / 47180 | -0.66 / -0.65 | +1.14 (3.2) | +0.85 (0.8) | -1.8 (-1.3) | -3.5 (-2.7) |
| HHHL | masuk Bear | 17535 / 22577 | -2.88 / -2.51 | -0.03 (-0.1) | +0.72 (1.0) | +1.5 (1.0) | -0.9 (-0.8) |
| ST | flip ke Bear | 54509 / 70249 | +0.00 / +0.00 | +1.19 (2.2) | +0.16 (0.3) | -3.3 (-1.7) | -4.3 (-4.9) |
| ADX | hilang Bull | 77974 / 98609 | -2.47 / -2.16 | +0.84 (3.0) | -0.62 (-1.3) | -2.0 (-1.2) | -1.4 (-1.8) |
| ADX | masuk Bear | 58005 / 76399 | -2.01 / -1.50 | +1.03 (2.7) | -0.31 (-0.5) | -2.5 (-1.3) | -2.3 (-2.7) |
| MULA | hilang Bull | 85920 / 107462 | -2.53 / -2.58 | +1.19 (4.0) | -0.27 (-0.5) | -3.3 (-2.8) | -1.5 (-1.9) |
| MULA | masuk Bear | 66211 / 82950 | -2.19 / -2.06 | +0.68 (2.3) | -0.37 (-0.6) | -2.7 (-2.3) | -1.6 (-2.2) |

- Umur status D10 Bull pada hari-posisi (> 60 lawan ≤ 60 hari, dalam sel): asas K baki log −0.64 (t −1.7) IS, −1.18 (t −1.4) OOS; P(jatuh) +0.8 (t 0.7) IS, +2.4 (t 2.5) OOS; asas L2 P(jatuh) +1.3 (t 1.0) IS, +3.3 (t 2.6) OOS ([tambahan.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/tambahan.py)).
- Semakan tanpa syarat (semua saham-hari, panel kajian terdahulu): lebihan P(jatuh > 8%/10 sesi) Bear − Bull hari sama: D10 +6.0 mata (t 3.7) IS, +3.7 (t 3.0) OOS; WST ±1% +5.7 (t 4.2), +3.4 (t 3.5); subset momentum D10 +11.3 / +8.1, WST +7.4 / +8.9 ([risiko_wst.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/risiko_wst.py); asal [trend/risiko2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend/risiko2.py)).
- Kebetulan dengan keluar kaedah: D10 hilang Bull sebelum keluar kaedah hanya dalam 6.6% (IS) / 7.0% (OOS) dagangan; ST flip ke Bear 23% dan 42% daripadanya pada tutup terakhir sebelum keluar kaedah, jadi baki median 0.00% ialah peristiwa yang serentak dengan isyarat keluar kaedah sendiri ([tambahan.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/tambahan.py)).

### Inferences
- Peranan status jangka panjang ialah **maklumat risiko relatif** (posisi mana lebih mudah jatuh tajam minggu ini), bukan ramalan pulangan. Ini mengesahkan dapatan tanpa syarat kajian terdahulu pada peringkat posisi sebenar ([trend/nota_amalan_trend.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend/nota_amalan_trend.md)).
- Flip itu sendiri bukan amaran: ia biasanya berlaku selepas kejatuhan sudah berlaku, dan selepasnya risiko jatuh lanjut lebih rendah daripada posisi lain (ST −5.3 mata t −4.3 OOS). Yang membawa maklumat ialah *berada* dalam Bear jangka panjang, bukan *saat* bertukar.
- Status jangka pendek "Bull" (EMA/ST/ADX/MULA) menandakan saham baru naik kuat, yang lebih meruap; melabelnya "Bullish" tanpa konteks boleh mengelirukan pengguna tentang risiko.

### Gaps
- Dalam IS asas L2, posisi berstatus Bear mempunyai baki log lebih tinggi (D10 −1.79 t −4.1), tetapi OOS tidak (−0.54 t −0.7): mungkin kesan lantunan 2020/2022; tidak dapat dipisahkan dengan sampel ini.
- P(jatuh) mentah OOS hampir sama bagi Bull dan Bear (D10 20.1% lawan 19.5%); beza hanya muncul dalam perbandingan bulan sama. Paparan risiko mutlak tidak disokong.

## 4. Adakah keluar atau amaran berasaskan status mengatasi atau melengkapi keluar kaedah dan lorong 2?

### Takeaway
Tidak. Ke-43 peraturan menurunkan purata log setiap dagangan dalam kedua-dua tempoh (IS 43/43 negatif, 2 hampir sifar, 1 dengan t < −2; OOS 43/43 negatif, 23 dengan t < −2), dengan hanya 0–10 daripada 19 kaedah mendapat manfaat; menjual pada flip "membantu" lebih separuh posisi yang terkena (median baki negatif) tetapi kehilangan ekor kanan yang menjadi sumber untung swing. Ukuran sebulan (modal dipusing) memberi petunjuk bercampur bagi "L2 + keluar bila D10 hilang Bull", tetapi tidak teguh (log OOS t 0.5) dan tidak menang dalam simulasi portfolio 8 slot. Mengetatkan Chandelier selepas masuk Bear juga tidak membantu.

### Cited Findings
- Peraturan keluar (Δ = peraturan − asas setiap dagangan; "kena" = % dagangan dengan peristiwa sebelum keluar asas; "bantu" = % daripada yang kena di mana jual awal lebih baik; laras masa = Δ log − kadar log harian asas × Δ hari, iaitu andaian modal dibebaskan memperoleh kadar purata asas; [analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py), [jadual.md](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/jadual.md)):

| Peraturan | Kena % IS / OOS | Bantu % (antara yang kena) IS / OOS | Median baki % IS / OOS | Δ purata % IS / OOS | Δ log % IS (t) | OOS (t) | Kaedah untung IS · OOS | Δ log laras masa IS (t) | OOS (t) | p5 % IS / OOS | Hari IS / OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **ASAS kaedah** | | | | purata +1.80 / +3.54 | log +0.46 | log +1.39 | | | | -12.2 / -11.5 | 20.2 / 20.1 |
| **ASAS lorong 2** | | | | purata +5.35 / +11.46 | log +2.20 | log +3.13 | | | | -20.0 / -19.8 | 46.5 / 44.2 |
| K D10 hb | 5 / 6 | 56 / 60 | -0.8 / -1.4 | -0.07 / -0.32 | -0.03 (-1.2) | -0.15 (-1.8) | 4/18 · 2/18 | -0.01 (-0.5) | -0.08 (-1.0) | -12.0 / -11.5 | 19.3 / 19.2 |
| L2 D10 hb | 40 / 38 | 55 / 59 | -1.1 / -1.6 | -0.48 / -0.78 | -0.09 (-0.6) | -0.44 (-1.9) | 6/19 · 1/19 | +0.31 (2.6) | +0.11 (0.5) | -18.7 / -18.1 | 38.0 / 36.4 |
| K D10 mb | 2 / 2 | 41 / 43 | +0.5 / +0.2 | -0.05 / -0.03 | -0.06 (-1.7) | -0.02 (-2.0) | 2/5 · 0/5 | -0.05 (-1.6) | -0.01 (-0.5) | -12.2 / -11.5 | 20.0 / 19.9 |
| L2 D10 mb | 12 / 10 | 57 / 59 | -1.7 / -1.9 | -0.33 / -1.05 | -0.13 (-0.8) | -0.31 (-1.6) | 4/17 · 2/18 | +0.01 (0.1) | -0.12 (-0.7) | -19.4 / -19.4 | 43.6 / 41.6 |
| L2 D10 ketat | – / – | – / – | – / – | -0.28 / -1.01 | -0.11 (-0.9) | -0.28 (-1.6) | 3/17 · 2/18 | +0.00 (0.0) | -0.13 (-0.8) | -19.4 / -19.5 | 44.1 / 42.1 |
| K D10m hb | 30 / 30 | 16 / 18 | +0.0 / +0.0 | -0.21 / -0.32 | -0.08 (-1.7) | -0.14 (-1.6) | 4/18 · 1/17 | -0.05 (-1.1) | -0.05 (-0.6) | -12.0 / -11.4 | 19.0 / 18.9 |
| L2 D10m hb | 56 / 56 | 50 / 53 | -0.0 / -0.9 | -1.28 / -0.80 | -0.52 (-1.6) | -0.36 (-1.2) | 1/19 · 3/19 | +0.06 (0.2) | +0.40 (1.5) | -18.1 / -17.2 | 34.3 / 33.5 |
| K D10m mb | 9 / 7 | 17 / 18 | +0.0 / +0.0 | -0.05 / -0.04 | -0.04 (-1.3) | -0.02 (-2.1) | 2/5 · 0/5 | -0.03 (-1.1) | -0.00 (-0.3) | -12.1 / -11.5 | 19.8 / 19.8 |
| L2 D10m mb | 16 / 14 | 57 / 55 | -1.5 / -1.2 | -0.60 / -1.22 | -0.23 (-1.1) | -0.38 (-1.5) | 2/18 · 2/18 | -0.03 (-0.2) | -0.13 (-0.6) | -19.1 / -19.2 | 42.2 / 40.6 |
| L2 D10m ketat | – / – | – / – | – / – | -0.47 / -1.17 | -0.18 (-1.2) | -0.36 (-1.6) | 2/18 · 2/18 | -0.03 (-0.2) | -0.16 (-0.8) | -19.2 / -19.3 | 43.2 / 41.4 |
| K MTT hb | 29 / 29 | 18 / 21 | +0.0 / +0.0 | -0.30 / -0.97 | -0.12 (-2.0) | -0.20 (-2.0) | 2/18 · 0/18 | -0.08 (-1.6) | -0.10 (-1.0) | -12.0 / -11.3 | 18.8 / 18.6 |
| L2 MTT hb | 55 / 54 | 51 / 53 | -0.2 / -0.9 | -1.31 / -6.68 | -0.53 (-1.8) | -1.00 (-2.4) | 1/19 · 1/19 | +0.04 (0.2) | -0.23 (-0.6) | -18.2 / -17.4 | 34.4 / 33.3 |
| K MTT mb | 8 / 7 | 53 / 50 | -0.7 / -0.0 | -0.19 / -0.11 | -0.11 (-1.1) | -0.05 (-1.3) | 7/16 · 6/17 | -0.08 (-0.8) | +0.03 (0.9) | -11.9 / -11.4 | 18.8 / 19.0 |
| L2 MTT mb | 16 / 16 | 57 / 57 | -2.2 / -1.6 | -0.67 / -0.29 | -0.27 (-1.2) | -0.09 (-0.8) | 5/19 · 3/18 | -0.03 (-0.2) | +0.22 (2.4) | -19.5 / -19.3 | 41.4 / 39.9 |
| L2 MTT ketat | – / – | – / – | – / – | -0.60 / -0.24 | -0.25 (-1.5) | -0.09 (-1.0) | 2/19 · 2/18 | -0.07 (-0.5) | +0.13 (1.7) | -19.6 / -19.5 | 42.7 / 41.1 |
| K WST hb | 4 / 5 | 47 / 47 | +0.0 / +0.0 | -0.08 / -0.11 | -0.04 (-0.6) | -0.06 (-1.5) | 7/18 · 5/17 | -0.02 (-0.4) | -0.01 (-0.3) | -12.0 / -11.5 | 19.6 / 19.4 |
| L2 WST hb | 17 / 20 | 47 / 48 | +0.0 / +0.0 | -0.52 / -3.43 | -0.25 (-1.4) | -0.48 (-1.9) | 2/19 · 1/19 | -0.08 (-0.5) | -0.20 (-0.8) | -19.5 / -18.9 | 42.8 / 40.2 |
| K WST mb | 8 / 6 | 55 / 52 | -1.1 / -0.4 | -0.12 / -0.07 | -0.06 (-0.6) | -0.03 (-0.9) | 8/16 · 10/17 | -0.03 (-0.3) | +0.05 (1.5) | -12.0 / -11.4 | 18.9 / 19.1 |
| L2 WST mb | 14 / 13 | 60 / 59 | -2.7 / -2.4 | -0.49 / -0.25 | -0.15 (-0.8) | -0.09 (-1.0) | 5/19 · 4/18 | +0.07 (0.4) | +0.18 (2.4) | -19.5 / -19.4 | 41.8 / 40.4 |
| L2 WST ketat | – / – | – / – | – / – | -0.43 / -0.24 | -0.16 (-1.1) | -0.12 (-1.5) | 2/19 · 2/18 | -0.00 (-0.0) | +0.08 (1.3) | -19.6 / -19.5 | 43.0 / 41.4 |
| K EMA hb | 52 / 51 | 59 / 59 | -1.4 / -1.2 | -0.96 / -1.63 | -0.39 (-1.3) | -0.45 (-2.0) | 4/19 · 1/19 | -0.21 (-0.7) | +0.10 (0.5) | -10.7 / -9.6 | 11.9 / 12.3 |
| L2 EMA hb | 89 / 89 | 61 / 63 | -2.7 / -2.8 | -3.27 / -8.61 | -1.49 (-1.8) | -1.82 (-2.2) | 0/19 · 0/19 | -0.17 (-0.2) | -0.00 (-0.0) | -15.6 / -14.3 | 18.7 / 18.6 |
| K EMA mb | 10 / 8 | 37 / 38 | +0.0 / +0.0 | -0.05 / -0.15 | -0.00 (-0.0) | -0.11 (-1.9) | 5/15 · 4/14 | +0.02 (0.3) | -0.05 (-1.0) | -11.7 / -11.3 | 19.5 / 19.4 |
| L2 EMA mb | 30 / 29 | 55 / 58 | -1.8 / -1.6 | -1.25 / -0.95 | -0.58 (-1.3) | -0.40 (-1.4) | 2/19 · 2/19 | -0.16 (-0.4) | +0.15 (0.6) | -17.8 / -17.5 | 37.7 / 36.6 |
| L2 EMA ketat | – / – | – / – | – / – | -0.91 / -0.73 | -0.40 (-1.3) | -0.30 (-1.2) | 2/19 · 2/19 | -0.08 (-0.3) | +0.11 (0.5) | -18.3 / -18.1 | 39.9 / 38.5 |
| K HHHL hb | 17 / 17 | 47 / 47 | +0.0 / +0.0 | -0.21 / -0.87 | -0.00 (-0.0) | -0.20 (-2.6) | 7/18 · 1/17 | +0.04 (0.5) | -0.07 (-1.0) | -11.9 / -11.4 | 18.4 / 18.3 |
| L2 HHHL hb | 51 / 50 | 54 / 52 | -1.0 / -0.6 | -0.95 / -5.83 | -0.31 (-1.3) | -1.01 (-2.6) | 2/19 · 0/19 | +0.19 (0.9) | -0.30 (-0.9) | -18.5 / -18.3 | 35.9 / 34.3 |
| K HHHL mb | 9 / 9 | 51 / 49 | -0.2 / +0.0 | -0.20 / -0.48 | -0.06 (-0.5) | -0.23 (-2.9) | 4/18 · 0/19 | -0.02 (-0.2) | -0.12 (-1.6) | -11.9 / -11.4 | 18.7 / 18.5 |
| L2 HHHL mb | 25 / 24 | 60 / 60 | -2.8 / -2.5 | -0.72 / -4.54 | -0.25 (-0.9) | -0.88 (-2.6) | 2/19 · 0/19 | +0.13 (0.5) | -0.32 (-1.0) | -19.2 / -18.9 | 38.5 / 36.3 |
| L2 HHHL ketat | – / – | – / – | – / – | -0.41 / -3.71 | -0.11 (-0.7) | -0.51 (-1.9) | 6/19 · 2/19 | +0.15 (1.0) | -0.12 (-0.5) | -19.4 / -19.3 | 40.9 / 38.8 |
| K ST hb | 25 / 25 | 43 / 37 | +0.0 / +0.0 | -0.15 / -1.23 | -0.01 (-0.2) | -0.31 (-3.0) | 10/19 · 0/19 | +0.04 (0.4) | -0.15 (-1.6) | -11.9 / -11.3 | 18.0 / 17.8 |
| L2 ST hb | 86 / 83 | 46 / 45 | +0.0 / +0.0 | -0.73 / -7.11 | -0.20 (-0.7) | -1.37 (-3.3) | 4/19 · 0/19 | +0.26 (1.0) | -0.67 (-1.8) | -18.2 / -17.9 | 36.8 / 34.3 |
| L2 ST ketat | – / – | – / – | – / – | -0.72 / -7.10 | -0.19 (-0.7) | -1.37 (-3.3) | 4/19 · 0/19 | +0.25 (1.0) | -0.69 (-1.8) | -18.3 / -18.1 | 37.1 / 34.6 |
| K ADX hb | 37 / 36 | 59 / 56 | -1.6 / -0.9 | -0.53 / -1.53 | -0.19 (-0.9) | -0.44 (-2.6) | 3/19 · 0/19 | -0.06 (-0.3) | -0.06 (-0.4) | -11.3 / -10.5 | 14.2 / 14.6 |
| L2 ADX hb | 76 / 76 | 59 / 59 | -2.2 / -1.8 | -2.68 / -7.91 | -1.21 (-1.7) | -1.67 (-2.6) | 1/19 · 0/19 | -0.21 (-0.3) | -0.32 (-0.6) | -17.8 / -16.8 | 25.4 / 25.3 |
| K ADX mb | 30 / 30 | 58 / 53 | -1.4 / -0.5 | -0.34 / -1.25 | -0.08 (-0.4) | -0.31 (-2.4) | 6/19 · 1/19 | +0.02 (0.1) | -0.01 (-0.1) | -11.6 / -10.9 | 15.8 / 15.9 |
| L2 ADX mb | 67 / 69 | 59 / 57 | -1.9 / -1.4 | -1.95 / -7.19 | -0.80 (-1.6) | -1.33 (-2.5) | 1/19 · 0/19 | -0.04 (-0.1) | -0.26 (-0.6) | -18.2 / -17.5 | 30.5 / 29.1 |
| L2 ADX ketat | – / – | – / – | – / – | -1.63 / -7.09 | -0.64 (-1.6) | -1.28 (-2.6) | 2/19 · 0/19 | +0.01 (0.0) | -0.36 (-0.8) | -18.5 / -17.9 | 32.9 / 31.2 |
| K MULA hb | 37 / 36 | 61 / 61 | -1.6 / -1.3 | -0.69 / -1.47 | -0.28 (-1.4) | -0.43 (-2.7) | 3/19 · 1/17 | -0.15 (-0.8) | -0.03 (-0.2) | -11.2 / -10.5 | 14.4 / 14.4 |
| L2 MULA hb | 86 / 83 | 62 / 64 | -2.5 / -2.5 | -2.84 / -8.54 | -1.32 (-1.8) | -1.95 (-2.7) | 0/19 · 0/19 | -0.21 (-0.3) | -0.40 (-0.6) | -16.2 / -15.8 | 23.1 / 22.3 |
| K MULA mb | 26 / 26 | 59 / 56 | -1.3 / -0.7 | -0.25 / -0.99 | -0.06 (-0.5) | -0.22 (-2.3) | 6/17 · 1/17 | +0.02 (0.1) | -0.00 (-0.0) | -11.7 / -11.0 | 17.0 / 16.9 |
| L2 MULA mb | 77 / 75 | 60 / 64 | -2.0 / -2.2 | -2.03 / -7.09 | -0.86 (-1.7) | -1.19 (-2.0) | 1/19 · 0/19 | +0.02 (0.0) | -0.01 (-0.0) | -16.7 / -16.0 | 27.9 / 27.5 |
| L2 MULA ketat | – / – | – / – | – / – | -1.68 / -7.00 | -0.66 (-1.5) | -1.20 (-2.1) | 2/19 · 0/19 | +0.11 (0.3) | -0.16 (-0.3) | -17.2 / -16.7 | 30.2 / 29.5 |

- Versi aritmetik ([analisis.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis.py), [hasil_IS.txt / hasil_OOS.txt](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/hasil_OOS.txt)): L2 + D10 hilang Bull Δ purata −0.48% (t −2.3) IS, −0.78% (t −1.6) OOS; sebulan 2.69% lawan 2.42% (IS), 6.15% lawan 5.44% (OOS); laras masa aritmetik +0.50 (t 3.3) IS, +1.24 (t 2.8) OOS; baki sebulan selepas peristiwa 0.90% (IS) dan 3.25% (OOS) lawan kadar asas 2.42% / 5.44%. Bagi L2 + ST flip, laras masa aritmetik OOS −4.53 (t −2.0).
- Semakan berat dagangan (bukan kaedah) dan ikut kaedah: K D10 hb Δ log −0.04 (t −1.6) IS, −0.06 (t −2.3) OOS; L2 D10 hb −0.13 (t −1.1), −0.27 (t −2.1); L2 MULA hb −1.03 (t −1.7), −1.12 (t −2.6); negatif bagi hampir semua kaedah ([tambahan.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/tambahan.py)).
- Portfolio 8 slot enjin (modal dipusing; median 19 kaedah, [portfolio.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/portfolio.py)): L2 CAGR H1 19.9%, H2 33.9%, MDD −37.1%; L2 + D10 hilang Bull 17.0%, 28.5%, −36.9% (lebih baik dalam 9/19 kaedah H1, 7/19 H2; MDD lebih baik 11/19); L2 + ST flip 20.4%, 25.5%, −36.4% (11/19 H1, 5/19 H2).
- Rujukan reka bentuk lorong 2: median dagangan negatif dan untung datang daripada sebilangan kecil trend besar; henti kaedah dalam lorong 2 memotong 33% trend besar ([kajian/KAJIAN_LORONG2.md](/home/user/papertrade-claude/BacktestShariah2/kajian/KAJIAN_LORONG2.md)).

### Inferences
- Keputusan pegang/jual tidak patut dicetus oleh perubahan status: jual pada flip menukar beberapa kerugian kecil dengan kehilangan beberapa trend besar, dan secara purata itu rugi; 5% terburuk hanya baik sedikit (cth. L2 D10 hb −18.7/−18.1% lawan −20.0/−19.8%).
- Satu-satunya hujah untuk keluar berasaskan status ialah kecekapan modal dalam portfolio terhad slot, dan itu bergantung pada andaian kadar pelaburan semula; simulasi slot sebenar tidak menyokongnya.

### Gaps
- Tidak diuji: keluar separa (jual separuh pada flip), atau gabungan flip dengan syarat lain (cth. Bear + umur posisi); sengaja tidak ditambah selepas OOS untuk elak pencarian berlebihan.
- Portfolio 8 slot sangat bergantung laluan (path-dependent); keputusan per kaedah berselerak.

## 5. Definisi mana paling berguna, dan perubahan status mana patut dipapar kepada pengguna?

### Takeaway
Paparkan satu label jangka panjang (cadangan: **D10 dengan pengesahan 2 tutup**, Bullish/Neutral/Bearish; WST setara dalam ujian risiko) sebagai **maklumat risiko dan konteks**, bersama "sejak bila" (tarikh bertukar, bilangan hari, % sejak bertukar). Paparkan perubahan "hilang Bullish" dan "masuk Bearish" sebagai berita, dengan teks jelas bahawa ia bukan isyarat jual. Jangan jadikan sebarang status atau flip sebagai peraturan keluar/amaran; kekalkan lorong 1 dan lorong 2.

### Cited Findings
- D10 dan WST sama kuat bagi risiko jatuh 10 sesi (posisi: D10 −2.6/−2.4 mata, WST −3.8/−2.1, MTT −3.6/−1.4; tanpa syarat D10 +6.0/+3.7, WST +5.7/+3.4 mata Bear − Bull) ([analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py), [risiko_wst.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/risiko_wst.py)). D10 lebih jarang Bull (29% lawan 43%) dan berlarian lebih panjang (31.7 lawan 29.1 hari) ([status.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/status.py)).
- Umur D10 Bull > 60 hari: masuk baharu lemah ~1.3% (t −2.2 / −1.8); posisi terbuka risiko jatuh +2.4 hingga +3.3 mata dalam OOS (t 2.5–2.6), sama tanda tetapi tidak signifikan dalam IS ([analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py), [tambahan.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/tambahan.py)).
- Flip tidak diikuti baki pulangan lebih rendah, dan risiko selepas flip lebih rendah (Bahagian 3; [analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py)); keluar pada flip menurunkan purata log dalam 43/43 peraturan, IS dan OOS (Bahagian 4; [analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py)).
- "Mula naik/turun" (MULA) dan EMA20/50 bertukar setiap 7–11 hari; selepas "mula turun" baki log +1.12 (t 3.7) IS / +0.10 (t 0.3) OOS dan risiko jatuh −3.0 / −2.2 mata (t −2.4 / −2.7) berbanding posisi sebaya ([analisis2.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend3/analisis2.py)).

### Inferences
- **Cadangan paparan (Posisi dan Watchlist)**:
  1. Pill utama D10 (2 tutup): "Bullish sejak 3 Sep (34 hari, +18%)". Jika umur > 60 hari, tambah "trend lewat" (bukti: masuk baharu lebih lemah, risiko jatuh lebih tinggi dalam OOS).
  2. Teks risiko relatif, bukan arahan: Bearish = "lebih mudah jatuh tajam berbanding saham lain bulan ini" (beza ~2–4 mata pada asas ~20–24%).
  3. Perubahan status yang dipapar: "hilang Bullish" (Bull → Neutral) dan "masuk Bearish", masing-masing dengan tarikh dan tutup hari bertukar. Teks tetap: "Maklumat, bukan isyarat jual: dalam backtest, menjual pada perubahan ini menurunkan purata pulangan; keluar ikut lorong 1/lorong 2."
  4. "Mula naik / mula turun": jika mahu dipapar untuk menjawab "dari mana mula naik", gunakan pivot rendah/tinggi terakhir yang disahkan (zigzag 2×ATR14 dalam `status.py`) sebagai tarikh dan harga titik mula, sebagai teks deskriptif sahaja; jangan warnakan sebagai amaran (bukti: flip jangka pendek diikuti lantunan atau tiada kesan, risiko lebih rendah).
  5. Jangan papar Supertrend, ADX atau EMA20/50 sebagai label Bullish/Bearish: larian pendek, "Bull" jangka pendek bermakna risiko jatuh LEBIH TINGGI (+0.8 hingga +2.9 mata), dan kesan masuk tidak bertahan OOS.
- Kesan pada keputusan pengguna: label membantu memilih posisi mana perlu dipantau rapat dan menerangkan konteks, tetapi keputusan jual kekal pada peraturan kaedah dan Chandelier lorong 2.

### Gaps
- Tidak diuji kesan label terhadap tingkah laku pengguna sebenar (risiko pengguna menjual awal kerana label merah); teks "bukan isyarat jual" dicadangkan untuk mengurangkannya.
- Pivot "mula naik" (tarikh/harga) hanya dicadangkan untuk paparan; kuasa ramalnya tidak diuji selain melalui status HHHL (yang tiada kesan konsisten).
- WST lawan D10: beza kecil; pilihan D10 berdasarkan kesinambungan dengan kajian terdahulu dan bahagian Bull yang lebih ketat, bukan bukti keunggulan.
