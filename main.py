import pygame, sys
from button import imageButton
from game import Game
from spaceship import Spaceship

pygame.init()


speed_enemy = 1
level = 1

width = 1024
height = 1024
fps = 60

grey = (29, 29, 27)

paused = pygame.image.load("txt/paused.png")
paused = pygame.transform.scale(paused,(586,121))
game_over = pygame.image.load("txt/go.png")
level_up = pygame.image.load("txt/level.png")
live = pygame.image.load("txt/live.png")
live = pygame.transform.scale(live,(42,36))

back_s = pygame.mixer.Sound("button/sound/back.mp3")

window = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Space v0.1")
main_background = pygame.image.load("background/background.jpg")
clock = pygame.time.Clock()
 
game = Game(width,height)

font = pygame.font.Font(None,60)
score_text = font.render("Score:",False,(255,255,255))
level_text = font.render("Level:",False,(255,255,255))

BUTTON_CLICK_EVENT = pygame.USEREVENT + 1

shoot_laser = pygame.USEREVENT
pygame.time.set_timer(shoot_laser,500)


def main_menu():
    global speed_enemy

    play_button = imageButton(width/3+(width/20),900,252,74,"","button/play/play01.png","button/play/play03.png","button/sound/sound.mp3")
    option_button = imageButton(width/12,900,252,74,"","button/option/option01.png","button/option/option03.png","button/sound/sound.mp3")
    home_button = imageButton(width/2+(width/6),900,252,74,"","button/home/home01.png","button/home/home03.png","button/sound/sound.mp3")


    running =  True
    while running:
        window.fill((0,0,0))
        window.blit(main_background,(-100,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == BUTTON_CLICK_EVENT and event.button == play_button:
                fade()
                new_game()

            if event.type == BUTTON_CLICK_EVENT and event.button == option_button:
                fade()
                settings_menu()
            
            if event.type == BUTTON_CLICK_EVENT and event.button == home_button:
                running = False
                pygame.quit()
                sys.exit()   

            for btn in [play_button,option_button,home_button]:
                btn.handle_event(event)

        for btn in [play_button,option_button,home_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(window)

        pygame.display.flip()          
                
def settings_menu():
    sound_button = imageButton(width/2-(252/2),150,252,74,"","button/sound/sound01.png","button/sound/sound03.png","button/sound/sound.mp3")
    music_button = imageButton(width/2-(252/2),250,252,74,"","button/music/music01.png","button/music/music03.png","button/sound/sound.mp3")
    star_button = imageButton(width/2-(252/2),350,252,74,"","button/star/star01.png","button/star/star03.png","button/sound/sound.mp3")
    back_button = imageButton(width/2-(252/2),450,252,74,"","button/back/back01.png","button/back/back03.png","button/sound/sound.mp3")

    running =  True
    while running:
        window.fill((0,0,0))
        window.blit(main_background,(-100,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    back_s.play()
                    fade()
            
            if event.type == BUTTON_CLICK_EVENT and event.button == back_button:
                running = False
                back_s.play()
                fade()

            for btn in [sound_button,music_button,star_button,back_button]:
                btn.handle_event(event)

        for btn in [sound_button,music_button,star_button,back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(window)

        pygame.display.flip()

def new_game():
    global speed_enemy

    running = True
    while running:
        window.fill(grey)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == shoot_laser and game.run:
                game.enemy_shoot_laser()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    upp()

                    surf = pygame.Surface((width, height))
                    surf.fill((0, 0, 0))
                    surf.set_alpha(200)
                    window.blit(surf, (0, 0))
                    window.blit(paused,(width/4-40,height/4+100))
                    pause()
        if game.run:
            upp()
        else:
            upp()
            surf = pygame.Surface((width, height))
            surf.fill((0, 0, 0))
            surf.set_alpha(200)
            window.blit(surf, (0, 0))
            window.blit(game_over,(width/4-40,height/4+100))
            game_reset()

        if not game.enemy_group:
            upp()
            surf = pygame.Surface((width, height))
            surf.fill((0, 0, 0))
            surf.set_alpha(200)
            window.blit(surf, (0, 0))
            window.blit(level_up,(width/4+10,height/8))
            next_level()

        clock.tick(fps)
        pygame.display.flip()

def pause():
    global speed_enemy
    global level
    running = True
    back_button = imageButton(width/2-(252/2),700,252,74,"","button/back/back01.png","button/back/back03.png","button/sound/sound.mp3")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    new_game()

            if event.type == BUTTON_CLICK_EVENT and event.button == back_button:
                back_s.play()
                speed_enemy = 1
                fade()
                game.reset()
                game.reset_score()
                level = 1
                main_menu()

            for btn in [back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(window)

        pygame.display.flip()

def game_reset():
    global speed_enemy
    global level
    running = True
    restart_button = imageButton(width/2-(252/2),600,252,74,"","button/restart/restart01.png","button/restart/restart03.png","button/sound/sound.mp3")
    back_button = imageButton(width/2-(252/2),700,252,74,"","button/back/back01.png","button/back/back03.png","button/sound/sound.mp3")


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    back_s.play()
                    speed_enemy = 1
                    game.reset()    
                    game.reset_score()
                    level = 1
                    fade()                
                    new_game()
            
            if event.type == BUTTON_CLICK_EVENT and event.button == restart_button:
                back_s.play()
                speed_enemy = 1
                game.reset()
                game.reset_score()
                level = 1
                fade()
                new_game()


            if event.type == BUTTON_CLICK_EVENT and event.button == back_button:
                back_s.play()
                speed_enemy = 1
                game.reset()
                game.reset_score()
                level = 1
                fade()
                main_menu()



            for btn in [restart_button,back_button]:
                btn.handle_event(event)

        for btn in [restart_button,back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(window)

        pygame.display.flip()



def next_level():
    global speed_enemy
    global level
    running = True
    next_button = imageButton(width/2-(252/2),600,252,74,"","button/next/next01.png","button/next/next03.png","button/sound/sound.mp3")
    back_button = imageButton(width/2-(252/2),700,252,74,"","button/back/back01.png","button/back/back03.png","button/sound/sound.mp3")


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == BUTTON_CLICK_EVENT and event.button == next_button:
                speed_enemy += 1
                level += 1
                back_s.play()
                game.reset()
                fade()
                game.enemy_direct(speed_enemy)
                new_game()


            if event.type == BUTTON_CLICK_EVENT and event.button == back_button:
                back_s.play()
                game.reset()
                game.reset_score()
                level = 1
                fade()
                main_menu()



            for btn in [next_button,back_button]:
                btn.handle_event(event)

        for btn in [next_button,back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(window)

        pygame.display.flip()
#затемнение
def fade():
    running = True
    fade_aplha = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        fade_surface = pygame.Surface((width, height))
        fade_surface.fill((0,0,0))
        fade_surface.set_alpha(fade_aplha)
        window.blit(fade_surface,(0,0))

        fade_aplha += 5
        if fade_aplha >= 105:
            fade_aplha = 255
            running = False
        
        clock.tick(fps)

        pygame.display.flip()


def upp():
    x = 0
    for life in range(game.lives):
        window.blit(live,(x,0))
        x += 50

    window.blit(score_text,(width/2+(width/4),15,50,50))
    score_score = font.render(str(game.score),False,(255,255,255))
    window.blit(score_score,(width/2+(width/3+50),15,50,50))

    window.blit(level_text,(width/4+(width/8),15))
    level_number = font.render(str(level),False,(255,255,255))
    window.blit(level_number,(width/4+(width/4),15))

    game.ship_group.update()
    game.ship_group.draw(window)
    game.ship_group.sprite.lasers_group.draw(window)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(window)
    game.enemy_group.draw(window)
    game.move_enemy(speed_enemy)
    game.enemy_lasers_group.update()
    game.enemy_lasers_group.draw(window)
    game.check_for_collisions()

if __name__ == "__main__":
    main_menu()