---
name: gracker-deep-research
description: Gracker Deep Research Skill · 三阶段调研法（本地扫描 → 探索落盘 → 利用写作）。Phase 0 扫描本地优质资料，Phase 1 全力搜索并落盘，Phase 2 断网只读本地文件写报告。触发词：「深度调研 XXX」/ 「Gracker Research XXX」/ 「dg XXX」。
---

# Gracker Deep Research Skill

> **核心理念**：三阶段解耦 —— 本地扫描（已有知识激活）→ 探索落盘（互联网 → 本地文件）→ 利用写作（断网读本地文件）。
>
> 参考：2026 年两阶段深度研究范式（探索-利用解耦），扩展为三阶段，优先激活本地资产。

---

## ⚙️ 配置（Portable）

```yaml
# 本地知识库路径（Gracker 默认配置）
local_vault_path: /Users/gracker/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian
workspace_path: /Users/gracker/.openclaw/workspace
research_output_dir: {local_vault_path}/调研/

# 其他用户请修改上述三个变量，或设置环境变量：
# export DEEP_RESEARCH_VAULT_PATH=/your/obsidian/path
# export DEEP_RESEARCH_OUTPUT=/your/obsidian/path/调研/
```

**Portability 策略**：
- 路径全部变量化，不写死绝对路径
- Phase 0 扫描失败（路径不存在）时 **静默跳过**，不影响后续执行
- Phase 0 结果中标注"本地命中"的文件路径供溯源

---

## 术语

| 术语 | 含义 |
|------|------|
| **Phase 0 scan** | 扫描本地 Vault 相关文件，生成覆盖度评估 |
| **research dump** | 研究员对每个子问题的原始发现，写入本地文件 |
| **local context** | 本地知识摘要（Phase 0 的产出） |
| **master research** | dump + local context 汇总后的单一文件（写入报告的原材料） |

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
│  原则: 全力搜索，不漏信号                                   │
├──────────────────────────────────────────────────────────┤
│  PHASE 2: 利用 —— 读文件 + 写作                          │
│  目标: 基于本地干净文件进行高频迭代写作                       │
│  原则: 断网，只读本地文件                                   │
└──────────────────────────────────────────────────────────┘
```

---

## 路径定义

```
Obsidian 根目录:   {local_vault_path}
调研输出目录:       {research_output_dir}
报告路径:           {调研}/{YYYY-MM-DD}-{topic-slug}-深度调研.md
研究材料目录:        {调研}/{YYYY-MM-DD}-{topic-slug}-研究材料/
  ├── 00-local-context.md       # Phase 0 产出：本地知识摘要
  ├── 01-{slug}-dump-1.md      # 子问题1 的原始研究
  ├── ...
  ├── master-research.md         # dump + local context 汇总
  └── references/                # 参考资料全文归档
      ├── 01-{source-slug}.md
      └── ...
```

---

## Phase 0: 本地文件扫描（优先激活已有知识）

**执行时机**：在规划任何子问题之前，**第一个**执行。

**Portability**：路径不存在时静默跳过，不报错，不阻断。

### 执行步骤

**Step 0a: 确定搜索范围**

扫描以下本地目录（存在才扫）：
- `{local_vault_path}/Android-Internal-Wiki/` — AIW 知识库（Gracker 核心资产）
- `{local_vault_path}/DeepResearch/` — 历史深度调研报告
- `{local_vault_path}/调研/` — 历史调研材料
- `{local_vault_path}/awesome-ai-field-notes/` — AI Field Notes
- `{local_vault_path}/X 文章/` — X/Twitter 收藏文章
- `{workspace_path}/MEMORY.md` — 助手长期记忆
- `{workspace_path}/memory/` — 日记层记忆

**Step 0b: 关键词扫描**

用 ripgrep 对每个存在的目录执行：

```bash
# 对每个存在的目录，搜索 topic 相关关键词，限制结果数
rg -l --max-count 10 "{keyword1}|{keyword2}" "{dir}/" --type md 2>/dev/null
```

关键词从题目提取 3-5 个核心概念。

**Step 0c: 读取高匹配文件**

对 Step 0b 找到的文件，读取相关段落（最多 5 个最有价值的文件）：

```bash
rg -C 3 "{keyword}" "{file}" 2>/dev/null | head -100
```

**Step 0d: 编译本地覆盖度评估**

写入 `00-local-context.md`：

```markdown
---
phase: 0
topic: {topic}
vault_path: {local_vault_path}
---

# Phase 0 · 本地知识扫描结果

## 扫描目录
{扫描了哪些目录，成功哪些，跳过了哪些（不存在）}

## 命中文件

### {文件名1}
- **路径**: {path}
- **相关段落**:
  ```
  {rg 输出的相关段落片段，限制 80 行}
  ```
- **对本题的价值**: 高/中/低（为什么）

### {文件名2}
...

## 覆盖度评估

| 子维度 | 本地覆盖度 | 本地来源 |
|--------|-----------|---------|
| {维度1} | 高/中/低 | {文件列表} |
| {维度2} | 高/中/低 | {文件列表} |
| ... | ... | ... |

## 子问题范围调整建议

基于本地扫描结果：
- **{子问题A}**：本地已有高覆盖 → **缩小搜索范围，重点补充最新动态**
- **{子问题B}**：本地无覆盖 → **全文搜索，不设限制**
- **{子问题C}**：本地有部分覆盖 → **补充缺失部分，验证时效性**
```

### Phase 0 输出

- 文件：`{研究材料目录}/00-local-context.md`
- 覆盖度矩阵：指导 Phase 1a 的子问题范围
- 命中文件路径列表：写入 local context，供后续溯源

---

## Phase 1a: 规划子问题（受 Phase 0 结果指导）

**关键区别**：Phase 0 的覆盖度评估直接影响子问题范围。

1. 读取 Phase 0 输出的 `00-local-context.md`
2. 结合 topic 拆解子问题，Phase 0 高覆盖的子问题**明确标注缩小范围**
3. 创建目录结构

```bash
TOPIC_SLUG=$(echo "{topic}" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/-/g')
DATE=$(date +%Y-%m-%d)
mkdir -p "{调研}/{DATE}-{TOPIC_SLUG}-研究材料/references"
```

4. 回执用户：
   `收到，开始处理。本地扫描命中 X 个相关文件。预估 X 分钟，Y 个方向（Phase 0 发现 {A} 子问题本地已有高覆盖，搜索聚焦缺失部分）。`

---

## Phase 1b: 并行研究员写 research dump

（与前版一致，区别是每个研究员收到 Phase 0 的 local context + 覆盖度标注）

研究员 prompt 增加：

```
## Phase 0 本地覆盖度标注
{从 00-local-context.md 提取该子问题的覆盖度行}
```

---

## Phase 1c/1d: 缺口检查 + 补充 + 编译 master-research

（与前版一致）

---

## Phase 2: 写作（断网模式）

**核心约束：此阶段 agent 不使用 web_search/web_fetch，只读本地文件。**

### Phase 2a: 验证 master-research.md 存在

如果 master-research.md 不存在或为空，报错通知用户，不继续写作。

### Phase 2b: 写作 Agent

**模型: openai-codex/gpt-5.4（强制，不可用其他模型）**

**Prompt 增加 Phase 0 说明**：

```
## 本地资产激活记录（Phase 0）
本次调研在开始互联网搜索之前，优先扫描了本地知识库。
{从 00-local-context.md 提取覆盖度矩阵}
报告应区分：哪些是本地已有知识，哪些是本次新研究发现。
```

---

## Phase 3: 交付

```
已完成。
- Phase 0: 扫描 {X} 个目录，命中 {N} 个本地文件
- Phase 1: Y 个研究员落盘，共抓取 {Z} 个来源
- Phase 2: GPT-5.4 断网写作
- 报告: Obsidian/调研/{filename}，共 {X} 字
- 参考资料: {N} 篇已归档到同目录
```

---

## 一手资料优先原则

| 优先级 | 资料类型 |
|--------|----------|
| 1 | 源码（AOSP cs.android.com / GitHub） |
| 2 | 官方文档 |
| 3 | 学术论文（arxiv） |
| 4 | 官方 Issue / CL / Release Notes |
| 5 | 官方博客 |
| — | 二手博客（仅作线索，必须追溯到一手） |

---

## 错误处理

| 场景 | 处理 |
|------|------|
| Phase 0 扫描目录不存在 | **静默跳过**，不报错，不阻断 |
| Phase 0 ripgrep 无结果 | 正常继续，输出"本地无命中" |
| 研究员超时 | 缩小范围重试 1 次 |
| GPT-5.4 不可用 | **立即通知用户，不降级** |
| 写文件到 Vault 失败 | 降级到 workspace tmp，通知用户 |

---

## 与旧版 deep-research skill 的差异

| 差异点 | 旧版 | 新版 |
|--------|------|------|
| Phase 0 本地扫描 | 无 | **优先执行，影响子问题规划** |
| 本地知识激活 | Phase 2 顺手搜 | **Phase 0 主动扫，输出覆盖度矩阵** |
| 子问题范围 | 固定 | **动态，受本地覆盖度指导** |
| 写作素材传递 | inline 拼接 | 只读本地文件 |
| 写作阶段网络 | 可能继续访问 | **断网，只读本地** |
| Portability | 无 | **路径可配置，扫描失败静默跳过** |
