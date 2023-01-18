import multiprocessing
import pygame
import os
from enum import Enum 

class State(Enum):
    IDLE = 1
    GEO = 2
    TRIVIA = 3
    NASA = 4

def load_images(path):
    image_list = []
    files = os.listdir(path)
    files.sort()
    for file in files:
        if file.endswith(".png"):
            image = pygame.image.load(os.path.join(path, file))
            image_list.append(image)
    return image_list


def display_Bob(input_queue):
    """Displays the text pressed on the screen"""
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Key Display")
    font = pygame.font.Font(None, 30)
    faces = load_images("./BobDisplay/data/visage_bob")
    state = State.IDLE
    # ['baton.png', 'face_1.png', 'face_2.png', 'face_3.png', 'face_4.png', 
    # 'face_challenge.png', 'face_geography.png', 'face_nasa.png', 'face_trivia.png']
    image_nasa = pygame.image.load("./BobDisplay/data/default_image.png")
    current_face = faces[1] 

    running = True
    while running:
        #screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not input_queue.empty():
            input = input_queue.get().decode()
            print(f"input detected = {input}")
            if input == "nasa" :
                state = State.NASA
                current_face = faces[7]

            elif input == "trivia" :
                state = State.TRIVIA
                current_face = faces[8]

            elif input == "geography" :
                state = State.GEO
                current_face = faces[6]

            else:
                action = input.split(" ")
                if action[0] == "image_nasa" :
                    print("je dois afficher une nouvelle image")
                    try :
                        image_nasa = pygame.image.load(action[1])
                    except :
                        print("ALED")

                else :
                    state = State.IDLE
                    current_face = faces[1]
        



        screen.blit(current_face, (0, 0))

        if state == State.IDLE :
            pass
        
        elif state == State.GEO :
            #text = font.render(input, True, (255, 255, 255))
            pass
        
        elif state == State.TRIVIA :
            pass

        elif state == State.NASA :
            screen.blit(image_nasa, (0, 0))

            pass


        pygame.display.update()
    pygame.quit()
