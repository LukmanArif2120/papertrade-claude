# Gate C: portfolio daripada kombinasi silang-keluarga

Dijana 2026-10-29 07:48 UTC oleh `REVERSE/step14_silang_portfolio.py`. Pradaftar `REVERSE/SPEC_SILANG.md` §5 Gate C.

## Keputusan akhir: **DITOLAK**

Pembinaan: `REF_jual_hari63`, 8 slot, saiz tetap — lalai TETAP kajian (`SPEC.md` §3), bukan dipilih selepas melihat hasil. 20 benih × 2020–2025, kos penuh.

**SPUS 2020–2025:** median tahunan +26.09% / MDD -10.14% · CAGR tingkap +17.95% / MDD -26.82%. Kedua-dua konvensyen diperlukan (`PEMBINAAN.md`).

| Kombinasi | Pulangan median | MDD median | CAGR median | p10 | p90 | MDD terdalam | Masuk/thn | Slot terisi | Gate C |
|---|---|---|---|---|---|---|---|---|---|
| `q5:atr_pct+q5:pecutan_hasil&sejak_earnings_le5` | +11.80% | -29.90% | +12.52% | +8.12% | +16.07% | -38.37% | 30 | 6.5 | tidak |
| `q5:julat20+q5:pecutan_hasil&sejak_earnings_le5` | +3.31% | -24.03% | +10.99% | +8.74% | +13.35% | -32.87% | 32 | 6.9 | tidak |
| `q5:j_ma200+q5:pecutan_hasil&sejak_earnings_le5` | +7.54% | -23.94% | +9.07% | +6.86% | +10.78% | -45.43% | 26 | 5.8 | tidak |
| `q5:cerun_ma50+q5:pecutan_hasil&sejak_earnings_le5` | +12.79% | -15.46% | +8.34% | +7.51% | +9.30% | -46.10% | 22 | 5.1 | tidak |
| **SPUS** | **+26.09%** | **-10.14%** | **+17.95%** | — | — | **-26.82%** | 1 | — | — |

## Kapasiti slot

Soalan (c) arahan asal: cukup untuk mengisi portfolio? Fasa 1 mendapati **kapasiti slot yang mengikat, bukan kadar menang** — rujukan pegang panjang hanya membuka 8–16 posisi setahun berbanding ~130 yang diperlukan untuk 8 slot.

- `q5:julat20+q5:pecutan_hasil&sejak_earnings_le5`: **32 masuk/tahun**, slot terisi purata **6.9 daripada 8**
- `q5:atr_pct+q5:pecutan_hasil&sejak_earnings_le5`: **30 masuk/tahun**, slot terisi purata **6.5 daripada 8**
- `q5:j_ma200+q5:pecutan_hasil&sejak_earnings_le5`: **26 masuk/tahun**, slot terisi purata **5.8 daripada 8**
- `q5:cerun_ma50+q5:pecutan_hasil&sejak_earnings_le5`: **22 masuk/tahun**, slot terisi purata **5.1 daripada 8**

## Tafsiran

**Tiada kombinasi lulus Gate C.** Maklumat silang-keluarga **WUJUD** — empat kombinasi lulus Gate A dan Gate B, jadi jangkaan priori saya dalam `SPEC_SILANG.md` §7 (DITOLAK pada Gate B) ialah **SALAH**. Tetapi ia **tidak mencukupi** untuk mengalahkan memegang SPUS.

Itu hasil yang spec §6 namakan secara khusus: "maklumat silang-keluarga WUJUD tetapi tidak mencukupi" — berbeza daripada penolakan penuh, dan mesti dinyatakan sebagai begitu.

Gagal pada: konvensyen median tahunan, konvensyen CAGR.

## Mengapa signal yang nyata tetap tidak cukup

Pulangan SETIAP PERISTIWA bagi keempat-empat kombinasi kuat, tetapi jangkaan selepas membuang 5% pemenang teratas hampir hilang:

| Kombinasi | Pulangan purata/peristiwa | Jangkaan tanpa 5% teratas |
|---|---|---|
| `q5:atr_pct+q5:pecutan_hasil&sejak_earnings_le5` | +5.90% | +1.17% |
| `q5:cerun_ma50+q5:pecutan_hasil&sejak_earnings_le5` | +4.73% | +0.80% |
| `q5:j_ma200+q5:pecutan_hasil&sejak_earnings_le5` | +4.78% | +0.58% |
| `q5:julat20+q5:pecutan_hasil&sejak_earnings_le5` | +4.91% | +0.22% |

Itu jawapannya. Dengan 8 slot dan ufuk 63 sesi, portfolio memerlukan ~32 masuk/tahun untuk kekal penuh, dan signal ini membekalkan 22–32 — jadi **kapasiti BUKAN pengikat utama di sini**, tidak seperti fasa 1. Yang mengikat ialah **bentuk taburan**: kelebihan signal hidup dalam ekor kanan yang nipis, dan 8 posisi tidak cukup untuk menangkapnya dengan boleh harap.

Itu dapatan yang sama seperti `KOLAM_EKOR.md` §2 (5% teratas = 63.7% daripada jumlah pulangan kolam), kini dilihat pada signal yang BETUL-BETUL mempunyai kelebihan. Signal yang sah tidak menyelesaikan masalah bentuk taburan; ia mewarisinya.

## Mengapa kesemua empat berkongsi induk SEC yang sama

Kesemua empat kombinasi yang lulus Gate A + B ialah konteks harga × `q5:pecutan_hasil&sejak_earnings_le5` — iaitu **PEAD**, satu-satunya signal yang bertahan §5.3 fasa 2. Tiada kombinasi dengan `q5:sue`, `q5:tumbuh_hasil` atau `q5:pecutan_hasil` tanpa tingkap earnings yang lulus.

Maksudnya maklumat silang itu **bukan sifat umum "fundamental × harga"**. Ia khusus: kesan PEAD menjadi lebih kuat apabila disaring oleh konteks harga (cerun MA50 tinggi, jauh di atas MA200, julat/ATR mengembang). Itu konsisten dengan kesusasteraan PEAD — hanyutan lebih kuat apabila pasaran sedang memberi perhatian kepada saham itu.

## Had

- Alam Release `autotune-data-a02`, **bukan** ditapis Syariah; SPUS ditapis. Tapisan Syariah membuang semua kewangan, jadi perbandingan tidak setara pada paksi itu.
- Satu rujukan keluar dan satu saiz sahaja. Spec §5 Gate C tidak menamakannya; `REF_jual_hari63` + saiz tetap diguna sebagai lalai kajian. Menguji beberapa rujukan dan melaporkan yang terbaik akan menjadi pemilihan selepas fakta.
- Tingkap 2020–2025 sahaja (6 tahun) kerana SPUS mula Dis 2019. Itu tempoh yang pendek dan ia merangkumi satu pasaran menaik yang kuat.
- Pulangan tahunan dikira setiap tahun secara berasingan (mesin fasa 1/2), kemudian dikompaun untuk CAGR. Posisi tidak dibawa merentas sempadan tahun.
- MDD SPUS daripada tutup **bulanan**, jadi lebih cetek daripada MDD harian yang benar. Itu menjadikan syarat MDD **lebih sukar** bagi sistem, bukan lebih mudah.

**Ia tidak mencapai +10%/bulan.** Lihat `SASARAN.md`.
