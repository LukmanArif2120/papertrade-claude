# stage.py — Stage Analysis gaya Stan Weinstein (bar mingguan, MA30) bagi posisi Papertrade C dan watchlist
# (dashboard: lajur Stage, dokumen db harian/stage). PAPARAN SAHAJA (keputusan pengguna 27 Okt 2026): bukan penapis
# belian dan bukan isyarat jual; keluar kekal ikut lorong kaedah dan lorong 2.
#
# Tiada sambungan ke stageanalysis.net (tiada API awam; kandungan screener berlangganan). Label dikira semula
# daripada stor harga repo mengikut takrif yang diterbitkan laman itu.
#
# Takrif (versi W30-r1):
#   bar mingguan = kumpulan W-FRI daripada bar harian stor (buka pertama, tinggi maks, rendah min, tutup akhir,
#                  volum jumlah). Minggu terakhir boleh separa ("minggu berjalan").
#   MA30 / MA10  = purata mudah 30 / 10 tutup mingguan. Cerun = MA30 minggu ini lawan minggu lalu.
#   peringkat    = 2 (naik)  jika tutup > MA30 dan MA30 menaik
#                  4 (turun) jika tutup < MA30 dan MA30 menurun
#                  0 ("1/3") selainnya — asas atau kawasan puncak; kedua-duanya kelihatan sama pada carta, jadi
#                  screener stageanalysis.net menggabungkannya. Medan `dari` memberi peringkat berarah sebelumnya:
#                  dari 4 = kawasan asas (Stage 1), dari 2 = kawasan puncak (Stage 3).
#   kitaran      = minggu pertama peringkat 2 selepas peringkat berarah 4 memulakan kitaran Stage 2 (sebaliknya bagi
#                  Stage 4). Surut sementara ke 1/3 tidak menetapkan semula kiraan (tiada Stage 4 = kitaran sama).
#   sub-stage    = 11 label screener stageanalysis.net:
#                  2A  minggu breakout pertama kitaran ini      4A  minggu breakdown pertama kitaran ini
#                  2 / 2−   dalam Stage 2, < 39 minggu          4 / 4−   dalam Stage 4, < 39 minggu
#                  2B / 2B− dalam Stage 2, >= 39 minggu         4B / 4B− dalam Stage 4, >= 39 minggu
#                  1/3      neutral
#                  "−" = harga menentang arah peringkat berbanding MA10 minggu (Stage 2: tutup < MA10 = corak hambar;
#                  Stage 4: tutup > MA10 = mula perk up).
#   kualiti      = penggred (+)/(−) Weinstein, BERASINGAN daripada "−" dalam label:
#                  (+) Mansfield > 0 DAN volum minggu mula kitaran >= 2x purata 4 minggu sebelumnya (jika minggu mula
#                      berada dalam liputan data; jika tidak, Mansfield > 0 sahaja). Bagi 1/3 tiada minggu breakout,
#                      jadi Mansfield > 0 sahaja.
#                  (−) Mansfield < 0.
#                  Mansfield = (tutup saham / tutup SPY) ÷ purata 52 minggunya − 1, dalam % (garis RP Mansfield).
#   tepat        = mula kitaran (atau mula larian 1/3) berada dalam liputan data. Stor = 520 bar harian ~ 104 minggu,
#                  jadi kitaran panjang tersensor: `minggu` menjadi had bawah dan label A tidak diberi.
#
# Guna:
#   python3 BacktestShariah2/standard/stage.py tulis [--folder <papertrade>] [--keluar data/stage/status.json]
#   python3 BacktestShariah2/standard/stage.py garis TICKER   -> jadual mingguan (tutup, MA30, peringkat, label)
import argparse, json, os, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import trend_status as TS  # noqa: E402

BS2 = os.path.dirname(HERE)
FAIL = os.path.join(BS2, 'data', 'stage', 'status.json')

VERSI = 'W30-r1'
N_MA, N_PENDEK, N_MANSFIELD = 30, 10, 52
MIN_MINGGU = N_MA + 1          # MA30 + satu minggu untuk cerun
LEWAT = 39                     # minggu dalam kitaran -> sub-stage B
N_VOL = 4                      # purata volum sebelum minggu mula
VOL_BREAKOUT = 2.0
MINUS = '−'               # tanda tolak (bukan hifen)
LAJUR = ['saham', 'p', 'label', 'kualiti', 'minggu', 'mula', 'tepat', 'dari', 'c', 'ma30', 'ma10', 'cerun',
         'mansfield', 'vol_mula', 'separa', 'n_minggu', 'sebab', 'tarikh_data']
K = {n: i for i, n in enumerate(LAJUR)}
TAKRIF = ('Stage Analysis Weinstein pada bar mingguan: Stage 2 = tutup > MA30 minggu dan MA30 menaik; Stage 4 = tutup < MA30 '
          'dan MA30 menurun; selainnya 1/3 (asas atau kawasan puncak). A = minggu breakout/breakdown pertama kitaran ini; '
          f'B = sudah {LEWAT} minggu atau lebih dalam kitaran; "{MINUS}" = harga menentang arah peringkat berbanding MA10 minggu. '
          'Kualiti (+)/(−) = Mansfield RP dan volum minggu mula. Paparan sahaja: bukan penapis belian, bukan isyarat jual.')


# ------------------------------------------------------------------ bar mingguan
def mingguan(g):
    """g: DataFrame harian date(int)/open/high/low/close[/volume] menaik -> DataFrame mingguan (indeks Period W-FRI)."""
    t = pd.to_datetime(g.date.astype(int).astype(str), format='%Y%m%d')
    ag = dict(open=('open', 'first'), high=('high', 'max'), low=('low', 'min'), close=('close', 'last'),
              tarikh=('date', 'last'), n=('date', 'size'))
    if 'volume' in g.columns:
        ag['volume'] = ('volume', 'sum')
    a = g.groupby(t.dt.to_period('W-FRI').to_numpy(), sort=True).agg(**ag)
    if 'volume' not in a.columns:
        a['volume'] = np.nan
    return a


def sma(x, n):
    return pd.Series(x).rolling(n).mean().to_numpy()


# ------------------------------------------------------------------ peringkat dan kitaran
def siri(c, ma30):
    """Peringkat setiap minggu: 2 naik, 4 turun, 0 = 1/3; NaN sebelum MA30 (dan minggu pertamanya: cerun belum ada)."""
    n = len(c); p = np.full(n, np.nan)
    for i in range(1, n):
        if np.isnan(ma30[i]) or np.isnan(ma30[i - 1]):
            continue
        if c[i] > ma30[i] and ma30[i] > ma30[i - 1]:
            p[i] = 2.0
        elif c[i] < ma30[i] and ma30[i] < ma30[i - 1]:
            p[i] = 4.0
        else:
            p[i] = 0.0
    return p


def jejak(p):
    """-> (mula, dari, tepat, awal) setiap minggu.
    mula  = indeks minggu mula keadaan yang dipapar (kitaran 2/4, atau larian 1/3 semasa)
    dari  = peringkat berarah sebelum keadaan ini (None jika tidak diketahui)
    tepat = mula itu berada dalam liputan data
    awal  = minggu ini ialah minggu breakout/breakdown pertama kitaran (label A)"""
    n = len(p)
    mula = np.full(n, -1, int); dari = np.full(n, np.nan); tepat = np.zeros(n, bool); awal = np.zeros(n, bool)
    i0 = anc = neu = cur = prev = None
    for i in range(n):
        if np.isnan(p[i]):
            continue
        if i0 is None:
            i0 = i
        x = p[i]
        if x:
            neu = None
            if cur is None or x != cur:
                prev, cur, anc = cur, x, i
                awal[i] = i > i0          # minggu pertama liputan tidak boleh dipanggil breakout
            mula[i] = anc
            dari[i] = np.nan if prev is None else prev
            tepat[i] = prev is not None
        else:
            if neu is None:
                neu = i
            mula[i] = neu
            dari[i] = np.nan if cur is None else cur
            tepat[i] = neu > i0
    return mula, dari, tepat, awal


def label(p, minggu, awal, bawah_ma10):
    """Label sub-stage screener stageanalysis.net."""
    if not p:
        return '1/3'
    g = '2' if p == 2 else '4'
    if awal:
        return g + 'A'
    b = 'B' if minggu >= LEWAT else ''
    if bawah_ma10 is None:
        return g + b
    lemah = bawah_ma10 if p == 2 else not bawah_ma10
    return g + b + (MINUS if lemah else '')


def kualiti(mf, vol_mula):
    """(+) RS positif (dan volum mula >= 2x jika diketahui); (−) RS negatif; '' selainnya."""
    if mf is None:
        return ''
    if mf < 0:
        return MINUS
    if mf > 0 and (vol_mula is None or vol_mula >= VOL_BREAKOUT):
        return '+'
    return ''


# ------------------------------------------------------------------ satu saham
def _f(v, n=2):
    return None if v is None or not np.isfinite(v) else round(float(v), n)


def kira(g, spy=None, tarikh_pasaran=0):
    """Ringkasan stage satu ticker. g: DataFrame harian; spy: Series tutup mingguan SPY (indeks Period W-FRI)."""
    a = mingguan(g)
    n = len(a)
    d = a.tarikh.to_numpy(int)
    r = dict(n_minggu=n, tarikh_data=int(d[-1]) if n else None)
    if n:
        r['c'] = float(a.close.iloc[-1])
        akhir = a.index[-1].end_time
        r['separa'] = bool(tarikh_pasaran and int(akhir.strftime('%Y%m%d')) > tarikh_pasaran)
    if n < MIN_MINGGU:
        r.update(p=None, sebab=f'sejarah {n} minggu < {MIN_MINGGU}')
        return r
    c = a.close.to_numpy(float); v = a.volume.to_numpy(float)
    ma30, ma10 = sma(c, N_MA), sma(c, N_PENDEK)
    p = siri(c, ma30)
    if np.isnan(p[-1]):
        r.update(p=None, sebab='MA30 belum boleh dikira pada minggu terakhir')
        return r
    mula, dari, tepat, awal = jejak(p)
    i = n - 1; m0 = int(mula[i]); pr = int(p[i])
    r.update(p=pr, minggu=i - m0 + 1, mula=int(d[m0]), tepat=bool(tepat[i]),
             dari=None if np.isnan(dari[i]) else int(dari[i]),
             ma30=_f(ma30[i]), ma10=_f(ma10[i]), cerun=_f((ma30[i] / ma30[i - 1] - 1) * 100, 3))
    vm = None
    if pr and m0 >= N_VOL:
        asas = np.nanmean(v[m0 - N_VOL:m0])
        if np.isfinite(asas) and asas > 0 and np.isfinite(v[m0]):
            vm = float(v[m0] / asas)
    r['vol_mula'] = _f(vm, 2)
    mf = None
    if spy is not None:
        s = spy.reindex(a.index).to_numpy(float)
        if np.isfinite(s).sum() >= N_MANSFIELD:
            rl = pd.Series(c / s)
            x = (rl / rl.rolling(N_MANSFIELD, min_periods=N_MANSFIELD).mean() - 1).iloc[-1] * 100
            mf = None if not np.isfinite(x) else float(x)
    r['mansfield'] = _f(mf, 2)
    bawah = None if np.isnan(ma10[i]) else bool(c[i] < ma10[i])
    r['label'] = label(pr, r['minggu'], bool(awal[i]), bawah)
    r['kualiti'] = kualiti(mf, vm if r['tepat'] else None)
    return r


# ------------------------------------------------------------------ dokumen db
def baris(t, r):
    o = [None] * len(LAJUR); o[0] = t
    if not r:
        return o
    for f in LAJUR[1:]:
        v = r.get(f)
        o[K[f]] = int(v) if isinstance(v, (bool, np.bool_)) else v
    return o


def spy_mingguan(idx):
    g = (idx or {}).get('SPY')
    return None if g is None or not len(g) else mingguan(g).close


def dokumen(H, saham, idx=None):
    """Dokumen db harian/stage. H: {ticker: DataFrame harian}; saham: alam papan (posisi C + Moomoo lama + watchlist)."""
    spy = spy_mingguan(idx)
    tarikh = max((int(g.date.iloc[-1]) for g in H.values() if len(g)), default=0)
    rows = []; n = {}
    for t in sorted(saham):
        g = H.get(t)
        r = kira(g, spy, tarikh) if g is not None and len(g) else None
        rows.append(baris(t, r))
        k = (r or {}).get('label') or 'tiada'
        n[k] = n.get(k, 0) + 1
    return dict(tarikh=tarikh, versi=VERSI, lajur=LAJUR, rows=rows, kiraan=n, takrif=TAKRIF)


def bina(folder=TS.PT, stor=TS.STOR, terkini=TS.TERKINI):
    H, _ = TS.muat_harga(stor, terkini, lajur=('date', 'open', 'high', 'low', 'close', 'volume'))
    I, _ = TS.muat_harga(stor, terkini, fail=('harga_idx.csv',))
    return dokumen(H, TS.alam(folder, H), I)


# ------------------------------------------------------------------ garis masa
def garis(g, spy=None):
    a = mingguan(g)
    c = a.close.to_numpy(float); ma30, ma10 = sma(c, N_MA), sma(c, N_PENDEK)
    p = siri(c, ma30); mula, dari, tepat, awal = jejak(p)
    out = []
    for i in range(len(c)):
        if np.isnan(p[i]):
            continue
        bawah = None if np.isnan(ma10[i]) else bool(c[i] < ma10[i])
        out.append((int(a.tarikh.iloc[i]), round(c[i], 2), round(float(ma30[i]), 2), int(p[i]),
                    label(int(p[i]), i - int(mula[i]) + 1, bool(awal[i]), bawah), i - int(mula[i]) + 1,
                    '' if tepat[i] else 'tersensor'))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Stage Analysis Weinstein mingguan (dashboard harian/stage)')
    ap.add_argument('arahan', choices=['tulis', 'garis']); ap.add_argument('ticker', nargs='?')
    ap.add_argument('--folder', default=TS.PT); ap.add_argument('--stor', default=TS.STOR); ap.add_argument('--terkini', default=TS.TERKINI)
    ap.add_argument('--keluar', default=FAIL)
    a = ap.parse_args(argv)
    if a.arahan == 'tulis':
        doc = bina(a.folder, a.stor, a.terkini)
        os.makedirs(os.path.dirname(os.path.abspath(a.keluar)), exist_ok=True)
        s = json.dumps(doc, separators=(',', ':'), ensure_ascii=False)
        open(a.keluar, 'w', encoding='utf-8').write(s)
        urut = sorted(doc['kiraan'].items(), key=lambda x: -x[1])
        print(f"{len(doc['rows'])} saham, {len(s.encode())} bait, tarikh {doc['tarikh']}: "
              + ', '.join(f'{k} {v}' for k, v in urut))
    else:
        H, _ = TS.muat_harga(a.stor, a.terkini, lajur=('date', 'open', 'high', 'low', 'close', 'volume'))
        I, _ = TS.muat_harga(a.stor, a.terkini, fail=('harga_idx.csv',))
        for x in garis(H[a.ticker], spy_mingguan(I)):
            print(x[0], f'tutup {x[1]:10.2f}  MA30 {x[2]:10.2f}  peringkat {x[3]}  {x[4]:4s} minggu {x[5]:3d} {x[6]}')


if __name__ == '__main__':
    main()
