"""Bawah jalur BB tanpa penapis RSI — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : tutup < ma20 - 2 x sd20
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

SUPERSET TEPAT `N19` tanpa penapis `rsi14 < 30` (Jaccard ~0.30 kerana N19 subset
N73). Menguji secara langsung sama ada penapis RSI itu menambah apa-apa, iaitu
soalan yang `SETUP.md` ukur secara am (setiap penapis merugikan) tetapi belum
pernah diuji pada pasangan tepat ini.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N73'
NAMA = 'Bawah jalur BB tanpa penapis RSI'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n73(f, g))
        g['_rsi14'] = f.rsi14
        g['_bbb'] = f.ma20 - 2.0 * f.sd20


def hampir(g, idx):
    """[1] tutup < jalur bawah BB(20,2). Satu syarat, jadi jarak harga sahaja."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('tutup < jalur bawah BB', float(r.close) < float(r._bbb),
          (float(r.close) / float(r._bbb) - 1.0) * 100.0 if r._bbb else None)], len(g), 300)
