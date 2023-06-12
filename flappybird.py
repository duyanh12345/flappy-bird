import pygame,sys,random

def draw_bg():
    screen.blit(bg,(xbg,0))
    screen.blit(bg,(xbg+432,0))

def draw_floor():
    screen.blit(floor,(xbg,600))
    screen.blit(floor,(xbg+432,600))

def draw_bird():
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*2,1)
    screen.blit(new_bird,bird_rect)

def create_pipe():
    random_down=random.choice(random_downs)
    random_up=random.choice(random_ups)
    bottom_pipe=pipe_surface.get_rect(bottomleft = (432,random_down))
    top_pipe=pipe_surface.get_rect(bottomleft = (432,random_down-450))
    return bottom_pipe,top_pipe

def draw_pipe(pipes):
    for pipe in pipes :
        pipe.centerx-=1

        if pipe.centery >=450 :
           screen.blit(pipe_surface,pipe)
        else :
           flip_surface=pygame.transform.flip(pipe_surface,False,True)
           screen.blit(flip_surface,pipe)

def gameovers():
    if bird_rect.centery >= 768 or bird_rect.centery<=0 :
        hit_sound.play()
        die_sound.play()
        return 2

    for pipe in pipe_list :
        if bird_rect.colliderect(pipe) :
            hit_sound.play()
            die_sound.play()
            return 2

    return 1

pygame.init()
screen= pygame.display.set_mode((432,768))
clock = pygame.time.Clock()

#back_ground
bg=pygame.image.load('assets/background-night.png').convert()
bg=pygame.transform.scale2x(bg)
xbg=0

#floor
floor=pygame.image.load('assets/floor.png').convert()
floor=pygame.transform.scale2x(floor)

#bird
bird1=pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird2=pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird3=pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird1,bird2,bird3]
bird_index= 0
bird = bird_list[bird_index]
time_bird=pygame.USEREVENT
pygame.time.set_timer(time_bird,1)
bird_rect=bird.get_rect(center = (100,384))
bird_movement=0
gravity=0.1

#gameover
game_ative= 0
gameover=pygame.image.load('assets/gameover.png').convert_alpha()
gamover=pygame.transform.scale2x(gameover)

#pipe
pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
random_downs = [600,625,650,675,700]
random_ups = [100,150,200,250]
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe,2000)

#open_screen
open_screen=pygame.image.load('assets/message.png')
open_screen=pygame.transform.scale2x(open_screen)

#sound
flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
die_sound=pygame.mixer.Sound("sound/sfx_die.wav")
hit_sound=pygame.mixer.Sound("sound/sfx_hit.wav")
game_sound=pygame.mixer.Sound("sound/LetsBeFriendsNjsThemeOurBelovedSummerOst-NamHyeSeungKoEunJung-7129700.mp3")
game_sound.play()

#score
game_font=pygame.font.Font(None,40)
score=0
score_surface=game_font.render(f'Score :{int(score)}',True,(250,250,250))
high_score=0
high_score_surface=game_font.render(f'High Score :{int(high_score)}',True,(250,250,250))

#edit
edit=game_font.render(f'Code by Duy Anh',True,(250,250,250))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()
        if event.type == pygame.KEYDOWN:
            if game_ative ==1 and event.key==pygame.K_SPACE :
                bird_movement =-5
                flap_sound.play()
            if game_ative != 1 and event.key==pygame.K_SPACE :
                bird_rect=bird.get_rect(center = (100,384))
                game_ative =1
                bird_movement=-5
                pipe_list =[]
                flap_sound.play()
        if event.type == spawnpipe :
                pipe_list.extend(create_pipe())
        if event.type == time_bird :
                bird_index +=1
                if bird_index == 3 :
                    bird_index =0
    
    bird = bird_list[bird_index]
    bird_movement +=gravity  
    bird_rect.centery +=bird_movement
    
    if game_ative == 0 :
       draw_bg()
       draw_floor()
       screen.blit(open_screen,(70,50))
    elif game_ative ==1 :
       draw_bg()
       draw_bird()
       draw_pipe(pipe_list)
       draw_floor()
       game_ative=gameovers()
       for pipe in pipe_list :
        if bird_rect.centerx==pipe.centerx:
            score+=0.5
       high_score=max(high_score,score)
       score_surface=game_font.render(f'Score :{int(score)}',True,(250,250,250))
       screen.blit(score_surface,(100,200))
       screen.blit(high_score_surface,(100,700))
       high_score_surface=game_font.render(f'High Score :{int(high_score)}',True,(250,250,250))
    else :
       draw_bg()
       draw_floor()
       screen.blit(gameover,(120,300))
       score=0
    
    screen.blit(edit,(10,10))
    pygame.display.update()   
    clock.tick(120)

    xbg-=1
    if xbg <= -432 :
        xbg=0