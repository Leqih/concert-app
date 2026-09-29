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
demo/                 ← 主作品：单文件 HTML 交互 demo（当前 = M16.6 / 线上 v91）
  demo2_tpl.html      模板源码（唯一需要改的文件）
  build.py            把数据注入模板 → dist/plusone-demo.html
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
- 模板里有 4 个占位符，由 `build.py` 替换：`/*SHOWS*/`、`/*AVATARS*/`、`/*CITIES*/`、`/*MAP*/`。
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
python3 demo/build.py                 # 生成 demo/dist/plusone-demo.html
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
- 不做全站广场：公开内容只存在于每场演出的 Show wall，且只有持票人能发；热搜只来自组队行为，不接受投放。

## 7. 待办

1. **Figma**：把 M6 截图上传到 M6 分区的空矩形；新增 M7 分区并上传截图。
2. **迭代对比页**：加入 M7（`iterations/` 下新增 `m7.html`，并更新 `index.html`）。
3. **PPT**：M7 页（`deck/slides/m7.html`）可随后续迭代更新；fit 评分页（`fit`）在 M6 时是 7 个满足 / 4 个部分满足 / 3 个未满足，M7 之后可以重新打分。
4. 可选方向：＋菜单里建小队时可选演出（目前默认 Harry Styles）；Explore 中「Find a ticket」与 Tickets 页的 Spares 合并；把 demo 迁到 `app-expo/` 做成真实 App。

## 8. 安全与注意事项

- **Ticketmaster API key 不在仓库里**，也绝不能放进任何发布的页面。需要实时数据时，新账号去 https://developer.ticketmaster.com 申请自己的 key，放进 `app-expo/.env`（根目录 .gitignore 已忽略 .env），或作为本地环境变量使用。
- `demo/` 的演出数据是静态快照（2026 年 9 月抓取；如何刷新见 data/merge_tm.py：用自己的 key 调 Discovery API，按列写入 .psv 再运行脚本），日期以 2026-09-27 为「今天」计算（见 `xDays`）。
- 头像为 Unsplash 图片，仅用于作品集演示。
