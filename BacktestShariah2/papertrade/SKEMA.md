# Skema data papertrade (berkuat kuasa 14 Okt 2026)

Semakan automatik: `python3 BacktestShariah2/standard/sahkan.py` (kod keluar 1 = ada RALAT → jangan push data; betulkan dahulu).
`--betulkan` menyusun semula lajur fail posisi ikut susunan rasmi di bawah (nilai tidak diubah).

## Fail posisi: `moomoo.csv`, `claude.csv`, `claude_N.csv`
`claude.csv`, `claude_2.csv`, … dipadankan 1:1 dengan dokumen db dashboard `papertrade/claude`, `papertrade/claude_2`, … (had db ~256 KB setiap dokumen). Baris baharu ditambah ke fail bernombor terakhir. Papertrade C = gabungan semua fail `claude*.csv`.

Susunan lajur rasmi (lajur tambahan dibenarkan di hujung):

| Lajur | Jenis | Peraturan |
|---|---|---|
| tarikh_beli | YYYY-MM-DD | wajib kecuali baris tidak_dibeli |
| saham | ticker | wajib |
| kaedah, id_kaedah | Mxx | wajib (id_kaedah = kaedah bagi kaedah M) |
| sektor, industri | teks | wajib, bukan kosong/"-" (guna "Tiada data" jika benar-benar tiada) |
| harga_beli | nombor > 0 | = `open` kline harian rasmi hari beli; kosong jika tidak_dibeli |
| unit | integer > 0 | Papertrade C = 1; Moomoo warisan boleh > 1 |
| harga_terkini | nombor | tutup sesi terakhir; dibekukan selepas keluar |
| untung_pct | nombor 2 tp | = (harga_terkini/harga_beli − 1) × 100 (toleransi 0.02) |
| hari | integer | hari dagangan dipegang |
| henti, sasaran | nombor | paras enjin pada hari isyarat. Kosong = kaedah tanpa henti rugi (ADA_HENTI False: M01, M73, M82; dashboard "tiada henti (kaedah)"). Henti ikut tutup (modul `HENTI_TUTUP`, cth. M31 = LOWER BB hari isyarat; sejak 23 Okt 2026) direkod di sini untuk paparan/R sahaja — keluar tetap ikut exitc enjin. Isi semula: `standard/henti_isi.py`; `harian_c` mengisi henti kosong setiap malam |
| isyarat_keluar | teks | "Pegang …", "Keluar: …", "Isyarat keluar … (menunggu)", atau "TIDAK DIBELI" |
| keluar | True/False | True ⇒ tarikh_keluar, harga_keluar, untung_akhir_pct wajib; False ⇒ ketiga-tiganya kosong |
| tarikh_keluar | YYYY-MM-DD | ≥ tarikh_beli |
| harga_keluar | nombor | isyarat keluar kaedah = buka hari berikutnya; henti/sasaran = paras atau buka jurang; had masa = tutup |
| untung_akhir_pct | nombor 2 tp | = (harga_keluar/harga_beli − 1) × 100 |
| sumber | teks | harian_c, penuh_v1, penuh_20261012, harian, log_v1, luar |
| kaedah_kongsi | teks | kaedah lain yang berkongsi unit yang sama |
| tarikh_isyarat | YYYY-MM-DD | sesi isyarat entry. moomoo.csv sumber harian/log_v1: sesi sebelum tarikh_beli (isi 23 Okt 2026, `standard/isi_audit.py`); sumber luar (strategi luar) kosong |
| nota, dikesan | teks | nota bebas; masa larian yang mengesan keluar |
| nota (penanda tetap) | teks | Penanda yang dibaca kod (jangan ubah tangan): `buka sementara = tutup isyarat; buka_lewat: …` (saham belum didagangkan pada 9:36 NY; harga_beli sementara diganti buka rasmi malam itu); `buka rasmi <tarikh> (bar harian; disahkan …)` (harga_beli = buka rasmi; hanya baris ini disalin ke `stor/buka_moomoo.csv`); `faktor <jenis> <tarikh_ex> x<f>` (harga beli/henti/sasaran dilaras oleh `kod/peristiwa.py` sekali sahaja); `keluar dinilai semula … (dagangan sendiri, kod/dagangan.py)` (kaedah replika, sejak 22 Okt 2026) |
| tidak_sah | True/kosong | tidak dikira dalam prestasi/pendedahan. Sejak 21 Okt 2026 juga posisi yang dibeli pada/selepas pengumuman ambil alih (`sebab_tidak_sah` = `isyarat palsu: saham diambil alih (…)`; kedua-dua lorong ditutup pada tutup bar terakhir oleh `kod/tidak_layak.py posisi`). Sebab lain (`kod/tidak_layak.py posisi`): `isyarat palsu: saham tidak cair (…) pada <tarikh isyarat>`; `isyarat berganda: kelas berganda …` (kelas kurang cair, kaedah+hari sama; sejak 22 Okt 2026). Delist (tiada bar ≥ 10 sesi) ditutup pada tutup akhir tanpa tidak_sah |
| sebab_tidak_sah | teks | wajib jika tidak_sah |
| tidak_dibeli | True/kosong | belian tidak berlaku (langkau kaedah kena pada buka rasmi). harga_beli kosong, isyarat_keluar = "TIDAK DIBELI", keluar = False, tidak dikemas kini lagi |
| luar_peraturan | True/kosong | Moomoo sahaja: dibeli sebenar tetapi luar peraturan (kekal dikemas kini harga, tidak dikira) |
| harga_buka_rujukan, tarikh_beli_dirancang | nombor, tarikh | untuk baris tidak_dibeli |
| keluar_henti, tarikh_keluar_henti, harga_keluar_henti, untung_henti_pct, status_henti | True/False, tarikh, nombor, nombor 2 tp, teks | Lorong 2 (pegang selagi naik). Lihat bahagian Dua lorong keluar |
| tutup_semua | True/False | = keluar AND keluar_henti (rekod). Sejak 19 Okt 2026 belian semula kaedah+saham sama selepas `keluar` (lorong 1) = True; lorong 2 tidak menyekat (17–18 Okt: selepas tutup_semua) |

## Dua lorong keluar (keputusan pengguna 17 Okt 2026; lorong 10% dibuang hari yang sama)
Setiap posisi yang dibeli dinilai serentak dengan dua peraturan keluar dari harga beli yang sama. Setiap lorong direkod dalam lajurnya sendiri dan dibekukan sebaik keluar:
1. **Kaedah** (`keluar`, `tarikh_keluar`, `harga_keluar`, `untung_akhir_pct`, `isyarat_keluar`): peraturan penuh kaedah (henti, sasaran, isyarat keluar, had masa), seperti sebelum ini.
2. **Pegang selagi naik** (`*_henti`; dipinda 19 Okt 2026, kajian `kajian/KAJIAN_LORONG2.md`): Chandelier tutup. Paras keluar = tutup tertinggi sejak beli − 4 × ATR14 (purata mudah julat sebenar 14 hari, sama seperti `enjin.atr`); paras hanya naik, tidak pernah turun. Tutup < paras keluar → jual pada buka esok. Henti kaedah TIDAK dipakai dalam lorong ini (kekal dalam lorong 1). Selagi sejarah harga < 14 hari, paras keluar belum ada (tiada keluar). Tujuan: ukur berapa lama trend naik dan berapa hari dipegang. (17–18 Okt 2026: 2 tutup turun berturut atau kena henti kaedah.)
Lorong 2 diisi oleh `python3 BacktestShariah2/standard/keluar_lorong.py --stor <folder stor>` (`--semula henti` mengira semula lorong itu selepas peraturan dipinda; lajur lorong 10% lama dibuang secara automatik). Baris yang buka stor hari beli berbeza > 15% daripada harga_beli tidak dinilai. Lajur kosong = belum dinilai (amaran `sahkan.py`). `status_henti` = teks paparan: `Pegang (paras keluar X; puncak Y; n hari)`, `Tutup … bawah paras keluar … — jual pada buka esok (menunggu)`, `Keluar: tutup … bawah paras keluar … pada <tarikh> (<tarikh jual> @ harga)`. Baris yang keluar dengan peraturan lama (status tanpa `paras keluar`) dikira semula sekali secara automatik. Lejar Penuh memakai lajur sama (tanpa status) dan dibina semula apabila peraturan berubah (`keluar_lorong.VERSI`).

Kunci unik: (akaun, kaedah, saham, tarikh_beli) bagi baris yang dibeli. Akaun = moomoo atau claude (semua claude*.csv dikira satu akaun).

## `senarai_beli.csv` (ditulis 8:02 malam, dibaca 9:35 NY)
Lajur wajib: saham, kaedah, sektor, industri, pct_dipenuhi (= 100 sahaja), harga_rujukan, henti, nota_henti, buka_maks, sasaran, tarikh_isyarat, tarikh_imbasan. Lajur lain: nama, sumber, asal, belian_ke (1 = belian pertama kaedah+saham ini dalam Papertrade C; 2, 3 … = belian semula selepas keluar). `destinasi`/`slot_moomoo` lapuk (mod Papertrade C sahaja); jika ada, destinasi = Claude. Kunci unik: (saham, kaedah, tarikh_isyarat).

## `watchlist.csv` (ditulis 8:02 malam, disemak semula 6:02 pagi)
Tajuk lajur dikekalkan seperti sedia ada (dipakai oleh dashboard): Saham, Nama, Kaedah, Sektor, Industri, Harga, % hampir, Pencetus, Keadaan semasa, Syarat belum cukup, Syarat dipenuhi, Paras pencetus, Jarak %, Tarikh masuk watchlist, Hari dalam watchlist, Skor, Set, tarikh_data, dibina.
`% hampir` mesti 90–100; baris yang terkeluar signal (< 90 atau isyarat batal) dibuang serta-merta. Kunci unik: (Saham, Kaedah).

## Lajur gred (senarai_beli, watchlist, fail posisi) — sejak 14 Okt 2026
Diisi oleh `standard/gred.py tambah` semasa imbasan 8:02 malam; disalin ke baris posisi oleh belian 9:35 NY dan TIDAK dikemas kini selepas itu (gred pada hari isyarat). Baris lama: kosong.

| Lajur | Nilai |
|---|---|
| sektor_us, industri_us | sektor Morningstar dan industri Moomoo saham itu (seluruh pasaran AS) |
| gred_sektor, gred_industri | A–E atau "–". v2 sejak 19 Okt 2026 (`standard/gred_kumpulan.py`, fail `data/kumpulan/gred_kumpulan.csv` + `gred_kumpulan_sejarah.csv`; snapshot mesti sama tarikh dengan sesi isyarat baris itu (`tarikh_isyarat` / `tarikh_data`), jika tiada → "–"): Industri = pangkat (Weinstein + median 1 bulan), Sektor = pangkat % saham > SMA200, kedua-duanya seluruh pasaran AS; A > 80, B > 60, C > 40, D > 20, E ≤ 20. Sebelum 19 Okt: v1 skor panas (A ≥ 80 …). Baris lama yang dikira semula dengan v2 (snapshot sesi isyarat daripada `gred_kumpulan_sejarah.csv`) mesti menambah "S/I v2" dalam `gred_pada` — dashboard Prestasi ikut gred hanya mengira S/I bertanda v2 atau gred_pada ≥ 19 Okt |
| skor_sektor, skor_industri | 0–100 |
| rs_rating, gred_rs | 1–99 (lawan seluruh pasaran AS harga ≥ USD5, `data/rs/rs_pasaran.csv`; sandaran stor harga). Sejak 18 Okt 2026: A = RS 90–99 disahkan, B = 80–89 disahkan, C = 70–79 atau ≥ 80 tidak/belum disahkan, D < 70; "–" = tiada data. Baris sebelum 18 Okt: skala lama (A ≥ 90, B ≥ 80, C ≥ 60, D ≥ 40, E < 40) melainkan dikira semula (lihat gred_pada) |
| rs_sah | ya / tidak: saham naik 12 bulan, SPY > SMA200 dan Mansfield > 0 (RS line atas purata 52 minggu); kosong = tiada data |
| rs_tanda | sebab RS ≥ 80 tidak disahkan, atau "RS 95+: … berisiko"; kosong jika tiada |
| rs_industri | 1–99: kekuatan industri (TradingView) saham itu antara industri; direkod, bukan gred |
| rs_sumber | pasaran / stor / `anggaran sejarah pendek (N bar)` (sejak 23 Okt 2026: saham < 253 bar, `gred.rs_pendek` — suku tersedia dipangkat lawan skor pasaran; pengesahan tiada -> gred maks C) |
| gred_pemangkin, mata_pemangkin, pemangkin | Pemangkin v3 (sejak 18 Okt 2026; bukti dan kalibrasi: ulasan `standard/gred.py` dan data `data/pemangkin/sejarah/`): K1 earnings dijadualkan 6–21 hari dagangan lagi +2, 1–5 hari +1 (premium pengumuman; data 2012–2026: AR21 +0.2–0.4%, luar sampel t 3.4); K2 reaksi hari earnings ≥ +20% lawan SPY, umur ≤ 10 hari dagangan +4, 11–20 hari +3 (🔥 PANAS; AR21 +1.4–1.7%, bukti lemah); veto berita ≤ 20 hari dagangan: tawaran saham (pencairan) atau keputusan FDA akan datang → had C, sasaran ambil alih → had D. Gred A ≥ 3, B 2, C 1, D 0 (tiada pemangkin); E tidak dipakai. Tajuk berita, tindakan analisis, volum dan orang dalam tidak lagi diberi mata (diuji tiada nilai luar sampel / belum diuji). Ringkasan = sebab setiap mata/had, bermula "🔥 PANAS · " jika K2 aktif; "tiada pemangkin" = D; "–" = tiada data earnings dan berita. Baris 15–17 Okt 2026 guna skala Berita Panas (A ≥ 5); sebelum 15 Okt skala lama (A ≥ 4) — jangan campur skala bila menilai prestasi gred |
| pemangkin_url | JSON [{"tajuk", "url"}] maks 2 (pemangkin terkuat dahulu, kemudian terkini; URL https daripada quote_news_search / rating_summary); kosong jika tiada |
| tarikh_earnings, hari_ke_earnings, sumber_earnings, gred_qr | hari dagangan ke laporan suku: A > 21 (atau tiada dalam 30 hari), B 16–21, C 11–15, D 6–10, E ≤ 5; selepas QR lalu: 0–1 hari sekurang-kurangnya C, 2–3 hari sekurang-kurangnya B (gred lebih buruk dipakai; sumber_earnings ditanda `; QR lalu N hari`); asas: kajian 18 Okt 2026 (659k dagangan 134 kaedah, 2019–2026; `standard/gred.py gred_qr`); sumber SST / Nasdaq / anggaran / tiada data; sejak 23 Okt 2026 juga yfinance / `Moomoo earnings_price_history` / `anggaran (…)` (kalendar gabungan `standard/kalendar_earnings.py`, isi semula `standard/qr_isi.py`), dan `tidak diketahui (sebab)` apabila tiada sumber memberi tarikh (gred_qr kekal "–") |
| gred_keseluruhan | purata mata gred yang ada (paparan sahaja; belum diuji). Sejak 19 Okt 2026: Industri (kecuali kaedah pantulan dalam `kod/jenis_kaedah.csv`), Pemangkin, QR — Sektor dan RS tidak dikira (RS sejak 18 Okt) |
| gred_pada | tarikh imbasan gred dikira, diikuti catatan isi semula: "industri sandaran sektor (industri < 3 saham)" (gred industri = gred sektor), "QR/pemangkin isi semula 23 Okt (…; pemangkin tanpa berita, veto tidak disemak)", "kewangan isi semula 23 Okt (v7.1, penyata <= tarikh)" |
| gred_kewangan, kewangan_ringkas, kewangan_tempoh, kewangan_butiran | gred kewangan v7 (sejak 18 Okt 2026; `spec/GRED_KEWANGAN_v7.md`): A–E atau "–"; ringkasan "B (K:A U:B T:C S:B) · peringkat · F:n · keyakinan … · Syariah …"; label suku penyata; JSON butiran (semakan gagal, bendera, Syariah, nisbah) — butiran dalam senarai_beli/watchlist sahaja (tidak disalin ke fail posisi dan tidak dihantar ke db dashboard). Daripada `data/kewangan/<T>.json`; tiada fail → "–". Tidak masuk gred_keseluruhan; rekod sahaja |

## `pemangkin.json`
Ditulis oleh `standard/gred.py kumpul` (imbasan 8:02 malam) daripada hasil mentah alat Moomoo/SST: {ticker: {dikumpul, berita [{tajuk, tarikh (New York), selepas_tutup, hari_lalu, url, sumber}], analisis [{kategori, mata, firma, tarikh, hari_lalu, sasaran, url}], orang_dalam {bilangan, tarikh}, earnings_lalu_tarikh, earnings_lalu_hari, earnings_gerak_pct, earnings_anggaran, institusi}}. Berita yang bukan tentang saham itu sudah ditapis. Entri > 5 hari dagangan dibuang semasa gabung; `tambah` hanya memakai entri ≤ 2 hari dagangan.

## `peta_industri.csv`
ticker, industri, plate_code — keahlian plate industri Moomoo bagi semua saham AS. Dibina semula jika lebih 30 hari (quote_plate_list INDUSTRY + quote_plate_stock setiap plate).

## `data/kumpulan/gred_kumpulan.csv` (Actions `gred_kumpulan.yml`; jangan ubah secara manual)
Snapshot terkini gred Sektor/Industri v2: tarikh (sesi data), jenis (Sektor/Industri), nama, sektor, n (saham layak), skor (0–100), gred, w_rs_positif / w_rs_naik / w_trend (syarat Weinstein 0/1), m1m_med (% median 1 bulan), pct_atas_sma200, dibina. `gred_kumpulan_sejarah.csv` = semua snapshot (tarikh sama diganti).

## `kod/jenis_kaedah.csv`
kaedah, jenis (momentum / pantulan = median pulangan 20 hari sebelum isyarat > 0 / ≤ 0 dalam dagangan 2019–2026), pre20_median (%), n_dagangan. Dipakai oleh gred_keseluruhan.

## `sektor_pasaran.csv`
Snapshot harian kekuatan sektor/industri SELURUH pasaran AS (`standard/sektor_pasaran.py`): tarikh, jenis, nama, sektor, n, prestasi_1w, prestasi_1m, prestasi_3m (median %), breadth (% saham 1M > 0), rel_1m, rel_3m (lawan median pasaran), fasa, skor_panas, mcap_bilion, teratas, alam. Sejarah dikekalkan; snapshot tarikh sama diganti.

## `sektor.csv`
Snapshot harian bertambah (sejarah dikekalkan). Satu baris setiap (tarikh, jenis, nama).
