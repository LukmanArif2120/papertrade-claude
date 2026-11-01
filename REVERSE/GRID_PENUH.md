# GRID_PENUH — 1,495 kombinasi MASUK × KELUAR, dan senarai 40 untuk papertrade

Pradaftar: `REVERSE/SPEC_GRID_PENUH.md` (komit `198ffa5`, sebelum larian).
Skrip: `REVERSE/step32_grid_penuh.py` · Data: `grid_penuh.csv` (1,495), `grid_top40.csv`,
log penuh `grid_larian.log`.

**KAWALAN REGRESI LULUS: 46 sel bertindih dengan `nxx_keluar.csv`, 0 metrik terpesong.**

## Keputusan gate — penyebut BH-FDR JUJUR m = 1,495

| syarat | lulus |
|---|---:|
| 1 · jangkaan **mutlak** > 0 pada kedua-dua tingkap | 688 / 1,495 |
| 2 · lift > 0 pada kedua-dua tingkap | 461 / 1,495 |
| 1+2+3 · tambah `n_tahan ≥ 200` | **313** / 1,495 |
| 4 · BH-FDR q ≤ 0.05 pada **m = 1,495** (ambang p ≤ 4.556e-03) | **139** / 1,495 |

**139 lulus kesemua empat syarat**, jadi senarai 40 penuh tanpa perlu label `TIADA_FDR`.
Itu membetulkan secara langsung kecacatan `AUDIT_JEJAK_N.md` F1: penyebut di sini ialah
setiap sel yang diukur, bukan m=8 pada satu sudut grid.

## Senarai 40 (maks 3 keluar setiap masuk → 21 masuk berbeza)

Lihat `grid_top40.csv`. Sepuluh teratas:

| # | masuk | kelg | keluar | jang latih | jang tahan | lift tahan | menang | n | p | tanpa5 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `N124` | POLA | `X15` | +3.064 | **+16.127** | **+12.421** | 44.2% | 12,728 | 0.00367 | **+0.396** |
| 2 | `N19` | BB | `X13` | +5.597 | +11.285 | +6.935 | 63.8% | 73,769 | 0.00358 | **+4.262** |
| 3 | `N124` | POLA | `X12` | +0.633 | +9.275 | +8.314 | 36.7% | 12,334 | 0.00284 | −4.794 |
| 4 | `N75` | RSI | `X13` | +4.748 | +7.468 | +3.118 | 62.6% | 861,071 | 0.00000 | +1.752 |
| 5 | `N73` | BB | `X13` | +4.523 | +6.892 | +2.542 | 63.8% | 240,838 | 0.00103 | +2.311 |
| 6 | `N124` | POLA | `X36` | +1.508 | +5.906 | +5.014 | 36.8% | 12,728 | 0.00011 | −4.022 |
| 7 | `N16` | RSI | `X13` | +3.875 | +5.857 | +1.506 | 63.4% | 567,422 | 0.00013 | +1.222 |
| 8 | `N75` | RSI | `X15` | +2.913 | +5.608 | +1.902 | 41.3% | 861,071 | 0.00000 | −2.432 |
| 9 | `N42` | VOLUM | `X15` | +2.723 | +5.461 | +1.755 | 41.6% | 130,675 | 0.00010 | −1.915 |
| 10 | `N119` | RSI | `X13` | +3.319 | +5.090 | +0.740 | 64.9% | 1,051,604 | 0.00011 | +1.176 |

## Empat dapatan yang mengubah keputusan

**(1) `N124 × X15` ialah sel TERBAIK dalam kajian, dan ia GAGAL gate dalam grid jarang.**
Jangkaan tahan **+16.127%**, lift **+12.421** — 1.8× `N19` dan 4× apa yang dihantar ke
produksi. `tanpa5` **+0.396 POSITIF**. Dalam `nxx.csv` (yang hanya menguji `X1`–`X4`) `N124`
gagal gate1 kerana lift latihnya negatif pada keluar asas; pada `X15` ia positif pada
kedua-dua tingkap. **Keluar yang salah menyembunyikan masuk yang terbaik.** `n` hanya 12,728
jadi ia jarang, dan latihnya +3.064 jauh di bawah tahannya +16.127 — jadi bahagian besar
kelebihan itu khusus 2020–2025.

**(2) `N19 × X13` ada `tanpa5` = +4.262 — tertinggi di mana-mana dalam kajian.** Lebih baik
daripada +2.858 `GB02_atau3 × X13` yang spec lama dakwa "satu-satunya". Jadi bukan sahaja
dakwaan "satu-satunya" itu salah (audit F5), nombor yang betul **lebih tinggi** dan ia milik
masuk **tunggal**, bukan kesatuan.

**(3) Jangkaan priori #4 saya BETUL: `GB02_atau3 × X13` tidak layak.** +8.5413% akan
berpangkat **7 daripada 1,496**, dan **enam sel mengalahkannya** — termasuk dua kaki
tunggalnya sendiri (`N19 × X13` +11.285, `N75 × X13` +7.468). Kesatuan **mencairkan**.
Konfigurasi yang saya hantar ke produksi memang bukan yang terbaik.

**(4) Keluar mendominasi, seperti dijangka — tetapi bukan keluar yang saya sangka.**
Antara 139 yang lulus FDR: `X36` 40 · `X16` 27 · `X14` 12 · `X17` 11 · `X12` 9 · `X13` 6.
Jadi **`X36` (keluar selepas DUA tutup bawah ma50) dan `X16` (supertrend berbalik) memegang
48% slot**, sedangkan `X13` yang dikunci dalam produksi hanya 6. Dan keluarga masuk tersebar
luas (`PECAH` 21 · `RSI` 18 · `POLA` 17 · `TREND` 16) — **bukan** didominasi RSI/BB seperti
grid jarang cadangkan. Jangkaan priori #5 saya SALAH.

## Jangkaan priori lawan keputusan

| | jangkaan | berlaku | |
|---|---|---|---|
| 1 | 15–60 lulus empat syarat | **139** | **salah** (terlalu rendah) |
| 2 | `X13`/`X15`/`X17` > 60% slot | 22/40 dalam senarai; **hanya 16% daripada 139** | separa |
| 3 | `N19 × X13` pangkat 1 atau 2 | pangkat **4** mentah (#2 dalam senarai) | separa |
| 4 | `GB02_atau3 × X13` tiada dalam 10 teratas | pangkat **7** | **betul** |
| 5 | RSI dan BB mendominasi; MA/TREND/KEKUATAN hampir tiada | `PECAH` 21 > `RSI` 18; `TREND` 16, `KEKUATAN` 13, `MA` 8 | **salah** |
| 6 | `tanpa5` negatif pada majoriti | **7/40 positif**, median −2.442 | **betul** |

Dua betul, dua separa, dua salah.

## Had

- `tanpa5` ialah **lajur, bukan gate** (spec §3). 33 daripada 40 adalah **negatif** — jadi
  kelebihan majoriti senarai masih hidup dalam ekor kanan, dan `SETUP.md` masih terpakai.
  Hanya 7 yang tahan pemangkasan ekor: `N124×X15`, `N19×X13`, `N73×X13`, `N75×X13`,
  `N16×X13`, `N119×X13`, `N55×X13` — kesemuanya `X13` kecuali yang pertama.
- **Ini jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.** `KEPUTUSAN_AKHIR.md` sudah
  mengukur 724 konfigurasi portfolio dengan T1 = 0.
- 65 topeng dipilih daripada 147 oleh `status = DIUJI`; senarai ini **bersyarat** kepada itu.
- `p` menguji **lift** (salinan verbatim `step19`), bukan jangkaan mutlak. Syarat 1 dan 2
  mengendalikan jangkaan mutlak secara berasingan.
- Alam kajian `a02` tiada delist; alam dagangan ditapis SPUS. Berbeza.
- Paksi **PEGANG** sebahagiannya dalam 23 keluar (`X29` 10 bar, `X33` tutup sesi masuk, semua
  dihadkan ufuk 126 bar). `TMAX` sebagai paksi berasingan **belum diuji**.
- `N124` latih +3.064 lawan tahan +16.127: jurang 5× bermakna sebahagian besar kelebihannya
  khusus tingkap. Jangan saiz ia seperti +16%.

## Dua pepijat ditangkap sebelum sebarang nombor dilaporkan

1. **Larian pertama DIBUNUH** pada kelompok 4/8. Gelung Python saya membina 1,495 × ~1,500 =
   2.2 juta entri dict setiap kelompok, dan sesi dimulakan semula. Dibetulkan: tatasusunan
   padat 27 MB + `np.add.at`, checkpoint setiap kelompok, `setsid`.
2. **Ujian `p` menguji hipotesis yang SALAH.** Kawalan regresi gagal 46/46 metrik, kesemuanya
   pada `p`, sementara setiap metrik lain sepadan 5e-07. Saya ukur kedua-dua kaedah
   pengagregatan hari secara langsung — **identik** (|Δ| = 0.00e+00) — jadi penulisan semula
   bukan puncanya. Puncanya: `step19` menguji `H0: lift = 0` (purata harian tolak asas,
   ddof=1, ambang 20 hari, satu hujung `t.sf`); saya menguji `H0: jangkaan mutlak = 0` dua
   hujung. Blok itu kini salinan verbatim `step19`, dan kawalan regresi LULUS 46/46.
