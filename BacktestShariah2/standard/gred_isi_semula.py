# Isi semula gred bagi posisi papertrade yang dibeli sebelum gred mula direkod (14 Okt 2026). Keputusan pengguna 17 Okt 2026.
# Hanya baris dibeli tanpa gred_keseluruhan diubah; baris yang sudah bergred tidak disentuh.
#   RS        : dikira tepat pada tarikh rujukan (tarikh_isyarat, atau sesi sebelum tarikh_beli): seluruh pasaran
#               (data/rs/rs_pasaran.csv) jika ada, sandaran stor harga; skema gred RS 18 Okt 2026 (gred.gred_rs).
#   QR        : hari dagangan dari tarikh rujukan ke earnings terdekat (Nasdaq data/pemangkin/earnings_nasdaq.json).
#   Sektor/Ind: snapshot sektor_pasaran.csv terkini (data hari isyarat tiada) — ditanda dalam gred_pada.
#   Pemangkin : '–' (berita hari isyarat tiada).
# Guna: python3 BacktestShariah2/standard/gred_isi_semula.py --harga <folder stor> [--folder papertrade] [--tarikh YYYY-MM-DD]
import argparse, csv, glob, json, os, re, sys
from datetime import date, timedelta

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gred as G  # noqa: E402
from sektor_pasaran import SEKTOR_INDUSTRI  # noqa: E402

BS2 = os.path.dirname(HERE)
PT = os.path.join(BS2, 'papertrade')


def fail_posisi(folder):
    c = sorted(glob.glob(os.path.join(folder, 'claude*.csv')),
               key=lambda p: int(re.search(r'claude_?(\d*)', os.path.basename(p)).group(1) or 1))
    return [os.path.join(folder, 'moomoo.csv')] + c


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--harga', required=True, help='folder harga_A/B.csv')
    ap.add_argument('--folder', default=PT)
    ap.add_argument('--nasdaq', default=os.path.join(BS2, 'data', 'pemangkin', 'earnings_nasdaq.json'))
    ap.add_argument('--tarikh', default=date.today().isoformat(), help='tarikh isi semula (untuk gred_pada)')
    ap.add_argument('--rs', default=os.path.join(BS2, 'data', 'rs'), help='folder rs_pasaran.csv + status.json')
    a = ap.parse_args(argv)
    c, _ = G.muat_harga(a.harga)
    spy = G.muat_spy(a.harga)
    sesi = list(c.index)
    pusek, puind = G.peta_pasaran(os.path.join(a.folder, 'sektor_pasaran.csv'))
    sek, ind = G.peta_sektor(os.path.join(a.folder, 'sektor.csv'))
    snap = max(r['tarikh'] for r in csv.DictReader(open(os.path.join(a.folder, 'sektor_pasaran.csv'), encoding='utf-8')))
    pind = {r['ticker']: r['industri'] for r in csv.DictReader(open(os.path.join(a.folder, 'peta_industri.csv'), encoding='utf-8'))}
    nasd = json.load(open(a.nasdaq, encoding='utf-8'))
    nas, dari, hingga = nasd.get('saham') or {}, date.fromisoformat(nasd['dari']), date.fromisoformat(nasd['hingga'])
    rs_cache, n, kira = {}, 0, {}
    for p in fail_posisi(a.folder):
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames); rows = list(rd)
        ubah = 0
        for r in rows:
            if r.get('tidak_dibeli') == 'True' or not r.get('tarikh_beli') or r.get('gred_keseluruhan'):
                continue
            t = r['saham']
            ti = r.get('tarikh_isyarat') or ''
            if not ti:
                sb = [x for x in sesi if x < pd.Timestamp(r['tarikh_beli'])]
                if not sb:
                    continue
                ti = str(sb[-1].date())
            if ti not in rs_cache:
                k = c[c.index <= pd.Timestamp(ti)]
                rs_cache[ti] = G.rs_semua(k, spy, a.rs)
            rsd, spy_atas = rs_cache[ti]
            ref = date.fromisoformat(ti)
            iu = pind.get(t); su = SEKTOR_INDUSTRI.get(iu) if iu else None
            s1 = pusek.get(su) if su in pusek else sek.get(r.get('sektor'))
            s2 = puind.get(iu) if iu in puind else ind.get(r.get('industri'))
            r['sektor_us'] = su or ''; r['industri_us'] = iu or ''
            r['skor_sektor'] = '' if s1 is None else round(s1, 1); r['gred_sektor'] = G.gred_kumpulan(s1)
            r['skor_industri'] = '' if s2 is None else round(s2, 1); r['gred_industri'] = G.gred_kumpulan(s2)
            G.isi_rs(r, rsd.loc[t] if t in rsd.index else None, spy_atas)
            e = nas.get(t) or {}
            cal = sorted(d for d in (G._tarikh(e.get('lalu')), G._tarikh(e.get('seterusnya'))) if d and d >= ref)
            te = cal[0] if cal else None
            if te is not None or (e.get('lalu') and dari <= ref and ref + timedelta(days=35) <= hingga):
                h = G.hari_dagangan(ref, te) if te else None
                r['tarikh_earnings'] = te.isoformat() if te else ''
                r['hari_ke_earnings'] = '' if h is None else h
                sj = G.sejak_qr(G._tarikh(e.get('lalu')), ref)
                r['sumber_earnings'] = G.tanda_pasca_qr('Nasdaq' if te else 'tiada dalam 35 hari (Nasdaq)', sj)
                r['gred_qr'] = G.gred_qr(h, sj)
            else:
                r['tarikh_earnings'] = ''; r['hari_ke_earnings'] = ''; r['sumber_earnings'] = 'tiada data'; r['gred_qr'] = G.TIADA
            r['mata_pemangkin'] = ''; r['pemangkin'] = 'tiada data (isi semula)'; r['gred_pemangkin'] = G.TIADA; r['pemangkin_url'] = ''
            r['gred_keseluruhan'] = G.gred_keseluruhan([r['gred_sektor'], r['gred_industri'], r['gred_pemangkin'], r['gred_qr']])
            r['gred_pada'] = f'isi semula {a.tarikh} (RS & QR pada {ti}; sektor/industri snapshot {snap})'
            ubah += 1
            for k in ('gred_rs', 'gred_qr', 'gred_keseluruhan'):
                kira.setdefault(k, {}); kira[k][r[k]] = kira[k].get(r[k], 0) + 1
        if ubah:
            lajur += [k for k in G.LAJUR if k not in lajur]
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows: w.writerow({k: r.get(k, '') for k in lajur})
        n += ubah
    print(json.dumps(dict(diisi=n, snapshot_sektor=snap, **{k: dict(sorted(v.items())) for k, v in kira.items()}), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
