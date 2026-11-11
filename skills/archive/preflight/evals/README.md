# Preflight evals

34 个用例，每个分别运行 `with_skill` 和 `without_skill`，共 68 次执行。每个用例使用独立临时夹具目录；运行完成后保存回复、工具记录、文件变化和工作区副本。

从仓库根目录运行：

```bash
# 本地回归检查，不请求模型
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills-pi/preflight/evals/scripts -p 'test_*.py' -v

# 先用三例验证查询、计划写入、失败后修订
PYTHONDONTWRITEBYTECODE=1 python3 skills-pi/preflight/evals/scripts/run_evals.py skills/plan/preflight/evals/iteration-1 --only 2,27,31 --jobs 3
PYTHONDONTWRITEBYTECODE=1 python3 skills-pi/preflight/evals/scripts/grade_evals.py skills/plan/preflight/evals/iteration-1 --only 2,27,31 --jobs 3

# 全量执行：已成功且输入一致的三例会自动跳过
PYTHONDONTWRITEBYTECODE=1 python3 skills-pi/preflight/evals/scripts/run_evals.py skills/plan/preflight/evals/iteration-1 --jobs 8
PYTHONDONTWRITEBYTECODE=1 python3 skills-pi/preflight/evals/scripts/grade_evals.py skills/plan/preflight/evals/iteration-1 --jobs 6
```

执行模型默认 `auto/deepseek-v4.1-flash`，评分模型默认 `xhy-api/gpt-6.1-sol`，均可用 `--model` 覆盖。需要本机已经配置好 Pi 的模型和凭据。两阶段都支持 `--only id,id` 和 `--timeout 秒`；超时默认分别为 900 秒和 600 秒。

`with_skill` 只提供 preflight：`explicit: true` 的用例强制调用，其余用例验证自动选择技能。`without_skill` 禁用技能，并移除模拟历史中的 `/skill:preflight`。两组均禁用扩展、MCP、全局 AGENTS/CLAUDE 上下文和提示模板，工具集合保持一致。

依赖和缓存目录 `node_modules`、`.git`、`.venv`、`__pycache__` 不计入源码变更，也不复制到 `workspace-after/`。安装过程仍保留在工具记录中；`package.json` 和锁文件照常作为证据。评分输入会明确列出排除目录；对旧记录，另列原始变更清单中排除的文件数量。

每次执行以 `status.json` 的 `success` 为成功依据。非零退出码、超时、模型错误、输出不完整都会标记失败、保存日志，且整批命令以非零状态退出。失败或旧格式的结果可以直接重跑；成功结果的用例、模型、夹具或技能内容变化时，应使用新的 `iteration-N` 目录。

评分只接收成功执行，使用执行时保存的用例断言和实际 prompt。回复、工具记录和变更文件内容完整传入，不静默截断。模型必须按原顺序返回每一条断言的原文、JSON 布尔值和证据；无效结果最多重试三次，之后保存失败状态，不产生分数。每次评分调用的 stdout/stderr 单独保存。`[auto]` 表示需要文件证据的断言，当前仍由评分模型判断，不代表独立的确定性检查。

每个 `eval-<id>-<name>/<config>/run-1/` 目录中：

- `input.json`：用例、实际 prompt、模型和输入指纹。
- `status.json`、`stderr.log`、`events.jsonl`：执行状态与原始日志。
- `outputs/response.md`、`outputs/files/`：最终回复与新增/修改文件。
- `workspace-after/`、`changes.json`、`transcript.md`：工作区副本、变更清单和完整工具记录。
- `timing.json`、`metrics.json`：执行时间、token 和工具调用计数。
- `grading.json`、`grading-status.json`、`grading-input.json`、`grader-attempt-*`：评分、状态、证据与调用日志。

评分不自动更改技能或断言。比较两组时，应逐例审查证据，并将基础设施失败与技能表现分开统计。

`events.jsonl`（原始事件流）和运行中安装的 `node_modules/` 只保留在本地，不进入 git；评分所需的回复、工具记录与变更文件均已单独保存。

二进制变更文件（如 .pptx、.pdf、.png）只以路径、大小和哈希交给评分模型，不按文本解码；文本文件照常完整传入。
