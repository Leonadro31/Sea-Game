import math, random, pygame


class Utils(object):
	def __init__(self):
		self.last_flash_tick = 0
		self.flash_image = pygame.transform.scale(pygame.image.load("textures/flash.png").convert(), (400, 200))


	def get_distance(p1, p2):
		return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)



	def clicked_on_object(object=None, mouse_pos=(0, 0)):
		if object.Rect.collidepoint(mouse_pos):
			return True
		return False

	def remove_black_background(object=None, iterable=None):
		if object == None:
			for object in iterable:
				if object.type == "Fish":
					for image in object.facing_down:
						image.set_colorkey((0, 0, 0))
					for image in object.facing_up:
						image.set_colorkey((0, 0, 0))
					for image in object.facing_right:
						image.set_colorkey((0, 0, 0))
					for image in object.facing_left:
						image.set_colorkey((0, 0, 0))
		else:
			if object.type == "Fish":
				for image in object.facing_down:
					image.set_colorkey((0, 0, 0))
				for image in object.facing_up:
					image.set_colorkey((0, 0, 0))
				for image in object.facing_right:
					image.set_colorkey((0, 0, 0))
				for image in object.facing_left:
					image.set_colorkey((0, 0, 0))