# banding_bayang.py — mod selari (bayang) peralihan ke GitHub Actions (keputusan pengguna 17 Okt 2026: 3 hari dagangan
# berjalan selari sebelum rutin Claude dihentikan). Setiap rutin Claude (6:02 pagi, imbas malam, beli 9:35 NY) diulang
# tayang dengan standard/harian_c.py atas keadaan repo SEBELUM commit rutin itu, kemudian hasilnya dibanding dengan commit
# rutin. Tiada fail papertrade sebenar diubah.
#
#   python3 banding_bayang.py hari --tarikh D [--keluar BacktestShariah2/bayang]   # semua rutin Claude bertarikh MYT D
#   python3 banding_bayang.py kemas --sasaran <commit> | imbas --sasaran <commit> | beli --sasaran <commit>
# Laporan: bayang/BANDING_<D>.md (+ .json). Beza dijangka (bukan ralat): teks paparan, harga sementara 9:35 (Claude: quote
# Moomoo; Actions: bar harian muktamad), gred P (data pemangkin diambil pada masa berbeza), sumber tarikh earnings.
import argparse, csv, glob, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile
from collections import Counter

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
ROOT = os.path.dirname(BS2)
sys.path.insert(0, HERE)
import sahkan as SH  # noqa: E402

REL_PT = 'BacktestShariah2/papertrade'
CORAK = {'kemas': r'^Kemas kini 6:02 pagi (\d{4}-\d{2}-\d{2})', 'imbas': r'^Imbas (?:malam|8:02 malam|7:47 malam) (\d{4}-\d{2}-\d{2})',
         'beli': r'^Beli 9:35 NY (\d{4}-\d{2}-\d{2})'}


def git(*a):
    return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True, check=True).stdout


def ekstrak(commit, rel, dest):
    """Salin folder/fail `rel` pada `commit` ke dest (struktur repo dikekalkan). Pulang laluan penuh."""
    data = subprocess.run(['git', '-C', ROOT, 'archive', commit, rel], capture_output=True, check=True).stdout
    tarfile.open(fileobj=io.BytesIO(data)).extractall(dest, filter='data')
    return os.path.join(dest, rel)


def masa_commit(commit):
    t = pd.Timestamp(git('show', '-s', '--format=%cI', commit).strip()).tz_convert('Asia/Kuala_Lumpur')
    return t.strftime('%Y-%m-%d %H:%M')


def cari_commit(D):
    """Commit rutin Claude bagi tarikh MYT D -> {'kemas': c, 'imbas': [c…] (lama -> baharu), 'beli': c}."""
    out = {'imbas': []}
    for ln in git('log', '--format=%H %s', '--since', f'{D} 00:00 +0800', '--until', f'{D} 23:59 +0800').splitlines()[::-1]:
        h, msg = ln.split(' ', 1)
        for k, pat in CORAK.items():
            m = re.match(pat, msg)
            if m and m.group(1) == D:
                if k == 'imbas':
                    out['imbas'].append(h)
                else:
                    out.setdefault(k, h)
    # commit "Kemas kini 6:02 pagi D" ditulis pada D (MYT) tetapi boleh juga dicari mengikut mesej sahaja
    for k in ('kemas', 'beli'):
        if k not in out:
            for ln in git('log', '--format=%H %s', '-200').splitlines():
                h, msg = ln.split(' ', 1)
                m = re.match(CORAK[k], msg)
                if m and m.group(1) == D:
                    out[k] = h; break
    return out


def jalan(args):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'harian_c.py')] + args, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'harian_c.py {" ".join(args[:1])} gagal:\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}')
    return r.stdout


def baca_posisi(folder):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, 'claude*.csv'))) + [os.path.join(folder, 'moomoo.csv')]:
        if not os.path.exists(p):
            continue
        ak = 'M' if p.endswith('moomoo.csv') else 'C'
        for r in SH.baca(p)[1]:
            k = (ak, r['kaedah'], r['saham'], r.get('tarikh_isyarat') or '', r.get('tarikh_beli') or r.get('tarikh_beli_dirancang') or '')
            out[k] = r
    return out


def nb(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def sama_harga(a, b, tol=0.0005):
    a, b = nb(a), nb(b)
    if a is None or b is None:
        return a is None and b is None
    return abs(a / b - 1) <= tol if b else a == b


# ---------------------------------------------------------------- banding setiap peringkat
def banding_kemas(asas, kami, claude):
    A, K, C = baca_posisi(asas), baca_posisi(kami), baca_posisi(claude)
    kunci = sorted(set(K) & set(C)); hanya_k = sorted(set(K) - set(C)); hanya_c = sorted(set(C) - set(K))
    st = Counter(); beza = {'harga_beli': [], 'tidak_dibeli': [], 'keluar': [], 'harga_keluar': [], 'harga_terkini': []}
    for k in kunci:
        a, x, c = A.get(k, {}), K[k], C[k]
        ubah = any(a.get(f) != c.get(f) for f in ('harga_beli', 'keluar', 'tidak_dibeli', 'harga_terkini', 'harga_keluar'))
        st['diubah_claude'] += ubah
        if (x.get('tidak_dibeli') == 'True') != (c.get('tidak_dibeli') == 'True'):
            beza['tidak_dibeli'].append(f"{k}: kami {x.get('tidak_dibeli') or '-'} ({x.get('sebab_tidak_sah', '')}) / Claude {c.get('tidak_dibeli') or '-'}")
            continue
        if x.get('tidak_dibeli') == 'True':
            st['tidak_dibeli_sama'] += 1; continue
        st['dibanding'] += 1
        if sama_harga(x.get('harga_beli'), c.get('harga_beli')):
            st['harga_beli_sama'] += 1
        else:
            beza['harga_beli'].append(f"{k}: kami {x.get('harga_beli')} / Claude {c.get('harga_beli')}")
        kx, kc = x.get('keluar') == 'True', c.get('keluar') == 'True'
        if kx == kc and (not kx or x.get('tarikh_keluar') == c.get('tarikh_keluar')):
            st['keluar_sama'] += 1
            if kx:
                if sama_harga(x.get('harga_keluar'), c.get('harga_keluar'), 0.001):
                    st['harga_keluar_sama'] += 1
                else:
                    beza['harga_keluar'].append(f"{k}: kami {x.get('harga_keluar')} / Claude {c.get('harga_keluar')} ({c.get('isyarat_keluar')})")
            elif sama_harga(x.get('harga_terkini'), c.get('harga_terkini'), 0.001):
                st['harga_terkini_sama'] += 1
            else:
                beza['harga_terkini'].append(f"{k}: kami {x.get('harga_terkini')} / Claude {c.get('harga_terkini')}")
        else:
            beza['keluar'].append(f"{k}: kami {x.get('isyarat_keluar')} / Claude {c.get('isyarat_keluar')}")
        st['teks_sama'] += x.get('isyarat_keluar') == c.get('isyarat_keluar')
    return dict(stat=dict(st, baris=len(kunci), hanya_kami=len(hanya_k), hanya_claude=len(hanya_c)), beza=beza,
                hanya_kami=[str(k) for k in hanya_k[:20]], hanya_claude=[str(k) for k in hanya_c[:20]])


def kunci_senarai(p):
    return {(r['saham'], r['kaedah'], r['tarikh_isyarat']): r for r in SH.baca(p)[1]} if os.path.exists(p) else {}


def banding_imbas(kami, claude):
    K, C = kunci_senarai(os.path.join(kami, 'senarai_beli.csv')), kunci_senarai(os.path.join(claude, 'senarai_beli.csv'))
    sama = set(K) & set(C)
    st = Counter(senarai_kami=len(K), senarai_claude=len(C), senarai_sama=len(sama))
    beza = {'hanya_kami': [], 'hanya_claude': [], 'henti': [], 'sasaran': [], 'gred': [], 'belian_ke': []}
    for k in sorted(set(K) - set(C)):
        beza['hanya_kami'].append(f"{k} asal={K[k].get('asal')} rank? sumber={K[k].get('sumber')}")
    for k in sorted(set(C) - set(K)):
        beza['hanya_claude'].append(f"{k} asal={C[k].get('asal')} sumber={C[k].get('sumber')}")
    gred_sama = Counter()
    for k in sorted(sama):
        x, c = K[k], C[k]
        for f in ('henti', 'sasaran'):
            if sama_harga(x.get(f), c.get(f), 0.001):
                st[f + '_sama'] += 1
            else:
                beza[f].append(f"{k}: kami {x.get(f)} / Claude {c.get(f)}")
        st['belian_ke_sama'] += x.get('belian_ke') == c.get('belian_ke')
        if x.get('belian_ke') != c.get('belian_ke'):
            beza['belian_ke'].append(f"{k}: kami {x.get('belian_ke')} / Claude {c.get('belian_ke')}")
        for g in ('gred_sektor', 'gred_industri', 'gred_rs', 'gred_qr', 'gred_pemangkin'):
            gred_sama[g] += x.get(g) == c.get(g)
            if x.get(g) != c.get(g) and len(beza['gred']) < 40:
                beza['gred'].append(f"{k} {g}: kami {x.get(g)} / Claude {c.get(g)}")
    st.update({f'{g}_sama': n for g, n in gred_sama.items()})
    # watchlist
    def wk(p):
        return {(r['Saham'], r['Kaedah']) for r in SH.baca(p)[1]} if os.path.exists(p) else set()
    WK, WC = wk(os.path.join(kami, 'watchlist.csv')), wk(os.path.join(claude, 'watchlist.csv'))
    st.update(watch_kami=len(WK), watch_claude=len(WC), watch_sama=len(WK & WC))
    return dict(stat=dict(st), beza=beza, watch_hanya_kami=sorted(map(str, WK - WC))[:30], watch_hanya_claude=sorted(map(str, WC - WK))[:30])


def baris_beli(folder, D):
    out = {}
    for p in glob.glob(os.path.join(folder, 'claude*.csv')):
        for r in SH.baca(p)[1]:
            if (r.get('tarikh_beli') == D or r.get('tarikh_beli_dirancang') == D) and r.get('sumber') == 'harian_c':
                out[(r['kaedah'], r['saham'])] = r
    return out


def banding_beli(kami, claude, claude_betul, D):
    K, C = baris_beli(kami, D), baris_beli(claude, D)
    B = baris_beli(claude_betul, D) if claude_betul else {}
    st = Counter(direkod_kami=len(K), direkod_claude=len(C), sama=len(set(K) & set(C)))
    beza = {'hanya_kami': [f'{k}' for k in sorted(set(K) - set(C))][:40], 'hanya_claude': [f'{k}' for k in sorted(set(C) - set(K))][:40],
            'harga_lawan_betul': []}
    for k in set(K) & set(B):
        if B[k].get('tidak_dibeli') == 'True':
            continue
        st['harga_banding_betul'] += 1
        if sama_harga(K[k].get('harga_beli'), B[k].get('harga_beli')):
            st['harga_sama_betul'] += 1
        elif len(beza['harga_lawan_betul']) < 30:
            beza['harga_lawan_betul'].append(f"{k}: kami {K[k].get('harga_beli')} / Claude (dibetulkan 6:02) {B[k].get('harga_beli')}")
    for k in set(K) & set(C):
        st['harga_sama_sementara'] += sama_harga(K[k].get('harga_beli'), C[k].get('harga_beli'))
    return dict(stat=dict(st), beza=beza)


# ---------------------------------------------------------------- peringkat
def peringkat_kemas(c, kerja, masa=None):
    asas = ekstrak(c + '^', REL_PT, os.path.join(kerja, 'asas'))
    kami = ekstrak(c + '^', REL_PT, os.path.join(kerja, 'kami'))
    claude = ekstrak(c, REL_PT, os.path.join(kerja, 'claude'))
    ekstrak(c + '^', 'BacktestShariah2/data/harga/univ.txt', os.path.join(kerja, 'kami_u'))
    D = re.match(CORAK['kemas'], git('show', '-s', '--format=%s', c)).group(1)
    S = sesi_sebelum_tarikh(D)
    out = jalan(['malam', '--folder', kami, '--sesi', S, '--masa', masa or masa_commit(c), '--tanpa-imbas', '--isyarat', '',
                 '--univ', os.path.join(kerja, 'kami_u', 'BacktestShariah2/data/harga/univ.txt'), '--paksa'])
    return dict(peringkat='kemas', commit=c[:7], sesi=S, ringkas=status(kami).get('malam', {}), **banding_kemas(asas, kami, claude))


def peringkat_imbas(cs, kerja, masa=None):
    c0, c1 = cs[0], cs[-1]
    kami = ekstrak(c0 + '^', REL_PT, os.path.join(kerja, 'kami'))
    claude = ekstrak(c1, REL_PT, os.path.join(kerja, 'claude'))
    u = ekstrak(c0, 'BacktestShariah2/data/harga/univ.txt', os.path.join(kerja, 'u'))
    pem = ekstrak(c1, 'BacktestShariah2/data/pemangkin', os.path.join(kerja, 'p'))
    D = re.match(CORAK['imbas'], git('show', '-s', '--format=%s', c0)).group(1)
    S = sesi_sebelum_tarikh(D)
    isy = os.path.join(kerja, 'isyarat')
    m = masa or masa_commit(c0)
    out = jalan(['malam', '--folder', kami, '--sesi', S, '--masa', m, '--isyarat', isy, '--univ', u, '--paksa'])
    rk = status(kami).get('malam', {})
    # gred: data pemangkin pada commit Claude (diambil masa yang sama), stor dipotong <= S
    stor = os.path.join(kerja, 'stor'); potong_stor(S, stor)
    shutil.copy(os.path.join(claude, 'pemangkin.json'), os.path.join(kami, 'pemangkin.json')) if os.path.exists(os.path.join(claude, 'pemangkin.json')) else None
    jalan(['gred', '--folder', kami, '--stor', stor, '--pemangkin', pem, '--tarikh', D, '--masa', m, '--tanpa-tarik'])
    return dict(peringkat='imbas', commit=c0[:7] + '..' + c1[:7], sesi=S, ringkas=rk, **banding_imbas(kami, claude))


def peringkat_beli(c, kerja, betul=None, masa=None):
    kami = ekstrak(c + '^', REL_PT, os.path.join(kerja, 'kami'))
    claude = ekstrak(c, REL_PT, os.path.join(kerja, 'claude'))
    cb = ekstrak(betul, REL_PT, os.path.join(kerja, 'betul')) if betul else None
    D = re.match(CORAK['beli'], git('show', '-s', '--format=%s', c)).group(1)
    # harga buka = bar harian muktamad hari D daripada stor (Actions sebenar: yfinance semasa 9:35–10:00 NY)
    fr = [pd.read_csv(os.path.join(BS2, 'data/harga/stor', f)) for f in ('harga_A.csv', 'harga_B.csv')]
    d = pd.concat(fr); d = d[d.date == int(D.replace('-', ''))]
    buka = os.path.join(kerja, 'buka.csv'); d[['ticker', 'open', 'volume']].to_csv(buka, index=False)
    stor = os.path.join(kerja, 'stor'); potong_stor(sesi_sebelum_tarikh(D), stor)
    out = jalan(['beli', '--folder', kami, '--stor', stor, '--tarikh', D, '--buka', buka, '--sumber-buka', 'buka bar harian (ulang tayang)',
                 '--masa', masa or masa_commit(c), '--paksa'])
    return dict(peringkat='beli', commit=c[:7], tarikh=D, ringkas=status(kami).get('beli', {}), **banding_beli(kami, claude, cb, D))


def status(folder):
    p = os.path.join(folder, 'status_harian.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def potong_stor(S, out):
    os.makedirs(out, exist_ok=True)
    Si = int(S.replace('-', ''))
    for f in ('harga_A.csv', 'harga_B.csv', 'harga_idx.csv'):
        d = pd.read_csv(os.path.join(BS2, 'data/harga/stor', f))
        d[d.date <= Si].to_csv(os.path.join(out, f), index=False, float_format='%.6g')


def sesi_sebelum_tarikh(D):
    import exchange_calendars as xc
    c = xc.get_calendar('XNYS'); d = pd.Timestamp(D)
    return str(c.previous_session(d).date()) if c.is_session(d) else str(c.date_to_session(d, direction='previous').date())


# ---------------------------------------------------------------- laporan
def laporan(D, hasil, keluar):
    os.makedirs(keluar, exist_ok=True)
    L = [f'# Banding mod selari {D}: Actions (harian_c.py) lawan rutin Claude', '',
         'Setiap rutin Claude diulang tayang oleh `standard/harian_c.py` atas keadaan repo sebelum commit rutin itu '
         '(`standard/banding_bayang.py`). Beza dijangka: teks paparan, harga sementara 9:35 NY, gred P (masa data '
         'pemangkin), sumber tarikh earnings (SST Claude lawan Nasdaq/fail mingguan).', '']
    for h in hasil:
        L.append(f"## {h['peringkat']} ({h.get('commit')}, sesi {h.get('sesi') or h.get('tarikh')})")
        if h.get('ralat'):
            L += ['', f"RALAT: {h['ralat']}", '']; continue
        L += ['', '```', json.dumps(h['stat'], ensure_ascii=False, indent=1), '```', '']
        for k, v in (h.get('beza') or {}).items():
            if v:
                L += [f'**{k}** ({len(v)}):', ''] + [f'- {x}' for x in v[:25]] + ['']
        for k in ('hanya_kami', 'hanya_claude', 'watch_hanya_kami', 'watch_hanya_claude'):
            if h.get(k):
                L += [f'**{k}**: ' + ', '.join(h[k][:30]), '']
    p = os.path.join(keluar, f'BANDING_{D}.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    json.dump(hasil, open(os.path.join(keluar, f'BANDING_{D}.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    return p


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    x = sp.add_parser('hari'); x.add_argument('--tarikh', required=True); x.add_argument('--keluar', default=os.path.join(BS2, 'bayang'))
    for k in ('kemas', 'imbas', 'beli'):
        y = sp.add_parser(k); y.add_argument('--sasaran', required=True, nargs='+'); y.add_argument('--betul')
        y.add_argument('--keluar', default=os.path.join(BS2, 'bayang'))
    a = ap.parse_args(argv)
    hasil = []
    kerja = tempfile.mkdtemp(prefix='bayang_')
    try:
        if a.cmd == 'hari':
            # beli D diulang tayang dengan bar harian D: jika stor belum ada bar itu, jangan tulis laporan (larian
            # seterusnya mengulang); laporan yang sudah wujud tidak ditulis semula oleh harian.yml
            import exchange_calendars as xc
            akhir = int(pd.read_csv(os.path.join(BS2, 'data/harga/stor/harga_idx.csv'), usecols=['date']).date.max())
            if xc.get_calendar('XNYS').is_session(pd.Timestamp(a.tarikh)) and akhir < int(a.tarikh.replace('-', '')):
                print(f'stor harga belum ada bar {a.tarikh} (bar terakhir {akhir}); banding ditangguh')
                return
            cs = cari_commit(a.tarikh)
            seterus = cari_commit(str((pd.Timestamp(a.tarikh) + pd.Timedelta(days=1)).date())).get('kemas')
            tugas = [('kemas', cs.get('kemas')), ('imbas', cs['imbas'] or None), ('beli', cs.get('beli'))]
            D = a.tarikh
        else:
            tugas = [(a.cmd, a.sasaran if a.cmd == 'imbas' else a.sasaran[0])]
            seterus = a.betul
            D = 'manual'
        for k, c in tugas:
            if not c:
                hasil.append(dict(peringkat=k, ralat='tiada commit rutin Claude bagi tarikh ini')); continue
            d = os.path.join(kerja, k); os.makedirs(d)
            try:
                hasil.append(peringkat_kemas(c, d) if k == 'kemas' else peringkat_imbas(c, d) if k == 'imbas'
                             else peringkat_beli(c, d, seterus))
            except Exception as e:
                hasil.append(dict(peringkat=k, commit=str(c)[:20], ralat=f'{type(e).__name__}: {e}'))
        p = laporan(D, hasil, a.keluar)
        print(p)
        for h in hasil:
            print(h['peringkat'], json.dumps(h.get('stat') or h.get('ralat'), ensure_ascii=False))
    finally:
        shutil.rmtree(kerja, ignore_errors=True)


if __name__ == '__main__':
    main()
