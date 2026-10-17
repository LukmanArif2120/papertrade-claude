"""Pemuat data AUTOTUNE. API: ambil(), muat(), topeng(), muat_431().
Data = aset Release `autotune-data` (parquet), cache tempatan AUTOTUNE/.cache/."""
import hashlib
import json
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

REPO = 'pedagangsenja/papertrade-claude'
TAG = 'autotune-data'
AKAR = Path(__file__).resolve().parents[2]
CACHE_LALAI = 'AUTOTUNE/.cache'
LAJUR = ['open', 'high', 'low', 'close', 'volume']
LAJUR_OUT = LAJUR + ['turnover']


def _sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _url_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'autotune', 'Accept': 'application/vnd.github+json'})
    tok = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if tok:
        req.add_header('Authorization', f'Bearer {tok}')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def _url_simpan(url, tujuan):
    req = urllib.request.Request(url, headers={'User-Agent': 'autotune'})
    tmp = Path(str(tujuan) + '.tmp')
    with urllib.request.urlopen(req, timeout=300) as r, open(tmp, 'wb') as f:
        shutil.copyfileobj(r, f, 1 << 20)
    tmp.replace(tujuan)


def _lengkap(cache):
    """True jika manifest.json ada dan semua fail wujud dengan saiz betul."""
    m = cache / 'manifest.json'
    if not m.exists():
        return False
    try:
        man = json.loads(m.read_text())
        return all((cache / f['nama']).exists() and (cache / f['nama']).stat().st_size == f['bait']
                   for f in man['fail'])
    except Exception:
        return False


def ambil(cache=CACHE_LALAI):
    """Pastikan data ada dalam `cache`; muat turun aset Release jika tiada. Pulangkan Path cache."""
    cache = Path(cache)
    if not cache.is_absolute():
        cache = AKAR / cache
    cache.mkdir(parents=True, exist_ok=True)
    try:  # cache tidak dicommit
        (cache / '.gitignore').write_text('*\n')
    except OSError:
        pass
    if _lengkap(cache):
        return cache
    if os.environ.get('GH_TOKEN') and shutil.which('gh'):
        r = subprocess.run(['gh', 'release', 'download', TAG, '-R', REPO, '-D', str(cache), '--clobber'],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print('gh gagal, guna API awam:', r.stderr[-200:])
    if not _lengkap(cache):
        rel = _url_json(f'https://api.github.com/repos/{REPO}/releases/tags/{TAG}')
        for a in rel['assets']:
            tujuan = cache / a['name']
            if tujuan.exists() and tujuan.stat().st_size == a['size']:
                continue
            _url_simpan(a['browser_download_url'], tujuan)
    man = json.loads((cache / 'manifest.json').read_text())
    for f in man['fail']:
        p = cache / f['nama']
        if not p.exists() or _sha256(p) != f['sha256']:
            raise RuntimeError(f"sha256 tidak sepadan: {f['nama']}")
    return cache


def _ke_fr(d):
    """DataFrame ticker-tunggal (lajur date + LAJUR) -> float64 + turnover, indeks 'date'."""
    g = d.set_index('date')[LAJUR].astype('float64')
    g['turnover'] = g['close'] * g['volume']
    return g


def muat(mula, akhir, kumpulan='AB', dir=None):
    """(fr, idx, univ). fr: ticker -> DataFrame (indeks 'date', float64 open..volume, turnover) bagi ticker yang
    ada dalam universe (kumpulan A/B/AB) sekurang-kurangnya satu bulan dalam [mula, akhir]; bar mula..akhir
    termasuk. idx: {'SPY','QQQ'}. univ: DataFrame universe penuh (bulan, ticker, kedudukan, kumpulan)."""
    d = Path(dir) if dir else ambil()
    mula, akhir = pd.Timestamp(mula), pd.Timestamp(akhir)
    univ = pd.read_parquet(d / 'universe.parquet')
    b0, b1 = mula.year * 100 + mula.month, akhir.year * 100 + akhir.month
    bi = univ['bulan'].str[:4].astype(int) * 100 + univ['bulan'].str[5:7].astype(int)
    m = (bi >= b0) & (bi <= b1) & univ['kumpulan'].isin(list(kumpulan))
    tick = sorted(univ.loc[m, 'ticker'].unique())
    bahagian = []
    for y in range(mula.year, akhir.year + 1):
        p = d / f'harga_{y}.parquet'
        if p.exists():
            bahagian.append(pd.read_parquet(p, filters=[('ticker', 'in', tick)]))
    fr = {}
    if bahagian:
        df = pd.concat(bahagian, ignore_index=True)
        df = df[(df['date'] >= mula) & (df['date'] <= akhir)]
        for t, g in df.groupby('ticker', sort=True):
            fr[t] = _ke_fr(g.sort_values('date'))
    ix = pd.read_parquet(d / 'idx.parquet')
    ix = ix[(ix['date'] >= mula) & (ix['date'] <= akhir)]
    idx = {t: _ke_fr(g.sort_values('date')) for t, g in ix.groupby('ticker')}
    return fr, idx, univ


_PETA = {}


def _peta(univ):
    """ticker -> (kumpulan, array YYYYMM tersusun); dicache bagi satu objek univ."""
    if _PETA.get('id') != id(univ):
        bi = (univ['bulan'].str[:4].astype(int) * 100 + univ['bulan'].str[5:7].astype(int)).to_numpy()
        peta = {}
        for t, ix in univ.groupby('ticker').indices.items():
            peta[t] = (univ['kumpulan'].to_numpy()[ix[0]], np.unique(bi[ix]))
        _PETA.clear()
        _PETA.update(id=id(univ), ref=univ, peta=peta)
    return _PETA['peta']


def topeng(g, ticker, univ, kumpulan='AB'):
    """Boolean Series sejajar g.index: True pada hari yang bulannya ada ticker dalam universe dan kumpulan."""
    ya = _peta(univ).get(ticker)
    if ya is None or ya[0] not in kumpulan:
        return pd.Series(False, index=g.index)
    ym = g.index.year * 100 + g.index.month
    return pd.Series(np.isin(np.asarray(ym), ya[1]), index=g.index)


def muat_431():
    """(fr, idx) daripada data_mentah/dataset_S1-S4.csv + index_benchmark.csv, format sama dengan muat().
    Turnover diambil daripada fail (serupa data asal kaedah)."""
    def baca(f):
        d = pd.read_csv(AKAR / 'data_mentah' / f)
        d['date'] = pd.to_datetime(d['date'].astype(str))
        return d

    def pecah(d):
        out = {}
        for t, g in d.groupby('ticker'):
            out[t] = g.sort_values('date').set_index('date')[LAJUR_OUT].astype('float64')
        return out

    fr = {}
    for s in ('S1', 'S2', 'S3', 'S4'):
        fr.update(pecah(baca(f'dataset_{s}.csv')))
    idx = pecah(baca('index_benchmark.csv'))
    return fr, idx
