import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
a=s.index('function plusSheet(){'); b=s.index('function closePlus(after){')
s=s[:a]+r'''function plusRows(){ const nt=MYTIX().length, on=!!ME.looking;
  return `<button class="pfr p2" data-act="lookon" role="switch" aria-checked="${on}"><i class="pfe">🙋</i><span class="pft"><b>Find a plus one</b><small>${on?'Crews for your shows can invite you':'Let crews invite you to their show'}</small></span><span class="tgl pfsw" aria-hidden="true"><i></i></span></button>
    <button class="pfr p1" data-act="sellstart"><i class="pfe">🎟️</i><span class="pft"><b>List a spare</b><small>${nt} ${nt===1?'ticket':'tickets'} you can list · face value</small></span>${ic('right',16)}</button>
    <button class="pfr p0 pri" data-act="ncopen"><i class="pfe">🤝</i><span class="pft"><b>Start a crew</b><small>Pick any show · 4–8 people</small></span>${ic('right',16)}</button>`; }
function plusSheet(){ return `<div class="pfbg" data-act="plusclose"></div><div class="pfan" id="psheet" role="dialog" aria-label="Create"><p class="pfh">What are you up to?</p><div class="pfst">${plusRows()}</div></div>`; }
function plusAim(){ const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); if(!pb) return; const r=pb.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
  document.querySelectorAll('#psheet .pfr').forEach(c=>{ const prev=c.style.animation; c.style.animation='none'; const q=c.getBoundingClientRect(); c.style.animation=prev; c.style.setProperty('--fx',(cx-(q.left+q.width/2))+'px'); c.style.setProperty('--fy',(cy-(q.top+q.height/2))+'px'); });
  const st=document.querySelector('#psheet .pfst'); if(st&&!st._sw){ st._sw=1; let y0=null; st.addEventListener('touchstart',e=>{ y0=e.touches[0].clientY; },{passive:true}); st.addEventListener('touchmove',e=>{ if(y0!=null&&e.touches[0].clientY-y0>0) st.style.transform=`translateY(${(e.touches[0].clientY-y0)*.6}px)`; },{passive:true}); st.addEventListener('touchend',e=>{ const d=(e.changedTouches[0].clientY-(y0||0)); y0=null; if(d>60) closePlus(); else { st.style.transition='transform .25s'; st.style.transform=''; setTimeout(()=>st.style.transition='',260); } }); } }
'''+s[b:]
# remove old plusAim (second definition) if duplicated
first=s.index('function plusAim(){'); second=s.find('function plusAim(){',first+10)
if second>0:
    end=s.index('\n',s.index('}); }',second))+1; s=s[:second]+s[end:]
rep("else if(a==='lookon'){ ME.looking=!ME.looking; closePlus(); if(state.screen==='show') render();",
    "else if(a==='lookon'){ ME.looking=!ME.looking; const st=document.querySelector('#psheet .pfst'); if(st){ st.innerHTML=plusRows(); st.classList.add('still'); } if(state.screen==='show'){ const sc=document.querySelector('.scroll'),y=sc&&sc.scrollTop; state.psheet=false; render(); state.psheet=true; const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; if(!document.getElementById('psheet')){ document.getElementById('view').insertAdjacentHTML('beforeend',plusSheet()); document.querySelector('#psheet').classList.add('still'); } }")
rep("document.getElementById('app').addEventListener('keydown',e=>{","document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&state.psheet) closePlus(); });\ndocument.getElementById('app').addEventListener('keydown',e=>{")
CSS=r'''
/* ---- ＋ menu v3: vertical deck from the + button */
.pfan{left:16px;right:16px;bottom:calc(84px + var(--sb));height:auto;top:auto;display:flex;flex-direction:column;gap:12px;pointer-events:none}
.pfan .pfh{position:static;font-size:24px;animation:sin .4s cubic-bezier(.2,.8,.2,1) .06s both;margin:0 0 2px}
.pfst{display:flex;flex-direction:column;gap:8px;pointer-events:auto}
.pfr{display:flex;align-items:center;gap:12px;height:72px;padding:0 16px 0 12px;border-radius:var(--r-lg);background:#fff;color:var(--text);text-align:left;box-shadow:0 14px 34px rgba(0,0,0,.14),inset 0 0 0 1px rgba(0,0,0,.04);
  transform-origin:100% 100%;animation:pfr .52s cubic-bezier(.34,1.4,.5,1) both;transition:transform .16s cubic-bezier(.2,.8,.2,1)}
.pfr.p0{animation-delay:0s}.pfr.p1{animation-delay:.05s}.pfr.p2{animation-delay:.1s}
.pfr:active{transform:scale(.97)}
.pfr.pri{background:#0B0B0C;color:#fff}
.pfr .pfe{width:44px;height:44px;flex-shrink:0;font-size:22px}
.pfr.pri .pfe{background:rgba(255,255,255,.14)}
.pft{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.pft b{font-family:var(--display);font-size:17px;font-weight:700;letter-spacing:-.03em}.pft small{font-size:13px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pfr.pri small{color:rgba(255,255,255,.65)}.pfr>svg{color:var(--dim);flex-shrink:0}.pfr.pri>svg{color:#fff}
.pfr[aria-checked=true] .pfsw{background:#0B0B0C}.pfr[aria-checked=true] .pfsw i{transform:translateX(18px)}
@keyframes pfr{0%{opacity:0;transform:translate(var(--fx,120px),var(--fy,60px)) scale(.2)}40%{opacity:1}100%{opacity:1;transform:none}}
.pfan.out .pfh{animation:fadeout .18s ease forwards}
.pfan.out .pfr{animation:pfrout .24s cubic-bezier(.5,0,.75,0) forwards}
.pfan.out .pfr.p2{animation-delay:0s}.pfan.out .pfr.p1{animation-delay:.03s}.pfan.out .pfr.p0{animation-delay:.06s}
@keyframes pfrout{to{opacity:0;transform:translate(var(--fx,120px),var(--fy,60px)) scale(.2)}}
.still .pfr,.pfst.still .pfr,.still .pfh{animation:none}
@media (prefers-reduced-motion:reduce){.pfr,.pfan .pfh{animation:none!important}}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok', s.count('function plusAim(){'))
