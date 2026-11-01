"""RSI2<10 + atas MA200 — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : rsi2 < 10 DAN tutup > ma200
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

`N16` dengan penapis trend. Pasangan terus dengan `N16` (tanpa penapis): `nxx.csv`
mengukur N16 LEBIH BAIK (lift +0.449 lawan -0.393), jadi penapis ma200 MERUGIKAN di
sini. Dijejak sebagai pasangan A/B penapis yang eksplisit.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N15'
NAMA = 'RSI2<10 + atas MA200'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n15(f, g), f)
        g['_rsi14'] = f.rsi14
        g['_rsi2'] = f.rsi2
        g['_ma200'] = f.ma200


def hampir(g, idx):
    """[1] rsi2 < 10  [2] tutup > ma200."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('rsi2 < 10', r._rsi2 < 10, float(r._rsi2) - 10.0),
         ('tutup > ma200', float(r.close) > float(r._ma200), None)], len(g), 300)
