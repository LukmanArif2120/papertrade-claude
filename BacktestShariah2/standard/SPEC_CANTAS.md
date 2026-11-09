# Pradaftar peraturan CANTAS (label maklumat bulanan; bukan tindakan automatik)

**Dipradaftar 9 Nov 2026** (cadangan `kajian/FABLE_CADANGAN.md` §1; pengguna menyerahkan pilihan kepada penilai pada
hari yang sama). Pelaksana: `standard/cantas.py` → `laporan/CANTAS.md`, `data/analisis/cantas.json`. Kunci:
`ujian/test_cantas.py::TestKunci`. Mengubah ambang memerlukan keputusan pengguna + pradaftar bertarikh di sini.

## Apa yang skrip ini BUAT dan TIDAK buat

- BUAT: menandakan kaedah yang memenuhi mana-mana peraturan C1–C5 sebagai **CALON CANTAS**, dengan peraturan dan nombor.
- TIDAK: tidak menghentikan Lejar, tidak mengubah kad skor, tidak mengubah penyebut G1–G6. Menghentikan rekod belian
  kaedah ialah **keputusan pengguna** yang dicatat dalam `koordinator/keputusan.csv`; skrip ini hanya memberi senarai.
- Dinilai setiap larian `analisis.yml` tetapi **dibaca sebulan sekali** (sesi pertama bulan): lajur `bulan_berturut`
  mengira berapa bulan berturut-turut kaedah itu kekal calon. Cadangan keputusan hanya bagi `bulan_berturut ≥ 2`.

## Peraturan (penyebut = baris `data/analisis/kad_skor.json`, LANGSUNG sahaja)

| Kod | Syarat | Ambang dikunci | Sumber |
|---|---|---|---|
| C1 | hari beli ≥ `C1_HARI_BELI` DAN posisi ≥ `C1_POSISI` DAN henti hari-0 ≥ `C1_HARI0_PCT` % posisi | 12 · 30 · 20.0 | `G4_HARI0_MAKS = 0` → gate pasti gagal |
| C2 | pantau Papan Penganalisis dalam `C2_PANTAU` | {BERSARA, GANTUNG} | `penganalisis.PANTAU_P/PANTAU_DD` |
| C3 | status kad skor NEGATIF | — | `SPEC_KAD_SKOR.md` |
| C4 | status kad skor GAGAL pada larian ini DAN larian sebelumnya (`cantas.json` lama) | 2 larian | `SPEC_KAD_SKOR.md` |
| C5 | lorong T4 L1 sesi ≥ `C5_SESI` DAN pulangan ≤ SPUS tingkap sama − `C5_JURANG` mata DAN MDD ≤ `C5_MDD` | 63 · 5.0 · -10.0 | `G6_SESI/2`, `G6_MDD_HAD` |

Nxx: C1 tidak terpakai (tiada henti). Kaedah replika dinilai seperti kad skor (dagangan replika).

## Keadaan pada pradaftar (9 Nov 2026, data 6 Nov 2026)

Kesan dijangka: C1 ≈ 12 kaedah Mxx (`FABLE_PENILAIAN.md` §8); C2–C5 0 (G1 belum lulus; lorong 16 sesi). Angka sebenar
dijana oleh skrip, bukan disalin ke sini.
