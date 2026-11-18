# Kad skor keputusan (satu jawapan)

Dijana 2026-11-18 oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate: `standard/SPEC_KAD_SKOR.md` (pradaftar 2026-11-06; pindaan 2026-11-07). Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Tiada kaedah lulus. Kematangan paling awal ~2026-11-17 dan ≥ 10 hari beli dalam setiap rejim (kini ON 1, OFF 22; bergantung pasaran); portfolio lawan SPUS pada MDD -10% ~2027-04-09

**Tindakan hari ini:** JANGAN guna wang sebenar: tiada kaedah TERBUKTI. Papertrade C dan Lejar terus mengumpul data. Rejim OFF sejak 2026-10-16 (23 sesi): saham momentum paling terjejas dalam fasa ini; data hari ini dikira dalam baldi OFF.

Penyebut: **42,436 posisi LANGSUNG** Lejar Penuh lorong 1 merentas 226 kaedah, 23 hari beli (rejim ON 1, OFF 22); 36,202 posisi isian bina semula dan 94 posisi dengan data harga dikuarantin tidak dikira (Mxx sejak isyarat 2026-10-15, Nxx/GB sejak 2026-11-03). Harga pada tutup 2026-11-17.

| Status | Bilangan |
|---|---|
| NEGATIF | 0 |
| GAGAL | 0 |
| BELUM CUKUP | 226 |
| CALON | 0 |
| TERBUKTI | 0 |

## Bila keputusan boleh dibuat

- **G1 kematangan:** ≥ 20 hari beli langsung (ada 23) **dan** ≥ 10 dalam rejim ON (ada 1) **dan** ≥ 10 dalam rejim OFF (ada 22). Rejim ON = QQQ > SMA50 dan SMA10 > SMA20. Paling awal ~2026-11-17 jika rejim ON muncul cukup lama; jika pasaran kekal OFF, G1 menunggu.
- **G6 portfolio:** 126 sesi lorong T4 (paling lama 23); ~2027-04-09. Dibanding dengan SPUS **pada MDD -10%** (toleransi anda), bukan pada MDD SPUS penuh.

## 20 kaedah teratas ikut lift masuk (calon, BUKAN pangkat sehingga status berubah)

| Kaedah | Status | Posisi / tutup | Hari beli (ON/OFF) | Jangkaan % | Jika henti tergelincir % | Buku harian % [95%] | Lift masuk | Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 pada MDD -10% vs SPUS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `M01` Bollinger Band + RSI | BELUM CUKUP | 112 / 25 | 20 (1/19) | -0.98 | -0.98 | -0.294 [-1.085, +0.497] | – | 43 | 1.08 | -2.47 | 0 | 23 | -8.49 vs -8.18 |
| `M05` MACD Divergence + Pengesahan | BELUM CUKUP | 41 / 12 | 15 (1/14) | -2.31 | -2.57 | -0.125 [-0.480, +0.230] | – | 22 | 1.78 | -4.46 | 0 | 23 | +0.30 vs -8.18 |
| `M07` Qullamaggie Breakout | BELUM CUKUP | 1 / 1 | 1 (1/0) | -2.53 | -3.60 | -0.143 [-1.539, +1.253] | – | 0 | – | – | 0 | 23 | -0.25 vs -8.18 |
| `M100` Bulkowski Segi Empat & Segi  | BELUM CUKUP | 60 / 41 | 15 (1/14) | -0.58 | -0.79 | -0.007 [-0.430, +0.416] | – | 40 | 1.27 | -1.23 | 0 | 23 | +0.36 vs -8.18 |
| `M104` High Tight Flag / Power Play | BELUM CUKUP | 1 / 0 | 1 (0/1) | +21.63 | +21.63 | +2.540 [-0.484, +5.564] | – | 100 | – | – | 0 | 8 | +2.18 vs -2.05 |
| `M106` DMI Wilder | BELUM CUKUP | 132 / 83 | 20 (1/19) | -1.92 | -1.96 | -0.124 [-0.537, +0.289] | – | 28 | 1.18 | -2.96 | 0 | 23 | -3.21 vs -8.18 |
| `M107` Golden Cross SMA50/200 | BELUM CUKUP | 43 / 9 | 20 (1/19) | -2.77 | -3.02 | -0.108 [-0.574, +0.359] | – | 33 | 0.77 | -3.96 | 0 | 23 | -4.97 vs -8.18 |
| `M121` High 2 bull flag (Brooks) | BELUM CUKUP | 7 / 4 | 5 (0/5) | -10.63 | -11.08 | -1.087 [-2.289, +0.115] | – | 14 | 0.05 | -12.50 | 0 | 19 | -7.34 vs -7.31 |
| `M126` Hidden Smash Day (beli, Larr | BELUM CUKUP | 21 / 11 | 11 (0/11) | -3.84 | -4.16 | -0.239 [-0.716, +0.238] | – | 29 | 0.49 | -4.88 | 0 | 22 | -5.12 vs -7.51 |
| `M129` Wick Play | BELUM CUKUP | 26 / 10 | 10 (1/9) | -2.40 | -2.95 | -0.035 [-0.563, +0.492] | – | 35 | 1.24 | -4.98 | 0 | 23 | +2.50 vs -8.18 |
| `M130` 多方炮 (dua lilin hijau mengapi | BELUM CUKUP | 12 / 3 | 8 (0/8) | -5.81 | -5.89 | -0.232 [-0.940, +0.476] | – | 17 | 0.82 | -7.59 | 0 | 21 | -6.69 vs -7.19 |
| `M135` 3rd Watch | BELUM CUKUP | 15 / 4 | 9 (1/8) | -9.88 | -10.02 | -0.548 [-1.337, +0.242] | – | 27 | 0.10 | -10.77 | 0 | 23 | -6.32 vs -8.18 |
| `M138` 直升机空中加油 (Helikopter isi miny | BELUM CUKUP | 4 / 0 | 4 (0/4) | -3.30 | -3.30 | -0.274 [-0.612, +0.063] | – | 0 | – | -4.29 | 0 | 16 | -1.24 vs -7.87 |
| `M139` 均线首次粘合向上发散 (MA berhimpun kal | BELUM CUKUP | 89 / 33 | 22 (1/21) | -3.78 | -4.06 | -0.151 [-0.642, +0.340] | – | 31 | 0.86 | -5.07 | 0 | 23 | -1.36 vs -8.18 |
| `M141` First Thrust (Landry) | BELUM CUKUP | 26 / 16 | 8 (1/7) | -7.85 | -8.56 | -0.696 [-1.618, +0.227] | – | 23 | 0.30 | -9.18 | 0 | 23 | -9.32 vs -8.18 |
| `M142` Pecahan volum dari dasar (底部 | BELUM CUKUP | 54 / 7 | 16 (0/16) | -1.92 | -2.01 | -0.061 [-0.645, +0.523] | – | 50 | 0.50 | -2.81 | 0 | 21 | +1.29 vs -7.19 |
| `M143` 장대양봉 이후 눌림목 / 5일선 매매 (Undur  | BELUM CUKUP | 28 / 3 | 14 (0/14) | -2.92 | -3.07 | -0.439 [-1.282, +0.403] | – | 25 | 0.43 | -3.47 | 0 | 22 | -2.02 vs -7.51 |
| `M144` Screw Bar | BELUM CUKUP | 10 / 7 | 7 (0/7) | -2.72 | -2.72 | -0.573 [-1.970, +0.823] | – | 20 | 1.05 | -3.66 | 0 | 21 | -2.64 vs -7.19 |
| `M145` Yum-Yum Continuation | BELUM CUKUP | 309 / 73 | 22 (1/21) | -2.26 | -2.48 | -0.069 [-0.470, +0.332] | – | 37 | 0.95 | -3.55 | 0 | 23 | +3.29 vs -8.18 |
| `M150` Trend Bar Failure (Brooks) | BELUM CUKUP | 107 / 53 | 21 (1/20) | -1.04 | -1.12 | -0.090 [-0.390, +0.211] | – | 28 | 1.59 | -2.03 | 0 | 23 | -5.94 vs -8.18 |

## Cara membaca

- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.**
- **Lift masuk** = adakah kaedah memilih saham lebih baik daripada saham lain yang Lejar beli pada hari sama dan tahap turun-naik sama, diukur 10 sesi (bebas peraturan keluar). Disahkan plasebo: `laporan/PLASEBO_GATE.md`.
- **Buku harian** = pulangan harian purata jika setiap isyarat kaedah itu diberi modal sama dan keluar ikut peraturannya sendiri. Selang 95% Newey-West mengambil kira bahawa semua posisi bergerak bersama pasaran.
- **Jika henti tergelincir** = jangkaan jika setiap keluar henti intrahari diisi pada titik tengah antara paras henti dan harga rendah hari itu (Lejar mengandaikan isian tepat pada henti; rendah hari itu di bawah henti pada ~95% kes). Maklumat sahaja: anggaran kos realistik pelaksanaan, bukan gate.
- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif.
- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan.
- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.

