import re
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,count=1):
    global s
    n=s.count(old)
    assert n>=1, 'missing: '+old[:80]
    if count==1: assert n==1, f'ambiguous ({n}): '+old[:80]
    s=s.replace(old,new)

CSS=r"""
/* ===== M7: trust, safety, commitment ===== */
.mst{display:flex;align-items:center;gap:10px;margin-top:10px;padding:10px 10px 10px 12px;border-radius:18px;background:rgba(40,40,44,.5);backdrop-filter:blur(12px)}
.mst.on{background:rgba(255,255,255,.14)}
.msi{width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.12);display:grid;place-items:center;font-size:16px;flex-shrink:0}
.msb{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px;text-align:left}.msb b{font-size:14px;letter-spacing:-.02em}.msb small{font-size:12px;color:rgba(255,255,255,.62)}
.mst button{height:34px;padding:0 14px;border-radius:17px;background:#F5F5F7;color:#0B0B0C;font-weight:600;font-size:13px;flex-shrink:0}
.locchip{margin-top:8px;display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 12px;border-radius:14px;background:rgba(255,255,255,.14);font-size:12px;color:rgba(255,255,255,.85)}
.pollc{align-self:stretch;margin:4px 0 10px;padding:14px;border-radius:20px;background:rgba(40,40,44,.55);backdrop-filter:blur(14px);display:flex;flex-direction:column;gap:8px}
.pch{display:flex;flex-direction:column;gap:2px}.pch b{font-size:12.5px;color:rgba(255,255,255,.65);font-weight:600}.pch span{font-size:16px;font-weight:600;letter-spacing:-.02em;color:#fff}
.pco{position:relative;height:40px;border-radius:12px;background:rgba(255,255,255,.1);color:#fff;font-size:14px;font-weight:600;display:flex;align-items:center;justify-content:space-between;padding:0 12px;overflow:hidden;text-align:left;width:100%}
.pco.res i{position:absolute;left:0;top:0;bottom:0;background:rgba(255,255,255,.16);border-radius:12px;transition:width .5s cubic-bezier(.2,.8,.2,1)}
.pco.res.me i{background:rgba(255,255,255,.36)}
.pco span,.pco em{position:relative;font-style:normal}
.pcf{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:12.5px;color:rgba(255,255,255,.7)}
.pcf b{color:#fff}
.pcf button{height:30px;padding:0 12px;border-radius:15px;background:rgba(255,255,255,.12);color:#fff;font-size:12.5px;font-weight:600;flex-shrink:0}
.homec{align-self:stretch;margin:8px 0;padding:14px;border-radius:20px;background:#F5F5F7;color:#0B0B0C;display:flex;flex-direction:column;gap:6px}
.homec b{font-size:15px;letter-spacing:-.02em}
.homec span{font-size:14px;color:#55555B;line-height:1.35}
.homec button{align-self:flex-start;height:36px;padding:0 16px;border-radius:18px;background:#0B0B0C;color:#fff;font-weight:600;font-size:14px;margin-top:4px}
.nb.sfb{width:auto;padding:0 14px;font-size:14px;font-weight:600;color:#fff;gap:6px}
.sfl{margin:14px 16px 0;display:flex;flex-direction:column;gap:8px}
.sfr{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:16px;background:var(--bg);text-align:left;color:var(--text);width:100%}
.sfr>span.sft{flex:1;display:flex;flex-direction:column;gap:2px}.sfr b{font-size:15px;letter-spacing:-.02em}.sfr small{font-size:12.5px;color:var(--muted)}
.tg{width:44px;height:26px;border-radius:13px;background:#D6D6DA;position:relative;flex-shrink:0;transition:background .2s}
.tg i{position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.2)}
.sfr[aria-pressed=true] .tg{background:#0B0B0C}.sfr[aria-pressed=true] .tg i{transform:translateX(18px)}
.vbadges{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.vbadges span{height:30px;padding:0 12px;border-radius:15px;background:var(--card2);display:inline-flex;align-items:center;gap:5px;font-size:13px;font-weight:600;letter-spacing:-.01em}
.vcard{margin-top:14px;width:100%;display:flex;align-items:center;gap:12px;padding:14px;border-radius:18px;background:#0B0B0C;color:#fff;text-align:left}
.vcard.busy{opacity:.85}
.vci{font-size:22px}.vcb{flex:1;display:flex;flex-direction:column;gap:2px}.vcb b{font-size:15px;letter-spacing:-.02em}.vcb small{font-size:12.5px;color:rgba(255,255,255,.65)}
.rpt{display:flex;gap:8px;align-items:center;margin-top:18px;font-size:13px;color:var(--muted)}.rpt button{color:var(--muted);font-size:13px;text-decoration:underline;text-underline-offset:3px}
.splitc{margin:14px 16px 6px;padding:14px;border-radius:20px;background:#fff;box-shadow:0 1px 0 var(--line),0 10px 30px rgba(0,0,0,.06);display:flex;flex-direction:column;gap:10px}
.sph{display:flex;align-items:baseline;justify-content:space-between;gap:8px}.sph b{font-size:15px;letter-spacing:-.02em}.sph span{font-size:12.5px;color:var(--muted)}
.spr2{display:flex;align-items:center;gap:10px}.spr2>span.spt{flex:1;display:flex;flex-direction:column;text-align:left}.spr2 b{font-size:14px}.spr2 small{font-size:12.5px;color:var(--muted)}
.spav{width:34px;height:34px;border-radius:50%;overflow:hidden;flex-shrink:0}.spav img{width:100%;height:100%;object-fit:cover}
.spr2 em{font-style:normal;font-size:12.5px;font-weight:600;display:inline-flex;align-items:center;gap:4px;color:#0B0B0C}
.spr2 button{height:32px;padding:0 14px;border-radius:16px;background:#0B0B0C;color:#fff;font-size:13px;font-weight:600}
.sprel{height:38px;border-radius:12px;background:var(--bg);font-size:13px;font-weight:600;color:var(--text)}
.spnone.lk a{display:inline-flex;align-items:center;justify-content:center;height:40px;padding:0 16px;border-radius:20px;background:#0B0B0C;color:#fff;font-weight:600;font-size:14px;text-decoration:none;margin-top:6px}
.recrew{margin:14px 16px 0;width:calc(100% - 32px);display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:16px;background:#0B0B0C;color:#fff;text-align:left}
.rcb{flex:1;display:flex;flex-direction:column;gap:2px}.rcb b{font-size:15px;letter-spacing:-.02em}.rcb small{font-size:12.5px;color:rgba(255,255,255,.65)}
.wtag{display:inline-flex;margin-left:6px;height:20px;padding:0 8px;border-radius:10px;background:#0B0B0C;color:#fff;font-size:11px;font-weight:600;align-items:center;vertical-align:1px}
</style>"""
i=s.index('</style>')
s=s[:i]+CSS+s[i+len('</style>'):]

# ---- data + helpers
rep("const KIT={show:'Wave To Earth',who:[5,7,2],pick:{5:true,7:true,2:true},done:false};",
"""const KIT={show:'Wave To Earth',who:[5,7,2],pick:{5:true,7:true,2:true},done:false};
const FEE=2, ME={idv:false};
const REL=[[12,12],[7,8],[9,9],[15,15],[5,5],[6,6],[4,5],[10,11]];
const SONGS={'Harry Styles':['As It Was','Watermelon Sugar','Sign of the Times'],'Doja Cat':['Say So','Paint The Town Red','Kiss Me More'],'Gorillaz':['Feel Good Inc.','Clint Eastwood','On Melancholy Hill'],'Steve Lacy':['Bad Habit','Dark Red','Static']};
const songsFor=a=>SONGS[a]||['The opener','The big single','The encore'];
const LOCKED=s=>!!s&&!['Harry Styles','Doja Cat','Gorillaz','Steve Lacy'].includes(s.artist)&&h(s.id)%4===2;
const SPLIT={show:'Doja Cat',released:false};
function meetStrip(t){ if(t.k!=='crew') return ''; const n=t.who.length+1, here=Math.min(n-1,2+h(t.id)%2), st=t.hold||'none';
  if(st==='in') return `<div class="mst on"><span class="msi">✓</span><span class="msb"><b>Checked in · $5 released</b><small>${here+1} of ${n} here · ${esc(t.plan[1])}</small></span></div>`;
  if(st==='held') return `<div class="mst"><span class="msi">🔒</span><span class="msb"><b>$5 held · check in at ${esc(t.plan[1])}</b><small>From ${t.plan[0]} · ${here} of ${n} already here</small></span><button data-act="checkin">I’m here</button></div>`;
  return `<div class="mst"><span class="msi">🤝</span><span class="msb"><b>Hold $5 to lock your spot</b><small>Back when you check in · no-shows buy the crew a round</small></span><button data-act="hold">Hold $5</button></div>`; }
function pollCard(t){ if(t.k!=='crew') return ''; const S=songsFor(t.show), base=[3+h(t.id)%3,2+h(t.title)%3,1+h(t.show)%2], v=t.vote;
  const c=base.map((x,i)=>x+(v===i?1:0)), tot=c.reduce((a,b)=>a+b,0), top=c.indexOf(Math.max(...c));
  return `<div class="pollc"><div class="pch"><b>Warm-up 🎤</b><span>Which song are you screaming tonight?</span></div>${S.map((x,i)=>v==null?`<button class="pco" data-act="vote" data-v="${i}"><span>${esc(x)}</span></button>`:`<div class="pco res ${v===i?'me':''}"><i style="width:${Math.round(c[i]/tot*100)}%"></i><span>${esc(x)}</span><em>${Math.round(c[i]/tot*100)}%</em></div>`).join('')}<div class="pcf"><span>${v==null?'Vote to reveal the crew anthem':'Crew anthem: <b>'+esc(S[top])+'</b>'}</span><button data-act="bracelet">📿 Bracelet swap</button></div></div>`; }
function homeCard(t){ const st=t.homeSt||'offer', a=P0(t.who[1]||t.host), b=P0(t.who[t.who.length-1]);
  return `<div class="homec"><b>Heading home? 🏠</b><span>${st==='done'?'Everyone’s home safe. Night mode is off.':st==='joined'?`You’re riding with ${a} & ${b} · tap when you’re back`:`${a} & ${b} are taking the L toward Brooklyn after the show`}</span>${st==='offer'?'<button data-act="homejoin">Ride together</button>':st==='joined'?'<button data-act="homedone">I’m home</button>':''}</div>`; }
function safetySheet(){ const t=thById(state.tid)||{}, s=t.show?thShow(t):null, on=!!(state.loc&&state.loc[state.tid]);
  return `<div class="sheetbg" data-act="safeclose"></div><div class="sheet csheet" id="safesheet" role="dialog" aria-label="Safety tools">
  <div class="cgrab"><i class="grab"></i><h3>Safety tools <span class="emo">🛡️</span></h3><p>Only this crew sees it · everything switches off after the show</p></div>
  <div class="sfl">
   <button class="sfr" data-act="loc" aria-pressed="${on}"><i class="eb">📍</i><span class="sft"><b>Share my location</b><small>Doors → 1h after the show · crew only</small></span><span class="tg"><i></i></span></button>
   <button class="sfr" data-act="homeplan"><i class="eb">🏠</i><span class="sft"><b>Plan the ride home</b><small>Pair up with crew-mates heading your way</small></span>${ic('right',16)}</button>
   <button class="sfr" data-act="alert"><i class="eb">🚨</i><span class="sft"><b>Alert my crew</b><small>Sends “need help” and where you are</small></span>${ic('right',16)}</button>
   <button class="sfr" data-act="toast" data-msg="Calling venue security (demo)"><i class="eb">☎️</i><span class="sft"><b>Venue security</b><small>${s?esc(s.venue.replace('Madison Square Garden','MSG')):'Venue'} · staff point by the main entrance</small></span>${ic('right',16)}</button>
   <button class="sfr" data-act="toast" data-msg="Open someone’s profile to report or block"><i class="eb">🚫</i><span class="sft"><b>Report or block</b><small>From any profile · they leave your crews</small></span>${ic('right',16)}</button>
  </div></div>`; }
function closeSafe(after){ const sh=document.getElementById('safesheet'), bg=document.querySelector('.sheetbg'); if(!sh){ state.safe=false; render(); after&&after(); return; }
  sh.classList.add('out'); bg&&bg.classList.add('out'); setTimeout(()=>{ state.safe=false; render(); after&&after(); },260); }
function vBadges(p){ const r=REL[p]||[5,5]; return `<div class="vbadges"><span>${ic('check',12)} ID + ticket verified</span><span>🤝 Showed up ${r[0]}/${r[1]}</span></div>`; }
function vCard(){ const st=ME.idv; return st===true?`<div class="vbadges"><span>${ic('check',12)} ID + ticket verified</span><span>🤝 Showed up 8/8</span></div>`
  :`<button class="vcard ${st==='busy'?'busy':''}" data-act="idv" ${st==='busy'?'disabled':''}><span class="vci">🪪</span><span class="vcb"><b>${st==='busy'?'Checking your ID…':'Verify your ID · 1 min'}</b><small>Ticket ✓ · ID not yet · unlocks women-only crews</small></span>${st==='busy'?'<i class="spin sm"></i>':ic('right',16)}</button>`; }
function rptRow(p){ return `<div class="rpt"><button data-act="report" data-v="${p}">Report</button><span>·</span><button data-act="block" data-v="${p}">${(state.blocked||{})[p]?'Blocked':'Block'}</button></div>`; }
function splitCard(){ const s=A(SPLIT.show); if(!s) return ''; const tot=spareOf(s).face+FEE;
  return `<div class="splitc"><div class="sph"><b>Split · ${esc(s.artist)}</b><span>3 tickets · you paid upfront</span></div>
  <div class="spr2"><span class="spav">${avi(PEOPLE[1][3])}</span><span class="spt"><b>${PEOPLE[1][0]}</b><small>Paid $${tot}</small></span><em>${ic('check',12)} Paid</em></div>
  <div class="spr2"><span class="spav">${avi(PEOPLE[6][3])}</span><span class="spt"><b>${PEOPLE[6][0]}</b><small>${SPLIT.released?'Seat listed · your crew gets 24h first':'$'+tot+' due in 2 days'}</small></span>${SPLIT.released?'<em>Listed</em>':'<button data-act="nudge">Nudge</button>'}</div>
  ${SPLIT.released?'':'<button class="sprel" data-act="release">Unpaid by the deadline? Release the seat to your crew</button>'}</div>`; }
function lockedCard(s){ return `<h2 class="h2" style="font-size:24px;text-align:center">Spare tickets <span class="emo">🎟️</span></h2><div class="spnone lk"><b>🔒 Transfers are locked for this show</b><span>The artist only allows resale through Ticketmaster’s Face Value Exchange. Crews still work as usual.</span><a href="https://help.ticketmaster.com/hc/en-us/articles/9781464415249-How-does-Ticketmaster-s-Face-Value-Exchange-work" target="_blank" rel="noopener">Face Value Exchange ↗</a></div>`; }""")

# ---- tickets: flat fee + locked shows
rep("function sparesFor(s){ if(!s) return [];","function sparesFor(s){ if(!s||LOCKED(s)) return [];")
rep('<span class="spkr"><b>$${x.face}</b><small>face value</small>','<span class="spkr"><b>$${x.face+FEE}</b><small>$${x.face} + $${FEE} fee</small>')
rep("fee=Math.round(sp.face*.06*100)/100","fee=FEE")
rep("<div><span>Plus One protection</span>","<div><span>Plus One protection · flat</span>")
rep('<em>🎟️ Spare ticket · face value</em>','<em>🎟️ Face value + $2 flat</em>')
rep('<span class="spr"><b>$${sp.face}</b>','<span class="spr"><b>$${sp.face+FEE}</b>')
rep('<span><i class="eb">🔒</i>Locked at face value</span>','<span><i class="eb">🔒</i>Face value + $2 flat</span>')
rep("      ${(()=>{ const L=sparesFor(s).filter(x=>!(state.claimedIds||{})[x.id]);","      ${LOCKED(s)?lockedCard(s):(()=>{ const L=sparesFor(s).filter(x=>!(state.claimedIds||{})[x.id]);")
rep('<small>${sd(s.dates[0])} · ${4+h(s.id)%30} on the waitlist</small>','<small>${sd(s.dates[0])} · ${LOCKED(s)?\'Official exchange only\':(4+h(s.id)%30)+\' on the waitlist\'}</small>')
# women-only crew gating on show page
rep('${crews.map(([p,name,f,n],i)=>`<button class="crewrow" data-act="crew" data-id="${s.id}">','${crews.map(([p,name,f,n],i)=>`<button class="crewrow" data-act="${i===2?\'wcrew\':\'crew\'}" data-id="${s.id}">')
rep('<b class="rt">${name}</b>','<b class="rt">${name}${i===2?\'<span class="wtag">ID verified</span>\':\'\'}</b>')
# split card on tickets
rep('    <div class="wal" id="wal" data-n="${all.length}">','    ${splitCard()}<div class="wal" id="wal" data-n="${all.length}">')

# ---- crew chat
rep("const msgs=t.msgs.concat(claimed&&t.spare?","const msgs=t.msgs.filter(m=>!(m.p!=null&&(state.blocked||{})[m.p])).concat(claimed&&t.spare?")
rep("<small>${DOW[new Date(s.dates[0]+'T12:00:00Z').getUTCDay()]}</small></div></div>`;",
    "<small>${DOW[new Date(s.dates[0]+'T12:00:00Z').getUTCDay()]}</small></div></div>${meetStrip(t)}${state.loc&&state.loc[t.id]?'<div class=\"locchip\">📍 Sharing location with this crew · until 1h after the show</div>':''}`;")
rep("const bub=m=>m.d==='spare'?","const bub=m=>m.d==='home'?homeCard(t):m.d==='spare'?")
rep("<div class=\"msgs\" ${dm?'style=\"margin-top:220px\"':''}>${msgs.map(bub).join('')}","<div class=\"msgs\" ${dm?'style=\"margin-top:220px\"':''}>${dm?'':pollCard(t)}${msgs.map(bub).join('')}")
rep('<div class="nav cnav"><button class="nb" data-act="back" aria-label="Back">${ic(\'back\')}</button></div>',
    '<div class="nav cnav"><button class="nb" data-act="back" aria-label="Back">${ic(\'back\')}</button>${dm?\'\':\'<button class="nb sfb" data-act="safety" aria-label="Safety tools">🛡️ Safety</button>\'}</div>')
rep("'Everyone here has a verified ticket. Meetups are in public spots.'","'Everyone here is ID + ticket verified. Meetups are in public spots.'")

# ---- render: safety sheet
rep("+(state.kit?kitSheet():'');","+(state.kit?kitSheet():'')+(state.safe?safetySheet():'');")

# ---- keep-in-touch: re-form crew
rep("<p>Last night · ${esc(KIT.show)} · Only people who add you back become buddies</p></div>",
    "<p>Last night · ${esc(KIT.show)} · Only people who add you back become buddies</p></div>${(()=>{ const nx=A('Steve Lacy')||SHOWS[0]; return `<button class=\"recrew\" data-act=\"recrew\"><span class=\"mreqav\">${KIT.who.map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}</span><span class=\"rcb\"><b>Keep this crew together</b><small>3 shows together · go again: ${esc(nx.artist)}, ${sd(nx.dates[0])}</small></span>${ic('right',16)}</button>`; })()}")

# ---- profile: verification, reliability, report/block
rep('<div style="font-size:15px;margin-top:6px;color:var(--muted)">${P.handle}</div>',
    '<div style="font-size:15px;margin-top:6px;color:var(--muted)">${P.handle}</div>${mine?vCard():vBadges(state.pid||0)}')
rep('<div class="tags">${P.tags.map(t=>`<span>${t}</span>`).join(\'\')}</div>',
    '<div class="tags">${P.tags.map(t=>`<span>${t}</span>`).join(\'\')}</div>${mine?\'\':rptRow(state.pid||0)}')

# ---- click handlers
rep("  if(a==='show') go('show',id);\n",
"""  if(a==='show') go('show',id);
  else if(a==='hold'){ const t=thById(state.tid); t.hold='held'; render(); toast('$5 held · it comes back when you check in'); }
  else if(a==='checkin'){ const t=thById(state.tid); t.hold='in'; t.msgs.push({d:'sys',t:`You checked in at ${t.plan[1]} · $5 released`}); t.ts=++TSEQ; render(); toast('Checked in · $5 released'); }
  else if(a==='vote'){ const t=thById(state.tid); t.vote=+v; render(); }
  else if(a==='bracelet'){ toast('Pick 3 letters · trade real bracelets at the meetup 📿'); }
  else if(a==='safety'){ state.safe=true; render(); }
  else if(a==='safeclose'){ closeSafe(); }
  else if(a==='loc'){ state.loc=state.loc||{}; const on=!state.loc[state.tid]; state.loc[state.tid]=on; render(); toast(on?'Sharing with this crew until 1h after the show':'Location sharing off'); }
  else if(a==='homeplan'){ const t=thById(state.tid); if(!t.msgs.some(m=>m.d==='home')){ t.msgs.push({d:'home',time:nowT()}); t.homeSt='offer'; t.ts=++TSEQ; } closeSafe(); }
  else if(a==='homejoin'){ const t=thById(state.tid); t.homeSt='joined'; state.loc=state.loc||{}; state.loc[t.id]=true; render(); toast('Riding together · location on until you’re home'); }
  else if(a==='homedone'){ const t=thById(state.tid); t.homeSt='done'; state.loc[t.id]=false; t.msgs.push({d:'sys',t:'You’re home · the crew has been told'}); render(); }
  else if(a==='alert'){ const t=thById(state.tid); state.loc=state.loc||{}; state.loc[t.id]=true; t.msgs.push({d:'sys',t:'Alert sent · your crew can see where you are'}); t.ts=++TSEQ; closeSafe(()=>toast('Your crew has been alerted')); }
  else if(a==='report'){ toast('Report sent · our team reviews within 1 hour'); }
  else if(a==='block'){ const p=+v; state.blocked=state.blocked||{}; state.blocked[p]=true; toast(`${P0(p)} blocked · they can’t see you or message you`); back(); }
  else if(a==='idv'){ if(ME.idv) return; ME.idv='busy'; render(); setTimeout(()=>{ ME.idv=true; if(state.screen==='me') render(); toast('ID verified · women-only crews unlocked'); },1600); }
  else if(a==='wcrew'){ if(ME.idv!==true) toast('Women-only crews need a verified ID · verify it on your profile'); else go('crew',id); }
  else if(a==='recrew'){ const s2=A('Steve Lacy')||SHOWS[0]; const nt={id:'t'+(++TSEQ),k:'crew',show:s2.artist,title:'Same crew, again',long:`The ${KIT.show} crew, back for ${s2.artist}`,host:KIT.who[0],who:KIT.who.slice(),cap:6,un:0,ts:++TSEQ,plan:['6:30 PM','Main entrance'],msgs:[{d:'sys',t:`Crew re-formed from ${KIT.show} · 3 shows together`},{d:'in',p:KIT.who[1],t:'Round 4 🙌 same meetup spot?',time:nowT()}],replies:[[KIT.who[0],'Obviously. See you all there']]}; TH.unshift(nt); KIT.done=true; state.kit=false; openThread(nt); toast('Crew re-formed · everyone gets a ping to confirm'); }
  else if(a==='nudge'){ toast(`Reminder sent to ${P0(6)} · due in 2 days`); }
  else if(a==='release'){ SPLIT.released=true; render(); toast('Seat listed · your crew gets 24h first'); }
""")
open(P,'w',encoding='utf-8').write(s)
print('ok', len(s))
