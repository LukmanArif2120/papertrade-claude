# Tolak db dashboard harian (sesi Claude BAHARU setiap kali; aktif sejak peralihan 27 Okt 2026, lihat `PERALIHAN.md`)

Masa: 10:20 pagi New York, Isnin–Sabtu (= 10:20 atau 11:20 malam MYT), iaitu selepas belian 9:35 NY.
Model `claude-sonnet-5-5`. Automatik; jangan tanya soalan. Tiada order Moomoo, tiada wang sebenar.
Semua pengiraan dibuat oleh GitHub Actions (`standard/harian_c.py`, `.github/workflows/harian.yml` dan `beli.yml`).
Sesi ini hanya (1) memastikan Actions sudah berjalan dan (2) menolak fail yang sudah dijana ke db dashboard.
Jangan baca fail CSV besar dan jangan bina JSON dengan tangan; guna skrip.

Alat (satu panggilan ToolSearch): `select:ArtifactData,Artifact,mcp__github__actions_list,mcp__github__actions_run_trigger`
Notifikasi (keputusan pengguna 27 Okt 2026): ntfy SAHAJA (ringkasan belian dihantar oleh `beli.yml`); JANGAN guna PushNotification.
Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e

Semakan kedua: `tolak_db_semak.md` (12:20 NY, trig_013bee461xNS3Z5meBZQ9zTh) menyemak hasil
tugasan ini dua jam kemudian dan menolak SEMULA hanya jika db tidak segar atau tidak lengkap.
Kalau tugasan ini gagal senyap, itulah satu-satunya perkara yang akan menangkapnya.

1. `git pull --rebase origin main`, kemudian `python3 -m pip install -q -r requirements.txt` (pip MESTI melalui
   `python3 -m pip`: pada 6 Nov 2026 `pip` memasang ke Python 3.13 sementara `python3` ialah 3.11 tanpa numpy).
2. `python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db0` dan baca medan `pengawas` dalam output.
   Jika `tembak` mengandungi `harian.yml` atau `beli.yml`: semak larian terakhir workflow itu (`mcp__github__actions_list`,
   method `list_workflow_runs`, owner `pedagangsenja`, repo `papertrade-claude`, resource_id nama workflow, perPage 1).
   Jika tiada larian `queued`/`in_progress`, tembak sekali (`mcp__github__actions_run_trigger`, method `run_workflow`,
   workflow_id nama workflow, ref `main`). Jangan tunggu; teruskan dengan data sedia ada dan catat dalam notifikasi.
3. **Versi dokumen db = DAFTAR, bukan senarai** (sejak 6 Nov 2026). `ArtifactData` kini MENOLAK `list`/`get`
   dengan `out_dir` bagi dokumen yang "mungkin ditulis orang lain", dan tanpa `out_dir` 36 MB kandungan masuk ke
   perbualan — itulah sebab tolakan gagal 4–6 Nov 2026. JANGAN guna `list` atau `out_dir` lagi.
   `ArtifactData` `get`, koleksi `meta`, doc_id `versi_db` (TANPA out_dir; ~3 KB). Hasilnya ada medan `data.versi`
   (peta {"koleksi/doc": versi}) dan `version` (versi dokumen `meta/versi_db` itu sendiri — ingat nombor ini untuk
   langkah 5c). Tulis `data` ke `<scratchpad>/versi.json` dengan Write (salin tepat; jangan ubah nombor).
   Kenapa ia betul: setiap tulisan menaikkan versi tepat 1 dan hanya paip ini menulis dokumen ini, jadi
   `jana_db.py` boleh MENGIRA versi selepas tolakan (`versi_selepas.json`, langkah 5c).
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
   ada `file_path` dan `if_version`). **Ditolak kerana versi** (`version_mismatch`): ralat menamakan SATU dokumen
   dan versinya sekarang ("writes[i] … "koleksi/doc" … is now at version N") — tukar `if_version` entri itu kepada N
   dalam `writes` dan hantar semula batch YANG SAMA (ia atomik: tiada apa ditulis). Jika ralat berkata "the server
   named no current version", dokumen itu tiada: buang `if_version` entri itu. Ulang sehingga batch diterima
   (maks 10 kali setiap batch). Catat setiap pembetulan (koleksi/doc, versi sebenar) untuk langkah 5c.
   **URUTAN WAJIB: batch_0, batch_1, … mengikut nombor, dan urutan entri dalam setiap fail jangan diubah.**
   `ringkas_c` ialah berpuluh dokumen (27 / 5.3 MB pada 6 Nov 2026, bertambah setiap hari) — ia TIDAK muat satu batch, jadi `jana_db.py` meletakkan
   dokumen asasnya (yang membawa `induk`) pada entri TERAKHIR. Halaman tidak merender sehingga
   setiap bahagian sepadan dengan induk asas, jadi dengan urutan ini halaman kekal memapar set
   LAMA yang lengkap sepanjang tolakan. Tolak asas lebih awal dan tab Posisi memapar "Belum ada
   posisi dalam pangkalan data" selama beberapa minit (berlaku 3 Nov 2026: 1,641 posisi Nxx).
5b. **Sahkan penghimpunan** = SETIAP batch_N.json berakhir dengan "Database batch committed". Batch
   atomik, dan asas setiap kumpulan ditolak terakhir (langkah 5), jadi jika batch terakhir sesuatu kumpulan
   diterima, setiap bahagiannya sudah ditulis. (Semakan lama membaca asas + bahagian dengan `out_dir`;
   itu kini ditolak — lihat langkah 3.) Mana-mana batch TIDAK diterima selepas 10 cubaan → cetus amaran
   (langkah 6) "tolak db separa: batch_N"; JANGAN laporkan berjaya, dan JANGAN laksana langkah 5c.
5c. **Kemas daftar versi** (hanya jika SEMUA batch diterima). `<scratchpad>/db/versi_selepas.json` ialah
   daftar baharu yang dikira `jana_db.py` (pin + 1; dokumen baharu = 1). Jika langkah 5 membetulkan mana-mana
   pin, kemas entri itu dalam fail = (versi sebenar + 1) dengan Edit. Kemudian `ArtifactData` `set`, koleksi
   `meta`, doc_id `versi_db`, `file_path` fail itu, `if_version` = versi `meta/versi_db` daripada langkah 3.
   Daftar yang salah tidak merosakkan data — langkah 5 esok membetulkannya — tetapi ia melambatkan tolakan.
6. Amaran (hanya jika langkah 2–5b gagal atau db tidak ditolak): `mcp__github__actions_run_trigger` (method `run_workflow`,
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
