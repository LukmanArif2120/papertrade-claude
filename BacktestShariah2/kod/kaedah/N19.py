"""Bawah jalur BB + RSI<30 — kaedah Nxx (kombinasi indikator REVERSE). Jejak hadapan, bukan dakwaan.

Pradaftar jejak: `REVERSE/SPEC_JEJAK_N.md`. Peraturan dan nombor: `REVERSE/registry_N.csv`
dan `REVERSE/silang_akhir.csv`. Formula indikator: `kaedah/_nxx.py` (salinan verbatim
`REVERSE/teras/ind.py`, disahkan bit-identik oleh `ujian/test_nxx_sepadan.py`).

MASUK  : bb_pctb < 0 DAN rsi14 < 30  (LuxAlgo)
CARA   : C01 — beli pada BUKA esok (enjin v1.2 `o[i+1]`)
KELUAR : lorong 1 = X13 (rsi14 > 70 -> jual buka esok) · lorong 2 = X15 Chandelier 4xATR14
HENTI  : TIADA dengan sengaja — `KOLAM_EKOR.md` §4a mengukur henti ketat menghasilkan 421
         daripada 1,770 posisi C yang dibeli DAN dihentikan pada hari masuk dengan kadar
         menang 0.00%. `stop = NaN` menjadikan kecacatan itu mustahil secara struktur.
SASARAN: TIADA — `KOMBINASI.md` mengukur sasaran 1xATR menukar asas +2.595% jadi -0.281%.
TMAX   : 126 bar = ufuk keluar `IMBAS` kajian, jadi tiada dagangan melebihi apa yang diukur.

Lift terbaik dalam ujian MASUK Nxx: +0.873 latih / +3.618 tahan pada keluar X3
(9x N01), n 73,769. Gate1 LULUS, gate2 gagal pada ambang BH 0.00097 jadi TIADA
dakwaan sendiri dibuat; ia disertakan kerana ia salah satu daripada tiga kaki GB02
dan kerana `NXX.md` mendapati ia memperbaiki jangkaan terpangkas-ekor +1.08 mata
atas asasnya — satu daripada dua kes dalam kajian yang kelebihannya TIDAK hidup
sepenuhnya dalam ekor kanan.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N19'
NAMA = 'Bawah jalur BB + RSI<30'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 240


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n19(f))
        g['_rsi14'] = f.rsi14
        g['_bb'] = f.bb_pctb


def hampir(g, idx):
    """[1] bb_pctb < 0  [2] rsi14 < 30."""
    r = g.iloc[-1]
    if bool(r.sig) or not (r._bb == r._bb) or not (r._rsi14 == r._rsi14):
        return None
    return NX.hampir_syarat(
        [('bb_pctb < 0', r._bb < 0, abs(float(r._bb))),
         ('rsi14 < 30', r._rsi14 < 30, float(r._rsi14) - 30.0)], len(g), 60)
