# Ringkasan masa setiap tugasan → AUTOTUNE/hasil/tala/_masa.csv (dibaca rancang.py untuk anggaran kos).
# Guna: python3 masa.py [dir_hasil]
import os, sys, json, glob
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala


def main(d=tala.KELUAR):
    R = []
    for f in sorted(glob.glob(os.path.join(d, 'M*', 'k*.json'))):
        try: H = json.load(open(f))
        except Exception: continue
        m = H.get('masa') or {}
        R.append(dict(kaedah=H.get('kaedah'), kajian=H.get('kajian'), status=H.get('status'), n_trials=H.get('n_trials'),
                      n_trials_diminta=H.get('n_trials_diminta'), s_percubaan=m.get('s_percubaan'), s_jumlah=m.get('jumlah'),
                      s_muat=m.get('muat_latih'), s_ujian=m.get('ujian'), rss_mb=H.get('rss_mb'), silang=H.get('silang'),
                      belum_ditala=H.get('belum_ditala'), mula=H.get('mula'), ralat=' | '.join(H.get('ralat') or [])[:200]))
    if not R: print('tiada hasil'); return
    D = pd.DataFrame(R)
    D['_n'] = pd.to_numeric(D.kaedah.str[1:], errors='coerce')
    D = D.sort_values(['_n', 'kajian']).drop(columns='_n')
    D.to_csv(os.path.join(d, '_masa.csv'), index=False)
    print(f"{len(D)} tugasan; SIAP {(D.status == 'SIAP').sum()}; s/cuba median {D.s_percubaan.median():.2f}; "
          f"rss maks {D.rss_mb.max()} MB")


if __name__ == '__main__':
    main(*sys.argv[1:])
