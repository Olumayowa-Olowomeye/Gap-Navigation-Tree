import pygame
import math
from simple_pid import PID
class Robot:
    def __init__(self,startpos,robotImg,width) -> None:
        self.m2p = 3780 #meters/pixels
        self.l = width 
        self.x = startpos[0]
        self.y= startpos[1]
        self.theta = 0
        self.vl = 0.001*self.m2p
        self.vr = 0.001*self.m2p
        self.maxspeed = 0.01*self.m2p
        self.minspeed = 0.01*self.m2p
        self.pid = PID()

        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
        self.theta = 0
        self.gapToChase = ""
        self.desired_angle = self.theta
    def draw(self,map):
        map.blit(self.rotated, self.rect)

    # def move(self,event = None):
    #     if event is not None:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_q :
    #                 self.vl+=0.0005*self.m2p
    #             if event.key == pygame.K_a:
    #                 self.vl-=0.0005*self.m2p
    #             if event.key == pygame.K_e:
    #                 self.vr+=0.0005*self.m2p
    #             if event.key == pygame.K_d:
    #                 self.vr-=0.0005*self.m2p
    #             if event.key == pygame.K_w:
    #                 self.vr=0.001*self.m2p
    #                 self.vl=0.001*self.m2p
    #             if event.key == pygame.K_s:
    #                 self.vr=-1*0.001*self.m2p
    #                 self.vl=-1*0.001*self.m2p
    #     pid = PID(1,1,0,setpoint=self.theta)
    #     self.x+=((self.vl+self.vr)/2)*math.cos(self.theta)*dt
    #     self.y-=((self.vl+self.vr)/2)*math.sin(self.theta)*dt
    #     self.theta += (self.vr-self.vl)/self.l*dt


        # self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        # self.rect = self.rotated.get_rect(center=(self.x,self.y))


    def checkbound(self,map):
        color = map.get_at((int(self.x),int(self.y)))
        if (color[0],color[1],color[2]) == (0,0,0):
            self.vl =0
            self.vr=0
            
    def move(self,dt):
        self.pid = PID(.5,1,.4,setpoint=math.radians(self.desired_angle))
        w = self.pid(self.theta)
        self.theta += w *dt
        self.vr = (w*self.l) + self.vl
        self.vl = -1*((w*self.l) - self.vr)
        self.x+=((self.vl+self.vr)/2)*math.cos(self.theta)*dt
        self.y-=((self.vl+self.vr)/2)*math.sin(self.theta)*dt
        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))

    # def chasegap(self,gaps,dt):
    #     if self.gapToChase == "":
    #         self.gapToChase = random.choice(gaps)

    #     if "R" in self.gapToChase and self.gapToChase in gaps:
    #         self.desired_angle = 0
    #         self.move(dt)
    #     if "L" in self.gapToChase and self.gapToChase in gaps:
    #         self.desired_angle = 180
    #         self.move(dt)

        
    def forward(self,x):
        pass
    def backward(self,x):
        pass
    def turn(self,theta):
        pass
    def get_theta(self):
        return self.theta
    def getpos(self):
        return [self.x,self.y]
