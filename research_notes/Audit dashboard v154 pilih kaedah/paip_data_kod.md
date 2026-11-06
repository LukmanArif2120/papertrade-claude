# Paip data dan kesihatan kod dashboard v154 (Papan Backtest Shariah)

Audit dalaman repo `/home/user/papertrade-claude` pada 2026-11-06 (salinan kerja = komit `1d476fe`, klon **cetek** 56 komit). Tiada fail repo diubah; `jana_db.py` dijalankan ke scratchpad sahaja (`python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db0`, 30.8 s, exit 0, stderr kosong). Semua laluan relatif kepada akar repo. Zon masa: cron GitHub = UTC; November 2026 = EST (NY = UTC−5), MYT = UTC+8.

## KQ1 — Dokumen db: dibaca oleh HTML lawan ditulis oleh `jana_db.py` lawan ditolak oleh `tolak_db.md`

### Takeaway
HTML melanggan **26 laluan dokumen + 2 koleksi**; `jana_db.py` menghasilkan **238 dokumen / 36.67 MB** setiap hari dalam **46 batch**; **62% bait yang ditolak (22.6 MB) tidak pernah dibaca pada laluan biasa** (`papertrade/claude*` 154 dokumen dan `papertrade/moomoo*` ialah sandaran yang hanya dibaca jika `ringkas_c`/`ringkas_m` tiada; `prestasi/ringkasan` tidak dibaca langsung). Tujuh laluan yang dibaca **tiada penulis harian** (`registry/*`, `meta/info`, `kaedah/katalog`, `autotune/*`, `papertrade/moomoo_peta`, `kumpulan/siri`, `sektor/snapshot`) dan `kumpulan/siri` tiada penulis langsung dalam repo.

### Cited Findings

**(a) Semua bacaan db dalam HTML** — satu blok `connect()` [dashboard_v2.html:5141–5350](BacktestShariah2/standard/dashboard_v2.html). Pembantu: `langgan()` = kolam langganan (`KOLAM.maks=44`, baris 5161), `sub()` (5204), `subRingkas()` (5215; bentuk padat ikut lajur + kamus), `subBhg()` (5273; dokumen dibahagi `bahagi_db`). Parameter ketiga `tabs` ialah tab yang dilukis semula apabila dokumen tiba.

| Laluan dibaca | Pembantu | Tab (`tabs`) | Baris |
|---|---|---|---|
| koleksi `registry` (limit 1000) | `db.collection` | backtest (+ Ringkasan/Kaedah ikut `dashboard.md` §Struktur) | 5195 |
| `meta/info` | `langgan` | backtest | 5202 |
| `papertrade/ringkas_m` (+`_kamus_1`) | `subRingkas` | semua (`re()`) | 5321 |
| `papertrade/moomoo` (+`_2`) — **sandaran** | `subBhg` | ptm, prestasi | 5321 |
| `papertrade/moomoo_peta` — **sandaran** | `sub` | ptm, prestasi | 5321 |
| `papertrade/ringkas_c` (+`_2..18`, `_kamus_1..9`) | `subRingkas` | semua | 5322 |
| `papertrade/claude`, `claude_N` tanpa had — **sandaran** | `sub`/`langgan` | ptc, prestasi | 5323–5328 |
| `papertrade/watchlist` (+`_2..4`) | `subBhg` | watch, sektor | 5329 |
| `sektor/snapshot` | `sub` | sektor | 5330 |
| `harian/status` | `langgan` | pengepala (`renderData`) | 5331 |
| `prestasi/mae` (+2,3) · `prestasi/mae_atr` (+2,3) | `subBhg` | prestasi | 5332 |
| `prestasi/garis` | `subBhg` | utama, ptc, prestasi, watch | 5333 |
| `prestasi/mfe` (+2,3) | `subBhg` | prestasi | 5333 |
| `prestasi/harian_kaedah` | `subBhg` | utama, prestasi, analisis | 5333 |
| `posisi/lorong2` (+`_2..24`) · `posisi/jalur` (+`_2..4`) | `subBhg` | ptc | 5333 |
| `harian/trend` · `harian/stage` | `subBhg` | ptc, watch | 5333 |
| `kumpulan/siri` | `subBhg` | sektor | 5333 |
| `prestasi/portfolio_slot` | `sub` | utama, prestasi | 5334 |
| `analisis/papan` (+2) | `subBhg` | analisis | 5339 |
| `analisis/lift` (baharu v154) | `sub` | analisis | 5340 |
| `kaedah/katalog` | `sub` | kaedah | 5341 |
| `kaedah_n/papan` (+2) | `subBhg` | kaedahn | 5347 |
| koleksi `autotune` (limit 1000) | `db.collection` | autotune, backtest | 5349 |

Sandaran disahkan daripada kod: `subRingkas` memanggil `lama()` **hanya** jika dokumen asas `!s.exists` atau ralat [dashboard_v2.html:5252–5263](BacktestShariah2/standard/dashboard_v2.html); `ptmRows()` memilih `S.ptm` dahulu dan `S.ptmPeta` hanya jika kosong [dashboard_v2.html:1881–1882](BacktestShariah2/standard/dashboard_v2.html). `S.ksiri` dirujuk sekali [dashboard_v2.html:3171](BacktestShariah2/standard/dashboard_v2.html).

**(b) Semua dokumen yang `jana_db.py` tulis** (larian 2026-11-06 15:15 MYT; `ringkas.json`: `dokumen: 238`, `batch: 46`, `hampir_had: []`, `kumpulan_terpecah: ['posisi/lorong2 (24 bahagian, 4592233 bait)', 'papertrade/ringkas_c (27 bahagian, 5291555 bait)']`):

| Dokumen asas | Bahagian | Jumlah bait | Bhg terbesar | % had 262,144 | Sumber dalam jana_db.py |
|---|---|---|---|---|---|
| `papertrade/moomoo` (+`_2`) | 2 | 251,782 | 199,258 | 76.0 | 1248; PECAH 1178; gugur medan dahulu 1249–1259 |
| `papertrade/claude` | 1 | 173,134 | 173,134 | 66.0 | 1266; bukan PECAH (pecah_claude.py) |
| `papertrade/claude_2 … claude_154` | 153 | 22,200,764 | 210,304 (`claude_2`) | 80.2 | 1263–1267 (`glob claude*.csv`) |
| `papertrade/watchlist` | 4 | 683,101 | 199,934 | 76.3 | 1297 |
| `papertrade/ringkas_c` (+17 bhg +9 kamus) | 27 | 5,291,555 | 199,987 | 76.3 | `ringkas_pt` 217, 1320–1326 |
| `papertrade/ringkas_m` (+1 kamus) | 2 | 90,688 | 77,688 | 29.6 | 1320–1326 |
| `prestasi/mae` | 3 | 488,388 | 199,994 | 76.3 | 1306 |
| `prestasi/mae_atr` | 3 | 486,944 | 199,995 | 76.3 | 1310 |
| `prestasi/ringkasan` | 1 | 90,930 | 90,930 | 34.7 | 1313 — **tidak dibaca HTML** |
| `prestasi/garis` | 1 | 152,853 | 152,853 | 58.3 | 1328 |
| `prestasi/mfe` | 3 | 473,626 | 199,992 | 76.3 | 1331 |
| `prestasi/harian_kaedah` | 1 | 181,292 | 181,292 | 69.2 | 1335 |
| `harian/trend` | 1 | 154,405 | 154,405 | 58.9 | 1348 (`trend_status.py` + `bawa_semalam`) |
| `posisi/lorong2` | 24 | 4,592,233 | 199,995 | 76.3 | 1349 (`lorong2_siri.py`) |
| `harian/stage` | 1 | 87,377 | 87,377 | 33.3 | 1350 (`stage.py`) |
| `posisi/jalur` | 4 | 672,132 | 199,890 | 76.3 | 1353 (`jalur_jangka.py`) |
| `prestasi/portfolio_slot` | 1 | 37,273 | 37,273 | 14.2 | 1359–1361 |
| `analisis/papan` | 2 | 279,171 | 199,741 | 76.2 | 1363–1365 ← `data/analisis/papan.json` (`penganalisis.py`) |
| `analisis/lift` | 1 | 49,041 | 49,041 | 18.7 | 1372–1374 ← `data/analisis/lift.json` (`lift_kaedah.py:59,346–352`) |
| `sektor/snapshot` | 0 | — | — | — | 1376–1378 **hanya jika** `data/db/sektor_snapshot.json` wujud — fail/folder TIADA dalam repo (`ls BacktestShariah2/data/db` gagal) |
| `harian/status` | 1 | 650 | 650 | 0.2 | 1381 |
| `kaedah_n/papan` | 2 | 234,782 | 199,790 | 76.2 | 1390–1392 (`kaedah_n()` daripada CSV REVERSE) |
| **Jumlah** | **238** | **36,672,121** | | | |

Senarai `PECAH` (dokumen yang dipecah dengan `bahagi_db.bahagi(…, 200000)`): `papertrade/senarai_beli`, `papertrade/watchlist`, `prestasi/garis`, `prestasi/mfe`, `prestasi/mae_atr`, `prestasi/harian_kaedah`, `harian/trend`, `harian/stage`, `posisi/lorong2`, `posisi/jalur`, `prestasi/mae`, `analisis/papan`, `kaedah_n/papan`, `papertrade/moomoo` [jana_db.py:1151–1179](BacktestShariah2/standard/jana_db.py). `papertrade/senarai_beli` **tidak pernah dijana** — komen di 1291 "tidak ditolak ke db sejak 19 Okt 2026 (halaman tidak membacanya)" — jadi entri PECAH itu mati.

Penulis lain (bukan harian): `dashboard_kemaskini.py` → `registry/<ID>` dan `papertrade/log` secara manual (`ArtifactData set`) [dashboard_kemaskini.py:1–6](BacktestShariah2/standard/dashboard_kemaskini.py); `kaedah/katalog` di-`set` manual daripada `standard/katalog_kaedah.json` [dashboard.md:62](BacktestShariah2/standard/dashboard.md); `snapshot_sektor_db.py` → `sektor/snapshot` melalui `jadual/mingguan.md` langkah 6 (Ahad 10:47 MYT) ke `BacktestShariah2/data/db/sektor_snapshot.json` "jana_db.py menolaknya bersama dokumen harian" [mingguan.md:26–29](BacktestShariah2/jadual/mingguan.md) — tetapi fail itu tidak ada dalam `main`, jadi laluan itu tidak berfungsi pada klon ini. `kumpulan/siri`: `grep -rln "kumpulan/siri"` ke seluruh repo (py/md/yml) memberi **sifar** selain HTML; `gred_kumpulan.py` ada `def siri` tetapi menulis CSV sahaja [gred_kumpulan.py:74,160–169](BacktestShariah2/standard/gred_kumpulan.py). `autotune/*`: tiada penulis ditemui (`grep ArtifactData .github/workflows` = 0; Actions tidak boleh menulis db).

**(c) Apa yang `tolak_db.md` tolak dan bila**: 10:20 pagi NY Isn–Sab (= 15:20 UTC Nov); langkah 3 mengambil versi bagi koleksi `papertrade, prestasi, harian, sektor, analisis, posisi` — **`kaedah_n` tiada dalam senarai**, jadi `kaedah_n/papan` ditolak tanpa `if_version`; langkah 5 = satu panggilan `ArtifactData batch` bagi **setiap** `batch_N.json` (46 panggilan hari ini) mengikut urutan [tolak_db.md:23–36](BacktestShariah2/jadual/tolak_db.md). Semakan kedua 12:20 NY (`tolak_db_semak.md`) menolak semula **hanya** jika Semakan A (kesegaran `harga_tutup_pada`/`tarikh_data`/`beli_pada`) atau B (penghimpunan `bahagian.id` lawan `induk`) gagal [tolak_db_semak.md:28–47](BacktestShariah2/jadual/tolak_db_semak.md). Teks `tolak_db.md:38` "ringkas_c ialah 22 dokumen / 3.3 MB" sudah hanyut: hari ini 27 dokumen / 5.29 MB.

**(d) Diff dua arah**
- Ditulis, **tidak dibaca**: `prestasi/ringkasan` (90,930 B; `grep "prestasi/ringkasan" dashboard_v2.html` = 0).
- Ditulis setiap hari, dibaca **hanya sebagai sandaran** (laluan biasa tidak pernah): `papertrade/claude` + `claude_2..154` = 154 dokumen / **22,373,898 B** (61% daripada bait harian); `papertrade/moomoo`+`_2` 251,782 B; bersama `ringkasan` = 22.72 MB / 36.67 MB = **62%** bait yang ditolak setiap hari tanpa pembaca aktif.
- Dibaca, **tiada penulis harian / tiada penulis langsung**: `registry/*`, `meta/info`, `kaedah/katalog`, `autotune/*`, `papertrade/moomoo_peta` (warisan P1, `binaan_v2_log.md:35,51`), `kumpulan/siri` (tiada penulis dalam repo), `sektor/snapshot` (penulis mingguan; fail sumber tiada dalam `main`).
- Berganda (data sama dua bentuk): `ringkas_c` ≡ `claude*` (5.29 MB lawan 22.37 MB); `ringkas_m` ≡ `moomoo` ≡ `moomoo_peta`; `harian/trend`/`harian/stage` dikira dua kali — `harian.yml` menulis `data/trend/status.json` + `data/stage/status.json` [harian.yml:92–97](.github/workflows/harian.yml) dan `jana_db.py` **mengira semula** daripada stor lalu `bawa_semalam` menggabung medan beku [jana_db.py:1343–1350](BacktestShariah2/standard/jana_db.py).
- Hanyutan dokumentasi berbanding bacaan sebenar: jadual tab `dashboard.md` menyatakan Analisis = `analisis/papan` sahaja (v154 menambah `analisis/lift`), Sektor = `sektor/snapshot` sahaja (HTML juga membaca `kumpulan/siri` dan `papertrade/watchlist`), Watchlist = `papertrade/watchlist` sahaja (HTML juga `harian/trend`, `harian/stage`, `prestasi/garis`) [dashboard.md:10–20](BacktestShariah2/standard/dashboard.md).

### Inferences
- Beban tolakan harian boleh dipotong ~62% dengan membuang `claude*`/`moomoo*`/`ringkasan` daripada tolakan harian (hantar hanya bila `ringkas_*` gagal), tanpa mengubah paparan — tetapi `tolak_db.md` dan `semak_data.yml` (`pecah_claude.py --gagal-pada 262144`, [semak_data.yml:65–72](.github/workflows/semak_data.yml)) masih menganggap `claude_N` dokumen db hidup.
- Tab Sektor berjalan atas dua dokumen yang tidak boleh disegarkan oleh paip semasa (`sektor/snapshot` fail sumber tiada; `kumpulan/siri` tiada penulis) — kandungannya beku pada tarikh tolakan terakhir yang tidak dapat ditentukan dari repo.
- `kaedah_n` yang tertinggal dari langkah 3 bermakna tolakan `kaedah_n/papan` tiada perlindungan versi; impak kecil kerana hanya satu penulis.

### Gaps
- Versi/tarikh dokumen hidup `sektor/snapshot`, `kumpulan/siri`, `meta/info`, `autotune/*`, `moomoo_peta` tidak boleh ditentukan tanpa `ArtifactData` (dilarang dalam audit ini).
- Siapa menulis `autotune/*` dan `kumpulan/siri` tidak ditemui dalam repo; mungkin sesi lama (rutin 6:02 yang dimatikan 27 Okt 2026) atau Project claude.ai yang dibekukan.

## KQ2 — Saiz dokumen dan had 262,144 bait; pembetulan `prestasi/mae`

### Takeaway
Tiada dokumen melebihi 85% had hari ini (`hampir_had: []`); **satu** dokumen dalam 20% teratas had: `papertrade/claude_2` 210,304 B (80.2%). `prestasi/mae` dibetulkan dengan **pemecahan** (`bahagi_db`) selepas `rows` ditukar daripada peta kepada senarai pasangan tersusun pada 2 Nov 2026, bukan pemangkasan; `papertrade/moomoo` pula memakai dua lapisan — gugur medan teks, kemudian pecah.

### Cited Findings
- Had: `HAD_DB = 262144` [bahagi_db.py:14](BacktestShariah2/standard/bahagi_db.py); pemecahan pada sasaran 200,000 B setiap bahagian [jana_db.py:1397](BacktestShariah2/standard/jana_db.py); `SystemExit` jika `sz >= HAD_DB` [jana_db.py:1410–1411](BacktestShariah2/standard/jana_db.py); amaran stderr pada ≥ 85% bagi dokumen bukan-PECAH [jana_db.py:1416–1420](BacktestShariah2/standard/jana_db.py). Had batch `HAD_BATCH = 900_000` [jana_db.py:28](BacktestShariah2/standard/jana_db.py).
- Ukuran hari ini (jadual KQ1b, kaedah: `os.path.getsize` atas `<scratchpad>/db0/<koleksi>/<doc>.json`): dokumen ≥ 80% had = `papertrade/claude_2` sahaja (210,304 B). Semua bahagian PECAH ditutup pada 199,2xx–199,995 B (76.0–76.3%) secara reka bentuk. Dokumen tunggal bukan-PECAH terbesar: `papertrade/claude` 173,134 B (66.0%) — dilindungi oleh `pecah_claude.py` yang memecah fail CSV pada **unjuran** 240,000 B (sasaran 190,000) [pecah_claude.py:1–9](BacktestShariah2/standard/pecah_claude.py) dan dijalankan oleh `harian.yml:147` dan `beli.yml:90`; anggaran meta `papertrade/claude` terkurang 17,945 B (8.6%) sebelum dibetulkan 4 Nov 2026 [pecah_claude.py:17–32](BacktestShariah2/standard/pecah_claude.py).
- `prestasi/mae`: "2 Nov 2026: rows ditukar daripada peta kepada senarai pasangan tersusun supaya dokumen boleh DIBAHAGI (ia melebihi had 262,144 bait)" [jana_db.py:1303–1306](BacktestShariah2/standard/jana_db.py); ditambah ke PECAH [jana_db.py:1155–1159](BacktestShariah2/standard/jana_db.py); hari ini 3 bahagian, 488,388 B jumlah. ATR dipindah ke `prestasi/mae_atr` pada 23 Okt 2026 "kerana mae + atr melebihi had" [jana_db.py:1309](BacktestShariah2/standard/jana_db.py). `dashboard.md:45` masih menulis bentuk lama `rows:{"kunci": %}` (peta) — hanyut.
- `papertrade/moomoo`: lapisan 1 gugur medan `gred_pada, pemangkin_url, kewangan_ringkas, rs_tanda, pemangkin, sumber_earnings, nota` sehingga < had−2000 [jana_db.py:1249–1259](BacktestShariah2/standard/jana_db.py); lapisan 2 PECAH sejak 3 Nov 2026 pada 93.1% had [jana_db.py:1163–1166](BacktestShariah2/standard/jana_db.py).
- `analisis/papan` 274,573 B pada 228 kaedah melanggar had pada 2 Nov 2026 → PECAH [jana_db.py:1160–1162](BacktestShariah2/standard/jana_db.py); `kaedah_n/papan` 234,697 B / 263 baris, +~892 B setiap baris registry → PECAH 4 Nov 2026 [jana_db.py:1169–1177](BacktestShariah2/standard/jana_db.py).
- Peraturan gandingan: "Setiap nama di sini MESTI dibaca dengan subBhg() dalam dashboard_v2.html" dan "pembaca dahulu, baru pemecah" [jana_db.py:1150,1164–1166](BacktestShariah2/standard/jana_db.py); pepijat padanan atas `doc_id` sahaja (`papan` dikongsi dua koleksi) dibetulkan 2 Nov 2026 [jana_db.py:1145–1149](BacktestShariah2/standard/jana_db.py).
- Pembatchan: kumpulan yang tidak muat 900 KB dipecah merentas batch dan dokumen asas diletak **terakhir** supaya halaman terbuka terus memapar set lama yang lengkap [jana_db.py:1203–1221](BacktestShariah2/standard/jana_db.py); diuji `test_jana_db_batch.py` (7 ujian: `test_kumpulan_terpecah_letak_asas_terakhir`, `test_setiap_batch_dalam_had`, …) [test_jana_db_batch.py:37–99](BacktestShariah2/ujian/test_jana_db_batch.py).
- Semakan saiz automatik harian: `harian.yml` langkah "Saiz db (amaran sahaja)" menjalankan `jana_db.py --keluar /tmp/db_semak` dan mencetak `::warning::`/`::error::` [harian.yml:158–172](.github/workflows/harian.yml); langkah "Notifikasi ntfy (saiz db)" bersyarat `steps.db.outputs.amaran != ''` [harian.yml:219–226](.github/workflows/harian.yml) — **tetapi langkah `db` tidak pernah menulis `amaran` ke `$GITHUB_OUTPUT`** (`grep -n "amaran=" harian.yml` = 0), jadi notifikasi itu tidak boleh berbunyi.

### Inferences
- Pertumbuhan yang mengancam had seterusnya ialah `papertrade/claude_2` (80.2%, dokumen pecah_claude yang unjurannya sepatutnya ≤ 240 KB — ia di bawah unjuran itu, jadi selamat ikut peraturan sendiri) dan `prestasi/harian_kaedah` (69.2%, dalam PECAH, jadi akan dipecah sendiri).
- Jaring amaran saiz db yang sebenar ialah stderr `jana_db.py` yang dibaca oleh sesi `tolak_db` (manusia/LLM), bukan ntfy — kerana pepijat `outputs.amaran`.

### Gaps
- Saiz dokumen **hidup** (di pelayan) mungkin berbeza daripada yang dijana di sini jika tolakan terakhir gagal separa; tidak disemak.

## KQ3 — Komposisi HTML 683,519 bait, kod mati, bloat

### Takeaway
JS = **580,643 B (84.9%)**, CSS 99,241 B (14.5%), badan HTML 3,362 B (0.5%). Kamus tooltip `TIPS` sahaja 58,294 B (8.5% fail) dan `renderKaedahN` 35,713 B (teks kajian REVERSE terbenam) ialah dua blok terbesar. Kod mati yang dikesan kecil: 6 fungsi tidak dipanggil, 27 kelas CSS tidak muncul di luar `<style>` (≈ 12 daripadanya mungkin dibina dinamik), 1 `console.*`, 61 rujukan versi `v1xx` dalam komen.

### Cited Findings
- Kaedah: Python atas teks fail — rantau mengikut tag (`<style>` baris 5–1047, badan 1048–1099, `<script>` 1100–5352) [dashboard_v2.html:5,1047,1100,5352](BacktestShariah2/standard/dashboard_v2.html); blok = daripada `^function nama(`/`^const TIPS` peringkat atas ke permulaan blok seterusnya (jumlah span 579,865 B ≈ JS).
- 25 blok terbesar (bait, baris): `const TIPS` 58,294 (4842–5016) · `renderKaedahN` 35,713 (4563–4780) · `pnavKe`+blok `connect` 17,904 (5134–5352) · `prSkor` 14,567 (3672–3733) · `renderSektor` 11,977 · `renderUtama` 9,420 · `renderKaedah` 9,182 · `renderAnalisis` 8,825 · `prHarian` 8,437 · `prRIsi` 8,317 · `skwRamal` 8,278 · `renderWatch` 7,198 · `skwKira` 7,078 · `renderAt01` 6,978 · `renderPos` 6,726 · `openPanduan` 6,500 · `renderAtV` 6,259 · `topScrolls` 6,174 · `openAnl` 6,004 · `openKaedah` 5,664 · `renderKeputusan` 5,322 · `renderRingkasan` 5,297 · `prAnalisis` 5,231 · `renderPrestasi` 5,118 · `renderData` 5,025.
- Fungsi `render*` (20) = 141,222 B (24% JS); `renderKaedahN` sahaja 25% daripadanya. Baris terpanjang: 4964 (3,066 B, entri `skor_swing` TIPS), 3729 (2,107 B, perenggan skor), 4844 (1,660 B, `stage_w`), 801 (1,509 B CSS `.hkw`), 4766 (1,328 B nota pradaftar) — teks penerangan, bukan data JSON.
- Fungsi/konst ditakrif sekali dan tidak dirujuk di tempat lain (regex sempadan kata atas JS): `grCols` (1829), `pc1` (1998), `tandaPos` (2908), `pangkasK` (3505), `kuantil` (3772), `pot` (3783) [dashboard_v2.html](BacktestShariah2/standard/dashboard_v2.html). (`connect` = IIFE, bukan mati.)
- Nama dikongsi: `lepasAnak` ditakrif dalam `subRingkas` (5219) **dan** `subBhg` (5274) — dua pelaksanaan logik himpun-bahagian yang hampir sama (kira `ada`, bina `hil`, `Diag`, `Tunggu`) [dashboard_v2.html:5230–5242 lawan 5275–5283](BacktestShariah2/standard/dashboard_v2.html). Nama lain yang berulang (`pct, lebih, X, q, seg, kotak, tag, sel, baris, P, wk, rk, lukis, henti`) ialah `const` tempatan dalam skop berbeza — bukan disahkan sebagai pendua.
- Kelas CSS: 466 pemilih kelas; 27 tidak muncul di luar `<style>`: `al-l al-t full g-A g-B g-C g-D g-E g-x grk grp hm0 hmall k-henti k-keluar k-masuk k-pegang kpil l2bar ph pn-n sal-basi sal-lewat sal-ok sal-x v-h v-j`. Awalan `sal-`, `g-`, `k-`, `al-`, `v-` ada binaan dinamik (`'sal-'+…`/`` `g-${…}` ``: 2, 3, 2, 2, 3 kejadian), jadi hanya `full grk grp hm0 hmall kpil l2bar ph pn-n` (9) boleh dianggap mati; `grk`/`grp` ialah sisa lajur Pemangkin/Kewangan yang dibuang v122 [dashboard.md:3 (v122, v75)](BacktestShariah2/standard/dashboard.md).
- `console.*` = 1 (`console.error` dalam `dbErr`, [dashboard_v2.html:5188](BacktestShariah2/standard/dashboard_v2.html)); `TODO/FIXME` = 0; `v1xx` dalam komen = 61 (`v105` 8, `v139` 7, `v151` 5, `v133` 5, …) — komen sejarah, bukan bendera ciri; tiada `if(versi…)` guard ditemui.
- Komen hanyut dalam HTML: "232,704 bait pada 489 baris ujian = 88.8% had" bagi `kaedah_n/papan` [dashboard_v2.html:5342–5346](BacktestShariah2/standard/dashboard_v2.html) sedangkan dokumen itu kini dipecah 2 bahagian; "halaman ini membuka 71 serentak: ringkas_c 22, posisi/lorong2 20" [dashboard_v2.html:5144–5146](BacktestShariah2/standard/dashboard_v2.html) sedangkan hari ini ringkas_c 27 dan lorong2 24.
- Klon cetek: `git rev-parse --is-shallow-repository` = true; `git log --follow -- dashboard_v2.html` hanya 2 komit — `2ed7a27` (2026-11-05, +5,263 baris, fail masuk bersama seluruh repo) dan `372db4a` (2026-11-06, v154, +98/−9). Sejarah v132–v153 tidak boleh dibina semula di sini.

### Inferences
- "Bloat" sebenar bukan kod mati tetapi **teks terbenam**: TIPS + panel naratif Kombinasi N + nota pradaftar ≈ 100 KB (≈ 15% fail) yang boleh dipindah ke dokumen db (`kaedah_n/papan` sudah membawa `nota`/`tarik`) tanpa mengubah paparan.
- Dua pelaksanaan himpun (`subRingkas`/`subBhg`) ialah risiko pemeliharaan: pembetulan 3–4 Nov 2026 perlu dibuat dua kali (komen v145/v149 di 5224–5231 dan 5265–5272 menunjukkan itu memang berlaku).

### Gaps
- Pengiraan "dipanggil" berasaskan regex teks; panggilan melalui rentetan (`window[nama]`) tidak dikesan — tidak ada bukti ia dipakai di sini.

## KQ4 — Pustaka

### Takeaway
Tiada pustaka JS luar langsung: `<script src>` = 0; satu-satunya sumber luar ialah Google Fonts (Inter). Semua carta ialah SVG inline tulisan tangan (23 `<svg`, 0 `<canvas>`), jadi tiada dua pustaka berfungsi sama.

### Cited Findings
- `<link rel="preconnect" href="https://fonts.googleapis.com">` dan stylesheet Inter [dashboard_v2.html:3–4](BacktestShariah2/standard/dashboard_v2.html); senarai URL luar dalam fail = dua URL itu sahaja.
- `<canvas>` 0, `getContext` 0, `<svg` 23, `<path` 14, `<polyline` 7, `<rect` 23 (grep atas fail penuh).
- Google Fonts disekat dalam kotak pasir ujian ("hanya Google Fonts disekat dalam kotak pasir") [binaan_v2_log.md:123](BacktestShariah2/standard/binaan_v2_log.md).

### Inferences
- Kebergantungan rangkaian tunggal = fon; kegagalannya hanya FOUT/fallback sistem, bukan kegagalan fungsi.

### Gaps
- Tiada.

## KQ5 — Mudah alih

### Takeaway
Tiada `<meta name="viewport">` standard dalam sumber (format artifact tanpa `<head>`; cengkerang penerbit membekalkannya), tetapi ada `claude:viewport-fit-sides`. 50 media query pada 6 titik putus (420/520/620/760·761/860/1100 px), transformasi jadual→kad bagi Posisi/Watchlist pada ≤ 760 px, saiz fon minimum 10 px; 5 daripada 17 `<thead>` statik melebihi 6 lajur, dan jadual dinamik Posisi mencapai 17 lajur.

### Cited Findings
- Meta: `<meta name="claude:viewport-fit-sides" content="cover">` [dashboard_v2.html:2](BacktestShariah2/standard/dashboard_v2.html); tiada `name="viewport"`. Peraturan format: "tanpa doctype/head; `<title>` + `<style>` di atas" [dashboard.md:6](BacktestShariah2/standard/dashboard.md). `semak_dashboard.js` membalut fail dengan `<head>` tanpa viewport meta [semak_dashboard.js:33](BacktestShariah2/ujian/semak_dashboard.js).
- Media query: 50; titik putus unik: `max-width 420, 520, 620, 760, 860, 1100`, `min-width 520, 761, 1100`, 4 `prefers-reduced-motion` (kiraan regex `@media[^{]+` atas CSS).
- Kad telefon: ≤ 760 px Posisi/Watchlist jadi kad lipat (v79, v81) dan tab sisi panel (v93/v94) [dashboard.md:3](BacktestShariah2/standard/dashboard.md); CSS `display:block` 56, `display:grid` 56, `data-label` 2, `::before{content:attr(` 1; 15 blok media sempit menyentuh `table/td/tr/th`, cth. `@media (max-width:760px){table[data-st="keputusan"] tbody td{flex-wrap:wrap…` (hasil pengiraan dalam audit).
- Fon: `html{font-size:16px}`, `body … font-size:14.5px`; nilai px dalam CSS: 10, 11, 12, 14.5, 16 px; `.pill` 0.72rem (≈ 10.4 px) — minimum berkesan ≈ 10 px.
- Lajur: 17 blok `<thead>` statik dalam templat; bilangan `<th>` = [0,2,3,4,4,4,4,4,4,5,5,6,7,7,8,10,11] → **5 jadual > 6 lajur** (kaedah: regex `<thead>…</thead>` atas JS; jadual yang membina tajuk daripada tatasusunan, seperti `ptCols()` 14 lajur [dashboard.md:31](BacktestShariah2/standard/dashboard.md) dan Posisi Penuh 17 lajur [dashboard.md:3 (v130)](BacktestShariah2/standard/dashboard.md), **tidak** dikira). Baris setiap halaman: telefon 10 (+25), desktop 25 (+100) — `?10:25` di 1130–1131,1863 dan `+100` di 4885.
- Had langganan telefon: pelanggan db menolak > ~60 langganan serentak ("Too many active subscriptions" pada telefon pengguna 4 Nov 2026) [semak_kolam_langganan.js:3–7](BacktestShariah2/ujian/semak_kolam_langganan.js); kolam `KOLAM.maks=44` dengan syarat "mesti muat langganan KEKAL (22 dokumen asas) + kumpulan terbesar serentak (ringkas_c: 21 anak)" [dashboard_v2.html:5156–5161](BacktestShariah2/standard/dashboard_v2.html). Hari ini: 22 panggilan `sub/subBhg/subRingkas` asas + 2 `langgan` (`meta/info`, `harian/status`) ≈ 24 kekal, dan `ringkas_c` ada **26** anak (17 bahagian + 9 kamus) → 50 > 44; penjaga kemajuan menaikkan had +3 setiap 2 s hingga 64 [dashboard_v2.html:5183–5185](BacktestShariah2/standard/dashboard_v2.html).

### Inferences
- Pada telefon, tab Posisi memuat lebih perlahan daripada yang direka (had 44 kini di bawah keperluan 50); ia masih memuat kerana penjaga kemajuan, tetapi komen dan ujian `semak_kolam_langganan.js` (had 46/50/60 lulus dengan 21 anak) perlu diukur semula dengan 26 anak.

### Gaps
- Tiada ukuran render sebenar pada 390 px dibuat di sini (Playwright tidak dipasang; `semak_dashboard.js` perlu `playwright`).

## KQ6 — Kesegaran/latensi setiap tab pada 09:00 NY (telefon) dan 20:00 NY (desktop)

### Takeaway
Semua tab data harian disegarkan **sekali** sehari pada 10:20 NY (Isn–Sab) oleh sesi LLM, selepas belian 09:40. Akibatnya pada **09:00 NY** telefon memapar petikan **pagi semalam**: harga tutup T−2 (1 sesi di belakang sesi terakhir yang sudah lengkap di repo sejak ~01:48 NY), belian semalam, dan watchlist/rancangan beli semalam — rancangan beli **hari ini** (yang `beli.yml` laksana 40 minit kemudian) tidak kelihatan. Pada **20:00 NY** desktop memapar tutup T−1 + belian hari ini (1 sesi di belakang; tutup hari ini tidak ada di mana-mana sehingga 00:07 NY). Kes terburuk (10:20 dan 12:20 gagal) = +24 jam = 2 sesi.

### Cited Findings
- Jadual cron (UTC → NY EST) dan masa komit sebenar yang diperhatikan:
  - `harian.yml` `7 5/7/9/11 * * 2-6` = 00:07/02:07/04:07/06:07 NY Sel–Sab [harian.yml:16–19](.github/workflows/harian.yml); komit sebenar `1d476fe` 2026-11-06 06:48 UTC = **01:48 NY** (sesi 2026-11-05) → menulis `papertrade/*`, `data/trend`, `data/stage`, stor harga, `KOORDINATOR.md`.
  - `lejar.yml` `17 6/10 * * 2-6` = 01:17/05:17 NY [lejar.yml:13–14](.github/workflows/lejar.yml); komit `cb82b29` 2026-11-05 07:07 UTC = **02:07 NY** (sesi 2026-11-04) → `lejar/`, `portfolio_slot/`.
  - `analisis.yml` dicetus `workflow_run` Lejar penuh [analisis.yml:10–11](.github/workflows/analisis.yml); komit `77e2dc8` 07:08 UTC = **02:08 NY** → `data/analisis/papan.json`, `lift.json` (`lift_kaedah.py`) [analisis.yml:36–52](.github/workflows/analisis.yml).
  - `petang.yml` `47 11, 17 12 * * 1-5` = 06:47/07:17 NY [petang.yml:11–12](.github/workflows/petang.yml); komit `d01f8fb` 12:40 UTC = **07:40 NY** → gred P.
  - `beli.yml` `40 14 * * 1-5` = 09:40 NY (± pintu musim) [beli.yml:27–32](.github/workflows/beli.yml); komit `790bf6b` 14:45 UTC = **09:45 NY**.
  - `rs_pasaran.yml` 22:41/03:17 UTC = 17:41/22:17 NY; `gred_kumpulan.yml` 04:17/08:17 UTC = 23:17/03:17 NY; `skrin_tv.yml` 21:47 UTC = 16:47 NY; `harga_harian.yml` 21:37/00:23 UTC — semua memberi input kepada `harian.yml` esok [KOORDINATOR.md:87–104](KOORDINATOR.md).
  - Tolakan db: 10:20 NY Isn–Sab [tolak_db.md:3](BacktestShariah2/jadual/tolak_db.md); semakan 12:20 NY [tolak_db_semak.md:3](BacktestShariah2/jadual/tolak_db_semak.md); mingguan Ahad 10:47 MYT = Sabtu 21:47 NY [mingguan.md:3](BacktestShariah2/jadual/mingguan.md).
- Peraturan "data muktamad": `pengawas()` menganggap sesi hanya boleh diproses apabila tutup ≥ 9 jam lalu (01:00 NY) [jana_db.py:373–390](BacktestShariah2/standard/jana_db.py) — jadi tutup hari D tidak boleh masuk db sebelum ~02:00 NY D+1 walau apa pun.
- Keadaan dokumen yang dijana 2026-11-06 15:15 MYT (= 02:15 NY): `harian/status` `harga_tutup_pada 2026-11-05`, `kemaskini_pagi 2026-11-06 14:23 MYT`, `beli_pada 2026-11-05 22:44 MYT`, `gred_pada 2026-11-06 14:32 MYT`; `watchlist.tarikh_data 2026-11-05`; `harian/trend.tarikh 20261105` (947 baris); `analisis/papan.kini 2026-11-04` (dibina 2026-11-06 02:03 MYT — larian lejar 10:17 UTC tanpa sesi baharu); `analisis/lift.kini 2026-11-06`; `prestasi/portfolio_slot.sesi_terakhir 2026-11-04` (larian lejar 06:17 UTC 6 Nov belum komit pada masa klon).
- Peraturan kesegaran dashboard dalam `dashboard.md` masih menerangkan rutin Claude 8:02 malam MYT / 9:35 NY / 6:02 pagi MYT [dashboard.md:57–61](BacktestShariah2/standard/dashboard.md) yang **dimatikan 27 Okt 2026** (CLAUDE.md; `PERALIHAN.md`).

Kesegaran kes **biasa** mengikut tab (D = hari dibuka; "sesi lengkap terakhir" = tutup 16:00 sebelum masa buka):

| Tab | Dokumen pemacu | 09:00 NY telefon (db = tolakan D−1 10:20) | 20:00 NY desktop (db = tolakan D 10:20) | Kes terburuk (10:20 & 12:20 gagal) |
|---|---|---|---|---|
| Ringkasan, Prestasi, Posisi | `ringkas_c/m`, `garis`, `mae*`, `mfe`, `harian_kaedah`, `lorong2`, `jalur`, `trend`, `stage` | tutup **D−2** (1 sesi di belakang; 41 j selepas tutup yang dipapar); belian D−1 09:45; repo sudah ada D−1 sejak 01:48 → **lag db lawan repo ≈ 8.5 j** | tutup **D−1** (1 sesi di belakang; 28 j); belian D 09:45 | 2 sesi |
| Watchlist / "Esok" | `watchlist`, `trend`, `stage`, `garis` | watchlist yang dikira D−1 00:07 **untuk belian D−1** (sudah berlaku); rancangan D tidak kelihatan | watchlist D (dikira 00:07 D) — sudah dilaksana 09:40 | 2 sesi |
| Analisis | `analisis/papan`, `analisis/lift`, `harian_kaedah` | `kini` = D−2 (lejar D−1 02:07 memproses tutup D−2) | `kini` = D−1 | D−3 |
| Kombinasi N | `kaedah_n/papan` | dijana semula setiap 10:20 daripada CSV REVERSE; berubah hanya bila CSV berubah | sama | — |
| Backtest, Kaedah | `registry/*`, `meta/info`, `kaedah/katalog`, `autotune/*` | statik; `set` manual (tiada dalam tolakan harian) | sama | tiada jadual |
| Sektor | `sektor/snapshot`, `kumpulan/siri`, `watchlist` | `snapshot`: mingguan paling baik (Ahad), tetapi fail sumber tiada di `main`; `siri`: tiada penulis → **beku** | sama | tidak terhad |
| Pengepala "Kemas kini terakhir" | `harian/status` | menunjuk `kemaskini_pagi` D−1 | D | — |

Hujung minggu: Sabtu 10:20 menolak tutup Jumaat (harian Sab 00:07); Ahad tiada tolakan; Isnin 09:00 = tutup Jumaat (0 sesi di belakang); Selasa 09:00 = tolakan Isnin = tutup Jumaat (1 sesi).

### Inferences
- Detik telefon pagi ialah detik paling kurang dilayan: data yang pengguna mahu lihat sebelum pasaran (apa yang akan dibeli/dijual pada buka hari ini) sudah ada di repo sejak ~01:48 NY tetapi hanya sampai ke db 10:20, iaitu selepas pasaran buka. Satu tolakan tambahan ~02:30 NY (selepas `analisis.yml`) akan menutup jurang 8.5 j tanpa mengubah paip pengiraan; tolakan 10:20 kekal untuk membawa belian.
- Kesegaran "28 j" pada 20:00 NY ialah had reka bentuk (yfinance 9 j), bukan kelewatan paip.

### Gaps
- Kejayaan/kegagalan sebenar sesi 10:20 dan 12:20 (log tugasan berjadual Claude) tidak boleh dibaca dari repo; tiada rekod kadar kegagalan.
- Masa sebenar `mingguan.md` menolak `sektor/snapshot` kali terakhir tidak ada dalam repo (`binaan_v2_log.md` disemak hanya pada entri lama).

## KQ7 — Titik rapuh dan tadbir urus (`semak_terbit.py`, `dashboard_terbit.json`, `tolak_db.md` langkah 7, `amaran_ntfy.yml`, ujian)

### Takeaway
Semakan dua arah wujud tetapi asimetri: arah "disunting tanpa diterbit" disemak oleh CI (sha256 fail lawan manifes); arah "diterbit tanpa dikomit" hanya disemak oleh sesi LLM harian langkah 7 (Actions tidak boleh membaca artifact kerana Cloudflare), dan ia sudah berlaku tiga kali (v132–v138, v139, v151–v153). Tiada ujian JS dashboard dalam CI; tiga pemeriksa Playwright dijalankan tangan.

### Cited Findings
- `semak_terbit.py`: `semak()` membanding `sha256(dashboard_v2.html)` dengan `data/dashboard_terbit.json.sha256`; sama → 0, beza → 1 "dashboard_v2.html BERUBAH tetapi tidak diterbitkan"; `--kemas --versi --nombor` menulis manifes [semak_terbit.py:53–94](BacktestShariah2/standard/semak_terbit.py); hadnya dinyatakan dalam docstring ("BOLEH repo disunting tanpa diterbitkan … TIDAK diterbitkan tanpa dikomit") [semak_terbit.py:1–20](BacktestShariah2/standard/semak_terbit.py). Dijalankan dalam `semak_data.yml` [semak_data.yml:79–80](.github/workflows/semak_data.yml). Dijalankan di sini: `dashboard selaras dengan terbitan terakhir: versi 1793937695-9368 (#185), 683,519 bait`, exit 0.
- Manifes semasa: `versi_artifact 1793937695-9368`, `nombor 185`, `bait 683519`, `dikemas 2026-11-06 04:01 UTC`, nota v154 menyatakan "Terbitan ini juga memulihkan v151-v153 yang dikomit pada cawangan claude/sleepy-noether-gx742r tetapi tidak pernah digabung ke main, jadi manifes main tertinggal tiga versi di belakang artifact hidup" [dashboard_terbit.json](BacktestShariah2/data/dashboard_terbit.json).
- Langkah 7 `tolak_db.md`: `Artifact read` → version id baris pertama → banding `versi_artifact`; beza → `amaran_ntfy.yml` `workflow_dispatch` mesej `dashboard hidup <versi> != repo <versi>; perlu gabung`; "JANGAN terbit apa-apa dan JANGAN tulis ganti" [tolak_db.md:55–68](BacktestShariah2/jadual/tolak_db.md). `amaran_ntfy.yml` menerima `workflow_dispatch` dengan `tajuk`/`mesej` dan `workflow_run` bagi 15 workflow pada `failure/timed_out/startup_failure` [amaran_ntfy.yml:7–42](.github/workflows/amaran_ntfy.yml).
- Nota hanyutan terdahulu dalam `dashboard.md`: versi 163 "diterbitkan oleh sesi lain TANPA dikomit, jadi versi 164 dibina DI ATAS HTML hidup … `standard/jalur_jangka.py` dan `REVERSE/SILING_ARAH.md` masih TIADA dalam repo" dan v127 "diterbit daripada sesi lain dan belum ada dalam repo" [dashboard.md:3](BacktestShariah2/standard/dashboard.md).
- Rapuh #1 — gandingan PECAH↔`subBhg` berurutan ("pembaca dahulu, baru pemecah"; terbalik → "halaman kehilangan baris secara senyap") [jana_db.py:1150,1164–1166](BacktestShariah2/standard/jana_db.py); [dashboard_v2.html:5312–5320](BacktestShariah2/standard/dashboard_v2.html).
- Rapuh #2 — tolakan db ialah titik kegagalan tunggal LLM; `SystemExit` had 262,144 menghentikan **seluruh** tolakan malam, bukan satu dokumen [tolak_db.md:28–33](BacktestShariah2/jadual/tolak_db.md); [jana_db.py:1410–1411](BacktestShariah2/standard/jana_db.py).
- Rapuh #3 — notifikasi ntfy saiz db dalam `harian.yml` mati (syarat `steps.db.outputs.amaran != ''` tetapi output tidak pernah ditetapkan) [harian.yml:158–172, 219–226](.github/workflows/harian.yml).
- Rapuh #4 — koleksi `kaedah_n` tiada dalam langkah 3 → tiada `if_version` [tolak_db.md:23–25](BacktestShariah2/jadual/tolak_db.md).
- Rapuh #5 — `KOLAM.maks=44` < keperluan semasa 50 (KQ5); bergantung pada penjaga kemajuan.
- Rapuh #6 — klon cetek + sejarah HTML 2 komit: sebarang gabung "di atas HTML hidup" tidak boleh disahkan secara diff di repo ini.
- Ujian Python yang menyentuh paip dashboard (dijalankan CI `semak_data.yml:61–62` dan `harian.yml:181–185`): `test_jana_db_batch.py` (7 ujian protokol batch), `test_jana_db_ringkas.py`, `test_jana_db_garis.py`, `test_jana_db_harian_kaedah.py`, `test_jana_db_sesi.py`, `test_pecah_claude.py`, `test_penganalisis.py`, `test_semak_terbit.py` (5 ujian: tiada manifes gagal, selaras lulus, fail berubah gagal, manifes merekod versi/saiz, `--kemas` tanpa `--versi` mengekalkan versi) [test_semak_terbit.py:28–60](BacktestShariah2/ujian/test_semak_terbit.py). **Tiada** ujian Python memuatkan `dashboard_v2.html` (grep `dashboard_v2` dalam `ujian/*.py` hanya mengenai rentetan nama dalam 3 fail).
- Ujian JS (Playwright, **tangan sahaja**, "tidak dipasang dalam semak_data.yml"): `semak_dashboard.js` (audit susun atur semua tab; `--min-jadual` ditambah 4 Nov 2026 selepas liputan jatuh 44→22 jadual tanpa disedari) [semak_dashboard.js:1–30](BacktestShariah2/ujian/semak_dashboard.js); `semak_himpun_db.js` (penghimpunan dokumen padat) [semak_himpun_db.js:1–13](BacktestShariah2/ujian/semak_himpun_db.js); `semak_kolam_langganan.js` (had langganan) [semak_kolam_langganan.js:1–25](BacktestShariah2/ujian/semak_kolam_langganan.js).

### Inferences
- Arah "diterbit tanpa dikomit" tidak akan tertutup dengan alat semasa; satu-satunya mitigasi struktur ialah peraturan proses (terbit hanya daripada sesi yang komit ke `main` dan jalankan `--kemas` dalam komit yang sama) — dan v151–v153 menunjukkan "dikomit pada cawangan" pun tidak memadai: manifes di cawangan tidak dilihat `main`.
- Ketiadaan ujian JS dalam CI bermakna regresi render (cth. tab kosong kerana had langganan) hanya ditemui oleh pengguna di telefon, seperti pada 3–4 Nov 2026.

### Gaps
- Sama ada `semak_dashboard.js`/`semak_himpun_db.js` dijalankan sebelum terbitan v154 tidak direkod (komit `372db4a` tidak menyebutnya).

## KQ8 — Peraturan `dashboard.md` dan pelanggaran oleh v154

### Takeaway
`dashboard.md` sendiri basi (menyatakan "Versi semasa = versi 132 (artifact versi 164)" sedangkan repo di v154/#185; fail tidak berubah sejak klon awal) dan bahagian "Cara kemas kini harian" menerangkan rutin yang terbatal. Peraturan paparan yang boleh disemak secara statik dipatuhi v154 (storan pelayar dalam try/catch, format tanpa head, 10/25 baris, sha selaras); pelanggaran yang pasti ialah **dokumentasi**, bukan kod.

### Cited Findings
Peraturan (dengan status v154):
1. Sumber = `standard/dashboard_v2.html`, format artifact tanpa doctype/head, `<title>` + `<style>` di atas; halaman terbit mesti sama dengan fail [dashboard.md:6](BacktestShariah2/standard/dashboard.md) — **patuh**: baris 1 `<title>Papan Backtest Shariah</title>`, `<style>` baris 5; `semak_terbit.py` exit 0.
2. Capabilities `assets`, `db`; jangan ubah semasa menerbit [dashboard.md:7] — tidak boleh disemak dari repo.
3. Jadual tab ↔ dokumen db [dashboard.md:10–20] — **hanyut** (KQ1d: `analisis/lift`, `kumpulan/siri`, `harian/trend`/`stage` dalam Watchlist tidak disenaraikan).
4. Lajur M/C/Prestasi sama susunan `ptCols()` 14 lajur [dashboard.md:31] — tidak disemak secara dinamik.
5. Semua jadual boleh disusun kecuali Banding [dashboard.md:32] — tidak disemak.
6. `keluar=true` → baris merah, harga dibekukan [dashboard.md:33] — tidak disemak.
7. Setiap istilah ada tooltip; kamus `TIPS` = glosari [dashboard.md:34] — `TIPS` wujud (4842–5016); `data-tip` 121, `title="` 90.
8. Telefon ≤ 760 px: 10 baris, +25; desktop 25, +100 [dashboard.md:37] — **patuh** (`?10:25` 1130–1131,1863; `+100` 4885).
9. Storan pelayar hanya tab/sub-tab/set/lipatan, dibalut try/catch [dashboard.md:39] — **patuh pada try/catch** (23 kejadian `localStorage`, semuanya dalam `try{…}catch`, termasuk blok 1132–1136); skop kunci lebih luas daripada ayat itu: `pbs3_tab, pbs3_akaun, pbs_set, pbs2_b4, pbs2_sub, pbs3_lajur, pbs3_pandangan, pbs2_fold, pbs2_pnav_pilih, pbs2_pnav, pbs3_lajur_semua` (pandangan/lajur/rel panel = keutamaan UI).
10. Had dokumen 256 KiB; `claude_N` tanpa had; `watchlist`/`senarai_beli` dibahagi `bahagi_db` [dashboard.md:64] — **hanyut**: senarai PECAH kini 14 nama; `senarai_beli` tidak ditolak.
11. "Jika halaman perlu diubah": edit → uji Playwright 1400 px dan 390 px → `Artifact read` → publish dengan `url` sama → commit [dashboard.md:67] — komit v154 tidak merekod ujian; CLAUDE.md menambah `semak_terbit.py --kemas` + komit manifes (dipatuhi: manifes #185 dikomit bersama).
12. Bentuk `prestasi/mae` = peta [dashboard.md:45] — **hanyut** (kini senarai pasangan, KQ2).
13. "Cara kemas kini harian" 8:02 malam / 9:35 / 6:02 pagi rutin Claude [dashboard.md:57–61] — **terbatal** sejak 27 Okt 2026 (Actions `harian.yml`/`beli.yml` + `tolak_db.md` 10:20 NY).
14. Pengepala `dashboard.md` "Versi semasa = versi 132 (artifact versi 164; 2 Nov 2026)" [dashboard.md:3] lawan manifes `nombor 185`, nota "v154" — **22 versi tidak didokumenkan** dalam fail peraturan (`git log -- dashboard.md`: hanya komit klon `2ed7a27`).

### Inferences
- Fail peraturan dan sumber kebenaran operasi sudah berpisah: peraturan hidup sebenar berada dalam komen kod (`jana_db.py` PECAH, `dashboard_v2.html` connect) dan `jadual/*.md`, manakala `dashboard.md` ialah log sejarah hingga v132. Pembaca baharu yang mengikut `dashboard.md` §57–64 akan menjalankan prosedur yang salah.

### Gaps
- Peraturan paparan 4–6 memerlukan render sebenar untuk disahkan; tidak dibuat (tiada Playwright).
