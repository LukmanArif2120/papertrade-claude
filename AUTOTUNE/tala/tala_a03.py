# Sistem dan penala A03 (SPEC_A03 §2–§4). A01/A02 tidak berubah: A03 memakai enjin_at (pilihan had_rugi), tala_a02.tala
# (pilihan penilai/tambah) dan Penilai02 sebagai asas.
#   Sistem utama 'utama' = F (EPS suku terkini > 0 dan pertumbuhan tahun ke tahun >= 25%, titik masa) + M (SPY > SMA50
#   dan SMA50 > SMA200) + 5 slot × 20% + had rugi 8% (henti = maks(henti kaedah, 0.92 × harga masuk), berkuat kuasa
#   mulai hari masuk + 1). Ablasi (dilaporkan sahaja): 'f_sahaja', 'm_sahaja', 'tanpa' (tanpa F/M); kesemuanya 5 slot
#   dan had rugi 8% — hanya topeng F/M yang berbeza.
#   Topeng isyarat = universe/kumpulan (A02) ∧ F ∧ M pada hari isyarat.
# Guna: python3 tala_a03.py M54 had60 6 [--percubaan 120] [--cache AUTOTUNE/.cache_a02] [--fund AUTOTUNE/.cache_fund_a03]
import os, sys, json, glob, shutil, subprocess, argparse
import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import tala as T1
import tala_a02 as T2
from tala import E, O

AKAR = T1.AKAR
HASIL = os.path.join(AKAR, 'AUTOTUNE', 'hasil_a03')
KELUAR = os.path.join(HASIL, 'tala')
CACHE = T2.CACHE
CACHE_F = 'AUTOTUNE/.cache_fund_a03'
TAG_F = 'autotune-fundamental-a03'
REPO = 'pedagangsenja/papertrade-claude'
DIR_FUND = os.path.join(AKAR, 'AUTOTUNE', 'fundamental')
SLOT, W, HAD_RUGI, AMBANG = 5, 0.20, 0.08, 0.25
SISTEM = {'utama': (True, True), 'f_sahaja': (True, False), 'm_sahaja': (False, True), 'tanpa': (False, False)}
UTAMA = 'utama'
ABLASI = ('f_sahaja', 'm_sahaja', 'tanpa')
PAKAR = ['M06', 'M28', 'M35', 'M37', 'M38', 'M44', 'M51', 'M54', 'M64', 'M66', 'M74', 'M87', 'M88', 'M104']
N_LAIN = 6
N_TALA = 10
SARINGAN_A02 = os.path.join(AKAR, 'AUTOTUNE', 'hasil_a02', 'saringan.csv')


def kaedah_lain(csv=SARINGAN_A02, n=N_LAIN, kecuali=PAKAR):
    """n kaedah teratas saringan A02 lorong 'asal' ikut min(lebihan_A, lebihan_B), selain kaedah pakar (SPEC_A03 §3)."""
    D = pd.read_csv(csv)
    d = D[(D.lorong == 'asal') & (D.status == 'SIAP') & ~D.kaedah.isin(kecuali)].copy()
    d['_m'] = d[['lebihan_A', 'lebihan_B']].min(axis=1)
    d = d.dropna(subset=['_m']).sort_values(['_m', 'kaedah'], ascending=[False, True])
    return d.kaedah.head(n).tolist()


def senarai_kaedah(csv=SARINGAN_A02):
    return list(PAKAR) + kaedah_lain(csv)


# ---------- fundamental ----------
def _ciri():
    if DIR_FUND not in sys.path: sys.path.insert(0, DIR_FUND)
    try:
        import ciri
        return ciri
    except ImportError:
        return None


def ambil_fundamental(cache=CACHE_F, tag=TAG_F):
    """Direktori aset Release fundamental A03 (dimuat turun sekali). Guna ciri.ambil jika ada."""
    c = _ciri()
    for nama in ('ambil', 'ambil_eps'):
        if c is not None and hasattr(c, nama):
            try: return str(getattr(c, nama)(cache))
            except TypeError: return str(getattr(c, nama)())
    d = cache if os.path.isabs(cache) else os.path.join(AKAR, cache)
    os.makedirs(d, exist_ok=True)
    try:  # cache tidak dicommit
        with open(os.path.join(d, '.gitignore'), 'w') as fh: fh.write('*\n')
    except OSError: pass
    if not [f for f in os.listdir(d) if not f.startswith('.')]:
        if shutil.which('gh') and os.environ.get('GH_TOKEN'):
            subprocess.run(['gh', 'release', 'download', tag, '-R', REPO, '-D', d, '--clobber'], check=False)
        if not [f for f in os.listdir(d) if not f.startswith('.')]:
            import data
            rel = data._url_json(f'https://api.github.com/repos/{REPO}/releases/tags/{tag}')
            for a in rel['assets']: data._url_simpan(a['browser_download_url'], os.path.join(d, a['name']))
    return d


def muat_eps(dir_=None):
    """Jadual EPS (format ciri.py). ciri.muat_eps/muat jika ada; jika tidak, semua parquet/csv dalam dir_."""
    c = _ciri()
    for nama in ('muat_eps', 'muat'):
        if c is not None and hasattr(c, nama):
            try: return getattr(c, nama)(dir_)
            except TypeError: return getattr(c, nama)()
    fs = sorted(glob.glob(os.path.join(dir_, '*.parquet'))) or sorted(glob.glob(os.path.join(dir_, '*.csv*')))
    if not fs: raise RuntimeError(f'tiada data EPS dalam {dir_}')
    return pd.concat([pd.read_parquet(f) if f.endswith('.parquet') else pd.read_csv(f) for f in fs], ignore_index=True)


def lajur_f(fr, eps, ambang=AMBANG):
    """ticker -> bool Series titik masa (ciri.lajur_f). eps None → semua True (pengganti ujian sahaja)."""
    if eps is None: return {t: pd.Series(True, index=g.index) for t, g in fr.items()}
    c = _ciri()
    if c is None: raise RuntimeError('AUTOTUNE/fundamental/ciri.py tiada')
    return c.lajur_f(fr, eps, ambang)


def siri_m(idx):
    """M (SPEC_A03 §2): tutup SPY > SMA50 dan SMA50 > SMA200 (data <= hari itu sahaja). Bool Series ikut tarikh SPY."""
    c = idx['SPY']['close'].astype(float)
    s50, s200 = c.rolling(50).mean(), c.rolling(200).mean()
    return ((c > s50) & (s50 > s200)).fillna(False)


def topeng_m(fr, idx):
    m = siri_m(idx)
    return {t: m.reindex(g.index, method='ffill').fillna(False).astype(bool) for t, g in fr.items()}


# ---------- statistik dagangan dan objektif (SPEC_A03 §6) ----------
MENANG_LATIH_MIN = 0.50     # kekangan tambahan tala: kadar menang dagangan dipegang (latih) >= 50%


def statistik(T):
    """Jumlah asas daripada dagangan dipegang: n_menang (ret > 0), n_kalah (ret <= 0), jumlah_untung, jumlah_rugi (positif)."""
    r = pd.Series(getattr(T, 'ret', []), dtype=float).dropna() if T is not None and len(T) else pd.Series(dtype=float)
    return dict(n_menang=int((r > 0).sum()), n_kalah=int((r <= 0).sum()),
                jumlah_untung=float(r[r > 0].sum()), jumlah_rugi=float(-r[r <= 0].sum()))


def terbitan(n_menang, n_kalah, jumlah_untung, jumlah_rugi):
    """kadar menang/kalah, purata untung/rugi setiap dagangan, jangkaan (purata pulangan dagangan), faktor untung."""
    n = n_menang + n_kalah
    if not n: return dict(n=0, menang=None, kalah=None, purata_untung=None, purata_rugi=None, jangkaan=None, pf=None)
    return dict(n=n, menang=n_menang / n, kalah=n_kalah / n,
                purata_untung=jumlah_untung / n_menang if n_menang else None,
                purata_rugi=-jumlah_rugi / n_kalah if n_kalah else None,
                jangkaan=(jumlah_untung - jumlah_rugi) / n,
                pf=(jumlah_untung / jumlah_rugi) if jumlah_rugi > 0 else (float('inf') if jumlah_untung > 0 else None))


def lulus_a03(m):
    """Kekangan SPEC_A02 §2 + kadar menang latih >= 50% (SPEC_A03 §6)."""
    return O.lulus_a02(m) and (m.get('win') or 0.0) >= MENANG_LATIH_MIN


def skor_a03(m):
    """Objektif = lebihan atas SPY (tidak berubah) jika lulus_a03; pelanggar: skor_a02 pelanggar (−1 + lebihan − 2 × lebihan
    MDD) tolak kekurangan kadar menang di bawah 50% (kecerunan untuk TPE)."""
    if lulus_a03(m): return float(m['lebihan'])
    return float(-1 + m['lebihan'] - 2 * max(0.0, (m['spy_mdd'] - O.MDD_LONGGAR_A02) - m['mdd'])
                 - max(0.0, MENANG_LATIH_MIN - (m.get('win') or 0.0)))


class Penilai03(T2.Penilai02):
    """Penilai02 + topeng F/M + had rugi + 5 slot × 20%. varian: kunci SISTEM (lalai 'utama')."""
    def __init__(self, m, fr, idx, univ, sumber, mula, akhir, kumpulan_list, eps=None, varian=UTAMA):
        super().__init__(m, fr, idx, univ, sumber, mula, akhir, kumpulan_list)
        self.eps, self.varian = eps, varian
        self._fm = {}

    def _bersambung(self, jenis, f):
        kira = lambda: E.topeng_bersambung(lajur_f(f, self.eps) if jenis == 'F' else topeng_m(f, self.idx), f)
        if f is not self.fr: return kira()          # sedia() mengubah set saham: kira semula (jarang)
        if jenis not in self._fm: self._fm[jenis] = kira()
        return self._fm[jenis]

    def topeng_fm(self, varian, f=None):
        """Tatasusunan bool bersambung (urutan f) bagi topeng F/M varian; None jika tiada topeng."""
        f = self.fr if f is None else f
        pf, pm = SISTEM[varian]; out = None
        for jenis, ya in (('F', pf), ('M', pm)):
            if ya:
                a = self._bersambung(jenis, f)
                out = a if out is None else (out & a)
        return out

    def jalan03(self, P, kumpulan_list=None, lorong_list=('had60',), varian_list=(UTAMA,), harian=False):
        """{(lorong, kumpulan, varian): (metrik_a02, pulangan_harian | None, dagangan_dipegang)}; sedia() sekali."""
        m = self.m; Pp = dict(m.PARAM); Pp.update(P or {})
        f = T1.salin(self.fr); m.sedia(f, self.idx, Pp)
        tmax = Pp['tmax'] if 'tmax' in Pp else m.TMAX
        sejajar = self.asas.sejajar(f)
        S = E.Susun(f, asas=self.asas if sejajar else None)
        asas_f = self.fr if sejajar else f
        out = {}
        for k in (kumpulan_list or list(self.tp)):
            tp = self.tp[k] if sejajar else E.topeng_bersambung(self.sumber.topeng(f, self.univ, k), f)
            for v in varian_list:
                fm = self.topeng_fm(v, asas_f)
                Sk = S.dengan_topeng(tp if fm is None else (tp & fm))
                for lo in lorong_list:
                    Tt = Sk.dagangan(tmax, m.WARM, self.mula, self.akhir, had60=E.had60_lorong(lo), had_rugi=HAD_RUGI)
                    cv, Tp = self.pasaran.lengkung(Tt, SLOT, W, pegang=True)
                    mt = O.ringkas_a02(Tp, cv, self.spy_cv); mt.update(statistik(Tp))
                    out[(lo, k, v)] = (mt, E.pulangan_harian(cv) if harian else None, Tp)
        return out

    def jalan02(self, P, kumpulan_list=None, lorong_list=('had60',), harian=False):
        """Antara muka Penilai02 (tala_a02.tala) bagi varian penilai ini."""
        r = self.jalan03(P, kumpulan_list, lorong_list, (self.varian,), harian)
        return {(lo, k): v for (lo, k, _), v in r.items()}


def kilang(eps, varian=UTAMA):
    return lambda m, fr, idx, univ, sumber, mula, akhir, kum: Penilai03(m, fr, idx, univ, sumber, mula, akhir, kum,
                                                                        eps=eps, varian=varian)


def keterangan_sistem(varian=UTAMA):
    pf, pm = SISTEM[varian]
    return dict(varian=varian, F=pf, M=pm, slot=SLOT, w=W, had_rugi=HAD_RUGI, ambang_eps=AMBANG)


def tala(mid, lorong, k, sumber, eps, n_trials=T2.PERCUBAAN, had_minit=T2.HAD_MINIT, tamat=None, keluar=KELUAR, tulis=True):
    return T2.tala(mid, lorong, k, sumber, n_trials, had_minit, tamat, keluar, tulis, penilai=kilang(eps, UTAMA),
                   tambah=dict(versi='A03', sistem=keterangan_sistem(UTAMA)), skor_fn=skor_a03, lulus_fn=lulus_a03)


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('kaedah'); a.add_argument('lorong', choices=T2.LORONG); a.add_argument('kajian', type=int)
    a.add_argument('--percubaan', type=int, default=T2.PERCUBAAN); a.add_argument('--had-minit', type=float, default=T2.HAD_MINIT)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', CACHE))
    a.add_argument('--fund', default=CACHE_F); a.add_argument('--keluar', default=KELUAR)
    x = a.parse_args(argv)
    eps = muat_eps(ambil_fundamental(x.fund))
    H = tala(x.kaedah, x.lorong, x.kajian, T1.Sumber(T2.ambil_data(x.cache)), eps, x.percubaan, x.had_minit, keluar=x.keluar)
    print(H['kaedah'], H['kajian'], H['status'], 'skor', H.get('skor'), 'masa', H['masa'].get('jumlah'), H['ralat'][:2])


if __name__ == '__main__':
    main()
