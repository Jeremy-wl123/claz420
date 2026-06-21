"""
Git Push - 需要 GitHub Token 认证
"""
from dulwich import porcelain
import os

repo_path = r'd:\PythonProject\claz420'
remote_url = b'https://github.com/Jeremy-wl123/claz420.git'

# 从环境变量读取 token
token = os.environ.get('GITHUB_TOKEN', '')
if not token:
    print("ERROR: GITHUB_TOKEN 环境变量未设置")
    print()
    print("请执行以下步骤：")
    print("1. 前往 https://github.com/settings/tokens")
    print("2. 点击 'Generate new token (classic)'")
    print("3. 勾选 'repo' 权限")
    print("4. 生成并复制 token")
    print("5. 运行: set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx")
    print("6. 重新运行本脚本")
    exit(1)

print("正在推送到远程仓库...")
print(f"Remote: {remote_url.decode()}")
print(f"Branch: main")
print()

# 使用 token 认证的 URL
auth_url = f'https://{token}:x-oauth-basic@github.com/Jeremy-wl123/claz420.git'.encode()

try:
    result = porcelain.push(
        repo_path,
        remote_location=auth_url,
        refspecs=[b'refs/heads/main:refs/heads/main'],
    )
    print("Push 成功!")
    print(f"Result: {result}")
except Exception as e:
    error_msg = str(e)
    print(f"Push 失败: {error_msg}")
    if 'denied' in error_msg.lower() or 'permission' in error_msg.lower():
        print("提示: 确保 token 具有 'repo' 权限")
