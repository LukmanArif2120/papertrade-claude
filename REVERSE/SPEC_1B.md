# SPEC FASA 1B — saiz posisi dan henti berskala kemeruapan

Dikunci **28 Okt 2026**, sebelum sebarang larian 1b. Fasa 1 (`SPEC.md`, `KEPUTUSAN_FASA1.md`)
**ditutup dan tidak disentuh**; keputusan 1b tidak boleh mencemari rekod fasa 1.

## 1. Mengapa 1b ada

`DIAGNOSIS_FASA1.md` mengukur dua perkara yang mengubah soalan:

1. **Siling pandangan sempurna** = median bulanan 12.89%; Step 9 sebenar menangkap 0.91%
   (≈ 7% daripada nilai pemilihan yang ada).
2. **Korelasi pangkat** `atr_pct` terhadap pulangan yang boleh didagangkan = **−0.251**, sedangkan
   kuintil ATR% tertinggi ialah signal berlift tertinggi dalam Step 4. Perkara yang memilih
   pergerakan besar ialah perkara yang sama yang menghalang pegangan sampai habis.

Hipotesis 1b, satu sahaja: **kekangan yang mengikat ialah pembinaan dagangan, bukan signal.**
Fasa 1 mengenakan saiz posisi tetap 12.5% dan henti tetap −2×ATR sama rata kepada nama
berkemeruapan 4% dan 15% sehari. 1b menyamakan **risiko setiap dagangan** dan membiarkan saiz
berubah.

## 2. Perubahan tunggal yang diuji

Saiz posisi tidak lagi tetap. Dengan henti pada **k × ATR14** di bawah harga masuk:

```
nilai_posisi = (RISIKO × ekuiti) ÷ (k × ATR%)
```

supaya kerugian jika dihentikan ≈ RISIKO × ekuiti bagi setiap dagangan, tanpa mengira kemeruapan.

**Semua yang lain kekal sama seperti fasa 1**: universe A02, definisi peristiwa sah, signal ENTRY
(asas yang sama seperti Step 9 setiap tahun), kos (SPEC §3.1), masuk buka esok, ufuk 252 hari,
tiada leverage, satu posisi satu saham, tiada penalaan parameter.

### Grid dipradaftar

| Parameter | Nilai |
|---|---|
| RISIKO setiap dagangan | 0.5%, 1.0%, 1.5% ekuiti |
| k (gandaan ATR untuk henti mengekor) | 2, 3, 4 |
| Varian kekangan | **V1** maksimum 8 posisi (kesan saiz sahaja) · **V2** tiada had bilangan, pendedahan ≤ 100% (saiz + kepelbagaian) |

**N ujian 1b = 3 × 3 × 2 = 18 setiap tahun**, 108 merentas enam tahun. Keluarga FDR sendiri
(`SISTEM_1B`), BH q ≤ 0.01, dikira berasingan daripada keluarga fasa 1.

### Had saiz (mengelak leverage tersembunyi dan posisi habuk)

- nilai_posisi dihadkan **≤ 25%** ekuiti dan **≥ 2%** ekuiti; di luar julat itu, dihadkan ke sempadan.
- Jumlah pendedahan **≤ 100%** ekuiti. Jika tunai tidak cukup, posisi dilangkau (bukan dikecilkan),
  supaya kesan kekangan kelihatan.

### Exit

Henti mengekor **k × ATR14** yang sama dengan andaian saiz (konsisten secara dalaman), ditambah
**tiga rujukan wajib fasa 1** yang dijalankan semula dengan saiz baharu: pegang-252,
Chandelier 4×ATR14, jual hari ke-63.

## 3. Kawalan dan ambang penerimaan (dikunci sebelum larian)

1. **Asas fasa 1**: `portfolio_<TAHUN>.csv` yang sudah dicommit (saiz tetap 12.5%).
2. **KAWALAN RAWAK dengan saiz 1b yang sama** — supaya perbandingan kritikal fasa 1 diulang.
3. **SPY** tempoh sama.

**1b diterima sebagai penambahbaikan hanya jika** satu konfigurasi mengalahkan **ketiga-tiganya**
— asas fasa 1, kawalan rawak bersaiz sama, dan SPY — dalam **≥ 4 daripada 6 tahun**, pada pulangan
tahunan **dan** MDD. Jika tidak: 1b DITOLAK dan dilaporkan sebagai ditolak.

## 4. Had yang diakui lebih awal

1b menggunakan **enam tahun yang sama** seperti fasa 1, dan idea saiz berskala dipilih **selepas**
melihat hasil fasa 1. Maka keputusan tertinggi 1b ialah **CALON**, walaupun ambang §3 dipenuhi.
Ujian sebenar memerlukan tempoh yang belum disentuh atau ujian ke hadapan hidup.

Kaveat fasa 1 terpakai sepenuhnya: tiada saham delist (survivorship), peta sektor bukan titik-masa,
universe 2020 lebih kecil, portfolio bilangan posisi kecil = varians tinggi.

## 5. Output

`REVERSE/portfolio_1b_<TAHUN>.csv`, `REVERSE/KEPUTUSAN_1B.md`, baris `FASA1B` dalam `log_ujian.csv`.
Fail fasa 1 **tidak** ditulis semula.
