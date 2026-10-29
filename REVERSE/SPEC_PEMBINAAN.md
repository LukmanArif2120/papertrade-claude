# SPEC PEMBINAAN — pradaftar, 29 Okt 2026

**Dikomit SEBELUM apa-apa keputusan dilihat.** Satu tembakan. Tiada pelarasan selepas melihat hasil.

## 1. Soalan

`REVERSE/KOLAM_EKOR.md` menunjukkan dua masalah berbeza, dan hanya satu pernah dikaji:

| | Masalah | Pernah dikaji? |
|---|---|---|
| 1 | Pemicu tiada kelebihan | **Ya** — fasa 1, 1b, 2 SEC: semuanya DITOLAK |
| 2 | Pembinaan portfolio menjauhi ekor kanan kolam | **Tidak** |

Soalan tunggal yang diuji di sini:

> **Bolehkah pembinaan portfolio sahaja — TANPA pemicu sama sekali — mengalahkan penanda aras pasif patuh Syariah pada kedua-dua paksi (pulangan DAN MDD)?**

Ini **bukan** ujian signal. Masuk adalah **rawak** dengan sengaja: itu menetapkan kelebihan pemicu
kepada tepat sifar supaya hanya pembinaan yang diukur. Jika pembinaan sahaja tidak cukup, maka
sebarang pemicu mesti membekalkan seluruh jurang, dan kita sudah mengukur bahawa ia tidak boleh.

## 2. Bukan penalaan parameter

`ARAHAN` melarang penalaan ("TIADA penalaan parameter. Optuna dan mana-mana pengoptimum TIDAK
digunakan"). Ujian ini mematuhinya:

- Grid **6 konfigurasi** ditetapkan di bawah dan **tidak akan dilebarkan** selepas melihat hasil.
- Tiada pengoptimum. Tiada carian. Tiada pemilihan konfigurasi terbaik sebagai "dapatan".
- Nilai parameter diwarisi daripada tempat lain dalam repo, bukan dicari: henti −2×ATR14
  (`pul_henti2atr`, dipakai seluruh REVERSE), Chandelier 4×ATR14 (lorong 2, `CLAUDE.md`),
  ufuk 63 sesi (`SPEC.md` §2), 8 slot (`SPEC.md` §3).
- Yang baharu hanyalah **40 slot** sebagai pasangan A/B kepada 8, kerana `KEPEKATAN.md` sudah
  mengukur 8–60 dan 40 berada dalam julat yang diukur itu.

## 3. Populasi

- Alam: Release `autotune-data-a02` (~3,300 ticker AS), sama seperti `KOLAM_EKOR.md`.
- Tempoh: **2012-01-01 hingga 2025-12-31** (14 tahun penuh).
- Layak pada tarikh masuk `t`: ada bar pada `t`, ATR14 terhingga, dan median nilai dagangan 20 bar
  **≥ USD 100,000** (ambang repo sendiri, `kod/tidak_layak.py`).
- Panjang sahaja. Tiada jual pendek, tiada margin, tiada leverage (margin = riba).
- Tunai tidak berbunga (0%). Itu merugikan sistem berbanding realiti dan dikekalkan dengan sengaja.

## 4. Masuk — tiada pemicu

- Tarikh masuk = **bar dagangan terakhir setiap bulan kalendar** (12 setahun).
- Pada setiap tarikh masuk, slot kosong diisi daripada **pilih atur rawak** senarai layak,
  mengecualikan nama yang sudah dipegang.
- Masuk pada **buka esok** selepas tarikh sauh, dengan kos satu sisi.
- Saiz = `ekuiti_semasa / bilangan_slot` pada masa masuk. Slot yang tidak terisi kekal tunai.

## 5. Keluar — tiga peraturan

| Kod | Peraturan |
|---|---|
| `H63S` | Pegang 63 sesi, ATAU henti keras `harga_masuk − 2×ATR14(masuk)` pada sentuhan pertama — mana dahulu. **Ini pembinaan kajian sendiri.** |
| `H63` | Pegang 63 sesi. Tiada henti keras. |
| `TRAIL` | Chandelier: keluar apabila tutup < (tutup tertinggi sejak masuk − 4×ATR14(masuk)). **Tiada had ufuk** — pemenang dibiarkan berjalan. |

Keluar pada buka hari berikutnya selepas syarat dipenuhi, dengan kos satu sisi. Posisi yang masih
terbuka pada 2025-12-31 ditutup pada tutup akhir.

## 6. Grid — tepat 6 konfigurasi

| Nama | Slot | Keluar | Niat |
|---|---|---|---|
| `A8` | 8 | `H63S` | **Asas** — pembinaan kajian sendiri, pemicu dibuang |
| `A40` | 40 | `H63S` | kesan slot sahaja |
| `B8` | 8 | `H63` | kesan membuang henti keras sahaja |
| `B40` | 40 | `H63` | slot + tiada henti |
| `C8` | 8 | `TRAIL` | terima ekor kanan, tertumpu |
| `C40` | 40 | `TRAIL` | **terima ekor kanan, tersebar** — hipotesis penuh |

## 7. Kos

`REVERSE/teras/kos.py` tanpa perubahan: komisen 0.1% setiap sisi + slippage berperingkat ikut
median nilai 20 bar pada hari sauh (0.05% ≥ USD50j; 0.10% USD10–50j; 0.25% < USD10j).

## 8. Hingar pemilihan — 20 benih, bukan satu

`KEPEKATAN_BENIH.md` mengukur hingar pemilihan pada 8 slot = **17.3 mata peratus setahun**
(20 benih: median 9.93%, julat 2.57–19.90%). Maka satu larian ialah **satu cabutan** dan tidak
boleh ditafsir. Setiap konfigurasi dijalankan dengan **benih 1–20**, dan yang dilaporkan ialah
**median, p10 dan p90 merentas 20 benih**, bukan satu nombor.

## 9. Penanda aras

- **Utama: SPUS** (patuh Syariah), `BacktestShariah2/data/penanda_aras/spus_bulanan.csv`.
  SPUS mula Dis 2019, jadi perbandingan utama ialah **2020–2025** sahaja.
- **Kedua: SPY** bagi 14 tahun penuh, sebagai rujukan sahaja. SPY **bukan** patuh Syariah
  (`PENANDA_ARAS_SYARIAH.md`) dan tidak menentukan keputusan.
- Kedua-duanya beli-dan-pegang, tanpa kos (memihak kepada penanda aras dengan sengaja).

## 10. Peraturan keputusan — ditetapkan sekarang

Pembinaan-tanpa-pemicu **LULUS** hanya jika sekurang-kurangnya satu daripada 6 konfigurasi,
pada tempoh 2020–2025 lawan SPUS, memenuhi **KETIGA-TIGA**:

1. **Pulangan**: median 20-benih pulangan tahunan > pulangan tahunan SPUS; **dan**
2. **MDD**: median 20-benih MDD lebih cetek (kurang negatif) daripada MDD SPUS; **dan**
3. **Di luar hingar**: **p10** 20-benih pulangan tahunan masih > pulangan tahunan SPUS.

Syarat 3 adalah yang penting. Tanpanya, konfigurasi bertuah akan kelihatan seperti dapatan.

Jika tiada konfigurasi memenuhi ketiga-tiganya: **DITOLAK**. Pembinaan sahaja tidak cukup, dan
oleh kerana ruang pemicu sudah diukur dan kosong, arah ini juga ditutup.

Keputusan **tidak** bergantung pada: nisbah pulangan/MDD, Sharpe, mana-mana ukuran yang tidak
disenaraikan di atas, atau apa-apa tempoh selain 2020–2025 bagi syarat lulus.

## 11. Jangkaan priori (ditulis sebelum larian)

Saya menjangka **DITOLAK**, atas tiga sebab yang sudah diukur:

1. `KOLAM_EKOR.md` §1: saham median kolam +0.82%/bulan lawan SPY +1.82%. SPUS lebih tinggi lagi
   (2.59% bulanan). Pemilihan rawak mendarat dekat median kolam.
2. `KEPEKATAN.md`: 8→60 slot memperbaiki MDD 3.48 mata tetapi mengorbankan pulangan 5.97 mata —
   nisbah tidak pernah bertambah baik.
3. `KOLAM_EKOR.md` §2: membuang henti menaikkan min 9.79 mata/tahun tetapi memperdalam
   persentil 5 daripada −15.58% ke −54.67% setiap saham-tahun. Syarat MDD mungkin gagal tepat
   pada konfigurasi yang lulus syarat pulangan.

Jangkaan ini direkodkan supaya ia tidak boleh dilaraskan selepas fakta. Jika hasilnya LULUS,
jangkaan saya salah dan itu mesti dinyatakan dengan jelas.

## 12. Apa yang ujian ini TIDAK boleh buktikan

- Ia tidak boleh mencapai **+10%/bulan**. Tiada apa-apa dalam reka bentuk ini menghampiri
  3.14×/tahun (`SASARAN.md`). Soalan itu sudah dijawab.
- Ia tidak boleh mengesahkan mana-mana pemicu. Masuk rawak dengan sengaja.
- LULUS bermakna "pembinaan sahaja mengalahkan penanda aras pasif pada 2020–2025 dalam
  simulasi" — ia **mesti** disahkan ke hadapan sebelum dipercayai, kerana ia tetap backtest.
