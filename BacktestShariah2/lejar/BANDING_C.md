# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-22. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 3143; ada dalam lejar: 2881; tiada: 262 {'isyarat ada, belum diproses': 11, 'isyarat ada, dipegang lejar': 249, 'tiada isyarat dalam lejar': 2}
- Posisi lejar: 8528 (C hanya 3143; lejar 2.7×)
- Harga beli berbeza > 0.5%: 0 daripada 2881
- Status keluar sama: 2880 daripada 2881; berbeza: 1

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
