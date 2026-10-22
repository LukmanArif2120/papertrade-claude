# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-21. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 3157; ada dalam lejar: 2304; tiada: 853 {'isyarat ada, belum diproses': 601, 'isyarat ada, dipegang lejar': 249, 'tiada isyarat dalam lejar': 3}
- Posisi lejar: 7179 (C hanya 3157; lejar 2.3×)
- Harga beli berbeza > 0.5%: 0 daripada 2304
- Status keluar sama: 2303 daripada 2304; berbeza: 1

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
