# jadual/ — prosedur tugasan berjadual

Prompt tugasan berjadual (Routine) hanya perlu: clone repo, kemudian "ikut `BacktestShariah2/jadual/<fail>.md`". Prosedur dan peraturan disimpan di sini supaya berversi dalam git. Peraturan umum: `standard/tugasan_v3.md`.

| Fail | Routine | Masa |
|---|---|---|
| `kemas_kini_0602.md` | Papertrade – Kemas kini 6:02 pagi (sesi repo) | 6:02 pagi MYT, Sel–Sab |
| `imbas_2002.md` | Papertrade – Imbas 7:47 malam (sesi repo) | 7:47 malam MYT, Isn–Jum (dianjak dari 8:02 pada 15 Okt 2026) |
| `beli_0935.md` | Papertrade – Beli 9:35 NY (sesi repo) | 9:35 pagi New York, Isn–Jum |

Model: `claude-sonnet-5-5` sahaja.

## Pengawas (sejak 15 Okt 2026)
**DIMATIKAN 19 Okt 2026** (keputusan pengguna, jimat ~4 juta token sehari; ~0.66 juta setiap semakan). Rutin tidak lagi ditembak semula secara automatik; jika rutin gagal, tembak manual atau tunggu peralihan ke Actions.

Sesi Sonnet `session_01686xK3etzJNAReGbsM8sAw` ("Pengawas jadual papertrade") menerima tiga tugasan semakan. Setiap semakan memastikan rutin sudah ditembak; jika belum (atau larian gagal tanpa commit dan sesi tidak bekerja selepas 60 minit), rutin itu ditembak semula sekali.

| Pengawas | Masa | Rutin diawasi |
|---|---|---|
| `trig_018zyZSoegh4fQWpWGv3wS9m` | 8:10 dan 9:10 malam MYT, Isn–Jum | Imbas 7:47 malam |
| `trig_01AJf4h6GffXNmHXmQsVzzGF` | 10:00 dan 11:00 pagi New York, Isn–Jum | Beli 9:35 NY |
| `trig_018eaPB3VHoodMscT1s8BiLs` | 6:25 dan 7:25 pagi MYT, Sel–Sab | Kemas kini 6:02 pagi |

Kerana rutin boleh ditembak dua kali, setiap prosedur bermula dengan "Semak pendua".

## Peralihan ke GitHub Actions (sejak 17 Okt 2026; mod selari 3 hari dagangan)
Keputusan pengguna 17 Okt 2026 (jimat token): kerja harian dipindah ke GitHub Actions tanpa LLM — `.github/workflows/harian.yml`
(kemas kini + imbas + gred, 05:07 UTC Sel–Sab), `beli.yml` (9:40 NY), `petang.yml` (gred P sebelum buka); skrip `standard/harian_c.py`. Papan Penganalisis (20 Okt 2026):
`analisis.yml` dicetus sebaik `lejar.yml` siap (`standard/penganalisis.py`); rutin 6:02 menolak `analisis/papan` ke db.
Mod dalam `BacktestShariah2/MOD_ACTIONS`: `bayang` (sekarang) = Actions menulis ke `BacktestShariah2/bayang/` dan membanding setiap
hari dengan rutin Claude (`bayang/BANDING_<tarikh>.md`); tiga rutin di atas KEKAL RASMI sehingga peralihan.
Selepas peralihan (`PERALIHAN.md`): rutin di atas dan pengawas dimatikan; sesi Claude hanya `tolak_db.md` (Isn–Sab 10:20 NY; notifikasi belian),
`notifikasi_harian.md` (Sel–Sab 3:17 petang MYT; notifikasi kemas kini + imbas) dan `mingguan.md` (Ahad).
