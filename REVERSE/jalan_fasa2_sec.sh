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
DATARAN=12        # kitaran tanpa pertambahan sebelum diteruskan (12 x 600s = 2 jam;
                  # MESTI jauh lebih lama daripada satu larian isian awal ~45 min,
                  # jika tidak rantaian berputus asa sebelum larian itu commit)
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
  # Gerbang = KEDUA-DUA syarat (§9.9): >= 10 tahun layak setiap lajur (§9.7) DAN isian awal
  # selesai (§4.4 "populasi penuh"). Tahun layak sahaja tidak cukup: pada 28 Okt 16:30 gerbang
  # lama dipenuhi (13 13 13) sedangkan liputan hanya 48% ticker dan 1,530 CIK belum diisi.
  kurang=$(echo "$L" | tr ' ' '\n' | awk '$1 < 10' | wc -l)
  if [ "$kurang" -eq 0 ] && [ "$baki" = "0" ]; then
    LOG "gerbang §9.9 dipenuhi: >= 10 tahun layak setiap lajur DAN isian awal selesai"
    break
  fi
  if [ "$L $baki" = "$lalu" ]; then
    sama=$((sama + 1))
    LOG "liputan tidak bertambah ($sama/$DATARAN)"
    [ "$sama" -ge "$DATARAN" ] && { LOG "DATARAN: diteruskan dengan liputan yang ada; lajur tidak cukup akan dilapor BELUM BOLEH DINILAI"; break; }
  else
    sama=0
  fi
  lalu="$L $baki"
  sleep "$JEDA"
done

LOG "step11_sec_nilai.py (penilaian §5; sekali sahaja)"
python3 REVERSE/step11_sec_nilai.py > /tmp/claude-0/step11.log 2>&1 || { LOG "GAGAL step11"; exit 1; }
# §5.4 hanya jika §5.1 dan §5.3 lulus (§6 syarat 1). step12 sendiri menolak untuk berjalan jika
# tiada signal lulus, jadi keluar bukan-sifar di sini BUKAN kegagalan rantaian.
LOG "step12_sec_portfolio.py (§5.4; hanya jika §5 lulus)"
if python3 REVERSE/step12_sec_portfolio.py >> /tmp/claude-0/step11.log 2>&1; then
  LOG "§5.4 dijalankan"
else
  LOG "§5.4 dilangkau (tiada signal lulus §5.3, atau §5 belum ada) — lihat step11.log"
fi

LOG "jana_keputusan_fasa2.py"
python3 REVERSE/jana_keputusan_fasa2.py >> /tmp/claude-0/step11.log 2>&1 || { LOG "GAGAL laporan"; exit 1; }
LOG "RANTAIAN SIAP"
