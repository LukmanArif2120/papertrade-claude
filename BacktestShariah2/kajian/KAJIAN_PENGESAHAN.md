# Kajian: "tunggu confirmation, contohnya higher high, baru entry" — betul ke? (14 Nov 2026)

Soalan pengguna: seorang pakar saham berkata tunggu isyarat pengesahan dahulu baru beli, contohnya selepas *higher high*. (1) Adakah itu amalan standard pakar? (2) Adakah ia betul pada data kita? (3) Boleh diintegrasikan ke dalam keluarga F?

Dokumen ini ditulis tangan (bertarikh). Angka data dipetik daripada `kajian/carian_setup/hasil/PENGESAHAN.md` (dijana `cs_sahkan.py`, pradaftar `SPEC_CARIAN_SETUP.md` pindaan (ac), asalnya (r) di cawangan lama `claude/dreamy-lovelace-38z7wm`; dibawa ke `main` 16 Nov 2026 atas keputusan pengguna, tanpa dijana semula); fail itulah sumber kebenaran. Bahagian amalan pakar ialah ringkasan carian web (halaman tidak dibaca penuh; kebanyakannya blog dan laman vendor, bukan teks utama).

## 1. Amalan pakar: standard bagi SATU aliran, bukan semua

- **Aliran ikut trend / pecah tinggi memang menunggu pengesahan.** Teori Dow (awal 1900-an) mentakrifkan uptrend sebagai puncak lebih tinggi dan lembah lebih tinggi, dan menekankan pengesahan. O'Neil dan Minervini membeli apabila harga MEMECAH titik pivot (puncak tapak) dengan volum 40–50 % di atas purata, dengan henti rugi ketat 7–8 %. Darvas dan Weinstein (Stage 2) serupa. Pedagang *price action* (Raschke, Brooks) meletak *buy-stop* di atas tinggi bar sebelumnya.
- **Aliran lain tidak menunggu.** Aliran pembalikan purata (cth. Connors RSI2) membeli semasa saham lemah. Ada juga pedagang trend yang sengaja masuk AWAL sebelum pecah tinggi (pocket pivot, pivot dalam konsolidasi) kerana harga lebih baik.
- **Pakar sendiri mengakui tukar ganti:** pengesahan menapis isyarat palsu, tetapi harga beli lebih mahal dan sebahagian pergerakan sudah terlepas. Ukuran yang betul ialah jangkaan setiap dagangan, bukan kadar menang sahaja. Ujian yang diterbitkan bercampur: satu kajian RSI pada Nasdaq 100 mendapati membeli terus (menang 56.3 %) lebih baik daripada menunggu pengesahan (53.2 %); kajian Bulkowski menunjukkan sebahagian besar pecah tinggi gagal (bergantung pada corak dan takrif).
- **Kesimpulan (1):** dakwaan itu BENAR sebagai amalan aliran ikut trend, tetapi ia bukan satu-satunya amalan standard. *Higher high* lebih kerap dianggap pengesahan trend, bukan semestinya titik masuk.

## 2. Pada data kita (saham yang carian tidak lihat, 2010–2026)

**(a) Gaya masuk, pencetus sahaja** (656 varian keluarga indikator; kelebihan atas saham rawak hari sama):

| Gaya masuk | Swing 4 minggu | Trend 6 bulan |
|---|---|---|
| Beli semasa lemah (RSI rendah, bawah Bollinger, jatuh) | +0.32 mata; 92 % varian positif | −0.26 mata; 32 % positif |
| Pengesahan kekuatan / higher high | +0.06 mata; 65 % positif | +0.02 mata; 55 % positif |
| Pecah tinggi n hari (`K10`, *higher high* paling terus) | +0.28 mata; 88 % positif | +0.20 mata; 80 % positif |

Untuk swing, beli semasa lemah paling konsisten. Untuk trend besar, kekuatan lebih baik daripada kelemahan; yang terbaik ialah gap ≥ 15 % dengan volum (+5.1 mata) dan RS silang atas 95 (+4.4 mata). Kelebihan pencetus sahaja adalah kecil dalam kedua-dua lorong; prasyarat (earnings, hasil tumbuh) yang menyumbang paling banyak.

**(b) Menambah pengesahan pada setup F sedia ada** (42 setup dipercayai; isyarat yang sama, tiga cara masuk):

| Cara | % isyarat dibeli | Harga beli | Naik lagi hingga minggu 4 | Tangkap penuh | Menang | Purata |
|---|---|---|---|---|---|---|
| Beli buka esok (sekarang) | 100 % | – | 13.5 % | 14.5 % | 52 % | +1.72 % |
| Tunggu TUTUP di atas tinggi hari isyarat | 52 % | +4.1 % lebih mahal | 12.4 % | 12.0 % | 52 % | +1.44 % |
| Buy-stop pada tinggi hari isyarat | 74 % | +1.6 % lebih mahal | 12.7 % | 14.0 % | 52 % | +1.67 % |

- Bacaan dikunci: pengesahan menolong bagi 2 daripada 42 setup (tutup sahkan) dan 5 daripada 42 (buy-stop) → **TIDAK menolong**. Bilangan tangkapan mutlak jatuh 57 % dan 28 %.
- **Intuisi pakar itu betul, tetapi tidak boleh diniagakan:** isyarat yang kemudian memecah tinggi hari isyarat memang jauh lebih baik (naik lagi 17.5 %, purata +3.46 %) daripada yang tidak (4.0 %, −2.86 %). Tetapi apabila pengesahan itu tiba, harga sudah 1.6–4.1 % lebih mahal, dan itu menghapuskan kelebihannya.

## 3. Boleh diintegrasikan ke dalam F?

- **Dari segi teknikal: ya, sudah dibina** (`cs_sahkan.py`; kernel menerima harga beli khas; diuji).
- **Dari segi hasil: tidak disyorkan untuk lorong swing F.** Setup F terbaik membeli saham yang lemah menjelang earnings; menunggu *higher high* membuang separuh isyarat dan membeli lebih mahal tanpa menaikkan kadar tangkap.
- **Tempat pengesahan yang betul ialah lorong trend (`T01`–`T12`, CS08):** di situ pencetusnya memang jenis pengesahan (RS silang atas 95, undur pemimpin, Supertrend naik), dan `T11` ialah setup yang akan membeli MXL pada 22 April 2026.

## 4. Kaveat

Kumpulan B sudah dilihat; tiada saham delist; buy-stop diandaikan terisi tanpa gelinciran; prasyarat dinilai pada hari isyarat. Backtest sahaja, bukan bukti.

## Sumber (carian web 14 Nov 2026)

- Teori Dow dan pengesahan: https://thedowtheory.com/dow-theory-special-issue-why-it-is-a-bad-idea-to-apply-the-dow-theory-to-monthly-highs-and-the-vital-importance-of-confirmation
- Cara O'Neil, Minervini, Darvas, Kullamägi masuk pecah tinggi: https://www.financialwisdomtv.com/post/how-legendary-traders-enter-breakouts-minervini-kullamagi-darvas-o-neil
- Analisis tapak O'Neil: https://www.luxalgo.com/library/concept/oneil-base-analysis/
- Higher high sebagai pengesahan: https://therighttrader.com/learn/trend-analysis/higher-high
- Teknik masuk awal: https://traderlion.com/trading-strategies/3-early-entry-techniques-to-improve-win-rate/
- Masuk awal lawan tunggu pengesahan: https://civolatility.substack.com/p/breakout-trading
- Kajian RSI Nasdaq 100 (menunggu pengesahan merugikan): https://backtest.substack.com/p/why-waiting-for-rsi-confirmation
- Buy-stop di atas tinggi bar sebelumnya (Brooks): https://www.brookstradingcourse.com/?p=19180
- Van Tharp tentang masuk dan jangkaan: https://the7circles.uk/?p=32719
- Bulkowski, pengesahan dan kadar gagal corak: https://www.thepatternsite.com/Confirmation.html
