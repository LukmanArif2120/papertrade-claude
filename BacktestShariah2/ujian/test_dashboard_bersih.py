"""dashboard_v2.html mesti bebas tanda konflik git dan kurungan CSS mesti seimbang.

Sebab (16 Nov 2026): penggabungan dua sesi meninggalkan satu baris `=======` di tempat `}` penutup blok
@media; semua gaya selepasnya (tab Robot) hanya berlaku di telefon dan rosak, dan halaman itu sempat diterbitkan.
"""
import os
import re
import unittest

HTML = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard', 'dashboard_v2.html')


class TestDashboardBersih(unittest.TestCase):
    def setUp(self):
        with open(HTML, encoding='utf-8') as f:
            self.s = f.read()

    def test_tiada_tanda_konflik(self):
        buruk = [i + 1 for i, b in enumerate(self.s.split('\n')) if re.match(r'^(<{7}|={7}|>{7})( |$)', b)]
        self.assertEqual(buruk, [], f'tanda konflik git pada baris {buruk}')

    def test_kurungan_css_seimbang(self):
        for m in re.finditer(r'<style>(.*?)</style>', self.s, re.S):
            css = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
            d = 0
            for ch in css:
                d += (ch == '{') - (ch == '}')
                self.assertGreaterEqual(d, 0, 'kurungan } berlebihan dalam <style>')
            self.assertEqual(d, 0, 'blok CSS tidak ditutup dalam <style>')


if __name__ == '__main__':
    unittest.main()
