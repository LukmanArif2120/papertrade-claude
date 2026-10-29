"""Setup gaya pedagang: jalur tengah + urutan + 3 syarat — pradaftar `REVERSE/SPEC_SETUP.md`.

Permintaan pengguna 29 Okt 2026. BUKAN ulangan fasa 1:
  - fasa 1 guna kuintil q1/q5 (hujung melampau); ini guna jalur TENGAH (RSI 45-60)
  - fasa 1 uji syarat SERENTAK; ini uji URUTAN (hari_macd_cross, hari_gc)
  - fasa 1 uji 2 syarat; ini uji 3 (pemicu + jalur + penapis)
  - fasa 1 nilai 10,637 peristiwa sah/tahun; ini nilai 367,632 bar/tahun

Pemilihan dikawal oleh pecahan masa: LATIH 2012-2019 memilih 10 teratas daripada 672; TAHAN
2020-2025 menguji HANYA 10 itu. Keluarga ujian tahan ialah 10, bukan 672.

Guna: python3 REVERSE/step15_setup.py [--laporan-sahaja]
Output: REVERSE/SETUP.md, REVERSE/setup_latih.csv, REVERSE/setup_tahan.csv
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import kos as K  # noqa: E402
from REVERSE.teras import stat as ST  # noqa: E402

KELUAR = AKAR / 'REVERSE'
CACHE = KELUAR / '.cache'
HARGA = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'
PUL = CACHE / 'pul_setup.parquet'

TH0, TH1 = 2012, 2025
LATIH = (2012, 2019)
TAHAN = (2020, 2025)
UFUK = 63          # E63 / E63S
HENTI_ATR = 2.0    # E63S
TRAIL_ATR = 4.0    # ETRAIL (Chandelier)
TRAIL_MAKS = 126   # had imbasan ETRAIL (6 bulan); didokumen dalam laporan
ATR_N = 14
MIN_N_LATIH = 500  # spec §4
N_PILIH = 10       # spec §4
MIN_N_TAHAN = 200  # spec §5 A1
MIN_TAHUN = 4      # spec §5 A5: jangkaan > 0 dalam >= 4 daripada 6 tahun

LAJUR_IND = ['rsi14', 'stoch_k', 'bb_pctb', 'mfi14', 'macd_cross', 'hari_macd_cross',
             'rsi_lintas50', 'rsi_lintas60', 'ema_crossback', 'donchian20', 'pocket_pivot',
             'gap_and_go', 'vcp', 'bb_squeeze', 'breakout_asas', 'hari_gc', 'j_ma200',
             'cerun_ma50', 'vol_n50', 'supertrend']


def atr_wilder(h, lo, c, n=ATR_N):
    pc = np.concatenate([[np.nan], c[:-1]])
    tr = np.maximum(h - lo, np.maximum(np.abs(h - pc), np.abs(lo - pc)))
    out = np.full(len(c), np.nan)
    if len(c) <= n:
        return out
    out[n] = np.nanmean(tr[1:n + 1])
    for i in range(n + 1, len(c)):
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def pul_satu_ticker(g):
    """Tiga pulangan keluaran bagi SETIAP bar satu ticker. Masuk pada buka bar berikutnya.

    Dikira dengan lingkaran offset tervektor: untuk setiap j, bandingkan bar t+j merentas semua t
    serentak. Itu mengelakkan imbasan setiap bar dan menjadikan 8.7 juta bar boleh dikira.
    """
    o = g.open.to_numpy('float64')
    h = g.high.to_numpy('float64')
    lo = g.low.to_numpy('float64')
    c = g.close.to_numpy('float64')
    v = g.volume.to_numpy('float64')
    m = len(c)
    a = atr_wilder(h, lo, c)
    nilai = pd.Series(c * v).rolling(20, min_periods=10).median().to_numpy()
    masuk = np.concatenate([o[1:], [np.nan]])          # buka t+1
    paras_h = masuk - HENTI_ATR * a                     # henti E63S
    paras_t = TRAIL_ATR * a                             # lebar Chandelier

    idx = np.arange(m)
    kena_h = np.full(m, -1)                             # bar sentuhan pertama henti
    kena_t = np.full(m, -1)
    puncak = np.where(np.isfinite(masuk), masuk, -np.inf)
    for j in range(1, max(UFUK, TRAIL_MAKS) + 1):
        k = idx + j
        sah = k < m
        kk = np.where(sah, k, 0)
        if j <= UFUK:
            hit = sah & (kena_h < 0) & np.isfinite(paras_h) & (lo[kk] <= paras_h)
            kena_h[hit] = kk[hit]
        if j <= TRAIL_MAKS:
            ck = np.where(sah, c[kk], np.nan)
            puncak = np.where(sah & np.isfinite(ck), np.maximum(puncak, ck), puncak)
            hitt = (sah & (kena_t < 0) & np.isfinite(ck) & np.isfinite(paras_t)
                    & (ck < puncak - paras_t))
            kena_t[hitt] = kk[hitt]

    def keluar_pada(bar, had):
        """Harga keluar = buka bar+1 (atau tutup bar akhir); bar<0 -> hujung had."""
        b = np.where(bar >= 0, bar, np.minimum(idx + had, m - 1))
        kk = np.minimum(b + 1, m - 1)
        return np.where(kk < m, o[kk], c[m - 1]), b

    px63, _ = keluar_pada(np.full(m, -1), UFUK)
    pxs, _ = keluar_pada(kena_h, UFUK)
    pxt, _ = keluar_pada(kena_t, TRAIL_MAKS)
    ks = K.KOMISEN + np.array([K.slippage(x) for x in nilai])
    with np.errstate(invalid='ignore', divide='ignore'):
        def bersih(px):
            return (px * (1 - ks)) / (masuk * (1 + ks)) - 1.0
        return pd.DataFrame({'ticker': g.ticker.iloc[0], 'date': g.date.to_numpy(),
                             'E63': bersih(px63), 'E63S': bersih(pxs), 'ETRAIL': bersih(pxt),
                             'nilai20': nilai})


def bina_pulangan():
    """Kira tiga pulangan bagi setiap bar, cache ke parquet. Sekali sahaja."""
    if PUL.exists():
        return pd.read_parquet(PUL)
    bhg = []
    for y in range(TH0 - 1, TH1 + 2):
        p = HARGA / f'harga_{y}.parquet'
        if p.exists():
            bhg.append(pd.read_parquet(p, columns=['ticker', 'date', 'open', 'high', 'low',
                                                   'close', 'volume']))
    df = pd.concat(bhg, ignore_index=True).sort_values(['ticker', 'date'])
    out = []
    n = 0
    for _, g in df.groupby('ticker', sort=False):
        if len(g) < ATR_N + UFUK + 2:
            continue
        out.append(pul_satu_ticker(g))
        n += 1
        if n % 500 == 0:
            print(f'    {n} ticker', flush=True)
    R = pd.concat(out, ignore_index=True)
    for c in ('E63', 'E63S', 'ETRAIL', 'nilai20'):
        R[c] = R[c].astype('float32')
    CACHE.mkdir(exist_ok=True)
    R.to_parquet(PUL, index=False)
    print(f'  pulangan setiap bar dicache: {len(R):,} baris -> {PUL.name}')
    return R


def muat_indikator():
    """Indikator pada setiap bar dalam alam, daripada cache signals_*.parquet fasa 1."""
    bhg = []
    for y in range(TH0, TH1 + 1):
        p = CACHE / f'signals_{y}.parquet'
        if not p.exists():
            continue
        d = pd.read_parquet(p, columns=['ticker', 'tarikh', 'dalam_univ'] + LAJUR_IND)
        d = d[d.dalam_univ == 1].drop(columns='dalam_univ')
        bhg.append(d)
    D = pd.concat(bhg, ignore_index=True)
    D['tarikh'] = pd.to_datetime(D.tarikh)
    return D.rename(columns={'tarikh': 'date'})


def pemicu(d):
    """14 pemicu: 12 serentak + 2 URUTAN (spec §3). Dikunci."""
    T = {}
    for nm in ('macd_cross', 'rsi_lintas50', 'rsi_lintas60', 'ema_crossback', 'donchian20',
               'pocket_pivot', 'gap_and_go', 'vcp', 'bb_squeeze', 'breakout_asas'):
        T[nm] = d[nm].fillna(0).to_numpy().astype(bool)
    hm = d.hari_macd_cross.to_numpy('float64')
    hg = d.hari_gc.to_numpy('float64')
    T['hari_macd_cross<=3'] = np.nan_to_num(hm, nan=1e9) <= 3
    T['hari_macd_cross<=5'] = np.nan_to_num(hm, nan=1e9) <= 5
    # URUTAN: yang mana silang DAHULU. hari_x kecil = baru berlaku.
    T['urutan:macd->gc'] = (np.nan_to_num(hm, nan=1e9) <= 10) & (np.nan_to_num(hg, nan=1e9) <= 5)
    T['urutan:gc->macd'] = (np.nan_to_num(hg, nan=1e9) <= 10) & (np.nan_to_num(hm, nan=1e9) <= 5)
    return T


def jalur(d):
    """8 jalur TENGAH — bahagian 'longgar' yang kuintil fasa 1 tidak boleh nyatakan."""
    J = {}
    for lj, lo, hi in (('rsi14', 45, 60), ('rsi14', 40, 55), ('rsi14', 50, 65), ('rsi14', 55, 70),
                       ('stoch_k', 20, 50), ('stoch_k', 40, 70), ('bb_pctb', 40, 70),
                       ('mfi14', 40, 60)):
        x = d[lj].to_numpy('float64')
        J[f'{lj}[{lo},{hi}]'] = np.isfinite(x) & (x >= lo) & (x <= hi)
    return J


def penapis(d):
    """6 penapis trend/volum, termasuk 'tiada' sebagai kawalan."""
    n = len(d)
    P = {'tiada': np.ones(n, bool)}
    P['j_ma200>0'] = d.j_ma200.to_numpy('float64') > 0
    P['cerun_ma50>0'] = d.cerun_ma50.to_numpy('float64') > 0
    P['hari_gc<=60'] = np.nan_to_num(d.hari_gc.to_numpy('float64'), nan=1e9) <= 60
    P['vol_n50>=1.2'] = d.vol_n50.to_numpy('float64') >= 1.2
    P['supertrend'] = d.supertrend.to_numpy('float64') > 0
    return P


def metrik_asas(pul):
    """Kadar menang, untung purata, rugi purata, jangkaan — spec §6 mahu kesemuanya."""
    pul = pul[np.isfinite(pul)]
    if pul.size == 0:
        return dict(n=0)
    w = pul > 0
    urut = np.sort(pul)[::-1]
    return dict(n=int(pul.size), menang=float(w.mean() * 100),
                untung=float(pul[w].mean() * 100) if w.any() else 0.0,
                rugi=float(pul[~w].mean() * 100) if (~w).any() else 0.0,
                jangkaan=float(pul.mean() * 100),
                median=float(np.median(pul) * 100),
                tanpa5=float(urut[int(np.ceil(0.05 * urut.size)):].mean() * 100)
                if urut.size > 20 else np.nan)


def grid(d):
    """672 setup = 14 pemicu x 8 jalur x 6 penapis. Pulangkan {nama: topeng}."""
    T, J, P = pemicu(d), jalur(d), penapis(d)
    S = {}
    for tn, tv in T.items():
        for jn, jv in J.items():
            tj = tv & jv
            for pn, pv in P.items():
                S[f'{tn} & {jn} & {pn}'] = tj & pv
    return S, len(T), len(J), len(P)


def tahap_latih(d, S):
    """Nilai KESEMUA 672 pada 2012-2019 dan pilih 10 teratas. Pemilihan berlaku di sini sahaja."""
    m = (d.tahun >= LATIH[0]) & (d.tahun <= LATIH[1])
    pul = d.E63S.to_numpy('float64')
    baris = []
    for nm, ada in S.items():
        r = metrik_asas(pul[ada & m.to_numpy()])
        r['setup'] = nm
        baris.append(r)
    R = pd.DataFrame(baris).set_index('setup')
    layak = R[(R.n >= MIN_N_LATIH) & R.jangkaan.notna()]
    pilih = layak.sort_values('jangkaan', ascending=False).head(N_PILIH)
    return R, list(pilih.index)


def tahap_tahan(d, S, pilih):
    """Mesin penuh fasa 2 pada 10 yang dipilih, tingkap 2020-2025 SAHAJA."""
    m = ((d.tahun >= TAHAN[0]) & (d.tahun <= TAHAN[1])).to_numpy()
    pul = d.E63S.to_numpy('float64')
    bulan = d.date.dt.strftime('%Y-%m').to_numpy()
    minggu = d.date.dt.strftime('%G-W%V').to_numpy()
    tick = d.ticker.to_numpy()
    th = d.tahun.to_numpy()
    pop = m & np.isfinite(pul)
    baris = []
    for nm in pilih:
        ada = S[nm] & pop
        r = metrik_asas(pul[ada])
        r['setup'] = nm
        if r['n'] < 30:
            baris.append(r)
            continue
        # Lift memerlukan label binari: guna pulangan positif sebagai "hasil" supaya
        # permutasi menguji perkara yang sama seperti fasa 2 (kehadiran dalam kelas baik).
        hasil = np.where(pul[pop] > 0, 'PADU', 'GAGAL')
        p, _ = ST.permutasi_lift(hasil, ada[pop], bulan[pop], keluarga='PADU', n=1000)
        r['p_permutasi'] = p
        pb = pul[ada]
        r['p5_blok_ticker'] = ST.bootstrap_blok(pb, tick[ada], n=1000)[0] * 100
        r['p5_blok_minggu'] = ST.bootstrap_blok(pb, minggu[ada], n=1000)[0] * 100
        kon = 0
        for y in range(TAHAN[0], TAHAN[1] + 1):
            ay = ada & (th == y)
            if ay.sum() >= 20 and np.nanmean(pul[ay]) > 0:
                kon += 1
        r['tahun_positif'] = kon
        baris.append(r)
    R = pd.DataFrame(baris).set_index('setup')
    R['lulus_fdr'] = False
    ada_p = R.p_permutasi.notna() if 'p_permutasi' in R else pd.Series(False, index=R.index)
    if ada_p.any():
        lulus, amb = ST.bh_fdr(R.loc[ada_p, 'p_permutasi'].to_numpy(), q=0.01)
        R.loc[ada_p, 'lulus_fdr'] = lulus
        R.loc[ada_p, 'ambang_fdr'] = amb
    R['gate_a'] = (R.lulus_fdr & (R.n >= MIN_N_TAHAN) & (R.tanpa5 > 0)
                   & (R.p5_blok_ticker > 0) & (R.p5_blok_minggu > 0)
                   & (R.tahun_positif >= MIN_TAHUN)).fillna(False)
    return R


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    fl, ft = KELUAR / 'setup_latih.csv', KELUAR / 'setup_tahan.csv'
    if a.laporan_sahaja and fl.exists() and ft.exists():
        return laporan(pd.read_csv(fl).set_index('setup'),
                       pd.read_csv(ft).set_index('setup'), None)

    print('1/4 pulangan setiap bar...', flush=True)
    P = bina_pulangan()
    print('2/4 indikator setiap bar...', flush=True)
    D = muat_indikator()
    print(f'  indikator {len(D):,} bar | pulangan {len(P):,} bar', flush=True)
    d = D.merge(P, on=['ticker', 'date'], how='inner')
    d['tahun'] = d.date.dt.year
    d = d[np.isfinite(d.E63S.to_numpy('float64'))].reset_index(drop=True)
    print(f'  bergabung: {len(d):,} bar dengan pulangan dan indikator', flush=True)
    print('3/4 grid 672 setup, tahap LATIH 2012-2019...', flush=True)
    S, nt, nj, npf = grid(d)
    RL, pilih = tahap_latih(d, S)
    RL.to_csv(fl)
    print(f'  {len(S)} setup ({nt}x{nj}x{npf}); {N_PILIH} teratas dipilih', flush=True)
    for i, nm in enumerate(pilih, 1):
        print(f'    {i:2d}. {nm}  n{RL.loc[nm, "n"]:.0f} jangkaan {RL.loc[nm, "jangkaan"]:+.3f}%',
              flush=True)
    print('4/4 tahap TAHAN 2020-2025 (10 sahaja)...', flush=True)
    RT = tahap_tahan(d, S, pilih)
    RT.to_csv(ft)
    return laporan(RL, RT, d)


def laporan(RL, RT, d):
    lulus = RT[RT.gate_a.fillna(False)]
    L = ['# Setup gaya pedagang: jalur tengah, urutan, 3 syarat', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/step15_setup.py`. Pradaftar `REVERSE/SPEC_SETUP.md` (dikomit sebelum '
             'larian ini).')
    L.append('')
    L.append(f'## Keputusan Gate A: **{"LULUS " + str(len(lulus)) if len(lulus) else "DITOLAK"}**')
    L.append('')
    L.append('Tiga perkara yang fasa 1 **tidak** uji, diuji di sini: jalur **tengah** '
             '(RSI 45–60, bukan kuintil hujung), **urutan** masa (MACD silang dahulu kemudian '
             'golden cross), dan **3** syarat serentak. Populasi juga lebih luas: setiap bar '
             'dalam alam, bukan peristiwa sah sahaja.')
    L.append('')
    L.append(f'**Pecahan masa mengawal pemilihan:** 672 setup dinilai pada LATIH '
             f'{LATIH[0]}–{LATIH[1]}, {N_PILIH} teratas dipilih, dan **hanya** {N_PILIH} itu '
             f'diuji pada TAHAN {TAHAN[0]}–{TAHAN[1]}. Keluarga ujian tahan ialah {N_PILIH}, '
             'bukan 672.')
    L.append('')
    # ---- Jadual tahan ----
    L.append(f'## {N_PILIH} setup terpilih, diuji pada tahan {TAHAN[0]}–{TAHAN[1]}')
    L.append('')
    L.append('| Setup | n | Menang | Untung purata | Rugi purata | Jangkaan | Tanpa 5% teratas | '
             'p | Tahun + | Gate A |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for nm, r in RT.sort_values('jangkaan', ascending=False).iterrows():
        pp = f'{r.p_permutasi:.4f}' if pd.notna(r.get('p_permutasi')) else '–'
        typ = f'{r.tahun_positif:.0f}/6' if pd.notna(r.get('tahun_positif')) else '–'
        L.append(f'| `{nm}` | {r.n:,.0f} | {r.menang:.1f}% | {r.untung:+.2f}% | '
                 f'{r.rugi:+.2f}% | **{r.jangkaan:+.3f}%** | {r.tanpa5:+.3f}% | {pp} | {typ} | '
                 f'{"**YA**" if r.gate_a else "tidak"} |')
    L.append('')
    return laporan2(L, RL, RT, lulus, d)


def laporan2(L, RL, RT, lulus, d):
    # ---- Kadar menang lawan jangkaan (spec §6) ----
    L.append('## Kadar menang BUKAN keuntungan — ini buktinya daripada 672 setup')
    L.append('')
    V = RL[RL.n >= MIN_N_LATIH].dropna(subset=['menang', 'jangkaan'])
    if len(V) > 10:
        from scipy import stats as sps
        rho, p = sps.spearmanr(V.menang, V.jangkaan)
        hi = V.sort_values('menang', ascending=False).head(50)
        L.append(f'Merentas **{len(V)} setup** yang mempunyai ≥ {MIN_N_LATIH} dagangan pada '
                 f'tingkap latih, korelasi antara **kadar menang** dan **jangkaan** ialah '
                 f'Spearman rho **{rho:+.3f}** (p {p:.4f}).')
        L.append('')
        L.append(f'- Kadar menang tertinggi: **{V.menang.max():.1f}%**, '
                 f'jangkaannya {V.loc[V.menang.idxmax(), "jangkaan"]:+.3f}%')
        L.append(f'- 50 setup dengan kadar menang TERTINGGI: jangkaan median '
                 f'**{hi.jangkaan.median():+.3f}%**, dan **{int((hi.jangkaan < 0).sum())} '
                 f'daripada 50 adalah NEGATIF**')
        L.append(f'- Jangkaan tertinggi: {V.jangkaan.max():+.3f}%, kadar menangnya '
                 f'{V.loc[V.jangkaan.idxmax(), "menang"]:.1f}%')
        L.append('')
        L.append('Premis "70% menang, 30% gagal ditampung henti" separuh betul. Kadar menang '
                 '70% pada +1% dengan 30% rugi pada −4% memberi jangkaan **−0.5%**. Jadual di '
                 'atas memaparkan untung purata dan rugi purata bersebelahan supaya ini boleh '
                 'dilihat terus — perhatikan bahawa setup dengan kadar menang tinggi mempunyai '
                 '**untung purata kecil**, dan itulah yang memakannya.')
        L.append('')
    # ---- Tafsiran ----
    L.append('## Tafsiran')
    L.append('')
    if len(lulus):
        L.append(f'**{len(lulus)} setup lulus Gate A pada data TAHAN.** Jangkaan priori saya '
                 'dalam spec §7 ialah DITOLAK, dan ia **SALAH**.')
        L.append('')
        for nm, r in lulus.iterrows():
            L.append(f'- `{nm}`: n {r.n:,.0f}, jangkaan {r.jangkaan:+.3f}%, kadar menang '
                     f'{r.menang:.1f}%, p {r.p_permutasi:.4f}, positif '
                     f'{r.tahun_positif:.0f}/6 tahun')
        L.append('')
        L.append('**Gate B (portfolio lawan SPUS) belum dinilai dan ia menentukan.** Fasa 2 dan '
                 'ujian silang kedua-duanya menunjukkan signal boleh bertahan setiap ujian '
                 'statistik dan tetap gagal di peringkat portfolio.')
    else:
        L.append('**Tiada setup lulus Gate A.** Pecahan 50 terbaik pada latih tidak bertahan '
                 'pada tahan.')
        L.append('')
        gagal = []
        for nm, syarat in (('FDR', RT.lulus_fdr), ('n ≥ 200', RT.n >= MIN_N_TAHAN),
                           ('jangkaan tanpa 5% teratas > 0', RT.tanpa5 > 0),
                           ('bootstrap blok', (RT.p5_blok_ticker > 0) & (RT.p5_blok_minggu > 0)),
                           ('≥ 4/6 tahun positif', RT.tahun_positif >= MIN_TAHUN)):
            gagal.append(f'- lulus `{nm}`: **{int(syarat.fillna(False).sum())}** daripada '
                         f'{len(RT)}')
        L += gagal
        L.append('')
        L.append('Maksudnya setup yang nampak terbaik pada 8 tahun latihan **tidak kekal** pada '
                 '6 tahun seterusnya. Itu tandatangan pemilihan atas hingar, bukan kelebihan: '
                 'menilai 672 setup menghasilkan pemenang latih walaupun tiada satu pun '
                 'mempunyai kelebihan sebenar.')
        L.append('')
        L.append('Ini **bukan** kerana syaratnya terlalu ketat. Jalur yang diuji di sini ialah '
                 'yang paling longgar dalam keseluruhan kajian: julat tengah selebar 15 mata '
                 'RSI, penapis trend ringkas, dan pilihan "tiada penapis" sebagai kawalan.')
    L.append('')
    L.append('## Had')
    L.append('')
    L.append(f'- Alam Release `autotune-data-a02`, **bukan** ditapis Syariah.')
    L.append(f'- `ETRAIL` diimbas maksimum {TRAIL_MAKS} sesi; jika Chandelier tidak tercetus, '
             'posisi ditutup pada hujung tingkap itu. Keputusan Gate A dinilai pada `E63S` '
             '(keluaran yang dipakai seluruh kajian), bukan `ETRAIL`.')
    L.append('- Ambang jalur dan penapis ditetapkan dalam spec §3 sebelum larian dan **tidak '
             'ditala**. Menala ambang akan memerlukan pradaftar baharu dan akan melanggar '
             'larangan penalaan dalam `ARAHAN`.')
    L.append('- Lajur indikator daripada cache `signals_*.parquet` fasa 1 (dikira step1 tanpa '
             'pandang hadapan), jadi ia tepat lajur yang sama yang fasa 1 nilai.')
    L.append('')
    L.append('**Ia tidak mencapai +10%/bulan.** Lihat `SASARAN.md`.')
    L.append('')
    (KELUAR / 'SETUP.md').write_text('\n'.join(L), encoding='utf-8')
    c = ['n', 'menang', 'untung', 'rugi', 'jangkaan', 'tanpa5', 'gate_a']
    print('\n' + RT[[x for x in c if x in RT]].round(3).to_string())
    print(f'\nGate A: {len(lulus)}/{len(RT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
