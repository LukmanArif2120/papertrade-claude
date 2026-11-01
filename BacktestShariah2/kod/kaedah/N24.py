"""KAWALAN TREND: Supertrend + ADX>20 — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : supertrend > 0 DAN adx14 > 20
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

KAWALAN NEGATIF keluarga `TREND`. Lift tahan **-0.161**. Keluarga TREND memberi
0/24. Juga topeng paling bertindih dalam registry (Jaccard 0.805 dengan N56).
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N24'
NAMA = 'KAWALAN TREND: Supertrend + ADX>20'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n24(f))
        g['_rsi14'] = f.rsi14
        g['_st'] = f.supertrend
        g['_adx'] = f.adx14


def hampir(g, idx):
    """[1] supertrend menaik  [2] adx14 > 20."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('supertrend > 0', r._st > 0, None),
         ('adx14 > 20', r._adx > 20, 20.0 - float(r._adx))], len(g), 300)
