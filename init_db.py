"""
数据库初始化脚本
手动运行此脚本来创建数据库表
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.database.initialization import initialize_database
from app.log.logger import get_database_logger

logger = get_database_logger()


def main():
    """
    主函数：初始化数据库
    """
    try:
        logger.info("开始初始化数据库...")
        initialize_database()
        logger.info("✅ 数据库初始化成功！")
        print("\n✅ 数据库表创建成功！")
        print("   表包括：")
        print("   - t_settings (设置表)")
        print("   - t_error_logs (错误日志表)")
        print("   - t_request_log (请求日志表)")
        print("   - t_file_records (文件记录表)")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}", exc_info=True)
        print(f"\n❌ 数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
