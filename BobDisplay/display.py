import multiprocessing
import pygame
import os
import BobDisplay.text as text
from enum import Enum 
from urllib.request import urlopen
import io

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

def get_nasa_image(url : str):
    image_url = url
    image_str = urlopen(image_url).read()
    image_file = io.BytesIO(image_str)

    image = pygame.image.load(image_file)
    
    img_size = (600, 500)
    image_finale = pygame.transform.scale(image, img_size)
    return image_finale






def display_Bob(input_queue):
    """Displays the text pressed on the screen"""
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Key Display")
    question_font = pygame.font.SysFont('ubuntu',25, bold=True)
    font = pygame.font.SysFont('ubuntu', 20)
    faces = load_images("./BobDisplay/data/visage_bob")
    state = State.IDLE
    # ['baton.png', 'face_1.png', 'face_2.png', 'face_3.png', 'face_4.png', 
    # 'face_challenge.png', 'face_geography.png', 'face_nasa.png', 'face_trivia.png']
    image_nasa = pygame.image.load("./BobDisplay/data/default_image.png")
    trivia_question = "Loading..."
    trivia_answers = ["Loading...","Loading...","Loading...","Loading..."]
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
                current_face = faces[5]

            elif input == "geography" :
                state = State.GEO
                current_face = faces[6]

            elif input[:3] == "TQ/":
                trivia_question = input.split("/")[1]
            
            elif input[:3] == "TA/":
                trivia_answers = input.split("/")[1:]

            else:
                action = input.split(" ")
                if action[0] == "image_nasa" :
                    try :
                        image_nasa = get_nasa_image(action[1])
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
            question = text.format(trivia_question, question_font, 50, 190, 500, (255,255,255))
            text.render(screen,question)
            answer_1 = text.format(trivia_answers[0], font, 50, question.end_y + 25, 225, (255,255,255))
            answer_2 = text.format(trivia_answers[1], font, 300, question.end_y + 25, 225, (255,255,255))
            y = max(answer_1.end_y,answer_2.end_y) + 10
            answer_3 = text.format(trivia_answers[2], font, 50, y, 250, (255,255,255))
            answer_4 = text.format(trivia_answers[3], font, 300, y, 250, (255,255,255))
            text.render(screen,answer_1)
            text.render(screen,answer_2)
            text.render(screen,answer_3)
            text.render(screen,answer_4)
            pass

        elif state == State.NASA :
            screen.blit(image_nasa, (0, 0))

            pass


        pygame.display.update()
    pygame.quit()
