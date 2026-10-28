"""STEP 12 — §5.4 portfolio leg SEC (KRITERIA AKHIR, SPEC_FASA2 §5.4 dan §6 syarat 3).

Dijalankan HANYA jika §5.1 dan §5.3 lulus (§6 syarat 1). Jika tidak, tiada apa untuk diuji: mencari
portfolio yang kelihatan baik daripada signal yang sudah gagal ujian kebetulan ialah mencari
kebetulan yang lebih besar.

8 slot x 12.5%, kos penuh, tiga rujukan keluar fasa 1, dua saiz (§5.4):
  - tetap 12.5%
  - berskala risiko SPEC_1B: (RISIKO x ekuiti) / (k x ATR%), had 2-25%, k = 4, risiko 1.0%

Kawalan rawak (§6 syarat 3): entri rawak, bilangan sama SETIAP BULAN, benih 42 — sama seperti
fasa 1. Signal mesti mengalahkannya pada pulangan DAN MDD.

Guna: python3 REVERSE/step12_sec_portfolio.py [--signal nama] [--tahun-min 2012]
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
from REVERSE.teras import data as D, stat as T  # noqa: E402
from REVERSE.step9_portfolio import jalankan, SLOT, BAHAGIAN  # noqa: E402
from REVERSE.step7b_hadapan import _pra_siri  # noqa: E402
import REVERSE.step11_sec_nilai as S11  # noqa: E402

KELUAR = AKAR / 'REVERSE'
RUJUKAN = ['REF_pegang_252', 'REF_chandelier_4atr', 'REF_jual_hari63']
RISIKO, K_ATR, SAIZ_MIN, SAIZ_MAKS = 0.010, 4.0, 0.02, 0.25   # SPEC_1B
BENIH = 42


def saiz_risiko(atrp):
    """Pecahan ekuiti berskala risiko (SPEC_1B). atrp: ticker -> array ATR% sejajar indeks harga."""
    def f(t, i):
        a = atrp.get(t)
        if a is None or i >= a.size or not np.isfinite(a[i]) or a[i] <= 0:
            return BAHAGIAN                      # ATR tidak diketahui: jatuh balik ke saiz tetap
        return min(max(RISIKO / (K_ATR * a[i] / 100.0), SAIZ_MIN), SAIZ_MAKS)
    return f


def sedia_tahun(th, entri_th):
    """(fr, pra_all, c_all, o_all, to_all, atrp, kal, spy) bagi satu tahun."""
    tick = sorted(entri_th.ticker.unique())
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{th - 2}-06-01', '2026-10-16')
    spy_c = ix['SPY']['close']
    spy_n = ((spy_c > spy_c.rolling(50, min_periods=50).mean())
             & (spy_c > spy_c.rolling(200, min_periods=200).mean()))
    pra_all, c_all, o_all, to_all, atrp = {}, {}, {}, {}, {}
    for t, g in fr.items():
        sn = spy_n.reindex(g.index).fillna(False).to_numpy()
        pra_all[t] = _pra_siri(g, sn)
        c_all[t] = g['close'].to_numpy('float64')
        o_all[t] = g['open'].to_numpy('float64')
        to_all[t] = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy()
        tr = pd.concat([g['high'] - g['low'], (g['high'] - g['close'].shift(1)).abs(),
                        (g['low'] - g['close'].shift(1)).abs()], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
        atrp[t] = (atr / g['close'] * 100.0).to_numpy('float64')
    kal = spy_c.index[(spy_c.index >= pd.Timestamp(f'{th}-01-01'))
                      & (spy_c.index <= pd.Timestamp(f'{th}-12-31'))]
    return fr, pra_all, c_all, o_all, to_all, atrp, kal, spy_c.reindex(kal).ffill()


def rawak_sepadan(d, entri, benih=BENIH):
    """Entri rawak: bilangan sama SETIAP BULAN, daripada populasi peristiwa sah tahun itu."""
    rng = np.random.default_rng(benih)
    bhg = []
    e = entri.copy()
    e['bulan'] = pd.to_datetime(e.tarikh).dt.strftime('%Y-%m')
    pop = d[['saham', 'tarikh']].rename(columns={'saham': 'ticker'}).copy()
    pop['bulan'] = pd.to_datetime(pop.tarikh).dt.strftime('%Y-%m')
    for b, g in e.groupby('bulan'):
        kandidat = pop[pop.bulan == b]
        if kandidat.empty:
            continue
        n = min(len(g), len(kandidat))
        bhg.append(kandidat.iloc[rng.choice(len(kandidat), n, replace=False)])
    return (pd.concat(bhg, ignore_index=True)[['ticker', 'tarikh']]
            if bhg else entri[['ticker', 'tarikh']])


def metrik_siri(nama, siri, dag, info):
    """Pulangan tahunan terkompaun, MDD, median bulanan, % bulan >= 10%, bulan terburuk."""
    e = siri.set_index('tarikh').ekuiti
    bulanan = e.resample('ME').last().pct_change().dropna() * 100
    tahun = len(e) / 252.0
    pul = (float(e.iloc[-1]) ** (1 / tahun) - 1) * 100 if tahun > 0 and e.iloc[-1] > 0 else np.nan
    return dict(sistem=nama, n_masuk=info['n_masuk'], slot_purata=info['purata_slot_terisi'],
                pulangan_tahunan=round(pul, 2), mdd=round(T.mdd(e.to_numpy()), 2),
                median_bulanan=round(float(bulanan.median()), 2) if len(bulanan) else np.nan,
                pct_bulan_ge10=round(float((bulanan >= 10).mean() * 100), 1) if len(bulanan) else np.nan,
                bulan_terburuk=round(float(bulanan.min()), 2) if len(bulanan) else np.nan,
                n_bulan=len(bulanan),
                pulangan_median_dagangan=round(float(dag.pulangan.median()), 2) if len(dag) else np.nan)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--signal', default='', help='nama signal; kosong = ambil yang lulus §5.3')
    ap.add_argument('--tahun-min', type=int, default=2012)
    a = ap.parse_args(argv)
    t0 = time.time()

    p53 = KELUAR / 'sec_ujian53.csv'
    if not p53.exists():
        print('sec_ujian53.csv tiada: step11 (§5) belum dijalankan. §5.4 tidak boleh mendahului §5.')
        return 1
    r53 = pd.read_csv(p53)
    if a.signal:
        lulus = [a.signal]
    else:
        lulus = r53.loc[r53.lulus_53.fillna(False), 'signal'].tolist() if 'lulus_53' in r53 else []
    if not lulus:
        print('TIADA signal lulus §5.3 — §5.4 tidak dijalankan (§6 syarat 1 tidak dipenuhi).')
        print('Mencari portfolio daripada signal yang sudah gagal ujian kebetulan hanya mencari')
        print('kebetulan yang lebih besar. Leg SEC fasa 2 DITOLAK pada §5.1/§5.3.')
        return 0
    print(f'signal lulus §5.3: {lulus}')

    d = S11.muat(sorted(int(p.stem.split('_')[1]) for p in S11.CACHE.glob('signals_*.parquet')))
    d = d[d.tahun >= a.tahun_min]
    batas = S11.batas_kuintil(d)
    S = S11.signal_binari(d, batas)

    baris = []
    for nm in lulus:
        ada = S[nm]
        ent = d.loc[ada, ['saham', 'tarikh']].rename(columns={'saham': 'ticker'}).drop_duplicates()
        for jenis, e in (('signal', ent), ('RAWAK', rawak_sepadan(d, ent))):
            for th in sorted(d.tahun.unique()):
                eth = e[pd.to_datetime(e.tarikh).dt.year == th]
                if eth.empty:
                    continue
                fr, pra, c, o, to, atrp, kal, _ = sedia_tahun(th, eth)
                pilihan = {(t, pd.Timestamp(dd)): (0.0, 0.0, t) for t, dd in zip(eth.ticker, eth.tarikh)}
                eth = eth.assign(tarikh=pd.to_datetime(eth.tarikh))
                for ref in RUJUKAN:
                    for saiz_nama, fsaiz in (('tetap', None), ('risiko', saiz_risiko(atrp))):
                        siri, dag, info = jalankan(ref, eth, fr, pra, c, o, to, kal, ref, None,
                                                   pilihan, saiz=fsaiz)
                        if siri.empty:
                            continue
                        m = metrik_siri(f'{nm}|{jenis}|{ref}|{saiz_nama}', siri, dag, info)
                        m.update(signal=nm, jenis=jenis, keluar=ref, saiz=saiz_nama, tahun=th)
                        baris.append(m)
                print(f'[{time.time()-t0:.0f}s] {nm} {jenis} {th}: {len(baris)} baris')
    if not baris:
        print('tiada baris portfolio')
        return 1
    R = pd.DataFrame(baris)
    R.to_csv(KELUAR / 'sec_portfolio.csv', index=False)
    rum = (R.groupby(['signal', 'jenis', 'keluar', 'saiz'])
           [['pulangan_tahunan', 'mdd', 'median_bulanan', 'pct_bulan_ge10', 'bulan_terburuk']]
           .median().round(2).reset_index())
    rum.to_csv(KELUAR / 'sec_portfolio_ringkas.csv', index=False)
    print('\n' + rum.to_string(index=False))
    json.dump(dict(signal=lulus, slot=SLOT, bahagian=BAHAGIAN, risiko=RISIKO, k_atr=K_ATR,
                   n_baris=int(len(R))), open(KELUAR / 'sec_portfolio.json', 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
