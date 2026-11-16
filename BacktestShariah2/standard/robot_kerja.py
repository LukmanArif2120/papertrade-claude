"""Robot kerja: keadaan setiap kerja automatik projek untuk tab Robot dashboard (db `robot/kerja`).

Keputusan pengguna 16 Nov 2026 (selepas contoh v1, v2, galeri gaya dan v3 3D): tab sendiri di rel kiri, pejabat 3D,
robot gaya C (kepala skrin). PAPARAN SAHAJA: tiada keputusan, tiada isyarat, tidak dibaca oleh kad skor.

Setiap robot = satu kerja automatik yang sudah berjalan:
  * GitHub Actions  -> larian dibaca daripada `data/robot/larian.json`, ditulis oleh `robot_larian.py` dalam
    `harian.yml` (API GitHub Actions; hanya Actions yang ada token untuk membacanya).
  * Tugasan berjadual Claude -> tiada API dalam sesi berjadual, jadi larian DIKESAN daripada kesannya:
      - tolak db / paparan awal / semak tolakan: sesi itu sendiri yang menjalankan jana_db.py, jadi masa larian
        semasa direkod dalam medan `robot_claude` daftar `meta/versi_db` (dibawa dari larian ke larian oleh
        tolak_db.md langkah 3 dan 5c tanpa perubahan prosedur; jana_db.py membaca dan menulis medan itu);
      - pengejut penjaga: `penjaga_jadual.yml` dicetus tangan (workflow_dispatch) tepat pada minit :20 jadualnya;
      - analisis mingguan: komit "Analisis mingguan" dalam git;
      - penyemak tolakan tidak meninggalkan kesan bila semuanya baik (keadaan "senyap").

Status: siap (larian terakhir berjaya), gagal, lewat (tiada larian lebih lama daripada jurang jadual terpanjang
+ 6 jam), senyap (tiada yang perlu dilapor), belum (belum pernah berjalan). Ulang tayang = 24 jam (03:00-03:00 MYT)
paling sibuk dalam data larian.

Guna:  python3 BacktestShariah2/standard/robot_kerja.py [--masa 2026-11-16T10:04] > robot.json
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AKAR = os.path.dirname(BS2)
LARIAN = os.path.join(BS2, 'data', 'robot', 'larian.json')
UTC = timezone.utc
MYT = 'Asia/Kuala_Lumpur'
NY = 'America/New_York'

BILIK = [
    dict(id='pusat', nama='Pusat kawalan'),
    dict(id='data', nama='Data'),
    dict(id='pt', nama='Papertrade'),
    dict(id='analisis', nama='Analisis'),
    dict(id='carian', nama='Carian setup'),
    dict(id='dash', nama='Dashboard'),
]

# id, bilik, nama, kerja, sumber ('wf:<fail>' | 'claude:<kunci>'), cron, zon cron, teks jadual
KATALOG = [
    ('penjaga', 'pusat', 'Penjaga jadual', 'Setiap 30 minit: semak kerja yang lewat dan hidupkan semula.',
     'wf:penjaga_jadual.yml', ['23 * * * *', '53 * * * *'], 'UTC', 'Setiap 30 minit + selepas setiap kerja'),
    ('cetus', 'pusat', 'Pengejut penjaga', 'Kejutkan penjaga jadual enam kali sehari.',
     'claude:cetus', ['20 5,6,12,14,22,23 * * 1-6'], 'UTC', '6 kali sehari, Isn–Sab'),
    ('pengawal', 'pusat', 'Pengawal papertrade', 'Semak data papertrade lengkap; betulkan yang selamat.',
     'wf:pengawal.yml', ['35 12 * * 1-5', '0 16 * * 1-5'], 'UTC', '2 kali sehari Isn–Jum + selepas Lejar'),
    ('semak', 'pusat', 'Penyemak kod & data', 'Uji kod dan data setiap kali repo berubah.',
     'wf:semak_data.yml', None, 'UTC', 'Setiap kali repo berubah'),
    ('loceng', 'pusat', 'Loceng amaran', 'Hantar amaran ke telefon (ntfy) bila ada kerja gagal.',
     'wf:amaran_ntfy.yml', None, 'UTC', 'Selepas setiap kerja (berbunyi jika gagal sahaja)'),
    ('sandaran', 'pusat', 'Sandaran', 'Simpan salinan data penting setiap minggu.',
     'wf:sandaran.yml', ['19 2 * * 6'], 'UTC', 'Seminggu sekali, Sabtu'),
    ('harga', 'data', 'Harga harian', 'Ambil harga tutup semua saham (Yahoo).',
     'wf:harga_harian.yml', ['37 21 * * 1-5', '23 0 * * 2-6'], 'UTC', '2 kali selepas pasaran AS tutup'),
    ('harian', 'data', 'Kemas kini harian', 'Proses harga baharu: posisi papertrade, isyarat semua kaedah, gred.',
     'wf:harian.yml', ['7 5 * * 2-6', '7 7 * * 2-6', '7 9 * * 2-6', '7 11 * * 2-6'], 'UTC', '4 kali sehari, Sel–Sab'),
    ('rs', 'data', 'Kekuatan relatif', 'Kira kekuatan setiap saham lawan pasaran.',
     'wf:rs_pasaran.yml', ['41 22 * * 1-5', '17 3 * * 2-6'], 'UTC', '2 kali sehari selepas pasaran tutup'),
    ('gred', 'data', 'Gred sektor & industri', 'Beri gred kepada setiap sektor dan industri.',
     'wf:gred_kumpulan.yml', ['17 4 * * 2-6', '17 8 * * 2-6'], 'UTC', '2 kali sehari, Sel–Sab'),
    ('tv', 'data', 'Saringan TradingView', 'Saring saham daripada TradingView.',
     'wf:skrin_tv.yml', ['47 21 * * 1-5'], 'UTC', 'Sekali sehari selepas pasaran tutup'),
    ('sec', 'data', 'Laporan syarikat (SEC)', 'Ambil EPS dan hasil jualan syarikat daripada SEC.',
     'wf:fundamental_sec.yml', ['41 23 * * 1-5', '11 4 * * 2-6'], 'UTC', '2 kali sehari'),
    ('bursa', 'data', 'Senarai bursa', 'Semak saham baharu dan saham yang keluar bursa.',
     'wf:senarai_bursa.yml', ['53 23 * * 1-5', '23 4 * * 2-6'], 'UTC', '2 kali sehari'),
    ('edgar', 'data', 'Ambil alih', 'Cari syarikat yang sedang diambil alih (EDGAR).',
     'wf:edgar.yml', ['17 23 * * 1-5', '47 3 * * 2-6'], 'UTC', '2 kali sehari'),
    ('institusi', 'data', 'Dana besar (13F)', 'Kumpul pegangan dana besar.',
     'wf:institusi.yml', ['37 3 * * 1'], 'UTC', 'Seminggu sekali, Isnin'),
    ('petang', 'pt', 'Gred petang', 'Segarkan gred berita & earnings sebelum pasaran AS buka.',
     'wf:petang.yml', ['47 11 * * 1-5', '17 12 * * 1-5'], 'UTC', 'Petang Isn–Jum'),
    ('beli', 'pt', 'Beli 9:35 NY', 'Rekod belian papertrade pada harga buka (tiada wang sebenar).',
     'wf:beli.yml', ['40 13 * * 1-5', '40 14 * * 1-5', '25 16 * * 1-5', '25 17 * * 1-5', '25 19 * * 1-5',
                     '25 20 * * 1-5'], 'UTC', 'Malam Isn–Jum (pasaran AS buka)'),
    ('lejar', 'pt', 'Lejar penuh', 'Rekod setiap isyarat beli dan jual semua kaedah.',
     'wf:lejar.yml', ['17 6 * * 2-6', '17 10 * * 2-6'], 'UTC', '2 kali sehari, Sel–Sab'),
    ('papan', 'analisis', 'Papan penganalisis', 'Kira kad skor dan papan kaedah selepas Lejar.',
     'wf:analisis.yml', None, 'UTC', 'Selepas setiap Lejar'),
    ('mingguan', 'analisis', 'Analisis mingguan', 'Semak prestasi papertrade (Claude).',
     'claude:mingguan', ['52 9 * * 6'], MYT, 'Sabtu 9:52 pagi'),
    ('suku', 'analisis', 'Tala suku tahunan', 'Cadang tala semula parameter (Claude); cadangan sahaja.',
     'claude:suku', ['49 9 1 1,4,7,10 *'], MYT, '1 Jan, Apr, Jul, Okt'),
    ('mesin', 'carian', 'Mesin carian setup', 'Cari dan tala setup baharu.',
     'wf:mesin_carian.yml', ['23 2 * * 0'], 'UTC', 'Seminggu sekali, Ahad'),
    ('jejakf', 'carian', 'Jejak setup F', 'Papertrade maya setup F selepas Lejar.',
     'wf:jejak_f.yml', None, 'UTC', 'Selepas setiap Lejar'),
    ('awal', 'dash', 'Paparan awal', 'Hantar harga tutup awal ke dashboard (Claude).',
     'claude:awal', ['47 6 * * 2-6'], MYT, '6:47 pagi, Sel–Sab'),
    ('tolak_ptg', 'dash', 'Hantar data petang', 'Hantar data muktamad ke dashboard (Claude).',
     'claude:tolak_ptg', ['41 16 * * 2-6'], MYT, '4:41 petang, Sel–Sab'),
    ('tolak_ny', 'dash', 'Hantar data malam', 'Hantar data ke dashboard selepas kerja malam (Claude).',
     'claude:tolak_ny', ['20 10 * * 1-6'], NY, '10:20 pagi New York, Isn–Sab'),
    ('semak_db', 'dash', 'Penyemak dashboard', 'Pastikan dashboard benar-benar dikemas kini (Claude).',
     'claude:semak_db', ['20 12 * * 1-6'], NY, '12:20 tengah hari New York, Isn–Sab'),
]
# siapa memberi kerja kepada siapa (robot pembawa kotak dalam ulang tayang)
ALIRAN = [('harga', 'harian'), ('harga', 'lejar'), ('lejar', 'papan'), ('lejar', 'jejakf'), ('lejar', 'pengawal'),
          ('harian', 'tolak_ptg'), ('papan', 'tolak_ptg'), ('harian', 'tolak_ny'), ('papan', 'tolak_ny'),
          ('tolak_ny', 'semak_db'), ('petang', 'beli'), ('harga', 'awal')]
GAGAL = ('failure', 'timed_out', 'startup_failure')


def iso(d):
    return d.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def dt(s):
    return datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=UTC)


def _zon(nama):
    if nama == 'UTC' or ZoneInfo is None:
        return UTC
    return ZoneInfo(nama)


def _medan(f, lo, hi):
    out = set()
    for bah in f.split(','):
        lang = 1
        if '/' in bah:
            bah, lang = bah.split('/')
            lang = int(lang)
        if bah == '*':
            a, b = lo, hi
        elif '-' in bah:
            a, b = map(int, bah.split('-'))
        else:
            a = b = int(bah)
        out.update(range(a, b + 1, lang))
    return out


def tembakan(crons, mula, hari=21, zon='UTC', had=None):
    """Masa tembakan cron (UTC) selepas `mula` dalam `hari` hari; cron ditafsir dalam zon `zon`."""
    tz = _zon(zon)
    sp = []
    for c in crons:
        m, h, dom, mon, dow = c.split()
        sp.append((_medan(m, 0, 59), _medan(h, 0, 23), _medan(dom, 1, 31), _medan(mon, 1, 12), _medan(dow, 0, 6)))
    out = []
    t = mula.astimezone(UTC).replace(second=0, microsecond=0) + timedelta(minutes=1)
    akhir = t + timedelta(days=hari)
    while t < akhir:
        lt = t.astimezone(tz)
        d = lt.isoweekday() % 7
        for M, H, DOM, MON, DOW in sp:
            if lt.minute in M and lt.hour in H and lt.day in DOM and lt.month in MON and d in DOW:
                out.append(t)
                break
        if had and len(out) >= had:
            break
        # langkau terus ke jam seterusnya jika jam ini tiada dalam mana-mana cron (pantas untuk jadual jarang)
        if not any(lt.hour in H for _, H, _, _, _ in sp):
            t = (t + timedelta(hours=1)).replace(minute=0)
        else:
            t += timedelta(minutes=1)
    return out


def baca_larian(path=LARIAN):
    """{'dibina': iso, 'runs': [[wf, mula, akhir, status, hasil, peristiwa], ...]} atau None."""
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        return d if isinstance(d.get('runs'), list) else None
    except (OSError, ValueError):
        return None


def mingguan_git(n=3):
    """Masa komit 'Analisis mingguan' terkini (rekod larian tugasan Claude Sabtu)."""
    try:
        out = subprocess.run(['git', '-C', AKAR, 'log', f'-n{n}', '--format=%cI', '--grep', '^Analisis mingguan'],
                             capture_output=True, text=True, timeout=20).stdout.split()
        return [iso(datetime.fromisoformat(x)) for x in out if x]
    except Exception:
        return []


def tugas_claude_semasa(masa, awal=False):
    """Tugasan Claude yang sedang menjalankan jana_db.py, ikut masa larian (atau None = sesi tangan)."""
    if awal:
        return 'awal'
    ny = masa.astimezone(_zon(NY))
    my = masa.astimezone(_zon(MYT))
    if 16 <= my.hour <= 18:
        return 'tolak_ptg'
    if 10 <= ny.hour <= 11:
        return 'tolak_ny'
    if 12 <= ny.hour <= 13:
        return 'semak_db'
    return None


def kemas_robot_claude(lama, masa, awal=False):
    """Daftar larian tugasan Claude {kunci: {mula, akhir, hasil}} selepas larian jana_db.py ini."""
    rc = {k: v for k, v in (lama or {}).items() if isinstance(v, dict)}
    t = tugas_claude_semasa(masa, awal)
    if t:
        rc[t] = dict(mula=iso(masa), akhir=iso(masa), hasil='success')
    return rc


def bina(masa=None, larian=None, robot_claude=None, mingguan=None, ulang_jam=24):
    """Dokumen db robot/kerja. `masa`: datetime (UTC/aware); `larian`: hasil baca_larian()."""
    masa = (masa or datetime.now(UTC)).astimezone(UTC)
    larian = larian if larian is not None else baca_larian()
    runs = (larian or {}).get('runs') or []
    snap = dt(larian['dibina']) if larian and larian.get('dibina') else None
    segar = snap is not None and (masa - snap) < timedelta(minutes=90)
    ikut = {}
    for r in runs:
        if len(r) < 6:
            continue
        wf, mula, akhir, status, hasil, ev = r[:6]
        if status != 'completed':
            if not segar:
                continue          # larian 'sedang berjalan' dalam petikan lama: tidak diketahui sekarang
            hasil = 'in_progress'
        ikut.setdefault(wf, []).append((mula, akhir or mula, hasil or '', ev or ''))
    for v in ikut.values():
        v.sort()
    rc = robot_claude or {}
    if mingguan is None:
        mingguan = mingguan_git()
    # pengejut penjaga: penjaga_jadual dicetus tangan tepat pada minit :20 jam jadualnya
    cetus = [r for r in ikut.get('penjaga_jadual.yml', [])
             if r[3] == 'workflow_dispatch' and r[0][14:16] in ('20', '21') and int(r[0][11:13]) in (5, 6, 12, 14, 22, 23)]
    sejak = min((r[0] for v in ikut.values() for r in v), default=None)

    # tetingkap ulang tayang: 24 jam (03:00-03:00 MYT) paling sibuk
    ulang = None
    if runs:
        hujung = masa
        calon = []
        mula0 = (masa - timedelta(days=4)).astimezone(_zon(MYT)).replace(hour=3, minute=0, second=0, microsecond=0)
        t = mula0
        while t < hujung:
            a, b = t.astimezone(UTC), (t + timedelta(hours=ulang_jam)).astimezone(UTC)
            n = sum(1 for v in ikut.values() for r in v if iso(a) <= r[0] < iso(b) and r[2] != 'skipped')
            calon.append((n, a, b))
            t += timedelta(days=1)
        n, a, b = max(calon, key=lambda x: (x[0], x[1]))
        if n:
            ulang = dict(mula=iso(a), akhir=iso(min(b, masa)))

    def dalam(r):
        return ulang and ulang['mula'] <= r[0] < ulang['akhir']

    robot = []
    for rid, bil, nama, kerja, sumber, cron, zon, jadual in KATALOG:
        d = dict(id=rid, bilik=bil, nama=nama, kerja=kerja, jadual=jadual)
        jenis, kunci = sumber.split(':', 1)
        if jenis == 'wf':
            d['jenis'] = 'GitHub Actions'
            d['rujukan'] = kunci
            semua = ikut.get(kunci, [])
            nyata = [r for r in semua if r[2] not in ('cancelled', 'in_progress')]
            jalan = [r for r in semua if r[2] == 'in_progress']
            a = nyata[-1] if nyata else None
            d['akhir'] = dict(mula=a[0], akhir=a[1], hasil=a[2]) if a else None
            d['sedang'] = bool(jalan)
            d['ulang'] = [[r[0], r[1], r[2], {'workflow_dispatch': 'penjaga', 'workflow_run': 'aliran'}.get(r[3], 'jadual')]
                          for r in semua if dalam(r) and r[2] not in ('skipped', 'in_progress')]
            k = {}
            for r in semua:
                if r[2] != 'in_progress':
                    k[r[2]] = k.get(r[2], 0) + 1
            d['kiraan'] = k
        else:
            d['jenis'] = 'Claude (tugasan berjadual)'
            d['rujukan'] = 'tugasan berjadual Claude'
            d['sedang'] = False
            d['kiraan'] = None
            if kunci == 'cetus':
                a = cetus[-1] if cetus else None
                d['akhir'] = dict(mula=a[0], akhir=a[1], hasil='success') if a else None
                d['ulang'] = [[r[0], r[1], 'success', 'jadual'] for r in cetus if dalam(r)]
            elif kunci == 'mingguan':
                d['akhir'] = dict(mula=mingguan[0], akhir=mingguan[0], hasil='success') if mingguan else None
                d['ulang'] = [[x, x, 'success', 'jadual'] for x in mingguan if dalam((x,))]
            else:
                x = rc.get(kunci)
                d['akhir'] = dict(mula=x['mula'], akhir=x.get('akhir') or x['mula'], hasil=x.get('hasil', 'success')) if x else None
                d['ulang'] = [[x['mula'], x.get('akhir') or x['mula'], 'success', 'jadual']] if x and dalam((x['mula'],)) else []
        # seterusnya + had lewat
        d['seterusnya'] = None
        had = None
        if cron:
            f = tembakan(cron, masa, hari=100 if rid == 'suku' else 21, zon=zon, had=None if rid != 'suku' else 1)
            d['seterusnya'] = iso(f[0]) if f else None
            if len(f) > 2 and rid != 'suku':
                had = max((f[i + 1] - f[i]).total_seconds() for i in range(len(f) - 1)) / 3600 + 6
        a = d['akhir']
        if a is None:
            st = 'senyap' if rid == 'semak_db' else 'belum'
        elif a['hasil'] in GAGAL:
            st = 'gagal'
        elif a['hasil'] == 'skipped':
            st = 'senyap'
        else:
            st = 'siap'
            if had and (masa - dt(a['mula'])).total_seconds() / 3600 > had:
                st = 'lewat'
        if rid == 'semak_db' and st == 'belum':
            st = 'senyap'
        # paparan awal boleh melangkau hari tanpa data baharu, dan penyemak tolakan tidak meninggalkan kesan bila
        # semua baik: rekod basi bagi kedua-duanya bukan tanda rosak (amaran sebenar: tolak_db_semak.md + ntfy)
        if rid in ('awal', 'semak_db') and st == 'lewat':
            st = 'senyap'
        d['status'] = st
        robot.append(d)
    return dict(
        versi=1, kini=iso(masa), dibina=iso(masa),
        larian_pada=larian.get('dibina') if larian else None, kiraan_sejak=sejak,
        ulang=ulang, bilik=BILIK, robot=robot, aliran=ALIRAN,
        sumber='GitHub Actions (data/robot/larian.json, robot_larian.py dalam harian.yml) + kesan tugasan Claude '
               '(meta/versi_db.robot_claude, komit git)',
        nota='Paparan sahaja. Setiap robot = satu kerja automatik projek; tiada keputusan atau isyarat.')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--masa', help='masa UTC ISO (lalai: sekarang)')
    ap.add_argument('--larian', default=LARIAN)
    a = ap.parse_args(argv)
    masa = datetime.fromisoformat(a.masa).replace(tzinfo=UTC) if a.masa else None
    json.dump(bina(masa=masa, larian=baca_larian(a.larian)), sys.stdout, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
