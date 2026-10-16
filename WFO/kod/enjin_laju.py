# Enjin laju — salinan logik trades() dan portfolio() enjin v1.2 (BacktestShariah2/kod/enjin.py) dalam numba.
# Enjin v1.2 kekal sumber kebenaran dan tidak diubah. Kesetaraan bait demi bait disahkan oleh
# WFO/kod/sahkan_enjin.py dan WFO/ujian/test_enjin_laju.py; sebarang beza = jangan guna enjin ini.
#
#   trades_laju(fr, tmax, warm)  ≡ enjin.trades(fr, tmax, warm)
#   portfolio_laju(T, fr)        ≡ enjin.portfolio(T, fr)          (slots=8, w=0.125)
#   Susun / Pasaran              — tatasusunan yang disediakan sekali untuk larian berulang (WFO)
import os, sys
import numpy as np, pandas as pd
from numba import njit

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..', '..', 'BacktestShariah2', 'kod'))
import enjin

SEBAB = ['hujung', 'henti', 'sasaran', 'isyarat keluar', 'masa']
LAJUR_T = ['ticker', 'sig', 'ent', 'ex', 'ret', 'days', 'why', 'rank', 'mfe']


@njit(cache=True)
def _trades(o, h, l, c, sig, st, tg, ex, mula, akhir, tmax, warm, cost):
    N = len(o)
    r_t = np.empty(N, np.int64); r_i = np.empty(N, np.int64); r_j = np.empty(N, np.int64)
    r_x = np.empty(N); r_w = np.empty(N, np.int64); r_mfe = np.empty(N); r_e = np.empty(N)
    k = 0
    for t in range(len(mula)):
        s = mula[t]; n = akhir[t] - s; i = warm
        while i < n - 1:
            if not sig[s + i]:
                i += 1; continue
            e = o[s + i + 1]
            sp = st[s + i]
            if np.isnan(sp): sp = -np.inf
            j = i + 1; jumpa = False; x = 0.0; why = 0
            while j < n:
                tgt = tg[s + j - 1] if j > i + 1 else np.nan
                if j > i + 1 and o[s + j] <= sp:
                    x = o[s + j]; why = 1; jumpa = True; break
                if l[s + j] <= sp:
                    x = sp; why = 1; jumpa = True; break
                if not np.isnan(tgt):
                    if j > i + 1 and o[s + j] >= tgt:
                        x = o[s + j]; why = 2; jumpa = True; break
                    if h[s + j] >= tgt:
                        x = tgt; why = 2; jumpa = True; break
                if ex[s + j] and j + 1 < n:
                    j += 1; x = o[s + j]; why = 3; jumpa = True; break
                if tmax > 0 and (j - i) >= tmax:
                    x = c[s + j]; why = 4; jumpa = True; break
                j += 1
            if not jumpa:
                j = n - 1; x = c[s + j]; why = 0
            # mfe = h[i+1:j+1].max()/e - 1 (NaN merebak seperti numpy)
            m = -np.inf; adanan = False
            for q in range(i + 1, j + 1):
                v = h[s + q]
                if np.isnan(v): adanan = True
                elif v > m: m = v
            if adanan: m = np.nan
            r_t[k] = t; r_i[k] = i; r_j[k] = j; r_x[k] = x; r_w[k] = why; r_mfe[k] = m; r_e[k] = e
            k += 1
            i = j + 1
    ret = np.empty(k); mfe = np.empty(k)
    for q in range(k):
        ret[q] = r_x[q] / r_e[q] * (1 - cost) / (1 + cost) - 1
        mfe[q] = r_mfe[q] / r_e[q] - 1
    return r_t[:k], r_i[:k], r_j[:k], ret, r_w[:k], mfe


class Susun:
    """Tatasusunan bersambung bagi semua saham (urutan dict fr dikekalkan)."""
    def __init__(self, fr):
        self.nama = list(fr); panjang = [len(g) for g in fr.values()]
        self.akhir = np.cumsum(panjang).astype(np.int64); self.mula = self.akhir - np.array(panjang, np.int64)
        cat = lambda f: np.concatenate([f(g) for g in fr.values()]) if fr else np.empty(0)
        self.tarikh = np.concatenate([g.index.values for g in fr.values()]) if fr else np.empty(0, 'datetime64[ns]')
        self.o, self.h, self.l, self.c = (cat(lambda g, k=k: g[k].values.astype(float)) for k in ('open', 'high', 'low', 'close'))
        self.sig = cat(lambda g: g.sig.fillna(False).astype(bool).values)
        self.rank = cat(lambda g: g['rank'].astype(float).values)

    def lajur(self, fr, nama):
        """Satu lajur (stop/tgt float, exitc bool) bersambung, dengan penukaran sama seperti enjin.trades."""
        if nama == 'exitc': return np.concatenate([g.exitc.fillna(False).astype(bool).values for g in fr.values()])
        return np.concatenate([g[nama].astype(float).values for g in fr.values()])

    def dagangan(self, st, tg, ex, tmax, warm):
        t, i, j, ret, w, mfe = _trades(self.o, self.h, self.l, self.c, self.sig, st, tg, ex,
                                       self.mula, self.akhir, int(tmax or 0), int(warm), enjin.COST)
        if len(t) == 0: return pd.DataFrame(columns=LAJUR_T)
        b = self.mula[t]
        return pd.DataFrame(dict(ticker=[self.nama[x] for x in t], sig=self.tarikh[b + i], ent=self.tarikh[b + i + 1],
                                 ex=self.tarikh[b + j], ret=ret, days=(j - i).astype(np.int64),
                                 why=[SEBAB[x] for x in w], rank=self.rank[b + i], mfe=mfe))


def trades_laju(fr, tmax=None, warm=200):
    fr = {t: enjin.siap(g) for t, g in fr.items()}
    s = Susun(fr)
    return s.dagangan(s.lajur(fr, 'stop'), s.lajur(fr, 'tgt'), s.lajur(fr, 'exitc'), tmax, warm)


@njit(cache=True)
def _jumlah_py(v, np_, n):
    """Tiru sum() CPython 3.12+ bagi jana nilai bermula dengan int 0: float tulen dijumlah secara Neumaier
    (mula item ke-2), numpy.float64 dijumlah biasa; pampasan ditambah sebelum bertukar ke laluan biasa.
    Pulang (nilai, adalah_numpy)."""
    if n == 0: return 0.0, False
    f = 0.0 + v[0]
    if np_[0]:
        for k in range(1, n): f = f + v[k]
        return f, True
    c = 0.0
    for k in range(1, n):
        if np_[k]:
            if c != 0.0 and np.isfinite(c): f += c
            f = f + v[k]
            for q in range(k + 1, n): f = f + v[q]
            return f, True
        x = v[k]; t = f + x
        if abs(f) >= abs(x): c += (f - t) + x
        else: c += (x - t) + f
        f = t
    if c != 0.0 and np.isfinite(c): f += c
    return f, False


@njit(cache=True)
def _portfolio(A, tk, ent, ex, ret, g0, g1, slots, w):
    # Logik enjin.portfolio v1.2. Jenis nilai (float Python lawan numpy.float64) dijejak kerana sum() Python
    # menjumlah float tulen secara terpampas: cash/eq/a bermula float; nilai asof() ialah numpy.float64;
    # ret daripada iterrows ialah float.
    D = A.shape[1]; curve = np.empty(D)
    p_t = np.empty(slots, np.int64); p_ex = np.empty(slots, np.int64); p_ret = np.empty(slots)
    p_a = np.empty(slots); p_ent = np.empty(slots, np.int64); p_np = np.zeros(slots, np.bool_); n = 0
    v = np.empty(slots); vn = np.zeros(slots, np.bool_)
    eq = 1.0; cash = 1.0; eq_np = False; cash_np = False
    for d in range(D):
        m = 0
        for q in range(n):
            if p_ex[q] == d:
                cash += p_a[q] * (1 + p_ret[q]); cash_np = cash_np or p_np[q]
            else:
                p_t[m] = p_t[q]; p_ex[m] = p_ex[q]; p_ret[m] = p_ret[q]; p_a[m] = p_a[q]; p_ent[m] = p_ent[q]; p_np[m] = p_np[q]; m += 1
        n = m
        for r in range(g0[d], g1[d]):
            if n >= slots: break
            ada = False
            for q in range(n):
                if p_t[q] == tk[r]:
                    ada = True; break
            if ada: continue
            a = cash; a_np = cash_np
            if eq * w < a:                     # min(cash, eq*w) Python
                a = eq * w; a_np = eq_np
            if a <= 0: break
            cash -= a; cash_np = cash_np or a_np
            p_t[n] = tk[r]; p_ex[n] = ex[r]; p_ret[n] = ret[r]; p_a[n] = a; p_ent[n] = d; p_np[n] = a_np; n += 1
        m = 0
        for q in range(n):
            if p_ex[q] == d and p_ent[q] == d:
                cash += p_a[q] * (1 + p_ret[q]); cash_np = cash_np or p_np[q]
            else:
                p_t[m] = p_t[q]; p_ex[m] = p_ex[q]; p_ret[m] = p_ret[q]; p_a[m] = p_a[q]; p_ent[m] = p_ent[q]; p_np[m] = p_np[q]; m += 1
        n = m
        for q in range(n):
            if p_ent[q] != d:
                v[q] = p_a[q] * A[p_t[q], d] / A[p_t[q], p_ent[q]]; vn[q] = True
            else:
                v[q] = p_a[q]; vn[q] = p_np[q]
        if n == 0:
            eq = cash + 0.0; eq_np = cash_np
        else:
            mv, mv_np = _jumlah_py(v, vn, n)
            eq = cash + mv; eq_np = cash_np or mv_np
        curve[d] = eq
    return curve


class Pasaran:
    """Tarikh (>= START) dan matriks harga tutup 'asof' (abaikan NaN, seperti Series.asof) bagi satu fr."""
    def __init__(self, fr):
        mula = pd.Timestamp(enjin.START)
        # = sorted(set().union(*indeks)) ditapis >= START, tetapi dalam numpy
        semua = pd.DatetimeIndex(np.unique(np.concatenate([g.index.values for g in fr.values()]))) if fr else pd.DatetimeIndex([])
        self.tarikh = semua[semua >= mula]
        self.kod = {t: k for k, t in enumerate(fr)}
        self.A = np.full((len(fr), len(self.tarikh)), np.nan)
        for t, k in self.kod.items():
            s = fr[t].close.dropna()
            if len(s): self.A[k] = s.reindex(self.tarikh, method='ffill').values
        self.pos = pd.Series(np.arange(len(self.tarikh)), self.tarikh)

    def lengkung(self, T, slots=8, w=0.125):
        if len(T): T = T[T.ent >= pd.Timestamp(enjin.START)].sort_values(['ent', 'rank'], ascending=[True, False])
        D = len(self.tarikh)
        tk = (T.ticker.astype(object).map(self.kod).fillna(-1).values.astype(np.int64) if len(T)
              else np.empty(0, np.int64))
        en = self.pos.reindex(T.ent).fillna(-1).values.astype(np.int64) if len(T) else np.empty(0, np.int64)
        ek = self.pos.reindex(T.ex).fillna(-1).values.astype(np.int64) if len(T) else np.empty(0, np.int64)
        ret = T.ret.values.astype(float) if len(T) else np.empty(0)
        # baris bagi setiap tarikh masuk (T disusun ikut ent → baris setarikh bersebelahan)
        g0 = np.zeros(D, np.int64); g1 = np.zeros(D, np.int64)
        for r in range(len(en) - 1, -1, -1):
            d = en[r]
            if d < 0: continue
            if g1[d] == 0: g1[d] = r + 1
            g0[d] = r
        sah = tk >= 0
        if not sah.all():   # saham tiada dalam fr → enjin asal akan gagal (KeyError); kekalkan tingkah laku
            raise KeyError('saham dalam T tiada dalam fr')
        return pd.Series(_portfolio(self.A, tk, en, ek, ret, g0, g1, slots, w), index=self.tarikh)


def portfolio_laju(T, fr, slots=8, w=0.125):
    return Pasaran(fr).lengkung(T, slots, w)
