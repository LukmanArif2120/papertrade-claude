# Pradaftar kad skor keputusan — gate G1–G6

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
| G4 henti hari-0 | bilangan henti pada hari beli = 0, **ATAU** jangkaan semua posisi (TERMASUK posisi hari-0) > 0. Posisi hari-0 **tidak boleh** dikecualikan daripada jangkaan. | — | `REVERSE/KOLAM_EKOR.md` §4a; `REVERSE/CARA.md` |
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

## Keadaan pada pradaftar (6 Nov 2026)

222 kaedah: TERBUKTI 0 · CALON 0 · BELUM CUKUP 212 · GAGAL 0 · NEGATIF 10. Paling awal G1 (lift 2 mata) ~6 Jan 2027; paling awal G6 ~9 Apr 2027.
