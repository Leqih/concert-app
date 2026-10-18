"""Quick accessibility + performance pass over the main screens.
Per screen: DOM nodes, unlabeled buttons, text < 11px, low-contrast text (< 4.5:1, < 3:1 for >= 18.66px bold / 24px),
tap targets < 32px, images without alt. Plus page load timings."""
from playwright.sync_api import sync_playwright
import os, json
D = os.path.dirname(os.path.abspath(__file__)); html = os.path.abspath(os.path.join(D, '..', 'dist', 'plusone-demo.html'))
SC = [('home', '0'), ('explore', "go('explore')"), ('clips', "go('clips')"), ('chats', "go('crews')"), ('crew', "go('crew','t1')"),
      ('tickets', "go('tickets')"), ('show', "go('show',A('Harry Styles').id)"), ('wall', "go('wall',A('Gorillaz').id)"),
      ('scene', "go('scene','1')"), ('me', "go('me')"), ('person', "state.pid=1;go('person')"), ('search', "go('search')")]
JS = r"""() => {
 const lum=c=>{const m=c.match(/[\d.]+/g); if(!m) return null; const a=m.length>3?+m[3]:1; const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}; return {L:.2126*f(+m[0])+.7152*f(+m[1])+.0722*f(+m[2]),a}};
 const bgOf=el=>{ for(let e=el;e;e=e.parentElement){ const cs=getComputedStyle(e); if(cs.backgroundImage!=='none'&&!/gradient/.test(cs.backgroundImage)) return null; const b=lum(cs.backgroundColor); if(b&&b.a>.9) return b.L; if(/gradient/.test(cs.backgroundImage)) return null; } return 1; };
 const vis=e=>{const r=e.getBoundingClientRect(); return e.offsetParent&&r.width>0&&r.height>0&&r.bottom>0&&r.top<852};
 const out={nodes:document.querySelectorAll('*').length, unlabeled:[], small:[], contrast:[], tap:[], noalt:0};
 document.querySelectorAll('button,[data-act],a,input').forEach(b=>{ if(!vis(b)) return; const name=(b.getAttribute('aria-label')||b.innerText||b.title||b.placeholder||'').trim(); if(!name) out.unlabeled.push(b.className||b.dataset.act);
   const r=b.getBoundingClientRect(); if((r.width<32||r.height<32) && !b.closest('[data-act]:not(:scope)')) out.tap.push(`${b.dataset.act||b.tagName}:${Math.round(r.width)}x${Math.round(r.height)}`); });
 const w=document.createTreeWalker(document.getElementById('app'),NodeFilter.SHOW_TEXT); let n;
 while(n=w.nextNode()){ if(!n.textContent.trim()) continue; const el=n.parentElement; if(!vis(el)) continue; const cs=getComputedStyle(el); const fs=parseFloat(cs.fontSize);
   if(fs<11) out.small.push(`${fs}px "${n.textContent.trim().slice(0,24)}"`);
   const fg=lum(cs.color), bg=bgOf(el); if(fg&&bg!=null&&fg.a>.3){ const L1=Math.max(fg.L,bg),L2=Math.min(fg.L,bg); let r=(L1+.05)/(L2+.05); if(fg.a<1) r=1+(r-1)*fg.a; const big=fs>=24||(fs>=18.66&&+cs.fontWeight>=700); if(r<(big?3:4.5)) out.contrast.push(`${r.toFixed(1)} ${fs}px "${n.textContent.trim().slice(0,24)}"`); } }
 document.querySelectorAll('img').forEach(i=>{ if(vis(i)&&!i.hasAttribute('alt')) out.noalt++; });
 out.unlabeled=[...new Set(out.unlabeled)]; out.small=[...new Set(out.small)]; out.contrast=[...new Set(out.contrast)]; out.tap=[...new Set(out.tap)];
 return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); res = {}
    pg = b.new_page(viewport={'width': 393, 'height': 852})
    pg.route('**/*ticketm.net/**', lambda r: r.abort()); pg.route('**/fonts.g*/**', lambda r: r.abort())
    pg.goto('file://' + html); pg.wait_for_timeout(1500)
    print('timing', pg.evaluate("(()=>{const t=performance.getEntriesByType('navigation')[0]; return {dcl:Math.round(t.domContentLoadedEventEnd), load:Math.round(t.loadEventEnd), heapMB: performance.memory? Math.round(performance.memory.usedJSHeapSize/1e6):null}})()"))
    for name, js in SC:
        pg.goto('file://' + html); pg.wait_for_timeout(500)
        if js != '0': pg.evaluate(js)
        pg.wait_for_timeout(1200)
        r = pg.evaluate(JS); res[name] = r
        print(f"== {name}: nodes {r['nodes']} | unlabeled {len(r['unlabeled'])} {r['unlabeled'][:5]} | <11px {len(r['small'])} {r['small'][:4]} | lowcontrast {len(r['contrast'])} {r['contrast'][:5]} | tap<32 {len(r['tap'])} {r['tap'][:6]} | img no alt {r['noalt']}")
    b.close()
json.dump(res, open(os.path.join(D, 'a11y_perf.json'), 'w'))
