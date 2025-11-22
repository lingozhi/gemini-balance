"""
直接连接数据库清理 t_settings 表
不依赖应用配置，可以直接运行
"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Railway MySQL 连接信息
MYSQL_HOST = "caboose.proxy.rlwy.net"
MYSQL_PORT = 15528
MYSQL_USER = "root"
MYSQL_PASSWORD = "tuODKyQwEmWJQXAfNHbEofQzFYjwwljn"
MYSQL_DATABASE = "railway"

# 构建连接字符串
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print("=" * 60)
print("Railway MySQL Database - t_settings Table Cleanup")
print("=" * 60)
print(f"Host: {MYSQL_HOST}")
print(f"Database: {MYSQL_DATABASE}")
print("=" * 60)
print()


def show_table():
    """显示 t_settings 表内容"""
    try:
        engine = create_engine(DATABASE_URL)
        with Session(engine) as session:
            result = session.execute(text("SELECT * FROM t_settings"))
            rows = result.fetchall()

            if not rows:
                print("[INFO] t_settings table is empty")
                return

            print(f"[INFO] t_settings table contains {len(rows)} records:")
            print("-" * 80)
            print(f"{'ID':<5} {'Key':<35} {'Value':<40}")
            print("-" * 80)

            for row in rows:
                value_preview = str(row[2])[:40] if len(row) > 2 and row[2] else ""
                key_name = str(row[1])[:35] if len(row) > 1 else ""
                print(f"{row[0]:<5} {key_name:<35} {value_preview:<40}")

            print("-" * 80)
            print()

    except Exception as e:
        print(f"[ERROR] Failed to show table: {e}")
        sys.exit(1)


def clean_table():
    """清空 t_settings 表"""
    try:
        engine = create_engine(DATABASE_URL)
        with Session(engine) as session:
            # 先查看有多少条记录
            result = session.execute(text("SELECT COUNT(*) FROM t_settings"))
            count_before = result.fetchone()[0]

            if count_before == 0:
                print("[INFO] t_settings table is already empty")
                return

            print(f"[INFO] Found {count_before} records in t_settings table")
            print()
            print("[WARN] This will DELETE ALL records from t_settings table!")
            print("[INFO] t_settings is only used for runtime configuration.")
            print("[INFO] App configuration is read from environment variables.")
            print()

            confirm = input("Continue? (yes/no): ")

            if confirm.lower() not in ['yes', 'y']:
                print("[INFO] Operation cancelled")
                return

            # 执行删除
            session.execute(text("TRUNCATE TABLE t_settings"))
            session.commit()

            print()
            print(f"[OK] Successfully cleaned t_settings table ({count_before} records deleted)")

    except Exception as e:
        print(f"[ERROR] Failed to clean table: {e}")
        sys.exit(1)


def test_connection():
    """测试数据库连接"""
    try:
        engine = create_engine(DATABASE_URL)
        with Session(engine) as session:
            result = session.execute(text("SELECT 1"))
            result.fetchone()
            print("[OK] Database connection successful")
            print()
            return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Cleanup t_settings table in Railway MySQL")
    parser.add_argument("--show", action="store_true", help="Show table content")
    parser.add_argument("--clean", action="store_true", help="Clean table (delete all records)")
    parser.add_argument("--test", action="store_true", help="Test database connection")

    args = parser.parse_args()

    if args.test or not (args.show or args.clean):
        if not test_connection():
            sys.exit(1)

    if args.show:
        show_table()
    elif args.clean:
        clean_table()
    else:
        print("Usage:")
        print("  python cleanup_db_direct.py --test   # Test connection")
        print("  python cleanup_db_direct.py --show   # Show table content")
        print("  python cleanup_db_direct.py --clean  # Clean table")


if __name__ == "__main__":
    main()
