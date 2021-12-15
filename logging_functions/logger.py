import logging
import getpass
user = getpass.getuser()


class logger():

    def __init__(self, LoggerName=__name__):
        self.logger = logging.getLogger(LoggerName)
        self.user = user
    # * below you can find an example of how to add an extra
    # * queryable parameter to the syslog message 
    # def logDebug(self, msg, controllerIp=None):
    #    extras = dict({'ip': controllerIp})
    #    self.logger.debug(msg, extra=extras)

    def log_debug(self, msg: str):
        extras = dict({'user': self.user})
        self.logger.debug(msg, extra=extras)

    def log_info(self, msg: str):
        extras = dict({'user': self.user})
        self.logger.info(msg, extra=extras)


    def log_warning(self, msg: str):
        extras = dict({'user': self.user})
        self.logger.warning(msg, extra=extras)


    def log_error(self, msg: str):
        extras = dict({'user': self.user})
        self.logger.error(msg, extra=extras)


    def log_critical(self, msg: str):
        extras = dict({'user': self.user})
        self.logger.critical(msg, extra=extras)


    def log_exception(self, msg: str):
        extras = dict({'user': self.user})
        self.logger.exception(msg, extra=extras)

