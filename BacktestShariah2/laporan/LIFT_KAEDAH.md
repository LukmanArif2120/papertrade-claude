# Lift setiap kaedah atas kolam Lejar Penuh

Dijana 2026-11-06 11:10 UTC oleh `standard/lift_kaedah.py` (Actions `analisis.yml`, selepas Lejar Penuh). Rekod analisis sahaja: tiada order, tiada wang sebenar.

Lejar bermula 2026-10-15; sesi terakhir 2026-11-05 (15 hari beli berbeza). **62,018 posisi** merentas **222 kaedah** (Mxx + Nxx), 26,016 tutup lorong 1 dan 36,002 terbuka ditanda-ke-pasaran pada tutup 20261105. Kos 0.2% setiap pusingan ditolak.

## Mengapa ukuran ini ada

`laporan/KAEDAH_TERBAIK.md` menguji posisi **DITUTUP** sahaja, dan peraturan keluar itu sendiri memilih posisi mana ditutup dahulu — jadi arah biasnya bertentangan antara dua jenis keluar: kaedah ber**sasaran untung** keluar awal bila MENANG (purata ditutup terlebih tinggi), kaedah ber**henti ketat** keluar awal bila RUGI (terlebih rendah). Ukuran di sini menilai SEMUA posisi, jadi penapisan itu hilang.

Tetapi purata tanda-ke-pasaran lawan **sifar** hanya mengukur arah pasaran dalam tingkap itu: **0 daripada 189** kaedah kelihatan positif pada ujian itu. Jadi lajur utama di bawah ialah **lift atas kolam**, dipadan ikut **hari beli × baldi hari pegang** — hari beli membuang arah pasaran, baldi hari pegang membuang kesan lebar henti. Asas setiap sel dikira **tinggal-satu-kaedah-keluar** supaya kaedah besar tidak mencairkan asasnya sendiri.

## Keputusan

| Ujian | Diuji | Lift positif bertahan BH-FDR | Lift negatif bertahan |
|---|---|---|---|
| Lawan sifar (tiada padanan) | 189 | 0 | 20 |
| Lift, padan hari beli | 189 | 0 | 2 |
| **Lift, padan hari beli × baldi hari pegang** | **189** | **5** | **10** |

**5 kaedah mempunyai lift positif yang bertahan BH-FDR** pada ujian utama. Senarai penuh di bawah; baca lajur `% terbuka` sebelum mempercayainya.

## 20 calon teratas ikut lift (padan hari beli × baldi hari pegang)

| # | Kaedah | n | % terbuka | Hari beli | Pul % | **Lift mata** | Lift/bulan % | Hari | Menang % | t | p | Ambang BH | BH | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `M15` Break & Retest + Henti ATR | 249 | 52% | 15 | +0.95 | **+2.52** | +10.6 | 5 | 45 | +4.81 | 0.0003 | 0.0005 | lulus | BELUM CUKUP |
| 2 | `M33` Supertrend + SMA10 | 186 | 83% | 15 | +1.58 | **+2.40** | +5.6 | 9 | 55 | +2.42 | 0.0295 | 0.0074 | tidak | BELUM CUKUP |
| 3 | `M80` Radge Saluran Purata Bergerak (MAC | 223 | 83% | 15 | +1.40 | **+2.26** | +5.3 | 9 | 56 | +2.40 | 0.0307 | 0.0077 | tidak | BELUM CUKUP |
| 4 | `M118` Expansion Pivot (Cooper) | 63 | 76% | 15 | +0.38 | **+2.25** | +7.9 | 6 | 46 | +1.79 | 0.0949 | 0.0159 | tidak | BELUM CUKUP |
| 5 | `M18` EMA9/21 Pullback | 269 | 28% | 15 | +0.30 | **+2.25** | +15.8 | 3 | 32 | +3.89 | 0.0016 | 0.0021 | lulus | BELUM CUKUP |
| 6 | `M73` ADX(5) > 40 + Julat Terkecil 6 Har | 641 | 15% | 15 | -0.79 | **+2.22** | +15.6 | 3 | 62 | +2.59 | 0.0214 | 0.0069 | tidak | BELUM CUKUP |
| 7 | `M146` 3-Bar Momentum Pattern | 72 | 68% | 15 | +1.57 | **+2.17** | +11.4 | 4 | 57 | +2.63 | 0.0197 | 0.0063 | tidak | BELUM CUKUP |
| 8 | `M158` Doubly Adaptive Profit Targets | 297 | 71% | 15 | +0.77 | **+2.10** | +5.2 | 8 | 46 | +2.09 | 0.0551 | 0.0108 | tidak | BELUM CUKUP |
| 9 | `M92` CCI-50 | 447 | 49% | 15 | -0.12 | **+1.93** | +8.1 | 5 | 43 | +3.09 | 0.0079 | 0.0045 | tidak | BELUM CUKUP |
| 10 | `M153` Range Leader | 1035 | 29% | 15 | -0.13 | **+1.84** | +9.7 | 4 | 44 | +3.53 | 0.0033 | 0.0040 | lulus | BELUM CUKUP |
| 11 | `M124` 'Last' Stochastic Technique (Chart | 317 | 58% | 15 | +0.04 | **+1.72** | +7.2 | 5 | 43 | +1.99 | 0.0663 | 0.0124 | tidak | BELUM CUKUP |
| 12 | `M32` Momentum Burst | 51 | 45% | 11 | -0.11 | **+1.66** | +7.0 | 5 | 31 | +0.69 | 0.5053 | 0.0315 | tidak | BELUM CUKUP |
| 13 | `M151` Outside Bar Failure | 80 | 55% | 14 | +0.22 | **+1.64** | +6.9 | 5 | 36 | +1.46 | 0.1669 | 0.0198 | tidak | BELUM CUKUP |
| 14 | `M106` DMI Wilder | 91 | 55% | 13 | -0.57 | **+1.63** | +6.8 | 5 | 40 | +1.72 | 0.1105 | 0.0175 | tidak | BELUM CUKUP |
| 15 | `M35` Pocket Pivot Morales & Kacher | 276 | 39% | 15 | -0.13 | **+1.54** | +10.8 | 3 | 27 | +2.90 | 0.0117 | 0.0048 | tidak | BELUM CUKUP |
| 16 | `M105` Supertrend tulen | 298 | 74% | 15 | +0.75 | **+1.50** | +3.9 | 8 | 51 | +1.85 | 0.0860 | 0.0151 | tidak | BELUM CUKUP |
| 17 | `M93` Bollinger Kaedah II: %b + MFI | 234 | 74% | 15 | +0.55 | **+1.49** | +3.9 | 8 | 49 | +1.59 | 0.1339 | 0.0188 | tidak | BELUM CUKUP |
| 18 | `M150` Trend Bar Failure (Brooks) | 77 | 60% | 14 | +0.30 | **+1.47** | +3.1 | 10 | 42 | +1.84 | 0.0880 | 0.0153 | tidak | BELUM CUKUP |
| 19 | `M70` Pecahan Hari Dalam | 348 | 21% | 15 | -0.12 | **+1.43** | +30.0 | 1 | 18 | +2.04 | 0.0606 | 0.0111 | tidak | BELUM CUKUP |
| 20 | `M116` 2/20 EMA Breakout (Landry) | 503 | 41% | 15 | -0.08 | **+1.42** | +3.0 | 10 | 50 | +2.00 | 0.0653 | 0.0122 | tidak | BELUM CUKUP |

Disekat kepada n ≥ 50 posisi. `Lift/bulan` = lift ÷ hari pegang × 21, iaitu lift setiap posisi jika modal dipusing penuh — ia **bukan** pulangan portfolio, dan setiap kali repo ini menukar jangkaan setiap-dagangan kepada portfolio sebenar ia jatuh ke bawah indeks (`REVERSE/KEPUTUSAN_AKHIR.md`: 0/24 lulus).

## Lift NEGATIF yang bertahan BH-FDR

| Kaedah | n | % terbuka | Lift mata | Hari | Menang % | t | p |
|---|---|---|---|---|---|---|---|
| `N55X13` BB + RSI + ADX>20 → keluar bila rs | 110 | 97% | -7.40 | 10 | 25 | -5.81 | 0.0000 |
| `N19X13` Bawah jalur BB + RSI<30 → keluar b | 137 | 100% | -7.28 | 9 | 26 | -3.80 | 0.0019 |
| `N73X13` Tutup bawah jalur bawah BB(20,2) → | 391 | 99% | -7.24 | 10 | 25 | -3.62 | 0.0028 |
| `N16X15` RSI2<10 tanpa penapis → ekori Chan | 568 | 100% | -6.15 | 10 | 31 | -3.70 | 0.0024 |
| `N75X15` RSI14 < 40 tanpa penapis → ekori C | 498 | 100% | -5.96 | 13 | 31 | -4.56 | 0.0004 |
| `N16X13` RSI2<10 tanpa penapis → keluar bil | 569 | 95% | -5.96 | 10 | 31 | -3.53 | 0.0033 |
| `N75X13` RSI14 < 40 tanpa penapis → keluar  | 498 | 94% | -5.82 | 13 | 31 | -4.55 | 0.0005 |
| `N119X15` 3 tutup turun berturut → ekori Cha | 823 | 100% | -4.32 | 12 | 39 | -3.67 | 0.0025 |
| `M81` Bensdorp Long Trend High Momentum | 331 | 65% | -3.46 | 12 | 23 | -4.91 | 0.0005 |
| `M90` Pring KST | 61 | 43% | -3.26 | 6 | 18 | -4.09 | 0.0013 |

Ini lebih berguna daripada senarai positif: `GB08` (penapis terbalik) ialah paksi yang memerlukan senarai buang, dan senarai ini dibina daripada data hadapan, bukan backtest.

## Bila jadual ini boleh dipercayai

SD lift setiap hari beli (median dalam-kaedah): **3.40 mata**. Membanding 189 kaedah serentak (Bonferroni, anggaran konservatif bagi BH):

| Lift benar | Hari beli diperlukan | Setara bulan dagangan |
|---|---|---|
| 1 mata | 234 | ~12 |
| 2 mata | 59 | ~3 |
| 3 mata | 26 | ~2 |
| 4 mata | 15 | ~1 |

**Sekarang ada 15 hari beli.** Lajur `status` menanda `BELUM CUKUP` bagi kaedah dengan hari beli di bawah 59 (ambang lift 2 mata). Angka ini dikira setiap larian supaya ia tidak boleh hanyut dalam teks.

## Had

- Tingkap Lejar pendek, dan kaedah pegang-panjang mempunyai majoriti posisi masih terbuka. Lift mereka ialah untung kertas, bukan hasil.
- Paksi CARA dikunci `C01` (beli pada buka esok), jadi kecacatan henti hari-0 (`REVERSE/KOLAM_EKOR.md` §4a) hadir dalam setiap nombor.
- Alam Lejar tiada saham delist sebelum tingkap ini, jadi ia bukan alam titik-masa yang kausal (`REVERSE/ALAM.md`).
- Lift diukur atas kolam Lejar, bukan atas SPUS. Penanda aras pulangan yang sah ialah SPUS (`REVERSE/PENANDA_ARAS_SYARIAH.md`), dan itu perbandingan portfolio (`laporan/BANDING_SPUS.md`), bukan perbandingan setiap dagangan.
- Sasaran +10%/bulan: lihat `REVERSE/SASARAN.md`. Ia tidak dicapai oleh mana-mana baris di atas, dan lajur `Lift/bulan` tidak boleh dibaca sebagai pulangan bulanan.
