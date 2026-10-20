# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-19. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 1881; ada dalam lejar: 1345; tiada: 536 {'isyarat ada, dipegang lejar': 104, 'isyarat ada, belum diproses': 427, 'tiada isyarat dalam lejar': 5}
- Posisi lejar: 4828 (C hanya 1881; lejar 2.6×)
- Harga beli berbeza > 0.5%: 0 daripada 1345
- Status keluar sama: 1343 daripada 1345; berbeza: 2

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar terbuka
- M18 ADI 2026-10-15: C keluar 2026-10-19 / lejar terbuka
