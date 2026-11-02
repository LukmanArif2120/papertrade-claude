"""N28X17 = N28 x X17 — pangkat 12/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : adx14 > 25 DAN mdi < adx14
KELUAR : lorong 1 = X17 (keluar bila adx14 < 20)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +1.742%  tahan +4.586%  ·  lift latih +1.004  tahan +2.731
  menang 45.9%  untung +23.16%  rugi -11.18%  n tahan 1,404,045  p 0.00000
  tanpa5 -2.259%  -> NEGATIF: kelebihan hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N28X17'
NAMA = 'ADX>25 + DI+ > DI- x X17'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n28(f), f, keluar='X17')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
