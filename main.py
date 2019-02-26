#from connect_nb import Connection
from connect_wifi import Connection

#import usocket

import socks5
import time 



#create Connection object:
connection = Connection()


#case of nb-iot:
#connection.nb_connect()

#case of wifi:
connection.wifi_connect(access_point='hacker-point', password='mahmoud2013')

IP = "212.201.8.88"
PORT = 3001

sock = socks5.Socks5()
sock.setproxy(addr="212.201.8.88", port=1080, rdns=True, username="pycom_gp", password="narrowband2019" )
sock.connect(('212.201.8.88',3001))
#sock.settimeout(None)
#sock.connect((IP, PORT))

count = 0
while count < 3 :
    count += 1
    sock.sendall('Hi')
    data = sock.recv(1)
    print(data)
    time.sleep(10)

#GO to sleep
sock.close()
#connection.nb_disconnect()

print('end of main!')
    
