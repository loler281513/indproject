import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load("ship/idle.png")
        self.rect = self.image.get_rect(midbottom = (self.width/2,self.height))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        self.laser_offset = 25

        self.shoot_animation = []
        for i in range(4):
            self.shoot_animation.append(pygame.image.load(f"ship/shoot/{i}.png"))

        self.go_up_animation = []
        for i in range(5):
            self.go_up_animation.append(pygame.image.load(f"ship/up/{i}.png"))
            
        self.current_slide = 0
        self.go_up = False
        self.shooting = False

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.go_right = True

        if keys[pygame.K_LEFT]: 
            self.rect.x -= self.speed
            self.go_left = True

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.go_up = True

        if keys[pygame.K_DOWN]: 
            self.rect.y += self.speed
            

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.shooting = True
            self.laser_ready = False
            self.current_slide = 0
            laser = Laser((self.rect.centerx,self.rect.centery - self.laser_offset), 9, self.height )
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()


    def update (self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()
        
        if self.shooting:
            if self.current_slide < len(self.shoot_animation):
                self.image = self.shoot_animation[self.current_slide]
                self.current_slide += 1
            else:
                self.shooting = False

        elif self.go_up and self.current_slide < len(self.go_up_animation):
            self.image = self.go_up_animation[self.current_slide]
            self.current_slide += 1
        elif self.go_up:
            self.current_slide = 0
            self.go_up = False

        if not self.shooting and not self.go_up:
            self.image = pygame.image.load("ship/idle.png")  # Возврат к основному спрайту после завершения анимации


    def constrain_movement(self):
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
        if self.rect.top < self.height-290:
            self.rect.top = self.height-290

    
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True
    
    def reset(self):
        self.rect = self.image.get_rect(midbottom = (self.width/2,self.height))
        self.lasers_group.empty()
