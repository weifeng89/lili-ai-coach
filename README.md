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
└── examples/                      # 样张（可选，lili酱 不下载）
    ├── 日语助手-PRD示例.md         # 闭环主路径
    └── 沟通卡点-查理陪练示例.md     # 随问随答 / 卡点陪练实景
```

> `lili-coach-log.md`（及紧凑版 `lili-coach-log.v2.md`）是**运行时按项目生成**的成长账本——磁盘文件、不进仓库，也只在里程碑 / compact / 复盘时才读入上下文（见 SKILL.md 🪞 复盘与迭代模式）。

---

## 安装（按你用的 Agent 选一种）

本 skill 支持 **WorkBuddy、Hermes、Codex** 三种 agent。WorkBuddy 与 Hermes 都遵循 **agentskills.io** 开放标准（Markdown + YAML 头），所以**共用同一份 `SKILL.md`**；只有 Codex 用单独的 `agents/openai.yaml`。

> ⚠️ **给 lili酱 的安装（也提醒各 agent）**：只下载 `SKILL.md` + `references/`（+Codex 的 `agents/openai.yaml`）。**不要下载 `eval/` 和 `examples/`**——那是给 mentor 验收与样张用的，lili酱 不需要也不该看到；`eval/` 是可选下载、运行时无需，各 agent 不必拉取。

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

## 风险与边界（给 mentor）

已知风险与缓解，部署前过一遍：

- **R1 双脑困惑**：查理 user-invoked 且 Mode 0 也教沟通，lili酱 可能分不清「在跟查理还是 base agent 说话」。→ 查理是「按需调用的专项教练」，个性化 prompt 是「常驻性格层」，查理叠方法论不抢性格。
- **R2 Mode 0 范围蔓延**：若 Mode 0 答任何问题，查理变通用助手，违背 AC1 / 小且可组合。→ Mode 0 明确定界「只管 AI 协作 / 沟通」，不接领域问答（领域澄清归 base 的头脑风暴模式）。
- **R3 AC13 强制局限**：≤8 轮、懒加载等是「指示」非「机制」，弱模型可能无视。→ 诚实局限：真强制靠 runtime，skill 只能约束行为。
- **R4 references 懒加载假设**：若 runtime 每次调用查理都全量加载 3 份 references，是隐藏成本。→ 约束「按 phase 只载对应一页」，发布前验证 runtime 行为。
- **R5 Hermes frontmatter 差异**：假设一份 SKILL.md 通吃 WB+Hermes，若 Hermes 要求额外头字段可能挂。→ 发布前核对 Hermes frontmatter；只改头不正文（AC8 比的是正文）。
- **R6 转发失真**：lili酱 把查理生成的 prompt 贴给无查理上下文的 Agent，可能降级。→ prompt 信封自包含 + 附「直接复制发给它」说明。
- **R7 复盘日志膨胀**：`lili-coach-log.md` 无限增长又被重载，反成 context 负担。→ 追加式 + 每 ~5 次复盘或超 ~40 行自动 compact 精简，旧 raw 归档。
- **R8 头脑风暴双触发**：「一起想想」→ base 进 brainstorm；同时调查理 → 双 brainstorm。→ 路由明确：领域澄清归 base，沟通教练归查理。

> 递延项：独立 `token-efficiency-audit` 诊断 skill（Q3）本轮未做；若后续要，按「独立 skill + 查理转诊」落地，不塞进查理以保持小且可组合。

## 许可

自由下载、自用、改。欢迎提 PR 优化查理的方法论。
