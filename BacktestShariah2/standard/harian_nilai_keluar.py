# Larian harian 6:02 MYT: nilai keluar posisi M & C dengan tutup sesi terakhir
import sys, os, json, importlib, copy
import pandas as pd, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from stor import *
SP = os.path.dirname(HERE)
fr0, idx = frames_dict(muat(os.path.join(HERE, 'data')))
SES = list(idx['SPY'].index)
TAKHIR = SES[-1]
snap = pd.read_csv(os.path.join(SP, 'snap12.csv')).set_index('ticker')

def sesi_sebelum(d):
    d = pd.Timestamp(d); s = [x for x in SES if x < d]; return s[-1]

def hari(beli, sampai):
    b, s = pd.Timestamp(beli), pd.Timestamp(sampai)
    return sum(1 for x in SES if b < x <= s)

def keluar(g, ti, e, tmax):
    ix = g.index
    try: i = ix.get_loc(pd.Timestamp(ti))
    except KeyError: return None, 'tiada bar isyarat'
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    st = g['stop'].astype(float).values; tg = g['tgt'].astype(float).values
    ex = g['exitc'].fillna(False).astype(bool).values; n = len(g)
    sp = st[i] if not np.isnan(st[i]) else -np.inf
    j = i + 1
    while j < n:
        tgt = tg[j - 1] if j > i + 1 else np.nan
        if j > i + 1 and o[j] <= sp: return dict(t=ix[j], p=float(o[j]), why='kena henti (buka bawah henti)'), sp
        if l[j] <= sp: return dict(t=ix[j], p=float(sp), why='kena henti'), sp
        if not np.isnan(tgt):
            if j > i + 1 and o[j] >= tgt: return dict(t=ix[j], p=float(o[j]), why='capai sasaran (buka atas sasaran)'), sp
            if h[j] >= tgt: return dict(t=ix[j], p=float(tgt), why='capai sasaran'), sp
        if ex[j]:
            if j + 1 < n: return dict(t=ix[j + 1], p=float(o[j + 1]), why=f'isyarat keluar kaedah {ix[j].strftime("%d %b")}'), sp
            return dict(t=None, p=None, why='menunggu', isy=ix[j]), sp
        if tmax and (j - i) >= tmax: return dict(t=ix[j], p=float(c[j]), why=f'had masa {tmax} hari'), sp
        j += 1
    return None, sp

def main():
    out = {}
    for ak in ['moomoo', 'claude']:
        out[ak] = json.load(open(os.path.join(SP, 'db/papertrade', ak + '.json')))
    # kumpul kerja ikut kaedah
    kerja = {}
    for ak, d in out.items():
        for k, r in enumerate(d['rows']):
            if r.get('keluar'): continue
            mid = r.get('id_kaedah') or ''
            if not mid.startswith('M'): continue
            kerja.setdefault(mid, []).append((ak, k))
    log = []
    for mid, lst in sorted(kerja.items()):
        m = importlib.import_module(f'kaedah.{mid}')
        tick = {out[ak]['rows'][k]['saham'] for ak, k in lst}
        if m.SILANG:
            fr = {t: g.copy() for t, g in fr0.items() if len(g) >= 60}
        else:
            fr = {t: fr0[t].copy() for t in tick if t in fr0}
        try:
            m.sedia(fr, idx)
        except Exception as e:
            log.append(f'{mid}: sedia gagal {e}'); continue
        tmax = getattr(m, 'TMAX', None)
        for ak, k in lst:
            r = out[ak]['rows'][k]; g = fr.get(r['saham'])
            if g is None or 'sig' not in g:
                log.append(f'{ak} {mid} {r["saham"]}: tiada data'); r['_nota'] = 'tiada data'; continue
            for c in ['stop', 'tgt', 'exitc']:
                if c not in g: g[c] = np.nan if c != 'exitc' else False
            ti = r.get('tarikh_isyarat') or str(sesi_sebelum(r['tarikh_beli']).date())
            x, sp = keluar(g, ti, r['harga_beli'], tmax)
            r['_x'] = None if x is None else {kk: (str(v.date()) if isinstance(v, pd.Timestamp) else v) for kk, v in x.items()}
            r['_sp'] = None if sp is None or (isinstance(sp, float) and not np.isfinite(sp)) else float(sp)
            r['_tgt'] = None if np.isnan(g['tgt'].iloc[-1]) else float(g['tgt'].iloc[-1])
    json.dump(out, open(os.path.join(SP, 'nilai_out.json'), 'w'), default=str)
    print('\n'.join(log))

main()
