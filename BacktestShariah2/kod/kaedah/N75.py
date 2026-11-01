"""RSI14 < 40 tanpa penapis — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : rsi14 < 40
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Diukur terhadap X13 oleh `REVERSE/step30_nxx_x13.py` (peraturan keputusan dikomit
SEBELUM larian, spec §8b; kawalan regresi N115 LULUS identik |delta| = 0.00e+00):
  jangkaan +4.748 latih / +7.468 tahan · lift +2.043 / +3.118 ·
  menang 62.6% · untung +26.22% · rugi -23.96% · n tahan 861,071
Lulus keempat-empat syarat (jangkaan dan lift positif pada KEDUA-DUA tingkap).
Asas X13: latih +2.705% tahan +4.350%.

Melepasi BH-FDR pada TIGA keluar (X2/X3/X4) dalam `nxx.csv` — satu-satunya
topeng MASUK yang melakukannya. Tetapi ia mencetus pada ~18% bar, jadi ia hampir
syarat REJIM bukan setup: had MAKS_KAEDAH=10 mengikat kuat dan pemeringkat U14
menjadi lebih penting bagi kohort ini daripada kohort lain.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N75'
NAMA = 'RSI14 < 40 tanpa penapis'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n75(f), f)
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """[1] rsi14 < 40. Satu syarat."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('rsi14 < 40', r._rsi14 < 40, float(r._rsi14) - 40.0)], len(g), 300)
