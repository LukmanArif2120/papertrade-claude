"""Pembinaan signal daripada lajur indikator (REVERSE SPEC §8.4, §9, Step 4.2).

Signal = Series boolean. Tiga bentuk:
  b:<kol>            indikator ya/tidak (31)
  q1:<kol>/q5:<kol>  hujung kuintil indikator berterusan, atas POPULASI KUINTIL yang dibekukan
  <pemicu>&q<k>:<kon> pemicu x 1 konteks (HAD BERSYARAT aktif: pemicu x 2 konteks tidak diuji)
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# 31 indikator ya/tidak
BINARI = ['rsi_lintas50', 'rsi_lintas60', 'macd_cross', 'macd_atas0', 'bb_squeeze',
          'obv_tinggi_baru', 'ad_tinggi_baru', 'atas_awan', 'tenkan_atas', 'donchian20',
          'donchian55', 'inside_day', 'outside_day', 'nr7', 'hammer', 'bullish_engulfing',
          'pocket_pivot', 'vcp', 'gap_and_go', 'breakout_52w', 'breakout_asas', 'ema_crossback',
          'garis_rs_tinggi', 'sektor_atas_ma50', 'spy_ma50', 'spy_ma200', 'qqq_ma50', 'qqq_ma200']
BINARI_TANDA = {'supertrend': 'supertrend_naik', 'psar_arah': 'psar_naik',
                'spy_cerun_ma50': 'spy_ma50_menaik'}

# SENARAI KEUTAMAAN TETAP dedup (SPEC §8.4) — susunan tidak boleh diubah
KEUTAMAAN = ['j_ma200', 'j_ma50', 'j_ema21', 'j_ema9', 'j_ma150', 'lapis', 'cerun_ma50',
             'cerun_ema21', 'cerun_ma200', 'hari_gc', 'rsi14', 'roc60', 'roc20', 'macd_hist',
             'hari_macd_cross', 'adx14', 'pdi', 'mdi', 'stoch_k', 'stoch_d', 'willr14', 'cci20',
             'rsi2', 'atr_pct', 'nisbah_atr', 'bb_lebar', 'julat20', 'julat10', 'bb_pctb',
             'kelt_pos', 'vol_n50', 'vol_n50_5h', 'vol_naik_turun20', 'mfi14', 'cmf20',
             'j_52w_tinggi', 'j_52w_rendah', 'rs_spy_6b', 'rs_spy_3b', 'rs_spy_12b', 'sektor_1b']

PEMICU = ['macd_cross', 'rsi_lintas50', 'ema_crossback', 'donchian20', 'pocket_pivot', 'gap_and_go']
KONTEKS = ['j_52w_tinggi', 'rs_spy_6b', 'bb_lebar', 'atr_pct', 'lapis', 'cerun_ma50', 'vol_n50',
           'julat20', 'j_ma200', 'sektor_1b']


def dedup(pop, ambang=0.8):
    """Buang indikator berterusan yang Spearman |rho| > ambang dengan yang lebih utama.

    KONTEKS dipradaftar dilindungi (dibenih dahulu). Pulangkan (simpan, dibuang).
    """
    ada = [k for k in KEUTAMAAN if k in pop.columns]
    X = pop[ada].to_numpy('float64')
    with np.errstate(all='ignore'):
        rho, _ = spearmanr(X, nan_policy='omit')
    rho = np.atleast_2d(np.asarray(rho, dtype='float64'))
    pos = {k: i for i, k in enumerate(ada)}
    simpan, buang = [], []
    benih = [k for k in KEUTAMAAN if k in KONTEKS and k in pos]
    for k in benih:
        simpan.append(k)
    for k in ada:
        if k in simpan:
            continue
        kena = None
        for s in simpan:
            r = rho[pos[k], pos[s]]
            if np.isfinite(r) and abs(r) > ambang:
                kena = (s, float(r))
                break
        if kena:
            buang.append((k, kena[0], kena[1]))
        else:
            simpan.append(k)
    simpan = [k for k in KEUTAMAAN if k in simpan]
    return simpan, buang


def kuintil(pop, kols):
    """Sempadan Q1 (p20) dan Q5 (p80) setiap indikator, atas POPULASI KUINTIL (dibekukan)."""
    out = {}
    for k in kols:
        x = pop[k].to_numpy('float64')
        x = x[np.isfinite(x)]
        if x.size < 100:
            continue
        out[k] = dict(q1=float(np.quantile(x, 0.20)), q5=float(np.quantile(x, 0.80)),
                      n=int(x.size))
    return out


def bina(df, kuin, had_bersyarat=True):
    """{nama_signal: array boolean} bagi DataFrame indikator df."""
    s = {}
    for k in BINARI:
        if k in df.columns:
            s[f'b:{k}'] = (df[k].to_numpy('float64') > 0.5)
    for k, nama in BINARI_TANDA.items():
        if k in df.columns:
            s[f'b:{nama}'] = (df[k].to_numpy('float64') > 0)
    for k, v in kuin.items():
        if k not in df.columns:
            continue
        x = df[k].to_numpy('float64')
        s[f'q1:{k}'] = np.isfinite(x) & (x <= v['q1'])
        s[f'q5:{k}'] = np.isfinite(x) & (x >= v['q5'])
    # pemicu x 1 konteks
    for p in PEMICU:
        if p not in df.columns:
            continue
        pm = df[p].to_numpy('float64') > 0.5
        for kon in KONTEKS:
            for hj in ('q1', 'q5'):
                nm = f'{hj}:{kon}'
                if nm in s:
                    s[f'{p}&{nm}'] = pm & s[nm]
    if not had_bersyarat:
        raise NotImplementedError('pemicu x 2 konteks tidak diuji: HAD BERSYARAT aktif (SPEC §13.4)')
    return s
