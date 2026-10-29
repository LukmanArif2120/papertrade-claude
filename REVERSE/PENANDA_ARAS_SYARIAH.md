# Penanda aras PATUH SYARIAH: pembetulan kesilapan asas kajian ini

Dijana 2026-10-29 02:26 UTC oleh `REVERSE/penanda_aras_syariah.py`.

## Kesilapan

Projek ini bernama **Backtest Shariah**, tetapi setiap perbandingan dalam kajian REVERSE — termasuk `KEPUTUSAN_FASA1.md`, `KEPUTUSAN_FASA2_SEC.md`, `SASARAN.md` dan `KOS_DRAG.md` — menggunakan **SPY**, yang **bukan patuh Syariah**. Sistem diukur terhadap sesuatu yang pengguna mungkin tidak boleh beli, dan penanda aras yang betul tidak pernah dikira sekali pun.

Repo sendiri sudah menapis Syariah melalui **SPUS** (SP Funds S&P 500 Sharia Industry Exclusions ETF): `data/skrin/etf_shariah.csv` (326 ticker) dan `semak_shariah.csv`. Jadi alternatif pasif yang sah sudah ada dalam repo sejak awal.

## Apa yang SPUS beri

| Tahun | SPUS | SPY | SPUS bulanan | SPY bulanan |
|---|---|---|---|---|
| 2020 | 25.68% | 18.33% | 3.35% | 2.74% |
| 2021 | 35.81% | 28.73% | 3.45% | 2.61% |
| 2022 | -22.76% | -18.18% | -5.01% | -3.52% |
| 2023 | 34.24% | 26.18% | 2.99% | 2.44% |
| 2024 | 26.49% | 24.89% | 2.19% | 2.22% |
| 2025 | 19.77% | 17.72% | 1.71% | 2.18% |

Median: **SPUS 26.09%/tahun** lawan SPY 21.61%/tahun. SPUS **mengalahkan** SPY, kerana membuang kewangan dan syarikat berleveraj tinggi memberatkannya ke arah teknologi dalam tempoh ini.

Maka penanda aras yang betul **lebih tinggi** daripada yang saya guna sepanjang kajian, bukan lebih rendah. Setiap kesimpulan sebelum ini terlalu memihak kepada sistem.

## Perbandingan yang menentukan, 2020–2025

| | Pulangan/tahun | MDD | Median bulanan | Dagangan/tahun |
|---|---|---|---|---|
| **SPUS (patuh Syariah)** | **26.09%** | -10.14% | **2.59%** | **1** |
| SPY | 21.61% | -7.96% | 2.33% | 1 |
| Sistem: REF_chandelier_4atr | -0.56% | -22.32% | -0.53% | 42 |
| Sistem: REF_jual_hari63 | 18.12% | -28.42% | 0.33% | 40 |
| Sistem: REF_pegang_252 | 13.75% | -24.46% | 0.73% | 8 |

Sistem terbaik (`REF_jual_hari63`) memberi 18.12%/tahun — **-7.96 mata peratus** lawan SPUS, dengan MDD 2.8 kali lebih dalam dan median bulanan 0.33% lawan 2.59%.

MDD penanda aras dikira daripada tutup **bulanan**, jadi ia memandang **rendah** drawdown harian sebenar. Itu memihak kepada penanda aras — maka jurang di atas adalah **konservatif** terhadap SPUS, dan jurang sebenar pada data harian akan lebih kecil pada paksi MDD sahaja, bukan pada pulangan.

## Had yang diakui

- SPUS mula didagangkan **Dis 2019**, jadi hanya 6 tahun penuh. Tempoh itu ialah prestasi teknologi yang luar biasa kuat. **26%/tahun bukan jangkaan ke hadapan**, dan sesiapa yang menganggapnya begitu akan kecewa.
- Penapisan Syariah SPUS ialah satu standard tertentu (S&P Shariah). Sama ada ia memenuhi standard yang pengguna pakai, dan bagaimana cukai serta akses broker mempengaruhinya, **bukan sesuatu yang kajian ini boleh jawab**.
- Ini pengukuran sistem pengguna sendiri terhadap penanda aras, **bukan nasihat pelaburan**. Saya tidak bertauliah memberi nasihat pelaburan peribadi.
