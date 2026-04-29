# 安装指南

系统要求
- Ubuntu / Debian
- bash 4+
- Python 3（用于同步对比、图标/报告辅助）

必需依赖
- gh
- git
- jq
- curl

可选依赖
- fzf
- whiptail
- rsync
- script（推荐，用于桌面启动时提供稳定伪终端）

安装步骤
1. 进入项目目录
   `cd /home/hanhan/Desktop/github`

2. 安装依赖
   `./install-deps.sh all`

3. 授予执行权限
   `chmod +x github-manager.sh github-upload.sh install-deps.sh bin/* tests/*.sh`

4. GitHub 认证
   推荐：
   `gh auth login`

5. 桌面快捷方式
   - 桌面入口：`~/Desktop/GitHubManager.desktop`
   - 双击即可启动交互界面

6. 安装命令到 ~/.local/bin（可选）
   `./github-manager.sh install --with-desktop`

7. 生成发布目录（答辩展示用）
   `./github-manager.sh release`

8. 验证安装
   `./github-manager.sh --help`
   `./github-manager.sh about`
   `./github-manager.sh audit`

关键路径
- 审计日志：`~/.local/state/github-manager/audit.log`
- 报告目录：`/home/hanhan/Desktop/github/reports`
- 发布目录：`/home/hanhan/Desktop/github/release`

故障排查
1. 桌面双击没反应
   - 检查 `~/Desktop/GitHubManager.desktop` 是否可执行且 trusted
2. sync 报 conflict
   - 说明本地与远程同路径内容不同，先手动处理冲突后再同步
3. about/release 不可用
   - 确认正在使用最新的 `github-manager.sh`
