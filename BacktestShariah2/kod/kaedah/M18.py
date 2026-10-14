from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M18'
NAMA = 'EMA9/21 Pullback'
VARIAN = 'V2 V1 Model A sahaja'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

ema = lambda s, k: s.ewm(span=k, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        E9, E21 = ema(c, 9), ema(c, 21)
        ATH = h.cummax().shift(1)      # proksi ATH: high tertinggi dalam data sebelum hari i
        A = (l < l.shift()) & (c > l.shift())
        RR = (ATH - c) / (c - l)
        sig = (c > E21) & (l <= E9) & A & (ATH > c) & (E9 > E21) & (c > o) & (RR >= 2)
        # Kad/laporan: langkau jika buka masuk <= henti (low_i) atau >= ATH
        lk = ((o.shift(-1) <= l) | (o.shift(-1) >= ATH)).fillna(False)
        g['_E9'] = E9; g['_E21'] = E21; g['_ATH'] = ATH
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = l
        g['tgt'] = ATH                   # ATH bergerak (enjin pakai nilai hari sebelumnya)
        g['exitc'] = c < E21
        g['rank'] = RR


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V2 Model A (kod sedia, PADAN registry), N=6:
    1 EMA9 > EMA21; 2 tutup > EMA21; 3 low <= EMA9 (undur sentuh EMA9); 4 ATH > tutup;
    5 R:R ke ATH >= 2 (henti = low); 6 PENCETUS lilin pembalikan hijau (low < low semalam,
    tutup > low semalam, tutup > buka).
    Syarat 1–5 dipenuhi pada bar terakhir; pencetus ialah corak satu hari -> jarak_pct = None."""
    if len(g) < 30: return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._ATH): return None
    if not (r._E9 > r._E21 and r.close > r._E21 and r.low <= r._E9): return None    # 1, 2, 3
    ath = max(r._ATH, r.high)                   # ATH yang dipakai esok (termasuk high hari ini)
    if not (r._ATH > r.close and ath > r.close): return None                     # 4
    # Andaian saya: R:R esok dianggar dengan tutup ≈ tutup hari ini dan henti ≈ low hari ini.
    if r.close <= r.low or (ath - r.close) / (r.close - r.low) < 2: return None   # 5
    return {'sebab': f'EMA9 ({r._E9:.2f}) > EMA21 ({r._E21:.2f}); tutup > EMA21; low hari ini sentuh EMA9; '
                     f'ATH {ath:.2f} > tutup; R:R anggaran {(ath - r.close) / (r.close - r.low):.1f} >= 2',
            'syarat_beli': f'Esok lilin hijau: low < {r.low:.2f} tetapi tutup > {r.low:.2f} dan tutup > buka; '
                           f'low esok <= EMA9, tutup > EMA21, R:R ke {ath:.2f} >= 2 (henti = low esok); langkau jika buka <= low atau >= ATH',
            'pencetus': 'Lilin pembalikan hijau (Model A)', 'paras': None, 'jarak_pct': None,
            'syarat_dipenuhi': '5/6', 'skor': 0.9}
