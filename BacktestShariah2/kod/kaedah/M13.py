from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M13'
NAMA = 'Garis Trend Action/Safety Line'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
K = 3          # pivot k=3
WIN = 252      # tetingkap 252 hari


def _pivot(a, k, fn):
    p = np.zeros(len(a), bool)
    for t in range(k, len(a) - k):
        if a[t] == fn(a[t - k:t + k + 1]): p[t] = True
    return np.where(p)[0]


def _garis(Y, piv, upper):
    """Untuk setiap hari i: segmen terakhir kulit cembung (atas jika upper) atas bar [m, P],
    m = indeks ekstrem tetingkap (pertama jika seri), P = pivot disahkan terakhir (P <= i-K, P >= w0).
    Andaian saya (ikut laporan M13): tetingkap dipendekkan ke mula data bila sejarah < 252 hari.
    Pulang nilai garis pada i, indeks B, dan nilai ekstrem tetingkap (untuk garis naik mendatar)."""
    n = len(Y); val = np.full(n, np.nan); Bi = np.full(n, -1); ext = np.full(n, np.nan)
    nxt = np.full(n, np.nan)   # pembantu hampir: nilai garis pada i+1 (segmen sama)
    st = []; cur_m = -1; cur_P = -1; pj = 0; lastp = -1
    for i in range(n):
        w0 = max(0, i - WIN + 1)
        seg = Y[w0:i + 1]
        m = w0 + (int(np.argmax(seg)) if upper else int(np.argmin(seg)))
        ext[i] = Y[m]
        while pj < len(piv) and piv[pj] <= i - K: lastp = piv[pj]; pj += 1
        if lastp < w0 or lastp <= m:
            continue
        P = lastp
        if m != cur_m or P < cur_P:
            st = []; cur_m = m; cur_P = m - 1
        for t in range(cur_P + 1, P + 1):
            y = Y[t]
            while len(st) >= 2:
                (t1, y1), (t2, y2) = st[-2], st[-1]; cr = (t2 - t1) * (y - y1) - (y2 - y1) * (t - t1)
                if (upper and cr >= 0) or (not upper and cr <= 0): st.pop()
                else: break
            st.append((t, y))
        cur_P = P
        (A, ya), (B, yb) = st[-2], st[-1]
        val[i] = ya + (yb - ya) * (i - A) / (B - A); Bi[i] = B
        nxt[i] = ya + (yb - ya) * (i + 1 - A) / (B - A)
    _garis.nxt = nxt
    return val, Bi, ext


def _kira(g):
    H, L, C = g.high.values.astype(float), g.low.values.astype(float), g.close.values.astype(float)
    D, Bd, _ = _garis(H, _pivot(H, K, np.max), True)
    _kira.Dn = _garis.nxt
    U, _, lmin = _garis(L, _pivot(L, K, np.min), False)
    U = np.where(np.isnan(U), lmin, U)          # tiada swing low selepas low terendah -> garis mendatar
    n = len(C); sg = np.zeros(n, bool); pecah = set()
    for i in range(n):
        if np.isnan(D[i]) or C[i] <= D[i]: continue
        if Bd[i] not in pecah: sg[i] = True
        pecah.add(Bd[i])
    return sg, D, Bd, U, pecah


def sedia(fr, idx):
    for g in fr.values():
        sg, D, Bd, U, pecah = _kira(g)
        stop = pd.Series(U, g.index)
        sig = pd.Series(sg, g.index) & ~(g.open.shift(-1) <= stop)   # langkau jika buka masuk <= henti
        g['_Dn'] = _kira.Dn; g['_D'] = D; g['_Bd'] = Bd; g['_U'] = U
        g['_dipecah'] = [b in pecah and b >= 0 for b in Bd]
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < stop
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Piawaian KETAT. Syarat entry V1 (N=2):
    1 garis trend turun (action line) wujud dan belum pernah dipecah sejak B; 2 PENCETUS: tutup > garis."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._D) or np.isnan(r._Dn) or bool(r._dipecah):
        return None
    # Andaian saya: tiada swing high baharu disahkan esok dan high tertinggi 252 hari tidak berubah (garis esok = segmen sama dilanjutkan).
    paras = float(r._Dn)
    jarak = (paras - r.close) / r.close * 100
    if jarak <= 0 or jarak > 2.0:
        return None
    return {'sebab': f'Garis trend turun aktif (nilai hari ini {r._D:.2f}) dan belum pernah dipecah; tutup ({r.close:.2f}) di bawah garis',
            'syarat_beli': f'Tutup esok > {paras:.2f} (garis trend turun esok); henti = garis naik {r._U:.2f}',
            'pencetus': 'Tutup atas garis trend turun', 'paras': round(paras, 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '1/2', 'skor': round(1 - jarak / 2, 2)}
