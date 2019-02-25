from connect_nb import Connection
#from connect_wifi import Connection

import usocket
import time 



connection = Connection()
connection.nb_connect()

IP = "212.201.8.88"
PORT = 3001

sock = usocket.socket()
sock.settimeout(None)

sock.connect((IP, PORT))

count = 0
while count < 3 :
    count += 1
    sock.sendall('Hi')
    time.sleep(10)

#GO to sleep
sock.close()
connection.nb_disconnect()

print('end of main!')
    
