"""Carian setup — PAPERTRADE kohort "gred A" (SPEC pindaan 16 Nov 2026 (ae) Bahagian D). Maya; tiada order; BUKAN Lejar.

  python3 cs_hadapan19.py kohort    bina jejak_f2/kohort.json (29 ahli dikunci, takrif daripada registry F)
  python3 cs_hadapan19.py harga --ke DIR                 harga 3 tahun SEMUA saham alam (Yahoo) -> DIR (format stor; tidak dikomit)
  python3 cs_hadapan19.py kalendar --stor DIR --ke F     kalendar laporan Nasdaq semua saham alam, seperti diketahui hari D -> F
  python3 cs_hadapan19.py jejak --stor DIR --kalendar F  tambah isyarat hari harga TERAKHIR ke isyarat.csv; nilai semua ->
                                                         lejar.csv, RINGKASAN.md (alam = semua saham; pindaan (af))
  python3 cs_hadapan19.py jejak     yang sama pada stor harga repo (senarai Shariah; cara lama, untuk ujian sahaja)

Alam (pindaan 17 Nov 2026 (af), keputusan pengguna: tiada tapisan Shariah buat masa ini): `jejak_f2/alam.txt` = 3,260 saham
alam backtest A02; layak = 2,000 paling cair setiap bulan mengikut peraturan universe A02 yang dikira ke hadapan.

Beza daripada penjejak lama (`cs_hadapan.py`, 8 setup): setup di sini memakai prasyarat "laporan kewangan dalam 1-5 sesi",
iaitu maklumat AKAN DATANG. Maka isyarat TIDAK dikira semula daripada awal setiap larian: ia ditulis sekali, pada hari itu,
dengan kalendar laporan seperti yang diketahui hari itu (`isyarat.csv`, tambah-sahaja). Hasil (beli, jual, naik / jatuh)
dikira semula daripada stor harga setiap larian. Isyarat benih M dikira dalam mod tanpa intai (`cs_cari.tanpa_intai`).
"""
import argparse
import csv
import json
import os
import sys
import warnings
from datetime import date, timedelta

import numpy as np
import pandas as pd
from numba import njit

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_hadapan as lama  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_param as kp  # noqa: E402

BS2 = lama.BS2
STOR = lama.STOR
KELUAR = os.path.join(BS2, 'jejak_f2')
PEMANGKIN = os.path.join(BS2, 'data', 'pemangkin')
SPEC = 'kajian/SPEC_CARIAN_SETUP.md pindaan 16 Nov 2026 (ae) Bahagian D + pindaan 17 Nov 2026 (af)'
ALAM = os.path.join(KELUAR, 'alam.txt')                      # 3,260 saham alam backtest A02 (pindaan (af))
# peraturan universe bulanan A02 (AUTOTUNE/SPEC_A02.md §1), dikira ke hadapan
N_ALAM, HARGA_MIN, NILAI_MIN, BAR_MIN, TET_NILAI, TET_SAH = 2000, 10.0, 1e6, 200, 60, 50
LIPUTAN_MIN = 0.9                                            # bahagian saham alam yang mesti ada bar pada hari D
TEMPOH_HARGA = '3y'
KAL_BELAKANG, KAL_HADAPAN = 6, 24                            # tetingkap kalendar Nasdaq sekitar D - 1 (hari)
TEKS_ALAM = {False: 'stor harga repo (senarai Shariah semasa)',
             True: 'semua saham alam backtest (3,260 saham; 2,000 paling cair setiap bulan), BUKAN senarai Shariah sahaja'}
KOS, T20, HAD_B, ATR_STOP = 0.005, 20, 126, 4.0
MIN_BACAAN = 300                                             # belian unik tetingkap lengkap sebelum bacaan dikunci
KW1 = 'KW1'                                                  # kawalan: laporan 1-5 sesi, tiada isyarat beli
L_ISYARAT = ['tarikh_isyarat', 'saham', 'id', 'tarikh_laporan', 'masa_laporan', 'hingga', 'lewat', 'direkod']
L_HARI = ['tarikh', 'lewat', 'isyarat', 'kawalan', 'direkod']
L_ARKIB = ['dilihat', 'saham', 'tarikh_laporan', 'masa']
STATUS = ('TUNGGU_BELI', 'TERBUKA', 'JUAL_ESOK', 'TUTUP')
SEBAB = ('', 'had masa', 'trend tamat', 'stop loss', 'stop loss (harga melompat)', 'stop loss (tutup hari beli)')


# ---------- kalendar sesi NYSE ----------
def _paskah(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    m_ = (32 + 2 * e + 2 * i - h - k) % 7
    n = (a + 11 * h + 22 * m_) // 451
    bulan, hari = divmod(h + m_ - 7 * n + 114, 31)
    return date(y, bulan, hari + 1)


def cuti_nyse(y):
    """Cuti penuh NYSE tahun y mengikut peraturan (penutupan khas tidak termasuk)."""
    def isnin(bulan, ke):                                    # Isnin ke-n; ke = -1: Isnin terakhir
        if ke > 0:
            d = date(y, bulan, 1)
            return d + timedelta(days=(7 - d.weekday()) % 7 + 7 * (ke - 1))
        d = date(y, bulan + 1, 1) - timedelta(days=1)
        return d - timedelta(days=d.weekday())

    def tetap(d, sabtu_ke_jumaat=True):
        if d.weekday() == 5:
            return d - timedelta(days=1) if sabtu_ke_jumaat else None
        return d + timedelta(days=1) if d.weekday() == 6 else d
    nov1 = date(y, 11, 1)
    syukur = nov1 + timedelta(days=(3 - nov1.weekday()) % 7 + 21)
    c = {tetap(date(y, 1, 1), False), isnin(1, 3), isnin(2, 3), _paskah(y) - timedelta(days=2), isnin(5, -1),
         tetap(date(y, 6, 19)), tetap(date(y, 7, 4)), isnin(9, 1), syukur, tetap(date(y, 12, 25))}
    return {d for d in c if d is not None}


_CUTI = {}


def sesi(d):
    if d.weekday() >= 5:
        return False
    if d.year not in _CUTI:
        _CUTI[d.year] = cuti_nyse(d.year)
    return d not in _CUTI[d.year]


def sesi_pada_atau_selepas(d):
    while not sesi(d):
        d += timedelta(days=1)
    return d


def bil_sesi(a, b):
    """Bilangan sesi NYSE selepas a hingga b (termasuk b); 0 jika b <= a."""
    n, d = 0, a
    while d < b:
        d += timedelta(days=1)
        n += sesi(d)
    return n


def _d(x):
    x = int(x)
    return date(x // 10000, x // 100 % 100, x % 100)


def _i(d):
    return d.year * 10000 + d.month * 100 + d.day


# ---------- tarikh laporan seperti diketahui ----------
def muat_kalendar(folder=PEMANGKIN, tambahan=None):
    """(modul kalendar, K = {saham: {tarikh: sumber}}, nas = {saham: {seterusnya, seterusnya_masa, ...}}). tambahan: fail
    kalendar Nasdaq semua saham alam (`tarik_kalendar`); tarikhnya ditambah ke K dan entrinya mengatasi entri repo."""
    sys.path.insert(0, os.path.join(BS2, 'standard'))
    import kalendar_earnings as KE
    p = os.path.join(folder, 'earnings_nasdaq.json')
    nas = (json.load(open(p, encoding='utf-8')).get('saham') or {}) if os.path.exists(p) else {}
    K = KE.muat(folder)
    if tambahan:
        for t, e in (json.load(open(tambahan, encoding='utf-8')).get('saham') or {}).items():
            for k in ('lalu', 'seterusnya'):
                try:
                    K.setdefault(t, {}).setdefault(date.fromisoformat(str(e.get(k))[:10]), 'Nasdaq')
                except ValueError:
                    pass
            nas[t] = e
    return KE, K, nas


def baca(fail, lajur):
    p = os.path.join(KELUAR, fail) if not os.path.isabs(fail) else fail
    if not os.path.exists(p):
        return pd.DataFrame(columns=lajur)
    return pd.read_csv(p, dtype=str).fillna('')


def tambah(p, lajur, baris):
    """Tambah baris ke hujung fail (tidak pernah menulis semula baris sedia ada)."""
    if not baris:
        return
    baru = not os.path.exists(p)
    with open(p, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=lajur)
        if baru:
            w.writeheader()
        for b in baris:
            w.writerow({k: b.get(k, '') for k in lajur})


def tindak_balas(KE, K, nas, arkib, t, D):
    """Laporan seterusnya bagi saham t seperti diketahui selepas tutup hari D -> (tarikh laporan, masa, sesi tindak balas)
    atau None. Sesi tindak balas = hari laporan (atau sesi berikutnya jika bukan hari dagangan), atau sesi SELEPAS hari
    laporan jika masa = selepas tutup. Laporan pada hari D sendiri hanya dikira jika selepas tutup."""
    def masa(R):
        e = nas.get(t) or {}
        if e.get('seterusnya') == R.isoformat():
            return e.get('seterusnya_masa') or ''
        return arkib.get((t, R.isoformat()), '')
    R, _ = KE.seterusnya(K, t, D)
    if R is not None and R == D and masa(R) != 'time-after-hours':
        R, _ = KE.seterusnya(K, t, D + timedelta(days=1))
    if R is None:
        return None
    m = masa(R)
    tb = sesi_pada_atau_selepas(R + timedelta(days=1)) if m == 'time-after-hours' else sesi_pada_atau_selepas(R)
    return R, m, tb


# ---------- alam semua saham (pindaan (af)) ----------
def baca_alam(p=None):
    return sorted({x.strip().upper() for x in open(p or ALAM, encoding='utf-8') if x.strip()})


def topeng_bulanan(fr, kal):
    """dict saham -> ndarray bool sejajar bar: True jika saham itu ahli universe bulan bar tersebut. Peraturan A02 dikira ke
    hadapan: pada hari dagangan terakhir bulan m -- tutup > USD 10, median 60 hari (tutup x volum) >= USD 1 juta dengan >= 50
    bar sah, >= 200 bar; 2,000 teratas ikut median; berkuat kuasa bulan m + 1. kal = kalendar sesi (DatetimeIndex)."""
    tick = sorted(fr)
    kal = pd.DatetimeIndex(kal).sort_values()
    c = pd.DataFrame({t: fr[t].close for t in tick}).reindex(kal).to_numpy(float)
    dv = c * pd.DataFrame({t: fr[t].volume for t in tick}).reindex(kal).to_numpy(float)
    bar = np.cumsum(~np.isnan(c), axis=0)
    per = kal.to_period('M')
    ahli = {}
    for p in np.flatnonzero(np.append(per[1:] != per[:-1], True)):
        win = dv[max(0, p - TET_NILAI + 1):p + 1]
        sah = (~np.isnan(win)).sum(axis=0)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            med = np.nanmedian(win, axis=0)
        with np.errstate(invalid='ignore'):
            ok = (c[p] > HARGA_MIN) & (med >= NILAI_MIN) & (bar[p] >= BAR_MIN) & (sah >= TET_SAH)
        ix = np.flatnonzero(ok)
        b = per[p] + 1
        ahli[b.year * 100 + b.month] = set(ix[np.argsort(-med[ix], kind='stable')][:N_ALAM].tolist())
    out = {}
    for j, t in enumerate(tick):
        ym = np.asarray(fr[t].index.year * 100 + fr[t].index.month)
        out[t] = np.isin(ym, [b for b, a in ahli.items() if j in a])
    return out


def _sesi_stor(stor):
    return int(pd.read_csv(os.path.join(stor, 'harga_idx.csv'), usecols=['date']).date.max())


def tarik_harga(ke, alam=None, rujukan=STOR, tarik=None):
    """Harga 3 tahun semua saham alam + SPY / QQQ (Yahoo, konvensyen stor) -> folder `ke` dalam format stor. Bar selepas
    sesi terakhir stor repo (`rujukan`) dibuang. Gagal (SystemExit) jika < LIPUTAN_MIN saham alam ada bar pada hari itu."""
    sys.path.insert(0, os.path.join(BS2, 'standard'))
    import harga_yf as H
    tarik = tarik or H.muat_turun
    tk = baca_alam(alam)
    D = _sesi_stor(rujukan)
    d, gagal = tarik(tk + list(H.IDX), period=TEMPOH_HARGA)
    if gagal:                                                    # cubaan kedua bagi yang tiada data (had kadar Yahoo)
        d2, gagal = tarik(sorted(gagal), period=TEMPOH_HARGA)
        d = pd.concat([d, d2], ignore_index=True)
    d = d[d.date <= D].drop_duplicates(['ticker', 'date']).sort_values(['ticker', 'date'])
    ix = d[d.ticker.isin(H.IDX)]
    s = d[d.ticker.isin(set(tk))]
    ada = int(s[s.date == D].ticker.nunique())
    os.makedirs(ke, exist_ok=True)
    L = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
    s[L].to_csv(os.path.join(ke, 'harga_A.csv'), index=False, float_format='%.6g')
    s.iloc[:0][L].to_csv(os.path.join(ke, 'harga_B.csv'), index=False)
    ix[L].to_csv(os.path.join(ke, 'harga_idx.csv'), index=False, float_format='%.6g')
    st = dict(dijana=pd.Timestamp.now('UTC').strftime('%Y-%m-%d %H:%M UTC'), sesi=D, alam=len(tk), ada_data=int(s.ticker.nunique()),
              ada_sesi=ada, tiada_data=sorted(set(tk) - set(s.ticker))[:200])
    json.dump(st, open(os.path.join(ke, 'status.json'), 'w'), indent=1)
    print(f"harga semua saham: sesi {D}; {st['ada_data']} daripada {len(tk)} ada data; {ada} ada bar sesi itu")
    if set(ix[ix.date == D].ticker) != set(H.IDX):
        raise SystemExit(f'harga semua saham: SPY / QQQ tiada bar sesi {D}')
    if ada < LIPUTAN_MIN * len(tk):
        raise SystemExit(f'harga semua saham: liputan {ada} / {len(tk)} < {LIPUTAN_MIN:.0%}; tiada isyarat ditulis')
    return st


def tarik_kalendar(stor, ke, alam=None, tarik=None):
    """Kalendar laporan Nasdaq bagi semua saham alam seperti diketahui sekarang, rujukan D - 1 hari (D = sesi terakhir
    `stor`): `seterusnya` = laporan terawal pada / selepas D. Gagal (SystemExit) jika mana-mana hari tetingkap ralat."""
    sys.path.insert(0, os.path.join(BS2, 'standard'))
    if tarik is None:
        import pemangkin_actions as PA
        tarik = PA.tarik_nasdaq
    D = _d(_sesi_stor(stor))
    nas = tarik(D - timedelta(days=1), simpan=set(baca_alam(alam)), ke_belakang=KAL_BELAKANG, ke_hadapan=KAL_HADAPAN)
    nas = dict(dijana=pd.Timestamp.now('UTC').strftime('%Y-%m-%d %H:%M UTC'), sesi=_i(D), **nas)
    json.dump(nas, open(ke, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"kalendar semua saham: sesi {_i(D)}; {len(nas.get('saham') or {})} saham; hari ralat {nas.get('hari_ralat')}")
    if nas.get('hari_ralat') or not nas.get('saham'):
        raise SystemExit(f"kalendar semua saham: tidak lengkap ({nas.get('hari_ralat')} hari ralat); tiada isyarat ditulis")
    return nas


# ---------- kohort ----------
def bina_kohort():
    import cs_audit19 as a19
    reg = pd.read_csv(os.path.join(BS2, 'data', 'registry_F.csv'), dtype=str).fillna('').set_index('id')
    U = pd.read_csv(os.path.join(SINI, 'hasil', 'CS13', 'senarai_utama.csv')).set_index('id')
    kq1, kq2 = [x[:4] for x in lapis.PASARAN], [x[:4] for x in lapis.KUMPULAN]
    grid = {n: (fam, p) for n, fam, p in kp.grid()}
    ahli = []
    for i in a19.KOHORT:
        b = reg.loc[i, 'takrif'].split('|')
        assert b[2] == 'G6' and b[3] == 'PB', (i, b)             # stop loss 4xATR14 + cara pegang B
        q = b[4].split('+')
        assert 'QF01' in q and all(k in kq1 or k in kq2 for k in q), (i, q)
        a = dict(id=i, takrif=reg.loc[i, 'takrif'], pencetus=b[0], fs=[int(x[1:]) - 1 for x in b[1].split('+') if x],
                 pasaran=[k for k in q if k in kq1], syarikat=[k for k in q if k in kq2],
                 teks_prasyarat=str(U.loc[i, 'prasyarat']), teks_isyarat=str(U.loc[i, 'nama']),
                 teks_penapis='' if U.loc[i, 'penapis'] != U.loc[i, 'penapis'] else str(U.loc[i, 'penapis']))
        if b[0][0] == 'K':
            a.update(jenis='K', keluarga=grid[b[0]][0], param=grid[b[0]][1])
        elif b[0][0] in 'MN':
            _, modul, P = a19.tugas_benih([b[0]])[0]
            a.update(jenis='benih', modul=modul, param=P)
        else:
            a.update(jenis='P')
        ahli.append(a)
    os.makedirs(KELUAR, exist_ok=True)
    json.dump({'spec': SPEC, 'alam': TEKS_ALAM[True], 'kawalan': KW1, 'stop': '4xATR14', 'ahli': ahli}, open(os.path.join(KELUAR, 'kohort.json'), 'w'),
              indent=1, ensure_ascii=False)
    print(f'kohort: {len(ahli)} ahli ->', os.path.join(KELUAR, 'kohort.json'))


# ---------- panel stor + prasyarat pasaran ----------
def panel(fr, idx, topeng=None):
    """topeng (dict saham -> bool setiap bar, `topeng_bulanan`): alam semua saham -- layak = >= 252 bar DAN ahli universe
    bulan itu (seperti backtest). Tanpa topeng: cara lama (stor Shariah; tutup >= USD 10 dan nilai dagangan >= USD 1 juta)."""
    pan = atom.bina(fr, idx, 'hadapan' if topeng is None else 'alam', topeng)
    hu = np.unique(pan['tarikh'])
    pan['hari'], pan['hari_unik'] = np.searchsorted(hu, pan['tarikh']), hu
    pan['akhir'] = pan['mula'][pan['tid'] + 1]
    pan['calon'] = pan['layak'] & (pan['atr'] > 0)
    c, tid = pan['c'], pan['tid']
    S = np.concatenate([[0.0], np.cumsum(c)])
    i = np.arange(len(c))
    for n in (20, 50):
        ok = (i - n + 1) >= pan['mula'][tid]
        pan[f'sma{n}'] = np.where(ok, (S[i + 1] - S[np.maximum(i + 1 - n, 0)]) / n, np.nan)
    return pan


def pasaran_stor(pan, idx):
    """dict kod prasyarat pasaran -> ndarray bool setiap HARI (formula enjin; QQQ / SPY dan keluasan daripada stor)."""
    import cs_prasyarat as pr
    hu, ly = pan['hari_unik'], pan['layak']
    L = pd.DataFrame({'date': pan['tarikh'][ly], 'b50': pan['F'][1][ly] > 0, 'b200': pan['F'][2][ly] > 0,
                      'b5': pan['F'][18][ly] > 0}).groupby('date').mean()
    ke_int = lambda g: g.set_axis((g.index.year * 10000 + g.index.month * 100 + g.index.day).to_numpy())
    q, s = ke_int(idx['QQQ']), ke_int(idx['SPY'])
    PM = {'Q' + k: v for k, v in pr.pasaran(hu, L, q=q.close, s=s.close).items()}
    PM.update(lapis.pakar(q[['low', 'close', 'volume']].reindex(hu).ffill(), s[['low', 'close', 'volume']].reindex(hu).ffill(),
                          lapis.harian_saham({'S': pan}, hu)))
    return {k: np.asarray(v.reindex(hu).fillna(False), bool) for k, v in PM.items()}


def pencetus_semua(pan, fr, idx, ahli):
    """dict nama pencetus -> ndarray bool setiap bar (hari PERTAMA isyarat)."""
    warnings.filterwarnings('ignore')
    tick, out = sorted(fr), {}
    perlu_k = sorted({a['pencetus'] for a in ahli if a['jenis'] == 'K'})
    if perlu_k:
        G = [g for g in kp.grid() if g[0] in perlu_k]
        px = pd.DataFrame({t: fr[t].close for t in tick})
        RS = (px / px.shift(126) - 1).rank(axis=1, pct=True) * 100
        M = np.concatenate([kp.kira(fr[t], RS[t].reindex(fr[t].index), G) for t in tick], axis=1)
        for j, g in enumerate(G):
            out[g[0]] = atom.mula_isyarat(M[j], pan['mula'])
    for a in ahli:
        pc = a['pencetus']
        if pc in out:
            continue
        if a['jenis'] == 'P':
            out[pc] = atom.mula_isyarat(pan['P'][pc], pan['mula'])
        elif a['jenis'] == 'benih':
            cari._KAUSAL = True                                  # mod tanpa intai (pindaan (ae) Bahagian C)
            try:
                out[pc] = atom.mula_isyarat(lama.isyarat_modul(fr, idx, pc, a['modul'], a['param']), pan['mula'])
            finally:
                cari._KAUSAL = False
    return out


# ---------- mekanik (tetingkap belum tentu lengkap) ----------
@njit(cache=True)
def simulasi(ix, akhir, o, l, c, atr, sma, had):
    """Setiap isyarat bar ix[k]: beli buka esok; stop loss = harga beli - 4xATR14 hari isyarat; mulai tutup sesi ke-20 jual
    pada buka esok selepas tutup < purata (sma); had = bilangan sesi paling lama (0 = tiada had). Dagangan belum ditutup
    dinilai pada tutup terkini. Pulangkan status (0 tunggu beli, 1 terbuka, 2 jual esok, 3 tutup), sebab (indeks SEBAB),
    bar keluar, harga keluar / terkini, sesi, R (selepas kos)."""
    n = ix.shape[0]
    st, sb, bk = np.zeros(n, np.int64), np.zeros(n, np.int64), np.full(n, -1, np.int64)
    hk, ss, R = np.full(n, np.nan), np.zeros(n, np.int64), np.full(n, np.nan)
    for k in range(n):
        i = ix[k]
        e, z = i + 1, akhir[k]
        if e >= z:
            continue
        P = o[e]
        Ls = P - ATR_STOP * atr[i]
        d = 0
        while True:
            b = e + d
            if b >= z:                                           # data habis: masih dipegang
                st[k], hk[k], ss[k], R[k] = 1, c[z - 1], d, c[z - 1] / P - 1.0 - KOS
                if d == 1 and c[e] <= Ls:
                    st[k], sb[k] = 2, 5
                elif d >= T20 and c[z - 1] < sma[z - 1]:
                    st[k], sb[k] = 2, 2
                break
            if d >= 1:
                if d == 1 and c[e] <= Ls:
                    st[k], sb[k], bk[k], hk[k], ss[k] = 3, 5, b, o[b], d
                elif d >= T20 and c[b - 1] < sma[b - 1]:
                    st[k], sb[k], bk[k], hk[k], ss[k] = 3, 2, b, o[b], d
                elif o[b] <= Ls:
                    st[k], sb[k], bk[k], hk[k], ss[k] = 3, 4, b, o[b], d
                elif l[b] <= Ls:
                    st[k], sb[k], bk[k], hk[k], ss[k] = 3, 3, b, Ls, d
                if st[k] == 3:
                    R[k] = hk[k] / P - 1.0 - KOS
                    break
            if had > 0 and d == had - 1:
                st[k], sb[k], bk[k], hk[k], ss[k], R[k] = 3, 1, b, c[b], d, c[b] / P - 1.0 - KOS
                break
            d += 1
    return st, sb, bk, hk, ss, R


@njit(cache=True)
def label(ix, akhir, o, l, c):
    """[m5, j5, terus] bagi setiap isyarat; NaN jika tetingkap belum lengkap (m5 / j5 perlu 5 sesi; terus perlu 20)."""
    out = np.full((ix.shape[0], 3), np.nan)
    for k in range(ix.shape[0]):
        e, z = ix[k] + 1, akhir[k]
        if e + 4 >= z:
            continue
        P = o[e]
        c5 = c[e + 4]
        out[k, 0], out[k, 1] = c5 >= P * 1.05, c5 <= P * 0.95
        if e + T20 - 1 >= z:
            continue
        h8 = c[e] <= P * 0.92
        for d in range(1, T20):
            if o[e + d] <= P * 0.92 or l[e + d] <= P * 0.92:
                h8 = True
        out[k, 2] = out[k, 0] == 1.0 and c[e + T20 - 1] > c5 and not h8
    return out


def nilai_bar(pan, ix):
    """DataFrame hasil bagi senarai bar isyarat (kedua-dua cara pegang + label)."""
    ix = np.ascontiguousarray(ix, dtype=np.int64)
    z = pan['akhir'][ix].astype(np.int64)
    a = (pan['o'], pan['l'], pan['c'], pan['atr'])
    Lb = label(ix, z, pan['o'], pan['l'], pan['c'])
    d = {'bar': ix, 'm5': Lb[:, 0], 'j5': Lb[:, 1], 'terus': Lb[:, 2]}
    for nm, sma, had in (('B', pan['sma20'], HAD_B), ('50', pan['sma50'], 0)):
        st, sb, bk, hk, ss, R = simulasi(ix, z, *a, sma, had)
        d.update({f'st_{nm}': st, f'sb_{nm}': sb, f'bk_{nm}': bk, f'hk_{nm}': hk, f'ss_{nm}': ss, f'R_{nm}': R})
    return pd.DataFrame(d)


def asas_hari(pan, hari):
    """Asas "saham rawak hari sama x tercile ATR %" bagi setiap hari isyarat: purata label dan hasil kedua-dua cara pegang
    antara SEMUA saham layak hari itu. Pulangkan DataFrame berindeks (hari, tercile) + tercile setiap bar layak."""
    m = pan['calon'] & np.isin(pan['hari'], hari)
    ix = np.flatnonzero(m)
    if not len(ix):
        return pd.DataFrame(), {}
    V = nilai_bar(pan, ix)
    V['hari'] = pan['hari'][ix]
    V['terc'] = np.minimum((pd.Series(pan['atr'][ix] / pan['c'][ix]).groupby(V.hari.to_numpy()).rank(pct=True) * 3).astype(int), 2).to_numpy()
    for nm in ('B', '50'):
        V[f'W_{nm}'] = np.where(V[f'st_{nm}'] > 0, (V[f'R_{nm}'] > 0).astype(float), np.nan)
    A = V.groupby(['hari', 'terc'])[['m5', 'j5', 'terus', 'R_B', 'W_B', 'R_50', 'W_50']].mean()
    return A, dict(zip(ix.tolist(), V.terc.tolist()))


# ---------- larian harian ----------
def isyarat_hari(pan, PM, PC, K3, ahli, h, sudah=()):
    """Isyarat hari ke-h (indeks hari): senarai (saham, id, tarikh laporan, masa, hingga) -- setup dan kawalan KW1.
    sudah: set (saham, tarikh laporan) yang kawalannya sudah direkod (kawalan = SATU baris setiap saham setiap laporan,
    iaitu hari pertama ia masuk tetingkap 1-5 sesi; sama dengan peraturan satu posisi)."""
    KE, K, nas, arkib = K3
    D = _d(pan['hari_unik'][h])
    bar = np.flatnonzero((pan['hari'] == h) & pan['calon'])
    tk = pan['ticker'][pan['tid'][bar]]
    lap = {}
    for t in tk:
        x = tindak_balas(KE, K, nas, arkib, t, D)
        if x is not None:
            hg = bil_sesi(D, x[2])
            if 1 <= hg <= 5:
                lap[t] = (x[0].isoformat(), x[1], hg)
    out = [(t, KW1) + lap[t] for t in tk if t in lap and (t, lap[t][0]) not in sudah]
    for a in ahli:
        if not all(PM[k][h] for k in a['pasaran']):
            continue
        m = PC[a['pencetus']][bar].copy()
        for f in a['fs']:
            m &= pan['F'][f][bar] > 0
        out += [(t, a['id']) + lap[t] for t in tk[m] if t in lap]
    return out


def kemas_arkib(nas, D, direkod):
    """Tambah ke kalendar_dilihat.csv tarikh laporan yang dilihat hari ini (hanya yang dekat dan belum direkod sama)."""
    A = baca('kalendar_dilihat.csv', L_ARKIB)
    akhir = {(r.saham, r.tarikh_laporan): r.masa for r in A.itertuples()}
    baris = []
    for t, e in sorted(nas.items()):
        R = e.get('seterusnya')
        if not R:
            continue
        try:
            jarak = (date.fromisoformat(R) - D).days
        except ValueError:
            continue
        m = e.get('seterusnya_masa') or ''
        if -1 <= jarak <= 14 and akhir.get((t, R)) != m:
            baris.append(dict(dilihat=_i(D), saham=t, tarikh_laporan=R, masa=m))
    tambah(os.path.join(KELUAR, 'kalendar_dilihat.csv'), L_ARKIB, baris)
    akhir.update({(b['saham'], b['tarikh_laporan']): b['masa'] for b in baris})
    return akhir


def jejak(stor=STOR, keluar=None, pemangkin=PEMANGKIN, direkod=None, kalendar=None, semua=False, alam=None):
    """semua=True (pindaan (af)): `stor` = folder `tarik_harga` (semua saham alam), `kalendar` = fail `tarik_kalendar`."""
    global KELUAR
    if keluar:
        KELUAR = keluar
    warnings.filterwarnings('ignore')
    Kh = json.load(open(os.path.join(KELUAR, 'kohort.json'), encoding='utf-8'))
    ahli = Kh['ahli']
    fr, idx = lama.muat_stor(stor)
    topeng = None
    if semua:
        dalam = set(baca_alam(alam))
        fr = {t: g for t, g in fr.items() if t in dalam}
        topeng = topeng_bulanan(fr, idx['SPY'].index)
    pan = panel(fr, idx, topeng)
    hu = pan['hari_unik']
    PM, PC = pasaran_stor(pan, idx), pencetus_semua(pan, fr, idx, ahli)
    KE, K, nas = muat_kalendar(pemangkin, kalendar)
    direkod = direkod or pd.Timestamp.now('UTC').strftime('%Y-%m-%d %H:%M')
    H = baca('hari.csv', L_HARI)
    siap = set(H.tarikh.astype(int)) if len(H) else set()
    akhir_h = len(hu) - 1
    mula_h = akhir_h if not siap else int(np.searchsorted(hu, max(siap), 'right'))      # larian pertama: hari terakhir sahaja
    arkib = kemas_arkib(nas, _d(hu[akhir_h]), direkod)
    S0 = baca('isyarat.csv', L_ISYARAT)
    sudah = set(zip(S0[S0.id == KW1].saham, S0[S0.id == KW1].tarikh_laporan)) if len(S0) else set()
    for h in range(mula_h, akhir_h + 1):
        lewat = int(h < akhir_h)
        S = isyarat_hari(pan, PM, PC, (KE, K, nas, arkib), ahli, h, sudah)
        sudah |= {(t, R) for t, i, R, m, hg in S if i == KW1}
        tambah(os.path.join(KELUAR, 'isyarat.csv'), L_ISYARAT,
               [dict(tarikh_isyarat=int(hu[h]), saham=t, id=i, tarikh_laporan=R, masa_laporan=m, hingga=hg, lewat=lewat, direkod=direkod)
                for t, i, R, m, hg in S])
        tambah(os.path.join(KELUAR, 'hari.csv'), L_HARI,
               [dict(tarikh=int(hu[h]), lewat=lewat, isyarat=sum(1 for x in S if x[1] != KW1), kawalan=sum(1 for x in S if x[1] == KW1),
                     direkod=direkod)])
    L = nilai(pan)
    p_st = os.path.join(stor, 'status.json')
    st = json.load(open(p_st)) if semua and os.path.exists(p_st) else {}
    layak = int((pan['calon'] & (pan['hari'] == akhir_h)).sum())
    lapor(pan, PM, Kh, L, TEKS_ALAM[bool(semua)] + f'; saham layak hari ini: {layak}'
          + (f"; harga diperoleh bagi {st['ada_sesi']} daripada {st['alam']} saham" if st else ''))
    print(f"papertrade gred A ({'semua saham' if semua else 'stor Shariah'}; layak {layak}): harga hingga {int(hu[-1])}; hari diproses {len(baca('hari.csv', L_HARI))}; "
          f"isyarat {int((L.id != KW1).sum()) if len(L) else 0}; kawalan {int((L.id == KW1).sum()) if len(L) else 0}")


def nilai(pan):
    """Nilai SEMUA baris isyarat.csv daripada stor harga -> lejar.csv (dijana semula sepenuhnya; log isyarat tidak disentuh)."""
    S = baca('isyarat.csv', L_ISYARAT)
    lajur = ['id', 'saham', 'tarikh_isyarat', 'lewat', 'tarikh_laporan', 'hingga', 'diambil', 'tarikh_beli', 'harga_beli', 'stop',
             'm5', 'j5', 'terus', 'a_m5', 'a_j5', 'a_terus']
    for nm in ('B', '50'):
        lajur += [f'status_{nm}', f'sebab_{nm}', f'tarikh_jual_{nm}', f'harga_jual_{nm}', f'sesi_{nm}', f'untung_{nm}', f'a_menang_{nm}',
                  f'a_untung_{nm}']
    lajur.append('harga_terkini')
    if not len(S):
        pd.DataFrame(columns=lajur).to_csv(os.path.join(KELUAR, 'lejar.csv'), index=False)
        return pd.DataFrame(columns=lajur)
    tid = {t: j for j, t in enumerate(pan['ticker'])}
    hari = {int(d): j for j, d in enumerate(pan['hari_unik'])}
    S['d'] = S.tarikh_isyarat.astype(int)
    S = S.sort_values(['id', 'saham', 'd'], kind='stable').reset_index(drop=True)
    bar = np.full(len(S), -1, np.int64)
    for k, r in enumerate(S.itertuples()):
        if r.saham in tid and r.d in hari:
            a, b = pan['mula'][tid[r.saham]], pan['mula'][tid[r.saham] + 1]
            j = a + np.searchsorted(pan['tarikh'][a:b], r.d)
            if j < b and pan['tarikh'][j] == r.d:
                bar[k] = j
    ada = bar >= 0
    V = nilai_bar(pan, bar[ada])
    V.index = np.flatnonzero(ada)
    A, terc = asas_hari(pan, sorted({pan['hari'][b] for b in bar[ada]}))
    out, t_akhir, b_akhir = [], None, -1
    for k, r in enumerate(S.itertuples()):
        d = dict.fromkeys(lajur, '')
        d.update(id=r.id, saham=r.saham, tarikh_isyarat=r.d, lewat=r.lewat, tarikh_laporan=r.tarikh_laporan, hingga=r.hingga, diambil=0)
        if not ada[k]:
            d['status_B'] = d['status_50'] = 'TIADA_DATA'
            out.append(d)
            continue
        v, i = V.loc[k], int(bar[k])
        if (r.id, r.saham) == t_akhir and i <= b_akhir:              # satu posisi setiap (setup, saham), ikut cara pegang B
            out.append(d)
            continue
        t_akhir = (r.id, r.saham)
        b_akhir = int(v.bk_B) if v.st_B == 3 else 10 ** 12
        d['diambil'] = 1
        e = i + 1
        if v.st_B > 0:
            P = float(pan['o'][e])
            d.update(tarikh_beli=int(pan['tarikh'][e]), harga_beli=round(P, 4), stop=round(P - ATR_STOP * float(pan['atr'][i]), 4),
                     harga_terkini=round(float(pan['c'][pan['akhir'][i] - 1]), 4))
            kunci = (int(pan['hari'][i]), int(terc.get(i, -1)))
            a = A.loc[kunci] if len(A) and kunci in A.index else None
            for nm in ('m5', 'j5', 'terus'):
                if v[nm] == v[nm]:
                    d[nm] = int(v[nm])
                    if a is not None and a[nm] == a[nm]:
                        d['a_' + nm] = round(float(a[nm]), 4)
        for nm in ('B', '50'):
            st = int(v[f'st_{nm}'])
            d[f'status_{nm}'] = STATUS[st]
            if st == 0:
                continue
            d.update({f'sebab_{nm}': SEBAB[int(v[f'sb_{nm}'])], f'sesi_{nm}': int(v[f'ss_{nm}']), f'untung_{nm}': round(float(v[f'R_{nm}']) * 100, 2)})
            if st == 3:
                d.update({f'tarikh_jual_{nm}': int(pan['tarikh'][int(v[f'bk_{nm}'])]), f'harga_jual_{nm}': round(float(v[f'hk_{nm}']), 4)})
            if a is not None and a[f'W_{nm}'] == a[f'W_{nm}']:
                d.update({f'a_menang_{nm}': round(float(a[f'W_{nm}']), 4), f'a_untung_{nm}': round(float(a[f'R_{nm}']) * 100, 2)})
        out.append(d)
    L = pd.DataFrame(out, columns=lajur).sort_values(['tarikh_isyarat', 'id', 'saham'], kind='stable').reset_index(drop=True)
    L.to_csv(os.path.join(KELUAR, 'lejar.csv'), index=False)
    return L


def ringkas(g):
    """Ukuran pindaan (ae) Bahagian D bagi satu kumpulan baris lejar (isyarat tidak lewat, diambil)."""
    f = lambda s: pd.to_numeric(s, errors='coerce')
    g = g[(g.diambil.astype(str) == '1') & (g.lewat.astype(str) == '0')]
    lk = g[f(g.terus).notna()]
    o = dict(belian=len(g), terbuka=int(g.status_B.isin(['TERBUKA', 'JUAL_ESOK', 'TUNGGU_BELI']).sum()), lengkap=len(lk))
    for nm in ('m5', 'j5', 'terus'):
        o[nm], o['a_' + nm] = f(lk[nm]).mean(), f(lk['a_' + nm]).mean()
    o['arah'] = (o['m5'] - o['a_m5']) - (o['j5'] - o['a_j5']) if len(lk) else np.nan
    for nm in ('B', '50'):
        u = f(lk[f'untung_{nm}'])
        o[f'menang_{nm}'], o[f'a_menang_{nm}'] = (u > 0).mean() if len(lk) else np.nan, f(lk[f'a_menang_{nm}']).mean()
        o[f'untung_{nm}'], o[f'a_untung_{nm}'] = u.mean(), f(lk[f'a_untung_{nm}']).mean()
    return o


def unik(L):
    """Belian unik kohort: satu baris setiap (saham, hari isyarat), tanpa kawalan."""
    return L[(L.id != KW1) & (L.diambil.astype(str) == '1')].drop_duplicates(['saham', 'tarikh_isyarat'])


def lapor(pan, PM, Kh, L, alam_teks=TEKS_ALAM[False]):
    try:
        sys.path.insert(0, os.path.join(BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    hu = pan['hari_unik']
    D = int(hu[-1])
    H = baca('hari.csv', L_HARI)
    p = lambda v, d=0: '–' if v != v else f'{v * 100:.{d}f}'
    u = lambda v: '–' if v != v else f'{v:+.1f}'
    semua_q = sorted({k for a in Kh['ahli'] for k in a['pasaran']})
    nama_q = {x[:4]: x[5:] for x in lapis.PASARAN}
    aktif = [a['id'] for a in Kh['ahli'] if all(PM[k][-1] for k in a['pasaran'])]
    hari_ini = L[L.tarikh_isyarat.astype(str) == str(D)] if len(L) else L
    beli = hari_ini[(hari_ini.id != KW1) & (hari_ini.status_B == 'TUNGGU_BELI')] if len(L) else L
    A = ['# Papertrade setup F gred A (maya; BUKAN keputusan wang sebenar)', '', status, '',
         f'Dijana `kajian/carian_setup/cs_hadapan19.py`; harga hingga {D}. Peraturan: `{SPEC}`. Tiada order. **Jangan sunting.**', '',
         '## Hari ini', '',
         f"- Hari diproses: {len(H)} (mula {H.tarikh.astype(int).min() if len(H) else '–'}); terlepas dan diisi lewat: "
         f"{int((H.lewat.astype(str) == '1').sum()) if len(H) else 0}.",
         f"- Setup yang syarat pasarannya benar hari ini: {len(aktif)} daripada {len(Kh['ahli'])}"
         + (f" ({', '.join(f'`{x}`' for x in aktif)})." if aktif else '.'),
         '- Syarat pasaran: ' + '; '.join(f"{nama_q.get(k, k)} = {'YA' if PM[k][-1] else 'tidak'}" for k in semua_q) + '.',
         f"- Saham layak yang laporannya dalam 1–5 sesi: {int((hari_ini.id == KW1).sum()) if len(L) else 0}.", '',
         '## Belian esok (isyarat hari ini; beli pada harga buka sesi berikutnya)', '']
    if len(beli):
        A += ['| Saham | Setup | Tarikh laporan | Sesi lagi |', '|---|---|---|---|']
        for t, g in beli.groupby('saham'):
            A.append(f"| {t} | {', '.join(f'`{x}`' for x in g.id)} | {g.tarikh_laporan.iloc[0]} | {g.hingga.iloc[0]} |")
    else:
        A.append('Tiada.')
    A += ['', '## Hasil setakat ini (isyarat tidak lewat; kurungan = saham rawak hari sama, dipegang cara sama)', '',
          '| Kumpulan | Belian | Belum ditutup | Tetingkap 20 sesi lengkap | Tangkap % | Naik ≥ 5 % | Jatuh ≥ 5 % | Menang % cara B | Purata % cara B | '
          'Menang % cara 50 | Purata % cara 50 |', '|---' * 11 + '|']

    def baris(nama, g):
        o = ringkas(g)
        return (f"| {nama} | {o['belian']} | {o['terbuka']} | {o['lengkap']} | {p(o['terus'])} ({p(o['a_terus'])}) | {p(o['m5'])} ({p(o['a_m5'])}) | "
                f"{p(o['j5'])} ({p(o['a_j5'])}) | {p(o['menang_B'])} ({p(o['a_menang_B'])}) | {u(o['untung_B'])} ({u(o['a_untung_B'])}) | "
                f"{p(o['menang_50'])} ({p(o['a_menang_50'])}) | {u(o['untung_50'])} ({u(o['a_untung_50'])}) |"), o
    if len(L):
        Lu = unik(L)
        b1, ok = baris('**Semua 29 setup (belian unik)**', Lu)
        b2, kw = baris('Kawalan: laporan 1–5 sesi, tiada isyarat beli', L[L.id == KW1])
        A += [b1, b2]
        for a in Kh['ahli']:
            g = L[L.id == a['id']]
            if len(g):
                A.append(baris(f"`{a['id']}`", g)[0])
    else:
        ok = kw = dict(lengkap=0)
    A += ['', '## Bacaan dikunci', '']
    if ok['lengkap'] >= MIN_BACAAN:
        P = [('P1 kelebihan tangkap > 0', ok['terus'] - ok['a_terus'] > 0), ('P2 arah > 0 (tambahan naik melebihi tambahan jatuh)', ok['arah'] > 0),
             ('P3 kadar menang cara B melebihi saham rawak', ok['menang_B'] - ok['a_menang_B'] > 0),
             ('P3b (tambahan, keputusan pengguna 17 Nov 2026) kadar menang cara 50 melebihi saham rawak', ok['menang_50'] - ok['a_menang_50'] > 0),
             ('P4 arah kohort melebihi arah kawalan (isyarat beli menambah)', ok['arah'] > kw.get('arah', np.nan))]
        A += [f"- {t}: **{'YA' if v else 'TIDAK'}**" for t, v in P]
        A.append(f"- Dibaca pada {ok['lengkap']} belian unik dengan tetingkap lengkap (perlu ≥ {MIN_BACAAN}). Bacaan pertama yang direkod dalam "
                 'nota serahan ialah bacaan rasmi; angka selepas itu maklumat sahaja.')
    else:
        A.append(f"**Belum cukup:** {ok['lengkap']} daripada {MIN_BACAAN} belian unik dengan tetingkap 20 sesi lengkap. Angka di atas belum boleh dibaca.")
    A += ['', '## Cara baca', '',
          '- Tangkap = naik ≥ 5 % minggu pertama DAN naik lagi hingga minggu ke-4 tanpa jatuh 8 %. Naik / Jatuh ≥ 5 % = pada tutup sesi ke-5.',
          '- Cara B = pegang sekurang-kurangnya 20 sesi, kemudian jual selepas tutup di bawah purata 20 hari (paling lama 126 sesi). '
          'Cara 50 = yang sama dengan purata 50 hari, tiada had masa. Stop loss 4×ATR14 pada kedua-duanya; kos 0.5 %.',
          '- Dagangan yang belum ditutup dinilai pada harga tutup terkini; cara yang sama bagi saham rawak.',
          f'- Tarikh laporan = seperti diketahui pada hari isyarat (`isyarat.csv`, tidak pernah dikira semula). Alam: {alam_teks}.',
          '- Kebanyakan setup hanya aktif dalam keadaan pasaran tertentu dan pada musim laporan kewangan; hari tanpa belian adalah biasa.', '']
    open(os.path.join(KELUAR, 'RINGKASAN.md'), 'w', encoding='utf-8').write('\n'.join(A))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('arahan', choices=['kohort', 'harga', 'kalendar', 'jejak'])
    ap.add_argument('--stor', help='folder harga semua saham (hasil `harga`)')
    ap.add_argument('--kalendar', help='fail kalendar semua saham (hasil `kalendar`)')
    ap.add_argument('--ke', help='destinasi `harga` (folder) atau `kalendar` (fail)')
    a = ap.parse_args(argv)
    if a.arahan == 'kohort':
        bina_kohort()
    elif a.arahan == 'harga':
        tarik_harga(a.ke)
    elif a.arahan == 'kalendar':
        tarik_kalendar(a.stor, a.ke)
    elif a.stor:
        if not a.kalendar:
            ap.error('jejak --stor memerlukan --kalendar')
        jejak(stor=a.stor, kalendar=a.kalendar, semua=True)
    else:
        jejak()


if __name__ == '__main__':
    main()
