"""Lift MASUK setiap kaedah atas kolam Lejar Penuh — gate G3 kad skor (pindaan 7 Nov 2026).

Soalan: adakah kaedah ini MEMILIH saham yang lebih baik daripada saham lain yang dibeli Lejar pada hari
yang sama? Itu kemahiran masuk. Nilai peraturan KELUAR diukur di tempat lain (G2 buku harian, G6
portfolio) — sengaja dipisahkan.

Mengapa versi lama (lift padan hari beli x baldi hari pegang, SE ikut hari beli) dibuang — DIUKUR
7 Nov 2026 (`standard/SPEC_KAD_SKOR.md` pindaan 7 Nov; `laporan/PLASEBO_GATE.md`):
  1. Baldi hari pegang ditentukan oleh peraturan keluar, jadi belian RAWAK dengan henti 2xATR + sasaran
     6% mendapat lift +2.17 mata (p < 0.05 dalam 95% cabutan) dan tanpa henti -2.00 mata. Ukuran itu
     mengukur bentuk keluar dalam satu fasa pasaran, bukan pemilihan saham.
  2. SE berkelompok ikut hari beli meluluskan plasebo "lekit" (saham sama dibeli berulang) 51% masa dan
     plasebo condong ATR 30% masa, lawan sasaran 5%.

Reka bentuk sekarang (lulus plasebo: kadar lulus palsu 1.9-3.4% pada ketiga-tiga plasebo, kod produksi):
  - Pulangan UFUK TETAP: beli pada buka `tarikh_beli` (harga_beli Lejar) -> tutup sesi ke-UFUK
    (sesi beli = sesi 1), tolak kos KOS. Bebas peraturan keluar. Hanya posisi dengan ufuk lengkap.
  - Unit = saham-hari UNIK. Kolam = setiap saham-hari yang dibeli mana-mana kaedah hari itu (Nxx yang
    membeli saham sama pada hari sama tidak lagi dikira berkali-kali).
  - Asas = purata kolam pada hari beli sama DAN tercile ATR14% (hari isyarat) sama, TIDAK termasuk
    saham-hari kaedah itu sendiri (tinggal-satu-kaedah-keluar). Padanan ATR membuang pendedahan
    turun-naik (kaedah yang selalu membeli saham meruap bukan "pandai" hanya kerana pasaran naik).
  - SE dua hala (saham, minggu ISO beli), df = bilangan kluster terkecil - 1. BH-FDR step-up.
  - Hanya hari beli LANGSUNG (MULA_LANGSUNG): bina semula 3 Nov 2026 mengisi Nxx 15 Okt-2 Nov dengan kod
    yang belum wujud ketika itu, jadi baris itu isian, bukan rekod hadapan.

Guna: python3 BacktestShariah2/standard/lift_kaedah.py
Keluaran: BacktestShariah2/laporan/LIFT_KAEDAH.md, BacktestShariah2/data/analisis/lift.json
          (= dokumen db dashboard `analisis/lift`)
"""
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
STOR = os.environ.get('LEJAR_STOR', os.path.join(BS2, 'data', 'harga', 'stor'))
MD = os.environ.get('LIFT_MD', os.path.join(BS2, 'laporan', 'LIFT_KAEDAH.md'))
JSN = os.environ.get('LIFT_JSON', os.path.join(BS2, 'data', 'analisis', 'lift.json'))

# ---------- PRADAFTAR 7 Nov 2026 (SPEC_KAD_SKOR.md) - dikunci oleh ujian/test_kad_skor.py::TestKunci ----------
KOS = 0.2          # 0.1% setiap belah
UFUK = 10          # G3_UFUK: sesi dari buka hari beli hingga tutup sesi ke-10
MIN_N = 30         # G3_MIN_N: saham-hari minimum sebelum satu kaedah diuji
MIN_MINGGU = 5     # G3_MIN_MINGGU: minggu ISO beli berbeza minimum (kluster SE)
Q_FDR = 0.05       # G3_Q
TERCILE = 3        # padanan ATR14% hari isyarat
MULA_LANGSUNG = {'M': '2026-10-15', 'N': '2026-11-03', 'GB': '2026-11-03'}   # tarikh isyarat
# ---------------------------------------------------------------------------------------------------------------
Z_KUASA = 0.8416


def mula_langsung(mid):
    """Tarikh isyarat pertama yang dikira data hadapan langsung bagi kaedah `mid`."""
    mid = str(mid)
    if mid.startswith('GB'):
        return MULA_LANGSUNG['GB']
    return MULA_LANGSUNG.get(mid[:1], MULA_LANGSUNG['M'])


def langsung(P):
    """Topeng baris yang direkod langsung (tarikh isyarat >= MULA_LANGSUNG kaedahnya)."""
    mula = {m: mula_langsung(m) for m in P.id_kaedah.unique()}
    return P.tarikh_isyarat.astype(str).to_numpy() >= P.id_kaedah.map(mula).to_numpy()


def posisi():
    """Semua posisi Lejar Penuh (terbuka.csv + tutup/*.csv). Lorong 1."""
    f = [os.path.join(LEJAR, 'terbuka.csv')] + sorted(glob.glob(os.path.join(LEJAR, 'tutup', '*.csv')))
    P = pd.concat([pd.read_csv(x) for x in f if os.path.exists(x)], ignore_index=True)
    P['tarikh_keluar'] = P.tarikh_keluar.fillna('').astype(str)
    return P


def sesi_lejar():
    """Sesi terakhir Lejar 'YYYYMMDD' (status.json), atau None jika tiada."""
    f = os.path.join(LEJAR, 'status.json')
    if not os.path.exists(f):
        return None
    s = (json.load(open(f, encoding='utf-8')).get('sesi_terakhir') or '').replace('-', '')
    return s or None


def potong_sesi(H):
    """Selaraskan stor dengan Lejar: buang bar SELEPAS sesi terakhir Lejar (keluar belum diproses untuk sesi
    itu), dan GAGAL jika stor lebih lama daripada Lejar (penanda basi). Audit 7 Nov 2026: tiada semakan ini
    sebelumnya, jadi kad skor boleh membaca harga basi tanpa sesiapa tahu."""
    had = sesi_lejar()
    if had is None or H.empty:
        return H
    akhir = H.date.max()
    if akhir < had:
        raise SystemExit(f'stor harga basi: bar terakhir {akhir} < sesi Lejar {had}')
    return H[H.date <= had]


def harga_akhir():
    """(tutup terakhir setiap ticker, indeks sesi stor) - dihadkan kepada sesi terakhir Lejar."""
    f = [os.path.join(STOR, x) for x in ('harga_A.csv', 'harga_B.csv')]
    H = pd.concat([pd.read_csv(x, usecols=['ticker', 'date', 'close'])
                   for x in f if os.path.exists(x)], ignore_index=True)
    H['date'] = H.date.astype(str)
    H = potong_sesi(H)
    sesi = sorted(H.date.unique())
    return H.sort_values('date').groupby('ticker').close.last(), {d: i for i, d in enumerate(sesi)}, sesi


def nilai(P, akhir, idx):
    """Pulangan setiap posisi: tutup = untung akhir, terbuka = ditanda-ke-pasaran. Tolak kos.
    (Maklumat kad skor - bukan ujian G3.)"""
    P = P.copy()
    P['untung_pct'] = pd.to_numeric(P.untung_pct, errors='coerce')
    P['hari'] = pd.to_numeric(P.hari, errors='coerce')
    P['terbuka'] = P.tarikh_keluar == ''
    beli = pd.to_numeric(P.harga_beli, errors='coerce')
    kini = (P.saham.map(akhir) / beli - 1) * 100
    P['pul'] = np.where(P.terbuka, kini, P.untung_pct) - KOS
    hb = P.tarikh_beli.astype(str).str.replace('-', '', regex=False).map(idx)
    P['hari_pegang'] = np.where(P.terbuka, max(idx.values()) - hb, P.hari).astype(float)
    return P.dropna(subset=['pul', 'hari_pegang']).copy()


def panel_harga(stor=None):
    """(sesi ['YYYYMMDD'], C, A): C = tutup ticker x sesi (ffill), A = ATR14% Wilder ticker x sesi."""
    stor = stor or STOR
    f = [os.path.join(stor, x) for x in ('harga_A.csv', 'harga_B.csv')]
    H = pd.concat([pd.read_csv(x, usecols=['ticker', 'date', 'high', 'low', 'close'])
                   for x in f if os.path.exists(x)], ignore_index=True)
    H['date'] = H.date.astype(str)
    H = potong_sesi(H).drop_duplicates(['ticker', 'date']).sort_values(['ticker', 'date'])
    pc = H.groupby('ticker').close.shift(1)
    tr = np.maximum(H.high - H.low, np.maximum((H.high - pc).abs(), (H.low - pc).abs()))
    atr = tr.groupby(H.ticker).transform(lambda s: s.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean())
    H['atrp'] = atr / H.close * 100
    sesi = sorted(H.date.unique())
    C = H.pivot(index='ticker', columns='date', values='close').reindex(columns=sesi).ffill(axis=1)
    A = H.pivot(index='ticker', columns='date', values='atrp').reindex(columns=sesi)
    return sesi, C, A


def rejim_qqq(stor=None):
    """{'YYYYMMDD': True/False} rejim R1: QQQ tutup > SMA50 DAN SMA10 > SMA20 (SPEC_KAD_SKOR pindaan 7 Nov)."""
    p = os.path.join(stor or STOR, 'harga_idx.csv')
    if not os.path.exists(p):
        return {}
    d = pd.read_csv(p)
    q = d[d.ticker == 'QQQ'].assign(date=lambda x: x.date.astype(str)).sort_values('date').set_index('date').close
    on = (q > q.rolling(50).mean()) & (q.rolling(10).mean() > q.rolling(20).mean())
    on = on[q.rolling(50).mean().notna()]
    return {k: bool(v) for k, v in on.items()}


def _kuarantin():
    """Fungsi tercemar(ticker, mula, tamat) daripada standard/kuarantin.py (data harga tercemar, cth. SUPN/INDV
    7 Nov 2026); jika modul tiada, sentiasa False."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from kuarantin import tercemar  # noqa: WPS433
        return tercemar
    except Exception:
        return lambda t, a, b=None: False


def bh_lulus(p, q=Q_FDR):
    """BH-FDR step-up: lulus semua p <= p_(k), k terbesar dengan p_(k) <= q k / m."""
    p = np.asarray(p, float)
    m = len(p)
    if not m:
        return np.zeros(0, bool)
    o = np.argsort(p)
    ok = p[o] <= q * np.arange(1, m + 1) / m
    lulus = np.zeros(m, bool)
    if ok.any():
        k = np.nonzero(ok)[0].max()
        lulus[o[:k + 1]] = True
    return lulus


def _se_kl(e, kl):
    """SE berkelompok (CR1) bagi purata, dengan G/(G-1). Pulang (se, G)."""
    s = pd.Series(e).groupby(np.asarray(kl)).sum().to_numpy()
    G = len(s)
    if G < 2:
        return np.nan, G
    return float(np.sqrt((s ** 2).sum()) / len(e) * np.sqrt(G / (G - 1))), G


def se_dua_hala(x, k1, k2):
    """SE purata `x` berkelompok dua hala (Cameron-Gelbach-Miller), df = min(G1, G2) - 1.
    Disahkan plasebo 7 Nov 2026 (`laporan/PLASEBO_GATE.md`). Pulang (se, df)."""
    x = np.asarray(x, float)
    e = x - x.mean()
    k1, k2 = np.asarray(k1).astype(str), np.asarray(k2).astype(str)
    s1, g1 = _se_kl(e, k1)
    s2, g2 = _se_kl(e, k2)
    s12, _ = _se_kl(e, np.char.add(np.char.add(k1, '|'), k2))
    v = max(s1 ** 2 + s2 ** 2 - s12 ** 2, s1 ** 2, s2 ** 2)
    return float(np.sqrt(v)), int(min(g1, g2) - 1)


def saham_hari(P, sesi, C, A, kuarantin=None):
    """Baris saham-hari unik setiap kaedah (langsung, ufuk lengkap): id_kaedah, saham, tarikh_beli, r, q.
    r = pulangan UFUK sesi (%) tolak KOS; q = tercile ATR14% hari isyarat dalam kolam hari itu.
    kuarantin(ticker, mula, tamat) -> True membuang saham-hari yang ufuknya menyentuh data harga tercemar."""
    kuarantin = kuarantin or (lambda t, a, b=None: False)
    Q = P.loc[langsung(P), ['id_kaedah', 'saham', 'tarikh_isyarat', 'tarikh_beli', 'harga_beli']].copy()
    Q['harga_beli'] = pd.to_numeric(Q.harga_beli, errors='coerce')
    Q = Q.dropna(subset=['harga_beli'])
    Q = Q.drop_duplicates(['id_kaedah', 'saham', 'tarikh_beli'])
    si = {d: i for i, d in enumerate(sesi)}
    hb = Q.tarikh_beli.astype(str).str.replace('-', '', regex=False).map(si)
    Q = Q[hb.notna()].copy()
    Q['hb'] = hb[hb.notna()].astype(int)
    Q = Q[(Q.hb + UFUK - 1 <= len(sesi) - 1) & Q.saham.isin(C.index)].copy()
    if Q.empty:
        return Q.assign(r=[], q=[])
    ri = C.index.get_indexer(Q.saham)
    Cv = C.to_numpy()
    Q['r'] = (Cv[ri, (Q.hb + UFUK - 1).to_numpy()] / Q.harga_beli.to_numpy() - 1) * 100 - KOS
    isy = Q.tarikh_isyarat.astype(str).str.replace('-', '', regex=False)
    ci = A.columns.get_indexer(isy)
    Av = A.to_numpy()
    Q['atrp'] = np.where(ci >= 0, Av[ri, np.maximum(ci, 0)], np.nan)
    Q = Q[np.isfinite(Q.r) & np.isfinite(Q.atrp)]
    tamat = [f'{sesi[i][:4]}-{sesi[i][4:6]}-{sesi[i][6:]}' for i in (Q.hb + UFUK - 1)]
    bebas = np.array([not kuarantin(t, a, b) for t, a, b in zip(Q.saham, Q.tarikh_beli.astype(str), tamat)], dtype=bool)
    Q = Q.loc[bebas].copy()
    if Q.empty:
        return Q.drop(columns='atrp').assign(q=[])
    kol = Q.drop_duplicates(['saham', 'tarikh_beli'])[['saham', 'tarikh_beli', 'atrp']].copy()
    kol['q'] = kol.groupby('tarikh_beli').atrp.transform(
        lambda s: np.floor(s.rank(method='first') * TERCILE / (len(s) + 1e-9)).clip(0, TERCILE - 1)
        if len(s) >= TERCILE else pd.Series(0, index=s.index))
    Q = Q.drop(columns='atrp').merge(kol[['saham', 'tarikh_beli', 'q']], on=['saham', 'tarikh_beli'])
    return Q.reset_index(drop=True)


def lift_masuk(Q):
    """Tambah lajur `asas` dan `lift` kepada saham-hari Q. Asas = purata kolam saham-hari UNIK pada
    (tarikh_beli, q) TANPA saham-hari kaedah itu sendiri."""
    kol = Q.drop_duplicates(['saham', 'tarikh_beli'])
    S = kol.groupby(['tarikh_beli', 'q']).r.agg(['sum', 'size']).rename(columns={'sum': 'S', 'size': 'N'})
    M = Q.groupby(['id_kaedah', 'tarikh_beli', 'q']).r.agg(['sum', 'size']).rename(columns={'sum': 's', 'size': 'n'})
    X = Q.join(S, on=['tarikh_beli', 'q']).join(M, on=['id_kaedah', 'tarikh_beli', 'q'])
    baki = X.N - X.n
    X['asas'] = np.where(baki > 0, (X.S - X.s) / baki.replace(0, np.nan), np.nan)
    X['lift'] = X.r - X.asas
    return X.drop(columns=['S', 'N', 's', 'n']).dropna(subset=['lift'])


def uji(X):
    """Satu baris setiap kaedah: lift masuk, t dua hala (saham, minggu ISO), BH-FDR step-up."""
    X = X.copy()
    tb = pd.to_datetime(X.tarikh_beli.astype(str))
    iso = tb.dt.isocalendar()
    X['minggu'] = (iso.year * 100 + iso.week).astype(int).to_numpy()
    baris = []
    for mid, g in X.groupby('id_kaedah'):
        if len(g) < MIN_N or g.minggu.nunique() < MIN_MINGGU:
            continue
        se, df = se_dua_hala(g.lift, g.saham, g.minggu)
        if not (se > 0) or df < 1:
            continue
        m = float(g.lift.mean())
        t = m / se
        baris.append(dict(id=mid, n=len(g), hari_beli=int(g.tarikh_beli.nunique()), minggu=int(g.minggu.nunique()),
                          pul=float(g.r.mean()), lift=m, se=se, df=df, menang=float((g.r > 0).mean() * 100),
                          t=t, p=float(2 * (1 - stats.t.cdf(abs(t), df))),
                          sd_hari=float(g.groupby('tarikh_beli').lift.mean().std(ddof=1))))
    kol = ['n', 'hari_beli', 'minggu', 'pul', 'lift', 'se', 'df', 'menang', 't', 'p', 'sd_hari', 'bh', 'lulus']
    if not baris:
        return pd.DataFrame(columns=kol, index=pd.Index([], name='id'))
    R = pd.DataFrame(baris).set_index('id').sort_values('p')
    R['bh'] = Q_FDR * np.arange(1, len(R) + 1) / len(R)
    R['lulus'] = bh_lulus(R.p.to_numpy())
    return R


def hari_perlu(sd, m, lift):
    """Hari beli berbeza untuk melihat `lift` mata pada kuasa 80%, Bonferroni merentas m kaedah."""
    z = stats.norm.ppf(1 - Q_FDR / max(m, 1) / 2)
    return float(np.ceil((z + Z_KUASA) ** 2 * sd * sd / lift / lift))


def nama_kaedah():
    """Nama setiap ID. Mxx daripada ringkasan Lejar; Nxx/GBxx dibina `masuk → keluar` daripada
    `data/registry_N.csv`."""
    out = {}
    f = os.path.join(LEJAR, 'ringkasan.json')
    if os.path.exists(f):
        out = {r['id']: (r.get('nama') or '')
               for r in json.load(open(f, encoding='utf-8')).get('kaedah', [])}
    reg = os.path.join(BS2, 'data', 'registry_N.csv')
    if os.path.exists(reg):
        import csv
        N = {r['id']: (r.get('nama') or '') for r in csv.DictReader(open(reg, encoding='utf-8'))}
        for mid in list(out):
            if out[mid]:
                continue
            m = re.fullmatch(r'(N\d+|GB\d+\w*?)(X\d+)', mid)
            if m and N.get(m.group(1)):
                out[mid] = f'{N[m.group(1)]} → {N.get(m.group(2), m.group(2))}'
            elif N.get(mid):
                out[mid] = N[mid]
    return out


def status(hari_beli, perlu2):
    return 'BELUM CUKUP' if hari_beli < perlu2 else 'BOLEH DIBACA'


def laporan(M, R, nm):
    A = ['# Lift MASUK setiap kaedah (gate G3)', '',
         f"Dijana {M['dijana']} UTC oleh `standard/lift_kaedah.py` (Actions `analisis.yml`). Pradaftar: "
         '`standard/SPEC_KAD_SKOR.md` pindaan 7 Nov 2026. Rekod analisis sahaja: tiada order, tiada wang sebenar.', '',
         '## Apa yang diukur', '',
         f"Adakah kaedah ini memilih saham yang lebih baik daripada saham lain yang dibeli Lejar **pada hari yang "
         f"sama dan tahap turun-naik (tercile ATR) yang sama**? Pulangan diukur pada ufuk TETAP {UFUK} sesi (buka "
         f"hari beli → tutup sesi ke-{UFUK}, kos {KOS}%), jadi peraturan keluar TIDAK mempengaruhi nombor ini. "
         'Nilai keluar diukur oleh G2 (buku harian) dan G6 (portfolio).', '',
         'Versi lama (padanan baldi hari pegang, SE ikut hari beli) dibuang kerana ia meluluskan belian RAWAK: '
         'henti + sasaran rawak mendapat lift +2.17 mata, dan SE lama meluluskan plasebo sehingga 51% masa. '
         'Reka bentuk ini lulus plasebo pada kadar 1.9–3.4% (`laporan/PLASEBO_GATE.md`).', '',
         '## Data', '',
         f"Hari beli LANGSUNG sahaja (Mxx sejak isyarat {MULA_LANGSUNG['M']}, Nxx/GB sejak {MULA_LANGSUNG['N']}). "
         f"**{M['saham_hari']:,} saham-hari** dengan ufuk {UFUK} sesi lengkap, {M['hari_beli']} hari beli, "
         f"{M['kaedah_ada']} kaedah. Rejim (QQQ > SMA50 dan SMA10 > SMA20) pada hari beli ini: "
         f"ON {M['hari_on']} · OFF {M['hari_off']}.", '',
         '## Keputusan', '',
         f"Diuji (≥ {MIN_N} saham-hari, ≥ {MIN_MINGGU} minggu): **{M['diuji']}** kaedah. "
         f"Lift positif lulus BH-FDR: **{M['positif']}**. Lift negatif lulus BH-FDR: **{M['negatif']}**.", '']
    if M['diuji'] == 0:
        A += ['**Belum ada kaedah yang cukup data untuk diuji.** Ufuk 10 sesi dan hari beli langsung bermakna ujian '
              'pertama memerlukan ~5 minggu data langsung. Ini disengajakan: tiada jawapan lebih baik daripada '
              'jawapan palsu.', '']
    else:
        A += ['| Kaedah | Saham-hari | Hari beli | Minggu | Pulangan 10 sesi % | **Lift mata** | t | p | BH | Status |',
              '|---|---|---|---|---|---|---|---|---|---|']
        for mid, r in R.sort_values('lift', ascending=False).head(25).iterrows():
            A.append(f"| `{mid}` {str(nm.get(mid, ''))[:30]} | {r.n:.0f} | {r.hari_beli:.0f} | {r.minggu:.0f} | "
                     f"{r.pul:+.2f} | **{r.lift:+.2f}** | {r.t:+.2f} | {r.p:.4f} | {'lulus' if r.lulus else 'tidak'} | "
                     f"{r.status} |")
        A.append('')
    A += ['## Bila jadual ini boleh dipercayai', '',
          f"Hari beli diperlukan untuk melihat lift 2 mata merentas kaedah diuji: **{M['perlu2'] or '–'}** "
          f"(dikira semula setiap larian). Ada {M['hari_beli']}. Kad skor juga mewajibkan ≥ 10 hari beli dalam "
          'setiap rejim (G1), supaya keputusan tidak datang daripada satu fasa pasaran.', '',
          '## Had', '',
          '- Lift ialah kemahiran MASUK relatif kepada saham lain yang Lejar beli, bukan pulangan akaun.',
          '- Kolam ialah alam Lejar (saham patuh Syariah ≥ USD10), bukan seluruh pasaran.',
          '- Sasaran +10%/bulan tidak boleh dibaca daripada jadual ini (`REVERSE/SASARAN.md`).', '']
    return '\n'.join(A)


def main():
    if not os.path.exists(os.path.join(LEJAR, 'terbuka.csv')):
        print('lift_kaedah: lejar/terbuka.csv tiada; tiada apa untuk diukur', file=sys.stderr)
        return 0
    P = posisi()
    sesi, C, A = panel_harga()
    rj = rejim_qqq()
    st = json.load(open(os.path.join(LEJAR, 'status.json'), encoding='utf-8')) \
        if os.path.exists(os.path.join(LEJAR, 'status.json')) else {}
    Q = saham_hari(P, sesi, C, A, _kuarantin())
    X = lift_masuk(Q) if len(Q) else Q.assign(asas=[], lift=[])
    R = uji(X) if len(X) else uji(pd.DataFrame(columns=['id_kaedah', 'saham', 'tarikh_beli', 'r', 'lift']))
    sd = float(np.nanmedian(R.sd_hari)) if len(R) and R.sd_hari.notna().any() else float('nan')
    perlu2 = int(hari_perlu(sd, len(R), 2.0)) if np.isfinite(sd) and len(R) else None
    R['status'] = [status(h, perlu2 if perlu2 else 10 ** 9) for h in R.hari_beli]
    hb = sorted(X.tarikh_beli.astype(str).unique()) if len(X) else []
    isy = P.drop_duplicates('tarikh_beli').set_index('tarikh_beli').tarikh_isyarat.astype(str)
    on = [rj.get(isy.get(h, '').replace('-', '')) for h in hb]
    nm = nama_kaedah()
    L = langsung(P)
    M = dict(dijana=f'{pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M}', saham_hari=int(len(X)), hari_beli=len(hb),
             kaedah_ada=int(X.id_kaedah.nunique()) if len(X) else 0, hari_on=int(sum(v is True for v in on)),
             hari_off=int(sum(v is False for v in on)), diuji=int(len(R)),
             positif=int(((R.lift > 0) & R.lulus).sum()), negatif=int(((R.lift < 0) & R.lulus).sum()),
             perlu2=perlu2)
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, 'w', encoding='utf-8').write(laporan(M, R, nm))

    PL = P[L].copy()
    PL['terbuka'] = PL.tarikh_keluar == ''
    info = PL.groupby('id_kaedah').agg(tutup=('terbuka', lambda s: int((~s).sum())), buka=('terbuka', 'mean'))
    rows = []
    for mid, r in R.sort_values('lift', ascending=False).iterrows():
        d = dict(id=mid, nama=nm.get(mid, ''), n=int(r.n), hari_beli=int(r.hari_beli), minggu=int(r.minggu),
                 tutup=int(info.tutup.get(mid, 0)), buka_pct=round(float(info.buka.get(mid, 0)) * 100, 2),
                 pul=round(float(r.pul), 4), lift=round(float(r.lift), 4), hari=UFUK, sebulan=None,
                 menang=round(float(r.menang), 2), t=round(float(r.t), 4), p=round(float(r.p), 6),
                 bh=round(float(r.bh), 6), lulus=bool(r.lulus), status=r.status)
        rows.append(d)
    os.makedirs(os.path.dirname(JSN), exist_ok=True)
    json.dump(dict(kini=str(pd.Timestamp.now(tz='UTC').date()), versi='lift_masuk_2026-11-07',
                   mula=st.get('mula'), mula_langsung=MULA_LANGSUNG, sesi_terakhir=st.get('sesi_terakhir'),
                   harga_pada=sesi[-1] if sesi else None, ufuk=UFUK, posisi=int(len(X)),
                   kaedah=M['kaedah_ada'], hari_beli=M['hari_beli'], hari_on=M['hari_on'], hari_off=M['hari_off'],
                   kos=KOS, sd_lift=None if not np.isfinite(sd) else round(sd, 4), perlu_2mata=perlu2,
                   diuji=M['diuji'], positif=M['positif'], negatif=M['negatif'], rows=rows),
              open(JSN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"LIFT_KAEDAH.md | {M['saham_hari']} saham-hari langsung (ufuk {UFUK}) | {M['diuji']} kaedah diuji | "
          f"positif {M['positif']} | negatif {M['negatif']} | {M['hari_beli']} hari beli (ON {M['hari_on']}, OFF {M['hari_off']})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
