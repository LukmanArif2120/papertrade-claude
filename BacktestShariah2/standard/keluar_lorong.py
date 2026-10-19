# Dua lorong keluar (keputusan pengguna 17 Okt 2026; lorong 10% dibuang pada hari yang sama). Setiap posisi dinilai serentak
# dengan dua peraturan keluar dari harga beli yang sama, direkod dalam lajur berasingan:
#   1. Kaedah            — peraturan penuh kaedah (henti, sasaran, isyarat keluar, had masa): lajur sedia ada `keluar`, `tarikh_keluar` …
#   2. Pegang selagi naik (lajur *_henti; dipinda 19 Okt 2026, kajian kajian/KAJIAN_LORONG2.md) — Chandelier tutup:
#                          paras keluar = tutup tertinggi sejak beli − GANDA_ATR (4) × ATR14; paras hanya naik, tidak pernah turun.
#                          Tutup < paras keluar -> jual pada buka esok. Henti kaedah tidak dipakai dalam lorong ini (kekal dalam lorong 1).
# Belian semula kaedah+saham yang sama hanya selepas kedua-dua lorong keluar (`tutup_semua` = True).
# Lorong 2 hanya perlukan harga (OHLC, termasuk sejarah sebelum beli untuk ATR) dan harga beli, jadi dikira di sini tanpa modul kaedah.
#
# Guna (rutin 6:02 pagi, selepas lorong 1 dinilai; juga untuk isi semula):
#   python3 BacktestShariah2/standard/keluar_lorong.py [--stor <folder harga_A/B/idx.csv>] [--folder <papertrade>]
#       -> kemas kini lajur lorong 2 serta tutup_semua dalam moomoo.csv dan claude*.csv (lorong yang sudah keluar dibekukan,
#          kecuali baris yang keluar dengan peraturan lama — status_henti tanpa PENANDA — yang dikira semula secara automatik);
#          lajur lorong 10% lama (LAJUR_BUANG) dibuang daripada fail
#   --semula henti   -> kira semula lorong 2 walaupun sudah keluar (selepas peraturan lorong dipinda)
import argparse, csv, glob, json, os, re, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
PT = os.path.join(BS2, 'papertrade')
STOR = os.path.join(BS2, 'data', 'harga', 'stor')

GANDA_ATR = 4.0          # lorong 2: paras keluar = tutup tertinggi sejak beli − GANDA_ATR × ATR
TEMPOH_ATR = 14          # ATR seperti enjin.atr: purata mudah julat sebenar 14 hari
VERSI = 'chandelier_tutup_4xATR14'   # peraturan lorong 2 semasa; Lejar Penuh dibina semula apabila nilai ini berubah
PENANDA = 'paras keluar'             # ada dalam setiap status_henti peraturan semasa; tiada -> dikira dengan peraturan lama
BEZA_HARGA_MAKS = 0.15   # buka stor pada hari beli lawan harga_beli; lebih -> data tidak sepadan (split/ticker lain), langkau

LAJUR_HENTI = ['keluar_henti', 'tarikh_keluar_henti', 'harga_keluar_henti', 'untung_henti_pct', 'status_henti']
LAJUR_LORONG = LAJUR_HENTI + ['tutup_semua']
# lorong 10% (dibuang 17 Okt 2026): lajur ini dibuang daripada fail posisi apabila skrip dijalankan
LAJUR_BUANG = ['capai_10', 'tarikh_capai_10', 'keluar_10', 'tarikh_keluar_10', 'harga_keluar_10', 'untung_10_pct', 'status_10']

BULAN = ['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogo', 'Sep', 'Okt', 'Nov', 'Dis']


def hb(t):
    """'2026-10-16' atau Timestamp -> '16 Okt'."""
    s = str(t)[:10]
    return f'{int(s[8:10])} {BULAN[int(s[5:7]) - 1]}'


def atr(h, l, c, n=TEMPOH_ATR):
    """Sama seperti enjin.atr: purata mudah n bar julat sebenar (bar pertama = tinggi − rendah); NaN sebelum bar ke-n."""
    pc = np.r_[np.nan, c[:-1]]
    tr = np.fmax(h - l, np.fmax(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr).rolling(n).mean().to_numpy()


# ---------------------------------------------------------------- logik (tatasusunan bar; k = indeks bar hari beli)
def lorong_henti(o, h, l, c, k, ganda=GANDA_ATR, n_atr=TEMPOH_ATR):
    """Lorong 2 (pegang selagi naik, Chandelier tutup). Tatasusunan termasuk sejarah sebelum bar beli k (untuk ATR).
    Setiap bar j >= k: puncak = tutup tertinggi bar k..j; paras = max(paras semalam, puncak − ganda × ATR[j]), jadi paras
    hanya naik. Tutup[j] < paras -> jual pada buka bar j+1. Selagi ATR belum ada (sejarah < n_atr bar), paras = -inf.
    Pulang dict: keluar (j, harga, sebab) | menunggu (j, paras, tutup) | terbuka (paras, puncak)."""
    a = atr(h, l, c, n_atr)
    n = len(c); puncak = paras = -np.inf
    for j in range(k, n):
        puncak = max(puncak, c[j])
        if np.isfinite(a[j]):
            paras = max(paras, puncak - ganda * a[j])
        if c[j] < paras:
            if j + 1 < n:
                return dict(jenis='keluar', j=j + 1, harga=float(o[j + 1]),
                            sebab=f'tutup {c[j]:.2f} bawah {PENANDA} {paras:.2f} pada {{t{j}}}')
            return dict(jenis='menunggu', j=j, paras=float(paras), tutup=float(c[j]))
    return dict(jenis='terbuka', paras=float(paras), puncak=float(puncak))


def _teks(s, ix):
    return re.sub(r'\{t(\d+)\}', lambda m: hb(ix[int(m.group(1))]), s)


def r4(x):
    return f'{float(x):.4f}'.rstrip('0').rstrip('.')


def r2(x):
    return f'{float(x):.2f}'


def nilai_baris(ix, o, h, l, c, tarikh_beli, e):
    """Kira lorong 2 bagi satu posisi. ix = senarai tarikh 'YYYY-MM-DD'. Pulang (dict lajur CSV lorong 2, None),
    atau (None, sebab) jika tidak boleh dinilai."""
    if tarikh_beli not in ix:
        return None, f'tiada bar hari beli {tarikh_beli} dalam stor harga'
    k = ix.index(tarikh_beli)
    if not (o[k] > 0) or abs(o[k] / e - 1) > BEZA_HARGA_MAKS:
        return None, f'buka stor {o[k]:.4g} tidak sepadan harga beli {e:.4g}'
    akhir = len(o) - 1
    a = lorong_henti(o, h, l, c, k)
    L2 = dict.fromkeys(LAJUR_HENTI, '')
    if a['jenis'] == 'keluar':
        L2.update(keluar_henti='True', tarikh_keluar_henti=ix[a['j']], harga_keluar_henti=r4(a['harga']),
                  untung_henti_pct=r2((a['harga'] / e - 1) * 100),
                  status_henti=f"Keluar: {_teks(a['sebab'], ix)} ({hb(ix[a['j']])} @ {a['harga']:.2f})")
    else:
        L2['keluar_henti'] = 'False'
        if a['jenis'] == 'menunggu':
            L2['status_henti'] = (f"Tutup {a['tutup']:.2f} bawah {PENANDA} {a['paras']:.2f} pada {hb(ix[a['j']])}"
                                  ' — jual pada buka esok (menunggu)')
        elif np.isfinite(a['paras']):
            L2['status_henti'] = f"Pegang ({PENANDA} {a['paras']:.2f}; puncak {a['puncak']:.2f}; {akhir - k} hari)"
        else:
            L2['status_henti'] = f"Pegang ({PENANDA} belum ada: sejarah harga < {TEMPOH_ATR} hari; {akhir - k} hari)"
    return L2, None


# ---------------------------------------------------------------- fail papertrade
def benar(v):
    return str(v or '').strip().lower() in ('true', '1', 'ya')


def nombor(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def tutup_semua(r):
    return 'True' if benar(r.get('keluar')) and benar(r.get('keluar_henti')) else 'False'


def muat_harga(stor):
    sys.path.insert(0, os.path.join(BS2, 'kod'))
    from stor import muat, frames_dict
    fr, _ = frames_dict(muat(stor))
    out = {}
    for t, g in fr.items():
        out[t] = ([str(x.date()) for x in g.index], g.open.values.astype(float), g.high.values.astype(float),
                  g.low.values.astype(float), g.close.values.astype(float))
    return out


def kemas_baris(r, H, nota, semula=()):
    """Ubah baris r di tempat. Lorong 2 yang sudah keluar dibekukan, kecuali --semula henti atau keluar dengan peraturan lama
    (status_henti tanpa PENANDA; dikira semula sekali secara automatik). Pulang True jika ada perubahan."""
    lama = {c: r.get(c, '') for c in LAJUR_LORONG}
    if benar(r.get('tidak_dibeli')) or not r.get('tarikh_beli'):
        for c in LAJUR_LORONG: r[c] = ''
        return lama != {c: r.get(c, '') for c in LAJUR_LORONG}
    e = nombor(r.get('harga_beli'))
    if e is None or e <= 0:
        return False
    beku = benar(r.get('keluar_henti')) and PENANDA in (r.get('status_henti') or '') and 'henti' not in semula
    if not beku:
        d = H.get(r.get('saham'))
        if d is None:
            nota.append(f"{r.get('saham')} {r.get('kaedah')} {r.get('tarikh_beli')}: tiada dalam stor harga")
        else:
            L2, sebab = nilai_baris(*d, r['tarikh_beli'], e)
            if L2 is None:
                nota.append(f"{r.get('saham')} {r.get('kaedah')} {r.get('tarikh_beli')}: {sebab}")
            else:
                r.update(L2)
    r['tutup_semua'] = tutup_semua(r)
    return lama != {c: r.get(c, '') for c in LAJUR_LORONG}


def fail_posisi(folder):
    c = sorted(glob.glob(os.path.join(folder, 'claude*.csv')),
               key=lambda p: int(re.search(r'claude_?(\d*)', os.path.basename(p)).group(1) or 1))
    m = os.path.join(folder, 'moomoo.csv')
    return ([m] if os.path.exists(m) else []) + c


def main(argv=None):
    ap = argparse.ArgumentParser(description='Kemas kini lorong keluar 2 (pegang selagi naik) dalam fail posisi papertrade')
    ap.add_argument('--stor', default=STOR, help='folder harga_A/B/idx.csv (lalai: stor repo)')
    ap.add_argument('--folder', default=PT, help='folder papertrade')
    ap.add_argument('--semula', action='append', default=[], choices=['henti'],
                    help='kira semula lorong ini walaupun sudah keluar (selepas peraturan dipinda)')
    a = ap.parse_args(argv)
    H = muat_harga(a.stor)
    nota, ringkas = [], {}
    for p in fail_posisi(a.folder):
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        buang = [c for c in LAJUR_BUANG if c in lajur]
        lajur = [c for c in lajur if c not in buang] + [c for c in LAJUR_LORONG if c not in lajur]
        ubah = sum(kemas_baris(r, H, nota, a.semula) for r in rows) + (len(rows) if buang else 0)
        if ubah:
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows: w.writerow({c: r.get(c, '') for c in lajur})
        ringkas[os.path.basename(p)] = ubah
    dibeli = [r for p in fail_posisi(a.folder) for r in csv.DictReader(open(p, newline='', encoding='utf-8'))
              if not benar(r.get('tidak_dibeli')) and r.get('tarikh_beli')]
    out = dict(baris_berubah=ringkas, posisi=len(dibeli),
               keluar_kaedah=sum(benar(r.get('keluar')) for r in dibeli),
               keluar_henti=sum(benar(r.get('keluar_henti')) for r in dibeli),
               tutup_semua=sum(benar(r.get('tutup_semua')) for r in dibeli),
               tidak_dinilai=len(nota), nota=nota[:30])
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
