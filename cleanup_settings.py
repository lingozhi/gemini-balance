"""
清理和修复 t_settings 表的脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy.orm import Session
from app.database.connection import engine
from app.database.models import Settings
from app.log.logger import get_database_logger

logger = get_database_logger()


def cleanup_settings_table():
    """
    清空 t_settings 表

    注意：这会删除表中的所有数据！
    t_settings 表主要用于运行时动态配置，不影响应用启动。
    应用配置主要从环境变量（.env 或 Railway Variables）读取。
    """
    try:
        with Session(engine) as session:
            # 获取当前记录数
            count_before = session.query(Settings).count()
            logger.info(f"Found {count_before} records in t_settings table")

            if count_before == 0:
                print("✅ t_settings table is already empty")
                return

            # 删除所有记录
            session.query(Settings).delete()
            session.commit()

            # 确认删除
            count_after = session.query(Settings).count()
            logger.info(f"Deleted {count_before - count_after} records from t_settings table")

            print(f"✅ Successfully cleaned up t_settings table")
            print(f"   - Deleted: {count_before} records")
            print(f"   - Remaining: {count_after} records")

    except Exception as e:
        logger.error(f"Failed to cleanup t_settings table: {e}", exc_info=True)
        print(f"❌ Failed to cleanup t_settings table: {e}")
        sys.exit(1)


def show_settings_table():
    """显示 t_settings 表的内容"""
    try:
        with Session(engine) as session:
            settings = session.query(Settings).all()

            if not settings:
                print("t_settings table is empty")
                return

            print(f"\nt_settings table contains {len(settings)} records:")
            print("-" * 80)
            print(f"{'ID':<5} {'Key':<30} {'Value':<40}")
            print("-" * 80)

            for setting in settings:
                value_preview = str(setting.value)[:40] if setting.value else ""
                print(f"{setting.id:<5} {setting.key:<30} {value_preview:<40}")

            print("-" * 80)

    except Exception as e:
        logger.error(f"Failed to show t_settings table: {e}", exc_info=True)
        print(f"❌ Failed to show t_settings table: {e}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Cleanup and manage t_settings table")
    parser.add_argument("--show", action="store_true", help="Show current settings")
    parser.add_argument("--clean", action="store_true", help="Clean up all settings")

    args = parser.parse_args()

    if args.show:
        show_settings_table()
    elif args.clean:
        print("⚠️  WARNING: This will delete ALL records in t_settings table!")
        print("   t_settings is only used for runtime dynamic configuration.")
        print("   App configuration is mainly read from environment variables.")
        print()
        confirm = input("Are you sure you want to continue? (yes/no): ")

        if confirm.lower() in ['yes', 'y']:
            cleanup_settings_table()
        else:
            print("❌ Operation cancelled")
    else:
        print("Usage:")
        print("  python cleanup_settings.py --show   # Show current settings")
        print("  python cleanup_settings.py --clean  # Clean up all settings")


if __name__ == "__main__":
    main()
