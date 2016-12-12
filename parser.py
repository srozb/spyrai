from struct import unpack
from netaddr import IPAddress

def Parse(buf):
    #duration, unkb1, unkb2, unkint1 = unpack("<IBBI", buf[:6])
    duration = unpack(">I", buf[4:8])[0]
    t_count = buf[9]
    t_ip = str(IPAddress((unpack(">I", buf[10:14]))[0]))
    t_mask = buf[14]
    return "DURATION: {}s, target count: {}, target: {}/{}".format(
        duration, t_count, t_ip, t_mask)
    #print(duration, attack_id, attack_count)
    raise Exception("Unimplemented")
