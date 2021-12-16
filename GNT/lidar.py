import math
import pygame
import numpy as np

def uncertainty_add(distance,angle,sigma):
    mean = np.array([distance,angle])
    covariance = np.diag(sigma**2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance,0)
    angle = max(angle,0)
    return [distance,angle]

class Sensor:
    def __init__(self,range,map,uncertainty) -> None:
        self.range = range
        self.spin = 5
        self.sigma = np.array([uncertainty[0],uncertainty[1]])
        self.pos = (0,0) # also location of the robot
        self.map  = map
        self.w,self.h = pygame.display.get_surface().get_size()

    def distance(self,obspos):
        px = (obspos[0]-self.pos[0])**2
        py = (obspos[1]-self.pos[1])**2
        return math.sqrt(px+py)

    def sense_obstacles(self,ang):
        data = []
        x1,y1 = self.pos[0],self.pos[1]
        for angle in np.linspace(0,2*math.pi,360,False):
            angle+=ang
            x2,y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            for i in range (0,200):
                u = i / 200
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.w and 0 < y < self.h:
                    color = self.map.get_at((x,y))
                    if (color[0],color[1],color[2]) == (255,0,0):
                        break
                    if (color[0],color[1],color[2]) == (0,0,0):
                        distance = self.distance((x,y))
                        output = uncertainty_add(distance, angle, self.sigma)
                        output.append(self.pos)
                        data.append(output)
                        break
                        
        if len(data) > 0:
            return data
        else:
            return False

    def sense_gaps(self,ang):
        data = []
        x1,y1 = self.pos[0],self.pos[1]
        for angle in np.linspace(0,2*math.pi,360,False):
            angle+=ang
            x2,y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            for i in range (0,200):
                u = i / 200
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.w and 0 < y < self.h:
                    color = self.map.get_at((x,y))
                    if (color[0],color[1],color[2]) == (0,0,0):
                        break
                    if i ==199:
                        distance = self.distance((x,y))
                        output = uncertainty_add(distance, angle, self.sigma)
                        output.append(self.pos)
                        data.append(output)
                        break

        if len(data) > 0:
            return data
        else:
            return False

