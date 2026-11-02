"""N37X14 = N37 x X14 — pangkat 23/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : gap_and_go
KELUAR : lorong 1 = X14 (keluar bila rsi14 silang naik 50)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +1.528%  tahan +3.448%  ·  lift latih +0.909  tahan +2.457
  menang 45.5%  untung +21.18%  rugi -11.37%  n tahan 19,652  p 0.00059
  tanpa5 -1.855%  -> NEGATIF: kelebihan hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N37X14'
NAMA = 'Gap and go x X14'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n37(f), f, keluar='X14')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
