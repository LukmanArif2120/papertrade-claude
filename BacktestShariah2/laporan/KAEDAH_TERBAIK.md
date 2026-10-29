# Kaedah mana terbaik buat masa sekarang?

Dijana 2026-10-29 09:00 UTC oleh `standard/kaedah_terbaik.py`. Rekod analisis sahaja.

Papan Penganalisis (`laporan/PENGANALISIS.md`) sudah membanding semua kaedah dan dijana semula setiap malam. Dokumen ini tidak mengulanginya — ia menjawab soalan yang mesti dijawab **dahulu** sebelum mana-mana pangkat boleh dipercayai.

**REVERSE menguji signal/indikator, BUKAN kaedah Mxx** (`CLAUDE.md`). Keputusan REVERSE tidak terpakai di sini. Ini populasi berasingan.

## 1. Jawapan pendek

**Tiada.** Daripada 38 kaedah yang mempunyai cukup posisi ditutup untuk diuji, **25 terbukti NEGATIF** pada BH-FDR q ≤ 0.05 dengan ralat piawai berkelompok ikut hari beli, dan **0 terbukti positif**.

Itu bukan bermakna semua kaedah buruk. Ia bermakna tingkap hadapan masih terlalu pendek, dan bahagian 2 menunjukkan mengapa pangkat yang anda lihat sekarang tidak boleh diguna.

## 2. Adakah pangkat backtest meramal prestasi hadapan?

Korelasi mentah jangkaan backtest lawan pulangan realisasi Papertrade C merentas **107 kaedah**: Spearman rho **-0.442**, p 0.0000.

Negatif. Dibaca mentah, itu bermakna kaedah dengan backtest LEBIH BAIK berprestasi LEBIH BURUK ke hadapan — dan itu akan menjadi dapatan yang besar. **Ia salah.**

Jangkaan backtest berkorelasi **+0.859** dengan hari pegang backtest — sepele: pegang lebih lama memberi pulangan lebih besar setiap dagangan. Dan dalam tingkap hadapan 3 minggu, kaedah pegang-panjang belum ada masa untuk berfungsi.

| Korelasi | rho | p |
|---|---|---|
| Mentah: backtest → realisasi | **-0.442** | 0.0000 |
| Separa, kawal lebar henti | -0.385 | 0.0001 |
| **Separa, kawal hari pegang** | **+0.099** | **0.3081** |

Mengawal hari pegang, korelasi bertukar daripada -0.442 kepada **+0.099** dan **tidak lagi signifikan** (p 0.308). Jadi tanda negatif itu **artifak panjang tingkap**, bukan bukti pangkat terbalik.

**Kesimpulan bahagian ini:** pangkat backtest tidak mempunyai kuasa ramalan yang boleh diukur pada data hadapan sekarang — tidak positif, tidak negatif. Jadi "kaedah teratas papan" bukan jawapan kepada "kaedah terbaik".

## 3. Ada kaedah yang positif secara boleh ukur?

Ujian: purata pulangan realisasi setiap kaedah dengan ≥ 20 posisi ditutup, t dengan ralat piawai **berkelompok ikut hari beli** (posisi hari sama bergerak bersama pasaran), BH-FDR q ≤ 0.05 merentas 38 kaedah yang diuji.

| Kaedah | n | Hari beli | Realisasi | Median | Menang | t | p | FDR | Backtest hari |
|---|---|---|---|---|---|---|---|---|---|
| `M36` Turtle 55/20 | 23 | 12 | -6.47% | -6.25% | 0% | -14.1 | 0.0000 | **lulus** | 29.6 |
| `M55` Guppy GMMA | 35 | 13 | -4.68% | -4.11% | 0% | -10.6 | 0.0000 | **lulus** | 28.2 |
| `M54` IBD Power Trend | 28 | 12 | -6.06% | -5.66% | 0% | -10.3 | 0.0000 | **lulus** | 36.8 |
| `M102` Stockbee SLTB | 66 | 15 | -3.07% | -2.37% | 2% | -8.4 | 0.0000 | **lulus** | 15.6 |
| `M14` Walking with the Whales | 86 | 15 | -2.00% | -1.56% | 0% | -8.2 | 0.0000 | **lulus** | 15.2 |
| `M89` Chande 65sma-3cc | 24 | 9 | -5.96% | -5.77% | 4% | -12.2 | 0.0000 | **lulus** | 26.0 |
| `M08` SMA20 + SMA200 | 50 | 14 | -3.61% | -4.12% | 10% | -7.9 | 0.0000 | **lulus** | 12.2 |
| `M15` Break & Retest + Henti ATR | 49 | 14 | -3.81% | -3.59% | 8% | -7.7 | 0.0000 | **lulus** | 12.2 |
| `M70` Pecahan Hari Dalam | 71 | 15 | -1.62% | -1.50% | 0% | -6.5 | 0.0000 | **lulus** | 10.3 |
| `M76` Undercut & Rally pada Low  | 20 | 9 | -3.13% | -3.01% | 5% | -9.1 | 0.0000 | **lulus** | 9.5 |

**25 daripada 38 kaedah terbukti negatif; 0 terbukti positif.** Jadual di atas 10 teratas ikut p — kesemuanya negatif.

Calon positif terbaik ialah `M03` BB Break + Divergence RSI: **+1.34%** atas 100 posisi ditutup merentas 14 hari beli, kadar menang 71%, median +1.62%, t +2.27, p 0.0410.

**Ia TIDAK bertahan pembetulan pelbagai ujian.** p 0.0410 melepasi ambang mentah 0.05 tetapi bukan ambang BH bagi pangkatnya merentas 38 kaedah. Menguji 38 kaedah dan melaporkan yang terbaik adalah cara paling biasa untuk menipu diri sendiri. Ia **calon untuk diperhatikan**, bukan jawapan.

## 4. Mengapa separuh papan belum boleh dinilai

| Kumpulan backtest | Kaedah | Posisi masih terbuka | Realisasi purata | Positif |
|---|---|---|---|---|
| pegang ≤ 10 hari | 20 | 53% | -1.71% | 2/12 |
| pegang 11–20 hari | 27 | 65% | -2.79% | 0/16 |
| pegang > 20 hari | 77 | 85% | -5.47% | 0/10 |

Kaedah pegang-panjang mempunyai **85% posisi masih terbuka**, jadi "realisasi" bagi mereka hanyalah himpunan posisi yang dihentikan awal — yang paling buruk daripada taburan. Angka itu bukan prestasi kaedah; ia prestasi hentinya dalam tiga minggu.

## 5. "Setiap kaedah ada sebab musabab daripada pakar" — ya, dan ini yang diukur

Premis itu betul: kaedah ini datang daripada pedagang yang berjaya dengannya. Tetapi repo ini sudah menguji versi mekanikalnya di luar sampel, dan hasilnya:

- Lulus S1–S4: **6** daripada 134 kaedah
- Lulus WFO 2023–2026: **22**
- Lulus AUTOTUNE 2000 saham AS 2013–2024: **0**
- Lulus **≥ 2 daripada 3**: **0**

Semakan 2000-saham-AS ialah yang paling menuntut kerana ia menguji kaedah LENGKAP (masuk + keluar + henti) pada alam dan tempoh yang tidak pernah dilihat. **0 kaedah melepasinya.**

**Had yang jujur, dan ia penting:** kaedah ini ialah **anggaran mekanikal** bagi kaedah yang asalnya mempunyai pertimbangan manusia — pemilihan saham, saiz, masa keluar, keadaan pasaran yang tidak dikodkan. `spec/SPEC_SEMUA_KAEDAH.md` menanda `FAIL ASAL` di tempat spec asal tidak dapat ditentukan. Jadi kegagalan di sini bermakna "versi mekanikal kami tidak berfungsi pada alam kami", **bukan** "pakar itu salah". Perbezaan itu nyata dan saya tidak boleh merapatkannya dengan data yang ada.

## 6. Bila pangkat kaedah boleh dipercayai

Sisihan piawai pulangan setiap posisi (median dalam-kaedah): **3.14 mata**.

| Untuk membezakan dua kaedah yang berbeza | Perlu posisi DITUTUP setiap kaedah |
|---|---|
| 3.0 mata setiap posisi | ~9 |
| 2.0 mata setiap posisi | ~19 |
| 1.0 mata setiap posisi | ~77 |
| 0.5 mata setiap posisi | ~309 |

Sekarang: median **10** posisi ditutup setiap kaedah, maksimum **101**. Jadi perbezaan bawah ~2 mata setiap posisi belum boleh dilihat bagi hampir semua kaedah.

## 7. Syor

1. **Jangan pilih kaedah sekarang.** Pangkat backtest tiada kuasa ramalan yang boleh diukur (bahagian 2), dan tiada kaedah positif yang bertahan pembetulan pelbagai ujian (bahagian 3).
2. **Betulkan kecacatan henti hari-0 dahulu.** `REVERSE/KOLAM_EKOR.md` §4a: 421 daripada 1,770 posisi dibeli dan dihentikan pada hari masuk dengan kadar menang 0.00% kerana paras henti terletak dalam julat intrabar hari masuk. Itu bukan prestasi kaedah, itu pepijat pelaksanaan, dan ia mencemari setiap pangkat di atas.
3. **Perhatikan kaedah pegang-pendek dahulu.** Hanya kumpulan ≤ 10 hari ada data yang hampir matang (53% masih terbuka lawan 85% bagi pegang-panjang). Pangkat pegang-panjang tidak bermakna sebelum satu tempoh pegang penuh berlalu.
4. **Baca semula selepas 6 bulan.** Papan dijana semula setiap malam tanpa kos. Jadual bahagian 6 memberi bilangan posisi yang diperlukan.

**Ia tidak akan mencapai +10%/bulan.** Kaedah teratas papan ikut skor sebulan memberi +3.40% dengan status BELUM CUKUP dan 0 posisi hadapan matang. Lihat `REVERSE/SASARAN.md`.
