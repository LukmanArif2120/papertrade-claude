from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M01'
NAMA = 'Bollinger Band + RSI'
VARIAN = 'V0 Video tulen'
TMAX = None
WARM = 200
ADA_HENTI = False      # V0 sumber tulen: tiada henti rugi
SILANG = False
PERLU_BAR = 230


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        bbm = c.rolling(30).mean(); sd = c.rolling(30).std(ddof=0)
        bbl = bbm - 2 * sd
        r13 = rsi(c, 13)
        g['_bbl'] = bbl; g['_rsi13'] = r13
        g['sig'] = ((c < bbl) & (r13 < 25)).fillna(False)
        g['stop'] = np.nan                      # V0: tiada henti
        g['tgt'] = bbm                          # sasaran SMA30 bergerak (enjin baca nilai semalam)
        g['exitc'] = False
        g['rank'] = -r13                        # RSI paling rendah dahulu



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V0 (N=2): [1] tutup < band bawah BB(30,2) [2] RSI13 Wilder < 25.
       Pencetus = syarat yang belum dipenuhi; yang satu lagi mesti sudah dipenuhi hari ini.
       Paras = tutup esok TERTINGGI yang menjadikan KEDUA-DUA syarat benar (band dan RSI dikira dengan tutup esok)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._bbl) or np.isnan(r._rsi13) or len(g) < 60:
        return None
    a1, a2 = r.close < r._bbl, r._rsi13 < 25
    if a1 == a2:                       # kedua-dua belum (terlalu jauh) atau kedua-dua sudah (= sig)
        return None
    c = g.close.values
    dl = g.close.diff(); al = 1 / 13
    au = float(dl.clip(lower=0).ewm(alpha=al, adjust=False).mean().iloc[-1])
    ad = float((-dl.clip(upper=0)).ewm(alpha=al, adjust=False).mean().iloc[-1])
    w29 = c[-29:]
    def ok(x):
        w = np.append(w29, x); bbl = w.mean() - 2 * w.std()
        d = x - c[-1]; u = au * (1 - al) + al * max(d, 0); v = ad * (1 - al) + al * max(-d, 0)
        rs = 100.0 if v == 0 else 100 - 100 / (1 + u / v)
        return x < bbl and rs < 25
    c0 = float(c[-1]); lo = 0.98 * c0
    if not ok(lo):
        return None                    # perlu jatuh > 2%
    if ok(c0):
        paras = c0                     # tutup esok sama dengan hari ini pun mencetuskan
    else:
        hi = c0
        for _ in range(50):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if ok(m) else (lo, m)
        paras = lo
    jarak = max(0.0, (c0 - paras) / c0 * 100)
    # Andaian saya: jarak = 0 jika paras >= tutup semasa (pencetus berlaku walaupun harga tidak berubah)
    if a2:
        sebab = f'RSI13 = {r._rsi13:.1f} (< 25, terlebih jual); tutup {c0:.2f} masih di atas band bawah BB(30,2) {r._bbl:.2f}'
        pc = 'Tutup < band bawah BB(30,2)'
    else:
        sebab = f'Tutup {c0:.2f} di bawah band bawah BB(30,2) {r._bbl:.2f}; RSI13 = {r._rsi13:.1f} (belum < 25)'
        pc = 'RSI13 < 25'
    return _hasil(sebab, f'Tutup esok <= {paras:.2f} (band bawah BB30 dan RSI13 < 25 dikira dengan tutup esok)',
                  pc, paras, jarak, 1, 2)
