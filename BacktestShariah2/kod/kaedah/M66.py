from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M66'
NAMA = 'IBD Undur Pertama ke Purata 50 Hari'
VARIAN = 'V0 Sumber tulen (UNDUR+NAIK50+PUSING+BARU; tanpa PERTAMA/HIGHBARU/NIPIS)'
TMAX = None
WARM = 292
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300


def sedia(fr, idx):
    for g in fr.values():
        s50 = g.close.rolling(50).mean()
        sentuh = g.low <= 1.02 * s50
        undur = sentuh.astype(int).rolling(4, min_periods=1).max() > 0     # k dalam i-3..i
        naik50 = s50 > s50.shift(10)
        pusing = (g.close > g.high.shift(1)) & (g.close > g.open) & (g.close > s50)
        calon = (undur & naik50 & pusing).values
        # BARU: tiada isyarat AKHIR dalam i-10..i-1 (Andaian saya dalam laporan; dikira berulang)
        sig = np.zeros(len(g), bool); akhir = -999
        for i in range(len(g)):
            if calon[i] and i - akhir > 10:
                sig[i] = True; akhir = i
        g['_undur'] = undur; g['_naik50'] = naik50; g['_s50'] = s50
        g['sig'] = sig
        g['stop'] = g.low.rolling(4).min()
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V0 (N=5) untuk isyarat esok (i = esok):
       [1] UNDUR: low <= 1.02 x SMA50 dalam i-3..i (dinilai: dalam 3 hari terakhir termasuk hari ini)
       [2] NAIK50: SMA50 esok > SMA50 10 hari sebelumnya (disemak pada paras pencetus)
       [3] tutup > SMA50 (keadaan hari ini; esok mesti kekal) [4] BARU: tiada isyarat dalam 10 hari terakhir
       [5] PENCETUS (lilin pusingan): tutup esok > high hari ini DAN tutup esok > buka esok (lilin hijau)."""
    r = g.iloc[-1]; n = len(g)
    if bool(r.sig) or n < PERLU_BAR:
        return None
    lo = g.low.values; cl = g.close.values; s50 = g._s50.values
    if not (lo[-3:] <= 1.02 * s50[-3:]).any():       # [1]
        return None
    if g.sig.values[-10:].any():                      # [4]
        return None
    if not cl[-1] > s50[-1]:                          # [3]
        return None
    s50_min = cl[-49:].mean()
    paras = max(float(r.high), s50_min)
    s50_esok = (cl[-49:].sum() + paras) / 50
    if not s50_esok > s50[-10]:                       # [2] SMA50 esok vs SMA50 pada i-10
        return None
    jarak = (paras - r.close) / r.close * 100
    # Andaian saya: jarak 0 (tutup = high hari ini) diterima kerana pencetus tetap belum berlaku (perlu tutup > high).
    if jarak < 0 or jarak > 2.0:
        return None
    return _hasil(f'Undur ke SMA50 ({s50[-1]:.2f}) dalam 3 hari terakhir; SMA50 menaik; tutup > SMA50; tiada isyarat 10 hari',
                  f'Tutup esok > {paras:.2f} (high hari ini) DAN tutup esok > buka esok (lilin hijau); henti = low terendah 4 hari',
                  'Lilin pusingan (tutup > high semalam, hijau)', paras, jarak, 4, 5)
