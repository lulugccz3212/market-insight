---
name: Brazil_Election_Weekly
description: 对巴西大选每周动态进行分析，包括左派右派支持率、竞选政策，尤其是对华为有影响的政策分析，并输出摘要报告。
---

# 巴西大选每周动态分析，并输出摘要报告

对巴西2026年总统大选每周关键动态进行洞察分析，重点关注左派和右派支持率变化、新竞选政策提案，以及影响华为在巴西业务的政策分析。

## 1. 数据获取

### 1.1 民调数据

使用 `mcp__brave-search__brave_web_search` 工具搜索以下关键词获取最新民调数据（参数格式：`{"query": "关键词", "count": 10}`）：

**葡萄牙语关键词：**
- `Pesquisa eleitoral 2026 Brasil`
- `intenção de voto 2026 presidente`
- `Datafolha 2026`
- `Quaest 2026 eleição`
- `Ipec pesquisa 2026`
- `AtlasIntel 2026 Brasil`
- `Paraná Pesquisas 2026`

**英语关键词：**
- `Brazil election polls 2026`
- `Brazil presidential race 2026 latest polls`
- `Lula approval rating 2026`

> **提示：** 优先使用葡萄牙语关键词搜索，可获得更丰富的巴西本地新闻源结果。

**民调数据关键指标：**
- 各候选人的投票意向（intenção de voto）
- 模拟对决场景（cenários estimulados）
- 自发投票（cenário espontâneo）
- 连任评估（avaliação de governo - ótimo/bom/regular/ruim/péssimo）
- 拒绝率（rejeição）

**主要民调机构：** Datafolha, Quaest, Ipec, AtlasIntel, Paraná Pesquisas, Futura/ModalMais

### 1.2 左派政策动态

使用 `mcp__brave-search__brave_web_search` 工具搜索（参数格式：`{"query": "关键词", "count": 10}`）：

**葡萄牙语关键词：**
- `Lula propostas 2026`
- `PT programa governo 2026`
- `Haddad candidato 2026 propostas`
- `esquerda Brasil políticas 2026 telecom`

**英语关键词：**
- `Lula reelection policies 2026`
- `Brazil left-wing campaign platform 2026`
- `Brazil PT technology policy 2026`

**左派主要力量：** PT（劳工党）, PSB, PSOL, PCdoB, PDT 等
**可能的候选人：** Luiz Inácio Lula da Silva (PT), Fernando Haddad (PT), Gleisi Hoffmann (PT) 等

### 1.3 右派政策动态

使用 `mcp__brave-search__brave_web_search` 工具搜索（参数格式：`{"query": "关键词", "count": 10}`）：

**葡萄牙语关键词：**
- `Tarcísio de Freitas 2026 propostas`
- `direita Brasil candidato 2026`
- `PL programa governo 2026`
- `Zema 2026 presidência`
- `Ratinho Júnior 2026`

**英语关键词：**
- `Brazil right-wing candidate 2026 policies`
- `Tarcísio Freitas campaign 2026`
- `Brazil conservative platform 2026`

**右派主要力量：** PL, Republicanos, PSD, Novo, PP, União Brasil 等
**可能的候选人：** Tarcísio de Freitas (Republicanos), Romeu Zema (Novo), Ratinho Júnior (PSD), Ronaldo Caiado (União Brasil) 等
**注意：** Jair Bolsonaro (PL) 被TSE裁定在2030年前无被选举资格。

### 1.4 华为相关政策

使用 `mcp__brave-search__brave_web_search` 工具搜索（参数格式：`{"query": "关键词", "count": 10}`）：

**葡萄牙语关键词：**
- `Huawei Brasil 5G 2026`
- `Huawei telecom Brasil governo`
- `China Brasil tecnologia parceria 2026`
- `Huawei Anatel regulamentação`

**英语关键词：**
- `Huawei Brazil 5G policy 2026`
- `US pressure Brazil Huawei`
- `China Brazil telecom cooperation 2026`
- `Huawei Brazil ban 5G`

### 1.5 补充新闻来源

使用 `mcp__fetch__fetch` 工具从以下巴西主流新闻网站获取深度报道（参数格式：`{"url": "https://...", "max_length": 5000}`）：

- `www1.folha.uol.com.br` — Folha de S.Paulo (巴西最大报纸)
- `oglobo.globo.com` — O Globo
- `www.estadao.com.br` — Estadão
- `www.poder360.com.br` — Poder360 (政治新闻专业网站)
- `www.metropoles.com` — Metrópoles
- `www.cnnbrasil.com.br` — CNN Brasil
- `congressoemfoco.uol.com.br` — Congresso em Foco (聚焦国会)

> **URL发现提示：** 从以上来源浏览到具体文章后，使用 `mcp__brave-search__brave_web_search` 以 `site:<domain> <文章标题关键词>` 查询确认文章URL。不要直接根据浏览到的标题拼接URL——巴西主流新闻网站（如 folha.uol.com.br、oglobo.globo.com）的URL结构由CMS自动生成，无法从标题预测。
> 
> **注意：** 部分巴西新闻网站可能有付费墙限制，如果 `mcp__fetch__fetch` 返回内容不完整或被拦截，可改用 `mcp__brave-search__brave_web_search` 搜索该文章标题获取摘要内容作为补充。

### 1.6 URL保留（关键步骤）

> **重要：** 从所有数据源发现的每篇文章，必须保留其完整URL，供报告中的超链接使用。

1. 从 Brave Search（§1.1-§1.4）结果中提取每篇文章的完整URL并记录。
2. 从 `mcp__fetch__fetch`（§1.5）浏览新闻网站时，记录发现的每篇文章的完整URL。
3. 对从 §1.5 来源发现的文章，使用 `mcp__brave-search__brave_web_search` 以 `site:<domain> <keywords>` 格式确认正确URL：
   - 示例：`site:valor.globo.com Flávio Bolsonaro plano governo`
4. **严禁**根据文章标题猜测或拼接URL。所有链接必须来自 Brave Search `site:` 查询结果或 `mcp__fetch__fetch` 返回的原始URL。
5. 如果 Brave Search 未找到某篇文章，则不应在报告中包含该文章（宁可缺漏，不可给出无效链接）。

## 2. 数据分析

### 2.1 民调数据分析
- 整理各民调机构最新一轮调查的核心数据
- 计算左派和右派候选人的平均投票意向
- 对比近几周的数据趋势（上升/下降/稳定）
- 识别关键变化点和可能的原因

### 2.2 政策分析
- 按阵营（左派/右派）整理本周新提出的竞选政策
- 对每条政策进行分类：
  - 经济政策（Economia）
  - 外交政策（Política Externa）
  - 科技/电信政策（Tecnologia/Telecomunicações）
  - 社会政策（Política Social）
  - 基础设施（Infraestrutura）
  - 其他（Outros）
- 对政策进行摘要，包含：政策内容、提出人/政党、提出日期、政治背景

### 2.3 华为影响分析（核心分析板块）

> **分析工具推荐：** 对于涉及多维度交叉影响的复杂政策分析，建议使用 `mcp__sequential-thinking__sequentialthinking` 工具进行结构化推理。按照以下链条逐步分析每条政策：
> ```
> 政策内容 → 直接影响维度识别 → 间接影响维度识别 → 交叉影响评估 → 综合影响评级
> ```
> 当一条政策同时涉及5G基础设施、网络安全法规和中美巴三角关系等多个维度时，sequential-thinking 可帮助系统化地梳理影响链条，避免遗漏关键因素。

对每条可能影响华为的政策进行多维度评估：

**直接影响维度：**
- 5G/电信基础设施政策：是否有限制或欢迎中国设备的提案
- 网络安全法规：设备认证要求、"可信供应商"政策
- 频谱拍卖规则：是否设置技术/地缘政治门槛
- Anatel监管决定：设备认证、频谱分配、市场准入

**间接影响维度：**
- 中美巴西三角关系：美国对巴西的压力程度
- 中巴经贸关系：一带一路参与、技术转让协议
- 产业链政策：本地化要求、技术转移条款

**影响评级：**
- 🟢 正面（Positive）— 有利于华为在巴西的市场拓展和运营
- 🟡 中性（Neutral）— 对华为业务无明显影响
- 🔴 负面（Negative）— 可能限制或损害华为在巴西的业务
- ⚪ 不确定（Uncertain）— 影响方向尚不明确，需持续关注

### 2.4 时间范围
- 仅分析本周（周一至周六）的新闻和动态
- 民调数据可放宽至最近2-3周，确保有足够的数据支撑分析

### 2.5 数据可视化

使用 `mcp__mcp-server-chart__*` 系列工具生成图表，将关键数据以可视化形式嵌入报告中：

| 图表 | MCP 工具 | 用途 |
|------|---------|------|
| 民调趋势图 | `mcp__mcp-server-chart__generate_line_chart` | 各候选人近几周支持率变化趋势，x轴为时间，y轴为支持率%，可按候选人用 `group` 字段分组 |
| 支持率对比图 | `mcp__mcp-server-chart__generate_column_chart` | 左右派主要候选人当前支持率横向对比 |
| 政策分类分布图 | `mcp__mcp-server-chart__generate_pie_chart` | 本周政策按类型（经济/外交/科技/社会/基础设施）分布占比 |
| 华为影响雷达图 | `mcp__mcp-server-chart__generate_radar_chart` | 华为政策环境多维度评估（5G政策、网络安全、市场准入、中美压力、中巴合作） |

图表以 Markdown 图片格式嵌入 HTML 报告的对应板块中。

## 3. 报告生成

### 3.1 报告标题
- 主标题：`巴西大选每周动态分析 + 本周周一日期 ~ 本周周六日期`
- 副标题：`by 战略助理 with Claude Code + DeepSeek V4 Pro`

### 3.2 报告结构

报告包含以下五个板块：

#### 板块一：选情概览（Election Overview）
- KPI指标卡片展示：
  - 左派主要候选人平均支持率
  - 右派主要候选人平均支持率
  - Lula政府支持率（ótimo/bom %）
  - Lula政府反对率（ruim/péssimo %）
- 民调趋势简要分析
- 数据来源标注（民调机构名称、日期、样本量）

#### 板块二：左派政策动态（Left-wing Policy Updates）
- 本周左派重要竞选政策/言论
- 每条政策：标题（含可点击的 `<a href="URL">` 超链接指向原文）、摘要、提出人/政党、发布日期
- 所有链接必须来自数据获取阶段（§1.6）保留的URL
- 对科技/电信相关政策进行重点标注

#### 板块三：右派政策动态（Right-wing Policy Updates）
- 本周右派重要竞选政策/言论
- 每条政策：标题（含可点击的 `<a href="URL">` 超链接指向原文）、摘要、提出人/政党、发布日期
- 所有链接必须来自数据获取阶段（§1.6）保留的URL
- 对科技/电信相关政策进行重点标注

#### 板块四：华为影响分析（Huawei Impact Analysis）
- 本周对华为在巴西业务有影响的政策汇总
- 每条政策详细分析：
  - 政策内容
  - 来源和提出方（含可点击的 `<a href="URL">` 超链接指向原文）
  - 对华为的影响分析（直接/间接）
  - 影响评级（正面/中性/负面/不确定）
  - 影响程度评估（高/中/低）
- 本周华为政策影响总览表
- 趋势判断：整体政策环境对华为的友好度变化

#### 板块五：总结与展望（Summary & Outlook）
- 本周大选动态关键要点（3-5条）
- 对华为在巴西业务影响的综合评估
- 下周需要关注的动态预告
- 风险提示和建议关注方向

### 3.3 报告格式
- 中文撰写，HTML格式
- 使用 `mcp__filesystem__read_file` 读取 `.claude/output-styles/template-dashboard.html` 模板文件作为格式参考
- 每个板块的新闻卡片可点击跳转到原文链接
- 日期、来源标签清晰展示
- 使用 `mcp__mcp-server-chart__*` 工具生成的图表以 Markdown 图片格式嵌入报告
- 文件名：`巴西大选每周动态分析_<周一日期 YYYY-MM-DD>_<周六日期 YYYY-MM-DD>_dashboard.html`
- 示例：`巴西大选每周动态分析_2026-06-01_2026-06-06_dashboard.html`
- 每个新闻卡片的标题或链接区域必须包含可点击的 `<a href="...">` 超链接，链接来自数据获取阶段保留的URL

### 3.4 输出位置
- 使用 `mcp__filesystem__write_file` 将报告写入 `.claude/output/` 路径下

## 4. 评估与校对

### 4.1 数据准确性
- 民调数据至少来自2个不同机构交叉验证
- 政策摘要需引用具体来源URL
- 华为影响分析要基于具体政策提案，避免臆测

### 4.2 报告完整性
- 检查五个板块是否全部包含
- 确保至少分析了1-2条华为相关影响
- 如果没有本周新政策，如实标注"本周无重大新政策发布"
- 如果本周没有对华为直接影响的政策，仍应分析间接政策环境变化
- 确认报告中每条新闻/政策条目均包含可点击的来源链接（`<a href>` 标签），而非纯文本来源标注

### 4.3 平衡性
- 左派和右派政策覆盖均衡
- 华为分析保持事实性和商业视角，避免政治立场偏好
- 报告语言中立客观

### 4.4 格式与链接验证

- 标题格式正确、HTML结构完整
- 文件名符合规范（格式 YYYY-MM-DD，如 `巴西大选每周动态分析_2026-06-01_2026-06-06_dashboard.html`）

**超链接有效性验证（关键步骤）：**

1. 逐条检查报告中所有外部文章链接，确认可正常打开目标文章而非404或错误页面。
2. 确认每个链接均来自数据获取阶段（§1.6）保留的 Brave Search 或 `mcp__fetch__fetch` URL，而非根据标题猜测。
3. 对存疑链接，使用 `mcp__brave-search__brave_web_search` 以 `site:<domain> <关键词>` 格式重新验证。
4. **确认报告中无纯文本来源标注**——每个来源引用必须是可点击的 `<a href="...">` 标签，不得出现仅含域名/媒体名称而无链接的文本（如 `→ 来源: Valor Econômico`）。
5. 发现死链（404）时，用 Brave Search 找到正确URL后替换；若找不到正确URL，从报告中移除该条目。
