import pygame, sys
from pygame import QUIT
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60 #speed of game

#define usefull colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 

#set up assets:art and sound
game_folder = os.path.dirname(__file__) #our project
img_folder = os.path.join(game_folder, "img")

#initialize pygame and screen
pygame.init()
pygame.mixer.init() #soundeffects of game
pygame.mixer.music.load("spaceship.wav")
pygame.mixer.music.play()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteorites fall down")
clock = pygame.time.Clock() #track the time
start = 6000 #for 1 minute
running = True

font_name = pygame.font.match_font('calibri')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x , y)
    surf.blit(text_surface, text_rect)

def show_go_screen(): 
        #screen.blit(background, background_rect)
        draw_text(screen, "Meteorites fall down", 44, WIDTH /2 , HEIGHT /4)
        draw_text(screen, "Try not to touch the meteorites, with arrow keys", 
                16, WIDTH /2 , HEIGHT /2)
        draw_text(screen, "Press an arrow key to start", 
                  16, WIDTH /2 , HEIGHT /2 * ( 3/4))
        pygame.display.flip()
        waiting = True
        while waiting:
         clock.tick(FPS)
         for event in pygame.event.get():
             if event.type == pygame.QUIT: #first the exit-event
                 pygame.quit()
                 sys.exit()
             if event.type == pygame.KEYUP:
                 waiting = False
# effect, geluid en snelheid
def show_next_screen(): 
        #screen.blit(background, background_rect)
        draw_text(screen, "Your score was: " + str(score1), 36, WIDTH /2 , HEIGHT /4)
        draw_text(screen, "CRASHED!", 
                52, WIDTH /2 , HEIGHT /2)
        pygame.display.flip()
        waiting = True
        while waiting:
         clock.tick(FPS) 
         for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               if event.type == pygame.KEYUP:
                   waiting = False


#define sprite objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,50)) #give new format
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = 18
        #####pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        self.rect.x = self.rect.x + self.speedx 
        self.rect.y = self.rect.y + self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
 
class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = meteor_img
        self.image_orig.set_colorkey(BLACK)
        self.image_orig = pygame.transform.scale(meteor_img, (50,50)) #give new format
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        ######pygame.draw.circle(self.image, BLUE, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width) #it has to come on the screen
        self.rect.y = random.randrange(-100, -40) #minus is above the screen placing
        self.speedy = random.randrange(1, 4) # slow and fast enemies
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8) #rotationspeed
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
 

    def update(self):
        self.rotate()
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -2 or self.rect.right > WIDTH + 5:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #randomize place for same meteorites
            self.rect.y = random.randrange(-100, -40) #y-as punt voor enemy
            self.speedy = random.randrange(2, 6) #randomize speed

    


#load all game graphics
background = pygame.image.load(os.path.join(img_folder, "achtergrong1.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "Naamloos2.ico")).convert()
meteor_img = pygame.image.load(os.path.join(img_folder, "Naamloos1.ico")).convert()
#sound_game = pygame.mixer.Sound(path.join(snd_dir, "spaceship.wav"))


#Game loop
game_over = False
game_start = True
running = True
while running:
    if game_start:
        show_go_screen() #show start  screen
        game_start = False #text will go
        #Sprite: objects that move around. make all update
        all_sprites = pygame.sprite.Group() 
        meteorites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        #all_sprites.add(meteorites)
        for i in range(8):
            m = Meteorite()
            all_sprites.add(m)
            meteorites.add(m)
            

    if game_over:
         show_next_screen()
         game_over = True


    clock.tick (FPS) #keep loop running at the right speed
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #first the exit-event
            running = False

    # Update: what need a sprite to do
    all_sprites.update()
   
    # Check if meteor hit the player
    hits = pygame.sprite.spritecollide(player, meteorites, False, pygame.sprite.collide_circle) #boolean tells if it has the get deleted
    if hits:
        #running = False
        game_over = True



    # Draw/render: draw the sprite into the screen
    screen.fill(BLACK)
    #screen.blit(background, background_rect)#old fashioned copy the pixels.
    all_sprites.draw(screen)
    start -= 1
    start1 = start // 100
    score = 6000 - start 
    score1 = score // 100
    draw_text(screen, str(start1), 18, WIDTH / 2, 10)
    draw_text(screen, "score:" + str(score1), 18, 400, 10)
    # Double buffering: after I draw, always do this last.
    pygame.display.flip()
    if start <= 0:
        show_next_screen()
        pygame.display.update()

    
pygame.quit()
