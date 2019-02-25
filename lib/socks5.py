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
import struct 


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

    def __init__(self, family=usocket.AF_INET, type=usocket.SOCK_STREAM, proto=0, _sock=None ):
        _orgsocket.__init__(self, family, type, proto, _sock)
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

    def __start_socks5_session(self, destadd, destport):
        """ask the proxy server to connect us to the cloud application that is listening on port: destport at IP: destip"""
        
        # check if the user supplied us with authentication
        if self.__proxy[3]!=None and self.__proxy[4]!=None :
            #=>>> we support both None authentication and authentication with username+password 
            #ToDo: make support for other type of authentication
            self.sendall("\x05\x02\x00\x02")
            #05=the protocol version, 
            #02=number of suported methods (2 in our case) -- see rfc 1928 
            #00 the code for None authentication
            #02 the code for authentication with username and password
        else:
            #we suport only None authentication
            self.sendall("\x05\x01\x00")
        
        chosenauth = self.__recvall(2)  
        # the first byte is the socks version. must be 5. the second is the authentication method selected
        if chosenauth[0] != "\x05":
            self.close() # bad guys are sitting at the server side
            raise GeneralProxyError((1,_generalerrors[1]))
        if chosenauth[1] == "\x00":
            pass # No need to send username and password
        elif chosenauth[1] == "\x02":
            #-> The server selected authetication method with username and password. We should send them :(
            # we should send the following: sub_negotioation version + length of username + username + length of password + password
            self.sendall("\x01"+chr(len(self.__proxy[3]))+self.__proxy[3]+chr(len(self.__proxy[4]))+self.__proxy[4])
            #The reply: consistes of 2 bytes. first byte is the sus_negotioation version. second is the answer (Accept, or not) ->
            auth_reply = self.__recvall(2)
            if auth_reply[0] != "\x01":
                self.close() # bad guys are sitting at the server side
                raise GeneralProxyError((1, _generalerrors[1]))
            if auth_reply != "\x00":
                self.close() # incorrect username or password!
                raise Socks5AuthError ((3, _socks5autherrors[3]))
            else:
                self.close() # the server didn't accept our authentication methods :( shit!!
                if chosenauth[1] == "\xff" :
                    self.close()
                    raise Socks5AuthError((2,_socks5autherrors[2]))
                else:
                    raise GeneralProxyError((1,_generalerrors[1])) # the bad guys again
                
                #Ask the proxy to establish a connection with the target Cloud application :)
                #We support only tcp. 
                # ToDo: make support for udp 
                connection_request = "\0x5\0x01\0x00" # Version + command (tcp) + reserved byte
                 
