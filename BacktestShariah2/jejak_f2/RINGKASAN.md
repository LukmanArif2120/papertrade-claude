# Papertrade setup F gred A (maya; BUKAN keputusan wang sebenar)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_hadapan19.py`; harga hingga 20261113. Peraturan: `kajian/SPEC_CARIAN_SETUP.md pindaan 16 Nov 2026 (ae) Bahagian D + pindaan 17 Nov 2026 (af)`. Tiada order. **Jangan sunting.**

## Hari ini

- Hari diproses: 1 (mula 20261113); terlepas dan diisi lewat: 0.
- Setup yang syarat pasarannya benar hari ini: 3 daripada 29 (`F200`, `F833`, `F1354`).
- Syarat pasaran: QQQ OFF = YA; SPY atas SMA200 = YA; QQQ dalam 3% dari puncak 52 minggu = tidak; rejim OFF baharu (<= 10 sesi) = tidak; QQQ naik >= 3% dalam 5 sesi = YA; keluasan naik >= 10 mata dalam 10 sesi = tidak; >= 60% saham di atas MA200 = tidak; >= 15% saham dalam 5% dari puncak 52 minggu = tidak; Mei-Okt = tidak; nisbah 4% (10 hari) > 2 = tidak; nisbah 4% (10 hari) < 0.5 = tidak; hari 90% turun kemudian naik (20 sesi) = tidak.
- Saham layak yang laporannya dalam 1–5 sesi: 85.

## Belian esok (isyarat hari ini; beli pada harga buka sesi berikutnya)

Tiada.

## Hasil setakat ini (isyarat tidak lewat; kurungan = saham rawak hari sama, dipegang cara sama)

| Kumpulan | Belian | Belum ditutup | Tetingkap 20 sesi lengkap | Tangkap % | Naik ≥ 5 % | Jatuh ≥ 5 % | Menang % cara B | Purata % cara B | Menang % cara 50 | Purata % cara 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Semua 29 setup (belian unik)** | 0 | 0 | 0 | – (–) | – (–) | – (–) | – (–) | – (–) | – (–) | – (–) |
| Kawalan: laporan 1–5 sesi, tiada isyarat beli | 85 | 85 | 0 | – (–) | – (–) | – (–) | – (–) | – (–) | – (–) | – (–) |

## Bacaan dikunci

**Belum cukup:** 0 daripada 300 belian unik dengan tetingkap 20 sesi lengkap. Angka di atas belum boleh dibaca.

## Cara baca

- Tangkap = naik ≥ 5 % minggu pertama DAN naik lagi hingga minggu ke-4 tanpa jatuh 8 %. Naik / Jatuh ≥ 5 % = pada tutup sesi ke-5.
- Cara B = pegang sekurang-kurangnya 20 sesi, kemudian jual selepas tutup di bawah purata 20 hari (paling lama 126 sesi). Cara 50 = yang sama dengan purata 50 hari, tiada had masa. Stop loss 4×ATR14 pada kedua-duanya; kos 0.5 %.
- Dagangan yang belum ditutup dinilai pada harga tutup terkini; cara yang sama bagi saham rawak.
- Tarikh laporan = seperti diketahui pada hari isyarat (`isyarat.csv`, tidak pernah dikira semula). Alam: semua saham alam backtest (3,260 saham; 2,000 paling cair setiap bulan), BUKAN senarai Shariah sahaja; saham layak hari ini: 1992; harga diperoleh bagi 3242 daripada 3260 saham.
- Kebanyakan setup hanya aktif dalam keadaan pasaran tertentu dan pada musim laporan kewangan; hari tanpa belian adalah biasa.
