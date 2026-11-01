# SEMAKAN_LATIH — pemalsuan luar sampel bagi dua dapatan pembinaan

Pradaftar: `REVERSE/SPEC_SEMAKAN_LATIH.md` (komit `45e6804`, sebelum keputusan latih
dilihat). Grid, benih dan enjin **tidak berubah**; satu lajur `mdd_latih` ditambah dan
E5 + E6 dijalankan semula.

**Kawalan regresi LULUS:** 1,008 + 440 baris, nilai `cagr`, `mdd` dan `cagr_latih` tingkap
tahan dihasilkan semula **identik** (maks |Δ| = 0.00e+00). Jadi satu-satunya perkara baharu
ialah tingkap latih.

## Keputusan: Dakwaan A **DIPALSUKAN** · Dakwaan B **DISAHKAN tetapi jauh lebih kecil**

## Dakwaan A — had industri: kaki CAGR tidak bertahan

| had | TAHAN Δ CAGR | Δ MDD | LATIH Δ CAGR | Δ MDD | % sel MDD cetek (latih) |
|---:|---:|---:|---:|---:|---:|
| **1** | **+1.65** | **+1.60** | **−0.19** | **+1.12** | 83.3% |
| 2 | +0.76 | +0.02 | +0.04 | +0.00 | 45.8% |
| 3 | +0.47 | +0.00 | +0.12 | +0.00 | 33.3% |

- **R1 (tanda sama pada kedua-dua paksi): GAGAL.** Tiada aras had mempunyai kedua-dua Δ
  positif dalam latih. Had 1 bertukar daripada **+1.65** kepada **−0.19** pada paksi CAGR.
- R2 (≥ 50% sel MDD mencetek): lulus, 54.2%.

Jadual keputusan spec §4: **R1 gagal → DIPALSUKAN.**

**Apa yang sebenarnya benar:** had industri ialah **lever risiko tulen**, bukan lever
dwi-arah. Kaki MDD bertahan kukuh — +1.12 mata dalam latih, mencetek pada **83.3%** sel,
berbanding +1.60 dan 56.9% dalam tahan. Kaki CAGR **tidak wujud**.

Dakwaan asal dalam `KORELASI.md` dan `KEPUTUSAN_AKHIR.md` §3 — *"kekangan yang MEMBAYAR …
memperbaiki kedua-dua paksi"* — **ditarik balik**. Gantinya: *had industri membeli MDD
yang lebih cetek pada kos CAGR hampir sifar.* Itu masih berguna, dan ia masih lebih baik
daripada setiap lever lain yang diukur, tetapi ia **bukan** makan tengah hari percuma.

## Dakwaan B — saringan berdiri: bertahan, tetapi saiznya runtuh

| saringan | TAHAN Δ CAGR | Δ MDD | LATIH Δ CAGR | Δ MDD | % sel MDD cetek (latih) |
|---|---:|---:|---:|---:|---:|
| `A1` `tutup > ma200` | +1.67 | +1.47 | **+0.63** | **+1.11** | 66.7% |
| `A2` `rs_pst ≥ 50` | +4.26 | +0.94 | **+0.64** | **+0.64** | 66.7% |
| `A3` `rs_pst ≥ 80` | +6.29 | +0.23 | **0.00** | **0.00** | 33.3% |

- **R1: LULUS** — `A1` dan `A2` kedua-duanya positif pada kedua-dua paksi dalam latih.
- **R2: LULUS** — 55.6%.

Jadual keputusan: **DISAHKAN.**

**Tetapi magnitudnya mesti dibetulkan.** `A2` jatuh daripada **+4.26** kepada **+0.64** mata
CAGR — kira-kira **satu perlima**. `A3`, saringan paling ketat, **hilang sepenuhnya**
(0.00 / 0.00). Itu konsisten dengan mekanisme yang E4/E6 sudah ukur: menapis lebih ketat
membuang calon yang pemeringkat perlukan, dan `A3` hanya mengekalkan 102 nama daripada 500.

Dapatan yang bertahan ialah **arah dan peraturan kolam**, bukan nombor: saringan berdiri
yang **longgar** (mengekalkan ~300 daripada 500) membantu sedikit pada kedua-dua paksi;
saringan ketat tidak.

## Dapatan POST-HOC yang membalikkan dapatan kelima (bukan gate)

`A4` (separuh berkevolatilan rendah) **bukan** sebahagian dakwaan yang dipradaftar (spec §2
menyatakannya secara eksplisit), jadi ini pemerhatian, bukan keputusan gate. Ia tetap
penting:

| | TAHAN | LATIH |
|---|---:|---:|
| Δ CAGR | **−17.47** | **+0.16** |
| Δ MDD | +22.09 | **+18.62** |
| % sel MDD cetek | — | **100.0%** |

Dalam 2012–2019, saringan volatiliti rendah memberi **+18.62 mata MDD lebih cetek pada kos
CAGR hampir sifar**, pada **setiap** sel. Dalam 2020–2025 ia membayar **−17.47 mata**.

Jadi dapatan kelima `KEPUTUSAN_AKHIR.md` — *"volatiliti rendah ialah pertukaran TULEN"* —
**khusus kepada 2020–2025**, bukan sifat umum. Tingkap itu mempunyai kepimpinan
berkevolatilan tinggi yang luar biasa; menapisnya keluar mahal di sana dan hampir percuma
sebelum itu. Dapatan kelima dibetulkan, bukan ditarik balik.

## Jangkaan priori lawan keputusan

| | Saya jangka | Berlaku | |
|---|---|---|---|
| (1) kaki MDD Dakwaan A disahkan | ya | +1.12, 83.3% sel | **betul** |
| (2) kaki CAGR Dakwaan A lebih lemah, mungkin negatif | ya | **−0.19** | **betul** |
| (3) B bertahan pada CAGR, lebih lemah pada MDD | ya | bertahan pada kedua-dua, tetapi **MDD bertahan lebih baik** (75% dikekalkan) daripada CAGR (38%) | separa — arah salah |
| (4) satu daripada dua dakwaan turun | ya | A DIPALSUKAN | **betul** |

Tiga betul, satu separa — rekod terbaik setakat ini, dan ia pada semakan terhadap kerja saya
sendiri. Jangkaan (2) khususnya tepat atas sebab yang betul: saya menulis bahawa +1.65 mata
itu "mencurigakan" kerana 2020–2025 mempunyai kepimpinan sempit dan mengehadkan industri
sepatutnya merugikan pulangan di sana. Ia memang artifak tingkap.

## Pembetulan yang dibuat

1. `KEPUTUSAN_AKHIR.md` §3 dapatan (3) ditulis semula: lever **risiko**, bukan dwi-arah.
2. `KEPUTUSAN_AKHIR.md` §3 dapatan (5) dibetulkan: pertukaran `A4` khusus 2020–2025.
3. `KORELASI.md` dan `HIERARKI.md` membawa nota pembetulan di atas, laporan asal **tidak**
   dipadam.
4. Registry `KR03` dan `GB07` dikemas dengan nombor latih.
5. `CLAUDE.md` dan dashboard dikemas.

## Had

- Latih 2012–2019 ialah **satu** tingkap tambahan, bukan pengesahan merentas rejim.
- Semakan ini membetulkan **tingkap**, bukan **pemilihan**: alam, kolam signal dan ambang
  saringan masih dipilih daripada data yang sama.
- Ia **tidak** menguji dakwaan pada populasi **Mxx**. Lejar Penuh hanya mengandungi 11 sesi
  isyarat Mxx (15–28 Okt 2026) dan tiada matriks isyarat Mxx bersejarah di cakera.
- `mdd_latih` kini direkod; mana-mana laporan E1–E4 yang melapor kesan pada MDD **masih**
  tingkap tahan sahaja dan belum disemak dengan cara yang sama.
