# Gred Sektor dan Industri v2 (sejak 19 Okt 2026; kajian 18 Okt 2026: BacktestShariah2/kajian/KAJIAN_GRED_KUMPULAN.md).
# Kekuatan kumpulan SELURUH pasaran AS (semua ticker papertrade/peta_industri.csv, harga >= USD5; industri = plate Moomoo,
# sektor = SEKTOR_INDUSTRI). Indeks setiap kumpulan = purata sama rata pulangan harian ahli yang layak.
#
#   Industri: skor = pangkat persentil (Weinstein + pangkat median pulangan 1 bulan) antara industri, di mana
#             Weinstein = purata 3 syarat: (1) RS lawan SPY > purata 52 minggunya (Mansfield RS > 0), (2) Mansfield RS
#             naik dalam 21 sesi, (3) indeks > purata 150 hari (30 minggu) yang sedang naik (lawan 20 sesi lalu).
#   Sektor:   skor = pangkat persentil % saham layak di atas SMA200 antara sektor (paparan sahaja; tidak membantu memilih
#             saham dalam kajian, tidak dikira dalam gred_keseluruhan).
#   Gred: A > 80, B > 60, C > 40, D > 20, E <= 20 (kuintil). Kajian: A dan E signifikan; B–D hampir neutral.
#
# Guna (GitHub Actions .github/workflows/gred_kumpulan.yml, sebelum harian.yml):
#   python3 gred_kumpulan.py [--peta papertrade/peta_industri.csv] [--keluar data/kumpulan/gred_kumpulan.csv]
#       [--sejarah data/kumpulan/gred_kumpulan_sejarah.csv] [--hari 470]
import argparse, os, sys, time
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sektor_pasaran import SEKTOR_INDUSTRI  # noqa: E402

HARGA_MIN = 5.0
MIN_SAHAM = 3
LAJUR = ['tarikh', 'jenis', 'nama', 'sektor', 'n', 'skor', 'gred', 'w_rs_positif', 'w_rs_naik', 'w_trend', 'm1m_med',
         'pct_atas_sma200', 'dibina']


def gred(skor):
    if skor is None or pd.isna(skor):
        return '–'
    return 'A' if skor > 80 else 'B' if skor > 60 else 'C' if skor > 40 else 'D' if skor > 20 else 'E'


def muat_turun(tickers, mula, saiz=200, rehat=2.0):
    import yfinance as yf
    C, gagal = [], []
    for i in range(0, len(tickers), saiz):
        kump = tickers[i:i + saiz]; d = None
        for cuba in range(3):
            try:
                d = yf.download([t.replace('.', '-') for t in kump], start=mula, auto_adjust=True, progress=False,
                                threads=True, group_by='column')
                break
            except Exception as e:  # noqa: BLE001
                print('ralat', i, e, flush=True); time.sleep(10 * (cuba + 1))
        if d is None or d.empty:
            gagal += kump; continue
        c = d['Close'] if len(kump) > 1 else d[['Close']].set_axis([kump[0]], axis=1)
        c.columns = [x.replace('-', '.') for x in c.columns]
        kosong = [t for t in kump if t not in c.columns or c[t].notna().sum() == 0]
        gagal += kosong
        C.append(c.drop(columns=[t for t in kosong if t in c.columns]).astype('float64'))
        time.sleep(rehat)
    return C, gagal


def muat_turun_penuh(tickers, mula):
    """Cuba semula ticker yang gagal (had kadar Yahoo) dalam kumpulan kecil dengan rehat lebih lama."""
    C, gagal = muat_turun(tickers, mula)
    for saiz, rehat in [(50, 8.0), (20, 15.0), (10, 30.0)]:
        if not gagal:
            break
        print(f'cuba semula: {len(gagal)} ticker', flush=True); time.sleep(60)
        c2, gagal = muat_turun(gagal, mula, saiz=saiz, rehat=rehat)
        C += c2
    C = pd.concat(C, axis=1).sort_index()
    return C.loc[:, ~C.columns.duplicated()], gagal


def siri(C, peta, spy):
    """C: tutup harian (index tarikh, lajur ticker); peta: DataFrame index ticker, lajur industri & sektor; spy: Series.
    Pulangkan dict jenis -> dict komponen (DataFrame tarikh x kumpulan) dan 'skor' (0–100)."""
    C = C.dropna(how='all').sort_index()
    R = C.pct_change(fill_method=None).clip(-0.5, 1.0)
    layak = C.shift(1) >= HARGA_MIN
    r21 = C / C.shift(21) - 1
    r21 = r21.where(r21.abs() <= 10)
    atas200 = C > C.rolling(200).mean()
    spy = spy.reindex(C.index).ffill()
    out = {}
    for jenis, kol in [('Industri', 'industri'), ('Sektor', 'sektor')]:
        I, M1, N, A200 = {}, {}, {}, {}
        for nama, g in peta.groupby(kol):
            c = [t for t in g.index if t in C.columns]
            if len(c) < MIN_SAHAM or nama in ('', 'Lain-lain'):
                continue
            L = layak[c]
            I[nama] = (1 + R[c].where(L).mean(axis=1).fillna(0)).cumprod()
            M1[nama] = r21[c].where(L).median(axis=1)
            N[nama] = L.sum(axis=1)
            A200[nama] = atas200[c].where(L).sum(axis=1) / N[nama].replace(0, np.nan)
        I, M1, N, A200 = (pd.DataFrame(x) for x in (I, M1, N, A200))
        ok = N >= MIN_SAHAM
        rs = I.div(spy, axis=0); mrs = rs / rs.rolling(252).mean() - 1; ma = I.rolling(150).mean()
        w1 = (mrs > 0).astype(float).where(mrs.notna())
        w2 = (mrs > mrs.shift(21)).astype(float).where(mrs.notna() & mrs.shift(21).notna())
        w3 = ((I > ma) & (ma > ma.shift(20))).astype(float).where(mrs.notna() & ma.shift(20).notna())
        wst = (w1 + w2 + w3) / 3
        pk = lambda X: X.where(ok).rank(axis=1, pct=True)
        if jenis == 'Industri':
            skor = 100 * pk(wst + pk(M1))
        else:
            skor = 100 * pk(A200)
        out[jenis] = dict(skor=skor, w1=w1, w2=w2, w3=w3, m1m=M1, a200=A200, n=N)
    return out


def snapshot(S, peta, dibina, pada=None):
    """Gred setiap kumpulan pada sesi terakhir (atau sesi `pada`, Timestamp, untuk isi sejarah)."""
    rows = []
    for jenis, d in S.items():
        t = d['skor'].dropna(how='all').index.max() if pada is None else pada
        if t not in d['skor'].index:
            continue
        if pd.isna(t):
            continue
        for nama in d['skor'].columns:
            sk = d['skor'].at[t, nama]
            if pd.isna(sk):
                continue
            v = lambda k: d[k].at[t, nama]
            sek = SEKTOR_INDUSTRI.get(nama, '') if jenis == 'Industri' else nama
            rows.append(dict(tarikh=t.strftime('%Y-%m-%d'), jenis=jenis, nama=nama, sektor=sek, n=int(v('n')),
                             skor=round(float(sk), 1), gred=gred(sk),
                             w_rs_positif='' if pd.isna(v('w1')) else int(v('w1')),
                             w_rs_naik='' if pd.isna(v('w2')) else int(v('w2')),
                             w_trend='' if pd.isna(v('w3')) else int(v('w3')),
                             m1m_med='' if pd.isna(v('m1m')) else round(100 * float(v('m1m')), 2),
                             pct_atas_sma200='' if pd.isna(v('a200')) else round(100 * float(v('a200')), 1),
                             dibina=dibina))
    return pd.DataFrame(rows, columns=LAJUR).sort_values(['jenis', 'skor'], ascending=[True, False])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--peta', default=os.path.join(BS2, 'papertrade', 'peta_industri.csv'))
    ap.add_argument('--keluar', default=os.path.join(BS2, 'data', 'kumpulan', 'gred_kumpulan.csv'))
    ap.add_argument('--sejarah', default=os.path.join(BS2, 'data', 'kumpulan', 'gred_kumpulan_sejarah.csv'))
    ap.add_argument('--hari', type=int, default=470)
    ap.add_argument('--had', type=int, default=0)
    ap.add_argument('--sejarah-sesi', type=int, default=0,
                    help='tulis juga snapshot N sesi sebelum sesi terakhir ke --sejarah (isi semula gred posisi lama)')
    a = ap.parse_args(argv)
    peta = pd.read_csv(a.peta, keep_default_na=False).drop_duplicates('ticker').set_index('ticker')
    peta['sektor'] = peta.industri.map(SEKTOR_INDUSTRI).fillna('Lain-lain')
    tickers = sorted(peta.index.astype(str))[: a.had or None]
    mula = (date.today() - timedelta(days=a.hari)).isoformat()
    C, gagal = muat_turun_penuh(tickers + ['SPY'], mula)
    if 'SPY' not in C.columns:
        raise SystemExit('SPY tiada: gred tidak dikira')
    spy = C.pop('SPY')
    print(f'saham {C.shape[1]} / {len(tickers)}, gagal {len(gagal)}, bar {len(C)}', flush=True)
    if C.shape[1] < 0.9 * len(tickers):
        raise SystemExit(f'hanya {C.shape[1]} daripada {len(tickers)} saham dimuat turun: gred tidak ditulis')
    dibina = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M MYT')
    S = siri(C, peta.loc[[t for t in peta.index if t in C.columns]], spy)
    snap = snapshot(S, peta, dibina)
    os.makedirs(os.path.dirname(a.keluar), exist_ok=True)
    snap.to_csv(a.keluar, index=False)
    if a.sejarah:
        lama = pd.read_csv(a.sejarah, keep_default_na=False) if os.path.exists(a.sejarah) else pd.DataFrame(columns=LAJUR)
        baru = [snap] + [snapshot(S, peta, dibina, t) for t in C.index[-1 - a.sejarah_sesi:-1]]
        tarikh = {x for b in baru for x in b.tarikh.astype(str)}
        lama = lama[~lama.tarikh.astype(str).isin(tarikh)]
        pd.concat([lama] + baru).sort_values(['tarikh', 'jenis', 'skor'], ascending=[True, True, False]).to_csv(a.sejarah, index=False)
    for j in ['Industri', 'Sektor']:
        s = snap[snap.jenis == j]
        print(j, len(s), dict(s.gred.value_counts().sort_index()), '| teratas:', ', '.join(s.nama.head(5)))


if __name__ == '__main__':
    main()
