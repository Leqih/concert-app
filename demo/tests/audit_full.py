"""Full design-rule audit: every screen + sheets, whole scroll height.
Rules: radii in {30,20,18,14,12} or pill/circle; titles per DESIGN.md; grayscale only; Inter / Inter Tight."""
from playwright.sync_api import sync_playwright
import json, os, sys, collections
out=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','dist','plusone-demo.html'))
C="document.querySelector('[data-act=%s]').click()"
ST=[('home',"0"),('explore',"go('explore')"),('search',"go('search')"),('search-q',"go('search');state.sq='ma';render()"),('crews',"go('crews')"),
('tickets',"go('tickets')"),('spares',"go('tickets');setTimeout(()=>document.querySelector('[data-act=tview][data-v=spares]').click(),100)"),
('me',"go('me')"),('person',"state.pid=1;go('person')"),('show',"go('show',A('Gorillaz').id)"),('show-locked',"go('show',SHOWS.find(LOCKED).id)"),('scene',"go('scene','1')"),
('crew',"go('crew','t1')"),('dm',"openThread(dmFor(4))"),('sell',"%s;setTimeout(()=>{%s},600)"%(C%'plusmenu',C%'sellstart')),
('plus',C%'plusmenu'),('city',C%'citysheet'),('filters',C%'ufopen'),('newcrew',"go('show',A('Gorillaz').id);setTimeout(()=>{%s},200)"%(C%'ncopen')),
('safety',"go('crew','t3');setTimeout(()=>{%s},200)"%(C%'safety')),('kit',"go('crews');setTimeout(()=>{%s},200)"%(C%'kitopen')),
('ticketsheet',"go('crew','t1');setTimeout(()=>{%s},200)"%(C%'claim'))]
JS=r'''(()=>{ const bad=[], T=[]; const ok=[30,20,18,14,12];
 const gray=c=>{ const m=c.match(/rgba?\(([^)]+)\)/); if(!m) return true; const [r,g,b,a]=m[1].split(',').map(parseFloat); if(a===0) return true; return Math.max(r,g,b)-Math.min(r,g,b)<=12; };
 document.querySelectorAll('#view *, #app .toast').forEach(e=>{ const c=getComputedStyle(e), r=e.getBoundingClientRect(); if(r.width<2||r.height<2||c.display==='none'||c.visibility==='hidden') return;
   const id=(e.className&&e.className.baseVal===undefined?e.className:e.tagName)+'';
   const br=parseFloat(c.borderTopLeftRadius), brs=c.borderTopLeftRadius;
   if(br>0&&!brs.includes('%')&&r.width>=40&&r.height>=36&&!(br>=Math.min(r.width,r.height)/2-1)&&!ok.includes(Math.round(br))) bad.push(['radius',Math.round(br),id,Math.round(r.width)+'x'+Math.round(r.height)]);
   if(e.children.length===0&&e.textContent.trim()){ const f=c.fontFamily.split(',')[0].replace(/"/g,''); if(!['Inter','Inter Tight','Noto Sans SC'].includes(f)&&!/emo|eb/.test(id)) bad.push(['font',f,id]); if(!gray(c.color)) bad.push(['color',c.color,id,e.textContent.trim().slice(0,20)]); }
   if(!gray(c.backgroundColor)) bad.push(['bg',c.backgroundColor,id]);
   if(c.backgroundImage.includes('gradient')&&/rgb/.test(c.backgroundImage)){ const cols=c.backgroundImage.match(/rgba?\([^)]+\)/g)||[]; if(cols.some(x=>!gray(x))) bad.push(['gradient',id]); }
   if(/^H[123]$/.test(e.tagName)||/(^| )(sub|wcity|slab|ncl|umon)( |$)/.test(id)) T.push([e.tagName.toLowerCase(),id.slice(0,20),c.fontSize,c.fontWeight,c.textAlign,Math.round(r.top+document.querySelector('#view .scroll')?.scrollTop||0),e.textContent.trim().slice(0,24)]); });
 const u={}; bad.forEach(b=>{ const k=b.join('|'); u[k]=b; }); return {bad:Object.values(u),T}; })()'''
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,js in ST:
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/*ticketm.net/**',lambda r:r.abort()); pg.route('**/fonts.g*/**',lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+out); pg.wait_for_timeout(700); pg.evaluate(js); pg.wait_for_timeout(1100)
        pg.evaluate("document.querySelectorAll('#view .scroll').forEach(s=>{s.style.overflow='visible';s.style.position='relative';s.style.height='auto'})")
        r=pg.evaluate(JS); r['err']=errs; res[n]=r; pg.close()
json.dump(res,open(sys.argv[1] if len(sys.argv)>1 else '/tmp/audit_full.json','w'),indent=1)
for n,r in res.items():
    print('=====',n,'errors' if r['err'] else '', r['err'][:1])
    for bd in r['bad']: print('  ✗',bd)
    for t in r['T']:
        if t[0] in('h1','h2','h3'): print('   ',t)
