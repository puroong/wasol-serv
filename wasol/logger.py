import logging

logger_name = 'wasol_logger'
log_filepath = 'C:\\Windows\\Temp\\wasol-serv.log'

logger = logging.getLogger(logger_name)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_filepath)

c_format = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s')
f_format = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.setLevel(logging.DEBUG)
