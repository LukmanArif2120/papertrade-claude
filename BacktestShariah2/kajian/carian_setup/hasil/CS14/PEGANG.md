# CS14: cara pegang "jual yang rugi, pegang yang untung", tanpa had masa (backtest; BUKAN bukti)

Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (x). Dijana `cs_pegang14.py`; jangan sunting.

- Permintaan pengguna 16 Nov 2026: pegang selagi untung, jual bila rugi, tiada had 20 hari; keputusan "ya dan C".
- 2,001 setup senarai utama; 2,001 dengan ≥ 30 dagangan dalam kedua-dua kumpulan saham. Peraturan beli dan stop loss (4×ATR14) tidak diubah; 20 hari pertama tidak diubah. Kadar tangkap tidak terkesan oleh cara pegang.
- 108 cara diuji: 4 peraturan "rugi" × 9 peraturan "trend tamat" × 3 had masa (126 sesi, 252 sesi, tiada). Cara dipilih pada saham carian; keputusan dibaca pada saham yang carian tidak lihat.
- Semakan pariti: cara sekarang menghasilkan semula angka senarai utama (beza terbesar kadar menang 0.000005, purata 0.000005).

## 1. Keputusan (ujian ditetapkan dahulu)

- **Cara terpilih: jual bila tutup di bawah harga beli − 1×ATR ATAU tutup di bawah purata 20 hari · tanpa had masa** (`r2.t1.0`; menepati syarat pemilihan pada saham carian). Pada saham yang carian tidak lihat, lawan cara sekarang: (1) purata lebih tinggi bagi 1,005 daripada 2,001 setup → ya; (2) beza kadar menang -0.2 mata (perlu ≥ −2) → ya; (3) beza rugi ≥ 15 % +0.0 mata (perlu ≤ +2) → ya; (4) dagangan 2025–26: beza purata +0.0 mata (988 daripada 1,877 setup lebih tinggi; perlu > 0) → ya. **Keputusan: MENOLONG.** Beza purata kurang 0.1 mata: **secara praktikal ini cara yang sama dengan cara sekarang**, jadi lulus ujian di sini TIDAK bermakna ada pembaikan.
- **Terbaik tafsiran A (selagi di atas harga beli): jual bila rugi pada hari ke-20 (semak sekali) · tanpa had masa** (`r3.t0.0`; TIADA calon menepati syarat pemilihan pada saham carian). Pada saham yang carian tidak lihat, lawan cara sekarang: (1) purata lebih tinggi bagi 2,001 daripada 2,001 setup → ya; (2) beza kadar menang -31.6 mata (perlu ≥ −2) → TIDAK; (3) beza rugi ≥ 15 % +9.8 mata (perlu ≤ +2) → TIDAK; (4) dagangan 2025–26: beza purata +4.6 mata (1,608 daripada 1,840 setup lebih tinggi; perlu > 0) → ya. **Keputusan: TIDAK menolong.**
- **Terbaik tafsiran B (selagi trend naik): jual bila tutup di bawah harga beli − 1×ATR ATAU tutup di bawah purata 20 hari · tanpa had masa** (`r2.t1.0`; menepati syarat pemilihan pada saham carian). Pada saham yang carian tidak lihat, lawan cara sekarang: (1) purata lebih tinggi bagi 1,005 daripada 2,001 setup → ya; (2) beza kadar menang -0.2 mata (perlu ≥ −2) → ya; (3) beza rugi ≥ 15 % +0.0 mata (perlu ≤ +2) → ya; (4) dagangan 2025–26: beza purata +0.0 mata (988 daripada 1,877 setup lebih tinggi; perlu > 0) → ya. **Keputusan: MENOLONG.** Beza purata kurang 0.1 mata: **secara praktikal ini cara yang sama dengan cara sekarang**, jadi lulus ujian di sini TIDAK bermakna ada pembaikan.

**Ringkasnya:** tiada cara yang menaikkan purata setiap dagangan TANPA menurunkan kadar menang. Makin longgar peraturan jual, makin besar purata dan makin kurang dagangan yang menang (tangga di bawah). "Jual hanya bila sudah rugi" bermakna hampir setiap dagangan yang dijual ialah dagangan rugi: untung yang ada dipulangkan dahulu sebelum jualan.

## 2. Tangga tukar ganti (tambahan selepas hasil dilihat; saham yang carian tidak lihat; nilai tengah setiap kumpulan setup)

**Semua setup (2,001)**

| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | Untung setiap 20 hari pegang % | 2025–26: beza purata lawan cara sekarang (mata) | 2025–26: beza menang (mata) |
|---|---|---|---|---|---|---|---|---|
| cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan) | +0.5 | 47 | 6 | 0.7 | 21 | +0.41 | +0.0 | +0.0 |
| jual bila tutup di bawah purata 50 hari · tanpa had masa | +1.0 | 41 | 6 | 1.6 | 25 | +0.59 | +0.9 | -4.2 |
| jual bila jatuh 4×ATR dari tutup tertinggi · tanpa had masa | +2.0 | 39 | 8 | 3.2 | 40 | +0.74 | +3.3 | -6.3 |
| jual bila tutup di bawah purata 200 hari · tanpa had masa | +3.2 | 35 | 8 | 5.1 | 46 | +0.77 | +3.1 | -7.0 |
| jual bila jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +6.1 | 32 | 13 | 8.7 | 78 | +0.89 | +6.1 | -9.5 |
| jual bila tutup di bawah harga beli · tanpa had masa | +26.0 | 12 | 7 | 6.5 | 22 | +2.24 | +3.1 | -24.0 |

**Setup lama yang dipercayai (42)**

| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | Untung setiap 20 hari pegang % | 2025–26: beza purata lawan cara sekarang (mata) | 2025–26: beza menang (mata) |
|---|---|---|---|---|---|---|---|---|
| cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan) | +2.1 | 49 | 16 | 2.5 | 22 | +1.71 | +0.0 | +0.0 |
| jual bila tutup di bawah purata 50 hari · tanpa had masa | +2.7 | 41 | 17 | 4.6 | 26 | +1.50 | +2.1 | -4.7 |
| jual bila jatuh 4×ATR dari tutup tertinggi · tanpa had masa | +4.2 | 40 | 26 | 7.3 | 42 | +1.46 | +5.9 | -6.0 |
| jual bila tutup di bawah purata 200 hari · tanpa had masa | +5.3 | 42 | 24 | 7.0 | 21 | +1.62 | +4.7 | -5.6 |
| jual bila jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +9.9 | 36 | 43 | 12.9 | 88 | +1.54 | +10.8 | -9.7 |
| jual bila tutup di bawah harga beli · tanpa had masa | +24.3 | 14 | 17 | 7.2 | 23 | +2.26 | +1.4 | -26.6 |

**Setup "pilihan" (210)**

| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | Untung setiap 20 hari pegang % | 2025–26: beza purata lawan cara sekarang (mata) | 2025–26: beza menang (mata) |
|---|---|---|---|---|---|---|---|---|
| cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan) | +2.6 | 53 | 8 | 1.5 | 22 | +2.10 | +0.0 | +0.0 |
| jual bila tutup di bawah purata 50 hari · tanpa had masa | +3.5 | 53 | 8 | 2.7 | 21 | +2.14 | +1.4 | +0.7 |
| jual bila jatuh 4×ATR dari tutup tertinggi · tanpa had masa | +5.2 | 47 | 11 | 5.0 | 45 | +1.77 | +5.2 | -4.5 |
| jual bila tutup di bawah purata 200 hari · tanpa had masa | +5.6 | 48 | 9 | 5.5 | 21 | +1.71 | +1.9 | -3.7 |
| jual bila jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +11.1 | 40 | 17 | 11.8 | 105 | +1.39 | +8.9 | -8.3 |
| jual bila tutup di bawah harga beli · tanpa had masa | +41.5 | 17 | 9 | 10.4 | 26 | +2.71 | +2.7 | -25.6 |

**Saham rawak, cara sama (300,000 belian rawak mana-mana saham mana-mana hari):** berapa banyak hasil pegang lama datang daripada sekadar memegang saham dalam data ini (pasaran naik; tiada saham delist), bukan daripada setup.

| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung setiap 20 hari pegang % |
|---|---|---|---|---|
| cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan) | +0.7 | 47 | 6 | +0.59 |
| jual bila tutup di bawah purata 50 hari · tanpa had masa | +1.1 | 45 | 6 | +0.70 |
| jual bila jatuh 4×ATR dari tutup tertinggi · tanpa had masa | +2.7 | 41 | 11 | +0.92 |
| jual bila tutup di bawah purata 200 hari · tanpa had masa | +2.4 | 45 | 8 | +0.98 |
| jual bila jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +9.4 | 36 | 23 | +1.26 |
| jual bila tutup di bawah harga beli · tanpa had masa | +40.5 | 13 | 13 | +3.07 |

## 3. Sebelah-menyebelah dengan rujukan (nilai tengah merentas semua setup; saham yang carian tidak lihat)

| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | Untung setiap 20 hari pegang % | Masih dipegang pada hujung data % | Dagangan setiap setup | Saham rawak, cara sama: purata % · menang % · setiap 20 hari % |
|---|---|---|---|---|---|---|---|---|---|
| jual pada hari ke-20 | +0.4 | 50 | 6 | 0.4 | 20 | +0.43 | 0.0 | 893 | +0.4 · 52 · +0.46 |
| cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan) | +0.5 | 47 | 6 | 0.7 | 21 | +0.41 | 0.0 | 890 | +0.7 · 47 · +0.59 |
| pegang 6 bulan, stop loss sahaja | +3.1 | 39 | 13 | 4.6 | 85 | +0.84 | 0.0 | 863 | +4.3 · 43 · +1.02 |
| beli dan simpan, stop loss sahaja (rujukan) | +61.6 | 18 | 21 | 14.6 | 84 | +2.34 | 18.1 | 746 | +112.9 · 21 · +3.10 |
| jual bila rugi pada hari ke-20 (semak sekali) · tanpa had masa | +49.1 | 15 | 16 | 12.0 | 36 | +2.33 | 14.7 | 774 | +82.5 · 16 · +3.11 |
| jual bila tutup di bawah harga beli − 1×ATR ATAU tutup di bawah purata 20 hari · tanpa had masa | +0.5 | 46 | 6 | 0.7 | 21 | +0.42 | 0.0 | 892 | +0.7 · 47 · +0.58 |

"Untung setiap 20 hari pegang" = jumlah untung ÷ jumlah hari pegang × 20: pegang lebih lama menaikkan purata setiap dagangan walaupun tanpa kemahiran, jadi lajur ini menunjukkan untung bagi tempoh pegang yang sama.

## 4. Semua cara tanpa had masa (saham yang carian tidak lihat; beza lawan cara sekarang, nilai tengah)

| Peraturan rugi | Peraturan trend tamat | Purata % | Menang % | Rugi ≥ 15 % % | Median hari | Δ purata (mata) | Δ menang (mata) | Δ rugi ≥ 15 % (mata) | Setup lebih baik % |
|---|---|---|---|---|---|---|---|---|---|
| tiada | tiada | +61.6 | 18 | 21 | 84 | +61.0 | -29.0 | +15.5 | 100 |
| tiada | tutup di bawah purata 20 hari | +0.5 | 47 | 6 | 21 | +0.0 | +0.0 | +0.0 | 1 |
| tiada | tutup di bawah purata 50 hari | +1.0 | 41 | 6 | 25 | +0.5 | -5.6 | +0.0 | 87 |
| tiada | tutup di bawah purata 100 hari | +1.8 | 37 | 7 | 31 | +1.2 | -9.4 | +0.7 | 94 |
| tiada | tutup di bawah purata 200 hari | +3.2 | 35 | 8 | 46 | +2.7 | -11.5 | +2.1 | 97 |
| tiada | jatuh 4×ATR dari tutup tertinggi | +2.0 | 39 | 8 | 40 | +1.5 | -7.9 | +1.9 | 96 |
| tiada | jatuh 6×ATR dari tutup tertinggi | +3.9 | 35 | 11 | 64 | +3.5 | -11.3 | +4.8 | 99 |
| tiada | jatuh 8×ATR dari tutup tertinggi | +6.1 | 32 | 13 | 78 | +5.7 | -14.5 | +6.9 | 99 |
| tiada | jatuh 25 % dari tutup tertinggi | +9.9 | 30 | 12 | 72 | +9.4 | -16.6 | +6.2 | 100 |
| tutup di bawah harga beli | tiada | +26.0 | 12 | 7 | 22 | +25.5 | -34.5 | +0.7 | 100 |
| tutup di bawah harga beli | tutup di bawah purata 20 hari | +0.5 | 46 | 6 | 21 | -0.0 | -1.0 | -0.0 | 41 |
| tutup di bawah harga beli | tutup di bawah purata 50 hari | +0.8 | 39 | 6 | 21 | +0.4 | -7.9 | +0.0 | 85 |
| tutup di bawah harga beli | tutup di bawah purata 100 hari | +1.4 | 33 | 6 | 21 | +0.9 | -13.9 | +0.0 | 91 |
| tutup di bawah harga beli | tutup di bawah purata 200 hari | +2.2 | 28 | 6 | 21 | +1.7 | -19.0 | +0.1 | 96 |
| tutup di bawah harga beli | jatuh 4×ATR dari tutup tertinggi | +1.4 | 32 | 6 | 22 | +0.9 | -14.6 | +0.0 | 94 |
| tutup di bawah harga beli | jatuh 6×ATR dari tutup tertinggi | +2.4 | 25 | 6 | 22 | +1.9 | -21.4 | +0.1 | 97 |
| tutup di bawah harga beli | jatuh 8×ATR dari tutup tertinggi | +3.4 | 21 | 6 | 22 | +2.9 | -25.3 | +0.2 | 99 |
| tutup di bawah harga beli | jatuh 25 % dari tutup tertinggi | +4.8 | 20 | 6 | 22 | +4.4 | -26.5 | +0.3 | 99 |
| tutup di bawah harga beli − 1×ATR | tiada | +36.1 | 11 | 8 | 31 | +35.4 | -35.9 | +1.7 | 100 |
| tutup di bawah harga beli − 1×ATR | tutup di bawah purata 20 hari | +0.5 | 46 | 6 | 21 | +0.0 | -0.2 | +0.0 | 50 |
| tutup di bawah harga beli − 1×ATR | tutup di bawah purata 50 hari | +0.9 | 40 | 6 | 23 | +0.5 | -6.5 | +0.0 | 86 |
| tutup di bawah harga beli − 1×ATR | tutup di bawah purata 100 hari | +1.6 | 34 | 6 | 25 | +1.1 | -12.1 | +0.1 | 93 |
| tutup di bawah harga beli − 1×ATR | tutup di bawah purata 200 hari | +2.5 | 30 | 6 | 25 | +2.1 | -17.0 | +0.3 | 97 |
| tutup di bawah harga beli − 1×ATR | jatuh 4×ATR dari tutup tertinggi | +1.6 | 34 | 6 | 29 | +1.2 | -12.2 | +0.2 | 95 |
| tutup di bawah harga beli − 1×ATR | jatuh 6×ATR dari tutup tertinggi | +2.9 | 27 | 6 | 31 | +2.4 | -19.2 | +0.5 | 98 |
| tutup di bawah harga beli − 1×ATR | jatuh 8×ATR dari tutup tertinggi | +4.2 | 23 | 6 | 31 | +3.8 | -23.7 | +0.7 | 99 |
| tutup di bawah harga beli − 1×ATR | jatuh 25 % dari tutup tertinggi | +6.2 | 21 | 6 | 31 | +5.8 | -25.4 | +0.6 | 100 |
| rugi pada hari ke-20 (semak sekali) | tiada | +49.1 | 15 | 16 | 36 | +48.4 | -31.6 | +9.8 | 100 |
| rugi pada hari ke-20 (semak sekali) | tutup di bawah purata 20 hari | +0.5 | 46 | 6 | 21 | -0.0 | -0.8 | -0.0 | 47 |
| rugi pada hari ke-20 (semak sekali) | tutup di bawah purata 50 hari | +0.9 | 40 | 6 | 21 | +0.4 | -7.2 | +0.0 | 85 |
| rugi pada hari ke-20 (semak sekali) | tutup di bawah purata 100 hari | +1.6 | 34 | 6 | 21 | +1.0 | -12.2 | +0.3 | 93 |
| rugi pada hari ke-20 (semak sekali) | tutup di bawah purata 200 hari | +2.7 | 31 | 7 | 21 | +2.3 | -15.1 | +1.0 | 97 |
| rugi pada hari ke-20 (semak sekali) | jatuh 4×ATR dari tutup tertinggi | +1.7 | 34 | 6 | 25 | +1.2 | -12.2 | +0.4 | 95 |
| rugi pada hari ke-20 (semak sekali) | jatuh 6×ATR dari tutup tertinggi | +3.2 | 30 | 8 | 33 | +2.8 | -16.6 | +1.9 | 99 |
| rugi pada hari ke-20 (semak sekali) | jatuh 8×ATR dari tutup tertinggi | +5.0 | 27 | 9 | 36 | +4.6 | -19.6 | +3.3 | 99 |
| rugi pada hari ke-20 (semak sekali) | jatuh 25 % dari tutup tertinggi | +7.9 | 25 | 8 | 32 | +7.5 | -21.1 | +2.6 | 100 |

## 5. Kesan had masa pada cara terpilih

| Cara pegang | Purata setiap dagangan % | Menang % | Rugi ≥ 15 % % | Untung ≥ 50 % % | Median hari pegang | Untung setiap 20 hari pegang % | Masih dipegang pada hujung data % | Dagangan setiap setup | Saham rawak, cara sama: purata % · menang % · setiap 20 hari % |
|---|---|---|---|---|---|---|---|---|---|
| jual bila tutup di bawah harga beli − 1×ATR ATAU tutup di bawah purata 20 hari · had 126 sesi | +0.5 | 46 | 6 | 0.7 | 21 | +0.42 | 0.0 | 892 | +0.7 · 47 · +0.58 |
| jual bila tutup di bawah harga beli − 1×ATR ATAU tutup di bawah purata 20 hari · had 252 sesi | +0.5 | 46 | 6 | 0.7 | 21 | +0.42 | 0.0 | 892 | +0.7 · 47 · +0.58 |
| jual bila tutup di bawah harga beli − 1×ATR ATAU tutup di bawah purata 20 hari · tanpa had masa | +0.5 | 46 | 6 | 0.7 | 21 | +0.42 | 0.0 | 892 | +0.7 · 47 · +0.58 |

## 6. Pemilihan pada saham carian (kumpulan A; nilai tengah beza lawan cara sekarang)

| Cara | Δ purata (mata) | Δ menang (mata) | Δ rugi ≥ 15 % (mata) |
|---|---|---|---|
| jual bila rugi pada hari ke-20 (semak sekali) · tanpa had masa | +55.4 | -34.0 | +9.8 |
| jual bila tutup di bawah harga beli − 1×ATR · tanpa had masa | +37.7 | -38.2 | +1.6 |
| jual bila tutup di bawah harga beli · tanpa had masa | +26.3 | -36.4 | +0.7 |
| jual bila jatuh 25 % dari tutup tertinggi · tanpa had masa | +10.5 | -17.6 | +5.6 |
| jual bila rugi pada hari ke-20 (semak sekali) ATAU jatuh 25 % dari tutup tertinggi · tanpa had masa | +8.4 | -21.8 | +2.2 |
| jual bila jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +6.9 | -15.8 | +6.2 |
| jual bila tutup di bawah harga beli − 1×ATR ATAU jatuh 25 % dari tutup tertinggi · tanpa had masa | +6.6 | -26.2 | +0.6 |
| jual bila rugi pada hari ke-20 (semak sekali) ATAU jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +5.5 | -20.4 | +2.8 |
| jual bila tutup di bawah harga beli ATAU jatuh 25 % dari tutup tertinggi · tanpa had masa | +5.2 | -26.9 | +0.2 |
| jual bila tutup di bawah harga beli − 1×ATR ATAU jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +4.5 | -24.4 | +0.6 |
| jual bila tutup di bawah harga beli ATAU jatuh 8×ATR dari tutup tertinggi · tanpa had masa | +3.6 | -25.7 | +0.2 |
| jual bila jatuh 6×ATR dari tutup tertinggi · tanpa had masa | +3.5 | -11.7 | +4.1 |

## 7. Kes rujukan pengguna: MXL (satu contoh, bukan bukti)

Beli 20260422 pada 34.00; data hingga 20261016; tutup tertinggi +277 %.

| Cara pegang | Jual | Hari | Untung % |
|---|---|---|---|
| jual pada hari ke-20 | 20260519 | 20 | +179 |
| cara sekarang: jual bila tutup di bawah purata 20 hari (had 6 bulan) | 20260602 | 29 | +169 |
| jual bila tutup di bawah purata 50 hari · tanpa had masa | 20260708 | 53 | +148 |
| jual bila jatuh 4×ATR dari tutup tertinggi · tanpa had masa | 20260717 | 60 | +108 |
| jual bila tutup di bawah purata 200 hari · tanpa had masa | masih dipegang | 124 | +109 |
| jual bila jatuh 8×ATR dari tutup tertinggi · tanpa had masa | 20260825 | 87 | +95 |
| jual bila tutup di bawah harga beli · tanpa had masa | masih dipegang | 124 | +109 |
| beli dan simpan, stop loss sahaja | masih dipegang | 124 | +109 |

## 8. Kaveat

- Tiada saham delist dalam data: saham yang gagal hilang, dan bias ini membesar dengan tempoh pegang. Purata cara yang memegang bertahun-tahun (cth. "tutup di bawah harga beli" sahaja) dikuasai beberapa saham yang naik berganda dan TIDAK boleh dipercayai.
- Posisi yang masih dipegang pada hujung data dinilai pada harga terakhir, bukan harga jual.
- 108 cara dicuba; yang terbaik condong ke atas. Kumpulan saham "tidak dilihat" sudah dilihat berkali-kali; 2025–26 pendek.
- Tangga tukar ganti dan kawalan rawak ditambah SELEPAS hasil dilihat (maklumat; bukan sebahagian ujian yang ditetapkan dahulu).
- Laporan dan cadangan sahaja: senarai utama, registry dan kohort tidak diubah. Menukar cara pegang ialah keputusan pengguna.
