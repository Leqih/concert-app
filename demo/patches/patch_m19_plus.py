import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
a=s.index('function plusRows(){'); b=s.index('function closePlus(after){')
s=s[:a]+r'''function plusCards(){ const nt=MYTIX().length, on=!!ME.looking;
  const tix=`<svg viewBox="0 0 104 58" class="pkart" aria-hidden="true"><path d="M8 4h88a4 4 0 0 1 4 4v14a7 7 0 0 0 0 14v14a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V36a7 7 0 0 0 0-14V8a4 4 0 0 1 4-4z" fill="#fff" stroke="#0B0B0C" stroke-width="2"/><path d="M72 8v42" stroke="#0B0B0C" stroke-width="2" stroke-dasharray="3 4"/><text x="38" y="35" text-anchor="middle" font-family="Inter Tight,Inter,sans-serif" font-weight="800" font-size="17" fill="#0B0B0C">FACE</text><text x="86" y="34" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="12" fill="#0B0B0C">$2</text></svg>`;
  const crew=`<span class="pkav">${[3,5,1].map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}<span class="pkme">${ic('plus',16)}</span></span>`;
  const radar=`<span class="pkrad"><i></i><i></i><i></i><span>${avi(MEP[3])}</span></span>`;
  const C=[['k0','sellstart','02',tix,'List a spare',`${nt} ${nt===1?'ticket':'tickets'} you can list at face value`,ic('right',14)],
           ['k1','ncopen','01',crew,'Start a crew','Pick any show · 4–8 people',ic('right',14)],
           ['k2'+(on?' on':''),'lookon','03',radar,'Find a plus one',on?'You’re visible to crews':'Let crews invite you',`<em class="pkon">${on?'ON':'OFF'}</em>`]];
  return C.map(([k,act,n,art,t,d,go])=>`<button class="pk ${k}" data-act="${act}"${act==='lookon'?` role="switch" aria-checked="${on}"`:''}><span class="pkt"><small>${n}</small>${go}</span><span class="pka">${art}</span><b>${t}</b><small class="pkd">${d}</small></button>`).join(''); }
function plusSheet(){ return `<div class="pfbg" data-act="plusclose"></div><div class="pfan pfan3" id="psheet" role="dialog" aria-label="Create"><p class="pfh">What are you up to?</p><div class="pkd3">${plusCards()}</div><p class="pfhint">Tap a card, or hold ＋ and slide</p></div>`; }
function plusAim(){ const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); if(!pb) return; const r=pb.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
  document.querySelectorAll('#psheet .pk').forEach(c=>{ const st=getComputedStyle(c), L=c.offsetLeft+c.offsetWidth/2, host=c.offsetParent.getBoundingClientRect(); const x0=host.left+L, y0=host.top+c.offsetTop+c.offsetHeight/2;
    c.style.setProperty('--fx',(cx-x0)+'px'); c.style.setProperty('--fy',(cy-y0)+'px'); c.addEventListener('animationend',()=>c.classList.add('dealt'),{once:true}); }); }
function plusOpen(){ state.psheet=true; const v=document.getElementById('view'); v.querySelectorAll('.pfbg,#psheet').forEach(x=>x.remove()); v.insertAdjacentHTML('beforeend',plusSheet()); plusAim(); const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.add('open'); }
function pkHot(x,y){ const el=document.elementFromPoint(x,y), c=el&&el.closest&&el.closest('#psheet .pk'); document.querySelectorAll('#psheet .pk.hot').forEach(k=>{ if(k!==c) k.classList.remove('hot'); }); if(c) c.classList.add('hot'); return c; }
function pkPick(c){ const f=document.getElementById('psheet'); if(!f||f.classList.contains('pick')) return; if(c.dataset.act==='lookon'){ c.dataset.go='1'; c.click(); return; }
  f.classList.add('pick'); c.classList.add('chosen'); setTimeout(()=>{ c.dataset.go='1'; c.click(); },300); }
(function(){ let drag=false, sx=0, sy=0;
  document.addEventListener('pointerdown',e=>{ const pb=e.target.closest&&e.target.closest('#navroot .bcir[data-act=plusmenu]'); if(pb&&!state.psheet){ plusOpen(); window._pfT=Date.now(); drag=true; sx=e.clientX; sy=e.clientY; } else if(e.target.closest&&e.target.closest('#psheet .pk')) pkHot(e.clientX,e.clientY); });
  document.addEventListener('pointermove',e=>{ if(state.psheet&&(drag||e.pointerType==='mouse')) pkHot(e.clientX,e.clientY); });
  document.addEventListener('pointerup',e=>{ if(!drag) return; drag=false; const c=pkHot(e.clientX,e.clientY); if(c&&Math.hypot(e.clientX-sx,e.clientY-sy)>24){ window._pfT=Date.now(); pkPick(c); } });
})();
'''+s[b:]
# old plusAim duplicates cleanup
while s.count('function plusAim(){')>1:
    second=s.index('function plusAim(){',s.index('function plusAim(){')+10); end=s.index('\n',s.index('}); }',second))+1
    # only drop the old definition that contains '.pfr' or '.pfc'
    blk=s[second:end]
    s=s[:second]+s[end:]
rep("else if(a==='plusmenu'){ if(state.psheet){ closePlus(); return; } state.psheet=true; const v=document.getElementById('view'); v.querySelectorAll('.pfbg,#psheet').forEach(x=>x.remove()); v.insertAdjacentHTML('beforeend',plusSheet()); plusAim(); const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.add('open'); }",
    "else if(a==='plusmenu'){ if(Date.now()-(window._pfT||0)<700) return; if(state.psheet){ closePlus(); return; } plusOpen(); }")
# intercept card clicks for pick animation
rep("  if(a==='show'){","  if(t.closest&&t.closest('#psheet')&&t.classList.contains('pk')&&!t.dataset.go){ pkPick(t); return; }\n  if(a==='show'){")
# lookon: update cards in place
i=s.index("else if(a==='lookon'){"); j=s.index('\n',i)
s=s[:i]+"else if(a==='lookon'){ ME.looking=!ME.looking; const d3=document.querySelector('#psheet .pkd3'); if(d3){ d3.innerHTML=plusCards(); d3.querySelectorAll('.pk').forEach(k=>k.classList.add('dealt','still')); const k2=d3.querySelector('.k2'); k2&&k2.classList.add('bump'); } else toast(ME.looking?'You’re visible · crews for your saved shows can invite you':'Hidden · crews won’t see you as looking'); }"+s[j:]
CSS=r'''
/* ---- ＋ menu v4: a hand of cards dealt from the + button */
.pfan3{left:0;right:0;bottom:calc(88px + var(--sb));height:auto;display:block;pointer-events:none}
.pfan3 .pfh{position:static;text-align:center;margin:0 0 18px;font-size:24px}
.pfhint{margin:14px 0 0;text-align:center;font-size:12px;color:var(--muted);animation:fadein .4s ease .5s both}
.pfan3.out .pfhint{animation:fadeout .15s forwards}
.pkd3{position:relative;height:214px}
.pk{position:absolute;left:50%;bottom:0;width:134px;height:196px;margin-left:-67px;padding:12px 12px 14px;border-radius:var(--r-lg);background:#fff;color:var(--text);text-align:left;display:flex;flex-direction:column;pointer-events:auto;
  box-shadow:0 18px 40px rgba(0,0,0,.16),inset 0 0 0 1px rgba(0,0,0,.05);transform-origin:50% 170%;transform:rotate(var(--r)) translateY(var(--y));
  transition:transform .42s cubic-bezier(.34,1.5,.5,1),opacity .25s,box-shadow .3s;animation:pkin .7s cubic-bezier(.3,1.35,.5,1) backwards}
.pk.k0{--r:-20deg;--y:0px;animation-delay:.08s;z-index:1}
.pk.k1{--r:0deg;--y:-16px;animation-delay:0s;z-index:3;background:#0B0B0C;color:#fff}
.pk.k2{--r:20deg;--y:0px;animation-delay:.16s;z-index:2}
.pk.dealt{animation:none}
.pk.hot,.pk:focus-visible{transform:rotate(calc(var(--r)*.7)) translateY(calc(var(--y) - 26px)) scale(1.05);z-index:5;box-shadow:0 26px 50px rgba(0,0,0,.24)}
.pk:active{transform:rotate(calc(var(--r)*.7)) translateY(calc(var(--y) - 20px)) scale(1.02)}
@keyframes pkin{0%{transform:translate(var(--fx,120px),var(--fy,120px)) rotate(calc(var(--r) + 40deg)) scale(.25);opacity:0}30%{opacity:1}100%{transform:rotate(var(--r)) translateY(var(--y));opacity:1}}
.pkt{display:flex;align-items:center;justify-content:space-between}.pkt small{font-size:11px;font-weight:700;letter-spacing:.08em;color:var(--muted)}.k1 .pkt small{color:rgba(255,255,255,.55)}
.pkt svg{width:24px;height:24px;padding:5px;box-sizing:border-box;border-radius:50%;background:var(--card2)}.k1 .pkt svg{background:#fff;color:#0B0B0C}
.pkon{font-style:normal;height:20px;padding:0 8px;border-radius:var(--r-pill);background:var(--card2);font-size:10.5px;font-weight:700;letter-spacing:.06em;display:inline-flex;align-items:center}.k2.on .pkon{background:#0B0B0C;color:#fff}
.pka{flex:1;display:grid;place-items:center}
.pk b{font-family:var(--display);font-size:18px;font-weight:700;letter-spacing:-.035em;line-height:1.05}
.pkd{font-size:12px;line-height:1.3;color:var(--muted);margin-top:4px}.k1 .pkd{color:rgba(255,255,255,.62)}
.pkart{width:96px}
.pkav{display:flex}.pkav>span{width:34px;height:34px;border-radius:50%;overflow:hidden;position:relative;border:2px solid #0B0B0C;margin-left:-10px;background:#333}.pkav>span:first-child{margin-left:0}.pkav img{width:100%;height:100%;object-fit:cover}
.pkav .pkme{display:grid;place-items:center;background:#0B0B0C;border:1.5px dashed rgba(255,255,255,.7);color:#fff}
.pkrad{position:relative;width:74px;height:74px;display:grid;place-items:center}.pkrad i{position:absolute;inset:0;border-radius:50%;border:1.5px solid #0B0B0C;opacity:.18}.pkrad i:nth-child(2){inset:12px;opacity:.3}.pkrad i:nth-child(3){inset:24px;opacity:.5}
.pkrad>span{width:26px;height:26px;border-radius:50%;overflow:hidden;position:relative;z-index:1}.pkrad img{width:100%;height:100%;object-fit:cover}
.k2.on .pkrad i{animation:rad 1.8s ease-out infinite;opacity:.5}.k2.on .pkrad i:nth-child(2){animation-delay:.6s}.k2.on .pkrad i:nth-child(3){animation-delay:1.2s}
@keyframes rad{0%{transform:scale(.35);opacity:.7}100%{transform:scale(1.15);opacity:0}}
.pk.bump{animation:bump .45s cubic-bezier(.34,1.6,.5,1)}@keyframes bump{0%{transform:rotate(var(--r)) translateY(var(--y)) scale(.94)}100%{transform:rotate(var(--r)) translateY(var(--y)) scale(1)}}
.pfan3.pick .pk{transition:transform .38s cubic-bezier(.5,0,.3,1),opacity .3s}
.pfan3.pick .pk:not(.chosen){transform:rotate(calc(var(--r)*2)) translateY(180px);opacity:0}
.pfan3.pick .pk.chosen{transform:translateY(-70px) scale(1.14);z-index:9}
.pfan3.out .pk{animation:pkout .26s cubic-bezier(.5,0,.75,0) forwards}
.pfan3.pick.out .pk{animation:none}
@keyframes pkout{to{transform:translate(var(--fx,120px),var(--fy,120px)) rotate(calc(var(--r) + 30deg)) scale(.25);opacity:0}}
@media (prefers-reduced-motion:reduce){.pk{animation:none!important;transition:none}}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok',s.count('function plusAim(){'))
