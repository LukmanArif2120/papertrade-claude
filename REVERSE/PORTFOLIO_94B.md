# Portfolio 94 — larian B (tiga kecacatan dibetulkan, jalur benih)

Pradaftar `REVERSE/SPEC_PORTFOLIO_94B.md` — dikomit sebelum keputusan dilihat.
Penanda aras SPUS: CAGR +17.95%  MDD -26.82%  nisbah 0.669
Semakan §2(a): Spearman `U14` lawan `U02` = **0.7185** (< 0.99, jadi `U02` bukan pendua seperti dalam larian A).

## Jalur benih setiap lengan (20 benih)

| Lengan | Slot | Urutan | CAGR p5 | CAGR median | CAGR p95 | MDD median | Nisbah median | Dedah |
|---|---|---|--:|--:|--:|--:|--:|--:|
| P94 | 8 | U01 | -10.01% | **+7.72%** | +20.30% | -55.75% | 0.15 | 97% |
| P94 | 8 | U02 | +19.80% | **+19.80%** | +19.80% | -83.25% | 0.24 | 92% |
| P94 | 8 | U08 | +12.17% | **+12.17%** | +12.17% | -39.31% | 0.31 | 98% |
| P94 | 8 | U14 | +11.65% | **+11.65%** | +11.65% | -69.41% | 0.17 | 90% |
| P94 | 40 | U01 | +5.07% | **+10.02%** | +25.62% | -45.83% | 0.21 | 98% |
| P94 | 40 | U02 | -3.85% | **-3.85%** | -3.85% | -86.69% | -0.04 | 96% |
| P94 | 40 | U08 | +6.88% | **+6.88%** | +6.88% | -36.20% | 0.19 | 99% |
| P94 | 40 | U14 | +16.46% | **+16.46%** | +16.46% | -75.69% | 0.22 | 96% |
| PENUH | penuh | U14 | +16.00% | **+16.00%** | +16.00% | -68.42% | 0.23 | 100% |
| RAWAKALAM | 8 | U14 | -5.52% | **+2.70%** | +10.64% | -78.38% | 0.03 | 94% |
| RAWAKALAM | 40 | U14 | +9.51% | **+18.77%** | +22.88% | -71.91% | 0.26 | 96% |

## Gate (median lengan; P3 = median P94 > p95 RAWAKALAM slot sama)

| Lengan | Slot | Urutan | P1 | P2 | P3 | P4 | T1 |
|---|---|---|:-:|:-:|:-:|:-:|:-:|
| P94 | 40 | U01 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P94 | 40 | U02 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P94 | 40 | U08 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P94 | 40 | U14 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P94 | 8 | U01 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P94 | 8 | U02 | ✓ | ✗ | ✓ | ✗ | ✗ |
| P94 | 8 | U08 | ✗ | ✗ | ✓ | ✗ | ✗ |
| P94 | 8 | U14 | ✗ | ✗ | ✓ | ✗ | ✗ |
| PENUH | penuh | U14 | ✗ | ✗ | ✗ | ✗ | ✗ |

## Tafsiran

### Jangkaan priori §7 #1 — yang paling saya yakin — SALAH

Saya menulis: *"`P3` GAGAL — isyarat tidak mengalahkan masuk rawak yang dipadankan ... Ini
jangkaan yang paling saya yakin dalam spec ini."*

**Ia lulus pada 8 slot, pada 3 daripada 4 pemeringkat.** Jalur `RAWAKALAM` 8 slot ialah
p95 **+10.64%**; `U14` beri **+11.65%**, `U08` **+12.17%**, `U02` **+19.80%** — ketiga-tiganya
di atas p95. Hanya `U01` (susunan rawak) gagal, dan itu memang sepatutnya kerana ia bukan
pemeringkat.

Jadi pada kepekatan tinggi, **isyarat masuk MEMANG menambah sesuatu** atas cabutan rawak
daripada alam cair yang sama, dengan kolam, kiraan/hari, taburan keluar dan pemeringkat
semuanya dipadankan. Itu ujian isyarat pertama dalam repo yang kawalannya benar-benar
dipadankan, dan ia memihak isyarat.

**Pada 40 slot ia gagal pada KEEMPAT-EMPAT pemeringkat.** Jalur `RAWAKALAM` 40 slot ialah
p95 **+22.88%** dan tiada lengan `P94` melepasinya (terbaik `U14` +16.46%). Masuk rawak
bertambah baik jauh lebih cepat dengan slot (+2.70% → +18.77% median) daripada isyarat
(+11.65% → +16.46%).

Mekanismenya konsisten dengan kolam 1,060× slot: pada 8 slot, pemeringkat memilih 8 teratas
daripada 8,476 dan **had kolam** yang isyarat kenakan masih penting; pada 40 slot kolam
rawak sudah cukup besar untuk memberi hasil yang sama. Kelebihan isyarat ialah kesan
KEPEKATAN, dan ia hilang apabila kepekatan dilonggarkan.

### Yang tidak berubah, kini dengan 201 larian dan jalur benih

**P2 = 0/9.** MDD median −36.20% (terbaik) hingga −86.69% (terburuk) lawan SPUS −26.82%.
Pendedahan 90–100% setiap lengan. **P4 = 0/9**, nisbah terbaik **0.31** lawan 0.669.
**T1 = 0.** Kohort 94 bukan peruntukan modal, dan itu kini kukuh merentas 4 pemeringkat,
2 saiz slot, kolam penuh dan 20 benih.

**P1 = 1/9**: `U02` 8 slot +19.80% melepasi SPUS +17.95% — tetapi MDD **−83.25%**, kedua
terburuk dalam jadual. CAGR tanpa MDD bukan keputusan.

### Pemeringkat: `U08` mengalahkan `U14` dengan margin yang MELUAS, bukan mengecil

Jangkaan priori §7 #2 saya berkata jurang `U08` lawan `U14` akan **lebih kecil** dengan
jalur benih. Ia **lebih besar**:

| Pemeringkat | Slot | CAGR | MDD | Nisbah |
|---|---|--:|--:|--:|
| `U08` ATR% songsang | 8 | +12.17% | **−39.31%** | **0.31** |
| `U14` momentum 12−1 | 8 | +11.65% | −69.41% | 0.17 |
| `U08` | 40 | +6.88% | **−36.20%** | 0.19 |
| `U14` | 40 | +16.46% | −75.69% | 0.22 |

Pada 8 slot `U08` lebih baik pada **kedua-dua** paksi: MDD **30 mata** lebih cetek pada CAGR
lebih tinggi, nisbah hampir dua kali. Pada 40 slot ia menukar 9.6 mata CAGR untuk **39 mata**
MDD.

**Jalur benih pemeringkat determinan ialah SIFAR** (p5 = median = p95 bagi `U02`, `U08`,
`U14`) — benih hanya memecah seri, dan seri tidak pernah menentukan. Jangkaan priori #3
betul, dan itu bermakna perbandingan pemeringkat di sini **boleh dipercayai**, tidak seperti
perbandingan CAGR mutlak yang `U01` tunjukkan berjulat 30 mata.

**`U02` (momentum 6−1) ialah yang paling berbahaya**: CAGR terbaik pada 8 slot (+19.80%)
tetapi MDD terburuk (−83.25%), dan pada 40 slot ia **negatif** (−3.85%, nisbah −0.04).
Momentum jangka lebih pendek memilih nama yang jatuh paling keras.

### `PENUH` dengan pecahan TETAP — ujian `SZ10` yang sah

+16.00%, MDD −68.42%, pendedahan 100%, 62,266 dagangan. Gagal P1 dan P2. Jangkaan priori #4
betul: ia tidak mengalahkan 40 slot. Jadi `SZ10` ("pegang kolam penuh") **tidak** menyelamatkan
kohort ini, dan kini itu diukur dengan saiz yang betul, bukan dengan saiz yang berayun 2.7×
seperti larian A.

## Kesan kepada produksi

Produksi memakai `rank = U14` pada kesemua 94 modul. Larian ini mengukur `U08` lebih baik
pada kedua-dua paksi pada 8 slot dan **39 mata MDD lebih cetek** pada 40 slot, dengan jalur
benih sifar pada kedua-duanya. Itu dapatan yang boleh ditindaklanjuti — tetapi ia diukur pada
alam `AL01` yang **tiada delist**, dan Papertrade C/Lejar Penuh membeli SETIAP isyarat tanpa
had slot, jadi pemeringkat tidak menyekat apa-apa dalam Lejar. Pemeringkat hanya penting
apabila slot mengikat (`portfolio_slot/`, 10 slot). Jadi: **jangan tukar `rank` dalam 94
modul atas larian ini sahaja**; ia memberi sebab yang kukuh untuk mengukur `U08` sebagai
lorong `portfolio_slot` baharu, di mana slot benar-benar mengikat.

## Syarat BERHENTI §8 — tidak dicetus

Spec §8: *"Jika `P3` gagal pada kedua-dua slot: ruang isyarat masuk untuk portfolio ditutup
secara muktamad."* `P3` **lulus** pada 8 slot, jadi syarat itu tidak dicetus dan ruang itu
**tidak** ditutup. Tetapi spec juga berkata jika `P3` lulus ia mesti diulang pada alam
`AL02`, kerana E4 mengukur `AL02` menyanjung MDD sebanyak 30.9 mata berbanding `AL04`
titik-masa. Itu syarat yang belum dipenuhi, jadi dakwaan "isyarat mengalahkan rawak" kekal
**bersyarat kepada alam tanpa delist**.
