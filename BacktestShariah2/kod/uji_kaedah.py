"""Semak modul kaedah lawan registry: python3 uji_kaedah.py M54 [M55 ...]
Perlu registry/Mxx.csv tempatan (salin daripada Project)."""
import sys, importlib, pickle, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tambahan import *

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_data431.pkl')
def data():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    fr, idx, asal = muat(); pickle.dump((fr, idx, asal), open(CACHE, 'wb')); return fr, idx, asal

def uji(mid):
    fr, idx, asal = data()
    fr = {t: g[['open','high','low','close','volume','turnover']].copy() for t, g in fr.items()}
    m = importlib.import_module(f'kaedah.{mid}')
    t0 = time.time(); m.sedia(fr, idx); t1 = time.time()
    T = trades(fr, tmax=m.TMAX, warm=m.WARM); cv = portfolio(T, fr)
    B = penanda(idx, fr); me = metrik(T, cv, B, ada_henti=m.ADA_HENTI)
    reg = pd.read_csv(f'registry/{mid}.csv'); r = reg[(reg['set'].astype(str) == '431') & (reg.varian == m.VARIAN)]
    if r.empty:
        print(mid, 'VARIAN tiada dalam registry:', m.VARIAN); return
    r = r.iloc[0]
    out = {k: (round(me[k], 4), r[k]) for k in ['n', 'cagr', 'mdd', 'win', 'avg', 'days']}
    ok = abs(me['n'] - r['n']) <= max(3, 0.02 * r['n']) and abs(me['cagr'] - r['cagr']) <= 0.015
    # hampir() pada bar terakhir untuk semua saham
    nh = 0; contoh = None
    for t, g in fr.items():
        h = m.hampir(g, idx)
        if h: nh += 1; contoh = contoh or (t, h)
    nsig = sum(bool(g.sig.iloc[-1]) for g in fr.values())
    print(f"{mid} {'PADAN' if ok else 'TIDAK PADAN'} | sedia {t1-t0:.1f}s | " +
          ' '.join(f'{k}={a}/{b}' for k, (a, b) in out.items()) +
          f" | isyarat bar akhir={nsig} hampir={nh} contoh={contoh}")

if __name__ == '__main__':
    for x in sys.argv[1:]: uji(x)
