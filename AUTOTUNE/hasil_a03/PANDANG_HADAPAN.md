# Imbasan pandang ke hadapan A03

Dijana oleh `AUTOTUNE/sahkan/imbas_a03.py` (2026-10-18 13:57 UTC). Logik `semak_hadapan.imbas` atas parameter AKHIR (k06) dan SEMASA (k07) setiap sistem ditala; isyarat = sig kaedah ∧ F ∧ M, dengan F dalam larian dipotong dikira daripada EPS yang sudah dilaporkan pada tarikh potong. Sampel 150 ticker universe A02 (susunan md5, sejarah sejak 2010), 12 tarikh potong: 2012-06-29, 2013-09-30, 2014-12-31, 2016-03-31, 2017-06-30, 2018-09-28, 2019-12-31, 2021-03-31, 2022-06-30, 2023-09-29, 2024-12-31, 2026-03-31.

Semakan F (set `F`): F(data dan EPS dipotong pada c) = F(penuh) bagi semua hari <= c; peraturan `tersedia` atas 12931 baris EPS sampel: 0 melanggar.

Sistem diimbas: 10. Bersih: 10. PANDANG HADAPAN (melanggar atau ralat): 0.

| Sistem | Status | Set parameter | Lajur dilanggar | Catatan |
|---|---|---|---|---|
| M04_had60 | BERSIH | AKHIR, F, SEMASA | — |  |
| M37_asal | BERSIH | AKHIR, F, SEMASA | — |  |
| M37_had60 | BERSIH | AKHIR, F, SEMASA | — |  |
| M38_had60 | BERSIH | AKHIR, F, SEMASA | — |  |
| M51_asal | BERSIH | AKHIR, F, SEMASA | — |  |
| M78_had60 | BERSIH | AKHIR, F, SEMASA | — |  |
| M88_asal | BERSIH | AKHIR, F, SEMASA | — |  |
| M88_had60 | BERSIH | AKHIR, F, SEMASA | — |  |
| M121_asal | BERSIH | AKHIR, F, SEMASA | — |  |
| M121_had60 | BERSIH | AKHIR, F, SEMASA | — |  |

Kebergantungan hari c yang dibenarkan (buka c+1 sahaja / kewujudan bar c+1) dijumpai pada lajur: exitc, stop. Imbasan bersifat sampel (ticker dan tarikh potong terhad).
