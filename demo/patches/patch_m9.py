import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:90])
    s=s.replace(old,new)

JS=r'''
const VSH=v=>v.replace('Madison Square Garden','MSG').replace('Radio City Music Hall','Radio City').replace('Barclays Center','Barclays');
function trending(){ const c=SHOWS.filter(x=>xDays(x.dates[0])>=0&&xDays(x.dates[0])<=31).sort((a,b)=>(h(b.id)%97+(XOV[b.artist]?60:0))-(h(a.id)%97+(XOV[a.artist]?60:0))).slice(0,5);
  return c.map((x,i)=>{ const k=Math.abs(h(x.id)), song=songsFor(x.artist)[k%3];
    const T=[[`${x.artist} · ${18+k%30} crews forming`,'Hot','show',`${(1.2+(k%30)/10).toFixed(1)}k going`],
      [`${x.artist} solo-goers up ${12+k%40}% today`,'Up','show',`${40+k%300} solo`],
      [`“${song}” as the opener?`,'Talk','wall',`${60+k%400} posts`],
      [`${x.artist} · ${2+k%8} spares at face value`,'New','show',`${sd(x.dates[0])}`],
      [`Missed connection at ${VSH(x.venue)}`,'Wall','wall',`${20+k%90} posts`]][i];
    return {s:x,text:T[0],tag:T[1],act:T[2],meta:T[3]}; }); }
function trendCard(){ const L=trending(); if(!L.length) return '';
  return `<div class="xtr"><div class="xtrh"><b>Trending in ${state.city} <span class="emo">🔥</span></b><span>Updated 2 min ago</span></div>${L.map((t,i)=>`<button class="xtrr" data-act="${t.act==='wall'?'wallgo':'show'}" data-id="${t.s.id}"><em class="${i<3?'top':''}">${i+1}</em><span class="xtrt">${esc(t.text)}</span><i class="xtg ${t.tag==='Hot'?'hot':''}">${t.tag}</i></button>`).join('')}</div>`; }

const BUDDY_GO=()=>[[A('Gorillaz'),[4,7],'t3'],[A('Steve Lacy'),[5,2],null]].filter(r=>r[0]);
function buddiesGoing(){ const R=BUDDY_GO();
  return `<section class="sec pad hsec"><h2 class="h2">Your buddies are going <span class="emo">👯</span></h2><p class="sub">Easier with people you already know</p>
    <div class="wcard flush bgo">${R.map(([x,ps,tid])=>{ const inIt=tid&&thById(tid)&&TH.indexOf(thById(tid))>-1&&thById(tid).joined;
      return `<div class="bgr"><button class="bgi" data-act="show" data-id="${x.id}"><span class="xth">${img(x)}</span></button><span class="bgb"><span class="bgav">${ps.map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}</span><b>${P0(ps[0])}${ps.length>1?' and '+P0(ps[1]):''} are going</b><small>${esc(x.artist)} · ${sd(x.dates[0])} · ${esc(VSH(x.venue))}</small></span><button class="xjn" data-act="bjoin" data-id="${x.id}" data-v="${ps.join(',')}">Join them</button></div>`; }).join('')}</div></section>`; }

const WTAGS=['All','Getting there','Outfits','Setlist','Missed connections'];
function wallPosts(x){ const k=Math.abs(h(x.id)), S=songsFor(x.artist), v=VSH(x.venue), P=i=>(k+i*3)%8;
  const base=[
    {p:P(0),tag:'Getting there',t:`Anyone taking the subway from Union Square around 6? Happy to walk over together.`,m:12,l:24,r:6},
    {p:P(1),tag:'Outfits',t:`Fit check for ${x.artist} 🖤 going full black, you?`,img:1,m:34,l:81,r:14},
    {p:P(2),tag:'Setlist',t:`Calling it now: “${S[0]}” opens, “${S[2]}” for the encore.`,m:58,l:132,r:41},
    {p:P(3),tag:'Missed connections',t:`To the person in the red jacket who shared their water in the GA line at ${v}, thank you. Hope you had the best night.`,m:95,l:57,r:3,mc:true},
    {p:P(4),tag:'Getting there',t:`Bag policy is clear bags only, small clutch is fine. Learned that the hard way last time.`,m:140,l:203,r:19}];
  return (state.wall&&state.wall[x.id]||[]).concat(base).map((o,i)=>({...o,id:x.id+'-w'+i})); }
function hasTix(x){ return MYTIX().some(r=>r[0]===x)||!!(state.claimed&&state.claimed[x.id]); }
function wallView(x){ const tag=state.wtag||'All', L=wallPosts(x).filter(o=>(tag==='All'||o.tag===tag)&&!(o.p!=null&&(state.blocked||{})[o.p])), lk=state.wlk||{}, me=hasTix(x);
  return `<div id="wall"><h2 class="h2" style="font-size:24px;text-align:center;margin-top:14px">Show wall <span class="emo">🧱</span></h2><p class="note" style="margin:-4px 0 4px">Only people with a ticket to this show can post</p>
    <div class="hs wtg">${WTAGS.map(t=>`<button class="gch" data-act="wtag" data-v="${t}" aria-pressed="${tag===t}">${t}</button>`).join('')}</div>
    ${me?`<form class="wcomp2" onsubmit="return wallPost(event,'${x.id}')"><span class="bgav"><span>${avi(MEP[3])}</span></span><label for="wq" hidden>Post</label><input id="wq" placeholder="Post to the ${esc(x.artist)} wall" autocomplete="off"><button type="submit">Post</button></form>`
      :`<div class="wlock"><span>🎟️</span><span><b>Read-only for now</b><small>Claim a spare or import your ticket to post</small></span><button data-act="toast" data-msg="Import a ticket from email or a screenshot">Add ticket</button></div>`}
    ${L.map(o=>{ const p=o.me?MEP:PEOPLE[o.p], liked=!!lk[o.id];
      return `<article class="wp"><div class="wph"><button class="bgav" ${o.me?'':`data-act="person" data-v="${o.p}"`} aria-label="${p[0]}"><span>${avi(p[3])}</span></button><span class="wpn"><b>${o.me?'You':p[0]}</b><small>${ic('check',10)} Ticket holder · ${o.m<60?o.m+' min':Math.round(o.m/60)+' h'} ago</small></span><i class="wpt">${o.tag}</i></div>
        <p>${esc(o.t)}</p>${o.img?`<span class="wpi">${img(x)}</span>`:''}
        <div class="wpf"><button data-act="wlike" data-v="${o.id}" aria-pressed="${liked}">${liked?'♥':'♡'} ${o.l+(liked?1:0)}</button><button data-act="toast" data-msg="Replies open in the full thread">💬 ${o.r}</button>${o.me?'':o.mc?`<button class="wme" data-act="wmc" data-v="${o.p}">That’s me 👋</button>`:`<button class="wme" data-act="dm" data-v="${o.p}">Say hi</button>`}</div></article>`; }).join('')||`<p class="note">Nothing here yet. Be the first to post.</p>`}</div>`; }
function wallPost(e,sid){ e.preventDefault(); const i=document.getElementById('wq'), v=i.value.trim(); if(!v) return false; state.wall=state.wall||{}; (state.wall[sid]=state.wall[sid]||[]).unshift({me:true,p:null,tag:state.wtag&&state.wtag!=='All'?state.wtag:'Getting there',t:v,m:0,l:0,r:0}); render(); toast('Posted to the wall'); setTimeout(()=>{ const w=document.getElementById('wall'); w&&w.scrollIntoView({block:'start'}); },30); return false; }
'''
i=s.index('function home(){'); s=s[:i]+JS.lstrip()+s[i:]

# explore trending
rep("body=proof+(groups.length?", "body=proof+(tag<0&&!q?trendCard():'')+(groups.length?")
# home buddies going: after drop section
rep('''      <div class="wcard wcomp flush" id="dropcard">${dropCard()}</div>
    </section>
''','''      <div class="wcard wcomp flush" id="dropcard">${dropCard()}</div>
    </section>
${state.city==='New York'?buddiesGoing():''}
''')
# show page wall + looking count
rep('''<p class="note" style="margin:0">Crews cap at 8 · when one fills, we open the next</p>''',
    '''<p class="note" style="margin:0">Crews cap at 8 · when one fills, we open the next</p>
      ${wallView(s)}''')
rep("${6+h(s.id)%60} looking for a buddy</span>","${6+h(s.id)%60+(ME.looking?1:0)} looking for a buddy${ME.looking?' · incl. you':''}</span>")
# scene start button
rep('''<button class="wpill big" data-act="toast" data-msg="Pick a show, set a meetup, and tag it ${esc(sc[0])}">''',
    '''<button class="wpill big" data-act="ncopen" data-id="${shows[0].id}" data-j="${i}">''')
# plus menu find a plus one
rep("['🙋','Find a plus one','Let crews find you','toast','Tell your crews you’re looking']",
    "['🙋',ME.looking?'You’re visible':'Find a plus one',ME.looking?'Crews can invite you · tap to hide':'Let crews find you','lookon','']")
# ncopen reads preset vibe
rep("state.nc={sid:id||(A('Harry Styles')||SHOWS[0]).id,j:0,","state.nc={sid:id||(A('Harry Styles')||SHOWS[0]).id,j:t.dataset.j!=null?+t.dataset.j:0,")
H=r'''  else if(a==='wallgo'){ go('show',id); setTimeout(()=>{ const w=document.getElementById('wall'); w&&w.scrollIntoView({block:'start'}); },60); }
  else if(a==='wtag'){ state.wtag=v; const sc=document.querySelector('.scroll'), y=sc&&sc.scrollTop; render(); const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; }
  else if(a==='wlike'){ state.wlk=state.wlk||{}; state.wlk[v]=!state.wlk[v]; const sc=document.querySelector('.scroll'), y=sc&&sc.scrollTop; render(); const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; }
  else if(a==='wmc'){ toast(`We’ll let ${P0(+v)} know · you can chat only if they say yes`); }
  else if(a==='lookon'){ ME.looking=!ME.looking; state.psheet=false; render(); toast(ME.looking?'You’re visible · crews for your saved shows can invite you':'Hidden · crews won’t see you as looking'); }
  else if(a==='bjoin'){ const x=byId[id]||A('Gorillaz'), ps=v.split(',').map(Number); let tt=TH.find(q=>q.k==='crew'&&q.show===x.artist&&ps.every(k=>q.who.includes(k)));
    if(!tt){ tt={id:'t'+(++TSEQ),k:'crew',show:x.artist,title:'Buddies',long:`${x.artist} with ${P0(ps[0])} and ${P0(ps[1])}`,host:ps[0],who:ps.slice(),cap:6,un:0,ts:++TSEQ,plan:['6:30 PM',XSPOT[Math.abs(h(x.id))%XSPOT.length]],msgs:[{d:'in',p:ps[0],t:`Oh nice, you’re coming too? 🙌`,time:nowT()}],replies:[[ps[1],'Finally, the whole gang']]}; TH.unshift(tt); }
    tt.msgs.push({d:'sys',t:`You joined ${P0(ps[0])} and ${P0(ps[1])}`}); openThread(tt); }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")

CSS=r'''
.xtr{margin:14px 12px 4px;padding:12px 14px 6px;border-radius:24px;background:var(--card)}
.xtrh{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:4px}.xtrh b{font-family:var(--display);font-size:17px;letter-spacing:-.03em}.xtrh span{font-size:11.5px;color:var(--muted)}
.xtrr{display:flex;align-items:center;gap:12px;width:100%;height:42px;text-align:left;color:var(--text);border-top:1px solid var(--line)}.xtrr:first-of-type{border-top:0}
.xtrr em{font-style:normal;width:18px;text-align:center;font-family:var(--display);font-weight:800;font-size:16px;color:#A3A3A8}.xtrr em.top{color:#0B0B0C}
.xtrt{flex:1;min-width:0;font-size:14px;font-weight:500;letter-spacing:-.015em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.xtg{font-style:normal;flex-shrink:0;height:20px;padding:0 8px;border-radius:10px;background:var(--card2);font-size:11px;font-weight:600;display:inline-flex;align-items:center;color:#3C3C40}.xtg.hot{background:#0B0B0C;color:#fff}
.bgo{padding:4px 14px}
.bgr{display:flex;align-items:center;gap:12px;padding:12px 0;border-top:1px solid var(--line)}.bgr:first-child{border-top:0}
.bgi .xth{display:block;position:relative}
.bgb{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}.bgb b{font-size:15px;letter-spacing:-.02em}.bgb small{font-size:12.5px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bgav{display:flex;flex-shrink:0}.bgav span{width:22px;height:22px;border-radius:50%;overflow:hidden;position:relative;border:2px solid var(--card);margin-left:-6px;background:var(--card2)}.bgav span:first-child{margin-left:0}.bgav img{width:100%;height:100%;object-fit:cover;display:block}
.wtg{margin:8px -16px 0;padding:0 16px}
.wcomp2{display:flex;align-items:center;gap:10px;padding:8px 8px 8px 12px;border-radius:18px;background:var(--card)}.wcomp2 .bgav span{width:30px;height:30px}
.wcomp2 input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:15px;outline:none;color:var(--text)}
.wcomp2 button{height:34px;padding:0 14px;border-radius:17px;background:#0B0B0C;color:#fff;font-weight:600;font-size:13.5px}
.wlock{display:flex;align-items:center;gap:12px;padding:12px 12px 12px 14px;border-radius:18px;background:var(--card)}.wlock>span:first-child{font-size:20px}
.wlock span:nth-child(2){flex:1;display:flex;flex-direction:column}.wlock b{font-size:14.5px}.wlock small{font-size:12.5px;color:var(--muted)}
.wlock button{height:34px;padding:0 12px;border-radius:17px;box-shadow:inset 0 0 0 1.5px #0B0B0C;font-weight:600;font-size:13px}
.wp{padding:14px;border-radius:22px;background:var(--card);display:flex;flex-direction:column;gap:10px}
.wph{display:flex;align-items:center;gap:10px}.wph .bgav span{width:34px;height:34px;border:0}
.wpn{flex:1;min-width:0;display:flex;flex-direction:column}.wpn b{font-size:14.5px;letter-spacing:-.02em}.wpn small{font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:3px}
.wpt{font-style:normal;height:22px;padding:0 9px;border-radius:11px;background:var(--card2);font-size:11px;font-weight:600;display:inline-flex;align-items:center;color:#3C3C40;white-space:nowrap}
.wp p{margin:0;font-size:15px;line-height:1.45;letter-spacing:-.01em}
.wpi{display:block;position:relative;height:170px;border-radius:16px;overflow:hidden}
.wpf{display:flex;align-items:center;gap:6px}.wpf button{height:32px;padding:0 12px;border-radius:16px;background:var(--card2);font-size:13px;font-weight:600;color:var(--text)}
.wpf button[aria-pressed=true]{background:#0B0B0C;color:#fff}.wpf .wme{margin-left:auto;background:transparent;box-shadow:inset 0 0 0 1.5px #0B0B0C}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
