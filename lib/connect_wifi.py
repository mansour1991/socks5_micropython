import network 

class Connection:
    def __init__(self):
        self.wifi_client = network.WLAN(network.STA_IF)

    def wifi_connect(self, access_point, password):
        if not self.wifi_client.isconnected():
            print('enabling WLAN interface as Wifi Station (client)')
            self.wifi_client.active(True)
               
        while not self.wifi_client.isconnected():
            try:
                self.wifi_client.connect(access_point, password)
            except Exception:
                print('Got an exception !!!')
            
            print("Obtained IP address...\n", self.wifi_client.ifconfig())