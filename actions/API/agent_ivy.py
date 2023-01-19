#!/usr/bin/env/python
# Mon agent ivy en python3
"""
from ivy.ivy import IvyServer

class ActionIvyServer(IvyServer):

    def __init__(self, name):
        IvyServer.__init__(self,'RasaActionAgent')
        self.name = name
        self.start('127.255.255.255:2010')

        self.bind_msg(self.handle_geography, '^GEO (.*)/(.*)/(.*)/(.*)/(.*)')
        self.bind_msg(self.handle_trivia, '^TRIVIA (.*)/(.*)/(.*)/(.*)/(.*)')
        self.bind_msg(self.handle_nasa, '^NASA (.*)')
        self.bind_msg(self.handle_response_trivia, '^TRIVIA (.*)')
        self.bind_msg(self.handle_response_geography, '^GEO (.*)')
        self.bind_msg(self.handle_play_again, 'PLAY_AGAIN')
        self.bind_msg(self.handle_stop_game, 'STOP_GAME')
        self.bind_msg(self.handle_repeat_question, 'REPEAT_QUESTION')

    def handle_geography(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent geography" %(self.name, agent))

    def handle_trivia(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent trivial" %(self.name, agent))

    def handle_nasa(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent nasa" %(self.name, agent))

    def handle_response_trivia(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent response_trivia" %(self.name, agent))

    def handle_response_geography(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent response_geographie" %(self.name, agent))

    def handle_play_again(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent play_again" %(self.name, agent))

    def handle_stop_game(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent stop_game" %(self.name, agent))

    def handle_repeat_question(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent repeat_question" %(self.name, agent))




a=ActionIvyServer('HelloBack')
"""