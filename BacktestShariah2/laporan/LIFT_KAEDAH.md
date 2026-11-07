# Lift setiap kaedah atas kolam Lejar Penuh

Dijana 2026-11-07 14:17 UTC oleh `standard/lift_kaedah.py` (Actions `analisis.yml`, selepas Lejar Penuh). Rekod analisis sahaja: tiada order, tiada wang sebenar.

Lejar bermula 2026-10-15; sesi terakhir 2026-11-06 (16 hari beli berbeza). **64,010 posisi** merentas **223 kaedah** (Mxx + Nxx), 29,209 tutup lorong 1 dan 34,801 terbuka ditanda-ke-pasaran pada tutup 20261106. Kos 0.2% setiap pusingan ditolak.

## Mengapa ukuran ini ada

`laporan/KAEDAH_TERBAIK.md` menguji posisi **DITUTUP** sahaja, dan peraturan keluar itu sendiri memilih posisi mana ditutup dahulu — jadi arah biasnya bertentangan antara dua jenis keluar: kaedah ber**sasaran untung** keluar awal bila MENANG (purata ditutup terlebih tinggi), kaedah ber**henti ketat** keluar awal bila RUGI (terlebih rendah). Ukuran di sini menilai SEMUA posisi, jadi penapisan itu hilang.

Tetapi purata tanda-ke-pasaran lawan **sifar** hanya mengukur arah pasaran dalam tingkap itu: **0 daripada 191** kaedah kelihatan positif pada ujian itu. Jadi lajur utama di bawah ialah **lift atas kolam**, dipadan ikut **hari beli × baldi hari pegang** — hari beli membuang arah pasaran, baldi hari pegang membuang kesan lebar henti. Asas setiap sel dikira **tinggal-satu-kaedah-keluar** supaya kaedah besar tidak mencairkan asasnya sendiri.

## Keputusan

| Ujian | Diuji | Lift positif bertahan BH-FDR | Lift negatif bertahan |
|---|---|---|---|
| Lawan sifar (tiada padanan) | 191 | 0 | 41 |
| Lift, padan hari beli | 191 | 1 | 1 |
| **Lift, padan hari beli × baldi hari pegang** | **191** | **6** | **8** |

**6 kaedah mempunyai lift positif yang bertahan BH-FDR** pada ujian utama. Senarai penuh di bawah; baca lajur `% terbuka` sebelum mempercayainya.

## 20 calon teratas ikut lift (padan hari beli × baldi hari pegang)

| # | Kaedah | n | % terbuka | Hari beli | Pul % | **Lift mata** | Lift/bulan % | Hari | Menang % | t | p | Ambang BH | BH | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `M15` Break & Retest + Henti ATR | 254 | 46% | 16 | +0.59 | **+2.47** | +8.6 | 6 | 44 | +5.67 | 0.0000 | 0.0003 | lulus | BELUM CUKUP |
| 2 | `M73` ADX(5) > 40 + Julat Terkecil 6 Har | 644 | 15% | 16 | -0.64 | **+2.38** | +16.7 | 3 | 62 | +3.32 | 0.0047 | 0.0039 | tidak | BELUM CUKUP |
| 3 | `M153` Range Leader | 1040 | 18% | 16 | -0.35 | **+2.38** | +16.7 | 3 | 43 | +4.96 | 0.0002 | 0.0008 | lulus | BELUM CUKUP |
| 4 | `M100` Bulkowski Segi Empat & Segi Tiga M | 58 | 36% | 14 | -0.36 | **+2.34** | +7.0 | 7 | 40 | +1.41 | 0.1820 | 0.0183 | tidak | BELUM CUKUP |
| 5 | `M159` Heikin-Ashi Trend | 1397 | 21% | 16 | -0.67 | **+2.10** | +14.7 | 3 | 39 | +4.96 | 0.0002 | 0.0005 | lulus | BELUM CUKUP |
| 6 | `M18` EMA9/21 Pullback | 271 | 25% | 16 | -0.12 | **+2.08** | +14.5 | 3 | 31 | +4.04 | 0.0011 | 0.0018 | lulus | BELUM CUKUP |
| 7 | `M33` Supertrend + SMA10 | 195 | 82% | 16 | +0.93 | **+2.07** | +6.2 | 7 | 53 | +2.23 | 0.0414 | 0.0084 | tidak | BELUM CUKUP |
| 8 | `M03` BB Break + Divergence RSI | 324 | 13% | 16 | -1.01 | **+2.01** | +14.1 | 3 | 52 | +2.97 | 0.0096 | 0.0047 | tidak | BELUM CUKUP |
| 9 | `M92` CCI-50 | 458 | 42% | 16 | -0.54 | **+1.91** | +8.0 | 5 | 42 | +3.46 | 0.0035 | 0.0037 | lulus | BELUM CUKUP |
| 10 | `M116` 2/20 EMA Breakout (Landry) | 508 | 37% | 16 | -0.52 | **+1.86** | +4.9 | 8 | 48 | +2.26 | 0.0391 | 0.0079 | tidak | BELUM CUKUP |
| 11 | `M118` Expansion Pivot (Cooper) | 69 | 72% | 16 | -0.19 | **+1.79** | +7.5 | 5 | 46 | +1.62 | 0.1252 | 0.0139 | tidak | BELUM CUKUP |
| 12 | `M106` DMI Wilder | 100 | 50% | 14 | -0.69 | **+1.68** | +7.9 | 4 | 42 | +2.04 | 0.0623 | 0.0099 | tidak | BELUM CUKUP |
| 13 | `M146` 3-Bar Momentum Pattern | 76 | 64% | 16 | +0.70 | **+1.68** | +7.1 | 5 | 57 | +3.23 | 0.0056 | 0.0042 | tidak | BELUM CUKUP |
| 14 | `M124` 'Last' Stochastic Technique (Chart | 328 | 52% | 16 | -0.42 | **+1.62** | +6.8 | 5 | 42 | +2.09 | 0.0539 | 0.0094 | tidak | BELUM CUKUP |
| 15 | `M151` Outside Bar Failure | 81 | 46% | 15 | -0.43 | **+1.54** | +6.5 | 5 | 32 | +1.59 | 0.1345 | 0.0149 | tidak | BELUM CUKUP |
| 16 | `M35` Pocket Pivot Morales & Kacher | 281 | 32% | 16 | -0.59 | **+1.51** | +10.6 | 3 | 26 | +2.81 | 0.0131 | 0.0052 | tidak | BELUM CUKUP |
| 17 | `M158` Doubly Adaptive Profit Targets | 330 | 66% | 16 | +0.12 | **+1.44** | +3.8 | 8 | 43 | +1.71 | 0.1087 | 0.0126 | tidak | BELUM CUKUP |
| 18 | `M20` EMA10/15 Crossover + Sudut | 369 | 14% | 16 | -1.57 | **+1.42** | +9.9 | 3 | 29 | +2.45 | 0.0268 | 0.0060 | tidak | BELUM CUKUP |
| 19 | `M117` Landry Pullback (high 2 bulan) | 81 | 79% | 14 | -0.00 | **+1.38** | +5.8 | 5 | 41 | +0.77 | 0.4530 | 0.0293 | tidak | BELUM CUKUP |
| 20 | `M32` Momentum Burst | 51 | 37% | 11 | -0.77 | **+1.38** | +5.8 | 5 | 25 | +0.59 | 0.5690 | 0.0335 | tidak | BELUM CUKUP |

Disekat kepada n ≥ 50 posisi. `Lift/bulan` = lift ÷ hari pegang × 21, iaitu lift setiap posisi jika modal dipusing penuh — ia **bukan** pulangan portfolio, dan setiap kali repo ini menukar jangkaan setiap-dagangan kepada portfolio sebenar ia jatuh ke bawah indeks (`REVERSE/KEPUTUSAN_AKHIR.md`: 0/24 lulus).

## Lift NEGATIF yang bertahan BH-FDR

| Kaedah | n | % terbuka | Lift mata | Hari | Menang % | t | p |
|---|---|---|---|---|---|---|---|
| `N55X13` BB + RSI + ADX>20 → keluar bila rs | 127 | 97% | -5.62 | 10 | 28 | -4.45 | 0.0005 |
| `N16X15` RSI2<10 tanpa penapis → ekori Chan | 594 | 100% | -4.78 | 10 | 33 | -3.77 | 0.0019 |
| `N16X13` RSI2<10 tanpa penapis → keluar bil | 597 | 94% | -4.50 | 10 | 33 | -3.50 | 0.0032 |
| `N75X15` RSI14 < 40 tanpa penapis → ekori C | 544 | 100% | -4.21 | 14 | 33 | -4.04 | 0.0011 |
| `N75X13` RSI14 < 40 tanpa penapis → keluar  | 544 | 94% | -4.02 | 14 | 33 | -3.94 | 0.0013 |
| `N119X15` 3 tutup turun berturut → ekori Cha | 826 | 100% | -3.56 | 13 | 40 | -3.89 | 0.0014 |
| `M81` Bensdorp Long Trend High Momentum | 331 | 60% | -3.39 | 11 | 22 | -4.85 | 0.0005 |
| `M90` Pring KST | 64 | 41% | -2.93 | 6 | 16 | -3.74 | 0.0022 |

Ini lebih berguna daripada senarai positif: `GB08` (penapis terbalik) ialah paksi yang memerlukan senarai buang, dan senarai ini dibina daripada data hadapan, bukan backtest.

## Bila jadual ini boleh dipercayai

SD lift setiap hari beli (median dalam-kaedah): **3.29 mata**. Membanding 191 kaedah serentak (Bonferroni, anggaran konservatif bagi BH):

| Lift benar | Hari beli diperlukan | Setara bulan dagangan |
|---|---|---|
| 1 mata | 219 | ~11 |
| 2 mata | 55 | ~3 |
| 3 mata | 25 | ~2 |
| 4 mata | 14 | ~1 |

**Sekarang ada 16 hari beli.** Lajur `status` menanda `BELUM CUKUP` bagi kaedah dengan hari beli di bawah 55 (ambang lift 2 mata). Angka ini dikira setiap larian supaya ia tidak boleh hanyut dalam teks.

## Had

- Tingkap Lejar pendek, dan kaedah pegang-panjang mempunyai majoriti posisi masih terbuka. Lift mereka ialah untung kertas, bukan hasil.
- Paksi CARA dikunci `C01` (beli pada buka esok), jadi kecacatan henti hari-0 (`REVERSE/KOLAM_EKOR.md` §4a) hadir dalam setiap nombor.
- Alam Lejar tiada saham delist sebelum tingkap ini, jadi ia bukan alam titik-masa yang kausal (`REVERSE/ALAM.md`).
- Lift diukur atas kolam Lejar, bukan atas SPUS. Penanda aras pulangan yang sah ialah SPUS (`REVERSE/PENANDA_ARAS_SYARIAH.md`), dan itu perbandingan portfolio (`laporan/BANDING_SPUS.md`), bukan perbandingan setiap dagangan.
- Sasaran +10%/bulan: lihat `REVERSE/SASARAN.md`. Ia tidak dicapai oleh mana-mana baris di atas, dan lajur `Lift/bulan` tidak boleh dibaca sebagai pulangan bulanan.
