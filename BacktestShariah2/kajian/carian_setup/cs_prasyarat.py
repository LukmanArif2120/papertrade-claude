"""Carian setup — tinjauan PRASYARAT (SPEC pindaan 14 Nov 2026 (h)): isyarat yang BUKAN daripada harga saham itu
sendiri (pasaran, keluasan, sektor, industri, earnings, kalendar) lawan kadar saham "lari".
Guna: python3 cs_prasyarat.py <kerja>   (folder kerja CS02: panel_A/B, benih_A/B[_tala]).
Keluaran: hasil/PRASYARAT/LAPORAN.md dan prasyarat.csv. Maklumat sahaja; bukan pemilihan setup."""
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_hadapan as hadapan  # noqa: E402
import cs_lapor as lapor  # noqa: E402
import cs_tala as tala  # noqa: E402
import cs_tangkap as tk  # noqa: E402
import cs_teras as teras  # noqa: E402

BS2 = lapor.BS2
KUMP = {'A': 'A. Arah pasaran', 'B': 'B. Turun-naik pasaran', 'C': 'C. Keluasan pasaran', 'D': 'D. Sektor saham itu',
        'E': 'E. Industri saham itu', 'F': 'F. Earnings syarikat', 'G': 'G. Kalendar'}
PRASYARAT = [
    'A01 QQQ ON', 'A02 QQQ OFF', 'A03 SPY atas SMA200', 'A04 SPY bawah SMA200', 'A05 QQQ dalam 3% dari puncak 52 minggu',
    'A06 QQQ >= 10% di bawah puncak', 'A07 QQQ >= 20% di bawah puncak', 'A08 rejim ON baharu (<= 10 sesi)',
    'A09 rejim OFF baharu (<= 10 sesi)', 'A10 QQQ RSI14 < 35', 'A11 QQQ naik >= 3% dalam 5 sesi',
    'B01 turun-naik SPY 21 hari >= 25% setahun', 'B02 turun-naik SPY 21 hari <= 10% setahun',
    'B03 turun-naik SPY menurun (21 hari < 63 hari)',
    'C01 >= 60% saham di atas MA50', 'C02 <= 30% saham di atas MA50', 'C03 keluasan naik >= 10 mata dalam 10 sesi',
    'C04 >= 60% saham di atas MA200', 'C05 >= 15% saham dalam 5% dari puncak 52 minggu',
    'D01 sektor 3 teratas (pulangan 63 sesi)', 'D02 sektor 3 terbawah (pulangan 63 sesi)',
    'D03 >= 60% saham sektor di atas MA50',
    'E01 industri 20% teratas (pulangan 63 sesi)', 'E02 industri 20% teratas (pulangan 21 sesi)',
    'E03 industri 20% terbawah (pulangan 63 sesi)', 'E04 >= 60% saham industri di atas MA50',
    'E05 saham lain dalam industri sama naik >= 20% dalam 20 sesi',
    'F01 earnings dalam 1-5 sesi akan datang', 'F02 0-4 sesi selepas earnings', 'F03 5-19 sesi selepas earnings',
    'F04 tiada earnings dalam 20 sesi akan datang', 'F05 kejutan untung terkini positif (SUE > 0)',
    'F06 hasil suku terkini tumbuh >= 20%', 'F07 harga melompat >= 5% pada hari earnings (20 sesi lalu)',
    'G01 Nov-Apr', 'G02 Mei-Okt', 'G03 7 hari pertama bulan', 'G04 Januari',
]


def _rsi(s, n=14):
    d = s.diff()
    u = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    v = (-d).clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + u / v.replace(0, np.nan))


def pasaran(hu, keluasan, q=None, s=None):
    """dict nama -> Series bool berindeks tarikh (int). hu: tarikh tersusun; keluasan: DataFrame b50, b200, b5.
    q, s: tutup QQQ / SPY berindeks tarikh (int) -- pilihan (pindaan (ae): penjejak papertrade memberi harga stor); lalai =
    indeks Release A02 seperti semua pusingan backtest."""
    if q is None or s is None:
        from AUTOTUNE.teras import data as D
        ix = pd.read_parquet(D.ambil(tag='autotune-data-a02') / 'idx.parquet')
        ix['d'] = ix.date.dt.year * 10000 + ix.date.dt.month * 100 + ix.date.dt.day
        q, s = ix[ix.ticker == 'QQQ'].set_index('d').close, ix[ix.ticker == 'SPY'].set_index('d').close
    q, s = q.reindex(hu).ffill(), s.reindex(hu).ffill()
    m50 = q.rolling(50).mean()
    on = (q > m50) & (q.rolling(10).mean() > q.rolling(20).mean())
    off = (~on) & m50.notna()
    umur = on.groupby((on != on.shift()).cumsum()).cumcount() + 1
    qmax = q.rolling(252).max()
    m200 = s.rolling(200).mean()
    rv21 = s.pct_change().rolling(21).std() * np.sqrt(252)
    rv63 = s.pct_change().rolling(63).std() * np.sqrt(252)
    bulan, hari = pd.Series((hu // 100) % 100, index=hu), pd.Series(hu % 100, index=hu)
    k = keluasan.reindex(hu)
    P = {
        'A01': on, 'A02': off, 'A03': s > m200, 'A04': s < m200, 'A05': q >= 0.97 * qmax, 'A06': q <= 0.90 * qmax,
        'A07': q <= 0.80 * qmax, 'A08': on & (umur <= 10), 'A09': off & (umur <= 10), 'A10': _rsi(q) < 35,
        'A11': q / q.shift(5) - 1 >= 0.03, 'B01': rv21 >= 0.25, 'B02': rv21 <= 0.10, 'B03': rv21 < rv63,
        'C01': k.b50 >= 0.60, 'C02': k.b50 <= 0.30, 'C03': k.b50 - k.b50.shift(10) >= 0.10, 'C04': k.b200 >= 0.60,
        'C05': k.b5 >= 0.15,
        'G01': bulan.isin([11, 12, 1, 2, 3, 4]), 'G02': bulan.isin([5, 6, 7, 8, 9, 10]), 'G03': hari <= 7, 'G04': bulan == 1,
    }
    return {n: v.fillna(False).astype(bool) for n, v in P.items()}


_KOD = {'sektor': {}, 'industri': {}}


def kod_tetap(x, jenis):
    """Kod integer yang sama merentas kedua-dua panel; -1 = Lain-lain / tiada."""
    K = _KOD[jenis]
    for v in pd.unique(x):
        if v != 'Lain-lain' and v == v and v not in K:
            K[v] = len(K)
    return x.map(K).fillna(-1).astype(np.int16).to_numpy()


def bingkai(pan, peta, nama):
    """Ciri setiap bar untuk agregat sektor/industri."""
    c, mula = pan['c'], pan['mula']
    r = {k: np.full(len(c), np.nan) for k in (63, 21, 20)}
    for t in range(len(mula) - 1):
        a, b = mula[t], mula[t + 1]
        cs = pd.Series(c[a:b])
        for k in r:
            r[k][a:b] = (cs / cs.shift(k) - 1).to_numpy()
    p = peta.reindex(pan['ticker'])
    return pd.DataFrame({'panel': nama, 'bar': np.arange(len(c)), 'date': pan['tarikh'], 'r63': r[63], 'r21': r[21],
                         'r20': r[20], 'b20': r[20] >= 0.20, 'a50': pan['F'][1] > 0, 'a200': pan['F'][2] > 0,
                         'd5': pan['F'][18] > 0, 'layak': pan['layak'],
                         'sektor': pd.Series(p.sektor.to_numpy()[pan['tid']]), 'industri': pd.Series(p.industri.to_numpy()[pan['tid']])}
                        ).assign(sektor=lambda d: kod_tetap(d.sektor, 'sektor'), industri=lambda d: kod_tetap(d.industri, 'industri'))


def kumpulan(df):
    """Tambah lajur prasyarat D dan E (dikira merentas kedua-dua panel, bar layak sahaja)."""
    L = df[df.layak]
    s = L[L.sektor >= 0].groupby(['date', 'sektor']).agg(m=('r63', 'median'), b=('a50', 'mean')).reset_index()
    s['kd'] = s.groupby('date').m.rank(ascending=False, method='first')
    s['ns'] = s.groupby('date').m.transform('count')
    s['D01'], s['D02'], s['D03'] = s.kd <= 3, s.kd > s.ns - 3, s.b >= 0.60
    i = L[L.industri >= 0].groupby(['date', 'industri']).agg(
        m63=('r63', 'median'), m21=('r21', 'median'), b=('a50', 'mean'), n=('a50', 'size'), besar=('b20', 'sum')).reset_index()
    i = i[i.n >= 5]
    i['p63'] = i.groupby('date').m63.rank(pct=True)
    i['p21'] = i.groupby('date').m21.rank(pct=True)
    i['E01'], i['E02'], i['E03'], i['E04'] = i.p63 >= 0.8, i.p21 >= 0.8, i.p63 <= 0.2, i.b >= 0.60
    df = df.merge(s[['date', 'sektor', 'D01', 'D02', 'D03']], on=['date', 'sektor'], how='left')
    df = df.merge(i[['date', 'industri', 'E01', 'E02', 'E03', 'E04', 'besar']], on=['date', 'industri'], how='left')
    df['ada_D'] = df.D01.notna()
    df['ada_E'] = df.E01.notna()
    df['E05'] = (df.besar.fillna(0) - (df.b20 & df.layak).astype(int)) >= 1
    for k in ('D01', 'D02', 'D03', 'E01', 'E02', 'E03', 'E04'):
        df[k] = df[k].fillna(False).astype(bool)
    return df


def earnings(pan):
    """Prasyarat F setiap bar + topeng 'ada data'."""
    e = pd.read_csv(os.path.join(BS2, 'data', 'sec', 'earnings_8k.csv'), usecols=['saham', 'tarikh_fail', 'masa_terima', 'items'])
    e = e[e['items'].astype(str).str.contains('2.02', regex=False)]
    e['d'] = e.tarikh_fail.str.replace('-', '').astype(int)
    e['lewat'] = pd.to_datetime(e.masa_terima, errors='coerce', utc=True).dt.hour >= 20     # selepas tutup -> sesi berikutnya
    su = pd.read_csv(os.path.join(BS2, 'data', 'sec', 'sue.csv'), usecols=['saham', 'sue', 'tumbuh_hasil', 'tarikh_umum'])
    su = su.dropna(subset=['tarikh_umum'])
    su['d'] = su.tarikh_umum.str.replace('-', '').astype(int)
    eg, sg = dict(tuple(e.groupby('saham'))), dict(tuple(su.sort_values('d').groupby('saham')))
    N = len(pan['c'])
    out = {k: np.zeros(N, bool) for k in ('F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'ada_F', 'ada_S')}
    c, tarikh, mula = pan['c'], pan['tarikh'], pan['mula']
    for t, nama in enumerate(pan['ticker']):
        a, b = mula[t], mula[t + 1]
        d = tarikh[a:b]
        T = b - a
        if nama in eg:
            g = eg[nama]
            ev = np.where(g.lewat.to_numpy(), np.searchsorted(d, g.d.to_numpy(), 'right'), np.searchsorted(d, g.d.to_numpy(), 'left'))
            ev = np.unique(ev[(ev > 0) & (ev < T)])
            if len(ev):
                i = np.arange(T)
                kn = np.searchsorted(ev, i, 'right')                    # peristiwa seterusnya (> i)
                ada_n = kn < len(ev)
                hingga = np.where(ada_n, ev[np.minimum(kn, len(ev) - 1)] - i, 10 ** 6)
                ada_l = kn > 0
                lalu = ev[np.maximum(kn - 1, 0)]
                sejak = np.where(ada_l, i - lalu, 10 ** 6)
                reaksi = np.where(ada_l, c[a + lalu] / c[a + np.maximum(lalu - 1, 0)] - 1, np.nan)
                out['F01'][a:b] = (hingga >= 1) & (hingga <= 5)
                out['F02'][a:b] = sejak <= 4
                out['F03'][a:b] = (sejak >= 5) & (sejak <= 19)
                out['F04'][a:b] = ada_n & (hingga > 20)
                out['F07'][a:b] = (sejak <= 19) & (reaksi >= 0.05)
                out['ada_F'][a:b] = ada_n & ada_l                       # di antara dua earnings yang direkod
        if nama in sg:
            g = sg[nama]
            k = np.searchsorted(g.d.to_numpy(), d, 'left') - 1          # diumumkan SEBELUM hari bar
            ok = k >= 0
            kk = np.maximum(k, 0)
            sue, th = g.sue.to_numpy()[kk], g.tumbuh_hasil.to_numpy()[kk]
            out['F05'][a:b] = ok & (sue > 0)
            out['F06'][a:b] = ok & (th >= 0.20)
            out['ada_S'][a:b] = ok & ~np.isnan(sue)
    return out


def ukur(X, pilih, tp, P, ada=None):
    """Kadar lari / t10 / gagal bila P benar lawan palsu, setiap tempoh, antara bar `pilih` (indeks)."""
    out = {}
    for p in range(int(tp.max()) + 1):
        k = pilih[tp[pilih] == p]
        if ada is not None:
            k = k[ada[k]]
        b, f = k[P[k]], k[~P[k]]
        r = {'n_benar': len(b), 'n_palsu': len(f)}
        for j, n in ((4, 'lari'), (1, 't10'), (3, 'gagal')):
            r[n + '_b'] = float(X[b, j].mean()) if len(b) else np.nan
            r[n + '_p'] = float(X[f, j].mean()) if len(f) else np.nan
        out[p] = r
    return out


def isyarat_kohort(kerja, pan, set_, C):
    """Bar isyarat lapan setup kohort (gabungan), satu posisi setiap saham setiap setup."""
    K = json.load(open(os.path.join(hadapan.KELUAR, 'kohort.json')))['ahli']
    bn = pickle.load(open(os.path.join(kerja, f'benih_{set_}.pkl'), 'rb'))['sig']
    f = os.path.join(kerja, f'benih_{set_}_tala.pkl')
    bn = {**bn, **(pickle.load(open(f, 'rb'))['sig'] if os.path.exists(f) else {})}
    semua = []
    for a in K:
        pc = a['pencetus']
        ev = tala.isyarat(pan, pan['P'][pc] if pc.startswith('P') else bn[pc])
        ev = ev[tala.topeng(pan, C, ev, a['fs'][0], a['amb'][0]) & tala.topeng(pan, C, ev, a['fs'][1], a['amb'][1])]
        semua.append(ev[teras.satu_posisi(ev, np.full(len(ev), tk.TMAX - 1), pan['tid'])])
    return np.sort(np.concatenate(semua))


def main(kerja):
    sys.path.insert(0, cari.AKAR)
    from REVERSE.teras import data as RD
    pans = {s: cari.panel(kerja, s) for s in ('A', 'B')}
    peta = RD.peta_sektor(sorted(set(pans['A']['ticker']) | set(pans['B']['ticker'])))
    df = kumpulan(pd.concat([bingkai(pans[s], peta, s) for s in ('A', 'B')], ignore_index=True))
    L = df[df.layak].groupby('date').agg(b50=('a50', 'mean'), b200=('a200', 'mean'), b5=('d5', 'mean'))
    hu = np.array(sorted(df.date.unique()))
    PM = pasaran(hu, L)
    nama_tempoh = {'A': [t[0] for t in atom.TEMPOH['A']], 'B': [t[0] for t in atom.TEMPOH['B']]}
    baris = []
    for s in ('A', 'B'):
        pan = pans[s]
        X = tk.label_asas(pan)
        C = tala.ciri(pan)
        d = df[df.panel == s].sort_values('bar')
        E = earnings(pan)
        P = {n: PM[n].reindex(pan['tarikh']).to_numpy() for n in PM}
        P.update({k: d[k].to_numpy() for k in ('D01', 'D02', 'D03', 'E01', 'E02', 'E03', 'E04', 'E05')})
        P.update({k: E[k] for k in ('F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07')})
        ada = {'D': d.ada_D.to_numpy(), 'E': d.ada_E.to_numpy(), 'F': E['ada_F']}
        ada_khas = {'F05': E['ada_S'], 'F06': E['ada_S']}
        semua, koh = np.flatnonzero(pan['sah']), isyarat_kohort(kerja, pan, s, C)
        tp = pan['tempoh']
        for n in PRASYARAT:
            k = n[:3]
            m = ada_khas.get(k, ada.get(k[0]))
            for pop, pilih in (('semua', semua), ('kohort', koh)):
                for p, r in ukur(X, pilih, tp, P[k], m).items():
                    baris.append({'prasyarat': n, 'populasi': pop, 'kepingan': nama_tempoh[s][p], **r})
        cari.log(f'kumpulan {s}: {len(semua):,} bar layak, {len(koh):,} isyarat kohort')
    T = pd.DataFrame(baris)
    d_ = os.path.join(SINI, 'hasil', 'PRASYARAT')
    os.makedirs(d_, exist_ok=True)
    T.to_csv(os.path.join(d_, 'prasyarat.csv'), index=False, float_format='%.5f')

    def ringkas(n, pop):
        t = T[(T.prasyarat == n) & (T.populasi == pop)]
        kb = t[t.kepingan.str.startswith('K')]
        nb, npal = kb.n_benar.sum(), kb.n_palsu.sum()
        w = lambda kol, berat: float((kb[kol] * kb[berat]).sum() / kb[berat].sum()) if kb[berat].sum() else np.nan
        sah = t[(t.n_benar >= 30) & (t.n_palsu >= 30)]
        return {'bahagian': nb / max(nb + npal, 1), 'n_benar': int(nb), 'lari_b': w('lari_b', 'n_benar'), 'lari_p': w('lari_p', 'n_palsu'),
                'gagal_b': w('gagal_b', 'n_benar'), 'gagal_p': w('gagal_p', 'n_palsu'),
                'naik': int((sah.lari_b > sah.lari_p).sum()), 'kepingan': len(sah)}

    R = {(n, pop): ringkas(n, pop) for n in PRASYARAT for pop in ('semua', 'kohort')}
    p = lambda x, k=1: '–' if x != x else f'{x * 100:.{k}f}'
    try:
        sys.path.insert(0, os.path.join(BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    A = ['# Tinjauan prasyarat: apa selain QQQ yang mengubah peluang saham "lari"? (backtest, BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_prasyarat.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (h). '
         '**Jangan sunting secara manual.**', '',
         'Prasyarat = isyarat yang BUKAN daripada harga saham itu sendiri. "Lari" = naik ≥ 5 % minggu pertama, capai ≥ 10 % '
         'sebelum henti −8 %, masih ≥ 10 % pada minggu ke-4. Angka jadual daripada **kumpulan B** (saham yang carian tidak '
         'lihat, 2010 – Ogo 2026). "Konsisten" = bilangan kepingan (E1, E2 kumpulan A; K1, K2, K3 kumpulan B) di mana kadar lari '
         'lebih tinggi bila prasyarat BENAR.', '',
         '| Prasyarat | % masa benar | Semua saham: lari % benar / palsu | Konsisten | Kena henti % benar / palsu | '
         'Kohort F: lari % benar / palsu | Konsisten (kohort) | Isyarat kohort (benar) |', '|---' * 8 + '|']
    for g, tajuk in KUMP.items():
        A.append(f'| **{tajuk}** | | | | | | | |')
        for n in [x for x in PRASYARAT if x[0] == g]:
            a, k = R[(n, 'semua')], R[(n, 'kohort')]
            A.append(f"| {n[4:]} | {p(a['bahagian'], 0)} | {p(a['lari_b'])} / {p(a['lari_p'])} | {a['naik']}/{a['kepingan']} | "
                     f"{p(a['gagal_b'])} / {p(a['gagal_p'])} | {p(k['lari_b'])} / {p(k['lari_p'])} | {k['naik']}/{k['kepingan']} | "
                     f"{k['n_benar']:,} |")
    kuat = [n for n in PRASYARAT if R[(n, 'semua')]['kepingan'] == 5 and R[(n, 'semua')]['naik'] == 5]
    lemah = [n for n in PRASYARAT if R[(n, 'semua')]['kepingan'] == 5 and R[(n, 'semua')]['naik'] == 0]
    kk = [n for n in PRASYARAT if R[(n, 'kohort')]['kepingan'] == 5 and R[(n, 'kohort')]['naik'] == 5]
    A += ['', '## Bacaan', '',
          f'- Menaikkan kadar lari bagi SEMUA saham dalam kelima-lima kepingan ({len(kuat)}): '
          + ('; '.join(x[4:] for x in kuat) or 'tiada') + '.',
          f'- Menurunkan kadar lari dalam kelima-lima kepingan ({len(lemah)}): ' + ('; '.join(x[4:] for x in lemah) or 'tiada') + '.',
          f'- Menaikkan kadar lari bagi isyarat KOHORT F dalam kelima-lima kepingan ({len(kk)}): '
          + ('; '.join(x[4:] for x in kk) or 'tiada') + '.', '',
          '## Kaveat', '',
          '- Prasyarat pasaran, keluasan dan kalendar berubah ikut HARI: bar banyak tetapi pemerhatian bebas sedikit; satu '
          'tahun yang luar biasa boleh mengubah bacaan. Sebab itu lajur "Konsisten" lebih penting daripada beza peratus.',
          '- Prasyarat yang menaikkan kadar lari selalunya turut menaikkan kadar kena henti (saham lebih meruap); baca kedua-dua '
          'lajur.',
          '- "Earnings akan datang" memakai tarikh sebenar (pandang ke hadapan ringan). Peta sektor/industri ialah peta '
          'semasa. Tiada saham delist. Set 2000 bukan tapisan Shariah.',
          '- Tinjauan, bukan pemilihan: 38 prasyarat diukur, jadi beberapa akan kelihatan baik secara kebetulan. Prasyarat '
          'hanya boleh dipakai selepas dimasukkan ke pusingan carian dengan pradaftar tersendiri.', '']
    open(os.path.join(d_, 'LAPORAN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f'prasyarat siap: konsisten naik {len(kuat)}, konsisten turun {len(lemah)}, kohort {len(kk)}')


if __name__ == '__main__':
    main(sys.argv[1])
