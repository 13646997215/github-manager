#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

repo="${1:-13646997215/github-manager}"
branch="${2:-}"
run_id="e2e-$(date +%Y%m%d%H%M%S)-$$"
remote_root="github-manager-e2e/$run_id"
workdir="$(mktemp -d /tmp/github-manager-e2e.XXXXXX)"
trap 'rm -rf "$workdir"' EXIT

assert_contains() {
  local needle="$1"
  local file="$2"
  grep -Fq "$needle" "$file" || {
    echo "ASSERT FAIL: $file does not contain $needle" >&2
    echo "--- $file ---" >&2
    sed -n '1,160p' "$file" >&2
    exit 1
  }
}

assert_file_content() {
  local file="$1"
  local expected="$2"
  [[ -f "$file" ]] || { echo "ASSERT FAIL: missing file $file" >&2; exit 1; }
  grep -Fq "$expected" "$file" || { echo "ASSERT FAIL: content mismatch in $file" >&2; exit 1; }
}

cleanup_remote() {
  ./bin/ghm-delete "$repo" "$remote_root" --branch "$branch" --force --message "cleanup $run_id" >/dev/null 2>&1 || true
}
trap 'cleanup_remote; rm -rf "$workdir"' EXIT

mkdir -p "$workdir/local/sub" "$workdir/download" "$workdir/pull"
printf 'hello from %s\n' "$run_id" > "$workdir/local/a.txt"
printf 'sub file %s\n' "$run_id" > "$workdir/local/sub/b.txt"
printf 'update content %s\n' "$run_id" > "$workdir/update.txt"
printf 'special 中文 %s\n' "$run_id" > "$workdir/local/特殊 字符 文件.txt"

printf '[0] repo info\n'
./bin/ghm-repo info "$repo" >/dev/null

if [[ -z "$branch" ]]; then
  branch="$(gh repo view "$repo" --json defaultBranchRef --jq '.defaultBranchRef.name // empty' 2>/dev/null || true)"
fi
branch="${branch:-main}"
printf 'Using branch: %s\n' "$branch"

printf '[1] upload folder\n'
./bin/ghm-upload --repo "$repo" --branch "$branch" --remote-path "$remote_root" --message "upload $run_id" "$workdir/local" >/tmp/ghm-upload.out

printf '[2] list root and tree\n'
./bin/ghm-list "$repo" "$remote_root" --branch "$branch" > "$workdir/list.txt"
assert_contains 'a.txt' "$workdir/list.txt"
assert_contains '特殊 字符 文件.txt' "$workdir/list.txt"
./bin/ghm-list "$repo" --tree --branch "$branch" > "$workdir/tree.txt"
assert_contains "$run_id" "$workdir/tree.txt"

printf '[3] download file\n'
./bin/ghm-download "$repo" "$remote_root/a.txt" "$workdir/download" --branch "$branch" >/tmp/ghm-download.out
assert_file_content "$workdir/download/a.txt" "hello from $run_id"

printf '[4] update file\n'
./bin/ghm-update "$repo" "$remote_root/a.txt" "$workdir/update.txt" --branch "$branch" --message "update $run_id" >/tmp/ghm-update.out
rm -rf "$workdir/download2" && mkdir -p "$workdir/download2"
./bin/ghm-download "$repo" "$remote_root/a.txt" "$workdir/download2" --branch "$branch" >/dev/null
assert_file_content "$workdir/download2/a.txt" "update content $run_id"

printf '[5] sync dry-run push report\n'
printf 'local only %s\n' "$run_id" > "$workdir/local/c.txt"
./bin/ghm-sync "$repo" "$workdir/local" "$remote_root" --branch "$branch" --mode push --dry-run --report "$workdir/push-report.txt" > "$workdir/push.out"
assert_contains 'local_only' "$workdir/push-report.txt"
assert_contains 'c.txt' "$workdir/push-report.txt"

printf '[6] sync dry-run pull report\n'
./bin/ghm-sync "$repo" "$workdir/pull" "$remote_root" --branch "$branch" --mode pull --dry-run --report "$workdir/pull-report.txt" > "$workdir/pull.out"
assert_contains 'remote_only' "$workdir/pull-report.txt"

printf '[7] sync conflict preview\n'
mkdir -p "$workdir/conflict"
printf 'different local %s\n' "$run_id" > "$workdir/conflict/a.txt"
./bin/ghm-sync "$repo" "$workdir/conflict" "$remote_root" --branch "$branch" --mode push --dry-run --report "$workdir/conflict-report.txt" > "$workdir/conflict.out"
assert_contains 'conflict' "$workdir/conflict-report.txt"

printf '[8] delete file\n'
./bin/ghm-delete "$repo" "$remote_root/sub/b.txt" --branch "$branch" --force --message "delete $run_id" >/tmp/ghm-delete.out
if ./bin/ghm-list "$repo" "$remote_root/sub/b.txt" --branch "$branch" >/tmp/ghm-deleted-list.out 2>&1; then
  echo 'ASSERT FAIL: deleted file still exists' >&2
  exit 1
fi

printf '[9] about audit release install desktop\n'
./github-manager.sh about > "$workdir/about.txt"
assert_contains 'GitHub Manager Pro' "$workdir/about.txt"
./github-manager.sh audit > "$workdir/audit.txt" || true
./github-manager.sh release >/tmp/ghm-release.out
test -f "$ROOT_DIR/release/github-manager.sh"
./github-manager.sh install --local-bin "$workdir/bin" --with-desktop >/tmp/ghm-install.out
test -L "$workdir/bin/ghm-list"
test -f "$HOME/.local/share/applications/GitHubManager.desktop"

desktop-file-validate "$HOME/Desktop/GitHubManager.desktop"
if command -v script >/dev/null 2>&1; then
  python3 - <<'PY' "$ROOT_DIR" "$workdir/desktop-script.log"
import os, pty, select, signal, subprocess, sys, time
root = sys.argv[1]
log_path = sys.argv[2]
env = os.environ.copy()
env.update({'GITHUB_MANAGER_USE_FZF':'0','GITHUB_MANAGER_NO_CLEAR':'1','FORCE_COLOR':'1','TERM':'xterm-256color'})
master, slave = pty.openpty()
proc = subprocess.Popen(['./bin/launch-github-manager.sh'], cwd=root, stdin=slave, stdout=slave, stderr=slave, env=env, preexec_fn=os.setsid)
os.close(slave)
out = b''
steps = [('功能选择', 'e')]
idx = 0
start = time.time()
rc = 1
try:
    while time.time() - start < 20:
        r, _, _ = select.select([master], [], [], 0.2)
        if master in r:
            try:
                data = os.read(master, 8192)
            except OSError:
                break
            if not data:
                break
            out += data
        text = out.decode('utf-8', 'ignore')
        if idx < len(steps) and steps[idx][0] in text:
            os.write(master, (steps[idx][1] + '\n').encode())
            idx += 1
        if proc.poll() is not None:
            rc = proc.poll()
            break
    else:
        rc = proc.poll()
finally:
    if proc.poll() is None:
        os.write(master, b'e\n')
        time.sleep(0.4)
        try:
            rc = proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            rc = None
            os.killpg(proc.pid, signal.SIGTERM)
        else:
            rc = proc.poll()
    os.close(master)
text = out.decode('utf-8', 'ignore')
with open(log_path, 'w', encoding='utf-8') as f:
    f.write(text)
required = ['GitHub Manager Pro']
missing = [item for item in required if item not in text]
if missing:
    print('ASSERT FAIL: desktop launcher smoke failed', file=sys.stderr)
    print(text[-4000:], file=sys.stderr)
    sys.exit(1)
PY
  assert_contains 'GitHub Manager Pro' "$workdir/desktop-script.log"
fi

printf '[10] cleanup remote\n'
cleanup_remote
trap 'rm -rf "$workdir"' EXIT

echo "Integration E2E PASS for $repo#$branch remote=$remote_root"
