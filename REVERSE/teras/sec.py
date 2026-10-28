"""Masa ketersediaan data SEC (REVERSE fasa 2 leg SEC; `SPEC_FASA2.md` §4.2).

Masalah: 52% earnings 8-K difail SELEPAS tutup 16:00 ET (petikan 28 Okt 2026: 28,161 daripada
54,109; pra-buka 35.5%, intraday 12.4%), dan 5.2% baris mempunyai `tarikh_fail` berbeza daripada
tarikh ET `masa_terima`. Menggunakan `tarikh_fail` sebagai tarikh ketersediaan memberi lebih separuh
peristiwa maklumat kira-kira satu sesi dagangan lebih awal — tepat jenis kelebihan palsu yang fasa 1
dibina untuk mengelak.

Peraturan dikunci: hari tersedia = sesi dagangan PERTAMA yang pembukaannya (09:30 ET) jatuh
selepas cap masa pemfailan. Ia sejajar dengan REVERSE `SPEC.md` §3.1 (masuk pada buka esok) dan
melayan ketiga-tiga kes dengan satu peraturan:

    difail 06:00 ET Sel  -> tersedia buka Sel       (pra-buka sesi yang sama)
    difail 11:00 ET Sel  -> tersedia buka Rab       (intraday; buka Sel sudah lepas)
    difail 20:00 ET Sel  -> tersedia buka Rab       (selepas tutup)
    difail 20:00 ET Jum  -> tersedia buka Isn       (kalendar sesi melangkau hujung minggu/cuti)

Zon waktu dikira dengan `America/New_York` (zoneinfo), bukan offset tetap: 2004-2026 merangkumi
banyak peralihan waktu musim panas, dan peraturan 2007 menukar tarikh peralihan itu.
"""
from datetime import time
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

NY = ZoneInfo('America/New_York')
BUKA = time(9, 30)


def hari_tersedia(masa, sesi, tarikh_sandaran=None):
    """Series tarikh (datetime64[ns]) sesi pertama yang bukanya selepas `masa`.

    masa: Series cap masa pemfailan (apa-apa bentuk yang `to_datetime(utc=True)` terima).
    sesi: senarai/array tarikh sesi dagangan tersusun (stor harga; bukan kalendar kalendar).
    tarikh_sandaran: Series tarikh bagi baris yang `masa` kosong (cth. `sumber_tarikh == 'fail'`,
        di mana hanya tarikh pemfailan 10-Q/10-K diketahui). Baris itu dianggap SELEPAS TUTUP
        pada tarikh itu — pilihan konservatif, kerana waktu sebenar tidak diketahui.
    Baris tanpa kedua-duanya, atau yang jatuh selepas sesi terakhir, pulang NaT.
    """
    masa = pd.to_datetime(pd.Series(masa).reset_index(drop=True), utc=True, errors='coerce')
    ny = masa.dt.tz_convert(NY)
    # Pra-buka -> sesi hari sama; selainnya -> sesi selepas hari itu.
    calon = pd.Series(pd.NaT, index=masa.index, dtype='datetime64[ns]')
    ada = ny.notna()
    if ada.any():
        hari = ny[ada].dt.normalize().dt.tz_localize(None)
        pra = (ny[ada].dt.hour * 60 + ny[ada].dt.minute) < (BUKA.hour * 60 + BUKA.minute)
        calon[ada] = hari + pd.to_timedelta((~pra).astype(int), unit='D')
    if tarikh_sandaran is not None:
        sd = pd.to_datetime(pd.Series(tarikh_sandaran).reset_index(drop=True), errors='coerce')
        guna = calon.isna() & sd.notna()
        calon[guna] = sd[guna].dt.normalize() + pd.Timedelta(days=1)   # waktu tidak diketahui = selepas tutup
    if tarikh_sandaran is not None:
        # Tidak lebih awal daripada tarikh pemfailan rasmi: EDGAR tutup pada cuti persekutuan yang NYSE buka (Columbus
        # Day, Veterans Day), jadi 8-K diterima hujung minggu/cuti tersebar pada filingDate, bukan sesi pertama
        # selepas cap masa (28 Okt 2026: LRN 2011-10-10, MIDD 2015-11-11 mendahului tarikh_umum sehari).
        lantai = sd.dt.normalize()
        lebih_awal = calon.notna() & lantai.notna() & (calon < lantai)
        calon[lebih_awal] = lantai[lebih_awal]
    s = np.sort(pd.to_datetime(pd.Series(list(sesi))).values.astype('datetime64[ns]'))
    ix = np.searchsorted(s, calon.values.astype('datetime64[ns]'), side='left')
    hasil = pd.Series(pd.NaT, index=calon.index, dtype='datetime64[ns]')
    sah = calon.notna().values & (ix < len(s))
    hasil[sah] = s[ix[sah]]
    return hasil
