"""Tinjauan jenis dan tempoh trend menaik setiap saham (SPEC pindaan 16 Nov 2026 (w)). DESKRIPTIF: bukan carian setup.

Satu trend menaik = dari satu dasar ke satu puncak (zigzag ATR): disahkan bermula apabila tutup naik >= k x ATR14 di atas
tutup terendah sejak puncak lalu; disahkan tamat apabila tutup jatuh >= k x ATR14 di bawah tutup tertinggi sejak dasar.
Tiga saiz (k = 2, 4, 8) dan empat jenis ikut kelajuan. Dasar dan puncak hanya diketahui selepas berlaku.
Guna: python3 cs_jenis_trend.py <kerja>. Jangan sunting keluaran secara manual."""
import os
import sys

import numpy as np
import pandas as pd
from numba import njit

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402

SAIZ = ((2.0, 'kecil'), (4.0, 'sederhana'), (8.0, 'besar'))             # dikunci pindaan (w)
LAJU = ((0.0025, 'sangat perlahan'), (0.005, 'perlahan'), (0.01, 'sederhana'), (np.inf, 'laju'))
MIN_SESI, BULAN = 5, 21
BAKUL = ((BULAN, '< 1 bulan'), (3 * BULAN, '1–3 bulan'), (6 * BULAN, '3–6 bulan'), (10 ** 9, '> 6 bulan'))
N_BAKI = (5, 10, 20, 40, 60, 126)


@njit(cache=True)
def zigzag(c, atr, mula, k):
    """Ayunan naik lengkap setiap saham. Pulangkan (dasar, puncak, sah_naik, sah_tamat, turun_tengah, n_awal, n_gantung):
    indeks bar dasar, puncak, bar pengesahan naik dan bar pengesahan tamat; turun paling dalam di tengah jalan; bilangan
    ayunan pertama (dasar terpotong) dan ayunan yang belum tamat pada hujung data (kedua-duanya dibuang)."""
    kap = len(c) // 2 + 8
    T, P = np.empty(kap, np.int64), np.empty(kap, np.int64)
    U, D = np.empty(kap, np.int64), np.empty(kap, np.int64)
    G = np.empty(kap)
    n = n_awal = n_gantung = 0
    for t in range(len(mula) - 1):
        a, b = mula[t], mula[t + 1]
        i0 = a
        while i0 < b and not (atr[i0] > 0.0):
            i0 += 1
        if i0 >= b - 1:
            continue
        arah, hi, lo, tr, cu, kira = 0, i0, i0, i0, i0, False
        dd = dds = 0.0
        for i in range(i0 + 1, b):
            x, th = c[i], k * atr[i]
            if not (th > 0.0):
                continue
            if arah == 0:
                if x > c[hi]:
                    hi = i
                if x < c[lo]:
                    lo = i
                if x <= c[hi] - th:
                    arah, lo = -1, i
                elif x >= c[lo] + th:
                    arah, tr, cu, hi, kira, dd, dds = 1, lo, i, i, False, 0.0, 0.0
            elif arah == 1:
                if x > c[hi]:
                    hi = i
                    if dds > dd:
                        dd = dds
                    dds = 0.0
                else:
                    d = 1.0 - x / c[hi]
                    if x <= c[hi] - th:
                        if kira:
                            T[n], P[n], U[n], D[n], G[n] = tr, hi, cu, i, dd
                            n += 1
                        else:
                            n_awal += 1
                        arah, lo = -1, i
                    elif d > dds:
                        dds = d
            else:
                if x < c[lo]:
                    lo = i
                elif x >= c[lo] + th:
                    arah, tr, cu, hi, kira, dd, dds = 1, lo, i, i, True, 0.0, 0.0
        if arah == 1 and kira:
            n_gantung += 1
    return T[:n], P[:n], U[:n], D[:n], G[:n], n_awal, n_gantung


def trend(pan, k):
    """Satu baris setiap ayunan naik lengkap dengan dasar pada bar layak."""
    T, P, U, D, G, n_awal, n_gantung = zigzag(pan['c'], pan['atr'], pan['mula'], float(k))
    c = pan['c']
    ok = pan['sah'][T]
    T, P, U, D, G = T[ok], P[ok], U[ok], D[ok], G[ok]
    sesi = P - T
    naik = c[P] / c[T] - 1.0
    t = pd.DataFrame({'tid': pan['tid'][T], 'tahun': pan['tarikh'][T] // 10000, 'sesi': sesi, 'naik': naik,
                      'laju': (1.0 + naik) ** (1.0 / np.maximum(sesi, 1)) - 1.0, 'turun_tengah': G,
                      'lewat': U - T, 'sesi_kenal': D - U, 'naik_kenal': c[D] / c[U] - 1.0, 'naik_selepas_sah': c[P] / c[U] - 1.0})
    t['jenis'] = np.asarray([x[1] for x in LAJU])[np.searchsorted(np.asarray([x[0] for x in LAJU]), t.laju.to_numpy(), side='right')]
    t['bakul'] = np.asarray([x[1] for x in BAKUL])[np.searchsorted(np.asarray([x[0] for x in BAKUL]), t.sesi.to_numpy(), side='right')]
    return t, n_awal, n_gantung


def kumpul(kerja):
    """dict saiz -> (jadual trend A + B, saham-tahun layak, ayunan pertama dibuang, belum tamat dibuang)."""
    out = {}
    for k, nama in SAIZ:
        bhg, st, na, ng = [], 0.0, 0, 0
        for j, set_ in enumerate(('A', 'B')):
            pan = cari.panel(kerja, set_)
            t, a, g = trend(pan, k)
            t['tid'] += j * 100000
            bhg.append(t)
            st += float(pan['sah'].sum()) / 252.0
            na, ng = na + a, ng + g
        out[nama] = (pd.concat(bhg, ignore_index=True), st, na, ng)
        cari.log(f'trend {nama} (k={k:g}): {len(out[nama][0]):,} ayunan lengkap; saham-tahun {st:,.0f}; awal {na:,}, belum tamat {ng:,}')
    return out


def ringkas(x):
    q = lambda s, p: float(s.quantile(p)) if len(s) else np.nan
    return dict(n=len(x), sesi_25=q(x.sesi, .25), sesi_50=q(x.sesi, .5), sesi_75=q(x.sesi, .75), sesi_90=q(x.sesi, .9),
                naik_25=q(x.naik, .25), naik_50=q(x.naik, .5), naik_75=q(x.naik, .75), turun_50=q(x.turun_tengah, .5),
                turun_75=q(x.turun_tengah, .75), lewat_50=q(x.lewat, .5), sesi_kenal_50=q(x.sesi_kenal, .5),
                naik_kenal_50=q(x.naik_kenal, .5), naik_kenal_purata=float(x.naik_kenal.mean()) if len(x) else np.nan,
                kenal_untung=float((x.naik_kenal > 0).mean()) if len(x) else np.nan, naik_selepas_sah_50=q(x.naik_selepas_sah, .5))


def jadual(S):
    """Semua jadual sebagai satu DataFrame panjang (lajur `jadual` membezakan)."""
    B = []
    for nama, (t, st, na, ng) in S.items():
        tr = t[t.sesi >= MIN_SESI]
        B.append(dict(jadual='saiz', saiz=nama, kumpulan='semua', setahun=len(tr) / st, lonjakan=float((t.sesi < MIN_SESI).mean()),
                      buang_awal=na, buang_gantung=ng, bahagian=1.0, **ringkas(tr)))
        for _, nm in BAKUL:
            B.append(dict(jadual='tempoh', saiz=nama, kumpulan=nm, bahagian=float((tr.bakul == nm).mean()), **ringkas(tr[tr.bakul == nm])))
        for _, nm in LAJU:
            B.append(dict(jadual='jenis', saiz=nama, kumpulan=nm, bahagian=float((tr.jenis == nm).mean()), **ringkas(tr[tr.jenis == nm])))
        for N in N_BAKI:
            x = tr[tr.sesi >= N]
            if len(x) >= 100:
                B.append(dict(jadual='baki', saiz=nama, kumpulan=str(N), n=len(x), bahagian=float((x.sesi >= 2 * N).mean()),
                              sesi_50=float((x.sesi - N).median()), sesi_25=float((x.sesi - N).quantile(.25)),
                              sesi_75=float((x.sesi - N).quantile(.75))))
        th = tr.groupby('tahun').sesi.agg(['median', 'size'])
        th = th[th['size'] >= 200]
        B.append(dict(jadual='tahun', saiz=nama, kumpulan='julat median tempoh ikut tahun', n=len(th), sesi_25=float(th['median'].min()),
                      sesi_50=float(th['median'].median()), sesi_75=float(th['median'].max())))
    return pd.DataFrame(B)


def lapor_(kerja):
    import cs_lapor as lapor
    S = kumpul(kerja)
    J = jadual(S)
    d_ = os.path.join(SINI, 'hasil', 'TREND')
    os.makedirs(d_, exist_ok=True)
    J.to_csv(os.path.join(d_, 'jenis_trend.csv'), index=False, float_format='%.5f')
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0: '–' if x != x else f'{x * 100:.{k}f}'
    mg = lambda s: '–' if s != s else (f'{s:.0f} hari' if s < 10 else f'{s / 5:.0f} minggu' if s < 3 * BULAN else f'{s / BULAN:.0f} bulan')
    g = lambda jd, sz: J[(J.jadual == jd) & (J.saiz == sz)]
    n_saham = sum(len(cari.panel(kerja, s)['ticker']) for s in ('A', 'B'))
    A = ['# Jenis dan tempoh trend menaik setiap saham (tinjauan; gambaran sahaja, BUKAN isyarat beli atau jual)', '', status, '',
         'Dijana `kajian/carian_setup/cs_jenis_trend.py`. Takrif ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (w). '
         '**Jangan sunting secara manual.**', '',
         f'Data: {n_saham:,} saham AS, 2010 – 2026, harga tutup harian. "Hari" di sini = hari dagangan (5 hari seminggu; 21 = sebulan).', '',
         '**Apa kata buku (Teori Dow, untuk pasaran keseluruhan):** tiga trend serentak — utama (kira-kira setahun atau lebih), sekunder '
         '(kira-kira 3 minggu hingga 3 bulan) dan kecil (beberapa hari hingga 3 minggu); angka itu kelaziman, bukan peraturan tetap '
         '([thismatter.com](https://thismatter.com/money/technical-analysis/dow-theory.htm), '
         '[babypips.com](https://www.babypips.com/forexpedia/dow-theory)). Tiada jadual tempoh piawai bagi saham tunggal dalam sumber yang '
         'disemak, jadi tempoh di bawah diukur sendiri.', '',
         '**Satu trend menaik** = dari satu dasar ke satu puncak. Trend dikira tamat apabila harga jatuh melebihi had toleransi dari harga '
         'tertingginya. Tiga saiz ikut had toleransi itu (ATR = julat gerakan harian biasa saham itu, lazimnya 2–4 % harga):', '',
         '- **Kecil**: tamat bila jatuh 2 × ATR (kira-kira 5–8 %). Ayunan beberapa hari hingga beberapa minggu.',
         '- **Sederhana**: tamat bila jatuh 4 × ATR (kira-kira 10–15 %). "Turun sikit masih ok."',
         '- **Besar**: tamat bila jatuh 8 × ATR (kira-kira 20–30 %). Trend utama; di dalamnya ada beberapa trend sederhana.', '',
         '## 1. Tiga saiz trend: berapa kerap, berapa lama, berapa banyak naik', '',
         '| Saiz | Bilangan setiap saham setahun | Tempoh biasa (nilai tengah) | Julat separuh tengah | 1 daripada 10 lebih lama daripada | Naik dasar → puncak (nilai tengah) | Julat separuh tengah |',
         '|---' * 7 + '|']
    for _, nama in SAIZ:
        r = g('saiz', nama).iloc[0]
        A.append(f"| **{nama.capitalize()}** | {r.setahun:.1f} | **{mg(r.sesi_50)}** ({r.sesi_50:.0f} hari) | {mg(r.sesi_25)} – {mg(r.sesi_75)} | {mg(r.sesi_90)} | "
                 f"**+{p(r.naik_50)} %** | +{p(r.naik_25)} % – +{p(r.naik_75)} % |")
    A += ['', '## 2. Berapa lama: pecahan ikut tempoh', '',
          '| Saiz | < 1 bulan | 1–3 bulan | 3–6 bulan | > 6 bulan |', '|---' * 5 + '|']
    for _, nama in SAIZ:
        x = g('tempoh', nama).set_index('kumpulan')
        A.append(f"| **{nama.capitalize()}** | " + ' | '.join(f"{p(x.bahagian[nm])} % (naik +{p(x.naik_50[nm])} %)" for _, nm in BAKUL) + ' |')
    A += ['', 'Dalam kurungan = kenaikan nilai tengah bagi trend dalam kumpulan tempoh itu.', '',
          '## 3. Empat jenis ikut kelajuan', '',
          'Kelajuan = purata kenaikan sehari dari dasar ke puncak. **Sangat perlahan** < 0.25 % sehari (kurang ~5 % sebulan); **perlahan** '
          '0.25–0.5 % sehari (~5–11 % sebulan); **sederhana** 0.5–1 % sehari (~11–23 % sebulan); **laju** ≥ 1 % sehari (≥ ~5 % seminggu).', '']
    for _, nama in SAIZ[1:]:
        A += [f'**Trend {nama}:**', '',
              '| Jenis | Bahagian | Tempoh biasa | Julat separuh tengah | Naik dasar → puncak | Turun paling dalam di tengah jalan (nilai tengah) |',
              '|---' * 6 + '|']
        for r in g('jenis', nama).itertuples():
            A.append(f"| {r.kumpulan.capitalize()} | {p(r.bahagian)} % | **{mg(r.sesi_50)}** | {mg(r.sesi_25)} – {mg(r.sesi_75)} | +{p(r.naik_50)} % | −{p(r.turun_50)} % |")
        A.append('')
    A += ['## 4. Kalau sudah naik N hari, berapa lama lagi?', '',
          '| Saiz | Sudah naik | Berapa peratus sampai dua kali ganda tempoh itu | Baki tempoh (nilai tengah) | Julat separuh tengah baki |', '|---' * 5 + '|']
    for _, nama in SAIZ[1:]:
        for r in g('baki', nama).itertuples():
            A.append(f"| {nama.capitalize()} | {mg(float(r.kumpulan))} | {p(r.bahagian)} % | {mg(r.sesi_50)} | {mg(r.sesi_25)} – {mg(r.sesi_75)} |")
    A += ['', '## 5. Bahagian yang boleh dikenal semasa berlaku', '',
          'Dasar dan puncak hanya diketahui kemudian. Trend hanya boleh DIKENAL selepas harga sudah naik melebihi had toleransi dari dasar, '
          'dan hanya DISAHKAN tamat selepas harga sudah jatuh sebanyak itu dari puncak. Jadual ini mengukur bahagian tengah itu sahaja '
          '(tanpa kos):', '',
          '| Saiz | Lewat dikenal (dari dasar) | Tempoh dikenal → disahkan tamat | Perubahan harga sepanjang itu (nilai tengah) | Purata | Berapa peratus berakhir untung |',
          '|---' * 6 + '|']
    for _, nama in SAIZ:
        r = g('saiz', nama).iloc[0]
        A.append(f"| **{nama.capitalize()}** | {mg(r.lewat_50)} | {mg(r.sesi_kenal_50)} | {r.naik_kenal_50 * 100:+.1f} % | {r.naik_kenal_purata * 100:+.1f} % | {p(r.kenal_untung)} % |")
    A += ['', '## 6. Kestabilan dan bilangan', '']
    for _, nama in SAIZ:
        r, th = g('saiz', nama).iloc[0], g('tahun', nama).iloc[0]
        A.append(f"- {nama.capitalize()}: {int(r.n):,} trend lengkap (≥ {MIN_SESI} hari); {p(r.lonjakan)} % ayunan lebih pendek daripada {MIN_SESI} hari "
                 f"(lonjakan, tidak dikira); nilai tengah tempoh setiap tahun antara {th.sesi_25:.0f} dan {th.sesi_75:.0f} hari; dibuang: "
                 f"{int(r.buang_awal):,} ayunan pertama dan {int(r.buang_gantung):,} yang belum tamat pada hujung data.")
    A += ['', '## 7. Kaveat', '',
          '- Ini gambaran apa yang SUDAH berlaku, bukan isyarat beli atau jual: dasar dan puncak tidak diketahui pada masa itu (lihat §5).',
          '- Kenaikan dan kelajuan dasar → puncak melebihi apa yang dagangan sebenar boleh tangkap.',
          '- Trend yang belum tamat pada hujung data dibuang, jadi trend paling panjang sedikit terkurang kira; tiada saham delist dalam data.',
          '- Angka bergantung pada takrif; sebab itu tiga saiz ditunjuk. Jadual penuh: `hasil/TREND/jenis_trend.csv`.', '']
    open(os.path.join(d_, 'JENIS_TREND.md'), 'w', encoding='utf-8').write('\n'.join(A))
    return J


if __name__ == '__main__':
    lapor_(sys.argv[1])
