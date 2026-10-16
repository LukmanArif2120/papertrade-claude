# Pengesahan enjin laju lawan enjin v1.2

Kaedah disemak: 4. Sama bait demi bait (semua gabungan): **4/4**. Jumlah gabungan diuji: 16 (tetapan asal + 3 rawak setiap kaedah).

Setiap gabungan: `trades()` dibanding semua lajur (ticker, sig, ent, ex, ret, days, why, rank, mfe; float tepat, NaN = NaN); `portfolio()` dibanding atas data penuh dan tetingkap 2020–2022 selepas `potong()`.

| Kaedah | Gabungan | n | trades | portfolio penuh | portfolio tetingkap |
|---|---|---|---|---|---|
| M13 | ASAL/ASAL/0 | 21919 | sama | sama | sama |
| M13 | PCT15/CHAN2/21 | 25880 | sama | sama | sama |
| M13 | ATR4/SMA50/21 | 25756 | sama | sama | sama |
| M13 | LOW10/SMA50/21 | 25916 | sama | sama | sama |
| M22 | ASAL/ASAL/0 | 37 | sama | sama | sama |
| M22 | ASAL/SMA20/21 | 37 | sama | sama | sama |
| M22 | PCT6/ASAL/21 | 37 | sama | sama | sama |
| M22 | LOW1/EMA21/42 | 37 | sama | sama | sama |
| M37 | ASAL/ASAL/0 | 532 | sama | sama | sama |
| M37 | ATR4/EMA21/0 | 559 | sama | sama | sama |
| M37 | ATR4/TIADA/10 | 568 | sama | sama | sama |
| M37 | ATR4/CHAN3/63 | 551 | sama | sama | sama |
| M96 | ASAL/ASAL/0 | 294 | sama | sama | sama |
| M96 | ATR1.5/CHAN3/63 | 494 | sama | sama | sama |
| M96 | ASAL/SMA50/10 | 648 | sama | sama | sama |
| M96 | LOW10/CHAN3/10 | 648 | sama | sama | sama |
