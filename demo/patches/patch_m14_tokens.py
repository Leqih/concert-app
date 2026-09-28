import os,re
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','demo2_tpl.html')
s=open(P,encoding='utf-8').read()
n=s.count('class="h2" style="font-size:24px;text-align:center"'); s=s.replace('class="h2" style="font-size:24px;text-align:center"','class="h2 sec"')
s=s.replace('class="h2" style="font-size:24px;text-align:center;margin-top:14px"','class="h2 sec" style="margin-top:14px"')
s=s.replace('<h2 class="h2" style="margin-top:34px">${P.title}</h2>','<h2 class="h2 sec" style="margin-top:34px">${P.title}</h2>')
s=s.replace('<h2>Crews forming','<h2 class="h2 sec">Crews forming')
TOK=r'''
/* ================= DESIGN TOKENS (M14) — see DESIGN.md ================= */
:root{
  --t-brand:32px;   /* Home wordmark only */
  --t-hero:44px;    /* Title on a full-bleed image hero (show, scene) */
  --t-page:26px;    /* Page title: Explore, Chats, Tickets, List a spare */
  --t-section:26px; /* Section title inside a page */
  --t-card:17px;    /* Card / group title */
  --t-row:16px;     /* List row title */
  --t-body:15px; --t-meta:13px; --t-label:12px;
  --r-xl:30px;  /* page-level cards, sheets, image heroes */
  --r-lg:20px;  /* single-row cards, banners, chat strips */
  --r-md:16px;  /* tiles inside cards, primary CTA buttons, inline media */
  --r-sm:14px;  /* thumbnails */
  --r-xs:12px;  /* segmented controls, small notes */
  --r-pill:999px;
}
/* page titles: same size, weight and vertical position on every tab page */
.sh1,.chead h1,.xhd h1{font-family:var(--display)!important;font-size:var(--t-page)!important;font-weight:800!important;letter-spacing:-.045em!important;line-height:1.05!important}
.xhd{padding-top:10px}
.chead{padding-top:22px}
.wcity{font-size:var(--t-meta)}
/* section titles: centred, 26/700, optional 14px subtitle */
.h2.sec,.hsec>.h2,.ssec h2{font-family:var(--display);font-size:var(--t-section)!important;font-weight:700;letter-spacing:-.045em;line-height:1.05;text-align:center}
.hsec>.sub,.h2.sec+.sub{font-size:14px;text-align:center}
/* hero titles on images */
.big,.stitle h1{font-size:var(--t-hero)!important;letter-spacing:-.055em;line-height:.95}
/* group labels (dates, form sections, months, search groups) */
.slab,.ncl,.umon,.srh b{font-family:var(--body)!important;font-size:var(--t-label)!important;font-weight:600!important;letter-spacing:.06em!important;text-transform:uppercase;color:var(--muted)}
/* card + row titles */
.xsh .xsb b,.xtrh b{font-size:var(--t-card)}
.ub>b{font-size:var(--t-row)}
/* radii */
.wcard,.xgrp,.xtr,.ssec2,.bgo,.wp,.xempty,.hero,.pcard,.spnone{border-radius:var(--r-xl)!important}
.sheet{border-radius:var(--r-xl) var(--r-xl) 0 0!important}
.xstart,.wlock,.wcomp2,.mst,.pollc,.pollmini,.crewrow,.screw,.cpanel,.spk{border-radius:var(--r-lg)!important}
.ufkc,.svibe button,.plan div,.wpi,.cgo,.wpill.big{border-radius:var(--r-md)!important}
.uthumb,.xth,.wthumb,.crewrow .thumb,.spwi,.fthumb,.jthumb,.scimg{border-radius:var(--r-sm)!important}
.ncsz button,.ncw{border-radius:var(--r-xs)!important}
.shero{border-radius:0 0 var(--r-xl) var(--r-xl)}
</style>'''
i=s.rindex('</style>'); s=s[:i]+TOK+s[i+8:]
open(P,'w',encoding='utf-8').write(s); print('ok',n)
