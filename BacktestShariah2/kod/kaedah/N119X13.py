"""N119X13 = N119 x X13 — pangkat 9/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : tutup[-2] > tutup[-1] DAN tutup[-1] > tutup
KELUAR : lorong 1 = X13 (keluar bila rsi14 > 70)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +3.319%  tahan +5.090%  ·  lift latih +0.614  tahan +0.740
  menang 64.9%  untung +19.62%  rugi -21.74%  n tahan 1,051,604  p 0.00011
  tanpa5 +1.176%  -> POSITIF: kelebihan tidak bergantung ekor kanan

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N119X13'
NAMA = '3 tutup turun berturut x X13'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n119(g), f, keluar='X13')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
