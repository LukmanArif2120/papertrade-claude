# isi_audit.py — isi medan posisi/watchlist yang kosong selepas audit dashboard 23 Okt 2026 (keputusan pengguna: data tidak
# boleh dibiar kosong). Hanya baris yang medannya kosong diubah; nilai yang sudah ada tidak disentuh.
#   RS        : saham baru disenarai (< 253 bar) -> RS anggaran suku tersedia (gred.rs_pendek) pada sesi rujukan; gred maks C.
#   Industri  : industri < 3 saham (tidak digred dalam gred_kumpulan) -> sandaran gred sektor sesi rujukan, ditanda gred_pada.
#   tarikh_isyarat (Moomoo lama, sumber harian / log_v1): sesi sebelum tarikh_beli (sama dengan harian_c.kumpul_posisi).
#               Sumber luar (strategi luar, tiada isyarat kaedah) dibiar kosong.
# Sesi rujukan = tarikh_isyarat, tarikh_data (watchlist), atau sesi sebelum tarikh_beli.
#   python3 BacktestShariah2/standard/isi_audit.py [--folder papertrade] [--harga data/harga/stor] [--uji]
import argparse, json, os, sys
from collections import Counter

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
BS2 = os.path.dirname(HERE)
import gred as G  # noqa: E402
import sahkan as SH  # noqa: E402
from gred_isi_semula import fail_posisi  # noqa: E402
from gred_kira_semula import peta_kumpulan_sejarah  # noqa: E402

KOSONG = ('', '–', '-')


def kosong(v):
    return str(v if v is not None else '').strip() in KOSONG


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    ap.add_argument('--harga', default=os.path.join(BS2, 'data', 'harga', 'stor'))
    ap.add_argument('--rs', default=os.path.join(BS2, 'data', 'rs'))
    ap.add_argument('--kumpulan', default=os.path.join(BS2, 'data', 'kumpulan', 'gred_kumpulan_sejarah.csv'))
    ap.add_argument('--uji', action='store_true')
    a = ap.parse_args(argv)
    c, _ = G.muat_harga(a.harga)
    spy = G.muat_spy(a.harga)
    sesi = list(c.index)
    kum = peta_kumpulan_sejarah(a.kumpulan)
    if os.path.exists(a.kumpulan.replace('_sejarah', '')):
        kum.update(peta_kumpulan_sejarah(a.kumpulan.replace('_sejarah', '')))
    jenis = G.peta_jenis_kaedah()
    cache, kira, contoh = {}, Counter(), []

    def rujukan(r):
        t = r.get('tarikh_isyarat') or r.get('tarikh_data')
        if t:
            return pd.Timestamp(t[:10])
        tb = r.get('tarikh_beli')
        x = [s for s in sesi if tb and s < pd.Timestamp(tb)]
        return x[-1] if x else None

    fail = fail_posisi(a.folder) + [os.path.join(a.folder, 'watchlist.csv')]
    for p in fail:
        if not os.path.exists(p):
            continue
        lajur, rows = SH.baca(p); ubah = 0; m_fail = os.path.basename(p) == 'moomoo.csv'
        for r in rows:
            if SH.benar(r.get('tidak_dibeli')):
                continue
            t = r.get('saham') or r.get('Saham')
            # tarikh_isyarat Moomoo lama
            if m_fail and kosong(r.get('tarikh_isyarat')) and r.get('sumber') in ('harian', 'log_v1') and r.get('tarikh_beli'):
                D = rujukan(r)
                if D is not None:
                    r['tarikh_isyarat'] = str(D.date()); kira['tarikh_isyarat'] += 1; ubah += 1
            if kosong(r.get('gred_keseluruhan')) and kosong(r.get('gred_rs')) and kosong(r.get('gred_industri')):
                continue          # baris tanpa gred langsung (bukan skop skrip ini)
            D = rujukan(r)
            if D is None:
                continue
            # RS
            if kosong(r.get('gred_rs')) and 'gred_rs' in lajur:
                if D not in cache:
                    cc = c[c.index <= D]
                    cache[D] = G.rs_semua(cc, spy, a.rs)
                rsd, atas = cache[D]
                if t in rsd.index and pd.notna(rsd.loc[t, 'rs']):
                    G.isi_rs(r, rsd.loc[t], atas); kira['rs'] += 1; ubah += 1
                    contoh.append(f"{t} RS {r['rs_rating']} {r['gred_rs']} ({r['rs_sumber']}) @ {D.date()}")
                else:
                    kira['rs tiada (< 64 bar)'] += 1
            # Industri
            if kosong(r.get('gred_industri')) and r.get('industri_us') and 'gred_industri' in lajur:
                k = kum.get(str(D.date()))
                su = G.SEKTOR_INDUSTRI.get(r['industri_us']) if hasattr(G, 'SEKTOR_INDUSTRI') else None
                su = su or r.get('sektor_us')
                if k and su in k[0]:
                    s1, g1 = k[0][su]
                    r['skor_industri'] = round(s1, 1); r['gred_industri'] = g1
                    if G.SANDARAN_INDUSTRI not in (r.get('gred_pada') or ''):
                        r['gred_pada'] = (r.get('gred_pada') or '') + '; ' + G.SANDARAN_INDUSTRI
                    if r.get('gred_keseluruhan') not in (None,):
                        r['gred_keseluruhan'] = G.keseluruhan_baris(r, jenis)
                    kira['industri sandaran sektor'] += 1; ubah += 1
                    contoh.append(f"{t} industri {r['industri_us']} -> sektor {su} {g1} @ {D.date()}")
                else:
                    kira['industri tiada snapshot'] += 1
        if ubah and not a.uji:
            SH.tulis(p, lajur, rows)
    print(json.dumps(dict(kira=dict(kira), contoh=contoh[:12], uji=a.uji), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
