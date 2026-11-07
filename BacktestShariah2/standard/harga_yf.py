"""Harga harian percuma (yfinance) untuk stor harga papertrade.

Dijalankan oleh GitHub Actions (`.github/workflows/harga_harian.yml`) selepas pasaran AS tutup;
sesi Claude tidak boleh capai Yahoo (polisi rangkaian), jadi tugasan Claude hanya membaca fail di repo.

Subarahan:
  python3 harga_yf.py terkini  [--hari 10]        -> data/harga/terkini.csv (10 sesi terakhir, semua universe)
  python3 harga_yf.py sejarah  [--maks 300]       -> data/harga/sejarah.csv (520 bar; ticker dalam perlu_sejarah.txt)
  python3 harga_yf.py gabung   --stor DIR [--fail F ...] [--kuarantin F]   gabung ke stor harga_A/B/idx.csv (format
                                                         kod/stor.py); lalai terkini.csv; sejarah.csv hanya jika diberi
                                                         dengan --fail; kuarantin lalai data/harga/kuarantin.csv (stor repo)
  python3 harga_yf.py semak    --kline TICKER=fail.json ... banding dengan kline Moomoo; keluar 1 jika beza > 0.5%

Universe = set 431 (data_mentah/dataset_S*.csv) + semua saham dalam papertrade/*.csv + data/harga/univ.txt
(senarai skrin Shariah Moomoo, ditulis oleh imbasan 8:02 malam) + saham posisi Lejar terbuka dan isyarat Lejar menunggu
(lejar/terbuka.csv, lejar/tunggu.csv; sejak 7 Nov 2026) + SPY, QQQ. Tanpa Lejar, saham yang keluar daripada univ.txt
(NEGG jatuh bawah skrin $10 pada 23 Okt 2026) berhenti mendapat bar dan posisi Lejarnya ditutup 'delist' secara palsu.
Kuarantin (7 Nov 2026; standard/kuarantin.py, data/harga/kuarantin.csv): keputusan 'anomali', faktor kembar dan peristiwa
direktori Nasdaq tukar_nama/buang dalam tetingkap bar baharu MEMBEKUKAN bar stor ticker itu (tiada timpa, tiada tambah);
ticker kuarantin dimuat turun semula sejarah penuh (`sejarah`) dan dilepaskan hanya apabila sejarah segar konsisten dengan
bar stor yang dipercayai (semak_kuarantin).
Harga: OHLC mentah (auto_adjust=False; split dilaras oleh Yahoo, dividen tidak). Sumber tidak rasmi —
Moomoo menang jika berbeza. NOTA (22 Okt 2026, laporan kajian 'Pengesanan data tercemar yang tinggal'): bar stor sebelum
~2 Okt 2026 berasal daripada data backtest (kline Moomoo dilaras hadapan termasuk dividen = konvensyen backtest); bar
yfinance selepasnya tidak dilaras dividen. Peristiwa besar (spin-off, dividen >= 2%) dilaras melalui data/harga/faktor.csv.
"""
import sys, os, json, glob, argparse, time
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
ROOT = os.path.dirname(BS2)
HARGA = os.path.join(BS2, 'data', 'harga')
sys.path.insert(0, os.path.join(BS2, 'kod'))
from stor import LAJ, SIMPAN_BAR, TOL_LARAS, baca_kline, nisbah_laras  # noqa: E402
import kuarantin as KR  # noqa: E402

IDX = ['SPY', 'QQQ']
TOLERANSI = 0.005


def ke_yahoo(t):
    return t.replace('.', '-')


def dari_yahoo(t):
    return t.replace('-', '.')


def set_431():
    s = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'data_mentah', 'dataset_S*.csv'))):
        s |= set(pd.read_csv(f, usecols=['ticker']).ticker.dropna().astype(str))
    return s


def universe(lejar_dir=None):
    s = set_431()
    for f in glob.glob(os.path.join(BS2, 'papertrade', '*.csv')):
        d = pd.read_csv(f, nrows=0)
        kol = next((c for c in d.columns if c.lower() in ('saham', 'ticker')), None)
        if kol and not f.endswith(('peta_industri.csv', 'sektor_pasaran.csv', 'sektor.csv')):
            s |= set(pd.read_csv(f, usecols=[kol])[kol].dropna().astype(str).str.strip())
    u = os.path.join(HARGA, 'univ.txt')
    if os.path.exists(u):
        s |= {x.strip() for x in open(u) if x.strip()}
    s |= saham_lejar(lejar_dir)
    s = {t.replace('US.', '') for t in s if t and t.replace('.', '').replace('-', '').isalnum()}
    return sorted(s - set(IDX)), IDX


def saham_lejar(lejar_dir=None):
    """Saham posisi Lejar terbuka (lejar/terbuka.csv) dan isyarat menunggu (lejar/tunggu.csv). 7 Nov 2026: bar saham ini
    mesti terus dikemas kini walaupun ia keluar daripada univ.txt, supaya posisi terus ditanda ke pasaran."""
    lj = lejar_dir or os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
    out = set()
    for nm in ('terbuka.csv', 'tunggu.csv'):
        p = os.path.join(lj, nm)
        if not os.path.exists(p):
            continue
        try:
            out |= set(pd.read_csv(p, usecols=['saham'], dtype=str).saham.dropna().str.strip())
        except (ValueError, pd.errors.EmptyDataError):
            continue
    return out


def panjang(df, dividen=None):
    """DataFrame yf.download (lajur MultiIndex (medan, ticker)) -> format panjang LAJ. Jika `dividen` (senarai) diberi dan
    lajur 'Dividends' ada (actions=True), baris dividen > 0 (ticker, date, dividen) ditambah ke senarai itu."""
    if df is None or df.empty:
        return pd.DataFrame(columns=LAJ)
    if not isinstance(df.columns, pd.MultiIndex):
        raise ValueError('jangka lajur MultiIndex (group_by=column)')
    d = df.stack(level=1, future_stack=True).reset_index()
    d.columns = [str(c).lower() for c in d.columns]
    d = d.rename(columns={'level_1': 'ticker', 'date': 'date'})
    d['ticker'] = d['ticker'].map(dari_yahoo)
    d['date'] = pd.to_datetime(d['date']).dt.strftime('%Y%m%d').astype(int)
    if dividen is not None and 'dividends' in d:
        v = pd.to_numeric(d['dividends'], errors='coerce')
        dividen.append(d.loc[v > 0, ['ticker', 'date']].assign(dividen=v[v > 0]))
    return bersih(d[LAJ])


def bersih(d):
    d = d.dropna(subset=['open', 'high', 'low', 'close']).copy()
    h = d[['open', 'high', 'low', 'close']]
    ok = (h > 0).all(axis=1)
    # high/low mesti meliputi open/close (toleransi bundar)
    ok &= d.high >= h[['open', 'close', 'low']].max(axis=1) * (1 - 1e-4)
    ok &= d.low <= h[['open', 'close', 'high']].min(axis=1) * (1 + 1e-4)
    d = d[ok]
    d['volume'] = d['volume'].fillna(0).clip(lower=0).round().astype('int64')
    return d.sort_values(['ticker', 'date']).reset_index(drop=True)


def muat_turun(tickers, period, kumpulan=200, cuba=3, dividen=None):
    """Bar harian mentah (auto_adjust=False). `dividen` (senarai): actions=True dan rekod dividen dikumpul (peristiwa.py)."""
    import yfinance as yf
    out, gagal = [], []
    for i in range(0, len(tickers), kumpulan):
        ks = [ke_yahoo(t) for t in tickers[i:i + kumpulan]]
        for n in range(cuba):
            try:
                df = yf.download(ks, period=period, interval='1d', auto_adjust=False, actions=dividen is not None,
                                 group_by='column', threads=True, progress=False)
                d = panjang(df, dividen)
                break
            except Exception as e:  # had kadar / rangkaian
                if n == cuba - 1:
                    print(f'kumpulan {i}: gagal ({e})', file=sys.stderr); d = pd.DataFrame(columns=LAJ)
                time.sleep(20 * (n + 1))
        out.append(d)
        gagal += [dari_yahoo(k) for k in ks if dari_yahoo(k) not in set(d.ticker)]
        time.sleep(2)
    return (pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=LAJ)), gagal


def sesi_terakhir():
    import exchange_calendars as xc
    c = xc.get_calendar('XNYS')
    now = pd.Timestamp.now(tz='America/New_York')
    d = now.normalize().tz_localize(None)
    if c.is_session(d) and now.hour * 60 + now.minute >= 16 * 60 + 15:
        return int(d.strftime('%Y%m%d'))
    return int(c.date_to_session(d, direction='previous').strftime('%Y%m%d')) if not c.is_session(d) \
        else int(c.previous_session(d).strftime('%Y%m%d'))


def tulis_status(nama, **kv):
    p = os.path.join(HARGA, 'status.json')
    st = json.load(open(p)) if os.path.exists(p) else {}
    st[nama] = dict(dijana=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC'), **kv)
    json.dump(st, open(p, 'w'), ensure_ascii=False, indent=1)


def liputan_sesi(path, sesi):
    """Bilangan ticker dalam fail terkini `path` yang ada bar sesi `sesi` (YYYYMMDD); 0 jika tiada fail."""
    if not os.path.exists(path):
        return 0
    try:
        d = pd.read_csv(path, usecols=['ticker', 'date'])
    except Exception:
        return 0
    return int(d.loc[d.date == sesi, 'ticker'].nunique())


def cmd_terkini(a):
    os.makedirs(HARGA, exist_ok=True)
    saham, idx = universe()
    sesi = sesi_terakhir()
    div = []
    d, gagal = muat_turun(saham + idx, period='1mo', dividen=div)
    d = d[d.date <= sesi].groupby('ticker', group_keys=False).tail(a.hari)
    try:   # dividen untuk jadual faktor (kod/peristiwa.py); kegagalan tidak menghalang harga
        import peristiwa
        n_div = peristiwa.simpan_dividen(pd.concat(div, ignore_index=True) if div else None)
    except Exception as e:
        print(f'dividen: {type(e).__name__}: {e}', file=sys.stderr); n_div = None
    akhir = d.groupby('ticker').date.max()
    lewat = sorted(akhir[akhir < sesi].index)
    if d.ticker.nunique() < 0.5 * (len(saham) + len(idx)):
        print(f'GAGAL: hanya {d.ticker.nunique()} ticker; fail lama dikekalkan', file=sys.stderr); sys.exit(1)
    lama = os.path.join(HARGA, 'terkini.csv')
    n_lama, n_baru = liputan_sesi(lama, sesi), int((akhir == sesi).sum())
    if n_baru < 0.5 * n_lama:
        # Yahoo kerap membuang bar sesi terakhir ~00:00–01:00 UTC (lengkap semula ~05:00): jangan timpa tarikan yang jauh
        # lebih lengkap (status tidak dikemas kini, jadi gerbang data awal lejar.py kekal)
        print(json.dumps(dict(sesi=sesi, dikekalkan=f'terkini.csv lama ada bar sesi bagi {n_lama} ticker; tarikan ini {n_baru}')))
        return
    d.to_csv(lama, index=False, float_format='%.6g')
    tulis_status('terkini', sesi=sesi, bil_ticker=int(d.ticker.nunique()), bil_universe=len(saham) + len(idx),
                 tiada_data=gagal, tiada_bar_sesi=lewat[:200], bil_tiada_bar_sesi=len(lewat), dividen_baharu=n_div)
    print(json.dumps(dict(sesi=sesi, ticker=int(d.ticker.nunique()), gagal=len(gagal), lewat=len(lewat))))


def cmd_sejarah(a):
    p = os.path.join(HARGA, 'perlu_sejarah.txt')
    t = sorted({x.strip().replace('US.', '') for x in open(p) if x.strip()}) if os.path.exists(p) else []
    # ticker kuarantin aktif yang masih tersenarai: sejarah PENUH dimuat turun semula setiap permintaan (didahulukan supaya
    # tidak terpotong oleh --maks) sehingga semak_kuarantin melepaskannya (7 Nov 2026)
    q = KR.perlu_muat_semula()
    t = (q + [x for x in t if x not in set(q)])[:a.maks]
    if not t:
        print('tiada ticker dalam perlu_sejarah.txt'); return
    d, gagal = muat_turun(t, period='3y')
    d = d[d.date <= sesi_terakhir()]   # bar sesi yang belum tutup (larian semasa pasaran) = separa, bukan muktamad
    d = d.groupby('ticker', group_keys=False).tail(SIMPAN_BAR)
    d.to_csv(os.path.join(HARGA, 'sejarah.csv'), index=False, float_format='%.6g')
    tulis_status('sejarah', bil_ticker=int(d.ticker.nunique()), diminta=t, tiada_data=gagal, kuarantin=q)
    if os.path.exists(p):
        os.remove(p)  # permintaan selesai; sejarah.csv kekal sehingga permintaan seterusnya
    print(json.dumps(dict(ticker=int(d.ticker.nunique()), gagal=gagal)))


def gabung_satu(lama, kl, log=None, kr=None):
    """Logik sama dengan kod/stor.py gabung_kline: sejarah lama dilaras hanya jika nisbah bertindih seragam
    (stor.nisbah_laras); keputusan 'laras'/'anomali' ditambah ke senarai log jika diberi.
    'anomali' (7 Nov 2026): bar stor ticker itu DIKEKALKAN sepenuhnya — bar bertindih tidak dipadam/ditimpa dan bar baharu
    tidak ditambah — dan rekod kuarantin (ticker, tarikh_mula = bar baharu pertama, sebab) ditambah ke senarai `kr` jika
    diberi. Dahulu bar bertindih tetap ditimpa: 2026-11-04 bar INDV x 0.7759 masuk ke SUPN walaupun keputusan 'anomali'."""
    if len(lama):
        r, kep, n, serak = nisbah_laras(lama, kl)
        t = str(kl.ticker.iloc[0]) if 'ticker' in kl and len(kl) else ''
        if log is not None and kep in ('laras', 'anomali'):
            log.append(dict(ticker=t, nisbah=round(r, 6), bar=n, serak=round(serak, 6), keputusan=kep, sumber='yfinance'))
        if kep == 'anomali':
            if kr is not None:
                kr.append(dict(ticker=t, tarikh_mula=KR.tarikh_teks(int(kl.date.min())),
                               sebab=f'anomali nisbah_laras: nisbah {r:.6f}, serak {serak:.4f}, {n} bar bertindih '
                                     f'(bar baharu {int(kl.date.min())}..{int(kl.date.max())}); bar stor tidak ditimpa'))
            return lama.copy()
        if kep == 'laras':
            lama = lama.copy()
            for c in ['open', 'high', 'low', 'close']:
                lama[c] = lama[c] * r
            lama['volume'] = (lama['volume'] / r).round()
        lama = lama[~lama.date.isin(kl.date)]
    return pd.concat([lama, kl[LAJ]], ignore_index=True)


# Ambang semakan konsisten (dikalibrasi 7 Nov 2026 atas stor): nisbah tutup INDV/SUPN (dua saham farmasi yang luar biasa
# serupa) atas 40 bar sebelum 2026-10-21 berserak 8.4% (20 bar: 3.6%); 2,000 pasangan saham rawak harga_A atas 40 bar:
# persentil 1 = 11.7%. Data vendor yang sama (stor yfinance lawan muat turun semula) berserak ~0; satu dividen suku tahunan
# biasa dalam 40 bar (~2 bulan) < 2%.
KONSISTEN_BAR = 40        # bar stor DIPERCAYAI terakhir (< tarikh_mula) yang dibanding dengan sejarah segar
KONSISTEN_MIN = 20        # bar bertindih minimum sebelum kuarantin boleh dilepaskan (tetingkap terkini 10 sesi tidak cukup)
SERAK_KONSISTEN = 0.02    # nisbah segar/stor mesti seragam dalam 2%: dividen biasa dalam tetingkap dibenarkan, saham lain tidak
# Sambungan vendor: semakan < tarikh_mula sahaja tidak menolak siri yang DISAMBUNG (sejarah sebenar sebelum tarikh_mula, data
# syarikat lain selepasnya). 7 Nov 2026 terkini.csv yfinance masih menyajikan bar INDV di bawah SUPN bagi akhir Okt (tutup
# 2026-10-26 34.56 = INDV, volum sama). Cap jari pencemaran ini ialah VOLUM harian yang sama dengan ticker lain dalam stor
# pada tarikh yang sama; volum ialah integer besar, jadi >= 3 padanan dengan satu ticker lain bukan kebetulan.
VOLUM_KEMBAR_BAR = 20     # bar segar >= tarikh_mula pertama yang diperiksa
VOLUM_KEMBAR_MIN = 3      # padanan volum minimum dengan SATU ticker lain (dan >= separuh bar diperiksa) = data ticker lain


def volum_kembar(segar, volum_lain, t=None):
    """(ticker lain, padanan, bar bertindih) jika bar segar (>= tarikh_mula) berkongsi volum harian dengan satu ticker lain
    dalam stor pada >= VOLUM_KEMBAR_MIN bar DAN >= separuh bar yang tarikhnya juga ada bagi ticker itu (ticker kembar yang
    sudah delist, cth. INDV selepas 2026-11-02, tidak mencairkan nisbah); selainnya None. volum_lain = indeks_volum(...)."""
    if not volum_lain or not len(segar):
        return None
    s = segar[segar.volume > 0].sort_values('date').head(VOLUM_KEMBAR_BAR)
    tarikh = set(s.date.astype('int64').tolist())
    kira = {}
    for d, v in zip(s.date.astype('int64'), s.volume.round().astype('int64')):
        for x in volum_lain['volum'].get((int(d), int(v)), ()):
            if x != t:
                kira[x] = kira.get(x, 0) + 1
    calon = []
    for x, k in kira.items():
        n = len(tarikh & volum_lain['tarikh'].get(x, set()))
        if k >= VOLUM_KEMBAR_MIN and 2 * k >= n:
            calon.append((k, x, n))
    if not calon:
        return None
    k, x, n = max(calon)
    return x, k, n


def indeks_volum(stor, mula):
    """Rujukan volum_kembar daripada bar stor bertarikh >= mula (int) dengan volum > 0:
    dict(volum={(tarikh, volum): set ticker}, tarikh={ticker: set tarikh})."""
    vol, tkh = {}, {}
    for d in stor.values():
        if not len(d):
            continue
        x = d[(d.date >= mula) & (d.volume > 0)]
        for t, dt, v in zip(x.ticker, x.date.astype('int64'), x.volume.round().astype('int64')):
            vol.setdefault((int(dt), int(v)), set()).add(t)
            tkh.setdefault(t, set()).add(int(dt))
    return dict(volum=vol, tarikh=tkh)


def semak_kuarantin(lama, kl, mula, volum_lain=None):
    """Semakan konsisten bagi ticker kuarantin (7 Nov 2026). lama = bar stor, kl = bar segar (sejarah penuh + terkini),
    mula = tarikh_mula kuarantin, volum_lain = indeks_volum stor (ticker lain). Bar stor < mula = DIPERCAYAI. Lulus jika
    >= KONSISTEN_MIN daripada KONSISTEN_BAR bar dipercayai terakhir ada dalam data segar, nisbah tutup segar/stor seragam
    (serak <= SERAK_KONSISTEN), ada bar segar >= mula, DAN bar segar >= mula bukan data ticker lain (volum_kembar). Pulang
    (bar gabungan, info) jika lulus — bar dipercayai x nisbah median (jika |r - 1| > TOL_LARAS) + bar segar >= mula;
    selainnya (None, info) dan stor tidak diubah."""
    m_i = KR.tarikh_int(mula)
    kl = kl.sort_values('date').drop_duplicates('date', keep='last')
    dipercayai = lama[lama.date < m_i]
    segar = kl[kl.date >= m_i]
    m = dipercayai[['date', 'close']].merge(kl.loc[kl.date < m_i, ['date', 'close']], on='date', suffixes=('_l', '_k'))
    m = m.sort_values('date').tail(KONSISTEN_BAR)
    n = int(len(m))
    if n < KONSISTEN_MIN:
        return None, dict(sebab=f'sejarah segar bertindih {n} bar < {KONSISTEN_MIN} sebelum {KR.tarikh_teks(m_i)}', n=n)
    rr = (m.close_k / m.close_l).astype(float)
    r = float(rr.median())
    serak = float(rr.max() / rr.min() - 1) if rr.min() > 0 else float('inf')
    info = dict(r=r, n=n, serak=serak)
    if serak > SERAK_KONSISTEN:
        return None, dict(info, sebab=f'tidak konsisten: nisbah segar/stor {r:.4f}, serak {serak:.2%} > {SERAK_KONSISTEN:.0%}')
    if not len(segar):
        return None, dict(info, sebab=f'tiada bar segar pada/selepas {KR.tarikh_teks(m_i)}')
    t = str(kl.ticker.iloc[0]) if 'ticker' in kl and len(kl) else None
    vk = volum_kembar(segar, volum_lain, t)
    if vk:
        return None, dict(info, sebab=f'bar segar >= {KR.tarikh_teks(m_i)} berkongsi volum harian dengan {vk[0]} '
                                      f'({vk[1]}/{vk[2]} bar): data ticker lain, bukan sejarah sebenar')
    d = dipercayai.copy()
    if abs(r - 1) > TOL_LARAS:
        for c in ['open', 'high', 'low', 'close']:
            d[c] = d[c].astype(float) * r
        d['volume'] = (d['volume'] / r).round()
    return pd.concat([d[LAJ], segar[LAJ]], ignore_index=True), dict(info, sebab='konsisten')


def gabung(stor, baru, folder=None, kuarantin=None, bursa=None):
    """stor: dict nama->DataFrame (harga_A/B/idx). baru: DataFrame LAJ. Pulang (stor, nota).
    folder (stor pada cakera): peristiwa besar dalam data/harga/faktor.csv digunakan dahulu pada bar lama stor (sekali,
    <folder>/faktor_diguna.csv) dan pada bar baharu mentah, supaya sejarah merentasi tarikh_ex kekal seragam. Baris faktor
    KEMBAR (peristiwa.asing_kembar) tidak digunakan dan sahamnya dikuarantin.
    kuarantin (laluan data/harga/kuarantin.csv; 7 Nov 2026): ticker kuarantin aktif dibekukan sehingga sejarah segarnya lulus
    semak_kuarantin (kemudian dilepaskan); kuarantin baharu (anomali / faktor kembar / peristiwa direktori) ditulis ke fail
    itu. None = tiada fail (keputusan tetap dibuat dan dilapor dalam nota['kuarantin']).
    bursa (laluan data/senarai_bursa/peristiwa.csv): peristiwa tukar_nama/buang bertarikh dalam tetingkap bar baharu ticker
    yang sudah ada bar stor = kuarantin (simbol mungkin kini menyajikan data syarikat lain). None = pengawal ini dimatikan."""
    A = set(stor.get('harga_A.csv', pd.DataFrame(columns=LAJ)).ticker)
    nota = {}; log = []; kr = []; dilepas = []; kekal = {}
    rekod = KR.muat(kuarantin) if kuarantin else pd.DataFrame(columns=KR.LAJUR)
    aktif = KR.aktif(rekod)
    beku = set()
    if folder:
        import peristiwa
        rows, kembar = peristiwa.asing_kembar(peristiwa.muat())
        log += peristiwa.guna_stor(stor, folder, rows)
        _, sudah = peristiwa._diguna(folder)
        baru = peristiwa.laras_baru(baru, rows[[(s, e) in sudah for s, e in zip(rows.saham, rows.tarikh_ex)]] if len(rows) else rows)
        for r in kembar.itertuples():
            if r.saham in aktif or KR.ditangani(rekod, r.saham, r.ditambah or r.tarikh_ex):
                continue
            lain = sorted(set(kembar.saham[(kembar.tarikh_ex == r.tarikh_ex)
                                           & (pd.to_numeric(kembar.faktor).round(6) == round(float(r.faktor), 6))]) - {r.saham})
            kr.append(dict(ticker=r.saham, tarikh_mula=r.tarikh_ex,
                           sebab=f'faktor kembar {r.jenis} {r.tarikh_ex} x{r.faktor} sama dengan {",".join(lain)} '
                                 f'({r.catatan}); faktor tidak digunakan, bar stor tidak ditimpa'))
            beku.add(r.saham)
    ev = KR.peristiwa_bursa(bursa) if bursa else {}
    # rujukan volum stor (sebelum gabungan) bagi semakan sambungan vendor; hanya jika ada kuarantin aktif dalam kelompok ini
    sah_aktif = sorted(set(aktif) & set(baru.ticker))
    volum_lain = indeks_volum(stor, min(KR.tarikh_int(aktif[t]) for t in sah_aktif)) if sah_aktif else None
    for nm in ['harga_A.csv', 'harga_B.csv', 'harga_idx.csv']:
        d = stor.get(nm, pd.DataFrame(columns=LAJ))
        if nm == 'harga_idx.csv':
            pilih = baru[baru.ticker.isin(IDX)]
        elif nm == 'harga_A.csv':
            pilih = baru[baru.ticker.isin(A)]
        else:
            pilih = baru[~baru.ticker.isin(A | set(IDX))]
        if pilih.empty:
            stor[nm] = d; continue
        kump = dict(tuple(d.groupby('ticker'))) if len(d) else {}
        hasil = [g for t, g in kump.items() if t not in set(pilih.ticker)]
        for t, kl in pilih.groupby('ticker'):
            lama = kump.get(t, pd.DataFrame(columns=LAJ))
            if t in aktif:     # kuarantin aktif: lepaskan hanya jika sejarah segar konsisten, selainnya stor beku
                g, info = semak_kuarantin(lama, kl, aktif[t], volum_lain)
                if g is None:
                    hasil.append(lama); kekal[t] = info['sebab']
                else:
                    hasil.append(g)
                    dilepas.append(dict(ticker=t, tarikh_mula=aktif[t], nisbah=round(info['r'], 6), bar=info['n'],
                                        serak=round(info['serak'], 6)))
                continue
            if t in beku:
                hasil.append(lama); continue
            e = KR.peristiwa_dalam(ev.get(t), kl.date.min(), kl.date.max()) if len(lama) else None
            if e and not KR.ditangani(rekod, t, e[0]):
                kr.append(dict(ticker=t, tarikh_mula=KR.tarikh_teks(int(kl.date.min())),
                               sebab=f'direktori Nasdaq {e[1]} {KR.tarikh_teks(e[0])} dalam tetingkap bar baharu '
                                     f'{int(kl.date.min())}..{int(kl.date.max())}; bar stor tidak ditimpa'))
                hasil.append(lama); continue
            hasil.append(gabung_satu(lama, kl, log, kr))
        x = pd.concat(hasil, ignore_index=True).sort_values(['ticker', 'date'])
        stor[nm] = x.drop_duplicates(['ticker', 'date'], keep='last').groupby('ticker', group_keys=False).tail(SIMPAN_BAR)
        nota[nm] = dict(ticker_dikemaskini=int(pilih.ticker.nunique()), bar_terakhir=int(stor[nm].date.max()))
    # rekod kuarantin: satu baris setiap ticker setiap larian (tambah sahaja, idempoten), dan log_laras
    baru_kr, dilihat = [], set()
    for c in kr:
        if c['ticker'] in dilihat or c['ticker'] in aktif:
            continue
        dilihat.add(c['ticker'])
        if kuarantin and not KR.tambah(c['ticker'], c['tarikh_mula'], c['sebab'], kuarantin):
            continue
        baru_kr.append(c)
        log.append(dict(ticker=c['ticker'], nisbah=1.0, bar=0, serak=0.0, keputusan='kuarantin',
                        sumber=f"mula {c['tarikh_mula']}: {c['sebab']}"))
    for x in dilepas:
        sebab = (f"sejarah segar konsisten dengan bar stor dipercayai (< {x['tarikh_mula']}): nisbah {x['nisbah']:g}, "
                 f"serak {x['serak']:.4f}, {x['bar']} bar; bar >= {x['tarikh_mula']} diganti")
        if kuarantin:
            KR.lepas(x['ticker'], sebab, kuarantin)
        log.append(dict(ticker=x['ticker'], nisbah=x['nisbah'], bar=x['bar'], serak=x['serak'], keputusan='lepas',
                        sumber=f"kuarantin {x['tarikh_mula']}: {sebab}"))
    nota['log_laras'] = log
    nota['kuarantin'] = dict(baru=[[c['ticker'], c['tarikh_mula'], c['sebab']] for c in baru_kr],
                             dilepaskan=[[x['ticker'], x['tarikh_mula']] for x in dilepas], kekal_beku=kekal)
    return stor, nota


def cmd_gabung(a):
    fail = a.fail or [os.path.join(HARGA, 'terkini.csv')]
    baru = pd.concat([pd.read_csv(f) for f in fail if os.path.exists(f)], ignore_index=True)
    stor = {nm: pd.read_csv(os.path.join(a.stor, nm)) for nm in ['harga_A.csv', 'harga_B.csv', 'harga_idx.csv']
            if os.path.exists(os.path.join(a.stor, nm))}
    kr = a.kuarantin or (KR.FAIL if os.path.realpath(a.stor) == os.path.realpath(os.path.join(HARGA, 'stor'))
                         else os.path.join(a.stor, 'kuarantin.csv'))
    stor, nota = gabung(stor, baru, a.stor, kuarantin=kr, bursa=KR.PERISTIWA_BURSA)
    for nm, d in stor.items():
        d[LAJ].to_csv(os.path.join(a.stor, nm), index=False, float_format='%.6g')
    from stor import tulis_log_laras
    nota['log_laras'] = tulis_log_laras(a.stor, nota.pop('log_laras'))
    print(json.dumps(nota, indent=1))


def banding(yf_d, mm_d):
    """Pulang DataFrame beza relatif (open/high/low/close) bagi tarikh yang sama."""
    m = yf_d.merge(mm_d, on='date', suffixes=('_yf', '_mm'))
    for c in ['open', 'high', 'low', 'close']:
        m[c] = (m[c + '_yf'] / m[c + '_mm'] - 1).abs()
    return m[['date', 'open', 'high', 'low', 'close']]


def cmd_semak(a):
    d = pd.concat([pd.read_csv(os.path.join(HARGA, f)) for f in ('terkini.csv',) if os.path.exists(os.path.join(HARGA, f))])
    buruk = []
    for spec in a.kline:
        t, path = spec.split('=', 1)
        mm = baca_kline(path); mm['date'] = pd.to_datetime(mm['date']).dt.strftime('%Y%m%d').astype(int)
        b = banding(d[d.ticker == t], mm)
        mx = float(b[['open', 'high', 'low', 'close']].max().max()) if len(b) else None
        print(f'{t}: {len(b)} tarikh sama, beza maks {mx:.4%}' if mx is not None else f'{t}: tiada tarikh sama')
        if mx is None or mx > TOLERANSI:
            buruk.append(t)
    if buruk:
        print('BERBEZA (guna Moomoo):', ' '.join(buruk)); sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest='cmd', required=True)
    x = s.add_parser('terkini'); x.add_argument('--hari', type=int, default=10); x.set_defaults(f=cmd_terkini)
    x = s.add_parser('sejarah'); x.add_argument('--maks', type=int, default=300); x.set_defaults(f=cmd_sejarah)
    x = s.add_parser('gabung'); x.add_argument('--stor', required=True); x.add_argument('--fail', nargs='*')
    x.add_argument('--kuarantin', help='laluan kuarantin.csv (lalai: data/harga/kuarantin.csv bagi stor repo, '
                                      'selainnya <stor>/kuarantin.csv)')
    x.set_defaults(f=cmd_gabung)
    x = s.add_parser('semak'); x.add_argument('--kline', nargs='+', required=True); x.set_defaults(f=cmd_semak)
    a = p.parse_args(); a.f(a)


if __name__ == '__main__':
    main()
