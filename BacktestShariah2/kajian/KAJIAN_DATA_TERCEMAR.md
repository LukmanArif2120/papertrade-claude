# Kajian data tercemar — data hadapan (22 Okt 2026)

Permintaan pengguna 22 Okt 2026: kaji semua punca yang boleh mengganggu data hadapan (isyarat entry/keluar palsu, harga salah,
bias perbandingan) sebelum memutuskan penapis atau pembetulan seterusnya. Skop: **Papertrade C** (`papertrade/claude*.csv`) dan
**Lejar Penuh** (`lejar/`); backtest di luar skop. Kajian sahaja: tiada kod atau data diubah.

## Data dan kaedah
- C: 4,240 posisi dibeli 8–21 Okt 2026 (3,543 dengan bar hari beli dalam stor; belian 21 Okt belum ada bar). Lejar: 5,789 posisi
  (16–20 Okt; sebelum bina semula `tidak_layak`) dan bina semula percubaan 5,682 posisi (salinan scratch, 21 Okt).
- Stor harga `data/harga/stor/` hingga sesi 20 Okt (520 bar setiap saham). Tarikh earnings: lajur gred `tarikh_earnings`,
  `hari_ke_earnings`; Syariah: `kewangan_ringkas` (gred kewangan v7) dan `data/skrin/semak_shariah.csv`.
- Sumber: (1) log repo — `standard/binaan_v2_log*.md`, `bayang/`, `lejar/BANDING_C.md`, `status_harian.json` (insiden 12–22 Okt);
  (2) kajian web — dokumentasi yfinance, Nasdaq/NYSE/SEC/FINRA, CRSP, QuantConnect, kertas akademik (senarai sumber di hujung);
  (3) ukuran atas data (skrip scratch; angka di bawah). Angka bertanda "(log)" dipetik daripada log tanpa diukur semula.

## Ringkasan
1. **Pepijat yang sedang mencemar data (perlu dibaiki dahulu):**
   - B3: `lejar.py tampal_moomoo` menyimpan buka sementara 9:35 NY sebagai buka "Moomoo menang" dalam stor. Ia sudah tercemar bagi
     22 saham pada 20 Okt dan 33 saham pada 21 Okt (cth. KN 20 Okt: stor 34.10, buka rasmi 35.04), dan 52 posisi Lejar berbeza > 0.5% daripada C.
   - P1: `lejar.py semak` tidak mengenali sebab_keluar `delist`. CI akan gagal apabila Lejar menutup posisi delist pertama.
   - P2: `keluar_lorong.py` membuka semula lorong 2 bagi 89 posisi palsu ambil alih (status tanpa penanda `paras keluar`).
   - B5: `harian.yml` tiada gerbang masa, jadi bar separa intrahari boleh masuk stor (REF 21 Okt).
2. **Isyarat palsu yang sudah dikawal:** ambil alih tunai (89 C, `tidak_sah`), tidak cair (isyarat baharu) dan delist. Baki: 18 posisi C
   tidak cair masih dikira, dan ambil alih bayaran saham bergantung pada senarai manual.
3. **Isyarat palsu yang belum dikawal:** lonjakan melampau / bar salah (10 saham, 21 peristiwa dalam stor; C: ASST 10, SVRN 6), dua kelas
   saham syarikat sama (66 posisi C), dan saham volatiliti melampau (ATR > 8%: 53 C, 75 Lejar).
4. **Bias perbandingan (bukan palsu, tetapi paling besar kesannya):**
   - 27% posisi C dan 59% posisi Lejar berada dalam kluster ≥ 5 kaedah (saham dan hari sama).
   - 37% belian C dibuat ≤ 10 hari sebelum earnings.
   - Semua data datang dari 10 sesi dalam satu rejim, dan 62% posisi Lejar dibeli pada satu hari (16 Okt, hari pertama Lejar = opex bulanan).
   - 77% posisi C belum keluar (median 3 hari).
   - 134 kaedah diuji serentak (ujian berganda).
5. **Kesahihan universe:** 25% posisi C (1,063) ialah saham yang gred kewangan v7 nilai "Syariah gagal / gagal sebahagian". 68% posisi tiada
   pengesahan ETF Syariah (`tiada_maklumat`). Medan `is_shariah_compliant` TradingView kosong bagi AS.

## A. Isyarat palsu daripada tindakan korporat / jenis instrumen
| ID | Punca | Mekanisme | Ukuran (C / Lejar) | Kawalan |
|---|---|---|---|---|
| A1 | Ambil alih tunai (harga terkunci) | Lonjakan hari pengumuman kelihatan breakout; ruang naik ≈ 0 | 89 C `tidak_sah`; Lejar lama 83 (68 selepas umum) | Ya — `ambil_alih.py`, `tidak_layak.py`, 6:02 langkah 2c; Lejar bina semula (sahkan 22 Okt) |
| A2 | Ambil alih bayaran saham / campuran, tender offer | Harga ikut pembeli × nisbah (tidak terkunci); tender = terkunci ≥ 10–20 hari urus niaga | PEN (campuran) sahaja diketahui | Separa — senarai manual `data/ambil_alih.csv`; tiada pengesan berita/EDGAR (425, S-4, SC TO-T) |
| A3 | Tidak cair (kelas B, saham nipis) | Bar tanpa julat/volum → breakout dan henti palsu; isian buka mustahil | 18 C (BKHA 6, AKA 4, WLYB 2, MGRT 2, FEDU 2, SENEB 1, MAYS 1); Lejar 38 | Isyarat baharu: ya. Posisi C lama: belum diputuskan |
| A4 | Delist / tiada bar | Harga basi, posisi tersangkut | 0 terbuka kini (ATKR ditutup sebagai A1) | Ya — tutup pada tutup akhir. Pepijat P1 |
| A5 | Lonjakan melampau, pump/squeeze, bar salah | Pulangan > +100% atau < −60% sehari lalu berbalik → isyarat momentum/volum palsu | Stor: 21 peristiwa / 10 saham (PHOE +997% → −87%, RPGL, VEEE, KELYB, MGRT, SVRN, ASST, AGL, AGPU, AEBI). C: ASST 10, SVRN 6 (log); lonjak-balik 25%/20%: 7 C (HQ, SVRN, TANH) | Tiada |
| A6 | Dua kelas saham syarikat sama (FOX/FOXA, NWS/NWSA, BELFA/B, RUSHA/B, SENEA/B, WLY/WLYB) | Satu isyarat dikira dua kali; satu kelas biasanya tidak cair | 66 C | Tiada |
| A7 | Split / reverse split tidak dilaras | Lompatan 1/k atau ×k palsu | Ujian nisbah (k ≥ 2) atas 120 bar saham C/Lejar: 0 split tidak dilaras (PRIM, WGS = kejatuhan earnings, bukan split). Lejar: 0 posisi `laras` > 15% | Separa — yfinance melaras split; C lorong 1 tiada laras; tiada pengesan nisbah |
| A8 | Dividen khas / ≥ 25%, spin-off, rights | Jurang ex-date kelihatan breakdown / kena henti | Tidak diukur (tiada data tindakan korporat dalam stor; `auto_adjust=False`, `actions=False`) | Tiada |
| A9 | IPO baharu / sejarah pendek, lock-up | Penunjuk belum stabil; tekanan lock-up | 4 C (HQ 148 bar, PARK, VSNT, BLLN < 260 bar) | Separa — `PERLU_BAR`/`WARM` setiap kaedah |
| A10 | Jenis instrumen bukan saham (ADR, dana, ETF, keutamaan, unit/waran, SPAC) | Pemandu harga lain (NAV, FX, trust $10) | 0 C / 0 Lejar ikut nama TradingView | Cukup buat masa ini (universe Moomoo/Shariah); tiada semakan jenis |
| A11 | Tawaran saham susulan / ATM | Jurang buka ≤ −5% pada volum ≥ 3× | 2 C, 1 Lejar pada hari beli | Tiada |

## B. Harga dan vendor data
| ID | Punca | Ukuran | Kawalan |
|---|---|---|---|
| B1 | Buka sementara 9:35 NY ≠ buka rasmi kline | (log) 213–553 baris dibetulkan sehari, 23–58 beza > 0.5%; semakan sampel "SAMA" dalam log beli 9:35 tidak berkesan | Ya — 6:02 §5.2 membetulkan harga_beli |
| B2 | Moomoo ≠ yfinance (buka; rendah sub-sen) | 59 C (1.4%) beza > 0.5% dengan buka stor: 24 saham 20 Okt (KN +2.8%, OII, RYZ +1.9%), DAC −3.5% (12 Okt, belum disahkan), SENEB/WLYB (tidak cair). SBH 19 Okt: kena henti dalam C, tidak dalam Lejar (log) | Separa — "Moomoo menang" (lihat B3) |
| B3 | **`tampal_moomoo` menyimpan buka sementara** | Stor 20 Okt: 22 saham (KN 34.10 lawan 35.04); 21 Okt: 33 saham (FC 17.95 lawan 18.39); 52 posisi Lejar beza > 0.5% daripada C (log, KN disahkan) | **BELUM** — `nota.contains('kline')` turut sepadan "buka sementara … (sahkan kline …)"; `keep='first'` menghalang nilai disahkan |
| B4 | Tarikan yfinance awal / bar hilang setiap saham | (log) 16 Okt: 110 posisi Lejar salah harga, diproses semula; 50 ticker tiada bar 20 Okt. Ukuran: 1 bar hilang dalam pegangan (ET) | Separa — liputan ≥ 99% dan masa ≥ 00:20 UTC; tiada semakan setiap saham |
| B5 | **Bar separa intrahari (harian.yml semasa pasaran)** | REF 21 Okt (log) | **BELUM** — tiada gerbang masa |
| B6 | Pelarasan sejarah / dividen mengubah bar lama | Lejar `laras` (INTU ×1.0047, WLYB ×1.0037; log) | Ya bagi Lejar; C tiada |
| B7 | Bar tidak sah (tinggi < buka/tutup, harga ≤ 0, bar salinan) | 0 OHLC tidak sah; bar salinan 35 C (BKHA, DV, FEDU, MAYS, MGRT, SENEB, WLYB = tidak cair/terkunci) | Separa (tidak cair) |
| B8 | Buka lelongan lawan cetakan pertama (yfinance Open ≠ NOOP/NYSE open) | Sebahagian beza B2 | Tiada — konvensyen isian tidak direkod |

## C. Proses, peraturan dan kod
| ID | Punca | Ukuran | Kawalan |
|---|---|---|---|
| C1 | "Belum didagangkan 9:36" dilangkau dalam C, tetapi dibeli Lejar pada buka rasmi | 12–19 baris sehari (log) | Tiada — set C ≠ Lejar |
| C2 | Rutin 9:35 tidak menilai peraturan buka kaedah (`buka_maks`/`nota_henti` kosong bagi ~130 kaedah) | 27 baris jadi TIDAK DIBELI keesokannya (log) | Separa — §5.4 esok; `harian_c.py beli` menilai |
| C3 | Logik keluar Lejar ≠ C/Actions | GEF M76, DELL M81 (log); punca belum disiasat | **BELUM** |
| C4 | Rekod ke belakang 12 Okt (kohort pra-Lejar) | 598 posisi (276 slot penuh + 322) | Diterima; harga = buka stor |
| C5 | Gred diisi semula ke belakang (pandang depan) | 1,126 posisi 17 Okt (log) | Ya — dikira semula pada tarikh isyarat |
| C6 | Sambungan Moomoo/SST luput | Gred P/QR "–", medan SST basi (log) | Dicatat sahaja |
| C7 | Drift universe apabila Lejar dibina semula (univ.txt semasa, bukan ikut tarikh) | 49 posisi Lejar berubah (hilang 25, tambah 24; 13 saham) | Tiada universe ikut tarikh |
| P1 | **`lejar.py semak` tidak terima `delist`** | Belum berlaku | **BELUM** (ralat saya, 21 Okt) |
| P2 | **Lorong 2 dibuka semula bagi posisi palsu** | 89 C | **BELUM** (ralat saya, 21 Okt; kesan kecil kerana `tidak_sah`) |
| C8 | Peraturan berubah semasa ujian (lorong 2 ×3, penapis 21 Okt) | Semua kohort sebelum 19/21 Okt | Ya — VERSI + bina semula; perlu dilapor ikut versi |

## D. Bias perbandingan dan statistik
| ID | Punca | Ukuran | Kesan |
|---|---|---|---|
| D1 | Kluster: banyak kaedah beli saham sama hari sama | C: 157 kluster ≥ 5 kaedah = 1,165 posisi (27%); terbesar RAMP 20 Okt 18, CTSH 16 Okt 17, BIIB 21 Okt 17, BRZE 21 Okt 13. Lejar: 3,397 (59%) ≥ 5; 1,580 ≥ 10 | Kaedah tidak bebas; satu peristiwa = puluhan "dagangan". Saiz sampel sebenar ≈ pasangan (saham, hari) unik |
| D2 | Tempoh pendek, satu rejim, belum matang | C dibeli dalam 10 sesi (8–21 Okt; 819 pada 16 Okt); Lejar 3,575/5,789 (62%) pada 16 Okt. 77% C belum keluar lorong 1 (median 3 hari) | Purata kaedah kini = beta pasaran dua minggu; tidak setanding backtest 2019–2026 |
| D3 | Musim earnings | 1,393/3,774 (37%) belian ≤ 10 hari ke earnings; 34 posisi sudah melintas earnings | Jurang earnings menguasai pulangan swing; bukan kelebihan kaedah |
| D4 | Volatiliti melampau | ATR14 > 8% harga: 53 C (FSLY, GRAL, BUUU, SVRN, BKHA, MXL), 75 Lejar; > 5%: 323 C | Satu dagangan ekstrem menguasai purata kaedah kecil |
| D5 | Jurang buka hari beli | \|jurang\| > 3%: 104 C, 106 Lejar; > +5%: 10 C | Isian jauh daripada harga isyarat |
| D6 | Sekatan jualan singkat (Reg SHO 201) selepas hari −10% | 21 C, 27 Lejar dibeli sehari selepas | Dinamik pantulan berat sebelah |
| D7 | Spread lebar (anggaran Corwin–Schultz 20 hari) | > 2%: 31 C, 49 Lejar (> 1%: 719 C — penganggar bising) | Kos isian sebenar lebih tinggi |
| D8 | Ujian berganda 134 kaedah, memilih "pemenang" daripada data hadapan | 134 kaedah, ~10 sesi | Pemenang awal kebanyakannya hingar; perlu Deflated Sharpe / PBO / ambang t > 3 |
| D9 | Hari opex bulanan / indeks | 16 Okt = opex (819 C, 3,575 Lejar) | Kecil; perlu ditanda sahaja |

## E. Kesahihan universe (Syariah, harga)
| ID | Punca | Ukuran | Kawalan |
|---|---|---|---|
| E1 | Status Syariah tidak disahkan / gagal nisbah kewangan | `kewangan_ringkas`: lulus 2,635, gagal sebahagian 952, gagal 111, hampir had 256, kosong 286 → 1,063 C (25%) gagal/gagal sebahagian. `semak_shariah`: tiada_maklumat 2,880, disahkan_etf 970, sp500_tiada_spus 372 | Rekod sahaja (gred kewangan); universe = skrin Moomoo |
| E2 | Saringan universe ikut nilai semasa (harga ≥ 10, Syariah) bukan ikut tarikh | Lejar 12 posisi harga_beli < 10 (penapis tutup isyarat ≥ 10) | Separa |

## Cadangan (ikut keutamaan; menunggu keputusan pengguna)
1. **Pepijat (P1, P2, B3, B5):** baiki `semak` (terima `delist`); bekukan lorong 2 bagi baris `tidak_sah` / `delist`; `tampal_moomoo`
   hanya menerima nota `buka rasmi … (kline …)` dan nilai terkini menang; gerbang masa `harian.yml`; kemudian bina semula stor buka 20–21 Okt
   dan Lejar.
2. **Penapis isyarat baharu (melalui `tidak_layak.py`):** A5 lonjakan/bar salah (pulangan sehari > +100% / < −60% dengan pembalikan → tolak
   20 sesi); A6 kelas berganda (simpan kelas paling cair sahaja); A2 ambil alih saham (berita Yahoo/EDGAR "to acquire <nama>" → calon
   senarai, disahkan manusia).
3. **Laporan perbandingan (tanpa ubah data):** Papan Penganalisis dan Lejar melapor juga (a) pasangan (saham, hari) unik, (b) tanpa
   kluster ≥ 5, (c) tanda earnings dalam pegangan, (d) median dan purata dipangkas, (e) posisi matang sahaja, (f) ikut VERSI peraturan,
   (g) ambang ujian berganda (Deflated Sharpe, N = 134).
4. **Keputusan pengguna:** E1 Syariah (tapis "gagal" atau rekod sahaja?); A3 18 posisi C tidak cair (`tidak_sah` atau kekal).
5. **Pemantauan:** C1/C3 (set C ≠ Lejar), A8 (perlu data tindakan korporat — yfinance `actions=True` atau Moomoo
   `quote_corporate_actions_*` seminggu sekali).

## Sumber utama
- yfinance: Price repair https://github.com/ranaroussi/yfinance/wiki/Price-repair ; auto_adjust lalai #2422
  https://github.com/ranaroussi/yfinance/issues/2422 ; bar hidup berganda PR #1070 / #2389 ; sesi hilang #2621 ; CHANGELOG
  https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst
- Buka lelongan: Nasdaq cross FAQ https://www.nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf ; NYSE
  https://www.nyse.com/publicdocs/nyse/markets/nyse/NYSE_Opening_and_Closing_Auctions_Fact_Sheet.pdf
- Henti dagangan dan LULD: https://nasdaqtrader.com/Trader.aspx?id=TradeHaltCodes ; https://www.finra.org/filing-reporting/trf/limit-uplimit-down-luld-plan ;
  Reg SHO 201 https://www.sec.gov/divisions/marketreg/rule201faq.htm
- Tindakan korporat: Nasdaq Daily List https://m.nasdaqtrader.com/content/technicalSupport/specifications/dataproducts/dlcompletespec.pdf ;
  akhiran ke-5 Nasdaq https://m.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/nasdaqfifthcharactersuffixlist.pdf ;
  QuantConnect https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/us-equity/corporate-actions ;
  tender 10 hari (Apr 2026) https://www.clearygottlieb.com/-/media/files/alert-memos-2026/sec-reduces-minimum-equity-tender-offer-period-to-10-business-days.pdf
- Jenis instrumen: CRSP share code https://www.crsp.org/wp-content/uploads/ShareCode.html ; direktori simbol https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
- Bias: Luo et al., Seven Sins of Quantitative Investing https://columbia.edu/~nyc2107/papers/seven_sins_of_quantitative_investing.pdf ;
  Bailey et al. PBO https://papers.ssrn.com/abstract=2326253 ; Deflated Sharpe https://papers.ssrn.com/abstract=2460551 ;
  Harvey, Liu & Zhu https://www.nber.org/papers/w20592 ; White Reality Check
  https://www.econometricsociety.org/publications/econometrica/2000/09/01/reality-check-data-snooping ; McLean & Pontiff
  https://ivey.uwo.ca/media/3775549/pontiff.pdf ; Petersen (ralat piawai berkelompok) https://www.nber.org/papers/w11280.pdf ;
  Corwin & Schultz https://projects.nber.org/confer/2009/mms09/Corwin_Schultz.pdf ; Mitchell & Pulvino (arbitraj merger)
  https://ideas.repec.org/a/bla/jfinan/v56y2001i6p2135-2175.html
- Senarai penuh 58 punca daripada kajian web (dengan peraturan pengesanan) disimpan dalam sejarah sesi Claude 22 Okt 2026; item yang
  relevan sudah dipetakan ke ID A–E di atas.
