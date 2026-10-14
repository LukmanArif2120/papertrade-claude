# Antara muka modul kaedah (scan harian Papertrade)

Setiap kaedah = satu fail `kaedah/Mxx.py`. Fail ini diimport oleh `scanner.py` (scan harian) dan `uji_kaedah.py` (semakan lawan registry).

```python
from enjin import rsi, atr          # boleh guna; jangan ubah enjin.py
import pandas as pd, numpy as np

ID      = 'M54'
NAMA    = 'IBD Power Trend'
VARIAN  = 'V4 V1 sig=PT benar & tutup>high 20 hari'   # SALIN TEPAT rentetan lajur `varian` dalam registry/Mxx.csv
TMAX    = None        # had hari pegangan (sama seperti backtest) atau None
WARM    = 200         # pemanasan (bar) seperti backtest
ADA_HENTI = True
SILANG  = False       # True jika isyarat bergantung pada saham lain (persentil RS, rotasi); sedia() tetap terima semua saham
PERLU_BAR = 260       # bilangan bar harian minimum yang diperlukan untuk isyarat hari terakhir sah

def sedia(fr, idx):
    """fr: dict ticker -> DataFrame (index DatetimeIndex; lajur open high low close volume turnover).
       idx: dict 'SPY','QQQ' -> DataFrame sama format.
       Isi lajur sig, stop, tgt, exitc, rank DALAM SETIAP g (tulis semula semua lajur; ubah di tempat).
       Mesti tanpa pandang ke hadapan: nilai hari i hanya guna data <= i."""

def hampir(g, idx):
    """Dipanggil SELEPAS sedia(), untuk BAR TERAKHIR g sahaja.
       Pulangkan None jika tiada persediaan.
       Jika persediaan sedang terbentuk tetapi sig bar terakhir = False, pulangkan dict:
         {'sebab': 'ayat BM ringkas: kenapa layak dipantau (syarat mana sudah dipenuhi)',
          'syarat_beli': 'ayat BM: apa yang mesti berlaku untuk isyarat beli, dengan paras harga jika ada (cth. tutup > 123.45)',
          'skor': nombor 0-1, makin dekat dengan isyarat makin tinggi}
       Takrif 'hampir' mesti diambil daripada spec (syarat persediaan dipenuhi, pencetus belum)."""
```

Peraturan:
- Logik isyarat MESTI ikut Kad Spesifikasi Mesin (spec/Mxx_*.md atau `## SPEC Mxx` dalam KOMPILASI_KAEDAH_M01-M31.md) dan varian yang dipilih, sama seperti backtest /step2 yang menghasilkan registry/Mxx.csv.
- Varian dipilih: dalam registry/Mxx.csv, baris `set==431`; pilih skor tertinggi antara keputusan bukan DITOLAK; jika semua DITOLAK, CAGR tertinggi.
- Penapis pasaran (SPY/QQQ) diambil daripada idx dan di-reindex ke tarikh saham (ffill).
- Jangan reka. Andaian tambahan ditulis sebagai komen `# Andaian saya:`.
