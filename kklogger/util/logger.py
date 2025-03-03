import sys, logging, io, os, datetime


__all__ = [
    "set_logger",
    "set_loglevel",
    "MyLogger",
    "LoggingNameException",
]


# Save logger name. We can't access name space with "logging"
_list_logname  = []
_dict_loglevel = {"info":logging.INFO, "debug":logging.DEBUG, "warn":logging.WARNING, "error":logging.ERROR}
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s : %(message)s')
_pycolor = {
    "BLACK"     : '\033[30m',
    "RED"       : '\033[31m',
    "GREEN"     : '\033[32m',
    "YELLOW"    : '\033[33m',
    "BLUE"      : '\033[34m',
    "PURPLE"    : '\033[35m',
    "CYAN"      : '\033[36m',
    "WHITE"     : '\033[37m',
    "BOLD"      : '\033[1m',
    "UNDERLINE" : '\033[4m',
    "INVISIBLE" : '\033[08m',
    "REVERCE"   : '\033[07m',        
    "END"       : '\033[0m',
}


class MyFormatter(logging.Formatter):
    """
    Override Formatter's format to suppress the color code
    """
    global _pycolor
    def format(self, record: str) -> str:
        string = super().format(record)
        for x in _pycolor.values(): string = string.replace(x, "")
        return string
_formatter_outfile = MyFormatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s : %(message)s')



class MyLogger(logging.Logger):
    """
    Not used to define instances.
    See "set_logger" function.
    """
    global _pycolor
    def __init__(self):
        super().__init__(self)
        self.internal_stream = io.StringIO()
        self.color_info      = None
        self.color_debug     = None
        self.color_warning   = ["BOLD", "YELLOW"]
        self.color_error     = ["BOLD", "RED"]
    
    def set_message_color(self, msg, level, color):
        if hasattr(sys, "_getframe"):
            # To match function name which I want to use before "info" is called.
            logging.currentframe = lambda: sys._getframe(1)
        if   color is None and level == logging.INFO:    color = self.color_info
        elif color is None and level == logging.WARNING: color = self.color_warning
        elif color is None and level == logging.ERROR:   color = self.color_error
        elif color is None and level == logging.DEBUG:   color = self.color_debug
        if   color is not None:
            addmsg = "".join([_pycolor[x] for x in color]) if isinstance(color, list) else _pycolor[color]
            msg    = addmsg + msg + _pycolor["END"]
        return msg

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, color: str=None):
        super()._log(
            level, self.set_message_color(msg, level, color=color), args, 
            exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=2,
        )

    def raise_error(self, msg: str, exception: Exception = Exception()):
        self.error(f"{type(exception)}: {msg}")
        raise exception

    def set_internal(self):
        """ internal log """
        for x in self.handlers:
            if x.get_name == "internal_logger":
                return None
        self.internal_stream = io.StringIO()
        s_handler = logging.StreamHandler(self.internal_stream)
        s_handler.setFormatter(_formatter)
        s_handler.set_name("internal_logger")
        self.addHandler(s_handler)

    def set_logfile(self, filepath: str):
        """log file"""
        for x in self.handlers:
            if x.get_name == "logfile_logger":
                # If it is already set, do not set it further.
                return None
        # Don't remove under code. I don't know, XXX.%YYYY%%MM%%DD%.log remains
        time      = datetime.datetime.now()
        filepath  = filepath.replace("%YYYY%",time.strftime("%Y")).replace("%MM%",time.strftime("%m")).replace("%DD%",time.strftime("%d"))
        f_handler = logging.FileHandler(filename=filepath)
        f_handler.setFormatter(_formatter_outfile)
        f_handler.set_name("logfile_logger")
        self.addHandler(f_handler)
    
    def close(self):
        handlers: list[logging.Handler] = self.handlers
        for x in handlers:
            if hasattr(x, "close"):
                x.close()


def set_logger(
    name: str, log_level: str="info", 
    internal_log: bool=False, logfilepath: str=None, is_newlogfile: bool=False, is_force: bool=False,
    color_info:    str | list[str] = None,
    color_debug:   str | list[str] = None,
    color_warning: str | list[str] = ["BOLD", "YELLOW"],
    color_error:   str | list[str] = ["BOLD", "RED"],
) -> MyLogger:
    """
    Return the address in the logging namespace
    Params::
        filepath:
            If you want to set the date to the name of the log file, you can use %YYYY%, %MM%,%DD% special string.
    Usage::
        >>> from kklogger.logger import set_logger
        >>> logger = set_logger(__name__)
        >>> logger.info("Test message", color=["BOLD", "GREEN"])
    """
    global _list_logname
    global _dict_loglevel
    global _formatter

    logger: MyLogger = logging.getLogger(name)
    logger.__class__ = MyLogger # Cast
    logger.color_info    = color_info
    logger.color_debug   = color_debug
    logger.color_warning = color_warning
    logger.color_error   = color_error
    if is_force:
        print("\033[33mForce to reset logger.\033[0m")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        if name in _list_logname:
            _list_logname.remove(name)        
    if name in _list_logname:
        logger.warning("Logger already exists.")
    else:
        # stdout
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(_formatter)
        logger.addHandler(s_handler)
        # Unify log output levels
        logger.setLevel(_dict_loglevel[log_level])
        _list_logname.append(name)
        if internal_log:
            logger.set_internal()
        if logfilepath is not None:
            time        = datetime.datetime.now()
            logfilepath = logfilepath.replace("%YYYY%",time.strftime("%Y")).replace("%MM%",time.strftime("%m")).replace("%DD%",time.strftime("%d")).replace("%hh%",time.strftime("%H")).replace("%mm%",time.strftime("%M")).replace("%ss%",time.strftime("%S"))
            if is_newlogfile:
                try: os.remove(logfilepath)
                except FileNotFoundError: pass
            logger.set_logfile(logfilepath)
    return logger

class LoggingNameException(Exception): pass
def set_loglevel(name: str = None, log_level: str = "info"):
    """
    Set log level.
    Params::
        name: log name. If None, change the logger for all names
        log_level: info, debug, warn, error
    Usage::
        >>> set_loglevel(name=None, log_level="debug")
    """
    global _list_logname
    global _dict_loglevel
    if name is None:
        for x in _list_logname:
            logging.getLogger(x).setLevel(_dict_loglevel[log_level])
    else:
        if name in _list_logname:
            logging.getLogger(name).setLevel(_dict_loglevel[log_level])
        else:
            raise LoggingNameException("No name in logging space.")