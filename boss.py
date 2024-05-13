import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load("boss/boss.png")
        self.rect = self.image.get_rect(midtop=(self.width/3, 80))
        self.hp = 100
    
    def update_x(self,direction):
        self.rect.x += direction

    def update_y(self,direction):
        self.rect.y += direction
    
    def reset_image(self):
        self.rect = self.image.get_rect(midtop=(self.width/3, 80))
        