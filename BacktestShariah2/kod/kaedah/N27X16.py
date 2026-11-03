"""N27X16 = N27 x X16 — pangkat 88/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : atas_awan DAN tenkan_atas
KELUAR : lorong 1 = X16 (keluar bila supertrend berbalik)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +0.778%  tahan +1.102%  ·  lift latih +0.410  tahan +0.385
  menang 34.3%  untung +17.24%  rugi -7.33%  n tahan 1,562,663  p 0.00096
  tanpa5 -2.430%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N27X16'
NAMA = 'Ichimoku atas awan x X16'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n27(f), f, keluar='X16')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Calon watchlist: syarat masuk yang sebahagiannya sudah dipenuhi.

    Jarak dilapor dalam unit syarat itu sendiri (mata RSI/ADX/%b, atau peratus harga), dan
    `paras` kekal None: peraturan ini ialah ambang INDIKATOR, jadi menukar jarak indikator
    kepada paras harga esok akan mengandaikan hubungan linear yang tidak wujud. Kaedah Mxx
    boleh melaporkan paras kerana peraturannya ditulis pada harga; Nxx tidak boleh, dan
    mendakwa sebaliknya lebih buruk daripada membiarkannya kosong."""
    return NX.hampir_nxx(g, 'n27', PERLU_BAR)
