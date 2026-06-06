---
name: Telecom_Market_Update_Weekly
description: 对巴西电信市场一周的关键动态进行分析，并输出摘要报告。
---

# 巴西电信市场关键动态分析，并输出摘要报告

对巴西电信市场一周的关键动态进行洞察和分析，并输出摘要报告。


## 1. 数据获取

### 1.1 电信新闻网站

使用 `mcp__fetch__fetch` 工具从以下电信专业新闻网站获取完整文章（参数格式：`{"url": "https://...", "max_length": 5000}`）：

- **teletime.com.br** — 巴西电信行业权威新闻
- **dplnews.com/brasil** — 巴西电信/科技新闻
- **convergenciadigital.com.br** — 巴西数字融合与电信新闻

> 仅从以上三个来源获取电信市场新闻，不扩展到其他新闻网站。

### 1.2.1 teletime.com.br URL发现（关键步骤 — 每次必须执行）

> **重要：** teletime.com.br 使用编辑自定义的URL slug，同一篇文章的标题关键词在不同顺序排列下会产生不同的slug。例如，文章 "BNDES aprova R$ 10 milhões do Fust para a Aonet" 的正确slug为 `bndes-aonet-fust/`，而**不是**按标题直译的 `bndes-fust-aonet/`。根据标题直接猜测或拼接slug会导致404错误——读者点击报告中的链接将无法打开目标文章。

**URL发现流程（对每篇拟纳入的 teletime 文章必须执行）：**

1. 使用 `mcp__fetch__fetch` 读取 `https://teletime.com.br` 首页，识别本周要纳入报告的候选文章（通过标题和摘要判断主题和发布日期）。
2. 对每篇候选文章，使用 `mcp__brave-search__brave_web_search` 以 `site:` 查询搜索正确URL：
   - 命令格式：`{"query": "site:teletime.com.br <文章标题中的葡萄牙语关键词>", "count": 5}`
   - 示例：`site:teletime.com.br BNDES aprovou Fust Aonet`
3. 从Brave Search返回结果中提取匹配文章的完整URL，用作报告中该条目的超链接。
4. **严禁**根据文章标题直接拼接或猜测URL slug。所有teletime.com.br的链接必须来自Brave Search `site:` 查询结果。
5. 如果Brave Search未找到某篇文章，则不应在报告中包含该文章（宁可缺漏，不可给出404链接）。


- Anatel公开征询只从https://apps.anatel.gov.br/ParticipaAnatel/获取。

  - **重要：** Anatel网站（gov.br）拦截所有非浏览器HTTP请求。`WebFetch` 工具和 `mcp__fetch__fetch` 工具均会返回 403。
  - 使用PowerShell脚本 `.claude/scripts/fetch-browser.ps1` 替代访问Anatel页面。
  - 命令格式：`& ".claude/scripts/fetch-browser.ps1" -Url "https://apps.anatel.gov.br/ParticipaAnatel/"`，脚本使用Chrome浏览器Headers绕过WAF检测。
  - 脚本输出格式：`OK:<临时文件路径>:<字符数>`。
  - **输出文件复制（关键步骤）：** 脚本将输出写入Windows临时目录（`C:\Users\...\AppData\Local\Temp\...`），而 `mcp__filesystem__read_text_file` 仅能访问项目目录内的路径。**必须先将临时文件复制到项目目录：**
    1. 从脚本输出的 `OK:` 行提取临时文件完整路径。
    2. 使用 `bash cp` 复制到项目输出目录：`cp "<临时文件路径>" ".claude/output/anatel_page_<YYYY-MM-DD>.txt"`
       - 示例：`cp "C:/Users/.../Temp/tmpXXXXXX.txt" ".claude/output/anatel_page_2026-06-05.txt"`
    3. 使用 `mcp__filesystem__read_text_file` 读取 `.claude/output/anatel_page_<YYYY-MM-DD>.txt` 的内容进行分析。

  - **数据来源严格限定：** Anatel公开征询板块的所有内容必须直接来自Anatel门户页面，**禁止**使用新闻报道中的信息填充该板块。页面中"Consultas Abertas"部分列出了当前进行中的公开征询，每条征询包含编号、发布日期、标题、状态和负责部门。

- 只从上面提到的来源获取。

- 时间范围：本周周一到周五的新闻和Anatel公开征询。
  - **Anatel公开征询时间过滤：** 仅纳入**发布日期（publicação）在本周周一至周五范围内**的公开征询。不要将发布日期在本周之前但状态为"进行中（Aberta）"的征询列入"本周Anatel公开征询"板块。
  - 如果本周没有新发布的公开征询，则如实标注"本周无新发布公开征询"，不得用往期征询充数。

### 1.2 新闻搜索（补充来源）

使用 `mcp__brave-search__brave_web_search` 工具搜索电信新闻作为补充来源（参数格式：`{"query": "关键词", "count": 10}`）：

- **综合搜索：** `telecom Brasil notícias`, `mercado telecomunicações Brasil`
- **监管动态：** `Anatel decisão`, `Mcom Brasil telecom`
- **运营商动态：** `VIVO Claro TIM Brasil mercado`, `Brisanet Unifique Algar`
- **URL发现（teletime.com.br）：** 使用 `site:teletime.com.br <文章关键词>` 格式搜索每篇候选文章的正确URL。具体流程见下方 1.2.1 节

> **注意：** brave-search 仅作为补充来源，主力新闻源仍然来自上方 1.1 节指定的三大电信新闻网站。


## 2. 数据分析

- 电信市场动态分析：

    - 分析新闻的标题、内容、来源和发布时间。

    - 根据新闻的标题和内容，判断其所属的分类。分类如下：

        - 监管机构：Mcom、Anatel。

        - 关键客户：VIVO、Claro、TIM、Algar、Brisanet、Unifique、Amazonia、iez。

        - 关键事件：U6G、700MHz、850MHz、RQUAL、Quality Seals、Spectrum Auction、FUST、FISTEL、FUNTTEL、5G Obligation。

    - 将新闻归类到相应的分类中。

    - 如果同一新闻出现在多个分类中，以新闻主要内容的归属作为分类。

    - 按新闻发布时间倒序进行分析。

- Anatel公开征询分析：

    - 从Anatel门户页面中提取"Consultas Abertas"（进行中的公开征询）列表。每条征询包含：编号（CP nº）、发布日期（de dd/mm/yyyy）、标题、状态、负责部门（Órgão）。

    - **时间过滤（关键）：** 仅保留发布日期在本周周一至周五范围内的征询。过滤规则：
        - 征询编号中的日期（如"CP nº 22 de 25/05/2026"中的25/05/2026）即为发布日期。
        - 如果发布日期 < 本周周一 → **排除**（即使状态为"Aberta"）。
        - 如果发布日期 > 本周周五 → **排除**（未来发布的不属于本周）。
        - 仅发布日期在本周范围内 → **纳入**。

    - 分析公开征询的标题和内容，判断是否为我们关心的领域。

    - 我们关注的领域包括：频谱拍卖、卫星通信、网络安全、网络质量、覆盖义务等。
      - 对于不在关注领域内的征询（如广播Basic Plans），仍应列入报告但标注其实际领域。

    - 按公开征询发布日期倒序排列。

    - **补充信息：** Anatel页面中非"Consultas Abertas"部分的内容（如左侧导航中的"Espectro"、"Rede Óptica"、"Sanções"等主题分类），不要放到报告中。


## 3. 报告生成

- 报告标题：巴西电信市场一周动态 + 本周周一日期 ~ 本周周五日期 + “by 战略助理 with Claude Code + DeepSeek V4 Pro”。

- 报告包含以下部分：

    - 本周电信市场动态：

        - 监管机构动态：
            - 包含*监管机构*的动态。
            - 对事件/新闻进行摘要，不需要额外信息。
            - 单击摘要可以打开相关新闻的详细链接。

        - 关键客户动态：
            - 包含*关键客户*的动态。
            - 对事件/新闻进行摘要，不需要额外信息。
            - 单击摘要可以打开相关新闻的详细链接

        - 关键事件动态：
            - 包含*关键事件*的动态。
        - 对事件/新闻进行摘要，不需要额外信息。
        - 单击摘要可以打开相关新闻的详细链接。

        - 如果同一新闻出现在多个分类中，以新闻主要内容的归属作为分类，并且只在报告中出现一次。

    - 本周Anatel公开征询：

        - 包含*Anatel公开征询*的动态。
        - 对公开征询进行摘要，不需要额外信息。
        - 单击摘要可以打开相关公开征询的详细链接。

- 报告使用中文撰写，输出html格式。

- 输出两份报告，内容一样，但格式不同：

    - 第一份为普通html格式，可以内容可以直接复制并粘贴到outlook邮件中，格式友好。
    - 文件名命名：巴西电信市场一周动态 + _ + 本周周一日期（格式 YYYY-MM-DD） + _ + 本周周五日期（格式 YYYY-MM-DD） + outlook .html
    - 示例：巴西电信市场一周动态_2026-06-01_2026-06-05_outlook.html

    - 第二份参考”.claude/output-styles/template-dashboard.html”格式。
    - 文件名命名：巴西电信市场一周动态 + _ + 本周周一日期（格式 YYYY-MM-DD） + _ + 本周周五日期（格式 YYYY-MM-DD） + dashboard .html
    - 示例：巴西电信市场一周动态_2026-06-01_2026-06-05_dashboard.html

- 报告最后不要增加新闻来源和链接。

- 使用 `mcp__filesystem__read_file` 读取 `.claude/output-styles/template-dashboard.html` 模板文件作为第二份报告的格式参考。

- 使用 `mcp__filesystem__write_file` 将两份报告写入 `.claude/output/` 路径下。


## 4. 评估与校对

- 报告标题：检查格式是否正确。

- 报告结构：检查是否包含所有要求的部分。

- 语言与格式：确保内容是中文且格式为 HTML。

- 摘要准确性：对比原始信息来源，确保摘要没有错误或遗漏关键细节。

- 时间范围：确认报告内容仅覆盖本周周一到周五。
  - 逐条检查Anatel公开征询的发布日期，确保每条征询的发布日期均在本周范围内。

- 数据来源验证：
  - Anatel公开征询板块：确认所有内容均来自Anatel门户页面（apps.anatel.gov.br/ParticipaAnatel），**无**来自新闻网站的信息混入。
  - 如果Anatel页面中某条征询的摘要信息不足，不得从新闻中补充——保持从Anatel页面获取的原始信息即可。

- 超链接有效性验证：
  - 逐条检查报告中所有外部文章链接（teletime.com.br、dplnews.com、convergenciadigital.com.br 等来源），确认链接可正常打开目标文章而非404或错误页面。
  - **teletime.com.br 专项检查：** 确认报告中每条 teletime 链接均来自 Brave Search `site:teletime.com.br` 查询结果，而非根据标题猜测的URL。如果任何 teletime 链接的来源无法追溯到 Brave Search 查询，必须使用 `mcp__brave-search__brave_web_search` 重新验证。
  - 对其他来源（dplnews.com/brasil、convergenciadigital.com.br）的链接，如果存疑，同样使用 `site:<域名> <关键词>` 格式通过 Brave Search 确认。
  - 发现死链（404）时，必须用 Brave Search 找到正确URL后替换；如果搜索结果中无法找到该文章的正确URL，则从报告中移除该条目。

- 关键要素：检查是否涵盖所有指定的监管机构、客户和事件。

- 内容重复：确保同一个事件只出现一次。
