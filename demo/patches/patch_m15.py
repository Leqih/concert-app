import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(s.count(o),o[:90]); s=s.replace(o,n)
# ---------- entry points
rep('data-act="toast" data-msg="Import a ticket from email or a screenshot" aria-label="Add ticket"','data-act="itopen" aria-label="Add ticket"')
rep('<button data-act="toast" data-msg="Import a ticket from email or a screenshot">Add ticket</button>','<button data-act="itopen">Add ticket</button>')
rep('data-act="toast" data-msg="Edit your profile, genres and meetup preferences" aria-label="Edit profile"','data-act="epopen" aria-label="Edit profile"')
rep('<button class="sfr" data-act="toast" data-msg="Calling venue security (demo)">','<button class="sfr" data-act="secopen">')
rep('<button type="button" aria-label="Attach" data-act="toast" data-msg="Share a photo or your ticket">','<button type="button" aria-label="Attach" data-act="attach" aria-expanded="${!!state.att}">')
rep('<button data-act="toast" data-msg="Replies open in the full thread">💬 ${o.r}</button>','<button data-act="wrep" data-v="${o.id}" aria-expanded="${!!(state.wopen||{})[o.id]}">💬 ${o.r+((state.wrp||{})[o.id]||[]).length}</button>')
# wall replies block after footer
rep("</div></article>`; }).join('')||`<p class=\"note\">Nothing here yet. Be the first to post.</p>`}</div>`; }",
    "</div>${(state.wopen||{})[o.id]?wallThread(o,x,me):''}</article>`; }).join('')||`<p class=\"note\">Nothing here yet. Be the first to post.</p>`}</div>`; }")
# profile overrides
rep("  return `<div class=\"scroll\"><div style=\"padding-bottom:${mine?120:110}px\">",
    "  if(mine&&state.prof){ P.bio=esc(state.prof.bio||'')+(state.prof.spot?`<br>Usually by the ${esc(state.prof.spot.toLowerCase())}.`:''); P.tags=state.prof.tags.map(t=>'#'+t); }\n  return `<div class=\"scroll\"><div style=\"padding-bottom:${mine?120:110}px\">")
# my tickets include imported
rep("const MYTIX=()=>[[A('Gorillaz'),'Floor GA','General admission',2],[A('Doja Cat'),'Section 105','Row 12 · Seats 8–9',2]];",
    "const MYTIX=()=>[[A('Gorillaz'),'Floor GA','General admission',2],[A('Doja Cat'),'Section 105','Row 12 · Seats 8–9',2]].concat((state.extraTix||[]).map(t=>[t[0],t[1],t[2],t[3]]));")
rep("  const all=claimed.concat(mine).sort(","  const all=claimed.concat(mine,(state.extraTix||[]).map(t=>[t[0],t[1],t[2],'imported',t[4]])).sort(")
# chat image bubble
rep("  const bub=m=>m.d==='home'?homeCard(t):","  const bub=m=>m.d==='img'?`<div class=\"bub out bimg\"><span>${img(s)}</span></div><div class=\"when\">${m.time}</div>`:m.d==='home'?homeCard(t):")
# attach menu above composer
rep("${dm?'':`<div class=\"mstpin\">${meetStrip(t)}</div>`}<form class=\"composer\"","${state.att?attMenu(t,s,dm):''}${dm||state.att?'':`<div class=\"mstpin\">${meetStrip(t)}</div>`}<form class=\"composer\"")
JS=r'''
// ---------- M15: real flows for former placeholder buttons
const IMPORTABLE=()=>[[A('Beck'),'Orchestra','Row K · Seat 12',1,'Main'],[A('The Neighbourhood'),'Section 214','Row 8 · Seats 3–4',2,'Gate C'],[A('Weezer'),'Floor GA','General admission',1,'Gate B']].filter(r=>r[0]&&!(state.extraTix||[]).some(x=>x[0]===r[0]));
function itSheet(){ const k=state.itk, L=IMPORTABLE();
  const head=`<div class="sheetbg" data-act="itclose"></div><div class="sheet csheet" role="dialog" aria-label="Add a ticket"><div class="cgrab"><i class="grab"></i><h3>Add a ticket</h3><p>We verify every ticket with the seller before it shows in your wallet</p></div><div class="ufb">`;
  let b='';
  if(k.step==='choose') b=`<button class="sopt" data-act="itstep" data-v="email"><i>📧</i><span><b>From your email</b><small>Find Ticketmaster and AXS confirmations</small></span>${ic('right',16)}</button>
      <button class="sopt" data-act="itstep" data-v="scan"><i>📷</i><span><b>From a screenshot</b><small>We read the barcode and check it</small></span>${ic('right',16)}</button>`;
  else if(k.busy) b=`<div class="itbusy"><i class="spin"></i><b>${k.step==='email'?'Checking your inbox…':'Reading the barcode…'}</b><small>${k.step==='email'?'Looking for ticket confirmations from the last 90 days':'Matching it with the official event'}</small></div>`;
  else if(k.step==='email'){ b=L.length?`<p class="ncl">Found ${L.length} ${L.length===1?'ticket':'tickets'}</p>${L.map((r,i)=>`<button class="itrow" data-act="itpick" data-v="${i}" aria-pressed="${!!(k.pick||{})[i]}"><span class="uthumb">${img(r[0])}</span><span class="ub"><b>${esc(r[0].artist)}</b><span class="um">${sd(r[0].dates[0])} · ${esc(VSH(r[0].venue))} · ${r[1]}</span></span><i class="kitc">${ic('check',14)}</i></button>`).join('')}`:`<div class="itbusy"><b>No new tickets found</b><small>Everything in your inbox is already in your wallet</small></div>`; }
  else { const r=L[0]; b=r?`<div class="itscan"><span class="itshot">${img(r[0])}<i></i></span><span><small>Found in your screenshot</small><b>${esc(r[0].artist)}</b><span>${sd(r[0].dates[0])} · ${esc(VSH(r[0].venue))}</span><span>${r[1]} · ${r[2]}</span><em>${ic('check',12)} Matches the official event</em></span></div>`:`<div class="itbusy"><b>No new tickets found</b></div>`; }
  const n=k.step==='email'?Object.values(k.pick||{}).filter(Boolean).length:(L.length?1:0);
  const cta=k.step==='choose'||k.busy?'':`<div class="uff"><button class="ufx" data-act="itstep" data-v="choose">Back</button><button class="cgo new" data-act="itadd" ${n?'':'disabled'}>${n?`Add ${n} ${n===1?'ticket':'tickets'}`:'Pick a ticket'}</button></div>`;
  return head+b+'</div>'+cta+'</div>'; }
function epSheet(){ const p=state.prof, TG=['indie','rnb','hiphop','pop','rock','jazz','latin','classical','soundboard','frontrow','dinnerfirst','sober'];
  return `<div class="sheetbg" data-act="epclose"></div><div class="sheet csheet ufs" role="dialog" aria-label="Edit profile"><div class="cgrab"><i class="grab"></i><h3>Edit profile</h3></div><div class="ufb">
    <p class="ncl">Bio</p><textarea id="epbio" class="eptx" rows="2" maxlength="80" aria-label="Bio">${esc(p.bio)}</textarea>
    <p class="ncl">Tags <em class="epn">${p.tags.length}/4</em></p><div class="ncv">${TG.map(t=>`<button class="gch" data-act="eptag" data-v="${t}" aria-pressed="${p.tags.includes(t)}" ${p.tags.length>=4&&!p.tags.includes(t)?'disabled':''}>#${t}</button>`).join('')}</div>
    <p class="ncl">Where you usually stand</p><div class="ncsz">${['Front row','Soundboard','Balcony','Bar'].map(x=>`<button data-act="epspot" data-v="${x}" aria-pressed="${p.spot===x}">${x}</button>`).join('')}</div>
    <small class="nch">Crews see this before they invite you.</small></div>
    <div class="uff"><button class="ufx" data-act="epclose">Cancel</button><button class="cgo new" data-act="epsave">Save</button></div></div>`; }
function secSheet(){ const t=thById(state.tid), s=t&&thShow(t), my=s&&MYTIX().find(r=>r[0]===s), seat=my?my[1]+(my[2]&&!/General/.test(my[2])?' · '+my[2]:''):'General admission', sent=state.secSent;
  return `<div class="sheetbg" data-act="secclose"></div><div class="sheet csheet" role="dialog" aria-label="Alert venue staff"><div class="cgrab"><i class="grab"></i><h3>Alert venue staff</h3><p>${s?esc(VSH(s.venue)):'Venue'} · for anything that feels unsafe</p></div><div class="ufb">
    ${sent?`<div class="secok"><i>${ic('check',18)}</i><b>Staff notified</b><small>Stay where you are. Your crew can see your live location.</small></div>`
      :`<p class="ncl">What we send</p><div class="secl"><span>📍<b>Your live location</b><small>Updated every few seconds</small></span><span>🎟️<b>${esc(seat)}</b><small>From your verified ticket</small></span><span>👯<b>Your crew</b><small>${t?t.who.length+1:1} people get a ping too</small></span></div>`}
  </div><div class="uff">${sent?`<button class="ufx" data-act="seccancel">Cancel alert</button><button class="cgo new" data-act="secclose">Done</button>`:`<button class="ufx" data-act="secclose">Not now</button><button class="cgo new" data-act="secsend">Send alert</button>`}</div></div>`; }
function attMenu(t,s,dm){ return `<div class="attm" role="menu"><button data-act="attsend" data-v="photo" role="menuitem"><i>📷</i>Photo</button><button data-act="attsend" data-v="ticket" role="menuitem"><i>🎟️</i>My ticket</button>${dm?'':`<button data-act="attsend" data-v="pin" role="menuitem"><i>📍</i>Meetup pin</button>`}</div>`; }
function wallThread(o,x,me){ const k=Math.abs(h(o.id)), R=[[(k+2)%8,['Same! See you there','I’ll be on the 6 train around then','Saving this']][k%3]],[(k+5)%8,['Count me in','Love this','Where exactly?'][k%3]]].concat(((state.wrp||{})[o.id]||[]).map(t=>['me',t]));
  return `<div class="wth">${R.map(([p,t])=>`<div class="wtr"><span class="bgav"><span>${avi(p==='me'?MEP[3]:PEOPLE[p][3])}</span></span><span><b>${p==='me'?'You':PEOPLE[p][0]}</b> ${esc(t)}</span></div>`).join('')}
    ${me?`<form class="wtf" onsubmit="return wallReply(event,'${o.id}')"><label hidden for="wr-${o.id}">Reply</label><input id="wr-${o.id}" placeholder="Reply to ${o.me?'your post':P0(o.p)}" autocomplete="off"><button type="submit">Reply</button></form>`:`<p class="note" style="margin:6px 0 0;text-align:left">Add your ticket to reply</p>`}</div>`; }
function wallReply(e,id){ e.preventDefault(); const i=document.getElementById('wr-'+id), v=i.value.trim(); if(!v) return false; state.wrp=state.wrp||{}; (state.wrp[id]=state.wrp[id]||[]).push(v); const sc=document.querySelector('.scroll'), y=sc&&sc.scrollTop; render(); const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; return false; }
'''
i=s.index('function upSwap(anim){'); s=s[:i]+JS.lstrip()+s[i:]
rep("+(state.ufo?ufSheet():'')","+(state.ufo?ufSheet():'')+(state.itk?itSheet():'')+(state.ep?epSheet():'')+(state.secO?secSheet():'')")
H=r'''  else if(a==='itopen'){ state.itk={step:'choose'}; render(); }
  else if(a==='itclose'){ state.itk=null; render(); }
  else if(a==='itstep'){ state.itk={step:v,busy:v!=='choose',pick:{0:true}}; render(); if(v!=='choose') setTimeout(()=>{ if(state.itk){ state.itk.busy=false; render(); } },1100); }
  else if(a==='itpick'){ const k=state.itk; k.pick=k.pick||{}; k.pick[v]=!k.pick[v]; render(); }
  else if(a==='itadd'){ const k=state.itk, L=IMPORTABLE(), add=k.step==='email'?L.filter((_,i)=>(k.pick||{})[i]):L.slice(0,1); state.extraTix=(state.extraTix||[]).concat(add); state.itk=null; render(); toast(`${add.length} ${add.length===1?'ticket':'tickets'} added · verified ✓`); }
  else if(a==='epopen'){ state.prof=state.prof||{bio:'Indie, R&B, anything live.',tags:['indie','soundboard','dinnerfirst'],spot:'Soundboard'}; state.ep={...state.prof,tags:state.prof.tags.slice()}; state.prof=state.ep._keep||state.prof; render(); }
  else if(a==='epclose'){ state.ep=null; render(); }
  else if(a==='eptag'){ const b=document.getElementById('epbio'); if(b) state.ep.bio=b.value; const L=state.ep.tags, i=L.indexOf(v); if(i<0){ if(L.length<4) L.push(v); } else L.splice(i,1); render(); }
  else if(a==='epspot'){ const b=document.getElementById('epbio'); if(b) state.ep.bio=b.value; state.ep.spot=v; render(); }
  else if(a==='epsave'){ const b=document.getElementById('epbio'); state.prof={bio:(b?b.value:state.ep.bio).trim(),tags:state.ep.tags,spot:state.ep.spot}; state.ep=null; render(); toast('Profile updated'); }
  else if(a==='secopen'){ state.safe=false; state.secO=true; state.secSent=false; render(); }
  else if(a==='secsend'){ state.secSent=true; const t=thById(state.tid); if(t){ t.msgs.push({d:'sys',t:'You alerted venue staff · your crew can see your location'}); t.ts=++TSEQ; state.loc=state.loc||{}; state.loc[t.id]=true; } render(); }
  else if(a==='seccancel'){ state.secSent=false; state.secO=false; render(); toast('Alert cancelled'); }
  else if(a==='secclose'){ state.secO=false; render(); }
  else if(a==='attach'){ state.att=!state.att; render(); }
  else if(a==='attsend'){ const t=thById(state.tid), s=thShow(t); state.att=false; if(v==='photo'){ t.msgs.push({d:'img',time:nowT()}); }
    else if(v==='ticket'){ const my=MYTIX().find(r=>r[0]===s); if(!my){ render(); toast('No ticket for this show yet · add one in Tickets'); return; } t.msgs.push({d:'sys',t:`You shared your verified ticket · ${my[1]}`}); }
    else { if(!t.plan){ render(); toast('Set a meetup first'); return; } t.msgs.push({d:'out',t:`📍 I’m at ${t.plan[1]}`,time:nowT()}); }
    t.ts=++TSEQ; render(); }
  else if(a==='wrep'){ state.wopen=state.wopen||{}; state.wopen[v]=!state.wopen[v]; const sc=document.querySelector('.scroll'), y=sc&&sc.scrollTop; render(); const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")
CSS=r'''
.sopt{display:flex;align-items:center;gap:12px;width:100%;padding:14px;margin-top:8px;border-radius:var(--r-lg);background:var(--card2);text-align:left;color:var(--text)}
.sopt i{font-style:normal;font-size:22px}.sopt span{flex:1;display:flex;flex-direction:column;gap:2px}.sopt b{font-size:15px}.sopt small{font-size:12.5px;color:var(--muted)}
.itbusy{display:flex;flex-direction:column;align-items:center;gap:6px;padding:28px 0;text-align:center}.itbusy b{font-size:15px}.itbusy small{font-size:13px;color:var(--muted)}
.itrow{display:flex;align-items:center;gap:12px;width:100%;padding:10px 0;border-top:1px solid var(--line);text-align:left;color:var(--text)}.itrow:first-of-type{border-top:0}
.itrow .kitc{width:24px;height:24px;border-radius:50%;box-shadow:inset 0 0 0 1.5px #C9C9CE;display:grid;place-items:center;color:transparent;flex-shrink:0}.itrow[aria-pressed=true] .kitc{background:#0B0B0C;box-shadow:none;color:#fff}
.itscan{display:flex;gap:14px;align-items:center;padding:8px 0}.itshot{position:relative;width:96px;height:150px;border-radius:var(--r-md);overflow:hidden;flex-shrink:0;background:#111}
.itshot i{position:absolute;left:0;right:0;height:2px;background:#fff;box-shadow:0 0 12px #fff;animation:scanl 1.6s ease-in-out infinite}@keyframes scanl{0%{top:8%}50%{top:88%}100%{top:8%}}
.itscan>span:last-child{display:flex;flex-direction:column;gap:3px;font-size:13px;color:var(--muted)}.itscan b{font-family:var(--display);font-size:20px;color:var(--text);letter-spacing:-.03em}.itscan em{font-style:normal;display:inline-flex;align-items:center;gap:4px;margin-top:6px;color:var(--text);font-weight:600;font-size:12.5px}
.eptx{width:100%;box-sizing:border-box;padding:12px 14px;border:0;border-radius:var(--r-md);background:var(--card2);font:inherit;font-size:15px;color:var(--text);resize:none;outline:none}
.epn{font-style:normal;float:right;letter-spacing:0;text-transform:none}
.secl{display:flex;flex-direction:column;gap:8px}.secl span{display:grid;grid-template-columns:28px 1fr;align-items:center;padding:12px 14px;border-radius:var(--r-lg);background:var(--card2);font-size:18px}.secl b{font-size:15px}.secl small{grid-column:2;font-size:12.5px;color:var(--muted)}
.secok{display:flex;flex-direction:column;align-items:center;gap:6px;padding:20px 0;text-align:center}.secok i{width:48px;height:48px;border-radius:50%;background:#0B0B0C;color:#fff;display:grid;place-items:center}.secok b{font-size:17px}.secok small{font-size:13px;color:var(--muted);max-width:260px}
.attm{position:absolute;left:14px;bottom:calc(80px + var(--sb));z-index:4;display:flex;gap:8px;animation:sin .25s cubic-bezier(.2,.8,.2,1)}
.attm button{height:40px;padding:0 14px;border-radius:var(--r-pill);background:rgba(28,28,32,.86);backdrop-filter:blur(16px);color:#fff;font-size:14px;font-weight:600;display:inline-flex;align-items:center;gap:6px}.attm i{font-style:normal}
.bub.bimg{padding:4px;width:200px}.bub.bimg span{display:block;position:relative;height:130px;border-radius:18px;overflow:hidden}
.wth{display:flex;flex-direction:column;gap:8px;padding-top:10px;border-top:1px solid var(--line)}
.wtr{display:flex;gap:8px;align-items:flex-start;font-size:14px;line-height:1.35}.wtr .bgav span{width:24px;height:24px;border:0}.wtr b{font-weight:600}
.wtf{display:flex;gap:8px;align-items:center}.wtf input{flex:1;min-width:0;height:38px;padding:0 14px;border:0;border-radius:var(--r-pill);background:var(--card2);font:inherit;font-size:14px;outline:none}.wtf button{height:38px;padding:0 14px;border-radius:var(--r-pill);background:#0B0B0C;color:#fff;font-weight:600;font-size:13.5px}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
