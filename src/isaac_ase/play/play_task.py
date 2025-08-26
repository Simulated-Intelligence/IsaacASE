import logging

logger = logging.getLogger(__name__)


class PlayTask:
    def __init__(self, *args, **kwargs):
        logger.info("Loading play task.")

    def run(self, *args, **kwargs):
        logger.info("Running play task.")
