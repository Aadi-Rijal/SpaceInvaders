import pygame
import random
import pandas as pd

pygame.init()

word=pd.read_csv("assets/files/words.csv")
wordlist=word['Word']

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders!')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

score = 0

background=pygame.image.load("assets/images/background.jpg")
alien1_image=pygame.image.load("assets/images/alien1.png")
alien2_image=pygame.image.load("assets/images/alien2.png")
alien3_image=pygame.image.load("assets/images/alien3.png")
alien4_image=pygame.image.load("assets/images/alien4.png")
alien5_image=pygame.image.load("assets/images/alien5.png")
alien6_image=pygame.image.load("assets/images/alien6.png")
ship_image=pygame.image.load("assets/images/spaceship.png")
# boss_image=pygame.image.load("assets/images/boss.png")
bullet_image=pygame.image.load("assets/images/bullet.png")
finish_image=pygame.image.load("assets/images/earth.jpg")
alienwidth,alienheight=alien1_image.get_size()
alienwidth=int(alienwidth/4)
alienheight=int(alienheight/4)
# print(shipwidth,shipheight)
alien1=pygame.transform.scale(alien1_image,(alienwidth, alienheight)).convert_alpha()
alien2=pygame.transform.scale(alien2_image,(alienwidth,alienheight)).convert_alpha()
alien3=pygame.transform.scale(alien3_image,(alienwidth,alienheight)).convert_alpha()
alien4=pygame.transform.scale(alien4_image,(alienwidth,alienheight)).convert_alpha()
alien5=pygame.transform.scale(alien5_image,(alienwidth,alienheight)).convert_alpha()
alien6=pygame.transform.scale(alien6_image,(alienwidth,alienheight)).convert_alpha()
# boss=pygame.transform.scale(boss_image,(alienwidth*2,alienheight*2)).convert_alpha()
ship=pygame.transform.scale(ship_image,(200,100)).convert_alpha()
bullet=pygame.transform.scale(bullet_image,(20,20)).convert_alpha()
finishline=pygame.transform.scale(finish_image,(800,150)).convert_alpha()
alien_list=[alien1,alien2,alien3, alien4, alien5,alien6]
header_font = pygame.font.Font('assets/fonts/Jersey25.ttf', 70)
pause_font = pygame.font.Font('assets/fonts/1up.ttf', 40)
countdown_font = pygame.font.Font('assets/fonts/1up.ttf', 100)
banner_font = pygame.font.Font('assets/fonts/Jersey25.ttf', 45)
font = pygame.font.Font('assets/fonts/Montserrat.ttf', 20)
# music and sounds
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music_background.wav')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

click = pygame.mixer.Sound('assets/sounds/shoot.wav')
woosh = pygame.mixer.Sound('assets/sounds/explosion.wav')
wrong = pygame.mixer.Sound('assets/sounds/Instrument Strum.mp3')
click.set_volume(0.2)
woosh.set_volume(0.4)
wrong.set_volume(0.3)

# game variables
is_countdown= True
level = 1
lives = 5
word_objects = []
file = open('assets/files/high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()
pz = True
new_level = True
submit = ''
active_string = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ship_x=300
ship_y=630
drawship_x=ship_x
bullet_objects=[]
selected_word=None

class Alien:
    def __init__(self, text, speed, x_pos, y_pos, alien):
        self.text = text
        self.speed = speed
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.alien= alien

    def draw(self):
        screen.blit(self.alien,(self.x_pos,self.y_pos))
        color = 'white'
        screen.blit(font.render(self.text, True, color), (self.x_pos+32, self.y_pos+5))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'green'), (self.x_pos+32, self.y_pos + 5))
        pause_butt=draw_screen()

    def update(self):
        self.y_pos +=self.speed


class Bullet:
    def __init__(self, x, y,removepoint):
        self.x_pos=x
        self.y_pos=y
        self.remove=removepoint
        self.speed=40
    def draw(self):
        screen.blit(bullet,(self.x_pos,self.y_pos))
    def update(self):
        self.y_pos-= self.speed

class Ship:
    def __init__(self,x):
        self.x=x
        self.y=ship_y
    def draw(self):
        screen.blit(ship,(self.x,self.y))

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, 'black', (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (7, 70, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (70, 7, 35), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


def draw_screen():
    # screen outlines for main game window and 'header' section
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, (32, 42, 68), [0, 0, WIDTH, 50], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (0,50), (WIDTH, 50), 2)
    pygame.draw.line(screen, 'white', (190, 0), (190, 50), 2)
    pygame.draw.line(screen, 'white', (500, 0), (500, 50), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    # text for showing current level, player's current string, high score and pause options
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT - 90))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 90))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    # draw lives, score, and high score on top of screen
    screen.blit(banner_font.render(f'Score: {score}', True, 'white'), (220, 3))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'white'),(530, 3))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'white'), (30, 3))
    return pause_btn.clicked


def draw_pause():
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255,255,255, 50), [100, 70, 600, 270], 0, 5)
    pygame.draw.rect(surface, (255, 255, 255, 200), [100, 70, 600, 270], 5, 5)
    resume_btn = Button(160, 278, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(495, 278, 'X', False, surface)
    quit_btn.draw()
    surface.blit(header_font.render('MENU', True, 'white'), (325, 95))
    surface.blit(header_font.render('PLAY!', True, 'white'), (200, 240))
    surface.blit(header_font.render('QUIT!', True, 'white'), (535, 240))
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, quit_btn.clicked

def game_level():
    word_objs = []
    lane_positions=[80, 250, 420, 590]
    for i in range(random.randint(1,4)):
        x_pos = random.choice(lane_positions)
        lane_positions.remove(x_pos)
        y_pos = random.randint(-100, -50)
        text_added=False
        while not text_added:
            text_added=True
            text= random.choice(wordlist)
            if len(word_objs)!=0:
                for word in word_objs:
                    if word.text.startswith(text[0]):
                        text_added=False
                        break      
        new_word = Alien(text.lower(),0.1 * level, x_pos, y_pos,random.choice(alien_list))
        word_objs.append(new_word)  
    return word_objs

def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
            scor += int(points)
            word_objects.remove(wrd)
            woosh.play()
    return scor


def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('assets/files/high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

#gameloop
run = True
while run:
    screen.blit(background,(0,0))
    timer.tick(fps)
    # draw static background
    pause_butt = draw_screen()
    the_ship=Ship(drawship_x)
    if pz:
        resume_butt,quit_butt = draw_pause()
        if resume_butt:     
            if(lives<=0):
                lives=5
                level=1
                score=0
            pz = False
            is_countdown=True
        if quit_butt:
            check_high_score()
            run = False
    if not pz and is_countdown:
        for _ in range(3,0,-1):
            screen.blit(background,(0,0))
            pause_butt = draw_screen()
            screen.blit(countdown_font.render(str(_), True, 'white'), (360, 290))
            screen.blit(finishline,(0,HEIGHT-250))
            the_ship.draw()
            draw_screen()
            pygame.display.flip()
            pygame.time.delay(1000)
        is_countdown = False   
    if new_level and not pz:
        word_objects = game_level()
        #pygame.time.delay(500)
        new_level = False
    else:

        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
            if w.y_pos > HEIGHT-275:
                word_objects.remove(w)
                lives -= 1

        screen.blit(finishline,(0,HEIGHT-250))

        the_ship.draw()

        for b in bullet_objects:
            b.draw()
            if not pz:
                b.update()
            if b.y_pos<b.remove+50:
                bullet_objects.remove(b)

    if len(word_objects) <= 0 and not pz:
        level += 1
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()

    if active_string=='':
        drawship_x=ship_x
        targetword_found=False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False

        if event.type == pygame.KEYDOWN:
            if not pz:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                    #click.play()

                    if active_string=='':
                        drawship_x=ship_x
                    else:
                        for w in word_objects:
                            if w.text.startswith(active_string):
                                drawship_x=w.x_pos - 41
                                the_ship.x= drawship_x
                                removepoint=(w.y_pos*40 + w.speed*ship_y)/(w.speed+ 40)
                                new_bullet= Bullet(the_ship.x + 92.5, the_ship.y, removepoint)
                                bullet_objects.append(new_bullet)
                                click.play()
                                break
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if pz:
                    pz = False
                else:
                    pz = True

    if pause_butt:
        pz = True

    if lives < 0:
        pz = True
        lives = 0
        word_objects = []
        new_level = True
        check_high_score()
    pause_butt=draw_screen()
    if pz:
        draw_pause()
    pygame.display.flip()
pygame.quit()