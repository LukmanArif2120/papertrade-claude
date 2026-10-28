"""Jejak hadapan portfolio maya 10 slot (sejak 19 Okt 2026; kajian kajian/KAJIAN_PORTFOLIO.md). Rekod sahaja: tiada order,
tiada wang sebenar. Dibina semula sepenuhnya daripada Lejar Penuh pada setiap larian (deterministik, tanpa LLM):
  RS_10    — setiap sesi beli, slot kosong diisi dengan posisi lejar baharu yang RS pasarannya (data/rs/rs_pasaran.csv pada
             tarikh isyarat) tertinggi; RS tiada -> paling akhir.
  RAWAK_10 — kawalan: susunan rawak tetap (benih = tarikh beli), supaya kelebihan RS boleh diukur ke hadapan.
  RISIKO_10 — susunan SAMA seperti RS_10, tetapi saiz berskala kemeruapan: saiz = risiko 1% ekuiti / (4 x ATR14%),
             dihadkan 2%-25%. Dipasangkan dengan RS_10 supaya satu-satunya perbezaan ialah SAIZ (A/B bersih).
             Asal: REVERSE/KEPUTUSAN_1B.md - dalam enam tahun data A02, saiz berskala risiko memperbaiki MDD
             terbaik 6/6 tahun (-27%..-17% -> -10%..-6%) tetapi TIDAK memperbaiki pulangan.
             BUKAN ujian ke hadapan bagi dapatan 1b itu (REVERSE/SPEC_FASA2.md §9.2): lorong ini membeli
             daripada Lejar = isyarat kaedah Mxx, populasi kemasukan yang berbeza sama sekali daripada signal
             REVERSE. Yang diuji di sini: adakah saiz berskala risiko memperbaiki drawdown ATAS ISYARAT Mxx. Nota: jika tunai tidak cukup, saiz dikecilkan ke tunai
             (konvensyen portfolio_slot), bukan dilangkau seperti REVERSE/SPEC_1B.md §2. Kerana saiznya kecil,
             10 slot tidak menghabiskan tunai: lorong ini berpendedahan LEBIH RENDAH daripada RS_10, jadi MDD-nya
             mesti dibaca bersama lajur `tunai`, bukan sebagai perbandingan setara.
Gabungan beku (22 Okt 2026, Fasa 4 item 13; data/analisis/gabungan_beku.json; hanya posisi dibeli >= mula_jejak):
  GABUNGAN_10     — kaedah gabungan beku, kuota slot setiap kaedah (slot tidak terpakai dikongsi), keluar ikut lorong
                    terbaik setiap kaedah (kaedah = keluar lorong 1 Lejar, tunai sesi berikutnya; henti = lorong 2).
  TOP1_10         — kaedah #1 sahaja, 10 slot, lorongnya.
  RAWAK_KAEDAH_10 — kawalan: kaedah rawak beku (bilangan sama, benih tetap), kuota sama, lorong 2.
  Kaedah beku yang Papan Penganalisis tandakan GANTUNG/BERSARA tidak dibeli lagi mulai sesi selepas status dilihat (log
  portfolio_slot/gantung.csv; posisi sedia ada kekal hingga keluar). Susunan dalam sesi = rawak tetap (benih = tarikh beli).
Peraturan sama dengan kajian: 10 slot; saiz = min(tunai, ekuiti semalam x 10%); satu posisi bagi setiap saham; keluar =
lorong 2 lejar (Chandelier tutup 4xATR14, jual pada buka esok; lajur *_henti), direalisasi sebelum belian hari sama;
nilai pasaran = saiz x tutup / harga beli; kos 0.1% setiap belah (seperti enjin). Calon = posisi yang lejar beli (isyarat
100% semua kaedah, seluruh alam Shariah >= USD10; tiada bias kemandirian set 431).
  python3 BacktestShariah2/standard/portfolio_slot.py   -> BacktestShariah2/portfolio_slot/ (dijalankan oleh lejar.yml)
"""
import os, sys, json

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(BS2, 'kod')); sys.path.insert(0, HERE)
from stor import muat, frames_dict  # noqa: E402

LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
STOR = os.environ.get('LEJAR_STOR', os.path.join(BS2, 'data', 'harga', 'stor'))
RS = os.path.join(BS2, 'data', 'rs', 'rs_pasaran.csv')
KELUAR = os.environ.get('PORTFOLIO_SLOT_DIR', os.path.join(BS2, 'portfolio_slot'))
BEKU = os.environ.get('GABUNGAN_BEKU', os.path.join(BS2, 'data', 'analisis', 'gabungan_beku.json'))
PAPAN = os.environ.get('PAPAN_ANALISIS', os.path.join(BS2, 'data', 'analisis', 'papan.json'))
SLOT, W, KOS = 10, 0.10, 0.001
RISIKO, K_ATR, SAIZ_MIN, SAIZ_MAKS = 0.010, 4.0, 0.02, 0.25   # RISIKO_10 (REVERSE/SPEC_1B.md)
PORTFOLIO = {'RS_10': 'RS pasaran tertinggi', 'RAWAK_10': 'Rawak (kawalan)', 'GABUNGAN_10': 'Gabungan kaedah beku',
             'TOP1_10': 'Kaedah #1 sahaja', 'RAWAK_KAEDAH_10': 'Kaedah rawak (kawalan gabungan)',
             'RISIKO_10': 'RS pasaran tertinggi, saiz berskala risiko'}
BEKU_JENIS = ('GABUNGAN_10', 'TOP1_10', 'RAWAK_KAEDAH_10')
L_POSISI = ['saham', 'id_kaedah', 'tarikh_isyarat', 'rs', 'tarikh_beli', 'harga_beli', 'saiz_pct', 'status', 'tarikh_keluar',
            'harga_keluar', 'untung_pct', 'harga_terkini', 'untung_semasa_pct', 'lorong']
L_EKUITI = ['tarikh', 'ekuiti', 'tunai', 'bil_posisi', 'spy']


def calon_lejar():
    """Semua posisi lejar yang dibeli (terbuka + tutup) dengan lorong 2 dan RS pada tarikh isyarat."""
    import lejar
    T, O = lejar.semua_posisi()
    P = pd.concat([T, O], ignore_index=True)
    P = P[(P.tarikh_beli != '') & (P.harga_beli != '')].copy()
    P['harga_beli'] = P.harga_beli.astype(float)
    P['keluar'] = P.keluar_henti.astype(str).str.lower().eq('true') & P.tarikh_keluar_henti.ne('')
    P['harga_keluar_henti'] = pd.to_numeric(P.harga_keluar_henti, errors='coerce')
    P['harga_keluar1'] = pd.to_numeric(P.harga_keluar, errors='coerce')
    P['keluar1'] = P.tarikh_keluar.ne('') & P.harga_keluar1.notna()
    if os.path.exists(RS):
        r = pd.read_csv(RS, usecols=['tarikh', 'ticker', 'rs']).rename(columns={'tarikh': 'tarikh_isyarat', 'ticker': 'saham'})
        P = P.merge(r.drop_duplicates(['tarikh_isyarat', 'saham']), on=['tarikh_isyarat', 'saham'], how='left')
    else:
        P['rs'] = np.nan
    return P.sort_values(['tarikh_beli', 'saham', 'id_kaedah']).reset_index(drop=True)


def susun(G, jenis, tarikh):
    """Susunan calon satu sesi beli. G diisih saham, id_kaedah (tetap)."""
    if jenis in ('RS_10', 'RISIKO_10'):
        return G.assign(_k=G.rs.fillna(-1.0)).sort_values('_k', ascending=False, kind='stable')
    rng = np.random.default_rng(int(tarikh.replace('-', '')))
    return G.iloc[rng.permutation(len(G))]


def konfigurasi(beku):
    """{jenis: dict(mula, kuota {id: slot}, lorong {id: 'kaedah'|'henti'})} daripada gabungan_beku.json; {} jika tiada."""
    if not beku:
        return {}
    K, ruj = beku['kaedah'], beku.get('rujukan', {})
    out = {'GABUNGAN_10': dict(kuota={k['id']: int(k['slot']) for k in K}, lorong={k['id']: k['lorong'] for k in K})}
    t = ruj.get('TOP1_10')
    if t:
        out['TOP1_10'] = dict(kuota={t['id']: SLOT}, lorong={t['id']: t['lorong']})
    r = ruj.get('RAWAK_KAEDAH_10')
    if r:
        out['RAWAK_KAEDAH_10'] = dict(kuota=dict(zip(r['id'], (int(x) for x in r['slot']))), lorong={i: r['lorong'] for i in r['id']})
    for v in out.values():
        v['mula'] = beku['mula_jejak']
    return out


def keluar_pada(p, d, sebelum_beli):
    """(tarikh, harga) keluar posisi p yang direalisasi pada sesi d: lorong 2 (jual buka) sebelum belian hari itu; lorong
    kaedah sebelum belian jika keluar sebelum d, selepas belian jika keluar pada d (harga keluar intrahari/tutup)."""
    if p.get('lorong', 'henti') == 'henti':
        if sebelum_beli and p['keluar'] and p['tarikh_keluar_henti'] <= d:
            return p['tarikh_keluar_henti'], p['harga_keluar_henti']
    elif p.get('keluar1'):
        t = p['tarikh_keluar']
        if (t < d) if sebelum_beli else (t <= d):
            return t, p['harga_keluar1']
    return None


def bina(P, jenis, hari, tutup, cfg=None, gantung=None, atrp=None):
    """hari: senarai tarikh 'YYYY-MM-DD' (sesi dagangan); tutup(saham, tarikh) -> harga tutup atau None. cfg (portfolio beku):
    dict(mula, kuota, lorong); gantung: {id_kaedah: tarikh mula tiada belian}; atrp(saham, tarikh) -> ATR14% (RISIKO_10
    sahaja). Pulang (posisi DataFrame, ekuiti DataFrame)."""
    tunai = eq = 1.0; pos = {}; rekod = []; kurva = []; gantung = gantung or {}
    if cfg:
        P = P[P.id_kaedah.isin(list(cfg['kuota'])) & (P.tarikh_beli >= cfg['mula'])]
        hari = [d for d in hari if d >= cfg['mula']]
    ikut_beli = {d: g for d, g in P.groupby('tarikh_beli')}

    def realisasi(sebelum_beli):
        nonlocal tunai
        for s in list(pos):
            k = keluar_pada(pos[s], d, sebelum_beli)
            if k is None:
                continue
            p = pos.pop(s); t, hk = k
            tunai += p['amaun'] * hk / p['harga_beli'] * (1 - KOS) / (1 + KOS)
            rekod.append(dict(p, status='Keluar', tarikh_keluar=t, harga_keluar=hk,
                              untung_pct=100 * (hk / p['harga_beli'] * (1 - KOS) / (1 + KOS) - 1)))

    def pecahan(r):
        """Pecahan ekuiti bagi satu posisi. RISIKO_10: risiko tetap / (K x ATR%), dihadkan; lain: W tetap."""
        if jenis != 'RISIKO_10':
            return W
        a = atrp(r['saham'], d) if atrp else None
        if a is None or not (a > 0):
            return W                      # ATR tiada -> jatuh balik ke saiz tetap (direkod apa adanya)
        return min(max(RISIKO / (K_ATR * a / 100.0), SAIZ_MIN), SAIZ_MAKS)

    def beli(r):
        nonlocal tunai
        am = min(tunai, eq * pecahan(r))
        if am <= 1e-12:
            return False
        lor = cfg['lorong'][r['id_kaedah']] if cfg else 'henti'
        tunai -= am; pos[r['saham']] = dict(r, amaun=am, saiz_pct=100 * am / eq, lorong=lor)
        return True

    for d in hari:
        realisasi(True)
        if d in ikut_beli:
            G = susun(ikut_beli[d], 'RAWAK_10' if cfg else jenis, d).to_dict('records')
            if cfg:
                G = [r for r in G if not (r['id_kaedah'] in gantung and gantung[r['id_kaedah']] <= d)]
                kini = {}
                for p in pos.values():
                    kini[p['id_kaedah']] = kini.get(p['id_kaedah'], 0) + 1
                for r in G:   # 1: dalam kuota setiap kaedah
                    if len(pos) >= SLOT: break
                    if r['saham'] in pos or kini.get(r['id_kaedah'], 0) >= cfg['kuota'][r['id_kaedah']]: continue
                    if not beli(r): break
                    kini[r['id_kaedah']] = kini.get(r['id_kaedah'], 0) + 1
            for r in G:       # RS/RAWAK: semua; beku: 2 = slot tidak terpakai dikongsi
                if len(pos) >= SLOT: break
                if r['saham'] in pos: continue
                if not beli(r): break
        realisasi(False)
        mv = 0.0
        for s, p in pos.items():
            c = tutup(s, d)
            mv += p['amaun'] * (c / p['harga_beli'] if c else 1.0)
        eq = tunai + mv; kurva.append(dict(tarikh=d, ekuiti=eq, tunai=tunai, bil_posisi=len(pos)))
    akhir = hari[-1] if hari else ''
    for s, p in pos.items():
        c = tutup(s, akhir)
        rekod.append(dict(p, status='Pegang', harga_terkini=c, tarikh_keluar='', harga_keluar=np.nan, untung_pct=np.nan,
                          untung_semasa_pct=100 * (c / p['harga_beli'] - 1) if c else np.nan))
    R = pd.DataFrame(rekod).reindex(columns=L_POSISI)
    return R.sort_values(['tarikh_beli', 'saham']).reset_index(drop=True), pd.DataFrame(kurva, columns=L_EKUITI[:-1])


def muat_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def log_gantung(CFG, sesi, papan=PAPAN, path=None):
    """{id: tarikh mula tiada belian}: log portfolio_slot/gantung.csv (tambah sahaja). Kaedah beku yang papan.json tandakan
    GANTUNG/BERSARA dan belum dilog ditambah dengan tarikh = sesi selepas sesi terakhir (status dilihat selepas sesi itu)."""
    path = path or os.path.join(KELUAR, 'gantung.csv')
    L = pd.read_csv(path, dtype=str) if os.path.exists(path) else pd.DataFrame(columns=['tarikh', 'id_kaedah', 'pantau', 'sebab'])
    beku = {i for c in CFG.values() for i in c['kuota']}
    A = muat_json(papan) or {}
    baru = [dict(tarikh=str((pd.Timestamp(sesi) + pd.offsets.BDay(1)).date()), id_kaedah=r['id'], pantau=r.get('pantau'),
                 sebab=r.get('p_sebab', '')) for r in A.get('rows', [])
            if sesi and r.get('id') in beku and r.get('pantau') in ('GANTUNG', 'BERSARA') and r['id'] not in set(L.id_kaedah)]
    if baru:
        L = pd.concat([L, pd.DataFrame(baru)], ignore_index=True); L.to_csv(path, index=False)
    return dict(zip(L.id_kaedah, L.tarikh))


def mdd(x):
    x = pd.Series(np.r_[1.0, np.asarray(x, float)]); return float((x / x.cummax() - 1).min())   # ekuiti mula = 1 (buka hari pertama)


def ringkasan(hasil, spy_mula, spy_akhir, hari, CFG=None):
    L = [f'# Portfolio maya 10 slot (jejak hadapan; rekod sahaja)', '',
         'Dibina semula daripada Lejar Penuh oleh `standard/portfolio_slot.py`; kajian `kajian/KAJIAN_PORTFOLIO.md`. '
         'Tiada order, tiada wang sebenar. Jangan ubah secara manual.', '',
         f'Tempoh: {hari[0] if hari else "-"} hingga {hari[-1] if hari else "-"} ({len(hari)} sesi). '
         f'SPY dalam tempoh sama: {100 * (spy_akhir / spy_mula - 1):+.2f}%.' if spy_mula else 'SPY: tiada data.', '',
         '| Portfolio | Pulangan % | MDD % | Posisi dipegang | Dagangan keluar | Kadar menang % | Purata untung keluar % |',
         '|---|---|---|---|---|---|---|']
    for k, (R, E) in hasil.items():
        k_ = R[R.status == 'Keluar']; ret = 100 * (E.ekuiti.iloc[-1] - 1) if len(E) else 0.0
        L.append(f'| {k} — {PORTFOLIO[k]} | {ret:+.2f} | {100 * mdd(E.ekuiti):.2f} | {(R.status == "Pegang").sum()} | {len(k_)} | '
                 + (f'{100 * (k_.untung_pct > 0).mean():.0f} | {k_.untung_pct.mean():+.2f} |' if len(k_) else '– | – |'))
    for k, (R, _) in hasil.items():
        H = R[R.status == 'Pegang']
        L += ['', f'## {k} — posisi dipegang', '', '| Saham | Kaedah | RS | Beli | Harga beli | Terkini | Untung % |', '|---|---|---|---|---|---|---|']
        L += [f'| {r.saham} | {r.id_kaedah} | {"" if pd.isna(r.rs) else int(r.rs)} | {r.tarikh_beli} | {r.harga_beli:.2f} | '
              f'{"" if pd.isna(r.harga_terkini) else f"{r.harga_terkini:.2f}"} | {"" if pd.isna(r.untung_semasa_pct) else f"{r.untung_semasa_pct:+.2f}"} |'
              for r in H.itertuples()]
    if CFG:
        L += ['', '## Gabungan beku (jejak hadapan sejak ' + next(iter(CFG.values()))['mula'] + '; data/analisis/gabungan_beku.json)', '',
              '| Portfolio | Kaedah (slot, lorong) | Sesi | Pulangan % | SPY tempoh sama % |', '|---|---|---|---|---|']
        for k, c in CFG.items():
            R, E = hasil.get(k, (None, pd.DataFrame()))
            kl = ', '.join('%s (%s, %s)' % (i, n, c['lorong'][i]) for i, n in c['kuota'].items())   # serasi Python 3.11
            L.append(f"| {k} | {kl} | {len(E)} | "
                     + (f"{100 * (E.ekuiti.iloc[-1] - 1):+.2f} | {100 * (E.spy.iloc[-1] - 1):+.2f} |" if len(E) else '– | – |'))
    L += ['', 'Penilaian adil memerlukan sekurang-kurangnya 6–12 bulan (KAJIAN_PORTFOLIO.md). Kelebihan yang dicari: RS_10 mengatasi '
          'RAWAK_10 dan SPY dengan MDD yang setanding; GABUNGAN_10 mengatasi TOP1_10, RAWAK_KAEDAH_10 dan SPY.',
          '', 'RISIKO_10 dipasangkan dengan RS_10: susunan calon SAMA, hanya saiz berbeza (risiko 1% ekuiti / 4×ATR14%, '
          'dihadkan 2%–25%). Yang dicari di sini ialah MDD lebih baik pada pulangan yang setanding — bukan pulangan lebih '
          'tinggi. Idea saiz itu datang daripada REVERSE/KEPUTUSAN_1B.md (MDD bertambah baik 6/6 tahun, pulangan tidak), '
          'tetapi lorong ini **bukan** ujian ke hadapan dapatan itu: ia membeli daripada Lejar = isyarat kaedah Mxx, '
          'bukan signal REVERSE (lihat REVERSE/SPEC_FASA2.md §9.2). Yang diuji di sini ialah saiz atas isyarat Mxx.',
          '', '**Baca MDD RISIKO_10 bersama lajur `tunai`.** Kerana saham momentum Shariah kebanyakannya ber-ATR tinggi, '
          'saiznya kecil (2%–5%) dan 10 slot tidak menghabiskan tunai: sebahagian daripada MDD yang lebih baik datang '
          'daripada **pendedahan yang lebih rendah**, bukan daripada saiz yang lebih bijak. Perbandingan yang adil ialah '
          'MDD bagi setiap unit pendedahan; lihat `RISIKO_10_ekuiti.csv` lajur `tunai`.']
    return '\n'.join(L) + '\n'


def main():
    P = calon_lejar()
    fr, idx = frames_dict(muat(STOR))
    if 'SPY' not in idx or P.empty:
        print('tiada calon lejar atau SPY: portfolio tidak dibina'); return 0
    spy = idx['SPY'].close
    hari = [d.strftime('%Y-%m-%d') for d in spy.index if d.strftime('%Y-%m-%d') >= P.tarikh_beli.min()]
    cl = {t: g.close for t, g in fr.items()}

    def _atr_pct(g):
        tr = pd.concat([g.high - g.low, (g.high - g.close.shift(1)).abs(),
                        (g.low - g.close.shift(1)).abs()], axis=1).max(axis=1)
        a = tr.ewm(alpha=1 / 14.0, adjust=False, min_periods=14).mean()
        return a / g.close.replace(0, np.nan) * 100.0

    ap = {t: _atr_pct(g) for t, g in fr.items() if {'high', 'low', 'close'} <= set(g.columns)}

    def atrp(s, d):
        a = ap.get(s)
        if a is None:
            return None
        v = a.asof(pd.Timestamp(d))
        return float(v) if pd.notna(v) and v > 0 else None

    def tutup(s, d):
        c = cl.get(s)
        if c is None: return None
        v = c.asof(pd.Timestamp(d)); return float(v) if pd.notna(v) and v > 0 else None

    os.makedirs(KELUAR, exist_ok=True); hasil = {}
    s0 = float(idx['SPY'].open.asof(pd.Timestamp(hari[0]))) if hari else None   # belian pertama pada buka
    CFG = konfigurasi(muat_json(BEKU))
    GT = log_gantung(CFG, hari[-1] if hari else None)
    for k in PORTFOLIO:
        if k in BEKU_JENIS and k not in CFG:
            continue
        R, E = bina(P, k, hari, tutup, CFG.get(k), GT, atrp)
        a = float(idx['SPY'].open.asof(pd.Timestamp(E.tarikh.iloc[0]))) if len(E) else None   # SPY tempoh sama (buka hari pertama)
        E['spy'] = [float(spy.asof(pd.Timestamp(d))) / a for d in E.tarikh] if a else np.nan
        R.to_csv(os.path.join(KELUAR, f'{k}_posisi.csv'), index=False, float_format='%.4f')
        E.to_csv(os.path.join(KELUAR, f'{k}_ekuiti.csv'), index=False, float_format='%.6f')
        hasil[k] = (R, E)
    s1 = float(spy.asof(pd.Timestamp(hari[-1]))) if hari else None
    open(os.path.join(KELUAR, 'RINGKASAN.md'), 'w').write(ringkasan(hasil, s0, s1, hari, CFG))
    json.dump({k: dict(sesi_terakhir=E.tarikh.iloc[-1] if len(E) else None, ekuiti=round(float(E.ekuiti.iloc[-1]), 6) if len(E) else 1.0,
                       dipegang=int((R.status == 'Pegang').sum()), keluar=int((R.status == 'Keluar').sum()))
               for k, (R, E) in hasil.items()}, open(os.path.join(KELUAR, 'status.json'), 'w'), indent=1)
    for k, (R, E) in hasil.items():
        print(k, 'ekuiti %.4f' % (E.ekuiti.iloc[-1] if len(E) else 1.0), 'dipegang', (R.status == 'Pegang').sum(),
              'keluar', (R.status == 'Keluar').sum())
    return 0


if __name__ == '__main__':
    sys.exit(main())
