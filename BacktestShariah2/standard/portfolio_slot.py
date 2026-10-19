"""Jejak hadapan portfolio maya 10 slot (sejak 19 Okt 2026; kajian kajian/KAJIAN_PORTFOLIO.md). Rekod sahaja: tiada order,
tiada wang sebenar. Dibina semula sepenuhnya daripada Lejar Penuh pada setiap larian (deterministik, tanpa LLM):
  RS_10    — setiap sesi beli, slot kosong diisi dengan posisi lejar baharu yang RS pasarannya (data/rs/rs_pasaran.csv pada
             tarikh isyarat) tertinggi; RS tiada -> paling akhir.
  RAWAK_10 — kawalan: susunan rawak tetap (benih = tarikh beli), supaya kelebihan RS boleh diukur ke hadapan.
Peraturan sama dengan kajian: 10 slot; saiz = min(tunai, ekuiti semalam x 10%); satu posisi bagi setiap saham; keluar =
lorong 2 lejar (Chandelier tutup 4xATR14, jual pada buka esok; lajur *_henti), direalisasi sebelum belian hari sama;
nilai pasaran = saiz x tutup / harga beli; kos 0.1% setiap belah (seperti enjin). Calon = posisi yang lejar beli (isyarat
100% semua kaedah, seluruh alam Shariah >= USD10; tiada bias kemandirian set 431).
  python3 BacktestShariah2/standard/portfolio_slot.py   -> BacktestShariah2/portfolio_slot/ (dijalankan oleh lejar.yml)
"""
import os, sys, json

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(BS2, 'kod')); sys.path.insert(0, HERE)
from stor import muat, frames_dict  # noqa: E402

LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
STOR = os.environ.get('LEJAR_STOR', os.path.join(BS2, 'data', 'harga', 'stor'))
RS = os.path.join(BS2, 'data', 'rs', 'rs_pasaran.csv')
KELUAR = os.environ.get('PORTFOLIO_SLOT_DIR', os.path.join(BS2, 'portfolio_slot'))
SLOT, W, KOS = 10, 0.10, 0.001
PORTFOLIO = {'RS_10': 'RS pasaran tertinggi', 'RAWAK_10': 'Rawak (kawalan)'}
L_POSISI = ['saham', 'id_kaedah', 'tarikh_isyarat', 'rs', 'tarikh_beli', 'harga_beli', 'saiz_pct', 'status', 'tarikh_keluar',
            'harga_keluar', 'untung_pct', 'harga_terkini', 'untung_semasa_pct']
L_EKUITI = ['tarikh', 'ekuiti', 'tunai', 'bil_posisi', 'spy']


def calon_lejar():
    """Semua posisi lejar yang dibeli (terbuka + tutup) dengan lorong 2 dan RS pada tarikh isyarat."""
    import lejar
    T, O = lejar.semua_posisi()
    P = pd.concat([T, O], ignore_index=True)
    P = P[(P.tarikh_beli != '') & (P.harga_beli != '')].copy()
    P['harga_beli'] = P.harga_beli.astype(float)
    P['keluar'] = P.keluar_henti.astype(str).str.lower().eq('true') & P.tarikh_keluar_henti.ne('')
    P['harga_keluar_henti'] = pd.to_numeric(P.harga_keluar_henti, errors='coerce')
    if os.path.exists(RS):
        r = pd.read_csv(RS, usecols=['tarikh', 'ticker', 'rs']).rename(columns={'tarikh': 'tarikh_isyarat', 'ticker': 'saham'})
        P = P.merge(r.drop_duplicates(['tarikh_isyarat', 'saham']), on=['tarikh_isyarat', 'saham'], how='left')
    else:
        P['rs'] = np.nan
    return P.sort_values(['tarikh_beli', 'saham', 'id_kaedah']).reset_index(drop=True)


def susun(G, jenis, tarikh):
    """Susunan calon satu sesi beli. G diisih saham, id_kaedah (tetap)."""
    if jenis == 'RS_10':
        return G.assign(_k=G.rs.fillna(-1.0)).sort_values('_k', ascending=False, kind='stable')
    rng = np.random.default_rng(int(tarikh.replace('-', '')))
    return G.iloc[rng.permutation(len(G))]


def bina(P, jenis, hari, tutup):
    """hari: senarai tarikh 'YYYY-MM-DD' (sesi dagangan); tutup(saham, tarikh) -> harga tutup atau None.
    Pulang (posisi DataFrame, ekuiti DataFrame)."""
    tunai = eq = 1.0; pos = {}; rekod = []; kurva = []
    ikut_beli = {d: g for d, g in P.groupby('tarikh_beli')}
    for d in hari:
        for s in [s for s, p in pos.items() if p['keluar'] and p['tarikh_keluar_henti'] <= d]:
            p = pos.pop(s); hk = p['harga_keluar_henti']
            tunai += p['amaun'] * hk / p['harga_beli'] * (1 - KOS) / (1 + KOS)
            rekod.append(dict(p, status='Keluar', tarikh_keluar=p['tarikh_keluar_henti'], harga_keluar=hk,
                              untung_pct=100 * (hk / p['harga_beli'] * (1 - KOS) / (1 + KOS) - 1)))
        if d in ikut_beli:
            for r in susun(ikut_beli[d], jenis, d).to_dict('records'):
                if len(pos) >= SLOT: break
                if r['saham'] in pos: continue
                am = min(tunai, eq * W)
                if am <= 1e-12: break
                tunai -= am; pos[r['saham']] = dict(r, amaun=am, saiz_pct=100 * am / eq)
        mv = 0.0
        for s, p in pos.items():
            c = tutup(s, d)
            mv += p['amaun'] * (c / p['harga_beli'] if c else 1.0)
        eq = tunai + mv; kurva.append(dict(tarikh=d, ekuiti=eq, tunai=tunai, bil_posisi=len(pos)))
    akhir = hari[-1] if hari else ''
    for s, p in pos.items():
        c = tutup(s, akhir)
        rekod.append(dict(p, status='Pegang', harga_terkini=c,
                          untung_semasa_pct=100 * (c / p['harga_beli'] - 1) if c else np.nan))
    R = pd.DataFrame(rekod).reindex(columns=L_POSISI)
    return R.sort_values(['tarikh_beli', 'saham']).reset_index(drop=True), pd.DataFrame(kurva, columns=L_EKUITI[:-1])


def mdd(x):
    x = pd.Series(np.r_[1.0, np.asarray(x, float)]); return float((x / x.cummax() - 1).min())   # ekuiti mula = 1 (buka hari pertama)


def ringkasan(hasil, spy_mula, spy_akhir, hari):
    L = [f'# Portfolio maya 10 slot (jejak hadapan; rekod sahaja)', '',
         'Dibina semula daripada Lejar Penuh oleh `standard/portfolio_slot.py`; kajian `kajian/KAJIAN_PORTFOLIO.md`. '
         'Tiada order, tiada wang sebenar. Jangan ubah secara manual.', '',
         f'Tempoh: {hari[0] if hari else "-"} hingga {hari[-1] if hari else "-"} ({len(hari)} sesi). '
         f'SPY dalam tempoh sama: {100 * (spy_akhir / spy_mula - 1):+.2f}%.' if spy_mula else 'SPY: tiada data.', '',
         '| Portfolio | Pulangan % | MDD % | Posisi dipegang | Dagangan keluar | Kadar menang % | Purata untung keluar % |',
         '|---|---|---|---|---|---|---|']
    for k, (R, E) in hasil.items():
        k_ = R[R.status == 'Keluar']; ret = 100 * (E.ekuiti.iloc[-1] - 1) if len(E) else 0.0
        L.append(f'| {k} — {PORTFOLIO[k]} | {ret:+.2f} | {100 * mdd(E.ekuiti):.2f} | {(R.status == "Pegang").sum()} | {len(k_)} | '
                 + (f'{100 * (k_.untung_pct > 0).mean():.0f} | {k_.untung_pct.mean():+.2f} |' if len(k_) else '– | – |'))
    for k, (R, _) in hasil.items():
        H = R[R.status == 'Pegang']
        L += ['', f'## {k} — posisi dipegang', '', '| Saham | Kaedah | RS | Beli | Harga beli | Terkini | Untung % |', '|---|---|---|---|---|---|---|']
        L += [f'| {r.saham} | {r.id_kaedah} | {"" if pd.isna(r.rs) else int(r.rs)} | {r.tarikh_beli} | {r.harga_beli:.2f} | '
              f'{"" if pd.isna(r.harga_terkini) else f"{r.harga_terkini:.2f}"} | {"" if pd.isna(r.untung_semasa_pct) else f"{r.untung_semasa_pct:+.2f}"} |'
              for r in H.itertuples()]
    L += ['', 'Penilaian adil memerlukan sekurang-kurangnya 6–12 bulan (KAJIAN_PORTFOLIO.md). Kelebihan yang dicari: RS_10 mengatasi '
          'RAWAK_10 dan SPY dengan MDD yang setanding.']
    return '\n'.join(L) + '\n'


def main():
    P = calon_lejar()
    fr, idx = frames_dict(muat(STOR))
    if 'SPY' not in idx or P.empty:
        print('tiada calon lejar atau SPY: portfolio tidak dibina'); return 0
    spy = idx['SPY'].close
    hari = [d.strftime('%Y-%m-%d') for d in spy.index if d.strftime('%Y-%m-%d') >= P.tarikh_beli.min()]
    cl = {t: g.close for t, g in fr.items()}

    def tutup(s, d):
        c = cl.get(s)
        if c is None: return None
        v = c.asof(pd.Timestamp(d)); return float(v) if pd.notna(v) and v > 0 else None

    os.makedirs(KELUAR, exist_ok=True); hasil = {}
    s0 = float(idx['SPY'].open.asof(pd.Timestamp(hari[0]))) if hari else None   # belian pertama pada buka
    for k in PORTFOLIO:
        R, E = bina(P, k, hari, tutup)
        E['spy'] = [float(spy.asof(pd.Timestamp(d))) / s0 for d in E.tarikh] if s0 else np.nan
        R.to_csv(os.path.join(KELUAR, f'{k}_posisi.csv'), index=False, float_format='%.4f')
        E.to_csv(os.path.join(KELUAR, f'{k}_ekuiti.csv'), index=False, float_format='%.6f')
        hasil[k] = (R, E)
    s1 = float(spy.asof(pd.Timestamp(hari[-1]))) if hari else None
    open(os.path.join(KELUAR, 'RINGKASAN.md'), 'w').write(ringkasan(hasil, s0, s1, hari))
    json.dump({k: dict(sesi_terakhir=hari[-1] if hari else None, ekuiti=round(float(E.ekuiti.iloc[-1]), 6) if len(E) else 1.0,
                       dipegang=int((R.status == 'Pegang').sum()), keluar=int((R.status == 'Keluar').sum()))
               for k, (R, E) in hasil.items()}, open(os.path.join(KELUAR, 'status.json'), 'w'), indent=1)
    for k, (R, E) in hasil.items():
        print(k, 'ekuiti %.4f' % E.ekuiti.iloc[-1], 'dipegang', (R.status == 'Pegang').sum(), 'keluar', (R.status == 'Keluar').sum())
    return 0


if __name__ == '__main__':
    sys.exit(main())
