# SPEC — Bolehkah "sejauh mana saham akan naik" diramal? (paksi EKOR)

## STATUS: DITARIK BALIK 1 Nov 2026, SEBELUM DIJALANKAN — PENDUA `L99`

Pradaftar ini ditulis pada 1 Nov 2026 sebagai jawapan kepada soalan pengguna: "boleh tak
[jalur] digunakan utk predict momentum, sejauh mana saham akan naik, possible tak? utk
setiap saham."

Ia **ditarik balik sebelum sebarang keputusan dijana**. Sebabnya: `REVERSE/L99.md` +
`REVERSE/SPEC_L99.md` dikomit ke `main` pada hari yang sama (`e897a8a`) dan sudah menjawab
soalan teras ini dengan reka bentuk yang **lebih baik** daripada yang di bawah. Sesi ini
bermula daripada HEAD terpisah sebelum komit itu, jadi L99 tiada dalam pokok kerja dan
tidak kelihatan semasa pradaftar ini ditulis.

Fail ini dikekalkan sebagai rekod "jangan ulangi", bukan sebagai rancangan.

### Apa yang L99 sudah ukur, yang menjadikan spec ini pendua

Hipotesis utama di bawah ialah: peramal skala akan meramal MFE **dan** MAE hampir simetri,
jadi ia mengukur volatiliti dan bukan arah (gate3). **L99 §2c sudah mengukur tepat itu dan
keputusannya muktamad:**

- `C1 ATR% tertile teratas` memberi ΔP(trend besar) **+23.72 mata** — kesan terbesar dalam
  seluruh kajian repo — dan `C2 ATR% tertile terbawah` memberi **−23.90 mata**. Hampir
  simetri sempurna.
- Dengan sasaran dinormal volatiliti (`mx120 ÷ ATR%`), **8 daripada 8** pattern menukar tanda
  atau berubah besar; kesan runtuh kepada ±3–6 mata.
- Ayat L99: **"Volatiliti mentah bukan pattern; ia unit ukuran."**

L99 juga sudah menjalankan, pada 763,327 dagangan enjin + alam A02 penuh:
- sasaran "keahlian ekor" (`mx120/buka − 1 ≥ 0.30`) = MFE berambang — kuantiti yang sama;
- urutan lawan penapis lawan kesatuan (urutan +0.520 · penapis +0.034 · kesatuan +0.015);
- diagnostik portfolio 8/40 slot lawan SPUS;
- sapuan parameter keluar (ganda ATR 1.5× hingga 12×);
- audit enam agen yang menangkap satu pepijat MAUT (`float NaN .astype(bool)` → `True`).

### Apa yang spec ini akan tambah, dan mengapa ia tidak berbaloi

Bezanya hanya **penghuraian**: spec ini mengukur MFE dan MAE sebagai dua sasaran berterusan
berasingan dan menguji asimetri secara langsung, manakala L99 **menormalkan** dengan ATR%
dan menyimpulkan daripada keruntuhan kesan. Kedua-duanya sampai ke jawapan yang sama melalui
jalan berbeza. Penghuraian akan memperhalusi mekanisme; ia **tidak** akan menukar kesimpulan,
kerana kesimpulan itu sudah ±23.7 mata simetri dan runtuh ke ±3 selepas normalisasi.

Menjalankannya bermakna membelanjakan beberapa jam untuk menghasilkan semula dapatan yang
sudah ada dengan jentera berbeza. Itu bukan pengesahan bebas — ia alam yang sama, konvensyen
yang sama dan pengarang yang sama.

### Yang BELUM dijawab oleh L99 (jika hendak diteruskan, pradaftar semula)

1. **Lebar jalur, bukan pusat jalur.** L99 menjawab "boleh tak ramal arah/magnitud" = tidak.
   Ia tidak menanya "boleh tak ramal **ketidakpastian**". Pengelompokan volatiliti bermakna
   lebar taburan hadapan memang boleh diramal — itu sebenarnya sebab `C1`/`C2` memberi
   ±23.7 mata. Itu bukan alfa dan tidak boleh didagangkan, tetapi ia **paparan jujur**
   setiap saham.
2. Penguraian MFE/MAE eksplisit (di bawah, §4–§5) sebagai semakan bahawa normalisasi ATR%
   ialah pelarasan yang betul — nilai metodologi, bukan nilai dagangan.
3. L99 §2f "perangkap pangkat #1" diukur pada tiga skor sahaja; sama ada ia am belum diuji.

### Apa yang KEKAL berguna daripada kerja ini

`REVERSE/step22_ekor.py` dikekalkan. Ia membina panel setiap bar dengan **MFE, MAE dan
pulangan terminal berterusan** pada ufuk 21 dan 63 hari (L99 hanya ada sasaran berambang
120 bar). Panel itu ialah input yang betul bagi perkara (1) di atas — jalur ketidakpastian
setiap saham untuk dashboard — dan bagi apa-apa kerja MFE/MAE kemudian. `gate0()` di dalamnya
melaksanakan ujian asap **kombinasi** yang `L99 §8a` dapati hilang daripada L99 sendiri
(dua daripada lima ujian asap L99 adalah vakum: `hari < 1` dan `(j_keluar == k) & (kod == 1)`
kedua-duanya mustahil mengikut pembinaan).

---

## Rekod reka bentuk asal (TIDAK dijalankan)

Dikekalkan di bawah supaya sesiapa yang terfikir soalan ini sekali lagi nampak ia sudah
difikirkan, dan nampak mengapa ia tidak dijalankan.

**Alam.** A02, 2012–2025, bar cair `nilai20 ≥ USD100,000`, LATIH 2012–2019 / TAHAN 2020–2025.

**Sasaran §4.** Masuk buka `t+1`, ufuk H ∈ {21, 63}: `mfe_hi`, `mfe_cl`, `mae_lo`, `mae_cl`,
`term`, dan `asim = mfe_cl + mae_cl` sebagai metrik kepala.

**Peramal §5.** 22 lajur, empat keluarga — SKALA (8), SEJARAH-EKOR (4), TREND (6), CAIR/SAIZ (4).

**Gate §6.** gate0 asap kombinasi · gate1 Fama–MacBeth Spearman dalam tarikh · gate2 TAHAN ·
gate3 bukan-sekadar-volatiliti · gate3b cabang keluar · gate4 jangkaan mutlak > 0 + BH-FDR ·
gate5 portfolio lawan SPUS, nisbah `CAGR ÷ abs(MDD)` > 0.669.

**Jangkaan priori §7 (direkod sebelum penarikan balik, dan kini boleh dinilai terhadap L99):**
saya meramalkan keluarga SKALA lulus gate1 dengan kuat lalu **gagal gate3 kerana ia volatiliti
tulen**, dan 0 daripada semua lulus kelima-lima gate. **L99 §2c mengesahkan ramalan itu** —
±23.72 lawan −23.90 mata ialah definisi simetri. Jadi untuk kali pertama dalam empat pradaftar
jangkaan priori saya betul pada perkara utama; tetapi ia betul tentang ujian yang **sudah
dijalankan oleh orang lain**, jadi ia bukan ramalan yang disahkan secara bebas.

### Dua kelemahan reka bentuk yang saya tangkap sendiri sebelum penarikan balik

1. `rs_pst` (pangkat `mom126` dalam tarikh) dan `rs_spy_6b` (tolak sebutan SPY yang **malar
   dalam tarikh**) kedua-duanya transformasi monotonik `mom126` dalam tarikh. Spearman
   keratan rentasnya **seiras**. Itu satu ujian, bukan tiga, dan `m = 132` terlebih kira.
2. gate5 membanding dengan SPUS sahaja. Ia mesti juga dibanding dengan **kolam penuh berat
   sama rata** (`KOLAM_EKOR.md`: +1.64%/bulan lawan saham median +0.82%), kerana apa-apa
   penumpuan di bawah kolam penuh kalah kepada kolam penuh melainkan peraturan pemilihannya
   ada lift-ekor positif — dan itulah yang diuji.

Kedua-duanya kekal sebagai nota bagi sesiapa yang menulis pradaftar seterusnya dalam ruang ini.
