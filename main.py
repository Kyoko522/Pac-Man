import pygame
from board import boards
import math

pygame.init()

Width = 900  # the width of the game
Height = 950  # the height of the game
screen = pygame.display.set_mode([Width, Height])  # create the screen for the game
timer = pygame.time.Clock()  # set the game timer, how long the game has been running
fps = 60  # set a limit on the fps of the game
font = pygame.font.Font("freesansbold.ttf", 20)  # set the basic font-family and the text size
level = boards
color = "blue"
PI = math.pi
player_images = []
for i in range(1, 5):
	player_images.append(pygame.transform.scale(pygame.image.load(f'Pac-img/{i}.png'), (
	45, 45)))  # taking the images and making a list into the a 45 by 45 square
	red_ghost = pygame.transform.scale(pygame.image.load(f'Ghost/red.png'), (45, 45))
	pink_ghost = pygame.transform.scale(pygame.image.load(f'Ghost/pink.png'), (45, 45))
	blue_ghost = pygame.transform.scale(pygame.image.load(f'Ghost/blue.png'), (45, 45))
	orange_ghost = pygame.transform.scale(pygame.image.load(f'Ghost/orange.png'), (45, 45))
	poweredup_ghost = pygame.transform.scale(pygame.image.load(f'Ghost/powerup.png'), (45, 45))
	dead_ghost = pygame.transform.scale(pygame.image.load(f'Ghost/dead.png'), (45, 45))
player_x = 450
player_y = 663
red_ghost_x = 56
red_ghost_y = 58
red_ghost_direction = 0
pink_ghost_x = 440
pink_ghost_y = 438
pink_ghost_direction = 0
blue_ghost_x = 440
blue_ghost_y = 438
blue_ghost_direction = 0
orange_ghost_x = 440
orange_ghost_y = 438
orange_ghost_direction = 0
target = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
red_dead = False
pink_dead = False
blue_dead = False
orange_dead = False
red_box = False
pink_box = False
blue_box = False
orange_box = False
ghost_speed = 2
flicker = False
lives = 3


class Ghost:
	def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
		self.x_pos = x_coord
		self.y_pos = y_coord
		self.center_x = self.x_pos + 22
		self.center_y = self.y_pos + 22
		self.target = target
		self.speed = speed
		self.img = img
		self.direction = direct
		self.dead = dead
		self.in_box = box
		self.id = id
		self.turns, self.in_box = self.check_collisions()
		self.rect = self.draw()

	def draw(self):
		if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
			screen.blit(self.img, (self.x_pos, self.y_pos))
		elif powerup and not self.dead and not eaten_ghost[self.id]:
			screen.blit(poweredup_ghost, (self.x_pos, self.y_pos))
		else:
			screen.blit(dead_ghost, (self.x_pos, self.y_pos))
		ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
		return ghost_rect

	def check_collisions(self):
		# R, L, U, D
		num1 = ((Height - 50) // 32)
		num2 = (Width // 30)
		num3 = 15
		self.turns = [False, False, False, False]
		if 0 < self.center_x // 30 < 29:
			if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
				self.turns[2] = True
			if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
					or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
					self.in_box or self.dead)):
				self.turns[1] = True
			if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
					or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
					self.in_box or self.dead)):
				self.turns[0] = True
			if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
					or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
					self.in_box or self.dead)):
				self.turns[3] = True
			if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
					or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
					self.in_box or self.dead)):
				self.turns[2] = True

			if self.direction == 2 or self.direction == 3:
				if 12 <= self.center_x % num2 <= 18:
					if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
							or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[3] = True
					if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
							or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[2] = True
				if 12 <= self.center_y % num1 <= 18:
					if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
							or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[1] = True
					if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
							or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[0] = True

			if self.direction == 0 or self.direction == 1:
				if 12 <= self.center_x % num2 <= 18:
					if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
							or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[3] = True
					if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
							or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[2] = True
				if 12 <= self.center_y % num1 <= 18:
					if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
							or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[1] = True
					if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
							or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
							self.in_box or self.dead)):
						self.turns[0] = True
		else:
			self.turns[0] = True
			self.turns[1] = True
		if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
			self.in_box = True
		else:
			self.in_box = False
		return self.turns, self.in_box

	def move_clyde(self):
		# r, l, u, d
		# clyde is going to turn whenever advantageous for pursuit
		# going right
		if self.direction == 0:
			if self.target[0] > self.x_pos and self.turns[0]:   #the ghost is going right and the target is to the right and i can go to the right
				self.x_pos += self.speed    #the ghost will go to the right
			elif not self.turns[0]: #the ghost has hit something that isn't a empty spot and it can't go right anymore
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
			elif self.turns[0]: #the ghost can go right but the target is not on the right side
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				if self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				else:
					self.x_pos += self.speed

		# going left
		elif self.direction == 1:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.direction = 3
			elif self.target[0] < self.x_pos and self.turns[1]:
				self.x_pos -= self.speed
			elif not self.turns[1]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[1]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				if self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				else:
					self.x_pos -= self.speed

		# going down
		elif self.direction == 2:
			if self.target[0] < self.x_pos and self.turns[1]:
				self.direction = 1
				self.x_pos -= self.speed
			elif self.target[1] < self.y_pos and self.turns[2]:
				self.direction = 2
				self.y_pos -= self.speed
			elif not self.turns[2]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[2]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				else:
					self.y_pos -= self.speed

		#going up
		elif self.direction == 3:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.y_pos += self.speed
			elif not self.turns[3]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[3]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				else:
					self.y_pos += self.speed
		if self.x_pos < -30:
			self.x_pos = 900
		elif self.x_pos > 900:
			self.x_pos - 30
		return self.x_pos, self.y_pos, self.direction

	def move_blinky(self):
		# r, l, u, d
		# blinky is going to turn whenever colliding with walls, otherwise continue straight
		if self.direction == 0:
			if self.target[0] > self.x_pos and self.turns[0]:
				self.x_pos += self.speed
			elif not self.turns[0]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
			elif self.turns[0]:
				self.x_pos += self.speed
		elif self.direction == 1:
			if self.target[0] < self.x_pos and self.turns[1]:
				self.x_pos -= self.speed
			elif not self.turns[1]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[1]:
				self.x_pos -= self.speed
		elif self.direction == 2:
			if self.target[1] < self.y_pos and self.turns[2]:
				self.direction = 2
				self.y_pos -= self.speed
			elif not self.turns[2]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
			elif self.turns[2]:
				self.y_pos -= self.speed
		elif self.direction == 3:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.y_pos += self.speed
			elif not self.turns[3]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
			elif self.turns[3]:
				self.y_pos += self.speed
		if self.x_pos < -30:
			self.x_pos = 900
		elif self.x_pos > 900:
			self.x_pos - 30
		return self.x_pos, self.y_pos, self.direction

	def move_inky(self):
		# r, l, u, d
		# inky turns up or down at any point to pursue, but left and right only on collision
		if self.direction == 0:
			if self.target[0] > self.x_pos and self.turns[0]:
				self.x_pos += self.speed
			elif not self.turns[0]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
			elif self.turns[0]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				if self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				else:
					self.x_pos += self.speed
		elif self.direction == 1:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.direction = 3
			elif self.target[0] < self.x_pos and self.turns[1]:
				self.x_pos -= self.speed
			elif not self.turns[1]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[1]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				if self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				else:
					self.x_pos -= self.speed
		elif self.direction == 2:
			if self.target[1] < self.y_pos and self.turns[2]:
				self.direction = 2
				self.y_pos -= self.speed
			elif not self.turns[2]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[2]:
				self.y_pos -= self.speed
		elif self.direction == 3:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.y_pos += self.speed
			elif not self.turns[3]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[3]:
				self.y_pos += self.speed
		if self.x_pos < -30:
			self.x_pos = 900
		elif self.x_pos > 900:
			self.x_pos - 30
		return self.x_pos, self.y_pos, self.direction

	def move_pinky(self):
		# r, l, u, d
		# inky is going to turn left or right whenever advantageous, but only up or down on collision
		if self.direction == 0:
			if self.target[0] > self.x_pos and self.turns[0]:
				self.x_pos += self.speed
			elif not self.turns[0]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
			elif self.turns[0]:
				self.x_pos += self.speed
		elif self.direction == 1:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.direction = 3
			elif self.target[0] < self.x_pos and self.turns[1]:
				self.x_pos -= self.speed
			elif not self.turns[1]:
				if self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[1]:
				self.x_pos -= self.speed
		elif self.direction == 2:
			if self.target[0] < self.x_pos and self.turns[1]:
				self.direction = 1
				self.x_pos -= self.speed
			elif self.target[1] < self.y_pos and self.turns[2]:
				self.direction = 2
				self.y_pos -= self.speed
			elif not self.turns[2]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] > self.y_pos and self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[3]:
					self.direction = 3
					self.y_pos += self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[2]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				else:
					self.y_pos -= self.speed
		elif self.direction == 3:
			if self.target[1] > self.y_pos and self.turns[3]:
				self.y_pos += self.speed
			elif not self.turns[3]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.target[1] < self.y_pos and self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[2]:
					self.direction = 2
					self.y_pos -= self.speed
				elif self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				elif self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
			elif self.turns[3]:
				if self.target[0] > self.x_pos and self.turns[0]:
					self.direction = 0
					self.x_pos += self.speed
				elif self.target[0] < self.x_pos and self.turns[1]:
					self.direction = 1
					self.x_pos -= self.speed
				else:
					self.y_pos += self.speed
		if self.x_pos < -30:
			self.x_pos = 900
		elif self.x_pos > 900:
			self.x_pos - 30
		return self.x_pos, self.y_pos, self.direction

def draw_misc():
	score_text = font.render(f'Score: {score}', True, color)
	screen.blit(score_text, (10, 920))
	if powerup:
		pygame.draw.circle(screen, "blue", (140, 930), 15)

	for i in range(lives):
		screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))


def draw_board():
	num1 = ((Height - 50) // 32)
	num2 = (Width // 30)
	for i in range(len(level)):  # go through every single row in the board
		for j in range(len(level[i])):  # we are going every since coulm in the board
			if level[i][j] == 1:
				pygame.draw.circle(screen, "white", (j * num2 + (0.5 * num2), i * num1 + (num1 * 0.5)),
				                   4)  # there are 4 arguments the first being the surface you want to add it to, the second is the color you want it to be, third the x and y postion of each square which for us us hte center of the tile, adn last is how big the radius u want it
			if level[i][j] == 2 and not flicker:
				pygame.draw.circle(screen, "white", (j * num2 + (0.5 * num2), i * num1 + (num1 * 0.5)),
				                   10)  # the same as the one before it but this time it just bigger as we just want the power up to be bigger
			if level[i][j] == 3:
				pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
				                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
			if level[i][j] == 4:
				pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
				                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
			if level[i][j] == 4:
				pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
				                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
			if level[i][j] == 5:
				pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2,
				                                (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
			if level[i][j] == 6:
				pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)),
				                                (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
			if level[i][j] == 7:
				pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)),
				                                (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
			if level[i][j] == 8:
				pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2,
				                                (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, PI * 2, 3)
			if level[i][j] == 9:
				pygame.draw.line(screen, "white", (j * num2, i * num1 + (0.5 * num1)),
				                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


direction = 0
counter = 0


def draw_player():
	# Right
	if direction == 0:
		screen.blit(player_images[counter // 5], (player_x, player_y))
	# left
	elif direction == 1:
		screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
	# up
	elif direction == 2:
		screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
	# down
	elif direction == 3:
		screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


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


player_speed = 3


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


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

score = 0
power_count = 0
powerup = False
eaten_ghost = [False, False, False, False]
moving = False
startup_counter = 0


def check_collisions(scor, power_counter, power, eaten_ghosts):
	num1 = (Height - 50) // 32
	num2 = Width // 30
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

while run:  # while the game is running whatever is inside this loop will happen
	timer.tick(fps)  #
	if counter < 19:  # controls the counter variable and reset the animation every 19 times
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

	screen.fill('black')  # setting the background color to a black
	draw_board()
	draw_player()
	blinky = Ghost(red_ghost_x, red_ghost_y, target[0], ghost_speed, red_ghost, red_ghost_direction, red_dead, red_box,
	               0)
	inky = Ghost(pink_ghost_x, pink_ghost_y, target[1], ghost_speed, pink_ghost, pink_ghost_direction, pink_dead,
	             pink_box, 1)
	pinky = Ghost(blue_ghost_x, blue_ghost_y, target[2], ghost_speed, blue_ghost, blue_ghost_direction, blue_dead,
	              blue_box, 2)
	clyde = Ghost(orange_ghost_x, orange_ghost_y, target[3], ghost_speed, orange_ghost, orange_ghost_direction,
	              orange_dead, orange_box, 3)
	draw_misc()
	target = get_targets(red_ghost_x, red_ghost_y, pink_ghost_x, pink_ghost_y, blue_ghost_x, blue_ghost_y, orange_ghost_x, orange_ghost_y)
	center_x = player_x + 23
	center_y = player_y + 24
	turn_allowed = check_pos(center_x, center_y)
	if moving:
		player_x, player_y = move_player(player_x, player_y)
		red_ghost_x, red_ghost_y, red_ghost_direction = blinky.move_blinky()
		pink_ghost_x, pink_ghost_y, pick_ghost_direction = inky.move_inky()
		blue_ghost_x, blue_ghost_y, blue_ghost_direction = pinky.move_pinky()
		orange_ghost_x, orange_ghost_y, orange_ghost_direction = clyde.move_clyde()
	score, power_count, powerup, eaten_ghost = check_collisions(score, power_count, powerup, eaten_ghost)

	for event in pygame.event.get():  # leave the while loop
		if event.type == pygame.QUIT:  # when the top red button on the top of the x is clicked it will leave the loop
			run = False  # set the run to false
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
