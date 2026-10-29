# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-28. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 6354; ada dalam lejar: 5175; tiada: 1179 {'isyarat ada, belum diproses': 527, 'tiada isyarat dalam lejar': 14, 'isyarat ada, dipegang lejar': 638}
- Posisi lejar: 13687 (C hanya 6354; lejar 2.2×)
- Harga beli berbeza > 0.5%: 0 daripada 5175
- Status keluar sama: 5174 daripada 5175; berbeza: 1

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
