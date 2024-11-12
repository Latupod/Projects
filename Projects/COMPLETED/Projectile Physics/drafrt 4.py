import math
import pygame
from time import sleep

power_ = 60#int(input("initial velocity")) #getting initial velocity
angle_ = math.pi/3#int(input("angle"))*(math.pi/180) #getting initial launch angle


wScreen  = 600 #screen width
hScreen = 600 #screen height
screencolour = (64,64,64) #screen colour

win = pygame.display.set_mode((wScreen,hScreen)) #setting up the window dimensions

class particle():
    def __init__(self,x,y,radius,colour,type): #initial particle varibales
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.type = type
    
    def draw(self,win):
        if self.type == 0:
            pygame.draw.circle(win,(0,0,0),(self.x,self.y),self.radius) #drawring circle outline
            pygame.draw.circle(win,self.colour,(self.x,self.y),self.radius-1) #drawring circle
        elif self.type == 1:
            pygame.draw.circle(win,(self.colour),(self.x,self.y),self.radius)

    @staticmethod #such the trajectory calc isnt bound to the class, just here for sake of convenience
    def ParticleTrajectory(startX,startY,power,angle,time,gravity=9.81):
        velx = math.cos(angle) * power 
        vely = math.sin(angle) * power

        distX = velx * time
        distY = (vely * time) + (((-1*gravity)*((time)**2))/2)

        newx = round(distX + startX)
        newy = round(startY - distY)

        return(newx,newy)

def redrawWindow():
    trailcover.draw(win)
    trail.draw(win)
    particle_.draw(win)
    pygame.display.update()

x=0
y=0
time = 0
power = 0
angle = 0
shoot = False
radius = 5
#xstartpoint = (wScreen/2) - (radius+1)
xstartpoint = wScreen/4
ystartpoint = hScreen-(radius+1) 

particle_ = particle(xstartpoint,ystartpoint,radius,(255,255,255),0)
trailcover = particle(xstartpoint,ystartpoint,radius,screencolour,1)
trail = particle(xstartpoint,ystartpoint,1,(255,0,0),1)

win.fill(screencolour)
run = True
while run:
    if shoot:
        #print("inmotion")
        if particle_.y < hScreen - particle_.radius:
            time += 0.015 #speed at which simulation runs at
            pos_ = particle_.ParticleTrajectory(x,y,power,angle,time)
            trail.x = particle_.x - radius
            trail.y = particle_.y - radius
            trailcover.x = particle_.x
            trailcover.y = particle_.y
            particle_.x = pos_[0]
            particle_.y = pos_[1]

        else:
            #print("grounded")
            shoot = False
            particle_.y = ystartpoint

    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if shoot == False:
                    sleep(2)
                    shoot = True
                    x = particle_.x
                    y = particle_.y
                    power = power_
                    angle = angle_
                    time = 0
pygame.quit()