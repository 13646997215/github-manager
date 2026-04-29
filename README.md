# GitHub Manager Pro

GitHub Manager Pro 是一个面向 Ubuntu / Linux 桌面环境的中文 GitHub 文件与仓库管理工具。

它把常见 GitHub 文件操作做成了“既能双击启动，也能命令行自动化”的终端工作台：
- 上传文件 / 文件夹
- 浏览远程仓库目录
- 下载远程文件 / 目录
- 更新远程文件
- 删除远程文件 / 目录
- 本地与远程目录同步（push / pull）
- 仓库创建、查看、克隆、重命名、转移、删除
- 审计日志、同步报告、桌面启动、发布打包

项目特点：
- 中文交互式向导
- 选择器优先，手动输入作为补充
- 适合桌面用户，也适合脚本用户
- 基于 Shell + GitHub CLI + GitHub API，依赖透明、容易维护

--------------------------------------------------
一、适用场景
--------------------------------------------------

适合这些人：
- 想在 Linux 桌面上方便管理 GitHub 文件的人
- 不想总记远程路径、希望用选择器完成操作的人
- 想把 GitHub 文件管理做成可开源、可二次开发、可脚本化工具的人

你可以把它理解成：
“一个面向 GitHub 仓库文件层的中文终端文件管理器”

--------------------------------------------------
二、核心能力
--------------------------------------------------

1. 文件上传
- 支持上传单文件、多文件、整个目录
- 支持拖拽路径启动
- 支持交互式本地文件选择器
- 支持自定义目标仓库、分支、远程目录、提交信息

2. 仓库浏览
- 支持浏览仓库根目录或子目录
- 支持 tree 递归查看
- 交互式模式下支持远程路径浏览器

3. 文件下载
- 支持下载单个文件
- 支持递归下载远程目录
- 可通过选择器或手动输入指定本地保存目录

4. 文件更新
- 基于 GitHub Contents API + SHA 更新远程文件
- 向导模式下只允许选择远程文件，避免误操作

5. 文件删除
- 支持删除单个远程文件
- 支持递归删除远程目录
- 交互模式默认二次确认
- 非交互模式可使用 --force

6. 目录同步
- 支持 push / pull 两种同步模式
- 先拉取远程 manifest，再做本地哈希比对
- 支持 same / local_only / remote_only / conflict 四种状态
- 支持 dry-run
- 支持同步报告导出

7. 仓库管理
- create
- info
- clone
- rename
- transfer
- delete

8. 产品化能力
- 桌面快捷方式
- 启动器
- About 页面
- 首次启动向导
- 结构化审计日志
- release 目录生成

--------------------------------------------------
三、项目结构
--------------------------------------------------

```text
github/
├── README.md                      # 主文档（开源入口）
├── github-manager.sh              # 主入口脚本
├── github-upload.sh               # 快速上传入口
├── GitHubManager.desktop          # 桌面入口
├── install-deps.sh                # 依赖安装脚本
├── assets/
│   └── github-manager.svg         # 项目图标
├── bin/
│   ├── ghm-upload
│   ├── ghm-list
│   ├── ghm-download
│   ├── ghm-delete
│   ├── ghm-update
│   ├── ghm-sync
│   ├── ghm-repo
│   ├── ghm-tui.py
│   └── launch-github-manager.sh
├── config/
│   ├── config.yaml
│   └── themes/
│       └── default.yaml
├── docs/
│   ├── README.md
│   ├── INSTALL.md
│   ├── API.md
│   └── GRADUATION_EDITION.md
├── lib/
│   ├── env.sh
│   ├── common.sh
│   ├── deps.sh
│   ├── auth.sh
│   ├── repos.sh
│   ├── ui.sh
│   ├── files.sh
│   └── bootstrap.sh
└── tests/
    ├── test_basic.sh
    ├── test_interactive_pty.py
    └── test_integration.sh
```

说明：
- release/ 是运行时/发版时动态生成的发布目录，不属于必须保留的源码
- reports/、日志、缓存、__pycache__ 也不属于核心源码
- 历史规划文档已归档到 docs/archive/，方便保留设计背景但不干扰最终用户

--------------------------------------------------
四、依赖要求
--------------------------------------------------

必需依赖：
- gh
- git
- jq
- curl
- python3

推荐可选依赖：
- fzf
- whiptail
- rsync
- script（通常由 util-linux 提供）

安装依赖：

```bash
cd /path/to/github
./install-deps.sh all
```

只安装必需依赖：

```bash
./install-deps.sh required
```

--------------------------------------------------
五、认证方式
--------------------------------------------------

推荐使用 GitHub CLI 登录：

```bash
gh auth login
gh auth status
```

备用方式：Personal Access Token

```bash
mkdir -p ~/.config/github-manager
printf 'YOUR_TOKEN' > ~/.config/github-manager/token
chmod 600 ~/.config/github-manager/token
```

--------------------------------------------------
六、启动方式
--------------------------------------------------

1. 主菜单

```bash
./github-manager.sh menu
```

2. 查看帮助

```bash
./github-manager.sh --help
```

3. 桌面双击
- 直接双击 GitHubManager.desktop
- 会通过 gnome-terminal 打开交互界面

4. 快捷命令

```bash
./bin/ghm-upload
./bin/ghm-list
./bin/ghm-download
./bin/ghm-delete
./bin/ghm-update
./bin/ghm-sync
./bin/ghm-repo
```

--------------------------------------------------
七、交互设计说明
--------------------------------------------------

当前交互原则：
- 优先选择器
- 允许手动输入
- 远程路径、本地路径、仓库名都尽量减少死记硬背

1. 仓库选择方式
进入下载 / 删除 / 更新 / 同步等向导时，会先询问：
- 选择器
- 手动输入 owner/repo
- 取消

2. 本地路径方式
进入上传 / 下载 / 更新 / 同步时，会询问：
- 选择器
- 手动输入本地路径
- 取消

3. 远程路径方式
会提供远程路径向导：
- 浏览当前目录
- 手动输入路径
- 返回仓库根目录
- 取消

4. 远程路径规则
- 浏览/下载/删除：可选文件或目录
- 更新：只允许远程文件
- 同步：优先目录，可直接使用当前目录

--------------------------------------------------
八、常用命令示例
--------------------------------------------------

1. 上传文件 / 目录

```bash
./bin/ghm-upload \
  --repo owner/repo \
  --branch main \
  --remote-path docs \
  --message "upload docs" \
  ./README.md ./docs
```

2. 浏览仓库

```bash
./bin/ghm-list owner/repo
./bin/ghm-list owner/repo docs
./bin/ghm-list owner/repo --tree
```

3. 下载文件或目录

```bash
./bin/ghm-download owner/repo docs/README.md ./downloads
./bin/ghm-download owner/repo docs ./downloads
```

4. 更新远程文件

```bash
./bin/ghm-update owner/repo docs/README.md ./README.md --message "update readme"
```

5. 删除远程文件 / 目录

```bash
./bin/ghm-delete owner/repo docs/old.txt --force
./bin/ghm-delete owner/repo docs/old-folder --force
```

6. 同步 dry-run

```bash
./bin/ghm-sync owner/repo ./local docs --mode push --dry-run --report ./reports/push.txt
./bin/ghm-sync owner/repo ./local docs --mode pull --dry-run --report ./reports/pull.txt
```

7. 仓库管理

```bash
./bin/ghm-repo info owner/repo
./bin/ghm-repo create demo-repo --public --description "demo"
./bin/ghm-repo clone owner/repo ./repo-copy
./bin/ghm-repo rename owner/repo new-name
./bin/ghm-repo transfer owner/repo new-owner [new-name]
./bin/ghm-repo delete owner/repo --force
```

--------------------------------------------------
九、日志与输出目录
--------------------------------------------------

运行时会使用这些目录：
- 审计日志：~/.local/state/github-manager/audit.log
- 运行日志：~/.local/state/github-manager/github-manager.log
- 桌面启动日志：~/.local/state/github-manager/desktop-launch.log
- 同步报告目录：./reports
- 发布目录：./release

说明：
- 这些目录大部分是运行产物，不建议作为源码提交
- release/ 应该在发版时生成，而不是长期带着构建产物一起提交

--------------------------------------------------
十、测试
--------------------------------------------------

1. 基础测试

```bash
bash tests/test_basic.sh
```

2. 交互 PTY 测试

```bash
python3 tests/test_interactive_pty.py
```

3. 完整 GitHub E2E 测试

```bash
bash tests/test_integration.sh 13646997215/github-manager
```

--------------------------------------------------
十一、开源发布建议
--------------------------------------------------

建议提交到 GitHub 仓库时：
- 保留源码、文档、测试、配置、图标
- 不提交 __pycache__
- 不提交运行时日志
- 不提交 reports/
- 不提交 release/
- 不提交临时缓存
- 保留 docs/archive/ 中的历史规划文档作为开发背景（可选）

建议额外补充：
- .gitignore
- LICENSE
- CHANGELOG（可选）
- docs/archive/（放历史规划文档，可保留开发背景但不打扰最终用户）

--------------------------------------------------
十二、已知设计取向
--------------------------------------------------

这个项目的设计目标不是“最短命令”，而是：
- 桌面可用
- 中文友好
- 交互明确
- 操作安全
- 同时兼容 CLI 自动化

所以它会比单纯的 gh api 命令更偏产品化。

如果你要继续增强，后续最值得做的方向有：
- 更强的远程多级目录浏览器
- 更完整的 .gitignore / LICENSE / issue template
- 更丰富的错误码与 JSON 输出模式
- 更正式的 release 版本流程
