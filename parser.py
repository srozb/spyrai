from struct import unpack
from netaddr import IPAddress
from collections import namedtuple


ATK_VEC = ["UDP", "VSE", "DNS", "SYN", "ACK", "STOMP", "GREIP", "GREETH",
"PROXY", "UDP_PLAIN", "HTTP"]

ATK_OPT = ["PAYLOAD_SIZE", "PAYLOAD_RAND", "IP_TOS", "IP_IDENT", "IP_TTL",
"IP_DF", "SPORT", "DPORT", "DOMAIN", "DNS_HDR_ID", "TCPCC", "URG", "ACK", "PSH",
"RST", "SYN", "FIN", "SEQRND", "ACKRND", "GRE_CONSTIP", "METHOD", "POST_DATA",
"PATH", "HTTPS", "CONNS", "SOURCE"]

#Prepare structures
Target = namedtuple("Target", "IP mask")
Opts = namedtuple("Options", "var val_len val")
Message = namedtuple("Message", "duration atk_vec targets options")

def _RemoveLeadingBytesIfNeeded(buf):
    if len(buf) == unpack(">H", buf[2:4])[0] + 2:
        #need to remove 2 leading bytes - probably ping reply
        return buf[2:]
    elif len(buf) != unpack(">H", buf[0:2])[0]:
        #reported len != recv len so give up.
        raise Exception("couldn't determine message length.")
    #no need to do anything.
    return buf

def _ParseTargets(buf):
    targets = []
    targets_len = buf[0]
    buf = buf[1:]
    for i in range(targets_len):
        ip = str(IPAddress((unpack(">I", buf[:4]))[0]))
        mask = buf[4]
        targets.append(Target(ip, mask))
        buf = buf[5:]
    return targets

def _ParseOpts(buf):
    opts = []
    opts_len = buf[0]
    buf = buf[1:]
    for i in range(opts_len):
        try:
            var = ATK_OPT[buf[0]]
        except IndexError:
            var = buf[0]
        val_len = buf[1]
        try:
            val = buf[2:2+val_len].decode('ascii')
        except:
            val = str(buf[2:2+val_len])
        opts.append(Opts(var, val_len, val))
        buf = buf[2+val_len:]
    return opts

def Parse(buf):
    buf = _RemoveLeadingBytesIfNeeded(buf)
    duration = unpack(">I", buf[2:6])[0]
    atk_vec = ATK_VEC[buf[6]]
    targets = _ParseTargets(buf[7:])
    options = _ParseOpts(buf[8+5*len(targets):])
    return Message(duration, atk_vec, targets, options)
