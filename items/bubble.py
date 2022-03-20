import pygame
import math
import random

class Bubble(object):
	def __init__(self, x, y, speed, size):
		self.size = size
		self.image = pygame.transform.scale(pygame.image.load("textures/bubble.png").convert(), (self.size, self.size))
		self.dark_image = pygame.transform.scale(pygame.image.load("textures/dark_bubble.png").convert(), (self.size, self.size))
		self.pop_image = pygame.transform.scale(pygame.image.load("textures/bubble_pop.png").convert(), (self.size+4, self.size+4))
		self.dark_pop_image = pygame.transform.scale(pygame.image.load("textures/dark_bubble_pop.png").convert(), (self.size+4, self.size+4))
		self.x, self.y = x, y
		self.popped = False
		self.speed = speed
		self.Rect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.to_delete = False
		self.count_since_pop = 0

	def move_bubble(self):
		if self.y == 0:
			self.to_delete = True
		else:
			self.y -= self.speed
		self.x += math.sin(0.06*self.y)
		self.Rect = pygame.Rect(self.x, self.y, self.size, self.size)

	def draw_bubble(self,surface, level):
		if self.popped and self.count_since_pop < 15:
			self.count_since_pop += 1
		if self.count_since_pop == 0:
			self.move_bubble()
			match level:
				case "sand":
					surface.blit(self.image, (self.x, self.y))
				case "deep":
					surface.blit(self.dark_image, (self.x, self.y))
		else:
			match level:
				case "sand":
					surface.blit(self.pop_image, (self.x, self.y))
				case "deep":
					surface.blit(self.dark_pop_image, (self.x, self.y))

		if self.count_since_pop == 5:
			self.to_delete = True