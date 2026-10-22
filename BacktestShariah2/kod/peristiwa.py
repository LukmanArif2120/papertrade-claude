# peristiwa.py — jadual faktor peristiwa korporat besar (22 Okt 2026; kajian/reports/Pengesanan data tercemar yang tinggal.md).
# Stor harga = konvensyen backtest: bar sebelum ~2 Okt 2026 ialah data backtest (kline Moomoo dilaras hadapan termasuk dividen
# dan spin-off); bar yfinance selepasnya hanya dilaras pecahan. Peristiwa besar selepas itu (spin-off, dividen khas >= 2% harga,
# pengagihan >= 25%) mencipta jurang palsu (cth. DD spin-off Qnity 3 Nov 2025: −57.5% mentah). Jadual `data/harga/faktor.csv`
# memegang faktor hadapan (bar sebelum tarikh_ex x faktor, sama seperti Moomoo autype=1 / CRSP) dan digunakan pada stor:
#   - guna_stor(): bar lama stor sebelum tarikh_ex didarab faktor SEKALI (rekod dalam <stor>/faktor_diguna.csv, jadi salinan
#     stor rutin dan stor repo masing-masing tahu sama ada sudah dilaras);
#   - laras_baru(): bar baharu yfinance (mentah) sebelum tarikh_ex didarab faktor sebelum digabung, supaya tetingkap 10 sesi
#     yang merentasi tarikh_ex kekal seragam.
# Lejar dibina semula apabila jadual berubah (tidak_layak.versi); posisi Lejar dilaras oleh mekanisme `laras` sedia ada;
# posisi Papertrade C yang merentasi tarikh_ex dilaras oleh laras_c() (tidak_layak.py posisi).
# Sumber: (1) dividen yfinance (`actions=True` dalam harga_yf terkini -> data/harga/dividen.csv): D/P >= 2% ditambah automatik;
# (2) calon jurang buka <= −15% tanpa earnings (faktor_calon.csv) disahkan rutin 6:02 dengan Moomoo
# `quote_corporate_actions_rehab` (SPINOFF / SPECIALDIVIDEND) melalui CLI `tambah` / `tolak`.
#
#   python3 kod/peristiwa.py calon                       # calon belum disahkan
#   python3 kod/peristiwa.py tambah --saham DD --tarikh-ex 2025-11-03 --jenis spin_off --faktor 0.4182 --sumber "moomoo rehab"
#   python3 kod/peristiwa.py tolak --saham XYZ --tarikh 2026-10-21 --sebab "kejatuhan sebenar (berita)"
import argparse, hashlib, json, os, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
HARGA = os.path.join(BS2, 'data', 'harga')
FAKTOR = os.path.join(HARGA, 'faktor.csv')
CALON = os.path.join(HARGA, 'faktor_calon.csv')
DIVIDEN = os.path.join(HARGA, 'dividen.csv')
LAJUR = ['saham', 'tarikh_ex', 'jenis', 'faktor', 'sumber', 'catatan', 'ditambah']
LAJUR_CALON = ['saham', 'tarikh', 'jurang', 'nilai_x', 'status', 'catatan', 'dikesan']
DIV_MIN = 0.02          # dividen >= 2% harga = dividen khas (Morningstar: >= 5%; 2% dipilih kerana ~0.6 x ATR median 3.4%)
PENGAGIHAN = 0.25       # >= 25%: FINRA 11140 tarikh-ex selepas tarikh bayar; dilayan seperti spin-off
JURANG_CALON = -0.15    # jurang buka <= −15% tanpa earnings = calon spin-off/pengagihan
VERSI = 'peristiwa v1 (22 Okt 2026)'


def kini():
    return pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d')


def muat(path=None):
    path = path or FAKTOR
    if not os.path.exists(path):
        return pd.DataFrame(columns=LAJUR)
    d = pd.read_csv(path, dtype=str, keep_default_na=False)
    return d[(d.saham != '') & (d.tarikh_ex != '') & (pd.to_numeric(d.faktor, errors='coerce') > 0)]


def versi(path=None):
    path = path or FAKTOR
    h = hashlib.sha1(open(path, 'rb').read()).hexdigest()[:8] if os.path.exists(path) else '-'
    return f'{VERSI}; faktor {h}'


def _int(t):
    return int(str(t).replace('-', ''))


def _diguna(folder):
    p = os.path.join(folder, 'faktor_diguna.csv')
    return p, ({(r.saham, r.tarikh_ex) for r in pd.read_csv(p, dtype=str).itertuples()} if os.path.exists(p) else set())


def guna_stor(stor, folder, rows=None):
    """Darab bar stor sebelum tarikh_ex dengan faktor bagi peristiwa yang belum diguna pada stor `folder` dan tarikh_ex-nya
    sudah ada dalam stor (bar >= tarikh_ex wujud). stor = {nama fail: DataFrame LAJ}. Ubah di tempat; pulang log."""
    rows = muat() if rows is None else rows
    p, sudah = _diguna(folder)
    log = []
    for r in rows.itertuples():
        if (r.saham, r.tarikh_ex) in sudah:
            continue
        ex, f = _int(r.tarikh_ex), float(r.faktor)
        for nm, d in stor.items():
            m = d.ticker == r.saham
            if not m.any() or d.loc[m, 'date'].max() < ex or d.loc[m, 'date'].min() >= ex:
                continue
            k = m & (d.date < ex)
            for c in ('open', 'high', 'low', 'close'):
                d.loc[k, c] = d.loc[k, c].astype(float) * f
            sudah.add((r.saham, r.tarikh_ex))
            log.append(dict(ticker=r.saham, nisbah=round(f, 6), bar=int(k.sum()), serak=0.0, keputusan='faktor',
                            sumber=f'{r.jenis} {r.tarikh_ex} ({r.sumber})'))
    if log:
        pd.DataFrame(sorted(sudah), columns=['saham', 'tarikh_ex']).to_csv(p, index=False)
    return log


def laras_baru(baru, rows=None, akhir=None):
    """Bar baharu mentah (LAJ) -> bar sebelum tarikh_ex didarab hasil darab faktor semua peristiwa yang tarikh_ex-nya sudah
    berlaku (<= bar terakhir saham itu dalam `baru` atau `akhir` {ticker: tarikh int}). Pulang salinan."""
    rows = muat() if rows is None else rows
    if not len(rows) or not len(baru):
        return baru
    b = baru.copy()
    hujung = b.groupby('ticker').date.max().to_dict()
    for t, v in (akhir or {}).items():
        hujung[t] = max(hujung.get(t, 0), v)
    for r in rows.itertuples():
        ex = _int(r.tarikh_ex)
        if hujung.get(r.saham, 0) < ex:
            continue
        k = (b.ticker == r.saham) & (b.date < ex)
        for c in ('open', 'high', 'low', 'close'):
            b.loc[k, c] = b.loc[k, c].astype(float) * float(r.faktor)
    return b


def simpan_dividen(div, path=None):
    """Gabung rekod dividen (ticker, date int, dividen) ke data/harga/dividen.csv (unik ikut ticker+tarikh)."""
    path = path or DIVIDEN
    if div is None or not len(div):
        return 0
    lama = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=['ticker', 'date', 'dividen'])
    x = pd.concat([lama, div[['ticker', 'date', 'dividen']]]).drop_duplicates(['ticker', 'date'], keep='last')
    x.sort_values(['date', 'ticker']).to_csv(path, index=False, float_format='%.6g')
    return len(x) - len(lama)


def tambah_dari_dividen(frames, path=None, dividen=None, mula='2026-10-02'):
    """Dividen yfinance >= DIV_MIN x tutup sesi sebelum tarikh-ex (selepas `mula` = hujung data backtest) -> baris faktor
    (dividen_khas / pengagihan; faktor = 1 − D/P). frames = {ticker: DataFrame berindeks tarikh}. Pulang baris baharu."""
    path, dividen = path or FAKTOR, dividen or DIVIDEN
    if not os.path.exists(dividen):
        return []
    dv = pd.read_csv(dividen)
    dv = dv[(dv.dividen > 0) & (dv.date > _int(mula))]
    ada = muat(path)
    kunci = set(zip(ada.saham, ada.tarikh_ex))
    baru = []
    for r in dv.itertuples():
        g = frames.get(r.ticker)
        ex = pd.Timestamp(str(r.date))
        if g is None or (r.ticker, str(ex.date())) in kunci:
            continue
        sebelum = g[g.index < ex]
        if not len(sebelum):
            continue
        P = float(sebelum.close.iloc[-1]); x = float(r.dividen) / P
        if x < DIV_MIN:
            continue
        baru.append(dict(saham=r.ticker, tarikh_ex=str(ex.date()), jenis='pengagihan' if x >= PENGAGIHAN else 'dividen_khas',
                         faktor=f'{1 - x:.6f}', sumber='yfinance dividen', catatan=f'D={r.dividen:g} P={P:g} ({x:.1%})',
                         ditambah=kini()))
    if baru:
        tulis(pd.concat([ada, pd.DataFrame(baru)], ignore_index=True), path)
    return baru


def tulis(d, path=None):
    path = path or FAKTOR
    d = d.reindex(columns=LAJUR).fillna('')
    d.drop_duplicates(['saham', 'tarikh_ex'], keep='last').sort_values(['tarikh_ex', 'saham']).to_csv(path, index=False)


def kesan_calon(frames, sesi, earnings=None, path=None, faktor=None, n_sesi=10):
    """Jurang buka <= JURANG_CALON dalam n_sesi terakhir, tiada earnings dalam ±1 hari kalendar dan belum dalam jadual faktor
    -> faktor_calon.csv (status 'calon'). Pulang calon baharu."""
    path, faktor = path or CALON, faktor or FAKTOR
    earnings = earnings or {}
    ada = muat(faktor)
    kunci = set(zip(ada.saham, ada.tarikh_ex))
    lama = pd.read_csv(path, dtype=str, keep_default_na=False) if os.path.exists(path) else pd.DataFrame(columns=LAJUR_CALON)
    dah = set(zip(lama.saham, lama.tarikh))
    tetingkap = set(pd.DatetimeIndex(sesi)[-n_sesi:])
    baru = []
    for t, g in frames.items():
        if len(g) < 22:
            continue
        j = g.open / g.close.shift(1) - 1
        for d in g.index[(j <= JURANG_CALON).values]:
            if d not in tetingkap:
                continue
            ds = str(d.date())
            if (t, ds) in dah or (t, ds) in kunci:
                continue
            if any(abs((pd.Timestamp(e) - d).days) <= 1 for e in earnings.get(t, ())):
                continue
            i = g.index.get_loc(d)
            nilai = float((g.close * g.volume).iloc[i] / max(1.0, float((g.close * g.volume).iloc[max(0, i - 20):i].median())))
            baru.append(dict(saham=t, tarikh=ds, jurang=f'{float(j.loc[d]):.4f}', nilai_x=f'{nilai:.2f}', status='calon',
                             catatan='', dikesan=kini()))
    if baru:
        pd.concat([lama, pd.DataFrame(baru)], ignore_index=True).reindex(columns=LAJUR_CALON).to_csv(path, index=False)
    return baru


def laras_c(folder, rows=None):
    """Posisi Papertrade C yang dibeli sebelum tarikh_ex dan masih dipegang pada tarikh_ex (lorong 1 terbuka atau keluar >= ex):
    harga_beli, henti, sasaran x faktor (jumlah pulangan berterusan, sama seperti laras Lejar); untung dikira semula. Sekali
    sahaja (penanda dalam nota). Pulang senarai perubahan; posisi yang keluar pada tarikh_ex dibenderakan 'semak'."""
    import sahkan as SH
    rows = muat() if rows is None else rows
    if not len(rows):
        return []
    ev = {}
    for r in rows.itertuples():
        ev.setdefault(r.saham, []).append(r)
    out = []
    for p in sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('claude') and f.endswith('.csv')):
        lajur, data = SH.baca(p)
        ubah = False
        for x in data:
            for r in ev.get(x.get('saham'), ()):
                tanda = f'faktor {r.jenis} {r.tarikh_ex}'
                tb = x.get('tarikh_beli') or ''
                if not tb or tb >= r.tarikh_ex or tanda in (x.get('nota') or '') or SH.benar(x.get('tidak_dibeli')):
                    continue
                kel = SH.benar(x.get('keluar'))
                if kel and (x.get('tarikh_keluar') or '') < r.tarikh_ex:
                    continue
                f = float(r.faktor)
                hb = SH.nombor(x.get('harga_beli'))
                if not hb:
                    continue
                hb2 = hb * f
                x['harga_beli'] = f'{hb2:.4f}'.rstrip('0').rstrip('.')
                for c in ('henti', 'sasaran'):
                    v = SH.nombor(x.get(c))
                    if v:
                        x[c] = f'{v * f:.4f}'.rstrip('0').rstrip('.')
                hk = SH.nombor(x.get('harga_terkini'))
                if hk:
                    x['untung_pct'] = f'{(hk / hb2 - 1) * 100:.2f}'
                if kel and SH.nombor(x.get('harga_keluar')):
                    x['untung_akhir_pct'] = f"{(SH.nombor(x['harga_keluar']) / hb2 - 1) * 100:.2f}"
                if SH.benar(x.get('keluar_henti')) and SH.nombor(x.get('harga_keluar_henti')) and (x.get('tarikh_keluar_henti') or '') >= r.tarikh_ex:
                    x['untung_henti_pct'] = f"{(SH.nombor(x['harga_keluar_henti']) / hb2 - 1) * 100:.2f}"
                x['nota'] = ((x.get('nota') or '') + f'; {tanda} x{f:g} (harga beli/henti/sasaran dilaras)').lstrip('; ')
                ubah = True
                out.append((os.path.basename(p), x['saham'], x.get('kaedah'), tb, r.tarikh_ex,
                            'semak' if kel and x.get('tarikh_keluar') == r.tarikh_ex else 'dilaras'))
        if ubah:
            SH.tulis(p, lajur, data)
    return out


# ---------------------------------------------------------------- CLI (rutin 6:02: sahkan calon dengan Moomoo rehab)
def main(argv=None):
    ap = argparse.ArgumentParser(description='Jadual faktor peristiwa korporat besar')
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('calon')
    t = sp.add_parser('tambah')
    for k in ('--saham', '--tarikh-ex', '--jenis', '--faktor', '--sumber'):
        t.add_argument(k, required=True)
    t.add_argument('--catatan', default='')
    x = sp.add_parser('tolak'); x.add_argument('--saham', required=True); x.add_argument('--tarikh', required=True)
    x.add_argument('--sebab', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'calon':
        c = pd.read_csv(CALON, dtype=str, keep_default_na=False) if os.path.exists(CALON) else pd.DataFrame(columns=LAJUR_CALON)
        print(c[c.status == 'calon'].to_csv(index=False), end='')
        return
    if a.cmd == 'tambah':
        f = float(a.faktor)
        if not 0 < f < 1:
            sys.exit('faktor mesti antara 0 dan 1 (bahagian nilai kekal pada saham induk / 1 − D/P)')
        if a.jenis not in ('spin_off', 'dividen_khas', 'pengagihan'):
            sys.exit('jenis: spin_off | dividen_khas | pengagihan')
        d = pd.concat([muat(), pd.DataFrame([dict(saham=a.saham, tarikh_ex=a.tarikh_ex, jenis=a.jenis, faktor=f'{f:.6f}',
                                                  sumber=a.sumber, catatan=a.catatan, ditambah=kini())])], ignore_index=True)
        tulis(d)
    sah = a.saham, (a.tarikh_ex if a.cmd == 'tambah' else a.tarikh)
    if os.path.exists(CALON):
        c = pd.read_csv(CALON, dtype=str, keep_default_na=False)
        m = (c.saham == sah[0]) & (c.tarikh == sah[1])
        c.loc[m, 'status'] = 'disahkan' if a.cmd == 'tambah' else 'bukan'
        c.loc[m, 'catatan'] = a.catatan if a.cmd == 'tambah' else a.sebab
        c.to_csv(CALON, index=False)
    print(json.dumps(dict(cmd=a.cmd, saham=sah[0], tarikh=sah[1]), ensure_ascii=False))


if __name__ == '__main__':
    main()
