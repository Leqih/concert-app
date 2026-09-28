P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
a=s.index('function explore(){'); b=s.index('\nconst MYTIX=')
NEW=r'''const XSPOT=['Box office','Main entrance','Bar by Section 105','Merch stand','Gate B line'];
const XDIN=['Ramen across the street','Taco spot on 8th Ave','Pizza by the venue'];
function xCrews(){ const out=[];
  SHOWS.slice().sort((a,b)=>a.dates[0].localeCompare(b.dates[0])).forEach(s=>{ const k0=h(s.id), nc=1+k0%2;
    for(let k=0;k<nc;k++){ const j=(k0+k*3)%8, host=PEOPLE[(k0+k*5)%8], n=4+(k0+k)%3, f=1+((k0>>k)%(n-1));
      out.push({s,j,name:SCENE_LIST[j][2][(k0+k)%4],host,n,f,time:['5:45 PM','6:00 PM','6:15 PM','6:30 PM'][(k0+k)%4],spot:j===2?XDIN[(k0+k)%3]:XSPOT[(k0+k)%5],wo:j===7,rel:(k0+k)%3!==0,solo:8+(k0>>2)%30}); } });
  return out; }
const xDays=d=>Math.round((Date.UTC(...d.split('-').map((v,i)=>i===1?v-1:+v))-Date.UTC(2026,8,27))/864e5);
const xBucket=d=>{ const n=xDays(d); return n<=1?'Tonight & tomorrow':n<=7?'This week':n<=31?'Next few weeks':'Later'; };
const XB=['Tonight & tomorrow','This week','Next few weeks','Later'];
function xCard(c){ const left=c.n-c.f, sh=v=>v.replace('Madison Square Garden','MSG').replace('Radio City Music Hall','Radio City');
  return `<button class="screw xc" data-act="${c.wo?'wcrew':'crew'}" data-id="${c.s.id}"><span class="scimg">${img(c.s)}</span>
    <span class="scb"><b>${esc(c.name)} <span class="emo">${SCENE_EMO[c.j]}</span></b><span class="scm">${esc(c.s.artist)} · ${sd(c.s.dates[0])} · ${esc(sh(c.s.venue))}</span>
      <span class="xmeet">📍 ${c.time} · ${esc(c.spot)}</span>
      <span class="scf"><span class="schost">${avi(c.host[3])}</span><span>${c.host[0]}${c.f>1?' + '+(c.f-1):''} · ${left} of ${c.n} spots left</span></span>
      <span class="xtags"><i>${ic('check',11)} Verified</i>${c.wo?'<i>Women only</i>':''}${c.rel?'<i>Everyone showed up last time</i>':''}</span></span>
    <span class="scjoin">Join</span></button>`; }
function explore(){
  const q=(state.q||'').trim().toLowerCase(), mode=state.xmode||'crew', tag=state.xtag==null?-1:state.xtag;
  const match=t=>!q||t.toLowerCase().includes(q);
  const seg=`<div class="tseg xseg" role="tablist"><button data-act="xmode" data-v="crew" aria-selected="${mode==='crew'}">Find a crew</button><button data-act="xmode" data-v="ticket" aria-selected="${mode==='ticket'}">Find a ticket</button><span class="tsegi ${mode==='crew'?'mine':'spares'}"></span></div>`;
  const search=`<div class="pad" style="margin-top:12px"><label class="sbar">${ic('search',20)}<span hidden>Search</span><input id="xq" value="${esc(state.q||'')}" placeholder="${mode==='crew'?'Artists, venues, or people going':'Artists or venues'}" data-live="1"></label></div>`;
  let body='', sub='';
  if(mode==='crew'){
    const order=[0,1,2,4,6,7,3,5];
    const L=xCrews().filter(c=>(tag<0||c.j===tag)&&match(c.s.artist+' '+c.s.venue+' '+c.name+' '+c.host[0]));
    sub=`${L.length} crews forming in ${state.city}`;
    const tonight=xCrews().filter(c=>xDays(c.s.dates[0])<=1), solo=tonight.reduce((n,c)=>n+c.solo,0)||23;
    const chips=`<div class="pad"><div class="hs" style="margin-top:12px"><button class="gch" data-act="xtag" data-v="-1" aria-pressed="${tag<0}">All</button>${order.map(j=>`<button class="gch" data-act="xtag" data-v="${j}" aria-pressed="${tag===j}">${SCENE_EMO[j]} ${SCENE_LIST[j][0]}</button>`).join('')}</div></div>`;
    const proof=`<div class="xsolo"><span class="mreqav">${[3,5,7,1].map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}</span><span><b>${solo} people</b> in ${state.city} are going to a show alone this week. You won’t be the only one.</span></div>`;
    const groups=XB.map(bk=>[bk,L.filter(c=>xBucket(c.s.dates[0])===bk)]).filter(g=>g[1].length);
    body=chips+(tag<0&&!q?proof:'')+(groups.length?groups.map(([bk,cs])=>`<p class="slab">${bk}</p>${cs.slice(0,6).map(xCard).join('')}`).join('')
      :`<div class="xempty"><b>No ${tag>=0?esc(SCENE_LIST[tag][0].toLowerCase())+' ':''}crews ${q?'match “'+esc(state.q)+'”':'yet'}</b><span>Be the first. We’ll suggest a meetup spot and time.</span><button data-act="toast" data-msg="Pick a show, set a meetup, and invite people">＋ Start the first crew</button></div>`);
  } else {
    const L=allSpares().filter(x=>match(byId[x.sid].artist+' '+byId[x.sid].venue)).sort((a,b)=>byId[a.sid].dates[0].localeCompare(byId[b.sid].dates[0]));
    const locked=SHOWS.filter(x=>LOCKED(x)&&match(x.artist+' '+x.venue)).slice(0,3);
    sub=`${L.length} spare tickets · face value + $${FEE}`;
    const groups=XB.map(bk=>[bk,L.filter(x=>xBucket(byId[x.sid].dates[0])===bk)]).filter(g=>g[1].length);
    body=`<div class="sprule" style="margin-top:12px"><span><i class="eb">🔒</i>Face value + $${FEE} flat</span><span><i class="eb">👯</i>Crews get 24h first</span><span><i class="eb">↩️</i>Refund if it doesn’t arrive</span></div>`
      +(groups.length?groups.map(([bk,xs])=>`<p class="slab">${bk}</p><div class="splist">${xs.map(x=>spareCard(x)).join('')}</div>`).join(''):`<div class="xempty"><b>No spares match</b><span>Turn on alerts and we’ll ping you when one drops.</span></div>`)
      +(locked.length?`<p class="slab">Official exchange only</p><div class="spwait">${locked.map(x=>`<div class="spwr"><span class="spwi">${img(x)}</span><span class="spwb"><b>${esc(x.artist)}</b><small>${sd(x.dates[0])} · transfers locked by the artist</small></span><a class="xfv" href="https://help.ticketmaster.com/hc/en-us/articles/9781464415249-How-does-Ticketmaster-s-Face-Value-Exchange-work" target="_blank" rel="noopener">Exchange ↗</a></div>`).join('')}</div>`:'');
  }
  return `<div class="scroll"><div style="padding-bottom:130px">
    <header class="whead"><span></span><div class="wtitle"><h1>Explore</h1><span class="wcity">${sub}</span></div><span></span></header>
    ${seg}${search}${body}
  </div></div>${dock('explore')}`;
}
'''
s=s[:a]+NEW+s[b:]
# handlers
old="  if(a==='show') go('show',id);\n"
assert s.count(old)==1
s=s.replace(old,old+"  else if(a==='xmode'){ state.xmode=v; state.q=''; render(); }\n  else if(a==='xtag'){ state.xtag=+v<0?null:+v; render(); }\n")
CSS=r'''
.xseg{margin-top:12px}
.xc{align-items:flex-start}
.xc .scimg{margin-top:2px}
.xmeet{display:block;font-size:12.5px;font-weight:600;margin-top:6px;letter-spacing:-.01em}
.xtags{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px}
.xtags i{font-style:normal;height:20px;padding:0 8px;border-radius:10px;background:var(--card2);font-size:11px;font-weight:600;display:inline-flex;align-items:center;gap:3px;color:#3C3C40}
.xc .scjoin{align-self:center}
.xsolo{display:flex;align-items:center;gap:12px;margin:14px 12px 0;padding:12px 14px;border-radius:18px;background:#0B0B0C;color:#fff;font-size:13.5px;line-height:1.35;letter-spacing:-.01em}
.xsolo b{font-weight:700}
.xempty{margin:16px 12px 0;padding:22px 18px;border-radius:20px;background:var(--card);display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}
.xempty b{font-size:16px;letter-spacing:-.02em}.xempty span{font-size:13.5px;color:var(--muted)}
.xempty button{margin-top:8px;height:40px;padding:0 18px;border-radius:20px;background:#0B0B0C;color:#fff;font-weight:600;font-size:14px}
.xfv{flex-shrink:0;height:32px;padding:0 12px;border-radius:16px;background:#0B0B0C;color:#fff;font-size:12.5px;font-weight:600;display:inline-flex;align-items:center;text-decoration:none}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
