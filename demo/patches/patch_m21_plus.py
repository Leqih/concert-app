import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s; assert s.count(o)==1,(s.count(o),o[:90]); s=s.replace(o,n)
rep("family=Inter+Tight:wght@600;700;800&","family=Inter+Tight:ital,wght@0,600;0,700;0,800;1,300;1,400&")
a=s.index('function plusCards(){'); b=s.index('function plusAim(){')
STAR="M50 2 C56 2 58 12 64 14 C70 16 78 9 83 13 C88 18 81 26 83 32 C85 38 96 40 97 46 C98 52 88 56 87 62 C86 68 94 76 90 81 C85 86 77 79 71 81 C65 83 62 94 56 96 C50 98 46 88 40 87 C34 86 26 94 21 90 C16 85 23 77 21 71 C19 65 8 62 7 56 C6 50 16 46 17 40 C18 34 10 26 14 21 C19 16 27 23 33 21 C39 19 44 2 50 2Z"
s=s[:a]+r'''function plusCards(){ const on=!!ME.looking, my=MYTIX()[0], hot=DROPS()[0], nc=xCrews().filter(c=>c.s===hot).length+(hot.dates.length>1?6:2);
  return `<button class="pk sh sc" data-act="ncopen"><span class="shl"><b>Start a crew</b><small>${nc} crews forming · 4–8 people</small></span></button>
  <button class="pk sh sq" data-act="sellstart"><span class="shl"><b>List a spare</b><small>${esc(my[1])} · ${sd(my[0].dates[0])}</small></span></button>
  <button class="pk sh st${on?' on':''}" data-act="lookon" role="switch" aria-checked="${on}"><svg viewBox="0 0 100 100" aria-hidden="true"><path d="STAR"/></svg><span class="shl"><b>Find a +1</b><small>${on?'Visible':'Hidden'}</small></span></button>`; }
function plusSheet(){ return `<div class="pfbg" data-act="plusclose"></div><div class="pfan pfan4" id="psheet" role="dialog" aria-label="Create"><h2 class="p4h"><b>What are you</b><i>up to</i><b>tonight?</b></h2><div class="pkd3">${plusCards()}</div><p class="p4n">Picked your<br>next show?</p></div>`; }
'''.replace('STAR',STAR)+s[b:]
CSS=r'''
/* ---- ＋ menu v6: playful shapes (after the owner's reference) */
.pfan4{left:0;right:0;top:calc(var(--st) + 40px);bottom:calc(84px + var(--sb));height:auto;display:block;pointer-events:none}
.p4h{margin:0;padding:0 26px;display:flex;flex-direction:column;align-items:flex-start;line-height:.98;color:#0B0B0C;animation:sin .5s cubic-bezier(.2,.8,.2,1) .05s both}
.p4h b{font-family:var(--display);font-weight:800;font-size:44px;letter-spacing:-.05em}
.p4h i{font-family:var(--display);font-style:italic;font-weight:300;font-size:46px;letter-spacing:-.04em}
.pfan4.out .p4h,.pfan4.out .p4n{animation:fadeout .18s forwards}
.p4n{position:absolute;right:26px;bottom:18px;margin:0;font-size:14px;line-height:1.25;color:#0B0B0C;animation:fadein .4s ease .5s both}
.pfan4 .pkd3{position:absolute;left:0;right:0;bottom:0;height:430px}
.pk.sh{position:absolute;left:auto;bottom:auto;margin:0;padding:0;overflow:visible;border-radius:0;background:none;box-shadow:none;color:#0B0B0C;display:grid;place-items:center;
  transform-origin:50% 50%;transform:translate(0,0) rotate(var(--r));animation:shin .75s cubic-bezier(.3,1.45,.5,1) backwards;transition:transform .45s cubic-bezier(.34,1.56,.5,1),filter .3s}
.pk.sh.dealt{animation:shfloat 6s ease-in-out infinite}
.pk.sh.sc{--r:-16deg;width:236px;height:236px;left:-34px;bottom:-26px;border-radius:50%;background:#0B0B0C;color:#fff;animation-delay:0s;z-index:3}
.pk.sh.sq{--r:13deg;width:186px;height:186px;right:-22px;bottom:150px;border-radius:30px;background:#DCDCD8;animation-delay:.08s;z-index:1}
.pk.sh.st{--r:-24deg;width:156px;height:156px;left:26px;bottom:228px;animation-delay:.16s;z-index:2}
.pk.sh.st svg{position:absolute;inset:0;width:100%;height:100%;fill:#BDBDB8;animation:spin 26s linear infinite}
.pk.sh.st.on svg{fill:#0B0B0C}.pk.sh.st.on{color:#fff}
.shl{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;transform:rotate(0deg)}
.pk.sh b{font-family:var(--display);font-weight:800;font-size:25px;letter-spacing:-.045em;line-height:1}
.pk.sh small{font-size:12.5px;margin-top:5px;opacity:.72;letter-spacing:-.005em}
.pk.sh.sc .shl{transform:translate(18px,-16px)}
.pk.sh.hot,.pk.sh:focus-visible{transform:scale(1.07) rotate(calc(var(--r)*.6));z-index:6;animation:none}
.pk.sh:active{transform:scale(.95) rotate(var(--r))}
@keyframes shin{0%{transform:translate(var(--fx,120px),var(--fy,120px)) rotate(calc(var(--r) + 90deg)) scale(.1);opacity:0}35%{opacity:1}100%{transform:rotate(var(--r)) scale(1);opacity:1}}
@keyframes shfloat{0%,100%{transform:rotate(var(--r)) translateY(0)}50%{transform:rotate(calc(var(--r) + 2deg)) translateY(-6px)}}
@keyframes spin{to{transform:rotate(360deg)}}
.pk.sh.bump{animation:shbump .5s cubic-bezier(.34,1.6,.5,1)}@keyframes shbump{0%{transform:rotate(var(--r)) scale(.9)}100%{transform:rotate(var(--r)) scale(1)}}
.pfan4.pick .pk.sh{transition:transform .4s cubic-bezier(.5,0,.3,1),opacity .3s;animation:none}
.pfan4.pick .pk.sh:not(.chosen){transform:rotate(calc(var(--r)*3)) scale(.3);opacity:0}
.pfan4.pick .pk.sh.chosen{transform:rotate(0deg) scale(1.25);z-index:9}
.pfan4.out .pk.sh{animation:shout .28s cubic-bezier(.5,0,.75,0) forwards}
.pfan4.pick.out .pk.sh{animation:none}
@keyframes shout{to{transform:translate(var(--fx,120px),var(--fy,120px)) rotate(calc(var(--r) - 60deg)) scale(.1);opacity:0}}
@media (prefers-reduced-motion:reduce){.pk.sh,.pk.sh.st svg{animation:none!important}}
</style>'''
i=s.index('</style>'); s=s[:i]+CSS+s[i+8:]
# lookon: bump the star
rep("const k2=d3.querySelector('.k2'); k2&&k2.classList.add('bump');","const k2=d3.querySelector('.st'); k2&&k2.classList.remove('still'); k2&&k2.classList.add('bump'); k2&&k2.addEventListener('animationend',()=>{ k2.classList.remove('bump'); },{once:true});")
open(P,'w',encoding='utf-8').write(s); print('ok')
