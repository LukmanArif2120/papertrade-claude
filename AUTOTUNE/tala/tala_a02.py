# Penala A02 (SPEC_A02 §2–§3). Satu tugasan = (kaedah, lorong, kajian). A01 (tala.py) tidak berubah.
#   lorong : 'had60' (had pegang 60 hari enjin, seperti A01) atau 'asal' (tiada had enjin; TMAX asal kaedah).
#   kajian 0–5 : ujian tahun 2013+k penuh (A dan B); latih = 3 tahun sebelum mula ujian.
#   kajian 6   : AKHIR  — latih 2016-01-01–2018-12-31; ujian 2019-01-01–hujung data (A, B, A+B = pengesahan).
#   kajian 7   : SEMASA — latih 3 tahun terakhir data; tiada ujian.
# Objektif latih (kumpulan A): CAGR portfolio − CAGR SPY tempoh sama (objektif.skor_a02); n/hari/menang daripada
# dagangan yang benar-benar dipegang portfolio. Pemanasan = objektif.panas_a02 (maks(400 hari, 1.6 × (tetingkap + WARM))).
# Output: <keluar>/<ID>_<lorong>/kNN.json (medan 'kaedah' = '<ID>_<lorong>' supaya gabung_hasil.py boleh dipakai).
# Guna: python3 tala_a02.py M54 had60 6 [--percubaan 120] [--cache AUTOTUNE/.cache_a02] [--keluar AUTOTUNE/hasil_a02/tala]
import os, sys, json, time, math, argparse, traceback, warnings
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala as T1
from tala import E, O, salin, _cadang, _bulat
from gabung_hasil import versi_kod

AKAR = T1.AKAR
HASIL = os.path.join(AKAR, 'AUTOTUNE', 'hasil_a02')
KELUAR = os.path.join(HASIL, 'tala')
CACHE = 'AUTOTUNE/.cache_a02'
BENIH = 42
PERCUBAAN = 120
HAD_MINIT = 300
LORONG = ('had60', 'asal')
K_WFO = list(range(6))
K_AKHIR, K_SEMASA = 6, 7
NAMA_KAJIAN = {K_AKHIR: 'AKHIR', K_SEMASA: 'SEMASA'}
SARING = ('2013-01-01', '2018-12-31')
TAG_A02 = 'autotune-data-a02'


def ambil_data(cache=CACHE):
    """Direktori data A02 (Release autotune-data-a02). Guna pilihan tag pemuat jika ada; jika tidak, TAG modul
    ditukar supaya muat turun automatik tidak sekali-kali mengambil data A01."""
    import inspect
    import data
    if 'tag' in inspect.signature(data.ambil).parameters: return data.ambil(cache, tag=TAG_A02)
    data.TAG = TAG_A02
    return data.ambil(cache)


def tetingkap(k, akhir_data):
    """dict(latih=(L0, L1), ujian=(U0, U1) | None) bagi kajian A02 k."""
    T = pd.Timestamp; ad = T(akhir_data)
    if 0 <= k <= 5:
        y = 2013 + k; return dict(latih=(T(f'{y - 3}-01-01'), T(f'{y - 1}-12-31')), ujian=(T(f'{y}-01-01'), T(f'{y}-12-31')))
    if k == K_AKHIR: return dict(latih=(T('2016-01-01'), T('2018-12-31')), ujian=(T('2019-01-01'), ad))
    if k == K_SEMASA: return dict(latih=(ad - pd.DateOffset(years=3) + pd.Timedelta(days=1), ad), ujian=None)
    raise ValueError(f'kajian A02 {k} tidak sah')


def nama_tugas(mid, lorong):
    return f'{mid}_{lorong}'


def pecah_tugas(nama):
    mid, _, lorong = str(nama).partition('_')
    return mid, lorong


class Penilai02(T1.Penilai):
    """Penilai A01 + SPY tempoh sama + lorong + dagangan dipegang (SPEC_A02 §2)."""
    def __init__(self, m, fr, idx, univ, sumber, mula, akhir, kumpulan_list):
        super().__init__(m, fr, idx, univ, sumber, mula, akhir, kumpulan_list)
        spy = idx.get('SPY')
        if spy is None or not len(spy): raise RuntimeError('tiada SPY dalam idx')
        self.spy_cv = O.spy_lengkung(spy['close'], self.pasaran.tarikh)
        self.spy_r = E.pulangan_harian(self.spy_cv)

    def jalan02(self, P, kumpulan_list=None, lorong_list=('had60',), harian=False):
        """Pulang {(lorong, kumpulan): (metrik_a02, pulangan_harian | None, dagangan_dipegang)}; sedia() sekali."""
        m = self.m; Pp = dict(m.PARAM); Pp.update(P or {})
        f = salin(self.fr); m.sedia(f, self.idx, Pp)
        tmax = Pp['tmax'] if 'tmax' in Pp else m.TMAX
        sejajar = self.asas.sejajar(f)
        S = E.Susun(f, asas=self.asas if sejajar else None)
        out = {}
        for k in (kumpulan_list or list(self.tp)):
            tp = self.tp[k] if sejajar else self.sumber.topeng(f, self.univ, k)
            Sk = S.dengan_topeng(tp)
            for lo in lorong_list:
                Tt = Sk.dagangan(tmax, m.WARM, self.mula, self.akhir, had60=E.had60_lorong(lo))
                cv, Tp = self.pasaran.lengkung(Tt, pegang=True)
                out[(lo, k)] = (O.ringkas_a02(Tp, cv, self.spy_cv), E.pulangan_harian(cv) if harian else None, Tp)
        return out


def metrik_json(mt):
    d = {k: mt[k] for k in ('cagr', 'mdd', 'n', 'win', 'avg', 'days', 'thn_min', 'spy_cagr', 'spy_mdd', 'lebihan')}
    d['tahunan'] = {str(y): v for y, v in mt['tahunan'].items()}
    d['tahunan_lebih'] = {str(y): v for y, v in mt['tahunan_lebih'].items()}
    return _bulat(d)


def tala(mid, lorong, k, sumber, n_trials=PERCUBAAN, had_minit=HAD_MINIT, tamat=None, keluar=KELUAR, tulis=True):
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING); warnings.filterwarnings('ignore')
    t0 = time.time(); masa = {}
    tamat = min(tamat or math.inf, t0 + had_minit * 60)
    H = dict(kaedah=nama_tugas(mid, lorong), id_kaedah=mid, lorong=lorong, kajian=k, kajian_a02=True,
             nama_kajian=NAMA_KAJIAN.get(k, f'WF{k:02d}'), n_trials_diminta=n_trials, ralat=[], status='MULA',
             versi_kod=versi_kod(mid), mula=pd.Timestamp.now('UTC').strftime('%Y-%m-%dT%H:%M:%SZ'))
    try:
        E.had60_lorong(lorong)
        m = T1.muat_kaedah(mid)
        panas = pd.Timedelta(days=O.panas_a02(m))
        H.update(belum_ditala=bool(m.BELUM_DITALA), tala=list(m.TALA), silang=bool(m.SILANG), tmax_asal=m.TMAX,
                 warm=m.WARM, panas_hari=int(panas.days))
        w = tetingkap(k, sumber.akhir_data()); L0, L1 = w['latih']
        H['latih'] = [str(L0.date()), str(L1.date())]
        H['ujian'] = [str(w['ujian'][0].date()), str(w['ujian'][1].date())] if w['ujian'] else None
        kl = 'AB' if m.SILANG else 'A'
        t = time.time(); fr, idx, univ = sumber.muat(L0 - panas, L1, kl); masa['muat_latih'] = time.time() - t
        H['n_ticker_latih'] = len(fr)
        if not fr or not any((g.index >= L0).any() for g in fr.values()): raise RuntimeError('tiada data latih')
        pn = Penilai02(m, fr, idx, univ, sumber, L0, L1, ['A'])
        rekod = []; jejak = {}; s_cuba = []

        def obj(tr):
            ts = time.time()
            P = _cadang(tr, m) if m.TALA else {}
            kunci = tuple(sorted(P.items()))
            if kunci in jejak:
                tr.set_user_attr('ulang', True); return jejak[kunci]['skor']
            try:
                mt, rh, _ = pn.jalan02(P, ['A'], (lorong,), harian=True)[(lorong, 'A')]
                r = dict(P=P, skor=O.skor_a02(mt), lulus=O.lulus_a02(mt), thn_min=mt['thn_min'], m=mt,
                         rh=(rh - pn.spy_r.reindex(rh.index).fillna(0.0)).values.astype(np.float32))
            except Exception as e:
                r = dict(P=P, skor=-2.0, lulus=False, thn_min=-1.0, m=None, rh=None, ralat=f'{type(e).__name__}: {e}'[:300])
                if len(H['ralat']) < 5: H['ralat'].append('percubaan: ' + r['ralat'])
            if not math.isfinite(r['skor']): r['skor'] = -2.0
            jejak[kunci] = r; rekod.append(r); s_cuba.append(time.time() - ts)
            return r['skor']

        lebih = 3 if w['ujian'] else 0

        def henti(st, tr):
            purata = np.mean(s_cuba) if s_cuba else 0
            if time.time() + purata * (1 + lebih) > tamat: st.stop()

        st = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=BENIH + k))
        if m.TALA:
            st.enqueue_trial({p: m.PARAM[p] for p in m.TALA}); n_cuba = n_trials
        else:
            n_cuba = 1
        t = time.time()
        st.optimize(obj, n_trials=n_cuba, callbacks=[henti], catch=(Exception,))
        masa['optuna'] = time.time() - t
        H['n_trials'] = len(st.trials); H['n_unik'] = len(rekod); H['n_sasaran'] = n_cuba
        masa['s_percubaan'] = float(np.mean(s_cuba)) if s_cuba else None
        if len(st.trials) < n_cuba: H['ralat'].append(f'had masa: {len(st.trials)}/{n_cuba} percubaan')
        sah = [r for r in rekod if r['m'] is not None]
        if not sah: raise RuntimeError('semua percubaan gagal')
        pil, ada_lulus = O.pilih_teguh(sah)
        H['ada_lulus'] = ada_lulus
        H['params'] = _bulat(pil['P']); H['params_penuh'] = _bulat({**m.PARAM, **pil['P']})
        H['skor'] = _bulat(pil['skor']); H['latih_A'] = metrik_json(pil['m'])
        H['top10'] = [dict(params=_bulat(r['P']), skor=_bulat(r['skor']), lulus=r['lulus'], lebihan=_bulat(r['m']['lebihan']),
                           mdd=_bulat(r['m']['mdd']), n=r['m']['n'], thn_min=_bulat(r['thn_min']))
                      for r in sorted(sah, key=lambda r: r['skor'], reverse=True)[:10]]
        asal = jejak.get(tuple(sorted({p: m.PARAM[p] for p in m.TALA}.items())))
        if asal and asal['m'] is not None: H['latih_A_asal'] = metrik_json(asal['m'])
        if k == K_AKHIR:   # PBO (dilaporkan sahaja): 50 percubaan teratas, pulangan berlebihan harian latih
            atas = [r for r in sorted(sah, key=lambda r: r['skor'], reverse=True) if r['rh'] is not None][:50]
            if len(atas) >= 2:
                H['pbo'] = _bulat(dict(O.pbo(np.column_stack([r['rh'] for r in atas]), 8), n_percubaan=len(atas)))
        del pn, fr; sumber._fr.clear()

        if w['ujian']:
            U0, U1 = w['ujian']; t = time.time()
            fr, idx, univ = sumber.muat(U0 - panas, U1, 'AB')
            kum = ['A', 'B', 'AB'] if k == K_AKHIR else ['A', 'B']
            pu = Penilai02(m, fr, idx, univ, sumber, U0, U1, kum)
            hs = pu.jalan02(pil['P'], kum, (lorong,), harian=True)
            H['harian_ujian'] = dict(tarikh=[str(d.date()) for d in pu.pasaran.tarikh],
                                     SPY=[round(float(x), 6) for x in pu.spy_r])
            for (lo, g), (mt, rh, _) in hs.items():
                H[f'ujian_{g}'] = metrik_json(mt)
                H['harian_ujian'][g] = [round(float(x), 6) for x in rh]
            del pu, fr; sumber._fr.clear(); masa['ujian'] = time.time() - t
        H['status'] = 'SIAP'
    except Exception as e:
        H['status'] = 'RALAT'; H['ralat'].append(f'{type(e).__name__}: {e}'[:500])
        H['jejak'] = traceback.format_exc()[-1500:]
    masa['jumlah'] = time.time() - t0
    try:
        import resource; H['rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    except Exception: pass
    H['masa'] = _bulat(masa, 2); H['n_trials'] = H.get('n_trials', 0)
    if tulis: T1.simpan(H, keluar)
    return H


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('kaedah'); a.add_argument('lorong', choices=LORONG); a.add_argument('kajian', type=int)
    a.add_argument('--percubaan', type=int, default=PERCUBAAN); a.add_argument('--had-minit', type=float, default=HAD_MINIT)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', CACHE))
    a.add_argument('--keluar', default=KELUAR)
    x = a.parse_args(argv)
    H = tala(x.kaedah, x.lorong, x.kajian, T1.Sumber(ambil_data(x.cache)), x.percubaan, x.had_minit, keluar=x.keluar)
    print(H['kaedah'], H['kajian'], H['status'], 'skor', H.get('skor'), 'masa', H['masa'].get('jumlah'), H['ralat'][:2])


if __name__ == '__main__':
    main()
