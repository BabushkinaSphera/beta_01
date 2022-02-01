import pygame
import math
import os
import sys
from random import *
def xyangle(xy, ang ):
    if ang >= 270:
        ang = math.fabs(90-(ang-270))
        if xy == 'x':
            return -math.fabs(90-(ang))
        if xy == 'y':
            return -ang
    
    if ang > 180 and ang <= 270:
        ang = ang - 180
        if xy == 'x':
            return math.fabs(90-(ang))
        if xy == 'y':
            return -ang
    
    if ang > 90 and ang <= 180:
        ang = math.fabs(90-(ang-90))
        if xy == 'x':
            return math.fabs(90-(ang))
        if xy == 'y':
            return ang
    
    if ang <= 90:
        if xy == 'x':
            return -math.fabs(90-(ang))
        if xy == 'y':
            return ang
def angl(ang,angt):
    if ang != angt:
        if (ang - angt < 1 and ang - angt > 0) or (ang - angt > -1 and ang - angt < 0):
            ang = angt
        else:
            if angt > ang:
                if angt > 270 and ang < 90:
                    ang -= 1
                    if ang < 0:
                        ang += 360
                else:
                    ang += 1
            if angt < ang:
                if angt < 90 and ang > 270:
                    ang += 1
                    if ang > 360:
                        ang -= 360
                else:
                    ang -= 1
    return ang
def angleto(xy,txy):
    return -math.degrees(math.atan2(txy[1]-xy[1], txy[0]-xy[0]))-90
def blitRotate(surf, image, xy, originxy, angfb):
    image_rect = image.get_rect(topleft = (xy[0] - originxy[0], xy[1]-originxy[1]))
    offset_center_to_pivot = pygame.math.Vector2(xy) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angfb)
    rotated_image_center = (xy[0] - rotated_offset.x, xy[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angfb)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)
def textblit(text,textsize,rgb,xy):
    if not isinstance(text,str):
        text = str(text)
    font = pygame.font.Font(None, textsize)
    text = font.render(text, True, rgb)
    screen.blit(text, xy)
def d(a,b):
    if b!=0:
        return a/b
    else:
        return 0
resolution = [1920,1080]
screen = pygame.display.set_mode(tuple(resolution))
leftclick = (True, True and False, True and False)
rightclick = (True and False, True and False, True)
#---------------------------------------------------------------------
class ship():
    def __init__(self):
        self.xy = [randint(0,resolution[0]),randint(0,resolution[1])]
        self.m = 10000
        self.ang = randint(0,360)
        self.angm = 0
        self.v = 0
        self.a = 0
        self.f = 0
    #-----------------------------------------------------------------
    class recon():
        def __init__(self):
            self.texture = pygame.image.load('recon.png')
            self.w, self.h = self.texture.get_size()
            self.xy = [resolution[0]/2,resolution[1]/2]
            self.m = 8000
            self.ang = 0
            self.angm = 0
            self.angt = 0
            self.v = 0
            self.a = 0
            self.f = 0
            self.trajectory = [0,0]
        def moveto(self,cxy):
            if pygame.mouse.get_pressed(num_buttons=3) == leftclick:
                self.angt = 270+angleto(tuple((self.xy[0]+cxy[0],self.xy[1]+cxy[1])),pygame.mouse.get_pos())
                self.ang = angl(self.ang, self.angt)
                self.f = 0.5
                return True
            else:
                if self.f > 0:
                    if self.f >= 0.01:
                        self.f -= 0.01
                    else:
                        self.f = 0
                else:
                    self.f = 0
            if pygame.mouse.get_pressed(num_buttons=3) == rightclick:
                self.v -= 1/self.m
            return False
        def friction(self):
            if self.v >= 0.1/self.m:
                self.v -= 0.1/self.m
            else:
                self.v = 0
        def move(self,cxy):
            if not self.moveto(cxy):
                self.friction()
            self.a = self.f/self.m
            self.v += self.a
            self.angm = angl(self.angm,self.ang)
            self.xy = [self.xy[0]+(self.v*xyangle('x',self.angm)),self.xy[1]+(self.v*xyangle('y',self.angm))]
        def blit(self,cxy):
            self.move(cxy)
            textblit(self.xy,20,(255,0,0),(191,127))
            textblit(self.v,20,(255,0,0),(191,147))
            textblit(self.f,20,(255,0,0),(191,167))
            textblit(self.angm,20,(255,0,0),(191,187))
            blitRotate(screen, self.texture, tuple((self.xy[0]+cxy[0], self.xy[1]+cxy[1])), (self.w/2, self.h/2), self.ang+90)

#---------------------------------------------------------------------
class main():
    def __init__(self):
        pygame.init()
        pygame.clock = pygame.time.Clock()
        self.done = False
        self.player = ship.recon()
        self.objects = [self.player]
        self.cxy = [0,0]
        self.zoom = 1
        self.cm1 = False
    def cameraview(self):
        for i in range(0,len(self.objects)):
            if self.cm1:
                self.objects[i].blit(list(((resolution[0]/2)-self.objects[0].xy[0],(resolution[1]/2)-self.objects[0].xy[1])))
            elif not self.cm1:
                self.objects[i].blit(self.cxy)
        for event in pygame.event.get():
            if self.keys[pygame.K_w]:
                self.cxy[1] += self.zoom
            if self.keys[pygame.K_a]:
                self.cxy[0] += self.zoom
            if self.keys[pygame.K_s]:
                self.cxy[1] -= self.zoom
            if self.keys[pygame.K_d]:
                self.cxy[0] -= self.zoom
            if self.keys[pygame.K_F2]:
                self.cm1 = True
            if self.keys[pygame.K_F1]:
                self.cm1 = False
            if event.type == pygame.MOUSEWHEEL:
                self.zoom += event.y
        textblit(self.zoom,20,(255,0,0),(191,217))
    def mainloop(self):
        while not self.done:
            self.keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                    self.done = True
            self.cameraview()
            pygame.display.flip()
            screen.fill(0)
        pygame.quit()
#---------------------------------------------------------------------
m = main()
m.mainloop()
