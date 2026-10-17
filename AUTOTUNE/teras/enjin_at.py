# Enjin autotune (SPEC A01 §3). Asas: WFO/kod/enjin_laju.py (setara enjin v1.2), disalin di sini supaya
# AUTOTUNE tidak mengimport WFO/ semasa larian. Perbezaan (setiap satu boleh dimatikan; semua dimatikan
# = enjin v1.2 bait demi bait, disahkan AUTOTUNE/ujian/test_enjin_at.py):
#   gap    — hari masuk: jika buka <= henti, keluar pada buka itu juga (sebab 'henti').
#   kos    — kos setiap sisi = 0.001 + slippage ikut median 20 hari (tutup x volum) pada hari isyarat:
#            >= 5e7 → 0.0005; >= 1e7 → 0.0010; selain itu (atau NaN) → 0.0025.
#   had60  — pegangan maksimum 60 hari dagangan: tmax = min(TMAX, 60) (TMAX None/0 → 60).
#   topeng — isyarat sah hanya jika topeng (universe bulan itu & kumpulan) benar.
#   mula/akhir — hanya kemasukan dalam [mula, akhir]; data selepas akhir diabaikan (posisi terbuka ditutup
#            pada tutup bar terakhir <= akhir, sebab 'hujung'); dagangan sebelum mula tidak menyekat.
# Portfolio: 8 slot x 12.5%, susunan ikut rank (tertinggi dahulu), satu posisi setiap ticker (v1.2).
import numpy as np, pandas as pd
from numba import njit

COST = 0.001            # komisen setiap sisi (= enjin v1.2 COST)
START = '2019-11-01'    # START enjin v1.2 (hanya untuk mod setara)
HAD_HARI = 60
SLIP = ((5e7, 0.0005), (1e7, 0.0010), (0.0, 0.0025))
SEBAB = ['hujung', 'henti', 'sasaran', 'isyarat keluar', 'masa']
LAJUR_T = ['ticker', 'sig', 'ent', 'ex', 'ret', 'days', 'why', 'rank', 'mfe', 'kos']


def siap(g):
    for k, v in [('sig', False), ('stop', np.nan), ('tgt', np.nan), ('exitc', False), ('rank', 0.0)]:
        if k not in g: g[k] = v
    return g


def kos_sisi(medv):
    """Kos setiap sisi bagi tatasusunan median nilai dagangan 20 hari."""
    m = np.nan_to_num(np.asarray(medv, float), nan=-1.0)
    return COST + np.where(m >= SLIP[0][0], SLIP[0][1], np.where(m >= SLIP[1][0], SLIP[1][1], SLIP[2][1]))


@njit(cache=True)
def _trades(o, h, l, c, sig, st, tg, ex, kos, mula, akhir, i0, n1, tmax, warm, gap):
    N = len(o)
    r_t = np.empty(N, np.int64); r_i = np.empty(N, np.int64); r_j = np.empty(N, np.int64)
    r_x = np.empty(N); r_w = np.empty(N, np.int64); r_mfe = np.empty(N); r_e = np.empty(N); r_k = np.empty(N)
    k = 0
    for t in range(len(mula)):
        s = mula[t]; n = n1[t]; i = max(warm, i0[t] - 1)
        while i < n - 1:
            if not sig[s + i]:
                i += 1; continue
            e = o[s + i + 1]
            sp = st[s + i]
            if np.isnan(sp): sp = -np.inf
            j = i + 1; jumpa = False; x = 0.0; why = 0
            while j < n:
                tgt = tg[s + j - 1] if j > i + 1 else np.nan
                if (j > i + 1 or gap) and o[s + j] <= sp:
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
            m = -np.inf; adanan = False
            for q in range(i + 1, j + 1):
                v = h[s + q]
                if np.isnan(v): adanan = True
                elif v > m: m = v
            if adanan: m = np.nan
            r_t[k] = t; r_i[k] = i; r_j[k] = j; r_x[k] = x; r_w[k] = why; r_mfe[k] = m; r_e[k] = e
            r_k[k] = kos[s + i]
            k += 1
            i = j + 1
    ret = np.empty(k); mfe = np.empty(k)
    for q in range(k):
        ret[q] = r_x[q] / r_e[q] * (1 - r_k[q]) / (1 + r_k[q]) - 1
        mfe[q] = r_mfe[q] / r_e[q] - 1
    return r_t[:k], r_i[:k], r_j[:k], ret, r_w[:k], mfe, r_k[:k]


class Asas:
    """Tatasusunan harga bersambung (tarikh, o, h, l, c, medv) — tidak bergantung parameter; dikira sekali."""
    def __init__(self, fr):
        self.nama = list(fr); self.panjang = [len(g) for g in fr.values()]
        cat = lambda f, d=float: np.concatenate([f(g) for g in fr.values()]) if fr else np.empty(0, d)
        self.tarikh = (np.concatenate([g.index.values for g in fr.values()]) if fr
                       else np.empty(0, 'datetime64[ns]'))
        self.o, self.h, self.l, self.c = (cat(lambda g, k=k: g[k].values.astype(float)) for k in ('open', 'high', 'low', 'close'))
        self.medv = medv_bersambung(fr)

    def sejajar(self, fr):
        return list(fr) == self.nama and [len(g) for g in fr.values()] == self.panjang


class Susun:
    """Tatasusunan bersambung bagi fr yang sudah melalui sedia() (urutan dict dikekalkan).
    topeng: None, atau dict ticker -> bool Series/array sejajar g.index (isyarat di luar topeng dibuang).
    asas: Asas bagi data yang sama (harga + medv dikira sekali); None → dikira di sini."""
    def __init__(self, fr, topeng=None, asas=None):
        fr = {t: siap(g) for t, g in fr.items()}
        if asas is not None and not asas.sejajar(fr): asas = None
        if asas is None: asas = Asas(fr)
        self.nama = asas.nama; self._q = {t: q for q, t in enumerate(self.nama)}
        self.akhir = np.cumsum(asas.panjang).astype(np.int64); self.mula = self.akhir - np.array(asas.panjang, np.int64)
        cat = lambda f, d=float: np.concatenate([f(g) for g in fr.values()]) if fr else np.empty(0, d)
        self.tarikh, self.o, self.h, self.l, self.c, self.medv = asas.tarikh, asas.o, asas.h, asas.l, asas.c, asas.medv
        sig = cat(lambda g: g.sig.fillna(False).astype(bool).values, bool)
        if topeng is not None:
            sig = sig & np.concatenate([_topeng(topeng, t, g) for t, g in fr.items()]) if fr else sig
        self.sig = sig
        self.st = cat(lambda g: g['stop'].astype(float).values)
        self.tg = cat(lambda g: g['tgt'].astype(float).values)
        self.ex = cat(lambda g: g.exitc.fillna(False).astype(bool).values, bool)
        self.rank = cat(lambda g: g['rank'].astype(float).values)

    def dengan_topeng(self, topeng):
        """Salinan cetek dengan isyarat ditapis topeng (sedia() sekali, beberapa kumpulan)."""
        import copy
        b = copy.copy(self)
        if isinstance(topeng, np.ndarray):
            if len(topeng) != len(self.sig): raise ValueError('topeng tidak sejajar')
            b.sig = self.sig & topeng
        elif topeng is not None and len(self.nama):
            b.sig = self.sig & np.concatenate([_topeng(topeng, t, self._g(t)) for t in self.nama])
        return b

    def _g(self, t):
        q = self._q[t]
        return pd.DataFrame(index=pd.DatetimeIndex(self.tarikh[self.mula[q]:self.akhir[q]]))

    def _sempadan(self, mula, akhir):
        i0 = np.zeros(len(self.mula), np.int64); n1 = (self.akhir - self.mula).copy()
        if mula is None and akhir is None: return i0, n1
        m = np.datetime64(pd.Timestamp(mula), 'ns') if mula is not None else None
        a = np.datetime64(pd.Timestamp(akhir), 'ns') if akhir is not None else None
        for t in range(len(self.mula)):
            d = self.tarikh[self.mula[t]:self.akhir[t]]
            if m is not None: i0[t] = np.searchsorted(d, m, 'left')
            if a is not None: n1[t] = np.searchsorted(d, a, 'right')
        return i0, n1

    def dagangan(self, tmax=None, warm=200, mula=None, akhir=None, gap=True, kos=True, had60=True):
        tm = int(tmax or 0)
        if had60: tm = HAD_HARI if tm <= 0 else min(tm, HAD_HARI)
        k = kos_sisi(self.medv) if kos else np.full(len(self.o), COST)
        i0, n1 = self._sempadan(mula, akhir)
        t, i, j, ret, w, mfe, kk = _trades(self.o, self.h, self.l, self.c, self.sig, self.st, self.tg, self.ex, k,
                                           self.mula, self.akhir, i0, n1, tm, int(warm), bool(gap))
        if len(t) == 0: return pd.DataFrame(columns=LAJUR_T)
        b = self.mula[t]
        return pd.DataFrame(dict(ticker=[self.nama[x] for x in t], sig=self.tarikh[b + i], ent=self.tarikh[b + i + 1],
                                 ex=self.tarikh[b + j], ret=ret, days=(j - i).astype(np.int64),
                                 why=[SEBAB[x] for x in w], rank=self.rank[b + i], mfe=mfe, kos=kk))


def medv_bersambung(fr):
    """Median 20 hari (tutup × volum) bagi setiap saham, bersambung ikut urutan fr."""
    if not fr: return np.empty(0)
    return np.concatenate([(g.close.astype(float) * g.volume.astype(float)).rolling(20).median().values
                           if 'volume' in g else np.full(len(g), np.nan) for g in fr.values()])


def topeng_bersambung(tp, fr):
    """Topeng bersambung ikut urutan fr (dict ticker -> Series/array, atau callable(g, t))."""
    if not fr: return np.empty(0, bool)
    return np.concatenate([_topeng(tp, t, g) for t, g in fr.items()])


def _topeng(tp, t, g):
    if callable(tp): v = tp(g, t)
    else: v = tp.get(t)
    if v is None: return np.zeros(len(g), bool)
    if isinstance(v, pd.Series): v = v.reindex(g.index).fillna(False).values
    return np.asarray(v, bool)


def trades(fr, tmax=None, warm=200, **kw):
    """Setara enjin.trades apabila gap=kos=had60=False dan tiada topeng/mula/akhir."""
    tp = kw.pop('topeng', None)
    return Susun(fr, tp).dagangan(tmax, warm, **kw)


@njit(cache=True)
def _jumlah_py(v, np_, n):
    """Tiru sum() CPython 3.12+ (lihat enjin_laju): float tulen dijumlah Neumaier, numpy.float64 biasa."""
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
            if eq * w < a:
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
    """Tarikh dalam [mula, akhir] (gabungan indeks semua saham) dan matriks tutup 'asof' (ffill).
    mula=None → START v1.2 (mod setara). Bina sekali bagi setiap (data, tetingkap); guna semula setiap percubaan."""
    def __init__(self, fr, mula=None, akhir=None):
        self.mula = pd.Timestamp(mula if mula is not None else START)
        self.akhir = pd.Timestamp(akhir) if akhir is not None else None
        semua = (pd.DatetimeIndex(np.unique(np.concatenate([g.index.values for g in fr.values()])))
                 if fr else pd.DatetimeIndex([]))
        k = semua >= self.mula
        if self.akhir is not None: k &= semua <= self.akhir
        self.tarikh = semua[k]
        self.kod = {t: q for q, t in enumerate(fr)}
        self.A = np.full((len(fr), len(self.tarikh)), np.nan)
        for t, q in self.kod.items():
            s = fr[t].close.dropna()
            if len(s): self.A[q] = s.reindex(self.tarikh, method='ffill').values
        self.pos = pd.Series(np.arange(len(self.tarikh)), self.tarikh)

    def lengkung(self, T, slots=8, w=0.125):
        if len(T):
            k = T.ent >= self.mula
            if self.akhir is not None: k &= T.ent <= self.akhir
            T = T[k].sort_values(['ent', 'rank'], ascending=[True, False])
        D = len(self.tarikh)
        if len(T):
            tk = T.ticker.astype(object).map(self.kod).fillna(-1).values.astype(np.int64)
            en = self.pos.reindex(T.ent).fillna(-1).values.astype(np.int64)
            ek = self.pos.reindex(T.ex).fillna(-1).values.astype(np.int64)
            ret = T.ret.values.astype(float)
        else:
            tk = en = ek = np.empty(0, np.int64); ret = np.empty(0)
        g0 = np.zeros(D, np.int64); g1 = np.zeros(D, np.int64)
        for r in range(len(en) - 1, -1, -1):
            d = en[r]
            if d < 0: continue
            if g1[d] == 0: g1[d] = r + 1
            g0[d] = r
        if not (tk >= 0).all(): raise KeyError('saham dalam T tiada dalam fr')
        return pd.Series(_portfolio(self.A, tk, en, ek, ret, g0, g1, slots, w), index=self.tarikh)


def portfolio(T, fr, slots=8, w=0.125, mula=None, akhir=None):
    """Setara enjin.portfolio apabila mula/akhir None."""
    return Pasaran(fr, mula, akhir).lengkung(T, slots, w)


def pulangan_harian(cv):
    """Pulangan harian lengkung (modal awal 1.0)."""
    if cv is None or len(cv) == 0: return pd.Series(dtype=float)
    r = cv / cv.shift(1) - 1
    r.iloc[0] = cv.iloc[0] - 1
    return r
