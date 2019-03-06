#from connect_nb import Connection
from connect_wifi import Connection


import socks5_proxy 
import socket
import time 



#create Connection object:
connection = Connection()


#case of nb-iot:
#connection.nb_connect()

#wifi configs:
wifi_access_point = 'hacker-point'
wifi_password = 'mahmoud2013'

#case of wifi:
connection.wifi_connect(access_point=wifi_access_point, password=wifi_password)

#proxy configs:
proxy_address = "212.201.8.88"
proxy_port = 1080
remote_dns = True
proxy_username= "pycom_gp"
proxy_password="narrowband2019"
proxy_configs = (proxy_address, proxy_port, remote_dns, proxy_username, proxy_password)

#cloud foundry configs:
application_address = 'nbiotoverproxy.eu-gb.mybluemix.net'
application_port = 80
cf_configs = (application_address, application_port)

#create a socket:
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((proxy_address,proxy_port))
#get the address from the proxy:
proxy_bound_address , proxy_bound_port = socks5_proxy.start_socks5_session(s, proxy_configs , cf_configs)

count = 0
while count < 3 :
    count += 1
    s.send(b"GET /data HTTP/1.1 \r\nHost:nbiotoverproxy.eu-gb.mybluemix.net\r\n\r\n")
    data = s.recv(1024)
    print(data)
    time.sleep(10)

#GO to sleep
s.close()

print('end of main!')
    
