"""N42X14 = N42 x X14 — pangkat 29/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : vol_n50 >= 2.0 DAN tutup > tutup[-1]
KELUAR : lorong 1 = X14 (keluar bila rsi14 silang naik 50)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +1.295%  tahan +2.599%  ·  lift latih +0.676  tahan +1.608
  menang 48.3%  untung +16.91%  rugi -10.78%  n tahan 130,675  p 0.00000
  tanpa5 -2.201%  -> NEGATIF: kelebihan hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N42X14'
NAMA = 'Lonjakan volum 2x x X14'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n42(f, g), f, keluar='X14')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
