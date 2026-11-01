"""RSI14 silang naik 30 — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : rsi14 silang naik 30
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Diukur terhadap X13 oleh `REVERSE/step30_nxx_x13.py` (peraturan keputusan dikomit
SEBELUM larian, spec §8b; kawalan regresi N115 LULUS identik |delta| = 0.00e+00):
  jangkaan +5.004 latih / +8.320 tahan · lift +2.299 / +3.970 ·
  menang 63.5% · untung +26.54% · rugi -23.44% · n tahan 54,073
Lulus keempat-empat syarat (jangkaan dan lift positif pada KEDUA-DUA tingkap).
Asas X13: latih +2.705% tahan +4.350%.

LIFT TERTINGGI antara empat yang melepasi FDR — lebih kuat daripada `N115`
(+3.159) walaupun pada keluar X2 ia kelihatan lebih lemah (+1.264 lawan +1.464).
Jadi pilihan keluar menukar susunan masuk; "masuk mana terbaik" tidak bermakna
tanpa menyebut keluar.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N17'
NAMA = 'RSI14 silang naik 30'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n17(f), f)
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """[1] rsi14 > 30 hari ini DAN rsi14 <= 30 semalam (silang naik)."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('rsi14 silang naik 30',
          (r._rsi14 > 30) and (float(g._rsi14.iloc[-2]) <= 30),
          abs(float(r._rsi14) - 30.0))], len(g), 300)
