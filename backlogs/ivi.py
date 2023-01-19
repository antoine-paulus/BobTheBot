import os
from ivy.ivy import IvyServer
import threading
import time

class Agent(IvyServer):
    def __init__(self,name = "Default_Agent",ivyAdress = '127.255.255.255:2010'):
        IvyServer.__init__(self,name)
        self.start(ivyAdress)

    def send_message(self, topic="TOPIC" ,message = "test"):
        self.send_msg(f"{topic} message={message}")


agent = Agent(name="Prog1")
agent.send_message(message="Bonjour")
