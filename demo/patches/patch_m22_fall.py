import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
JS=r'''
// free-fall entrance: gravity + bouncy landing + rotation settling
function shDrop(){ const L=[...document.querySelectorAll('#psheet .pk.sh')]; if(!L.length) return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){ L.forEach(c=>c.classList.add('dealt')); return; }
  const order=['sc','sq','st'], G=4200, REST=.36;
  const bodies=order.map((k,i)=>{ const c=L.find(x=>x.classList.contains(k)); if(!c) return null; const r=c.getBoundingClientRect(), tgt=parseFloat(getComputedStyle(c).getPropertyValue('--r'))||0;
    const spin=(i%2?1:-1)*(28+Math.random()*30);
    return {c,y:-(r.bottom+60+Math.random()*80),vy:0,rot:tgt+spin,tgt,delay:i*110,t:0,done:false,sq:0}; }).filter(Boolean);
  bodies.forEach(b=>{ b.c.style.transform=`translateY(${b.y}px) rotate(${b.rot}deg)`; b.c.style.visibility='visible'; });
  let last=performance.now(); const t0=last;
  function step(now){ const dt=Math.min(.034,(now-last)/1000); last=now; let alive=false;
    bodies.forEach(b=>{ if(b.done) return; alive=true; if(now-t0<b.delay) return;
      b.vy+=G*dt; b.y+=b.vy*dt;
      if(b.y>=0){ b.y=0; if(b.vy>180){ b.sq=Math.min(.16,b.vy/9000); b.vy=-b.vy*REST; } else { b.vy=0; b.done=true; } }
      b.rot+=(b.tgt-b.rot)*Math.min(1,dt*(b.y===0?14:3.2)); b.sq*=.82;
      const sx=1+b.sq, sy=1-b.sq;
      b.c.style.transform=b.done?'':`translateY(${b.y}px) rotate(${b.rot}deg) scale(${sx},${sy})`;
      if(b.done) b.c.classList.add('dealt'); });
    if(alive) requestAnimationFrame(step); }
  requestAnimationFrame(step); }
function shFallOut(){ const L=[...document.querySelectorAll('#psheet .pk.sh')]; L.forEach((c,i)=>{ const r=c.getBoundingClientRect(), dy=innerHeight-r.top+60, tg=parseFloat(getComputedStyle(c).getPropertyValue('--r'))||0;
  c.classList.remove('dealt','hot'); c.style.transition=`transform .5s cubic-bezier(.55,0,.9,.5) ${i*40}ms`; c.style.transform=`translateY(${dy}px) rotate(${tg+(i%2?40:-40)}deg)`; }); }
'''
i=s.index('function plusOpen(){'); s=s[:i]+JS.lstrip()+s[i:]
rep("v.insertAdjacentHTML('beforeend',plusSheet()); plusAim(); const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.add('open","v.insertAdjacentHTML('beforeend',plusSheet()); plusAim(); shDrop(); const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.add('open")
rep("  if(!f){ after&&after(); return; } f.classList.add('out'); bg&&bg.classList.add('out'); setTimeout(()=>{ f.remove(); bg&&bg.remove(); after&&after(); },280); }",
    "  if(!f){ after&&after(); return; } const fall=f.classList.contains('pfan4')&&!f.classList.contains('pick'); if(fall) shFallOut(); f.classList.add('out'); bg&&bg.classList.add('out'); setTimeout(()=>{ f.remove(); bg&&bg.remove(); after&&after(); },fall?520:280); }")
i=s.rindex('</style>'); s=s[:i]+"""
/* free-fall: JS drives transforms, so no keyframe entrance for shapes */
.pk.sh{animation:none;visibility:hidden;transition:transform .45s cubic-bezier(.34,1.56,.5,1)}
.pk.sh.dealt{visibility:visible;animation:shfloat 6s ease-in-out infinite}
.pk.sh.hot{animation:none}
.pfan4.out .pk.sh{animation:none}
.pfbg.out{animation:fadeout .45s ease .1s both}
"""+s[i:]
open(P,'w',encoding='utf-8').write(s); print('ok')
