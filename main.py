#Made in 2023 by Bear BlinSchauer
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

#LOAD IMAGES
background_image = pygame.image.load("assets/img/background.jpg")
background_image = pygame.transform.smoothscale(background_image, screen.get_size())
#list of possible enemy images
enemy_image1 = pygame.image.load("assets/img/enemy.png")
enemy_image1 = pygame.transform.scale(enemy_image1, (100, 100))
enemy_images = [enemy_image1]

mixer.music.set_volume(0.7)
mixer.music.load("assets/sound/Automation.mp3")
mixer.music.play(-1)


laser_interval = 250
class new_player:
    def __init__(self,laser_interval):
        self.player_pos = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) +  (screen.get_height() / 3)*1.2)
        self.player_img = pygame.image.load("assets/img/player.png")
        self.player_img = pygame.transform.scale(self.player_img, (150, 150))
        self.laser_interval = laser_interval

        self.laser_flag = False

    #powerups may perhaps be able to change firing speed
    def change_interval(self, interval):
        self.laser_interval = interval
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
            lasers.append(new_laser(self.player_pos+(0,-50),True))
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

#True for left to right false for right to left
enemy_direction = False
#TODO FIX ENEMY UNALIGNMENT OVER TIME ISSUE
class new_enemy:
    def __init__(self, origin,img_source):
        #images
        self.enemy_image = img_source
        self.origin = origin
        self.enemy_pos = pygame.Vector2(origin)
        self.direction = True
    def switch_direction(self):
        self.direction = not self.direction
    def update(self):
        global enemy_direction
        if self.direction:
            self.enemy_pos.x += 100 * dt
        elif not self.direction:
            self.enemy_pos.x -= 100 * dt
        if self.enemy_pos.x < 0 or self.enemy_pos.x+self.enemy_image.get_width() > screen.get_width():
            enemy_direction = not enemy_direction

        #check edge collision
        #clamp the x values to the edges of the screen
        self.enemy_pos.x = max(min(screen.get_width(), self.enemy_pos.x), 0)

    def draw(self):
        pygame.draw.circle(screen, "red", self.enemy_pos, 10)
        screen.blit (self.enemy_image,self.enemy_pos)
#
class new_enemy_swarm:
    def __init__(self,row_count,columm_count,swarm_image):
        # enemy_row_count = 3
        # enemy_columm_count = 12
        self.swarm_image = swarm_image
        self.row_size = 100
        self.enemy_row_count = row_count
        self.enemy_columm_count = columm_count
        self.enemies = []
        for i in range (1,self.enemy_row_count+1):
            #divide screen width by the number of iteratiosn in the loop
            for f in range (1, self.enemy_columm_count+1):
                self.enemies.append(new_enemy((((screen.get_width()-screen.get_width()/self.enemy_columm_count)/self.enemy_columm_count*(f))-(screen.get_width()/self.enemy_columm_count),i*self.row_size-self.row_size),swarm_image))
        self.bounds = [pygame.Rect(0,0, 50,100),pygame.Rect(((screen.get_width()-screen.get_width()/self.enemy_columm_count)/self.enemy_columm_count*(self.enemy_row_count)),0, 50,100)]
    def update(self):
        # for i in self.enemies:
        #      i.update()
        if self.bounds[1].collidepoint(0,0) or self.bounds[1].collidepoint(screen.get_width(),0):
            for i in self.enemies:
                i.switch_direction()
        self.bounds[0] = self.bounds[0].move(100*dt,0)
    def draw(self):
        for i in self.enemies:
            i.draw()
        pygame.draw.rect(screen, "red",self.bounds[1],5)
#

lasers = []
laser_height = 50
laser_width = 15
laser_speed = 650
laser_sound = mixer.Sound("assets/sound/laser_sound.wav")
class new_laser:
    #origin = where to draw the laser
    #direction: boolean on which direction to go
    #True = bottom to top false = top to bottom
    def __init__(self, origin, direction):
        self.direction = direction
        self.origin = origin
        # self.laser_pos = pygame.Vector2(0,screen.get_height()-laser_height)
        self.laser_pos = pygame.Vector2(origin)
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
    global player
    global enemy_swarm
    player = new_player(laser_interval)
    enemy_swarm = new_enemy_swarm(6,10,enemy_images[0])

#
def cleanup():
    pass
#

def gameloop():
    player.update()
    enemy_swarm.update()
#

def render():
    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("black")
    screen.blit(background_image,(0,0))



    #draw and update lasers
    handle_lasers()

    #draw player
    player.draw()

    #draw enemies
    enemy_swarm.draw()

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
