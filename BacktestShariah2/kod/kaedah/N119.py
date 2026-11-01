"""Tiga tutup menurun berturut — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : tutup[-2] > tutup[-1] DAN tutup[-1] > tutup
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

Pembalikan min paling mudah dalam registry — tiada indikator sama sekali, hanya
tiga tutup. Melepasi gate1 pada KEEMPAT keluar (lift +0.072 tahan) tetapi gagal FDR.
Nilainya sebagai ASAS keluarga RSI: kalau peraturan RSI tidak mengalahkan ini,
indikator RSI tidak menambah apa-apa atas "tiga hari jatuh".
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N119'
NAMA = 'Tiga tutup menurun berturut'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n119(g))
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """[1] tutup[-2] > tutup[-1]  [2] tutup[-1] > tutup hari ini."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('tutup[-2] > tutup[-1]',
          float(g.close.iloc[-3]) > float(g.close.iloc[-2]), None),
         ('tutup[-1] > tutup', float(g.close.iloc[-2]) > float(r.close), None)], len(g), 300)
