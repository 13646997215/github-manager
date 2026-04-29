# GitHub Manager Pro API / CLI 文档

## 全局约定

所有命令都在项目根目录 `/home/hanhan/Desktop/github` 下执行，或通过 `./bin/ghm-*` 封装执行。

通用参数：

- `--repo owner/repo`：指定仓库，主要用于 upload/list/download/update/delete/sync。
- `--branch BRANCH`：指定分支；不指定时读取仓库默认分支，缺省回退到 main。
- `--remote-path PATH`：仓库内远程相对路径。
- `--message MSG`：提交信息。
- `--help` / `-h`：显示子命令帮助。

## github-manager.sh

```bash
./github-manager.sh menu
./github-manager.sh upload|quick-upload [options] <file_or_dir>...
./github-manager.sh list <repo> [remote_path] [--tree]
./github-manager.sh download <repo> <remote_path> <save_to>
./github-manager.sh delete <repo> <remote_path> [--force]
./github-manager.sh update <repo> <remote_path> <local_file>
./github-manager.sh sync <repo> <local_dir> [remote_path] [--mode push|pull] [--dry-run] [--report FILE]
./github-manager.sh repo <create|delete|info|clone|rename|transfer> ...
./github-manager.sh install [--local-bin DIR] [--with-desktop]
./github-manager.sh settings
./github-manager.sh about
./github-manager.sh audit
./github-manager.sh release
```

## ghm-upload

```bash
./bin/ghm-upload [--repo owner/repo] [--remote-path PATH] [--branch BRANCH] [--message MSG] <file_or_dir>...
```

行为：

1. 检查认证和依赖。
2. 克隆目标仓库到临时目录。
3. 复制文件或目录到远程路径。
4. git add/commit/push。
5. 清理临时目录并写入审计日志。

## ghm-list

```bash
./bin/ghm-list <repo> [remote_path] [--tree] [--branch BRANCH]
```

普通模式使用 Contents API 列出指定目录；`--tree` 使用 Git Tree API 递归展示。

## ghm-download

```bash
./bin/ghm-download <repo> <remote_path> <save_to> [--branch BRANCH]
```

远程路径是文件时下载到 `save_to/basename(remote_path)`；远程路径是目录时递归下载。

## ghm-delete

```bash
./bin/ghm-delete <repo> <remote_path> [--force] [--branch BRANCH] [--message MSG]
```

支持文件和目录递归删除。交互模式会确认；自动化测试或脚本可使用 `--force`。

## ghm-update

```bash
./bin/ghm-update <repo> <remote_path> <local_file> [--branch BRANCH] [--message MSG]
```

先获取远程文件 SHA，再通过 Contents API PUT 更新内容。

## ghm-sync

```bash
./bin/ghm-sync <repo> <local_dir> [remote_path] [--mode push|pull] [--dry-run] [--report FILE]
```

同步算法：

1. 生成本地 manifest。
2. 获取远程 Git Tree manifest。
3. 下载远程目标文件到临时目录。
4. SHA256 对比，生成 same/local_only/remote_only/conflict。
5. 输出摘要并写报告。
6. dry-run 停在预览；真实执行时遇到 conflict 会阻止。

push：上传 local_only，删除 remote_only，conflict 阻止。
pull：下载 remote_only，删除 local_only，conflict 阻止。

## ghm-repo

```bash
./bin/ghm-repo create <name> [--public|--private] [--description MSG] [--homepage URL] [--disable-issues] [--disable-wiki] [--clone] [--team TEAM]
./bin/ghm-repo delete <owner/repo> [--force]
./bin/ghm-repo info <owner/repo>
./bin/ghm-repo clone <owner/repo> [target]
./bin/ghm-repo rename <owner/repo> <new-name>
./bin/ghm-repo transfer <owner/repo> <new-owner> [new-name]
```

## 认证与账号切换

优先 GitHub CLI：

```bash
gh auth login
gh auth status
```

备选 PAT：

```bash
mkdir -p ~/.config/github-manager
printf 'YOUR_TOKEN' > ~/.config/github-manager/token
chmod 600 ~/.config/github-manager/token
```

交互式账号入口：

```text
./github-manager.sh menu
主菜单 -> 账号/设置 -> 账号切换/登录
```

该入口支持查看当前账号、切换 gh 登录账号、重新登录 gh、配置 PAT、清除 PAT。切换账号后会自动清空仓库缓存。

## 测试命令

```bash
./tests/test_basic.sh
./tests/test_integration.sh 13646997215/github-manager-test main
```
