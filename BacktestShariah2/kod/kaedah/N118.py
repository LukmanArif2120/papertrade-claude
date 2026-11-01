"""Atas MA200 selepas 4/5 sesi menurun — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : tutup > ma200 DAN 4 daripada 5 sesi terakhir menurun
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Pembalikan min dengan penapis trend jangka panjang (Connors & Alvarez keluarga).
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N118'
NAMA = 'Atas MA200 selepas 4/5 sesi menurun'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n118(f, g))
        g['_rsi14'] = f.rsi14
        g['_ma200'] = f.ma200
        g['_t45'] = f.turun_4d5


def hampir(g, idx):
    """[1] tutup > ma200  [2] 4 daripada 5 sesi terakhir tutup lebih rendah."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('tutup > ma200', float(r.close) > float(r._ma200),
          (float(r._ma200) / float(r.close) - 1.0) * 100.0 if r.close else None),
         ('4/5 sesi menurun', bool(r._t45), None)], len(g), 300)
