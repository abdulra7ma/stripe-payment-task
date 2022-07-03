# Python imports
import logging
from logging.handlers import RotatingFileHandler
from os.path import abspath, isdir, join

# app imports
from .exceptions import ExceedFileSizeException


class Logger:
    DEFAULT_LEVEL = logging.DEBUG
    DEFAULT_LOG_FILE_PATH = abspath("logs")
    DEFAULT_LOG_FILE_SIZE = 10
    DEFAULT_BACKUP_COUNT = 10
    DEFAULT_LOG_FILE_NAME = "log.log"

    def __init__(
        self,
        logger_name,
        logging_level=None,
        formatter=None,
        handler=None,
        log_file_name=None,
        log_file_path=None,
        log_file_size=None,
        backup_count=None,
    ) -> None:
        """
        Initialize Custom Logger instance

        Attributes:
            logger_name   (str): string that indicate the logger name
            logging_level (str): string that indicate the logger level
            log_file_name (str): log file name
            log_file_path (str): log file directory path
            log_file_size (int): log file size in Megabytes (default value is 100 MB)
            backup_count  (int): max number of files to be generated if the main log file exceeded the file size (default value is 10)
            formatter     (logging.Formatter): a logging formatter instance that defines the log file format
            handler       (logging.handler)  : a logging handler class instance

        Return:
            None

        """

        self.logger_name = logger_name
        self.logging_level = logging_level
        self.formatter = formatter
        self.handler = handler
        self.log_file_path = log_file_path
        self.log_file_name = log_file_name
        self.log_file_size = log_file_size
        self.backup_count = backup_count

    def __call__(self, *args, **kwds):
        """runs when the class is called"""
        return self.logger()

    def logger(self):
        """
        Define the business logic of logger

        Return:
            logger: return a logger driver
        """
        # initialize logger instance
        logger = logging.getLogger(self.logger_name)

        # set Logging level
        logger.setLevel(self.get_logging_level)

        # set log file format
        formatter = self.get_formatter()

        # initialize logging handler
        handler = self.get_handler()

        # assign a formatter instance to the handler
        handler.setFormatter(formatter)

        # assign a handler instance to the handler
        logger.addHandler(handler)

        return logger

    @property
    def get_logging_level(self):
        """
        Get the user logging level or use the default one

        Return:
            str: return logging level

        """

        # dict of the different logging levels
        logging_levels_dict = {
            "info": logging.INFO,
            "debug": logging.DEBUG,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        if self.logging_level is not None:
            return logging_levels_dict[self.logging_level.lower()]
        return self.DEFAULT_LEVEL

    @property
    def get_log_file_path(self):
        """
        Get the user logging file path or use the default file path

        Return:
            str: return the path directory of the log file

        """
        if self.log_file_path is not None:
            if not isdir(self.log_file_path):
                raise FileNotFoundError("'log_file_path' can not be found")
            return self.log_file_path
        return self.DEFAULT_LOG_FILE_PATH

    @property
    def get_log_file_size(self):
        """
        Get the user logging file size or use the default file size

        Return:
            int: return the log file size
        """
        if self.log_file_size is not None:
            if self.log_file_size > 1024:
                raise ExceedFileSizeException(
                    "File size can not be more than 1024 MB"
                )
            return self.log_file_size
        return self.DEFAULT_LOG_FILE_SIZE

    @property
    def get_log_file_name(self):
        """
        Get the user logging file size or use the default file size

        Return:
            str: return the log file name
        """
        if self.log_file_name is not None:
            return self.log_file_name
        return self.logger_name + "_" + self.DEFAULT_LOG_FILE_NAME

    @property
    def get_backup_count(self):
        """
        Get the user backup file count or use the default backup file count

        Return:
            int: return the number of files that gonna be used as a backup files
        """

        if self.backup_count is not None:
            return self.get_backup_count
        return self.DEFAULT_BACKUP_COUNT

    def get_formatter(self):
        """
        Get the user formatter or use the default one

        Return:
            logging.Formatter: return a logging formatter instance

        """
        if self.formatter is not None:
            if not isinstance(logging.Formatter, self.formatter):
                raise TypeError
            return self.formatter

        formatter = logging.Formatter(
            "%(asctime)s %(created)f %(levelname)s %(message)s"
        )

        return formatter

    def get_handler(self):
        """
        Get the user handler or use the default one

        Return:
            logging.Handler: return a logging handler instance

        """

        if self.handler is not None:
            if not hasattr(logging.handlers, self.handler):
                if not isinstance(
                    getattr(logging.handlers, self.handler.__name__),
                    self.handler,
                ):
                    raise TypeError
                raise TypeError
            return self.handler

        handler = RotatingFileHandler(
            filename=join(self.get_log_file_path, self.get_log_file_name),
            mode="a",  # append file mode
            maxBytes=self.get_log_file_size * 1024 * 1024,  # file size in MB
            backupCount=self.get_backup_count,
        )

        return handler
