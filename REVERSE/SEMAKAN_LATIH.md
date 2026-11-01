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
CAGR — kira-kira **satu perlima**. Itu konsisten dengan mekanisme yang E4/E6 sudah ukur:
menapis lebih ketat membuang calon yang pemeringkat perlukan, dan `A3` hanya mengekalkan
102 nama daripada 500.

`A3` dilaporkan **0.00 / 0.00** di atas, dan semakan semula (§ di bawah) mendapati nombor itu
**artifak pencairan**, bukan ukuran: 4 daripada 12 sel `A3` ialah `A3`×`U02` yang **degenerat
ikut binaan** (spec §4.1) dan memberi Δ = 0.00 **tepat**, jadi median mendarat di dalam blok
sifar itu. Pada 8 sel bukan-degenerat `A3` memberi **+1.33** CAGR tetapi **−1.74** MDD.
Kesimpulannya **tidak berubah** — `A3` masih gagal R1 — tetapi sebabnya **tanda bertentangan**,
bukan "hilang". Jadual di atas dikekalkan seperti dilaporkan; angka bukan-degenerat ada dalam
`semak_latih.py` bahagian 3.

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

## Semakan semula bebas (1 Nov 2026, permintaan pengguna "recheck sekali lagi")

Skrip: `REVERSE/semak_latih.py` — **tanpa pandas**, hanya `csv` + `statistics` pustaka
standard, supaya ia bukan `groupby` yang sama mengesahkan dirinya sendiri. Empat semakan:

**(1) Keutuhan tingkap — LULUS.** `latih` idx 252–2263 = 2012-01-03…2019-12-30 (2,011 sesi),
`tahan` idx 2264–akhir = 2020-01-02…2025-12-31 (1,508 sesi); bertindih **tiada**. Dagangan
bermula tepat pada idx 252, jadi tingkap latih tidak mengandungi tempoh pemanasan momentum.

**(2) Saiz alam dalam kedua-dua tingkap — LULUS, tiada perancu.** Nama LAYAK: 1,682 (2012) ·
2,082 (2016) · 2,507 (2020) · 3,123 (2025). `AL04`-500 **tidak pernah** terikat pada
ketersediaan, jadi alam berwatak sama pada kedua-dua tingkap.

**(3) Pengiraan semula bebas — LULUS, kesemua 28 nombor identik** (toleransi 0.01 mata).
Sebaran setiap sel juga disemak: bagi dakwaan utama (had 1, CAGR latih) median **−0.19**
bersamaan **min −0.19** dengan **58.3%** daripada 24 sel negatif. **Jadi `DIPALSUKAN` bukan
didorong oleh beberapa sel terpencil** — ia majoriti sel, dan min bersetuju dengan median.

**(4) Ujian tanda berpasangan + BH-FDR merentas kesemua 28 kesan** — bahagian paling berguna,
dan ia **mengubah tafsiran dua kali**:

| | median | sel + | p | FDR |
|---|---:|---:|---:|---|
| `had 1` CAGR **tahan** (dakwaan asal) | +1.65 | 16/24 | **0.152** | gagal |
| `had 1` CAGR **latih** | −0.19 | 10/24 | 0.541 | gagal |
| `had 1` MDD **latih** | +1.12 | 20/23 | **0.0005** | **LULUS** |
| `A2` MDD **latih** | +0.64 | 8/8 | **0.0078** | **LULUS** |
| `A4` MDD **latih** | +18.62 | 12/12 | **0.0005** | **LULUS** |
| `A4` CAGR **latih** | +0.16 | 6/12 | **1.000** | gagal |

Pertama: **dakwaan +1.65 itu tidak pernah boleh dibezakan daripada sifar walaupun dalam
tingkap ia diukur** (16/24 sel, p = 0.152). Jadi penarikan balik lebih kukuh daripada yang
laporan ini mula-mula nyatakan — ia bukan kes "kesan nyata yang hilang di luar sampel", ia
kes **kesan yang tidak pernah ada**. Yang bertahan ialah kaki MDD, dan ia bertahan dengan
p = 0.0005 **dalam tingkap luar sampel**.

Kedua: **8 daripada 28 kesan melepasi BH-FDR; 3 daripadanya luar sampel; kesemua 3 ialah
MDD. SIFAR kesan CAGR luar sampel melepasi FDR.** Itu ayat tunggal yang paling padat dalam
semakan ini: lever pembinaan menggerakkan **risiko**, bukan **pulangan**, dan kini itu benar
pada dua tingkap dengan kawalan pelbagai ujian. Ia sejajar sepenuhnya dengan
`KEPUTUSAN_AKHIR.md` §2 (set risiko-boleh-terima dan set pulangan-mencukupi tidak bertindih).

Ketiga: `A4` ialah lever paling kukuh yang pernah diukur dalam baris gilir — MDD mencetek
pada **12/12 sel dalam KEDUA-DUA tingkap** (p = 0.0005 setiap satu) — dan kos CAGR-nya
signifikan **hanya** dalam tahan (0/12, p = 0.0005), **tepat nol** dalam latih (6/12,
p = 1.000). Pembetulan dapatan kelima `KEPUTUSAN_AKHIR.md` disahkan dengan ujian, bukan
sekadar median.

**Keputusan semakan semula: Dakwaan A kekal `DIPALSUKAN` (lebih kukuh); Dakwaan B kekal
`DISAHKAN` (perihalan `A3` dibetulkan, verdict tidak berubah — `A1` +0.54/+1.92 dan `A2`
+1.30/+1.78 pada sel bukan-degenerat, kedua-dua paksi positif, jadi R1 masih lulus).**

`python3 REVERSE/semak_latih.py --semak` keluar 1 jika mana-mana nombor di atas tidak
dihasilkan semula, atau jika mana-mana kesan CAGR luar sampel mula melepasi FDR.

## Had

- Latih 2012–2019 ialah **satu** tingkap tambahan, bukan pengesahan merentas rejim.
- Semakan ini membetulkan **tingkap**, bukan **pemilihan**: alam, kolam signal dan ambang
  saringan masih dipilih daripada data yang sama.
- Ia **tidak** menguji dakwaan pada populasi **Mxx**. Lejar Penuh hanya mengandungi 11 sesi
  isyarat Mxx (15–28 Okt 2026) dan tiada matriks isyarat Mxx bersejarah di cakera.
- `mdd_latih` kini direkod; mana-mana laporan E1–E4 yang melapor kesan pada MDD **masih**
  tingkap tahan sahaja dan belum disemak dengan cara yang sama.
