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

## `sektor.csv`
Snapshot harian bertambah (sejarah dikekalkan). Satu baris setiap (tarikh, jenis, nama).
