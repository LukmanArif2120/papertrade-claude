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
- 87 kaedah M; varian dipilih dalam registry set 431: skor tertinggi bukan DITOLAK, jika tiada, CAGR tertinggi. Indikator I01–I32 tidak digunakan.
- Kod isyarat: `BacktestShariah2/kod/` (sumber kebenaran; lihat `kod/README.md`). Enjin v1.2 beku.
- Skop imbasan: saham AS Shariah (screener Moomoo) harga ≥ USD10; senarai 431 diutamakan.
- **Senarai beli** = isyarat entry 100% dipenuhi pada tutup sesi DAN lulus kesahihan:
  - (a) Isyarat MINGGUAN (M52 dan modul yang guna `akhir`) sah hanya jika sesi itu hari dagangan terakhir minggu.
  - (b) Setiap baris wajib ada `henti`, `nota_henti` (formula jika henti bergantung pada buka masuk, cth. M52 = 0.60×buka), `buka_maks` (cth. M08 = 1.05×SMA20, M06 = 1.05×pangsi, M20/M19 = sasaran) dan `sasaran`, diambil daripada `sedia()` modul kaedah.
- **Watchlist (Hampir Signal)** = 90–99% dipenuhi (semua syarat kecuali pencetus; pencetus dalam ≤ 2%; pencetus kalendar ≤ 3 hari dagangan). Maks 5 setiap kaedah (431 dahulu, kemudian skor).
  - Dinilai semula pada 6:02 pagi DAN imbasan malam (7:47). Terkeluar signal (< 90% atau isyarat batal/tidak sah) → BUANG serta-merta.
  - Calon baharu hanya ditambah pada imbasan malam. Calon yang menjadi 100% dipindah ke senarai beli pada imbasan malam.
  - Peraturan lama "buang selepas 10 hari" dimansuhkan.

## 4. Belian maya (9:35 NY)
- Calon = semua baris senarai_beli (tiada had slot). 1 unit setiap saham; kaedah kedua untuk saham sama = baris dengan `kaedah_kongsi`.
- Langkau jika: buka ≤ henti; buka > buka_maks; buka ≥ sasaran (jika kaedah melangkau); isyarat batal; buka = 0 atau saham belum didagangkan (high/low = 0); kunci kaedah+saham+tarikh_isyarat sudah wujud dalam claude*.csv.
- Harga beli = harga buka sebenar. Buka sementara disahkan dengan kline harian; larian 6:02 membetulkan baki.

## 5. Kualiti data (wajib)
1. `quote_stock_quote` dengan low/high = 0 bermaksud tiada dagangan; JANGAN tafsir sebagai kena henti. Guna kline harian.
2. Harga beli = `open` kline harian rasmi hari beli.
3. Keluar dinilai dengan enjin rasmi (`kod/`) dan `standard/harian_nilai_keluar.py` fungsi `keluar()`:
   - henti dinilai dari hari masuk (buka jurang bawah henti dari hari kedua → harga buka);
   - sasaran hanya dari hari selepas hari masuk, dengan tgt hari sebelumnya;
   - isyarat keluar kaedah → jual pada BUKA hari berikutnya; had masa → tutup.
   - Ujian: `python3 -m unittest discover -s BacktestShariah2/ujian`.
4. Kesahihan belian: belian semalam disemak semula dengan `sedia()` atas bar hari beli. `sig` = False → baris TIDAK DIBELI (lihat `papertrade/SKEMA.md`). Baris `tidak_dibeli`/`tidak_sah` tidak dikira dalam prestasi atau pendedahan sektor.
5. Sebelum push data: `python3 BacktestShariah2/standard/sahkan.py --betulkan` MESTI keluar 0. Jika 1: betulkan; jika tidak boleh, JANGAN push fail data yang rosak — catat ralat dalam log dan push log sahaja.
6. Setiap saham wajib ada sektor & industri (SST `get_stock`, sandaran Moomoo `quote_owner_plate`; tiada → "Tiada data" + catat).

## 6. Stor
- Repo GitHub `pedagangsenja/papertrade-claude`, cawangan `main`. Mula: `git pull --rebase origin main`. Akhir: `git add -A`, commit, `git push origin main` (ditolak → pull --rebase, cuba semula maks 3 kali; tiada --force).
- Skema CSV: `papertrade/SKEMA.md`.
- Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (db melalui ArtifactData; muatkan skill artifact-capabilities). JANGAN cipta artifact baharu. Dokumen: `papertrade/moomoo`, `papertrade/claude`, `papertrade/claude_2` … `claude_N` (tanpa had sejak 16 Okt 2026; halaman melanggan nombor seterusnya secara automatik), `papertrade/watchlist`, `papertrade/senarai_beli` (kedua-duanya dibahagi oleh `standard/bahagi_db.py` kepada `<nama>`, `<nama>_2` …; halaman menggabung bahagian yang `induk`-nya sepadan), `sektor/snapshot`, `prestasi/mae`, `prestasi/ringkasan`, `harian/status`. JSON padat; setiap dokumen < 250 KB (had keras 262,144 bait). Dokumen claude_N membesar ±130 bait setiap posisi keluar: `standard/pecah_claude.py --pecah` memecah fail `claude*.csv` yang unjurannya > 240 KB (CI menyemak setiap push).
- Log: imbasan → `standard/binaan_v2_log.md`; kemas kini dan belian → `standard/binaan_v2_log_tambahan.md` (baca dahulu, tambah di hujung).
- Harga yfinance (sejak 14 Okt 2026): GitHub Actions `.github/workflows/harga_harian.yml` (21:37 UTC Isn–Jum, sandaran 00:23 UTC; jadual GitHub boleh lewat 2–4 jam, jadi rutin 6:02 menembak workflow ini sendiri jika data belum siap, `jadual/kemas_kini_0602.md` langkah 0a) menulis `data/harga/terkini.csv` (10 sesi terakhir; universe = set 431 + semua saham papertrade + `data/harga/univ.txt` + SPY/QQQ), `status.json`, dan `sejarah.csv` (3 tahun, bagi ticker dalam `perlu_sejarah.txt`). Skrip: `standard/harga_yf.py`. Sumber tidak rasmi: wajib semak silang dengan kline Moomoo sebelum guna (`harga_yf.py semak`); beza > 0.5% → Moomoo menang. Harga beli/keluar rasmi kekal = kline Moomoo (§5.2).
- Alat besar: keputusan disimpan ke fail oleh sistem — proses dengan Python; jangan salin data harga secara manual. Had kline Moomoo ~4 panggilan seminit; maks 24 ticker setiap larian.

## 7. Prestasi
Papertrade M, Papertrade C (gabungan semua claude*.csv) dan Combine; baris sah sahaja. KPI, untung purata setiap kaedah, kadar menang, penurunan maksimum, Paling Teruk, skor Untung×Selamat. Skrip `standard/harian_prestasi.py <folder>` (DIBINA dan HARGA_PADA melalui env) dan `bina_p4_mae.py`; peraturan sama dengan halaman dashboard.
- Label (keputusan pengguna 14 Okt 2026): kaedah dengan **< 20 dagangan tertutup** = `BELUM CUKUP DATA`. Selepas ≥ 20: HENTIKAN jika untung purata ≤ −3% atau kadar gagal ≥ 75% atau skor < 25; TERUSKAN jika skor ≥ 55 dan untung purata > 0; selainnya PERHATI (gagal = % dagangan untung < 0; skor dibundar ke integer sebelum dibanding).
- Metrik portfolio dalam dolar: setiap posisi dianggap **USD1,000 (sama berat)**, bukan 1 unit. Rekod CSV kekal 1 unit.
- Ujian luar sampel backtest: tidak dibuat (keputusan pengguna 14 Okt 2026).

## 8. Gred calon (sejak 14 Okt 2026; keputusan pengguna: rekod dan uji dahulu, bukan penapis)
Lima gred A–E dikira pada hari isyarat oleh `standard/gred.py` dan direkod bersama setiap belian maya:
1. **Sektor** dan 2. **Industri** — kekuatan dalam SELURUH pasaran AS (kira-kira 6,100 saham harga ≥ USD5, bukan Shariah sahaja): `standard/sektor_pasaran.py` → `papertrade/sektor_pasaran.csv` (median 1W/1M/3M, breadth, fasa, skor panas 0–100). Industri saham = plate industri Moomoo (`papertrade/peta_industri.csv`, ~145 industri, dibina semula setiap 30 hari); sektor = 11 sektor Morningstar. Sandaran jika tiada: snapshot SST (`sektor.csv`). Ujian 13 Okt 2026 (snapshot SST): TIDAK meramal pulangan 1–3 bulan; direkod untuk diuji semula.
3. **RS rating** (1–99, gaya IBD, dikira sendiri daripada stor harga). Ujian 2019–2026 (431 saham, pulangan 21 hari): RS ≥ 90 purata +4.2% lawan +1.6–2.2% bagi gred lain, dan mendahului setiap tahun 2020–2026.
4. **Pemangkin (Berita Panas, sejak 15 Okt 2026)** — berita 10 hari yang benar-benar tentang saham itu (Moomoo `quote_news_search`, SST `search_news`), tindakan analisis berstruktur (Moomoo `quote_research_rating_summary`), belian orang dalam (Moomoo `quote_insider_trade_list`), reaksi earnings terakhir, aliran institusi (SST). Sejak 16 Okt 2026 sumber kedua percuma: GitHub Actions `.github/workflows/pemangkin.yml` (dicetus push senarai_beli/watchlist; `standard/pemangkin_actions.py`) menulis `data/pemangkin/yahoo.json` (berita, analisis, orang dalam; yfinance) dan `earnings_nasdaq.json` (kalendar Nasdaq) — dipakai bagi saham yang belum dikumpul melalui Moomoo hari itu (Moomoo diutamakan). Dikelaskan ikut kuasa (Tier 1 +3 … negatif −3) dengan susutan masa, dan disahkan pasaran (hari reaksi naik, volum ≥ 2×, harga kekal di atas tutup sebelum berita → 🔥 PANAS). Butiran: `jadual/imbas_2002.md` §5b, kod `standard/gred.py`. Belum diuji.
5. **QR** — hari dagangan ke laporan suku seterusnya (SST `market_events` 30 hari; kemudian kalendar Nasdaq `data/pemangkin/earnings_nasdaq.json` ≤ 4 hari; jika tiada, anggaran = earnings lalu + 91 hari). Makin jauh, makin kecil risiko jurang harga semasa pegang ~20 hari.

Dashboard Prestasi memaparkan prestasi setiap gred; sesuatu gred hanya dinilai selepas ≥ 20 dagangan tertutup. Gred tidak menapis belian sehingga pengguna memutuskan berdasarkan data papertrade.

