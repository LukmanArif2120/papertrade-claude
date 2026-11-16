# CS03: 50 peraturan masuk teratas ikut kadar tangkap (backtest, BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_ringkas.py` daripada `hasil/CS03/senarai_kunci.csv` (200 teratas + 200 rawak). **Jangan sunting secara manual.**

Pangkat ditentukan pada kumpulan A (separuh set 2000 yang dicari). Angka di bawah daripada **kumpulan B** (saham yang tidak dilihat, 2010 – Ogo 2026), dalam MATA PERATUS melebihi saham rawak pada hari dan tercile ATR% yang sama. "Lari" = naik ≥ 5 % minggu pertama, capai ≥ 10 % sebelum henti −8 %, masih ≥ 10 % pada minggu ke-4. "Lari 2025–26" = kepingan K3 (tahun yang tidak dilihat).

| # | Masuk | Penapis | Belian | Lebih lari | Lebih capai +10% | Lebih kena henti | Lari 2025–26 |
|---|---|---|---|---|---|---|---|
| 1 | N40 OBV tinggi baharu + MA50 | tutup > MA200 + >= 30% di bawah puncak 52 minggu | 851 | +1.7 | +2.2 | +6.8 | +4.1 |
| 2 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | ATR% >= 4 + rejim QQQ ON | 2,480 | +3.5 | +4.9 | +7.3 | +2.7 |
| 3 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 90 + SPY > SMA200 | 630 | +4.3 | +4.4 | +10.2 | +0.1 |
| 4 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | ATR% >= 4 + rejim QQQ ON | 2,251 | +3.0 | +4.2 | +7.3 | +1.5 |
| 5 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) (ditala 2) | RS >= 90 + SPY > SMA200 | 627 | +4.9 | +6.1 | +10.0 | +0.2 |
| 6 | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (ditala 2) | RS >= 90 + ATR% >= 4 | 2,405 | +3.1 | +3.9 | +7.0 | +2.0 |
| 7 | M57 Landry Trend Knockout (TKO) (ditala 1) | RS >= 90 + ATR% >= 4 | 3,166 | +2.5 | +2.2 | +8.8 | +0.5 |
| 8 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) (ditala 1) | RS >= 90 + SPY > SMA200 | 480 | +4.6 | +7.5 | +7.8 | -0.6 |
| 9 | M50 Elder Triple Screen (ditala 2) | RS >= 90 + ATR% >= 4 | 3,388 | +2.4 | +5.0 | +6.5 | -0.5 |
| 10 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 90 + dalam 15% dari puncak 52 minggu | 655 | +3.9 | +3.0 | +9.4 | -1.4 |
| 11 | M57 Landry Trend Knockout (TKO) (ditala 2) | RS >= 90 + ATR% >= 4 | 3,827 | +2.1 | +3.0 | +8.2 | -0.6 |
| 12 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | MA50 naik (lawan 20 bar lalu) + RS >= 90 | 669 | +2.3 | +2.0 | +10.2 | -1.6 |
| 13 | N73 Tutup bawah jalur bawah BB(20,2) | RS >= 70 + ATR% >= 4 | 4,816 | +2.5 | +4.4 | +0.7 | +3.2 |
| 14 | M92 CCI-50 (ditala 2) | >= 30% di bawah puncak 52 minggu + rejim QQQ OFF | 2,704 | +1.7 | +3.6 | +3.5 | +2.5 |
| 15 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | ATR% >= 4 + SPY > SMA200 | 2,933 | +2.9 | +2.8 | +9.1 | +1.8 |
| 16 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | ATR% >= 4 + SPY > SMA200 | 3,309 | +3.2 | +3.2 | +8.9 | +1.9 |
| 17 | P13 RSI14 silang atas 60 | RS >= 90 + ATR% >= 4 | 4,009 | +2.0 | +2.6 | +6.7 | -0.5 |
| 18 | N73 Tutup bawah jalur bawah BB(20,2) | tutup > MA200 + ATR% >= 4 | 5,687 | +1.9 | +3.7 | +0.8 | +0.9 |
| 19 | M50 Elder Triple Screen (ditala 1) | RS >= 90 + ATR% >= 4 | 3,127 | +2.9 | +4.8 | +5.7 | +0.7 |
| 20 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | MA20 > MA50 + ATR% >= 4 | 3,402 | +3.3 | +3.4 | +6.8 | +3.0 |
| 21 | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (ditala 2) | RS >= 70 + ATR% >= 4 | 4,205 | +1.7 | +3.4 | +3.8 | +2.0 |
| 22 | N43 Undur EMA8 + penapis MA50 | Supertrend naik + ATR% >= 4 | 10,715 | +1.4 | +2.6 | +4.4 | +1.6 |
| 23 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RSI14 > 60 + RS >= 90 | 739 | +4.0 | +3.7 | +8.9 | +1.3 |
| 24 | M149 3-Step Pullback (ditala 2) | RS >= 90 + ATR% >= 4 | 2,686 | +2.3 | +4.7 | +6.9 | +1.2 |
| 25 | N43 Undur EMA8 + penapis MA50 | tutup > MA20 + ATR% >= 4 | 12,720 | +1.6 | +2.2 | +4.4 | +2.4 |
| 26 | M161 EMA 10/21 + Supertrend (10,3) (ditala 1) | RS >= 90 + ATR% >= 4 | 3,998 | +2.0 | +3.1 | +6.3 | +1.3 |
| 27 | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (ditala 2) | MA50 > MA200 + ATR% >= 4 | 4,605 | +2.0 | +3.0 | +3.7 | +1.9 |
| 28 | P29 Holy Grail (ADX>30, undur EMA20, tutup > tinggi semalam) | Supertrend naik + RS >= 90 | 1,339 | +0.8 | +0.9 | +4.9 | -1.8 |
| 29 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | MACD > 0 + RS >= 90 | 748 | +4.3 | +4.2 | +8.6 | +1.2 |
| 30 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | templat trend Minervini + RS >= 90 | 584 | +3.4 | +2.7 | +8.8 | -1.8 |
| 31 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | templat trend Minervini + ATR% >= 4 | 2,854 | +2.3 | +3.6 | +7.2 | +1.2 |
| 32 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | dalam 15% dari puncak 52 minggu + ATR% >= 4 | 2,783 | +2.8 | +3.7 | +6.3 | +1.3 |
| 33 | M94 Pecutan Momentum (Chen, Yu & Wang) (ditala 1) | ATR% >= 4 + rejim QQQ ON | 3,921 | +3.0 | +4.0 | +3.8 | +1.5 |
| 34 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | Supertrend naik + RS >= 90 | 739 | +4.1 | +4.1 | +8.7 | +1.2 |
| 35 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | tutup > MA50 + ATR% >= 4 | 3,322 | +2.4 | +2.9 | +7.4 | +2.1 |
| 36 | N43 Undur EMA8 + penapis MA50 | MACD > isyarat + ATR% >= 4 | 7,549 | +1.7 | +2.7 | +3.4 | +1.8 |
| 37 | P48 EMA crossback | RS >= 90 + ATR% >= 4 | 2,651 | +2.1 | +5.0 | +5.1 | -1.1 |
| 38 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | Supertrend naik + ATR% >= 4 | 2,774 | +2.8 | +2.9 | +7.6 | +1.8 |
| 39 | P16 RSI2<5 atas MA200 | volum hari isyarat >= 1.5x purata 50 + ATR% >= 4 | 2,343 | +2.9 | +4.8 | -0.4 | +1.2 |
| 40 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | tutup > MA20 + RS >= 90 | 763 | +4.4 | +4.3 | +8.6 | +1.4 |
| 41 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 90 | 763 | +4.4 | +4.3 | +8.6 | +1.4 |
| 42 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RS >= 70 + RS >= 90 | 763 | +4.4 | +4.3 | +8.6 | +1.4 |
| 43 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | RSI14 > 50 + RS >= 90 | 763 | +4.4 | +4.3 | +8.6 | +1.4 |
| 44 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | tutup > MA200 + RS >= 90 | 760 | +4.3 | +4.3 | +8.7 | +1.4 |
| 45 | M21 Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan) | tutup > MA50 + RS >= 90 | 762 | +4.4 | +4.3 | +8.6 | +1.4 |
| 46 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | MA50 naik (lawan 20 bar lalu) + ATR% >= 4 | 3,741 | +2.8 | +3.1 | +7.2 | +3.1 |
| 47 | M84 Jarak purata bergerak MAD 21/200 (ditala 1) | tutup > MA50 + ATR% >= 4 | 3,283 | +2.5 | +3.2 | +7.3 | +2.3 |
| 48 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | RSI14 > 50 + ATR% >= 4 | 2,979 | +2.6 | +2.8 | +7.5 | +2.6 |
| 49 | M161 EMA 10/21 + Supertrend (10,3) (ditala 1) | ATR% >= 4 + tutup dalam 25% teratas julat hari | 10,453 | +1.3 | +2.6 | +4.5 | +1.9 |
| 50 | M84 Jarak purata bergerak MAD 21/200 (ditala 2) | MA50 naik (lawan 20 bar lalu) + ATR% >= 4 | 3,256 | +2.7 | +3.2 | +7.1 | +2.7 |

## Bacaan

- Median "lebih lari" +2.8 mata; 41 daripada 50 kekal positif pada 2025–26; median "lebih kena henti" +7.2 mata.
- Hanya 16 pencetus berbeza: banyak baris ialah kembar (pencetus sama, penapis hampir sama). Papan 10 teratas (`F21`–`F30`) mengambil satu sahaja bagi setiap pencetus.
- Ini kadar tangkap, bukan untung. Untung setiap dagangan hanya dikira untuk papan dan anak-anaknya (`kajian/CARIAN_SETUP.md`, `hasil/CS03/LAPORAN.md`, `hasil/CS04/LAPORAN.md`).
