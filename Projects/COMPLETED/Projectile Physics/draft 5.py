import math
import pygame
from time import sleep

pi = math.pi
power_ = 50#int(input("initial velocity")) #getting initial velocity
angle_ = pi/4#int(input("angle"))*(math.pi/180) #getting initial launch angle


wScreen  = 500 #screen width
hScreen = 500 #screen height
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
    def ParticleTrajectory(startX,startY,vel,angle,time,gravity=9.81):
        velx = math.cos(angle) * vel 
        vely = math.sin(angle) * vel
        
        distX = velx * time
        distY = (vely * time) + (((-1*gravity)*((time)**2))/2)

        newx = round(distX + startX)
        newy = round(startY - distY)
        return(newx,newy)

def redrawWindow():
    trailcover.draw(win)
    trail.draw(win)
    if particle_.y <= hScreen - particle_.radius:
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
simulationspeed = 0.009
delay = (1/(angle_/pi))**3 - ((angle_/pi)*((1/(angle_/pi))**2/15))

particle_ = particle(xstartpoint,ystartpoint,radius,(255,255,255),0)
trailcover = particle(xstartpoint,ystartpoint,radius,screencolour,1)
trail = particle(xstartpoint,ystartpoint,1,(255,0,0),1)

win.fill(screencolour)
run = True
while run:
    if shoot:
        #print("inmotion")
        if trail.y < hScreen - (particle_.radius):
            time += simulationspeed #speed at which simulation runs at
            if particle_.y < hScreen - particle_.radius:
                pos_1 = particle_.ParticleTrajectory(x,y,power,angle,time)
            pos_2 = particle_.ParticleTrajectory(x,y,power,angle,time-(delay*simulationspeed))
            if time >= (delay*simulationspeed):
                trail.x = pos_2[0] #- radius
                trail.y = pos_2[1] #- radius
            trailcover.x = particle_.x
            trailcover.y = particle_.y
            particle_.x = pos_1[0]
            particle_.y = pos_1[1]

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