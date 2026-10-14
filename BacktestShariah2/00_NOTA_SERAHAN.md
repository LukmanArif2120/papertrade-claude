# Nota Serahan: Backtest Shariah → Backtest Shariah 2

Tarikh: 13 Oktober 2026. Pemilik: Abd Azim Abu Hasan.

Project asal "Backtest Shariah" telah penuh. Ruang pengetahuannya sudah 99.2% digunakan (1.98 juta daripada 2.0 juta). Pakej ini memindahkan semua kerja yang masih diperlukan ke Project baharu dalam bentuk yang padat. Baca nota ini dahulu sebelum memulakan apa-apa tugasan dalam Project 2.

## 1. Matlamat

Tujuannya ialah mencari kaedah entry, tempoh pegang dan exit yang terbaik untuk swing momentum saham Shariah. Sasarannya ialah untung minimum 10% sebulan, dengan tempoh pegangan kira-kira sebulan. Kaedah yang mempunyai peluang menang paling tinggi lebih diutamakan.

Satu kaedah hanya dianggap berjaya jika ia juga mengalahkan penanda aras, iaitu membeli semua saham Shariah secara sama berat (EW). Portfolio backtest menggunakan 8 slot, dengan setiap slot 12.5% daripada modal.

## 2. Peraturan kerja (wajib)

- Setiap chat menguji 1 kaedah dan menghasilkan 1 keputusan. Selepas itu, keputusan dibandingkan dengan kaedah lain.
- Jika ada perkara yang tidak jelas, tanya pengguna dahulu.
- Jangan reka atau andaikan perkara yang tidak pasti.
- Setiap kaedah baharu mesti ada spec terperinci dalam Project sebelum /step2 dijalankan. Jika ada perkara yang masih tidak dapat disahkan, padam kaedah itu. Kaedah yang sudah OK jangan diusik.
- Enjin backtest ialah v1.2 dan ia beku (tidak boleh diubah). Gate dan skor ikut standard yang sama. Enjin ini berada dalam skill /step2 (skill akaun), bukan dalam doc Project.
- Gunakan Opus 5.5 (usaha sederhana) untuk backtest. Jangan gunakan Fable.
- Gunakan Bahasa Melayu baku untuk penerangan teknikal. Terangkan langkah demi langkah dengan jelas.

## 3. Status keputusan

**Kaedah M (88 kaedah, 550 varian atas set 431)**

Status terbaik bagi setiap kaedah:

| Status | Bilangan kaedah |
|---|---|
| GUNA | 4 |
| UJI KERTAS | 23 |
| SIMPAN | 30 |
| DITOLAK | 31 |

Kedudukan penuh ada dalam `laporan/PAPAN_KEDUDUKAN_M.md`. Lima teratas:

| # | Kaedah | Varian | Skor | CAGR |
|---|---|---|---|---|
| 1 | M96 Momo India Sharpe | V1 | 80.3 | 40.0% |
| 2 | M114 RS Peneraju Pasaran Naik | V4 | 77.4 | 49.6% |
| 3 | M30 BB Free Bar + Himpitan | V3 | 76.2 | 52.0% |
| 4 | M79 Radge 20% Flipper | V3 | 75.9 | 35.5% |
| 5 | M111 Wilder Volatiliti | V5 | 74.2 | 43.0% |

**Indikator I01 hingga I32**

Semua 32 indikator ini DITOLAK secara rasmi kerana gagal gate G1. Sebabnya, peraturan exit seragam tidak mempunyai henti rugi. Kedudukan mengikut skor tanpa gate ada dalam `laporan/LAPORAN_UTAMA.md`, di bahagian RINGKASAN_I01-I32.

Exit yang digunakan untuk fasa indikator ialah: pegang selagi harga tutup di atas MA20.

**Kajian corak P01 (corak isyarat MACD) dan P02 (RS peneraju)**

Laporan peringkat ada dalam `LAPORAN_UTAMA.md`. Data mentahnya ada dalam `data/P01*.csv` dan `data/P02.csv`.

## 4. Kandungan pakej

| Fail / folder | Isi |
|---|---|
| `data/registry_M_gabung.csv` | Gabungan registry/M01–M114 (1,222 baris, set 431 + S1–S4). Lajur `id` menunjukkan kaedah. |
| `data/registry_I_gabung.csv` | Gabungan registry/I01–I32 (160 baris). |
| `data/P01*.csv`, `data/P02.csv` | Registry kajian P01 dan P02 (asal, tidak diubah). |
| `spec/SPEC_SEMUA_KAEDAH.md` | KOMPILASI M01–M31, INDEKS M34–M113, CALON K32–K144, dan semua spec M32–M114, P01, P02. Setiap spec bermula dengan tanda `<!-- FAIL ASAL: spec/... -->`. |
| `laporan/PAPAN_KEDUDUKAN_M.md` | Papan kedudukan baharu yang dijana daripada registry gabungan. |
| `laporan/LAPORAN_UTAMA.md` | RINGKASAN_I01-I32, SEMAKAN_TANPA_8_SAHAM, laporan P01, P02 dan M114. |
| `standard/` | 22 fail asal tanpa perubahan: skrip harian, skrip binaan dashboard v2, enjin P01/P02, `tugasan_v2.md`, `papertrade_harian.md`, `dashboard.md`, `binaan_v2_log.md`, `dashboard_v2.html`. |
| `papertrade/` | `moomoo.csv`, `claude.csv`, `watchlist.csv`, `senarai_beli.csv`, `sektor.csv` (asal). |
| `uji_kertas/log.csv` | Log uji kertas (asal). |

**Tidak dibawa:** laporan individu M01–M114 dan I01–I32 (.md). Semua angka kuncinya sudah ada dalam registry gabungan. Dataset `dataset_S1`–`S4.csv` dan `index_benchmark.csv` juga tidak dibawa, kerana pengguna akan memuat naiknya sendiri.

**Penting untuk skill /step2 dan /step3 dalam Project 2:** registry kini dalam bentuk satu fail gabungan, bukan satu fail bagi setiap kaedah. Untuk kaedah baharu, tambah baris ke `data/registry_M_gabung.csv`, atau simpan sebagai `registry/Mxx.csv` dan gabungkan kemudian. Begitu juga, spec lama dicari dalam `spec/SPEC_SEMUA_KAEDAH.md` menggunakan tanda `FAIL ASAL`.

## 5. Rutin harian papertrade (v2, mula 12 Okt 2026)

> **TERBATAL (14 Okt 2026).** Rutin harian kini dalam `standard/tugasan_v3.md` dan `jadual/` (Papertrade C sahaja; imbasan 8:02 malam; model Sonnet 5.5).

Peraturan penuh ada dalam `standard/tugasan_v2.md`. Ringkasannya:

- **Skop imbasan:** semua saham AS berharga lebih daripada USD10 (Shariah atau tidak). Senarai 431 diimbas dahulu.
- **Syarat beli:** hanya jika isyarat entry kaedah dipenuhi 90–100%. Beli 1 unit setiap saham.
- **Tempat beli:** Moomoo papertrade dahulu, maksimum 10 saham bagi setiap kaedah. Jika kaedah itu sudah 10/10, beli secara maya dalam "Claude Papertrade".
- **Isyarat keluar:** baris ditanda merah dan harga dibekukan. Posisi TIDAK dijual.
- **Wang sebenar:** tidak sekali-kali digunakan tanpa kelulusan pengguna.
- **Hari operasi:** hari dagangan AS sahaja.

**Dashboard (artifact):** "Papan Backtest Shariah" di https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e. Kemas kini artifact pada URL ini. Jangan cipta artifact baharu.

**Tugasan berjadual yang aktif:**

| Tugasan | Masa |
|---|---|
| Harian v2 – Imbas pasaran | 8:02 malam MYT, Isnin–Jumaat |
| Harian v2 – Beli bila pasaran AS buka | 9:35 pagi New York, Isnin–Jumaat |
| Harian v2 – Kemas kini | 6:02 pagi MYT, Selasa–Sabtu |

Arahan ketiga-tiga tugasan ini masih merujuk Projek "Backtest Shariah" dan laluan lama (contohnya `spec/`). Selepas Project 2 siap dimuat naik, arahan tugasan ini perlu dikemas kini supaya merujuk Project 2 dan laluan baharu.

## 6. Fasa seterusnya (yang telah dinyatakan pengguna)

1. Senaraikan 10 teknik terbaik.
2. Imbas Moomoo untuk mencari saham yang sesuai bagi setiap teknik.
3. Pantau prestasi setiap teknik.
4. Papertrade semua kaedah dalam registry, dan papar kaedah mana yang sedang dicuba dan yang belum.
5. Pantau juga entry manual pengguna (contohnya DCI dan MGA): selepas saham jatuh beberapa minggu, pengguna memasang alert MACD, kemudian membeli apabila MA10 melintas di atas MA20.
