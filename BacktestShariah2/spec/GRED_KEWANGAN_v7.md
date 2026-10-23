# Gred kewangan v7 (A–E)

Kod: `standard/gred_kewangan.py`. Ujian: `ujian/test_gred_kewangan.py`, `ujian/test_gred_kewangan_v71.py` (v7.1). Lajur: `gred_kewangan`, `kewangan_ringkas`, `kewangan_tempoh`, `kewangan_butiran` (senarai_beli, watchlist, fail posisi).
Status: rekod sahaja (keputusan pengguna 18 Okt 2026, selepas tujuh pusingan kajian). Belum diuji prestasi. TIDAK dimasukkan ke dalam `gred_keseluruhan` supaya rekod gred sedia ada kekal setanding.
v7.1 (23 Okt 2026, keputusan pengguna "Penuh"): sambungan §11–13 HANYA apabila peraturan v7 memberi `–`; apabila v7 memberi gred, hasil v7.1 sama tepat dengan v7 (disahkan pada 2,319 baris bergred: gred, K/U/T/S, keyakinan dan ringkasan sama). `kewangan_butiran.versi` = `7` (laluan v7) atau `7.1` (sambungan; `sebab_v7` merekod sebab v7 tidak dapat menggred).

## 1. Tujuan
Menggambarkan keadaan kewangan syarikat (bukan harga, bukan valuasi) dengan cara yang dipakai pakar: beberapa dimensi berasingan, ambang mutlak untuk kekukuhan, kemampanan berbilang tahun, kelemahan utama mengehadkan gred, komponen dan keyakinan dipaparkan.
Asas: S&P Corporate Methodology, Moody's, Simply Wall St (MODEL.markdown, Nov 2024), GuruFocus, Value Line, Morningstar, CFA Institute, Graham, Buffett, Munger, Lynch, Fisher, Greenblatt, Dorsey, Akre, Terry Smith, Minervini, Damodaran, Piotroski, Beneish, Sloan, Altman, Bharath & Shumway, indeks MSCI/S&P Quality, saringan Syariah AAOIFI/S&P/DJIM/MSCI/FTSE/SC.

## 2. Data (peraturan wajib; audit 8 saham 18 Okt 2026)
- Sumber: Moomoo `quote_financials_statements` (US GAAP), suku tunggal (financial_type 9) dan tahunan (7); `quote_financials_earnings_price_history` (tarikh siaran); `quote_market_snapshot` (`issued_shares`).
- Nisbah siap Moomoo (statement_type 4) TIDAK dipakai: ia TTM, liputan faedahnya termasuk untung luar biasa dan meletup apabila faedah ≈ 0.
- Tempoh dikenal pasti ikut label (`period_text`); tarikh akhir = `date_time` + 8 jam (UTC+8). Penyata berbeza boleh berbeza 1 hari, digabung ikut label.
- TTM = 4 suku berturut (jarak 70–125 hari; suku 16 minggu dan tahun 52/53 minggu). Minimum 8 suku berturut; 24 suku untuk ujian 5 tahun.
- Medan yang tiada = tidak dikira (bukan 0), kecuali hutang pendek/panjang (tiada = 0).
- Untung luar biasa: suku dengan |Other Income| atau |Special Income| > 5% hasil atau > 20% untung sebelum cukai. Untung bersih dan EPS teras = dilapor tolak item itu selepas cukai (kadar cukai suku, had 0–35%). ROE, ROA, OCF > untung, akruan dan semua ujian EPS memakai angka teras; nota `untung_luar_biasa`.
- Q4 Moomoo = tahunan − 9 bulan. Jika Q4 ada baris kos negatif, belanja operasi > 2× purata Q1–Q3, atau caj khas bertentangan tanda dengan Q1–Q3 (> 5% hasil), tetingkap TTM itu memakai EBIT = untung sebelum cukai + faedah; nota `q4_ragu`.
- ROE: untung induk / purata ekuiti induk (t, t−4). Ekuiti ≤ 0 → ROE tidak dikira. ROA: untung disatukan / aset. Modal dilabur: jumlah ekuiti (termasuk minoriti) + hutang − tunai.
- Point-in-time: tempoh dipakai mulai tarikh siaran (+1 hari jika selepas tutup; tarikh hanya dipercayai jika 1–120 hari selepas akhir tempoh, kerana rekod Moomoo kadang tersalah label); tanpa rekod: akhir + 45 hari (Q1–Q3) atau + 60 hari (Q4/FY). Suku terakhir tamat > 200 hari lalu → `–`.
- Moomoo menimpa angka apabila syarikat menyata semula (tiada versi); kesan look-ahead diterima dan dicatat. `kewangan_butiran` menyimpan input setiap gred (rekod point-in-time).
- Tiada dalam data: pampasan saham (SBC), capex kasar (kebanyakan), bilangan saham dalam penyata, tarikh matang hutang/covenant, pendapat going concern, KPI sektor (NRR, jualan kedai sama, rizab). Tidak dianggar.

## 3. Sub-gred
### K – Kekukuhan (S&P standard volatility; utiliti: low volatility)
- Hutang bersih (hutang termasuk pajakan − tunai) / EBITDA TTM: < 1.5 A, < 3 B, < 4 C, < 5 D, selainnya E (utiliti dikawal selia, jadual low volatility: 2 / 4 / 5 / 6).
- FFO (OCF − perubahan modal kerja) / hutang bersih: > 60% A, > 30% B, > 20% C, > 12% D, selainnya E (utiliti: 35 / 13 / 9 / 6).
- K = yang lebih teruk antara dua. Hutang bersih ≤ 1% aset → A.
- Turun 1 huruf jika ≥ 2 semakan Simply Wall St gagal (tidak bagi utiliti dikawal selia, yang gagal semakan kecairan secara struktur): aset semasa > liabiliti semasa; aset semasa > liabiliti jangka panjang; hutang/ekuiti tidak naik dalam 5 tahun; EBIT ≥ 5× faedah (had 100×; faedah tiada dan hutang ≤ 1% aset = lulus; faedah tiada dengan hutang = tidak dikira).
- Altman Z'' (6.56, 3.26, 6.72, 1.05) < 1.10 = semakan silang sahaja (nota `altman_z2<1.1`): maksimum D hanya jika distance-to-default juga < 2. Sebab: Z'' menghukum syarikat sihat yang untung tertahannya negatif kerana belian balik saham (DOCU, ADSK) atau modal kerja negatif (pengedar, perisian langganan); kajian mendapati model diskriminan Altman paling lemah (Wu, Gaunt & Gray 2010).
- EBITDA ≤ 0 dan FCF < 0: tunai / pembakaran FCF ≥ 1 tahun → D, selainnya E.
- Distance-to-default naif (Bharath & Shumway 2008; F = hutang pendek + 0.5 hutang panjang, σD = 0.05 + 0.25σE, T = 1, harga 1 tahun daripada stor harga, `issued_shares`): DD < 1 → K dan gred maksimum D; DD < 0 → E. Dikenakan selepas histerisis. Ambang DD ialah andaian.

### U – Keuntungan (6 semakan)
1. ROIC (NOPAT / purata modal dilabur) > 9% (kos modal anggaran; andaian).
2. ROE ≥ 15% DAN ROA ≥ 6% (menapis ROE daripada hutang; Munger, Akre, Dorsey).
3. Kemampanan: ROE ≥ 15% dan FCF/hasil ≥ 5% dalam ≥ 5 daripada 10 tahun terakhir (kurang 10 tahun: ≥ separuh, minimum 5 tahun).
4. Margin operasi TTM > median industri DAN ≥ margin 5 tahun lalu.
5. Kemeruapan EPS (sisihan piawai pertumbuhan EPS tahunan 5 tahun) ≤ median industri (MSCI).
6. OCF TTM > untung bersih teras TTM.
- Peringkat `kitaran`: semakan 2 dan 4 memakai purata 5 tahun.
- Peringkat `muda`: diganti dengan tunai ≥ 1 tahun pembakaran (atau FCF ≥ 0), margin kasar naik YoY, margin kasar > median industri, OCF > untung.

### T – Pertumbuhan (6 semakan)
1. EPS TTM > EPS TTM 5 tahun lalu (asas ≤ 0: tidak dikira).
2. ROIC tambahan 5 tahun (ΔNOPAT / Δmodal dilabur, hanya jika modal bertambah) > 9%.
3. Pertumbuhan EPS 1 tahun > purata tahunan 5 tahun.
4. EPS suku terkini YoY ≥ 18% (O'Neil).
5. Jualan suku terkini YoY ≥ 20%.
6. Jualan naik YoY dalam ≥ 6 daripada 8 suku terakhir.

### S – Arah suku terkini (YoY; 6 semakan)
Margin kasar naik; margin operasi naik; hutang/aset tidak naik; nisbah semasa naik; tiada terbitan saham bersih 12 bulan; Code 33 (EPS YoY, jualan YoY dan margin bersih memecut 3 suku berturut).

### Penukaran semakan → huruf (U, T, S)
Nisbah lulus daripada semakan yang boleh dikira: 6/6 A, ≥ 5/6 B, ≥ 3/6 C, ≥ 2/6 D, selainnya E. Kurang 4 semakan boleh dikira → `–`.

## 4. Gabungan
- Gred = purata mata K, U, T, S (A = 4 … E = 0; ≥ 3.5 A, ≥ 2.5 B, ≥ 1.5 C, ≥ 0.5 D). Perlu K dan ≥ 3 sub-gred.
- Had: gred ≤ K + 1 huruf.
- Histerisis (Altman & Rijken; MSCI): gred dikira pada 3 suku terakhir (point-in-time); ubah 1 huruf hanya jika 2 suku berturut menunjuk arah sama; ubah ≥ 2 huruf terus.
- Bank, insurans, REIT: model berasingan (§13, v7.1). Sektor kewangan lain dengan penyata format syarikat biasa (pengurusan aset, pasaran modal, data kewangan, broker insurans, syarikat cangkerang): model standard (v7.1). (v7: semua `–`.)

## 5. Bendera forensik (F; menurunkan keyakinan sahaja)
`belum_terima>jualan` dan `inventori>jualan` (pertumbuhan > pertumbuhan hasil + 10 mata); `akruan_tinggi` ((untung − OCF) / aset > 10%); `beneish` (M 8 pembolehubah > −1.78); `ocf<50%_ebitda`; `tumbuh_bakar_nilai` (hasil > +20% tetapi ROIC < 9%). Ambang +10 mata, 10% dan 50% ialah andaian.

## 6. Label peringkat (Damodaran, Lynch)
`muda` (hasil > +20%, margin operasi < 5%); `merosot` (hasil turun 2 tahun dan margin operasi turun berbanding 2 tahun lalu); `kitaran` (kemeruapan EPS > median industri; tanpa median: sektor Energy / Basic Materials); `tumbuh laju` (hasil ≥ +15%, margin > 0); `matang` (hasil < +10%, FCF > 0); selainnya `lain`.

## 7. Syariah (paparan jarak, mata peratus di bawah had)
- Hutang berfaedah (tanpa pajakan) dan tunai berbanding jumlah aset (had 33%: MSCI/FTSE/SC) dan purata nilai pasaran 24 dan 36 bulan (had 30%: DJIM/S&P Ogos 2026; nilai pasaran = `issued_shares` semasa × purata harga, anggaran). Pendapatan faedah / hasil ≤ 5%.
- `gagal` (gred → E): hutang atau pendapatan faedah melebihi had dalam SEMUA kaedah yang boleh dikira (minimum 2). `gagal_sebahagian`: sebahagian kaedah, atau tunai sahaja (Moomoo tidak membezakan deposit Islam/konvensional). `hampir_had`: dalam 2 mata daripada had. Dua yang terakhir menurunkan keyakinan.

## 8. Keyakinan
Tinggi: ≥ 90% semakan boleh dikira dan jurang sub-gred ≤ 2 huruf. Rendah: < 70% atau A dan E serentak. Selainnya sederhana. Turun satu tahap bagi: ada bendera F; jumlah 4 suku ≠ tahunan (> 2%) dalam 5 tahun terakhir (penyataan semula atau penukaran mata wang; nota `suku_tidak_sepadan_tahunan`); industri perisian/internet (FCF belum tolak SBC); Syariah `gagal_sebahagian`/`hampir_had`.

## 9. Pengumpulan data (dalam sesi; Moomoo tiada dalam GitHub Actions)
Bagi setiap saham: `quote_financials_statements` statement_type 1, 2, 3 × financial_type 10 (suku + tahunan dalam satu panggilan; limit 50, currency_code USD; halaman 1 = 40 suku + 10 tahun, cukup untuk semua semakan) — atau financial_type 9 dan 7 berasingan (limit 50) — `quote_financials_earnings_price_history`, dan `quote_market_snapshot` (≤ 400 kod setiap panggilan). Simpan setiap hasil sebagai `<T>_<jenis>_<tempoh>.json`, `<T>_eph.json`, `<T>_snap.json` dalam satu folder, kemudian:
`python3 BacktestShariah2/standard/gred_kewangan.py simpan --folder <folder> --keluar BacktestShariah2/data/kewangan`.
Tanpa taip semula (sejak 19 Okt 2026): `python3 BacktestShariah2/standard/tuai_kewangan.py --transkrip ~/.claude/projects/<projek> --keluar <folder>` menuai hasil alat terus daripada transkrip sesi (termasuk sub-ejen dan hasil besar yang disimpan alat ke fail), memecah financial_type 10 kepada `_9`/`_7`, memecah snapshot berkelompok, dan menulis `tuai_status.json` (bahagian yang belum dikumpul; ret_code -10 "no data" = muktamad).
Had kadar Moomoo (diukur 19 Okt 2026): ~1 panggilan sesaat atau lebih (cth. 3 ejen × 4 panggilan serentak) mencetuskan had kadar dan sesi log masuk penyambung Moomoo luput (pengguna perlu log masuk semula). Guna SATU ejen, ≤ 2 panggilan setiap mesej (~0.4 panggilan sesaat).
Kemas kini hanya selepas syarikat melapor (tarikh earnings). Automatik sejak 20 Okt 2026: imbasan malam (`jadual/imbas_2002.md` langkah 5c) mengumpul ≤ 40 saham sehari daripada `tuai_kewangan.py perlu` (saham tanpa fail; saham aktif yang akhir suku terakhir + 136 hari < hari ini dan fail dikumpul > 7 hari lalu). `isi` tidak mengisi `moomoo.csv` (had saiz db). Jika folder `data/kewangan` wujud, `harian_c.py gred` dan `gred.py tambah --kewangan` mengisi lajur; tanpa fail saham → `–`.
Pelapor separuh tahun: lihat §12 (financial_type 11/5). Isi semula baris `–` sahaja (termasuk moomoo.csv): §14.
Isi semula baris sedia ada (posisi, senarai_beli, watchlist) pada tarikh asal setiap baris, lajur kewangan SAHAJA: `python3 BacktestShariah2/standard/gred_kewangan.py isi --folder BacktestShariah2/papertrade --kewangan BacktestShariah2/data/kewangan --harga BacktestShariah2/data/harga/stor`, kemudian `pecah_claude.py --pecah` (lajur baharu menambah ±85 bait setiap baris posisi) dan `sahkan.py --betulkan`. Sesi rujukan sama dengan `gred_kira_semula.py`: harga ≤ sesi isyarat, penyata yang diterbitkan ≤ hari imbasan asal. Dijalankan pertama kali 19 Okt 2026 (3,703 baris).

## 10. Belum disahkan / andaian
Baris S&P selain minimal dan aggressive; jadual low volatility (utiliti) daripada ingatan; zon Z'' 1.10; had S&P Shariah 2026 (30% atau 33%); ambang EBIT/faedah SWS (dokumen 5×, laman 3×); kos modal 9%; ambang DD; ambang forensik; ambang peringkat. Semua ambang ditetapkan sebelum ujian; komponen baharu hanya selepas ujian luar sampel.
v7.1 (andaian tambahan, belum disahkan): sandaran H1 + 90 hari; aliran tunai tahunan ganti <= 275 hari; jarak peralihan 126–160 hari; minimum 3 semakan bagi sejarah pendek; semua ambang model bank/insurans/REIT §13 (dibundarkan daripada rujukan; jalur S&P insurans dan REIT daripada ingatan, perlu disemak dengan dokumen asal); tanda Moomoo "Credit Losses Provision" (negatif = belanja) disahkan pada satu bank (JPM) sahaja.

## 11. Sambungan v7.1 (23 Okt 2026): hanya apabila v7 memberi `–`
Siasatan 23 Okt 2026 (550 baris `–`/kosong dalam moomoo.csv, claude*.csv, senarai_beli, watchlist) menemui punca berikut. Setiap sambungan menggantikan nilai `None` sahaja; semakan yang dikira melaluinya disenaraikan dalam `kewangan_butiran.semakan_ganti` dan tidak dikira dalam liputan keyakinan (§8).
- Punca "N suku; sub U:– T:–" (bukan medan dibuang semasa `simpan`; MEDAN memuatkan semua medan yang dipakai): (a) median industri memerlukan >= 5 rakan dalam `data/kewangan` (746 saham; banyak industri kurang); (b) tetingkap 5 tahun (24 suku) bagi syarikat muda / spin-off (GEV, ALAB, NXT …); (c) asas EPS/hasil <= 0 (pertumbuhan tidak ditakrif); (d) aliran tunai suku tiada (10-K belum difailkan, cth. AZO Q4; pelapor asing 6-K tanpa aliran tunai suku, cth. TCOM, CAAP, VET, GLOB); (e) ekuiti <= 0 (belian balik, cth. AZO, MCK, MKTW); (f) penyata pendapatan tahunan tiada dalam Moomoo (cth. AMR); (g) 4 saham sektor kewangan (ASST, IREN, MKTW, SVRN) ditolak oleh label "Financial Services" walaupun penyata mereka format syarikat biasa.
- Median: industri < 5 rakan -> median sektor (pemetaan `sektor_pasaran.SEKTOR_INDUSTRI`) -> median semua saham `data/kewangan`. Peringkat Damodaran/Lynch kekal memakai median industri v7 sahaja.
- Tetingkap "5 tahun" -> tetingkap terpanjang dalam tahun penuh (>= 2 tahun; `nisbah.tetingkap_tahun`) bagi EPS TTM, ROIC tambahan, purata pertumbuhan EPS dan hutang/ekuiti; margin operasi lawan tahun terawal (>= 2 tahun lalu); kemampanan ROE/FCF dengan 3–4 tahun = >= separuh.
- Asas <= 0: lulus hanya jika nilai semasa > 0 (pusing untung; hasil pertama), masih rugi = gagal. EPS semasa <= 0 -> "pertumbuhan 1 tahun > purata" gagal; asas 1 tahun <= 0 < semasa -> lulus. NOPAT <= 0 dengan modal dilabur <= 0 -> ROIC gagal. Modal dilabur tidak bertambah -> ROIC tambahan lulus hanya jika NOPAT naik. Ekuiti <= 0 -> semakan ROE/ROA memakai ROA >= 6% sahaja. Kemeruapan EPS tidak dapat dikira dan EPS tahunan <= 0 dalam 5 tahun (>= 3 tahun data) -> tidak stabil (Graham: untung setiap tahun). Hasil naik YoY: perbandingan yang ada (>= setahun tempoh) dengan ambang 75% (= 6/8).
- Aliran tunai ganti (nota `aliran_tunai_<sumber>`; keyakinan turun satu tahap): tetingkap berturut lengkap terkini yang lewat <= 2 tempoh, atau tahunan point-in-time yang tamat <= 275 hari sebelum akhir tetingkap. OCF > untung dan akruan dibanding dengan untung tempoh yang sama (`ni_tunai`); Beneish dan OCF/EBITDA tidak dinilai dengan aliran tunai ganti. D&A tiada -> D&A penyata pendapatan (medan baharu) atau tetingkap ganti.
- Tahunan tanpa penyata pendapatan/aliran tunai = jumlah 4 suku tahun kewangan sama (Q4 tamat ± 7 hari; `dijumlah_suku`).
- Data: label tempoh sama dengan tarikh akhir berbeza > 20 hari = tempoh berasingan (sebelum ini digabung, cth. FERG 2025/Q4 Jul dan Dis). Rantaian suku: satu jarak 126–160 hari dibenarkan jika label melangkau (peralihan tahun kewangan, cth. GEF Okt -> Sep 2025; nota `peralihan_tahun_kewangan`); jarak ~182 hari (suku hilang) tetap memutuskan rantaian. Suku tanpa penyata pendapatan diabaikan (rantaian putus di situ; sebab dicatat).
- Sebab `–` yang tepat: `kewangan_butiran.sebab` menyenaraikan sub-gred yang tidak dapat dikira (bilangan semakan boleh dikira) atau rantaian tempoh yang tidak mencukupi.

## 12. Tempoh separuh tahun, tahunan dan sejarah pendek (v7.1)
- Punca "< 8 suku berturut" (bukan halaman cache tiada: halaman 1 = 40 suku mencukupi; `has_more` hanya sejarah lebih lama): pelapor asing separuh tahun (BHP, RIO, WDS, SNN, HLN sejak 2025, WPP, GFI, HMY, DRD, SSL, PSO, ZGN, CYD, ELVR, SVRN, BUUU …) — Moomoo hanya menyimpan kunci kira-kira pada label Q2/Q4; penyata pendapatan H1 berada dalam laporan kumulatif `Q6` (financial_type 5). Juga: spin-off/penyenaraian baharu (VSNT, HQ), peralihan tahun kewangan (GEF, FERG), cache rosak (NWSA: label kalendar syarikat lain tanpa penyata pendapatan; dibina semula 23 Okt 2026).
- Separuh tahun: H1 = Q6 kumulatif; H2 = tahunan − H1 (medan aliran yang ada dalam kedua-duanya; EPS H2 = EPS tahunan − EPS H1, anggaran). Label `YYYY/Q2` (H1) dan `YYYY/Q4` (H2), sepadan rekod tarikh siaran Moomoo. TTM = 2 separuh; YoY = separuh sama tahun lalu; minimum 4 separuh (2 tahun); semua semakan §3 dengan n = 2 tempoh setahun. Tersedia: tarikh siaran, sandaran H1 + 90 hari, H2 + 60 hari (sama seperti tahunan). Basi: > 290 hari.
- Tahunan sahaja: TTM = tahun kewangan; minimum 2 tahun; basi > 475 hari.
- Sejarah pendek (4–7 suku; syarikat muda/spin-off): dinilai dengan suku yang ada; minimum 3 semakan bagi setiap sub-gred (bukan 4) dan >= 2 perbandingan hasil YoY; keyakinan sentiasa `rendah` (`sejarah pendek` dalam `kewangan_ringkas`).
- Keutamaan: suku (>= 8) -> separuh (>= 4) -> suku pendek (4–7) -> separuh pendek (2–3) -> tahunan (>= 2). Calon hanya sah jika tempoh terakhirnya ialah data terkini yang ada (cth. tahunan Dis 2025 tidak dipakai jika suku Mac 2026 ada — konsisten dengan peraturan basi). Data separuh tahun/tahunan: keyakinan turun satu tahap; `kewangan_ringkas` menanda `data separuh tahun` / `data tahun`.
- Pengumpulan (§9): pelapor separuh tahun — `quote_financials_statements` statement_type 1 (dan 3 jika berjaya) financial_type 11 (Q6 + tahunan; limit 50 menghasilkan fail, bukan teks dalam konteks) atau 5 (Q6 sahaja); `tuai_kewangan.py` menulis `<T>_<jenis>_6_c<halaman>.json` / `_7_c…` dan status `separuh`; `simpan` menyimpan senarai `separuh` dan `struktur`. Aliran tunai H1 pilihan (financial_type 11 jenis 3 kerap gagal "orchestration error"; tanpa itu aliran tunai = tahunan ganti §11).

## 13. Model bank / insurans / REIT (v7.1)
Sub-gred K/U/T/S setara (A–E; U/T/S = nisbah semakan lulus seperti §3; K = yang lebih teruk antara komponen), gabungan, had K + 1, histerisis, point-in-time, Syariah (§7) dan keyakinan (§8) sama. Tiada distance-to-default (Bharath & Shumway mengecualikan institusi kewangan). Medan Moomoo yang disimpan sejak 23 Okt 2026 (MEDAN; data lama tanpa medan ini perlu dikumpul semula): bank — Net Interest Income, -Interest Income, -Interest Expense, Non-Interest Income/Expense, Credit Losses Provision (Moomoo: negatif = belanja), Net Loan, Total Deposits, Goodwill and Other Intangible Assets, -Preferred Stock, Cash, Cash Equivalents & Federal Funds Sold; insurans — Total Premiums Earned, Net Investment Income, Loss Adjustment Expense, Policy Acquisition Expense, Underwriting Expenses, Policy Holders Liabilities, Total Investments; REIT — Depreciation & Amortization & Depletion (penyata pendapatan), Gain on Sale of Security, Asset Impairment Loss, Cash Dividends Paid. Penghala: `structure_name` Moomoo BANK_MSTAR / INSURANCE_MSTAR atau medan khas, kemudian label industri (Banks …, Insurance … kecuali Insurance Brokers, REIT …); sektor kewangan tanpa penyata format biasa dan tanpa medan bank/insurans -> `–` (kumpul semula).
### Bank
- K: TCE/aset nyata = (ekuiti induk − saham keutamaan − muhibah & tak ketara) / (aset − muhibah & tak ketara): >= 9% A, >= 7% B, >= 5% C, >= 4% D, selainnya E — proksi nisbah leveraj: FDIC Prompt Corrective Action (12 CFR 324.403: "well capitalized" leveraj Tier 1 >= 5%, "adequately capitalized" >= 4%); Basel III leveraj minimum 3% (BCBS, Jan 2014); TCE/TA dipakai Moody's (Banks Methodology). Pinjaman/deposit <= 80% A, <= 90% B, <= 100% C, <= 110% D, selainnya E (julat berhemat lazim analisis kecairan; andaian).
- U: ROA >= 1% (penanda aras industri; FDIC Quarterly Banking Profile); ROE >= 10% (anggaran kos ekuiti); nisbah kecekapan (belanja bukan faedah / (pendapatan faedah bersih + bukan faedah)) <= 60%; kos kredit (peruntukan TTM / purata pinjaman bersih) <= 1%; ROE tahunan >= 10% dalam >= separuh daripada <= 5 tahun (minimum 3).
- T: EPS TTM > EPS L tahun lalu (L = 5 atau terpanjang >= 2; asas <= 0: semasa > 0); pertumbuhan EPS 1 tahun > purata L tahun; EPS tempoh terkini YoY >= 10%; hasil tempoh terkini YoY >= 10%; hasil naik YoY >= 75% daripada <= 2 tahun tempoh; nilai buku (ekuiti induk) tumbuh YoY. Ambang 10% ialah andaian (pertumbuhan bank lebih perlahan daripada ambang O'Neil 18–20%).
- S (tempoh terkini lawan setahun lalu): ROA naik; kecekapan bertambah baik; TCE/aset tidak turun; kos kredit tidak naik; deposit tumbuh; tiada terbitan saham bersih 12 bulan.
- Syariah: pendapatan faedah = -Interest Income (perbankan konvensional lazimnya gagal saringan pendapatan faedah).
### Insurans
- K: leveraj kewangan hutang / (hutang + ekuiti) < 15% A, < 25% B, < 35% C, < 45% D, selainnya E; liputan caj tetap (untung sebelum cukai + faedah) / faedah >= 12× A, >= 8× B, >= 4× C, >= 2× D, selainnya E; hutang <= 1% aset -> A (jalur berasaskan jadual leveraj kewangan dan liputan caj tetap S&P Insurers Rating Methodology, dibundarkan; andaian).
- U: ROE >= 10%; ROA >= 1%; nisbah gabungan (kerugian & pelarasan + perolehan polisi + underwriting) / premium diperoleh < 100% (untung underwriting; P&C sahaja — tanpa medan kerugian: tidak dikira); margin sebelum cukai >= 10%; ROE mampan (seperti bank); OCF > untung bersih.
- T: seperti bank. S: nisbah gabungan turun; margin sebelum cukai naik; leveraj tidak naik; premium diperoleh tumbuh YoY; ROE TTM naik; tiada terbitan saham bersih.
- Syariah: pendapatan faedah = Net Investment Income (anggaran konservatif; insurans konvensional lazimnya gagal saringan aktiviti).
### REIT
- FFO anggaran (Nareit, FFO White Paper 2018): untung bersih induk + D&A (aliran tunai; sandaran penyata pendapatan) − untung jualan sekuriti/harta − item khas (caj rosot nilai ditambah balik). EBITDA = untung operasi + D&A.
- K: hutang / jumlah aset <= 35% A, <= 45% B, <= 55% C, <= 60% D, selainnya E (perjanjian bon tidak bercagar REIT lazim: jumlah hutang / jumlah aset <= 60%); EBITDA / faedah >= 5× A, >= 4× B, >= 3× C, >= 1.5× D, selainnya E (perjanjian lazim: liputan caj tetap >= 1.5×); hutang bersih / EBITDA < 5.5 A, < 6.5 B, < 7.5 C, < 9 D, selainnya E (REIT gred pelaburan lazimnya <= 6–7×). Ambang A–C ialah andaian.
- U: margin FFO >= 30%; FFO / purata ekuiti >= 8%; dividen tunai <= 90% FFO (REIT AS wajib mengagih >= 90% pendapatan bercukai, IRC §857; bayaran > 90% FFO kurang mampan); OCF >= dividen tunai; margin EBITDA >= 50%.
- T: FFO TTM > FFO L tahun lalu; pertumbuhan FFO 1 tahun > purata L tahun; FFO tempoh terkini YoY >= 10%; hasil tempoh terkini YoY >= 10%; hasil naik >= 75% tempoh (FFO keseluruhan, bukan sesaham: bilangan saham sejarah tiada dalam penyata).
- S: hutang/aset tidak naik; margin EBITDA naik; liputan faedah naik; FFO tempoh terkini naik YoY; tiada terbitan saham bersih; nisbah semasa naik.

## 14. Isi semula baris `–` (23 Okt 2026)
`python3 BacktestShariah2/standard/gred_kewangan_isi.py --harga BacktestShariah2/data/harga/stor [--uji]`: baris gred_kewangan kosong/`–` SAHAJA dalam moomoo.csv, claude*.csv, senarai_beli dan watchlist (tidak_dibeli/tidak_sah diabaikan). Sesi rujukan D = tarikh_isyarat / tarikh_data / sesi sebelum tarikh_beli; penyata yang diterbitkan <= tarikh imbasan dalam gred_pada (awalan tarikh, atau "pada YYYY-MM-DD") jika >= D, selainnya D; harga <= D. Lajur gred_kewangan, kewangan_ringkas, kewangan_tempoh; kewangan_butiran bagi senarai_beli/watchlist dan fail posisi yang sudah menyimpan butiran (atau `--butiran-posisi`; moomoo.csv tidak: had 256 KiB db); gred_pada + "kewangan isi semula <tarikh> (v7.1, penyata <= …)". Selepas tulis: `pecah_claude.py --pecah`, `sahkan.py --betulkan`.
Baki `–` (uji 23 Okt 2026) ialah kekurangan data Moomoo sebenar, bukan peraturan: ASST (penyata pendapatan 2025/Q3 dan tahunan 2025 tiada; Q9 kumulatif 2025 juga tiada), FERG (suku Mei–Jul 2025 tiada; tahun 2025 Moomoo = tempoh peralihan Ogo–Dis), VSNT dan HQ (spin-off/penyenaraian baharu: 2 suku berturut), BUUU (separuh tahun terkini Dis 2025 > 290 hari / tahunan Jun 2025 > 475 hari), VECO dan NVO (penyata 2026/Q2 belum ada dalam Moomoo: data basi), TLK dan SQM (aliran tunai Moomoo tanpa OCF dan D&A: K tidak dapat dikira), BKHA (syarikat cangkerang tanpa operasi).
