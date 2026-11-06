# Lift setiap kaedah atas kolam Lejar Penuh

Dijana 2026-11-06 03:42 UTC oleh `standard/lift_kaedah.py` (Actions `analisis.yml`, selepas Lejar Penuh). Rekod analisis sahaja: tiada order, tiada wang sebenar.

Lejar bermula 2026-10-15; sesi terakhir 2026-11-04 (14 hari beli berbeza). **56,695 posisi** merentas **222 kaedah** (Mxx + Nxx), 22,784 tutup lorong 1 dan 33,911 terbuka ditanda-ke-pasaran pada tutup 20261104. Kos 0.2% setiap pusingan ditolak.

## Mengapa ukuran ini ada

`laporan/KAEDAH_TERBAIK.md` menguji posisi **DITUTUP** sahaja, dan peraturan keluar itu sendiri memilih posisi mana ditutup dahulu — jadi arah biasnya bertentangan antara dua jenis keluar: kaedah ber**sasaran untung** keluar awal bila MENANG (purata ditutup terlebih tinggi), kaedah ber**henti ketat** keluar awal bila RUGI (terlebih rendah). Ukuran di sini menilai SEMUA posisi, jadi penapisan itu hilang.

Tetapi purata tanda-ke-pasaran lawan **sifar** hanya mengukur arah pasaran dalam tingkap itu: **17 daripada 180** kaedah kelihatan positif pada ujian itu. Jadi lajur utama di bawah ialah **lift atas kolam**, dipadan ikut **hari beli × baldi hari pegang** — hari beli membuang arah pasaran, baldi hari pegang membuang kesan lebar henti. Asas setiap sel dikira **tinggal-satu-kaedah-keluar** supaya kaedah besar tidak mencairkan asasnya sendiri.

## Keputusan

| Ujian | Diuji | Lift positif bertahan BH-FDR | Lift negatif bertahan |
|---|---|---|---|
| Lawan sifar (tiada padanan) | 180 | 17 | 1 |
| Lift, padan hari beli | 180 | 0 | 1 |
| **Lift, padan hari beli × baldi hari pegang** | **180** | **0** | **0** |

**Tiada kaedah mempunyai lift positif yang bertahan BH-FDR** pada ujian utama. Jadual di bawah ialah senarai CALON, bukan pangkat yang boleh dipilih.

## 20 calon teratas ikut lift (padan hari beli × baldi hari pegang)

| # | Kaedah | n | % terbuka | Hari beli | Pul % | **Lift mata** | Lift/bulan % | Hari | Menang % | t | p | Ambang BH | BH | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `M118` Expansion Pivot (Cooper) | 57 | 77% | 14 | +3.31 | **+2.90** | +11.1 | 6 | 60 | +1.88 | 0.0823 | 0.0106 | tidak | BELUM CUKUP |
| 2 | `M33` Supertrend + SMA10 | 156 | 85% | 14 | +4.81 | **+2.63** | +6.9 | 8 | 74 | +2.22 | 0.0448 | 0.0058 | tidak | BELUM CUKUP |
| 3 | `M15` Break & Retest + Henti ATR | 238 | 55% | 14 | +3.08 | **+2.44** | +10.2 | 5 | 53 | +4.80 | 0.0003 | 0.0003 | tidak | BELUM CUKUP |
| 4 | `M80` Radge Saluran Purata Bergerak (MAC | 207 | 87% | 14 | +4.14 | **+2.26** | +5.9 | 8 | 71 | +2.45 | 0.0291 | 0.0044 | tidak | BELUM CUKUP |
| 5 | `M124` 'Last' Stochastic Technique (Chart | 293 | 66% | 14 | +2.67 | **+1.90** | +8.0 | 5 | 56 | +2.11 | 0.0551 | 0.0078 | tidak | BELUM CUKUP |
| 6 | `M105` Supertrend tulen | 266 | 79% | 14 | +3.72 | **+1.76** | +4.6 | 8 | 68 | +2.00 | 0.0669 | 0.0089 | tidak | BELUM CUKUP |
| 7 | `M92` CCI-50 | 417 | 53% | 14 | +2.10 | **+1.73** | +7.3 | 5 | 57 | +2.37 | 0.0340 | 0.0050 | tidak | BELUM CUKUP |
| 8 | `M73` ADX(5) > 40 + Julat Terkecil 6 Har | 627 | 22% | 14 | +0.17 | **+1.68** | +11.8 | 3 | 64 | +2.42 | 0.0309 | 0.0047 | tidak | BELUM CUKUP |
| 9 | `N57X16` ADX bangkit daripada <20 → keluar  | 186 | 89% | 14 | +3.62 | **+1.67** | +5.0 | 7 | 70 | +2.15 | 0.0506 | 0.0067 | tidak | BELUM CUKUP |
| 10 | `M106` DMI Wilder | 79 | 51% | 12 | +1.80 | **+1.67** | +7.0 | 5 | 52 | +1.08 | 0.3023 | 0.0236 | tidak | BELUM CUKUP |
| 11 | `M158` Doubly Adaptive Profit Targets | 273 | 77% | 14 | +3.04 | **+1.67** | +4.4 | 8 | 62 | +2.06 | 0.0597 | 0.0083 | tidak | BELUM CUKUP |
| 12 | `N57X36` ADX bangkit daripada <20 → keluar  | 186 | 92% | 14 | +3.62 | **+1.61** | +4.2 | 8 | 70 | +1.94 | 0.0740 | 0.0094 | tidak | BELUM CUKUP |
| 13 | `M93` Bollinger Kaedah II: %b + MFI | 217 | 78% | 14 | +3.13 | **+1.55** | +4.1 | 8 | 66 | +1.29 | 0.2183 | 0.0178 | tidak | BELUM CUKUP |
| 14 | `M18` EMA9/21 Pullback | 259 | 33% | 14 | +1.09 | **+1.46** | +10.2 | 3 | 39 | +3.29 | 0.0058 | 0.0017 | tidak | BELUM CUKUP |
| 15 | `N37X36` Gap and go → keluar selepas DUA tu | 50 | 76% | 11 | +2.43 | **+1.33** | +9.3 | 3 | 62 | +0.90 | 0.3905 | 0.0278 | tidak | BELUM CUKUP |
| 16 | `M10` EMA3 + CCI + MACD | 83 | 70% | 14 | +2.32 | **+1.27** | +3.8 | 7 | 51 | +0.84 | 0.4145 | 0.0281 | tidak | BELUM CUKUP |
| 17 | `M146` 3-Bar Momentum Pattern | 69 | 75% | 14 | +3.25 | **+1.25** | +6.6 | 4 | 68 | +1.16 | 0.2682 | 0.0211 | tidak | BELUM CUKUP |
| 18 | `N68X16` Bullish engulfing + EMA21 → keluar | 263 | 56% | 14 | +2.28 | **+1.15** | +6.0 | 4 | 60 | +1.91 | 0.0783 | 0.0097 | tidak | BELUM CUKUP |
| 19 | `M74` Lulus Baharu Trend Template Minerv | 65 | 40% | 14 | +1.22 | **+1.13** | +9.5 | 2 | 35 | +0.90 | 0.3824 | 0.0275 | tidak | BELUM CUKUP |
| 20 | `M160` Measured Move Up | 61 | 46% | 12 | +1.42 | **+1.13** | +7.9 | 3 | 44 | +0.94 | 0.3651 | 0.0269 | tidak | BELUM CUKUP |

Disekat kepada n ≥ 50 posisi. `Lift/bulan` = lift ÷ hari pegang × 21, iaitu lift setiap posisi jika modal dipusing penuh — ia **bukan** pulangan portfolio, dan setiap kali repo ini menukar jangkaan setiap-dagangan kepada portfolio sebenar ia jatuh ke bawah indeks (`REVERSE/KEPUTUSAN_AKHIR.md`: 0/24 lulus).

## Bila jadual ini boleh dipercayai

SD lift setiap hari beli (median dalam-kaedah): **3.34 mata**. Membanding 180 kaedah serentak (Bonferroni, anggaran konservatif bagi BH):

| Lift benar | Hari beli diperlukan | Setara bulan dagangan |
|---|---|---|
| 1 mata | 225 | ~11 |
| 2 mata | 57 | ~3 |
| 3 mata | 25 | ~2 |
| 4 mata | 15 | ~1 |

**Sekarang ada 14 hari beli.** Lajur `status` menanda `BELUM CUKUP` bagi kaedah dengan hari beli di bawah 57 (ambang lift 2 mata). Angka ini dikira setiap larian supaya ia tidak boleh hanyut dalam teks.

## Had

- Tingkap Lejar pendek, dan kaedah pegang-panjang mempunyai majoriti posisi masih terbuka. Lift mereka ialah untung kertas, bukan hasil.
- Paksi CARA dikunci `C01` (beli pada buka esok), jadi kecacatan henti hari-0 (`REVERSE/KOLAM_EKOR.md` §4a) hadir dalam setiap nombor.
- Alam Lejar tiada saham delist sebelum tingkap ini, jadi ia bukan alam titik-masa yang kausal (`REVERSE/ALAM.md`).
- Lift diukur atas kolam Lejar, bukan atas SPUS. Penanda aras pulangan yang sah ialah SPUS (`REVERSE/PENANDA_ARAS_SYARIAH.md`), dan itu perbandingan portfolio (`laporan/BANDING_SPUS.md`), bukan perbandingan setiap dagangan.
- Sasaran +10%/bulan: lihat `REVERSE/SASARAN.md`. Ia tidak dicapai oleh mana-mana baris di atas, dan lajur `Lift/bulan` tidak boleh dibaca sebagai pulangan bulanan.
