---
name: chart-visualization
description: 将数据可视化为图表。当用户需要生成柱状图、折线图、饼图、散点图、雷达图、桑基图、思维导图、流程图等图表时调用此技能，通过 mcp__mcp-server-chart MCP 工具生成图表图片
---

请根据用户输入的内容，将数据可视化为图表。

## 步骤
1. 分析用户数据和需求，选择最合适的图表类型
2. 构造符合 MCP 工具参数规范的数据和配置
3. 使用 `mcp__mcp-server-chart__generate_*` 对应的 MCP 工具生成图表
4. MCP 工具直接返回图表图片，以 Markdown 图片格式呈现

## 图表选择指南

根据用户的数据特征和需求，选择最合适的图表类型：

- **时间序列**：用 `line`（趋势）或 `area`（累计趋势）；两个不同量纲用 `dual-axes`
- **比较类**：用 `bar`（横向分类对比）或 `column`（纵向分类对比）；频率分布用 `histogram`
- **占比类**：用 `pie`（比例构成）或 `treemap`（层级占比）
- **关系与流程**：用 `scatter`（相关性）、`sankey`（流向）或 `venn`（集合重叠）
- **层级与树形**：用 `organization-chart` 或 `mind-map`
- **专用类型**：
  - `radar`：多维度对比
  - `funnel`：流程阶段转化
  - `liquid`：百分比/进度
  - `word-cloud`：文本词频
  - `boxplot` / `violin`：统计分布
  - `network-graph`：复杂节点关系
  - `fishbone-diagram`：因果分析
  - `flow-diagram`：流程图
  - `spreadsheet`：结构化数据表或透视表

## MCP 工具映射

每种图表类型对应一个 `mcp__mcp-server-chart` 下的专用工具，直接调用即可：

| 图表类型 | MCP 工具 |
|---------|---------|
| area (面积图) | `mcp__mcp-server-chart__generate_area_chart` |
| bar (条形图) | `mcp__mcp-server-chart__generate_bar_chart` |
| boxplot (箱线图) | `mcp__mcp-server-chart__generate_boxplot_chart` |
| column (柱状图) | `mcp__mcp-server-chart__generate_column_chart` |
| dual-axes (双轴图) | `mcp__mcp-server-chart__generate_dual_axes_chart` |
| fishbone-diagram (鱼骨图) | `mcp__mcp-server-chart__generate_fishbone_diagram` |
| flow-diagram (流程图) | `mcp__mcp-server-chart__generate_flow_diagram` |
| funnel (漏斗图) | `mcp__mcp-server-chart__generate_funnel_chart` |
| histogram (直方图) | `mcp__mcp-server-chart__generate_histogram_chart` |
| line (折线图) | `mcp__mcp-server-chart__generate_line_chart` |
| liquid (水波图) | `mcp__mcp-server-chart__generate_liquid_chart` |
| mind-map (思维导图) | `mcp__mcp-server-chart__generate_mind_map` |
| network-graph (关系图) | `mcp__mcp-server-chart__generate_network_graph` |
| organization-chart (组织架构图) | `mcp__mcp-server-chart__generate_organization_chart` |
| pie (饼图) | `mcp__mcp-server-chart__generate_pie_chart` |
| radar (雷达图) | `mcp__mcp-server-chart__generate_radar_chart` |
| sankey (桑基图) | `mcp__mcp-server-chart__generate_sankey_chart` |
| scatter (散点图) | `mcp__mcp-server-chart__generate_scatter_chart` |
| spreadsheet (表格/透视表) | `mcp__mcp-server-chart__generate_spreadsheet` |
| treemap (矩形树图) | `mcp__mcp-server-chart__generate_treemap_chart` |
| venn (韦恩图) | `mcp__mcp-server-chart__generate_venn_chart` |
| violin (小提琴图) | `mcp__mcp-server-chart__generate_violin_chart` |
| waterfall (瀑布图) | `mcp__mcp-server-chart__generate_waterfall_chart` |
| word-cloud (词云) | `mcp__mcp-server-chart__generate_word_cloud_chart` |

### MCP 独有图表类型

以下图表类型仅在 MCP 工具中可用：

| 图表类型 | MCP 工具 | 说明 |
|---------|---------|------|
| district-map (区域分布图) | `mcp__mcp-server-chart__generate_district_map` | 仅支持中国行政区划，本项目（巴西市场）较少使用 |
| path-map (路径地图) | `mcp__mcp-server-chart__generate_path_map` | 路径规划/行程展示 |
| pin-map (点位地图) | `mcp__mcp-server-chart__generate_pin_map` | POI 点位标记展示 |

## 通用参数

所有图表工具均支持以下参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | string | "" | 图表标题 |
| width | number | 600 | 图表宽度 |
| height | number | 400 | 图表高度 |
| theme | string | "default" | 主题："default" / "academy" / "dark" |
| style.texture | string | "default" | 纹理："default" / "rough"（手绘风格） |
| style.backgroundColor | string | - | 背景色，如 '#fff' |
| style.palette | string[] | - | 自定义配色方案 |

带坐标轴的图表（area, bar, column, line, scatter, histogram, boxplot, violin, waterfall, dual-axes）还支持：
- `axisXTitle`: X轴标题
- `axisYTitle`: Y轴标题

## 各图表 data 格式及调用示例

### area / line（面积图/折线图）
- **data**: `{time: string, value: number, group?: string}[]`
- **可选**: `stack: boolean`（仅 area）
- **可选**: `style.startAtZero: boolean`（仅 line）、`style.lineWidth: number`

### bar（条形图）
- **data**: `{category: string, value: number, group?: string}[]`
- **可选**: `group: boolean` / `stack: boolean`（默认 stack: true）

### column（柱状图）
- **data**: `{category: string, value: number, group?: string}[]`
- **可选**: `group: boolean`（默认 true）/ `stack: boolean`

### scatter（散点图）
- **data**: `{x: number, y: number, group?: string}[]`

### pie（饼图）
- **data**: `{category: string, value: number}[]`
- **可选**: `innerRadius: number`（0-1，生成环形图）

### radar（雷达图）
- **data**: `{name: string, value: number, group?: string}[]`
- **可选**: `style.lineWidth: number`

### funnel（漏斗图）
- **data**: `{category: string, value: number}[]`

### waterfall（瀑布图）
- **data**: `{category: string, value?: number, isTotal?: boolean, isIntermediateTotal?: boolean}[]`

### dual-axes（双轴图）
- **categories**: `string[]`
- **series**: `{type: "column"|"line", data: number[], axisYTitle?: string}[]`

### histogram（直方图）
- **data**: `number[]`
- **可选**: `binNumber: number`

### boxplot / violin（箱线图/小提琴图）
- **data**: `{category: string, value: number, group?: string}[]`
- **可选**: `style.startAtZero: boolean`

### liquid（水波图）
- **percent**: `number`（0-1）
- **可选**: `shape: "circle"|"rect"|"pin"|"triangle"`

### word-cloud（词云）
- **data**: `{text: string, value: number}[]`

### sankey（桑基图）
- **data**: `{source: string, target: string, value: number}[]`
- **可选**: `nodeAlign: "left"|"right"|"justify"|"center"`

### treemap（矩形树图）
- **data**: `{name: string, value: number, children?: ...}[]`（最深3层）

### venn（韦恩图）
- **data**: `{sets: string[], value: number, label?: string}[]`

### network-graph / flow-diagram（关系图/流程图）
- **data**: `{nodes: {name: string}[], edges: {source: string, target: string, name?: string}[]}`

### fishbone-diagram / mind-map（鱼骨图/思维导图）
- **data**: `{name: string, children?: {name: string, children?: ...}[]}`（最深3层）

### organization-chart（组织架构图）
- **data**: `{name: string, description?: string, children?: ...}[]`（最深3层）
- **可选**: `orient: "horizontal"|"vertical"`

### spreadsheet（表格/透视表）
- **data**: `Record<string, string | number>[]`
- **可选**: `rows: string[]`, `columns: string[]`, `values: string[]`（透视表字段）

### district-map（区域分布图 - MCP独有）
- **title**: 地图标题（不超过16字）
- **data**: `{name: string, dataType?: "number"|"enum", dataValue?: string, subdistricts?: ...}`
- **注意**: 仅支持中国行政区划

### path-map（路径地图 - MCP独有）
- **title**: 地图标题
- **data**: `{data: string[]}[]`（各组POI名称列表）

### pin-map（点位地图 - MCP独有）
- **title**: 地图标题
- **data**: `string[]`（POI名称列表）
- **可选**: `markerPopup: {type: "image", width: number, height: number, borderRadius: number}`
