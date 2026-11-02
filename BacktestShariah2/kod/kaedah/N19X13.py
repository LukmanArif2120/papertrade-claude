"""N19X13 = N19 x X13 — pangkat 2/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : bb_pctb < 0 DAN rsi14 < 30
KELUAR : lorong 1 = X13 (keluar bila rsi14 > 70)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +5.597%  tahan +11.285%  ·  lift latih +2.892  tahan +6.935
  menang 63.8%  untung +30.53%  rugi -22.57%  n tahan 73,769  p 0.00358
  tanpa5 +4.262%  -> POSITIF: kelebihan tidak bergantung ekor kanan

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N19X13'
NAMA = 'Bawah jalur BB + RSI<30 x X13'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n19(f), f, keluar='X13')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
