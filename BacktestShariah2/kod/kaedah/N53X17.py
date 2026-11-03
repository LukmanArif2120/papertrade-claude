"""N53X17 = N53 x X17 — pangkat 21/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : supertrend > 0 DAN adx14 > 25
KELUAR : lorong 1 = X17 (keluar bila adx14 < 20)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +1.516%  tahan +3.814%  ·  lift latih +0.779  tahan +1.958
  menang 41.9%  untung +23.40%  rugi -10.33%  n tahan 913,085  p 0.00000
  tanpa5 -2.446%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N53X17'
NAMA = 'Supertrend + ADX>25 x X17'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n53(f), f, keluar='X17')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Calon watchlist: syarat masuk yang sebahagiannya sudah dipenuhi.

    Jarak dilapor dalam unit syarat itu sendiri (mata RSI/ADX/%b, atau peratus harga), dan
    `paras` kekal None: peraturan ini ialah ambang INDIKATOR, jadi menukar jarak indikator
    kepada paras harga esok akan mengandaikan hubungan linear yang tidak wujud. Kaedah Mxx
    boleh melaporkan paras kerana peraturannya ditulis pada harga; Nxx tidak boleh, dan
    mendakwa sebaliknya lebih buruk daripada membiarkannya kosong."""
    return NX.hampir_nxx(g, 'n53', PERLU_BAR)
