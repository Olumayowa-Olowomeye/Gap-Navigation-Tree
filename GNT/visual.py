from numpy.lib.shape_base import get_array_prepare
import pygame
import random
import math
import numpy as np
#Colors
grey = (70, 70, 70)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0,0,0)

class GNTmap:
    def __init__(self, Mapdimensions) -> None:
        pygame.init()
        self.pointcloud = []
        self.gapcloud = []
        self.pointcloudang = []
        self.gapcloudang = []
        self.LMS_data = []
        self.lines = []
        self.floormap = pygame.image.load('i.jpg')
        self.maph ,self.mapw = Mapdimensions
        pygame.display.set_caption("GNT")
        self.map = pygame.display.set_mode((self.mapw,self.maph))
        self.map.blit(self.floormap,(0,0))
        self.l = 1
        self.r = 1
        #gap history
        self.Treesave=[]
        self.Treehist = []
        self.Angles = []

    def AD2pos(self,distance,angle,robopos):
        x = distance * math.cos(angle) + robopos[0]
        y = -distance * math.sin(angle) + robopos[1]
        return [int(x),int(y)]

    def datastorage(self,data):
        self.pointcloudang = data
        if data!=False:
            for element in data:
                point = self.AD2pos(element[0],element[1],element[2])
                if point not in self.pointcloud:
                    self.pointcloud.append(point)

    def datastoragegap(self,data):
        self.gapcloudang = data
        if data!=False:
            for element in data:
                point = self.AD2pos(element[0],element[1],element[2])
                if point not in self.gapcloud:
                    self.gapcloud.append(point)

    def LMS_storage(self,data):
        self.LMS_data = data
        
    def drawwall(self,pos):
        pygame.draw.circle(self.infomap, red, pos, 2)
    def drawgap(self,pos):
        pygame.draw.circle(self.infomap, blue, pos, 2)
      
    def showdata(self,robopos,range):
        self.map.fill(black)
        self.infomap = self.map.copy()

        for point in self.pointcloud:
            self.drawwall(point)
            if self.adistance(point,robopos) > range:
                self.pointcloud.remove(point) 

        for point in self.gapcloud:
            self.drawgap(point)
            dist = self.adistance(point,robopos)
            if dist > range or dist < range-3:
                self.gapcloud.remove(point)

        self.drawlines(robopos)

        check = self.checklines(robopos)
        self.Angles = check[1]
        check = check[0]
        if self.Treesave == []:
            self.Treesave = check
            if self.Treehist ==[]:
                self.Treehist.append(self.Treesave)
            # else:
            #     self.Treehist.append(self.CEhandler(self.Treehist[-1],self.Treesave))
            # print(self.Treesave)
        elif check ==[]:
            pass
        else:
            if check!=self.Treesave:
                self.Treesave = check
                if self.Treehist ==[]:
                    self.Treehist.append(self.Treesave)
                # else:
                #    self.Treehist.append(self.CEhandler(self.Treehist[-1],self.Treesave))
        # self.CEhandler(self.Treesave)
        self.pointcloud.clear()
        self.gapcloud.clear()
       
    def printdata(self):
        print("Point cloud:",self.pointcloudang,'\n\n\n\n\n')    
        print("Gap cloud:",self.gapcloudang) 

    def drawlines(self,robopos):
        self.lines=[]
        if self.gapcloudang != False and self.pointcloudang != False:
            dots = self.gapcloudang + self.pointcloudang
            dots.sort(key = lambda x: x[1])

            for i in range(0,len(dots)-1):
                x = self.AD2pos(dots[i][0],dots[i][1],dots[i][2])
                y = self.AD2pos(dots[i+1][0],dots[i+1][1],dots[i+1][2])
                self.lines.append([x,self.adistance(x,robopos),y,self.adistance(y,robopos)])
            #     pygame.draw.line(self.infomap,(0,255,0),x,y)

            # pygame.draw.line(self.infomap,(0,255,0),self.AD2pos(dots[-1][0],dots[-1][1],dots[-1][2]),self.AD2pos(dots[0][0],dots[0][1],dots[0][2]))
            x = self.AD2pos(dots[-1][0],dots[-1][1],dots[-1][2])
            y = self.AD2pos(dots[0][0],dots[0][1],dots[0][2])
            self.lines.append([x,self.adistance(x,robopos),y,self.adistance(y,robopos)])

        if self.gapcloudang == False and self.pointcloudang != False:
            dots = self.pointcloudang
            dots.sort(key = lambda x: x[1])

            for i in range(0,len(dots)-1):
                x = self.AD2pos(dots[i][0],dots[i][1],dots[i][2])
                y = self.AD2pos(dots[i+1][0],dots[i+1][1],dots[i+1][2])
                self.lines.append([x,self.adistance(x,robopos),y,self.adistance(y,robopos)])
            #     pygame.draw.line(self.infomap,(0,255,0),x,y)

            # pygame.draw.line(self.infomap,(0,255,0),self.AD2pos(dots[-1][0],dots[-1][1],dots[-1][2]),self.AD2pos(dots[0][0],dots[0][1],dots[0][2]))
            x = self.AD2pos(dots[-1][0],dots[-1][1],dots[-1][2])
            y = self.AD2pos(dots[0][0],dots[0][1],dots[0][2])
            self.lines.append([x,self.adistance(x,robopos),y,self.adistance(y,robopos)])

        if self.gapcloudang != False and self.pointcloudang == False:
            dots = self.gapcloudang
            dots.sort(key = lambda x: x[1])

            for i in range(0,len(dots)-1):
                x = self.AD2pos(dots[i][0],dots[i][1],dots[i][2])
                y = self.AD2pos(dots[i+1][0],dots[i+1][1],dots[i+1][2])
                self.lines.append([x,self.adistance(x,robopos),y,self.adistance(y,robopos)])
            #     pygame.draw.line(self.infomap,(0,255,0),x,y)

            # pygame.draw.line(self.infomap,(0,255,0),self.AD2pos(dots[-1][0],dots[-1][1],dots[-1][2]),self.AD2pos(dots[0][0],dots[0][1],dots[0][2]))
            x = self.AD2pos(dots[-1][0],dots[-1][1],dots[-1][2])
            y = self.AD2pos(dots[0][0],dots[0][1],dots[0][2])
            self.lines.append([x,self.adistance(x,robopos),y,self.adistance(y,robopos)])

    def adistance(self,obspos,robopos):
        px = (obspos[0]-robopos[0])**2
        py = (obspos[1]-robopos[1])**2
        return math.sqrt(px+py)
    #checks if dots are close to same line. If they are return false else return true
    def checkdots(self,a,b):
        unc = 3
        ax,ay = a[0], a[1]
        bx,by = b[0], b[1]
        if bx==ax and by==ay:
            return True
        if (ax-unc<= bx <= ax+unc) and (ay-unc<= by <= ay+unc):
            return True
        return False
    def get_angle_gap(self,p1,p2,robopos):
        changeInX = p2[0] - robopos[0]
        changeInY = p2[1] - robopos[1]
        f1= math.degrees(math.atan2(changeInY,changeInX))
        changeInX = p1[0] - robopos[0]
        changeInY = p1[1] - robopos[1]
        f2= math.degrees(math.atan2(changeInY,changeInX))
        return (f1+f2)/2
    '''
    if connecting 2 blue dots: in middle of gap; ignore
    if connecting a blue and red dot: check distance and mark
    if connecting 2 red: check distance within threshold and mark
    '''
    def checklines(self,robopos,threshold=30):
        Tree = []
        Angles =[]
        closegap = False
        l=0
        r=0
        for i in self.lines:
            if i[0] in self.gapcloud and i[2] in self.pointcloud or i[0] in self.pointcloud and i[2] in self.gapcloud:
                if closegap != True:
                    Angles.append(self.get_angle_gap(i[0],i[2],robopos))
                    if i[1] >= i[3]:
                        Tree.append('L{}'.format(l))
                        l+=1
                        pygame.draw.line(self.infomap,white,i[0],i[2])
                    else:
                        Tree.append('R{}'.format(r))
                        r+=1
                        pygame.draw.line(self.infomap,blue,i[0],i[2])
                    closegap =True
                else:
                    closegap = False
            if i[0] in self.pointcloud and i[2] in self.pointcloud:
                if self.adistance(i[0],i[2]) >= threshold and not self.checkdots(i[0],i[2]):
                    if i[0][0] != i[2][0] and i[0][1] != i[2][1]:
                        Angles.append(self.get_angle_gap(i[0],i[2],robopos))
                        if i[1] >= i[3]:
                            Tree.append('L{}'.format(l))
                            l+=1
                            pygame.draw.line(self.infomap,white,i[0],i[2])
                            
                        else:
                            Tree.append('R{}'.format(r))
                            r+=1
                            pygame.draw.line(self.infomap,blue,i[0],i[2])
        # print([Tree,Angles])         
        return [Tree,Angles]

    def show_LMS(self,robopos,range):
        self.map.fill(black)
        self.infomap = self.map.copy()
        for i in self.LMS_data:

            self.drawwall(i)
        self.LMS_data.clear()

        
