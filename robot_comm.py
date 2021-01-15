import socket
import struct

import srtp_message


def open_socket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(srtp_message.INIT_MSG)
    init_resp = s.recv(1024)
    if init_resp[0] != 1:
        raise Exception("Init Response: ", init_resp[0])
    init_comm = read_mem(0, "R", s)
    if init_comm == 256:
        return s
    else:
        raise Exception("Communication Fault: ", init_comm)


def read_mem(addr, reg, s, size=1):
    msg = srtp_message.BASE_MSG.copy()
    msg[42] = srtp_message.SERVICE_REQUEST_CODE["READ_SYS_MEMORY"]
    msg[43] = srtp_message.MEMORY_TYPE_CODE[reg]
    msg[44] = b'\x00'
    if addr > 0:
        msg[44] = int(int((addr - 1) / 8) & 255).to_bytes(1, byteorder='big')
        if reg == "AI" or size > 1:
            msg[44] = int(addr - 1 & 255).to_bytes(1, byteorder='big')
        msg[45] = int(addr - 1 >> 8).to_bytes(1, byteorder='big')
    msg[46] = int(size).to_bytes(1, byteorder='big')
    out_bytes = b''.join(msg)

    s.send(out_bytes)
    r = s.recv(1024)

    if addr == 0:  # Init Comm Check
        return struct.unpack('H', bytearray(r[47:49]))[0]
    return r


# Only tested writing strings
def write_mem(addr, reg, var, s):
    msg = srtp_message.BASE_MSG.copy()
    if len(var) % 2:
        fill = True
        var_length = len(var)+1
    else:
        fill = False
        var_length = len(var)
    msg[4] = var_length.to_bytes(1, byteorder='big')
    msg[9] = b'\x02'
    msg[17] = b'\x02'
    msg[30] = b'\x09'
    msg[31] = b'\x80'
    msg[42] = var_length.to_bytes(1, byteorder='big')
    msg[48] = b'\x01'
    msg[49] = b'\x01'
    msg[50] = srtp_message.SERVICE_REQUEST_CODE["WRITE_SYS_MEMORY"]
    msg[51] = srtp_message.MEMORY_TYPE_CODE[reg]
    msg[52] = int(addr - 1 & 255).to_bytes(1, byteorder='big')
    msg[53] = int(addr - 1 >> 8).to_bytes(1, byteorder='big')
    msg[54] = (int(var_length / 2)).to_bytes(1, byteorder='big')
    for x in var:
        msg.append(x.encode('utf8'))
    if fill:
        msg.append(b'\x00')

    out_bytes = b''.join(msg)
    s.send(out_bytes)
    print(decode_packet(out_bytes))
    return s.recv(1024)


# For Decoding Words (GOs and Numeric Registers)
def decode_register(r):
    return struct.unpack('H', bytearray(r[44:46]))[0]


# For decoding DOs and DIs
def decode_bit(r, addr):
    return format(int(struct.unpack('H', bytearray(r[44:46]))[0]), '08b')[::-1][(addr - 1) % 8]


def decode_string(r):
    return r[56:].decode()


def decode_packet(msg):
    iter_len = sum(1 for _ in enumerate(msg))
    out = ""
    for idx, i in enumerate(msg):
        if iter_len - idx <= iter_len:
            out += " {:02x}".format(i)
    return out


if __name__ == '__main__':
    port = 18245
    ip = "127.0.0.1"
    sock = open_socket(ip, port)

    # print("", srtp_message.DEBUG_HEADER)

    # for a in range(1, 17):
    #     print("DI", a, "-", decode_bit(read_mem(a, "Q", sock), a), end=", ")
    # print("\n")
    #
    # for a in range(1, 17):
    #     print("DO", a, "-", decode_bit(read_mem(a, "I", sock), a), end=", ")
    # print("\n")
    #
    # print("GO11 :", decode_register(read_mem(11, "AI", sock)))
    #
    # print("R1   :", decode_register(read_mem(1, "R", sock)))

    # TODO Add String Registers
    # SETVAR $SNPX_ASG[2].$ADDRESS 2001
    # SETVAR $SNPX_ASG[2].$SIZE 3960
    # SETVAR $SNPX_ASG[2].$VAR_NAME "SR[1]"
    # R2001-R2040: String register 1
    # print("SR1  :", decode_string(read_mem(11001, "R", sock, 40)))

    print("", decode_packet(write_mem(11001, "R", "b", sock)))

    sock.close()
