"""Carian setup — jejak hadapan kohort F (SPEC pindaan 13 Nov 2026 (f)). Penjejak berasingan; BUKAN Lejar.

  python3 cs_hadapan.py kohort     bina jejak_f/kohort.json daripada registry F + hasil CS04 (peraturan pindaan (f))
  python3 cs_hadapan.py jejak      nilai kohort pada stor harga -> jejak_f/lejar.csv dan jejak_f/RINGKASAN.md

Mekanik = SPEC §4 (sama seperti backtest; pariti lawan `cs_teras` diuji `ujian/test_carian_setup.py`). Hanya isyarat
pada atau selepas MULA dikira. Dikira semula sepenuhnya setiap larian daripada stor harga (tiada keadaan tersimpan).
Tiada order, tiada wang sebenar.
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_lapor as lapor  # noqa: E402
import cs_tala as tala  # noqa: E402
import cs_tangkap as tk  # noqa: E402
import cs_teras as teras  # noqa: E402

BS2 = lapor.BS2
STOR = os.path.join(BS2, 'data', 'harga', 'stor')
KELUAR = os.path.join(BS2, 'jejak_f')
MULA = atom.TEMPOH['hadapan'][0][1]
LAJUR = ['id', 'saham', 'tarikh_isyarat', 'tarikh_beli', 'harga_beli', 'henti', 'status', 'tarikh_keluar', 'harga_keluar',
         'sebab', 'sesi', 'untung_pct', 'harga_terkini', 'm5', 't10', 't20', 'gagal', 'lari']


# ---------- kohort ----------
def dari_takrif(tk_):
    """'M84.t7|F23@5+F26|H2|X11 ATAU X21' -> pencetus, fs, amb, lajur."""
    pc, pen, hen, kel = tk_.split('|')
    fs, amb = [], []
    for x in ([] if pen == '-' else pen.split('+')):
        kod, _, a = x.partition('@')
        fs.append(int(kod[1:]) - 1)
        amb.append(float(a) if a else None)
    fs += [-1] * (2 - len(fs))
    amb += [None] * (2 - len(amb))
    s = [h[:2] for h in atom.HENTI].index(hen)
    kod = [k[:3] for k in atom.KELUAR]
    if kel == 'X00':
        cari_r = (0, 0, 0)
    elif ' ATAU ' in kel or ' DAN ' in kel:
        a, o, b = kel.split(' ')
        cari_r = (kod.index(a), kod.index(b), 2 if o == 'ATAU' else 3)
    else:
        cari_r = (kod.index(kel), kod.index(kel), 1)
    r = next(i for i in range(cari.NR) if (cari.A1[i], cari.A2[i], cari.OP[i]) == cari_r)
    return {'pencetus': pc, 'fs': fs, 'amb': amb, 'lajur': s * cari.NR + r}


TAMBAHAN = ['F24']            # pindaan (g), POST-HOC: induk yang untung setiap dagangan dalam K1-K3 walaupun anaknya dipilih


def bina_kohort():
    """Peraturan pindaan (f): anak jika ditala dan mengatasi induk pada kumpulan B (gabungan DAN K3); selainnya induk;
    masuk kohort hanya jika T1 dan T2 benar. Kemudian TAMBAHAN pindaan (g)."""
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    T = pd.read_csv(os.path.join(SINI, 'hasil', 'CS04', 'papan.csv'))
    ahli, log = [], []
    for x in T.itertuples():
        anak_menang = (not x.kekal) and x.lebih_anak > x.lebih_induk and x.lebih_anak_K3 > x.lebih_induk_K3
        fid = x.anak if anak_menang else x.induk
        r = reg.loc[fid]
        lulus = r['T1'] == 'True' and r['T2'] == 'True'
        log.append(f"{x.induk}: calon {fid} ({'anak mengatasi induk' if anak_menang else 'induk'}); "
                   f"T1 {r['T1']} T2 {r['T2']} -> {'MASUK' if lulus else 'tidak'}")
        if lulus:
            ahli.append({'id': fid, 'induk': x.induk, 'takrif': r['takrif'],
                         'param': json.loads(r['param']) if r['param'] else None, 'masuk': r['masuk'],
                         'penapis': r['penapis'], 'henti': r['henti'], 'keluar': r['keluar'], **dari_takrif(r['takrif'])})
    for fid in TAMBAHAN:
        if fid not in {x['id'] for x in ahli}:
            r = reg.loc[fid]
            log.append(f'{fid}: TAMBAHAN pindaan (g), post-hoc')
            ahli.append({'id': fid, 'induk': fid, 'takrif': r['takrif'],
                         'param': json.loads(r['param']) if r['param'] else None, 'masuk': r['masuk'],
                         'penapis': r['penapis'], 'henti': r['henti'], 'keluar': r['keluar'], **dari_takrif(r['takrif'])})
    os.makedirs(KELUAR, exist_ok=True)
    json.dump({'mula': MULA, 'spec': 'kajian/SPEC_CARIAN_SETUP.md pindaan 13 Nov 2026 (f)', 'ahli': ahli, 'log': log},
              open(os.path.join(KELUAR, 'kohort.json'), 'w'), indent=1, ensure_ascii=False)
    print('\n'.join(log))
    print(f'kohort: {len(ahli)} ahli ->', os.path.join(KELUAR, 'kohort.json'))


# ---------- data ----------
def muat_stor(stor=STOR):
    d = pd.concat([pd.read_csv(os.path.join(stor, f'harga_{s}.csv')) for s in ('A', 'B')])
    ix = pd.read_csv(os.path.join(stor, 'harga_idx.csv'))

    def pecah(x):
        x = x.drop_duplicates(['ticker', 'date']).copy()
        x['date'] = pd.to_datetime(x['date'].astype(str))
        out = {}
        for t, g in x.groupby('ticker'):
            g = g.sort_values('date').set_index('date')[['open', 'high', 'low', 'close', 'volume']].astype('float64')
            g['turnover'] = g['close'] * g['volume']
            out[t] = g
        return out

    return pecah(d), pecah(ix)


def panel_stor(fr, idx):
    pan = atom.bina(fr, idx, 'hadapan')
    hu = np.unique(pan['tarikh'])
    pan['hari'] = np.searchsorted(hu, pan['tarikh'])
    pan['hari_unik'] = hu
    akhir = pan['mula'][pan['tid'] + 1]
    i = np.arange(len(pan['c']))
    pan['calon'] = pan['layak'] & (pan['tempoh'] >= 0) & (pan['atr'] > 0)          # isyarat sah (tetingkap belum tentu lengkap)
    pan['sah'] = pan['calon'] & (i + teras.TMAX < akhir)                           # tetingkap 20 sesi lengkap (untuk label)
    return pan


def isyarat_modul(fr, idx, nama, modul, P):
    cari._FR, cari._IDX, cari._TICK = fr, idx, sorted(fr)
    _, bit, ralat = cari._jalan_modul((nama, modul, P))
    if ralat:
        raise RuntimeError(f'{nama}: {ralat}')
    return np.unpackbits(bit)[:sum(len(fr[t]) for t in cari._TICK)].astype(bool)


# ---------- mekanik hadapan (tetingkap belum tentu lengkap) ----------
def simulasi(pan, i, s, r, pegang_min=None):
    """Satu isyarat bar i, henti s, peraturan keluar r. Status: TUNGGU_BELI, TERBUKA, JUAL_ESOK atau TUTUP.
    Pegang minimum (pindaan 14 Nov 2026 (p)): indikator keluar hanya dinilai mulai tutup sesi `pegang_min`, iaitu jualan
    indikator paling awal pada buka sesi pegang_min + 1 (lalai atom.PEGANG_MIN = 3: beli Isnin -> paling awal Khamis). Henti
    rugi kekal aktif sejak sesi ke-2; tiada jualan pada hari beli. Bagi tetingkap lengkap, pegang_min=1 sama dengan
    `cs_teras.hasil_satu` dan lalai sama dengan kernel `cs_keluar7` (kedua-duanya diuji)."""
    pm = atom.PEGANG_MIN if pegang_min is None else pegang_min
    o, lo, c, atr, X = pan['o'], pan['l'], pan['c'], pan['atr'], pan['X']
    akhir = int(pan['mula'][pan['tid'][i] + 1])
    e = i + 1
    if e >= akhir:
        return {'status': 'TUNGGU_BELI'}
    P = o[e]
    L = (P * 0.92, P * 0.90, P - 3.0 * atr[i], P - 4.0 * atr[i])[s]
    a1, a2, op = int(cari.A1[r]), int(cari.A2[r]), int(cari.OP[r])
    asas = {'bar_beli': e, 'harga_beli': P, 'henti': L}

    def benar(a, b, hc):
        if cari.JENIS[a] == 0:
            return X[a, b] != 0
        if cari.JENIS[a] == 1:
            return c[b] < hc - cari.PAR[a] * atr[b]
        return c[b] < cari.PAR[a] * hc

    def tutup(harga, b, sebab, sesi):
        return {**asas, 'status': 'TUTUP', 'bar_keluar': b, 'harga_keluar': harga, 'sebab': sebab, 'sesi': sesi,
                'R': harga / P - 1.0 - teras.KOS}

    hc = c[e]
    for d in range(teras.TMAX):
        b = e + d
        if b >= akhir:
            return {**asas, 'status': 'TERBUKA', 'sesi': d, 'harga_terkini': c[akhir - 1],
                    'R': c[akhir - 1] / P - 1.0 - teras.KOS}
        if d >= 1:
            if o[b] <= L:
                return tutup(o[b], b, 'henti (buka di bawah paras)', d + 1)
            if lo[b] <= L:
                return tutup(L, b, 'henti', d + 1)
        if c[b] > hc:
            hc = c[b]
        if d <= teras.TMAX - 2:
            sebab = ''
            if d == 0 and c[b] <= L:
                sebab = 'henti (tutup hari beli)'
            elif d < pm - 1:
                pass                                              # pegang minimum: indikator belum boleh menjual
            elif op == 1 and benar(a1, b, hc):
                sebab = 'keluar indikator'
            elif op == 2 and (benar(a1, b, hc) or benar(a2, b, hc)):
                sebab = 'keluar indikator'
            elif op == 3 and benar(a1, b, hc) and benar(a2, b, hc):
                sebab = 'keluar indikator'
            if sebab:
                if b + 1 < akhir:
                    return tutup(o[b + 1], b + 1, sebab, d + 1)
                return {**asas, 'status': 'JUAL_ESOK', 'sebab': sebab, 'sesi': d + 1, 'harga_terkini': c[b],
                        'R': c[b] / P - 1.0 - teras.KOS}
        else:
            return tutup(c[b], b, 'had 20 sesi', teras.TMAX)
    raise AssertionError('tidak sampai')


def jejak(stor=STOR, keluar=KELUAR):
    warnings.filterwarnings('ignore')
    K = json.load(open(os.path.join(keluar, 'kohort.json')))
    fr, idx = muat_stor(stor)
    pan = panel_stor(fr, idx)
    C = tala.ciri(pan)
    X = tk.label_asas(pan) if pan['sah'].any() else None
    modul_n = {n: m for n, m, _ in cari.senarai_benih() if n.startswith('N')}
    tarikh = pan['tarikh']
    baris = []
    for a in K['ahli']:
        pc = a['pencetus']
        if pc.startswith('P'):
            sig = pan['P'][pc]
        elif pc.startswith('N'):
            sig = isyarat_modul(fr, idx, pc, modul_n[pc], None)
        else:
            sig = isyarat_modul(fr, idx, pc, pc.split('.')[0], a['param'])
        ev = np.flatnonzero(atom.mula_isyarat(sig, pan['mula']) & pan['calon'])
        ev = ev[tala.topeng(pan, C, ev, a['fs'][0], a['amb'][0]) & tala.topeng(pan, C, ev, a['fs'][1], a['amb'][1])]
        s, r = divmod(int(a['lajur']), cari.NR)
        t_akhir, b_akhir = -1, -1
        for i in ev:
            if pan['tid'][i] == t_akhir and i <= b_akhir:              # satu posisi setiap saham
                continue
            x = simulasi(pan, int(i), s, r)
            t_akhir = pan['tid'][i]
            b_akhir = x.get('bar_keluar', 10 ** 12)                     # terbuka / menunggu: sekat isyarat seterusnya
            d = dict.fromkeys(LAJUR, '')
            d.update(id=a['id'], saham=pan['ticker'][pan['tid'][i]], tarikh_isyarat=int(tarikh[i]), status=x['status'])
            if x['status'] != 'TUNGGU_BELI':
                d.update(tarikh_beli=int(tarikh[x['bar_beli']]), harga_beli=round(float(x['harga_beli']), 4),
                         henti=round(float(x['henti']), 4), sebab=x.get('sebab', ''), sesi=x['sesi'],
                         untung_pct=round(float(x['R']) * 100, 2))
                if x['status'] == 'TUTUP':
                    d.update(tarikh_keluar=int(tarikh[x['bar_keluar']]), harga_keluar=round(float(x['harga_keluar']), 4))
                else:
                    d['harga_terkini'] = round(float(x['harga_terkini']), 4)
                if X is not None and pan['sah'][i]:
                    d.update({n: int(X[i, j]) for j, n in enumerate(tk.LABEL)})
                    d.update({'a_' + n: float(X[i, tk.NL + j]) for j, n in enumerate(tk.LABEL)})
            baris.append(d)
    L = pd.DataFrame(baris, columns=LAJUR + ['a_' + n for n in tk.LABEL])
    L[LAJUR].to_csv(os.path.join(keluar, 'lejar.csv'), index=False)
    akhir_data = int(pan['hari_unik'][-1])
    try:
        sys.path.insert(0, os.path.join(BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    pct = lambda v: '–' if v != v else f'{v:.1f}'
    A = ['# Jejak hadapan kohort F (papertrade maya; BUKAN keputusan wang sebenar)', '', status, '',
         f'Dijana `kajian/carian_setup/cs_hadapan.py`; harga hingga {akhir_data}; isyarat sejak {K["mula"]}. Pradaftar: '
         '`kajian/SPEC_CARIAN_SETUP.md` pindaan 13 Nov 2026 (f). Penjejak berasingan, bukan Lejar; tiada order. '
         '**Jangan sunting secara manual.**', '',
         '| ID | Masuk | Penapis | Henti | Keluar | Isyarat | Tunggu beli | Terbuka | Ditutup | Purata ditutup % | Menang % | '
         'Tetingkap lengkap | Lari % (rawak) | Capai +10 % dahulu % (rawak) |', '|---' * 14 + '|']
    for a in K['ahli']:
        g = L[L.id == a['id']]
        tt = g[g.status == 'TUTUP']
        lk = g[g.lari != '']
        u = pd.to_numeric(tt.untung_pct)
        kadar = lambda n: (f"{pct(pd.to_numeric(lk[n]).mean() * 100)} ({pct(pd.to_numeric(lk['a_' + n]).mean() * 100)})"
                           if len(lk) else '–')
        A.append(f"| `{a['id']}` | {a['masuk']} | {a['penapis']} | {a['henti']} | {a['keluar']} | {len(g)} | "
                 f"{int((g.status == 'TUNGGU_BELI').sum())} | {int(g.status.isin(['TERBUKA', 'JUAL_ESOK']).sum())} | {len(tt)} | "
                 f"{pct(u.mean()) if len(tt) else '–'} | {pct((u > 0).mean() * 100) if len(tt) else '–'} | {len(lk)} | "
                 f"{kadar('lari')} | {kadar('t10')} |")
    A += ['', '- "Lari" = naik ≥ 5 % minggu pertama, capai ≥ 10 % sebelum henti −8 %, masih ≥ 10 % pada minggu ke-4; hanya dikira '
          'selepas 20 sesi berlalu. "Rawak" = saham layak lain pada hari yang sama dan tahap turun-naik yang sama.',
          '- Bacaan awal tidak bermakna: perlu sekurang-kurangnya 100 belian dengan tetingkap lengkap bagi setiap setup sebelum '
          'kadar tangkap boleh dibandingkan dengan backtest (`kajian/CARIAN_SETUP.md`).',
          '- Pegang minimum (pindaan 14 Nov 2026 (p)): tiada jualan pada hari beli; indikator keluar hanya menjual mulai buka '
          'sesi ke-4; henti rugi kekal aktif sejak sesi ke-2.',
          '- Senarai penuh: `jejak_f/lejar.csv`. Alam: stor harga (senarai Shariah semasa).', '']
    open(os.path.join(keluar, 'RINGKASAN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    print(f'jejak F: {len(L)} isyarat sejak {K["mula"]}; harga hingga {akhir_data}; '
          + ', '.join(f"{k} {v}" for k, v in L.status.value_counts().items()))


if __name__ == '__main__':
    {'kohort': bina_kohort, 'jejak': jejak}[sys.argv[1]]()
