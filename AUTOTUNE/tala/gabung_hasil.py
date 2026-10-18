# Gabung hasil penalaan daripada beberapa direktori (artifak shard dan direktori repo) → satu direktori keluar.
# Bagi setiap Mxx/kNN.json dipilih versi TERBAIK:
#   1. hanya JSON yang boleh dihurai (fail rosak, cth. "Extra data", diabaikan);
#   0. (Pindaan 18 Okt 2026) JSON yang `versi_kod`nya sama dengan cincangan fail kaedah semasa
#      (AUTOTUNE/kaedah/Mxx.py) didahulukan, supaya hasil tala semula selepas pembetulan kod menang;
#   2. SIAP lengkap (n_trials ≥ n_sasaran) — antaranya n_trials_diminta terbesar, kemudian `mula` terbaharu;
#   3. jika tiada, SIAP separa dengan n_trials terbanyak (kemudian terbaharu);
#   4. jika tiada, apa-apa JSON sah (RALAT) — n_trials terbanyak, kemudian terbaharu.
# Fail ditulis secara atomik (fail sementara + os.replace) supaya tiada sisa kandungan lama. Fail keluar yang rosak
# dan tiada ganti yang sah dibuang. _masa.csv dibina semula daripada JSON terpilih (masa.py).
# Guna: python3 gabung_hasil.py [--keluar DIR] [--percubaan 120] DIR1 [DIR2 ...]
#   Direktori keluar sentiasa turut dinilai sebagai calon. Setiap DIR mengandungi Mxx/kNN.json.
import os, sys, json, glob, shutil, argparse, tempfile, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import masa

KELUAR = masa.KELUAR
DIR_KAEDAH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kaedah'))


def versi_kod(mid, dir_kaedah=DIR_KAEDAH):
    """16 aksara pertama sha256 fail AUTOTUNE/kaedah/Mxx.py (None jika tiada). A02: 'Mxx_<lorong>' → Mxx.py."""
    for nama in ([mid, mid.split('_')[0]] if '_' in str(mid) else [mid]):
        try:
            with open(os.path.join(dir_kaedah, nama + '.py'), 'rb') as fh: return hashlib.sha256(fh.read()).hexdigest()[:16]
        except OSError: continue
    return None


def baca(f):
    """Pulang dict hasil jika fail JSON sah dan sepadan dengan laluannya; selain itu None."""
    try:
        with open(f, 'rb') as fh: H = json.loads(fh.read().decode('utf-8'))
    except Exception: return None
    if not isinstance(H, dict): return None
    mid = os.path.basename(os.path.dirname(f)); nama = os.path.basename(f)
    if H.get('kaedah') not in (None, mid): return None
    try:
        if H.get('kajian') is not None and f"k{int(H['kajian']):02d}.json" != nama: return None
    except (TypeError, ValueError): return None
    return H


def _n(x):
    try: return float(x)
    except (TypeError, ValueError): return 0.0


def lengkap(H):
    """SIAP dan bilangan percubaan mencapai sasaran."""
    if H.get('status') != 'SIAP': return False
    sas = H.get('n_sasaran', H.get('n_trials_diminta'))
    return _n(H.get('n_trials')) >= _n(sas)


def taraf(H, semasa=None):
    """Kunci susunan (lebih besar = lebih baik). semasa: versi_kod fail kaedah sekarang (padanan didahulukan)."""
    mula = str(H.get('mula') or '')
    v = int(semasa is not None and H.get('versi_kod') == semasa)
    if lengkap(H): return (v, 3, _n(H.get('n_trials_diminta')), mula)
    if H.get('status') == 'SIAP': return (v, 2, _n(H.get('n_trials')), mula)
    return (v, 1, _n(H.get('n_trials')), mula)


def kelas(H):
    if lengkap(H): return 'lengkap'
    return 'separa' if H.get('status') == 'SIAP' else 'RALAT'


def tulis_atomik(sumber, f):
    d = os.path.dirname(f); os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.gabung_', suffix='.tmp', dir=d)
    try:
        with os.fdopen(fd, 'wb') as fo, open(sumber, 'rb') as fi: shutil.copyfileobj(fi, fo)
        os.replace(tmp, f)
    except BaseException:
        if os.path.exists(tmp): os.remove(tmp)
        raise


def gabung(dirs, keluar=KELUAR, percubaan=None, masa_csv=True, dir_kaedah=DIR_KAEDAH):
    """Pulang dict kiraan. dirs: senarai direktori calon (keluar ditambah secara automatik di hadapan)."""
    keluar = os.path.abspath(keluar)
    senarai, lihat = [], set()
    for d in [keluar] + list(dirs):
        r = os.path.realpath(d)
        if r in lihat or not os.path.isdir(d): continue
        lihat.add(r); senarai.append(d)
    calon = {}   # (Mxx, kNN.json) → [(fail, H|None)]
    for d in senarai:
        for f in sorted(glob.glob(os.path.join(d, 'M*', 'k*.json'))):
            k = (os.path.basename(os.path.dirname(f)), os.path.basename(f))
            calon.setdefault(k, []).append((f, baca(f)))
    C = dict(lengkap=0, separa=0, RALAT=0, rosak_diabai=0, ditulis=0, dibuang=0, perlu_kerja=0)
    for (mid, nama), L in sorted(calon.items()):
        sah = [(f, H) for f, H in L if H is not None]
        C['rosak_diabai'] += len(L) - len(sah)
        sasaran = os.path.join(keluar, mid, nama)
        if not sah:
            if os.path.exists(sasaran): os.remove(sasaran); C['dibuang'] += 1
            C['perlu_kerja'] += 1
            continue
        f, H = sah[0]; v = versi_kod(mid, dir_kaedah)
        for g, J in sah[1:]:   # seri: calon terawal (direktori keluar dahulu) dikekalkan
            if taraf(J, v) > taraf(H, v): f, H = g, J
        C[kelas(H)] += 1
        if not lengkap(H) or (percubaan is not None and _n(H.get('n_trials_diminta')) < percubaan):
            C['perlu_kerja'] += 1
        if os.path.realpath(f) != os.path.realpath(sasaran):
            semasa = None
            if os.path.exists(sasaran):
                with open(sasaran, 'rb') as fh: semasa = fh.read()
            with open(f, 'rb') as fh: baru = fh.read()
            if semasa != baru: tulis_atomik(f, sasaran); C['ditulis'] += 1
    C['tugasan'] = len(calon)
    if masa_csv: masa.main(keluar)
    return C


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--keluar', default=KELUAR)
    a.add_argument('--percubaan', type=float, default=None, help='sasaran percubaan untuk kiraan perlu_kerja')
    a.add_argument('dirs', nargs='*')
    x = a.parse_args(argv)
    C = gabung(x.dirs, x.keluar, x.percubaan)
    print(f"gabung: {C['tugasan']} tugasan daripada {len(x.dirs)} direktori calon")
    print(f"  lengkap {C['lengkap']} | separa {C['separa']} | RALAT {C['RALAT']}")
    print(f"  fail rosak diabaikan {C['rosak_diabai']} | ditulis {C['ditulis']} | dibuang (tiada versi sah) {C['dibuang']}")
    print(f"  masih perlu kerja (antara fail sedia ada) {C['perlu_kerja']}")
    return C


if __name__ == '__main__':
    main()
