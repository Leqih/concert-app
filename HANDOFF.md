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
| M21 | Crews: no more walking straight in. Start a crew as **Invite only** (default, link) or **Ask to join** (listed; host approves each request in the chat with Approve/Decline). Explore, show page and scene page buttons are now Ask to join → Requested → Open. Show chat stays open to everyone |
| M22 | Chat pages redesigned (one skeleton, three roles). **Show chat = plaza**: header + “At the venue now” avatars + topic cards (Find a crew first); tap a topic for its chat (topic tabs, 🎫 seat badges, “Message # topic”). **Crew = ticket stub**: photo stub with countdown + members, pinned meet / spare / $5 pills, quick actions that change after check-in, host Invite + join-request cards. **DM = business card**: profile card (city, verified, shows, show-up, mutual, “You’re both going”), quick actions Invite to my crew / Share ticket; tapping a request opens it with Accept / Delete / Block · Report. Classes prefixed `k` (`.ktop`, `.kstub`, `.ktpc`, `.kcard`…) |
| M22.1 | Chat polish: emoji swapped for line icons (topic tiles, pins, quick actions, seat badges); quick actions are compact pills; system lines are quiet grey text; reply quotes are a thin left bar; ticket stub uses a dashed tear line; DM header shows just Active now |
| M23 | Chats v2 — Leqi: a group chat is not a forum, and the UI looked poor. Show chat is now ONE continuous group chat (no topics). All three chats share one messenger layout: frosted header (back · cover/avatar · name · status · ⓘ), one pinned bar (Show chat: Find a crew → crews sheet with Ask; Crew: meet time/spot, doors, spare, $5 hold + Hold $5 / I’m here), solid dark bubbles on a heavily blurred backdrop, quick chips, one composer. Crew header subline has the countdown. DM keeps the profile card and request Accept/Delete |
| M24 | Public vs private (Leqi): Explore, show page and scene pages list **public show chats** (one per show, anyone can join). **Crews are private**: no public listings anywhere; create from Chats (＋) and join only with an invite (Requests → Crew invites) or by typing the **crew ID** (e.g. #PC-9321) in Chats search → Ask to join → host approves. Host Invite sheet shows the crew ID, copy link and people to invite. Show chat has no pinned bar. Create sheet: invite only. Old crew-listing code (xRow/xCard/scPrev) is now unused |
| M24.1 | Crew names sound like real group chats (lowercase, inside jokes, emoji): hs pit people 🤘, doja ramen night 🍜, gorillaz solo squad, rail or die, after?? 🪩 … The create sheet has a Name field (placeholder suggests one per vibe) |
| M24.2 | Show chats are official and numbered (Leqi: like 演唱会一群/二群): `scName(x)` = “Artist · Venue m/d · Group N”; groups hold 2,000 (`SC_CAP`), you land in the newest open group; the chat opens with an “Official chat for … · Group 1 full, you’re in Group 2” line; counts read “1,430 / 2,000 members”. Removed leftover topic tags from the show page chat card |
| M25 | Chat types are obvious everywhere: **Official show chat** (badge icon next to the name, square cover), **Private crew** (lock icon, two-face group avatar, “Private crew · Artist · 4/6”), **Direct message** (chat icon, round avatar). Same labels in the Chats list; tab Shows → Official. Crew countdown moved into the pinned plan bar. New icons: `lock`, `badge` |
| M25.1 | Crew names start with a capital letter (Harry pit people 🤘, Rail or die …); names typed in the create sheet are capitalised too |
| M26 | Chats → chat open animation (shared element), `cbGo()` in two beats so nothing flashes white: over the still-visible list the tapped bubble grows to the phone frame and darkens to the chat colour (340ms) while its avatar heads for the header; then the chat renders underneath, the ghost fades and the avatar settles onto the header avatar. Checked frame by frame from a recorded video (brightness never jumps). Works for crews, DMs, show chats and requests; skipped with reduced motion |
| M26.1 | Back animation (chat → Chats), `cbBack()`: the list renders underneath, the chat shrinks back into its bubble while fading and turning the bubble’s colour, and the header avatar flies back to the bubble’s avatar. Falls back to a fade when the bubble is off screen |
| M27 | Chats header: title row, then one row with an always-visible search pill (“Search chats or a crew ID”, clear ✕) and a black ＋ (new crew). Focusing search outlines the pill and swaps ＋ for Cancel; the crew-ID hint shows under it |
| M28 | Chat features. **Info sheet** (tap the chat name or ⓘ): show chat = members with seats, shared photos, Mute / Search / Show, Leave Group N; crew = crew ID + Copy, members (Host, verified, show-up), shared, Mute / Search / Invite or Show, Leave crew; DM = Profile / Mute / Search, going together, shared, Block / Report. **Mute** shows a bell-off next to the name (header + Chats list). **Search in chat** swaps the header for a search field, filters to matching messages and highlights them. **Show chat**: “New messages” divider on first visit (opens there), ↓ jump-to-latest button, “@ 1 mention” pill that scrolls to and flashes the message. **Sending**: @mention suggestions while typing (crew members / DM person / show chat people), mentions in bold (yours highlighted); photo attach shows a preview strip with caption; mic button records a voice note (timer + live waveform, ✕ / send) and voice bubbles play; Poll from ＋ in crews (question + 2–4 options, live percentages, change vote). #app scroll is pinned to 0 so focusing inputs in sheets can’t shift the phone |
| M29 | Flow audit fixes. **Conflicts with private crews**: Home “See crews” → Join chat; Clips “Find a crew” → Join chat (opens the show chat); buddies “Join them” → Ask to join (they add you, then Open); spare cards say “Seller’s crew first” / “N online in the show chat” and Crew first explains the rule; trending and ＋ copy no longer say “crews forming”; clipboard errors swallowed. **New paths**: Activity (bell in Chats header + Me) collects invites, approvals, mentions, join requests, ticket updates via `kNote()`; request outcomes (approved / filled up), Your requests in Requests with Withdraw / Dismiss; host tools in crew info (Edit meetup sheet, rename, remove member, End crew); lifecycle note (archives 7 days after the show); first-run onboarding (city → artists → who can message you + verify ID; artists picked join their show chats; `?noonb` skips; remembered in localStorage); Privacy & messages sheet from Me (DM rule, read receipts, blocked list with Unblock) |
| M30 | Onboarding + plus menu + design-system pass. **Onboarding**: poster fan on the welcome step, one header row (back / dots / Skip), fixed CTA bar, city list from `CITIES` with show counts (the pick now calls `setCity`), artists from the picked city; overlay fades in only on first open (`o.seen`) so Home no longer flashes on every tap. **Plus menu**: solid backdrop, stickers keep one tilt from drop to rest (no idle rotate/`will-change`, so tilted text is sharp), List a spare is a ticket stub, Start a crew shows faces, hover lifts/half-straightens the picked sticker via `translate`/`rotate`/`scale` and dims the others; fixed stray ★★★★★ (`.st` name clash). **Design pass**: tokens `--t-sheet`, `--live`, `--ease-*`, `--dur-*`, `--sh-1..3`; online dots all use `--live` (green #34C759, the second colour exception, owner's call); off-scale radii fixed; all chips 34; `.nb` 40; emoji only on section titles; `audit_full.py` updated (27 screens, `?noonb`, chip/sheet-title/emoji checks, `PW_CHROMIUM`) → `TOTAL ✗ 0`. See DESIGN.md §4–7. |
| M31 | Clip comments v2. Top / Newest sort (`cmListHTML`), creator's pinned note on top (`cmTops`), seeded comments never by the creator, black **Creator** tag vs light-grey **Was there**, "Creator liked" mark, reply threads (`cmReps` / `cmThread`, "View n replies", indented), Reply shows "Replying to … ×" and posts into that thread (`state.cmRep`, counted in `cmCount`), new top-level comments land under the pinned note, double-tap a comment to like it. |
| M32 | Plus-button flows. **Start a crew**: show picker lists "You have tickets" first, then upcoming, each with "n crews going"; form subtitle has **Change** (`ncrepick`); creating a crew opens the invite sheet straight away. **List a spare**: "Why are you selling?" label, left-aligned reasons, line icons (not emoji) on the Listed → Paid steps, lock icon in the wallet hint. **Share a clip**: clip → location → show → caption → rating (review from a show page keeps rating first). Fixed chips rendering digits as emoji keycaps (`.gch{font-variant-emoji:normal}`, was showing "Sep 2 9"). |
| M32.1 | Flow UI pass on the plus-button flows: shared context card `.csloc.fctx` (Start a crew show with Change; Share a clip location + matched show, other shows as "Not this one?" chips), quieter crew subtitle, outlined "Who can join", inputs on `--card2`, Share a clip footer is one full-width button (no Cancel), Optional / Required labels in one style. |

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
4. 可选方向：＋菜单里建小队时可选演出（目前默认 Harry Styles）；Explore 中「Find a ticket」与 Tickets 页的 Spares 合并；把 demo 迁到 `app-expo/` 做成真实 App。

## 8. 安全与注意事项

- **Ticketmaster API key 不在仓库里**，也绝不能放进任何发布的页面。需要实时数据时，新账号去 https://developer.ticketmaster.com 申请自己的 key，放进 `app-expo/.env`（根目录 .gitignore 已忽略 .env），或作为本地环境变量使用。
- `demo/` 的演出数据是静态快照（2026 年 9 月抓取；如何刷新见 data/merge_tm.py：用自己的 key 调 Discovery API，按列写入 .psv 再运行脚本），日期以 2026-09-27 为「今天」计算（见 `xDays`）。
- 头像为 Unsplash 图片，仅用于作品集演示。
