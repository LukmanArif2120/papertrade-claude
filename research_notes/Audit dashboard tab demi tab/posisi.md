# Audit tab Posisi dashboard (Papertrade C · Moomoo lama · Gabung), 24 Okt 2026

Skop: tab **Posisi** dalam `BacktestShariah2/standard/dashboard_v2.html` (v103). Ini merangkumi akaun C, M dan Gabung; pandangan Ringkas, Penuh, Risiko dan Gred; kad telefon; helaian butiran (termasuk carta lilin dan ulang tayang lorong 2); Peta portfolio; panel Isyarat tidak dibeli; dan KPI kepala. Panel "Isyarat lengkap dalam watchlist" sebenarnya terletak dalam tab Watchlist (`renderWatch`, [dashboard_v2.html:1333](BacktestShariah2/standard/dashboard_v2.html)), bukan Posisi, jadi ia tidak diaudit di sini.

Sesi AS terkini ialah Jumaat 2026-10-23. Audit ini baca sahaja: repo, db dan Moomoo tidak diubah. Untuk semakan, saya hanya membaca `quote_history_kline` Moomoo bagi 6 saham.

Bukti dan cara semakan semula (scratchpad):
- Salinan db: `/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/audit_posisi/db/`. Senarainya: papertrade/ringkas_c (+_2.._7, _kamus_1..4) v7/v4/v3/v1, ringkas_m v6, prestasi/garis v6, mae v19, mfe v6, mae_atr v2, ringkasan v18, posisi/lorong2 (+_2.._9), harian/trend v4 dan harian/status v41. Semua `dibina` 2026-10-24 06:30 MYT.
- `skrip/nyahkod.py` menyahkod ringkas_c/m sama seperti `nyahkod()` halaman ([dashboard_v2.html:3790-3796](BacktestShariah2/standard/dashboard_v2.html)).
- `skrip/banding.py` membandingkan db dengan `jana_db.py` yang dijana semula daripada CSV HEAD `c0adf74`.
- `skrip/semak.py`, `semak2.py` dan `semak3.py` menyemak semua baris: untung, hari, harga, lorong 1, lorong 2 Chandelier (dikira sendiri), MAE dan MFE.
- `skrip/kpi.py` mereplika `ptKpis`/`hasilL`. `skrip/sampel.py` menghasilkan jadual sampel 39 posisi.
- Rujukan harga bebas ialah stor repo (yfinance hingga 2026-10-22) ditambah bar 23 Okt daripada `data/harga/terkini.csv`. Bagi 31 ticker yang tiada bar yfinance 23 Okt, saya memakai bar rutin dalam db `posisi/lorong2`.

## 1. Adakah nilai yang dipapar betul? (untung %, harga terkini, hari, lorong 1, lorong 2, R/risiko/ke henti, MAE/MFE, 📅, trend/ATR, gred)

### Takeaway
Hampir semua nilai sepadan dengan data sumber. Data db sama tepat dengan CSV repo, dan pengiraan halaman konsisten merentasi 5,855 baris dibeli. Ada beberapa ralat sebenar:
- **(a)** DAC M80/M90 (beli 12 Okt) direkod dengan harga_beli 164.162, sedangkan buka rasmi ialah 170.19. Untung menjadi lebih baik sebanyak 3.4–3.5 mata.
- **(b)** Lorong 2 VIAV dan LITE (Moomoo lama, S04V2) keluar seminggu lewat dalam CSV, dan nilainya sudah dibekukan. Carta lilin dalam helaian yang sama menunjukkan tarikh keluar yang betul.
- **(c)** Ikon 📅 memakai tarikh earnings hari isyarat, bukan tarikh sebenar. Akibatnya 114 posisi (26 saham) tiada ikon walaupun earnings ≤ 10 hari, dan 32 posisi (4 saham) diberi ikon palsu.
- **(d)** ACA ialah saham yang sudah diambil alih (CRH, tunai USD150, selesai 23 Okt). Ia tidak ditanda `tidak_sah`, dan harga 23 Okt ialah bar sintetik.
- **(e)** Lajur `sasaran` bagi M03/M28/M01 ialah paras hari isyarat, bukan sasaran sebenar yang dipakai semasa keluar.
- Selain itu ada beberapa label yang salah (lihat bahagian 2 dan 5).

### Cited Findings

**Kesepadanan db lawan repo (semua baris)**
- Nyahkod `papertrade/ringkas_c` (5,711 baris; 7 bahagian, 4 kamus, induk `4e22db8f2ae9`) dan `ringkas_m` (208 baris), dibanding medan demi medan dengan `jana_db.py` yang dijana semula daripada `claude*.csv`/`moomoo.csv` HEAD `c0adf74`: **0 kunci berbeza, 0 medan berbeza**. — [jana_db.py:217-249 `ringkas_pt`](BacktestShariah2/standard/jana_db.py); [db papertrade/ringkas_c](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)
- `prestasi/ringkasan` C: dagangan 5,525, untung_purata 1.77, kadar_menang 59.7, keluar 1,366. Replika `ptKpis` dalam Python memberi angka yang sama: sah 5,525, purata +1.77, keluar 1,366, sedang untung 3,299/5,525. — [jana_db.py:84-138](BacktestShariah2/standard/jana_db.py); [dashboard_v2.html:1471-1478](BacktestShariah2/standard/dashboard_v2.html)

**Untung %, harga terkini dan hari (semua 5,855 baris dibeli, C + M)**
- `untung_pct` = (harga_terkini/harga_beli − 1)×100 dalam toleransi 0.02: 0 pengecualian. Bagi baris `keluar`: harga_terkini = harga_keluar dan untung_pct = untung_akhir_pct, juga 0 pengecualian. Halaman memapar `r.untung_pct`, dan `normPT` menggantikan harga terkini dengan harga keluar. — [dashboard_v2.html:1372-1381 `normPT`, 1464](BacktestShariah2/standard/dashboard_v2.html)
- Harga terkini posisi terbuka lawan tutup yfinance 23 Okt: 0 beza > 0.005 bagi semua ticker yang ada bar. 164 posisi terbuka (31 ticker) tiada bar yfinance 23 Okt (`data/harga/status.json` `tiada_bar_sesi`), jadi harganya diambil daripada skrin Moomoo oleh rutin 6:02 ("Gabungan yfinance dilangkau"). Dua daripadanya bar rata sintetik (O=H=L=C = tutup sebelum): **ACA 149.15** dan **FEDU 10.48**. — [data/harga/status.json](BacktestShariah2/data/harga/status.json); [binaan_v2_log_tambahan.md:307](BacktestShariah2/standard/binaan_v2_log_tambahan.md); db `posisi/lorong2` ACA|2026-10-12 bar 1023 `[149.15,…,149.15,149.15,149.15]`
- Kline Moomoo ACA (autype 0) hanya sampai 2026-10-22 (tiada bar 23 Okt). — Moomoo `quote_history_kline` US.ACA 20–23 Okt (dibaca 24 Okt)
- Hari (terbuka): `r.hari` sama dengan kiraan hari dagangan dari tarikh_beli hingga 23 Okt bagi semua baris. Bagi baris keluar, jadual memakai `hariAntara(tarikh_beli, tarikh_keluar)`, tetapi kad telefon memakai `r.hari` CSV. Kedua-duanya berbeza bagi 10 baris ATKR (M11, M66, M36, M54, M95, M100 …; jadual 1, kad 2). — [dashboard_v2.html:2396 `hariSel`, 2189-2191 `kadPos`](BacktestShariah2/standard/dashboard_v2.html)

**Harga beli**
- Bagi baris C, harga_beli lawan buka yfinance pada hari beli: 21 baris berbeza > 0.3%. 15 daripadanya dibeli 23 Okt (contoh ZYME M34/M89 28.77 lawan 27.28; NEOG 11.97 lawan 11.82; KARO 63.67 lawan 64.45), 2 baris DAC 12 Okt, RMR M99 13 Okt, dan SENEB/WLYB 13 Okt (direkod lewat).
- Saya menyemak dengan kline Moomoo. ZYME 23 Okt buka **28.77** (rendah 27.28). Ini bermakna yfinance meletakkan rendah sebagai buka, dan harga_beli dashboard betul ikut SKEMA ("open kline harian rasmi"). — Moomoo `quote_history_kline` US.ZYME; [SKEMA.md](BacktestShariah2/papertrade/SKEMA.md)
- **RALAT:** DAC M80 dan DAC M90 (tarikh_beli 2026-10-12, sumber `penuh_20261012`) ada harga_beli **164.162**. Buka rasmi 12 Okt ialah **170.19** (Moomoo kline autype 0 dan yfinance sepakat; rendah hari itu 169.25, jadi 164.162 tidak pernah didagangkan). Nilai sebenar:
  - M80: untung_akhir dipapar −4.27%, sebenar −7.66%.
  - M90: −1.84%, sebenar −5.32%.
  - Lorong 2 (masih dipegang): dipapar −3.55%, sebenar −6.96%.
  - Tiada nota `faktor` bagi DAC dalam `data/harga/faktor.csv`. — Moomoo `quote_history_kline` US.DAC 9–13 Okt; [data/harga/faktor.csv](BacktestShariah2/data/harga/faktor.csv)
- `sahkan.py` tidak menyemak harga_beli lawan buka bar hari beli. Ia hanya menyemak bentuk dan konsistensi untung. `keluar_lorong.py` hanya melangkau baris yang berbeza > 15% (`BEZA_HARGA_MAKS`), jadi DAC (3.5%) lolos. — [sahkan.py:119-145](BacktestShariah2/standard/sahkan.py); [keluar_lorong.py:30](BacktestShariah2/standard/keluar_lorong.py)
- Belian 23 Okt dengan harga sementara: semua 760 baris dibeli bertanda "buka rasmi kline 23 Okt (disahkan 6:02 MYT)". MTX M19 (63.49) dan STVN M99 (19.46), yang "belum didagangkan pada 9:35", sudah diganti dengan buka rasmi. 42 baris yang masih bertanda "buka sementara" semuanya `tidak_dibeli`. — [binaan_v2_log_tambahan.md:299](BacktestShariah2/standard/binaan_v2_log_tambahan.md)
- Bagi Moomoo lama, harga_beli = harga isian sim (bukan buka), contohnya SNDK 1643.505 lawan buka 1669.49 dan AMD 632.82 lawan 639.36. Tooltip `harga_beli` ("Harga isian purata order beli") betul bagi M, tetapi **salah bagi C** (C memakai buka rasmi). — [dashboard_v2.html:3586](BacktestShariah2/standard/dashboard_v2.html)

**Lorong 1 (keluar kaedah)**
- Harga keluar disemak lawan bar hari keluar:
  - Isyarat keluar: 390 disemak, 388 = buka. AVPT M82 16.04 dan GRAL M153 128.115 berbeza daripada buka yfinance (16.01, 127.09); kline Moomoo GRAL buka 128.115, jadi CSV betul.
  - Kena henti: 946 disemak, 944 = min(buka, henti). TTC M49 95.44 lawan henti direkod 95.24 (rendah 95.35 tidak sampai henti; kemungkinan henti mengekor). FRD M55 40.16 = henti, manakala buka yfinance 40.08; kline Moomoo FRD buka 40.24 > henti, jadi CSV betul. — skrip `semak2.py`; Moomoo `quote_history_kline` US.FRD, US.GRAL
- Capai sasaran: 138 disemak. **37 tidak sepadan** dengan max(buka, sasaran direkod) (M03 30, M28 4, M01 3), dan 22 keluar *di bawah* sasaran direkod. Contohnya KBH M01 13 Okt keluar 45.91, sasaran direkod 47.98, tinggi hari itu 46.28. 38 lagi keluar "capai sasaran" dengan `sasaran` kosong (M03 16, M20 8, M02 6, M26 5, M18 2, M19 1). Lajur `sasaran` = paras enjin hari isyarat (SKEMA), tetapi kaedah ini memakai sasaran dinamik. Kad telefon (`mkLorong`) dan teks "Pegang (henti X, sasaran Y)" memapar sasaran statik bagi 58 posisi M01/M03/M28 yang masih terbuka. — [dashboard_v2.html:2167-2179 `mkLorong`](BacktestShariah2/standard/dashboard_v2.html); [SKEMA.md](BacktestShariah2/papertrade/SKEMA.md)
- Posisi lorong 1 terbuka: 4,073 dengan henti disemak, dan **0** yang rendah sejak beli ≤ henti (M31: 0 tutup < henti). Jadi tiada keluar henti yang tertinggal. Teks henti dalam `isyarat_keluar` sama dengan lajur `henti` bagi semua 4,048 baris terbuka. — skrip `semak2.py`
- "Dibekukan" tidak mutlak. Sejak 21 Okt, 7 keluar lorong 1 sudah dibatalkan semula: RMR M99 (faktor dividen 0.975437), DT/PSX/DHT M82, TRMB M20, DELL/UMC M81 (oleh `dagangan.py betul`, kaedah replika). Ini ikut reka bentuk 22 Okt, tetapi tiada tanda pada halaman selain `nota`. — [binaan_v2_log_tambahan.md:306](BacktestShariah2/standard/binaan_v2_log_tambahan.md); [data/harga/faktor.csv:3](BacktestShariah2/data/harga/faktor.csv)

**Lorong 2 (pegang selagi naik)**
- Chandelier dikira sendiri (puncak tutup − 4×ATR14, paras hanya naik, jual buka esok) bagi 5,725 baris sah:
  - Status Pegang: paras dan puncak sama dalam 0.011, kecuali 262 baris dengan beza kecil (median 0.02%, p90 0.09%) akibat bar Moomoo lawan yfinance.
  - Status keluar: 12 berbeza. 10 daripadanya pada 23 Okt hanya kerana buka Moomoo lawan yfinance (SILC 37.17, disahkan kline Moomoo). **Dua ralat sebenar** diterangkan di bawah. — skrip `semak2.py`; [keluar_lorong.py:54-71](BacktestShariah2/standard/keluar_lorong.py)
- **RALAT:** M VIAV S04V2 2026-10-02. CSV: "Keluar: tutup 35.39 bawah paras keluar 37.51 pada 21 Okt (22 Okt @ 33.40)", untung_henti −27.53%. Kira semula: tutup 14 Okt 38.55 < paras 38.62, jual 15 Okt @ 36.88, iaitu −19.98% atas harga isian 46.09. Db `posisi/lorong2` VIAV|2026-10-02 sendiri menunjukkan `bawah` 1014 dan `jual` 1015 @ 36.88. Jadi dalam helaian yang sama, seksyen "Pegang selagi naik (lorong 2)" bercanggah dengan carta lilin dan ulang tayang.
- **RALAT:** M LITE S04V2 2026-10-02. CSV: keluar 22 Okt @ 804.06 (−22.93%). Siri db dan kira semula: jual 16 Okt @ 853.485 (−18.19%).
- Punca VIAV dan LITE: paras 37.51 sepadan dengan ATR yang hanya bermula 14 bar *selepas* beli. Lorong 2 dikira dengan stor kerja yang tiada sejarah sebelum beli bagi ticker bukan Shariah ini (VIAV/LITE diambil melalui kline sahaja; log "kline bagi … LITE … VIAV"). Lorong 2 yang sudah keluar dibekukan oleh `kemas_baris`, jadi nilai ini tidak akan dibetulkan tanpa `--semula henti`. — [keluar_lorong.py:140-160](BacktestShariah2/standard/keluar_lorong.py); [binaan_v2_log_tambahan.md:188,213,246,278](BacktestShariah2/standard/binaan_v2_log_tambahan.md)
- Selain dua baris itu, siri `posisi/lorong2` sepadan dengan CSV bagi 5,723 baris: 5,573 Pegang tanpa `bawah`/`jual`, 135 keluar pada tarikh dan harga sama, dan 15 menunggu. — skrip semakan siri
- BKHA M76 2026-10-14 (`tidak_sah`, tidak cair): lorong 2 "Pegang (paras keluar −0.06; puncak 7.74)". Paras negatif ini betul dari segi aritmetik (ATR14 46% bagi saham tidak cair), tetapi tidak bermakna.

**R, risiko awal dan jarak ke henti**
- `riskAwal` = (1 − henti/harga_beli)×100 jika henti < harga_beli. `rOf` = untung ÷ risiko, dan disembunyikan jika risiko < 0.5%. — [dashboard_v2.html:2634-2639](BacktestShariah2/standard/dashboard_v2.html)
- Lajur `henti` hampir statik sejak 21 Okt: hanya 8 perubahan > 0.01, iaitu faktor (RMR) dan kaedah replika/isi semula. Jadi R memang memakai henti awal, sama seperti tooltip. — [dashboard_v2.html:3513](BacktestShariah2/standard/dashboard_v2.html)
- R tidak dipapar bagi 287 baris tanpa henti (M82 117, M73 111, M01 38, M31 10, S04V2 5, BandWalk 4, MANUAL 2), 83 baris dengan risiko < 0.5% (contoh TECH M14 0.07%, WDAY M13 0.08%), dan 4 baris M dengan henti ≥ harga isian (AMD M70, SWKS M57, SBH M49, RYAAY M18).
- ACA M95/M54 (risiko 0.6%) memapar R +2.65 bagi untung +1.46%. Ini R besar yang tidak bermakna, daripada saham yang harganya terkunci.

**MAE / MFE**
- Dikira semula untuk 5,855 posisi (rendah atau tinggi dari hari beli hingga sehari sebelum keluar lorong 1, ditambah harga keluar): MAE 63 beza > 0.05 mata, MFE 94 beza. Hampir semuanya belian 23 Okt (bar Moomoo lawan yfinance, contoh URBN −3.02 lawan −2.76) dan RMR M99 (faktor). MAE dan MFE berhenti pada keluar lorong 1, jadi bagi **1,348** posisi yang masih dipegang dalam lorong 2 ia tidak meliputi tempoh pegangan lorong 2. — [jana_db.py:141-166, 252-299](BacktestShariah2/standard/jana_db.py); skrip `semak3.py`

**📅 Earnings**
- `earnH` memakai `r.tarikh_earnings`, iaitu rekod hari isyarat. `earn_seb` (tarikh sebenar daripada kalendar gabungan, `jana_db.earn_sebenar`) hanya dipapar dalam sel QR melalui `qrSeb`. — [dashboard_v2.html:2371-2373, 3275-3276](BacktestShariah2/standard/dashboard_v2.html); [jana_db.py:52-72](BacktestShariah2/standard/jana_db.py)
- Kesan bagi 5,632 posisi yang belum `tutup_semua`:
  - 3,991 (71%) memapar 📅.
  - **114 posisi (26 saham) tiada ikon** walaupun earnings sebenar ≤ 10 hari. Contoh: CRSR 5 Nov, FRPT 4 Nov, SIBN 2 Nov, RDNT 5 Nov, FRD 4 Nov, GRAL 4 Nov.
  - **32 posisi (4 saham) diberi ikon palsu**. SONO (rekod 4 Nov, sebenar 10 Nov), VIV (29 Okt lawan 10 Nov), DRD (SST 27 Okt lawan 17 Feb 2027) dan PSO (25 Okt, hari Ahad, lawan 25 Feb 2027).
  - CNXN M39 memapar 📅8 sedangkan sebenar 28 Okt (3 hari).
  - 245 posisi dengan tarikh_earnings yang sudah lalu tidak akan menunjukkan earnings seterusnya. — skrip semakan earnings

**Trend / ATR**
- `harian/trend` (tarikh 20261023, D10H2-r2): bagi 886 ticker dengan ≥ 200 bar, susunan mentah tutup/SMA50/150/200 sama 100% dengan kiraan saya. ATR14% sama dalam 0.02 kecuali 27 ticker (≤ 0.14 mata; bar 23 Okt Moomoo). 25 ticker ada `tarikh_data` < 23 Okt (6 pada 19 Okt, 4 pada 16 Okt, 2 pada 7 Okt, 2 pada 5 Okt), dan halaman menandanya "data <tarikh>". — [dashboard_v2.html:3253-3260 `trBaris`](BacktestShariah2/standard/dashboard_v2.html)
- ACA dipapar "Bullish lama · ATR 0.35% Q1". Pada hakikatnya harga terkunci pada tawaran tunai: julat harian 0.13–0.59% selama 40 sesi.

**Gred**
- `gred_keseluruhan` 39/39 dalam sampel sama dengan `gred.keseluruhan_baris` (Industri kecuali kaedah pantulan, Pemangkin, QR). Lajur gred memapar nilai CSV hari isyarat tanpa pengiraan halaman (selain `skPerf` 1B kini). — [standard/gred.py:876-891](BacktestShariah2/standard/gred.py); [dashboard_v2.html:1449-1456](BacktestShariah2/standard/dashboard_v2.html)

**Jadual sampel: 39 posisi.** Format setiap sel ialah "papar / kira bebas". "kira" memakai buka yfinance, jadi bagi M (harga isian) dan belian 23 Okt (buka rasmi Moomoo) beza kecil adalah perbezaan konvensyen; lihat lajur Keputusan.

| # | Posisi | Harga beli papar / buka yfinance | Untung % papar / kira | Hari papar / kira | R papar / kira | Lorong 1 papar · semakan bar | Lorong 2 papar · kira semula | MAE · MFE (papar / kira) | 📅 papar / ikut earn_seb | Trend · ATR doc · kira | Gred simpan / kira | Keputusan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C SSNC M02 2026-10-09 | 80.62 / 80.620 | +2.90 / +2.90 | 10 / 10 | 0.32 / 0.32 (risiko 9.0%) | Pegang · semak: – | Pegang paras 82.68 (+2.90) · kira: Pegang paras 82.68 (+2.90) | -1.18 / -1.18 · +11.40 / +11.40 | 📅−1 / 📅−1 (rekod 2026-10-22; sebenar 2026-10-22) | Neutral ATR 2.55 Q2 · mentah 0 (doc 0) ATR 2.55 | C / C | OK (M02 replika, terbuka) |
| 2 | C ACA M95 2026-10-12 (yf-tiada-1023) | 147.01 / 147.010 | +1.46 / +1.46 | 9 / 9 | 2.65 / 2.64 (risiko 0.6%) | Pegang · semak: – | Pegang paras 147.05 (+1.46) · kira: Pegang paras 147.05 (+1.46) | -0.10 / -0.10 · +1.50 / +1.50 | 📅4 / 📅4 (rekod 2026-10-29; sebenar 2026-10-29) | Bullish lama ATR 0.35 Q1 · mentah 1 (doc 1) ATR 0.35 | C / C | Nilai = data, TETAPI saham diambil alih (CRH, tutup 23 Okt); bar 23 Okt sintetik O=H=L=C=149.15; patut tidak_sah |
| 3 | C DAC M39 2026-10-09 | 170.97 / 170.970 | -7.39 / -7.39 | 10 / 10 | -0.48 / -0.48 (risiko 15.4%) | Pegang · semak: – | Pegang paras 152.75 (-7.39) · kira: Pegang paras 152.75 (-7.39) | -9.34 / -9.34 · +1.05 / +1.05 | - / - (rekod 2026-11-16; sebenar 2026-11-16) | Bullish lama ATR 2.69 Q2 · mentah 1 (doc 1) ATR 2.69 | B / B | OK |
| 4 | C APA M31 2026-10-14 | 48.53 / 48.530 | +6.94 / +6.94 | 7 / 7 | 0.44 / 0.44 (risiko 15.6%) | Pegang · semak: – | Pegang paras 45.23 (+6.94) · kira: Pegang paras 45.23 (+6.94) | -4.12 / -4.12 · +7.95 / +7.95 | 📅8 / 📅8 (rekod 2026-11-04; sebenar 2026-11-04) | Bullish lama ATR 3.21 Q3 · mentah 1 (doc 1) ATR 3.21 | B / B | OK (M31 henti tutup) |
| 5 | C NEO M82 2026-10-13 | 16.3 / 16.300 | +1.78 / +1.78 | 8 / 8 | – / – (risiko –) | Pegang · semak: – | Pegang paras 13.36 (+1.78) · kira: Pegang paras 13.36 (+1.78) | -1.96 / -1.96 · +7.06 / +7.06 | 📅3 / 📅3 (rekod 2026-10-28; sebenar 2026-10-28) | Neutral ATR 5.86 Q5 · mentah 0 (doc 0) ATR 5.86 | B / B | OK (tiada henti → R "tiada henti") |
| 6 | C SNPS M73 2026-10-08 | 501.47 / 501.470 | -14.22 / -14.22 | 11 / 11 | – / – (risiko –) | Pegang · semak: – | Keluar 23 Okt @ 419.42 (-16.36) · kira: Keluar 23 Okt @ 419.42 (-16.36) | -16.72 / -16.72 · +2.20 / +2.20 | - / - (rekod –; sebenar 2026-12-09) | Bearish baharu ATR 3.88 Q4 · mentah -1 (doc -1) ATR 3.88 | B / B | OK (L1 pegang, L2 keluar) |
| 7 | C APPF M11 2026-10-21 | 224.87 / 224.870 | -6.34 / -6.34 | 2 / 2 | -0.39 / -0.39 (risiko 16.5%) | Tunggu · semak: – | Pegang paras 180.80 (-6.34) · kira: Pegang paras 180.80 (-6.34) | -9.90 / -9.90 · +1.23 / +1.23 | 📅−1 / 📅−1 (rekod 2026-10-22; sebenar 2026-10-22) | Neutral ATR 4.76 Q4 · mentah 0 (doc 0) ATR 4.76 | C / C | OK (L1 menunggu) |
| 8 | C BE M08 2026-10-12 | 275.33 / 275.330 | -4.89 / -4.89 | 0 / 0 | -1.00 / -1.00 (risiko 4.9%) | Keluar 12 Okt @ 261.86 (-4.89) · semak: min(buka 275.33, henti 261.855) ; rendah 257.76 | Tunggu · kira: Tunggu (tutup 193.30 < 193.69) | -4.89 / -4.89 · +0.00 / +0.00 | 📅−1 / 📅−1 (rekod 2026-10-22; sebenar 2026-10-22) | Neutral ATR 10.16 Q5 · mentah 0 (doc 0) ATR 10.16 | C / C | OK (keluar hari beli; L2 menunggu) |
| 9 | C ZYME M34 2026-10-23 | 28.77 / 27.280 | -1.91 / +3.45 | 0 / 0 | -0.13 / 0.35 (risiko 14.5%) | Pegang · semak: – | Pegang paras 23.59 (-1.91) · kira: Pegang paras 23.59 (+3.45) | -5.18 / -5.18 · +0.00 / +0.00 | 📅9 / 📅9 (rekod 2026-11-05; sebenar 2026-11-05) | Bullish baharu ATR 4.1 Q4 · mentah 1 (doc 1) ATR 4.10 | D / D | Papar ikut buka rasmi Moomoo 28.77 (betul ikut SKEMA); buka yfinance 27.28 = rendah Moomoo (yfinance salah) |
| 10 | C NEOG M82 2026-10-23 | 11.97 / 11.820 | +1.84 / +3.13 | 0 / 0 | – / – (risiko –) | Pegang · semak: – | Pegang paras 9.63 (+1.84) · kira: Pegang paras 9.64 (+3.13) | -1.25 / -1.25 · +3.09 / +3.01 | - / - (rekod 2027-01-05; sebenar 2027-01-07) | Neutral ATR 5.24 Q5 · mentah 1 (doc 1) ATR 5.24 | B / B | Papar ikut Moomoo 11.97; yfinance 11.82 (sumber berbeza, tidak disahkan) |
| 11 | C KFRC M74 2026-10-23 (yf-tiada-1023) | 54.17 / 54.170 | +7.99 / +7.99 | 0 / 0 | 5.60 / 5.61 (risiko 1.4%) | Pegang · semak: – | Pegang paras 51.33 (+7.99) · kira: Pegang paras 51.33 (+7.99) | +0.00 / +0.00 · +8.14 / +8.14 | 📅1 / 📅1 (rekod 2026-10-26; sebenar 2026-10-26) | Bullish baharu ATR 3.07 Q2 · mentah 1 (doc 1) ATR 3.07 | C / C | OK (bar 23 Okt daripada Moomoo; yfinance tiada) |
| 12 | C ABT M15 2026-10-23 | 102.28 / 102.280 | +1.39 / +1.39 | 0 / 0 | 0.19 / 0.19 (risiko 7.3%) | Pegang · semak: – | Pegang paras 91.97 (+1.39) · kira: Pegang paras 91.98 (+1.39) | -0.70 / -0.70 · +1.68 / +1.64 | - / - (rekod 2027-01-20; sebenar –) | Neutral ATR 2.83 Q2 · mentah 0 (doc 0) ATR 2.83 | C / C | OK |
| 13 | C HP M02 2026-10-09 | 40.01 / 40.010 | -10.28 / -10.28 | 9 / 9 | -1.00 / -1.00 (risiko 10.3%) | Keluar 22 Okt @ 35.90 (-10.28) · semak: min(buka 38.35, henti 35.8967) ; rendah 35.78 | Pegang paras 34.43 (-2.65) · kira: Pegang paras 34.43 (-2.65) | -10.28 / -10.28 · +2.42 / +2.42 | - / - (rekod 2026-11-16; sebenar 2026-11-18) | Neutral ATR 3.77 Q3 · mentah 0 (doc 0) ATR 3.77 | B / B | OK (M02 replika, kena henti) |
| 14 | C DAC M80 2026-10-12 | 164.162 / 170.190 | -4.27 / -7.66 | 4 / 4 | -1.00 / -1.00 (risiko 4.3%) | Keluar 16 Okt @ 157.16 (-4.27) · semak: min(buka 159.85, henti 157.1557) ; rendah 156.66 | Pegang paras 152.75 (-3.55) · kira: Pegang paras 152.75 (-6.96) | -4.27 / -4.27 · +5.24 / +5.24 | - / - (rekod 2026-11-16; sebenar 2026-11-16) | Bullish lama ATR 2.69 Q2 · mentah 1 (doc 1) ATR 2.69 | B / B | RALAT harga_beli 164.162 ≠ buka rasmi 170.19 (Moomoo + yfinance); untung −4.27 → −7.66 |
| 15 | C DAC M90 2026-10-12 | 164.162 / 170.190 | -1.84 / -5.32 | 2 / 2 | -1.00 / -1.00 (risiko 1.8%) | Keluar 14 Okt @ 161.13 (-1.84) · semak: min(buka 164.79, henti 161.1338) ; rendah 159.39 | Pegang paras 152.75 (-3.55) · kira: Pegang paras 152.75 (-6.96) | -1.84 / -1.84 · +5.24 / +5.24 | - / - (rekod 2026-11-16; sebenar 2026-11-16) | Bullish lama ATR 2.69 Q2 · mentah 1 (doc 1) ATR 2.69 | B / B | RALAT sama; untung −1.84 → −5.32 |
| 16 | C KBH M01 2026-10-13 | 42.06 / 42.060 | +9.15 / +9.15 | 7 / 7 | – / – (risiko –) | Keluar 22 Okt @ 45.91 (+9.15) · semak: max(buka 43.14, sasaran 47.9763); tinggi 46.28 | Pegang paras 40.63 (+11.86) · kira: Pegang paras 40.63 (+11.86) | -2.71 / -2.71 · +9.15 / +9.15 | - / - (rekod –; sebenar 2026-12-17) | Bearish baharu ATR 3.41 Q3 · mentah -1 (doc -1) ATR 3.41 | B / B | Harga keluar 45.91 < sasaran direkod 47.98: sasaran M01 dinamik; lajur sasaran mengelirukan |
| 17 | C TX M06 2026-10-21 | 59.58 / 59.580 | -7.08 / -7.08 | 2 / 2 | -0.89 / -0.89 (risiko 8.0%) | Keluar 23 Okt @ 55.36 (-7.08) · semak: buka 55.36 | Pegang paras 51.77 (-6.08) · kira: Pegang paras 51.77 (-6.08) | -7.47 / -7.47 · +0.47 / +0.47 | 📅7 / 📅7 (rekod 2026-11-03; sebenar 2026-11-03) | Neutral ATR 3.28 Q3 · mentah 0 (doc 0) ATR 3.28 | C / C | OK |
| 18 | C FRD M55 2026-10-20 | 42.02 / 42.020 | -4.43 / -4.43 | 3 / 3 | -1.00 / -1.00 (risiko 4.4%) | Keluar 23 Okt @ 40.16 (-4.43) · semak: min(buka 40.08, henti 40.16) ; rendah 40.04 | Pegang paras 36.30 (-0.45) · kira: Pegang paras 36.30 (-0.45) | -4.43 / -4.43 · +1.71 / +1.71 | - / 📅8 (rekod 2026-11-09; sebenar 2026-11-04) | Neutral ATR 3.9 Q4 · mentah 0 (doc 0) ATR 3.90 | B / B | OK ikut Moomoo (buka 40.24 > henti); 📅 HILANG (earnings sebenar 4 Nov, 8 hari) |
| 19 | C GRAL M153 2026-10-22 | 133.13 / 133.130 | -3.77 / -3.77 | 1 / 1 | -0.31 / -0.31 (risiko 12.4%) | Keluar 23 Okt @ 128.12 (-3.77) · semak: buka 127.09 | Pegang paras 88.80 (-0.44) · kira: Pegang paras 88.80 (-0.44) | -7.41 / -7.41 · +0.58 / +0.58 | - / 📅8 (rekod 2026-11-11; sebenar 2026-11-04) | Neutral ATR 8.25 Q5 · mentah 0 (doc 0) ATR 8.25 | B / B | OK ikut Moomoo (buka 128.115); 📅 HILANG (sebenar 4 Nov) |
| 20 | C AVPT M82 2026-10-13 | 14.43 / 14.430 | +11.16 / +11.16 | 8 / 8 | – / – (risiko –) | Keluar 23 Okt @ 16.04 (+11.16) · semak: buka 16.01 | Pegang paras 14.05 (+14.41) · kira: Pegang paras 14.05 (+14.41) | -3.40 / -3.40 · +11.64 / +11.64 | 📅9 / 📅9 (rekod 2026-11-05; sebenar 2026-11-05) | Bullish baharu ATR 3.72 Q3 · mentah 1 (doc 1) ATR 3.72 | B / B | OK ikut Moomoo (replika M82) |
| 21 | C TRMB M20 2026-10-16 | 61.2 / 61.200 | +3.74 / +3.74 | 5 / 5 | 0.94 / 0.94 (risiko 4.0%) | Pegang · semak: – | Pegang paras 57.02 (+3.74) · kira: Pegang paras 57.02 (+3.74) | -3.59 / -3.59 · +4.77 / +4.77 | 📅8 / 📅8 (rekod 2026-11-04; sebenar 2026-11-04) | Neutral ATR 2.75 Q2 · mentah 0 (doc 0) ATR 2.75 | C / C | OK (keluar L1 21 Okt dibatalkan semula oleh dagangan.py) |
| 22 | C SAIL M08 2026-10-12 | 20.89 / 20.890 | -6.32 / -6.32 | 1 / 1 | -0.78 / -0.78 (risiko 8.1%) | Keluar 13 Okt @ 19.57 (-6.32) · semak: buka 19.57 | Pegang paras 17.28 (+4.31) · kira: Pegang paras 17.28 (+4.31) | -7.66 / -7.66 · +1.01 / +1.01 | - / - (rekod –; sebenar 2026-12-15) | Bullish baharu ATR 5.18 Q5 · mentah 1 (doc 1) ATR 5.18 | B / B | OK |
| 23 | C AMSC M08 2026-10-08 | 31.14 / 31.140 | -10.35 / -10.35 | 4 / 4 | -1.00 / -1.00 (risiko 10.3%) | Keluar 14 Okt @ 27.92 (-10.35) · semak: min(buka 28.00, henti 27.918) ; rendah 25.38 | Keluar 23 Okt @ 24.54 (-21.19) · kira: Keluar 23 Okt @ 24.50 (-21.32) | -10.35 / -10.35 · +2.63 / +2.63 | - / - (rekod 2026-11-04; sebenar 2026-11-04) | Neutral ATR 6.94 Q5 · mentah 0 (doc 0) ATR 6.94 | B / B | L2 ikut buka Moomoo 24.54 (yf 24.50) |
| 24 | C SILC M57 2026-10-12 | 58.83 / 58.830 | -6.12 / -6.12 | 0 / 0 | -1.00 / -1.00 (risiko 6.1%) | Keluar 12 Okt @ 55.23 (-6.12) · semak: min(buka 58.83, henti 55.23) ; rendah 53.70 | Keluar 23 Okt @ 37.17 (-36.82) · kira: Keluar 23 Okt @ 37.73 (-35.87) | -6.12 / -6.12 · +0.00 / +0.00 | - / - (rekod 2026-10-29; sebenar 2026-10-29) | Neutral ATR 10.52 Q5 · mentah 0 (doc 0) ATR 10.52 | B / B | L2 ikut buka Moomoo 37.17 (disahkan kline Moomoo) |
| 25 | C INTC M81 2026-10-08 | 110.38 / 110.380 | -15.19 / -15.19 | 5 / 5 | -1.09 / -1.09 (risiko 13.9%) | Keluar 15 Okt @ 93.61 (-15.19) · semak: min(buka 93.61, henti 95.027) ; rendah 90.02 | Keluar 23 Okt @ 85.915 (-22.16) · kira: Keluar 23 Okt @ 85.87 (-22.21) | -15.19 / -15.19 · +1.11 / +1.11 | - / - (rekod 2026-10-29; sebenar 2026-10-29) | Neutral ATR 6.26 Q5 · mentah 0 (doc 0) ATR 6.26 | B / B | OK (replika M81) |
| 26 | C INSW M32 2026-10-09 | 121.48 / 121.480 | -3.04 / -3.04 | 3 / 3 | -1.00 / -1.00 (risiko 3.0%) | Keluar 14 Okt @ 117.79 (-3.04) · semak: min(buka 125.92, henti 117.79) ; rendah 115.14 | Keluar 20 Okt @ 103.91 (-14.46) · kira: Keluar 20 Okt @ 103.91 (-14.46) | -3.04 / -3.04 · +3.23 / +3.23 | - / - (rekod 2026-11-05; sebenar 2026-11-05) | Bullish lama ATR 5.22 Q5 · mentah 1 (doc 1) ATR 5.22 | B / B | OK |
| 27 | C CNXN M39 2026-10-13 | 94.99 / 94.990 | -6.63 / -6.63 | 8 / 8 | -0.43 / -0.43 (risiko 15.3%) | Pegang · semak: – | Keluar 20 Okt @ 86.48 (-8.96) · kira: Keluar 20 Okt @ 86.48 (-8.96) | -9.66 / -9.66 · +2.02 / +2.02 | 📅8 / 📅3 (rekod 2026-11-04; sebenar 2026-10-28) | Bullish lama ATR 2.81 Q2 · mentah 1 (doc 1) ATR 2.81 | B / B | 📅 SALAH hari: papar 8, sebenar 3 (28 Okt) |
| 28 | C ATKR M11 2026-10-15 (tidak_sah) | 94.88 / 94.880 | +0.08 / +0.08 | 1 / 1 | 0.06 / 0.07 (risiko 1.3%) | Keluar 16 Okt @ 94.96 (+0.08) · semak: tutup bar akhir 94.96 | Keluar 16 Okt @ 94.96 (+0.08) · kira: Pegang paras 94.52 (+0.08) | +0.00 / +0.00 · +0.09 / +0.09 | - / - (rekod 2026-11-19; sebenar 2026-11-19) | Bullish ATR 0.12 Q1 · mentah 1 (doc 1) ATR 0.12 | C / C | OK (ambil alih: L2 ditutup paksa, dikecualikan KPI) |
| 29 | C BKHA M76 2026-10-14 (tidak_sah) | 10.75 / 10.750 | -11.63 / -11.63 | 0 / 0 | -1.00 / -1.00 (risiko 11.6%) | Keluar 14 Okt @ 9.50 (-11.63) · semak: min(buka 10.75, henti 9.5) ; rendah 5.47 | Pegang paras -0.06 (-49.77) · kira: Pegang paras -0.06 (-49.77) | -11.63 / -11.63 · +0.00 / +0.00 | - / - (rekod –; sebenar –) | Neutral ATR 46.2 Q5 · mentah 0 (doc 0) ATR 46.20 | B / B | tidak_sah (tidak cair) tetapi L2 kekal "Pegang" paras −0.06; label "Luar peraturan" salah |
| 30 | C FOX M02 2026-10-16 (tidak_sah) | 59.02 / 59.020 | +0.75 / +0.75 | 5 / 5 | 0.13 / 0.12 (risiko 6.0%) | Pegang · semak: – | Pegang paras 54.53 (+0.75) · kira: Pegang paras 54.53 (+0.75) | -4.06 / -4.06 · +3.15 / +3.15 | 📅6 / 📅6 (rekod 2026-11-02; sebenar 2026-11-02) | Neutral ATR 2.65 Q2 · mentah 0 (doc 0) ATR 2.65 | B / B | tidak_sah (kelas berganda) kekal terbuka; label "Luar peraturan" salah |
| 31 | M VIAV S04V2 2026-10-02 | 46.09 / 45.910 | -33.94 / -33.69 | 15 / 15 | – / – (risiko –) | Pegang · semak: – | Keluar 22 Okt @ 33.4 (-27.53) · kira: Keluar 15 Okt @ 36.88 (-19.67) | -35.88 / -35.88 · +5.06 / +5.06 | 📅8 / 📅8 (rekod 2026-11-04; sebenar 2026-11-04) | Neutral ATR 9.62 Q5 · mentah 0 (doc 0) ATR 9.62 | B / B | RALAT L2: keluar 22 Okt @33.40 (−27.53) lawan kira 15 Okt @36.88 (−19.98 ikut harga isian); carta lilin db sendiri tunjuk 15 Okt |
| 32 | M LITE S04V2 2026-10-02 | 1043.31 / 1053.260 | -27.52 / -28.21 | 15 / 15 | – / – (risiko –) | Pegang · semak: – | Keluar 22 Okt @ 804.06 (-22.93) · kira: Keluar 16 Okt @ 853.49 (-18.97) | -29.45 / -29.45 · +9.56 / +9.56 | 📅9 / 📅9 (rekod 2026-11-05; sebenar 2026-11-05) | Neutral ATR 9.49 Q5 · mentah 0 (doc 0) ATR 9.49 | B / B | RALAT L2: 22 Okt @804.06 (−22.93) lawan 16 Okt @853.49 (−18.19 ikut harga isian) |
| 33 | M SNDK M81 2026-10-08 | 1643.505 / 1669.490 | -14.44 / -15.77 | 3 / 3 | -0.88 / -0.89 (risiko 16.3%) | Keluar 13 Okt @ 1406.22 (-14.44) · semak: buka 1406.22 | Keluar 23 Okt @ 1271.62 (-22.63) · kira: Keluar 23 Okt @ 1269.00 (-23.99) | -14.44 / -14.44 · +1.92 / +1.92 | - / - (rekod 2026-10-29; sebenar 2026-10-29) | Neutral ATR 7.68 Q5 · mentah 0 (doc 0) ATR 7.68 | B / B | Harga isian Moomoo (bukan buka); L2 ikut buka Moomoo |
| 34 | M AMN M31 2026-10-01 (yf-tiada-1023) | 35.44 / 35.610 | +35.47 / +34.82 | 16 / 16 | 4.99 / 4.61 (risiko 7.1%) | Pegang · semak: – | Pegang paras 40.50 (+35.47) · kira: Pegang paras 40.50 (+34.82) | -2.34 / -2.34 · +35.98 / +35.98 | 📅9 / 📅9 (rekod 2026-11-05; sebenar 2026-11-05) | Bullish ATR 3.91 Q4 · mentah 1 (doc 1) ATR 3.91 | B / B | Harga isian Moomoo; OK |
| 35 | M VIV M04 2026-10-06 | 12.8 / 12.850 | +1.25 / +0.86 | 13 / 13 | 0.09 / 0.06 (risiko 13.6%) | Pegang · semak: – | Pegang paras 11.90 (+1.25) · kira: Pegang paras 11.90 (+0.86) | -5.78 / -5.78 · +2.58 / +2.58 | 📅4 / - (rekod 2026-10-29; sebenar 2026-11-10) | Neutral ATR 2.27 Q1 · mentah 0 (doc 0) ATR 2.27 | B / B | 📅 PALSU (rekod 29 Okt; sebenar 10 Nov) |
| 36 | M XOM M49 2026-10-08 | 167.8 / 167.110 | +9.18 / +9.63 | 11 / 11 | 3.05 / 3.69 (risiko 3.0%) | Pegang · semak: – | Pegang paras 167.51 (+9.18) · kira: Pegang paras 167.51 (+9.63) | -0.65 / -0.65 · +9.51 / +9.51 | 📅5 / 📅5 (rekod 2026-10-30; sebenar 2026-10-30) | Bullish ATR 2.14 Q1 · mentah 1 (doc 1) ATR 2.14 | B / B | Harga isian Moomoo; OK |
| 37 | M AMD M70 2026-10-08 | 632.82 / 639.360 | +0.05 / -0.97 | 0 / 0 | – / -1.00 (risiko –) | Keluar 8 Okt @ 633.16 (+0.05) · semak: min(buka 639.36, henti 633.16) ; rendah 613.34 | Keluar 19 Okt @ 551.78 (-12.81) · kira: Keluar 19 Okt @ 551.78 (-13.70) | +0.00 / +0.00 · +0.05 / +0.05 | - / - (rekod 2026-11-03; sebenar 2026-11-03) | Neutral ATR 5.66 Q5 · mentah 0 (doc 0) ATR 5.66 | B / B | henti ≥ harga isian → R "–" |
| 38 | M OKTA M52 2026-10-08 (tidak_sah) | 219.27 / 216.610 | -2.84 / -1.64 | 11 / 11 | -0.07 / -0.04 (risiko 40.7%) | Pegang · semak: – | Keluar 19 Okt @ 190.4 (-13.17) · kira: Keluar 19 Okt @ 190.40 (-12.10) | -16.27 / -16.27 · +7.17 / +7.17 | - / - (rekod –; sebenar 2026-12-01) | Bullish ATR 5.81 Q5 · mentah 1 (doc 1) ATR 5.81 | B / B | tidak_sah (luar peraturan) — label betul |
| 39 | M KNF M13 2026-10-06 | 52.38 / 52.780 | -6.16 / -6.87 | 5 / 5 | -1.00 / -1.00 (risiko 6.1%) | Keluar 13 Okt @ 49.16 (-6.16) · semak: min(buka 49.48, henti 49.16) ; rendah 48.71 | Pegang paras 46.05 (+1.41) · kira: Pegang paras 46.11 (+0.64) | -6.16 / -6.16 · +2.29 / +2.29 | 📅7 / 📅7 (rekod 2026-11-03; sebenar 2026-11-03) | Bearish baharu ATR 3.67 Q3 · mentah -1 (doc -1) ATR 3.64 | B / B | Harga isian Moomoo; OK |

### Inferences
- Bagi lajur teras (untung, harga terkini, hari, R, MAE/MFE, trend/ATR, gred), dashboard memapar dengan tepat apa yang ada dalam CSV dan db. Ralat yang ditemui berpunca di hulu, dalam data CSV yang dibekukan (DAC, VIAV, LITE, ACA), bukan dalam logik halaman.
- Konvensyen harga 23 Okt ialah kline Moomoo (rasmi ikut SKEMA). Bar yfinance hari terakhir kadang-kadang salah pada buka (ZYME). Semakan atau Lejar yang hanya memakai stor yfinance akan tersasar sedikit daripada Papertrade C pada hari terakhir.
- Ralat DAC menaikkan purata M80 dan M90 kira-kira 3.4 mata setiap satu, iaitu kesan besar bagi kaedah dengan n kecil. Tiada pemeriksaan automatik yang menangkap harga_beli yang tidak sepadan dengan bar.
- Ikon 📅 sepatutnya memakai `earn_seb` (atau min(tarikh_earnings, earn_seb) yang masih akan datang). Medan ini sudah ada dalam db, tetapi tidak dipakai oleh `earnH`, `statusPos` dan panel "📅 Earnings ≤ 10 hari" ([dashboard_v2.html:2455](BacktestShariah2/standard/dashboard_v2.html)).

### Gaps
- Saya hanya mengesahkan buka atau tutup Moomoo bagi 6 saham (ZYME, DAC, ACA, FRD, GRAL, SILC). Baki 13 belian 23 Okt yang berbeza > 0.3% daripada yfinance (contoh NEOG, KARO, PODD, TANH, CERT, VCEL, JOUT) tidak disemak dengan kline Moomoo.
- Sumber nilai 164.162 bagi DAC M80/M90 tidak dapat ditentukan, kerana sejarah git cetek (hanya dari 21 Okt).
- TTC M49 (keluar 95.44 lawan henti 95.24) tidak dapat disahkan tanpa membaca logik henti M49 dan bar Moomoo 12 Okt.
- Ketepatan isyarat keluar kaedah bagi posisi terbuka (selain pelanggaran henti) memerlukan larian enjin setiap kaedah. Ini tidak dibuat.

## 2. Adakah posisi tidak_sah / tidak_dibeli / ambil alih / delist dikendalikan secara konsisten dalam kiraan dan purata?

### Takeaway
Dari segi pengecualian, ya: KPI, Peta dan semua dokumen prestasi mengecualikan `tidak_sah`, dan baris `tidak_dibeli` dibuang daripada jadual. Kelemahannya ada pada label dan liputan. Semua baris `tidak_sah` C dilabel "Luar peraturan". Kiraan dalam segmen dan KPI memakai penyebut berbeza. Baris tidak cair dan kelas berganda kekal "Dipegang" tanpa had masa. Lebih penting, satu saham yang sudah diambil alih (ACA, 8 posisi C) tidak dikesan dan masih dikira sah. Panel "Isyarat tidak dibeli" pula hanya menunjukkan sebahagian kecil isyarat yang dilangkau.

### Cited Findings
- `posRows` membuang `tidak_dibeli`. `ptKpis` mengira `sahSahaja` (tanpa `tidak_sah`), dan Peta memakai `sahSahaja(peg)`. — [dashboard_v2.html:1497-1499, 1471-1472, 1527](BacktestShariah2/standard/dashboard_v2.html)
- `jana_db.sah()` mengecualikan tidak_dibeli, tidak_sah dan luar_peraturan bagi `prestasi/ringkasan` dan `harian_kaedah`. `lorong2_siri.posisi()` mengecualikan tidak_dibeli dan tidak_sah. Halaman (`normPT`) hanya membaca `tidak_sah`. Ini selamat sekarang kerana 8 baris M `luar_peraturan` juga `tidak_sah`, tetapi tiada jaminan untuk masa depan. — [jana_db.py:79-81](BacktestShariah2/standard/jana_db.py); [lorong2_siri.py:49-56](BacktestShariah2/standard/lorong2_siri.py); [dashboard_v2.html:1377](BacktestShariah2/standard/dashboard_v2.html)
- Komposisi C `tidak_sah` dibeli (122 baris): ambil alih 89 (RAMP 22, DV 21, BRZE 14, ATKR 10, PTC 9, TECH 7, PEN 4, SLAB 2; semua `tutup_semua`), tidak cair 18 (BKHA 6, AKA 4, WLYB 2, MGRT 2, FEDU 2, SENEB 1, MAYS 1; 12 belum `tutup_semua`) dan kelas berganda 15 (FOX 14, NWS 1; semuanya belum `tutup_semua`). `tidak_dibeli` 64 baris (semua juga `tidak_sah`). Tiada baris delist pada masa ini. — skrip `kpi.py`, semakan komposisi
- **Label salah:**
  - Subtajuk KPI memapar "`122 dibeli luar peraturan (tidak dikira)`" bagi C. Ini kerana `all.some(r=>r.tidak_dibeli)` sentiasa palsu selepas `posRows` membuang tidak_dibeli.
  - Lajur Keluar kaedah (Penuh: `r.tidak_dibeli?'Tidak dibeli':'Luar peraturan'`), Ringkas dan helaian butiran memapar pil "Luar peraturan" bagi isyarat palsu ambil alih, tidak cair dan kelas berganda. Sebab sebenar hanya ada dalam teks kecil (`sebab_tidak_sah`, lajur Penuh sahaja).
  - [dashboard_v2.html:1475, 1468, 1514, 2192, 2297](BacktestShariah2/standard/dashboard_v2.html)
- **Penyebut berbeza:** segmen "Semua (5,647) · Dipegang (4,178) · Sudah keluar (1,469)" termasuk 122 baris tidak_sah, manakala kad KPI "Posisi Claude dibeli 5,525" tidak. — [dashboard_v2.html:1529, 1475](BacktestShariah2/standard/dashboard_v2.html); skrip `kpi.py`
- Baris tidak cair dan kelas berganda dibiarkan terbuka. Contohnya BKHA M76 lorong 2 "Pegang" dengan untung semasa −49.77% dan FOX M02 terbuka. `tidak_layak.py posisi` hanya menutup baris ambil alih dan delist (SKEMA: "kedua-dua lorong ditutup" bagi ambil alih). Baris ini kekal dalam segmen "Dipegang" selama-lamanya dan menambah hingar. — [SKEMA.md](BacktestShariah2/papertrade/SKEMA.md)
- **Ambil alih tidak dikesan: ACA (Arcosa).** CRH bersetuju membeli Arcosa pada USD150 tunai (perjanjian 21 Jun 2026; pemegang saham meluluskan 4 Sep 2026). 8-K menyatakan penggabungan selesai pada **23 Okt 2026**. — [SEC 8-K Arcosa (CRH to acquire)](https://www.sec.gov/Archives/edgar/data/0001739445/000173944526000112/exh991-crhtoacquirearcos.htm); [SEC 8-K penutupan](https://www.sec.gov/Archives/edgar/data/0001739445/000114036126040596/ef20084131_8k.htm); [Arcosa IR: kelulusan pemegang saham](https://ir.arcosa.com/news-events/press-releases/news-details/2026/Arcosa-Stockholders-Approve-Acquisition-by-CRH/default.aspx)
- 8 posisi C ACA dibeli selepas pengumuman: M95 dan M54 (12 Okt @147.01), dan M06, M23, M46, M100, M101, M120 (22 Okt @148.90). Semuanya tanpa `tidak_sah` dan dikira dalam KPI dan prestasi kaedah. Ini bercanggah dengan peraturan CLAUDE.md ("Posisi C dibeli selepas pengumuman ambil alih → tidak_sah dan ditutup"). — [CLAUDE.md](CLAUDE.md); db `ringkas_c`
- Punca ACA terlepas: jurang buka hari pengumuman (22 Jun 2026) hanya **+6.74%** (volum 4.46 juta ≈ 17× median, julat 2.04%), lebih rendah daripada `JURANG_MIN = 0.10` dalam pengesan corak harga. ACA juga tiada dalam `data/ambil_alih.csv`. Folder `data/edgar/` tiada dalam repo, jadi lapisan EDGAR belum menghasilkan apa-apa. Bagi penggabungan tunai melalui undian (DEFM14A), lapisan itu hanya menulis "calon". — [kod/ambil_alih.py:32-39, 56-76](BacktestShariah2/kod/ambil_alih.py); [standard/tawaran_edgar.py:10,30,170-172](BacktestShariah2/standard/tawaran_edgar.py); [data/ambil_alih.csv](BacktestShariah2/data/ambil_alih.csv)
- **Panel "Isyarat tidak dibeli" tidak lengkap.**
  - Panel ini memapar 64 baris: 42 "sedia() sig=False", 15 M52 mingguan dan 7 "Langkau …" dari 8 dan 13 Okt. Semua medan lengkap (tarikh dirancang, harga buka rujukan, henti, sebab).
  - Langkauan semasa belian 9:35 tidak direkod sebagai baris. Log mencatat 14, 12, 27, 21, 28, 27, 21 dan 9 langkauan (≈ 159 isyarat, 14–23 Okt). Contoh 23 Okt: FRPT, ROL, WS, NSIT M08 (buka > buka_maks); COR M14, SSNC M23, PVH M70, GNTX M106, TANH M140 (buka ≤ henti).
  - Subtajuk panel "dilangkau ikut peraturan kaedah" memberi gambaran senarai itu lengkap. — [dashboard_v2.html:1531-1535](BacktestShariah2/standard/dashboard_v2.html); [binaan_v2_log_tambahan.md:65,102,122,176,208,229,274,302](BacktestShariah2/standard/binaan_v2_log_tambahan.md); [jadual/beli_0935.md:12,17](BacktestShariah2/jadual/beli_0935.md)
- `harian/status.beli_ringkas` {direkod 761, dilangkau 9} tidak dipapar dalam tab Posisi. — db `harian/status` v41

### Inferences
- Bagi pemilihan kaedah, isu terbesar ialah liputan, bukan pengecualian. Saham terkunci yang tidak dikesan (ACA) masuk sebagai dagangan "sah" berisiko hampir sifar dan mengganggu R serta kadar menang kaedah. Langkauan yang tidak direkod pula menyembunyikan kadar isyarat yang tidak boleh dilaksanakan bagi setiap kaedah (contoh M08 buka > buka_maks, M14 buka ≤ henti). Kadar ini penting bila menilai sama ada sesuatu kaedah boleh dilaksanakan dengan wang sebenar.
- Label "Luar peraturan" ialah istilah Moomoo (dibeli sebenar di luar peraturan). Bagi C, label "Isyarat palsu" / "Tidak cair" / "Kelas berganda" lebih tepat.

### Gaps
- Tidak disemak sama ada ticker lain dalam posisi terbuka ada corak terkunci yang serupa tetapi tidak dikesan. Cadangan imbasan: median julat 10 bar ≤ 0.6% dan ATR Q1 < 0.5%.
- Tidak ditentusahkan dengan SEC sama ada ACA dinyahsenarai pada 23 Okt (tiada bar 23 Okt dalam Moomoo dan yfinance menyokong kemungkinan itu). Harga akhir patut USD150 tunai, bukan 149.15.

## 3. Adakah Gabung mengira dua kali atau mencampur posisi yang tidak serasi?

### Takeaway
Gabung tidak mengira dua kali: tiada kunci (saham, kaedah, tarikh_beli) yang sama antara M dan C. Namun ia mencampur dua populasi yang tidak serasi:
- konvensyen harga beli yang berbeza (isian sim lawan buka rasmi);
- 11 posisi strategi luar yang bukan kaedah M;
- 15 posisi dengan unit > 1;
- pegangan warisan v1;
- tempoh pasaran yang berbeza (1–8 Okt lawan 8–23 Okt).
Jadi purata Gabung tidak sesuai untuk menilai kaedah.

### Cited Findings
- `posRows('gab')` = baris M diikuti baris C, dengan kunci `_p` 'M|i'/'C|i' yang unik. Tiada pertindihan kunci tepat (0). 29 pasangan saham+kaedah wujud dalam kedua-dua akaun (31 baris C dibeli 12–23 Okt selepas belian M 8 Okt). — [dashboard_v2.html:1497-1499](BacktestShariah2/standard/dashboard_v2.html); skrip pertindihan
- M = 208 baris: harian 147, log_v1 (warisan v1, "Pegang (warisan v1)") 50 dan luar 11 (S04V2 5, BandWalk 4, MANUAL 2; nota "Strategi luar 87 M; tiada peraturan keluar M"). 15 baris unit > 1 (19, 22, 33, 10 unit). Tarikh beli M 1–8 Okt; C 8–23 Okt. — db `ringkas_m`
- KPI tanpa strategi luar: M +0.86% menjadi +1.27%. Gabung +1.73%, atau +1.75% tanpa luar. Kerugian terbesar Gabung/M ialah VIAV (S04V2) −33.94%, iaitu strategi luar, bukan kaedah. Kiraan "125 kaedah" Gabung termasuk S04V2, BandWalk dan MANUAL. — skrip `kpi.py`; db `prestasi/ringkasan` (`rugi_terbesar_saham` "VIAV (S04V2)")
- Harga beli M ialah isian sim (contoh SNDK 1643.505 lawan buka 1669.49 (−1.6%), AMD 632.82 lawan 639.36, OKTA 219.27 lawan 216.61). Harga beli C ialah buka rasmi. Untung M dan C oleh itu diukur atas asas berbeza. — sampel #33, #37, #38
- Tajuk Moomoo menyatakan "1 unit setiap saham", padahal 15 baris > 1 unit. Tajuk itu juga menyatakan "Saham yang kena isyarat keluar ditanda merah", tetapi `rclsPT` hanya menanda merah apabila `tutup_semua` (kedua-dua lorong). — [dashboard_v2.html:1523, 1457](BacktestShariah2/standard/dashboard_v2.html)
- Purata adalah setara (equal-weight %), tanpa mengira unit atau nilai USD. Ini konsisten dengan `prestasi/ringkasan` (`USD_POSISI` 1000 seragam). — [jana_db.py:99-107](BacktestShariah2/standard/jana_db.py)

### Inferences
- Akaun C ialah satu-satunya populasi yang bersih untuk menilai kaedah. Gabung berguna sebagai pandangan pendedahan sahaja. Untuk pemilihan kaedah, akaun M sepatutnya mengecualikan `sumber=luar` dan menanda log_v1. Paling baik, Gabung tidak dipapar dalam KPI purata.

### Gaps
- Tidak disemak sama ada isyarat keluar bagi baris log_v1 dinilai dengan enjin v1.2 atau logik v1 lama.

## 4. Adakah data terkini? (tarikh dokumen db lawan repo/sesi, logik lencana kesegaran, harga atau keluar yang lapuk)

### Takeaway
Ya pada peringkat dokumen. Semua dokumen yang dibaca tab Posisi dibina 2026-10-24 06:30 MYT dengan harga tutup 2026-10-23 (sesi terkini), dan tiada perubahan papertrade dalam repo selepas tolakan itu. Masalah kesegaran berada pada peringkat baris dan label:
- harga ACA dan FEDU ialah bar rata sintetik;
- 31 ticker hanya ada bar 23 Okt daripada Moomoo, jadi dokumen terbitan tidak boleh dijana semula daripada repo;
- keluar lorong 2 VIAV/LITE dan harga beli DAC yang salah sudah dibekukan;
- label sumber harga menyebut "yfinance muktamad; GitHub Actions" walaupun mod masih `bayang` dan harga diambil oleh rutin Claude daripada skrin Moomoo.
Lencana "Kemas kini terakhir" hanya mengukur masa tolakan, bukan sama ada tarikh data ialah sesi yang dijangka.

### Cited Findings
- `harian/status` v41: dikemaskini/kemaskini_pagi "2026-10-24 06:30 MYT", harga_tutup_pada/tarikh_data "2026-10-23", beli_pada "2026-10-23 21:41 MYT", beli_ringkas {direkod 761, dilangkau 9}, kemaskini_pagi_ringkas {C_keluar_baru 186, M_keluar_baru 3, menunggu_buka 55, tidak_dibeli_baru 1, watchlist_dibuang 91}. — db `harian/status`
- `papertrade/ringkas_c` v7 dan `ringkas_m` v6: dibina 06:30 MYT, harga_pada "2026-10-23 tutup …". `prestasi/garis` tarikh terakhir 20261023 (SPY 759.90/759.97). `prestasi/mae`, `mfe`, `mae_atr` dan `posisi/lorong2` harga_hingga "2026-10-23 tutup". `harian/trend` tarikh 20261023. — salinan db scratchpad
- Commit repo selepas tolakan (`3fc565e` 22:12 UTC, "Kemas kini 6:02 pagi 24 Okt … db ditolak") hanyalah RS, TradingView, analisis mingguan dan yfinance 23:59 UTC. yfinance 23:59 membetulkan sedikit tinggi/rendah sesetengah bar dan membuang bar BLBD. Tiada fail `papertrade/` berubah, jadi db selari dengan repo. — `git log` HEAD `c0adf74`; `git diff ca14de6 3707702`
- Stor harga repo (`data/harga/stor/harga_A/B.csv`) berakhir 20261022. Bar 23 Okt dalam repo hanya ada dalam `terkini.csv` (883/930 ticker; 47 `tiada_bar_sesi`). `jana_db.py` yang dijalankan atas stor repo memberi `prestasi/garis` tanpa tutup 23 Okt. Dengan stor + `terkini.csv` pun, masih berbeza daripada db bagi 36 ticker garis, 28 kunci MAE/MFE (posisi 23 Okt) dan 16 kunci lorong 2, kerana rutin mengisi bar itu daripada Moomoo. — [data/harga/status.json](BacktestShariah2/data/harga/status.json); [jana_db.py:252-299](BacktestShariah2/standard/jana_db.py); skrip `banding2.py`
- ACA 23 Okt dalam db = [buka, tinggi, rendah, tutup] 149.15/149.15/149.15/149.15, sama dengan tutup 22 Okt. Kline Moomoo tiada bar 23 Okt, dan penggabungan CRH selesai 23 Okt. FEDU 10.48 rata selama 3 sesi. Kedua-duanya dipapar sebagai "Harga terkini pada 2026-10-23 tutup". — db `posisi/lorong2`, `prestasi/garis`; [SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001739445/000114036126040596/ef20084131_8k.htm)
- Label sumber: `jana_db.py` menulis `harga_pada = "… tutup (bar harian yfinance muktamad; GitHub Actions)"` dan `nota = "Dikemas kini oleh GitHub Actions (standard/harian_c.py) {masa}…"` tanpa mengira mod. `MOD_ACTIONS` = `bayang`, dan `papertrade/status_harian.json` tiada, jadi `{masa}` kosong (nota tertulis "harian_c.py) : harga tutup"). Log 24 Okt pula menyatakan "Gabungan yfinance dilangkau" (harga daripada skrin Moomoo). Tajuk C memapar label ini. — [jana_db.py:446-452](BacktestShariah2/standard/jana_db.py); [BacktestShariah2/MOD_ACTIONS](BacktestShariah2/MOD_ACTIONS); [binaan_v2_log_tambahan.md:307](BacktestShariah2/standard/binaan_v2_log_tambahan.md); [dashboard_v2.html:854, 1525](BacktestShariah2/standard/dashboard_v2.html)
- Lencana kesegaran: `renderData` menandakan merah jika masa sekarang − `dikemaskini` > 30 jam (74 jam jika hari MYT Ahad–Selasa). Tarikh data ditunjukkan sebagai teks "data tutup X" tetapi tidak dibanding dengan sesi yang dijangka. `jangkaSesi()` sudah wujud dan hanya dipakai dalam panel saluran. Jadi tolakan yang membawa harga sesi lama tetap hijau. Bagi jadual tolakan Selasa–Sabtu 6:02 dan Isnin–Jumaat 9:35 NY, ambang ini tidak memberi merah palsu pada hujung minggu: Sabtu 06:30 + 30 jam = Ahad 12:30, dan Ahad memakai 74 jam. — [dashboard_v2.html:844-866, 2418-2430](BacktestShariah2/standard/dashboard_v2.html)
- `trend`: 25 ticker dengan `tarikh_data` lama (19, 16, 7 dan 5 Okt) dilabel "data <tarikh>". 13 ticker tanpa status (sejarah < 201 sesi) dilabel "Sejarah pendek". — db `harian/trend`; [dashboard_v2.html:3253-3260](BacktestShariah2/standard/dashboard_v2.html)
- Keluar yang dibekukan tetapi salah: VIAV dan LITE lorong 2 (bahagian 1); DAC M80/M90 harga_beli. Sebaliknya, 7 keluar lorong 1 "dibekukan" telah dibuka semula oleh pelarasan faktor atau kaedah replika sejak 21 Okt. — [keluar_lorong.py:140-160](BacktestShariah2/standard/keluar_lorong.py); perbandingan `577883c` lawan HEAD
- Tanda "BARU" memakai `belianTerkini(prSrc('c'))` (23 Okt). Posisi beli 23 Okt menunjukkan Hari 0 dan untung buka ke tutup. — [dashboard_v2.html:2374](BacktestShariah2/standard/dashboard_v2.html)

### Inferences
- Bagi pengguna, "Harga terkini pada 2026-10-23" boleh dipercayai bagi kira-kira 97% posisi terbuka (semua yang ada bar yfinance sepadan sehingga 0.005). Pengecualiannya ialah saham tanpa dagangan pada sesi itu. Dashboard tidak memberi tanda bagi bar yang diisi Moomoo atau bar sintetik.
- Data yang tidak boleh dijana semula daripada repo (bar Moomoo hanya dalam stor kerja rutin) melemahkan audit. Bar 23 Okt yang dipakai sepatutnya disimpan dalam repo, contohnya sebagai `terkini_moomoo.csv`.

### Gaps
- Larian GitHub Actions tidak disemak. Alat MCP github gagal disambung (ERR_PROXY_TUNNEL). Mod bayang bermakna Actions tidak menulis ke `papertrade/`, jadi kesegaran db bergantung pada rutin Claude 6:02 dan 9:35.
- Saya tidak dapat menentukan sama ada `dikemaskini` 06:30 MYT ialah masa tolakan sebenar atau parameter `--masa`. Commit rutin ialah 06:12 MYT.

## 5. Adakah tab Posisi membantu memilih kaedah untuk wang sebenar? Lajur atau panel mana yang hingar, berulang, mengelirukan atau tiada?

### Takeaway
Tab Posisi ialah buku besar operasi (5,647 baris C). Ia bukan alat pemilihan kaedah. KPI kepalanya mengelirukan untuk tujuan itu: purata +1.77% mencampur 4,159 posisi terbuka (+3.28% belum direalisasi, median 3 hari) dengan 1,366 keluar lorong 1 (−2.84%), dan KPI tidak mengikut tapisan kaedah. Lebih separuh lajur Penuh (7 lajur gred, Trend, Pemangkin, Kewangan) ialah rekod hari isyarat yang dinyatakan sendiri sebagai "belum terbukti meramal" atau "tidak meramal". Yang benar-benar berguna untuk menilai kaedah ialah perbandingan dua lorong, R, MAE/MFE, beza lawan SPY dan hari lawan had masa. Semua ini dipapar setiap posisi dan tidak diagregat mengikut kaedah dalam tab ini.

### Cited Findings
- Campuran KPI C: sah 5,525 = terbuka lorong 1 4,159 (purata +3.28%; hari median 3, purata 3.53; 2,598 < 5 hari, hanya 114 ≥ 10 hari) dan keluar lorong 1 1,366 (purata −2.84%; majoriti "kena henti" 876). — skrip `kpi.py`; db `ringkas_c`
- `ptKpis(all,…)` dan `panelPeta(sahSahaja(peg),…)` menerima set penuh, bukan `rows` yang ditapis oleh `ptFilterBar`. Memilih kaedah, sektor atau carian hanya mengubah jadual; kad KPI dan Peta kekal bagi semua kaedah. — [dashboard_v2.html:1517-1529](BacktestShariah2/standard/dashboard_v2.html)
- Segmen "Dipegang" = lorong 1 belum keluar. 1,268 posisi C (1,348 Gabung) yang masih dipegang dalam lorong 2 berada dalam "Sudah keluar" dan tidak masuk Peta. Tooltip Peta menyebut "(lorong kaedah)", tetapi tajuk "posisi dipegang" tidak. — [dashboard_v2.html:1518, 3054](BacktestShariah2/standard/dashboard_v2.html); TIPS `peta_portfolio` [3517](BacktestShariah2/standard/dashboard_v2.html)
- Peta mengira posisi, bukan saham. 4,159 posisi terbuka C hanya dalam 605 saham (BIIB 34 posisi; NOW, EXLS, CTSH 32; ANF, BDX, TRI, DOCU 31). 3,613 baris C ada `kaedah_kongsi`. Saiz kotak menggambarkan pertindihan isyarat antara kaedah, bukan pendedahan sebenar. — [dashboard_v2.html:3037-3058](BacktestShariah2/standard/dashboard_v2.html); skrip `kpi.py`
- Ikon 📅 dipapar pada 71% posisi belum tutup (3,991/5,632) dalam musim earnings, jadi daya bezanya rendah, dan sumber tarikhnya pula salah bagi 146 posisi (bahagian 1). — skrip earnings
- Gred dan trend dinyatakan oleh halaman atau projek sendiri sebagai tidak teruji:
  - TIPS `gred`: "Direkod untuk diuji, belum terbukti meramal dan bukan penapis belian" [3642](BacktestShariah2/standard/dashboard_v2.html).
  - SKEMA: gred kewangan "rekod sahaja".
  - CLAUDE.md: trend "Paparan sahaja (kajian 23 Okt 2026: tidak meramal pulangan 3–30 hari; bukan penapis atau peraturan jual)".
  - TIPS `trend_jp` menyatakan sama, dan bahawa ATR ialah "ukuran risiko yang lulus ujian luar sampel" [3511-3512](BacktestShariah2/standard/dashboard_v2.html).
  - Pandangan Penuh mempunyai 7 lajur gred (`grCols`) ditambah Trend, dan pandangan Gred mengulanginya. — [dashboard_v2.html:1449-1456, 3071-3074](BacktestShariah2/standard/dashboard_v2.html); [SKEMA.md](BacktestShariah2/papertrade/SKEMA.md); [CLAUDE.md](CLAUDE.md)
- Empat takrif "hampir paras keluar" yang berbeza:
  - ◆ `statusPos`: ¼ julat lorong 2 atau henti dalam 2%.
  - Jalur oren `jalurPT`: mana-mana lorong dalam 3%.
  - Warna `mkLorong` (kad): −1% merah, −3% oren.
  - Cip `l2Cip`: jarak dalam unit ATR (Jauh, Sederhana, Dekat, Sangat dekat).
  - [dashboard_v2.html:2362-2368, 2165-2166, 2174-2176, 3288-3294](BacktestShariah2/standard/dashboard_v2.html)
- Pengulangan: status lorong 1 dipapar dalam lajur "Keluar kaedah", cip K, kad dan helaian. R dipapar dalam Penuh, Risiko dan helaian. Lorong 2 dipapar sebagai lajur, bar l2, cip ATR dan titik ◆. Harga beli → terkini dipapar dua kali dalam Ringkas (lajur Untung % juga memaparnya). — [dashboard_v2.html:1458-1470, 1505-1514, 3071-3088](BacktestShariah2/standard/dashboard_v2.html)
- Jadual boleh menjadi 5,647 baris. "Papar semua" hanya muncul jika ≤ 400 baris, dan susunan lalai ialah untung menurun, jadi posisi menang dilihat dahulu. — [dashboard_v2.html:1484, 1530](BacktestShariah2/standard/dashboard_v2.html)
- Elemen yang berguna untuk menilai kaedah sudah ada, tetapi hanya setiap posisi atau dalam helaian lain: cip "SPY … · beza" (`spyCip`), MAE/MFE (pandangan Risiko), bar hari lawan had masa atau purata backtest (`hariSel`), dan "Dua lorong keluar: kaedah X · selagi naik Y" setiap kaedah dalam helaian `openKaedah`. — [dashboard_v2.html:2381-2383, 2396-2400, 2280](BacktestShariah2/standard/dashboard_v2.html)
- Tooltip `harga_beli` ("Harga isian purata order beli") salah bagi C. Tajuk Moomoo menyatakan "1 unit setiap saham" walaupun ada 15 baris > 1 unit. — [dashboard_v2.html:3586, 1523](BacktestShariah2/standard/dashboard_v2.html)

### Inferences
- **Paling mengelirukan untuk keputusan wang sebenar:**
  - (1) KPI "Purata untung", kerana bias ke atas daripada posisi muda yang belum kena henti;
  - (2) KPI dan Peta yang tidak mengikut tapisan kaedah;
  - (3) label "Luar peraturan" bagi isyarat palsu;
  - (4) 📅 dengan tarikh basi;
  - (5) Gabung yang mencampur strategi luar.
- **Hingar untuk pemilihan kaedah (simpan dalam helaian, bukan lajur):** 7 lajur gred, Trend, Pemangkin, Kewangan, Peta portfolio (sesuai untuk pendedahan, bukan pemilihan) dan 📅 (berguna sebagai amaran risiko operasi, tetapi perlu sumber `earn_seb`).
- **Tiada tetapi diperlukan:**
  - (a) ringkasan setiap kaedah yang mengikut tapisan: n, n matang ≥ had masa, purata realisasi lawan belum realisasi, lorong 1 lawan lorong 2, beza lawan SPY, kadar kena henti;
  - (b) kadar isyarat yang dilangkau atau tidak boleh dilaksanakan setiap kaedah (langkauan 9:35 tidak direkod);
  - (c) penanda kualiti data setiap baris (bar Moomoo sahaja, bar sintetik, harga beli ≠ buka bar, keluar dibuka semula oleh replika);
  - (d) MAE/MFE lorong 2;
  - (e) pautan terus ke Papan Penganalisis atau Prestasi bagi kaedah yang ditapis.
  - Penilaian kaedah yang sah (posisi matang, skor dipotong, BERSARA/GANTUNG) sudah ada dalam tab Analisis dan Prestasi (CLAUDE.md, Papan Penganalisis). Tab Posisi sepatutnya merujuk ke sana dan tidak memberi purata sendiri.

### Gaps
- Saya tidak menguji dengan data sama ada gred atau trend pada hari isyarat meramal untung posisi C (n masih kecil dan kebanyakannya belum matang). Penilaian bergantung pada kenyataan projek sendiri dan panel Prestasi ikut gred.
- Paparan sebenar pada telefon dan desktop tidak dilihat dalam pelayar. Penilaian kad dan lajur berdasarkan kod sahaja.
