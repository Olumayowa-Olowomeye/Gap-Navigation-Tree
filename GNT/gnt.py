
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
from Robot import Robot
environment = sensor.GNTmap((600,1200))
environment.originalMap = environment.map.copy()
laser = lidar.Sensor(250,environment.originalMap,uncertainty=(0,0))
environment.map.fill((0,0,0))
environment.infomap = environment.map.copy()
#robot
dt =0
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
                s=0
            if event.key == pygame.K_2:
                s=90
            if event.key == pygame.K_3:
                s=180
            if event.key == pygame.K_4:
                s=270
            if event.key == pygame.K_p:
                time.sleep(10)
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
    robot.desired_angle = s
    # robot.chasegap(gaps,dt)
    robot.move(dt)
    robot.checkbound(environment.floormap)
    robot.draw(environment.infomap)
    
    # print(math.degrees(ang))
    # print(robot.desired_angle)
    environment.map.blit(environment.infomap, (0,0))
    
    pygame.display.update()
    # environment.printdata()
    # running =False
    


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