---
name: gracker-deep-research
description: Gracker Deep Research Skill · 深度技术调研的完整交付工作流：本地扫描 → 探索与证据落盘 → 断网写作与四层质检 → Gracker 风格真实成图 → Obsidian 归档。适用于「深度调研 XXX」「Gracker Research XXX」「dg XXX」以及需要把技术研究、引用、图片和过程材料一起沉淀到知识库的任务。
---

# Gracker Deep Research Skill

> **核心理念**：研究、写作、视觉化和发布四段解耦。先把网络证据完整落盘，再断网写作；报告通过质检后才生成 Gracker 风格图片，最后把报告、成图和过程材料作为一个可审计包发布到 Obsidian。
>
> **质检标准**：Phase 2 报告必须通过 Gracker 写作四层质检，否则触发 rewrite。
>
> **配套 skill**：如果运行环境安装了 `gracker-writing`，优先读取其 `SKILL.md` 作为完整文风规范。技术调研默认还需要安装 `gracker-diagrams`；缺失时保留全部研究成果，但不得把任务标记为完整交付。

---

## ⚙️ 配置

```yaml
local_vault_path: null        # 可选：本地知识库、笔记库或资料库路径；未配置则跳过本地资料扫描
workspace_path: .             # 当前项目或 AI 运行时工作目录
research_output_dir: ./research
writing_skill_path: null      # 可选：gracker-writing/SKILL.md 的本地路径
diagram_skill_path: null      # gracker-diagrams/SKILL.md 的本地路径；技术调研交付必需
obsidian_vault_path: null     # Obsidian vault 根目录，目录内必须存在 .obsidian/
obsidian_research_dir: DeepResearch
required_accepted_diagrams: 2 # 深度技术调研默认至少两张通过验收的成图
```

**Portability**：所有路径都必须由当前用户、运行时或只读发现得到，不得写死用户名、HOME、模型或图像后端。`local_vault_path` 只影响可选的 Phase 0 扫描；`obsidian_vault_path` 和 `diagram_skill_path` 是完整交付门禁，不能用临时目录或伪图绕过。

---

## 术语

| 术语 | 含义 |
|------|------|
| **Phase 0 scan** | 扫描本地知识库相关文件，生成覆盖度评估 |
| **research dump** | 研究员对每个子问题的原始发现，写入本地 .md 文件 |
| **local context** | Phase 0 产出的本地知识摘要 |
| **master research** | dump + local context 汇总后的单一文件 |
| **四层质检** | L1 禁用词/硬伤 → L2 可读性 → L3 内容深度 → L4 活人感（Gracker 写作标准） |
| **accepted diagram** | 已通过语义、文字、结构、风格和技术规格验收的真实栅格图片 |
| **Obsidian 发布包** | 报告、成图、研究材料、成图中间文件和发布清单组成的可迁移目录 |

---

## 四段工作流总览

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
├──────────────────────────────────────────────────────────┤
│  PHASE 3: 视觉化 + 发布                                   │
│  目标: Gracker 风格真实成图，并把完整研究包发布到 Obsidian   │
│  门禁: 图片验收、嵌入可解析、材料可追溯                     │
├──────────────────────────────────────────────────────────┤
│  PHASE 4: 交付回执                                        │
│  目标: 只报告已验证的产物、路径、数量和残余限制              │
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

把每轮结果写入 `{OUT_DIR}/quality-report.md`；rewrite 后更新该文件，保留轮次和最终结论。Phase 3 发布脚本会把它作为完成证据校验。

### rewrite 触发逻辑

| 质检结果 | 处理 |
|---------|------|
| L1 不通过 | **强制 rewrite**，明确列出 L1 命中的禁用词/硬伤位置，主 session 监督修复 |
| L2 不通过（开头未过） | **强制 rewrite** |
| L2 不通过（其他项） | 可选 rewrite，明确告知具体段落 |
| L3-1/3-2 不通过 | **强制 rewrite**，指出缺乏支撑的具体判断 |
| L4 整体不通过 | **强制 rewrite**，给出"哪个段落 AI 味重"的具体指引 |
| 全部通过 | 进入 Phase 3 视觉化与发布 |

**rewrite 配置**：
- 执行方式：复用 Phase 2b 的写作执行方式；如果运行时支持独立 writer/rewrite 任务，可以单独执行
- 模型：不在 Skill 中指定，由运行时或用户配置决定
- prompt：在 Phase 2b writer prompt 基础上，附加质检报告，让 rewrite 专门修复标出的问题
- rewrite 完成后再执行一次 Phase 2c 质检，通过才能交付

---

## Phase 3: Gracker 视觉化 + Obsidian 发布

开始前必须读取 `references/visual-obsidian-delivery.md`，并读取 `diagram_skill_path` 指向的完整 `gracker-diagrams/SKILL.md`。后者是图片分析、结构化、提示词、生成与验收的执行规范；本文只定义深度调研的选图策略和发布门禁。

### Phase 3a: 选择图片

- 深度技术调研默认产出 `required_accepted_diagrams` 张图片，默认值为 2。
- 至少覆盖两类信息：① 架构、机制或时序；② 方案选择、评审清单或结论摘要。
- 每张图片必须服务于正文中的明确章节，不为装饰而作图。
- 如果用户明确指定更少数量，可降低门禁；否则不能因生成困难自行降级。

### Phase 3b: 生成与验收

每张图都必须保留下列中间文件：

```text
gracker-diagrams/{diagram-name}/
├── source.md
├── analysis.md
├── structured-content.md
├── copy.md
├── prompts/infographic.md
├── output/diagram.png
└── quality-review.md
```

必须调用真实图像生成能力并遵循 Gracker 风格。不得用 HTML、SVG、Mermaid 或网页截图冒充生成图。每张图最多进行一次有针对性的视觉修正；修正后仍有事实、字符或结构错误，则标记为 rejected，不计入完成数量，也不得嵌入报告。

### Phase 3c: 发布到 Obsidian

1. 验证 `obsidian_vault_path/.obsidian/` 存在；缺失时停止发布并请求正确路径。
2. 在 `{obsidian_vault_path}/{obsidian_research_dir}/{YYYY-MM-DD}-{slug}/` 创建独立发布包。
3. 可使用 `scripts/publish_to_obsidian.py` 做原子化复制和成图嵌入。脚本默认拒绝覆盖已存在目录；只有用户明确要求替换时才传 `--overwrite`。
4. 检查 Obsidian note 中每个 `![[assets/...]]` 都能解析到非空文件，研究材料链接指向发布包内文件。
5. 保留完整研究材料与每张 accepted diagram 的修订中间文件。整体被拒收的 diagram 可以留在 workspace 审计，但不得进入发布包；已通过 diagram 的早期修订稿只能留在它自己的 `gracker-diagrams/` 工作目录，不得进入 `assets/` 或主 note。

发布包结构：

```text
{YYYY-MM-DD}-{slug}/
├── {report-title}.md
├── assets/
│   └── *.png
├── research-materials/
├── gracker-diagrams/
│   └── {diagram-name}/
└── publish-manifest.json
```

### Phase 3d: 完成门禁

以下条件必须全部成立，才能进入最终交付：

- 报告和 `master-research.md` 存在且非空；
- 引用来源已归档，正文关键结论可追溯；
- accepted diagram 数量达到门禁，图片文件非空且通过验收；
- Obsidian note 已嵌入全部 accepted diagrams，所有嵌入目标存在；
- 发布包包含研究材料、成图中间文件和 `publish-manifest.json`；
- 发布脚本或等价验证没有报错。

## Phase 4: 交付回执

1. **工作区报告路径**：`{research_output_dir}/{YYYY-MM-DD}-{slug}-深度调研.md`
2. **Obsidian 路径**：给出实际 vault 内发布包路径和主 note 路径。
3. **发送用户**：标题、摘要预览、来源数量、accepted/rejected 图片数量、质检轮次和可点击路径。不要把 rejected 图片计入成果。
4. **可选记录**：如果运行环境提供 memory / notes / task log，则追加一条简短记录；没有则跳过，不影响已经完成的实体交付。

```
## [HH:MM] task | 深度调研·{topic}·已完成
- 规模: {small/medium/large}，耗时约 X 分钟
- Phase 0: 扫描 {X} 个目录，命中 {N} 个本地文件
- Phase 1: Y 个研究员落盘，Z 个来源
- Phase 2: 断网写作
- Phase 2c: 四层质检 [{通过/强制 rewrite X 轮}]
- Phase 3: Gracker 成图 {accepted} 张，拒收 {rejected} 张；已发布到 Obsidian
- 报告: {research_output_dir}/{filename}
- Obsidian: {obsidian_publish_dir}/{report-title}.md
```

---

## 产出文件规范（cron / 定时任务与深度调研通用）

所有最终笔记、报告和总结必须遵守以下规范，便于事后快速理解具体产物：

- **文件名**：使用基于核心内容的描述性 slug（日期 + 主要主题关键词），例如 `2026-07-05-并行-Agent在Gracker研究workflow中的工程实践.md`；避免只有日期的纯时间戳文件名。
- **摘要先行**：frontmatter 和一级标题之后立即放置独立的 `## 执行摘要` / `## Summary` 区块。任何人打开文件，前 15–20 行就能看到：
  - 本次主要产出的文件与可解析路径 / wikilink；
  - 1–3 条最关键发现或信号；
  - 核心 takeaway 和仍存在的限制。
- Phase 3 完成后，更新发布版执行摘要，加入 Obsidian 发布包、accepted diagrams 和研究材料路径。
- 定时任务的最终交付内容（包括发往 Telegram 的部分）也必须以执行摘要开头。

此规范与 `gracker-writing`、四层质检和 Obsidian 完成门禁共同生效。

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
| `diagram_skill_path` 不存在 | 保留报告与研究材料，说明视觉交付未完成；不得生成替代伪图 |
| `obsidian_vault_path` 未配置或不是 vault | 停止 Phase 3c，请求正确路径；不得把 workspace 临时目录称为 Obsidian 交付 |
| 图像生成后出现错字或事实错误 | 最多定向修正 1 次；仍失败则 rejected，不嵌入、不计数 |
| Obsidian 目标目录已存在 | 默认停止，避免覆盖；仅在用户明确授权时使用 `--overwrite` |
| Obsidian 嵌入或内部链接失效 | 修复并重新验证；未通过不得宣布完整交付 |
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
| 技术图 | 可选或无 | **真实 Gracker 成图 + 中间文件 + 逐图验收** |
| 知识库交付 | 仅工作区文件 | **完整发布包落盘到 Obsidian，嵌入与链接通过验证** |
