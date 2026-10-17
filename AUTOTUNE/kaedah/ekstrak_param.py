# Penukar AST: modul asal BacktestShariah2/kod/kaedah/Mxx.py -> salinan berparameter AUTOTUNE/kaedah/Mxx.py.
# Literal nombor (int/float; kecuali bool, 0, 1, -1) dalam sedia() dan fungsi pembantu yang dicapainya
# diganti dengan P['<nama>']; PARAM = nilai asal. Pemalar modul bernombor yang dibaca fungsi turut diparameter.
# Nilai lalai pembantu (cth. atr(g) n=14) ditulis jelas di tapak panggilan supaya boleh ditala.
# Guna: python3 AUTOTUNE/kaedah/ekstrak_param.py [Mxx ...|semua]
# Output: AUTOTUNE/kaedah/Mxx.py, AUTOTUNE/kaedah/param_meta.json (konteks literal untuk pilih_julat.py).
import ast, copy, glob, inspect, json, os, re, sys

AKAR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ASAL = os.path.join(AKAR, 'BacktestShariah2', 'kod', 'kaedah')
SINI = os.path.join(AKAR, 'AUTOTUNE', 'kaedah')
META = os.path.join(SINI, 'param_meta.json')
STD = ('ID', 'NAMA', 'VARIAN', 'TMAX', 'WARM', 'ADA_HENTI', 'SILANG', 'PERLU_BAR')
LAJUR = ('sig', 'stop', 'tgt', 'exitc', 'rank')
KALENDAR = {'month', 'day', 'dayofweek', 'weekday', 'quarter', 'year', 'dayofyear', 'week', 'hour', 'minute',
            'days_in_month', 'is_month_end', 'weekofyear'}
LALU = {'mean', 'sum', 'max', 'min', 'std', 'abs', 'shift', 'rolling', 'ewm', 'fillna', 'astype', 'values', 'median',
        'to_numpy', 'diff', 'pct_change', 'var', 'cummax', 'cummin', 'ffill', 'bfill', 'reindex', 'where', 'clip'}
OPN = {ast.Mult: 'kali', ast.Div: 'bahagi', ast.Add: 'tambah', ast.Sub: 'tolak', ast.Pow: 'kuasa', ast.Mod: 'mod',
       ast.FloorDiv: 'bahagi_bulat'}
KEPALA = ('# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/{id}.py\n'
          '# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.\n'
          'import os as _os, sys as _sys\n'
          '_D = _os.path.dirname(_os.path.abspath(__file__))\n'
          "for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):\n"
          '    if _p not in _sys.path: _sys.path.insert(0, _p)\n')
BLOK_JT = '# --- JULAT/TALA (pilih_julat.py) ---'


def _k145_info():
    if SINI not in sys.path: sys.path.insert(0, SINI)
    import _k145 as K
    sig, kunci = {}, dict(K.KUNCI_K145)
    for n, f in vars(K).items():
        if callable(f) and not n.startswith('_') and not isinstance(f, type):
            try: sig[n] = inspect.signature(f)
            except (TypeError, ValueError): pass
    return K, sig, kunci


def nombor(n):
    return isinstance(n, ast.Constant) and type(n.value) in (int, float)


def dikecuali(v):
    return v in (0, 1)


def nilai_str(v):
    s = repr(v).replace('-', 'm').replace('.', '_').replace('+', '')
    return re.sub(r'[^0-9a-z_]', '_', s.lower())


def bersih(s):
    s = re.sub(r'[^0-9a-zA-Z_]', '_', s).strip('_').lower()
    return re.sub(r'_+', '_', s)[:28].strip('_')


def nama_panggil(f):
    if isinstance(f, ast.Name): return f.id
    if isinstance(f, ast.Attribute): return f.attr
    return ''


def petunjuk(e):
    """Nama pendek bermakna bagi ungkapan (untuk menamakan literal)."""
    if e is None: return ''
    if isinstance(e, ast.Name): return e.id
    if isinstance(e, ast.Attribute):
        if e.attr in LALU: return petunjuk(e.value)
        return e.attr
    if isinstance(e, ast.Call):
        n = nama_panggil(e.func)
        if isinstance(e.func, ast.Attribute) and n in LALU:
            return petunjuk(e.func.value) or (petunjuk(e.args[0]) if e.args else '')
        if n in ('float', 'abs', 'Series', 'asarray', 'array', 'maximum', 'minimum') and e.args:
            return petunjuk(e.args[0]) or n
        return n
    if isinstance(e, ast.Subscript):
        if isinstance(e.slice, ast.Constant) and isinstance(e.slice.value, str): return e.slice.value
        return petunjuk(e.value)
    if isinstance(e, ast.BinOp): return petunjuk(e.left) or petunjuk(e.right)
    if isinstance(e, ast.UnaryOp): return petunjuk(e.operand)
    return ''


class Modul:
    def __init__(self, mid, K, ksig, kkunci):
        self.id = mid
        self.src = open(os.path.join(ASAL, mid + '.py')).read()
        self.tree = ast.parse(self.src)
        self.K, self.ksig, self.kkunci = K, ksig, kkunci
        self.param = {}          # nama -> nilai
        self.meta = {}           # nama -> konteks
        self.kunci = {}          # (peranan, repr, jenis) -> nama
        self.amaran = []

    # ---------- pra-proses ----------
    def tukar_nama_P(self):
        """Nama P sedia ada dalam modul asal ditukar kepada P_ (P dikhaskan untuk parameter)."""
        for n in ast.walk(self.tree):
            if isinstance(n, ast.Name) and n.id == 'P': n.id = 'P_'
            elif isinstance(n, ast.arg) and n.arg == 'P': n.arg = 'P_'
            elif isinstance(n, ast.keyword) and n.arg == 'P': n.arg = 'P_'

    def kumpul(self):
        t = self.tree
        self.fungsi, self.lambda_ = {}, {}
        self.pemalar = {}        # nama -> nilai (pemalar nombor modul)
        self.uses_k145 = any(isinstance(s, ast.Try) for s in t.body)
        for s in t.body:
            if isinstance(s, ast.FunctionDef): self.fungsi[s.name] = s
            elif isinstance(s, ast.Assign) and len(s.targets) == 1:
                tg, v = s.targets[0], s.value
                if isinstance(tg, ast.Name) and isinstance(v, ast.Lambda): self.lambda_[tg.id] = s
                elif isinstance(tg, ast.Name) and nombor(v) and tg.id not in STD: self.pemalar[tg.id] = v.value
                elif isinstance(tg, ast.Name) and isinstance(v, ast.UnaryOp) and isinstance(v.op, ast.USub) \
                        and nombor(v.operand) and tg.id not in STD: self.pemalar[tg.id] = -v.operand.value
                elif isinstance(tg, ast.Tuple) and isinstance(v, ast.Tuple) and len(tg.elts) == len(v.elts):
                    for a, b in zip(tg.elts, v.elts):
                        if isinstance(a, ast.Name) and nombor(b): self.pemalar[a.id] = b.value
        # pemalar yang dirujuk di peringkat modul (di luar fungsi) dibekukan: pautan dengan ungkapan modul kekal
        for s in t.body:
            if isinstance(s, (ast.FunctionDef,)): continue
            if isinstance(s, ast.Assign) and isinstance(s.value, ast.Lambda): continue
            for n in ast.walk(s):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in self.pemalar:
                    self.pemalar.pop(n.id)
        # capaian dari sedia
        semua = set(self.fungsi) | set(self.lambda_)
        cap, baru = set(), ['sedia']
        while baru:
            f = baru.pop()
            if f in cap: continue
            cap.add(f)
            nod = self.fungsi.get(f) or self.lambda_.get(f)
            for n in ast.walk(nod):
                if isinstance(n, ast.Name) and n.id in semua and n.id not in cap: baru.append(n.id)
        self.capai = cap
        self.k145_guna = set()
        if self.uses_k145:
            for f in cap:
                nod = self.fungsi.get(f) or self.lambda_.get(f)
                for n in ast.walk(nod):
                    if isinstance(n, ast.Name) and n.id in self.ksig and n.id not in semua: self.k145_guna.add(n.id)
        # tandatangan untuk mengisi nilai lalai di tapak panggilan
        self.tt = {}
        if self.uses_k145:
            for n, sg in self.ksig.items():
                self.tt[n] = [(p.name, p.default, p.kind) for p in sg.parameters.values()]
        else:
            import enjin
            for n in ('rsi', 'atr'):
                self.tt[n] = [(p.name, p.default, p.kind) for p in inspect.signature(getattr(enjin, n)).parameters.values()]
        for n, f in self.fungsi.items():
            a = f.args; pos = a.posonlyargs + a.args
            df = [None] * (len(pos) - len(a.defaults)) + list(a.defaults)
            self.tt[n] = [(x.arg, d, inspect.Parameter.POSITIONAL_OR_KEYWORD) for x, d in zip(pos, df)]
            for x, d in zip(a.kwonlyargs, a.kw_defaults):
                self.tt[n].append((x.arg, d, inspect.Parameter.KEYWORD_ONLY))

    # ---------- penamaan ----------
    def nama(self, peranan, v, ctx):
        peranan = bersih(peranan) or 'nilai'
        k = (peranan, repr(v), type(v).__name__)
        if k not in self.kunci:
            n = f'{peranan}_{nilai_str(v)}'
            while n in self.param and self.param[n] != v: n += '_'
            self.kunci[k] = n
            self.param[n] = v
            self.meta[n] = {'nilai': v, 'peranan_kod': peranan, 'flag': set(), 'kali': 0, 'urut': len(self.meta)}
        n = self.kunci[k]
        self.meta[n]['flag'] |= ctx
        self.meta[n]['kali'] += 1
        return n

    def peranan_literal(self, node, par):
        """Pulangkan (peranan, flag) berdasarkan konteks induk."""
        flag = set()
        cur = node
        p = par.get(cur)
        elt_i = -1
        while isinstance(p, (ast.Tuple, ast.List, ast.IfExp, ast.BoolOp, ast.Starred)) or \
                (isinstance(p, ast.UnaryOp) and isinstance(p.op, (ast.USub, ast.UAdd))):
            if isinstance(p, (ast.Tuple, ast.List)) and elt_i < 0 and cur in p.elts: elt_i = p.elts.index(cur)
            cur, p = p, par.get(p)
        # dalam subskrip/hirisan -> indeks
        q, c2 = p, cur
        while q is not None and not isinstance(q, ast.stmt):
            if isinstance(q, ast.Slice): flag.add('indeks')
            if isinstance(q, ast.Subscript) and c2 is q.slice: flag.add('indeks')
            c2, q = q, par.get(q)
        if isinstance(p, ast.Call):
            fn = nama_panggil(p.func); i = p.args.index(cur) if cur in p.args else -1
            flag.add('arg'); flag.add('fn:' + fn)
            if fn in self.tt and 0 <= i < len(self.tt[fn]):
                an = self.tt[fn][i][0]
                return (fn if an in ('n', 'window') else f'{fn}_{an}'), flag
            return (fn if i <= 0 else f'{fn}_a{i}'), flag
        if isinstance(p, ast.keyword):
            call = par.get(p); fn = nama_panggil(call.func) if isinstance(call, ast.Call) else ''
            flag.add('arg'); flag.add('fn:' + fn); flag.add('kw:' + (p.arg or ''))
            return (fn if p.arg in ('n', 'window') else f'{fn}_{p.arg}'), flag
        if isinstance(p, ast.BinOp):
            lain = p.right if cur is p.left else p.left
            op = OPN.get(type(p.op), 'op'); flag.add('op:' + op)
            if cur is p.right: flag.add('kanan')
            if op == 'bahagi' and cur is p.right and isinstance(p.left, ast.BinOp) and isinstance(p.left.op, ast.Add):
                flag.add('purata')
            # dalam argumen fungsi tetingkap?
            q = par.get(p)
            while isinstance(q, (ast.BinOp, ast.UnaryOp)): q = par.get(q)
            if isinstance(q, (ast.Call, ast.keyword)): flag.add('dalam_arg')
            if isinstance(q, ast.Subscript) or isinstance(q, ast.Slice): flag.add('indeks')
            h = petunjuk(lain)
            if h in KALENDAR: flag.add('kalendar')
            return (f'{h}_{op}' if h else op), flag
        if isinstance(p, ast.Compare):
            flag.add('banding')
            lain = p.left if cur is not p.left else (p.comparators[0] if p.comparators else None)
            # pautan: x.rolling(N).sum() == N
            for n in ast.walk(lain) if lain is not None else []:
                if isinstance(n, ast.Call) and nama_panggil(n.func) == 'rolling' and n.args and nombor(n.args[0]) \
                        and n.args[0].value == node.value:
                    flag.add('arg'); flag.add('fn:rolling')
                    return 'rolling', flag
            h = petunjuk(lain)
            if h in KALENDAR or (isinstance(lain, ast.Attribute) and lain.attr in KALENDAR): flag.add('kalendar')
            return (f'{h}_ambang' if h else 'ambang'), flag
        if isinstance(p, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            tg = p.targets[0] if isinstance(p, ast.Assign) else p.target
            if isinstance(tg, ast.Tuple) and 0 <= elt_i < len(tg.elts): tg = tg.elts[elt_i]
            flag.add('tugasan')
            return petunjuk(tg) or 'nilai', flag
        if isinstance(p, ast.Dict):
            i = p.values.index(cur) if cur in p.values else -1
            k = p.keys[i] if i >= 0 else None
            return (k.value if isinstance(k, ast.Constant) and isinstance(k.value, str) else 'nilai'), flag
        if isinstance(p, ast.Return): return 'pulang', flag
        return 'nilai', flag

    # ---------- penukaran ----------
    def tukar_fungsi(self, nod, nama_f):
        par = {}
        for a in ast.walk(nod):
            for b in ast.iter_child_nodes(a): par[b] = a
        badan = nod.body if isinstance(nod, ast.FunctionDef) else None
        helpers = (set(self.fungsi) | set(self.lambda_)) & self.capai
        # 1. isi nilai lalai di tapak panggilan + P=P
        for c in [n for n in ast.walk(nod) if isinstance(n, ast.Call)]:
            fn = c.func.id if isinstance(c.func, ast.Name) else None
            if fn is None or fn not in self.tt: continue
            if any(isinstance(a, ast.Starred) for a in c.args) or any(k.arg is None for k in c.keywords): continue
            ada = {k.arg for k in c.keywords}
            for i, (an, d, kind) in enumerate(self.tt[fn]):
                if an == 'P' or i < len(c.args) or an in ada: continue
                if kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY): continue
                if isinstance(d, ast.AST):
                    if nombor(d) and not dikecuali(d.value) and not isinstance(d.value, bool):
                        c.keywords.append(ast.keyword(an, ast.Constant(d.value)))
                    elif isinstance(d, ast.Name) and d.id in self.pemalar:
                        c.keywords.append(ast.keyword(an, ast.Name(d.id, ast.Load())))
                elif type(d) in (int, float) and not dikecuali(d):
                    c.keywords.append(ast.keyword(an, ast.Constant(d)))
            if fn in helpers or (fn in self.k145_guna and fn in ('siap_lajur', 'naik_aliran', 'pasang', 'lajur_stop', 'lajur_exit')):
                c.keywords.append(ast.keyword('P', ast.Name('P', ast.Load())))
        # rujukan pembantu tanpa panggilan -> partial(f, P=P)
        par = {}
        for a in ast.walk(nod):
            for b in ast.iter_child_nodes(a): par[b] = a
        for n in [n for n in ast.walk(nod) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in helpers]:
            p = par.get(n)
            if isinstance(p, ast.Call) and p.func is n: continue
            if isinstance(p, ast.Attribute): continue          # atribut fungsi (cth. f.ep) kekal
            if isinstance(nod, ast.FunctionDef) and n.id == nod.name: continue
            self.ganti(par, n, ast.Call(ast.Name('_partial', ast.Load()), [ast.Name(n.id, ast.Load())],
                                        [ast.keyword('P', ast.Name('P', ast.Load()))]))
            self.perlu_partial = True
        par = {}
        for a in ast.walk(nod):
            for b in ast.iter_child_nodes(a): par[b] = a
        # langkau literal dalam nilai lalai argumen fungsi peringkat modul (diisi di tapak panggilan)
        lalai = set()
        if isinstance(nod, ast.FunctionDef):
            for d in nod.args.defaults + [d for d in nod.args.kw_defaults if d is not None]:
                for x in ast.walk(d): lalai.add(x)
        elif isinstance(nod, ast.Lambda):
            for d in nod.args.defaults + [d for d in nod.args.kw_defaults if d is not None]:
                for x in ast.walk(d): lalai.add(x)
        # 2. pemalar modul
        for n in [n for n in ast.walk(nod) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in self.pemalar
                  and n not in lalai]:
            v = self.pemalar[n.id]
            nm = bersih(n.id)
            if nm in self.param and self.param[nm] != v: nm = nm + '_m'
            if nm not in self.param:
                self.param[nm] = v
                self.meta[nm] = {'nilai': v, 'peranan_kod': nm, 'flag': {'pemalar_modul'}, 'kali': 0, 'urut': len(self.meta)}
            r, fl = self.peranan_literal(n, par) if False else ('', set())
            self.meta[nm]['kali'] += 1
            self.ganti(par, n, self.rujuk(nm, n, par, nod))
        # 3. literal
        lit = []
        for n in ast.walk(nod):
            if nombor(n) and not isinstance(n.value, bool) and not dikecuali(n.value):
                lit.append(n)
        for n in lit:
            if n in lalai: continue
            r, fl = self.peranan_literal(n, par)
            if self.dalam_gelung(n, par, nod): fl.add('gelung')
            nm = self.nama(r, n.value, fl)
            self.ganti(par, n, self.rujuk(nm, n, par, nod))
        return nod

    def dalam_gelung(self, n, par, akar):
        p = par.get(n)
        while p is not None and p is not akar:
            if isinstance(p, (ast.For, ast.While, ast.comprehension, ast.ListComp, ast.GeneratorExp, ast.DictComp,
                              ast.SetComp, ast.Lambda)): return True
            if isinstance(p, ast.FunctionDef): return False
            p = par.get(p)
        return False

    def rujuk(self, nm, n, par, akar):
        """P['nm'], atau nama tempatan _p_nm (diangkat ke atas fungsi) jika dalam gelung/lambda."""
        # cari FunctionDef terdekat
        p, f = par.get(n), None
        gel = False
        while p is not None:
            if isinstance(p, (ast.For, ast.While, ast.comprehension, ast.Lambda)): gel = True
            if isinstance(p, ast.FunctionDef): f = p; break
            p = par.get(p)
        if f is None and isinstance(akar, ast.FunctionDef): f = akar
        if gel and f is not None:
            self.angkat.setdefault(id(f), (f, {}))[1][nm] = True
            return ast.Name('_p_' + nm, ast.Load())
        return ast.Subscript(ast.Name('P', ast.Load()), ast.Constant(nm), ast.Load())

    @staticmethod
    def ganti(par, lama, baru):
        p = par[lama]
        for medan, nilai in ast.iter_fields(p):
            if nilai is lama: setattr(p, medan, baru); par[baru] = p; return
            if isinstance(nilai, list):
                for i, x in enumerate(nilai):
                    if x is lama: nilai[i] = baru; par[baru] = p; return
        raise RuntimeError('ganti gagal')

    def jana(self):
        self.tukar_nama_P()
        self.kumpul()
        self.angkat = {}
        self.perlu_partial = False
        t = self.tree
        if 'sedia' not in self.fungsi: raise RuntimeError('tiada sedia')
        # k145: kunci fungsi berparameter + kod henti/keluar
        kod = {}
        for s in t.body:
            if isinstance(s, ast.Assign) and isinstance(s.targets[0], ast.Name) and s.targets[0].id in ('HENTI_KOD', 'KELUAR_KOD'):
                kod[s.targets[0].id] = s.value.value
        for f in sorted(self.capai):
            nod = self.fungsi.get(f)
            if nod is not None: self.tukar_fungsi(nod, f)
            else: self.tukar_fungsi(self.lambda_[f].value, f)
        if self.uses_k145:
            for fn in sorted(self.k145_guna):
                for k, v in self.kkunci.get(fn, {}).items():
                    self.param[k] = v
                    self.meta[k] = {'nilai': v, 'peranan_kod': k, 'flag': {'k145', 'fn:' + fn}, 'kali': 1, 'urut': len(self.meta)}
            if 'pasang' in self.k145_guna and kod:
                for k, v in self.K.kunci_kod(kod.get('HENTI_KOD', 'ASAL'), kod.get('KELUAR_KOD', 'ASAL')).items():
                    self.param[k] = v
                    self.meta[k] = {'nilai': v, 'peranan_kod': k, 'flag': {'k145', 'fn:pasang'}, 'kali': 1, 'urut': len(self.meta)}
        # TMAX
        for s in t.body:
            if isinstance(s, ast.Assign) and isinstance(s.targets[0], ast.Name) and s.targets[0].id == 'TMAX' \
                    and nombor(s.value) and isinstance(s.value.value, int):
                self.param['tmax'] = s.value.value
                self.meta['tmax'] = {'nilai': s.value.value, 'peranan_kod': 'tmax', 'flag': {'tmax'}, 'kali': 1, 'urut': -1}
        # angkat nama tempatan dalam gelung
        for f, nm in self.angkat.values():
            st = [ast.parse(f"_p_{k} = P['{k}']").body[0] for k in nm]
            i = 1 if (f.body and isinstance(f.body[0], ast.Expr) and isinstance(getattr(f.body[0], 'value', None), ast.Constant)
                      and isinstance(f.body[0].value.value, str)) else 0
            if f.name == 'sedia': i += 0   # gabungan P dimasukkan kemudian di kedudukan 0 / selepas docstring
            f.body[i:i] = st
        # tandatangan: P
        for fname in self.capai:
            if fname == 'sedia': continue
            nod = self.fungsi.get(fname)
            a = nod.args if nod is not None else self.lambda_[fname].value.args
            if any(x.arg == 'P' for x in a.args + a.kwonlyargs): continue
            a.kwonlyargs.append(ast.arg('P')); a.kw_defaults.append(ast.Name('PARAM', ast.Load()))
        sd = self.fungsi['sedia']
        sd.args.args.append(ast.arg('P')); sd.args.defaults.append(ast.Constant(None))
        gab = ast.parse('P = {**PARAM, **(P or {})}').body[0]
        i = 1 if (sd.body and isinstance(sd.body[0], ast.Expr) and isinstance(sd.body[0].value, ast.Constant)) else 0
        sd.body.insert(i, gab)
        # buang hampir
        t.body = [s for s in t.body if not (isinstance(s, ast.FunctionDef) and s.name == 'hampir')]
        # import k145: guna salinan AUTOTUNE
        badan = []
        for s in t.body:
            if isinstance(s, ast.Try) and 'k145' in ast.unparse(s): badan.append(ast.parse('from _k145 import *').body[0])
            else: badan.append(s)
        t.body = badan
        # PARAM selepas import
        i = 0
        while i < len(t.body) and isinstance(t.body[i], (ast.Import, ast.ImportFrom)): i += 1
        pr = ast.parse('PARAM = {}').body[0]
        pr.value = ast.Dict([ast.Constant(k) for k in self.param], [ast.Constant(v) for v in self.param.values()])
        t.body.insert(i, pr)
        if self.perlu_partial: t.body.insert(0, ast.parse('from functools import partial as _partial').body[0])
        ast.fix_missing_locations(t)
        kod_py = ast.unparse(t)
        # format PARAM satu kunci sebaris
        if self.param:
            baris = ',\n'.join(f'    {k!r}: {v!r}' for k, v in self.param.items())
            kod_py = kod_py.replace(ast.unparse(pr), 'PARAM = {\n' + baris + ',\n}', 1)
        else:
            kod_py = kod_py.replace(ast.unparse(pr), 'PARAM = {}', 1)
        kod_py = (KEPALA.format(id=self.id) + kod_py + '\nBELUM_DITALA = False\n\n' + BLOK_JT +
                  '\nJULAT = {}\nTALA = []\n')
        return kod_py


def pembalut(mid):
    """Salinan pembalut (BELUM DITALA): panggil modul asal tanpa perubahan."""
    return (KEPALA.format(id=mid) +
            'import importlib.util as _iu\n'
            f"_f = _os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod', 'kaedah', '{mid}.py'))\n"
            f"_s = _iu.spec_from_file_location('_asal_{mid}', _f); _asal = _iu.module_from_spec(_s); _s.loader.exec_module(_asal)\n"
            'ID, NAMA, VARIAN, TMAX, WARM = _asal.ID, _asal.NAMA, _asal.VARIAN, _asal.TMAX, _asal.WARM\n'
            'ADA_HENTI, SILANG, PERLU_BAR = _asal.ADA_HENTI, _asal.SILANG, _asal.PERLU_BAR\n'
            'PARAM = {}\nBELUM_DITALA = True\n\n\n'
            'def sedia(fr, idx, P=None):\n'
            '    """Modul asal tanpa parameter (gagal kesetaraan); P diabaikan."""\n'
            '    return _asal.sedia(fr, idx)\n\n' + BLOK_JT + '\nJULAT = {}\nTALA = []\n')


def senarai(args):
    if not args or args == ['semua']:
        return sorted((os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ASAL, 'M*.py'))), key=lambda s: int(s[1:]))
    return args


def main(args):
    sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'kod'))
    K, ksig, kkunci = _k145_info()
    meta = json.load(open(META)) if os.path.exists(META) else {}
    balut = set(json.load(open(os.path.join(SINI, 'balut.json')))) if os.path.exists(os.path.join(SINI, 'balut.json')) else set()
    ok = gagal = 0
    for mid in senarai(args):
        try:
            if mid in balut: raise RuntimeError('disenarai dalam balut.json')
            m = Modul(mid, K, ksig, kkunci)
            kod = m.jana()
            compile(kod, mid, 'exec')
            meta[mid] = {n: {**d, 'flag': sorted(d['flag'])} for n, d in m.meta.items()}
            ok += 1
        except Exception as e:
            kod = pembalut(mid); meta[mid] = {}; gagal += 1
            print(f'{mid}: pembalut ({type(e).__name__}: {e})')
        open(os.path.join(SINI, mid + '.py'), 'w').write(kod)
    json.dump(meta, open(META, 'w'), indent=0, sort_keys=True)
    print(f'siap: {ok} berparameter, {gagal} pembalut')


if __name__ == '__main__':
    main(sys.argv[1:])
