"""Carian setup — pusingan CS07: pendaftaran setup lengkap (masuk (a) + henti/keluar (b)) sebagai keluarga F (F88 dan
seterusnya), dan penghurai takrif CS07 untuk kedudukan akhir (SPEC pindaan 14 Nov 2026 (n), "Pendaftaran").

Takrif CS07: 'pencetus|penapis|henti|keluar|prasyarat', cth. 'K01.012|F11+F20|G7|Y09.1 ATAU Y09.4@10|QA08+QF01'.
Henti G1-G8 = cs_keluar7.HENTI; keluar = cs_keluar7.kod_peraturan (akhiran @5/@10 = aktif selepas untung sebanyak itu).
Guna: python3 cs_cs07.py daftar <kerja>. Takrif yang sudah berdaftar mengekalkan ID; baris lain tidak disentuh."""
import json
import os
import pickle
import sys

import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_lapor as lapor  # noqa: E402
import cs_tala7 as t7  # noqa: E402

PUS = 'CS07'
HENTI_KOD = [f'G{i}' for i in range(1, k7.NH + 1)]
_KOL = {}


def _kol(kod):
    """Songsang kod_peraturan: 'Y09.1 ATAU Y09.4@10' -> lajur."""
    if not _KOL:
        _KOL.update({k7.kod_peraturan(r * k7.NG): r for r in range(k7.NR)})
    asas, _, akt = kod.partition('@')
    return _KOL[asas] * k7.NG + ({'': 0, '5': 1, '10': 2}[akt])


def takrif7(pencetus, q1, q2, f1, f2, s, kol):
    pen = '+'.join(atom.PENAPIS[f][:3] for f in (f1, f2) if f >= 0)
    return f'{pencetus}|{pen}|{HENTI_KOD[s]}|{k7.kod_peraturan(kol)}|{c5.tk_pra(q1, q2, kod=True)}'


def dari_takrif7(tk):
    b = tk.split('|')
    fs = [[x[:3] for x in atom.PENAPIS].index(k) for k in b[1].split('+') if k] + [-1, -1]
    q1 = q2 = -1
    for kod in (b[4].split('+') if b[4] else []):
        if kod in [x[:4] for x in lapis.PASARAN]:
            q1 = [x[:4] for x in lapis.PASARAN].index(kod)
        else:
            q2 = [x[:4] for x in lapis.KUMPULAN].index(kod)
    return {'pencetus': b[0], 'f1': fs[0], 'f2': fs[1], 'q1': q1, 'q2': q2, 's': HENTI_KOD.index(b[2]), 'kol': _kol(b[3])}


def dipercayai(kerja, papan, S0):
    """Takrif "dipercayai" pindaan (m) bagi setiap setup papan CS07 dengan henti dan keluar terpilihnya (kumpulan B, satu
    posisi setiap saham): belian >= 300, >= 10 tahun aktif, kelebihan `terus` > 0 dalam K1, K2 dan K3. Sama seperti cs_akhir."""
    import numpy as np

    import cs_akhir as ak
    import cs_cari as cari
    import cs_lengkap as lg
    import cs_teras as teras
    pan, Tb = cari.panel(kerja, 'B'), lg.muat_asas(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr, XA = (L['L1'], L['L2']), k7.siri_set(kerja, 'B')
    sah, g, ng = np.flatnonzero(pan['sah']), Tb['g'], np.maximum(Tb['n'], 1)
    Lb = ak.label2(sah, pan['o'], pan['l'], pan['c'])[:, 1]
    lebih = np.zeros(len(pan['c']))
    lebih[sah] = Lb - (np.bincount(g[sah], Lb, minlength=len(ng)) / ng)[g[sah]]
    out = {}
    for b in papan:
        if b['id'] not in S0:
            continue
        s, kol = S0[b['id']]['pilih']
        ev = t7.ev_satu(kerja, 'B', b['pencetus'])
        e0 = ev[c5.topeng(pan, Lr, ev, b['q1'], b['q2'], b['f1'], b['f2'])]
        St = k7.sedia_pan(pan, XA, e0)
        _, sk = k7.hasil(*St[:7], k7.A1, k7.A2, k7.OP, s, kol)
        e = e0[teras.satu_posisi(e0, sk, pan['tid'])]
        tp = pan['tempoh'][e]
        kl = [float(lebih[e[tp == j]].mean()) if (tp == j).any() else float('nan') for j in range(3)]
        tahun = int(len(np.unique(pan['tarikh'][e] // 10000)))
        out[b['id']] = dict(belian=len(e), tahun=tahun, kl=kl, ya=bool(
            len(e) >= ak.MIN_BELIAN and tahun >= ak.MIN_TAHUN and all(x > 0 for x in kl)))
    return out


def daftar(kerja):
    """Daftar setup papan CS07 yang DIPERCAYAI (penjelasan (n)-2) ke data/registry_F.csv. Pulangkan {id papan: id F}."""
    papan = pickle.load(open(os.path.join(kerja, 'cs07_papan.pkl'), 'rb'))
    S0 = pickle.load(open(os.path.join(kerja, 'cs07_keluar_pilih.pkl'), 'rb'))['setup']
    K = pickle.load(open(os.path.join(kerja, 'cs07_keluar_kunci.pkl'), 'rb'))
    lulus = dipercayai(kerja, papan, S0)
    pickle.dump(lulus, open(os.path.join(kerja, 'cs07_dipercayai.pkl'), 'wb'))
    papan = [b for b in papan if lulus.get(b['id'], {}).get('ya')]
    param = t7.param_semua(kerja)
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').reindex(columns=lapor.LAJUR_F, fill_value='')
    idf = {}
    for b in papan:
        if b['id'] not in S0 or b['id'] not in K:
            continue
        s, kol = S0[b['id']]['pilih']
        tk = takrif7(b['pencetus'], b['q1'], b['q2'], b['f1'], b['f2'], s, kol)
        lama = reg[reg.takrif == tk]
        if len(lama):
            idf[b['id']] = lama.id.iloc[0]
            continue
        fid = f"F{max(int(x[1:]) for x in reg.id) + 1:02d}"
        P = param.get(b['pencetus']) if b['pencetus'][0] == 'M' else t7.nama7(b['pencetus'], param) and dict(
            t7._GRID[b['pencetus']][1])
        m = K[b['id']]['pilih']
        baru = dict.fromkeys(lapor.LAJUR_F, '')
        baru.update(id=fid, keluarga='F', pusingan=PUS, tarikh_daftar=pd.Timestamp.now().strftime('%Y-%m-%d'), takrif=tk,
                    param=json.dumps({a: (round(x, 6) if isinstance(x, float) else x) for a, x in P.items()}, sort_keys=True)
                    if P else '', masuk=t7.nama7(b['pencetus'], param), penapis=c5.tk_pen(b['f1'], b['f2']),
                    henti=f'{HENTI_KOD[s]} {k7.HENTI[s]}', keluar=k7.nama_peraturan(kol), skor_tepat=f"{b['skor']:.5f}",
                    status='BACKTEST', prasyarat=c5.buang_kod(c5.tk_pra(b['q1'], b['q2'])).replace(' DAN ', ' + '),
                    syarat=c5.buang_kod(c5.tk_pen(b['f1'], b['f2'])).replace(' DAN ', ' + '))
        for j, t in enumerate(('K1', 'K2', 'K3')):
            v = m[('satu', j)]
            baru[f'n_{t}'] = str(v['n'])
            if v['n']:
                baru.update({f'purata_{t}': f"{v['purata']:.5f}", f'k10_{t}': f"{v['jadi']:.4f}",
                             f'menang_{t}': f"{v['menang']:.4f}"})
        baru['menang'] = f"{m[('satu', -1)]['menang']:.4f}"
        reg = pd.concat([reg, pd.DataFrame([baru])[lapor.LAJUR_F].astype(str)], ignore_index=True)
        idf[b['id']] = fid
    reg['_n'] = reg.id.str[1:].astype(int)
    reg.sort_values('_n').drop(columns='_n').to_csv(lapor.REG_F, index=False)
    pickle.dump(idf, open(os.path.join(kerja, 'cs07_idf.pkl'), 'wb'))
    return idf


if __name__ == '__main__':
    if sys.argv[1] == 'daftar':
        print(daftar(sys.argv[2]))
    else:
        raise SystemExit(f'arahan tidak dikenali: {sys.argv[1]}')
