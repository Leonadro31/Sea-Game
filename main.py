import pygame, time, random, math
from items.bubble import Bubble
from entities.player import Player
from entities.green_fish import GreenFish
from utils import Utils
from constants import *

running = True

level = "sand"
bg_x = 0
flash_tick = 0
player = Player(x=600)



bubbles = []
fishes = []
def create_objects():
	global bubbles, fishes
	for i in range(40):
		bubbles.append(Bubble(x=random.randint(50, 1950), y=random.randint(800, 2000), speed=random.randint(1, 3), size=random.randint(5, 16)))
	for i in range(10):
		fishes.append(GreenFish(x=random.randint(50, 1950), y=random.randint(100, 700), level=random.randint(player.level, player.level+2)))
	Utils.remove_black_background(iterable=fishes)

def move_background(delta_x, delta_y):
	global bg_x
	bg_x += delta_x
	for bubble in bubbles:
		bubble.x += delta_x
	for fish in fishes:
		if len(fish.blood_patches) > 0:
			for patch in fish.blood_patches:
				patch["x"] += delta_x
		fish.x += delta_x


def game_over_screen():
	global running
	clock.tick(frame_rate)
	match level:
		case "sand":
			win.blit(background_image["sand"], (bg_x, 0))
		case "deep":
			win.blit(background_image["deep"], (bg_x, 0))	
	
	win.blit(game_over_text, (screen_width/2 - game_over_text_size[0]/2, screen_height/2 - game_over_text_size[1]/2))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			player.health = 1
			running = False
			return None
	pygame.display.update()

create_objects()



tick = 0
while running:
	tick += 1
	clock.tick(frame_rate)
	
	while (player.health <= 0):
		game_over_screen()

	player.is_moving = False
	match level:
		case "sand":
			win.blit(background_image["sand"], (bg_x, 0))
		case "deep":
			win.blit(background_image["deep"], (bg_x, 0))			

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONUP:
			x, y = pygame.mouse.get_pos()

			for fish in fishes:
				if Utils.clicked_on_object(fish, (x, y)):
					if Utils.get_distance(fish.Rect, player.Rect) < player.attack_range:
						player.attack(fish)

			if level == "sand":
				if 763 <= y <= 790 and 1550 <=x + abs(bg_x) <= 1600: #goes to "sand" level and cleares all the fish that arent in the right habitat
					if Utils.get_distance((player.x, player.y), (x, y)) < 100:
						level = "deep"
						for fish in fishes[:]:
							if level not in fish.habitat:
								fishes.remove(fish)
								del fish
						player.y = 534
					else:
						flash_tick = tick
			elif level == "deep":
				if 600 <= y <= 635 and 1580 <= x + abs(bg_x) <= 1630:  #goes to "deep" level and cleares all the fish that arent in the right habitat
					if Utils.get_distance((player.x, player.y), (x, y)) < 100:
						level = "sand"
						for i in range(10):
							fishes.append(GreenFish(x=random.randint(50, 1950), y=random.randint(100, 800), level=random.randint(player.level, player.level)))
						Utils.remove_black_background(fishes)
						player.y = 740
					else:
						flash_tick = tick

	#player movement
	key = pygame.key.get_pressed()
	if key[pygame.K_w] and not key[pygame.K_a] and not key[pygame.K_d]:
		if player.y > 100:
			player.direction = "UP"
			player.is_moving = True
			player.move()
	if key[pygame.K_s] and not key[pygame.K_a] and not key[pygame.K_d]:
		if player.y < 700 - (player.speed + 1):
			player.direction = "DOWN"
			player.is_moving = True
			player.move()
	if key[pygame.K_a]:
		if key[pygame.K_w]:
			player.direction = "LEFT UP"
			if player.x > 200:
				if player.y > 50 + player.width + player.speed + 1:
					player.is_moving = True
					player.move()
			elif bg_x < 0 - player.speed - 1:
				player.is_moving = True
				move_background(+player.speed, 0)
				if player.y > 50:
					player.y -= player.angular_speed
			else:
				if player.x > 50 + (player.speed + 1 + player.width):
					player.is_moving = True
					player.x -= player.angular_speed
				if player.y > 50 + player.speed + 1:
					player.is_moving = True
					player.y -= player.angular_speed
		elif key[pygame.K_s]:
			player.direction = "LEFT DOWN"
			if player.x > 200:
				if player.y < 700 - (player.speed + 1):
					player.is_moving = True
					player.move()
			elif bg_x < 0 - player.speed - 1:
				player.is_moving = True
				move_background(player.speed, 0)
				if player.y < 700 + (player.speed + 1):
					player.y += player.angular_speed
			else:
				if player.x > 50 + player.width + player.speed + 1:
					player.is_moving = True
					player.x -= player.angular_speed
				if player.y < 700 - (player.speed + 1):
					player.is_moving = True
					player.y += player.angular_speed
		else:
			player.direction = "LEFT"			
			if player.x < 200:
				if bg_x < 0 - (player.speed + 1):
					player.is_moving = True
					move_background(+player.speed, 0)
				else:
					if player.x > 50 + player.width + player.speed + 1:
						player.is_moving = True
						player.x -= player.speed
			else:
				player.is_moving = True
				player.move()
	if key[pygame.K_d]:
		if key[pygame.K_w]:
			player.direction = "RIGHT UP"
			if player.x < 800:
				if player.y > 50 + player.width + player.speed + 1:
					player.is_moving = True
					player.move()
			elif bg_x > -800 + player.speed + 1:
				player.is_moving = True
				move_background(-player.speed, 0)
				if player.y > 50:
					player.y -= player.angular_speed
			else:
				if player.x < 950 - (player.width + player.speed + 1):
					player.is_moving = True
					player.x += player.angular_speed					
				if player.y > 50 + player.speed + 1:
					player.is_moving = True
					player.y -= player.angular_speed
		elif key[pygame.K_s]:
			player.direction = "RIGHT DOWN"
			if player.x < 800:
				if player.y < 700 + (player.speed + 1):
					player.is_moving = True
					player.move()
			elif bg_x > -800 + player.speed + 1:
				move_background(-player.speed, 0)
				player.is_moving = True
				if player.y < 700 + (player.speed + 1):
					player.y += player.angular_speed
			else:
				if player.x < 950 - (player.width + player.speed + 1):
					player.is_moving = True
					player.x += player.angular_speed					
				if player.y < 700 - (player.speed + 1):
					player.is_moving = True
					player.y += player.angular_speed
		else:
			player.direction = "RIGHT"
			if player.x > 800:
				if bg_x > -800 + player.speed + 1:
					player.is_moving = True
					move_background(-player.speed, 0)
				else:
					if player.x < 950 - (player.width + player.speed + 1):
						player.is_moving = True
						player.x += player.speed
			else:
				player.is_moving = True
				player.move()
	if key[pygame.K_SPACE]:
		if player.sprint_count > 0:
			player.sprinting = True
			player.speed = 10
			player.sprint_count -= 0.8
		else:
			player.sprinting = False
			player.speed = 3
	else:
		player.sprinting = False
		if player.sprint_count < 10:
			player.sprint_count += 0.05
		player.speed = 3


	for fish in fishes[:]:
		fish.move(player)
		if (fish.health > 0):
			fish.draw(win)
		else:
			del fish

	#draw bubbles
	for bubble in bubbles[:]:
		if bubble.Rect.colliderect(player.Rect):
			bubble.popped = True
		if bubble.to_delete:
			bubbles.remove(bubble) #replace
			bubbles.append(Bubble(x=random.randint(50, 950), y=random.randint(800, 1700), speed=random.randint(1, 3), size=random.randint(5, 16)))
			del bubble
		else:
			bubble.draw_bubble(win, level)
	
	player.draw(win)
	player.draw_stats(win)
	if tick - flash_tick < 100 and tick > 100:
		win.blit(too_far_text, (320, 200))
	pygame.display.update()

pygame.quit()