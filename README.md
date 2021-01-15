# Fanuc_GESRTP_Driver
Python 3 communication driver for reading and writing data to Fanuc Robots with HMI Device (SNPX) Option R553.

This was created in hopes to emulate Kepware's GE FANUC driver



## Read / Write Example:
```
sock = open_socket("127.0.0.1", 18245)
write_mem(1, "R", 32767, sock)
print("R1   :", decode_register(read_mem(1, "R", sock)))
sock.close()
```



## Reading Strings:
Inside your SNPX_ASG System Variable on the robot, configure the memory address

    - SETVAR $SNPX_ASG[X].$ADDRESS 2001
    - SETVAR $SNPX_ASG[X].$SIZE 3960    
    - SETVAR $SNPX_ASG[X].$VAR_NAME "SR[1]"    
    - *R2001-R2040: String register 1*
    
```
write_mem(2001, "R", "Hello World.", sock)
print("Wrote \"%s\" to SR1" % decode_string(read_mem(11001, "R", sock, 40)))
```



## Notes on Numeric Registers
- Write range for numeric registers is from -32768 to 32767
- Even though 65535 is the highest number you can read.
- Probably wont read floats when SNPX_ASG[X].$MULTIPLY is 0
- Tested with $MULTIPLY set to 1 (Signed 16 bit)



## Credits
[Research Paper on GE SRTP Protocol](https://www.sciencedirect.com/science/article/pii/S1742287617301925?via%3Dihub)

[C# Library](https://github.com/kkuba91/uGESRTP)

[Python Library](https://github.com/TheMadHatt3r/ge-ethernet-SRTP)

[C++ Library](https://github.com/sharonh102/gesrtp_session_simulator)

[Wireshark](https://www.wireshark.org/)
