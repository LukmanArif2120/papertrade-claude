"""kaedah_siri.py — ringkasan setiap kaedah untuk helaian kaedah dashboard v161 (keputusan pengguna 8 Nov 2026).

Tiga perkara yang kad skor tidak bawa tetapi helaian kaedah perlukan, semuanya daripada populasi YANG SAMA
seperti kad skor (Lejar Penuh lorong 1, posisi LANGSUNG sahaja `lift_kaedah.langsung` dan tanpa data harga
dikuarantin `kuarantin.topeng_posisi` — pindaan 7 Nov 2026 — terbuka ditanda-ke-pasaran, tolak kos `lift_kaedah.KOS`):

  1. Bagaimana posisi berakhir: henti hari-0 · henti kemudian · sasaran · isyarat jual · had masa · lain
     (delist) · masih terbuka — bilangan dan purata pulangan setiap satu. Henti hari-0 ditakrif SAMA seperti
     `kad_skor.statistik` (G4), supaya bar ini dan G4 tidak boleh bercanggah.
  2. Taburan pulangan setiap posisi dalam baldi tetap `BALDI` (hujung dipotong ke baldi pertama/akhir).
  3. Tiga contoh dagangan SEBENAR yang ditutup — terkini, terbaik, terburuk — dengan lilin harian daripada
     stor harga dan satu garis purata bergerak jika peraturan kaedah menyebutnya (cth `SMA50` bagi M14).
     Contoh bukan bukti; ia menunjukkan bagaimana peraturan berlaku pada data sebenar.

Keluaran: data/analisis/kaedah_siri.json (bentuk {meta…, rows:[…]}; jana_db.py memecahnya kerana ~600 KB).
Dijalankan oleh analisis.yml selepas kad_skor.py. PAPARAN SAHAJA — tiada gate atau status dikira di sini.
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lift_kaedah as lk  # noqa: E402

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KATALOG = os.path.join(BS2, 'standard', 'katalog_kaedah.json')
KELUAR = os.path.join(BS2, 'data', 'analisis', 'kaedah_siri.json')

BALDI = [-20, -15, -10, -6, -4, -2, 0, 2, 4, 6, 10, 15, 20, 30]   # 13 baldi; < -20 dan > 30 dipotong ke hujung
KAT = ('henti0', 'henti', 'sasaran', 'isyarat', 'masa', 'lain', 'terbuka')
SEBAB = {'henti': 'henti', 'sasaran': 'sasaran', 'isyarat keluar': 'isyarat', 'masa': 'masa'}
PRA, PASCA, MAKS_BAR = 10, 3, 30   # bar sebelum beli, selepas keluar, dan had bar carta (lebih = dihimpun)
RE_MA = re.compile(r'\b(sma|ema|ma)\s?(\d{1,3})\b', re.I)


def kategori(P):
    """Kategori akhir setiap posisi (Series). Henti hari-0 = definisi kad_skor.statistik."""
    sb = P.sebab_keluar.fillna('').astype(str)
    k = sb.map(SEBAB).fillna('lain')
    h0 = (~P.terbuka) & (P.tarikh_keluar == P.tarikh_beli.astype(str)) & (sb == 'henti')
    k = k.where(~h0, 'henti0')
    return k.where(~P.terbuka, 'terbuka')


def ma_kaedah(k):
    """('SMA'|'EMA', n) daripada teks peraturan katalog; keluar/pegang dahulu kerana ia menentukan bila jual."""
    if not k:
        return None
    for medan in ('keluar', 'pegang', 'masuk', 'henti'):
        for jenis, n in RE_MA.findall(str(k.get(medan) or '')):
            n = int(n)
            if 2 <= n <= 200:
                return ('EMA' if jenis.lower() == 'ema' else 'SMA'), n
    return None


def bulat(v, d=2):
    if v is None or (isinstance(v, float) and not math.isfinite(v)):
        return None
    return round(float(v), d)


def harga(v):
    return bulat(v, 2 if abs(v) >= 1 else 4)


def taburan(p):
    x = np.clip(np.asarray(p, float), BALDI[0], BALDI[-1] - 1e-9)
    return np.histogram(x, bins=BALDI)[0].astype(int).tolist()


def tetingkap(h, ib, ik, ii):
    """Potong bar sekitar dagangan dan himpun jika terlalu panjang. h = DataFrame bar satu ticker (indeks 0..).
    Pulangkan (bar, ib, ik, ii) dengan indeks dalam tetingkap; bar = [mmdd, o, h, l, c, ma|None]."""
    a = max(0, min(ib, ii if ii is not None else ib) - PRA)
    b = min(len(h), ik + PASCA + 1)
    w = h.iloc[a:b]
    s = max(1, math.ceil(len(w) / MAKS_BAR))
    bar, peta = [], {}
    for j in range(0, len(w), s):
        g = w.iloc[j:j + s]
        for t in range(j, j + len(g)):
            peta[t] = len(bar)
        ma = g['ma'].iloc[-1] if 'ma' in g else None
        bar.append([int(str(g.date.iloc[-1])[4:8]), harga(g.open.iloc[0]), harga(g.high.max()), harga(g.low.min()),
                    harga(g.close.iloc[-1]), None if ma is None or pd.isna(ma) else harga(ma)])
    loc = lambda i: None if i is None or not (a <= i < b) else peta[i - a]  # noqa: E731
    return bar, loc(ib), loc(ik), loc(ii)


def contoh(g):
    """Tiga dagangan ditutup: terkini, terbaik, terburuk (baris DataFrame)."""
    t = g[~g.terbuka]
    if not len(t):
        return []
    t = t.sort_values(['tarikh_keluar', 'tarikh_beli', 'saham'])
    return [('terkini', t.iloc[-1]), ('terbaik', t.loc[t.pul.idxmax()]), ('terburuk', t.loc[t.pul.idxmin()])]


def bar_ticker(tickers):
    f = [os.path.join(lk.STOR, x) for x in ('harga_A.csv', 'harga_B.csv')]
    H = pd.concat([pd.read_csv(x, usecols=['ticker', 'date', 'open', 'high', 'low', 'close'])
                   for x in f if os.path.exists(x)], ignore_index=True)
    H = H[H.ticker.isin(tickers)].copy()
    H['date'] = H.date.astype(str).str.replace('-', '', regex=False)
    return {t: g.sort_values('date').drop_duplicates('date', keep='last').reset_index(drop=True)
            for t, g in H.groupby('ticker')}


def bina_contoh(jenis, r, bars, ma):
    h = bars.get(r.saham)
    if h is None or not len(h):
        return None
    h = h.copy()
    if ma:
        h['ma'] = (h.close.ewm(span=ma[1], adjust=False).mean() if ma[0] == 'EMA'
                   else h.close.rolling(ma[1]).mean())
    d = {x: str(getattr(r, x)).replace('-', '') for x in ('tarikh_isyarat', 'tarikh_beli', 'tarikh_keluar')}
    idx = {v: i for i, v in enumerate(h.date)}
    ib, ik = idx.get(d['tarikh_beli']), idx.get(d['tarikh_keluar'])
    if ib is None or ik is None or ik < ib:
        return None
    ii = idx.get(d['tarikh_isyarat'])
    c, jb, jk, ji = tetingkap(h, ib, ik, ii)
    st = pd.to_numeric(r.henti, errors='coerce')
    return dict(j=jenis, s=r.saham, i=str(r.tarikh_isyarat), b=str(r.tarikh_beli), k=str(r.tarikh_keluar),
                hb=harga(float(r.harga_beli)), hk=harga(float(r.harga_keluar)),
                st=None if pd.isna(st) else harga(float(st)), sb=str(r.sebab_keluar),
                hr=bulat(pd.to_numeric(r.hari, errors='coerce'), 0), p=bulat(r.pul), c=c, ib=jb, ik=jk, ii=ji)


def ringkas(mid, g, bars, ma):
    k = kategori(g)
    kat = [int((k == c).sum()) for c in KAT]
    pk = [bulat(g.pul[k == c].mean()) if n else None for c, n in zip(KAT, kat)]
    p = g.pul.to_numpy(float)
    ex = [e for e in (bina_contoh(j, r, bars, ma) for j, r in contoh(g)) if e]
    return dict(id=mid, n=int(len(g)), kat=kat, pk=pk, h=taburan(p), med=bulat(np.median(p)),
                lo=bulat(p.min()), hi=bulat(p.max()), ma=f'{ma[0]}{ma[1]}' if ma else None, ex=ex)


def populasi(P0):
    """Penyebut kad skor (kad_skor.main): posisi langsung sahaja, tanpa posisi dengan data harga dikuarantin."""
    P = P0[lk.langsung(P0)].copy()
    try:
        import kuarantin as KR
        cemar = KR.topeng_posisi(P).to_numpy()
    except Exception:
        cemar = np.zeros(len(P), bool)
    return P[~cemar].copy()


def main():
    if not os.path.exists(os.path.join(lk.LEJAR, 'terbuka.csv')):
        print('kaedah_siri: lejar/terbuka.csv tiada', file=sys.stderr)
        return 0
    akhir, idx, sesi = lk.harga_akhir()
    P0 = lk.nilai(lk.posisi(), akhir, idx)
    P0['sebab_keluar'] = P0.sebab_keluar.fillna('').astype(str)
    P = populasi(P0)
    kat = json.load(open(KATALOG, encoding='utf-8'))
    kat = {r['id']: r for r in (kat['rows'] if isinstance(kat, dict) else kat)}
    G = dict(tuple(P.groupby('id_kaedah')))
    perlu = {r.saham for g in G.values() for _, r in contoh(g)}
    bars = bar_ticker(perlu)
    rows = [ringkas(mid, g, bars, ma_kaedah(kat.get(mid))) for mid, g in sorted(G.items())]
    akhir_sesi = sesi[-1] if sesi else None
    meta = dict(kini=str(pd.Timestamp.now(tz='UTC').date()),
                harga_pada=f'{akhir_sesi[:4]}-{akhir_sesi[4:6]}-{akhir_sesi[6:]}' if akhir_sesi else None,
                kos=lk.KOS, baldi=BALDI, kat=list(KAT), posisi=int(len(P)), kaedah=len(rows),
                definisi='Lejar Penuh lorong 1, posisi langsung, tanpa data dikuarantin (= penyebut kad skor); terbuka ditanda-ke-pasaran; pulangan tolak kos. Henti hari-0 = '
                          'kad_skor.statistik (G4). Contoh = dagangan ditutup terkini/terbaik/terburuk; lilin '
                          'stor harga, dihimpun jika > %d bar.' % MAKS_BAR)
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    with open(KELUAR, 'w', encoding='utf-8') as f:
        json.dump(dict(meta, rows=rows), f, ensure_ascii=False, separators=(',', ':'))
    sz = os.path.getsize(KELUAR)
    print(f'KAEDAH_SIRI | {len(rows)} kaedah | {len(P)} posisi | {sum(len(r["ex"]) for r in rows)} contoh | {sz:,} bait')
    return 0


if __name__ == '__main__':
    sys.exit(main())
