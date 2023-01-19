import os
from ivy.ivy import IvyServer
import threading
import time

class ScratchAgent(IvyServer):
    def __init__(self,name = "Default_Agent",ivyAdress = '127.255.255.255:2010'):
        IvyServer.__init__(self,name)
        self.start(ivyAdress)

        self.bind_msg(self.receiver,'^TOPIC message=(.*)')
    
    def receiver(self, agent, message):
        print(agent)
        print(message)
        self.stop()

agent = ScratchAgent(name="Prog2")


