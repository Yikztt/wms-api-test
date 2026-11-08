import logging
import os

# 日志目录：与 pytest.ini 中的 log_file 保持一致
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log")
LOG_FILE = os.path.join(LOG_DIR, "test.log")

# 统一格式：时间 - 级别 - 文件名:行号 - 消息
_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 命名 logger，避免与 pytest 自带的 root logger 重复注册 handler
_LOGGER_NAME = "wms_auto"


def get_logger(name: str = _LOGGER_NAME) -> logging.Logger:
    """获取统一的框架日志对象。

    设计说明：
    - 默认 propagate=True，因此在 pytest 中会自动被 pytest.ini 配置的
      CLI / 文件 handler 接管（控制台 + ./log/test.log 双写）。
    - 若脱离 pytest 单独运行（无 pytest handler），下面会兜底挂上
      控制台 + 文件 handler，保证日志不丢失、也不重复。
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 没有 handler 时（通常是脱离 pytest 运行）才自行添加，避免重复写
    if not logger.handlers:
        # 确保日志目录存在
        os.makedirs(LOG_DIR, exist_ok=True)

        formatter = logging.Formatter(_LOG_FORMAT, _DATE_FORMAT)

        # 控制台：只显示 WARNING 及以上，避免 66 条用例把屏幕刷满；
        # 完整 INFO/DEBUG 细节已写入 ./log/test.log，需要排查时看该文件即可。
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.WARNING)

        # 文件（utf-8，追加写）
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)

        logger.addHandler(sh)
        logger.addHandler(fh)
        # 自己已处理输出，不让记录再冒泡到 root，避免脱离 pytest 时重复打印
        logger.propagate = False

    return logger
