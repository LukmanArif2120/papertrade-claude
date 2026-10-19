# Ujian standard/tuai_kewangan.py: transkrip sesi -> folder mentah gred_kewangan.py simpan
import os, sys, json, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import tuai_kewangan as TK  # noqa: E402
import gred_kewangan as GK  # noqa: E402


def laporan(label, ft, ms, nilai):
    return {'date_time': ms, 'period_text': label, 'financial_type': ft, 'currency_code': 'USD',
            'item_list': [{'display_name': 'Total Operating Revenue', 'data': nilai}]}


class TestTuai(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.baris = []

    def guna(self, i, nama, inp, hasil):
        self.baris.append({'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'id': f'u{i}', 'name': 'mcp__Moo_Moo__' + nama, 'input': inp}]}})
        self.baris.append({'type': 'user', 'timestamp': f'2026-10-19T00:00:{i:02d}Z', 'message': {'content': [
            {'type': 'tool_result', 'tool_use_id': f'u{i}', 'content': hasil}]}})

    def jalan(self):
        p = os.path.join(self.d, 'sesi.jsonl')
        with open(p, 'w', encoding='utf-8') as f:
            for b in self.baris:
                f.write(json.dumps(b) + '\n')
        keluar = os.path.join(self.d, 'mentah')
        return keluar, TK.tuai([p], keluar)

    def test_pecah_suku_tahunan_fail_simpan_dan_tiada(self):
        # suku + tahunan (ft 10) inline -> _9 dan _7
        r1 = {'ret_code': 0, 'data': {'report_list': [laporan('2026/Q2', 2, 1782748800000, 120.0),
                                                       laporan('2025/FY', 7, 1767110400000, 400.0),
                                                       laporan('2025/Q4', 4, 1767110400000, 110.0)]},
              'pagination': {'has_more': True, 'next_key': '1767110401|2025_4'}}
        self.guna(1, 'quote_financials_statements', {'symbol': 'US.XYZ', 'statement_type': 1, 'financial_type': 10,
                                                     'limit': 50, 'currency_code': 'USD'}, json.dumps(r1))
        # hasil besar yang disimpan alat ke fail
        simpan = os.path.join(self.d, 'besar.txt')
        with open(simpan, 'w', encoding='utf-8') as f:
            json.dump({'ret_code': 0, 'data': {'report_list': [laporan('2026/Q2', 2, 1782748800000, 9.0)]},
                       'pagination': {'has_more': False, 'next_key': '-1'}}, f)
        self.guna(2, 'quote_financials_statements', {'symbol': 'US.XYZ', 'statement_type': 2, 'financial_type': 10},
                  [{'type': 'text', 'text': f'Error: result (999,999 characters across 1 line) exceeds maximum allowed '
                                            f'tokens. Output has been saved to {simpan}.\nFormat: Plain text'}])
        # had kadar: diabaikan; tiada data: muktamad
        self.guna(3, 'quote_financials_statements', {'symbol': 'US.XYZ', 'statement_type': 3, 'financial_type': 10},
                  json.dumps({'ret_code': -11, 'ret_msg': 'rate limit exceeded'}))
        self.guna(4, 'quote_financials_earnings_price_history', {'symbol': 'US.XYZ'},
                  json.dumps({'ret_code': -10, 'ret_msg': 'no data'}))
        self.guna(5, 'quote_market_snapshot', {'code_list': ['US.XYZ', 'US.ABC']},
                  json.dumps({'ret_code': 0, 'data': {'snapshot_list': [{'code': 'US.XYZ', 'issued_shares': 1000},
                                                                        {'code': 'US.ABC', 'issued_shares': 5}]}}))
        keluar, st = self.jalan()
        fail = sorted(os.listdir(keluar))
        self.assertEqual(fail, ['ABC_snap.json', 'XYZ_1_7_p1.json', 'XYZ_1_9_p1.json', 'XYZ_2_9_p1.json',
                                'XYZ_snap.json', 'tuai_status.json'])
        self.assertEqual(st['XYZ']['1']['suku'], 2)
        self.assertEqual(st['XYZ']['1']['tahun'], 1)
        self.assertEqual(st['XYZ']['1']['next_key'], '1767110401|2025_4')
        self.assertNotIn('3', st['XYZ'])            # had kadar: perlu diulang
        self.assertEqual(st['XYZ']['eph'], 'tiada')
        # fail mentah boleh dibaca gred_kewangan.py simpan
        kew = os.path.join(self.d, 'kewangan')
        GK.simpan(keluar, kew, '2026-10-19')
        k = json.load(open(os.path.join(kew, 'XYZ.json'), encoding='utf-8'))
        self.assertEqual([e['label'] for e in k['suku']], ['2025/Q4', '2026/Q2'])
        self.assertEqual([e['label'] for e in k['tahunan']], ['2025/FY'])
        self.assertEqual(k['suku'][-1][GK.K], {})
        self.assertEqual(k['saham_terbit'], 1000.0)

    def test_halaman_kedua_dan_tiada_ditimpa_data(self):
        self.guna(1, 'quote_financials_statements', {'symbol': 'US.XYZ', 'statement_type': 1, 'financial_type': 10},
                  json.dumps({'ret_code': -10, 'ret_msg': 'no data'}))
        r = {'ret_code': 0, 'data': {'report_list': [laporan('2016/Q3', 3, 1475164800000, 50.0)]},
             'pagination': {'has_more': False, 'next_key': '-1'}}
        self.guna(2, 'quote_financials_statements', {'symbol': 'US.XYZ', 'statement_type': 1, 'financial_type': 10,
                                                     'next_key': '1475164801|2016_4'}, json.dumps(r))
        # format kedua hasil besar: <persisted-output> (fail = senarai blok teks)
        simpan = os.path.join(self.d, 'toolu_x.json')
        with open(simpan, 'w', encoding='utf-8') as f:
            json.dump([{'type': 'text', 'text': json.dumps(r)}], f)
        self.guna(3, 'quote_financials_statements', {'symbol': 'US.XYZ', 'statement_type': 3, 'financial_type': 10},
                  f'<persisted-output>\nOutput too large (57.6KB). Full output saved to: {simpan}\n\nPreview (first 2KB):\n[\n...\n</persisted-output>')
        keluar, st = self.jalan()
        self.assertTrue(os.path.exists(os.path.join(keluar, 'XYZ_3_9_p1.json')))
        self.assertTrue(os.path.exists(os.path.join(keluar, 'XYZ_1_9_k1475164801.json')))
        self.assertEqual(st['XYZ']['1']['halaman'], ['k1475164801'])
        self.assertFalse(st['XYZ']['1']['has_more'])


if __name__ == '__main__':
    unittest.main()
