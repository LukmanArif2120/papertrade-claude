/* Pemeriksa paparan dashboard yang dijalankan DALAM halaman (pg.evaluate). Dikongsi oleh audit_tindih.js (pantas)
 * dan audit_terperinci.js (mendalam). Setiap fungsi memulangkan senarai {jenis, a, b, label} bagi skrin semasa sahaja.
 *
 * semak(label)                  TINDIH (teks atas teks tanpa lapisan legap di antara), POTONG (teks diklip tanpa
 *                               elipsis), LEBAR (halaman lebih lebar daripada skrin)
 * semakLanjut({label, mob})     DATA (NaN/undefined/null/[object…] kelihatan), KONTRAS (WCAG: < 4.5, atau < 3 untuk
 *                               teks besar), SENTUH (telefon: sasaran ketik < 24px, WCAG 2.5.8), BUTANG (dua kawalan
 *                               bertindih), LIMPAH (unsur terkeluar dari kad tanpa bekas skrol)
 */
const semak = (label) => {
  const W = innerWidth, H = innerHeight, out = [];
  // kelegapan warna: rgb()/rgba(), dan color(srgb r g b / a) yang dipulangkan Chromium untuk color-mix()
  const alfa = c => { if (!c || c === 'transparent') return 0;
    let m = c.match(/^rgba?\(([^)]+)\)/); if (m) { const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return p.length > 3 ? p[3] : 1; }
    m = c.match(/^color\([^)]*?\/\s*([\d.]+)\s*\)$/); if (m) return +m[1]; return /^color\(/.test(c) ? 1 : 0; };
  // lapisan legap: warna latar legap, ATAU gradien yang setiap hentian warnanya legap (kaki helaian bergradien dari
  // lut sinar TIDAK dikira legap - itulah pepijat kaki helaian v171), ATAU backdrop-filter dengan latar separa legap
  const legap = c => { if (alfa(c.backgroundColor) >= 0.85) return true;
    if (/gradient/.test(c.backgroundImage)) { const w = c.backgroundImage.match(/(rgba?\([^)]*\)|color\([^)]*\))/g) || []; if (w.length && Math.min(...w.map(alfa)) >= 0.85) return true; }
    return c.backdropFilter && c.backdropFilter !== 'none' && alfa(c.backgroundColor) >= 0.6; };
  const nama = el => { const c = (el.getAttribute && el.getAttribute('class') || '').trim().split(/\s+/).slice(0, 2).join('.');
    return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const T = [];
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => n.textContent.trim() ? 1 : 2 });
  let n; while ((n = tw.nextNode())) {
    const el = n.parentElement; if (!el || el.closest('script,style,title,option,#tip,.tip,.toast')) continue;
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    for (const r of rg.getClientRects()) {
      if (r.width < 2 || r.height < 2 || r.right <= 0 || r.bottom <= 0 || r.left >= W || r.top >= H) continue;
      T.push({ el, r, t: n.textContent.trim().slice(0, 30) });
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
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) {
    const A = T[i], B = T[j]; if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
    const x1 = Math.max(A.r.left, B.r.left), x2 = Math.min(A.r.right, B.r.right), y1 = Math.max(A.r.top, B.r.top), y2 = Math.min(A.r.bottom, B.r.bottom);
    if (x2 - x1 < 3 || y2 - y1 < 3) continue;
    const st = document.elementsFromPoint((x1 + x2) / 2, (y1 + y2) / 2);
    const ia = st.findIndex(e => e === A.el || A.el.contains(e)), ib = st.findIndex(e => e === B.el || B.el.contains(e));
    if (ia < 0 || ib < 0) continue;
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

const semakLanjut = ({ label, mob }) => {
  const W = innerWidth, H = innerHeight, out = [];
  const nama = el => { const c = (el.getAttribute && el.getAttribute('class') || '').trim().split(/\s+/).slice(0, 2).join('.');
    return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const dlmSkrin = r => r.width > 0 && r.height > 0 && r.right > 0 && r.bottom > 0 && r.left < W && r.top < H;
  const kena = (el, r) => { const x = Math.min(W - 1, Math.max(0, r.left + r.width / 2)), y = Math.min(H - 1, Math.max(0, r.top + r.height / 2));
    const t = document.elementFromPoint(x, y); return t && (t === el || el.contains(t) || t.contains(el)); };
  // warna -> [r, g, b, a] (0-255, a 0-1); rgb()/rgba() dan color(srgb …) (color-mix dalam Chromium)
  const warna = c => { if (!c || c === 'transparent' || c === 'none') return null;
    let m = c.match(/^rgba?\(([^)]+)\)/); if (m) { const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; }
    m = c.match(/^color\(srgb\s+([-\d.e]+)\s+([-\d.e]+)\s+([-\d.e]+)(?:\s*\/\s*([\d.]+))?\)/); if (m) return [m[1] * 255, m[2] * 255, m[3] * 255, m[4] != null ? +m[4] : 1];
    return null; };
  const campur = (a, b) => [a[0] * a[3] + b[0] * (1 - a[3]), a[1] * a[3] + b[1] * (1 - a[3]), a[2] * a[3] + b[2] * (1 - a[3]), 1];
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const latar = el => { const lap = [];
    for (let a = el; a && a.nodeType === 1; a = a.parentElement) { const cs = getComputedStyle(a); let bg = warna(cs.backgroundColor);
      if ((!bg || bg[3] === 0) && /gradient/.test(cs.backgroundImage)) {   // gradien: purata hentian warna
        const w = (cs.backgroundImage.match(/(rgba?\([^)]*\)|color\([^)]*\))/g) || []).map(warna).filter(Boolean);
        if (w.length) bg = [0, 1, 2, 3].map(i => w.reduce((s, x) => s + x[i], 0) / w.length); }
      if (bg && bg[3] > 0) { lap.push(bg); if (bg[3] >= 0.99) break; } }
    let c = [21, 24, 29, 1]; for (let i = lap.length - 1; i >= 0; i--) c = campur(lap[i], c); return c; };
  // teks: DATA dan KONTRAS
  const dilihat = new Set();
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => n.textContent.trim() ? 1 : 2 });
  let n; while ((n = tw.nextNode())) {
    const el = n.parentElement; if (!el || el.closest('script,style,title,option,#tip,.tip,.toast,[hidden]')) continue;
    const rg = document.createRange(); rg.selectNodeContents(n); const r = rg.getBoundingClientRect();
    if (!dlmSkrin(r)) continue;
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const t = n.textContent.trim();
    if (/(^|[^A-Za-z])(undefined|NaN|null|Infinity)([^A-Za-z]|$)|\[object |\$\{/.test(t)) out.push({ jenis: 'DATA', a: nama(el) + ' "' + t.slice(0, 40) + '"', b: '', label });
    if (dilihat.has(el) || !kena(el, r)) continue; dilihat.add(el);
    if (el.closest('[disabled],[aria-disabled="true"]')) continue;
    const svg = el instanceof SVGElement;
    let fg = warna(svg ? cs.fill : cs.color); if (!fg) continue;
    let op = 1; for (let a = el; a && a.nodeType === 1; a = a.parentElement) op *= +getComputedStyle(a).opacity;
    fg = [fg[0], fg[1], fg[2], fg[3] * op * (svg && cs.fillOpacity ? +cs.fillOpacity : 1)];
    const bg = latar(el), f2 = campur(fg, bg), L1 = lum(f2), L2 = lum(bg), nisbah = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const px = parseFloat(cs.fontSize), besar = px >= 24 || (px >= 18.66 && +cs.fontWeight >= 700), had = besar ? 3 : 4.5;
    if (nisbah < had) out.push({ jenis: 'KONTRAS', a: nama(el) + ' "' + t.slice(0, 26) + '"', b: nisbah.toFixed(2) + ' < ' + had + ' (' + px.toFixed(1) + 'px)', label });
  }
  // kawalan: SENTUH (telefon) dan BUTANG bertindih
  const K = [...document.querySelectorAll('button,a[href],select,input,summary,[role=button],[role=tab],[data-tab],[data-pos],[data-kd],[data-wl]')]
    .filter(el => !(el instanceof SVGElement) && !el.closest('svg,[hidden],.tip'))
    .map(el => ({ el, r: el.getBoundingClientRect(), cs: getComputedStyle(el) }))
    .filter(k => dlmSkrin(k.r) && k.cs.visibility !== 'hidden' && k.cs.display !== 'none' && +k.cs.opacity > 0 && kena(k.el, k.r));
  if (mob) for (const k of K) {
    if (k.el.tagName === 'A' && k.cs.display === 'inline') continue;      // pautan dalam ayat dikecualikan (WCAG 2.5.8)
    if (k.el.matches('tr,td')) continue;
    if (k.r.width < 24 || k.r.height < 24) out.push({ jenis: 'SENTUH', a: nama(k.el) + ' "' + (k.el.textContent || '').trim().slice(0, 20) + '"', b: Math.round(k.r.width) + '×' + Math.round(k.r.height) + 'px', label });
  }
  for (let i = 0; i < K.length; i++) for (let j = i + 1; j < K.length; j++) {
    const A = K[i], B = K[j]; if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
    const x1 = Math.max(A.r.left, B.r.left), x2 = Math.min(A.r.right, B.r.right), y1 = Math.max(A.r.top, B.r.top), y2 = Math.min(A.r.bottom, B.r.bottom);
    if (x2 - x1 < 4 || y2 - y1 < 4) continue;
    out.push({ jenis: 'BUTANG', a: nama(A.el) + ' "' + (A.el.textContent || '').trim().slice(0, 18) + '"', b: nama(B.el) + ' "' + (B.el.textContent || '').trim().slice(0, 18) + '"', label });
  }
  // LIMPAH: unsur terkeluar dari sisi kad (tanpa bekas skrol/klip di antara); laporkan unsur paling luar sahaja
  for (const kad of document.querySelectorAll('.panel,.v5c,.k5,.kpi,.j30,.kputus,.strip,.kadk,.v5lagi')) {
    const kr = kad.getBoundingClientRect(); if (!dlmSkrin(kr) || getComputedStyle(kad).display === 'none') continue;
    const jalan = (el) => { for (const c of el.children) {
      const cs = getComputedStyle(c); if (cs.display === 'none' || cs.position === 'fixed') continue;
      const r = c.getBoundingClientRect();
      if (r.width > 0 && r.height > 0 && (r.right > kr.right + 1 || r.left < kr.left - 1)) {
        out.push({ jenis: 'LIMPAH', a: nama(c) + ' ' + Math.round(r.left - kr.left) + '…' + Math.round(r.right - kr.right) + 'px', b: 'kad ' + nama(kad), label }); continue; }
      if (/(auto|scroll|hidden|clip)/.test(cs.overflowX)) continue;
      jalan(c); } };
    jalan(kad);
  }
  return out;
};

module.exports = { semak, semakLanjut };
