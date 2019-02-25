"""The yuthor wrote this module to be used in the following scenario:
        NarrowBand IoT device ->
        Vodafone LTE Infrastrucutre -> 
        Whitlested Server ->
        Application on Cloud foundry ->

#         """
import usocket 
import ustruct 

#in the future, we will support more than one type of proxy
PROXY_TYPE_SOCKS_5 = 1

_defaultproxy = None
_orgsocket = None