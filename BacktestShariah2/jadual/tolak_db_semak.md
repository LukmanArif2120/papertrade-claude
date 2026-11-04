# Semak tolakan db (sesi Claude BAHARU; sejak 4 Nov 2026)

Masa: 12:20 tengah hari New York, Isnin–Sabtu — **dua jam selepas** `tolak_db.md` (10:20 NY).
Model `claude-sonnet-5-5`. Automatik; jangan tanya soalan. Tiada order Moomoo, tiada wang sebenar.

**Kenapa ia wujud.** Tolakan db ialah **titik kegagalan tunggal**: satu larian sehari, ia sesi LLM
(bukan workflow), dan GitHub Actions **tidak boleh menyemaknya** kerana `/api/artifacts/...`
dilindungi cabaran Cloudflare. Kalau larian 10:20 gagal, tidak pernah bermula, atau berhenti
di tengah jalan, dashboard basi 24 jam dan tiada apa-apa dalam sistem yang tahu. Sesi ini ialah
satu-satunya semakan kedua.

**Ia MENYEMAK dahulu, menolak kemudian.** Kalau tolakan 10:20 berjaya — kes biasa — sesi ini
tidak menolak apa-apa, tidak menghantar notifikasi, dan tamat dalam beberapa minit. Sesi yang
menolak semula setiap hari hanya menggandakan beban dan menyembunyikan kegagalan sebenar.

Alat (satu panggilan ToolSearch): `select:ArtifactData,mcp__github__actions_run_trigger`
Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e — jangan cipta artifact baharu.
Notifikasi: ntfy SAHAJA (`amaran_ntfy.yml`), dan **hanya** apabila sesuatu dipulihkan atau gagal.

---

1. `git checkout main && git pull --rebase origin main`.

2. `python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db0`
   (tanpa `--versi`; ini hanya untuk MEMBANDING, bukan menolak).
   Baca `<scratchpad>/db0/ringkas.json` → simpan senarai `kumpulan_terpecah`.

3. Baca keadaan HIDUP tanpa memuatkan kandungan ke dalam perbualan:
   `ArtifactData` `list` bagi koleksi `harian`, `papertrade`, `analisis`, `posisi`, `prestasi`
   (query.limit 100; ulang dengan next_cursor) dengan `out_dir` `<scratchpad>/hidup`.
   Kalau `out_dir` ditolak bagi sesuatu koleksi, guna `get` bagi dokumen yang diperlukan sahaja.

4. **Semakan A — kesegaran.** Banding `<scratchpad>/hidup/harian/status.json` dengan
   `<scratchpad>/db0/harian/status.json` pada tiga medan: `harga_tutup_pada`, `tarikh_data`,
   `beli_pada`. Ketiga-tiganya sama → db segar.

5. **Semakan B — penghimpunan.** Bagi setiap nama dalam `kumpulan_terpecah` (langkah 2) dan
   setiap dokumen dalam `jana_db.PECAH`, banding `bahagian.id` dokumen asas HIDUP dengan
   `induk` bahagian bernombor TERTINGGI yang hidup. Sama → lengkap.
   (Sah kerana `jana_db.batchkan` menolak dokumen asas TERAKHIR dalam kumpulan yang tidak muat
   satu batch: kalau induk asas sudah baharu, setiap bahagiannya sudah ditulis sebelum itu.)

6. **Kedua-dua semakan lulus** → tamat. Tiada tolakan, tiada notifikasi, tiada commit.
   Balas satu baris: `db segar (sesi <tarikh>), 0 tindakan`.

7. **Mana-mana semakan gagal** → jalankan `BacktestShariah2/jadual/tolak_db.md` langkah 3–5b
   sepenuhnya (versi dokumen → `jana_db.py --versi` → `ArtifactData batch` mengikut urutan
   `batch_0, batch_1, …` → sahkan penghimpunan). Kemudian cetus ntfy:
   `mcp__github__actions_run_trigger` (method `run_workflow`, owner `pedagangsenja`,
   repo `papertrade-claude`, workflow_id `amaran_ntfy.yml`, ref `main`,
   inputs `{"tajuk": "tolak db dipulihkan", "mesej": "<tarikh>: <semakan mana gagal>, <n> batch ditolak"}`).

8. **Tolakan itu sendiri gagal** → cetus ntfy dengan tajuk `tolak db semak GAGAL` dan sebabnya.
   JANGAN laporkan kejayaan.

---

**Jangan** ubah fail repo, jangan commit, jangan terbitkan dashboard. Sesi ini hanya membaca
repo dan menulis ke db. Kalau `jana_db.py` gagal kerana dokumen melebihi 262,144 bait, berhenti
dan cetus ntfy dengan nama dokumen itu — pembetulannya ialah menambahnya ke `jana_db.PECAH`
**selepas** pembacanya dalam `dashboard_v2.html` ditukar kepada `subBhg`, dan itu perubahan kod
yang sesi ini tidak boleh buat.
