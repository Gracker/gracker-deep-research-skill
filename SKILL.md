---
name: gracker-deep-research
description: Gracker Deep Research Skill · 三阶段调研法（本地扫描 → 探索落盘 → 利用写作）。Phase 0 扫描本地优质资料，Phase 1 全力搜索并落盘，Phase 2 断网只读本地文件写报告。触发词：「深度调研 XXX」/ 「Gracker Research XXX」/ 「dg XXX」。
---

# Gracker Deep Research Skill

> **核心理念**：三阶段解耦 —— 本地扫描（已有知识激活）→ 探索落盘（互联网 → 本地文件）→ 利用写作（断网读本地文件）。
>
> 参考：2026 年两阶段深度研究范式（探索-利用解耦），扩展为三阶段，优先激活本地资产。

---

## ⚙️ 配置

```yaml
local_vault_path: /Users/gracker/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian
workspace_path: /Users/gracker/.openclaw/workspace
research_output_dir: {local_vault_path}/调研/
```

**Portability**：路径不存在时 Phase 0 静默跳过，不阻断全流程。其他用户改这三个变量即可。

---

## 术语

| 术语 | 含义 |
|------|------|
| **Phase 0 scan** | 扫描本地 Vault 相关文件，生成覆盖度评估 |
| **research dump** | 研究员对每个子问题的原始发现，写入本地 .md 文件 |
| **local context** | Phase 0 产出的本地知识摘要 |
| **master research** | dump + local context 汇总后的单一文件 |

---

## 三阶段总览

```
用户输入 (题目)
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│  PHASE 0: 本地扫描 —— 激活已有知识资产                      │
│  目标: 在规划子问题之前，先摸清本地有什么                    │
│  策略: 扫描结果影响子问题范围（已有高覆盖 → 缩小搜索范围）    │
├──────────────────────────────────────────────────────────┤
│  PHASE 1: 探索 —— 调研 + 落盘                             │
│  目标: 把互联网的零散知识全部沉淀成本地文件                   │
│  原则: 全力搜索，不漏信号，断网前完成所有网络访问             │
├──────────────────────────────────────────────────────────┤
│  PHASE 2: 利用 —— 读文件 + 写作                          │
│  目标: 基于本地干净文件进行高频迭代写作                       │
│  原则: 断网，只读本地文件                                   │
└──────────────────────────────────────────────────────────┘
```

---

## Phase 0: 本地文件扫描

**执行时机**：整个流程第一步，在规划任何子问题之前执行。

### 执行步骤

**Step 0a: 扫描目录**

对以下目录（存在才扫）执行 ripgrep 关键词扫描：

```
{local_vault_path}/Android-Internal-Wiki/
{local_vault_path}/DeepResearch/
{local_vault_path}/调研/
{local_vault_path}/awesome-ai-field-notes/
{local_vault_path}/X 文章/
{workspace_path}/MEMORY.md
{workspace_path}/memory/
```

关键词从 topic 提取 3-5 个核心概念。

```bash
# 示例
rg -l --max-count 10 "Android CLI|Android Agent|android agents" "{dir}/" --type md 2>/dev/null
```

**Step 0b: 读取高匹配文件**

对每个找到的文件，提取相关段落（最多 5 个最有价值的文件，每文件限制 100 行）：

```bash
rg -C 3 "{keyword}" "{file}" 2>/dev/null | head -100
```

**Step 0c: 写入 local context**

路径：`{research_output_dir}/{YYYY-MM-DD}-{slug}-研究材料/00-local-context.md`

格式：

```markdown
---
phase: 0
topic: {topic}
---

# Phase 0 · 本地知识扫描结果

## 扫描目录
- ✓ AIW: 扫描了 X 个文件，命中 {N}
- ✓ DeepResearch: 命中 {N}
- ✗ 调研/（目录不存在，静默跳过）
...

## 命中文件

### {文件名1}
- **路径**: {path}
- **相关段落**: `{rg 输出片段，限制 80 行}`
- **对本题的价值**: 高/中/低

...

## 覆盖度评估

| 子维度 | 本地覆盖度 | 本地来源 |
|--------|-----------|---------|
| {维度1} | 高/中/低 | {文件列表} |
| {维度2} | 高/中/低 | {文件列表} |

## 子问题范围调整

- **{子问题A}**：本地高覆盖 → 缩小搜索范围，补充最新动态
- **{子问题B}**：本地无覆盖 → 全文搜索
```

---

## Phase 1a: 规划子问题 + 创建目录

1. 读取 Phase 0 输出的 `00-local-context.md`
2. 结合 topic 拆解 2-4 个子问题，Phase 0 高覆盖的明确标注缩小范围
3. 创建目录：

```bash
DATE=$(date +%Y-%m-%d)
TOPIC_SLUG=$(echo "{topic}" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/-/g')
OUT_DIR="{research_output_dir}/${DATE}-${TOPIC_SLUG}-研究材料"
mkdir -p "${OUT_DIR}/references"
```

4. 回执用户：`收到，开始处理。本地扫描命中 X 个文件。Phase 0 发现 {A} 子问题本地高覆盖，聚焦缺失部分。`

---

## Phase 1b: 并行研究员写 research dump

**关键约束：研究员的全部网络访问（web_search + web_fetch）必须在写 dump 文件之前完成，不在写作阶段访问网络。**

### 子问题规划（主 session）

根据 topic 和 Phase 0 结果，拆解 2-4 个子问题，每个附搜索策略：

| 子问题 | 搜索关键词 | 偏好来源 |
|--------|-----------|---------|
| Android CLI 核心功能与架构 | android agents CLI SDK | cs.android.com / developer.android.com |
| Android Skills 机制与首批技能 | android skills SKILL.md agent | github.com/android |
| Android Knowledge Base | android knowledge base docs agent RAG | source.android.com |
| 对比分析：Google vs OpenClaw | google android agents vs openclaw skills | developer.android.com / github |

### Spawn 配置

每个子问题一个 researcher，同时 spawn，然后 `sessions_yield`：

```
runtime: subagent
mode: run
model: zai/glm-5-turbo
timeoutSeconds: 600
```

### Researcher Prompt（完整模板）

```
你是一个专业研究员。请针对以下子问题进行深度调研，并把发现写入本地文件。

## 研究问题
{sub_question}

## 搜索策略
{search_strategy}

## Phase 0 本地覆盖度标注
{从 00-local-context.md 提取该子问题的覆盖度行}
如果本地已有高覆盖：补充最新动态即可，不需要重复基础搜索。
如果本地无覆盖：全文搜索，不设限制。

## ⚠️ 核心执行原则
1. **调研阶段全力搜索**：所有 web_search + web_fetch 在写文件之前完成
2. **写文件阶段断网**：开始写 dump 文件时，不再访问网络
3. **一手资料优先**：源码 > 官方文档 > 论文 > 官方 Issue > 二手博客

## 搜索要求
- web_search 3-5 个不同角度的查询
- 至少 1 次专门搜源码/官方文档：`site:cs.android.com`、`site:developer.android.com`
- 精选 3-5 个最有价值的页面，用 web_fetch 抓取全文
- 交叉验证信息来源

## 输出要求：写入本地文件

**必须用 exec + python 写入文件，不在 prompt 里输出长文本。**

文件路径：`{OUT_DIR}/{sub_num}-{slug}-dump-{N}.md`

文件格式：
```markdown
---
source: research
sub_question: {sub_question}
researcher: researcher-{N}
phase: 1b
---

# 子问题: {sub_question}

## 核心发现（3-5 条）
- **{发现标题}**: {一句话描述} [来源: {source}]

## 详细分析

### {分析小节1}
{2-4 段详细分析，含内联引用 [source-n]}

### {分析小节2}
{...}

## 信息源
1. [{title}]({url}) — {一句话摘要} **[一手/二手]**
2. ...

## 质量自评
- 信息充分度: X/5
- 源可信度: X/5
- 一手资料占比: X/5
- 本地知识匹配度: 高/中/低
- 是否需要补充调研: 是/否（如是，说明缺什么）
```

## Phase 1c: 参考资料归档

研究员完成后，主 session 对所有 cite 的 URL 执行 web_fetch（未抓取过的），保存到：

```
{OUT_DIR}/references/{num}-{slug}.md
```

格式：
```markdown
---
source: {url}
title: {title}
fetched: {ISO timestamp}
research_topic: {topic}
sub_question: {sub_question}
---

{full content}
```

## Phase 1d: 缺口检查 + 编译 master-research

1. 读取所有 dump 文件，评估 `是否需要补充调研`
2. 如有缺口：主 session 直接补搜，不派新 researcher
3. 编译 master-research：

```bash
cat "{OUT_DIR}/00-local-context.md" \
    "{OUT_DIR}"/*-dump-*.md \
    > "{OUT_DIR}/master-research.md"
```

---

## Phase 2: 写作（断网模式）

**⚠️ 绝对约束：此阶段 agent 不得使用 web_search/web_fetch，只读本地文件。**

### Phase 2a: 验证

检查 `{OUT_DIR}/master-research.md` 存在且非空。不存在则报错，不继续写作。

### Phase 2b: 写作 Agent

**模型: openai-codex/gpt-5.4（强制，不可用其他模型）**

Spawn：
```
runtime: subagent
mode: run
model: openai-codex/gpt-5.4
timeoutSeconds: 900
```

Prompt：
```
你是一个资深技术分析师。请根据本地研究材料撰写深度调研报告。

## 报告主题
{topic}

## ⚠️ 断网约束（最高优先级）
本次写作阶段你不得使用 web_search、web_fetch 或任何联网工具。
你只能读取以下本地文件：
- {OUT_DIR}/master-research.md（必读）
- {OUT_DIR}/00-local-context.md（必读）
- {OUT_DIR}/references/*.md（按需读）

## 本地资产激活记录（Phase 0）
{从 00-local-context.md 提取覆盖度矩阵}
报告应区分：哪些是本地已有知识，哪些是本次新研究发现。

## 写作要求

### 格式
1. 标题: `# 深度调研：{topic}`
2. 元信息: 调研时间、耗时
3. 摘要: 200-300 字，概括核心结论
4. 正文: 按逻辑组织（不是子问题堆砌），段落间有过渡
5. 关键发现: 3-5 条，用加粗标注
6. 参考资料: 编号列表，标注 [一手] / [二手] / [本地: {path}]

### 质量标准
- ❌ 禁止堆砌搜索结果，要有分析综合
- ❌ 禁止无引用的断言
- ❌ 禁止"综上所述"空洞结尾
- ❌ 禁止仅以二手博客为论据
- ✅ 每个论点有 [n] 引用支撑
- ✅ 技术细节给出源码行号/文件路径
- ✅ 适当使用表格对比

### 语言
- 中文为主，技术术语保留英文
- 专业但不晦涩，有观点
- 字数: 3000-8000 字

## 输出
将报告写入：{research_output_dir}/{YYYY-MM-DD}-{slug}-深度调研.md
使用 exec + python（Obsidian iCloud 路径）写入。
```

---

## Phase 3: 交付

1. **报告路径**：`{research_output_dir}/{YYYY-MM-DD}-{slug}-深度调研.md`
2. **发送用户**：
   - 标题 + 摘要预览（前 5 行）
   - 全文
   - 附注：`已完成。报告共 X 字，Phase 0 命中 {N} 个本地文件，Phase 1 抓取 {Z} 个来源，参考资料 {M} 篇已归档。`
3. **记录到记忆**：

```
## [HH:MM] task | 深度调研·{topic}·已完成
- 规模: {small/medium/large}，耗时约 X 分钟
- Phase 0: 扫描 {X} 个目录，命中 {N} 个本地文件
- Phase 1: Y 个研究员落盘，Z 个来源
- Phase 2: GPT-5.4 断网写作
- 报告: Obsidian/调研/{filename}
```

---

## 一手资料优先原则

| 优先级 | 资料类型 |
|--------|----------|
| 1 | 源码（AOSP） |
| 2 | 官方文档 |
| 3 | 学术论文（arxiv） |
| 4 | 官方 Issue / CL / Release Notes |
| 5 | 官方博客 |
| — | 二手博客（仅作线索，必须追溯到一手） |

---

## 错误处理

| 场景 | 处理 |
|------|------|
| Phase 0 扫描目录不存在 | **静默跳过** |
| Phase 0 ripgrep 无结果 | 正常继续，输出"本地无命中" |
| 研究员超时 | 缩小范围重试 1 次 |
| GPT-5.4 不可用 | **立即通知用户，不降级，不继续** |
| 写文件到 Vault 失败 | 降级到 workspace tmp，通知用户 |

---

## 与旧版 deep-research skill 的差异

| 差异点 | 旧版 | 新版 |
|--------|------|------|
| Phase 0 本地扫描 | 无 | **优先执行，影响子问题规划** |
| 写作阶段网络 | 可能继续访问 | **断网，只读本地文件** |
| 研究员输出 | inline 文本 | **写入 .md dump 文件** |
| 参考资料 | 有归档但非强制 | **强制归档到 references/** |
| Portability | 无 | **路径可配置，扫描失败静默跳过** |
