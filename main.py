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

def draw_board():
	num1 = ((Height - 50)//32)
	num2 = (Width // 30)
	for i in range(len(level)): #go through every single row in the board
		for j in range(len(level[i])): #we are going every since coulm in the board
			if level[i][j] == 1:
				pygame.draw.circle(screen, "white", (j * num2 + (0.5*num2), i * num1 + (num1*0.5)), 4)    #there are 4 arguments the first being the surface you want to add it to, the second is the color you want it to be, third the x and y postion of each square which for us us hte center of the tile, adn last is how big the radius u want it
			if level[i][j] == 2:
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




run = True
while run: #while the game is running whatever is inside this loop will happen
	timer.tick(fps)     #
	screen.fill('black')    #setting the background color to a black
	draw_board()


	for event in pygame.event.get():    #leave the while loop
		if event.type == pygame.QUIT:     #when the top red button on the top of the x is clicked it will leave the loop
			run = False     #set the run to false

	pygame.display.flip()
pygame.quit();