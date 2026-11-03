# Banding Papertrade C dengan Lejar Penuh (fasa 1)

Dijana oleh `standard/lejar.py banding`. Lejar bermula 2026-10-15; sesi terakhir 2026-11-02. Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan keutamaan 431 dalam C (lejar membeli semua isyarat).

- Posisi C (isyarat >= 2026-10-15): 8566; ada dalam lejar: 7140; tiada: 1426 {'isyarat ada, dipegang lejar': 1395, 'isyarat batal pada buka (peraturan kaedah)': 6, 'isyarat ada, belum diproses': 11, 'tiada isyarat dalam lejar': 14}
- Posisi lejar: 51225 (C hanya 8566; lejar 6.0×)
- Harga beli berbeza > 0.5%: 48 daripada 7140
- Status keluar sama: 7139 daripada 7140; berbeza: 1

## Harga beli berbeza > 0.5%

- M01 PLPC 2026-10-30: C 301.87 / lejar 300.01 (+0.62%)
- M08 INTA 2026-10-30: C 41.78 / lejar 42.03 (-0.59%)
- M20 CF 2026-10-30: C 118.55 / lejar 120.78 (-1.85%)
- M20 PAYX 2026-10-30: C 112.02 / lejar 112.71 (-0.61%)
- M25 HQY 2026-10-30: C 104.08 / lejar 102.85 (+1.20%)
- M26 CF 2026-10-30: C 118.55 / lejar 120.78 (-1.85%)
- M28 ZBRA 2026-10-30: C 366.23 / lejar 363.12 (+0.86%)
- M41 CAI 2026-10-30: C 34.76 / lejar 34.945 (-0.53%)
- M49 INTA 2026-10-30: C 41.78 / lejar 42.03 (-0.59%)
- M66 INTA 2026-10-30: C 41.78 / lejar 42.03 (-0.59%)
- M73 CRM 2026-10-30: C 231.34 / lejar 229.75 (+0.69%)
- M77 INTA 2026-10-30: C 41.78 / lejar 42.03 (-0.59%)
- M79 HOFT 2026-10-30: C 14.314 / lejar 14.4 (-0.60%)
- M80 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- M92 INTA 2026-10-30: C 41.78 / lejar 42.03 (-0.59%)
- M93 QLYS 2026-10-30: C 222.77 / lejar 224.15 (-0.62%)
- M94 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- M106 INTA 2026-10-30: C 41.78 / lejar 42.03 (-0.59%)
- M107 PPIH 2026-10-30: C 30.0 / lejar 29.54 (+1.56%)
- M118 HOFT 2026-10-30: C 14.314 / lejar 14.4 (-0.60%)
- M147 CF 2026-10-30: C 118.55 / lejar 120.78 (-1.85%)
- N50X17 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N56X17 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N50X14 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N42X36 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N09X36 CF 2026-10-30: C 118.55 / lejar 120.78 (-1.85%)
- N113X36 CF 2026-10-30: C 118.55 / lejar 120.78 (-1.85%)
- N42X16 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N42X17 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N56X36 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N113X16 CF 2026-10-30: C 118.55 / lejar 120.78 (-1.85%)
- N75X14 AUGO 2026-10-30: C 67.62 / lejar 68.005 (-0.57%)
- N24X16 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N57X16 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N42X14 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N55X13 TEAM 2026-10-30: C 190.178 / lejar 193.73 (-1.83%)
- N73X13 AUGO 2026-10-30: C 67.62 / lejar 68.005 (-0.57%)
- N75X13 AUGO 2026-10-30: C 67.62 / lejar 68.005 (-0.57%)
- N56X16 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N07X16 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N75X15 AUGO 2026-10-30: C 67.62 / lejar 68.005 (-0.57%)
- N57X36 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N06X36 PPIH 2026-10-30: C 30.0 / lejar 29.54 (+1.56%)
- N24X17 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N42X15 MPWR 2026-10-30: C 1239.66 / lejar 1231.18 (+0.69%)
- N24X36 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)
- N75X17 AUGO 2026-10-30: C 67.62 / lejar 68.005 (-0.57%)
- N07X36 LFST 2026-10-30: C 13.6 / lejar 13.5 (+0.74%)

## Status keluar berbeza

- M13 SBH 2026-10-15: C keluar 2026-10-19 / lejar keluar 2026-10-20 henti
