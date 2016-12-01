import socket
import time
import opcodes

DEBUG = True

def haxorview(buf):
    return " ".join("{:02x}".format(ord(c)) for c in buf)

class Agent():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
    def __ProcessReply(self, data):
        if DEBUG:
            hex_data = haxorview(data.decode())
            print("{} bytes recv: {}".format(len(data), hex_data))
        msg = opcodes.Resolve(data)
        print("{}".format(msg))
    def __SayHello(self):
        self.s.sendall(b'\x00\x00\x00\x01')
        self.s.sendall(b'\x00')
    def __Ping(self):
        self.s.sendall(b'\x00\x00')
    def __Recv(self):
        return self.s.recv(1024)
    def Spy(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect((self.host, self.port))
            self.__SayHello()
            while True:
                self.__Ping()
                data = self.__Recv()
                self.__ProcessReply(data)
                time.sleep(10)
