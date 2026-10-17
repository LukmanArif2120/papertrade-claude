# Bina JULAT dan TALA bagi setiap salinan berparameter (SPEC §2), suntik ke fail Mxx.py, tulis param_julat.csv.
# Heuristik: int tetingkap/tempoh 0.5x–2x (min 2; tmax had 60); float pengganda/ambang 0.5x–1.5x
# (aras gaya RSI dikepit [1,99]; pecahan (0,1) dikepit [0.01,0.99]); pemalar struktur dibekukan.
# TALA (<= 6): henti/sasaran/keluar dahulu, kemudian tetingkap/ambang isyarat utama.
# Peranan = lajur output (sig/stop/tgt/exitc/rank) yang bergantung pada parameter (aliran data ringkas atas AST salinan).
# Guna: python3 AUTOTUNE/kaedah/pilih_julat.py [Mxx ...|semua] [--sahkan N]  (--sahkan: uji sedia() pada bawah/atas TALA)
import argparse, ast, csv, glob, json, os, re, sys

AKAR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SINI = os.path.join(AKAR, 'AUTOTUNE', 'kaedah')
META = os.path.join(SINI, 'param_meta.json')
CSV = os.path.join(SINI, 'param_julat.csv')
BLOK_JT = '# --- JULAT/TALA (pilih_julat.py) ---'
LAJUR = ('sig', 'stop', 'tgt', 'exitc', 'rank')
STRUKTUR = {100, 252, 365, 360, 1000, 10000, 1e6, 1e9, 100.0, 252.0, 365.0, 0.015}   # 0.015 = pemalar CCI
FN_BEKU = {'round', 'zeros', 'ones', 'full', 'empty', 'reshape', 'percentile_a0', 'mod', 'pow', 'power', 'sqrt', 'log',
           'astype', 'linspace', 'tile', 'repeat', 'broadcast_to', 'concatenate', 'Timedelta', 'DateOffset', 'Timestamp',
           'timedelta', 'nlargest', 'nsmallest', 'head', 'tail', 'iloc', 'resample'}
NAMA_BEKU = ('cost', 'kos', 'slot', 'start', 'mula_tarikh', 'tahun', 'bulan')
GAYA_RSI = ('rsi', 'stoch', 'mfi', 'wr', 'williams', 'crsi', 'pct_k', 'pctl', 'persentil', 'pctile', 'pr', 'pct_rank')
K145_HENTI = ('henti_atr', 'henti_pct', 'henti_low', 'keluar_ema', 'keluar_sma', 'keluar_chan', 'keluar_chan_tinggi',
              'keluar_chan_atr', 'had_henti')
# Pembetulan manual selepas pengesahan sempadan ((kaedah, nama) -> 'beku' atau ('int'|'float', bawah, atas)).
MANUAL = {('M34', 'rolling_20'): 'beku', ('M34', 'linreg_end_20'): 'beku'}   # _X = np.arange(20) peringkat modul


# ---------------- aliran data (peranan) ----------------
class Aliran:
    def __init__(self, tree):
        self.fn = {}
        for s in tree.body:
            if isinstance(s, ast.FunctionDef): self.fn[s.name] = s
            elif isinstance(s, ast.Assign) and isinstance(s.targets[0], ast.Name) and isinstance(s.value, ast.Lambda):
                self.fn[s.targets[0].id] = s.value
        self._semua, self._out = {}, {}

    @staticmethod
    def param_dalam(nod):
        r = set()
        for n in ast.walk(nod):
            if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == 'P' \
                    and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str): r.add(n.slice.value)
            elif isinstance(n, ast.Name) and n.id.startswith('_p_'): r.add(n.id[3:])
        return r

    def semua(self, f, jejak=()):
        if f in self._semua: return self._semua[f]
        if f in jejak: return set()
        nod = self.fn[f]; r = self.param_dalam(nod)
        for n in ast.walk(nod):
            if isinstance(n, ast.Name) and n.id in self.fn and n.id != f: r |= self.semua(n.id, jejak + (f,))
        self._semua[f] = r
        return r

    def E(self, e, env):
        if e is None: return set()
        if isinstance(e, ast.Subscript) and isinstance(e.value, ast.Name) and e.value.id == 'P' and isinstance(e.slice, ast.Constant):
            return {e.slice.value}
        if isinstance(e, ast.Name):
            if e.id.startswith('_p_'): return {e.id[3:]}
            if e.id in self.fn: return set(self.semua(e.id))
            return set(env.get(e.id, ()))
        if isinstance(e, ast.Subscript) and isinstance(e.slice, ast.Constant) and isinstance(e.slice.value, str):
            return set(env.get('col:' + e.slice.value, ())) | self.E(e.value, env)
        if isinstance(e, ast.Attribute):
            return set(env.get('col:' + e.attr, ())) | self.E(e.value, env)
        if isinstance(e, ast.Lambda): return self.E(e.body, env) | self.param_dalam(e)
        r = set()
        for c in ast.iter_child_nodes(e): r |= self.E(c, env)
        return r

    def tetap(self, t, nilai, env, out, nod_nilai=None):
        if isinstance(t, ast.Name): env[t.id] = env.get(t.id, set()) | nilai
        elif isinstance(t, (ast.Tuple, ast.List)):
            hf = nod_nilai.func.id if isinstance(nod_nilai, ast.Call) and isinstance(nod_nilai.func, ast.Name) else None
            ret = self.pulang(hf) if hf in self.fn else None
            if ret is not None and len(ret) == len(t.elts):
                ar = self._ctx.copy()
                for x in nod_nilai.args: ar |= self.E(x, env)
                for k in nod_nilai.keywords:
                    if k.arg != 'P': ar |= self.E(k.value, env)
                for a, r in zip(t.elts, ret): self.tetap(a, ar | r, env, out)
            elif isinstance(nod_nilai, (ast.Tuple, ast.List)) and len(nod_nilai.elts) == len(t.elts):
                for a, b in zip(t.elts, nod_nilai.elts): self.tetap(a, self._ctx | self.E(b, env), env, out, b)
            else:
                for a in t.elts: self.tetap(a, nilai, env, out)
        elif isinstance(t, ast.Subscript):
            cols = [n.value for n in ast.walk(t.slice) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            for c in cols:
                if c in LAJUR: out[c] = out.get(c, set()) | nilai
                env['col:' + c] = env.get('col:' + c, set()) | nilai
            if not cols:
                b = t.value
                while isinstance(b, (ast.Subscript, ast.Attribute)): b = b.value
                if isinstance(b, ast.Name): env[b.id] = env.get(b.id, set()) | nilai | self.E(t.slice, env)
        elif isinstance(t, ast.Attribute):
            env['col:' + t.attr] = env.get('col:' + t.attr, set()) | nilai

    def panggilan(self, c, env, out):
        """Kesan sampingan panggilan: pembantu yang menulis lajur output, siap_lajur, pasang."""
        fn = c.func.id if isinstance(c.func, ast.Name) else None
        ar = self._ctx.copy()
        for a in c.args: ar |= self.E(a, env)
        for k in c.keywords:
            if k.arg != 'P': ar |= self.E(k.value, env)
        if fn == 'siap_lajur':
            kw = {k.arg: k.value for k in c.keywords}
            pos = ['g', 'sig', 'stop', 'exitc', 'tgt']
            for i, a in enumerate(c.args): kw[pos[i]] = a
            for col in ('sig', 'stop', 'exitc', 'tgt'):
                if col in kw: out[col] = out.get(col, set()) | self._ctx | self.E(kw[col], env)
            out['rank'] = out.get('rank', set()) | {'rank_shift_63'}
        elif fn == 'pasang':
            out['stop'] = out.get('stop', set()) | {k for k in K145_HENTI if k.startswith('henti') or k == 'had_henti'}
            out['exitc'] = out.get('exitc', set()) | {k for k in K145_HENTI if k.startswith('keluar')}
            out['tgt'] = out.get('tgt', set())
        elif fn in self.fn:
            oh = self.output(fn)
            for col, s in oh.items(): out[col] = out.get(col, set()) | s | ar
        # mutasi kaedah (cth. x.fillna(inplace=True)) diabaikan

    def output(self, f):
        if f in self._out: return self._out[f]
        self._out[f] = {}; self._ret = getattr(self, '_ret', {}); self._ret.setdefault(f, None)
        nod = self.fn[f]
        env, out = {}, {}
        simpan = getattr(self, '_ctx', set())
        self._ctx = set()
        if isinstance(nod, ast.FunctionDef):
            for _ in range(2): self.badan(nod.body, env, out, set())
            # taint setiap unsur tuple yang dipulangkan (jika semua return ialah tuple sama panjang)
            rs = [n.value for n in ast.walk(nod) if isinstance(n, ast.Return) and n.value is not None]
            if rs and all(isinstance(r, ast.Tuple) for r in rs) and len({len(r.elts) for r in rs}) == 1:
                ret = [set() for _ in rs[0].elts]
                for r in rs:
                    for i, e in enumerate(r.elts): ret[i] |= self.E(e, env)
                self._ret[f] = ret
        self._out[f] = out
        self._ctx = simpan
        return out

    def pulang(self, f):
        self.output(f)
        return self._ret.get(f)

    def badan(self, stmts, env, out, ctx):
        for s in stmts:
            self._ctx = ctx
            if isinstance(s, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                v = ctx | self.E(s.value, env)
                tg = s.targets if isinstance(s, ast.Assign) else [s.target]
                for t in tg: self.tetap(t, v, env, out, s.value)
                for c in ast.walk(s.value):
                    if isinstance(c, ast.Call): self.panggilan(c, env, out)
            elif isinstance(s, ast.Expr):
                v = s.value
                if isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) and isinstance(v.func.value, ast.Name) \
                        and v.func.attr in ('append', 'extend', 'update', 'insert', 'add', 'appendleft'):
                    b = v.func.value.id
                    env[b] = env.get(b, set()) | ctx | {p for x in v.args for p in self.E(x, env)}
                for c in ast.walk(s.value):
                    if isinstance(c, ast.Call): self._ctx = ctx; self.panggilan(c, env, out)
            elif isinstance(s, (ast.For, ast.AsyncFor)):
                it = ctx | self.E(s.iter, env)
                self.tetap(s.target, it, env, out)
                self.badan(s.body, env, out, it); self.badan(s.orelse, env, out, ctx)
            elif isinstance(s, (ast.If, ast.While)):
                t = ctx | self.E(s.test, env)
                self.badan(s.body, env, out, t); self.badan(s.orelse, env, out, t)
            elif isinstance(s, ast.FunctionDef):
                env[s.name] = self.param_dalam(s) | {p for n in ast.walk(s) if isinstance(n, ast.Name) for p in env.get(n.id, ())}
                sub_out = {}
                self.badan(s.body, dict(env), sub_out, ctx)
                for col, v in sub_out.items(): out[col] = out.get(col, set()) | v
            elif isinstance(s, (ast.With, ast.Try)):
                for b in ('body', 'orelse', 'finalbody'): self.badan(getattr(s, b, []) or [], env, out, ctx)
                for h in getattr(s, 'handlers', []): self.badan(h.body, env, out, ctx)
            self._ctx = ctx


def peranan(tree):
    a = Aliran(tree)
    out = a.output('sedia')
    r = {}
    for col in LAJUR:
        for p in out.get(col, ()): r.setdefault(p, set()).add(col)
    return r


# ---------------- julat ----------------
OP_AKHIR = ('_ambang', '_kali', '_tolak', '_tambah', '_bahagi', '_bahagi_bulat', '_mod', '_kuasa')


def info_struktur(tree):
    """Nama pembolehubah gelung/panjang, dan parameter yang dibanding dengan == / != (kod keadaan)."""
    gel, sama = {'len', 'size', 'shape', 'i', 'j', 'k'}, set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.For, ast.comprehension)):
            for x in ast.walk(n.target):
                if isinstance(x, ast.Name): gel.add(x.id.lower().strip('_'))
        elif isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) \
                and n.value.func.id == 'len':
            for t in n.targets:
                if isinstance(t, ast.Name): gel.add(t.id.lower().strip('_'))
        elif isinstance(n, ast.Compare) and any(isinstance(o, (ast.Eq, ast.NotEq)) for o in n.ops):
            for x in [n.left] + n.comparators:
                p = Aliran.param_dalam(x) if isinstance(x, (ast.Subscript, ast.Name)) else set()
                sama |= p
    return gel, sama


def julat(nama, v, m, per, mid='', st=(set(), set(), set())):
    """Pulangkan (jenis, bawah, atas, sebab_beku)."""
    F = set(m.get('flag', [])); r = m.get('peranan_kod', nama)
    gel, sama, nilai_sama = st
    hint = r
    for o in OP_AKHIR:
        if r.endswith(o): hint = r[: -len(o)]; break
    if hint != r and hint in gel: return 'beku', None, None, 'indeks gelung'
    if 'fn:range' in F: return 'beku', None, None, 'julat gelung'
    tug, hint_sama = nilai_sama
    if nama in sama and hint in tug: return 'beku', None, None, 'kod keadaan'
    if 'tugasan' in F and isinstance(v, int) and r in hint_sama: return 'beku', None, None, 'kod keadaan'
    fns = {f[3:] for f in F if f.startswith('fn:')}
    if (mid, nama) in MANUAL:
        x = MANUAL[(mid, nama)]
        return ('beku', None, None, 'manual') if x == 'beku' else (x[0], x[1], x[2], '')
    if isinstance(v, bool): return 'beku', None, None, 'bool'
    if nama == 'tmax':
        if v >= 60: return 'beku', None, None, 'tmax >= 60 (enjin had 60)'
        return 'int', max(2, round(v / 2)), min(60, 2 * v), ''
    if nama in ('henti_atr', 'henti_pct', 'keluar_chan'):
        return 'float', round(0.5 * v, 4), round(1.5 * v, 4), ''
    if nama == 'had_henti': return 'float', round(0.5 * v, 4), 0.99, ''
    if nama in ('henti_low',):
        return 'int', v if v < 2 else max(2, round(v / 2)), max(2, 2 * v), ''
    if 'indeks' in F: return 'beku', None, None, 'indeks'
    if 'kalendar' in F: return 'beku', None, None, 'kalendar'
    if 'purata' in F: return 'beku', None, None, 'purata'
    if 'op:kuasa' in F or 'op:mod' in F or 'op:bahagi_bulat' in F: return 'beku', None, None, 'struktur'
    if fns & FN_BEKU: return 'beku', None, None, 'fungsi struktur'
    if v in STRUKTUR or (isinstance(v, float) and abs(v) < 1e-4): return 'beku', None, None, 'struktur'
    if 'fn:quantile' in F and v == 0.5: return 'beku', None, None, 'median'
    if 'fn:median' in F: return 'beku', None, None, 'median'
    if any(k in nama for k in NAMA_BEKU): return 'beku', None, None, 'struktur'
    if v < 0:
        lo, hi = 1.5 * v, 0.5 * v
        return ('int', round(lo), round(hi), '') if isinstance(v, int) and round(lo) < round(hi) else \
               ('float', round(lo, 6), round(hi, 6), '')
    rsi = 'banding' in F and 1 < v < 100 and any(t in r.split('_') or r.startswith(t) for t in GAYA_RSI)
    if isinstance(v, int):
        if 'banding' in F and 'arg' not in F:
            lo, hi = max(1, round(0.5 * v)), max(round(1.5 * v), round(0.5 * v) + 1)
            if rsi: lo, hi = max(1, lo), min(99, hi)
            if lo >= hi: return 'beku', None, None, 'julat kosong'
            return 'int', lo, hi, ''
        if ('op:kali' in F or 'op:bahagi' in F) and 'dalam_arg' not in F and 'arg' not in F:
            return 'float', round(0.5 * v, 6), round(1.5 * v, 6), ''
        lo, hi = max(2, round(v / 2)), 2 * v
        if v < 2: lo = v
        if lo >= hi: return 'beku', None, None, 'julat kosong'
        return 'int', lo, hi, ''
    lo, hi = 0.5 * v, 1.5 * v
    if rsi: lo, hi = max(1.0, lo), min(99.0, hi)
    elif 0 < v < 1: lo, hi = max(0.01, lo), min(0.99, hi)
    return 'float', round(lo, 6), round(hi, 6), ''


def kategori(nama, per, m):
    F = set(m.get('flag', []))
    if nama == 'tmax': return 0
    if nama in K145_HENTI: return 1 if nama != 'had_henti' else 1.5
    keluar = per & {'stop', 'tgt', 'exitc'}
    if keluar and not (per & {'sig'}): return 1.2
    if keluar: return 2
    if 'sig' in per: return 3
    return 9


def berat(m):
    """Keutamaan dalam kategori: tetingkap indikator, ambang dan pengganda (2) mendahului lag/kiraan lain (1)."""
    F = set(m.get('flag', [])); r = m.get('peranan_kod', '')
    if 'banding' in F and 'arg' not in F: return 2
    if 'op:kali' in F or 'op:bahagi' in F: return 2
    if r.startswith('shift') or r.startswith('range') or r.startswith('nilai'): return 1
    return 2


def pilih_tala(cal):
    """cal: senarai (nama, kategori, berat, kali, urut). Pulangkan <= 6 nama."""
    cal = [c for c in cal if c[1] < 9]
    cal.sort(key=lambda c: (c[1], -c[2], -c[3], c[4]))
    keluar = [c for c in cal if c[1] < 2][:4]
    lain = [c for c in cal if c[1] >= 2]
    return [c[0] for c in (keluar + lain)[:6]]


def proses(mid, meta):
    f = os.path.join(SINI, mid + '.py')
    src = open(f).read()
    tree = ast.parse(src)
    PARAM = {}
    for s in tree.body:
        if isinstance(s, ast.Assign) and isinstance(s.targets[0], ast.Name) and s.targets[0].id == 'PARAM':
            PARAM = ast.literal_eval(s.value)
    md = meta.get(mid, {})
    per = peranan(tree) if PARAM else {}
    if 'tmax' in PARAM: per['tmax'] = {'tmax'}
    gel, sama = info_struktur(tree)
    def _hint(r):
        for o in OP_AKHIR:
            if r.endswith(o): return r[: -len(o)]
        return r
    tug = {md[n]['peranan_kod'] for n in md if 'tugasan' in md[n].get('flag', []) and isinstance(PARAM.get(n), int)}
    st = (gel, sama, (tug, {_hint(md[n]['peranan_kod']) for n in sama if n in md}))
    J, baris, cal = {}, [], []
    for n, v in PARAM.items():
        m = md.get(n, {'flag': [], 'peranan_kod': n, 'kali': 1, 'urut': 999})
        jenis, lo, hi, sebab = julat(n, v, m, per.get(n, set()), mid, st)
        if jenis != 'beku':
            if not (lo <= v <= hi): jenis, sebab = 'beku', 'asal di luar julat'
            else:
                J[n] = (jenis, lo, hi)
                cal.append((n, kategori(n, per.get(n, set()), m), berat(m), m.get('kali', 1), m.get('urut', 999)))
        baris.append([mid, n, v, jenis, '' if lo is None or jenis == 'beku' else lo, '' if hi is None or jenis == 'beku' else hi,
                      '', '|'.join(sorted(per.get(n, set()))), sebab])
    T = pilih_tala(cal)
    for b in baris: b[6] = 'Y' if b[1] in T else 'N'
    # suntik
    i = src.index(BLOK_JT)
    jt = BLOK_JT + '\n'
    jt += ('JULAT = {\n' + ''.join(f'    {k!r}: {v!r},\n' for k, v in J.items()) + '}\n') if J else 'JULAT = {}\n'
    jt += f'TALA = {T!r}\n'
    open(f, 'w').write(src[:i] + jt)
    return baris, T, J


def sahkan(ids, n_ticker):
    """Jalankan sedia() dengan semua TALA di sempadan bawah, kemudian atas."""
    sys.path.insert(0, SINI)
    import kesetaraan as K, importlib, time
    fr, idx = K.muat(n_ticker)
    gagal = []
    for mid in ids:
        B = K.import_fail('jt_' + mid, os.path.join(SINI, mid + '.py'))
        if not B.TALA: continue
        for sisi in (1, 2):
            P = {k: B.JULAT[k][sisi] for k in B.TALA}
            try:
                f = K.salin(fr); B.sedia(f, idx, P)
                for g in f.values():
                    for c in LAJUR: g[c]
            except Exception as e:
                gagal.append((mid, 'bawah' if sisi == 1 else 'atas', f'{type(e).__name__}: {e}'[:150]))
    return gagal


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kaedah', nargs='*'); ap.add_argument('--sahkan', type=int, default=0, help='bilangan ticker untuk uji sempadan')
    a = ap.parse_args()
    sys.path.insert(0, SINI)
    from ekstrak_param import senarai
    ids = senarai(a.kaedah)
    meta = json.load(open(META))
    lama = []
    if os.path.exists(CSV) and a.kaedah and a.kaedah != ['semua']:
        lama = [r for r in csv.reader(open(CSV))][1:]
        lama = [r for r in lama if r[0] not in ids]
    semua, nt, npar = [], [], []
    for mid in ids:
        b, T, J = proses(mid, meta)
        semua += b; nt.append(len(T)); npar.append(len(b))
    semua = lama + semua
    semua.sort(key=lambda r: (int(r[0][1:]), r[1]))
    with open(CSV, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['kaedah', 'nama', 'nilai_asal', 'jenis', 'bawah', 'atas', 'tala', 'peranan', 'catatan'])
        w.writerows(semua)
    srt = lambda x: sorted(x)[len(x) // 2] if x else 0
    print(f'{len(ids)} modul; param median {srt(npar)} maks {max(npar)}; TALA median {srt(nt)} maks {max(nt)}; '
          f'TALA kosong: {sum(1 for x in nt if x == 0)}')
    if a.sahkan:
        g = sahkan(ids, a.sahkan)
        for x in g: print('GAGAL', *x)
        print('sahkan sempadan:', len(ids), 'modul,', len(g), 'gagal')


if __name__ == '__main__':
    main()
