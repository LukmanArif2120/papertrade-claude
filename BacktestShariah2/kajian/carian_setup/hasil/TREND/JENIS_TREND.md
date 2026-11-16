# Jenis dan tempoh trend menaik setiap saham (tinjauan; gambaran sahaja, BUKAN isyarat beli atau jual)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_jenis_trend.py`. Takrif ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (w). **Jangan sunting secara manual.**

Data: 3,260 saham AS, 2010 – 2026, harga tutup harian. "Hari" di sini = hari dagangan (5 hari seminggu; 21 = sebulan).

**Apa kata buku (Teori Dow, untuk pasaran keseluruhan):** tiga trend serentak — utama (kira-kira setahun atau lebih), sekunder (kira-kira 3 minggu hingga 3 bulan) dan kecil (beberapa hari hingga 3 minggu); angka itu kelaziman, bukan peraturan tetap ([thismatter.com](https://thismatter.com/money/technical-analysis/dow-theory.htm), [babypips.com](https://www.babypips.com/forexpedia/dow-theory)). Tiada jadual tempoh piawai bagi saham tunggal dalam sumber yang disemak, jadi tempoh di bawah diukur sendiri.

**Satu trend menaik** = dari satu dasar ke satu puncak. Trend dikira tamat apabila harga jatuh melebihi had toleransi dari harga tertingginya. Tiga saiz ikut had toleransi itu (ATR = julat gerakan harian biasa saham itu, lazimnya 2–4 % harga):

- **Kecil**: tamat bila jatuh 2 × ATR (kira-kira 5–8 %). Ayunan beberapa hari hingga beberapa minggu.
- **Sederhana**: tamat bila jatuh 4 × ATR (kira-kira 10–15 %). "Turun sikit masih ok."
- **Besar**: tamat bila jatuh 8 × ATR (kira-kira 20–30 %). Trend utama; di dalamnya ada beberapa trend sederhana.

## 1. Tiga saiz trend: berapa kerap, berapa lama, berapa banyak naik

| Saiz | Bilangan setiap saham setahun | Tempoh biasa (nilai tengah) | Julat separuh tengah | 1 daripada 10 lebih lama daripada | Naik dasar → puncak (nilai tengah) | Julat separuh tengah |
|---|---|---|---|---|---|---|
| **Kecil** | 6.4 | **3 minggu** (17 hari) | 2 minggu – 6 minggu | 9 minggu | **+14 %** | +9 % – +23 % |
| **Sederhana** | 2.4 | **9 minggu** (44 hari) | 5 minggu – 4 bulan | 6 bulan | **+26 %** | +17 % – +43 % |
| **Besar** | 0.7 | **7 bulan** (140 hari) | 4 bulan – 13 bulan | 21 bulan | **+58 %** | +36 % – +103 % |

## 2. Berapa lama: pecahan ikut tempoh

| Saiz | < 1 bulan | 1–3 bulan | 3–6 bulan | > 6 bulan |
|---|---|---|---|---|
| **Kecil** | 60 % (naik +11 %) | 37 % (naik +20 %) | 3 % (naik +37 %) | 0 % (naik +55 %) |
| **Sederhana** | 18 % (naik +17 %) | 48 % (naik +23 %) | 24 % (naik +37 %) | 9 % (naik +61 %) |
| **Besar** | 0 % (naik +31 %) | 18 % (naik +35 %) | 27 % (naik +43 %) | 55 % (naik +84 %) |

Dalam kurungan = kenaikan nilai tengah bagi trend dalam kumpulan tempoh itu.

## 3. Empat jenis ikut kelajuan

Kelajuan = purata kenaikan sehari dari dasar ke puncak. **Sangat perlahan** < 0.25 % sehari (kurang ~5 % sebulan); **perlahan** 0.25–0.5 % sehari (~5–11 % sebulan); **sederhana** 0.5–1 % sehari (~11–23 % sebulan); **laju** ≥ 1 % sehari (≥ ~5 % seminggu).

**Trend sederhana:**

| Jenis | Bahagian | Tempoh biasa | Julat separuh tengah | Naik dasar → puncak | Turun paling dalam di tengah jalan (nilai tengah) |
|---|---|---|---|---|---|
| Sangat perlahan | 11 % | **5 bulan** | 3 bulan – 7 bulan | +21 % | −5 % |
| Perlahan | 35 % | **12 minggu** | 8 minggu – 4 bulan | +25 % | −5 % |
| Sederhana | 35 % | **7 minggu** | 5 minggu – 11 minggu | +27 % | −4 % |
| Laju | 19 % | **4 minggu** | 2 minggu – 6 minggu | +33 % | −2 % |

**Trend besar:**

| Jenis | Bahagian | Tempoh biasa | Julat separuh tengah | Naik dasar → puncak | Turun paling dalam di tengah jalan (nilai tengah) |
|---|---|---|---|---|---|
| Sangat perlahan | 36 % | **13 bulan** | 8 bulan – 21 bulan | +58 % | −12 % |
| Perlahan | 38 % | **6 bulan** | 4 bulan – 10 bulan | +55 % | −9 % |
| Sederhana | 20 % | **3 bulan** | 9 minggu – 5 bulan | +57 % | −5 % |
| Laju | 6 % | **9 minggu** | 6 minggu – 11 minggu | +78 % | −2 % |

## 4. Kalau sudah naik N hari, berapa lama lagi?

| Saiz | Sudah naik | Berapa peratus sampai dua kali ganda tempoh itu | Baki tempoh (nilai tengah) | Julat separuh tengah baki |
|---|---|---|---|---|
| Sederhana | 5 hari | 97 % | 8 minggu | 4 minggu – 3 bulan |
| Sederhana | 2 minggu | 86 % | 7 minggu | 3 minggu – 3 bulan |
| Sederhana | 4 minggu | 66 % | 7 minggu | 3 minggu – 3 bulan |
| Sederhana | 8 minggu | 44 % | 6 minggu | 3 minggu – 3 bulan |
| Sederhana | 12 minggu | 30 % | 7 minggu | 3 minggu – 3 bulan |
| Sederhana | 6 bulan | 9 % | 7 minggu | 3 minggu – 4 bulan |
| Besar | 5 hari | 100 % | 6 bulan | 3 bulan – 13 bulan |
| Besar | 2 minggu | 100 % | 6 bulan | 3 bulan – 12 bulan |
| Besar | 4 minggu | 94 % | 6 bulan | 11 minggu – 12 bulan |
| Besar | 8 minggu | 78 % | 5 bulan | 9 minggu – 11 bulan |
| Besar | 12 minggu | 68 % | 6 bulan | 9 minggu – 11 bulan |
| Besar | 6 bulan | 52 % | 6 bulan | 11 minggu – 12 bulan |

## 5. Bahagian yang boleh dikenal semasa berlaku

Dasar dan puncak hanya diketahui kemudian. Trend hanya boleh DIKENAL selepas harga sudah naik melebihi had toleransi dari dasar, dan hanya DISAHKAN tamat selepas harga sudah jatuh sebanyak itu dari puncak. Jadual ini mengukur bahagian tengah itu sahaja (tanpa kos):

| Saiz | Lewat dikenal (dari dasar) | Tempoh dikenal → disahkan tamat | Perubahan harga sepanjang itu (nilai tengah) | Purata | Berapa peratus berakhir untung |
|---|---|---|---|---|---|
| **Kecil** | 6 hari | 3 minggu | -1.1 % | +1.4 % | 44 % |
| **Sederhana** | 3 minggu | 9 minggu | -2.7 % | +2.5 % | 41 % |
| **Besar** | 9 minggu | 7 bulan | -4.7 % | +10.1 % | 42 % |

## 6. Kestabilan dan bilangan

- Kecil: 161,459 trend lengkap (≥ 5 hari); 9 % ayunan lebih pendek daripada 5 hari (lonjakan, tidak dikira); nilai tengah tempoh setiap tahun antara 15 dan 20 hari; dibuang: 1,664 ayunan pertama dan 1,265 yang belum tamat pada hujung data.
- Sederhana: 60,847 trend lengkap (≥ 5 hari); 0 % ayunan lebih pendek daripada 5 hari (lonjakan, tidak dikira); nilai tengah tempoh setiap tahun antara 36 dan 62 hari; dibuang: 1,234 ayunan pertama dan 961 yang belum tamat pada hujung data.
- Besar: 16,995 trend lengkap (≥ 5 hari); 0 % ayunan lebih pendek daripada 5 hari (lonjakan, tidak dikira); nilai tengah tempoh setiap tahun antara 102 dan 257 hari; dibuang: 1,931 ayunan pertama dan 1,335 yang belum tamat pada hujung data.

## 7. Kaveat

- Ini gambaran apa yang SUDAH berlaku, bukan isyarat beli atau jual: dasar dan puncak tidak diketahui pada masa itu (lihat §5).
- Kenaikan dan kelajuan dasar → puncak melebihi apa yang dagangan sebenar boleh tangkap.
- Trend yang belum tamat pada hujung data dibuang, jadi trend paling panjang sedikit terkurang kira; tiada saham delist dalam data.
- Angka bergantung pada takrif; sebab itu tiga saiz ditunjuk. Jadual penuh: `hasil/TREND/jenis_trend.csv`.
