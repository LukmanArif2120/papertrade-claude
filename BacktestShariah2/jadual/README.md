# jadual/ — prosedur tugasan berjadual

Prompt tugasan berjadual (Routine) hanya perlu: clone repo, kemudian "ikut `BacktestShariah2/jadual/<fail>.md`". Prosedur dan peraturan disimpan di sini supaya berversi dalam git. Peraturan umum: `standard/tugasan_v3.md`.

| Fail | Routine | Masa |
|---|---|---|
| `kemas_kini_0602.md` | Papertrade – Kemas kini 6:02 pagi (sesi repo) | 6:02 pagi MYT, Sel–Sab |
| `imbas_2002.md` | Papertrade – Imbas 7:47 malam (sesi repo) | 7:47 malam MYT, Isn–Jum (dianjak dari 8:02 pada 15 Okt 2026) |
| `beli_0935.md` | Papertrade – Beli 9:35 NY (sesi repo) | 9:35 pagi New York, Isn–Jum |

Model: `claude-sonnet-5-5` sahaja.

## Pengawas (sejak 15 Okt 2026)
Sesi Sonnet `session_01686xK3etzJNAReGbsM8sAw` ("Pengawas jadual papertrade") menerima tiga tugasan semakan. Setiap semakan memastikan rutin sudah ditembak; jika belum (atau larian gagal tanpa commit dan sesi tidak bekerja selepas 60 minit), rutin itu ditembak semula sekali.

| Pengawas | Masa | Rutin diawasi |
|---|---|---|
| `trig_018zyZSoegh4fQWpWGv3wS9m` | 8:10 dan 9:10 malam MYT, Isn–Jum | Imbas 7:47 malam |
| `trig_01AJf4h6GffXNmHXmQsVzzGF` | 10:00 dan 11:00 pagi New York, Isn–Jum | Beli 9:35 NY |
| `trig_018eaPB3VHoodMscT1s8BiLs` | 6:25 dan 7:25 pagi MYT, Sel–Sab | Kemas kini 6:02 pagi |

Kerana rutin boleh ditembak dua kali, setiap prosedur bermula dengan "Semak pendua".
