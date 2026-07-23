# Gracker 视觉与 Obsidian 发布规范

本文件是 `SKILL.md` Phase 3 的执行细则。先完成报告质检，再进入本阶段。

## 1. 选图

深度技术调研默认选择两张互补的图：

1. **机制图**：解释架构、数据流、时序、状态机或版本变化。
2. **决策图**：汇总适用边界、评审问题、风险、测试方法或选型结论。

图必须对应正文的具体章节。长报告可增加到 3-4 张，但不要重复表达相同信息。

## 2. Gracker 工作目录

对每张图单独建立工作目录，并严格执行已安装的 `gracker-diagrams/SKILL.md`：

```text
{diagram-name}/
├── source.md
├── analysis.md
├── structured-content.md
├── copy.md
├── prompts/infographic.md
├── output/diagram.png
└── quality-review.md
```

- `source.md` 只摘录已落盘报告和研究材料中的相关事实。
- `copy.md` 控制图中文字长度；关键 API、类名、数值和单位不得改写。
- `quality-review.md` 记录语义、文字、结构、风格和规格检查，以及是否 accepted。
- 必须使用真实图像生成后端。HTML、SVG、Mermaid 和网页截图不是可接受的替代品。
- 每张图最多一次定向修正。仍有错字、事实错误或层级错误时，标为 rejected。

## 3. Obsidian note

主 note 应包含可检索的 frontmatter，例如：

```yaml
---
date: 2026-07-21
tags:
  - deep-research
  - topic-keyword
---
```

在相关章节附近嵌入图片：

```markdown
![[assets/diagram-name.png]]
```

不要只在文末堆放所有图片。每个嵌入路径都必须解析到发布包内的非空图片。

## 4. 发布脚本

推荐命令：

```bash
python3 scripts/publish_to_obsidian.py \
  --vault "/path/to/Vault" \
  --collection "DeepResearch" \
  --slug "2026-07-21-topic" \
  --report "./research/2026-07-21-topic-深度调研.md" \
  --materials "./research/2026-07-21-topic-研究材料" \
  --diagram "mechanism=./visuals/mechanism/output/diagram.png" \
  --diagram-workdir "mechanism=./visuals/mechanism" \
  --diagram "review=./visuals/review/output/diagram.png" \
  --diagram-workdir "review=./visuals/review" \
  --tag "deep-research" \
  --tag "topic-keyword"
```

脚本默认拒绝已有目标目录，并在同一父目录内 staging 后原子 rename。`--overwrite` 会替换整个目标发布包，只能在用户明确授权时使用。

脚本默认要求至少两张 accepted diagram，并验证 `master-research.md`、`quality-report.md`、引用归档、PNG 文件、逐图中间文件、验收结论以及 `output/diagram.png` 与待发布图片的哈希一致性。用户明确降低图片数量时，才使用 `--minimum-diagrams 1`。脚本会把报告中指向原材料目录名的相对链接重写为发布包内的 `research-materials/`，随后拒绝任何越界或断裂的本地链接。

## 5. 发布后验证

至少验证：

- 主 note、`master-research.md`、所有 accepted 图片非空；
- `publish-manifest.json` 中的图片数量达到门禁；
- note 中的每个 `![[...]]` 目标存在；
- `research-materials/references/` 中保留引用归档；
- 每张已发布图片都有完整中间文件和 accepted 结论；
- 整体 rejected 的 diagram 没有进入发布包；accepted diagram 的早期修订稿没有进入 `assets/` 或主 note。

任何一项失败，都应报告“研究或发布已部分完成”，而不是宣称完整交付。
