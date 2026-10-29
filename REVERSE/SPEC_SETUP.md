# SPEC SETUP — pradaftar, 29 Okt 2026

**Dikomit SEBELUM apa-apa keputusan dilihat.** Permintaan pengguna 29 Okt 2026: setup gaya pedagang
sebenar — syarat yang **lebih longgar**, **berjalur**, **berurutan**, dan **3 syarat** bukan 1.

## 1. Mengapa ini BUKAN ulangan fasa 1

Fasa 1 diuji dan ditolak, tetapi ia **tidak** menguji tiga perkara yang pengguna minta:

| Yang diminta | Fasa 1 buat apa | Jurang |
|---|---|---|
| "RSI antara 45–60" | kuintil `q1`/`q5` = 20% **terbawah/teratas** | kuintil tidak boleh menyatakan **jalur tengah** |
| "MACD silang **dahulu**, kemudian MA silang" | syarat **serentak** pada bar sama | **urutan masa** tidak pernah diuji |
| pemicu + jalur + penapis trend | kombinasi **2** syarat | **3 syarat** tidak pernah diuji |

Ketiga-tiganya boleh dinyatakan daripada data sedia ada: `rsi14`/`stoch_k`/`bb_pctb`/`mfi14`
berterusan (jalur), dan `hari_macd_cross`/`hari_gc` ialah **bilangan hari sejak** silang (urutan).

Populasi juga berbeza: fasa 1 menilai **10,637 peristiwa sah** setahun (tutup ≥ 5% atas rendah 20
hari DAN tutup > EMA21). Kajian ini menilai **367,632 bar setahun** — iaitu setiap bar dalam alam,
tanpa penapis peristiwa. Setup bebas menyala di mana-mana.

## 2. Populasi dan keluaran

- Alam: Release `autotune-data-a02` (~3,300 ticker AS), cache `signals_*.parquet` fasa 1
  (108 lajur indikator, dikira step1 **tanpa pandang hadapan**).
- Tempoh: 2012–2025. `dalam_univ == 1` sahaja.
- Masuk: **buka bar berikutnya** selepas setup menyala, tolak kos sisi.
- Tiga keluaran dikira bagi SETIAP bar (soalan EXIT pengguna):
  - `E63` — pegang 63 sesi, keluar pada buka sesi berikutnya
  - `E63S` — sama, tetapi henti keras `masuk − 2×ATR14` pada sentuhan pertama
  - `ETRAIL` — Chandelier: keluar apabila tutup < (tutup tertinggi sejak masuk − 4×ATR14)
- Kos: `REVERSE/teras/kos.py` tanpa perubahan.

## 3. Grid — dikunci sekarang

**Pemicu (14).** 12 serentak + **2 urutan**:

`macd_cross` · `hari_macd_cross≤3` · `hari_macd_cross≤5` · `rsi_lintas50` · `rsi_lintas60` ·
`ema_crossback` · `donchian20` · `pocket_pivot` · `gap_and_go` · `vcp` · `bb_squeeze` ·
`breakout_asas` · **`urutan:macd→gc`** (`hari_macd_cross≤10 & hari_gc≤5`) ·
**`urutan:gc→macd`** (`hari_gc≤10 & hari_macd_cross≤5`)

**Jalur (8).** Inilah bahagian "longgar" — julat TENGAH, bukan hujung:

`rsi14∈[45,60]` · `rsi14∈[40,55]` · `rsi14∈[50,65]` · `rsi14∈[55,70]` ·
`stoch_k∈[20,50]` · `stoch_k∈[40,70]` · `bb_pctb∈[40,70]` · `mfi14∈[40,60]`

**Penapis (6).** Termasuk "tiada" sebagai kawalan supaya kesan penapis boleh diasingkan:

`j_ma200>0` · `cerun_ma50>0` · `hari_gc≤60` · `vol_n50≥1.2` · `supertrend` · `tiada`

**14 × 8 × 6 = 672 setup.** Grid ini **tidak akan dilebarkan**. Tiada pengoptimum, tiada Optuna
(`ARAHAN`). Ambang jalur dan penapis ditetapkan di atas dan **tidak ditala**.

## 4. Pecahan latihan/tahan — ini yang mengawal pemilihan

Masalah utama menguji 672 setup ialah sesetengahnya akan nampak baik secara kebetulan. Dikawal
dengan pecahan masa yang ketat:

- **LATIH: 2012–2019** (8 tahun). Kesemua 672 dinilai. Pilih **10 teratas** ikut jangkaan `E63S`
  dengan `n ≥ 500`. Pemilihan berlaku **sepenuhnya** di sini.
- **TAHAN: 2020–2025** (6 tahun). **Hanya 10 itu** diuji, dengan mesin penuh fasa 2:
  permutasi label dalam-bulan 1000×, bootstrap blok ikut ticker DAN minggu, BH-FDR q ≤ 0.01
  merentas 10.

Tingkap TAHAN **tidak dilihat** sebelum 10 dipilih. Keluarga ujian TAHAN hanya 10, bukan 672.

## 5. Gate — kesemuanya diperlukan

**Gate A (tahan, statistik)** bagi setiap 10:
1. `n ≥ 200` dalam tingkap tahan
2. Jangkaan > 0 **selepas membuang 5% pemenang teratas**
3. Permutasi 1000× → p; **BH-FDR q ≤ 0.01** merentas 10
4. Bootstrap blok ikut ticker DAN minggu kedua-duanya positif
5. Jangkaan tahan > 0 dalam **≥ 4 daripada 6** tahun tahan

**Gate B (portfolio)**: median 20 benih mengalahkan **SPUS** pada **pulangan DAN MDD**, 2020–2025,
kedua-dua konvensyen penanda aras (`PEMBINAAN.md`). 8 slot, kos penuh.

**DITERIMA** hanya jika ≥ 1 setup lulus Gate A **dan** Gate B.
Jika lulus A tetapi gagal B: dilaporkan sebagai **setup sah tetapi tidak mencukupi**.

## 6. Kadar menang BUKAN kriteria — dan sebabnya dilaporkan

Pengguna menyatakan premis: pakar mungkin 70% berjaya, 30% gagal ditampung henti. Premis itu
**separuh betul**. Kadar menang tinggi **tidak** bermakna untung: 70% menang pada +1% dengan 30%
rugi pada −4% memberi jangkaan **−0.5%**. Yang menentukan ialah **jangkaan**, iaitu
kadar menang × untung purata − kadar rugi × rugi purata.

Bukti dalam repo sendiri: `M03` mempunyai kadar menang hadapan **71%** dan `M55` mempunyai **0%** —
tetapi kedua-duanya diuji pada jangkaan, bukan kadar menang (`laporan/KAEDAH_TERBAIK.md`).

Maka laporan ini **mesti** memaparkan kadar menang, untung purata, rugi purata dan jangkaan
bersebelahan bagi setiap setup, serta korelasi antara kadar menang dan jangkaan merentas 672
setup. Keputusan tetap pada jangkaan.

## 7. Jangkaan priori (ditulis sebelum larian)

Saya menjangka **DITOLAK pada Gate A atau B**, tetapi dengan **kurang keyakinan** daripada
pradaftar terdahulu, atas dua sebab:

1. Jalur tengah dan urutan **belum pernah** diukur, jadi tiada bukti langsung menentangnya.
   Pradaftar saya sebelum ini (`SPEC_SILANG.md` §7) salah tepat kerana saya memanjangkan
   kecenderungan am kepada ruang yang belum diukur. Saya tidak mengulangi kesilapan itu.
2. Tetapi `KOLAM_EKOR.md` tetap terpakai: setup mesti menambah ≥ 1.00 mata sebulan hanya untuk
   seri dengan SPY, dan kelebihan hidup dalam ekor kanan nipis yang 8 slot sukar tangkap.

Jika hasilnya LULUS, jangkaan saya salah dan itu mesti dinyatakan dengan jelas.

## 8. Apa yang ujian ini TIDAK boleh buktikan

- Ia tidak boleh mencapai **+10%/bulan** (`SASARAN.md`).
- LULUS bermakna "setup ini bertahan pada tingkap tahan 2020–2025 dalam simulasi" — ia **mesti**
  disahkan ke hadapan sebagai lorong `portfolio_slot/` sebelum dipercayai.
- Ia tidak menguji kaedah Mxx (`laporan/KAEDAH_TERBAIK.md` untuk itu).
