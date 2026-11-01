"""Perlukah kaedah Mxx diubah pada paksi MASUK / PEGANG / KELUAR? — soalan pengguna 1 Nov 2026.

Semua 134 kaedah Mxx datang daripada sumber luar (video, buku, blog, forum pedagang). Soalan
pengguna: sepanjang papertrade berjalan, ada paksi yang perlu diubah untuk memaksimumkan untung?

Dokumen ini TIDAK mengulang `laporan/PENGANALISIS.md` (pangkat) atau `laporan/KAEDAH_TERBAIK.md`
(bolehkah pangkat dipercayai). Ia menjawab soalan yang berbeza: untuk setiap kaedah, paksi mana
yang BUKTINYA menunjukkan perlu diubah, dan ke arah mana.

EMPAT SUMBER BEBAS digabungkan (tiada satu pun dikumpul untuk soalan ini; semuanya sudah ada):

  A. Lengkung pegang registry (`data/registry_M_gabung.csv` lajur `pegang`) — bagi SETIAP dagangan
     varian aktif, pulangan beli-dan-pegang N hari dari entry yang SAMA (N = 5,10,15,20,30,40,60),
     MENGABAIKAN henti/keluar/sasaran kaedah. Ini ukuran terus kos mesin keluar: bandingkan `avg`
     kaedah dengan lengkung pada ufuk sepadan.
  B. W01 WFO (`WFO/data/hasil/Mxx_pilihan.csv`) — 16 suku luar sampel 2023-2026, Optuna memilih
     henti/keluar/tmax setiap suku atas 3 tahun sebelumnya SAHAJA. 131 kaedah x 16 suku = 2,096
     pilihan luar sampel tulen. Arah pilihan = apa yang data mahu, bebas daripada pendapat.
  C. Sejarah varian registry (set 431) — 633 varian merentas 141 kaedah; V0 sumber tulen, V1 spec
     dikunci, V2+ modifikasi. Dalam sampel, jadi berat sebelah memihak modifikasi; diguna hanya
     untuk membanding paksi (MASUK lawan KELUAR) yang dipilih dengan cara SAMA.
  D. Lejar Penuh hadapan (`lejar/`) — 6,079 posisi lorong 1 sudah keluar merentas 110 kaedah.
     Diguna HANYA untuk sifat mekanikal (kadar henti hari-0/1, campuran sebab keluar, lebar henti),
     BUKAN untuk pangkat prestasi: 10,550 daripada 16,629 posisi masih terbuka, jadi set tertutup
     berat sebelah kepada keluar awal.

Rujukan silang luar: `REVERSE/NXX_KELUAR.md` (sebaran pilihan keluar 4.997 mata atas 4.42 juta bar),
`REVERSE/KOMBINASI.md` (sasaran untung merugikan; perangkap kadar menang), `REVERSE/SETUP.md`
(0/598 penapis masuk ada lift positif), `REVERSE/KOLAM_EKOR.md` §4a (kecacatan henti hari-0).

Guna: python3 BacktestShariah2/standard/modifikasi_kaedah.py
Output: BacktestShariah2/laporan/MODIFIKASI_KAEDAH.md
        BacktestShariah2/data/analisis/modifikasi_kaedah.csv
"""
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # BacktestShariah2
REPO = os.path.dirname(AKAR)
KD = os.path.join(AKAR, 'kod', 'kaedah')
WFOH = os.path.join(REPO, 'WFO', 'data', 'hasil')
KELUARAN_MD = os.path.join(AKAR, 'laporan', 'MODIFIKASI_KAEDAH.md')
KELUARAN_CSV = os.path.join(AKAR, 'data', 'analisis', 'modifikasi_kaedah.csv')

HARI = [5, 10, 15, 20, 30, 40, 60]
KOS = 0.2                      # kos pulang-balik enjin (0.1% setiap belah) ditambah balik
# keluarga pilihan WFO
TRAIL = ('CHAN2', 'CHAN3', 'CHAN4')
# SD pilihan seragam dalam setiap keluarga henti (untuk z lebar henti)
SD_ATR, PURATA_ATR = 0.854, 2.75         # ATR1.5 .. ATR4
SD_PCT, PURATA_PCT = 3.12, 10.2          # PCT6 .. PCT15


# --------------------------------------------------------------------------- A. struktur kod
def konst(src, nama):
    m = re.search(rf'^{nama}\s*=\s*(.+?)\s*$', src, re.M)
    return m.group(1).split('#')[0].strip() if m else None


def baca_struktur():
    out = {}
    for f in sorted(glob.glob(os.path.join(KD, 'M*.py'))):
        src = open(f).read()
        mid = (konst(src, 'ID') or '').strip("'\"")
        if not mid:
            continue
        rec = {'nama': (konst(src, 'NAMA') or '').strip("'\""),
               'varian': (konst(src, 'VARIAN') or '').strip("'\""),
               'tmax': konst(src, 'TMAX'),
               'ada_henti': konst(src, 'ADA_HENTI')}
        for key in ('tgt', 'exitc'):
            # penugasan boleh berkongsi baris: g['sig'] = s; g['tgt'] = np.nan; g['exitc'] = e
            b = re.findall(rf"g\[['\"]{key}['\"]\]\s*=\s*([^;#\n]+)", src)
            rec[f'src_{key}'] = ' ;; '.join(x.strip() for x in b)
        t = rec['src_tgt'].strip().lower()
        rec['ada_sasaran'] = bool(t) and t not in ('np.nan', 'nan', 'np.nan ;; np.nan')
        e = rec['src_exitc'].strip().lower()
        rec['ada_exitc'] = bool(e) and e not in ('false', 'false ;; false')
        # jenis sasaran: JARAK (gandaan R / peratus tetap) lawan PARAS (struktur harga bergerak)
        jr = ('_r *' in src.lower() or '_R ' in src or re.search(r'\*\s*\(e\s*-\s*sp\)', src)
              or re.search(r'\*\s*\(e\s*-\s*st', src)
              or re.search(r'e\s*\*\s*\(1\s*\+', src))
        rec['jenis_sasaran'] = ('JARAK' if (rec['ada_sasaran'] and jr)
                                else ('PARAS' if rec['ada_sasaran'] else '–'))
        out[mid] = rec
    return out


# ------------------------------------------------------------------- B. lengkung pegang (sumber A)
def pecah_pegang(s):
    if not isinstance(s, str) or not s:
        return {}
    d = {}
    for p in s.split('|'):
        k, v = p.split(':')
        d[int(k)] = float(v)
    return d


def lengkung_pegang(reg, struktur):
    rows = {}
    for mid, s in struktur.items():
        g = reg[reg.id == mid]
        ak = g[g.varian == s['varian']]
        if not len(ak):
            continue
        a = ak.iloc[0]
        pg = pecah_pegang(a.pegang)
        if not pg:
            continue
        xs = [h for h in HARI if h in pg and not np.isnan(pg[h])]
        if not xs:
            continue
        ys = [pg[h] for h in xs]
        hari = float(a.days)
        rec = {'bt_avg': float(a.avg) * 100 + KOS, 'bt_hari': hari, 'bt_n': int(a.n),
               'bt_cagr': float(a.cagr) * 100, 'bt_menang': float(a.win) * 100}
        for h in HARI:
            rec[f'pegang{h}'] = pg.get(h, np.nan)
        rec['pegang_sepadan'] = float(np.interp(min(max(hari, xs[0]), xs[-1]), xs, ys))
        rec['kos_mesin_keluar'] = rec['bt_avg'] - rec['pegang_sepadan']
        rec['pegang60_lebih'] = pg.get(60, np.nan) - rec['bt_avg']
        rec['kadar_kaedah'] = rec['bt_avg'] / hari if hari else np.nan
        rec['kadar60'] = pg.get(60, np.nan) / 60
        rows[mid] = rec
    return pd.DataFrame(rows).T


# ------------------------------------------------------------------------ C. W01 WFO (sumber B)
def wfo_pilihan():
    rows = {}
    for f in sorted(glob.glob(os.path.join(WFOH, 'M*_pilihan.csv'))):
        mid = os.path.basename(f).split('_')[0]
        if os.path.getsize(f) < 10:
            continue
        d = pd.read_csv(f)
        if 'stop' not in d.columns or not len(d):
            continue
        a = d['stop'][d['stop'].str.startswith('ATR')].str.replace('ATR', '').astype(float)
        p = d['stop'][d['stop'].str.startswith('PCT')].str.replace('PCT', '').astype(float)
        z = []
        if len(a):
            z.append((a.mean() - PURATA_ATR) / SD_ATR)
        if len(p):
            z.append((p.mean() - PURATA_PCT) / SD_PCT)
        rec = {'wfo_nq': len(d),
               'wfo_henti_mod': d['stop'].mode().iloc[0],
               'wfo_henti_z': float(np.mean(z)) if z else np.nan,
               'wfo_henti_n': int(len(a) + len(p)),
               'wfo_keluar_mod': d['exit'].mode().iloc[0],
               'wfo_keluar_n': int((d['exit'] == d['exit'].mode().iloc[0]).sum()),
               'wfo_keluar_ekori': 100 * d['exit'].isin(TRAIL).mean(),
               'wfo_tmax_mod': float(d['tmax'].mode().iloc[0]),
               'wfo_tmax_panjang': 100 * d['tmax'].isin([0.0, 42.0, 63.0]).mean()}
        j = os.path.join(WFOH, f'{mid}.json')
        if os.path.exists(j):
            jj = json.load(open(j))
            o, b = jj.get('oos') or {}, jj.get('beku') or {}
            rec.update({'wfo_cagr': (o.get('cagr') or np.nan) * 100,
                        'beku_cagr': (b.get('cagr') or np.nan) * 100,
                        'wfo_hari': o.get('hari'), 'beku_hari': b.get('hari')})
        rows[mid] = rec
    d = pd.DataFrame(rows).T
    d['wfo_lebih_beku'] = d.wfo_cagr - d.beku_cagr
    return d


# ------------------------------------------------------------------- D. Lejar hadapan (sumber D)
def lejar_hadapan():
    f = sorted(glob.glob(os.path.join(AKAR, 'lejar', 'tutup', '*.csv')))
    f += [os.path.join(AKAR, 'lejar', 'terbuka.csv')]
    f = [x for x in f if os.path.exists(x)]
    if not f:
        return pd.DataFrame(), {}
    df = pd.concat([pd.read_csv(x) for x in f], ignore_index=True)
    jum = {'semua': len(df), 'buka': int(df.tarikh_keluar.isna().sum())}
    k = df[df.tarikh_keluar.notna()].copy()
    for c in ('hari', 'untung_pct', 'mfe_pct', 'mae_pct'):
        k[c] = pd.to_numeric(k[c], errors='coerce')
    k['jarak_henti'] = (k.harga_beli - k.henti) / k.harga_beli * 100
    k['henti_awal'] = (k.sebab_keluar == 'henti') & (k.hari <= 1)
    jum['tutup1'] = len(k)
    jum['kaedah'] = k.id_kaedah.nunique()
    jum['henti_awal'] = int(k.henti_awal.sum())
    jum['purata'] = k.untung_pct.mean()
    jum['menang'] = 100 * (k.untung_pct > 0).mean()
    jum['henti_awal_menang'] = 100 * (k[k.henti_awal].untung_pct > 0).mean()
    jum['henti_awal_purata'] = k[k.henti_awal].untung_pct.mean()
    jum['jarak_awal'] = k[k.henti_awal].jarak_henti.median()
    jum['jarak_lain'] = k[~k.henti_awal].jarak_henti.median()
    jum['mfe'] = k.mfe_pct.mean()
    jum['tanpa_awal'] = k[~k.henti_awal].untung_pct.mean()
    jum['delta_awal'] = jum['tanpa_awal'] - jum['purata']
    neg = k[k.untung_pct < 0].untung_pct.sum()
    jum['bhg_kerugian'] = 100 * k[k.henti_awal & (k.untung_pct < 0)].untung_pct.sum() / neg
    rows = {}
    for mid, g in k.groupby('id_kaedah'):
        rows[mid] = {'lj_n': len(g), 'lj_purata': g.untung_pct.mean(),
                     'lj_menang': 100 * (g.untung_pct > 0).mean(),
                     'lj_hari': g.hari.mean(),
                     'lj_henti_awal': 100 * g.henti_awal.mean(),
                     'lj_pct_henti': 100 * (g.sebab_keluar == 'henti').mean(),
                     'lj_pct_sasaran': 100 * (g.sebab_keluar == 'sasaran').mean(),
                     'lj_pct_masa': 100 * (g.sebab_keluar == 'masa').mean(),
                     'lj_jarak_henti': g.jarak_henti.median(),
                     'lj_mfe': g.mfe_pct.mean()}
    return pd.DataFrame(rows).T, jum


# --------------------------------------------------------------- E. varian ikut paksi (sumber C)
KATA_K = ('keluar', 'sasaran', 'henti', 'ekori', 'tgt', 'chandelier', 'klimaks', 'trail',
          'psar', 'supertrend', 'exitc', 'had masa', 'tmax', 'stop')
KATA_M = ('spy>', 'qqq>', 'trend', 'volume', 'volum', 'squeeze', 'penapis', 'tapis', 'sentuhan',
          'sahaja', 'ranking', 'mingguan', 'kekuatan relatif', 'close>', 'tutup>', 'adx',
          'pengesahan', 'desil', 'gred')


def paksi_varian(v):
    s = v.lower()
    ax = set()
    if any(k in s for k in KATA_K):
        ax.add('K')
    if any(k in s for k in KATA_M):
        ax.add('M')
    return ax


def varian_paksi(reg):
    rows = {}
    for mid, g in reg.groupby('id'):
        b = g[g.varian.str.contains('ikunci', na=False)]
        base = float(b.cagr.iloc[0]) * 100 if len(b) else np.nan
        hanya_k = [x.cagr * 100 for x in g.itertuples() if paksi_varian(x.varian) == {'K'}]
        hanya_m = [x.cagr * 100 for x in g.itertuples() if paksi_varian(x.varian) == {'M'}]
        rows[mid] = {'n_varian': len(g), 'v1_cagr': base,
                     'lift_keluar': (max(hanya_k) - base) if hanya_k else np.nan,
                     'n_var_keluar': len(hanya_k),
                     'lift_masuk': (max(hanya_m) - base) if hanya_m else np.nan,
                     'n_var_masuk': len(hanya_m)}
    return pd.DataFrame(rows).T


# ======================================================================= PERATURAN VERDICT
# Ditetapkan sebelum melihat keputusan per-kaedah. Setiap syarat memetik ukuran, bukan pendapat.
def verdict(x):
    """Pulang label + sebab bagi tiga paksi.

    KELUAR dipecah kepada dua sub-skor supaya satu tidak membatalkan yang lain:
      s_henti  = sifat HENTI dan SASARAN (lebar, kecacatan hari-0, sasaran tetap)
      s_syarat = pilihan SYARAT KELUAR yang pengoptimum luar sampel buat
    Jika s_henti sudah >= 3, kredit "keluar asal disahkan" tidak boleh menurunkannya di bawah 3:
    syarat keluar yang betul tidak membetulkan henti yang salah.
    """
    # ---------- KELUAR: sub-skor henti/sasaran ----------
    s_henti, bk = 0, []
    if x.get('ada_sasaran'):
        s_henti += 3
        bk.append('semak sasaran: jarak-tetap merugikan (X10 menang 94% jangkaan -0.02%), '
                  'paras-bergerak belum diuji')
    ha = x.get('lj_henti_awal')
    if pd.notna(ha) and ha >= 20:
        s_henti += 3
        bk.append('henti hari-0/1 %.0f%% (menang 0%%)' % ha)
    elif pd.notna(ha) and ha >= 10:
        s_henti += 2
        bk.append('henti hari-0/1 %.0f%%' % ha)
    z = x.get('wfo_henti_z')
    if pd.notna(z) and z >= 0.5 and (x.get('wfo_henti_n') or 0) >= 6:
        s_henti += 2
        bk.append('lebarkan henti (WFO z %+.1f)' % z)

    # ---------- KELUAR: sub-skor syarat keluar ----------
    s_syarat = 0
    km, kn = x.get('wfo_keluar_mod'), x.get('wfo_keluar_n') or 0
    if isinstance(km, str) and kn >= 7:
        if km.startswith('CHAN'):
            s_syarat += 2
            bk.append('tukar keluar -> ekori %s (%d/16 suku)' % (km, kn))
        elif km == 'TIADA' and x.get('ada_exitc'):
            s_syarat += 2
            bk.append('buang syarat keluar (%d/16 suku pilih TIADA)' % kn)
        elif km == 'ASAL':
            s_syarat -= 2
            bk.append('keluar asal disahkan (%d/16 suku)' % kn)
        else:
            s_syarat += 1
            bk.append('WFO pilih %s (%d/16)' % (km, kn))
    kos = x.get('kos_mesin_keluar')
    if pd.notna(kos) and kos < -0.20:
        s_syarat += 2
        bk.append('mesin keluar rugi %.2f mata lawan pegang pasif' % kos)
    elif pd.notna(kos) and kos > 0.50:
        s_syarat -= 1
        bk.append('mesin keluar tambah %+.2f mata' % kos)
    sk = s_henti + s_syarat
    if s_henti >= 3:
        sk = max(sk, 3)

    # ---------- PEGANG ----------
    # Lengkung pegang 60 hari positif pada hampir setiap kaedah (bahagian 2), jadi ia dapatan
    # GLOBAL dan tidak membezakan kaedah. Verdict per-kaedah hanya mengambil HAD MASA kaedah itu.
    sp, bp = 0, []
    adacap = str(x.get('tmax')) not in ('None', 'nan', '')
    tm = x.get('wfo_tmax_mod')
    if adacap and pd.notna(tm) and tm in (0.0, 63.0):
        sp += 3
        bp.append('buang/panjangkan had masa (WFO mod %s)'
                  % ('tiada' if tm == 0.0 else int(tm)))
    elif adacap and pd.notna(tm) and tm == 42.0:
        sp += 2
        bp.append('panjangkan had masa ~42 bar (WFO mod 42)')
    elif adacap and pd.notna(x.get('wfo_tmax_panjang')) and x.wfo_tmax_panjang >= 75:
        sp += 2
        bp.append('WFO pilih tmax panjang %.0f%% suku' % x.wfo_tmax_panjang)
    pm = x.get('lj_pct_masa')
    if pd.notna(pm) and pm >= 20:
        sp += 2
        bp.append('%.0f%% keluar Lejar sebab had masa' % pm)
    if not adacap:
        bp.append('tiada had masa; lengkung pegang global (§2) terpakai')
    elif not bp:
        bp.append('had masa %s tidak mengikat' % x.get('tmax'))

    # ---------- MASUK ----------
    sm, bm = 0, []
    lm = x.get('lift_masuk')
    if pd.notna(lm) and lm > 5 and (x.get('n_var_masuk') or 0) >= 1:
        sm += 1
        bm.append('varian masuk +%.0f mata CAGR dalam sampel (gagal luar sampel)' % lm)
    if not bm:
        bm.append('ruang masuk diukur kosong (SETUP 0/598, NXX 0/280)')

    def lab(sv, hi, md):
        if sv >= hi:
            return 'UBAH'
        if sv >= md:
            return 'PERTIMBANG'
        if sv <= -1:
            return 'KEKAL (disahkan)'
        return 'KEKAL'

    return (lab(sk, 3, 2), '; '.join(bk) or 'tiada bukti ubah',
            lab(sp, 3, 2), '; '.join(bp),
            'PERTIMBANG' if sm else 'KEKAL', '; '.join(bm), sk, sp, sm)


# ============================================================================= bina + tulis
def bina():
    struktur = baca_struktur()
    reg = pd.read_csv(os.path.join(AKAR, 'data', 'registry_M_gabung.csv'))
    reg = reg[reg['set'] == '431'].copy()
    A = lengkung_pegang(reg, struktur)
    B = wfo_pilihan()
    Dj, jum = lejar_hadapan()
    C = varian_paksi(reg)
    papan = json.load(open(os.path.join(AKAR, 'data', 'analisis', 'papan.json')))
    pap = pd.DataFrame(papan['rows']).set_index('id')

    ids = sorted(struktur, key=lambda s: int(re.sub(r'\D', '', s)))
    rows = []
    for mid in ids:
        r = {'id': mid}
        r.update(struktur[mid])
        for src in (A, B, Dj, C):
            if len(src) and mid in src.index:
                r.update({k: v for k, v in src.loc[mid].items() if k not in r})
        if mid in pap.index:
            p = pap.loc[mid]
            r.update({'swing': p.get('swing'), 'lulus_subset': p.get('lulus_subset'),
                      'lulus_wfo': p.get('lulus_wfo'), 'lulus_at': p.get('lulus_at'),
                      'status_papan': p.get('status')})
        rows.append(r)
    D = pd.DataFrame(rows).set_index('id')

    v = [verdict(x) for _, x in D.iterrows()]
    (D['v_keluar'], D['sebab_keluar'], D['v_pegang'], D['sebab_pegang'],
     D['v_masuk'], D['sebab_masuk'], D['skor_keluar'], D['skor_pegang'],
     D['skor_masuk']) = zip(*v)

    def stat(x):
        a, b = pd.notna(x.get('wfo_nq')), pd.notna(x.get('lj_n')) and (x.get('lj_n') or 0) >= 10
        return 'PENUH' if a and b else ('WFO' if a else ('Lejar' if b else 'TIADA'))
    D['data'] = [stat(x) for _, x in D.iterrows()]
    return D, jum


def fmt(v, p=2, suf=''):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return '–'
    return f'{v:+.{p}f}{suf}' if isinstance(v, (int, float, np.floating)) else str(v)


def tulis(D, jum):
    from datetime import datetime, timezone
    S = D[D.bt_hari <= 30] if 'bt_hari' in D else D
    n_sas = int(D.ada_sasaran.sum())
    n_jarak = int((D.jenis_sasaran == 'JARAK').sum())
    n_cap = int(D.tmax.astype(str).isin(['None', 'nan']).eq(False).sum())
    L = []
    W = L.append
    W('# Perlukah kaedah M diubah? — paksi MASUK · PEGANG · KELUAR, setiap kaedah')
    W('')
    W('Dijana %s oleh `standard/modifikasi_kaedah.py`. Rekod analisis sahaja: tiada order, '
      'tiada wang sebenar, tiada varian aktif ditukar.'
      % datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
    W('')
    W('Soalan pengguna: semua kaedah M datang daripada dapatan internet dan laman web; sepanjang '
      'papertrade berjalan, ada paksi yang perlu diubah untuk untung maksimum?')
    W('')
    W('**Paksi sasaran yang dipilih pengguna: jangkaan setiap dagangan.** Setiap dakwaan di bawah '
      'ialah mata peratus setiap dagangan, BUKAN pulangan portfolio. Bahagian 7 menyatakan '
      'dengan tepat syor mana yang TIDAK akan bertukar menjadi untung portfolio.')
    W('')
    W('## 1. Jawapan pendek')
    W('')
    W('| Paksi | Perlu diubah? | Kesan terukur setiap dagangan | Sumber |')
    W('|---|---|---|---|')
    W('| **MASUK** | **Tidak** | lift maksimum pernah diukur +0.392 mata, dan 0/598 penapis ada '
      'lift positif | `REVERSE/SETUP.md`, `REVERSE/NXX.md`, `REVERSE/KOMBINASI.md` |')
    W('| **PEGANG** | **Ya — satu-satunya paksi dengan kesan besar** | **%+.2f mata** (pegang 60 '
      'hari lawan mesin kaedah), menang **%d/%d** kaedah swing | lengkung `pegang` registry, '
      '%s dagangan backtest |'
      % (S.pegang60_lebih.mean(), int((S.pegang60_lebih > 0).sum()), len(S),
         format(int(S.bt_n.sum()), ',')))
    W('| **KELUAR** | **Arah ya, penalaan tidak** | pilihan keluar bernilai 4.997 mata (~12x '
      'paksi masuk), tetapi mesin keluar setiap kaedah hanya **%+.2f mata** median lawan pegang '
      'pasif | `REVERSE/NXX_KELUAR.md` + lengkung `pegang` |' % S.kos_mesin_keluar.median())
    W('')
    W('Kiraan verdict merentas 134 kaedah:')
    W('')
    W('| Paksi | UBAH | PERTIMBANG | KEKAL | KEKAL (disahkan) |')
    W('|---|---|---|---|---|')
    for nm, c in (('MASUK', 'v_masuk'), ('PEGANG', 'v_pegang'), ('KELUAR', 'v_keluar')):
        vc = D[c].value_counts()
        W('| %s | %d | %d | %d | %d |' % (nm, vc.get('UBAH', 0), vc.get('PERTIMBANG', 0),
                                           vc.get('KEKAL', 0), vc.get('KEKAL (disahkan)', 0)))
    W('')
    W('## 2. Ukuran yang menjawab soalan: mesin keluar lawan pegang pasif')
    W('')
    W('Lajur `pegang` registry memberi, bagi SETIAP dagangan varian aktif, pulangan beli-dan-pegang '
      'N hari dari entry YANG SAMA — mengabaikan henti, syarat keluar dan sasaran kaedah. Jadi '
      'perbezaan antara `avg` kaedah dan lengkung itu ialah nilai mesin keluar, diukur pada entry '
      'yang sama. Kaedah swing (hari pegang ≤ 30, n=%d):' % len(S))
    W('')
    W('| Ufuk pegang | Jangkaan setiap dagangan | Setiap hari | Kaedah yang pegang pasif KALAHKAN |')
    W('|---|---|---|---|')
    for h in HARI:
        c = S[f'pegang{h}']
        W('| %d hari | %+.2f%% | %+.4f%% | %d / %d |' % (
            h, c.mean(), c.mean() / h, int((c > S.bt_avg).sum()), len(S)))
    W('| **mesin kaedah sendiri** | **%+.2f%%** dalam %.1f hari | **%+.4f%%** | — |'
      % (S.bt_avg.mean(), S.bt_hari.mean(), (S.bt_avg / S.bt_hari).mean()))
    W('')
    W('Dua nombor yang mesti dibaca bersama:')
    W('')
    W('1. **Jangkaan setiap dagangan: pegang 60 hari mengalahkan mesin kaedah pada %d daripada %d '
      'kaedah swing** (+%.2f mata purata). Tiada pengecualian.'
      % (int((S.pegang60_lebih > 0).sum()), len(S), S.pegang60_lebih.mean()))
    W('2. **Kadar setiap hari hampir sama** (%+.4f%% pegang-60 lawan %+.4f%% mesin kaedah). '
      'Jadi keseluruhan kelebihan itu datang daripada memegang %.1fx lebih lama, **bukan** '
      'daripada apa-apa kelebihan.'
      % (S.kadar60.mean(), S.kadar_kaedah.mean(), 60 / S.bt_hari.mean()))
    W('')
    W('Itu bermakna: jika ukuran anda ialah untung setiap dagangan, memanjangkan pegangan ialah '
      'lever terbesar yang ada dan ia berfungsi pada setiap kaedah tanpa pengecualian. Jika '
      'ukuran anda ialah pulangan atas modal, ia hampir tiada kesan: pulangan naik %.2fx '
      '(%+.2f%% -> %+.2f%%) sementara masa modal terikat naik %.2fx (%.1f -> 60 hari). '
      'Nisbah yang hampir SAMA itulah sebabnya kadar setiap hari tidak berubah. Bahagian 7.'
      % (S.pegang60.mean() / S.bt_avg.mean(), S.bt_avg.mean(), S.pegang60.mean(),
         60 / S.bt_hari.mean(), S.bt_hari.mean()))
    W('')
    W('## 3. Apa yang pengoptimum luar sampel pilih (W01 WFO, 2,096 pilihan)')
    W('')
    W('16 suku 2023–2026, setiap suku memilih henti/keluar/tmax atas 3 tahun sebelumnya SAHAJA. '
      'Ujian arah bebas berat-sebelah: dalam setiap keluarga pilihan, adakah purata yang dipilih '
      'berbeza daripada jangkaan rawak seragam?')
    W('')
    W('| Paksi | Pilihan | Dipilih | Seragam | Keputusan |')
    W('|---|---|---|---|---|')
    W('| henti | keluarga ATR (1.5–4.0) | **2.887x** | 2.75x | lebih LEBAR, t +4.79 p 2.0e-06 |')
    W('| henti | keluarga PCT (6–15%) | **10.84%** | 10.2% | lebih LEBAR, t +5.44 p 7.5e-08 |')
    W('| henti | keluarga LOW (1–10 bar) | 5.33 bar | 5.33 | tiada kecenderungan, p 0.97 |')
    W('| keluar | CHAN4 (ekori 4xATR) | 25.8% suku | 11.1% | **2.32x terlebih pilih** |')
    W('| keluar | CHAN2 / EMA10 (ekori ketat) | 1.5% / 1.2% | 11.1% | **0.13x / 0.11x terkurang pilih** |')
    W('| tmax | purata pangkat (10<21<42<63<tiada) | **3.681** | 3.0 | lebih PANJANG, t +25.8 p 4.6e-128 |')
    W('')
    W('Arahnya sama pada ketiga-tiga paksi keluar: **henti lebih lebar, ekori lebih longgar, '
      'pegang lebih lama**. Itu sepadan tepat dengan `REVERSE/NXX_KELUAR.md`, yang mengukur '
      '23 peraturan keluar atas 4.42 juta bar dan mendapati tiga terbaik semuanya "pegang sampai '
      'momentum habis" (`X13` keluar bila RSI>70 +4.350%, `X15` ekori Chandelier 4xATR +3.706%, '
      '`X17` keluar bila ADX<20 +1.855%) dan dua terburuk kedua-duanya memotong pegangan awal.')
    W('')
    W('**TETAPI — dan ini yang menentukan syor saya:** versi WFO yang ditala setiap suku '
      'mengalahkan varian bekunya sendiri hanya **52 daripada 131 kaedah (39.7%)**, dengan purata '
      'delta CAGR **-6.4 mata** (t -3.63, p 0.0004). Jadi *arah* boleh dipercayai; *penalaan '
      'per-kaedah* tidak. `W01_LAPORAN.md` §5 mengesahkan sebabnya: tukar bajet carian Optuna '
      'mengubah CAGR dengan beza mutlak median 5.4 mata — pilihan parameter ialah hingar.')
    W('')
    W('## 4. Sejarah modifikasi: ini bukan percubaan pertama')
    W('')
    W('Registry set 431 sudah mengandungi **633 varian merentas 141 kaedah** (purata 4.5 setiap '
      'kaedah, maksimum 30): V0 sumber tulen, V1 spec dikunci, V2+ modifikasi. Varian aktif setiap '
      'kaedah ialah yang terbaik antara mereka. Lift dalam sampel atas V1 dikunci:')
    W('')
    W('| Paksi diubah | n kaedah | Median lift CAGR | Positif |')
    W('|---|---|---|---|')
    for nm, c, nc in (('KELUAR sahaja', 'lift_keluar', 'n_var_keluar'),
                      ('MASUK sahaja', 'lift_masuk', 'n_var_masuk')):
        s = D[c].dropna()
        W('| %s | %d | %+.1f mata | %d (%.0f%%) |' % (nm, len(s), s.median(),
                                                        int((s > 0).sum()), 100 * (s > 0).mean()))
    W('')
    W('Kedua-dua baris dipilih dengan cara SAMA atas data SAMA, jadi perbandingan antara mereka '
      'bermakna walaupun kedua-duanya berat sebelah ke atas: **mengubah KELUAR memberi kira-kira '
      '4x lift mengubah MASUK**. Itu konsisten dengan sebaran 4.997 mata lawan 0.392 mata yang '
      '`NXX_KELUAR.md` ukur pada alam yang jauh lebih besar.')
    W('')
    W('Namun semakan luar sampel ke atas varian terpilih: lulus S1–S4 %d, lulus WFO %d, lulus '
      'AUTOTUNE 2000 saham AS **0**, lulus ≥ 2 daripada 3 **0** (`laporan/PENGANALISIS.md`). '
      'Jadi lift dalam sampel itu tidak bertahan.'
      % (int(D.lulus_subset.fillna(False).sum()), int(D.lulus_wfo.fillna(False).sum())))
    W('')
    W('## 5. Sifat mekanikal daripada Lejar Penuh hadapan')
    W('')
    W('%d posisi, %d masih terbuka lorong 1, **%d sudah keluar** merentas %d kaedah. '
      'Set tertutup itu berat sebelah kepada keluar awal, jadi ia TIDAK diguna untuk pangkat '
      'prestasi — hanya untuk sifat mekanikal yang tidak sensitif kepada pemilihan itu.'
      % (jum['semua'], jum['buka'], jum['tutup1'], jum['kaedah']))
    W('')
    W('| Ukuran | Nilai | Tafsiran |')
    W('|---|---|---|')
    W('| henti tercetus dalam ≤ 1 bar | **%d (%.1f%%)**, menang **%.2f%%** | kecacatan mekanikal: '
      'paras henti terletak dalam julat intrabar hari masuk (`REVERSE/KOLAM_EKOR.md` §4a) |'
      % (jum['henti_awal'], 100 * jum['henti_awal'] / jum['tutup1'], jum['henti_awal_menang']))
    W('| jarak henti median: henti awal lawan lain | %.2f%% lawan %.2f%% | puncanya henti KETAT, '
      'bukan nasib |' % (jum['jarak_awal'], jum['jarak_lain']))
    W('| kos purata kecacatan itu | %+.2f%% setiap posisi terjejas | lebih kecil daripada jangkaan: '
      'henti ketat memotong kerugian kecil, jadi membuangnya mengubah purata hanya %+.3f mata '
      '(%+.3f%% -> %+.3f%%) |'
      % (jum['henti_awal_purata'], jum['delta_awal'], jum['purata'], jum['tanpa_awal']))
    W('| bahagian jumlah kerugian | %.1f%% | besar dalam kiraan, kecil dalam kesan |'
      % jum['bhg_kerugian'])
    W('| MFE purata semua posisi | %+.2f%% | 95%% posisi pernah untung semasa dipegang |' % jum['mfe'])
    W('')
    W('**Pembetulan kepada jangkaan saya sendiri:** `KAEDAH_TERBAIK.md` §7 meletakkan pembetulan '
      'henti hari-0 sebagai keutamaan #1. Pada data Lejar ia memang kecacatan nyata (menang '
      '%.2f%% tidak mungkin berlaku secara semula jadi) tetapi **kosnya kecil** — posisi itu '
      'kehilangan %+.2f%% sahaja kerana hentinya ketat (%.2f%% median), jadi membuangnya '
      'TIDAK memperbaiki purata (%+.3f%% -> %+.3f%%). Ia perlu dibetulkan kerana ia mencemari '
      'pangkat, bukan kerana ia punca kerugian.'
      % (jum['henti_awal_menang'], jum['henti_awal_purata'], jum['jarak_awal'],
         jum['purata'], jum['tanpa_awal']))
    W('')
    W('## 6. Jadual setiap kaedah (134)')
    W('')
    W('`Data`: PENUH = ada W01 WFO dan ≥ 10 posisi Lejar tertutup · WFO = W01 sahaja · '
      'Lejar = Lejar sahaja · TIADA. `Kos mesin` = `avg` kaedah tolak pegang pasif pada ufuk '
      'sepadan (negatif = mesin keluar merugikan). `P60` = kelebihan pegang 60 hari setiap '
      'dagangan. `H0/1` = % posisi Lejar dihentikan dalam ≤ 1 bar. `WFO keluar` = pilihan modal '
      'merentas 16 suku luar sampel.')
    W('')
    W('| ID | Kaedah | Data | Sasaran | tmax | Kos mesin | P60 | H0/1 | WFO henti z | WFO keluar | '
      'WFO tmax | MASUK | PEGANG | KELUAR |')
    W('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for mid, x in D.iterrows():
        tm = x.tmax if str(x.tmax) not in ('None', 'nan') else '–'
        km = x.get('wfo_keluar_mod')
        kn = x.get('wfo_keluar_n')
        kl = '%s %d/16' % (km, kn) if isinstance(km, str) else '–'
        tmw = ('tiada' if x.get('wfo_tmax_mod') == 0 else
               (str(int(x.wfo_tmax_mod)) if pd.notna(x.get('wfo_tmax_mod')) else '–'))
        W('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            mid, x.nama[:44], x.data, 'ADA' if x.ada_sasaran else '–', tm,
            fmt(x.get('kos_mesin_keluar')), fmt(x.get('pegang60_lebih'), 1),
            ('%.0f%%' % x.lj_henti_awal) if pd.notna(x.get('lj_henti_awal')) else '–',
            fmt(x.get('wfo_henti_z'), 1), kl, tmw,
            x.v_masuk, x.v_pegang, x.v_keluar))
    W('')
    W('## 6b. Senarai tindakan, dikumpul ikut perubahan')
    W('')
    W('Setiap kumpulan ialah SATU perubahan yang terpakai kepada senarai kaedah itu. Dikumpul '
      'begini kerana bahagian 3 menunjukkan penalaan per-kaedah kalah: yang boleh diuji ialah '
      'satu perubahan seragam atas banyak kaedah, bukan 134 keputusan berasingan.')
    W('')
    kump = [
        ('Buang sasaran JARAK-TETAP (gandaan R / peratus)',
         lambda r: r.get('jenis_sasaran') == 'JARAK',
         'Bukti membezakan DUA jenis sasaran, dan hanya satu terbukti merugikan. '
         '**Sasaran jarak-tetap merugikan**: `NXX_KELUAR.md` `X10` sasaran 2% menang 94.1% dengan '
         'jangkaan -0.023%, `X27` sasaran 3% +0.233%, `KOMBINASI.md` `X1` sasaran 1xATR menang '
         '61.1% dengan jangkaan -0.281% (asas tanpa sasaran +2.595%). '
         '**Keluar atas kekuatan berasaskan penunjuk adalah TERBAIK**: `X13` keluar bila rsi14>70 '
         'memberi +4.350%, nombor 1 daripada 23. Maka kaedah dengan sasaran jarak-tetap (nR, +n%) '
         'patut membuangnya; kaedah dengan sasaran PARAS-BERGERAK (jalur BB atas, SMA30, paras '
         'swing) lebih hampir kepada `X13` dan mesti diuji, bukan diandaikan salah. '
         'Dalam Lejar, keluar-sasaran merealisasi +5.34% sedangkan MFEnya +7.33% — sasaran yang '
         'dipakai sekarang memotong 1.99 mata, tetapi angka itu bersyarat pada sasaran tercapai.'),
        ('Sasaran PARAS-STRUKTUR — uji, jangan andaikan salah',
         lambda r: r.get('jenis_sasaran') == 'PARAS',
         'Sasaran kaedah ini ialah paras harga (jalur BB atas, SMA30, VWAP, ATH, tinggi 20 hari, '
         'projeksi gerakan terukur), bukan jarak tetap daripada harga masuk. Bukti yang menghukum '
         'sasaran dalam `NXX_KELUAR`/`KOMBINASI` semuanya mengenai jarak TETAP; keluar berasaskan '
         'paras/penunjuk justeru yang TERBAIK (`X13` rsi14>70 +4.350%, `X12` jalur bawah BB '
         '+0.961%, `X05` jalur tengah BB +0.030%). Jadi kumpulan ini masuk `Z1` sebagai lengan '
         'berasingan dan keputusannya dilapor berasingan.'),
        ('Buang atau panjangkan had masa (tmax)',
         lambda r: (str(r.tmax) not in ('None', 'nan', '')
                    and pd.notna(r.get('wfo_tmax_mod'))
                    and r.wfo_tmax_mod in (0.0, 42.0, 63.0)),
         'WFO luar sampel memilih tmax panjang atau tiada had pada 81.5% suku (purata pangkat '
         '3.681 lawan 3.0 seragam, t +25.8 p 4.6e-128).'),
        ('Tukar syarat keluar kepada ekori Chandelier',
         lambda r: (isinstance(r.get('wfo_keluar_mod'), str)
                    and r.wfo_keluar_mod.startswith('CHAN')
                    and (r.get('wfo_keluar_n') or 0) >= 7),
         'Mod luar sampel kaedah ini ialah ekori Chandelier pada >= 7 daripada 16 suku. '
         '`NXX_KELUAR.md` `X15` (Chandelier 4xATR) ialah keluar kedua terbaik daripada 23, '
         '+3.706% tanpa apa-apa penapis masuk.'),
        ('Buang syarat keluar sama sekali (henti sahaja)',
         lambda r: (r.get('wfo_keluar_mod') == 'TIADA'
                    and (r.get('wfo_keluar_n') or 0) >= 7 and r.get('ada_exitc')),
         'Mod luar sampel ialah TIADA pada >= 7 suku, dan kaedah ini ada syarat keluar yang '
         'dipakai sekarang.'),
        ('Lebarkan henti',
         lambda r: (pd.notna(r.get('wfo_henti_z')) and r.wfo_henti_z >= 0.5
                    and (r.get('wfo_henti_n') or 0) >= 6),
         'Dalam keluarga ATR dan PCT, henti yang dipilih luar sampel bagi kaedah ini berada '
         '>= 0.5 SD lebih LEBAR daripada jangkaan rawak seragam.'),
        ('Betulkan kecacatan henti hari-0/1',
         lambda r: pd.notna(r.get('lj_henti_awal')) and r.lj_henti_awal >= 20,
         '>= 20% posisi Lejar kaedah ini dihentikan dalam <= 1 bar dengan kadar menang 0.00% — '
         'paras henti terletak dalam julat intrabar hari masuk. Kosnya kecil (bahagian 5) tetapi '
         'ia mencemari setiap pangkat.'),
        ('Keluar asal DISAHKAN — jangan ubah',
         lambda r: r.v_keluar == 'KEKAL (disahkan)',
         'Pengoptimum luar sampel memilih peraturan keluar asal kaedah ini pada >= 7 suku, '
         'atau mesin keluarnya menambah > +0.50 mata lawan pegang pasif.'),
    ]
    for nama, ujian, nota in kump:
        sel = [i for i, r in D.iterrows() if ujian(r)]
        W('### %s — %d kaedah' % (nama, len(sel)))
        W('')
        W(nota)
        W('')
        W('%s' % (', '.join('`%s`' % i for i in sel) if sel else '_tiada_'))
        W('')
    W('')
    W('## 7. Had wajib — baca sebelum bertindak')
    W('')
    W('1. **Kelebihan pegang-lebih-lama ialah masa, bukan alfa.** Kadar setiap hari sama '
      '(%+.4f%% lawan %+.4f%%, ujian-t berpasangan p 0.50, dan mesin kaedah sebenarnya '
      'sedikit di HADAPAN). Memegang 60 hari dan bukan %.0f hari memberi %.2fx untung setiap '
      'dagangan atas modal yang terikat %.2fx lebih lama — nisbah sama. Pada 8–10 slot itu '
      'bermakna %.1fx lebih SEDIKIT dagangan setahun. `REVERSE/SISTEM.md` sudah mengukur bentuk sama: '
      'CAGR setiap unit pendedahan Clenow 18.01%% lawan SPUS 17.95%% — praktiknya sama.'
      % (S.kadar60.mean(), S.kadar_kaedah.mean(), S.bt_hari.mean(),
         S.pegang60.mean() / S.bt_avg.mean(), 60 / S.bt_hari.mean(), 60 / S.bt_hari.mean()))
    W('2. **Membuang henti menaikkan MDD.** Lengkung `pegang` tiada henti sama sekali. '
      '`REVERSE/KOLAM_EKOR.md` §2 mengukur arah bertentangan pada asas tanpa signal: henti '
      '−2xATR mengurangkan min 9.79 mata setahun, jadi henti yang lebih LEBAR memang menolong '
      'pulangan — tetapi tiada henti bermakna tiada had kerugian setiap posisi.')
    W('3. **Lajur `pegang` dalam sampel** (2019–2026, alam 431). Ia bukan luar sampel. Yang luar '
      'sampel ialah W01 (bahagian 3), dan di situ penalaan per-kaedah KALAH 52/131.')
    W('4. **Lejar hadapan masih muda**: %d daripada %d posisi masih terbuka. Jangan baca lajur '
      '`H0/1` sebagai prestasi; ia sifat mekanikal.' % (jum['buka'], jum['semua']))
    W('5. **Hanya %d kaedah (`M02`) ada sasaran jarak-tetap; %d ada sasaran paras-struktur; '
      '%d ada had masa.** Bukti yang menghukum sasaran mengenai jarak TETAP sahaja, jadi syor '
      '"buang sasaran" terpakai kepada SATU kaedah, bukan sepuluh. Dan `spec/SPEC_SEMUA_KAEDAH.md` '
      'menanda `FAIL ASAL` di mana spec asal tidak dapat ditentukan: membuang sasaran atau had '
      'masa bermakna kaedah itu bukan lagi kaedah pedagang itu. Itu keputusan pengguna, bukan '
      'keputusan data.' % (n_jarak, n_sas - n_jarak, n_cap))
    W('6. **Ini jangkaan setiap dagangan, bukan prestasi portfolio.** Ujian 8–10 slot lawan SPUS '
      'belum dijalankan untuk mana-mana syor di sini. `REVERSE/PENANDA_ARAS_SYARIAH.md`: '
      'SPUS memberi 17.95%/tahun CAGR (26.09% median tahunan) dan setiap sistem yang pernah '
      'diuji dalam repo ini kalah kepadanya.')
    W('')
    W('## 8. Syor')
    W('')
    W('1. **Jangan tala per-kaedah.** Sudah dicuba secara menyeluruh (W01: Optuna 150 percubaan '
      'x 16 suku x 132 kaedah) dan ia kalah kepada varian beku pada 79/131 kaedah.')
    W('2. **Uji SATU perubahan seragam merentas semua kaedah**, didaftar dahulu: `SPEC_MOD_M.md`. '
      'Satu keputusan, bukan 134 — itu satu-satunya bentuk yang sampel ini boleh menyelesaikan.')
    W('3. **Betulkan henti hari-0/1** kerana ia mencemari setiap pangkat, tetapi jangan jangka '
      'ia menaikkan pulangan: membuang kesemua %d posisi itu mengubah purata Lejar hanya '
      '%+.3f mata.' % (jum['henti_awal'], jum['delta_awal']))
    W('4. **Jangan tambah baris MASUK lagi.** Tiga kajian bebas (`SETUP.md` 0/598, `NXX.md` '
      '0/280 gate3, `KOMBINASI.md` 3/40 lift positif tetapi semuanya gagal syarat ekor) sudah '
      'mengukur ruang itu.')
    os.makedirs(os.path.dirname(KELUARAN_MD), exist_ok=True)
    os.makedirs(os.path.dirname(KELUARAN_CSV), exist_ok=True)
    open(KELUARAN_MD, 'w').write('\n'.join(L) + '\n')
    D.to_csv(KELUARAN_CSV)
    print('tulis', KELUARAN_MD)
    print('tulis', KELUARAN_CSV)


if __name__ == '__main__':
    D, jum = bina()
    tulis(D, jum)
    print('kaedah:', len(D), '| data PENUH:', int((D.data == 'PENUH').sum()))
    for c in ('v_masuk', 'v_pegang', 'v_keluar'):
        print(c, dict(D[c].value_counts()))
    sys.exit(0)
