"""Copy rights 2019, Mahmoud Mansour"""
import network 
import time

class Connection:
    def __init__(self):
        self.wlan_client = network.WLAN(mode=network.WLAN.STA)

    def wifi_connect(self, access_point, password):
        counter = 0
        print('Attatching to WLAN network')
        if not self.wlan_client.isconnected():
            self.wlan_client.connect(ssid=access_point, auth=(network.WLAN.WPA2, password))
        while not self.wlan_client.isconnected():
            if counter >= 10:
                import machine 
                machine.reset()
            time.sleep(1)
            counter = counter + 1
            print(str(counter) + ' seconds elapsed')
        print('Connected, IP address:', self.wlan_client.ifconfig())
