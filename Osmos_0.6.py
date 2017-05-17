#########################################
# Osmos - Mr. Curran - Jan 2017         #
# Eat the smaller creatures,            #
# Don't get eaten by the bigger ones!   #
# Version 0.6                           #
#########################################


import pygame
import random

#initialise pygame
pygame.init()
clock = pygame.time.Clock()

#Colours - in CAPS because they are constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

#Screen size
screenX = 700
screenY = 500

#Launch the screen
screen = pygame.display.set_mode([screenX,screenY])

#Set the title
pygame.display.set_caption("Osmos 0.6 - Mr. Curran - 2017")

#GameSpeed
baseSpeed = 1

#Game Difficulty
difficulty = "medium"

#Number of monsters
numMobs = 100

#Class (template) for player
class Player():
    def __init__(self,startX,startY,size):
        #Basic Attributes
        self.x = startX
        self.y = startY
        self.size = size
        self.playerDead = False

    def draw(self):
        pygame.draw.rect(screen,RED,[self.x,self.y,self.size,self.size])

    def eatMob(self,mobStack):
        
        for mob in mobStack:

            if isPointBetween(self.x,self.y,self.size,mob.x,mob.y) or isPointBetween(self.x,self.y,self.size,mob.x + mob.size,mob.y) or isPointBetween(self.x,self.y,self.size,mob.x,mob.y + mob.size) or isPointBetween(self.x,self.y,self.size,mob.x + mob.size,mob.y + mob.size):

                if self.size >= mob.size:
                    self.size += mob.size * 0.5
                    mobStack.remove(mob)


                #YOU ARE HERE - THE PLAYER GETS EATEN!
                else:
                    mob.size += self.size * 0.5
                    self.playerDead = True


#Class (template) for enemies
class Enemy():
    def __init__(self,startX,startY,size):
        #Basic Attributes
        self.x = startX
        self.y = startY

        self.size = size

        #Sequence to select starting direction
        self.startDirs = [-1,1]

        self.speedX = (baseSpeed/self.size) * random.choice(self.startDirs)
        self.speedY = (baseSpeed/self.size) * random.choice(self.startDirs)



        self.colour = BLACK

    def screenCollision(self):
        if (self.x + self.size) >= screenX:
            self.x = screenX - self.size
            self.speedX = self.speedX *-1
        elif self.x <= 0:
            self.x = 0
            self.speedX *=-1

        if (self.y + self.size) >= screenY:
            self.y = screenY - self.size
            self.speedY *=-1
        elif self.y <= 0:
            self.y = 0
            self.speedY *=-1
        
    def mobCollision(self,mobStack):
        
        for mob in mobStack:
            xCol = False
            yCol = False
            buffer = 2

            #If we're not looking at ourself (because this mob is in the stack it's looking at)...
            if self.x != mob.x and self.y != mob.y:

                #Collision check
                if self.x + self.size >= mob.x and self.x <= mob.x + mob.size:
                    xCol = True          

                if self.y + self.size >= mob.y and self.y <= mob.y + mob.size:
                    yCol = True

                if xCol == True and yCol == True:
            
                    #Eat the other monster!
                    if self.size > mob.size:
                        #Remove it from the stack
                        mobStack.remove(mob)
                        #Gain half of its size
                        self.size += mob.size *0.5


    def move(self, mobStack):
        self.speed = baseSpeed / self.size
        self.x += self.speedX
        self.y += self.speedY
        self.screenCollision()
        self.mobCollision(mobStack)

    def draw(self):
        pygame.draw.rect(screen,self.colour,[self.x,self.y,self.size,self.size])



class Level():
    def __init__(self,player,numMobs,speed):


        #Basic Attributes
        self.player = player
        self.numMobs = numMobs
        self.speed = speed

        self.pXSpeed = 0
        self.pYSpeed = 0

        self.mobStack = []

        #Generate Mobs
        for i in range (numMobs):
            newMob = Enemy(random.randrange(0,screenX),random.randrange(0,screenY),random.randrange(3,10))
            self.mobStack.append(newMob)
        


    #Run a level
    def gameLoop(self):
        
        levelEnd = False

        while not levelEnd:

            #Check if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    levelEnd = True

                #Check for key presses and move the player
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.pXSpeed = - 3
                    elif event.key == pygame.K_RIGHT:
                        self.pXSpeed = 3
                    elif event.key == pygame.K_UP:
                        self.pYSpeed = -3
                    elif event.key == pygame.K_DOWN:
                        self.pYSpeed = 3


                #Stop moving if the player has released the arrow.
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.pXSpeed = 0
                    elif event.key == pygame.K_RIGHT:
                        self.pXSpeed = 0
                    elif event.key == pygame.K_UP or pygame.K_DOWN:
                        self.pYSpeed = 0


            #Game logic functions
            for mob in self.mobStack:
                mob.move(self.mobStack)


            if player.playerDead == False:
                ##Move the player
                player.x += self.pXSpeed
                player.y += self.pYSpeed
                player.eatMob(self.mobStack)


            #Clear the screen
            screen.fill(WHITE)

            #Drawing functions
            if player.playerDead == False:
                player.draw()

            for mob in self.mobStack:
                mob.draw()
            

            #Add current drawings
            pygame.display.flip()

            #Limit clock to 60 frames per second
            clock.tick(60)

            if player.playerDead:
                pass

        pygame.quit()


#Game Tools

#Collision detection
def isPointBetween(rectX,rectY,rectSize,pointX,pointY):
    if pointX > rectX and pointX < rectX + rectSize and pointY > rectY and pointY < rectY + rectSize:
        return True

#Menus

#Menu tools

#Print text centred
def centrePrint(text,yPos,fontSize,colour):
    font = pygame.font.SysFont("Impact Regular.ttf",fontSize)
    text = font.render(text,True,(colour))

    textWidth = text.get_width()

    screen.blit (text,((screenX / 2) -  (textWidth /2),yPos))

#Print text anywhere
def anyPrint(text,xPos,yPos,fontSize,colour):
    font = pygame.font.SysFont("Impact Regular.ttf",fontSize)
    text = font.render(text,True,(colour))

    screen.blit (text,(xPos,yPos))   
        
    

    
#Set colour for selected text
def activeText(textID,playerSelection):
    if textID == playerSelection:
        return RED
    else:
        return BLACK

#Main Menu
def mainMenu():


    ###YOU ARE HERE! We need an options menu and a way to launch the game!

    gameEnd = False

    playerSelection = 0
    numSelects = 2
  
    while not gameEnd:

        
        #Check if the user wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameEnd = True

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    playerSelection -=1
                    if playerSelection <0:
                        playerSelection = numSelects
                    
                elif event.key == pygame.K_DOWN:
                    playerSelection +=1
                    if playerSelection >numSelects:
                        playerSelection = 0

                elif event.key == pygame.K_RETURN:
                    if playerSelection == 0:
                        print("Play game!")
                    elif playerSelection == 1:
                        optionsMenu()
                    elif playerSelection == 2:
                        gameEnd = True
                      
                    

        screen.fill(WHITE)
        centrePrint("OSMOS",screenY/3,120,BLACK)
        centrePrint("PLAY GAME",screenY /2,50,activeText(0,playerSelection))
        centrePrint("OPTIONS",screenY/2 + 40,35,activeText(1,playerSelection))
        centrePrint("QUIT",screenY/2 + 70,25,activeText(2,playerSelection))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def optionsMenu():

    ####YOU ARE HERE: Setting up the options menu with horizontal choices!

    gameEnd = False

    global difficulty

    playerSelection = 0
    numSelects = 3
  
    while not gameEnd:

        
        #Check if the user wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameEnd = True

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    playerSelection -=1
                    if playerSelection <0:
                        playerSelection = numSelects
                    
                elif event.key == pygame.K_DOWN:
                    playerSelection +=1
                    if playerSelection >numSelects:
                        playerSelection = 0

                elif event.key == pygame.K_RETURN:
                    if playerSelection == 0:
                        difficulty = "easy"
                    elif playerSelection == 1:
                        difficulty = "medium"
                    elif playerSelection == 2:
                        difficulty = "hard"
                    elif playerSelection == 3:
                        return
                      
                    

        screen.fill(WHITE)
        #Add squares to show wich difficulty is selected
        if difficulty == "easy":
            pygame.draw.rect(screen,RED,[screenX/2 - 85,screenY / 2 + 47,10,10])
            pygame.draw.rect(screen,RED,[screenX/2 + 75,screenY / 2 + 47,10,10])
        elif difficulty == "medium":
            pygame.draw.rect(screen,RED,[screenX/2 - 115,screenY / 2 + 77,10,10])
            pygame.draw.rect(screen,RED,[screenX/2 + 105,screenY / 2 + 77,10,10])
        else:
            pygame.draw.rect(screen,RED,[screenX/2 - 170,screenY / 2 + 107,10,10])
            pygame.draw.rect(screen,RED,[screenX/2 + 160,screenY / 2 + 107,10,10])
        
        centrePrint("OSMOS",screenY/3,120,BLACK)
        centrePrint("Difficulty:",screenY /2,50,BLACK)
        centrePrint("RELAXING", screenY /2 + 40,40,activeText(0,playerSelection))
        centrePrint("CHALLENGING",screenY /2 + 70,40,activeText(1,playerSelection))
        centrePrint("VERY, VERY DIFFICULT", screenY /2 + 100,40,activeText(2,playerSelection))

        centrePrint("Back",screenY/2 + 130,25,activeText(3,playerSelection))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


######TESTING######
player = Player(screenX/2,screenY/2,10)
lvl = Level(player,100,100)
lvl.gameLoop()

#mainMenu()


##################

