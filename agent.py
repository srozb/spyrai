import socket
import time
import parser
from logger import Logger
from utils import haxorview


class Agent():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.l = Logger("{}-{}_{}".format(__name__, host, port))
        self.stats = {'ping': 0, 'pong': 0, 'commands': 0}
    def __ProcessReply(self, data):
        hex_data = haxorview(data)
        self.l.debug("{} bytes recv, hexdump:\n{}".format(len(data), hex_data))
        if len(data) < 4:
            self.stats['pong'] += 1
        else:
            self.stats['commands'] += 1
            try:
                m = parser.Parse(data)
                self.l.debug("Parsed message: {}".format(str(m)))
                self.l.warn("ATK_VEC_{atk_vec} for {duration} seconds\
                    ".format(**m._asdict()))
                for t in m.targets:
                    self.l.warn("TARGET: {IP}/{mask}".format(**t._asdict()))
                for o in m.options:
                    self.l.warn("OPTIONS: {var}={val}".format(**o._asdict()))
            except:
                self.l.error("Unable to parse:\n{}".format(hex_data))
    def __SayHello(self):
        self.s.sendall(b'\x00\x00\x00\x01')
        self.s.sendall(b'\x00')
        self.l.debug("Hello sent.")
    def __Ping(self):
        self.s.sendall(b'\x00\x00')
        self.stats['ping'] += 1
    def __Recv(self):
        return self.s.recv(1024)
    def __Communicate(self):
        self.__Ping()
        data = self.__Recv()
        self.__ProcessReply(data)
        time.sleep(10)
        if not self.stats['ping'] % 100:
            self.l.info("STATS - ping:{ping}/{pong}, commands:{commands}\
                ".format(**self.stats))
    def Spy(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect((self.host, self.port))
            self.l.info("Connected.")
            self.__SayHello()
            while True:
                self.__Communicate()
