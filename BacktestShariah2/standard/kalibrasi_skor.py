# kalibrasi_skor.py — julat beku skor kaedah swing v2 (dashboard Fasa 2; laporan reports/Skor KPI pemilihan kaedah swing.md item 10)
# Jana dagangan backtest set 431 (enjin v1.2, 1 Nov 2019 hingga akhir data) bagi setiap kaedah aktif dalam katalog, kira metrik v2
# setiap kaedah, kemudian simpan persentil ke-5 dan ke-95 merentas kaedah SWING (purata pegang backtest 3–30 hari, sama dengan
# pintu skor) ke data/analisis/kalibrasi_skor.json. Dijalankan sekali;
# julat dibekukan dalam dashboard_v2.html (TIANG_V2) bersama versi dan tarikh. Tanpa LLM.
#   python3 BacktestShariah2/standard/kalibrasi_skor.py [--hanya M03,M70]
# Metrik (sama dengan dashboard): u1 purata pulangan bersih % (tanpa pangkas: kaedah swing bergantung pada ekor kanan; purata
# dipangkas 5% direkod sebagai u1_pangkas untuk perbandingan); u2 = 21 × u1 ÷ hari pegang; u3 = purata lebihan atas
# penanda aras dalaman (purata semua dagangan semua kaedah yang dibeli pada hari sama); k1 = faktor untung (had 3); k2 = had bawah
# Wilson pecahan hari beli berpurata positif; r1 = CVaR 10% (purata 10% dagangan terburuk, minimum 3); r2 = purata MAE ÷ ATR14
# (MAE: rendah terendah dari hari beli hingga sehari sebelum keluar dan harga keluar; ATR14 % pada hari isyarat).
import argparse, importlib, json, math, os, sys, time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
ROOT = os.path.dirname(BS2)
sys.path.insert(0, os.path.join(BS2, 'kod'))
from enjin import trades, atr, COST, START  # noqa: E402

DATA = os.path.join(ROOT, 'data_mentah')
KATALOG = os.path.join(HERE, 'katalog_kaedah.json')
OUT = os.path.join(BS2, 'data', 'analisis', 'kalibrasi_skor.json')
VERSI = 'v2-2026-10-22'
N_MIN = 30               # dagangan backtest minimum untuk masuk kalibrasi
PANGKAS = 0.05
P_BAWAH, P_ATAS = 5, 95
SWING = (3, 30)          # purata hari pegang backtest (enjin: bar isyarat hingga keluar), sama dengan registry 'days'


def muat():
    fr = {}
    for s in ('S1', 'S2', 'S3', 'S4'):
        d = pd.read_csv(os.path.join(DATA, f'dataset_{s}.csv')); d['date'] = pd.to_datetime(d.date.astype(str))
        for t, g in d.groupby('ticker'):
            fr[t] = g.sort_values('date').set_index('date').copy()
    ix = pd.read_csv(os.path.join(DATA, 'index_benchmark.csv')); ix['date'] = pd.to_datetime(ix.date.astype(str))
    return fr, {t: g.sort_values('date').set_index('date').copy() for t, g in ix.groupby('ticker')}


def pangkas(x, p=PANGKAS):
    s = np.sort(np.asarray(x, float)); k = int(len(s) * p)
    return float(s[k:len(s) - k].mean()) if len(s) > 2 * k else float(s.mean())


def wilson_bawah(k, n, z=1.96):
    if not n:
        return None
    p = k / n; d = 1 + z * z / n
    return (p + z * z / (2 * n) - z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d


def cvar(x, a=0.10, k_min=3):
    s = np.sort(np.asarray(x, float)); k = min(len(s), max(k_min, math.ceil(a * len(s))))
    return float(s[:k].mean())


def mae_atr(T, fr):
    """Purata MAE % ÷ ATR14 % hari isyarat bagi setiap dagangan (≤ 0)."""
    out = []
    for t, d in T.groupby('ticker'):
        g = fr[t]; lo = g.low.values; a = (atr(g) / g.close * 100).values; ix = g.index
        i_sig = ix.get_indexer(d.sig); i_ent = ix.get_indexer(d.ent); i_ex = ix.get_indexer(d.ex)
        e = g.open.values[i_ent]
        for k in range(len(d)):
            if i_ent[k] < 0 or i_ex[k] < 0 or not a[i_sig[k]] > 0:
                continue
            px = e[k] * (1 + d.ret.values[k]) * (1 + COST) / (1 - COST)
            w = list(lo[i_ent[k]:i_ex[k]]) + [px]
            out.append(min(0.0, (min(w) / e[k] - 1) * 100) / a[i_sig[k]])
    return float(np.mean(out)) if out else None


def metrik(T):
    x = T.ret.values * 100; hari = max(1.0, float((T.days - 1).mean()))
    u1 = float(x.mean()); sw = x[x > 0].sum(); sl = -x[x < 0].sum()
    hp = T.assign(x=x).groupby('ent').x.mean()
    return dict(n=int(len(T)), u1=u1, u1_pangkas=pangkas(x), hari=hari, hari_bt=float(T.days.mean()), u2=21 * u1 / hari, k1=min(3.0, sw / sl) if sl > 0 else 3.0,
                k2=wilson_bawah(int((hp > 0).sum()), int(len(hp))), r1=cvar(x))


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--hanya'); ap.add_argument('--keluar', default=OUT); a = ap.parse_args(argv)
    kat = json.load(open(KATALOG, encoding='utf-8')); kat = kat['rows'] if isinstance(kat, dict) else kat
    ids = [r['id'] for r in kat if not a.hanya or r['id'] in a.hanya.split(',')]
    fr0, idx = muat(); M, semua, gagal = {}, [], {}
    for mid in ids:
        t0 = time.time()
        try:
            f = {t: g[['open', 'high', 'low', 'close', 'volume', 'turnover']].copy() for t, g in fr0.items()}
            m = importlib.import_module(f'kaedah.{mid}'); m.sedia(f, idx)
            T = trades(f, tmax=m.TMAX, warm=m.WARM); T = T[T.ent >= pd.Timestamp(START)]
        except Exception as e:  # noqa: BLE001 — kaedah yang gagal dilangkau dan dilapor
            gagal[mid] = f'{type(e).__name__}: {e}'[:200]; continue
        if len(T) < N_MIN:
            gagal[mid] = f'{len(T)} dagangan < {N_MIN}'; continue
        r = metrik(T); r['r2'] = mae_atr(T, fr0); r['varian'] = getattr(m, 'VARIAN', ''); M[mid] = r
        semua.append(T.assign(kaedah=mid, x=T.ret * 100)[['kaedah', 'ent', 'x']])
        print(f'{mid} n={r["n"]} u1={r["u1"]:.2f} hari={r["hari"]:.1f} r2={r["r2"]} ({time.time() - t0:.1f}s)', flush=True)
    A = pd.concat(semua); A['tanda'] = A.groupby('ent').x.transform('mean')
    for mid, v in A.assign(lebih=A.x - A.tanda).groupby('kaedah').lebih.mean().items():
        M[mid]['u3'] = float(v)
    tiang = {}; sw = [m for m in M if SWING[0] <= M[m]['hari_bt'] <= SWING[1]]
    for k in ('u1', 'u2', 'u3', 'k1', 'k2', 'r1', 'r2'):
        v = np.array([M[m][k] for m in sw if M[m].get(k) is not None], float)
        tiang[k] = [round(float(np.percentile(v, P_BAWAH)), 3), round(float(np.percentile(v, P_ATAS)), 3)]
    out = dict(versi=VERSI, dibina=time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), set='431', mula=START,
               persentil=[P_BAWAH, P_ATAS], swing=list(SWING), n_kaedah=len(sw), n_semua=len(M), tiang=tiang, gagal=gagal,
               kaedah={m: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for m, r in sorted(M.items())})
    os.makedirs(os.path.dirname(a.keluar), exist_ok=True)
    json.dump(out, open(a.keluar, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(n_kaedah=len(sw), n_semua=len(M), gagal=len(gagal), tiang=tiang), ensure_ascii=False))


if __name__ == '__main__':
    main()
