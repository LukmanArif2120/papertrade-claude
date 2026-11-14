"""Carian setup — keluarga pencetus BERPARAMETER K01-K25 (SPEC pindaan 14 Nov 2026 (n), bahagian (a)).

Setiap keluarga ialah satu syarat indikator dengan grid parameter penuh; ahli yang parameternya sama dengan takrif `P`
(cs_atom) atau `N` (_nxx) asal ditanda `asal`. Takrif memakai fungsi bantu cs_atom supaya ahli `asal` menghasilkan isyarat
yang sama dengan pencetus `P` asal (diuji). Tiada pandang hadapan: setiap syarat hanya memakai bar hari itu dan sebelumnya."""
import numpy as np
import pandas as pd

import cs_atom as atom

_w, _silang, _dulu = atom._wilder, atom._silang, atom._dulu


def _rsi_x(n):
    return (3, 5, 8, 10, 15, 20, 25, 30) if n <= 5 else (15, 20, 25, 30, 35) if n <= 10 else (25, 30, 35, 40, 45)


def grid():
    """Senarai (nama, keluarga, parameter) dalam susunan tetap; nama = K<ff>.<nnn>."""
    G = []
    add = lambda fam, **p: G.append((fam, p))
    for n in (2, 3, 4, 5, 7, 10, 14):
        for x in _rsi_x(n):
            for tren in (0, 1):
                add('K01', n=n, x=x, tren=tren)
    for n in (5, 7, 10, 14, 21):
        for x in (20, 25, 30, 35, 40, 50, 60):
            add('K02', n=n, x=x)
    for n in (10, 15, 20, 30, 50):
        for k in (1.5, 2.0, 2.5, 3.0):
            for r in (0, 30, 40):
                add('K03', n=n, k=k, r=r)
    for n in (10, 20, 30):
        for k in (1.5, 2.0, 2.5):
            add('K04', n=n, k=k)
    for n in (10, 20, 30, 50):
        for k in (1.5, 2.0, 2.5, 3.0):
            add('K05', n=n, k=k)
    for k in (2, 3, 4, 5, 6, 7):
        for tren in (0, 1):
            add('K06', k=k, tren=tren)
    for n in (5, 8, 10, 15, 20, 30, 50, 100, 150, 200):
        for j in ('sma', 'ema'):
            add('K07', n=n, j=j)
    for f, s in ((3, 10), (5, 10), (5, 20), (8, 21), (10, 20), (10, 30), (10, 50), (20, 50), (20, 100), (50, 100),
                 (50, 150), (50, 200), (100, 200)):
        for j in ('sma', 'ema'):
            add('K08', f=f, s=s, j=j)
    for f, s, g in ((12, 26, 9), (8, 17, 9), (5, 35, 5), (6, 19, 6), (10, 20, 7), (19, 39, 9), (3, 10, 16), (24, 52, 18)):
        for z in (0, -1, 1):
            add('K09', f=f, s=s, g=g, z=z)
    for n in (5, 10, 20, 30, 40, 55, 90, 126, 189, 252):
        for v in (0, 1.5, 2.0, 3.0):
            add('K10', n=n, v=v)
    for n in (7, 10, 14, 20):
        for m in (1.5, 2.0, 2.5, 3.0, 4.0):
            add('K11', n=n, m=m)
    for n in (7, 10, 14, 20):
        for x in (15, 20, 25, 30, 35):
            add('K12', n=n, x=x)
    for n in (5, 9, 14, 21):
        for x in (10, 20, 30, 40):
            add('K13', n=n, x=x)
    for r in (0.0, 0.02, 0.03, 0.04, 0.05, 0.07, 0.10):
        for v in (1.5, 2.0, 3.0):
            for p in (0.0, 0.75):
                add('K14', r=r, v=v, p=p)
    for g in (0.02, 0.03, 0.05, 0.08, 0.10, 0.15):
        for v in (0, 1.5, 2.0, 3.0):
            add('K15', g=g, v=v)
    for g in (0.0, 0.01, 0.02, 0.03, 0.05):
        for v in (0, 1.5, 2.0, 3.0):
            add('K16', g=g, v=v)
    for n in (10, 20, 50, 100):
        for tol in (0.0, 0.01, 0.02):
            for j in ('sma', 'ema'):
                for tren in (0, 1):
                    add('K17', n=n, tol=tol, j=j, tren=tren)
    for x in (2, 3, 5, 10, 20):
        for y in (0.05, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30):
            add('K18', x=x, y=y)
    for n in (10, 20, 30):
        for k in (1.0, 1.5, 2.0, 2.5, 3.0):
            add('K19', n=n, k=k)
    for kb in (1.5, 2.0, 2.5):
        for kk in (1.0, 1.5, 2.0):
            add('K20', kb=kb, kk=kk)
    for k in (4, 5, 7, 10, 14):
        for d in (0, 1):
            add('K21', k=k, d=d)
    for x in (20, 25, 30, 35, 40):
        for n in (10, 20, 30):
            add('K22', x=x, n=n)
    for x in (70, 80, 85, 90, 95):
        add('K23', x=x)
    for a in (0.1, 0.2, 0.3):
        for b in (0.7, 0.8, 0.9):
            add('K24', a=a, b=b)
    for n in (10, 20, 40, 60):
        for w in (0.08, 0.12, 0.20, 0.35):
            for v in (0, 1.5):
                add('K25', n=n, w=w, v=v)
    bil, out = {}, []
    for fam, p in G:
        bil[fam] = bil.get(fam, 0) + 1
        out.append((f'{fam}.{bil[fam]:03d}', fam, p))
    return out


NAMA = {
    'K01': 'RSI({n}) < {x}', 'K02': 'RSI({n}) silang atas {x}', 'K03': 'tutup < jalur bawah BB({n}, {k})',
    'K04': 'masuk semula atas jalur bawah BB({n}, {k})', 'K05': 'tutup silang atas jalur atas BB({n}, {k})',
    'K06': '{k} tutup menurun berturut', 'K07': 'tutup silang atas {j}{n}', 'K08': '{j}{f} silang atas {j}{s}',
    'K09': 'MACD({f},{s},{g}) silang naik', 'K10': 'pecah tinggi {n} hari', 'K11': 'Supertrend({n}, {m}) bertukar naik',
    'K12': 'ADX({n}) silang atas {x} & +DI > -DI', 'K13': 'Stochastic({n}) silang naik dari bawah {x}',
    'K14': 'lonjakan >= {r:.1%} + volum {v}x', 'K15': 'gap >= {g:.1%}', 'K16': 'gap-and-go (buka > tinggi semalam + {g:.1%})',
    'K17': 'undur ke {j}{n} yang naik (tol {tol:.1%})', 'K18': 'jatuh >= {y:.0%} dalam {x} hari',
    'K19': 'pecah atas Keltner({n}, {k})', 'K20': 'squeeze lepas ke atas (BB {kb}, KC {kk})', 'K21': 'NR{k}',
    'K22': 'Holy Grail (ADX > {x}, undur EMA{n})', 'K23': 'RS silang atas {x}',
    'K24': 'bar pembalikan (buka <= {a:.0%}, tutup >= {b:.0%} julat)', 'K25': 'pecah julat sempit {n} hari (<= {w:.0%})',
}
# ahli yang sama dengan takrif asal (P = cs_atom, tepat; N = _nxx, setara)
ASAL = [
    ('K01', dict(n=2, x=10, tren=0), 'N16'), ('K01', dict(n=2, x=10, tren=1), 'P15'), ('K01', dict(n=2, x=5, tren=1), 'P16'),
    ('K01', dict(n=14, x=40, tren=0), 'N75'), ('K02', dict(n=14, x=30), 'P14'), ('K02', dict(n=14, x=50), 'P12'),
    ('K02', dict(n=14, x=60), 'P13'), ('K03', dict(n=20, k=2.0, r=0), 'N73'), ('K03', dict(n=20, k=2.0, r=30), 'P19'),
    ('K05', dict(n=20, k=2.0), 'P18'), ('K06', dict(k=3, tren=0), 'N119'), ('K07', dict(n=20, j='sma'), 'P09'),
    ('K07', dict(n=50, j='sma'), 'P10'), ('K07', dict(n=200, j='sma'), 'P11'), ('K08', dict(f=5, s=20, j='sma'), 'P04'),
    ('K08', dict(f=10, s=20, j='sma'), 'P05'), ('K08', dict(f=10, s=50, j='sma'), 'P06'),
    ('K08', dict(f=20, s=50, j='sma'), 'P07'), ('K08', dict(f=50, s=200, j='sma'), 'P08'),
    ('K09', dict(f=12, s=26, g=9, z=0), 'P01'), ('K09', dict(f=12, s=26, g=9, z=-1), 'P02'),
    ('K09', dict(f=12, s=26, g=9, z=1), 'P03'), ('K10', dict(n=20, v=0), 'P25'), ('K10', dict(n=55, v=0), 'P26'),
    ('K10', dict(n=126, v=0), 'P27'), ('K10', dict(n=252, v=0), 'P28'), ('K10', dict(n=126, v=1.5), 'P35'),
    ('K11', dict(n=10, m=3.0), 'P21'), ('K12', dict(n=14, x=25), 'P22'), ('K13', dict(n=14, x=20), 'P24'),
    ('K14', dict(r=0.04, v=2.0, p=0.75), 'P32'), ('K15', dict(g=0.08, v=3.0), 'P31'), ('K16', dict(g=0.02, v=1.5), 'P30'),
    ('K17', dict(n=50, tol=0.01, j='sma', tren=1), 'P47'), ('K19', dict(n=20, k=2.0), 'P17'),
    ('K20', dict(kb=2.0, kk=1.5), 'P20'), ('K21', dict(k=7, d=1), 'N49'), ('K22', dict(x=30, n=20), 'P29'),
    ('K23', dict(x=90), 'P44'), ('K24', dict(a=0.2, b=0.8), 'N113'), ('K25', dict(n=60, w=0.35, v=1.5), 'P34'),
]


KELUARGA = tuple(f'K{i:02d}' for i in range(1, 26))


def rawak(fam, rng):
    """Satu set parameter rawak bagi keluarga (julat berterusan, termasuk nilai di luar grid) — untuk mesin berkala."""
    ri = lambda a, b: int(rng.integers(a, b + 1))
    ru = lambda a, b, d=2: round(float(rng.uniform(a, b)), d)
    pl = lambda *x: x[int(rng.integers(0, len(x)))]
    if fam == 'K01':
        n = ri(2, 21)
        return dict(n=n, x=ri(3, 30) if n <= 5 else ri(12, 45), tren=pl(0, 1))
    if fam == 'K02':
        return dict(n=ri(3, 30), x=ri(15, 65))
    if fam == 'K03':
        return dict(n=ri(8, 60), k=ru(1.0, 3.5), r=pl(0, 0, 25, 30, 35, 40))
    if fam == 'K04':
        return dict(n=ri(8, 40), k=ru(1.0, 3.0))
    if fam == 'K05':
        return dict(n=ri(8, 60), k=ru(1.0, 3.5))
    if fam == 'K06':
        return dict(k=ri(2, 8), tren=pl(0, 1))
    if fam == 'K07':
        return dict(n=ri(3, 250), j=pl('sma', 'ema'))
    if fam == 'K08':
        f_ = ri(3, 60)
        return dict(f=f_, s=min(250, max(f_ + 2, int(round(f_ * rng.uniform(1.5, 5.0))))), j=pl('sma', 'ema'))
    if fam == 'K09':
        f_ = ri(3, 24)
        return dict(f=f_, s=max(f_ + 2, int(round(f_ * rng.uniform(1.8, 3.0)))), g=ri(3, 18), z=pl(0, -1, 1))
    if fam == 'K10':
        return dict(n=ri(5, 260), v=pl(0, 0, 1.2, 1.5, 2.0, 2.5, 3.0))
    if fam == 'K11':
        return dict(n=ri(5, 25), m=ru(1.0, 5.0, 1))
    if fam == 'K12':
        return dict(n=ri(5, 25), x=ri(12, 40))
    if fam == 'K13':
        return dict(n=ri(5, 25), x=ri(10, 45))
    if fam == 'K14':
        return dict(r=ru(0.0, 0.12, 3), v=ru(1.2, 4.0, 1), p=pl(0.0, 0.5, 0.75))
    if fam == 'K15':
        return dict(g=ru(0.01, 0.20, 3), v=pl(0, 1.5, 2.0, 3.0))
    if fam == 'K16':
        return dict(g=ru(0.0, 0.06, 3), v=pl(0, 1.5, 2.0, 3.0))
    if fam == 'K17':
        return dict(n=ri(8, 120), tol=ru(0.0, 0.03, 3), j=pl('sma', 'ema'), tren=pl(0, 1))
    if fam == 'K18':
        return dict(x=ri(2, 25), y=ru(0.04, 0.35))
    if fam == 'K19':
        return dict(n=ri(8, 40), k=ru(0.8, 3.5, 1))
    if fam == 'K20':
        return dict(kb=ru(1.2, 2.8, 1), kk=ru(0.8, 2.2, 1))
    if fam == 'K21':
        return dict(k=ri(3, 15), d=pl(0, 1))
    if fam == 'K22':
        return dict(x=ri(18, 45), n=ri(8, 35))
    if fam == 'K23':
        return dict(x=ri(60, 97))
    if fam == 'K24':
        return dict(a=ru(0.05, 0.35), b=ru(0.65, 0.95))
    if fam == 'K25':
        return dict(n=ri(8, 80), w=ru(0.05, 0.40), v=pl(0, 1.5, 2.0))
    raise ValueError(fam)


def asal():
    """dict nama varian -> id pencetus asal (P../N..)."""
    peta = {(f, tuple(sorted(p.items()))): a for f, p, a in ASAL}
    out = {nama: peta[(fam, tuple(sorted(p.items())))] for nama, fam, p in grid() if (fam, tuple(sorted(p.items()))) in peta}
    assert len(out) == len(ASAL), 'ahli asal tidak ditemui dalam grid'
    return out


def teks(fam, p):
    t = NAMA[fam].format(**p)
    if p.get('tren'):
        t += ' + atas MA200'
    if fam == 'K03' and p['r']:
        t += f" + RSI14 < {p['r']}"
    if fam == 'K09' and p['z']:
        t += ' bawah sifar' if p['z'] < 0 else ' atas sifar'
    if fam in ('K10', 'K15', 'K16', 'K25') and p['v']:
        t += f" + volum {p['v']}x"
    if fam == 'K14' and p['p']:
        t += ' + tutup 25 % teratas'
    if fam == 'K21' and p['d']:
        t += ' + hari dalam'
    return t


class Ind:
    """Indikator satu saham dengan cache; takrif sama seperti cs_atom.indikator."""

    def __init__(self, g, rs):
        self.o, self.h, self.l, self.c, self.v = g.open, g.high, g.low, g.close, g.volume.astype(float)
        self.rs, self.idx, self._c = rs, g.index, {}
        self.pc = self.c.shift()
        self.tr = pd.concat([self.h - self.l, (self.h - self.pc).abs(), (self.l - self.pc).abs()], axis=1).max(axis=1)
        self.dl = self.c.diff()
        self.vr = self.v / self.v.rolling(50).mean().shift(1).replace(0, np.nan)
        self.ret1, self.gap = self.c / self.pc - 1, self.o / self.pc - 1
        self.pos = (self.c - self.l) / (self.h - self.l).replace(0, np.nan)

    def _m(self, kunci, f):
        if kunci not in self._c:
            self._c[kunci] = f()
        return self._c[kunci]

    def sma(self, n):
        return self._m(('sma', n), lambda: self.c.rolling(n).mean())

    def ema(self, n):
        return self._m(('ema', n), lambda: self.c.ewm(span=n, adjust=False, min_periods=n).mean())

    def ma(self, n, j):
        return self.sma(n) if j == 'sma' else self.ema(n)

    def sd(self, n):
        return self._m(('sd', n), lambda: self.c.rolling(n).std(ddof=0))

    def rsi(self, n):
        return self._m(('rsi', n), lambda: 100 - 100 / (1 + _w(self.dl.clip(lower=0), n)
                                                           / _w((-self.dl).clip(lower=0), n).replace(0, np.nan)))

    def atr(self, n):
        return self._m(('atr', n), lambda: _w(self.tr, n))

    def atr_r(self, n):
        return self._m(('atr_r', n), lambda: self.tr.rolling(n).mean())

    def hh(self, n):                                           # tinggi n bar SEBELUM hari ini
        return self._m(('hh', n), lambda: self.h.rolling(n).max().shift(1))

    def ll(self, n):
        return self._m(('ll', n), lambda: self.l.rolling(n).min().shift(1))

    def adx(self, n):
        def f():
            um, dm = self.h.diff(), -self.l.diff()
            pdm = pd.Series(np.where((um > dm) & (um > 0), um, 0.0), index=self.idx)
            ndm = pd.Series(np.where((dm > um) & (dm > 0), dm, 0.0), index=self.idx)
            a = self.atr(n)
            pdi, ndi = 100 * _w(pdm, n) / a, 100 * _w(ndm, n) / a
            return _w(100 * (pdi - ndi).abs() / (pdi + ndi).replace(0, np.nan), n), pdi, ndi
        return self._m(('adx', n), f)

    def st(self, n, m):
        return self._m(('st', n, m), lambda: pd.Series(atom._supertrend(
            self.h.to_numpy(float), self.l.to_numpy(float), self.c.to_numpy(float), self.atr(n).to_numpy(float), m),
            index=self.idx))

    def stoch(self, n):
        def f():
            lo, hi = self.l.rolling(n).min(), self.h.rolling(n).max()
            sk = (100 * (self.c - lo) / (hi - lo).replace(0, np.nan)).rolling(3).mean()
            return sk, sk.rolling(3).mean()
        return self._m(('stoch', n), f)

    def tren(self, ya):
        return (self.c > self.sma(200)) if ya else True

    def vol(self, v):
        return (self.vr >= v) if v else True


def syarat(I, fam, p):
    """Siri boolean syarat satu ahli keluarga (belum 'hari pertama')."""
    c, o, h, l = I.c, I.o, I.h, I.l
    k_ = lambda x: pd.Series(float(x), index=I.idx)
    if fam == 'K01':
        return (I.rsi(p['n']) < p['x']) & I.tren(p['tren'])
    if fam == 'K02':
        return _silang(I.rsi(p['n']), k_(p['x']))
    if fam == 'K03':
        s = c < I.sma(p['n']) - p['k'] * I.sd(p['n'])
        return s & (I.rsi(14) < p['r']) if p['r'] else s
    if fam == 'K04':
        b = I.sma(p['n']) - p['k'] * I.sd(p['n'])
        return (c.shift(1) < b.shift(1)) & (c > b)
    if fam == 'K05':
        return _silang(c, I.sma(p['n']) + p['k'] * I.sd(p['n']))
    if fam == 'K06':
        s = c < c.shift(1)
        for i in range(1, p['k'] - 1):
            s = s & (c.shift(i) < c.shift(i + 1))
        return s & I.tren(p['tren'])
    if fam == 'K07':
        return _silang(c, I.ma(p['n'], p['j']))
    if fam == 'K08':
        return _silang(I.ma(p['f'], p['j']), I.ma(p['s'], p['j']))
    if fam == 'K09':
        macd = I.ema(p['f']) - I.ema(p['s'])
        s = _silang(macd, macd.ewm(span=p['g'], adjust=False).mean())
        return s & (macd < 0) if p['z'] < 0 else s & (macd > 0) if p['z'] > 0 else s
    if fam == 'K10':
        return (c > I.hh(p['n'])) & I.vol(p['v'])
    if fam == 'K11':
        st = I.st(p['n'], p['m'])
        return (st > 0) & (st.shift() < 0)
    if fam == 'K12':
        adx, pdi, ndi = I.adx(p['n'])
        return _silang(adx, k_(p['x'])) & (pdi > ndi)
    if fam == 'K13':
        sk, sdd = I.stoch(p['n'])
        return _silang(sk, sdd) & (sk.shift() < p['x'])
    if fam == 'K14':
        naik = (I.ret1 > 0) if p['r'] == 0 else (I.ret1 >= p['r'])
        return naik & (I.vr >= p['v']) & ((I.pos >= p['p']) if p['p'] else True)
    if fam == 'K15':
        return (I.gap >= p['g']) & I.vol(p['v']) & (c >= o)
    if fam == 'K16':
        return (o > h.shift(1) * (1 + p['g'])) & (c > o) & I.vol(p['v'])
    if fam == 'K17':
        m = I.ma(p['n'], p['j'])
        return (m > m.shift(20)) & (l <= m * (1 + p['tol'])) & (c > m) & (c > I.pc) & I.tren(p['tren'])
    if fam == 'K18':
        return (c / c.shift(p['x']) - 1) <= -p['y']
    if fam == 'K19':
        return _silang(c, I.ema(p['n']) + p['k'] * I.atr_r(p['n']))
    if fam == 'K20':
        m20, sd20, a20 = I.sma(20), I.sd(20), I.atr_r(20)
        on = (m20 + p['kb'] * sd20 < m20 + p['kk'] * a20) & (m20 - p['kb'] * sd20 > m20 - p['kk'] * a20)
        mom = c - ((h.rolling(20).max() + l.rolling(20).min()) / 2 + m20) / 2
        return (~on) & _dulu(on) & (mom > 0)
    if fam == 'K21':
        jr = h - l
        s = jr <= jr.rolling(p['k'], min_periods=p['k']).min() + 1e-12
        return s & (h < h.shift(1)) & (l > l.shift(1)) if p['d'] else s
    if fam == 'K22':
        return (I.adx(14)[0] > p['x']) & (l <= I.ema(p['n'])) & (c > h.shift(1))
    if fam == 'K23':
        return (I.rs >= p['x']) & (I.rs.shift(1) < p['x']) & (c > I.sma(50))
    if fam == 'K24':
        jl = (h - l).replace(0, np.nan)
        return ((o - l) / jl <= p['a']) & ((c - l) / jl >= p['b'])
    if fam == 'K25':
        return ((I.hh(p['n']) / I.ll(p['n']) - 1) <= p['w']) & (c > I.hh(p['n'])) & I.vol(p['v'])
    raise ValueError(fam)


def kira(g, rs, G=None):
    """Matriks boolean [varian, bar] bagi satu saham (syarat benar pada bar itu)."""
    G = grid() if G is None else G
    I = Ind(g, rs)
    out = np.zeros((len(G), len(g)), bool)
    for i, (_, fam, p) in enumerate(G):
        s = syarat(I, fam, p)
        out[i] = np.asarray(s.fillna(False) if s.dtype != bool else s, dtype=bool)
    return out
