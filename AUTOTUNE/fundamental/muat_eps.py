"""AUTOTUNE A03 §1: muat turun EPS sebenar setiap suku daripada Yahoo (yfinance `get_earnings_dates`).

Satu shard: ticker universe A02 (`universe.parquet`) yang tersusun, diambil i, i+N, i+2N, ...
Output (dalam --keluar):
  eps_shard_<i>.csv : ticker, tarikh_laporan (ISO, zon America/New_York), masa, eps_sebenar, eps_anggaran, sumber
  gagal_<i>.txt     : satu baris setiap ticker yang gagal / kosong (jenis, sumber ganti)
`masa`: 'sebelum' (< 09:30), 'selepas' (>= 16:00), selain itu 'tidak diketahui' (09:30-15:59 dan 00:00 = tiada masa).
Jika Yahoo gagal atau kosong bagi satu ticker, baris daripada fail repo `eps.csv` (benih) digunakan (sumber = 'repo').
Guna: python3 AUTOTUNE/fundamental/muat_eps.py --shard 0 --shards 10 --universe universe.parquet --keluar shard_out
"""
import argparse
import csv
import sys
import time
from pathlib import Path

NY = 'America/New_York'
AKAR = Path(__file__).resolve().parents[2]
BENIH_LALAI = AKAR / 'BacktestShariah2' / 'data' / 'pemangkin' / 'sejarah' / 'eps.csv'
LAJUR = ['ticker', 'tarikh_laporan', 'masa', 'eps_sebenar', 'eps_anggaran', 'sumber']
HAD_BERTURUT = (100, 40)           # had get_earnings_dates; yang lebih kecil dicuba jika yang besar ralat
TIADA_DATA = ('delisted', 'no earnings dates', 'no data found', 'not found', 'no fundamentals')


def yf_simbol(t):
    return str(t).strip().upper().replace('.', '-')


def klasifikasi_masa(jam, minit=0):
    """'sebelum' jika < 09:30; 'selepas' jika >= 16:00; selain itu (termasuk 00:00 = tarikh sahaja) 'tidak diketahui'."""
    if jam == 0 and minit == 0:
        return 'tidak diketahui'
    m = jam * 60 + minit
    if m < 9 * 60 + 30:
        return 'sebelum'
    if m >= 16 * 60:
        return 'selepas'
    return 'tidak diketahui'


def ke_ny(ts):
    """Timestamp (bertz atau tidak) -> Timestamp bertz America/New_York (tanpa tz = UTC)."""
    import pandas as pd
    ts = pd.Timestamp(ts)
    ts = ts.tz_localize('UTC') if ts.tzinfo is None else ts
    return ts.tz_convert(NY)


def _angka(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if v != v else v


def _lajur(df, kata):
    for c in df.columns:
        if kata in str(c).lower():
            return c
    return None


def baris_dari_df(t, df):
    """get_earnings_dates -> senarai baris [ticker, tarikh_laporan, masa, eps_sebenar, eps_anggaran, 'yahoo'];
    hanya baris dengan EPS sebenar dilaporkan."""
    out = []
    if df is None or getattr(df, 'empty', True):
        return out
    c_sb, c_ang = _lajur(df, 'reported'), _lajur(df, 'estimate')
    if c_sb is None:
        return out
    for idx, r in df.iterrows():
        sb = _angka(r[c_sb])
        if sb is None:
            continue
        try:
            ts = ke_ny(idx)
        except (ValueError, TypeError):
            continue
        ang = _angka(r[c_ang]) if c_ang is not None else None
        out.append([t, ts.isoformat(), klasifikasi_masa(ts.hour, ts.minute), sb, '' if ang is None else ang, 'yahoo'])
    return out


def baca_benih(laluan):
    """eps.csv repo (ticker,tarikh,masa HH:MM,eps_anggaran,eps_sebenar,kejutan_pct) -> {ticker Yahoo: baris}."""
    import pandas as pd
    p = Path(laluan)
    if not p.exists():
        return {}
    d = pd.read_csv(p, dtype=str)
    benih = {}
    for r in d.itertuples(index=False):
        sb = _angka(r.eps_sebenar)
        if sb is None:
            continue
        try:
            jam, minit = (int(x) for x in str(r.masa).split(':')[:2])
            ts = pd.Timestamp(f'{r.tarikh} {jam:02d}:{minit:02d}').tz_localize(NY, ambiguous=True, nonexistent='shift_forward')
        except (ValueError, TypeError):
            continue
        ang = _angka(r.eps_anggaran)
        benih.setdefault(yf_simbol(r.ticker), []).append(
            [yf_simbol(r.ticker), ts.isoformat(), klasifikasi_masa(jam, minit), sb, '' if ang is None else ang, 'repo'])
    return benih


def _tiada_data(x):
    s = (type(x).__name__ + ' ' + str(x)).lower()
    return any(k in s for k in TIADA_DATA)


def _had_kadar(x):
    s = (type(x).__name__ + ' ' + str(x)).lower()
    return 'ratelimit' in s or 'rate limit' in s or 'too many' in s or '429' in s


def tarik_satu(t, fn_ambil, tidur=time.sleep):
    """(baris, ralat). fn_ambil(simbol, had) -> DataFrame. Cuba had besar kemudian kecil; ulang + backoff.
    ralat None jika Yahoo menjawab (walau kosong); 'kosong' jika tiada baris; selain itu mesej ralat terakhir."""
    ralat = None
    for had in HAD_BERTURUT:
        for cuba in range(2):
            try:
                baris = baris_dari_df(t, fn_ambil(yf_simbol(t), had))
                return baris, (None if baris else 'kosong')
            except Exception as x:  # noqa: BLE001 - yfinance melempar pelbagai jenis
                ralat = f'{type(x).__name__}: {str(x)[:80]}'
                if _tiada_data(x):
                    return [], 'kosong'
                tidur(30 * (cuba + 1) if _had_kadar(x) else 3 * (cuba + 1) ** 2)
    return [], ralat


def _ambil_yf(simbol, had):
    import yfinance as yf
    return yf.Ticker(simbol).get_earnings_dates(limit=had)


def senarai_shard(universe, shard, shards):
    import pandas as pd
    tick = sorted(pd.read_parquet(universe, columns=['ticker'])['ticker'].unique())
    return tick[shard::shards]


def jalankan(tick, benih, keluar, shard, fn_ambil=_ambil_yf, rehat=0.4, tidur=time.sleep, senyap=False):
    keluar = Path(keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    semua, gagal, berturut = [], [], 0
    for n, t in enumerate(tick):
        baris, ralat = tarik_satu(t, fn_ambil, tidur)
        sumber = 'yahoo'
        if not baris:
            ganti = benih.get(yf_simbol(t), [])
            if ganti:
                baris, sumber = ganti, 'repo'
            gagal.append(f'{t}\t{ralat}\tganti={sumber if ganti else "tiada"}\tbaris={len(baris)}')
        semua += baris
        berturut = berturut + 1 if (ralat and ralat != 'kosong') else 0
        if berturut >= 15:  # kemungkinan disekat kadar: rehat panjang
            tidur(120)
            berturut = 0
        tidur(rehat)
        if not senyap and n % 50 == 0:
            print(f'shard {shard}: {n}/{len(tick)} {t} baris={len(semua)} gagal={len(gagal)}', flush=True)
    with open(keluar / f'eps_shard_{shard}.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(LAJUR)
        w.writerows(semua)
    (keluar / f'gagal_{shard}.txt').write_text(
        f'# shard {shard}: {len(tick)} ticker; gagal/kosong {len(gagal)}\n' + '\n'.join(gagal) + '\n')
    return semua, gagal


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=1)
    ap.add_argument('--universe', default='universe.parquet')
    ap.add_argument('--benih', default=str(BENIH_LALAI))
    ap.add_argument('--keluar', default='shard_out')
    ap.add_argument('--had', type=int, default=0, help='hadkan bilangan ticker (ujian)')
    ap.add_argument('--rehat', type=float, default=0.4)
    a = ap.parse_args(argv)
    tick = senarai_shard(a.universe, a.shard, a.shards)
    if a.had:
        tick = tick[:a.had]
    semua, gagal = jalankan(tick, baca_benih(a.benih), a.keluar, a.shard, rehat=a.rehat)
    n_tick = len({r[0] for r in semua})
    print(f'shard {a.shard}: {len(tick)} ticker; {n_tick} ada EPS; {len(semua)} baris; gagal/kosong {len(gagal)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
