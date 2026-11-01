"""Gap 8% + volum 2x — kaedah Nxx. Jejak hadapan, bukan dakwaan. Pradaftar `REVERSE/SPEC_JEJAK_N.md`.

MASUK  : gap >= 8% DAN vol_n50 >= 2.0
CARA   : C01 beli pada BUKA esok · KELUAR: lorong 1 X13 (rsi14 > 70) + lorong 2 X15 Chandelier
HENTI  : TIADA (`stop = NaN`) · SASARAN: TIADA · TMAX 126 = ufuk IMBAS kajian
URUTAN : `rank` = U14 momentum 12-1 (hingar pemilihan susunan sewenang-wenang = 17.3 mata/tahun)

KES SOALAN REJIM. Lift tahan **+7.066** = TERTINGGI antara 65 topeng, hampir 2x
`N19` dan 4x `N115`, dengan jangkaan +9.660%. TETAPI lift LATIH negatif, jadi ia
GAGAL gate1 pradaftar dan TIADA dakwaan dibuat.

Dijejak dengan mata terbuka bahawa ia gagal gate, kerana jejak hadapan boleh
membezakan dua tafsiran yang kajian TIDAK boleh: (a) peraturan gagal yang bernasib
baik dalam 2020-2025, atau (b) peraturan yang hanya berfungsi dalam rejim selepas
2020. n tahan hanya 12,728 jadi ia jarang; jangan jangka banyak isyarat.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'N124'
NAMA = 'Gap 8% + volum 2x'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n124(f))
        g['_rsi14'] = f.rsi14
        g['_gap'] = f.gap
        g['_vol'] = f.vol_n50


def hampir(g, idx):
    """[1] gap >= 8%  [2] vol_n50 >= 2.0. Kedua-duanya pada bar yang sudah tamat."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300:
        return None
    return NX.hampir_syarat([('gap >= 8%', r._gap >= 0.08, (0.08 - float(r._gap)) * 100.0),
         ('vol_n50 >= 2.0', r._vol >= 2.0, (2.0 - float(r._vol)) * 10.0)], len(g), 300)
