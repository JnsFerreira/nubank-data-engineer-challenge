import logging
import logging.config
from typing import Optional


class LocalLogging:
    """Local logging class that abstract default logging class"""
    DEFAULT_CONFIG = {
            'version': 1,
            'formatters': {'default': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s',
            }},
            'handlers': {'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            }},
            'loggers': {
                __name__: {
                    'level': 'INFO',
                    'handlers': ['console']
                }
            }
        }

    def __init__(
        self,
        logging_config: Optional[dict] = None
    ):
        self.setup(config=logging_config or self.DEFAULT_CONFIG)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def setup(config: dict) -> None:
        """
        Perform the logger setup based on a configuration dictionary.

        Args:
            config (dict):
        Returns:
            None
        """

        logging.config.dictConfig(config)

    def info(self, message: str, **kwargs) -> None:
        """
        Log 'msg' with severity 'INFO'.
        Args:
            message: Message to be logged
            **kwargs: keyword arguments

        Returns:
            None
        """
        self.logger.info(msg=message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """
        Log 'msg' with severity 'WARNING'.
        Args:
            message: Message to be logged
            **kwargs: keyword arguments

        Returns:
            None
        """
        self.logger.warning(msg=message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """
        Log 'msg' with severity 'ERROR'.
        Args:
            message: Message to be logged
            **kwargs: keyword arguments

        Returns:
            None
        """
        self.logger.error(msg=message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """
        Log 'msg' with severity 'CRITICAL'.
        Args:
            message: Message to be logged
            **kwargs: keyword arguments

        Returns:
            None
        """
        self.logger.critical(msg=message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """
        Log 'msg' with severity 'DEBUG'.
        Args:
            message: Message to be logged
            **kwargs: keyword arguments

        Returns:
            None
        """
        self.logger.debug(msg=message, **kwargs)
