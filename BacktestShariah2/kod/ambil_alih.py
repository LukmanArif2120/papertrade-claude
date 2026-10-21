# ambil_alih.py — penapis saham yang sedang diambil alih (keputusan pengguna 21 Okt 2026, selepas 13 kaedah membeli BRZE
# sehari selepas Salesforce mengumumkan belian tunai Braze). Harga saham sasaran ambil alih tunai terkunci hampir pada
# harga tawaran: lonjakan pada hari pengumuman kelihatan seperti momentum/breakout, tetapi ruang naik hampir tiada dan
# risiko jatuh besar jika perjanjian gagal. Isyarat beli bagi saham itu = isyarat palsu.
#
# Dua sumber (tiada pandang depan: hanya bar <= sesi S dan rekod bertarikh <= S):
# 1. Corak harga (automatik): hari pengumuman = jurang buka >= +10%, volum >= 4x median 50 hari, julat hari itu <= 3%
#    (saham biasa yang melonjak kerana earnings berjulat lebar), dan saham itu biasanya bergerak (median julat 50 hari
#    sebelum >= 1%; kelas saham tidak cair seperti BIO.B tidak dikira). Saham kekal ditapis selagi harga masih terkunci:
#    10 bar terakhir sejak pengumuman (atau semua bar jika kurang) median julat <= 1.5% dan julat tutup <= 4%.
#    Pengumuman dicari dalam 260 bar terakhir (perjanjian boleh mengambil masa hingga setahun).
# 2. Senarai sah `data/ambil_alih.csv` (saham, tarikh_umum, tarikh_tamat, pembeli, harga_tawaran, bayaran, sumber):
#    ditapis dari tarikh_umum hingga sebelum tarikh_tamat (kosong = belum selesai). bayaran 'bukan' = bukan ambil alih:
#    pengesanan automatik dimatikan bagi saham itu. Perjanjian bayaran saham (harga ikut pembeli, tidak terkunci) perlu
#    dimasukkan di sini kerana corak harga tidak mengesannya.
#
#   python3 kod/ambil_alih.py senarai [--stor DIR] [--sesi S]     # saham ditapis pada sesi S (lalai: bar terakhir)
#   python3 kod/ambil_alih.py posisi [--folder PT] [--stor DIR] [--tulis]
#       Posisi Papertrade C yang dibeli pada/selepas tarikh pengumuman = isyarat palsu: tidak_sah dan kedua-dua lorong
#       ditutup pada tutup bar terakhir (tanda_posisi). Dijalankan setiap malam selepas kemas kini posisi. Tanpa --tulis = cuba.
import argparse, csv, json, os, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(BS2, 'standard'))

SENARAI = os.path.join(BS2, 'data', 'ambil_alih.csv')
VERSI = 'ambil_alih v1 (21 Okt 2026)'   # + cincangan data/ambil_alih.csv: versi()
JURANG_MIN = 0.10
VOLUM_X = 4.0
JULAT_UMUM_MAKS = 0.03
JULAT_BIASA_MIN = 0.01
JULAT_KUNCI_MAKS = 0.015
BAND_KUNCI_MAKS = 0.04
BAR_KUNCI = 10
CARI_BAR = 260
LAJUR = ['saham', 'tarikh_umum', 'tarikh_tamat', 'pembeli', 'harga_tawaran', 'bayaran', 'sumber']


def versi(path=SENARAI):
    """VERSI + cincangan senarai sah: lejar.py membina semula lejar apabila peraturan atau senarai berubah."""
    import hashlib
    h = hashlib.sha1(open(path, 'rb').read()).hexdigest()[:8] if path and os.path.exists(path) else '-'
    return f'{VERSI}; senarai {h}'


def baca_senarai(path=SENARAI):
    if not path or not os.path.exists(path):
        return []
    return [r for r in csv.DictReader(open(path, encoding='utf-8')) if r.get('saham')]


def kesan_harga(g):
    """Tarikh pengumuman (Timestamp) jika harga g (bar <= sesi semasa) masih terkunci selepas corak ambil alih, atau None."""
    if g is None or len(g) < 60:
        return None
    g = g.iloc[-(CARI_BAR + 60):]
    c, o, v = g.close.values.astype(float), g.open.values.astype(float), g.volume.values.astype(float)
    rng = (g.high.values - g.low.values) / np.where(c > 0, c, np.nan)
    pc = np.r_[np.nan, c[:-1]]
    mv = pd.Series(v).rolling(50, min_periods=20).median().shift(1).values
    mr = pd.Series(rng).rolling(50, min_periods=20).median().shift(1).values
    with np.errstate(invalid='ignore', divide='ignore'):
        ev = (o / pc - 1 >= JURANG_MIN) & (v >= VOLUM_X * mv) & (rng <= JULAT_UMUM_MAKS) & (mr >= JULAT_BIASA_MIN)
    ev[:max(0, len(g) - CARI_BAR)] = False
    i = np.flatnonzero(ev)
    if not len(i):
        return None
    e = int(i[-1]); w = slice(max(e, len(g) - BAR_KUNCI), len(g))
    cw = c[w]
    if np.nanmedian(rng[w]) <= JULAT_KUNCI_MAKS and cw.max() / cw.min() - 1 <= BAND_KUNCI_MAKS:
        return g.index[e]
    return None


def tapis(frames, S=None, senarai=None):
    """{saham: maklumat} saham yang ditapis pada sesi S (lalai: bar terakhir setiap saham). frames = {ticker: DataFrame
    open/high/low/close/volume berindeks tarikh}. Bar > S diabaikan."""
    S = pd.Timestamp(S) if S is not None else None
    rekod = baca_senarai() if senarai is None else senarai
    bukan = {r['saham'] for r in rekod if (r.get('bayaran') or '').strip().lower() == 'bukan'}
    out = {}
    for t, g in frames.items():
        if t in bukan:
            continue
        if S is not None and len(g) and g.index[-1] > S:
            g = g[g.index <= S]
        e = kesan_harga(g)
        if e is not None:
            out[t] = dict(saham=t, tarikh_umum=str(e.date()), sumber='corak harga', pembeli='', harga_tawaran='')
    Ss = str(S.date()) if S is not None else None
    for r in rekod:
        b = (r.get('bayaran') or '').strip().lower()
        if b == 'bukan' or not r.get('tarikh_umum'):
            continue
        if Ss is not None and (r['tarikh_umum'] > Ss or (r.get('tarikh_tamat') and r['tarikh_tamat'] <= Ss)):
            continue
        if Ss is None and r.get('tarikh_tamat'):
            g = frames.get(r['saham'])
            if g is None or not len(g) or str(g.index[-1].date()) >= r['tarikh_tamat']:
                continue
        out[r['saham']] = dict(saham=r['saham'], tarikh_umum=r['tarikh_umum'], sumber='senarai',
                               pembeli=r.get('pembeli', ''), harga_tawaran=r.get('harga_tawaran', ''))
    return out


def teks(x):
    s = f"saham diambil alih (umum {x['tarikh_umum']}"
    if x.get('pembeli'):
        s += f", {x['pembeli']}"
    if x.get('harga_tawaran'):
        s += f", tawaran ${x['harga_tawaran']}"
    return s + f"; {x['sumber']})"


def tarikh_umum_awal(t, frames, senarai):
    """Tarikh pengumuman paling awal yang diketahui bagi saham t (senarai dahulu, kemudian corak harga pada bar terakhir)."""
    d = [r['tarikh_umum'] for r in senarai if r['saham'] == t and r.get('tarikh_umum')
         and (r.get('bayaran') or '').strip().lower() != 'bukan']
    if d:
        return min(d)
    e = kesan_harga(frames.get(t))
    return str(e.date()) if e is not None else None


# ---------------------------------------------------------------- CLI
def _frames(stor):
    from stor import muat, frames_dict
    fr, _ = frames_dict(muat(stor))
    return fr


def cmd_senarai(a):
    fr = _frames(a.stor)
    x = tapis(fr, a.sesi)
    for t in sorted(x):
        print(t, teks(x[t]))
    print(f'{len(x)} saham ditapis', file=sys.stderr)


def nombor_teks(x):
    return f'{x:.4f}'.rstrip('0').rstrip('.')


def tanda_posisi(folder, frames, tulis=True, senarai=None):
    """Posisi Papertrade C (claude*.csv) yang dibeli pada/selepas tarikh pengumuman ambil alih = isyarat palsu:
    tidak_sah = True (tidak dikira dalam prestasi) dan kedua-dua lorong ditutup pada tutup bar terakhir saham itu (saham
    delist selepas perjanjian selesai: tutup akhir). Posisi yang dibeli selepas bar terakhir stor ditanda dahulu dan ditutup
    pada larian seterusnya. Posisi yang dibeli sebelum pengumuman tidak diubah. Pulang senarai perubahan."""
    import sahkan as SH
    sen = baca_senarai() if senarai is None else senarai
    akhir = max((g.index[-1] for g in frames.values() if len(g)), default=None)
    aktif = tapis(frames, akhir, sen)
    for r in sen:   # termasuk saham yang sudah delist (ATKR: bar akhir sebelum sesi semasa)
        if r['saham'] not in aktif and (r.get('bayaran') or '').strip().lower() != 'bukan' and r.get('tarikh_umum'):
            aktif[r['saham']] = dict(saham=r['saham'], tarikh_umum=r['tarikh_umum'], sumber='senarai',
                                     pembeli=r.get('pembeli', ''), harga_tawaran=r.get('harga_tawaran', ''))
    fail = sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('claude') and f.endswith('.csv'))
    ubah_semua = []
    for p in fail:
        lajur, rows = SH.baca(p)
        ubah = False
        for r in rows:
            t = r.get('saham'); x = aktif.get(t)
            if not x or SH.benar(r.get('tidak_dibeli')) or not r.get('tarikh_beli') or not r.get('harga_beli'):
                continue
            if SH.benar(r.get('tidak_sah')) and not (r.get('sebab_tidak_sah') or '').startswith('isyarat palsu'):
                continue
            umum = tarikh_umum_awal(t, frames, sen) or x['tarikh_umum']
            if r['tarikh_beli'] < umum:
                continue      # dibeli sebelum pengumuman: isyarat sah, untung/rugi sebenar dikekalkan
            if SH.benar(r.get('keluar')) and SH.benar(r.get('keluar_henti', 'True')) and SH.benar(r.get('tidak_sah')):
                continue      # sudah ditutup
            sebab = f'isyarat palsu: {teks(x)}'
            r['tidak_sah'] = 'True'; r['sebab_tidak_sah'] = sebab; ubah = True
            g = frames.get(t)
            if g is None or not len(g) or str(g.index[-1].date()) < r['tarikh_beli']:
                if not SH.benar(r.get('keluar')):
                    r['isyarat_keluar'] = 'Isyarat palsu (saham diambil alih) — ditutup pada tutup sesi beli (menunggu)'
                ubah_semua.append((os.path.basename(p), t, r.get('kaedah'), r['tarikh_beli'], 'menunggu', '', ''))
                continue
            tk = str(g.index[-1].date()); hk = float(g.close.iloc[-1])
            hb = float(r['harga_beli']); u = f'{(hk / hb - 1) * 100:.2f}'
            nota_k = f'Keluar: isyarat palsu, {teks(x)} — tutup {tk} @ {hk:.2f}'
            if not SH.benar(r.get('keluar')):
                r.update(keluar='True', tarikh_keluar=tk, harga_keluar=nombor_teks(hk), untung_akhir_pct=u,
                         harga_terkini=nombor_teks(hk), untung_pct=u, isyarat_keluar=nota_k)
            if 'keluar_henti' in lajur and not SH.benar(r.get('keluar_henti')):
                r.update(keluar_henti='True', tarikh_keluar_henti=tk, harga_keluar_henti=nombor_teks(hk),
                         untung_henti_pct=u, status_henti=nota_k)
            if 'tutup_semua' in lajur:
                r['tutup_semua'] = 'True'
            ubah_semua.append((os.path.basename(p), t, r.get('kaedah'), r['tarikh_beli'], tk, hk, u))
        if ubah and tulis:
            SH.tulis(p, lajur, rows)
    return ubah_semua


def cmd_posisi(a):
    fr = _frames(a.stor)
    x = tanda_posisi(a.folder, fr, a.tulis)
    for j in x:
        print(*j, sep='\t')
    print(json.dumps(dict(posisi=len(x), ditutup=sum(j[4] != 'menunggu' for j in x), menunggu=sum(j[4] == 'menunggu' for j in x),
                          saham=sorted({j[1] for j in x}), ditulis=bool(a.tulis)), ensure_ascii=False), file=sys.stderr)


def main(argv=None):
    from stor import muat  # noqa: F401  (pastikan laluan kod/ betul)
    ap = argparse.ArgumentParser(description=__doc__)
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('senarai'); s.add_argument('--stor', default=os.path.join(BS2, 'data', 'harga', 'stor')); s.add_argument('--sesi')
    p = sp.add_parser('posisi'); p.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    p.add_argument('--stor', default=os.path.join(BS2, 'data', 'harga', 'stor')); p.add_argument('--tulis', action='store_true')
    a = ap.parse_args(argv)
    return {'senarai': cmd_senarai, 'posisi': cmd_posisi}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main() or 0)
