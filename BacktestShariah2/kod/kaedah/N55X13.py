"""N55X13 = N55 x X13 — pangkat 14/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : bb_pctb < 20 DAN rsi14 > 40 DAN adx14 > 20
KELUAR : lorong 1 = X13 (keluar bila rsi14 > 70)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +3.475%  tahan +4.449%  ·  lift latih +0.770  tahan +0.098
  menang 64.6%  untung +18.54%  rugi -21.29%  n tahan 113,407  p 0.00251
  tanpa5 +1.115%  -> POSITIF: kelebihan tidak bergantung ekor kanan

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N55X13'
NAMA = 'BB + RSI + ADX>20 x X13'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n55(f), f, keluar='X13')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
