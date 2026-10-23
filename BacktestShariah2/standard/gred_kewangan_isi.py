# Isi semula lajur kewangan (gred kewangan v7.1; spec/GRED_KEWANGAN_v7.md) bagi baris yang gred_kewangan kosong atau
# '–' SAHAJA, dalam moomoo.csv (posisi akaun lama, dibeli 1–8 Okt sebelum v7 wujud), fail posisi claude*.csv,
# senarai_beli.csv dan watchlist.csv. Keputusan pengguna 23 Okt 2026 ("Penuh"). Baris bergred tidak disentuh; baris
# tidak_dibeli / tidak_sah diabaikan; lajur lain tidak disentuh kecuali catatan dalam gred_pada.
#
# Point-in-time: sesi rujukan D = tarikh_isyarat / tarikh_data, atau sesi dagangan sebelum tarikh_beli. Hari rujukan
# penyata = tarikh imbasan dalam gred_pada (gred_pada bermula dengan tarikh, atau "... pada YYYY-MM-DD") jika >= D,
# selainnya D. Hanya penyata yang diterbitkan <= hari rujukan (gred_kewangan.tersedia) dan harga <= D dipakai.
# Lajur: gred_kewangan, kewangan_ringkas, kewangan_tempoh; kewangan_butiran bagi senarai_beli/watchlist, dan bagi fail
# posisi claude*.csv yang sudah menyimpan butiran (atau --butiran-posisi). moomoo.csv tidak menerima kewangan_butiran:
# dokumen db papertrade/moomoo akan melepasi had 256 KiB (lihat gred_kewangan.isi). gred_pada ditambah
# "kewangan isi semula <tarikh> (v7.1, penyata <= <hari rujukan>)".
# Guna: python3 BacktestShariah2/standard/gred_kewangan_isi.py --harga <folder stor harga> [--folder papertrade]
#           [--kewangan data/kewangan] [--tarikh YYYY-MM-DD] [--uji] [--butiran-posisi]
#   --uji: kira sahaja; tiada fail ditulis. Cetak kiraan sebelum/selepas dan sebab setiap baki '–'.
# Selepas tulis: python3 BacktestShariah2/standard/pecah_claude.py --pecah dan sahkan.py --betulkan.
import argparse, csv, json, os, re, sys
from collections import Counter, defaultdict
from datetime import date

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gred as G  # noqa: E402
import gred_kewangan as GK  # noqa: E402
from gred_isi_semula import fail_posisi  # noqa: E402
from sektor_pasaran import SEKTOR_INDUSTRI  # noqa: E402

BS2 = os.path.dirname(HERE)
TANDA = 'kewangan isi semula'
SIMPLE = ('senarai_beli.csv', 'watchlist.csv')


def kosong(r):
    return (r.get('gred_kewangan') or '').strip() in ('', GK.TIADA)


def abaikan(r):
    return str(r.get('tidak_dibeli', '')).strip() == 'True' or str(r.get('tidak_sah', '')).strip() == 'True'


def kategori(r):
    """Kategori sebab '–' sedia ada (untuk kiraan sebelum)."""
    s = (r.get('kewangan_ringkas') or '').strip()
    if not s:
        return 'kosong (belum dikira)'
    m = re.match(r'– \((.*)\)$', s)
    x = m.group(1) if m else s
    x = re.sub(r'^\d+ (suku|separuh tahun|tahun); sub .*', r'N \1; sub K/U/T/S tidak cukup', x)
    x = re.sub(r'^\d+ suku berturut \(< \d\).*', '< 8 suku berturut', x)
    return x


def tarikh_imbasan(gp):
    """Tarikh imbasan asal dalam gred_pada: awalan YYYY-MM-DD, atau 'pada YYYY-MM-DD' pertama."""
    gp = gp or ''
    d = G._tarikh(gp[:10])
    if d:
        return d
    m = re.search(r'pada (\d{4}-\d\d-\d\d)', gp)
    return G._tarikh(m.group(1)) if m else None


def rujukan(r, sesi):
    """-> (D: pd.Timestamp sesi isyarat | None, hari rujukan penyata: date | None)."""
    ti = r.get('tarikh_isyarat') or r.get('tarikh_data') or ''
    if not ti and r.get('tarikh_beli'):
        sb = [x for x in sesi if x < pd.Timestamp(r['tarikh_beli'])]
        ti = str(sb[-1].date()) if sb else ''
    D = max([x for x in sesi if x <= pd.Timestamp(ti)], default=None) if ti else None
    if D is None:
        return None, None
    gp = tarikh_imbasan(r.get('gred_pada'))
    return D, (gp if gp and gp >= D.date() else D.date())


def main(argv=None):
    ap = argparse.ArgumentParser(description='Isi semula lajur kewangan v7.1 bagi baris kosong/– sahaja')
    ap.add_argument('--harga', required=True, help='folder stor harga (harga_A/B.csv)')
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--kewangan', default=os.path.join(BS2, 'data', 'kewangan'))
    ap.add_argument('--tarikh', default=date.today().isoformat(), help='tarikh isi semula (catatan gred_pada)')
    ap.add_argument('--uji', action='store_true', help='kira sahaja; jangan tulis fail')
    ap.add_argument('--butiran-posisi', action='store_true', help='tulis kewangan_butiran ke semua claude*.csv')
    ap.add_argument('--json', help='simpan ringkasan (sebelum/selepas, baki) ke fail JSON')
    a = ap.parse_args(argv)
    c, _ = G.muat_harga(a.harga)
    sesi = list(c.index)
    peta = os.path.join(a.folder, 'peta_industri.csv')
    pind = {r['ticker']: r['industri'] for r in csv.DictReader(open(peta, newline='', encoding='utf-8'))} \
        if os.path.exists(peta) else {}
    data, med = {}, {}
    sebelum, selepas, gred_baru = Counter(), Counter(), Counter()
    baki = defaultdict(list)
    n_isi = 0
    tl = date.fromisoformat(a.tarikh)
    tanda_tarikh = f'{tl.day} {["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"][tl.month - 1]}'

    def muat(t):
        if t not in data:
            p = os.path.join(a.kewangan, f'{t}.json')
            data[t] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
        return data[t]

    fail = fail_posisi(a.folder) + [os.path.join(a.folder, f) for f in SIMPLE]
    for p in fail:
        if not os.path.exists(p):
            continue
        nama = os.path.basename(p)
        kump = 'moomoo' if nama == 'moomoo.csv' else 'claude' if nama.startswith('claude') else nama[:-4]
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        posisi = nama not in SIMPLE
        butiran = not posisi or (nama != 'moomoo.csv' and (a.butiran_posisi or any(r.get('kewangan_butiran') for r in rows)))
        ubah = 0
        for r in rows:
            if abaikan(r) or not kosong(r):
                continue
            t = G.ambil(r, 'saham', 'Saham')
            sebelum[(kump, kategori(r))] += 1
            D, hi = rujukan(r, sesi)
            if D is None:
                rk = GK.hasil_kosong('tiada tarikh/harga rujukan')
            else:
                k = muat(t)
                if k is None:
                    rk = GK.hasil_kosong('tiada data kewangan')
                else:
                    iu = r.get('industri_us') or pind.get(t) or G.ambil(r, 'industri', 'Industri') or ''
                    su = r.get('sektor_us') or SEKTOR_INDUSTRI.get(iu) or G.ambil(r, 'sektor', 'Sektor') or ''
                    if hi not in med:
                        med[hi] = GK.median_industri(a.kewangan, pind, hi)
                    h = c[t][c.index <= D].dropna() if t in c.columns else None
                    try:
                        rk = GK.kira(k, h, hi, med[hi].get(iu), su, iu)
                    except Exception as ex:   # data rosak tidak boleh menghentikan pengisian fail lain
                        rk = GK.hasil_kosong(f'ralat {type(ex).__name__}: {ex}'[:120])
            if rk['gred'] == GK.TIADA:
                sb = rk['butiran'].get('sebab')
                sebab = rk['ringkas'] + (f' — {sb}' if sb and sb not in rk['ringkas'] else '')
                selepas[(kump, re.sub(r'^\d+ ', 'N ', sebab))] += 1
                baki[f'{kump}|{sebab}'].append(f'{t}@{D.date() if D is not None else "?"}')
            else:
                gred_baru[(kump, rk['gred'])] += 1
            r['gred_kewangan'] = rk['gred']; r['kewangan_ringkas'] = rk['ringkas']; r['kewangan_tempoh'] = rk['tempoh']
            if butiran:
                r['kewangan_butiran'] = json.dumps(rk['butiran'], ensure_ascii=False, separators=(',', ':'))
            gp = r.get('gred_pada') or ''
            if TANDA not in gp and hi is not None:
                r['gred_pada'] = (gp + '; ' if gp else '') + f'{TANDA} {tanda_tarikh} (v{GK.VERSI}, penyata <= {hi})'
            ubah += 1
        n_isi += ubah
        if ubah and not a.uji:
            baru = GK.LAJUR_KEW if butiran else GK.LAJUR_KEW[:3]
            lajur += [x for x in baru + ['gred_pada'] if x not in lajur]
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows:
                    w.writerow({x: r.get(x, '') for x in lajur})
    ring = {'uji': a.uji, 'baris_disasar': n_isi,
            'sebelum': {f'{k}|{s}': v for (k, s), v in sorted(sebelum.items())},
            'gred_baharu': {f'{k}|{g}': v for (k, g), v in sorted(gred_baru.items())},
            'baki_tiada': {f'{k}|{s}': v for (k, s), v in sorted(selepas.items())},
            'baki_terperinci': {k: sorted(set(v)) for k, v in sorted(baki.items())}}
    print(json.dumps(ring, ensure_ascii=False, indent=1))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(ring, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
