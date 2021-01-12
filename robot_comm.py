import binascii
import socket
import struct
import time

import srtp_message

port = 18245
ip = "127.0.0.1"


def open_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(srtp_message.INIT_MSG)
    init_resp = s.recv(1024)
    if init_resp[0] != 1:
        raise Exception("Init Response: ", init_resp[0])
    init_comm = read_go(0, s)
    if init_comm == 256:
        return s
    else:
        raise Exception("Communication Fault: ", init_comm)


def read_go(addr, s):
    msg = srtp_message.BASE_MSG.copy()
    msg[42] = srtp_message.SERVICE_REQUEST_CODE["READ_SYS_MEMORY"]
    msg[43] = srtp_message.MEMORY_TYPE_CODE["AI"]
    msg[44] = b'\x00'
    if addr > 0:
        msg[44] = binascii.a2b_hex(format(addr-1, '02X'))
    msg[45] = int(addr >> 8).to_bytes(1, byteorder='big')
    msg[46] = b'\x01'
    out_bytes = b''.join(msg)

    s.send(out_bytes)
    if addr == 0:
        return struct.unpack('H', bytearray(s.recv(1024)[47:49]))[0]
    return struct.unpack('H', bytearray(s.recv(1024)[44:46]))[0]


def decode(msg):
    iter_len = sum(1 for _ in enumerate(msg))
    out = ""
    for idx, i in enumerate(msg):
        if iter_len - idx <= iter_len:
            out += " {:02x}".format(i)
    return out


if __name__ == '__main__':
    sock = open_socket()
    for itr in range(100):
        print("GO11:", read_go(11, sock))
        print("GO13:", read_go(13, sock))
        print("GO15:", read_go(15, sock))
        print("GO17:", read_go(17, sock))
        print("GO19:", read_go(19, sock))
        print("GO20:", read_go(20, sock))
        time.sleep(1)

    sock.close()
