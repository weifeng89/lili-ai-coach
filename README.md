# lili-ai-coach · 查理（lili酱的 AI 协作教练）

一个给**非技术初学者**的 AI 协作教练 skill。它不替你写代码、不考试打分，而是陪你把「模糊想法 / 跟 Agent 聊卡住的下一步」变成「清楚能做的计划」：

- **随问随答模式**：你跟任何 Agent 聊卡住、看不懂输出、不知下一步时，查理帮你命名问题、定位不清、拟一句能回发的澄清问句，并教你这个套路。
- **需求挖掘**：用「你提选项、她只确认」+ 跨轮 pattern 识别，挖出真需求、标出伪需求（手段）。
- **PTCF PRD**：把需求落成 画像 / 任务 / 约束 / 验收 四段，带完整度查漏补缺，**MVP 优先**。
- **workflow 设计**：显式拆出 触发→步骤→决策点→产出→回流，让她真正拥有并优化自己的协作方法。
- **收口 + 感知提效**：让她自己说出「AI 这次帮我省了哪几步」。

> 教练 persona 叫 **查理**；服务对象叫 **lili酱**。包名 `lili-ai-coach` 保持稳定（GitHub 仓库名）。
> 沟通风格（简单中文、音乐比喻、一步步来）由 lili酱 的**个性化 prompt** 负责，本 skill 不重复——两者配合，不重叠。

---

## 仓库结构

```
lili-ai-coach/
├── README.md                      # 本文件（总览 + 按 agent 安装）
├── SKILL.md                       # agentskills.io 格式 → WorkBuddy 与 Hermes 共用
├── agents/openai.yaml             # Codex 适配器（同方法论正文，version 同步）
├── references/                    # 三 harness 共享，运行时懒加载
│   ├── need-mining.md             # 挖掘、3–5 问、pattern 识别
│   ├── prd-template.md            # PTCF 模板 + 完整度检查（MVP 优先）
│   └── workflow-card.md           # workflow 五段结构 + 可选 🛠 字段
├── eval/                          # mentor / 验收（可选下载，运行时不用）
│   ├── eval-criteria.md           # AC1–14 + UC1–14
│   ├── eval-checklist.json
│   └── eval-checklist.csv
└── examples/                      # 样张（可选）
    ├── 日语助手-PRD示例.md         # 闭环主路径
    └── 沟通卡点-查理陪练示例.md     # 随问随答 / 卡点陪练实景
```

---

## 安装（按你用的 Agent 选一种）

本 skill 支持 **WorkBuddy、Hermes、Codex** 三种 agent。WorkBuddy 与 Hermes 都遵循 **agentskills.io** 开放标准（Markdown + YAML 头），所以**共用同一份 `SKILL.md`**；只有 Codex 用单独的 `agents/openai.yaml`。

### ① WorkBuddy
1. 找到 skills 目录（一般 `~/.codebuddy/skills/` 或设置里写的路径）。
2. 新建 `lili-ai-coach/` → 把 `SKILL.md` 和 `references/` 丢进去。
3. 重启 / 刷新 WorkBuddy。

### ② Hermes
1. Hermes 的 Skill 也是 agentskills.io 格式，存 `~/.hermes/skills/`。
2. 同样新建 `lili-ai-coach/` → 把 `SKILL.md` 和 `references/` 丢进去。
3. 重启 Hermes 即可（它会自动匹配加载）。
   > 注：若你的 Hermes 版本对 frontmatter 要求额外字段（如 `type`），**只改 `SKILL.md` 的 YAML 头，不改正文**——方法论正文跨 harness 一致性（AC8）比的是正文，不是 frontmatter。

### ③ Codex
1. 找到 Codex 的 agents/skills 目录。
2. 新建 `lili-ai-coach/agents/openai.yaml`（连同 `references/`）。
3. Codex 加载即可。

> **个性化 prompt 单独设**：说话风格（简单中文、音乐比喻等）在你各自 agent 的配置里设，**不进这个包**，避免和查理的方法论重叠。

---

## 怎么用

开对话，直接说：
- 「我想做个 XX，帮我先想清楚」→ 进 需求挖掘
- 「PRD 写好了，帮我拆 workflow」→ 直接从 C 进（柔性入口，不必从 A 走到底）
- 「我跟那个 Agent 聊卡住了，看不懂它说的」→ 进 随问随答模式
- 「一起想想这个需求」→ 进 需求挖掘

查理会按「入口路由」判断你现在在哪一站，不会每次都逼你走完整四阶段。

---

## 验收 / 质量

交付标准见 `eval/eval-criteria.md`（AC1–AC14 + UC1–UC14，参考 [mattpocock/skills](https://github.com/mattpocock/skills) 的「小且可组合 / user-invoked / 文档中立 / 版本同步」质量杆，改为非技术初学者口径）。机读勾选版：`eval/eval-checklist.json` / `.csv`。

重点验收项：
- **AC8 跨 harness 一致**：`SKILL.md` 与 `agents/openai.yaml` 方法论正文逐字符一致（已脚本校验）。
- **AC13 Token 效率纪律**：压缩优先 / 懒加载 references / 产物落文件 / 软预算 ≤~8 轮——这是防止直接当教练用时上下文爆炸的硬约束。
- **AC9 零重叠**：查理不重复个性化 prompt 的沟通风格规则。

---

## 许可

自由下载、自用、改。欢迎提 PR 优化查理的方法论。
