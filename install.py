#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lili-ai-coach 通用安装器（跨 OS / 跨三 harness）。

设计目标（对应 AC17 零安装感知）：
- lili酱 全程零文件 / 目录 / 命令行操作；开发者（你）对 lili 的环境跑一次即可。
- 自动探测 WorkBuddy / Hermes / Codex 的 skills 目录（同时兼容 ~/.codebuddy 与 ~/.workbuddy 的路径歧义）。
- 仅安装白名单：SKILL.md + references/ 全目录；Codex 额外装 agents/openai.yaml。
- 严禁安装黑名单：eval/、examples/ 绝不拷贝。
- 校验 version 一致、核心文件齐备；不触碰运行时日志 lili-coach-log.md。
- 退出码非 0 = 安装失败，供 Agent / CI 判读。

用法：
  python3 install.py                 # 自动探测 + 从 GitHub 拉最新
  python3 install.py --src ./       # 离线/测试：用本地仓库目录作源
  python3 install.py --target ~/x/skills --harness workbuddy   # 显式指定
  python3 install.py --dry-run      # 只打印将要做什么
"""

import os
import sys
import shutil
import argparse
import subprocess
import tempfile
import urllib.request

REPO = "weifeng89/lili-ai-coach"
GIT_URL = f"https://github.com/{REPO}.git"
RAW_URL = f"https://raw.githubusercontent.com/{REPO}/main"
SKILL_NAME = "lili-ai-coach"

# 白名单：固定要装的（相对仓库根）
WHITELIST_FILES = ["SKILL.md"]
WHITELIST_DIRS = ["references"]
# Codex 额外要装的
CODEX_EXTRA = ["agents/openai.yaml"]
# 黑名单：绝不安装
BLACKLIST_DIRS = ["eval", "examples"]


def log(msg):
    print(f"[install] {msg}")


def die(msg, code=1):
    print(f"[install][ERROR] {msg}", file=sys.stderr)
    sys.exit(code)


def detect_targets():
    """返回 (harness, dir) 列表：探测已存在的 skills 目录。"""
    home = os.path.expanduser("~")
    found = []
    checks = [
        ("workbuddy", os.path.join(home, ".workbuddy", "skills")),
        ("workbuddy", os.path.join(home, ".codebuddy", "skills")),
        ("hermes", os.path.join(home, ".hermes", "skills")),
        ("codex", os.path.join(home, ".codex", "skills")),
        ("codex", os.path.join(home, ".config", "codex", "skills")),
    ]
    for h, d in checks:
        if os.path.isdir(d):
            found.append((h, d))
    return found


def infer_harness(target):
    t = target.replace("\\", "/").lower()
    if "codex" in t:
        return "codex"
    if "hermes" in t:
        return "hermes"
    return "workbuddy"


def fetch_source(args):
    """返回本地源目录路径（可能临时目录，需调用方清理）。"""
    if args.src:
        src = os.path.abspath(args.src)
        if not os.path.isfile(os.path.join(src, "SKILL.md")):
            die(f"--src 指定的目录不含 SKILL.md：{src}")
        return src, None

    # 优先 git clone
    tmp = tempfile.mkdtemp(prefix="lili-coach-")
    log(f"从 GitHub 拉取最新（main）：{GIT_URL}")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", GIT_URL, tmp],
            check=True, capture_output=True,
        )
        return tmp, tmp
    except Exception as e:
        log(f"git clone 失败（{e}），改用 curl 逐文件拉取")
        shutil.rmtree(tmp, ignore_errors=True)
        tmp = tempfile.mkdtemp(prefix="lili-coach-")
        # 先拿到 references 目录文件清单：硬编码已知白名单即可
        files = list(WHITELIST_FILES) + [
            "references/need-mining.md",
            "references/prd-template.md",
            "references/workflow-card.md",
            "references/token-optimize.md",
            "references/review-template.md",
        ] + CODEX_EXTRA
        for f in files:
            os.makedirs(os.path.dirname(os.path.join(tmp, f)) or tmp, exist_ok=True)
            url = f"{RAW_URL}/{f}"
            try:
                urllib.request.urlretrieve(url, os.path.join(tmp, f))
            except Exception as ex:
                # Codex 专属文件在非 Codex 拉取时可缺，不致命
                if f in CODEX_EXTRA:
                    log(f"  （跳过 Codex 专属 {f}：{ex}）")
                    continue
                die(f"拉取失败 {url}：{ex}")
        return tmp, tmp


def read_version(skill_md):
    with open(skill_md, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def install(args):
    dry = args.dry_run
    src, tmp_src = fetch_source(args)

    # 校验源含白名单
    if not os.path.isfile(os.path.join(src, "SKILL.md")):
        die("源目录缺少 SKILL.md")
    if not os.path.isdir(os.path.join(src, "references")):
        die("源目录缺少 references/")

    # 解析目标
    if args.target:
        target = os.path.abspath(args.target)
        harness = args.harness or infer_harness(target)
    else:
        detected = detect_targets()
        if not detected:
            die("未探测到任何 harness 的 skills 目录。"
                "请显式指定：--target <skills目录> --harness workbuddy|hermes|codex")
        # 装到所有已探测到的目录
        targets = detected
        log(f"探测到 {len(targets)} 个 harness：{', '.join(h for h, _ in targets)}")
        code = 0
        for h, d in targets:
            if not _install_one(src, d, h, dry):
                code = 1
        if tmp_src:
            shutil.rmtree(tmp_src, ignore_errors=True)
        sys.exit(code)

    if not _install_one(src, target, harness, dry):
        if tmp_src:
            shutil.rmtree(tmp_src, ignore_errors=True)
        sys.exit(1)
    if tmp_src:
        shutil.rmtree(tmp_src, ignore_errors=True)
    sys.exit(0)


def _install_one(src, target_dir, harness, dry):
    dest = os.path.join(target_dir, SKILL_NAME)
    log(f"目标：{dest}  (harness={harness})")

    # 校验黑名单不会被拷（防御性：源里若误含也不拷）
    for b in BLACKLIST_DIRS:
        if os.path.isdir(os.path.join(dest, b)):
            log(f"  发现已存在的黑名单目录 {b}/，保持删除/跳过")

    if dry:
        log("  [dry-run] 将写入 SKILL.md + references/")
        if harness == "codex":
            log("  [dry-run] 将额外写入 agents/openai.yaml")
        return True

    os.makedirs(dest, exist_ok=True)

    # 1) SKILL.md
    shutil.copy2(os.path.join(src, "SKILL.md"), os.path.join(dest, "SKILL.md"))
    # 2) references/ 整目录
    ref_dest = os.path.join(dest, "references")
    if os.path.isdir(ref_dest):
        shutil.rmtree(ref_dest)
    shutil.copytree(os.path.join(src, "references"), ref_dest)
    # 3) Codex 额外
    if harness == "codex":
        ag_dir = os.path.join(dest, "agents")
        os.makedirs(ag_dir, exist_ok=True)
        src_yaml = os.path.join(src, "agents", "openai.yaml")
        if os.path.isfile(src_yaml):
            shutil.copy2(src_yaml, os.path.join(ag_dir, "openai.yaml"))

    # 4) 保护运行时日志：若已存在则不覆盖（理论上安装不创建它）
    for name in ("lili-coach-log.md", "lili-coach-log.v2.md"):
        p = os.path.join(dest, name)
        if os.path.exists(p):
            log(f"  保留已有日志 {name}（不覆盖）")

    # 5) 校验
    ok = _verify(dest, harness)
    if ok:
        log(f"✅ 安装成功：{dest}")
    return ok


def _verify(dest, harness):
    problems = []
    # 核心文件
    core = ["SKILL.md",
            "references/need-mining.md",
            "references/prd-template.md",
            "references/workflow-card.md"]
    for f in core:
        if not os.path.isfile(os.path.join(dest, f)):
            problems.append(f"缺少核心文件 {f}")
    # references 全目录（至少 3 页，含新增 2 页）
    ref_dir = os.path.join(dest, "references")
    if os.path.isdir(ref_dir):
        md_files = [x for x in os.listdir(ref_dir) if x.endswith(".md")]
        if len(md_files) < 5:  # need-mining/prd/workflow/token-optimize/review
            problems.append(f"references/ 文件数异常：{len(md_files)}")
    # Codex 必须有 openai.yaml
    if harness == "codex":
        if not os.path.isfile(os.path.join(dest, "agents", "openai.yaml")):
            problems.append("Codex 缺少 agents/openai.yaml")
    # version 一致
    v_skill = read_version(os.path.join(dest, "SKILL.md"))
    if harness == "codex" and os.path.isfile(os.path.join(dest, "agents", "openai.yaml")):
        v_yaml = read_version(os.path.join(dest, "agents", "openai.yaml"))
        if v_skill and v_yaml and v_skill != v_yaml:
            problems.append(f"版本不一致 SKILL.md={v_skill} openai.yaml={v_yaml}")
    # 黑名单必须不存在
    for b in BLACKLIST_DIRS:
        if os.path.exists(os.path.join(dest, b)):
            problems.append(f"误装黑名单目录 {b}/")
    if problems:
        for p in problems:
            log(f"  [校验失败] {p}")
        return False
    log(f"  校验通过：version={v_skill}, 核心文件齐备, 无黑名单")
    return True


def main():
    ap = argparse.ArgumentParser(description="lili-ai-coach 通用安装器")
    ap.add_argument("--src", help="本地仓库目录（离线/测试用），默认从 GitHub 拉")
    ap.add_argument("--target", help="显式安装目录（skills 父目录），跳过探测")
    ap.add_argument("--harness", choices=["workbuddy", "hermes", "codex"],
                    help="目标 harness 类型（影响是否装 openai.yaml）")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不写入")
    args = ap.parse_args()
    install(args)


if __name__ == "__main__":
    main()
