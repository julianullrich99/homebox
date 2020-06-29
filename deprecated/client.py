# Echo client program
import socket
import sys



HOST = '127.0.0.1'                 # Symbolic name meaning the local host
PORT = 44148                        # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
r = sys.argv[1]
g = sys.argv[2]
b = sys.argv[3]
txt = ('{"type":"light","action":"start","color":[%s, %s, %s]}' % (r,g,b))

s.send(txt)
data = s.recv(1024)
s.close()
print 'Received', repr(data)
