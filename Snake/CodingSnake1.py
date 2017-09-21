import pygame, random, sys
from pygame.locals import *


'''Declare constants'''

WW = 800
WH = 600
border = 10


'''Color'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)



'''Initialize window and pygame'''

pygame.init()
window = pygame.display.set_mode((WW, WH))
pygame.display.set_caption("Snake")
fps = pygame.time.Clock()



'''Snake class variable'''
snake_length = 3
segment_width = 15
segment_height = 15
segment_margin = 3
x_change = segment_width + segment_margin
y_change = 0


'''Apple class variable'''
apple_size = 15






def setupScreen():
    #Fills up the screen with blue background but with a black rectangle to create border line
    window.fill((BLUE))
    pygame.draw.rect(window, BLACK, (border, border, WW-2*border, WH - 2*border))
    
    
    

    

#Set up segment class
class Segment(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(GREEN)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
    #Logic to test if the object hits the wall
    def wallCollide(self):
        if self.rect.x < border:
            return True
        elif self.rect.x + segment_width > WW-2*border:
            return True
        if self.rect.y < border:
            return True
        elif self.rect.y + segment_height > WH-2*border:
            return True
        else:
            return False



#Set up apple class
class Apple(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface([apple_size, apple_size])
        self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        




'''Sprite group'''
        
        
#Declare sprite group
allspriteslist = pygame.sprite.Group()
applelist = pygame.sprite.Group()


'''Apple object'''

def applespawn():
    for i in range(1):
        x = random.randrange(border, WW-2*border)
        y = random.randrange(border, WH-2*border)
        apple = Apple(x, y)
        applelist.add(apple)

    



    
    
    
'''Snake Object'''        


#A list to store the snake block
snake_segments = []


#This function will initialize the segments position and the length
def startingsnake():    
    
    #As a start, it will take in the snake length (3) and draw 3 rectangles
    for i in range(snake_length):
        #Declare x,y as starting position for the segment and multiply by 3 (snake length)
        x = (WW/4) - (segment_width + segment_margin) * i
        y = WH/2
        segment = Segment(x, y)
        #Append the segments into a list and Group them
        snake_segments.append(segment)
        allspriteslist.add(segment)
        

#This function deletes the end segment and increase the front segment by 1 so 
#it makes it seems like it is moving.
def snakemove():
    #Deletes the end segment
    old_segment = snake_segments.pop()
    allspriteslist.remove(old_segment)
    
    #Declare new position for new segment
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y)
    
    #Insert the segment at the front
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)








'''Snake eats apple and grows'''
    
#This function detects apple and snake collision
def collision(allspritelist, applelist):
    #When the segment group collide with the apple group, False = keep segment, True = Delete apple
    if pygame.sprite.groupcollide(allspritelist, applelist, False, True):
        applespawn()
        new_segment = Segment(20, 20)
        snake_segments.append(new_segment)
        allspritelist.add(new_segment)




   
   
   



'''Main Function Starts Here'''

def main():
    
    global x_change, y_change
    
    #This must be declare here otherwise the main loop will keep spawning apple and snake 
    startingsnake()
    applespawn()
    
    font = pygame.font.Font(None, 36)
            
    end = False
    game_over = False
    
    while not end:
        
        
        window.fill(BLUE)
        setupScreen()   
        
        
        
        
        '''Events that controls the game'''
        for event in pygame.event.get():
            if event.type == QUIT:
                end = True
                sys.exit()
                pygame.quit()
            
            #Controls using updownleftright key for the direction of snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = (segment_width + segment_margin) * -1
                    y_change = 0
                if event.key == pygame.K_RIGHT:
                    x_change = (segment_width + segment_margin)
                    y_change = 0
                if event.key == pygame.K_UP:
                    x_change = 0
                    y_change = (segment_height + segment_margin) * -1
                if event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = (segment_width + segment_margin)
                

        

        
        collision(allspriteslist,applelist)
    
        snakemove()
        
        allspriteslist.draw(window)
        applelist.draw(window)
    
        
        
        #CHECK COLLISION BETWEEN SNAKE AND WALL       
        if snake_segments[0].wallCollide():
            game_over = True         
            x_change = 0
            y_change = 0            
            
            
        if game_over:
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect()
            text_x = window.get_width() / 2 - text_rect.width / 2
            text_y = window.get_height() / 2 - text_rect.height / 2
            window.blit(text, [text_x, text_y])
        
        
        
        fps.tick(10)
        
        pygame.display.update()
    
    
    
    
    
if __name__=='__main__':
    main()