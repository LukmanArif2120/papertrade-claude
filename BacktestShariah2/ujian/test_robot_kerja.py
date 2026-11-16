"""Ujian robot_kerja.py dan robot_larian.py (tab Robot dashboard, 16 Nov 2026; paparan sahaja)."""
import os
import sys
import unittest
from datetime import datetime, timezone
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import robot_kerja as RK  # noqa: E402
import robot_larian as RL  # noqa: E402

UTC = timezone.utc


def larian(runs, dibina='2026-11-16T02:05:00Z'):
    return dict(dibina=dibina, runs=runs)


class TestJadual(unittest.TestCase):
    def test_tembakan_utc(self):
        # harian.yml '7 5 * * 2-6' dari Isnin 16 Nov 03:40 UTC -> Selasa 17 Nov 05:07 UTC
        f = RK.tembakan(['7 5 * * 2-6'], datetime(2026, 11, 16, 3, 40, tzinfo=UTC), hari=3)
        self.assertEqual(RK.iso(f[0]), '2026-11-17T05:07:00Z')

    def test_tembakan_zon_myt_dan_ny(self):
        mula = datetime(2026, 11, 16, 3, 40, tzinfo=UTC)
        # 16:41 MYT = 08:41 UTC
        self.assertEqual(RK.iso(RK.tembakan(['41 16 * * 2-6'], mula, hari=3, zon=RK.MYT)[0]), '2026-11-17T08:41:00Z')
        # 10:20 New York (EST, November) = 15:20 UTC; Isnin dibenarkan (1-6)
        self.assertEqual(RK.iso(RK.tembakan(['20 10 * * 1-6'], mula, hari=3, zon=RK.NY)[0]), '2026-11-16T15:20:00Z')

    def test_tembakan_suku_tahunan(self):
        f = RK.tembakan(['49 9 1 1,4,7,10 *'], datetime(2026, 11, 16, tzinfo=UTC), hari=100, zon=RK.MYT, had=1)
        self.assertEqual(RK.iso(f[0]), '2027-01-01T01:49:00Z')


class TestClaude(unittest.TestCase):
    def test_tugas_ikut_masa(self):
        self.assertEqual(RK.tugas_claude_semasa(datetime(2026, 11, 17, 8, 43, tzinfo=UTC)), 'tolak_ptg')   # 16:43 MYT
        self.assertEqual(RK.tugas_claude_semasa(datetime(2026, 11, 16, 15, 23, tzinfo=UTC)), 'tolak_ny')   # 10:23 NY
        self.assertEqual(RK.tugas_claude_semasa(datetime(2026, 11, 16, 17, 22, tzinfo=UTC)), 'semak_db')   # 12:22 NY
        self.assertEqual(RK.tugas_claude_semasa(datetime(2026, 11, 16, 22, 50, tzinfo=UTC), awal=True), 'awal')
        self.assertIsNone(RK.tugas_claude_semasa(datetime(2026, 11, 16, 3, 0, tzinfo=UTC)))           # sesi tangan

    def test_kemas_kekalkan_yang_lain(self):
        lama = {'awal': {'mula': '2026-11-13T22:48:14Z', 'akhir': '2026-11-13T22:49:39Z', 'hasil': 'success'}}
        rc = RK.kemas_robot_claude(lama, datetime(2026, 11, 17, 8, 43, tzinfo=UTC))
        self.assertEqual(rc['awal'], lama['awal'])
        self.assertEqual(rc['tolak_ptg']['mula'], '2026-11-17T08:43:00Z')
        self.assertEqual(RK.kemas_robot_claude(None, datetime(2026, 11, 16, 3, 0, tzinfo=UTC)), {})


class TestBina(unittest.TestCase):
    MASA = datetime(2026, 11, 16, 3, 40, tzinfo=UTC)

    def doc(self, runs, **kw):
        return {r['id']: r for r in RK.bina(masa=self.MASA, larian=larian(runs), mingguan=[], **kw)['robot']}

    def test_status_siap_gagal_senyap_belum(self):
        d = self.doc([
            ['harian.yml', '2026-11-14T17:00:02Z', '2026-11-14T17:03:55Z', 'completed', 'success', 'schedule'],
            ['lejar.yml', '2026-11-14T16:36:40Z', '2026-11-14T16:38:02Z', 'completed', 'failure', 'schedule'],
            ['amaran_ntfy.yml', '2026-11-16T00:54:56Z', '2026-11-16T00:54:58Z', 'completed', 'skipped', 'workflow_run'],
        ])
        self.assertEqual(d['harian']['status'], 'siap')
        self.assertEqual(d['harian']['seterusnya'], '2026-11-17T05:07:00Z')
        self.assertEqual(d['lejar']['status'], 'gagal')
        self.assertEqual(d['loceng']['status'], 'senyap')
        self.assertEqual(d['suku']['status'], 'belum')
        self.assertEqual(d['semak_db']['status'], 'senyap')     # tiada kesan bila semua baik
        self.assertEqual(len(d), len(RK.KATALOG))

    def test_lewat_bila_melepasi_jurang_jadual(self):
        # harian Sel-Sab 4 kali sehari: jurang terpanjang Sab 11:07 -> Sel 05:07 (66 jam) + 6 jam
        d = self.doc([['harian.yml', '2026-11-12T11:00:00Z', '2026-11-12T11:05:00Z', 'completed', 'success', 'schedule']])
        self.assertEqual(d['harian']['status'], 'lewat')

    def test_lewat_diukur_pada_masa_petikan(self):
        # petikan 02:05; penjaga 00:51 (sebelum petikan). Dibina 15:24 -> bukan lewat (larian selepas petikan
        # tidak kelihatan, bukan hilang)
        doc = RK.bina(masa=datetime(2026, 11, 16, 15, 24, tzinfo=UTC), mingguan=[], larian=larian([
            ['penjaga_jadual.yml', '2026-11-16T00:51:36Z', '2026-11-16T00:51:44Z', 'completed', 'success', 'push']]))
        d = {r['id']: r for r in doc['robot']}
        self.assertEqual(d['penjaga']['status'], 'siap')

    def test_petikan_basi_dinilai_pada_masa_sekarang(self):
        doc = RK.bina(masa=datetime(2026, 11, 20, 3, 0, tzinfo=UTC), mingguan=[], larian=larian([
            ['penjaga_jadual.yml', '2026-11-16T00:51:36Z', '2026-11-16T00:51:44Z', 'completed', 'success', 'push']]))
        d = {r['id']: r for r in doc['robot']}
        self.assertEqual(d['penjaga']['status'], 'lewat')

    def test_dibatalkan_tidak_dikira_terakhir(self):
        d = self.doc([
            ['semak_data.yml', '2026-11-14T02:53:00Z', '2026-11-14T02:56:00Z', 'completed', 'success', 'push'],
            ['semak_data.yml', '2026-11-14T02:56:30Z', '2026-11-14T02:57:00Z', 'completed', 'cancelled', 'pull_request'],
        ])
        self.assertEqual(d['semak']['akhir']['mula'], '2026-11-14T02:53:00Z')
        self.assertEqual(d['semak']['kiraan'], {'success': 1, 'cancelled': 1})

    def test_kiraan_hanya_dalam_tetingkap(self):
        doc = RK.bina(masa=self.MASA, larian=dict(dibina='2026-11-16T02:05:00Z', hari=4, runs=[
            ['institusi.yml', '2026-11-09T11:59:50Z', '2026-11-09T12:02:05Z', 'completed', 'success', 'schedule'],
            ['harian.yml', '2026-11-14T17:00:02Z', '2026-11-14T17:03:55Z', 'completed', 'success', 'schedule']]), mingguan=[])
        d = {r['id']: r for r in doc['robot']}
        self.assertEqual(doc['kiraan_sejak'], '2026-11-14T17:00:02Z')
        self.assertEqual(d['institusi']['kiraan'], {})
        self.assertEqual(d['institusi']['akhir']['mula'], '2026-11-09T11:59:50Z')   # terakhir tetap dipapar

    def test_sedang_berjalan_hanya_bila_petikan_segar(self):
        runs = [['harian.yml', '2026-11-16T01:00:00Z', None, 'in_progress', None, 'schedule']]
        segar = RK.bina(masa=datetime(2026, 11, 16, 2, 30, tzinfo=UTC), larian=larian(runs), mingguan=[])
        basi = RK.bina(masa=datetime(2026, 11, 16, 9, 0, tzinfo=UTC), larian=larian(runs), mingguan=[])
        g = lambda d: {r['id']: r for r in d['robot']}['harian']  # noqa: E731
        self.assertTrue(g(segar)['sedang'])
        self.assertFalse(g(basi)['sedang'])

    def test_pengejut_dari_penjaga_dicetus_tangan(self):
        d = self.doc([
            ['penjaga_jadual.yml', '2026-11-14T23:20:48Z', '2026-11-14T23:20:56Z', 'completed', 'success', 'workflow_dispatch'],
            ['penjaga_jadual.yml', '2026-11-14T23:42:00Z', '2026-11-14T23:42:10Z', 'completed', 'success', 'schedule'],
        ])
        self.assertEqual(d['cetus']['akhir']['mula'], '2026-11-14T23:20:48Z')
        self.assertEqual(d['penjaga']['akhir']['mula'], '2026-11-14T23:42:00Z')

    def test_robot_claude_dan_ulang_tayang(self):
        runs = [['harga_harian.yml', f'2026-11-14T0{h}:00:00Z', f'2026-11-14T0{h}:02:00Z', 'completed', 'success', 'schedule']
                for h in range(1, 6)]
        rc = {'tolak_ptg': {'mula': '2026-11-14T08:41:39Z', 'akhir': '2026-11-14T08:44:40Z', 'hasil': 'success'}}
        doc = RK.bina(masa=self.MASA, larian=larian(runs), robot_claude=rc, mingguan=[])
        self.assertEqual(doc['ulang'], {'mula': '2026-11-13T19:00:00Z', 'akhir': '2026-11-14T19:00:00Z'})
        d = {r['id']: r for r in doc['robot']}
        self.assertEqual(d['tolak_ptg']['status'], 'siap')
        self.assertEqual(len(d['tolak_ptg']['ulang']), 1)
        self.assertEqual(len(d['harga']['ulang']), 5)
        self.assertEqual(d['tolak_ny']['status'], 'belum')

    def test_tanpa_larian(self):
        doc = RK.bina(masa=self.MASA, larian=larian([]), mingguan=[])
        self.assertIsNone(doc['ulang'])
        self.assertEqual(len(doc['robot']), len(RK.KATALOG))


class TestLarian(unittest.TestCase):
    def test_kumpul_tetingkap_dan_terkini_luar(self):
        kini = datetime(2026, 11, 16, 3, 0, tzinfo=UTC)

        def r(i, wf, t):
            return dict(id=i, path=f'.github/workflows/{wf}', run_started_at=t, created_at=t, updated_at=t,
                        status='completed', conclusion='success', event='schedule')
        semua = [r(1, 'harian.yml', '2026-11-15T05:07:00Z'), r(2, 'luar_robot.yml', '2026-11-15T05:00:00Z')]
        mingguan = {'institusi.yml': [r(3, 'institusi.yml', '2026-11-09T11:59:50Z'), r(4, 'institusi.yml', '2026-11-02T03:37:00Z')]}

        def palsu(api, path, token):
            if '/actions/runs?' in path:
                return dict(workflow_runs=semua if 'page=1' in path else [])
            wf = path.split('/workflows/')[1].split('/')[0]
            return dict(workflow_runs=mingguan.get(wf, []))
        with mock.patch.object(RL, '_get', side_effect=palsu):
            d = RL.kumpul('https://api', 'o/r', 't', kini=kini)
        wfs = [b[0] for b in d['runs']]
        self.assertIn('harian.yml', wfs)
        self.assertNotIn('luar_robot.yml', wfs)            # bukan robot
        self.assertEqual([b[1] for b in d['runs'] if b[0] == 'institusi.yml'], ['2026-11-09T11:59:50Z'])  # terkini sahaja

    def test_main_tanpa_token_tidak_gagal(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(RL.main(), 0)


if __name__ == '__main__':
    unittest.main()
