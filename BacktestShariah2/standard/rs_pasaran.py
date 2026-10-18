# RS rating (gaya IBD) berbanding SELURUH pasaran AS, setiap sesi -> data/rs/rs_pasaran.csv + status.json.
# Dijalankan oleh GitHub Actions `.github/workflows/rs_pasaran.yml` selepas tutup New York (sesi Claude tidak boleh capai Yahoo).
# Dibaca oleh `gred.py tambah --rs data/rs` (skema gred RS 18 Okt 2026; tugasan_v3.md §8; bukti kajian/rs/RINGKASAN.md).
#
# Guna:
#   python3 rs_pasaran.py [--keluar BacktestShariah2/data/rs] [--sejak YYYY-MM-DD] [--simpan 60]
#   python3 rs_pasaran.py --cache /tmp/h.pkl ...     (guna semula harga yang sudah ditarik; ujian setempat)
#
# Lajur rs_pasaran.csv: tarikh (sesi New York), ticker, rs (1–99, dipangkat antara saham tutup >= USD5 dan >= 253 bar),
#   skor (skor IBD 40/20/20/20), mutlak12 (% 252 hari), mansfield (% RS line lawan SPY atas purata 252 hari),
#   rs_industri (1–99: pangkat median skor industri TradingView antara industri; >= 5 saham).
# Hanya ticker stor harga ditulis (pangkat tetap lawan seluruh pasaran); --semua untuk semua saham.
# status.json: dijana, sesi_terakhir, saham_pasaran, saham_ditulis, spy_atas200 {sesi: true/false}.
import sys, os, json, argparse, time
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kajian_rs as K  # noqa: E402

BS2 = os.path.dirname(HERE)
KELUAR = os.path.join(BS2, 'data', 'rs')


def univ_stor():
    """Ticker stor harga (harga_yf.universe): hanya baris ini ditulis (gred.py menggred calon daripada stor)."""
    try:
        from harga_yf import universe
        return set(universe()[0])
    except Exception as e:  # universe() perlu data papertrade
        print(f'universe harga_yf tidak dibaca ({e})', file=sys.stderr)
        return set()


def senarai(us):
    s = set(K.senarai()) | us
    return sorted(t for t in s if t and t.replace('.', '').replace('-', '').isalnum())


def tarik(tk, mula):
    import yfinance as yf
    C, gagal = [], []
    for i in range(0, len(tk), 200):
        ks = [t.replace('.', '-') for t in tk[i:i + 200]]
        df = None
        for n in range(3):
            try:
                df = yf.download(ks, start=mula, interval='1d', auto_adjust=False, actions=False,
                                 group_by='column', threads=True, progress=False)
                break
            except Exception as e:
                print(f'kumpulan {i}: cuba {n + 1} gagal ({e})', file=sys.stderr, flush=True)
                time.sleep(20 * (n + 1))
        if df is None or df.empty:
            gagal += ks; continue
        x = df['Close'].copy(); x.columns = [c.replace('-', '.') for c in x.columns]
        C.append(x.astype('float64'))
        time.sleep(1)
    c = pd.concat(C, axis=1)
    c.index = pd.to_datetime(c.index).tz_localize(None)
    c = c.loc[:, ~c.columns.duplicated()]
    return c.loc[:, c.notna().sum() > 0], gagal


def kira(c):
    """c: DataFrame tutup (termasuk SPY). Pulang (DataFrame panjang semua sesi, Series spy_atas200)."""
    spy = c['SPY'].ffill()
    c = K.bersih(c.drop(columns='SPY'))
    q = [c.shift(k) for k in (63, 126, 189, 252)]
    ok = (c >= K.HARGA_MIN) & q[3].notna()
    sk = (0.4 * (c / q[0] - 1) + 0.2 * (q[0] / q[1] - 1) + 0.2 * (q[1] / q[2] - 1) + 0.2 * (q[2] / q[3] - 1))
    sk = sk.replace([np.inf, -np.inf], np.nan).where(ok)
    rs = K.persentil(sk, ok)
    mut = (c / q[3] - 1) * 100
    rl = c.div(spy, axis=0)
    mf = (rl / rl.rolling(252, min_periods=200).mean() - 1) * 100
    ri, _ = K.industri(sk, c.columns)
    F = {'rs': rs, 'skor': sk, 'mutlak12': mut, 'mansfield': mf, 'rs_industri': ri}
    d = pd.DataFrame({k: x.stack() for k, x in F.items()})
    d.index.names = ['tarikh', 'ticker']
    d = d.dropna(subset=['rs']).reset_index()
    atas = (spy > spy.rolling(200).mean()).where(spy.rolling(200).count() >= 200)
    return d, atas


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluar', default=KELUAR)
    ap.add_argument('--sejak', help='tulis semua sesi sejak tarikh ini (isi sejarah); lalai: 10 sesi terakhir')
    ap.add_argument('--simpan', type=int, default=30, help='bilangan sesi disimpan dalam rs_pasaran.csv')
    ap.add_argument('--cache', help='pickle {"c": DataFrame tutup} (ujian; tanpa yfinance)')
    ap.add_argument('--semua', action='store_true', help='tulis semua saham pasaran (lalai: ticker stor harga sahaja)')
    a = ap.parse_args(argv)
    us = univ_stor()
    os.makedirs(a.keluar, exist_ok=True)
    if a.cache and os.path.exists(a.cache):
        D = pd.read_pickle(a.cache); c, gagal = D['c'], D.get('gagal', [])
    else:
        mula = (date.fromisoformat(a.sejak) if a.sejak else date.today()) - timedelta(days=800)
        c, gagal = tarik(senarai(us) + ['SPY'], mula.isoformat())
        if a.cache:
            pd.to_pickle({'c': c, 'gagal': gagal}, a.cache)
    if 'SPY' not in c or c['SPY'].dropna().empty:
        raise SystemExit('SPY tiada: RS tidak dikira')
    d, atas = kira(c)
    sesi = sorted(d.tarikh.unique())
    pilih = [t for t in sesi if t >= pd.Timestamp(a.sejak)] if a.sejak else sesi[-10:]
    n_pasaran = int((d.tarikh == sesi[-1]).sum())
    d = d[d.tarikh.isin(pilih) & (a.semua or not us or d.ticker.isin(us))].copy()
    d['tarikh'] = d.tarikh.dt.strftime('%Y-%m-%d')
    for k in ('rs', 'rs_industri'):
        d[k] = d[k].round().astype('Int64')
    for k in ('skor', 'mutlak12', 'mansfield'):
        d[k] = d[k].round(4)
    f = os.path.join(a.keluar, 'rs_pasaran.csv')
    if os.path.exists(f):
        lama = pd.read_csv(f, dtype={'tarikh': str})
        d = pd.concat([lama[~lama.tarikh.isin(d.tarikh.unique())], d], ignore_index=True)
    simpan = sorted(d.tarikh.unique())[-a.simpan:]
    d = d[d.tarikh.isin(simpan)].sort_values(['tarikh', 'ticker'])
    d.to_csv(f, index=False)
    st_f = os.path.join(a.keluar, 'status.json')
    st = json.load(open(st_f, encoding='utf-8')) if os.path.exists(st_f) else {}
    sa = st.get('spy_atas200') or {}
    sa.update({t.strftime('%Y-%m-%d'): bool(v) for t, v in atas.dropna().items() if t.strftime('%Y-%m-%d') in set(simpan)})
    st.update(dijana=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), sesi_terakhir=simpan[-1],
              saham_pasaran=n_pasaran, saham_ditulis=int((d.tarikh == simpan[-1]).sum()), gagal_tarik=len(gagal),
              spy_atas200={k: sa[k] for k in sorted(sa) if k in set(simpan)})
    json.dump(st, open(st_f, 'w', encoding='utf-8'), indent=1)
    print(json.dumps({k: v for k, v in st.items() if k != 'spy_atas200'}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
