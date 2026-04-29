#!/usr/bin/env python3
import os, pty, subprocess, time, select, sys, signal
ROOT='/home/hanhan/Desktop/github'

def run_interaction(name, inputs, expects, timeout=60):
    env=os.environ.copy()
    env.update({'GITHUB_MANAGER_USE_FZF':'0','GITHUB_MANAGER_NO_CLEAR':'1','FORCE_COLOR':'1','TERM':'xterm-256color'})
    master, slave = pty.openpty()
    proc=subprocess.Popen(['./bin/launch-github-manager.sh'], cwd=ROOT, stdin=slave, stdout=slave, stderr=slave, env=env, preexec_fn=os.setsid)
    os.close(slave)
    out=b''; idx=0; start=time.time()
    try:
        while time.time()-start < timeout:
            r,_,_=select.select([master], [], [], 0.15)
            if master in r:
                try: data=os.read(master, 8192)
                except OSError: break
                if not data: break
                out += data
            text=out.decode('utf-8','ignore')
            if idx < len(inputs) and inputs[idx][0] in text:
                os.write(master, (inputs[idx][1]+'\n').encode())
                idx += 1
            if proc.poll() is not None: break
        text=out.decode('utf-8','ignore')
        missing=[e for e in expects if e not in text]
        if missing:
            print(f'FAIL {name}: missing {missing}')
            print(text[-5000:])
            return False
        print(f'PASS {name}')
        return True
    finally:
        if proc.poll() is None:
            try: os.killpg(proc.pid, signal.SIGTERM)
            except Exception: pass
        os.close(master)

ok=True
ok &= run_interaction('menu-exit', [('功能选择','e')], ['GitHub Manager Pro','上传文件','浏览仓库'])
ok &= run_interaction('quick-upload-entry', [('功能选择','1'), ('本地文件选择','q')], ['本地文件选择', '当前目录:', '/home/hanhan'])
ok &= run_interaction('download-flow-guided', [('功能选择','3'), ('选择仓库方式','\n'), ('选择仓库','\n'), ('远程路径向导','q'), ('功能选择','e')], ['选择仓库方式', '远程路径向导'])
ok &= run_interaction('update-flow-guided', [('功能选择','5'), ('选择仓库方式','\n'), ('选择仓库','\n'), ('远程路径向导','q'), ('功能选择','e')], ['选择仓库方式', '远程路径向导'])
ok &= run_interaction('sync-flow-guided', [('功能选择','6'), ('选择仓库方式','\n'), ('选择仓库','\n'), ('本地路径向导','q'), ('功能选择','e')], ['选择仓库方式', '本地路径向导'])
ok &= run_interaction('about', [('功能选择','9'), ('按 Enter',''), ('功能选择','e')], ['GitHub Manager Pro','核心能力'])
ok &= run_interaction('settings-account-entry', [('功能选择','8'), ('账号/设置','\n'), ('按 Enter',''), ('账号/设置','q'), ('功能选择','e')], ['账号/设置','当前 GitHub 账号'])
sys.exit(0 if ok else 1)
