# 接口包

[![主仓 FinshinImpact](https://img.shields.io/badge/主仓-FinshinImpact-blue.svg)](https://github.com/lym2006/FinshinImpact)

插件与适配器共用的那一包：契约基类、领域词表、数据形状、异常族与命令绑定，本体与外部件同时读这一份。

## 放在哪儿

本仓不单独开发。先 clone 主仓 `FinshinImpact`，再把本仓 clone 进它的 `finshin/sdk`，改动在那棵目录里做，代码在 `src` 那一层，声明按 `package-dir` 把它映射成包名。

改完生效跑 `.venv\Scripts\uv.exe sync --all-packages --reinstall-package finshin-sdk`，普通 sync 不重装子仓那棵。

## 跑法

```powershell
# 在主仓根执行
python -m pytest devtools/tests/test_public_pieces.py devtools/tests/test_command_bind.py
```

本仓不带用例，门面代发与命令绑定由主仓那棵树里的用例覆盖，全量口径见主仓 `docs/testing.md`。

## 规范归主仓

- 挂载、更新与摘掉见 [docs/development.md](https://github.com/lym2006/FinshinImpact/blob/main/docs/development.md) 的「挂载子仓」一节。
- 接口包对外该放什么、不放什么见同一文件的「新增平台适配器」一节。
- 构建、tag 与 release 附件见 [docs/release-workflow.md](https://github.com/lym2006/FinshinImpact/blob/main/docs/release-workflow.md) 的「子仓供件」一节。
- 编码规范见 [docs/coding-style.md](https://github.com/lym2006/FinshinImpact/blob/main/docs/coding-style.md)，静态检查与豁免见 [docs/style-checker.md](https://github.com/lym2006/FinshinImpact/blob/main/docs/style-checker.md)。
- 本仓不另立一套规范。
