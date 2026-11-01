"""KAWALAN PECAH: Donchian 55 hari — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : tutup > tinggi 55 hari sebelumnya
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

KAWALAN NEGATIF keluarga `PECAH`. Lift tahan **-1.590**. Ini peraturan Turtle
klasik, dan `NXX.md` mengukur keluarga PECAH memberi 6 daripada 8 negatif.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N31'
NAMA = 'KAWALAN PECAH: Donchian 55 hari'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n31(f))
        g['_rsi14'] = f.rsi14
        g['_dc'] = f.donchian55


def hampir(g, idx):
    """[1] tutup > tinggi tertinggi 55 hari sebelumnya."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('pecah donchian55', r._dc > 0, None)], len(g), 300)
