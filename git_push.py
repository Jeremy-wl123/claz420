"""
Git Push 脚本 - 使用 dulwich 推送 Week1 到远程仓库
执行步骤:
1. 添加 Week1 相关文件到暂存区
2. 创建提交
3. 推送到 origin/main
"""
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.config import ConfigFile
import os

repo_path = r'd:\PythonProject\claz420'

print("=" * 50)
print("步骤 1/4: 检查仓库状态")
print("=" * 50)

repo = Repo(repo_path)
status = porcelain.status(repo_path)

# 列出所有需要添加的 Week1 文件（排除 .env 等敏感文件）
files_to_add = []
for f in status.unstaged:
    f_str = f.decode('utf-8', 'ignore')
    # 只添加 Week1 相关文件，排除 .env 和 .idea
    if f_str.startswith('Week1/') and not f_str.endswith('.env') and '.env' not in f_str.split('/')[-1]:
        files_to_add.append(f_str)
        print(f'  [WILL ADD] {f_str}')

# 也添加 main.py 和 str.py (根目录的改动)
for f in status.unstaged:
    f_str = f.decode('utf-8', 'ignore')
    if f_str in ('main.py', 'str.py'):
        files_to_add.append(f_str)
        print(f'  [WILL ADD] {f_str}')

# 添加未跟踪文件（排除 git_check.py）
for f in status.untracked:
    f_str = f.decode('utf-8', 'ignore')
    if f_str != 'git_check.py':
        files_to_add.append(f_str)
        print(f'  [WILL ADD] {f_str}')

if not files_to_add:
    print('  No files to add. Checking if push is still needed...')
else:
    print(f'\n  共 {len(files_to_add)} 个文件待添加')

    print()
    print("=" * 50)
    print("步骤 2/4: 添加到暂存区 (git add)")
    print("=" * 50)
    for f in files_to_add:
        porcelain.add(repo_path, [f])
        print(f'  added: {f}')

    print()
    print("=" * 50)
    print("步骤 3/4: 创建提交 (git commit)")
    print("=" * 50)
    
    # 提交信息
    commit_msg = "feat: add Week1 day05 docker demo files and updates"
    
    try:
        commit_sha = porcelain.commit(
            repo_path,
            message=commit_msg,
            author="Jeremy-wl123 <jeremy@example.com>"
        )
        print(f'  Commit SHA: {commit_sha.decode("utf-8")}')
        print(f'  Message: {commit_msg}')
    except Exception as e:
        print(f'  Commit error: {e}')
        # 可能没有变化需要提交
        if 'nothing to commit' in str(e).lower() or 'no changes' in str(e).lower():
            print('  Nothing to commit, proceeding to push existing commits...')
        else:
            raise

print()
print("=" * 50)
print("步骤 4/4: 推送到远程 (git push)")
print("=" * 50)

remote_url = b'https://github.com/Jeremy-wl123/claz420.git'
print(f'  Remote: {remote_url.decode()}')
print(f'  Branch: main')

# 尝试使用 credential store 或环境变量
# dulwich 会尝试从 git credential 系统获取凭据
try:
    result = porcelain.push(
        repo_path,
        remote_location=remote_url,
        refspecs=[b'refs/heads/main:refs/heads/main'],
    )
    print(f'  Push result: {result}')
    print()
    print("=" * 50)
    print("✅ 推送成功!")
    print("=" * 50)
except Exception as e:
    error_msg = str(e)
    print(f'  Push failed: {error_msg}')
    print()
    if 'Authentication' in error_msg or 'auth' in error_msg.lower() or '401' in error_msg:
        print("⚠️  需要 GitHub 认证。请提供以下信息之一：")
        print("  1. GitHub Personal Access Token (推荐)")
        print("  2. GitHub 用户名和密码")
    else:
        print(f'  错误详情: {error_msg}')
