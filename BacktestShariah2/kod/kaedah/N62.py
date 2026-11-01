"""KAWALAN POLA: pecah julat ketat 20 hari — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : julat20 <= 8% tutup DAN tutup > tinggi20[-1]
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

KAWALAN NEGATIF keluarga `POLA`, dan topeng PALING BURUK antara kesemua 65: lift
tahan **-2.651** dan satu-satunya dengan jangkaan MUTLAK negatif (-0.057%). Kalau
mana-mana kohort tidak mengalahkan ini ke hadapan, jejak itu tiada maklumat.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N62'
NAMA = 'KAWALAN POLA: pecah julat ketat 20 hari'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n62(f, g), f)
        g['_rsi14'] = f.rsi14
        g['_j20'] = f.julat20
        g['_t20'] = f.tinggi20


def hampir(g, idx):
    """[1] julat20 <= 8% tutup  [2] tutup > tinggi 20 hari."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('julat20 <= 8%', r._j20 <= 0.08 * float(r.close), None),
         ('tutup > tinggi20', float(r.close) > float(r._t20),
          (float(r._t20) / float(r.close) - 1.0) * 100.0 if r.close else None)], len(g), 300)
