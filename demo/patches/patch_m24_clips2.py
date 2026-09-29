import os,re
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(s.count(o),o[:90]); s=s.replace(o,n)
# ---- + menu: star becomes Share a clip, pill removed
rep('''  <button class="pk sh sp" data-act="clshare"><span class="shl"><b>Share a clip</b></span></button>\n''','')
rep('''<button class="pk sh st${on?' on':''}" data-act="lookon" role="switch" aria-checked="${on}">''','''<button class="pk sh st" data-act="clshare">''')
rep('''<span class="shl"><b>Find a +1</b><small>${on?'Visible':'Hidden'}</small></span></button>`; }''','''<span class="shl"><b>Share a clip</b><small>From last night</small></span></button>`; }''')
rep("const order=['sc','sq','st','sp'], G=4200","const order=['sc','sq','st'], G=4200")
# ---- Find a +1 moves to profile (next to Edit)
rep('''mine?`<button class="nb" data-act="epopen" aria-label="Edit profile" style="width:auto;padding:0 16px;font-size:14px;font-weight:600;color:#fff">Edit</button>`''',
    '''mine?`<span class="pvr"><button class="nb pvlook${ME.looking?' on':''}" data-act="lookon" role="switch" aria-checked="${!!ME.looking}" style="width:auto;padding:0 14px;font-size:13.5px;font-weight:600;color:#fff"><i></i>${ME.looking?'Open to invites':'Find a +1'}</button><button class="nb" data-act="epopen" aria-label="Edit profile" style="width:auto;padding:0 16px;font-size:14px;font-weight:600;color:#fff">Edit</button></span>`''')
i=s.index("else if(a==='lookon'){"); j=s.index('\n',i)
s=s[:i]+"else if(a==='lookon'){ ME.looking=!ME.looking; if(state.screen==='me'){ const sc=document.querySelector('.scroll'),y=sc&&sc.scrollTop; render(); const n=document.querySelector('.scroll'); if(n) n.scrollTop=y; } toast(ME.looking?'You’re open to invites · crews for your saved shows can reach you':'Hidden · crews won’t see you as looking'); }"+s[j:]
# ---- Clips: following filter, disc + marquee, swipe hint, comments
rep("function clips(){ const L=clipList(),","function clips(){ const L0=clipList(), L=state.clFeed==='fo'?L0.filter(c=>c.me||BUD[c.p]||[1,3,4,7].includes(c.p)):L0,")
rep('<span class="clsong">♪ ${esc(c.song)} · ${esc(c.s.artist)}</span>','<span class="clsong"><span class="clmq"><i>♪ ${esc(c.song)} · ${esc(c.s.artist)}&nbsp;&nbsp;&nbsp;♪ ${esc(c.song)} · ${esc(c.s.artist)}&nbsp;&nbsp;&nbsp;</i></span></span>')
rep('<span class="clbar"><i></i></span></section>`; }).join(\'\')}</div>','<span class="clbar"><i></i></span><span class="cldisc">${img(c.s)}</span><span class="cldur">0:${[14,22,31,09,18,26,12,40][i%8]}</span></section>`; }).join(\'\')}${state.clSeen?\'\':`<div class="clhint">${ic(\'chev\',18)}<span>Swipe up</span></div>`}</div>')
rep("  else if(a==='clcom'){ toast('Comments open to people who were at this show'); }","  else if(a==='clcom'){ state.cmt={id:v}; render(); }\n  else if(a==='cmclose'){ state.cmt=null; render(); }\n  else if(a==='cmlike'){ state.cml=state.cml||{}; state.cml[v]=!state.cml[v]; render(); }")
rep("  if(state.screen==='clips') clWatch();","  if(state.screen==='clips'){ clWatch(); const cv=document.getElementById('clv'); if(cv&&!state.clSeen){ cv.addEventListener('scroll',()=>{ if(!state.clSeen){ state.clSeen=true; const hn=document.querySelector('.clhint'); hn&&hn.remove(); } },{once:true,passive:true}); } }")
# re-render keeps scroll position of feed
rep("function clWatch(){ const v=document.getElementById('clv'); if(!v||v._w) return; v._w=1;","function clWatch(){ const v=document.getElementById('clv'); if(!v||v._w) return; v._w=1; if(state.clY) v.scrollTop=state.clY; v.addEventListener('scroll',()=>{ state.clY=v.scrollTop; },{passive:true});")
rep("else if(a==='clfeed'){ state.clFeed=v; document.querySelectorAll('.clseg button').forEach(x=>x.setAttribute('aria-pressed',x.dataset.v===v)); const cv=document.getElementById('clv'); if(cv) cv.scrollTo({top:0,behavior:'smooth'}); if(v==='fo') toast('Clips from your buddies and crews'); }",
    "else if(a==='clfeed'){ state.clFeed=v; state.clY=0; state.clSeen=true; render(); }")
JS=r'''
function cmSheet(){ const c=clipList().find(x=>x.id===state.cmt.id); if(!c) return ''; const k=Math.abs(h(c.id+'m')), lk=state.cml||{};
  const T=['That encore was insane','I was two rows behind you!!','The crowd sang louder than the band','Same crew next show?','Goosebumps rewatching this','Where were you standing?'];
  const R=[0,1,2,3,4].map(i=>({id:c.id+'-'+i,p:(k+i*3)%8,t:T[(k+i)%T.length],l:3+((k>>i)%60),ago:(i+1)*7+'m'})).concat((state.cmMine||{})[c.id]||[]);
  return `<div class="sheetbg" data-act="cmclose"></div><div class="sheet csheet cms" role="dialog" aria-label="Comments"><div class="cgrab"><i class="grab"></i><h3>${c.com+((state.cmMine||{})[c.id]||[]).length} comments</h3><p>Only people who were at ${esc(c.s.artist)} can comment</p></div>
  <div class="ufb">${R.map(r=>{ const p=r.me?MEP:PEOPLE[r.p], on=!!lk[r.id]; return `<div class="cmr"><span class="bgav"><span>${avi(p[3])}</span></span><span class="cmb"><b>${r.me?'You':p[0]} <em>${ic('check',9)} Was there</em></b><span>${esc(r.t)}</span><small>${r.ago}</small></span><button class="cml" data-act="cmlike" data-v="${r.id}" aria-pressed="${on}">${ic('heart',16)}<small>${r.l+(on?1:0)}</small></button></div>`; }).join('')}</div>
  <form class="wtf cmf" onsubmit="return cmPost(event,'${c.id}')"><span class="bgav"><span>${avi(MEP[3])}</span></span><label hidden for="cmin">Comment</label><input id="cmin" placeholder="Add a comment" autocomplete="off"><button type="submit">Post</button></form></div>`; }
function cmPost(e,id){ e.preventDefault(); const i=document.getElementById('cmin'), v=i.value.trim(); if(!v) return false; state.cmMine=state.cmMine||{}; (state.cmMine[id]=state.cmMine[id]||[]).push({id:id+'-me'+Date.now(),me:true,t:v,l:0,ago:'now'}); render(); const b=document.querySelector('.cms .ufb'); if(b) b.scrollTop=b.scrollHeight; return false; }
'''
i=s.index('function csSheet(){'); s=s[:i]+JS.lstrip()+s[i:]
rep("+(state.cs?csSheet():'')","+(state.cs?csSheet():'')+(state.cmt?cmSheet():'')")
CSS=r'''
.clsong{display:block;width:170px;overflow:hidden;-webkit-mask:linear-gradient(90deg,#000 80%,transparent);mask:linear-gradient(90deg,#000 80%,transparent)}
.clmq{display:inline-block;white-space:nowrap}.clmq i{font-style:normal;display:inline-block;animation:mq 9s linear infinite;animation-play-state:paused}
.clp.act .clmq i{animation-play-state:running}.clp.paused .clmq i{animation-play-state:paused}@keyframes mq{to{transform:translateX(-50%)}}
.cldisc{position:absolute;right:12px;bottom:calc(98px + var(--sb));width:40px;height:40px;border-radius:50%;overflow:hidden;z-index:2;box-shadow:0 0 0 6px rgba(20,20,22,.85);animation:spin 5s linear infinite;animation-play-state:paused}
.cldisc::after{content:'';position:absolute;left:50%;top:50%;width:8px;height:8px;margin:-4px;border-radius:50%;background:#141416}
.clp.act .cldisc{animation-play-state:running}.clp.paused .cldisc{animation-play-state:paused}
.clrail{bottom:calc(160px + var(--sb))}
.clbar{transition:height .2s}.clp.paused .clbar{height:4px}
.cldur{position:absolute;right:14px;bottom:calc(88px + var(--sb));font-size:11px;font-weight:600;opacity:0;transition:opacity .2s;z-index:2}.clp.paused .cldur{opacity:.85}
.clp.paused .cldisc{opacity:.9}
.clhint{position:absolute;left:50%;bottom:calc(150px + var(--sb));transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:2px;color:#fff;font-size:12px;font-weight:600;z-index:3;pointer-events:none;animation:hint 1.6s ease-in-out 3;opacity:.9;text-shadow:0 1px 6px rgba(0,0,0,.4)}
.clhint svg{transform:rotate(180deg)}@keyframes hint{50%{transform:translate(-50%,-10px)}}
.cms{max-height:72%;display:flex;flex-direction:column}.cms .ufb{flex:1}
.cmr{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-top:1px solid var(--line)}.cmr:first-child{border-top:0}.cmr .bgav span{width:32px;height:32px;border:0}
.cmb{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px;font-size:14px;line-height:1.35}.cmb b{font-size:13px;display:flex;align-items:center;gap:6px}.cmb b em{font-style:normal;font-size:10.5px;font-weight:600;color:var(--muted);display:inline-flex;align-items:center;gap:2px}.cmb small{font-size:11.5px;color:var(--muted)}
.cml{display:flex;flex-direction:column;align-items:center;gap:1px;color:var(--muted);flex-shrink:0;padding-top:2px}.cml small{font-size:11px}.cml[aria-pressed=true]{color:#0B0B0C}.cml[aria-pressed=true] svg{fill:#0B0B0C}
.cmf{padding:10px 16px 0;border-top:1px solid var(--line)}.cmf .bgav span{width:30px;height:30px;border:0}
.pvr{display:flex;gap:8px}.pvlook i{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.5);margin-right:6px;display:inline-block}.pvlook.on{background:#fff!important;color:#0B0B0C!important}.pvlook.on i{background:#0B0B0C;animation:ldot 1.4s ease-in-out infinite}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
