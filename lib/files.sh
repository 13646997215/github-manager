#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/ui.sh"

api_get_contents() {
  local repo="$1"
  local path="$2"
  local ref="${3:-}"
  local endpoint="repos/$repo/contents"
  [[ -n "$path" ]] && endpoint+="/$path"
  [[ -n "$ref" ]] && endpoint+="?ref=$ref"
  run_gh_api "$endpoint"
}

api_get_git_tree() {
  local repo="$1"
  local branch="$2"
  run_gh_api "repos/$repo/git/trees/$branch?recursive=1"
}

list_remote_files() {
  local repo="$1"
  local path="${2:-}"
  local branch="${3:-}"
  api_get_contents "$repo" "$path" "$branch" | jq -r '
    if type == "array" then
      .[] | [.type, .path, (.size // 0), (.sha // ""), (.download_url // "")] | @tsv
    else
      [.type, .path, (.size // 0), (.sha // ""), (.download_url // "")] | @tsv
    end'
}

list_remote_tree() {
  local repo="$1"
  local branch="${2:-$DEFAULT_BRANCH}"
  api_get_git_tree "$repo" "$branch" | jq -r '.tree[] | [.type, .path, (.size // 0), (.sha // "")] | @tsv'
}

clone_repo_temp() {
  local repo="$1"
  local branch="$2"
  local tmpdir default_branch clone_args=()
  tmpdir="$(with_temp_dir clone)"
  progress "临时克隆仓库 $repo#$branch" >&2
  if [[ -n "$branch" ]]; then
    clone_args=(-- --depth=1 --branch "$branch")
  fi
  if ! gh repo clone "$repo" "$tmpdir" "${clone_args[@]}" >/dev/null 2>&1; then
    default_branch="$(gh repo view "$repo" --json defaultBranchRef --jq '.defaultBranchRef.name // empty' 2>/dev/null || true)"
    if [[ -n "$default_branch" && "$default_branch" != "$branch" ]]; then
      progress "主分支回退为 $default_branch，重新克隆 $repo" >&2
      gh repo clone "$repo" "$tmpdir" -- --depth=1 --branch "$default_branch" >/dev/null 2>&1 || die "克隆仓库失败：$repo"
    else
      gh repo clone "$repo" "$tmpdir" >/dev/null 2>&1 || die "克隆仓库失败：$repo"
    fi
  fi
  printf '%s\n' "$tmpdir"
}

copy_path_into_repo() {
  local source_path="$1"
  local repo_dir="$2"
  local remote_path="$3"
  local target_dir="$repo_dir"
  [[ -n "$remote_path" ]] && target_dir="$repo_dir/$remote_path"
  mkdir -p "$target_dir"
  if [[ -d "$source_path" ]]; then
    cp -a "$source_path/." "$target_dir/"
  else
    cp -a "$source_path" "$target_dir/$(basename "$source_path")"
  fi
}

warn_large_files() {
  local path
  for path in "$@"; do
    if [[ -f "$path" ]]; then
      local size_mb
      size_mb="$(python3 - <<'PY' "$path"
import os,sys
print(os.path.getsize(sys.argv[1]) / 1024 / 1024)
PY
)"
      if ! python3 - <<'PY' "$size_mb" "$MAX_FILE_SIZE_WARN_MB"
import sys
size=float(sys.argv[1]); limit=float(sys.argv[2])
raise SystemExit(0 if size <= limit else 1)
PY
      then
        warn "文件 $path 超过 ${MAX_FILE_SIZE_WARN_MB}MB，GitHub 普通上传可能失败"
      fi
    fi
  done
}

normalize_remote_path() {
  local path="${1:-}"
  path="${path#/}"
  path="${path%/}"
  printf '%s\n' "$path"
}

remote_join() {
  local base
  base="$(normalize_remote_path "${1:-}")"
  local child="${2:-}"
  if [[ -z "$base" ]]; then
    printf '%s\n' "$child"
  else
    printf '%s/%s\n' "$base" "$child"
  fi
}

get_remote_manifest() {
  local repo="$1"
  local remote_root
  remote_root="$(normalize_remote_path "${2:-}")"
  local branch="$3"
  list_remote_tree "$repo" "$branch" | awk -F'\t' '$1=="blob" {print $2}' | while IFS= read -r path; do
    if [[ -z "$remote_root" ]]; then
      printf '%s\n' "$path"
    elif [[ "$path" == "$remote_root" || "$path" == "$remote_root/"* ]]; then
      local rel="${path#${remote_root}/}"
      [[ "$rel" == "$path" ]] && rel=""
      [[ -n "$rel" ]] && printf '%s\n' "$rel"
    fi
  done | sort -u
}

get_local_manifest() {
  local local_dir="$1"
  (cd "$local_dir" && find . -type f ! -path './.git/*' -printf '%P\n' | sort)
}

get_file_sha256() {
  sha256sum "$1" | awk '{print $1}'
}

compare_sync_state() {
  local repo="$1"
  local local_dir="$2"
  local remote_root="$3"
  local branch="$4"
  local tmpdir
  tmpdir="$(with_temp_dir compare)"
  mkdir -p "$tmpdir/remote" "$tmpdir/local"

  get_local_manifest "$local_dir" > "$tmpdir/local_manifest"
  get_remote_manifest "$repo" "$remote_root" "$branch" > "$tmpdir/remote_manifest"

  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    local src="$local_dir/$rel"
    local dest="$tmpdir/local/$rel"
    mkdir -p "$(dirname "$dest")"
    cp -a "$src" "$dest"
  done < "$tmpdir/local_manifest"

  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    local target="$tmpdir/remote/$rel"
    mkdir -p "$(dirname "$target")"
    download_file "$repo" "$(remote_join "$remote_root" "$rel")" "$target" "$branch" >/dev/null
  done < "$tmpdir/remote_manifest"

  local report="$tmpdir/report.tsv"
  python3 - <<'PY' "$tmpdir/local_manifest" "$tmpdir/remote_manifest" "$tmpdir/local" "$tmpdir/remote" "$report"
import hashlib, pathlib, sys
local_manifest = pathlib.Path(sys.argv[1]).read_text().splitlines()
remote_manifest = pathlib.Path(sys.argv[2]).read_text().splitlines()
local_root = pathlib.Path(sys.argv[3])
remote_root = pathlib.Path(sys.argv[4])
out = pathlib.Path(sys.argv[5])

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

all_paths = sorted(set([p for p in local_manifest if p]) | set([p for p in remote_manifest if p]))
rows = []
for rel in all_paths:
    lp = local_root / rel
    rp = remote_root / rel
    has_local = lp.exists()
    has_remote = rp.exists()
    if has_local and has_remote:
        state = 'same' if sha(lp) == sha(rp) else 'conflict'
    elif has_local:
        state = 'local_only'
    else:
        state = 'remote_only'
    rows.append(f"{state}\t{rel}")
out.write_text("\n".join(rows) + ("\n" if rows else ""))
PY
  cat "$report"
  cleanup_dir "$tmpdir"
}

print_sync_plan() {
  local report="$1"
  local action="$2"
  printf '同步模式: %s\n' "$action"
  printf '%s\n' "$report" | awk -F'\t' '
    BEGIN {same=0; local_only=0; remote_only=0; conflict=0}
    $1=="same" {same++}
    $1=="local_only" {local_only++}
    $1=="remote_only" {remote_only++}
    $1=="conflict" {conflict++}
    END {
      printf "  相同: %d\n  仅本地: %d\n  仅远程: %d\n  冲突: %d\n", same, local_only, remote_only, conflict
    }'
  printf '%s\n' "$report" | while IFS=$'\t' read -r state rel; do
    case "$state" in
      local_only) printf '  + 上传 %s\n' "$rel" ;;
      remote_only) printf '  - 远程新增 %s\n' "$rel" ;;
      conflict) printf '  ! 冲突 %s\n' "$rel" ;;
    esac
  done
}

upload_single_file_to_remote() {
  local repo="$1"
  local branch="$2"
  local local_file="$3"
  local remote_file="$4"
  local commit_message="$5"
  local sha
  sha="$(resolve_remote_sha "$repo" "$remote_file" "$branch" || true)"
  local payload
  if [[ -n "$sha" ]]; then
    payload="$(jq -n --arg message "$commit_message" --arg content "$(base64_file "$local_file")" --arg branch "$branch" --arg sha "$sha" '{message:$message, content:$content, branch:$branch, sha:$sha}')"
  else
    payload="$(jq -n --arg message "$commit_message" --arg content "$(base64_file "$local_file")" --arg branch "$branch" '{message:$message, content:$content, branch:$branch}')"
  fi
  gh api --method PUT "repos/$repo/contents/$remote_file" --input - <<< "$payload" >/dev/null
}

stage_upload_files() {
  local repo_dir="$1"
  local remote_path="$2"
  shift 2
  local file
  for file in "$@"; do
    [[ -e "$file" ]] || die "本地路径不存在：$file"
    copy_path_into_repo "$file" "$repo_dir" "$remote_path"
  done
}

git_commit_and_push_with_retry() {
  local repo_dir="$1"
  local branch="$2"
  local commit_message="$3"
  local max_attempts="${GITHUB_MANAGER_PUSH_RETRIES:-3}"
  local attempt=1
  (
    cd "$repo_dir"
    if [[ -z "$(git status --short)" ]]; then
      warn "没有检测到文件变更，跳过提交"
      return 0
    fi
    git add .
    git commit -m "$commit_message" >/dev/null
    while (( attempt <= max_attempts )); do
      if git push origin "$branch" >/dev/null 2>push.err; then
        rm -f push.err
        return 0
      fi
      warn "push 被远端拒绝，准备自动 rebase 重试 ($attempt/$max_attempts)"
      if git fetch origin "$branch" >/dev/null 2>&1 && git rebase "origin/$branch" >/dev/null 2>&1; then
        attempt=$((attempt + 1))
        continue
      fi
      cat push.err >&2 || true
      return 1
    done
    cat push.err >&2 || true
    return 1
  )
}

upload_via_git() {
  local repo="$1"
  local branch="$2"
  local remote_path="$3"
  local commit_message="$4"
  shift 4
  local files=("$@")
  [[ ${#files[@]} -gt 0 ]] || die "没有要上传的文件"
  warn_large_files "${files[@]}"

  local tmpdir
  tmpdir="$(clone_repo_temp "$repo" "$branch")"
  stage_upload_files "$tmpdir" "$remote_path" "${files[@]}"

  if ! git_commit_and_push_with_retry "$tmpdir" "$branch" "$commit_message"; then
    cleanup_dir "$tmpdir"
    die "上传失败：远端分支有并发更新或冲突，请稍后重试"
  fi
  cleanup_dir "$tmpdir"
  success "上传完成：$repo#$branch"
}

resolve_remote_sha() {
  local repo="$1"
  local path="$2"
  local branch="${3:-}"
  api_get_contents "$repo" "$path" "$branch" | jq -r '.sha // empty'
}

download_file() {
  local repo="$1"
  local remote_path="$2"
  local save_to="$3"
  local branch="${4:-}"
  local content_json
  content_json="$(api_get_contents "$repo" "$remote_path" "$branch")"
  local type
  type="$(jq -r '.type' <<< "$content_json")"
  if [[ "$type" == "dir" ]]; then
    die "download_file 仅支持单文件，请使用 download_path"
  fi
  mkdir -p "$(dirname "$save_to")"
  jq -r '.content' <<< "$content_json" | tr -d '\n' | base64 -d > "$save_to"
  success "已下载文件到 $save_to"
}

download_path() {
  local repo="$1"
  local remote_path="$2"
  local save_dir="$3"
  local branch="${4:-}"
  local content_json
  content_json="$(api_get_contents "$repo" "$remote_path" "$branch")"
  local type
  type="$(jq -r 'if type == "array" then "dir" else .type end' <<< "$content_json")"
  if [[ "$type" == "file" ]]; then
    local target
    if [[ -d "$save_dir" || "$save_dir" == */ ]]; then
      target="${save_dir%/}/$(basename "$remote_path")"
    else
      target="$save_dir"
    fi
    download_file "$repo" "$remote_path" "$target" "$branch"
    return 0
  fi

  mkdir -p "$save_dir"
  jq -c '.[]' <<< "$content_json" | while IFS= read -r item; do
    local child_type child_path child_name
    child_type="$(jq -r '.type' <<< "$item")"
    child_path="$(jq -r '.path' <<< "$item")"
    child_name="$(basename "$child_path")"
    if [[ "$child_type" == "file" ]]; then
      download_file "$repo" "$child_path" "$save_dir/$child_name" "$branch"
    elif [[ "$child_type" == "dir" ]]; then
      download_path "$repo" "$child_path" "$save_dir/$child_name" "$branch"
    fi
  done
}

update_file_contents() {
  local repo="$1"
  local remote_path="$2"
  local local_file="$3"
  local branch="$4"
  local commit_message="$5"
  local sha
  sha="$(resolve_remote_sha "$repo" "$remote_path" "$branch")"
  [[ -n "$sha" ]] || die "远程文件不存在：$remote_path"
  local payload
  payload="$(jq -n \
    --arg message "$commit_message" \
    --arg content "$(base64_file "$local_file")" \
    --arg branch "$branch" \
    --arg sha "$sha" \
    '{message:$message, content:$content, branch:$branch, sha:$sha}')"
  if [[ "$AUTH_MODE" == "gh" ]] || is_gh_authenticated; then
    gh api --method PUT "repos/$repo/contents/$remote_path" --input - <<< "$payload" >/dev/null
  else
    local header_args=()
    mapfile -t header_args < <(get_auth_header_args)
    curl -fsSL -X PUT --connect-timeout "$API_TIMEOUT" \
      -H "Accept: application/vnd.github+json" \
      -H "Content-Type: application/json" \
      "${header_args[@]}" \
      -d "$payload" \
      "https://api.github.com/repos/$repo/contents/$remote_path" >/dev/null
  fi
  success "文件已更新：$remote_path"
}

delete_remote_file() {
  local repo="$1"
  local remote_path="$2"
  local branch="$3"
  local commit_message="$4"
  local sha
  sha="$(resolve_remote_sha "$repo" "$remote_path" "$branch")"
  [[ -n "$sha" ]] || die "远程路径不存在：$remote_path"
  local payload
  payload="$(jq -n --arg message "$commit_message" --arg sha "$sha" --arg branch "$branch" '{message:$message, sha:$sha, branch:$branch}')"
  if [[ "$AUTH_MODE" == "gh" ]] || is_gh_authenticated; then
    gh api --method DELETE "repos/$repo/contents/$remote_path" --input - <<< "$payload" >/dev/null
  else
    local header_args=()
    mapfile -t header_args < <(get_auth_header_args)
    curl -fsSL -X DELETE --connect-timeout "$API_TIMEOUT" \
      -H "Accept: application/vnd.github+json" \
      -H "Content-Type: application/json" \
      "${header_args[@]}" \
      -d "$payload" \
      "https://api.github.com/repos/$repo/contents/$remote_path" >/dev/null
  fi
  success "已删除远程文件：$remote_path"
}

delete_remote_path_recursive() {
  local repo="$1"
  local remote_path="$2"
  local branch="$3"
  local commit_prefix="$4"
  local content_json
  content_json="$(api_get_contents "$repo" "$remote_path" "$branch")"
  local type
  type="$(jq -r 'if type == "array" then "dir" else .type end' <<< "$content_json")"
  if [[ "$type" == "file" ]]; then
    delete_remote_file "$repo" "$remote_path" "$branch" "$commit_prefix: $remote_path"
    return 0
  fi
  jq -r '.[].path' <<< "$content_json" | sort -r | while IFS= read -r child; do
    delete_remote_path_recursive "$repo" "$child" "$branch" "$commit_prefix"
  done
}

sync_local_to_remote() {
  local repo="$1"
  local local_dir="$2"
  local remote_path="$3"
  local branch="$4"
  local dry_run="$5"
  [[ -d "$local_dir" ]] || die "本地目录不存在：$local_dir"
  remote_path="$(normalize_remote_path "$remote_path")"

  local report
  report="$(compare_sync_state "$repo" "$local_dir" "$remote_path" "$branch")"
  print_sync_plan "$report" "push"

  if [[ -z "$report" ]] || ! grep -qE 'local_only|remote_only|conflict' <<< "$report"; then
    success "本地与远程已经同步"
    return 0
  fi

  if [[ "$dry_run" == "true" ]]; then
    success "dry-run 完成，未执行实际同步"
    return 0
  fi

  if grep -q '^conflict' <<< "$report"; then
    die "检测到冲突，请先处理后重试，或改用 pull 模式"
  fi

  while IFS=$'\t' read -r state rel; do
    case "$state" in
      local_only|same)
        [[ "$state" == "same" ]] && continue
        upload_single_file_to_remote "$repo" "$branch" "$local_dir/$rel" "$(remote_join "$remote_path" "$rel")" "Sync upload $rel"
        ;;
      remote_only)
        delete_remote_file "$repo" "$(remote_join "$remote_path" "$rel")" "$branch" "Sync delete remote-only $rel"
        ;;
    esac
  done <<< "$report"
  success "push 模式同步完成"
}

sync_remote_to_local() {
  local repo="$1"
  local local_dir="$2"
  local remote_path="$3"
  local branch="$4"
  local dry_run="$5"
  mkdir -p "$local_dir"
  remote_path="$(normalize_remote_path "$remote_path")"

  local report
  report="$(compare_sync_state "$repo" "$local_dir" "$remote_path" "$branch")"
  print_sync_plan "$report" "pull"

  if [[ -z "$report" ]] || ! grep -qE 'local_only|remote_only|conflict' <<< "$report"; then
    success "本地与远程已经同步"
    return 0
  fi

  if [[ "$dry_run" == "true" ]]; then
    success "dry-run 完成，未执行实际同步"
    return 0
  fi

  if grep -q '^conflict' <<< "$report"; then
    die "检测到冲突，请先处理后重试，或改用 push 模式"
  fi

  while IFS=$'\t' read -r state rel; do
    case "$state" in
      remote_only)
        download_file "$repo" "$(remote_join "$remote_path" "$rel")" "$local_dir/$rel" "$branch" >/dev/null
        ;;
      local_only)
        rm -f "$local_dir/$rel"
        ;;
    esac
  done <<< "$report"
  success "pull 模式同步完成"
}

print_tree_view() {
  local repo="$1"
  local branch="$2"
  local tree_data
  tree_data="$(list_remote_tree "$repo" "$branch")"
  printf '%s\n' "$tree_data" | python3 -c '
import sys
for line in sys.stdin:
    line=line.rstrip("\n")
    if not line:
        continue
    parts=line.split("\t")
    if len(parts) < 4:
        continue
    typ, path, size, sha = parts[:4]
    depth = path.count("/")
    prefix = "  " * depth
    icon = "DIR " if typ == "tree" else "FILE"
    size_text = "" if typ == "tree" else f" ({int(size) if size.isdigit() else size} B)"
    print(f"{prefix}{icon} {path.split(chr(47))[-1]}{size_text}")
'
}
