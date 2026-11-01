"""NR7 + hari dalam — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : nr7 DAN inside_day
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Pemampatan julat (Connors/Raschke ID-NR4 keluarga). Melepasi gate1 pada 2 keluar.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N49'
NAMA = 'NR7 + hari dalam'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n49(f), f)
        g['_rsi14'] = f.rsi14
        g['_nr7'] = f.nr7
        g['_ins'] = f.inside_day


def hampir(g, idx):
    """[1] julat tersempit 7 hari  [2] hari dalam (tinggi lebih rendah, rendah lebih tinggi)."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('nr7', r._nr7 > 0, None), ('inside_day', r._ins > 0, None)], len(g), 300)
