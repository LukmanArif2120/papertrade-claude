# Adakah angka 8-slot kajian ini cabutan bertuah?

Dijana 2026-10-29 05:42 UTC oleh `REVERSE/kepekatan_benih.py`.

`step9_portfolio.jalankan()` menyusun calon dengan tuple `(0.0, 0.0, ticker)` dan `reverse=True`. Tanpa pemeringkatan signal, tuple itu **pemalar**, jadi susunan menjadi **ticker menurun ikut abjad**. "8 slot" bermakna 8 calon terakhir ikut abjad setiap hari — subset sewenang-wenang yang TETAP, bukan sampel neutral.

`KEPEKATAN.md` menunjukkan 8 slot = 19.31%/tahun tetapi 60 slot = 13.34%. Oleh kerana 60 slot mengambil hampir semua calon, 13.34% menghampiri min populasi. Jadi 19.31% mungkin cabutan bertuah.

Ujian: 8 slot, populasi/keluar/kos **sama**, hanya susunan pemilihan ditukar kepada rawak dengan beberapa benih.

| Susunan | Pulangan/tahun | MDD | Median bulanan |
|---|---|---|---|
| 1 | 8.12% | -18.34% | 1.07% |
| 10 | 2.57% | -22.32% | -0.21% |
| 11 | 9.48% | -18.39% | 0.34% |
| 12 | 16.36% | -15.01% | 1.49% |
| 13 | 12.22% | -16.36% | 1.17% |
| 14 | 14.66% | -14.64% | 1.21% |
| 15 | 9.80% | -20.72% | 0.84% |
| 16 | 19.90% | -17.54% | 1.16% |
| 17 | 8.64% | -20.09% | 0.73% |
| 18 | 12.60% | -19.90% | 1.06% |
| 19 | 16.63% | -17.62% | 0.56% |
| 2 | 9.70% | -17.82% | 0.26% |
| 20 | 8.86% | -16.70% | 1.70% |
| 3 | 8.52% | -18.99% | 0.80% |
| 4 | 7.05% | -16.48% | 0.86% |
| 5 | 13.12% | -15.66% | 1.21% |
| 6 | 5.33% | -18.66% | 0.48% |
| 7 | 11.44% | -16.94% | 1.40% |
| 8 | 10.06% | -20.23% | 0.81% |
| 9 | 15.04% | -15.24% | 0.62% |
| abjad **(yang diguna seluruh kajian)** | 19.31% | -16.28% | 1.16% |

Susunan rawak: median **9.93%**, julat 2.57% hingga 19.90% (20 benih). Susunan abjad yang diguna seluruh kajian: **19.31%**.

Susunan abjad melebihi **19 daripada 20** benih rawak; nilai-p satu-hujung **0.095**.

Itu **tidak** melepasi ambang kelaziman (p = 0.095 > 0.05). Susunan abjad berada pada hujung tinggi taburan tetapi **tidak boleh didakwa bertuah secara pasti** — sekurang-kurangnya satu benih rawak (19.90%) mengalahkannya.

**Dapatan yang menentukan bukan nilai-p itu, tetapi SEBARANNYA.**

- Median susunan neutral: **9.93%/tahun** — ini anggaran pusat yang betul bagi sistem pada 8 slot, bukan 19.31%.
- Julat: 2.57% hingga 19.90%, sisihan piawai **4.15 mata**.
- Maka apa-apa perbandingan sistem yang bezanya lebih kecil daripada kira-kira **17.3 mata** adalah dalam hingar pemilihan, bukan dapatan.

Nombor 19.31% yang dilaporkan sepanjang kajian ialah **satu cabutan** daripada taburan ini, dan cabutan itu berada di hujung tinggi (persentil 95). Anggaran yang betul ialah medianya, 9.93%/tahun pada MDD -17.72%.
