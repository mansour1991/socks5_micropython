"""
Copy rights 2019, Mahmoud Mansour

not every thing tested yet. may contains bugs. use it on your own risk!

You can use either Wifi or NB-IoT

In case you are using a proxy, Ask your admin for username and password!!

"""

#from connect_nb import Connection
from connect_wifi import Connection


import ureqs


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
proxy_address = "xx.xx.xx.xx"
proxy_port = 1080
remote_dns = True
proxy_username= "username"
proxy_password="password"

#proxy setup - if you don't perform this setup, you will communicate without proxy
ureqs.proxy_configs = (proxy_address, proxy_port, remote_dns, proxy_username, proxy_password)

room_id = '1234'
block_id = '1'

#HTTP GET
headers = { 
    'room_id' : room_id,
    'block_id' : block_id
    }

body= {
    'room_id' : room_id,
    'block_id' : block_id
}

#construct our URL:
protocol = "http://"
#protocol = "https://"
host="nbiotoverproxy.eu-gb.mybluemix.net"
port=":80"
path="/data" 

url = protocol + host + port + path

#You can either send your data in the headers or in the body.

#PLEASE, think how you might use the following methods in your project:

#HTTP GET:

#GET is usually used to fethch a respose. it has no body...
r = ureqs.get(url, headers=headers )
#print(r)
print(r.content)
#print(r.text)
#print(r.json)
#print(r.status_code)

#HTTP HEAD

#HEAD is like GET but you fetch http headers only without the body. 
#it's useful when you want to check the status header to know if your resource has been changed or not
#so you don't have to fetch the resource and can reduce the traffic! 

r = ureqs.head(url, json=body , headers=headers)
#print(r)
print(r.content)
#print(r.text)
#print(r.json)
print(r.status_code)

#HTTP POST

#POST is usually used to modify or update a new resource (a new file, an entry in a database..) under the specified path (/data)

r = ureqs.post(url, json=body , headers=headers)
#or: 
#r = ureqs.post(url, data='hello world!!' , headers=headers)
#print(r)
print(r.content)
#print(r.text)
#print(r.json)
#print(r.status_code)


#HTTP PUT
#PUT is usually used to create or to overwrite a new resource (a new file, an entry in a database..) under the specified path (/data)
r = ureqs.put(url, json=body , headers=headers)
#or: 
#r = ureqs.put(url, data='hello world!!' , headers=headers)
#print(r)
print(r.content)
#print(r.text)
#print(r.json)
#print(r.status_code)

#HTTP PATCH
#PATCH is usually used to update partially a resource (a file or an entry in the database). 
#for example, you would pass the changes in the body in a json or xml format..
r = ureqs.patch(url, json=body , headers=headers)
#or: 
#r = ureqs.patch(url, data='hello world!!' , headers=headers)
#print(r)
print(r.content)
#print(r.text)
#print(r.json)
#print(r.status_code)


#HTTP DELETE
#used usually to delete a resource...
r = ureqs.delete(url, json=body , headers=headers)
#or: 
#r = ureqs.delete(url, data='hello world!!' , headers=headers)
# print(r)
print(r.content)
# print(r.text)
# print(r.json)
# print(r.status_code)

#important. Don't forget to call the close method when you finish!!

r.close()

