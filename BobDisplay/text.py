import pygame

class TextObject :
    def __init__(self,rendered,start_x,start_y,end_x,end_y):
        self.data = rendered[:]
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.height = end_y - start_y
        self.width = end_x - start_x
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height


def format(text : str, font : pygame.font.Font, start_x : int, start_y : int, max_width : int,color) :
    #Handle Line Breaks
    paragraphs = text.split("\n")
    current_x = start_x
    current_y = start_y
    max_x = start_x + max_width
    rendered = []
    for paragraph in paragraphs :

        words = paragraph.split()

        for word in words :
            word_obj = font.render(word+" ", True, color)
            if word_obj.get_width()+current_x > max_x :
                current_y += font.get_linesize() if current_x != start_x else 0
                current_x = start_x
            rendered.append([word_obj,(current_x,current_y)])
            current_x += word_obj.get_width()

        current_y += font.get_linesize()
        current_x = start_x
    return TextObject (rendered,start_x,start_y,max_x,current_y)

def render(screen : pygame.display, rendered : TextObject) : 
    for elem in rendered.data :
        screen.blit(elem[0],elem[1])