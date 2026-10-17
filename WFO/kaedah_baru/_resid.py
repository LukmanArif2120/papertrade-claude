# M162 RESID — momentum residual harian (spec: SPEC_SEMUA_KAEDAH.md, `FAIL ASAL: spec/M162`).
# resid(g, spy) -> (RESID, beta). e = r - beta.m (alfa tidak ditolak); beta tetingkap 252 hari (min 200); pembentukan t-251..t-21 (min 180).
# Disahkan lawan regresi terus (np.polyfit / lstsq) pada 17 Okt 2026.
import numpy as np, pandas as pd
def _rs(x, n, mp): return x.rolling(n, min_periods=mp).sum()
def _mom(cols, n, mp, sh=0):
    """Momen bergolek: dict nama->Series (sudah ditopeng). Pulangkan count, jumlah, jumlah hasil darab."""
    k={}; 
    for a in cols: k[a]=_rs(cols[a], n, mp).shift(sh)
    return k
def resid(g, mser, ind=None, nb=252, nf=231, lang=21, mp_b=200, mp_f=180):
    r=g.close.pct_change(); m=mser.reindex(g.index, method='ffill').pct_change()
    X=[m] if ind is None else [m, ind.reindex(g.index)]
    v=r.notna(); 
    for x in X: v&=x.notna()
    y=r.where(v); X=[x.where(v) for x in X]; one=v.astype(float).where(v)
    def stats(n, mp, sh):
        N=_rs(one,n,mp).shift(sh)
        Sy=_rs(y,n,mp).shift(sh); Sx=[_rs(x,n,mp).shift(sh) for x in X]
        Syy=_rs(y*y,n,mp).shift(sh); Sxy=[_rs(x*y,n,mp).shift(sh) for x in X]
        Sxx=[[_rs(a*b,n,mp).shift(sh) for b in X] for a in X]
        vy=(Syy-Sy*Sy/N)/(N-1); cxy=[(Sxy[a]-Sx[a]*Sy/N)/(N-1) for a in range(len(X))]
        cxx=[[(Sxx[a][b]-Sx[a]*Sx[b]/N)/(N-1) for b in range(len(X))] for a in range(len(X))]
        return N,Sy,Sx,vy,cxy,cxx
    N,_,_,_,cxy,cxx=stats(nb,mp_b,0)
    if len(X)==1: b=[cxy[0]/cxx[0][0]]
    else:
        det=cxx[0][0]*cxx[1][1]-cxx[0][1]**2
        b=[(cxx[1][1]*cxy[0]-cxx[0][1]*cxy[1])/det, (cxx[0][0]*cxy[1]-cxx[0][1]*cxy[0])/det]
    Nf,Sy,Sx,vy,cxy,cxx=stats(nf,mp_f,lang)
    se=Sy-sum(b[a]*Sx[a] for a in range(len(X)))
    ve=vy+sum(b[a]*b[c]*cxx[a][c] for a in range(len(X)) for c in range(len(X)))-2*sum(b[a]*cxy[a] for a in range(len(X)))
    out=se/(np.sqrt(ve)*np.sqrt(Nf))
    return out.where(N.notna() & Nf.notna() & (ve>0)), b[0]
