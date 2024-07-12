# 配置信息
import logging
from logging import getLogger


def get_logger(logger_name: str, log_level: int = logging.DEBUG, log_path: str = ""):
    """
    日志模块
    :param logger_name: 日志别名
    :param log_level: 日记等级
    :param log_path: 日志保存的路径
    :return:
    """
    logger = getLogger(logger_name)
    logger.setLevel(log_level)

    if logger.handlers:
        for i in range(len(logger.handlers)):
            logger.handlers.pop()

    if log_path:
        file_handler = logging.FileHandler(log_path)  # 指定日志文件名
        file_handler.setLevel(log_level)  # 设置handler级别
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)  # 可以根据需要调整控制台输出的级别

    base_format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    date_format = '%a, %Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(base_format, date_format)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


sql_log = get_logger('sql')
blog_log = get_logger('blog')
