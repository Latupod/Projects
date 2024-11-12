import pygame 
import random 
  
# GLOBAL VARIABLES 
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 
WIDTH = 500
HEIGHT = 500
  
# Object class 
class Sprite(pygame.sprite.Sprite): 
    def __init__(self, color, height, width): 
        super().__init__() 

        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR) 
        self.width = width
        self.height = height
        self.color = color

        pygame.draw.rect(self.image,self.color,pygame.Rect(0, 0, self.width, self.height)) 
  
        self.rect = self.image.get_rect() 

  
pygame.init() 
  
RED = (255, 0, 0) 
  
size = (WIDTH, HEIGHT) 
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Creating Sprite") 
  
all_sprites_list = pygame.sprite.Group() 
  
object1 = Sprite(RED, 30, 30) #rect
object2 = Sprite((0,0,0),10,10) #trail dot
object3 = Sprite((SURFACE_COLOR),30,30) #trail cover

all_sprites_list.add(object1) 
all_sprites_list.add(object3) 
all_sprites_list.add(object2) 

    
exit = True
clock = pygame.time.Clock() 
screen.fill(SURFACE_COLOR)

while exit: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = False
        if event.type == pygame.KEYDOWN:
            object3.rect.x = object2.rect.x = object1.rect.x
            object3.rect.y = object2.rect.y = object1.rect.y
            if event.key == pygame.K_w:
                object1.rect.x += 0#random.randint(0,200)
                object1.rect.y += -30#random.randint(0,300)
            if event.key == pygame.K_a:
                object1.rect.x += -30#random.randint(0,200)
                object1.rect.y += 0#random.randint(0,300)   
            if event.key == pygame.K_s:
                object1.rect.x += 0#random.randint(0,200)
                object1.rect.y += 30#random.randint(0,300)   
            if event.key == pygame.K_d:
                object1.rect.x += 30#random.randint(0,200)
                object1.rect.y += 0#random.randint(0,300)        
        all_sprites_list.update() 
        all_sprites_list.draw(screen)
        pygame.display.flip() 
    #clock.tick(2)  
  
pygame.quit() 