import argparse, sys

sys.path.append('../')
import robot_comm


parser = argparse.ArgumentParser(description='GE SRTP PLC Communication Test.')
parser.add_argument(action="store", dest='plc_ip', help='IP address of PLC')
parser.add_argument(action="store", dest='reg', help='Register to read or write', default='ALLTHETHINGS')
args = parser.parse_args()


# connect to the plc
sock = robot_comm.open_socket(args.plc_ip, 18245) 

for i in args.reg.split(","):
  regtype = ''.join(filter(str.isalpha, i)).upper()
  regnum = ''.join(filter(str.isdigit, i))
  print(i + "\t ", robot_comm.decode_register(robot_comm.read_mem(int(regnum), regtype, sock)))

# dont forget to turn out the lights.
sock.close()

