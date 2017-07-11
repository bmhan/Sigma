import socket

###############################################################################

# Next tutorial (Port Scanner)

'''
Scans ports, and determines if it is open or closed.

'''

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
server = raw_input ('Enter a server name: ')

def pscan (port):
    try:
        s.connect ((server,port))
        return True
    except:
        return False

for x in range (1,26):
    if pscan (x):
        print ('Port', x, 'is open')
    else:
        print ('Port', x, 'is closed')
