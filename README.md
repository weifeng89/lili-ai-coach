# lili-ai-coach · 查理（lili酱的 AI 协作教练）

> **本文件面向 Agent / 开发者（安装执行规范），lili酱 无需阅读，也无需做任何文件 / 目录 / 命令行操作。**

- **版本**：2.2.0
- **一句话能力**：给**非技术初学者**的 AI 协作教练——自动在「需求不清 / 跟 Agent 聊卡住 / 要写需求四件套 / 要拆步骤 / 对话变卡 / 做完想复盘」时切入，陪她把模糊变清楚、把卡点翻成能直接发的精准指令，不考试不打分。
- **支持 harness**：WorkBuddy、Hermes、Codex（三端共用同一套方法论正文，跨端一致）。
- **核心纪律**：小且可组合、只教协作方法不替代思考、不重复个性化 prompt 的人设层、MVP 优先、Token 高效。

---

## 仓库结构

```
lili-ai-coach/
├── README.md                      # 本文件（Agent/开发者安装规范）
├── install.py                     # 通用安装器（跨 OS / 跨三 harness，单源逻辑）
├── install.sh                     # bash 便捷封装，调用 install.py
├── SKILL.md                       # agentskills.io 格式 → WorkBuddy 与 Hermes 共用
├── agents/openai.yaml             # Codex 适配器（同方法论正文，version 同步）
├── references/                    # 三 harness 共享，运行时懒加载
│   ├── need-mining.md             # 挖掘、3–5 问（每问 ≤2 候选）、pattern 识别
│   ├── prd-template.md            # 项目四件套模板 + 完整度检查（MVP 优先）
│   ├── workflow-card.md           # 落地步骤清单五段结构 + 可选 🛠 字段
│   ├── token-optimize.md          # 对话精简诊断、指令压缩、省事技巧
│   └── review-template.md         # 分层复盘引导、自动记账格式、归档规则
├── eval/                          # mentor / 验收（可选，运行时不用，禁装）
│   ├── eval-criteria.md           # AC1–AC20 + UC1–UC20
│   ├── eval-checklist.json
│   └── eval-checklist.csv
└── examples/                      # 样张（可选，lili酱 不下载，禁装）
    ├── 日语助手-PRD示例.md
    └── 沟通卡点-查理陪练示例.md
```

> `lili-coach-log.md`（及精简版 `lili-coach-log.v2.md`）是**运行时按项目生成**的成长账本——磁盘文件、不进仓库、不每轮加载，也只在复盘时才读入上下文。安装过程绝不触碰它。

---

## 强制安装执行流程（Agent / 开发者照此执行）

### 拉取源
固定拉取 `main` 分支最新版本：`https://github.com/weifeng89/lili-ai-coach`。

### 下载白名单（仅这些，违者安装失败）
- `SKILL.md`
- `references/` 全目录
- Codex 环境额外：`agents/openai.yaml`

### 下载黑名单（严禁，违者安装失败）
- `eval/` —— 仅 mentor 验收用，运行时不需要
- `examples/` —— 仅样张，lili酱 不需要也不该看到

### 三 harness 目标路径（脚本自动探测，兼容品牌改名歧义）
| harness | 目标目录（任一存在即装） |
| :--- | :--- |
| WorkBuddy | `~/.codebuddy/skills/` **或** `~/.workbuddy/skills/` |
| Hermes | `~/.hermes/skills/` |
| Codex | 对应 agents/skills 下的 `lili-ai-coach/` |

> 注：WorkBuddy 公开文档用 `~/.workbuddy/skills/`，本沙盒历史用 `~/.codebuddy/skills/`——安装器两处都探测，无需人工判断。

### 两条安装命令（二选一）
1. **通用（推荐，全 harness 适用）**：
   ```bash
   python3 install.py            # 自动探测 harness + 从 GitHub 拉最新
   # 或离线/指定： python3 install.py --src ./ --target ~/skills --harness workbuddy
   ```
2. **WorkBuddy 便捷**（仅最新版 WorkBuddy 支持）：
   ```bash
   npx add-skill weifeng89/lili-ai-coach
   ```

### 安装后校验（install.py 自动完成，人工可复核）
- 文件完整性：`SKILL.md` + `references/` 5 页齐备；Codex 额外有 `agents/openai.yaml`。
- 跨端一致性：`SKILL.md` 与 `agents/openai.yaml` 方法论正文逐字符一致（AC8）。
- 懒加载规则：`references/` 不进 `SKILL.md` 正文，仅运行时按阶段加载。
- 版本一致：`SKILL.md` 与 `agents/openai.yaml` 的 `version:` 相同。

---

## 版本更新规则
- 定期检查仓库 `version:`；有更新时增量同步 `SKILL.md` + `references/`（+Codex `openai.yaml`），重跑校验。
- **用户本地 `lili-coach-log.md` 必须保留，不得覆盖**（安装器已做保护）。

---

## 极简触发示例（供入口语义识别，非操作说明）
- 「我想做个练日语的东西，帮我先想清楚」
- 「我跟那个 Agent 聊卡住了，看不懂它说的」
- 「搞定了，这个做完了」

---

## 验收 / 质量
交付标准见 `eval/eval-criteria.md`（AC1–AC20 + UC1–UC20，参考 [mattpocock/skills](https://github.com/mattpocock/skills) 的「小且可组合 / 文档中立 / 版本同步」质量杆，改为非技术初学者口径）。机读勾选版：`eval/eval-checklist.json` / `.csv`。

重点验收项：
- **AC8 跨 harness 一致**：`SKILL.md` 与 `agents/openai.yaml` 方法论正文逐字符一致。
- **AC17 零安装感知**：lili酱 端零文件操作；install 脚本落盘到正确目录、版本校验、保留 log、不拷 eval/examples。
- **AC18 术语零暴露**：面向 lili酱 的输出无内部术语，方法论均说人话。
- **AC13 Token 效率纪律**：压缩优先 / 懒加载 / 产物落文件 / 软预算（自动触发下仍控上下文）。

---

## 风险与边界（给 mentor）
- **R9 自动触发双触发**：查理自动触发与 base Agent 自身能力可能重叠。缓解：`description` 精准限定「AI 协作/沟通/需求/PRD/workflow/卡点/提效」；纯领域问题走柔性分流产出信封交 base，不自答（见 SKILL.md 🚦）。
- **R10 安装脚本依赖**：需网络 / git 权限；无网环境退化到手动拷贝白名单（见上方「下载白名单」）。`npx add-skill` 仅 WorkBuddy 新版可用，Hermes/Codex 请用 `install.py`。
- **R1 双脑困惑**：查理是「按需自动切入的专项教练」，个性化 prompt 是「常驻性格层」，查理叠方法论不抢性格。
- **R2 范围蔓延**：查理不写领域答案，只做「问题翻译官」+ 教协作方法，保持小且可组合。

> 递延项：独立 `token-efficiency-audit` 诊断 skill（Q3）本轮未做；若后续要，按「独立 skill + 查理转诊」落地，不塞进查理。

## 许可
自由下载、自用、改。欢迎提 PR 优化查理的方法论。
