import socket
from binascii import hexlify, unhexlify

test = ["00220000012C03012939511920020C0131190F3235352E3235352E3235352E323535",
    "0000002200000E100301293951001A020C0131190F3235352E3235352E3235352E323535",
    "00000022000007080301293951001A020C0131190F3235352E3235352E3235352E323535",
    "00190000025809016855a50120020702353300053635353030",
    "000e0000012c04011882e9952000",
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 2323))
    s.listen(1)
    connection, address = s.accept()
    buf = connection.recv(1024)
    if len(buf) > 0:
        print("RECV: {}".format(hexlify(buf)))
    print("sending test payloads.")
    for t in test:
        print("SEND: {}".format(t))
        connection.sendall(unhexlify(t))
        buf = connection.recv(1024)
    print("{} tests finished.".format(len(test)))
