#Made 2023 by Bear BlinSchauer
#see license for more info
#dont judge my code lol
import random
import pygame
# from animation_logic import SpriteStripAnim
from pygame import mixer
from pygame import freetype
#setup
pygame.init()
GAME_FONT = freetype.Font("assets/DarumadropOne-Regular.ttf", 24)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
score = 0
score_multiplier = 1
lives = 3
score_bool = True

#LOAD IMAGES
background_image = pygame.image.load("assets/img/background.jpg")
background_image = pygame.transform.smoothscale(background_image, screen.get_size())
# explosion_image = pygame.image.load("assets/img/explosion.gif")
#list of possible enemy images
enemy_image1 = pygame.image.load("assets/img/enemy.png")
enemy_image1 = pygame.transform.scale(enemy_image1, (100, 100))
enemy_images = [enemy_image1]


mixer.music.set_volume(0.7)
mixer.music.load("assets/sound/Automation.mp3")
mixer.music.play(-1)

def new_button(Picture, coords, surface):
    image = pygame.image.load(Picture)
    image = pygame.transform.scale_by(image,.30)
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    return (image,imagerect)

laser_interval = 500
class new_player:
    def __init__(self,laser_interval):
        self.player_pos = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) +  (screen.get_height() / 3)*1.2)
        self.player_img = pygame.image.load("assets/img/player.png")
        self.player_img = pygame.transform.scale(self.player_img, (100, 100))
        self.laser_interval = laser_interval

        self.player_hitbox = pygame.Rect(self.player_pos.x-self.player_img.get_width()/2,self.player_pos.y - self.player_img.get_height()/2, self.player_img.get_width(), self.player_img.get_height())
        self.laser_flag = False

    #powerups may perhaps be able to change firing speed
    def change_interval(self, interval):
        self.laser_interval = interval

    def check_player_collisions(self):
        global player
        global lives
        for laser in lasers:
            if laser.laser_hitbox.colliderect(self.player_hitbox) and laser.direction == False:
                startup()
                lives -= 1
    
    def update(self):
        global enemy_swarm
        self.player_hitbox = pygame.Rect(self.player_pos.x-self.player_img.get_width()/2,self.player_pos.y - self.player_img.get_height()/2, self.player_img.get_width(), self.player_img.get_height())
        keys = pygame.key.get_pressed()
        
        self.check_player_collisions()
        # keys = pygame.key.()
        if keys[pygame.K_a]:
            self.player_pos.x -= 800 * dt
        if keys[pygame.K_d]:
            self.player_pos.x += 800 * dt

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
        if not enemy_swarm.enemies[0]:
            return
        self.player_pos.x = max(min(screen.get_width()-enemy_swarm.enemies[0][0].enemy_image.get_width(), self.player_pos.x), 0+enemy_swarm.enemies[0][0].enemy_image.get_width())
    def draw(self):
        #draw player
        screen.blit(self.player_img,(self.player_pos.x-self.player_img.get_width()/2,self.player_pos.y - self.player_img.get_height()/2))
        # pygame.draw.rect(screen,"white",self.player_hitbox,10)
    def __del__(self):
        pass
#

#self.direction True for left to right false for right to left
class new_enemy:
    def __init__(self, origin,img_source):
        #images
        self.enemy_image = img_source
        self.origin = origin
        self.enemy_pos = pygame.Vector2(origin)
        self.direction = True
        self.enemy_hitbox = pygame.Rect(self.origin[0],self.origin[1], self.enemy_image.get_width(),self.enemy_image.get_height())
    def switch_direction(self):
        self.direction = not self.direction
    def update(self):
        if self.direction:
            self.enemy_pos.x += 100 * dt
            self.enemy_hitbox = (self.enemy_pos.x,self.enemy_pos.y, self.enemy_image.get_width(),self.enemy_image.get_height())
        elif not self.direction:
            self.enemy_pos.x -= 100 * dt
            self.enemy_hitbox = (self.enemy_pos.x,self.enemy_pos.y, self.enemy_image.get_width(),self.enemy_image.get_height())
        # if self.enemy_pos.x < 0 or self.enemy_pos.x+self.enemy_image.get_width() > screen.get_width():
        #     enemy_direction = not enemy_direction

        if random.randint(1,500) == 5:
            lasers.append(new_laser(self.enemy_pos, False))

        #check edge collision
        #clamp the x values to the edges of the screen
        self.enemy_pos.x = max(min(screen.get_width(), self.enemy_pos.x), 0)
    def enemy_attack(self):
            lasers.append(new_laser(self.enemy_pos, False))

    def draw(self):
        screen.blit (self.enemy_image,self.enemy_pos)
        # pygame.draw.rect(screen,"blue", self.enemy_hitbox, 10)
    def __del__(self):
        global score
        global score_multiplier
        global score_bool
        if score_bool:
            score += 1 * score_multiplier
            print("enemy deleted but explosion animation not yet added")
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
        self.enemy_row_list =[]
        #construct a list of enemies based of the columms and rows passed
        for i in range (1,self.enemy_row_count+1):
            #divide screen width by the number of iteratiosn in the loop
            for f in range (1, self.enemy_columm_count+1):
                self.enemy_row_list.append(new_enemy((((screen.get_width()-screen.get_width()/self.enemy_columm_count)/self.enemy_columm_count*(f))-(screen.get_width()/self.enemy_columm_count),i*self.row_size-self.row_size),swarm_image))
            self.enemies.append(self.enemy_row_list)
            self.enemy_row_list = []

        #define hitbox size and location based on the elements inside of enemies list
        self.rect_size = (self.enemies[0][0].enemy_image.get_width(),self.enemies[0][0].enemy_image.get_height()*self.enemy_row_count)
        self.bounds = [pygame.Rect(self.enemies[0][0].enemy_pos.x,self.enemies[0][0].enemy_pos.y,self.rect_size[0],self.rect_size[1]),pygame.Rect(self.enemies[0][self.enemy_columm_count-1].enemy_pos.x,self.enemies[0][self.enemy_columm_count-1].enemy_pos.y,self.rect_size[0],self.rect_size[1])]


    def check_laser_collisions(self):
        for rows in self.enemies:
            for columm in rows:
                for laser in lasers:
                    if laser.laser_hitbox.colliderect(columm.enemy_hitbox) and laser.direction == True:
                        rows.remove(columm)
                        lasers.remove(laser)
    def update(self):
        #update the hitboxes for the edges based on the list
        for rows in self.enemies :
            if rows == []:
                self.enemies.remove(rows)
        if self.enemies == []:
            return(False)
        self.bounds = [pygame.Rect(self.enemies[0][0].enemy_pos.x,self.enemies[0][0].enemy_pos.y,self.rect_size[0],self.rect_size[1]),pygame.Rect(self.enemies[0][-1].enemy_pos.x,self.enemies[0][-1].enemy_pos.y,self.rect_size[0],self.rect_size[1])]
        # self.bounds = [self.bounds[0].move(10*dt,0),self.bounds[1].move(10*dt,0)]

        #detect if the side hitboxes touch the wall and update evey enemy in the enemies list
        if self.bounds[0].collidepoint(0,0) or self.bounds[1].collidepoint(screen.get_width(),0):
            for i in self.enemies:
                for f in i:
                    f.switch_direction()

        #call all of the update fuctions from within the enemy objects
        for i in self.enemies:
            for f in i:
                f.update()

        #run a for loop to check the hitboxes of enemies with lasers
        #enemies are deleted if they come in contact with laser
        self.check_laser_collisions()
        return(True)

    #draw function - draws all enemies in the swarm
    def draw(self):
        for i in self.enemies:
            for f in i:
                f.draw()

        #draws left and right hitboxes for the swarm
        # pygame.draw.rect(screen, "red",self.bounds[1],5)
        # pygame.draw.rect(screen, "red",self.bounds[0],5)
#

laser_height = 30
laser_width = 10
laser_speed = 1000
laser_sound = mixer.Sound("assets/sound/laser_sound.wav")
laser_sound.set_volume(0.3)
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
        self.laser_hitbox = pygame.Rect(self.laser_pos.x, self.laser_pos.y,laser_width,laser_height)
    def update(self):
        if self.direction:
            self.laser_pos.y -= laser_speed *dt
        if not self.direction:
            self.laser_pos.y += laser_speed *dt
        self.laser_hitbox = pygame.Rect(self.laser_pos.x, self.laser_pos.y,laser_width,laser_height)
    def draw(self):
        pygame.draw.rect(screen, "red",self.laser_hitbox,0)
#
def handle_lasers():
    for i in lasers:
        i.update()
        i.draw()
        if i.laser_pos.y <= 0 or i.laser_pos.y >= screen.get_height():
            lasers.remove(i)
#

#

def startup():
    global player
    global enemy_swarm
    global lasers
    global restart_button
    global score_bool
    score_bool = False
    restart_button = new_button("assets/img/retry_button.png",(screen.get_width(),screen.get_height()),screen)
    player = new_player(laser_interval)
    lasers = []
    enemy_swarm = new_enemy_swarm(2,10,enemy_images[0])
    score_bool = True
    # while True:
    #     print("waiting")
#
def cleanup():
    pass
#

def gameloop():
    global enemy_swarm
    global score_multiplier
    player.update()
    #make a new swarm at 0 enemies remaining
    if not enemy_swarm.update():
        swarm_columms = random.randint(5,15)
        swarm_rows = random.randint(2,4)
        enemy_swarm = new_enemy_swarm(swarm_rows,swarm_columms,enemy_images[0])
        score_multiplier *=2
def render():
    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("black")
    screen.blit(background_image,(0,0))



    #draw and update lasers
    handle_lasers()

    #draw player
    player.draw()

    text_surface, txt_rect = GAME_FONT.render("Score = " + str(score), (225, 225, 225))
    lives_surface, txt_rect = GAME_FONT.render("Lives = " + str(lives), (225,225,225))
    screen.blit(text_surface, (10, screen.get_height()-20))
    screen.blit(lives_surface, (screen.get_width()-100, screen.get_height()-20))

    #draw enemies
    enemy_swarm.draw()


    # screen.blit(explosion_image,(0,0))

    # flip() the display to put your work on screen
    pygame.display.flip()
#

def death_screen():
    #logic
    #draw
    global restart_button
    screen.blit(background_image,(0,0))



    score_txt, txt_rect = GAME_FONT.render("Your score was: " + str(score), (225,225,225))
    gameover_txt, txt_rect = GAME_FONT.render("Would you like to play again?", (225,225,225))
    screen.blit(score_txt, (screen.get_width()/2-gameover_txt.get_width()/2, (screen.get_height()/2-gameover_txt.get_height()/2) +20))
    screen.blit(gameover_txt, (screen.get_width()/2-gameover_txt.get_width()/2, screen.get_height()/2-gameover_txt.get_height()/2))
    restart_button = new_button("assets/img/retry_button.png",(screen.get_width()/2+gameover_txt.get_width()/4,screen.get_height()/2+50),screen)

    # draw everything to the screen
    pygame.display.flip()
#




startup()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if restart_button[1].collidepoint(mouse):
                startup()
                score = 0
                lives =3
        #code if button is pressed goes here

        if event.type == pygame.QUIT:
            running = False
#

    if lives > 0:
        gameloop()
        render()
    else:
        death_screen()

    dt = clock.tick(60) / 1000
#
cleanup()
pygame.quit()
