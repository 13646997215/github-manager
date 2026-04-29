# GitHub 文件管理脚本 - 完整实现规划

## 📋 项目概述
创建一个交互式GitHub文件管理工具，支持：
- **第一版**：本地文件/文件夹选择 → 上传到GitHub仓库
- **第二版**：完整的仓库文件管理（上传、下载、删除、更新、查看）

---

## 🎯 核心设计原则

### 1. 交互方式
- **拖拽支持**：`./github-upload.sh /path/to/file` 直接上传
- **交互式选择**：无参数运行时，启动交互式菜单
- **多文件支持**：同时选择多个文件/文件夹

### 2. 认证方式
- **首选**：GitHub CLI (`gh`) 浏览器登录（最安全便捷）
- **备选**：Personal Access Token (PAT) 配置
- **自动检测**：优先使用gh，未安装则引导安装或使用PAT

### 3. 技术栈
- **Shell脚本**：主程序框架（兼容性最好）
- **GitHub CLI**：认证、仓库列表、API调用
- **fzf**：交互式选择（可选，没有则用简单文本菜单）
- **curl/jq**：API调用和JSON处理

---

## 📁 项目结构

```
/home/hanhan/Desktop/github/
├── github-manager.sh              # 主入口脚本（第一版 + 第二版入口）
├── github-upload.sh               # 第一版：快速上传脚本（拖拽友好）
├── lib/
│   ├── auth.sh                    # 认证管理模块
│   ├── repos.sh                   # 仓库操作模块
│   ├── files.sh                   # 文件操作模块
│   └── ui.sh                      # 交互界面模块
├── config/
│   ├── config.yaml                # 用户配置（PAT、默认仓库等）
│   └── themes/                    # UI主题（可选）
├── bin/
│   ├── ghm-upload                 # 编译后的快速上传命令
│   ├── ghm-list                   # 列出仓库文件
│   ├── ghm-download               # 下载文件
│   ├── ghm-delete                 # 删除文件
│   └── ghm-sync                   # 同步文件夹
├── docs/
│   ├── README.md                  # 使用说明
│   ├── INSTALL.md                 # 安装指南
│   └── API.md                     # API文档
├── tests/                         # 测试脚本
├── .env.example                   # 环境变量模板
└── .gitignore

```

---

## 🔐 认证方案设计

### 方案A：GitHub CLI 推荐（首选）
```bash
# 1. 安装 GitHub CLI
sudo apt install gh   # Ubuntu/Debian

# 2. 浏览器登录（脚本自动检测和引导）
gh auth login
# → 选择 GitHub.com
# → 选择 HTTPS
# → 选择 "Login with a web browser"
# → 复制代码，在浏览器中完成验证

# 3. 脚本中调用
gh repo view          # 测试认证
gh repo list          # 获取仓库列表
```

**优点**：
- 安全（OAuth token自动管理）
- 支持双因素认证
- Token自动续期
- 提供完整API和git操作

### 方案B：Personal Access Token（备选）
```bash
# 1. 用户手动生成PAT（repo权限）
# 2. 保存到 ~/.config/github-manager/token
# 3. 脚本读取使用
```

**脚本检测逻辑**：
```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
    USE_GH_CLI=true
elif [ -f "$CONFIG_DIR/token" ]; then
    USE_PAT=true
    export GITHUB_TOKEN=$(cat "$CONFIG_DIR/token")
else
    # 引导用户安装/配置
    install_github_cli
fi
```

---

## 🎮 第一版实现：快速上传

### 功能流程
```
启动脚本
    ↓
检测认证 → 未配置? → 引导安装gh并登录
    ↓
选择文件/文件夹
    ├─ 拖拽路径参数 → 直接使用
    └─ 无参数 → 交互式选择（fzf或菜单）
    ↓
选择目标仓库
    ├─ 获取用户所有仓库（gh repo list）
    └─ 交互式选择
    ↓
选择分支（默认main）
    ↓
确认上传信息
    ↓
执行上传：
    ├─ 临时克隆仓库到/tmp
    ├─ 复制文件到对应位置
    ├─ git add/commit/push
    └─ 清理临时目录
    ↓
显示结果（成功/失败）
```

### 交互式文件选择
**方式1：fzf（推荐，需安装）**
```bash
# 递归查找当前目录所有文件
find . -type f | fzf --multi --prompt="选择文件: "
```

**方式2：simple_menu（无需额外依赖）**
```bash
# 使用whiptail或dialog（已安装）
# 或使用简单的数字菜单
```

**方式3：拖拽支持**
```bash
# 终端拖拽文件，路径作为参数传入
./github-upload.sh /home/user/file.txt
```

### 上传策略
**策略1：直接Git操作**（推荐）
```bash
tmpdir=$(mktemp -d)
git clone "https://github.com/user/repo.git" "$tmpdir" --depth=1
cp -r "$selected_files" "$tmpdir/"
cd "$tmpdir"
git add .
git commit -m "Upload via github-manager"
git push origin main
rm -rf "$tmpdir"
```

**策略2：GitHub API上传**（单文件小文件）
```bash
# 使用 gh api 或 curl 直接创建/更新文件
# 适合小文件，大文件还是用git
```

---

## 🚀 第二版实现：完整仓库管理

### 功能模块

#### 1. 文件浏览 (`ghm-list`)
```
功能：
- 列出仓库根目录或指定路径的文件
- 显示文件大小、修改时间、类型
- 支持递归浏览子目录

命令：
ghm-list <repo> [path] [--tree]

实现：
gh api repos/:owner/:repo/contents/:path \
  -H "Accept: application/vnd.github.v3+json"
```

#### 2. 文件上传 (`ghm-upload`)
```
功能：
- 单文件/多文件上传
- 文件夹递归上传
- 自定义提交信息
- 选择分支

命令：
ghm-upload <repo> <file1> [file2...] [--message "msg"]

交互模式：
ghm-upload
→ 选择仓库
→ 选择文件
→ 输入提交信息
→ 确认上传
```

#### 3. 文件下载 (`ghm-download`)
```
功能：
- 下载单个文件
- 下载整个文件夹（递归）
- 指定保存位置

命令：
ghm-download <repo> <path> [save_to]

实现：
gh api repos/:owner/:repo/contents/:path \
  -H "Accept: application/vnd.github.v3+json" | jq -r .content | base64 -d > file
```

#### 4. 文件删除 (`ghm-delete`)
```
功能：
- 删除文件
- 删除文件夹（递归）
- 确认提示（防止误删）

命令：
ghm-delete <repo> <path> [--force]

实现：使用 GitHub API DELETE /repos/:owner/:repo/contents/:path
需要提供当前文件SHA
```

#### 5. 文件更新 (`ghm-update`)
```
功能：
- 更新现有文件（新版本）
- 自动检测冲突
- 强制覆盖

命令：
ghm-update <repo> <file> [new_file]

实现：上传前获取SHA，使用PUT API
```

#### 6. 同步文件夹 (`ghm-sync`)
```
功能：
- 本地文件夹 ↔ 远程仓库双向同步
- 智能比对（新增、修改、删除）
- 预览模式（dry-run）

命令：
ghm-sync <repo> <local_dir> [remote_path]

实现：
1. 获取远程文件列表（API）
2. 比对本地文件（哈希）
3. 生成操作清单
4. 用户确认后执行
```

#### 7. 仓库管理 (`ghm-repo`)
```
功能：
- 创建新仓库
- 删除仓库（需确认）
- 查看仓库信息
- 克隆仓库
- 重命名/转移仓库

命令：
ghm-repo create <name> [--private|--public]
ghm-repo delete <repo> [--force]
ghm-repo info <repo>
```

---

## 🎨 交互界面设计

### 主菜单结构
```
┌─ GitHub Manager ──────────────────────┐
│                                        │
│  1. 🚀 快速上传文件/文件夹             │
│  2. 📋 浏览仓库文件                    │
│  3. ⬇️  下载文件                       │
│  4. 🗑️  删除文件                       │
│  5. ✏️  更新文件                       │
│  6. 🔄 同步文件夹                      │
│  7. 📦 仓库管理                        │
│  8. ⚙️  设置                           │
│  9. ❌ 退出                           │
│                                        │
└────────────────────────────────────────┘
请选择 (1-9)：
```

### 子菜单示例：快速上传
```
┌─ 快速上传 ────────────────────────────┐
│                                        │
│  选择文件/文件夹：                    │
│  [ ] file1.txt                        │
│  [x] folder/                          │
│  [ ] image.png                        │
│                                        │
│  目标仓库：my-awesome-project         │
│  分支：main ✓                         │
│  提交信息：Upload files               │
│                                        │
│  [确认上传]  [返回]                   │
└────────────────────────────────────────┘
```

---

## 🛠️ 依赖检查与安装

### 必需依赖
| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `gh` | GitHub CLI（认证+API） | `sudo apt install gh` |
| `git` | Git操作 | `sudo apt install git` |
| `jq` | JSON处理 | `sudo apt install jq` |
| `curl` | HTTP请求 | `sudo apt install curl` |

### 可选依赖（增强体验）
| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `fzf` | 模糊搜索选择 | `sudo apt install fzf` |
| `dialog`/`whiptail` | 图形化菜单 | `sudo apt install dialog` |
| `rsync` | 高效同步 | `sudo apt install rsync` |

### 自动安装脚本
```bash
#!/bin/bash
# install-deps.sh
deps=("gh" "git" "jq" "curl")
for dep in "${deps[@]}"; do
    if ! command -v $dep &>/dev/null; then
        echo "安装 $dep..."
        sudo apt update && sudo apt install -y $dep
    fi
done
```

---

## 📝 详细实现计划（分阶段）

### Phase 1：基础架构搭建（第1天）
- [ ] 创建项目目录结构
- [ ] 编写依赖检查和安装脚本
- [ ] 实现认证模块（auth.sh）
  - 检测gh是否安装
  - 检测gh是否已登录
  - 未登录则引导登录
  - 备选PAT配置
- [ ] 实现仓库列表获取（repos.sh）
  - `get_repos()` 函数
  - 缓存机制（避免频繁API调用）
  - 分页处理（用户仓库多的情况）

### Phase 2：第一版核心功能（第2-3天）
- [ ] 实现文件选择模块（ui.sh）
  - 参数检测（拖拽路径）
  - 交互式文件选择（支持多选）
  - 文件夹递归选择
- [ ] 实现上传核心逻辑（files.sh）
  - 临时克隆仓库
  - 文件复制
  - git commit & push
  - 错误处理和回滚
- [ ] 编写快速上传脚本（github-upload.sh）
  - 单文件直接上传
  - 多文件交互式选择
- [ ] 编写主菜单脚本（github-manager.sh）
  - 主菜单循环
  - 各功能入口

### Phase 3：测试与优化（第4天）
- [ ] 边界情况测试
  - 大文件上传（>100MB）
  - 特殊字符文件名
  - 无网络情况
  - 认证过期
- [ ] 用户体验优化
  - 进度显示
  - 颜色输出
  - 错误提示友好化
- [ ] 编写使用文档

### Phase 4：第二版扩展功能（第5-7天）
- [ ] 文件浏览功能（ghm-list）
  - 目录树显示
  - 文件元信息展示
- [ ] 文件下载功能（ghm-download）
  - 单文件下载
  - 文件夹递归下载
- [ ] 文件删除功能（ghm-delete）
  - 安全确认机制
  - 批量删除支持
- [ ] 文件更新功能（ghm-update）
  - SHA检测
  - 冲突处理
- [ ] 同步功能（ghm-sync）
  - 双向同步算法
  - 增量同步
  - dry-run模式

### Phase 5：高级功能（可选）
- [ ] 仓库管理（ghm-repo）
  - 创建/删除/重命名仓库
  - 仓库设置修改
- [ ] 配置文件系统
  - 默认分支设置
  - 默认仓库选择
  - 快捷键绑定
- [ ] 日志系统
  - 操作记录
  - 错误日志
  - 审计追踪
- [ ] GUI版本（Python + Tkinter/Qt）
  - 图形化文件浏览器
  - 拖拽上传界面

---

## 🔒 安全与错误处理

### 安全措施
1. **Token保护**
   - 配置文件权限 `chmod 600 ~/.config/github-manager/token`
   - 不在日志中打印敏感信息
   - 内存中及时清除

2. **操作确认**
   - 删除操作强制确认
   - 覆盖文件二次确认
   - 危险操作记录日志

3. **网络安全**
   - 验证SSL证书
   - API调用超时处理
   - 失败重试机制

### 错误处理策略
```bash
# 统一错误处理函数
handle_error() {
    local error_code=$1
    local message=$2

    case $error_code in
        AUTH_FAILED)
            echo "❌ 认证失败，请重新登录：gh auth login"
            ;;
        NETWORK_ERROR)
            echo "❌ 网络错误，请检查网络连接"
            ;;
        RATE_LIMIT)
            echo "⚠️  API限制，请稍后再试"
            ;;
        PERMISSION_DENIED)
            echo "❌ 权限不足，请检查仓库权限"
            ;;
        *)
            echo "❌ 错误：$message"
            ;;
    esac
    exit 1
}
```

---

## 🎯 使用示例

### 示例1：拖拽上传
```bash
# 在文件管理器拖动文件到终端
./github-upload.sh ~/Documents/report.pdf
# → 自动选择最近使用的仓库
# → 确认后上传
```

### 示例2：交互式上传多个文件
```bash
$ ./github-upload.sh
正在检测认证... ✓

选择要上传的文件（空格多选，Enter确认）：
  1. docs/README.md
  2. src/main.py
  3. images/logo.png
  4. data/sample.csv

选择目标仓库：
>  my-awesome-project
  another-repo
  test-repo

分支：main
提交信息：Add new files

确认上传？[Y/n]
```

### 示例3：查看仓库文件
```bash
$ ghm-list my-awesome-project
📁 docs/
   📄 README.md       (2.3 KB)
   📄 GUIDE.md        (5.1 KB)
📁 src/
   📄 main.py         (12 KB)
   📄 utils.py        (8 KB)
📄 LICENSE           (1.1 KB)
```

### 示例4：同步本地文件夹
```bash
$ ghm-sync my-project ./local-folder/
🔍 比对中...
  ✓ 新增：3个文件
  ✗ 删除：1个文件（远程）
  ~ 修改：2个文件

执行操作？[Y/n]
  [1] 上传新增文件
  [2] 删除远程多余文件
  [3] 更新修改的文件
```

---

## 📊 项目时间线

```
Day 1-2  : 基础架构 + 认证 + 仓库列表
Day 3-4  : 第一版上传功能 + 测试
Day 5-6  : 第二版浏览/下载/删除
Day 7    : 同步功能 + 文档完善
Total    : ~1周时间
```

---

## 🎓 学习资源

### GitHub API文档
- REST API v3: https://docs.github.com/en/rest
- 认证：https://docs.github.com/en/rest/overview/other-authentication-methods
- 内容API：https://docs.github.com/en/rest/repos/contents

### GitHub CLI文档
- 官方文档：https://cli.github.com/manual/
- 仓库命令：`gh repo --help`
- API调用：`gh api --help`

---

## 🚦 现在开始执行！

哥哥，予渡已经规划好啦~ 这个方案你觉得怎么样？有什么需要调整的吗？

如果没有问题，予渡就开始按照 **Phase 1 → Phase 2** 的顺序实现啦！

首先从：
1. 创建项目目录
2. 实现依赖检查
3. 实现认证模块

让予渡开始工作吧！(๑>◡<๑)
