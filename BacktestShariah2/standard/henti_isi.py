# henti_isi.py — isi semula lajur henti yang kosong bagi posisi (claude*.csv, moomoo.csv) yang kaedahnya ada henti rugi
# (ADA_HENTI). Audit 23 Okt 2026 (keputusan pengguna: data tidak boleh dibiar kosong).
#   - Henti harga (lajur stop modul) pada bar isyarat: posisi 9–13 Okt yang direkod sebelum harian_c menyalin stop_i.
#   - Henti ikut tutup (modul.HENTI_TUTUP = nama lajur paras, cth. M31 LOWER BB hari isyarat): stop modul NaN kerana keluar
#     dinilai pada tutup (exitc); paras itu direkod dalam henti untuk paparan dan R sahaja (enjin tidak berubah).
# Bar isyarat = tarikh_isyarat, atau sesi sebelum tarikh_beli (sama dengan harian_c.kumpul_posisi). Baris lain tidak disentuh.
#   python3 BacktestShariah2/standard/henti_isi.py [--folder papertrade] [--stor data/harga/stor] [--uji]
import argparse, importlib, json, os, sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
BS2 = os.path.dirname(HERE); sys.path.insert(0, os.path.join(BS2, 'kod'))
import enjin  # noqa: E402
from stor import muat, frames_dict  # noqa: E402
import sahkan as SH  # noqa: E402
from harian_c import fail_posisi, sesi_sebelum, _bar_isyarat, s  # noqa: E402


def paras_henti(m, g, i):
    """(paras, jenis) pada bar i selepas m.sedia: stop modul jika terhingga, selainnya lajur HENTI_TUTUP modul."""
    sp = float(g['stop'].iloc[i]) if 'stop' in g else np.nan
    if np.isfinite(sp):
        return round(sp, 4), 'harga'
    col = getattr(m, 'HENTI_TUTUP', None)
    if col and col in g:
        v = float(g[col].iloc[i])
        if np.isfinite(v):
            return round(v, 4), 'tutup'
    return None, None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--stor', default=os.path.join(BS2, 'data', 'harga', 'stor'))
    ap.add_argument('--uji', action='store_true')
    a = ap.parse_args(argv)
    FR, IDX = frames_dict(muat(a.stor))
    SES = list(IDX['SPY'].index)
    fail = {p: SH.baca(p) for p in fail_posisi(a.folder)}
    kerja = defaultdict(list)          # kaedah -> [(fail, n, saham, ti)]
    for p, (lajur, rows) in fail.items():
        for n, r in enumerate(rows):
            if SH.benar(r.get('tidak_dibeli')) or not SH.kosong(r.get('henti')) or not r.get('tarikh_beli'):
                continue
            mid = r.get('id_kaedah') or r.get('kaedah') or ''
            ti = r.get('tarikh_isyarat') or sesi_sebelum(r['tarikh_beli'], SES)
            if mid.startswith('M') and ti:
                kerja[mid].append((p, n, r['saham'], ti))
    kira, contoh = Counter(), []
    for mid, L in sorted(kerja.items()):
        try:
            m = importlib.import_module(f'kaedah.{mid}')
        except Exception:
            kira['tiada modul'] += len(L); continue
        if not getattr(m, 'ADA_HENTI', False):
            kira[f'tanpa henti ({mid})'] += len(L); continue
        fr = {t: FR[t].copy() for t in {x[2] for x in L} if t in FR}
        m.sedia(fr, {k: v.copy() for k, v in IDX.items()})
        for g in fr.values():
            enjin.siap(g)
        for p, n, t, ti in L:
            g = fr.get(t); i = _bar_isyarat(g, ti) if g is not None else None
            v, jenis = paras_henti(m, g, i) if i is not None else (None, None)
            if v is None:
                kira[f'tiada paras ({mid})'] += 1; continue
            r = fail[p][1][n]; r['henti'] = s(v)
            kira[f'diisi {jenis} ({mid})'] += 1
            if len(contoh) < 6:
                contoh.append(f'{t} {mid} {ti}: {v} ({jenis})')
    if not a.uji:
        for p, (lajur, rows) in fail.items():
            SH.tulis(p, lajur, rows)
    print(json.dumps(dict(kira=dict(sorted(kira.items())), contoh=contoh, uji=a.uji), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
