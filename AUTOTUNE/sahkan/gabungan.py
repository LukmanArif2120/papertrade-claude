# F6 Portfolio gabungan (SPEC §6). Calon = TINGGI + SEDERHANA (parameter_sedia.csv).
# Bagi setiap calon dan setiap tetingkap 0–11 (A dan B) serta k12 (A+B), dagangan dijana semula dengan parameter
# pilihan tetingkap itu (cache AUTOTUNE/.cache/gabungan/). Rank setiap dagangan = persentil rank dalam kaedah
# sendiri antara dagangan yang masuk pada hari yang sama (transformasi monoton, jadi gabungan satu kaedah = OOS
# kaedah itu). Dagangan kaedah terpilih dikongsi dalam satu portfolio 8 × 12.5% (enjin_at.Pasaran) bagi setiap
# tetingkap; pulangan harian tetingkap disambung. Pemilihan tamak atas OOS-A; nilai akhir atas OOS-B dan kunci.
#   python3 AUTOTUNE/sahkan/gabungan.py [--maks 6] [--data DIR]
import argparse, hashlib, importlib, json, os, sys, time
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umum as U
import pengesahan as P

HAD_KOR = 0.7
MAKS = 6
CACHE_G = os.path.join(U.CACHE, 'gabungan')


# ---------- logik pemilihan (tulen; diuji dengan data palsu) ----------
def korelasi(a, b):
    x = pd.concat([a, b], axis=1, join='inner').dropna()
    if len(x) < 20 or x.iloc[:, 0].std() == 0 or x.iloc[:, 1].std() == 0: return 0.0
    return float(x.iloc[:, 0].corr(x.iloc[:, 1]))


def pilih_tamak(calon, r_individu, nilai_fn, maks=MAKS, had_kor=HAD_KOR, had_mdd=U.HAD_MDD):
    """calon: senarai ID tersusun ikut CAGR OOS-A menurun. r_individu: {id: siri pulangan harian OOS-A kaedah}.
    nilai_fn(senarai_id) -> (cagr, mdd) gabungan OOS-A. Pulang (terpilih, log, (cagr, mdd) akhir)."""
    log = []
    if not calon: return [], log, (float('nan'), float('nan'))
    pilih = [calon[0]]
    c0, d0 = nilai_fn(pilih)
    log.append(dict(langkah=1, kaedah=calon[0], tindakan='mula', cagr=c0, mdd=d0))
    for k in calon[1:]:
        if len(pilih) >= maks: break
        kor = {s: korelasi(r_individu[k], r_individu[s]) for s in pilih}
        kmaks = max(kor.values())
        if kmaks > had_kor:
            log.append(dict(langkah=len(log) + 1, kaedah=k, tindakan='langkau: korelasi',
                            korelasi=kmaks, dengan=max(kor, key=kor.get)))
            continue
        c, d = nilai_fn(pilih + [k])
        if c > c0 and d >= had_mdd:
            pilih.append(k); c0, d0 = c, d
            log.append(dict(langkah=len(log) + 1, kaedah=k, tindakan='tambah', cagr=c, mdd=d, korelasi=kmaks))
        else:
            sebab = 'CAGR tidak naik' if not c > c0 else 'MDD < -30%'
            log.append(dict(langkah=len(log) + 1, kaedah=k, tindakan='tolak: ' + sebab, cagr=c, mdd=d, korelasi=kmaks))
    return pilih, log, (c0, d0)


def persentil(T):
    """rank → persentil (0,1] dalam kaedah, antara dagangan yang masuk pada hari sama."""
    if not len(T): return T
    T = T.copy()
    T['rank'] = T.groupby('ent')['rank'].rank(pct=True, method='average')
    return T


def kongsi(senarai_T):
    """Gabung dagangan beberapa kaedah (urutan senarai = keutamaan seri)."""
    s = [t for t in senarai_T if t is not None and len(t)]
    if not s: return pd.DataFrame(columns=['ticker', 'ent', 'ex', 'ret', 'rank', 'days'])
    return pd.concat(s, ignore_index=True).sort_values(['ent', 'rank'], ascending=[True, False], kind='stable')


# ---------- tetingkap ----------
def tetingkap_kajian(d, k):
    """(latih_mula, ujian_mula, ujian_akhir|None) daripada JSON kajian (latih [L0, L1], ujian [U0, U1]);
    jika tiada, ikut SPEC §4."""
    lt = d.get('latih') if isinstance(d, dict) else None
    uj = d.get('ujian') if isinstance(d, dict) else None
    if isinstance(uj, (list, tuple)) and len(uj) == 2:
        um, ua = str(uj[0])[:10], str(uj[1])[:10]
    elif k <= 10: um, ua = f'{2013 + k}-01-01', f'{2013 + k}-12-31'
    elif k == 11: um, ua = '2024-01-01', '2024-09-30'
    else: um, ua = '2024-10-01', None
    lm = str(lt[0])[:10] if isinstance(lt, (list, tuple)) and lt else \
        (pd.Timestamp(um) - pd.DateOffset(years=3)).strftime('%Y-%m-%d')
    return lm, um, ua


# ---------- penjana dagangan: logik ujian AUTOTUNE/tala/tala.py (sedia atas AB, topeng kumpulan) ----------
class Penjana:
    """Jana semula dagangan ujian (kaedah, kajian, kumpulan) sama seperti tala.tala(): data AB
    [latih_mula − 400 hari, ujian_akhir], sedia(salin(fr), idx, PARAM ∪ params), Susun.dengan_topeng(kumpulan)
    .dagangan(tmax, WARM, U0, U1). Dagangan dicache ke parquet; Pasaran (tutup AB) dicache bagi setiap kajian."""
    def __init__(self, data_dir=None):
        sys.path.insert(0, os.path.join(U.AT, 'tala'))
        self.T = importlib.import_module('tala')
        self.E = self.T.E
        self.sumber = self.T.Sumber(data_dir)
        self._k = None; self._d = None
        self._pasaran = {}; self._mod = {}
        os.makedirs(CACHE_G, exist_ok=True)

    def _laluan(self, kid, k, g, Pm):
        h = hashlib.md5(json.dumps(Pm, sort_keys=True, default=str).encode()).hexdigest()[:8]
        return os.path.join(CACHE_G, f'dag_{kid}_k{k:02d}_{g}_{h}.parquet')

    def _muat(self, k, lm, um, ua):
        if self._k == k: return self._d
        self._d = None; self.sumber._fr.clear()
        U1 = pd.Timestamp(ua) if ua else self.sumber.akhir_data()
        fr, idx, univ = self.sumber.muat(pd.Timestamp(lm) - self.T.PANAS, U1, 'AB')
        kum = ['A', 'B', 'AB'] if k == U.K_AKHIR else ['A', 'B']
        self._d = dict(fr=fr, idx=idx, U0=pd.Timestamp(um), U1=U1, kum=kum,
                       tp={g: self.sumber.topeng(fr, univ, g) for g in kum})
        self._k = k
        return self._d

    def pasaran(self, k, g, um, ua, lm):
        if k in self._pasaran: return self._pasaran[k]
        f = os.path.join(CACHE_G, f'tutup_k{k:02d}.parquet')
        if os.path.exists(f):
            W = pd.read_parquet(f)
            U1 = W.index.max() if ua is None else pd.Timestamp(ua)
        else:
            d = self._muat(k, lm, um, ua); t0 = d['U0'] - pd.Timedelta(days=10); U1 = d['U1']
            W = pd.DataFrame({t: x.close[x.index >= t0] for t, x in d['fr'].items()}).sort_index().astype('float64')
            W.columns = W.columns.astype(str)
            W.to_parquet(f)
        fr = {t: pd.DataFrame({'close': W[t].dropna()}) for t in W.columns}
        p = self.E.Pasaran({t: x for t, x in fr.items() if len(x)}, pd.Timestamp(um), U1)
        self._pasaran[k] = p
        return p

    def modul(self, kid):
        if kid not in self._mod: self._mod[kid] = self.T.muat_kaedah(kid)
        return self._mod[kid]

    def dagangan(self, kid, k, g, Pm, lm, um, ua):
        f = self._laluan(kid, k, g, Pm)
        if os.path.exists(f): return pd.read_parquet(f)
        d = self._muat(k, lm, um, ua)
        m = self.modul(kid)
        Pp = dict(m.PARAM); Pp.update(Pm or {})
        fr = self.T.salin(d['fr']); m.sedia(fr, d['idx'], Pp)
        tmax = Pp['tmax'] if 'tmax' in Pp else m.TMAX
        S = self.E.Susun(fr)
        out = None
        for gg in d['kum']:
            T = S.dengan_topeng(d['tp'][gg]).dagangan(tmax, m.WARM, d['U0'], d['U1'])
            T = T[['ticker', 'sig', 'ent', 'ex', 'ret', 'days', 'why', 'rank']].copy()
            for c in ('sig', 'ent', 'ex'): T[c] = pd.to_datetime(T[c])
            T['ticker'] = T.ticker.astype(str); T['rank'] = T['rank'].astype(float)
            T.to_parquet(self._laluan(kid, k, gg, Pm))
            if gg == g: out = T
        del fr
        return out


class Penilai:
    """Pulangan harian gabungan bagi set kaedah atas satu bahagian ('A' = k0–11 A, 'B' = k0–11 B, 'K' = k12 AB)."""
    def __init__(self, semua_kaj, penjana, proses=1):
        self.kaj = semua_kaj; self.pj = penjana; self._T = {}; self.proses = proses; self.gagal = {}

    def _bahagian(self, b):
        return [(k, b) for k in U.K_WFO] if b in ('A', 'B') else [(U.K_AKHIR, 'AB')]

    def dagangan(self, kid, k, g):
        kk = (kid, k, g)
        if kk not in self._T:
            d = self.kaj[kid][k]
            lm, um, ua = tetingkap_kajian(d, k)
            self._T[kk] = persentil(self.pj.dagangan(kid, k, g, P.param(d), lm, um, ua))
        return self._T[kk]

    def pulangan(self, ids, b):
        out = []
        for k, g in self._bahagian(b):
            d = self.kaj[ids[0]][k]
            lm, um, ua = tetingkap_kajian(d, k)
            ps = self.pj.pasaran(k, g, um, ua, lm)
            T = kongsi([self.dagangan(i, k, g) for i in ids])
            out.append(self.pj.E.pulangan_harian(ps.lengkung(T)))
        return U.sambung(out)

    def sediakan(self, ids, b):
        """Jana (dan cache) semua dagangan bagi ids, kajian demi kajian (data dimuat sekali setiap kajian).
        proses > 1: kaedah dijana selari dalam proses fork (data dikongsi). Kaedah yang gagal direkod dalam
        self.gagal dan dikeluarkan daripada calon. Pulang senarai ids yang berjaya."""
        for k, g in self._bahagian(b):
            ok = [i for i in ids if i not in self.gagal]
            if not ok: break
            lm, um, ua = tetingkap_kajian(self.kaj[ok[0]][k], k)
            tugas = []
            for i in ok:
                d = self.kaj[i][k]; l2, u2, a2 = tetingkap_kajian(d, k)
                if not os.path.exists(self.pj._laluan(i, k, g, P.param(d))): tugas.append((i, k, g, P.param(d), l2, u2, a2))
            if tugas and self.proses > 1 and len(tugas) > 1:
                self.pj._muat(k, lm, um, ua)
                global _PJ
                _PJ = self.pj
                from multiprocessing import get_context
                with get_context('fork').Pool(min(self.proses, len(tugas)), maxtasksperchild=4) as pool:
                    for i, e in pool.imap_unordered(_kerja, tugas):
                        if e: self.gagal[i] = e
            for i in ok:
                if i in self.gagal: continue
                try: self.dagangan(i, k, g)
                except Exception as e: self.gagal[i] = f'k{k:02d}: {type(e).__name__}: {e}'[:300]
            self.pj.pasaran(k, g, um, ua, lm)
        return [i for i in ids if i not in self.gagal]


_PJ = None


def _kerja(t):
    i, k, g, Pm, lm, um, ua = t
    try:
        _PJ.dagangan(i, k, g, Pm, lm, um, ua); return i, None
    except Exception as e:
        return i, f'k{k:02d}: {type(e).__name__}: {e}'[:300]


def _metrik(r, spy):
    return U.bersih(dict(cagr=U.cagr(r), mdd=U.mdd(r), spy=P.spy_cagr(spy, r.index),
                         mula=r.index[0].strftime('%Y-%m-%d') if len(r) else None,
                         akhir=r.index[-1].strftime('%Y-%m-%d') if len(r) else None, hari=len(r)), 4)


def jalan(csv=None, tala=None, keluar=None, data_dir=None, maks=MAKS, penjana=None, spy=None, proses=1):
    keluar = keluar or U.HASIL; tala = tala or U.TALA
    df = pd.read_csv(csv or os.path.join(keluar, 'parameter_sedia.csv'))
    calon_df = df[df.label.isin(['TINGGI', 'SEDERHANA'])].sort_values('cagr_a', ascending=False)
    calon = calon_df.kaedah.tolist()
    terbaik3 = U.bersih(df[~df.label.isin(U.BUKAN_CALON)].sort_values('cagr_a', ascending=False).head(3)[
        ['kaedah', 'label', 'cagr_a', 'mdd_a', 'cagr_b', 'cagr_kunci']].to_dict('records'), 4)
    hasil = dict(dijana=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%dT%H:%MZ'), calon=calon,
                 had=dict(maks=maks, korelasi=HAD_KOR, mdd=U.HAD_MDD), terbaik3_oos_a=terbaik3)
    if not calon:
        hasil.update(terpilih=[], log=[], penjelasan='Tiada kaedah TINGGI atau SEDERHANA; portfolio gabungan tidak dibina. '
                     'Tiga kaedah terbaik ikut CAGR OOS-A disenaraikan sebagai rujukan sahaja.')
        U.tulis_json(os.path.join(keluar, 'gabungan.json'), hasil)
        return hasil
    kaj = {k: U.baca_kajian(k, os.path.join(tala, k)) for k in calon}
    rA = {k: P.oos(kaj[k], 'A') for k in calon}
    if spy is None: spy = P.muat_spy(data_dir)
    pj = penjana or Penjana(data_dir)
    pn = Penilai(kaj, pj, proses)
    t0 = time.time()
    calon = pn.sediakan(calon, 'A')
    hasil['gagal_jana'] = dict(pn.gagal)
    print(f'gabungan: dagangan OOS-A {len(calon)} calon siap, {len(pn.gagal)} gagal ({time.time() - t0:.0f} s)')
    if not calon:
        hasil.update(terpilih=[], log=[], penjelasan='Jana semula dagangan gagal bagi semua calon; lihat gagal_jana.')
        U.tulis_json(os.path.join(keluar, 'gabungan.json'), U.bersih(hasil))
        return hasil
    # semakan: gabungan satu kaedah mesti sama dengan OOS-A JSON kaedah itu
    semak = {}
    for k in calon[:3]:
        r1 = pn.pulangan([k], 'A')
        x = pd.concat([r1, rA[k]], axis=1, join='inner').dropna()
        semak[k] = dict(beza_maks=float((x.iloc[:, 0] - x.iloc[:, 1]).abs().max()) if len(x) else None,
                        hari_jana=len(r1), hari_json=len(rA[k]))
    cache_n = {}

    def nilai_fn(ids):
        key = tuple(ids)
        if key not in cache_n:
            r = pn.pulangan(ids, 'A'); cache_n[key] = (U.cagr(r), U.mdd(r))
        return cache_n[key]

    pilih, log, _ = pilih_tamak(calon, rA, nilai_fn, maks=maks)
    print(f'gabungan: terpilih {pilih} ({time.time() - t0:.0f} s)')
    gA = pn.pulangan(pilih, 'A')
    pB = pn.sediakan(pilih, 'B'); gB = pn.pulangan(pB, 'B') if pB == pilih else pd.Series(dtype=float)
    pK = pn.sediakan(pilih, 'K'); gK = pn.pulangan(pK, 'K') if pK == pilih else pd.Series(dtype=float)
    hasil['gagal_jana'] = dict(pn.gagal)
    sA = U.spy_pulangan(spy, gA.index); sK = U.spy_pulangan(spy, gK.index)
    hasil.update(
        terpilih=pilih, log=U.bersih(log, 4), semakan_satu_kaedah=U.bersih(semak, 8),
        metrik=dict(A=_metrik(gA, spy), B=_metrik(gB, spy), kunci=_metrik(gK, spy)),
        param_semasa={k: json.loads(df.set_index('kaedah').loc[k, 'param_semasa'] or '{}') for k in pilih},
        param_akhir={k: json.loads(df.set_index('kaedah').loc[k, 'param_akhir'] or '{}') for k in pilih},
        param_semasa_penuh={k: P.param_penuh(kaj[k].get(U.K_SEMASA, {})) for k in pilih},
        ekuiti_bulanan=dict(A=U.ekuiti_bulanan(gA), B=U.ekuiti_bulanan(gB), kunci=U.ekuiti_bulanan(gK),
                            spy_A=U.ekuiti_bulanan(sA), spy_kunci=U.ekuiti_bulanan(sK)),
        masa_s=round(time.time() - t0))
    U.tulis_json(os.path.join(keluar, 'gabungan.json'), U.bersih(hasil))
    return hasil


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--maks', type=int, default=MAKS); ap.add_argument('--data', default=None)
    ap.add_argument('--keluar', default=None); ap.add_argument('--tala', default=None)
    ap.add_argument('--proses', type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    h = jalan(tala=a.tala, keluar=a.keluar, data_dir=a.data, maks=a.maks, proses=a.proses)
    if not h['terpilih']:
        print('gabungan: ' + h['penjelasan']); return
    m = h['metrik']
    for b in ('A', 'B', 'kunci'):
        print(f"  {b:5s} CAGR {m[b]['cagr']} MDD {m[b]['mdd']} SPY {m[b]['spy']}")
    print('  semakan satu kaedah: ' + ', '.join(f"{k} {v['beza_maks']}" for k, v in h['semakan_satu_kaedah'].items()))


if __name__ == '__main__':
    main()
