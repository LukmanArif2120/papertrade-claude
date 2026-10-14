from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M74'
NAMA = 'Lulus Baharu Trend Template Minervini'
VARIAN = 'V2 V1 tanpa S8 (7 syarat harga)'
TMAX = None
WARM = 275
ADA_HENTI = True
SILANG = False      # V2 membuang S8 (RS), jadi tiada kebergantungan merentas saham
PERLU_BAR = 280


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _syarat(g):
    c = g.close
    s50 = c.rolling(50).mean(); s150 = c.rolling(150).mean(); s200 = c.rolling(200).mean()
    h252 = g.high.rolling(252).max(); l252 = g.low.rolling(252).min()
    S = pd.DataFrame({
        'S1': (c > s150) & (c > s200),
        'S2': s150 > s200,
        'S3': s200 > s200.shift(21),
        'S4': (s50 > s150) & (s50 > s200),
        'S5': c > s50,
        'S6': c >= 1.30 * l252,
        'S7': c >= 0.75 * h252}, index=g.index)
    return S, s50, s150, s200, h252, l252


def sedia(fr, idx):
    for g in fr.values():
        S, s50, s150, s200, h252, l252 = _syarat(g)
        lulus = S.all(axis=1)
        sebelum = lulus.astype(int).shift(1).rolling(20, min_periods=1).sum().fillna(0) > 0
        baharu = lulus & ~sebelum
        stop = np.maximum(g.close - 1.5 * _rma_atr(g), s50)
        # Langkau jika buka masuk (buka i+1) <= henti; bar terakhir: buka esok belum diketahui -> isyarat dikekalkan
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_bil'] = S.sum(axis=1); g['_lulus'] = lulus; g['_sebelum'] = sebelum
        g['_s50'] = s50; g['_s150'] = s150; g['_s200'] = s200; g['_h252'] = h252; g['_l252'] = l252
        g['sig'] = baharu & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    # Syarat entry V2 (N=8): S1..S7 Trend Template (7 syarat harga) + BAHARU (tiada lulus penuh dalam 20 hari lalu).
    # PENCETUS = satu-satunya syarat S1..S7 yang belum dipenuhi hari ini; semua syarat lain mesti dipenuhi.
    # Semua syarat S1..S7 menaik dengan tutup esok x, jadi paras = tutup minimum esok supaya KESEMUA 7 lulus.
    r = g.iloc[-1]
    if bool(r.sig) or bool(r._lulus) or len(g) < 260 or np.isnan(r._s200) or np.isnan(r._h252):
        return None
    if g._lulus.iloc[-20:].any():           # tetingkap BAHARU esok = 20 hari terakhir termasuk hari ini
        return None
    S, *_ = _syarat(g.iloc[-300:])
    gagal = [k for k, v in S.iloc[-1].items() if not v]
    if len(gagal) != 1:
        return None
    k = gagal[0]
    c = g.close.values.astype(float)
    s49, s149, s199 = c[-49:].sum(), c[-149:].sum(), c[-199:].sum()
    ref200 = float(g._s200.iloc[-21])       # SMA200 pada hari (esok − 21)
    # Andaian saya: high dan low esok = tutup esok (untuk H252/L252 esok); tetingkap 252 esok = 251 bar terakhir + esok.
    H = float(g.high.iloc[-251:].max()); L = float(g.low.iloc[-251:].min())
    amb = {
        'S1': max(s149 / 149, s199 / 199),
        'S2': (s199 / 200 - s149 / 150) * 600,
        'S3': 200 * ref200 - s199,
        'S4': max((s149 / 150 - s49 / 50) * 75, (s199 / 200 - s49 / 50) * 200 / 3),
        'S5': s49 / 49,
        'S6': 1.30 * L,
        'S7': 0.75 * H}
    paras = max(amb.values())
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    nama = {'S1': 'tutup > SMA150 & SMA200', 'S2': 'SMA150 > SMA200', 'S3': 'SMA200 naik 21 hari',
            'S4': 'SMA50 > SMA150 & SMA200', 'S5': 'tutup > SMA50', 'S6': 'tutup ≥ 1.30 × low 52 minggu',
            'S7': 'tutup ≥ 0.75 × high 52 minggu'}
    lulus = '; '.join(nama[x] for x in nama if x != k)
    return {'sebab': f'{lulus}; tiada lulus penuh dalam 20 hari lalu',
            'syarat_beli': f'Tutup esok > {paras:.2f} supaya "{nama[k]}" dipenuhi dan kesemua 7 syarat lulus serentak; '
                           f'henti maks(tutup − 1.5 × ATR14, SMA50)',
            'pencetus': nama[k], 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '7/8', 'skor': round(1 - jarak / 2, 3)}
