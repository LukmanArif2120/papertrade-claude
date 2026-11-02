# JEJAK_SEMUA — 94 kombinasi MASUK × KELUAR dalam Papertrade C (2 Nov 2026)

**Setiap kombinasi yang lulus kesemua empat syarat pradaftar dan boleh dilaksanakan.** Bukan
sampel, bukan top-N. Pradaftar `REVERSE/SPEC_GRID_PENUH.md`, keputusan `REVERSE/GRID_PENUH.md`,
senarai mesin `REVERSE/jejak_semua.csv`.

**Pembetulan kepada keputusan saya sebelum ini:** saya mula-mula menjalankan 40 sahaja kerana
pengguna menyebut "top 30 ke, atau top 40 ke". Itu **contoh**, bukan had, dan saya salah
menganggapnya sebagai kekangan. Had 40 dan had 3-keluar-setiap-masuk **dibuang sepenuhnya**.

## Corong penuh

| | |
|---|---:|
| baris MASUK dalam registry | 147 |
| status `DIUJI` | 78 |
| hadir dalam panel grid | 65 |
| **sel diukur (65 × 23 keluar)** | **1,495** |
| lulus jangkaan mutlak dua tingkap | 688 |
| + lift dua tingkap | 461 |
| + `n ≥ 200` | 313 |
| + BH-FDR pada m = 1,495 | **139** |
| − keluar tidak boleh dilaksanakan (`X12` henti bergerak, 5 keluar lain) | 101 |
| − masuk yang perlukan RS (`N69`, `N70`, `N120`) | **94** ← BERJALAN |

**45 masuk berbeza.** Keluar: `X36` 37 · `X16` 26 · `X17` 10 · `X14` 10 ·
`X13` 6 · `X15` 5.

## Apa yang masih DIBUANG, dan mengapa

- **`X12`** (henti pada jalur bawah BB, bergerak setiap bar) — `enjin.trades` membaca `stop`
  **sekali** pada bar isyarat (`enjin.py:31`). Diuji: henti yang naik 98 → 109 **tidak
  pernah** tercetus. Henti mengekor **mustahil** sebagai lorong 1.
- **`X15`** dikekalkan (5 sel) kerana **lorong 2 repo ialah X15** dan berjalan automatik.
  Audit M1: lorong 2 produksi guna ATR purata-mudah dan kira semula setiap bar, kajian guna
  Wilder dan bekukan pada bar isyarat — jadi 5 kohort itu **anggaran**, bukan replikasi.
- **`N69`, `N70`, `N120`** perlukan RS pasaran / indeks sektor yang tiada dalam
  `sedia(fr, idx)` — masalah sama seperti `U02`.
- **69 baris `PERLU`** dalam registry tidak boleh diuji sama sekali: ia memerlukan ~56
  indikator/sumber data yang repo tiada (`harmonik`, `td_seq`, 62 pola lilin TA-Lib,
  `data_putcall`, `data_13f`…). **Itu halangan sebenar kepada ruang N, bukan had bilangan.**

## Senarai penuh

| # | ID | keluarga | jang latih | jang tahan | lift tahan | menang | n | p | tanpa5 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `N124X15` | POLA | +3.06 | **+16.13** | +12.42 | 44.2% | 12,728 | 0.00367 | +0.40 |
| 2 | `N19X13` | BB | +5.60 | **+11.29** | +6.94 | 63.8% | 73,769 | 0.00358 | +4.26 |
| 3 | `N75X13` | RSI | +4.75 | **+7.47** | +3.12 | 62.6% | 861,071 | 0.00000 | +1.75 |
| 4 | `N73X13` | BB | +4.52 | **+6.89** | +2.54 | 63.8% | 240,838 | 0.00103 | +2.31 |
| 5 | `N124X36` | POLA | +1.51 | **+5.91** | +5.01 | 36.8% | 12,728 | 0.00011 | -4.02 |
| 6 | `N16X13` | RSI | +3.87 | **+5.86** | +1.51 | 63.4% | 567,422 | 0.00013 | +1.22 |
| 7 | `N75X15` | RSI | +2.91 | **+5.61** | +1.90 | 41.3% | 861,071 | 0.00000 | -2.43 |
| 8 | `N42X15` | VOLUM | +2.72 | **+5.46** | +1.75 | 41.6% | 130,675 | 0.00010 | -1.91 |
| 9 | `N119X13` | RSI | +3.32 | **+5.09** | +0.74 | 64.9% | 1,051,604 | 0.00011 | +1.18 |
| 10 | `N37X17` | PECAH | +1.40 | **+4.87** | +3.01 | 42.9% | 19,652 | 0.00076 | -2.90 |
| 11 | `N64X17` | POLA | +1.58 | **+4.82** | +2.96 | 41.7% | 13,667 | 0.00151 | -3.36 |
| 12 | `N28X17` | TREND | +1.74 | **+4.59** | +2.73 | 45.9% | 1,404,045 | 0.00000 | -2.26 |
| 13 | `N75X17` | RSI | +1.97 | **+4.53** | +2.67 | 56.0% | 861,071 | 0.00001 | -1.48 |
| 14 | `N55X13` | ADX | +3.47 | **+4.45** | +0.10 | 64.6% | 113,407 | 0.00251 | +1.12 |
| 15 | `N16X15` | RSI | +2.60 | **+4.35** | +0.65 | 41.2% | 567,422 | 0.00043 | -2.37 |
| 16 | `N37X36` | PECAH | +1.84 | **+4.15** | +3.25 | 36.9% | 19,652 | 0.00000 | -3.11 |
| 17 | `N64X36` | POLA | +1.91 | **+4.11** | +3.22 | 36.1% | 13,667 | 0.00000 | -3.53 |
| 18 | `N50X17` | KETAT | +1.15 | **+3.98** | +2.12 | 45.1% | 14,857 | 0.00351 | -2.11 |
| 19 | `N42X17` | VOLUM | +1.40 | **+3.93** | +2.07 | 43.2% | 130,675 | 0.00005 | -3.05 |
| 20 | `N119X15` | RSI | +2.26 | **+3.93** | +0.22 | 41.2% | 1,051,604 | 0.00026 | -2.12 |
| 21 | `N53X17` | ADX | +1.52 | **+3.81** | +1.96 | 41.9% | 913,085 | 0.00000 | -2.45 |
| 22 | `N65X36` | POLA | +2.93 | **+3.74** | +2.84 | 37.3% | 6,537 | 0.00001 | -3.14 |
| 23 | `N37X14` | PECAH | +1.53 | **+3.45** | +2.46 | 45.5% | 19,652 | 0.00059 | -1.86 |
| 24 | `N37X16` | PECAH | +1.51 | **+3.39** | +2.68 | 39.5% | 19,652 | 0.00129 | -2.46 |
| 25 | `N65X14` | POLA | +2.15 | **+3.23** | +2.24 | 42.7% | 6,537 | 0.00013 | -2.18 |
| 26 | `N64X14` | POLA | +1.59 | **+3.20** | +2.21 | 43.8% | 13,667 | 0.00201 | -2.42 |
| 27 | `N64X16` | POLA | +1.67 | **+3.12** | +2.40 | 38.2% | 13,667 | 0.00456 | -3.03 |
| 28 | `N06X36` | MA | +0.72 | **+2.90** | +2.01 | 33.7% | 13,422 | 0.00205 | -2.27 |
| 29 | `N24X17` | TREND | +1.23 | **+2.85** | +0.99 | 40.7% | 1,359,653 | 0.00035 | -2.44 |
| 30 | `N25X17` | TREND | +1.42 | **+2.73** | +0.87 | 40.8% | 948,243 | 0.00007 | -2.45 |
| 31 | `N42X14` | VOLUM | +1.30 | **+2.60** | +1.61 | 48.3% | 130,675 | 0.00000 | -2.20 |
| 32 | `N42X36` | VOLUM | +1.40 | **+2.59** | +1.70 | 36.0% | 130,675 | 0.00000 | -3.37 |
| 33 | `N53X36` | ADX | +1.02 | **+2.42** | +1.52 | 34.4% | 913,085 | 0.00000 | -2.75 |
| 34 | `N56X17` | ADX | +1.16 | **+2.37** | +0.52 | 39.7% | 1,384,407 | 0.00065 | -2.54 |
| 35 | `N25X36` | TREND | +1.07 | **+2.31** | +1.42 | 34.5% | 948,243 | 0.00000 | -2.72 |
| 36 | `N38X36` | PECAH | +0.62 | **+2.29** | +1.40 | 31.1% | 452,952 | 0.00092 | -2.23 |
| 37 | `N50X14` | KETAT | +0.73 | **+2.20** | +1.21 | 52.1% | 14,857 | 0.00055 | -1.32 |
| 38 | `N56X36` | ADX | +0.96 | **+2.17** | +1.27 | 33.3% | 1,384,407 | 0.00000 | -2.74 |
| 39 | `N53X16` | ADX | +0.89 | **+2.16** | +1.45 | 34.1% | 913,085 | 0.00000 | -2.57 |
| 40 | `N40X36` | VOLUM | +0.90 | **+2.14** | +1.24 | 31.2% | 132,453 | 0.00000 | -2.75 |
| 41 | `N36X36` | PECAH | +0.96 | **+2.13** | +1.24 | 32.9% | 386,797 | 0.00000 | -2.94 |
| 42 | `N24X36` | TREND | +0.94 | **+2.12** | +1.23 | 33.7% | 1,359,653 | 0.00000 | -2.67 |
| 43 | `N22X36` | BB | +1.13 | **+2.09** | +1.20 | 33.5% | 288,864 | 0.00000 | -3.23 |
| 44 | `N33X36` | PECAH | +1.14 | **+2.09** | +1.20 | 35.8% | 223,348 | 0.00000 | -2.45 |
| 45 | `N24X16` | TREND | +0.94 | **+1.98** | +1.27 | 34.2% | 1,359,653 | 0.00000 | -2.48 |
| 46 | `N45X36` | UNDUR | +0.93 | **+1.93** | +1.04 | 32.5% | 1,649,671 | 0.00000 | -2.67 |
| 47 | `N54X36` | ADX | +0.93 | **+1.90** | +1.01 | 32.7% | 1,820,574 | 0.00000 | -2.59 |
| 48 | `N57X36` | ADX | +1.12 | **+1.90** | +1.00 | 33.2% | 45,009 | 0.00004 | -2.92 |
| 49 | `N07X36` | MA | +0.89 | **+1.89** | +1.00 | 31.8% | 85,712 | 0.00012 | -2.69 |
| 50 | `N66X36` | POLA | +1.65 | **+1.84** | +0.95 | 37.1% | 43,179 | 0.00186 | -3.16 |
| 51 | `N27X36` | TREND | +0.92 | **+1.83** | +0.94 | 33.0% | 1,562,663 | 0.00000 | -2.54 |
| 52 | `N42X16` | VOLUM | +1.15 | **+1.82** | +1.11 | 37.0% | 130,675 | 0.00000 | -3.16 |
| 53 | `N25X16` | TREND | +0.92 | **+1.81** | +1.09 | 34.9% | 948,243 | 0.00000 | -2.58 |
| 54 | `N31X36` | PECAH | +1.06 | **+1.79** | +0.89 | 36.1% | 176,582 | 0.00000 | -2.89 |
| 55 | `N29X36` | TREND | +0.94 | **+1.78** | +0.89 | 32.1% | 1,557,048 | 0.00000 | -2.67 |
| 56 | `N47X36` | KETAT | +0.90 | **+1.77** | +0.88 | 31.9% | 303,256 | 0.00004 | -2.60 |
| 57 | `N76X36` | MA | +0.86 | **+1.76** | +0.87 | 31.3% | 2,296,233 | 0.00000 | -2.67 |
| 58 | `N28X36` | TREND | +0.65 | **+1.74** | +0.85 | 36.9% | 1,404,045 | 0.00000 | -2.68 |
| 59 | `N43X36` | UNDUR | +0.72 | **+1.66** | +0.77 | 29.6% | 233,028 | 0.00011 | -2.64 |
| 60 | `N75X14` | RSI | +1.36 | **+1.62** | +0.63 | 66.2% | 861,071 | 0.00062 | -0.49 |
| 61 | `N28X14` | TREND | +0.82 | **+1.60** | +0.61 | 49.6% | 1,404,045 | 0.00044 | -1.57 |
| 62 | `N54X16` | ADX | +0.98 | **+1.58** | +0.87 | 35.1% | 1,820,574 | 0.00000 | -2.41 |
| 63 | `N68X36` | POLA | +0.82 | **+1.57** | +0.67 | 31.8% | 106,476 | 0.00004 | -2.85 |
| 64 | `N41X36` | VOLUM | +0.83 | **+1.57** | +0.67 | 32.5% | 1,536,991 | 0.00000 | -2.73 |
| 65 | `N09X36` | MA | +0.65 | **+1.54** | +0.65 | 29.5% | 229,340 | 0.00003 | -2.61 |
| 66 | `N36X16` | PECAH | +0.84 | **+1.53** | +0.81 | 36.0% | 386,797 | 0.00000 | -2.64 |
| 67 | `N39X36` | PECAH | +0.97 | **+1.50** | +0.61 | 34.0% | 36,881 | 0.00120 | -2.65 |
| 68 | `N56X16` | ADX | +0.80 | **+1.48** | +0.77 | 34.9% | 1,384,407 | 0.00001 | -2.53 |
| 69 | `N07X16` | MA | +0.91 | **+1.48** | +0.76 | 36.1% | 85,712 | 0.00117 | -2.37 |
| 70 | `N22X14` | BB | +0.85 | **+1.44** | +0.45 | 39.3% | 288,864 | 0.00023 | -2.50 |
| 71 | `N36X14` | PECAH | +0.68 | **+1.44** | +0.45 | 41.1% | 386,797 | 0.00183 | -2.25 |
| 72 | `N08X36` | MA | +0.66 | **+1.40** | +0.51 | 30.5% | 1,596,759 | 0.00038 | -2.60 |
| 73 | `N22X16` | BB | +0.94 | **+1.40** | +0.68 | 35.5% | 288,864 | 0.00001 | -2.97 |
| 74 | `N35X36` | PECAH | +1.38 | **+1.34** | +0.44 | 36.0% | 182,300 | 0.00001 | -2.67 |
| 75 | `N45X16` | UNDUR | +0.84 | **+1.32** | +0.60 | 35.1% | 1,649,671 | 0.00014 | -2.44 |
| 76 | `N28X16` | TREND | +0.47 | **+1.31** | +0.59 | 36.7% | 1,404,045 | 0.00013 | -2.44 |
| 77 | `N47X16` | KETAT | +0.85 | **+1.30** | +0.58 | 35.3% | 303,256 | 0.00002 | -2.34 |
| 78 | `N33X14` | PECAH | +0.80 | **+1.30** | +0.31 | 40.0% | 223,348 | 0.00044 | -2.04 |
| 79 | `N48X36` | KETAT | +0.52 | **+1.28** | +0.38 | 34.1% | 158,573 | 0.00214 | -2.56 |
| 80 | `N40X16` | VOLUM | +0.91 | **+1.27** | +0.55 | 35.3% | 132,453 | 0.00003 | -2.53 |
| 81 | `N57X16` | ADX | +0.97 | **+1.26** | +0.54 | 35.5% | 45,009 | 0.00439 | -2.71 |
| 82 | `N29X16` | TREND | +0.84 | **+1.23** | +0.51 | 35.6% | 1,557,048 | 0.00007 | -2.45 |
| 83 | `N08X16` | MA | +0.67 | **+1.18** | +0.46 | 35.8% | 1,596,759 | 0.00099 | -2.23 |
| 84 | `N33X16` | PECAH | +0.88 | **+1.16** | +0.44 | 36.1% | 223,348 | 0.00053 | -2.47 |
| 85 | `N74X16` | TREND | +0.58 | **+1.15** | +0.44 | 37.1% | 2,255,263 | 0.00437 | -2.29 |
| 86 | `N68X16` | POLA | +0.74 | **+1.15** | +0.43 | 35.9% | 106,476 | 0.00064 | -2.56 |
| 87 | `N76X16` | MA | +0.75 | **+1.14** | +0.42 | 34.9% | 2,296,233 | 0.00046 | -2.42 |
| 88 | `N27X16` | TREND | +0.78 | **+1.10** | +0.38 | 34.3% | 1,562,663 | 0.00096 | -2.43 |
| 89 | `N41X16` | VOLUM | +0.75 | **+1.05** | +0.33 | 35.3% | 1,536,991 | 0.00073 | -2.51 |
| 90 | `N80X36` | PECAH | +1.15 | **+0.99** | +0.09 | 36.1% | 110,082 | 0.00026 | -2.41 |
| 91 | `N113X36` | POLA | +0.61 | **+0.97** | +0.08 | 34.2% | 389,109 | 0.00034 | -2.64 |
| 92 | `N51X36` | KETAT | +0.46 | **+0.95** | +0.06 | 27.8% | 59,912 | 0.00053 | -2.60 |
| 93 | `N51X16` | KETAT | +0.74 | **+0.84** | +0.12 | 30.8% | 59,912 | 0.00001 | -2.70 |
| 94 | `N113X16` | POLA | +0.50 | **+0.82** | +0.10 | 37.3% | 389,109 | 0.00163 | -2.35 |

## Had yang mengikat setiap baris

- **`tanpa5` POSITIF hanya pada 7 daripada 94** — dan **enam daripada tujuh memakai
  `X13`**. Jadi kelebihan 87 kombinasi **hidup dalam ekor kanan**, dan `SETUP.md` (598/598
  penapis merugikan selepas pemangkasan ekor) masih terpakai sepenuhnya kepada mereka.
  Tujuh itu: `N19X13` +4.26 · `N73X13` +2.31 · `N75X13` +1.75 · `N16X13` +1.22 ·
  `N119X13` +1.18 · `N55X13` +1.12 · `N124X15` +0.40.
- **`N124` latih +3.06 lawan tahan +16.13** — jurang 5×. Sebahagian besar kelebihannya
  khusus 2020–2025. Jangan saiz ia seperti +16%.
- Ini jangkaan **setiap dagangan**, bukan prestasi portfolio. `KEPUTUSAN_AKHIR.md` sudah
  mengukur 724 konfigurasi portfolio dengan T1 = 0.
- Kos produksi ≈ ⅓ kos kajian; alam dagangan ditapis SPUS lawan `a02` kajian (tiada delist).
  Nombor hadapan **tidak** boleh dibanding terus dengan jadual di atas.
- `p` menguji **lift**, bukan jangkaan mutlak (salinan verbatim `step19`).
- Paksi **PEGANG** belum diuji sebagai paksi berasingan; `TMAX` dikunci 126 pada semua.
- Keputusan **bersyarat**: 65 topeng dipilih daripada 147 oleh `status = DIUJI`.

## Pengesahan hujung-ke-hujung (sebelum larian sebenar)

`harian_c.py malam` penuh ke folder **sandbox**, bukan `papertrade/`:

```
ralat_kaedah: TIADA
senarai_beli 1,333 baris · isyarat 16,841 · watchlist 297
kombinasi: 93/94 hasilkan isyarat, 880 jumlah
pecahan keluar: X36 36 · X16 26 · X17 10 · X14 10 · X13 6 · X15 5
baris dengan `henti` bukan kosong: 0
sahkan.py pada sandbox: 0 ralat, 0 amaran
```

`N06X36` sifar isyarat — `N06` ialah golden cross `ma50` silang `ma200`, yang ujian pariti
ukur mencetus pada **0.17% bar** (53 dalam 30,828). Sifar pada satu sesi dijangka; modulnya
berfungsi.

**880 isyarat Nxx setiap sesi** berbanding 345 dengan 40 kombinasi. Pada 1.67 KB/posisi dan
126 sesi itu ~**185 MB**, dan `.git` sudah 484 MB. Kalau saiz repo menjadi masalah, pilihan
yang betul ialah **memangkas 87 kombinasi yang `tanpa5` negatif**, bukan memangkas secara
rawak — tujuh yang tahan pemangkasan ekor ialah maklumat yang 87 itu tidak beri.
