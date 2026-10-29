"""Pembinaan portfolio TANPA pemicu — pradaftar `REVERSE/SPEC_PEMBINAAN.md`.

Masuk adalah RAWAK dengan sengaja: itu menetapkan kelebihan pemicu kepada tepat sifar supaya
hanya PEMBINAAN yang diukur. Grid tetap 6 konfigurasi x 20 benih; peraturan keputusan ditetapkan
dalam spec sebelum larian ini dijalankan.

Guna: python3 REVERSE/pembinaan.py [--benih 20] [--laporan-sahaja]
Output: REVERSE/PEMBINAAN.md, REVERSE/pembinaan.csv
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import kos as K  # noqa: E402

CACHE = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'
KELUAR = AKAR / 'REVERSE'
SPUS = AKAR / 'BacktestShariah2' / 'data' / 'penanda_aras' / 'spus_bulanan.csv'

TH0, TH1 = 2012, 2025          # tempoh penuh
UJI0, UJI1 = '2020-01-01', '2025-12-31'   # tempoh keputusan (SPUS bermula Dis 2019)
CAIR = 100_000.0               # ambang kecairan repo (kod/tidak_layak.py)
ATR_N = 14
UFUK = 63                      # SPEC.md §2
HENTI_ATR = 2.0                # pul_henti2atr
TRAIL_ATR = 4.0               # Chandelier lorong 2
TRAIL_MAKS = 504               # had imbasan TRAIL (2 tahun); tanpa letupan masa
N_BENIH = 20                   # KEPEKATAN_BENIH.md: hingar pemilihan 17.3 mata/tahun

# Grid TETAP — spec §6. Jangan lebarkan.
GRID = [('A8', 8, 'H63S'), ('A40', 40, 'H63S'),
        ('B8', 8, 'H63'), ('B40', 40, 'H63'),
        ('C8', 8, 'TRAIL'), ('C40', 40, 'TRAIL')]


def atr_wilder(h, lo, c, n=ATR_N):
    pc = np.concatenate([[np.nan], c[:-1]])
    tr = np.maximum(h - lo, np.maximum(np.abs(h - pc), np.abs(lo - pc)))
    out = np.full(len(c), np.nan)
    if len(c) <= n:
        return out
    out[n] = np.nanmean(tr[1:n + 1])
    for i in range(n + 1, len(c)):
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


class Panel:
    """Matriks padat ticker x tarikh bagi seluruh alam, + ATR dan nilai dagangan 20 bar."""

    def __init__(self, th0=TH0, th1=TH1):
        bhg = []
        for y in range(th0 - 1, th1 + 2):
            p = CACHE / f'harga_{y}.parquet'
            if p.exists():
                bhg.append(pd.read_parquet(p, columns=['ticker', 'date', 'open', 'high', 'low',
                                                       'close', 'volume']))
        df = pd.concat(bhg, ignore_index=True)
        df = df[(df.date >= pd.Timestamp(f'{th0 - 1}-01-01')) &
                (df.date <= pd.Timestamp(f'{th1}-12-31'))]
        self.tarikh = np.array(sorted(df.date.unique()))
        self.tick = np.array(sorted(df.ticker.unique()))
        it = {t: i for i, t in enumerate(self.tick)}
        idt = {d: i for i, d in enumerate(self.tarikh)}
        n, m = len(self.tick), len(self.tarikh)
        self.O, self.H, self.L, self.C = (np.full((n, m), np.nan, 'float32') for _ in range(4))
        self.A = np.full((n, m), np.nan, 'float32')
        self.N = np.full((n, m), np.nan, 'float32')
        for t, g in df.groupby('ticker', sort=False):
            i = it[t]
            g = g.sort_values('date')
            j = np.array([idt[d] for d in g.date])
            o, h, lo, c = (g[x].to_numpy('float64') for x in ('open', 'high', 'low', 'close'))
            v = g.volume.to_numpy('float64')
            self.O[i, j], self.H[i, j], self.L[i, j], self.C[i, j] = o, h, lo, c
            self.A[i, j] = atr_wilder(h, lo, c)
            self.N[i, j] = pd.Series(c * v).rolling(20).median().to_numpy()
        self.th = pd.DatetimeIndex(self.tarikh).year

    def sauh(self, th0=TH0, th1=TH1):
        """Indeks bar terakhir setiap bulan kalendar dalam [th0, th1]."""
        bl = pd.DatetimeIndex(self.tarikh).to_period('M')
        out = []
        for b in pd.unique(bl):
            if th0 <= b.year <= th1:
                ii = np.flatnonzero(bl == b)
                out.append(int(ii[-1]))
        return out

    def layak(self, a):
        """Indeks ticker yang layak dimasuki pada sauh a (masuk pada buka a+1)."""
        if a + 1 >= len(self.tarikh):
            return np.array([], int)
        ok = (np.isfinite(self.C[:, a]) & np.isfinite(self.A[:, a]) &
              np.isfinite(self.N[:, a]) & (self.N[:, a] >= CAIR) &
              np.isfinite(self.O[:, a + 1]) & (self.O[:, a + 1] > 0))
        return np.flatnonzero(ok)


def keluar(P, ti, a, rule, cache):
    """(indeks_keluar, harga_masuk, harga_keluar) bagi satu (ticker, sauh, peraturan).

    Masuk pada buka a+1. Syarat dinilai pada bar tutup; keluar pada buka hari BERIKUTNYA
    (spec §5) — itu mengambil jurang terhadap kita, bukan memihak kepada kita.
    """
    kunci = (ti, a, rule)
    if kunci in cache:
        return cache[kunci]
    e = a + 1
    m = len(P.tarikh)
    masuk = float(P.O[ti, e])
    atr = float(P.A[ti, a])
    akhir = m - 1

    def harga_pada(k):
        """Buka pada k jika ada, jika tidak tutup bar sah terakhir."""
        if k <= akhir and np.isfinite(P.O[ti, k]) and P.O[ti, k] > 0:
            return int(k), float(P.O[ti, k])
        sah = np.flatnonzero(np.isfinite(P.C[ti, e:akhir + 1]))
        k2 = e + int(sah[-1]) if sah.size else e
        return k2, float(P.C[ti, k2])

    if rule == 'H63':
        k, px = harga_pada(min(e + UFUK + 1, akhir))
    elif rule == 'H63S':
        hi = min(e + UFUK, akhir)
        paras = masuk - HENTI_ATR * atr
        w = P.L[ti, e:hi + 1]
        kena = np.flatnonzero(np.isfinite(w) & (w <= paras))
        bar = e + int(kena[0]) if kena.size else hi
        k, px = harga_pada(min(bar + 1, akhir))
    else:  # TRAIL — Chandelier 4xATR, tiada had ufuk (had imbasan TRAIL_MAKS)
        hi = min(e + TRAIL_MAKS, akhir)
        c = P.C[ti, e:hi + 1].astype('float64')
        sah = np.isfinite(c)
        cc = np.where(sah, c, -np.inf)
        puncak = np.maximum.accumulate(cc)
        cond = sah & (c < puncak - TRAIL_ATR * atr)
        kena = np.flatnonzero(cond)
        bar = e + int(kena[0]) if kena.size else hi
        k, px = harga_pada(min(bar + 1, akhir))
    hasil = (k, masuk, px)
    cache[kunci] = hasil
    return hasil


def simulasi(P, sauh, slot, rule, benih, cache):
    """Siri ekuiti harian bagi satu konfigurasi dan satu benih. Panjang sahaja, tiada leverage."""
    rng = np.random.default_rng(benih)
    pilih = {a: rng.permutation(P.layak(a)) for a in sauh}
    m = len(P.tarikh)
    mula = sauh[0] + 1
    tunai = 1.0
    buka = []          # (ti, unit, idx_keluar, px_keluar)
    ek = np.full(m, np.nan)
    prev = 1.0
    for d in range(mula, m):
        for p in [x for x in buka if x[2] == d]:
            tunai += p[1] * p[3] * (1 - K.kos_sisi(P.N[p[0], d]))
            buka.remove(p)
        if d - 1 in pilih:
            a = d - 1
            for ti in pilih[a]:
                if len(buka) >= slot:
                    break
                if any(x[0] == ti for x in buka):
                    continue
                px = float(P.O[ti, d])
                if not np.isfinite(px) or px <= 0:
                    continue
                belanja = min(prev / slot, tunai)
                if belanja <= 1e-12:
                    break
                kx, _, pkeluar = keluar(P, int(ti), a, rule, cache)
                if kx <= d:
                    continue
                unit = belanja * (1 - K.kos_sisi(P.N[ti, a])) / px
                tunai -= belanja
                buka.append((int(ti), unit, kx, pkeluar))
        nilai = tunai
        for ti, unit, _, _ in buka:
            c = P.C[ti, d]
            if np.isfinite(c):
                nilai += unit * float(c)
        ek[d] = prev = nilai
    return ek


def mdd(e):
    e = np.asarray(e, 'float64')
    e = e[np.isfinite(e)]
    if e.size < 2:
        return np.nan
    return float((e / np.maximum.accumulate(e) - 1).min() * 100)


def cagr(e, hari):
    e = np.asarray(e, 'float64')
    ok = np.isfinite(e)
    if ok.sum() < 2:
        return np.nan
    e = e[ok]
    n = hari[ok]
    th = (n[-1] - n[0]).days / 365.25
    return float(((e[-1] / e[0]) ** (1 / th) - 1) * 100) if th > 0 else np.nan


def penanda_aras():
    """(SPUS, SPY) sebagai (cagr, mdd) pada tempoh keputusan 2020-2025."""
    out = {}
    s = pd.read_csv(SPUS, comment='#')
    s['bulan'] = pd.PeriodIndex(s.bulan, freq='M')
    s = s[(s.bulan >= pd.Period('2020-01')) & (s.bulan <= pd.Period('2025-12'))]
    v = s.tutup.to_numpy('float64')
    th = (s.bulan.iloc[-1] - s.bulan.iloc[0]).n / 12.0
    out['SPUS'] = (float(((v[-1] / v[0]) ** (1 / th) - 1) * 100), mdd(v), 'tutup bulanan')
    # Konvensyen KEDUA: median pulangan/MDD setiap tahun. Itu yang direkod oleh
    # PENANDA_ARAS_SYARIAH.md dan KEPEKATAN.md (26.09% / -10.14%). Ia BUKAN CAGR dan lebih
    # tinggi kerana median membuang tahun terburuk (2022: -22.76%). Kedua-duanya betul;
    # mencampurkannya tidak.
    s2 = pd.read_csv(SPUS, comment='#')
    s2['bulan'] = pd.PeriodIndex(s2.bulan, freq='M')
    pt, mt = [], []
    for y in range(2020, 2026):
        q = s2[(s2.bulan >= pd.Period(f'{y - 1}-12')) &
               (s2.bulan <= pd.Period(f'{y}-12'))].tutup.to_numpy('float64')
        if len(q) >= 3:
            pt.append((q[-1] / q[0] - 1) * 100)
            mt.append(mdd(q))
    out['SPUS_median_tahunan'] = (float(np.median(pt)), float(np.median(mt)), 'median setiap tahun')
    ix = pd.read_parquet(CACHE / 'idx.parquet')
    q = ix[ix.ticker == 'SPY'].sort_values('date')
    q = q[(q.date >= pd.Timestamp(UJI0)) & (q.date <= pd.Timestamp(UJI1))]
    out['SPY'] = (cagr(q.close.to_numpy('float64'), pd.DatetimeIndex(q.date)),
                  mdd(q.close.to_numpy('float64')), 'tutup harian')
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', type=int, default=N_BENIH)
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = KELUAR / 'pembinaan.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f))

    print('membina panel...', flush=True)
    P = Panel()
    sauh = P.sauh()
    print(f'  {len(P.tick):,} ticker x {len(P.tarikh):,} sesi, {len(sauh)} sauh bulanan',
          flush=True)
    hari = pd.DatetimeIndex(P.tarikh)
    m0 = int(np.searchsorted(P.tarikh, np.datetime64(UJI0)))
    cache = {}
    baris = []
    for nama, slot, rule in GRID:
        for b in range(1, a.benih + 1):
            ek = simulasi(P, sauh, slot, rule, b, cache)
            ek2 = ek[m0:]
            baris.append(dict(konfig=nama, slot=slot, keluar=rule, benih=b,
                              pul_14th=cagr(ek, hari), mdd_14th=mdd(ek),
                              pul_uji=cagr(ek2, hari[m0:]), mdd_uji=mdd(ek2)))
        print(f'  {nama}: {a.benih} benih siap', flush=True)
    R = pd.DataFrame(baris)
    R.to_csv(f, index=False, float_format='%.4f')
    return laporan(R)


def laporan(R):
    pa = penanda_aras()
    sp_pul, sp_mdd, sp_nota = pa['SPUS']
    g = R.groupby(['konfig', 'slot', 'keluar']).agg(
        pul=('pul_uji', 'median'), p10=('pul_uji', lambda x: x.quantile(0.10)),
        p90=('pul_uji', lambda x: x.quantile(0.90)), md=('mdd_uji', 'median'),
        pul14=('pul_14th', 'median'), md14=('mdd_14th', 'median'),
        n=('benih', 'size')).reset_index()
    # Peraturan keputusan spec §10 — ketiga-tiga syarat, tiada yang lain.
    g['s1_pulangan'] = g.pul > sp_pul
    g['s2_mdd'] = g.md > sp_mdd
    g['s3_p10'] = g.p10 > sp_pul
    g['lulus'] = g.s1_pulangan & g.s2_mdd & g.s3_p10
    lulus = g[g.lulus]

    L = ['# Pembinaan portfolio tanpa pemicu: keputusan', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/pembinaan.py`. Pradaftar: `REVERSE/SPEC_PEMBINAAN.md` '
             '(dikomit sebelum larian ini).')
    L.append('')
    L.append(f'## Keputusan: **{"DITERIMA" if len(lulus) else "DITOLAK"}**')
    L.append('')
    L.append(f'Tempoh keputusan {UJI0[:4]}–{UJI1[:4]} lawan **SPUS: {sp_pul:.2f}%/tahun, '
             f'MDD {sp_mdd:.2f}%** ({sp_nota}). SPY rujukan sahaja: '
             f'{pa["SPY"][0]:.2f}%/tahun, MDD {pa["SPY"][1]:.2f}%.')
    L.append('')
    L.append(f'Masuk **rawak** (tiada pemicu), {int(g.n.iloc[0])} benih setiap konfigurasi, '
             'kos penuh. Penanda aras tanpa kos.')
    L.append('')
    L.append('| Konfig | Slot | Keluar | Pulangan median | p10 | p90 | MDD median | '
             'S1 pul | S2 mdd | S3 p10 | LULUS |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for _, r in g.iterrows():
        tk = {True: 'ya', False: 'tidak'}
        L.append(f'| `{r.konfig}` | {r.slot} | `{r.keluar}` | {r.pul:+.2f}% | {r.p10:+.2f}% | '
                 f'{r.p90:+.2f}% | {r.md:.2f}% | {tk[r.s1_pulangan]} | {tk[r.s2_mdd]} | '
                 f'{tk[r.s3_p10]} | {"**YA**" if r.lulus else "tidak"} |')
    L.append(f'| **SPUS** | — | beli-pegang | **{sp_pul:+.2f}%** | — | — | **{sp_mdd:.2f}%** | '
             '— | — | — | — |')
    L.append('')
    mp, mm, _ = pa['SPUS_median_tahunan']
    bp = float(g.pul.max())
    bm = float(g.md.max())
    L.append('### Dua konvensyen SPUS — keputusan bertahan pada kedua-duanya')
    L.append('')
    L.append(f'Repo ini merekod SPUS sebagai **{mp:.2f}%/tahun, MDD {mm:.2f}%** '
             '(`PENANDA_ARAS_SYARIAH.md`, `KEPEKATAN.md`) manakala ujian ini menggunakan '
             f'**{sp_pul:.2f}%/tahun, MDD {sp_mdd:.2f}%**. Kedua-duanya betul dan dari data '
             f'yang sama: {mp:.2f}% ialah **median pulangan setiap tahun** (konvensyen '
             f'median-setiap-tahun seluruh kajian) manakala {sp_pul:.2f}% ialah **CAGR seluruh '
             'tingkap**. Median lebih tinggi kerana ia membuang tahun terburuk (2022: −22.76%); '
             'CAGR ialah angka pengkompaunan yang sebenar. Ujian ini menggunakan CAGR bagi '
             'sistem DAN penanda aras, jadi perbandingannya setara.')
    L.append('')
    L.append(f'Keputusan tidak bergantung pada pilihan itu. Konfigurasi terbaik memberi '
             f'**{bp:+.2f}%** pulangan dan **{bm:.2f}%** MDD. Itu kalah kepada versi SPUS yang '
             f'paling memihak kepada sistem pada kedua-dua paksi: pulangan SPUS terendah '
             f'({sp_pul:.2f}%) masih lebih tinggi, dan MDD SPUS terdalam ({sp_mdd:.2f}%) masih '
             'lebih cetek. Tiada gabungan konvensyen menukar keputusan.')
    L.append('')
    L.append('`S1` pulangan median > SPUS · `S2` MDD lebih cetek daripada SPUS · `S3` **p10** '
             'masih > SPUS. Spec §10 memerlukan **ketiga-tiga**. S3 ialah syarat yang menghalang '
             'konfigurasi bertuah kelihatan seperti dapatan.')
    L.append('')
    return laporan2(L, g, R, lulus, sp_pul, sp_mdd)


def laporan2(L, g, R, lulus, sp_pul, sp_mdd):
    """Bahagian tafsiran — dipisahkan supaya laporan() kekal boleh dibaca."""
    a8 = g[g.konfig == 'A8'].iloc[0]
    L.append('## Apa yang setiap lajur grid ubah')
    L.append('')
    L.append(f'`A8` ialah pembinaan kajian sendiri dengan pemicu dibuang: '
             f'{a8.pul:+.2f}%/tahun, MDD {a8.md:.2f}%. Setiap konfigurasi lain berbeza '
             'daripadanya pada SATU paksi sahaja (slot, atau henti, atau kedua-duanya).')
    L.append('')
    for paksi, kiri, kanan in (('Slot 8 → 40 (henti kekal)', 'A8', 'A40'),
                               ('Buang henti keras (8 slot)', 'A8', 'B8'),
                               ('Terima ekor: TRAIL (8 slot)', 'A8', 'C8'),
                               ('Kedua-dua: 40 slot + TRAIL', 'A8', 'C40')):
        x, y = g[g.konfig == kiri].iloc[0], g[g.konfig == kanan].iloc[0]
        L.append(f'- **{paksi}**: pulangan {y.pul - x.pul:+.2f} mata, '
                 f'MDD {y.md - x.md:+.2f} mata (`{kiri}`→`{kanan}`)')
    L.append('')
    L.append('## Hingar pemilihan')
    L.append('')
    sb = R.groupby('konfig').pul_uji.agg(['std', 'min', 'max'])
    sebaran = ', '.join(f'`{k}` {v:.1f} mata'
                        for k, v in zip(g.konfig, (g.p90 - g.p10)))
    L.append(f'Sebaran p90−p10 merentas benih: {sebaran}.')
    L.append('')
    L.append(f'Julat penuh 20 benih bagi `A8`: {sb.loc["A8", "min"]:+.2f}% hingga '
             f'{sb.loc["A8", "max"]:+.2f}% (sisihan piawai {sb.loc["A8", "std"]:.2f} mata). '
             'Itulah sebabnya syarat `S3` ada: satu larian tunggal boleh mendarat di mana-mana '
             'dalam julat itu, dan melaporkan larian terbaik sebagai prestasi sistem adalah '
             'kesilapan yang sama yang dibetulkan oleh `KEPEKATAN_BENIH.md`.')
    L.append('')
    L.append('## Tafsiran')
    L.append('')
    if len(lulus):
        L.append(f'**{len(lulus)} konfigurasi memenuhi ketiga-tiga syarat:** '
                 f'{", ".join("`" + x + "`" for x in lulus.konfig)}. '
                 '**Jangkaan priori saya dalam spec §11 ialah DITOLAK, dan ia SALAH.**')
        L.append('')
        L.append('Itu bermakna pembinaan portfolio sahaja — tanpa pemicu sama sekali — '
                 'mengalahkan penanda aras pasif patuh Syariah pada kedua-dua paksi dalam '
                 'simulasi ini, dan jurangnya bertahan pada p10.')
        L.append('')
        L.append('**Ia tetap backtest.** Ia mesti disahkan ke hadapan sebelum dipercayai: '
                 'jalankan sebagai lorong `portfolio_slot/` dengan jalur benih, bukan sebagai '
                 'dakwaan.')
    else:
        L.append('**Tiada konfigurasi memenuhi ketiga-tiga syarat.** Jangkaan priori dalam '
                 'spec §11 ialah DITOLAK dan ia tepat.')
        L.append('')
        kalah = []
        if not g.s1_pulangan.any():
            kalah.append('pulangan (S1) gagal pada SETIAP konfigurasi')
        if not g.s2_mdd.any():
            kalah.append('MDD (S2) gagal pada SETIAP konfigurasi')
        both = g[g.s1_pulangan & g.s2_mdd]
        if len(both) and not both.s3_p10.any():
            kalah.append('ada konfigurasi melepasi pulangan dan MDD tetapi gagal p10 (S3) — '
                         'iaitu dalam hingar pemilihan, bukan dapatan')
        L.append(('Sebabnya: ' + '; '.join(kalah) + '.') if kalah
                 else 'Kegagalan tersebar antara syarat.')
        L.append('')
        L.append('Maksudnya ruang **pembinaan** kini juga diukur. Ruang **pemicu** sudah '
                 'diukur dan kosong (fasa 1, 1b, 2 SEC). Kedua-dua paksi yang ada pada kita '
                 'telah diukur terhadap penanda aras yang betul, dan kedua-duanya tidak '
                 'mengalahkannya.')
        L.append('')
        L.append('Kesimpulan jujur: **memegang SPUS mengalahkan apa-apa yang kajian ini boleh '
                 'bina daripada alam ini.** Itu bukan kegagalan pelaksanaan; ia hasil yang '
                 'diukur enam kali dengan cara berbeza.')
        L.append('')
        c40 = g[g.konfig == 'C40'].iloc[0]
        a8b = g[g.konfig == 'A8'].iloc[0]
        L.append('### Tetapi satu sebab priori saya SALAH, dan ia penting')
        L.append('')
        L.append('Spec §11 sebab 2 menjangka nisbah tidak akan bertambah baik, bersandarkan '
                 '`KEPEKATAN.md` yang mendapati 8→60 slot memperbaiki MDD 3.48 mata tetapi '
                 '**mengorbankan pulangan 5.97 mata**. Hasil di sini bertentangan: setiap '
                 'perubahan pembinaan memperbaiki **kedua-dua** paksi secara monoton, dan '
                 f'`A8`→`C40` memberi pulangan **{c40.pul - a8b.pul:+.2f} mata** DAN MDD '
                 f'**{c40.md - a8b.md:+.2f} mata** (lebih cetek) serentak.')
        L.append('')
        L.append('Sebab kedua-dua dokumen boleh betul: populasinya berbeza. `KEPEKATAN.md` '
                 'menambah slot pada entri yang **dipilih** (susunan abjad daripada peristiwa '
                 'sah SEC), jadi slot tambahan mencairkan subset yang sudah terpilih. Di sini '
                 'entri **rawak**, jadi slot tambahan hanya mengurangkan varians sampel tanpa '
                 'apa-apa untuk dicairkan. Itu bukan percanggahan; ia memberitahu bahawa '
                 'kenaikan pembinaan bergantung pada apa yang ia dikenakan ke atas.')
        L.append('')
        L.append(f'Jadi paksi pembinaan **memang** mengandungi kenaikan sebenar — kira-kira '
                 f'{c40.pul - a8b.pul:.1f} mata pulangan dan {c40.md - a8b.md:.1f} mata MDD '
                 f'daripada pembinaan sahaja, yang lebih besar daripada apa-apa yang mana-mana '
                 'pemicu dalam fasa 1/1b/2 pernah hasilkan. Ia tetap tidak cukup: ia bermula '
                 f'dari {a8b.pul:.2f}% dan berakhir pada {c40.pul:.2f}%, sedangkan SPUS '
                 f'{sp_pul:.2f}%. Kenaikan itu nyata tetapi jurangnya lebih besar.')
        L.append('')
        L.append('**Implikasi yang perlu dinyatakan:** jika kerja selepas ini dibuat juga, '
                 'arahnya ialah pembinaan (slot lebih banyak, tiada henti keras, biarkan '
                 'pemenang berjalan), **bukan** pemicu. Tetapi destinasinya tetap di bawah '
                 'memegang SPUS, jadi yang rasional ialah berhenti membina dan bandingkan '
                 'jejak hadapan dengan SPUS.')
    L.append('')
    L.append('## Had')
    L.append('')
    L.append('- Backtest, bukan jejak hadapan. Semua kaveat `KEPEKATAN_BENIH.md` terpakai.')
    L.append('- MDD SPUS daripada tutup **bulanan** (data yang ada), jadi ia lebih cetek '
             'daripada MDD harian yang benar. Itu memihak kepada SPUS — ia menjadikan syarat '
             '`S2` lebih sukar, bukan lebih mudah.')
    L.append('- Alam A02 **bukan** ditapis Syariah; SPUS ditapis. Perbandingan itu tidak '
             'setara pada paksi tapisan, dan tapisan Syariah membuang semua kewangan.')
    L.append('- Siri ekuiti tempoh keputusan dihiris daripada larian 14 tahun dan '
             'dinormalkan semula, jadi posisi yang terbuka pada sempadan 2020 diwarisi.')
    L.append('- Tunai tidak berbunga (0%), yang merugikan sistem berbanding realiti.')
    L.append('- `TRAIL` diimbas maksimum 504 sesi; jika Chandelier tidak tercetus, posisi '
             'ditutup pada hujung tingkap itu.')
    L.append('')
    L.append('**Ia tidak mencapai +10%/bulan dan tidak pernah boleh.** Lihat `SASARAN.md`.')
    L.append('')
    (KELUAR / 'PEMBINAAN.md').write_text('\n'.join(L), encoding='utf-8')
    print('\n' + g[['konfig', 'pul', 'p10', 'md', 'lulus']].round(2).to_string(index=False))
    print(f'\nSPUS {sp_pul:.2f}% / MDD {sp_mdd:.2f}% | '
          f'{"DITERIMA: " + ",".join(lulus.konfig) if len(lulus) else "DITOLAK"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
