# Jejak hadapan kohort F (papertrade maya; BUKAN keputusan wang sebenar)

> **Status keputusan (kad skor, harga 2026-11-16):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_hadapan.py`; harga hingga 20261116; isyarat sejak 20261113. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 13 Nov 2026 (f). Penjejak berasingan, bukan Lejar; tiada order. **Jangan sunting secara manual.**

| ID | Masuk | Penapis | Henti | Keluar | Isyarat | Tunggu beli | Terbuka | Ditutup | Purata ditutup % | Menang % | Tetingkap lengkap | Lari % (rawak) | Capai +10 % dahulu % (rawak) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `F21` | N40 OBV tinggi baharu + MA50 (benih N) | F03 tutup > MA200 DAN F20 >= 30% di bawah puncak 52 minggu | H2 -10% | X09 MACD < isyarat ATAU X10 histogram MACD turun 3 hari | 0 | 0 | 0 | 0 | – | – | 0 | – | – |
| `F22` | M84 Jarak purata bergerak MAD 21/200 (benih M, varian 1: close_ambang_5=2, rma_atr_14=19, rma_atr_kali_3=2.188, rolling_200=350, rolling_21=19, rolling_50=85) | F23 ATR% >= 4 DAN F26 rejim QQQ ON | H2 -10% | X11 RSI14 < 50 ATAU X21 Stochastic silang turun di atas 80 | 0 | 0 | 0 | 0 | – | – | 0 | – | – |
| `F34` | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (benih M, varian t7: rolling_26=32, rolling_52=104, rolling_9=8, shift_26=48) [tala daripada F24] | RS >= 95 DAN ATR% >= 4 | H4 4xATR14 | X21 Stochastic silang turun di atas 80 ATAU X22 hari turun dengan volum >= 1.5x | 2 | 1 | 1 | 0 | – | – | 0 | – | – |
| `F27` | N73 Tutup bawah jalur bawah BB(20,2) (benih N) | F16 RS >= 70 DAN F23 ATR% >= 4 | H4 4xATR14 | X07 dua tutup berturut < MA20 DAN X21 Stochastic silang turun di atas 80 | 6 | 6 | 0 | 0 | – | – | 0 | – | – |
| `F28` | M92 CCI-50 (benih M, varian 2: cci_50=91, rma_atr_14=15, rma_atr_kali_2=2.496) | F20 >= 30% di bawah puncak 52 minggu DAN F27 rejim QQQ OFF | H4 4xATR14 | X20 tutup < 92% tutup tertinggi sejak beli DAN X21 Stochastic silang turun di atas 80 | 1 | 1 | 0 | 0 | – | – | 0 | – | – |
| `F38` | P13 RSI14 silang atas 60 [tala daripada F29] | RS >= 95 DAN ATR% >= 4 | H2 -10% | X14 Supertrend turun ATAU X18 Chandelier 3xATR14 (dari tutup tertinggi sejak beli) | 2 | 0 | 2 | 0 | – | – | 0 | – | – |
| `F30` | N43 Undur EMA8 + penapis MA50 (benih N) | F15 Supertrend naik DAN F23 ATR% >= 4 | H4 4xATR14 | X21 Stochastic silang turun di atas 80 DAN X22 hari turun dengan volum >= 1.5x | 13 | 5 | 8 | 0 | – | – | 0 | – | – |
| `F24` | M49 Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun) (benih M, varian 2: rolling_26=33, rolling_52=93, rolling_9=8, shift_26=40) | F17 RS >= 90 DAN F23 ATR% >= 4 | H4 4xATR14 | X11 RSI14 < 50 DAN X22 hari turun dengan volum >= 1.5x | 2 | 1 | 1 | 0 | – | – | 0 | – | – |

- "Lari" = naik ≥ 5 % minggu pertama, capai ≥ 10 % sebelum henti −8 %, masih ≥ 10 % pada minggu ke-4; hanya dikira selepas 20 sesi berlalu. "Rawak" = saham layak lain pada hari yang sama dan tahap turun-naik yang sama.
- Bacaan awal tidak bermakna: perlu sekurang-kurangnya 100 belian dengan tetingkap lengkap bagi setiap setup sebelum kadar tangkap boleh dibandingkan dengan backtest (`kajian/CARIAN_SETUP.md`).
- Pegang minimum (pindaan 14 Nov 2026 (p)): tiada jualan pada hari beli; indikator keluar hanya menjual mulai buka sesi ke-4; henti rugi kekal aktif sejak sesi ke-2.
- Senarai penuh: `jejak_f/lejar.csv`. Alam: stor harga (senarai Shariah semasa).
