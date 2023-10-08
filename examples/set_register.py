import argparse, sys

sys.path.append('../')
import robot_comm


parser = argparse.ArgumentParser(description='GE SRTP PLC Communication Test.')
parser.add_argument(action="store", dest='plc_ip', help='IP address of PLC')
parser.add_argument(action="store", dest='reg', help='Register to read or write')
parser.add_argument(action="store", dest='value', help='What value to write to the Register')
args = parser.parse_args()

regtype = ''.join(filter(str.isalpha, args.reg)).upper()
regnum = ''.join(filter(str.isdigit, args.reg))

# connect to the plc
sock = robot_comm.open_socket(args.plc_ip, 18245) 
robot_comm.write_mem(int(regnum), regtype, int(args.value), sock)
print(args.reg.upper() + "   :", robot_comm.decode_register(robot_comm.read_mem(int(regnum), regtype, sock)))

# dont forget to turn out the lights.
sock.close()

