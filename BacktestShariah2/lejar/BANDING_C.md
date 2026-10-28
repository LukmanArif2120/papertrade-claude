# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-27. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 5755; ada dalam lejar: 4645; tiada: 1110 {'isyarat ada, belum diproses': 543, 'tiada isyarat dalam lejar': 14, 'isyarat ada, dipegang lejar': 553}
- Posisi lejar: 12394 (C hanya 5755; lejar 2.2×)
- Harga beli berbeza > 0.5%: 0 daripada 4645
- Status keluar sama: 4644 daripada 4645; berbeza: 1

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
