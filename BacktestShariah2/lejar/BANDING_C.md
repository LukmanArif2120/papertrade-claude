# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-23. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 3903; ada dalam lejar: 3552; tiada: 351 {'isyarat ada, belum diproses': 11, 'isyarat ada, dipegang lejar': 335, 'tiada isyarat dalam lejar': 5}
- Posisi lejar: 10268 (C hanya 3903; lejar 2.6×)
- Harga beli berbeza > 0.5%: 0 daripada 3552
- Status keluar sama: 3551 daripada 3552; berbeza: 1

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
