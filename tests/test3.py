# main.py -- put your code here!
from connect_nb import Connection
import time
import socket

connection = Connection()

connection.lte_connect()

IP = "212.201.8.88"
PORT = 3000
MESSAGE = 'Hello From NB-IoT'
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(MESSAGE, "utf-8"), (IP, PORT))
# # data = sock.recv(100)
# # print(data)

# from network import LTE
# import time
# import socket
# lte = LTE()
# lte.attach(band=20, apn="nb.inetd.gdsp")
# while not lte.isattached():
#     time.sleep(0.25)
# lte.connect()      
# while not lte.isconnected():
#     time.sleep(0.25)

# print("connected!!")

# IP = "212.201.8.88"
# PORT = 3001       
          
# s = socket.socket()
# s.connect((IP, PORT))
# s.sendall(b'Hello from NB-IoT')
# data = s.recv(1024)
# s.close()
# print('Received', repr(data))