import socket

#INET tells you what kind of connection 
#SOCK_STREAM allows you to make a TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(s)

'''
What server we want to access, in this case a website
You can access a socket using the domain name, but the
formal way is to get the IP Address
You can do:

server_ip = socket.gethsotbyname(server)

or do:

ping server (from command line)

'''

server = 'pythonprogramming.net'
port = 80
