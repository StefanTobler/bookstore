from datetime import date


class Logger():
    def log(self, msg):
        print(f"{date.today()}")
        print(msg)


class LoggerInfo(Logger):
    def log(self, msg):
        print(f"{date.today()} INFO:")
        print(msg)


class LoggerError(Logger):
    def log(self, msg):
        print(f"{date.today()} ERROR:")
        print(msg)


class LoggerWarning(Logger):
    def log(self, msg):
        print(f"{date.today()} WARNING:")
        print(msg)


class LoggerFactory():
    def get_logger(self, logtype):
        if logtype == 'INFO':
            return LoggerInfo()
        if logtype == 'ERROR':
            return LoggerError()
        if logtype == 'WARNING':
            return LoggerWarning()
