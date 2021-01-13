import binascii
import socket
import struct
import time

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


def read_mem(addr, reg, s):
    msg = srtp_message.BASE_MSG.copy()
    msg[42] = srtp_message.SERVICE_REQUEST_CODE["READ_SYS_MEMORY"]
    msg[43] = srtp_message.MEMORY_TYPE_CODE[reg]
    msg[44] = b'\x00'
    if addr > 0:
        msg[44] = binascii.a2b_hex(format(int((addr-1)/8), '02X'))
        if reg == "AI":
            msg[44] = binascii.a2b_hex(format(addr - 1, '02X'))
    msg[45] = int(addr >> 8).to_bytes(1, byteorder='big')
    msg[46] = b'\x01'
    out_bytes = b''.join(msg)

    s.send(out_bytes)
    if addr == 0:
        return struct.unpack('H', bytearray(s.recv(1024)[47:49]))[0]
    if reg == "I" or reg == "Q":
        return format(int(struct.unpack('H', bytearray(s.recv(1024)[44:46]))[0]), '08b')[::-1][(addr-1) % 8]
    return struct.unpack('H', bytearray(s.recv(1024)[44:46]))[0]


def decode(msg):
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

    for a in range(1, 8):
        print("DI", a, "-", read_mem(a, "Q", sock), end=", ")
    print("\n")

    for a in range(1, 8):
        print("DO", a, "-", read_mem(a, "I", sock), end=", ")
    print("\n")

    print("GO11 :", read_mem(11, "AI", sock))

    print("R1   :", read_mem(1, "R", sock))

    # SETVAR $SNPX_ASG[2].$ADDRESS 2001
    # SETVAR $SNPX_ASG[2].$SIZE 3960
    # SETVAR $SNPX_ASG[2].$VAR_NAME "SR[1]"
    response = read_mem(2001, "R", sock)
    print("SR1  :", response)   # TODO

    sock.close()
