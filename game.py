import pygame, random
from spaceship import Spaceship
from prop import Obstacle
from prop import grid
from enemy import Enemy
from laser import Laser
from boss import Boss

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

        self.hp = 200
        self.max_hp = 200
        self.red = (255,0,0)
        self.green = (0,255,0)

        self.invulnerable_time = 0

        self.boss_direction_x = 2
        self.boss_direction_y = 8
        self.boss = Boss(self.window_width,self.window_height)
        self.boss_group = pygame.sprite.Group()
        self.random_num = self.get_random_number(1, 100)
        self.randomning = True
        self.rand = True
        self.rand_num = self.get_random_number(1, 2)

        self.boss_laser_group = pygame.sprite.Group()

    
    def get_random_number(self,a, b):
        return random.randint(a, b)
    
    def add_boss(self):
        self.boss_group.add(self.boss)
    
    def delete_boss(self):
        self.boss_group.empty()

    def move_boss(self):
        if self.randomning:
            self.random_num = self.get_random_number(1, 100)
            print(self.random_num)
            self.randomning = False
        
        if  60 <= self.random_num <= 100:
            self.boss.update_x(self.boss_direction_x)
            if self.boss.rect.right >= self.window_width:
                self.boss_direction_x = -4
                self.boss.update_x(self.boss_direction_x)

            elif self.boss.rect.left <= 0:
                self.boss_direction_x = 4
                self.boss.update_x(self.boss_direction_x)
                self.randomning = True

        if 31 <= self.random_num <= 59:
            if self.boss.rect.centerx < self.window_width / 2:  
                self.boss.update_x(self.boss_direction_x)
                self.boss_direction_x = 1 

            elif self.boss.rect.centerx > self.window_width / 2:  
                self.boss.update_x(self.boss_direction_x)
                self.boss_direction_x = -1
            
            else:
                self.boss_direction_x = 0
                
                if self.boss_direction_y == 0:
                    self.boss_direction_y = 8

                if self.boss_direction_y == 8:  # движение вниз
                    self.boss.update_y(self.boss_direction_y)
                    if self.boss.rect.bottom >= self.window_height:
                        self.boss_direction_y = -8
                        
                if self.boss_direction_y == -8:  # движение вверх
                    self.boss.update_y(self.boss_direction_y)
                    if self.boss.rect.top <= 80:
                        self.boss_direction_y = 0
                        self.randomning = True
                        if self.rand:
                            self.rand_num = self.get_random_number(1, 2)
                            print(self.rand_num,"сторона")
                            self.rand = False
                        if self.rand_num == 1:
                            self.boss_direction_x = 4
                            self.boss_direction_y = 8

                        if self.rand_num == 2:
                            self.boss_direction_x = -4
                            self.boss_direction_y = 8

        if 1 <= self.random_num <= 30:
            if self.boss_direction_x == 4:  # движение вправо
                self.boss.update_x(self.boss_direction_x)
                if self.boss.rect.right >= self.window_width:
                    self.boss_direction_x = 0
                    self.boss_direction_y = 8
                
            elif self.boss_direction_y == 8:  # движение вниз
                self.boss.update_y(self.boss_direction_y)
                if self.boss.rect.bottom >= self.window_height:
                    self.boss_direction_y = -8
                    
            

                
            elif self.boss_direction_y == -8:  # движение вверх
                self.boss.update_y(self.boss_direction_y)
                if self.boss.rect.top <= 80:
                    self.boss_direction_y = 0
                    self.boss_direction_x = -4
                if self.boss.rect.top <= 80 and self.boss.rect.left <= 0:
                    self.boss_direction_y = 0
                    self.boss_direction_x = 4
                    self.randomning = True


            elif self.boss_direction_x == -4:  # движение влево
                self.boss.update_x(self.boss_direction_x)
                if self.boss.rect.left < 0:
                    self.boss_direction_x = 0
                    self.boss_direction_y = 8
    
    def boss_shoot_laser(self):
        if self.boss_group.sprites():
            laser_sprites = Laser((self.boss.rect.centerx,self.boss.rect.centery + 100), -6, self.window_height)
            self.boss_laser_group.add(laser_sprites)

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
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1

        #ship
        if self.ship_group.sprite.lasers_group:
            for laser_sprite in self.ship_group.sprite.lasers_group:

                enemy_hit = pygame.sprite.spritecollide(laser_sprite,self.enemy_group, True)
                if enemy_hit:
                    for enemy in enemy_hit:
                        self.score += enemy.type * 100
                        laser_sprite.kill()

                boss_hit =  pygame.sprite.spritecollide(laser_sprite,self.boss_group, True)
                if boss_hit:
                    self.hp -= 2
                    laser_sprite.kill()
                    if self.hp == 0:
                        self.delete_boss()


                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()
        


        #enemy
        if self.enemy_lasers_group:
            for laser_sprite in self.enemy_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite,self.ship_group,False):
                    laser_sprite.kill()
                    if self.invulnerable_time == 0:
                        self.lives -= 1
                        self.invulnerable_time = 180  
                        if self.lives == 0:
                            self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        #boss
        if self.boss_laser_group:

            for laser_sprite in self.boss_laser_group:
                laser_hits_boss = pygame.sprite.spritecollide(laser_sprite,self.ship_group,False)
                if laser_hits_boss:
                    laser_sprite.kill()
                    if self.invulnerable_time == 0:  
                        self.lives -= 1
                        self.invulnerable_time = 180  
                        if self.lives == 0:
                            self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        

        hits = pygame.sprite.spritecollide(self.boss, self.ship_group, False)
        if hits:  
            if self.invulnerable_time == 0:
                self.lives -= 1
                self.invulnerable_time = 180  
                if self.lives == 0:
                    self.game_over()
        for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(self.boss, obstacle.blocks_group, True):
                        pass

    
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

        self.reset_boss()
    

    def reset_boss(self):
        self.boss.reset_image()
        self.hp = 200
        self.invulnerable_time = 0
        self.boss_direction_x = 4
        self.boss_direction_y = 8
        self.random_num = self.get_random_number(1, 100)
        self.randomning = True
        self.rand = True
        self.rand_num = self.get_random_number(1, 2)
        self.boss_group.empty()
        self.boss_laser_group.empty()

    def heal_bar(self,window):
        pygame.draw.rect(window, self.red, ((self.window_width/2-((self.max_hp*3)/2)), 70, (self.max_hp*3), 20))
        pygame.draw.rect(window, self.green, ((self.window_width/2-((self.max_hp*3)/2)), 70, (self.hp*3), 20))



    def reset_score(self):
        self.score = 0

        


