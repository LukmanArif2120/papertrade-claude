# Pradaftar — semakan pemalsuan LUAR SAMPEL bagi dua dapatan pembinaan

Ditulis dan dikomit **sebelum** sebarang keputusan latih dilihat. Skrip: `step28_korelasi.py`
dan `step29_hierarki.py` (grid, benih dan enjin **tidak berubah**; satu lajur keluaran
ditambah). Keluaran: `REVERSE/SEMAKAN_LATIH.md`.

## 1. Ini BUKAN eksperimen ke-7

`STRATEGI.md` §3 menetapkan, dan pengguna persetujui sebelum E1: selepas `BERHENTI–TUTUP`,
**tiada eksperimen ke-7 ditambah selepas melihat keputusan E1–E6.** Peraturan itu dibuat
untuk menghentikan carian sistem yang menang tanpa penghujung.

Semakan ini **tidak mencari apa-apa**. Ia menjalankan **grid yang sama**, **konfigurasi yang
sama**, **benih yang sama**, pada **tingkap yang lain**, untuk menguji dua dakwaan yang
**sudah diterbitkan**. Ia tidak boleh menghasilkan kelulusan T1/T3 baharu — ia hanya boleh
**melemahkan** dakwaan sedia ada. Itu pemalsuan, bukan carian, dan repo sudah pernah
menjalankannya (`NXX.md` "semakan pemalsuan").

Jika pengguna mahu peraturan ke-7 ditafsirkan lebih ketat daripada ini, semakan ini dibuang
dan dakwaan sedia ada dilabel "tidak pernah disemak luar sampel".

## 2. Dua dakwaan yang diuji

Kedua-duanya diukur pada tingkap **TAHAN 2020–2025** sahaja, dan kedua-duanya disenaraikan
dalam `KEPUTUSAN_AKHIR.md` §3 sebagai "dapatan yang BERTAHAN":

**Dakwaan A (E5, `KORELASI.md`):** had 1 pegangan setiap industri memperbaiki **kedua-dua**
paksi — median **+1.65 mata CAGR** dan **+1.60 mata MDD** lebih cetek, lawan tiada had pada
sel sepadan. Had 2 memberi +0.76/+0.02; had 3 memberi +0.47/+0.00.

**Dakwaan B (E6, `HIERARKI.md`):** saringan **berdiri** memperbaiki kedua-dua paksi —
median Δ CAGR / Δ MDD: `A1` +1.67/+1.47 · `A2` +4.26/+0.94 · `A3` +6.29/+0.23. (`A4`
volatiliti rendah ialah pertukaran tulen dan **bukan** sebahagian dakwaan ini.)

## 3. Apa yang berubah dalam kod

Satu perkara sahaja: `mdd_latih` ditambah kepada keluaran. `cagr_latih` sudah direkod;
`mdd_latih` tidak, dan tanpa ia kaki MDD — iaitu separuh penting kedua-dua dakwaan — tidak
boleh disemak.

Grid, benih, alam, kos, enjin dan gate **tidak disentuh**. Kawalan regresi: nilai `cagr` dan
`mdd` tingkap tahan mesti dihasilkan semula **identik** dengan larian asal, kerana tiada
apa-apa yang mempengaruhinya berubah. Jika ia tidak identik, larian dibuang dan sebabnya
disiasat sebelum apa-apa dilaporkan.

## 4. Syarat lulus — ditetapkan sekarang

Bagi setiap dakwaan, pada tingkap **LATIH 2012–2019**, pada sel sepadan yang **sama**:

- **R1 (tanda)** — median Δ CAGR dan median Δ MDD mesti mempunyai **tanda yang sama**
  seperti dalam tahan (iaitu kedua-duanya positif) bagi sekurang-kurangnya **satu** aras
  had (Dakwaan A) dan sekurang-kurangnya **satu** saringan `A1`–`A3` (Dakwaan B).
- **R2 (bukan cabutan)** — bahagian sel yang MDD-nya mencetek mesti ≥ **50%** dalam latih,
  ambang yang sama seperti `E5a-MDD`.

| R1 | R2 | Keputusan |
|---|---|---|
| ya | ya | **DISAHKAN.** Dakwaan bertahan luar sampel; ia kekal dalam `KEPUTUSAN_AKHIR.md` §3 sebagai dapatan. |
| ya | tidak | **LEMAH.** Tanda bertahan tetapi tidak konsisten. Dakwaan dilabel semula sebagai "diukur pada 2020–2025 sahaja; tanda bertahan dalam latih tetapi di bawah separuh sel". |
| tidak | — | **DIPALSUKAN.** Dakwaan ditarik balik daripada `KEPUTUSAN_AKHIR.md` §3 dan dilabel artifak tingkap. Laporan asal **tidak** dipadam; pembetulan ditulis di atasnya. |

Penarikan balik ditulis ke `KEPUTUSAN_AKHIR.md`, `KORELASI.md`/`HIERARKI.md`, registry dan
`CLAUDE.md` — di setiap tempat dakwaan itu dibuat.

## 5. Jangkaan priori — ditulis sebelum melihat sebarang nombor latih

1. **Kaki MDD Dakwaan A DISAHKAN.** Had industri ialah kawalan kepekatan mekanikal; ia
   sepatutnya mencetekkan MDD dalam mana-mana tingkap. Keyakinan tinggi.
2. **Kaki CAGR Dakwaan A LEBIH LEMAH dalam latih, dan mungkin negatif.** +1.65 mata itu
   yang paling mengejutkan dalam E5, dan saya tidak mempunyai mekanisme yang kukuh
   untuknya. 2020–2025 mempunyai kepimpinan teknologi yang sempit, jadi mengehadkan
   industri sepatutnya **merugikan** pulangan pada tingkap itu — ia tidak, dan itu
   mencurigakan. Saya mengesyaki ia didorong oleh pengelakan drawdown 2022, yang tiada
   analog dalam 2012–2019.
3. **Dakwaan B bertahan pada CAGR tetapi lebih lemah pada MDD.** Saringan `A2`/`A3` ialah
   saringan momentum/RS, dan momentum ialah salah satu daripada sedikit kesan yang
   berulang merentas tingkap. Kaki MDD-nya kecil dalam tahan (+0.94/+0.23), jadi ia mudah
   bertukar tanda.
4. **Keseluruhan: satu daripada dua dakwaan akan turun kepada LEMAH atau DIPALSUKAN.**

Rekod saya merentas enam pradaftar ialah **15 betul, 3 separa, 13 salah**, jadi jangkaan ini
dicatat supaya kesilapan boleh dikira — bukan kerana ia patut dipercayai.

## 6. Had

- Tingkap latih 2012–2019 ialah **satu** tingkap, bukan pengesahan merentas rejim.
- Alam, kolam signal dan ambang saringan masih dipilih daripada data yang sama; semakan ini
  membetulkan **tingkap**, bukan **pemilihan**.
- `AL04` membetulkan keahlian tetapi bukan delist; alam asas `a02` tiada saham delist dalam
  kedua-dua tingkap.
- Ini **tidak** menguji dakwaan itu pada populasi **Mxx**. Lejar Penuh hanya mengandungi 11
  sesi isyarat Mxx (15–28 Okt 2026) dan tiada matriks isyarat Mxx bersejarah di cakera,
  jadi ujian populasi-silang memerlukan penjanaan semula 136 modul kaedah merentas 14 tahun
  — kerja berasingan yang tidak dijalankan di sini.
