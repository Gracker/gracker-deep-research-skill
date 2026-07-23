---
name: gracker-deep-research
description: Gracker Deep Research Skill · 三阶段调研法（本地扫描 → 探索落盘 → 利用写作）。Phase 0 扫描本地优质资料，Phase 1 全力搜索并落盘，Phase 2 断网只读本地文件写报告 + Gracker 写作四层质检。触发词：「深度调研 XXX」/ 「Gracker Research XXX」/ 「dg XXX」。
---

# Gracker Deep Research Skill

> **核心理念**：三阶段解耦 —— 本地扫描（已有知识激活）→ 探索落盘（互联网 → 本地文件）→ 利用写作（断网读本地文件）。
>
> **质检标准**：Phase 2 报告必须通过 Gracker 写作四层质检，否则触发 rewrite。
>
> **可选配套 skill**：如果运行环境安装了 `gracker-writing`，优先读取其 `SKILL.md` 作为完整文风规范；否则使用本文内置的质检摘要。

---

## ⚙️ 配置

```yaml
local_vault_path: null        # 可选：本地知识库、笔记库或资料库路径；未配置则跳过本地资料扫描
workspace_path: .             # 当前项目或 AI 运行时工作目录
research_output_dir: ./research
writing_skill_path: null      # 可选：gracker-writing/SKILL.md 的本地路径
```

**Portability**：所有路径都必须由当前用户或运行时提供。路径不存在时 Phase 0 静默跳过，不阻断全流程；不得假定存在特定 AI 运行时、特定 HOME 路径或特定模型。

---

## 术语

| 术语 | 含义 |
|------|------|
| **Phase 0 scan** | 扫描本地知识库相关文件，生成覆盖度评估 |
| **research dump** | 研究员对每个子问题的原始发现，写入本地 .md 文件 |
| **local context** | Phase 0 产出的本地知识摘要 |
| **master research** | dump + local context 汇总后的单一文件 |
| **四层质检** | L1 禁用词/硬伤 → L2 可读性 → L3 内容深度 → L4 活人感（Gracker 写作标准） |

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
│  PHASE 2: 利用 —— 读文件 + 写作 + 四层质检                  │
│  目标: 基于本地干净文件进行高频迭代写作                       │
│  原则: 断网，只读本地文件                                   │
│  质检: Gracker 写作四层标准，不通过则 rewrite              │
└──────────────────────────────────────────────────────────┘
```

---

## Phase 0: 本地文件扫描

**执行时机**：整个流程第一步，在规划任何子问题之前执行。

### 执行步骤

**Step 0a: 扫描目录**

对以下候选目录（存在才扫）执行关键词扫描。`local_vault_path` 未配置时，跳过所有本地知识库子目录；目录名应按用户实际资料库调整：

```
{local_vault_path}/DeepResearch/
{local_vault_path}/Research/
{local_vault_path}/调研/
{local_vault_path}/Notes/
{local_vault_path}/Articles/
{local_vault_path}/KnowledgeBase/
{workspace_path}/MEMORY.md
{workspace_path}/memory/
```

关键词从 topic 提取 3-5 个核心概念。

```bash
rg -l --max-count 10 --type md "keyword1|keyword2|keyword3" "{dir}/" 2>/dev/null
```

如果没有 `rg`，使用当前运行环境可用的等价全文搜索能力。

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
- ✓ 本地知识库 A: 扫描了 X 个文件，命中 {N}
- ✓ Research: 命中 {N}
- ✗ Notes/（目录不存在，静默跳过）
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
- **{子问题B}**：本地无覆盖 → 正文搜索
```

---

## Phase 1a: 规划子问题 + 创建目录

1. 读取 Phase 0 输出的 `00-local-context.md`
2. 结合 topic 拆解 2-4 个子问题，Phase 0 高覆盖的明确标注缩小范围
3. 创建目录：

```bash
DATE=$(date +%Y-%m-%d)
TOPIC_SLUG="{short-topic-slug}"  # 保留字母、数字和必要的中日韩字符；其他字符替换为 -
OUT_DIR="{research_output_dir}/${DATE}-${TOPIC_SLUG}-研究材料"
mkdir -p "${OUT_DIR}/references"
```

4. 回执用户：`收到，开始处理。本地扫描命中 X 个文件。Phase 0 发现 {A} 子问题本地高覆盖，聚焦缺失部分。`

---

## Phase 1b: 研究员写 research dump

**关键约束：研究员的全部网络访问必须在写 dump 文件之前完成，不在写作阶段访问网络。**

### 子问题规划（主 session）

根据 topic 和 Phase 0 结果，拆解 2-4 个子问题，每个附搜索策略：

| 子问题 | 搜索关键词 | 偏好来源 |
|--------|-----------|---------|
| {子问题A} | keyword1, keyword2 | 官方文档 / 官方源码 |
| {子问题B} | keyword3, keyword4 | 论文 / 标准 / 官方 Issue |
| ... | ... | ... |

### 执行方式

- 如果运行环境支持并行任务：每个子问题分配一个 researcher，同时执行，最后汇总 dump 文件。
- 如果运行环境不支持并行：在当前 session 按子问题顺序执行，仍然保持“一题一 dump 文件”。
- Skill 不指定模型。由当前 AI 运行时、用户配置或调用方策略选择模型和超时。

### Researcher Prompt

按子问题生成 researcher prompt 时，读取 `references/research-dump-template.md`。该模板定义了研究问题、搜索策略、断网写 dump、文件格式和质量自评要求。

## Phase 1c: 参考资料归档

研究员完成后，主 session 对所有 cite 的 URL 执行抓取或打开归档（未抓取过的），保存到：

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

**⚠️ 绝对约束：此阶段不得使用联网、搜索、抓取或浏览器工具，只读本地文件。**

### Phase 2a: 验证

检查 `{OUT_DIR}/master-research.md` 存在且非空。不存在则报错，不继续写作。

### Phase 2b: 写作执行

优先使用当前运行环境中最适合长文综合写作的能力；如果支持独立 writer 任务，可以单独启动 writer，但不得在 Skill 中固定模型、供应商或 runtime。

Prompt：读取 `references/writer-prompt-template.md`，用本次 topic、OUT_DIR 和 research_output_dir 替换模板变量。模板包含断网约束、报告结构、引用要求和写作质量标准。

---

## Phase 2c: 四层质检（Gracker 写作标准）

**执行时机**：报告草稿产出后、正式交付前。如质检不通过，触发 rewrite。

### 配套 skill

如果 `writing_skill_path` 指向可读文件，先读取该文件作为完整写作规范。常见值是 `gracker-writing/SKILL.md`。

如果没有配置或文件不存在，继续使用本 Skill 内置的四层质检摘要。不得自动下载或安装额外 skill，除非用户明确要求。

### 执行方式

主 session 读取报告草稿 + 可选 `gracker-writing` 规范，执行四层质检。

**不得使用联网工具**，全部基于本地文件内容判断。

详细质检规则和报告格式见 `references/quality-gate.md`。执行质检时先读取该文件，再结合可选 `gracker-writing` 规范检查报告草稿。

### rewrite 触发逻辑

| 质检结果 | 处理 |
|---------|------|
| L1 不通过 | **强制 rewrite**，明确列出 L1 命中的禁用词/硬伤位置，主 session 监督修复 |
| L2 不通过（开头未过） | **强制 rewrite** |
| L2 不通过（其他项） | 可选 rewrite，明确告知具体段落 |
| L3-1/3-2 不通过 | **强制 rewrite**，指出缺乏支撑的具体判断 |
| L4 整体不通过 | **强制 rewrite**，给出"哪个段落 AI 味重"的具体指引 |
| 全部通过 | 进入 Phase 3 交付 |

**rewrite 配置**：
- 执行方式：复用 Phase 2b 的写作执行方式；如果运行时支持独立 writer/rewrite 任务，可以单独执行
- 模型：不在 Skill 中指定，由运行时或用户配置决定
- prompt：在 Phase 2b writer prompt 基础上，附加质检报告，让 rewrite 专门修复标出的问题
- rewrite 完成后再执行一次 Phase 2c 质检，通过才能交付

---

## Phase 3: 交付

1. **报告路径**：`{research_output_dir}/{YYYY-MM-DD}-{slug}-深度调研.md`
2. **发送用户**：
   - 标题 + 摘要预览（前 5 行）
   - 全文
   - 附注：`已完成。报告共 X 字，Phase 0 命中 {N} 个本地文件，Phase 1 抓取 {Z} 个来源，Phase 2c 四层质检 [通过/强制 rewrite X 轮]，参考资料 {M} 篇已归档。`
3. **可选记录**：如果运行环境提供 memory / notes / task log，则追加一条简短记录；没有则跳过，不影响交付。

```
## [HH:MM] task | 深度调研·{topic}·已完成
- 规模: {small/medium/large}，耗时约 X 分钟
- Phase 0: 扫描 {X} 个目录，命中 {N} 个本地文件
- Phase 1: Y 个研究员落盘，Z 个来源
- Phase 2: 断网写作
- Phase 2c: 四层质检 [{通过/强制 rewrite X 轮}]
- 报告: {research_output_dir}/{filename}
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
| `writing_skill_path` 不存在 | 使用内置质检摘要继续；不自动联网安装 |
| 研究员超时 | 缩小范围重试 1 次 |
| 当前模型/运行时不适合长文综合 | 通知用户能力限制，给出已落盘研究材料和建议下一步 |
| Phase 2c 质检不通过 | 触发 rewrite，修复后再质检 |
| 写文件到 `research_output_dir` 失败 | 降级到 workspace tmp，通知用户 |

---

## 与旧版 deep-research skill 的差异

| 差异点 | 旧版 | 新版 |
|--------|------|------|
| Phase 0 本地扫描 | 无 | **优先执行，影响子问题规划** |
| 写作阶段网络 | 可能继续访问 | **断网，只读本地文件** |
| 研究员输出 | inline 文本 | **写入 .md dump 文件** |
| 参考资料 | 有归档但非强制 | **强制归档到 references/** |
| Portability | 无 | **路径可配置，扫描失败静默跳过** |
| Phase 2c 质检 | content-quality-gate 通用质检 | **Gracker 写作四层质检 + 文风禁区 + rewrite 触发** |
| 文风规范 | 无 | **15 类禁用词/句式，明确 rewrite 触发条件** |
| 写作规范依赖 | 无 | **可选读取 `gracker-writing`，缺失时使用内置摘要** |
