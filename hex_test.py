import binascii
import struct


addr = 1
# print(bytes.fromhex(format(int(struct.unpack('H', bytearray(binascii.a2b_hex(format(address, '04X'))))[0]), '04X')))
# print(bytes.fromhex(format(binascii.a2b_hex(format(address, '04X').encode('utf8'))[0], '02X')))
# print(bytes.fromhex(format(binascii.a2b_hex(format(address, '04X').encode('utf8'))[1], '02X')))

# a1 = binascii.a2b_hex(format(address, '02X'))
# addr = int((addr-1)/8)
# print(addr)

# a1 = int(addr-1 & 255).to_bytes(1, byteorder='big')
# a2 = int(addr-1 >> 8).to_bytes(1, byteorder='big')

# print(a1, a2)

# print(int(40).to_bytes(1, byteorder='big'))

# for s in "abcd":
#     print((s.encode('utf8').hex()))

var = "bbb"
# for x in range(len(var)):
#     print(56+x, var[x].encode('utf8').hex())

if len(var) % 2:
    x = (len(var)+1).to_bytes(1, byteorder='big')
else:
    x = (len(var)).to_bytes(1, byteorder='big')
print(x)