# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-10-20. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 2577; ada dalam lejar: 1767; tiada: 810 {'isyarat ada, dipegang lejar': 184, 'tiada isyarat dalam lejar': 9, 'isyarat ada, belum diproses': 617}
- Posisi lejar: 5789 (C hanya 2577; lejar 2.2×)
- Harga beli berbeza > 0.5%: 52 daripada 1767
- Status keluar sama: 1764 daripada 1767; berbeza: 3

## Harga beli berbeza > 0.5%

- M01 ODC 2026-10-19: C 70.64 / lejar 70.0 (+0.91%)
- M02 NEM 2026-10-19: C 116.04 / lejar 115.42 (+0.54%)
- M11 KN 2026-10-19: C 35.04 / lejar 34.1 (+2.76%)
- M14 BDX 2026-10-19: C 192.78 / lejar 191.5 (+0.67%)
- M15 DLB 2026-10-19: C 61.06 / lejar 61.58 (-0.84%)
- M15 CVSA 2026-10-19: C 129.43 / lejar 130.68 (-0.96%)
- M19 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M20 CVSA 2026-10-19: C 129.43 / lejar 130.68 (-0.96%)
- M25 DLB 2026-10-19: C 61.06 / lejar 61.58 (-0.84%)
- M29 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M31 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M31 DLB 2026-10-19: C 61.06 / lejar 61.58 (-0.84%)
- M33 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M33 LPX 2026-10-19: C 71.18 / lejar 71.72 (-0.75%)
- M33 RS 2026-10-19: C 412.31 / lejar 409.46 (+0.70%)
- M33 HXL 2026-10-19: C 91.23 / lejar 91.79 (-0.61%)
- M34 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M35 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M55 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M66 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M73 BDX 2026-10-19: C 192.78 / lejar 191.5 (+0.67%)
- M73 HPE 2026-10-19: C 54.3 / lejar 54.71 (-0.75%)
- M76 TDW 2026-10-19: C 81.46 / lejar 82.07 (-0.74%)
- M77 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M79 AS 2026-10-19: C 30.5 / lejar 30.73 (-0.75%)
- M80 AS 2026-10-19: C 30.5 / lejar 30.73 (-0.75%)
- M82 RYZ 2026-10-19: C 27.66 / lejar 27.14 (+1.92%)
- M89 NEM 2026-10-19: C 116.04 / lejar 115.42 (+0.54%)
- M89 M 2026-10-19: C 23.84 / lejar 23.67 (+0.72%)
- M90 MATX 2026-10-19: C 232.02 / lejar 235.87 (-1.63%)
- M92 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)
- M92 CVSA 2026-10-19: C 129.43 / lejar 130.68 (-0.96%)
- M99 OII 2026-10-19: C 44.73 / lejar 43.89 (+1.91%)
- M105 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M105 LPX 2026-10-19: C 71.18 / lejar 71.72 (-0.75%)
- M105 RS 2026-10-19: C 412.31 / lejar 409.46 (+0.70%)
- M111 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M111 HXL 2026-10-19: C 91.23 / lejar 91.79 (-0.61%)
- M122 NEM 2026-10-19: C 116.04 / lejar 115.42 (+0.54%)
- M124 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M124 HXL 2026-10-19: C 91.23 / lejar 91.79 (-0.61%)
- M128 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M128 SDRL 2026-10-19: C 48.24 / lejar 49.03 (-1.61%)
- M131 RS 2026-10-19: C 412.31 / lejar 409.46 (+0.70%)
- M133 DLB 2026-10-19: C 61.06 / lejar 61.58 (-0.84%)
- M136 CVSA 2026-10-19: C 129.43 / lejar 130.68 (-0.96%)
- M136 GRDN 2026-10-19: C 40.39 / lejar 40.15 (+0.60%)
- M137 MUR 2026-10-19: C 43.1 / lejar 42.86 (+0.56%)
- M145 MUR 2026-10-19: C 43.1 / lejar 42.86 (+0.56%)
- M151 VAL 2026-10-19: C 90.035 / lejar 90.91 (-0.96%)
- M151 TDC 2026-10-19: C 31.46 / lejar 31.645 (-0.58%)
- M154 FET 2026-10-19: C 85.39 / lejar 84.81 (+0.68%)

## Status keluar berbeza

- M76 GEF 2026-10-15: C keluar 2026-10-20 / lejar terbuka
- M81 DELL 2026-10-15: C keluar 2026-10-20 / lejar terbuka
- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
