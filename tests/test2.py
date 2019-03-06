from network import LTE
import time
import socket
lte = LTE()
lte.attach(band=20, apn="nb.inetd.gdsp")
while not lte.isattached():
    time.sleep(0.25)
lte.connect()      
while not lte.isconnected():
    time.sleep(0.25)

print("connected!!")


IP = socket.gethostname()
PORT = 3001                  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.sendall(b'Hello, world')
data = s.recv(1024)
s.close()
print('Received', repr(data))