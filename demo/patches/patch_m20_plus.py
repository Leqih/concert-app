import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
GR=open('/tmp/claude-0/-home-claude-concert-app/632dad76-ea66-5370-b8fa-1e3adb71d7ae/scratchpad/grain.txt').read().strip()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
a=s.index('function plusCards(){'); b=s.index('function plusSheet(){')
s=s[:a]+r'''function plusCards(){ const on=!!ME.looking, my=MYTIX()[0], hot=DROPS()[0], nc=xCrews().filter(c=>c.s===hot).length+(hot.dates.length>1?6:2);
  const ph=u=>`<img class="cover" alt="" decoding="async" src="${u}">`;
  const card=(k,act,bg,top,mid,t,d,x='')=>`<button class="pk ${k}" data-act="${act}"${x}>${bg}<span class="pksh"></span><span class="pkgr"></span><span class="pktop">${top}</span><span class="pkbot">${mid}<b>${t}</b><small>${d}</small></span></button>`;
  return card('k0','sellstart',ph(my[0].img),`<em>${esc(my[1])}</em><em>${sd(my[0].dates[0])}</em>`,'','List a spare',`${esc(my[0].artist)} · face value`,'')
    +card('k1','ncopen',ph(hot.img),`<em>${nc} crews forming</em>`,`<span class="pkav">${[3,5,1].map(k=>`<span>${avi(PEOPLE[k][3])}</span>`).join('')}<span class="pkme"></span></span>`,'Start a crew','Any show · 4–8 people','')
    +card('k2'+(on?' on':''),'lookon',avi(MEP[3],'class="cover"'),`<em class="pkon"><i></i>${on?'Visible':'Hidden'}</em>`,'','Find a plus one',on?'Crews can invite you':'Let crews find you',` role="switch" aria-checked="${on}"`); }
'''+s[b:]
rep('<div class="pkd3">${plusCards()}</div><p class="pfhint">Tap a card, or hold ＋ and slide</p>','<div class="pkd3">${plusCards()}</div><p class="pfhint">Hold ＋ and slide to pick</p>')
CSS=r'''
/* ---- ＋ menu v5: photographic cards (replaces illustrated v4 look) */
.pk{width:128px;height:200px;margin-left:-64px;padding:0;background:#111;color:#fff;overflow:hidden;border-radius:var(--r-lg);box-shadow:0 22px 44px rgba(0,0,0,.22)}
.pk.k0{--x:-104px;--r:-7deg;--y:8px;padding:0}
.pk.k1{--x:0px;--r:0deg;--y:-14px;background:#111}
.pk.k2{--x:104px;--r:7deg;--y:8px;padding:0}
.pk>img.cover,.pk>.avimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.pk.hot>img.cover,.pk.hot>.avimg{transform:scale(1.06)}
.pk.k2>.avimg{filter:grayscale(1) contrast(1.05)}
.pk.k2.on>.avimg{filter:none}
.pksh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 34%,rgba(0,0,0,.18) 55%,rgba(0,0,0,.86) 100%)}
.pkgr{position:absolute;inset:0;opacity:.16;mix-blend-mode:overlay;GRAIN}
.pktop{position:absolute;left:10px;right:10px;top:10px;display:flex;flex-wrap:wrap;gap:4px}
.pktop em{font-style:normal;height:22px;padding:0 8px;border-radius:var(--r-pill);background:rgba(255,255,255,.16);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);font-size:10.5px;font-weight:600;letter-spacing:.01em;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.pkon i{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.5)}
.k2.on .pkon{background:#fff;color:#0B0B0C}.k2.on .pkon i{background:#0B0B0C;animation:ldot 1.4s ease-in-out infinite}
@keyframes ldot{50%{opacity:.25}}
.pkbot{position:absolute;left:12px;right:12px;bottom:12px;display:flex;flex-direction:column;align-items:flex-start}
.pk b{font-family:var(--display);font-size:19px;font-weight:800;letter-spacing:-.045em;line-height:1;color:#fff}
.pk .pkbot small{font-size:11.5px;line-height:1.3;color:rgba(255,255,255,.72);margin-top:4px}
.pkav{display:flex;margin-bottom:8px}.pkav>span{width:24px;height:24px;border-radius:50%;overflow:hidden;position:relative;border:1.5px solid #fff;margin-left:-7px;background:#333}.pkav>span:first-child{margin-left:0}.pkav img{width:100%;height:100%;object-fit:cover}
.pkav .pkme{border:1.5px dashed rgba(255,255,255,.85);background:rgba(255,255,255,.08)}
/* ticket notches on the spare card */
.pk.k0{-webkit-mask:radial-gradient(circle 9px at 0 62%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 9px at 100% 62%,#0000 98%,#000) right/51% 100% no-repeat;mask:radial-gradient(circle 9px at 0 62%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 9px at 100% 62%,#0000 98%,#000) right/51% 100% no-repeat}
.pk.k0::after{content:'';position:absolute;left:12px;right:12px;top:62%;border-top:1.5px dashed rgba(255,255,255,.4)}
.pk.k0 .pkbot{bottom:12px}
.pfhint{font-size:11.5px;letter-spacing:.01em}
</style>'''.replace('GRAIN',GR)
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok')
