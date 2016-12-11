import socket
import time
#import opcodes
import binascii
import logging
import parser

def setupLogger(loglvl, loggerName):
    logging.basicConfig(level=loglvl)
    l = logging.getLogger(loggerName)
    fh = logging.FileHandler("sp-{}.log".format(loggerName))
    fh.setLevel(loglvl)
    l.addHandler(fh)
    return l

def haxorview(buf):
    buf = binascii.hexlify(buf).decode('ascii')
    return " ".join(buf[i:i+2] for i in range(0, len(buf), 2))

class Agent():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.l = setupLogger("INFO", "agent-{}-{}".format(self.host, self.port))
        self.stats = {'ping': 0, 'pong': 0, 'commands': 0}
    def __ProcessReply(self, data):
        hex_data = haxorview(data)
        self.l.debug("{} bytes recv: {}".format(len(data), hex_data))
        if len(hex_data) < 4:
            self.l.debug("{}".format(msg))
            self.stats['pong'] += 1
        else:
            self.stats['commands'] += 1
            try:
                msg = parser.Parse(data)
                l.warning("GOT: {}".format(msg))
                l.info("HEX DUMP:\n{}".format(hex_data))
            except:
                l.error("Unable to parse:\n{}".format(hex_data))
    def __SayHello(self):
        self.s.sendall(b'\x00\x00\x00\x01')
        self.s.sendall(b'\x00')
        self.l.debug("Hello sent.")
    def __Ping(self):
        self.s.sendall(b'\x00\x00')
        self.stats['ping'] += 1
    def __Recv(self):
        return self.s.recv(1024)
    def Spy(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect((self.host, self.port))
            self.l.info("Connected.")
            self.__SayHello()
            while True:
                self.__Ping()
                data = self.__Recv()
                self.__ProcessReply(data)
                time.sleep(10)
                if not self.stats['ping'] % 100:
                    self.l.info("STATS - ping:{ping}/{pong}, commands:{commands}\
                        ".format(**self.stats))
