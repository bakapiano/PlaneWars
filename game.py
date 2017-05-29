# -*- coding:utf-8 -*-

score = 0

import pygame, random, time, os
from sys import exit

class bullet(object):

    def __init__(self):
        self.set()

    def set(self):
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]
        self.fired = False

    def move(self):
        if self.fired == True and self.y > 0:
            self.y = self.y - 0.5
        else:
            self.set()

    def hit(self):
        for e in enemy:
            if self.fired == True and self.x < e.x + 20 and self.x > e.x - 20 and self.y < e.y + 20 and self.y > e.y - 20:
                global score
                score += 1
                screen.blit(im_crash,(self.x-(im_crash.get_width()/2),self.y-(im_crash.get_height()/2)))
                for c in crashdown:
                    if c.flag == False:
                        c.create(self.x,self.y)
                        break
                self.set()
                e.set()
                
class enemy(object):

    def __init__(self):
        self.set()

    def set(self):
        self.speed = random.uniform(0.1,0.8)
        self.x = random.randint(0,500)
        self.y = 0
        
    def move(self):
        if self.y < 700:
            self.y = self.y + self.speed
        else:
            self.set()

    def crash(self):
        x,y = pygame.mouse.get_pos()
        if self.x < x + 40 and self.x > x - 40 and self.y < y + 40 and self.y > y - 40:
            screen.blit(im_crash,(x-20,y-20))
            Game_Over()

class crashdown(object):
    
    def __init__(self):
        self.flag = False
        self.dead_time = 0
        
    def create(self,x,y):
        self.x = x
        self.y = y
        self.flag = True
        self.dead_time = 500
        
    def die(self):
        if self.dead_time == 0:
            self.flag = False
            self.x = 0
            self.y = 0
        else:
            self.dead_time -= 1
 
def Game_Over():
    global score
    pygame.display.update()
    print ("Your score:%d\nClick to restart...\n" % score)
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for e in enemy:
                    e.set()
                for b in bullet:
                    b.set()
                score = 0
                flag = False
                
pygame.init()
screen = pygame.display.set_mode((500,700),0,32)
pygame.display.set_caption("HIT PLANE")

#image
background = pygame.image.load("Resource/bg.jpg").convert_alpha()
plane = pygame.image.load("Resource/plane.png").convert_alpha()
im_bullet = pygame.image.load("Resource/bullet.jpg").convert_alpha()
im_enemy = pygame.image.load("Resource/enemy.png").convert_alpha()
im_crash = pygame.image.load("Resource/crash.png").convert_alpha()

a = int(raw_input("The number of enemies:"))
b = int(raw_input("The number of bullets:"))

print("\n--------Game Start--------\nPress space to pause\n")

bullet = [bullet() for x in range(b)]
enemy = [enemy() for x in range(a)]
crashdown = [crashdown() for x in range(a)]


while True:

    for b in bullet:
        b.move()
        b.hit()
        
    for e in enemy:
        e.crash()
        e.move()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print ("Game Pause\nPress space to continue\n")
            pause = True
            while pause:
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                        pause = False
            print ("Game continues in 2 seconds...\n")
            time.sleep(2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for temp in bullet:
                if temp.fired == False:
                    temp.fired = True
                    break
                
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    screen.blit(background,(0,0))

    for b in bullet:
        screen.blit(im_bullet,(b.x-(im_bullet.get_width()/2),b.y-(im_bullet.get_height()/2)))
        
    for e in enemy:
        screen.blit(im_enemy,(e.x-(im_enemy.get_width()/2),e.y-(im_enemy.get_height()/2)))

    for c in crashdown:
        if c.flag == True:
            screen.blit(im_crash,(c.x-(im_crash.get_width()/2),c.y-(im_crash.get_height()/2)))
            c.die()
    
    x,y = pygame.mouse.get_pos()
    x -= plane.get_width() / 2
    y -= plane.get_height() / 2
    screen.blit(plane,(x,y))
    
    pygame.display.update()
