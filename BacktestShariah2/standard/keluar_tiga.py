# Tiga lorong keluar (keputusan pengguna 17 Okt 2026). Setiap posisi dinilai serentak dengan tiga peraturan keluar,
# masing-masing dari harga beli yang sama, dan direkod dalam lajur berasingan:
#   1. Kaedah  — peraturan penuh kaedah (henti, sasaran, isyarat keluar, had masa): lajur sedia ada `keluar`, `tarikh_keluar` …
#   2. Henti   — henti kaedah sahaja, pegang hingga kena. Kaedah tanpa henti: "pegang selagi untung" = keluar pada buka esok
#                selepas tutup pertama < harga beli.
#   3. 10%     — sebelum tutup >= harga beli × 1.10: peraturan lorong 2 (perlindungan rugi). Selepas capai: pegang selagi
#                tutup >= low semalam; tutup pertama < low semalam -> jual pada buka esok. Henti kaedah kekal aktif.
# Belian semula kaedah+saham yang sama hanya selepas ketiga-tiga lorong keluar (`tutup_semua` = True).
# Lorong 2 dan 3 hanya perlukan harga (OHLC), harga beli dan henti, jadi dikira di sini tanpa modul kaedah.
#
# Guna (rutin 6:02 pagi, selepas lorong 1 dinilai; juga untuk isi semula):
#   python3 BacktestShariah2/standard/keluar_tiga.py [--stor <folder harga_A/B/idx.csv>] [--folder <papertrade>]
#       -> kemas kini lajur lorong 2 dan 3 serta tutup_semua dalam moomoo.csv dan claude*.csv (lorong yang sudah keluar dibekukan)
import argparse, csv, glob, json, os, re, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
PT = os.path.join(BS2, 'papertrade')
STOR = os.path.join(BS2, 'data', 'harga', 'stor')

AMBANG_10 = 0.10
BEZA_HARGA_MAKS = 0.15   # buka stor pada hari beli lawan harga_beli; lebih -> data tidak sepadan (split/ticker lain), langkau

LAJUR_HENTI = ['keluar_henti', 'tarikh_keluar_henti', 'harga_keluar_henti', 'untung_henti_pct', 'status_henti']
LAJUR_10 = ['capai_10', 'tarikh_capai_10', 'keluar_10', 'tarikh_keluar_10', 'harga_keluar_10', 'untung_10_pct', 'status_10']
LAJUR_TIGA = LAJUR_HENTI + LAJUR_10 + ['tutup_semua']

BULAN = ['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogo', 'Sep', 'Okt', 'Nov', 'Dis']


def hb(t):
    """'2026-10-16' atau Timestamp -> '16 Okt'."""
    s = str(t)[:10]
    return f'{int(s[8:10])} {BULAN[int(s[5:7]) - 1]}'


def ada_henti(sp):
    return sp is not None and np.isfinite(sp)


# ---------------------------------------------------------------- logik (tatasusunan bar; k = indeks bar hari beli)
def lorong_henti(o, h, l, c, k, e, sp):
    """Lorong 2. Pulang dict: keluar (j, harga, sebab) | menunggu (j isyarat) | terbuka.
    Henti dinilai dari hari beli (rendah <= henti), buka jurang bawah henti dari hari kedua -> harga buka (seperti enjin)."""
    n = len(o)
    for j in range(k, n):
        if ada_henti(sp):
            if j > k and o[j] <= sp:
                return dict(jenis='keluar', j=j, harga=float(o[j]), sebab='kena henti (buka bawah henti)')
            if l[j] <= sp:
                return dict(jenis='keluar', j=j, harga=float(sp), sebab='kena henti')
        elif c[j] < e:
            if j + 1 < n:
                return dict(jenis='keluar', j=j + 1, harga=float(o[j + 1]), sebab=f'tutup bawah harga beli {{t{j}}}')
            return dict(jenis='menunggu', j=j, sebab='tutup bawah harga beli')
    return dict(jenis='terbuka')


def lorong_10(o, h, l, c, k, e, sp, ambang=AMBANG_10):
    """Lorong 3. Sebelum capai (tutup >= e × (1 + ambang)): peraturan lorong 2. Selepas capai (dari bar berikutnya):
    tutup < low semalam -> jual buka esok. Henti kaedah kekal aktif sepanjang posisi."""
    n = len(o); cp = None; paras = round(e * (1 + ambang), 6)   # bundar: elak 100 × 1.1 = 110.00000000000001
    for j in range(k, n):
        if ada_henti(sp):
            if j > k and o[j] <= sp:
                return dict(jenis='keluar', j=j, harga=float(o[j]), sebab='kena henti (buka bawah henti)', capai=cp)
            if l[j] <= sp:
                return dict(jenis='keluar', j=j, harga=float(sp), sebab='kena henti', capai=cp)
        if cp is None:
            if not ada_henti(sp) and c[j] < e:
                if j + 1 < n:
                    return dict(jenis='keluar', j=j + 1, harga=float(o[j + 1]), sebab=f'tutup bawah harga beli {{t{j}}}', capai=cp)
                return dict(jenis='menunggu', j=j, sebab='tutup bawah harga beli', capai=cp)
            if c[j] >= paras:
                cp = j
        elif c[j] < l[j - 1]:
            if j + 1 < n:
                return dict(jenis='keluar', j=j + 1, harga=float(o[j + 1]), sebab=f'tutup < low semalam {{t{j}}}', capai=cp)
            return dict(jenis='menunggu', j=j, sebab='tutup < low semalam', capai=cp)
    return dict(jenis='terbuka', capai=cp)


def _teks(s, ix):
    return re.sub(r'\{t(\d+)\}', lambda m: hb(ix[int(m.group(1))]), s)


def r4(x):
    return f'{float(x):.4f}'.rstrip('0').rstrip('.')


def r2(x):
    return f'{float(x):.2f}'


def nilai_baris(ix, o, h, l, c, tarikh_beli, e, sp):
    """Kira lorong 2 dan 3 bagi satu posisi. ix = senarai tarikh 'YYYY-MM-DD'. Pulang (dict lorong2, dict lorong3) bentuk lajur CSV,
    atau (None, sebab) jika tidak boleh dinilai."""
    if tarikh_beli not in ix:
        return None, f'tiada bar hari beli {tarikh_beli} dalam stor harga'
    k = ix.index(tarikh_beli)
    if not (o[k] > 0) or abs(o[k] / e - 1) > BEZA_HARGA_MAKS:
        return None, f'buka stor {o[k]:.4g} tidak sepadan harga beli {e:.4g}'
    akhir = len(o) - 1
    a = lorong_henti(o, h, l, c, k, e, sp)
    L2 = dict.fromkeys(LAJUR_HENTI, '')
    if a['jenis'] == 'keluar':
        L2.update(keluar_henti='True', tarikh_keluar_henti=ix[a['j']], harga_keluar_henti=r4(a['harga']),
                  untung_henti_pct=r2((a['harga'] / e - 1) * 100),
                  status_henti=f"Keluar: {_teks(a['sebab'], ix)} ({hb(ix[a['j']])} @ {a['harga']:.2f})")
    else:
        L2['keluar_henti'] = 'False'
        if a['jenis'] == 'menunggu':
            L2['status_henti'] = f"{a['sebab'].capitalize()} {hb(ix[a['j']])} — jual pada buka esok (menunggu)"
        elif ada_henti(sp):
            L2['status_henti'] = f'Pegang (henti {sp:.2f})'
        else:
            L2['status_henti'] = f'Pegang selagi untung (keluar jika tutup < {e:.2f})'
    b = lorong_10(o, h, l, c, k, e, sp)
    L3 = dict.fromkeys(LAJUR_10, '')
    cp = b.get('capai')
    L3['capai_10'] = 'True' if cp is not None else 'False'
    if cp is not None:
        L3['tarikh_capai_10'] = ix[cp]
    if b['jenis'] == 'keluar':
        L3.update(keluar_10='True', tarikh_keluar_10=ix[b['j']], harga_keluar_10=r4(b['harga']),
                  untung_10_pct=r2((b['harga'] / e - 1) * 100),
                  status_10=f"Keluar: {_teks(b['sebab'], ix)}{'' if cp is not None else ' sebelum +10%'} ({hb(ix[b['j']])} @ {b['harga']:.2f})")
    else:
        L3['keluar_10'] = 'False'
        if b['jenis'] == 'menunggu':
            L3['status_10'] = f"{b['sebab'].capitalize()} {hb(ix[b['j']])} — jual pada buka esok (menunggu)"
        elif cp is not None:
            L3['status_10'] = f'Capai +10% {hb(ix[cp])}; pegang (keluar jika tutup < {l[akhir]:.2f})'
        else:
            lindung = f'henti {sp:.2f}' if ada_henti(sp) else f'keluar jika tutup < {e:.2f}'
            L3['status_10'] = f'Pegang (belum +10%: tutup >= {e * (1 + AMBANG_10):.2f}; {lindung})'
    return L2, L3


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
    return 'True' if benar(r.get('keluar')) and benar(r.get('keluar_henti')) and benar(r.get('keluar_10')) else 'False'


def muat_harga(stor):
    sys.path.insert(0, os.path.join(BS2, 'kod'))
    from stor import muat, frames_dict
    fr, _ = frames_dict(muat(stor))
    out = {}
    for t, g in fr.items():
        out[t] = ([str(x.date()) for x in g.index], g.open.values.astype(float), g.high.values.astype(float),
                  g.low.values.astype(float), g.close.values.astype(float))
    return out


def kemas_baris(r, H, nota):
    """Ubah baris r di tempat. Lorong yang sudah keluar dibekukan. Pulang True jika ada perubahan."""
    lama = {c: r.get(c, '') for c in LAJUR_TIGA}
    if benar(r.get('tidak_dibeli')) or not r.get('tarikh_beli'):
        for c in LAJUR_TIGA: r[c] = ''
        return lama != {c: r.get(c, '') for c in LAJUR_TIGA}
    e = nombor(r.get('harga_beli'))
    if e is None or e <= 0:
        return False
    beku2, beku3 = benar(r.get('keluar_henti')), benar(r.get('keluar_10'))
    if not (beku2 and beku3):
        d = H.get(r.get('saham'))
        if d is None:
            nota.append(f"{r.get('saham')} {r.get('kaedah')} {r.get('tarikh_beli')}: tiada dalam stor harga")
        else:
            sp = nombor(r.get('henti'))
            L2, L3 = nilai_baris(*d, r['tarikh_beli'], e, sp)
            if L2 is None:
                nota.append(f"{r.get('saham')} {r.get('kaedah')} {r.get('tarikh_beli')}: {L3}")
            else:
                if not beku2: r.update(L2)
                if not beku3: r.update(L3)
    r['tutup_semua'] = tutup_semua(r)
    return lama != {c: r.get(c, '') for c in LAJUR_TIGA}


def fail_posisi(folder):
    c = sorted(glob.glob(os.path.join(folder, 'claude*.csv')),
               key=lambda p: int(re.search(r'claude_?(\d*)', os.path.basename(p)).group(1) or 1))
    m = os.path.join(folder, 'moomoo.csv')
    return ([m] if os.path.exists(m) else []) + c


def main(argv=None):
    ap = argparse.ArgumentParser(description='Kemas kini lorong keluar 2 (henti) dan 3 (10%) dalam fail posisi papertrade')
    ap.add_argument('--stor', default=STOR, help='folder harga_A/B/idx.csv (lalai: stor repo)')
    ap.add_argument('--folder', default=PT, help='folder papertrade')
    a = ap.parse_args(argv)
    H = muat_harga(a.stor)
    nota, ringkas = [], {}
    for p in fail_posisi(a.folder):
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        lajur += [c for c in LAJUR_TIGA if c not in lajur]
        ubah = sum(kemas_baris(r, H, nota) for r in rows)
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
               capai_10=sum(benar(r.get('capai_10')) for r in dibeli),
               keluar_10=sum(benar(r.get('keluar_10')) for r in dibeli),
               tutup_semua=sum(benar(r.get('tutup_semua')) for r in dibeli),
               tidak_dinilai=len(nota), nota=nota[:30])
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
