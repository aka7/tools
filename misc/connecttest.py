#!/usr/bin/env python
# simple connect test, to see if a tcp port is open on a given address.
# Provide address and port as first argument, comma seperated.  
# python connectest.py ip,port
# 
# add multiple lines in a file
# exmaple
# cat connectest.txt
# 10.10.10.10,22
# 10.10.10.11,639
# 
# run in for loop:
# for url in $(cat connecttest.txt ); do python connecttest.py $url; done
#

import socket
import sys
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1.0)

if len(sys.argv) != 2:
	print "Usage: $0 ip,port"
	sys.exit(1)
address = sys.argv[1].split(',')[0]
port = int(sys.argv[1].split(',')[1])
result=s.connect_ex((address,port))
s.close()
if result:
	print address,"("+str(port)+") ,Fail"
else:
	print address,"("+str(port)+") ,Success"
