import pygame
import random
import math
import time
from pygame import mixer

# Intialize the pygame
pygame.init()

# screen height = 600 and width = 800
screen = pygame.display.set_mode((800, 600))
# in pygame (0,0) is on left top.
# left to right x increases
# top to bottom y increases

# Title and Icon
pygame.display.set_caption("Jump In Abbys")
icon = pygame.image.load('witch1.png')
pygame.display.set_icon (icon)

# Background
background = pygame.image.load("moonlight.png")

# Platform and gate
platform1= pygame.image.load("platform1.png")
platform2= pygame.image.load("platform2.png")
platform3= pygame.image.load("platform3.png")
platform4= pygame.image.load("platform4.png")
platform5= pygame.image.load("platform5.png")
gate = pygame.image.load("gate.png")

# Spikes
spike=pygame.image.load("spikes.png")

# Sound/music
#mixer.music.load('')
#mixer.music.play(-1) # this will play the music on loop
jumping_sound = mixer.Sound("jump.wav")
jumping_sound.set_volume(0.2)# volume b/w 0-1

landing_sound1 = mixer.Sound("landing1.wav")
landing_sound2 = mixer.Sound("landing2.wav")
inAir = True

fall_sound1 = mixer.Sound("fall1.wav")
fall_sound2 = mixer.Sound("fall2.wav")

enemyDead_sound = mixer.Sound("punch.wav")
enemyDead_sound.set_volume(0.2)

# Player
playerImg = pygame.image.load('wizard1.png')
playerX = 0
playerY = 0
playerX_change = 0
playerY_change = 0
playerY_gravity = 0.98
player_state = "still"

#enemy
enemyImg = pygame.image.load('goblin.png')
enemyX = 450
enemyY = 185
enemyX_change = 2
enemyY_change = 0
enemy_state = "still"

# health
health1 = pygame.image.load("diamond.png")
health2 = pygame.image.load("diamond.png")
health3 = pygame.image.load("diamond.png")
health_1X = 0
health_1Y = 0
health_2X = 20
health_2Y = 0
health_3X = 40
health_3Y = 0
healthLimit = 0

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 65)
textX = 300
textY = 200

# Functions

def player(x, y) :
    global player_state
    player_state = "jump"
    screen.blit(playerImg, (x, y)) #means to draw. it draws image on screen

def enemy(x, y) :
    screen.blit(enemyImg, (x, y))

def landing_Sound() :
    random_sound = random.randint(1, 2)
    if random_sound == 1 :
        landing_sound1.play()
    else:
        landing_sound2.play()

def falling_Sound() :
    random_sound = random.randint(1, 2)
    if random_sound == 1 :
        fall_sound1.play()
    else:
        fall_sound2.play()

def you_won(x, y):
    won_display = font.render("You Won", True, (255, 255, 255))
    score_display = font.render("Score:" +str(score), True, (255, 255, 255))
    screen.blit(won_display, (x, y))
    screen.blit(score_display, (x, y + 70))

def you_loose(x, y):
    loose_display = font.render("You loose", True, (255, 255, 255))
    score_display = font.render("Score:" +str(score), True, (255, 255, 255))
    screen.blit(loose_display, (x, y))
    screen.blit(score_display, (x, y + 70))

WHITE = (255, 255, 255)
f = pygame.font.Font(None, 36)
display_instructions = True
page = 1

# -------- Instruction Page Loop -----------
while display_instructions:
    screen.blit(background, (0, 0))
    player(350,300)
    if page == 1:
        text = f.render("Click On The Screen To Start The Game", True, WHITE)
        screen.blit(text, [150, 270])

        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display_instructions = False
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            page += 1
            if page == 2:
                display_instructions = False
                running = True


# Game Loop 1 ------------------------------------------ #
closing = False
while running:
    
    # Background image
    screen.blit(background, (0, 0))



    # health bar
    screen.blit(health1, (health_1X, health_1Y))
    screen.blit(health2, (health_2X, health_2Y))
    screen.blit(health3, (health_3X, health_3Y))

    # Platform and gate
    screen.blit(platform1, (0,500))
    screen.blit(platform2, (400,300))
    screen.blit(platform3, (600, 100))
    screen.blit(gate, (750,50))
    
    
    for event in pygame.event.get(): #any type of control happens in event
        if event.type == pygame.QUIT: # close button
            running = False
            
        # if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN: # keydown = pressing key
            if event.key == pygame.K_RIGHT:
                playerX_change += 7
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
            if event.key == pygame.K_SPACE:
                if player_state is "still":
                    jumping_sound.play()
                    for jump in range(15):
                            playerY_change -= playerY_gravity + 0.25 
                            playerY += playerY_change 
                            player(playerX, playerY)
                            playerY_gravity -= 0.03
                    playerY_gravity = 0.98
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
    
    
    # while falling
    #   checking whether person is in air so that when landing it wil play sound
    if playerY_change > 0 :#if there is a change(falling) in y axix then 
        inAir = True

    # movment of player
        # always put player img after screenfill because screen is drawn first
        #then character is draw on the screen not behind
    playerX += playerX_change
    # player is define before gravity to let its state be 'jump' in gravity  portion
    player(playerX, playerY)
    # gravity
    playerY_change += playerY_gravity
    playerY += playerY_change 
    
    # Platforms 
    #   platform1
        # height of PF(480-490)              final limit        intial limit
    if (playerY > 480 and playerY < 510) and (playerX <= 300 and playerX >= -10) :
        if inAir : # if change(falling)=0 then this tells us that player is no longer in air
            landing_Sound()
            inAir = False        
        player_state = "still"
        playerY = 480
        playerY_change = 0
    #   platform2
    if (playerY > 250 and playerY < 280) and (playerX <= 540 and playerX >= 360) :
        if inAir :
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 250
        playerY_change = 0
    #   platform3
    if (playerY > 60 and playerY < 80) and (playerX <= 825 and playerX >= 570) :
        if inAir :
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 60
        playerY_change = 0
   

    # Border of left wall
    if playerX < 0:
        playerX = 0

     # respawn back
    if playerY > 650 :
        falling_Sound()
        time.sleep(1)   
        playerY_change = 0
        playerX = 0
        playerY = 0
        healthLimit += 1
    
    # Health limit
    if healthLimit == 1:
        health_3X = 1000
        health_3Y = 1000
    if healthLimit == 2:
        health_2X = 1000
        health_2Y = 1000
    if healthLimit == 3:
        health_1X = 1000
        health_1Y = 1000
        closing = True
        running = False

    
    # End Level
    #   y and x axis of where character reach the door and next level starts
    if (playerY < 70 and playerY > 30) and (playerX >= 740 and playerX <= 770) :
        time.sleep(0.5)
        break
    pygame.display.update() #update the display every time (pixel by pixel)

# Level one ends here ----------------------------------

#pause
time.sleep(0.5)

# Player
playerX = 0
playerY = 0


# Game Loop 2 -----------------------------------------
while running:
    
    # Background image
    screen.blit(background, (0, 0))

    # health bar
    screen.blit(health1, (health_1X, health_1Y))
    screen.blit(health2, (health_2X, health_2Y))
    screen.blit(health3, (health_3X, health_3Y))

    # Platform and gate
    screen.blit(platform2, (0, 500))
    screen.blit(platform5, (250, 400))
    screen.blit(platform4, (450, 200))
    screen.blit(platform5, (740, 400))
    screen.blit(gate, (750,340))

    # Enemy
    enemy(enemyX, enemyY)
    enemyX += enemyX_change
    if enemyX >= 590 or enemyX <= 430:
        enemyX_change *= -1
    
    
    
    for event in pygame.event.get(): #any type of control happens in event
        if event.type == pygame.QUIT: # close button
            running = False
            
        # if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN: # keydown = pressing key
            if event.key == pygame.K_RIGHT:
                playerX_change += 7
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
            if event.key == pygame.K_SPACE:
                if player_state is "still":
                    jumping_sound.play()
                    for jump in range(15):
                            playerY_change -= playerY_gravity + 0.25 
                            playerY += playerY_change 
                            player(playerX, playerY)
                            playerY_gravity -= 0.03
                    playerY_gravity = 0.98
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
    
    
    # while falling
    #   checking whether person is in air so that when landing it wil play sound
    if playerY_change > 0 :#if there is a change(falling) in y axix then 
        inAir = True

    # movment of player
        # always put player img after screenfill because screen is drawn first
        #then character is draw on the screen not behind
    playerX += playerX_change
    # player is define before gravity to let its state be 'jump' in gravity  portion
    player(playerX, playerY)
    # gravity
    playerY_change += playerY_gravity
    playerY += playerY_change 
    
    # Platforms 
    #   platform2
        # height of PF(480-490)              final limit        intial limit
    if (playerY > 450 and playerY < 490) and (playerX <= 125 and playerX >= -10):
        if inAir:  # if change(falling)=0 then this tells us that player is no longer in air
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 450
        playerY_change = 0
    #   platform5
    if (playerY > 342 and playerY < 410 ) and (playerX <= 300 and playerX >= 210):
        if inAir:  # if change(falling)=0 then this tells us that player is no longer in air
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 342
        playerY_change = 0
    #   platform2
    if (playerY > 155 and playerY < 200) and (playerX <= 550 and playerX >= 400):
        if inAir:
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 155
        playerY_change = 0
    #platform5
    if (playerY > 342 and playerY < 352 ) and (playerX <= 800 and playerX >= 700):
        if inAir:  # if change(falling)=0 then this tells us that player is no longer in air
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 342
        playerY_change = 0
   
   # enemy collision
   #    when hit by the enemy
    if (playerY + 30 >= enemyY and playerY + 30 <= enemyY + 16) and (playerX + 38 >= enemyX and playerX <= enemyX + 15):
        falling_Sound()
        time.sleep(0.5)
        playerX = 0
        playerY = 0
        healthLimit += 1
    #   when player kills the enemy
    if (playerY + 30 < enemyY - 5 and playerY > enemyY - 60) and (playerX >= enemyX - 35 and playerX <= enemyX + 20):
        enemyDead_sound.play()
        enemyX = 1000
        enemyY = 1000
        score += 1
    


    # Border of left wall
    if playerX < 0:
        playerX = 0

     # respawn back
    if playerY > 650 :
        falling_Sound()
        time.sleep(1)   
        playerY_change = 0
        playerX = 0
        playerY = 0
        healthLimit += 1

    # Health limit
    if healthLimit == 1:
        health_3X = 1000
        health_3Y = 1000
    if healthLimit == 2:
        health_2X = 1000
        health_2Y = 1000
    if healthLimit == 3:
        health_1X = 1000
        health_1Y = 1000
        closing = True
        running = False
    
    # End Level
    #   y and x axis of where character reach the door and next level starts
    if (playerY < 380 and playerY > 340) and (playerX >= 740 and playerX <= 780) :
        time.sleep(0.5)
        break
    pygame.display.update() #update the display every time (pixel by pixel)

# Level two ends here ----------------------------------

#pause
time.sleep(0.5)

# Player
playerX = 0
playerY = 0

#enemy
enemyX = 250
enemyY = 420
enemyX_change = 1.5
enemyY_change = 0
enemy_state = "still"
EnemyY=420
EnemyX=495
EnemyX_change = 1.5

def Enemy(x, y) :
    screen.blit(enemyImg, (x, y))

# Game Loop 3 -----------------------------------------
while running:
    
    # Background image
    screen.blit(background, (0, 0))

    # health bar
    screen.blit(health1, (health_1X, health_1Y))
    screen.blit(health2, (health_2X, health_2Y))
    screen.blit(health3, (health_3X, health_3Y))

    # Platform
    screen.blit(platform3, (0, 450))
    screen.blit(platform3, (218, 450))
    screen.blit(platform3, (436,450))
    screen.blit(platform3, (654, 450))
    screen.blit(gate, (750,400))
    
    # Spikes
    screen.blit(spike, (180, 410))
    screen.blit(spike, (426, 410))
    screen.blit(spike, (634, 410))


    # Enemy1
    enemy(enemyX, enemyY)
    enemyX+= enemyX_change
    if enemyX >= 400 or enemyX <= 250:
        enemyX_change *= -1

    # Enemy 2
    Enemy(EnemyX, EnemyY)
    EnemyX += EnemyX_change
    if EnemyX >= 620 or EnemyX <= 495:
        EnemyX_change *= -1
    
    
    
    for event in pygame.event.get(): #any type of control happens in event
        if event.type == pygame.QUIT: # close button
            running = False
            
        # if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN: # keydown = pressing key
            if event.key == pygame.K_RIGHT:
                playerX_change += 7
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
            if event.key == pygame.K_SPACE:
                if player_state is "still":
                    jumping_sound.play()
                    for jump in range(15):
                            playerY_change -= playerY_gravity + 0.25 
                            playerY += playerY_change 
                            player(playerX, playerY)
                            playerY_gravity -= 0.03
                    playerY_gravity = 0.98
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
    
    
    # while falling
    #   checking whether person is in air so that when landing it wil play sound
    if playerY_change > 0 :#if there is a change(falling) in y axix then 
        inAir = True

    # movment of player
        # always put player img after screenfill because screen is drawn first
        #then character is draw on the screen not behind
    playerX += playerX_change
    # player is define before gravity to let its state be 'jump' in gravity  portion
    player(playerX, playerY)
    # gravity
    playerY_change += playerY_gravity
    playerY += playerY_change 
    
    # Platforms 
    #   platform3
        # height of PF(480-490)              final limit        intial limit
    if (playerY > 395 and playerY < 450) and (playerX <= 770 and playerX >= -10):
        if inAir:  # if change(falling)=0 then this tells us that player is no longer in air
            landing_Sound()
            inAir = False
        player_state = "still"
        playerY = 395
        playerY_change = 0
   
        # enemy1 collision
        #    when hit by the enemy
    if (playerY + 30 >= enemyY and playerY + 30 <= enemyY + 16) and (playerX + 38 >= enemyX and playerX <= enemyX + 15):
            falling_Sound()
            time.sleep(0.5)
            playerX = 0
            playerY = 0
            healthLimit += 1
        #   when player kills the enemy
    if (playerY + 30 < enemyY - 5 and playerY > enemyY - 60) and ( playerX >= enemyX - 35 and playerX <= enemyX + 20):
            enemyDead_sound.play()
            enemyX = 1000
            enemyY = 1000
            score += 1

        # Enemy2 collision
        # when hit by the enemy
    if (playerY + 30 >= EnemyY and playerY + 30 <= EnemyY + 16) and (playerX + 38 >= EnemyX and playerX <= EnemyX + 15):
            falling_Sound()
            time.sleep(0.5)
            playerX = 0
            playerY = 0
            healthLimit += 1
        #   when player kills the enemy
    if (playerY + 30 < EnemyY - 5 and playerY > EnemyY - 60) and ( playerX >= EnemyX - 35 and playerX <= EnemyX + 20):
            enemyDead_sound.play()
            EnemyX = 1000
            EnemyY = 1000
            score += 1
    
    # Spike1 collision
    if (playerY + 30 >= 410 and playerY + 30 <= 410 + 50) and (playerX + 38 >= 175 and playerX <= 175 + 60):
            falling_Sound()
            time.sleep(0.25)
            playerX = 0
            playerY = 0
            healthLimit += 1
            playerY_change = 0

    # Spike2 collision
    if (playerY + 30 >= 410 and playerY + 30 <= 410 + 50) and (playerX + 38 >= 420 and playerX <= 420 + 60):
        falling_Sound()
        time.sleep(0.25)
        playerX = 0
        playerY = 0
        healthLimit += 1
        playerY_change = 0

    # Spike3 collision
    if (playerY + 30 >= 410 and playerY + 30 <= 410 + 50) and (playerX + 38 >= 630 and playerX <= 630 + 60):
            falling_Sound()
            time.sleep(0.25)
            playerX = 0
            playerY = 0
            healthLimit += 1
            playerY_change = 0
    


    # Border of left wall
    if playerX < 0:
        playerX = 0

     # respawn back
    if playerY > 650 :
        falling_Sound()
        time.sleep(1)   
        playerY_change = 0
        playerX = 0
        playerY = 0
        healthLimit += 1

    # Health limit
    if healthLimit == 1:
        health_3X = 1000
        health_3Y = 1000
    if healthLimit == 2:
        health_2X = 1000
        health_2Y = 1000
    if healthLimit == 3:
        health_1X = 1000
        health_1Y = 1000
        closing = True
        running = False
    
    # End Level
    #   y and x axis of where character reach the door and next level starts
    if (playerY < 440 and playerY > 380) and (playerX >= 740 and playerX <= 780) :
        time.sleep(0.5)
        closing = True
        break
    pygame.display.update() #update the display every time (pixel by pixel)

# Level three ends here ----------------------------------

while closing:
    screen.fill((0, 0, 0))        
    if running:
        you_won(textX, textY)
    else:
        you_loose(textX, textY)
        
    for event in pygame.event.get(): #any type of control happens in event
        if event.type == pygame.QUIT: # close button
            closing = False
        
    pygame.display.update()