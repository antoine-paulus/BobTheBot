import multiprocessing
import pygame
import os
import BobDisplay.text as text
import actions.API.users as usr
from enum import Enum 
from urllib.request import urlopen
import io

class State(Enum):
    IDLE = 1
    GEO = 2
    TRIVIA = 3
    NASA = 4
    RESULT_TRIVIA = 5
    RESULT_GEO = 6

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
    question_font = pygame.font.SysFont('ubuntu',30, bold=True)
    font = pygame.font.SysFont('ubuntu', 20)
    faces = load_images("./BobDisplay/data/visage_bob")
    state = State.IDLE
    # ['baton.png', 'face_1.png', 'face_2.png', 'face_3.png', 'face_4.png', 
    # 'face_challenge.png', 'face_geography.png', 'face_nasa.png', 'face_trivia.png']
    image_nasa = pygame.image.load("./BobDisplay/data/default_image.png")
    trivia_question = "Loading..."
    trivia_answers = ["Loading...","Loading...","Loading...","Loading..."]
    geo_question = "Loading..."
    geo_answers = ["Loading...","Loading...","Loading...","Loading..."]
    geo_flag = False
    user_name = "Unknown_user"
    current_face = faces[1] 
    final_score = "0"
    txt_color = (92,244,228)

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
                current_face = faces[5]
            
            elif input == "scoreboard_trivia" : 
                state = State.RESULT_TRIVIA
                current_face = faces[5]

            elif input == "scoreboard_geo" : 
                state = State.RESULT_GEO
                current_face = faces[6]

            elif input[:3] == "TQ/":
                trivia_question = input.split("/")[1]
            
            elif input[:3] == "TA/":
                trivia_answers = input.split("/")[1:]

            elif input[:3] == "TU/" : 
                user_name = input.split("/")[1]

            elif input[:3] == "GQ/" : # Geo Answers. Format GQ/Which question is that question ? 
                geo_question = input.split("/")[1]

            elif input[:3] == "GA/": # Geo Answers. Format GA/A-Answer A/B-AnswerB...
                geo_answers = input.split("/")[1:]

            elif input[:3] == "GF/" : # Is Flag in geo question. Format ; GF/T or GF/F
                geo_flag = input=="GF/T"

            else:
                action = input.split(" ")
                if action[0] == "image_nasa" :
                    try :
                        image_nasa = get_nasa_image(action[1])
                    except :
                        print("ALED")
                elif action[0] == "score" :
                    final_score = action[1]

                else :
                    state = State.IDLE
                    current_face = faces[1]
        



        screen.blit(current_face, (0, 0))

        if state == State.IDLE :
            pass
        
        elif state == State.GEO :
            # Check if a flag has to be displayed
            if geo_flag :
                image = pygame.image.load("data/current_flag.png")
                img_size = (320, 200)
                image_geo = pygame.transform.scale(image, img_size)
                screen.blit(image_geo, (140, 20))
                y = 220
            else :
                y = 150
            
            # Display Question
            question = text.format(geo_question, question_font, 50, y+40, 500, txt_color)
            text.render(screen,question)

            # Display Answers
            answer_1 = text.format(geo_answers[0], font, 50, question.end_y + 25, 225, txt_color)
            answer_2 = text.format(geo_answers[1], font, 300, question.end_y + 25, 225, txt_color)
            y = max(answer_1.end_y,answer_2.end_y) + 10
            answer_3 = text.format(geo_answers[2], font, 50, y, 250, txt_color)
            answer_4 = text.format(geo_answers[3], font, 300, y, 250,txt_color)
            text.render(screen,answer_1)
            text.render(screen,answer_2)
            text.render(screen,answer_3)
            text.render(screen,answer_4)
            
            pass
        
        elif state == State.TRIVIA :
            # Display Question
            question = text.format(trivia_question, question_font, 50, 190, 500, txt_color)
            text.render(screen,question)

            # Display Answers
            answer_1 = text.format(trivia_answers[0], font, 50, question.end_y + 25, 225, txt_color)
            answer_2 = text.format(trivia_answers[1], font, 300, question.end_y + 25, 225, txt_color)
            y = max(answer_1.end_y,answer_2.end_y) + 10
            answer_3 = text.format(trivia_answers[2], font, 50, y, 250, txt_color)
            answer_4 = text.format(trivia_answers[3], font, 300, y, 250,txt_color)
            text.render(screen,answer_1)
            text.render(screen,answer_2)
            text.render(screen,answer_3)
            text.render(screen,answer_4)
            pass

        elif state == State.RESULT_TRIVIA : 
            text_score = text.format("Your score : " + str(final_score),question_font,50, 190, 500, txt_color)
            text.render(screen,text_score)
            score_board = usr.get_score_board(game=usr.Game.TRIVIA)
            y = text_score.end_y + 50
            for score in score_board : 
                user_text = text.format(score[1],font,50,y,400,txt_color)
                scoreb_text = text.format(str(score[0]),font,450,y,100,txt_color)
                text.render(screen,user_text)
                text.render(screen,scoreb_text)
                y = user_text.end_y + 10
        
        elif state == State.RESULT_GEO : 
            text_score = text.format("Your score : " + str(final_score),question_font,300, 50, 250, txt_color)
            text.render(screen,text_score)
            score_board = usr.get_score_board(game=usr.Game.GEO)
            y = 250
            for score in score_board : 
                user_text = text.format(score[1],font,15,y,125,txt_color)
                scoreb_text = text.format(str(score[0]),font,140,y,100,txt_color)
                text.render(screen,user_text)
                text.render(screen,scoreb_text)
                y = user_text.end_y + 10


        elif state == State.NASA :
            screen.blit(image_nasa, (0, 0))

            pass


        pygame.display.update()
    pygame.quit()
