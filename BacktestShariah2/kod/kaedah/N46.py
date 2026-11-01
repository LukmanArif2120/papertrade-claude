"""Undur ke EMA21 lalu pecah — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : rendah[-1] <= ema21[-1] DAN tutup > tinggi[-1]
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Corak undur-lalu-pecah, sepupu `N115` tanpa syarat ADX. Melepasi gate1 pada 1 keluar.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N46'
NAMA = 'Undur ke EMA21 lalu pecah'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n46(f, g))
        g['_rsi14'] = f.rsi14
        g['_e21'] = f.ema21


def hampir(g, idx):
    """[1] rendah semalam <= ema21 semalam  [2] tutup > tinggi semalam."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('rendah[-1] <= ema21[-1]',
          float(g.low.iloc[-2]) <= float(g._e21.iloc[-2]), None),
         ('tutup > tinggi[-1]', float(r.close) > float(g.high.iloc[-2]), None)], len(g), 300)
