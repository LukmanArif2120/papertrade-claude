# Imbasan pandang ke hadapan bagi salinan AUTOTUNE/kaedah/Mxx.py (selepas audit M81, 18 Okt 2026).
# Bagi setiap tarikh potong c: sedia() atas data dipotong pada c (termasuk) lwn sedia() atas data penuh, PARAM asal.
#   exitc, stop, tgt : mesti sama bagi semua tarikh <= c (exitc[j] → keluar buka j+1, jadi hanya data <= j).
#                      exitc hari c yang hanya bergantung pada KEWUJUDAN bar c+1 (pengawal `j + 1 < n`; ujian bar c+1
#                      = tutup c tanpa maklumat baharu) dicatat sebagai dibenarkan.
#                      stop/tgt pada hari c sahaja boleh berbeza jika diterbitkan daripada buka c+1 (ujian buka-sahaja).
#   sig, rank        : mesti sama bagi tarikh <= c-1; pada hari c boleh berbeza hanya jika bergantung pada buka c+1
#                      sahaja (peraturan boleh laksana "langkau jika buka esok <= henti").
#   stop dan rank dibanding hanya pada hari sig benar (dalam mana-mana larian): enjin membaca st[i]/rank[i] pada
#   hari isyarat i sahaja. tgt dan exitc dibanding pada semua hari (dibaca sepanjang dagangan).
# Ujian buka-sahaja: data dipotong pada c + bar c+1 dengan high/low/close/volume/turnover diganti nilai buka c+1;
# jika hasil hari c sama dengan larian penuh, kebergantungan hanya pada buka c+1 (dibenarkan).
# Guna: python3 AUTOTUNE/kaedah/semak_hadapan.py [Mxx ...|semua] [--proses 4] [--ticker N]
#       python3 AUTOTUNE/kaedah/semak_hadapan.py M81 --asal   (imbas modul asal = keadaan sebelum dibaiki)
# Output: AUTOTUNE/hasil/PANDANG_HADAPAN.md, AUTOTUNE/hasil/pandang_hadapan.json
import argparse, glob, json, os, re, sys, time, traceback
from multiprocessing import Pool

import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import kesetaraan as K   # noqa: E402

AKAR = K.AKAR
HASIL = os.path.join(AKAR, 'AUTOTUNE', 'hasil')
JSON = os.path.join(HASIL, 'pandang_hadapan.json')
MD = os.path.join(HASIL, 'PANDANG_HADAPAN.md')
POTONG = ('2021-06-30', '2023-03-31', '2025-06-30')
KETAT = ('exitc', 'stop', 'tgt')      # sama hingga c (stop/tgt hari c: buka-sahaja dibenarkan)
LONGGAR = ('sig', 'rank')            # sama hingga c-1; hari c: buka-sahaja dibenarkan
HARI_ISYARAT = ('stop', 'rank')      # enjin membaca lajur ini pada hari isyarat sahaja
TANDA_BAIKI = '# Dibaiki (pandang ke hadapan):'
# Pembetulan yang dibuat dalam salinan AUTOTUNE (keterangan untuk pandang_hadapan.json).
BAIKI = {
    'M81': 'exitc[j] = True apabila tutup[j] <= paras henti mengekor (keluar buka j+1); '
           'dahulu exitc[j-1] ditanda daripada rendah[j] (keluar buka j dengan pengetahuan hari j).',
}
_DATA = {}


def potong(fr, idx, c, buka_sahaja=False, wujud_sahaja=False):
    """Salinan fr/idx dengan bar <= c.
    buka_sahaja: tambah bar pertama selepas c dengan high/low/close/volume/turnover = buka bar itu.
    wujud_sahaja: tambah bar pertama selepas c dengan semua harga = tutup c dan volume/turnover = bar c
    (bar wujud tetapi tiada maklumat baharu; untuk pengawal `j + 1 < n`)."""
    c = pd.Timestamp(c)

    def satu(g):
        a = g[g.index <= c]
        if buka_sahaja or wujud_sahaja:
            b = g[g.index > c].iloc[:1].copy()
            if len(b):
                for k in ('high', 'low', 'close', 'volume', 'turnover'):
                    if k in b: b[k] = b['open'].astype(b[k].dtype)
                if wujud_sahaja and len(a):
                    for k in b.columns:
                        if k in ('open', 'high', 'low', 'close'): b[k] = a['close'].iloc[-1]
                        elif k in ('volume', 'turnover'): b[k] = a[k].iloc[-1]
                a = pd.concat([a, b])
        return a.copy()
    f2 = {t: satu(g[K.ASAS]) for t, g in fr.items()}
    f2 = {t: g for t, g in f2.items() if len(g)}
    return f2, {t: satu(g) for t, g in idx.items()}


def _bool(x):
    return np.asarray(pd.Series(x).fillna(False).astype(bool).values)


def _beza(a, b):
    """Topeng hari berbeza (NaN == NaN)."""
    a = np.asarray(a); b = np.asarray(b)
    na, nb = pd.isna(a), pd.isna(b)
    with np.errstate(invalid='ignore'):
        eq = np.asarray(a == b, dtype=bool)
    return ~((eq & ~na & ~nb) | (na & nb))


def banding(fx, ff, c, lajur):
    """{lajur: {ticker: [tarikh berbeza <= c]}} antara fx (dipotong) dan ff (penuh)."""
    c = pd.Timestamp(c); hasil = {}
    for t, g in fx.items():
        if t not in ff: continue
        h = ff[t]
        ix = g.index[g.index <= c]
        if not len(ix): continue
        for k in lajur:
            if k not in g.columns and k not in h.columns: continue
            if k not in g.columns or k not in h.columns:
                hasil.setdefault(k, {})[t] = [ix[-1]]; continue
            m = _beza(g[k].loc[ix].values, h[k].reindex(ix).values)
            if k in HARI_ISYARAT and 'sig' in g.columns and 'sig' in h.columns:
                # stop dan rank hanya dibaca enjin pada hari isyarat (st[i], rank[i]): banding pada hari sig benar
                # dalam salah satu larian sahaja
                m &= (_bool(g['sig'].loc[ix]) | _bool(h['sig'].reindex(ix)))
            if m.any(): hasil.setdefault(k, {})[t] = list(ix[m])
    return hasil


def _sedia(mod, f, i):
    """sedia() atas data dipotong. Jika ralat (cth. ticker terlalu pendek sebelum c) dan kaedah bukan SILANG,
    ulang tanpa ticker yang < PERLU_BAR bar (ticker itu tidak dibanding)."""
    try:
        mod.sedia(f, i); return f
    except Exception:
        if getattr(mod, 'SILANG', False): raise
        had = max(int(getattr(mod, 'PERLU_BAR', 0) or 0), int(getattr(mod, 'WARM', 0) or 0)) + 5
        f2 = {t: g[K.ASAS].copy() for t, g in f.items() if len(g) >= had}
        mod.sedia(f2, {t: g.copy() for t, g in i.items()})
        return f2


def imbas(mod, fr, idx, potong_=POTONG):
    """Imbas satu modul. Pulang {'langgar': {lajur: {'ticker': set, 'hari': set, 'sifat': set}}, 'dibenar': {...}}."""
    ff = K.salin(fr); ix_ = {t: g.copy() for t, g in idx.items()}
    mod.sedia(ff, ix_)
    langgar, dibenar = {}, {}

    def catat(d, k, t, hari, sifat):
        e = d.setdefault(k, {'ticker': set(), 'hari': set(), 'sifat': set()})
        e['ticker'].add(t); e['hari'].update(str(x.date()) for x in hari); e['sifat'].add(sifat)
    for c in potong_:
        C = pd.Timestamp(c)
        ft, it = potong(fr, idx, c)
        ft = _sedia(mod, ft, it)
        b = banding(ft, ff, c, KETAT + LONGGAR)
        perlu_buka = {}       # lajur -> {ticker: [hari c]} yang perlu ujian buka-sahaja
        perlu_wujud = {}      # exitc -> {ticker: [hari c]} yang perlu ujian bar-wujud
        for k, d in b.items():
            for t, hari in d.items():
                awal = [x for x in hari if x < C]
                hc = [x for x in hari if x == C]
                if awal:
                    catat(langgar, k, t, awal, 'beza sebelum hari potong (bergantung > 1 bar ke hadapan)')
                if hc:
                    if k == 'exitc': perlu_wujud.setdefault(k, {})[t] = hc
                    else: perlu_buka.setdefault(k, {})[t] = hc
        if perlu_wujud:
            # exitc hari c: hanya kewujudan bar c+1 (tanpa nilai baharu) dibenarkan, cth. pengawal `j + 1 < n`
            fw, iw = potong(fr, idx, c, wujud_sahaja=True)
            fw = _sedia(mod, fw, iw)
            bw = banding(fw, ff, c, ('exitc',))
            for t, hc in perlu_wujud['exitc'].items():
                if C in bw.get('exitc', {}).get(t, []):
                    catat(langgar, 'exitc', t, hc, 'exitc hari c bergantung nilai bar c+1')
                else:
                    catat(dibenar, 'exitc', t, hc, 'exitc hari c bergantung kewujudan bar c+1 sahaja (pengawal j+1<n)')
        if perlu_buka:
            fo, io = potong(fr, idx, c, buka_sahaja=True)
            fo = _sedia(mod, fo, io)
            bo = banding({t: fo[t] for t in fo}, ff, c, tuple(perlu_buka))
            for k, d in perlu_buka.items():
                for t, hc in d.items():
                    if C in bo.get(k, {}).get(t, []):
                        catat(langgar, k, t, hc, 'hari c bergantung high/low/close/volume bar c+1')
                    else:
                        catat(dibenar, k, t, hc, 'hari c bergantung buka c+1 sahaja')
    return {'langgar': langgar, 'dibenar': dibenar}


def _jsonkan(d):
    return {k: {'ticker': len(v['ticker']), 'hari': len(v['hari']), 'sifat': sorted(v['sifat']),
                'contoh': sorted(v['ticker'])[:5], 'contoh_hari': sorted(v['hari'])[:5]} for k, v in d.items()}


def _init(n_ticker):
    _DATA['fr'], _DATA['idx'] = K.muat(n_ticker)


def semak(mid, asal=False):
    """asal=True: imbas modul asal BacktestShariah2/kod/kaedah/Mxx.py (= salinan sebelum dibaiki)."""
    t0 = time.time()
    try:
        m = K.import_fail(('hadapan_asal_' if asal else 'hadapan_') + mid, os.path.join(K.ASAL if asal else SINI, mid + '.py'))
        r = imbas(m, _DATA['fr'], _DATA['idx'])
        return {'kaedah': mid, 'langgar': _jsonkan(r['langgar']), 'dibenar': _jsonkan(r['dibenar']),
                'masa': round(time.time() - t0, 1)}
    except Exception as e:
        return {'kaedah': mid, 'ralat': f'{type(e).__name__}: {e}'[:300], 'jejak': traceback.format_exc()[-800:],
                'masa': round(time.time() - t0, 1)}


def dibaiki(mid):
    try:
        with open(os.path.join(SINI, mid + '.py')) as fh: return TANDA_BAIKI in fh.read()
    except OSError:
        return False


def tulis(baris):
    lama = json.load(open(JSON)) if os.path.exists(JSON) else {}
    mentah_f = os.path.join(SINI, 'pandang_hadapan_mentah.json')
    mentah = json.load(open(mentah_f)) if os.path.exists(mentah_f) else {}
    for r in baris:
        if r.get('asal'): mentah.setdefault('_sebelum', {})[r['kaedah']] = r
        else: mentah[r['kaedah']] = r
    sebelum_semua = mentah.get('_sebelum', {})
    kunci = lambda x: (0, int(x[0][1:])) if x[0][1:].isdigit() else (1, 0)
    json.dump(dict(sorted(mentah.items(), key=kunci)), open(mentah_f, 'w'), indent=1, ensure_ascii=False)
    mentah = {k: v for k, v in mentah.items() if not k.startswith('_')}
    out = {}
    for mid, r in sorted(mentah.items(), key=kunci):
        if r.get('ralat'):
            out[mid] = {'lajur': [], 'baiki': '', 'status': 'PANDANG HADAPAN', 'catatan': 'imbasan ralat: ' + r['ralat']}
        elif r['langgar']:
            out[mid] = {'lajur': sorted(r['langgar']), 'baiki': '', 'status': 'PANDANG HADAPAN',
                        'butiran': r['langgar']}
        elif dibaiki(mid):
            sb = (sebelum_semua.get(mid) or {}).get('langgar') or {}
            sebelum = lama.get(mid, {})
            out[mid] = {'lajur': sorted(sb) or sebelum.get('lajur', []), 'baiki': BAIKI.get(mid, sebelum.get('baiki', '')),
                        'status': 'DIBAIKI',
                        'butiran_sebelum': sb or sebelum.get('butiran', sebelum.get('butiran_sebelum', {}))}
    with open(JSON, 'w') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    dibenar = {mid: r['dibenar'] for mid, r in mentah.items() if r.get('dibenar')}
    kunci_d = lambda x: int(x[0][1:])
    n_l = sum(v['status'] == 'PANDANG HADAPAN' for v in out.values())
    n_b = sum(v['status'] == 'DIBAIKI' for v in out.values())
    L = ['# Imbasan pandang ke hadapan (AUTOTUNE)', '',
         f'Dijana oleh `AUTOTUNE/kaedah/semak_hadapan.py` ({time.strftime("%Y-%m-%d %H:%M")} UTC). Data 431 saham '
         f'(`data_mentah/`), PARAM asal, tarikh potong {", ".join(POTONG)}. Selepas audit [M81](AUDIT_M81.md).', '',
         'Peraturan: `exitc`, `stop`, `tgt` sama dengan larian penuh bagi semua tarikh ≤ c (stop/tgt hari c boleh '
         'berbeza hanya jika diterbitkan daripada buka c+1); `sig`, `rank` sama bagi tarikh ≤ c−1, dan pada hari c '
         'hanya boleh bergantung pada buka c+1 (ujian buka-sahaja: bar c+1 dengan high/low/close/volume = buka).', '',
         f'Kaedah diimbas: {len(mentah)}. Melanggar sekarang (label PANDANG HADAPAN): {n_l}. Dibaiki: {n_b}.', '',
         '## Pelanggaran', '', '| Kaedah | Status | Lajur | Ticker | Hari | Sifat | Pembetulan |', '|---|---|---|---|---|---|---|']
    for mid, v in out.items():
        b = v.get('butiran') or v.get('butiran_sebelum') or {}
        if not b:
            L.append(f"| {mid} | {v['status']} | {', '.join(v['lajur'])} | | | {v.get('catatan', '')} | {v['baiki']} |")
        for k, e in sorted(b.items()):
            L.append(f"| {mid} | {v['status']} | {k} | {e['ticker']} | {e['hari']} | {'; '.join(e['sifat'])} | {v['baiki'] or '—'} |")
    L += ['', 'Bagi DIBAIKI, bilangan ticker/hari ialah imbasan modul asal (`--asal`, = salinan sebelum dibaiki) dengan PARAM '
          'asal; imbasan semula salinan dibaiki bersih. Imbasan potong-data bersifat sampel (3 tarikh × 431 saham): M81 PARAM '
          'asal (ekor 25%) hanya tercetus pada 1 ticker-hari, tetapi kesannya besar selepas penalaan (AUDIT_M81.md).', '',
          'Semakan statik pelengkap (18 Okt 2026): `shift(-…)` dalam salinan hanya pada `open` (harga pesanan) dan sempadan '
          'minggu `ws.shift(-1)` (M52, kalendar); tiada lagi corak `ex[j - 1] = True`; indeks hadapan `l[k + 1]`/`h[k + 1]` '
          'dalam M131 ialah fraktal dengan k = i − 2 (disahkan pada hari i).', '',
          '## Dibenarkan (hari c sahaja)', '',
          '- `sig/stop/tgt/rank` hari c yang memakai buka hari esok sahaja (harga pesanan), cth. '
          '"langkau jika buka esok ≤ henti" atau sasaran = buka_masuk + k×R: boleh dilaksana kerana pesanan dibuat pada buka.',
          '- `exitc` hari c yang hanya bergantung pada kewujudan bar c+1 (pengawal `j + 1 < n` dalam gelung replika '
          'dagangan; ujian: bar c+1 = tutup c tanpa maklumat baharu). Enjin juga memerlukan j+1 < n, jadi tiada kesan backtest.',
          '- `stop/rank` dibanding hanya pada hari `sig` benar (enjin membaca st[i] dan rank[i] pada hari isyarat sahaja).', '',
          '| Kaedah | Lajur (ticker) |', '|---|---|']
    for mid, d in sorted(dibenar.items(), key=lambda x: int(x[0][1:])):
        L.append(f"| {mid} | {', '.join(f'{k} ({e['ticker']})' for k, e in sorted(d.items()))} |")
    open(MD, 'w').write('\n'.join(L) + '\n')
    return n_l, n_b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kaedah', nargs='*'); ap.add_argument('--proses', type=int, default=4)
    ap.add_argument('--ticker', type=int, default=None); ap.add_argument('--tanpa-tulis', action='store_true')
    ap.add_argument('--asal', action='store_true', help='imbas modul asal BacktestShariah2/kod/kaedah (sebelum dibaiki)')
    a = ap.parse_args()
    ids = K.senarai(a.kaedah)
    baris = []
    fn = semak
    if a.asal:     # imbas modul asal (keadaan sebelum dibaiki) bagi kaedah tersenarai
        import functools; fn = functools.partial(semak, asal=True)
    with Pool(a.proses, initializer=_init, initargs=(a.ticker,), maxtasksperchild=8) as p:
        for r in p.imap_unordered(fn, ids):
            if a.asal: r['asal'] = True
            baris.append(r)
            s = 'RALAT ' + r['ralat'] if r.get('ralat') else ('LANGGAR ' + ','.join(sorted(r['langgar'])) if r['langgar'] else 'bersih')
            print(r['kaedah'], s, r['masa'], flush=True)
    if not a.tanpa_tulis:
        print('PANDANG HADAPAN, DIBAIKI:', tulis(baris))


if __name__ == '__main__':
    main()
