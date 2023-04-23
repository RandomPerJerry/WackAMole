# Jerry Zhang
# WackAMole
# Apr 12

import pygame, sys
import random, time


# setting pygame up
pygame.init()

# setting window and cloak up
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Wack A Mole")

clock = pygame.time.Clock()


# This function returns the cordinates of the mouse
def mousefind():
    return pygame.mouse.get_pos()


# Creating the mole class
class Mole():

    # defining the data of the mole
    def __init__(self):

        # importing the image and scaling it to a ideal size
        self.image = pygame.image.load("Image\Mole.png")
        self.image = pygame.transform.scale(self.image, (200, 150))

        # importing the death image and scaling it
        self.normalimage = self.image
        self.deathimage = pygame.image.load("Image\Explosion.png")

        #Setting up the location it could be
        self.x = random.choice([100, 300, 500])
        self.y = random.choice([0, 225, 450])
        
        # the sound when the mole gets hit
        self.deathsound = pygame.mixer.Sound("Audio\DeathSFX.mp3")

        #ticks for time mesuring
        self.point = 0
        self.timetick = 0

        #Death tick is time how long it will take for the mole to respawn after getting hit
        self.deathtimetick = 0

        #If this is true, the mole will enter a respawn timer
        self.gothit = False

        #This is designed for the death image to fit in the programme.
        self.duringhit = False

  


    # Drawing the image
    def draw(self):

        # This if statement check to see if the mole got hit,
        # if it did, then the "deathtimtick" with start ticking
        # Once it reaches 64(2 seconds at x1 speed), the mole will respawn
        if self.gothit == False or self.deathtimetick > 64:  
            #Since there are two images with diffrent size:the mole, and the explosion. 
            #There will be two seperate ways to draw it(the cordinate it needs to be drawn in the holes has to change)
            #if duringhit == true, then it means its in its "explosion phase", if not then its in its normal "mole phase"
            if self.duringhit == True:
                screen.blit(self.image, (self.x-85, self.y-200))
            else:
                screen.blit(self.image, (self.x, self.y))

            #setting the deathtimetick back to 0 and gothit is now back to false
            self.deathtimetick = 0
            self.gothit = False

            #This increases the deathtimetick, when the mole is hit and deathtimetick is below 64(more points=faster number growth)
        else:
            self.deathtimetick += 1 + self.point/20

    # Image it moves
    def move(self):
        #making it change positions every 2 seconds, gets faster when there are more points
        
        self.timetick += 1 + self.point/50

        # I put this here in order for the explosion image to stay on the screen
        if self.timetick > 32 and self.duringhit == True:
            self.gothit = True
            self.duringhit = False

        # This loop mesures the time and moves the mole every 2 seconds in x1 speed
        if self.timetick > 64:
            self.image = self.normalimage
            self.timetick = 0
            self.x = random.choice([100, 300, 500])
            self.y = random.choice([0, 225, 450]) 
    
    def hitbox(self):
        #checking if the mouse clicked the mole and see if the mole is in its "mole phase", not if its in its "explosion phase"
        if self.x < mousefind()[0] < self.x + 200 and \
        self.y < mousefind()[1] < self.y + 150 and self.image == self.normalimage: 

            #plays the death sound, setting timetick 0 so the explosion image could stay on the screen for 64 tick    
            #display image is now the explosion image, add 10 points, duringhit is true means the mole is in his "explosion phase"       
            self.deathsound.play()
            self.timetick = 0
            self.image = self.deathimage 
            self.point += 10
            self.duringhit = True

        #This else staement runs when the player clicked the mouse but did not hit the mole
        else:
            #This if statement make sures the player is above 0 so when the player lose score the score wont be negative
            if self.point > 0:
                self.point -= 5


    # This function is responsible for the score and speed count
    def score(self):
        return self.point, 1 + self.point/50
            

# Hammer class
class Wacker():
    def __init__(self):
        #starting cordinates
        self.x = 325
        self.y = 550 

        #importing the image
        self.image = pygame.image.load("Image\Hammer.png")
        self.image = pygame.transform.scale(self.image, (150, 150))

        #The two hammer image, one when the hammer is in the "waiting phase", the rotateimage is when the player hits
        self.normalimage = self.image
        self.rotateimage = pygame.transform.rotate(self.image, -45)

        #import sound
        self.hitsound = pygame.mixer.Sound("Audio\HammerSFX.mp3")

        #setting up timer
        self.startcloak = time.time()
        self.currentcloak = 0

    #This function runs when the player clicks
    def get_click(self, pos):

        #adjusting the image position
        self.x = pos[0]-150
        self.y = pos[1]-40

        #Plays the hammer hitting sound and rotate the image 45 degrees when player clicks
        self.hitsound.play()
        self.image = self.rotateimage

        #start timer
        self.startcloak = time.time()
        self.currentcloak = time.time()
        
    
    def draw(self):
        #draw the hammer
        screen.blit(self.image, (self.x, self.y))
        self.currentcloak = time.time()

        #The hammer will return to its original position after the player clicks
        if self.currentcloak - self.startcloak > 1:
            self.x = 325
            self.y = 550

            #Rotating the image back to normal
            self.image = self.normalimage


# Naming the mole 
arthur = Mole()
Hammer = Wacker()

Rungame = True

#Game loop
while Rungame: 
    #constantly filling it white as a update system
    screen.fill((102,205,0))

    # drawing the holes
    for i in range(3):
        pygame.draw.ellipse(screen, (0, 0, 0), (120 + 200*i, 75, 150, 70))
        pygame.draw.ellipse(screen, (0, 0, 0), (120 + 200*i, 300, 150, 70))
        pygame.draw.ellipse(screen, (0, 0 ,0), (120 + 200*i, 525, 150, 70))

    #setting the font
    font = pygame.font.Font(None, 36)
    
    # Seeing if the viewer decides to quit. If yes, exist pygame and the system
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RunGame = False
            pygame.quit()
            sys.exit()
        
        # When player click the mouse, the hammer will move to player mouse position and hit
        # Then the system will check if your click is in the mole's hitbox
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                Hammer.get_click(mousefind())
                arthur.hitbox()


    #Its movement
    arthur.move()
    arthur.draw()

    #hammer movement
    Hammer.draw()

    #draws the score on the top left corner
    scoretext = font.render(f'Score: {arthur.score()[0]}', True, (255, 255, 255))
    screen.blit(scoretext, (10, 10))

    #draws the speed multiplier on the top right
    speedtext = font.render(f'Speed: x{arthur.score()[1]}', True, (255, 255, 255))
    screen.blit(speedtext, (650, 10))

    #Update the game and setting up the tick(fps)
    pygame.display.update()
    clock.tick(32)