import logging
import config
from os import mkdir


class Logger():

    def __init__(self, mod_name):
        self._CreateLogDir()
        self.mod_name = mod_name
        self.logger = logging.getLogger(mod_name)
        self.logger.setLevel(config.log_level)
        self.logger.addHandler(self._GetConsoleHandler())
        self.logger.addHandler(self._GetFileHandler())

    def _CreateLogDir(self):
        try:
            mkdir(config.log_dir)
        except FileExistsError:
            pass

    def _GetConsoleHandler(self):
        formatter = logging.Formatter(config.console_log_format)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        return ch

    def _GetFileHandler(self):
        formatter = logging.Formatter(config.file_log_format)
        fh = logging.FileHandler("{}/spyrai-{}.log".format(config.log_dir,
            self.mod_name))
        fh.setFormatter(formatter)
        fh.setLevel(config.log_level)
        return fh

    def debug(self, buf):
        self.logger.debug(buf)

    def info(self, buf):
        self.logger.info(buf)

    def warn(self, buf):
        self.logger.warn(buf)

    def error(self, buf):
        self.logger.error(buf)

    def critical(self, buf):
        self.logger.critical(buf)
