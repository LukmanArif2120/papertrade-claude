# Audit tab katalog kaedah dashboard v154: `kaedah` · `kaedahn` · `backtest`

Skop: tiga tab METHOD-CATALOG dalam `BacktestShariah2/standard/dashboard_v2.html` (v154, 683,519 bait, manifes `data/dashboard_terbit.json` nombor 185, 6 Nov 2026). Semua angka dikira daripada fail repo pada 6 Nov 2026; tiada akses ke db hidup, jadi kandungan db dinyatakan daripada penjana (`jana_db.py`, `katalog_kaedah.json`, `dashboard_kemaskini.py`) dan audit 24 Okt 2026 yang pernah memuat turun db. Matlamat pemilik yang dipakai pada setiap penilaian: "SATU kaedah untuk wang sebenar — rugi kecil, untung besar". Setiap panel dinilai: **MEMUTUSKAN** (membantu pilih kaedah) atau **MENGKATALOG** (hanya menerangkan), dan status REDUNDAN / MATI / PENTING / HILANG.

## Soalan 1: Mengapa TIGA tab untuk kaedah, dan apa yang setiap satu tunjukkan (inventori panel demi panel + pertindihan lajur)?

### Takeaway
Tiga tab ialah tiga **populasi dan tiga sumber data** yang tumbuh berasingan — `backtest` = registry enjin v1.2 set 431/S1–S4 (141 kaedah M, 1,589 varian) + AUTOTUNE 2000 saham; `kaedah` = katalog teks tangan 228 baris (134 M + 94 N) yang menggabungkan semula baris registry 431 dan dagangan Papertrade C; `kaedahn` = dokumen `kaedah_n/papan` (263 baris registry N + 94 kombinasi produksi + 413 ujian pradaftar REVERSE). Angka backtest Mxx yang sama (CAGR, MDD, menang, purata/dagangan, hari pegang, n, keputusan) dipapar di **lima** tempat: Backtest › Keputusan, Backtest › Butiran, Kaedah (lajur `Backtest (set 431)`), Analisis (`bt_*`) dan podium Ringkasan. Tiada satu pun daripada tiga tab ini memangkat Mxx dan Nxx pada paksi yang sama; satu-satunya tempat itu berlaku ialah panel Lift dalam tab Analisis (v154).

### Cited Findings

**Peta tab → paparan → sumber db**
- Butang tab: `backtest`, `kaedah`, `kaedahn` — [dashboard_v2.html:1065-1067](../../BacktestShariah2/standard/dashboard_v2.html#L1065). `backtest` ada dua sub-tab (`keputusan`, `butiran`) dan `butiran` bercabang tiga pandangan 431/S1–S4 (`papan`, `ringkasan`, `banding`) + set `2000` (`v-autotune`) — `viewId()` [dashboard_v2.html:1200](../../BacktestShariah2/standard/dashboard_v2.html#L1200); `B4=[papan, ringkasan, banding]` [:1342](../../BacktestShariah2/standard/dashboard_v2.html#L1342); `AT_V` 4 versi AUTOTUNE (`sar`, `a02`, `a03`, `a01`) [:2389](../../BacktestShariah2/standard/dashboard_v2.html#L2389). Jadi "tiga tab" sebenarnya **tujuh pandangan** berbeza (keputusan, papan, ringkasan, banding, autotune×4 versi, kaedah, kaedahn).
- Langganan db: koleksi `registry` penuh (`limit(1000)`) dimuat pada SETIAP pembukaan halaman tanpa mengira tab, dan menetapkan label "Langsung · ujian terkini <tarikh>" — [dashboard_v2.html:5214-5217](../../BacktestShariah2/standard/dashboard_v2.html#L5214); `meta/info` [:5219](../../BacktestShariah2/standard/dashboard_v2.html#L5219); `kaedah/katalog` → `S.kat` [:5341](../../BacktestShariah2/standard/dashboard_v2.html#L5341); `kaedah_n/papan` → `S.kn` (subBhg) [:5347](../../BacktestShariah2/standard/dashboard_v2.html#L5347); koleksi `autotune` penuh [:5349](../../BacktestShariah2/standard/dashboard_v2.html#L5349).
- Penulis db: `registry/<ID>` ditulis manual oleh `dashboard_kemaskini.py` (CSV → JSON, `set registry/<ID>`) — [dashboard_kemaskini.py:1-4](../../BacktestShariah2/standard/dashboard_kemaskini.py#L1); `kaedah/katalog` ditolak manual daripada `standard/katalog_kaedah.json` (dashboard.md langkah 4) — [dashboard.md:62](../../BacktestShariah2/standard/dashboard.md#L62); `kaedah_n/papan` dijana `jana_db.kaedah_n()` setiap tolakan db [jana_db.py:574](../../BacktestShariah2/standard/jana_db.py#L574), [:1390-1392](../../BacktestShariah2/standard/jana_db.py#L1390). `meta/info` **tiada penulis dalam repo** (grep `standard/*.py`, `jadual/*.md`, `.github/workflows/*.yml` → 0 padanan). `tolak_db.md` tidak menyebut `katalog`, `registry` atau `meta/info` (grep → 0) — [tolak_db.md:18-37](../../BacktestShariah2/jadual/tolak_db.md#L18) hanya `jana_db.py` + batch.

**Tab `backtest` › Keputusan (`renderKeputusan`, 5,323 bait kod)**
- Panel 1 — headline + podium 3 teratas (`kpPod`): "Terbaik ikut backtest: M..", "RM10,000 → RM… dalam 6.9 tahun", jatuh terburuk, menang x/10, pegang, Ujian 2, papertrade C — [dashboard_v2.html:1290-1295](../../BacktestShariah2/standard/dashboard_v2.html#L1290), [:1311-1312](../../BacktestShariah2/standard/dashboard_v2.html#L1311).
- Panel 2 — "Saringan 7 langkah" corong boleh ketik; `LANGKAH` 1–5 = gate enjin G2/G3/G4/G1/G5 pada set 431; 6 = CAGR S1–S4 semuanya > 0; 7 = `min(cA,cB) > 0` pada `autotune/a02_saringan` — [dashboard_v2.html:1239-1247](../../BacktestShariah2/standard/dashboard_v2.html#L1239), logik `kpM` [:1251-1268](../../BacktestShariah2/standard/dashboard_v2.html#L1251). Pingat 🥇/🥈/🥉 = `keputusan` enjin GUNA/UJI KERTAS/SIMPAN bagi varian aktif (`varian_kod` daripada katalog) [:1248](../../BacktestShariah2/standard/dashboard_v2.html#L1248), [:1256](../../BacktestShariah2/standard/dashboard_v2.html#L1256).
- Panel 3 — jadual "Semua kaedah" 10 lajur `kpCols`: #, Kaedah, Keputusan/pingat, Saringan 1–7 (7 titik), Untung setahun Ujian 1 (+RM10k→), Untung setahun Ujian 2 (A/B), Jatuh terburuk, Menang x/10, Pegang (+dag/thn), Papertrade C (`prStats` purata kasar) — [dashboard_v2.html:1279-1289](../../BacktestShariah2/standard/dashboard_v2.html#L1279). Penapis: Dapat pingat/Semua, cip "Gaya saya ≤ 40 hari", carian.
- Jalur "Cara baca" + kaki "Hasil backtest, bukan jaminan" — [:1323-1324](../../BacktestShariah2/standard/dashboard_v2.html#L1323).
- Populasi: hanya `id[0]==='M'` set 431 [:1257](../../BacktestShariah2/standard/dashboard_v2.html#L1257) = 141 kaedah M unik dalam `registry_M_gabung.csv` (1,589 baris: 633 set 431 + 239 × S1–S4; keputusan 431: DITOLAK 446, SIMPAN 128, UJI KERTAS 48, GUNA 11; 0 baris indikator `I`) — [data/registry_M_gabung.csv](../../BacktestShariah2/data/registry_M_gabung.csv) (dikira 6 Nov 2026).

**Tab `backtest` › Butiran › Papan penuh (`renderPapan`, 3,061 bait)**
- Jadual 22 lajur: Kaedah/varian, Keputusan, `COLS` 18 metrik (skor, jumlah, cagr, win, n, avg, avgwin, avgloss, nisbah, days, harian, mdd, mar, ret10, hit10, bulan10, pf, dagangan_setahun), Gate gagal — [dashboard_v2.html:1413-1420](../../BacktestShariah2/standard/dashboard_v2.html#L1413), [:1433-1436](../../BacktestShariah2/standard/dashboard_v2.html#L1433). Penapis `jenisSeg` Semua / Kaedah M / **Indikator I** [:1440](../../BacktestShariah2/standard/dashboard_v2.html#L1440) sedangkan CSV repo ada 0 baris `I` (db Okt 2026 pernah ada 32 dokumen I — [tab_lain.md:41](../Audit%20dashboard%20tab%20demi%20tab/tab_lain.md)).
- Helaian butiran `openDetail`: 6 gate G1–G6, kad saringan 7 langkah, 23 metrik `mgrid`, carta profil pegangan 5–60 hari, "Konsisten merentas set" S1–S4, butang Tambah ke banding — [dashboard_v2.html:1460-1491](../../BacktestShariah2/standard/dashboard_v2.html#L1460).

**Tab `backtest` › Butiran › Carta & gaya (`renderRingkasan`, 5,298 bait)**
- 4 KPI (Kaedah diuji; GUNA+UJI KERTAS; "Terbaik gaya anda" = `bestBy(..,'avg')` atas SEMUA varian termasuk DITOLAK; Atasi beli semua), jadual "Gaya anda" 8 varian ≤ 40 hari ≥ 100 entry, "Taburan keputusan" + "Skor tertinggi" 5, serakan CAGR lawan MDD, jalur "Ingat" (kadar menang 30–40%), jalur "Tindakan seterusnya: Pantau dalam papertrade M.., M.., M.." — [dashboard_v2.html:1348-1388](../../BacktestShariah2/standard/dashboard_v2.html#L1348).

**Tab `backtest` › Butiran › Banding varian (`renderBanding`, 3,729 bait)**
- Pilih ≤ 3 varian (lalai: 3 skor tertinggi), carta profil pegangan + jadual 24 metrik ikut baris — [dashboard_v2.html:1510-1532](../../BacktestShariah2/standard/dashboard_v2.html#L1510).

**Tab `backtest` › set 2000 (AUTOTUNE, `renderAutotune` + 3 pandangan, 18,423 bait)**
- `sar` saringan 134 kaedah × 2 lorong PARAM asal 2013–2018, KPI "Menang ≥ 55%", "CAGR > 0", "Atasi SPY" [dashboard_v2.html:2443-2473](../../BacktestShariah2/standard/dashboard_v2.html#L2443); `a02` parameter ditala / `a03` fokus kadar menang (label LULUS/CALON, MENANG/HAMPIR) [:2402-2442](../../BacktestShariah2/standard/dashboard_v2.html#L2402); `a01` walk-forward 12 tetingkap + kemajuan tala + portfolio gabungan [:2356-2388](../../BacktestShariah2/standard/dashboard_v2.html#L2356). Sumber folder `AUTOTUNE/hasil`, `hasil_a02`, `hasil_a03` wujud dalam repo.

**Tab `kaedah` (`renderKaedah`, 7,494 bait)**
- Headline: "Katalog 228 baris — DUA keluarga: 134 kaedah Mxx … dan 94 kombinasi NxxXyy … 94 kombinasi NxxXyy **belum** [dibeli] — lihat panel Status dalam tab Kombinasi N" — teks TETAP, tidak membaca `PR.berjalan` — [dashboard_v2.html:2284](../../BacktestShariah2/standard/dashboard_v2.html#L2284). Repo 6 Nov 2026: `papertrade/claude*.csv` ada **3,419** posisi Nxx merentas 94 ID; Lejar `terbuka.csv` 35,103 + `tunggu.csv` 3,101 baris Nxx (dikira atas `id_kaedah`).
- 5 KPI teks (Baris dalam kod; Backtest/papertrade nBt/nPt; Ada had masa; Beli "Buka esok"; Dua lorong keluar) — [:2285-2291](../../BacktestShariah2/standard/dashboard_v2.html#L2285).
- Jadual "Semua kaedah": mod ringkas 4 lajur (Kaedah, Backtest set 431, Papertrade C, Asal) atau penuh 7 lajur (ID, Kaedah, Asal, Masuk, Keluar, Pegang, Henti rugi) dengan pil jenis peraturan (`katPilOf`) — [:2274-2283](../../BacktestShariah2/standard/dashboard_v2.html#L2274), [:2225-2237](../../BacktestShariah2/standard/dashboard_v2.html#L2225). Segmen Semua/Kaedah M/Kombinasi N (v132).
- Lajur Backtest = baris registry set 431 bagi `varian_kod`, dipapar dengan `kpStatus` yang sama seperti tab Backtest (pingat/langkah gagal, CAGR, MDD, avg, win, n, days) — `katGabungM` [:2244-2251](../../BacktestShariah2/standard/dashboard_v2.html#L2244). Lajur Papertrade C = `prStats` (purata semua dagangan, menang, terburuk, n) + pil status Analisis `kdPill` [:2252-2253](../../BacktestShariah2/standard/dashboard_v2.html#L2252), [:1944-1945](../../BacktestShariah2/standard/dashboard_v2.html#L1944).
- Jalur "Sama untuk semua" (peraturan pelaksanaan + kekhususan Nxx: `stop = NaN`, `tgt = NaN`, 126 bar, U14, tiada backtest 431) [:2297](../../BacktestShariah2/standard/dashboard_v2.html#L2297); kaki "Dibina ${k.dibina}" = **2026-10-17** dalam `katalog_kaedah.json` walaupun 94 baris N ditambah 2 Nov — [katalog_kaedah.json](../../BacktestShariah2/standard/katalog_kaedah.json) (`dibina` 2026-10-17; 228 baris; medan `id, nama, varian, varian_kod, pencipta, sumber, masuk, keluar, pegang, henti`; 0 baris ada `ringkas`/`baris` yang kod cuba baca [:2241,2278](../../BacktestShariah2/standard/dashboard_v2.html#L2241)).
- Helaian `openKaedah`: cara berfungsi (masuk/keluar/henti/pegang/asal), Papertrade akaun, "Sebenar lawan backtest" (`bt_vs_pt`), Backtest set 431 + kad saringan — [:2678-2705](../../BacktestShariah2/standard/dashboard_v2.html#L2678).

**Tab `kaedahn` (`renderKaedahN`, 35,283 bait — terbesar antara ketiga-tiga)**
- Headline + 4 KPI (Kombinasi dipilih; Baris registry 263; Lulus gate kajian %; Terbaik diukur) — [dashboard_v2.html:4596-4602](../../BacktestShariah2/standard/dashboard_v2.html#L4596).
- Panel Produksi (jika `d.produksi`): status dikira, ayat "kesimpulan", 4 KPI (Masuk × keluar; Tanpa 5% POSITIF n/94 + berapa X13; Keluarga masuk; Konfigurasi C01 · tiada henti), corong 7 tahap daripada 1,495 sel, jadual 11 lajur (#, Kombinasi, Masuk — bila beli, Keluar — bila jual, Jangkaan tahan/latih, Lift tahan/latih, n, Menang, Untung/rugi, Tanpa 5%, p) dengan segmen tapis ikut keluar, nota `had`, nota "Prestasi hadapan … ada dalam tab Analisis" — [:4603-4637](../../BacktestShariah2/standard/dashboard_v2.html#L4603).
- Panel ⚠ Penarikan balik `m=8` (`d.tarik`) [:4638-4645](../../BacktestShariah2/standard/dashboard_v2.html#L4638); Keputusan akhir E1–E6 + jadual T4 SPUS+tunai (`d.akhir`) [:4655-4672](../../BacktestShariah2/standard/dashboard_v2.html#L4655); Baris gilir E1–E6 (`d.giliran`) [:4673-4679](../../BacktestShariah2/standard/dashboard_v2.html#L4673); Kad skor 413 ujian + corong setiap pradaftar + jadual GB02_atau3 "BERSARA" (`d.skor`) [:4680-4700](../../BacktestShariah2/standard/dashboard_v2.html#L4680); "Empat pradaftar, empat keputusan" (gate A/B/GAB/SX) [:4701-4706](../../BacktestShariah2/standard/dashboard_v2.html#L4701); Portfolio (`d.port`) [:4707-4716](../../BacktestShariah2/standard/dashboard_v2.html#L4707); Cara masuk C01–C06 (`d.cara`) [:4717-4722](../../BacktestShariah2/standard/dashboard_v2.html#L4717); Silang akhir (ditarik balik) [:4723-4727](../../BacktestShariah2/standard/dashboard_v2.html#L4723); Keluar X01–X45 sebaran [:4728](../../BacktestShariah2/standard/dashboard_v2.html#L4728); Registry penuh 7 lajur (ID, Nama, Sumber, Status PERLU/SEDIA/DIUJI, Lift tahan, Jangkaan, Tanpa 5%) [:4729-4731](../../BacktestShariah2/standard/dashboard_v2.html#L4729); Semua ujian dipradaftar 16 lajur [:4732-4769](../../BacktestShariah2/standard/dashboard_v2.html#L4732); Nota. Jumlah **13 panel**, 9 daripadanya jadual statik `<table data-st="kn-*">` (cara, diambil, gate, giliran, keluar, port, silang, skor, t4).
- Sumber: `kaedah_n(dibina)` membaca `data/registry_N.csv` (263 baris: DIUJI 147, PERLU 99, SEDIA 17) + `REVERSE/nxx.csv`, `nxx_keluar.csv`, `gabungan.csv`, `silang_akhir.csv`, `portfolio_n_ringkas.csv`, `cara.csv`, `portfolio_94_ringkas.csv`, `cara_keluar_94.csv` — [jana_db.py:605-635](../../BacktestShariah2/standard/jana_db.py#L605); produksi daripada `REVERSE/jejak_semua.csv` + `grid_penuh.csv` [jana_db.py:460](../../BacktestShariah2/standard/jana_db.py#L460). Dokumen 234,697 bait = 89.5% had 262,144 (4 Nov) dan dipecah (`PECAH`) — [jana_db.py:1172-1177](../../BacktestShariah2/standard/jana_db.py#L1172).

**Pertindihan lajur demi lajur (angka Mxx yang SAMA, sumber `registry/*` set 431 varian aktif)**
- CAGR: Backtest Keputusan `u1` [:1284] · Papan `cagr` [:1413] · Kaedah `selBt` "Untung setahun" [:2250] · Analisis `bt_cagr` "Backtest 431" [:4435+] · Ringkasan podium `kpPod` [:4359-4360] = **5 tempat**.
- MDD: Keputusan `mdd` · Papan `mdd` · Kaedah "jatuh terburuk" · Analisis helaian `bt_mdd` · podium = 5.
- Kadar menang: Keputusan `win` ("x/10") · Papan `win` · Kaedah "menang" · Analisis `bt_menang` · podium = 5.
- Purata setiap dagangan: Papan `avg` · Kaedah · Analisis `bt_purata` = 3 (Keputusan tidak memaparkannya).
- Hari pegang: Keputusan `days` · Papan `days` · Kaedah · Analisis `hari` · podium = 5.
- n dagangan + dagangan/tahun: Keputusan · Papan · Kaedah · Analisis `bt_n`/`bt_setahun` = 4.
- Keputusan enjin GUNA/UJI/SIMPAN/DITOLAK: Keputusan (pingat) · Papan (pil) · Kaedah (`kpStatus`) · Analisis `bt_keputusan` · podium = 5.
- Semakan luar sampel S1–S4 / AUTOTUNE 2000: Keputusan langkah 6–7 (ambang > 0) · Analisis `lulus_subset`/`lulus_at` (ambang atasi EW ≥ 3/4; > SPY A dan B) — **dua takrif berbeza untuk ujian yang sama**; WFO hanya dalam Analisis.
- Papertrade C purata kasar (`prStats`): Keputusan `kp_pt` [:1289] · Kaedah `selPt` [:2252] · Prestasi; Analisis memakai `c_purata`/`h_purata` (matang, dipangkas) — nombor berlainan untuk soalan sama.
- Lajur yang WUJUD HANYA di satu tab: Backtest Papan = skor, jumlah, mar, h1/h2, ret10/hit10/bulan10, pf, harian, gate_gagal, profil pegangan, banding; Kaedah = masuk/keluar/pegang/henti teks + pencipta/sumber; Kombinasi N = jangkaan/lift/tanpa5/n/p/keluar bagi Nxx + semua rekod REVERSE.
- Nxx: `kaedah` memaparkan 94 baris teks (tanpa backtest, `selBt` → "Tiada dalam registry"); `kaedahn` Produksi memaparkan nombor kajian; Analisis `papan.json` ada 94 baris N dengan `bt_*` = null, `kedudukan` = null (0/94), `status` = BELUM CUKUP (94/94), `h_posisi` jumlah 37,069 — [data/analisis/papan.json](../../BacktestShariah2/data/analisis/papan.json); `lift.json` memangkat 180 kaedah termasuk 89 N — [data/analisis/lift.json](../../BacktestShariah2/data/analisis/lift.json), panel Lift [dashboard_v2.html:4397-4432](../../BacktestShariah2/standard/dashboard_v2.html#L4397).

### Inferences
- Tiga tab wujud kerana tiga lapisan sejarah: enjin v1.2 (Okt 2026 awal, registry), katalog pembaca pemula (17 Okt, versi 73), dan kajian REVERSE/Nxx (31 Okt–2 Nov). Tiada satu pun direka untuk soalan "kaedah mana"; `backtest` menjawab "varian mana lulus gate enjin", `kaedah` menjawab "apa peraturan kaedah ini", `kaedahn` menjawab "apa yang kajian REVERSE ukur".
- **REDUNDAN**: Backtest › Keputusan jadual (angka = Analisis `bt_*` + semakan luar sampel yang Analisis buat dengan lebih ketat); Kaedah lajur Backtest (set 431) dan Papertrade C (pendua Keputusan/Prestasi/Analisis dengan takrif berbeza); podium Ringkasan (salinan `kpPod`); Backtest › Carta & gaya KPI "Terbaik gaya anda" (menobatkan varian DITOLAK yang tidak didagang). **PENTING tetapi MENGKATALOG**: Kaedah lajur masuk/keluar/pegang/henti (satu-satunya tempat peraturan dibaca manusia); Kombinasi N panel Produksi (satu-satunya tempat nombor pradaftar Nxx + keluar setiap kombinasi). **MATI/RUJUKAN**: Papan penuh 22 lajur, Banding, 4 versi AUTOTUNE, 9 jadual statik rekod kajian `kn-*` — bahan penyelidikan, bukan keputusan harian. **HILANG**: satu jadual Mxx+Nxx pada ukuran hadapan yang sama DI DALAM tab kaedah (ia hanya ada dalam Analisis panel Lift v154).
- `kaedah` headline dan `dashboard.md` menyatakan Nxx "belum" dibeli sedangkan 3,419 posisi C sudah ada: prosa tangan hanyut tepat seperti amaran `jana_db._produksi_n` [:440-448].

### Gaps
- Kandungan db hidup (`registry` 173 dokumen termasuk 32 `I`? `meta/info` nilai `ew/spy/qqq`?) tidak boleh disahkan tanpa `ArtifactData`; angka db yang disebut datang daripada audit 24 Okt 2026.
- Tiada telemetri klik; "MATI" bermaksud "tiada keputusan bergantung padanya", bukan "tidak pernah dibuka".

## Soalan 2: Adakah pangkat backtest masih dipapar sebagai isyarat "kaedah terbaik", dan adakah dashboard menyatakan ia tiada kuasa ramalan?

### Takeaway
Ya, pangkat backtest masih dipersembahkan sebagai "Terbaik ikut backtest" dengan pingat emas/perak/gangsa, nombor `#` dan "RM10,000 → RM…" di dua tempat (Backtest › Keputusan dan Ringkasan), dan tiada satu ayat pun dalam 683 KB HTML yang menyebut dapatan `KAEDAH_TERBAIK.md` bahawa pangkat backtest tiada kuasa ramalan boleh ukur atau bahawa 0/134 lulus AUTOTUNE pada ambang Analisis; perkataan "meramal" hanya muncul bagi sektor/trend/stage.

### Cited Findings
- Headline Keputusan: "Daripada N kaedah, P lulus semua dan mendapat pingat … Terbaik ikut backtest: M.., M.., M.." + podium — [dashboard_v2.html:1311-1312](../../BacktestShariah2/standard/dashboard_v2.html#L1311). Lajur `#` = "kedudukan antara pemenang pingat" — [:1280](../../BacktestShariah2/standard/dashboard_v2.html#L1280), TIPS `kp_pingat` [:TIPS]. Ringkasan panel "Terbaik ikut backtest … Lihat tab Backtest" + podium yang sama — [:4359-4360](../../BacktestShariah2/standard/dashboard_v2.html#L4359).
- Butiran › Carta & gaya jalur "Tindakan seterusnya: Pantau dalam papertrade: M.., M.., M.. iaitu tiga kaedah dengan untung/entry tertinggi" — [:1387](../../BacktestShariah2/standard/dashboard_v2.html#L1387) — arahan terus daripada angka dalam sampel.
- Ambang langkah 6 = `sc.every(x=>x>0)`, langkah 7 = `v2.c>0` — [:1259-1260](../../BacktestShariah2/standard/dashboard_v2.html#L1259); Analisis memerlukan S1–S4 atasi EW ≥ 3/4 dan AUTOTUNE A01 CAGR > SPY dalam A dan B — [tugasan_v3.md:118-120](../../BacktestShariah2/standard/tugasan_v3.md#L118). Audit 24 Okt mengukur jurang: langkah 6 lulus 123 lawan Analisis 6; langkah 7 lulus 70 lawan Analisis 0 (68 daripada 70 di bawah SPY) — [tab_lain.md:103-104](../Audit%20dashboard%20tab%20demi%20tab/tab_lain.md).
- `papan.json` 6 Nov 2026: `lulus_at` benar bagi **0/134** M; `lulus ≥ 2` bagi **0/134**; status M: BELUM CUKUP 131, PERHATI 2, AMARAN 1 — [data/analisis/papan.json](../../BacktestShariah2/data/analisis/papan.json).
- `KAEDAH_TERBAIK.md` (dijana 6 Nov 2026 05:03 UTC): rho mentah backtest→realisasi **−0.566** (123 kaedah), separa kawal hari pegang **+0.145, p 0.110**; "pangkat backtest tidak mempunyai kuasa ramalan yang boleh diukur"; 59/74 terbukti negatif, 1 positif (`M82`) dengan amaran bias penapisan keluar; lulus S1–S4 6/228, WFO 22, AUTOTUNE 0, ≥ 2/3: 0 — [KAEDAH_TERBAIK.md:17-30](../../BacktestShariah2/laporan/KAEDAH_TERBAIK.md#L17), [:32-50](../../BacktestShariah2/laporan/KAEDAH_TERBAIK.md#L32), [:83-88](../../BacktestShariah2/laporan/KAEDAH_TERBAIK.md#L83). (Nota: CLAUDE.md memetik versi lama rho +0.16 p 0.105 dan 25 negatif / 0 positif; fail semasa berbeza.)
- Grep HTML: "kuasa ramalan" 0, "KAEDAH_TERBAIK" 0, "pangkat backtest" 0; "meramal" 8 padanan semuanya sektor/trend/stage/gred — [dashboard_v2.html:1637,3197,4108,4147,4843,4844,4936,4975](../../BacktestShariah2/standard/dashboard_v2.html#L1637).
- Satu-satunya kaveat: kaki "Hasil backtest, bukan jaminan · tiada wang sebenar" [:1324] dan TIPS `kaedah_terbaik` ("Kaedah terbaik ikut % untung", Prestasi) [:4848].
- Panel Lift v154 (tab Analisis) ialah satu-satunya paparan yang menyatakan "17 kaedah positif lawan SIFAR, 0 selepas hari beli dipadankan = arah pasaran, bukan kemahiran" dan "hari beli perlu (lift 2 mata) 56 lawan ada 14" — [dashboard_v2.html:4419-4422](../../BacktestShariah2/standard/dashboard_v2.html#L4419); manifes [dashboard_terbit.json](../../BacktestShariah2/data/dashboard_terbit.json) `nota`.

### Inferences
- Pemilik yang membuka Ringkasan atau Backtest masih mendapat jawapan "kaedah terbaik = pemenang pingat" — jawapan yang repo sendiri sudah ukur sebagai tiada kuasa ramalan. Panel podium di dua tempat ialah panel yang paling bercanggah dengan matlamat pemilik, bukan sekadar redundan.
- Dua set ambang untuk ujian luar sampel yang sama (> 0 lawan atasi penanda aras) bermakna 7 langkah saringan boleh meluluskan 44 kaedah (ukuran Okt) sementara Analisis meluluskan 0 pada ujian 2000 saham; `backtest` secara struktur **terlalu longgar** berbanding dokumen keputusan repo.

### Gaps
- Bilangan pemenang pingat semasa (44 pada 24 Okt) tidak dikira semula di sini kerana `kpM` memerlukan `autotune/a02_saringan` daripada db.

## Soalan 3: Nxx — adakah `kaedahn` mendedahkan keluar setiap kombinasi dan nombor pradaftar `jejak_semua.csv`?

### Takeaway
Ya: panel Produksi memaparkan kesemua 94 baris `jejak_semua.csv` dengan `keluar`, `keluar_aturan`, jangkaan latih/tahan, lift latih/tahan, n, menang, untung/rugi, tanpa5 dan p, serta KPI "Tanpa 5% POSITIF 7/94 · 6 memakai X13"; tetapi medan status `lejar` dalam dokumen yang sama sentiasa 0 kerana penjana mencari lajur `kaedah`/`id` sedangkan Lejar memakai `id_kaedah`.

### Cited Findings
- `jejak_semua.csv` 94 baris, lajur `pangkat, masuk, keluarga, keluar, peraturan, jangkaan_latih, lift_latih, n_latih, jangkaan_tahan, lift_tahan, n_tahan, menang, untung, rugi, asas_latih, asas_tahan, n_hari, t, p, s1_mutlak, s2_lift, s3_n, s123, s4_fdr, lulus, tanpa5_tahan`; taburan keluar X36 37 · X16 26 · X17 10 · X14 10 · X13 6 · X15 5; `tanpa5_tahan > 0` pada 7: N19X13 +4.262, N73X13 +2.311, N75X13 +1.752, N16X13 +1.222, N119X13 +1.176, N55X13 +1.115, N124X15 +0.396; jangkaan tahan tertinggi N124X15 +16.127, N19X13 +11.285 — [REVERSE/jejak_semua.csv](../../REVERSE/jejak_semua.csv) (dikira 6 Nov 2026). Sepadan dengan CLAUDE.md.
- Pemetaan ke db: `_produksi_n` → `baris[]` dengan `id=masuk+keluar, keluar, keluar_aturan(=peraturan), jangkaan, jangkaan_latih, lift, lift_latih, n, menang, untung, rugi, tanpa5, p`; `keluar` taburan; `tanpa5_positif`, `tanpa5_x13`; corong 7 tahap daripada `grid_penuh.csv` — [jana_db.py:509-548](../../BacktestShariah2/standard/jana_db.py#L509). Nama dan peraturan MASUK tidak diulang; dashboard mencarinya daripada registry `rows` ikut `masuk` [jana_db.py:502-508](../../BacktestShariah2/standard/jana_db.py#L502), [dashboard_v2.html:4604-4607](../../BacktestShariah2/standard/dashboard_v2.html#L4604).
- Jadual Produksi 11 lajur termasuk "Keluar — bila jual" (`r.keluar` + `keluar_aturan`) dan segmen tapis ikut keluar `knKeluar` — [dashboard_v2.html:4611-4630](../../BacktestShariah2/standard/dashboard_v2.html#L4611). KPI "Tanpa 5% POSITIF" `PR.tanpa5_positif/PR.bil` dan `PR.tanpa5_x13` — [:4626](../../BacktestShariah2/standard/dashboard_v2.html#L4626).
- FDR: lajur `p` dipapar; `s4_fdr`/`lulus` tidak dipapar setiap baris (kesemua 94 lulus mengikut takrif), hanya dalam corong "S4 BH-FDR q ≤ 0.05, penyebut m = 1,495" — [jana_db.py:530-535](../../BacktestShariah2/standard/jana_db.py#L530).
- **Pepijat status**: `_kira(pola, medan=('kaedah','id'))` mengambil `r['kaedah']` atau `r['id']`; Lejar `terbuka.csv`/`tunggu.csv` berlajur `id_kaedah` — [jana_db.py:474-482](../../BacktestShariah2/standard/jana_db.py#L474), pengepala [lejar/terbuka.csv:1](../../BacktestShariah2/lejar/terbuka.csv#L1). Replikasi tepat 6 Nov 2026: `posisi` = 3,419; `lejar` (medan kaedah/id) = **0**; dengan `id_kaedah` = **38,204**. `berjalan = bool(posisi or lejar_n)` tetap benar kerana `posisi` > 0, tetapi ayat `status` akan berbunyi "ada 3419 posisi Papertrade C dan **0 baris Lejar**" — [jana_db.py:521,549-552](../../BacktestShariah2/standard/jana_db.py#L549).
- Registry penuh 263 baris memaparkan `hasil` (lift/jangkaan/tanpa5) hanya bagi baris MASUK yang ada dalam `REVERSE/nxx.csv` (grid jarang 4 keluar asas), bukan daripada grid penuh — [jana_db.py:612-630](../../BacktestShariah2/standard/jana_db.py#L612).
- Nxx dalam `kaedah`: `test_nxx_tiada_registry_431` menetapkan Nxx tiada `kod/registry/<ID>.csv` — [ujian/test_katalog_kaedah.py:70](../../BacktestShariah2/ujian/test_katalog_kaedah.py#L70); `kod/registry/` 141 fail, 0 bermula `N`.

### Inferences
- Untuk Nxx, `kaedahn` Produksi ialah **satu-satunya** paparan nombor pradaftar dan ia lengkap; `kaedah` menambah hanya teks peraturan yang sama (nama masuk daripada registry) tanpa nombor — redundan bagi Nxx.
- Lajur `tanpa5` + "Untung / rugi" dalam Produksi ialah lajur yang paling dekat dengan kriteria pemilik "rugi kecil, untung besar", tetapi ia kajian 2012–2025 setiap dagangan; data hadapan Nxx (3,419 posisi C, 38,204 baris Lejar) hanya dalam Analisis dan semuanya BELUM CUKUP.

### Gaps
- Tidak disahkan sama ada panel Produksi dalam db hidup sudah dijana selepas imbasan 3 Nov (ayat status bergantung pada bila `tolak_db.md` terakhir dijalankan).

## Soalan 4: Kaedah replika (M02, M19, …, M100) dan penanda `FAIL ASAL` — adakah tab membezakan anggaran mekanikal daripada kaedah pakar asal?

### Takeaway
Tidak. Set `REPLIKA` 13 modul dan 66 kaedah dengan penanda `FAIL ASAL` dalam spec tidak dipaparkan di mana-mana: 0 padanan "replika"/"FAIL ASAL"/"mekanikal" dalam HTML dan dalam `katalog_kaedah.json`.

### Cited Findings
- `REPLIKA = {'M02','M19','M20','M26','M31','M38','M41','M47','M76','M78','M81','M82','M100'}` — [kod/dagangan.py:17](../../BacktestShariah2/kod/dagangan.py#L17).
- `FAIL ASAL` muncul 72 kali dalam `spec/SPEC_SEMUA_KAEDAH.md` (1,158,542 bait), di bawah 66 tajuk kaedah M berbeza (M04, M32–M41, M44–M52, M54–M57, …, M111, M114) — dikira 6 Nov 2026 daripada [spec/SPEC_SEMUA_KAEDAH.md](../../BacktestShariah2/spec/SPEC_SEMUA_KAEDAH.md).
- HTML: `FAIL ASAL` 0, `replika` 0, `anggaran mekanikal` 0 (grep). Katalog: 0 baris mengandungi `FAIL ASAL`/`replika`/`mekanikal`; 17 baris `pencipta` "Tidak dinyatakan" — [katalog_kaedah.json](../../BacktestShariah2/standard/katalog_kaedah.json). TIPS `kat_asal` hanya menerangkan "Tidak dinyatakan = sumber tidak menamakan pencipta" [dashboard_v2.html TIPS `kat_asal`].
- `KAEDAH_TERBAIK.md` §5: kaedah ialah "anggaran mekanikal … `spec` menanda `FAIL ASAL` … kegagalan bermakna versi mekanikal kami tidak berfungsi, bukan pakar itu salah" — [KAEDAH_TERBAIK.md:88-90](../../BacktestShariah2/laporan/KAEDAH_TERBAIK.md#L88).

### Inferences
- Lajur "Asal" memberi nama pencipta tetapi menyamakan kaedah yang spec asalnya terkunci (V1 "Spesifikasi dikunci") dengan kaedah yang spec asalnya tidak dapat ditentukan; bagi pemilik yang mahu mempercayai "sebab musabab pakar", pembezaan ini **HILANG** dan murah untuk ditambah (dua bendera boolean daripada `dagangan.REPLIKA` dan imbasan `FAIL ASAL`).

### Gaps
- Pengiraan 66 bergantung pada ungkapan tajuk `^#{1,3} M\d+`; spec mungkin menandakan `FAIL ASAL` dalam jadual ringkasan yang tidak berada di bawah tajuk kaedah (94 tajuk dikenal pasti daripada 134 kaedah).

## Soalan 5: Berapa banyak daripada 683 KB HTML / aset ialah kod kaedah atau teks spec yang pedagang tidak baca?

### Takeaway
HTML tidak membenamkan kod kaedah atau spec (0 blok base64, 0 `FAIL ASAL`); 580,626 bait (85%) ialah skrip, 99,226 bait CSS, 57,375 bait kamus TIPS, dan kod render tiga tab ini 78,611 bait (11.5%). Kod kaedah hidup sebagai aset berasingan (salinan `kod/`, ~2.09 MB, 388 fail) dan teks peraturan sebagai dokumen db `kaedah/katalog` 155,282 bait (69,776 bait teks masuk/keluar/pegang/henti).

### Cited Findings
- Pecahan HTML (dikira 6 Nov 2026): total 683,519 bait, 5,352 baris; `<style>` 99,226; satu `<script>` 580,626; `const TIPS` 57,375; `renderKeputusan` 5,323 · `renderRingkasan` 5,298 · `renderPapan` 3,061 · `renderBanding` 3,729 · `renderKaedah` 7,494 · AUTOTUNE (4 fungsi) 18,423 · `renderKaedahN` 35,283; `data:…;base64` 0; "FAIL ASAL" 0 — [dashboard_v2.html](../../BacktestShariah2/standard/dashboard_v2.html).
- Aset kod dashboard = salinan `kod/` (id `4663135cc115bb60b40a6d93983f1456`, 185 fail pada 14 Okt 2026) — [kod/README.md:3-4](../../BacktestShariah2/kod/README.md#L3); `du -sb kod/` 2,088,647 bait (388 fail termasuk `registry/` 141 CSV); `kod/kaedah/M*.py` 424,874 bait, `N*.py` 167,303 bait, 0 fail `GB*.py` (walaupun `POLA` ujian masih `('M*.py','N*.py','GB*.py')` [test_katalog_kaedah.py:7](../../BacktestShariah2/ujian/test_katalog_kaedah.py#L7)).
- `kaedah/katalog`: fail sumber 155,282 bait; audit Okt mengukur dokumen db 149.8 KiB — [audit_posisi_hingga_sektor.md:274](../Audit%20dan%20reka%20semula%20dashboard/audit_posisi_hingga_sektor.md). `registry` ~2.0 MB (termasuk 32 dokumen I ~0.31 MB) + `autotune` ~0.24 MB dilanggan pada setiap buka — [tab_lain.md:114](../Audit%20dashboard%20tab%20demi%20tab/tab_lain.md); langganan [dashboard_v2.html:5214,5349](../../BacktestShariah2/standard/dashboard_v2.html#L5214).
- `kaedah_n/papan` 234,697 bait (89.5% had), bertambah ~892 bait setiap baris registry — [jana_db.py:1172-1177](../../BacktestShariah2/standard/jana_db.py#L1172).

### Inferences
- Beban yang pedagang tidak baca bukan dalam HTML tetapi dalam muatan db: ~2.2 MB `registry`+`autotune` dimuat walaupun pemilik hanya membuka Posisi; `kaedahn` 35 KB kod + 235 KB dokumen untuk 13 panel rekod kajian yang kebanyakannya statik.

### Gaps
- Saiz aset kod dashboard semasa (selepas 14 Okt) tidak boleh dibaca tanpa `Artifact list scope assets`; angka 2.09 MB ialah folder repo (had atas termasuk `__pycache__`).

## Soalan 6: Saranan audit v102/v103 (`Audit dashboard tab demi tab`, `Audit dan reka semula dashboard`) — mana yang dilaksanakan menjelang v154?

### Takeaway
Daripada 14 saranan audit 24 Okt bagi Backtest dan Kaedah, 3 dilaksanakan (ujian unit penyegerakan katalog, label U×S diganti pil Analisis, segmen keluarga M/N), 1 separa (Kaedah tab "Sama untuk semua" diperluas bagi Nxx), dan 10 tidak (podium, langkah 6–7, Papertrade C dalam Backtest, muat registry atas permintaan, KPI "Terbaik gaya anda", AUTOTUNE pindah, label "Langsung", pil M31, ayat pegang M117, gabung ke Profil kaedah).

### Cited Findings
- Jadual saranan asal — [tab_lain.md:131-158](../Audit%20dashboard%20tab%20demi%20tab/tab_lain.md); laporan awal mencadangkan Backtest → "Lagi", Kaedah → "Profil" — [tab_lain.md:128](../Audit%20dashboard%20tab%20demi%20tab/tab_lain.md); "Bersarakan sebagai alat pemilihan … podium backtest di Ringkasan" — [logik_keputusan_metrik.md:115](../Audit%20dan%20reka%20semula%20dashboard/logik_keputusan_metrik.md).
- TIDAK dilaksanakan: podium masih di [dashboard_v2.html:1311-1312](../../BacktestShariah2/standard/dashboard_v2.html#L1311) dan [:4359](../../BacktestShariah2/standard/dashboard_v2.html#L4359); `LANGKAH` 6–7 masih ambang `> 0` [:1244-1245,1259-1260](../../BacktestShariah2/standard/dashboard_v2.html#L1244); lajur Papertrade C `kp_pt` masih `prStats` [:1289](../../BacktestShariah2/standard/dashboard_v2.html#L1289); `registry` masih dilanggan pada muat [:5214](../../BacktestShariah2/standard/dashboard_v2.html#L5214); "Terbaik gaya anda" masih `bestBy` atas semua varian [:1356](../../BacktestShariah2/standard/dashboard_v2.html#L1356); AUTOTUNE 4 versi masih dalam Backtest set 2000 [:2389,2475](../../BacktestShariah2/standard/dashboard_v2.html#L2389); label "Langsung · ujian terkini" [:5217](../../BacktestShariah2/standard/dashboard_v2.html#L5217); teks henti M31 masih bermula "Tiada henti harga; henti tutup di bawah band bawah…" (regex `/^tiada henti/` → pil "⚠ Tiada henti") — [katalog_kaedah.json M31], [dashboard_v2.html:2235](../../BacktestShariah2/standard/dashboard_v2.html#L2235); M117 masih "pegang sehingga isyarat keluar atau henti" dengan keluar "Tiada; hanya henti/had masa" — [katalog_kaedah.json M117]; 8 tab masih berasingan (tiada "Profil kaedah").
- DILAKSANAKAN: `test_katalog_kaedah.py` 6 ujian (`test_semua_modul_ada`, `test_medan_lengkap_dan_unik`, `test_nama_sama_dengan_kod`, `test_varian_kod_ada_dalam_registry`, `test_nxx_tiada_registry_431`, `test_saiz_dokumen_db`) — [ujian/test_katalog_kaedah.py:29-79](../../BacktestShariah2/ujian/test_katalog_kaedah.py#L29); pil Papertrade C kini `kdPill` = status Papan Penganalisis (TIPS `kat_pt`: "Pil status … datang daripada Papan Penganalisis") — [dashboard_v2.html:1944-1945,2253](../../BacktestShariah2/standard/dashboard_v2.html#L1944); segmen Semua / Kaedah M / Kombinasi N (v132) — [dashboard.md:3 (d)](../../BacktestShariah2/standard/dashboard.md#L3), [dashboard_v2.html:2294](../../BacktestShariah2/standard/dashboard_v2.html#L2294).
- Sejarah versi tidak boleh dijejak dari git: klon cetek 56 komit; hanya 2 komit menyentuh `dashboard_v2.html` (372db4a v154, 2ed7a27); komit 372db4a merekod v151–v153 "dikomit pada cawangan, tidak digabung" — `git show 372db4a`. `dashboard.md` masih menyatakan "Versi semasa = versi 132" — [dashboard.md:3](../../BacktestShariah2/standard/dashboard.md#L3) lawan manifes v154 nombor 185 [dashboard_terbit.json](../../BacktestShariah2/data/dashboard_terbit.json).

### Inferences
- Saranan yang dilaksanakan ialah yang bersifat "betulkan data"; saranan "buang/gabung panel" tiada satu pun dilaksanakan — struktur tiga tab kekal sama seperti v103 dan bertambah satu tab (Kombinasi N).

### Gaps
- Tanpa log versi v133–v153 dalam repo, perubahan antara v132 dan v154 bagi tiga tab ini tidak dapat diasingkan (binaan_v2_log hanya sampai v92; dashboard.md berhenti pada v132).

## Soalan 7: Apa yang `dashboard.md` dan `tugasan_v3.md` WAJIBKAN tab ini tunjukkan?

### Takeaway
Hanya `dashboard.md` (jadual Struktur tab) menetapkan kandungan tiga tab ini; `tugasan_v3.md` tidak mewajibkan tab Backtest/Kaedah/Kombinasi N langsung — ia hanya mewajibkan URL artifact, dokumen papertrade, tab Analisis (`analisis/papan`) dan formula skor Analisis, dan merekod keputusan pengguna "Ujian luar sampel backtest: tidak dibuat".

### Cited Findings
- Backtest wajib: Keputusan (7 langkah + pingat varian `varian_kod`), Butiran (papan penuh, carta & gaya, banding, set 431/S1–S4/2000) — [dashboard.md:17](../../BacktestShariah2/standard/dashboard.md#L17). Kombinasi N wajib: Produksi 94 "yang diimbas setiap malam", penarikan balik m=8, rekod kajian (E1–E6, kad skor 413, empat pradaftar, portfolio, cara, silang, keluar, registry 263, semua ujian) — [dashboard.md:18](../../BacktestShariah2/standard/dashboard.md#L18). Kaedah wajib: katalog (nama, asal, masuk/keluar/pegang/henti, Backtest istilah sama, Papertrade C) — [dashboard.md:19](../../BacktestShariah2/standard/dashboard.md#L19).
- Percanggahan dalaman: baris 18 "diimbas setiap malam" lawan pengepala baris 3 "belum diimbas, kerana `main` tiada modulnya" — [dashboard.md:3,18](../../BacktestShariah2/standard/dashboard.md#L3).
- Peraturan paparan umum: semua jadual boleh susun kecuali Banding; setiap istilah ada tooltip TIPS; telefon 10 baris +25; "Papertrade C sahaja" — [dashboard.md:31-39](../../BacktestShariah2/standard/dashboard.md#L31).
- `tugasan_v3.md`: dashboard URL + dokumen db [tugasan_v3.md:70](../../BacktestShariah2/standard/tugasan_v3.md#L70); "Ujian luar sampel backtest: tidak dibuat (keputusan pengguna 14 Okt 2026)" [:83](../../BacktestShariah2/standard/tugasan_v3.md#L83); Analisis skor + ambang semakan luar sampel [:116-128](../../BacktestShariah2/standard/tugasan_v3.md#L116). Grep "tab Backtest|tab Kaedah|katalog" → 0 padanan.

### Inferences
- Tiada peraturan pengguna yang menghalang penggabungan atau penurunan tiga tab ini; satu-satunya kekangan ialah `dashboard.md`, dokumen yang disunting bersama HTML. Sebarang penyusunan semula perlu mengemas kini baris 17–19 dan pengepala versi.

### Gaps
- Keputusan pengguna lisan di luar dokumen (cth. permintaan nama "Kombinasi N" 2 Nov) hanya direkod dalam `dashboard.md:3`; mungkin ada keputusan lain dalam log sesi yang tidak disemak.

## Soalan 8: Muat lebar telefon (pemilik guna telefon dan desktop sama rata)

### Takeaway
Pada ≤ 760px semua jadual bertukar kepada grid kad 2 lajur dengan label daripada tajuk; hanya `keputusan` (LP_KP), `katalog` (LP_KAT) dan `lift` memakai mod baris-lipat satu garis, manakala Papan 22 lajur, Produksi 11 lajur, Semua ujian 16 lajur, AUTOTUNE 12 lajur dan 9 jadual statik `kn-*` memaparkan setiap sel bertindan — kelas keutamaan `kp-lo`/`kp-hi` pada tajuk Kombinasi N tiada takrif CSS, jadi ia tidak menyembunyikan apa-apa.

### Cited Findings
- `TELEFON = matchMedia('(max-width:760px)')` [dashboard_v2.html:1127](../../BacktestShariah2/standard/dashboard_v2.html#L1127); had baris telefon `AWAL`=10 (+25) — [dashboard.md:37](../../BacktestShariah2/standard/dashboard.md#L37).
- CSS `@media (max-width:760px)`: `.tablewrap tbody tr{display:grid;grid-template-columns:1fr 1fr}`, `td::before{content:attr(data-label)}`, `td.name/.wrap` merentang 2 lajur — [dashboard_v2.html:≈300-314 (blok `.tablewrap{border:0;…}`)](../../BacktestShariah2/standard/dashboard_v2.html); `data-label` diisi `topScrolls()` bagi SEMUA `.tablewrap` termasuk jadual statik — [:4378-4383](../../BacktestShariah2/standard/dashboard_v2.html#L4378).
- Mod lipat `lp` (`.tw-lp`, `.mline`/`.mkad`) hanya pada `sortTable({id:'keputusan',lp:LP_KP})` [:1319](../../BacktestShariah2/standard/dashboard_v2.html#L1319), `katalog` `lp:LP_KAT` [:2296](../../BacktestShariah2/standard/dashboard_v2.html#L2296), `papan` lp [:1446](../../BacktestShariah2/standard/dashboard_v2.html#L1446), `autotune*` lp [:2377,2430,2465], `lift` [:4428]; TIADA `lp` pada `gaya`, `top5`, `kaedahn`, `knprod`, `knujian` — senarai `sortTable({id:…})` dikira 6 Nov.
- `kp-lo` 14 kejadian dan `kp-hi` 11 kejadian dalam fail, **0** dalam `<style>` — kelas mati (dikira 6 Nov 2026).
- Jadual statik 9 buah `data-st="kn-cara|kn-diambil|kn-gate|kn-giliran|kn-keluar|kn-port|kn-silang|kn-skor|kn-t4"` (4–11 lajur) tanpa `sortTable`, tanpa had baris; `kn-giliran` memakai `colspan="10"` baris kedua [:4677](../../BacktestShariah2/standard/dashboard_v2.html#L4677).
- Nav telefon `PNAV_KUMP['v-kaedahn']` 3 kumpulan: "Produksi · yang membeli", "Rekod kajian · bukan isyarat", "Rujukan" — [:5079-5081](../../BacktestShariah2/standard/dashboard_v2.html#L5079); tiada kumpulan untuk `v-kaedah` atau `v-keputusan`.
- Jadual Banding "metrik ikut baris, tajuk tidak disusun" — [:1531](../../BacktestShariah2/standard/dashboard_v2.html#L1531); pada telefon ia grid 2 lajur dengan 4 sel (Metrik + 3 varian) setiap baris × 26 baris.

### Inferences
- Pada telefon, Backtest › Keputusan dan Kaedah (mod ringkas) boleh dibaca satu baris setiap kaedah; Kombinasi N Produksi (11 sel × 10 baris) dan Semua ujian (16 sel) menjadi ~110–160 sel bertindan setiap skrin — paling berat antara ketiga-tiga tab, dan ia tab yang memegang satu-satunya nombor Nxx yang berguna.
- Kelas `kp-lo/kp-hi` menunjukkan niat menyembunyikan lajur keutamaan rendah di telefon yang tidak pernah disiapkan.

### Gaps
- Tiada tangkapan skrin/ujian Playwright 390px dijalankan dalam audit ini; `ujian/semak_dashboard.js` hanya mengaudit jadual Posisi — [dashboard.md:4](../../BacktestShariah2/standard/dashboard.md#L4).

## Soalan 9 (sintesis): Penilaian setiap panel terhadap matlamat "SATU kaedah untuk wang sebenar"

### Takeaway
Tiada satu pun daripada 7 pandangan / ~30 panel dalam tiga tab ini MEMUTUSKAN kaedah pada ukuran yang repo sendiri sahkan (hadapan, tanda-ke-pasaran, padan hari beli, Mxx+Nxx satu paksi) — itu hanya ada dalam panel Lift (Analisis v154) yang kini melaporkan 0 kaedah bertahan BH-FDR daripada 180. Tiga tab ini MENGKATALOG; panel yang berpura-pura memutuskan (podium, pingat, "Tindakan seterusnya", "Terbaik gaya anda") memutuskan atas angka yang diukur tiada kuasa ramalan.

### Cited Findings (jadual penilaian; rujukan baris di S1–S8)
| Tab › Panel | Soalan yang dijawab | Memutuskan? | Status |
|---|---|---|---|
| Backtest › Keputusan › headline + podium + RM10k | "varian mana skor enjin tertinggi" | Tidak (dalam sampel, tiada ramalan — S2) | REDUNDAN dengan Ringkasan podium; bercanggah matlamat |
| Backtest › Keputusan › corong 7 langkah + pingat | "berapa lulus gate enjin + S1–S4>0 + A02>0" | Tidak (ambang > 0 lawan Analisis atasi EW/SPY) | REDUNDAN dengan Analisis `lulus`/`kekal`, takrif lebih longgar |
| Backtest › Keputusan › jadual 10 lajur | angka 431 + Ujian 2 + Papertrade kasar | Tidak | REDUNDAN (Analisis `bt_*`, Kaedah `selBt`) |
| Backtest › Keputusan › lajur Papertrade C (`prStats`) | purata kasar C | Tidak (campur terbuka/tertutup; Analisis ada `h_purata` matang) | REDUNDAN |
| Backtest › Butiran › Papan penuh 22 lajur + `I` | metrik mentah 665 varian | Tidak | MATI bagi operasi; penapis `Indikator I` MATI (0 baris) |
| Backtest › Butiran › Carta & gaya | KPI "Terbaik gaya anda", "Tindakan seterusnya" | Berpura-pura (menobatkan varian DITOLAK) | MATI/mengelirukan |
| Backtest › Butiran › Banding | banding ≤ 3 varian | Tidak (pilihan varian, bukan kaedah) | RUJUKAN penyelidikan |
| Backtest › 2000 AUTOTUNE 4 versi | A01/A02/A03/saringan 2013–2018 | Tidak (Analisis sudah ringkaskan `lulus_at`) | REDUNDAN; A02/A03/sar MATI |
| Kaedah › headline + 5 KPI teks | bilangan baris, "Buka esok", "Dua lorong" | Tidak | MATI (teks tetap; ayat "belum" hanyut) |
| Kaedah › jadual masuk/keluar/pegang/henti | "bagaimana kaedah ini beli/jual" | Tidak, tetapi prasyarat berdagang | PENTING (satu-satunya tempat) |
| Kaedah › lajur Backtest (set 431) | sama seperti Keputusan | Tidak | REDUNDAN |
| Kaedah › lajur Papertrade C | purata kasar + pil Analisis | Separa (pil status) | REDUNDAN dengan Analisis |
| Kaedah › helaian `openKaedah` | profil penuh satu kaedah (peraturan+C+backtest) | Separa | PENTING (titik gabung tunggal), tetapi tiada bendera replika/`FAIL ASAL` → HILANG |
| Kombinasi N › Produksi (status, corong, jadual 94) | kombinasi mana lulus 4 syarat; keluar, tanpa5, p | Separa (kajian setiap dagangan; 7/94 tanpa5>0) | PENTING (satu-satunya nombor Nxx); medan `lejar` 0 = pepijat |
| Kombinasi N › Penarikan balik, Keputusan akhir, Baris gilir, Kad skor, Empat pradaftar, Portfolio, Cara, Silang, Keluar, Semua ujian, Nota (11 panel) | rekod kajian REVERSE | Tidak ("Rekod kajian sahaja; bukan isyarat beli") | RUJUKAN/MATI bagi pemilihan; 35 KB kod |
| Kombinasi N › Registry penuh 263 | katalog peraturan N + status PERLU | Tidak | RUJUKAN |
| (Analisis) Lift v154 | Mxx+Nxx hadapan, padan hari beli | YA (satu-satunya) | PENTING; bukan dalam tiga tab ini |
| HILANG dalam tiga tab | satu paparan setiap kaedah: lift hadapan + taburan rugi/untung (untung purata, rugi purata, tanpa5 hadapan) + bendera replika/`FAIL ASAL` + "cukup data pada <tarikh>" | — | HILANG |

### Inferences
- Jawapan kepada "mengapa tiga tab": kerana setiap populasi mendapat tab apabila ia lahir, dan audit yang menyarankan penggabungan tidak dilaksanakan. Kandungan yang pemilik perlukan daripada ketiga-tiganya ialah (i) teks peraturan (Kaedah) dan (ii) jadual Produksi Nxx (Kombinasi N); selebihnya pendua Analisis atau rekod kajian.
- Panel yang paling merbahaya kepada matlamat pemilik ialah dua podium "Terbaik ikut backtest" dan jalur "Tindakan seterusnya", kerana ia satu-satunya tempat dashboard mengeluarkan arahan ("Pantau M.., M.., M..") dan ia berasaskan ukuran yang `KAEDAH_TERBAIK.md` tolak.

### Gaps
- Penilaian "MATI" adalah berdasarkan kandungan dan kebergantungan keputusan, bukan telemetri penggunaan.
- Tidak disemak sama ada `meta/info` (penanda aras EW/SPY/QQQ bagi set 431) masih sepadan dengan registry semasa kerana tiada penulis dalam repo.
