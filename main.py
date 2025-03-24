# pygame template - skeleton for a new pygame project
from distutils.dep_util import newer
from operator import truediv

import pygame as pygame
import random

WIDTH = 600
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (220,208,255)
ORANGE = (255,165,0)
YELLOW = (255,255,0)


font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y,color):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surf.blit(text_surface,text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()

        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


def newmob():
    i =random.randrange(1,5)
    rock = MOB(i)
    mobs.add(rock)
    all_sprites.add(rock)
# def newmob2():
#     car2 = MOB2()
#     mobs.add(car2)
#     all_sprites.add(car2)
def newmob3():
    signs = MOB3()
    mobs.add(signs)
    all_sprites.add(signs)
# def newmob4():
#     car3 = MOB4()
#     mobs.add(car3)
#     all_sprites.add(car3)
#
# def newmob5():
#     car4 = MOB5()
#     mobs.add(car4)
#     all_sprites.add(car4)

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.width = 100
        self.height = 100
        self.expl_anim={}
        self.expl_anim['sm']=[]
        self.expl_anim['lg'] = []
        self.load_image()
        self.image=self.expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame=0
        self.frame_rate =75
        self.last_update=pygame.time.get_ticks()

    def update(self):
        now=pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def load_image(self):
        for i in range(1,9):
            filename='explosion/regularExplosion0{}.png'.format(i)
            img =pygame.image.load(filename)
            img_lg=pygame.transform.scale(img,(150,150))
            self.expl_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (70, 70))
            self.expl_anim['sm'].append(img_sm)

            # hits = pygame.sprite.spritecollide(player, MOB, True)
            # if hits:
            #     expl = Explosion(player.rect.midtop, "sm")
            #     all_sprites.add(expl)






class MOB(pygame.sprite.Sprite):
    def __init__(self,lane):
        pygame.sprite.Sprite.__init__(self)
        self.width = 90
        self.height = 60
        self.car_list=[]
        self.cop_list=[]
        self.type = random.choice(["cop","car"])
        self.load_images()
        self.lane = lane
        self.cop_car = False
        self.pick_car=random.randrange(1,21)
        self.image = pygame.Surface((self.width, self.height))
        if self.pick_car%4==0:
            # self.pick_image=self.cop_list
            self.cop_car=True
        else:
            self.image = random.choice(self.car_list)

        #self.image = pygame.image.load("cars_img/car 1.png")
        # self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image=pygame.transform.rotate(self.image,270)
        self.rect = self.image.get_rect()

        x1 = WIDTH // 4  - 10
        x2 =  75
        if lane ==2:
            x1=WIDTH//4+50
            x2=WIDTH//2-10
        if lane ==3:
            x1 =WIDTH//2+10
            x2=WIDTH//4*3-10
        if lane==4:
            x1 =WIDTH//4*3+10
            x2=WIDTH-75
        #lanes= random.randrange(x1,x2)
        lanes=(x1+x2)//2
        self.rect.centerx =lanes
        self.rect.y=random.randrange(-1600,-800)
        self.speedy = 5
        self.frame = 0
        self.frame_rate = 75
        self.last_update = pygame.time.get_ticks()
        self.current_frame=0

    def load_images(self):
        for i in range(2,8):
           filename = 'cars_img/car {}.png'.format(i)
           img = pygame.image.load(filename)
           self.car_list.append(img)


        for i in range(1, 3):
            filename = 'cars_img/cop{}.png'.format(i)
            img = pygame.image.load(filename)
            self.cop_list.append(img)
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 80:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.cop_list)
            self.image = self.cop_list[self.current_frame]
            self.image = pygame.transform.flip(self.image,False,True)
    def update(self):
        if self.cop_car == True:
            self.animate()
        if self.rect.top >= HEIGHT:
            ship.car_pass+=1
            self.kill()

        self.rect.y+=self.speedy
class Power(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.width = 50
        self.height = 60
        self.type=random.choice(['health','speed_up'])
        self.image= pygame.image.load ("gas_can.png")
        if self.type== 'speed_up':
            self.image = pygame.image.load("bolt_gold.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.speedy = 10
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()




#MOB


 #PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 65
        self.height = 110
        #self.image = pygame.Surface((self.width,self.height))
        #self.image.fill(GREEN)
        self.image = pygame.image.load("cars_img/car 8.png")
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT
        self.speedx = 10
        self.shoot_delay =250
        self.last_shot =pygame.time.get_ticks()
        self.score =0
        self.car_pass=0
        self.lives = 3
        self.health = 100
        self.level_score = 0
        self.spawn =True
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.start = False
        self.level = 1
    def powerup(self):
        self.power+=1
        self.power_time= pygame.get_ticks()
    def update(self):
        if self.power>=2 and pygame.time.get_ticks()-self.power_time>5000:
            self.power-=1
            for m in mobs:
                m.speedy = 5
            for l in lanes:
                l.speedy = 3
            self.power_time=pygame.time.get_ticks()
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_UP]:
            for l in lanes:
                l.speedy = 3
                self.start = True

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right>=WIDTH-60:
            self.health-=0.5
        if self.rect.left<=60:
            self.health-=0.5
        self.rect.x += self.speedx




        if self.rect.centerx <=300  :
            self.health -= .1
        if self.rect.centerx >= 310:
            self.health -= .1

        #if self.rect.left <= 125:
        #    self.health -= 0.3
        #self.rect.x += self.speedx
# class Mark(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.width = 100
#         self.height = 3
#         # self.meteor_list=[]
#         # self.load_images()
#         self.image = pygame.Surface((self.width, self.height))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.x = WIDTH // 4 + 30
#         self.rect.top = 130
class Lane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 10
        self.height = 30
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//4+30
        #self.rect.bottom=40
        self.rect.centery=-200

        self.speedy = 0
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.centery = -150
            ship.score+=1
            ship.level_score+=1

class Lane2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 10
        self.height = 30
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 4 * 3 - 30
        #self.rect.bottom=40
        self.rect.centery=-200
        self.speedy = 0
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.centery = -150


class MOB3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 90
        self.height = 60
        self.sign_list=[]
        self.load_images()
       # self.image = pygame.Surface((self.width,self.height))
        #self.image.fill(RED)
        self.pick =  random.choice(self.sign_list)
        self.image = self.pick
        #self.image = pygame.image.load("cars_img/car 1.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 270)
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image=pygame.transform.rotate(self.image,90)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,30)
        self.rect.centery= random.randrange(-200,-100)
        self.rect.bottom = -100
        self.speedx = 0
        self.speedy = 5

    def load_images(self):
        for i in range(1,4):
           filename = 'Signs/sign {}.png'.format(i)
           img = pygame.image.load(filename)
           self.sign_list.append(img)
    def update(self):
        if self.rect.top >= HEIGHT:
            self.rect.x = random.randrange(0,30)
            self.rect.centery = random.randrange(-200, -100)

        self.rect.y+=self.speedy




def start_screen():
    screen.blit(background_img, background_rect)
    draw_text(screen, "Near Miss", 64, WIDTH // 2, HEIGHT//4, BLACK)
    draw_text(screen, "Use arrow keys to move", 32, WIDTH//2 , 2, BLACK)
    draw_text(screen, "Press A to begin", 32, WIDTH // 2, 3*HEIGHT//4 , BLACK)
    draw_text(screen, "Press up arrow to begin moving", 32, WIDTH // 2, 2 * HEIGHT // 4, BLACK)
    pygame.display.flip()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate= pygame.key.get_pressed()
            if event.type==pygame.QUIT:
                #running=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting=False


def level_screen():
    screen.blit(background_img, background_rect)
    draw_text(screen, "Level "+str(ship.level)+" Complete!", 64, WIDTH // 2, HEIGHT // 4, BLACK)
    draw_text(screen, "Press A to continue", 32, WIDTH // 2, 3 * HEIGHT // 4, BLACK)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                # running=False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False
# initialize pygame and create window
pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()

lanes = pygame.sprite.Group()
lane = Lane()
l = Lane()
new_level=False
lane2=Lane2()
l2=Lane2()
ship = Player()
all_sprites.add(ship)
for i in range((HEIGHT+180)//90):
    l = Lane()
    all_sprites.add(l)
    lanes.add(l)
    l.rect.bottom = HEIGHT-i*90
    l2 = Lane2()
    lanes.add(l2)
    all_sprites.add(l2)
    l2.rect.bottom = HEIGHT  - i * 90
    # l.image.fill(RED)

#for i in range(8):
   # newmob()

#for i in range(3):
   # newmob3()
rock1=MOB(1)
mobs.add(rock1)
all_sprites.add(rock1)
rock2=MOB(2)
mobs.add(rock2)
all_sprites.add(rock2)
rock3=MOB(3)
mobs.add(rock3)
all_sprites.add(rock3)
rock4=MOB(4)
mobs.add(rock4)
all_sprites.add(rock4)
rock1.rect.y=-100
rock2.rect.y=-250
rock3.rect.y=-400
rock4.rect.y=-550

background_img = pygame.image.load ("road.png")
background_img = pygame.transform.scale(background_img,(WIDTH,HEIGHT))
background_rect = background_img.get_rect()

player_mini_img = pygame.image.load('cars_img/car 3.png')
player_mini_img = pygame.transform.scale(player_mini_img, (30, 20))
player_mini_img = pygame.transform.rotate(player_mini_img, 90)
# Game loop
last_shot=pygame.time.get_ticks()
shoot_delay=1500
running = True
new_game=True
delay_spawn=pygame.time.get_ticks()
last_spawn=pygame.time.get_ticks()
delay =2000
running=True
new_game=True
while running:
    if new_game:
        start_screen()
        new_game=False
        player=Player()
        all_sprites.add(player)

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    if new_level:
        level_screen()
        ship.level+=1
        new_level = False

    # if ship.score==30:
    #     new_level=True
    if ship.level_score == 30:
        new_level = True
        ship.level_score = 0



        # all_sprites.add(line)
    # now = pygame.time.get_ticks()
    # if now - delay_spawn > 1500:
    #     lane = Lane()
    #     all_sprites.add(lane)
    #     lanes.add(lane)
    #     lane2 = Lane2()
    #     all_sprites.add(lane2)
    #     delay = random.randrange(1500, 3500)
    #     delay_spawn = now
    now = pygame.time.get_ticks()
    if now - delay_spawn > delay:
        newmob()
        delay=random.randrange(1500,3500)
        delay_spawn=now
    if ship.car_pass ==1:
        pow = Power(random.randrange(100,375))
        all_sprites.add(pow)
        powers.add(pow)
        ship.car_pass=0

        #ADD score to player
        # ship.score += 10
    hit_power=pygame.sprite.spritecollide(ship,powers,True)
    for hit in hit_power:
        if hit.type=='health':
            ship.power += 1
            ship.health+= random.randrange(10,30)
            if ship.health>=100:
                ship.health =100

        if hit.type=='speed_up':
            ship.power += 1
            for m in mobs:
                m.speedy*=2
            for l in lanes:
                l.speedy*=2
    hit_player = pygame.sprite.spritecollide(ship,mobs,True)
    for hit in hit_player:

        #Damage to player(ship)
        ship.health-= 25
        newmob()
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
    if ship.health <=0:
        ship.health =100
        ship.lives -= 1
    if ship.lives <=0:
        running = False

    # Update
    all_sprites.update()
    # Draw / render
    screen.fill(VIOLET)
    screen.blit(background_img,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(ship.score),32,WIDTH//2,10,BLACK)
    draw_text(screen, "Lives:",32, 3*WIDTH // 4, 10, BLACK)
    draw_text(screen, "Gas:",32, WIDTH // 6-36, 5, BLACK)

    draw_shield_bar(screen, WIDTH // 6 , 20, ship.health)
    draw_lives(screen, WIDTH - 100, 13, ship.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()