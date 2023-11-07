from tool.logging import setup_logger

# 配置日志记录器
logger = setup_logger('logs/app.log')

# 添加日志记录
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
