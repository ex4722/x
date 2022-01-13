import pygame as pg

# Create screen session
SC_WID = 1000 
SC_HIG = int(SC_WID * .7)
screen = pg.display.set_mode((SC_WID, SC_HIG))
pg.display.set_caption("HELLO WORLD")

# Frame limit
time = pg.time.Clock()
FPS = 20
back_color = ( 0,43,54)

# Update background to remove moving sprites
def clean_bg():
    screen.fill(back_color)

class turret( pg.sprite.Sprite):
    # XY original positions
    def __init__(self, x,y, scale, speed):
        pg.sprite.Sprite.__init__(self)

        self.speed = speed

        # Load im, get size, center size , Use size in blit
        img = pg.image.load("./img/tank_model_1_1_b.png")
        img = pg.image.load("./img/tank_model_1_2_w1.png")
        self.img = pg.transform.scale(img, ( img.get_width() * scale, img.get_height() * scale))
        self.rect = self.img.get_rect()
        self.rect.center = ( x,y)

    # Relative movement
    def move(self, coord):
        dx = self.rect.x + coord[0]
        dy = self.rect.y + coord[1]

        self.rect.x= dx
        self.rect.y= dy

    # Absolute movment
    def goto( self, coord):
        self.rect.x = coord[0] - self.originx
        self.rect.y = coord[1] - self.originy

    # Update sptires
    def draw(self):
        screen.blit(self.img, self.rect)

    # Sets center value to so go to can subtract from it
    def set_origin(self):
        self.rect = self.img.get_rect()
        self.originx = self.rect.centerx
        self.originx = self.rect.centerx
        self.originy = self.rect.centery

dog1 = turret(500,500,.5,2)

while True:
    time.tick(FPS)
    clean_bg()
    dog1.draw()

    for event in pg.event.get():
        if event == pg.QUIT:
            break
        if event.type == pg.KEYDOWN:
            print(pg.mouse.get_pos())
        if event.type == pg.MOUSEMOTION:
            dog1.set_origin()
            dog1.goto(pg.mouse.get_pos())



    pg.display.update()
# pg.quit()

