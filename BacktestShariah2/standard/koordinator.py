"""KOORDINATOR.md — satu halaman: apa perlu keputusan, apa menunggu masa, apa rosak.

Jurutulis, bukan pencari. Tiada penalaan, tiada LLM, tiada rangkaian: semuanya dibaca daripada
fail keadaan yang sudah ada dalam repo. Setiap pembaca gagal-lembut (fail tiada -> 'tiada').

  python3 BacktestShariah2/standard/koordinator.py   -> KOORDINATOR.md (akar repo)
"""
import csv
import glob
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
AKAR = os.path.dirname(BS2)
KELUAR = os.environ.get('KOORDINATOR_OUT', os.path.join(AKAR, 'KOORDINATOR.md'))
KEPUTUSAN = os.path.join(BS2, 'koordinator', 'keputusan.csv')
LEWAT_HARI = 3          # stor/data lebih lama daripada ini ditanda LEWAT

# Ambang yang sedang ditunggu (sumber: REVERSE/SPEC_FASA2.md §4, kajian/KAJIAN_PORTFOLIO.md)
F2_HARI, F2_SUKU = 250, 2
SLOT_BULAN_ADIL = 6


def _json(p, lalai=None):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return lalai


def _tarikh_csv(p, kol='tarikh'):
    """(n_tarikh_unik, min, maks) daripada satu lajur tarikh; (0, None, None) jika gagal."""
    try:
        import pandas as pd
        d = pd.read_csv(p, usecols=[kol])
        s = d[kol].astype(str).str.strip()
        s = s[s.str.match(r'\d{4}-\d{2}-\d{2}|\d{8}')]
        if s.empty:
            return 0, None, None
        u = sorted(set(s))
        return len(u), u[0], u[-1]
    except Exception:
        return 0, None, None


def _umur(t):
    """Hari dari tarikh 'YYYY-MM-DD' atau 'YYYYMMDD' hingga hari ini; None jika gagal."""
    if not t:
        return None
    s = str(t)[:10].replace('/', '-')
    for f in ('%Y-%m-%d', '%Y%m%d'):
        try:
            return (date.today() - datetime.strptime(s if f == '%Y-%m-%d' else str(t)[:8], f).date()).days
        except ValueError:
            continue
    return None


def _tanda(umur):
    if umur is None:
        return 'tiada'
    return 'OK' if umur <= LEWAT_HARI else f'**LEWAT {umur} hari**'


def git_keadaan():
    """(cawangan, tarikh HEAD, n commit di belakang origin/main, umur ref origin).

    PENTING: tanpa ini, seksyen kesegaran menipu. Salinan kerja yang lama akan melaporkan stor
    dan Lejar sebagai LEWAT walaupun `origin/main` sudah segar. Dikesan 28 Okt 2026 apabila
    larian pertama melaporkan Lejar LEWAT 5 hari sedangkan salinan kerja 94 commit di belakang.
    Tiada rangkaian: `origin/main` yang dibaca ialah ref tempatan daripada fetch terakhir.
    """
    def g(*a):
        try:
            return subprocess.run(['git', '-C', AKAR, *a], capture_output=True, text=True,
                                  timeout=20).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ''
    cab = g('rev-parse', '--abbrev-ref', 'HEAD') or 'tidak diketahui'
    head = g('log', '-1', '--format=%cs')
    blkg = g('rev-list', '--count', 'HEAD..origin/main')
    ref = g('log', '-1', '--format=%cs', 'origin/main')
    try:
        blkg = int(blkg)
    except ValueError:
        blkg = None
    return cab, head, blkg, ref


def keputusan_terbuka():
    try:
        with open(KEPUTUSAN, encoding='utf-8') as f:
            return [r for r in csv.DictReader(f) if (r.get('status') or '').strip() == 'terbuka']
    except OSError:
        return []


def kesegaran():
    """Senarai (sumber, tarikh terakhir, umur hari, tanda)."""
    out = []
    st = _json(os.path.join(BS2, 'data', 'harga', 'stor', 'status.json'), {})
    out.append(('Stor harga', st.get('bar_terakhir'), _umur(st.get('bar_terakhir'))))
    tr = _json(os.path.join(BS2, 'data', 'trend', 'status.json'), {})
    out.append(('Trend D10H2-r2', tr.get('tarikh'), _umur(tr.get('tarikh'))))
    lj = _json(os.path.join(BS2, 'lejar', 'ringkasan.json'), {}) or {}
    sl = lj.get('sesi_terakhir') or lj.get('sesi') or lj.get('tarikh')
    out.append(('Lejar Penuh', sl, _umur(sl)))
    ps = _json(os.path.join(BS2, 'portfolio_slot', 'status.json'), {}) or {}
    s1 = next((v.get('sesi_terakhir') for v in ps.values() if isinstance(v, dict)), None)
    out.append(('portfolio_slot', s1, _umur(s1)))
    pp = _json(os.path.join(BS2, 'data', 'analisis', 'papan.json'), {}) or {}
    db = (pp.get('dibina') or '')[:10]
    out.append(('Papan Penganalisis', db, _umur(db)))
    for nama, p, kol in (('RS pasaran', os.path.join(BS2, 'data', 'rs', 'rs_pasaran.csv'), 'tarikh'),
                         ('Gred kumpulan', os.path.join(BS2, 'data', 'kumpulan',
                                                        'gred_kumpulan_sejarah.csv'), 'tarikh')):
        n, a, b = _tarikh_csv(p, kol)
        out.append((nama, b, _umur(b)))
    for nama, p in (('SEC fundamental', os.path.join(BS2, 'data', 'sec', 'eps_hasil.csv')),
                    ('Senarai bursa', os.path.join(BS2, 'data', 'senarai_bursa', 'semasa.csv'))):
        u = None
        if os.path.exists(p):
            u = (date.today() - date.fromtimestamp(os.path.getmtime(p))).days
        out.append((nama, 'fail diubah' if u is not None else None, u))
    return [(a, b, c, _tanda(c)) for a, b, c in out]


def ambang_fasa2():
    """Kemajuan ambang SPEC_FASA2.md §4 bagi setiap sumber data titik-masa."""
    rows = []
    for nama, p, kol in (('RS pasaran', os.path.join(BS2, 'data', 'rs', 'rs_pasaran.csv'), 'tarikh'),
                         ('Gred kumpulan', os.path.join(BS2, 'data', 'kumpulan',
                                                        'gred_kumpulan_sejarah.csv'), 'tarikh')):
        n, a, b = _tarikh_csv(p, kol)
        rows.append(dict(sumber=nama, hari=n, mula=a, akhir=b,
                         suku=round(n / 63.0, 1), sedia='ya' if n >= F2_HARI else 'tidak'))
    # SEC = nilai pertama difail -> titik-masa retrospektif (SPEC_FASA2.md §4.1), jadi `tarikh_fail`
    # memang mengukur liputan. Halangan sebenar leg ini ialah liputan ticker, bukan bilangan hari.
    for nama, p in (('SEC EPS/hasil', os.path.join(BS2, 'data', 'sec', 'eps_hasil.csv')),
                    ('SEC earnings 8-K', os.path.join(BS2, 'data', 'sec', 'earnings_8k.csv'))):
        n, a, b = _tarikh_csv(p, 'tarikh_fail')
        baris = 0
        if os.path.exists(p):
            try:
                with open(p, encoding='utf-8') as f:
                    baris = max(sum(1 for _ in f) - 1, 0)
            except OSError:
                baris = 0
        rows.append(dict(sumber=nama, hari=n, mula=a, akhir=b, suku=round(n / 63.0, 1),
                         sedia='ya' if n >= F2_HARI else 'tidak', baris=baris, sec=True))
    return rows


def liputan_sec():
    """(ticker ada data, ticker universe, belum_diisi) - halangan sebenar leg SEC fasa 2."""
    st = _json(os.path.join(BS2, 'data', 'sec', 'status.json'), {}) or {}
    ada = 0
    try:
        import pandas as pd
        ada = pd.read_csv(os.path.join(BS2, 'data', 'sec', 'eps_hasil.csv'), usecols=['saham']).saham.nunique()
    except Exception:
        pass
    return ada, st.get('saham_universe'), st.get('belum_diisi')


def kajian():
    """Status setiap fasa kajian yang ada dalam repo."""
    out = []
    a2 = _json(os.path.join(AKAR, 'AUTOTUNE', 'hasil_a02', 'ringkasan.json'), {}) or {}
    k = a2.get('kiraan_label', {})
    if k:
        out.append(('AUTOTUNE A02 (penalaan Optuna)', 'DITUTUP',
                    f"{a2.get('n_cubaan_jumlah', '?')} konfigurasi diuji -> "
                    f"LULUS {k.get('LULUS', '?')}, CALON {k.get('CALON', '?')}, "
                    f"TIDAK LULUS {k.get('TIDAK LULUS', '?')}"))
    rev = sorted(glob.glob(os.path.join(AKAR, 'REVERSE', 'keputusan_*.csv')))
    if rev:
        try:
            import pandas as pd
            n_t = n_c = n_x = 0
            tahun = []
            for p in rev:
                y = os.path.basename(p).split('_')[-1].split('.')[0]
                if not y.isdigit():
                    continue
                tahun.append(y)
                d = pd.read_csv(p)
                n_t += int((d.keputusan == 'DITERIMA').sum())
                n_c += int((d.keputusan == 'CALON').sum())
                n_x += int((d.keputusan == 'DITOLAK').sum())
            out.append((f'REVERSE fasa 1 ({min(tahun)}–{max(tahun)})', 'DITUTUP — DITOLAK',
                        f'DITERIMA {n_t}, CALON {n_c}, DITOLAK {n_x}; sasaran +10%/bulan '
                        f'0 daripada 36 sistem-tahun'))
        except Exception:
            pass
    if os.path.exists(os.path.join(AKAR, 'REVERSE', 'KEPUTUSAN_1B.md')):
        out.append(('REVERSE fasa 1b (saiz berskala risiko)', 'DITUTUP — DITOLAK',
                    'pulangan ditolak; MDD bertambah baik 6/6 tahun -> diuji hadapan '
                    'sebagai lorong RISIKO_10'))
    if os.path.exists(os.path.join(AKAR, 'REVERSE', 'SPEC_FASA2.md')):
        out.append(('REVERSE fasa 2 leg RS/gred', 'SPEC DIKUNCI — menunggu masa',
                    'RS/gred dikira harian, tiada sejarah; anggaran ~Okt 2027'))
        out.append(('REVERSE fasa 2 leg SEC', 'SPEC DIKUNCI — menunggu liputan ticker',
                    'data titik-masa sejak 2009 (§4.1); menunggu isian awal 3,335 ticker, bukan masa'))
    return out


def slot():
    """Keadaan lorong portfolio_slot + kemajuan bacaan adil."""
    ps = _json(os.path.join(BS2, 'portfolio_slot', 'status.json'), {}) or {}
    rows = []
    for k, v in ps.items():
        if not isinstance(v, dict):
            continue
        rows.append(dict(lorong=k, ekuiti=v.get('ekuiti'), dipegang=v.get('dipegang'),
                         keluar=v.get('keluar'), sesi=v.get('sesi_terakhir')))
    return rows


def papan():
    pp = _json(os.path.join(BS2, 'data', 'analisis', 'papan.json'), {}) or {}
    rows = pp.get('rows', [])
    kira = {}
    for r in rows:
        kira[r.get('pantau') or '—'] = kira.get(r.get('pantau') or '—', 0) + 1
    return len(rows), kira


def jadual():
    """Workflow berjadual + sama ada penjaga_jadual menjaganya."""
    jaga = set()
    try:
        with open(os.path.join(HERE, 'penjaga_jadual.py'), encoding='utf-8') as f:
            s = f.read()
        blok = s[s.index('JAGA = {'):]
        jaga = set(re.findall(r"'([\w.]+\.yml)'", blok[:blok.index('}')]))
    except (OSError, ValueError):
        pass
    out = []
    for p in sorted(glob.glob(os.path.join(AKAR, '.github', 'workflows', '*.yml'))):
        try:
            with open(p, encoding='utf-8') as f:
                t = f.read()
        except OSError:
            continue
        cron = re.findall(r"cron:\s*'([^']+)'", t)
        if cron:
            n = os.path.basename(p)
            out.append((n, ', '.join(cron), 'ya' if n in jaga else '**tidak**'))
    return out


def jadual_md(baris, kol):
    o = ['| ' + ' | '.join(kol) + ' |', '|' + '|'.join('---' for _ in kol) + '|']
    for r in baris:
        o.append('| ' + ' | '.join('' if x is None else str(x) for x in r) + ' |')
    return '\n'.join(o) + '\n'


def main():
    L = []
    A = L.append
    A('# KOORDINATOR — keadaan repo dalam satu halaman\n')
    A(f'Dijana `BacktestShariah2/standard/koordinator.py` pada '
      f'{datetime.now().strftime("%Y-%m-%d %H:%M")} (waktu pelayan). Tiada rangkaian, tiada LLM, '
      'tiada penalaan — semuanya dibaca daripada fail keadaan repo. **Jangan ubah manual.**\n')

    cab, head, blkg, ref = git_keadaan()
    A('## 0. Salinan kerja\n')
    A(jadual_md([(cab, head or 'tiada', 'tiada' if blkg is None else blkg, ref or 'tiada')],
                ['Cawangan', 'HEAD', 'Commit di belakang origin/main', 'origin/main (fetch terakhir)']))
    if blkg:
        A(f'\n> **AMARAN: salinan kerja {blkg} commit di belakang `origin/main`.** Seksyen '
          f'"Kesegaran data" di bawah menerangkan **salinan ini**, bukan keadaan repo sebenar. '
          f'Jalankan `git pull --rebase origin main` dahulu, kemudian jana semula halaman ini, '
          f'sebelum melaporkan apa-apa sebagai LEWAT.\n')
    elif blkg == 0:
        A('\nSelari dengan `origin/main` pada fetch terakhir — angka kesegaran di bawah boleh '
          'dipercayai.\n')

    kt = keputusan_terbuka()
    A(f'\n## 1. Perlu keputusan anda ({len(kt)})\n')
    if kt:
        A(jadual_md([(r['tarikh'], r['perkara'], r.get('catatan', '')) for r in kt],
                    ['Dibuka', 'Perkara', 'Catatan']))
        A(f'\nSunting `BacktestShariah2/koordinator/keputusan.csv` — tukar `status` ke `selesai` '
          'apabila diputuskan (tambah sahaja; jangan buang baris).\n')
    else:
        A('Tiada. (`BacktestShariah2/koordinator/keputusan.csv` tiada baris `terbuka`.)\n')

    A('\n## 2. Kajian REVERSE — signal dan indikator (BUKAN kaedah Mxx)\n')
    A('REVERSE menguji **signal dan indikator** untuk ENTRY/HOLD/EXIT. Ia **tidak** menguji 134 '
      'kaedah Mxx repo dan tidak menala parameter. Populasi ujiannya ialah **peristiwa sah** '
      '(`REVERSE/SPEC.md` §7: tutup ≥ 5% di atas rendah terendah 20 hari DAN tutup > EMA21, '
      'kausal) atas universe A02 — bukan Lejar Penuh, bukan `portfolio_slot/`. Jangan campurkan '
      'kedua-dua jejak (`REVERSE/SPEC_FASA2.md` §9).\n')
    A(f'\n### Ambang fasa 2 (`SPEC_FASA2.md` §4: ≥ {F2_HARI} hari dagangan liputan bertindih, '
      f'≥ 3,000 peristiwa sah, ≥ {F2_SUKU} suku penuh)\n')
    f2 = ambang_fasa2()
    A(jadual_md([(r['sumber'], r.get('hari'), r.get('mula'), r.get('akhir'), r.get('suku'),
                  r.get('baris', ''), r['sedia']) for r in f2],
                ['Sumber', 'Hari dagangan', 'Mula', 'Akhir', 'Suku (anggaran)', 'Baris', 'Cukup?']))
    rs = [r['hari'] for r in f2 if r.get('hari') and not r.get('sec')]
    A(f'\nLeg **RS/gred**: terbaik **{max(rs or [0])} / {F2_HARI}** hari dagangan. Peristiwa sah ialah '
      'fungsi deterministik stor harga, jadi join peristiwa × data titik-masa boleh dibuat '
      '**retrospektif** — yang perlu ditunggu ialah masa, bukan kod.\n')
    ada, univ, baki = liputan_sec()
    A(f'\nLeg **SEC** tidak menunggu: nilai pertama difail = titik-masa retrospektif sejak 2009 '
      f'(`SPEC_FASA2.md` §4.1). Halangannya **liputan ticker**: {ada} daripada {univ} ticker '
      f'universe ada data EPS/hasil, {baki} belum diisi. Universe REVERSE kira-kira 2,300 setahun.\n')

    A('\n## 3. Operasi repo — 134 kaedah Mxx dan papertrade C\n')
    A('Jejak berasingan daripada §2. Semua di bawah ini dipacu oleh isyarat kaedah **Mxx** '
      'melalui Lejar Penuh.\n')
    A(f'\n### Lorong portfolio_slot (bacaan adil ≥ {SLOT_BULAN_ADIL} bulan, '
      '`kajian/KAJIAN_PORTFOLIO.md`)\n')
    sl = slot()
    if sl:
        A(jadual_md([(r['lorong'], r['ekuiti'], r['dipegang'], r['keluar'], r['sesi'])
                     for r in sl], ['Lorong', 'Ekuiti', 'Dipegang', 'Keluar', 'Sesi terakhir']))
        A('\n`RISIKO_10` (sejak 28 Okt 2026) dipasangkan dengan `RS_10`: susunan calon sama, hanya '
          'saiz berbeza. **MDD-nya mesti dibaca bersama lajur `tunai`** — pendedahannya lebih '
          'rendah, jadi sebahagian kelebihan MDD datang daripada pendedahan, bukan saiz. Ia '
          'menguji saiz atas **isyarat Mxx** dan bukan ujian ke hadapan dapatan REVERSE fasa 1b '
          '(`REVERSE/SPEC_FASA2.md` §9.2).\n')
    else:
        A('Tiada `portfolio_slot/status.json`.\n')

    n_p, kira = papan()
    A(f'\n### Papan Penganalisis — {n_p} kaedah Mxx\n')
    A(jadual_md(sorted(kira.items()), ['Status pantau', 'Bilangan']))
    if kira.get('BELUM CUKUP') == n_p and n_p:
        A('\nSemua kaedah masih **BELUM CUKUP** (< 10 hari beli berbeza). Tiada kaedah boleh '
          'dinilai ke hadapan lagi; penilaian penuh dijangka 15 Jan 2027 (`WFO/README.md`).\n')

    A('\n## 4. Kesegaran data\n')
    A(jadual_md([(a, b, c, d) for a, b, c, d in kesegaran()],
                ['Sumber', 'Terakhir', 'Umur (hari)', 'Status']))
    A(f'\nAmbang LEWAT: > {LEWAT_HARI} hari. Dua sebab biasa **bukan** kerosakan: hujung minggu '
      'atau cuti pasaran, dan salinan kerja yang lama (lihat §0). Periksa kedua-duanya, kemudian '
      '`penjaga_jadual` dan log workflow, sebelum menganggap saluran rosak.\n')

    A('\n## 5. Workflow berjadual\n')
    A(jadual_md(jadual(), ['Workflow', 'Cron', 'Dijaga penjaga_jadual?']))
    A('\nWorkflow berjadual baharu **mesti** ditambah ke `JAGA` dalam '
      '`standard/penjaga_jadual.py`; lajur "tidak" di atas bermakna cetusan yang hilang tidak '
      'akan dipulihkan.\n')

    A('\n## 6. Status kajian\n')
    kj = kajian()
    A(jadual_md(kj, ['Kajian', 'Status', 'Hasil']) if kj else 'Tiada.\n')

    A('\n## 7. Jangan ulangi — sudah diukur, ruang kosong\n')
    A('- **Penalaan parameter indikator.** AUTOTUNE A02: 38,400 konfigurasi dengan Optuna TPE, '
      'walk-forward, DSR dan PBO → LULUS 0, CALON 0. Setiap konfigurasi tambahan menaikkan '
      'ambang yang hasilnya mesti lepasi, bukan peluang menemui sesuatu.\n'
      '- **Signal entry berasaskan indikator harga.** REVERSE fasa 1: 6 tahun, 4 rejim, '
      '20,640 ujian ENTRY → tiada signal lulus gate keras dalam lebih daripada satu tahun; '
      'portfolio signal kalah kepada entri rawak pada 3 daripada 5 tahun yang diuji.\n'
      '- **Signal EXIT berasaskan indikator.** FDR 0 pada setiap satu daripada enam tahun.\n'
      '- Baca `REVERSE/KEPUTUSAN_FASA1.md` dan `REVERSE/DIAGNOSIS_FASA1.md` sebelum mencadangkan '
      'kajian indikator baharu.\n')
    with open(KELUAR, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    print(f'KOORDINATOR.md: {len("".join(L)):,} aksara | keputusan terbuka {len(kt)} | '
          f'fasa 2 RS/gred {max(rs or [0])}/{F2_HARI} hari | SEC {ada}/{univ} ticker | '
          f'lorong {len(sl)} | '
          f'di belakang origin/main: {blkg}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
