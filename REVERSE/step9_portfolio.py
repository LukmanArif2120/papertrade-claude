"""STEP 9 — penilaian portfolio 8 slot x 12.5% (KRITERIA AKHIR kajian).

Bagi setiap sistem: signal ENTRY (status CALON selepas Step 8) + peraturan HOLD + signal EXIT.
Pemilihan apabila calon melebihi slot (DIBEKUKAN, SPEC §12): lift_presisi menurun, kemudian
rs_spy_6b menurun, kemudian ticker (abjad).

Guna: python3 REVERSE/step9_portfolio.py 2025
Output: REVERSE/portfolio_<TAHUN>.csv, REVERSE/portfolio_bulanan_<TAHUN>.csv
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, keluar as K, signal as S, stat as T  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402
from REVERSE.step7b_hadapan import _pra_siri, TRAIL, PRA  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
SLOT = 8
BAHAGIAN = 0.125
UFUK = 252


def exit_hari(pra, asas, lv, c, o, i, exit_nama, hold, n):
    """Hari exit (indeks bar) bagi satu kemasukan di i (masuk buka i+1). None = pegang hingga had."""
    i0 = i + 1
    b = min(i + UFUK, n - 1)
    W = b - i0 + 1
    if W < 2:
        return None, None
    cw = c[i0:b + 1]
    puncak = np.maximum.accumulate(np.where(np.isfinite(cw), cw, -np.inf))
    ipk = np.maximum.accumulate(np.where(cw >= puncak, np.arange(W), 0))
    if exit_nama == 'REF_pegang_252':
        return b, 'had_252'
    if exit_nama == 'REF_jual_hari63':
        return min(i + 63, n - 1), 'hari63'
    nm = 'chandelier_4atr' if exit_nama == 'REF_chandelier_4atr' else exit_nama
    if nm in PRA:
        fire = pra[nm][i0:b + 1]
    else:
        jen, p = TRAIL[nm]
        atr_pk = lv['atr'][i0:b + 1][ipk]
        fire = (cw <= puncak - p * atr_pk) if jen == 'atr' else (cw <= puncak * p)
    if hold is not None:
        x, y = hold
        dd = (cw / np.where(puncak > 0, puncak, np.nan) - 1.0) * 100.0
        veto = (dd >= -float(x)) & (cw >= lv[y][i0:b + 1]) & asas[i0:b + 1]
        fire = fire & ~veto
    if fire.any():
        j = int(np.argmax(fire))
        return min(i0 + j + 1, n - 1), nm
    return b, 'had_252'


def jalankan(nama, entri, fr, pra_all, c_all, o_all, to_all, kal, exit_nama, hold, pilihan,
             saiz=None):
    """Simulasi portfolio 8 slot. entri: DataFrame ticker, tarikh, skor1, skor2.

    saiz: None = bahagian tetap BAHAGIAN (12.5%), tingkah laku asal fasa 1 tidak berubah.
    Jika diberi, saiz(ticker, i) -> pecahan ekuiti bagi posisi itu (SPEC_FASA2 §5.4 menuntut dua
    saiz: tetap dan berskala risiko SPEC_1B). Had slot, susunan pilihan dan kos tidak berubah.
    """
    ekuiti = 1.0
    posisi = []            # dict(ticker, i_keluar, unit, kos_jual, tarikh_keluar)
    tunai = 1.0
    siri, dagangan = [], []
    slot_hari, n_masuk = [], 0
    peta_entri = {}
    for t, d in zip(entri.ticker, entri.tarikh):
        peta_entri.setdefault(d, []).append(t)
    for hari in kal:
        # 1) tutup posisi yang keluar hari ini (pada buka)
        baki = []
        for p in posisi:
            if p['tarikh_keluar'] == hari:
                g = fr[p['ticker']]
                k = g.index.get_loc(hari)
                harga = o_all[p['ticker']][k] if p['sebab'] != 'had_252' else c_all[p['ticker']][k]
                if not np.isfinite(harga) or harga <= 0:
                    harga = c_all[p['ticker']][k]
                tunai += p['unit'] * harga * (1 - p['ks'])
                dagangan.append(dict(sistem=nama, ticker=p['ticker'], masuk=p['tarikh_masuk'],
                                     keluar=hari, hari=p['hari'], sebab=p['sebab'],
                                     pulangan=round(float(p['unit'] * harga * (1 - p['ks'])
                                                          / p['nilai'] - 1) * 100, 2)))
            else:
                baki.append(p)
        posisi = baki
        # 2) nilai ekuiti pada tutup
        nilai = tunai
        for p in posisi:
            g = fr[p['ticker']]
            k = g.index.get_loc(hari) if hari in g.index else None
            if k is not None and np.isfinite(c_all[p['ticker']][k]):
                p['harga_akhir'] = c_all[p['ticker']][k]
            # hari tanpa bar (saham digantung / bar dibuang QC): guna tutup sah TERAKHIR,
            # bukan harga hari keluar — supaya siri ekuiti tidak memandang ke hadapan.
            nilai += p['unit'] * p['harga_akhir']
        ekuiti = nilai
        siri.append((hari, ekuiti))
        slot_hari.append(len(posisi))
        # 3) kemasukan: signal semalam -> masuk buka hari ini
        semalam = kal[kal.get_loc(hari) - 1] if kal.get_loc(hari) > 0 else None
        if semalam is None or semalam not in peta_entri:
            continue
        calon = [t for t in peta_entri[semalam] if t in fr and hari in fr[t].index
                 and not any(p['ticker'] == t for p in posisi)]
        if not calon:
            continue
        calon.sort(key=lambda t: pilihan.get((t, semalam), (0.0, 0.0, t)), reverse=True)
        for t in calon:
            if len(posisi) >= SLOT:
                break
            g = fr[t]
            i = g.index.get_loc(semalam)
            k = i + 1
            if k >= len(g):
                continue
            ks = kos_sisi(to_all[t][i])
            harga = o_all[t][k] * (1 + ks)
            if not np.isfinite(harga) or harga <= 0:
                continue
            bhg = BAHAGIAN if saiz is None else saiz(t, i)
            if not (np.isfinite(bhg) and bhg > 0):
                continue
            nilai_pos = ekuiti * bhg
            if nilai_pos > tunai:
                nilai_pos = tunai
            if nilai_pos <= 0:
                continue
            unit = nilai_pos / harga
            tunai -= nilai_pos
            pra, asas, lv = pra_all[t]
            ik, sebab = exit_hari(pra, asas, lv, c_all[t], o_all[t], i, exit_nama, hold, len(g))
            if ik is None:
                tunai += nilai_pos
                continue
            n_masuk += 1
            posisi.append(dict(ticker=t, unit=unit, ks=ks, nilai=nilai_pos,
                               tarikh_masuk=hari, tarikh_keluar=g.index[ik],
                               hari=int(ik - k + 1), sebab=sebab,
                               harga_akhir=harga / (1 + ks)))
    info = dict(n_masuk=n_masuk, n_tutup=len(dagangan), n_terbuka_akhir=len(posisi),
                purata_slot_terisi=round(float(np.mean(slot_hari)), 2) if slot_hari else 0.0)
    return pd.DataFrame(siri, columns=['tarikh', 'ekuiti']), pd.DataFrame(dagangan), info


def ringkas(nama, siri, dag, spy, info):
    s = siri.set_index('tarikh')['ekuiti']
    bulanan = s.resample('ME').last() / s.resample('ME').last().shift(1) - 1
    bulanan.iloc[0] = s.resample('ME').last().iloc[0] / 1.0 - 1
    b = bulanan.dropna() * 100
    sp = spy.resample('ME').last().pct_change()
    sp.iloc[0] = spy.resample('ME').last().iloc[0] / spy.iloc[0] - 1
    return dict(sistem=nama, n_posisi_dibuka=info['n_masuk'],
                n_dagangan_ditutup=info['n_tutup'],
                n_posisi_terbuka_hujung_tahun=info['n_terbuka_akhir'],
                purata_slot_terisi=info['purata_slot_terisi'],
                pulangan_tahun=round(float(s.iloc[-1] - 1) * 100, 2),
                median_bulanan=round(float(b.median()), 2),
                purata_bulanan=round(float(b.mean()), 2),
                pct_bulan_ge10=round(float((b >= 10).mean() * 100), 1),
                pct_bulan_positif=round(float((b > 0).mean() * 100), 1),
                bulan_terbaik=round(float(b.max()), 2), bulan_terburuk=round(float(b.min()), 2),
                mdd=round(T.mdd(s.to_numpy()), 2),
                purata_hari_pegang=round(float(dag.hari.mean()), 1) if len(dag) else '',
                pusing_ganti_bulanan=round(info['n_masuk'] / 12.0, 1),
                spy_pulangan_tahun=round(float(spy.iloc[-1] / spy.iloc[0] - 1) * 100, 2),
                spy_mdd=round(T.mdd(spy.to_numpy()), 2)), b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a_ = ap.parse_args()
    th = a_.tahun
    t0 = time.time()
    kp = pd.read_csv(KELUAR / f'keputusan_{th}.csv')
    calon = kp[kp.keputusan == 'CALON'].signal.tolist()
    fs = pd.read_csv(KELUAR / f'false_signal_{th}.csv')
    cu = pd.read_csv(KELUAR / f'common_unique_{th}.csv')
    lp = cu[(cu.subset == 'S2') & (cu.populasi == 'a') & (cu.kumpulan_data == 'A')
            & (cu.keluarga == 'PADU')].set_index('signal').lift_presisi.to_dict()
    hh = pd.read_csv(KELUAR / f'hadapan_hold_exit_{th}.csv')
    l7b = json.loads((CACHE / f'lulus7b_{th}.json').read_text())
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    sig = sig[sig.dalam_univ == 1].reset_index(drop=True)
    asas = 'CALON selepas Step 8'
    if not calon:
        # SPEC pindaan §13.10: jika TIADA signal CALON, Step 9 tetap dijalankan atas signal yang
        # lulus Step 7 supaya kriteria akhir ada angka — dilabel jelas, BUKAN sistem yang lulus.
        calon = json.loads((CACHE / f'lulus7_{th}.json').read_text())['signal']
        asas = 'lulus Step 7 sahaja (TIADA signal CALON tahun ini)'
        print(f'TIADA signal ENTRY berstatus CALON — sandaran: {len(calon)} signal lulus Step 7.')
    if not calon:
        print('Tiada signal lulus Step 7 juga — Step 9 tidak boleh dijalankan.')
        return
    sg = S.bina(sig, kuin)
    mana = np.zeros(len(sig), dtype=bool)
    skor = {}
    for nm in calon:
        a = sg[nm]
        mana |= a
        for t, d, rs in zip(sig.ticker[a], sig.tarikh[a], sig.rs_spy_6b[a]):
            v = (float(lp.get(nm, 0) or 0), float(rs) if np.isfinite(rs) else -999.0, t)
            if skor.get((t, d), (-1, -1, '')) < v:
                skor[(t, d)] = v
    entri = sig.loc[mana, ['ticker', 'tarikh']].drop_duplicates().reset_index(drop=True)
    print(f'signal ENTRY ({asas}): {len(calon)} | kemunculan entri unik {len(entri)}')
    tick = sorted(entri.ticker.unique())
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{th - 2}-06-01', '2026-10-16')
    spy_c = ix['SPY']['close']
    spy_n = ((spy_c > spy_c.rolling(50, min_periods=50).mean())
             & (spy_c > spy_c.rolling(200, min_periods=200).mean()))
    pra_all, c_all, o_all, to_all = {}, {}, {}, {}
    for t, g in fr.items():
        sn = spy_n.reindex(g.index).fillna(False).to_numpy()
        pra_all[t] = _pra_siri(g, sn)
        c_all[t] = g['close'].to_numpy('float64')
        o_all[t] = g['open'].to_numpy('float64')
        to_all[t] = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy()
    kal = spy_c.index[(spy_c.index >= pd.Timestamp(f'{th}-01-01'))
                      & (spy_c.index <= pd.Timestamp(f'{th}-12-31'))]
    spy_th = spy_c.reindex(kal).ffill()
    print(f'[{time.time()-t0:.0f}s] data sedia | hari dagangan {len(kal)}')

    # sistem yang diuji: 3 rujukan + 3 terbaik 7b + kawalan rawak
    hh2 = hh[~hh.sistem.str.startswith('REF_')].copy()
    hh2['j'] = pd.to_numeric(hh2.jangkaan, errors='coerce')
    atas = hh2.sort_values('j', ascending=False).sistem.head(3).tolist()
    ujian = [('REF_pegang_252', 'REF_pegang_252', None),
             ('REF_chandelier_4atr', 'REF_chandelier_4atr', None),
             ('REF_jual_hari63', 'REF_jual_hari63', None)]
    for nm in atas:
        e, hp = nm.split('|')
        x = int(hp.split('X=')[1].split('%')[0])
        y = hp.split('Y=')[1]
        ujian.append((nm, e, (x, y)))
    rows, bulanan = [], {}
    for nama, e, hold in ujian:
        siri, dag, info = jalankan(nama, entri, fr, pra_all, c_all, o_all, to_all, kal, e,
                                   hold, skor)
        r, b = ringkas(nama, siri, dag, spy_th, info)
        rows.append(r)
        bulanan[nama] = b
        dag.to_csv(CACHE / f'dagangan9_{nama.replace("|", "_").replace("%","")}_{th}.csv',
                   index=False)
        print(f"  {nama:34s} pulangan {r['pulangan_tahun']:7.2f}% median bulanan "
              f"{r['median_bulanan']:6.2f}% bulan>=10% {r['pct_bulan_ge10']:5.1f}% "
              f"MDD {r['mdd']:7.2f}% buka {r['n_posisi_dibuka']:3d} tutup "
              f"{r['n_dagangan_ditutup']:3d} slot {r['purata_slot_terisi']:.1f}")
    # KAWALAN RAWAK: entri rawak, saiz sama, benih 42
    rawak = pd.read_parquet(CACHE / f'rawak_{th}.parquet')[['ticker', 'tarikh']]
    rawak = rawak[rawak.ticker.isin(fr)].drop_duplicates()
    sk_r = {(t, d): (0.0, 0.0, t) for t, d in zip(rawak.ticker, rawak.tarikh)}
    for nama, e, hold in (('KAWALAN_RAWAK|pegang_252', 'REF_pegang_252', None),
                          ('KAWALAN_RAWAK|chandelier', 'REF_chandelier_4atr', None)):
        siri, dag, info = jalankan(nama, rawak, fr, pra_all, c_all, o_all, to_all, kal, e,
                                   hold, sk_r)
        r, b = ringkas(nama, siri, dag, spy_th, info)
        rows.append(r)
        bulanan[nama] = b
        print(f"  {nama:34s} pulangan {r['pulangan_tahun']:7.2f}% median bulanan "
              f"{r['median_bulanan']:6.2f}% buka {r['n_posisi_dibuka']:3d} tutup "
              f"{r['n_dagangan_ditutup']:3d} slot {r['purata_slot_terisi']:.1f}")
    out = pd.DataFrame(rows)
    out['asas_entry'] = asas
    out['had_fasa'] = 'CALON sahaja (SPEC §11.8)'
    out['kaveat'] = 'tiada saham delist (survivorship); satu tahun satu rejim pasaran'
    out.to_csv(KELUAR / f'portfolio_{th}.csv', index=False)
    pd.DataFrame(bulanan).round(2).to_csv(KELUAR / f'portfolio_bulanan_{th}.csv')
    print(f'\nSASARAN PENGGUNA +10% SEBULAN (median):')
    for _, r in out.iterrows():
        kata = 'TERCAPAI' if r.median_bulanan >= 10 else 'TIDAK TERCAPAI'
        print(f"  {r.sistem:34s} median bulanan {r.median_bulanan:6.2f}% -> {kata}")
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()
