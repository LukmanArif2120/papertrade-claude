# Liputan EPS A03 (Yahoo `get_earnings_dates`)

Dijana 2026-10-18T12:44Z. Shard 10. Spesifikasi: `AUTOTUNE/SPEC_A03.md` §1.

## Ringkasan
- Ticker universe A02: 3260; ticker dengan sekurang-kurangnya satu EPS: 3190 (97.9%); tanpa EPS: 70.
- Baris suku (selepas nyahpendua): 185431; sumber yahoo 185431, repo (benih eps.csv) 0; laporan 1998-05-30 hingga 2026-10-17.
- Masa: selepas 93287, sebelum 87151, tidak diketahui 4993.
- eps_yoy sah (EPS suku lalu > 0 dan jarak ~1 tahun): 135804 baris.

## Liputan setiap tahun
Peratus baris ticker-bulan universe pada hari dagangan terakhir bulan yang suku terkininya tersedia (titik masa) dan dilaporkan <= 135 hari sebelum ("ada"); "yoy" = ada dan eps_yoy sah; "F" = yoy dan EPS > 0 dan yoy >= 25%.

| Tahun | Baris | ada % | ada A % | ada B % | yoy % | F % |
|---|---|---|---|---|---|---|
| 2010 | 12153 | 93.5 | 92.3 | 94.7 | 78.7 | 30.6 |
| 2011 | 13343 | 93.9 | 93.1 | 94.6 | 82.5 | 34.0 |
| 2012 | 13408 | 94.3 | 93.9 | 94.7 | 85.3 | 25.2 |
| 2013 | 14925 | 94.2 | 93.4 | 95.1 | 85.1 | 23.3 |
| 2014 | 16599 | 93.6 | 93.0 | 94.3 | 83.9 | 23.2 |
| 2015 | 17502 | 93.3 | 92.9 | 93.8 | 83.1 | 21.1 |
| 2016 | 17823 | 93.5 | 93.2 | 93.9 | 83.5 | 18.9 |
| 2017 | 19689 | 93.6 | 93.3 | 94.0 | 80.9 | 21.8 |
| 2018 | 20981 | 93.9 | 93.4 | 94.3 | 80.9 | 34.4 |
| 2019 | 21244 | 94.3 | 94.3 | 94.3 | 82.4 | 21.2 |
| 2020 | 21824 | 94.1 | 94.2 | 94.0 | 79.1 | 18.7 |
| 2021 | 23989 | 94.6 | 94.4 | 94.8 | 71.2 | 34.4 |
| 2022 | 24000 | 95.7 | 95.4 | 96.0 | 77.6 | 26.8 |
| 2023 | 24000 | 95.8 | 95.9 | 95.8 | 79.8 | 21.2 |
| 2024 | 24000 | 96.2 | 96.1 | 96.4 | 81.6 | 21.1 |
| 2025 | 24000 | 96.4 | 96.4 | 96.4 | 82.3 | 23.0 |
| 2026 | 20000 | 96.9 | 96.8 | 97.0 | 82.0 | 28.5 |

Tanda SPEC §1: liputan < 70% bagi tahun 2013-2018 -> **tiada (semua >= 70%)**.

## Kegagalan
- Ticker gagal/kosong pada Yahoo: 70.
  - kosong (sumber ganti: tiada): 70
- Ticker universe tanpa sebarang EPS: 70; contoh: AAUC, ABTS, AGIG, AIIO, AIV, AMBR, ARQQ, ASA, ATHE, AYA, BATRA, BF-A, BHK, BME, BTT, CRML, DDS, DGNX, DJCO, DJT, DOGZ, DXYZ, ET, ETO, FER, FNGD, FNGO, GAM, GFAI, GLIBK.

## Kaveat
- EPS Yahoo ialah EPS dilaporkan/dilaras penganalisis, bukan GAAP; sejarah awal tidak lengkap; tiada saham delist.
- Masa laporan 09:30-15:59 dan 00:00 = "tidak diketahui" (guna hari dagangan berikutnya).
