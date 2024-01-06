import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d:%(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)