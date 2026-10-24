# Notifikasi harian Actions (sesi Claude BAHARU setiap kali; aktif selepas peralihan, lihat `PERALIHAN.md`)

Permintaan pengguna 24 Okt 2026: notifikasi setiap kali kerja papertrade GitHub Actions siap (papertrade sahaja; kegagalan
workflow lain disertakan). Dua notifikasi sehari: (1) fail ini selepas `harian.yml` (kemas kini posisi + imbas);
(2) `jadual/tolak_db.md` langkah 6 selepas `beli.yml`.

Masa: 3:17 petang MYT, Selasa–Sabtu (`harian.yml` biasanya siap 2:00–3:00 petang MYT). Model `claude-sonnet-5-5`.
Automatik; jangan tanya soalan. Tiada order, tiada wang sebenar. Jangan ubah fail repo; tiada commit.

Alat (satu panggilan ToolSearch): `select:PushNotification,mcp__github__actions_list`

1. `git pull --rebase origin main`.
2. `mcp__github__actions_list` (method `list_workflow_runs`, owner `pedagangsenja`, repo `papertrade-claude`, perPage 50).
   Kumpul nama fail workflow (`path` tanpa `.github/workflows/`) yang `conclusion` = `failure` dan `created_at` dalam 24 jam
   lepas, KECUALI yang berjaya pada larian lebih baharu bagi workflow sama. Gagal panggil alat → `--gagal ""` dan teruskan.
3. `python3 BacktestShariah2/standard/notifikasi.py malam --gagal "<nama,dipisah,koma>"` → satu baris.
4. `PushNotification`, status "proactive", mesej = baris itu TEPAT (jangan tambah atau ubah angka).
