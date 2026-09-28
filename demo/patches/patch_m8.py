import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:80])
    s=s.replace(old,new)

# --- 1. deposit is opt-in by host (only t1 has it), light check-in otherwise
rep("un:37,ts:9,spare:true,plan:","un:37,ts:9,spare:true,dep:true,plan:")
a=s.index('function meetStrip(t){'); b=s.index('function pollCard(t){')
s=s[:a]+r'''function meetStrip(t){ if(t.k!=='crew') return ''; const n=t.who.length+1, here=Math.min(n-1,t.mine?t.who.length:2+h(t.id)%2), st=t.hold||'none';
  if(!t.plan) return `<div class="mst"><span class="msi">📍</span><span class="msb"><b>No meetup yet</b><small>Optional · most crews meet 30 min before doors</small></span><button data-act="setmeet">Suggest one</button></div>`;
  if(!t.dep){ if(st==='in') return `<div class="mst on"><span class="msi">✓</span><span class="msb"><b>You’re here</b><small>${here+1} of ${n} here · ${esc(t.plan[1])}</small></span></div>`;
    return `<div class="mst"><span class="msi">📍</span><span class="msb"><b>${t.plan[0]} · ${esc(t.plan[1])}</b><small>${here?here+' of '+n+' already here · ':''}tap when you arrive</small></span><button data-act="checkin">I’m here</button></div>`; }
  if(st==='in') return `<div class="mst on"><span class="msi">✓</span><span class="msb"><b>Checked in · $5 released</b><small>${here+1} of ${n} here · ${esc(t.plan[1])}</small></span></div>`;
  if(st==='held') return `<div class="mst"><span class="msi">🔒</span><span class="msb"><b>$5 held · check in at ${esc(t.plan[1])}</b><small>From ${t.plan[0]} · ${here} of ${n} already here</small></span><button data-act="checkin">I’m here</button></div>`;
  return `<div class="mst"><span class="msi">🤝</span><span class="msb"><b>Host asked for a $5 hold</b><small>Back when you check in · keeps the spot for people who show</small></span><button data-act="hold">Hold $5</button></div>`; }
'''+s[b:]
rep("else if(a==='checkin'){ const t=thById(state.tid); t.hold='in';",
    "else if(a==='checkin'&&!thById(state.tid).dep){ const t=thById(state.tid); t.hold='in'; t.msgs.push({d:'sys',t:`You’re at ${t.plan[1]}`}); t.ts=++TSEQ; render(); toast('Nice · this counts toward your show-up record'); }\n  else if(a==='setmeet'){ const t=thById(state.tid); t.plan=['6:30 PM',XSPOT[h(t.id)%XSPOT.length]]; t.msgs.push({d:'sys',t:`Meetup suggested · ${t.plan[0]} at ${t.plan[1]}`}); t.ts=++TSEQ; render(); }\n  else if(a==='pollopen'){ thById(state.tid).pollOpen=true; render(); }\n  else if(a==='checkin'){ const t=thById(state.tid); t.hold='in';")

# --- 2. warm-up poll collapsed by default
rep("function pollCard(t){ if(t.k!=='crew') return '';",
    "function pollCard(t){ if(t.k!=='crew') return ''; if(!t.pollOpen&&t.vote==null) return `<button class=\"pollmini\" data-act=\"pollopen\"><i>🎤</i><span><b>Warm-up poll</b><small>Which song are you screaming tonight?</small></span>${ic('right',14)}</button>`;")

# --- 3. crew head: optional plan, mine / invite-only
rep("<div><small>Meet</small><b>${t.plan[0]}</b><small>${esc(t.plan[1])}</small></div>",
    "<div><small>Meet</small><b>${t.plan?t.plan[0]:'Not set'}</b><small>${t.plan?esc(t.plan[1]):'Optional'}</small></div>")
rep("const person=dm?PEOPLE[t.person]:PEOPLE[t.host], n=dm?2:t.who.length+1;",
    "const person=dm?PEOPLE[t.person]:(t.mine?MEP:PEOPLE[t.host]), n=dm?2:t.who.length+1;")
old='''<button class="row" data-act="person" data-v="${t.host}" style="margin-left:auto;'''
i=s.index(old); j=s.index('</button></div>',i)+len('</button></div>')
host_btn=s[i:j]
s=s[:i]+"${t.mine?`<span class=\"hostme\">${t.priv?`<button data-act=\"toast\" data-msg=\"Invite link copied · only people with the link can join\">🔗 Invite</button>`:''}<b>You’re hosting</b></span></div>`:`"+host_btn.replace('`','\\`')+"`}"+s[j:]

# --- 4. crews: size cap, auto-split, user-created crews
a=s.index('function xCrews(){'); b=s.index('const xDays=')
s=s[:a]+r'''const MEP=['Jordan Lee','JL','a2',10], MINE=[];
function xCrews(){ const out=[];
  SHOWS.slice().sort((a,b)=>a.dates[0].localeCompare(b.dates[0])).forEach(s=>{ const k0=h(s.id), nc=1+k0%2;
    MINE.filter(m=>m.s===s).forEach(m=>{ const t=thById(m.tid); const c={s,k:-1,j:m.j,name:m.name,host:MEP,n:t.cap,f:t.who.length+1,time:t.plan?t.plan[0]:'',spot:t.plan?t.plan[1]:'Meetup optional',rel:false,solo:8+Math.abs(k0>>2)%30,mine:true,tid:t.id,who:t.who}; c.ix=out.length; out.push(c); });
    for(let k=0;k<nc;k++){ const j=(k0+k*3)%8, host=PEOPLE[(k0+k*5)%8], n=4+(k0+k)%3, o=k===0&&XOV[s.artist], full=!o&&(k0+k)%4===0, f=full?n:1+((k0>>k)%(n-1));
      const c={s,k,j:o?o[0]:j,name:o?o[1]:SCENE_LIST[j][2][(k0+k)%4],host,n,f,time:o?o[3]:['5:45 PM','6:00 PM','6:15 PM','6:30 PM'][(k0+k)%4],spot:o?o[2]:j===2?XDIN[(k0+k)%3]:XSPOT[(k0+k)%5],rel:(k0+k)%3!==0,solo:8+Math.abs(k0>>2)%30,full}; c.wo=c.j===7; c.ix=out.length; out.push(c);
      if(full){ const c2={...c,k:k+10,name:c.name+' 2',host:PEOPLE[(k0+k*5+3)%8],f:1+(k0>>3)%2,full:false,auto:true,rel:false}; c2.ix=out.length; out.push(c2); } } });
  return out; }
'''+s[b:]
# xRow: full / auto / mine
rep("function xRow(c){ const left=c.n-c.f, hot=left===1;",
    "function xRow(c){ const left=c.n-c.f, hot=left===1;\n  if(c.full) return `<div class=\"xcr xfull\"><span class=\"xfi\">${ic('check',12)}</span><span class=\"xci\"><b>${esc(c.name)} is full · ${c.n} of ${c.n}</b><small>We opened ${esc(c.name)} 2 for everyone else</small></span></div>`;\n  const avs=c.mine?[MEP[3]].concat(c.who.map(k=>PEOPLE[k][3])):Array.from({length:c.f},(_,m)=>PEOPLE[(PEOPLE.indexOf(c.host)+m*3)%8][3]);")
rep("<span class=\"xav\">${Array.from({length:Math.min(3,c.f)},(_,m)=>`<span>${avi(PEOPLE[(PEOPLE.indexOf(c.host)+m*3)%8][3])}</span>`).join('')}</span>",
    "<span class=\"xav\">${avs.slice(0,3).map(p=>`<span>${avi(p)}</span>`).join('')}</span>")
rep("<em>${hot?'1 spot left':left+' spots left'}${c.rel?' · 100% showed up':''}</em>",
    "<em>${c.mine?'Your crew · ':''}${c.auto?'Just opened · ':''}${hot?'1 spot left':left+' spots left'}${c.rel?' · 100% showed up':''}</em>")
rep('''<button class="xjn ${hot?'hot':''}" data-act="xjoin" data-v="${c.ix}">${hot?'Last spot':'Join'}</button>''',
    '''<button class="xjn ${hot&&!c.mine?'hot':''}" data-act="xjoin" data-v="${c.ix}">${c.mine?'Open':hot?'Last spot':'Join'}</button>''')
rep("<span class=\"xmt\">📍 ${c.time} · ${esc(c.spot)}</span>",
    "<span class=\"xmt\">📍 ${c.time?c.time+' · ':''}${esc(c.spot)}</span>")
# group: start another crew row
rep("<span class=\"xsp\">👤 ${cs[0].solo} solo</span></button>${cs.map(xRow).join('')}</div>`; }",
    "<span class=\"xsp\">👤 ${cs[0].solo} solo</span></button>${cs.map(xRow).join('')}<button class=\"xnew\" data-act=\"ncopen\" data-id=\"${s.id}\">${ic('plus',14)} Start a crew for this show</button></div>`; }")
# xjoin: mine opens; last spot closes crew
rep("else if(a==='xjoin'){ const c=xCrews()[+v];",
    "else if(a==='xjoin'){ const c=xCrews()[+v]; if(c.mine){ openThread(thById(c.tid)); return; }")
rep("msgs:[{d:'sys',t:`You joined ${c.name}`},",
    "msgs:[{d:'sys',t:c.n-c.f===1?`You took the last spot · ${c.name} is now full, new people go to ${c.name} 2`:`You joined ${c.name} · ${c.f+1} of ${c.n}`},")
# explore empty state
rep('''<button data-act="toast" data-msg="Pick a show, set a meetup, and invite people">＋ Start the first crew</button>''',
    '''<button data-act="ncopen" data-id="${(L[0]||all[0]).s.id}">＋ Start the first crew</button>''')
# plus menu
rep("['🤝','Start a crew','Pick a show, set a meetup','toast','Pick a show, set a meetup, invite buddies']",
    "['🤝','Start a crew','Pick a show, up to 8 people','ncopen','']")

# --- 5. show page: real crews list + start crew
rep("  const crews=[[PEOPLE[0],'Pit crew, then late-night food',3,5],[PEOPLE[1],'Solo-goers meet at the bar',2,6],[PEOPLE[2],'Women-only crew',3,4]];\n",
    "  const cs=xCrews().filter(c=>c.s===s);\n")
a=s.index("      ${crews.map(([p,name,f,n],i)=>"); b=s.index("Start your own crew</span></button>")+len("Start your own crew</span></button>")
s=s[:a]+'''      <div class="xgrp xgs">${cs.map(xRow).join('')}</div>
      <button class="crewrow newcrew" data-act="ncopen" data-id="${s.id}">${ic('plus',20)}<span style="flex:1;font-weight:600;letter-spacing:-.02em">Start your own crew</span></button>
      <p class="note" style="margin:0">Crews cap at 8 · when one fills, we open the next</p>'''+s[b:]

# --- 6. start-a-crew sheet
NC=r'''
function ncSheet(){ const c=state.nc, s=byId[c.sid], order=[0,1,2,4,6,7,3,5], wo=c.j===7, lock=wo&&ME.idv!==true;
  const tg=(k,on,b,sm)=>`<div class="nct"><span><b>${b}</b><small>${sm}</small></span><button class="tgl" role="switch" aria-checked="${on}" aria-label="${b}" data-act="ncset" data-k="${k}" data-v="${on?0:1}"><i></i></button></div>`;
  return `<div class="sheetbg" data-act="ncclose"></div><div class="sheet csheet ncs" role="dialog" aria-label="Start a crew">
  <div class="cgrab"><i class="grab"></i><h3>Start a crew <span class="emo">🤝</span></h3><p>${esc(s.artist)} · ${sd(s.dates[0])} · ${esc(s.venue.replace('Madison Square Garden','MSG').replace('Radio City Music Hall','Radio City'))}</p></div>
  <div class="ncb">
    <p class="ncl">Vibe</p><div class="ncv">${order.map(j=>`<button class="gch" data-act="ncset" data-k="j" data-v="${j}" aria-pressed="${c.j===j}">${SCENE_EMO[j]} ${SCENE_LIST[j][0]}</button>`).join('')}</div>
    <p class="ncl">Crew size</p><div class="ncsz">${[4,5,6,7,8].map(n=>`<button data-act="ncset" data-k="cap" data-v="${n}" aria-pressed="${c.cap===n}">${n}</button>`).join('')}</div>
    <small class="nch">Small crews actually talk. When yours fills, new people go to the next crew.</small>
    <p class="ncl">Who can join</p><div class="ncsz two"><button data-act="ncset" data-k="vis" data-v="1" aria-pressed="${!c.priv}">Anyone going</button><button data-act="ncset" data-k="vis" data-v="0" aria-pressed="${!!c.priv}">Invite only</button></div>
    <p class="ncl">Optional</p>
    ${tg('meet',c.meet,'Suggest a meetup',c.meet?'6:30 PM · '+esc(XSPOT[h(s.id)%XSPOT.length])+' · you can change it later':'Skip it, sort it out in the chat')}
    ${tg('dep',c.dep,'Ask for a $5 hold','Refunded when people show up · good for hot shows')}
    ${wo?`<p class="ncw">💃 Women-only crews need a verified ID${lock?' · verify on your profile first':' · you’re verified'}</p>`:''}
  </div>
  <button class="cgo new" data-act="nccreate" ${lock?'aria-disabled="true"':''}>${lock?'Verify ID to create':'Create crew'}</button></div>`; }
'''
i=s.index('function kitSheet(){'); s=s[:i]+NC.lstrip()+s[i:]
rep("+(state.safe?safetySheet():'')","+(state.safe?safetySheet():'')+(state.nc?ncSheet():'')")
H=r'''  else if(a==='ncopen'){ closePlus&&document.getElementById('psheet')&&(state.psheet=false); state.nc={sid:id||(A('Harry Styles')||SHOWS[0]).id,j:0,cap:6,priv:false,meet:true,dep:false}; render(); }
  else if(a==='ncclose'){ state.nc=null; render(); }
  else if(a==='ncset'){ const k=t.dataset.k, n=+v; if(k==='vis') state.nc.priv=!n; else if(k==='meet'||k==='dep') state.nc[k]=!!n; else state.nc[k]=n; render(); }
  else if(a==='nccreate'){ const c=state.nc, s=byId[c.sid]; if(c.j===7&&ME.idv!==true){ toast('Women-only crews need a verified ID · verify it on your profile'); return; }
    const name=SCENE_LIST[c.j][2][0], p=(h(s.id)+1)%8;
    const t={id:'t'+(++TSEQ),k:'crew',mine:true,priv:c.priv,show:s.artist,title:name,long:`${name} · ${s.artist}`,host:-1,who:[],cap:c.cap,un:0,ts:++TSEQ,dep:c.dep,plan:c.meet?['6:30 PM',XSPOT[h(s.id)%XSPOT.length]]:null,
      msgs:[{d:'sys',t:`You started ${name} · 1 of ${c.cap}`}].concat(c.priv?[{d:'sys',t:'Invite only · share the link with friends'}]:[]),replies:[[p,'Sounds good!']]};
    TH.unshift(t); MINE.push({tid:t.id,s,j:c.j,name}); state.nc=null; openThread(t); toast(c.priv?'Crew created · invite link ready':'Crew created · it’s now listed on Explore');
    setTimeout(()=>{ t.who.push(p); t.msgs.push({d:'sys',t:`${P0(p)} joined${c.priv?' via your link':''} · ${t.who.length+1} of ${t.cap}`}); t.msgs.push({d:'in',p,t:`Hey! First time seeing ${s.artist} live 🙌`,time:nowT()}); t.ts=++TSEQ; if(state.screen==='crew'&&state.tid===t.id) render(); else t.un++; },2600); }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")

CSS=r'''
.pollmini{align-self:stretch;display:flex;align-items:center;gap:10px;margin:4px 0 10px;padding:10px 12px;border-radius:16px;background:rgba(40,40,44,.55);backdrop-filter:blur(14px);color:#fff;text-align:left}
.pollmini i{font-style:normal;font-size:18px}.pollmini span{flex:1;display:flex;flex-direction:column}.pollmini b{font-size:14px;letter-spacing:-.01em}.pollmini small{font-size:12px;color:rgba(255,255,255,.6)}
.hostme{margin-left:auto;display:flex;align-items:center;gap:6px}.hostme b,.hostme button{height:34px;padding:0 12px;border-radius:17px;background:rgba(60,60,64,.5);backdrop-filter:blur(12px);color:#fff;font-size:13px;font-weight:600;display:inline-flex;align-items:center}
.xfull{opacity:.75}.xfull .xci b{font-size:14px;color:var(--muted);font-weight:600}.xfull small{font-size:12px;color:var(--muted)}
.xfi{width:24px;height:24px;border-radius:50%;background:var(--card2);display:grid;place-items:center;flex-shrink:0;color:#6B6B70}
.xnew{display:flex;align-items:center;justify-content:center;gap:6px;width:100%;height:40px;margin:2px 0 6px;border-top:1px solid var(--line);font-size:13px;font-weight:600;color:var(--muted);letter-spacing:-.01em}
.xgs{margin:0;padding:4px 12px 2px}.xgs .xcr:first-child{border-top:0;margin-top:0}
.ncs{max-height:calc(100% - 40px);display:flex;flex-direction:column}
.ncb{padding:4px 16px 0;overflow-y:auto}
.ncl{margin:16px 0 8px;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.ncv{display:flex;flex-wrap:wrap;gap:6px}
.ncsz{display:flex;gap:6px}.ncsz button{flex:1;height:40px;border-radius:12px;background:var(--card2);font-weight:600;font-size:15px;color:var(--text)}
.ncsz button[aria-pressed=true]{background:#0B0B0C;color:#fff}.ncsz.two button{font-size:14px}
.nch{display:block;margin-top:8px;font-size:12.5px;color:var(--muted);line-height:1.4}
.nct{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}.nct:last-of-type{border-bottom:0}
.nct span{flex:1;display:flex;flex-direction:column;gap:2px}.nct b{font-size:15px;letter-spacing:-.02em}.nct small{font-size:12.5px;color:var(--muted)}
.tgl{width:46px;height:28px;border-radius:14px;background:#D6D6DA;position:relative;flex-shrink:0;transition:background .2s}
.tgl i{position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:transform .2s}
.tgl[aria-checked=true]{background:#0B0B0C}.tgl[aria-checked=true] i{transform:translateX(18px)}
.ncw{margin:12px 0 0;padding:10px 12px;border-radius:12px;background:var(--card2);font-size:13px}
.cgo[aria-disabled=true]{background:var(--card2);color:var(--muted)}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
