"""N53X16 = N53 x X16 — pangkat 36/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : supertrend > 0 DAN adx14 > 25
KELUAR : lorong 1 = X16 (keluar bila supertrend berbalik)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +0.894%  tahan +2.163%  ·  lift latih +0.526  tahan +1.445
  menang 34.1%  untung +22.95%  rugi -8.58%  n tahan 913,085  p 0.00000
  tanpa5 -2.569%  -> NEGATIF: kelebihan hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N53X16'
NAMA = 'Supertrend + ADX>25 x X16'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n53(f), f, keluar='X16')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
