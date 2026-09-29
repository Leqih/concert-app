import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(s.count(o),o[:90]); s=s.replace(o,n)
# icons
rep("camera:'<path","play:'<path d=\"M8 5.5v13l10.5-6.5z\"/>', clip:'<rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"4\"/><path d=\"M10 9v6l5-3z\"/>', heart:'<path d=\"M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z\"/>', sound:'<path d=\"M5 10v4h3l4 3.5v-11L8 10z\"/><path d=\"M16 9.5a3.5 3.5 0 0 1 0 5\"/>', mute:'<path d=\"M5 10v4h3l4 3.5v-11L8 10z\"/><path d=\"M16 10l4 4M20 10l-4 4\"/>', camera:'<path")
# nav: add Clips tab
rep("${it('explore','Explore','compass')}${it('crews','Chat","${it('explore','Explore','compass')}${it('clips','Clips','clip')}${it('crews','Chat")
rep("const tab=['home','explore','crews','tickets'].includes(active)?active:null;","const tab=['home','explore','clips','crews','tickets'].includes(active)?active:null;")
rep("_ap.classList.toggle('dk',['crew','me','person'].includes(state.screen));","_ap.classList.toggle('dk',['crew','me','person','clips'].includes(state.screen));")
rep("v.innerHTML={home,show,crew,crews,me,person,explore,tickets,scene,sell,search}","v.innerHTML={home,show,crew,crews,me,person,explore,tickets,scene,sell,search,clips}")
rep("  else if(a==='explore'){ state.history=[]; state.screen='explore'; render(); }","  else if(a==='explore'){ state.history=[]; state.screen='explore'; render(); }\n  else if(a==='clips'){ state.history=[]; state.screen='clips'; render(); }")
JS=r'''
// ---------- Clips: concert moments from verified ticket holders
const CAPS=['The lights dropped and the whole floor lost it','Front row, no regrets','Screamed every word with strangers who are now my crew','That encore though','Came alone, left with three new friends','Best crowd I’ve ever been in','Goosebumps from the first note','Our crew’s view from Section 105'];
function clipList(){ const base=NYC_SHOWS.filter(x=>x.img.startsWith('data:')).slice(0,8).map((x,i)=>{ const k=Math.abs(h(x.id)), p=(k+i)%8, song=songsFor(x.artist)[k%3];
    return {id:'c'+i,s:x,p,cap:CAPS[(k+i)%CAPS.length],song,likes:180+k%4200,com:12+k%260,ago:[2,5,9,14,20,26,30,41][i]+'h',sec:['Floor GA','Section 105','Balcony','Pit'][k%4]}; });
  return (state.myClips||[]).concat(base); }
const fmtK=n=>n>=1000?(n/1000).toFixed(n>=10000?0:1)+'k':''+n;
function clips(){ const L=clipList(), lk=state.clk||{}, mute=state.clMute!==false;
  return `<div class="clips" id="clv">${L.map((c,i)=>{ const p=c.me?MEP:PEOPLE[c.p], on=!!lk[c.id];
    return `<section class="clp${i===0?' act':''}" data-i="${i}" data-id="${c.id}"><div class="clm" data-act="cltap" data-v="${c.id}">${img(c.s)}</div><span class="clsh"></span><span class="clgr"></span><i class="clbig">${ic('play',40)}</i><i class="clheart">${ic('heart',96)}</i>
      <div class="clrail"><button class="clav" ${c.me?'':`data-act="person" data-v="${c.p}"`} aria-label="${p[0]}"><span>${avi(p[3])}</span>${c.me?'':`<i>${ic('plus',10)}</i>`}</button>
        <button data-act="cllike" data-v="${c.id}" aria-pressed="${on}" aria-label="Like">${ic('heart',26)}<small>${fmtK(c.likes+(on?1:0))}</small></button>
        <button data-act="clcom" data-v="${c.id}" aria-label="Comments">${ic('chat',26)}<small>${fmtK(c.com)}</small></button>
        <button data-act="toast" data-msg="Link copied" aria-label="Share">${ic('share',24)}<small>Share</small></button></div>
      <div class="clinfo"><span class="clwho"><b>${c.me?'You':p[0]}</b><em>${ic('check',10)} Was there · ${c.sec}</em><span>${c.ago}</span></span>
        <p>${esc(c.cap)}</p><span class="clsong">♪ ${esc(c.song)} · ${esc(c.s.artist)}</span>
        <button class="clshow" data-act="show" data-id="${c.s.id}"><span class="xth">${img(c.s)}</span><span><b>${esc(c.s.artist)}</b><small>${xDays(c.s.dates[0])<0?'Last night':sd(c.s.dates[0])} · ${esc(VSH(c.s.venue))}</small></span><em>Find a crew</em></button></div>
      <span class="clbar"><i></i></span></section>`; }).join('')}</div>
    <header class="clhd"><span></span><div class="clseg"><button data-act="clfeed" data-v="fy" aria-pressed="${(state.clFeed||'fy')==='fy'}">For you</button><button data-act="clfeed" data-v="fo" aria-pressed="${state.clFeed==='fo'}">Following</button></div><button class="clmute" data-act="clmute" aria-label="${mute?'Unmute':'Mute'}">${ic(mute?'mute':'sound',20)}</button></header>
    <button class="clpost" data-act="clshare" aria-label="Share a clip">${ic('camera',20)}</button>${dock('clips')}`; }
function clWatch(){ const v=document.getElementById('clv'); if(!v||v._w) return; v._w=1;
  const io=new IntersectionObserver(es=>es.forEach(e=>{ e.target.classList.toggle('act',e.intersectionRatio>.6); }),{root:v,threshold:[.6]}); v.querySelectorAll('.clp').forEach(x=>io.observe(x));
  let lt=0; v.addEventListener('click',e=>{ const m=e.target.closest('.clm'); if(!m) return; const now=Date.now(); if(now-lt<280){ const id=m.dataset.v; state.clk=state.clk||{}; if(!state.clk[id]) { state.clk[id]=true; clUpd(id); } const hs=m.parentElement.querySelector('.clheart'); hs.classList.remove('go'); void hs.offsetWidth; hs.classList.add('go'); lt=0; e.stopPropagation(); return; } lt=now; },true); }
function clUpd(id){ const b=document.querySelector(`.clp[data-id="${id}"] [data-act=cllike]`); if(!b) return; const c=clipList().find(x=>x.id===id), on=!!(state.clk||{})[id]; b.setAttribute('aria-pressed',on); b.querySelector('small').textContent=fmtK(c.likes+(on?1:0)); b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop'); }
function csSheet(){ const k=state.cs, past=A(KIT.show);
  const head=`<div class="sheetbg" data-act="csclose"></div><div class="sheet csheet" role="dialog" aria-label="Share a clip"><div class="cgrab"><i class="grab"></i><h3>Share a clip</h3><p>From a show you were at · only ticket holders can post</p></div><div class="ufb">`;
  let b=`<p class="ncl">Show</p><div class="itrow" style="border:0"><span class="uthumb">${img(past)}</span><span class="ub"><b>${esc(past.artist)}</b><span class="um">Last night · ${esc(VSH(past.venue))} · ticket verified ✓</span></span></div>
    <p class="ncl">Pick a video</p><div class="csvid">${[0,1,2].map(i=>`<button data-act="cspick" data-v="${i}" aria-pressed="${k.v===i}"><span>${img(past)}</span><em>0:${['14','22','09'][i]}</em></button>`).join('')}</div>
    <p class="ncl">Caption</p><input id="cscap" class="eptx" style="height:46px" maxlength="80" placeholder="What was the moment?" value="${esc(k.cap||'')}">`;
  return head+b+`</div><div class="uff"><button class="ufx" data-act="csclose">Cancel</button><button class="cgo new" data-act="cspost">Post clip</button></div></div>`; }
'''
i=s.index('function upSwap(anim){'); s=s[:i]+JS.lstrip()+s[i:]
rep("+(state.secO?secSheet():'')","+(state.secO?secSheet():'')+(state.cs?csSheet():'')")
rep("  state._ufAnim=false; if(state.screen==='home'){","  if(state.screen==='clips') clWatch();\n  state._ufAnim=false; if(state.screen==='home'){")
H=r'''  else if(a==='cltap'){ const sec=t.closest('.clp'); sec.classList.toggle('paused'); }
  else if(a==='cllike'){ state.clk=state.clk||{}; state.clk[v]=!state.clk[v]; clUpd(v); }
  else if(a==='clcom'){ toast('Comments open to people who were at this show'); }
  else if(a==='clmute'){ state.clMute=state.clMute===false; const b=t; b.innerHTML=ic(state.clMute!==false?'mute':'sound',20); toast(state.clMute!==false?'Muted':'Sound on'); }
  else if(a==='clfeed'){ state.clFeed=v; document.querySelectorAll('.clseg button').forEach(x=>x.setAttribute('aria-pressed',x.dataset.v===v)); const cv=document.getElementById('clv'); if(cv) cv.scrollTo({top:0,behavior:'smooth'}); if(v==='fo') toast('Clips from your buddies and crews'); }
  else if(a==='clshare'){ if(document.getElementById('psheet')) closePlus(); state.cs={v:0}; render(); }
  else if(a==='csclose'){ state.cs=null; render(); }
  else if(a==='cspick'){ const c=document.getElementById('cscap'); state.cs.cap=c?c.value:''; state.cs.v=+v; render(); }
  else if(a==='cspost'){ const c=document.getElementById('cscap'), past=A(KIT.show); state.myClips=[{id:'m'+Date.now(),me:true,p:null,s:past,cap:(c&&c.value.trim())||'Last night was unreal',song:songsFor(past.artist)[0],likes:0,com:0,ago:'now',sec:'Floor GA'}].concat(state.myClips||[]); state.cs=null; state.history=[]; state.screen='clips'; render(); toast('Clip posted · your crew gets a ping'); }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")
CSS=r'''
/* ---------- Clips */
.clips{position:absolute;inset:0;overflow-y:auto;scroll-snap-type:y mandatory;background:#000;scrollbar-width:none}.clips::-webkit-scrollbar{display:none}
.clp{position:relative;height:100%;scroll-snap-align:start;scroll-snap-stop:always;overflow:hidden;color:#fff;background:#000}
.clm{position:absolute;inset:0;overflow:hidden}
.clm img.cover{position:absolute;inset:-6%;width:112%;height:112%;object-fit:cover;animation:kb 14s ease-in-out infinite alternate;animation-play-state:paused}
.clp.act .clm img.cover{animation-play-state:running}.clp.paused .clm img.cover{animation-play-state:paused}
@keyframes kb{0%{transform:scale(1) translate(0,0)}100%{transform:scale(1.14) translate(-3%,-2%)}}
.clsh{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 48%,rgba(0,0,0,.82) 100%)}
.clgr{position:absolute;inset:0;pointer-events:none;opacity:.12;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
.clbig{position:absolute;left:50%;top:46%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;background:rgba(0,0,0,.35);backdrop-filter:blur(8px);display:grid;place-items:center;opacity:0;transform:scale(.8);transition:opacity .2s,transform .25s;pointer-events:none}
.clbig svg{fill:#fff;stroke:none;margin-left:4px}.clp.paused .clbig{opacity:1;transform:none}
.clheart{position:absolute;left:50%;top:44%;margin:-48px 0 0 -48px;pointer-events:none;opacity:0}.clheart svg{fill:#fff;stroke:none}
.clheart.go{animation:hburst .8s cubic-bezier(.2,.8,.2,1)}@keyframes hburst{0%{opacity:0;transform:scale(.3) rotate(-12deg)}25%{opacity:1;transform:scale(1.1) rotate(4deg)}60%{opacity:1;transform:scale(1)}100%{opacity:0;transform:translateY(-60px) scale(.9)}}
.clrail{position:absolute;right:10px;bottom:calc(118px + var(--sb));display:flex;flex-direction:column;align-items:center;gap:16px;z-index:2}
.clrail button{display:flex;flex-direction:column;align-items:center;gap:3px;color:#fff;filter:drop-shadow(0 1px 6px rgba(0,0,0,.4))}.clrail small{font-size:11.5px;font-weight:600}
.clrail button[aria-pressed=true] svg{fill:#fff}
.clrail button.pop svg{animation:hpop .35s cubic-bezier(.34,1.6,.5,1)}@keyframes hpop{0%{transform:scale(.6)}100%{transform:scale(1)}}
.clav{position:relative;margin-bottom:4px}.clav>span{display:block;width:44px;height:44px;border-radius:50%;overflow:hidden;border:2px solid #fff;position:relative}.clav img{width:100%;height:100%;object-fit:cover}
.clav i{position:absolute;left:50%;bottom:-8px;margin-left:-9px;width:18px;height:18px;border-radius:50%;background:#fff;color:#0B0B0C;display:grid;place-items:center}
.clinfo{position:absolute;left:14px;right:78px;bottom:calc(96px + var(--sb));z-index:2;display:flex;flex-direction:column;gap:6px}
.clwho{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px}.clwho b{font-size:15px;letter-spacing:-.02em}.clwho em{font-style:normal;height:20px;padding:0 8px;border-radius:var(--r-pill);background:rgba(255,255,255,.18);backdrop-filter:blur(8px);font-size:11px;font-weight:600;display:inline-flex;align-items:center;gap:3px}.clwho>span{opacity:.6}
.clinfo p{margin:0;font-size:15px;line-height:1.35;letter-spacing:-.01em}
.clsong{font-size:12.5px;opacity:.8}
.clshow{display:flex;align-items:center;gap:10px;margin-top:6px;padding:6px 6px 6px 6px;border-radius:var(--r-lg);background:rgba(255,255,255,.14);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);color:#fff;text-align:left}
.clshow .xth{width:40px;height:40px;border-radius:12px;position:relative}.clshow>span:nth-child(2){flex:1;min-width:0;display:flex;flex-direction:column}.clshow b{font-size:14px}.clshow small{font-size:11.5px;opacity:.7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.clshow em{font-style:normal;flex-shrink:0;height:32px;padding:0 12px;border-radius:var(--r-pill);background:#fff;color:#0B0B0C;font-size:12.5px;font-weight:700;display:inline-flex;align-items:center}
.clbar{position:absolute;left:14px;right:14px;bottom:calc(82px + var(--sb));height:2px;border-radius:2px;background:rgba(255,255,255,.25);overflow:hidden;z-index:2}.clbar i{display:block;height:100%;width:0;background:#fff}
.clp.act .clbar i{animation:clprog 14s linear infinite}.clp.paused .clbar i{animation-play-state:paused}@keyframes clprog{to{width:100%}}
.clhd{position:absolute;left:0;right:0;top:0;padding:calc(var(--st) + 6px) 14px 0;display:grid;grid-template-columns:44px 1fr 44px;align-items:center;z-index:4;pointer-events:none}
.clhd>*{pointer-events:auto}
.clseg{justify-self:center;display:flex;gap:18px}.clseg button{font-family:var(--display);font-size:17px;font-weight:700;letter-spacing:-.02em;color:rgba(255,255,255,.55);padding:6px 0;position:relative}
.clseg button[aria-pressed=true]{color:#fff}.clseg button[aria-pressed=true]::after{content:'';position:absolute;left:30%;right:30%;bottom:0;height:2px;border-radius:2px;background:#fff}
.clmute{width:40px;height:40px;border-radius:50%;background:rgba(0,0,0,.28);backdrop-filter:blur(10px);color:#fff;display:grid;place-items:center}
.clpost{position:absolute;left:14px;top:calc(var(--st) + 6px);width:40px;height:40px;border-radius:50%;background:rgba(0,0,0,.28);backdrop-filter:blur(10px);color:#fff;display:grid;place-items:center;z-index:5}
.csvid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.csvid button{position:relative;aspect-ratio:9/14;border-radius:var(--r-md);overflow:hidden;box-shadow:0 0 0 0 #0B0B0C;transition:box-shadow .2s}
.csvid button span{position:absolute;inset:0}.csvid button em{position:absolute;right:6px;bottom:6px;font-style:normal;font-size:11px;font-weight:600;color:#fff;background:rgba(0,0,0,.5);padding:1px 6px;border-radius:var(--r-pill)}
.csvid button[aria-pressed=true]{box-shadow:0 0 0 3px #0B0B0C}
.bcap .nit{padding:0 10px}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
