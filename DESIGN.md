# Plus One — 设计规范（M14）

以首页为基准制定，所有页面都遵守这份规范。代码里的 token 定义在 `demo/demo2_tpl.html` 样式表末尾的 `DESIGN TOKENS (M14)` 块。新写的样式请直接使用这些变量，不要再写新的像素值。

## 1. 基础

| 项目 | 规范 |
|---|---|
| 颜色 | 只用黑、白、灰。强调色为 `#0B0B0C`，页面背景 `--bg #F2F2F4`，卡片 `--card #FFF`，次级底色 `--card2 #ECECEF`，分隔线 `--line rgba(0,0,0,.07)`，次要文字 `--muted`。**唯一例外**：Clips 的点赞红心 `--like #FE2C55`（双击出现的心 + 已点赞状态，主人要求） |
| 字体 | 标题用 Inter Tight（`--display`），正文用 Inter（`--body`） |
| 画布 | iPhone 16，393×852；状态栏安全区 `--st` 54px，Home 指示条安全区 `--sb` 34px |
| 页面左右边距 | 卡片离屏幕边缘 12px，卡片内边距 12–16px，纯文字内容 16–20px |

## 2. 字号层级

| Token | 字号 / 字重 | 字体 | 对齐 | 用在哪里 |
|---|---|---|---|---|
| `--t-brand` | 32 / 800 | Inter Tight | 居中 | 只用于首页顶部的 PLUS ONE 字标 |
| `--t-hero` | 44 / 800 | Inter Tight | 跟随大图 | 全出血大图上的标题（演出页艺人名、场景页名称） |
| `--t-page` | 26 / 800 | Inter Tight | 居中 | 页面标题：Explore、Tickets、List a spare。**唯一例外：Chats 左对齐** |
| 页面副标题 | 13 / 400 | Inter | 与标题对齐 | 页面标题下方一行，灰色（`.wcity`） |
| `--t-section` | 26 / 700 | Inter Tight | 居中 | 页面里的板块标题（This week's drop、Scenes、Spare tickets、Crews going、Show wall、Going to） |
| 板块副标题 | 14 / 400 | Inter | 居中 | 板块标题下方，灰色（`.sub`），间距 3–4px |
| `--t-card` | 17 / 700 | Inter Tight | 左对齐 | 卡片或分组标题（Explore 演出组头、Trending 标题） |
| `--t-row` | 16 / 700 | Inter Tight | 左对齐 | 列表行标题（Upcoming 行的艺人名） |
| `--t-body` | 15 / 400–600 | Inter | 左对齐 | 正文、帖子、表单项标题 |
| `--t-meta` | 13 / 400 | Inter | — | 日期、场馆、说明文字 |
| `--t-label` | 12 / 600，全大写，字距 .06em | Inter | 左对齐 | 分组标签：日期分组（TONIGHT & TOMORROW）、月份（OCTOBER）、表单分区（VIBE、CREW SIZE）、搜索页分组 |

**位置**：所有一级页面（首页、Explore、Chats、Tickets、List a spare）的标题，顶部都在距屏幕顶端 66px 处。

## 3. 圆角

| Token | 数值 | 用在哪里 |
|---|---|---|
| `--r-xl` | 30 | 页面级大卡片（首页各卡、Explore 演出组、Trending、演出墙帖子、空状态卡）、底部面板顶部、演出页大图 |
| `--r-lg` | 20 | 单行卡片或横幅（Don’t see your vibe、Up next、余票卡、聊天置顶条、投票卡、小队行、票夹票面、认证卡） |
| `--r-md` | 18 | 卡片里的小块（Filters 类型卡、Browse by vibe、计划格子）、主按钮（Create crew、Join a crew）、帖子配图、分段控件 |
| `--r-sm` | 14 | 缩略图（Upcoming、Explore 组头、余票图、小队行图片） |
| `--r-xs` | 12 | 表单里的分段按钮（Crew size、Venue）、小提示框 |
| `--r-pill` | 999 | 所有胶囊元素：筛选 chip、标签、Join 按钮、搜索框、输入框 |

保留的特例：聊天气泡（22，带 8 的尾角）、场景页扇形小照片（12）、首页 Scenes 头像拼图（32）。

## 4. 组件约定

- **Chip / 筛选**：胶囊形，高 34；选中为黑底白字；数量放在文字后，灰色小字；无结果时变灰（opacity .35）并禁用。
- **主按钮**：黑底白字，高 52，圆角 `--r-md`。**次按钮**：白底，1.5px 黑色内描边。
- **行内操作按钮**（Join、Say hi）：胶囊形，高 32–34，白底黑描边；需要强调时改为黑底（Last spot）。
- **底部面板**：白色，顶部圆角 `--r-xl`，上方有拖拽条，标题居中 24；最下方固定主操作按钮。
- **空状态**：白卡片，圆角 `--r-xl`，一行粗体标题，一行灰色说明，下方一个主按钮。
- **动效**：入场用 0.32–0.46s、`cubic-bezier(.2,.8,.2,1)`，只做透明度 + 8–14px 位移；页面跳转用共享元素过渡；需要尊重 `prefers-reduced-motion`。

## 5. 自动检查

`python3 demo/tests/audit_full.py` 会打开 22 个页面和面板（整页滚动高度），检查：圆角是否只用 30/20/18/14/12/胶囊/圆形、文字和背景是否只有黑白灰、字体是否只有 Inter / Inter Tight、各级标题的字号字重和对齐。改完样式后跑一遍，输出里除上面的例外外不应有 ✗。

## 6. 首页

首页是这套规范的基准，整体保持不变，只做明确要求的小改动。
