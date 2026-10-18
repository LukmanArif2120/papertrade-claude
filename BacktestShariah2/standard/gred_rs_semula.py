# Kira semula lajur RS (skema 18 Okt 2026; keputusan pengguna) bagi baris bergred dalam fail posisi, senarai_beli dan
# watchlist, pada tarikh rujukan asal (tarikh_isyarat, atau sesi sebelum tarikh_beli). Sumber RS: data/rs/rs_pasaran.csv
# bagi sesi itu jika ada, sandaran stor harga (rs_sumber). gred_keseluruhan dikira semula tanpa RS. Lajur lain tidak disentuh.
# Guna: python3 BacktestShariah2/standard/gred_rs_semula.py --harga <folder stor> [--folder papertrade] [--tarikh YYYY-MM-DD]
import argparse, csv, json, os, sys
from collections import Counter
from datetime import date

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gred as G  # noqa: E402
from gred_isi_semula import fail_posisi  # noqa: E402

BS2 = os.path.dirname(HERE)
TANDA = 'RS skema 18 Okt'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--harga', required=True, help='folder harga_A/B.csv + harga_idx.csv')
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--rs', default=os.path.join(BS2, 'data', 'rs'))
    ap.add_argument('--tarikh', default=date.today().isoformat())
    a = ap.parse_args(argv)
    c, _ = G.muat_harga(a.harga)
    spy = G.muat_spy(a.harga)
    sesi = list(c.index)
    cache, kira, n = {}, Counter(), 0
    jenis = G.peta_jenis_kaedah()
    fail = fail_posisi(a.folder) + [os.path.join(a.folder, f) for f in ('senarai_beli.csv', 'watchlist.csv')]
    for p in fail:
        if not os.path.exists(p):
            continue
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        if 'gred_rs' not in lajur:
            continue
        ubah = 0
        for r in rows:
            if not (r.get('gred_rs') or r.get('rs_rating')):
                continue
            ti = r.get('tarikh_isyarat') or ''
            if not ti and r.get('tarikh_beli'):
                sb = [x for x in sesi if x < pd.Timestamp(r['tarikh_beli'])]
                ti = str(sb[-1].date()) if sb else ''
            if not ti:
                continue
            if ti not in cache:
                k = c[c.index <= pd.Timestamp(ti)]
                cache[ti] = G.rs_semua(k, spy, a.rs) if len(k) else (pd.DataFrame(), None)
            rsd, atas = cache[ti]
            t = G.ambil(r, 'saham', 'Saham')
            G.isi_rs(r, rsd.loc[t] if t in rsd.index else None, atas)
            if r.get('gred_keseluruhan'):
                r['gred_keseluruhan'] = G.keseluruhan_baris(r, jenis)
            gp = r.get('gred_pada') or ''
            if TANDA not in gp:
                r['gred_pada'] = (gp + '; ' if gp else '') + f'{TANDA} (dikira semula {a.tarikh}, RS pada {ti})'
            kira[(r['gred_rs'], r.get('rs_sumber') or '')] += 1
            ubah += 1
        if ubah:
            lajur += [k for k in G.LAJUR if k not in lajur]
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in lajur})
        n += ubah
    print(json.dumps(dict(dikira_semula=n, gred_sumber={f'{g}|{s}': v for (g, s), v in sorted(kira.items())}), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
