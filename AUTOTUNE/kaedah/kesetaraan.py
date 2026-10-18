# Semakan kesetaraan: sedia() asal lawan sedia() salinan (PARAM asal) atas data 431 saham.
# Banding lajur sig, stop, tgt, exitc, rank setiap ticker secara tepat; ukur masa kedua-duanya.
# Guna: python3 AUTOTUNE/kaedah/kesetaraan.py [Mxx ...|semua] [--proses 4] [--ticker N]
# Output: AUTOTUNE/kaedah/kesetaraan.csv, AUTOTUNE/kaedah/KESETARAAN.md
import argparse, csv, glob, importlib.util, json, os, sys, time, traceback
from multiprocessing import Pool

import numpy as np, pandas as pd

AKAR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
KOD = os.path.join(AKAR, 'BacktestShariah2', 'kod')
ASAL = os.path.join(KOD, 'kaedah')
SINI = os.path.join(AKAR, 'AUTOTUNE', 'kaedah')
LAJUR = ('sig', 'stop', 'tgt', 'exitc', 'rank')
ASAS = ['open', 'high', 'low', 'close', 'volume', 'turnover']
CSV = os.path.join(SINI, 'kesetaraan.csv')
MEDAN = ['kaedah', 'status', 'n_param', 'n_tala', 'masa_asal', 'masa_salin', 'nisbah', 'beza', 'catatan']
_DATA = {}


def muat(n_ticker=None):
    for p in (KOD, SINI):
        if p not in sys.path: sys.path.insert(0, p)
    import enjin, tambahan
    enjin.cari = lambda n: os.path.join(AKAR, 'data_mentah', n); tambahan.cari = enjin.cari
    fr, idx, _ = tambahan.muat()
    if n_ticker:
        fr = {t: fr[t] for t in sorted(fr)[:: max(1, len(fr) // n_ticker)][:n_ticker]}
    return fr, idx


def import_fail(nama, laluan):
    s = importlib.util.spec_from_file_location(nama, laluan)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def salin(fr):
    return {t: g[ASAS].copy() for t, g in fr.items()}


def sama(a, b):
    if a.shape != b.shape: return False
    if a.dtype.kind == 'f' and b.dtype.kind == 'f':
        return a.dtype == b.dtype and np.array_equal(a, b, equal_nan=True)
    if a.dtype != b.dtype and not {a.dtype.kind, b.dtype.kind} <= {'b', 'O'}: return False
    na, nb = pd.isna(a), pd.isna(b)
    if not np.array_equal(na, nb): return False
    return bool(np.all((a == b) | na))


def banding(fa, fb):
    beza = []
    for t in fa:
        for c in LAJUR:
            if c not in fa[t] or c not in fb[t]:
                beza.append(f'{t}:{c}:tiada'); continue
            if not sama(fa[t][c].values, fb[t][c].values): beza.append(f'{t}:{c}')
    return beza


def _init(n_ticker):
    _DATA['fr'], _DATA['idx'] = muat(n_ticker)


def semak(mid):
    fr, idx = _DATA['fr'], _DATA['idx']
    r = {'kaedah': mid, 'status': 'RALAT', 'n_param': '', 'n_tala': '', 'masa_asal': '', 'masa_salin': '',
         'nisbah': '', 'beza': '', 'catatan': ''}
    try:
        A = import_fail('asal_' + mid, os.path.join(ASAL, mid + '.py'))
        B = import_fail('at_' + mid, os.path.join(SINI, mid + '.py'))
        r['n_param'] = len(B.PARAM); r['n_tala'] = len(getattr(B, 'TALA', []))
        if getattr(B, 'BELUM_DITALA', False): r['catatan'] = 'pembalut'
        for k in ('ID', 'NAMA', 'VARIAN', 'TMAX', 'WARM', 'ADA_HENTI', 'SILANG', 'PERLU_BAR'):
            if getattr(A, k) != getattr(B, k): raise RuntimeError(f'pemalar {k} berbeza')
        masa = []
        for ulang in range(4):
            fa, fb = salin(fr), salin(fr)
            if ulang % 2 == 0:
                t0 = time.perf_counter(); A.sedia(fa, idx); t1 = time.perf_counter(); B.sedia(fb, idx); t2 = time.perf_counter()
                masa.append((t1 - t0, t2 - t1))
            else:                                    # susunan diterbalikkan supaya kesan cache/GC seimbang
                t0 = time.perf_counter(); B.sedia(fb, idx); t1 = time.perf_counter(); A.sedia(fa, idx); t2 = time.perf_counter()
                masa.append((t2 - t1, t1 - t0))
            if ulang == 0:
                beza = banding(fa, fb)
            ta, tb = min(m[0] for m in masa), min(m[1] for m in masa)
            if beza or tb <= 1.2 * ta or ulang == 3: break
        r.update(masa_asal=round(ta, 2), masa_salin=round(tb, 2), nisbah=round(tb / ta, 3) if ta > 0 else '')
        r['beza'] = len(beza)
        baiki = '# Dibaiki (pandang ke hadapan):' in open(os.path.join(SINI, mid + '.py')).read()
        if baiki:    # Pindaan 18 Okt 2026: salinan dibaiki sengaja berbeza daripada asal (semak_hadapan.py)
            r['status'] = 'DIBAIKI'
            r['catatan'] = (r['catatan'] + f' dibaiki pandang ke hadapan; beza dijangka ({len(beza)} lajur-ticker): '
                            + ';'.join(beza[:3])).strip()
        elif beza: r['status'] = 'BEZA'; r['catatan'] = (r['catatan'] + ' ' + ';'.join(beza[:4])).strip()
        else: r['status'] = 'SAMA'
    except Exception as e:
        r['catatan'] = (r['catatan'] + f' {type(e).__name__}: {e}'.replace('\n', ' ')[:200]).strip()
    return r


def senarai(args):
    if not args or args == ['semua']:
        return sorted((os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ASAL, 'M*.py'))), key=lambda s: int(s[1:]))
    return args


def tulis(baris):
    lama = {}
    if os.path.exists(CSV):
        for r in csv.DictReader(open(CSV)): lama[r['kaedah']] = r
    for r in baris: lama[r['kaedah']] = r
    semua = sorted(lama.values(), key=lambda r: int(r['kaedah'][1:]))
    with open(CSV, 'w', newline='') as f:
        w = csv.DictWriter(f, MEDAN); w.writeheader(); w.writerows(semua)
    label = lambda r: 'BELUM DITALA' if 'pembalut' in str(r['catatan']) else r['status']
    n = {}
    for r in semua: n[label(r)] = n.get(label(r), 0) + 1
    L = ['# Kesetaraan salinan berparameter (F2)', '',
         f'Dijana oleh `kesetaraan.py` ({time.strftime("%Y-%m-%d %H:%M")}). Data 431 saham (`data_mentah/`); '
         'banding tepat lajur sig, stop, tgt, exitc, rank setiap ticker; nisbah = masa salinan ÷ masa asal (min hingga 4 ulangan bersilih susunan jika > 1.2).', '',
         'Ringkasan: ' + ', '.join(f'{k} {v}' for k, v in sorted(n.items())), '',
         'BELUM DITALA = salinan pembalut (modul asal dipanggil tanpa parameter; PARAM/JULAT/TALA kosong).',
         'DIBAIKI = salinan dibaiki kerana pandang ke hadapan (Pindaan 18 Okt 2026; `semak_hadapan.py`, '
         '`AUTOTUNE/hasil/PANDANG_HADAPAN.md`); sengaja tidak sama dengan modul asal.', '',
         '| Kaedah | Status | Param | Tala | Asal (s) | Salinan (s) | Nisbah | Catatan |', '|---|---|---|---|---|---|---|---|']
    for r in semua:
        L.append(f"| {r['kaedah']} | {label(r)} | {r['n_param']} | {r['n_tala']} | {r['masa_asal']} | {r['masa_salin']} | "
                 f"{r['nisbah']} | {str(r['catatan'])[:120]} |")
    open(os.path.join(SINI, 'KESETARAAN.md'), 'w').write('\n'.join(L) + '\n')
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kaedah', nargs='*'); ap.add_argument('--proses', type=int, default=4)
    ap.add_argument('--ticker', type=int, default=None); ap.add_argument('--tanpa-tulis', action='store_true')
    a = ap.parse_args()
    ids = senarai(a.kaedah)
    with Pool(a.proses, initializer=_init, initargs=(a.ticker,)) as p:
        baris = list(p.imap_unordered(semak, ids))
    for r in sorted(baris, key=lambda r: int(r['kaedah'][1:])):
        if r['status'] != 'SAMA' or (r['nisbah'] and r['nisbah'] > 1.2):
            print(r['kaedah'], r['status'], r['nisbah'], str(r['catatan'])[:160])
    if not a.tanpa_tulis:
        n = tulis(baris)
        print('ringkasan:', n)
    else:
        print('SAMA', sum(r['status'] == 'SAMA' for r in baris), '/', len(baris))


if __name__ == '__main__':
    main()
