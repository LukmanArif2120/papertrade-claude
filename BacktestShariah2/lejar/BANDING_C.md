# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-21. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 2496; ada dalam lejar: 2304; tiada: 192 {'isyarat ada, belum diproses': 11, 'isyarat ada, dipegang lejar': 179, 'tiada isyarat dalam lejar': 2}
- Posisi lejar: 7179 (C hanya 2496; lejar 2.9×)
- Harga beli berbeza > 0.5%: 0 daripada 2304
- Status keluar sama: 2301 daripada 2304; berbeza: 3

## Status keluar berbeza

- M82 APA 2026-10-15: C keluar 2026-10-21 / lejar terbuka
- M82 BIIB 2026-10-15: C keluar 2026-10-21 / lejar terbuka
- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
