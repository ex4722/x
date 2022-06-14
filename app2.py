import pygame as pg
# Used for vector calcs
import math, random


'''NOTES
Screen is 0 top and 0 Left, grows positive down and right
https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
'''

# Screen Varibles 
SCREEN_RATIO = .5
SCREEN_WID = 2000
SCREEN_HIG = SCREEN_WID * SCREEN_RATIO

screen = pg.display.set_mode((SCREEN_WID, SCREEN_HIG))
pg.display.set_caption("TANKED")
FPS = 60
time = pg.time.Clock()

# Colors 
BASE = ( 0,43,54)
CYAN = ( 38,139,210)
RED  = ( 255,0,0)

# Game Varibles 
# TANK_SCALE = 1
# TURRET_SCALE = 1.5

TANK_SCALE = .5
TURRET_SCALE = .75

BALL_SCALE = .08
CAP = 36
GRAVITY = 9.81 /10
GAME_START = False
GDB  = True 


# GAME STATE 
SHOTS_LEFT = 0
CRATES_HIT = 0
# NEed more?
CRATE = True


pg.font.init()
FONT = pg.font.SysFont(None, 32)

explosion_images = []
for i in range(1,6):
    explosion_images.append ( pg.image.load(f"./images/explosion/exp{i}.png").convert_alpha())
print(explosion_images)

background_image = pg.image.load("./img/transparent PNG/Full-background.png")
background_image = pg.transform.scale(background_image, (SCREEN_WID, SCREEN_HIG) )


# Helper Function
# Writes text
def draw_text(text, color, xy):
    blob = FONT.render(text,True, color) 
    screen.blit(blob, xy)


# Redraw in each loop
def clean_bg():
    # screen.fill(BASE)
    screen.blit(background_image, (0,0))



def get_mouse():
    print(pg.mouse.get_pos())

# Math.sin takes radians 
def f_sin(degree):
    return (math.sin((math.pi / 180 )  * degree))

def f_cos(degree):
    return (math.cos((math.pi / 180 )  * degree))

class Button(pg.sprite.Sprite):
    def __init__(self, x,y,scale):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load("./img/buttons/black_button.png").convert_alpha()
        self.img = pg.transform.scale( img, (img.get_width() * scale , img.get_height() * scale))
        self.rect = self.img.get_rect()
        self.rect.center = ( x,y)
    def draw(self):
        screen.blit( self.img, self.rect) 
    def update(self):
        global GAME_START
        if ( self.rect.collidepoint(pg.mouse.get_pos())):
            print("COLLISON")
            if ( pg.mouse.get_pressed()[0]):
                GAME_START = True



# Game Classes 
class Tank(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        pg.sprite.Sprite.__init__(self)
        # Load img, gen rect for boundries, scale img
        img = pg.image.load("./images/tanks/outputfolder/tank_model_1_1_b.png").convert_alpha()
        # img = pg.image.load("/tmp/tank.png").convert_alpha()
        self.img = pg.transform.scale( img, (img.get_width() * TANK_SCALE , img.get_height() * TANK_SCALE))

        # self.rect = self.img.get_bounding_rect()   # PYGAME STUPID, FIX:find  -name "*.png" -exec convert {} -trim outputfolder/{} \;
        self.rect = self.img.get_rect()
        self.rect.center = ( x,y)

    def update(self):
        # Calls own functions, declutters the final code
        pass 
    def draw(self):
        # Img is graphical, rect is location
        screen.blit( self.img, self.rect) 
        # Debug, Prints hitboxes
        if GDB:
            pg.draw.rect(screen, RED, self.rect,2)
    def move(self):
        # Tank don't need to move
        pass

class Turret(pg.sprite.Sprite):
    # XY is for the left turret NOT center
    def __init__(self, x, y, color):
        pg.sprite.Sprite.__init__(self)
        self.angle = 0
        self.cannon_balls = 10100000

        # Load img, gen rect for boundries, scale img
        # img = pg.image.load("./images/tanks/outputfolder/tank_model_1_2_w1.png").convert_alpha()
        img = pg.image.load("./images/tanks/outputfolder/tank_model_1_3_w1.png").convert_alpha()
        # img = pg.image.load("/tmp/turret.png").convert_alpha()
        self.master_img = pg.transform.scale( img, (img.get_width() * TURRET_SCALE, img.get_height() * TURRET_SCALE))
        self.img = pg.transform.scale( img, (img.get_width() * TURRET_SCALE, img.get_height() * TURRET_SCALE))

        # Len of turret, used for ball spawning
        self.length = self.img.get_width() + 30
        self.rect = self.img.get_rect()
        self.rect.bottomleft = (x,y)

        # Anchors differ, left and right should be width of turret apart

        self.left_anchor = (x,y)
        # Left and right anchor changes by width of turret
        self.right_anchor = (x+ self.master_img.get_height()  , y)
        # Angle from master; NOT RELATIVE 

    def update(self):
        # Calls own functions, declutters the final code
        pass 
    def draw(self):
        # Img is graphical, rect is location
        screen.blit( self.img, self.rect) 
        if GDB:
            pg.draw.rect(screen, CYAN, self.rect,2)

    def set_origin(self):
        # Moving moves the top left corner only, change to center;; NM Change to top right
        pass
    # Relative Movements
    def move_turret(self, angle):
        self.angle = (self.angle + angle )% 180
        # Use delta XY for collision calcs, NO NEED THEIRS NO COLLISIONS
        # dx = 0; dy = 0
        self.img = pg.transform.rotozoom(self.master_img, self.angle, 1)
        if self.angle <= 90:
            self.rect = self.img.get_rect(bottomleft = self.left_anchor)
        else:
            self.rect = self.img.get_rect(bottomright = self.right_anchor)


    def move_turret_absolute(self, angle):
        if angle >= 180:
            return
        self.img = pg.transform.rotozoom(self.master_img, int(angle), 1)
        if angle <= 90:
            self.rect = self.img.get_rect(bottomleft = self.left_anchor)
        else:
            self.rect = self.img.get_rect(bottomright = self.right_anchor)



    # Left is 180, past 180 is rounded
    def get_angle(self):
        mousex, mousey = pg.mouse.get_pos()
        # resultx , resulty = mousex - self.rect.x , mousey - self.rect.y
        # resultx , resulty = self.rect.x - mousex ,self.rect.y -  mousey
        resultx , resulty = self.left_anchor[0] - mousex ,self.left_anchor[1] -  mousey
        # Angle in Radians, Need to convert
        # angle = ((180 / math.pi) * math.atan2(resultx, resulty) ) * -1 + 90 #UPSIDEDOWN
        # angle = ((180 / math.pi) * (math.atan2(resultx, resulty) ))    # Change x-y
        # Pygame coord plane screwed, grows downwards 
        angle = int(180 - ((180 / math.pi) * (math.atan2(resulty, resultx) )))

        # Can't shoot below 0
        if angle > 270:
            return 0
        if angle > 180:
            return 180
        return int(angle)

    def follow_mouse(self):
        self.move_turret_absolute(self.get_angle())


    def ball_y(self):
        # Uses Ax = A sin Theta
        return (f_sin(self.get_angle() ) * self.length)
    def ball_x(self):
        # Uses Ay = A cos Theta
        return (f_cos(self.get_angle() + 180) * self.length)

    def ball_cos(self):
        return (f_cos(self.get_angle() + 180) )

    def ball_sin(self):
        return (f_sin(self.get_angle() + 180) )

    def get_distance(self):
        mousex, mousey = pg.mouse.get_pos()
        return math.sqrt( (mousex - self.left_anchor[0])**2 +  (mousey - self.left_anchor[1])**2 )

    def shoot(self):
        if self.cannon_balls > 0:
            if self.get_angle() < 90:
                x = self.left_anchor[0] - self.ball_x()
                y = self.left_anchor[1] - self.ball_y() - (self.master_img.get_height() /2)
                # y = self.left_anchor[1] - self.ball_y()
            else:
                x = self.right_anchor[0] - self.ball_x()
                y = self.right_anchor[1] - self.ball_y() - self.master_img.get_height() /2

            # CAP at 300, 37 is max 45 degreee
            # ball = Cannon_balls( x,y, self.get_angle(), self.get_distance() / 18)

            ball = Cannon_balls( x,y, self.get_angle(), self.get_distance())
            # ball = Cannon_balls( x,y, self.get_angle(), 37 )

            balls_group.add(ball)
            self.cannon_balls -= 1
            # explosion = Explode( x,y )
            # explode_group.add(explosion)

            # Have explosin animation 

    def debug_dump(self):
        print(f"ANGLE {self.get_angle()} FORCE { self.get_distance()}")

        hypo_force = self.get_distance() if self.get_distance() < 25 * CAP else 25 * CAP
        x_cord = self.left_anchor[0] + (  hypo_force * f_cos(self.get_angle()) )
        pg.draw.line(screen, CYAN, self.left_anchor , ( x_cord, self.left_anchor[1]  ) )

        y_cord = self.left_anchor[1] -  ( hypo_force * f_sin(self.get_angle())  ) 
        pg.draw.line(screen, CYAN, self.left_anchor , ( self.left_anchor[0], (   y_cord)  )) 

        pg.draw.line(screen, CYAN, self.left_anchor , pg.mouse.get_pos() )


        draw_text( str(self.get_angle()), CYAN, pg.mouse.get_pos()   )

        draw_text( str("%.1f" % (hypo_force * f_cos(self.get_angle()))), CYAN, ( self.left_anchor[0] + hypo_force * f_cos(self.get_angle()) * .5 , self.left_anchor[1] )   )

        draw_text( str("%.1f" % (hypo_force * f_sin(self.get_angle()))), CYAN, ( self.left_anchor[0] -65, self.left_anchor[1] - ( hypo_force * f_sin(self.get_angle()) * .5  )   ))




class Cannon_balls(pg.sprite.Sprite):
    def __init__(self, x, y, angle, force ):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load("./images/bullet4.png").convert_alpha()
        self.image = pg.transform.scale( img, (img.get_width() * BALL_SCALE, img.get_height() * BALL_SCALE))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.angle = angle 
        self.direction = 1 if angle < 90 else -1

        #### CAP FORCE AT 300
        # CAPPED FORCE

        force /= 25
        if force > CAP:
            force = CAP

        # Velocity crap
        self.x_vel = (f_cos(angle) * force) * self.direction
        self.y_vel = -(f_sin(angle) * force)
        print(force)


    def update(self):
        if GDB:
            pg.draw.rect(screen, CYAN, self.rect,2)
        self.y_vel += GRAVITY
        # Direction matters
        dx  = self.x_vel * self.direction
        # Direction not matter
        dy  = self.y_vel

        self.rect.x += dx
        self.rect.y += dy

        if ( self.rect.y > 850):
            explosion = Explode( self.rect.x, self.rect.y )
            explode_group.add(explosion)
            self.kill()

        for c in crate_group:
            if pg.sprite.collide_rect(self, c):
                explosion = Explode( self.rect.x, self.rect.y )
                explode_group.add(explosion)
                self.kill()


class Explode(pg.sprite.Sprite):
    def __init__(self, x, y ):
        pg.sprite.Sprite.__init__(self)
        # Ticks for animation speed
        self.frame_index = 0
        self.tick_counter = 0
        self.image = explosion_images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        ticks_speed = 4
        self.tick_counter += 1

        if self.tick_counter > ticks_speed:
            self.tick_counter = 0
            self.frame_index += 1

            # 0 Based arrays :)
            if self.frame_index > len(explosion_images) -1:
                self.remove()
                self.kill()
            else:
                self.image = explosion_images[self.frame_index]


class Crate(pg.sprite.Sprite):
    def __init__(self, x,y,scale):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load("./img/crtes/Crate game assets/Crates etc/CrateSmall.png").convert_alpha()
        self.image = pg.transform.scale( img, (img.get_width() * scale , img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = ( x,y)
    def draw(self):
        screen.blit( self.image, self.rect) 


    def update(self):
        global CRATE, CRATES_HIT
        for blow in explode_group:
            if pg.sprite.collide_rect(self, blow):
                print("HIT")
                CRATE = True
                CRATES_HIT += 1
                self.remove()
                self.kill()

        for can in balls_group:
            if pg.sprite.collide_rect(self, can):
                CRATE = True
                CRATES_HIT += 1
                print("HIT")
                self.remove()
                self.kill()


balls_group = pg.sprite.Group()
explode_group = pg.sprite.Group()
crate_group = pg.sprite.Group()

tank_x = 150
tank_y = 850

tank1 = Tank(tank_x,tank_y,"yellow")
# Add a bit to the Y so anchor point ain't screwed up
turret1 = Turret( tank1.rect.midtop[0],  tank1.rect.midtop[1]+30,"yellow")

# crate = Crate( 400,tank_y, .3)
# crate_group.add(crate)
start_button = Button(  SCREEN_WID/2,SCREEN_HIG/2, .5 )


active = True


while active:
    time.tick(FPS)

    if GAME_START == False:
        clean_bg()
        # pg.draw.rect(screen, RED, [SCREEN_WID/2 -(300/2),SCREEN_HIG/2, 300, 200] )
        start_button.draw()
        start_button.update()
    else:

        if CRATE:
            CRATE = False
            x_addr =  tank_x +50 + ( SCREEN_WID - tank_x - 200) * random.uniform(0, 1)
            crate = Crate( x_addr , tank_y, .3)
            crate_group.add(crate)
            print(CRATES_HIT)


        clean_bg()
        tank1.draw()
        turret1.follow_mouse()
        turret1.draw()
        if (GDB):
            turret1.debug_dump()

        balls_group.draw(screen)
        balls_group.update()

        explode_group.draw(screen)
        explode_group.update()

        crate_group.draw(screen)
        crate_group.update()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # turret1.ball_y()
                # turret1.ball_x()
                # get_mouse()
                turret1.shoot()
            if event.unicode == "!":
                GDB = not GDB 
    pg.display.update()
