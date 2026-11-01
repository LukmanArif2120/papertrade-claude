"""Holy Grail (Raschke) — kaedah Nxx (kombinasi indikator REVERSE). Jejak hadapan, bukan dakwaan.

Pradaftar jejak: `REVERSE/SPEC_JEJAK_N.md`. Peraturan dan nombor: `REVERSE/registry_N.csv`
dan `REVERSE/silang_akhir.csv`. Formula indikator: `kaedah/_nxx.py` (salinan verbatim
`REVERSE/teras/ind.py`, disahkan bit-identik oleh `ujian/test_nxx_sepadan.py`).

MASUK  : adx14 > 30 DAN rendah menyentuh ema20 DAN tutup > tinggi[-1]  (Linda Raschke, Street Smarts)
CARA   : C01 — beli pada BUKA esok (enjin v1.2 `o[i+1]`)
KELUAR : lorong 1 = X13 (rsi14 > 70 -> jual buka esok) · lorong 2 = X15 Chandelier 4xATR14
HENTI  : TIADA dengan sengaja — `KOLAM_EKOR.md` §4a mengukur henti ketat menghasilkan 421
         daripada 1,770 posisi C yang dibeli DAN dihentikan pada hari masuk dengan kadar
         menang 0.00%. `stop = NaN` menjadikan kecacatan itu mustahil secara struktur.
SASARAN: TIADA — `KOMBINASI.md` mengukur sasaran 1xATR menukar asas +2.595% jadi -0.281%.
TMAX   : 126 bar = ufuk keluar `IMBAS` kajian, jadi tiada dagangan melebihi apa yang diukur.

SATU-SATUNYA peraturan MASUK Nxx yang melepasi gate1 DAN gate2: lift +0.452 latih
/ +1.750 tahan, n 104,014, dan ia bertahan BH-FDR. `NXX.md` juga mendapati ia
memperbaiki jangkaan terpangkas-ekor +0.70 mata atas asasnya. Teks buku BELUM
dibaca; peraturan ini daripada ringkasan pihak ketiga, jadi ia SATU versi.
"""
import _nxx as NX

ID = 'N115'
NAMA = 'Holy Grail (Raschke)'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 240


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n115(f, g))
        g['_rsi14'] = f.rsi14
        g['_adx'] = f.adx14
        g['_e20'] = f.ema20


def hampir(g, idx):
    """[1] adx14 > 30  [2] rendah <= ema20  [3] tutup > tinggi semalam."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 60 or not (r._adx == r._adx) or not (r._e20 == r._e20):
        return None
    h1 = float(g.high.iloc[-2])
    return NX.hampir_syarat(
        [('adx14 > 30', r._adx > 30, 30.0 - float(r._adx)),
         ('rendah <= ema20', float(r.low) <= float(r._e20), None),
         ('tutup > tinggi[-1]', float(r.close) > h1, None)], len(g), 60)
