import random
import time
from logger import setup_logger

logger = setup_logger(__name__)


def random_sleep():
    rand = random.randint(0, 2)
    logger.info(f"Sleeping for {rand} seconds...")
    time.sleep(rand)
    return
