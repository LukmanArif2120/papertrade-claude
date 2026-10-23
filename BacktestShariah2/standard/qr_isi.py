# qr_isi.py — isi gred QR dan pemangkin yang kosong ('–') selepas audit dashboard 23 Okt 2026 (keputusan pengguna: data tidak
# boleh dibiar kosong; pemangkin dikira K1/K2 dan ditanda tanpa veto berita).
#   QR       : tarikh earnings seterusnya daripada kalendar gabungan (kalendar_earnings.py: Nasdaq, yfinance, Moomoo) pada sesi
#              rujukan asal (gred_pada "QR pada X", atau tarikh_isyarat / tarikh_data / hari bekerja sebelum tarikh_beli).
#              Siri tidak berterusan -> anggaran kitaran (laporan lalu + median jarak laporan 3 tahun), sumber "anggaran (…)".
#              Tiada sebarang tarikh dalam semua sumber -> kekal '–' (sebab dilapor).
#   Pemangkin: kosong -> gred.nilai_pemangkin tanpa berita (K1 premium pengumuman + K2 reaksi earnings lalu daripada harga);
#              v3 sedia ada -> K1 dilaras ikut jarak baharu (gred_qr_semula.laras_pemangkin).
#   gred_keseluruhan dikira semula (gred.keseluruhan_baris). gred_pada ditambah TANDA.
#   python3 BacktestShariah2/standard/qr_isi.py [--folder papertrade] [--harga data/harga/stor] [--uji]
import argparse, json, os, re, statistics, sys
from collections import Counter
from datetime import date, timedelta

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
BS2 = os.path.dirname(HERE)
import gred as G  # noqa: E402
import sahkan as SH  # noqa: E402
import kalendar_earnings as KE  # noqa: E402
from gred_isi_semula import fail_posisi  # noqa: E402
from gred_qr_semula import tarikh_ruj, laras_pemangkin  # noqa: E402

TANDA = 'QR/pemangkin isi semula 23 Okt (kalendar gabungan; pemangkin tanpa berita, veto tidak disemak)'
KOSONG = ('', '–', '-')


def kosong(v):
    return str(v if v is not None else '').strip() in KOSONG


SUMBER_KALENDAR = ('Nasdaq', 'yfinance', 'Moomoo earnings_price_history')


def anggaran(K, t, D, hari_ini=None):
    """Laporan seterusnya dianggar bagi siri tanpa tarikh akan datang yang dipercayai. (date, kaedah) atau (None, sebab).
    1. Musim: laporan pertama (sumber kalendar sahaja, bukan berita) dalam [D − 365, D − 245] hari + 52 minggu.
    2. Kitaran: >= 4 laporan dalam 400 hari lalu dengan jarak sekata (maks/min <= 1.35) -> terakhir + median jarak.
    Ditolak jika jatuh sebelum D, dalam 40 hari selepas laporan terakhir, atau sudah lepas (< hari_ini) tanpa laporan
    direkod dalam sumber (sumber Moomoo dikumpul pada hari isi semula)."""
    hari_ini = hari_ini or date.today()
    x = sorted(d for d in K.get(t, {}) if d < D)
    if not x:
        return None, 'tiada laporan lalu dalam sumber'
    calon = []
    musim = [d for d in x if D - timedelta(days=365) <= d <= D - timedelta(days=245) and K[t][d] in SUMBER_KALENDAR]
    if musim:
        calon.append((musim[0] + timedelta(weeks=52), 'anggaran (suku sama tahun lalu + 52 minggu)'))
    baru = [d for d in x if d > D - timedelta(days=400)]
    jarak = [(b - a).days for a, b in zip(baru, baru[1:]) if (b - a).days > 40]
    if len(jarak) >= 3 and max(jarak) / min(jarak) <= 1.35:
        calon.append((baru[-1] + timedelta(days=int(statistics.median(jarak))), 'anggaran (median jarak laporan sekata)'))
    sebab = 'siri terlalu pendek / tidak sekata untuk anggaran'
    for nx, kaedah in calon:
        if nx < D or (nx - x[-1]).days <= 40:
            continue
        if nx < hari_ini and not any(nx <= d < hari_ini for d in K.get(t, {})):
            sebab = f'anggaran {nx} sudah lepas tanpa laporan direkod'
            continue
        return nx, kaedah
    return None, sebab


def rujukan(r, sesi):
    D = tarikh_ruj(r.get('gred_pada'))
    if D:
        return D
    t0 = r.get('tarikh_isyarat') or r.get('tarikh_data')
    if t0:
        return date.fromisoformat(t0[:10])
    tb = r.get('tarikh_beli')
    x = [s for s in sesi if tb and s.date() < date.fromisoformat(tb[:10])]
    return x[-1].date() if x else None


def hari_imbas(r, D):
    m = re.match(r'\s*(\d{4}-\d\d-\d\d)', r.get('gred_pada') or '')
    if m:
        return date.fromisoformat(m.group(1))
    d = D + timedelta(days=1)
    while d.weekday() > 4:
        d += timedelta(days=1)
    return d


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--harga', default=os.path.join(BS2, 'data', 'harga', 'stor'))
    ap.add_argument('--uji', action='store_true')
    a = ap.parse_args(argv)
    K = KE.muat()
    c, v = G.muat_harga(a.harga)
    spy = G.muat_spy(a.harga)
    sesi = list(c.index)
    jenis = G.peta_jenis_kaedah()
    kira, contoh, baki = Counter(), [], Counter()
    fail = fail_posisi(a.folder) + [os.path.join(a.folder, f) for f in ('senarai_beli.csv', 'watchlist.csv')]
    for p in fail:
        if not os.path.exists(p):
            continue
        lajur, rows = SH.baca(p); ubah = 0
        if 'gred_qr' not in lajur:
            continue
        for r in rows:
            if SH.benar(r.get('tidak_dibeli')) or (kosong(r.get('gred_keseluruhan')) and kosong(r.get('gred_rs'))
                                                    and kosong(r.get('gred_industri'))):
                continue
            q_kos, p_kos = kosong(r.get('gred_qr')), kosong(r.get('gred_pemangkin'))
            if not (q_kos or p_kos):
                continue
            t = r.get('saham') or r.get('Saham'); D = rujukan(r, sesi)
            if not t or not D:
                continue
            hi = hari_imbas(r, D)
            lalu_d, _ = KE.lalu(K, t, D)
            sj = G.sejak_qr(lalu_d, hi) if lalu_d else None
            h = int(float(r['hari_ke_earnings'])) if not kosong(r.get('hari_ke_earnings')) else None
            if q_kos:
                te, sb = KE.seterusnya(K, t, D)
                if te is None:
                    an, sb2 = anggaran(K, t, D)
                    te, sb = (an, sb2) if an else (None, f'{sb}; {sb2}')
                if te is None:
                    baki[f'{t}: {sb}'] += 1
                    lap = sorted(d for d in K.get(t, {}) if D <= d < date.today())
                    r['sumber_earnings'] = (f'tidak diketahui ({sb}; tiada laporan direkod {D}–{date.today() - timedelta(days=1)})'
                                            if not lap else f'tidak diketahui ({sb})')
                    ubah += 1
                else:
                    h = G.hari_dagangan(D, te)
                    r['tarikh_earnings'] = te.isoformat(); r['hari_ke_earnings'] = str(h)
                    r['sumber_earnings'] = G.tanda_pasca_qr(sb, sj)
                    r['gred_qr'] = G.gred_qr(h if (te - D).days <= 35 else None, sj)
                    kira['qr diisi'] += 1; ubah += 1
                    contoh.append(f"{t} @ {D}: {te} ({h}h, {sb}) -> QR {r['gred_qr']}")
                    if not p_kos:
                        laras_pemangkin(r, h)
            if p_kos and t in c.columns:
                hh = h if h is not None and h <= 21 else None
                pr = {}
                if lalu_d:
                    pr.update(earnings_lalu_tarikh=lalu_d.isoformat(), earnings_selepas_tutup=None)
                Dt = pd.Timestamp(D)
                m, g, ring = G.nilai_pemangkin(pr, hi, hh, c[t][c.index <= Dt], v[t][v.index <= Dt],
                                               spy[spy.index <= Dt] if spy is not None else None)
                r['mata_pemangkin'] = m; r['pemangkin'] = ring; r['gred_pemangkin'] = g; r['pemangkin_url'] = ''
                kira['pemangkin diisi'] += 1; ubah += 1
            elif p_kos:
                baki[f'{t}: pemangkin tiada harga'] += 1
            r['gred_keseluruhan'] = G.keseluruhan_baris(r, jenis)
            if TANDA not in (r.get('gred_pada') or ''):
                r['gred_pada'] = (r.get('gred_pada') or '') + '; ' + TANDA
        if ubah and not a.uji:
            SH.tulis(p, lajur, rows)
    print(json.dumps(dict(kira=dict(kira), baki=dict(baki), contoh=contoh[:15], uji=a.uji), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
