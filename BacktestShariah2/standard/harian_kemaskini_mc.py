import json, csv, pandas as pd, numpy as np
SP = '/tmp/claude-0/-home-claude/1065e185-9b92-5438-9115-e17141ed91ba/scratchpad/'
DIBINA = '2026-10-13 06:10 MYT (larian harian 6:02)'
HARGA_PADA = '2026-10-12 tutup (Moomoo snapshot, sesi biasa)'
o = json.load(open(SP + 'nilai_out.json'))
snap = pd.read_csv(SP + 'snap12.csv').set_index('ticker')
idx = pd.read_csv(SP + 'kod/data/harga_idx.csv'); SES = sorted(pd.to_datetime(idx[idx.ticker == 'SPY'].date.astype(str)))
LOW = pd.concat([pd.read_csv(SP + 'kod/data/harga_A.csv'), pd.read_csv(SP + 'kod/data/harga_B.csv')])
LOW = {t: g.set_index('date')['low'] for t, g in LOW.groupby('ticker')}
BLN = {10: 'Okt'}
def tk(d): d = pd.Timestamp(d); return f'{d.day} {BLN.get(d.month, d.strftime("%b"))}'
def hari(b, s): b, s = pd.Timestamp(b), pd.Timestamp(s); return sum(1 for x in SES if b < x <= s)
def r2(x): return None if x is None else round(float(x), 2)
def r4(x): return None if x is None else round(float(x), 4)
def status_pegang(r):
    h, s = r.get('henti'), r.get('sasaran')
    base = r['isyarat_keluar']
    if base.startswith('Pegang (luar') or base.startswith('Pegang (warisan'): return base
    p = []
    if h: p.append(f'henti {h:.2f}')
    if s: p.append(f'sasaran {s:.2f}')
    return 'Pegang' + (f' ({", ".join(p)})' if p else '')
baru = {'M': [], 'C': []}; menunggu = []
for ak in ['moomoo', 'claude']:
    for r in o[ak]['rows']:
        r = dict(r)
        x = r.pop('_x', None); r.pop('_sp', None); r.pop('_tgt', None); r.pop('_nota', None)
        if r.get('keluar'):
            pass
        elif x and x.get('t'):
            r['keluar'] = True; r['tarikh_keluar'] = x['t']; r['harga_keluar'] = r4(x['p'])
            r['untung_akhir_pct'] = r2((x['p'] / r['harga_beli'] - 1) * 100)
            r['harga_terkini'] = r['harga_keluar']; r['untung_pct'] = r['untung_akhir_pct']
            r['hari'] = hari(r['tarikh_beli'], x['t'])
            why = x['why'].replace(' 09 Oct',' 9 Okt').replace(' 07 Oct',' 7 Okt').replace(' Oct',' Okt')
            r['isyarat_keluar'] = f'Keluar: {why} ({tk(x["t"])} @ {x["p"]:.2f})'
            r['dikesan'] = '2026-10-13 06:02 MYT'
            baru['M' if ak == 'moomoo' else 'C'].append((r['saham'], r['kaedah'], why, x['t'], r['untung_akhir_pct']))
        else:
            t = r['saham']
            if t in snap.index and snap.loc[t].data_date == '2026-10-12':
                c = float(snap.loc[t].close); r['harga_terkini'] = r4(c); r['untung_pct'] = r2((c / r['harga_beli'] - 1) * 100)
            r['hari'] = hari(r['tarikh_beli'], '2026-10-12')
            if x and x.get('why') == 'menunggu':
                r['isyarat_keluar'] = f'Isyarat keluar {tk(x["isy"])} — jual pada buka esok (menunggu)'
                menunggu.append((ak, r['saham'], r['kaedah']))
            else:
                r['isyarat_keluar'] = status_pegang(r)
        r['_ak'] = ak
        o.setdefault('_new_' + ak, []).append(r)
for ak in ['moomoo', 'claude']:
    d = o[ak]; d['rows'] = [{k: v for k, v in r.items() if k != '_ak'} for r in o['_new_' + ak]]
    d['dibina'] = DIBINA; d['harga_pada'] = HARGA_PADA
    d['nota'] = ('Larian 6:02 MYT 13 Okt: harga tutup 12 Okt (Moomoo snapshot). Keluar dinilai semula dengan enjin kaedah (stor harga hingga 12 Okt) bagi semua posisi belum keluar, '
                 'termasuk isyarat bukan-henti pegangan warisan v1. Baris keluar dibekukan; posisi Moomoo TIDAK dijual. "Menunggu" = isyarat keluar pada tutup 12 Okt, harga keluar = buka 13 Okt (diisi larian esok).')
    json.dump(d, open(SP + f'out_{ak}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
# CSV
K = ['tarikh_beli', 'saham', 'kaedah', 'sektor', 'industri', 'harga_beli', 'unit', 'harga_terkini', 'untung_pct', 'hari', 'isyarat_keluar', 'tarikh_keluar', 'harga_keluar', 'untung_akhir_pct',
     'id_kaedah', 'sumber', 'kaedah_kongsi', 'henti', 'sasaran', 'keluar', 'nota']
for ak in ['moomoo', 'claude']:
    kk = K + (['tarikh_isyarat'] if ak == 'claude' else [])
    with open(SP + f'{ak}.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(kk)
        for r in o[ak]['rows']:
            w.writerow(['+'.join(r.get(k) or []) if k == 'kaedah_kongsi' else ('' if r.get(k) is None else r.get(k)) for k in kk])
# MAE
mae0 = json.load(open(SP + 'db/prestasi/mae.json'))['rows']; mae = {}; fb = 0
for ak, A in [('moomoo', 'M'), ('claude', 'C')]:
    for r in o[ak]['rows']:
        k = f"{A}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"; b = int(r['tarikh_beli'].replace('-', ''))
        lo = LOW.get(r['saham'])
        if lo is None:
            v = mae0.get(k, 0); t = r['saham']
            if not r.get('keluar') and t in snap.index: v = min(v, (snap.loc[t].low / r['harga_beli'] - 1) * 100)
            fb += 1
        else:
            if r.get('keluar') and r.get('tarikh_keluar'):
                e = int(r['tarikh_keluar'].replace('-', '')); w = lo[(lo.index >= b) & (lo.index < e)].tolist()
                if r.get('harga_keluar') is not None: w.append(r['harga_keluar'])
            else: w = lo[lo.index >= b].tolist()
            v = (min(w) / r['harga_beli'] - 1) * 100 if w else mae0.get(k, 0)
        v = round(min(0, v), 2); mae[k] = min(v, mae.get(k, 0))
json.dump({'rows': mae, 'dibina': DIBINA, 'harga_hingga': '2026-10-12 tutup', 'definisi': 'Penurunan maksimum % = (harga rendah terendah sejak hari beli hingga hari ini, atau sehingga keluar) ÷ harga beli − 1, maksimum 0. Bagi posisi keluar: rendah hari sebelum hari keluar dan harga keluar. Kunci: akaun|saham|kaedah|tarikh_beli (akaun M=Moomoo, C=Claude).'},
          open(SP + 'out_mae.json', 'w'), separators=(',', ':'))
json.dump({'baru': baru, 'menunggu': menunggu, 'mae_fallback': fb}, open(SP + 'ringkas_keluar.json', 'w'))
print(json.dumps(baru)); print(len(menunggu), menunggu); print('mae', len(mae), fb)
for ak in ['moomoo', 'claude']:
    R = o[ak]['rows']; print(ak, len(R), sum(r.get('keluar', False) for r in R))
