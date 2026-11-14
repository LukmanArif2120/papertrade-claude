# CS08: lorong KEDUA — beli selepas pengesahan uptrend, pegang sampai trend tamat (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-12):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_trend8.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (q), dikomit sebelum dijalankan. **Jangan sunting secara manual.** Lorong ini BERASINGAN daripada swing 4 minggu (keluarga F); ID `T..` bukan kod F.

## 1. Apa yang dicari

- Permintaan pengguna (kes MXL): tunggu pengesahan uptrend besar, beli di tengah, pegang sampai trend tamat.
- **Pelari besar** = selepas beli, tutup mencapai ≥ +50% dalam 126 sesi (≈ 6 bulan) SEBELUM mana-mana tutup ≤ −15%. Saham rawak (mana-mana hari, kumpulan B): **7.9 %** jadi pelari besar; 1.4 % capai +100 %.
- Dicari pada kumpulan A: 2,628 pencetus (500 asal, 656 K, 1,072 M1, 400 M2) × 544 gabungan prasyarat × 379 gabungan penapis; 2,481 cukup isyarat, 2,300 dengan skor > 0.
- Keluar: 38 indikator trend tamat × 3 syarat aktif × 6 henti; ukuran = dijual dengan untung ≥ +30%. Pegang minimum 3 sesi; tiada jual hari beli; henti rugi wajib.

## 2. Bacaan dikunci (kumpulan B, saham yang carian tidak lihat)

- Setup papan Dipercayai-T (belian ≥ 200, ≥ 8 tahun aktif, mengatasi rawak dalam K1, K2 DAN K3): **11 daripada 12** → lorong trend **ADA kelebihan** mengikut bacaan yang dikunci.
- Keluar terpilih mengatasi pegang sahaja (henti sama) pada B: **0 daripada 12** → keluar **TIDAK menolong**.
- Median papan: pelari besar 20.8 % (rawak hari sama 14.1 %); dijual ≥ +30 % 23.1 %; menang 42 %; rugi ≥ 15 % 45 %; purata +5.8 %; pegang median 126 sesi.

## 3. Papan lorong trend (12 setup)

| ID | Prasyarat | Pencetus (parameter) | Penapis saham | Henti · keluar | Belian (setahun) | **Pelari besar %** (rawak) | Capai +100 % % (rawak) | Dijual ≥ +30 % % (rawak) | Menang % | Rugi ≥ 15 % % | Purata % | Pegang (sesi) | Kelebihan K1 / K2 / K3 | Dipercayai-T |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `T01` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s8: a14_kali_0_5=0.688, atr_14=26, np_ambang_2=1, pivot_k_3=2, rolling_20=36, rolling_50=80) | Supertrend naik + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 308 (19) | **33.1** (19.8) | 12.0 (4.5) | 32.5 (24.7) | 54 | 33 | +16.9 | 126 | +11.4 / +13.8 / +16.9 | **ya** |
| `T02` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s6: a14_kali_0_5=0.75, atr_14=28, np_ambang_2=1, pivot_k_3=2, rolling_20=35, rolling_50=84) | Supertrend naik + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 305 (18) | **33.8** (20.0) | 12.5 (4.5) | 33.4 (24.9) | 55 | 33 | +17.7 | 126 | +10.9 / +15.1 / +17.8 | **ya** |
| `T03` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 2: rolling_50=34, shift_2=3) | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 203 (12) | **28.6** (21.3) | 8.4 (5.0) | 29.1 (24.9) | 52 | 37 | +12.0 | 126 | +1.9 / +11.2 / +14.3 | **ya** |
| `T04` | turun-naik SPY 21 hari <= 10% setahun + hasil suku terkini tumbuh >= 20% | K01.074 RSI(7) < 35 + atas MA200 | RS >= 90 + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 260 (16) | **19.6** (13.8) | 7.7 (3.3) | 23.1 (17.0) | 37 | 50 | +1.4 | 126 | +11.4 / +0.4 / +1.8 | **ya** |
| `T05` | QQQ dalam 3% dari puncak 52 minggu + hasil suku terkini tumbuh >= 20% | M10 EMA3 + CCI + MACD (benih M, varian 9s7: cci_20=12, e125_kali_0_99=0.495, ewm_span_125=64, ewm_span_250=325, ewm_span_60=56, rolling_11=17) | ADX < 20 + RS >= 90 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 358 (22) | **17.3** (12.0) | 5.9 (2.8) | 18.4 (16.0) | 41 | 46 | +3.4 | 126 | +4.6 / +2.1 / +17.8 | **ya** |
| `T06` | turun-naik SPY 21 hari <= 10% setahun + hasil suku terkini tumbuh >= 20% | K01.073 RSI(7) < 35 | RS >= 90 + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 259 (16) | **19.7** (13.8) | 7.7 (3.3) | 23.2 (17.0) | 37 | 49 | +1.5 | 126 | +11.5 / +0.4 / +1.8 | **ya** |
| `T07` | SPY atas SMA200 + hasil suku terkini tumbuh >= 20% | P45 pemimpin undur ke MA20 | ADX < 20 + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 330 (20) | **26.1** (16.5) | 7.9 (4.6) | 26.1 (20.3) | 49 | 40 | +8.1 | 126 | +10.7 / +4.2 / +24.9 | **ya** |
| `T08` | QQQ dalam 3% dari puncak 52 minggu + hasil suku terkini tumbuh >= 20% | M10 EMA3 + CCI + MACD (benih M, varian 9s8: cci_20=11, e125_kali_0_99=0.558, ewm_span_125=78, ewm_span_250=244, ewm_span_60=56, rolling_11=15) | RS >= 90 + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 297 (18) | **20.5** (14.4) | 6.1 (3.7) | 21.9 (17.5) | 38 | 49 | +2.1 | 126 | +6.1 / +2.9 / +14.6 | **ya** |
| `T09` | QQQ dalam 3% dari puncak 52 minggu + hasil suku terkini tumbuh >= 20% | M92 CCI-50 (benih M, varian 3s1: cci_50=77, rma_atr_14=19, rma_atr_kali_2=2.015) | RS >= 90 + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 207 (12) | **20.8** (12.9) | 4.8 (3.0) | 20.3 (15.7) | 38 | 50 | -1.6 | 126 | +14.5 / -1.5 / +16.9 | tidak |
| `T10` | turun-naik SPY 21 hari <= 10% setahun + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 3: rolling_50=70, shift_2=4) | ADX < 20 + RS >= 90 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 380 (23) | **17.1** (10.6) | 5.0 (2.2) | 17.9 (14.0) | 38 | 44 | +2.9 | 126 | +5.4 / +0.9 / +35.3 | **ya** |
| `T11` | keluasan naik >= 10 mata dalam 10 sesi + hasil suku terkini tumbuh >= 20% | K23.005 RS silang atas 95 | MA20 > MA50 + ADX > 25 | -20% · X00 tiada keluar indikator (henti + 126 sesi) | 250 (15) | **20.8** (11.3) | 7.6 (2.4) | 21.2 (14.8) | 42 | 47 | +8.2 | 126 | +8.7 / +11.1 / +3.2 | **ya** |
| `T12` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M137 Livermore System (benih M, varian 4: a_kali_4=5.017, atr_kali_6=6.621, henti_atr=2.949, keluar_chan=2.296, keluar_chan_atr=18, keluar_chan_tinggi=33) | templat trend Minervini + ATR% >= 4 | 6xATR14 · X00 tiada keluar indikator (henti + 126 sesi) | 242 (15) | **25.2** (17.9) | 8.7 (4.5) | 24.4 (22.4) | 47 | 41 | +8.5 | 126 | +7.6 / +6.6 / +9.0 | **ya** |

## 4. Keluar "trend tamat" sejagat (dipilih pada A)

| # | Henti | Keluar | A: tambahan "dijual ≥ +30 %" atas pegang sahaja (mata) |
|---|---|---|---|
| 1 | -10% | Chandelier 8.0xATR14 dari tutup tertinggi | -0.84 |
| 2 | -10% | Chandelier 8.0xATR14 dari tutup tertinggi [aktif selepas +10%] | -0.84 |
| 3 | -10% | Chandelier 8.0xATR14 dari tutup tertinggi [aktif selepas +20%] | -0.84 |
| 4 | -10% | tiada kemajuan (selepas 40 sesi, tutup < harga beli) [aktif selepas +20%] | -1.18 |
| 5 | -15% | Chandelier 8.0xATR14 dari tutup tertinggi [aktif selepas +10%] | -1.22 |
| 6 | -15% | Chandelier 8.0xATR14 dari tutup tertinggi [aktif selepas +20%] | -1.22 |
| 7 | -15% | Chandelier 8.0xATR14 dari tutup tertinggi | -1.27 |
| 8 | -10% | tiada kemajuan (selepas 20 sesi, tutup < harga beli) [aktif selepas +20%] | -1.47 |
| 9 | -20% | Chandelier 8.0xATR14 dari tutup tertinggi [aktif selepas +10%] | -1.48 |
| 10 | -20% | Chandelier 8.0xATR14 dari tutup tertinggi [aktif selepas +20%] | -1.48 |

## 4a. "Pegang sampai trend tamat": keluar rujukan (maklumat; purata 12 setup papan, kumpulan B, henti 6xATR14)

| Keluar | Dijual ≥ +30 % % | Menang % | Rugi ≥ 15 % % | Purata % | Median % | Pegang median (sesi) | Pada pelari besar: untung dapat / puncak % |
|---|---|---|---|---|---|---|---|
| X00 tiada keluar indikator (henti + 126 sesi) | 24.4 | 44 | 43 | +6.7 | -7.3 | 126 | +58 / +97 |
| tutup < MA50 | 6.6 | 33 | 7 | +1.4 | -3.3 | 14 | +19 / +96 |
| dua tutup berturut < MA50 | 7.4 | 33 | 8 | +1.6 | -3.7 | 18 | +21 / +96 |
| MA20 < MA50 | 7.4 | 41 | 13 | +1.7 | -2.3 | 20 | +23 / +96 |
| tutup < rendah 20 hari | 12.1 | 35 | 16 | +3.2 | -5.5 | 31 | +35 / +97 |
| Supertrend(14, 4.0) turun | 9.8 | 38 | 14 | +3.1 | -3.1 | 22 | +31 / +96 |
| Chandelier 5.0xATR14 dari tutup tertinggi | 17.9 | 39 | 34 | +5.2 | -7.3 | 60 | +50 / +97 |
| Chandelier 8.0xATR14 dari tutup tertinggi | 22.5 | 42 | 44 | +6.1 | -8.9 | 108 | +57 / +97 |
| tutup < 80% tutup tertinggi sejak beli | 16.9 | 40 | 33 | +4.8 | -7.2 | 54 | +44 / +97 |
| tiada kemajuan (selepas 40 sesi, tutup < harga beli) | 17.7 | 27 | 24 | +6.0 | -4.2 | 45 | +52 / +97 |

## 5. Kes rujukan pengguna: MXL (Mac–Jun 2026)

MXL berada dalam kumpulan B. Isyarat setup papan pada MXL (tarikh isyarat @ harga beli): `T11`: 20260421 @ 34.0.
Isyarat selepas pertengahan April 2026 tidak masuk statistik (tetingkap 126 sesi belum lengkap) tetapi ditunjukkan di sini.
Satu kes bukan bukti; ia hanya menunjukkan sama ada setup terbaik akan menangkap contoh yang pengguna ingat.

## 6. Kaveat

- Tiada saham delist: bagi pegang 6 bulan, bias ini LEBIH besar daripada lorong swing (saham yang gagal hilang).
- K3 pendek: tetingkap 126 sesi bermakna isyarat selepas ~April 2026 tidak dikira.
- Kumpulan B sudah dilihat untuk label lain; skor A melambung kerana banyak calon. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.
