# JEJAK40 — 40 kombinasi MASUK × KELUAR dalam Papertrade C (2 Nov 2026)

Menggantikan jejak 20-kohort. Pradaftar `REVERSE/SPEC_GRID_PENUH.md`, keputusan
`REVERSE/GRID_PENUH.md`, senarai mesin `REVERSE/jejak40.csv`.

Setiap ID produksi ialah **`masuk` + `keluar`** (cth. `N19X13`), jadi paksi keluar — yang
diukur **~12× lebih berpengaruh** daripada masuk — akhirnya diuji ke hadapan. Jejak lama
mengunci `X13` pada kesemua 20 kohort, dan `X13` hanya memegang 6 daripada 139 slot yang
lulus FDR.

## Mengapa 40 ini dan bukan top-40 mentah

Senarai mentah mengandungi dua keluar yang **tidak boleh dilaksanakan dengan setia**, dan
saya mengesahkannya dengan ujian pada enjin, bukan dengan membaca kod:

- **`X12`** (henti pada jalur bawah BB, bergerak setiap bar) dan **`X15`** (Chandelier
  mengekor) memerlukan henti yang BERGERAK. `enjin.trades` membaca `stop` **sekali** pada bar
  isyarat (`enjin.py:31` `sp = st[i]`). Ujian: henti yang naik 98 → 109 **tidak pernah**
  tercetus; dagangan berjalan ke hujung data. Jadi henti mengekor **mustahil** sebagai
  lorong 1.
- `X12` **dibuang** (5 sel). `X15` **dikekalkan** (5 sel) kerana **lorong 2 repo ialah X15** —
  kohort itu dikod tanpa keluar kaedah dan lorong 2 ialah keluarnya. Nota audit M1 terpakai:
  lorong 2 produksi guna ATR purata-mudah dan mengira semula setiap bar, sedangkan kajian
  guna Wilder dan membekukannya pada bar isyarat. Jadi 5 kohort itu ialah **anggaran**
  `X15`, bukan replikasi.
- **`N69`/`N70` dibuang** — ia perlukan RS pasaran dan indeks sektor yang tidak tersedia
  dalam `sedia(fr, idx)`, masalah sama seperti `U02` dan `N120`.

Slot yang terkosong diisi oleh sel seterusnya yang lulus kesemua empat syarat, mengikut
susunan `jangkaan_tahan` yang sama dan had 3-keluar-setiap-masuk yang sama. 101 daripada 139
yang lulus FDR mempunyai keluar yang boleh dilaksanakan, jadi senarai 40 penuh.

## Senarai

| # | masuk | keluarga | keluar | jang latih | jang tahan | lift tahan | menang | n | p | tanpa5 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `N124` | POLA | `X15` | +3.064 | **+16.127** | +12.421 | 44.2% | 12,728 | 0.00367 | +0.396 |
| 2 | `N19` | BB | `X13` | +5.597 | **+11.285** | +6.935 | 63.8% | 73,769 | 0.00358 | +4.262 |
| 3 | `N75` | RSI | `X13` | +4.748 | **+7.468** | +3.118 | 62.6% | 861,071 | 0.00000 | +1.752 |
| 4 | `N73` | BB | `X13` | +4.523 | **+6.892** | +2.542 | 63.8% | 240,838 | 0.00103 | +2.311 |
| 5 | `N124` | POLA | `X36` | +1.508 | **+5.906** | +5.014 | 36.8% | 12,728 | 0.00011 | -4.022 |
| 6 | `N16` | RSI | `X13` | +3.875 | **+5.857** | +1.506 | 63.4% | 567,422 | 0.00013 | +1.222 |
| 7 | `N75` | RSI | `X15` | +2.913 | **+5.608** | +1.902 | 41.3% | 861,071 | 0.00000 | -2.432 |
| 8 | `N42` | VOLUM | `X15` | +2.723 | **+5.461** | +1.755 | 41.6% | 130,675 | 0.00010 | -1.915 |
| 9 | `N119` | RSI | `X13` | +3.319 | **+5.090** | +0.740 | 64.9% | 1,051,604 | 0.00011 | +1.176 |
| 10 | `N37` | PECAH | `X17` | +1.402 | **+4.868** | +3.013 | 42.9% | 19,652 | 0.00076 | -2.895 |
| 11 | `N64` | POLA | `X17` | +1.582 | **+4.815** | +2.960 | 41.7% | 13,667 | 0.00151 | -3.363 |
| 12 | `N28` | TREND | `X17` | +1.742 | **+4.586** | +2.731 | 45.9% | 1,404,045 | 0.00000 | -2.259 |
| 13 | `N75` | RSI | `X17` | +1.973 | **+4.526** | +2.670 | 56.0% | 861,071 | 0.00001 | -1.484 |
| 14 | `N55` | ADX | `X13` | +3.475 | **+4.449** | +0.098 | 64.6% | 113,407 | 0.00251 | +1.115 |
| 15 | `N16` | RSI | `X15` | +2.603 | **+4.352** | +0.646 | 41.2% | 567,422 | 0.00043 | -2.373 |
| 16 | `N37` | PECAH | `X36` | +1.839 | **+4.145** | +3.253 | 36.9% | 19,652 | 0.00000 | -3.114 |
| 17 | `N64` | POLA | `X36` | +1.907 | **+4.115** | +3.222 | 36.1% | 13,667 | 0.00000 | -3.531 |
| 18 | `N50` | KETAT | `X17` | +1.152 | **+3.977** | +2.121 | 45.1% | 14,857 | 0.00351 | -2.114 |
| 19 | `N42` | VOLUM | `X17` | +1.397 | **+3.929** | +2.073 | 43.2% | 130,675 | 0.00005 | -3.052 |
| 20 | `N119` | RSI | `X15` | +2.262 | **+3.927** | +0.221 | 41.2% | 1,051,604 | 0.00026 | -2.125 |
| 21 | `N53` | ADX | `X17` | +1.516 | **+3.814** | +1.958 | 41.9% | 913,085 | 0.00000 | -2.446 |
| 22 | `N65` | POLA | `X36` | +2.927 | **+3.736** | +2.844 | 37.3% | 6,537 | 0.00001 | -3.140 |
| 23 | `N37` | PECAH | `X14` | +1.528 | **+3.448** | +2.457 | 45.5% | 19,652 | 0.00059 | -1.855 |
| 24 | `N65` | POLA | `X14` | +2.151 | **+3.230** | +2.239 | 42.7% | 6,537 | 0.00013 | -2.185 |
| 25 | `N64` | POLA | `X14` | +1.593 | **+3.199** | +2.208 | 43.8% | 13,667 | 0.00201 | -2.419 |
| 26 | `N06` | MA | `X36` | +0.721 | **+2.904** | +2.012 | 33.7% | 13,422 | 0.00205 | -2.270 |
| 27 | `N24` | TREND | `X17` | +1.231 | **+2.847** | +0.991 | 40.7% | 1,359,653 | 0.00035 | -2.438 |
| 28 | `N25` | TREND | `X17` | +1.423 | **+2.730** | +0.874 | 40.8% | 948,243 | 0.00007 | -2.451 |
| 29 | `N42` | VOLUM | `X14` | +1.295 | **+2.599** | +1.608 | 48.3% | 130,675 | 0.00000 | -2.201 |
| 30 | `N53` | ADX | `X36` | +1.025 | **+2.417** | +1.525 | 34.4% | 913,085 | 0.00000 | -2.750 |
| 31 | `N56` | ADX | `X17` | +1.161 | **+2.373** | +0.517 | 39.7% | 1,384,407 | 0.00065 | -2.544 |
| 32 | `N25` | TREND | `X36` | +1.067 | **+2.308** | +1.416 | 34.5% | 948,243 | 0.00000 | -2.717 |
| 33 | `N38` | PECAH | `X36` | +0.619 | **+2.292** | +1.400 | 31.1% | 452,952 | 0.00092 | -2.226 |
| 34 | `N50` | KETAT | `X14` | +0.733 | **+2.201** | +1.210 | 52.1% | 14,857 | 0.00055 | -1.318 |
| 35 | `N56` | ADX | `X36` | +0.960 | **+2.167** | +1.275 | 33.3% | 1,384,407 | 0.00000 | -2.741 |
| 36 | `N53` | ADX | `X16` | +0.894 | **+2.163** | +1.445 | 34.1% | 913,085 | 0.00000 | -2.569 |
| 37 | `N40` | VOLUM | `X36` | +0.900 | **+2.137** | +1.245 | 31.2% | 132,453 | 0.00000 | -2.747 |
| 38 | `N36` | PECAH | `X36` | +0.959 | **+2.129** | +1.237 | 32.9% | 386,797 | 0.00000 | -2.936 |
| 39 | `N24` | TREND | `X36` | +0.944 | **+2.122** | +1.230 | 33.7% | 1,359,653 | 0.00000 | -2.665 |
| 40 | `N22` | BB | `X36` | +1.128 | **+2.095** | +1.202 | 33.5% | 288,864 | 0.00000 | -3.225 |

**Pecahan keluar:** `X36` 13 · `X17` 10 · `X13` 6 · `X15` 5 · `X14` 5 · `X16` 1
**22 masuk berbeza** merentas 10 keluarga indikator.

## Had yang mengikat setiap baris

- **`tanpa5` NEGATIF pada 33 daripada 40** (positif hanya 7, dan 6 daripada 7 memakai `X13`).
  Jadi kelebihan majoriti senarai **hidup dalam ekor kanan**, dan `SETUP.md` masih terpakai.
- **`N124` latih +3.064 lawan tahan +16.127** — jurang 5×. Sebahagian besar kelebihannya
  khusus 2020–2025. Jangan saiz ia seperti +16%.
- Ini jangkaan **setiap dagangan**, bukan prestasi portfolio. `KEPUTUSAN_AKHIR.md` sudah
  mengukur 724 konfigurasi portfolio dengan T1 = 0.
- Alam kajian `a02` tiada delist; alam dagangan ditapis SPUS. Kos produksi ≈ ⅓ kos kajian
  (audit M3). Jadi nombor hadapan **tidak** boleh dibandingkan terus dengan jadual di atas.
- 65 topeng dipilih daripada 147 oleh `status = DIUJI`; keputusan **bersyarat**.
- `p` menguji **lift**, bukan jangkaan mutlak (salinan verbatim `step19`). Syarat 1 dan 2
  mengendalikan jangkaan mutlak secara berasingan.
- Paksi **PEGANG** belum diuji sebagai paksi berasingan; `TMAX` dikunci 126 pada semua.

## Jurang audit F6 ditutup

Jejak 20-kohort hanya menguji pariti bit bagi **6 daripada 20** topeng. `TestPariti40` kini
menguji **kesemua 22 topeng + 5 keluar** yang 40 kohort pakai, dengan senarai dijana daripada
`jejak40.csv` — jadi kohort baharu **tidak boleh** masuk produksi tanpa pariti diuji.
