# KORELASI — `KR03`: had bilangan pegangan setiap industri

> **PEMBETULAN 1 Nov 2026 — `SEMAKAN_LATIH.md`.** Dakwaan utama laporan ini, bahawa had
> industri memperbaiki **kedua-dua** paksi, **DIPALSUKAN** oleh semakan luar sampel. Kaki
> CAGR tidak bertahan dalam latih 2012–2019: had 1 memberi **−0.19** mata, bukan +1.65. Kaki
> MDD **bertahan** (+1.12, 83.3% sel). Baca laporan ini sebagai: **had industri ialah lever
> RISIKO yang hampir percuma, bukan lever dwi-arah.**
>
> **Semakan semula 1 Nov 2026 (`semak_latih.py`, ujian tanda berpasangan) menajamkannya
> lagi: +1.65 itu tidak pernah boleh dibezakan daripada sifar walaupun dalam tingkap ia
> diukur** — 16 daripada 24 sel positif, p = **0.152**. Jadi ia bukan kesan yang hilang di
> luar sampel; ia kesan yang tidak pernah ada. Kaki MDD sebaliknya **melepasi BH-FDR** pada
> tingkap luar sampel: +1.12 mata, 20/23 sel, p = **0.0005**. Laporan asal dikekalkan tanpa
> diubah di bawah supaya rekodnya utuh.

Pradaftar: `REVERSE/SPEC_KORELASI.md` (komit `26c135b`, sebelum larian).
Skrip: `REVERSE/step28_korelasi.py` · Data: `REVERSE/korelasi.csv`,
`REVERSE/korelasi_ringkas.csv`

96 konfigurasi pada **`AL04` titik-masa** (214 dan 500 teratas ikut nilai dagangan 20 hari
pada sauh itu sendiri), `U01` 20 benih → 1,008 larian.

## Keputusan: T1 **0**, T3 **0** → teruskan ke E6. **`E5a` LULUS kedua-dua bahagian.**

| Gate | | |
|---|---|---|
| P1 | CAGR > 17.95% | 23 / 96 |
| P2 | MDD ≥ −26.82% | **0 / 96** |
| P3 | CAGR > p95 kawalan pangkat rawak | 24 / 96 |
| P4 | nisbah > 0.669 | 8 / 96 |
| **T1 / T3** | | **0 / 0** |
| **E5a-MDD** | had mencetekkan MDD pada ≥ 50% sel | **LULUS — 41/72 = 56.9%** |
| **E5a-NISBAH** | ada had menaikkan nisbah | **LULUS — 52/72 sel** |

`P2` gagal pada setiap sel untuk kali **kelima berturut-turut**. Tetapi MDD paling cetek
yang pernah diukur dalam baris gilir muncul di sini: **−28.97%**, hanya **2.15 mata**
daripada SPUS — walaupun CAGR-nya cuma +10.41%.

## Dapatan utama: had industri BUKAN pertukaran

Jangkaan priori saya #3 ialah `E5a-NISBAH` akan **gagal** — bahawa mengekang kepekatan akan
mengurangkan pulangan dan risiko bersama, jadi nisbahnya tidak berubah ("peruntukan tunai
dalam samaran", `SISTEM.md`). **Itu salah.**

Kesan median setiap had, lawan `tiada` pada sel sepadan:

| had maksimum setiap industri | Δ CAGR | Δ MDD (positif = lebih cetek) | Δ nisbah |
|---|---:|---:|---:|
| **1** | **+1.65** | **+1.60** | **+0.05** |
| 2 | +0.76 | +0.02 | +0.02 |
| 3 | +0.47 | +0.00 | +0.01 |

**Had 1 memperbaiki KEDUA-DUA paksi serentak.** Itu bukan pertukaran — ia kekangan yang
membayar. Dalam seluruh kajian ini, hampir setiap lever yang menaikkan pulangan menaikkan
risiko juga; ini yang pertama bergerak ke arah betul pada kedua-duanya.

Mekanismenya diukur dalam ujian asap sebelum larian: **tanpa had, 6 daripada 8 slot boleh
berada dalam SATU industri.** Portfolio "8 slot" itu sebenarnya ~3 taruhan. Had industri
memulihkan slot yang hilang itu, dan kerana kepekatan tidak dibayar pada tempoh ini, ia
tidak mengorbankan pulangan untuk melakukannya.

Saiznya kecil — **1.65 mata CAGR dan 1.60 mata MDD** — jadi ia komponen, bukan penyelesaian.
Ia direkod sebagai lever sah untuk mana-mana lorong hadapan.

## Dapatan E4 BERULANG pada alam kausal, dan lebih kuat

| alam | masuk | CAGR terbaik | MDD | nisbah |
|---|---|---:|---:|---:|
| `AL04` 500 | **`RAWAK`** (tiada isyarat) | **+49.55%** | −66.02% | 0.75 |
| `AL04` 500 | `GB02_atau3` (isyarat) | +11.98% | −37.03% | 0.32 |
| `AL04` 214 | **`RAWAK`** | **+34.78%** | −36.37% | 0.55 |
| `AL04` 214 | `GB02_atau3` | +12.92% | −28.97% | 0.37 |

Jurangnya **37.6 mata** pada alam 500. Pada alam yang keahlian**nya kausal** — bukan `AL02`
yang disanjung — isyarat masuk masih memusnahkan putaran berpangkat, dan lebih teruk
daripada yang E4 ukur.

Ini bukan lagi satu pemerhatian; ia keputusan yang **direplikasi pada dua alam bebas**:
**jangan tapis dahulu kemudian peringkat.** Pemeringkat memerlukan calon.

Satu nuansa yang jujur: lorong `GB02_atau3` mempunyai MDD **lebih cetek** (−28.97% lawan
−36.37%) — menapis memang mengurangkan risiko. Tetapi ia mengurangkan pulangan jauh lebih
banyak, jadi nisbahnya lebih rendah (0.37 lawan 0.55).

## Jangkaan priori lawan keputusan

| | Saya jangka | Berlaku | |
|---|---|---|---|
| (1) T1 = 0, T3 = 0 | ya | ya | **betul** |
| (2) `E5a-MDD` lulus | ya | 56.9% | **betul** |
| (3) `E5a-NISBAH` **gagal** | gagal | **LULUS, 52/72** | **salah** |
| (4) `RAWAK` > `GB02` berulang | ya | jurang 37.6 mata | **betul** |
| (5) had 1 = MDD paling cetek tetapi CAGR **paling rendah** | ya | MDD paling cetek **dan CAGR paling tinggi** antara ketiga-tiga had | **salah** |

Tiga betul, dua salah — dan kedua-dua yang salah salah ke arah yang **sama**: saya
memandang rendah had industri. Saya menjangkanya sebagai pertukaran kosong; ia ternyata
lever dwi-arah yang kecil tetapi nyata.

## Had

- `AL04` membetulkan keahlian tetapi **bukan** delist; alam asas `a02` tiada saham delist,
  jadi tiada alam dalam kajian ini bersih sepenuhnya.
- Peta industri ialah petikan **semasa**, bukan titik-masa (127 industri, 20 sektor; 665
  daripada 3,260 ticker tanpa industri, dikumpulkan sebagai satu kumpulan tertakluk had).
- `imbang` dikunci 63; interaksi had × kekerapan imbang tidak diuji.
- Hanya `U01` mempunyai jalur benih; `U02` satu cabutan tentu.
- Kesan had 1 ialah **median merentas 24 sel sepadan**; sebarannya tidak dilaporkan sebagai
  selang keyakinan dan tidak patut dibaca sebagai satu.
- Paksi `CARA` kekal `C01`.
