# Aren Illustrations

阿任风格的中文正文配图生成 Skill。基于 [Ian Xiaohei Illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations) 改造，把 IP 从"小黑"换成"阿任"。

## 这个 skill 是什么

为中文文章设计和生成 16:9 横版正文配图。默认视觉 IP 是 **阿任**：

- 蓬松黑色短发到中发，圆框眼镜，明显的橙红腮红
- oversized 风格黑色皮夹克 + 白 T 恤 + 纯黑运动裤 + 黑白运动鞋
- Q 萌版身材（头身比约 1:2.5-1:3）
- 整体画风：新海诚动画风格 + 铅笔线稿 + 彩铅涂色混合手绘
- 表情：温和闭口微笑或平静专注，**绝不能呆滞或无表情**

阿任不是吉祥物，不是贴纸，是正在认真参与系统运转的青少年角色。详见 `references/ip-character.md`。

## 怎么用

```text
Use $aren-illustrations 为这篇中文文章设计并生成 4 张阿任怪诞正文配图。<粘贴文章>
```

也可以只出配图策略不生图：

```text
Use $aren-illustrations 先不要生图。分析下面这篇文章哪里值得配图，输出 5 张左右的 shot list。
```

## 视觉风格

- 16:9 横版，纯白背景
- 5 色制：黑 / 橙红腮红（IP 专属） / 红 / 橙 / 蓝
- 大量留白，主结构占画面 40-60%
- 一张图只讲一个核心动作
- 中文手写批注 ≤ 5-8 处

## 目录结构

```
aren-illustrations/
├── SKILL.md                       Skill 入口
├── LICENSE                        MIT License（继承自上游）
├── NOTICE.md                      归属说明
├── .gitignore
├── agents/
│   └── openai.yaml                Agent 元数据
├── assets/
│   └── examples/                  风格校准图（阿任 IP）
│       ├── 01-aren-carrying-box.png
│       ├── 02-aren-debugging-funnel.png
│       └── README.md
└── references/
    ├── ip-character.md            阿任 IP 视觉 DNA
    ├── style-dna.md               风格 DNA 与色系
    ├── composition-patterns.md    8 种结构类型与隐喻
    ├── prompt-template.md         生图 prompt 模板
    └── qa-checklist.md            必过项与失败信号
```

## 与上游的差异

| 维度 | 上游（ian-xiaohei-illustrations） | 本 fork（aren-illustrations） |
|---|---|---|
| IP | 小黑（纯黑实心小怪物） | 阿任（彩铅手绘少年） |
| 风格 | 纯线稿 | 铅笔线稿 + 彩铅涂色混合 |
| 笔触 | 单色 | 彩铅涂色 + 暖色腮红 |
| 表情 | 空白、呆（IP 设计如此） | 温和微笑或平静专注（绝不能呆滞） |
| 构图禁忌 | 阿任可以塞进机器/漏斗 | 阿任**不**能塞进机器/漏斗（真人比例） |

## 校准图覆盖情况

- ✅ Workflow 流程 — 待补
- ⚠️ 系统局部 — 02 部分覆盖
- ✅ 角色状态 — 01 覆盖
- ⚠️ 概念隐喻 — 01/02 部分覆盖
- ✅ 前后对比 — 待补
- ✅ 方法分层 — 待补
- ✅ 地图路线 — 待补
- ✅ 小漫画分镜 — 待补

详见 `assets/examples/README.md`。

## 维护

```bash
# 装到 Codex / Mavis skills 目录
cp -R ./aren-illustrations "$HOME/.codex/skills/"  # Codex
# 或
cp -R ./aren-illustrations "$HOME/.mavis/skills/"   # Mavis
```

## 致谢

- 原始 skill：[helloianneo/ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations) by Ian
- 派生 fork 维护者：RossBool
- 校准图由 AI 图像生成工具生成

## License

MIT（继承自上游）。详见 `LICENSE` 和 `NOTICE.md`。
