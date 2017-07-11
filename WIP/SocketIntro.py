import socket

#Python Tutorial (Introduction)


#INET tells you what kind of connection 
#SOCK_STREAM allows you to make a TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(s)

'''
What server we want to access, in this case a website
You can access a socket using the domain name, but the
formal way is to get the IP Address
You can do:

server_ip = socket.gethostbyname(server)
print (server_ip)

or do:

ping server (from command line)

'''


server = 'pythonprogramming.net'
port = 80


request = "GET / HTTP/1.1\nHost: " + server + "\n\n"
s.connect ( (server, port))



'''
NOTE: in 2.7, you use strings
      in 3, you use byte strings using encode()
'''

s.send(request)
result = s.recv (4096)
print (result)



