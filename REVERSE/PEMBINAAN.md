# Pembinaan portfolio tanpa pemicu: keputusan

Dijana 2026-10-29 06:53 UTC oleh `REVERSE/pembinaan.py`. Pradaftar: `REVERSE/SPEC_PEMBINAAN.md` (dikomit sebelum larian ini).

## Keputusan: **DITOLAK**

Tempoh keputusan 2020–2025 lawan **SPUS: 17.95%/tahun, MDD -26.82%** (tutup bulanan). SPY rujukan sahaja: 14.82%/tahun, MDD -33.72%.

Masuk **rawak** (tiada pemicu), 20 benih setiap konfigurasi, kos penuh. Penanda aras tanpa kos.

| Konfig | Slot | Keluar | Pulangan median | p10 | p90 | MDD median | S1 pul | S2 mdd | S3 p10 | LULUS |
|---|---|---|---|---|---|---|---|---|---|---|
| `A40` | 40 | `H63S` | +6.44% | +3.92% | +9.07% | -39.52% | tidak | tidak | tidak | tidak |
| `A8` | 8 | `H63S` | +4.71% | -3.61% | +18.87% | -48.97% | tidak | tidak | tidak | tidak |
| `B40` | 40 | `H63` | +10.72% | +7.87% | +14.89% | -36.39% | tidak | tidak | tidak | tidak |
| `B8` | 8 | `H63` | +9.46% | +3.53% | +17.80% | -44.72% | tidak | tidak | tidak | tidak |
| `C40` | 40 | `TRAIL` | +12.61% | +7.38% | +16.05% | -34.28% | tidak | tidak | tidak | tidak |
| `C8` | 8 | `TRAIL` | +7.68% | +2.23% | +20.89% | -42.59% | tidak | tidak | tidak | tidak |
| **SPUS** | — | beli-pegang | **+17.95%** | — | — | **-26.82%** | — | — | — | — |

### Dua konvensyen SPUS — keputusan bertahan pada kedua-duanya

Repo ini merekod SPUS sebagai **26.09%/tahun, MDD -10.14%** (`PENANDA_ARAS_SYARIAH.md`, `KEPEKATAN.md`) manakala ujian ini menggunakan **17.95%/tahun, MDD -26.82%**. Kedua-duanya betul dan dari data yang sama: 26.09% ialah **median pulangan setiap tahun** (konvensyen median-setiap-tahun seluruh kajian) manakala 17.95% ialah **CAGR seluruh tingkap**. Median lebih tinggi kerana ia membuang tahun terburuk (2022: −22.76%); CAGR ialah angka pengkompaunan yang sebenar. Ujian ini menggunakan CAGR bagi sistem DAN penanda aras, jadi perbandingannya setara.

Keputusan tidak bergantung pada pilihan itu. Konfigurasi terbaik memberi **+12.61%** pulangan dan **-34.28%** MDD. Itu kalah kepada versi SPUS yang paling memihak kepada sistem pada kedua-dua paksi: pulangan SPUS terendah (17.95%) masih lebih tinggi, dan MDD SPUS terdalam (-26.82%) masih lebih cetek. Tiada gabungan konvensyen menukar keputusan.

`S1` pulangan median > SPUS · `S2` MDD lebih cetek daripada SPUS · `S3` **p10** masih > SPUS. Spec §10 memerlukan **ketiga-tiga**. S3 ialah syarat yang menghalang konfigurasi bertuah kelihatan seperti dapatan.

## Apa yang setiap lajur grid ubah

`A8` ialah pembinaan kajian sendiri dengan pemicu dibuang: +4.71%/tahun, MDD -48.97%. Setiap konfigurasi lain berbeza daripadanya pada SATU paksi sahaja (slot, atau henti, atau kedua-duanya).

- **Slot 8 → 40 (henti kekal)**: pulangan +1.73 mata, MDD +9.46 mata (`A8`→`A40`)
- **Buang henti keras (8 slot)**: pulangan +4.75 mata, MDD +4.25 mata (`A8`→`B8`)
- **Terima ekor: TRAIL (8 slot)**: pulangan +2.97 mata, MDD +6.39 mata (`A8`→`C8`)
- **Kedua-dua: 40 slot + TRAIL**: pulangan +7.90 mata, MDD +14.69 mata (`A8`→`C40`)

## Hingar pemilihan

Sebaran p90−p10 merentas benih: `A40` 5.2 mata, `A8` 22.5 mata, `B40` 7.0 mata, `B8` 14.3 mata, `C40` 8.7 mata, `C8` 18.7 mata.

Julat penuh 20 benih bagi `A8`: -6.48% hingga +24.26% (sisihan piawai 8.61 mata). Itulah sebabnya syarat `S3` ada: satu larian tunggal boleh mendarat di mana-mana dalam julat itu, dan melaporkan larian terbaik sebagai prestasi sistem adalah kesilapan yang sama yang dibetulkan oleh `KEPEKATAN_BENIH.md`.

## Tafsiran

**Tiada konfigurasi memenuhi ketiga-tiga syarat.** Jangkaan priori dalam spec §11 ialah DITOLAK dan ia tepat.

Sebabnya: pulangan (S1) gagal pada SETIAP konfigurasi; MDD (S2) gagal pada SETIAP konfigurasi.

Maksudnya ruang **pembinaan** kini juga diukur. Ruang **pemicu** sudah diukur dan kosong (fasa 1, 1b, 2 SEC). Kedua-dua paksi yang ada pada kita telah diukur terhadap penanda aras yang betul, dan kedua-duanya tidak mengalahkannya.

Kesimpulan jujur: **memegang SPUS mengalahkan apa-apa yang kajian ini boleh bina daripada alam ini.** Itu bukan kegagalan pelaksanaan; ia hasil yang diukur enam kali dengan cara berbeza.

### Tetapi satu sebab priori saya SALAH, dan ia penting

Spec §11 sebab 2 menjangka nisbah tidak akan bertambah baik, bersandarkan `KEPEKATAN.md` yang mendapati 8→60 slot memperbaiki MDD 3.48 mata tetapi **mengorbankan pulangan 5.97 mata**. Hasil di sini bertentangan: setiap perubahan pembinaan memperbaiki **kedua-dua** paksi secara monoton, dan `A8`→`C40` memberi pulangan **+7.90 mata** DAN MDD **+14.69 mata** (lebih cetek) serentak.

Sebab kedua-dua dokumen boleh betul: populasinya berbeza. `KEPEKATAN.md` menambah slot pada entri yang **dipilih** (susunan abjad daripada peristiwa sah SEC), jadi slot tambahan mencairkan subset yang sudah terpilih. Di sini entri **rawak**, jadi slot tambahan hanya mengurangkan varians sampel tanpa apa-apa untuk dicairkan. Itu bukan percanggahan; ia memberitahu bahawa kenaikan pembinaan bergantung pada apa yang ia dikenakan ke atas.

Jadi paksi pembinaan **memang** mengandungi kenaikan sebenar — kira-kira 7.9 mata pulangan dan 14.7 mata MDD daripada pembinaan sahaja, yang lebih besar daripada apa-apa yang mana-mana pemicu dalam fasa 1/1b/2 pernah hasilkan. Ia tetap tidak cukup: ia bermula dari 4.71% dan berakhir pada 12.61%, sedangkan SPUS 17.95%. Kenaikan itu nyata tetapi jurangnya lebih besar.

**Implikasi yang perlu dinyatakan:** jika kerja selepas ini dibuat juga, arahnya ialah pembinaan (slot lebih banyak, tiada henti keras, biarkan pemenang berjalan), **bukan** pemicu. Tetapi destinasinya tetap di bawah memegang SPUS, jadi yang rasional ialah berhenti membina dan bandingkan jejak hadapan dengan SPUS.

## Had

- Backtest, bukan jejak hadapan. Semua kaveat `KEPEKATAN_BENIH.md` terpakai.
- MDD SPUS daripada tutup **bulanan** (data yang ada), jadi ia lebih cetek daripada MDD harian yang benar. Itu memihak kepada SPUS — ia menjadikan syarat `S2` lebih sukar, bukan lebih mudah.
- Alam A02 **bukan** ditapis Syariah; SPUS ditapis. Perbandingan itu tidak setara pada paksi tapisan, dan tapisan Syariah membuang semua kewangan.
- Siri ekuiti tempoh keputusan dihiris daripada larian 14 tahun dan dinormalkan semula, jadi posisi yang terbuka pada sempadan 2020 diwarisi.
- Tunai tidak berbunga (0%), yang merugikan sistem berbanding realiti.
- `TRAIL` diimbas maksimum 504 sesi; jika Chandelier tidak tercetus, posisi ditutup pada hujung tingkap itu.

**Ia tidak mencapai +10%/bulan dan tidak pernah boleh.** Lihat `SASARAN.md`.
