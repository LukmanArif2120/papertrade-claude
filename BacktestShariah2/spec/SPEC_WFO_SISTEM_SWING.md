# SPEC W01 — Sistem Swing Momentum Adaptif (Walk-Forward Optimization)

**Tarikh:** 15 Okt 2026 · **Status:** DRAF, menunggu kelulusan pengguna · **Enjin:** v1.2 (beku, tidak diubah)

## 1. Tujuan

Mencari gabungan **entry + stop loss + exit + tempoh pegangan** terbaik untuk swing momentum carta harian, dan menala semula gabungan itu secara berkala tanpa pandang ke hadapan.

**Objektif (dipilih pengguna):** CAGR maksimum dengan syarat MDD ≥ −35%.

W01 tidak menggantikan kaedah M. Varian beku dalam registry kekal. W01 ialah satu sistem baharu yang dibandingkan dengan M96 V1 dan EW.

## 2. Data

- Alam utama: set 431 (`data_mentah/dataset_S1–S4.csv`) **tolak 8 saham bermasalah** (ASST, FCEL, MTDR, OVV, PR, SM, VAL, XENE) = **423 saham**. Sebab: `LAPORAN_UTAMA.md` Bahagian 10 (dagangan FCEL +780% mengherotkan keputusan).
- Indeks: `index_benchmark.csv` (SPY, QQQ).
- Tempoh data: 2 Jan 2019 – 2 Okt 2026, bar harian.
- Ujian kekukuhan: set 431 penuh dan setiap subset S1–S4 (tolak 8 saham itu).

## 3. Batasan enjin v1.2 (menentukan apa yang boleh diuji)

Daripada `kod/enjin.py`:
- Masuk pada **buka hari selepas isyarat**. Kos 0.1% setiap belah.
- `stop` dibaca **sekali sahaja pada hari isyarat** dan kekal tetap. Henti mengekor tidak boleh dibuat melalui `stop`; ia dibuat melalui `exitc`.
- `exitc` benar → keluar pada **buka hari berikutnya**.
- `tgt` dibaca dari bar sebelumnya. Sasaran peratus tetap dari harga masuk tidak boleh dinyatakan; oleh itu sasaran hanya wujud melalui pilihan ASAL (§4.3).
- `tmax` = had hari pegangan.
- Satu posisi setiap saham pada satu masa. Portfolio 8 slot × 12.5%; keutamaan slot ikut lajur `rank`.

## 4. Ruang carian

### 4.1 Entry (isyarat `sig` dan `rank` daripada `sedia()` modul sedia ada)

| Kod | Kaedah | Varian (registry) |
|---|---|---|
| M96 | Momo India Ranking Sharpe | V1 Dikunci |
| M30 | BB Free Bar + Himpitan | V3 BB20/2 |
| M79 | Radge 20% Flipper | V3 A=0.15 |
| M111 | Sistem Volatiliti Wilder | V5 |
| M74 | Lulus Baharu Trend Template Minervini | V2 |
| M05 | MACD Divergence + Pengesahan | V3 |
| M80 | Radge Saluran Purata Bergerak (MAC) | V2 |
| M37 | Weinstein Peringkat 2 | V2 |
| M04 | BB Squeeze Breakout | U2 |

- **Dikecualikan:** M114 (tiada modul `kod/kaedah/M114.py`), M40 dan M45 (isyarat bergantung pada pra-simulasi 8 slot kaedah itu sendiri, jadi tidak boleh dipisahkan daripada exit asalnya).
- Syarat kelayakan modul: `sig` hari *i* hanya bergantung pada data ≤ *i* dan tidak bergantung pada posisi kaedah itu sendiri. Modul yang gagal semakan ini dibuang sebelum backtest dan dicatat dalam laporan.

### 4.2 Stop loss (lajur `stop`, ditetapkan pada hari isyarat)

| Kod | Formula | Parameter |
|---|---|---|
| S-PCT | tutup × (1 − p) | p ∈ {0.06, 0.08, 0.10, 0.12, 0.15} |
| S-ATR | tutup − k × ATR14 | k ∈ {1.5, 2, 2.5, 3, 3.5, 4} |
| S-LOW | low terendah n hari terakhir | n ∈ {1, 5, 10} |
| S-ASAL | `stop` asal modul | — |

**Had global:** stop = maks(stop, 0.85 × tutup). Sebab: gate G1 (purata rugi ≥ −12%).

### 4.3 Exit (lajur `exitc`; keluar buka hari berikutnya)

| Kod | Syarat keluar | Parameter |
|---|---|---|
| E-MA | tutup < purata bergerak | EMA10, EMA21, SMA20, SMA50 |
| E-CHAN | tutup < high tertinggi 22 hari − k × ATR22 (Chandelier) | k ∈ {2, 3, 4} |
| E-ASAL | `exitc` dan `tgt` asal modul | — |
| E-TIADA | tiada; bergantung pada stop dan had masa sahaja | — |

### 4.4 Tempoh pegangan (`tmax`)

{10, 21, 42, 63, tiada had} hari dagangan. Gabungan E-TIADA + tiada had tidak dibenarkan.

**Saiz ruang:** 9 entry × 15 stop × 9 exit × 5 tmax ≈ 6,000 gabungan.

## 5. Prosedur walk-forward

1. **Jana isyarat entry sekali** atas data penuh untuk setiap modul (dibenarkan kerana `sig` tanpa pandang ke hadapan, §4.1).
2. **Tetingkap latihan:** 3 tahun kalendar bergolek. **Tetingkap ujian:** 1 suku tahun berikutnya.
   - Suku ujian pertama: 2023 S1 (latihan 2020-01-01 – 2022-12-31).
   - Suku ujian terakhir: 2026 S3 (data hingga 2 Okt 2026). Jumlah 15 suku luar sampel.
3. **Dalam setiap tetingkap latihan:** Optuna (pensampel TPE, benih tetap 42) menguji 150 gabungan. Setiap percubaan = `trades()` + `portfolio()` enjin v1.2 atas dagangan yang masuk dalam tetingkap latihan sahaja.
   - Nilai percubaan = CAGR tetingkap latihan.
   - Ditolak (nilai −∞) jika MDD < −35% atau bilangan dagangan < 30.
4. **Pilihan kukuh:** daripada 10 percubaan teratas, pilih yang mempunyai **pulangan tahunan terendah paling tinggi** dalam 3 tahun latihan (elak gabungan yang bergantung pada satu tahun bertuah).
5. **Luar sampel:** gabungan terpilih menjana dagangan yang **masuk** dalam suku ujian. Dagangan dibiarkan berjalan hingga exit sendiri walaupun melepasi hujung suku.
6. Dagangan luar sampel 15 suku digabungkan, kemudian dijalankan melalui `portfolio()` enjin v1.2 sekali → satu lengkung ekuiti luar sampel 2023-01-01 – 2026-10-02.
7. **Tetapan semasa:** gabungan yang dipilih untuk tetingkap terkini disimpan ke `data/wfo/W01_parameter_semasa.json` (untuk uji kertas, jika lulus).

## 6. Penanda aras (tempoh luar sampel yang sama)

- M96 V1 (varian beku) — dagangan masuk ≥ 2023-01-01, `portfolio()` yang sama.
- Kaedah entry terbaik dengan exit/stop asal (varian beku) dalam tempoh sama.
- EW 423 saham, SPY, QQQ.

## 7. Kriteria lulus

W01 **LULUS** jika semua benar dalam tempoh luar sampel:
1. CAGR W01 > CAGR M96 V1 **dan** > CAGR EW.
2. MDD W01 ≥ −35%.
3. Bilangan dagangan ≥ 60.
4. Mengalahkan EW dalam sekurang-kurangnya 3/4 subset S1–S4.
5. Tiada satu saham menyumbang > 25% jumlah keuntungan.

Jika gagal → DITOLAK. Varian beku kekal digunakan dan WFO dihentikan.

**Nota:** skor dan gate v1.2 (`skor()`, `gate()`) menggunakan H1 hingga 2022-12-31, sebelum tempoh luar sampel bermula. Ia dilaporkan sebagai rujukan atas lengkung penuh sahaja, bukan sebagai kriteria lulus.

## 8. Output

- `kod/wfo.py` — skrip WFO (mengimport `enjin.py` tanpa ubah).
- `ujian/test_wfo.py` — ujian unit: tiada pandang ke hadapan (isyarat hari *i* tidak berubah apabila data selepas *i* dibuang), had stop 15%, pemisahan tetingkap.
- `data/wfo/W01_pilihan.csv` — gabungan terpilih setiap suku, dengan metrik latihan.
- `data/wfo/W01_dagangan_oos.csv` — semua dagangan luar sampel.
- `laporan/W01_LAPORAN.md` — keputusan, perbandingan penanda aras, kestabilan pilihan antara suku, verdict.

## 9. Pelaksanaan dan peraturan projek

- Satu chat menguji satu sistem. Backtest dijalankan dengan Opus 5.5.
- Pakej: `scikit-learn` tidak diperlukan untuk fasa ini; `optuna` diperlukan.
- Sebelum WFO penuh: ukur masa satu percubaan. Jika > 5 saat, bilangan percubaan dikurangkan kepada 75 dan dicatat dalam laporan.
- Penalaan semula berjadual (setiap suku) hanya dibina **selepas** W01 LULUS.

## 10. Andaian (perlu disahkan pengguna)

1. Tetingkap latihan 3 tahun dan suku ujian 3 bulan.
2. Alam utama 423 saham (tolak 8 saham bermasalah).
3. 150 percubaan Optuna bagi setiap suku.
4. Sasaran harga hanya melalui E-ASAL; tiada sasaran peratus tetap (batasan enjin, §3).
5. Kriteria lulus §7.

## 11. Pindaan 15 Okt 2026 (arahan pengguna)

- Skop diluaskan: WFO stop/exit/tmax dijalankan **berasingan bagi setiap kaedah M** (87 modul; M40 dan M45 tidak layak, dan mana-mana modul yang gagal semakan pandang ke hadapan). Syarat entry setiap kaedah kekal ikut varian registry. W01 gabungan (entry turut dipilih, §4.1) dijalankan selepas semua kaedah siap.
- Bandingan setiap kaedah: versi WFO lawan varian beku sendiri dalam tempoh luar sampel yang sama.
- Suku ujian: 2023 S1 hingga 2026 S4 (2026 S4 hanya 1–2 Okt 2026) = 16 suku.
- Semakan pandang ke hadapan: `sig` dikira atas data penuh dan atas data dipotong pada 28 Jun 2024; sebarang beza = tidak layak.
- Subset S1–S4: gabungan terpilih yang sama (tidak ditala semula) dinilai atas alam subset.
- Larian: 5 kaedah serentak (`kod/wfo.py kelompok 5`); keputusan di `data/wfo/hasil/`. Kerja berhenti di Fasa C (laporan).
- Laporan menyertakan pembetulan ujian berganda (deflated Sharpe ratio) merentas semua kaedah.
