import native_appy
import sys

__buffer__ = []

class LogcatWriter:
    VERBOSE = 2
    DEBUG = 3
    INFO = 4
    WARN = 5
    ERROR = 6
    FATAL = 7
    
    def __init__(self, lvl):
        self.lvl = lvl
        self.buf = b''
        self.crash_handler = None
        
    def write(self, s):
        if isinstance(s, str):
            s = s.encode()
        self.buf = self.buf + s
        while True:
            i = self.buf.find(b'\n')
            if i == -1:
                break
            b = self.buf[:i]
            __buffer__.append(b)
            native_appy.logcat_write(self.lvl, b'APPY', b)
            self.buf = self.buf[i + 1:]

    @property
    def fileno(self):
        if self.crash_handler is None:
            self.crash_handler = open('/sdcard/crash.txt', 'wb')
        return self.crash_handler.fileno

    def isatty(self):
        return False

    def flush(self):
        self.write('\n')
            
sys.stdout = LogcatWriter(LogcatWriter.INFO)
sys.stderr = LogcatWriter(LogcatWriter.ERROR)

def buffer():
    return __buffer__[:]