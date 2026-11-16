# f_utama_db.py — dokumen db dashboard `carian/f_utama` (+ `_2`…): senarai utama setup F (Rujukan → Setup F).
# Sumber: kajian/carian_setup/hasil/CS13/senarai_utama.csv dan bacaan.json (dijana cs_daftar13.py, pindaan (v)); cara pegang
# kedua "pegang lebih lama" (keputusan pengguna 16 Nov 2026 "B" selepas CS14): hasil/CS14/setup.csv.gz dan cara.csv
# (cs_pegang14.py, pindaan (x); cara `r0.t2.0` = jual bila tutup di bawah purata 50 hari, tiada had masa).
# Dokumen STATIK: ia berubah hanya apabila senarai utama dijana semula, jadi ia TIDAK ditulis oleh jana_db.py dan
# tidak berada dalam daftar versi `meta/versi_db`; tolak secara manual selepas setiap pusingan carian yang mengubahnya:
#   python3 BacktestShariah2/standard/f_utama_db.py --keluar <folder>
#   -> <folder>/carian/f_utama.json, f_utama_2.json …; senarai fail dicetak. Tolak SEMUA dalam SATU batch ArtifactData
#   (collection `carian`; if_version bagi dokumen yang sudah wujud). Halaman membacanya dengan subBhg().
# Bentuk: {tajuk, sumber, dibina, n, n_pilihan, n_lama, n_baharu, ujian{…}, semak_masa{…}, pegang, pegang2, banding{…}, kol[],
#          kamus{pra, nama, pen}, rows[[…]]}; baris padat sejajar `kol`: peratus x10 (tangkap, rawak, m5, menang, rugi15,
#          menang2, rugi2), x100 (purata, k3, purata2). Lajur baharu hanya DITAMBAH di hujung `kol` (halaman membaca ikut nama).
import argparse
import json
import os
import sys

import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(SINI)
sys.path.insert(0, SINI)
sys.path.insert(0, os.path.join(BS2, 'kajian', 'carian_setup'))
from bahagi_db import bahagi, bait, padat, HAD_DB  # noqa: E402

CS13 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS13')
CS14 = os.path.join(BS2, 'kajian', 'carian_setup', 'hasil', 'CS14')
CARA1, CARA2 = 'r0.t1.126', 'r0.t2.0'                    # cara sekarang (pegang B) dan "pegang lebih lama" (pilihan pengguna B, 16 Nov 2026)
KOL = ['id', 'asal', 'pil', 'pra', 'nama', 'pen', 'beli', 'shar', 'tangkap', 'rawak', 'm5', 'menang', 'purata', 'rugi15', 'hari', 'k3', 'n',
       'menang2', 'purata2', 'rugi2', 'hari2']
HAD_BAHAGI = 200000
PEGANG = ('Beli pada buka esok · stop loss 4×ATR14 · pegang sekurang-kurangnya 20 hari (20 hari ialah minimum, bukan had), kemudian jual '
          'bila harga tutup di bawah purata 20 hari · paling lama 6 bulan · tiada jualan pada hari beli')
PEGANG2 = ('Sama hingga hari ke-20; selepas itu jual hanya bila harga tutup di bawah purata 50 hari · tiada had masa')


def banding(folder14=CS14):
    """Ringkasan dua cara pegang (nilai tengah semua setup, saham yang carian tidak lihat) + saham rawak dengan cara sama."""
    T = pd.read_csv(os.path.join(folder14, 'cara.csv'))
    T = T[T.set == 'B'].set_index('cara')
    g = lambda c, awal='': {k: round(float(T.loc[c, awal + k]), 4) for k in ('purata', 'menang', 'rugi15')}
    return dict(kini=dict(g(CARA1), hari=float(T.loc[CARA1, 'sesi_med'])), lama=dict(g(CARA2), hari=float(T.loc[CARA2, 'sesi_med'])),
                rawak_kini=g(CARA1, 'rawak_'), rawak_lama=g(CARA2, 'rawak_'))


def bina(folder=CS13, folder14=CS14):
    """Dokumen penuh (belum dibahagi) daripada senarai_utama.csv + cara pegang kedua (CS14); None jika fail tiada."""
    import cs_ringkas
    f = os.path.join(folder, 'senarai_utama.csv')
    if not os.path.exists(f):
        return None
    U = pd.read_csv(f).fillna({'prasyarat': '', 'penapis': ''})
    X = pd.read_csv(os.path.join(folder14, 'setup.csv.gz')).set_index('id').loc[U.id]
    assert (abs(X[CARA1 + ':menang'].to_numpy() - U.menang_B.to_numpy()) < 2e-4).all(), 'CS14 tidak sepadan dengan senarai utama'
    for k, a in (('menang2', 'menang'), ('purata2', 'purata'), ('rugi2', 'rugi15'), ('hari2', 'sesi_med')):
        U[k] = X[f'{CARA2}:{a}'].to_numpy()
    J = json.load(open(os.path.join(folder, 'bacaan.json'), encoding='utf-8'))
    U['nama_p'] = U.nama.map(cs_ringkas.nama_pendek)
    kamus, ix = {}, {}
    for k, kol in (('pra', 'prasyarat'), ('nama', 'nama_p'), ('pen', 'penapis')):
        kamus[k] = sorted(set(U[kol]))
        ix[k] = {v: i for i, v in enumerate(kamus[k])}
    b = lambda x, kali: None if x != x else int(round(float(x) * kali))
    rows = []
    for r in U.itertuples():
        rows.append([r.id, int(r.asal == 'baharu'), int(bool(r.pilihan)), ix['pra'][r.prasyarat], ix['nama'][r.nama_p], ix['pen'][r.penapis],
                     b(r.setahun, 1), b(r.shariah_setahun, 1), b(r.terus, 1000), b(r.a_terus, 1000), b(r.m5, 1000), b(r.menang_B, 1000),
                     b(r.purata_B, 10000), b(r.rugi15_B, 1000), b(r.hari_B, 1), b(r.kl_terus_K3, 10000), int(r.n),
                     b(r.menang2, 1000), b(r.purata2, 10000), b(r.rugi2, 1000), b(r.hari2, 1)])
    sm = J.get('semak_masa') or {}
    return dict(
        tajuk='Senarai utama setup F (saham naik laju) dengan cara pegang B', sumber='kajian/carian_setup/hasil/CS13/senarai_utama.csv',
        dibina=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC'), n=len(U), n_pilihan=int(U.pilihan.sum()),
        n_lama=int((U.asal == 'lama').sum()), n_baharu=int((U.asal == 'baharu').sum()),
        n_earnings=int(U.prasyarat.str.contains('earnings dalam 1-').sum()),
        ujian=dict(calon=J.get('n_calon'), lulus=J.get('n_lulus'), kembar=J.get('n_kembar'), lulus_calon=J.get('lulus_calon'),
                   lulus_kawalan=J.get('lulus_kawalan'), k3_calon=J.get('k3_calon'), k3_kawalan=J.get('k3_kawalan')),
        semak_masa={k: {a: (round(x, 4) if isinstance(x, float) else x) for a, x in v.items()} for k, v in sm.items()},
        pegang=PEGANG, pegang2=PEGANG2, banding=banding(folder14), kol=KOL, kamus=kamus, rows=rows,
        nota='Pangkat backtest pada saham yang carian tidak lihat (2010–2026); BUKAN bukti dan BUKAN keputusan wang sebenar. '
             'Tiada saham delist dalam data. Tiada papertrade tanpa keputusan pengguna.')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluar', required=True)
    a = ap.parse_args(argv)
    doc = bina()
    if doc is None:
        raise SystemExit('senarai_utama.csv tiada: jalankan cs_daftar13.py lapor dahulu')
    out = []
    for doc_id, dd in bahagi(doc, 'f_utama', HAD_BAHAGI):
        sz = bait(dd)
        if sz >= HAD_DB:
            raise SystemExit(f'carian/{doc_id}: {sz} bait melebihi had db {HAD_DB}')
        p = os.path.join(a.keluar, 'carian', doc_id + '.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(padat(dd))
        out.append(dict(collection='carian', doc_id=doc_id, file_path=os.path.abspath(p), bait=sz))
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return out


if __name__ == '__main__':
    main()
