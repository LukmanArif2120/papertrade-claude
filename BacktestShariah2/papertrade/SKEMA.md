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
| henti, sasaran | nombor | paras enjin pada hari isyarat |
| isyarat_keluar | teks | "Pegang …", "Keluar: …", "Isyarat keluar … (menunggu)", atau "TIDAK DIBELI" |
| keluar | True/False | True ⇒ tarikh_keluar, harga_keluar, untung_akhir_pct wajib; False ⇒ ketiga-tiganya kosong |
| tarikh_keluar | YYYY-MM-DD | ≥ tarikh_beli |
| harga_keluar | nombor | isyarat keluar kaedah = buka hari berikutnya; henti/sasaran = paras atau buka jurang; had masa = tutup |
| untung_akhir_pct | nombor 2 tp | = (harga_keluar/harga_beli − 1) × 100 |
| sumber | teks | harian_c, penuh_v1, penuh_20261012, harian, log_v1, luar |
| kaedah_kongsi | teks | kaedah lain yang berkongsi unit yang sama |
| tarikh_isyarat | YYYY-MM-DD | sesi isyarat entry |
| nota, dikesan | teks | nota bebas; masa larian yang mengesan keluar |
| tidak_sah | True/kosong | tidak dikira dalam prestasi/pendedahan |
| sebab_tidak_sah | teks | wajib jika tidak_sah |
| tidak_dibeli | True/kosong | belian tidak berlaku (langkau kaedah kena pada buka rasmi). harga_beli kosong, isyarat_keluar = "TIDAK DIBELI", keluar = False, tidak dikemas kini lagi |
| luar_peraturan | True/kosong | Moomoo sahaja: dibeli sebenar tetapi luar peraturan (kekal dikemas kini harga, tidak dikira) |
| harga_buka_rujukan, tarikh_beli_dirancang | nombor, tarikh | untuk baris tidak_dibeli |
| keluar_henti, tarikh_keluar_henti, harga_keluar_henti, untung_henti_pct, status_henti | True/False, tarikh, nombor, nombor 2 tp, teks | Lorong 2 (pegang selagi naik). Lihat bahagian Tiga lorong keluar |
| capai_10, tarikh_capai_10, keluar_10, tarikh_keluar_10, harga_keluar_10, untung_10_pct, status_10 | True/False, tarikh, True/False, tarikh, nombor, nombor 2 tp, teks | Lorong 3 (sasaran 10%) |
| tutup_semua | True/False | = keluar AND keluar_henti AND keluar_10. Belian semula kaedah+saham sama hanya selepas True |

## Tiga lorong keluar (keputusan pengguna 17 Okt 2026)
Setiap posisi yang dibeli dinilai serentak dengan tiga peraturan keluar dari harga beli yang sama. Setiap lorong direkod dalam lajurnya sendiri dan dibekukan sebaik keluar:
1. **Kaedah** (`keluar`, `tarikh_keluar`, `harga_keluar`, `untung_akhir_pct`, `isyarat_keluar`): peraturan penuh kaedah (henti, sasaran, isyarat keluar, had masa), seperti sebelum ini.
2. **Pegang selagi naik** (`*_henti`; dipinda 17 Okt 2026): pegang selagi harga terus naik; 2 tutup berturut lebih rendah daripada tutup semalam → jual pada buka esok (satu hari turun sahaja tidak keluar; tutup >= tutup semalam mengosongkan kiraan). Henti kaedah kekal sebagai perlindungan (rendah <= henti → paras henti; buka <= henti dari hari kedua → harga buka). Tujuan: ukur berapa lama untung terus naik dan berapa hari dipegang.
3. **10%** (`*_10`): sebelum tutup >= harga beli × 1.10, henti kaedah (kaedah tanpa henti M01, M24, M31, M73, M82, M94: tutup < harga beli → jual pada buka esok). Selepas capai (`capai_10`, `tarikh_capai_10`): pegang selagi tutup >= low semalam; tutup pertama < low semalam → jual pada buka esok. Henti kaedah kekal aktif.
Lorong 2 dan 3 diisi oleh `python3 BacktestShariah2/standard/keluar_tiga.py --stor <folder stor>` (`--semula henti` / `--semula 10` mengira semula lorong itu selepas peraturan dipinda) (harga = stor harga; baris yang buka stor hari beli berbeza > 15% daripada harga_beli tidak dinilai). Lajur kosong = belum dinilai (amaran `sahkan.py`). `status_henti`/`status_10` = teks paparan (Pegang …, menunggu, Keluar: …). Lejar Penuh memakai lajur sama (tanpa status).

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
| gred_sektor, gred_industri | A–E atau "–" (skor panas seluruh pasaran AS, sandaran SST: A ≥ 80, B ≥ 60, C ≥ 40, D ≥ 20, E < 20; "–" = tiada data) |
| skor_sektor, skor_industri | 0–100 |
| rs_rating, gred_rs | 1–99; A ≥ 90, B ≥ 80, C ≥ 60, D ≥ 40, E < 40 |
| gred_pemangkin, mata_pemangkin, pemangkin | Berita Panas (sejak 15 Okt 2026): A ≥ 5 mata, B 3–4.9, C 1–2.9, D 0–0.9, E < 0 (mata boleh berpecahan .5); ringkasan sebab, bermula "🔥 PANAS · " jika pemangkin Tier 1/2 disahkan harga + volum; "–" = belum dikumpul. Baris sebelum 15 Okt guna skala lama (A ≥ 4) |
| pemangkin_url | JSON [{"tajuk", "url"}] maks 2 (pemangkin terkuat dahulu, kemudian terkini; URL https daripada quote_news_search / rating_summary); kosong jika tiada |
| tarikh_earnings, hari_ke_earnings, sumber_earnings, gred_qr | hari dagangan ke laporan suku: A > 21 (atau tiada dalam 30 hari), B 16–21, C 11–15, D 6–10, E ≤ 5; sumber SST / anggaran / tiada data |
| gred_keseluruhan | purata mata gred yang ada (paparan sahaja; belum diuji) |
| gred_pada | tarikh imbasan gred dikira |

## `pemangkin.json`
Ditulis oleh `standard/gred.py kumpul` (imbasan 8:02 malam) daripada hasil mentah alat Moomoo/SST: {ticker: {dikumpul, berita [{tajuk, tarikh (New York), selepas_tutup, hari_lalu, url, sumber}], analisis [{kategori, mata, firma, tarikh, hari_lalu, sasaran, url}], orang_dalam {bilangan, tarikh}, earnings_lalu_tarikh, earnings_lalu_hari, earnings_gerak_pct, earnings_anggaran, institusi}}. Berita yang bukan tentang saham itu sudah ditapis. Entri > 5 hari dagangan dibuang semasa gabung; `tambah` hanya memakai entri ≤ 2 hari dagangan.

## `peta_industri.csv`
ticker, industri, plate_code — keahlian plate industri Moomoo bagi semua saham AS. Dibina semula jika lebih 30 hari (quote_plate_list INDUSTRY + quote_plate_stock setiap plate).

## `sektor_pasaran.csv`
Snapshot harian kekuatan sektor/industri SELURUH pasaran AS (`standard/sektor_pasaran.py`): tarikh, jenis, nama, sektor, n, prestasi_1w, prestasi_1m, prestasi_3m (median %), breadth (% saham 1M > 0), rel_1m, rel_3m (lawan median pasaran), fasa, skor_panas, mcap_bilion, teratas, alam. Sejarah dikekalkan; snapshot tarikh sama diganti.

## `sektor.csv`
Snapshot harian bertambah (sejarah dikekalkan). Satu baris setiap (tarikh, jenis, nama).
