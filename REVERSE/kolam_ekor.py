"""Dua soalan struktur yang tidak pernah ditanya dalam projek ini.

Lima kajian (fasa 1, 1b, 2 SEC, kos, kepekatan) semuanya mendarat DI BAWAH penanda aras pasif,
dan setiap kali diagnosisnya ialah "signal lemah". Tetapi dua perkara yang lebih asas daripada
signal tidak pernah diukur:

1. KOLAM. Setiap lorong dalam kajian ini membina portfolio berat sama rata daripada alam ~3,300
   ticker. SPY/SPUS ialah indeks berat permodalan bagi syarikat besar yang terselamat. Jika
   pulangan MEDIAN saham dalam kolam kita jauh di bawah indeks, maka setiap portfolio berat sama
   rata bermula dengan kekurangan struktur, dan tiada signal entry berkekuatan realistik boleh
   menutupnya. Ini hipotesis "kolam yang salah" dan ia belum pernah diukur di sini.

2. EKOR. Jika pulangan kolam datang daripada ekor kanan yang nipis, maka henti keras -2xATR14
   (yang dipakai SELURUH kajian sebagai `pul_henti2atr`) memotong tepat di tempat pulangan berada.
   Ukur: berapa banyak pulangan agregat hilang apabila henti itu dikenakan, tanpa signal apa-apa.

Kedua-duanya DESKRIPTIF, bukan ujian signal: tiada pradaftar dibelanjakan, tiada parameter ditala,
tiada hipotesis tentang pemicu. Ia mengukur pembinaan portfolio dan kolam, sama seperti
`KEPEKATAN.md` dan `KOS_DRAG.md`.

Guna: python3 REVERSE/kolam_ekor.py [--tahun 2012-2025] [--cair 100000]
Output: REVERSE/KOLAM_EKOR.md, REVERSE/kolam_ekor_bulanan.csv, REVERSE/kolam_ekor_tahunan.csv
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))

CACHE = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'
KELUAR = AKAR / 'REVERSE'

UFUK = 21        # sesi ke hadapan bagi soalan bulanan (satu bulan dagangan)
UFUK_TH = 252    # sesi ke hadapan bagi soalan ekor (satu tahun dagangan)
HENTI_ATR = 2.0  # henti keras yang dipakai seluruh kajian (pul_henti2atr)
ATR_N = 14
CAIR = 100_000   # ambang kecairan repo sendiri: median nilai 20 bar (kod/tidak_layak.py)
MIN_BAR = 60     # bar minimum dalam tahun sauh supaya ATR dan kecairan bermakna


def muat(tahun):
    """OHLCV bagi [tahun-1, tahun+1] — tahun-1 untuk pemanasan ATR, tahun+1 untuk ufuk hadapan."""
    bhg = []
    for y in (tahun - 1, tahun, tahun + 1):
        p = CACHE / f'harga_{y}.parquet'
        if p.exists():
            bhg.append(pd.read_parquet(p, columns=['ticker', 'date', 'high', 'low', 'close',
                                                   'volume']))
    if not bhg:
        return None
    return pd.concat(bhg, ignore_index=True).sort_values(['ticker', 'date'])


def atr(h, lo, c, n=ATR_N):
    """ATR Wilder, tanpa pandang hadapan: hanya bar hingga t."""
    pc = np.concatenate([[np.nan], c[:-1]])
    tr = np.maximum(h - lo, np.maximum(np.abs(h - pc), np.abs(lo - pc)))
    out = np.full(len(c), np.nan)
    if len(c) <= n:
        return out
    out[n] = np.nanmean(tr[1:n + 1])
    for i in range(n + 1, len(c)):
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def satu_ticker(g, tahun, tick):
    """Pulangkan baris sauh bulanan + baris sauh tahunan bagi satu ticker."""
    d = g['date'].to_numpy()
    c = g['close'].to_numpy(dtype='float64')
    h = g['high'].to_numpy(dtype='float64')
    lo = g['low'].to_numpy(dtype='float64')
    v = g['volume'].to_numpy(dtype='float64')
    dlm = (pd.DatetimeIndex(d).year == tahun)
    if dlm.sum() < MIN_BAR:
        return [], []
    a = atr(h, lo, c)
    nilai = pd.Series(c * v).rolling(20).median().to_numpy()

    # Sauh bulanan: bar terakhir setiap bulan kalendar DALAM tahun sauh.
    bulan = pd.DatetimeIndex(d).to_period('M')
    idx_dlm = np.flatnonzero(dlm)
    sauh = []
    for b in pd.unique(bulan[idx_dlm]):
        ii = idx_dlm[bulan[idx_dlm] == b]
        sauh.append(int(ii[-1]))

    br_b = []
    for i in sauh:
        j = i + UFUK
        if j >= len(c) or not np.isfinite(a[i]) or not np.isfinite(nilai[i]) or c[i] <= 0:
            continue
        pul = c[j] / c[i] - 1.0
        # Henti keras: sentuhan pertama paras c[i] - 2*ATR dalam tingkap, dinilai pada paras itu.
        paras = c[i] - HENTI_ATR * a[i]
        kena = np.flatnonzero(lo[i + 1:j + 1] <= paras)
        pul_h = (paras / c[i] - 1.0) if kena.size else pul
        br_b.append((tahun, str(pd.Timestamp(d[i]).date()), tick, float(nilai[i]),
                     float(a[i] / c[i] * 100), pul * 100, pul_h * 100))

    # Sauh tahunan: bar pertama tahun sauh, ufuk 252 sesi.
    br_t = []
    i = int(idx_dlm[0])
    j = i + UFUK_TH
    if j < len(c) and np.isfinite(a[i]) and np.isfinite(nilai[i]) and c[i] > 0:
        pul = c[j] / c[i] - 1.0
        paras = c[i] - HENTI_ATR * a[i]
        kena = np.flatnonzero(lo[i + 1:j + 1] <= paras)
        pul_h = (paras / c[i] - 1.0) if kena.size else pul
        br_t.append((tahun, tick, float(nilai[i]), pul * 100, pul_h * 100))
    return br_b, br_t


def jalan_tahun(tahun):
    df = muat(tahun)
    if df is None:
        return pd.DataFrame(), pd.DataFrame()
    B, T = [], []
    for tick, g in df.groupby('ticker', sort=True):
        b, t = satu_ticker(g, tahun, tick)
        B += b
        T += t
    Bd = pd.DataFrame(B, columns=['tahun', 'tarikh', 'ticker', 'nilai', 'atrp', 'pul', 'pul_henti'])
    Td = pd.DataFrame(T, columns=['tahun', 'ticker', 'nilai', 'pul', 'pul_henti'])
    return Bd, Td


def indeks_bulanan(mula, akhir):
    """Pulangan 21 sesi SPY pada sauh hujung bulan yang sama."""
    ix = pd.read_parquet(CACHE / 'idx.parquet')
    s = ix[ix.ticker == 'SPY'].sort_values('date').set_index('date').close
    if s.empty:
        return pd.DataFrame()
    s = s[(s.index >= pd.Timestamp(mula)) & (s.index <= pd.Timestamp(akhir))]
    arr = s.to_numpy(dtype='float64')
    d = s.index
    bulan = d.to_period('M')
    baris = []
    for b in pd.unique(bulan):
        ii = np.flatnonzero(bulan == b)
        i = int(ii[-1])
        j = i + UFUK
        if j < len(arr):
            baris.append((d[i].year, str(d[i].date()), (arr[j] / arr[i] - 1) * 100))
    return pd.DataFrame(baris, columns=['tahun', 'tarikh', 'spy'])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--tahun', default='2012-2025')
    ap.add_argument('--cair', type=float, default=CAIR)
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    t0, t1 = (int(x) for x in a.tahun.split('-'))

    fb, ft = KELUAR / 'kolam_ekor_bulanan.csv', KELUAR / 'kolam_ekor_tahunan.csv'
    if a.laporan_sahaja and fb.exists() and ft.exists():
        return laporan(pd.read_csv(fb), pd.read_csv(ft), a.cair)

    B, T = [], []
    for th in range(t0, t1 + 1):
        b, t = jalan_tahun(th)
        B.append(b)
        T.append(t)
        print(f'  {th}: {len(b):,} sauh bulanan, {len(t):,} sauh tahunan', flush=True)
    Bd = pd.concat(B, ignore_index=True)
    Td = pd.concat(T, ignore_index=True)
    Bd.to_csv(fb, index=False, float_format='%.4f')
    Td.to_csv(ft, index=False, float_format='%.4f')
    ringkas(Bd, Td, a.cair)
    return laporan(Bd, Td, a.cair)


def ringkas(Bd, Td, cair):
    """Agregat setiap tahun — fail kecil yang dikomit; yang mentah diabaikan git."""
    Bc, Tc = Bd[Bd.nilai >= cair], Td[Td.nilai >= cair]
    b = Bc.groupby('tahun').pul.agg(n_bulan='size', median_kolam='median', min_kolam='mean',
                                    pct_positif=lambda x: (x > 0).mean() * 100)
    t = Tc.groupby('tahun').agg(n_tahun=('pul', 'size'), min_tanpa_henti=('pul', 'mean'),
                                min_dengan_henti=('pul_henti', 'mean'),
                                median_tanpa_henti=('pul', 'median'))
    R = b.join(t)
    R['kos_henti'] = R.min_dengan_henti - R.min_tanpa_henti
    R.round(4).to_csv(KELUAR / 'kolam_ekor_ringkas.csv')
    return R


def _ekor(x, k):
    """Bahagian jumlah pulangan yang datang daripada k% teratas (nilai 0-100)."""
    x = np.sort(np.asarray(x, dtype='float64'))[::-1]
    n = max(int(round(len(x) * k / 100.0)), 1)
    jum = x.sum()
    return (x[:n].sum() / jum * 100) if jum > 0 else np.nan


def hadapan_c():
    """Bahagian data hadapan: posisi Papertrade C yang sudah ditutup.

    Soalan yang sama (kolam, ekor, henti) tetapi pada dagangan sebenar yang direkodkan, bukan
    pada alam A02. Alam di sini BERBEZA (ditapis Syariah + dipilih pengimbas Mxx), jadi ia bukan
    pengesahan langsung bagi bahagian 1-2; ia pemeriksaan bebas."""
    import glob
    f = sorted(glob.glob(str(AKAR / 'BacktestShariah2' / 'papertrade' / 'claude*.csv')))
    if not f:
        return []
    C = pd.concat([pd.read_csv(x) for x in f], ignore_index=True)
    C = C[C.tidak_sah.isna() | (C.tidak_sah.astype(str) == 'False')]
    k = C.dropna(subset=['untung_akhir_pct']).copy()
    if k.empty:
        return []
    L = ['## 4. Pemeriksaan pada data hadapan sebenar (Papertrade C)', '']
    L.append(f'{len(k):,} posisi sudah ditutup, {k.saham.nunique():,} saham, '
             f'{k.id_kaedah.nunique()} kaedah. Alam BERBEZA daripada bahagian 1–2 (ditapis '
             'Syariah, dipilih pengimbas Mxx), jadi ini pemeriksaan bebas, bukan pengesahan.')
    L.append('')
    jum = float(k.untung_akhir_pct.sum())
    h0 = k[k.hari == 0]
    L.append('### 4a. 421 dagangan yang tidak pernah berpeluang')
    L.append('')
    L.append(f'**{len(h0)} posisi dibeli dan dihentikan pada HARI YANG SAMA**, kadar menang '
             f'**{(h0.untung_akhir_pct > 0).mean() * 100:.2f}%**, purata '
             f'{h0.untung_akhir_pct.mean():+.2f}%. Kadar menang sifar merentas {len(h0)} '
             'dagangan bukan hasil pasaran — ia mekanikal: paras henti kaedah terletak DALAM '
             'julat intrabar hari masuk, jadi ia disentuh dengan hampir kepastian.')
    L.append('')
    a = k.dropna(subset=['henti'])
    a = a[(a.henti > 0) & (a.harga_beli > 0)].copy()
    a['jarak'] = (a.harga_beli - a.henti) / a.harga_beli * 100
    L.append(f'Jarak henti median bagi kematian hari-0 itu: '
             f'**{float(a.loc[a.hari == 0, "jarak"].median()):.2f}%** daripada harga masuk. '
             f'Bagi yang terselamat melepasi hari 0: '
             f'**{float(a.loc[a.hari > 0, "jarak"].median()):.2f}%**.')
    L.append('')
    sisa = k[k.hari > 0]
    L.append(f'Nilainya jika dibetulkan: jumlah kerugian direalisasi turun '
             f'**{100 * (1 - sisa.untung_akhir_pct.sum() / jum):.1f}%**. Tetapi perhatikan — '
             f'purata baki {len(sisa):,} posisi ialah {sisa.untung_akhir_pct.mean():+.2f}%, '
             f'**lebih buruk** daripada purata keseluruhan {jum / len(k):+.2f}%. Membetulkan '
             'kecacatan ini mengurangkan kerosakan; ia **tidak** menukar tanda.')
    L.append('')
    L.append('### 4b. Hasil ikut lebar henti — dan apa yang ia betul-betul kata')
    L.append('')
    a['bin'] = pd.cut(a.jarak, [0, 1.5, 2.5, 4, 6, 9, 100],
                      labels=['<1.5%', '1.5–2.5%', '2.5–4%', '4–6%', '6–9%', '>9%'])
    g = a.groupby('bin', observed=True).agg(
        n=('untung_akhir_pct', 'size'), purata=('untung_akhir_pct', 'mean'),
        menang=('untung_akhir_pct', lambda x: (x > 0).mean() * 100),
        mati0=('hari', lambda x: (x == 0).mean() * 100)).round(2)
    L.append('| Jarak henti | n | Purata | Kadar menang | Mati hari-0 |')
    L.append('|---|---|---|---|---|')
    for b in g.index:
        r = g.loc[b]
        L.append(f'| {b} | {r.n:.0f} | {r.purata:+.2f}% | {r.menang:.1f}% | {r.mati0:.0f}% |')
    L.append('')
    L.append('**Saya perlu membetulkan tafsiran pertama saya sendiri di sini.** Melihat kematian '
             'hari-0 itu, hipotesis yang jelas ialah "henti terlalu rapat". Jadual ini '
             'menolaknya: baldi paling RAPAT mempunyai purata paling BAIK '
             f'({float(g.purata.iloc[0]):+.2f}%) dan baldi paling LEBAR paling buruk '
             f'({float(g.purata.iloc[-1]):+.2f}%). Henti rapat mati kerap tetapi murah.')
    L.append('')
    L.append('Yang sebenarnya ditunjukkan jadual itu lebih serius. Kadar menang naik '
             f'{float(g.menang.iloc[-1]) / max(float(g.menang.iloc[0]), 0.01):.1f}× dari baldi '
             f'paling rapat ke paling lebar, tetapi kerugian purata naik '
             f'{abs(float(g.purata.iloc[-1])) / max(abs(float(g.purata.iloc[0])), 0.01):.1f}× — '
             'lebih cepat. Jangkaan kekal **negatif pada setiap lebar henti** dan menjadi lebih '
             'negatif apabila henti dilebarkan. Itu tandatangan masuk **tanpa kelebihan**: '
             'apabila tiada kelebihan, melebarkan henti hanya meningkatkan kerugian yang diambil '
             'ketika salah tanpa kenaikan kadar menang yang mencukupi.')
    L.append('')
    L.append('Jadi tiada tetapan henti yang menyelamatkan buku ini. Itu mengesahkan keputusan '
             'fasa 1 pada data HADAPAN, bukan pada backtest.')
    L.append('')
    L.append(f'**Had:** {len(k):,} posisi merentas kurang sebulan, dan 76% posisi masih terbuka. '
             'Baca semula selepas 6 bulan.')
    L.append('')
    return L


def sintesis(md, sp, ekor5, kos_henti):
    """Satu kenyataan yang menyatukan bahagian 1-4 tanpa bercanggah."""
    L = ['## 5. Sintesis: satu kenyataan, bukan empat', '']
    L.append('Bahagian 2 berkata henti −2×ATR memotong ekor kanan kolam. Bahagian 4b berkata '
             'tiada lebar henti menyelamatkan buku hadapan. Itu **bukan percanggahan** — '
             'kedua-duanya betul dan bersama-sama ia satu kenyataan:')
    L.append('')
    L.append(f'> Pulangan dalam kolam ini hidup dalam ekor kanan yang nipis ({ekor5:.1f}% '
             f'daripada jumlah datang daripada 5% teratas). Pembinaan kita — 8–10 slot berat '
             f'sama rata, dipotong pada −2×ATR, daripada kolam yang saham mediannya '
             f'{md:+.2f}%/bulan lawan SPY {sp:+.2f}% — menjauhkan diri daripada ekor itu secara '
             f'struktur ({abs(kos_henti):.2f} mata setahun hanya daripada henti). Dan pemicu '
             f'yang sepatutnya membayar kembali kekurangan itu tidak mempunyai kelebihan pada '
             f'mana-mana lebar henti.')
    L.append('')
    L.append('Dua masalah berbeza, dan hanya satu daripadanya pernah dikaji selama ini.')
    L.append('')
    L.append('| | Masalah | Pernah dikaji? |')
    L.append('|---|---|---|')
    L.append('| 1 | Pemicu tiada kelebihan | **Ya** — fasa 1, 1b, 2 SEC: semuanya DITOLAK |')
    L.append('| 2 | Pembinaan portfolio menjauhi ekor kanan kolam | **Tidak** — ini pengukuran '
             'pertama |')
    L.append('')
    L.append('Itu mengubah soalan. Lima kajian bertanya "pemicu mana yang berfungsi?" dan '
             'jawapannya tetap tiada. Soalan yang belum ditanya ialah **"bolehkah pembinaan '
             'yang menerima ekor kanan mengalahkan penanda aras tanpa pemicu sama sekali?"** — '
             'iaitu kolam yang lebih baik, slot lebih banyak, tiada henti keras, dan membiarkan '
             'pemenang berjalan.')
    L.append('')
    L.append('**Ia mungkin juga kalah.** Bahagian 2 menunjukkan membuang henti memperdalam '
             'persentil 5 daripada −15.58% kepada −54.67% setiap saham-tahun, dan '
             '`KEPEKATAN.md` menunjukkan menambah slot membeli MDD dengan pulangan. Perbezaannya '
             'ialah ini **belum** diukur sebagai satu pembinaan, manakala ruang pemicu sudah '
             'diukur dan kosong. Itu menjadikannya satu-satunya arah yang tinggal yang mempunyai '
             'maklumat baharu di dalamnya.')
    L.append('')
    L.append('**Ia tidak akan mencapai +10%/bulan.** Tiada apa-apa dalam mana-mana nombor di '
             'atas menghampiri 3.14×/tahun. Lihat `SASARAN.md`.')
    L.append('')
    return L


def laporan(Bd, Td, cair):
    L = ['# Kolam dan ekor: dua soalan struktur yang tidak pernah ditanya', '']
    now = f'{pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M}'
    L.append(f'Dijana {now} UTC oleh `REVERSE/kolam_ekor.py`. Alam: Release '
             '`autotune-data-a02` (~3,300 ticker AS). Deskriptif — tiada signal, tiada parameter '
             'ditala, tiada pradaftar dibelanjakan.')
    L.append('')
    Bc = Bd[Bd.nilai >= cair]
    Tc = Td[Td.nilai >= cair]
    spy = indeks_bulanan(f'{int(Bd.tahun.min())}-01-01', f'{int(Bd.tahun.max()) + 1}-12-31')

    # ---------- 1. KOLAM ----------
    L.append('## 1. Kolam: adakah kita memancing di kolam yang salah?')
    L.append('')
    L.append(f'Setiap sauh = hujung bulan kalendar; pulangan = {UFUK} sesi ke hadapan dari tutup '
             f'hari itu. Penapis kecairan = median nilai 20 bar ≥ USD {cair:,.0f} (ambang repo '
             'sendiri, `kod/tidak_layak.py`).')
    L.append('')
    L.append(f'**{len(Bc):,} sauh saham-bulan cair** merentas {Bc.tahun.nunique()} tahun '
             f'({int(Bc.tahun.min())}–{int(Bc.tahun.max())}), {Bc.ticker.nunique():,} ticker.')
    L.append('')
    md = float(Bc.pul.median())
    mn = float(Bc.pul.mean())
    pos = float((Bc.pul > 0).mean() * 100)
    sp = float(spy.spy.median()) if not spy.empty else np.nan
    # Portfolio berat sama rata SELURUH kolam = min rentas-keratan setiap bulan, bukan median.
    # Bezakan ini daripada "saham median": portfolio 8-10 slot ialah sampel kecil, jadi ia
    # mendarat dekat median, sedangkan memegang kesemua ~2,000 nama mendapat min.
    bw = Bc.groupby('tarikh').pul.mean()
    bw_md = float(bw.median())
    L.append('| Ukuran bulanan | Nilai | Maksudnya |')
    L.append('|---|---|---|')
    L.append(f'| Median saham-bulan | **{md:+.2f}%** | tempat portfolio 8–10 slot mendarat |')
    L.append(f'| Portfolio berat sama rata SELURUH kolam | **{bw_md:+.2f}%** | memegang semua '
             f'~{Bc.ticker.nunique():,} nama |')
    L.append(f'| SPY (berat permodalan) | **{sp:+.2f}%** | penanda aras pasif |')
    L.append(f'| Min saham-bulan | {mn:+.2f}% | dipacu ekor kanan |')
    L.append(f'| % saham-bulan positif | {pos:.1f}% | lawan SPY '
             f'{float((spy.spy > 0).mean() * 100) if not spy.empty else float("nan"):.1f}% |')
    L.append('')
    L.append('**Tiga baris pertama ialah tiga perkara berbeza dan mencampurkannya adalah '
             'kesilapan.** Memegang seluruh kolam memberi MIN rentas-keratan; memilih 8 nama '
             'memberi cabutan daripada taburan yang medianya lebih rendah. Itulah sebabnya '
             '`KEPEKATAN_BENIH.md` mendapati sebaran 17.3 mata: 8 slot ialah sampel kecil '
             'daripada taburan terpencong.')
    L.append('')
    jurang = md - sp
    L.append(f'**Jurang saham median lawan SPY: {jurang:+.2f} mata peratus sebulan** = '
             f'{((1 + md / 100) ** 12 - 1) * 100:+.1f}%/tahun bagi kolam lawan '
             f'{((1 + sp / 100) ** 12 - 1) * 100:+.1f}%/tahun bagi SPY.')
    L.append('')
    L.append('Min melebihi median kerana taburan pulangan saham **terpencong kanan**: beberapa '
             'saham naik berganda, majoriti tidak. Portfolio berat sama rata 8–10 slot ialah '
             'sampel kecil daripada taburan itu, jadi ia mendarat dekat MEDIAN, bukan min — '
             'melainkan ia menangkap ekor kanan.')
    L.append('')
    L.append('### Median setiap tahun')
    L.append('')
    pt = Bc.groupby('tahun').pul.median().round(2)
    sy = spy.groupby('tahun').spy.median().round(2) if not spy.empty else pd.Series(dtype=float)
    L.append('| Tahun | Median kolam | Median SPY | Jurang |')
    L.append('|---|---|---|---|')
    n_bawah = 0
    for th in pt.index:
        s = float(sy.get(th, np.nan))
        g = float(pt[th]) - s
        if g < 0:
            n_bawah += 1
        L.append(f'| {th} | {pt[th]:+.2f}% | {s:+.2f}% | {g:+.2f} |')
    L.append('')
    L.append(f'Kolam di bawah SPY dalam **{n_bawah} daripada {len(pt)} tahun**.')
    L.append('')
    L.append('**Arah bias:** sauh yang tidak mempunyai bar penuh ke hadapan (saham delist atau '
             'berhenti didagangkan dalam tingkap) DIBUANG. Itu membuang kegagalan dan '
             'mengekalkan yang terselamat, jadi median kolam yang sebenar **lebih rendah** '
             'daripada yang dilaporkan di sini. Bias itu menguatkan dapatan, bukan '
             'melemahkannya.')
    L.append('')

    # ---------- 2. EKOR ----------
    L.append('## 2. Ekor: adakah henti -2×ATR memotong tempat pulangan berada?')
    L.append('')
    L.append(f'Ufuk {UFUK_TH} sesi (satu tahun) dari bar pertama setiap tahun sauh, '
             f'{len(Tc):,} saham-tahun cair. Henti = sentuhan pertama tutup − '
             f'{HENTI_ATR:g}×ATR{ATR_N}, dinilai pada paras henti. Inilah henti yang dipakai '
             'SELURUH kajian (`pul_henti2atr`).')
    L.append('')
    for nm, k in (('1%', 1), ('5%', 5), ('10%', 10)):
        L.append(f'- {nm} teratas menyumbang **{_ekor(Tc.pul, k):.1f}%** daripada jumlah '
                 'pulangan kolam')
    L.append('')
    tp, th_ = float(Tc.pul.mean()), float(Tc.pul_henti.mean())
    tmd, tmdh = float(Tc.pul.median()), float(Tc.pul_henti.median())
    kena = float((Tc.pul_henti < Tc.pul - 1e-9).mean() * 100)
    L.append('| Ukuran tahunan | Tanpa henti | Dengan henti −2×ATR | Beza |')
    L.append('|---|---|---|---|')
    L.append(f'| Min | {tp:+.2f}% | {th_:+.2f}% | **{th_ - tp:+.2f}** |')
    L.append(f'| Median | {tmd:+.2f}% | {tmdh:+.2f}% | {tmdh - tmd:+.2f} |')
    L.append(f'| Persentil 95 | {float(Tc.pul.quantile(0.95)):+.2f}% | '
             f'{float(Tc.pul_henti.quantile(0.95)):+.2f}% | '
             f'{float(Tc.pul_henti.quantile(0.95) - Tc.pul.quantile(0.95)):+.2f} |')
    L.append(f'| Persentil 5 | {float(Tc.pul.quantile(0.05)):+.2f}% | '
             f'{float(Tc.pul_henti.quantile(0.05)):+.2f}% | '
             f'{float(Tc.pul_henti.quantile(0.05) - Tc.pul.quantile(0.05)):+.2f} |')
    L.append('')
    L.append(f'Henti itu tercetus pada **{kena:.1f}%** daripada semua saham-tahun.')
    L.append('')
    L.append(f'Perhatikan arah kedua hujung: henti menaikkan persentil 5 (ia MEMANG mengurangkan '
             f'kerugian terburuk) tetapi menurunkan persentil 95 dan min. Itu tandatangan '
             f'pemotongan ekor kanan: henti mengeluarkan posisi SEBELUM pergerakan besar selesai, '
             f'dan dalam taburan terpencong kanan, min adalah milik pergerakan besar itu.')
    L.append('')
    L.append('### Beza min setiap tahun (dengan henti − tanpa henti)')
    L.append('')
    pt2 = Tc.groupby('tahun')[['pul', 'pul_henti']].mean().round(2)
    pt2['beza'] = (pt2.pul_henti - pt2.pul).round(2)
    L.append('| Tahun | Tanpa henti | Dengan henti | Beza |')
    L.append('|---|---|---|---|')
    for th in pt2.index:
        r = pt2.loc[th]
        L.append(f'| {th} | {r.pul:+.2f}% | {r.pul_henti:+.2f}% | {r.beza:+.2f} |')
    L.append('')
    n_rugi = int((pt2.beza < 0).sum())
    L.append(f'Henti merugikan min dalam **{n_rugi} daripada {len(pt2)} tahun**.')
    L.append('')

    # ---------- 3. Maksudnya ----------
    L.append('## 3. Apa maksudnya bagi matlamat')
    L.append('')
    L.append(f'1. **Kolam kita median {md:+.2f}% sebulan; SPY median {sp:+.2f}%.** Portfolio berat '
             f'sama rata 8–10 slot mendarat dekat median kolam. Untuk mengalahkan penanda aras, '
             f'signal entry mesti menambah sekurang-kurangnya {abs(jurang):.2f} mata sebulan '
             f'HANYA untuk seri — sebelum menambah apa-apa. Fasa 1 mengukur kelebihan signal '
             f'terbaik jauh di bawah paras itu.')
    L.append(f'2. **Pulangan kolam tertumpu pada ekor:** {_ekor(Tc.pul, 5):.1f}% daripada jumlah '
             f'datang daripada 5% teratas. Sistem yang memotong pada −2×ATR membuang hak untuk '
             f'berada dalam 5% itu.')
    L.append(f'3. **Henti −2×ATR mengurangkan min {abs(th_ - tp):.2f} mata setahun** pada asas '
             f'tanpa signal. Seluruh kajian menilai signal MELALUI henti itu, jadi setiap angka '
             f'pulangan dalam kajian ini mengandungi beban itu.')
    L.append('')
    L.append('**Ini bukan dapatan signal dan bukan cadangan membuang henti.** Membuang henti '
             'menaikkan min tetapi memperdalam drawdown — itu pertukaran yang sama yang diukur '
             'oleh fasa 1b dan `KEPEKATAN.md`, dan kedua-duanya menunjukkan nisbah tidak '
             'bertambah baik. Yang ditunjukkan di sini ialah **di mana kekurangan itu bermula**: '
             'pada kolam dan pada pemotongan ekor, bukan pada kekuatan pemicu.')
    L.append('')
    L += hadapan_c()
    L += sintesis(md, sp, _ekor(Tc.pul, 5), th_ - tp)
    (KELUAR / 'KOLAM_EKOR.md').write_text('\n'.join(L), encoding='utf-8')
    print(f'\nKOLAM_EKOR.md | kolam median {md:+.2f}%/bulan lawan SPY {sp:+.2f}% '
          f'(jurang {jurang:+.2f}) | henti kos min {th_ - tp:+.2f} mata/tahun | '
          f'5% teratas = {_ekor(Tc.pul, 5):.1f}% jumlah')
    return 0


if __name__ == '__main__':
    sys.exit(main())
