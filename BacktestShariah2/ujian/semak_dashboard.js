// Semakan render dashboard di luar talian (28 Okt 2026): memuatkan dashboard_v2.html sebenar dalam Chromium dengan
// stub `window.claude.use('db')` yang membaca dokumen jana_db daripada cakera, kemudian mengaudit SEMUA tab:
//   bertindih   kandungan melepasi tepi sel
//   tajuk       jajaran tajuk lajur tidak sama dengan jajaran selnya
//   valign      jajaran menegak bercampur dalam baris yang sama
//   kosong      lajur yang kandungannya < 45% lebar lajur (ruang terlebih)
//   sempit      jurang antara kandungan dua lajur bersebelahan < 6px (terlalu rapat)
//   tepi        kandungan kurang 2px daripada tepi sel
//   sbn         lajur disembunyi kerana tidak muat
//   keluar      jadual lebih lebar daripada bekasnya
//   tinggi      [min, maks] tinggi baris (jurang besar = baris tidak seragam)
//
// Guna:
//   python3 BacktestShariah2/standard/jana_db.py --keluar /tmp/db
//   node BacktestShariah2/ujian/semak_dashboard.js /tmp/db [lebar ...]
// Kod keluar 1 jika ada kegagalan (bertindih, tajuk, keluar, tepi).
const fs=require('fs'),path=require('path'),os=require('os');
const {chromium}=require('playwright');
const DB=process.argv[2];
if(!DB){console.error('guna: node semak_dashboard.js <folder db jana_db> [lebar ...]');process.exit(2);}
const LEBAR=process.argv.slice(3).map(Number).filter(Boolean);
const HTML=path.join(path.dirname(__dirname),'standard','dashboard_v2.html');
const S=fs.mkdtempSync(path.join(os.tmpdir(),'dash-'));
fs.writeFileSync(path.join(S,'live.html'),'<!doctype html><html><head><meta charset=utf8></head><body>'+fs.readFileSync(HTML,'utf8')+'</body></html>');
const idx={};
for(const b of fs.readdirSync(DB).filter(f=>/^batch_\d+\.json$/.test(f)))
  for(const op of JSON.parse(fs.readFileSync(path.join(DB,b),'utf8')))(idx[op.collection]=idx[op.collection]||[]).push(op.doc_id);
const D={};
for(const [c,ids] of Object.entries(idx))for(const id of ids){
  const q=path.join(DB,c,id+'.json');if(fs.existsSync(q))D[c+'/'+id]=JSON.parse(fs.readFileSync(q,'utf8'));}

const AUDIT=()=>{
  const keluar=[];
  document.querySelectorAll('section.view:not([hidden]) .tablewrap').forEach(w=>{
    const t=w.querySelector(':scope>table');if(!t||!t.tHead||!t.offsetParent)return;
    const ths=[...t.tHead.rows[0].cells],nm=i=>(ths[i].textContent||'').replace(/[↕↓↑]/g,'').trim()||'#'+i;
    const rows=[...t.tBodies[0].rows].filter(r=>r.cells.length===ths.length&&r.offsetHeight);
    if(!rows.length)return;
    const o={id:t.dataset.st||'?',bertindih:[],tajuk:[],valign:[],kosong:[],sempit:[],tepi:[]};
    const lebarKol=ths.map(th=>th.getBoundingClientRect().width);
    const isiMaks=ths.map(()=>0),isiKiri=ths.map(()=>Infinity),isiKanan=ths.map(()=>-Infinity);
    ths.forEach((th,i)=>{const td=rows[0].cells[i];if(!td||!td.offsetWidth)return;
      const a=getComputedStyle(th).textAlign,c=getComputedStyle(td).textAlign;
      if(a!==c&&th.offsetWidth)o.tajuk.push(nm(i)+' '+a+'/'+c);});
    const va=new Set(rows[0].cells.length?[...rows[0].cells].filter(td=>td.offsetWidth).map(td=>getComputedStyle(td).verticalAlign):[]);
    if(va.size>1)o.valign.push([...va].join('/'));
    rows.slice(0,25).forEach(tr=>[...tr.cells].forEach((td,ci)=>{
      const tb=td.getBoundingClientRect();if(!tb.width)return;
      const anak=[...td.querySelectorAll('*')].filter(e=>e.offsetWidth&&getComputedStyle(e).position!=='absolute');
      let kiri=Infinity,kanan=-Infinity;
      anak.forEach(e=>{const eb=e.getBoundingClientRect();if(!eb.width)return;
        if(eb.right>tb.right+1.5)o.bertindih.push(nm(ci)+' +'+Math.round(eb.right-tb.right)+'px');
        kiri=Math.min(kiri,eb.left);kanan=Math.max(kanan,eb.right);});
      if(!anak.length&&td.textContent.trim()){kiri=tb.left+parseFloat(getComputedStyle(td).paddingLeft);kanan=tb.right-parseFloat(getComputedStyle(td).paddingRight);}
      if(kanan>-Infinity){isiMaks[ci]=Math.max(isiMaks[ci],kanan-kiri);isiKiri[ci]=Math.min(isiKiri[ci],kiri);isiKanan[ci]=Math.max(isiKanan[ci],kanan);
        if(kiri<tb.left+1.5||kanan>tb.right-1.5)o.tepi.push(nm(ci));}
    }));
    ths.forEach((th,i)=>{if(!lebarKol[i]||!isiMaks[i])return;
      if(lebarKol[i]>90&&isiMaks[i]/lebarKol[i]<0.45)o.kosong.push(nm(i)+' '+Math.round(100*isiMaks[i]/lebarKol[i])+'% drp '+Math.round(lebarKol[i])+'px');
      if(i<ths.length-1&&isiKanan[i]>-Infinity&&isiKiri[i+1]<Infinity){const j=isiKiri[i+1]-isiKanan[i];
        if(j<6)o.sempit.push(nm(i)+'→'+nm(i+1)+' '+Math.round(j)+'px');}});
    const hh=rows.map(r=>r.offsetHeight);
    o.sbn=[...t.querySelectorAll('th.sbn span')].map(x=>x.textContent.trim());
    o.keluar=t.offsetWidth>w.clientWidth+1;o.tinggi=[Math.min(...hh),Math.max(...hh)];o.baris=hh.length;o.lajur=ths.length;
    ['bertindih','tajuk','valign','kosong','sempit','tepi'].forEach(k=>o[k]=[...new Set(o[k])]);
    keluar.push(o);});
  return keluar;};

let gagal=0;
(async()=>{
  const b=await chromium.launch({args:['--no-sandbox']});
  for(const lebar of (LEBAR.length?LEBAR:[1900,1600])){
    const p=await b.newPage({viewport:{width:lebar,height:1200},deviceScaleFactor:1});
    await p.addInitScript(()=>{try{localStorage.setItem('pbs3_padat','1');}catch(e){}});
    await p.addInitScript(docs=>{window.__D=docs;window.claude={use:async function(){return {
      collection:function(c){return {limit:function(){return {onSnapshot:function(cb){
        var ds=Object.keys(window.__D).filter(function(k){return k.indexOf(c+'/')===0;}).map(function(k){
          return {id:k.slice(c.length+1),exists:true,data:function(){return window.__D[k];}};});
        cb({docs:ds});return function(){};}};}};},
      doc:function(q){return {onSnapshot:function(cb){cb({exists:!!window.__D[q],data:function(){return window.__D[q];}});return function(){};}};}};}};},D);
    await p.goto('file://'+S+'/live.html');await p.waitForTimeout(2500);
    const tabs=await p.$$eval('#mainTabs button',bs=>bs.map(b=>b.dataset.tab));
    for(const tab of tabs){
      const btn=await p.$(`#mainTabs button[data-tab="${tab}"]`);if(!btn)continue;
      await btn.click();await p.waitForTimeout(1200);
      const pand=await p.$$('[data-pand] button, [data-lajur] button');
      const sub=await p.$$('.pnav-in button');
      const kump=[...(sub.length?sub:[null])];
      for(const s of kump){
        if(s){try{await s.click();await p.waitForTimeout(700);}catch(e){continue;}}
        const nama=s?await s.evaluate(e=>e.textContent.trim().slice(0,22)):'';
        const hasil=await p.evaluate(AUDIT);
        hasil.forEach(h=>{
          const berat=h.bertindih.length||h.tajuk.length||h.keluar||h.tepi.length;
          if(berat)gagal++;
          const ringan=h.kosong.length||h.sempit.length||h.valign.length||(h.tinggi[1]-h.tinggi[0]>30);
          if(berat||ringan)console.log((berat?'GAGAL':'nota ')+' '+lebar+'px '+tab+(nama?'/'+nama:'')+' ['+h.id+'] '+
            JSON.stringify({bertindih:h.bertindih,tajuk:h.tajuk,tepi:h.tepi,keluar:h.keluar,valign:h.valign,
              kosong:h.kosong.slice(0,4),sempit:h.sempit.slice(0,4),tinggi:h.tinggi,sbn:h.sbn}));});
      }
      if(tab==='posisi')for(const v of ['ringkas','risiko','gred']){
        const vb=await p.$(`[data-pand] button[data-v="${v}"]`);if(!vb)continue;await vb.click();await p.waitForTimeout(800);
        const hasil=await p.evaluate(AUDIT);
        hasil.forEach(h=>{const berat=h.bertindih.length||h.tajuk.length||h.keluar||h.tepi.length;if(berat)gagal++;
          const ringan=h.kosong.length||h.sempit.length||h.valign.length||(h.tinggi[1]-h.tinggi[0]>30);
          if(berat||ringan)console.log((berat?'GAGAL':'nota ')+' '+lebar+'px posisi/'+v+' ['+h.id+'] '+
            JSON.stringify({bertindih:h.bertindih,tajuk:h.tajuk,tepi:h.tepi,keluar:h.keluar,valign:h.valign,
              kosong:h.kosong.slice(0,4),sempit:h.sempit.slice(0,4),tinggi:h.tinggi,sbn:h.sbn}));});
      }
    }
    await p.close();
  }
  await b.close();fs.rmSync(S,{recursive:true,force:true});
  console.log(gagal?('RINGKASAN: '+gagal+' kegagalan berat'):'RINGKASAN: tiada kegagalan berat');
  process.exit(gagal?1:0);})();
