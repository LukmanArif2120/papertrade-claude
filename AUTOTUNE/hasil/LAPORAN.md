# LAPORAN AUTOTUNE (A01)

Dijana 2026-10-18T04:02Z oleh `AUTOTUNE/sahkan/laporan.py`. Peraturan: `AUTOTUNE/SPEC.md` §5–§7. Semua angka ialah backtest; tiada order, tiada wang sebenar.

## Data dan kaveat
- Harga yfinance (`auto_adjust`), universe bulanan 2000 saham AS (harga > USD10, nilai dagangan ≥ USD1 juta), tanpa penapis Shariah. Data 2009-01-02 hingga 2026-10-16 (tarikan 2026-10-17T13:59Z; 3227 ticker pernah dalam universe).
- Universe kurang daripada 2000 saham sebelum 2021 (kira-kira 1100–1800 sebulan pada 2013–2020; lihat QC.md).
- Bias survivorship: saham delist tiada dalam data; semua keputusan ialah HAD ATAS.
- yfinance percuma: pelarasan dan bar boleh tersilap; ticker dengan > 5 hari |pulangan| > 50% dibuang (QC.md).
- OOS: 2013-01-02 – 2024-09-30 (12 tetingkap walk-forward, parameter setiap tetingkap sendiri). Kumpulan A = tala, B = semakan merentas saham. Tempoh kunci: 2024-10-01 – 2026-10-16 (parameter AKHIR, A+B, dibuka sekali). Ujian bersih: 2013-01-01 – 2018-12-31 (PARAM asal, A+B).
- SPY pada tarikh yang sama: OOS 14.6%, bersih 12.0% setahun.

## Kiraan label

| Label | Bilangan |
|---|---|
| TINGGI | 0 |
| SEDERHANA | 1 |
| RENDAH | 69 |
| GAGAL | 64 |
| BUKAN SWING | 0 |
| BELUM DITALA | 0 |

Jumlah 134 kaedah; N percubaan (DSR) = 225120.

## 20 kaedah teratas (CAGR OOS-A)

| # | Kaedah | Label | A CAGR | A MDD | B CAGR | B MDD | SPY OOS | Kunci | SPY kunci | DSR | PBO |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M81 (Bensdorp Long Trend High Mo…) | SEDERHANA | 66.6% | -21.3% | 48.2% | -21.6% | 14.6% | 192.2% | 16.3% | 0.99 | 0.61 |
| 2 | M93 (Bollinger Kaedah II: %b + M…) | RENDAH | 15.3% | -51.4% | 2.6% | -53.8% | 14.6% | 8.9% | 16.3% | 0.00 | 0.81 |
| 3 | M121 (High 2 bull flag (Brooks)) | RENDAH | 11.7% | -34.7% | -0.1% | -57.4% | 14.6% | -7.9% | 16.3% | 0.00 | 0.43 |
| 4 | M91 (Stochastic Pop (Bernstein/S…) | RENDAH | 8.8% | -50.1% | 9.7% | -22.8% | 14.6% | 28.6% | 16.3% | 0.00 | 0.64 |
| 5 | M20 (EMA10/15 Crossover + Sudut) | RENDAH | 8.5% | -49.5% | 4.3% | -43.2% | 14.6% | -11.0% | 16.3% | 0.00 | 0.53 |
| 6 | M146 (3-Bar Momentum Pattern) | RENDAH | 8.3% | -39.8% | 5.6% | -47.5% | 14.6% | 7.1% | 16.3% | 0.00 | 0.70 |
| 7 | M134 (First Kiss After Daylight (…) | RENDAH | 7.9% | -31.9% | 6.2% | -33.7% | 14.6% | -0.8% | 16.3% | 0.00 | 0.69 |
| 8 | M152 (Spike & Ledge) | RENDAH | 7.7% | -48.6% | 12.0% | -43.9% | 14.6% | 2.6% | 16.3% | 0.00 | 0.66 |
| 9 | M41 (FW Penyatuan Mingguan) | RENDAH | 7.7% | -53.0% | 6.0% | -56.5% | 14.6% | 3.7% | 16.3% | 0.00 | 0.87 |
| 10 | M01 (Bollinger Band + RSI) | RENDAH | 7.2% | -42.6% | -5.0% | -58.1% | 14.6% | 25.4% | 16.3% | 0.00 | 0.84 |
| 11 | M135 (3rd Watch) | RENDAH | 7.0% | -33.6% | 7.4% | -26.3% | 14.6% | 14.5% | 16.3% | 0.00 | 0.74 |
| 12 | M99 (Three Line Break) | RENDAH | 7.0% | -43.1% | -1.5% | -51.7% | 14.6% | -9.5% | 16.3% | 0.00 | 0.34 |
| 13 | M95 (Nisbah Kebaharuan High 52 M…) | RENDAH | 6.7% | -50.3% | 4.1% | -31.8% | 14.6% | -5.7% | 16.3% | 0.00 | 0.80 |
| 14 | M138 (直升机空中加油 (Helikopter isi min…) | RENDAH | 6.6% | -47.2% | 1.7% | -48.9% | 14.6% | -8.4% | 16.3% | 0.00 | 0.53 |
| 15 | M117 (Landry Pullback (high 2 bul…) | RENDAH | 6.5% | -48.2% | 2.3% | -37.0% | 14.6% | 9.8% | 16.3% | 0.00 | 0.61 |
| 16 | M130 (多方炮 (dua lilin hijau mengap…) | RENDAH | 6.4% | -31.2% | 7.9% | -48.6% | 14.6% | 7.8% | 16.3% | 0.00 | 0.36 |
| 17 | M123 (CCI Correction (Lambert, Ch…) | RENDAH | 6.0% | -45.4% | 0.0% | -53.5% | 14.6% | -0.7% | 16.3% | 0.00 | 0.41 |
| 18 | M02 (MACD + SMA200) | RENDAH | 6.0% | -45.0% | 2.6% | -51.6% | 14.6% | 7.3% | 16.3% | 0.00 | 0.59 |
| 19 | M67 (Rayner Teo: Ujian Ketiga pa…) | RENDAH | 5.7% | -55.4% | 3.2% | -41.8% | 14.6% | -22.9% | 16.3% | 0.00 | 0.50 |
| 20 | M59 (Anjakan Julat RSI) | RENDAH | 5.6% | -33.1% | -0.5% | -50.8% | 14.6% | 15.2% | 16.3% | 0.00 | 0.26 |

## Portfolio gabungan (8 slot × 12.5%)

Terpilih (urutan tamak atas OOS-A): M81.

| Bahagian | CAGR | MDD | SPY | Tempoh |
|---|---|---|---|---|
| OOS-A | 66.6% | -21.3% | 14.6% | 2013-01-02 – 2024-09-30 |
| OOS-B | 48.2% | -21.6% | 14.6% | 2013-01-02 – 2024-09-30 |
| Tempoh kunci | 192.2% | -37.7% | 16.3% | 2024-10-01 – 2026-10-16 |

Parameter SEMASA (untuk cadangan dagangan; parameter lain = PARAM asal):

- **M81**: a20_kali_3=2.249, close_ambang_5=6, nilai20_ambang_50000000=33123778, rma_atr_20=12, rolling_25=39, tt_kali_0_75=0.9259

Log pemilihan:

- M81: mula (CAGR 66.6%, MDD -21.3%)

Semakan jana semula (satu kaedah vs JSON tala, beza pulangan harian maksimum): M81 0.000000.

## Nota DSR dan PBO
- DSR (Bailey & López de Prado): Sharpe harian OOS-A dideflasi dengan N = jumlah semua percubaan semua kaedah; V[SR] = varians SR OOS-A antara kaedah (formula teras/objektif.py). SR0 = 1.61 setahun. TINGGI memerlukan DSR ≥ 0.95.
- PBO (CSCV, 8 blok, 50 percubaan teratas kajian AKHIR, pulangan latih): kebarangkalian pilihan terbaik dalam sampel jatuh di bawah median luar sampel. TINGGI memerlukan PBO ≤ 0.30.
- Nisbah dataran (±10%, ±25% setiap parameter TALA): < 0.5 bermakna pilihan berada di puncak sempit.
- Label tidak menjamin prestasi masa depan; tempoh kunci ialah semakan sekali sahaja.

## BELUM DITALA (0)

Tiada.
