# Lift MASUK setiap kaedah (gate G3)

Dijana 2026-11-08 05:15 UTC oleh `standard/lift_kaedah.py` (Actions `analisis.yml`). Pradaftar: `standard/SPEC_KAD_SKOR.md` pindaan 7 Nov 2026. Rekod analisis sahaja: tiada order, tiada wang sebenar.

## Apa yang diukur

Adakah kaedah ini memilih saham yang lebih baik daripada saham lain yang dibeli Lejar **pada hari yang sama dan tahap turun-naik (tercile ATR) yang sama**? Pulangan diukur pada ufuk TETAP 10 sesi (buka hari beli → tutup sesi ke-10, kos 0.2%), jadi peraturan keluar TIDAK mempengaruhi nombor ini. Nilai keluar diukur oleh G2 (buku harian) dan G6 (portfolio).

Versi lama (padanan baldi hari pegang, SE ikut hari beli) dibuang kerana ia meluluskan belian RAWAK: henti + sasaran rawak mendapat lift +2.17 mata, dan SE lama meluluskan plasebo sehingga 51% masa. Reka bentuk ini lulus plasebo pada kadar 1.9–3.4% (`laporan/PLASEBO_GATE.md`).

## Data

Hari beli LANGSUNG sahaja (Mxx sejak isyarat 2026-10-15, Nxx/GB sejak 2026-11-03). **11,353 saham-hari** dengan ufuk 10 sesi lengkap, 7 hari beli, 121 kaedah. Rejim (QQQ > SMA50 dan SMA10 > SMA20) pada hari beli ini: ON 1 · OFF 6.

## Keputusan

Diuji (≥ 30 saham-hari, ≥ 5 minggu): **0** kaedah. Lift positif lulus BH-FDR: **0**. Lift negatif lulus BH-FDR: **0**.

**Belum ada kaedah yang cukup data untuk diuji.** Ufuk 10 sesi dan hari beli langsung bermakna ujian pertama memerlukan ~5 minggu data langsung. Ini disengajakan: tiada jawapan lebih baik daripada jawapan palsu.

## Bila jadual ini boleh dipercayai

Hari beli diperlukan untuk melihat lift 2 mata merentas kaedah diuji: **–** (dikira semula setiap larian). Ada 7. Kad skor juga mewajibkan ≥ 10 hari beli dalam setiap rejim (G1), supaya keputusan tidak datang daripada satu fasa pasaran.

## Had

- Lift ialah kemahiran MASUK relatif kepada saham lain yang Lejar beli, bukan pulangan akaun.
- Kolam ialah alam Lejar (saham patuh Syariah ≥ USD10), bukan seluruh pasaran.
- Sasaran +10%/bulan tidak boleh dibaca daripada jadual ini (`REVERSE/SASARAN.md`).
