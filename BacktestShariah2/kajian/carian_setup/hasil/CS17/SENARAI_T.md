# CS17: lorong "pegang berbulan-bulan" (T) tanpa had bilangan (backtest; BUKAN bukti)

Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (aa). Dijana `cs_trend17.py`; jangan sunting.

- Lorong ini: beli selepas isyarat, pegang hingga 6 bulan (126 hari dagangan) dengan stop loss longgar (6×ATR14), tiada jualan lain. "Naik besar" = harga tutup mencapai ≥ +50 % dalam 6 bulan SEBELUM mana-mana tutup ≤ −15 %.
- Saham rawak (mana-mana hari): 7.9 % naik besar; 1.4 % capai +100 %.
- Dicari pada saham carian: 5,105 calon (sehingga 5 peraturan setiap isyarat beli, tiada had bilangan); 300 peraturan rawak sebagai kawalan. Dinilai pada saham yang carian tidak lihat. Tiada tapisan Shariah.

## 1. Keputusan (ujian ditetapkan dahulu)

- Lulus = ≥ 200 belian, ≥ 8 tahun, lebih kerap naik besar daripada saham rawak hari sama dalam ketiga-tiga tempoh (2010–19, 2020–24, 2025–26).
- (B1) calon yang lulus: 4,167 daripada 4,988 yang cukup belian = 84 %; peraturan rawak: 34 % (perlu beza ≥ 20 mata) → ya.
- (B2) lebih baik daripada rawak pada 2025–26: calon 90 %; peraturan rawak 64 % (perlu ≥ 60 % dan beza ≥ 10 mata) → ya.
- **Keputusan: LULUS.** 4,167 lulus; 1,603 kembar (belian bertindih ≥ 80 %); **2,564 setup baharu diberi kod `T13`–`T2576`**. Anggaran bahagian yang lulus kerana nasib: 40 %.

## 2. Gambaran setup baharu (nilai tengah; saham yang carian tidak lihat)

| | Naik besar % | Saham rawak hari sama % | Menang % | Purata setiap dagangan % | Rugi ≥ 15 % % | Dijual ≥ +30 % % | Belian setahun |
|---|---|---|---|---|---|---|---|
| Setup baharu (2,564) | 20.0 | 13.9 | 46 | +6.4 | 41 | 22 | 31 |
| Peraturan rawak (kawalan) | 7.5 | 7.3 | 50 | +4.0 | 23 | – | – |
| Papan lama `T01`–`T12` (CS08) | 20.8 | 14.1 | 42 | +5.8 | 45 | 23 | 17 |

- 55 % setup baharu memakai prasyarat "hasil suku terkini tumbuh ≥ 20 %" (calon: 52 %).
- 97 % setup baharu menambah ≥ 1 mata di atas prasyaratnya sahaja (nilai tengah tambahan +5.1 mata).
- Kes MXL (Mac–Jun 2026; satu contoh, bukan bukti): 1,005 setup baharu memberi isyarat beli pada MXL.

## 3. Senarai (60 teratas ikut kadar naik besar; penuh dalam `senarai_t.csv`)

| ID | Prasyarat | Isyarat beli | Syarat saham | Naik besar % (rawak) | Capai +100 % % | Menang % | Purata % | Rugi ≥ 15 % % | Belian | Lebih baik drpd rawak: 2010–19 / 2020–24 / 2025–26 (mata) | Atas prasyarat (mata) | MXL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `T964` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K16.001 gap-and-go (buka > tinggi semalam + 0.0%) | RSI14 > 50 + ATR% >= 4 | **38.5** (20.2) | 13.0 | 58 | +20.8 | 34 | 208 | +13.0 / +20.8 / +24.7 | +14.2 | – |
| `T730` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K16.001 gap-and-go (buka > tinggi semalam + 0.0%) | ATR% >= 4 | **37.7** (20.3) | 12.8 | 60 | +20.4 | 32 | 265 | +11.4 / +21.6 / +22.0 | +13.3 | – |
| `T32` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s6: a14_kali_0_5=0.75, atr_14=28, np_ambang_2=1, pivot_k_3=2, rolling_20=35, rolling_50=84) | MACD > isyarat + ATR% >= 4 | **37.0** (21.9) | 12.3 | 60 | +20.1 | 29 | 332 | +12.3 / +17.4 / +16.9 | +11.0 | – |
| `T197` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | RS >= 70 + ATR% >= 4 | **36.1** (17.8) | 11.4 | 54 | +18.7 | 35 | 202 | +15.2 / +19.4 / +26.8 | +14.2 | – |
| `T138` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, varian 1: had_henti=0.732, henti_pct=13.462, hh_kali_0_1=0.119, keluar_sma=19, shift_5=8, tmax=6) | tutup > MA200 + ATR% >= 4 | **34.9** (16.1) | 11.1 | 53 | +12.9 | 37 | 235 | +16.3 / +15.9 / +35.7 | +14.7 | – |
| `T662` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M13 Garis Trend Action/Safety Line (benih M, varian 1: k=2) | RSI14 > 50 + ATR% >= 4 | **34.4** (19.1) | 8.4 | 52 | +12.3 | 36 | 227 | +10.2 / +13.4 / +35.4 | +11.2 | – |
| `T15` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s8: a14_kali_0_5=0.688, atr_14=26, np_ambang_2=1, pivot_k_3=2, rolling_20=36, rolling_50=80) | tutup > MA20 + ATR% >= 4 | **34.3** (20.9) | 11.1 | 57 | +17.3 | 32 | 359 | +11.4 / +15.0 / +14.7 | +9.2 | – |
| `T137` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K02.014 RSI(7) silang atas 60 | MACD > isyarat + ATR% >= 4 | **34.1** (20.2) | 9.9 | 54 | +15.7 | 34 | 273 | +10.6 / +14.7 / +21.8 | +9.7 | – |
| `T58` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M14 Walking with the Whales (benih M, varian 2: rolling_50=34, shift_2=3) | MACD > isyarat + ATR% >= 4 | **33.5** (20.6) | 10.3 | 54 | +15.2 | 33 | 397 | +10.5 / +14.9 / +14.5 | +8.8 | – |
| `T463` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K10.009 pecah tinggi 20 hari | Supertrend naik + ATR% >= 4 | **33.5** (17.5) | 11.5 | 48 | +15.8 | 41 | 209 | +13.8 / +19.6 / +14.7 | +11.9 | – |
| `T13` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s8: a14_kali_0_5=0.688, atr_14=26, np_ambang_2=1, pivot_k_3=2, rolling_20=36, rolling_50=80) | Supertrend naik + ATR% >= 4 | **33.1** (19.8) | 12.0 | 54 | +16.9 | 33 | 308 | +11.4 / +13.8 / +16.9 | +9.2 | – |
| `T226` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M125 2-Bar Breakout (benih M, varian 1: had_henti=0.799, henti_atr=1.979, shift_2=3, shift_3=6) | RSI14 > 50 + ATR% >= 4 | **32.9** (18.8) | 9.4 | 52 | +14.1 | 37 | 371 | +13.4 / +12.9 / +19.0 | +9.9 | – |
| `T23` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | RSI14 > 50 + ATR% >= 4 | **32.4** (18.3) | 9.7 | 54 | +14.6 | 36 | 373 | +11.9 / +12.4 / +27.5 | +10.1 | – |
| `T28` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, varian 1: had_henti=0.732, henti_pct=13.462, hh_kali_0_1=0.119, keluar_sma=19, shift_5=8, tmax=6) | Supertrend naik + ATR% >= 4 | **32.4** (17.8) | 10.9 | 51 | +13.0 | 37 | 312 | +11.6 / +14.9 / +25.0 | +10.5 | – |
| `T543` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K10.001 pecah tinggi 5 hari | Supertrend naik + ATR% >= 4 | **32.3** (17.2) | 9.7 | 48 | +13.2 | 41 | 269 | +11.6 / +16.6 / +21.6 | +11.0 | – |
| `T49` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, varian 2: had_henti=0.575, henti_pct=16.388, hh_kali_0_1=0.117, keluar_sma=11, shift_5=8, tmax=16) | RSI14 > 50 + ATR% >= 4 | **32.3** (18.3) | 10.6 | 55 | +14.3 | 35 | 387 | +11.7 / +13.4 / +24.2 | +9.8 | – |
| `T561` | nisbah 4% (10 hari) > 2 + >= 60% saham sektor di atas MA50 | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: rank_ambang_0_8=0.508, shift_21=11) | RS >= 90 + ATR% >= 4 | **32.0** (20.3) | 10.4 | 54 | +14.1 | 35 | 384 | +8.8 / +11.7 / +23.2 | +11.4 | – |
| `T800` | Mei-Okt + hasil suku terkini tumbuh >= 20% | N80 Tinggi sepanjang masa (benih N) | RS >= 90 + ATR% >= 4 | **31.8** (17.0) | 11.7 | 53 | +17.6 | 38 | 223 | +17.1 / +13.1 / +14.3 | +12.1 | 20260501@77.74 |
| `T196` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K05.001 tutup silang atas jalur atas BB(10, 1.5) | RSI14 > 50 + ATR% >= 4 | **31.8** (17.8) | 9.6 | 53 | +14.5 | 38 | 311 | +10.1 / +17.0 / +18.3 | +9.9 | – |
| `T152` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | ATR% >= 4 | **31.8** (18.4) | 8.9 | 55 | +14.3 | 35 | 437 | +10.7 / +12.9 / +24.5 | +9.3 | – |
| `T1537` | >= 60% saham di atas MA200 + 5-19 sesi selepas earnings | K11.012 Supertrend(14, 2.0) bertukar naik | RS >= 90 + ATR% >= 4 | **31.8** (18.1) | 7.9 | 53 | +18.6 | 37 | 305 | +19.3 / +10.3 / +10.2 | +14.8 | – |
| `T24` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 9s8: a14_kali_0_5=0.688, atr_14=26, np_ambang_2=1, pivot_k_3=2, rolling_20=36, rolling_50=80) | ATR% >= 4 | **31.8** (19.8) | 10.1 | 54 | +14.7 | 34 | 447 | +10.8 / +12.1 / +14.9 | +7.9 | – |
| `T305` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K07.001 tutup silang atas sma5 | MACD > isyarat + ATR% >= 4 | **31.7** (21.6) | 9.7 | 53 | +12.9 | 34 | 309 | +10.0 / +8.1 / +18.0 | +6.0 | – |
| `T1976` | industri 20% teratas (pulangan 21 sesi) | M107 Golden Cross SMA50/200 (benih M, varian 2: rma_atr_14=16, rma_atr_kali_3=2.729, rolling_200=131, rolling_50=59) | tutup > MA50 + ATR% >= 4 | **31.7** (20.0) | 13.1 | 53 | +17.4 | 38 | 344 | +13.1 / +9.1 / +20.0 | +11.6 | – |
| `T612` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M116 2/20 EMA Breakout (Landry) (benih M, parameter asal) | Supertrend naik + ATR% >= 4 | **31.6** (17.8) | 11.4 | 51 | +16.1 | 38 | 237 | +8.7 / +15.8 / +24.3 | +9.7 | – |
| `T21` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M159 Heikin-Ashi Trend (benih M, parameter asal) | Supertrend naik + ATR% >= 4 | **31.5** (17.4) | 9.4 | 50 | +12.0 | 40 | 298 | +12.1 / +12.4 / +26.0 | +10.1 | – |
| `T417` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K19.006 pecah atas Keltner(20, 1.0) | ATR% >= 4 | **31.5** (17.7) | 10.5 | 50 | +13.9 | 38 | 267 | +12.1 / +15.4 / +14.9 | +9.6 | – |
| `T184` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M116 2/20 EMA Breakout (Landry) (benih M, varian 1: ema_20=24, had_henti=0.556, henti_pct=13.989, shift_2=3, tmax=5) | ATR% >= 4 + hari naik (tutup > buka) | **31.4** (17.6) | 10.9 | 49 | +14.2 | 39 | 229 | +7.9 / +17.0 / +27.6 | +9.7 | – |
| `T1037` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K19.001 pecah atas Keltner(10, 1.0) | Supertrend naik + ATR% >= 4 | **31.4** (16.6) | 9.9 | 50 | +12.8 | 40 | 223 | +13.4 / +13.8 / +23.0 | +10.6 | – |
| `T828` | nisbah 4% (10 hari) > 2 + >= 60% saham industri di atas MA50 | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: rank_ambang_0_8=0.508, shift_21=11) | RS >= 70 + ATR% >= 4 | **31.1** (20.7) | 8.7 | 60 | +16.3 | 28 | 527 | +5.8 / +11.8 / +17.2 | +10.2 | – |
| `T30` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | M27 Price Action 4 Tiang (benih M, varian 2: a14_kali_0_5=0.54, atr_14=25, np_ambang_2=2, pivot_k_3=2, rolling_20=27, rolling_50=53) | Supertrend naik + ATR% >= 4 | **31.1** (18.8) | 10.7 | 54 | +14.7 | 35 | 270 | +9.7 / +13.9 / +16.1 | +8.2 | – |
| `T266` | nisbah 4% (10 hari) > 2 + >= 60% saham sektor di atas MA50 | M84 Jarak purata bergerak MAD 21/200 (benih M, parameter asal) | Supertrend naik + ATR% >= 4 | **31.0** (21.2) | 10.8 | 50 | +10.9 | 36 | 342 | +8.2 / +9.0 / +21.7 | +9.5 | – |
| `T2097` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham sektor di atas MA50 | M107 Golden Cross SMA50/200 (benih M, parameter asal) | RSI14 > 50 + ATR% >= 4 | **31.0** (18.8) | 9.7 | 56 | +17.2 | 33 | 413 | +5.9 / +12.7 / +25.7 | +12.0 | – |
| `T2413` | QQQ OFF + hasil suku terkini tumbuh >= 20% | K22.011 Holy Grail (ADX > 35, undur EMA20) | RS >= 70 + ATR% >= 4 | **30.9** (18.4) | 10.6 | 59 | +16.8 | 29 | 217 | +13.7 / +7.1 / +25.8 | +11.0 | – |
| `T749` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K10.005 pecah tinggi 10 hari | RSI14 > 50 + ATR% >= 4 | **30.8** (17.9) | 9.2 | 51 | +13.7 | 40 | 292 | +9.0 / +18.5 / +12.1 | +8.8 | – |
| `T437` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | K10.005 pecah tinggi 10 hari | Supertrend naik + ATR% >= 4 | **30.7** (17.1) | 9.4 | 49 | +13.5 | 41 | 244 | +11.7 / +16.3 / +13.6 | +9.5 | – |
| `T2063` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham industri di atas MA50 | K08.023 sma50 silang atas sma200 | Supertrend naik + ATR% >= 4 | **30.6** (18.2) | 9.5 | 58 | +17.7 | 30 | 474 | +10.5 / +11.5 / +23.6 | +12.3 | – |
| `T679` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M137 Livermore System (benih M, varian 1: a_kali_4=4.259, atr_kali_6=6.193, henti_atr=1.764, keluar_chan=2.342, keluar_chan_atr=36, keluar_chan_tinggi=14) | RS >= 90 + ATR% >= 4 | **30.5** (16.7) | 10.7 | 47 | +10.0 | 41 | 243 | +11.4 / +11.3 / +24.7 | +11.5 | – |
| `T2521` | SPY bawah SMA200 | K18.012 jatuh >= 20% dalam 3 hari | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | **30.3** (26.6) | 10.3 | 66 | +24.3 | 23 | 1,184 | +7.2 / +2.6 / +5.7 | +3.8 | – |
| `T848` | >= 60% saham di atas MA200 + hasil suku terkini tumbuh >= 20% | K04.007 masuk semula atas jalur bawah BB(30, 1.5) | RS >= 90 + ATR% >= 4 | **30.2** (15.5) | 9.3 | 47 | +8.6 | 40 | 258 | +16.7 / +12.0 / +17.3 | +13.0 | 20260611@80.8 |
| `T1980` | turun-naik SPY menurun (21 hari < 63 hari) + >= 60% saham sektor di atas MA50 | K08.023 sma50 silang atas sma200 | Supertrend naik + ATR% >= 4 | **29.8** (17.8) | 9.5 | 58 | +17.6 | 31 | 473 | +5.8 / +12.8 / +24.3 | +11.8 | – |
| `T884` | >= 60% saham di atas MA200 + hasil suku terkini tumbuh >= 20% | M89 Chande 65sma-3cc (benih M, parameter asal) | RS >= 90 + ATR% >= 4 | **29.8** (19.3) | 6.8 | 48 | +11.2 | 40 | 205 | +15.4 / +6.3 / +12.5 | +8.8 | – |
| `T2279` | SPY bawah SMA200 + saham lain dalam industri sama naik >= 20% dalam 20 sesi | K18.026 jatuh >= 20% dalam 10 hari | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | **29.6** (24.8) | 7.2 | 56 | +16.8 | 30 | 581 | +4.4 / +5.4 / +2.2 | +4.6 | – |
| `T1227` | Mei-Okt + industri 20% teratas (pulangan 63 sesi) | M78 Alvarez Pecahan Mingguan DTAYS (benih M, parameter asal) | dalam 15% dari puncak 52 minggu + ATR% >= 4 | **29.6** (19.8) | 9.4 | 52 | +19.2 | 39 | 318 | +1.2 / +6.9 / +26.2 | +9.0 | 20260501@77.74 |
| `T2111` | turun-naik SPY menurun (21 hari < 63 hari) | M107 Golden Cross SMA50/200 (benih M, parameter asal) | Supertrend naik + ATR% >= 4 | **29.6** (18.6) | 9.9 | 55 | +15.9 | 34 | 538 | +8.6 / +11.3 / +13.7 | +11.0 | – |
| `T1840` | Nov-Apr + hasil suku terkini tumbuh >= 20% | K08.013 sma10 silang atas sma50 | RS >= 70 + ATR% >= 4 | **29.5** (16.9) | 7.9 | 55 | +15.7 | 34 | 403 | +11.7 / +11.2 / +17.0 | +11.7 | 20260409@20.08 |
| `T2179` | Mei-Okt + >= 60% saham sektor di atas MA50 | K15.003 gap >= 2.0% + volum 2.0x | templat trend Minervini + ATR% >= 4 | **29.5** (20.1) | 10.6 | 50 | +13.3 | 38 | 254 | +18.0 / +6.3 / +0.3 | +9.4 | 20260508@101.38 |
| `T2107` | turun-naik SPY menurun (21 hari < 63 hari) | M107 Golden Cross SMA50/200 (benih M, parameter asal) | tutup > MA20 + ATR% >= 4 | **29.5** (18.8) | 9.3 | 54 | +14.8 | 35 | 471 | +6.9 / +11.1 / +17.1 | +10.8 | – |
| `T119` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N45 Undur EMA21 cerun positif (benih N) | tutup > MA20 + ATR% >= 4 | **29.5** (19.2) | 8.5 | 56 | +15.3 | 28 | 200 | +9.2 / +13.1 / +3.6 | +6.2 | – |
| `T1627` | SPY atas SMA200 + 5-19 sesi selepas earnings | M105 Supertrend tulen (benih M, varian 1: close_kali_0_88=0.469, m=2.046, n=8) | RS >= 90 + ATR% >= 4 | **29.5** (17.3) | 6.7 | 52 | +14.8 | 39 | 356 | +18.2 / +8.9 / +9.7 | +13.0 | – |
| `T650` | nisbah 4% (10 hari) > 2 | M84 Jarak purata bergerak MAD 21/200 (benih M, parameter asal) | MA20 > MA50 + ATR% >= 4 | **29.2** (20.1) | 10.1 | 47 | +7.8 | 39 | 407 | +11.6 / +6.8 / +21.7 | +9.1 | – |
| `T259` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | K09.021 MACD(3,10,16) silang naik atas sifar | RS >= 90 + ATR% >= 4 | **29.1** (16.1) | 10.2 | 44 | +9.1 | 45 | 354 | +14.7 / +11.5 / +14.0 | +11.0 | 20260615@88.0 |
| `T2325` | industri 20% teratas (pulangan 21 sesi) | K08.022 ema50 silang atas ema150 | MA20 > MA50 + ATR% >= 4 | **29.0** (19.3) | 8.1 | 59 | +17.2 | 34 | 455 | +9.3 / +9.6 / +11.1 | +9.6 | – |
| `T1666` | turun-naik SPY 21 hari >= 25% setahun + industri 20% terbawah (pulangan 63 sesi) | K03.027 tutup < jalur bawah BB(20, 1.5) + RSI14 < 40 | >= 30% di bawah puncak 52 minggu + ATR% >= 4 | **29.0** (24.9) | 6.1 | 66 | +20.0 | 23 | 831 | +2.5 / +3.4 / +8.6 | +4.0 | – |
| `T1284` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + >= 60% saham industri di atas MA50 | M152 Spike & Ledge (benih M, parameter asal) | tutup > MA200 + ATR% >= 4 | **29.0** (18.8) | 9.8 | 53 | +11.2 | 37 | 407 | +10.3 / +8.8 / +16.0 | +10.1 | – |
| `T180` | regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | N68 Bullish engulfing + EMA21 (benih N) | RS >= 90 + ATR% >= 4 | **28.8** (15.5) | 10.7 | 45 | +8.3 | 41 | 215 | +11.8 / +17.5 / +6.8 | +11.3 | 20260519@97.61 |
| `T569` | turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | M94 Pecutan Momentum (Chen, Yu & Wang) (benih M, varian 1: rank_ambang_0_8=0.508, shift_21=11) | Supertrend naik + ATR% >= 4 | **28.8** (19.2) | 10.6 | 53 | +13.4 | 37 | 444 | +4.2 / +10.8 / +14.8 | +7.4 | 20260529@92.29 |
| `T1477` | QQQ SMA10 > SMA20 + hasil suku terkini tumbuh >= 20% | K15.005 gap >= 3.0% | RS >= 70 + ATR% >= 4 | **28.8** (18.0) | 10.4 | 52 | +14.8 | 38 | 569 | +15.1 / +9.8 / +9.5 | +9.5 | 20260421@34.0 |
| `T1407` | turun-naik SPY menurun (21 hari < 63 hari) + sektor 3 teratas (pulangan 63 sesi) | M82 Arthur Hill Rotasi Sasaran 10% (benih M, varian 2: e_kali_1_1=1.237, rolling_20=40, rolling_250=211, sd250_ambang_20=29, sma20_ambang_10=9, sma20_ambang_5000000=2560294) | RS >= 70 + ATR% >= 4 | **28.8** (16.6) | 5.8 | 50 | +9.2 | 40 | 344 | +13.1 / +11.9 / +11.0 | +11.9 | – |
| `T394` | distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | N45 Undur EMA21 cerun positif (benih N) | RSI14 > 50 + ATR% >= 4 | **28.7** (18.3) | 8.8 | 54 | +14.1 | 32 | 216 | +9.6 / +12.7 / +5.4 | +6.3 | – |

## 4. "Prasyarat sahaja" (tanpa isyarat beli; 12 teratas)

| Prasyarat | Naik besar % (rawak) | Lebih baik drpd rawak (mata) | 2010–19 / 2020–24 / 2025–26 | Menang % | Purata % | Rugi ≥ 15 % % | Belian | Lulus |
|---|---|---|---|---|---|---|---|---|
| distribution day QQQ <= 2 dalam 25 sesi + hasil suku terkini tumbuh >= 20% | 15.0 (10.8) | +4.1 | +3.0 / +4.6 / +13.8 | 54 | +8.3 | 27 | 2,472 | ya |
| Mei-Okt + hasil suku terkini tumbuh >= 20% | 14.0 (11.3) | +2.7 | +2.3 / +1.9 / +10.5 | 52 | +6.8 | 29 | 4,593 | ya |
| follow-through day aktif (QQQ, 20 sesi) + hasil suku terkini tumbuh >= 20% | 15.5 (13.1) | +2.4 | +1.2 / +2.2 / +7.9 | 51 | +7.2 | 32 | 3,747 | ya |
| nisbah 4% (10 hari) > 2 + hasil suku terkini tumbuh >= 20% | 13.0 (10.7) | +2.3 | +2.1 / +2.2 / +4.5 | 49 | +5.1 | 32 | 5,388 | ya |
| turun-naik SPY 21 hari <= 10% setahun + hasil suku terkini tumbuh >= 20% | 11.7 (9.5) | +2.2 | +2.1 / +1.7 / +5.1 | 47 | +4.2 | 32 | 4,270 | ya |
| Januari + hasil suku terkini tumbuh >= 20% | 12.6 (10.5) | +2.2 | +3.6 / +1.2 / +1.4 | 45 | +2.5 | 35 | 2,473 | ya |
| turun-naik SPY menurun (21 hari < 63 hari) + hasil suku terkini tumbuh >= 20% | 13.1 (11.0) | +2.2 | +2.1 / +1.8 / +4.7 | 49 | +5.3 | 32 | 5,821 | ya |
| rejim ON baharu (<= 10 sesi) + hasil suku terkini tumbuh >= 20% | 12.7 (10.7) | +2.0 | +2.3 / +1.6 / +2.4 | 49 | +5.5 | 33 | 5,276 | ya |
| regangan turun-naik SPY (proksi VIX) + SPY > SMA200 + hasil suku terkini tumbuh >= 20% | 11.8 (9.8) | +2.0 | +2.5 / +1.6 / +1.8 | 47 | +3.8 | 34 | 5,433 | ya |
| QQQ naik >= 3% dalam 5 sesi + hasil suku terkini tumbuh >= 20% | 12.6 (10.6) | +2.0 | +2.3 / +1.7 / +1.9 | 49 | +5.2 | 32 | 5,922 | ya |
| QQQ RSI14 < 35 + hasil suku terkini tumbuh >= 20% | 12.7 (10.7) | +1.9 | +1.8 / +2.0 / +1.7 | 53 | +6.6 | 32 | 3,951 | ya |
| QQQ dalam 3% dari puncak 52 minggu + hasil suku terkini tumbuh >= 20% | 12.7 (10.8) | +1.9 | +1.8 / +1.6 / +3.3 | 49 | +4.7 | 31 | 5,048 | ya |

## 5. Kaveat

- Tiada saham delist dalam data: bagi pegang 6 bulan, saham yang gagal hilang dan angka condong ke atas lebih daripada lorong swing.
- Lorong ini banyak rugi besar: lihat lajur "Rugi ≥ 15 %". Purata dikuasai sebilangan kecil saham yang naik besar.
- 2025–26 pendek (isyarat hingga awal 2026 sahaja, kerana perlu 6 bulan penuh selepas beli).
- Beribu calon disemak pada saham yang sama, jadi sebahagian lulus kerana nasib (anggaran di atas).
- Semakan kembar lawan `T01`–`T12` tidak dapat dibuat (isyarat varian lama tiada dalam folder kerja).
- Kod T bukan kod F: `registry_F.csv` tidak disentuh. Tiada papertrade tanpa keputusan pengguna.
