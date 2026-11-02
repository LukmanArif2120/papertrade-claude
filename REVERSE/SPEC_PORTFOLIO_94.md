# Pradaftar — portfolio 94 kombinasi produksi lawan SPUS

**Dikomit sebelum sebarang keputusan dilihat.** 2 Nov 2026.
Kod: `REVERSE/step33_portfolio_94.md` → `REVERSE/step33_portfolio_94.py`.
Keluaran: `REVERSE/PORTFOLIO_94.md`, `REVERSE/portfolio_94.csv`.

## 1. Mengapa larian ini perlu wujud

`REVERSE/portfolio_n_ringkas.csv` (36 konfigurasi, 264 larian) ialah satu-satunya ujian
portfolio yang pernah dijalankan pada kohort Nxx, dan ia menguji `GB02_atau3`,
`GB02_atau4` dan `RAWAK` — **bukan** 94 kombinasi yang kini dalam produksi.

Grid penuh 1,495 sel memangkatkan `GB02_atau3 × X13` pada **7 daripada 1,496**, dan ia
dikalahkan oleh **dua kaki tunggalnya sendiri**. Kohort produksi mengandungi sel pangkat
**1–139**, termasuk `N124X15` jangkaan tahan **+16.127%** dan `N19X13` **+11.285%** lawan
`GB02_atau3 × X13` **+8.541%**.

Jadi ayat "portfolio GAGAL 0/36, jadi ini kohort setiap dagangan bukan peruntukan modal"
ialah **kesimpulan tentang konfigurasi yang lemah yang dibawa kepada kohort yang lebih
kuat**. Itu kesilapan logik, bukan dapatan. Larian ini mengukur kohort yang sebenarnya
dijalankan.

**Ini BUKAN eksperimen ke-7.** Persetujuan "jangan tambah eksperimen ke-7" (sebelum E1)
ialah tentang **mencari** pembinaan portfolio yang mengalahkan SPUS. Larian ini tidak
mencari apa-apa yang baharu: ia mengukur tingkah laku portfolio bagi kohort yang **sudah**
dipilih dan **sudah** digabung ke `main`. Mengesahkan deliverable bukan memanjangkan
carian. Jika pengguna tidak bersetuju dengan perbezaan itu, hentikan larian ini.

## 2. Alam, kos, tingkap

Sama seperti `SPEC_PORTFOLIO_N.md` supaya nombor boleh dibanding terus:

- Alam `AL01` = cache `autotune-data-a02` (3,260 nama). **Tiada delist** — bias
  survivorship hadir dan tidak boleh dibetulkan dalam larian ini.
- Kos penuh `REVERSE/teras/kos.py` (komisen + spread ikut nilai dolar).
- Keputusan pada tingkap **TAHAN 2020-01-01 … 2025-12-31** (SPUS bermula Dis 2019).
  Tingkap latih 2012–2019 dilaporkan sebagai diagnostik, bukan gate.
- Penanda aras **SPUS**: CAGR **17.95%**, MDD **−26.82%**, nisbah **0.669**.
  Bukan SPY (`PENANDA_ARAS_SYARIAH.md`).

## 3. Unit posisi — keputusan yang mesti dinyatakan dahulu

Satu posisi = satu pasangan **(saham, keluar)**. Saham yang sama yang dicetus oleh dua
kombinasi dengan keluar BERBEZA ialah **dua** posisi; dicetus oleh dua kombinasi dengan
keluar SAMA ialah **satu**. Ini mencerminkan Lejar Penuh, di mana setiap ID memegang
posisinya sendiri.

Akibatnya mesti dinyatakan sekarang supaya ia tidak dibaca sebagai dapatan kemudian:
94 ID = **45 masuk** = **36 kelompok pertindihan** (`REVERSE/bertindih_kelompok.csv`),
faktor **2.6×**. `N42` muncul dengan 5 keluar; dua kelompok TREND memegang 7 masuk → 17 ID.
Jadi 94 **melebih-lebihkan** kepelbagaian, dan lengan dedup di §4 menguji berapa banyak
yang hilang bila pertindihan itu dibuang.

## 4. Grid — tetap, tiada penalaan

| Lengan | Kolam calon | Slot | Urutan | Benih |
|---|---|---|---|---|
| `P94` | kesemua 94 (masuk, keluar) | 8, 40 | U14 | 1 |
| `P36` | 36 wakil kelompok (ID pangkat terbaik setiap kelompok) | 8, 40 | U14 | 1 |
| `PENUH` | kesemua 94, **tiada had slot**, berat sama rata | — | — | 1 |
| `RAWAK` | masuk rawak, bilangan/hari dipadankan dengan `P94` | 8, 40 | U01 | 20 |
| `U-KAWAL` | kesemua 94 | 8 | U01, U02, U08 | 20 (U01) |

= 2 + 2 + 1 + 2×20 + 3 = **jumlah 50 larian simulasi**.

Keluar dilaksanakan dalam enjin portfolio: `X13` rsi14 > 70 · `X14` rsi14 silang naik 50 ·
`X15` Chandelier tutup 4×ATR14 · `X16` supertrend berbalik · `X17` adx14 < 20 ·
`X36` dua tutup bawah ma50. Kesemuanya jual pada **buka esok**, had imbasan 504 bar,
`TMAX` 126 bar. Cara `C01` sahaja (paksi CARA kekal tidak diuji untuk kohort ini).

## 5. Gate — ditetapkan sekarang, tidak boleh dilonggarkan selepas keputusan dilihat

- **P1** CAGR tahan > **17.95%**
- **P2** MDD tahan ≥ **−26.82%**
- **P3** CAGR > persentil-95 jalur `RAWAK` pada slot yang sama
- **P4** nisbah CAGR ÷ |MDD| > **0.669** (`SISTEM.md`: campuran SPUS+tunai hampir pemalar
  0.642–0.669 merentas setiap berat, jadi apa-apa di bawah 0.669 dikalahkan oleh SPUS+tunai
  pada pendedahan yang sama)
- **T1** = P1 **DAN** P2 serentak
- **T3** = CAGR ≥ 15% dengan MDD ≥ −15%

Gate dinilai pada tingkap TAHAN sahaja. `P3` memerlukan jalur rawak 20 benih; satu cabutan
rawak tidak mencukupi (`KEPEKATAN_BENIH.md`: SD hingar pemilihan 4.15 mata/tahun, ambang
95% 9.7 mata antara dua susunan tunggal).

## 6. Dapatan yang mesti dilaporkan tanpa mengira keputusan

1. CAGR, MDD, nisbah, pendedahan purata, bilangan dagangan, setiap lengan.
2. `P94` lawan `P36` — jika beza < jalur benih rawak, pertindihan 2.6× itu **tidak**
   menambah apa-apa dan 94 patut dilaporkan sebagai ~36 pertaruhan.
3. `PENUH` lawan 8/40 slot — menguji semula `SZ10` pada kohort ini (`KOLAM_EKOR.md`:
   kolam penuh +1.64%/bulan lawan saham median +0.82%).
4. `U14` lawan `U01`/`U02`/`U08` — sama ada pemeringkat yang dipilih tanpa ujian memang
   betul.
5. Pendedahan purata. Jika ia jauh di bawah 100%, MDD yang cetek ialah kesan **pendedahan**
   bukan kemahiran — kesilapan tepat yang Sistem B Clenow buat (`SISTEM.md`: 35.4%
   pendedahan, dan SPUS mengalahkannya pada pendedahan sama pada KEDUA-DUA paksi).

## 7. Jangkaan priori saya — direkod sebelum larian

Rekod saya: salah pada 2/3 gate dalam `SPEC_NXX`, salah arah bertentangan dalam
`SPEC_SISTEM`, dan salah pada had 40 dalam sesi ini. Jadi ini ditulis untuk disemak, bukan
untuk dipercayai.

1. **P1 LULUS pada 40 slot, GAGAL pada 8.** E1 mengukur 80 slot pada +39.24% dengan masuk
   yang lebih lemah; jangkaan setiap dagangan di sini lebih tinggi.
2. **P2 GAGAL pada setiap lengan.** Portfolio ekuiti panjang-sahaja 100% melabur tidak boleh
   mempunyai MDD lebih cetek daripada indeks ekuiti melainkan ia memegang tunai — itu
   struktur, bukan parameter, dan ia bertahan merentas 724 konfigurasi E1–E6.
3. **T1 = 0.** Akibat (1) dan (2).
4. **`P36` ≈ `P94`** dalam jalur benih. Jika benar, 94 ialah ~36 pertaruhan dan laporan
   mesti berkata begitu.
5. **`PENUH` mengalahkan 8 slot pada CAGR** tetapi MDD lebih dalam.
6. **`U14` mengalahkan `U01`** tetapi kurang daripada jalur benih rawak, jadi pilihan
   pemeringkat itu tidak dapat dibenarkan oleh larian ini.

## 8. Syarat BERHENTI

Jika T1 = 0 **dan** `P36` ≈ `P94`, maka: kohort ini ialah kohort **setiap dagangan** sahaja,
94 dilaporkan sebagai ~36 pertaruhan bebas, dan `T4` (SPUS + tunai) kekal cadangan modal.
Tiada larian portfolio lanjut untuk Nxx tanpa keputusan pengguna.

Jika ada lengan melepasi T1, ia mesti diulang pada alam `AL02` (keahlian SPUS) sebelum
sebarang dakwaan dibuat, kerana E4 mengukur `AL02` menyanjung MDD sebanyak **30.9 mata**
berbanding alam titik-masa `AL04` yang kausal.
