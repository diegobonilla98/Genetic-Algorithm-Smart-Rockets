import pygame, sys
from pygame.locals import *
from random import random
import numpy as np

pygame.init()
width=height=400
DISPLAYSURF = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('Smart rockets')
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)

popNum=100
lifespan=1200
maxMag=0.01
ttl=0
targetx=width/2
targety=50

class DNA:
    def __init__(self, genx, geny):
        self.genesx=[]
        self.genesy=[]
        if genx==None and geny==None:
            for i in range(lifespan):
                self.genesx.append(random()*2*maxMag-maxMag)
                self.genesy.append(random()*2*maxMag-maxMag)
        else:
            self.genesx=genx
            self.genesy=geny
    def crossover(self, partner):
        newGenesx=[]
        newGenesy=[]
        mid=int(random()*len(self.genesx))
        for i in range(len(self.genesx)):
            if i>mid:
                newGenesx.append(self.genesx[i])
                newGenesy.append(self.genesy[i])
            else:
                newGenesx.append(partner.genesx[i])
                newGenesy.append(partner.genesy[i])
        return DNA(newGenesx, newGenesy)


class Rocket:
    def __init__(self, d):
        self.posx=width/2
        self.posy=height
        self.velx=0
        self.vely=0
        self.accx=0
        self.accy=0
        self.time=0
        self.fitness=0
        if d==None:
            self.dna=DNA(None,None)
        else:
            self.dna=d
    def display(self):
        if self.crash():
            pygame.draw.rect(DISPLAYSURF, RED, (int(self.posx), int(self.posy), 10, 10))
        elif self.goal():
            pygame.draw.rect(DISPLAYSURF, BLUE, (int(self.posx), int(self.posy), 10, 10))
        else:
            pygame.draw.rect(DISPLAYSURF, WHITE, (int(self.posx), int(self.posy), 10, 10))
    def update(self):
        if self.crash()==False or self.goal()==False:
            self.posx+=self.velx
            self.posy+=self.vely
            self.velx+=self.accx
            self.vely+=self.accy
            self.accx*=0
            self.accy*=0
            self.applyForce(self.dna.genesx[ttl], self.dna.genesy[ttl])
    def goal(self):
        if np.sqrt(np.power(targetx-self.posx,2)+np.power(targety-self.posy,2))<10:
            if self.time==0:
                self.time=ttl+1
            return True
        else:
            return False
    def crash(self):
        hit=False
        if self.posx<0 or self.posx>width or self.posy>height+50 or self.posy<0:
            hit=True
        return hit
    def applyForce(self, forcex, forcey):
        self.accx+=forcex
        self.accy+=forcey
    def calcFitness(self):
        d=np.sqrt(np.power(targetx-self.posx,2)+np.power(targety-self.posy,2))
        self.fitness=100*(1/(d+self.time))
        if self.crash():
            self.fitness/=10
        if self.goal():
            self.fitness*=self.time
            self.fitness*=2


class Population:
    def __init__(self):
        self.rocket=[]
        self.matingpool=[]
        for i in range(popNum):
            self.rocket.append(Rocket(None))
    def run(self):
        for i in self.rocket:
            i.display()
            i.update()
    def evaluate(self):
        maxFit=0
        for i in range(popNum):
            self.rocket[i].calcFitness()
            if self.rocket[i].fitness>maxFit:
                maxFit=self.rocket[i].fitness
        for i in range(popNum):
            self.rocket[i].fitness/=maxFit

        lengthOfMatingPool=0
        for i in range(popNum):
            n=int(self.rocket[i].fitness*100)
            lengthOfMatingPool+=n
        currentIndex=0
        for i in range(popNum):
            n=int(self.rocket[i].fitness*100)
            for j in range(n):
                self.matingpool.append(self.rocket[i])
                currentIndex+=1
    def selection(self):
        newRockets=[]
        for i in range(len(self.rocket)):
            idxA=int(random()*len(self.matingpool))
            parentA=self.matingpool[idxA].dna
            idxB=int(random()*len(self.matingpool))
            parentB=self.matingpool[idxB].dna
            child=parentA.crossover(parentB)
            newRockets.append(Rocket(child))
        self.rocket=newRockets

pop=Population()

while True:
    DISPLAYSURF.fill(BLACK)

    pop.run()

    ttl+=1
    if ttl==lifespan:
        pop.evaluate()
        pop.selection()
        ttl=0

    pygame.draw.ellipse(DISPLAYSURF, WHITE, (int(targetx), int(targety), 20, 20))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
