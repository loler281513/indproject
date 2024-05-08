import pygame, random
from spaceship import Spaceship
from prop import Obstacle
from prop import grid
from enemy import Enemy
from laser import Laser

class Game:
    def __init__(self,window_width,window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.ship_group = pygame.sprite.GroupSingle()
        self.ship_group.add(Spaceship(self.window_width,self.window_height))

        self.obstacles = self.create_obstacles()

        self.enemy_group = pygame.sprite.Group()
        self.create_enemy()
        self.enemy_direction = 1
        self.enemy_lasers_group = pygame.sprite.Group()

        self.lives = 3
        self.run = True

        self.score = 0
        
        self.level = 1

        self.game_over_height = self.window_height -350

    
    
    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.window_width - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1)* gap + i * obstacle_width
            obstacle = Obstacle(offset_x,self.window_height-300)
            obstacles.append(obstacle)
        return obstacles
    
    def create_enemy(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 64
                y = 100 + row * 64
                
                if row == 0:
                    alien_type = 3
                elif row in(1,2):
                    alien_type = 2
                else:
                    alien_type = 1
                enemy = Enemy(alien_type,x,y) 
                self.enemy_group.add(enemy)

    def move_enemy(self, i):
        self.enemy_group.update(self.enemy_direction)
        enemy_sprites = self.enemy_group.sprites()
        for enemy in enemy_sprites:
            if enemy.rect.right >= self.window_width:
                self.enemy_direction = -i
                self.enemy_move_down(1)
            elif enemy.rect.left <= 0:
                self.enemy_direction = i
                self.enemy_move_down(1)
            if enemy.rect.bottom >= self.game_over_height:
                self.run = False
    


    def enemy_move_down(self,distance):
        if self.enemy_group:
            for enemy in self.enemy_group.sprites():
                enemy.rect.y += distance

    def enemy_direct(self,i):
        self.enemy_direction = i
    
    def enemy_shoot_laser(self):
        if self.enemy_group.sprites():
            random_enemy = random.choice(self.enemy_group.sprites())
            laser_sprite = Laser(random_enemy.rect.center, -6, self.window_height)
            self.enemy_lasers_group.add(laser_sprite)
    
    def check_for_collisions(self):
        #ship
        if self.ship_group.sprite.lasers_group:
            for laser_sprite in self.ship_group.sprite.lasers_group:

                enemy_hit = pygame.sprite.spritecollide(laser_sprite,self.enemy_group, True)
                if enemy_hit:
                    for enemy in enemy_hit:
                        self.score += enemy.type * 100
                        laser_sprite.kill()

                    


                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()
        


        #enemy
        if self.enemy_lasers_group:
            for laser_sprite in self.enemy_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite,self.ship_group,False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

    
    def game_over(self):
        self.run = False
    
    def reset(self):

        self.run = True
        self.lives = 3
        self.ship_group.sprite.reset()
        self.enemy_group.empty()
        self.enemy_lasers_group.empty()
        self.create_enemy()
        self.obstacles = self.create_obstacles()
        self.enemy_direction = 1


    def reset_score(self):
        self.score = 0

        


