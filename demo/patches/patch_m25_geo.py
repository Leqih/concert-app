import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
a=s.index('function csSheet(){'); b=s.index('function upSwap(anim){')
s=s[:a]+r'''const CSVID=[{geo:'Radio City Music Hall',d:'2026-09-29',len:'0:14'},{geo:'Radio City Music Hall',d:'2026-09-29',len:'0:22'},{geo:null,d:null,len:'0:09'}];
const VENUES=()=>[...new Set(SHOWS.map(x=>x.venue))].slice(0,8);
function csShows(v){ return SHOWS.filter(x=>x.venue===v).sort((a,b)=>Math.abs(xDays(a.dates[0])+1)-Math.abs(xDays(b.dates[0])+1)); }
function csSheet(){ const k=state.cs, vid=CSVID[k.v], loc=k.loc, sh=loc?csShows(loc):[], sel=k.sid?byId[k.sid]:sh[0], thumb=A(KIT.show);
  const head=`<div class="sheetbg" data-act="csclose"></div><div class="sheet csheet ufs" role="dialog" aria-label="Share a clip"><div class="cgrab"><i class="grab"></i><h3>Share a clip</h3><p>Every clip carries the venue it was filmed at</p></div><div class="ufb">`;
  let b=`<p class="ncl">Pick a video</p><div class="csvid">${CSVID.map((x,i)=>`<button data-act="cspick" data-v="${i}" aria-pressed="${k.v===i}"><span>${img(thumb)}</span>${x.geo?`<i class="csgeo">${ic('pin',10)}</i>`:''}<em>${x.len}</em></button>`).join('')}</div>
    <p class="ncl">Location <em class="csreq">Required</em></p>`;
  if(k.pickLoc) b+=`<div class="cslocs">${VENUES().map(v=>`<button class="itrow" data-act="csloc" data-v="${esc(v)}">${ic('pin',16)}<span class="ub"><b>${esc(VSH(v))}</b><span class="um">${esc(v)}</span></span>${ic('right',14)}</button>`).join('')}</div>`;
  else if(loc) b+=`<div class="csloc on">${ic('pin',18)}<span class="ub"><b>${esc(VSH(loc))}</b><span class="um">${k.src==='geo'?'From your video’s location · On-site':'Tagged by you'}</span></span><button class="ufx" data-act="csedit">Change</button></div>`;
  else b+=`<button class="csloc" data-act="csedit">${ic('pin',18)}<span class="ub"><b>Add the venue</b><span class="um">This video has no location · pick where you filmed it</span></span>${ic('right',14)}</button>`;
  if(loc&&!k.pickLoc&&sh.length) b+=`<p class="ncl">Show</p>${sh.length>1?`<div class="ncv">${sh.slice(0,4).map(x=>`<button class="gch" data-act="csshow" data-id="${x.id}" aria-pressed="${sel===x}">${esc(x.artist)} · ${sd(x.dates[0])}</button>`).join('')}</div>`:`<div class="itrow" style="border:0"><span class="uthumb">${img(sel)}</span><span class="ub"><b>${esc(sel.artist)}</b><span class="um">${sd(sel.dates[0])} · matched by venue and date</span></span></div>`}`;
  b+=`<p class="ncl">Caption</p><input id="cscap" class="eptx" style="height:46px" maxlength="80" placeholder="What was the moment?" value="${esc(k.cap||'')}">`;
  const ok=!!loc&&!k.pickLoc;
  return head+b+`</div><div class="uff"><button class="ufx" data-act="csclose">Cancel</button><button class="cgo new" data-act="cspost" ${ok?'':'disabled'}>${ok?'Post clip':'Add a location to post'}</button></div></div>`; }
'''+s[b:]
rep("else if(a==='clshare'){ if(document.getElementById('psheet')) closePlus(); state.cs={v:0}; render(); }",
    "else if(a==='clshare'){ if(document.getElementById('psheet')) closePlus(); state.cs={v:0,loc:CSVID[0].geo,src:'geo'}; render(); }")
i=s.index("  else if(a==='cspick'){"); j=s.index('\n',i)
s=s[:i]+"  else if(a==='cspick'){ const c=document.getElementById('cscap'), vd=CSVID[+v]; state.cs={v:+v,cap:c?c.value:'',loc:vd.geo,src:vd.geo?'geo':null}; render(); }\n  else if(a==='csedit'){ const c=document.getElementById('cscap'); state.cs.cap=c?c.value:''; state.cs.pickLoc=true; render(); }\n  else if(a==='csloc'){ state.cs.loc=v; state.cs.src='manual'; state.cs.pickLoc=false; state.cs.sid=null; render(); }\n  else if(a==='csshow'){ const c=document.getElementById('cscap'); state.cs.cap=c?c.value:''; state.cs.sid=id; render(); }"+s[j:]
i=s.index("  else if(a==='cspost'){"); j=s.index('\n',i)
s=s[:i]+"  else if(a==='cspost'){ const k=state.cs; if(!k.loc) return; const c=document.getElementById('cscap'), sh=csShows(k.loc), sel=k.sid?byId[k.sid]:(sh[0]||A(KIT.show)); state.myClips=[{id:'m'+Date.now(),me:true,p:null,s:sel,cap:(c&&c.value.trim())||'What a night',song:songsFor(sel.artist)[0],likes:0,com:0,ago:'now',loc:k.loc,onsite:k.src==='geo'}].concat(state.myClips||[]); state.cs=null; state.history=[]; state.screen='clips'; state.clY=0; render(); toast('Clip posted · tagged at '+VSH(k.loc)); }"+s[j:]
# clip overlay: location tag instead of seat
rep('<em>${ic(\'check\',10)} Was there · ${c.sec}</em>','<em class="clloc">${ic(\'pin\',10)} ${esc(VSH(c.loc||c.s.venue))}${(c.onsite!==false)?\' · On-site\':\' · Tagged\'}</em>')
# show wall: anyone can post
rep("${me?`<form class=\"wcomp2\"","${true?`<form class=\"wcomp2\"")
rep('<p class="sub" style="margin:-6px 0 2px">Only people with a ticket to this show can post</p>','<p class="sub" style="margin:-6px 0 2px">Plans, fits and setlist talk for this show</p>')
CSS=r'''
.csreq{font-style:normal;float:right;letter-spacing:0;text-transform:none;font-weight:600;color:#0B0B0C}
.csgeo{position:absolute;left:6px;top:6px;width:20px;height:20px;border-radius:50%;background:#fff;color:#0B0B0C;display:grid;place-items:center}
.csloc{display:flex;align-items:center;gap:12px;width:100%;padding:12px 14px;border-radius:var(--r-lg);background:var(--card2);text-align:left;color:var(--text);box-shadow:inset 0 0 0 1.5px transparent}
button.csloc{box-shadow:inset 0 0 0 1.5px #0B0B0C;background:transparent}
.csloc .ub b{font-size:15px}.csloc .ufx{height:auto;font-size:13.5px}
.cslocs{display:flex;flex-direction:column}.cslocs .itrow{gap:10px}
.clloc svg{margin-right:1px}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
