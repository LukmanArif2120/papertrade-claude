# KOS sebagai lever: berapa banyak pulangan dimakan oleh kos dagangan

Dijana 2026-10-29 01:47 UTC oleh `REVERSE/kos_drag.py`.

`REVERSE/SASARAN.md` memberi tiga pilihan dan dua bergantung pada selera risiko pengguna. Yang ketiga tidak: **apa-apa sasaran yang dipilih, wang yang tinggal lebih banyak kalau kos lebih rendah.** Repo ini mengukur signal, saiz dan fundamental, tetapi tidak pernah mengukur kos itu sendiri. Ini mengukurnya.

Kaedah: portfolio §5.4 yang **sama** dijalankan dua kali atas **semua** peristiwa sah 2012–2025 — sekali dengan model kos penuh (komisen 0.1% setiap sisi + slippage bertingkat 0.05/0.10/0.25%), sekali dengan kos **sifar**. Populasi penuh dan bukan signal terpilih, kerana drag kos ialah sifat dagangan dan bukan sifat signal.

| Keluar | Pulangan (kos penuh) | Pulangan (kos sifar) | Drag | Dagangan/tahun |
|---|---|---|---|---|
| REF_pegang_252 | 15.93% | 16.31% | **0.37 mata** | 8 |
| REF_chandelier_4atr | 11.42% | 13.81% | **2.39 mata** | 40 |
| REF_jual_hari63 | 19.31% | 21.83% | **2.51 mata** | 40 |

Nilai ialah **median merentas 14 tahun**. "Drag" = berapa mata peratus setahun yang hilang kepada komisen dan slippage.

Drag terbesar: **REF_jual_hari63, 2.51 mata peratus setahun**.

## Apa nombor ini sebenarnya berkata

**Saya menulis bahagian ini selepas melihat nombor, dan ia bertentangan dengan apa yang saya jangka.** Saya memilih mengukur kos kerana ia lever yang pasti dan tidak bergantung pada sasaran. Ukurannya menunjukkan lever itu lebih kecil daripada rupanya, dan sebahagiannya mengalahkan diri sendiri.

Mengurangkan pusing ganti **memang** memotong kos: `REF_pegang_252` membayar hanya 0.37 mata drag dengan 8 dagangan setahun, berbanding 2.51 mata dengan 40 dagangan.

Tetapi pulangan **bersihnya** lebih rendah: 15.93% lawan 19.31%. Menjimatkan 2.14 mata kos mengorbankan 3.38 mata pulangan. **Pusing ganti yang tinggi itu membayar kosnya sendiri.**

Drag terbesar, 2.51 mata, ialah 13% daripada pulangan konfigurasi itu. Itu wang sebenar dan patut dikurangkan di tempat yang boleh — komisen ialah terma broker, bukan sifat pasaran, dan slippage 0.25% pada nama < USD10 juta lawan 0.05% pada ≥ USD50 juta ialah lima kali bezanya, ditapis sebelum masuk tanpa menyentuh signal. Tetapi ia **tidak** mengubah gambaran strategik.

Bandingan yang menentukan, kos penuh, median 14 tahun:

| | Pulangan | MDD | Median bulanan | Dagangan/tahun |
|---|---|---|---|---|
| REF_pegang_252 | 15.93% | -16.53% | 1.00% | 8 |
| REF_chandelier_4atr | 11.42% | -15.12% | 0.75% | 40 |
| REF_jual_hari63 | 19.31% | -16.29% | 1.16% | 40 |
| **SPY beli-dan-pegang** | **17.62%** | **−9.44%** | **1.82%** | **1** |

Konfigurasi terbaik mengalahkan SPY pada pulangan (19.31% lawan 17.62%) tetapi dengan MDD 1.7 kali lebih dalam (-16.29% lawan −9.44%) dan median bulanan lebih rendah (1.16% lawan 1.82%). Walaupun kos **dihapuskan sepenuhnya** — mustahil — ia menjadi 21.83% pada MDD yang sama.

Maka kesimpulannya: **kos bukan masalahnya.** Ia 13% daripada pulangan dan patut dikurangkan, tetapi menghapuskannya sepenuhnya pun tidak membawa sistem ini kepada sasaran +10%/bulan, dan tidak menjadikan drawdownnya setanding SPY.

Saya mengukurnya kerana ia satu-satunya lever yang tinggal yang tidak memerlukan keputusan anda. Hasilnya menutup lever itu juga. Yang tinggal sekarang benar-benar hanya keputusan sasaran, dan ia milik anda.
