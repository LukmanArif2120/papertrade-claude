# harian_c.py — Papertrade C harian TANPA LLM (GitHub Actions). Menggantikan rutin Claude 6:02 pagi, 7:47 malam dan
# 9:35 NY (keputusan pengguna 17 Okt 2026: jimat token; peralihan selepas 3 hari dagangan berjalan selari).
# Peraturan: standard/tugasan_v3.md; skema: papertrade/SKEMA.md. Logik dagangan = modul kod/kaedah/Mxx.py + gelung enjin v1.2
# (sama seperti standard/harian_nilai_keluar.py dan standard/lejar.py). Tiada order, tiada wang sebenar.
#
#   python3 harian_c.py malam [--sesi S] [--folder PT] [--stor DIR] [--proses 4] [--masa "YYYY-MM-DD HH:MM"]
#       Langkah selepas tutup bagi sesi S (lalai: bar terakhir stor harga): (1) kemas kini posisi M dan C — betulkan harga
#       beli sementara kepada buka rasmi, semak kesahihan belian (§5.4), keluar lorong 1 (kaedah) dan lorong 2
#       (keluar_lorong.py), harga terkini; (2) imbas 134 kaedah — senarai_beli.csv, watchlist.csv, rekod isyarat.
#   python3 harian_c.py gred [--tarikh D] [--tanpa-tarik]
#       Gred S/I/R/Q/P senarai_beli + watchlist (data pemangkin Yahoo/Nasdaq daripada pemangkin_actions.py).
#   python3 harian_c.py beli [--tarikh D] [--buka FAIL.csv]
#       Belian maya pada harga buka (yfinance semasa pasaran dibuka, atau fail ticker,open[,volume]). Rekod ke claude_N.csv.
#   python3 harian_c.py db --keluar DIR
#       Dokumen db dashboard (papertrade/*, prestasi/*, harian/status) + fail batch untuk ArtifactData (file_path).
# Status larian: papertrade/status_harian.json (larian berulang bagi sesi/tarikh yang sama dilangkau: idempoten).
import argparse, csv, glob, importlib, json, os, re, shutil, subprocess, sys, tempfile, time
from collections import Counter
from multiprocessing import get_context

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
KOD = os.path.join(BS2, 'kod')
sys.path.insert(0, KOD); sys.path.insert(0, HERE)
import enjin  # noqa: E402
from stor import muat, frames_dict, LAJ  # noqa: E402
import keluar_lorong as KL  # noqa: E402
import sahkan as SH  # noqa: E402
import ambil_alih as AA  # noqa: E402

PT = os.path.join(BS2, 'papertrade')
STOR = os.path.join(BS2, 'data', 'harga', 'stor')
UNIV = os.path.join(BS2, 'data', 'harga', 'univ.txt')
ISYARAT = os.path.join(BS2, 'data', 'isyarat')
PEMANGKIN = os.path.join(BS2, 'data', 'pemangkin')
LOG_IMBAS = os.path.join(HERE, 'binaan_v2_log.md')
LOG_HARIAN = os.path.join(HERE, 'binaan_v2_log_tambahan.md')

HARGA_MIN = 10.0           # tugasan_v3 §3: harga >= USD10
MAKS_KAEDAH = 10           # isyarat baharu setiap kaedah setiap imbasan (431 dahulu, kemudian rank); calon watchlist di luar had
MAKS_WATCH = 5             # calon Hampir Signal setiap kaedah
# Kaedah isyarat MINGGUAN (tugasan_v3 §3a): sah hanya jika sesi isyarat = hari dagangan terakhir minggu
MINGGUAN = {'M37', 'M38', 'M41', 'M50', 'M52', 'M64', 'M78'}
BEZA_HARGA_MAKS = KL.BEZA_HARGA_MAKS   # buka stor hari beli lawan harga_beli > 15% -> data tidak sepadan (split), tidak dinilai
NOTA_HENTI = {'M06': 'max(0.99 x low 15 hari, 0.92 x buka masuk)', 'M08': '0.99 x low terendah 6 hari', 'M52': '0.60 x buka masuk'}
SENARAI_LAJUR = ['saham', 'nama', 'kaedah', 'sektor', 'industri', 'pct_dipenuhi', 'harga_rujukan', 'henti', 'nota_henti',
                 'buka_maks', 'sasaran', 'destinasi', 'sumber', 'tarikh_isyarat', 'tarikh_imbasan', 'asal', 'belian_ke']
WATCH_LAJUR = ['Saham', 'Nama', 'Kaedah', 'Sektor', 'Industri', 'Harga', '% hampir', 'Pencetus', 'Keadaan semasa',
               'Syarat belum cukup', 'Syarat dipenuhi', 'Paras pencetus', 'Jarak %', 'Tarikh masuk watchlist',
               'Hari dalam watchlist', 'Skor', 'Set', 'tarikh_data', 'dibina']
GRED_LAJUR = ['sektor_us', 'industri_us', 'gred_sektor', 'skor_sektor', 'gred_industri', 'skor_industri', 'rs_rating', 'gred_rs',
              'rs_sah', 'rs_tanda', 'rs_industri', 'rs_sumber', 'gred_pemangkin', 'mata_pemangkin', 'pemangkin', 'pemangkin_url', 'tarikh_earnings', 'hari_ke_earnings',
              'sumber_earnings', 'gred_qr', 'gred_keseluruhan', 'gred_pada',
              'gred_kewangan', 'kewangan_ringkas', 'kewangan_tempoh']   # kewangan_butiran: senarai_beli/watchlist sahaja (gred.py)


# ---------------------------------------------------------------- bantu
def r4(x):
    return None if x is None or not np.isfinite(float(x)) else round(float(x), 4)


def r2(x):
    return None if x is None or not np.isfinite(float(x)) else round(float(x), 2)


def s(x):
    """Nilai -> teks CSV ('' bagi None/NaN)."""
    if x is None:
        return ''
    if isinstance(x, (bool, np.bool_)):
        return 'True' if x else 'False'
    if isinstance(x, (float, np.floating)):
        if not np.isfinite(x):
            return ''
        return repr(float(x)) if abs(x) < 1e15 else str(x)
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    return str(x)


def nombor(v):
    try:
        f = float(v)
        return f if np.isfinite(f) else None
    except (TypeError, ValueError):
        return None


benar = SH.benar
hb = KL.hb      # '2026-10-16' -> '16 Okt'


def kini(masa=None):
    """Masa larian (MYT). --masa 'YYYY-MM-DD HH:MM' untuk ulang tayang."""
    if masa:
        return pd.Timestamp(masa).tz_localize('Asia/Kuala_Lumpur')
    return pd.Timestamp.now(tz='Asia/Kuala_Lumpur')


def teks_masa(t):
    return t.strftime('%Y-%m-%d %H:%M') + ' MYT'


def kal():
    import exchange_calendars as xc
    return xc.get_calendar('XNYS')


def akhir_minggu(S):
    """True jika sesi S ialah hari dagangan terakhir minggunya (kalendar NYSE)."""
    S = pd.Timestamp(S)
    try:
        n = kal().next_session(S)
    except Exception:
        n = S + pd.offsets.BDay(1)
    return tuple(n.isocalendar()[:2]) != tuple(S.isocalendar()[:2])


def nombor_kaedah(mid):
    try:
        return int(str(mid)[1:])
    except ValueError:
        return 10 ** 6


def senarai_kaedah():
    f = glob.glob(os.path.join(KOD, 'kaedah', 'M*.py'))
    return sorted((os.path.basename(x)[:-3] for x in f), key=nombor_kaedah)


def fail_posisi(folder):
    """moomoo.csv dahulu, kemudian claude.csv, claude_2.csv … ikut nombor."""
    c = sorted(glob.glob(os.path.join(folder, 'claude*.csv')), key=lambda p: KL_nombor(p))
    m = os.path.join(folder, 'moomoo.csv')
    return ([m] if os.path.exists(m) else []) + c


def KL_nombor(p):
    m = re.fullmatch(r'claude(?:_(\d+))?\.csv', os.path.basename(p))
    return (int(m.group(1)) if m and m.group(1) else 1) if m else 10 ** 6


def status_baca(folder):
    p = os.path.join(folder, 'status_harian.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def status_tulis(folder, st):
    with open(os.path.join(folder, 'status_harian.json'), 'w', encoding='utf-8') as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


def tambah_log(path, teks):
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + teks.rstrip() + '\n')


# ---------------------------------------------------------------- stor harga
def stor_hingga(stor, S, kerja):
    """Folder stor harga dengan bar <= S sahaja (salinan dipotong dalam `kerja` jika stor ada bar selepas S)."""
    fr = muat(stor)
    Si = int(pd.Timestamp(S).strftime('%Y%m%d'))
    if all(int(d.date.max()) <= Si for d in fr.values()):
        return stor
    out = os.path.join(kerja, 'stor_S'); os.makedirs(out, exist_ok=True)
    for nm, d in fr.items():
        d[d.date <= Si][LAJ].to_csv(os.path.join(out, nm), index=False, float_format='%.6g')
    return out


# ---------------------------------------------------------------- sektor, industri, nama
def peta_saham(folder):
    """saham -> (sektor, industri) dan saham -> nama, daripada semua fail papertrade (nilai terkini menang) + cache
    papertrade/sektor_saham.csv. Sandaran: industri Moomoo (peta_industri.csv) dengan sektor Morningstar."""
    sek, nama = {}, {}
    u = os.path.join(BS2, 'data', 'harga', 'univ.csv')     # skrin Shariah Moomoo mingguan (kod/parse_screen.py)
    if os.path.exists(u):
        for r in csv.DictReader(open(u, newline='', encoding='utf-8')):
            if r.get('nama'):
                nama[r['ticker']] = r['nama']
    p = os.path.join(folder, 'sektor_saham.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, newline='', encoding='utf-8')):
            if r.get('sektor') and r.get('industri'):
                sek[r['ticker']] = (r['sektor'], r['industri'])
            if r.get('nama'):
                nama[r['ticker']] = r['nama']
    for f in fail_posisi(folder) + [os.path.join(folder, 'senarai_beli.csv'), os.path.join(folder, 'watchlist.csv')]:
        if not os.path.exists(f):
            continue
        for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
            t = r.get('saham') or r.get('Saham')
            se, ind = r.get('sektor') or r.get('Sektor'), r.get('industri') or r.get('Industri')
            if t and not SH.kosong(se) and not SH.kosong(ind) and se != 'Tiada data':
                sek[t] = (se, ind)
            n = r.get('nama') or r.get('Nama')
            if t and n:
                nama[t] = n
    return sek, nama


def peta_sandaran(folder):
    p = os.path.join(folder, 'peta_industri.csv')
    if not os.path.exists(p):
        return {}
    from sektor_pasaran import SEKTOR_INDUSTRI
    out = {}
    for r in csv.DictReader(open(p, newline='', encoding='utf-8')):
        su = SEKTOR_INDUSTRI.get(r['industri'])
        if su and r['ticker'] not in out:
            out[r['ticker']] = (su, r['industri'])
    return out


def cari_sektor(t, sek, sandaran):
    return sek.get(t) or sandaran.get(t) or ('Tiada data', 'Tiada data')


# ---------------------------------------------------------------- kerja setiap kaedah (proses anak)
FR = {}
IDX = {}


def _bar_isyarat(g, ti):
    try:
        return g.index.get_loc(pd.Timestamp(ti))
    except KeyError:
        return None


def nilai_keluar(g, i, tmax):
    """Gelung enjin v1.2 bagi satu dagangan dari bar isyarat i (sama dengan harian_nilai_keluar.keluar).
    Pulang None (pegang), {'menunggu': tarikh isyarat keluar} atau {'t', 'p', 'why'}."""
    ix = g.index; n = len(g)
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    st = g['stop'].astype(float).values; tg = g['tgt'].astype(float).values
    ex = g['exitc'].fillna(False).astype(bool).values
    sp = st[i] if not np.isnan(st[i]) else -np.inf
    j = i + 1
    while j < n:
        tgt = tg[j - 1] if j > i + 1 else np.nan
        if j > i + 1 and o[j] <= sp:
            return dict(t=str(ix[j].date()), p=float(o[j]), why='kena henti (buka bawah henti)')
        if l[j] <= sp:
            return dict(t=str(ix[j].date()), p=float(sp), why='kena henti')
        if not np.isnan(tgt):
            if j > i + 1 and o[j] >= tgt:
                return dict(t=str(ix[j].date()), p=float(o[j]), why='capai sasaran (buka atas sasaran)')
            if h[j] >= tgt:
                return dict(t=str(ix[j].date()), p=float(tgt), why='capai sasaran')
        if ex[j]:
            if j + 1 < n:
                return dict(t=str(ix[j + 1].date()), p=float(o[j + 1]), why=f'isyarat keluar kaedah {hb(ix[j])}')
            return dict(menunggu=str(ix[j].date()))
        if tmax and (j - i) >= tmax:
            return dict(t=str(ix[j].date()), p=float(c[j]), why=f'had masa {tmax} hari')
        j += 1
    return None


def maklumat_buka(mid, g):
    """buka_maks bagi kaedah yang membatalkan masuk jika buka terlalu tinggi (tugasan_v3 §3b), bar terakhir."""
    try:
        if mid == 'M06':
            return r4(1.05 * float(g['_piv'].iloc[-1]))
        if mid == 'M08':
            return r4(1.05 * float(g['_s20'].iloc[-1]))
        if mid == 'M19':
            return r4(float(g['_RH20'].iloc[-1]))
        if mid == 'M20':
            return r4(float(g['tgt'].iloc[-1]))
    except (KeyError, TypeError, ValueError):
        return None
    return None


def kerja(arg):
    """Satu kaedah atas data <= S: keluar & kesahihan posisi, isyarat bar S, calon hampir bar S."""
    mid, S, posisi, layak, a431, imbas = arg
    t0 = time.time(); St = pd.Timestamp(S)
    out = dict(mid=mid, ralat=None, posisi={}, isyarat=[], hampir=[], s=0)
    try:
        m = importlib.import_module(f'kaedah.{mid}')
    except Exception as e:
        out['ralat'] = f'import: {type(e).__name__}: {e}'; return out
    perlu = getattr(m, 'PERLU_BAR', 260); silang = bool(getattr(m, 'SILANG', False)); tmax = getattr(m, 'TMAX', None) or 0
    pos_t = {p['saham'] for p in posisi}
    fr = {}
    for t, g in FR.items():
        if len(g) >= 60 or (not silang and t in pos_t and len(g) >= 2):
            fr[t] = g.copy()
    try:
        m.sedia(fr, {k: v.copy() for k, v in IDX.items()})
    except Exception as e:
        out['ralat'] = f'sedia: {type(e).__name__}: {e}'; return out
    for g in fr.values():
        enjin.siap(g)
    # 1) posisi: keluar lorong 1 dan kesahihan belian
    for p in posisi:
        g = fr.get(p['saham'])
        if g is None:
            out['posisi'][p['k']] = dict(nota='tiada data harga'); continue
        i = _bar_isyarat(g, p['ti'])
        if i is None:
            out['posisi'][p['k']] = dict(nota=f"bar isyarat {p['ti']} tiada dalam stor"); continue
        sp = float(g['stop'].iloc[i]); r = dict(stop_i=r4(sp) if np.isfinite(sp) else None)
        if p.get('semak'):
            tb = pd.Timestamp(p['tarikh_beli'])
            ok_bar = i + 1 < len(g) and g.index[i + 1] == tb
            r['sah'] = dict(bar=bool(ok_bar), sig=bool(g['sig'].iloc[i]),
                            buka=r4(float(g.open.iloc[i + 1])) if ok_bar else None,
                            vol=float(g.volume.iloc[i + 1]) if ok_bar else None)
        r['x'] = nilai_keluar(g, i, tmax)
        out['posisi'][p['k']] = r
    if not imbas:
        out['s'] = round(time.time() - t0, 1); return out
    # 2) isyarat bar S dan 3) calon hampir (watchlist)
    ada_hampir = hasattr(m, 'hampir')
    for t, g in fr.items():
        if g.index[-1] != St or t not in layak or (not silang and len(g) < perlu):
            continue
        try:
            sig = bool(g['sig'].iloc[-1])
        except Exception:
            continue
        if sig:
            rk = nombor(g['rank'].iloc[-1])
            out['isyarat'].append(dict(saham=t, rank=r4(rk) if rk is not None else None, henti=r4(nombor(g['stop'].iloc[-1])),
                                       sasaran=r4(nombor(g['tgt'].iloc[-1])), tutup=r4(float(g.close.iloc[-1])),
                                       sumber='431' if t in a431 else 'lain', buka_maks=maklumat_buka(mid, g)))
        elif ada_hampir:
            try:
                h = m.hampir(g, IDX)
            except Exception:
                h = None
            if h:
                out['hampir'].append(dict(saham=t, sumber='431' if t in a431 else 'lain', sebab=str(h.get('sebab', '')),
                                          syarat_beli=str(h.get('syarat_beli', '')), skor=r4(nombor(h.get('skor')) or 0),
                                          harga=r4(float(g.close.iloc[-1])), pencetus=h.get('pencetus') or '',
                                          paras=r4(nombor(h.get('paras'))), jarak_pct=r2(nombor(h.get('jarak_pct'))),
                                          syarat_dipenuhi=h.get('syarat_dipenuhi') or ''))
    out['s'] = round(time.time() - t0, 1)
    return out


def jalan_kaedah(stor_dir, S, posisi, layak, a431, imbas, proses):
    """Jalankan semua kaedah (selari). posisi: {mid: [ {k, saham, ti, tarikh_beli, semak} ]}."""
    global FR, IDX
    FR, IDX = frames_dict(muat(stor_dir))
    St = pd.Timestamp(S)
    FR = {t: g[g.index <= St] for t, g in FR.items()}
    IDX = {t: g[g.index <= St] for t, g in IDX.items()}
    kaedah = senarai_kaedah()
    tambahan = sorted(set(posisi) - set(kaedah), key=nombor_kaedah)   # id_kaedah tanpa modul (cth. luar) tidak dinilai
    args = [(mid, S, posisi.get(mid, []), layak, a431, imbas) for mid in kaedah]
    if proses > 1:
        with get_context('fork').Pool(proses) as pool:
            hasil = pool.map(kerja, args, chunksize=1)
    else:
        hasil = [kerja(a) for a in args]
    return {h['mid']: h for h in hasil}, tambahan


# ---------------------------------------------------------------- KEMAS: kemas kini posisi bagi sesi S
def status_pegang(r):
    base = r.get('isyarat_keluar') or ''
    if base.startswith('Pegang (luar') or base.startswith('Pegang (warisan'):
        return base
    p = []
    h, t = nombor(r.get('henti')), nombor(r.get('sasaran'))
    if h:
        p.append(f'henti {h:.2f}')
    if t:
        p.append(f'sasaran {t:.2f}')
    return 'Pegang' + (f' ({", ".join(p)})' if p else '')


def sesi_list():
    return list(IDX['SPY'].index) if 'SPY' in IDX else []


def hari_antara(beli, sampai, SES):
    b, s_ = pd.Timestamp(beli), pd.Timestamp(sampai)
    return int(sum(1 for x in SES if b < x <= s_))


def sesi_sebelum(d, SES):
    d = pd.Timestamp(d); x = [s_ for s_ in SES if s_ < d]
    return str(x[-1].date()) if x else None


def sementara(r):
    return (r.get('nota') or '').startswith('buka sementara') or 'buka sementara' in (r.get('nota') or '')[:40]


def kumpul_posisi(folder, S, SES):
    """Senarai kerja posisi bagi setiap kaedah. Kunci k = '<fail>#<baris>'."""
    kerja_ = {}
    for p in fail_posisi(folder):
        lajur, rows = SH.baca(p)
        for n, r in enumerate(rows):
            if benar(r.get('tidak_dibeli')) or not r.get('tarikh_beli') or nombor(r.get('harga_beli')) is None:
                continue
            mid = r.get('id_kaedah') or r.get('kaedah') or ''
            if not mid.startswith('M') or r.get('sumber') == 'luar':
                continue
            if benar(r.get('keluar')) and not sementara(r):
                continue      # lorong 1 sudah keluar dan dibekukan (lorong 2: keluar_lorong.py)
            if r['tarikh_beli'] > str(pd.Timestamp(S).date()):
                continue
            ti = r.get('tarikh_isyarat') or sesi_sebelum(r['tarikh_beli'], SES)
            if not ti:
                continue
            kerja_.setdefault(mid, []).append(dict(k=f'{os.path.basename(p)}#{n}', saham=r['saham'], ti=ti,
                                                    tarikh_beli=r['tarikh_beli'], semak=sementara(r)))
    return kerja_


def kemas(folder, stor_dir, S, hasil, masa, ringkas):
    """Tulis keputusan kerja kaedah ke fail posisi (lorong 1, harga, kesahihan); kemudian lorong 2 (keluar_lorong.py)."""
    St = pd.Timestamp(S); Ss = str(St.date()); SES = [x for x in sesi_list() if x <= St]
    bar = {t: g for t, g in FR.items()}
    sek, _ = peta_saham(folder); sand = peta_sandaran(folder)
    dikesan = teks_masa(masa)
    hasil_pos = {}
    for h in hasil.values():
        hasil_pos.update(h['posisi'])
    keluar_baru = {'M': Counter(), 'C': Counter()}
    menunggu, betul, betul_besar, tidak_dibeli, nota = 0, 0, 0, [], []
    for p in fail_posisi(folder):
        nm = os.path.basename(p); ak = 'M' if nm == 'moomoo.csv' else 'C'
        lajur, rows = SH.baca(p)
        for n, r in enumerate(rows):
            if SH.kosong(r.get('sektor')) or SH.kosong(r.get('industri')):
                r['sektor'], r['industri'] = cari_sektor(r['saham'], sek, sand)
            if benar(r.get('tidak_dibeli')):
                continue
            hb_ = nombor(r.get('harga_beli'))
            if hb_ is None or not r.get('tarikh_beli') or r['tarikh_beli'] > Ss:
                continue
            g = bar.get(r['saham'])
            res = hasil_pos.get(f'{nm}#{n}')
            tb = pd.Timestamp(r['tarikh_beli'])
            if g is not None and tb in g.index and not sementara(r) and abs(float(g.open.loc[tb]) / hb_ - 1) > BEZA_HARGA_MAKS:
                nota.append(f"{ak} {r['saham']} {r['kaedah']}: buka stor {g.open.loc[tb]:.2f} lawan harga_beli {hb_} "
                            f"(> {BEZA_HARGA_MAKS:.0%}; split/data tidak sepadan) — tidak dinilai")
                continue
            # (a) harga beli sementara -> buka rasmi bar harian hari beli (tugasan_v3 §5.2)
            if sementara(r) and not benar(r.get('keluar')) and g is not None and tb in g.index:
                ob = float(g.open.loc[pd.Timestamp(r['tarikh_beli'])])
                if ob > 0:
                    if abs(ob / hb_ - 1) > 1e-9:
                        betul += 1
                        betul_besar += abs(ob / hb_ - 1) > 0.005
                    hb_ = r4(ob); r['harga_beli'] = s(hb_)
                    ke = re.search(r'belian ke-\d+', r.get('nota') or '')
                    r['nota'] = (ke.group(0) + '; ' if ke else '') + f'buka rasmi {hb(r["tarikh_beli"])} (bar harian; disahkan {dikesan})'
                    # (b) kesahihan belian (§5.4): sig hari isyarat masih benar apabila bar hari beli diketahui; buka > henti
                    sah = (res or {}).get('sah')
                    sebab = None
                    if sah:
                        if not sah['bar']:
                            sebab = f"tiada bar dagangan pada {r['tarikh_beli']}"
                        elif not (sah['buka'] and sah['buka'] > 0 and (sah['vol'] or 0) > 0):
                            sebab = f"tiada dagangan pada {r['tarikh_beli']}"
                        elif not sah['sig']:
                            sebab = f"sedia() sig=False pada {r.get('tarikh_isyarat') or '?'} (disemak dengan bar hingga {Ss})"
                        elif res.get('stop_i') is not None and sah['buka'] <= res['stop_i']:
                            sebab = f"buka {sah['buka']} <= henti {res['stop_i']}"
                    if sebab:
                        tidak_dibeli.append(f"{r['saham']} {r['kaedah']}")
                        r.update(tidak_dibeli='True', tidak_sah='True', sebab_tidak_sah=sebab, harga_buka_rujukan=s(hb_),
                                 tarikh_beli_dirancang=r['tarikh_beli'], harga_beli='', harga_terkini='', untung_pct='', hari='',
                                 isyarat_keluar='TIDAK DIBELI', keluar='False', tarikh_keluar='', harga_keluar='',
                                 untung_akhir_pct='')
                        for c in KL.LAJUR_LORONG:
                            if c in r:
                                r[c] = ''
                        continue
                    if res and res.get('stop_i') is not None:
                        r['henti'] = s(res['stop_i'])
            if benar(r.get('keluar')):
                continue          # lorong 1 dibekukan
            # (c) keluar lorong 1
            x = (res or {}).get('x')
            if res and res.get('nota'):
                nota.append(f"{ak} {r['saham']} {r['kaedah']}: {res['nota']}")
            if x and x.get('t'):
                r['keluar'] = 'True'; r['tarikh_keluar'] = x['t']; r['harga_keluar'] = s(r4(x['p']))
                r['untung_akhir_pct'] = s(r2((x['p'] / hb_ - 1) * 100))
                r['harga_terkini'] = r['harga_keluar']; r['untung_pct'] = r['untung_akhir_pct']
                r['hari'] = s(hari_antara(r['tarikh_beli'], x['t'], SES))
                r['isyarat_keluar'] = f"Keluar: {x['why']} ({hb(x['t'])} @ {x['p']:.2f})"
                r['dikesan'] = dikesan
                w = x['why']
                keluar_baru[ak]['henti' if w.startswith('kena henti') else 'sasaran' if w.startswith('capai') else
                                'isyarat' if w.startswith('isyarat') else 'masa'] += 1
                continue
            # (d) masih dipegang: harga tutup terkini
            if g is not None and g.index[-1] == St:
                c = float(g.close.iloc[-1]); r['harga_terkini'] = s(r4(c)); r['untung_pct'] = s(r2((c / hb_ - 1) * 100))
            elif g is not None:
                nota.append(f"{ak} {r['saham']} {r['kaedah']}: tiada bar {Ss} (harga terkini {g.index[-1].date()})")
            r['hari'] = s(hari_antara(r['tarikh_beli'], Ss, SES))
            if x and x.get('menunggu'):
                r['isyarat_keluar'] = f"Isyarat keluar {hb(x['menunggu'])} — jual pada buka esok (menunggu)"
                menunggu += 1
            else:
                r['isyarat_keluar'] = status_pegang(r)
        SH.tulis(p, lajur, rows)
    # lorong 2 (pegang selagi naik) + tutup_semua
    KL.main(['--stor', stor_dir, '--folder', folder])
    ringkas.update(keluar_baru={k: dict(v) for k, v in keluar_baru.items()},
                   keluar_baru_jumlah={k: sum(v.values()) for k, v in keluar_baru.items()}, menunggu=menunggu,
                   harga_beli_dibetulkan=betul, harga_beli_beza_besar=int(betul_besar), tidak_dibeli=tidak_dibeli,
                   nota=nota[:40])


# ---------------------------------------------------------------- IMBAS: senarai beli + watchlist bagi sesi S
def layak_imbas(univ_path):
    if not os.path.exists(univ_path):
        return None
    u = {x.strip().replace('US.', '') for x in open(univ_path) if x.strip()}
    out = set()
    for t in u:
        g = FR.get(t)
        if g is not None and len(g) and float(g.close.iloc[-1]) >= HARGA_MIN:
            out.add(t)
    return out


def pct_hampir(jarak):
    return round(min(99.9, max(90.0, 100 - float(jarak))), 1)


def imbas(folder, S, hasil, masa, ringkas, isyarat_dir):
    from scanner import pegangan_c, simpan_isyarat
    St = pd.Timestamp(S); Ss = str(St.date()); SES = [x for x in sesi_list() if x <= St]
    tarikh_imbasan = str(masa.date())
    dibina = teks_masa(masa)
    sek, nama = peta_saham(folder); sand = peta_sandaran(folder)
    buka_c, bil_c = pegangan_c(folder)
    p_watch = os.path.join(folder, 'watchlist.csv')
    w_lajur, w_lama = SH.baca(p_watch) if os.path.exists(p_watch) else ([], [])
    lama = {(r['Saham'], r['Kaedah']): r for r in w_lama}
    minggu_akhir = akhir_minggu(St)
    aa = AA.tapis(FR, St)   # saham sedang diambil alih (kod/ambil_alih.py): isyarat palsu, tidak dibeli, tiada watchlist
    senarai, watch, rekod = [], [], []
    tolak = Counter()
    for mid in senarai_kaedah():
        h = hasil.get(mid) or {}
        sig = sorted(h.get('isyarat', []), key=lambda x: (x['sumber'] != '431', -(x['rank'] if x['rank'] is not None else -1e9)))
        dirancang = set()
        if mid in MINGGUAN and not minggu_akhir:
            if sig:
                tolak['mingguan'] += len(sig)
            sig_ok = []
        else:
            sig_ok = sig
        # 10 teratas (431 dahulu, kemudian rank) daripada semua isyarat yang tidak dipegang; calon watchlist yang kini
        # lengkap tetapi di luar 10 teratas ditambah di luar had (sama seperti imbasan malam Claude 16 Okt 2026)
        calon = []
        for x in sig_ok:
            if (mid, x['saham']) in buka_c:
                tolak['dipegang'] += 1; continue
            if x['saham'] in aa:
                tolak['ambil_alih'] += 1; continue
            calon.append(x)
        atas = calon[:MAKS_KAEDAH]
        luar = [x for x in calon[MAKS_KAEDAH:] if (x['saham'], mid) in lama]
        tolak['had'] += len(calon) - len(atas) - len(luar)
        pilih = [(x, 'watchlist' if (x['saham'], mid) in lama else 'isyarat') for x in atas + luar]
        for x, asal in pilih:
            t = x['saham']; se, ind = cari_sektor(t, sek, sand)
            senarai.append(dict(saham=t, nama=nama.get(t, ''), kaedah=mid, sektor=se, industri=ind, pct_dipenuhi=100,
                                harga_rujukan=x['tutup'], henti=x['henti'], nota_henti=NOTA_HENTI.get(mid, ''),
                                buka_maks=x['buka_maks'], sasaran=x['sasaran'], destinasi='Claude', sumber=x['sumber'],
                                tarikh_isyarat=Ss, tarikh_imbasan=tarikh_imbasan, asal=asal,
                                belian_ke=bil_c.get((mid, t), 0) + 1))
            dirancang.add(t)
        for x in sig:
            rekod.append(dict(tarikh_data=Ss, kaedah=mid, saham=x['saham'], rank=x['rank'], henti=x['henti'],
                              sasaran=x['sasaran'], tutup=x['tutup'], sumber=x['sumber'], dirancang=x['saham'] in dirancang))
        # watchlist: calon sedia ada yang masih layak dahulu, kemudian calon baharu (431 dahulu, kemudian skor); maks 5
        sig_t = {x['saham'] for x in sig}
        # % hampir = 100 - jarak pencetus, jadi calon tanpa jarak boleh diukur (pencetus corak, jarak_pct None) tidak
        # dimasukkan — sama seperti watchlist rutin Claude (tiada baris tanpa jarak sejak 14 Okt 2026)
        cand = [c for c in h.get('hampir', []) if (mid, c['saham']) not in buka_c and c['saham'] not in sig_t
                and c['jarak_pct'] is not None and c['saham'] not in aa]
        cand.sort(key=lambda c: ((c['saham'], mid) not in lama, c['sumber'] != '431', -(c['skor'] or 0), c['saham']))
        for c in cand[:MAKS_WATCH]:
            t = c['saham']; w0 = lama.get((t, mid))
            masuk = w0['Tarikh masuk watchlist'] if w0 and w0.get('Tarikh masuk watchlist') else Ss
            se, ind = cari_sektor(t, sek, sand)
            w = {'Saham': t, 'Nama': nama.get(t, (w0 or {}).get('Nama', '')), 'Kaedah': mid, 'Sektor': se, 'Industri': ind,
                 'Harga': c['harga'], '% hampir': pct_hampir(c['jarak_pct']), 'Pencetus': c['pencetus'],
                 'Keadaan semasa': c['sebab'], 'Syarat belum cukup': c['syarat_beli'], 'Syarat dipenuhi': c['syarat_dipenuhi'],
                 'Paras pencetus': c['paras'], 'Jarak %': c['jarak_pct'], 'Tarikh masuk watchlist': masuk,
                 'Hari dalam watchlist': hari_antara(masuk, Ss, SES), 'Skor': c['skor'], 'Set': c['sumber'],
                 'tarikh_data': Ss, 'dibina': dibina}
            if w0:   # gred hari sebelumnya dibawa sehingga gred.py dijalankan semula
                w.update({k: w0.get(k, '') for k in GRED_LAJUR})
            watch.append(w)
    # tulis
    p = os.path.join(folder, 'senarai_beli.csv')
    SH.tulis(p, SENARAI_LAJUR + GRED_LAJUR, [{k: s(v) for k, v in r.items()} for r in senarai])
    SH.tulis(p_watch, WATCH_LAJUR + GRED_LAJUR, [{k: s(v) for k, v in r.items()} for r in watch])
    fail_isy = simpan_isyarat(rekod, isyarat_dir, Ss, 'malam') if isyarat_dir else None
    wk = {(w['Saham'], w['Kaedah']) for w in watch}
    ringkas.update(senarai_beli=len(senarai), saham_unik=len({r['saham'] for r in senarai}),
                   kaedah=len({r['kaedah'] for r in senarai}), belian_semula=sum(r['belian_ke'] >= 2 for r in senarai),
                   dari_watchlist=sum(r['asal'] == 'watchlist' for r in senarai), isyarat=len(rekod),
                   ditolak=dict(tolak), ambil_alih=sorted(aa), watchlist=len(watch), watchlist_baharu=len(wk - set(lama)),
                   watchlist_dibuang=len(set(lama) - wk - {(r['saham'], r['kaedah']) for r in senarai}),
                   watchlist_ke_senarai=sum(r['asal'] == 'watchlist' for r in senarai), minggu_akhir=minggu_akhir,
                   fail_isyarat=os.path.relpath(fail_isy, BS2) if fail_isy else None)


# ---------------------------------------------------------------- MALAM: kemas + imbas
LIPUTAN_MIN = 0.99     # pecahan saham universe (ada bar sesi sebelum) yang mesti ada bar sesi S


def data_belum_muktamad(S, univ_path):
    """Sebab menangguh sesi S jika data yfinance belum muktamad (logik sama dengan lejar.py jalan), atau None.
    Tarikan yfinance sejurus selepas tutup boleh tersilap harga buka (URBN 16 Okt 2026) atau tiada bar bagi sebahagian saham."""
    S = pd.Timestamp(S)
    ses = [x for x in sesi_list() if x < S]
    u = {x.strip().replace('US.', '') for x in open(univ_path) if x.strip()} if os.path.exists(univ_path) else set(FR)
    if ses:
        ada = [t for t, g in FR.items() if t in u and ses[-1] in g.index]
        cukup = sum(1 for t in ada if S in FR[t].index) / max(len(ada), 1)
        if cukup < LIPUTAN_MIN:
            return f'liputan bar {cukup:.1%} < {LIPUTAN_MIN:.0%}'
    p = os.path.join(BS2, 'data', 'harga', 'status.json')
    tk = json.load(open(p)).get('terkini', {}) if os.path.exists(p) else {}
    if str(tk.get('sesi')) == S.strftime('%Y%m%d') and \
            pd.Timestamp(tk.get('dijana', '1970-01-01 00:00 UTC').replace(' UTC', '')) < S + pd.Timedelta(hours=24, minutes=20):
        return f"data yfinance awal ({tk.get('dijana')})"
    return None

def cmd_malam(a):
    folder = a.folder; masa = kini(a.masa)
    st = status_baca(folder)
    kerja_dir = tempfile.mkdtemp(prefix='harian_c_')
    try:
        fr0 = muat(a.stor)
        S = pd.Timestamp(str(a.sesi)) if a.sesi else pd.Timestamp(str(int(fr0['harga_idx.csv'].date.max())))
        Ss = str(S.date())
        if not a.paksa and st.get('malam', {}).get('sesi') == Ss:
            print(json.dumps(dict(sesi=Ss, langkau='sudah diproses', masa=st['malam'].get('masa')), ensure_ascii=False))
            return 0
        stor_dir = stor_hingga(a.stor, S, kerja_dir)
        global FR, IDX
        FR, IDX = frames_dict(muat(stor_dir))
        if 'SPY' not in IDX or IDX['SPY'].index[-1] != S:
            raise SystemExit(f'stor harga tiada bar SPY {Ss}')
        tangguh = None if a.paksa else data_belum_muktamad(S, a.univ)
        if tangguh:   # sama dengan pengawal lejar.py: larian sandaran memproses sesi ini dengan data muktamad
            print(json.dumps(dict(sesi=Ss, ditangguh=tangguh), ensure_ascii=False))
            return 0
        SES = sesi_list()
        posisi = kumpul_posisi(folder, S, SES)
        layak = layak_imbas(a.univ) if not a.tanpa_imbas else set()
        if layak is None:
            raise SystemExit(f'univ tiada: {a.univ}')
        a431 = set(fr0.get('harga_A.csv', pd.DataFrame(columns=['ticker'])).ticker)
        t0 = time.time()
        hasil, tanpa_modul = jalan_kaedah(stor_dir, S, posisi, layak, a431, not a.tanpa_imbas, a.proses)
        ralat = [f"{m}: {h['ralat']}" for m, h in hasil.items() if h['ralat']]
        rk = dict(sesi=Ss, masa=teks_masa(masa), ralat_kaedah=ralat, kaedah_tanpa_modul=tanpa_modul,
                  masa_kaedah_s=round(time.time() - t0))
        kemas(folder, stor_dir, S, hasil, masa, rk)
        # posisi dibeli selepas pengumuman ambil alih = isyarat palsu: tidak_sah, tutup kedua-dua lorong
        palsu = AA.tanda_posisi(folder, FR)
        rk['ambil_alih_posisi'] = dict(ditutup=sum(x[4] != 'menunggu' for x in palsu),
                                       menunggu=sum(x[4] == 'menunggu' for x in palsu), saham=sorted({x[1] for x in palsu}))
        if not a.tanpa_imbas:
            imbas(folder, S, hasil, masa, rk, a.isyarat)
        st['malam'] = rk
        status_tulis(folder, st)
        print(json.dumps(rk, ensure_ascii=False, indent=1))
        return 0
    finally:
        shutil.rmtree(kerja_dir, ignore_errors=True)


# ---------------------------------------------------------------- GRED
def cmd_gred(a):
    folder = a.folder; masa = kini(a.masa); D = a.tarikh or str(masa.date())
    sb, wl = os.path.join(folder, 'senarai_beli.csv'), os.path.join(folder, 'watchlist.csv')
    py = sys.executable
    if not a.tanpa_tarik:
        r = subprocess.run([py, os.path.join(HERE, 'pemangkin_actions.py'), '--keluar', a.pemangkin, '--univ', a.univ,
                            '--csv', sb, wl], capture_output=True, text=True)
        print(r.stdout[-3000:], r.stderr[-2000:])
    kum = [py, os.path.join(HERE, 'gred.py'), 'kumpul', '--yahoo', os.path.join(a.pemangkin, 'yahoo.json'),
           '--nasdaq', os.path.join(a.pemangkin, 'earnings_nasdaq.json'), '--csv', sb, wl,
           '--keluar', os.path.join(folder, 'pemangkin.json'), '--tarikh', D]
    if a.sejak:
        kum += ['--sejak', a.sejak]
    elif status_baca(folder).get('malam', {}).get('sesi'):
        # data Yahoo yang diambil selepas sesi isyarat tutup (16:00 New York) dipakai
        S = status_baca(folder)['malam']['sesi']
        kum += ['--sejak', pd.Timestamp(f'{S} 16:00', tz='America/New_York').tz_convert('UTC').isoformat()]
    r = subprocess.run(kum, capture_output=True, text=True); print(r.stdout[-3000:], r.stderr[-2000:])
    acara = os.path.join(a.pemangkin, 'market_events.json')
    for f in (sb, wl):
        # Sektor/Industri v2 (sejak 19 Okt 2026): data/kumpulan/gred_kumpulan.csv daripada Actions gred_kumpulan.yml
        cmd = [py, os.path.join(HERE, 'gred.py'), 'tambah', '--csv', f, '--harga', a.stor,
               '--kumpulan', os.path.join(os.path.dirname(HERE), 'data', 'kumpulan', 'gred_kumpulan.csv'),
               '--peta', os.path.join(folder, 'peta_industri.csv'), '--tarikh', D]
        if os.path.exists(os.path.join(folder, 'pemangkin.json')):
            cmd += ['--pemangkin', os.path.join(folder, 'pemangkin.json')]
        if os.path.exists(os.path.join(a.pemangkin, 'earnings_nasdaq.json')):
            cmd += ['--nasdaq', os.path.join(a.pemangkin, 'earnings_nasdaq.json')]
        if os.path.exists(acara) and (time.time() - os.path.getmtime(acara)) < 9 * 86400:
            cmd += ['--acara', acara]
        kew = os.path.join(os.path.dirname(HERE), 'data', 'kewangan')
        if os.path.isdir(kew):
            cmd += ['--kewangan', kew]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout[-2000:], r.stderr[-2000:])
        if r.returncode:
            raise SystemExit(f'gred.py tambah gagal untuk {f}')
    st = status_baca(folder)
    p = Counter(r.get('gred_pemangkin') for r in csv.DictReader(open(sb, newline='', encoding='utf-8')))
    st['gred'] = dict(tarikh=D, masa=teks_masa(masa), pemangkin=dict(p))
    status_tulis(folder, st)
    return 0


# ---------------------------------------------------------------- BELI (9:35 NY)
def ambil_buka_yf(tickers, D):
    """Harga buka hari D (New York) daripada yfinance semasa/selepas pasaran dibuka. Pulang {t: (open, volume)}."""
    import yfinance as yf
    out = {}
    tk = sorted(set(tickers))
    for i in range(0, len(tk), 200):
        part = tk[i:i + 200]
        yt = [t.replace('.', '-') for t in part]
        d = yf.download(yt, period='5d', interval='1d', group_by='ticker', auto_adjust=False, progress=False, threads=True)
        for t, y in zip(part, yt):
            try:
                x = d[y] if len(yt) > 1 else d
                x = x[x.index.normalize() == pd.Timestamp(D)]
                if len(x):
                    o, v = float(x['Open'].iloc[0]), float(x['Volume'].iloc[0] or 0)
                    if np.isfinite(o) and o > 0:
                        out[t] = (o, v)
            except Exception:
                pass
    return out


def semak_buka_semula(calon, opens, stor_dir, S, D):
    """Kaedah bukan SILANG: tambah bar hari beli sementara (O=H=L=C=buka) dan jalankan sedia() semula — peraturan buka
    kaedah (buka_maks, henti ikut buka, isyarat mingguan) dinilai tepat seperti enjin. Pulang {(mid,t): (sig, stop_i)}."""
    fr0, idx0 = frames_dict(muat(stor_dir))
    St, Dt = pd.Timestamp(S), pd.Timestamp(D)
    out = {}
    ikut = {}
    for r in calon:
        ikut.setdefault(r['kaedah'], set()).add(r['saham'])
    for mid, tick in ikut.items():
        try:
            m = importlib.import_module(f'kaedah.{mid}')
        except Exception:
            continue
        if getattr(m, 'SILANG', False):
            continue
        fr = {}
        for t in tick:
            g = fr0.get(t)
            if g is None or t not in opens:
                continue
            g = g[g.index <= St]
            o, v = opens[t]
            fr[t] = pd.concat([g, pd.DataFrame(dict(open=o, high=o, low=o, close=o, volume=max(v, 1.0)), index=[Dt])])
        if not fr:
            continue
        try:
            m.sedia(fr, {k: x[x.index <= St] for k, x in idx0.items()})
        except Exception:
            continue
        for t, g in fr.items():
            enjin.siap(g)
            i = _bar_isyarat(g, St)
            if i is None:
                continue
            sp = nombor(g['stop'].iloc[i])
            out[(mid, t)] = (bool(g['sig'].iloc[i]), r4(sp) if sp is not None else None)
    return out


def cmd_beli(a):
    folder = a.folder; masa = kini(a.masa)
    ny = masa.tz_convert('America/New_York')
    D = a.tarikh or str(ny.date())
    st = status_baca(folder)
    if not a.paksa and not a.cuba and st.get('beli', {}).get('tarikh') == D:
        print(json.dumps(dict(tarikh=D, langkau='sudah direkod', masa=st['beli'].get('masa')), ensure_ascii=False)); return 0
    c = kal()
    if not c.is_session(pd.Timestamp(D)):
        rk = dict(tarikh=D, masa=teks_masa(masa), direkod=0, nota='pasaran AS tutup (cuti/hujung minggu): tak beli')
        st['beli'] = rk; status_tulis(folder, st); print(json.dumps(rk, ensure_ascii=False)); return 0
    S = str(c.previous_session(pd.Timestamp(D)).date())
    lajur_s, senarai = SH.baca(os.path.join(folder, 'senarai_beli.csv'))
    calon = [r for r in senarai if r.get('tarikh_isyarat') == S]
    if not calon:
        rk = dict(tarikh=D, masa=teks_masa(masa), direkod=0,
                  nota=f'tak beli: senarai_beli belum dikemas kini bagi isyarat {S} (tarikh_isyarat dalam fail: '
                       f'{sorted({r.get("tarikh_isyarat") for r in senarai})[-1:] or "-"})')
        print(json.dumps(rk, ensure_ascii=False))
        if a.akhir:   # larian sandaran terakhir: rekod "tak beli" supaya jelas
            st['beli'] = rk; status_tulis(folder, st)
        return 0
    # harga buka
    if a.buka:
        d = pd.read_csv(a.buka)
        opens = {str(t): (float(o), float(v) if 'volume' in d else 1.0)
                 for t, o, v in zip(d.ticker, d.open, d['volume'] if 'volume' in d else [1.0] * len(d)) if o and o > 0}
        sumber_buka = a.sumber_buka or os.path.basename(a.buka)
    else:
        opens = ambil_buka_yf([r['saham'] for r in calon], D)
        sumber_buka = f'buka sementara yfinance {ny.strftime("%H:%M")} NY'
    stor_dir = a.stor
    semula = semak_buka_semula(calon, opens, stor_dir, S, D)
    # posisi sedia ada (kunci kaedah+saham+tarikh_isyarat / tarikh_beli)
    ada = set()
    for p in fail_posisi(folder):
        for r in SH.baca(p)[1]:
            ada.add((r.get('kaedah'), r.get('saham'), r.get('tarikh_isyarat')))
            ada.add((r.get('kaedah'), r.get('saham'), 'beli:' + (r.get('tarikh_beli') or '')))
    rekod, langkau = [], []
    for r in calon:
        mid, t = r['kaedah'], r['saham']
        o = opens.get(t)
        def lk(sebab):
            langkau.append(f'{t} {mid}: {sebab}')
        if (mid, t, r['tarikh_isyarat']) in ada or (mid, t, 'beli:' + D) in ada:
            lk('sudah direkod'); continue
        if o is None:
            lk('belum didagangkan / tiada harga buka'); continue
        o = o[0]
        henti, bmax, tgt = nombor(r.get('henti')), nombor(r.get('buka_maks')), nombor(r.get('sasaran'))
        sig2, stop2 = semula.get((mid, t), (None, None))
        if stop2 is not None:
            henti = stop2
        if henti is not None and o <= henti:
            lk(f'buka {o:.2f} <= henti {henti:.2f}'); continue
        if bmax is not None and o > bmax:
            lk(f'buka {o:.2f} > buka_maks {bmax:.2f}'); continue
        if sig2 is False:
            lk('isyarat batal pada buka (peraturan kaedah)'); continue
        rekod.append((r, o, henti))
    if a.cuba:   # percubaan: tiada fail ditulis; banding harga buka dengan bar harian stor (jika ada)
        fr0, _ = frames_dict(muat(a.stor)); Dt = pd.Timestamp(D); beza = []
        for t, (o, v) in opens.items():
            g = fr0.get(t)
            if g is not None and Dt in g.index and abs(o / float(g.open.loc[Dt]) - 1) > 0.005:
                beza.append(f'{t}: yf {o:.4f} / stor {float(g.open.loc[Dt]):.4f}')
        print(json.dumps(dict(cuba=True, tarikh=D, calon=len(calon), harga_buka=len(opens), direkod=len(rekod), dilangkau=len(langkau),
                              langkau=langkau[:30], beza_stor_lebih_0_5pct=len(beza), contoh_beza=beza[:15],
                              contoh=dict(list(opens.items())[:5])), ensure_ascii=False, indent=1))
        return 0
    # kaedah_kongsi: kaedah lain yang membeli saham sama hari ini
    ikut_saham = {}
    for r, o, h in rekod:
        ikut_saham.setdefault(r['saham'], []).append(r['kaedah'])
    sasaran_fail = max((p for p in fail_posisi(folder) if os.path.basename(p).startswith('claude')), key=KL_nombor)
    lajur, rows = SH.baca(sasaran_fail)
    for c_ in GRED_LAJUR + ['tarikh_isyarat', 'kaedah_kongsi']:
        if c_ not in lajur:
            lajur.append(c_)
    for r, o, henti in rekod:
        lain = sorted((k for k in ikut_saham[r['saham']] if k != r['kaedah']), key=nombor_kaedah)
        n = int(nombor(r.get('belian_ke')) or 1)
        baru = {k: '' for k in lajur}
        baru.update(tarikh_beli=D, saham=r['saham'], kaedah=r['kaedah'], id_kaedah=r['kaedah'], sektor=r['sektor'],
                    industri=r['industri'], harga_beli=s(r4(o)), unit='1', harga_terkini=s(r4(o)), untung_pct='0.0', hari='0',
                    henti=s(henti), sasaran=r.get('sasaran', ''), keluar='False', sumber='harian_c',
                    kaedah_kongsi=','.join(lain), tarikh_isyarat=r['tarikh_isyarat'],
                    nota=(f'belian ke-{n}; ' if n >= 2 else '') + f'{sumber_buka} (disahkan dengan bar harian selepas tutup)')
        baru['isyarat_keluar'] = status_pegang(baru)
        for k in GRED_LAJUR:
            baru[k] = r.get(k, '')
        rows.append(baru)
    SH.tulis(sasaran_fail, lajur, rows)
    rk = dict(tarikh=D, masa=teks_masa(masa), isyarat=S, calon=len(calon), direkod=len(rekod), dilangkau=len(langkau),
              langkau=langkau[:60], saham_unik=len(ikut_saham), sumber_buka=sumber_buka, fail=os.path.basename(sasaran_fail),
              belian_semula=sum(1 for r, _, _ in rekod if int(nombor(r.get('belian_ke')) or 1) >= 2))
    st['beli'] = rk; status_tulis(folder, st)
    print(json.dumps(rk, ensure_ascii=False, indent=1))
    return 0


# ---------------------------------------------------------------- LOG
def cmd_log(a):
    """Catatan log daripada status_harian.json (peringkat: malam | beli)."""
    st = status_baca(a.folder); x = st.get(a.peringkat) or {}
    if not x:
        return 0
    if a.peringkat == 'malam':
        kb = x.get('keluar_baru', {})
        L = [f"## {x.get('masa')} — GitHub Actions: kemas kini + imbas (sesi AS {x.get('sesi')})",
             f"- Keluar baharu {sum((x.get('keluar_baru_jumlah') or {}).values())} (C {kb.get('C', {})}, M {kb.get('M', {})}); "
             f"menunggu buka sesi seterusnya: {x.get('menunggu')}.",
             f"- Harga beli sementara dibetulkan kepada buka rasmi bar harian: {x.get('harga_beli_dibetulkan')} "
             f"(beza > 0.5%: {x.get('harga_beli_beza_besar')}). Tidak dibeli baharu: {', '.join(x.get('tidak_dibeli') or []) or 'tiada'}.",
             f"- Senarai beli {x.get('senarai_beli')} baris ({x.get('saham_unik')} saham, {x.get('kaedah')} kaedah; "
             f"{x.get('dari_watchlist')} daripada watchlist; belian semula {x.get('belian_semula')}). Ditolak: {x.get('ditolak')}.",
             f"- Watchlist {x.get('watchlist')} (baharu {x.get('watchlist_baharu')}, dibuang {x.get('watchlist_dibuang')}, "
             f"ke senarai beli {x.get('watchlist_ke_senarai')}). Isyarat direkod: {x.get('isyarat')} ({x.get('fail_isyarat')}).",
             f"- Ralat kaedah: {x.get('ralat_kaedah') or 'tiada'}. Nota: {'; '.join((x.get('nota') or [])[:8]) or 'tiada'}.",
             '- Tiada order. Tiada wang sebenar.']
    else:
        L = [f"## {x.get('masa')} — GitHub Actions: beli maya {x.get('tarikh')} (isyarat {x.get('isyarat', '-')})",
             f"- {x.get('nota') or ''}".rstrip() if x.get('nota') else
             f"- Direkod {x.get('direkod')} ({x.get('saham_unik')} saham; belian semula {x.get('belian_semula')}; fail {x.get('fail')}); "
             f"dilangkau {x.get('dilangkau')}. Harga: {x.get('sumber_buka')}.",
             f"- Dilangkau: {'; '.join((x.get('langkau') or [])[:30]) or 'tiada'}.",
             '- Tiada order. Tiada wang sebenar.']
    tambah_log(a.log, '\n'.join(L))
    return 0


# ---------------------------------------------------------------- utama
def main(argv=None):
    ap = argparse.ArgumentParser(description='Papertrade C harian tanpa LLM')
    sp = ap.add_subparsers(dest='cmd', required=True)

    def umum(x):
        x.add_argument('--folder', default=PT); x.add_argument('--stor', default=STOR); x.add_argument('--univ', default=UNIV)
        x.add_argument('--masa', help='masa larian MYT "YYYY-MM-DD HH:MM" (ulang tayang)')
        x.add_argument('--paksa', action='store_true', help='kecemasan: proses semula walaupun sudah diproses. AMARAN malam: watchlist yang dipakai ialah watchlist sesi itu sendiri, jadi calon watchlist yang lengkap tidak lagi ditanda asal=watchlist')
    x = sp.add_parser('malam'); umum(x)
    x.add_argument('--sesi', help='sesi YYYY-MM-DD (lalai: bar terakhir stor)'); x.add_argument('--proses', type=int, default=4)
    x.add_argument('--isyarat', default=ISYARAT, help='folder rekod isyarat (kosong = tidak ditulis)')
    x.add_argument('--tanpa-imbas', action='store_true', help='kemas kini posisi sahaja')
    x.set_defaults(f=cmd_malam)
    x = sp.add_parser('gred'); umum(x)
    x.add_argument('--tarikh'); x.add_argument('--pemangkin', default=PEMANGKIN); x.add_argument('--sejak')
    x.add_argument('--tanpa-tarik', action='store_true', help='jangan jalankan pemangkin_actions.py (guna fail sedia ada)')
    x.set_defaults(f=cmd_gred)
    x = sp.add_parser('beli'); umum(x)
    x.add_argument('--tarikh', help='tarikh beli New York YYYY-MM-DD'); x.add_argument('--buka', help='CSV ticker,open[,volume]')
    x.add_argument('--sumber-buka'); x.add_argument('--akhir', action='store_true', help='larian sandaran terakhir hari itu')
    x.add_argument('--cuba', action='store_true', help='percubaan: tarik harga dan nilai peraturan tanpa menulis fail')
    x.set_defaults(f=cmd_beli)
    x = sp.add_parser('log'); x.add_argument('--folder', default=PT); x.add_argument('--peringkat', choices=['malam', 'beli'], required=True)
    x.add_argument('--log', default=LOG_HARIAN); x.set_defaults(f=cmd_log)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == '__main__':
    sys.exit(main())
