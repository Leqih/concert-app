import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:90])
    s=s.replace(old,new)
# ---- Home: upcoming rows
a=s.index('function feedRow(s){'); b=s.index('\n}\n',a)+3
s=s[:a]+r'''function feedRow(s){ const sp=sparesFor(s).filter(x=>!(state.claimedIds||{})[x.id]).length, n=6+h(s.id)%60, d=new Date(s.dates[0]+'T12:00:00Z'), k=Math.abs(h(s.id));
  return `<button class="urow" data-act="show" data-id="${s.id}"><span class="udate"><small>${MON[d.getUTCMonth()]}</small><b>${d.getUTCDate()}</b></span><span class="uthumb">${img(s)}</span>
    <span class="ub"><b>${esc(s.artist)}</b><span class="um">${DOW[d.getUTCDay()]} · ${esc(VSH(s.venue))}${s.dates.length>1?' · '+s.dates.length+' nights':''}</span>
    <span class="ug"><span class="bgav">${[0,1,2].map(m=>`<span>${avi(PEOPLE[(k+m*3)%8][3])}</span>`).join('')}</span><span>${n} looking${sp?` · <b>${sp} spare${sp>1?'s':''}</b>`:''}</span></span></span></button>`;
}
'''+s[b:]
rep("<div class=\"wlist\">${feed.length?feed.map(feedRow).join('')",
    "<div class=\"wlist ulist\">${feed.length?(state.upAll?feed:feed.slice(0,6)).map(feedRow).join('')+(feed.length>6?`<button class=\"umore\" data-act=\"upall\">${state.upAll?'Show less':'Show all '+feed.length+' shows'}</button>`:'')")
rep("const VSH=v=>v.replace('Madison Square Garden','MSG').replace('Radio City Music Hall','Radio City').replace('Barclays Center','Barclays');",
    "const VSH=v=>v.replace('Madison Square Garden','MSG').replace('Radio City Music Hall','Radio City').replace('Barclays Center','Barclays').replace(' Theatre','').replace(' Theater','');")
# ---- spares: fix negative face value
rep("face:79+((k>>i)%140)","face:79+(Math.abs(k>>i)%140)")
# ---- Explore: crew row title, footer
rep('<span class="xtl"><b>${esc(c.name)}</b><span class="xsc">${SCENE_EMO[c.j]} ${SCENE_LIST[c.j][0]}</span></span>',
    '<span class="xtl"><i class="xse">${SCENE_EMO[c.j]}</i><b>${esc(c.name)}</b></span>')
rep("<em>${c.mine?'Your crew · ':''}${c.auto?'Just opened · ':''}",
    "<em>${c.mine?'Your crew · ':''}${c.wo?'Women only · ':''}${c.auto?'Just opened · ':''}")
rep("${cs.map(xRow).join('')}<button class=\"xnew\" data-act=\"ncopen\" data-id=\"${s.id}\">${ic('plus',14)} Start a crew for this show</button></div>`; }",
    "${cs.map(xRow).join('')}</div>`; }")
rep("body=proof+(tag<0&&!q?trendCard():'')+(groups.length?",
    "body=proof+(tag<0&&!q?trendCard()+`<button class=\"xstart\" data-act=\"ncopen\"><i>${ic('plus',18)}</i><span><b>Don’t see your vibe?</b><small>Start a crew for any show · up to 8 people</small></span>${ic('right',16)}</button>`:'')+(groups.length?")
rep("Face value + $${FEE} flat</span><span><i class=\"eb\">👯</i>Crews get 24h first</span><span><i class=\"eb\">↩️</i>Refund if it doesn’t arrive</span>",
    "Face value + $${FEE}</span><span><i class=\"eb\">👯</i>Crews first</span><span><i class=\"eb\">↩️</i>Refund guarantee</span>")
# sticky cover only when stuck
rep(".xstick::before{content:'';position:absolute;", ".xstick.stuck::before{content:'';position:absolute;")
rep("  syncNav(window._dockActive);\n",
    "  syncNav(window._dockActive);\n  const xs=document.querySelector('.xstick'); if(xs){ const sc=xs.closest('.scroll'), f=()=>xs.classList.toggle('stuck',xs.getBoundingClientRect().top<=parseFloat(getComputedStyle(xs).top)+1); sc&&sc.addEventListener('scroll',f,{passive:true}); f(); }\n")
H=r'''  else if(a==='upall'){ state.upAll=!state.upAll; const sc=document.getElementById('sc'), y=sc&&sc.scrollTop; render(); const n=document.getElementById('sc'); if(n) n.scrollTop=y; }
'''
rep("  else if(a==='xtag'){", H+"  else if(a==='xtag'){")
CSS=r'''
.ulist{margin-top:10px}
.urow{display:flex;align-items:center;gap:12px;width:100%;padding:10px 2px;text-align:left;color:var(--text)}
.urow+.urow{border-top:1px solid var(--line)}
.udate{width:34px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;line-height:1}
.udate small{font-size:10.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.udate b{font-family:var(--display);font-size:22px;font-weight:800;letter-spacing:-.04em;margin-top:3px;font-variant-numeric:tabular-nums}
.uthumb{position:relative;width:52px;height:52px;border-radius:14px;overflow:hidden;flex-shrink:0;background:var(--card2)}
.ub{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
.ub>b{font-family:var(--display);font-size:16.5px;font-weight:700;letter-spacing:-.03em;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.um{font-size:12.5px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ug{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin-top:2px;white-space:nowrap}.ug b{color:var(--text);font-weight:600}
.ug .bgav span{width:18px;height:18px;border-width:1.5px;margin-left:-5px}
.umore{width:100%;height:44px;margin-top:4px;border-top:1px solid var(--line);font-size:14px;font-weight:600;color:var(--text);letter-spacing:-.01em}
.xstick.stuck{box-shadow:0 1px 0 var(--line)}
.xtl{align-items:center;gap:6px}.xse{font-style:normal;font-size:15px;flex-shrink:0}
.xstart{display:flex;align-items:center;gap:12px;width:calc(100% - 24px);margin:10px 12px 0;padding:12px 14px;border-radius:20px;background:var(--card);text-align:left;color:var(--text)}
.xstart>i{width:36px;height:36px;border-radius:50%;background:#0B0B0C;color:#fff;display:grid;place-items:center;flex-shrink:0}
.xstart>span{flex:1;display:flex;flex-direction:column;gap:2px}.xstart b{font-size:15px;letter-spacing:-.02em}.xstart small{font-size:12.5px;color:var(--muted)}.xstart>svg{color:var(--dim)}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
