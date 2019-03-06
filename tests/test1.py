"""
Author : Mahmoud Mansour
Purpose : You can use this program to connect a GPy Module through Vodafone NB-LTE Network via a whitelisted SOCKS5 proxy server.
In This way you can target any application server!!   
In order to connect over this server, you need a USERNAME and a PASSWORD as well as the server address and the proxy port number.
Date: Saturday, 16th of February 2019
"""

## Import the proxy socket:
import socks
import socket
from network import LTE
import time
import socket

lte = LTE()
lte.attach(band=20, apn="nb.inetd.gdsp")
while not lte.isattached():
    time.sleep(0.25)
lte.connect()       # start a data session and obtain an IP address
while not lte.isconnected():
    time.sleep(0.25)

print("attatched and connected to LTE network")

## Your application/server IP address and Port Number 
address = "nb-iot.eu-gb.mybluemix.net"
PORT = 80    

## Create the Proxy Socket, Using SOCKS5 , Please ASK  The Proxy Admin for Username and PAssword!          
s = socks.socksocket(family=socket.AF_INET,type=socket.SOCK_STREAM)              
s.set_proxy(proxy_type=socks.SOCKS5,addr="212.201.8.88",port=1080,username="pycom_gp",password="narrowband2019")

## Connect to your preferrd Application/Server
s.connect((address, PORT))
s.send(b"GET /nb HTTP/1.1 \r\nHost:nb-iot.eu-gb.mybluemix.net\r\n\r\n")
data = s.recv(1024)
print(data)
s.close()

