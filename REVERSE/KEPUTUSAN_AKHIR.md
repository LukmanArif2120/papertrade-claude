# KEPUTUSAN AKHIR — baris gilir E1–E6 ditutup

**Status: `BERHENTI–TUTUP`.** Syarat ini ditetapkan dalam `REVERSE/STRATEGI.md` §3 dan
dipersetujui pengguna **sebelum** E1 dijalankan: jika E1 hingga E6 selesai tanpa mana-mana
konfigurasi mencapai **T1** atau **T3**, kajian signal/pembinaan ditutup dan **tiada
eksperimen ke-7 ditambah selepas melihat keputusan**.

Enam selesai. **T1 = 0. T3 = 0.**

## 1. Angka

| | konfigurasi | larian | P1 | **P2** | P3 | P4 | **T1** | **T3** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E1 PEGANG × SLOT | 320 | 3,360 | 29 | 24 | 101 | 9 | 0 | 0 |
| E2 ALAM `AL02` | 160 | 1,680 | 12 | **0** | 37 | 0 | 0 | 0 |
| E3 INSTRUMEN bakul sektor | 40 | 230 | 26 | **0** | 5 | 1 | 0 | 0 |
| E4 KELUAR portfolio | 48 | 276 | 33 | **0** | 16 | 17 | 0 | 0 |
| E5 KORELASI had industri | 96 | 1,008 | 23 | **0** | 24 | 8 | 0 | 0 |
| E6 GABUNGAN hierarki | 60 | 440 | 38 | **0** | 32 | 10 | 0 | 0 |
| **jumlah** | **724** | **6,994** | **161** | **24** | **215** | **45** | **0** | **0** |

Setiap satu dipradaftar: spec **dan** kod dikomit sebelum sebarang keputusan dilihat.

## 2. Satu ayat yang merangkum segalanya

**Set konfigurasi yang risikonya boleh diterima dan set yang pulangannya mencukupi tidak
pernah bertindih, dan jurangnya boleh diukur.**

- 24 konfigurasi melepasi `P2` (MDD ≥ −26.82%). **CAGR tertinggi antara kesemuanya ialah
  13.55%** — SPUS memerlukan > 17.95%. Jurang: **4.40 mata**.
- 161 konfigurasi melepasi `P1` (CAGR > 17.95%). **Tiada satu pun** melepasi `P2`.
- Pada E2, satu sel tersasar `P2` sebanyak **0.01 mata** (MDD −26.83%) — tetapi CAGR-nya
  7.28%, jadi ia tidak pernah hampir kepada T1.

Dan 22 daripada 24 konfigurasi yang risikonya boleh diterima memakai masuk **`RAWAK`** —
tiada isyarat langsung.

Sebabnya struktur, bukan nasib: **portfolio ekuiti panjang-sahaja yang 100% melabur tidak
boleh mempunyai MDD lebih cetek daripada indeks ekuiti melainkan ia memegang tunai** — dan
memegang tunai ialah `T4`. Enam mekanik bebas mengesahkannya.

## 3. Lima dapatan yang BERTAHAN, dan boleh diguna

Gate gagal; dapatan ini tidak. Kelima-limanya diukur, bukan ditafsir.

**(1) Keluar jauh lebih penting daripada masuk, dan keluar peringkat PORTFOLIO lebih penting
lagi.** Sebaran pilihan keluar ialah **4.997 mata** lawan lift masuk terbaik **0.392 mata**
(~12×). Dan putaran berpangkat peringkat portfolio mengalahkan keluar setiap posisi terbaik
pada alam yang sama: **+47.44% lawan +21.01%** (E4), kekal **+34.78%** selepas pembetulan
titik-masa.

**(2) Jangan tapis sehingga kolam calon runtuh — tetapi saringan berdiri membantu.** Ini
dapatan paling halus dan paling berguna. Pintu masuk **harian** (7.7–21.8 calon/sesi)
memusnahkan pemeringkat: jurang **37.6 mata** (E5). Saringan **berdiri** (102–326
calon/sesi) memperbaiki **kedua-dua** paksi (E6, `E6a` lulus 19/48).

Peraturan berangka: **kekalkan kolam calon sekurang-kurangnya ~10× bilangan slot.** Di bawah
itu menapis membunuh pemeringkat; di atas itu menapis membantu. Itu merekonsiliasi
`SETUP.md` (598/598 penapis merugikan — kesemuanya pencetus **jarang**) dengan E6.

**(3) Had industri ialah lever RISIKO yang hampir percuma.** ~~Kekangan yang memperbaiki
kedua-dua paksi~~ — **DITARIK BALIK 1 Nov 2026** oleh semakan luar sampel
(`SEMAKAN_LATIH.md`): kaki CAGR **tidak bertahan** dalam latih 2012–2019 (+1.65 → **−0.19**),
jadi +1.65 itu artifak tingkap. Kaki MDD **bertahan kukuh**: +1.60 (tahan) dan **+1.12**
(latih), mencetek pada **83.3%** sel latih. Rumusan yang betul: **had 1 pegangan setiap
industri membeli MDD lebih cetek pada kos CAGR hampir sifar.** Mekanismenya tetap diukur:
tanpa had, **6 daripada 8 slot** boleh berada dalam satu industri — "8 slot" sebenarnya ~3
taruhan.

**(4) Masalah ekor ialah sifat ALAM, bukan hukum pasaran.** 5% dagangan teratas membawa
**101.67%** jumlah pulangan pada alam 3,260 nama (95% yang lain negatif bersih), **47.92%**
pada 214 nama, dan **30.8–66.5%** pada bakul sektor — dengan `tanpa5` **positif** pada 8/8
sel bakul (E2, E3). Kesimpulan lama "kelebihan hidup sepenuhnya dalam ekor kanan" adalah
khusus kepada alam luas yang mengandungi ekor mikro-kapitalisasi.

**(5) Volatiliti rendah ialah lever MDD terbesar — dan harganya bergantung TINGKAP.**
Saringan separuh berkevolatilan rendah memberi **+22.09 mata** MDD lebih cetek pada kos
**−17.47 mata** CAGR dalam 2020–2025 (E6). **PEMBETULAN 1 Nov 2026** (`SEMAKAN_LATIH.md`,
post-hoc): dalam latih 2012–2019 ia memberi **+18.62 mata MDD pada kos +0.16 mata CAGR** —
hampir percuma, pada **100%** sel. Jadi "pertukaran tulen" ialah sifat **2020–2025**, bukan
sifat umum: tingkap itu mempunyai kepimpinan berkevolatilan tinggi yang luar biasa.

## 4. Apa yang perlu dibuat sekarang: `T4`

`SISTEM.md` mengukur nisbah `CAGR ÷ |MDD|` campuran SPUS + tunai hampir **pemalar
0.642–0.669 merentas setiap berat**. Maka **tiada titik optimum untuk dicari** — pilihan
berat bukan soalan data, ia soalan **toleransi drawdown**, dan itu keputusan pengguna.

| berat SPUS | CAGR/tahun | MDD |
|---:|---:|---:|
| 100% | +17.95% | −26.82% |
| 60% | +10.87% | −16.62% |
| 40% | +7.27% | −11.25% |
| 30% | +5.46% | −8.50% |

Diimbang bulanan. Baki dalam tunai (bukan bon — tiada riba).

Satu perbandingan yang menjelaskan keseluruhan kajian: lorong terbaik yang risikonya boleh
diterima dalam 724 konfigurasi memberi **+13.55% pada MDD −16.13%** (nisbah 0.84). Campuran
SPUS 60% memberi **+10.87% pada MDD −16.62%** (nisbah 0.65) — jadi lorong itu **memang**
sedikit lebih baik, tetapi ia memerlukan 20 slot, putaran berpangkat, kos dagangan, dan ia
satu cabutan daripada alam yang tiada saham delist. Perbezaan 2.68 mata CAGR itu bukan
jurang yang membenarkan risiko pelaksanaan.

## 5. Ke mana sumber patut dialih

Mengikut `STRATEGI.md` §3, selepas `BERHENTI–TUTUP` sumber beralih daripada **mencari
signal** kepada **pelaksanaan**. Tiga perkara yang sudah diukur merugikan dan belum
dibetulkan:

1. **Kecacatan henti hari-0** (`KOLAM_EKOR.md` §4a): 421 daripada 1,770 posisi C ditutup
   dibeli **dan** dihentikan pada hari masuk, kadar menang **0.00%**, bernilai 19.5% jumlah
   kerugian. `CARA.md` mengenal pasti puncanya — **henti ketat**, bukan "beli pada buka
   esok".
2. **Pangkat kaedah Mxx tidak boleh dipercayai** sehingga (1) dibetulkan
   (`KAEDAH_TERBAIK.md`: ia mencemari setiap pangkat).
3. **Jejak hadapan** `portfolio_slot/` perlu ~126 sesi sebelum apa-apa dakwaan
   (`BANDING_SPUS.md`); baca lajur persentil jalur, bukan lajur pulangan.

## 6. Apa yang kajian ini TIDAK buktikan

- **Tiada alam dalam kajian ini bersih.** `AL01` dan `AL02` tiada saham delist; `AL04`
  membetulkan keahlian tetapi bukan delist. Setiap CAGR condong ke atas.
- `AL02` menyanjung paksi **risiko** sebanyak **30.9 mata** (E4), jadi laporan E2 dan E3
  mesti dibaca dengan pembetulan itu.
- Keputusan **bersyarat**: kolam signal, keluar, ambang saringan dan metrik pangkat dipilih
  daripada data yang sama.
- Paksi `CARA` dikunci `C01` dalam setiap larian baris gilir.
- Enam eksperimen ialah sampel kecil bagi ruang yang mereka wakili. Kegagalan T1 **tidak**
  membuktikan tiada sistem boleh mengalahkan SPUS pada kedua-dua paksi — hanya bahawa
  **724 konfigurasi ini, pada alam ini, pada 2020–2025, tidak.**
- Satu tingkap keputusan (2020–2025) dengan satu rejim teknologi dominan.

## 7. Rekod jangkaan priori

| | betul | separa | salah |
|---|---:|---:|---:|
| E1 | 1 | 2 | 3 |
| E2 | 2 | 0 | 3 |
| E3 | 4 | 1 | 0 |
| E4 | 3 | 0 | 2 |
| E5 | 3 | 0 | 2 |
| E6 | 2 | 0 | 3 |
| **jumlah** | **15** | **3** | **13** |

Saya betul kira-kira separuh masa, dan satu-satunya pradaftar yang saya kebanyakannya betul
(E3) ialah yang menguji mekanisme yang **sudah** diukur. Pada ruang belum diukur saya salah
lebih kerap daripada betul. Corak itu sendiri dapatan, dan ia alasan mengapa setiap larian
dipradaftar: **jangkaan saya tidak patut dipercayai tanpa ukuran.**
