"""Pembantu dikongsi bagi kaedah Nxx (kombinasi indikator REVERSE).

PERATURAN WAJIB: formula di sini ialah salinan **verbatim** daripada `REVERSE/teras/ind.py`
dan `REVERSE/step18_nxx.py`, bukan daripada `enjin.rsi`/`enjin.atr`. Sebabnya:

  * `enjin.rsi` guna `ewm(alpha=1/n, adjust=False)` tanpa benih purata-n;
  * `enjin.atr` guna `rolling(n).mean()` (purata mudah), bukan pelicinan Wilder.

Kedua-duanya BERBEZA daripada `_wilder` kajian. Kalau kaedah Nxx memakai pembantu enjin,
jejak hadapan akan mengukur peraturan yang bukan peraturan yang dikaji, dan kesemua nombor
`REVERSE/silang_akhir.csv` tidak lagi terpakai. `ujian/test_nxx_sepadan.py` membandingkan
keluaran fail ini dengan `REVERSE/teras/ind.py` pada harga sebenar dan GAGAL jika terpesong.

Rujukan nombor (REVERSE/silang_akhir.csv, 2 tingkap, BH-FDR, gate0-gate3 LULUS):
  GB02_atau3 x X13 -> jangkaan tahan +8.541%, lift +4.191/+1.818, menang 64.2%,
  n 195,681, p 0.0068, tanpa5 +2.858% (POSITIF - tidak bergantung ekor kanan).
"""
import numpy as np
import pandas as pd

EPS = 1e-12                 # ind.py:9
IMBAS = 126                 # step19_nxx_keluar.py:29 - ufuk keluar kajian = TMAX


def _wilder(s, n):
    """Pelicinan Wilder (RMA) dengan nilai awal = purata n pertama. ind.py:13."""
    a = s.to_numpy(dtype='float64')
    out = np.full(a.size, np.nan)
    if a.size < n:
        return pd.Series(out, index=s.index)
    out[n - 1] = np.nanmean(a[:n])
    for i in range(n, a.size):
        x = a[i]
        if not np.isfinite(x):
            x = 0.0
        out[i] = (out[i - 1] * (n - 1) + x) / n
    return pd.Series(out, index=s.index)


def _ema(s, n):
    """ind.py:29."""
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def _supertrend(h, l, c, atr, mult=3.0):
    """Arah Supertrend(10,3): +1 menaik, -1 menurun. ind.py:_supertrend verbatim."""
    hl2 = ((h + l) / 2.0).to_numpy('float64')
    a = atr.to_numpy('float64')
    cc = c.to_numpy('float64')
    n = cc.size
    arah = np.full(n, np.nan)
    atas = hl2 + mult * a
    bawah = hl2 - mult * a
    fa, fb, d = np.nan, np.nan, 1
    for i in range(n):
        if not np.isfinite(a[i]):
            continue
        if not np.isfinite(fa):
            fa, fb, d = atas[i], bawah[i], 1
            arah[i] = d
            continue
        fa = min(atas[i], fa) if cc[i - 1] <= fa else atas[i]
        fb = max(bawah[i], fb) if cc[i - 1] >= fb else bawah[i]
        if d == 1 and cc[i] < fb:
            d = -1
        elif d == -1 and cc[i] > fa:
            d = 1
        arah[i] = d
    return pd.Series(arah, index=c.index)


def indikator(g):
    """Lajur yang N19/N20/N37/N115 dan keluar X13 perlukan, formula kajian verbatim."""
    o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
    d = pd.DataFrame(index=g.index)

    # rsi14 - ind.py:143-147
    delta = c.diff()
    naik_w = _wilder(delta.clip(lower=0), 14)
    turun_w = _wilder((-delta).clip(lower=0), 14)
    d['rsi14'] = 100.0 - 100.0 / (1.0 + naik_w / (turun_w + EPS))

    # rsi2 - ind.py:148-150 (Connors; N16 memerlukannya)
    n2 = _wilder(delta.clip(lower=0), 2)
    t2 = _wilder((-delta).clip(lower=0), 2)
    d['rsi2'] = 100.0 - 100.0 / (1.0 + n2 / (t2 + EPS))

    # adx14 - ind.py:168-178
    up, dn = h.diff(), -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=c.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=c.index)
    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    atr14 = _wilder(tr, 14)
    pdi = 100.0 * _wilder(pdm, 14) / (atr14 + EPS)
    mdi = 100.0 * _wilder(mdm, 14) / (atr14 + EPS)
    d['adx14'] = _wilder((100.0 * (pdi - mdi).abs() / (pdi + mdi + EPS)).fillna(0.0), 14)

    # bb_pctb - ind.py:189-193
    m20 = c.rolling(20, min_periods=20).mean()
    s20 = c.rolling(20, min_periods=20).std(ddof=0)
    bb_a, bb_b = m20 + 2 * s20, m20 - 2 * s20
    d['bb_pctb'] = (c - bb_b) / ((bb_a - bb_b) + EPS) * 100.0

    # ema20 + sentuh_ema20 - ind.py:196, step18_nxx.py:72
    d['ema20'] = _ema(c, 20)
    d['sentuh_ema20'] = l <= d['ema20']

    # vol_n50 - ind.py:202-203
    v50 = v.rolling(50, min_periods=50).mean()
    d['vol_n50'] = v / (v50 + EPS)

    # gap_and_go - ind.py:256-257
    gg = (o > h.shift(1) * 1.02) & (c > o) & (d['vol_n50'] >= 1.5)
    d['gap_and_go'] = gg.astype('float64')
    d.loc[v50.isna(), 'gap_and_go'] = np.nan

    # purata bergerak - ind.py:124-127
    d['ema21'] = _ema(c, 21)
    d['ma20'], d['sd20'] = m20, s20
    for n in (50, 150, 200):
        d[f'ma{n}'] = c.rolling(n, min_periods=n).mean()

    # supertrend(10,3) - ind.py:222
    d['supertrend'] = _supertrend(h, l, c, atr14)

    # donchian55 - ind.py:233-237
    dc55 = h.rolling(55, min_periods=55).max().shift(1)
    d['donchian55'] = (c > dc55).astype('float64')
    d.loc[dc55.isna(), 'donchian55'] = np.nan

    # inside_day + nr7 - ind.py:240-243
    d['inside_day'] = ((h < h.shift(1)) & (l > l.shift(1))).astype('float64')
    jr = h - l
    d['nr7'] = (jr <= jr.rolling(7, min_periods=7).min() + EPS).astype('float64')
    d.loc[jr.rolling(7, min_periods=7).min().isna(), 'nr7'] = np.nan

    # julat20 - ind.py:199
    d['julat20'] = ((h.rolling(20, min_periods=20).max()
                     - l.rolling(20, min_periods=20).min()) / (c + EPS) * 100.0)

    # step18_nxx.tambahan: tinggi20, gap, turun_4d5
    d['tinggi20'] = h.rolling(20).max().shift(1)
    d['gap'] = o / c.shift(1) - 1.0
    d['turun_4d5'] = (c < c.shift(1)).rolling(5).sum() >= 4

    return d


def _b(s):
    """Siri boolean tanpa NaN (NaN -> False), seperti `topeng()` kajian."""
    return s.fillna(False).astype(bool) if s.dtype == object else s.astype('float64').fillna(0.0) > 0.5


# ---------- topeng MASUK (step18_nxx.py:196,197,210,253) ----------
def n19(f):
    """Bawah jalur BB + RSI<30 (LuxAlgo). bb_pctb < 0 DAN rsi14 < 30."""
    return (f.bb_pctb < 0) & (f.rsi14 < 30)


def n20(f):
    """Kembali masuk jalur + RSI silang 30. bb_pctb[-1] < 0 DAN bb_pctb > 0 DAN rsi14 silang naik 30."""
    return (f.bb_pctb.shift(1) < 0) & (f.bb_pctb > 0) & (f.rsi14 > 30) & (f.rsi14.shift(1) <= 30)


def n37(f):
    """Gap and go. open > tinggi[-1] x 1.02 DAN tutup > open DAN vol_n50 >= 1.5."""
    return f.gap_and_go > 0


def n115(f, g):
    """Holy Grail (Raschke). adx14 > 30 DAN rendah menyentuh ema20 DAN tutup > tinggi[-1]."""
    return (f.adx14 > 30) & f.sentuh_ema20 & (g.close > g.high.shift(1))


def n16(f):
    """RSI2 < 10 tanpa penapis (Connors). `nxx.csv`: gate2 LULUS pada X2."""
    return f.rsi2 < 10


def n17(f):
    """RSI14 silang naik 30. `nxx.csv`: gate2 LULUS pada X2, lift +0.870/+1.264."""
    return (f.rsi14 > 30) & (f.rsi14.shift(1) <= 30)


def n75(f):
    """RSI14 < 40 tanpa penapis. `nxx.csv`: gate2 LULUS pada TIGA keluar (X2/X3/X4),
    dan jangkaan mutlak tertinggi antara semua topeng MASUK tunggal (+4.181% pada X3)."""
    return f.rsi14 < 40


# ---------- 7 topeng yang melepasi gate1 (lift positif dua tingkap) ----------
def n42(f, g):
    """Lonjakan volum + tutup naik. `vol_n50 >= 2.0 DAN tutup > tutup[-1]`."""
    return (f.vol_n50 >= 2.0) & (g.close > g.close.shift(1))


def n73(f, g):
    """Bawah jalur BB tanpa penapis RSI. SUPERSET tepat `N19` — menguji sama ada
    penapis `rsi14 < 30` menambah apa-apa (Jaccard N19/N73 ~0.30 = N19 subset N73)."""
    return g.close < (f.ma20 - 2.0 * f.sd20)


def n119(g):
    """Tiga tutup menurun berturut. `tutup[-2] > tutup[-1] DAN tutup[-1] > tutup`."""
    c = g.close
    return (c.shift(2) > c.shift(1)) & (c.shift(1) > c)


def n49(f):
    """Julat tersempit 7 hari DAN hari dalam. `nr7 DAN inside_day`."""
    return (f.nr7 > 0) & (f.inside_day > 0)


def n118(f, g):
    """Atas MA200 tetapi 4 daripada 5 sesi terakhir menurun."""
    return (g.close > f.ma200) & f.turun_4d5


def n46(f, g):
    """Undur ke EMA21 lalu pecah tinggi semalam."""
    return (g.low.shift(1) <= f.ema21.shift(1)) & (g.close > g.high.shift(1))


def n15(f, g):
    """RSI2 < 10 DAN atas MA200 (Connors dengan penapis trend)."""
    return (f.rsi2 < 10) & (g.close > f.ma200)


# ---------- 4 KAWALAN NEGATIF: lift tahan diukur NEGATIF, satu setiap keluarga gagal ----------
def n76(f, g):
    """KAWALAN `MA` (lift tahan −0.641). `tutup > ma50`."""
    return g.close > f.ma50


def n24(f):
    """KAWALAN `TREND` (lift tahan −0.161). `supertrend > 0 DAN adx14 > 20`."""
    return (f.supertrend > 0) & (f.adx14 > 20)


def n31(f):
    """KAWALAN `PECAH` (lift tahan −1.590). Pecah Donchian 55 hari."""
    return f.donchian55 > 0


def n62(f, g):
    """KAWALAN `POLA` (lift tahan −2.651, PALING BURUK dalam 65 dan satu-satunya dengan
    jangkaan mutlak negatif). `julat20 <= 0.08 x tutup DAN tutup > tinggi20[-1]`."""
    return (f.julat20 <= 0.08 * g.close) & (g.close > f.tinggi20)


# ---------- kes SOALAN REJIM: gagal gate1, dijejak dengan sengaja ----------
def n124(f):
    """Gap 8% + volum 2x. Lift tahan **+7.066** = TERTINGGI antara 65 topeng, hampir 2x
    `N19` — tetapi lift LATIH negatif, jadi ia GAGAL gate1 pradaftar.

    Dijejak bukan kerana ia dijangka berjaya, tetapi kerana jejak hadapan boleh membezakan
    dua tafsiran yang kajian tidak boleh: (a) peraturan gagal yang bernasib baik dalam
    2020-2025, atau (b) peraturan yang hanya berfungsi dalam rejim selepas 2020. Keputusan
    memasukkannya dibuat dengan mata terbuka bahawa ia gagal gate.
    """
    return (f.gap >= 0.08) & (f.vol_n50 >= 2.0)


def gb02_atau3(f, g):
    """KESATUAN N19 u N37 u N115 - konfigurasi yang melepasi KESEMUA empat gate."""
    return n19(f) | n37(f) | n115(f, g)


# ---------- keluar (lorong 1) ----------
def x13(f):
    """X13 - keluar bila rsi14 > 70; enjin menjual pada buka esok. Keluar TERBAIK diukur
    (asas +4.350%), dan satu-satunya yang asasnya POSITIF selepas buang 5% teratas."""
    return f.rsi14 > 70


def u14(g):
    """`U14` momentum 12-1 bulan = C[-21] / C[-252] - 1. step27_keluar_portfolio.py:56.

    Dipakai sebagai `rank` kerana `harian_c.MAKS_KAEDAH` mengehadkan 10 isyarat baharu
    setiap kaedah setiap imbasan dan memilih ikut `rank`. Dengan `rank = 0` pemilihan
    antara isyarat menjadi **sewenang-wenang**, dan `KEPEKATAN_BENIH.md` mengukur hingar
    pemilihan susunan sewenang-wenang pada **17.3 mata peratus setahun** pada 8 slot.
    `SISTEM.md` mengukur bahawa memeringkat ikut skor objektif BERTERUSAN memberi sebaran
    benih **0.00**, jadi pemeringkat berterusan menghapuskan hingar itu.

    `U14` dipilih kerana (a) ia pemeringkat paling KERAP antara pemenang `E6a` dan (b) ia
    boleh dikira daripada harga sahaja.

    **DUA PEMBETULAN 1 Nov 2026** (`REVERSE/AUDIT_JEJAK_N.md`), kedua-duanya disahkan terhadap
    CSV sumber:

    1. Dakwaan asal "setiap pemenang `E6a` memakai U14" (dalam `HIERARKI.md` dan
       `SPEC_JEJAK_N.md`) **SALAH**. 19 pemenang terbahagi **U14 11 · U01 8 · U02 0** — jadi
       **8 daripada 19 memakai `U01` yang RAWAK**, dan kelebihan U14 atas susunan rawak dalam
       E6 jauh lebih kecil daripada yang dinyatakan.
    2. Perbandingan "`U02` ... 16.12 lawan 11.93 pada 8 slot" membandingkan **DUA MASUK
       BERBEZA** (16.12 = `GB02_atau3,8,X13,U02`; 11.93 = `GB02_atau4,8,X13,U01`). Bagi masuk
       yang SAMA (`GB02_atau3,8,X13`): U02 16.12 · U01 9.40 · U08 8.83. Dan `U14` **tiada
       dalam `portfolio_n_ringkas.csv` sama sekali** — lajur urutan hanya U01/U02/U08, jadi
       pemeringkat yang sebenarnya dipasang di sini **tidak pernah diuji pada peringkat
       portfolio bagi mana-mana masuk Nxx**.

    Sebab tinggal untuk memakai U14 kekal sah tetapi lebih sempit: ia skor BERTERUSAN (jadi ia
    menghapuskan hingar pemilihan 17.3 mata/tahun yang susunan sewenang-wenang suntik) dan ia
    boleh dikira daripada harga sahaja. Itu sahaja. Ia BUKAN "pemeringkat terbaik yang diukur".
    """
    c = g.close
    s = c.shift(21) / c.shift(252) - 1.0
    return s.replace([np.inf, -np.inf], np.nan).fillna(-9e9)


def pasang(g, masuk, f=None, nama_rank=None):
    """Tulis lajur enjin v1.2. TIADA henti dan TIADA sasaran dengan sengaja:

    * `stop = NaN` -> `enjin.trades` guna `sp = -inf`, jadi kecacatan henti hari-0
      (`REVERSE/KOLAM_EKOR.md` §4a: 421/1,770 posisi, menang 0.00%) **tidak boleh berlaku**;
    * `tgt = NaN` -> tiada sasaran untung, kerana `KOMBINASI.md` mengukur sasaran 1xATR
      menukar asas +2.595% menjadi -0.281%.

    Lorong 2 repo (Chandelier tutup 4xATR14) = `X15` kajian dan berjalan automatik pada
    setiap posisi, jadi X13 dan X15 terukur BERSEBELAHAN tanpa kod tambahan.

    `rank` = `u14()` dan BUKAN 0.0 — lihat `u14` untuk sebabnya (hingar pemilihan 17.3
    mata/tahun kalau susunan sewenang-wenang).
    """
    if f is None:                      # pemanggil biasanya sudah mengiranya;
        f = indikator(g)               # `indikator()` ialah kos CPU termahal saluran
    g['sig'] = masuk.fillna(False).astype(bool)
    g['stop'] = np.nan
    g['tgt'] = np.nan
    g['exitc'] = x13(f).fillna(False).astype(bool)
    g['rank'] = u14(g) if nama_rank is None else f[nama_rank].fillna(-9e9).astype('float64')
    return f
    return f


def hampir_syarat(syarat, n_bar, cukup):
    """Watchlist "hampir" generik bagi kaedah Nxx.

    `syarat` = senarai (label, dipenuhi, jarak_unit) bagi bar TERAKHIR. Jarak dalam unit
    indikator sendiri (mata RSI, mata %b, mata ADX) kerana peraturan Nxx ialah ambang
    indikator, bukan paras harga: melaporkan "paras harga" akan mengandaikan hubungan
    harga->indikator yang tidak linear, jadi `paras` dibiar None dengan sengaja.
    """
    if n_bar < cukup:
        return None
    ok = [s for s in syarat if s[1]]
    belum = [s for s in syarat if not s[1]]
    if not belum or not ok:                 # semua sudah (= sig) atau semua belum (terlalu jauh)
        return None
    jarak = [s[2] for s in belum if s[2] is not None]
    j = float(min(jarak)) if jarak else None
    return {'sebab': ' DAN '.join(s[0] for s in ok) + ' sudah',
            'syarat_beli': ' DAN '.join(s[0] for s in syarat),
            'pencetus': ' DAN '.join(s[0] for s in belum),
            'paras': None,
            'jarak_pct': j,
            'syarat_dipenuhi': f'{len(ok)}/{len(syarat)}',
            'skor': 0.5 if j is None else round(float(max(0.0, 1.0 - j / 20.0)), 3)}
