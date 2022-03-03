import pygame
import os
import time
import random
#this is a test
# from ship import Ship

# font
pygame.font.init()

WIDTH = 750
HEIGHT = 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Project")


# frtyh
# creating instances of a ship that all have their own coord and health
class Ship:
    def __init__(self, x, y, hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0  # bullet cooldown

    def draw(self, window):
        # pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50))
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = spaceship_yellow
        self.laser = laser_yellow
        self.mask = pygame.mask.from_surface(self.ship_img)  # collisin detection
        self.max_health = health


# changed os.path.imag (?) to direct path for assests

#  image assests
spaceship_red = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/ship_red.png")
spaceship_green = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/ship_green.png")
spaceship_blue = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/ship_blue.png")

# player ship
spaceship_yellow = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/ship_yellow.png")

# lasers
laser_red = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/laser_red.png")
laser_blue = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/laser_blue.png")
laser_green = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/laser_green.png")

laser_yellow = pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/laser_yellow.png")

# background
bg = pygame.transform.scale(pygame.image.load("C2_Coursework_Space_Invaders/venv/assets/background_black.png"),
                            (WIDTH, HEIGHT))
#enemy

class Enemy(Ship):
    COLOR_MAP = {
                "red": (spaceship_red, laser_red),
                "green": (spaceship_green, laser_green),
                "blue": (spaceship_blue, laser_blue)
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel



# game loop
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)  # CHANGE THIS FONT PLEASE LIBBY
    lost_font = pygame.font.SysFont("comicsans", 70)

    enemies = [] # stores enemies
    wave_length = 5 # new wave of enemies will be incremented
    enemy_vel = 5

    player_vel = 5

    player = Player(300,650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0


    # asd
    def redraw_window():
        win.blit(bg, (0, 0))  # redraw background from top left (full screen)
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", True, (255, 0, 0))  # red font
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))  # white font

        win.blit(lives_label, (10, 10))  # top left posistion ?
        win.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(win) # inhhereted draw method from ship :)

        # draws ma ship
        player.draw(win)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1,(255,255,255))
            win.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350)) # displays in centre


        pygame.display.update()

    while run:
        clock.tick(FPS)  # ensures consistent game speed
        redraw_window()

        if lives <= 0 or player.hp <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False # 3 sec timer quit the game
            else:
                continue

        if len(enemies) == 0:
            level += 1 # levels player up when all current enemies defeated
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
        # check if user quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()  # keeps checking if a key is being pressed
        if keys[pygame.K_q]:# quits game if q clicked
            run = False
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:  # down
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)



main()
