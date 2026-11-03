"""N24X17 = N24 x X17 — pangkat 29/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : supertrend > 0 DAN adx14 > 20
KELUAR : lorong 1 = X17 (keluar bila adx14 < 20)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +1.231%  tahan +2.847%  ·  lift latih +0.493  tahan +0.991
  menang 40.7%  untung +19.95%  rugi -8.88%  n tahan 1,359,653  p 0.00035
  tanpa5 -2.438%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N24X17'
NAMA = 'Supertrend(10,3) + ADX>20 x X17'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n24(f), f, keluar='X17')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Calon watchlist: syarat masuk yang sebahagiannya sudah dipenuhi.

    Jarak dilapor dalam unit syarat itu sendiri (mata RSI/ADX/%b, atau peratus harga), dan
    `paras` kekal None: peraturan ini ialah ambang INDIKATOR, jadi menukar jarak indikator
    kepada paras harga esok akan mengandaikan hubungan linear yang tidak wujud. Kaedah Mxx
    boleh melaporkan paras kerana peraturannya ditulis pada harga; Nxx tidak boleh, dan
    mendakwa sebaliknya lebih buruk daripada membiarkannya kosong."""
    return NX.hampir_nxx(g, 'n24', PERLU_BAR)
