import pygame, time, random, math

pygame.init()

frame_rate = 60

screen_width, screen_height = 1000, 800
win = pygame.display.set_mode((screen_width, screen_height))
win.set_colorkey((0, 0, 0))


flash_font = pygame.font.SysFont("Helvetica", 22, bold=True)
too_far_text = flash_font.render("<!> You're too far away from the target! <!>", False, (82, 16, 16))
too_far_text_size = flash_font.size("<!> You're too far away from the target! <!>")


game_over_font = pygame.font.SysFont("Helvetica", 22, bold=True)
game_over_text = game_over_font.render("<!> You died! Game Over! <!>", False, (148, 42, 34))
game_over_text_size = game_over_font.size("<!> You died! Game Over! <!>")





clock = pygame.time.Clock()
background_image = {"sand":pygame.image.load("textures/bg.jpg").convert(), "deep":pygame.image.load("textures/deep.jpg").convert()}

#PLAYER
exp_for_level = {"1":100, "2":500, "3":1000, "4":2000, "5":5000, "6":10_000, "7":20_000, "8":30_000, "9":50_000, "10":100_000}
health_for_level = {"1":100, "2":200, "3":500, "4":1000, "5":1500, "6":2000, "7":2500, "8":3000, "9":3500, "10":4000}
power_for_level = {"1":20, "2":40, "3":50, "4":100, "5":150, "5":200, "7":300, "8":500, "9":700, "10":1000}
size_for_level = {"1":50}

#GREEN FISH
green_fish_sizes = {"1":35, "2":50, "3":60, "4":70, "5":80}
green_fish_power = {"1":10, "2":15, "3":30, "4":35, "5":40}
green_fish_health = {"1":50, "2":100, "3":300, "4":500, "5":600}
green_fish_exp = {"1":20, "2":40, "3":60, "4":70, "5":100}