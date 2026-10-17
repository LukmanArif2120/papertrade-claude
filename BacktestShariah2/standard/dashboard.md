# Dashboard: Papan Backtest Shariah (v2)

**Pautan:** https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (sama dengan https://claude.ai/artifact/3KAW4v9ZCkGbkAmwz2XiJ1). Versi akhir v2 = versi 25 (13 Okt 2026, 16:45 MYT: tab Sector buang skor panas selepas kalibrasi).
**Sumber HTML:** Project `standard/dashboard_v2.html` (format penerbitan Artifact: tanpa doctype/head; `<title>` + `<style>` di atas). Spesifikasi: `standard/tugasan_v2.md`. Log binaan: `standard/binaan_v2_log.md`.
**Capabilities:** `assets`, `db` (1 peraturan: baca = view, tulis = admin). Jangan ubah semasa menerbit semula (abaikan medan `capabilities`).

## Struktur tab
| Tab | Sub-tab / kandungan | Dokumen db |
|---|---|---|
| Backtest | Ringkasan · Papan Kedudukan · Banding (kandungan v1 kekal; pemilih set 431/S1–S4 hanya di sini) | `registry/<ID>` (119), `meta/info` |
| Sector | MAKLUMAT SAHAJA. Peta haba treemap (1H/1W/1M/3M, Sektor/Industri), ranking boleh-susun (lalai susun ikut 1M; fasa, RS, breadth, volum relatif, aliran institusi), kuadran fasa rotasi, aliran institusi & volum luar biasa, 10 industri 1M terkuat, nota kalibrasi | `sektor/snapshot` |
| Watchlist | Hampir Signal sahaja (90–100%): saham, kaedah, sektor, industri, harga, % hampir, syarat belum cukup, paras pencetus, tarikh & hari dalam watchlist | `papertrade/watchlist` |
| Paper Trade M | Posisi akaun simulasi Moomoo + keputusan (satu tab) | `papertrade/moomoo` (sandaran `moomoo_peta`) |
| Papertrade C | Posisi maya Claude + panel kiraan slot setiap kaedah + isyarat dibatalkan | `papertrade/claude` (`slot`, `batal`) |
| Prestasi | Papertrade M · Papertrade C · Combine: KPI, untung purata/kaedah, untung lawan risiko (scatter, kuadran Untung & Selamat), kadar menang/kaedah + donut, Paling Teruk, kedudukan Skor U×S, semua dagangan | dikira daripada `papertrade/moomoo` + `papertrade/claude`; risiko daripada `prestasi/mae` |
| Kaedah | Katalog semua kaedah aktif (satu baris setiap `kod/kaedah/Mxx.py`, varian dalam kod): ID, nama, asal (pencipta + sumber), masuk, keluar, pegang (had masa), henti rugi, Backtest set 431 (baris registry `varian == varian_kod`), Papertrade M+C (kiraan sama seperti Prestasi · Combine); carian + susun | `kaedah/katalog` (sumber `standard/katalog_kaedah.json`) + `registry/*` + `papertrade/*` |

Pautan terus: `#ringkasan #papan #banding #sektor #watchlist #ptm #ptc #prestasi #kaedah`.

## Kalibrasi tab Sector (13 Okt 2026)
Skor panas, fasa Leading dan kekuatan 1W/1M/3M/6M/12M sektor atau industri diuji lawan pulangan hadapan 1M dan 3M (kumpulan teratas tolak terbawah, IS 2019–22 lawan OOS 2023–26):
- 317 saham Shariah berlabel (dataset S1–S4, harian 2019–2026): tiada faktor signifikan; pangkat 12M industri (≥5 saham) hampir signifikan (t 1.7).
- 1,417 saham Moomoo (harga ≥ $5, mcap ≥ $300M, 1,500 terbesar; 145 industri Moomoo dipetakan ke 11 sektor; mingguan 2020–2026): semua faktor gagal; formula skor panas negatif; pangkat 12M tidak konsisten (IS negatif, OOS positif).
Keputusan: skor panas dan fasa TIDAK digunakan sebagai penapis atau keutamaan beli. `harian_sektor.py` masih mengira `skor_panas` dalam snapshot tetapi halaman tidak memaparnya.

## Peraturan paparan
- Lajur M, C dan jadual dagangan Prestasi sama dan sama susunan (`ptCols()`): Tarikh beli, Saham, Kaedah, Sektor, Industri, Harga beli, Unit, Harga terkini, Untung %, Hari dipegang, Isyarat keluar, Tarikh keluar, Harga keluar, Untung akhir %.
- Semua jadual boleh disusun (klik tajuk: turun/naik), kecuali Banding (metrik ikut baris).
- `keluar=true` → baris merah; `harga_terkini` = `harga_keluar` (dibekukan, tidak dikemas kini lagi). Moomoo tidak dijual; slot kekal dikira.
- Tiada tab Panduan istilah: setiap istilah ada tooltip (hover; tekan lama di telefon). Kamus `TIPS` dalam kod.
- Untung % = harga terkini ÷ harga beli − 1. Untung purata Prestasi = untung akhir bagi yang keluar, semasa bagi yang dipegang.
- Gaya SST Terminal, satu tema gelap. Storan pelayar hanya untuk tab/sub-tab/set/lipatan (dibalut try/catch).

## Bentuk baris papertrade (`papertrade/moomoo`, `papertrade/claude`)
`{rows:[...], harga_pada, akaun?, dibina, nota}`; setiap baris: `tarikh_beli, saham, kaedah, kaedah_kongsi[]?, sektor, industri, harga_beli, unit, harga_terkini, untung_pct, hari, henti, isyarat_keluar (teks), keluar (bool), tarikh_keluar, harga_keluar, untung_akhir_pct, id_kaedah, sumber (harian | log_v1 | luar | penuh_lama | isyarat)`. Claude juga: `tarikh_isyarat`, dan dokumen ada `slot{Mxx:{moomoo, moomoo_termasuk_warisan, claude_terbuka, claude_jumlah, nama}}`, `batal[]`.
`prestasi/mae`: `{rows:{"<M|C>|<saham>|<kaedah>|<tarikh_beli>": penurunan_%}, dibina, harga_hingga}`.

## Cara kemas kini harian (larian berjadual)
Halaman membaca db secara langsung — **tidak perlu terbit semula halaman** untuk data harian. Setiap tulisan: `ArtifactData get` dahulu untuk `version`, kemudian `set` dengan `if_version` (atau `batch`).
1. **8:02 malam MYT (Isn–Jum) — imbas & watchlist:** semak kalendar NYSE; jalankan pengimbas; tulis `papertrade/watchlist` + `papertrade/senarai_beli` (+ CSV Project). Kemudian jalankan `standard/bina_p3_sektor.py` (SST screen_stocks + sector/industry_rotation, market_heatmap, institutional_flow, unusual_volume, market_breadth) → `sektor/snapshot` + `papertrade/sektor.csv`.
2. **9:35 pagi New York (Isn–Jum) — beli:** Moomoo simulasi dahulu (maks 10 setiap kaedah, 1 unit); jika kaedah 10/10 → tambah baris maya ke `papertrade/claude` pada harga buka sebenar. **Dedup** dengan kunci kaedah+saham+tarikh_isyarat. Batalkan jika buka ≤ henti. Tiada wang sebenar.
3. **6:02 pagi MYT (Sel–Sab) — kemas kini M, C, Prestasi:** harga tutup terkini; nilai isyarat keluar ikut kaedah (henti, sasaran, isyarat jual, had masa) untuk semua posisi terbuka termasuk warisan v1; baris yang keluar: isi `tarikh_keluar`, `harga_keluar`, `untung_akhir_pct`, `keluar=true`, `harga_terkini=harga_keluar` dan jangan sentuh lagi. Kemas kini `hari`, `untung_pct`, `slot`. Kemudian jalankan `standard/bina_p4_mae.py` → `prestasi/mae`. Simpan `papertrade/moomoo.csv`, `papertrade/claude.csv`.
4. Kaedah baharu dalam `kod/kaedah/`: tambah baris dalam `standard/katalog_kaedah.json` (ujian `test_katalog_kaedah.py` gagal jika tertinggal), kemudian `set kaedah/katalog` dengan fail itu (if_version).
5. Backtest baharu: `python3 standard/dashboard_kemaskini.py registry_<ID>.csv` → `set registry/<ID>`.
6. Had saiz dokumen db 256 KiB (262,144 bait, JSON padat). Sejak 16 Okt 2026 halaman membaca `papertrade/claude`, `claude_2`, `claude_3`, … tanpa had: setiap dokumen yang wujud membuka langganan dua nombor seterusnya (`subPtc` dalam `connect()`; `S.ptcN`, `ptcRows()`). Fail `claude*.csv` dipecah dengan `standard/pecah_claude.py --pecah` apabila unjuran saiz (semua posisi terbuka dianggap sudah keluar) > 240 KB; tolak fail yang berubah ke dokumen sama nama. `papertrade/watchlist` dan `papertrade/senarai_beli` pula dibahagi oleh `standard/bahagi_db.py` (asas `bahagian:{id,n}` + `<nama>_2` … `{induk,bahagian,rows}`); halaman (`subBhg`) menggabung bahagian yang induknya sepadan dan mengabaikan bahagian lama.

## Jika halaman perlu diubah
`project_read standard/dashboard_v2.html` → simpan tempatan → edit → `Artifact read` URL di atas (wajib sebelum terbit) → `Artifact publish` dengan `url` yang sama → simpan semula `standard/dashboard_v2.html`. Uji dengan db tiruan (Playwright) pada 1400px dan 390px.

Nota: jumlah untung Backtest dikira daripada CAGR × tempoh 1 Nov 2019 – 2 Okt 2026 (6.92 tahun).
