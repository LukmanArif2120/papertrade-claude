"""N42X15 = N42 x X15 — pangkat 8/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : vol_n50 >= 2.0 DAN tutup > tutup[-1]
KELUAR : lorong 1 = X15 (ekori Chandelier 4 x ATR14)
         X15 TIDAK boleh jadi lorong 1 — enjin baca `stop` SEKALI pada bar
         isyarat, henti MENGEKOR mustahil (diuji). Lorong 2 ialah keluarnya.
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +2.723%  tahan +5.461%  ·  lift latih +0.675  tahan +1.755
  menang 41.6%  untung +34.64%  rugi -15.35%  n tahan 130,675  p 0.00010
  tanpa5 -1.915%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N42X15'
NAMA = 'Lonjakan volum 2x x X15'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n42(f, g), f, keluar='X15')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
