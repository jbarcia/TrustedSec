#!/usr/bin/python
#
#
# This is the actual egressbuster that will connect out from a network to the lisnter
#
# Egressbuster: Written by Dave Kennedy (ReL1K)
#
#
from socket import *
import sys
import time
import thread

# try to import
try:
        ipaddr = sys.argv[1]
        portrange = sys.argv[2]
        portrange = portrange.split("-")
        lowport = int(portrange[0])
        highport = int(portrange[1])        

except IndexError:
        print """
Quick egress buster written by: Dave Kennedy (ReL1K)

NOTE: Only supports a max of 1000 addresses at a time. It will die if
more is used!

Usage:

egressbuster.exe <listener_ip_address> <lowport-highport>

example: egressbuster.exe 10.9.5.2 1-1000
        """
        sys.exit()


# cycle through ranges
base_port = int(lowport)-1
end_port = int(highport)

print "Sending packets to egress listener..."

def start_socket(ipaddr,base_port):

        # try block to catch exceptions        
        try:
                sockobj = socket(AF_INET, SOCK_STREAM)
                sockobj.connect((ipaddr, base_port))
                sockobj.send(str(base_port))
                sockobj.close()
        # if we throw an error
        except Exception, e:
                print e
                # pass through, ports closed
                pass

# loop
while 1:
        base_port = base_port + 1
        thread.start_new_thread(start_socket, (ipaddr,base_port))

        time.sleep(0.02)
        
        if base_port == end_port:
                break

print "All packets have been sent"

