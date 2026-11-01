# HIERARKI — `GB07`: signal A tentukan ALAM, signal B tentukan URUTAN

> **PEMBETULAN 1 Nov 2026 — `SEMAKAN_LATIH.md`.** Dakwaan laporan ini **DISAHKAN** luar
> sampel tetapi **magnitudnya runtuh**: `A2` jatuh daripada +4.26 kepada **+0.64** mata CAGR
> dalam latih 2012–2019, dan `A3` hilang sepenuhnya (**0.00 / 0.00**). Yang bertahan ialah
> **arah** dan peraturan kolam, bukan nombor: saringan berdiri yang **longgar** membantu
> sedikit pada kedua-dua paksi; saringan **ketat** tidak. Juga: `A4` **bukan** pertukaran
> tulen di luar 2020–2025 — dalam latih ia memberi +18.62 mata MDD pada kos +0.16 mata CAGR.
> Laporan asal dikekalkan tanpa diubah di bawah.

Pradaftar: `REVERSE/SPEC_HIERARKI.md` (komit `b30b2a0`, sebelum larian).
Skrip: `REVERSE/step29_hierarki.py` · Data: `REVERSE/hierarki.csv`,
`REVERSE/hierarki_ringkas.csv`

60 konfigurasi pada `AL04` titik-masa 500 teratas, `U01` 20 benih → 440 larian.
**Eksperimen terakhir dalam baris gilir.**

## Keputusan: T1 **0**, T3 **0** → **BERHENTI–TUTUP**. Tetapi `E6a` **LULUS**.

| Gate | | |
|---|---|---|
| P1 | CAGR > 17.95% | 38 / 60 |
| P2 | MDD ≥ −26.82% | **0 / 60** |
| P3 | CAGR > p95 kawalan | 32 / 60 |
| P4 | nisbah > 0.669 | 10 / 60 |
| **T1 / T3** | | **0 / 0** |
| **E6a** | saringan mengalahkan `A0` pada **KEDUA-DUA** paksi | **LULUS — 19 / 48 sel** |

`P2` gagal pada setiap sel untuk kali **keenam berturut-turut**.

## Dapatan utama: menapis tidak buruk — menapis sehingga JARANG yang buruk

E4 dan E5 mengukur bahawa pintu masuk harian **memusnahkan** putaran berpangkat: jurang
**37.6 mata** antara `RAWAK` dan `GB02_atau3`. Kesimpulan mudahnya ialah "jangan menapis".
E6 menunjukkan itu **salah**, dan memberi versi yang betul.

| saringan | nama/sesi | Δ CAGR median | Δ MDD median (+ = cetek) |
|---|---:|---:|---:|
| `A0` tiada | 500 | — | — |
| `A1` `tutup > ma200` | 326 | **+1.67** | **+1.47** |
| `A2` `rs_pst ≥ 50` | 282 | **+4.26** | **+0.94** |
| `A3` `rs_pst ≥ 80` | 102 | **+6.29** | **+0.23** |
| `A4` `atr_pct` bawah median | 250 | **−17.47** | **+22.09** |

**`A1`, `A2` dan `A3` memperbaiki KEDUA-DUA paksi.** Perbezaannya dengan pintu harian bukan
*jenis* operasi — kedua-duanya menapis — tetapi **kekerapan**:

- Pintu harian `GB02_atau3`: **7.7–21.8** calon/sesi → kolam lebih kecil daripada, atau
  hampir sama dengan, bilangan slot. Pemeringkat tiada pilihan.
- Saringan berdiri: **102–326** calon/sesi → kolam **13–41×** bilangan slot. Pemeringkat
  masih mempunyai ruang penuh untuk bekerja.

**Peraturan yang boleh digunakan: kekalkan kolam calon sekurang-kurangnya ~10× bilangan
slot.** Di bawah itu, menapis membunuh pemeringkat; di atas itu, menapis membantu.

Itu merekonsiliasi `SETUP.md` (598/598 penapis merugikan) dengan dapatan ini: setiap setup
`SETUP.md` ialah pencetus **jarang**, bukan keadaan **berdiri**.

## `A4` ialah lever MDD terbesar dalam kajian — dan ia pertukaran tulen

`A4` (separuh berkevolatilan rendah) memberi **+22.09 mata** MDD lebih cetek — jauh lebih
besar daripada apa-apa lever lain yang pernah diukur — dan MDD paling cetek dalam E6,
**−32.01%**. Tetapi ia membayar **−17.47 mata** CAGR, dan nisbahnya jatuh kepada 0.36–0.39.

Itu tepat corak "peruntukan tunai dalam samaran" yang `SISTEM.md` jangkakan, dan ia
**berbeza** daripada had industri E5, yang memperbaiki kedua-dua paksi. Dua lever, dua
sifat berbeza, kedua-duanya kini diukur.

Walaupun dengan `A4`, MDD terbaik (−32.01%) masih **5.19 mata** lebih dalam daripada SPUS.

## Konfigurasi terbaik, dan apa yang ia bukan

`A2` (`rs_pst ≥ 50`) × `U14` (momentum 12−1) × 8 slot × had industri 2 →
**CAGR +53.15% / MDD −57.56% / nisbah 0.92**, d_CAGR **+10.63** dan d_MDD **+11.59** lawan
tiada saringan.

Itu nombor CAGR tertinggi dalam seluruh baris gilir. Ia **bukan** dapatan boleh didagang:
MDD −57.56% bermakna kehilangan lebih separuh modal, `nb = 1` (satu cabutan tentu, tiada
jalur benih), dan ia dipilih sebagai maksimum merentas 60 konfigurasi pada data yang sama.

**Setiap pemenang `E6a` memakai `U14`, bukan `U02`** — jangkaan priori saya #5 salah. `U02`
menang di E4/E5 pada alam `AL02`; pada alam titik-masa yang lebih luas, momentum 12−1 lebih
baik.

Sel `A2`/`A3` × `U02` adalah **degenerat mengikut binaan** (menyaring ikut RS lalu
memeringkat ikut RS), seperti didedahkan dalam spec §4.1 sebelum larian; ia dilaporkan
identik dengan `A0` dan tidak dikira sebagai dapatan.

## Jangkaan priori lawan keputusan

| | Saya jangka | Berlaku | |
|---|---|---|---|
| (1) T1 = 0, T3 = 0 | ya | ya | **betul** |
| (2) `A4` beri MDD paling cetek | ya | −32.01%, +22.09 mata | **betul** |
| (3) `E6a` **GAGAL** | gagal | **LULUS, 19/48** | **salah** |
| (4) `A3` lebih teruk daripada `A2`; `A2` ≈ `A0` | ya | `A3` beri Δ CAGR **terbaik**; `A2` jelas > `A0` | **salah** |
| (5) `U02` kekal pemeringkat terbaik | ya | **setiap** pemenang `E6a` memakai `U14` | **salah** |

Dua betul, tiga salah. Jangkaan (3) ialah yang paling penting dan saya menulis dalam spec:
*"Jika jangkaan 3 salah … itu dapatan paling berguna dalam seluruh baris gilir, kerana ia
satu-satunya cara yang tinggal untuk menggerakkan paksi MDD tanpa memegang tunai."* Ia
memang salah, dan dapatan itu memang berguna — tetapi ia tetap tidak mencukupi untuk T1.

## Had

- `AL04` membetulkan keahlian tetapi **bukan** delist; alam asas `a02` tiada saham delist.
- Ambang saringan dipilih oleh saya daripada ruang yang sama yang menghasilkan keputusan
  terdahulu; keputusan kekal **bersyarat**.
- `nb = 1` bagi `U02`/`U14`; hanya `U01` mempunyai jalur benih. Sel terbaik ialah **satu
  cabutan** dan tidak boleh dirapatkan.
- Lima saringan ialah sampel kecil bagi ruang "saringan berdiri"; kegagalan T1 di sini
  **tidak** membuktikan tiada saringan berdiri boleh mencapainya.
- `imbang` dikunci 63; `CARA` dikunci `C01`.
- Semakan pra-larian mendedahkan sebahagian CAGR sebelum gate dinilai (spec §4.1); grid dan
  gate tidak diubah selepas itu.
