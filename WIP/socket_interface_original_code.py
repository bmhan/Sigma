# -------------------------------------------------------------------------------
# Name:        Socket SCPI interface
# Purpose:     Example IQxstream Python Application
#
# Created:     05/15/2017
# Copyright:   (c) Litepoint 2017
# Licence:     All rights reserved
# -------------------------------------------------------------------------------

import socket
import time

session = None
sessNamePostfix = ''
RECV_BLOCK_SIZE = 1024

def send(cmd, timeout = 30):
    if len(cmd) > 0:
        print ('CMD >> ' + str(cmd))
        if cmd[-1] != '\n':
            cmd += '\n'
    else:
        return ''

    start_time = time.time()
    if cmd.find('?') > 0:
        session.send(cmd[:-1] + '; SESS:NAME?\n')
        ret = session.recv(RECV_BLOCK_SIZE)
        while not ret or ret.find(sessNamePostfix) < 0:
            ret += session.recv(RECV_BLOCK_SIZE)
            if time.time() - start_time > timeout:
                print ('Receiving operation timed out!')
                break

        ret = ret.replace(sessNamePostfix, '')
        print ('RET << ' + str(ret.strip()))
        return ret
    else:
        session.send(cmd)

    return ''


def init(host, port):
    global session, sessNamePostfix
    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    session.connect((host, port),)

	#Conversion of string into bytes
    command = '*IDN?; *RST\n'
    session.send(command.encode())
    print (session.recv(RECV_BLOCK_SIZE))
            
    session.send('SESS:NAME?\n')
    ret = session.recv(RECV_BLOCK_SIZE)    
    while not ret or ret.find('1') < 0:
        ret = session.recv(RECV_BLOCK_SIZE)
    sessNamePostfix = ret


def close():
    session.close()


def setup_vsg(frequency, power):
    send('VSG; FREQ:CENT ' + str(frequency * 1e6))
    send('VSG; POW:LEV ' + str(power))
    send('*OPC?')


def unittest():
    host = '192.168.4.184'  # '192.168.100.254'    # The remote host
    port = 24000  # The same port as used by the server

    init(host, port)

    setup_vsg(2500.0, -50.0)
    send('VSG; POW:STAT ON')
    
    errors = send('SYST:ERR:ALL?')
    print ('Errors reported:', errors)
    
    # SCPI test sequence here

if __name__ == "__main__":
	unittest()

