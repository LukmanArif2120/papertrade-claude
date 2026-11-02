"""N124X15 = N124 x X15 — pangkat 1/40 jejak grid penuh.

Pradaftar `REVERSE/SPEC_GRID_PENUH.md` · keputusan `REVERSE/GRID_PENUH.md` ·
senarai `REVERSE/jejak40.csv`

MASUK  : gap >= 8% DAN vol_n50 >= 2.0
KELUAR : lorong 1 = X15 (ekori Chandelier 4 x ATR14)
         X15 TIDAK boleh jadi lorong 1 — enjin v1.2 baca `stop` SEKALI pada bar
         isyarat, jadi henti MENGEKOR mustahil (diuji). Lorong 2 ialah keluarnya.
         lorong 2 = X15 Chandelier tutup 4xATR14 (automatik, setiap posisi)
CARA   : C01 beli pada BUKA esok · HENTI TIADA · SASARAN TIADA · TMAX 126
URUTAN : rank = U14 momentum 12-1

DIUKUR pada grid penuh 1,495 sel, penyebut BH-FDR JUJUR m = 1,495:
  jangkaan latih +3.064%  tahan +16.127%  ·  lift latih +1.016  tahan +12.421
  menang 44.2%  untung +64.23%  rugi -21.92%  n tahan 12,728  p 0.00367
  tanpa5 +0.396%  -> POSITIF: kelebihan tidak bergantung ekor kanan

HAD: jangkaan SETIAP DAGANGAN, bukan prestasi portfolio.
"""
try:
    from kaedah import _nxx as NX
except ImportError:
    import _nxx as NX

ID = 'N124X15'
NAMA = 'Episodic pivot gap 8-10% x X15'
VARIAN = 'V1 grid penuh'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.n124(f), f, keluar='X15')
        g['_rsi14'] = f.rsi14


def hampir(g, idx):
    """Watchlist tidak dilaporkan bagi kohort kombinasi."""
    return None
