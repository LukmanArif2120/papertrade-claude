"""Kembali masuk jalur BB + RSI silang 30 — kaedah Nxx (kombinasi indikator REVERSE). Jejak hadapan, bukan dakwaan.

Pradaftar jejak: `REVERSE/SPEC_JEJAK_N.md`. Peraturan dan nombor: `REVERSE/registry_N.csv`
dan `REVERSE/silang_akhir.csv`. Formula indikator: `kaedah/_nxx.py` (salinan verbatim
`REVERSE/teras/ind.py`, disahkan bit-identik oleh `ujian/test_nxx_sepadan.py`).

MASUK  : bb_pctb[-1] < 0 DAN bb_pctb > 0 DAN rsi14 silang naik 30  (therighttrader)
CARA   : C01 — beli pada BUKA esok (enjin v1.2 `o[i+1]`)
KELUAR : lorong 1 = X13 (rsi14 > 70 -> jual buka esok) · lorong 2 = X15 Chandelier 4xATR14
HENTI  : TIADA dengan sengaja — `KOLAM_EKOR.md` §4a mengukur henti ketat menghasilkan 421
         daripada 1,770 posisi C yang dibeli DAN dihentikan pada hari masuk dengan kadar
         menang 0.00%. `stop = NaN` menjadikan kecacatan itu mustahil secara struktur.
SASARAN: TIADA — `KOMBINASI.md` mengukur sasaran 1xATR menukar asas +2.595% jadi -0.281%.
TMAX   : 126 bar = ufuk keluar `IMBAS` kajian, jadi tiada dagangan melebihi apa yang diukur.

Lift terbaik +0.936 latih / +1.614 tahan, n 19,208. Gate1 LULUS, gate2 gagal.
Ia kaki KEEMPAT `GB02_atau4`; `GABUNGAN.md` mengukur `atau4` dan `atau3` hampir
sama (jangkaan +4.944% lawan +5.025%), jadi ia dijejak berasingan untuk melihat
sama ada menambahnya membantu ke hadapan.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N20'
NAMA = 'Kembali masuk jalur BB + RSI silang 30'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 240


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n20(f), f)
        g['_rsi14'] = f.rsi14
        g['_bb'] = f.bb_pctb


def hampir(g, idx):
    """[1] bb_pctb semalam < 0  [2] bb_pctb hari ini > 0  [3] rsi14 silang naik 30."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 60 or not (r._bb == r._bb) or not (r._rsi14 == r._rsi14):
        return None
    bb1 = float(g._bb.iloc[-2]) if len(g) > 1 else float('nan')
    rs1 = float(g._rsi14.iloc[-2]) if len(g) > 1 else float('nan')
    return NX.hampir_syarat(
        [('bb_pctb semalam < 0', bb1 < 0, None),
         ('bb_pctb > 0', r._bb > 0, abs(float(r._bb))),
         ('rsi14 silang naik 30', (r._rsi14 > 30) and (rs1 <= 30), abs(float(r._rsi14) - 30.0))],
        len(g), 60)
