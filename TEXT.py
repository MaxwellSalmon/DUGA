import pygame

pygame.font.init()

class Text:

    def __init__(self, posx, posy, string, color, font, size):
        self.posx = posx
        self.posy = posy
        self.string = string
        self.color = color
        self.size = size
        self.font = pygame.font.Font(font, self.size)
        self.layout = self.font.render(self.string, True, self.color)
        
    def draw(self, canvas):
        #Draw the text - Call each frame.
        canvas.blit(self.layout,(self.posx, self.posy))

    def update_string(self, string):
        #Update the string that will be shown if needed.
        self.layout = self.font.render(string, True, self.color)
        self.string = string

    def update_pos(self, x, y):
        #Updates the position of the text.
        self.posx = x
        self.posy = y
