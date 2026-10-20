# Plus One — 交接文档

> 给接手开发的 Claude：先读完这份，再动代码。本仓库包含 Plus One 项目到 M7 为止的全部资产。

## 1. 产品是什么

**Plus One**：一个面向北美的演唱会/音乐节「找搭子 + 面值换票」App，是一件设计作品集 demo（英文 UI，真实 Ticketmaster 演出数据）。

- 口号：**Never go alone. Never pay double.**
- 两件事合在一个 App 里：
  1. **找 crew（搭子小队）**：同一场演出的人组 4–6 人小队，约好集合点和时间，一起去、一起回。
  2. **面值换票**：认证粉丝之间按面值 + 固定 $2 手续费转让多余的票，钱放托管，票到才放款；crew 内成员有 24 小时优先权。
- 研究结论（详见 `research/`）：
  - **信任比价格更重要**。用户原话编码里，「被骗 / 分不清真假票」出现 19 次，「手续费太贵」只有 4 次。
  - **一个人去是真实痛点**：预期快乐度 4.81 vs 5.81（Jurewicz 2025）；英国 70% 女性从没一个人看过演唱会（男性约 50%）。
  - **放鸽子是找搭子的头号风险**：Meetup 免费活动到场率 40–50%，收费活动 70–85%；$100 可退押金让到场率从 45% 升到 91%。
  - **小组比一对一好**：对话在 4 人左右最自然，聚会 5–8 人最佳；Tinder Double Date 女性使用率是男性的 3 倍。
  - **女性安全**：64% 美国女性会共享位置；76% 女性更愿意参加女性专属团。

## 2. 设计规范（必须遵守，完整版见 DESIGN.md）

- **只用黑白灰**，没有品牌色；强调色 = 纯黑 `#0B0B0C`。
- 字体：标题 **Inter Tight**，正文 **Inter**。
- **标题居中**；唯一例外是 Chats 页标题左对齐。
- 极简、高级感；**每个元素都必须有实际功能**，不放纯装饰按钮。
- 画布：iPhone 16，**393×852**，安全区 `--st:54px`（状态栏）、`--sb:34px`（Home 指示条）。
- 少量 emoji 作为点缀（场景标签、提示），不要堆砌。
- 文案：英文，句子式大小写，简短直接。

## 3. 仓库结构

```
HANDOFF.md            ← 本文件
CLAUDE.md             ← 给 Claude 的工作规则（精简版）
demo/                 ← 主作品：单文件 HTML 交互 demo（当前 = M19.9 / 线上 v115）
  demo2_tpl.html      模板源码（唯一需要改的文件）
  build.py            把数据注入模板 → dist/plusone-demo.html
  clips/              Clips 用的 8 段演唱会视频 + 封面（Pexels，CREDITS.md）
  shows.js            纽约演出数据（Ticketmaster 抓取后的静态快照）
  cities.json         其他 4 个城市的演出数据（Los Angeles / Chicago / London / Toronto；纽约在 shows.js）
  avatars.json        头像图（base64）
  mapdots.json        城市选择器的点阵地图
  dist/               构建产物（可以直接用浏览器打开）
  patches/            M7 与 Explore 改版时用过的补丁脚本（已应用，仅作记录）
  snapshots/          M5、M7 两个里程碑的模板快照
  tests/              Playwright 截图脚本（批量截屏检查各页面）
deck/                 ← 42 页用户研究 PPT（Claude Slides 格式：deck.json + slides/*.html）
  render_deck.py      本地渲染每页为 PNG 做检查
research/             ← 用户研究
  report-deep-research.md   深度研究报告（带全部来源）
  notes/                    5 份分主题研究笔记
iterations/           ← M1–M6 迭代对比页（index.html + 每版 demo + 截图）
app-expo/             ← 早期的 Expo / React Native 版本（只有 Home 页，接真实 Ticketmaster API）
docs/milestones.md    ← 迭代里程碑表
```

## 4. Demo 架构（demo/demo2_tpl.html）

- **单文件原生 JS**，无框架、无构建依赖（只需 Python 跑 build.py）。
- 模板里有 5 个占位符，由 `build.py` 替换：`/*SHOWS*/`、`/*AVATARS*/`、`/*CITIES*/`、`/*MAP*/`、`/*CLIPV*/`（`demo/clips/` 里的视频 + 封面，base64 内联）。
- **状态**：全局 `state` 对象（第 ~1619 行）
  `{ city, screen, id, tab, genre, sort, q, drop, rsvp, history, msgs, ... }`，另有 `xmode / xtag`（Explore）、`sheet / tsheet / psheet / kit / safe`（各种底部弹层）。
- **渲染**：`render()` 按 `state.screen` 调用对应页面函数，返回 HTML 字符串写进 `#view`，再叠加打开的弹层。
- **导航**：`go(screen, id)` 入栈 history；`back()` 出栈。
- **交互**：`#app` 上一个大的 click 分发器，按元素的 `data-act`（及 `data-id` / `data-v`）分支处理。新增交互 = 在按钮上加 `data-act="xxx"`，再在分发器里加 `else if(a==='xxx'){...}`。
- **页面**：`home`、`show`（演出详情）、`crew`（小队聊天）、`crews`（Chats 列表）、`me`、`person`（他人主页）、`explore`、`tickets`（钱包）、`scene`（场景页）、`sell`（挂票流程）。
- **弹层**：`citySheet`（点阵地图选城市）、`ticketSheet`、`plusSheet`（＋菜单）、`kitSheet`（破冰工具包）、`safetySheet`。
- **M7 关键常量与辅助函数**：
  - 常量：`FEE=2`、`ME={idv:false}`（是否完成身份认证）、`REL`（每人的到场记录）、`LOCKED(s)`（艺人锁定转票的演出）、`SPLIT`。
  - 渲染辅助：`meetStrip`（押金/集合条）、`pollCard`（投票卡）、`homeCard`（结伴回家）、`vBadges` / `vCard`（认证徽章）、`splitCard`、`lockedCard`。
- **Explore（v67–v68）**：以找 crew 为主。
  - 数据：`xCrews()` 为每场演出生成 1–2 个 crew。
  - 列表：按日期分组（`XB` 分桶），再按演出分组；行模板在 `xRow` / `xGroup`。
  - 顶部吸顶区：「Find a crew / Find a ticket」分段控件 + 场景筛选 chips。

### 开发流程

```bash
python3 demo/build.py                 # 生成 demo/dist/plusone-demo.html（单文件）
python3 demo/build.py --web           # 生成 demo/dist-web/（网页版：轻页面 + clips/ 视频文件，发布 artifact 用）
open demo/dist/plusone-demo.html      # 直接浏览器打开
pip install playwright && python3 demo/tests/m7test.py   # 可选：批量截屏检查
```

改完后发布为新的 Artifact（旧链接属于原账号，新账号无法覆盖）。
**发布前务必检查**：用 grep 搜一遍构建产物，确认里面没有任何 API key（例如你自己的 Ticketmaster key、`apikey=`），不能把 key 放进可分享的页面。

## 5. 迭代历史

| # | 线上版本 | 主题 | 关键变化 |
|---|---|---|---|
| M1 | v12 | 白底、功能优先 | 白底；Stream / Field / Aura 三种卡片语言；红→青点缀；每个按钮都对应真实功能 |
| M2 | v17 | 字体系统与首屏 | Inter Tight + Inter 字号体系；首屏放 drop / Scenes / Upcoming；标题居中 |
| M3 | v32 | 场景、人、城市 | 按「怎么去」划分 Scenes；头像；故事式 drop 卡；5 个真实 Ticketmaster 城市 + 点阵地图选择器 |
| M4 | v47 | 黑白灰与动效 | 只用黑白灰；地图缩放聚合、照片扇形展开；drop 3D 翻转 + 打字效果；Scene 页共享元素转场 |
| M5 | v58 | 面值票务 | 聊天里认领多余票 + 托管；钱包式 Tickets；挂票流程（盖章、堆叠、滑动上架、雷达）；黑色胶囊导航 |
| M6 | v65 | 消息、多余票、iPhone 16 | 气泡堆叠式 Chats（All / Crews / Direct / Requests）；不强制加好友；Spares 市场；393×852 画框与安全区 |
| M7 | v66 | 补齐研究发现的 8 个缺口 | 可退押金 hold + 到场签到；集合点投票；手环/安全面板（位置共享、结伴回家、紧急联系）；身份认证 + 女性专属 crew（需认证）；举报/拉黑；到场记录徽章；$2 固定手续费；艺人锁票演出只走官方 Face Value Exchange；分摊卡；Re-crew（同一队人再约下一场）；押金条固定在输入框上方 |
| M7.1 | v67 | Explore 改为找 crew 优先 | 分段「Find a crew / Find a ticket」；按日期 → 演出分组；社交证明（本周多少人独自去）；Join 直接进入 crew 聊天 |
| M7.2 | v68 | Explore UI 精修 | 吸顶控件；演出头 + crew 行；空位圆点；「Last spot」高亮；缩略图修复 |
| M8 | v69 | 用户自建小队 + 信任轻量化 | 「Start a crew」流程（氛围、4–8 人上限、公开/仅邀请、可选集合点、可选 $5 押金；女性专属需认证），入口在演出页、Explore 每场演出、＋菜单；小队满员自动关闭并开 crew 2；演出页小队列表改为真实数据；押金只在发起人开启时出现，其余小队是一键「I’m here」签到（计入到场记录）；没设集合点可一键建议；暖场投票默认收起 |
| M9 | v70 | 社交内容层 | Explore 顶部「Trending in 城市」热搜榜（5 条，来自组队行为：小队数、独自去的人增长、演出墙话题、面值余票、错过的人），点「Talk / Wall」直达演出墙；（首页「Your buddies are going」已在 v73 按主人要求移除，函数 buddiesGoing 保留未调用）；演出页 Show wall（只有持票人能发帖，分 Getting there / Outfits / Setlist / Missed connections，点赞、Say hi、错过的人「That’s me」双向确认）；场景页建小队接入新流程并预选氛围；＋菜单「Find a plus one」切换可被邀请状态 |
| M10 | v71 | Explore 与首页 Upcoming 精修 | 修复 Explore 搜索框被吸顶遮罩盖住的 bug（遮罩只在吸顶时出现，并加底线）；小队行改为「场景 emoji + 名称」不再截断，女性专属标在底部；去掉每组重复的「Start a crew for this show」，改为热搜下方一张「Don’t see your vibe?」卡；票规则 chip 缩短；修复余票出现负价格（$-27）的 bug；首页 Upcoming 改为日期列 + 缩略图 + 头像行（「47 looking · 1 spare」），默认按日期排序，只显示 6 场并可「Show all」 |
| M11 | v72 | Explore 信息架构重整 | Explore 只做找小队：去掉「Find a ticket」模式（余票只在小队聊天、演出页、Tickets 页 Spares 出现）；标题 + 搜索入口 + 场景筛选整体固定在顶部，只有列表滚动；热搜移到二级「Search」页（点搜索框进入，也可从首页搜索图标进入）：最近搜索、Trending 榜、Browse by vibe，输入后实时分组结果（Shows / Crews / People），回车记入最近搜索 |
| M11.1 | v74 | 首页 Upcoming 筛选修复（仅此一行） | 去掉「Soonest/Most going」切换（固定按日期）；筛选改为一整行带数量的 chip：时间（All / This week / This month）｜分隔线｜至少 2 场的类型（如 Rock 6）；0 场置灰，再点已选类型取消；无结果时「Clear filters」 |
| M11.2 | v75 | Upcoming 无限滚动与动效 | 去掉「Show all」按钮，改为滑到底自动加载（IntersectionObserver，每批 6 场，加载时 3 行骨架屏微光，新行错峰淡入上移）；全部加载完显示「That’s every show in New York · 12 shows」；切换筛选时列表错峰重新进场；行按下缩放 + 缩略图轻微放大；支持 prefers-reduced-motion。相关函数：upTail / upMore / upWatch，状态 state.upN |
| M12 | v76 | 首页 Upcoming 交互动效 | 从 Upcoming 行点进演出页为同元素过渡：缩略图放大成演出页大图（圆角 14→32），标题与内容随后淡入；返回时大图缩回原来那一行，并恢复首页滚动位置（showFly / showBack / flyBox）；跨月插入月份分隔（upRows）；首页下拉刷新（触摸或触控板上滑，ptrAttach）：旋转指示器 → 列表错峰重进场 → 顶部提示「Updated · 3 new crews…」，looking 数字随刷新增加；均支持 prefers-reduced-motion |
| M12.1 | v77 | 列表流畅度 | 筛选/下拉刷新只替换 Upcoming 卡（upSwap），不再整页重绘；列表缩略图改异步解码；加载下一批前预解码图片；入场动画 8px / 0.32s / 35ms 错开（最多 8 行）；提前 480px 触发加载 |
| M12.2 | v78 | 进入演出页改为大图 FLIP | 不再用飞行克隆图：演出页大图本身从缩略图位置用 transform + clip-path 放大展开（0.56s）；标题 → 头像/looking → 日期场馆依次上浮淡入，返回/分享按钮、正文和底部按钮也错峰进场（showFly）；返回仍用克隆图缩回 |
| M13 | v79 | 真实数据 + 首页 Filters 面板 | 纽约演出从 15 场扩到 41 场真实 Ticketmaster 活动（2026-09-28 抓取，含 NYC 与周边：Barclays、UBS Arena、Town Hall、Brooklyn Paramount、Prudential Center、MetLife 等），原始数据 data/tm_nyc_2026-09-28.psv，合并脚本 data/merge_tm.py（新增字段 sub / n / kind / size）；新演出海报直接引用 Ticketmaster 图片链接，加载失败自动换黑白首字母海报（ptile）；首页 Upcoming 筛选行 = 时间 + 「Filters」按钮（带已选数量），底部面板：演出形式（Concerts / Classical & orchestra / Festivals & lineups / Residencies，带数量）、曲风多选、场馆（Any / Arenas / Theatres）、只看有余票，底部「Clear all」+「Show N shows」实时计数，只在点应用时刷新列表 |
| M14 | v80 | 设计规范统一 | 以首页为基准建立 token（DESIGN.md）：页面标题 26/800 统一在距顶 66px（Explore、Chats、Tickets、Sell），板块标题 26/700 居中 + 14 副标题（演出页、场景页、个人页的「Going to」原为 24/22/28 且有左对齐），大图标题统一 44，分组标签统一 12 大写；圆角收敛为 30/20/18/14/12/胶囊六档（原先 30 多种数值） |
| M14.1 | v81 | 全站规范复查 | 新增 demo/tests/audit_full.py（22 个页面与面板、整页高度）；修正面板里残留的圆角：安全面板行、Keep in touch 行、认领票面板、城市面板缩略图、场景页演出卡、聊天余票图、Notify me 按钮 |
| M15 | v82 | 所有按钮都有真功能 | 导入门票（邮箱找票 / 截图识别 → 进票夹，演出墙可发帖）；编辑资料（简介、最多 4 个标签、常站位置，保存后个人页更新）；联系场馆安保（发送位置 + 座位 + 通知小队 → Staff notified，可取消）；聊天附件（照片 / 我的票 / 集合点）；演出墙回复（展开回复、持票人可回复）；安全面板「Report or block」跳到对方主页；分享类按钮真正复制链接 |
| M16 | v85 | ＋ 菜单 v2（Tickets 页维持原设计） | 三张卡从 ＋ 按钮位置弹出（回弹曲线、错峰 50ms），收起时按反序缩回按钮；卡片加大、文字 12 号不再截断，文案带实时信息（可挂票张数、是否已可被邀请）；打开/关闭不再整页重绘；从 ＋ 或 Explore 建小队时先选演出（ncPick）。曾尝试改 Tickets 页布局，主人要求恢复原设计，已还原 |
| M16.1 | v86 | ＋ 菜单 v3 | 扇形改为三行整宽卡片，从 ＋ 按钮位置依次弹出（最下方黑底 Start a crew 为主操作，离拇指最近）；Find a plus one 直接做成开关，在菜单内切换不关闭；点背景 / × / Esc / 下滑关闭，收起时反序缩回 ＋ |
| M16.2 | v87 | ＋ 菜单 v4（取代 v3 列表） | 主人觉得整行列表没有设计感，改为「一手牌」：三张竖卡扇形展开（中间黑卡 Start a crew，左 List a spare 票券插画，右 Find a plus one 雷达插画 + ON/OFF），从 ＋ 按钮发牌入场；按住 ＋ 上滑到卡片松手即选（pointer 事件，pkHot/pkPick），直接点也可；选中的卡放大居中、其余落下后进入对应流程；Find a plus one 为开关，开启后雷达脉冲 |
| M16.3 | v88 | ＋ 菜单 v5：照片卡 | 主人觉得插画卡有 AI 感，改为摄影卡：Start a crew 用本周最热演出照片 + 真实头像，List a spare 用自己下一场票面照片 + 票券缺口和撕口虚线，Find a plus one 用本人照片（关闭时黑白、开启彩色 + Visible 胶囊）；统一暗色渐变 + 颗粒 + 特粗白字，去掉编号/小箭头/手绘图形；右卡镜像右对齐；交互（发牌、按住上滑选卡）保留 |
| M16.4 | v89 | ＋ 菜单 v6：趣味图形 | 按主人给的参考图：大标题粗体 + 细斜体混排（What are you / up to / tonight?，左对齐）；三个选项变成三种图形——黑色大圆 Start a crew、转角圆方块 List a spare、自转波浪星 Find a +1（开启后变黑）；文字随图形斜排；图形从 ＋ 弹出后轻轻漂浮；按住上滑选择、选中放大仍保留。另写好一套彩色版 CSS（.pfan4.pastel，参考图的粉/黄/蓝 + 米色底），未启用，等主人决定 |
| M16.5 | v90 | ＋ 菜单自由落体 | 打开时三个图形从屏幕上方依次（间隔 110ms）受重力下落（shDrop：g=4200px/s²，回弹系数 0.36，落地压扁、旋转逐渐回正），停稳后进入漂浮；关闭时图形带旋转掉出屏幕底部（shFallOut）；尊重 prefers-reduced-motion |
| M16.6 | v91 | ＋ 菜单悬停修正 | 悬停只放大 1.05 + 柔和投影（用独立 scale 属性，漂浮动画不中断、角度不变），不再跳位/改角度/抢层级；星星只在星形本身范围内触发 |
| M17 | v92 | Clips 社区（演唱会片段） | 底部导航新增 Clips 标签（Home / Explore / Clips / Chats / Tickets）；全屏竖滑一条一条看（scroll-snap），画面用演出图 + 慢推镜头模拟视频、进度条、点一下暂停、双击点赞爱心动画；右侧头像/点赞/评论/分享；左下「Was there · 座位」持票徽章、文案、歌名，以及演出卡片 +「Find a crew」直达该演出；顶部 For you / Following、静音；左上相机或 ＋ 菜单新增的「Share a clip」胶囊 → 发布面板（只能发自己去过的演出、选视频、写文案）→ 发布后出现在第一条 |
| M17.1 | v93 | 头像移出底部导航 | 主人选择：个人头像放首页左上角（黑色细圈），原左上铃铛移到右上与搜索并排；底部导航只剩 5 个标签 + ＋；个人页左上角加返回 |
| M17.2 | v94 | Clips v2 | ＋ 菜单：星星改为 Share a clip（From last night），去掉单独胶囊；Find a +1 开关移到个人页右上（Open to invites）。Clips：真实评论面板（只有去过的人可评论、Was there 标记、评论点赞、发评论）；Following 只看 buddy/小队成员；右下转动唱片 + 歌名滚动；首次打开 Swipe up 提示；暂停时进度条加粗并显示时长；切换 tab 保留滚动位置 |
| M17.3 | v95 | 评论对所有人开放 | 主人要求：任何人都能评论 Clips、回复演出墙；去过/持票的人只是名字旁多一个「Was there」/「Going」标记。发片段、在演出墙发帖仍需持票 |
| M17.4 | v96 | 片段必须带位置标签 | 主人要求：发片段不再要求持票，改为硬性要求场馆位置标签——视频带定位则自动识别（On-site），没有定位必须手动选场馆（Tagged），不选位置无法发布；按场馆+日期自动匹配演出，同场馆多场可切换；片段上显示「📍 场馆 · On-site/Tagged」；演出墙发帖也对所有人开放 |
| M17.5 | v97 | Clips 播放真视频 | 7 段 Pexels 免费演唱会竖屏视频（1080p 原片 → 720×1280 H.264，CRF 30、无 B 帧、1 秒一个关键帧，8–10 s，见 `demo/clips/CREDITS.md`），构建时内联；滑到哪条播哪条，离开即暂停；点一下暂停/播放，双击点赞也会恢复播放；进度条和「0:03 / 0:10」跟真实播放走；进度条可拖动（拖动时隐藏文案/右栏，居中大号时间）；静音按钮控制真实声音（3 段有现场声）；发布面板缩略图换成视频封面，发布的片段也带视频。**Claude 预览面板播不了 `<video>`**（实测：canPlayType 说支持，但 data:/blob: 的 mp4、webm 全部 NotSupportedError），所以那里自动改用 **WebCodecs** 解码同一份 mp4 画到 canvas：`clips/make_index.py` 生成 `index.json`（avcC + 每帧偏移/大小/关键帧），`CodecPlayer` 模拟 video 接口，只给当前这条开解码器，滑走即释放；该模式无声（静音按钮提示 No sound in this preview）。时钟按真实时间走（rAF + 30ms 定时器双驱动），解码没跟上就跳帧而不是等帧——之前等帧会在预览面板里变成慢放。改视频后要重跑 `make_index.py` |
| M17.6 | v98 | 双击点赞红心 | 主人要求：双击不再暂停。单击等 250ms 才暂停/播放，期间第二下就取消暂停、改为点赞，并在点击位置触发「Confetti drop」动效（主人从 4 个方案 A Plus One / B Confetti drop / C Bass thump / D Spotlight 里选了 B）：白色冲击波圆环扩散 + 红心弹出（1.28→0.92→1，随机倾斜）停留后上飘消失 + 14 片小红心/红白彩纸条/白点向四周喷出再下落，像返场彩纸炮；红心出现后 450ms 内继续点会连续冒心。已点赞的右栏爱心也变红。红色是唯一的彩色例外，token `--like #FE2C55`（DESIGN.md 已注明） |
| M17.7 | v99 | 去掉 Swipe up 提示 | 主人要求：Clips 首次打开的「Swipe up」箭头和文字提示删除（连同 clSeen 状态） |
| M17.8 | v100 | 搜索能搜到 Clips | 主人同意：搜索结果在 Shows 后面新增 Clips 分组（竖版缩略图横滑，封面 + 时长 + 艺人 + ♥ 点赞数 · 场馆），按艺人、场馆、文案、歌名、发布者匹配，最多 8 条；点缩略图跳到 Clips（For you）并直接定位到那一条播放。搜索框占位改为「Artists, clips, crews, people」 |
| M17.9 | v101 | 搜索同元素过渡 | 主人要求：点首页右上搜索按钮（或 Explore 的搜索条）时，按钮本身变形成搜索页顶部输入框（位置、尺寸、圆角、底色、放大镜图标一起过渡，0.44s），占位文字淡入，Cancel 从右滑入，下面的 Recent / Trending 等依次上浮淡入；原页面冻结成一层快照淡出。点 Cancel 反向：输入框缩回原来的按钮。实现：`sbSnap` 记录起点、`sbMorph` 克隆变形、`sbGhost` 旧页面快照；系统开启减少动态时直接切换 |
| M18 | v102 | 演出详情页优化 | 修 bug：Show wall 标题和副标题重叠；墙上「Say hi / That’s me」被首页头像的 `.wme` 样式压成 40px 圆（改为单行胶囊）；底部 Join a crew / Buy tickets 下加渐变底，内容不再从按钮之间透出来。主人选了全部 4 项优化：① 余票卡左侧重复的演出照片换成黑色票根（FLOOR **GA** / BALCONY **BAL** / SECTION **105** + 张数，带齿孔虚线），右侧标题改为区域全名；② 新增「Clips from this show」横滑竖版缩略图（显示发布者和时间），点开进 Clips 定位播放；clipList 给热门演出多加 8 条片段（Harry Styles 共 4 条），Clips feed 也随之变长；③ 大图下方加 Tickets / Crews / Clips / Wall 分段标签（没有片段的演出不显示 Clips），点一下平滑滚到对应区域；④ 滚过标签后顶部出现毛玻璃迷你标题栏（返回、艺人名、日期 · 场馆、分享 + 同一组标签），滚动时标签自动高亮当前区域 |
| M18.1 | v103 | 说明改 ⓘ 弹窗 · Clips = 演出评价 feed | 主人要求：删掉「Face value only…」「Crews cap at 8…」两行小字，改为标题旁 ⓘ，点开底部弹窗解释（余票：面值+$2、托管、加入卖家小队、小队优先 24h；小队：最多 8 人、满了开新队、集合点、到场分）。主人定义：Clip 就是用户对演唱会的评价 → **只改演出页**（Clips 标签页保持全屏）：Clips 区改为竖向评价 feed，顶部是 AI 总结卡（平均分大字 + 星级 + 评价数、AI 生成的一段总结、Setlist / Crowd / Sound / Venue 分项条），下面「How was it?」发帖入口和帖子流（文字帖、带视频的帖子混排，星级、Was there 标记、点赞/评论，默认 4 条可展开全部）；Clips 区也有 ⓘ 解释 AI 总结和打分。发帖面板支持 1–5 星（可选）、**纯文字帖**（Aa Text only）、从演出页进入时自动标记该演出；纯文字帖在 Clips 标签页显示为模糊背景上的大字引语 + 星级。Show wall 保留 |
| M18.2 | v104 | 评价改为小红书双列瀑布流 | 主人要求：Clips 评价 feed 改成小红书式左右两列瀑布流。视频帖 = 3:4 封面（右上播放标、左下时长）+ 两行文案；文字帖 = 灰底大字引语卡（上方星级）；卡片底部头像、名字、❤ 点赞。按真实高度分配到两列（≤12 条时穷举找最平的分法，列内保持原顺序）。视频卡点开进全屏 Clips，文字卡点开底部详情（作者、星级、全文 + 评论）。默认 6 条，可展开全部。顺手修了评论点赞数偶尔出现负数的 bug |
| M18.3 | v105 | Show wall 独立成页 | 主人决定：Show wall 做成单独页面，入口放在 Clips 前面。演出页顺序 Tickets → Crews → Show wall 预览卡 → Clips，标签也改为 Tickets / Crews / Wall / Clips。预览卡：头像叠放 + 帖子总数 + 最近一小时新帖数、最新 2 条（标签 + 名字 + 两行正文）、底部话题标签 +「Open wall ›」。点开进入 Show wall 页（sticky 头部：返回、Show wall、艺人 · 日期 · 场馆、分享；下面是原来的话题筛选、发帖框、帖子和回复）；发帖后回到顶部；返回演出页时恢复原来的滚动位置。首页 Trending 里的 wallgo 也改为直接打开 Show wall 页 |
| M19 | v106 | 大群 → 小队 → 私聊 | 主人提出：每场演出一个大群，大家可以从里面建小群（小队）或私聊。实现：Show wall 升级成 **Show chat**（大群，谁都能进、谁都能发，名字旁标 Ticket holder）：聊天气泡形式（别人白色靠左、自己黑色靠右，最新在底部），原话题标签变成 # 频道（All / # Getting there / # Outfits / # Setlist / # Missed connections），每条可点赞、展开回复；顶部置顶卡「Want a smaller group? Start a crew」；点头像或名字弹出卡片：Say hi（私聊）/ Invite to a crew / Profile。演出页顺序改为 Tickets → Show chat 预览卡（going 人数、在线人数、最新 2 条、# 频道、Join/Open chat）→ Crews going（副标题 Small groups from the chat · up to 8）→ Clips；标签 Tickets / Chat / Crews / Clips。底部主按钮从 Join a crew 改为「Join the show chat」，加入后变「Open show chat」，解决和小队列表的重复。Chats 页会显示你加入的大群（持票的演出自动在群里，如 Gorillaz、Doja Cat），刚加入的排最前 |
| M19.1 | v107 | Show chat 用回小队聊天的视觉 | 主人：逻辑不变，但聊天页要用之前小队聊天的背景和 UI；顶部 # 频道标签保留。Show chat 改为和 crew() 同一套：演出大图模糊背景 + 暗色渐变 + 颗粒、玻璃质感灰色气泡（别人）/ 白色气泡（自己）、气泡下方头像 + 名字 + ✓ + # 频道 + 时间 + 点赞 / 回复、大标题「艺人 · Show chat」、底部圆角玻璃输入框（未加入时是白色「Join the show chat」）。# 频道标签固定在返回键下方。注意 class 冲突：新增的 `.chnm`、`.scpic` 是为避开旧的 `.chn`、`.scimg` |
| M19.2 | v108 | Clips 评论框、点赞特效、发帖优化 | 主人：评论框右侧不要出现滚动条；优化点赞特效、发帖和 UI。评论框：所有 sheet 隐藏滚动条（上下渐隐提示可滚动）；评论和分享 sheet 改为原地挂载 / 局部更新，不再整页 render，所以视频不中断、sheet 不会重新滑入；修了 `.cmr` 与旧 crew 组件的 class 冲突（之前每行有奇怪的圆角描边和缩进）；标题「41 comments」+ 右上关闭；行内 Reply（自动填 @名字）；评论点赞变红并弹跳；表情快捷栏 🔥🙌😭🎶❤️👏🤘；输入框聚焦变白底黑边，有字才出现圆形发送键；发出的评论插到最上面并高亮渐隐，标题和右侧栏的评论数同步 +1。点赞：双击 = 渐变光泽大心（随机倾斜）+ 白色细波纹 + 7 颗小心向上飘散，连击时心逐渐变大；右侧栏红心有弹跳 + 圆环 + 6 个小点爆开，取消时轻微收缩，数字滚动。发帖：星级原地点亮逐颗弹出；标题旁有字数统计；选中的视频加白色内描边；「Post clip」按钮先显示上传进度填充 → ✓ Posted → sheet 下滑 → 新帖以缩放淡入落在 Clips 顶部，名字旁有「✓ Posted」标记 |
| M19.3 | v109 | 评论能发了 + 发送动效 | 主人：评论发不出去。原因：Claude 预览面板是沙盒 iframe（没有 allow-forms），原生表单提交根本不会触发，onsubmit 不执行（Show chat、小队聊天的输入框同理）。修复：全局接管——在 input 里按 Enter（中文输入法组字中不算）或点 submit 按钮时，取消原生提交，手动派发 submit 事件，所有表单在任何环境都能用。发送动效：发送键箭头向右上飞出再从左侧回来并轻微按压；文字变成黑色气泡从输入框沿弧线飞到列表顶部的新评论位置后淡入成正文；下面的评论用 FLIP 平滑下移让位；新头像弹出；标题评论数滚动 +1；评论里的 emoji 从发送键向上飘散；手机上轻震 |
| M19.4 | v110 | 评论区「Was there」改成实心标签 | 主人：不要名字旁那个淡淡的 ✓ 小勾，要更明显的标签表示这个人去过现场；去掉标题下「✓ marks people who were at …」提示。改为名字右侧黑底白字胶囊「🎫 Was there」（ticket 图标，class `.cmtag`，18px 高），评论行和评价详情头部统一；删除提示行。顺手：评价详情里正文和「N comments」之间加分隔线和间距，关闭键对齐 |
| M19.5 | v111 | 评论：去掉 ✕，支持 @、贴纸、表情、图片 | 主人：评论区不需要关闭的 ✕；发评论要有更多选择（@ 别人、表情包、图片）。去掉 ✕，改为点外面或下拉 sheet 关闭（拖动头部/把手，超过 90px 关闭，背景跟随变淡）。输入框内三个工具：@（插入 @ 并弹出人选）、😊 贴纸/表情面板、🖼 图片面板。@：光标前是「@字母」就在输入框上方出现横向人选（头像 + 名字 + Buddy / In this thread / Going，按好友 → 本帖参与者排序），点选替换为「@Name 」；评论里 @Name 加粗；发出后提示「Maya R. will get a heads-up」。贴纸面板：Stickers / Emoji 两个 tab；12 个黑白贴纸（ENCORE!、FRONT ROW、SEE YOU THERE、LOUDER 🔊、I WAS THERE 票根、GOAT 🐐、10/10、CRYING RN 😭、大号 🔥🎸🎤🪩），点一下直接发出并从面板飞到新评论位置；Emoji tab 32 个表情插入光标处。图片面板：Recent photos 4 列（Clips 视频封面 + 演出图），选中后输入框上方出现缩略图（可 ✕ 移除），可配文字一起发；评论里图片 3:4 圆角，点开全屏查看（从缩略图放大）。面板打开时收起键盘和快捷表情栏；聚焦输入框时面板收起。示例评论里加了一条 @、一条贴纸、一条带图，展示能力。注意：`.cmin button` 旧样式已限定为 `.cmsend`，避免工具按钮被染成黑色圆 |
| M19.6 | v112 | @ 可搜名字或 ID，点 @ 进主页 | 主人：@ 时要能搜名字或 ID；评论里点 @ 能跳到那个人的主页。每人有 ID = 名字小写 + live（和个人主页上显示的 @mayalive 一致，函数 `PH(i)`）。输入「@」即出现「Mention someone · Search a name or @id」，列出所有人；继续输入按 ID 子串或名字任一单词开头过滤（如 @jul → Jules W.，@theoli → Theo L.），命中部分灰底高亮，每项显示头像 + 名字 + @id（+ Buddy / In thread），好友 → 本帖参与者 → 字母排序；无结果显示「No one matches」。选中插入「@id 」。Reply 也改插 @id。评论里的 @id（兼容旧的 @名字）渲染为可点按钮，点击跳到对方主页；评论头像、名字也可点进主页（自己 → Me）。从评论跳主页时记住当前帖子，按返回回到原页面并自动重新打开同一个评论区，自己发的评论还在 |
| M19.7 | v113 | 私信请求的门槛 | 主人确认：私信要有门槛、防搭讪。已有：非好友/非同小队的第一条私信作为请求发出，对方接受前不能再发。新增：① 必须有共同演出才能发请求（`sharedShow`：从 Show chat 发起 = 该场；从主页发起 = 双方 Going to 的交集；Ines 与你无交集 → 主页按钮显示「No shared show」，点击提示）；系统消息改为「You’re both going to X · your first message is sent as a request」；② 每天最多 10 个请求（`DM_LIMIT`、`state.dmSent`），发送前提示「N of 10 requests left today」，超出提示明天再试；③ 发出后输入框锁定「Waiting for Sam to accept」，说明 7 天未回复自动过期；④ Requests 页：顶部「Only verified people」开关（隐藏未核验账号的请求并显示被隐藏数量），每条显示 Verified / Not verified、「Both going to X」、剩余有效天数，按钮 Report（举报并拉黑，对方不能再发）/ Delete / Accept，删除和举报都不通知对方。他人主页的 Going to 改为按人区分（`PGO`）。注意：demo 里对方仍会在 2 秒后自动接受，用于演示流程 |
| M19.8 | v114 | Scene 页：你的场次、信任信号、原价余票 | 主人选了优化建议 1、3、5。① Crews forming 上方加筛选 chip：Your shows（默认，你有票的场次，如 Gorillaz、Doja Cat）/ 各场演出 / With a spare / All，按场景分别记住（`state.scF` + `state.scFor`）；你的场次在缩略图上标「🎫 Going」；统计第一格随筛选变为「for your shows / crews here」，第三格改为 face-value spares 数。② 小队卡片加信任信号：发起人名字后「showed up 12/12」（REL）、「✓ 3/4 verified」、「$5 hold」（发起人开了押金）、「Women only」（Women only 场景）。③ 队里有人多一张票时，卡片底部出现余票条：黑色票根（GA / BAL / 区号 + 张数）+「Ines has a spare · $152 face value」+「Crew-mates get first dibs · $2 fee · escrow until it lands」，点击直接进认领面板（复用 claimspare）。`sceneCrews` 先为你的每个场次生成一个小队，再补城市里其他演出；卡片外层改为 div，内部分为主体按钮、Join、余票条，避免按钮嵌套。修正：Your shows 改为「你想去的场次」（Harry Styles、Gorillaz、Doja Cat、Steve Lacy），有票标「🎫 Going」、没票标「Want to go」；没票的场次优先展示余票（如 Harry Styles 的 Priya 余票），因为已经有票的场次不需要余票 |
| M19.9 | v115 | Scene 页改版 | 主人要求改版（上一轮建议 1、2、4、5）。目标：小队在首屏可见。① 头部压缩：照片扇形缩小为 58×72（保留首页飞入过渡，`.sh2`），描述改为每个场景专属文案 `SC_DESC`（Going solo：「22 people are going solo this week. Meet before doors, split after the encore — or don’t.」，按研究改掉 never on your own 的孤独框架）；② 去掉统计卡和重复的成员行，合并为一行「头像 + 86 in this scene · 11 crews open」，余票数和场次数放在筛选 chip 上；③ 筛选栏吸顶（`.scbar` sticky，滚过后加毛玻璃背景 + 返回键 + 迷你标题），切换筛选时保持位置并把选中 chip 滚到可见；④ 点小队或 Join 先弹出预览面板 `scPrev`：成员（Host 标签、ID 核验、到场记录，可点进主页）、The plan 三步时间线（`SC_PLAN`，每个场景不同）、Good to know（押金 / 女性专属 / 公共场所 + 位置共享 / 随时可退）、没票时的余票条，底部 Not now / Join（开押金则显示 Join · $5 hold）；⑤ 底部「Where this crowd is going」换成「Clips from this scene」（这些演出的 Clips，显示发布者）。只有发起人一人时显示「Host verified」 |
| M19.10 | v116 | 网页版改为「轻页面 + 独立视频文件」 | 10.7MB 的单文件在 claude.ai 网页版一直转圈加载。新增 `python3 demo/build.py --web` → `demo/dist-web/index.html`（约 2.3MB）+ `dist-web/clips/*.mp4/jpg`，视频按需加载；预览面板里的 WebCodecs 兜底会先 fetch 视频字节再解码。发布 artifact 时用 dist-web（页面 + clips 作为 files 一起发布）；`dist/plusone-demo.html` 仍是完整单文件，用于离线/侧边栏。dist-web 不进 git（.gitignore） |
| M19.2 | v108 | 网页版改为「轻页面 + 独立视频文件」 | 10.7MB 的单文件在 claude.ai 网页版一直转圈加载。新增 `python3 demo/build.py --web` → `demo/dist-web/index.html`（约 2.3MB）+ `dist-web/clips/*.mp4/jpg`，视频按需加载；预览面板里的 WebCodecs 兜底会先 fetch 视频字节再解码。发布 artifact 时用 dist-web（页面 + clips 作为 files 一起发布）；`dist/plusone-demo.html` 仍是完整单文件，用于离线/侧边栏。dist-web 不进 git（.gitignore） |
| M19.11 | v117 | 消息页 + 聊天详情优化 | 修 bug：小队聊天/私聊里标题、计划卡、气泡文字继承了页面的近黑色，暗背景上几乎看不清（`.chat{color:#fff}`，弹窗内恢复深色字）。聊天底部加渐变，消息不再从置顶条和输入框后面透出来。Show chat 右上从分享改为 🛡️ Safety：静音本群、陌生人私信先进 Requests、举报、已屏蔽；点名字的卡片底部加 Block / Report（屏蔽后其消息隐藏）。群聊内容按演出变化（每类话题 3–4 条文案按演出轮换），Chats 列表里各群的最新消息不再相同。Chats 筛选加 Shows（大群），Crews 只剩小队 |
| M20 | v118 | 聊天统一成 Instagram 式 | 主人：每个群聊设计不一样 → 做得像 Instagram 群聊、具备相同功能。小队群、私聊、演出大群共用一套（`igHead / igList / igComposer / igInfo / igWire`）：顶部头像（小队=双头像叠放、私聊=单头像、大群=演出方图 + 绿点）+ 名字 + 状态（成员数 / Active / 在线人数）+ 盾牌 Safety + ⓘ 详情；小队有 📌 置顶集合信息条，大群有 # 频道条；对话开头是介绍区。消息：连续消息成组（圆角按首/中/尾变化）、群里首条上方显示发送者名字（大群附 # 频道）、头像只在一组最后一条、日期分隔、表情回应小胶囊、引用回复（Replied to …）、自己最后一条下方 Seen / Seen by。手势：双击 = ❤️（带弹跳动画），长按 = 背景变暗 + 上方 6 个表情 + 下方 Reply / Copy。输入框：白色相机键 + Message… + 语音 / 相册 / 贴纸，输入文字后变 Send；回复时上方显示「Replying to …」。ⓘ 详情页：大头像、Show / Mute / Safety、计划、成员列表、Leave。Chats 列表改为 Instagram 式：56px 头像（类型由头像形状区分）、名字 + 小标签、预览 · 时间、未读加粗 + 黑点，不再按位置轮换黑白灰。背景保留演出大图（相当于 Instagram 的聊天主题） |
| M20.1 | v119 | 只借鉴 Instagram 的聊天细节，页面保持原样 | 主人纠正：参考 Instagram 的是「不同聊天里的细节」，不是改我们的 chat 页面。已恢复：Chats 列表原来的气泡卡片样式；小队群原来的头部（演出标签、人数、群主、大标题、集合/开门/日期卡、投票）、私聊头部、演出大群原来的标题区和 # 频道、原来的 🛡️ Safety 按钮和输入框。保留的 Instagram 细节（三种聊天一致）：连续消息成组、群里首条上方显示名字、头像只在一组最后一条、日期分隔、表情回应、双击 ❤️、长按表情条 + Reply / Copy、引用回复（输入框上方 Replying to …）、Seen / Seen by。ⓘ 详情页和 Instagram 式列表不再使用 |
| M20.2 | Removed the Safety buttons and Safety sheets from crew chats and the show chat (Leqi doesn't want this feature) |
| M21 | v120 | 流程补全 + 可读性 + 轻量网页版 | 主人同意按审查清单修改。**流程**：Explore / 演出页点 Join 先弹预览（谁在队里、到场记录、集合计划、你有没有票；没票可直接认领余票或开提醒），再加入；没票时群聊底部不再写「所有人都已验证持票」；小队和演出群右上角加 ⓘ 详情（成员、静音、退出；房主可结束小队，退出会真正离开）——**不含安全工具**，遵守 M20.2；挂出的余票有完整状态：有人认领 → 你在 Ticketmaster 转出点「I’ve sent it」→ 对方收到、到账，挂着时可下架；首页铃铛改为 Activity 面板（入队申请、余票提醒、评论回复、私信、过户，点哪条去哪里，可全部已读）；个人页加到场记录（showed up 8/8）、Crews/Tickets 数字可点、新增 Your clips；片段只能挂到今晚或最近 3 晚的演出（新增「昨晚 Wave To Earth 首场 9/26 @ Radio City」，9/29 是第二场）；认领余票后不在小队时文案改为「XX is sending it now」+ Find a crew；分享在剪贴板被禁时不再报错。**可读性**：次要灰 #86868C → #6E6E73（浅底对比度 3.2 → 4.5:1）；最小字号 11px；Chats 标签、Report/Block、城市切换、附件、搜索清空等小按钮点击区 ≥44px（外观不变）。**规范**：在线绿点改黑/白；城市卡片、Scenes 缩略图和扇形照片圆角改用 --r-xs。**性能**：Vercel 改为轻量网页版（`demo/dist-web/index.html` 0.6MB，图片和视频为独立文件，图片长期缓存），原 10.7MB 单文件保留在 `/offline` |
| M22 | v121 | 细节打磨 + 流程顺畅 | **打磨**：说明小字、搜索框 placeholder、Spares tab、Trending 序号等对比度达标；Explore 搜索框文案缩短不再换行；Clips 侧栏和搜索 Cancel 点击区 ≥44px；Scene 缩略图「Want」；Me 页右上角改为固定文案的「Open to invites」开关。**流程**（主人确认 4 项）：首页 See crews 直达演出页 Crews 段，tab 高亮跟随正确；已在其中的小队一律显示「Open」（Explore 与演出页）；Crews-only 余票不再是只弹提示的「Crew first」：已在该演出小队里可直接 Claim，否则「Join a crew」→ 小队预览（写明解锁哪张票）→ 入队后直接进结账；演出页底部第二个按钮随情况变化：有票没小队 → Find a crew，有余票 → Spares from $X，否则 Buy tickets ↗ |
| M23 | v122 | 首次使用流程 + 收尾 | **首次使用流程**（新屏 `onb`，打开 demo 先看到）：欢迎页（演出照片滚动拼贴 + Continue with Apple / email + 「Just looking · skip setup」）→ 名字和头像 → 关联票务账号（Ticketmaster / AXS / SeatGeek / Dice，连接后列出 3 场已购演出；可「I’ll do this later」）→ 选城市 → 选 1–3 个 Scene → 首页；每一步都能 Skip，顶部 4 段进度条。选的 Scene 会排在 Explore 筛选条最前面。自动化测试（navigator.webdriver）或网址带 `#home` 时直接进首页。**收尾**：演出页 📅📍 和 Tickets / Spare tickets 标题的 🎟️ 换成黑白线性图标（Scene 的 emoji 保留）；他人主页「Pit / Spot」从数字栏移到标签行（「Usually in the pit」）；Me 页头部压矮，底部导航改用标准样式并高亮 Home；删掉没用到的 igComposer（含只弹提示的贴纸/语音按钮）。 |
| M23.1 | v123 | 每场演出都有图 | 主人：「每一个演唱会都有图片」。纽约 26 场演出原来直接外链 Ticketmaster 图片，在 claude.ai 页面里外链被拦，只显示字母缩写方块（如 World of Warcraft 的「WO」）。已把这 26 张下载、缩到 420 宽，写进 `demo/shows.js` 作为内嵌图片；网页版构建会拆成 `dist-web/img/` 文件。现在 shows.js 里没有任何外链图片 |
| M23.2 | v124 | Chats 气泡颜色有含义 | 主人在 Chats 页评论「优化」。保留 M20.1 恢复的气泡卡片堆叠样式，只把颜色从按位置轮换（黑/白/灰）改为有含义：**有未读的聊天 = 黑色**（带白色未读数），已读的白 / 浅灰交替保持堆叠层次；读完一个聊天回来，它就变浅。相邻两张黑卡之间加了一道细高光和阴影，仍能分清 |
| M23.3 | v125 | Start a crew 的流程逻辑 | 主人在 ＋ 菜单「Start a crew」上评论「优化其用户逻辑」。① 卡片副标题不再引用别的演出的小队数，改为「For <你下一场有票的演出> or any show」；② 选演出：先列「Your tickets」，再列「Coming up」，每行写已在哪个小队 / 有几个小队开着 / 还没有小队；③ 表单顶部先查重：已在这场的小队里 → 提示 + Open；已有开放小队 → 「N crews already forming」+ 最匹配的一个（同 vibe 优先，不推荐女性专属给非女性专属）+ Join instead（走入队预览）；没有 → 「First crew for this show」；④ 新增可编辑的小队名（默认跟随 vibe 建议名，手动改过就保留）；⑤ 女性专属未验证时按钮改为「Verify ID · 1 min」可当场验证，不再是死按钮；⑥ 默认 vibe 取首次使用流程里选的第一个 Scene |
| M23.4 | v126 | 首页 Upcoming 列表 | 主人在 Upcoming in New York 评论「这个页面太难看了」。① 不再无限下拉（38 行一路滚下去，也是 10 月 7 日「太长、回不去」的根源）：先显示 6 场，底部「Show more · N left」每次多加 6 场；② 行样式精简：去掉三个小头像，缩略图 52→60，右侧加 ›；第三行改为标签：持票显示黑色「✓ Going」，有余票显示灰色「🎫 N spares」，后面是「N looking」；③ 修数字被拆开的 bug：`.gch{font-variant-emoji:emoji}` 让筛选 chip 里的数字按 emoji 字形渲染，「38」显示成「3 8」，筛选面板「Rock 12」同理；改为数字用文字字形 |
| M23.5 | v127 | Start a crew 选演出页更有趣 | 主人：「有没有更有趣的 UI 设计」。选演出从普通列表改为：**Your tickets** = 横滑的黑色实体票根（左侧演出图 + 白色日期块、虚线撕口、上下半圆缺口、交替微倾斜，写座位区 · 还有几天，底部状态胶囊：已在哪个小队 / 几个小队开着 / Be the first crew）；**Coming up** = 两列海报墙（高矮交错的瀑布感、白色日期胶囊、底部渐变上写艺人 / 场馆 / 小队数，用 1–3 个圆点表示开着的小队数）。仍是黑白灰 |
| M23.6 | v128 | 认领余票弹窗变小 | 主人在 Tickets 页评论「这个弹窗太大了」（Claim spare 弹窗，原高 653px）。确认步骤压到 417px：票面图 150→96px；三行价格表合并成一个总价块（大号总价 + 一行「面值 + $2 flat fee · 卖家原价」）；三行保障说明合并成一行三个小标签（Held until it lands / Official transfer / Refund if late）；去掉副标题。完成后的「Ticket claimed」步骤不变 |
| M23.7 | v129 | 欢迎流程只出现一次 | 主人：「流程有问题」。首次使用流程原来每次打开/刷新都会出现（每次发布新版本后都要重走一遍）。现在完成或跳过后记在本机（localStorage `po_onb`），之后直接进首页；Me 页底部加「Replay the welcome tour」可重看。「Find my crews」改为直接进 Explore（选的 Scene 排在最前），和提示文案一致 |
| M24 | v130 | 建队/入队流程重做 + 内容多的不用弹窗 | 主人：「流程有问题」→ 选「建小队 / 入队」；又评论「内容过多就不应该是弹窗的设计」。**改成整页**：Start a crew（选演出 → 表单，返回键先回选演出）和小队预览（顶部演出大图 + 剩余名额，底部固定按钮）都从底部弹窗改为独立页面（`nc` / `cp` 屏，`pageFrom()` 把原弹窗内容排成页面）；认领余票、城市、筛选等短内容仍是弹窗。**修流程 bug**：① Scene 页预览里点 Join，原来会进到这场演出的任意一个小队（甚至进 Pit crew），现在进的就是你看的那个小队；② 所有入口（Explore、演出页、Scene、Join instead、Crew first 余票）共用 `joinCrew()`；③ 已在这场另一个小队里时，预览顶部提示并把按钮改为「Switch to this crew」，切换后旧小队只通知其房主；④ 女性专属小队未验证时按钮变「Verify ID · 1 min」可当场验证；⑤ 选了 $5 hold 的小队入队后聊天里写明已冻结 $5；⑥ 入队/建队后按返回不会回到预览或表单页 |
| M24.1 | v131 | 欢迎流程按参考图重做 | 主人给了参考图（Comet / Breathwrk 的 onboarding）。5 屏全部改为深色夜空背景（深蓝黑渐变 + 微闪星点），顶部小写 wordmark「plus one」+ 胶囊式页码点，右上 Skip，底部一个白色大胶囊按钮。标题用 Inter Tight 粗体 + 细斜体强调词（Never go *alone.* / Bring your *tickets.*），参考 Comet 的「Learn *with* Comet」。欢迎页：倾斜漂浮的两张演出卡（Harry Styles 小队卡 + Doja Cat）、一条聊天气泡和一张「Floor GA · $135 face value」票签依次弹出。关联票务：连接后三张票像发牌一样叠落。城市：大图卡片网格。Scene 一步按 Breathwrk 做：大字陈述「Most people go to shows / with no one」，下面一堆倾斜的玻璃胶囊从上方掉落堆叠，点选变白。仍是黑白灰 |
| M24.2 | v132 | ＋ 菜单的设计语言延伸到它的三个流程 | 主人：喜欢「What are you up to tonight?」，参考 Cosmos / Music OS / Ai OS，要把这种语言用进它的用户流程。Start a crew（选演出 → 表单）、Share a clip（从弹窗改为整页 `cs` 屏）、List a spare 统一为：浅灰点阵底（#EEEEF0 + 14px 点阵）、左对齐的三行编辑式大标题（粗体 / 细斜体 / 粗体，如 Which show / *are you* / going to?、Make it / *your* / crew.、What was / *the* / moment?），左上白色圆形关闭/返回、中间短横线步骤点（Cosmos 式）、右上角是该流程在 ＋ 菜单里的那个形状（黑圆 = crew、灰色倾斜方块 = spare、旋转的波浪贴纸 = clip），底部居中黑色胶囊按钮而不是通栏按钮；选演出海报交替微倾斜、日期签改为浅黄便签。CSS 类前缀 `fl*`（`.pf*` 已被 ＋ 菜单占用） |
| M24.3 | v133 | Start a crew 改成一屏一个问题 | 主人：「没有感觉有改变」（M24.2 只换了底色和标题，太保守）。Start a crew 重做成 4 屏、每屏一个问题，直接用 ＋ 菜单的「实物感」：① Which show / *are you* / going to? — 你有票的演出是 2–3 张从上方掉落、互相压叠、倾斜的大卡（浅黄便签写日期），下面「Or another show」是一排拍立得；② How do you / *want to* / go? — 8 个 vibe 做成 ＋ 菜单同款的黑/灰圆、旋转波浪贴纸、白色圆角方块，掉落成一堆，点选变黑；查重提示是一张倾斜的黄色便利贴（Join instead / Open it）；③ How many / *of you,* / max? — 180px 的巨大数字 + Music OS 式刻度尺选 4–8；④ Last / *few* / things. — 大字可编辑队名、两张倾斜的 Anyone going / Invite only 卡、meetup 与 $5 hold 开关；底部始终是居中黑色胶囊（Next / Create crew），返回键逐步后退 |
| M24.4 | v134 | Start a crew 动效与交互打磨（UI 不变） | 选项（Scene 贴纸、人数、可见范围、开关）改为原地更新，不再整页重绘：贴纸不会每次点都重新掉落，开关真正滑动，已输入的名字不丢；步骤间按方向滑入/滑出（前进从右、返回从左，返回时不重播掉落）；选演出时卡片先抬起再进入下一步；人数大数字上下滚动切换，标尺可左右拖动、←/→ 调整；贴纸选中回弹；Esc 返回上一步，名字框回车直接创建；Create 按钮先显示「Creating…」再进入群聊；震动反馈只在用户点过之后触发。流程：没有票时第一步不再空白（显示最近的 3 场，副标题改为「Coming up soon」），超过 3 张票时第 4 张起不再从列表消失；名字只有被改过才保留，否则跟随 Scene 默认名。尊重 prefers-reduced-motion |
| M24.5 | v135 | 「Last few things」改成票根预览 | 主人：「这里的 UI 感觉能再设计一下」。第三步改为一张可编辑的小队票：上方演出图 + 日期便签 + 艺人/场馆；中间直接改名字（虚线下划线提示可编辑）；Scene 和人数做成胶囊（人数用圆点表示 1 of N），点它们跳回对应步骤，改完按钮显示「Done」直接回到票根；打孔分割线下是 Suggest a meetup / $5 hold 两个开关；票下方 Anyone going / Invite only 改为滑块分段控件，下面一行说明随之变化。原来的摘要副标题改为「Here’s your crew. Tap anything to change it.」 |
| M24.6 | v136 | 选演出页加搜索 + 拖动不选中文字 | 主人：拖人数标尺时会选中文字；第一步「如果这里没有满意的，怎么搜到想要的演出？」。整个建队流程禁止选中文字（输入框除外），标尺拖动时阻止默认行为。第一步改版：标题下加搜索框（按艺人、场馆或日期搜，例如「Oct 12」；滚动时吸顶；可一键清除，Esc 清空），下面是「Your tickets」票堆（没票时为「Coming up soon」），再下面列出所有即将开始的演出，按 This week / This month / Later 分组，三列拍立得网格（原来只有一行 10 场）。输入时票堆隐藏、只显示结果（「3 shows」）；没有结果时显示黄色便签提示 + Clear search。主人说 Chats 点不进去：从首页、Tickets 页（含展开的票）、建队后返回点 Chats 都能进入，列表里的群聊也能点开，暂未复现，待主人给出具体步骤 |
| M24.7 | v137 | 选演出页 UI 优化 | 主人：「UI 优化」。票堆缩小（高 330 → 250，卡片 46/42/38%），搜索框改为细描边 + 轻阴影，聚焦时 1.5px 黑描边、图标变黑（不再是粗黑框 + 重阴影）；搜索框下加快捷筛选胶囊（Pop / Rock / Hip-Hop / R&B / Country / MSG / Barclays / Radio City，再点取消，选中后滚到结果）；吸顶时背后加渐隐底色，下面内容不再透出来。演出列表从三列拍立得改为白色卡片里的列表行：左侧月/日、缩略图、艺人、场馆 · 已有几个小队（或「You’re in …」「No crews yet」），行间细分割线，按下变灰；搜索时匹配文字灰底高亮 |
| M24.8 | v138 | 建队流程标题改小 | 主人：「我不想要这种标题特别大且占位置」（中间一度误解为要更大，已撤回）。四步标题从三行堆叠（约 125px 高）改为一句话横排换行：粗体 30px + 中间斜体 31px，最多两行（约 34–66px 高）；副标题间距 8px。内容整体上移，Last few things 一屏能看到票根和可见范围 |
| M24.9 | v139 | （已撤回）Start a crew 改标准页面样式 | 曾按「Standard app style」改成标准页面，主人随后明确：「我喜欢他们独特的设计，我也希望我们需要的也能保持独特的设计」。已完整撤回，建队流程恢复拼贴风格（点阵背景、倾斜票堆、贴纸、黄色便签），与 List a spare / Share a clip 保持一致；那两个流程从未改动。**结论：三个 ＋ 菜单流程保留独特设计，不要改成标准页面** |
| M24.10 | v140 | List a spare / Share a clip 交互打磨（外观不变） | 主人：「我只是想优化他们的交互」。**Share a clip**：选视频、改地点、选场馆/演出原来每点一下都整页重绘（大标题重播进场动画、正在输入的说明框失焦、选中描边不过渡）。新增 `morph()`：把新 HTML 对比后只改变化的节点，相同节点保留（焦点、滚动、CSS 过渡都在），新增的区块淡入；sheet 模式同样适用，出错时退回整页重绘。视频卡按下缩放。**List a spare**：Continue / Review / 返回在切换动画期间（420ms）忽略重复点击（原来连点两下会跳过一步）；再点已选的票可取消选择；张数变化有滚动动画；滑动上架区和票卡禁止选中文字；最后一步 Done 和 View in Tickets 两个按钮原来超出屏幕两侧，现在平分一行。两个流程都支持 Esc（spare：返回上一步/关闭；clip：先收起键盘再关闭），点选项有轻震动 |
| M24.11 | v141 | Start a crew：边走边做一张小队票 + 按住盖章 | 主人问怎么让建队交互更有趣，同意推荐方案。**小队票**（ncMini，前三步顶部常驻，拼贴风格白色小票、两侧缺口）：第 1 步是「?」占位 + Pick a show；选演出时卡片里的图飞进票的图片位（ncFly）落地回弹；第 2 步点贴纸，emoji 飞到票右侧的贴纸位「啪」地贴上（压扁回弹）；第 3 步改人数，票上的座位圆点同步增减、新增的点弹出；进第 4 步时小票放大变成完整票根（ncGrow）。第 2 步副标题从重复的演出信息改为「Pick a vibe. It goes on your crew ticket.」。**按住盖章**：按钮改为「Hold to create crew」，按住 0.65 秒按钮内从左往右填满，松手太早按钮左右晃一下提示；完成后「CREW STARTED」印章砸到票上（票轻震），票根沿打孔线撕开下坠，约 1.1 秒后进入群聊。键盘（名字框回车、按钮 Enter/Space）直接盖章，不需要按住。尊重 prefers-reduced-motion（不飞、不晃，直接完成） |
| M24.12 | v142 | 座位圈 + meetup 定位针 | 第二轮趣味交互。**第 3 步人数**：刻度尺换成一排 8 个座位圈——第一个是自己的头像（下方「You」），其余是虚线空位；已选的座位白底黑虚线、未选的缩小变淡，增减时按顺序弹出/缩回（带回弹，错峰 18ms）；可点、可在整排上左右拖动、键盘 ←/→，最少 4 人；顶部小队票的圆点同步变化；下方提示「Tap or drag to add seats」。大数字保留。**第 4 步 meetup**：「Suggest a meetup」左侧加定位针，打开时针从上方落下（压扁回弹 + 地面小阴影），关闭时针向上飘走淡出。注意：类名不要用 `on` / `drop` 这类短名，`.drop` 与首页 This week's drop 的全局样式冲突过（曾把整行撑高并出现渐变），已改为 `pinon` / `pindrop` |
| M24.13 | v143 | 人数 2–8 + 座位排像滑块 | 主人：最低 4 人有问题；用户不知道怎么拖，需要指示。人数范围改为 **2–8**（2 = 你 + 一个 plus one；键盘 ←/→ 同步改为 2–8；旧的 ncSheet 里 4–8 的选择没动，新流程不用它）。座位排做成滑块的样子：背后一条灰色轨道，从你到最后一个选中座位的部分是黑色（宽度随人数过渡）；最后一个选中座位变成黑色「把手」，里面有 ‹ › 箭头、外圈浅灰光环，拖动时放大；第一次进入这一步时把手自动左右晃两下示范（之后返回再进来不再晃，一碰就停）；提示改为「Drag the handle, or tap a seat · 2 to 8 people」 |
| M24.14 | v144 | 去掉三个 ＋ 流程右上角的装饰图形 | 主人问建队页右上角的黑圆是什么——那是 M24.2 的流程标记（＋ 菜单里对应的形状：建队黑圆、挂票灰方块、分享片段旋转星星），纯装饰无功能。主人先要求去掉建队的，随后「全部去除」。三处都已删除：建队和 Share a clip 的 header 第三格换成空占位（进度条/标题位置不变），List a spare 的灰方块 `.sellx .whead>span` 设为不显示。`.flmark` 相关 CSS 已无引用 |
| M25 | v145 | ＋ 菜单：新形状 + 更好的下落回弹 + 去掉五颗星 | 主人：下落和回弹动画再优化、去掉五颗星、形状更独特。**五颗星**：是类名冲突——分享片段的形状类名 `st` 和全局评分星星 `.st::before{content:'★★★★★'}` 撞了，现在只在 ＋ 菜单内关掉（`.pfan4 .pk.sh.st::before{content:none}`），其他地方的评分星星不受影响。**形状**（仍黑白灰，SVG 画在按钮里）：Start a crew = 三个圆叠成的「一群人」（黑）；List a spare = 两侧有缺口、右边有虚线撕口的票（浅灰）；Share a clip = 竖版视频卡，左上播放键、底部进度条（灰），不再旋转。位置往里收，三个都不被屏幕边缘裁掉；点击区域就是图形本身。**下落**（shDrop 重写）：落下顺序改为 片段 → 票 → 小队（最重的主按钮最后落地）；每个形状回弹系数不同（越小越弹：0.52 / 0.42 / 0.30）；下落时纵向拉长、落地压扁，用弹簧恢复；旋转、横向漂移、压扁都用弹簧（会晃几下再停稳），不再到某个速度就突然停住；每个形状第一次落地轻震一下；约 2 秒全部停稳后进入原来的漂浮动画。卡片副标题「4–8 people」改为「2–8 people」 |
| M25.1 | v146 | ＋ 菜单点选后的过渡 | 主人：点三个按钮之后的过渡不好。原来：选中的放大、另外两个缩小消失，0.3 秒后整页硬切到流程（模糊背景、标题、图形一帧内消失）。现在（pkPick，约 0.62 秒）：没选中的两个像重力一样掉出屏幕底部（带旋转，错峰），标题和提示淡出；选中的停止漂浮、摆正并弹一下（scale 1.12，带阴影）；0.16 秒起，一个和 ＋ 流程同样点阵底色的圆从选中图形中心向外展开（`.pkwipe`，clip-path，在图形下面、模糊背景上面）；0.46 秒选中图形缩小淡出「钻进」页面；0.62 秒渲染流程——底色一样，所以没有跳变，流程自己的进场动画接着播放。注意：圆要插在 `#psheet` **之后**（用 z-index 6 压在它下面），插在前面会打断 `.pfbg:has(+ .pfan4)` 让模糊背景的白色蒙层瞬间消失。减少动态效果时直接进入 |
| M25.2 | v147 | Share a clip 改成发布页布局（保留拼贴风格） | 主人：这个不像正规软件。选「重排成发布页」。标题改为和建队一样的一行小标题（What was the moment?）。csSheet 主体重排：①顶部白色卡片＝左边选中片段的预览（带播放三角和时长；Text only 时显示 Aa）+ 右边说明输入框（textarea，placeholder 改为「Add a caption…」，不再和标题重复；字数在右下）；②「Clip」一排切换片段 / Text only；③一张白色列表卡：地点行（定位图标 + 场馆 + 来源 + Change；没地点时「Add the venue · Required」；选场馆时展开场馆列表行）、演出行（缩略图 + 演出 + 日期，多场时显示选择胶囊，没有演出时提示行）、评分行（★ 图标 + Rating + 右侧五颗星，评分文字显示在副标题，如 Great night）。点阵背景、黑白灰、底部 Post 按钮不变。从演出页进入的「How was …?」评价弹窗也用同一套布局（卡片底色为浅灰）。id（cscap / cscnt / cspb）和所有 data-act 保持不变 |
| M25.3 | v148 | Share a clip 按市面发布页重做 | 主人：参考市面上发布视频/动态的 App，现在感觉很假。参照 TikTok 发布页、Instagram New reel、小红书发布笔记的共同结构重写 `csPage`（＋ 菜单进入的页面；演出页的「How was …?」评价弹窗仍用 M25.2 的 csSheet 布局）：顶部导航栏（左关闭、居中小标题 New clip / 纯文字时 New post，去掉大标题和宣传副标题）；说明输入在左、视频封面在右（右上时长、底部「Change」，纯文字时显示 Aa +「Add clip」），点封面弹出「Choose a clip」相册式三列网格（Text only + 最近视频，有定位的带图钉）；输入框下「# Hashtag」「@ Mention」在光标处插入，右侧字数；分组设置卡：Location 行（值 + 箭头，没地点时「Add · Required」，下方「From your video’s location」提示和横向推荐场馆胶囊，点行展开全部场馆）；Show 行（自动匹配，多场时胶囊选择）；Rate the night（右侧五星）；Who can see this（Everyone / Your crews / Only you，点一下切换并提示）；如果你在这场演出的小队里，多一行「Also send to 〈小队名〉」开关，发布时把「🎬 + 说明」发到该小队群聊。底部双按钮：Drafts（存草稿并关闭，下次打开 Share a clip 自动恢复并提示 Draft restored；发布后清除）+ Post（没地点时禁用并显示 Add a location to post）。保留点阵背景和黑白灰；＋ 菜单的圆形展开过渡仍然无缝衔接 |
| M25.4 | v149 | Share a clip 两步流程 + 草稿 + 离开确认 | 主人：继续优化流程及步骤。按真实 App 的步骤拆成两步（`state.cs.stage`：pick / compose，切换时左右滑入）。**第 1 步 选片段**（csGallery）：顶部 X + New clip；大预览（9:14，时长、播放三角）；下方说明这段视频里读到的地点（「📍 Radio City · Sep 26 · location found in the video」，没有定位时提示下一步选场馆；纯文字时提示下一步标场馆）；Recents 四列网格（Text + 最近视频，选中有黑框和 ✓）；底部 Next。**第 2 步 发布详情**（csCompose，即 M25.3 页面）：左上改为返回箭头，点封面也回到第 1 步（不再弹相册弹窗），说明文字保留。**草稿**：不再自动恢复；打开时第 1 步顶部显示「Unfinished draft」卡（缩略图 + 说明 + Discard / Continue），Continue 直接进第 2 步；正在编辑草稿时不显示这张卡；发布后清除。**离开确认**：有未保存内容（说明、评分、可见范围、手选场馆）时点 X 弹出「Leave this post?」：Save draft / Discard / Keep editing。**Post 按钮**：没地点时「Add a location to post」，场馆最近 3 晚没有演出时「No show here in the last 3 nights」（都不可点），不再点了才报错。Esc：确认框里=继续编辑，第 2 步=返回，第 1 步=关闭。注意：`.cover` 全局是 absolute，放缩略图的容器要 `position:relative` |
| M25.5 | v150 | Share a clip 参照小红书发布流程 | 主人：参考小红书的发布流程。两页都改成白底（小红书发布页是白的；＋ 菜单展开的圆对这个流程也改成白色，衔接无缝）。**第 1 步（相册）**：标题「Recents」，三列满宽网格（相册里的视频从 3 个补到 7 个：多出来的是没有定位的普通视频），每格左下时长、左上图钉（有定位）、右上选择圈（选中变黑并显示 1，图片稍暗）；网格下说明这段视频里读到的地点；底部左侧 Album / Text 标签，右侧「Next (1)」。不再有大预览（小红书相册页也没有）。**Text 标签（文字配图）**：直接在 3:4 卡片上写字（140 字），可选 Paper / Ink / Dots 三种底；卡片为空时 Next 会提示。切回 Album 恢复之前选的视频和地点。**第 2 步（发布笔记）**：左上返回；顶部媒体缩略图 +「+」格（都回到第 1 步）；标题行「Add a title — posts with titles get more likes」0/20；正文（视频 200 字 / 文字 280 字）；# Topic / @ Mention；推荐话题横排（#艺人 #场馆 #LiveMusic …，点了加到正文）；设置行（无卡片，细分割线）：Mark location（推荐场馆胶囊）、Show、Tag a song（只在有真实歌单时出现，点开选歌）、Rate the night、Visible to、Also send to 小队；底部 Drafts + Post。发布时说明 = 标题 · 文字卡 · 正文，歌和标题存进片段。给 Wave To Earth、Two Door Cinema Club 补了真实歌名（SONGS），没有歌单的演出不显示选歌，避免出现「The big single」这种占位名。卡片样式类名用 `cps0–2`（避开短类名冲突） |
| M25.6 | v151 | Share a clip 加「编辑」步骤（参照小红书） | 主人同意做小红书的编辑步骤。流程变为 相册 → 编辑 → 发布笔记（`stage`：pick / edit / compose，左右滑动）。**编辑页**（csEdit，黑底，状态栏变白）：左上返回、中间 Edit、右上白色 Next；9:16 预览；底部工具栏：Filter（Original / Mono / Fade / Night / Warm 五个缩略图）、Text（在视频上打字，最多 40 字，可删除）、Sticker（沿用评论区的 12 个演唱会贴纸：ENCORE!、I WAS THERE、10/10、🔥…，一条只放一个，再点取消，落下有弹跳）、Song（只在这场演出有真实歌单时出现，选中后左下显示「♪ 歌名」）。贴纸和文字可直接拖动；拖动范围限制在上方 60%，底部 40% 留给信息流的说明文字（文字默认放在中间偏上）。纯文字帖只有 Sticker / Song。**带到后面**：发布页封面缩略图按比例显示滤镜、贴纸、文字和 ♪；点封面回到编辑，点「+」回到相册。发布后的片段保存 fx / stk / ovl 及位置和歌名，Clips 信息流里你自己的片段会显示滤镜、贴纸、文字（歌名走原来的滚动歌名）。草稿也会保存这些编辑。注意：`.pgf` 有更具体的背景规则，深色/白色底栏要写成 `.pgf.xxx` 才能覆盖 |
| M26 | v152 | Find me a crew（自动匹配 + 等待池） | 主人同意按「市场与风险」分析优化。解决冷启动：用户不用面对空列表。入口：建队第 2 步（选完演出和方式）底部改为两个按钮「Start my own」/「Find me a crew」（主按钮），副标题改为「Pick a vibe. We’ll match you…」；演出页 Crews 区新增黑色「Find me a crew · 我们按方式匹配 · N people looking」行。新页面 `mt`（拼贴风格）：顶部演出 + 方式小票；①搜索（雷达动画，「Checking N crews forming…」约 1.5 秒）；②有同方式、未满、不是自己的小队时显示「We found a match」：小队名、成员头像、剩余名额、匹配理由（同方式、全员持票、房主到场率、集合时间地点），按钮 Keep looking / See crew（进入原来的加入预览）；③否则进入等待池「You’re in the pool」：3 个座位（你 + 空位），显示「N people looking · M want 同方式」，约每 2.6 秒有人加入（演示），满 3 人自动成队「Your crew is ready」→「Open crew chat」，自动创建群聊（系统消息说明匹配原因 + 第一条欢迎）。在池中关闭页面会继续排队，成队时 toast 提醒，群聊带未读。按钮：Leave pool / Invite a friend（复制链接）。 |
| M26.1 | v153 | 加入前的信任信息 + 演出后到场确认 | 加入预览（xjPrev / scPrev）顶部新增信任条：这支小队成员的真实合计到场率（按 REL 计算，如 92%）、Tickets verified（或 IDs checked）、Public meetup、有押金时「$5 hold · refunded」。Chats 里「Last night’s crew」先变成「who made it?」：新的第一步「Who made it? 🎟️」，每个成员可选 Showed up / No-show，确认后更新每个人的到场记录（REL），提示有几个 no-show（只有小队可见）；你的记录从 8/8 变成 9/9（`MESU()`，资料页和认证徽章同步）。之后才进入原来的 Keep in touch，且只列出真正到场的人。 |
| M26.2 | v154 | 把小队带回来 + 年度现场回顾 | **Activity 新提醒**（铃铛未读数随之增加）：①「Wave To Earth has another night · Radio City, Sep 29 · Dev, Ines and Ana from last night’s crew are interested」（只列确认到场的人）→ 点了直接用这些人重组小队群聊（reCrew）；②「2 of your buddies are going to Steve Lacy · Oct 10 · start a crew with them?」→ 进入 Find me a crew；③「Your 2026, live is ready」→ 打开回顾。**Your 2026, live**（新页面 `wr`，黑底，类似 Spotify Wrapped）：顶部 6 段进度条，每页 5 秒自动前进，点右侧下一页、点左侧上一页，右上关闭；6 页：开场拼贴、23 场、9 个小队 + Showed up 记录、你的方式、最常一起看的人（3 场）、汇总卡（23 / 9 / 14 / 到场记录 + 下一场）+「Share your year」。数字与资料页一致。资料页名字下方加入口卡片「Your 2026, live」。 |
| M26.3 | v155 | 流程逻辑检查与修复 | 主人：继续优化，找不完善 / 不合逻辑 / 页面有问题的流程。先静态检查：229 个 data-act 都有处理（没有死按钮）。再逐个走流程，修了：①**一场演出只能在一个小队**：原来已在 Gorillaz「Solo, not alone」里，演出页仍提供 Find me a crew，匹配后会同时在两个小队；现在演出页先显示「You’re in 〈小队〉· Open the crew chat」并隐藏 Find me a crew；从别处进入匹配时先出现「You’re already in a crew」页（Open 它 / Find a new one），新建、匹配、重组都走同一规则 `leaveOldCrew`：离开旧小队并在新群里写「You left X · only its host was told」（和原来 joinCrew 一致），建队第 2 步提示也说明会移出。②**重组不再重复**：同一场已有「Same crew, again」时直接打开它。③**匹配 / 重组得到的小队会出现在演出页和 Explore 列表**（写入 MINE）。④**Explore** 顶部「N people are going solo」条加「Find me a crew」按钮。⑤**＋ 菜单** Start a crew 副标题改为推荐「有票但还没小队」的演出，没有就显示「2–8 people · any show」（原来推荐了已经有小队的 Gorillaz）。⑥**Clips 卡片**：上一晚的片段按钮其实跳到下一场，文字从「Last night」改为「Plays again Sep 29」。⑦**小队数**不再写死：资料页、回顾卡、回顾页、Activity 都用 `MECR()`（9 + 本次新加入/新建/匹配/重组的小队）。仍未复现：主人早先提到 Chats 点不进去 |
| M27 | v156 | 让面值换票成为主卖点 | 主人：换票是卖点但不突出。**①首页最上方新模块「Never pay double 🎟️」**（居中标题，「Spares from verified fans at face value · N live now」）：一行说明「Fans here save about $X a ticket vs resale (est.)」，横向余票卡（演出图、Save $X 标签、价格 + 删除线的估算转售价），末尾「See all」格跳到 Spares；下面「Have an extra? Offer it to your crew at face value」入口。**②演出页**：没票且有余票时底部主按钮变为黑色「Face value · $X」（直接打开最便宜那张的购买确认），Join the show chat 变成次要按钮；Spare tickets 区顶部加黑色条「Never pay double · Face value + $2 flat」+ 估算转售价对比。购买确认里加「about $X less than resale (est.)」。**③买方需求**：原来的「Notify me」改为「Request a ticket」，显示「You’re #N in line · crew-mates get first dibs」；Spares 页新增「Your requests」列表（可取消）；挂票第 1 步显示「N fans have requested tickets for your shows」。**④信任**：Spares 页顶部「How a swap works」三步（Claim it 我们托管 / Seller sends it 官方转让 / It lands 才放款）+「$2 flat, nothing else. Typical resale sites add 20–30% in fees…」。**⑤卖票时机**：My tickets 里「Can’t make a show? Offer your ticket to your crew first」→ 挂票流程。注意：demo 没有真实转售价格，`RESALE()` 按面值 2.0–2.8 倍估算，所有地方都标「est.」；做成真产品需要接入真实价格数据 |
| M27.1 | v157 | 去掉说明性文字 | 主人：备注文字太多、影响使用，应该隐藏。**原则：界面只留标签和数字，解释收进 ⓘ（infoB → INFO 弹窗）。** 删除 / 缩短：首页「Fans here save about…」、余票副标题改为「22 live now ⓘ」、「Have an extra? List it at face value」；首页底部数据来源说明改为小链接「About this demo」（新 INFO.demo）；演出页「Never pay double」下的小字、「Everyone going to this show, in one place」、Find me a crew 行改为「N people looking」；Spares 页整块「How a swap works」移进 ⓘ（INFO.tickets 新增「$2 flat, nothing else」「Your real ticket stays put」两条），sprule 末尾加 ⓘ，请求行去掉「crew-mates first」；My tickets 底部说明移进 ⓘ，Can’t make a show 副标题改「Offer it to your crew first」；Explore「Start one for any show」；建队各步标题下的解释句全部去掉，人数提示改「2–8 people」，可见范围说明改「Shown on Explore / Only people with the link」，已在小队提示改「A new crew moves you out of it.」；Find me a crew 搜索页改「N people looking ⓘ」（新 INFO.match 讲匹配和等待池），等待池去掉「You can close this…」，成队后去掉提示句；Share a clip 编辑页三条拖动/歌单提示全部删除，相册地点提示去掉「found in this video」；Who made it 副标题只留「Last night · 演出」。保留：演出简介、AI 评论摘要（内容本身） |
| M28 | v158 | 首页：Up next 卡片 + 待办 | 主人：优化首页 UI。首页最上方新增黑色「Up next」卡（nxHome）：你下一场有票的演出（图、「In 2 days · Tue」、艺人、你的小队名、小队成员头像），小队计划的集合时间和地点，按钮「Crew chat」/「Ticket」；没有小队时按钮变为「Find me a crew」；没有任何票时显示搜索框「Which show are you going to?」。卡片下方只在有事时出现的待办胶囊：「Who made it? · 演出」（打开到场确认）、「Pool · N more to go」/「Crew ready」（回到匹配页）、「N ticket requests」（去 Spares）。「This week’s drop」改名「Hot this week」并去掉副标题，Scenes 去掉副标题，Upcoming 副标题改为「N shows」。顺带修了数据不一致：Tickets 页 Up next 原来写死「Meet 6:15」，现在读小队真实计划（Gorillaz 是 7:30 PM）。余票模块没有做个性化排序：目前只能对「没有余票」的演出发请求，没有可用的个性化信号，就按最新排序 |
| M28.1 | v159 | 首页缩短 | 主人：首页太长。首页高度 2082px → 约 1360px（约 1.6 屏）。去掉「Upcoming in New York」整块演出列表（737px，和 Explore 重复），换成一行「All N shows in New York ›」跳到 Explore；去掉余票模块下的「Have an extra? List it at face value」（＋ 菜单和 My tickets 都有挂票入口）。首页现在：Up next 卡 + 待办 → Never pay double → Hot this week → Scenes → All shows → About this demo。原来的筛选（This week / This month / Filters）和分页代码还在，只是首页不再渲染 |
| M29 | v160 | 视觉风格定义：Monochrome Editorial | 主人：喜欢简洁时尚风，要定义并优化视觉风格。新增 **docs/STYLE.md**（补充 DESIGN.md，冲突时以它为准）：颜色（Ink / Paper / Canvas / Fog / Muted / Line，照片是唯一彩色）、字号层级（Page 26 / Section 20–22 / Flow 30+31 斜体 / Body 15 / Meta 12.5 / Label 11 大写）、圆角三档（12 / 20 / 胶囊）、主按钮 52 高黑色胶囊、单一阴影、版面间距、动效原则（平时安静，只在标志性时刻好玩）、品牌记号（三形状 + 票根打孔线）、＋ 流程的拼贴例外、新页面检查清单。按规范统一：13 个标题里的 emoji 去掉（只保留 Scene 页标题的 Scene emoji）；建队流程里 4 处黄色（#FFF3A8 / #FFF7C2：日期贴纸、「已有小队」便签、空状态便签、旧日期标签）改为白色 + 细描边；所有 .cgo / .wpill / Up next 按钮改为胶囊圆角；List a spare 标题从 42px 海报字改为 30px 紧凑字 |
| M30 | v161 | 首页改成杂志感（解决「无聊」） | 主人：首页设计很无聊。原因是每块都是「居中标题 + 一排卡片」，没有节奏和焦点。改成杂志封面 + 排行榜的节奏（仍黑白、少文字、功能不变）：**Up next 变成封面**——下一场的大照片铺满（高 380，缓慢放大），左上「UP NEXT」毛玻璃标签，右上超大倒计时数字「2 / DAYS」（当天显示 Tonight），左下大号艺人名、小队头像 + 小队名、毛玻璃集合点条、Crew chat / Ticket 按钮叠在照片上。**Hot this week 变成榜单**（hotChart）：01 大图卡（大号编号压在图上），02–04 带超大编号的列表行（缩略图、艺人、日期场馆、右侧 looking 数），**按显示的 looking 数严格排序**（原来的 DROPS 顺序和数字对不上，看起来是假的，已改）。**余票卡变成海报价签**：整张照片 + 渐变，白色「Save $X」标签，超大白色价格 + 删除线估算价，底部艺人和日期。首页高度约 1760px（原始 2082，上一版 1361）。旧的 dropCard 轮播代码保留未删，不再渲染 |

## 6. 链接（原账号所有，新账号只能查看）

- Demo（v68）：https://claude.ai/artifact/5pxYwP6SnNRQXat92kY3JP
- 迭代对比页（M1–M6）：https://claude.ai/artifact/D8wed6wb4zvV9B9sxbqpiM
- 用户研究 PPT（42 页）：https://claude.ai/artifact/V4NnC5gTxafRHiCo7XRydf
- 研究文档（初版）：https://claude.ai/code/artifact/76fd72bb-151d-4eab-a99e-9d06a97670e3
- Figma：文件 `Dp01oskPNang2AfFHIJkUp`，页面节点 `1343:11953`（"Plus One — Iterations"）
  - M1–M5 为 390×844 截图
  - M6 分区 `1353:11953` 里有 19 个 393×852 空矩形（`1353:11959 … 1353:12013`），**截图还没传上去**（19 张截图就在 `iterations/shots/`，文件名与画框一一对应）

## 定位共识（M8）

- **首页不大改**：主人对首页满意，只做被明确要求的小改动。
- **Plus One 不卖票**：原价票跳 Ticketmaster（Buy tickets ↗）；只撮合粉丝间多余票按面值转让，小队优先，过户走官方渠道。

- 找搭子和面值票单独都不是壁垒（Radiate、ConcertBuddy、Ticketmaster × CashorTrade 都在做）。
- 差异化落在「一定会一起到场的小队」：持票身份、到场记录（会累积的数据）、小队而非配对、多余票优先给小队、小队可延续。
- 原则：信任看得见但不强制。默认零门槛，押金/集合点都是可选项，只有女性专属必须认证。
- 不做几百人的演出大群；每个小队有 4–8 人上限，满了自动开新队。
- 片段社区 Clips（M17）：谁都能发，但每条片段必须带场馆位置标签（视频定位自动识别 On-site，或手动 Tagged）；评论、回复对所有人开放，持票者只加标记；每条都挂着演出与「Find a crew」，内容服务于组队。
- 不做全站广场：公开内容只存在于每场演出的 Show wall，且只有持票人能发；热搜只来自组队行为，不接受投放。

## 决策记录与 Figma 同步

- 讨论中的所有关键决定（含被否的方案）：`docs/DECISIONS.md`
- Figma（M6 起）之后的全部改动，按页面：`docs/CHANGES-SINCE-FIGMA.md`；当前 23 张页面截图：`docs/screens-v96/`（`demo/tests/capture_all.py` 可重新生成）

## 7. 待办

1. **Figma**：把 M6 截图上传到 M6 分区的空矩形；新增 M7 分区并上传截图。
2. **迭代对比页**：加入 M7（`iterations/` 下新增 `m7.html`，并更新 `index.html`）。
3. **PPT**：M7 页（`deck/slides/m7.html`）可随后续迭代更新；fit 评分页（`fit`）在 M6 时是 7 个满足 / 4 个部分满足 / 3 个未满足，M7 之后可以重新打分。
4. ~~首次使用流程~~：M23 已完成（`onb` 屏）。
5. **Figma 可编辑版**：页面「Plus One — v96 editable」只建好 01 首页；其余页面需按最新版本重新抓取后再建（工具在 `figma/`）。
6. 可选方向：＋菜单里建小队时可选演出（目前默认 Harry Styles）；Explore 中「Find a ticket」与 Tickets 页的 Spares 合并；把 demo 迁到 `app-expo/` 做成真实 App。

## 8. 安全与注意事项

- **Ticketmaster API key 不在仓库里**，也绝不能放进任何发布的页面。需要实时数据时，新账号去 https://developer.ticketmaster.com 申请自己的 key，放进 `app-expo/.env`（根目录 .gitignore 已忽略 .env），或作为本地环境变量使用。
- **两个构建**：`python3 demo/build.py` → `demo/dist/plusone-demo.html`（单文件 10.7MB，含视频，可离线/在 Claude 预览里打开）；`python3 demo/build.py --web` → `demo/dist-web/index.html`（0.6MB）+ `img/`（提交到仓库）+ `clips/`（不提交，Vercel 用 `/clips/*` 重写到 `demo/clips/`）。线上 Vercel 用的是网页版，改完模板两个都要重新构建。
- `demo/` 的演出数据是静态快照（2026 年 9 月抓取；如何刷新见 data/merge_tm.py：用自己的 key 调 Discovery API，按列写入 .psv 再运行脚本），日期以 2026-09-27 为「今天」计算（见 `xDays`）。
- 头像为 Unsplash 图片，仅用于作品集演示。
