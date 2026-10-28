#!/bin/sh
# Rantaian penilaian leg SEC fasa 2: tunggu prasyarat, kemudian step10 -> step11 -> laporan.
#
# Gerbang BUKAN `belum_diisi = 0`. Sebabnya: `belum_diisi` mengira CIK yang tiada dalam `akses`,
# dan CIK tanpa 10-Q/10-K (ETF, dana, syarikat dorman dalam universe A02) boleh menyebabkan ia
# tidak pernah mencapai 0 -- rantaian akan tergantung selama-lamanya dan tiada hasil pada waktu
# pagi. Gerbang sebenar ialah apa yang SPEC_FASA2 §9.5/§9.7 tuntut: >= 10 tahun layak (>= 3,000
# peristiwa dengan lajur tidak kosong) bagi KETIGA-TIGA lajur SEC.
#
# Pengesan dataran: jika liputan tidak bertambah selama DATARAN kitaran berturut-turut, rantaian
# diteruskan dengan liputan yang ada. Itu selamat kerana §9.5/§9.7 melaporkan lajur yang tidak
# cukup sebagai BELUM BOLEH DINILAI -- bukan lulus dan bukan gagal.
#
# Guna: nohup setsid sh REVERSE/jalan_fasa2_sec.sh > /tmp/claude-0/fasa2.log 2>&1 &
set -u
cd "$(dirname "$0")/.." || exit 1
JEDA=600          # saat antara kitaran
DATARAN=4         # kitaran tanpa pertambahan liputan sebelum diteruskan
LOG() { echo "[$(date -u +%H:%M:%S)] $*"; }

layak() {   # cetak "sue tumbuh_hasil pecutan_hasil" = bilangan tahun layak setiap lajur
  python3 - <<'PY' 2>/dev/null || echo "0 0 0"
import pandas as pd
d = pd.read_csv('REVERSE/sec_liputan.csv')
print(' '.join(str(int((d[f'n_{k}'] >= 3000).sum())) for k in ('sue', 'tumbuh_hasil', 'pecutan_hasil')))
PY
}

LOG "menunggu step1 14 tahun"
while :; do
  n=$(ls REVERSE/.cache/signals_*.parquet 2>/dev/null | wc -l)
  [ "$n" -ge 14 ] && break
  LOG "step1 $n/14"
  sleep "$JEDA"
done
LOG "step1 14/14 siap"

sama=0; lalu=""
while :; do
  git fetch -q origin main 2>/dev/null && git merge --no-edit -q origin/main >/dev/null 2>&1
  python3 REVERSE/step10_sec.py > /tmp/claude-0/step10_gerbang.log 2>&1 || { LOG "GAGAL step10"; exit 1; }
  L=$(layak)
  baki=$(python3 -c "import json;print(json.load(open('BacktestShariah2/data/sec/status.json')).get('belum_diisi','?'))" 2>/dev/null || echo '?')
  LOG "tahun layak (sue tumbuh pecutan) = $L | belum_diisi=$baki"
  kurang=$(echo "$L" | tr ' ' '\n' | awk '$1 < 10' | wc -l)
  [ "$kurang" -eq 0 ] && { LOG "gerbang §9.7 dipenuhi: ketiga-tiga lajur >= 10 tahun layak"; break; }
  if [ "$L" = "$lalu" ]; then
    sama=$((sama + 1))
    LOG "liputan tidak bertambah ($sama/$DATARAN)"
    [ "$sama" -ge "$DATARAN" ] && { LOG "DATARAN: diteruskan dengan liputan yang ada; lajur tidak cukup akan dilapor BELUM BOLEH DINILAI"; break; }
  else
    sama=0
  fi
  lalu=$L
  sleep "$JEDA"
done

LOG "step11_sec_nilai.py (penilaian §5; sekali sahaja)"
python3 REVERSE/step11_sec_nilai.py > /tmp/claude-0/step11.log 2>&1 || { LOG "GAGAL step11"; exit 1; }
LOG "jana_keputusan_fasa2.py"
python3 REVERSE/jana_keputusan_fasa2.py >> /tmp/claude-0/step11.log 2>&1 || { LOG "GAGAL laporan"; exit 1; }
LOG "RANTAIAN SIAP"
