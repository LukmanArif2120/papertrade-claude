"""STEP 10 — join peristiwa sah REVERSE x lajur SEC titik-masa (fasa 2 leg SEC).

Peringkat 2 workflow: **BINA JOIN SAHAJA**. Skrip ini tidak mengira dan tidak mencetak sebarang
statistik hasil (pulangan, rank-IC, lift). Ia hanya menghasilkan satu baris setiap peristiwa sah
dengan lajur SEC seperti yang DIKETAHUI pada hari peristiwa, plus kiraan liputan untuk gerbang
ambang `SPEC_FASA2.md` §4. Pemisahan ini menjaga pradaftar §5: peraturan dikunci sebelum keputusan
dilihat.

Masa ketersediaan: `teras/sec.py` `hari_tersedia()` (§4.2) — sesi dagangan pertama yang bukanya
selepas cap masa pemfailan, BUKAN `tarikh_fail`.

Jarak ke earnings (§4.3): `hari_sejak_earnings` tepat dan ke belakang. `hari_ke_earnings_jangka`
ialah **jangkaan** daripada kitaran pengumuman yang sudah tersedia; tarikh pemfailan 8-K yang
SEBENARNYA berikut TIDAK digunakan (itu lookahead).

Guna:
  python3 REVERSE/step10_sec.py --tahun 2025
  python3 REVERSE/step10_sec.py                 (semua tahun yang ada cache signals)
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR / 'REVERSE'))
from teras import sec as S  # noqa: E402

BS2 = AKAR / 'BacktestShariah2'
SEC = BS2 / 'data' / 'sec'
CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
A02 = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'

# Lajur SEC yang diuji (SPEC_FASA2.md §2). Tiada tambahan separuh jalan.
LAJUR_SEC = ['sue', 'tumbuh_hasil', 'pecutan_hasil']
SELANG_MAKS = 120      # hari kalendar: kitaran lebih panjang daripada ini tidak dipercayai (jangkaan = NaT)


def sesi_dagangan():
    """Kalendar sesi = tarikh SPY dalam data harga A02 (bukan kalendar kalendar; cuti dilangkau)."""
    ix = pd.read_parquet(A02 / 'idx.parquet', columns=['ticker', 'date'])
    return pd.DatetimeIndex(pd.to_datetime(ix.loc[ix.ticker == 'SPY', 'date']).sort_values().unique())


def sec_tersedia(sesi):
    """Jadual SUE setiap saham dengan `hari_tersedia` (§4.2), tersusun untuk merge_asof."""
    s = pd.read_csv(SEC / 'sue.csv')
    k = pd.read_csv(SEC / 'earnings_8k.csv', usecols=['saham', 'tarikh_fail', 'masa_terima'])
    # Cap masa 8-K bagi setiap (saham, tarikh_umum); baris `sumber_tarikh == 'fail'` tiada 8-K.
    k['tarikh_fail'] = pd.to_datetime(k.tarikh_fail, errors='coerce')
    s['tarikh_umum'] = pd.to_datetime(s.tarikh_umum, errors='coerce')
    s = s.merge(k.rename(columns={'tarikh_fail': 'tarikh_umum'}), on=['saham', 'tarikh_umum'], how='left')
    s['hari_tersedia'] = S.hari_tersedia(s.masa_terima, sesi, tarikh_sandaran=s.tarikh_umum)
    s = s.dropna(subset=['hari_tersedia']).sort_values(['saham', 'hari_tersedia'])
    # Jangkaan pengumuman berikut dikira pada jadual SEC, jadi ia mengalir melalui merge_asof dan
    # tidak boleh tersilap menggunakan baris masa hadapan.
    s['earnings_jangka'] = np.concatenate(
        [_kitaran(g.to_numpy()) for _, g in s.groupby('saham', sort=False)['hari_tersedia']]
    ) if len(s) else np.array([], dtype='datetime64[ns]')
    return s[['saham', 'hari_tersedia', 'tarikh_umum', 'akhir', 'sumber_tarikh', 'earnings_jangka'] + LAJUR_SEC]


def _kitaran(hari):
    """Jangkaan pengumuman berikut daripada selang pengumuman LALU sahaja (titik-masa).

    hari: array datetime64 pengumuman tersedia, tersusun. Pulang array datetime64 sejajar, di mana
    jangkaan[i] = hari[i] + median selang bagi hari[:i+1] (median bergulir yang hanya melihat ke
    belakang). Kurang daripada 2 pengumuman, atau semua selang > SELANG_MAKS -> NaT."""
    h = pd.DatetimeIndex(hari)
    d = np.diff(h.to_numpy()).astype('timedelta64[D]').astype('float64')
    tambah = np.full(len(h), np.nan)
    for i in range(1, len(h)):
        sel = d[:i]
        sel = sel[np.isfinite(sel) & (sel > 0) & (sel <= SELANG_MAKS)]
        if sel.size:
            tambah[i] = np.median(sel)
    hasil = np.full(len(h), np.datetime64('NaT', 'ns'))
    ada = np.isfinite(tambah)
    hasil[ada] = h.to_numpy()[ada] + tambah[ada].astype('int64') * np.timedelta64(1, 'D')
    return hasil


def peristiwa(tahun):
    """Peristiwa sah REVERSE bagi satu tahun (SPEC §7 + topeng universe §13.5)."""
    p = CACHE / f'signals_{tahun}.parquet'
    if not p.exists():
        return None
    s = pd.read_parquet(p, columns=['ticker', 'tarikh', 'jenis_peristiwa', 'dalam_univ', 'harga_masuk'])
    ev = s[(s.jenis_peristiwa != '') & (s.dalam_univ == 1)].copy()
    ev['tarikh'] = pd.to_datetime(ev.tarikh)
    return ev.sort_values('tarikh').reset_index(drop=True)


def gabung(tahun, sesi, sec):
    """Satu baris setiap peristiwa sah, dengan lajur SEC seperti diketahui pada hari peristiwa."""
    ev = peristiwa(tahun)
    if ev is None or ev.empty:
        return None
    ev = ev.rename(columns={'ticker': 'saham'})
    sec = sec[sec.saham.isin(set(ev.saham))]
    g = pd.merge_asof(ev.sort_values('tarikh'), sec.sort_values('hari_tersedia'),
                      left_on='tarikh', right_on='hari_tersedia', by='saham', direction='backward')
    g['hari_sejak_earnings'] = (g.tarikh - g.hari_tersedia).dt.days
    g['hari_ke_earnings_jangka'] = (g.earnings_jangka - g.tarikh).dt.days
    g['tahun'] = tahun
    return g


def liputan(g):
    """Kiraan liputan untuk gerbang ambang §4. KIRAAN SAHAJA — tiada statistik hasil."""
    n = len(g)
    out = dict(tahun=int(g.tahun.iloc[0]), n_peristiwa=n, n_saham=int(g.saham.nunique()),
               n_saham_ada_sec=int(g.loc[g.sue.notna(), 'saham'].nunique()))
    for k in LAJUR_SEC:
        out[f'n_{k}'] = int(g[k].notna().sum())
        out[f'pct_{k}'] = round(100.0 * g[k].notna().sum() / n, 1) if n else 0.0
    out['n_hari_sejak'] = int(g.hari_sejak_earnings.notna().sum())
    out['n_jangka'] = int(g.hari_ke_earnings_jangka.notna().sum())
    out['median_hari_sejak'] = float(g.hari_sejak_earnings.median()) if out['n_hari_sejak'] else np.nan
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--tahun', type=int, default=0, help='satu tahun; 0 = semua yang ada cache signals')
    a = ap.parse_args(argv)
    sesi = sesi_dagangan()
    sec = sec_tersedia(sesi)
    tahun = [a.tahun] if a.tahun else sorted(int(p.stem.split('_')[1]) for p in CACHE.glob('signals_*.parquet'))
    baris, lip = [], []
    for th in tahun:
        g = gabung(th, sesi, sec)
        if g is None:
            print(f'{th}: tiada cache signals — langkau')
            continue
        baris.append(g)
        lip.append(liputan(g))
        print(f'{th}: {lip[-1]["n_peristiwa"]} peristiwa | SUE tidak kosong {lip[-1]["pct_sue"]}%'
              f' | saham ada SEC {lip[-1]["n_saham_ada_sec"]}/{lip[-1]["n_saham"]}')
    if not baris:
        return 1
    kol = ['tahun', 'saham', 'tarikh', 'jenis_peristiwa', 'harga_masuk', 'hari_tersedia', 'tarikh_umum',
           'akhir', 'sumber_tarikh', 'hari_sejak_earnings', 'hari_ke_earnings_jangka'] + LAJUR_SEC
    pd.concat(baris, ignore_index=True)[kol].to_csv(KELUAR / 'sec_join.csv', index=False, float_format='%.6g')
    L = pd.DataFrame(lip)
    L.to_csv(KELUAR / 'sec_liputan.csv', index=False)
    print('\n' + L.to_string(index=False))
    print(f'\nsec_join.csv + sec_liputan.csv ditulis. Ambang §4: >= 3,000 peristiwa dengan lajur tidak kosong.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
