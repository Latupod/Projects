import math
import pygame
from time import sleep

power_ = int(input("initial velocity")) #getting initial velocity
angle_ = int(input("angle"))*(math.pi/180) #getting initial launch angle


wScreen  = 1200 #screen width
hScreen = 800 #screen height

win = pygame.display.set_mode((wScreen,hScreen)) #setting up the window dimensions

class particle():
    def __init__(self,x,y,radius,colour): #initial particle varibales
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
    
    def draw(self,win):
        pygame.draw.circle(win,(0,0,0),(self.x,self.y),self.radius) #drawring circle outline
        pygame.draw.circle(win,self.colour,(self.x,self.y),self.radius-1) #drawring circle
    
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
    win.fill((64,64,64))
    particle.draw(win)
    #pygame.draw.line(win,(255,255,255),line[0],line[1]) #drawring the actualy line 
    pygame.draw.circle(win,(255,0,0),(particle.x-1,particle.y+1),1) #attempt at draring a trajectory path behind the particle
    pygame.display.update()

def findangle(pos):
    sX = particle.x
    sY = particle.y
    try:
        angle = math.atan((sY-pos[1])/(sX-pos[0]))
    except:
        angle = math.pi / 2
    
    if pos[1]<sY and pos[0]>sX:
        angle = abs(angle)
    elif pos[1]<sY and pos[0]<sX:
        angle = math.pi-angle
    elif pos[1]>sY and pos[0]<sX:
        angle = math.pi + abs(angle)
    elif pos[1]>sY and pos[0]>sX:
        angle = (2*math.pi) - angle
    return angle

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

particle = particle(xstartpoint,ystartpoint,radius,(255,255,255))

run = True
while run:
    if shoot:
        print("inmotion")
        if particle.y < hScreen - particle.radius:
            time += 0.020 #speed at which simulation runs at
            pos_ = particle.ParticleTrajectory(x,y,power,angle,time)
            particle.x = pos_[0]
            particle.y = pos_[1]

        else:
            print("grounded")
            shoot = False
            particle.y = ystartpoint

    #pos = pygame.mouse.get_pos() #getting mouse position
    #line = [(particle.x,particle.y),(pos)] #setting up the line
    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Code using a line and "power" to project particle
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shoot == False:
                print("shooting")
                shoot = True
                x= particle.x
                y= particle.y
                time = 0
                power = math.sqrt((line[1][1]-line[0][1])**2 + (line[1][0]-line[0][0])**2)/5
                angle = findangle(pos)
            '''
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if shoot == False:
                    sleep(2)
                    shoot = True
                    x = particle.x
                    y = particle.y
                    power = power_
                    angle = angle_
                    time = 0
pygame.quit()