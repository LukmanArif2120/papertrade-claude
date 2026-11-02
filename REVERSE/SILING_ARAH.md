# SILING ramalan ARAH 5 hari — diukur, bukan dianggar

Dijalankan 1 Nov 2026. Skrip `REVERSE/step23_siling_arah.py`, dikomit (`2f61cb6`) **sebelum**
keputusan dilihat. Alam A02, bar cair `nilai20 ≥ USD100,000`. LATIH 2012–2019 (4,174,173 bar),
TAHAN 2020–2025 (4,408,173 bar). 21 peramal daripada panel `step22_ekor.py`. Penggalak kecerunan
(LightGBM, 400 pokok). **Tiada penalaan pada TAHAN.**

Soalan pengguna: ramal setiap hari selepas tutup, ufuk 5 hari, kebarangkalian naik atau turun,
dan tala setiap hari sehingga hampir 100% tepat.

---

## 1. Kadar asas — tanda aras sebenar

LATIH naik **52.70%**; TAHAN naik **50.50%**. Maka "sentiasa kata naik" sudah memberi **50.50%**
tepat pada TAHAN, dan apa-apa model mesti dibanding dengan itu, bukan dengan 50%.

## 2. Siling ketepatan

| | AUC | Tepat |
|---|---|---|
| LATIH (dilihat model) | 0.6015 | **57.04%** |
| TAHAN (tidak pernah dilihat) | 0.5199 | **51.55%** |
| Asas TAHAN (sentiasa naik) | — | 50.50% |

**Jurang 57.04% → 51.55% ialah perangkap penalaan, dibuat kelihatan.** Menala memberi 57% pada
data yang model sudah lihat dan membeli **1.05 mata** pada data yang ia belum lihat. Menala setiap
hari pada keputusan terkini menjadikan jurang itu lebih besar, bukan lebih kecil.

Brier TAHAN **0.25036** lawan Brier asas **0.25046** — penambahbaikan 0.0001, iaitu tiada.

Ketepatan pada kuantil paling yakin: 1% teratas **53.66%**, 5% 53.09%, 10% 52.81%, 25% 52.39%.
Jadi siling ketepatan ialah kira-kira **53.7%**, bukan 100%, bukan 90%, bukan 70%.

## 3. Kalibrasi — model memang tahu sesuatu

| Model kata | Sebenar berlaku | n |
|---|---|---|
| 0–40% | 42.07% | 69,208 |
| 40–45% | 46.01% | 243,478 |
| 45–47.5% | 48.37% | 347,980 |
| 47.5–50% | 49.67% | 693,602 |
| 50–52.5% | 50.64% | 1,065,296 |
| 52.5–55% | 51.43% | 1,052,496 |
| 55–60% | 52.40% | 856,745 |
| 60%+ | 53.49% | 79,368 |

Monotonik sempurna merentas lapan baldi. Sebaran terealisasi **11.4 mata** (42.07% → 53.49%).
Model ini **terkalibrasi dengan baik dan tersusun betul** — ia cuma terlalu yakin: bila ia kata
60%+ realitinya 53.5%.

## 4. DAPATAN UTAMA — kadar tepat naik, jangkaan TIDAK

Jangkaan asas **semua** bar TAHAN: **+0.3118%** setiap 5 hari (median +0.0703%).

| Kuantil keyakinan | n | Menang | **Jangkaan** | Median | Untung purata | Rugi purata |
|---|---|---|---|---|---|---|
| 0.1% teratas | 4,408 | 51.81% | +0.1861% | +0.2314% | +5.26% | −5.27% |
| **1% teratas** | 44,081 | **53.66%** | **+0.3105%** | +0.3617% | +4.64% | −4.71% |
| 5% teratas | 220,408 | 53.09% | +0.2539% | +0.2939% | +4.15% | −4.16% |
| 10% teratas | 440,817 | 52.81% | +0.2359% | +0.2674% | +4.02% | −4.00% |
| 25% teratas | 1,102,043 | 52.39% | +0.2235% | +0.2295% | +4.00% | −3.93% |
| **1% TERBAWAH** | 44,081 | **41.35%** | **+0.4119%** | −2.3529% | **+17.21%** | −11.43% |
| 10% terbawah | 440,817 | 45.95% | +0.4645% | −0.6576% | +10.50% | −8.07% |

**Bar yang model paling yakin akan NAIK memberi jangkaan +0.3105%, iaitu LEBIH RENDAH daripada
membeli semua bar (+0.3118%). Bar yang model paling yakin akan TURUN memberi +0.4119%, iaitu
LEBIH TINGGI — walaupun ia menang hanya 41.35% masa.**

Mekanismenya ada dalam dua lajur terakhir. Pilihan paling yakin ada bayaran **simetri dan kecil**
(+4.64% / −4.71%); pilihan paling tidak yakin ada bayaran **terpencong kuat** (+17.21% / −11.43%).
Dengan memaksimumkan `P(naik)`, pengelas secara sistematik memilih nama **volatiliti rendah,
bayaran simetri** dan secara sistematik mengelak nama terpencong kanan yang membawa pulangan.

Itu `KOLAM_EKOR.md` (5% teratas = 63.7% pulangan) dan `SETUP.md` (penapis membuang peluang ekor)
tiba semula melalui laluan yang sama sekali berbeza — pengelas pembelajaran mesin, bukan peraturan
pedagang. **Ini kali KELIMA perangkap kadar menang diukur dalam repo ini** (selepas `X1`, `X10`,
`N16`×`X1`, dan `X25`).

## 5. Kos membunuh bakinya

Pusingan penuh 0.2% (0.1% sebelah): jangkaan 1% teratas jatuh **+0.3105% → +0.1105%**. Pada ufuk
5 hari itu kira-kira 50 pusingan setahun = **~10 mata seret kos tahunan**, berbanding memegang
yang tidak membayar apa-apa.

Jangkaan 1% paling yakin **selepas membuang 5% dagangan terbaik: −0.7313%.** Maka walaupun
pilihan terbaik model hidup sepenuhnya dalam ekor kanan yang 8–10 slot tidak boleh tangkap.

## 6. Ciri yang model guna

`larian_maks252` · `log_tutup` · `log_nilai20` · `mom252` · `vol63_pct` · `gap_abs20` · `kurt60` ·
`skew60`. Dua daripada lapan ialah **saiz/kecairan** dan empat ialah **volatiliti/bentuk ekor**.
Hanya `mom252` ialah momentum. Model ini sebahagian besarnya mempelajari "saham kecil tidak cair
bergolak berkelakuan lain" — kesan saiz dan volatiliti, bukan pattern momentum.

## 7. Jawapan

Ramalan arah harian boleh dibina dan ia **terkalibrasi**, tetapi silingnya **51.55% keseluruhan
dan 53.66% pada keyakinan tertinggi**, dan pada tahap itu ia **memperoleh kurang daripada membeli
segala-galanya**. Penalaan harian tidak merapatkan jurang ke 100%; jurang 57.04% → 51.55% ialah
ukuran langsung berapa banyak penalaan menipu.

Yang boleh diramal dengan teguh bukan arah, ia **lebar**: `atr_pct` lawan MFE 21 hari rho +0.270
(positif pada 95.5% daripada 3,499 tarikh) dan lawan |MAE| rho +0.346 (98.5%), manakala lawan
pulangan terminal rho hanya −0.043 (41.8%).

## 8. Had

Alam A02 tiada saham delist (bias survivorship, memihak kepada model). Paksi CARA dikunci `C01`.
Satu konfigurasi model sahaja diuji — penalaan hiperparameter mungkin menaikkan AUC TAHAN sedikit,
tetapi §4 menunjukkan masalahnya **bukan** ketepatan, jadi AUC lebih tinggi tidak membetulkan
tanda. Kos 0.2% ialah anggaran; gelincir sebenar pada nama tidak cair lebih tinggi.
