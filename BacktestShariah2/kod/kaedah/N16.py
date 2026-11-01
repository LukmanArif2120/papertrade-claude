"""RSI2 < 10 tanpa penapis — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : rsi2 < 10
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Diukur terhadap X13 oleh `REVERSE/step30_nxx_x13.py` (peraturan keputusan dikomit
SEBELUM larian, spec §8b; kawalan regresi N115 LULUS identik |delta| = 0.00e+00):
  jangkaan +3.875 latih / +5.857 tahan · lift +1.170 / +1.506 ·
  menang 63.4% · untung +22.30% · rugi -22.64% · n tahan 567,422
Lulus keempat-empat syarat (jangkaan dan lift positif pada KEDUA-DUA tingkap).
Asas X13: latih +2.705% tahan +4.350%.

Connors RSI2. Pasangan A/B terus dengan `N15` (sama tetapi dengan penapis
`tutup > ma200`): `nxx.csv` mengukur N16 TANPA penapis LEBIH BAIK (lift +0.449
lawan -0.393), jadi penapis trend MERUGIKAN di sini.

AMARAN yang mesti dibaca: `N16 x X1` (sasaran 1xATR) memberi menang 62.4% dengan
jangkaan MUTLAK -0.088% = RUGI, kerana asas X1 sendiri -0.281%. Kohort ini guna
X13, bukan X1. Lift positif atas asas negatif masih rugi.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N16'
NAMA = 'RSI2 < 10 tanpa penapis'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n16(f), f)
        g['_rsi14'] = f.rsi14
        g['_rsi2'] = f.rsi2


def hampir(g, idx):
    """[1] rsi2 < 10. Satu syarat."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('rsi2 < 10', r._rsi2 < 10, float(r._rsi2) - 10.0)], len(g), 300)
