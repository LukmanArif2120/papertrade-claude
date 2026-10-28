// Semakan render dashboard di luar talian (28 Okt 2026): memuatkan dashboard_v2.html sebenar dalam Chromium
// dengan stub `window.claude.use('db')` yang membaca dokumen jana_db daripada cakera, kemudian mengaudit jadual
// Posisi: kandungan melepasi tepi sel (bertindih), jajaran tajuk lawan sel, pil lawan cip gred, bar lorong lawan
// peratus, cip ATR lawan pil, lajur disembunyi, jadual terkeluar skrin dan tinggi baris.
//
// Guna:
//   python3 BacktestShariah2/standard/jana_db.py --keluar /tmp/db
//   node BacktestShariah2/ujian/semak_dashboard.js /tmp/db [lebar ...]
// Perlukan playwright (sudah dipasang dalam sesi awan).
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const DB=process.argv[2];
if(!DB){console.error('guna: node semak_dashboard.js <folder db jana_db> [lebar ...]');process.exit(2);}
const LEBAR=process.argv.slice(3).map(Number).filter(Boolean);
const HTML=path.join(path.dirname(__dirname),'standard','dashboard_v2.html');
const S=fs.mkdtempSync(path.join(require('os').tmpdir(),'dash-'));
fs.writeFileSync(path.join(S,'live.html'),'<!doctype html><html><head><meta charset=utf8></head><body>'+fs.readFileSync(HTML,'utf8')+'</body></html>');
const idx={};for(const b of fs.readdirSync(DB).filter(f=>/^batch_\d+\.json$/.test(f)))for(const op of JSON.parse(fs.readFileSync(path.join(DB,b),'utf8')))(idx[op.collection]=idx[op.collection]||[]).push(op.doc_id);
const perlu=(c,id)=>['harian','posisi','prestasi','analisis'].includes(c)||(c==='papertrade'&&/^ringkas/.test(id));
const D={};for(const [c,ids] of Object.entries(idx))for(const id of ids){if(!perlu(c,id))continue;const q=path.join(DB,c,id+'.json');if(fs.existsSync(q))D[c+'/'+id]=JSON.parse(fs.readFileSync(q,'utf8'));}
const AUDIT=()=>{const t=document.querySelector('#v-pos table[data-st]');if(!t)return {ralat:'tiada jadual'};
 const w=t.closest('.tablewrap'),nm=i=>t.tHead.rows[0].cells[i].textContent.trim();const o={lebih:[],jajar:[],tajuk:[]};
 [...t.tHead.rows[0].cells].forEach((th,i)=>{const td=t.tBodies[0].rows[0].cells[i];if(!td||!td.offsetWidth)return;
  const a=getComputedStyle(th).textAlign,c=getComputedStyle(td).textAlign;if(a!==c)o.tajuk.push(nm(i)+' '+a+'/'+c);});
 [...t.tBodies[0].rows].forEach(tr=>[...tr.cells].forEach((td,ci)=>{const tb=td.getBoundingClientRect();if(!tb.width)return;
  [...td.querySelectorAll('*')].forEach(e=>{const eb=e.getBoundingClientRect();if(eb.width&&eb.right>tb.right+1.5)o.lebih.push(nm(ci));});
  const chip=td.querySelector(':scope>.grc>.gr'),pil=td.querySelector(':scope>.pill');
  if(chip&&pil&&Math.abs(chip.getBoundingClientRect().left-pil.getBoundingClientRect().left)>1)o.jajar.push('pil≠cip '+nm(ci));
  const bar=td.querySelector('.l2bar'),pct=td.querySelector('.lrp'),lb=td.querySelector('.lrb'),atr=td.querySelector('.l2j');
  if(bar&&pct&&Math.abs(bar.getBoundingClientRect().top-pct.getBoundingClientRect().top)>6)o.jajar.push('bar≠%');
  if(atr&&lb&&Math.abs(atr.getBoundingClientRect().top-lb.getBoundingClientRect().top)>3)o.jajar.push('ATR≠pil');}));
 const hh=[...t.tBodies[0].rows].map(r=>r.offsetHeight);
 return {lebih:[...new Set(o.lebih)],jajar:[...new Set(o.jajar)],tajuk:o.tajuk,sbn:[...t.querySelectorAll('th.sbn span')].map(x=>x.textContent),
  keluar:t.offsetWidth>w.clientWidth+1,tinggi:[Math.min(...hh),Math.max(...hh)],baris:hh.length,lajur:t.tHead.rows[0].cells.length};};
let gagal=0;
(async()=>{const b=await chromium.launch({args:['--no-sandbox']});
for(const lebar of (LEBAR.length?LEBAR:[1900,1600])){
 const p=await b.newPage({viewport:{width:lebar,height:1100},deviceScaleFactor:1.2});
 await p.addInitScript(()=>{try{localStorage.setItem('pbs3_padat','1');}catch(e){}});
 await p.addInitScript(docs=>{window.__D=docs;window.claude={use:async function(){return {collection:function(c){return {limit:function(){return {onSnapshot:function(cb){var ds=Object.keys(window.__D).filter(function(k){return k.indexOf(c+'/')===0;}).map(function(k){return {id:k.slice(c.length+1),exists:true,data:function(){return window.__D[k];}};});cb({docs:ds});return function(){};}};}};},doc:function(q){return {onSnapshot:function(cb){cb({exists:!!window.__D[q],data:function(){return window.__D[q];}});return function(){};}};}};}};},D);
 await p.goto('file://'+S+'/live.html');await p.waitForTimeout(2500);
 const t=await p.$('#mainTabs button[data-tab="posisi"]');if(t)await t.click();await p.waitForTimeout(1200);
 for(const v of ['Penuh','Ringkas','Risiko','Gred']){
  const btn=await p.$(`[data-pand] button[data-v="${v.toLowerCase()}"]`);if(btn){await btn.click();await p.waitForTimeout(900);}
  const h=await p.evaluate(AUDIT);const ok=!h.lebih.length&&!h.jajar.length&&!h.tajuk.length&&!h.keluar;
  console.log((ok?'OK  ':'GAGAL')+' '+lebar+'px '+v.padEnd(8)+JSON.stringify(h));if(!ok)gagal++;
 }
  await p.close();}
await b.close();fs.rmSync(S,{recursive:true,force:true});process.exit(gagal?1:0);})();
