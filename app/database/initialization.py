"""
数据库初始化模块
"""
from dotenv import dotenv_values

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.database.connection import engine, Base
from app.database.models import Settings
from app.log.logger import get_database_logger

logger = get_database_logger()


def create_tables():
    """
    创建数据库表
    """
    try:
        # 创建所有表
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise


def import_env_to_settings():
    """
    将.env文件中的配置项导入到t_settings表中

    注意：此功能已禁用。
    t_settings 表主要用于运行时动态配置，不应该在启动时自动导入所有环境变量。
    应用配置应该从环境变量中读取（.env 文件或 Railway Variables）。

    如果需要使用 t_settings 表，请通过管理界面或 API 手动配置。
    """
    try:
        # 检查 t_settings 表是否存在
        inspector = inspect(engine)

        if "t_settings" in inspector.get_table_names():
            logger.info("t_settings table exists (auto-import disabled)")
        else:
            logger.warning("t_settings table does not exist")

        logger.info("Skipped auto-import of environment variables to settings table")
    except Exception as e:
        logger.error(f"Failed to check settings table: {str(e)}")
        # 不抛出异常，允许应用继续启动
        pass


def initialize_database():
    """
    初始化数据库
    """
    try:
        # 创建表
        create_tables()
        
        # 导入环境变量
        import_env_to_settings()
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
