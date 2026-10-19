# Gred kewangan v7 (A–E)

Kod: `standard/gred_kewangan.py`. Ujian: `ujian/test_gred_kewangan.py`. Lajur: `gred_kewangan`, `kewangan_ringkas`, `kewangan_tempoh`, `kewangan_butiran` (senarai_beli, watchlist, fail posisi).
Status: rekod sahaja (keputusan pengguna 18 Okt 2026, selepas tujuh pusingan kajian). Belum diuji prestasi. TIDAK dimasukkan ke dalam `gred_keseluruhan` supaya rekod gred sedia ada kekal setanding.

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
- Bank, insurans, REIT, perkhidmatan kewangan: `–` (model lain diperlukan).

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
Kemas kini hanya selepas syarikat melapor (tarikh earnings). Jika folder `data/kewangan` wujud, `harian_c.py gred` dan `gred.py tambah --kewangan` mengisi lajur; tanpa fail saham → `–`.
Isi semula baris sedia ada (posisi, senarai_beli, watchlist) pada tarikh asal setiap baris, lajur kewangan SAHAJA: `python3 BacktestShariah2/standard/gred_kewangan.py isi --folder BacktestShariah2/papertrade --kewangan BacktestShariah2/data/kewangan --harga BacktestShariah2/data/harga/stor`, kemudian `pecah_claude.py --pecah` (lajur baharu menambah ±85 bait setiap baris posisi) dan `sahkan.py --betulkan`. Sesi rujukan sama dengan `gred_kira_semula.py`: harga ≤ sesi isyarat, penyata yang diterbitkan ≤ hari imbasan asal. Dijalankan pertama kali 19 Okt 2026 (3,703 baris).

## 10. Belum disahkan / andaian
Baris S&P selain minimal dan aggressive; jadual low volatility (utiliti) daripada ingatan; zon Z'' 1.10; had S&P Shariah 2026 (30% atau 33%); ambang EBIT/faedah SWS (dokumen 5×, laman 3×); kos modal 9%; ambang DD; ambang forensik; ambang peringkat. Semua ambang ditetapkan sebelum ujian; komponen baharu hanya selepas ujian luar sampel.
