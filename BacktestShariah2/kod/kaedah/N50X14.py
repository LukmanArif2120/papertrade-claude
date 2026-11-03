"""N50X14 = N50 x X14 — pangkat 37/94 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak_semua.csv`

MASUK  : julat10 < 0.5 x julat20 DAN vol_n50 >= 1.5 DAN tutup > tinggi[-1]
KELUAR : lorong 1 = X14 (keluar bila rsi14 silang naik 50)
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +0.733%  tahan +2.201%  ·  lift latih +0.114  tahan +1.210
  menang 52.1%  untung +12.70%  rugi -9.21%  n tahan 14,857  p 0.00055
  tanpa5 -1.318%  -> NEGATIF: hidup dalam ekor kanan, SETUP.md terpakai

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N50X14'
NAMA = 'Mampat + pecah volum 1.5x x X14'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n50(f, g), f, keluar='X14')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Calon watchlist: syarat masuk yang sebahagiannya sudah dipenuhi.

    Jarak dilapor dalam unit syarat itu sendiri (mata RSI/ADX/%b, atau peratus harga), dan
    `paras` kekal None: peraturan ini ialah ambang INDIKATOR, jadi menukar jarak indikator
    kepada paras harga esok akan mengandaikan hubungan linear yang tidak wujud. Kaedah Mxx
    boleh melaporkan paras kerana peraturannya ditulis pada harga; Nxx tidak boleh, dan
    mendakwa sebaliknya lebih buruk daripada membiarkannya kosong."""
    return NX.hampir_nxx(g, 'n50', PERLU_BAR)
