"""AUTOTUNE A03: ciri fundamental F (ala CAN SLIM "C"), ketat titik-masa.

    from AUTOTUNE.fundamental.ciri import muat_eps, lajur_f
    eps = muat_eps()                       # Release `autotune-fundamental-a03` (eps_a03.parquet) melalui D.ambil
    f = lajur_f(fr, eps, ambang=0.25)      # {ticker: bool Series sejajar fr[ticker].index}

Pada hari d, F benar jika suku terkini yang SUDAH TERSEDIA (tersedia <= d) mempunyai eps_sebenar > 0 dan
eps_yoy >= ambang (eps_yoy sudah NaN jika EPS tahun lepas <= 0). Tiada suku tersedia / eps_yoy NaN -> False.
Suku terkini sentiasa dipilih mengikut `tersedia` (bukan mengikut tarikh laporan); suku lebih lama tidak digunakan
sebagai ganti apabila suku terkini tidak layak.
"""
from pathlib import Path

import numpy as np
import pandas as pd

TAG = 'autotune-fundamental-a03'
FAIL = 'eps_a03.parquet'


def muat_eps(dir=None, tag=TAG):
    """DataFrame eps_a03 (ticker, tarikh_laporan, tarikh, masa, eps_sebenar, eps_anggaran, sumber, tersedia, eps_yoy,
    eps_yoy_sebelum). dir: folder yang mengandungi eps_a03.parquet; jika tiada, muat turun Release `tag`."""
    if dir is None:
        from AUTOTUNE.teras import data as D
        dir = D.ambil(tag=tag)
    return pd.read_parquet(Path(dir) / FAIL)


def lajur_f(fr, eps_df, ambang=0.25, usia_maks=None):
    """dict ticker -> bool Series (indeks = fr[ticker].index). usia_maks (hari, pilihan): suku terkini yang dilaporkan
    lebih lama daripada ini dianggap lapuk -> False (lalai tiada had, mengikut SPEC_A03 §2)."""
    d = eps_df[eps_df['tersedia'].notna()].sort_values(['ticker', 'tersedia', 'tarikh_laporan'])
    kumpulan = {t: g for t, g in d.groupby('ticker', sort=False)}
    out = {}
    for t, g in fr.items():
        indeks = g.index
        ada = kumpulan.get(t)
        if ada is None or len(indeks) == 0:
            out[t] = pd.Series(False, index=indeks)
            continue
        ters = ada['tersedia'].to_numpy('datetime64[ns]')
        layak = ((ada['eps_sebenar'].to_numpy(float) > 0) & (ada['eps_yoy'].to_numpy(float) >= ambang))  # NaN -> False
        if usia_maks is not None:
            lapor = ada['tarikh'].to_numpy('datetime64[ns]')
        hari = pd.DatetimeIndex(indeks).normalize().to_numpy('datetime64[ns]')
        pos = np.searchsorted(ters, hari, side='right') - 1   # suku terkini dengan tersedia <= hari
        ada_suku = pos >= 0
        nilai = np.where(ada_suku, layak[np.clip(pos, 0, None)], False)
        if usia_maks is not None:
            usia = (hari - lapor[np.clip(pos, 0, None)]).astype('timedelta64[D]').astype(int)
            nilai &= usia <= usia_maks
        out[t] = pd.Series(nilai, index=indeks)
    return out
