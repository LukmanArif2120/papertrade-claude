# Fungsi kongsi F6 (pengesahan, gabungan, laporan): laluan, pembaca JSON kajian, metrik, DSR, label SPEC §5.
# Fail ini tidak mengubah apa-apa di luar AUTOTUNE/hasil/ dan AUTOTUNE/.cache/.
import glob, json, math, os, re
from statistics import NormalDist
import numpy as np, pandas as pd

AT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../AUTOTUNE
HASIL = os.path.join(AT, 'hasil')
TALA = os.path.join(HASIL, 'tala')
KAEDAH = os.path.join(AT, 'kaedah')
CACHE = os.path.join(AT, '.cache')

K_WFO = list(range(12))       # kajian 0–11: tetingkap ujian walk-forward
K_AKHIR, K_SEMASA = 12, 13
HAD_MDD = -0.30
HARI_TAHUN = 252.0
LABEL = ['TINGGI', 'SEDERHANA', 'RENDAH', 'GAGAL', 'BUKAN SWING', 'BELUM DITALA']


# ---------- siri pulangan harian ----------
def siri(obj):
    """Tukar pulangan harian dalam JSON kepada pd.Series (indeks tarikh, float). Terima:
    {tarikh: r}, [[tarikh, r], ...], {'tarikh'|'t'|'dates': [...], 'r'|'ret'|'pulangan'|'nilai': [...]}."""
    if obj is None: return pd.Series(dtype=float)
    if isinstance(obj, pd.Series): return obj.astype(float)
    if isinstance(obj, dict):
        kt = next((k for k in ('tarikh', 't', 'dates', 'date', 'index') if k in obj), None)
        kv = next((k for k in ('r', 'ret', 'pulangan', 'nilai', 'data', 'values') if k in obj), None)
        if kt and kv: t, v = obj[kt], obj[kv]
        else: t, v = list(obj.keys()), list(obj.values())
    elif isinstance(obj, (list, tuple)):
        if not obj: return pd.Series(dtype=float)
        t, v = [x[0] for x in obj], [x[1] for x in obj]
    else:
        raise TypeError(f'format siri tidak dikenali: {type(obj)}')
    s = pd.Series(np.asarray(v, float), index=pd.to_datetime(t))
    return s[~s.index.duplicated(keep='last')].sort_index()


def sambung(senarai):
    """Gabung siri pulangan harian beberapa tetingkap (tidak bertindih) mengikut tarikh."""
    s = [x for x in senarai if x is not None and len(x)]
    if not s: return pd.Series(dtype=float)
    r = pd.concat(s).sort_index()
    if r.index.duplicated().any():
        raise ValueError('tetingkap bertindih: tarikh berulang dalam OOS')
    return r


# ---------- metrik ----------
def cagr(r):
    """CAGR daripada pulangan harian: (∏(1+r))^(252/n) − 1. Sama bagi kaedah dan SPY (tarikh serupa)."""
    r = pd.Series(r).dropna()
    if len(r) == 0: return float('nan')
    g = float(np.prod(1.0 + r.values))
    if g <= 0: return -1.0
    return g ** (HARI_TAHUN / len(r)) - 1


def mdd(r):
    r = pd.Series(r).dropna()
    if len(r) == 0: return float('nan')
    e = np.concatenate([[1.0], np.cumprod(1.0 + r.values)])
    return float((e / np.maximum.accumulate(e) - 1).min())


def ekuiti_bulanan(r):
    """Ekuiti hujung bulan (mula 1.0) untuk dashboard: [[YYYY-MM, nilai], ...]."""
    r = pd.Series(r).dropna()
    if not len(r): return []
    e = (1 + r).cumprod().resample('ME').last().dropna()
    return [[d.strftime('%Y-%m'), round(float(v), 4)] for d, v in e.items()]


def spy_pulangan(idx_spy_close, tarikh):
    """Pulangan harian SPY pada tarikh yang SAMA dengan siri kaedah (tutup/tutup sebelumnya)."""
    c = pd.Series(idx_spy_close).dropna().sort_index()
    p = c.pct_change()
    return p.reindex(pd.DatetimeIndex(tarikh)).fillna(0.0)


def dsr(r, n_cubaan, var_sr=None):
    """Deflated Sharpe Ratio (Bailey & López de Prado 2014), Sharpe harian.
    SR0 = √V·((1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(N·e))); V lalai = 1/T (varians penganggar SR di bawah hipotesis nol)."""
    r = pd.Series(r).dropna().values
    T = len(r)
    if T < 3 or not n_cubaan or n_cubaan < 1: return float('nan')
    sd = r.std(ddof=1)
    if not sd > 0: return float('nan')
    sr = r.mean() / sd
    z = (r - r.mean()) / r.std(ddof=0)
    g3 = float((z ** 3).mean()); g4 = float((z ** 4).mean())
    V = (1.0 / T) if var_sr is None else float(var_sr)
    nd = NormalDist(); em = 0.5772156649015329
    if n_cubaan <= 1: sr0 = 0.0
    else: sr0 = math.sqrt(V) * ((1 - em) * nd.inv_cdf(1 - 1 / n_cubaan) + em * nd.inv_cdf(1 - 1 / (n_cubaan * math.e)))
    pen = 1 - g3 * sr + (g4 - 1) / 4 * sr ** 2
    if pen <= 0: return float('nan')
    return float(nd.cdf((sr - sr0) * math.sqrt(T - 1) / math.sqrt(pen)))


# ---------- label SPEC §5 ----------
def _lebih(a, b):
    return a is not None and b is not None and not (isinstance(a, float) and math.isnan(a)) \
        and not (isinstance(b, float) and math.isnan(b)) and a > b


def _ge(a, b):
    return a is not None and not (isinstance(a, float) and math.isnan(a)) and a >= b


def _le(a, b):
    return a is not None and not (isinstance(a, float) and math.isnan(a)) and a <= b


def label(m, belum=False):
    """m: dict metrik (cagr_a, cagr_b, mdd_a, hari_a, spy_a, spy_b, cagr_kunci, spy_kunci, dsr, pbo)."""
    if belum: return 'BELUM DITALA'
    h = m.get('hari_a')
    if h is not None and not (isinstance(h, float) and math.isnan(h)) and (h < 2 or h > 60):
        return 'BUKAN SWING'
    asas = _lebih(m.get('cagr_a'), m.get('spy_a')) and _lebih(m.get('cagr_b'), m.get('spy_b')) \
        and _ge(m.get('mdd_a'), HAD_MDD)
    if asas:
        if _lebih(m.get('cagr_kunci'), m.get('spy_kunci')) and _ge(m.get('dsr'), 0.95) and _le(m.get('pbo'), 0.30):
            return 'TINGGI'
        return 'SEDERHANA'
    if _lebih(m.get('cagr_a'), 0.0): return 'RENDAH'
    return 'GAGAL'


# ---------- fail kajian ----------
def senarai_kaedah():
    """ID kaedah: gabungan salinan AUTOTUNE/kaedah/M*.py dan folder hasil/tala/*."""
    ids = set()
    for f in glob.glob(os.path.join(KAEDAH, 'M*.py')): ids.add(os.path.basename(f)[:-3])
    for d in glob.glob(os.path.join(TALA, '*')):
        if os.path.isdir(d): ids.add(os.path.basename(d))
    return sorted(ids, key=lambda s: (len(s), s))


def belum_ditala_modul(kid, folder=None):
    """True jika salinan kaedah ditanda BELUM_DITALA (gagal kesetaraan) atau tiada."""
    f = os.path.join(folder or KAEDAH, f'{kid}.py')
    if not os.path.exists(f): return True
    with open(f, encoding='utf-8') as fh: teks = fh.read()
    return bool(re.search(r'^BELUM_DITALA\s*=\s*(True|1|[\'"].+[\'"])', teks, re.M))


def nama_modul(kid, folder=None):
    f = os.path.join(folder or KAEDAH, f'{kid}.py')
    if not os.path.exists(f): return ''
    with open(f, encoding='utf-8') as fh: teks = fh.read()
    m = re.search(r'^NAMA\s*=\s*[\'"](.+?)[\'"]', teks, re.M)
    return m.group(1) if m else ''


def baca_kajian(kid, folder=None):
    """{k: dict} bagi fail hasil/tala/<kid>/kNN.json yang wujud."""
    folder = folder or os.path.join(TALA, kid)
    out = {}
    for f in glob.glob(os.path.join(folder, 'k*.json')):
        m = re.match(r'k(\d+)\.json$', os.path.basename(f))
        if not m: continue
        try:
            with open(f, encoding='utf-8') as fh: out[int(m.group(1))] = json.load(fh)
        except Exception as e:
            out[int(m.group(1))] = {'ralat': f'JSON rosak: {e}'}
    return out


def tulis_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'), default=_lalai)


def _lalai(x):
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return None if np.isnan(x) else float(x)
    if isinstance(x, (pd.Timestamp,)): return x.strftime('%Y-%m-%d')
    if isinstance(x, np.ndarray): return x.tolist()
    raise TypeError(type(x))


def bersih(x, nd=6):
    """Bundarkan float; NaN/inf → None (JSON sah)."""
    if isinstance(x, dict): return {k: bersih(v, nd) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [bersih(v, nd) for v in x]
    if isinstance(x, (float, np.floating)):
        return None if not np.isfinite(x) else round(float(x), nd)
    if isinstance(x, np.integer): return int(x)
    return x
