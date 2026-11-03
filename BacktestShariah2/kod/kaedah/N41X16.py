"""N41X16 = N41 x X16 — pangkat 89/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : cmf20 > 0 DAN tutup > ema20
KELUAR : lorong 1 = X16 (keluar bila supertrend berbalik)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +0.752%  tahan +1.051%  ·  lift latih +0.384  tahan +0.333
  menang 35.3%  untung +16.59%  rugi -7.42%  n tahan 1,536,991  p 0.00073
  tanpa5 -2.507%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N41X16'
NAMA = 'CMF20>0 + tutup>EMA20 x X16'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n41(f, g), f, keluar='X16')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Calon watchlist: syarat masuk yang sebahagiannya sudah dipenuhi.

    Jarak dilapor dalam unit syarat itu sendiri (mata RSI/ADX/%b, atau peratus harga), dan
    `paras` kekal None: peraturan ini ialah ambang INDIKATOR, jadi menukar jarak indikator
    kepada paras harga esok akan mengandaikan hubungan linear yang tidak wujud. Kaedah Mxx
    boleh melaporkan paras kerana peraturannya ditulis pada harga; Nxx tidak boleh, dan
    mendakwa sebaliknya lebih buruk daripada membiarkannya kosong."""
    return NX.hampir_nxx(g, 'n41', PERLU_BAR)
