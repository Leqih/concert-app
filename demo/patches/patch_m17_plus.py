import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
# --- plus sheet content
a=s.index('function plusSheet(){'); b=s.index('\n',s.index("</div>`; }",a))+1
s=s[:a]+r'''function plusSheet(){ const nt=MYTIX().length;
  const o=[['🤝','Start a crew','Pick any show · 4–8 people','ncopen'],['🎟️','List a spare',`${nt} ${nt===1?'ticket':'tickets'} you can list · face value`,'sellstart'],['🙋',ME.looking?'You’re visible':'Find a plus one',ME.looking?'Crews can invite you · tap to hide':'Let crews invite you to their show','lookon']];
  return `<div class="pfbg" data-act="plusclose"></div><div class="pfan" id="psheet" role="dialog" aria-label="Create"><p class="pfh">What are you up to?</p>
    ${o.map(([e,t,d,act],k)=>`<button class="pfc p${k}${act==='lookon'&&ME.looking?' on':''}" data-act="${act}"><i class="pfe">${e}</i><b>${t}</b><small>${d}</small><span class="pfgo">${ic(act==='lookon'?(ME.looking?'check':'plus'):'right',14)}</span></button>`).join('')}</div>`; }
function plusAim(){ const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); if(!pb) return; const r=pb.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
  document.querySelectorAll('#psheet .pfc').forEach(c=>{ const prev=c.style.animation; c.style.animation='none'; const q=c.getBoundingClientRect(); c.style.animation=prev; c.style.setProperty('--fx',(cx-(q.left+q.width/2))+'px'); c.style.setProperty('--fy',(cy-(q.top+q.height))+'px'); }); }
'''+s[b:]
rep("function closePlus(after){","function closePlusOld(after){")
rep("function plusAim(){",r"""function closePlus(after){ const f=document.getElementById('psheet'), bg=document.querySelector('.pfbg'), pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.remove('open'); state.psheet=false;
  if(!f){ after&&after(); return; } f.classList.add('out'); bg&&bg.classList.add('out'); setTimeout(()=>{ f.remove(); bg&&bg.remove(); after&&after(); },280); }
function plusAim(){""")
rep("else if(a==='plusmenu'){ if(state.psheet){ closePlus(); return; } state.psheet=true; render(); const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.add('open'); }",
    "else if(a==='plusmenu'){ if(state.psheet){ closePlus(); return; } state.psheet=true; const v=document.getElementById('view'); v.querySelectorAll('.pfbg,#psheet').forEach(x=>x.remove()); v.insertAdjacentHTML('beforeend',plusSheet()); plusAim(); const pb=document.querySelector('#navroot .bcir[data-act=plusmenu]'); pb&&pb.classList.add('open'); }")
# render path also aims
rep("  state._ufAnim=false; if(state.screen==='home'){","  if(state.psheet) plusAim();\n  state._ufAnim=false; if(state.screen==='home'){")
# lookon closes nicely without full render flash
rep("else if(a==='lookon'){ ME.looking=!ME.looking; state.psheet=false; render();","else if(a==='lookon'){ ME.looking=!ME.looking; closePlus(); if(state.screen==='show') render();")
# --- start-crew: show picker when opened without a show
rep("else if(a==='ncopen'){ closePlus&&document.getElementById('psheet')&&(state.psheet=false); state.nc={sid:id||(A('Harry Styles')||SHOWS[0]).id,",
    "else if(a==='ncopen'){ if(document.getElementById('psheet')) closePlus(); state.nc={sid:id||null,")
rep("function ncSheet(){ const c=state.nc, s=byId[c.sid],","function ncSheet(){ const c=state.nc; if(!c.sid) return ncPick(); const s=byId[c.sid],")
rep("function ncSheet(){",r"""function ncPick(){ const L=SHOWS.filter(x=>xDays(x.dates[0])>=0).sort((a,b)=>a.dates[0].localeCompare(b.dates[0])).slice(0,10);
  return `<div class="sheetbg" data-act="ncclose"></div><div class="sheet csheet ncs" role="dialog" aria-label="Pick a show"><div class="cgrab"><i class="grab"></i><h3>Start a crew <span class="emo">🤝</span></h3><p>Which show?</p></div>
  <div class="ncb">${L.map(x=>`<button class="itrow" data-act="ncshow" data-id="${x.id}"><span class="uthumb">${img(x)}</span><span class="ub"><b>${esc(x.artist)}</b><span class="um">${sd(x.dates[0])} · ${esc(VSH(x.venue))}</span></span>${ic('right',16)}</button>`).join('')}</div></div>`; }
function ncSheet(){""")
rep("  else if(a==='ncclose'){","  else if(a==='ncshow'){ state.nc.sid=id; render(); const sh=document.querySelector('.ncs'); if(sh) sh.style.animation='none'; }\n  else if(a==='ncclose'){")
CSS=r'''
/* ---- ＋ menu v2 */
.pfan{bottom:96px;height:290px}
.pfh{font-size:24px}
.pfc{width:116px;height:176px;margin-left:-58px;border-radius:var(--r-lg);padding:14px 12px 14px;animation-duration:.62s;animation-timing-function:cubic-bezier(.34,1.45,.5,1);transition:transform .18s cubic-bezier(.2,.8,.2,1)}
.pfc.p0{--to:translate(-122px,14px) rotate(-6deg);animation-delay:.03s}
.pfc.p1{--to:translate(0,-8px);animation-delay:.08s}
.pfc.p2{--to:translate(122px,14px) rotate(6deg);animation-delay:.13s}
.pfc b{font-size:16px}
.pfc small{font-size:12px;line-height:1.35;margin-top:5px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.pfc.on .pfgo{background:#0B0B0C;color:#fff}
.pfan .pfc:active{filter:none}
@keyframes pfin{0%{transform:translate(var(--fx,80px),var(--fy,150px)) scale(.18) rotate(0);opacity:0}35%{opacity:1}100%{transform:var(--to);opacity:1}}
@keyframes pfout{0%{transform:var(--to);opacity:1}100%{transform:translate(var(--fx,80px),var(--fy,150px)) scale(.18) rotate(0);opacity:0}}
.pfan.out .pfc{animation-duration:.26s;animation-timing-function:cubic-bezier(.5,0,.75,0)}
.pfan.out .pfc.p2{animation-delay:0s}.pfan.out .pfc.p1{animation-delay:.03s}.pfan.out .pfc.p0{animation-delay:.06s}
.pfbg{background:rgba(242,242,244,.62)}
@media (prefers-reduced-motion:reduce){.pfc{animation:none!important;transform:var(--to)}}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
