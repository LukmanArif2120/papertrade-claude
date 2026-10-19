# Lejar Penuh (fasa 1 sejak 16 Okt 2026)

Keputusan pengguna 16 Okt 2026: semua kaedah diuji ke hadapan dengan data yang adil. SEMUA isyarat 100% setiap kaedah dibeli
dan dikeluarkan dengan peraturan yang sama: tiada had 10 sekaedah, tiada keutamaan saham 431. Papertrade C (`papertrade/claude*.csv`)
dan tiga rutin Claude berjalan seperti biasa (selari); keputusan peralihan dibuat oleh pengguna selepas 2 minggu.

- Kod: `standard/lejar.py` (sesi demi sesi; logik dagangan = gelung `enjin.trades` v1.2; ujian `ujian/test_lejar.py` membuktikan dagangan lejar sama tepat dengan enjin).
- Jadual: GitHub Actions `.github/workflows/lejar.yml`, 06:17 UTC Sel–Sab (sandaran 10:17; sesi ditangguh jika data yfinance belum muktamad), tanpa LLM dan tanpa Moomoo. Setiap larian memproses semua sesi yang belum diproses mengikut urutan, jadi larian terlepas ditampung.
- Harga: stor repo `data/harga/stor/` (format `kod/stor.py`, 520 bar) = aset dashboard hingga 12 Okt 2026 + bar harian yfinance (`data/harga/terkini.csv`, Harga harian). Rutin 6:02 menyemak sampel dengan kline Moomoo. Jika sejarah dilaras (split), posisi terbuka dilaras dengan nisbah sama (lajur `laras`).

## Peraturan setiap sesi S
1. Keluar (bar demi bar selepas `dinilai_hingga`): buka <= henti (dari hari kedua) → buka; rendah <= henti → henti; sasaran (tgt bar sebelum, dari hari kedua): buka >= sasaran → buka, tinggi >= sasaran → sasaran; isyarat keluar → jual pada buka bar seterusnya (`keluar_esok`); had masa (bar sejak isyarat >= TMAX) → tutup.
2. Masuk: isyarat bar i dibeli pada buka bar i+1 hanya jika isyarat kaedah masih sah apabila buka itu diketahui (peraturan buka modul: buka_maks, henti ikut buka, isyarat mingguan), ada dagangan (buka dan volum > 0) dan buka > henti (tugasan_v3 §4). Henti dibekukan. Isyarat yang tidak dibeli → `langkau/` dengan sebab.
3. Isyarat baharu: saham dalam `data/harga/univ.txt` (skrin Shariah Moomoo), tutup >= USD10, bar >= PERLU_BAR (atau SILANG), indeks bar >= WARM. Isyarat semasa lorong 1 kaedah sama memegang saham itu (termasuk hari lorong 1 keluar) diabaikan, seperti enjin; saham yang sudah keluar boleh dibeli semula (`belian_ke`).

4. Dua lorong keluar (sejak 17 Okt 2026; `standard/keluar_lorong.py`): selain peraturan 1 (lorong 1, lajur `tarikh_keluar` …), setiap posisi dinilai dengan lorong 2 (pegang selagi naik, sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14 → buka esok; paras hanya naik; tanpa henti kaedah; lajur `*_henti`). Apabila peraturan lorong 2 berubah (`keluar_lorong.VERSI` lain daripada `lorong2` dalam `status.json`), `jalan` mengosongkan lejar dan memproses semula semua sesi dari `mula` (rekod dalam `status.json` `bina_semula`). Posisi kekal dalam `terbuka.csv` sehingga kedua-dua lorong keluar (`tutup_semua`), kemudian dipindah ke `tutup/<bulan lorong 1>.csv`. Sejak 19 Okt 2026 hanya lorong 1 menyekat isyarat baharu kaedah+saham sama, jadi dagangan lorong 1 lejar = enjin dan posisi lorong 2 boleh bertindih (17–18 Okt: disekat sehingga `tutup_semua`). Statistik lorong 1 dalam `RINGKASAN.md` dikira daripada semua posisi yang lorong 1 sudah keluar.

## Fail (jangan ubah secara manual)
- `terbuka.csv` — posisi terbuka. `tutup/<YYYY-MM>.csv` — posisi tutup mengikut bulan keluar (dibekukan, tambah sahaja).
- `langkau/<YYYY-MM>.csv` — isyarat tidak dibeli dan sebab. `tunggu.csv` — isyarat menunggu buka sesi seterusnya.
- `isyarat/<YYYYMMDD>.csv.gz` — SEMUA isyarat sesi itu (rank, henti, sasaran, `dipegang`, `pemanasan`).
- `status.json` — sesi terakhir diproses dan ringkasan setiap larian. `RINGKASAN.md`, `ringkasan.json` — prestasi setiap kaedah lawan jangkaan registry.

`untung_pct` = harga keluar / harga beli − 1 (seperti Papertrade C); `pulangan` = pulangan bersih kos enjin (0.1% setiap belah); `hari` = bar dari isyarat hingga keluar (enjin `days`).
Arahan: `python3 BacktestShariah2/standard/lejar.py stor | jalan | semak | ringkas`.

## Portfolio maya 10 slot (sejak 19 Okt 2026)
Selepas `ringkas`/`banding`, `lejar.yml` menjalankan `standard/portfolio_slot.py`, yang membina semula dua portfolio maya 10 slot
daripada posisi lejar (`BacktestShariah2/portfolio_slot/`): RS_10 (slot kosong diisi dengan RS pasaran tertinggi pada tarikh
isyarat) dan RAWAK_10 (kawalan). Keluar = lorong 2. Rekod sahaja; kajian `kajian/KAJIAN_PORTFOLIO.md`.
