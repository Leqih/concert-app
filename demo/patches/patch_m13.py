import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
lines=s.split('\n'); i=[k for k,l in enumerate(lines) if l.startswith("  const base=SHOWS.filter(s=>!drops.includes(s)), W=state.when||'all', G=state.genre||'All';")][0]
lines[i:i+7]=["  const base=SHOWS.filter(s=>!drops.includes(s)), W=state.when||'all', F=ufState();",
"  const inW=(s,w)=>w==='all'||(w==='week'?xDays(s.dates[0])<=7:xDays(s.dates[0])<=31);",
"  const feed=base.filter(s=>inW(s,W)&&ufPass(s,F)).sort((a,b)=>a.dates[0].localeCompare(b.dates[0]));",
"  const wc=w=>base.filter(s=>inW(s,w)&&ufPass(s,F)).length, nf=ufCount(F);"]
s='\n'.join(lines)
a=s.index('<div class="ufl hs">'); b=s.index('</div>',s.index("<i class=\"udiv\"></i>",a))+6
s=s[:a]+'''<div class="ufl hs">${[['all','All'],['week','This week'],['month','This month']].map(([w,l])=>{ const n=wc(w); return `<button class="gch" data-act="when" data-v="${w}" aria-pressed="${W===w}" ${n?'':'disabled'}>${l} <em>${n}</em></button>`; }).join('')}<i class="udiv"></i><button class="gch ufbtn" data-act="ufopen" aria-pressed="${nf>0}" aria-haspopup="dialog">${ic('sliders',14)} Filters${nf?` <b>${nf}</b>`:''}</button></div>'''+s[b:]
JS=r'''
const KINDS=[['concert','🎤','Concerts','One artist, one night'],['classical','🎻','Classical & orchestra','Symphonies, opera, film scores'],['festival','🎪','Festivals & lineups','Many artists, one ticket'],['residency','🔁','Residencies','Multi-night runs']];
const ARENAS=['Madison Square Garden','Barclays Center','UBS Arena','Prudential Center','MetLife Stadium'];
const skind=s=>s.kind||(s.genre==='Classical'?'classical':s.dates.length>=4?'residency':'concert'), ssize=s=>s.size||(ARENAS.includes(s.venue)?'arena':'theatre');
function ufState(){ return state.uf||(state.uf={k:[],g:[],z:'any',sp:false}); }
function ufPass(s,F){ return (!F.k.length||F.k.includes(skind(s)))&&(!F.g.length||F.g.includes(s.genre))&&(F.z==='any'||ssize(s)===F.z)&&(!F.sp||sparesFor(s).length>0); }
const ufCount=F=>F.k.length+F.g.length+(F.z!=='any'?1:0)+(F.sp?1:0);
function ufSheet(){ const F=state.ufd, drops=DROPS(), base=SHOWS.filter(s=>!drops.includes(s)), W=state.when||'all';
  const inW=s=>W==='all'||(W==='week'?xDays(s.dates[0])<=7:xDays(s.dates[0])<=31), B=base.filter(inW);
  const cnt=(patch)=>B.filter(s=>ufPass(s,{...F,...patch})).length, tot=cnt({});
  const GL=[...new Set(base.map(s=>s.genre).filter(g=>g&&g!=='Music'))].sort((a,b)=>base.filter(s=>s.genre===b).length-base.filter(s=>s.genre===a).length);
  return `<div class="sheetbg" data-act="ufclose"></div><div class="sheet csheet ufs" id="ufsheet" role="dialog" aria-label="Filters">
  <div class="cgrab"><i class="grab"></i><h3>Filters</h3></div>
  <div class="ufb">
    <p class="ncl">Type of show</p><div class="ufk">${KINDS.map(([k,e,l,d])=>{ const on=F.k.includes(k), n=cnt({k:on?F.k:[...F.k,k].filter((x,_,a)=>x===k||a.length===1)}); const c=B.filter(s=>skind(s)===k&&ufPass(s,{...F,k:[]})).length;
      return `<button class="ufkc" data-act="ufk" data-v="${k}" aria-pressed="${on}" ${c||on?'':'disabled'}><i>${e}</i><b>${l}</b><small>${d}</small><em>${c}</em></button>`; }).join('')}</div>
    <p class="ncl">Genre</p><div class="ncv">${GL.map(g=>{ const on=F.g.includes(g), c=B.filter(s=>s.genre===g&&ufPass(s,{...F,g:[]})).length; return `<button class="gch" data-act="ufg" data-v="${esc(g)}" aria-pressed="${on}" ${c||on?'':'disabled'}>${GEMO[g]?GEMO[g]+' ':''}${esc(g.replace('Hip-Hop/Rap','Hip-Hop'))} <em>${c}</em></button>`; }).join('')}</div>
    <p class="ncl">Venue</p><div class="ncsz">${[['any','Any'],['arena','Arenas'],['theatre','Theatres & clubs']].map(([z,l])=>`<button data-act="ufz" data-v="${z}" aria-pressed="${F.z===z}">${l}</button>`).join('')}</div>
    <div class="nct" style="margin-top:8px"><span><b>Only shows with spare tickets</b><small>Face value, from verified fans</small></span><button class="tgl" role="switch" aria-checked="${F.sp}" aria-label="Only shows with spare tickets" data-act="ufsp"><i></i></button></div>
  </div>
  <div class="uff"><button class="ufx" data-act="ufreset" ${ufCount(F)?'':'disabled'}>Clear all</button><button class="cgo new" data-act="ufapply" ${tot?'':'disabled'}>${tot?`Show ${tot} ${tot===1?'show':'shows'}`:'No shows match'}</button></div></div>`; }
function ufRedraw(){ const sh=document.getElementById('ufsheet'); if(!sh) return; const b=sh.querySelector('.ufb'), y=b?b.scrollTop:0; const t=document.createElement('div'); t.innerHTML=ufSheet(); const n=t.querySelector('#ufsheet'); n.style.animation='none'; sh.replaceWith(n); const nb=n.querySelector('.ufb'); if(nb) nb.scrollTop=y; }
function ufClose(){ const sh=document.getElementById('ufsheet'), bg=sh&&sh.previousElementSibling; state.ufo=false; if(!sh) return; sh.classList.add('out'); bg&&bg.classList.add('out'); setTimeout(()=>{ sh.remove(); bg&&bg.remove(); },260); }
'''
i=s.index('function upSwap(anim){'); s=s[:i]+JS.lstrip()+s[i:]
rep("+(state.nc?ncSheet():'')","+(state.nc?ncSheet():'')+(state.ufo?ufSheet():'')")
rep("  else if(a==='genre'){ state.genre=v; state.upN=6; upSwap(true); }\n","")
rep("if(a==='when') state.when=v; else { state.when='all'; state.genre='All'; }","if(a==='when') state.when=v; else { state.when='all'; state.uf=null; }")
H=r'''  else if(a==='ufopen'){ state.ufd=JSON.parse(JSON.stringify(ufState())); state.ufo=true; document.getElementById('view').insertAdjacentHTML('beforeend',ufSheet()); }
  else if(a==='ufclose'){ ufClose(); }
  else if(a==='ufk'||a==='ufg'){ const L=state.ufd[a==='ufk'?'k':'g'], i=L.indexOf(v); if(i<0) L.push(v); else L.splice(i,1); ufRedraw(); }
  else if(a==='ufz'){ state.ufd.z=v; ufRedraw(); }
  else if(a==='ufsp'){ state.ufd.sp=!state.ufd.sp; ufRedraw(); }
  else if(a==='ufreset'){ state.ufd={k:[],g:[],z:'any',sp:false}; ufRedraw(); }
  else if(a==='ufapply'){ state.uf=state.ufd; state.upN=6; ufClose(); upSwap(true); }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")
rep("state.genre='All'; state.when='all';","state.uf=null; state.when='all';")
# icon + image fallback
rep("clock:'<circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M12 7.5V12l3 2\"/>',","clock:'<circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M12 7.5V12l3 2\"/>', sliders:'<path d=\"M4 7h10M18 7h2M4 17h4M12 17h8\"/><circle cx=\"16\" cy=\"7\" r=\"2\"/><circle cx=\"10\" cy=\"17\" r=\"2\"/>',")
rep("const img = (s,extra='') => `<img class=\"cover\" alt=\"\" decoding=\"sync\" src=\"${s.img}\" ${extra}>`;",
    "const PT=s=>esc(s.artist.replace(/[^A-Za-z0-9À-ÿ ]/g,'').split(' ').filter(Boolean).slice(0,2).map(w=>w[0]).join('').toUpperCase());\nconst IMGERR=s=>`onerror=\"this.outerHTML='<span class=&quot;cover ptile&quot;>${PT(s)}</span>'\"`;\nconst img = (s,extra='') => `<img class=\"cover\" alt=\"\" decoding=\"${s.img.startsWith('data:')?'sync':'async'}\" src=\"${s.img}\" ${s.img.startsWith('data:')?'':IMGERR(s)} ${extra}>`;")
rep('<span class="uthumb"><img class="cover" alt="" decoding="async" src="${s.img}"></span>','<span class="uthumb"><img class="cover" alt="" decoding="async" src="${s.img}" ${s.img.startsWith(\'data:\')?\'\':IMGERR(s)}></span>')
CSS=r'''
.ufbtn{display:inline-flex;align-items:center;gap:5px}.ufbtn b{min-width:18px;height:18px;padding:0 5px;border-radius:9px;background:#fff;color:#0B0B0C;font-size:11px;display:inline-grid;place-items:center}
.ufbtn[aria-pressed=false] b{background:#0B0B0C;color:#fff}
.ufs{max-height:calc(100% - 40px);display:flex;flex-direction:column}
.ufb{padding:0 16px 8px;overflow-y:auto}
.ufk{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.ufkc{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:12px;border-radius:18px;background:var(--card2);text-align:left;color:var(--text);transition:background .18s,color .18s,transform .15s}
.ufkc:active{transform:scale(.97)}.ufkc i{font-style:normal;font-size:20px;margin-bottom:4px}.ufkc b{font-size:14px;letter-spacing:-.02em;line-height:1.2}.ufkc small{font-size:11.5px;color:var(--muted)}
.ufkc em{position:absolute;top:12px;right:12px;font-style:normal;font-size:12px;color:var(--muted);font-weight:600}
.ufkc[aria-pressed=true]{background:#0B0B0C;color:#fff}.ufkc[aria-pressed=true] small,.ufkc[aria-pressed=true] em{color:rgba(255,255,255,.65)}
.ufkc:disabled,.ufb .gch:disabled{opacity:.35}
.ufb .gch em{font-style:normal;font-size:12px;color:var(--muted);margin-left:2px}.ufb .gch[aria-pressed=true] em{color:rgba(255,255,255,.7)}
.uff{display:flex;align-items:center;gap:10px;padding:12px 16px 0;border-top:1px solid var(--line)}
.uff .cgo{margin:0;flex:1;width:auto}.uff .cgo:disabled{background:var(--card2);color:var(--muted)}
.ufx{height:52px;padding:0 6px;font-size:15px;font-weight:600;color:var(--text);text-decoration:underline;text-underline-offset:3px}.ufx:disabled{color:var(--dim);text-decoration:none}
.ptile{display:grid;place-items:center;background:linear-gradient(145deg,#2A2A2E,#0B0B0C);color:#fff;font-family:var(--display);font-weight:800;letter-spacing:-.04em;font-size:clamp(16px,28%,64px)}
.uthumb .ptile{font-size:18px}.hero .ptile{font-size:120px;color:rgba(255,255,255,.14)}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
