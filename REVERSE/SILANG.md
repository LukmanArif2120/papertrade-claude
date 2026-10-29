# Kombinasi silang-keluarga: konteks harga × fundamental SEC

Dijana 2026-10-29 07:47 UTC oleh `REVERSE/step13_silang.py`. Pradaftar: `REVERSE/SPEC_SILANG.md` (dikomit sebelum larian ini). **Ujian signal terakhir.**

## Keputusan: **LULUS GATE A + B — Gate C diperlukan**

48 kombinasi silang diuji (12 konteks harga × 4 syarat SEC). **Gate A lulus: 4. Gate A + B lulus: 4.**

## Gate A — statistik (sama seperti fasa 2 §5.3)

`n` ≥ 200 · konsisten ≥ 71% daripada ≥ 10 tahun dinilai · BH-FDR q ≤ 0.01 merentas 48 · jangkaan > 0 selepas buang 5% teratas · dua bootstrap blok positif.

- lulus `FDR`: **26** daripada 48
- lulus `n`: **48** daripada 48
- lulus `konsisten`: **10** daripada 48
- lulus `tanpa5`: **11** daripada 48
- lulus `blok`: **37** daripada 48

## Gate B — superaditif (soalan sebenarnya)

`lift(silang)` mesti melebihi **kedua-dua** induknya. Tanpa gate ini satu kombinasi boleh lulus Gate A hanya kerana induk yang lebih kuat menembusi — dan itu sudah diukur oleh fasa 1 dan 2.

**19 daripada 48 kombinasi superaditif** (40%).

Beza `lift(silang) − lift(induk terkuat)`: median **-0.139**, min -1.205, maks +2.237. Nilai negatif = **subaditif**: mensyaratkan dua keadaan memberi lift LEBIH RENDAH daripada syarat terkuat sendiri.

## 10 kombinasi silang dengan lift tertinggi

| Kombinasi | n | lift | lift induk maks | Beza | Gate A | Gate B |
|---|---|---|---|---|---|---|
| `q5:cerun_ma50+q5:tumbuh_hasil` | 6,138 | 5.584 | 3.347 | +2.237 | tidak | ya |
| `q5:cerun_ma50+q5:pecutan_hasil&sejak_earnings_le5` | 541 | 4.651 | 3.347 | +1.304 | ya | ya |
| `q5:cerun_ma50+q5:pecutan_hasil` | 6,104 | 4.102 | 3.347 | +0.755 | tidak | ya |
| `q5:j_ma200+q5:tumbuh_hasil` | 7,042 | 3.779 | 2.830 | +0.949 | tidak | ya |
| `q5:j_ma200+q5:pecutan_hasil` | 7,122 | 3.161 | 2.830 | +0.331 | tidak | ya |
| `q5:cerun_ma50+q5:sue` | 5,799 | 2.906 | 3.347 | -0.441 | tidak | tidak |
| `q5:j_ma200+q5:pecutan_hasil&sejak_earnings_le5` | 751 | 2.898 | 2.830 | +0.068 | ya | ya |
| `q5:atr_pct+q5:pecutan_hasil` | 5,968 | 2.597 | 2.217 | +0.380 | tidak | ya |
| `q5:j_ma200+q5:sue` | 7,002 | 2.506 | 2.830 | -0.324 | tidak | tidak |
| `q5:julat20+q5:pecutan_hasil&sejak_earnings_le5` | 731 | 2.361 | 1.852 | +0.509 | ya | ya |

## Induk, sebagai rujukan

| Syarat | Jenis | n | lift |
|---|---|---|---|
| `q5:cerun_ma50` | harga | 32,241 | 3.347 |
| `q5:j_ma200` | harga | 32,241 | 2.830 |
| `q5:atr_pct` | harga | 32,241 | 2.217 |
| `q5:julat20` | harga | 32,241 | 1.852 |
| `q5:bb_lebar` | harga | 32,241 | 1.692 |
| `q5:tumbuh_hasil` | sec | 23,428 | 1.356 |
| `q5:pecutan_hasil&sejak_earnings_le5` | sec | 2,367 | 1.330 |
| `q5:pecutan_hasil` | sec | 23,051 | 1.243 |
| `q1:j_52w_tinggi` | harga | 32,048 | 1.183 |
| `q5:sue` | sec | 25,984 | 0.917 |
| `q1:j_ma200` | harga | 32,241 | 0.836 |
| `q1:cerun_ma50` | harga | 32,241 | 0.819 |
| `q5:j_52w_tinggi` | harga | 32,048 | 0.593 |
| `q1:bb_lebar` | harga | 32,241 | 0.266 |
| `q1:julat20` | harga | 32,241 | 0.224 |
| `q1:atr_pct` | harga | 32,241 | 0.156 |

## Tafsiran

**4 kombinasi lulus Gate A dan Gate B.** Jangkaan priori saya dalam spec §7 ialah DITOLAK pada Gate B, dan ia **SALAH**. Maklumat silang-keluarga wujud: kombinasi ini membawa lift yang melebihi kedua-dua induknya dan bertahan setiap kawalan kebetulan.

- `q5:atr_pct+q5:pecutan_hasil&sejak_earnings_le5`: n 728, lift 2.349 lawan induk terkuat 2.217, p 0.0010, konsisten 9/11 tahun
- `q5:julat20+q5:pecutan_hasil&sejak_earnings_le5`: n 731, lift 2.361 lawan induk terkuat 1.852, p 0.0010, konsisten 9/12 tahun
- `q5:cerun_ma50+q5:pecutan_hasil&sejak_earnings_le5`: n 541, lift 4.651 lawan induk terkuat 3.347, p 0.0010, konsisten 9/11 tahun
- `q5:j_ma200+q5:pecutan_hasil&sejak_earnings_le5`: n 751, lift 2.898 lawan induk terkuat 2.830, p 0.0010, konsisten 11/12 tahun

**Gate C belum dinilai dan ia menentukan.** Spec §6: DITERIMA hanya jika portfolio median 20 benih mengalahkan SPUS pada pulangan DAN MDD. Fasa 2 menunjukkan satu signal boleh bertahan setiap ujian statistik dan tetap gagal di peringkat portfolio.

Dapatan struktur: beza lift median **-0.139** — interaksi di sini **subaditif secara majoriti** (29 daripada 48). Mensyaratkan dua keadaan mengecilkan `n` sementara keadaan itu sendiri berkorelasi, jadi lift biasanya jatuh di bawah syarat terkuat.

**Rujukan antara dua kenyataan di atas:** sebab 4 dalam spec §7 betul sebagai **kecenderungan** — majoriti kombinasi memang subaditif. Ia salah sebagai **dakwaan menyeluruh**: 19 daripada 48 superaditif, dan 4 daripadanya juga bertahan setiap kawalan kebetulan. Saya menggunakan kecenderungan itu untuk meramal tiada pengecualian, dan itu kesilapan penaakulan, bukan kesilapan ukuran.

## Had

- Alam Release `autotune-data-a02`, **bukan** ditapis Syariah; SPUS ditapis.
- Lajur harga diambil daripada cache `signals_*.parquet` fasa 1 (dikira step1 tanpa pandang hadapan), jadi ia tepat lajur yang sama yang fasa 1 nilai.
- Sempadan kuintil harga dibekukan pada larian pertama; ia **tidak** ditala.
- Grid 48 ditetapkan dalam spec §3 sebelum larian dan tidak dilebarkan.
- Konteks harga terbaik fasa 1 ialah konteks pengembangan kemeruapan, iaitu kohort yang paling tercemar oleh ketiadaan saham delist dalam stor. Bias itu **memihak** kepada kombinasi, bukan terhadapnya.

**Ia tidak mencapai +10%/bulan.** Lihat `SASARAN.md`.
