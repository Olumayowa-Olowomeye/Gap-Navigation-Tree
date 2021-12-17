
from time import sleep
import lidar
import sensor
import math
import pygame
import networkx as nx
import matplotlib.pyplot as pltpy
from simple_pid import PID
import random
import time
environment = sensor.GNTmap((600,1200))
environment.originalMap = environment.map.copy()
laser = lidar.Sensor(500,environment.originalMap,uncertainty=(0,0))
environment.map.fill((0,0,0))
environment.infomap = environment.map.copy()
#robot
dt =0
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
        self.pid = PID(.05,.03,0,setpoint=math.radians(self.desired_angle))
        w = self.pid(self.theta)
        self.theta += w *dt
        self.vr = (w*self.l) + self.vl
        self.vl = -1*((w*self.l) - self.vr)
        self.x+=((self.vl+self.vr)/2)*math.cos(self.theta)*dt
        self.y-=((self.vl+self.vr)/2)*math.sin(self.theta)*dt
        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))

    def chasegap(self,gaps,dt):
        if self.gapToChase == "":
            self.gapToChase = random.choice(gaps)

        if "R" in self.gapToChase and self.gapToChase in gaps:
            self.desired_angle = 0
            self.move(dt)
        if "L" in self.gapToChase and self.gapToChase in gaps:
            self.desired_angle = 180
            self.move(dt)

        
        

    def get_theta(self):
        return self.theta
    def getpos(self):
        return [self.x,self.y]

start = (402,395)

robot = Robot(start,'robot.png',0.01*3779.52)


lasttime = pygame.time.get_ticks()
s= 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # robot.move(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 :
                s=10
            if event.key == pygame.K_2:
                s=20
            if event.key == pygame.K_3:
                s=30
            if event.key == pygame.K_4:
                s=40
    dt = (pygame.time.get_ticks() - lasttime)/1000
    lasttime=pygame.time.get_ticks()
    pos = robot.getpos()
    ang = robot.get_theta()
    # print(pos)
    laser.pos = pos
    sensor_data = laser.sense_obstacles(ang)
    gap_data = laser.sense_gaps(ang)
    environment.datastorage(sensor_data)
    environment.datastoragegap(gap_data)
    environment.showdata(pos,laser.range)
    gaps = environment.Treehist[-1]
    # print(gaps)
    robot.desired_angle = s
    robot.chasegap(gaps,dt)
    robot.checkbound(environment.floormap)
    robot.draw(environment.infomap)
    print(math.degrees(ang))
    print(robot.desired_angle)
    environment.map.blit(environment.infomap, (0,0))
    
    pygame.display.update()
    


# while running:
#     collect=0
#     ICP = False
#     sensoron = False
#     disable_auto_ICP = True
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if pygame.mouse.get_focused():
#             sensoron = True
#         if event.type == pygame.KEYDOWN:
#             # if event.key == pygame.K_1:
#             #     environment.gapprev = environment.gapcloud
#             if event.key == pygame.K_2:
#                 environment.gapanalysis()
#             if event.key == pygame.K_3:
#                 environment.printdata()
#         elif not pygame.mouse.get_focused():
#             sensoron = False
#     if sensoron:
#         pos = pygame.mouse.get_pos()
#         laser.pos = pos
#         sensor_data = laser.sense_obstacles()
#         gap_data = laser.sense_gaps()
#         environment.datastorage(sensor_data)
#         environment.datastoragegap(gap_data)
#         environment.showdata(pos,laser.range)
#         collect+=1
#     environment.map.blit(environment.infomap, (0,0))
#     pygame.display.update()
    
pygame.quit()