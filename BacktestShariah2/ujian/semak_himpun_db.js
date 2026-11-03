/* Semakan PENGHIMPUNAN dokumen padat: "belum berhimpun" tidak boleh dilaporkan sebagai "tiada data".
 *
 * `ringkas_c` ialah 22 dokumen / 3.3 MB. Had satu batch ArtifactData ialah 900 KB, jadi tolakan db
 * malam menolaknya dalam beberapa panggilan berasingan - beberapa minit di mana dokumen asas dan
 * bahagiannya tidak sepadan. Pada 3 Nov 2026 halaman memapar "Belum ada posisi dalam pangkalan data"
 * dalam tingkap itu: 1,641 posisi Nxx dan 10,121 Mxx dilaporkan sebagai KOSONG. Bagi repo yang
 * tujuannya mengumpul data, mesej itu bukan sekadar hodoh - ia dakwaan palsu bahawa pengumpulan gagal.
 *
 * Perlu Playwright (tidak dipasang dalam semak_data.yml) jadi ia dijalankan TANGAN:
 *   node BacktestShariah2/ujian/semak_himpun_db.js <folder-db> [fail-html]
 * <folder-db> = <koleksi>/<doc>.json, cth. keluaran `ArtifactData list ... out_dir`, atau folder
 * keluaran `jana_db.py --keluar`. Keluar 0 = lulus.
 */
const fs = require('fs'), path = require('path'), os = require('os');
const { chromium } = require('playwright');
const DB = process.argv[2];
const HTML = process.argv[3] || path.join(__dirname, '..', 'standard', 'dashboard_v2.html');
if (!DB) { console.error('guna: node semak_himpun_db.js <folder-db> [fail-html]'); process.exit(2); }

function muat(dir) {
  const D = {};
  for (const c of fs.readdirSync(dir)) {
    const p = path.join(dir, c);
    if (!fs.statSync(p).isDirectory()) continue;
    for (const f of fs.readdirSync(p)) if (f.endsWith('.json')) D[c + '/' + f.slice(0, -5)] = JSON.parse(fs.readFileSync(path.join(p, f), 'utf8'));
  }
  return D;
}

async function jalan(D, tunggu) {
  const S = fs.mkdtempSync(path.join(os.tmpdir(), 'himpun-'));
  let h = fs.readFileSync(HTML, 'utf8');
  if (!/^\s*<!doctype/i.test(h)) h = '<!doctype html><html><head><meta charset=utf8></head><body>' + h + '</body></html>';
  fs.writeFileSync(path.join(S, 'd.html'), h);
  const br = await chromium.launch({ args: ['--headless', '--no-sandbox'] });
  const pg = await br.newPage({ viewport: { width: 1400, height: 1000 } });
  const ralat = [];
  pg.on('pageerror', e => ralat.push(String(e).slice(0, 200)));
  await pg.addInitScript(docs => {
    window.__D = docs;
    window.claude = { use: async function () { return {
      collection: function (c) { return { limit: function () { return { onSnapshot: function (cb) {
        cb({ docs: Object.keys(window.__D).filter(k => k.indexOf(c + '/') === 0).map(k => ({ id: k.slice(c.length + 1), exists: true, data: () => window.__D[k] })) });
        return function () {}; } }; } }; },
      doc: function (q) { return { onSnapshot: function (cb) { cb({ exists: !!window.__D[q], data: () => window.__D[q] }); return function () {}; } }; } }; } };
  }, D);
  await pg.goto('file://' + path.join(S, 'd.html'));
  await pg.waitForTimeout(tunggu);
  await (await pg.$('#mainTabs button[data-tab="posisi"]')).click();
  await pg.waitForTimeout(1200);
  const out = {};
  for (const v of ['cm', 'cn', 'gab']) {
    const b = await pg.$(`#subSeg button[data-sub="${v}"]`);
    if (!b) { out[v] = { tiadaButang: true }; continue; }
    await b.click(); await pg.waitForTimeout(1500);
    out[v] = await pg.evaluate(() => {
      const el = document.querySelector('section.view:not([hidden])');
      const ep = el.querySelector('.panel.empty') || el.querySelector('.rangka .sub');
      return { baris: el.querySelectorAll('table tbody tr').length,
               teks: ep ? ep.textContent.trim() : null,
               jumlah: (/(\d[\d,]*) posisi · ketik baris/.exec(el.textContent) || [, null])[1] };
    });
  }
  await br.close();
  return { out, ralat };
}

(async () => {
  const gagal = [];
  const penuh = muat(DB);
  // 1. db LENGKAP: setiap akaun mesti memapar barisnya, bukan panel kosong.
  {
    const { out, ralat } = await jalan(penuh, 7000);
    console.log('LENGKAP   ', JSON.stringify(out));
    if (ralat.length) gagal.push('ralat halaman: ' + ralat.join(' | '));
    for (const v of ['cm', 'cn']) {
      if (out[v].tiadaButang) { gagal.push(`butang akaun ${v} tiada`); continue; }
      if (!out[v].jumlah) gagal.push(`${v}: tiada jadual posisi (teks: ${out[v].teks})`);
    }
  }
  // 2. SATU bahagian dengan induk tak sepadan (keadaan tengah-tolakan): mesti "Memuatkan",
  //    dengan kiraan bahagian, dan JANGAN "Belum ada posisi". Tunggu > 20s: pemasa anti-
  //    tergantung menyala pada 20s dan dahulu ia yang menukar "Memuatkan" kepada dakwaan palsu.
  const bhg = Object.keys(penuh).filter(k => /^papertrade\/ringkas_c_\d+$/.test(k)).sort();
  if (!bhg.length) { console.log('LANGKAU   bahagian ringkas_c tiada dalam folder ini'); }
  else {
    const rosak = JSON.parse(JSON.stringify(penuh));
    rosak[bhg[bhg.length - 1]].induk = 'INDUK-LAIN';
    const { out, ralat } = await jalan(rosak, 24000);
    console.log('SEPARA    ', JSON.stringify(out));
    if (ralat.length) gagal.push('ralat halaman (separa): ' + ralat.join(' | '));
    for (const v of ['cm', 'cn', 'gab']) {
      const t = out[v].teks || '';
      if (/[Bb]elum ada posisi/.test(t)) gagal.push(`${v}: dokumen separa dilaporkan sebagai "tiada posisi" — ${t}`);
      else if (!/bahagian \d+\/\d+/.test(t)) gagal.push(`${v}: tiada kiraan bahagian semasa berhimpun — ${t || '(tiada teks)'}`);
      if (out[v].jumlah) gagal.push(`${v}: jadual SEPARA dirender (${out[v].jumlah} posisi) — pengawal kelengkapan tidak berfungsi`);
    }
  }
  if (gagal.length) { console.error('\nGAGAL:\n  ' + gagal.join('\n  ')); process.exit(1); }
  console.log('\nLULUS');
})();
