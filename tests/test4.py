import struct
import socket

#To do : try except!!
def inet_aton_(destaddr):
    list_ = destaddr.split('.')
    ip = b''
    for i in range(len(list_)) :
        ip = ip + struct.pack('>B', int(list_[i]))
    return ip

def _inet_ntoa_(ip):
    list_ = list(ip)
    _ip =  "{}.{}.{}.{}".format(list_[0],list_[1],list_[2],list_[3])
    return _ip

host = socket.gethostbyname('www.google.com')
print (host)

print(_inet_ntoa_(b'\xd4\xc9\x08X'))

""" value =  host[0][-1] [0]
print(value)
value = inet_aton_(value)
print(value) """