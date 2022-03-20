import pygame, math, random
from constants import *
pygame.init()

class Player(object):
	def __init__(self, x=100, y=100):
		#stats
		self.level = 1
		self.height = self.width = size_for_level[str(self.level)]
		self.experience = 0
		self.experience_to_lvl_up = exp_for_level[str(self.level)]
		self.speed = 3
		self.health = 70
		self.max_health = health_for_level[str(self.level)]
		self.power = power_for_level[str(self.level)]

		#images and animation
		self.paper_image = pygame.image.load("textures/paper.png").convert()
		self.facing_down = [pygame.transform.scale(pygame.image.load(f"textures/blue_fish_down_{i+1}.png").convert(), (50, 50)) for i in range(3)]
		self.facing_up = [pygame.transform.scale(pygame.image.load(f"textures/blue_fish_up_{i+1}.png").convert(), (50, 50)) for i in range(3)]
		self.facing_right = [pygame.transform.scale(pygame.image.load(f"textures/blue_fish_right_{i+1}.png").convert(), (50, 50)) for i in range(3)]
		self.facing_left = [pygame.transform.scale(pygame.image.load(f"textures/blue_fish_left_{i+1}.png").convert(), (50, 50)) for i in range(3)]
		self.animation_phase = 0
		
		
		#stats text
		self.font = pygame.font.SysFont("Helvetica", 10)
		self.health_text = self.font.render("Health:", False, (0, 0, 0))
		self.power_text = self.font.render("Power:",  False, (0, 0, 0))
		self.level_text = self.font.render(f"Level {self.level}: ", False, (0, 0, 0))
		self.sprint_text = self.font.render("Sprint:", False, (0, 0, 0))

		#movement
		self.direction = "RIGHT"
		self.x, self.y = x, y
		self.sprint_count = 10
		self.sprinting = False
		self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.angular_speed = math.sqrt(self.speed/2)
		self.is_moving = False

		#tick related
		self.damage_tick = 0
		self.attack_range = 60
		self.attack_tick = 0
		self.tick = 0

	

	def move(self):
		if not self.sprinting:
			self.angular_speed = math.sqrt(self.speed)/2 + 0.8
		else:
			self.angular_speed = 6
		match self.direction:
			case "UP":
				self.y -= self.speed
			case "DOWN":
				self.y += self.speed
			case "RIGHT":
				self.x += self.speed
			case "LEFT":
				self.x -= self.speed
			case "LEFT UP":
				self.y -= self.angular_speed
				self.x -= self.angular_speed
			case "LEFT DOWN":
				self.y += self.angular_speed
				self.x -= self.angular_speed
			case "RIGHT UP":
				self.y -= self.angular_speed
				self.x += self.angular_speed
			case "RIGHT DOWN":
				self.y += self.angular_speed
				self.x += self.angular_speed
			
		self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)			

	def draw(self, surface):
		self.tick += 1
		if self.animation_phase + 1 >= 54:
			self.animation_phase = 0
		else:
			self.animation_phase += 1
		
		match self.direction:
			case "RIGHT":
				surface.blit(self.facing_right[int(self.animation_phase/18)], (self.x, self.y))
			case "LEFT":
				surface.blit(self.facing_left[int(self.animation_phase/18)], (self.x, self.y))
			case "UP":
				surface.blit(self.facing_up[int(self.animation_phase/18)], (self.x, self.y))
			case "DOWN":
				surface.blit(self.facing_down[int(self.animation_phase/18)], (self.x, self.y))
			case "RIGHT UP":
				surface.blit(pygame.transform.rotate(self.facing_right[int(self.animation_phase/18)], 45), (self.x, self.y))
			case "RIGHT DOWN":
				surface.blit(pygame.transform.rotate(self.facing_right[int(self.animation_phase/18)], -45), (self.x, self.y))
			case "LEFT UP":
				surface.blit(pygame.transform.rotate(self.facing_left[int(self.animation_phase/18)], -45), (self.x, self.y))
			case "LEFT DOWN":
				surface.blit(pygame.transform.rotate(self.facing_left[int(self.animation_phase/18)], 45), (self.x, self.y))

	def attack(self, target):
		if self.tick - self.attack_tick > 30:
			if self.x > target.Rect[0]:
				self.x -= 15
			else:
				self.x += 15
			if self.y > target.Rect[1]:
				self.y -= 15
			else:
				self.y += 15
			self.attack_tick = self.tick
			target.health -= self.power

			if target.health <= 0:
				self.experience += target.exp_on_death
		
	def exp_manager(self):
		if self.experience >= self.experience_to_lvl_up:
			self.level += 1
			self.max_health = health_for_level[str(self.level)]
			self.power = power_for_level[str(self.level)]
			self.experience_to_lvl_up = exp_for_level[str(self.level)]
			self.height = self.width = size_for_level[str(self.level)]


	def draw_stats(self, surface):
		self.exp_manager()

		bar_background_color = (138, 149, 156)
		health_bar_color = (120, 2, 2)
		level_color = (10, 125, 37)
		sprint_color = (43, 53, 166)
		container_color = (222, 218, 206)
		power_color = (232, 135, 0)
		surface.blit(self.paper_image, (780, -10))
		surface.blit(self.font.render("Health:", False, (0, 0, 0)), (805, 10))
		surface.blit(self.font.render(f"Level {self.level}: ", False, (0, 0, 0)), (805, 50))
		surface.blit(self.font.render("Sprint:", False, (0, 0, 0)), (805, 70))
		surface.blit(self.font.render("Power:",  False, (0, 0, 0)), (805, 30))
		pygame.draw.rect(surface, bar_background_color, (850, 15, 140, 5))
		pygame.draw.rect(surface, bar_background_color, (850, 35, 140, 5))
		pygame.draw.rect(surface, bar_background_color, (850, 55, 140, 5))
		pygame.draw.rect(surface, bar_background_color, (850, 75, 140, 5))
		pygame.draw.rect(surface, health_bar_color, (850, 15, (self.health*140/self.max_health),5))
		pygame.draw.rect(surface, level_color, (850, 55, (self.experience*140/self.experience_to_lvl_up),5))
		pygame.draw.rect(surface, sprint_color, (850, 75, (self.sprint_count*140/10),5))
		pygame.draw.rect(surface, power_color, (850, 35, (self.power*140/200),5))