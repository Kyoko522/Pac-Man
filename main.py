import pygame
from board import boards
import math
pygame.init()

Width = 900     #the width of the game
Height = 950    #the height of the game
screen = pygame.display.set_mode([Width, Height])   #create the screen for the game
timer = pygame.time.Clock()     #set the game timer, how long the game has been running
fps = 60     #set a limit on the fps of the game
font = pygame.font.Font("freesansbold.ttf",20)      #set the basic font-family and the text size
level = boards
color = "purple"
PI = math.pi
player_images = []
for i in range(1,5):
	player_images.append(pygame.transform.scale(pygame.image.load(f'Pac-img/{i}.png'), (45, 45)))       #taking the images and making a list into the a 45 by 45 square
player_x = 450
player_y = 663
flicker = False
lives = 3

def draw_misc():
	score_text = font.render(f'Score: {score}', True, color)
	screen.blit(score_text, (10, 920))
	if powerup:
		pygame.draw.circle(screen, "blue", (140, 930), 15)

	for i in range(lives):
		screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

def draw_board():
	num1 = ((Height - 50)//32)
	num2 = (Width // 30)
	for i in range(len(level)): #go through every single row in the board
		for j in range(len(level[i])): #we are going every since coulm in the board
			if level[i][j] == 1:
				pygame.draw.circle(screen, "white", (j * num2 + (0.5*num2), i * num1 + (num1*0.5)), 4)    #there are 4 arguments the first being the surface you want to add it to, the second is the color you want it to be, third the x and y postion of each square which for us us hte center of the tile, adn last is how big the radius u want it
			if level[i][j] == 2 and not flicker:
				pygame.draw.circle(screen, "white", (j * num2 + (0.5*num2), i * num1 + (num1*0.5)), 10)     #the same as the one before it but this time it just bigger as we just want the power up to be bigger
			if level[i][j] == 3:
				pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i*num1),
				                 (j*num2 + (0.5 * num2), i*num1+num1), 3)
			if level[i][j] == 4:
				pygame.draw.line(screen, color, (j * num2, i*num1 + (0.5*num1)),
				                 (j * num2 + num2, i*num1 + (0.5 * num1)), 3)
			if level[i][j] == 4:
				pygame.draw.line(screen, color, (j * num2, i*num1 + (0.5*num1)),
				                 (j * num2 + num2, i*num1 + (0.5 * num1)), 3)
			if level[i][j] == 5:
				pygame.draw.arc(screen, color, [(j*num2 - (num2*0.4)) - 2,
				                                (i * num1 + (0.5*num1)), num2, num1],0, PI/2,3)
			if level[i][j] == 6:
				pygame.draw.arc(screen, color, [(j*num2 + (num2*0.5)),
				                                (i * num1 + (0.5*num1)), num2, num1], PI/2, PI,3)
			if level[i][j] == 7:
				pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)),
				                                (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI/2, 3)
			if level[i][j] == 8:
				pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2,
				                                (i * num1 - (0.4 * num1)), num2, num1], 3*PI/2, PI * 2, 3)
			if level[i][j] == 9:
				pygame.draw.line(screen, "white", (j * num2, i*num1 + (0.5*num1)),
				                 (j * num2 + num2, i*num1 + (0.5 * num1)), 3)

direction = 0
counter = 0
def draw_player():
	# Right
	if direction == 0:
		screen.blit(player_images[counter// 5], (player_x,player_y))
	# left
	elif direction == 1:
		screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
	# up
	elif direction == 2:
		screen.blit(pygame.transform.rotate(player_images[counter// 5],90), (player_x,player_y))
	# down
	elif direction == 3:
		screen.blit(pygame.transform.rotate(player_images[counter// 5],270), (player_x,player_y))

turn_allowed = False
direction_command = 0
def check_pos(x, y):
	turns = [False, False, False, False]
	num1 = (Height - 50) // 32
	num2 = (Width // 30)
	num3 = 15
	# check collisions based on center x and center y of player +/- fudge number
	if x // 30 < 29:
		if direction == 0:
			if level[y // num1][(x - num3) // num2] < 3:
				turns[1] = True
		if direction == 1:
			if level[y // num1][(x + num3) // num2] < 3:
				turns[0] = True
		if direction == 2:
			if level[(y + num3) // num1][x // num2] < 3:
				turns[3] = True
		if direction == 3:
			if level[(y - num3) // num1][x // num2] < 3:
				turns[2] = True

		if direction == 2 or direction == 3:
			if 12 <= x % num2 <= 18:
				if level[(y + num3) // num1][x // num2] < 3:
					turns[3] = True
				if level[(y - num3) // num1][x // num2] < 3:
					turns[2] = True
			if 12 <= y % num1 <= 18:
				if level[y // num1][(x - num2) // num2] < 3:
					turns[1] = True
				if level[y // num1][(x + num2) // num2] < 3:
					turns[0] = True
		if direction == 0 or direction == 1:
			if 12 <= x % num2 <= 18:
				if level[(y + num1) // num1][x // num2] < 3:
					turns[3] = True
				if level[(y - num1) // num1][x // num2] < 3:
					turns[2] = True
			if 12 <= y % num1 <= 18:
				if level[y // num1][(x - num3) // num2] < 3:
					turns[1] = True
				if level[y // num1][(x + num3) // num2] < 3:
					turns[0] = True
	else:
		turns[0] = True
		turns[1] = True

	return turns

player_speed = 2
def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turn_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turn_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turn_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turn_allowed[3]:
        play_y += player_speed
    return play_x, play_y

score = 0
power_count= 0
powerup = False
eaten_ghost = [False, False, False, False]
moving = False
startup_counter = 0

def check_collisions(scor, power_counter, power, eaten_ghosts):
	num1 = (Height - 50) // 32
	num2 = Width//30
	if 0 < player_x < 870:
		if level[center_y // num1][center_x // num2] == 1:
			level[center_y // num1][center_x // num2] = 0
			scor += 10
		if level[center_y // num1][center_x // num2] == 2:
			level[center_y // num1][center_x // num2] = 0
			scor += 50
			power = True
			power_counter = 0
			eaten_ghosts = [False, False, False, False]

	return scor, power_counter, power, eaten_ghosts

run = True
while run: #while the game is running whatever is inside this loop will happen
	timer.tick(fps)     #
	if counter < 19:   #controls the counter variable and reset the animation every 19 times
		counter += 1
		if counter > 5:
			flicker = False
	else:
		counter = 0
		flicker = True

	if powerup and power_count < 600:
		power_count += 1
	elif powerup and power_count >= 600:
		powerup = False
		power_count = 0
		eaten_ghost = [False, False, False, False]
	if startup_counter < 120:
		moving = False
		startup_counter += 1
	else:
		moving = True

	screen.fill('black')    #setting the background color to a black
	draw_board()
	draw_player()
	draw_misc()
	center_x = player_x + 23
	center_y = player_y + 24
	turn_allowed = check_pos(center_x, center_y)
	if moving:
		player_x, player_y = move_player(player_x, player_y)
	score, power_count, powerup, eaten_ghost = check_collisions(score, power_count, powerup, eaten_ghost)

	for event in pygame.event.get():    #leave the while loop
		if event.type == pygame.QUIT:     #when the top red button on the top of the x is clicked it will leave the loop
			run = False     #set the run to false
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				direction_command = 0
			if event.key == pygame.K_LEFT:
				direction_command = 1
			if event.key == pygame.K_UP:
				direction_command = 2
			if event.key == pygame.K_DOWN:
				direction_command = 3

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT and direction_command == 0:
				direction_command = direction
			if event.key == pygame.K_LEFT and direction_command == 1:
				direction_command = direction
			if event.key == pygame.K_UP and direction_command == 2:
				direction_command = direction
			if event.key == pygame.K_DOWN and direction_command == 3:
				direction_command = direction

	for i in range(4):
		if direction_command == i and turn_allowed[i]:
			direction = i

	if player_x > 900:
		player_x = -47
	elif player_y < -50:
		player_x = 897



	pygame.display.flip()
pygame.quit();