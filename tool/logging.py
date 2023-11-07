import logging


def setup_logger(log_file):
    # 配置日志记录器
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建文件处理程序，将日志写入到文件中
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)  # 设置文件处理程序的日志级别为 DEBUG
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    # 将文件处理程序添加到日志记录器
    logging.getLogger('').addHandler(file_handler)

    # 返回日志记录器，以便在程序的其他地方使用
    return logging.getLogger(__name__)
