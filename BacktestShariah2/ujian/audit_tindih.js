/* Audit tindihan paparan dashboard (v172, 9 Nov 2026, keputusan pengguna "cuba check keseluruhan dashboard").
 *
 * Mencari tiga jenis cacat yang dilihat pengguna pada telefon:
 *   TINDIH   — dua teks bertindih pada skrin dan tiada lapisan legap di antaranya (contoh: bulatan G1–G6
 *              terapung di atas butang kaki helaian; label 0% menindih bilangan bar).
 *   POTONG   — teks terpotong oleh induk overflow:hidden tanpa elipsis (contoh: cip "ISYARAT JUA").
 *   LEBAR    — halaman lebih lebar daripada skrin (skrol mendatar).
 * Melawat SETIAP tab, kumpulan (#kumpSeg) dan bahagian rel (.pnav-in), dan membuka helaian posisi dan kaedah (setiap
 * sub-tab), pada komputer 1440×1000 dan telefon 390×660 (tinggi paparan dalam app Claude di iPhone); setiap keadaan diskrol dari atas ke bawah (halaman atau helaian)
 * supaya unsur melekit (pengepala, kaki helaian, bar tab bawah) diuji pada setiap kedudukan. Telefon meniru ruang
 * selamat iPhone (env(safe-area-inset-bottom) = 34px) kerana Chromium ujian memulangkan 0.
 *
 * Perlu Playwright dan folder db daripada jana_db.py; dijalankan TANGAN (tiada dalam semak_data.yml):
 *   python3 BacktestShariah2/standard/jana_db.py --keluar /tmp/db
 *   node BacktestShariah2/ujian/audit_tindih.js /tmp/db [fail-html]
 * Keluar 1 jika ada cacat. Tab Rujukan memerlukan kaedah/katalog.json dan registry/<ID>.json dalam folder db
 * (lihat standard/dashboard.md v171).
 */
const fs = require('fs'), path = require('path'), os = require('os');
const { chromium } = require('playwright');
const DB = process.argv[2], HTML = process.argv[3] || path.join(__dirname, '..', 'standard', 'dashboard_v2.html');
if (!DB) { console.error('guna: node audit_tindih.js <folder-db> [fail-html]'); process.exit(2); }
const D = {};
for (const c of fs.readdirSync(DB)) { const p = path.join(DB, c); if (!fs.statSync(p).isDirectory()) continue;
  for (const f of fs.readdirSync(p)) if (f.endsWith('.json')) D[c + '/' + f.slice(0, -5)] = JSON.parse(fs.readFileSync(path.join(p, f), 'utf8')); }

/* dijalankan dalam halaman: pulangkan senarai cacat pada keadaan skrin semasa */
const semak = (label) => {
  const W = innerWidth, H = innerHeight, out = [];
  // kelegapan warna: rgb()/rgba(), dan color(srgb r g b / a) yang dipulangkan Chromium untuk color-mix()
  const alfa = c => { if (!c || c === 'transparent') return 0;
    let m = c.match(/^rgba?\(([^)]+)\)/); if (m) { const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return p.length > 3 ? p[3] : 1; }
    m = c.match(/^color\([^)]*?\/\s*([\d.]+)\s*\)$/); if (m) return +m[1]; return /^color\(/.test(c) ? 1 : 0; };
  // lapisan legap: warna latar legap, ATAU gradien yang setiap hentian warnanya legap (kaki helaian bergradien dari
  // lut sinar TIDAK dikira legap - itulah pepijat kaki helaian), ATAU backdrop-filter dengan latar separa legap
  const legap = c => { if (alfa(c.backgroundColor) >= 0.85) return true;
    if (/gradient/.test(c.backgroundImage)) { const w = c.backgroundImage.match(/(rgba?\([^)]*\)|color\([^)]*\))/g) || []; if (w.length && Math.min(...w.map(alfa)) >= 0.85) return true; }
    return c.backdropFilter && c.backdropFilter !== 'none' && alfa(c.backgroundColor) >= 0.6; };
  const nama = el => { const c = (el.getAttribute && el.getAttribute('class') || '').trim().split(/\s+/).slice(0, 2).join('.');
    return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  // kotak teks: setiap nod teks langsung, satu kotak setiap baris
  const T = [];
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => n.textContent.trim() ? 1 : 2 });
  let n; while ((n = tw.nextNode())) {
    const el = n.parentElement; if (!el || el.closest('script,style,title,option,#tip,.tip,.toast')) continue;
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    for (const r of rg.getClientRects()) {
      if (r.width < 2 || r.height < 2 || r.right <= 0 || r.bottom <= 0 || r.left >= W || r.top >= H) continue;
      T.push({ el, r, t: n.textContent.trim().slice(0, 30) });
      // POTONG: teks melepasi induk overflow:hidden/clip (bukan bekas skrol, bukan elipsis)
      for (let a = el; a && a !== document.body; a = a.parentElement) {
        const ac = getComputedStyle(a);
        if (/(auto|scroll)/.test(ac.overflowX + ac.overflowY)) break;
        if (/(hidden|clip)/.test(ac.overflowX) || /(hidden|clip)/.test(ac.overflowY)) {
          const ar = a.getBoundingClientRect();
          const keluar = r.right > ar.right + 1.5 || r.left < ar.left - 1.5 || (/(hidden|clip)/.test(ac.overflowY) && (r.bottom > ar.bottom + 1.5 || r.top < ar.top - 1.5));
          const elip = ac.textOverflow === 'ellipsis' || getComputedStyle(el).textOverflow === 'ellipsis';
          const lineclamp = ac.webkitLineClamp && ac.webkitLineClamp !== 'none';
          if (keluar && !elip && !lineclamp && ar.width > 0 && ar.height > 0)
            out.push({ jenis: 'POTONG', a: nama(el) + ' "' + n.textContent.trim().slice(0, 24) + '"', b: 'oleh ' + nama(a), label });
          break;
        }
      }
    }
  }
  // TINDIH: pasangan kotak teks bersilang, kedua-duanya kelihatan (tiada lapisan legap di antara)
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) {
    const A = T[i], B = T[j]; if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
    const x1 = Math.max(A.r.left, B.r.left), x2 = Math.min(A.r.right, B.r.right), y1 = Math.max(A.r.top, B.r.top), y2 = Math.min(A.r.bottom, B.r.bottom);
    if (x2 - x1 < 3 || y2 - y1 < 3) continue;
    const st = document.elementsFromPoint((x1 + x2) / 2, (y1 + y2) / 2);
    const ia = st.findIndex(e => e === A.el || A.el.contains(e)), ib = st.findIndex(e => e === B.el || B.el.contains(e));
    if (ia < 0 || ib < 0) continue;            // salah satu terklip / tidak dilukis di titik itu
    const [atas, bawah] = ia < ib ? [ia, ib] : [ib, ia];
    const elBawah = st[bawah];
    let tertutup = false;
    for (let k = atas; k < bawah; k++) { const e = st[k]; if (e.contains(elBawah)) continue;
      if (legap(getComputedStyle(e))) { tertutup = true; break; } }
    if (tertutup) continue;
    out.push({ jenis: 'TINDIH', a: nama(A.el) + ' "' + A.t + '"', b: nama(B.el) + ' "' + B.t + '"', label });
  }
  if (document.documentElement.scrollWidth > W + 1) out.push({ jenis: 'LEBAR', a: 'halaman ' + document.documentElement.scrollWidth + 'px', b: 'skrin ' + W + 'px', label });
  return out;
};

(async () => {
  const S = fs.mkdtempSync(path.join(os.tmpdir(), 'tindih-'));
  const asal = fs.readFileSync(HTML, 'utf8');
  const br = await chromium.launch();
  const semua = [];
  for (const [nm, vp, mob] of [['komputer', { width: 1440, height: 1000 }, false], ['telefon', { width: 390, height: 660 }, true]]) {
    // telefon: tiru ruang selamat bawah iPhone (Chromium memulangkan 0 untuk env())
    const h = mob ? asal.replace(/env\(safe-area-inset-bottom,\s*0px\)/g, '34px') : asal;
    fs.writeFileSync(path.join(S, nm + '.html'), '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>' + h + '</body></html>');
    const pg = await br.newPage({ viewport: vp, isMobile: mob, hasTouch: mob });
    const er = []; pg.on('pageerror', e => er.push(String(e).slice(0, 160)));
    await pg.addInitScript(([docs]) => { window.__D = docs; window.claude = { use: async () => ({
      collection: c => ({ limit: () => ({ onSnapshot: (ok) => { setTimeout(() => ok({ docs: Object.keys(window.__D).filter(k => k.indexOf(c + '/') === 0).map(k => ({ id: k.slice(c.length + 1), exists: true, data: () => window.__D[k] })) }), 0); return () => {}; } }) }),
      doc: q => ({ onSnapshot: (ok) => { setTimeout(() => ok({ exists: !!window.__D[q], data: () => window.__D[q] }), 0); return () => {}; } }) }) }; }, [D]);
    await pg.goto('file://' + path.join(S, nm + '.html')); await pg.waitForTimeout(6000);
    const klik = async (s, t = 600) => { await pg.evaluate(s => { const e = document.querySelector(s); if (e) e.click(); }, s); await pg.waitForTimeout(t); };
    // skrol halaman (atau helaian) dari atas ke bawah, semak pada setiap langkah
    const imbas = async (label, helaian) => {
      const tinggi = await pg.evaluate(h => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = 0; return [e.scrollHeight, e.clientHeight]; }, helaian);
      const f = helaian ? 0.22 : 0.8, langkah = Math.max(1, Math.min(40, Math.ceil(tinggi[0] / (tinggi[1] * f))));
      for (let s = 0; s < langkah; s++) {
        await pg.evaluate(([h, s, ch, f]) => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = s * ch * f; }, [helaian, s, tinggi[1], f]);
        await pg.waitForTimeout(120);
        for (const d of await pg.evaluate(semak, `${nm} · ${label} · skrol ${s + 1}/${langkah}`)) semua.push(d);
      }
      await pg.evaluate(h => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = 0; }, helaian);
    };
    const tabs = await pg.$$eval('#mainTabs button[data-tab]', bs => bs.map(b => b.dataset.tab));
    for (const t of tabs) {
      await klik(`#mainTabs button[data-tab="${t}"]`);
      const kump = await pg.$$eval('#kumpSeg:not([hidden]) button', bs => bs.map(b => b.dataset.k)).catch(() => []);
      for (const k of (kump.length ? kump : [null])) {
        if (k) await klik(`#kumpSeg button[data-k="${k}"]`, 900);
        const bh = await pg.$$eval('.pnav-in button', bs => bs.filter(b => b.getClientRects().length).map(b => b.textContent.trim().slice(0, 24)));
        for (let i = 0; i < Math.max(1, bh.length); i++) {
          await pg.evaluate(i => { const b = [...document.querySelectorAll('.pnav-in button')].filter(b => b.getClientRects().length)[i]; if (b) b.click(); }, i);
          await pg.waitForTimeout(500);
          await imbas(`${t}${k ? '/' + k : ''}${bh[i] ? ' › ' + bh[i] : ''}`, false);
        }
      }
    }
    for (const [tab, rx, sel, nmS] of [['posisi', 'keputusan', '[data-pos]', 'helaian posisi'], ['analisis', 'Kad skor setiap', '[data-kd]', 'helaian kaedah']]) {
      await klik(`#mainTabs button[data-tab="${tab}"]`);
      await pg.evaluate(() => { const b = document.querySelector('#kumpSeg:not([hidden]) button'); if (b) b.click(); }); await pg.waitForTimeout(800);
      await pg.evaluate(rx => { const b = [...document.querySelectorAll('.pnav-in button')].find(x => x.getClientRects().length && new RegExp(rx, 'i').test(x.textContent)); if (b) b.click(); }, rx);
      await pg.waitForTimeout(1200);
      const ada = await pg.evaluate(sel => { const e = [...document.querySelectorAll(sel)].find(x => x.getClientRects().length); if (!e) return false; e.scrollIntoView(); e.click();
        const buka = () => !!document.querySelector('#sheet:not([hidden]) .pv2');
        if (!buka()) { const b = e.querySelector('.mbtn-b') || (e.closest('tr') && e.closest('tr').querySelector('.mbtn-b')); if (b) b.click(); }
        return buka(); }, sel);
      await pg.waitForTimeout(1200);
      if (!ada) { semua.push({ jenis: 'UJIAN', a: nmS + ' tidak dapat dibuka', b: '', label: nm }); continue; }
      const st = await pg.$$eval('#sheet .pv2tabs button', bs => bs.map(b => b.textContent.trim()));
      for (let i = 0; i < Math.max(1, st.length); i++) {
        await pg.evaluate(i => { const b = document.querySelectorAll('#sheet .pv2tabs button')[i]; if (b) b.click(); }, i);
        await pg.waitForTimeout(700);
        await imbas(`${nmS} › ${st[i] || ''}`, true);
      }
      await pg.evaluate(() => { const c = document.querySelector('#sheet .pv2x,#sheet .close'); if (c) c.click(); }); await pg.waitForTimeout(400);
    }
    if (er.length) semua.push({ jenis: 'RALAT', a: er.slice(0, 3).join(' | '), b: '', label: nm });
    await pg.close();
  }
  await br.close();
  // satukan: satu baris setiap cacat unik, dengan keadaan pertama dan bilangan kejadian
  const U = new Map();
  for (const d of semua) { const k = d.jenis + '|' + d.a + '|' + d.b; const u = U.get(k); if (u) u.n++; else U.set(k, Object.assign({ n: 1 }, d)); }
  const L = [...U.values()].sort((x, y) => x.jenis.localeCompare(y.jenis) || x.label.localeCompare(y.label));
  for (const d of L) console.log(`${d.jenis.padEnd(6)} ${d.a}  ×  ${d.b}   [${d.label}]${d.n > 1 ? ' (x' + d.n + ')' : ''}`);
  console.log(`\n${L.length} cacat unik`);
  process.exit(L.length ? 1 : 0);
})();
