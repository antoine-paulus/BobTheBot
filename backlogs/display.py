import multiprocessing
import pygame
import os
import BobDisplay.text as text
import actions.API.users as usr
from enum import Enum 
from urllib.request import urlopen
import io
from ivy.ivy import IvyServer

class ActionIvyServer(IvyServer):
    def __init__(self, name):
        IvyServer.__init__(self,'RasaActionAgent')
        self.name = name
        self.start('127.255.255.255:2010')
        self.queue = []
        self.last_message = "loading"

        self.bind_msg(self.handle_geography, '^GEO (.*)/(.*)/(.*)/(.*)/(.*)')
        self.bind_msg(self.handle_trivia, '^TRIVIA (.*)/(.*)/(.*)/(.*)/(.*)')
        self.bind_msg(self.handle_nasa, '^NASA (.*)')
        self.bind_msg(self.handle_response_trivia, '^TRIVIA (.*)')
        self.bind_msg(self.handle_response_geography, '^GEO (.*)')
        self.bind_msg(self.handle_play_again, 'PLAY_AGAIN')
        self.bind_msg(self.handle_stop_game, 'STOP_GAME')
        self.bind_msg(self.handle_repeat_question, 'REPEAT_QUESTION')

    def bind(self):
        pass

    def handle_geography(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent geography" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg


    def handle_trivia(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent trivial" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    def handle_nasa(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent nasa" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    def handle_response_trivia(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent response_trivia" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    def handle_response_geography(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent response_geographie" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    def handle_play_again(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent play_again" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    def handle_stop_game(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent stop_game" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    def handle_repeat_question(self, agent, arg):
        print ("[Agent %s] GOT hello from %r with intent repeat_question" %(self.name, agent))
        self.queue.append(arg)
        self.last_message = arg

    
    def receiver(self, agent, message):
        self.last_message = message
    
    def pop(self) :
        return self.queue
    
    def display(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Bob")
        question_font = pygame.font.SysFont('ubuntu',25, bold=True)
        font = pygame.font.SysFont('ubuntu', 20)

        faces = load_images("./BobDisplay/data/visage_bob")
        current_face = faces[1]
        
        screen.blit(current_face, (0, 0))
        
        text.render(screen,self.last_message)




class State(Enum):
    IDLE = 1
    GEO = 2
    TRIVIA = 3
    NASA = 4
    RESULT_TRIVIA = 5


def load_images(path):
    image_list = []
    files = os.listdir(path)
    files.sort()
    for file in files:
        if file.endswith(".png"):
            image = pygame.image.load(os.path.join(path, file))
            image_list.append(image)
    return image_list

def get_nasa_image(url : str):
    image_url = url
    image_str = urlopen(image_url).read()
    image_file = io.BytesIO(image_str)

    image = pygame.image.load(image_file)
    
    img_size = (600, 500)
    image_finale = pygame.transform.scale(image, img_size)
    return image_finale





if __name__ == "__main__" :
    agent = ActionIvyServer("Bannane")
    agent.display()



