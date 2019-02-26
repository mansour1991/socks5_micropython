import struct
import socket

#To do : try except!!
def inet_aton_(destaddr):
    list_ = destaddr.split('.')
    ip = b''
    for i in range(len(list_)) :
        ip = ip + struct.pack('>B', int(list_[i]))
    return ip

host = socket.gethostbyname('www.google.com')
print (host)

""" value =  host[0][-1] [0]
print(value)
value = inet_aton_(value)
print(value) """