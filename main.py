#Made in 2023 by bear BlinSchauer
#see license for more info
import pygame
from pygame import mixer


#setup
pygame.init()
mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


mixer.music.set_volume(0.7)

#True for left to right false for right to left
enemy_direction = True

laser_interval = 250
class player:
    def __init__(self,laser_interval):
        self.player_pos = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) +  (screen.get_height() / 3)*1.2)
        self.player_img = pygame.image.load("player.png")
        self.player_img = pygame.transform.scale(self.player_img, (150, 150))
        self.laser_interval = laser_interval

        self.laser_flag = False
    def update(self):
        keys = pygame.key.get_pressed()
        # keys = pygame.key.()
        if keys[pygame.K_a]:
            self.player_pos.x -= 400 * dt
        if keys[pygame.K_d]:
            self.player_pos.x += 400 * dt

        #set timer for lasers and make new laser object when space key is pressed
        if keys[pygame.K_SPACE] and self.laser_flag == False:
            self.start_time = pygame.time.get_ticks()
            lasers.append(laser(self.player_pos+(0,-50),True))
            self.laser_flag = True
        if self.laser_flag == True and pygame.time.get_ticks() - self.start_time >= laser_interval:
            self.laser_flag = False
        #

        #check edge collision
        #clamp the x values to the edges of the screen
        self.player_pos.x = max(min(screen.get_width(), self.player_pos.x), 0)
    def draw(self):
        #draw player
        screen.blit(self.player_img,(self.player_pos.x-self.player_img.get_width()/2,self.player_pos.y - self.player_img.get_height()/2))
#

class enemy:
    def __init__(self, origin):
        #images
        self.enemy_image = pygame.image.load("enemy.png")
        self.enemy_image = pygame.transform.scale(self.enemy_image, (100, 100))
        self.origin = origin
        self.enemy_pos = pygame.Vector2(origin)
    def update(self):
        global enemy_direction
        if enemy_direction:
            self.enemy_pos.x += 100 * dt
            print("dun")
        elif not enemy_direction:
            print("switched")
            self.enemy_pos.x -= 100 * dt
        if self.enemy_pos.x <= 0 or self.enemy_pos.x >= screen.get_width():
            print("evaluated")
            enemy_direction = not enemy_direction

    def draw(self):
        screen.blit (self.enemy_image, self.enemy_pos)
#

lasers = []
laser_height = 50
laser_width = 15
laser_speed = 650
class laser:
    #origin = where to draw the laser
    #direction: boolean on which direction to go
    #True = bottom to top false = top to bottom
    def __init__(self, origin, direction):
        self.direction = direction
        self.origin = origin
        # self.laser_pos = pygame.Vector2(0,screen.get_height()-laser_height)
        self.laser_pos = pygame.Vector2(origin)
        laser_sound = mixer.Sound("laser_sound.wav")
        laser_sound.play()
    def update(self):
        if dir:
            self.laser_pos.y -= laser_speed *dt
        if not dir:
            self.laser_pos.y += laser_speed *dt
    def draw(self):
        pygame.draw.rect(screen, "red",(self.laser_pos.x,self.laser_pos.y,laser_width ,laser_height),0)
#
def handle_lasers():
    for i in lasers:
        i.update()
        i.draw()
        if i.laser_pos.y <= 0 or i.laser_pos.y >= screen.get_height():
            lasers.remove(i)
#

enemies = []
def startup():
    global player1
    player1 = player(laser_interval)

    enemy_row_count = 3
    enemy_columm_count = 12
    row_size = 100
    for i in range (1,enemy_row_count+1):
        #divide screen width by the number of iteratiosn in the loop
        for f in range (1, enemy_columm_count+1):
            enemies.append(enemy((((screen.get_width()-screen.get_width()/enemy_columm_count)/enemy_columm_count*(f))-(screen.get_width()/enemy_columm_count),i*row_size-row_size)))
#
def cleanup():
    pass
#

def gameloop():
    player1.update()
#

def render():
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for i in enemies:
        i.update()
        i.draw()


    #draw and update lasers
    handle_lasers()

    #draw player
    player1.draw()

    #draw enemies

    # flip() the display to put your work on screen
    pygame.display.flip()
#









startup()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#

    gameloop()
    render()
    dt = clock.tick(60) / 1000
#
cleanup()
pygame.quit()
