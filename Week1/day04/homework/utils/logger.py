"""
日志配置模块
----------
提供统一的日志记录器，同时输出到控制台和滚动文件。
日志文件持久化到项目根目录下的 log/ 目录中。
"""
import logging
import logging.handlers
import os

# 日志目录：当前文件所在目录的上一级（即 homework/）下的 log/ 目录
_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log")
_LOG_FILE = os.path.join(_LOG_DIR, "app.log")


def setup_logging():
    """配置日志记录器：同时输出到控制台和滚动文件"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 避免重复添加 handler
    if logger.handlers:
        return

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 确保日志目录存在
    os.makedirs(_LOG_DIR, exist_ok=True)

    # 文件输出（滚动日志，最大 10MB，保留 5 个备份）
    file_handler = logging.handlers.RotatingFileHandler(
        _LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("日志系统初始化完成")


# 模块加载时自动初始化日志
setup_logging()

