import pygame, math, random
from constants import *
from utils import Utils
pygame.init()

class GreenFish(object):
	def __init__(self, x=100, y=100, level=1):
		#id 
		self.type = "Fish"
		self.habitat = "sand"
		
		#stats
		self.level = level
		self.max_health = green_fish_health[str(self.level)]
		self.exp_on_death = green_fish_exp[str(self.level)]
		self.health = self.max_health
		self.power = green_fish_power[str(self.level)]
		self.focus_range = random.randint(100, 250)
		self.height = self.width = green_fish_sizes[str(self.level)]





		#blood
		self.blood_image = [pygame.image.load(f"textures/blood_{i+1}.png") for i in range(3)]
		self.blood_patches = []

		#images and animation
		self.facing_down = [pygame.transform.scale(pygame.image.load(f"C:/Users/Leonardo/Desktop/SeaHunters/Fishes/fish_{i}.png").convert(), (self.width, self.height)) for i in range(4, 7)]
		self.facing_up = [pygame.transform.scale(pygame.image.load(f"C:/Users/Leonardo/Desktop/SeaHunters/Fishes/fish_{i}.png").convert(), (self.width, self.height)) for i in range(40, 43)]
		self.facing_right = [pygame.transform.scale(pygame.image.load(f"C:/Users/Leonardo/Desktop/SeaHunters/Fishes/fish_{i}.png").convert(), (self.width, self.height)) for i in range(28, 31)]
		self.facing_left = [pygame.transform.scale(pygame.image.load(f"C:/Users/Leonardo/Desktop/SeaHunters/Fishes/fish_{i}.png").convert(), (self.width, self.height)) for i in range(16, 20)]
		self.animation_phase = 0
		self.count_to_delete = 30

		#movement
		self.x, self.y = x, y
		self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.direction = "RIGHT"
		self.focused_speed = 0
		self.speed = 0.5

		#player
		self.player_x = 0
		self.player_y = 0
		self.angle = 0

		#tick related
		self.tick = 21
		self.attack_tick = 0
		self.direction_count = 0

	
	def find_attack_path(self):
		m = (self.y - self.player_y)/(self.x - self.player_x)
		self.angle = (math.atan(m) *180 / 3.14)*-1

		speed_y = abs(math.sin(self.angle)*self.focused_speed)
		speed_x = abs(math.cos(self.angle)*self.focused_speed)
		if 33 <= abs(self.angle) <= 45:
			speed_x = speed_y = self.focused_speed/2
		if self.y > self.player_y:
			if self.y > 20:
				self.y -= speed_y
		else:
			if self.y < 780:
				self.y += speed_y

		if self.x > self.player_x:
			self.direction = "LEFT"
			if self.x > 20:
				self.x -= speed_x
		else:
			self.direction = "RIGHT"
			if self.x < 980:
				self.x += speed_x

		if 85 <= abs(self.angle) <= 95:
			if self.y > self.player_y:
				self.direction = "UP"
			else:
				self.direction = "DOWN"


	def attack(self, player):
		if (self.tick - player.damage_tick > 15):
			if self.x > self.player_x:
				self.x -= 15
			else:
				self.x += 15
			if self.y > self.player_y:
				self.y -= 15
			else:
				self.y += 15
			self.blood_patches.append({"x":self.x, "y":self.y, "patch_image":self.blood_image[random.randint(0, 2)], "tick":self.tick})
			self.attack_tick = self.tick
			player.damage_tick = self.tick
			player.health -= self.power

	def move(self, player):
		self.player_x = player.x
		self.player_y = player.y
		self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
		distance_from_player = Utils.get_distance((self.x, self.y), (player.x, player.y))
		if self.level > player.level:
			if distance_from_player < self.focus_range and self.tick - self.attack_tick > 30:
				self.focused_speed = 2.5
				self.find_attack_path()
				if self.Rect.colliderect(player.Rect):
					self.attack(player)

			elif self.tick - self.attack_tick < 30:
				self.angle = 0
				match self.direction:
					case "RIGHT":
						if self.x < 980:
							self.x += self.focused_speed
					case "LEFT":
						if self.x > 20:
							self.x -= self.focused_speed
					case "UP":
						if self.y > 20:
							self.y -= self.focused_speed
					case "DOWN":
						if self.y < 780:
							self.y += self.focused_speed
			else:
				self.angle = 0
				self.direction_count += 1
				if self.direction_count < 300:
					self.direction = "LEFT"
				elif self.direction_count < 600:
					self.direction = "RIGHT"
				else:
					self.direction_count = 0

				match self.direction:
					case "RIGHT":
						if self.x < 980:
							self.x += self.speed
					case "LEFT":
						if self.x > 20:
							self.x -= self.speed

		else:
			self.direction_count += 1
			if self.direction_count < 300:
				self.direction = "LEFT"
			elif self.direction_count < 600:
				self.direction = "RIGHT"
			else:
				self.direction_count = 0

			match self.direction:
				case "RIGHT":
					self.x += self.speed
				case "LEFT":
					self.x -= self.speed


	def draw(self, surface):
		self.tick += 1
		if self.animation_phase + 1 >= 54:
			self.animation_phase = 0
		else:
			self.animation_phase += 1



		bar_background_color = (138, 149, 156)
		health_bar_color = (120, 2, 2)
		pygame.draw.rect(surface, bar_background_color, (self.x, self.y - 10, self.width, 5))
		pygame.draw.rect(surface, health_bar_color, (self.x, self.y - 10, (self.health*self.width/self.max_health),5))
		for patch in self.blood_patches[:]:
			if self.tick - patch["tick"] <= 30:
				win.blit(patch["patch_image"], (patch["x"], patch["y"]))
			else:
				self.blood_patches.remove(patch)

		match self.direction:
			case "RIGHT":
				surface.blit(pygame.transform.rotate(self.facing_right[int(self.animation_phase/18)], self.angle), (self.x, self.y))
			case "LEFT":
				surface.blit(pygame.transform.rotate(self.facing_left[int(self.animation_phase/18)], self.angle), (self.x, self.y))
			case "UP":
				surface.blit(self.facing_up[int(self.animation_phase/18)], (self.x, self.y))
			case "DOWN":
				surface.blit(self.facing_down[int(self.animation_phase/18)], (self.x, self.y))
			