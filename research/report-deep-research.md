# 用"信任"而非"孤独"撬动 Plus One

**核心结论：** Plus One 真正要解决的，首先是"这张票和这个人是不是真的"，其次是"开场前那段干等的时间有没有人陪"。"永不孤单"排在更后面。需求端的宏观证据很强。18–34 岁人群看演出最频繁，也最孤独：Cigna 2024 年测得 Gen Z 孤独比例为 **67%**，Gallup 测得 15–34 岁男性每日孤独比例为 **25%**。他们的价格压力也最大：LendingTree 2025 年调查中 **53%** 的人因票价放弃过喜欢的艺人，Gen Z 用 BNPL 付演出费用的比例为 **37%**。但把"换票＋找伴"合成一个产品的需求，目前只有行为层面的旁证，没人直接说出"我想要这样一个 app"。

用户原声编码（北美 n=50）显示，票务侧最高频的主题是被骗（**20%**）和信任信号（**18%**）；抱怨手续费的只有 **8%**。社交侧的痛点和收获几乎持平：没人一起去 12%、独自尴尬 12%，与之相对，结识他人 16%、享受自由 12%。

竞争和监管面给出三条硬约束。第一，只有票务商自有的 Face Value Exchange 和 DICE wait list 能做到零费原价；第三方原价平台的买家实付通常高出 10–15%。第二，第三方 app 无法绕开 SafeTix 等转让控制，拟议中的 MAIN Event Act 还可能把绕开控制的行为纳入 BOTS Act。第三，Lyte 的倒闭（融资约 5300 万美元）和 IRL 的倒闭（95% 用户为机器人）说明，原价生意利润薄，虚假活跃则致命。

因此设计方向应当是：以原价换票作为获客工具，在官方转让之上叠加托管和身份核验，社交部分采用"按场次组 4–6 人小队、只陪开场前"的轻承诺模式。有待验证的核心假设有三个：原价换票的供给密度、"卖给愿意同去的人"的真实意愿，以及女性对陌生人同行的安全阈值。

> 方法与口径说明：本报告基于四份研究笔记（粉丝行为量化、转售机制与法规、竞品拆解、用户原声编码），外加本对话前期桌面研究的背景数据。前期数据在文中单独标注，本轮没有逐条复核原始链接。所有表格都注明单位、样本量、实地调研时间和来源，可以直接转成幻灯片图表。标"［推算］"的数字由笔记中的原始数据计算得出，不是出处原文。

---

## 需求端：主力人群同时处在"最常去、最孤独、最缺钱"的交叉点

Plus One 的目标人群（18–34 岁北美乐迷）在三个维度上同时处于极值，这是需求最扎实的部分。

**市场规模在扩大，但每场观众数基本持平。** Live Nation 的全球观众从 2022 年的 **1.21 亿**增长到 2025 年的 **1.59 亿**（[Live Nation FY2022](https://newsroom.livenation.com/news/live-nation-entertainment-reports-fourth-quarter-full-year-2022-results/)；[Live Nation FY2025](https://news.livenationentertainment.com/news/live-nation-entertainment-full-year-and-fourth-quarter-2025-results)）。场均观众在这几年里只从约 2,775 人变为约 2,890 人［推算］，说明增长主要来自场次增加。这对 Plus One 意味着，每场演出的潜在匹配池并没有变大，冷启动时的密度问题不会因为行业景气而自动缓解。跨城观演很普遍：Bank of America 2025 年调查中，**50%** 的受访者过去两年曾为演出出州或出国，千禧一代为 **70%**（[eMarketer](https://www.emarketer.com/content/2025-will-record-year-concertgoing)）。人去了别的城市，身边的朋友往往就不在了，"为这一场找伴"的场景由此产生。

**表 1　Live Nation 观众与票量时间序列（适合做折线图）**

| 年份 | 全球观众（百万人） | Ticketmaster 收费票（百万张） | 场次 | 来源 |
|---|---|---|---|---|
| 2019 | ≈98［推算：121÷1.24］ | ≈219［推算：280÷1.28］ | — | [FY2022 release](https://newsroom.livenation.com/news/live-nation-entertainment-reports-fourth-quarter-full-year-2022-results/) |
| 2022 | 121 | 280 | 43,600 | 同上 |
| 2023 | 145（未核实） | — | — | [FY2023 release](https://news.livenationentertainment.com/news/live-nation-entertainment-reports-full-year-and-fourth-quarter-2023-results)（仅检索摘要） |
| 2024 | 151 | — | — | [SEC 99.1](https://investors.livenationentertainment.com/sec-filings/all-sec-filings/content/0001335258-25-000027/lyv-2024q4xex991er.htm) |
| 2025 | 159 | 346 | ≈55,000 | [FY2025 release](https://news.livenationentertainment.com/news/live-nation-entertainment-full-year-and-fourth-quarter-2025-results) |

年轻人的孤独集中度，是"找伴"功能成立的人口学基础。Cigna 2024 年的调查（实地调研 2024 年 5 月 29 日至 6 月 14 日，报告于 2025 年发布）显示，孤独比例随年龄单调下降，从 Gen Z 的 **67%** 降到婴儿潮一代的 **44%**（[Cigna 2025 报告](https://filecache.mediaroom.com/mr5mr_thecignagroup/183661/2025-loneliness-in-america-report-the-cigna-group.pdf)）。Gallup 的数据给出了更细的性别切分：**15–34 岁男性每日孤独比例为 25%**，是所有年龄性别组中最高的，远高于 OECD 中位数 15%；同龄女性为 18%（[Gallup, 2025-05](https://news.gallup.com/poll/690788/younger-men-among-loneliest-west.aspx)）。Pew 的数据显示，30 岁以下有 5 个以上密友的人只占 **32%**，65 岁以上为 49%（[Pew, 2023-10](https://www.pewresearch.org/short-reads/2023/10/12/what-does-friendship-look-like-in-america/)）；50 岁以下经常感到孤独的比例为 **22%**，50 岁以上为 9%（[Pew, 2025-01](https://www.pewresearch.org/social-trends/2025/01/16/men-women-and-social-connections/)）。这里有一个此前被忽视的细分人群：**年轻男性在孤独维度上最突出，女性在安全维度上最突出**。两者对产品的诉求方向相反，界面和默认设置需要分别照顾。

**表 2　孤独感按世代（适合做柱状图）**

| 世代 | 孤独比例 | 样本 | 实地调研时间 | 来源 |
|---|---|---|---|---|
| Gen Z | 67% | n>5,000 美国成人（Advisory Board 摘要称 7,500+） | 2024-05-29 至 06-14 | [Cigna](https://filecache.mediaroom.com/mr5mr_thecignagroup/183661/2025-loneliness-in-america-report-the-cigna-group.pdf) |
| Millennials | 65% | 同上 | 同上 | 同上 |
| Gen X | 60% | 同上 | 同上 | 同上 |
| Boomers | 44% | 同上 | 同上 | 同上 |

**表 3　每日孤独比例：年龄 × 性别（适合做分组柱状图）**

| 年龄 | 男性 | 女性 | 样本 | 时间 | 来源 |
|---|---|---|---|---|---|
| 15–34 | 25% | 18% | 每年约 1,000 名美国成人（电话），2023–2024 合并 | 2024 年实地调研 06-28 至 08-01 | [Gallup](https://news.gallup.com/poll/690788/younger-men-among-loneliest-west.aspx) |
| 35–54 | 15% | 20% | 同上 | 同上 | 同上 |
| 55+ | 16% | 17% | 同上 | 同上 | 同上 |
| 全国平均 | 18% | | | | |

**表 4　拥有 5 个以上密友的比例（按年龄）**

| 年龄 | <30 | 30–49 | 50–64 | 65+ | 样本 / 时间 | 来源 |
|---|---|---|---|---|---|---|
| 比例 | 32% | 34% | 40% | 49% | n=5,057，2023-07-17 至 07-23 | [Pew](https://www.pewresearch.org/short-reads/2023/10/12/what-does-friendship-look-like-in-america/) |

价格压力的世代梯度同样清楚，而且三个独立来源方向一致：Gen Z ≈ 千禧一代 > Gen X ≫ 婴儿潮。LendingTree 2025 年的数据显示，**53%** 的人因票价放弃过喜欢的艺人，**23%** 用 BNPL 支付演出相关费用，其中 Gen Z 为 37%，有幼儿的父母高达 44%（[LendingTree 2025](https://www.lendingtree.com/credit-cards/study/concert-spending-report/)）。预期要为看演出负债的比例，从"历史基线" 12% 升至 2022 年的 26%，再到 2025 年的 31%（另有 8% 表示"可能"）。各年问法不同，这组数只能当作方向性趋势，不能当作严格的时间序列。一个值得注意的矛盾：CNBC 报道称 2022 年 Gen Z 愿意负债的比例为 25%，这很可能是把"绝对值得"的比例误当成了"计划负债"的比例，应以 LendingTree 原页的 **41%** 为准（[LendingTree 2022](https://www.lendingtree.com/credit-cards/study/concert-plans-budgets/)）。需求被价格压抑，而不是缺乏兴趣。这正是"原价"承诺能释放的那部分需求。

**表 5　演出负债 / BNPL 的世代梯度（适合做分组柱状图）**

| 指标 | Gen Z | Millennials | Gen X | Boomers | 样本 / 时间 | 来源 |
|---|---|---|---|---|---|---|
| 用过 BNPL 支付演出费用 | 37% | 35% | 19% | 3% | n=2,050，2025-06-12 至 14 | [LendingTree 2025](https://www.lendingtree.com/credit-cards/study/concert-spending-report/) |
| 愿为娱乐负债 | 35% | 33% | 16% | 6% | n=1,006，2023-09-01 至 04 | [Credit Karma](https://creditkarma.com/about/commentary/gen-z-opens-their-wallets-as-the-cost-of-entertainment-rises) |
| 计划为演出负债 | 41% | 31% | — | — | n=2,072，2022-05-06 至 10 | [LendingTree 2022](https://www.lendingtree.com/credit-cards/study/concert-plans-budgets/) |
| 月度演出支出高于疫情前 | 42% | 34% | 19% | 11% | n=1,006，2023-09 | [Credit Karma](https://creditkarma.com/about/commentary/gen-z-opens-their-wallets-as-the-cost-of-entertainment-rises) |

**表 6　负债意愿时间序列（问法不一致，仅作趋势参考）**

| 时点 | 预期为演出负债的比例 | 来源 |
|---|---|---|
| 历史基线 | 12% | [LendingTree 2022](https://www.lendingtree.com/credit-cards/study/concert-plans-budgets/) |
| 2022 | 26% | 同上 |
| 2025 | 31%（另 8% "可能"） | [LendingTree 2025](https://www.lendingtree.com/credit-cards/study/concert-spending-report/) |

**表 7　价格与票务风险关键指标（LendingTree 2025，n=2,050，2025-06，适合做 KPI 卡片）**

| 指标 | 数值 |
|---|---|
| 因高价放弃喜欢的艺人 | 53% |
| 因经济原因重新考虑是否观演 | 57% |
| 曾通过转售方购票 | 30% |
| 遭遇过票务诈骗或假票 | 25%（其中 14% 不止一次） |
| 为抢预售专门办信用卡 | 27% |
| 人均年度演出支出 | $992 |
| 单张票实付最高金额均值 | $237 |
| 为最爱艺人愿付金额均值 | $287 |

来源：[LendingTree 2025](https://www.lendingtree.com/credit-cards/study/concert-spending-report/)。非概率配额样本，18–79 岁。

安全维度出现了一项本轮最重要的新证据。BMJ 旗下 *Injury Prevention* 于 2025 年 9 月发表了美国首个同行评审的现场音乐性骚扰患病率研究（n=1,091，2024 年调研）：**82% 的女性、39% 的男性**在现场演出中遭遇过不当性行为，**88%** 没有向工作人员报告。更反直觉的是，**与朋友或伴侣同行的女性遭遇骚扰更多**（[BMJ Group](https://bmjgroup.com/6-in-10-us-music-fans-say-they-have-been-sexually-harassed-assaulted-at-a-live-gig-survey-suggests/)；[PubMed](https://pubmed.ncbi.nlm.nih.gov/40983536/)）。这推翻了"有人陪就安全"的朴素假设。Plus One 的安全叙事不能建立在"结伴＝安全"之上，而要落在具体机制上：身份核验、女性专属小队、场外集合、行程分享。

**表 8　现场音乐性骚扰经历（适合做对比柱状图）**

| 群体 | 遭遇过不当性行为 | 备注 | 样本 / 时间 | 来源 |
|---|---|---|---|---|
| 全体 | 61% | 88% 未上报；最常见原因是"报了也没用"（25%） | n=1,091 名过去一年看过演出的美国成人，51% 为女性；GrooveSafe 2024 调查 | [BMJ Group](https://bmjgroup.com/6-in-10-us-music-fans-say-they-have-been-sexually-harassed-assaulted-at-a-live-gig-survey-suggests/) |
| 女性 | 82% | 20% 表示"经常"发生 | 同上 | 同上 |
| 男性 | 39% | | 同上 | 同上 |

Eventbrite 2026 年的社交研究给出了产品定位上的关键提示（n=4,051，18–35 岁，美英合并，2025 年 7 月调研）：**58%** 的人更喜欢"社交不是主要目的"的活动，**89%** 希望活动能把自己和社群连起来，**69%** 靠熟人或口碑发现活动（[Eventbrite](https://www.eventbrite.com/blog/press/newsroom/eventbrites-inaugural-social-study-report-reveals-the-reset-to-real/)）。换句话说，年轻人要的是"围绕这场演出的陪伴"，而不是"来交朋友"的社交局。这支持 Plus One 以具体场次为锚点，而不是做成泛社交 app。

**前期桌面研究的背景数据（本轮未复核原始链接，仅供参考）：** Bandsintown 2022 年调查中 80% 的人愿意独自去看演出，40% 过去 12 个月确实独自去过。viagogo 英国 2024 年调查中，女性的安全顾虑为 36%，男性为 11%。Ticketmaster 2025 年数据显示音乐节独自参加比例从 8% 升至 29%。SeatGeek 佛罗里达单张票占比在 2022、2023、2025 年分别为 22%、24%、26%。Deloitte 2024 年调查中约 60% 的人因费用放弃过活动，54% 的 Gen Z 和千禧一代认为粉丝身份帮助他们交朋友（其他人群为 24%）。Pollstar Top 100 平均票价：2019 年 $96.17，2022 年 $106.07，2023 年 $130.81，2024 年 $135.92，2025 年 $132.62。以上数据与本轮发现方向一致：独自观演在增长，单张购票在增长，价格在 2024 年见顶后高位企稳。

---

## 用户原声：被骗与信任占主导，社交侧的痛点和收获几乎对半

研究团队对北美 50 条真实用户表达做了主题编码。来源包括 Substack 帖子和评论、Meetup 群组、Ticketmaster App Store 评论、StubHub 和 Tixel 的 Trustpilot 评论，以及 CBC、CBS、CNN、Globe and Mail 等媒体报道中实名引用的乐迷。另有 15 条非北美条目单独统计。**Reddit、TikTok 和 Quora 在本研究环境中均被屏蔽**，所以样本缺少年轻男性和 EDM/音乐节社群的声音。新闻来源天然偏向诈骗受害者，Substack 偏向已经克服恐惧的、以女性为主的独自观演者。下列频次描述的是这个样本，不能外推到总体。

**表 9　用户原声主题频次（北美 n=50，一条可带多个主题；适合做横向条形图）**

| 代码 | 主题 | 条数 | 占比 | 侧 |
|---|---|---|---|---|
| B4 | 被骗 / 票没到 / 假票 / 被盗 | 10 | 20% | 票务 |
| B3 | 信任信号与怕被骗 | 9 | 18% | 票务 |
| A6 | 结识他人 / 与人群产生连接 | 8 | 16% | 社交（收获） |
| A5 | 享受独自去的自由 | 6 | 12% | 社交（收获） |
| A1 | 朋友放鸽子 / 协调不了 / 没人一起去 | 6 | 12% | 社交（痛点） |
| A4 | 独自去尴尬、焦虑 | 6 | 12% | 社交（痛点） |
| A8 | 独自观演的技巧与习惯 | 6 | 12% | 社交 |
| B1 | 手上多出一张票（朋友退出、不付钱、买错日期） | 6 | 12% | 票务 |
| B2 | 原价与加价（寻求或维护原价） | 6 | 12% | 票务 |
| B7 | 平台客服失灵 | 6 | 12% | 票务 |
| B5 | 转让、入场、打款受限 | 5 | 10% | 票务 |
| A7 | 独自去更便宜 / 单张座位更好 | 4 | 8% | 社交 |
| B6 | 对手续费愤怒 | 4 | 8% | 票务 |
| B9 | App 或技术故障 | 4 | 8% | 票务 |
| B8 | 对认证平台的正面信任 | 3 | 6% | 票务 |
| A2 | 口味不合 / 迁就他人 | 1 | 2% | 社交 |
| A3 | 安全顾虑（女性 / 散场） | 1 | 2% | 社交 |
| C1 | 陌生人的余票变成同行伙伴 | 1 | 2% | 交叉 |

来源：研究团队对 50 条北美用户表达的内容编码，全部于 2026-09-28 抓取。来源包括 [TueNight](https://tuenight.substack.com/p/the-unexpected-joy-of-going-to-a/comments)、[Ticketmaster App Store 评论](https://apps.apple.com/us/app/ticketmaster-buy-sell-tickets/id500003565?see-all=reviews)、[Trustpilot StubHub](https://www.trustpilot.com/review/www.stubhub.com)、[Trustpilot Tixel](https://www.trustpilot.com/review/tixel.com)、[CNN](https://www.cnn.com/2023/05/13/tech/taylor-swift-ticket-drops-ticketmaster/index.html)、[CBC](https://www.cbc.ca/lite/story/1.7386376) 等，代表性引述见下文。

**表 10　细分人群的主题分布（适合做堆叠条形图）**

| 细分人群 | n | 头部主题（条数 / n） |
|---|---|---|
| 独自观演 / 找伴者 | 15 | 结识他人 7/15，自由 6/15，尴尬 6/15，技巧 6/15，没人同去 4/15，更便宜或座位更好 4/15 |
| 买家 | 25 | 被骗 10/25，信任 8/25，原价 5/25，客服 4/25，转让受限 4/25，手续费 4/25 |
| 余票持有者 / 卖家 | 9 | 多出一张票 6/9，平台摩擦（客服、转让、技术）3/9，正面信任 1/9 |

从这些数字可以读出三个与直觉不同的结论。

**第一，票务侧的痛点主要是"真假"，而不是"贵"。** 被骗和信任两项合计出现 19 次，手续费愤怒只有 4 次。诈骗受害者信任的线索，恰恰是一个社交型产品会天然依赖的那些：朋友的账号、朋友的朋友、同一个 Facebook 妈妈群、相识 23 年的发型师、在公共场所当面交易。Cincinnati 的 Jeremy Robinson 被一个被盗的朋友 Facebook 账号以"原价"骗走 800 美元，当时这张 Eras 门票的转售价已经超过 2,000 美元（[WCPO, 2024-09](https://www.wcpo.com/money/consumer/dont-waste-your-money/hacked-facebook-friends-offering-bogus-taylor-swift-tickets)）。多伦多一位母亲因为信任相识 23 年的发型师和一个本地妈妈群，损失超过 2,000 加元（[Globe and Mail](https://www.theglobeandmail.com/investing/personal-finance/article-taylor-swift-concert-ticket-scam-resale-tickets/)）。安大略一名诈骗者引来约 40 起投诉，涉案金额超过 7 万加元（[CBC, 2024-11](https://www.cbc.ca/lite/story/1.7386376)）。**"原价"本身就是诈骗诱饵，"社交关系"本身就是被伪造的信任信号。** Plus One 恰好同时依赖这两样东西，所以必须用平台托管和身份核验来兜底，不能让它们单独起作用。

**第二，社交侧的痛点是"空档期"，而不是"孤独"。** 独自观演者描述的不适集中在入场排队、GA 区站着等、换场间隙这些没人说话的时间。DC 的 Adri Vazquez 在搬家后没了演出搭子，她最怕的是"独自站在 general admission 区"（[Setting the Tone, 2024-03](https://settingthetone.substack.com/p/going-to-concerts-alone)）。收获方的语言则是自由和与人群的即时连接："一旦他们上台，就没有人是孤单的"（[TueNight 评论](https://tuenight.substack.com/p/the-unexpected-joy-of-going-to-a/comments)）。还有明确的反对声音："我不是去社交的，我是去听音乐的"（[Illinois Drifter](https://illinoisdrifter.substack.com/p/going-alone-to-concerts-plus-some)）。所以"Never go alone"这句口号有冒犯核心独自观演者的风险。更贴合原声的表述是"开场前有人聊，散场后各走各路"。

**第三，余票的主要来源是朋友放鸽子，持有者要的是"快速、公平地回本"，不是赚差价。** 一位 19 岁女生为 4 人买了 Ariana Grande 门票（每张 103 美元），其中一个朋友连续几周找借口不付钱（[People via AOL](https://www.aol.com/articles/woman-threatens-sell-friend-concert-190000686.html)）。r/AITA 上一名男子的朋友在演出前一天退出，他卖掉那张票并留下了钱，评论区普遍支持他（[TwistedSifter, 2026-03](https://twistedsifter.com/2026/03/their-friend-backed-out-from-a-concert-even-after-the-ticket-has-been-paid-so-this-man-decided-to-sell-it-and-keep-the-money-for-himself/)）。卖家遇到的阻力来自朋友间谈钱的尴尬、平台打款和转让的摩擦，以及客服的死胡同。StubHub 的卖出流程被评价为"非常复杂"（[Trustpilot StubHub](https://www.trustpilot.com/review/www.stubhub.com)）。另外，@ErasTourResell 的志愿者以原价转出了约 2,700–3,000 张票，卖家会**按故事挑选买家**，比如优先给急救人员，而不是价高者得（[CNN, 2023-05](https://www.cnn.com/2023/05/13/tech/taylor-swift-ticket-drops-ticketmaster/index.html)）。这说明部分卖家在乎"谁拿到这个座位"。这是"卖给愿意同去的人"最接近的行为证据。

"换票＋找伴"组合需求的直接证据只有一条（C1，占 2%）：Alabama 的 Katy Blackman 在 Eras 开场前几秒拿到陌生人的余票，"我和我的新朋友唱完了每一首歌"（[CNN](https://www.cnn.com/2023/05/13/tech/taylor-swift-ticket-drops-ticketmaster/index.html)）。Baltimore 的 Meetup 群"Concert Friends"就是为"没人一起去"的人建的，有 747 名成员（[Meetup](https://www.meetup.com/baltimore-concert-friends-and-live-shows/)）。准确的表述是：**行为存在，但没有人主动说出这个产品。** 需求是潜在的，作品集叙事应该写成"有行为证据、缺陈述需求证据"。

---

## 原价换票：官方零费、第三方收 10–15%，法规方向有利但技术上受制于票务商

原价转售在北美主要存在于一级票务商内部，这是本轮最关键的结构性发现。Ticketmaster Face Value Exchange 和 DICE wait list 都能做到卖家零费、按原价成交，但都要艺人或主办方主动开启（[Ticketmaster Help](https://help.ticketmaster.com/hc/en-us/articles/9781464415249-How-does-Ticketmaster-s-Face-Value-Exchange-work)；[DICE Help](https://dicefm.zendesk.com/hc/en-gb/articles/19958073128849-The-wait-list-explained)）。独立的原价平台必须向买家收费，才能养活自己。Tixel 美国站向买家收 6.9% 服务费，外加 4.5% 刷卡费，卖家另付 5.9%（[Tixel Help](https://tixelhelp.zendesk.com/hc/en-au/articles/18836653161113-Tixel-Fees-USA)，该页最后更新于 2023 年 5 月，可能已过时）。CashorTrade 对非会员买家收 10% 平台费，外加 3–5% 刷卡费（[CashorTrade Help](https://help.cashortrade.org/hc/en-us/articles/12918261373069-Understanding-Fees-on-CashorTrade)）。"原价"的承诺在买家那一端被打了约一成多的折扣。

**表 11　以 $100 面值票为例的平台费用对比（适合做堆叠柱状图）**

| 平台 | 价格上限 | 买家费用 | 买家实付≈［推算］ | 卖家费用 | 卖家到手≈［推算］ | 打款时间 | 来源 |
|---|---|---|---|---|---|---|---|
| Ticketmaster Face Value Exchange | 锁定为原付总价 | 帮助页未说明（展示价已含原始费用和税） | $100 | 免费 | $100 | 通常演出后 7 个工作日内 | [TM Help](https://help.ticketmaster.com/hc/en-us/articles/9781464415249-How-does-Ticketmaster-s-Face-Value-Exchange-work) |
| DICE wait list | 原价 | 未查到 | $100 | 全额退款给卖家 | $100 | 售出即退款 | [DICE Help](https://dicefm.zendesk.com/hc/en-gb/articles/19958073128849-The-wait-list-explained) |
| Tixel（美国） | 原价 | 6.9%（自动购买为 7.9%，最低 $4.50）＋ 4.5% 刷卡费＋州税 | ≈$111.4（未含税） | 5.9%（最低 $4.50） | ≈$94.1 | 未查到 | [Tixel Help](https://tixelhelp.zendesk.com/hc/en-au/articles/18836653161113-Tixel-Fees-USA)（2023-05） |
| CashorTrade | 严格原价 | 10%（非 Gold 会员）＋ 3–5% 刷卡费 | ≈$113–115 | 免费；交付失败罚款最高 150% | $100 | 经 PayPal，时间未查到 | [CashorTrade Help](https://help.cashortrade.org/hc/en-us/articles/12918261373069-Understanding-Fees-on-CashorTrade) |
| Twickets（美国） | 原价（+费用） | 未查到 | — | 未查到 | — | 未查到 | [Twickets US](https://www.twickets.live/en/us) |
| StubHub | 无上限 | 高且不固定；FTC 举例总价比标价高 25% | ≥$125（仅手续费，不含加价） | ≈15%＋处理费（第三方数据） | ≈$85 | 演出后 | [FTC 起诉书](https://www.ftc.gov/system/files/ftc_gov/pdf/StubHub-Complaint.pdf)；[SellTicketsFast](https://sellticketsfast.com/ticket-selling-fees-compared/) |
| SeatGeek | 无上限 | 约 10–30%（第三方估算，非官方） | ≈$110–130 | 10%（第三方） | ≈$90 | 约演出后 48 小时 | [SellTicketsFast](https://sellticketsfast.com/ticket-selling-fees-compared/) |
| Vivid Seats | 无上限 | 约 20–40%（第三方估算，非官方） | ≈$120–140 | 10%（第三方） | ≈$90 | 演出后 | 同上 |
| 参考：Posh（小型活动票务） | 不适用 | 10%＋$0.99 | ≈$111 | 主办方零费 | — | — | [DMN, 2024-07](https://www.digitalmusicnews.com/2024/07/24/posh-raises-22-million-with-small-events-platform-model/) |

说明：推算列假设百分比费用以面值为基数，并忽略最低收费和税费。开放市场的实际成交价通常还包含卖家加价，前期研究引用的 NITO 平均加价为 91%。

技术约束比费用更硬。SafeTix 一类的动态条码让截图和 PDF 失效。唯一有效的交接方式是票务商自己的"Transfer"功能（输入收件人邮箱或手机号），或者官方交换平台。转让是否开放、何时开放，都由票务商和活动方控制：DICE 的好友转让只在"该场演出开放此选项时"可用（[DICE Help](https://dicefm.zendesk.com/hc/en-gb/articles/19958073128849-The-wait-list-explained)）；Ticketmaster 在 2024 年因票被盗，推迟了 Eras Tour 印第安纳波利斯和多伦多场次的转让时间（[CBC](https://www.cbc.ca/news/business/ticketmaster-taylor-swift-1.7346088)，具体时间窗口未核实）。更值得警惕的是 **MAIN Event Ticketing Act**：该法案 2026 年 9 月 16 日以 36–0 通过众议院能源与商业委员会，会把规避票务商"访问控制"的行为定为违反 BOTS Act（[TicketNews, 2026-09](https://www.ticketnews.com/2026/09/main-event-ticketing-act-house-committee-bots-act/)）。因此 Plus One 在架构上只能做**撮合和托管层**：提示卖家何时在 TM、AXS 或 DICE 的 app 里点"Transfer"，买家确认收到后再放款；永远不索取账号密码，也不抓取票务商数据。遇到不能转让或只能官方渠道转售的场次，直接深链到 Face Value Exchange 或 DICE wait list。

法规走向对"只做原价"的产品有利。联邦层面管的是透明度，不管价格上限：FTC 的《不公平或欺骗性费用规则》2025 年 5 月 12 日生效，要求第一屏就显示含全部强制费用的总价（[FTC](https://www.ftc.gov/news-events/news/press-releases/2025/05/ftc-rule-unfair-or-deceptive-fees-take-effect-may-12-2025)），首起重大执法是 2026 年 4 月 9 日起诉 StubHub（[FTC 起诉书](https://www.ftc.gov/system/files/ftc_gov/pdf/StubHub-Complaint.pdf)）。价格上限在州和特区层面推进：缅因、佛蒙特、DC 已经立法，马萨诸塞还在协商，另有约 13 项限价提案失败（[TicketNews, 2026-08](https://www.ticketnews.com/2026/08/resale-industry-confronts-coordinated-statehouse-campaign-to-restrict-ticket-competition/)）。原价换票天然满足所有已知的上限法规；需要主动遵守的只有全价展示这一条，**包括 Plus One 自己收的任何费用**。

**表 12　北美票务监管时间线（适合做时间轴图）**

| 日期 | 司法辖区 | 措施 | 对 Plus One 的含义 | 来源 |
|---|---|---|---|---|
| 长期有效（需定期续期） | 纽约 ACA §25.30 | 纸质或无纸化票必须提供"任意价格、任意时间、免费"可转让的选项 | 纽约场次可转让性最有保障；现行续期状态未核实 | [FindLaw](https://codes.findlaw.com/ny/arts-and-cultural-affairs-law/aca-sect-25-30/)；[NY S276](https://www.nysenate.gov/legislation/bills/2025/S276) |
| 2025-03-31 | 联邦行政令 | 要求 FTC 严格执行 BOTS Act，不设价格上限 | 反机器人执法力度加大 | [Wiley](https://www.wiley.law/alert-Executive-Order-on-Ticket-Resale-Market-Calls-for-Greater-FTC-Enforcement) |
| 2025-04 | 联邦 TICKET Act | 众议院 409–15 通过，参议院尚未通过；内容为全价展示、退款、禁止投机挂单 | 全价展示成为常态 | [Congress.gov](https://www.congress.gov/bill/119th-congress/senate-bill/281) |
| 2025-05-12 | 联邦 FTC 费用规则 | 首屏显示全部费用 | Plus One 的费用必须首屏可见 | [FTC](https://www.ftc.gov/news-events/news/press-releases/2025/05/ftc-rule-unfair-or-deceptive-fees-take-effect-may-12-2025) |
| 2025-06 | 缅因 LD 913 | 转售平台收费上限为原票总价的 10%；禁止投机票；个人卖家豁免 | 原价模式合规 | [Maine AG](https://www.maine.gov/ag/consumer-protection/consumer-issues-scam/consumer-alert-ticket-resales-thu-01292026-0751) |
| 2026-04-09 | 联邦 FTC 起诉 StubHub | 指控隐藏费用 | 同上 | [FTC](https://www.ftc.gov/system/files/ftc_gov/pdf/StubHub-Complaint.pdf) |
| 2026-07-01 | 佛蒙特 Act 109 | 3,000 座及以下场馆，转售价上限为原价的 110% | 原价模式合规 | [TicketNews](https://www.ticketnews.com/2026/08/resale-industry-confronts-coordinated-statehouse-campaign-to-restrict-ticket-competition/) |
| 2026-09-16 | 联邦 MAIN Event Act | 众议院委员会 36–0 通过；规避访问控制将违反 BOTS Act | 禁止抓取和共享账号 | [TicketNews](https://www.ticketnews.com/2026/09/main-event-ticketing-act-house-committee-bots-act/) |
| 2026-10-01 | 北卡罗来纳 | 转售平台须链接原始票务商，全价展示 | 深链官方渠道是加分项 | [TicketNews](https://www.ticketnews.com/2026/08/resale-industry-confronts-coordinated-statehouse-campaign-to-restrict-ticket-competition/) |
| 2027-01-01 | 华盛顿特区 RESALE Act | 转售价上限为面值的 120%（含最多 10% 费用）；年转售 50 张以上须注册并缴 2.5 万美元保证金；仅适用于演艺活动 | 原价模式合规 | [DC Council](https://dccouncil.gov/council-gives-final-approval-to-resale-act-regulating-ticket-sales-and-capping-ticket-resale-prices/) |

**前期研究背景（未复核链接）：** VPA 2026 年估计转售每年推高票价 110 亿美元，其中经纪商加价 45 亿、手续费 68 亿，NITO 统计的平均加价为 91%。GAO 2018 年统计的手续费占比为一级市场 27%、二级市场 31%。FTC 2025 年 9 月起诉 5 家经纪商，涉及 6,345 个账号、246,407 张票，隐藏费用最高达 44%，2019–2024 年累计手续费 164 亿美元。Lloyds 统计英国 2023 年演出诈骗增长 529%，平均损失 110 英镑。

---

## 失败案例与小组模式的启示：原价生意利润薄，信任要靠真实活跃

Lyte 是最接近 Plus One 换票侧的前车之鉴。它 2014 年成立，四轮融资约 **5300 万美元**，最初是嵌在主办方系统里的官方原价交换平台，后来逐步偏离：开始帮主办方以加价方式"倒卖高端票和 VIP 票"并分成，收购了财务困难的 Festicket，又进入一级票务，把合作伙伴变成了竞争对手。2024 年 9 月中旬，Lyte 在还欠主办方钱的情况下突然停运，单一律师汇总的索赔就超过 100 万美元（[Billboard](https://www.billboard.com/pro/ticketing-company-lyte-shuts-down/)；[DMN](https://www.digitalmusicnews.com/2024/09/23/lyte-meltdown-update/)）。Hypebot 总结的失败原因是：获客成本上升、主办方用技术限制库存、手续费受到审视、收购拖累，以及身份从伙伴变成了对手（[Hypebot, 2024-10](https://www.hypebot.com/hypebot/2024/10/the-lyte-bankruptcy-and-what-it-reveals-about-the-ticketing-industry.html)）。放到 Plus One 上，这对应五条教训：原价余票只在有人去不了时才出现，所以单场匹配率低；依赖集成的产品随时可能被票务商关掉或被其自建功能替代（TM FVE 就是例子）；抽成被压在 10% 左右，付费获客算不过账；资金必须托管、不能混用；一旦靠加价赚钱，原价品牌就毁了。Twickets 2017 年宣布进入美国，到 2026 年美国站的挂单仍然稀少（[Twickets US](https://www.twickets.live/en/us)），也从侧面说明北美原价市场的流动性很难做起来。

IRL 是社交侧的警示。它融资超过 2 亿美元，2021 年估值 11.7 亿美元，自称有 2,000 万月活，2023 年 6 月董事会查明 **95% 的用户是机器人或自动账号**，随即关停（[TechCrunch](https://techcrunch.com/2023/06/26/irl-shut-down-fake-users/)）。对活动型社交产品来说，"每场真实、已核验的活跃人数"比注册数重要得多。

小组模式的证据是本轮竞品研究中最强的。公开数据里牵引力最好的几家，都用约 6 人的精选小组，而不是 1:1 滑卡：

**表 13　陌生人社交 / 活动型产品牵引力对比（适合做对比表或气泡图）**

| 产品 | 模式 | 关键指标 | 时间 | 变现 | 来源 |
|---|---|---|---|---|---|
| Timeleft | 6 人陌生人晚餐 | 每月 15 万参与者；€18M ARR；约 200 座活跃城市（2024 年峰值 320+）；68% 为女性 | 2025-08 | 仅订阅：约 $16/次或 $26/月 | [Tim Frin](https://timfrin.substack.com/p/inside-timelefts-journey-to-connecting)；[Alta](https://www.altaonline.com/dispatches/a63924701/strangers-in-the-night/) |
| Pie | AI 匹配 6 人小组＋活动前群聊 | 13 万+ MAU；A 轮 1,150 万美元；仅 SF 和 Chicago | 2025-03 | 向主办方付费办活动 | [TechCrunch](https://techcrunch.com/2025/03/04/andy-dunns-new-app-pie-uses-ai-to-help-you-make-friends) |
| 222 | 性格测试匹配小组活动，无资料页、私信或滑卡 | A 轮 1,010 万美元；16 名员工 | 2025-12 | 未查到 | [SV Post](https://svpost.com/articles/222-10m-series-a/) |
| Bumble BFF（整合 Geneva） | 从 1:1 转向群组和社区 | Geneva 截至 2025-06-30 无收入 | 2025-09 | 未查到 | [TechCrunch](https://techcrunch.com/2025/09/18/bumble-bffs-revamped-app-is-here-focusing-on-friend-groups-and-community-building) |
| Radiate | 按演出滑卡＋群聊＋PayPal 保障的票务市场 | App Store 4.9 分，约 3.1 万条评分；最近一次更新 2024-08 | 2026-09 读取 | 订阅 $9.99/月至 $99.99/年，外加代币 | [App Store](https://apps.apple.com/us/app/radiate/id939284774) |
| EventBuddie | 1:1 找同场乐迷 | 评分数不足以显示分数 | 2026-09 | 免费含广告 | [App Store](https://apps.apple.com/us/app/eventbuddie/id6748877517) |
| Posh | 小型活动票务＋发现 | 注册 200 万；累计 GMV 9,500 万美元；站内市场成交占比 6%→12% | 2024-07 | 买家付 10%＋$0.99 | [DMN](https://www.digitalmusicnews.com/2024/07/24/posh-raises-22-million-with-small-events-platform-model/) |
| IRL（已关停） | 活动群聊 | 自称 2,000 万 MAU，95% 为机器人 | 2023-06 | — | [TechCrunch](https://techcrunch.com/2023/06/26/irl-shut-down-fake-users/) |

**表 14　Timeleft 收入增长时间序列（适合做对数折线图）**

| 时点 | 收入 | 来源 |
|---|---|---|
| 2023-05（上线第一周） | €125 | [Tim Frin](https://timfrin.substack.com/p/inside-timelefts-journey-to-connecting) |
| 2023-12 | €20K MRR | 同上 |
| 上线约 16 个月后 | €1M/月 | 同上 |
| 2025-08 | €18M ARR | 同上 |

Radiate 是最直接的竞品，它已经做了"找同场的人＋有保障的票务市场"，本质上就是 Plus One 概念的雏形。它暴露的问题正好指明了 Plus One 可以做得更好的地方。一条 2025 年 1 月的 App Store 评论称其首页"90% 时间基本是色情内容"（[App Store](https://apps.apple.com/us/app/radiate/id939284774)）；竞品 FestivalMates 的创始人（立场有偏）批评它的滑卡匹配"随机"、有垃圾和虚假账号、组队工具弱（[FestivalMates](https://www.festivalmates.com/blog/radiate-alternatives-2026)）。1:1 滑卡式的演出 app 会向约会和约炮漂移，Tinder Festival Mode 本身就是约会产品。这对想找朋友的女性是信任杀手。Pew 的数据显示，**57% 的女性**（男性为 41%）认为约会 app 不是安全的认识人的方式；50 岁以下用过约会 app 的女性中，**56%** 收到过不想要的露骨内容，66% 至少经历过一种骚扰（[Pew, 2023-02](https://www.pewresearch.org/internet/2023/02/02/from-looking-for-love-to-swiping-the-field-online-dating-in-the-u-s/)）。Timeleft 用户中 68% 是女性，参与者说小组"比约会 app 更安全"（[Alta](https://www.altaonline.com/dispatches/a63924701/strangers-in-the-night/)）。这是目前最好的证据，表明小组形式能吸引女性。

冷启动方面，成功者都靠在时间和地点上集中需求来制造密度。Timeleft 要一个城市先凑够 151 个报名才开城，所有晚餐都安排在周三，从第一天就收费以过滤掉没有真实意图的人（[Startup Spells](https://startupspells.com/p/how-timeleft-solved-the-chicken-and-egg-problem)）。Tinder Festival Mode 只覆盖 20 多个精选音乐节，每个提前一个月开放（[Tinder](https://www.tinderpressroom.com/2022-04-14-Tinder-Kicks-Off-A-Return-to-IRL-with-Festival-Mode-TM)）。Radiate 的用户集中在 EDC、Ultra 等大型电子音乐节。对 Plus One 来说，演出本身就是天然的时间和地点锚点，比晚餐局更容易集中需求；但每个场次都是一次性的，不像 Timeleft 那样每周重复。这会让密度问题比 Timeleft 更难。

---

## 设计含义：以换票获客、以核验建立信任、以小队承接社交

把上述证据合在一起，Plus One 的产品结构应该从"双功能平铺"调整为"工具带社交"。原价换票是有明确痛点的刚需工具，余票持有者要的是快速公平地回本，买家要的是确认票是真的，所以它适合当入口。找伴是可选的增值层，默认措辞应当是"开场前一起"，而不是"整晚绑定"。

**表 15　证据到设计的映射**

| 证据 | 强度 | 设计含义 |
|---|---|---|
| 用户原声中被骗 20%、信任 18%；诈骗利用的正是社交关系和"原价"两个信号；LendingTree 调查中 25% 遇到过票务诈骗 | 强（多来源） | 买家确认收到票后才放款的托管；强制身份核验（可参考 Bumble 2025 年在美加墨推出的证件核验徽章，[Fast Company](https://www.fastcompany.com/91299913/bumble-adds-an-id-verification-feature-to-win-over-cautious-daters)）；绝不接受站外付款 |
| SafeTix 转让由票务商控制；MAIN Event Act 可能出台 | 强 | 只做撮合层，引导卖家使用官方 Transfer；不能转让的场次深链 TM FVE 或 DICE wait list；不碰账号凭证 |
| 第三方原价平台买家多付约 10–15%；FTC 要求首屏全价 | 强 | 收小额固定"买家保障费"（参考 Posh 的 $0.99），不按百分比抽成；首屏显示含全部费用的总价 |
| 余票主要来自朋友退出；部分卖家按故事挑买家 | 中 | 卖家可以选择"优先卖给愿意同行的人"；群内 AA 付款，未付款的座位自动释放给别人 |
| 痛点集中在空档期；有明确的"我是来听音乐的"反对声音；Eventbrite 调查中 58% 偏好不以社交为主的活动 | 中 | 默认"开场前集合点"和"开演前同坐"，散场各走各路；找伴始终是可选项 |
| Timeleft、Pie、222 的小组模式；Bumble 转向群组；Radiate 滑卡向色情漂移 | 中强 | 按场次组 4–6 人小队；不做滑卡和公开约会式资料页；换票之外不开放 1:1 私信 |
| 女性遭遇现场骚扰 82%；与朋友同行的女性反而遭遇更多；Pew 调查中 57% 的女性认为约会 app 不安全 | 强（患病率）/ 弱（对陌生人同行的顾虑） | 女性专属小队选项；场外公共地点集合；行程分享给朋友；举报和拉黑；品牌明确"不是约会 app" |
| 15–34 岁男性孤独比例 25% 为最高 | 中 | 不要把产品做成只面向女性的安全产品；年轻男性的找伴需求同样需要一个不带约会暗示的入口 |
| IRL 95% 机器人；Twickets 美国站流动性低 | 强 | 对外展示"每场已核验的真实人数"，不展示注册数；先聚焦一个城市、一个音乐圈层冷启动（例如单个巡演或单个音乐节） |

Plus One 的变现空间很窄，这一点应当在作品集中坦白说明。原价承诺排除了按百分比抽成；Meetup 2019 年试行向参与者收每次报名 2 美元，引发强烈反弹（[Wikipedia](https://en.wikipedia.org/wiki/Meetup)）；Geneva 做到被收购都没有收入。可行的方向有三个：小队或核验层的订阅（Timeleft 已证明与线下活动绑定的订阅能跑通），与艺人或场馆合作（作为官方原价交换的社交层），以及固定的买家保障费。

---

## 仍未验证的假设：组合需求、供给密度和安全阈值都缺直接证据

本轮研究把宏观需求（孤独、价格、诈骗）量化得比较充分，但决定 Plus One 能不能成立的几个关键假设，仍然缺少直接证据。部分原因是方法限制：Reddit、TikTok 和 Quora 被屏蔽，无法抓取；Sensor Tower 等 app 数据平台无法访问；StubHub、Vivid Seats 的上市文件没有取到。下表按对产品决策的影响排序。

**表 16　未验证假设清单**

| # | 假设 | 当前证据 | 缺口 | 建议验证方式 |
|---|---|---|---|---|
| 1 | 卖家愿意把余票卖给"会同行的人" | 仅 @ErasTourResell 按故事挑买家，1 个 C1 案例 | 没有陈述性需求，没有规模数据 | 手工梳理 Reddit 上 r/concerts、r/TaylorSwift、r/aves 的"extra ticket, want a buddy"类帖子；对 8–10 名余票持有者做访谈 |
| 2 | 单场原价余票足以支撑换票 | Twickets 美国站流动性低；Lyte 倒闭 | 没有"每场余票数""平均每单张数""粉丝按原价出售比例"等数据 | 从 StubHub S-1 和 Vivid Seats 10-K 推算平均每单张数；选一场演出做 Discord 或 Typeform 快速验证（Timeleft 式无 app 验证） |
| 3 | 独自观演者想要"陪伴"而不是"独处" | 原声中收获（结识 16%、自由 12%）和痛点（尴尬 12%）并存 | 没有美国独自观演的性别和年龄拆分；Bandsintown 2022 数据未复核 | 做 n≥300 的问卷，问"独自去时最想被解决的时刻"（入场、GA 等待、换场、散场） |
| 4 | 女性会接受与陌生人组成的小队 | Timeleft 68% 女性；BMJ 现场骚扰患病率数据 | 没有"与 app 上认识的朋友见面"的安全调查；viagogo 数据是英国的 | 用可用性测试比较女性对"女性专属小队""场外集合""证件核验"几种设计的接受度 |
| 5 | 小组比 1:1 留存更好 | 牵引力数据间接支持（Timeleft 每用户每月 2.2 次） | 没有公开的留存对比 | 在原型测试中对比 1:1 与 4–6 人小队的约见完成率 |
| 6 | 票务商会允许或至少容忍这种撮合 | TM FVE 和 DICE 都要主办方开启；MAIN Event Act 在推进 | 不知道有多少巡演限制或推迟转让（例如"开演前 72 小时"） | 抽样 20 场北美巡演，记录转让政策 |
| 7 | 年轻男性是被低估的用户群 | Gallup 调查中 15–34 岁男性每日孤独 25% | 用户原声里男性只有 2 条 | 分性别招募访谈对象 |
| 8 | 加拿大市场适用同样逻辑 | 原声中有安大略和多伦多的诈骗案例 | 没有核查安大略 Ticket Sales Act 和魁北克的转售规定 | 桌面补查省级法规 |

数据层面还有几处需要在引用时说明口径：Cigna 的样本量在报告 PDF（n>5,000）和二手摘要（7,500+）中不一致；LendingTree 2022 年"男性年均 3 场、女性 1 场"的差距异常大，谨慎使用；Tixel 的费用页最后更新于 2023 年；SeatGeek 和 Vivid Seats 的买家费用区间是第三方估算；Live Nation 2019 年和 2023 年的观众数分别是推算值和未核实值。

---

## 结论

这一轮研究改变了对 Plus One 的理解：它应该是一个信任产品，而不是一个社交产品。用户原声里，票务侧真正的恐惧是"钱付了、票是假的"，而诈骗者利用的正是熟人关系和"原价"这两个 Plus One 本来打算依赖的信号。社交侧的真实痛点是开场前那一两个小时，而不是整场演出的孤独。所以 Plus One 的差异化不在"把换票和找伴放进同一个 app"。Radiate 已经这样做了，但它的口碑被色情内容和虚假账号拖累。真正的差异化在于**把身份核验和托管做成两个功能共享的底层**：同一个经过核验的身份，既让陌生卖家可信，也让陌生同伴可信。这是单做票务或单做社交的竞品都无法复用的结构性优势。

对作品集而言，最有说服力的叙事是把约束变成设计：原价换票天然合规，但把票务商视为不可绕开的上游，只做撮合；小队模式由 Timeleft 等产品验证，能同时缓解冷启动密度和女性的安全顾虑；变现只收固定保障费，是原价承诺下的诚实选择。下一步最值得投入的验证，是一次针对单场演出的无 app 快速实验，用来同时测量余票供给和"卖给同行者"的意愿。这两个数字决定概念能否成立，而目前没有任何公开数据能回答它们。
