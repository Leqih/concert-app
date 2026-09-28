import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
# up-next merged into first ticket
rep('<span class="tchips">${chip(s,pending)}</span>','<span class="tchips">${i===0&&!pending?`<em class="nx">Up next · ${days(s.dates[0])}</em>`:''}${chip(s,pending)}</span>')
rep('''    <div class="upnx"><span class="upk">Up next</span><b>${esc(nx[0].artist)}</b><span class="upd">${days(nx[0].dates[0])}</span><span class="upr"><i class="eb">🚪</i>Doors 7:00<i class="eb">👯</i>Meet 6:15</span></div>
    ${splitCard()}<div class="wal" id="wal" data-n="${all.length}">${all.map(card).join('')}</div>
    <button class="wall" id="wall" data-act="wclose">Show all tickets</button>''',
'''    <div class="wal" id="wal" data-n="${all.length}">${all.map(card).join('')}<div class="wact" id="wact" aria-hidden="true"><button data-act="wqr">${ic('ticket',16)} Show QR</button><button data-act="wchat">${ic('chat',16)} Crew chat</button><button data-act="wsell">${ic('share',16)} Sell spare</button></div></div>
    <button class="wall" id="wall" data-act="wclose">Show all tickets</button>
    <p class="slab" style="margin:22px 20px 8px">To do</p>${splitCard()}''')
rep("const nx=all[0];","const nx=all[0]; window._wall=all;")
# compact split row with expand
a=s.index('function splitCard(){'); b=s.index('function lockedCard(')
s=s[:a]+r'''function splitCard(){ const s=A(SPLIT.show); if(!s) return ''; const tot=spareOf(s).face+FEE, op=!!state.splitOpen, paid=SPLIT.released?2:1;
  return `<div class="splitc ${op?'op':''}"><button class="sph2" data-act="splitop" aria-expanded="${op}"><span class="spav2"><span>${avi(PEOPLE[1][3])}</span><span>${avi(PEOPLE[6][3])}</span></span><span class="sptx"><b>Split · ${esc(s.artist)}</b><small>${SPLIT.released?'Seat released to your crew':`${paid} of 2 paid · ${P0(6)} owes $${tot}`}</small></span>${ic('chev',14)}</button>
  ${op?`<div class="spr2"><span class="spav">${avi(PEOPLE[1][3])}</span><span class="spt"><b>${PEOPLE[1][0]}</b><small>Paid $${tot}</small></span><em>${ic('check',12)} Paid</em></div>
  <div class="spr2"><span class="spav">${avi(PEOPLE[6][3])}</span><span class="spt"><b>${PEOPLE[6][0]}</b><small>${SPLIT.released?'Seat listed · your crew gets 24h first':'$'+tot+' due in 2 days'}</small></span>${SPLIT.released?'<em>Listed</em>':'<button data-act="nudge">Nudge</button>'}</div>
  ${SPLIT.released?'':'<button class="sprel" data-act="release">Unpaid by the deadline? Release the seat to your crew</button>'}`:''}</div>`; }
'''+s[b:]
# wallet layout: action bar under open ticket
rep("  let j=0; cs.forEach((c,i)=>{ if(i===open){","  const wa=document.getElementById('wact'); if(wa){ wa.classList.add('on'); wa.setAttribute('aria-hidden','false'); }\n  let j=0; cs.forEach((c,i)=>{ if(i===open){")
rep("c.style.transform=`translateY(${232+j*14}px) scale(${1-(n-1-j)*.035})`","c.style.transform=`translateY(${282+j*14}px) scale(${1-(n-1-j)*.035})`")
rep("w.style.height=(232+(n-2)*14+214)+'px'; }","w.style.height=(282+(n-2)*14+214)+'px'; }")
rep("  if(open==null){ cs.forEach((c,i)=>{","  if(open==null){ const wa=document.getElementById('wact'); if(wa){ wa.classList.remove('on'); wa.setAttribute('aria-hidden','true'); }\n    cs.forEach((c,i)=>{")
H=r'''  else if(a==='splitop'){ state.splitOpen=!state.splitOpen; const sc=document.querySelector('.scroll'), y=sc&&sc.scrollTop, o=(document.getElementById('wal')||{}).dataset; const op=o&&o.open; render(); const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; if(op!==''&&op!=null) layWallet(+op); }
  else if(a==='wqr'){ const w=document.getElementById('wal'), c=w&&w.querySelector('.wc.op'); if(c) c.querySelector('.tflip').classList.toggle('on'); }
  else if(a==='wchat'){ const w=document.getElementById('wal'), r=(window._wall||[])[+w.dataset.open]; if(r) openThread(threadFor(r[0].id)); }
  else if(a==='wsell'){ const w=document.getElementById('wal'), r=(window._wall||[])[+w.dataset.open]; if(r&&MYTIX().some(x=>x[0]===r[0])){ state.sell={step:1,id:r[0].id,qty:1}; go('sell'); } else toast('Only tickets in your name can be listed'); }
'''
rep("  else if(a==='wtap'){", H+"  else if(a==='wtap'){")
rep('<div class="sprule"><span><i class="eb">🔒</i>Face value + $2 flat</span><span><i class="eb">👯</i>Crews get 24h first</span><span><i class="eb">✌️</i>Max 2 per show</span></div>',
    '<div class="sprule"><span><i class="eb">🔒</i>Face value + $2</span><span><i class="eb">👯</i>Crews first</span><span><i class="eb">✌️</i>Max 2 each</span></div>')
CSS=r'''
.tchips em.nx{background:#fff;color:#0B0B0C}
.wact{position:absolute;left:0;right:0;top:226px;height:44px;display:flex;gap:8px;opacity:0;transform:translateY(-8px);pointer-events:none;transition:opacity .3s .15s,transform .4s cubic-bezier(.2,.8,.2,1) .15s;z-index:60}
.wact.on{opacity:1;transform:none;pointer-events:auto}
.wact button{flex:1;height:44px;border-radius:var(--r-pill);background:var(--card);box-shadow:inset 0 0 0 1px var(--line);display:inline-flex;align-items:center;justify-content:center;gap:6px;font-size:13.5px;font-weight:600;color:var(--text)}
.wact button:first-child{background:#0B0B0C;color:#fff;box-shadow:none}
.splitc{margin:0 16px;padding:0;background:var(--card);overflow:hidden}
.sph2{display:flex;align-items:center;gap:12px;width:100%;padding:12px 14px;text-align:left;color:var(--text)}.sph2>svg{color:var(--dim);transition:transform .25s}.splitc.op .sph2>svg{transform:rotate(180deg)}
.spav2{display:flex}.spav2 span{width:32px;height:32px;border-radius:50%;overflow:hidden;position:relative;border:2px solid var(--card);margin-left:-10px}.spav2 span:first-child{margin-left:0}.spav2 img{width:100%;height:100%;object-fit:cover}
.sptx{flex:1;display:flex;flex-direction:column;gap:2px}.sptx b{font-size:15px;letter-spacing:-.02em}.sptx small{font-size:12.5px;color:var(--muted)}
.splitc.op .spr2,.splitc.op .sprel{margin-left:14px;margin-right:14px}.splitc.op .sprel{margin-bottom:12px}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
