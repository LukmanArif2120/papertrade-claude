# Tugasan v3 — Peraturan tunggal papertrade harian (berkuat kuasa 14 Okt 2026)

Dokumen ini **satu-satunya** rujukan peraturan bagi tugasan harian. Ia menggantikan `tugasan_v2.md`, `papertrade_harian.md` dan bahagian 5 `00_NOTA_SERAHAN.md` (semuanya kini bertanda TERBATAL; dikekalkan untuk sejarah sahaja). Jika ada percanggahan, dokumen ini menang. Langkah setiap tugasan ada dalam `BacktestShariah2/jadual/`.

## 1. Mod
- Papertrade C (Claude, maya) SAHAJA untuk belian baharu sejak 13 Okt 2026, dilayan seperti papertrade sebenar di Moomoo: harga buka sebenar, tiada pandang belakang.
- Tiada order Moomoo (tiada `sim_trade_input_order`, tiada `trading_order_*`). Tiada jualan. Tiada wang sebenar tanpa kelulusan pengguna.
- Hook projek `.claude/settings.json` (sejak 16 Okt 2026): PreToolUse menyekat semua alat order (`trading_order_*`, `sim_trade_input/modify/cancel_order`, `crypto_account_create/modify/cancel_order`) tanpa mengira awalan pelayan; SessionStart memasang `requirements.txt` dalam sesi awan. Jangan buang atau longgarkan hook ini.
- Posisi Moomoo lama (akaun simulasi AS acc_id 4135388, market 100) kekal dikemas kini harganya sahaja.
- Prinsip pengguna: "Kalau tak beli, cakap tak beli." Data mesti betul; jangan reka.
- Hari operasi: hari dagangan NYSE sahaja (semak `quote_trading_days` / `quote_market_state`; cuti = catat dan berhenti).

## 2. Jadual (semua tugasan guna model `claude-sonnet-5-5`)
| Tugasan | Masa | Prosedur |
|---|---|---|
| Kemas kini | 6:02 pagi MYT, Selasa–Sabtu | `jadual/kemas_kini_0602.md` |
| Imbas pasaran | 7:47 malam MYT, Isnin–Jumaat (dahulu 8:02) | `jadual/imbas_2002.md` |
| Beli maya | 9:35 pagi New York, Isnin–Jumaat | `jadual/beli_0935.md` |

Pada 6:02 pagi SEMUA data dashboard dikemas kini: Sector, Watchlist, Paper Trade M, Papertrade C, Prestasi, `harian/status`.

## 3. Kaedah dan isyarat
- 134 kaedah M (87 asal + 47 calon K145+ M115–M161 sejak 16 Okt 2026: entry daripada `spec/KATALOG_K145.md`, henti/keluar/tempoh = pilihan WFO suku terkini dibekukan sebagai varian V1; tiada `hampir()` → tiada watchlist bagi kaedah ini; prestasi luar sampel: `WFO/laporan/W01_LAPORAN.md`); varian dipilih dalam registry set 431: skor tertinggi bukan DITOLAK, jika tiada, CAGR tertinggi. Indikator I01–I32 tidak digunakan.
- Kod isyarat: `BacktestShariah2/kod/` (sumber kebenaran; lihat `kod/README.md`). Enjin v1.2 beku.
- Skop imbasan: saham AS Shariah (screener Moomoo) harga ≥ USD10; senarai 431 diutamakan.
- **Senarai beli** = isyarat entry 100% dipenuhi pada tutup sesi DAN lulus kesahihan:
  - (a) Isyarat MINGGUAN (M52 dan modul yang guna `akhir`) sah hanya jika sesi itu hari dagangan terakhir minggu.
  - (b) Setiap baris wajib ada `henti`, `nota_henti` (formula jika henti bergantung pada buka masuk, cth. M52 = 0.60×buka), `buka_maks` (cth. M08 = 1.05×SMA20, M06 = 1.05×pangsi, M20/M19 = sasaran) dan `sasaran`, diambil daripada `sedia()` modul kaedah.
- **Saham diambil alih (keputusan pengguna 21 Okt 2026)** = isyarat palsu: tiada senarai beli, tiada watchlist, tiada belian Lejar Penuh. Harga sasaran ambil alih tunai terkunci pada harga tawaran (BRZE 20 Okt: 13 kaedah membeli selepas Salesforce mengumumkan belian). Penapis `kod/ambil_alih.py` (dipakai `scanner.py`, `harian_c.py`, `lejar.py`): corak harga (jurang buka ≥ +10%, volum ≥ 4× median 50 hari, julat ≤ 3% pada hari pengumuman; kekal selagi 10 bar terakhir median julat ≤ 1.5% dan julat tutup ≤ 4%) ATAU senarai sah `data/ambil_alih.csv` (tambah baris bagi perjanjian bayaran saham/campuran yang tidak terkunci; `bayaran` = `bukan` mematikan pengesanan bagi saham yang tersilap dikesan). Posisi C yang dibeli pada/selepas tarikh pengumuman: `tidak_sah` + kedua-dua lorong ditutup pada tutup bar terakhir (`kod/tidak_layak.py posisi --tulis`, setiap pagi selepas langkah keluar). Posisi yang dibeli sebelum pengumuman kekal sah.
- **Saham tidak cair (21 Okt 2026)**: 20 bar terakhir ada ≥ 3 bar tanpa julat (tinggi = rendah), ≥ 2 bar tanpa volum, atau median nilai dagangan (tutup × volum) < USD100 ribu (cth. BIO.B, KELYB, SENEB) → isyarat ditolak (senarai beli, watchlist, Lejar Penuh); posisi sedia ada tidak diubah. `kod/tidak_layak.py`.
- **Lapisan EDGAR (22 Okt 2026)**: `edgar.yml` / `standard/tawaran_edgar.py` membaca indeks harian EDGAR: subject company bagi SC TO-T, SC 14D9, SC 13E3 dan 425 (satu subject) dalam universe → baris aktif `data/ambil_alih.csv` (bayaran `edgar`); 25-NSE → `tarikh_tamat`; PREM14A/DEFM14A dan 425 berbilang subject → `data/edgar/calon.csv` (semak manual). Isyarat tender/pertukaran saham/campuran ditapis dari tarikh pemfailan seperti ambil alih tunai.
- **Kelas berganda (22 Okt 2026)**: syarikat dengan lebih satu kelas saham (`data/kelas_berganda.csv`, disemak manual): hanya kelas paling cair (median nilai 20 bar) diimbas; posisi C kaedah+hari beli sama yang membeli dua kelas → kelas kurang cair `tidak_sah` (`tidak_layak.py posisi`). Pintu akhir semua penapis tidak layak bagi `senarai_beli.csv` dan `watchlist.csv` (termasuk baris watchlist yang dibawa): `kod/tidak_layak.py fail --tulis` (imbas 8:02 langkah 6, beli 9:35 langkah 1).
- **Saham delist / tiada data (21 Okt 2026)**: tiada bar ≥ 10 sesi pasaran (5 sebelum 22 Okt 2026) → posisi terbuka (lorong yang belum keluar) ditutup pada tutup bar terakhir; kekal sah (cth. ATKR selepas Prysmian siap). C: `tidak_layak.py posisi`; Lejar: sebab_keluar `delist`.
- **Watchlist (Hampir Signal)** = 90–99% dipenuhi (semua syarat kecuali pencetus; pencetus dalam ≤ 2%; pencetus kalendar ≤ 3 hari dagangan). Maks 5 setiap kaedah (431 dahulu, kemudian skor).
  - Dinilai semula pada 6:02 pagi DAN imbasan malam (7:47). Terkeluar signal (< 90% atau isyarat batal/tidak sah) → BUANG serta-merta.
  - Calon baharu hanya ditambah pada imbasan malam. Calon yang menjadi 100% dipindah ke senarai beli pada imbasan malam.
  - Peraturan lama "buang selepas 10 hari" dimansuhkan.
- **Belian semula (keputusan pengguna 16 Okt 2026; dipinda 17 Okt 2026):** saham yang sudah keluar TIDAK diabaikan. Ia terus diimbas oleh semua kaedah; isyarat 100% baharu = belian ke-2, ke-3 … (lajur `belian_ke`). Yang dikecualikan hanya posisi Claude yang MASIH TERBUKA bagi kaedah yang sama (kaedah lain tetap boleh, dengan `kaedah_kongsi`). Posisi dikira terbuka selagi lorong 1 (kaedah) belum keluar (`keluar`; sejak 19 Okt 2026 — 17–18 Okt: sehingga `tutup_semua` = True); lorong 2 (§5.3a) tidak menyekat belian semula; `kod/scanner.py pegangan_c` melaksanakannya. Prestasi belian semula dinilai berasingan selepas ≥ 20 dagangan tertutup.

## 4. Belian maya (9:35 NY)
- Calon = semua baris senarai_beli (tiada had slot). 1 unit setiap saham; kaedah kedua untuk saham sama = baris dengan `kaedah_kongsi`.
- Langkau jika: buka ≤ henti; buka > buka_maks; buka ≥ sasaran (jika kaedah melangkau); isyarat batal; kunci kaedah+saham+tarikh_isyarat sudah wujud dalam claude*.csv.
- Belum didagangkan pada masa belian (buka = 0, high/low = 0; sejak 22 Okt 2026): TIDAK dilangkau — direkod dengan harga sementara = tutup isyarat dan nota `buka sementara … buka_lewat`; buka rasmi dan kesahihan (§5.4) disahkan dengan bar harian keesokannya, sama seperti Lejar yang membeli pada buka rasmi. Melangkaunya hanya dalam C mencipta bias (hentian berita dan pembukaan lewat bukan rawak).
- Harga beli = harga buka sebenar. Buka sementara disahkan dengan kline harian; larian 6:02 membetulkan baki.

## 5. Kualiti data (wajib)
1. `quote_stock_quote` dengan low/high = 0 bermaksud tiada dagangan; JANGAN tafsir sebagai kena henti. Guna kline harian.
2. Harga beli = `open` kline harian rasmi hari beli.
3. Keluar dinilai dengan enjin rasmi (`kod/`) dan `standard/harian_nilai_keluar.py` fungsi `keluar()`. Kaedah replika (`kod/dagangan.py`
   REPLIKA, sejak 22 Okt 2026): lajur exitc/tgt modul ialah milik dagangan replika (bermula WARM), jadi posisi yang isyaratnya jatuh
   semasa replika memegang dagangan lain mesti dinilai dengan `dagangan.sedia_dagangan()` (dagangan sendiri); rutin 6:02 langkah 2c
   `dagangan.py betul` membetulkannya secara automatik. Lejar dan `harian_c.py` memakainya terus:
   - henti dinilai dari hari masuk (buka jurang bawah henti dari hari kedua → harga buka);
   - sasaran hanya dari hari selepas hari masuk, dengan tgt hari sebelumnya;
   - isyarat keluar kaedah → jual pada BUKA hari berikutnya; had masa → tutup.
   - Ujian: `python3 -m unittest discover -s BacktestShariah2/ujian`.
3a. **Dua lorong keluar (keputusan pengguna 17 Okt 2026; lorong 10% dibuang hari yang sama):** selain lorong 1 (peraturan kaedah, perkara 3), setiap posisi dinilai dengan lorong 2 "pegang selagi naik" (sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14 → jual pada buka esok; paras hanya naik; tanpa henti kaedah). Selepas lorong 1 dinilai: `python3 BacktestShariah2/standard/keluar_lorong.py --stor <folder stor kerja>`. Takrif lajur: `papertrade/SKEMA.md` (Dua lorong keluar). Lejar Penuh (`standard/lejar.py`) memakai peraturan sama: posisi kekal dalam `terbuka.csv` sehingga kedua-dua lorong keluar; hanya lorong 1 menyekat belian semula kaedah+saham sama.
4. Kesahihan belian: belian semalam disemak semula dengan `sedia()` atas bar hari beli. `sig` = False → baris TIDAK DIBELI (lihat `papertrade/SKEMA.md`). Baris `tidak_dibeli`/`tidak_sah` tidak dikira dalam prestasi atau pendedahan sektor.
5. Sebelum push data: `python3 BacktestShariah2/standard/sahkan.py --betulkan` MESTI keluar 0. Jika 1: betulkan; jika tidak boleh, JANGAN push fail data yang rosak — catat ralat dalam log dan push log sahaja.
6. Setiap saham wajib ada sektor & industri (SST `get_stock`, sandaran Moomoo `quote_owner_plate`; tiada → "Tiada data" + catat).

## 6. Stor
- Repo GitHub `pedagangsenja/papertrade-claude`, cawangan `main`. Mula: `git pull --rebase origin main`. Akhir: `git add -A`, commit, `git push origin main` (ditolak → pull --rebase, cuba semula maks 3 kali; tiada --force).
- Skema CSV: `papertrade/SKEMA.md`.
- Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (db melalui ArtifactData; muatkan skill artifact-capabilities). JANGAN cipta artifact baharu. Dokumen: `papertrade/moomoo`, `papertrade/claude`, `papertrade/claude_2` … `claude_N` (tanpa had sejak 16 Okt 2026; halaman melanggan nombor seterusnya secara automatik), `papertrade/watchlist`, `papertrade/senarai_beli` (kedua-duanya dibahagi oleh `standard/bahagi_db.py` kepada `<nama>`, `<nama>_2` …; halaman menggabung bahagian yang `induk`-nya sepadan), `sektor/snapshot`, `prestasi/mae`, `prestasi/ringkasan`, `harian/status`. JSON padat; setiap dokumen < 250 KB (had keras 262,144 bait). Dokumen claude_N membesar ±130 bait setiap posisi keluar: `standard/pecah_claude.py --pecah` memecah fail `claude*.csv` yang unjurannya > 240 KB (CI menyemak setiap push).
- Log: imbasan → `standard/binaan_v2_log.md`; kemas kini dan belian → `standard/binaan_v2_log_tambahan.md` (baca dahulu, tambah di hujung).
- Harga yfinance (sejak 14 Okt 2026): GitHub Actions `.github/workflows/harga_harian.yml` (21:37 UTC Isn–Jum, sandaran 00:23 UTC; jadual GitHub boleh lewat 2–4 jam, jadi rutin 6:02 menembak workflow ini sendiri jika data belum siap, `jadual/kemas_kini_0602.md` langkah 0a) menulis `data/harga/terkini.csv` (10 sesi terakhir; universe = set 431 + semua saham papertrade + `data/harga/univ.txt` + SPY/QQQ), `status.json`, dan `sejarah.csv` (3 tahun, bagi ticker dalam `perlu_sejarah.txt`). Skrip: `standard/harga_yf.py`. Sumber tidak rasmi: wajib semak silang dengan kline Moomoo sebelum guna (`harga_yf.py semak`); beza > 0.5% → Moomoo menang. Harga beli/keluar rasmi kekal = kline Moomoo (§5.2).
- Stor harga repo (sejak 16 Okt 2026): `data/harga/stor/harga_A.csv`, `harga_B.csv`, `harga_idx.csv` (format `kod/stor.py`, 520 bar) dikemas kini setiap malam oleh workflow Lejar penuh daripada `terkini.csv`. Rutin menyalinnya ke folder kerja (tidak lagi memakai aset dashboard `harga_aset` A/B/idx, yang tersangkut pada 12 Okt); jangan ubah atau commit folder ini.
- Alat besar: keputusan disimpan ke fail oleh sistem — proses dengan Python; jangan salin data harga secara manual. Had kline Moomoo ~4 panggilan seminit; maks 24 ticker setiap larian.
- Setiap panggilan `quote_history_kline` mesti menyatakan `autype` 0 (tanpa pelarasan; lalai Moomoo 1 = dilaras hadapan termasuk dividen, tidak sama dengan bar yfinance stor; sejak 22 Okt 2026). Peristiwa korporat (spin-off, dividen khas) dilaras melalui `data/harga/faktor.csv`, bukan melalui kline dilaras.

- **Konvensyen stor dan peristiwa besar (22 Okt 2026)**: bar stor sebelum ~2 Okt 2026 = data backtest (Moomoo dilaras hadapan termasuk dividen); bar yfinance selepasnya dilaras pecahan sahaja. `kod/stor.py nisbah_laras`: sejarah lama dilaras hanya jika nisbah bar bertindih seragam (serak ≤ 0.2%, ≥ 3 bar atau nisbah pecahan); selainnya 'anomali' (tidak dilaras); semua dilog `data/harga/stor/log_laras.csv`. Spin-off, dividen ≥ 2% harga dan pengagihan ≥ 25% dilaras hadapan melalui `data/harga/faktor.csv` (`kod/peristiwa.py`: dividen yfinance automatik; jurang ≤ −15% tanpa earnings → `faktor_calon.csv` → rutin 6:02 langkah 2d sahkan dengan Moomoo `quote_corporate_actions_rehab`). Lejar dibina semula apabila jadual berubah; posisi C merentasi tarikh_ex dilaras (`tidak_layak.py posisi`); posisi yang keluar 'kena henti' pada/selepas tarikh_ex tetapi Low tidak sampai henti dilaras dibuka semula (jurang peristiwa, bukan kejatuhan; RMR M99 19 Okt). Versi pustaka workflow dipin dalam `kekangan.txt`.

## 7. Prestasi
Papertrade M, Papertrade C (gabungan semua claude*.csv) dan Combine; baris sah sahaja. KPI, untung purata setiap kaedah, kadar menang, penurunan maksimum, Paling Teruk, skor Untung×Selamat. Skrip `standard/harian_prestasi.py <folder>` (DIBINA dan HARGA_PADA melalui env) dan `bina_p4_mae.py`; peraturan sama dengan halaman dashboard.
- Label (keputusan pengguna 14 Okt 2026): kaedah dengan **< 20 dagangan tertutup** = `BELUM CUKUP DATA`. Selepas ≥ 20: HENTIKAN jika untung purata ≤ −3% atau kadar gagal ≥ 75% atau skor < 25; TERUSKAN jika skor ≥ 55 dan untung purata > 0; selainnya PERHATI (gagal = % dagangan untung < 0; skor dibundar ke integer sebelum dibanding).
- Metrik portfolio dalam dolar: setiap posisi dianggap **USD1,000 (sama berat)**, bukan 1 unit. Rekod CSV kekal 1 unit.
- Ujian luar sampel backtest: tidak dibuat (keputusan pengguna 14 Okt 2026).

## 8. Gred calon (sejak 14 Okt 2026; keputusan pengguna: rekod dan uji dahulu, bukan penapis)
Lima gred A–E dikira pada hari isyarat oleh `standard/gred.py` dan direkod bersama setiap belian maya:
1. **Sektor** dan 2. **Industri** — v2 sejak 19 Okt 2026 (kajian 18 Okt 2026: `kajian/KAJIAN_GRED_KUMPULAN.md`; keputusan pengguna 18 Okt 2026). Kekuatan kumpulan SELURUH pasaran AS (~5,600 saham harga ≥ USD5; industri = plate Moomoo `papertrade/peta_industri.csv`, ~141 industri; sektor = 11 sektor Morningstar), dikira setiap hari oleh GitHub Actions `.github/workflows/gred_kumpulan.yml` (`standard/gred_kumpulan.py`, yfinance) → `data/kumpulan/gred_kumpulan.csv` (sejarah: `gred_kumpulan_sejarah.csv`). Indeks kumpulan = purata sama rata pulangan harian ahli.
   - **Industri**: skor 0–100 = pangkat persentil (Weinstein + pangkat median pulangan 1 bulan). Weinstein = purata 3 syarat: Mansfield RS lawan SPY > 0 (RS > purata 52 minggu), Mansfield RS naik dalam 21 sesi, indeks > purata 150 hari yang sedang naik. Kajian (dagangan 119 kaedah momentum 2019–2026; panel 5,546 saham; indeks industri): satu-satunya definisi yang tersusun A→E dan signifikan dalam ketiga-tiga ujian (t 2.7 / 2.1 / 2.7). Purata relatif setiap dagangan: A +0.03%, B −0.18%, C −0.40%, D −0.89%, E −1.21%; A dan E signifikan, B–D hampir neutral. Tidak terpakai bagi 15 kaedah pantulan (`kod/jenis_kaedah.csv`): tidak dikira dalam gred_keseluruhan kaedah itu. (Kajian berasingan `kajian/industri/RINGKASAN.md`, 2005–2026, tidak menguji Weinstein; varian terbaiknya 12−1 bulan dan 3M+6M, t ≈ 2.)
   - **Sektor**: skor = pangkat persentil % saham di atas SMA200 (menyusun pulangan indeks sektor, t 3.2) — paparan sahaja; tidak membantu memilih saham dalam kajian, jadi tidak dikira dalam gred_keseluruhan.
   - Gred: A > 80, B > 60, C > 40, D > 20, E ≤ 20. Setiap baris memakai snapshot yang sama tarikh dengan sesi isyaratnya (`tarikh_isyarat` / `tarikh_data`; tiada pandang hadapan, tiada data basi); jika tiada → "–". Dashboard Prestasi ikut gred hanya mengira gred S/I v2 (gred_pada ≥ 19 Okt 2026). Gred sebelum 19 Okt 2026 = v1 (skor panas 1W/1M/3M + breadth; kajian: tidak meramal) — jangan dicampur ketika menilai prestasi ikut gred.
3. **RS rating** (1–99, gaya IBD 40/20/20/20) — sejak 18 Okt 2026 dipangkat berbanding SELURUH pasaran AS harga ≥ USD5 (`standard/rs_pasaran.py`, Actions `rs_pasaran.yml` → `data/rs/`; sandaran stor harga, `rs_sumber`). Gred (keputusan pengguna 18 Okt 2026): A = RS 90–99 **disahkan**, B = 80–89 disahkan, C = 70–79 atau ≥ 80 tidak disahkan, D < 70; disahkan = saham naik 12 bulan, SPY > SMA200 dan Mansfield > 0 (`rs_sah`, sebab dalam `rs_tanda`; RS 95+ ditanda berisiko). Bukti: `kajian/rs/RINGKASAN.md` (3,830 saham 2005–2026, `standard/kajian_rs.py`): lebihan 63 hari atas pasaran A +1.5% (CI95 +0.8..+2.3), B +0.6%, C ≈ 0, D −0.2..−0.4%; RS tinggi kalah kepada pasaran apabila SPY < SMA200; RS 95+ median ≈ 0. Had: kelebihan tidak signifikan 2005–2015 dan bagi harga ≥ USD15; data tanpa saham delist. Dakwaan lama (431 saham, "+4.2%, mendahului setiap tahun") dibatalkan. RS tidak lagi dikira dalam gred keseluruhan; `rs_industri` direkod sahaja.
4. **Pemangkin** — Pemangkin v3 (sejak 18 Okt 2026; bukti dan kalibrasi: ulasan `standard/gred.py` dan data `data/pemangkin/sejarah/`): K1 earnings dijadualkan 6–21 hari dagangan lagi +2, 1–5 hari +1 (premium pengumuman; data 2012–2026: AR21 +0.2–0.4%, luar sampel t 3.4); K2 reaksi hari earnings ≥ +20% lawan SPY, umur ≤ 10 hari dagangan +4, 11–20 hari +3 (🔥 PANAS; AR21 +1.4–1.7%, bukti lemah); veto berita ≤ 20 hari dagangan: tawaran saham (pencairan) atau keputusan FDA akan datang → had C, sasaran ambil alih → had D. Gred A ≥ 3, B 2, C 1, D 0 (tiada pemangkin); E tidak dipakai. Tajuk berita, tindakan analisis, volum dan orang dalam tidak lagi diberi mata (diuji tiada nilai luar sampel / belum diuji). Data dikumpul seperti dahulu (Moomoo/SST atau GitHub Actions `pemangkin.yml` → `data/pemangkin/yahoo.json`, kalendar Nasdaq `earnings_nasdaq.json`); berita kini untuk veto dan pautan sahaja. Skala Berita Panas 15–17 Okt 2026 dibatalkan. K1 (jangkaan pulangan: earnings dalam tempoh pegang memberi lebihan purata) dan QR (risiko harga melompat melepasi henti pada hari laporan) mengukur perkara berbeza: baca bersama.
5. **QR** — hari dagangan ke laporan suku seterusnya (SST `market_events` 30 hari; kemudian kalendar Nasdaq `data/pemangkin/earnings_nasdaq.json` ≤ 4 hari; jika tiada, anggaran = earnings lalu + 91 hari). Makin jauh, makin kecil risiko jurang harga semasa pegang ~20 hari.

Gred keseluruhan (paparan) sejak 19 Okt 2026 = purata mata Industri (kecuali kaedah pantulan), Pemangkin dan QR (Sektor dan RS tidak dikira). Dashboard Prestasi memaparkan prestasi setiap gred; sesuatu gred hanya dinilai selepas ≥ 20 dagangan tertutup. Gred tidak menapis belian sehingga pengguna memutuskan berdasarkan data papertrade.

## 9. Lejar Penuh (fasa 1 sejak 16 Okt 2026; keputusan pengguna: data adil untuk semua kaedah)
- SEMUA isyarat setiap kaedah dibeli pada buka rasmi esok dan dikeluarkan mengikut peraturan kaedah itu (enjin v1.2), tanpa had 10 sekaedah dan tanpa keutamaan 431. Harga: stor repo (yfinance), semakan silang sampel Moomoo oleh rutin 6:02.
- Dijalankan oleh GitHub Actions `.github/workflows/lejar.yml` (06:17 UTC Sel–Sab, sandaran 10:17; sesi ditangguh jika data yfinance belum muktamad), tanpa LLM dan tanpa Moomoo; larian terlepas ditampung. Butiran: `lejar/README.md`, kod `standard/lejar.py`.
- Fasa 1 (2 minggu): berjalan selari; Papertrade C dan tiga rutin tidak berubah (kecuali sumber stor harga, §6). Rutin tidak menulis ke `lejar/`. Peralihan (rutin 9:35 NY dibersarakan, dsb.) hanya selepas pengguna meluluskan berdasarkan perbandingan.

## 10. Peralihan ke GitHub Actions (keputusan pengguna 17 Okt 2026; mod selari 3 hari dagangan)
- Kerja harian tanpa LLM: `standard/harian_c.py` (kemas kini posisi, imbas 134 kaedah, gred, beli 9:35 NY) dijalankan oleh
  `.github/workflows/harian.yml` (05:07 UTC Sel–Sab + sandaran), `beli.yml` (9:40 NY + sandaran) dan `petang.yml` (gred P).
  Peraturan sama dengan §3–§8 (ulang tayang 16–17 Okt: sama tepat dengan rutin Claude kecuali beza data; `jadual/PERALIHAN.md`).
- Harga: yfinance ditarik oleh `harian.yml` sendiri (05:07 UTC); sesi ditangguh jika data belum muktamad (pengawal sama dengan `lejar.py`: tarikan < 00:20 UTC selepas sesi atau liputan bar < 99%).
  Harga beli 9:35 NY = buka sementara yfinance, dibetulkan kepada buka bar harian muktamad oleh larian harian seterusnya (§5.2).
- Calon watchlist tanpa jarak pencetus boleh diukur (`jarak_pct` kosong) tidak dimasukkan (% hampir = 100 − jarak), sama seperti
  watchlist rutin Claude.
- `BacktestShariah2/MOD_ACTIONS` = `bayang`: Actions menulis ke `BacktestShariah2/bayang/` sahaja dan rutin Claude kekal rasmi (§2);
  `rasmi`: Actions menulis ke `papertrade/`, rutin Claude dimatikan, dashboard ditolak oleh `jadual/tolak_db.md` dan data
  Moomoo/SST dikumpul mingguan (`jadual/mingguan.md`).

## 11. Papan Penganalisis (keputusan pengguna 20 Okt 2026; rekod analisis sahaja, tidak menapis belian)
- Satu jadual banding semua kaedah aktif: `standard/penganalisis.py` → `laporan/PENGANALISIS.md` + `data/analisis/papan.json` (db
  `analisis/papan`, tab Analisis). GitHub Actions `analisis.yml` dicetus sebaik `lejar.yml` siap (~14:30 MYT), tanpa LLM; data
  dipapar di dashboard selepas tolakan db seterusnya (rutin 6:02 pagi; selepas peralihan `jadual/tolak_db.md`).
- Skor (purata pulangan bersih setiap dagangan) = (n0 × jangkaan backtest + n × purata posisi hadapan matang) ÷ (n0 + n). Jangkaan =
  purata set 431 varian aktif × (25% + 25% bagi setiap semakan luar sampel lulus: S1–S4 ≥ 3/4 atasi EW; WFO W01 CAGR > EW 423;
  AUTOTUNE A01 CAGR > SPY dalam kumpulan A dan B). n0 = 1 ÷ (1/30 + 1/dagangan backtest). Bukti hadapan = Lejar Penuh + kohort
  Papertrade C sebelum Lejar (tiada kiraan berganda: posisi Lejar yang isyaratnya jatuh semasa C pra-Lejar masih memegang
  kaedah+saham sama dibuang, seperti enjin); harga beli Lejar dilaras jika stor dilaras (split); matang = dibeli ≥ maks(14 hari, 1.5 × hari pegang backtest) lalu.
- Kukuh (keputusan pengguna 22 Okt 2026, `kajian/KAJIAN_DATA_TERCEMAR.md` R5–R7): n dalam skor = n berkesan (n ÷ kesan reka bentuk berkelompok ikut hari beli; < 5 hari beli berbeza → bilangan hari); median, hari
  beli berbeza, posisi lintas earnings dan purata tanpa earnings dilapor (tidak mengubah skor). Sejak 22 Okt 2026 (keputusan
  pengguna) purata hadapan = purata matang PENUH; purata dipangkas 5% dilapor sebagai semakan sahaja (pangkas menukar tanda
  purata kebanyakan kaedah swing kerana untung datang daripada ekor kanan).
- Status: BELUM CUKUP (< 20 matang atau < 10 hari beli berbeza), AMARAN (≥ 10 matang, t < −2 lawan jangkaan atas n berkesan),
  KUAT / LEMAH (julat 95% skor di atas / di bawah 0), PERHATI. Swing = pegang backtest 3–30 hari; kedudukan ikut skor sebulan (skor ÷ hari pegang × 21); < 100 dagangan backtest = sampel kecil.
