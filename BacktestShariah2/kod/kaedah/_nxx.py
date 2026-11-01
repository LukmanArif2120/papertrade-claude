"""Pembantu dikongsi bagi kaedah Nxx (kombinasi indikator REVERSE).

PERATURAN WAJIB: formula di sini ialah salinan **verbatim** daripada `REVERSE/teras/ind.py`
dan `REVERSE/step18_nxx.py`, bukan daripada `enjin.rsi`/`enjin.atr`. Sebabnya:

  * `enjin.rsi` guna `ewm(alpha=1/n, adjust=False)` tanpa benih purata-n;
  * `enjin.atr` guna `rolling(n).mean()` (purata mudah), bukan pelicinan Wilder.

Kedua-duanya BERBEZA daripada `_wilder` kajian. Kalau kaedah Nxx memakai pembantu enjin,
jejak hadapan akan mengukur peraturan yang bukan peraturan yang dikaji, dan kesemua nombor
`REVERSE/silang_akhir.csv` tidak lagi terpakai. `ujian/test_nxx_sepadan.py` membandingkan
keluaran fail ini dengan `REVERSE/teras/ind.py` pada harga sebenar dan GAGAL jika terpesong.

Rujukan nombor (REVERSE/silang_akhir.csv, 2 tingkap, BH-FDR, gate0-gate3 LULUS):
  GB02_atau3 x X13 -> jangkaan tahan +8.541%, lift +4.191/+1.818, menang 64.2%,
  n 195,681, p 0.0068, tanpa5 +2.858% (POSITIF - tidak bergantung ekor kanan).
"""
import numpy as np
import pandas as pd

EPS = 1e-12                 # ind.py:9
IMBAS = 126                 # step19_nxx_keluar.py:29 - ufuk keluar kajian = TMAX


def _wilder(s, n):
    """Pelicinan Wilder (RMA) dengan nilai awal = purata n pertama. ind.py:13."""
    a = s.to_numpy(dtype='float64')
    out = np.full(a.size, np.nan)
    if a.size < n:
        return pd.Series(out, index=s.index)
    out[n - 1] = np.nanmean(a[:n])
    for i in range(n, a.size):
        x = a[i]
        if not np.isfinite(x):
            x = 0.0
        out[i] = (out[i - 1] * (n - 1) + x) / n
    return pd.Series(out, index=s.index)


def _ema(s, n):
    """ind.py:29."""
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def indikator(g):
    """Lajur yang N19/N20/N37/N115 dan keluar X13 perlukan, formula kajian verbatim."""
    o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
    d = pd.DataFrame(index=g.index)

    # rsi14 - ind.py:143-147
    delta = c.diff()
    naik_w = _wilder(delta.clip(lower=0), 14)
    turun_w = _wilder((-delta).clip(lower=0), 14)
    d['rsi14'] = 100.0 - 100.0 / (1.0 + naik_w / (turun_w + EPS))

    # adx14 - ind.py:168-178
    up, dn = h.diff(), -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=c.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=c.index)
    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    atr14 = _wilder(tr, 14)
    pdi = 100.0 * _wilder(pdm, 14) / (atr14 + EPS)
    mdi = 100.0 * _wilder(mdm, 14) / (atr14 + EPS)
    d['adx14'] = _wilder((100.0 * (pdi - mdi).abs() / (pdi + mdi + EPS)).fillna(0.0), 14)

    # bb_pctb - ind.py:189-193
    m20 = c.rolling(20, min_periods=20).mean()
    s20 = c.rolling(20, min_periods=20).std(ddof=0)
    bb_a, bb_b = m20 + 2 * s20, m20 - 2 * s20
    d['bb_pctb'] = (c - bb_b) / ((bb_a - bb_b) + EPS) * 100.0

    # ema20 + sentuh_ema20 - ind.py:196, step18_nxx.py:72
    d['ema20'] = _ema(c, 20)
    d['sentuh_ema20'] = l <= d['ema20']

    # vol_n50 - ind.py:202-203
    v50 = v.rolling(50, min_periods=50).mean()
    d['vol_n50'] = v / (v50 + EPS)

    # gap_and_go - ind.py:256-257
    gg = (o > h.shift(1) * 1.02) & (c > o) & (d['vol_n50'] >= 1.5)
    d['gap_and_go'] = gg.astype('float64')
    d.loc[v50.isna(), 'gap_and_go'] = np.nan

    return d


def _b(s):
    """Siri boolean tanpa NaN (NaN -> False), seperti `topeng()` kajian."""
    return s.fillna(False).astype(bool) if s.dtype == object else s.astype('float64').fillna(0.0) > 0.5


# ---------- topeng MASUK (step18_nxx.py:196,197,210,253) ----------
def n19(f):
    """Bawah jalur BB + RSI<30 (LuxAlgo). bb_pctb < 0 DAN rsi14 < 30."""
    return (f.bb_pctb < 0) & (f.rsi14 < 30)


def n20(f):
    """Kembali masuk jalur + RSI silang 30. bb_pctb[-1] < 0 DAN bb_pctb > 0 DAN rsi14 silang naik 30."""
    return (f.bb_pctb.shift(1) < 0) & (f.bb_pctb > 0) & (f.rsi14 > 30) & (f.rsi14.shift(1) <= 30)


def n37(f):
    """Gap and go. open > tinggi[-1] x 1.02 DAN tutup > open DAN vol_n50 >= 1.5."""
    return f.gap_and_go > 0


def n115(f, g):
    """Holy Grail (Raschke). adx14 > 30 DAN rendah menyentuh ema20 DAN tutup > tinggi[-1]."""
    return (f.adx14 > 30) & f.sentuh_ema20 & (g.close > g.high.shift(1))


def gb02_atau3(f, g):
    """KESATUAN N19 u N37 u N115 - konfigurasi yang melepasi KESEMUA empat gate."""
    return n19(f) | n37(f) | n115(f, g)


# ---------- keluar (lorong 1) ----------
def x13(f):
    """X13 - keluar bila rsi14 > 70; enjin menjual pada buka esok. Keluar TERBAIK diukur
    (asas +4.350%), dan satu-satunya yang asasnya POSITIF selepas buang 5% teratas."""
    return f.rsi14 > 70


def pasang(g, masuk, nama_rank=None):
    """Tulis lajur enjin v1.2. TIADA henti dan TIADA sasaran dengan sengaja:

    * `stop = NaN` -> `enjin.trades` guna `sp = -inf`, jadi kecacatan henti hari-0
      (`REVERSE/KOLAM_EKOR.md` §4a: 421/1,770 posisi, menang 0.00%) **tidak boleh berlaku**;
    * `tgt = NaN` -> tiada sasaran untung, kerana `KOMBINASI.md` mengukur sasaran 1xATR
      menukar asas +2.595% menjadi -0.281%.

    Lorong 2 repo (Chandelier tutup 4xATR14) = `X15` kajian dan berjalan automatik pada
    setiap posisi, jadi X13 dan X15 terukur BERSEBELAHAN tanpa kod tambahan.
    """
    f = indikator(g)
    g['sig'] = masuk.fillna(False).astype(bool)
    g['stop'] = np.nan
    g['tgt'] = np.nan
    g['exitc'] = x13(f).fillna(False).astype(bool)
    g['rank'] = 0.0 if nama_rank is None else f[nama_rank].fillna(0.0).astype('float64')
    return f


def hampir_syarat(syarat, n_bar, cukup):
    """Watchlist "hampir" generik bagi kaedah Nxx.

    `syarat` = senarai (label, dipenuhi, jarak_unit) bagi bar TERAKHIR. Jarak dalam unit
    indikator sendiri (mata RSI, mata %b, mata ADX) kerana peraturan Nxx ialah ambang
    indikator, bukan paras harga: melaporkan "paras harga" akan mengandaikan hubungan
    harga->indikator yang tidak linear, jadi `paras` dibiar None dengan sengaja.
    """
    if n_bar < cukup:
        return None
    ok = [s for s in syarat if s[1]]
    belum = [s for s in syarat if not s[1]]
    if not belum or not ok:                 # semua sudah (= sig) atau semua belum (terlalu jauh)
        return None
    jarak = [s[2] for s in belum if s[2] is not None]
    j = float(min(jarak)) if jarak else None
    return {'sebab': ' DAN '.join(s[0] for s in ok) + ' sudah',
            'syarat_beli': ' DAN '.join(s[0] for s in syarat),
            'pencetus': ' DAN '.join(s[0] for s in belum),
            'paras': None,
            'jarak_pct': j,
            'syarat_dipenuhi': f'{len(ok)}/{len(syarat)}',
            'skor': 0.5 if j is None else round(float(max(0.0, 1.0 - j / 20.0)), 3)}
