# Kad skor keputusan (satu jawapan)

Dijana 2026-11-17 oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate: `standard/SPEC_KAD_SKOR.md` (pradaftar 2026-11-06; pindaan 2026-11-07). Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Tiada kaedah lulus. Kematangan paling awal ~2026-11-16 dan ≥ 10 hari beli dalam setiap rejim (kini ON 1, OFF 21; bergantung pasaran); portfolio lawan SPUS pada MDD -10% ~2027-04-09

**Tindakan hari ini:** JANGAN guna wang sebenar: tiada kaedah TERBUKTI. Papertrade C dan Lejar terus mengumpul data. Rejim OFF sejak 2026-10-16 (22 sesi): saham momentum paling terjejas dalam fasa ini; data hari ini dikira dalam baldi OFF.

Penyebut: **41,586 posisi LANGSUNG** Lejar Penuh lorong 1 merentas 226 kaedah, 22 hari beli (rejim ON 1, OFF 21); 36,202 posisi isian bina semula dan 52 posisi dengan data harga dikuarantin tidak dikira (Mxx sejak isyarat 2026-10-15, Nxx/GB sejak 2026-11-03). Harga pada tutup 2026-11-16.

| Status | Bilangan |
|---|---|
| NEGATIF | 0 |
| GAGAL | 0 |
| BELUM CUKUP | 226 |
| CALON | 0 |
| TERBUKTI | 0 |

## Bila keputusan boleh dibuat

- **G1 kematangan:** ≥ 20 hari beli langsung (ada 22) **dan** ≥ 10 dalam rejim ON (ada 1) **dan** ≥ 10 dalam rejim OFF (ada 21). Rejim ON = QQQ > SMA50 dan SMA10 > SMA20. Paling awal ~2026-11-16 jika rejim ON muncul cukup lama; jika pasaran kekal OFF, G1 menunggu.
- **G6 portfolio:** 126 sesi lorong T4 (paling lama 22); ~2027-04-09. Dibanding dengan SPUS **pada MDD -10%** (toleransi anda), bukan pada MDD SPUS penuh.

## 20 kaedah teratas ikut lift masuk (calon, BUKAN pangkat sehingga status berubah)

| Kaedah | Status | Posisi / tutup | Hari beli (ON/OFF) | Jangkaan % | Jika henti tergelincir % | Buku harian % [95%] | Lift masuk | Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 pada MDD -10% vs SPUS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `M01` Bollinger Band + RSI | BELUM CUKUP | 113 / 26 | 20 (1/19) | +0.06 | +0.06 | -0.245 [-1.060, +0.569] | – | 45 | 1.23 | -1.66 | 0 | 22 | -8.46 vs -5.15 |
| `M05` MACD Divergence + Pengesahan | BELUM CUKUP | 41 / 12 | 15 (1/14) | -1.23 | -1.50 | -0.063 [-0.363, +0.237] | – | 34 | 1.33 | -3.42 | 0 | 22 | +2.15 vs -5.15 |
| `M07` Qullamaggie Breakout | BELUM CUKUP | 1 / 1 | 1 (1/0) | -2.53 | -3.60 | -0.143 [-1.539, +1.253] | – | 0 | – | – | 0 | 22 | -0.25 vs -5.15 |
| `M100` Bulkowski Segi Empat & Segi  | BELUM CUKUP | 60 / 41 | 15 (1/14) | -0.29 | -0.50 | +0.035 [-0.364, +0.435] | – | 43 | 1.20 | -0.93 | 0 | 22 | +1.83 vs -5.15 |
| `M104` High Tight Flag / Power Play | BELUM CUKUP | 1 / 0 | 1 (0/1) | +20.90 | +20.90 | +2.818 [-0.403, +6.038] | – | 100 | – | – | 0 | 7 | +2.11 vs +1.18 |
| `M106` DMI Wilder | BELUM CUKUP | 130 / 76 | 20 (1/19) | -1.23 | -1.26 | -0.055 [-0.391, +0.281] | – | 32 | 1.31 | -2.36 | 0 | 22 | -1.10 vs -5.15 |
| `M107` Golden Cross SMA50/200 | BELUM CUKUP | 41 / 8 | 19 (1/18) | -1.16 | -1.42 | -0.021 [-0.440, +0.397] | – | 46 | 0.80 | -2.55 | 0 | 22 | -1.93 vs -5.15 |
| `M121` High 2 bull flag (Brooks) | BELUM CUKUP | 7 / 4 | 5 (0/5) | -10.20 | -10.65 | -1.092 [-2.365, +0.181] | – | 14 | 0.07 | -12.05 | 0 | 18 | -7.06 vs -4.25 |
| `M126` Hidden Smash Day (beli, Larr | BELUM CUKUP | 21 / 11 | 11 (0/11) | -3.35 | -3.66 | -0.202 [-0.708, +0.304] | – | 33 | 0.50 | -4.33 | 0 | 21 | -4.80 vs -4.46 |
| `M129` Wick Play | BELUM CUKUP | 26 / 10 | 10 (1/9) | -1.40 | -1.95 | +0.032 [-0.460, +0.525] | – | 38 | 1.26 | -4.26 | 0 | 22 | +4.04 vs -5.15 |
| `M130` 多方炮 (dua lilin hijau mengapi | BELUM CUKUP | 12 / 3 | 8 (0/8) | -4.61 | -4.69 | -0.164 [-0.842, +0.515] | – | 17 | 1.16 | -6.43 | 0 | 20 | -5.25 vs -4.12 |
| `M135` 3rd Watch | BELUM CUKUP | 15 / 3 | 9 (1/8) | -4.41 | -4.56 | -0.255 [-0.858, +0.348] | – | 27 | 0.30 | -4.99 | 0 | 22 | -5.45 vs -5.15 |
| `M138` 直升机空中加油 (Helikopter isi miny | BELUM CUKUP | 3 / 0 | 3 (0/3) | -3.32 | -3.32 | -0.239 [-0.568, +0.089] | – | 0 | – | -4.37 | 0 | 15 | -0.93 vs -4.82 |
| `M139` 均线首次粘合向上发散 (MA berhimpun kal | BELUM CUKUP | 89 / 28 | 22 (1/21) | -2.91 | -3.17 | -0.100 [-0.555, +0.355] | – | 36 | 0.89 | -4.21 | 0 | 22 | -0.58 vs -5.15 |
| `M141` First Thrust (Landry) | BELUM CUKUP | 26 / 13 | 8 (1/7) | -3.78 | -4.40 | -0.358 [-0.771, +0.055] | – | 35 | 0.46 | -4.81 | 0 | 22 | -5.52 vs -5.15 |
| `M142` Pecahan volum dari dasar (底部 | BELUM CUKUP | 54 / 5 | 16 (0/16) | +0.67 | +0.58 | +0.077 [-0.353, +0.507] | – | 56 | 1.08 | -0.15 | 0 | 20 | +2.96 vs -4.12 |
| `M143` 장대양봉 이후 눌림목 / 5일선 매매 (Undur  | BELUM CUKUP | 28 / 1 | 14 (0/14) | -1.58 | -1.58 | -0.393 [-1.272, +0.486] | – | 32 | 0.77 | -2.25 | 0 | 21 | -0.35 vs -4.46 |
| `M144` Screw Bar | BELUM CUKUP | 10 / 7 | 7 (0/7) | -2.07 | -2.07 | -0.454 [-1.898, +0.991] | – | 20 | 1.60 | -3.39 | 0 | 20 | -2.00 vs -4.12 |
| `M145` Yum-Yum Continuation | BELUM CUKUP | 308 / 67 | 21 (1/20) | -0.74 | -0.95 | +0.014 [-0.317, +0.344] | – | 46 | 0.98 | -2.09 | 0 | 22 | +4.85 vs -5.15 |
| `M150` Trend Bar Failure (Brooks) | BELUM CUKUP | 104 / 48 | 20 (1/19) | -0.41 | -0.49 | -0.042 [-0.302, +0.218] | – | 37 | 1.46 | -1.46 | 0 | 22 | -5.46 vs -5.15 |

## Cara membaca

- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.**
- **Lift masuk** = adakah kaedah memilih saham lebih baik daripada saham lain yang Lejar beli pada hari sama dan tahap turun-naik sama, diukur 10 sesi (bebas peraturan keluar). Disahkan plasebo: `laporan/PLASEBO_GATE.md`.
- **Buku harian** = pulangan harian purata jika setiap isyarat kaedah itu diberi modal sama dan keluar ikut peraturannya sendiri. Selang 95% Newey-West mengambil kira bahawa semua posisi bergerak bersama pasaran.
- **Jika henti tergelincir** = jangkaan jika setiap keluar henti intrahari diisi pada titik tengah antara paras henti dan harga rendah hari itu (Lejar mengandaikan isian tepat pada henti; rendah hari itu di bawah henti pada ~95% kes). Maklumat sahaja: anggaran kos realistik pelaksanaan, bukan gate.
- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif.
- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan.
- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.

