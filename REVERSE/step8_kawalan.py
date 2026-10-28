"""STEP 8 — kawalan kebetulan (WAJIB sebelum kesimpulan).

8.1 pengesahan dalam tahun (kumpulan B) + merentas tahun (tahun lain yang sudah siap)
8.2 ujian label rawak 1000x (tukar label hasil, bilangan sama setiap bulan) + BH-FDR q <= 0.01,
    BERASINGAN bagi keluarga ENTRY, HOLD, EXIT, SISTEM; keluarga SUPER PADU FDR sendiri
8.3 bootstrap 1000x, blok ikut ticker DAN berasingan ikut minggu
8.4 jangkaan atas SEMUA kemunculan + ulang tanpa 5% pemenang teratas
8.5 penapis Step 7.4 kekal CALON (perlu >= 2 tahun lain)
8.6 tanda STATISTIK SAHAJA jika tiada penjelasan pasaran dipradaftar
8.7 keputusan gate demi gate; 8.8 had fasa: maksimum CALON

Guna: python3 REVERSE/step8_kawalan.py 2025
Output: REVERSE/keputusan_<TAHUN>.csv
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
from REVERSE.teras import signal as S, stat as T  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
NPERM = 1000
NBOOT = 1000
Q = 0.01

# 8.6 penjelasan pasaran dipradaftar bagi setiap bahan signal
PENJELASAN = {
    'atr_pct': 'kemeruapan tinggi = julat kenaikan lebih besar bagi tempoh sama',
    'bb_lebar': 'lebar Bollinger tinggi = pengembangan kemeruapan, biasanya permulaan trend',
    'julat20': 'julat 20 hari luas = pergerakan sedang berlaku, bukan asas mendatar',
    'j_52w_tinggi': 'dekat/jauh tertinggi 52 minggu = kedudukan dalam kitaran harga',
    'j_ema9': 'jarak dari EMA9 = momentum jangka sangat pendek',
    'j_ma200': 'kedudukan vs MA200 = trend jangka panjang',
    'j_ma50': 'kedudukan vs MA50 = trend jangka sederhana',
    'cerun_ma50': 'kecerunan MA50 = arah trend sederhana',
    'rs_spy_6b': 'kekuatan relatif 6 bulan = aliran modal institusi',
    'lapis': 'susunan MA = struktur trend',
    'vol_n50': 'volum relatif = penyertaan',
    'roc20': 'momentum 20 hari',
    'sektor_1b': 'putaran sektor',
    'macd_cross': 'cross MACD = perubahan momentum',
    'rsi_lintas50': 'RSI lintas 50 = momentum bertukar positif',
    'ema_crossback': 'tutup kembali atas EMA21 = pullback tamat',
    'donchian20': 'breakout 20 hari',
    'pocket_pivot': 'lonjakan volum pada hari naik = permintaan institusi',
    'gap_and_go': 'gap berita diikuti kekuatan',
}


def _penjelasan(nm):
    bahan = [b for b in PENJELASAN if b in nm]
    return '; '.join(PENJELASAN[b] for b in bahan) if bahan else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a_ = ap.parse_args()
    th = a_.tahun
    t0 = time.time()
    cu = pd.read_csv(KELUAR / f'common_unique_{th}.csv')
    fs = pd.read_csv(KELUAR / f'false_signal_{th}.csv')
    he = pd.read_csv(KELUAR / f'hold_exit_{th}.csv')
    hh = pd.read_csv(KELUAR / f'hadapan_hold_exit_{th}.csv')
    corong = json.loads((CACHE / f'corong_{th}.json').read_text())['signal']
    lulus7 = json.loads((CACHE / f'lulus7_{th}.json').read_text())['signal']
    l7b = json.loads((CACHE / f'lulus7b_{th}.json').read_text())
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    sig = sig[sig.dalam_univ == 1].reset_index(drop=True)
    had = pd.read_parquet(CACHE / f'hadapan_{th}.parquet')
    ev = sig[sig.jenis_peristiwa != ''].reset_index(drop=True)
    sg_ev = S.bina(ev, kuin)
    print(f'[{time.time()-t0:.0f}s] signal corong {len(corong)} | lulus Step 7 {len(lulus7)}'
          f' | sistem lulus 7b {len(l7b["sistem"])}')

    # ---------- keluarga ENTRY ----------
    rows = []
    m2 = ((ev.run_jenis.to_numpy() == 'BERTANGGA') | (ev.hasil.to_numpy() == 'GAGAL'))
    mpa = ev.jenis_peristiwa.isin(['mula_run', 'tiada_run']).to_numpy()
    for kel in ('PADU', 'SUPER PADU'):
        for kd in ('A', 'B'):
            m = m2 & mpa & (ev.kumpulan_data.to_numpy() == kd)
            hasil = ev.hasil.to_numpy()[m]
            bulan = ev.tarikh.dt.strftime('%Y-%m').to_numpy()[m]
            tick = ev.ticker.to_numpy()[m]
            mgg = ev.tarikh.dt.strftime('%G-W%V').to_numpy()[m]
            for nm in corong:
                ada = sg_ev[nm][m]
                if ada.sum() < 10:
                    continue
                p, lr = T.permutasi_lift(hasil, ada, bulan, kel, NPERM, 42)
                lb_t = T.bootstrap_lift_blok(hasil, ada, tick, kel, NBOOT, 42)
                lb_m = T.bootstrap_lift_blok(hasil, ada, mgg, kel, NBOOT, 42)
                rows.append(dict(keluarga=f'ENTRY/{kel}', kumpulan_data=kd, signal=nm,
                                 n=int(ada.sum()), nilai_p=p, lift_purata_rawak=lr,
                                 lift_bawah95_blok_ticker=lb_t, lift_bawah95_blok_minggu=lb_m))
    pm = pd.DataFrame(rows)
    print(f'[{time.time()-t0:.0f}s] permutasi + bootstrap ENTRY siap ({len(pm)} baris)')

    # ---------- 8.4 jangkaan atas SEMUA kemunculan ----------
    df = sig.merge(had, on=['ticker', 'tarikh'], how='left')
    sg_all = S.bina(df, kuin)
    jrows = []
    for nm in corong:
        d = df[sg_all[nm]]
        v = d.pul_henti2atr.to_numpy('float64')
        v = v[np.isfinite(v)]
        if v.size < 30:
            continue
        jk, km, pm_, pk = T.jangkaan(v)
        amb = np.quantile(v, 0.95)
        v2 = v[v <= amb]
        jk2, *_ = T.jangkaan(v2)
        lb_t = T.bootstrap_blok(d.pul_henti2atr.to_numpy('float64'), d.ticker.to_numpy(),
                                NBOOT, 42)
        lb_m = T.bootstrap_blok(d.pul_henti2atr.to_numpy('float64'),
                                d.tarikh.dt.strftime('%G-W%V').to_numpy(), NBOOT, 42)
        jrows.append(dict(signal=nm, n_kemunculan=int(v.size),
                          median_pulangan=round(float(np.median(v)) * 100, 2),
                          jangkaan=round(jk * 100, 3),
                          jangkaan_tanpa_5pct_teratas=round(jk2 * 100, 3),
                          pct_rugi_lebih_10=round(float((v < -0.10).mean() * 100), 1),
                          siri_kalah_terpanjang=T.siri_kalah_terpanjang(v),
                          jangkaan_bawah95_blok_ticker=round(lb_t[0] * 100, 3),
                          jangkaan_bawah95_blok_minggu=round(lb_m[0] * 100, 3)))
    jn = pd.DataFrame(jrows)
    print(f'[{time.time()-t0:.0f}s] jangkaan + bootstrap kemunculan siap')

    # ---------- FDR per keluarga ----------
    fdr = {}
    for kel in sorted(pm.keluarga.unique()):
        d = pm[(pm.keluarga == kel) & (pm.kumpulan_data == 'A')]
        lulus, amb = T.bh_fdr(d.nilai_p.to_numpy('float64'), Q)
        fdr[kel] = dict(n=len(d), lulus=int(lulus.sum()), ambang=amb,
                        signal=d.signal.to_numpy()[lulus].tolist())
    # HOLD / EXIT: permutasi atas snapshot
    for fasa, fail, lab in (('HOLD', f'snap_hold_{th}.csv', 'puncak_baru'),
                            ('EXIT', f'snap_exit_{th}.csv', 'sebelum_puncak_akhir')):
        sp = pd.read_csv(CACHE / fail)
        sp['tarikh'] = pd.to_datetime(sp['tarikh'])
        hasil = np.where(sp[lab].to_numpy() == 1, 'PADU', 'GAGAL')
        bulan = sp.tarikh.dt.strftime('%Y-%m').to_numpy()
        sgx = S.bina(sp, kuin)
        pilih = ([k for k in sgx if k.startswith('b:')] if fasa == 'HOLD'
                 else [k for k in sgx if k.startswith(('q1:', 'q5:'))])
        ps, nmx = [], []
        for nm in pilih:
            if sgx[nm].sum() < 20:
                continue
            p, _ = T.permutasi_lift(hasil, sgx[nm], bulan, 'PADU', 200, 42)
            ps.append(p)
            nmx.append(nm)
        lulus, amb = T.bh_fdr(np.array(ps), Q)
        fdr[fasa] = dict(n=len(ps), lulus=int(lulus.sum()), ambang=amb,
                         signal=[nmx[i] for i in np.flatnonzero(lulus)], nperm=200)
    # SISTEM (7b): nilai-p bootstrap blok terhadap rujukan terbaik
    z = np.load(CACHE / f'dagangan7b_{th}.npz', allow_pickle=True)
    pul, tkr, mgu, sis = z['pul'], z['ticker'], z['minggu'], z['sistem']
    ambang = l7b['ambang'] / 100.0
    ps, nmx, lb = [], [], []
    unik, inv = np.unique(tkr, return_inverse=True)
    peta = [np.flatnonzero(inv == i) for i in range(unik.size)]
    rng0 = np.random.default_rng(42)
    # indeks bootstrap dikongsi semua sistem (benih 42) supaya ia setara dan laju
    IDX = [np.concatenate([peta[j] for j in rng0.integers(0, unik.size, unik.size)])
           for _ in range(200)]
    for q, nm in enumerate(sis):
        if nm.startswith('REF_'):
            continue
        v = pul[:, q]
        if np.isfinite(v).sum() < 50:
            continue
        jj = np.empty(200)
        for k in range(200):
            jj[k] = T.jangkaan(v[IDX[k]])[0]
        ps.append(float((jj <= ambang).mean()))
        nmx.append(str(nm))
        lb.append(float(np.quantile(jj[np.isfinite(jj)], 0.05)) if np.isfinite(jj).any() else np.nan)
    lulus, amb = T.bh_fdr(np.array(ps), Q)
    fdr['SISTEM'] = dict(n=len(ps), lulus=int(lulus.sum()), ambang=amb,
                         signal=[nmx[i] for i in np.flatnonzero(lulus)], nboot=200)
    (CACHE / f'fdr_{th}.json').write_text(json.dumps(fdr, indent=1, default=str))
    print('FDR per keluarga (q <= 0.01):')
    for k, v in fdr.items():
        print(f'  {k:18s} N={v["n"]:4d} lulus={v["lulus"]:4d} ambang_p={v["ambang"]}')

    # ---------- 8.7 keputusan gate demi gate ----------
    kls_A = cu[(cu.subset == 'S2') & (cu.populasi == 'a') & (cu.kumpulan_data == 'A')
               & (cu.keluarga == 'PADU')].set_index('signal')
    kls_B = cu[(cu.subset == 'S2') & (cu.populasi == 'a') & (cu.kumpulan_data == 'B')
               & (cu.keluarga == 'PADU')].set_index('signal')
    pmA = pm[(pm.keluarga == 'ENTRY/PADU') & (pm.kumpulan_data == 'A')].set_index('signal')
    jni = jn.set_index('signal')
    fsi = fs[~fs.signal.str.contains(r'\| penapis:')].set_index('signal')
    lulus_fdr = set(fdr['ENTRY/PADU']['signal'])
    # 8.1 merentas tahun (pindaan SPEC §13.12, keputusan pengguna 28 Okt 2026):
    # naik taraf ke DITERIMA memerlukan signal LULUS GATE KERAS (step7 + G1 + G3 + G4 + G5)
    # dalam >= 2 tahun LAIN -- bukan sekadar kelas Step 4 yang sama. Kelas tetap dilaporkan.
    lain = sorted(int(f.stem.split('_')[-1]) for f in KELUAR.glob('common_unique_*.csv')
                  if f.stem.split('_')[-1].isdigit() and int(f.stem.split('_')[-1]) != th)
    g2_lab, g2_asas = {}, ('TIDAK TERSEDIA (tiada tahun lain siap)' if not lain
                           else f'perlu >= 2 tahun lain; siap: {lain}')
    PENEMUAN = ('TERAS', 'UNIQUE', 'LANGKA')
    if lain:
        kelas_lain, keras_lain = {}, {}
        for y in lain:
            dy = pd.read_csv(KELUAR / f'common_unique_{y}.csv')
            dy = dy[(dy.subset == 'S2') & (dy.populasi == 'a') & (dy.kumpulan_data == 'A')
                    & (dy.keluarga == 'PADU')]
            kelas_lain[y] = dy.set_index('signal').kelas.to_dict()
            fy = KELUAR / f'keputusan_{y}.csv'
            if fy.exists():
                ky = pd.read_csv(fy).set_index('signal')
                if 'lulus_gate_keras' in ky.columns:
                    keras_lain[y] = (ky.lulus_gate_keras == 'ya').to_dict()
                else:  # laluan pertama: lajur belum ditulis
                    keras_lain[y] = ky.keputusan.isin(['CALON', 'DITERIMA']).to_dict()
            else:
                keras_lain[y] = {}
        for nm in corong:
            kA = kls_A.kelas.get(nm, '-')
            but = '; '.join(f'{y}={kelas_lain[y].get(nm, "-")}' for y in lain)
            if kA not in PENEMUAN:
                g2_lab[nm] = f'TIDAK BOLEH DINILAI (kelas tahun ini {kA}, bukan penemuan; {but})'
                continue
            lulus_lain = [y for y in lain if keras_lain.get(y, {}).get(nm, False)]
            sama = [y for y in lain if kelas_lain[y].get(nm, '-') == kA]
            g2_lab[nm] = (
                f'LULUS ({len(lulus_lain)}/{len(lain)} tahun lain LULUS GATE KERAS: '
                f'{lulus_lain}; kelas: {but})' if len(lulus_lain) >= 2 else
                f'BELUM ({len(lulus_lain)}/{len(lain)} tahun lain lulus gate keras, perlu >= 2; '
                f'kelas sama {len(sama)}/{len(lain)}; {but})')
    krow = []
    for nm in corong:
        g = {}
        g['G1_kelas_A'] = kls_A.kelas.get(nm, '-')
        g['G1_kelas_B'] = kls_B.kelas.get(nm, '-')
        g['G1_sah_dalam_tahun'] = ('LULUS' if g['G1_kelas_A'] == g['G1_kelas_B']
                                   else ('SEBAHAGIAN' if g['G1_kelas_B'] in
                                         ('TERAS', 'UNIQUE', 'LANGKA', 'SEDERHANA') else 'GAGAL'))
        g['G2_merentas_tahun'] = g2_lab.get(nm, g2_asas)
        g['G3_nilai_p'] = round(float(pmA.nilai_p.get(nm, np.nan)), 5)
        g['G3_fdr'] = 'LULUS' if nm in lulus_fdr else 'GAGAL'
        lbt = pmA.lift_bawah95_blok_ticker.get(nm, np.nan)
        lbm = pmA.lift_bawah95_blok_minggu.get(nm, np.nan)
        g['G4_lift_bawah95_ticker'] = round(float(lbt), 3) if pd.notna(lbt) else ''
        g['G4_lift_bawah95_minggu'] = round(float(lbm), 3) if pd.notna(lbm) else ''
        jbt = jni.jangkaan_bawah95_blok_ticker.get(nm, np.nan)
        jbm = jni.jangkaan_bawah95_blok_minggu.get(nm, np.nan)
        g['G4_jangkaan_bawah95_ticker'] = jbt
        g['G4_jangkaan_bawah95_minggu'] = jbm
        g['G4_bootstrap'] = ('LULUS' if (pd.notna(lbt) and pd.notna(lbm) and lbt >= 1.5
                                         and lbm >= 1.5 and pd.notna(jbt) and jbt > 0
                                         and pd.notna(jbm) and jbm > 0) else 'GAGAL')
        jk = jni.jangkaan.get(nm, np.nan)
        jk2 = jni.jangkaan_tanpa_5pct_teratas.get(nm, np.nan)
        g['G5_jangkaan'] = jk
        g['G5_jangkaan_tanpa_5pct'] = jk2
        g['G5_outlier'] = ('BERGANTUNG PADA OUTLIER' if (pd.notna(jk2) and jk2 <= 0) else 'LULUS')
        g['G6_penjelasan'] = _penjelasan(nm)
        g['G6'] = 'LULUS' if g['G6_penjelasan'] else 'STATISTIK SAHAJA'
        g['step7'] = 'LULUS' if nm in lulus7 else 'GAGAL (BUNYI LATAR)'
        g['kapasiti'] = fsi.kapasiti.get(nm, '')
        keras = (g['step7'] == 'LULUS' and g['G3_fdr'] == 'LULUS' and g['G4_bootstrap'] == 'LULUS'
                 and g['G5_outlier'] == 'LULUS' and g['G1_sah_dalam_tahun'] != 'GAGAL')
        g['lulus_gate_keras'] = 'ya' if keras else 'tidak'
        g['keputusan'] = ('DITERIMA' if (keras and g['G2_merentas_tahun'].startswith('LULUS'))
                          else ('CALON' if keras else 'DITOLAK'))
        g['had_fasa'] = ('maksimum CALON sebelum >= 2 tahun lain LULUS GATE KERAS bagi signal '
                         'yang sama (gate 8.1, SPEC §11.8 + §13.12)')
        krow.append(dict(signal=nm, **g))
    kp = pd.DataFrame(krow)
    kp.to_csv(KELUAR / f'keputusan_{th}.csv', index=False)
    pm.to_csv(KELUAR / f'kawalan_rawak_bootstrap_{th}.csv', index=False)
    jn.to_csv(KELUAR / f'jangkaan_kemunculan_{th}.csv', index=False)
    print(f'\nKEPUTUSAN tahun {th} (maksimum CALON sebelum >= 2 tahun lain disahkan):')
    print(kp[['signal', 'G1_sah_dalam_tahun', 'G3_nilai_p', 'G3_fdr', 'G4_bootstrap',
              'G5_outlier', 'G6', 'step7', 'keputusan']].to_string(index=False))
    print(f"\nCALON {int((kp.keputusan=='CALON').sum())} | DITOLAK "
          f"{int((kp.keputusan=='DITOLAK').sum())}")
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()
