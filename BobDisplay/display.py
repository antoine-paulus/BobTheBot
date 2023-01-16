import multiprocessing
import pygame

def input_process(input_queue):
    """Captures the key events and put it in the queue"""
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Key Input")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                input_queue.put(event.unicode)
    pygame.quit()




def display_Bob(input_queue):
    """Displays the text pressed on the screen"""
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Key Display")
    font = pygame.font.Font(None, 30)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not input_queue.empty():
            key = input_queue.get()
            text = font.render(key, True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(text, (10, 10))
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    input_queue = multiprocessing.Queue()
    input_process = multiprocessing.Process(target=input_process, args=(input_queue,))
    display_process = multiprocessing.Process(target=display_Bob, args=(input_queue,))
    input_process.start()
    display_process.start()