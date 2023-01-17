import multiprocessing
import pygame
import os

def input_process(input_queue):
    """Captures the key events and put it in the queue"""
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Key Input")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                input_queue.put(event.unicode)
    pygame.quit()


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
    
    # ['baton.png', 'face_1.png', 'face_2.png', 'face_3.png', 'face_4.png', 
    # 'face_challenge.png', 'face_geography.png', 'face_nasa.png', 'face_trivia.png']
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
                current_face = faces[7]
            elif input == "trivia" :
                current_face = faces[8]
            elif input == "geography" :
                current_face = faces[6]
            else:
                current_face = faces[1]

            
            #text = font.render(input, True, (255, 255, 255))

            
        screen.blit(current_face, (0, 0))

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    input_queue = multiprocessing.Queue()
    input_process = multiprocessing.Process(target=input_process, args=(input_queue,))
    display_process = multiprocessing.Process(target=display_Bob, args=(input_queue,))
    input_process.start()
    display_process.start()