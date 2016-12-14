from binascii import unhexlify as uh
import parser

a = "00220000012C03012939511920020C0131190F3235352E3235352E3235352E323535"
b = "0000002200000E100301293951001A020C0131190F3235352E3235352E3235352E323535"
c = "00000022000007080301293951001A020C0131190F3235352E3235352E3235352E323535"
d = "00190000025809016855a50120020702353300053635353030"

data = (a, b, c, d)

from parser import Parse

def simulate_agent(data):
    m = parser.Parse(data)
    print("Parsed message: {}".format(str(m)))
    print("ATK_VEC_{atk_vec} for {duration} seconds".format(**m._asdict()))
    for t in m.targets:
        print("TARGET: {IP}/{mask}".format(**t._asdict()))
    for o in m.options:
        print("OPTIONS: {var}={val}".format(**o._asdict()))

for d in data:
    d = uh(d)
    print("test: {}\nparsed: {}".format(d, Parse(d)))
    simulate_agent(d)
