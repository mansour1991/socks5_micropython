""" Copy rights 2019, Mahmoud Mansour"""

from network import LTE
import time

class Connection:

    def __init__(self):
        self.lte = LTE()

    def nb_connect (self, band=20, apn="nb.inetd.gdsp"):
        counter1 = 0
        counter2 = 0

        if not self.lte.isattached():
            print("Attaching to LTE...")
            self.lte.attach(band=band, apn=apn)
            while not self.lte.isattached():
                counter1 += 1
                print(str(counter1) + ' seconds elapsed')
                if counter1 >= 50 :
                    import machine
                    machine.reset()
                time.sleep(1)

        if not self.lte.isconnected():
            print("Obtaining IP address...")
            self.lte.connect()
            while not self.lte.isconnected():
                counter2 += 1
                print(str(counter2) + ' seconds elapsed')
                time.sleep(0.25)

        print("Network ready ...")

    def nb_disconnect(self):
        if self.lte.isconnected():
            self.lte.disconnect()
        while self.lte.isattached():
            try:
                self.lte.dettach()
            except OSError as e:
                print(e, type(e))
            else:
                print("Network is now disconnected")


    