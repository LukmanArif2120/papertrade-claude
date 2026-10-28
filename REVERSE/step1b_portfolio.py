"""FASA 1B — saiz posisi dan henti berskala kemeruapan (SPEC_1B.md).

Perubahan tunggal berbanding fasa 1: nilai_posisi = (RISIKO x ekuiti) / (k x ATR%), bukan 12.5%
tetap. Semua yang lain sama. Grid 3 RISIKO x 3 k x 2 varian = 18 ujian setiap tahun, ditambah
tiga rujukan fasa 1 dengan saiz baharu dan KAWALAN RAWAK bersaiz sama.

Guna: python3 REVERSE/step1b_portfolio.py <TAHUN>
Output: REVERSE/portfolio_1b_<TAHUN>.csv
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
from REVERSE.teras import data as D, signal as S, stat as T  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402
from REVERSE.step7b_hadapan import _pra_siri, TRAIL, PRA  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
UFUK = 252
RISIKO = [0.005, 0.010, 0.015]
KVAL = [2, 3, 4]
VARIAN = {'V1_maks8': 8, 'V2_tiada_had': 10 ** 6}
HAD_ATAS, HAD_BAWAH = 0.25, 0.02


def exit_hari(pra, asas, lv, c, o, i, exit_nama, n, k_atr):
    """Hari exit. exit_nama: 'trail_k' (gandaan k_atr), atau rujukan fasa 1."""
    i0, b = i + 1, min(i + UFUK, n - 1)
    W = b - i0 + 1
    if W < 2:
        return None, None
    if exit_nama == 'REF_pegang_252':
        return b, 'had_252'
    if exit_nama == 'REF_jual_hari63':
        return min(i + 63, n - 1), 'hari63'
    cw = c[i0:b + 1]
    puncak = np.maximum.accumulate(np.where(np.isfinite(cw), cw, -np.inf))
    ipk = np.maximum.accumulate(np.where(cw >= puncak, np.arange(W), 0))
    atr_pk = lv['atr'][i0:b + 1][ipk]
    p = 4.0 if exit_nama == 'REF_chandelier_4atr' else float(k_atr)
    fire = cw <= puncak - p * atr_pk
    if fire.any():
        return min(i0 + int(np.argmax(fire)) + 1, n - 1), f'trail_{p:.0f}atr'
    return b, 'had_252'


def jalankan(entri, fr, pra_all, c_all, o_all, to_all, atrp_all, kal, exit_nama, risiko, k,
             maks_posisi, pilihan):
    """Simulasi portfolio bersaiz risiko. Pulangkan (siri ekuiti, dagangan, info)."""
    tunai, ekuiti = 1.0, 1.0
    posisi, siri, dagangan = [], [], []
    n_masuk, n_langkau, slot_hari, saiz = 0, 0, [], []
    peta = {}
    for t, dd in zip(entri.ticker, entri.tarikh):
        peta.setdefault(dd, []).append(t)
    for hari in kal:
        baki = []
        for p in posisi:
            if p['tarikh_keluar'] == hari:
                g = fr[p['ticker']]
                kk = g.index.get_loc(hari)
                harga = (o_all[p['ticker']][kk] if p['sebab'] != 'had_252'
                         else c_all[p['ticker']][kk])
                if not np.isfinite(harga) or harga <= 0:
                    harga = c_all[p['ticker']][kk]
                tunai += p['unit'] * harga * (1 - p['ks'])
                dagangan.append(dict(ticker=p['ticker'], masuk=p['tarikh_masuk'], keluar=hari,
                                     hari=p['hari'], sebab=p['sebab'],
                                     saiz_pct=round(p['nilai'] * 100, 2),
                                     pulangan=round(float(p['unit'] * harga * (1 - p['ks'])
                                                          / p['nilai_abs'] - 1) * 100, 2)))
            else:
                baki.append(p)
        posisi = baki
        nilai = tunai
        for p in posisi:
            g = fr[p['ticker']]
            kk = g.index.get_loc(hari) if hari in g.index else None
            if kk is not None and np.isfinite(c_all[p['ticker']][kk]):
                p['harga_akhir'] = c_all[p['ticker']][kk]
            nilai += p['unit'] * p['harga_akhir']
        ekuiti = nilai
        siri.append((hari, ekuiti))
        slot_hari.append(len(posisi))
        ix = kal.get_loc(hari)
        semalam = kal[ix - 1] if ix > 0 else None
        if semalam is None or semalam not in peta:
            continue
        calon = [t for t in peta[semalam] if t in fr and hari in fr[t].index
                 and not any(p['ticker'] == t for p in posisi)]
        calon.sort(key=lambda t: pilihan.get((t, semalam), (0.0, 0.0, t)), reverse=True)
        for t in calon:
            if len(posisi) >= maks_posisi:
                break
            g = fr[t]
            i = g.index.get_loc(semalam)
            if i + 1 >= len(g):
                continue
            ap = atrp_all[t][i]
            if not np.isfinite(ap) or ap <= 0:
                continue
            frac = risiko / (k * ap / 100.0)              # ATR% -> pecahan
            frac = min(max(frac, HAD_BAWAH), HAD_ATAS)
            nilai_pos = ekuiti * frac
            if nilai_pos > tunai:                          # SPEC_1B: langkau, jangan kecilkan
                n_langkau += 1
                continue
            ks = kos_sisi(to_all[t][i])
            harga = o_all[t][i + 1] * (1 + ks)
            if not np.isfinite(harga) or harga <= 0:
                continue
            pra, asas, lv = pra_all[t]
            ik, sebab = exit_hari(pra, asas, lv, c_all[t], o_all[t], i, exit_nama, len(g), k)
            if ik is None:
                continue
            tunai -= nilai_pos
            n_masuk += 1
            saiz.append(frac)
            posisi.append(dict(ticker=t, unit=nilai_pos / harga, ks=ks, nilai=frac,
                               nilai_abs=nilai_pos, tarikh_masuk=hari,
                               tarikh_keluar=g.index[ik], hari=int(ik - i),
                               sebab=sebab, harga_akhir=harga / (1 + ks)))
    info = dict(n_masuk=n_masuk, n_tutup=len(dagangan), n_terbuka=len(posisi),
                n_langkau_tunai=n_langkau,
                purata_posisi=round(float(np.mean(slot_hari)), 2) if slot_hari else 0.0,
                purata_saiz_pct=round(float(np.mean(saiz)) * 100, 2) if saiz else 0.0,
                maks_saiz_pct=round(float(np.max(saiz)) * 100, 2) if saiz else 0.0)
    return pd.DataFrame(siri, columns=['tarikh', 'ekuiti']), pd.DataFrame(dagangan), info


def ringkas(nama, siri, dag, spy, info):
    s = siri.set_index('tarikh')['ekuiti']
    bl = s.resample('ME').last().pct_change()
    bl.iloc[0] = s.resample('ME').last().iloc[0] / 1.0 - 1
    b = bl.dropna() * 100
    return dict(sistem=nama, **info,
                pulangan_tahun=round(float(s.iloc[-1] - 1) * 100, 2),
                median_bulanan=round(float(b.median()), 2),
                purata_bulanan=round(float(b.mean()), 2),
                pct_bulan_ge10=round(float((b >= 10).mean() * 100), 1),
                pct_bulan_positif=round(float((b > 0).mean() * 100), 1),
                bulan_terbaik=round(float(b.max()), 2), bulan_terburuk=round(float(b.min()), 2),
                mdd=round(T.mdd(s.to_numpy()), 2),
                purata_hari_pegang=round(float(dag.hari.mean()), 1) if len(dag) else '',
                spy_pulangan_tahun=round(float(spy.iloc[-1] / spy.iloc[0] - 1) * 100, 2),
                spy_mdd=round(T.mdd(spy.to_numpy()), 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    th = ap.parse_args().tahun
    t0 = time.time()
    kp = pd.read_csv(KELUAR / f'keputusan_{th}.csv')
    calon = kp[kp.keputusan.isin(['CALON', 'DITERIMA'])].signal.tolist()
    asas_lbl = 'CALON selepas Step 8'
    if not calon:
        calon = json.loads((CACHE / f'lulus7_{th}.json').read_text())['signal']
        asas_lbl = 'lulus Step 7 sahaja (TIADA signal CALON tahun ini)'
    cu = pd.read_csv(KELUAR / f'common_unique_{th}.csv')
    lp = cu[(cu.subset == 'S2') & (cu.populasi == 'a') & (cu.kumpulan_data == 'A')
            & (cu.keluarga == 'PADU')].set_index('signal').lift_presisi.to_dict()
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    sig = sig[sig.dalam_univ == 1].reset_index(drop=True)
    sg = S.bina(sig, kuin)
    mana = np.zeros(len(sig), dtype=bool)
    skor = {}
    for nm in calon:
        a = sg[nm]
        mana |= a
        for t, dd, rs in zip(sig.ticker[a], sig.tarikh[a], sig.rs_spy_6b[a]):
            v = (float(lp.get(nm, 0) or 0), float(rs) if np.isfinite(rs) else -999.0, t)
            if skor.get((t, dd), (-1, -1, '')) < v:
                skor[(t, dd)] = v
    entri = sig.loc[mana, ['ticker', 'tarikh']].drop_duplicates().reset_index(drop=True)
    print(f'asas entry: {asas_lbl} ({len(calon)} signal) | kemunculan {len(entri)}')
    fr = D.muat_harga(sorted(entri.ticker.unique()), f'{th - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{th - 2}-06-01', '2026-10-16')
    spy_c = ix['SPY']['close']
    spy_n = ((spy_c > spy_c.rolling(50, min_periods=50).mean())
             & (spy_c > spy_c.rolling(200, min_periods=200).mean()))
    pra_all, c_all, o_all, to_all, atrp_all = {}, {}, {}, {}, {}
    for t, g in fr.items():
        sn = spy_n.reindex(g.index).fillna(False).to_numpy()
        pra_all[t] = _pra_siri(g, sn)
        c_all[t] = g['close'].to_numpy('float64')
        o_all[t] = g['open'].to_numpy('float64')
        to_all[t] = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy()
        atrp_all[t] = pra_all[t][2]['atr'] / np.where(c_all[t] > 0, c_all[t], np.nan) * 100.0
    kal = spy_c.index[(spy_c.index >= pd.Timestamp(f'{th}-01-01'))
                      & (spy_c.index <= pd.Timestamp(f'{th}-12-31'))]
    spy_th = spy_c.reindex(kal).ffill()
    print(f'[{time.time()-t0:.0f}s] data sedia | hari {len(kal)}')

    rawak = pd.read_parquet(CACHE / f'rawak_{th}.parquet')[['ticker', 'tarikh']]
    rawak = rawak[rawak.ticker.isin(fr)].drop_duplicates()
    sk_r = {(t, dd): (0.0, 0.0, t) for t, dd in zip(rawak.ticker, rawak.tarikh)}
    rows = []
    for vn, maks in VARIAN.items():
        for r in RISIKO:
            for k in KVAL:
                nama = f'1b|{vn}|risiko{r*100:.1f}%|k{k}'
                s_, d_, inf = jalankan(entri, fr, pra_all, c_all, o_all, to_all, atrp_all, kal,
                                       'trail_k', r, k, maks, skor)
                rows.append(dict(**ringkas(nama, s_, d_, spy_th, inf), jenis='1b',
                                 varian=vn, risiko=r, k=k))
                print(f"  {nama:34s} pul {rows[-1]['pulangan_tahun']:8.2f}% med "
                      f"{rows[-1]['median_bulanan']:6.2f}% MDD {rows[-1]['mdd']:7.2f}% "
                      f"posisi {inf['purata_posisi']:.1f} saiz {inf['purata_saiz_pct']:.1f}%")
    for ref in ('REF_pegang_252', 'REF_chandelier_4atr', 'REF_jual_hari63'):
        s_, d_, inf = jalankan(entri, fr, pra_all, c_all, o_all, to_all, atrp_all, kal, ref,
                               0.010, 4, 8, skor)
        rows.append(dict(**ringkas(f'1b|{ref}|risiko1.0%|k4', s_, d_, spy_th, inf),
                         jenis='rujukan', varian='V1_maks8', risiko=0.010, k=4))
    for vn, maks in VARIAN.items():
        s_, d_, inf = jalankan(rawak, fr, pra_all, c_all, o_all, to_all, atrp_all, kal, 'trail_k',
                               0.010, 4, maks, sk_r)
        rows.append(dict(**ringkas(f'KAWALAN_RAWAK_1b|{vn}|risiko1.0%|k4', s_, d_, spy_th, inf),
                         jenis='kawalan_rawak', varian=vn, risiko=0.010, k=4))
    out = pd.DataFrame(rows)
    out['asas_entry'] = asas_lbl
    out['had_fasa'] = 'maksimum CALON (SPEC_1B §4)'
    out.to_csv(KELUAR / f'portfolio_1b_{th}.csv', index=False)
    print(f'\n[{time.time()-t0:.0f}s] siap | {len(out)} baris -> portfolio_1b_{th}.csv')


if __name__ == '__main__':
    main()
