import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
MONF=['January','February','March','April','May','June','July','August','September','October','November','December']
# ---- month separators + live count bump
rep('function feedRow(s){ const sp=sparesFor(s).filter(x=>!(state.claimedIds||{})[x.id]).length, n=6+h(s.id)%60,',
    'function feedRow(s){ const sp=sparesFor(s).filter(x=>!(state.claimedIds||{})[x.id]).length, n=6+h(s.id)%60+(state.rf||0)*(1+Math.abs(h(s.id))%3),')
rep('return `<button class="urow" data-act="show" data-id="${s.id}">','return `<button class="urow" data-act="show" data-id="${s.id}" data-m="${d.getUTCMonth()}">')
rep("function upTail(feed){", r"""const MONF=['January','February','March','April','May','June','July','August','September','October','November','December'];
function upRows(arr,prevM,anim,d0){ let out='', pm=prevM, k=0; arr.forEach(x=>{ const m=new Date(x.dates[0]+'T12:00:00Z').getUTCMonth(), st=anim?` style="animation-delay:${(d0||0)+(k++)*50}ms"`:'';
    if(pm!=null&&m!==pm) out+=`<p class="umon${anim?' uin':''}"${st}>${MONF[m]}</p>`; pm=m;
    let r=feedRow(x); if(anim) r=r.replace('class="urow"',`class="urow uin"${st}`); out+=r; }); return out; }
function upTail(feed){""")
rep("feed.slice(0,state.upN).map((x,i)=>state._ufAnim?feedRow(x).replace('class=\"urow\"',`class=\"urow uin\" style=\"animation-delay:${i*45}ms\"`):feedRow(x)).join('')+upTail(feed)",
    "upRows(feed.slice(0,state.upN),null,state._ufAnim,0)+upTail(feed)")
rep("s2.insertAdjacentHTML('beforebegin',feed.slice(n0,n1).map((x,i)=>feedRow(x).replace('class=\"urow\"',`class=\"urow uin\" style=\"animation-delay:${i*55}ms\"`)).join(''));",
    "const last=[...document.querySelectorAll('.ulist .urow')].pop(); s2.insertAdjacentHTML('beforebegin',upRows(feed.slice(n0,n1),last?+last.dataset.m:null,true,0));")

# ---- shared element: row thumb -> show hero
JS=r'''
const RM=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
function flyBox(src,from,to,rf,rt,done){ const c=document.createElement('div'); c.className='flyc flys'; c.innerHTML=`<img alt="" src="${src}">`; document.body.appendChild(c);
  const A=(r,rad)=>({left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',borderRadius:rad+'px'});
  Object.assign(c.style,A(to,rt)); const an=c.animate([A(from,rf),A(to,rt)],{duration:540,easing:'cubic-bezier(.2,.8,.2,1)',fill:'backwards'}); an.onfinish=()=>{ c.remove(); done&&done(); }; }
function showFly(row,id){ const th=row.querySelector('.uthumb'), im=th&&th.querySelector('img'); if(!im||RM()){ go('show',id); return; }
  const from=th.getBoundingClientRect(), sc=document.getElementById('sc'); state.homeScroll=[sc?sc.scrollTop:0,0];
  state.history.push([state.screen,state.id]); state.screen='show'; state.id=id; state.showFly=id; render(false);
  const hero=document.querySelector('.hero'), hi=hero&&hero.querySelector('img'); if(!hi) return;
  const v=document.getElementById('view'); v.classList.add('shEnter'); hi.style.visibility='hidden';
  flyBox(im.src,from,hero.getBoundingClientRect(),14,32,()=>{ hi.style.visibility=''; });
  setTimeout(()=>v.classList.remove('shEnter'),900); }
function showBack(){ const id=state.id, hero=document.querySelector('.hero'), hi=hero&&hero.querySelector('img'), sc0=document.querySelector('.scroll');
  const from=hero&&hero.getBoundingClientRect(), src=hi&&hi.src, heroVis=from&&from.bottom>60;
  const p=state.history.pop()||['home',null]; state.screen=p[0]; state.id=p[1]; render(false);
  const sc=document.getElementById('sc'); if(sc&&state.homeScroll) sc.scrollTop=state.homeScroll[0];
  const row=document.querySelector(`.urow[data-id="${id}"]`), th=row&&row.querySelector('.uthumb'), ti=th&&th.querySelector('img');
  if(!ti||!heroVis||RM()) return; const to=th.getBoundingClientRect(); if(to.bottom<0||to.top>innerHeight) return;
  ti.style.visibility='hidden'; row.classList.add('uback'); flyBox(src,from,to,32,14,()=>{ ti.style.visibility=''; row.classList.remove('uback'); }); }

// ---- pull to refresh (home)
function ptrAttach(){ const sc=document.getElementById('sc'); if(!sc||sc._ptr) return; sc._ptr=1; const inner=sc.firstElementChild, ind=document.getElementById('ptr'); let y0=null, dy=0, busy=false, wheel=0, wt;
  const set=d=>{ dy=d; inner.style.transform=d?`translateY(${d}px)`:''; ind.style.opacity=Math.min(1,d/60); ind.style.transform=`translate(-50%,${Math.min(d,70)-40}px) rotate(${d*4}deg)`; ind.classList.toggle('ready',d>=64); };
  const go=()=>{ busy=true; inner.style.transition='transform .25s'; set(56); ind.classList.add('spin');
    setTimeout(()=>{ ind.classList.remove('spin','ready'); set(0); setTimeout(()=>{ inner.style.transition=''; },260); busy=false; state.rf=(state.rf||0)+1; state._ufAnim=true; const y=sc.scrollTop; render(); const n=document.getElementById('sc'); if(n) n.scrollTop=y;
      const b=document.getElementById('ptrb'); if(b){ const nn=2+state.rf%3; b.innerHTML=`${ic('check',13)} Updated · ${nn} new crews and ${nn*4+3} more people looking`; b.classList.add('on'); setTimeout(()=>b.classList.remove('on'),2600); } },950); };
  sc.addEventListener('touchstart',e=>{ if(sc.scrollTop<=0&&!busy) y0=e.touches[0].clientY; },{passive:true});
  sc.addEventListener('touchmove',e=>{ if(y0==null) return; const d=e.touches[0].clientY-y0; if(d>0){ set(Math.min(110,d*.5)); } },{passive:true});
  sc.addEventListener('touchend',()=>{ if(y0==null) return; y0=null; if(dy>=64) go(); else { inner.style.transition='transform .25s'; set(0); setTimeout(()=>inner.style.transition='',260); } });
  sc.addEventListener('wheel',e=>{ if(busy||sc.scrollTop>0||e.deltaY>=0) return; wheel+=-e.deltaY; set(Math.min(110,wheel*.35)); clearTimeout(wt); wt=setTimeout(()=>{ if(dy>=64) go(); else { inner.style.transition='transform .25s'; set(0); setTimeout(()=>inner.style.transition='',260); } wheel=0; },160); },{passive:true}); }
'''
i=s.index('function upTail(feed){'); s=s[:i]+JS.lstrip()+s[i:]
# home markup: indicator + banner
rep('''  return `<div class="scroll" id="sc"><div style="padding-bottom:110px">''','''  return `<div class="ptr" id="ptr" aria-hidden="true">${ic('shuffle',16)}</div><p class="ptrb" id="ptrb" role="status"></p><div class="scroll" id="sc"><div style="padding-bottom:110px">''')
rep("state._ufAnim=false; if(state.screen==='home') upWatch();","state._ufAnim=false; if(state.screen==='home'){ upWatch(); ptrAttach(); }")
rep("  if(a==='show') go('show',id);","  if(a==='show'){ if(t.classList.contains('urow')) showFly(t,id); else go('show',id); }")
rep("else if(a==='back'){ const top=state.history[state.history.length-1]; if(state.screen==='scene'",
    "else if(a==='back'){ const top=state.history[state.history.length-1]; if(state.screen==='show'&&state.showFly===state.id&&top&&top[0]==='home'){ state.showFly=null; showBack(); } else if(state.screen==='scene'")
CSS=r'''
.umon{margin:0;padding:14px 2px 6px;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border-top:1px solid var(--line)}
.umon+.urow{border-top:0}
.flys{box-shadow:0 12px 30px rgba(0,0,0,.18);background:#111}
.shEnter .hero .htext,.shEnter .hero .nav{animation:fadein .35s ease both .32s}
.shEnter .pad{animation:sin .45s cubic-bezier(.2,.8,.2,1) both .18s}
.uback{animation:none}
.ptr{position:absolute;left:50%;top:calc(var(--st) + 6px);z-index:8;width:34px;height:34px;border-radius:50%;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,.12);display:grid;place-items:center;opacity:0;transform:translate(-50%,-40px);pointer-events:none;color:#6B6B70}
.ptr.ready{color:#0B0B0C}.ptr.spin{animation:ptrs .7s linear infinite;opacity:1!important}
@keyframes ptrs{from{transform:translate(-50%,16px) rotate(0)}to{transform:translate(-50%,16px) rotate(360deg)}}
.ptrb{position:absolute;left:50%;top:calc(var(--st) + 8px);z-index:8;margin:0;transform:translate(-50%,-12px);opacity:0;height:32px;padding:0 14px;border-radius:16px;background:#0B0B0C;color:#fff;font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:6px;white-space:nowrap;pointer-events:none;transition:opacity .3s,transform .3s cubic-bezier(.2,.8,.2,1)}
.ptrb.on{opacity:1;transform:translate(-50%,0)}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
