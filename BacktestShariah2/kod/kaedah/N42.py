"""Lonjakan volum + tutup naik — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : vol_n50 >= 2.0 DAN tutup > tutup[-1]
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Melepasi gate1 (lift +1.093 tahan, 3 daripada 4 keluar) tetapi GAGAL BH-FDR.
Dijejak untuk melihat sama ada kegagalan FDR itu kekurangan kuasa atau tiada kesan.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N42'
NAMA = 'Lonjakan volum + tutup naik'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n42(f, g), f)
        g['_rsi14'] = f.rsi14
        g['_vol'] = f.vol_n50


def hampir(g, idx):
    """[1] vol_n50 >= 2.0  [2] tutup > tutup semalam."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('vol_n50 >= 2.0', r._vol >= 2.0, (2.0 - float(r._vol)) * 10.0),
         ('tutup > tutup[-1]', float(r.close) > float(g.close.iloc[-2]), None)], len(g), 300)
