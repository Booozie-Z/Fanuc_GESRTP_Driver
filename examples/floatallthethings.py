import argparse, sys

sys.path.append('../')
import robot_comm

parser = argparse.ArgumentParser(description='GE SRTP PLC Communication Test.')
parser.add_argument(action="store", dest='plc_ip', help='IP address of PLC')
args = parser.parse_args()

# connect to the plc
sock = robot_comm.open_socket(args.plc_ip, 18245) 
for reg in range(1,1025):
  data = robot_comm.decode_float(robot_comm.read_mem(reg, "R", sock))
  
  print("R"+ str(reg) + "   :" + str(data))

# dont forget to turn out the lights.
sock.close()

