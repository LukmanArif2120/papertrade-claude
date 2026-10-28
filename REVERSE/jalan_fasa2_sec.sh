#!/bin/sh
# Rantaian penilaian leg SEC fasa 2: tunggu prasyarat, kemudian jalankan step10 -> step11 -> laporan.
#
# Prasyarat:
#   1. signals_<tahun>.parquet bagi 2012-2025 (step1_run.py)   -- 14 fail
#   2. data/sec/ terkini daripada main (isian awal fundamental_sec.yml)
#
# Ia memeriksa setiap 4 minit dan berjalan sebaik kedua-dua dipenuhi. `--tunggu-sec tidak` =
# jangan tunggu isian awal (guna liputan yang ada sekarang).
#
# Guna: nohup sh REVERSE/jalan_fasa2_sec.sh [tunggu_sec] > /tmp/fasa2.log 2>&1 &
set -u
cd "$(dirname "$0")/.." || exit 1
TUNGGU_SEC="${1:-ya}"
LOG() { echo "[$(date -u +%H:%M:%S)] $*"; }

LOG "menunggu prasyarat (step1 14 tahun; isian awal SEC: $TUNGGU_SEC)"
while :; do
  n=$(ls REVERSE/.cache/signals_*.parquet 2>/dev/null | wc -l)
  git fetch -q origin main 2>/dev/null || true
  baki=$(git show origin/main:BacktestShariah2/data/sec/status.json 2>/dev/null \
         | python3 -c "import json,sys;print(json.load(sys.stdin).get('belum_diisi','?'))" 2>/dev/null || echo '?')
  LOG "step1 $n/14 | SEC belum_diisi=$baki"
  [ "$n" -ge 14 ] || { sleep 240; continue; }
  if [ "$TUNGGU_SEC" = "ya" ] && [ "$baki" != "0" ]; then sleep 240; continue; fi
  break
done

LOG "prasyarat dipenuhi; tarik data SEC terkini daripada main"
git fetch -q origin main && git merge --no-edit -q origin/main || LOG "AMARAN: merge main gagal; guna salinan kerja"

LOG "step10_sec.py (join semua tahun)"
python3 REVERSE/step10_sec.py || { LOG "GAGAL step10"; exit 1; }

LOG "step11_sec_nilai.py (penilaian §5; sekali sahaja)"
python3 REVERSE/step11_sec_nilai.py || { LOG "GAGAL step11"; exit 1; }

LOG "jana_keputusan_fasa2.py"
python3 REVERSE/jana_keputusan_fasa2.py || { LOG "GAGAL laporan"; exit 1; }

LOG "RANTAIAN SIAP"
