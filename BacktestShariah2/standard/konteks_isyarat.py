"""Konteks isyarat DIBEKUKAN pada malam isyarat — supaya soalan "kaedah ini untung dalam keadaan apa?" boleh dijawab
kemudian tanpa membina semula sejarah (audit 7 Nov 2026, keputusan pengguna "lakukan fasa seterusnya").

Masalah yang ditutup: baris Lejar hanya menyimpan rank, henti, sasaran dan tutup. Rejim pasaran, ATR%, jarak ke tinggi 52
minggu, RS, sektor dan jarak ke earnings pada hari isyarat TIDAK disimpan, sedangkan `data/trend/status.json` dan
`data/stage/status.json` ditulis ganti setiap hari dan stor harga hanya menyimpan 520 bar yang dilaras semula. Kajian 7 Nov
2026 mendapati kelebihan relatif saham pemimpin bertukar tanda ikut rejim QQQ (12/17 tahun), jadi tanpa konteks ini kad skor
tidak boleh membezakan "kaedah lemah" daripada "kaedah yang diuji dalam rejim yang salah".

Dua fail TAMBAH-SAHAJA di `data/konteks/` (DI LUAR `lejar/`, kerana `lejar.bina_semula` memadam fail di bawah lejar/):
  pasaran.csv            satu baris setiap sesi isyarat: rejim QQQ/SPY (ON = tutup > SMA50 DAN SMA10 > SMA20, sama dengan
                         gate G1), jarak dari puncak 52 minggu, RV21, bilangan saham beri isyarat.
  saham_YYYYMM.csv.gz    satu baris setiap saham-hari yang diberi isyarat oleh mana-mana kaedah: n_kaedah, ATR14%, jarak ke
                         tinggi 252 sesi, ROC63 + pangkat persentil dalam stor hari itu, templat trend (tutup > SMA50 > SMA150
                         > SMA200), tutup/SMA200, nilai dagang 20 hari, RS pasaran (`data/rs/rs_pasaran.csv`), sektor/industri
                         (`data/skrin/tv_us.csv`), hari ke earnings seterusnya dan sejak earnings lalu
                         (kalendar gabungan `standard/kalendar_earnings.py`).
Lajur `langsung` = True jika baris dikira pada malam sesi itu sendiri (sesi = bar stor terakhir); False = isian kemudian
(dikira daripada stor semasa — nisbah harga tidak berubah dengan pelarasan, tetapi sektor dan kalendar earnings ialah
petikan semasa). Baris yang sudah ditulis TIDAK PERNAH dikira semula.

  python3 BacktestShariah2/standard/konteks_isyarat.py            # sesi isyarat yang belum ada (idempoten)
  python3 BacktestShariah2/standard/konteks_isyarat.py --semak    # laporan liputan sahaja
Dijalankan oleh `lejar.yml` selepas `lejar.py jalan`. Rekod sahaja: tiada order, tiada wang sebenar.
"""
import argparse
import glob
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
STOR = os.environ.get('LEJAR_STOR', os.path.join(BS2, 'data', 'harga', 'stor'))
KONTEKS = os.environ.get('KONTEKS_DIR', os.path.join(BS2, 'data', 'konteks'))
RS = os.environ.get('KONTEKS_RS', os.path.join(BS2, 'data', 'rs', 'rs_pasaran.csv'))
TV = os.environ.get('KONTEKS_TV', os.path.join(BS2, 'data', 'skrin', 'tv_us.csv'))
EARN = os.environ.get('KONTEKS_EARN')   # folder pemangkin (ujian); lalai = kalendar_earnings.PEMANGKIN
VERSI = 'konteks v1 (7 Nov 2026)'
L_PASARAN = ['sesi', 'qqq_on', 'qqq_dari_puncak', 'qqq_rv21', 'spy_on', 'spy_dari_puncak', 'n_saham', 'n_isyarat',
             'langsung', 'dikira', 'versi']
L_SAHAM = ['sesi', 'saham', 'n_kaedah', 'tutup', 'atr_pct', 'jarak52', 'roc63', 'pangkat_roc63', 'templat', 'atas_sma200',
           'nilai20_juta', 'rs', 'sektor', 'industri', 'hari_ke_earnings', 'hari_sejak_earnings', 'langsung']


def _ymd(s):
    s = str(s).replace('-', '')
    return f'{s[:4]}-{s[4:6]}-{s[6:8]}'


def sesi_isyarat(lejar=None):
    """Sesi (YYYYMMDD) yang ada fail isyarat Lejar."""
    f = glob.glob(os.path.join(lejar or LEJAR, 'isyarat', '*.csv.gz'))
    return sorted(os.path.basename(x)[:8] for x in f)


def sudah_ada(konteks=None):
    p = os.path.join(konteks or KONTEKS, 'pasaran.csv')
    if not os.path.exists(p):
        return set()
    return set(pd.read_csv(p, dtype={'sesi': str}).sesi.str.replace('-', '', regex=False))


def ciri_harga(stor=None):
    """DataFrame (ticker, date YYYYMMDD) dengan ciri harga yang dikira hanya daripada bar sehingga hari itu."""
    stor = stor or STOR
    f = [os.path.join(stor, x) for x in ('harga_A.csv', 'harga_B.csv')]
    H = pd.concat([pd.read_csv(x) for x in f if os.path.exists(x)], ignore_index=True)
    H['date'] = H.date.astype(str)
    H = H.drop_duplicates(['ticker', 'date']).sort_values(['ticker', 'date']).reset_index(drop=True)
    g = H.groupby('ticker', sort=False)
    c = H.close
    pc = g.close.shift(1)
    tr = np.maximum(H.high - H.low, np.maximum((H.high - pc).abs(), (H.low - pc).abs()))
    atr = tr.groupby(H.ticker, sort=False).transform(lambda s: s.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean())
    sma = {n: g.close.transform(lambda s, n=n: s.rolling(n, min_periods=n).mean()) for n in (50, 150, 200)}
    hi = g.high.transform(lambda s: s.rolling(252, min_periods=200).max())
    nilai = (c * H.volume).groupby(H.ticker, sort=False).transform(lambda s: s.rolling(20, min_periods=20).mean())
    X = pd.DataFrame(dict(
        ticker=H.ticker, date=H.date, tutup=c, atr_pct=atr / c * 100, jarak52=(c / hi - 1) * 100,
        roc63=(c / g.close.shift(63) - 1) * 100,
        templat=((c > sma[50]) & (sma[50] > sma[150]) & (sma[150] > sma[200])).astype(object),
        atas_sma200=(c > sma[200]).astype(object), nilai20_juta=nilai / 1e6))
    X.loc[sma[200].isna().to_numpy(), ['templat', 'atas_sma200']] = None   # belum cukup sejarah: tidak diketahui
    X['pangkat_roc63'] = X.groupby('date').roc63.rank(pct=True) * 100
    return X


def pasaran(stor=None):
    """{YYYYMMDD: dict} rejim QQQ dan SPY setiap sesi."""
    p = os.path.join(stor or STOR, 'harga_idx.csv')
    if not os.path.exists(p):
        return {}
    d = pd.read_csv(p)
    d['date'] = d.date.astype(str)
    out = {}
    for t in ('QQQ', 'SPY'):
        x = d[d.ticker == t].sort_values('date').set_index('date').close
        on = (x > x.rolling(50).mean()) & (x.rolling(10).mean() > x.rolling(20).mean())
        on = on.where(x.rolling(50).mean().notna())
        puncak = (x / x.rolling(252, min_periods=1).max() - 1) * 100
        rv = np.log(x).diff().rolling(21).std() * np.sqrt(252) * 100
        for k in x.index:
            r = out.setdefault(k, {})
            v = on.get(k)
            r[f'{t.lower()}_on'] = None if pd.isna(v) else bool(v)
            r[f'{t.lower()}_dari_puncak'] = round(float(puncak[k]), 2)
            if t == 'QQQ':
                r['qqq_rv21'] = None if pd.isna(rv[k]) else round(float(rv[k]), 2)
    return out


def earnings(path=None):
    """Kalendar earnings GABUNGAN repo (`standard/kalendar_earnings.py`: Nasdaq + yfinance + tambahan disahkan).
    `path` = folder pemangkin (ujian). Pulang {ticker: {date: sumber}}."""
    sys.path.insert(0, HERE)
    import kalendar_earnings as KE
    return KE.muat(path) if path else KE.muat()


def jarak_earnings(K, t, sesi):
    """(hari ke earnings seterusnya yang dipercayai > sesi, hari sejak earnings terakhir <= sesi), hari kalendar;
    peraturan 'dipercayai' = kalendar_earnings.seterusnya (dalam 80 hari atau siri berterusan). None jika tiada."""
    import kalendar_earnings as KE
    from datetime import date, timedelta
    D = date.fromisoformat(_ymd(sesi))
    nx, _ = KE.seterusnya(K, t, D + timedelta(days=1))
    lp, _ = KE.lalu(K, t, D + timedelta(days=1))
    return ((nx - D).days if nx else None), ((D - lp).days if lp else None)


def rs_sesi(path=None):
    path = path or RS
    if not os.path.exists(path):
        return pd.DataFrame(columns=['tarikh', 'ticker', 'rs'])
    r = pd.read_csv(path, usecols=['tarikh', 'ticker', 'rs'], dtype={'tarikh': str})
    r['tarikh'] = r.tarikh.str.replace('-', '', regex=False)
    return r


def sektor(path=None):
    path = path or TV
    if not os.path.exists(path):
        return {}
    t = pd.read_csv(path, usecols=['ticker', 'sector', 'industry'], dtype=str)
    return {r.ticker: (r.sector, r.industry) for r in t.itertuples()}


def kira(sesi_baru, lejar=None, stor=None, konteks=None):
    """Kira dan TAMBAH baris bagi `sesi_baru` (senarai YYYYMMDD). Pulang (n_sesi, n_baris)."""
    konteks = konteks or KONTEKS
    if not sesi_baru:
        return 0, 0
    os.makedirs(konteks, exist_ok=True)
    X = ciri_harga(stor)
    akhir = X.date.max()
    M = pasaran(stor)
    R = rs_sesi()
    S = sektor()
    E = earnings(EARN)
    rs_tarikh = np.array(sorted(R.tarikh.unique())) if len(R) else np.array([])
    kini = pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC')
    baris_p, n_baris = [], 0
    for s in sorted(sesi_baru):
        f = os.path.join(lejar or LEJAR, 'isyarat', f'{s}.csv.gz')
        if not os.path.exists(f):
            continue
        I = pd.read_csv(f, usecols=['kaedah', 'saham'])
        nk = I.groupby('saham').kaedah.nunique()
        D = X[X.date == s].set_index('ticker')
        # RS: petikan pada sesi itu, atau yang terakhir sebelum (dalam 5 hari kalendar); tiada jika lebih lama
        rsv = {}
        if len(rs_tarikh):
            j = int(np.searchsorted(rs_tarikh, s, side='right')) - 1
            if j >= 0 and (pd.Timestamp(_ymd(s)) - pd.Timestamp(_ymd(rs_tarikh[j]))).days <= 5:
                rsv = R[R.tarikh == rs_tarikh[j]].set_index('ticker').rs.to_dict()
        langsung = s == akhir
        rows = []
        for t, n in nk.items():
            d = D.loc[t] if t in D.index else None
            ke, sejak = jarak_earnings(E, t, s)
            sk, ind = S.get(t, (None, None))

            def v(k, nd=3):
                if d is None:
                    return None
                x = d[k]
                return None if pd.isna(x) else (bool(x) if isinstance(x, (bool, np.bool_)) else round(float(x), nd))
            rows.append(dict(sesi=_ymd(s), saham=t, n_kaedah=int(n), tutup=v('tutup', 4), atr_pct=v('atr_pct'),
                             jarak52=v('jarak52', 2), roc63=v('roc63', 2), pangkat_roc63=v('pangkat_roc63', 1),
                             templat=v('templat'), atas_sma200=v('atas_sma200'), nilai20_juta=v('nilai20_juta', 2),
                             rs=rsv.get(t), sektor=sk, industri=ind, hari_ke_earnings=ke,
                             hari_sejak_earnings=sejak, langsung=langsung))
        B = pd.DataFrame(rows, columns=L_SAHAM)
        fb = os.path.join(konteks, f'saham_{s[:6]}.csv.gz')
        if os.path.exists(fb):
            lama = pd.read_csv(fb, dtype={'sesi': str})
            B = B[~B.sesi.isin(set(lama.sesi))]          # TAMBAH-SAHAJA: baris sedia ada tidak disentuh
            B = pd.concat([lama, B], ignore_index=True)
        B.to_csv(fb, index=False, compression='gzip')
        m = M.get(s, {})
        baris_p.append(dict(sesi=_ymd(s), qqq_on=m.get('qqq_on'), qqq_dari_puncak=m.get('qqq_dari_puncak'),
                            qqq_rv21=m.get('qqq_rv21'), spy_on=m.get('spy_on'), spy_dari_puncak=m.get('spy_dari_puncak'),
                            n_saham=int(len(nk)), n_isyarat=int(len(I)), langsung=langsung, dikira=kini, versi=VERSI))
        n_baris += len(rows)
    if baris_p:
        fp = os.path.join(konteks, 'pasaran.csv')
        P = pd.DataFrame(baris_p, columns=L_PASARAN)
        if os.path.exists(fp):
            lama = pd.read_csv(fp, dtype={'sesi': str})
            P = pd.concat([lama, P[~P.sesi.isin(set(lama.sesi))]], ignore_index=True)
        P.sort_values('sesi').to_csv(fp, index=False)       # ditulis TERAKHIR: penanda sesi siap
    return len(baris_p), n_baris


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--semak', action='store_true')
    a = ap.parse_args()
    semua, ada = sesi_isyarat(), sudah_ada()
    baru = [s for s in semua if s not in ada]
    if a.semak:
        print(f'konteks: {len(ada)} sesi ada, {len(baru)} belum ({", ".join(baru[:5])}{"…" if len(baru) > 5 else ""})')
        return 0
    n, b = kira(baru)
    print(f'konteks_isyarat: {n} sesi baharu, {b} baris saham-hari ({VERSI})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
