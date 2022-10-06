import math
import pygame
import numpy as np
from bresenham import bresenham

# def uncertainty_add(distance,angle,sigma):
#     mean = np.array([distance,angle])
#     covariance = np.diag(sigma**2)
#     distance, angle = np.random.multivariate_normal(mean, covariance)
#     distance = max(distance,0)
#     angle = max(angle,0)
#     return [distance,angle]

class Sensor:
    def __init__(self,range,map,uncertainty) -> None:
        self.range = range
        self.spin = 5
        self.sigma = np.array([uncertainty[0],uncertainty[1]])
        self.pos = (0,0) #location of the robot
        self.map  = map
        self.w,self.h = pygame.display.get_surface().get_size()

    def distance(self,obspos):
        px = (obspos[0]-self.pos[0])**2
        py = (obspos[1]-self.pos[1])**2
        x=math.sqrt(px+py)
        return x

    def sense_obstacles(self,ang):
        data = []

        x1,y1 = int(self.pos[0]),int(self.pos[1])
        for angle in np.linspace(0,2*math.pi,180,False):
            angle+=ang
            x2,y2 = int(x1 + self.range * math.cos(angle)), int(y1 - self.range * math.sin(angle))
            points =list(bresenham(x1,y1,x2,y2))
            for i in points:
                x=i[0]
                y=i[1]
                if 0 < x < self.w and 0 < y < self.h:
                    color = self.map.get_at((x,y))
                    if (color[0],color[1],color[2]) == (255,0,0):
                        break
                    if (color[0],color[1],color[2]) == (0,0,0):
                        distance = self.distance((x,y))
                        # output = uncertainty_add(distance, angle, self.sigma)
                        # output.append(self.pos)
                        output = [distance,angle,self.pos]
                        data.append(output)
                        break
        if len(data) > 0:
            return data
        else:
            return False
    def sense_gaps(self,ang):
        data = []
        x1,y1 =  int(self.pos[0]),int(self.pos[1])
        for angle in np.linspace(0,2*math.pi,180,False):
            angle+=ang
            x2,y2 = int(x1 + self.range * math.cos(angle)), int(y1 - self.range * math.sin(angle))
            points =list(bresenham(x1,y1,x2,y2))
            for i in points:
                x=i[0]
                y=i[1]
                if 0 < x < self.w and 0 < y < self.h:
                    x=i[0]
                    y=i[1]
                    color = self.map.get_at((x,y))
                    if (color[0],color[1],color[2]) == (0,0,0):
                        break
                    if i ==points[-1]:
                        distance = self.distance((x,y))
                        # output = uncertainty_add(distance, angle, self.sigma)
                        # output.append(self.pos)
                        output = [distance,angle,self.pos]
                        data.append(output)
                        break
        if len(data) > 0:
            return data
        else:
            return False

