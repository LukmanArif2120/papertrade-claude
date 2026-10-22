# tidak_layak.py — saham yang isyaratnya tidak boleh dipercayai (keputusan pengguna 21 Okt 2026). Satu pintu untuk
# scanner.py, standard/harian_c.py dan standard/lejar.py:
# 1. Diambil alih (kod/ambil_alih.py): harga terkunci pada harga tawaran -> isyarat palsu.
# 2. Tidak cair: 20 bar terakhir (<= sesi S) ada >= 3 bar tanpa julat (tinggi = rendah), >= 2 bar tanpa volum, atau median
#    nilai dagangan harian (tutup x volum) < USD100 ribu. Bar sebegitu (cth. BIO.B, KELYB, SENEB) mencetus breakout/jurang
#    palsu dan harga buka tidak boleh diisi. Isyarat ditolak; posisi sedia ada tidak diubah.
# 3. Delist / tiada data: tiada bar bagi >= 5 sesi pasaran berturut (saham ditarik selepas ambil alih siap, cth. ATKR
#    16 Okt 2026, SLP, QRVO). Saham ini tidak lagi beri isyarat; posisi terbuka tersangkut -> kedua-dua lorong ditutup pada
#    tutup bar terakhir (anggaran nilai tunai; posisi kekal sah). Liputan data pasaran disemak dahulu oleh pemanggil.
#
#   python3 kod/tidak_layak.py senarai [--stor DIR] [--sesi S]
#   python3 kod/tidak_layak.py posisi [--folder PT] [--stor DIR] [--tulis]
#       Papertrade C: (a) ambil_alih.tanda_posisi (isyarat palsu -> tidak_sah, tutup); (b) posisi saham delist -> tutup
#       pada tutup bar terakhir; (c) saham tidak cair pada sesi isyarat -> tidak_sah (22 Okt 2026). Tanpa --tulis = cuba. Dijalankan setiap pagi selepas langkah keluar (rutin 6:02 langkah 2c).
import argparse, json, os, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(BS2, 'standard'))
import ambil_alih as AA  # noqa: E402

VERSI = 'tidak_layak v1 (21 Okt 2026): tidak cair 3/2/100k, delist 5 sesi'
BAR_CAIR = 20
JULAT0_MAKS = 3        # bar tanpa julat dalam 20 bar -> tidak cair
VOL0_MAKS = 2          # bar tanpa volum dalam 20 bar -> tidak cair
NILAI_MIN = 100_000.0  # median tutup x volum (USD)
DELIST_SESI = 5


def versi():
    """Kunci peraturan (termasuk senarai ambil alih): lejar.py membina semula lejar apabila berubah."""
    return f'{VERSI}; {AA.versi()}'


def tidak_cair(g):
    """Teks sebab jika 20 bar terakhir g tidak cair, atau None."""
    if g is None or len(g) < BAR_CAIR:
        return None
    w = g.iloc[-BAR_CAIR:]
    j0 = int(((w.high - w.low).abs() <= 1e-9).sum()); v0 = int((w.volume <= 0).sum())
    nilai = float((w.close * w.volume).median())
    if j0 >= JULAT0_MAKS or v0 >= VOL0_MAKS or nilai < NILAI_MIN:
        return f'tidak cair (20 bar: {j0} tanpa julat, {v0} tanpa volum, median nilai ${nilai:,.0f})'
    return None


def sesi_tanpa_bar(g, sesi, S):
    """Bilangan sesi pasaran (senarai `sesi`) selepas bar terakhir g hingga S."""
    akhir = g.index[-1] if g is not None and len(g) else None
    if akhir is None:
        return len(sesi)
    sesi = pd.DatetimeIndex(sesi)
    return int(((sesi > akhir) & (sesi <= pd.Timestamp(S))).sum())


def tapis(frames, S=None, senarai=None):
    """{saham: dict(sebab='ambil alih'|'tidak cair', teks=...)} pada sesi S (lalai: bar terakhir). Bar > S diabaikan."""
    S = pd.Timestamp(S) if S is not None else None
    out = {t: dict(sebab='ambil alih', teks=AA.teks(x), **x) for t, x in AA.tapis(frames, S, senarai).items()}
    for t, g in frames.items():
        if t in out:
            continue
        if S is not None and len(g) and g.index[-1] > S:
            g = g[g.index <= S]
        x = tidak_cair(g)
        if x:
            out[t] = dict(saham=t, sebab='tidak cair', teks=x)
    return out


def tutup_delist(folder, frames, sesi, tulis=True):
    """Posisi Papertrade C yang masih terbuka (lorong 1 atau 2) bagi saham tanpa bar >= DELIST_SESI sesi: tutup lorong yang
    terbuka pada tutup bar terakhir. Pulang senarai perubahan."""
    import sahkan as SH
    S = pd.DatetimeIndex(sesi)[-1]
    out = []
    fail = sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('claude') and f.endswith('.csv'))
    for p in fail:
        lajur, rows = SH.baca(p)
        ubah = False
        for r in rows:
            if SH.benar(r.get('tidak_dibeli')) or not r.get('tarikh_beli') or not r.get('harga_beli'):
                continue
            l1 = not SH.benar(r.get('keluar')); l2 = 'keluar_henti' in lajur and not SH.benar(r.get('keluar_henti'))
            if not (l1 or l2):
                continue
            g = frames.get(r['saham'])
            if g is None or not len(g) or str(g.index[-1].date()) < r['tarikh_beli']:
                continue
            n = sesi_tanpa_bar(g, sesi, S)
            if n < DELIST_SESI:
                continue
            tk = str(g.index[-1].date()); hk = float(g.close.iloc[-1]); hb = float(r['harga_beli'])
            u = f'{(hk / hb - 1) * 100:.2f}'; ht = AA.nombor_teks(hk)
            nota = f'Keluar: delist / tiada data {n} sesi — tutup akhir {tk} @ {hk:.2f}'
            if l1:
                r.update(keluar='True', tarikh_keluar=tk, harga_keluar=ht, untung_akhir_pct=u, harga_terkini=ht, untung_pct=u,
                         isyarat_keluar=nota)
            if l2:
                r.update(keluar_henti='True', tarikh_keluar_henti=tk, harga_keluar_henti=ht, untung_henti_pct=u, status_henti=nota)
            if 'tutup_semua' in lajur:
                r['tutup_semua'] = 'True'
            ubah = True
            out.append((os.path.basename(p), r['saham'], r.get('kaedah'), r['tarikh_beli'], tk, hk, u))
        if ubah and tulis:
            SH.tulis(p, lajur, rows)
    return out


def tanda_tidak_cair(folder, frames, tulis=True):
    """Posisi Papertrade C yang sahamnya tidak cair pada sesi isyarat (20 bar <= tarikh_isyarat; tiada pandang depan) ->
    tidak_sah (keputusan pengguna 22 Okt 2026: konsisten dengan Lejar, yang menolak isyarat itu). Posisi tidak ditutup;
    harga dan keluar terus dikemas kini tetapi tidak dikira dalam prestasi. Pulang senarai perubahan."""
    import sahkan as SH
    out = []
    for p in sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('claude') and f.endswith('.csv')):
        lajur, rows = SH.baca(p)
        ubah = False
        for r in rows:
            if SH.benar(r.get('tidak_dibeli')) or SH.benar(r.get('tidak_sah')) or not r.get('harga_beli'):
                continue
            g = frames.get(r.get('saham')); ti = r.get('tarikh_isyarat') or r.get('tarikh_beli')
            if g is None or not ti:
                continue
            x = tidak_cair(g[g.index <= pd.Timestamp(ti)])
            if not x:
                continue
            r['tidak_sah'] = 'True'; r['sebab_tidak_sah'] = f'isyarat palsu: saham {x} pada {ti}'
            ubah = True
            out.append((os.path.basename(p), r['saham'], r.get('kaedah'), r.get('tarikh_beli')))
        if ubah and tulis:
            SH.tulis(p, lajur, rows)
    return out


def posisi(folder, frames, sesi, tulis=True):
    """Langkah pagi/malam: isyarat palsu ambil alih (tidak_sah, tutup) kemudian posisi delist (tutup). Pulang ringkasan."""
    aa = AA.tanda_posisi(folder, frames, tulis)
    dl = tutup_delist(folder, frames, sesi, tulis)
    tc = tanda_tidak_cair(folder, frames, tulis)
    return dict(ambil_alih=dict(ditutup=sum(x[4] != 'menunggu' for x in aa), menunggu=sum(x[4] == 'menunggu' for x in aa),
                                saham=sorted({x[1] for x in aa})),
                delist=dict(ditutup=len(dl), saham=sorted({x[1] for x in dl})),
                tidak_cair=dict(tidak_sah=len(tc), saham=sorted({x[1] for x in tc})), _baris=aa + dl + tc)


# ---------------------------------------------------------------- CLI
def _muat(stor):
    from stor import muat, frames_dict
    fr, idx = frames_dict(muat(stor))
    return fr, list(idx['SPY'].index)


def cmd_senarai(a):
    fr, _ = _muat(a.stor)
    x = tapis(fr, a.sesi)
    for t in sorted(x, key=lambda t: (x[t]['sebab'], t)):
        print(t, x[t]['teks'], sep='\t')
    print(json.dumps({k: sum(v['sebab'] == k for v in x.values()) for k in ('ambil alih', 'tidak cair')}, ensure_ascii=False),
          file=sys.stderr)


def cmd_posisi(a):
    fr, sesi = _muat(a.stor)
    rk = posisi(a.folder, fr, sesi, a.tulis)
    for j in rk.pop('_baris'):
        print(*j, sep='\t')
    rk['ditulis'] = bool(a.tulis)
    print(json.dumps(rk, ensure_ascii=False), file=sys.stderr)


def main(argv=None):
    stor = os.path.join(BS2, 'data', 'harga', 'stor')
    ap = argparse.ArgumentParser(description='Saham tidak layak: diambil alih, tidak cair, delist')
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('senarai'); s.add_argument('--stor', default=stor); s.add_argument('--sesi')
    p = sp.add_parser('posisi'); p.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    p.add_argument('--stor', default=stor); p.add_argument('--tulis', action='store_true')
    a = ap.parse_args(argv)
    return {'senarai': cmd_senarai, 'posisi': cmd_posisi}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main() or 0)
