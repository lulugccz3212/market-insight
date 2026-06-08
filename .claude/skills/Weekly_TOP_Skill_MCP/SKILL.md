---
name: Weekly_TOP_Skill_MCP
description: 每周搜索和分析热门的Claude Code Skills与MCP服务器，生成TOP 5排名报告。
---

# 每周TOP Skill与MCP趋势分析，并输出排名报告

对当周热门的Claude Code Skills和MCP（Model Context Protocol）服务器进行搜索、识别、评分与排名分析，输出包含TOP 5排名、类别分布、周环比变化和趋势总结的HTML仪表盘报告。

## 1. 数据获取

### 1.1 GitHub Trending搜索（主要来源）

使用 `mcp__brave-search__brave_web_search` 工具搜索GitHub上的热门Skills和MCP项目（参数格式：`{"query": "关键词", "count": 10}`）：

**MCP服务器搜索：**
- `site:github.com "mcp-server" stars`
- `site:github.com "@modelcontextprotocol" server`
- `site:github.com "mcp" topic`
- `site:github.com mcp-server typescript OR python`

**Claude Code Skills搜索：**
- `site:github.com "claude-code" skill`
- `site:github.com "claude-code-skill"`
- `site:github.com "claude" skill mcp`

**综合趋势搜索：**
- `github trending repositories mcp this week`
- `github trending repositories claude code skill`

使用 `mcp__fetch__fetch` 工具获取GitHub Trending页面（参数格式：`{"url": "https://...", "max_length": 5000}`）：
- `https://github.com/trending?since=weekly`
- `https://github.com/topics/mcp`

> 从GitHub Trending页面和topic页面手动筛选与MCP、Claude Code Skill相关的项目。

### 1.2 npm Registry搜索

使用 `mcp__brave-search__brave_web_search` 工具搜索：
- `site:npmjs.com "@modelcontextprotocol" server`
- `site:npmjs.com "mcp-server" popular`
- `npm mcp server weekly downloads trend`
- `site:npmjs.com package "claude-code"`

使用 `mcp__fetch__fetch` 工具获取npm搜索页面：
- `https://www.npmjs.com/search?q=mcp-server`
- `https://www.npmjs.com/search?q=%40modelcontextprotocol`

> 从npm搜索结果中提取包名、描述、每周下载量、最新版本和发布时间。

### 1.3 官方来源

使用 `mcp__fetch__fetch` 工具获取Anthropic官方资源：
- `https://docs.anthropic.com/en/docs/agents-and-tools/mcp` — 官方MCP文档
- `https://www.anthropic.com/blog` — Anthropic官方博客
- `https://github.com/modelcontextprotocol/servers` — 官方MCP服务器仓库

使用 `mcp__brave-search__brave_web_search` 搜索官方动态：
- `site:docs.anthropic.com "skill" OR "mcp" new`
- `site:anthropic.com blog "claude code" OR "mcp"`
- `site:github.com modelcontextprotocol servers new`

### 1.4 Awesome列表

使用 `mcp__fetch__fetch` 工具获取精选列表：
- `https://github.com/punkpeye/awesome-mcp-servers` — 最全面的社区Awesome MCP列表
- `https://github.com/modelcontextprotocol/awesome-mcp` — 官方Awesome列表

使用 `mcp__brave-search__brave_web_search` 搜索：
- `site:github.com "awesome" "mcp" OR "claude-code"`

### 1.5 时间范围

时间范围：本周周一00:00 UTC 至 本周周日23:59 UTC。
在搜索时使用时效性过滤：优先关注本周内发布、更新或获得显著关注的Skills和MCPs。

### 1.6 URL保留（关键步骤）

> **重要：** 从所有数据源发现的每个Skill和MCP服务器，必须保留其完整URL，供报告中的超链接使用。

1. 从 Brave Search 结果中提取每个项目的完整URL并记录。
2. 从 `mcp__fetch__fetch` 浏览的页面中记录每个项目的URL。
3. **GitHub仓库确认：** 对于从npm或其他来源发现的MCP服务器，使用 `mcp__brave-search__brave_web_search` 以 `site:github.com <项目名称>` 格式查找其GitHub仓库URL。
4. **严禁**根据项目名称猜测或拼接URL。所有链接必须来自搜索或页面浏览的实际结果。
5. 如果无法找到某个项目的可靠URL，则不应将其纳入排名（宁可缺漏，不可给出无效链接）。


## 2. 数据分析

### 2.1 综合评分模型

对每个候选Skill和MCP服务器，按以下公式计算综合得分：

```
综合得分 = (GitHub增长分 * 0.35) 
        + (npm下载分_归一化 * 0.25) 
        + (新近度加分 * 0.25)
        + (官方认可分 * 0.15)
```

各项指标定义：

| 指标 | 说明 | 计算方法 |
|------|------|----------|
| GitHub增长分 | 本周新增Star数量（增长率优先于绝对数量） | (本周新增Star数 / 候选者中最大新增Star数) * 100 |
| npm下载分 | npm包每周下载量 | 仅适用于发布到npm的MCP服务器；对非npm项目，取全部候选npm项目的中位数（使该维度对非npm项目为中性） |
| 新近度加分 | 项目的新颖程度 | 本周首次发布/更新 = 100分；2周内 = 60分；1个月内 = 30分；超过1个月 = 0分 |
| 官方认可分 | 是否获得官方或权威社区认可 | 被列入Anthropic官方文档 = 100分；被列入主流Awesome列表 = 50分；其他 = 0分 |

### 2.2 分类体系

将每个项目按以下维度进行分类：

**功能类别（Category）：**

| 类别 | 说明 | 示例 |
|------|------|------|
| 开发工具 (Development Tools) | IDE集成、代码生成、调试工具、版本控制 | GitHub MCP Server, Git MCP |
| 数据与API (Data & APIs) | 数据库连接器、API封装、数据管道 | PostgreSQL MCP, Brave Search MCP |
| 文件与内容 (File & Content) | 文档处理、媒体处理、文件管理 | Filesystem MCP, Markitdown MCP |
| AI与LLM (AI & LLM) | 提示工程、模型管理、RAG、记忆 | Sequential Thinking, Memory MCP |
| 效率与工作流 (Productivity & Workflow) | 自动化、日程、通知、项目管理 | Todoist MCP, Slack MCP |
| 基础设施与DevOps (Infrastructure & DevOps) | 云服务、容器、监控、部署 | Docker MCP, AWS MCP |
| 网页与浏览器 (Web & Browser) | 网页抓取、自动化测试、浏览器操作 | Puppeteer MCP, Fetch MCP |

**成熟度（Maturity）：**
- 成熟 (Established): 发布超过1年
- 增长中 (Growing): 发布1-12个月
- 新兴 (New): 发布不到1个月

**生态系统角色（Ecosystem Role）：**
- 官方 (Official): 由Anthropic或MCP官方组织维护
- 社区已验证 (Community Verified): 社区广泛认可的高质量项目
- 社区未验证 (Community Unverified): 新出现的社区项目

### 2.3 周环比变化追踪

> **首次运行处理：** 如果 `.claude/output/` 目录下不存在上期报告（文件名匹配 `Weekly_TOP_Skill_MCP_*_dashboard.html`），则"周环比变化"板块标注"首个报告周，环比数据将在下周报告中提供"。

**后续运行：**

1. 使用 `mcp__filesystem__list_directory` 列出 `.claude/output/` 目录下的文件。
2. 筛选出文件名匹配 `Weekly_TOP_Skill_MCP_*_dashboard.html` 的报告文件。
3. 按文件名中的日期排序，找到最近一期（即上一周）的报告文件。
4. 使用 `mcp__filesystem__read_text_file` 读取上一期报告。
5. 从上一期报告中提取TOP 5 Skills和TOP 5 MCPs的排名列表（解析HTML中的排名数据）。
6. 将本周排名与上周排名进行对比，计算每个项目的排名变化：
   - 新上榜 (New): 上周不在TOP 5中
   - 上升 (Up): 排名上升 >= 2位
   - 微升 (Slight Up): 排名上升 1位
   - 持平 (Unchanged): 排名不变
   - 微降 (Slight Down): 排名下降 1位
   - 下降 (Down): 排名下降 >= 2位

### 2.4 数据可视化

使用 `mcp__mcp-server-chart__*` 系列工具生成图表，嵌入报告：

| 图表 | MCP 工具 | 用途 |
|------|---------|------|
| Skills类别分布 | `mcp__mcp-server-chart__generate_pie_chart` | TOP 5 Skills按功能类别分布占比 |
| MCPs类别分布 | `mcp__mcp-server-chart__generate_pie_chart` | TOP 5 MCPs按功能类别分布占比 |
| GitHub增长排行 | `mcp__mcp-server-chart__generate_column_chart` | TOP 5项目的本周GitHub Star增长量对比 |
| 生态系统全景 | `mcp__mcp-server-chart__generate_treemap_chart` | 按类别和成熟度的层级分布图 |

图表以 Markdown 图片格式嵌入 HTML 报告。


## 3. 报告生成

### 3.1 报告标题

- **主标题：** `Weekly TOP Skill & MCP 趋势分析 + 本周周一日期 ~ 本周周日日期`
  - 日期格式：如 `2026年6月1日 ~ 2026年6月7日`
- **副标题：** `第X期 · by 战略助理 with Claude Code + DeepSeek V4 Pro`
  - 期数通过对 `.claude/output/` 目录下已有报告数量+1自动计算

### 3.2 报告结构

报告包含以下七个板块，按顺序排列：

#### 板块一：概览仪表盘（Overview Dashboard）

4个KPI指标卡片，展示在报告顶部：
- **本周新增Skills:** 本周新发现/发布的Skill数量
- **本周新增MCPs:** 本周新发现/发布的MCP服务器数量
- **GitHub Trending项目:** 本周进入GitHub Trending的相关项目数
- **综合热度指数:** 1-100的综合热度评分（基于所有来源的提及和数据总量）

KPI卡片下方附一段50-80字的中文概览总结，概括本周Skill/MCP生态的关键动态。

#### 板块二：TOP 5 Skills（五大热门Skills排行榜）

- 按综合得分从高到低排列的5个Skill
- 每个Skill以卡片形式展示，包含：
  - **排名序号 + 变化标识：** 新上榜标记"NEW"，排名上升标记"↑N"，下降标记"↓N"，持平淡色显示
  - **Skill名称：** 可点击的 `<a href="URL">` 超链接指向项目源（GitHub仓库或官方文档页面）
  - **简短描述：** 1-2句中文摘要，说明Skill的核心功能
  - **类别标签：** 彩色chip样式，标注功能类别
  - **关键指标：** GitHub Stars总数 / 本周新增、成熟度、生态系统角色
  - **综合得分条形图：** 用CSS条形图直观展示综合得分（满分100）
- 排名第1的Skill使用高亮卡片样式（区别于其他卡片）

#### 板块三：TOP 5 MCP Servers（五大热门MCP服务器排行榜）

结构与板块二相同，额外增加：
- **npm周下载量**（如适用），标注在指标区域
- 卡片内同时包含GitHub仓库链接和npm包链接（如适用）

#### 板块四：类别分析（Category Analysis）

- 两张饼图并排：Skills类别分布、MCPs类别分布
- 一段100字左右的类别趋势分析文字
- 一张Treemap图展示生态系统全景（按类别和成熟度层级）

#### 板块五：周环比变化（Week-over-Week Changes）

- **新上榜（New Entries）：** 本周新进入TOP 5的项目列表
- **排名上升（Risers）：** 排名较上周上升的项目
- **排名下降（Fallers）：** 排名较上周下降的项目
- **保持稳定（Stable）：** 连续两周在榜且排名不变的项目
- 如果为首期报告：显示 "首个报告周，环比数据将在下周报告中提供"

#### 板块六：值得关注（Worth Watching）

- TOP 6-10的荣誉提名列表（简要卡片，不含详细指标）
- 一个"编辑推荐 (Editor's Pick)"特殊标注：选取一个本周特别有潜力但综合得分未进TOP 5的项目，附上推荐理由（50字左右）

#### 板块七：趋势总结与展望（Trend Summary & Outlook）

- 3-5条本周生态关键趋势观察
- 下周值得关注的动态预告
- 推荐1-2个值得尝试的Skill或MCP（可以是TOP 5之外的新发现）

### 3.3 报告格式

- 中文撰写，HTML格式
- 使用 `mcp__filesystem__read_text_file` 读取 `.claude/output-styles/template-dashboard.html` 模板文件作为格式参考
- 扩展模板的CSS变量，增加类别标签颜色（至少7种颜色对应7个类别）、排名标识颜色（绿色上升、红色下降、蓝色NEW）
- 每个项目卡片包含可点击的来源链接
- 图表以 Markdown 图片格式嵌入
- 所有日期、指标标签清晰展示

### 3.4 输出位置和文件命名

- 使用 `mcp__filesystem__write_file` 将报告写入 `.claude/output/` 路径下
- 文件名格式：`Weekly_TOP_Skill_MCP_<周一日期YYYYMMDD>_<周日日期YYYYMMDD>_dashboard.html`
- 示例：`Weekly_TOP_Skill_MCP_20260601_20260607_dashboard.html`
- 日期格式统一使用 `YYYYMMDD`（8位数字）

### 3.5 单份报告输出

仅输出一份dashboard格式的HTML报告，不需要outlook格式。


## 4. 评估与校对

### 4.1 数据准确性

- 每个TOP 5条目必须有至少2个独立来源交叉验证（如GitHub + npm、或GitHub + Awesome列表）
- 使用 `mcp__fetch__fetch` 直接访问GitHub仓库页面确认Star数量（而非仅依赖搜索摘要）
- npm下载数据使用 `mcp__fetch__fetch` 访问npm包页面确认
- 综合得分在最终排名前重新计算并验证

### 4.2 报告完整性

- 检查七个板块是否全部包含
- 确认TOP 5 Skills和TOP 5 MCPs各有5个条目
- 确认至少嵌入了3张图表
- 确认"值得关注"板块至少包含1个编辑推荐
- 确认"周环比变化"板块存在（即使显示首期消息）

### 4.3 超链接有效性验证

> **关键步骤：** 逐条检查报告中所有外部链接。

1. 对每个GitHub仓库链接，使用 `mcp__fetch__fetch` 验证可正常访问。
2. 对每个npm包链接，使用 `mcp__fetch__fetch` 验证可正常访问。
3. 对博客、文档链接，使用 `mcp__brave-search__brave_web_search` 以 `site:<domain> <关键词>` 格式验证URL正确性。
4. **严禁**报告中出现纯文本来源标注——每个来源引用必须是可点击的 `<a href="...">` 标签。
5. 发现死链（404）时，用 Brave Search 找到正确URL后替换；若找不到正确URL，从报告中移除该条目。

### 4.4 格式与语言检查

- 标题格式正确：主标题包含日期范围，副标题包含署名和期数
- 文件命名符合规范：`Weekly_TOP_Skill_MCP_YYYYMMDD_YYYYMMDD_dashboard.html`
- 报告语言为中文（技术术语如"GitHub", "npm", "MCP", "API"可保留英文）
- HTML结构完整，无破损标签
- CSS样式正确应用（参考template-dashboard.html的视觉风格）
- 图表图片正常显示，无裂图

### 4.5 排名合理性验证

- 检查排名前3的项目是否确实具有显著的指标优势
- 确认没有因数据获取不全而遗漏可能的热门项目（对比Awesome列表中的项目）
- 确认编辑推荐的合理性——推荐理由必须有事实依据
