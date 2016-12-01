table = {
    b'\x00\x00': "CNC_OP_PING",
    b'\x10\x00': "CNC_OP_KILLSELF",
    b'\x20\x00': "CNC_OP_KILLATTKS",
    b'\x30\x00': "CNC_OP_PROXY",
    b'\x40\x00': "CNC_OP_ATTACK",
}

def Resolve(opcode):
    try:
        return table[opcode]
    except IndexError:
        return "CNC_OP_UNKNOWN({})".format(opcode.decode('ascii'))
