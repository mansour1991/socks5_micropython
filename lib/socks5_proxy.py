
"""
copy rights 2019, Mahmoud Mansour

support only SOCKS5 CONNECT request. rewriten for micropython
"""
import usocket 
import ustruct 


class ProxyError (Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GeneralProxyError (ProxyError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Socks5AuthError(ProxyError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Socks5Error(ProxyError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

_generalerrors = (
    "success",
    "invalid data",
    "not connected",
    "not available",
    "bad proxy type",
    "bad input"
)

_socks5errors = (
    "succeeded",
    "general SOCKS server failure",
    "connection not allowed by rulset",
    "Network unreachable",
    "Host unreachable",
    "Connection refused",
    "TTL expired",
    "Command not supported",
    "Address type not supported",
    "unknown error"
)

_socks5autherrors = (
    "succeeded",
    "authentication is required",
    "all offered authentication methods were rejected",
    "unknown username or invalid password",
    "unknown error"
)



def __recvall (socket , bytes):
    """return the data received, (A bocking function!!)"""
    data = b"" 
    while len(data) < bytes:
        data = data + socket.recv(bytes - len(data))
    return data

def _bits_to_dotted_ip(ip):
    list_ = list(ip)
    _ip =  "{}.{}.{}.{}".format(list_[0],list_[1],list_[2],list_[3])
    return _ip


def _dotted_ip_to_bits(ip):
    list_ = ip.split('.')
    _ip = b''
    for i in range(len(list_)) :
        _ip = _ip + ustruct.pack('>B', int(list_[i]))
    return _ip

def start_socks5_session(socket, proxy, cf):
    """ask the proxy server to connect us to the cloud application that is listening on port: destport at IP: destip"""
    destadd = cf[0]
    destport = cf[1]
    # check if the user supplied us with authentication
    if proxy[3]!=None and proxy[4]!=None :
        #=>>> we support both None authentication and authentication with username+password 
        #ToDo: make support for other type of authentication
        socket.sendall(b"\x05\x02\x00\x02")
        #05=the protocol version, 
        #02=number of suported methods (2 in our case) -- see rfc 1928 
        #00 the code for None authentication
        #02 the code for authentication with username and password
    else:
        #we suport only None authentication
        socket.sendall(b"\x05\x01\x00")
    
    chosenauth = list(__recvall(socket, 2)) 
    # the first byte is the socks version. must be 5. the second is the authentication method selected
    if chosenauth[0] != list(b"\x05")[0]:
        socket.close() # bad guys are sitting at the server side
        raise GeneralProxyError((1,_generalerrors[1]))
    if chosenauth[1] == list(b"\x00")[0]:
        pass # No need to send username and password
    elif chosenauth[1] == list(b"\x02")[0]:
        #-> The server selected authetication method with username and password. We should send them :(
        # we should send the following: sub_negotioation version + length of username + username + length of password + password
        _username = proxy[3].encode()
        _password = proxy[4].encode()
        socket.sendall(b"\x01"+chr(len(_username))+ _username +chr(len(_password))+_password)
        #The reply: consistes of 2 bytes. first byte is the sus_negotioation version. second is the answer (Accept, or not) ->
        auth_reply = list(__recvall(socket, 2))
        if auth_reply[0] != list(b"\x01")[0]:
            socket.close() # bad guys are sitting at the server side
            raise GeneralProxyError((1, _generalerrors[1]))
        if auth_reply[1] != list(b"\x00")[0]:
            socket.close() # incorrect username or password!
            raise Socks5AuthError ((3, _socks5autherrors[3]))
    else:
        socket.close() # the server didn't accept our authentication methods :( shit!!
        if chosenauth[1] == list(b"\xff")[0] :
            raise Socks5AuthError((2,_socks5autherrors[2]))
        else:
            raise GeneralProxyError((1,_generalerrors[1])) # the bad guys again
        
            #Ask the proxy to establish a connection with the target Cloud application :)
            #We support only tcp. 
            # ToDo: make support for udp 
    connection_request = b'\x05\x01\x00'  # Version + command (tcp) + reserved byte
    #ToDo: support BIND and UDP assoiciate
    try:
        ipadd = _dotted_ip_to_bits(destadd)
        connection_request = connection_request + b'\x01' + ipadd
    except ValueError:
        #it's not an ip address !!
        if proxy[2] == True :
            #means we want to enable remote dns
            ipadd = None
            connection_request = connection_request + b'\x03'+ chr(len(destadd.encode())) + destadd.encode()
        else:
            #local dns resolving!
            ipadd = _dotted_ip_to_bits(usocket.getaddrinfo(destadd, destport)[0][-1][0])
            connection_request = connection_request + b"\x01" + ipadd
    connection_request = connection_request + ustruct.pack(">H", destport)
    socket.sendall(connection_request)
    #response:
    connection_response = list(__recvall(socket, 4))
    if connection_response[0] != list(b'\x05')[0] :
        socket.close() # bad guys are sitting at the server side
        raise GeneralProxyError((1,_generalerrors[1]))
    elif connection_response [1] != list(b'\x00')[0] :
        socket.close()
        if ord(connection_response[1]) <= 8 :
            raise Socks5Error((ord(connection_response[1]), _generalerrors[ord(connection_response[1])]))
        else:
            raise Socks5Error((9, _generalerrors[9]))
    elif connection_response[3] == list(b'\x01')[0] :
        proxy_bound_address = __recvall(socket, 4)
    elif connection_response[3] == list(b'\x03')[0]:
        connection_response = connection_response + __recvall(socket, 1)
        proxy_bound_address = __recvall(socket, ord(connection_response[4]))
    else:
        socket.close()
        raise GeneralProxyError((1, _generalerrors[1]))
    proxy_bound_port = ustruct.unpack('>H', __recvall(socket, 2)) [0]
    __proxysockname = (_bits_to_dotted_ip(proxy_bound_address), proxy_bound_port) # 32 bit binary ip address (4 bytes) , int port 
    return __proxysockname