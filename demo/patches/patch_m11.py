import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:90])
    s=s.replace(old,new)
a=s.index('function explore(){'); b=s.index('\n}\n',a)+3
s=s[:a]+r'''function explore(){
  const tag=state.xtag==null?-1:state.xtag, order=[0,1,2,4,6,7,3,5], all=xCrews();
  const L=all.filter(c=>tag<0||c.j===tag);
  const solo=all.filter(c=>xDays(c.s.dates[0])<=7).reduce((n,c)=>n+c.solo,0)||23;
  const top=`<div class="xtop"><header class="xhd"><h1 class="sh1">Explore <span class="emo">🧭</span></h1><span class="wcity">${L.length} crews forming in ${state.city}</span></header>
    <div class="pad"><button class="sbar sfake" data-act="search" aria-label="Search">${ic('search',20)}<span>Artists, crews, or people</span><i class="shot">🔥 Trending</i></button></div>
    <div class="hs xchips"><button class="gch" data-act="xtag" data-v="-1" aria-pressed="${tag<0}">All</button>${order.map(j=>`<button class="gch" data-act="xtag" data-v="${j}" aria-pressed="${tag===j}">${SCENE_EMO[j]} ${SCENE_LIST[j][0]}</button>`).join('')}</div></div>`;
  const proof=`<div class="xsolo2"><span class="xav">${[3,5,7].map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}</span><span><b>${solo} people</b> are going solo this week · every crew is ID + ticket verified</span></div>`;
  const groups=XB.map(bk=>{ const cs=L.filter(c=>xBucket(c.s.dates[0])===bk); const by=[]; cs.forEach(c=>{ let g=by.find(x=>x[0].s===c.s); if(!g){ g=[]; by.push(g); } g.push(c); }); return [bk,by]; }).filter(g=>g[1].length);
  const start=`<button class="xstart" data-act="ncopen"><i>${ic('plus',18)}</i><span><b>Don’t see your vibe?</b><small>Start a crew for any show · up to 8 people</small></span>${ic('right',16)}</button>`;
  const body=groups.length?proof+groups.map(([bk,by])=>`<p class="slab">${bk}</p>${by.slice(0,5).map(xGroup).join('')}`).join('')+start
    :`<div class="xempty"><b>No ${tag>=0?esc(SCENE_LIST[tag][0].toLowerCase())+' ':''}crews yet</b><span>Be the first. We’ll suggest a meetup spot and time.</span><button data-act="ncopen" data-j="${tag>=0?tag:0}">＋ Start the first crew</button></div>`;
  return `<div class="scroll"><div class="xpg" style="padding-bottom:130px">${top}${body}</div></div>${dock('explore')}`;
}
const RECENT0=['Harry Styles','Pit crew','MSG'];
function search(){ const q=(state.sq||'').trim().toLowerCase(), rec=state.recent||RECENT0, m=t=>t.toLowerCase().includes(q);
  let body='';
  if(!q){ body=`${rec.length?`<div class="srh"><b>Recent</b><button data-act="sclear">Clear</button></div><div class="srec">${rec.map(r=>`<button class="gch" data-act="sfill" data-v="${esc(r)}">${ic('clock',13)} ${esc(r)}</button>`).join('')}</div>`:''}
    ${trendCard()}
    <div class="srh"><b>Browse by vibe</b></div><div class="svibe">${[0,1,2,4,6,7,3,5].map(j=>`<button data-act="svibe" data-v="${j}"><i>${SCENE_EMO[j]}</i><span>${SCENE_LIST[j][0]}</span></button>`).join('')}</div>`; }
  else { const S=SHOWS.filter(x=>m(x.artist+' '+x.venue)).slice(0,4), C=xCrews().filter(c=>!c.full&&m(c.name+' '+c.s.artist+' '+c.spot)).slice(0,4), Pp=PEOPLE.map((p,i)=>[p,i]).filter(([p])=>m(p[0])).slice(0,4);
    body=(S.length?`<div class="srh"><b>Shows</b></div><div class="wcard flush ssec2">${S.map(feedRow).join('')}</div>`:'')
      +(C.length?`<div class="srh"><b>Crews</b></div><div class="xgrp xgs">${C.map(c=>xRow(c).replace('<span class="xmt">',`<span class="xmt">${esc(c.s.artist)} · `)).join('')}</div>`:'')
      +(Pp.length?`<div class="srh"><b>People</b></div><div class="wcard flush ssec2">${Pp.map(([p,i])=>`<button class="spp" data-act="person" data-v="${i}"><span class="bgav"><span>${avi(p[3])}</span></span><span><b>${p[0]}</b><small>${BUD[i]?'Buddy · ':''}${REL[i][0]} of ${REL[i][1]} shows showed up</small></span>${ic('right',16)}</button>`).join('')}</div>`:'')
      ||`<div class="xempty"><b>No results for “${esc(state.sq)}”</b><span>Try an artist, a venue, or a vibe like “pit crew”.</span></div>`; }
  return `<div class="scroll"><div class="xpg" style="padding-bottom:60px"><div class="xtop shd"><div class="shrow"><label class="sbar"><span hidden>Search</span>${ic('search',20)}<input id="sq" value="${esc(state.sq||'')}" placeholder="Artists, crews, or people" autocomplete="off" data-live2="1"></label><button class="scan" data-act="back">Cancel</button></div></div>${body}</div></div>`;
}
'''+s[b:]
rep("v.innerHTML={home,show,crew,crews,me,person,explore,tickets,scene,sell}","v.innerHTML={home,show,crew,crews,me,person,explore,tickets,scene,sell,search}")
rep('<button class="wicon" data-act="explore" aria-label="Search shows">','<button class="wicon" data-act="search" aria-label="Search">')
# sticky shadow hook
rep("const xs=document.querySelector('.xstick'); if(xs){ const sc=xs.closest('.scroll'), f=()=>xs.classList.toggle('stuck',xs.getBoundingClientRect().top<=parseFloat(getComputedStyle(xs).top)+1); sc&&sc.addEventListener('scroll',f,{passive:true}); f(); }",
    "const xs=document.querySelector('.xtop'); if(xs){ const sc=xs.closest('.scroll'), f=()=>xs.classList.toggle('stuck',sc.scrollTop>2); sc&&sc.addEventListener('scroll',f,{passive:true}); f(); } if(state.screen==='search'&&!state._sqf){ const i=document.getElementById('sq'); if(i){ i.focus(); state._sqf=true; } }")
# input handler for search
rep("document.getElementById('app').addEventListener('input',e=>{ if(e.target.dataset.live){",
    "document.getElementById('app').addEventListener('input',e=>{ if(e.target.dataset.live2){ state.sq=e.target.value; const pos=e.target.selectionStart; render(); const i=document.getElementById('sq'); i.focus(); i.setSelectionRange(pos,pos); return; } if(e.target.dataset.live){")
rep("document.getElementById('app').addEventListener('keydown',e=>{ if(e.key==='Enter'&&e.target.dataset.enter){",
    "document.getElementById('app').addEventListener('keydown',e=>{ if(e.key==='Enter'&&e.target.id==='sq'){ e.preventDefault(); const v=e.target.value.trim(); if(v){ state.recent=[v].concat((state.recent||RECENT0).filter(r=>r!==v)).slice(0,5); render(); } return; } if(e.key==='Enter'&&e.target.dataset.enter){")
H=r'''  else if(a==='search'){ state.sq=''; state._sqf=false; go('search'); }
  else if(a==='sfill'){ state.sq=v; render(); const i=document.getElementById('sq'); i&&i.focus(); }
  else if(a==='sclear'){ state.recent=[]; render(); }
  else if(a==='svibe'){ state.xtag=+v; state.history=[]; state.screen='explore'; render(); }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")
CSS=r'''
.scroll>.xpg:first-child{padding-top:0}
.xtop{position:sticky;top:0;z-index:6;background:var(--bg);padding:calc(var(--st) + 2px) 0 10px;transition:box-shadow .2s}
.xtop.stuck{box-shadow:0 1px 0 var(--line)}
.xhd{display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 16px 10px}
.sfake{width:100%;height:48px;text-align:left}.sfake span{flex:1;font-size:16px;color:var(--dim);letter-spacing:-.02em}
.shot{font-style:normal;flex-shrink:0;height:26px;padding:0 10px;border-radius:13px;background:var(--card2);font-size:12px;font-weight:600;color:#3C3C40;display:inline-flex;align-items:center}
.xtop .xchips{margin-top:10px}
.shd{padding-bottom:6px}.shrow{display:flex;align-items:center;gap:10px;padding:6px 16px 0}.shrow .sbar{flex:1;height:48px}
.scan{font-size:15px;font-weight:600;color:var(--text);flex-shrink:0}
.srh{display:flex;align-items:baseline;justify-content:space-between;margin:18px 20px 8px}.srh b{font-family:var(--display);font-size:17px;letter-spacing:-.03em}.srh button{font-size:13px;color:var(--muted);font-weight:600}
.srec{display:flex;flex-wrap:wrap;gap:6px;padding:0 16px}.srec .gch{display:inline-flex;align-items:center;gap:5px}
.svibe{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:0 12px}
.svibe button{height:76px;border-radius:18px;background:var(--card);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--text)}
.svibe i{font-style:normal;font-size:22px}.svibe span{font-size:11.5px;font-weight:600;letter-spacing:-.01em}
.ssec2{margin:0 12px;padding:2px 12px}
.spp{display:flex;align-items:center;gap:12px;width:100%;padding:10px 0;text-align:left;color:var(--text)}.spp+.spp{border-top:1px solid var(--line)}
.spp .bgav span{width:40px;height:40px;border:0}.spp>span:nth-child(2){flex:1;display:flex;flex-direction:column}.spp b{font-size:15px}.spp small{font-size:12.5px;color:var(--muted)}.spp>svg{color:var(--dim)}
.xtop+.xsolo2{margin-top:10px}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
