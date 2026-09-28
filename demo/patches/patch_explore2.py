P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
a=s.index('function explore(){'); b=s.index('\nconst MYTIX=')
NEW=r'''function xRow(c){ const left=c.n-c.f, hot=left===1;
  return `<div class="xcr"><div class="xci"><span class="xtl"><b>${esc(c.name)}</b><span class="xsc">${SCENE_EMO[c.j]} ${SCENE_LIST[c.j][0]}</span></span>
      <span class="xmt">📍 ${c.time} · ${esc(c.spot)}</span>
      <span class="xft"><span class="xav">${Array.from({length:Math.min(3,c.f)},(_,m)=>`<span>${avi(PEOPLE[(PEOPLE.indexOf(c.host)+m*3)%8][3])}</span>`).join('')}</span><span class="xdots">${Array.from({length:c.n},(_,k)=>`<i class="${k<c.f?'on':''}"></i>`).join('')}</span><em>${hot?'1 spot left':left+' spots left'}${c.rel?' · 100% showed up':''}</em></span></div>
    <button class="xjn ${hot?'hot':''}" data-act="xjoin" data-v="${c.ix}">${hot?'Last spot':'Join'}</button></div>`; }
function xGroup(cs){ const s=cs[0].s, sh=v=>v.replace('Madison Square Garden','MSG').replace('Radio City Music Hall','Radio City');
  return `<div class="xgrp"><button class="xsh" data-act="show" data-id="${s.id}"><span class="xth">${img(s)}</span><span class="xsb"><b>${esc(s.artist)}</b><small>${sd(s.dates[0])} · ${esc(sh(s.venue))}</small></span><span class="xsp">👤 ${cs[0].solo} solo</span></button>${cs.map(xRow).join('')}</div>`; }
function explore(){
  const q=(state.q||'').trim().toLowerCase(), mode=state.xmode||'crew', tag=state.xtag==null?-1:state.xtag;
  const match=t=>!q||t.toLowerCase().includes(q);
  const seg=`<div class="tseg xseg" role="tablist"><button data-act="xmode" data-v="crew" aria-selected="${mode==='crew'}">Find a crew</button><button data-act="xmode" data-v="ticket" aria-selected="${mode==='ticket'}">Find a ticket</button><span class="tsegi ${mode==='crew'?'mine':'spares'}"></span></div>`;
  const search=`<div class="pad" style="margin-top:10px"><label class="sbar">${ic('search',20)}<span hidden>Search</span><input id="xq" value="${esc(state.q||'')}" placeholder="${mode==='crew'?'Artists, venues, or people going':'Artists or venues'}" data-live="1"></label></div>`;
  let body='', sub='', chips='';
  if(mode==='crew'){
    const order=[0,1,2,4,6,7,3,5], all=xCrews();
    const L=all.filter(c=>(tag<0||c.j===tag)&&match(c.s.artist+' '+c.s.venue+' '+c.name+' '+c.host[0]));
    sub=`${L.length} crews forming in ${state.city}`;
    const solo=all.filter(c=>xDays(c.s.dates[0])<=7).reduce((n,c)=>n+c.solo,0)||23;
    chips=`<div class="hs xchips"><button class="gch" data-act="xtag" data-v="-1" aria-pressed="${tag<0}">All</button>${order.map(j=>`<button class="gch" data-act="xtag" data-v="${j}" aria-pressed="${tag===j}">${SCENE_EMO[j]} ${SCENE_LIST[j][0]}</button>`).join('')}</div>`;
    const proof=`<div class="xsolo2"><span class="xav">${[3,5,7].map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}</span><span><b>${solo} people</b> are going solo this week · every crew is ID + ticket verified</span></div>`;
    const groups=XB.map(bk=>{ const cs=L.filter(c=>xBucket(c.s.dates[0])===bk); const by=[]; cs.forEach(c=>{ let g=by.find(x=>x[0].s===c.s); if(!g){ g=[]; by.push(g); } g.push(c); }); return [bk,by]; }).filter(g=>g[1].length);
    body=proof+(groups.length?groups.map(([bk,by])=>`<p class="slab">${bk}</p>${by.slice(0,5).map(xGroup).join('')}`).join('')
      :`<div class="xempty"><b>No ${tag>=0?esc(SCENE_LIST[tag][0].toLowerCase())+' ':''}crews ${q?'match “'+esc(state.q)+'”':'yet'}</b><span>Be the first. We’ll suggest a meetup spot and time.</span><button data-act="toast" data-msg="Pick a show, set a meetup, and invite people">＋ Start the first crew</button></div>`);
  } else {
    const L=allSpares().filter(x=>match(byId[x.sid].artist+' '+byId[x.sid].venue)).sort((a,b)=>byId[a.sid].dates[0].localeCompare(byId[b.sid].dates[0]));
    const locked=SHOWS.filter(x=>LOCKED(x)&&match(x.artist+' '+x.venue)).slice(0,3);
    sub=`${L.length} spare tickets · face value + $${FEE}`;
    chips=`<div class="sprule xchips"><span><i class="eb">🔒</i>Face value + $${FEE} flat</span><span><i class="eb">👯</i>Crews get 24h first</span><span><i class="eb">↩️</i>Refund if it doesn’t arrive</span></div>`;
    const groups=XB.map(bk=>[bk,L.filter(x=>xBucket(byId[x.sid].dates[0])===bk)]).filter(g=>g[1].length);
    body=(groups.length?groups.map(([bk,xs])=>`<p class="slab">${bk}</p><div class="splist">${xs.map(x=>spareCard(x)).join('')}</div>`).join(''):`<div class="xempty"><b>No spares match</b><span>Turn on alerts and we’ll ping you when one drops.</span></div>`)
      +(locked.length?`<p class="slab">Official exchange only</p><div class="spwait">${locked.map(x=>`<div class="spwr"><span class="spwi">${img(x)}</span><span class="spwb"><b>${esc(x.artist)}</b><small>${sd(x.dates[0])} · transfers locked by the artist</small></span><a class="xfv" href="https://help.ticketmaster.com/hc/en-us/articles/9781464415249-How-does-Ticketmaster-s-Face-Value-Exchange-work" target="_blank" rel="noopener">Exchange ↗</a></div>`).join('')}</div>`:'');
  }
  return `<div class="scroll"><div style="padding-bottom:130px">
    <header class="whead"><span></span><div class="wtitle"><h1 class="sh1">Explore <span class="emo">🧭</span></h1><span class="wcity">${sub}</span></div><span></span></header>
    ${search}<div class="xstick">${seg}${chips}</div>${body}
  </div></div>${dock('explore')}`;
}
'''
s=s[:a]+NEW+s[b:]
CSS=r'''
.xstick{position:sticky;top:var(--st);z-index:6;background:var(--bg);padding:10px 0 8px;margin-top:2px}
.xstick .xseg{margin-top:0}
.xchips{margin:10px 0 0;padding:0 16px}
.xstick .sprule{margin-top:10px}
.xsolo2{display:flex;align-items:center;gap:10px;margin:6px 20px 0;font-size:12.5px;line-height:1.35;color:var(--muted);letter-spacing:-.01em}
.xsolo2 b{color:var(--text)}
.xav{display:flex;flex-shrink:0}.xav span{width:24px;height:24px;border-radius:50%;overflow:hidden;border:2px solid var(--card);margin-left:-7px;background:var(--card2)}.xav span:first-child{margin-left:0}.xav img{width:100%;height:100%;object-fit:cover;display:block}
.xsolo2 .xav span{border-color:var(--bg)}
.xgrp{margin:0 12px 10px;padding:12px 12px 4px;border-radius:24px;background:var(--card)}
.xsh{display:flex;align-items:center;gap:12px;width:100%;text-align:left;color:var(--text)}
.xth{width:48px;height:48px;border-radius:14px;overflow:hidden;flex-shrink:0;background:var(--card2)}.xth img{width:100%;height:100%;object-fit:cover;display:block}
.xsb{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.xsb b{font-size:17px;letter-spacing:-.035em;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.xsb small{font-size:12.5px;color:var(--muted)}
.xsp{flex-shrink:0;height:24px;padding:0 9px;border-radius:12px;background:var(--card2);font-size:11.5px;font-weight:600;display:inline-flex;align-items:center;white-space:nowrap;color:#3C3C40}
.xcr{display:flex;align-items:center;gap:12px;margin-top:10px;padding:10px 0 8px;border-top:1px solid var(--line)}
.xci{flex:1;min-width:0;display:flex;flex-direction:column;gap:5px}
.xtl{display:flex;align-items:baseline;gap:8px;min-width:0}.xtl b{font-size:15px;letter-spacing:-.025em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.xsc{flex-shrink:0;font-size:11.5px;font-weight:600;color:var(--muted);white-space:nowrap}
.xmt{font-size:12.5px;font-weight:600;letter-spacing:-.01em;color:#2A2A2E}
.xft{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--muted);min-width:0}
.xft em{font-style:normal;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.xdots{display:flex;gap:3px;flex-shrink:0}.xdots i{width:6px;height:6px;border-radius:50%;background:#D6D6DA}.xdots i.on{background:#0B0B0C}
.xjn{flex-shrink:0;height:34px;padding:0 16px;border-radius:17px;box-shadow:inset 0 0 0 1.5px #0B0B0C;color:#0B0B0C;background:transparent;font-weight:600;font-size:13.5px;letter-spacing:-.01em}
.xjn.hot{background:#0B0B0C;color:#fff;box-shadow:none}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
