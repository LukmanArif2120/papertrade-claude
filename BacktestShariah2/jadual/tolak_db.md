# Tolak db dashboard harian (sesi Claude BAHARU setiap kali; aktif sejak peralihan 27 Okt 2026, lihat `PERALIHAN.md`)

Masa: 10:20 pagi New York, Isnin–Sabtu (= 10:20 atau 11:20 malam MYT), iaitu selepas belian 9:35 NY.
Model `claude-sonnet-5-5`. Automatik; jangan tanya soalan. Tiada order Moomoo, tiada wang sebenar.
Semua pengiraan dibuat oleh GitHub Actions (`standard/harian_c.py`, `.github/workflows/harian.yml` dan `beli.yml`).
Sesi ini hanya (1) memastikan Actions sudah berjalan dan (2) menolak fail yang sudah dijana ke db dashboard.
Jangan baca fail CSV besar dan jangan bina JSON dengan tangan; guna skrip.

Alat (satu panggilan ToolSearch): `select:ArtifactData,Artifact,mcp__github__actions_list,mcp__github__actions_run_trigger`
Notifikasi (keputusan pengguna 27 Okt 2026): ntfy SAHAJA (ringkasan belian dihantar oleh `beli.yml`); JANGAN guna PushNotification.
Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e

1. `git pull --rebase origin main`.
2. `python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db0` dan baca medan `pengawas` dalam output.
   Jika `tembak` mengandungi `harian.yml` atau `beli.yml`: semak larian terakhir workflow itu (`mcp__github__actions_list`,
   method `list_workflow_runs`, owner `pedagangsenja`, repo `papertrade-claude`, resource_id nama workflow, perPage 1).
   Jika tiada larian `queued`/`in_progress`, tembak sekali (`mcp__github__actions_run_trigger`, method `run_workflow`,
   workflow_id nama workflow, ref `main`). Jangan tunggu; teruskan dengan data sedia ada dan catat dalam notifikasi.
3. Versi dokumen db: `ArtifactData` `list` bagi koleksi `papertrade` (query.limit 100; ulang dengan next_cursor),
   `prestasi`, `harian`, `sektor`, `analisis` dan `posisi`, dengan `out_dir` <scratchpad>/lama (kandungan tidak perlu dibaca).
   Tulis `<scratchpad>/versi.json` = {"papertrade/claude": versi, …} untuk SEMUA dokumen yang disenaraikan.
4. `python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db --versi <scratchpad>/versi.json`
   (`pecah_claude.py` dijalankan oleh Actions; `bahagi_db` **tidak** — ia diimport DALAM PROSES
   oleh `jana_db.py`, yang memecah sendiri setiap dokumen dalam `jana_db.PECAH`. Tiada workflow
   pernah menjalankan `bahagi_db.py` sebagai CLI. Skrip gagal jika mana-mana dokumen melebihi had
   262,144 bait; jika itu berlaku, dokumen itu perlu DITAMBAH ke `jana_db.PECAH` **dan** pembacanya
   dalam `dashboard_v2.html` ditukar kepada `subBhg` — itu perubahan kod, bukan sesuatu yang sesi ini
   boleh buat. Hentikan pada langkah 6 dan laporkan nama dokumen itu.)
   Nota: kegagalan had berlaku SEBELUM medan `pengawas` dihasilkan, jadi langkah 2 juga tidak dapat
   dipenuhi — jangan anggap `harian.yml`/`beli.yml` tidak perlu ditembak; nyatakan ia tidak diketahui.
5. Bagi setiap fail `batch_N.json` yang dicetak: `ArtifactData` `batch`, `writes` = kandungan fail itu (setiap entri sudah
   ada `file_path` dan `if_version`). Ditolak kerana versi berubah → ulang langkah 3–5 sekali.
6. Amaran (hanya jika langkah 2–5 gagal atau db tidak ditolak): `mcp__github__actions_run_trigger` (method `run_workflow`,
   owner `pedagangsenja`, repo `papertrade-claude`, workflow_id `amaran_ntfy.yml`, ref `main`, inputs
   {"tajuk": "tolak db gagal", "mesej": "<tarikh>: <sebab ringkas, < 200 aksara>"}). Berjaya → tiada notifikasi.
7. **Dashboard hidup lawan repo** (satu-satunya tempat semakan ini boleh dibuat: GitHub Actions
   tidak dapat membaca artifact kerana `/api/artifacts/...` dilindungi cabaran Cloudflare).
   `Artifact` `read`, `url` dashboard. Baris pertama hasilnya menyatakan version id, contohnya
   `(version 1793412015-9909)` — ambil id itu. (`Artifact` `list` TIDAK memadai: ia hanya memberi
   tajuk, pautan dan tarikh dikemas, tanpa version id.) Bacaan ini tidak perlu dibaca sepenuhnya
   kerana sesi ini tidak menerbit apa-apa; hanya baris pertama diperlukan.
   Banding dengan medan `versi_artifact` dalam `BacktestShariah2/data/dashboard_terbit.json`.
   - Sama → tiada tindakan.
   - BERBEZA → artifact diterbitkan tanpa dikomit (ini berlaku dua kali pada 30–31 Okt 2026:
     v132–v138, kemudian v139). JANGAN terbit apa-apa dan JANGAN tulis ganti. Cetus amaran
     `amaran_ntfy.yml` dengan mesej `dashboard hidup <versi> != repo <versi>; perlu gabung`,
     dan catat dalam notifikasi. Penggabungan dibuat oleh sesi kerja bersama pengguna, bukan di sini.
Tiada commit diperlukan (sesi ini tidak mengubah fail repo).
