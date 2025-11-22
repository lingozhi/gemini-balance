"""
配置检查脚本 - 验证 .env 配置是否正确
"""
import sys
import json
from pathlib import Path
from typing import List, Tuple

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

def check_env_file() -> List[Tuple[str, bool, str]]:
    """检查 .env 文件配置"""
    results = []
    env_file = PROJECT_ROOT / ".env"

    if not env_file.exists():
        results.append(("ENV_FILE", False, ".env file not found!"))
        return results

    results.append(("ENV_FILE", True, ".env file exists"))

    # 读取配置
    env_vars = {}
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value

    # 检查必需配置
    required_configs = {
        'DATABASE_TYPE': 'mysql',
        'MYSQL_HOST': None,
        'MYSQL_PORT': None,
        'MYSQL_USER': None,
        'MYSQL_PASSWORD': None,
        'MYSQL_DATABASE': None,
        'API_KEYS': None,
        'ALLOWED_TOKENS': None,
        'AUTH_TOKEN': None,
    }

    for key, expected in required_configs.items():
        if key not in env_vars or not env_vars[key]:
            results.append((key, False, f"[X] {key} is not configured"))
        elif env_vars[key] in ['', 'change_me', 'your-', 'xxxx', 'AIzaSyxxx']:
            results.append((key, False, f"[!] {key} is still a placeholder: {env_vars[key][:20]}..."))
        else:
            # 检查 JSON 格式
            if key in ['API_KEYS', 'ALLOWED_TOKENS']:
                try:
                    parsed = json.loads(env_vars[key])
                    if isinstance(parsed, list) and len(parsed) > 0:
                        # 检查是否是占位符
                        first_item = parsed[0]
                        if 'xxx' in first_item.lower() or 'your' in first_item.lower() or len(first_item) < 10:
                            results.append((key, False, f"[!] {key} contains placeholder"))
                        else:
                            results.append((key, True, f"[OK] {key} configured ({len(parsed)} items)"))
                    else:
                        results.append((key, False, f"[X] {key} is empty list"))
                except json.JSONDecodeError:
                    results.append((key, False, f"[X] {key} JSON format error"))
            else:
                results.append((key, True, f"[OK] {key} is configured"))

    return results

def main():
    """主函数"""
    print("=" * 60)
    print("Gemini Balance - Configuration Check")
    print("=" * 60)
    print()

    results = check_env_file()

    has_errors = False
    has_warnings = False

    for key, success, message in results:
        print(message)
        if not success:
            if "[X]" in message:
                has_errors = True
            elif "[!]" in message:
                has_warnings = True

    print()
    print("=" * 60)

    if has_errors:
        print("[FAIL] Configuration check failed! Please fix the errors above.")
        print()
        print("[TIP] Quick start:")
        print("  1. Copy .env.minimal to .env")
        print("  2. Fill in real database config and API keys")
        print("  3. Remove or comment out unused config items")
        sys.exit(1)
    elif has_warnings:
        print("[WARN] Configuration has warnings! Some values may still be placeholders.")
        print()
        print("App may start but functionality will be limited.")
        sys.exit(0)
    else:
        print("[OK] Configuration check passed! All required items are set correctly.")
        sys.exit(0)

if __name__ == "__main__":
    main()
