# Arahan: tulis semula hampir() dengan piawaian KETAT (90–100% entry)

Folder: /home/claude/scan. Setiap kaedah ada kaedah/Mxx.py (sedia + hampir) yang sudah PADAN dengan registry. Baca ANTARAMUKA.md dan spec kaedah (Projects: spec/Mxx_*.md atau `## SPEC Mxx` dalam KOMPILASI_KAEDAH_M01-M31.md; laporan/Mxx.md "Cara ujian"). JANGAN ubah sedia() atau logik isyarat; ubah HANYA fungsi hampir() (boleh tambah lajur pembantu bermula dengan `_` dalam sedia() jika perlu, asalkan sig/stop/tgt/exitc/rank tidak berubah).

## Piawaian baharu hampir(g, idx) — untuk bar terakhir
Pengguna mahu watchlist hanya calon yang memenuhi 90–100% syarat entry varian yang dipilih (VARIAN dalam modul):
1. Senaraikan SEMUA syarat entry varian itu (persediaan + penapis + pencetus), ikut kad spec dan laporan.
2. Kenal pasti PENCETUS: syarat terakhir yang menjadikan isyarat beli (cth. tutup > high 20 hari, silang MACD, lilin pembalikan, tutup > paras).
3. Pulangkan None jika:
   - sig bar terakhir sudah True (itu calon beli, bukan watchlist), ATAU
   - mana-mana syarat SELAIN pencetus tidak dipenuhi pada bar terakhir (termasuk penapis pasaran, penapis harga, volum, trend), ATAU
   - pencetus terlalu jauh: jarak > 2.0% (lihat 4).
4. Jarak pencetus:
   - Pencetus paras harga: jarak_pct = (paras − tutup)/tutup × 100 (untuk pecah ke atas); mesti 0 < jarak ≤ 2.0. Paras = nilai yang mesti dilepasi ESOK (kira dengan tetingkap yang akan digunakan esok).
   - Pencetus silang indikator (MACD, stokastik, EMA, DI): kira harga tutup esok yang diperlukan untuk silang berlaku (selesaikan secara algebra atau carian binari atas tutup esok, andaikan high/low = tutup jika perlu), kemudian jarak seperti di atas.
   - Pencetus volum: jika paras harga dekat (≤2%), nyatakan volum minimum yang diperlukan dalam syarat_beli.
   - Pencetus kalendar (rotasi hujung bulan/minggu/suku): semua syarat kelayakan dipenuhi hari ini DAN kedudukan dalam had pilihan (cth. rank ≤ bilangan slot) DAN tarikh rotasi seterusnya dalam ≤ 3 hari dagangan; jarak_pct = 0.
   - Pencetus corak satu hari (lilin pembalikan, jurang) yang tidak boleh diukur jarak: hanya masuk jika semua syarat lain dipenuhi dan pencetus boleh berlaku esok; nyatakan dengan tepat apa yang perlu berlaku; jarak_pct = null.
5. Pulangkan dict:
   {'sebab': 'BM baku: senarai ringkas syarat yang SUDAH dipenuhi (cth. "Power Trend aktif; EMA21 > SMA50 5 hari; SMA50 menaik")',
    'syarat_beli': 'BM baku: pencetus yang belum, dengan paras tepat (cth. "Tutup esok > 217.32 (high 20 hari)")',
    'pencetus': 'nama pendek pencetus', 'paras': nombor atau None, 'jarak_pct': nombor atau None,
    'syarat_dipenuhi': 'n/N' (n = syarat dipenuhi, N = jumlah syarat entry; n mesti N−1),
    'skor': 1 − jarak_pct/2 (atau 0.9 jika jarak None)}
6. Jangan reka syarat. Andaian ditulis sebagai komen `# Andaian saya:`.

## Semak
`cd /home/claude/scan && python3 uji_kaedah.py Mxx` — mesti kekal PADAN (sama seperti sebelum), dan lihat bilangan "hampir" (biasanya jauh lebih kecil daripada dulu). Pastikan tiada ralat.

Pulangkan hanya jadual: | ID | Pencetus | N syarat | Hampir (lama→baru) | Status uji | Catatan |
