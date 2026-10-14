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

Kunci unik: (akaun, kaedah, saham, tarikh_beli) bagi baris yang dibeli. Akaun = moomoo atau claude (semua claude*.csv dikira satu akaun).

## `senarai_beli.csv` (ditulis 8:02 malam, dibaca 9:35 NY)
Lajur wajib: saham, kaedah, sektor, industri, pct_dipenuhi (= 100 sahaja), harga_rujukan, henti, nota_henti, buka_maks, sasaran, tarikh_isyarat, tarikh_imbasan. Lajur lain: nama, sumber, asal. `destinasi`/`slot_moomoo` lapuk (mod Papertrade C sahaja); jika ada, destinasi = Claude. Kunci unik: (saham, kaedah, tarikh_isyarat).

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
| gred_pemangkin, mata_pemangkin, pemangkin | A ≥ 4 mata, B 3, C 1–2, D 0, E < 0; ringkasan sebab; "–" = belum dikumpul |
| tarikh_earnings, hari_ke_earnings, sumber_earnings, gred_qr | hari dagangan ke laporan suku: A > 21 (atau tiada dalam 30 hari), B 16–21, C 11–15, D 6–10, E ≤ 5; sumber SST / anggaran / tiada data |
| gred_keseluruhan | purata mata gred yang ada (paparan sahaja; belum diuji) |
| gred_pada | tarikh imbasan gred dikira |

## `peta_industri.csv`
ticker, industri, plate_code — keahlian plate industri Moomoo bagi semua saham AS. Dibina semula jika lebih 30 hari (quote_plate_list INDUSTRY + quote_plate_stock setiap plate).

## `sektor_pasaran.csv`
Snapshot harian kekuatan sektor/industri SELURUH pasaran AS (`standard/sektor_pasaran.py`): tarikh, jenis, nama, sektor, n, prestasi_1w, prestasi_1m, prestasi_3m (median %), breadth (% saham 1M > 0), rel_1m, rel_3m (lawan median pasaran), fasa, skor_panas, mcap_bilion, teratas, alam. Sejarah dikekalkan; snapshot tarikh sama diganti.

## `sektor.csv`
Snapshot harian bertambah (sejarah dikekalkan). Satu baris setiap (tarikh, jenis, nama).
