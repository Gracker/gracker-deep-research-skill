---
name: gracker-deep-research
description: Gracker Deep Research Skill · 两阶段调研法（探索 → 利用解耦）。Phase 1 全力搜索并落盘，Phase 2 断网只读本地文件写报告。触发词：「深度调研 XXX」/ 「Gracker Research XXX」/ 「dg XXX」。
---

# Gracker Deep Research Skill

> **核心理念**：探索（搜索 + 落盘）与 利用（读文件 + 写作）解耦。调研阶段全力吃信息写入本地，写作阶段断网只读本地文件。
>
> 参考：2026 年两阶段深度研究范式 —— 网络读写用于调研与规划，本地文件用于内循环迭代。

## 术语

| 术语 | 含义 |
|------|------|
| **research dump** | 研究员对每个子问题的原始发现输出，含核心发现 + 详细分析 + 信息源 |
| **local context** | 本地知识摘要（Phase 1b 的产出） |
| **master research** | 所有 dump 汇总编译后的单一研究文件（Phase 2a 产出） |

---

## 路径定义

```
Obsidian 根目录: /Users/gracker/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian
调研输出目录:    {Obsidian}/调研/
报告路径:        {调研}/{YYYY-MM-DD}-{topic-slug}-深度调研.md
研究材料目录:     {调研}/{YYYY-MM-DD}-{topic-slug}-研究材料/
  ├── 00-local-context.md          # 本地知识摘要
  ├── 01-{slug}-dump-1.md         # 子问题1 的原始研究
  ├── 02-{slug}-dump-2.md         # 子问题2 的原始研究
  ├── ...
  ├── master-research.md           # 汇总后的研究文件（写入报告的原材料）
  └── references/                  # 参考资料全文归档
      ├── 01-{source-slug}.md
      ├── 02-{source-slug}.md
      └── ...
```

---

## 两阶段总览

```
用户输入 (题目)
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│  PHASE 1: 探索 —— 调研 + 落盘                             │
│  目标: 把互联网的零散知识全部沉淀成本地文件                   │
│  原则: 全力搜索，不漏信号                                   │
├──────────────────────────────────────────────────────────┤
│  Phase 0: 理解题目 + 评估规模                              │
│  Phase 1a: 规划子问题 + 创建目录                            │
│  Phase 1b: 本地知识搜索 (memory + Obsidian)                │
│  Phase 1c: 并行研究员写 research dump 到文件                 │
│  Phase 1d: 缺口检查 + 补充搜索（可选）                       │
├──────────────────────────────────────────────────────────┤
│  PHASE 2: 利用 —— 读文件 + 写作                            │
│  目标: 基于本地干净文件进行高频迭代写作                       │
│  原则: 断网，只读本地文件                                   │
├──────────────────────────────────────────────────────────┤
│  Phase 2a: 编译 master-research.md                         │
│  Phase 2b: 写作 agent 只读本地文件产出报告                   │
│  Phase 3: 交付 (Obsidian + 通知 + 记忆)                    │
└──────────────────────────────────────────────────────────┘
```

---

## Phase 0: 理解题目 + 评估规模

1. 解析题目，判断是否清晰。模糊则问一个澄清问题。
2. 评估规模：

| 规模 |研究员数| 预估耗时 | 典型场景 |
|------|--------|----------|----------|
| Small | 2 | ~20min | 单一技术/概念 |
| Medium | 3 | ~35min | 对比分析/多面话题 |
| Large | 4 | ~50min | 领域全景/战略报告 |

3. 回执用户：`收到，开始处理。预估 X 分钟，Y 个方向并行调研（两阶段：调研落盘 → 断网写作）。`

---

## Phase 1a: 规划子问题 + 创建目录

1. 根据主题拆解 2-4 个子问题，每个附搜索策略（关键词 + 偏好来源）
2. 创建目录结构：

```bash
TOPIC_SLUG=$(echo "{topic}" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/-/g' | sed 's/-\+/-/g' | sed 's/^-\|-$//g')
DATE=$(date +%Y-%m-%d)
mkdir -p "{调研输出目录}/{DATE}-{TOPIC_SLUG}-研究材料/references"
```

---

## Phase 1b: 本地知识搜索

**在派出研究员之前必须执行**，避免研究员从零开始搜索已有知识。

1. `memory_search`：用 3-5 个子问题相关语义查询
2. `rg -l`：Obsidian 关键词匹配（每个子问题核心词，最多 20 个文件）
3. `read`：对高匹配文件精读相关段落（最多 3-5 个文件）
4. 编译 `00-local-context.md`：

```markdown
# 本地知识摘要

## 子问题 1: {title}
- 已有积累: {从 memory/Obsidian 提炼}
- 相关文件: {path} - {摘要}
- 覆盖度评估: 高/中/低

## 子问题 2: ...
```

---

## Phase 1c: 并行研究员写 research dump 到文件

### 研究员执行逻辑（不同于旧版）

旧版：研究员输出结构化文本 → 直接拼进 writer prompt  
**新版**：研究员把发现写入 `{slug}-dump-N.md` 文件，**不输出长文本 inline**

### 研究员 Prompt（Phase 1c）

```
你是一个专业研究员。请针对以下子问题进行深度调研，并把发现写入本地文件。

## 研究问题
{sub_question}

## 搜索策略
{search_strategy}

## 已有本地知识
{local_context_for_this_sub_question}

⚠️ 这些来自本地知识库，是你的基础，不是你的终点。用最新搜索结果补充、纠正、深化。

## 执行要求

1. **一手资料优先**：
   - `site:cs.android.com {keyword}`（Android 源码）
   - `site:developer.android.com {keyword}`（官方文档）
   - `site:arxiv.org {keyword}`（论文）
   - `repo:AOSP/{repo} {keyword}`（GitHub AOSP）
2. 使用 web_search 搜索 3-5 个不同角度的查询
3. 精选 3-5 个最有价值的页面，用 web_fetch 抓取全文
4. 交叉验证信息来源

## 输出要求：写入本地文件

**必须使用 exec + python 写入文件**，文件路径：
```
{Obsidian 调研目录}/{YYYY-MM-DD}-{slug}-研究材料/0{sub_num}-{slug}-dump-{N}.md
```

文件格式：
```markdown
---
source: research
sub_question: {sub_question}
researcher: {researcher_id}
phase: 1c
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
- 是否需要补充调研: 是/否

## 写入参考资料（如有）
对于每个重要信息源，用 exec + python 保存到：
`{研究材料目录}/references/{num}-{slug}.md`

格式：
```markdown
---
source: {url}
title: {title}
fetched: {ISO timestamp}
research_topic: {topic}
sub_question: {sub_question}
---

{full content from web_fetch}
```
```

### Spawn 配置

- `runtime: subagent`
- `mode: run`
- `model: zai/glm-5-turbo`
- `timeoutSeconds: 600`
- **所有研究员同时 spawn，然后 sessions_yield 等待**

---

## Phase 1d: 缺口检查 + 补充搜索

收到所有 dump 后，主 session 执行：

1. 读取每个 dump 文件，评估 `质量自评` 字段
2. 如果任何子问题的**信息充分度 < 4 或 需要补充调研 = 是**：
   - 直接主 session 做针对性搜索补充
   - 将补充内容追加到对应 dump 文件
3. 执行参考资料的 web_fetch 归档（如 Phase 1c 未完成）
4. 编译 `master-research.md`：

```bash
# 拼接所有 dump + local-context → master-research.md
cat "{研究材料目录}/00-local-context.md" \
    "{研究材料目录}"/*-dump-*.md \
    > "{研究材料目录}/master-research.md"
```

---

## Phase 2: 写作（断网模式）

**核心约束：此阶段 agent 不使用 web_search/web_fetch，只读本地文件。**

### Phase 2a: 编译 master-research.md

（已在 Phase 1d 末尾完成）

验证文件存在且内容完整。

### Phase 2b: 写作 Agent

**模型: openai-codex/gpt-5.4（强制，不可用其他模型）**

如果 GPT-5.4 不可用，立即通知用户，不降级。

**Prompt 模板：**

```
你是一个资深技术分析师。请根据本地研究材料撰写深度调研报告。

## 报告主题
{topic}

## 研究材料（来自本地文件，已脱网）
请读取以下文件：
- {研究材料目录}/master-research.md
- {研究材料目录}/00-local-context.md

## 写作要求

### 格式
1. 标题: `# 深度调研：{topic}`
2. 元信息: 调研时间、耗时、规模
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
- ✅ 本地知识与新发现融合

### 语言
- 中文为主，技术术语保留英文
- 专业但不晦涩，有观点
- 字数: 3000-8000 字
```

### 写入报告

报告写入：`{调研输出目录}/{YYYY-MM-DD}-{topic-slug}-深度调研.md`

使用 exec + python（Obsidian iCloud 路径）。

---

## Phase 3: 交付

1. **报告已保存到** Obsidian/调研/
2. **发送给用户**：
   - 标题 + 摘要预览（前 5 行）
   - 全文
   - 附注：`已完成。报告共 X 字，引用 X 个来源（本地 X + 网络 X），参考资料 X 篇已归档。`
3. **记录到记忆**：

```
## [HH:MM] task | 深度调研·{topic}·已完成
- 规模: {small/medium/large}，耗时约 X 分钟
- 两阶段: Y 个研究员落盘 → GPT-5.4 断网写作
- 本地命中: Z 篇相关文档
- 报告: Obsidian/调研/{filename}
- 参考资料: X 篇已归档
```

---

## 一手资料优先原则（不变）

| 优先级 | 资料类型 |
|--------|----------|
| 1 | 源码（AOSP cs.android.com / GitHub） |
| 2 | 官方文档（source.android.com / developer.android.com） |
| 3 | 学术论文（arxiv / ACM / IEEE） |
| 4 | 官方 Issue / CL / Release Notes |
| 5 | 官方博客 |
| — | 二手博客（仅作线索，必须追溯到一手） |

---

## 错误处理

| 场景 | 处理 |
|------|------|
| 研究员超时 | 缩小范围重试 1 次 |
| 研究员结果缺口大 | 主 session 补搜，不通知用户（静默补位） |
| GPT-5.4 不可用 | **立即通知用户，不降级，不继续** |
| web_fetch 失败 | 跳过该源，标注 `[抓取失败]` |
| 写文件到 iCloud 失败 | 降级到 workspace tmp 路径，通知用户 |

---

## 与旧版 deep-research skill 的差异

| 差异点 | 旧版 | 新版 |
|--------|------|------|
| 研究员输出 | 结构化文本 inline | 写入本地 .md 文件 |
| 写作素材传递 | inline 拼接 | 只读本地文件 |
| 写作阶段网络 | 可能继续访问网络 | **断网，只读本地** |
| 调研→写作边界 | 模糊交织 | **清晰解耦** |
| 参考资料 | 有归档但非强制 | **强制归档到 references/** |
| 确定性 | 同一任务多次运行结果可能不同 | **本地文件=时间静止快照，结果确定** |
