# Metrik dan objektif penalaan (SPEC A01 §4–§5).
# Lengkung cv: ekuiti portfolio harian dengan modal awal 1.0 (hari pertama tetingkap sudah termasuk pulangannya).
import math
from itertools import combinations
from statistics import NormalDist
import numpy as np, pandas as pd

MDD_HAD = -0.30
N_MIN = 30
HARI_MIN, HARI_MAKS = 2, 60
_N = NormalDist()


def _sah(cv):
    return cv is not None and len(cv) > 0 and np.isfinite(cv.values).all()


def cagr(cv):
    """(ekuiti akhir / 1.0)^(1/tahun) − 1; tahun = (hari kalendar tetingkap + 1) / 365.25."""
    if not _sah(cv): return -1.0
    akhir = float(cv.iloc[-1])
    if akhir <= 0: return -1.0
    y = ((cv.index[-1] - cv.index[0]).days + 1) / 365.25
    return akhir ** (1 / y) - 1


def mdd(cv):
    """Kejatuhan maksimum termasuk modal awal 1.0."""
    if not _sah(cv): return -1.0
    v = np.concatenate([[1.0], cv.values.astype(float)])
    return float((v / np.maximum.accumulate(v) - 1).min())


def tahunan(cv):
    """Pulangan setiap tahun kalendar (tahun separa dikira atas bahagian dalam tetingkap)."""
    if not _sah(cv): return {}
    a = cv.groupby(cv.index.year).last()
    sebelum = np.concatenate([[1.0], a.values[:-1]])
    return {int(y): float(v) for y, v in zip(a.index, a.values / sebelum - 1)}


def ringkas(T, cv):
    """Metrik satu tetingkap: cagr, mdd, n, win, avg, days, thn_min, tahunan."""
    n = int(len(T)) if T is not None else 0
    th = tahunan(cv)
    m = dict(cagr=cagr(cv), mdd=mdd(cv), n=n,
             win=float((T.ret > 0).mean()) if n else None, avg=float(T.ret.mean()) if n else None,
             days=float(T.days.mean()) if n else None,
             thn_min=min(th.values()) if th else -1.0, tahunan=th)
    return m


def lulus(m):
    d = m.get('days')
    return (m['mdd'] >= MDD_HAD and m['n'] >= N_MIN and d is not None and HARI_MIN <= d <= HARI_MAKS)


def skor(m):
    """Objektif: CAGR jika lulus kekangan; jika tidak −1 + CAGR − 2 × lebihan MDD."""
    if lulus(m): return float(m['cagr'])
    return float(-1 + m['cagr'] - 2 * max(0.0, MDD_HAD - m['mdd']))


def pilih_teguh(rekod, k=10):
    """rekod: senarai dict (skor, lulus, thn_min, ...). Antara k teratas yang lulus, pilih thn_min tertinggi
    (seri: skor). Tiada yang lulus → skor tertinggi. Pulang (rekod_dipilih, ada_lulus)."""
    ok = [r for r in rekod if r.get('lulus')]
    if not ok:
        return (max(rekod, key=lambda r: r['skor']) if rekod else None), False
    atas = sorted(ok, key=lambda r: r['skor'], reverse=True)[:k]
    return max(atas, key=lambda r: (r['thn_min'], r['skor'])), True


# ---------- A02 (SPEC_A02 §2): pulangan berlebihan atas SPY tempoh sama ----------
# Fungsi A01 di atas tidak berubah (lalai). A02 memakai fungsi *_a02 di bawah sahaja.
MDD_LONGGAR_A02 = 0.10      # MDD portfolio >= MDD SPY tempoh sama − 10 mata peratus
N_MIN_A02 = 30              # >= 30 dagangan yang benar-benar dipegang portfolio


def spy_lengkung(spy_tutup, tarikh):
    """Lengkung SPY (modal awal 1.0) atas tarikh yang SAMA dengan lengkung portfolio: pulangan hari pertama =
    tutup hari itu / tutup sebelumnya (asof) − 1, seperti portfolio yang hari pertamanya sudah termasuk pulangan.
    Hari tanpa tutup SPY dibawa ke hadapan (pulangan 0)."""
    tarikh = pd.DatetimeIndex(tarikh)
    c = pd.Series(spy_tutup, dtype=float).dropna().sort_index()
    if not len(tarikh): return pd.Series(dtype=float)
    sebelum = c[c.index < tarikh[0]]
    asas = float(sebelum.iloc[-1]) if len(sebelum) else np.nan
    v = c.reindex(c.index.union(tarikh)).ffill().reindex(tarikh)
    if not np.isfinite(asas): asas = float(v.iloc[0]) if np.isfinite(v.iloc[0]) else np.nan
    v = v.bfill()
    return v / asas


def tahunan_lebih(cv, spy_cv):
    """Pulangan berlebihan setiap tahun kalendar: tahun portfolio − tahun SPY (tarikh sama)."""
    a, b = tahunan(cv), tahunan(spy_cv)
    return {y: a[y] - b.get(y, 0.0) for y in a}


def ringkas_a02(T, cv, spy_cv):
    """Metrik A02 satu tetingkap. T = dagangan yang DIPEGANG portfolio (enjin_at.Pasaran.lengkung(pegang=True)).
    lebihan = CAGR portfolio − CAGR SPY; thn_min = pulangan berlebihan tahun kalendar terburuk."""
    m = ringkas(T, cv)
    m['spy_cagr'] = cagr(spy_cv); m['spy_mdd'] = mdd(spy_cv)
    m['lebihan'] = m['cagr'] - m['spy_cagr']
    tl = tahunan_lebih(cv, spy_cv) if _sah(cv) and _sah(spy_cv) else {}
    m['tahunan_lebih'] = tl
    m['thn_min'] = min(tl.values()) if tl else -1.0
    return m


def lulus_a02(m):
    return m['n'] >= N_MIN_A02 and m['mdd'] >= m['spy_mdd'] - MDD_LONGGAR_A02


def skor_a02(m):
    """Objektif A02: lebihan jika lulus; jika tidak −1 + lebihan − 2 × lebihan MDD atas had (MDD SPY − 0.10)."""
    if lulus_a02(m): return float(m['lebihan'])
    return float(-1 + m['lebihan'] - 2 * max(0.0, (m['spy_mdd'] - MDD_LONGGAR_A02) - m['mdd']))


def panas_a02(m, hari_min=400, faktor=1.6):
    """Pemanasan latih A02 (hari kalendar) = maksimum(400, 1.6 × (tetingkap terpanjang dalam julat atas + WARM)).
    Tetingkap terpanjang = nilai int terbesar antara had atas JULAT (int) dan PARAM int (parameter beku termasuk);
    parameter ambang (nama mengandungi 'ambang', cth. nilai dagangan USD) bukan tetingkap dan diabaikan."""
    w = 0
    for k, (jenis, lo, hi) in (getattr(m, 'JULAT', {}) or {}).items():
        if jenis == 'int' and 'ambang' not in k: w = max(w, int(hi))
    for k, v in (getattr(m, 'PARAM', {}) or {}).items():
        if isinstance(v, (int, np.integer)) and not isinstance(v, bool) and 'ambang' not in k: w = max(w, int(v))
    warm = int(getattr(m, 'WARM', 0) or 0)
    return int(max(hari_min, math.ceil(faktor * (w + warm))))


# ---------- DSR (salinan formula WFO/kod/wfo_laporan.py) ----------
def sharpe(r):
    """(SR harian, kecondongan, kurtosis (bukan lebihan), n) bagi pulangan harian."""
    r = pd.Series(r, dtype=float).dropna()
    if len(r) < 30 or r.std() == 0: return float('nan'), float('nan'), float('nan'), len(r)
    return float(r.mean() / r.std()), float(r.skew()), float(r.kurt() + 3), len(r)


def sr0(srs, n_cuba=None):
    """Jangkaan SR maksimum nasib bagi N percubaan (varians SR antara percubaan)."""
    srs = [s for s in srs if not math.isnan(s)]
    nk = n_cuba or len(srs); v = np.var(srs) if len(srs) > 1 else 0
    g = 0.5772156649
    return math.sqrt(v) * ((1 - g) * _N.inv_cdf(1 - 1 / nk) + g * _N.inv_cdf(1 - 1 / (nk * math.e))) if nk > 1 else 0


def dsr(sr, sk, ku, n, sr0_):
    """Deflated Sharpe ratio (Bailey & López de Prado 2014), SR harian."""
    d = math.sqrt(max(1e-12, 1 - sk * sr + (ku - 1) / 4 * sr ** 2))
    return _N.cdf((sr - sr0_) * math.sqrt(n - 1) / d)


# ---------- PBO melalui CSCV ----------
def pbo(M, blok=8):
    """M: tatasusunan (hari × percubaan) pulangan harian. CSCV: bahagi kepada `blok` blok berturut, setiap
    gabungan blok/2 = dalam sampel; pilihan terbaik (Sharpe) dalam sampel, logit kedudukan relatifnya luar
    sampel. PBO = pecahan logit <= 0. Pulang dict(pbo, n_gabung, logit_median)."""
    M = np.asarray(M, float)
    if M.ndim != 2 or M.shape[1] < 2 or M.shape[0] < blok * 2: return dict(pbo=None, n_gabung=0, logit_median=None)
    M = np.nan_to_num(M)
    B = np.array_split(np.arange(M.shape[0]), blok); N = M.shape[1]
    sh = lambda X: X.mean(0) / np.where(X.std(0) > 0, X.std(0), np.inf)
    L = []
    for c in combinations(range(blok), blok // 2):
        di = np.concatenate([B[k] for k in c]); lu = np.concatenate([B[k] for k in range(blok) if k not in c])
        a = sh(M[di]); b = sh(M[lu])
        best = int(np.argmax(a))
        w = (np.argsort(np.argsort(b))[best] + 1) / (N + 1)    # kedudukan relatif 1..N → (0,1)
        L.append(math.log(w / (1 - w)))
    L = np.array(L)
    return dict(pbo=float((L <= 0).mean()), n_gabung=len(L), logit_median=float(np.median(L)))
