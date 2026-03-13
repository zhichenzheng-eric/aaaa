# Demand Doc: Tech Internet 四大巨头财报分析与互动式汇报教学平台

> **版本**: 终极版 | **更新日期**: 2026-03-12

---

## 一、项目核心目标

基于 **Python** 构建自动化数据流，针对 **Tech Internet 行业**的 `Tencent`、`Google`、`Meta`、`Microsoft` 进行深度行业与财务比对。项目将通过 **Streamlit Community Cloud** 部署为轻量级 Web 应用。

该平台核心目标：
- ✅ 展示精准的图表与深度分析，确保 **40 分的内容准确性**
- ✅ 内置由 **DeepSeek V3.2** 驱动的防限流、低成本**交互式"汇报教练"**
- ✅ 帮助全组实现高质量的演讲配合

---

## 二、工作流架构设计 (三层 Pipeline + 实战演练)

### 🔵 第一层：静态数据与图表引擎 (Data & Viz Pipeline)

| 步骤 | 内容 |
|------|------|
| **数据获取** | 在本地 Antigravity 环境中运行 Python 脚本，通过金融 API 获取 **2022–2024 年**（及最新季报）的核心财务报表数据 |
| **图表生成** | 严格按照作业要求，使用 `Plotly` / `Matplotlib` 自动生成：① 市场规模趋势**折线图**；② 对比 Gross Margin、Net Margin、ROE、Debt-to-Asset Ratio 的**雷达图或柱状图** |
| **核心策略** | **数据静态化** — 所有基础数据获取和图表生成在推送到 Streamlit 云端前全部本地固化，消除大模型幻觉，并节省线上 API 调用的 Token |

---

### 🟢 第二层：多 Tab 结构化内容展示 (Content Layer - 核心教学区)

在 Streamlit 网页中，严格按照作业要求设置 **4 个核心 Tab**。每个 Tab 下方设置 `st.expander`（点击展开），后台 DeepSeek API 强制执行**"双轨输出"**：

- **【报告正文】** → 用于 PPT 内容
- **【💡 推导逻辑与讲稿】** → 用于组员演讲排练

---

#### Tab 1: 行业概览 (Industry Overview)

**严格覆盖指标：**

- 行业定义 (Definition)
- 产业链位置 (Position in the industry chain)
- 市场规模 (Market size)
- 增长趋势 (Growth trends) — **必须配图表**

**双轨输出示例：**

> **【报告正文】**：输出科技互联网行业的精准定义及市场规模数据。
>
> **【💡 推导逻辑与讲稿】**：「这页 PPT 大家重点指着这个增长趋势图讲。先说明我们在产业链属于哪一层，然后再引出这块蛋糕 (Market size) 每年还在以什么速度变大。」

---

#### Tab 2: 行业核心财务特征 (Core Financial Characteristics of the Industry)

**严格覆盖指标（绝不漏项）：**

- 典型毛利率区间及其驱动因素 (Typical Gross Margin range and its drivers: brand premium / technology / cost structure)
- 费用结构 (Expense structure: R&D-driven or Sales-driven)
- 盈利能力 (Profitability: industry average for Net Margin and ROE)
- 资产负债特征 (Asset and debt characteristics: leverage level, cash reserves)

**双轨输出示例：**

> **【报告正文】**：列出行业平均 Net Margin 和 ROE 数据，明确其 R&D-driven 的属性。
>
> **【💡 推导逻辑与讲稿】**：「讲这页时逻辑要一环扣一环：先用高额的现金储备 (cash reserves) 和低杠杆率说明这行不缺钱；再切入费用结构，告诉老师这些钱没拿去搞销售，而是砸在了 R&D 上；最后得出结论，正是这种技术壁垒 (technology) 带来了超高的毛利区间。」

---

#### Tab 3: 四家公司财务横向比对 (Financial Comparison of the Four Companies)

**严格覆盖指标：**

- 使用**雷达图或柱状图**对比核心指标：`Gross Margin`、`Net Margin`、`ROE`、`Debt-to-Asset Ratio` 等
- 分析差异原因 (Analyze reasons for differences: e.g., scale, positioning, business model)

**双轨输出示例：**

> **【报告正文】**：结合生成的雷达图，点出四家公司在 ROE 和 Debt-to-Asset Ratio 上的显著差异。
>
> **【💡 推导逻辑与讲稿】**：「展示雷达图时，直接对比 Meta 和 Microsoft 的资产负债率差异。你要强调：这不是谁好谁坏的问题，这是商业模式 (business model) 和市场定位 (positioning) 的区别。微软有庞大的 ToB 云资产，而 Meta 纯靠 ToC 广告流量。」

---

#### Tab 4: 行业展望与核心投资关注点 (Industry Outlook and Key Investment Focus Points)

**严格覆盖指标：**

- 机遇与挑战 (Opportunities and challenges)
- 投资该行业需关注的关键财务指标 (Key financial metrics to focus on when investing)
- *(报告完整性追加)* 最终结论：哪家公司最具投资价值及原因

**双轨输出示例：**

> **【报告正文】**：列出未来 AI 带来的机遇与反垄断挑战，圈定投资关注核心指标。
>
> **【💡 推导逻辑与讲稿】**：「结尾升华部分，别光念子弹头。告诉老师，在这个行业里投钱，不仅要看现在的净利率，更要盯紧他们的研发转化率和自由现金流，这是应对未来挑战的唯一底气。」

---

### 🔴 第三层：低成本交互式辅导教练 (Interactive Coaching Hub)

在每个 Tab 底部嵌入专属的 `st.chat_input` 聊天框，组员可随时针对当前页面的特定指标提问（例如：「老师如果问我为什么没选某某指标，怎么圆？」）。

---

### 🔥 终极杀手锏：红队测试 Q&A 模拟器 (Red Team Simulator)

在页面最后一个专属区域，点击 **"生成刁钻提问"** 按钮，触发以下三段式输出：

| 输出模块 | 内容 |
|----------|------|
| **【模拟提问】** | 基于前四个 Tab 的分析，DeepSeek 模拟苛刻老师生成 **3 个最可能的 Q&A 提问** |
| **【标准防守话术】** | 提供逻辑严密、可直接背诵的**口语化回答** |
| **【防守数据索引】** | 明确提示组员应立刻引导大家看哪个 Tab 下的哪张雷达图或折线图 |

---

## 三、API 成本控制与安全阀设计 (Cost-Control Mechanisms)

为彻底保护 API 余额，部署以下 **四道防线**：

| 防线 | 机制 | 实现方式 |
|------|------|----------|
| 🛡️ **铁腕 System Prompt** | 拒绝回答任何非本作业、非四家公司财报无关的问题 | Prompt Engineering |
| 🎭 **大师级角色扮演** | 以资深量化分析师 / 投资大师口吻进行 Q&A 模拟，提升护城河理论等高级框架的应用 | System Role Definition |
| 🔒 **Session 状态阻断** | 单用户会话最多提问 **15 次**，超限后冻结输入框 | `st.session_state` |
| ✂️ **动态滑动窗口** | 仅保留最近 **2 轮**对话上下文，截断历史废话，极大控制单次发包的 Token 消耗 | Context Window Management |

---

## 四、技术栈总览

```
Frontend / UI     →  Streamlit (Multi-Tab + Expander + Chat)
数据可视化         →  Plotly / Matplotlib
数据源             →  金融 API（本地预获取，静态化存储）
AI 教练引擎        →  DeepSeek V3.2 API
部署环境           →  Streamlit Community Cloud
本地开发环境        →  Python + Antigravity
```

---

## 五、项目优先级与评分保障

| 维度 | 目标 |
|------|------|
| 内容准确性 | 40 分（严格覆盖所有作业指标，绝不漏项）|
| 图表质量 | 雷达图 + 折线图双配置，数据来源清晰 |
| 演讲配合 | 双轨输出 + Red Team 模拟器，全组备战 |
| 成本控制 | 四道安全阀，API 余额零燃尽风险 |
