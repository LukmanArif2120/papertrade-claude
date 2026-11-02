# Paksi CARA pada KESEMUA enam keluar kohort 94

Pradaftar `REVERSE/SPEC_CARA_94.md` — dikomit sebelum keputusan dilihat.
BH-FDR dikira SEKALI merentas 30 perbandingan (m dipradaftar = 30); ambang BH p = nan.

## Gate — ringkasan setiap keluar

| Keluar | Slot produksi | Masuk | CARA1 | CARA2 | CARA3 | MENANG |
|---|--:|--:|--:|--:|--:|--:|
| `X36` | 37 | 37 | 0/5 | 0/5 | 4/5 | 0/5 |
| `X16` | 26 | 26 | 0/5 | 0/5 | 4/5 | 0/5 |
| `X17` | 10 | 10 | 0/5 | 0/5 | 4/5 | 0/5 |
| `X14` | 10 | 10 | 0/5 | 0/5 | 4/5 | 0/5 |
| `X13` | 6 | 6 | 0/5 | 0/5 | 4/5 | 0/5 |
| `X15` | 5 | 5 | 0/5 | 0/5 | 4/5 | 0/5 |

**LULUS KETIGA-TIGA GATE: 0 daripada 30** — tiada.

## Jangkaan setiap ISYARAT, tingkap TAHAN (bar tidak terisi = 0)

| Keluar | `C01` | `C02` | `C03` | `C04` | `C05` | `C06` | sebaran |
|---|--:|--:|--:|--:|--:|--:|--:|
| `X36` | **+1.222%** | +0.781% | +0.897% | +0.946% | +1.049% | -0.511% | 1.733 mata |
| `X16` | **+0.969%** | +0.545% | +0.768% | +0.787% | +0.792% | -0.506% | 1.475 mata |
| `X17` | **+3.287%** | +0.764% | +2.620% | +2.698% | +3.040% | -0.519% | 3.806 mata |
| `X14` | **+1.422%** | +0.474% | +1.241% | +1.269% | +1.183% | -0.523% | 1.946 mata |
| `X13` | **+5.954%** | +0.255% | +4.634% | +4.889% | +5.598% | -0.424% | 6.378 mata |
| `X15` | **+4.721%** | +0.442% | +3.832% | +3.949% | +4.403% | -0.447% | 5.168 mata |

Tebal = cara terbaik setiap keluar pada ukuran setiap ISYARAT.

## Jangkaan setiap ISIAN, tingkap TAHAN (hanya bar yang terisi)

| Keluar | `C01` | `C02` | `C03` | `C04` | `C05` | `C06` |
|---|--:|--:|--:|--:|--:|--:|
| `X36` | +1.223% | +2.090% | +1.369% | +1.270% | +1.098% | -0.511% |
| `X16` | +0.970% | +1.537% | +1.168% | +1.054% | +0.828% | -0.506% |
| `X17` | +3.289% | +2.668% | +3.906% | +3.572% | +3.165% | -0.519% |
| `X14` | +1.423% | +1.509% | +1.841% | +1.675% | +1.231% | -0.524% |
| `X13` | +5.961% | +2.788% | +6.870% | +6.464% | +5.777% | -0.424% |
| `X15` | +4.726% | +3.446% | +5.639% | +5.197% | +4.539% | -0.447% |

**Kadar isian setiap keluar** (bar isyarat yang benar-benar menjadi posisi):

| Keluar | `C01` | `C02` | `C03` | `C04` | `C05` | `C06` |
|---|--:|--:|--:|--:|--:|--:|
| `X36` | 99.9% | 37.4% | 65.5% | 74.5% | 95.5% | 99.9% |
| `X16` | 99.9% | 35.4% | 65.8% | 74.6% | 95.7% | 99.9% |
| `X17` | 99.9% | 28.6% | 67.1% | 75.5% | 96.0% | 99.9% |
| `X14` | 99.9% | 31.4% | 67.4% | 75.8% | 96.1% | 99.9% |
| `X13` | 99.9% | 9.1% | 67.5% | 75.6% | 96.9% | 99.9% |
| `X15` | 99.9% | 12.8% | 68.0% | 76.0% | 97.0% | 99.9% |

Jurang antara dua jadual di atas ialah sebab `jangkaan_isi` tidak boleh dibaca sendirian: `C03`/`C04` hanya terisi apabila harga JATUH, jadi jangkaan setiap isian yang tinggi boleh datang daripada pemilihan bar, bukan kelebihan.


## Diagnostik ekor — `tanpa5` (jangkaan selepas buang 5% pemenang teratas, TAHAN)

**Bukan gate** (spec §3: menambahnya sekarang akan menjadikan keputusan tidak boleh dibanding
dengan `cara.csv`/`cara_94.csv`). Dilapor kerana ia menunjukkan mekanisme yang min
sembunyikan.

| Keluar | `C01` | `C02` | `C03` | `C04` | `C05` | `C06` |
|---|--:|--:|--:|--:|--:|--:|
| `X36` | -2.535 | -2.626 | -2.549 | -2.536 | -2.714 | **-0.898** |
| `X16` | -2.235 | -2.448 | -2.245 | -2.240 | -2.421 | **-0.887** |
| `X17` | -2.160 | -2.487 | -2.100 | -2.104 | -2.365 | **-0.908** |
| `X14` | -1.419 | -2.200 | -1.217 | -1.276 | -1.619 | **-0.915** |
| `X13` | +1.378 | +0.251 | **+1.770** | +1.597 | +1.193 | -0.821 |
| `X15` | -2.140 | -1.938 | **-2.042** | -2.129 | -2.365 | -0.845 |

Berapa keluar di mana `tanpa5` cara **lebih baik** daripada `C01`:
`C06` 5/6 · `C03` 4/6 · `C04` 4/6 · `C02` 1/6 · `C05` 0/6.

## Tafsiran

### Keputusan: `C01` kekal, dan kini ia DIUKUR pada kesemua 94 slot

**0 daripada 30 lulus ketiga-tiga gate.** Lebih kuat daripada itu: **`CARA1` lulus 0/5 pada
setiap satu daripada enam keluar**, jadi tiada cara alternatif mengalahkan `C01` pada
kedua-dua tingkap di mana-mana keluar. `beza` tertinggi merentas kesemua 30 perbandingan
ialah **−0.154 mata** — bukan satu pun walaupun **nominally** positif, dan p terkecil
**0.9993**. Ambang BH tiada (`nan`) kerana tiada apa untuk dikorek.

Jadi ayat yang `CARA_94.md` tidak boleh tulis, kini boleh: **`C01` ialah cara pengisian
terbaik bagi kesemua enam keluar yang kohort 94 pakai, bukan hanya bagi `X13` yang memegang
6 daripada 94 slot.** Jurang anggapan itu ditutup dengan ukuran.

### Perangkap setiap-ISIAN: `C03` lebih baik pada 6/6 keluar dan tetap KALAH

| Ukuran | Berapa keluar `C03` > `C01` |
|---|--:|
| Jangkaan setiap **ISIAN** | **6/6** |
| Jangkaan setiap **ISYARAT** | **0/6** |

`C03` (buy-limit 1.5% bawah tutup) memberi jangkaan setiap isian lebih tinggi pada
**setiap** keluar — `X13` +6.870% lawan +5.961%, `X17` +3.906% lawan +3.289%. Dan ia kalah
pada setiap keluar apabila bar yang **tidak terisi** dikira. Sebabnya kadar isian **65–68%**:
sepertiga daripada isyarat tidak pernah menjadi posisi, dan bar yang hilang bukan rawak — ia
bar yang **terus naik** tanpa menyentuh had. Jadi `C03` membeli pilihan yang lebih murah
daripada subset yang lebih teruk.

Ini **bentuk keempat** perangkap yang sama yang kajian ini terus jumpa:
`KOMBINASI.md` kadar menang 61.1% pada jangkaan −0.281%; `NXX_KELUAR.md` `X10` menang 94.1%
pada −0.023%; `SETUP.md` setiap penapis positif mutlak tetapi lift negatif; dan kini
jangkaan setiap isian positif tetapi jangkaan setiap isyarat negatif. **Setiap kali,
penyebut yang salah menukar tanda.**

### `C02` (buy-stop pengesahan harga) rosak pada keluar yang terbaik

Kadar isian `C02`: `X36` 37.4% · `X16` 35.4% · `X17` 28.6% · `X14` 31.4% · **`X13` 9.1%** ·
**`X15` 12.8%**. Pada dua keluar dengan jangkaan tertinggi, menunggu pengesahan harga
kehilangan **87–91%** isyarat, dan `beza` pada `X13` ialah **−5.699 mata**. Pengesahan harga
ialah penapis, dan `SETUP.md` sudah mengukur bahawa penapis membuang peluang pada ekor.

### `C06` (bracket) — min TERBURUK, ekor TERBAIK, pada 5 daripada 6 keluar

`C06` ialah satu-satunya cara dengan jangkaan **negatif** pada setiap keluar (−0.42% hingga
−0.52%, `beza` sampai −6.378 pada `X13`). Tetapi `tanpa5`-nya **lebih baik daripada `C01`
pada 5/6 keluar**, dan pada `X36` jurangnya **+1.64 mata** (−0.898 lawan −2.535).

Itu bukan percanggahan, ia **mekanisme**: henti −3% memotong ekor KIRI (jadi purata terpangkas
naik) dan ekor KANAN (jadi min jatuh), dan kerana 5% teratas membawa 63.7% jumlah pulangan
kolam (`KOLAM_EKOR.md`), memotong ekor kanan jauh lebih mahal. `C06` juga mencetus **34,984**
henti hari-0 pada `X13` — kecacatan yang `KOLAM_EKOR.md` §4a kenal pasti, diukur di sini
sebagai akibat **henti ketat**, bukan akibat `C01`.

**Pelajaran yang boleh dipakai: jangan baca `tanpa5` sebagai "lebih kukuh".** `C06` menang
pada `tanpa5` tepat kerana ia memusnahkan apa yang membayar.

### Jangkaan priori §4 — KEEMPAT-EMPAT betul, kali pertama dalam kajian ini

| # | Jangkaan | Keyakinan | Keputusan |
|---|---|---|---|
| 1 | `C01` menang/seri pada majoriti keluar | sederhana | **BETUL**, dan lebih kuat: 6/6 |
| 2 | `C03`/`C04` lebih baik setiap isian tetapi gagal | tinggi | **BETUL** (6/6 vs 0/6) |
| 3 | sebaran cara MENGECIL pada `X36`/`X16` | **rendah** | **BETUL**: 1.733 / 1.475 lawan `X13` 6.378 |
| 4 | `C06` terburuk pada setiap keluar | tinggi | **BETUL** pada min; SALAH arah pada `tanpa5` |

Rekod sebelum ini: priori saya salah pada 2/3 gate dalam tiga pradaftar berturut-turut, dan
salah pada jangkaan yang **paling** saya yakin dalam 94B. Perbezaannya di sini jelas dan
patut dinyatakan supaya ia tidak dibaca sebagai kemahiran meramal: **larian ini menguji
mekanisme yang SUDAH diukur** (paksi CARA pada `X13`, `cara_94.csv`), bukan ruang belum
diukur. Pola itu konsisten — saya boleh meramal apa yang sudah diukur dan tidak boleh
meramal apa yang belum.

Nota kalibrasi: jangkaan #3 yang keyakinannya **paling rendah** ternyata betul dengan margin
paling besar (sebaran `X13` 4.3× sebaran `X16`). Keyakinan saya sendiri bukan penunjuk yang
boleh dipercayai, dan itu sebab setiap larian dipradaftar.

## Syarat BERHENTI §5 — DICETUS

Spec §5: *"Jika **tiada** cara lulus ketiga-tiga gate pada mana-mana keluar: paksi CARA
**DITUTUP**."* Tiada lulus, pada mana-mana enam keluar. Jadi:

- **Paksi CARA DITUTUP.** `C01` kekal dalam produksi atas sebab yang diukur merentas
  kesemua enam keluar kohort, bukan atas anggapan daripada satu keluar.
- **Jangan daftar cara ke-7**, dan jangan uji semula `C02`–`C06` pada varian lain. Jurangnya
  bukan marginal: cara terbaik yang kedua masih **−0.154 mata** di bawah `C01` dan p 0.9993.
- Kekangan sebenar yang tinggal pada kohort 94 bukan mekanik pengisian: ia **data hadapan**
  (kohort dilabel BELUM CUKUP 3–6 bulan) dan **69 baris `PERLU`** yang memerlukan ~56
  indikator/sumber data yang repo tiada.
