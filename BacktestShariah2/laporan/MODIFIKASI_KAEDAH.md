# Perlukah kaedah M diubah? — paksi MASUK · PEGANG · KELUAR, setiap kaedah

Dijana 2026-11-01 01:01 UTC oleh `standard/modifikasi_kaedah.py`. Rekod analisis sahaja: tiada order, tiada wang sebenar, tiada varian aktif ditukar.

Soalan pengguna: semua kaedah M datang daripada dapatan internet dan laman web; sepanjang papertrade berjalan, ada paksi yang perlu diubah untuk untung maksimum?

**Paksi sasaran yang dipilih pengguna: jangkaan setiap dagangan.** Setiap dakwaan di bawah ialah mata peratus setiap dagangan, BUKAN pulangan portfolio. Bahagian 7 menyatakan dengan tepat syor mana yang TIDAK akan bertukar menjadi untung portfolio.

## 1. Jawapan pendek

| Paksi | Perlu diubah? | Kesan terukur setiap dagangan | Sumber |
|---|---|---|---|
| **MASUK** | **Tidak** | lift maksimum pernah diukur +0.392 mata, dan 0/598 penapis ada lift positif | `REVERSE/SETUP.md`, `REVERSE/NXX.md`, `REVERSE/KOMBINASI.md` |
| **PEGANG** | **Ya — satu-satunya paksi dengan kesan besar** | **+4.36 mata** (pegang 60 hari lawan mesin kaedah), menang **74/74** kaedah swing | lengkung `pegang` registry, 589,187 dagangan backtest |
| **KELUAR** | **Arah ya, penalaan tidak** | pilihan keluar bernilai 4.997 mata (~12x paksi masuk), tetapi mesin keluar setiap kaedah hanya **+0.05 mata** median lawan pegang pasif | `REVERSE/NXX_KELUAR.md` + lengkung `pegang` |

Kiraan verdict merentas 134 kaedah:

| Paksi | UBAH | PERTIMBANG | KEKAL | KEKAL (disahkan) |
|---|---|---|---|---|
| MASUK | 0 | 17 | 117 | 0 |
| PEGANG | 18 | 9 | 107 | 0 |
| KELUAR | 60 | 24 | 29 | 21 |

## 2. Ukuran yang menjawab soalan: mesin keluar lawan pegang pasif

Lajur `pegang` registry memberi, bagi SETIAP dagangan varian aktif, pulangan beli-dan-pegang N hari dari entry YANG SAMA — mengabaikan henti, syarat keluar dan sasaran kaedah. Jadi perbezaan antara `avg` kaedah dan lengkung itu ialah nilai mesin keluar, diukur pada entry yang sama. Kaedah swing (hari pegang ≤ 30, n=74):

| Ufuk pegang | Jangkaan setiap dagangan | Setiap hari | Kaedah yang pegang pasif KALAHKAN |
|---|---|---|---|
| 5 hari | +0.36% | +0.0727% | 2 / 74 |
| 10 hari | +0.93% | +0.0934% | 20 / 74 |
| 15 hari | +1.43% | +0.0950% | 30 / 74 |
| 20 hari | +1.97% | +0.0984% | 45 / 74 |
| 30 hari | +2.86% | +0.0955% | 56 / 74 |
| 40 hari | +3.97% | +0.0992% | 68 / 74 |
| 60 hari | +6.14% | +0.1023% | 74 / 74 |
| **mesin kaedah sendiri** | **+1.77%** dalam 17.2 hari | **+0.1051%** | — |

Dua nombor yang mesti dibaca bersama:

1. **Jangkaan setiap dagangan: pegang 60 hari mengalahkan mesin kaedah pada 74 daripada 74 kaedah swing** (+4.36 mata purata). Tiada pengecualian.
2. **Kadar setiap hari hampir sama** (+0.1023% pegang-60 lawan +0.1051% mesin kaedah). Jadi keseluruhan kelebihan itu datang daripada memegang 3.5x lebih lama, **bukan** daripada apa-apa kelebihan.

Itu bermakna: jika ukuran anda ialah untung setiap dagangan, memanjangkan pegangan ialah lever terbesar yang ada dan ia berfungsi pada setiap kaedah tanpa pengecualian. Jika ukuran anda ialah pulangan atas modal, ia hampir tiada kesan: pulangan naik 3.46x (+1.77% -> +6.14%) sementara masa modal terikat naik 3.50x (17.2 -> 60 hari). Nisbah yang hampir SAMA itulah sebabnya kadar setiap hari tidak berubah. Bahagian 7.

## 3. Apa yang pengoptimum luar sampel pilih (W01 WFO, 2,096 pilihan)

16 suku 2023–2026, setiap suku memilih henti/keluar/tmax atas 3 tahun sebelumnya SAHAJA. Ujian arah bebas berat-sebelah: dalam setiap keluarga pilihan, adakah purata yang dipilih berbeza daripada jangkaan rawak seragam?

| Paksi | Pilihan | Dipilih | Seragam | Keputusan |
|---|---|---|---|---|
| henti | keluarga ATR (1.5–4.0) | **2.887x** | 2.75x | lebih LEBAR, t +4.79 p 2.0e-06 |
| henti | keluarga PCT (6–15%) | **10.84%** | 10.2% | lebih LEBAR, t +5.44 p 7.5e-08 |
| henti | keluarga LOW (1–10 bar) | 5.33 bar | 5.33 | tiada kecenderungan, p 0.97 |
| keluar | CHAN4 (ekori 4xATR) | 25.8% suku | 11.1% | **2.32x terlebih pilih** |
| keluar | CHAN2 / EMA10 (ekori ketat) | 1.5% / 1.2% | 11.1% | **0.13x / 0.11x terkurang pilih** |
| tmax | purata pangkat (10<21<42<63<tiada) | **3.681** | 3.0 | lebih PANJANG, t +25.8 p 4.6e-128 |

Arahnya sama pada ketiga-tiga paksi keluar: **henti lebih lebar, ekori lebih longgar, pegang lebih lama**. Itu sepadan tepat dengan `REVERSE/NXX_KELUAR.md`, yang mengukur 23 peraturan keluar atas 4.42 juta bar dan mendapati tiga terbaik semuanya "pegang sampai momentum habis" (`X13` keluar bila RSI>70 +4.350%, `X15` ekori Chandelier 4xATR +3.706%, `X17` keluar bila ADX<20 +1.855%) dan dua terburuk kedua-duanya memotong pegangan awal.

**TETAPI — dan ini yang menentukan syor saya:** versi WFO yang ditala setiap suku mengalahkan varian bekunya sendiri hanya **52 daripada 131 kaedah (39.7%)**, dengan purata delta CAGR **-6.4 mata** (t -3.63, p 0.0004). Jadi *arah* boleh dipercayai; *penalaan per-kaedah* tidak. `W01_LAPORAN.md` §5 mengesahkan sebabnya: tukar bajet carian Optuna mengubah CAGR dengan beza mutlak median 5.4 mata — pilihan parameter ialah hingar.

## 4. Sejarah modifikasi: ini bukan percubaan pertama

Registry set 431 sudah mengandungi **633 varian merentas 141 kaedah** (purata 4.5 setiap kaedah, maksimum 30): V0 sumber tulen, V1 spec dikunci, V2+ modifikasi. Varian aktif setiap kaedah ialah yang terbaik antara mereka. Lift dalam sampel atas V1 dikunci:

| Paksi diubah | n kaedah | Median lift CAGR | Positif |
|---|---|---|---|
| KELUAR sahaja | 77 | +4.8 mata | 55 (71%) |
| MASUK sahaja | 76 | +1.3 mata | 48 (63%) |

Kedua-dua baris dipilih dengan cara SAMA atas data SAMA, jadi perbandingan antara mereka bermakna walaupun kedua-duanya berat sebelah ke atas: **mengubah KELUAR memberi kira-kira 4x lift mengubah MASUK**. Itu konsisten dengan sebaran 4.997 mata lawan 0.392 mata yang `NXX_KELUAR.md` ukur pada alam yang jauh lebih besar.

Namun semakan luar sampel ke atas varian terpilih: lulus S1–S4 6, lulus WFO 22, lulus AUTOTUNE 2000 saham AS **0**, lulus ≥ 2 daripada 3 **0** (`laporan/PENGANALISIS.md`). Jadi lift dalam sampel itu tidak bertahan.

## 5. Sifat mekanikal daripada Lejar Penuh hadapan

16629 posisi, 10550 masih terbuka lorong 1, **6079 sudah keluar** merentas 110 kaedah. Set tertutup itu berat sebelah kepada keluar awal, jadi ia TIDAK diguna untuk pangkat prestasi — hanya untuk sifat mekanikal yang tidak sensitif kepada pemilihan itu.

| Ukuran | Nilai | Tafsiran |
|---|---|---|
| henti tercetus dalam ≤ 1 bar | **910 (15.0%)**, menang **0.00%** | kecacatan mekanikal: paras henti terletak dalam julat intrabar hari masuk (`REVERSE/KOLAM_EKOR.md` §4a) |
| jarak henti median: henti awal lawan lain | 1.96% lawan 7.95% | puncanya henti KETAT, bukan nasib |
| kos purata kecacatan itu | -2.58% setiap posisi terjejas | lebih kecil daripada jangkaan: henti ketat memotong kerugian kecil, jadi membuangnya mengubah purata hanya -0.042 mata (-2.824% -> -2.867%) |
| bahagian jumlah kerugian | 9.9% | besar dalam kiraan, kecil dalam kesan |
| MFE purata semua posisi | +3.24% | 95% posisi pernah untung semasa dipegang |

**Pembetulan kepada jangkaan saya sendiri:** `KAEDAH_TERBAIK.md` §7 meletakkan pembetulan henti hari-0 sebagai keutamaan #1. Pada data Lejar ia memang kecacatan nyata (menang 0.00% tidak mungkin berlaku secara semula jadi) tetapi **kosnya kecil** — posisi itu kehilangan -2.58% sahaja kerana hentinya ketat (1.96% median), jadi membuangnya TIDAK memperbaiki purata (-2.824% -> -2.867%). Ia perlu dibetulkan kerana ia mencemari pangkat, bukan kerana ia punca kerugian.

## 6. Jadual setiap kaedah (134)

`Data`: PENUH = ada W01 WFO dan ≥ 10 posisi Lejar tertutup · WFO = W01 sahaja · Lejar = Lejar sahaja · TIADA. `Kos mesin` = `avg` kaedah tolak pegang pasif pada ufuk sepadan (negatif = mesin keluar merugikan). `P60` = kelebihan pegang 60 hari setiap dagangan. `H0/1` = % posisi Lejar dihentikan dalam ≤ 1 bar. `WFO keluar` = pilihan modal merentas 16 suku luar sampel.

| ID | Kaedah | Data | Sasaran | tmax | Kos mesin | P60 | H0/1 | WFO henti z | WFO keluar | WFO tmax | MASUK | PEGANG | KELUAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `M01` | Bollinger Band + RSI | WFO | ADA | – | +0.33 | +6.1 | 0% | -0.2 | TIADA 11/16 | 10 | PERTIMBANG | KEKAL | UBAH |
| `M02` | MACD + SMA200 | PENUH | ADA | 20 | -0.22 | +5.3 | 30% | +0.6 | TIADA 7/16 | tiada | KEKAL | UBAH | UBAH |
| `M03` | BB Break + Divergence RSI | PENUH | ADA | – | +0.33 | +5.6 | 3% | +0.7 | TIADA 11/16 | 42 | KEKAL | KEKAL | UBAH |
| `M04` | BB Squeeze Breakout | PENUH | – | – | +1.76 | +1.6 | 0% | -0.7 | ASAL 6/16 | 63 | PERTIMBANG | KEKAL | KEKAL (disahkan) |
| `M05` | MACD Divergence + Pengesahan | WFO | – | – | – | – | 0% | +0.3 | ASAL 4/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M06` | Minervini VCP Breakout | WFO | – | – | -0.06 | +3.3 | 0% | +0.1 | TIADA 5/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M07` | Qullamaggie Breakout | WFO | – | – | -0.91 | +8.9 | – | +0.4 | CHAN4 11/16 | tiada | PERTIMBANG | KEKAL | UBAH |
| `M08` | SMA20 + SMA200 | PENUH | – | – | -0.35 | +5.4 | 16% | +0.2 | CHAN3 6/16 | tiada | KEKAL | KEKAL | UBAH |
| `M09` | Volumatic VIDYA Pivot Retest | PENUH | – | – | -0.67 | +2.5 | 10% | +0.3 | ASAL 8/16 | 63 | KEKAL | KEKAL | PERTIMBANG |
| `M10` | EMA3 + CCI + MACD | WFO | – | – | -0.11 | +0.8 | 33% | +0.4 | ASAL 9/16 | tiada | KEKAL | KEKAL | UBAH |
| `M11` | NR7 Breakout + Volume | PENUH | – | – | +0.78 | +2.9 | 7% | -0.1 | CHAN4 13/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M12` | Parabolic SAR | PENUH | – | – | -0.19 | +3.4 | 11% | +0.2 | CHAN4 9/16 | tiada | KEKAL | KEKAL | UBAH |
| `M13` | Garis Trend Action/Safety Line | PENUH | – | – | -0.14 | +5.5 | 28% | +0.5 | ASAL 8/16 | tiada | KEKAL | KEKAL | UBAH |
| `M14` | Walking with the Whales | PENUH | – | – | +0.10 | +3.6 | 35% | +0.1 | ASAL 5/16 | 21 | PERTIMBANG | KEKAL | UBAH |
| `M15` | Break & Retest + Henti ATR | PENUH | – | – | -0.19 | +5.4 | 4% | -0.6 | CHAN4 7/16 | 42 | KEKAL | KEKAL | PERTIMBANG |
| `M18` | EMA9/21 Pullback | PENUH | ADA | – | -0.07 | +4.8 | 38% | +0.0 | CHAN3 5/16 | 10 | PERTIMBANG | KEKAL | UBAH |
| `M19` | Sneaky Pivot (proksi harian) | PENUH | ADA | 20 | +0.20 | +5.6 | 6% | +0.2 | CHAN3 9/16 | tiada | KEKAL | UBAH | UBAH |
| `M20` | EMA10/15 Crossover + Sudut | PENUH | ADA | 20 | -0.03 | +4.8 | 21% | +0.5 | TIADA 7/16 | 21 | KEKAL | KEKAL | UBAH |
| `M21` | Marius 3 Persediaan (Pecahan+Jurang+Kesinamb | WFO | – | – | +1.07 | +12.2 | – | -0.1 | TIADA 6/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M22` | Qullamaggie Episodic Pivot | TIADA | – | – | +2.00 | +17.4 | – | – | – | – | KEKAL | KEKAL | KEKAL (disahkan) |
| `M23` | Breitstein Kapitulasi + Kesinambungan | PENUH | – | – | -0.06 | +4.7 | 64% | -0.1 | EMA21 4/16 | 21 | KEKAL | KEKAL | UBAH |
| `M24` | Rotasi Momentum ROC12 + SMA200 | WFO | – | – | – | – | – | -0.8 | EMA21 4/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M25` | VWAP Wave (proksi harian) | PENUH | – | 20 | -0.24 | +4.6 | 46% | +0.2 | CHAN4 6/16 | 63 | KEKAL | UBAH | UBAH |
| `M26` | Garis Trend Undur 3 Sentuhan + Pecahan | PENUH | ADA | – | +2.33 | -0.1 | 22% | +0.4 | ASAL 6/16 | 63 | KEKAL | KEKAL | UBAH |
| `M27` | Price Action 4 Tiang | PENUH | – | – | -0.11 | +5.1 | 7% | +0.1 | EMA10 7/16 | 63 | PERTIMBANG | KEKAL | KEKAL |
| `M28` | VWAP Separator + Kiss Pivot | PENUH | ADA | 10 | +0.02 | +8.4 | 18% | +0.1 | TIADA 14/16 | 21 | KEKAL | KEKAL | UBAH |
| `M29` | EMA3 + RSI75 + Stokastik | PENUH | – | – | -0.54 | +3.7 | 67% | -0.0 | ASAL 8/16 | 63 | KEKAL | KEKAL | UBAH |
| `M30` | BB Free Bar + Himpitan 50/2.5 | PENUH | – | – | +1.20 | +1.3 | 0% | -0.0 | CHAN4 6/16 | tiada | KEKAL | KEKAL | KEKAL (disahkan) |
| `M31` | Band Walk (BB 20/2) | WFO | – | – | +0.69 | +2.0 | 0% | +0.1 | CHAN4 5/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M32` | Momentum Burst | PENUH | – | – | +1.09 | +4.2 | 27% | +0.3 | CHAN4 8/16 | 63 | KEKAL | KEKAL | UBAH |
| `M33` | Supertrend + SMA10 | PENUH | – | – | -0.19 | +1.4 | 0% | +0.3 | ASAL 7/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M34` | Carter TTM Squeeze | PENUH | – | – | +0.78 | +1.2 | 0% | +0.4 | TIADA 6/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M35` | Pocket Pivot Morales & Kacher | PENUH | – | – | -0.17 | +4.0 | 38% | +0.6 | CHAN4 5/16 | 63 | KEKAL | KEKAL | UBAH |
| `M36` | Turtle 55/20 | PENUH | – | – | +1.07 | +1.9 | 6% | +0.7 | TIADA 7/16 | tiada | KEKAL | KEKAL | UBAH |
| `M37` | Weinstein Peringkat 2 | WFO | – | – | +1.53 | +1.1 | – | +0.1 | CHAN4 7/16 | 63 | KEKAL | KEKAL | KEKAL |
| `M38` | Darvas Kotak | WFO | – | – | – | – | – | +0.3 | ASAL 3/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M39` | Radge Pecahan Bollinger 100 hari | WFO | – | – | – | – | 17% | +0.7 | CHAN4 8/16 | tiada | KEKAL | KEKAL | UBAH |
| `M40` | Clenow Stocks on the Move | TIADA | – | – | -1.05 | +7.3 | – | – | – | – | KEKAL | KEKAL | PERTIMBANG |
| `M41` | FW Penyatuan Mingguan | WFO | – | – | – | – | – | +0.2 | CHAN4 8/16 | tiada | KEKAL | KEKAL | PERTIMBANG |
| `M44` | Tapak Rata IBD | WFO | – | – | -0.27 | +1.2 | 0% | +0.2 | CHAN4 9/16 | tiada | PERTIMBANG | KEKAL | UBAH |
| `M45` | High 52 Minggu (George & Hwang) | TIADA | – | 126 | – | – | – | – | – | – | KEKAL | KEKAL | KEKAL |
| `M46` | Jurang Naik Boleh Beli (Buyable Gap Up) | WFO | – | – | +0.82 | +2.6 | 75% | -0.5 | TIADA 7/16 | tiada | KEKAL | KEKAL | UBAH |
| `M47` | Holy Grail Raschke | WFO | ADA | – | -0.00 | +5.5 | 0% | -0.2 | ASAL 6/16 | 63 | PERTIMBANG | KEKAL | UBAH |
| `M48` | Cooper 1-2-3-4 | WFO | – | – | +0.35 | +2.6 | 0% | +0.7 | CHAN3 6/16 | 42 | KEKAL | KEKAL | PERTIMBANG |
| `M49` | Ichimoku (Tutup Atas Awan + Tenkan Silang Ki | PENUH | – | – | +1.52 | +0.8 | 43% | +0.1 | ASAL 4/16 | tiada | KEKAL | KEKAL | UBAH |
| `M50` | Elder Triple Screen | PENUH | – | – | +0.00 | +3.8 | 32% | +0.7 | CHAN4 7/16 | 63 | PERTIMBANG | KEKAL | UBAH |
| `M51` | O'Neil Cawan & Pemegang | WFO | – | – | -0.26 | +4.2 | – | -0.1 | TIADA 7/16 | 42 | KEKAL | KEKAL | UBAH |
| `M52` | Radge Weekend Trend Trader | WFO | – | – | +1.33 | +0.9 | – | -0.3 | CHAN4 5/16 | 42 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M54` | IBD Power Trend | PENUH | – | – | +0.79 | +0.7 | 3% | -0.0 | ASAL 8/16 | tiada | PERTIMBANG | KEKAL | KEKAL (disahkan) |
| `M55` | Guppy GMMA | PENUH | – | – | +0.82 | +1.7 | 29% | +0.1 | CHAN4 8/16 | 42 | PERTIMBANG | KEKAL | UBAH |
| `M56` | Gray & Vogel Momentum Lancar (FIP) | WFO | – | – | – | – | – | +0.1 | EMA21 7/16 | 63 | KEKAL | KEKAL | KEKAL |
| `M57` | Landry Trend Knockout (TKO) | PENUH | – | – | +0.33 | +4.2 | 42% | -0.4 | CHAN4 8/16 | 42 | KEKAL | KEKAL | UBAH |
| `M59` | Anjakan Julat RSI | WFO | – | – | -0.34 | +1.7 | 0% | +0.0 | TIADA 7/16 | 21 | KEKAL | KEKAL | UBAH |
| `M64` | O'Neil Tiga Minggu Ketat | WFO | – | – | +0.01 | +2.6 | 0% | +0.2 | TIADA 8/16 | 63 | KEKAL | KEKAL | PERTIMBANG |
| `M66` | IBD Undur Pertama ke Purata 50 Hari | PENUH | – | – | +0.33 | +4.2 | 18% | +0.3 | ASAL 5/16 | tiada | KEKAL | KEKAL | PERTIMBANG |
| `M67` | Rayner Teo: Ujian Ketiga pada Purata 50 | WFO | – | – | -0.05 | +2.8 | 20% | +0.7 | CHAN4 6/16 | 63 | KEKAL | KEKAL | UBAH |
| `M68` | Kell Base n' Break | WFO | – | – | -0.13 | +1.4 | 100% | -0.1 | CHAN4 8/16 | 42 | KEKAL | KEKAL | UBAH |
| `M70` | Pecahan Hari Dalam | PENUH | – | – | +0.42 | +3.6 | 66% | +0.7 | CHAN4 10/16 | tiada | PERTIMBANG | KEKAL | UBAH |
| `M73` | ADX(5) > 40 + Julat Terkecil 6 Hari | PENUH | – | – | – | – | 0% | +0.1 | CHAN4 8/16 | 21 | PERTIMBANG | KEKAL | PERTIMBANG |
| `M74` | Lulus Baharu Trend Template Minervini | PENUH | – | – | +0.58 | +4.7 | 52% | -0.1 | ASAL 6/16 | 42 | KEKAL | KEKAL | UBAH |
| `M76` | Undercut & Rally pada Low Penting | PENUH | – | – | +0.11 | +7.0 | 19% | -0.3 | TIADA 8/16 | 63 | KEKAL | KEKAL | UBAH |
| `M77` | Undercut & Rally pada Purata Bergerak (MAU&R | PENUH | – | – | +1.70 | +2.3 | 29% | +0.7 | CHAN4 9/16 | 42 | KEKAL | KEKAL | UBAH |
| `M78` | Alvarez Pecahan Mingguan DTAYS | PENUH | – | – | -1.90 | +3.9 | 0% | +0.4 | SMA50 4/16 | tiada | KEKAL | KEKAL | PERTIMBANG |
| `M79` | Radge: 20% Flipper | PENUH | – | – | -7.10 | +7.1 | 11% | -0.0 | CHAN4 7/16 | 10 | KEKAL | KEKAL | UBAH |
| `M80` | Radge Saluran Purata Bergerak (MAC) | PENUH | – | – | – | – | 0% | -0.2 | CHAN4 7/16 | tiada | KEKAL | KEKAL | PERTIMBANG |
| `M81` | Bensdorp Long Trend High Momentum | PENUH | – | – | – | – | 0% | -0.2 | ASAL 6/16 | 42 | KEKAL | KEKAL | KEKAL |
| `M82` | Arthur Hill Rotasi Sasaran 10% | PENUH | – | – | -0.41 | +1.6 | 0% | +0.1 | SMA50 6/16 | 21 | PERTIMBANG | KEKAL | PERTIMBANG |
| `M84` | Jarak purata bergerak MAD 21/200 | WFO | – | – | +0.07 | +4.7 | – | +0.3 | TIADA 7/16 | 63 | KEKAL | KEKAL | PERTIMBANG |
| `M87` | IBD Tapak Menaik | WFO | – | – | +1.27 | +2.1 | 0% | +0.4 | CHAN4 5/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M88` | O'Neil Shakeout +3 | PENUH | – | – | +0.12 | +4.1 | 0% | -0.0 | SMA20 9/16 | 21 | KEKAL | KEKAL | KEKAL |
| `M89` | Chande 65sma-3cc | PENUH | – | – | -0.51 | +3.9 | 40% | +0.6 | ASAL 12/16 | tiada | KEKAL | KEKAL | UBAH |
| `M90` | Pring KST | PENUH | – | – | +0.50 | +2.1 | 12% | -0.6 | CHAN3 9/16 | tiada | PERTIMBANG | KEKAL | UBAH |
| `M91` | Stochastic Pop (Bernstein/Steckler) | WFO | – | – | +0.03 | +5.0 | 0% | -0.4 | ASAL 9/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M92` | CCI-50 | PENUH | – | – | +0.08 | +4.7 | 6% | -0.1 | CHAN4 5/16 | 21 | KEKAL | KEKAL | KEKAL |
| `M93` | Bollinger Kaedah II: %b + MFI | PENUH | – | – | – | – | 14% | -0.1 | CHAN3 10/16 | 42 | KEKAL | KEKAL | UBAH |
| `M94` | Pecutan Momentum (Chen, Yu & Wang) | WFO | – | 126 | – | – | – | +0.4 | CHAN4 14/16 | 63 | KEKAL | UBAH | PERTIMBANG |
| `M95` | Nisbah Kebaharuan High 52 Minggu (Bhootra &  | PENUH | – | – | +0.93 | +2.5 | 0% | -0.3 | CHAN4 5/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M96` | Momo India: Ranking Sharpe 3/6/12 bulan | WFO | – | – | +0.07 | +1.4 | – | +0.5 | ASAL 7/16 | 42 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M99` | Three Line Break | PENUH | – | – | +0.18 | +3.9 | 24% | -0.6 | CHAN4 6/16 | 63 | PERTIMBANG | KEKAL | UBAH |
| `M100` | Bulkowski Segi Empat & Segi Tiga Menaik | PENUH | ADA | – | +0.35 | +0.9 | 0% | +0.5 | SMA50 6/16 | 42 | KEKAL | KEKAL | UBAH |
| `M101` | Bulkowski: Tiga lembah menaik | WFO | – | – | +2.50 | +0.6 | 0% | -0.3 | CHAN4 8/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M102` | Stockbee SLTB | PENUH | – | – | +0.39 | +3.6 | 42% | +1.2 | SMA20 11/16 | 42 | PERTIMBANG | KEKAL | UBAH |
| `M104` | High Tight Flag / Power Play | WFO | – | – | +2.07 | +6.8 | – | -0.3 | CHAN4 9/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M105` | Supertrend tulen | PENUH | – | – | -0.20 | +2.8 | 0% | +0.6 | ASAL 5/16 | 42 | KEKAL | KEKAL | UBAH |
| `M106` | DMI Wilder | PENUH | – | – | +0.32 | +4.6 | 0% | -0.2 | TIADA 7/16 | 63 | KEKAL | KEKAL | PERTIMBANG |
| `M107` | Golden Cross SMA50/200 | WFO | – | – | – | – | 0% | -0.1 | ASAL 12/16 | tiada | KEKAL | KEKAL | KEKAL (disahkan) |
| `M111` | Sistem Volatiliti Wilder | PENUH | – | – | +0.10 | +2.7 | 18% | +0.0 | ASAL 8/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M115` | Bow Tie (Landry) | WFO | – | 42 | -0.12 | +3.9 | 14% | +1.2 | ASAL 7/16 | 42 | KEKAL | PERTIMBANG | UBAH |
| `M116` | 2/20 EMA Breakout (Landry) | PENUH | – | 10 | -0.11 | +4.3 | 1% | -0.3 | CHAN4 7/16 | tiada | KEKAL | UBAH | PERTIMBANG |
| `M117` | Landry Pullback (high 2 bulan) | WFO | – | – | – | – | 0% | +0.3 | ASAL 7/16 | tiada | KEKAL | KEKAL | KEKAL (disahkan) |
| `M118` | Expansion Pivot (Cooper) | WFO | – | – | -0.60 | +2.8 | 11% | +0.8 | CHAN4 6/16 | tiada | KEKAL | KEKAL | UBAH |
| `M119` | 180 Bullish (Cooper) | PENUH | – | 42 | -0.03 | +3.2 | 18% | +0.8 | ASAL 5/16 | 63 | KEKAL | UBAH | UBAH |
| `M120` | Reversal New Highs | WFO | – | – | +1.48 | +0.6 | 0% | +0.2 | ASAL 6/16 | tiada | KEKAL | KEKAL | KEKAL (disahkan) |
| `M121` | High 2 bull flag (Brooks) | WFO | – | 63 | -0.59 | +1.5 | – | +1.1 | ASAL 10/16 | tiada | KEKAL | UBAH | PERTIMBANG |
| `M122` | Moving Momentum (ChartSchool) | PENUH | – | 42 | +0.61 | +3.4 | 19% | -0.8 | EMA10 4/16 | 21 | KEKAL | KEKAL | KEKAL |
| `M123` | CCI Correction (Lambert, ChartSchool) | PENUH | – | – | +0.44 | +4.5 | 37% | -0.2 | CHAN3 7/16 | 63 | KEKAL | KEKAL | UBAH |
| `M124` | Last' Stochastic Technique (ChartSchool) | PENUH | – | 63 | -0.37 | +3.8 | 12% | +0.2 | CHAN3 5/16 | 10 | KEKAL | KEKAL | UBAH |
| `M125` | 2-Bar Breakout | PENUH | – | – | – | – | 5% | +0.1 | CHAN4 6/16 | 42 | KEKAL | KEKAL | KEKAL |
| `M126` | Hidden Smash Day (beli, Larry Williams) | WFO | – | – | +2.81 | -1.2 | 0% | +1.0 | SMA50 7/16 | tiada | KEKAL | KEKAL | PERTIMBANG |
| `M127` | Slingshot Bullish | PENUH | – | – | +2.04 | +1.3 | 25% | -1.0 | ASAL 6/16 | tiada | KEKAL | KEKAL | UBAH |
| `M128` | Inventory Retracement Bar (IRB, Rob Hoffman) | PENUH | – | 42 | +0.00 | +4.5 | 5% | +0.6 | CHAN3 7/16 | 42 | KEKAL | PERTIMBANG | UBAH |
| `M129` | Wick Play | WFO | – | 63 | -0.44 | +2.0 | – | +0.5 | ASAL 7/16 | tiada | KEKAL | UBAH | KEKAL |
| `M130` | 多方炮 (dua lilin hijau mengapit satu merah) | WFO | – | – | – | – | – | +0.3 | ASAL 10/16 | 42 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M131` | Ross Hook (Joe Ross) | PENUH | – | 63 | +0.02 | +2.4 | 14% | +0.7 | ASAL 5/16 | 63 | KEKAL | UBAH | UBAH |
| `M132` | Ascending Scallop (Bulkowski) | WFO | – | 42 | +0.42 | +1.5 | 0% | +0.2 | ASAL 6/16 | 63 | KEKAL | UBAH | KEKAL |
| `M133` | Bull Hook (Crabel) | PENUH | – | 21 | -0.33 | +4.0 | 8% | +0.1 | SMA50 7/16 | tiada | KEKAL | UBAH | UBAH |
| `M134` | First Kiss After Daylight (Landry) | WFO | – | – | +1.94 | +0.4 | 20% | +0.4 | CHAN4 10/16 | tiada | KEKAL | KEKAL | UBAH |
| `M135` | 3rd Watch | WFO | – | 63 | +0.05 | +2.4 | – | +0.6 | EMA21 5/16 | 21 | KEKAL | KEKAL | PERTIMBANG |
| `M136` | Short/Intermediate-term Low (Larry Williams) | PENUH | – | – | – | – | 17% | -0.1 | CHAN3 8/16 | tiada | KEKAL | KEKAL | UBAH |
| `M137` | Livermore System | WFO | – | – | +1.48 | +0.5 | 11% | -0.4 | ASAL 7/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M138` | 直升机空中加油 (Helikopter isi minyak di udara) | WFO | – | 63 | -1.18 | +1.9 | – | -0.0 | CHAN3 5/16 | 42 | KEKAL | PERTIMBANG | PERTIMBANG |
| `M139` | 均线首次粘合向上发散 (MA berhimpun kali pertama, berki | WFO | – | 21 | -0.00 | +3.2 | 0% | +1.0 | ASAL 7/16 | 42 | KEKAL | PERTIMBANG | KEKAL |
| `M140` | 猎豹出击 (Serangan Cheetah) | WFO | – | 63 | -0.40 | +6.3 | 25% | -0.3 | ASAL 7/16 | tiada | KEKAL | UBAH | UBAH |
| `M141` | First Thrust (Landry) | WFO | – | 63 | -0.26 | +1.5 | 0% | +0.3 | ASAL 10/16 | tiada | KEKAL | UBAH | KEKAL |
| `M142` | Pecahan volum dari dasar (底部放量) | WFO | – | – | +0.93 | +0.7 | – | +0.7 | ASAL 5/16 | 63 | KEKAL | KEKAL | KEKAL |
| `M143` | 장대양봉 이후 눌림목 / 5일선 매매 (Undur ke MA5 selepas l | WFO | – | 21 | +0.23 | +2.6 | 0% | +0.2 | TIADA 10/16 | 42 | KEKAL | PERTIMBANG | KEKAL |
| `M144` | Screw Bar | WFO | – | – | +2.93 | +7.0 | 0% | -0.2 | CHAN4 11/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M145` | Yum-Yum Continuation | PENUH | – | – | – | – | 0% | -0.2 | ASAL 9/16 | 63 | KEKAL | KEKAL | KEKAL (disahkan) |
| `M146` | 3-Bar Momentum Pattern | WFO | – | – | +1.32 | +2.0 | 43% | -0.1 | ASAL 5/16 | tiada | KEKAL | KEKAL | UBAH |
| `M147` | Improved Three-Bar Pullback | WFO | – | – | – | – | 0% | +0.9 | ASAL 8/16 | 63 | KEKAL | KEKAL | KEKAL |
| `M148` | Natural Number Method | PENUH | – | 42 | -0.17 | +5.3 | 14% | -0.2 | ASAL 4/16 | 42 | KEKAL | PERTIMBANG | PERTIMBANG |
| `M149` | 3-Step Pullback | PENUH | – | – | – | – | 9% | +0.9 | ASAL 7/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M150` | Trend Bar Failure (Brooks) | WFO | – | 21 | -0.41 | +4.7 | 0% | +0.7 | CHAN3 8/16 | tiada | KEKAL | UBAH | UBAH |
| `M151` | Outside Bar Failure | PENUH | – | – | +0.24 | +2.0 | 21% | +0.3 | CHAN4 7/16 | tiada | KEKAL | KEKAL | UBAH |
| `M152` | Spike & Ledge | WFO | – | 42 | -0.17 | +1.6 | – | -0.0 | ASAL 8/16 | 63 | KEKAL | UBAH | KEKAL (disahkan) |
| `M153` | Range Leader | PENUH | – | 10 | -0.19 | +5.6 | 0% | +0.1 | CHAN4 6/16 | 42 | KEKAL | UBAH | KEKAL |
| `M154` | HOLP (High of Low Period) | PENUH | – | 42 | -0.22 | +4.3 | 15% | +0.4 | ASAL 8/16 | 63 | KEKAL | UBAH | PERTIMBANG |
| `M155` | Market Cycle Strategy | PENUH | – | 21 | -0.10 | +5.9 | 4% | -0.2 | CHAN4 8/16 | 42 | KEKAL | PERTIMBANG | PERTIMBANG |
| `M156` | Single Penetration (DiNapoli) | PENUH | – | 10 | -0.05 | +3.8 | 0% | +0.1 | SMA50 9/16 | 10 | KEKAL | PERTIMBANG | KEKAL |
| `M157` | Consolidation Pivot Breakout (versi angka) | WFO | – | – | – | – | – | +0.2 | ASAL 7/16 | tiada | KEKAL | KEKAL | KEKAL (disahkan) |
| `M158` | Doubly Adaptive Profit Targets | PENUH | – | – | +0.36 | +2.5 | 0% | +0.4 | ASAL 6/16 | tiada | KEKAL | KEKAL | KEKAL |
| `M159` | Heikin-Ashi Trend | PENUH | – | 10 | -0.05 | +5.8 | 1% | +1.0 | CHAN3 4/16 | 10 | KEKAL | PERTIMBANG | PERTIMBANG |
| `M160` | Measured Move Up | PENUH | – | 42 | +0.10 | +5.2 | 36% | +0.1 | ASAL 6/16 | 63 | KEKAL | UBAH | UBAH |
| `M161` | EMA 10/21 + Supertrend (10,3) | PENUH | – | – | -0.03 | +3.5 | 1% | +0.6 | CHAN2 4/16 | 63 | KEKAL | KEKAL | PERTIMBANG |

## 6b. Senarai tindakan, dikumpul ikut perubahan

Setiap kumpulan ialah SATU perubahan yang terpakai kepada senarai kaedah itu. Dikumpul begini kerana bahagian 3 menunjukkan penalaan per-kaedah kalah: yang boleh diuji ialah satu perubahan seragam atas banyak kaedah, bukan 134 keputusan berasingan.

### Buang sasaran JARAK-TETAP (gandaan R / peratus) — 1 kaedah

Bukti membezakan DUA jenis sasaran, dan hanya satu terbukti merugikan. **Sasaran jarak-tetap merugikan**: `NXX_KELUAR.md` `X10` sasaran 2% menang 94.1% dengan jangkaan -0.023%, `X27` sasaran 3% +0.233%, `KOMBINASI.md` `X1` sasaran 1xATR menang 61.1% dengan jangkaan -0.281% (asas tanpa sasaran +2.595%). **Keluar atas kekuatan berasaskan penunjuk adalah TERBAIK**: `X13` keluar bila rsi14>70 memberi +4.350%, nombor 1 daripada 23. Maka kaedah dengan sasaran jarak-tetap (nR, +n%) patut membuangnya; kaedah dengan sasaran PARAS-BERGERAK (jalur BB atas, SMA30, paras swing) lebih hampir kepada `X13` dan mesti diuji, bukan diandaikan salah. Dalam Lejar, keluar-sasaran merealisasi +5.34% sedangkan MFEnya +7.33% — sasaran yang dipakai sekarang memotong 1.99 mata, tetapi angka itu bersyarat pada sasaran tercapai.

`M02`

### Sasaran PARAS-STRUKTUR — uji, jangan andaikan salah — 9 kaedah

Sasaran kaedah ini ialah paras harga (jalur BB atas, SMA30, VWAP, ATH, tinggi 20 hari, projeksi gerakan terukur), bukan jarak tetap daripada harga masuk. Bukti yang menghukum sasaran dalam `NXX_KELUAR`/`KOMBINASI` semuanya mengenai jarak TETAP; keluar berasaskan paras/penunjuk justeru yang TERBAIK (`X13` rsi14>70 +4.350%, `X12` jalur bawah BB +0.961%, `X05` jalur tengah BB +0.030%). Jadi kumpulan ini masuk `Z1` sebagai lengan berasingan dan keputusannya dilapor berasingan.

`M01`, `M03`, `M18`, `M19`, `M20`, `M26`, `M28`, `M47`, `M100`

### Buang atau panjangkan had masa (tmax) — 25 kaedah

WFO luar sampel memilih tmax panjang atau tiada had pada 81.5% suku (purata pangkat 3.681 lawan 3.0 seragam, t +25.8 p 4.6e-128).

`M02`, `M19`, `M25`, `M94`, `M115`, `M116`, `M119`, `M121`, `M128`, `M129`, `M131`, `M132`, `M133`, `M138`, `M139`, `M140`, `M141`, `M143`, `M148`, `M150`, `M152`, `M153`, `M154`, `M155`, `M160`

### Tukar syarat keluar kepada ekori Chandelier — 33 kaedah

Mod luar sampel kaedah ini ialah ekori Chandelier pada >= 7 daripada 16 suku. `NXX_KELUAR.md` `X15` (Chandelier 4xATR) ialah keluar kedua terbaik daripada 23, +3.706% tanpa apa-apa penapis masuk.

`M07`, `M11`, `M12`, `M15`, `M19`, `M32`, `M37`, `M39`, `M41`, `M44`, `M50`, `M55`, `M57`, `M68`, `M70`, `M73`, `M77`, `M79`, `M80`, `M90`, `M93`, `M94`, `M101`, `M104`, `M116`, `M123`, `M128`, `M134`, `M136`, `M144`, `M150`, `M151`, `M155`

### Buang syarat keluar sama sekali (henti sahaja) — 8 kaedah

Mod luar sampel ialah TIADA pada >= 7 suku, dan kaedah ini ada syarat keluar yang dipakai sekarang.

`M36`, `M46`, `M51`, `M59`, `M64`, `M76`, `M84`, `M106`

### Lebarkan henti — 29 kaedah

Dalam keluarga ATR dan PCT, henti yang dipilih luar sampel bagi kaedah ini berada >= 0.5 SD lebih LEBAR daripada jangkaan rawak seragam.

`M02`, `M03`, `M13`, `M35`, `M36`, `M39`, `M48`, `M50`, `M67`, `M70`, `M77`, `M89`, `M102`, `M105`, `M115`, `M118`, `M119`, `M121`, `M126`, `M128`, `M131`, `M135`, `M139`, `M142`, `M147`, `M149`, `M150`, `M159`, `M161`

### Betulkan kecacatan henti hari-0/1 — 32 kaedah

>= 20% posisi Lejar kaedah ini dihentikan dalam <= 1 bar dengan kadar menang 0.00% — paras henti terletak dalam julat intrabar hari masuk. Kosnya kecil (bahagian 5) tetapi ia mencemari setiap pangkat.

`M02`, `M10`, `M13`, `M14`, `M18`, `M20`, `M23`, `M25`, `M26`, `M29`, `M32`, `M35`, `M46`, `M49`, `M50`, `M55`, `M57`, `M67`, `M68`, `M70`, `M74`, `M77`, `M89`, `M99`, `M102`, `M123`, `M127`, `M134`, `M140`, `M146`, `M151`, `M160`

### Keluar asal DISAHKAN — jangan ubah — 21 kaedah

Pengoptimum luar sampel memilih peraturan keluar asal kaedah ini pada >= 7 suku, atau mesin keluarnya menambah > +0.50 mata lawan pegang pasif.

`M04`, `M21`, `M22`, `M30`, `M31`, `M33`, `M34`, `M52`, `M54`, `M87`, `M91`, `M95`, `M96`, `M107`, `M117`, `M120`, `M130`, `M137`, `M145`, `M152`, `M157`


## 7. Had wajib — baca sebelum bertindak

1. **Kelebihan pegang-lebih-lama ialah masa, bukan alfa.** Kadar setiap hari sama (+0.1023% lawan +0.1051%, ujian-t berpasangan p 0.50, dan mesin kaedah sebenarnya sedikit di HADAPAN). Memegang 60 hari dan bukan 17 hari memberi 3.46x untung setiap dagangan atas modal yang terikat 3.50x lebih lama — nisbah sama. Pada 8–10 slot itu bermakna 3.5x lebih SEDIKIT dagangan setahun. `REVERSE/SISTEM.md` sudah mengukur bentuk sama: CAGR setiap unit pendedahan Clenow 18.01% lawan SPUS 17.95% — praktiknya sama.
2. **Membuang henti menaikkan MDD.** Lengkung `pegang` tiada henti sama sekali. `REVERSE/KOLAM_EKOR.md` §2 mengukur arah bertentangan pada asas tanpa signal: henti −2xATR mengurangkan min 9.79 mata setahun, jadi henti yang lebih LEBAR memang menolong pulangan — tetapi tiada henti bermakna tiada had kerugian setiap posisi.
3. **Lajur `pegang` dalam sampel** (2019–2026, alam 431). Ia bukan luar sampel. Yang luar sampel ialah W01 (bahagian 3), dan di situ penalaan per-kaedah KALAH 52/131.
4. **Lejar hadapan masih muda**: 10550 daripada 16629 posisi masih terbuka. Jangan baca lajur `H0/1` sebagai prestasi; ia sifat mekanikal.
5. **Hanya 1 kaedah (`M02`) ada sasaran jarak-tetap; 9 ada sasaran paras-struktur; 33 ada had masa.** Bukti yang menghukum sasaran mengenai jarak TETAP sahaja, jadi syor "buang sasaran" terpakai kepada SATU kaedah, bukan sepuluh. Dan `spec/SPEC_SEMUA_KAEDAH.md` menanda `FAIL ASAL` di mana spec asal tidak dapat ditentukan: membuang sasaran atau had masa bermakna kaedah itu bukan lagi kaedah pedagang itu. Itu keputusan pengguna, bukan keputusan data.
6. **Ini jangkaan setiap dagangan, bukan prestasi portfolio.** Ujian 8–10 slot lawan SPUS belum dijalankan untuk mana-mana syor di sini. `REVERSE/PENANDA_ARAS_SYARIAH.md`: SPUS memberi 17.95%/tahun CAGR (26.09% median tahunan) dan setiap sistem yang pernah diuji dalam repo ini kalah kepadanya.

## 8. Syor

1. **Jangan tala per-kaedah.** Sudah dicuba secara menyeluruh (W01: Optuna 150 percubaan x 16 suku x 132 kaedah) dan ia kalah kepada varian beku pada 79/131 kaedah.
2. **Uji SATU perubahan seragam merentas semua kaedah**, didaftar dahulu: `SPEC_MOD_M.md`. Satu keputusan, bukan 134 — itu satu-satunya bentuk yang sampel ini boleh menyelesaikan.
3. **Betulkan henti hari-0/1** kerana ia mencemari setiap pangkat, tetapi jangan jangka ia menaikkan pulangan: membuang kesemua 910 posisi itu mengubah purata Lejar hanya -0.042 mata.
4. **Jangan tambah baris MASUK lagi.** Tiga kajian bebas (`SETUP.md` 0/598, `NXX.md` 0/280 gate3, `KOMBINASI.md` 3/40 lift positif tetapi semuanya gagal syarat ekor) sudah mengukur ruang itu.
