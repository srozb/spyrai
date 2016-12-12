from struct import unpack
from netaddr import IPAddress

ATK_VEC = {
    0:  "UDP",
    1:  "VSE",
    2:  "DNS",
    3:  "SYN",
    4:  "ACK",
    5:  "STOMP",
    6:  "GREIP",
    7:  "GREETH",
    8:  "PROXY",
    9:  "UDP_PLAIN",
    10: "HTTP",
}

def Parse(buf):
    #duration, unkb1, unkb2, unkint1 = unpack("<IBBI", buf[:6])
    duration = unpack(">I", buf[4:8])[0]
    atk_vec = ATK_VEC[buf[8]]
    t_count = buf[9]
    t_ip = str(IPAddress((unpack(">I", buf[10:14]))[0]))
    t_mask = buf[14]
    return "DURATION: {}s, ATK_VEC_{}, target count: {}, target: {}/{}".format(
        duration, atk_vec, t_count, t_ip, t_mask)
    #print(duration, attack_id, attack_count)
    raise Exception("Unimplemented")
