from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M59'
NAMA = 'Anjakan Julat RSI'
VARIAN = 'V3 V1 LB65 ambang 39/69 (imbasan Hill 2019)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
LB, BAWAH, ATAS = 65, 39, 69


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        r = rsi(g.close, 14)
        rmin = r.rolling(LB).min(); rmax = r.rolling(LB).max()
        k = (rmin > BAWAH) & (rmax > ATAS)
        g['_rsi'] = r; g['_rmin'] = rmin; g['_rmax'] = rmax
        g['sig'] = k & ~k.shift(1, fill_value=False)
        g['stop'] = g.close - 3 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = r < 40
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def _rsi_esok(au, ad, c0, x, n=14):
    d = x - c0
    a = au * (1 - 1 / n) + max(d, 0) / n; b = ad * (1 - 1 / n) + max(-d, 0) / n
    return 100.0 if b == 0 else 100 - 100 / (1 + a / b)


def _cari(au, ad, c0, sasar, naik=True):
    """Tutup esok minimum (naik=True) supaya RSI esok > sasar; carian binari (RSI menokok dengan tutup)."""
    lo, hi = c0 * 0.5, c0 * 1.5
    for _ in range(80):
        m = (lo + hi) / 2
        if _rsi_esok(au, ad, c0, m) > sasar: hi = m
        else: lo = m
    return hi


def hampir(g, idx):
    """Syarat entry V3 (N=3) untuk isyarat esok: [1] RSI14 terendah 65 hari (64 hari terakhir + esok) > 39
       [2] RSI14 tertinggi 65 hari > 69 [3] keadaan belum aktif hari ini (isyarat hanya hari pertama).
       PENCETUS = syarat [1] atau [2] yang belum dipenuhi:
       (a) [2] sudah, [1] belum hanya kerana bacaan RSI <= 39 berada di bar tertua tetingkap (keluar esok):
           pencetus = RSI esok > 39 (paras = tutup minimum esok); 
       (b) [1] sudah, [2] belum: pencetus = RSI esok > 69 (silang indikator; paras = tutup esok minimum)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._rmin) or np.isnan(r._rmax) or len(g) < PERLU_BAR:
        return None
    if (r._rmin > BAWAH) and (r._rmax > ATAS):
        return None                      # keadaan sudah aktif -> tiada isyarat baharu esok ([3] gagal)
    rs = g._rsi.values[-(LB - 1):]       # 64 bacaan yang kekal dalam tetingkap esok
    if np.isnan(rs).any():
        return None
    c = g.close; dl = c.diff()
    au = dl.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean().iloc[-1]
    ad = (-dl.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean().iloc[-1]
    c0 = float(r.close)
    mn, mx = rs.min(), rs.max()
    if mx > ATAS and mn > BAWAH:
        # (a) Andaian saya: pencetus jenis 'keluar tetingkap' dilayan seperti pencetus kalendar (jarak_pct = 0);
        #     paras = tutup esok minimum supaya RSI esok kekal > 39.
        paras = _cari(au, ad, c0, BAWAH)
        if paras > c0:
            return None
        return _hasil(f'RSI14 tertinggi tetingkap {mx:.1f} (> {ATAS}); 64 bacaan RSI terakhir semuanya > {BAWAH}; RSI14 kini {r._rsi:.1f}; '
                      f'bacaan RSI <= {BAWAH} terakhir keluar tetingkap esok',
                      f'Tutup esok > {paras:.2f} (RSI14 esok kekal > {BAWAH})', 'Anjakan julat (RSI <= 39 keluar tetingkap)',
                      paras, 0.0, 2, 3)
    if mn > BAWAH and mx <= ATAS:
        paras = _cari(au, ad, c0, ATAS)
        jarak = (paras - c0) / c0 * 100
        if jarak <= 0 or jarak > 2.0:
            return None
        return _hasil(f'RSI14 kekal > {BAWAH} selama {LB} hari; RSI14 kini {r._rsi:.1f} (tertinggi tetingkap {r._rmax:.1f}); keadaan belum aktif',
                      f'Tutup esok > {paras:.2f} (RSI14 silang ke atas {ATAS})', 'RSI14 silang > 69', paras, jarak, 2, 3)
    return None
