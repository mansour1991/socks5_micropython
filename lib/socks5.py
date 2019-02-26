"""
The author wrote this module to be used in the following scenario:
        NarrowBand IoT device
                |
                Y
        Vodafone LTE Infrastrucutre
                |
                Y 
        Whitlisted Server (Socks5 proxy server)
                |
                Y
        Application on Cloud foundry
        """
import usocket 
import ustruct 


_defaultproxy = None
_orgsocket = usocket.socket

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

def setdefaultproxy (addr=None, port=None, rdns=True, username=None, password=None):
    """Setting the default proxy"""
    global _defaultproxy
    _defaultproxy = (addr, port, rdns, username, password)

class Socks5 (usocket.socket):
    """return a socket object"""

    def __init__(self, family=usocket.AF_INET, type=usocket.SOCK_STREAM, proto=0 ):
        _orgsocket.__init__(self, family, type, proto)
        if _defaultproxy != None:
            self.__proxy = _defaultproxy
        else:
            self.__proxy = (None, None, None, None, None)
        self.__proxysockname = None
        self.__proxypeername = None

    def __recvall (self, bytes):
        """return the data received, (A bocking function!!)"""
        data = "" 
        while len(data) < bytes:
            data = data + self.recv(bytes - len(data))
        return data
    
    def setproxy (self, addr=None, port=None, rdns=True, username=None, password=None):
        """
        addr: server IP address or name. 
        port: server port
        rdns: remote dns (optional), default True (perform remote dns) ToDo: Configure the proxy server to use a suitable DNS sever
        username, password : self-explanatory. default to use no authentication
        """
        self.__proxy = (addr, port, rdns, username, password)
    
    def _inet_aton_(self, destaddr):
        list_ = destaddr.split('.')
        ip = b''
        for i in range(len(list_)) :
            ip = ip + ustruct.pack('>B', int(list_[i]))
        return ip

    def __start_socks5_session(self, destadd, destport):
        """ask the proxy server to connect us to the cloud application that is listening on port: destport at IP: destip"""
        
        # check if the user supplied us with authentication
        if self.__proxy[3]!=None and self.__proxy[4]!=None :
            #=>>> we support both None authentication and authentication with username+password 
            #ToDo: make support for other type of authentication
            self.sendall(b"\x05\x02\x00\x02")
            #05=the protocol version, 
            #02=number of suported methods (2 in our case) -- see rfc 1928 
            #00 the code for None authentication
            #02 the code for authentication with username and password
        else:
            #we suport only None authentication
            self.sendall(b"\x05\x01\x00")
        
        chosenauth = self.__recvall(2)  
        # the first byte is the socks version. must be 5. the second is the authentication method selected
        if chosenauth[0] != b"\x05":
            self.close() # bad guys are sitting at the server side
            raise GeneralProxyError((1,_generalerrors[1]))
        if chosenauth[1] == b"\x00":
            pass # No need to send username and password
        elif chosenauth[1] == b"\x02":
            #-> The server selected authetication method with username and password. We should send them :(
            # we should send the following: sub_negotioation version + length of username + username + length of password + password
            _username = self.__proxy[3].encode()
            _password = self.__proxy[4].encode()
            self.sendall(b"\x01"+chr(len(_username))+ _username +chr(len(_password))+_password)
            #The reply: consistes of 2 bytes. first byte is the sus_negotioation version. second is the answer (Accept, or not) ->
            auth_reply = self.__recvall(2)
            if auth_reply[0] != b"\x01":
                self.close() # bad guys are sitting at the server side
                raise GeneralProxyError((1, _generalerrors[1]))
            if auth_reply[1] != b"\x00":
                self.close() # incorrect username or password!
                raise Socks5AuthError ((3, _socks5autherrors[3]))
        else:
            self.close() # the server didn't accept our authentication methods :( shit!!
            if chosenauth[1] == b"\xff" :
                raise Socks5AuthError((2,_socks5autherrors[2]))
            else:
                raise GeneralProxyError((1,_generalerrors[1])) # the bad guys again
            
                #Ask the proxy to establish a connection with the target Cloud application :)
                #We support only tcp. 
                # ToDo: make support for udp 
        connection_request = b'\x05\x01\x00'  # Version + command (tcp) + reserved byte
        #ToDo: support BIND and UDP assoiciate
        try:
            ipadd = self._inet_aton_(destadd)
            connection_request = connection_request + b'\x01' + ipadd
        except ValueError:
            #it's not an ip address !!
            if self.__proxy[2] == True :
                #means we want to enable remote dns
                ipadd = None
                connection_request = connection_request + b'\x03'+ chr(len(destadd.encode())) + destadd.encode()
            else:
                #local dns resolving!
                ipadd = self._inet_aton_(usocket.getaddrinfo(destadd, destport)[0][-1][0])
                connection_request = connection_request + b"\x01" + ipadd
        connection_request = connection_request + ustruct.pack(">H", destport)
        self.sendall(connection_request)
        #response:
        connection_response = self.__recvall(4)
        if connection_response[0] != b'\x05' :
            self.close() # bad guys are sitting at the server side
            raise GeneralProxyError((1,_generalerrors[1]))
        elif connection_response [1] != b'\x00' :
            self.close()
            if ord(connection_response[1]) <= 8 :
                raise Socks5Error((ord(connection_response[1]), _generalerrors[ord(connection_response[1])]))
            else:
                raise Socks5Error((9, _generalerrors[9]))
        elif connection_response[3] == b'\x01' :
            proxy_bound_address = self.__recvall(4)
        elif connection_response[3] == b'\x03':
            connection_response = connection_response + self.__recvall(1)
            proxy_bound_address = self.__recvall(ord(connection_response[4]))
        else:
            self.close()
            raise GeneralProxyError((1, _generalerrors[1]))
        proxy_bound_port = usocket.unpack('>H', self.__recvall(2)) [0]
        self.__proxysockname = (proxy_bound_address, proxy_bound_port) # 32 bit binary ip address (4 bytes) , int port 
        return self.__proxysockname
    def connect (self, destpair):
        """To connect to the application server (Cloud foundry) through a proxy
        destpair in tuple or list format: (ip/dns in string format , port in int format)
        call setproxy to connect over proxy otherwise you call directlly without proxy
        """
        if (type(destpair) in (list, tuple) == False) or (len(destpair)<2) or (type(destpair[0]) != str) or (type(destpair[1]) != int): 
            raise GeneralProxyError((5, _generalerrors[5]))
        if self.__proxy[0] != None and self.__proxy[1] != None :
            _orgsocket.connect(self, usocket.getaddrinfo(self.__proxy[0],self.__proxy[1])[0][-1])
            self.__start_socks5_session(destpair[0],destpair[1])
        elif self.__proxy[0] == None and self.__proxy[1] == None :
            _orgsocket.connect(self, usocket.getaddrinfo(self.__proxy[0],self.__proxy[1])[0][-1] )
        else:
            raise GeneralProxyError ((4, _generalerrors[4]))

