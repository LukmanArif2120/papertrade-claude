# Imbasan pandang ke hadapan (AUTOTUNE)

Dijana oleh `AUTOTUNE/kaedah/semak_hadapan.py` (2026-10-18 04:45 UTC). Data 431 saham (`data_mentah/`), PARAM asal, tarikh potong 2021-06-30, 2023-03-31, 2025-06-30. Selepas audit [M81](AUDIT_M81.md).

Peraturan: `exitc`, `stop`, `tgt` sama dengan larian penuh bagi semua tarikh ≤ c (stop/tgt hari c boleh berbeza hanya jika diterbitkan daripada buka c+1); `sig`, `rank` sama bagi tarikh ≤ c−1, dan pada hari c hanya boleh bergantung pada buka c+1 (ujian buka-sahaja: bar c+1 dengan high/low/close/volume = buka).

Kaedah diimbas: 134. Melanggar sekarang (label PANDANG HADAPAN): 0. Dibaiki: 1.

## Pelanggaran

| Kaedah | Status | Lajur | Ticker | Hari | Sifat | Pembetulan |
|---|---|---|---|---|---|---|
| M81 | DIBAIKI | exitc | 1 | 1 | exitc hari c bergantung nilai bar c+1 | exitc[j] = True apabila tutup[j] <= paras henti mengekor (keluar buka j+1); dahulu exitc[j-1] ditanda daripada rendah[j] (keluar buka j dengan pengetahuan hari j). |

Bagi DIBAIKI, bilangan ticker/hari ialah imbasan modul asal (`--asal`, = salinan sebelum dibaiki) dengan PARAM asal; imbasan semula salinan dibaiki bersih. Imbasan potong-data bersifat sampel (3 tarikh × 431 saham): M81 PARAM asal (ekor 25%) hanya tercetus pada 1 ticker-hari, tetapi kesannya besar selepas penalaan (AUDIT_M81.md).

Semakan statik pelengkap (18 Okt 2026): `shift(-…)` dalam salinan hanya pada `open` (harga pesanan) dan sempadan minggu `ws.shift(-1)` (M52, kalendar); tiada lagi corak `ex[j - 1] = True`; indeks hadapan `l[k + 1]`/`h[k + 1]` dalam M131 ialah fraktal dengan k = i − 2 (disahkan pada hari i).

## Dibenarkan (hari c sahaja)

- `sig/stop/tgt/rank` hari c yang memakai buka hari esok sahaja (harga pesanan), cth. "langkau jika buka esok ≤ henti" atau sasaran = buka_masuk + k×R: boleh dilaksana kerana pesanan dibuat pada buka.
- `exitc` hari c yang hanya bergantung pada kewujudan bar c+1 (pengawal `j + 1 < n` dalam gelung replika dagangan; ujian: bar c+1 = tutup c tanpa maklumat baharu). Enjin juga memerlukan j+1 < n, jadi tiada kesan backtest.
- `stop/rank` dibanding hanya pada hari `sig` benar (enjin membaca st[i] dan rank[i] pada hari isyarat sahaja).

| Kaedah | Lajur (ticker) |
|---|---|
| M02 | tgt (159) |
| M05 | sig (1) |
| M06 | sig (1), stop (10) |
| M07 | sig (1) |
| M13 | sig (10) |
| M14 | sig (13) |
| M15 | sig (1) |
| M20 | sig (1), tgt (24) |
| M23 | sig (2) |
| M26 | tgt (26) |
| M27 | sig (1) |
| M31 | exitc (6) |
| M36 | stop (44) |
| M41 | sig (2) |
| M44 | stop (3) |
| M45 | sig (20) |
| M47 | tgt (1) |
| M50 | sig (1) |
| M52 | rank (25), sig (25), stop (44) |
| M67 | stop (7) |
| M70 | sig (8) |
| M74 | sig (2) |
| M76 | exitc (1) |
| M77 | sig (1) |
| M78 | stop (22) |
| M82 | exitc (10) |
| M87 | stop (2) |
| M88 | stop (5) |
| M100 | tgt (30) |
| M102 | sig (1) |
| M116 | sig (2) |
| M125 | sig (9) |
| M139 | sig (2) |
| M143 | sig (1) |
| M153 | sig (52) |
| M156 | sig (1) |
