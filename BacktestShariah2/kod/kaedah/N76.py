"""KAWALAN MA: tutup atas MA50 — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : tutup > ma50
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

KAWALAN NEGATIF keluarga `MA`. Lift tahan diukur **-0.641** — lebih buruk daripada
beli setiap bar. Keluarga MA memberi 0/20 dalam `NXX.md`. Ia dijejak SUPAYA ada
garis bawah: kalau kohort berbukti tidak mengalahkan ini ke hadapan, dapatan
peringkat keluarga TIDAK direplikasi.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N76'
NAMA = 'KAWALAN MA: tutup atas MA50'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n76(f, g), f)
        g['_rsi14'] = f.rsi14
        g['_ma50'] = f.ma50


def hampir(g, idx):
    """[1] tutup > ma50. Satu syarat."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('tutup > ma50', float(r.close) > float(r._ma50),
          (float(r._ma50) / float(r.close) - 1.0) * 100.0 if r.close else None)], len(g), 300)
