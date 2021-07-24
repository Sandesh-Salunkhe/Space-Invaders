import pygame
import os
import math
#for enemy position to appear at random places
import random
#for music and sound
from pygame import mixer
#Initislize pygame
pygame.init()

#create a window
screen = pygame.display.set_mode((800,600))

#background
#background = pygame.image.load(os.path.join('D:\pyGamesByK', 'background.jpg'))
#bgm
#mixer.music.load('background.wav')
#mixer.music.play(-1)
#Title 
pygame.display.set_caption("Space Invader")

#player
playerImg = pygame.image.load(os.path.join('D:\Coding', 'spaceship.png'))
playerX = 350
playerY = 480
playerX_change = 0
def player(x,y):
	screen.blit(playerImg, (x, y))


#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load(os.path.join('D:\Coding', 'alien.png')))
	enemyX.append(random.randint(0, 736))
	enemyY.append(random.randint(50, 150))
	enemyX_change.append(0.3)
	enemyY_change.append(40)
def enemy(x,y,i):
		screen.blit(enemyImg[i], (x, y))


#bullet
#ready state means you cant see the bullet
#fire state means the bullet is moving

bulletImg = pygame.image.load(os.path.join('D:\Coding', 'bullet.png'))
bulletX = 0
#Bullet must be fired from spaceship  & spaceship is at 480 x-coordinate
bulletY = 480
bulletX_change = 0
#speed of bullet
bulletY_change = 0.5
bullet_state = "ready"

#Sore
score_value = 0
font = pygame.font.Font('freesansbold.ttf',16)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
	score = font.render("score: " + str(score_value),True,(255,255,255))
	screen.blit(score, (x,y))

def game_over_text():
	over_text = over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(over_text, (250,250))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
	if distance < 27:
		return True
	else:
		return False


# Game is running always...window will not close automatically
running=True
while running:
	screen.fill((0,0,0))

	#background apply
	#screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:#to check if close is clicked
			running = False

		#If keystroke is pressed checked whether is right or left
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change -= 0.3
			if event.key == pygame.K_RIGHT:
				playerX_change += 0.3
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					#bullet_sound = mixer.sound('laser.wav')
					#bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX,bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
		

	#Checking for boundaries for spaceship so it deosn't goes out of window
	playerX = playerX + playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736

	#Enemy movement
	for i in range(num_of_enemies):

		#Game over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i]

		if enemyX[i] <= 0:
			enemyX_change[i] = 0.3
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -0.3
			enemyY[i] += enemyY_change[i]
		#collision
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			#collision_sound = mixer.sound('explosion.wav')
			#collision_sound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemyX[i]= random.randint(0, 736)
			enemyY[i]= random.randint(50, 150)

		enemy(enemyX[i],enemyY[i],i)		
	#Bullet Movement
	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change

	

	player(playerX,playerY)
	show_score(textX,textY)
	pygame.display.update()

