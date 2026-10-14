from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M19'
NAMA = 'Sneaky Pivot (proksi harian)'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = 20
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _kunci(g, sig, stop, T, warm, tmax=None, ex=None):
    """Cermin gelung trades() enjin supaya lajur tgt kekal pada nilai hari isyarat sepanjang dagangan
    (laporan M19: sasaran dikunci pada hari isyarat, isian ke hadapan daripada isyarat yang diambil)."""
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g); tg = np.full(n, np.nan); ex = np.zeros(n, bool) if ex is None else ex
    i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        Ti = T[i]; sp = stop[i] if not np.isnan(stop[i]) else -np.inf
        j = i + 1; keluar = False
        while j < n:
            if j > i + 1 and o[j] <= sp: keluar = True; break
            if l[j] <= sp: keluar = True; break
            if not np.isnan(Ti) and j > i + 1 and (o[j] >= Ti or h[j] >= Ti): keluar = True; break
            if ex[j] and j + 1 < n: j += 1; keluar = True; break
            if tmax and (j - i) >= tmax: keluar = True; break
            j += 1
        if not keluar: j = n - 1
        tg[i:j + 1] = Ti
        i = j + 1
    tg[n - 1] = T[n - 1] if sig[n - 1] else tg[n - 1]
    return tg


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        RL20 = l.shift(3).rolling(20).min(); RH20 = h.shift(3).rolling(20).max()
        stop = 0.99 * np.minimum(l.shift(2), l.shift(1))
        sig = (l.shift(2) <= RL20) & (c.shift(1) > o.shift(1)) & (c > h.shift(1)) & (c < RH20)
        # Kad: langkau jika buka masuk <= henti atau >= sasaran
        lk = ((o.shift(-1) <= stop) | (o.shift(-1) >= RH20)).fillna(False)
        sig = (sig & ~lk).fillna(False)
        g['_RL20'] = RL20; g['_RH20'] = RH20
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _kunci(g, sig.values, stop.values.astype(float), RH20.values.astype(float), WARM, TMAX)
        g['exitc'] = False
        # Laporan: isyarat tanpa ROC63 diletak paling bawah
        g['rank'] = (c / c.shift(63) - 1).fillna(-9.0)


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V1 (kod sedia, PADAN registry), N=4, dinilai untuk esok (i+1):
    1 lilin A (hari ini−1) low <= RL20 (min low 20 hari sebelum A); 2 lilin B (hari ini) hijau;
    3 ruang: high hari ini < RH20 (tutup esok boleh < RH20); 4 PENCETUS tutup esok > high hari ini."""
    if len(g) < 30: return None
    r = g.iloc[-1]
    if bool(r.sig): return None
    l, h, o, c = g.low, g.high, g.open, g.close
    RL = l.iloc[-22:-2].min(); RH = h.iloc[-22:-2].max()     # RL20/RH20 esok = shift(3) rolling 20
    if not (l.iloc[-2] <= RL and c.iloc[-1] > o.iloc[-1]): return None   # 1, 2
    paras = h.iloc[-1]
    if not paras < RH: return None                                         # 3
    jarak = (paras - c.iloc[-1]) / c.iloc[-1] * 100
    if not (0 < jarak <= 2.0): return None
    henti = 0.99 * min(l.iloc[-2], l.iloc[-1])
    return {'sebab': f'Lilin A (semalam) sentuh low 20 hari ({RL:.2f}); lilin B (hari ini) hijau; high hari ini < RH20 ({RH:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high hari ini) dan < {RH:.2f} (RH20); henti {henti:.2f}, sasaran {RH:.2f}, had 20 hari; '
                           f'langkau jika buka masuk <= henti atau >= sasaran',
            'pencetus': 'Tutup > high lilin B', 'paras': round(float(paras), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}
