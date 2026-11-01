"""Gap and go — kaedah Nxx (kombinasi indikator REVERSE). Jejak hadapan, bukan dakwaan.

Pradaftar jejak: `REVERSE/SPEC_JEJAK_N.md`. Peraturan dan nombor: `REVERSE/registry_N.csv`
dan `REVERSE/silang_akhir.csv`. Formula indikator: `kaedah/_nxx.py` (salinan verbatim
`REVERSE/teras/ind.py`, disahkan bit-identik oleh `ujian/test_nxx_sepadan.py`).

MASUK  : buka > tinggi[-1] x 1.02 DAN tutup > buka DAN vol_n50 >= 1.5  (klasik intraday)
CARA   : C01 — beli pada BUKA esok (enjin v1.2 `o[i+1]`)
KELUAR : lorong 1 = X13 (rsi14 > 70 -> jual buka esok) · lorong 2 = X15 Chandelier 4xATR14
HENTI  : TIADA dengan sengaja — `KOLAM_EKOR.md` §4a mengukur henti ketat menghasilkan 421
         daripada 1,770 posisi C yang dibeli DAN dihentikan pada hari masuk dengan kadar
         menang 0.00%. `stop = NaN` menjadikan kecacatan itu mustahil secara struktur.
SASARAN: TIADA — `KOMBINASI.md` mengukur sasaran 1xATR menukar asas +2.595% jadi -0.281%.
TMAX   : 126 bar = ufuk keluar `IMBAS` kajian, jadi tiada dagangan melebihi apa yang diukur.

Lift terbaik +0.323 latih / +2.099 tahan, n 19,652. Gate1 LULUS, gate2 gagal.
Kaki MOMENTUM dalam GB02 — `GABUNGAN.md` mendapati yang lulus kesemua gate ialah
KESATUAN merentas keluarga signal (dua momentum + dua pembalikan min), bukan
persilangan, jadi kaki ini perlu dijejak sendiri untuk mengenal sumbangannya.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N37'
NAMA = 'Gap and go'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 240


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n37(f), f)
        g['_rsi14'] = f.rsi14
        g['_vol'] = f.vol_n50


def hampir(g, idx):
    """[1] buka > tinggi semalam x 1.02  [2] tutup > buka  [3] vol_n50 >= 1.5.
    Ketiga-tiganya dinilai pada bar yang SUDAH tamat, jadi "hampir" hanya bermakna
    sebahagian syarat dipenuhi hari ini; tiada paras harga esok yang boleh dikira."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 60 or not (r._vol == r._vol):
        return None
    h1 = float(g.high.iloc[-2])
    return NX.hampir_syarat(
        [('buka > tinggi[-1] x 1.02', float(r.open) > h1 * 1.02,
          (h1 * 1.02 / float(r.open) - 1.0) * 100.0 if r.open else None),
         ('tutup > buka', float(r.close) > float(r.open), None),
         ('vol_n50 >= 1.5', r._vol >= 1.5, (1.5 - float(r._vol)) * 10.0)], len(g), 60)
