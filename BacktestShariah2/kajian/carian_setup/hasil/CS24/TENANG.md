# CS24 — kumpulan "saham tenang" (pindaan (ak), 2026-11-17)

Dijana `cs_tenang24.py`; jangan sunting. Pangkat backtest, BUKAN bukti dan BUKAN keputusan wang sebenar. Tiada saham delist.

## Takrif (dikunci sebelum dijalankan)

- Alam: bar isyarat dengan ATR14 ÷ tutup ≤ 2.5 %. Cara pegang T5: beli buka esok; jual pada buka selepas tutup pertama ≤ 95 % tutup tertinggi sejak beli (termasuk harga beli); had teknikal 252 sesi; kos 0.5 %.
- "Berjaya" = dijual dengan untung. "Rawak" = saham tenang lain yang dibeli pada hari sama dan dipegang cara sama.

## Saham tenang rawak di bawah T5 (kumpulan B, semua bar layak)

- 1,371,737 dagangan selesai daripada 1,372,199 bar tenang layak. Dijual dengan untung 38.1 %; purata +0.48 %; nilai tengah -2.12 %; persentil ke-5 -7.72 %; nilai tengah pegang 23 sesi; mencapai had 252 sesi 0.14 %.

## Bacaan dikunci

| Semakan | Calon | Peraturan rawak | Perlu | Keputusan |
|---|---|---|---|---|
| B1: lulus (kelebihan > 0 dalam K1, K2, K3) | 46.2 % (224 / 485) | 5.7 % (300 layak) | beza ≥ 20 mata | LULUS |
| B2: lebih baik daripada rawak pada 2025–26 | 59.8 % | 48.0 % | ≥ 60 % dan beza ≥ 10 mata | GAGAL |

**Keputusan: GAGAL.** Tiada kod baharu.

## Nilai tengah (peraturan yang cukup belian, kumpulan B)

| Kumpulan | Bil. | Untung % (rawak) | Kelebihan K1 / K2 / K3 (mata) | Purata % (rawak) | Nilai tengah % | Persentil ke-5 % | Pegang (sesi) | Tahun positif |
|---|---|---|---|---|---|---|---|---|
| Calon | 485 | 38.0 (37.0) | +0.94 / +0.92 / +0.55 | +0.54 (+0.28) | -2.15 | -7.71 | 24 | 53 % |
| Calon lulus | 224 | 38.1 (36.6) | +1.25 / +1.27 / +2.45 | +0.54 (+0.22) | -2.15 | -7.71 | 24 | 59 % |
| Peraturan rawak | 300 | 37.0 (37.6) | -0.60 / -0.47 / -0.10 | +0.27 (+0.36) | -2.28 | -7.75 | 22 | 41 % |

## Calon lulus teratas ikut kelebihan (REKOD sahaja, tiada kod) — 40 teratas

| Id | Isyarat beli | Prasyarat | Syarat saham | Belian | Untung % (rawak) | K1 / K2 / K3 | Purata % (rawak) | Pegang | Minggu ada belian |
|---|---|---|---|---|---|---|---|---|---|
| Z0314 | K09.021 MACD(3,10,16) silang naik atas sifar | sektor 3 terbawah (pulangan 63 sesi) | ADX < 20 + dalam 15% dari puncak 52 minggu | 3,608 | 40.6 (37.3) | +3.2 / +4.4 / +0.3 | +0.99 (+0.32) | 26 | 82 % |
| Z0384 | K25.031 pecah julat sempit 60 hari (<= 35%) | sektor 3 terbawah (pulangan 63 sesi) | RSI14 > 60 + dalam 5% dari puncak 52 minggu | 2,936 | 39.0 (35.9) | +2.3 / +6.0 / +0.5 | +0.66 (+0.08) | 26 | 78 % |
| Z0391 | K25.031 pecah julat sempit 60 hari (<= 35%) | sektor 3 terbawah (pulangan 63 sesi) | MACD > 0 + dalam 5% dari puncak 52 minggu | 2,942 | 38.9 (36.0) | +2.1 / +6.1 / +0.2 | +0.65 (+0.08) | 26 | 78 % |
| Z0400 | K25.031 pecah julat sempit 60 hari (<= 35%) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 2,944 | 38.9 (36.0) | +2.1 / +6.1 / +0.2 | +0.65 (+0.08) | 26 | 78 % |
| Z0401 | K25.031 pecah julat sempit 60 hari (<= 35%) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA20 + dalam 5% dari puncak 52 minggu | 2,944 | 38.9 (36.0) | +2.1 / +6.1 / +0.2 | +0.65 (+0.08) | 26 | 78 % |
| Z0402 | K25.031 pecah julat sempit 60 hari (<= 35%) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA50 + dalam 5% dari puncak 52 minggu | 2,944 | 38.9 (36.0) | +2.1 / +6.1 / +0.2 | +0.65 (+0.08) | 26 | 78 % |
| Z0309 | K25.011 pecah julat sempit 20 hari (<= 12%) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + hari naik (tutup > buka) | 3,240 | 39.3 (36.6) | +2.7 / +2.9 / +1.4 | +0.77 (+0.21) | 27 | 80 % |
| Z0338 | K25.011 pecah julat sempit 20 hari (<= 12%) | sektor 3 terbawah (pulangan 63 sesi) | MACD > 0 + dalam 5% dari puncak 52 minggu | 3,253 | 39.1 (36.5) | +2.7 / +2.7 / +1.2 | +0.71 (+0.18) | 27 | 80 % |
| Z0108 | N27 Ichimoku atas awan (benih N) | sektor 3 terbawah (pulangan 63 sesi) | ADX < 20 + hari naik (tutup > buka) | 3,075 | 40.0 (37.5) | +2.8 / +2.2 / +1.0 | +0.96 (+0.36) | 25 | 80 % |
| Z0192 | K25.011 pecah julat sempit 20 hari (<= 12%) | sektor 3 terbawah (pulangan 63 sesi) | RSI14 > 60 + dalam 5% dari puncak 52 minggu | 3,195 | 39.0 (36.4) | +2.7 / +2.4 / +1.0 | +0.70 (+0.17) | 27 | 79 % |
| Z0345 | K25.011 pecah julat sempit 20 hari (<= 12%) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA50 + dalam 5% dari puncak 52 minggu | 3,317 | 39.1 (36.6) | +2.5 / +2.8 / +1.1 | +0.74 (+0.20) | 27 | 80 % |
| Z0353 | K25.011 pecah julat sempit 20 hari (<= 12%) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 3,318 | 39.1 (36.6) | +2.5 / +2.8 / +1.1 | +0.74 (+0.20) | 27 | 80 % |
| Z0021 | K06.001 2 tutup menurun berturut | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + volum 10 hari > volum 50 hari | 3,360 | 39.0 (36.7) | +2.0 / +3.1 / +3.6 | +0.63 (+0.23) | 26 | 83 % |
| Z0310 | M70 Pecahan Hari Dalam (benih M, parameter asal) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 3,777 | 38.8 (36.5) | +1.7 / +2.8 / +7.4 | +0.77 (+0.21) | 26 | 84 % |
| Z0311 | M70 Pecahan Hari Dalam (benih M, parameter asal) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA50 + dalam 5% dari puncak 52 minggu | 3,777 | 38.8 (36.5) | +1.7 / +2.8 / +7.4 | +0.77 (+0.21) | 26 | 84 % |
| Z0312 | M70 Pecahan Hari Dalam (benih M, parameter asal) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA200 + dalam 5% dari puncak 52 minggu | 3,777 | 38.8 (36.5) | +1.7 / +2.8 / +7.4 | +0.77 (+0.21) | 26 | 84 % |
| Z0313 | M70 Pecahan Hari Dalam (benih M, parameter asal) | sektor 3 terbawah (pulangan 63 sesi) | RSI14 > 50 + dalam 5% dari puncak 52 minggu | 3,777 | 38.8 (36.5) | +1.7 / +2.8 / +7.4 | +0.77 (+0.21) | 26 | 84 % |
| Z0022 | K06.002 2 tutup menurun berturut + atas MA200 | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + volum 10 hari > volum 50 hari | 3,360 | 39.0 (36.7) | +1.9 / +3.1 / +3.6 | +0.62 (+0.23) | 26 | 83 % |
| Z0348 | M70 Pecahan Hari Dalam (benih M, varian 1: ewm_span_10=17, ewm_span_21=41, rolling_200=378, rolling_50=59) | sektor 3 terbawah (pulangan 63 sesi) | RSI14 > 50 + dalam 5% dari puncak 52 minggu | 3,821 | 39.2 (36.9) | +1.7 / +2.4 / +7.1 | +0.85 (+0.28) | 26 | 84 % |
| Z0362 | M70 Pecahan Hari Dalam (benih M, varian 1: ewm_span_10=17, ewm_span_21=41, rolling_200=378, rolling_50=59) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 3,823 | 39.2 (36.9) | +1.7 / +2.4 / +7.1 | +0.85 (+0.28) | 26 | 84 % |
| Z0363 | M70 Pecahan Hari Dalam (benih M, varian 1: ewm_span_10=17, ewm_span_21=41, rolling_200=378, rolling_50=59) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA200 + dalam 5% dari puncak 52 minggu | 3,823 | 39.2 (36.9) | +1.7 / +2.4 / +7.1 | +0.85 (+0.28) | 26 | 84 % |
| Z0364 | M70 Pecahan Hari Dalam (benih M, varian 1: ewm_span_10=17, ewm_span_21=41, rolling_200=378, rolling_50=59) | sektor 3 terbawah (pulangan 63 sesi) | dalam 15% dari puncak 52 minggu + dalam 5% dari puncak 52 minggu | 3,823 | 39.2 (36.9) | +1.7 / +2.4 / +7.1 | +0.85 (+0.28) | 26 | 84 % |
| Z0365 | M70 Pecahan Hari Dalam (benih M, varian 1: ewm_span_10=17, ewm_span_21=41, rolling_200=378, rolling_50=59) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + ATR% <= 2.5 | 3,823 | 39.2 (36.9) | +1.7 / +2.4 / +7.1 | +0.85 (+0.28) | 26 | 84 % |
| Z0127 | M14 Walking with the Whales (benih M, parameter asal) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + volum 10 hari > volum 50 hari | 3,200 | 38.8 (36.6) | +1.5 / +4.6 / +1.0 | +0.51 (+0.20) | 26 | 84 % |
| Z0299 | M70 Pecahan Hari Dalam (benih M, varian 2: ewm_span_10=18, ewm_span_21=42, rolling_200=180, rolling_50=66) | sektor 3 terbawah (pulangan 63 sesi) | RSI14 > 50 + dalam 5% dari puncak 52 minggu | 3,987 | 38.6 (36.5) | +1.5 / +2.6 / +7.3 | +0.76 (+0.20) | 25 | 86 % |
| Z0305 | M70 Pecahan Hari Dalam (benih M, varian 2: ewm_span_10=18, ewm_span_21=42, rolling_200=180, rolling_50=66) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 3,990 | 38.6 (36.5) | +1.5 / +2.6 / +7.1 | +0.76 (+0.20) | 25 | 86 % |
| Z0306 | M70 Pecahan Hari Dalam (benih M, varian 2: ewm_span_10=18, ewm_span_21=42, rolling_200=180, rolling_50=66) | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA200 + dalam 5% dari puncak 52 minggu | 3,990 | 38.6 (36.5) | +1.5 / +2.6 / +7.1 | +0.76 (+0.20) | 25 | 86 % |
| Z0307 | M70 Pecahan Hari Dalam (benih M, varian 2: ewm_span_10=18, ewm_span_21=42, rolling_200=180, rolling_50=66) | sektor 3 terbawah (pulangan 63 sesi) | dalam 15% dari puncak 52 minggu + dalam 5% dari puncak 52 minggu | 3,990 | 38.6 (36.5) | +1.5 / +2.6 / +7.1 | +0.76 (+0.20) | 25 | 86 % |
| Z0152 | K21.001 NR4 | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + volum 10 hari > volum 50 hari | 3,235 | 38.8 (36.8) | +1.4 / +4.6 / +0.1 | +0.58 (+0.23) | 27 | 83 % |
| Z0227 | M70 Pecahan Hari Dalam (benih M, parameter asal) | sektor 3 terbawah (pulangan 63 sesi) | MA20 > MA50 + dalam 5% dari puncak 52 minggu | 3,397 | 38.2 (36.3) | +1.3 / +2.4 / +8.1 | +0.66 (+0.15) | 25 | 82 % |
| Z0009 | M14 Walking with the Whales (benih M, varian 2: rolling_50=34, shift_2=3) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + hari naik (tutup > buka) | 4,213 | 38.6 (36.6) | +1.3 / +4.1 / +2.0 | +0.64 (+0.23) | 25 | 88 % |
| Z0068 | K06.003 3 tutup menurun berturut | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 3,949 | 38.4 (36.5) | +1.8 / +2.0 / +4.3 | +0.62 (+0.19) | 25 | 83 % |
| Z0069 | K06.003 3 tutup menurun berturut | sektor 3 terbawah (pulangan 63 sesi) | dalam 15% dari puncak 52 minggu + dalam 5% dari puncak 52 minggu | 3,949 | 38.4 (36.5) | +1.8 / +2.0 / +4.3 | +0.62 (+0.19) | 25 | 83 % |
| Z0070 | K06.003 3 tutup menurun berturut | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + ATR% <= 2.5 | 3,949 | 38.4 (36.5) | +1.8 / +2.0 / +4.3 | +0.62 (+0.19) | 25 | 83 % |
| Z0071 | N119 3 tutup turun berturut (benih N) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu | 3,949 | 38.4 (36.5) | +1.8 / +2.0 / +4.3 | +0.62 (+0.19) | 25 | 83 % |
| Z0072 | N119 3 tutup turun berturut (benih N) | sektor 3 terbawah (pulangan 63 sesi) | dalam 15% dari puncak 52 minggu + dalam 5% dari puncak 52 minggu | 3,949 | 38.4 (36.5) | +1.8 / +2.0 / +4.3 | +0.62 (+0.19) | 25 | 83 % |
| Z0073 | N119 3 tutup turun berturut (benih N) | sektor 3 terbawah (pulangan 63 sesi) | dalam 5% dari puncak 52 minggu + ATR% <= 2.5 | 3,949 | 38.4 (36.5) | +1.8 / +2.0 / +4.3 | +0.62 (+0.19) | 25 | 83 % |
| Z0418 | M92 CCI-50 (benih M, varian 1: cci_50=41, rma_atr_14=16, rma_atr_kali_2=1.033) | >= 60% saham sektor di atas MA50 | ADX < 20 + volum 10 hari > volum 50 hari | 4,336 | 39.9 (38.0) | +1.8 / +2.1 / +2.9 | +0.80 (+0.43) | 25 | 80 % |
| Z0281 | K09.019 MACD(3,10,16) silang naik | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA50 + dalam 15% dari puncak 52 minggu | 5,742 | 38.5 (36.5) | +1.7 / +3.0 / +1.0 | +0.62 (+0.21) | 24 | 88 % |
| Z0056 | K06.003 3 tutup menurun berturut | sektor 3 terbawah (pulangan 63 sesi) | tutup > MA200 + dalam 5% dari puncak 52 minggu | 3,949 | 38.4 (36.5) | +1.7 / +2.0 / +4.3 | +0.61 (+0.19) | 25 | 83 % |

Calon: 485 daripada 147 isyarat beli (56028 peraturan ditinjau); kawalan 300 peraturan rawak (benih 20261119). Fail: `calon.csv.gz`, `kawalan.csv`, `bacaan.json`.
