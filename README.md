# Gracker Deep Research Skill

深度技术调研完整交付 Skill：本地扫描、探索落盘、断网写作、Gracker 风格真实成图，并把可审计研究包发布到 Obsidian。

## 安装

默认安装仓库当前默认分支，不需要版本号：

```bash
npx skills add Gracker/gracker-deep-research-skill --yes --global
```

需要可复现安装时，先发布 Git tag 或 release，再按安装器支持的 tag / commit 语法固定版本；当前命令不写虚构版本号。

## 触发词

深度调研、Gracker Research、dg

## 工作流程

```
本地扫描 → 子问题调研 → research dump 落盘 → master research 汇总 → 断网写报告 → 四层质检 → Gracker 成图与验收 → Obsidian 发布包
```

完整交付需要可用的 `gracker-diagrams` skill、真实图像生成能力，以及一个包含 `.obsidian/` 的 vault 路径。详细 prompt 模板、质检规则和发布门禁见 `references/` 目录；`scripts/publish_to_obsidian.py` 提供默认不覆盖、原子化的发布入口。

## 维护验证

```bash
python3 -m unittest discover -s tests
python3 /path/to/skill-creator/scripts/quick_validate.py .
git diff --check
```

第二条命令中的 `skill-creator` 路径由当前运行环境提供，不在仓库中写死。

## License

MIT
