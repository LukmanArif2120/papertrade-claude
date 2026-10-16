# Bina modul pengeluaran Papertrade C (BacktestShariah2/kod/kaedah/Mxx.py) bagi calon K145+ daripada
# WFO/kaedah_baru/Mxx.py + gabungan stop/exit/tmax pilihan WFO suku terkini (dibekukan).
#   python3 WFO/kod/bina_pengeluaran.py M115 ... M161
import os, re, sys
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
BARU = os.path.join(ROOT, '..', 'kaedah_baru'); HASIL = os.path.join(ROOT, '..', 'data', 'hasil')
KELUAR = os.path.join(ROOT, '..', '..', 'BacktestShariah2', 'kod', 'kaedah')


def pilihan(mid):
    p = pd.read_csv(os.path.join(HASIL, mid + '_pilihan.csv'))
    sah = p[p.get('stop').notna()] if 'stop' in p else p.iloc[0:0]
    if len(sah) == 0: return 'ASAL', 'ASAL', 0, 'tiada gabungan WFO sah; tetapan asal'
    r = sah.iloc[-1]
    return r.stop, r.exit, int(r.tmax), f'pilihan WFO suku {r.suku} (latih {r.latih})'


def bina(mid, tetapan=None):
    """tetapan: (henti, keluar, tmax, keterangan) yang diluluskan pengguna; None = pilihan WFO suku terkini."""
    src = open(os.path.join(BARU, mid + '.py')).read()
    s, e, x, asal = tetapan or pilihan(mid)
    src = re.sub(r'^from _alat import .*$', 'try:\n    from kaedah._k145 import *\nexcept ImportError:\n    from _k145 import *', src, count=1, flags=re.M)
    src = re.sub(r"^VARIAN = .*$", f"VARIAN = 'V1 WFO beku: henti {s}, keluar {e}, tmax {x or 'tiada'}'", src, count=1, flags=re.M)
    src = re.sub(r'^TMAX = .*$', f'TMAX = {x or None}', src, count=1, flags=re.M)
    src = re.sub(r'^ADA_HENTI = .*$', 'ADA_HENTI = True      # had henti 0.85 x tutup sentiasa dipasang', src, count=1, flags=re.M)
    src = src.replace('\ndef sedia(fr, idx):', '\ndef _entri(fr, idx):', 1)
    src = src.replace("# Sumber: BacktestShariah2/spec/KATALOG_K145.md", "# Calon K145+ dimasukkan ke Papertrade C 16 Okt 2026. Entry: salinan WFO/kaedah_baru/" + mid + ".py.\n# Sumber: BacktestShariah2/spec/KATALOG_K145.md", 1)
    src += f'''

HENTI_KOD = '{s}'
KELUAR_KOD = '{e}'
# Gabungan stop/exit/tmax: {asal}. Keputusan backtest set 431 dengan gabungan ini ialah DALAM SAMPEL
# (gabungan dipilih atas 2023–2026); rujuk WFO/laporan/W01_LAPORAN.md untuk prestasi luar sampel.


def sedia(fr, idx):
    _entri(fr, idx)
    pasang(fr, HENTI_KOD, KELUAR_KOD)


def hampir(g, idx):
    """Watchlist (Hampir Signal) belum ditakrif bagi calon K145+; tiada calon hampir."""
    return None
'''
    open(os.path.join(KELUAR, mid + '.py'), 'w').write(src)
    return mid, s, e, x, asal


if __name__ == '__main__':
    for mid in sys.argv[1:]:
        print(*bina(mid))
