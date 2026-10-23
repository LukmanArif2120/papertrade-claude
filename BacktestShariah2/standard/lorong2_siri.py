# lorong2_siri.py — siri harian lorong 2 (pegang selagi naik) bagi carta posisi dashboard: candlestick + paras keluar
# (dokumen db posisi/lorong2, dibahagi oleh jana_db.py). Peraturan sama dengan keluar_lorong.lorong_henti:
# puncak = tutup tertinggi sejak bar beli; paras = max(paras semalam, puncak − GANDA_ATR × ATR14); tutup < paras -> jual buka esok.
# Siri bergantung pada saham + tarikh beli sahaja, jadi posisi kaedah berbeza pada hari sama berkongsi satu siri.
#
#   baris: ["saham|tarikh_beli", [[bbhh, tutup, paras, puncak, status, buka_jual, buka, tinggi, rendah], …]]
#   status: '' sebelum beli | beli | naik | kunci | bawah (tutup < paras) | jual (bar jualan) | lepas (selepas jual lorong 2)
#   Posisi yang sudah tutup kedua-dua lorong: siri hingga tarikh keluar terakhir.
import csv, glob, os

import numpy as np

import keluar_lorong as KL
from trend_status import PT, benar

SEBELUM = 5      # bar sebelum beli (konteks carta)


def _r2(v):
    return None if v is None or not np.isfinite(v) else round(float(v), 2)


def siri(g, tb, sampai=0, sebelum=SEBELUM):
    """g: DataFrame date(int)/open/high/low/close menaik; tb: tarikh beli (int YYYYMMDD); sampai: tarikh akhir (0 = semua)."""
    d = g.date.to_numpy(int)
    k = np.flatnonzero(d == tb)
    if not len(k):
        return None
    k = int(k[0]); o, h, l, c = (g[x].to_numpy(float) for x in ('open', 'high', 'low', 'close'))
    a = KL.atr(h, l, c); out = []; pk = pr = -np.inf; bawah = lepas = False
    for j in range(max(0, k - sebelum), len(c)):
        if sampai and d[j] > sampai:
            break
        md = int(d[j] % 10000); ohl = [_r2(o[j]), _r2(h[j]), _r2(l[j])]
        if lepas:
            out.append([md, _r2(c[j]), None, None, 'lepas', None] + ohl); continue
        if bawah:
            out.append([md, _r2(c[j]), _r2(pr), None, 'jual', _r2(o[j])] + ohl); lepas = True; continue
        st = ''
        if j >= k:
            pk = max(pk, c[j]); npr = max(pr, pk - KL.GANDA_ATR * a[j]) if np.isfinite(a[j]) else pr
            st = 'beli' if j == k else ('naik' if npr > pr + 1e-9 else 'kunci'); pr = npr
            if c[j] < pr:
                st = 'bawah'; bawah = True
        out.append([md, _r2(c[j]), None if j < k else _r2(pr), None if j < k else _r2(pk), st, None] + ohl)
    return out


def posisi(folder=PT):
    """{(saham, tarikh_beli int): sampai int (0 = masih dipegang)} bagi posisi Papertrade C dan Moomoo lama yang sah."""
    P = {}
    for p in glob.glob(os.path.join(folder, 'claude*.csv')) + glob.glob(os.path.join(folder, 'moomoo.csv')):
        with open(p, encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            if benar(r.get('tidak_dibeli')) or benar(r.get('tidak_sah')) or not r.get('tarikh_beli'):
                continue
            key = (r['saham'], int(r['tarikh_beli'].replace('-', '')))
            hingga = 0
            if benar(r.get('tutup_semua')):
                hingga = int(max(r.get('tarikh_keluar') or '', r.get('tarikh_keluar_henti') or '').replace('-', '') or 0)
            P[key] = 0 if key in P and P[key] == 0 else max(P.get(key, -1), hingga) if hingga else 0
    return P


def dokumen(H, folder=PT):
    rows = []
    for (s, tb), hingga in sorted(posisi(folder).items()):
        g = H.get(s)
        x = siri(g, tb, hingga) if g is not None else None
        if x:
            rows.append([f'{s}|{tb // 10000}-{tb // 100 % 100:02d}-{tb % 100:02d}', x])
    return dict(rows=rows, lajur=['bbhh', 'tutup', 'paras', 'puncak', 'status', 'buka_jual', 'buka', 'tinggi', 'rendah'],
                definisi='Lorong 2: paras = max(paras semalam, tutup tertinggi sejak beli − 4 × ATR14); tutup < paras -> jual buka '
                         'esok. Kunci saham|tarikh_beli (dikongsi semua kaedah yang membeli hari itu).')
