# Papertrade harian automatik (mula 8 Okt 2026)

## Tugasan berjadual (auto, tanpa kelulusan; paper trade sahaja)
| Tugasan | Masa | Kerja |
|---|---|---|
| Scan malam Papertrade Shariah | 8:05 malam MYT, Isnin–Jumaat (diawalkan supaya siap sebelum beli) | Kemas kini harga, scan 87 kaedah M, bina senarai beli + watchlist |
| Beli Papertrade Shariah | 9:35 pagi waktu New York | Beli 1 unit setiap saham dalam senarai (akaun simulasi 4135388) |
| Scan tutup Papertrade Shariah | 4:30 petang waktu New York | Harga tutup, kemas kini kedudukan, keluar ikut peraturan, watchlist, senarai beli esok |
Setiap tugasan semak kalendar NYSE dahulu; cuti = berhenti.

## Peraturan beli (100% entry)
- Beli HANYA jika isyarat beli kaedah benar pada tutup sesi (semua syarat entry varian dipenuhi). Tiada belian "hampir".
- 87 kaedah M (varian terbaik set 431 dalam registry: skor tertinggi bukan DITOLAK, jika tiada CAGR tertinggi). Indikator I01–I32 tidak digunakan.
- Pasaran: saham AS bertanda Islamic dalam Moomoo, harga > USD10, float market cap > USD1 juta. 431 diutamakan, kemudian ikut kunci `rank` kaedah.
- 1 unit setiap belian; satu saham hanya 1 unit dalam akaun (kaedah kedua = "dikongsi", direkod pada harga buka tanpa unit baharu).
- Maksimum 10 saham setiap kaedah; saham tidak dijual. Langkau beli jika harga buka ≤ henti.
- Pembelian wang sebenar: MESTI minta kelulusan pengguna.

## Watchlist (2 jenis)
1. **Hampir isyarat (90–100%)**: SEMUA syarat entry selain pencetus sudah dipenuhi hari ini (syarat_dipenuhi = N−1/N), dan pencetus dalam ≤ 2% (paras harga esok dinyatakan). Pencetus kalendar: rotasi dalam ≤ 3 hari dagangan. Corak satu hari (lilin) tanpa jarak boleh masuk jika syarat lain lengkap. Maks 5 setiap kaedah (431 dahulu, kemudian skor terdekat). Dibuang selepas 10 hari tanpa isyarat. (Dikemas kini 8 Okt 2026.)
2. **Slot penuh**: kaedah sudah 10/10; isyarat beli baharu direkod seolah-olah dibeli pada buka esok (maks 5 terbaik ikut rank sehari, 50 terkini).
- Keluar ikut peraturan backtest dikira tetapi saham tetap dipegang. Kaedah bergantung-dagangan (M02, M18, M19, M24, M40, M45, M47, M56, M76, M78, M81, M82, M94, M96, M100) = anggaran.

## Teknikal
- Modul isyarat kaedah/Mxx.py ditulis semula daripada spec dan disahkan lawan registry (83 tepat; M40, M45, M81, M107 dalam toleransi; M24 tepat dengan 2 slot).
- Kod, stor harga (harga_A/B/idx, univ) disimpan sebagai aset dalam dashboard; status di db `harian/status`; data larian di `larian/<run>/kumpulan` dan `larian/<run>/meta`.
- Had: kline Moomoo ~4 panggilan seminit, jadi harga harian diambil melalui screener; jika satu hari terlepas, jurang diisi perlahan (24 saham setiap larian).
