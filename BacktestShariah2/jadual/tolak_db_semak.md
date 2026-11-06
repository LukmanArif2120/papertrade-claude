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

3. Baca keadaan HIDUP: `ArtifactData` `get` koleksi `harian` doc_id `status` (TANPA out_dir; dokumen kecil)
   dan koleksi `meta` doc_id `versi_db` (TANPA out_dir). `out_dir` dan `list` kini DITOLAK oleh alat bagi
   dokumen db ini (6 Nov 2026) — jangan cuba.

4. **Semakan A — kesegaran.** Banding `harian/status` hidup (langkah 3) dengan
   `<scratchpad>/db0/harian/status.json` pada tiga medan: `harga_tutup_pada`, `tarikh_data`,
   `beli_pada`. Ketiga-tiganya sama → db segar.

5. **Semakan B — daftar versi.** `meta/versi_db` hidup: medan `data.sesi` mesti sama dengan `sesi` dalam
   `<scratchpad>/db0/ringkas.json`. Daftar hanya ditulis selepas SEMUA batch diterima (tolak_db.md 5c), jadi
   sesi yang sama bermakna tolakan 10:20 lengkap. (Semakan lama membaca bahagian dengan `out_dir`; ditolak.)

6. **Kedua-dua semakan lulus** → tamat. Tiada tolakan, tiada notifikasi, tiada commit.
   Balas satu baris: `db segar (sesi <tarikh>), 0 tindakan`.

7. **Mana-mana semakan gagal** → jalankan `BacktestShariah2/jadual/tolak_db.md` langkah 3–5c
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
