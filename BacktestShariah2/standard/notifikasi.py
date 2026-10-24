# Satu baris notifikasi telefon (< 200 aksara) daripada papertrade/status_harian.json selepas kerja GitHub Actions
# (permintaan pengguna 24 Okt 2026: notifikasi kerja papertrade sahaja, mula selepas peralihan). Dipakai oleh
# jadual/notifikasi_harian.md (selepas harian.yml) dan jadual/tolak_db.md langkah 6 (selepas beli.yml).
# Tanpa rangkaian: senarai workflow gagal diberi oleh sesi Claude (--gagal). "Kalau tak beli, cakap tak beli."
#
# Guna:
#   python3 notifikasi.py malam [--folder F] [--gagal harian.yml,lejar.yml] [--masa "YYYY-MM-DD HH:MM"] [--tambah TEKS]
#   python3 notifikasi.py beli  [--folder F] [--gagal …] [--masa …] [--tambah TEKS]
# --masa dalam UTC (lalai: sekarang).
import argparse, json, os, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(os.path.dirname(HERE), 'papertrade')
HAD = 199


def kal():
    import exchange_calendars as xc
    return xc.get_calendar('XNYS')


def ringkas(teks, gagal, tambah):
    bah = [teks]
    if gagal:
        bah.append('GAGAL: ' + ', '.join(gagal))
    if tambah:
        bah.append(tambah)
    s = ' | '.join(bah)
    return s if len(s) <= HAD else s[:HAD - 1] + '…'


def baris_malam(st, kini):
    """Sesi dijangka = sesi NYSE terakhir sebelum tarikh MYT hari ini (harian.yml memproses sesi AS semalam)."""
    c = kal()
    hari = kini.tz_convert('Asia/Kuala_Lumpur').tz_localize(None).normalize()
    ses = c.sessions_in_range(hari - pd.Timedelta(days=10), hari - pd.Timedelta(days=1))
    S = str(ses[-1].date())
    m = st.get('malam') or {}
    if m.get('sesi') != S:
        return f"Harian {S} BELUM siap (sesi terakhir diproses: {m.get('sesi') or '-'}); semak harian.yml"
    kj = m.get('keluar_baru_jumlah') or {}
    kc = (m.get('keluar_baru') or {}).get('C') or {}
    jenis = ', '.join(f'{k} {v}' for k, v in sorted(kc.items()) if v)
    seterus = str(c.next_session(pd.Timestamp(S)).date())
    td = len(m.get('tidak_dibeli') or [])
    return (f"Harian {S}: keluar C {kj.get('C', 0)}" + (f' ({jenis})' if jenis else '') + f", M {kj.get('M', 0)}; "
            f"menunggu {m.get('menunggu', 0)}" + (f'; tidak sah {td}' if td else '') +
            f"; senarai beli {m.get('senarai_beli', 0)} ({m.get('saham_unik', 0)} saham) untuk {seterus}")


def baris_beli(st, kini):
    D = str(kini.tz_convert('America/New_York').date())
    if not kal().is_session(pd.Timestamp(D)):
        return f'Tak beli {D}: pasaran AS tutup'
    b = st.get('beli') or {}
    if b.get('tarikh') != D:
        return f"Tak beli {D} (belum direkod; belian terakhir {b.get('tarikh') or '-'}); semak beli.yml"
    if not b.get('direkod'):
        return f"Tak beli {D}: {b.get('nota') or 'tiada calon lulus'}"
    lw = len(b.get('buka_lewat') or [])
    return (f"Beli {D}: {b['direkod']} direkod ({b.get('saham_unik', 0)} saham), {b.get('dilangkau', 0)} dilangkau"
            + (f', {lw} buka lewat' if lw else '') + f"; {b.get('sumber_buka', '')}").rstrip('; ')


def main(argv=None):
    ap = argparse.ArgumentParser(description='Baris notifikasi kerja papertrade GitHub Actions')
    ap.add_argument('peringkat', choices=['malam', 'beli'])
    ap.add_argument('--folder', default=FOLDER)
    ap.add_argument('--gagal', default='', help='nama fail workflow gagal, dipisah koma')
    ap.add_argument('--masa', default=None, help='UTC "YYYY-MM-DD HH:MM" (ujian)')
    ap.add_argument('--tambah', default='')
    a = ap.parse_args(argv)
    p = os.path.join(a.folder, 'status_harian.json')
    st = {}
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            st = json.load(f)
    kini = pd.Timestamp(a.masa, tz='UTC') if a.masa else pd.Timestamp.now(tz='UTC')
    teks = (baris_malam if a.peringkat == 'malam' else baris_beli)(st, kini)
    print(ringkas(teks, [g.strip() for g in a.gagal.split(',') if g.strip()], a.tambah.strip()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
