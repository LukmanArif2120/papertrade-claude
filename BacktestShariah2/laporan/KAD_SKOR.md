# Kad skor keputusan (satu jawapan)

Dijana 2026-11-09 oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate: `standard/SPEC_KAD_SKOR.md` (pradaftar 2026-11-06; pindaan 2026-11-07). Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Tiada kaedah lulus. Kematangan paling awal ~2026-11-12 dan ≥ 10 hari beli dalam setiap rejim (kini ON 1, OFF 15; bergantung pasaran); portfolio lawan SPUS pada MDD -10% ~2027-04-09

**Tindakan hari ini:** JANGAN guna wang sebenar: tiada kaedah TERBUKTI. Papertrade C dan Lejar terus mengumpul data. Rejim OFF sejak 2026-10-16 (16 sesi): saham momentum paling terjejas dalam fasa ini; data hari ini dikira dalam baldi OFF.

Penyebut: **28,296 posisi LANGSUNG** Lejar Penuh lorong 1 merentas 223 kaedah, 16 hari beli (rejim ON 1, OFF 15); 35,700 posisi isian bina semula dan 14 posisi dengan data harga dikuarantin tidak dikira (Mxx sejak isyarat 2026-10-15, Nxx/GB sejak 2026-11-03). Harga pada tutup 2026-11-06.

| Status | Bilangan |
|---|---|
| NEGATIF | 0 |
| GAGAL | 0 |
| BELUM CUKUP | 223 |
| CALON | 0 |
| TERBUKTI | 0 |

## Bila keputusan boleh dibuat

- **G1 kematangan:** ≥ 20 hari beli langsung (ada 16) **dan** ≥ 10 dalam rejim ON (ada 1) **dan** ≥ 10 dalam rejim OFF (ada 15). Rejim ON = QQQ > SMA50 dan SMA10 > SMA20. Paling awal ~2026-11-12 jika rejim ON muncul cukup lama; jika pasaran kekal OFF, G1 menunggu.
- **G6 portfolio:** 126 sesi lorong T4 (paling lama 16); ~2027-04-09. Dibanding dengan SPUS **pada MDD -10%** (toleransi anda), bukan pada MDD SPUS penuh.

## 20 kaedah teratas ikut lift masuk (calon, BUKAN pangkat sehingga status berubah)

| Kaedah | Status | Posisi / tutup | Hari beli (ON/OFF) | Jangkaan % | Jika henti tergelincir % | Buku harian % [95%] | Lift masuk | Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 pada MDD -10% vs SPUS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `M01` Bollinger Band + RSI | BELUM CUKUP | 101 / 12 | 16 (1/15) | -2.45 | -2.45 | -0.502 [-1.619, +0.616] | – | 38 | 0.82 | -3.66 | 0 | 16 | -6.67 vs -5.77 |
| `M05` MACD Divergence + Pengesahan | BELUM CUKUP | 38 / 12 | 13 (1/12) | -1.57 | -1.86 | -0.128 [-0.483, +0.227] | – | 29 | 1.51 | -3.05 | 0 | 16 | +1.29 vs -5.77 |
| `M07` Qullamaggie Breakout | BELUM CUKUP | 1 / 1 | 1 (1/0) | -2.53 | -3.60 | -0.143 [-1.539, +1.253] | – | 0 | – | – | 0 | 16 | -0.25 vs -5.77 |
| `M100` Bulkowski Segi Empat & Segi  | BELUM CUKUP | 58 / 37 | 14 (1/13) | -0.36 | -0.58 | +0.039 [-0.517, +0.595] | – | 40 | 1.36 | -1.03 | 0 | 16 | +2.95 vs -5.77 |
| `M104` High Tight Flag / Power Play | BELUM CUKUP | 1 / 0 | 1 (0/1) | +10.02 | +10.02 | – [–, –] | – | 100 | – | – | 0 | 1 | +1.02 vs +0.52 |
| `M106` DMI Wilder | BELUM CUKUP | 99 / 49 | 14 (1/13) | -0.69 | -0.73 | -0.018 [-0.403, +0.368] | – | 42 | 1.05 | -1.68 | 0 | 16 | -3.49 vs -5.77 |
| `M107` Golden Cross SMA50/200 | BELUM CUKUP | 28 / 7 | 14 (1/13) | -1.35 | -1.74 | -0.045 [-0.657, +0.567] | – | 46 | 0.77 | -2.82 | 0 | 16 | -0.40 vs -5.77 |
| `M121` High 2 bull flag (Brooks) | BELUM CUKUP | 5 / 3 | 3 (0/3) | -11.65 | -11.84 | -1.234 [-3.504, +1.035] | – | 0 | – | -14.03 | 0 | 12 | -5.79 vs -4.88 |
| `M126` Hidden Smash Day (beli, Larr | BELUM CUKUP | 18 / 11 | 10 (0/10) | -4.64 | -4.92 | -0.405 [-1.214, +0.405] | – | 17 | 0.66 | -5.46 | 0 | 15 | -5.36 vs -5.08 |
| `M129` Wick Play | BELUM CUKUP | 23 / 9 | 9 (1/8) | -1.19 | -1.74 | +0.051 [-0.709, +0.810] | – | 39 | 1.27 | -3.87 | 0 | 16 | +3.56 vs -5.77 |
| `M130` 多方炮 (dua lilin hijau mengapi | BELUM CUKUP | 9 / 3 | 6 (0/6) | -3.73 | -3.83 | -0.088 [-0.951, +0.775] | – | 44 | 0.53 | -5.46 | 0 | 14 | -3.15 vs -4.75 |
| `M135` 3rd Watch | BELUM CUKUP | 12 / 2 | 7 (1/6) | -6.23 | -6.40 | -0.421 [-1.369, +0.527] | – | 8 | 0.26 | -6.96 | 0 | 16 | -7.22 vs -5.77 |
| `M138` 直升机空中加油 (Helikopter isi miny | BELUM CUKUP | 2 / 0 | 2 (0/2) | -2.53 | -2.53 | -0.269 [-0.837, +0.299] | – | 0 | – | -4.89 | 0 | 9 | -0.47 vs -5.45 |
| `M139` 均线首次粘合向上发散 (MA berhimpun kal | BELUM CUKUP | 65 / 16 | 16 (1/15) | -1.70 | -1.91 | -0.013 [-0.597, +0.572] | – | 49 | 0.71 | -3.22 | 0 | 16 | +2.96 vs -5.77 |
| `M141` First Thrust (Landry) | BELUM CUKUP | 20 / 8 | 7 (1/6) | -3.61 | -4.32 | -0.399 [-1.035, +0.236] | – | 20 | 0.54 | -4.12 | 0 | 16 | -3.94 vs -5.77 |
| `M142` Pecahan volum dari dasar (底部 | BELUM CUKUP | 37 / 4 | 12 (0/12) | +0.04 | -0.10 | -0.000 [-0.537, +0.537] | – | 46 | 1.20 | -0.93 | 0 | 14 | +1.26 vs -4.75 |
| `M143` 장대양봉 이후 눌림목 / 5일선 매매 (Undur  | BELUM CUKUP | 11 / 1 | 8 (0/8) | -1.23 | -1.23 | -0.525 [-1.720, +0.669] | – | 64 | 0.31 | -1.81 | 0 | 15 | -1.16 vs -5.08 |
| `M144` Screw Bar | BELUM CUKUP | 8 / 6 | 5 (0/5) | -2.88 | -2.88 | -1.546 [-4.387, +1.295] | – | 25 | 0.96 | -4.29 | 0 | 14 | -2.25 vs -4.75 |
| `M145` Yum-Yum Continuation | BELUM CUKUP | 276 / 53 | 16 (1/15) | -0.87 | -1.06 | +0.005 [-0.474, +0.483] | – | 44 | 1.00 | -1.95 | 0 | 16 | +2.21 vs -5.77 |
| `M147` Improved Three-Bar Pullback | BELUM CUKUP | 95 / 27 | 14 (1/13) | -3.15 | -3.56 | -0.261 [-0.634, +0.111] | – | 39 | 0.71 | -4.41 | 0 | 16 | +1.83 vs -5.77 |

## Cara membaca

- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.**
- **Lift masuk** = adakah kaedah memilih saham lebih baik daripada saham lain yang Lejar beli pada hari sama dan tahap turun-naik sama, diukur 10 sesi (bebas peraturan keluar). Disahkan plasebo: `laporan/PLASEBO_GATE.md`.
- **Buku harian** = pulangan harian purata jika setiap isyarat kaedah itu diberi modal sama dan keluar ikut peraturannya sendiri. Selang 95% Newey-West mengambil kira bahawa semua posisi bergerak bersama pasaran.
- **Jika henti tergelincir** = jangkaan jika setiap keluar henti intrahari diisi pada titik tengah antara paras henti dan harga rendah hari itu (Lejar mengandaikan isian tepat pada henti; rendah hari itu di bawah henti pada ~95% kes). Maklumat sahaja: anggaran kos realistik pelaksanaan, bukan gate.
- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif.
- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan.
- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.

