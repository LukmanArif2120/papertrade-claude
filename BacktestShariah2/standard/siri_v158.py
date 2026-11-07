# siri_v158.py — dua siri baharu untuk dashboard v158 (reka bentuk v5.1, keputusan pengguna 7 Nov 2026):
#
#   prestasi/untung_siri : untung purata SEMUA posisi Papertrade C lawan SPUS tempoh sama, setiap sesi.
#   analisis/t4_siri     : pulangan lorong T4 (L1) setiap kaedah + jalur rawak p50/p95 + SPUS, setiap sesi.
#
# Kenapa "semua posisi", bukan posisi terbuka sahaja: posisi yang rugi keluar dahulu (henti), jadi purata posisi
# terbuka sahaja berat sebelah ke atas. Pada 6 Nov 2026 purata terbuka sahaja ialah +0.16% lawan SPUS −3.57%
# (+3.73 mata) sedangkan purata semua posisi ialah −2.20% lawan −2.55% (+0.34 mata). Yang dijual dinilai pada
# harga jualan; SPUS baginya = buka hari beli hingga buka hari jual (sama dengan cara posisi itu dinilai).
import csv
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
T4_SIRI = os.path.join(BS2, 'portfolio_slot', 't4_siri.csv')
T4_RINGKASAN = os.path.join(BS2, 'portfolio_slot', 't4_ringkasan.csv')


def _n(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v == v else None


def _b(x):
    return str(x).strip().lower() in ('true', '1', 'ya', 'yes')


def _d(t):
    return int(str(t)[:10].replace('-', '')) if t else None


def untung_semua(C, harga, spus, sesi=None):
    """C: baris Papertrade C (dict CSV). harga: {ticker: {YYYYMMDD: tutup}}. spus: {YYYYMMDD: (buka, tutup)}.
    sesi: senarai YYYYMMDD (lalai: tarikh SPUS sejak belian terawal).
    Pulang dict(t, u, s, n): t sesi, u untung purata % semua posisi yang dibeli <= sesi itu, s purata SPUS tempoh sama %,
    n bilangan posisi dalam purata. Posisi tanpa harga pada sesi itu (tiada bar) tidak dikira."""
    pos = []
    for r in C:
        if _b(r.get('tidak_dibeli')) or _b(r.get('tidak_sah')) or _b(r.get('luar_peraturan')):
            continue
        hb, b = _n(r.get('harga_beli')), _d(r.get('tarikh_beli'))
        if not hb or not b:
            continue
        kel = _b(r.get('keluar'))
        e = _d(r.get('tarikh_keluar')) if kel else None
        hk = _n(r.get('harga_keluar')) if kel else None
        pos.append((r.get('saham'), b, e, hb, hk))
    if not pos:
        return dict(t=[], u=[], s=[], n=[])
    mula = min(p[1] for p in pos)
    if sesi is None:
        sesi = sorted(t for t in spus if t >= mula)
    t_out, u_out, s_out, n_out = [], [], [], []
    for d in sesi:
        if d not in spus:
            continue
        a, b_ = [], []
        for s, b, e, hb, hk in pos:
            if b > d or b not in spus:
                continue
            if e is not None and e <= d:
                if hk is None or e not in spus:
                    continue
                a.append(hk / hb - 1)
                b_.append(spus[e][0] / spus[b][0] - 1)
            else:
                c = harga.get(s, {}).get(d)
                if c is None:
                    continue
                a.append(c / hb - 1)
                b_.append(spus[d][1] / spus[b][0] - 1)
        if not a:
            continue
        t_out.append(d)
        u_out.append(round(100 * sum(a) / len(a), 3))
        s_out.append(round(100 * sum(b_) / len(b_), 3))
        n_out.append(len(a))
    return dict(t=t_out, u=u_out, s=s_out, n=n_out)


def t4_siri(spus, siri=T4_SIRI, ringkasan=T4_RINGKASAN, had_bait=None, bait=None):
    """Siri lorong T4 L1 setiap kaedah (pulangan %), jalur rawak p50/p95 dan SPUS (buka sesi pertama -> tutup), setiap sesi.
    pil: [[id, lebih_spus], …] disusun menurun (kaedah lalai dashboard = yang pertama). Jika had_bait diberi dan
    dokumen melebihinya, hanya kaedah teratas ikut lebih_spus dikekalkan (dicatat dalam `dipangkas`)."""
    if not (os.path.exists(siri) and os.path.exists(ringkasan)):
        return None
    W = pd.read_csv(siri, index_col=0)
    if W.empty:
        return None
    t = [str(x)[:10] for x in W.index]
    jal = W[[c for c in W.columns if c.startswith('JALUR')]]
    pct = lambda s: [None if pd.isna(v) else round((float(v) - 1) * 100, 2) for v in s]
    R = pd.read_csv(ringkasan)
    R = R[R.lorong == 'L1'].sort_values('lebih_spus', ascending=False)
    pil = [[r.id, round(float(r.lebih_spus), 2)] for r in R.itertuples() if f'{r.id}|L1' in W.columns and pd.notna(r.lebih_spus)]
    k = {i: pct(W[f'{i}|L1']) for i, _ in pil}
    t0 = _d(t[0])
    s = [round((spus[_d(x)][1] / spus[t0][0] - 1) * 100, 2) if _d(x) in spus and t0 in spus else None for x in t]
    doc = dict(t=t, k=k, p50=pct(jal.quantile(.5, axis=1)) if not jal.empty else [],
               p95=pct(jal.quantile(.95, axis=1)) if not jal.empty else [], spus=s, pil=pil)
    if had_bait and bait:
        n = len(pil)
        while n > 10 and bait(doc) > had_bait:
            n = int(n * 0.75)
            keep = {i for i, _ in pil[:n]}
            doc['k'] = {i: v for i, v in doc['k'].items() if i in keep}
            doc['pil'] = pil[:n]
            doc['dipangkas'] = f'{n} kaedah teratas sahaja (had saiz db)'
    return doc


def harga_tutup(stor, terkini=None, mula=0):
    """{ticker: {YYYYMMDD: tutup}} daripada stor harga (harga_A/B.csv) + terkini.csv (bar terbaharu)."""
    fail = [os.path.join(stor, f) for f in ('harga_A.csv', 'harga_B.csv')] + ([terkini] if terkini else [])
    fr = pd.concat([pd.read_csv(f, usecols=['ticker', 'date', 'close']) for f in fail if os.path.exists(f)])
    fr['date'] = fr.date.astype(int)
    fr = fr[fr.date >= mula].drop_duplicates(['ticker', 'date'], keep='last')
    return {t: dict(zip(g.date, g.close.astype(float))) for t, g in fr.groupby('ticker')}


def baris_csv(folder):
    """Baris Papertrade C daripada papertrade/claude*.csv."""
    import glob
    R = []
    for f in sorted(glob.glob(os.path.join(folder, 'claude*.csv'))):
        with open(f, encoding='utf-8') as h:
            R += list(csv.DictReader(h))
    return R
