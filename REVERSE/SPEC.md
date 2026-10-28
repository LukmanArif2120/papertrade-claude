# SPEC kajian REVERSE — reverse engineer saham padu US (ENTRY / HOLD / EXIT)

Dikunci **27 Okt 2026**, sebelum sebarang larian. Berdasarkan arahan pengguna versi 10 (27 Okt 2026).
Perubahan selepas tarikh ini hanya sebagai **pindaan bertarikh** di §13; hasil lama dikekalkan.

Kajian ini menguji **signal dan indikator** sahaja. Bukan kaedah Mxx repo, bukan penalaan parameter.
Tiada Optuna. Tiada pengoptimum. Semua indikator guna tetapan standard yang ditulis di sini.

---

## 1. Matlamat dan tiga soalan

Arah terbalik daripada backtest: **hasil dahulu, signal kemudian**. Cari saham US yang terbukti naik
kuat (10%–300%+) dalam maksimum 3 bulan, tangkap nilai indikator pada ENTRY/HOLD/EXIT, kemudian
banding silang untuk signal COMMON dan UNIQUE, dengan kawalan supaya ia bukan kebetulan.

Tiga soalan dipisahkan sepanjang kajian:

- **(a) ARAH** — adakah saham ini akan naik?
- **(b) MAGNITUD** — naik setinggi mana, dan secepat mana?
- **(c) KAPASITI** — berapa kerap, cukup untuk mengisi portfolio?

Hipotesis yang diuji: **maklumat magnitud tidak terletak pada pemicu, tetapi pada KONTEKS ketika
pemicu itu menyala.**

**Kriteria akhir kajian = Step 9 (prestasi portfolio 8 slot), bukan lift signal.** Sistem diterima
kerana taburan pulangan bulanannya. Sasaran regangan pengguna +10% sebulan (3.14× setahun) ialah
sasaran, **bukan andaian**. Dilaporkan tanpa dipermanis: median pulangan bulanan, % bulan ≥ +10%,
bulan terburuk, MDD.

Falsafah pegangan: tiada sasaran untung tetap. Selagi harga masih naik, tiada sebab menjual — keluar
hanya apabila peraturan exit menyala.

---

## 2. Data

| Perkara | Tetapan |
|---|---|
| Sumber harga | Release GitHub `autotune-data-a02` (219 MB, 18 fail parquet) |
| Pemuat | `AUTOTUNE/teras/data.py` `ambil(tag='autotune-data-a02')` — tiada pemuat baharu |
| Julat bar tersedia | 2009-01-02 – 2026-10-16 |
| Universe | `universe.parquet` A02, titik masa bulanan |
| Saiz universe 2025 | **2000 saham setiap bulan** (semua 12 bulan tepat 2000); **2321 ticker berbeza** sepanjang tahun |
| Kumpulan data | md5 ticker (AUTOTUNE/SPEC.md §1). 2025: A = 1185 ticker, B = 1136 ticker |
| A = cari, B = sahkan | Carian Step 4 atas A; Step 8.1 ulang atas B |
| Pemanasan | muat dari **2023-06-01** (≈ 397 hari dagangan sebelum 2025-01-01; syarat ≥ 300 dipenuhi) |
| Penilaian hadapan | hingga **2026-10-16** (hujung data) |
| Harga rujukan | semua syarat run guna **tutup**, kecuali "rendah terendah 20 hari" (guna **rendah**) |
| Indeks | `idx.parquet`: SPY dan QQQ, julat sama (disahkan) |
| Jangan guna | Release `autotune-data` (A01) — ia membuang saham meruap |

**Larangan `autotune-data` A01 disahkan dipatuhi:** semua larian guna `tag='autotune-data-a02'`.

### 2.1 Sektor dan industri

Sumber: `BacktestShariah2/papertrade/peta_industri.csv` (ticker → industri Moomoo) dipeta ke **11
sektor Morningstar** melalui `BacktestShariah2/standard/sektor_pasaran.py` `SEKTOR_INDUSTRI`.
Sandaran: `BacktestShariah2/data/skrin/tv_us.csv`. Kelas saham (BRK-B, BF-A, …) jatuh balik ke
ticker asas.

Liputan universe 2025: **2310 / 2321 = 99.5%**. Sisa ditanda sektor/industri `Lain-lain`.

**Kaveat:** peta ini **bukan titik masa** (petikan 2026). Sektor syarikat jarang berubah; dinyatakan
sebagai had kajian dalam setiap laporan.

### 2.2 Kaveat data dua arah (WAJIB dalam setiap laporan)

Data A02 **tiada saham delist** (bias survivorship). Ini memukul dua arah:

1. Run dipandang **tinggi** — had atas, bukan jangkaan.
2. Kadar signal palsu dipandang **rendah** — saham yang mati tidak ada dalam penyebut.

Satu tahun = **satu rejim pasaran**. Keputusan maksimum pada fasa 2025 ialah **CALON** (§11.8).

---

## 3. Kos dan ufuk

### 3.1 Kos (AUTOTUNE/SPEC.md §3) — dikenakan pada SEMUA metrik pulangan

Setiap sisi: komisen **0.1%** + slippage ikut **median nilai dagangan 20 hari pada hari isyarat**:

| Median nilai dagangan 20 hari | Slippage |
|---|---|
| ≥ USD 50 juta | 0.05% |
| USD 10 – 50 juta | 0.10% |
| < USD 10 juta | 0.25% |

### 3.2 Dua ufuk — jangan dicampur

- **UFUK LABEL = 63 hari dagangan.** Hanya untuk mencari dan mengelas run (Step 1, 2, 4, 7a).
- **UFUK PENILAIAN = terbuka, had 252 hari dagangan.** Untuk Step 2b, 7b dan 9: dagangan ditamatkan
  oleh **peraturan exit**, bukan oleh tetingkap. Ini yang membenarkan "pegang selagi naik" diukur.

### 3.3 Harga label lawan harga dagangan (penyelesaian kekaburan arahan)

Arahan menyebut `harga_sah` (Step 2) dan "masuk buka esok" (Tarikh sah). Dikunci:

- **`harga_sah` = tutup pada tarikh_sah** → untuk label run dan `%_naik_dagang`.
- **`harga_masuk` = buka hari dagangan berikut selepas tarikh_sah**, ditambah kos sisi beli →
  untuk SEMUA metrik dagangan (Step 7, 7b, 9).

### 3.4 Pemotongan hujung data (censoring)

Kemasukan yang ufuk 252 harinya melepasi 2026-10-16 ditutup pada bar terakhir yang ada dan ditanda
`terpotong_data = ya`. Peratusannya dilaporkan berasingan dalam Step 7b dan Step 9; ia **tidak**
dibuang.

### 3.5 Pandang ke hadapan

Indikator hari *t* hanya guna data hingga **tutup hari t**. Disemak oleh `REVERSE/semak_hadapan.py`
dengan **≥ 12 tarikh potong** mengikut cara `AUTOTUNE/kaedah/semak_hadapan.py`.

---

## 4. Definisi run (UFUK LABEL)

1. Imbas berurutan setiap saham; `tarikh_mula` run baharu mesti ≥ `tarikh_tamat` run sebelumnya.
   Run **tidak boleh bertindih**.
2. Run bermula apabila **tutup ≥ 5% di atas rendah terendah 20 hari sebelumnya**;
   `tarikh_mula` = hari rendah terendah itu.
3. TETINGKAP = **63 hari dagangan** selepas `tarikh_mula`. `tarikh_puncak` = hari dengan **tutup
   tertinggi dalam tetingkap itu**.
4. `masih_naik` = ya jika tutup tertinggi berlaku dalam **3 hari terakhir** tetingkap. Direkod; run
   kekal sah. Dianalisis khusus dalam Step 2b.
5. Tarikh turun (pemantauan maksimum 63 hari selepas `tarikh_puncak`):
   - `tarikh_turun_10` = hari pertama tutup ≤ harga_puncak × 0.90
   - `tarikh_turun_25` = hari pertama tutup ≤ harga_puncak × 0.75
   - `tarikh_tamat` = `tarikh_turun_25`, atau hujung pemantauan (`tamat_pemantauan = ya`)
6. `%_naik_rendah` = (harga_puncak − rendah tarikh_mula) ÷ rendah tarikh_mula × 100
   `%_naik_dagang` = (harga_puncak − harga_sah) ÷ harga_sah × 100
   `hari_ke_puncak` = bilangan hari dagangan tarikh_mula → tarikh_puncak
7. **SYARAT KELAYAKAN** (grid laju; gagal = BUKAN run, rekod dalam `skipped_2025.csv` sebab
   "terlalu perlahan"):

   | hari_ke_puncak | %_naik_rendah minimum |
   |---|---|
   | ≤ 21 | ≥ 10% |
   | 22 – 42 | ≥ 20% |
   | 43 – 63 | ≥ 30% |

8. Setiap pullback-pulih dalam tetingkap direkod sebagai **kaki** untuk Step 5.
9. Jatuh 10%/25% hanya **merekod tarikh turun** — BUKAN penentu `tarikh_puncak`. Penentu tunggal
   ialah tetingkap 63 hari. Oleh itu signal exit berasaskan % dari puncak **tidak bulat** dengan
   definisi run.

Run/peristiwa sah hanya jika ticker ada dalam universe pada **bulan berkenaan**.

### 4.1 Tarikh sah (entry yang boleh didagangkan)

Hari **pertama** yang: tutup ≥ 5% di atas rendah `tarikh_mula` **DAN** tutup > EMA21, **DAN** dalam
≤ **10 hari dagangan** selepas `tarikh_mula`.

Jika tidak dipenuhi: `entry_sah = tidak` — run kekal dalam `runs_2025.csv` tetapi **DIKECUALIKAN**
daripada analisis ENTRY/HOLD/EXIT. Bilangannya dilaporkan; jika **> 50%**, dilaporkan sebagai
**amaran** bahawa syarat 10 hari terlalu ketat.

Signal entry diukur pada `tarikh_sah`.

---

## 5. Kelas

### 5.1 KUMPULAN (ikut `%_naik_rendah`)

| Kumpulan | Syarat |
|---|---|
| SUPER PADU | ≥ 100% |
| PADU | 30 – 99% |
| BIASA | 10 – 29% |

### 5.2 KELAS LAJU (ikut `hari_ke_puncak`)

PANTAS ≤ 21 · SEDANG 22–42 · PERLAHAN 43–63.
Dilaporkan KUMPULAN × KELAS LAJU; sel **n < 20** ditanda **SAMPEL KECIL** dan tidak boleh jadi asas
keputusan.

### 5.3 JENIS KENAIKAN (dinilai tarikh_mula → tarikh_puncak)

Komponen:

- **KAKI** = pullback-pulih. Puncak sementara = tutup tertinggi setakat hari itu. Satu kaki direkod
  apabila tutup jatuh **≥ 5%** daripada puncak sementara (palung = tutup terendah dalam kejatuhan)
  **DAN** kemudian tutup melepasi semula puncak sementara itu dalam tetingkap.
- **HIGHER LOW** = palung kaki ke-*n* > palung kaki ke-(*n*−1); kaki pertama dibanding `rendah_mula`.
  `higher_low_pecah` = ya jika mana-mana palung lebih rendah daripada palung sebelumnya.
- `sumbangan_2_hari` = jumlah **dua hari kenaikan harga terbesar** ÷ (harga_puncak − rendah_mula)
- `pct_hari_atas_ema21` = % hari tutup > EMA21, dari `tarikh_sah` hingga `tarikh_puncak`

Kelas, **diuji mengikut urutan**:

1. **LONJAKAN** — `sumbangan_2_hari ≥ 50%`. Mengatasi kelas lain.
2. **BERTANGGA** — `bilangan_kaki ≥ 2` DAN `higher_low_pecah = tidak` DAN `pct_hari_atas_ema21 ≥ 60%`.
   Definisi operasi "naik dan naik".
3. **STABIL** — selain itu.

**Label sahaja — BUKAN penapis.**

### 5.4 GRAF MENAIK

ya/tidak, dinilai **pada puncak**: harga > MA50 > MA200 **dan** MA200 hari ini > MA200 20 hari lalu.

### 5.5 BUCKET laporan

`%_naik`: 10 / 20 / 30 / 50 / 100 / 200 / 300%+ · tempoh: ≤21, ≤42, ≤63 hari. **Tiada LONG RUN.**

### 5.6 Subset analisis

- **S1** = semua run layak
- **S2** = `jenis_kenaikan` BERTANGGA
- **S3** = `graf_menaik` ya

Carian atas **S1 dan S2 sahaja**; **keputusan utama = S2**. S3 bukan keluarga carian — hanya
dilaporkan bagi signal yang sudah lulus, jadi tidak menambah N.

---

## 6. Saham tidak layak

Run dan peristiwa ditapis melalui `BacktestShariah2/data/ambil_alih.csv` dan
`BacktestShariah2/kod/tidak_layak.py`. Run yang **puncaknya selepas pengumuman ambil alih** ditanda
`sebab_kecuali = "ambil_alih"` dan dikecualikan daripada analisis signal (kekal dalam `runs_` untuk
rekod).

---

## 7. Peristiwa sah (universe penuh)

Setiap hari mana-mana saham universe yang memenuhi syarat **TARIKH SAH** (§4.1) **tanpa melihat masa
depan**: tutup ≥ 5% di atas rendah terendah 20 hari sebelumnya DAN tutup > EMA21, dan hari itu ialah
hari pertama syarat dipenuhi dalam ≤ 10 hari dagangan selepas hari rendah terendah itu.

Setiap peristiwa direkod dengan:

- `jenis_peristiwa` = `mula_run` | `dalam_run` | `tiada_run`
- `hasil` = SUPER PADU / PADU / BIASA (ikut run induk) atau **GAGAL** (`tiada_run`)

**Step 4 dikira DUA kali:** (a) `mula_run` + `tiada_run` — **keputusan ikut ini**; (b) semua
peristiwa — semakan kekukuhan.

### 7.1 Kawalan

- **(a) KAWALAN PERISTIWA** = peristiwa sah yang GAGAL.
- **(b) KAWALAN RAWAK** = **10,000** titik rawak saham universe setahun tanpa syarat hasil (kadar
  asas), **diagih sama rata setiap bulan**, **benih tetap 42**.

### 7.2 POPULASI KUINTIL — DIBEKUKAN

Semua **PERISTIWA SAH tahun kajian dalam kumpulan data A**. Bukan atas run, bukan atas semua hari,
bukan dalam sektor. **Satu populasi sahaja, untuk semua indikator.** Sempadan kuintil ditulis ke
`REVERSE/.cache/kuintil_2025.json` pada larian Step 3 dan tidak dikira semula.

Indikator berterusan dijadikan signal pada **DUA HUJUNG kuintil sahaja (Q1 dan Q5)**. Q2–Q4 tidak
diuji.

---

## 8. Indikator (tetapan standard; tiada penalaan)

Modul: `REVERSE/teras/ind.py`, **77 lajur**. Semua lajur hari *t* hanya guna data hingga tutup *t*.

### 8.1 Senarai

**Moving average** — EMA9, EMA21, MA50, MA150, MA200; jarak % harga dari setiap satu (`j_*`);
kecerunan EMA21/MA50/MA200 (% ubah 10 hari, `cerun_*`); susunan EMA9>EMA21>MA50>MA150>MA200
(`lapis`, 0–4); hari sejak golden cross MA50/MA200 (`hari_gc`).

**Momentum** — RSI(14), RSI(2), lintas 50/60; MACD(12,26,9) nilai/signal/histogram, cross ke atas,
hari sejak cross, atas/bawah sifar; Stochastic(14,3); ROC 20/60; ADX(14) + DI; Williams %R(14);
CCI(20). RSI dan ADX guna pelicinan **Wilder**.

**Volatiliti** — ATR(14) Wilder, ATR%, nisbah ATR14/ATR50; Bollinger(20,2) lebar %, %B, squeeze
(lebar terendah 120 hari); Keltner(20, 2×ATR) kedudukan; julat harga 10 dan 20 hari.

**Volume & aliran wang** — volume ÷ purata 50 hari (hari 0 dan purata 5 hari); OBV dan garisan A/D
paras tertinggi baru **sebelum harga**; nisbah volum hari naik/turun (20 hari); MFI(14); CMF(20).

**Trend lain** — Supertrend(10,3), PSAR(0.02, 0.2), Ichimoku(9,26,52) harga atas awan + tenkan>kijun,
Donchian 20/55 breakout.

**Corak harga** — inside day, outside day, NR7, hammer, bullish engulfing, pocket pivot, VCP,
gap and go, breakout tertinggi 52 minggu, breakout base, EMA crossback.

**Kekuatan relatif** — jarak % dari tertinggi/terendah 52 minggu; RS lawan SPY 3/6/12 bulan
(lebihan pulangan, dikira sendiri daripada harga A02); garisan RS (tutup ÷ tutup SPY) paras
tertinggi baru 252 hari; prestasi indeks sektor 1 bulan.

**Konteks pasaran** — SPY dan QQQ atas MA50 dan MA200; kecerunan MA50 SPY.

### 8.2 Definisi operasi corak (dikunci, kerana istilah ini tidak standard)

| Corak | Definisi |
|---|---|
| `pocket_pivot` | tutup > tutup semalam DAN volum ≥ volum tertinggi antara **hari turun** dalam 10 hari lalu DAN tutup > EMA21 |
| `vcp` | `julat20` ≤ 0.6 × `julat20` 40 hari lalu DAN tutup > MA50 |
| `gap_and_go` | buka > tertinggi semalam × 1.02 DAN tutup > buka DAN volum ≥ 1.5 × purata 50 hari |
| `breakout_asas` | tutup > tertinggi 60 hari (hingga semalam) DAN `julat20` semalam ≤ persentil 30 `julat20` 120 hari |
| `ema_crossback` | tutup > EMA21 DAN tutup semalam ≤ EMA21 semalam DAN `cerun_ma50` > 0 |
| `hammer` | (min(buka,tutup) − rendah) ≥ 2 × |tutup−buka| DAN (tinggi − maks(buka,tutup)) ≤ |tutup−buka| |
| `obv_tinggi_baru` | OBV pada paras tertinggi 50 hari DAN tutup **belum** pada tertinggi 50 hari |
| `breakout_52w` | tutup ≥ tutup tertinggi 252 hari |

### 8.3 Indeks sektor — PINDAAN 27 Okt 2026 (lihat §13.1)

ETF SPDR **tidak dapat diperoleh**: endpoint sejarah Alpha Vantage premium-gated, Yahoo dan stooq
disekat proksi sesi. Ganti seperti dibenarkan arahan: **indeks sektor berpemberat sama dibina
daripada saham universe A02**.

Setiap hari, setiap sektor: pulangan = **median pulangan harian ahli universe (titik masa) dalam
sektor itu**; indeks = hasil darab kumulatif (1 + median). Pulangan ahli hanya dikira pada hari yang
bulannya ahli itu ada dalam universe.

Maka: "prestasi ETF sektor 1 bulan" → `sektor_1b` (% ubah indeks sektor 21 hari);
"ETF sektor > MA50" → `sektor_atas_ma50`.

### 8.4 Dedup — SENARAI KEUTAMAAN TETAP (ditulis sebelum larian)

Jika **korelasi Spearman > 0.8** antara dua indikator berterusan (dikira atas POPULASI KUINTIL
§7.2), **kekalkan yang lebih awal** dalam senarai ini; yang lain dibuang dan direkod dalam
`log_ujian.csv` (sebab `dedup_spearman`):

```
j_ma200, j_ma50, j_ema21, j_ema9, j_ma150, lapis, cerun_ma50, cerun_ema21, cerun_ma200, hari_gc,
rsi14, roc60, roc20, macd_hist, hari_macd_cross, adx14, pdi, mdi, stoch_k, stoch_d, willr14, cci20,
rsi2, atr_pct, nisbah_atr, bb_lebar, julat20, julat10, bb_pctb, kelt_pos, vol_n50, vol_n50_5h,
vol_naik_turun20, mfi14, cmf20, j_52w_tinggi, j_52w_rendah, rs_spy_6b, rs_spy_3b, rs_spy_12b,
sektor_1b
```

Rasional susunan: jarak MA sebelum kecerunan pendua; RSI(14) sebelum Williams %R / Stochastic yang
hampir monotonik dengannya; `bb_lebar` sebelum `julat20`/`julat10`; `rs_spy_6b` dahulu kerana ia
konteks yang dipradaftar (§9).

**10 KONTEKS yang dipradaftar (§9) tidak boleh dibuang oleh dedup** — jika satu daripadanya
berkorelasi > 0.8 dengan indikator lain, indikator **lain** itu yang dibuang.

---

## 9. Pemicu dan konteks (dipradaftar)

### 9.1 PEMICU (6)

| # | Pemicu | Lajur |
|---|---|---|
| 1 | MACD(12,26,9) cross ke atas | `macd_cross` |
| 2 | RSI(14) lintas 50 ke atas | `rsi_lintas50` |
| 3 | Tutup kembali atas EMA21 selepas pullback | `ema_crossback` |
| 4 | Donchian 20 breakout | `donchian20` |
| 5 | Pocket pivot | `pocket_pivot` |
| 6 | Gap and go | `gap_and_go` |

### 9.2 KONTEKS (10; dua hujung kuintil setiap satu = 20 syarat konteks)

| # | Konteks | Lajur |
|---|---|---|
| 1 | Jarak % dari tertinggi 52 minggu | `j_52w_tinggi` |
| 2 | RS lawan SPY 6 bulan | `rs_spy_6b` |
| 3 | Lebar Bollinger (squeeze) | `bb_lebar` |
| 4 | ATR% | `atr_pct` |
| 5 | Bilangan lapis MA tersusun | `lapis` |
| 6 | Kecerunan MA50 | `cerun_ma50` |
| 7 | Volume ÷ purata 50 hari | `vol_n50` |
| 8 | Ketat julat 20 hari | `julat20` |
| 9 | Kedudukan harga vs MA200 | `j_ma200` |
| 10 | Prestasi indeks sektor 1 bulan | `sektor_1b` |

---

## 10. Indikator DIKELUARKAN daripada fasa 1 (disahkan 27 Okt 2026)

Tiada data titik-masa 2025:

- **RS rating repo** (`BacktestShariah2/data/rs/` bermula 2026-09-15 — 0% liputan 2025)
- **Gred sektor/industri repo** (`gred_kumpulan_sejarah.csv` bermula 2026-09-25 — 0% liputan)
- **Earnings dalam ±5 hari, kejutan EPS, power earnings gap** (tiada kalendar earnings titik-masa
  2025; `data/sec/` bermula 27 Okt 2026)

Ditangguh ke fasa 2; **tidak boleh ditambah separuh jalan**.
RS lawan SPY 3/6/12 bulan dan garisan RS **dikira sendiri daripada harga A02** — kekal dalam kajian.

---

## 11. Kawalan bilangan ujian

### 11.1 HAD BERSYARAT (pra-daftar; dinilai **sekali** selepas Step 1, tidak boleh diubah selepas melihat hasil Step 4)

Jika **n peristiwa PADU dalam S2 < 300**: kombinasi dihadkan kepada **pemicu × 1 konteks sahaja
(120 ujian)**, dan kombinasi HOLD/EXIT dihadkan kepada **1 syarat**.

### 11.2 HAD CORONG

Maksimum **30 signal** diteruskan daripada Step 4 ke Step 7, diisih ikut `lift_presisi`.

### 11.3 KELUARGA FDR

Benjamini-Hochberg **q ≤ 0.01**, dikira **berasingan** bagi ENTRY, HOLD, EXIT dan SISTEM (7b), atas
N keluarga sendiri. Keluarga kedua **SUPER PADU** dilaporkan dengan FDR sendiri.

### 11.4 Jangkaan N

ENTRY 972 · HOLD 164 · EXIT 256 · SISTEM 234 (≈ 1,626). **N sebenar dilaporkan** bersama setiap
keputusan, dan setiap signal/kombinasi yang diuji direkod dalam `REVERSE/log_ujian.csv`.

### 11.5 Step 4 — metrik

Atas PERISTIWA SAH, **dua keluarga metrik**:

**KEHADIRAN** (signal dalam kalangan hasil)
- `K_super`, `K_padu`, `K_biasa`, `K_gagal` = % kemunculan dalam setiap hasil
- `K_rawak` = % kemunculan dalam KAWALAN RAWAK
- `lift` = K_padu ÷ maks(K_biasa, K_gagal, 1/n)
- `lift_rawak` = K_padu ÷ maks(K_rawak, 1/n)

**PRESISI** (hasil apabila signal muncul — lebih dekat dengan keputusan dagangan)
- `presisi` = peristiwa PADU atau SUPER PADU dengan signal ÷ semua peristiwa dengan signal
- `kadar_asas_padu` = peristiwa PADU atau SUPER PADU ÷ semua peristiwa sah
- `lift_presisi` = presisi ÷ kadar_asas_padu

### 11.6 Step 4 — kelas

| Kelas | Syarat |
|---|---|
| TERAS | K_padu ≥ 50% DAN lift ≥ 2 |
| UNIQUE | K_padu 15–49% DAN lift ≥ 3 |
| LANGKA | K_padu 3–14% DAN lift ≥ 5 DAN n ≥ 30 |
| SEDERHANA | K_padu ≥ 50% DAN lift 1.5–1.99, ATAU K_padu 15–49% DAN lift 2–2.99 |
| COMMON BIASA | K_padu ≥ 50% DAN lift < 1.5 |
| TIDAK BERGUNA | selain itu |

Diteruskan ke Step 7: TERAS, UNIQUE, LANGKA, **atau** mana-mana signal dengan `lift_presisi ≥ 3` dan
`n ≥ 30` walaupun kelasnya rendah. Had corong 30.

**Jika TERAS kosong, kajian diteruskan dengan UNIQUE/LANGKA — itu bukan kegagalan, ia keputusan.**

Tanda: `SAMPEL KECIL` jika n < 20 · `BERGANTUNG PADA TEMA` jika ≥ 50% kemunculan dalam satu industri
· `LONJAKAN BERITA` jika ≥ 50% kemunculan berakhir sebagai LONJAKAN.

Pemicu tunggal dilaporkan **walaupun DITOLAK**, dengan lift, K_rawak dan kekerapan setahun, dalam
seksyen **PEMICU YANG TIDAK MEMBEZAKAN**.

### 11.7 Step 7 — kapasiti dan bunyi latar

Portfolio rujukan 8 slot × 12.5%. Dengan pegangan purata ~15 hari dagangan, portfolio perlu ~11
kemasukan sebulan = **≥ 130 calon setahun selepas penapis** (idealnya 2–3× lebih).

| Label | Syarat |
|---|---|
| TULANG BELAKANG | ≥ 130 calon/tahun selepas penapis, jangkaan positif |
| PELENGKAP | jarang tetapi tepat |

Signal dengan kekerapan **> 5,000 kali setahun dan lift < 1.5** ditanda **BUNYI LATAR** dan **tidak
diteruskan**, walau apa pun K_padu-nya.

### 11.8 HAD FASA 2025

Gate 8.1 memerlukan pengesahan merentas tahun (2024–2021). Oleh itu keputusan **tertinggi** selepas
tahun 2025 sahaja ialah **CALON**. **Tiada signal boleh dilabel DITERIMA** sebelum dua tahun lain
disahkan. Ujian ke hadapan hidup = fasa kemudian, atas keputusan pengguna sahaja.

---

## 12. Step 9 — peraturan portfolio (DIBEKUKAN sebelum larian)

- 8 slot × 12.5% ekuiti, kos penuh, **tiada leverage**, satu posisi satu saham.
- Masuk pada **buka hari berikut** selepas signal (§3.3), kos sisi beli dikenakan.
- Pegang mengikut peraturan HOLD yang diuji; keluar pada signal EXIT yang diuji, kos sisi jual.
- **Peraturan pemilihan apabila calon melebihi slot:** isih menurun ikut `lift_presisi` signal yang
  mencetuskannya, kemudian ikut `rs_spy_6b` (RS 6 bulan) menurun, kemudian ikut ticker (abjad) untuk
  pemutus seri yang deterministik.
- Slot yang kosong kekal tunai (tiada pulangan).
- Dilaporkan: pulangan bulanan (median, purata, taburan penuh 12 bulan), % bulan ≥ +10%, % bulan
  positif, bulan terbaik, **bulan TERBURUK**, CAGR, MDD, purata slot terisi, pusing ganti bulanan,
  purata hari pegangan; banding dengan **SPY** tempoh sama dan dengan portfolio **KAWALAN RAWAK**.
- Dinyatakan terus tanpa dipermanis: adakah sistem mencapai 10% sebulan secara median, atau tidak,
  dan apa angka sebenarnya. Jika tidak, apa yang menghalang (kapasiti, kadar menang, saiz menang,
  atau bulan buruk).

---

## 13. Pindaan bertarikh

### 13.1 — 27 Okt 2026: indeks sektor ganti ETF SPDR

**Sebab:** semakan kesediaan Step 0.3d gagal. Diuji dan direkod:

- `TIME_SERIES_DAILY_ADJUSTED` (Alpha Vantage MCP) = endpoint premium → ditolak.
- `TIME_SERIES_DAILY` dengan `outputsize=full` = ciri premium → ditolak; `compact` hanya 100 bar
  terakhir (2026), tiada liputan 2025.
- `historical-price-eod-*` (FMP MCP) = plan lebih tinggi diperlukan → ditolak.
- `query1.finance.yahoo.com` dan `stooq.com` = proksi sesi menolak sambungan (403).
- Moomoo `quote_history_kline` **berjaya** tetapi responsnya ~500 aksara/bar (11 ETF × ~515 bar
  ≈ 780 ribu token konteks); ditolak atas kos, dengan persetujuan pengguna 27 Okt 2026.

**Ganti:** §8.3 — indeks sektor berpemberat sama daripada universe A02. Diluluskan pengguna
27 Okt 2026.

### 13.2 — 27 Okt 2026: `harga_sah` lawan `harga_masuk`

Arahan menyebut kedua-dua `harga_sah` (Step 2) dan "masuk buka esok" tanpa menyatakan yang mana
dipakai untuk metrik mana. Dikunci di §3.3. Tiada perubahan pada definisi run.

### 13.3 — 27 Okt 2026: pemotongan hujung data

Arahan menetapkan ufuk penilaian 252 hari tetapi data tamat 2026-10-16. Peraturan censoring dikunci
di §3.4 (tanda `terpotong_data`, tidak dibuang, dilapor berasingan).

### 13.4 — 27 Okt 2026: HAD BERSYARAT dinilai atas populasi keputusan

Arahan §11.1 menyebut "n peristiwa PADU dalam S2 < 300" tanpa menyatakan populasi peristiwa yang
mana, sedangkan arahan Step 4 menetapkan dua populasi: **(a) mula_run + tiada_run — keputusan ikut
ini** dan (b) semua peristiwa (semakan kekukuhan).

Dikunci: **HAD BERSYARAT dinilai atas populasi keputusan (a)**, kerana kuasa statistik keputusan
Step 4 ditentukan oleh populasi yang keputusan dibuat atas. Bacaan ini lebih ketat.

Dinilai **sekali** selepas Step 1, sebelum sebarang metrik Step 4 dikira:

| Populasi | n peristiwa PADU dalam S2 | Had |
|---|---|---|
| (a) mula_run + tiada_run — **dipakai** | **189** | **< 300 → AKTIF** |
| (b) semua peristiwa — rujukan sahaja | 995 | ≥ 300 |

**HAD BERSYARAT AKTIF.** Maka: kombinasi ENTRY dihadkan kepada **pemicu × 1 konteks sahaja (120
ujian)**; pemicu × 2 konteks **TIDAK** diuji. Kombinasi HOLD/EXIT dihadkan kepada **1 syarat**.
Keputusan ini tidak boleh diubah selepas melihat hasil Step 4.

### 13.5 — 27 Okt 2026: topeng universe pada peristiwa

Peristiwa sah mesti memenuhi syarat tarikh sah **dan** ticker ada dalam universe bulan itu
(arahan: "Run/peristiwa sah hanya jika ticker dalam universe pada bulan berkenaan"). Larian pertama
mencetak 16,324 peristiwa tanpa topeng itu; angka betul selepas topeng ialah **13,998**. Kod
dibetulkan dan Step 1 dijalankan semula sebelum Step 3.

### 13.6 — 27 Okt 2026: 13 signal EXIT dalam grid SISTEM

Arahan Step 6.2 menyenaraikan **20** calon exit, tetapi Step 7b menetapkan "18 peraturan HOLD × 13
= 234 ujian". Tiga belas dipradaftar sekarang sebagai signal yang **boleh menjadi exit tunggal**
(iaitu pasti menamatkan dagangan pada laluan menurun):

```
bawah_ema9, bawah_ema21, bawah_ma50, rsi_70_60, macd_bawah, hist_neg3, hari_agihan,
trail_2atr, trail_3atr, chandelier_4atr, trail_8pct, trail_10pct, trail_15pct
```

Tujuh calon yang lain — bearish divergence RSI, bearish divergence MACD, climax naik ≥ 25%/3 minggu,
gap up besar selepas kenaikan panjang, jarak MA50 ≥ 2× median run, ATR% ≥ 1.5× median run, pullback
bertukar SIHAT → AMARAN — ialah syarat **amaran**: ia boleh tidak menyala sama sekali, jadi sebagai
exit tunggal ia meninggalkan dagangan terbuka selama-lamanya. Ia kekal dalam Step 6 sebagai **CALON**
dan dilaporkan penuh (hari dari puncak, pulangan_exit, % keuntungan dikekalkan, kadar exit palsu),
tetapi tidak masuk grid 18 × 13.

### 13.7 — 27 Okt 2026: semantik peraturan HOLD dalam Step 7b

Arahan Step 5.5 memberi peraturan HOLD sebagai ayat ("pullback ≤ X% atau ≤ paras MA Y boleh
di-hold") dan Step 7b menetapkan "pegang mengikut peraturan HOLD, keluar pada signal EXIT". Dikunci:
peraturan HOLD ialah **veto** atas signal EXIT, bukan pencetus exit sendiri.

Dagangan keluar apabila signal EXIT menyala **DAN** veto HOLD tidak sah. Veto sah hanya jika SEMUA:

1. pullback dari tutup tertinggi sejak masuk ≤ X%
2. tutup ≥ paras MA Y
3. trend saham: tutup > MA50 **dan** cerun MA50 > 0
4. trend pasaran: SPY > MA50 **dan** SPY > MA200 pada hari itu

Dengan X = 20 dan Y = MA50 veto menjadi longgar (menghampiri rujukan "pegang tanpa jual"); dengan
X = 5 dan Y = EMA9 veto hampir tiada (menghampiri signal EXIT tulen). Grid 18 peraturan merentas
ruang itu dengan sengaja.

Jualan dilaksana pada **buka hari berikut** selepas signal, kos sisi jual dikenakan.

### 13.8 — 27 Okt 2026: pembinaan populasi subset S2 untuk Step 4

Arahan menetapkan S2 = run BERTANGGA, tetapi Step 4 dikira atas **peristiwa**, bukan run. Dikunci:
populasi S2 = peristiwa yang **run induknya BERTANGGA** (hasil SUPER PADU / PADU / BIASA) **+**
peristiwa `tiada_run` (hasil GAGAL, kegagalan bersih). Peristiwa yang run induknya LONJAKAN atau
STABIL **dikeluarkan** daripada S2 — ia bukan hasil sasaran dan bukan kegagalan bersih, jadi
memasukkannya akan mencairkan lift tanpa makna. S1 = semua peristiwa populasi berkenaan.

### 13.9 — 27 Okt 2026: MDD dalam Step 7b, dan skop Step 9

**MDD Step 7b.** Arahan Step 7b.3 meminta MDD setiap gabungan, tetapi 234 gabungan dinilai atas
dagangan bertindih (bukan portfolio), jadi MDD peringkat portfolio tidak terdefinisi di sana.
Dikunci: Step 7b melaporkan `mae_median` (median kejatuhan terburuk dalam dagangan) sebagai ganti;
**MDD peringkat portfolio dilaporkan dalam Step 9**, tempat ia bermakna.

**Set kemasukan Step 7b.** Gabungan kemunculan semua signal yang lulus Step 7, didedup ikut
(ticker, tarikh) = 232,292 kemunculan. Simulasi 234 sistem × 232,292 kemasukan tidak munasabah;
dikunci: **sampel berlapis ikut bulan, 2,000 sebulan = 24,000 kemasukan, benih 42**. Dilaporkan
sebagai sampel dalam setiap jadual Step 7b.

**Skop Step 9.** Arahan Step 9 meminta portfolio "bagi setiap sistem yang lulus Step 8". Jika tiada
sistem lulus (kerana rujukan (c) menang), Step 9 tetap dijalankan atas: (i) ketiga-tiga rujukan
wajib, (ii) tiga sistem jangkaan tertinggi daripada Step 7b, (iii) portfolio KAWALAN RAWAK, semuanya
dengan signal ENTRY yang berstatus CALON selepas Step 8. Ini supaya kriteria akhir (prestasi
portfolio) tetap dijawab dengan angka, bukan dibiar kosong.

### 13.10 — 27 Okt 2026: Step 9 apabila TIADA signal CALON

Tahun 2024 menghasilkan **0 signal ENTRY berstatus CALON** (semua 18 gagal gate G4 bootstrap dan
G5 outlier). Arahan Step 9 menetapkan portfolio dibina "bagi setiap sistem yang lulus Step 8", jadi
secara literal Step 9 2024 tiada apa untuk dinilai.

Dikunci: apabila tiada signal CALON, Step 9 tetap dijalankan atas signal yang **lulus Step 7**, dan
output menanda `asas_entry = "lulus Step 7 sahaja (TIADA signal CALON tahun ini)"`. Ini supaya
kriteria akhir (prestasi portfolio) tetap dijawab dengan angka untuk setiap tahun, dan supaya
perbandingan merentas tahun mempunyai baris yang setara. Angka itu **bukan** bukti sistem lulus —
ia dilaporkan di bawah label asas entry yang jelas.

### 13.11 — 27 Okt 2026: gate 8.1 tidak boleh disahkan oleh kelas yang bukan penemuan

**Kecacatan pelaksanaan, ditemui apabila 2020 siap.** Gate 8.1 seperti ditulis ("kelas sama dalam
≥ 2 tahun lain") dilaksanakan secara literal, jadi `macd_cross&q1:sektor_1b` dilabel **DITERIMA**
pada 2020 kerana kelasnya **TIDAK BERGUNA** pada kesemua enam tahun — "sama" pada 5/5 tahun lain.
Signal itu memasuki corong melalui laluan `lift_presisi ≥ 3` (Step 4.5), bukan melalui kelasnya.

Kekonsistenan "tidak berguna" bukan pengesahan. Dikunci: **G2 hanya boleh dinilai jika kelas tahun
itu sendiri ialah TERAS, UNIQUE atau LANGKA** (kelas yang arahan anggap penemuan). Jika tidak, G2 =
`TIDAK BOLEH DINILAI (kelas tahun ini <kelas>, bukan penemuan)` dan signal tidak boleh dinaik taraf
ke DITERIMA.

Pembetulan ini **mengetatkan** gate, bukan melonggarkannya, jadi ia tidak memihak kepada sebarang
hasil. Ia juga tidak menjawab soalan berasingan yang masih terbuka kepada pengguna: sama ada gate
8.1 patut menuntut **keputusan** CALON dalam ≥ 2 tahun lain, bukan sekadar kelas yang sama. Soalan
itu kekal keputusan pengguna.

### 13.12 — 28 Okt 2026: gate 8.1 diketatkan atas keputusan pengguna

**Keputusan pengguna 28 Okt 2026, selepas enam tahun siap.** Gate 8.1 seperti ditulis dalam arahan
v10 hanya memerlukan **kelas Step 4 yang sama** dalam ≥ 2 tahun lain. Itu menghasilkan 7 label
DITERIMA yang bercanggah dengan datanya sendiri: setiap satu daripadanya **DITOLAK** pada beberapa
tahun lain kerana gagal G4 (bootstrap) atau G5 (outlier). Kelas Step 4 ialah lift atas populasi
peristiwa; ia konsisten merentas tahun sedangkan kelebihan dagangan tidak.

Dikunci: naik taraf ke **DITERIMA** memerlukan signal **LULUS GATE KERAS** (step7 + G1 + G3 + G4 +
G5, iaitu layak berstatus CALON) dalam **≥ 2 tahun LAIN** — bukan sekadar kelas yang sama. Kelas
setiap tahun tetap dilaporkan dalam lajur `G2_merentas_tahun` untuk ketelusan, dan lajur baharu
`lulus_gate_keras` ditulis dalam `keputusan_<TAHUN>.csv` supaya tahun lain boleh membacanya.

Step 8 dijalankan **dua laluan** atas semua tahun: laluan pertama menulis `lulus_gate_keras`,
laluan kedua menilai G2 terhadap lajur itu.

Pindaan ini dibuat **selepas** melihat hasil, atas permintaan eksplisit pengguna, dan ia
**mengetatkan** gate. Ia direkod di sini supaya jelas bahawa keputusan asal (7 DITERIMA di bawah
gate v10) kekal dalam sejarah git dan tidak dipadamkan.
