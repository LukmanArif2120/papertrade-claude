"""N75X15 = N75 x X15 — pangkat 7/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : rsi14 < 40
KELUAR : lorong 1 = X15 (ekori Chandelier 4 x ATR14)
         X15 TIDAK boleh jadi lorong 1 — enjin v1.2 baca `stop` SEKALI pada bar
         isyarat, jadi henti MENGEKOR mustahil (diuji). Lorong 2 ialah keluarnya.
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +2.913%  tahan +5.608%  ·  lift latih +0.865  tahan +1.902
  menang 41.3%  untung +35.88%  rugi -15.68%  n tahan 861,071  p 0.00000
  tanpa5 -2.432%  -> NEGATIF: kelebihan hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N75X15'
NAMA = 'RSI14 < 40 tanpa penapis x X15'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n75(f), f, keluar='X15')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
