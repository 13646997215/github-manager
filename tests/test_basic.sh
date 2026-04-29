#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

printf '== Shell syntax ==\n'
files=(github-manager.sh github-upload.sh install-deps.sh lib/*.sh bin/ghm-delete bin/ghm-download bin/ghm-list bin/ghm-repo bin/ghm-sync bin/ghm-update bin/ghm-upload bin/launch-github-manager.sh tests/*.sh)
for file in "${files[@]}"; do
  bash -n "$file"
  printf 'PASS %s\n' "$file"
done

printf '\n== Desktop shortcut ==\n'
desktop-file-validate /home/hanhan/Desktop/GitHubManager.desktop
printf 'PASS desktop-file-validate\n'

printf '== Desktop launcher smoke ==\n'
python3 - "$ROOT_DIR" <<'PY'
import os, pty, select, signal, subprocess, sys, time
ROOT = sys.argv[1]
root = ROOT
env = os.environ.copy()
env.update({'GITHUB_MANAGER_USE_FZF':'0','GITHUB_MANAGER_NO_CLEAR':'1','FORCE_COLOR':'1','TERM':'xterm-256color'})
master, slave = pty.openpty()
proc = subprocess.Popen(['./bin/launch-github-manager.sh'], cwd=root, stdin=slave, stdout=slave, stderr=slave, env=env, preexec_fn=os.setsid)
os.close(slave)
out = b''
steps = [
    ('功能选择', 'e'),
]
idx = 0
start = time.time()
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
            break
    text = out.decode('utf-8', 'ignore')
    required = ['GitHub Manager Pro', '功能选择']
    missing = [item for item in required if item not in text]
    if missing or proc.poll() not in (0, None):
        print('FAIL desktop launcher smoke', file=sys.stderr)
        print(text[-4000:], file=sys.stderr)
        sys.exit(1)
finally:
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGTERM)
    os.close(master)
PY
printf 'PASS desktop launcher smoke\n'

printf '\n== Help output ==\n'
./github-manager.sh --help >/dev/null
printf 'PASS help\n'

printf '\n== Auth status ==\n'
gh auth status --hostname github.com >/dev/null 2>&1
printf 'PASS gh auth\n'

printf '\n== Repo cache refresh ==\n'
bash -lc 'source lib/repos.sh && refresh_repo_cache >/dev/null && test -s "$REPO_CACHE_FILE"'
printf 'PASS repo cache\n'

printf '\n== No-color / dumb-terminal fallback ==\n'
NO_COLOR=1 TERM=dumb timeout 15 script -q -c "printf '12\n' | $ROOT_DIR/github-manager.sh menu" /tmp/github-manager-nocolor.log >/dev/null 2>&1 || true
if grep -Fq '\033' /tmp/github-manager-nocolor.log; then
  echo 'FAIL no-color fallback: literal escape sequence found' >&2
  sed -n '1,80p' /tmp/github-manager-nocolor.log >&2 || true
  exit 1
fi
printf 'PASS no-color fallback\n'

printf '\n== PAT fallback loader ==\n'
pat_home="$(mktemp -d /tmp/ghm-pat-home.XXXXXX)"
mkdir -p "$pat_home/.config/github-manager"
printf 'ghp_testtoken' > "$pat_home/.config/github-manager/token"
HOME="$pat_home" XDG_CONFIG_HOME="$pat_home/.config" bash -lc 'cd /home/hanhan/Desktop/github && source lib/auth.sh && load_pat_token && test "$AUTH_MODE" = pat && test "$GITHUB_TOKEN" = ghp_testtoken'
rm -rf "$pat_home"
printf 'PASS PAT fallback loader\n'

printf '\n== Detailed audit log JSON ==\n'
audit_state_home="$(mktemp -d /tmp/ghm-audit-state.XXXXXX)"
XDG_STATE_HOME="$audit_state_home" bash -lc '
  mkdir -p "$XDG_STATE_HOME/github-manager"
  cd /home/hanhan/Desktop/github
  source lib/common.sh
  export AUDIT_LOG_FILE="$XDG_STATE_HOME/github-manager/audit.log"
  : > "$AUDIT_LOG_FILE"
  log_operation_start TEST_ACTION "$(build_audit_payload repo test/repo branch main remote_path docs local_path /tmp/demo.txt file_count 1)" >/dev/null
  log_operation_end success "$(build_audit_payload repo test/repo branch main remote_path docs local_path /tmp/demo.txt file_count 1 exit_code 0)"
  python3 - <<"PY" "$AUDIT_LOG_FILE"
import json, sys
lines=[line.strip() for line in open(sys.argv[1], encoding="utf-8") if line.strip()]
json_lines=[json.loads(line) for line in lines if line.startswith("{")]
assert len(json_lines) == 2, json_lines
assert json_lines[0]["phase"] == "start"
assert json_lines[1]["phase"] == "end"
assert json_lines[1]["result"] == "success"
assert json_lines[1]["repo"] == "test/repo"
assert json_lines[1]["duration_ms"] >= 0
print("PASS detailed audit log json")
PY
'
rm -rf "$audit_state_home"
printf '\n== Delete requires force in non-interactive mode ==\n'
if ./bin/ghm-delete fake/repo fake-path >/tmp/ghm-delete-no-force.out 2>&1; then
  echo 'FAIL delete without --force should fail in non-interactive mode' >&2
  exit 1
fi
printf 'PASS delete safety guard\n'
