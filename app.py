"""
Tech Internet 四大巨头财报分析与互动式汇报教学平台
====================================================
Streamlit App - Complete Version (Layer 1 + 2 + 3)
覆盖公司: Tencent | Google | Meta | Microsoft
AI Engine: DeepSeek V3.2 via OpenAI-compatible API

三层架构:
  Layer 1: 静态数据与图表引擎 (data/ + charts/)
  Layer 2: 多Tab结构化内容展示 + DeepSeek双轨输出
  Layer 3: 交互式辅导教练 + Red Team Q&A模拟器 + 四道安全阀
"""

import streamlit as st
import json
import os
import pandas as pd
import plotly.io as pio
from openai import OpenAI

# ============================================================
# 0. 全局页面配置
# ============================================================
st.set_page_config(
    page_title="Tech Internet 四大巨头 · 财报分析平台",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 0.1 自定义 CSS 样式注入 (Blue Theme)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

    /* Hide sidebar completely */
    section[data-testid="stSidebar"] { display: none !important; }

    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.015em;
        line-height: 1.8;
    }

    /* Markdown body */
    .stMarkdown p, .stMarkdown li {
        font-weight: 400 !important;
        line-height: 1.95 !important;
        letter-spacing: 0.013em !important;
        opacity: 0.88;
    }
    .stMarkdown h1 { font-weight: 900 !important; letter-spacing: -0.02em; line-height: 1.3; }
    .stMarkdown h2 { font-weight: 800 !important; letter-spacing: -0.015em; line-height: 1.4; }
    .stMarkdown h3 { font-weight: 700 !important; letter-spacing: -0.01em; line-height: 1.5; margin-top: 1.2em; }

    /* Bold */
    .stMarkdown strong, .stMarkdown b,
    .stMarkdown p strong, .stMarkdown li strong,
    .stMarkdown p b, .stMarkdown li b {
        font-weight: 900 !important;
        opacity: 1 !important;
        letter-spacing: 0.003em !important;
    }

    /* Table styles */
    .stMarkdown table {
        border-collapse: collapse;
        width: 100%;
        margin: 1.3rem 0;
        font-size: 0.95rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    .stMarkdown th {
        background: #1a1a2e;
        color: #7FB8E8;
        font-weight: 800;
        padding: 0.7rem 1.1rem;
        text-align: left;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-size: 0.82rem;
    }
    .stMarkdown td {
        padding: 0.7rem 1.1rem;
        border-bottom: 1px solid #e4e4f0;
        line-height: 1.75;
    }
    .stMarkdown tr:hover td { background: rgba(255,255,255,0.06); }

    /* Section title */
    .section-title {
        font-size: 1.3rem; font-weight: 800; color: #4A9EFF;
        border-left: 4px solid #4A9EFF; padding-left: 12px;
        margin: 1.5rem 0 1rem 0; letter-spacing: -0.01em;
    }

    /* Expander header */
    .streamlit-expanderHeader {
        font-weight: 700 !important; font-size: 1rem !important;
        color: #7FB8E8 !important; letter-spacing: 0.01em !important;
    }

    /* Chat divider */
    .chat-divider {
        border-top: 2px solid rgba(74, 158, 255, 0.3);
        margin: 2rem 0 1rem 0; padding-top: 1rem;
    }

    /* Chat bubbles */
    .user-msg {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: white; padding: 0.85rem 1.3rem; border-radius: 12px 12px 2px 12px;
        margin: 0.6rem 0; max-width: 85%; margin-left: auto; text-align: right;
        font-weight: 600; letter-spacing: 0.01em; line-height: 1.75;
    }
    .assistant-msg {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: #e0e0e0; padding: 0.85rem 1.3rem; border-radius: 12px 12px 12px 2px;
        margin: 0.6rem 0; max-width: 85%; border: 1px solid rgba(255,255,255,0.08);
        font-weight: 500; letter-spacing: 0.012em; line-height: 1.85;
    }

    /* Quota badge */
    .quota-badge {
        display: inline-block; background: rgba(74,158,255,0.15); color: #4A9EFF;
        padding: 0.25rem 0.9rem; border-radius: 20px;
        font-size: 0.8rem; font-weight: 700; letter-spacing: 0.04em;
    }

    /* Override all primary buttons to blue (softer blue) */
    button[kind="primary"],
    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #4A9EFF !important;
        border-color: #4A9EFF !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(74, 158, 255, 0.4) !important;
    }
    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        background-color: #3B82F6 !important;
        border-color: #3B82F6 !important;
        box-shadow: 0 6px 20px rgba(74, 158, 255, 0.6) !important;
    }
    button[kind="primary"]:active,
    .stButton > button[kind="primary"]:active {
        background-color: #2563EB !important;
        border-color: #2563EB !important;
    }

    /* Bigger company names in metrics */
    [data-testid="stMetricLabel"] > div > div > p {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em !important;
    }

    /* Page title */
    .page-title {
        font-size: 1.8rem; font-weight: 900; color: #4A9EFF;
        letter-spacing: -0.02em; margin: 0; padding: 0.5rem 0 0.2rem 0;
    }
    .page-subtitle {
        color: #888; font-size: 0.9rem; font-weight: 500;
        letter-spacing: 0.02em; margin-bottom: 1rem;
    }

    /* Custom tab navigation buttons */
    div.tab-nav-row { display: flex; gap: 0.6rem; margin: 0.5rem 0 1.5rem 0; }
    div.tab-nav-row > div { flex: 1; }
    .tab-btn {
        display: flex; align-items: center; justify-content: center;
        width: 100%; text-align: center;
        padding: 0.75rem 0.5rem; border-radius: 10px; cursor: pointer;
        font-family: 'Inter', sans-serif; font-size: 0.92rem; font-weight: 800;
        letter-spacing: 0.01em; transition: all 0.15s ease;
        border: 1.5px solid rgba(74,158,255,0.25);
        background: rgba(74,158,255,0.06); color: #b0b0c8;
    }
    .tab-btn:hover { background: rgba(74,158,255,0.12); color: #e0e0e0; }
    .tab-btn.active {
        background: rgba(74,158,255,0.18); color: #4A9EFF;
        border-color: #4A9EFF; box-shadow: 0 0 12px rgba(74,158,255,0.15);
    }

    /* Red Team specific styling */
    .section-title.red-team {
        color: #FF4B4B !important;
        border-left-color: #FF4B4B !important;
    }
    #red-team-anchor ~ div button[kind="primary"] {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
        box-shadow: 0 4px 14px rgba(255, 75, 75, 0.4) !important;
    }
    #red-team-anchor ~ div button[kind="primary"]:hover {
        background-color: #FF2B2B !important;
        border-color: #FF2B2B !important;
    }

    /* Subsection header (smaller than section title) */
    .subsection-header {
        font-size: 1.1rem; font-weight: 700; color: #e0e0e0;
        margin: 1.5rem 0 0.8rem 0; letter-spacing: 0.01em;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 0.2 语言切换系统
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "中文"

_L = {
    "中文": {
        "title": "Tech Internet 四大巨头 · 财报分析平台",
        "subtitle": "Tencent · Google · Meta · Microsoft | 深度行业比对 · 双轨教学输出 · AI 汇报教练",
        "metrics_header": "关键指标速览",
        "gross_margin": "毛利率",
        "net_margin": "净利率",
        "da_ratio": "资产负债率",
        "tab1": "Tab 1: 行业概览",
        "tab2": "Tab 2: 核心财务特征",
        "tab3": "Tab 3: 四家公司横向比对",
        "tab4": "Tab 4: 行业展望与投资关注",
        "tab1_sec": "行业概览",
        "tab1_points": "- **行业定义** · **产业链位置** · **市场规模** · **增长趋势**（配图表）",
        "tab1_chart": "全球科技互联网市场规模趋势",
        "tab2_sec": "行业核心财务特征",
        "tab2_points": "- **毛利率区间与驱动因素** · **费用结构**（R&D vs Sales）\n- **盈利能力**（Net Margin & ROE）· **资产负债特征**",
        "tab2_chart": "四家公司毛利率对比",
        "tab3_sec": "四家公司财务横向比对",
        "tab3_points": "- **雷达图/柱状图对比** Gross Margin, Net Margin, ROE, Debt-to-Asset\n- **差异原因分析**（规模、定位、商业模式）",
        "tab3_radar": "核心指标雷达图",
        "tab3_table": "详细指标数据表",
        "tab3_col_company": "公司",
        "tab4_sec": "行业展望与核心投资关注点",
        "tab4_points": "- **机遇与挑战**\n- **投资关键财务指标**\n- **最终结论**: 哪家公司最具投资价值及原因",
        "gen_btn": "生成双轨分析",
        "gen_spin1": "DeepSeek 正在生成行业概览的双轨输出...",
        "gen_spin2": "DeepSeek 正在生成核心财务特征的双轨输出...",
        "gen_spin3": "DeepSeek 正在生成横向比对的双轨输出...",
        "gen_spin4": "DeepSeek 正在生成行业展望的双轨输出...",
        "hint_title": "使用说明",
        "hint_tab1": "点击上方 **生成双轨分析** 按钮，DeepSeek 将自动生成报告正文 + Presentation 准备",
        "hint_default": "点击上方 **生成双轨分析** 按钮，生成报告正文 + Presentation 准备",
        "coach": "AI 教练 · 针对本 Tab 提问",
        "coach_ph": "关于「{label}」有什么想问 DeepSeek 教练的？",
        "send": "发送",
        "thinking": "DeepSeek 教练正在思考...",
        "remaining": "剩余: {r}/{t}",
        "limit_warn": "提问次数已达上限 (15 次)，输入框已冻结。请刷新页面开启新会话。",
        "limit_api": "本次会话提问次数已达上限 (15 次)，请刷新页面开启新会话。",
        "redteam_sec": "Red Team Q&A 模拟器",
        "redteam_desc": "模拟苛刻老师的刁钻提问，帮助全组做好答辩准备。点击按钮后 DeepSeek 将生成：\n- **3 个最刁钻的 Q&A 提问** + **标准防守话术** + **防守数据索引**",
        "redteam_btn": "生成刁钻提问",
        "redteam_rem": "剩余 API 调用: {r}/{t}",
        "redteam_max": "已达上限",
        "redteam_spin": "DeepSeek 正在模拟苛刻老师，生成刁钻提问中...",
        "footer1": "Tech Internet 四大巨头财报分析平台 · Powered by Streamlit + DeepSeek V3.2",
        "footer2": "数据来源: yfinance · 图表引擎: Plotly · 部署: Streamlit Community Cloud",
    },
    "English": {
        "title": "Tech Internet Giants · Financial Analysis Platform",
        "subtitle": "Tencent · Google · Meta · Microsoft | Industry Comparison · Dual-Track Output · AI Coaching",
        "metrics_header": "Key Metrics at a Glance",
        "gross_margin": "Gross Margin",
        "net_margin": "Net Margin",
        "da_ratio": "Debt-to-Asset",
        "tab1": "Tab 1: Industry Overview",
        "tab2": "Tab 2: Core Financial Characteristics",
        "tab3": "Tab 3: Financial Comparison",
        "tab4": "Tab 4: Industry Outlook",
        "tab1_sec": "Industry Overview",
        "tab1_points": "- **Industry Definition** · **Value Chain** · **Market Size** · **Growth Trends** (with charts)",
        "tab1_chart": "Global Tech Internet Market Size Trend",
        "tab2_sec": "Core Financial Characteristics",
        "tab2_points": "- **Gross Margin Range & Drivers** · **Expense Structure** (R&D vs Sales)\n- **Profitability** (Net Margin & ROE) · **Asset & Debt Characteristics**",
        "tab2_chart": "Gross Margin Comparison — Four Companies",
        "tab3_sec": "Financial Comparison — Four Companies",
        "tab3_points": "- **Radar/Bar Chart Comparison** Gross Margin, Net Margin, ROE, Debt-to-Asset\n- **Root Cause Analysis** (Scale, Positioning, Business Model)",
        "tab3_radar": "Key Metrics Radar Chart",
        "tab3_table": "Detailed Metrics Table",
        "tab3_col_company": "Company",
        "tab4_sec": "Industry Outlook & Investment Focus",
        "tab4_points": "- **Opportunities & Challenges**\n- **Key Financial Metrics for Investment**\n- **Final Conclusion**: Which company has the highest investment value and why",
        "gen_btn": "Generate Dual-Track Analysis",
        "gen_spin1": "DeepSeek is generating Industry Overview...",
        "gen_spin2": "DeepSeek is generating Core Financial Characteristics...",
        "gen_spin3": "DeepSeek is generating Financial Comparison...",
        "gen_spin4": "DeepSeek is generating Industry Outlook...",
        "hint_title": "How to Use",
        "hint_tab1": "Click **Generate Dual-Track Analysis** above. DeepSeek will produce Report Body + Presentation Prep.",
        "hint_default": "Click **Generate Dual-Track Analysis** above to produce Report Body + Presentation Prep.",
        "coach": "AI Coach · Ask about this Tab",
        "coach_ph": "Any questions about \"{label}\" for the DeepSeek coach?",
        "send": "Send",
        "thinking": "DeepSeek coach is thinking...",
        "remaining": "Remaining: {r}/{t}",
        "limit_warn": "Question limit reached (15). Input is frozen. Please refresh to start a new session.",
        "limit_api": "Session question limit reached (15). Please refresh to start a new session.",
        "redteam_sec": "Red Team Q&A Simulator",
        "redteam_desc": "Simulate tough professor questions to prepare for your defense. DeepSeek will generate:\n- **3 toughest Q&A questions** + **Standard defense talking points** + **Data reference index**",
        "redteam_btn": "Generate Tough Questions",
        "redteam_rem": "Remaining API calls: {r}/{t}",
        "redteam_max": "Limit reached",
        "redteam_spin": "DeepSeek is simulating a tough professor...",
        "footer1": "Tech Internet Giants Financial Analysis Platform · Powered by Streamlit + DeepSeek V3.2",
        "footer2": "Data: yfinance · Charts: Plotly · Deployed on Streamlit Community Cloud",
    }
}


def t(key):
    return _L[st.session_state.lang].get(key, key)


# ============================================================
# 1. Session State 初始化 + 安全阀配置
# ============================================================
MAX_QUESTIONS = 15
SLIDING_WINDOW = 2

def init_session_state():
    defaults = {
        "question_count": 0,
        "chat_histories": {f"tab{i}": [] for i in range(1, 5)},
        "dual_track_cache": {},
        "red_team_cache": None,
        "active_tab": "tab1",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# ============================================================
# 2. 加载静态数据与图表
# ============================================================
@st.cache_data
def load_financial_metrics():
    data_path = os.path.join(os.path.dirname(__file__), "data", "financial_metrics.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_plotly_chart(filename):
    """加载之前在 Layer 1 预生成的 Plotly JSON 图表"""
    chart_path = os.path.join(os.path.dirname(__file__), "charts", filename)
    with open(chart_path, "r", encoding="utf-8") as f:
        # 使用 skip_invalid 避免跨环境/版本时的模板解析错误
        return pio.from_json(f.read(), skip_invalid=True)

metrics = load_financial_metrics()
radar_fig = load_plotly_chart("radar_chart.json")
market_fig = load_plotly_chart("market_size_trend.json")

for trace in market_fig.data:
    trace.line.color = "#22C55E"
    trace.marker.color = "#22C55E"

# Define language-specific chart titles and axes
radar_title = "四大科技巨头核心财务指标对比分析" if st.session_state.lang == "中文" else "Four Companies Financial Comparison"
market_title = "全球科技互联网市场规模趋势" if st.session_state.lang == "中文" else "Global Tech Internet Market Size Trend"

radar_categories = {
    "Gross Margin": "毛利率" if st.session_state.lang == "中文" else "Gross Margin",
    "Net Margin": "净利率" if st.session_state.lang == "中文" else "Net Margin",
    "ROE": "净资产收益率" if st.session_state.lang == "中文" else "ROE",
    "Debt-to-Asset": "资产负债率" if st.session_state.lang == "中文" else "Debt-to-Asset Ratio"
}

for trace in radar_fig.data:
    trace.fill = "none"
    trace.line = dict(width=2.5)
    # Dynamically translate radar axes based on language
    if hasattr(trace, 'theta') and trace.theta is not None:
        translated_theta = []
        for t in trace.theta:
            # We match the original english string in the JSON
            if "Gross Margin" in t: translated_theta.append(radar_categories["Gross Margin"])
            elif "Net Margin" in t: translated_theta.append(radar_categories["Net Margin"])
            elif "ROE" in t: translated_theta.append(radar_categories["ROE"])
            elif "Debt-to-Asset" in t: translated_theta.append(radar_categories["Debt-to-Asset"])
            else: translated_theta.append(t)
        trace.theta = tuple(translated_theta)

radar_fig.update_layout(
    title=radar_title,
    polar=dict(
        domain=dict(x=[0.15, 0.85], y=[0.05, 0.85]),
        angularaxis=dict(tickfont=dict(size=14, family="Inter, sans-serif", color="#e0e0e0")),
        radialaxis=dict(visible=True, range=[0, 0.9], tickfont=dict(size=11, color="#999")),
    ),
    margin=dict(l=20, r=20, t=60, b=60),
)

market_fig.update_layout(
    title=market_title
)

FINANCIAL_CONTEXT = json.dumps(metrics, indent=2, ensure_ascii=False)


# ============================================================
# 3. DeepSeek API 引擎
# ============================================================
SYSTEM_PROMPT = f"""你是一位资深量化分析师和投资大师，专精于 Tech Internet 行业的财务分析与估值。
你的分析对象严格限定为以下四家公司：Tencent (腾讯), Google (Alphabet), Meta, Microsoft (微软)。

【铁腕规则 - 严格执行】
1. 你只回答与本次作业（Tech Internet 行业的行业分析、财报比对、投资展望）直接相关的问题。
2. 你只讨论 Tencent, Google, Meta, Microsoft 这四家公司的财务数据与业务模式。
3. 任何超出以上范围的问题（如其他行业、其他公司、日常闲聊、编程问题等），你必须礼貌但坚定地拒绝回答，并引导用户回到本作业的讨论范围。
4. 回答时请充分运用护城河理论 (Moat Theory)、DCF 折现逻辑、杜邦分析法等高级投资框架，以体现专业深度。

【四家公司最新财务指标数据（已静态化，请以此为准，不要编造）】
{FINANCIAL_CONTEXT}

【输出风格】
- 用中文回答，行文兼顾专业性与可读性。
- 涉及具体指标对比时，务必引用上方真实数据。
"""


def get_deepseek_client():
    try:
        api_key = st.secrets["DEEPSEEK_API_KEY"]
        return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    except Exception:
        return None


def call_deepseek(messages, temperature=0.7, max_tokens=2000):
    if st.session_state.question_count >= MAX_QUESTIONS:
        return t("limit_api")

    client = get_deepseek_client()
    if not client:
        return "无法读取 API Key，请在 `.streamlit/secrets.toml` 中配置 `DEEPSEEK_API_KEY`。"

    try:
        system_msg = messages[0]
        conversation = messages[1:]
        max_ctx = SLIDING_WINDOW * 2
        if len(conversation) > max_ctx:
            conversation = conversation[-max_ctx:]
        trimmed = [system_msg] + conversation

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=trimmed,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )
        st.session_state.question_count += 1
        return response.choices[0].message.content
    except Exception as e:
        return f"API 调用出错: {e}"


# ============================================================
# 4. 双轨输出 Prompt 定义
# ============================================================
TAB_PROMPTS = {
    "tab1": {
        "title": "行业概览 (Industry Overview)",
        "prompt": """请针对 Tech Internet 行业，严格按以下结构和格式生成完整输出。所有内容用中文，数据引用需具体。

---
## Report Body

### 1. 行业定义
用**一句话**（30字以内）精准定义科技互联网行业。
紧接着用 bullet points 补充 **3 条**关键特征（每条 ≤ 15 字，要具体，不要空泛）：
-
-
-

### 2. 产业链位置
直接输出一个 **Markdown 表格**，对比四家公司。列名为：

| 公司 | 产业链层级 | 核心业务入口 | 主要变现模式 |
|------|-----------|------------|------------|

（填入 Tencent, Google, Meta, Microsoft，各行内容简洁有力）

### 3. 市场规模
用**一句话**包含：① 当前全球市场体量（用具体数字/美元规模） ② 未来 3-5 年 CAGR 预测。
然后用 bullet points 给出 **3 个关键细分市场**（每条包含：细分名 + 规模/增速数据，≤ 20 字）：
-
-
-

### 4. 增长趋势
用 bullet points 列出 **4 个核心驱动力**（每条 ≤ 20 字，需点明具体案例或数据支撑）：
-
-
-
-

---
## Presentation 准备

按 PPT 页数组织。每页 2-3 条要点，直接可复制到 PPT 演讲者备注。
格式要求：纯 bullet points，不写任何括号内的动作描述词（如"开场""过渡""指向"等）。

**PPT 第 1 页 — 行业定义**
-
-

**PPT 第 2 页 — 产业链位置**
-
-

**PPT 第 3 页 — 市场规模**
（提示：结合市场规模趋势折线图讲解）
-
-

**PPT 第 4 页 — 增长趋势**
-
-
"""
    },

    "tab2": {
        "title": "行业核心财务特征 (Core Financial Characteristics)",
        "prompt": """请针对 Tech Internet 行业，严格按以下结构和格式生成完整输出。所有内容用中文，必须引用四家公司真实数据。

---
## Report Body

### 1. 毛利率对比 (Gross Margin)
直接输出一个 **Markdown 表格**，对比四家公司毛利率及驱动因素：

| 公司 | 毛利率 | 核心驱动因素（1行以内） |
|------|--------|----------------------|

（填入 Tencent, Google, Meta, Microsoft 的真实数据，驱动因素要具体，不超过 15 字）

### 2. 费用结构 (Expense Structure)
用 bullet points 说明 **4 家公司整体费用结构特征**（R&D-driven vs Marketing-driven），每条 ≤ 20 字，需点名公司：
-
-
-

### 3. 盈利能力 (Profitability)
直接输出一个 **Markdown 表格**，对比四家公司关键盈利指标：

| 公司 | Net Margin | ROE | 核心盈利逻辑（1行以内） |
|------|-----------|-----|----------------------|

（必须引用真实数据，盈利逻辑具体，不超过 12 字）

### 4. 资产负债特征 (Asset & Debt)
用 bullet points 列出该行业整体资产负债状况，**3 条**（每条 ≤ 20 字，包含具体数据或公司名）：
-
-
-

---
## Presentation 准备

按 PPT 页数组织，每页 2-3 条要点，直接可复制到 PPT 演讲者备注。
格式：纯 bullet points，不写括号内动作描述词（如"过渡""强调""指向"等）。

**PPT 第 1 页 — 毛利率对比**
-
-

**PPT 第 2 页 — 费用结构**
-
-

**PPT 第 3 页 — 盈利能力**
（提示：结合雷达图讲解 ROE 差异）
-
-

**PPT 第 4 页 — 资产负债**
-
-
"""
    },

    "tab3": {
        "title": "四家公司财务横向比对 (Financial Comparison)",
        "prompt": """请对 Tencent, Google, Meta, Microsoft 进行财务横向比对，严格按以下结构和格式生成完整输出。所有内容用中文，必须引用四家公司真实数据。

---
## Report Body

### 1. 核心指标对比
直接输出一个 **Markdown 表格**，对比四家公司核心财务指标：

| 公司 | Gross Margin | Net Margin | ROE | Debt-to-Asset |
|------|-------------|------------|-----|---------------|

（填入 Tencent, Google, Meta, Microsoft 的真实数据，用百分比格式）

### 2. 差异原因分析
直接输出一个 **Markdown 表格**，从三个维度对比差异原因：

| 维度 | Tencent | Google | Meta | Microsoft |
|------|---------|--------|------|-----------|
| Scale（规模效应） | | | | |
| Positioning（市场定位） | | | | |
| Business Model（商业模式） | | | | |

（每个单元格内容简洁有力，≤ 15 字）

### 3. 核心差异总结
用 bullet points 列出 **4-5 条**最关键的差异洞察（每条 ≤ 25 字，需引用具体数据或公司名）：
-
-
-
-

---
## Presentation 准备

按 PPT 页数组织，每页 2-3 条要点，直接可复制到 PPT 演讲者备注。
格式：纯 bullet points，不写括号内动作描述词（如"开场""过渡""转向""指向"等）。
核心叙事线：不是谁好谁坏，而是商业模式的区别（ToB vs ToC）。

**PPT 第 1 页 — 核心指标一览**
-
-
-

**PPT 第 2 页 — 差异根源：规模与定位**
-
-
-

**PPT 第 3 页 — 商业模式对比：ToB vs ToC**
（提示：结合雷达图讲解 ROE 和 Debt-to-Asset 差异）
-
-
-

**PPT 第 4 页 — 关键结论**
-
-
-
"""
    },
    "tab4": {
        "title": "行业展望与核心投资关注点 (Industry Outlook)",
        "prompt": """请针对 Tech Internet 行业未来展望，严格按以下结构和格式生成完整输出。所有内容用中文，必须引用四家公司真实数据。数据不能单独罗列，必须嵌入分析文字中一起呈现。

---
## Report Body

### 1. 机遇分析
用 bullet points 列出 **3-4 个核心机遇**（每条需包含具体数据或案例，数据与分析融合在同一句话中，≤ 30 字）：
-
-
-

### 2. 挑战与风险
用 bullet points 列出 **3-4 个核心风险**（每条需点明影响哪家公司及具体风险点，≤ 30 字）：
-
-
-

### 3. 投资关键财务指标
直接输出一个 **Markdown 表格**，列出 3-5 个最值得关注的财务指标，并标注四家公司的表现：

| 关键指标 | Tencent | Google | Meta | Microsoft | 关注理由（≤ 12 字） |
|---------|---------|--------|------|-----------|------------------|

### 4. 最终投资结论
用 bullet points 给出 **3-4 条**结论性观点（每条需包含具体公司名和数据支撑，≤ 30 字）：
-
-
-

---
## Presentation 准备

按 PPT 页数组织，每页 2-3 条要点，直接可复制到 PPT 演讲者备注。
格式：纯 bullet points，不写括号内动作描述词（如"开场""过渡""转向""升华"等）。
核心叙事线：研发转化率 + 自由现金流是应对未来的底气。

**PPT 第 1 页 — 行业机遇**
-
-
-

**PPT 第 2 页 — 风险与挑战**
-
-
-

**PPT 第 3 页 — 关键指标对比**
（提示：结合数据表讲解各公司差异）
-
-
-

**PPT 第 4 页 — 投资结论与展望**
-
-
-
"""
    }
}


def generate_dual_track(tab_key):
    if tab_key in st.session_state.dual_track_cache:
        return st.session_state.dual_track_cache[tab_key]
    prompt_info = TAB_PROMPTS[tab_key]
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_info["prompt"]}
    ]
    result = call_deepseek(messages, temperature=0.6, max_tokens=2500)
    st.session_state.dual_track_cache[tab_key] = result
    return result


# ============================================================
# 5. 交互式教练聊天引擎
# ============================================================

def handle_tab_chat(tab_key, tab_label, user_input):
    if st.session_state.question_count >= MAX_QUESTIONS:
        return t("limit_api")

    history = st.session_state.chat_histories[tab_key]
    history.append({"role": "user", "content": user_input})

    tab_context = f"\n\n【当前 Tab 上下文】用户正在查看：【{tab_label}】。请基于该 Tab 内容范围回答。"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + tab_context}
    ] + history

    response = call_deepseek(messages, temperature=0.7, max_tokens=1500)
    history.append({"role": "assistant", "content": response})

    if len(history) > SLIDING_WINDOW * 2:
        st.session_state.chat_histories[tab_key] = history[-(SLIDING_WINDOW * 2):]

    return response


def render_chat_section(tab_key, tab_label):
    st.markdown('<div class="chat-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"**{t('coach')}**")

    history = st.session_state.chat_histories[tab_key]
    if history:
        for msg in history:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-msg">{msg["content"]}</div>', unsafe_allow_html=True)

    if st.session_state.question_count < MAX_QUESTIONS:
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "提问", placeholder=t("coach_ph").format(label=tab_label),
                key=f"input_{tab_key}", label_visibility="collapsed"
            )
        with col_btn:
            send_clicked = st.button(t("send"), key=f"send_{tab_key}", type="primary",
                                     use_container_width=True)

        if send_clicked and user_input:
            with st.spinner(t("thinking")):
                handle_tab_chat(tab_key, tab_label, user_input)
            st.rerun()
    else:
        st.warning(t("limit_warn"))

    remaining = MAX_QUESTIONS - st.session_state.question_count
    st.markdown(f'<span class="quota-badge">{t("remaining").format(r=remaining, t=MAX_QUESTIONS)}</span>',
                unsafe_allow_html=True)


# ============================================================
# 6. Red Team Q&A 模拟器
# ============================================================

RED_TEAM_PROMPT = """你现在是一位极其苛刻的大学投资课教授。学生做了 Tech Internet 行业财报分析报告（Tencent, Google, Meta, Microsoft）。

请模拟课堂答辩场景，生成 **3 个最刁钻、最可能被问到的提问**。

严格按以下格式输出（重复 3 次）：

---
### 模拟提问 1
（刁钻问题）

**标准防守话术：**
（逻辑严密、口语化、可直接背诵的回答，约 200 字）

**防守数据索引：**
（告诉学生：回答时应立刻翻到哪个 Tab、看哪张雷达图或折线图来佐证论点）

---
### 模拟提问 2
...

---
### 模拟提问 3
...

【指导原则】
- 问题聚焦数据矛盾、逻辑漏洞、或学生可能忽视的细节
- 防守话术要像课堂上脱口而出的自然回答
- 数据索引精确到 Tab 编号和图表类型（雷达图/折线图/数据表）
"""


# ============================================================
# 7. 页面渲染
# ============================================================

# --- Title + Language Toggle ---
col_title, col_lang = st.columns([6, 1])
with col_title:
    st.markdown(f'<div class="page-title">{t("title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("subtitle")}</div>', unsafe_allow_html=True)
with col_lang:
    lang_choice = st.selectbox(
        "Language", ["中文", "English"],
        index=0 if st.session_state.lang == "中文" else 1,
        label_visibility="collapsed"
    )
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()


# --- 快速数据概览 ---
st.markdown(f'<div class="section-title">{t("metrics_header")}</div>', unsafe_allow_html=True)
cols = st.columns(4)
for i, (company, data) in enumerate(metrics.items()):
    with cols[i]:
        st.metric(
            label=company,
            value=f"{data['Gross Margin']*100:.1f}%",
            delta=f"{t('net_margin')}: {data['Net Margin']*100:.1f}%"
        )
        st.caption(f"ROE: {data['ROE']*100:.1f}% · {t('da_ratio')}: {data['Debt-to-Asset Ratio']*100:.1f}%")
st.divider()


# ============================================================
# 8. 四大核心 Tab（自定义全宽导航）
# ============================================================
_TAB_KEYS = ["tab1", "tab2", "tab3", "tab4"]
_TAB_LABEL_KEYS = ["tab1", "tab2", "tab3", "tab4"]

nav_cols = st.columns(4)
for i, key in enumerate(_TAB_KEYS):
    with nav_cols[i]:
        active_cls = "active" if st.session_state.active_tab == key else ""
        if st.button(t(_TAB_LABEL_KEYS[i]), key=f"nav_{key}", use_container_width=True):
            st.session_state.active_tab = key
            st.rerun()

# Inject active styling via HTML overlay
_active_idx = _TAB_KEYS.index(st.session_state.active_tab)
st.markdown(f"""
<style>
    div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button {{
        background: rgba(74,158,255,0.06) !important;
        border: 1.5px solid rgba(74,158,255,0.25) !important;
        color: #b0b0c8 !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        padding: 0.75rem 0.5rem !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 3rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button:hover {{
        background: rgba(74,158,255,0.12) !important;
        color: #e0e0e0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) > div:nth-child({_active_idx + 1}) button {{
        background: rgba(74,158,255,0.18) !important;
        color: #4A9EFF !important;
        border-color: #4A9EFF !important;
        box-shadow: 0 0 12px rgba(74,158,255,0.15) !important;
    }}
</style>
""", unsafe_allow_html=True)

st.divider()

# ── Tab Content Rendering ──
_active = st.session_state.active_tab

if _active == "tab1":
    st.markdown(f'<div class="section-title">{t("tab1_sec")}</div>', unsafe_allow_html=True)
    st.markdown(t("tab1_points"))

    st.markdown(f'<div class="subsection-header">{t("tab1_chart")}</div>', unsafe_allow_html=True)
    st.plotly_chart(market_fig, use_container_width=True)

    if st.button(t("gen_btn"), key="gen_tab1", type="primary"):
        with st.spinner(t("gen_spin1")):
            generate_dual_track("tab1")

    if "tab1" in st.session_state.dual_track_cache:
        st.markdown(st.session_state.dual_track_cache["tab1"])
    else:
        with st.expander(t("hint_title")):
            st.info(t("hint_tab1"))

    render_chat_section("tab1", t("tab1"))

elif _active == "tab2":
    st.markdown(f'<div class="section-title">{t("tab2_sec")}</div>', unsafe_allow_html=True)
    st.markdown(t("tab2_points"))

    st.markdown(f'<div class="subsection-header">{t("tab2_chart")}</div>', unsafe_allow_html=True)
    gm_cols = st.columns(4)
    for i, (company, data) in enumerate(metrics.items()):
        with gm_cols[i]:
            st.metric(label=company, value=f"{data['Gross Margin']*100:.1f}%", delta=t("gross_margin"))

    if st.button(t("gen_btn"), key="gen_tab2", type="primary"):
        with st.spinner(t("gen_spin2")):
            generate_dual_track("tab2")

    if "tab2" in st.session_state.dual_track_cache:
        st.markdown(st.session_state.dual_track_cache["tab2"])
    else:
        with st.expander(t("hint_title")):
            st.info(t("hint_default"))

    render_chat_section("tab2", t("tab2"))

elif _active == "tab3":
    st.markdown(f'<div class="section-title">{t("tab3_sec")}</div>', unsafe_allow_html=True)
    st.markdown(t("tab3_points"))

    st.markdown(f'<div class="subsection-header">{t("tab3_radar")}</div>', unsafe_allow_html=True)
    st.plotly_chart(radar_fig, use_container_width=True)

    st.markdown(f'<div class="subsection-header">{t("tab3_table")}</div>', unsafe_allow_html=True)
    df = pd.DataFrame(metrics).T
    df.columns = ["Gross Margin", "Net Margin", "ROE", "Debt-to-Asset"]
    table_html = "<table style='border-collapse:collapse;width:100%;font-family:Inter,sans-serif;font-size:0.95rem;'>"
    table_html += "<thead><tr>"
    table_html += f"<th style='background:#16213e;color:#e0e0e0;font-weight:700;padding:0.75rem 1.2rem;text-align:left;font-size:0.88rem;letter-spacing:0.03em;border-bottom:2px solid #4A9EFF;'>{t('tab3_col_company')}</th>"
    for col in df.columns:
        table_html += f"<th style='background:#16213e;color:#e0e0e0;font-weight:700;padding:0.75rem 1.2rem;text-align:center;font-size:0.88rem;letter-spacing:0.03em;border-bottom:2px solid #4A9EFF;'>{col}</th>"
    table_html += "</tr></thead><tbody>"
    for company, row in df.iterrows():
        table_html += "<tr>"
        table_html += f"<td style='padding:0.7rem 1.2rem;font-weight:700;color:#f0f0f0;border-bottom:1px solid rgba(255,255,255,0.08);white-space:nowrap;'>{company}</td>"
        for val in row:
            table_html += f"<td style='padding:0.7rem 1.2rem;text-align:center;color:#d0d0d0;font-weight:500;border-bottom:1px solid rgba(255,255,255,0.08);font-variant-numeric:tabular-nums;'>{val*100:.1f}%</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

    if st.button(t("gen_btn"), key="gen_tab3", type="primary"):
        with st.spinner(t("gen_spin3")):
            generate_dual_track("tab3")

    if "tab3" in st.session_state.dual_track_cache:
        st.markdown(st.session_state.dual_track_cache["tab3"])
    else:
        with st.expander(t("hint_title")):
            st.info(t("hint_default"))

    render_chat_section("tab3", t("tab3"))

elif _active == "tab4":
    st.markdown(f'<div class="section-title">{t("tab4_sec")}</div>', unsafe_allow_html=True)
    st.markdown(t("tab4_points"))

    if st.button(t("gen_btn"), key="gen_tab4", type="primary"):
        with st.spinner(t("gen_spin4")):
            generate_dual_track("tab4")

    if "tab4" in st.session_state.dual_track_cache:
        st.markdown(st.session_state.dual_track_cache["tab4"])
    else:
        with st.expander(t("hint_title")):
            st.info(t("hint_default"))

    render_chat_section("tab4", t("tab4"))


# ============================================================
# 9. Red Team Q&A 模拟器
# ============================================================
st.divider()
st.markdown('<div id="red-team-anchor"></div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-title red-team">{t("redteam_sec")}</div>', unsafe_allow_html=True)
st.markdown(t("redteam_desc"))

col_btn, col_info = st.columns([1, 3])
with col_btn:
    red_team_clicked = st.button(t("redteam_btn"), type="primary", use_container_width=True)
with col_info:
    remaining = MAX_QUESTIONS - st.session_state.question_count
    if remaining > 0:
        st.caption(t("redteam_rem").format(r=remaining, t=MAX_QUESTIONS))
    else:
        st.error(t("redteam_max"))

if red_team_clicked:
    if st.session_state.question_count >= MAX_QUESTIONS:
        st.warning(t("limit_warn"))
    else:
        with st.spinner(t("redteam_spin")):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": RED_TEAM_PROMPT}
            ]
            result = call_deepseek(messages, temperature=0.8, max_tokens=3000)
            st.session_state.red_team_cache = result
        st.rerun()

if st.session_state.red_team_cache:
    st.markdown(st.session_state.red_team_cache)


# ============================================================
# 10. Footer
# ============================================================
st.divider()
st.markdown(f"""
<div style="text-align:center; color:#666; font-size:0.8rem; padding: 1rem 0;">
    {t("footer1")}<br>
    {t("footer2")}
</div>
""", unsafe_allow_html=True)
