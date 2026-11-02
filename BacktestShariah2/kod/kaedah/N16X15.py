"""N16X15 = N16 x X15 — pangkat 15/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : rsi2 < 10
KELUAR : lorong 1 = X15 (ekori Chandelier 4 x ATR14)
         X15 TIDAK boleh jadi lorong 1 — enjin baca `stop` SEKALI pada bar
         isyarat, henti MENGEKOR mustahil (diuji). Lorong 2 ialah keluarnya.
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +2.603%  tahan +4.352%  ·  lift latih +0.555  tahan +0.646
  menang 41.2%  untung +31.09%  rugi -14.36%  n tahan 567,422  p 0.00043
  tanpa5 -2.373%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N16X15'
NAMA = 'RSI2<10 tanpa penapis x X15'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n16(f), f, keluar='X15')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
