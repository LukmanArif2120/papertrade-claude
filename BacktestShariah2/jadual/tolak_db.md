# Tolak db dashboard harian (sesi Claude BAHARU setiap kali; aktif selepas peralihan, lihat `PERALIHAN.md`)

Masa: 10:20 pagi New York, Isnin–Sabtu (= 10:20 atau 11:20 malam MYT), iaitu selepas belian 9:35 NY.
Model `claude-sonnet-5-5`. Automatik; jangan tanya soalan. Tiada order Moomoo, tiada wang sebenar.
Semua pengiraan dibuat oleh GitHub Actions (`standard/harian_c.py`, `.github/workflows/harian.yml` dan `beli.yml`).
Sesi ini hanya (1) memastikan Actions sudah berjalan dan (2) menolak fail yang sudah dijana ke db dashboard.
Jangan baca fail CSV besar dan jangan bina JSON dengan tangan; guna skrip.

Alat (satu panggilan ToolSearch): `select:ArtifactData,PushNotification,mcp__github__actions_list,mcp__github__actions_run_trigger`
Dashboard: https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e

1. `git pull --rebase origin main`.
2. `python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db0` dan baca medan `pengawas` dalam output.
   Jika `tembak` mengandungi `harian.yml` atau `beli.yml`: semak larian terakhir workflow itu (`mcp__github__actions_list`,
   method `list_workflow_runs`, owner `pedagangsenja`, repo `papertrade-claude`, resource_id nama workflow, perPage 1).
   Jika tiada larian `queued`/`in_progress`, tembak sekali (`mcp__github__actions_run_trigger`, method `run_workflow`,
   workflow_id nama workflow, ref `main`). Jangan tunggu; teruskan dengan data sedia ada dan catat dalam notifikasi.
3. Versi dokumen db: `ArtifactData` `list` bagi koleksi `papertrade` (query.limit 100; ulang dengan next_cursor),
   `prestasi`, `harian`, `sektor` dan `analisis`, dengan `out_dir` <scratchpad>/lama (kandungan tidak perlu dibaca).
   Tulis `<scratchpad>/versi.json` = {"papertrade/claude": versi, …} untuk SEMUA dokumen yang disenaraikan.
4. `python3 BacktestShariah2/standard/jana_db.py --keluar <scratchpad>/db --versi <scratchpad>/versi.json`
   (pecah_claude/bahagi_db sudah dijalankan oleh Actions; skrip gagal jika mana-mana dokumen melebihi had 262,144 bait).
5. Bagi setiap fail `batch_N.json` yang dicetak: `ArtifactData` `batch`, `writes` = kandungan fail itu (setiap entri sudah
   ada `file_path` dan `if_version`). Ditolak kerana versi berubah → ulang langkah 3–5 sekali.
6. Notifikasi (langkah terakhir, juga jika gagal): `PushNotification`, status "proactive", satu baris < 200 aksara:
   `Dashboard <tarikh>: sesi <S>, <n> keluar baharu, <m> senarai beli, <k> direkod hari ini<; tembak harian/beli jika ada>`
   (angka daripada `BacktestShariah2/papertrade/status_harian.json`: malam.keluar_baru_jumlah, malam.senarai_beli, beli.direkod).
Tiada commit diperlukan (sesi ini tidak mengubah fail repo).
