# Pradaftar kad skor keputusan — gate G1–G6

> **Gate yang berkuat kuasa sejak 7 Nov 2026 ialah versi dalam bahagian "Pindaan 7 Nov 2026" di hujung fail ini.** Jadual asal di bawah dikekalkan sebagai rekod pradaftar 6 Nov 2026.

**Dipradaftar 6 Nov 2026**, sebelum mana-mana kaedah matang (Lejar Penuh: 15 hari beli; lorong paling lama 15 sesi). Keputusan pengguna pada tarikh yang sama: Pilihan B + T4 daripada `reports/Audit dashboard v154 pilih kaedah.md`, dengan jawapan "Kunci apa adanya" bagi gate di bawah.

Pelaksana: `standard/kad_skor.py` (gate + status), `standard/portfolio_t4.py` (lorong T4). Kunci: `ujian/test_kad_skor.py::TestKunci` gagal jika mana-mana ambang di bawah berubah. **Mengubah ambang memerlukan keputusan pengguna DAN pradaftar baharu bertarikh dalam fail ini, sebelum data yang terkesan dilihat** — pelajaran `REVERSE/AUDIT_JEJAK_N.md` (`gate2` m=8 melonggarkan ambang selepas keputusan dilihat) dan prinsip `REVERSE/STRATEGI.md` §3.

## Soalan

Satu kaedah untuk wang sebenar. Rugi kecil, untung besar. Data papertrade mesti mencukupi untuk memutuskan.

## Penyebut (satu sahaja)

Setiap posisi Lejar Penuh **lorong 1** (keluar kaedah itu sendiri) bagi kesemua kaedah Mxx + Nxx. Posisi terbuka **ditanda-ke-pasaran** pada tutup terakhir stor. Kos 0.2% setiap pusingan ditolak. Sebab: penapisan keluar membuat purata posisi ditutup sahaja bias pada arah bertentangan bagi kaedah bersasaran dan kaedah berhenti ketat (`laporan/KAEDAH_TERBAIK.md` §3a; `laporan/LIFT_KAEDAH.md`).

## Gate

| Gate | Syarat lulus | Ambang dikunci | Sumber ambang |
|---|---|---|---|
| G1 kematangan | hari beli ≥ 20 **DAN** (posisi ditutup ≥ n_perlu **ATAU** hari beli ≥ hari beli perlu untuk lift 2 mata) | `G1_HARI_BELI_MIN = 20`, `G1_BEZA_MATA = 1.0`, `G1_LIFT_MATA = 2.0`, z 1.96 / 0.84 | `penganalisis.PANTAU_G`; `KAEDAH_TERBAIK.md` §6; `LIFT_KAEDAH.md` |
| G2 jangkaan | jangkaan semua posisi > 0 **DAN** had bawah selang keyakinan 95% > 0, SE berkelompok ikut hari beli | `G2_ALPHA = 0.05` | `REVERSE/NXX.md` (perangkap lift positif atas asas negatif: jangkaan mutlak wajib) |
| G3 lift | lift padan hari beli × baldi hari pegang > 0 **DAN** lulus BH-FDR pada penyebut semua kaedah diuji | `G3_Q = 0.05` | `standard/lift_kaedah.py` |
| G4 henti hari-0 | bilangan henti pada hari beli ≤ 0, iaitu **sifar secara struktur** (pindaan 6 Nov 2026, lihat di bawah) | `G4_HARI0_MAKS = 0` | `REVERSE/KOLAM_EKOR.md` §4a; `REVERSE/CARA.md`; laporan audit v154 |
| G5 pantau | status pantau Papan Penganalisis bukan GANTUNG/BERSARA, dan kejatuhan kohort `p_dd ≤ p_dd_had` jika had wujud | — | `standard/penganalisis.py` |
| G6 portfolio | lorong T4 **L1** kaedah itu: sesi ≥ 126 **DAN** pulangan > SPUS tingkap sama **DAN** pulangan > persentil 95 jalur rawak 20 cabutan tingkap sama **DAN** MDD ≥ −26.82% | `G6_SESI = 126`, `G6_PERSENTIL = 95`, `G6_MDD = -26.82` | `laporan/BANDING_SPUS.md`; `REVERSE/KEPEKATAN_BENIH.md`; `REVERSE/PENANDA_ARAS_SYARIAH.md` |

`n_perlu = ceil(((1.96 + 0.84) × SD ÷ 1.0)²)`, dengan SD = median SD pulangan setiap posisi dalam-kaedah, **dikira semula setiap larian**. Hari beli perlu untuk lift 2 mata dibaca daripada `lift.json` `perlu_2mata` (juga dikira semula setiap larian). Ambang yang bergerak dengan data ialah ambang yang tidak boleh hanyut dalam teks; ambang yang dikunci ialah **formula** dan **parameternya**.

## Status (satu kosa kata, keutamaan atas ke bawah)

1. **NEGATIF** — lift negatif yang bertahan BH-FDR (bukti merugikan, matang atau tidak).
2. **GAGAL** — G5 gagal, atau G1 lulus tetapi G2, G3 atau G4 gagal.
3. **BELUM CUKUP** — G1 belum lulus.
4. **CALON** — G1–G5 lulus; G6 belum. Setiap dagangan lulus, portfolio belum terbukti mengalahkan SPUS.
5. **TERBUKTI** — G1–G6 lulus. Satu-satunya status yang bermakna untuk wang sebenar.

## Lorong T4 (`portfolio_t4.py`)

- Satu lorong 10 slot bagi **setiap** kaedah dalam Lejar (keputusan pengguna: semua 222, bukan calon sahaja), bermula pada belian pertama kaedah itu. Saiz 10% ekuiti semalam, satu posisi setiap saham, kos 0.1% setiap belah, susunan ikut `rank` kaedah itu sendiri.
- **L1** = keluar kaedah (dinilai oleh G6). **L2** = lorong 2 Chandelier 4×ATR14 (maklumat). L1 dipilih kerana keluar ialah sebahagian kaedah (bagi Nxx, `N19X13` = keluar `X13`) dan pilihan keluar ~12× lebih berpengaruh daripada masuk (`REVERSE/NXX_KELUAR.md`).
- Kawalan: 20 cabutan rawak 10 slot atas SELURUH kolam Lejar, lorong kaedah, diasas semula pada tarikh mula setiap lorong.
- SPUS: asas buka sesi pertama lorong; MDD termasuk asas 1.0 (tiga peraturan `BANDING_SPUS.md`).
- Campuran T4 = teras SPUS + satelit kaedah L1 pada **80/20, 70/30 dan 50/50**, diimbang semula sesi pertama setiap bulan. Keputusan pengguna: papar ketiga-tiga; pilihan berat ditangguh sehingga G6 lulus. Campuran **bukan** gate.

## Lajur maklumat (bukan gate)

Menang %, untung purata, rugi purata, payoff, CVaR 10%, terburuk, MAE/MFE median, `tanpa5` (jangkaan selepas buang 5% posisi terbaik), kejatuhan kohort, lintas earnings, semakan luar sampel x/3, purata ditutup lawan terbuka. Kadar menang tidak pernah dipapar tanpa payoff di sebelahnya (`REVERSE/NXX_KELUAR.md`: `X10` menang 94.1% dengan jangkaan −0.023%).

## Pindaan 6 Nov 2026 — G4 diketatkan (keputusan pengguna)

**Pindaan bertarikh 6 Nov 2026**, dibuat pada hari yang sama dengan pradaftar dan **sebelum mana-mana kaedah melepasi G1** (paling awal ~6 Jan 2027), jadi tiada status yang dilihat bergantung padanya. Sebab: G4 asal lulus jika "hari-0 = 0 ATAU jangkaan termasuk hari-0 > 0". Oleh kerana G2 sudah mewajibkan jangkaan > 0, setiap kaedah yang lulus G2 juga lulus G4 — G4 tidak pernah mengubah status. Laporan audit v154 (G4: "henti hari-0 = 0 secara struktur") memaksudkan gate yang menapis. Pengguna memilih versi ketat: **`G4_HARI0_MAKS = 0`**. Kesan yang dijangka: kaedah Mxx berhenti ketat yang pernah dihentikan pada hari beli akan GAGAL selepas G1; Nxx (`stop = NaN`) lulus secara struktur. Ini bukan pelonggaran — ia mengetatkan — dan `TestKunci` kini mengunci nilai ini juga.

## Keadaan pada pradaftar (6 Nov 2026)

222 kaedah: TERBUKTI 0 · CALON 0 · BELUM CUKUP 212 · GAGAL 0 · NEGATIF 10. Paling awal G1 (lift 2 mata) ~6 Jan 2027; paling awal G6 ~9 Apr 2027.

## Pindaan 7 Nov 2026 — gate disahkan plasebo dan diselaraskan dengan toleransi MDD pengguna

**Dipradaftar 7 Nov 2026**, sebelum mana-mana kaedah melepasi G1 dan **sebelum status di bawah pindaan ini dikira**. Keputusan pengguna 7 Nov 2026 selepas audit penuh ("saya mengharapkan anda untuk tolong saya"; toleransi MDD akaun **-10%**, matlamat untung bersih > rugi).

### Mengapa (diukur, bukan pendapat)

1. **G3 lama mengukur bentuk keluar, bukan pemilihan saham.** Belian RAWAK daripada kolam Lejar sebenar dengan henti 2×ATR + sasaran 6% mendapat lift **+2.17 mata** (p < 0.05 dalam 95% cabutan); tanpa henti **-2.00 mata**. Punca: padanan baldi hari pegang (yang ditentukan oleh peraturan keluar) dan kolam yang 65% Nxx tanpa henti ditanda-ke-pasaran semasa pembetulan.
2. **SE berkelompok ikut hari beli terlalu sempit.** Plasebo pada panel A02 2010–2026 (207 tingkap × 60 hari beli): kadar lulus palsu **51%** bagi plasebo yang membeli saham sama berulang kali dan **30%** bagi plasebo condong ATR, lawan sasaran 5%. Posisi terbuka semua hari beli juga ditanda pada SATU tutup yang sama; menanda sehari lewat menukar NEGATIF 10 → 4.
3. **G1 lama boleh lulus ~12 Nov 2026** melalui laluan "≥ 610 posisi ditutup" sedangkan posisi sehari berkorelasi (varians 2.9–7× andaian bebas) dan kesemua 15 hari beli berada dalam satu fasa pasaran (QQQ di bawah SMA50 dan SMA10 < SMA20 sejak 16 Okt 2026). 88.9% posisi Nxx bertarikh isyarat sebelum larian malam langsung pertama Nxx (bina semula 3 Nov 2026 mengisi 15 Okt–2 Nov).
4. **G6 lama memakai MDD -26.82% (MDD SPUS)**, sedangkan toleransi pengguna ialah -10%; dan "p95 daripada 20 cabutan" ialah cabutan ke-2 terbesar (kadar lulus palsu disimulasi 9.2%).

### Peraturan tetap baharu: gate kemahiran mesti lulus plasebo

Mana-mana gate yang mendakwa mengukur KEMAHIRAN (G3, NEGATIF) mesti memberi kadar lulus palsu **≤ 5%** pada tiga plasebo (pilihan rawak bebas, rawak "lekit" yang membeli saham sama berulang kali, rawak condong ke tercile ATR tertinggi) pada panel A02 2010–2026, sebelum dikunci. Skrip pengesahan: `standard/plasebo_gate.py`; keputusan: `laporan/PLASEBO_GATE.md`. Gate yang lulus ujian ini tidak diubah lagi tanpa keputusan pengguna.

### Gate berkuat kuasa (menggantikan G1, G2, G3, G6 dan syarat NEGATIF)

| Gate | Syarat lulus | Ambang dikunci |
|---|---|---|
| G1 kematangan | hari beli **LANGSUNG** ≥ maks(`G1_HARI_BELI_MIN`, hari beli perlu untuk lift `G1_LIFT_MATA` mata) **DAN** ≥ `G1_REJIM_MIN` hari beli langsung dalam rejim ON **DAN** ≥ `G1_REJIM_MIN` dalam rejim OFF. Laluan "posisi ditutup ≥ n_perlu" **dibuang**. | `G1_HARI_BELI_MIN = 20`, `G1_LIFT_MATA = 2.0`, `G1_REJIM_MIN = 10`, `MULA_LANGSUNG = M: 2026-10-15, N/GB: 2026-11-03` |
| G2 jangkaan | **buku** kaedah (berat sama setiap posisi pada belian, keluar lorong 1, kos 0.2% setiap pusingan, ditanda setiap hari): purata pulangan harian > 0 **DAN** had bawah selang 95% > 0, SE **Newey-West** lag `G2_NW_LAG`, tingkap langsung. | `G2_ALPHA = 0.05`, `G2_NW_LAG = 5` |
| G3 lift masuk | pulangan ufuk TETAP `G3_UFUK` sesi (beli buka → tutup sesi ke-10, kos 0.2%), **bebas peraturan keluar**; asas = purata saham-hari UNIK kolam Lejar pada hari beli sama **DAN tercile ATR14% sama**, tidak termasuk saham-hari kaedah itu sendiri; SE **dua hala (saham, minggu ISO beli)**, df = kluster terkecil − 1; lift > 0 **DAN** lulus BH-FDR step-up q `G3_Q` atas semua kaedah diuji. Hanya posisi langsung dengan ufuk lengkap. | `G3_Q = 0.05`, `G3_UFUK = 10`, `G3_MIN_N = 30`, `G3_MIN_MINGGU = 5` |
| G4 hari-0 | tidak berubah | `G4_HARI0_MAKS = 0` |
| G5 pantau | tidak berubah | — |
| G6 portfolio | lorong T4 L1: sesi ≥ `G6_SESI` **DAN** pulangan > 0 **DAN** pulangan pada MDD `G6_MDD_HAD` (= pulangan × min(1, 10 ÷ \|MDD\|)) > SPUS pada MDD sama, tingkap sama **DAN** nisbah pulangan ÷ \|MDD\| > **maksimum** jalur rawak (ujian pangkat: kadar palsu 1/21 = 4.8% dengan 20 cabutan). | `G6_SESI = 126`, `G6_MDD_HAD = -10.0` |

**NEGATIF** = G1 lulus **DAN** lift masuk < 0 yang lulus BH-FDR. Sebelum G1 tiada label NEGATIF (data belum matang dan satu fasa pasaran sahaja).

**Rejim** (untuk G1 dan lajur maklumat): ON = QQQ tutup > SMA50 **DAN** SMA10 > SMA20 pada tarikh isyarat (`data/harga/stor/harga_idx.csv`). Asas: kelebihan relatif saham pemimpin bertukar tanda ikut rejim ini dalam kedua-dua tingkap 2010–19 dan 2020–26, 12/17 tahun (kajian 7 Nov 2026).

**Hari beli langsung**: tarikh isyarat ≥ tarikh larian malam langsung pertama selepas peraturan kaedah dibekukan. Mxx: 2026-10-15 (permulaan Lejar). Nxx/GBxx: 2026-11-03 (bina semula 3 Nov mengisi semula 15 Okt–2 Nov dengan kod baharu; itu isian, bukan rekod hadapan).

### Keputusan plasebo yang menentukan reka bentuk G3 (panel A02, 207 tingkap × 60 hari beli × 15 pilihan/hari)

| Plasebo | Asas | Kluster | Lulus palsu | Kalibrasi SD/SE |
|---|---|---|---|---|
| bebas | hari | hari beli (lama) | 5.3% | 1.01 |
| lekit | hari | hari beli (lama) | **51.2%** | 2.56 |
| condong ATR | hari | hari beli (lama) | **29.5%** | 2.29 |
| bebas | hari × tercile ATR | saham + minggu | 1.0% | 0.90 |
| lekit | hari × tercile ATR | saham + minggu | 1.9% | 0.96 |
| condong ATR | hari × tercile ATR | saham + minggu | 1.4% | 0.85 |

Reka bentuk terpilih (baris tiga terakhir) konservatif: kadar lulus palsu di bawah 2% pada ketiga-tiga plasebo (penerokaan). **Pengesahan dengan kod produksi** (`standard/plasebo_gate.py`, benih berbeza, 7 Nov 2026 12:26 UTC): **1.9% · 3.4% · 1.9%** (bebas · lekit · condong) lawan reka bentuk lama 5.3% · 45.4% · 28.5% — lulus had ≤ 5% (`laporan/PLASEBO_GATE.md`).

### Had yang diketahui

- G3 baharu mengukur kemahiran MASUK pada ufuk 10 sesi; nilai peraturan keluar diukur oleh G2 (mutlak) dan G6 (portfolio). Ini pemisahan yang disengajakan.
- Jalur rawak G6 masih mencampur keluar semua kaedah; nisbah pulangan ÷ \|MDD\| mengurangkan, tetapi tidak menghapuskan, kesan gaya keluar.
- G5 tidak boleh mengikat Nxx (tiada kalibrasi backtest); tidak berubah.
- Dashboard memaparkan lajur yang sama nama; teks penerangan dashboard dikemas dalam fasa persembahan.

## Pindaan 9 Nov 2026 — lorong T4 (G6) daripada posisi LANGSUNG sahaja

**Dipradaftar 9 Nov 2026**, sebelum mana-mana kaedah melepasi G1 (paling awal ~12 Nov 2026) dan sebelum mana-mana lorong
mencapai `G6_SESI` (paling lama 16 sesi). Keputusan pengguna 9 Nov 2026 ("ya") selepas semakan semula Skor Kaedah
(`SPEC_SKOR_KAEDAH.md` pindaan (a)) menemui: `portfolio_t4.py` membina lorong setiap kaedah daripada SEMUA posisi Lejar
sejak 16 Okt 2026, termasuk posisi isian bina semula Nxx/GB (15 Okt–2 Nov) yang bukan rekod hadapan — bercanggah dengan
penyebut "hari beli LANGSUNG" G1–G3. Contoh: `N50X14` lorong penuh +10.75 % (16 sesi) lawan +3.18 % (4 sesi LANGSUNG).

Pembetulan: `portfolio_t4.calon()` menapis `lift_kaedah.langsung` (`LANGSUNG_SAHAJA = True`, dikunci `TestKunci`), jadi
lorong L1/L2 setiap kaedah bermula pada belian LANGSUNG pertamanya dan jalur rawak dibina daripada kolam LANGSUNG yang
sama. Lorong Mxx tidak berubah (LANGSUNG sejak 15 Okt; lorong bermula 16 Okt). Ambang G6 (`G6_SESI`, `G6_MDD_HAD`) TIDAK
berubah; ini mengetatkan penyebut, bukan melonggarkan gate. Kesan: lorong Nxx/GB kini ~4 sesi, jadi anggaran G6 Nxx/GB
beralih ~12 sesi kemudian (~akhir April 2027).
