# Ujian plasebo gate kemahiran (G3 lift masuk, NEGATIF)

Dijana 2026-11-07 12:26 UTC oleh `standard/plasebo_gate.py`. Panel A02 2010–2026, ufuk 10 sesi, tingkap 60 hari beli, 15 pilihan sehari, 3 ulangan setiap plasebo. Fungsi SE = fungsi produksi `lift_kaedah`.

**Reka bentuk BAHARU LULUS** peraturan tetap (kadar lulus palsu ≤ 5% pada ketiga-tiga plasebo).

| Reka bentuk | Plasebo | Tingkap | Kadar lulus palsu | SD lift sebenar ÷ purata SE |
|---|---|---|---|---|
| LAMA: asas hari, kluster hari beli | bebas | 207 | **5.3%** | 1.01 |
| asas hari, kluster minggu | bebas | 207 | **5.8%** | 1.02 |
| asas hari x ATR, kluster saham | bebas | 207 | **3.4%** | 0.96 |
| BAHARU: asas hari x ATR, dua hala saham+minggu | bebas | 207 | **1.9%** | 0.90 |
| LAMA: asas hari, kluster hari beli | lekit | 207 | **45.4%** | 2.48 |
| asas hari, kluster minggu | lekit | 207 | **15.9%** | 1.45 |
| asas hari x ATR, kluster saham | lekit | 207 | **7.2%** | 1.06 |
| BAHARU: asas hari x ATR, dua hala saham+minggu | lekit | 207 | **3.4%** | 1.01 |
| LAMA: asas hari, kluster hari beli | condong | 207 | **28.5%** | 2.32 |
| asas hari, kluster minggu | condong | 207 | **15.9%** | 1.72 |
| asas hari x ATR, kluster saham | condong | 207 | **3.4%** | 0.89 |
| BAHARU: asas hari x ATR, dua hala saham+minggu | condong | 207 | **1.9%** | 0.85 |

Kalibrasi > 1 bermaksud SE terlalu kecil (ujian terlalu mudah lulus); < 1 bermaksud konservatif.

Bacaan: kluster ikut hari beli (reka bentuk lama) betul HANYA bagi pilihan bebas. Kaedah sebenar sering membeli saham sama berulang kali atau condong kepada saham meruap, dan di situ ia meluluskan plasebo berkali ganda melebihi 5%. Padanan tercile ATR membuang pendedahan turun-naik; kluster dua hala (saham, minggu) menyerap ulangan saham dan pergerakan bersama dalam minggu yang sama.
