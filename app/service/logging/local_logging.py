import logging
import logging.config


class LocalLogging:
    def __init__(self):
        self.config()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def config():
        logging.config.dictConfig({
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
                    'level': 'DEBUG',
                    'handlers': ['console']
                }
            }
        })

    def log_entry(self, message, severity='INFO'):
        method = getattr(self.logger, severity.lower())
        method(message)

    def debug(self, message):
        self.log_entry(message, 'DEBUG')

    def info(self, message):
        self.log_entry(message, 'INFO')

    def error(self, message):
        self.log_entry(message, 'ERROR')

    def critical(self, message):
        self.log_entry(message, 'CRITICAL')
