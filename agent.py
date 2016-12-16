import socket
import time
import parser
import config
from logger import Logger
from utils import haxorview
from retrying import retry


class Agent():

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.socket = None
        self.l = Logger("{}-{}_{}".format(__name__, host, port))
        self.stats = {'ping': 0, 'pong': 0, 'commands': 0, 'conn_fails': 0}

    def __SetupSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __ResetSocket(self):
        self.l.debug("Socket reset.")
        self.socket.close()
        self.__SetupSocket()

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=600000)
    def __Connect(self):
        self.l.debug("Connecting to {}:{}".format(self.host, self.port))
        self.__SetupSocket()
        self.socket.connect((self.host, self.port))
        self.l.debug("Connection established.")

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
        self.socket.sendall(b'\x00\x00\x00\x01')
        self.socket.sendall(b'\x00')
        self.l.debug("Hello sent.")

    def __Ping(self):
        self.socket.sendall(b'\x00\x00')
        self.stats['ping'] += 1

    def __Recv(self):
        return self.socket.recv(1024)

    def __Communicate(self):
        self.__Ping()
        data = self.__Recv()
        self.__ProcessReply(data)
        time.sleep(config.ping_interval)
        if not self.stats['ping'] % 100:
            self.l.info("STATS - ping:{ping}/{pong}, cmds:{commands}, \
reconn:{conn_fails}".format(**self.stats))

    def __DoSpy(self):
        self.__SayHello()
        self.l.info("Bot registered.")
        while True:
            try:
                self.__Communicate()
            except (BrokenPipeError, ConnectionRefusedError,
                ConnectionResetError) as e:
                self.stats['conn_fails'] += 1
                self.l.warn("Connection error ({}). Reconnecting...".format(e))
                self.__Connect()

    def Spy(self):
        self.__Connect()
        self.__DoSpy()
