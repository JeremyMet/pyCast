import pygame ;
from pygame.locals import * ;
import os, sys ;

import math ;

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0])) ;
os.chdir(APP_FOLDER) ;

__SCREEN_WIDTH__ = 640 ;
__SCREEN_HEIGHT__ = 480 ;

pygame.init() ;
fenetre = pygame.display.set_mode((__SCREEN_WIDTH__, __SCREEN_HEIGHT__), RESIZABLE)
fond = pygame.image.load("./media/img/background.jpg").convert()
pygame.key.set_repeat(400, 30)

class pyCast(object):

    def load_img(self):
        self.wall = pygame.image.load("./media/img/wall.gif").convert() ;
        self.wood = pygame.image.load("./media/img/wood.jpg").convert() ;
        self.grass = pygame.image.load("./media/img/grass.png").convert() ;

    def __init__(self, surface, level_array):
        self.surface = surface ;
        self.level_array = level_array ;
        self.go = True ;
        self.x_p = 0 ;
        self.y_p = 0 ;
        self.angle = 60 ;
        # "constants part"
        self.LEVEL_HEIGHT = len(level_array) ;
        self.LEVEL_WIDTH = len(level_array[0]) ;
        self.WALK_SPEED = 0.05 ;
        self.ROT_SPEED = 2 ;
        # engine constant part
        self.SCREEN_HEIGHT = 480 ;
        self.SCREEN_WIDTH = 640 ;
        self.FOV = 36 ;
        self.tile_dim = 64;
        self.s = 32 ; # screen distance
        self.h = __SCREEN_HEIGHT__ >> 1 ; # viewer height
        self.wall_size = 16 ;



    def ctrl(self):
        for event in pygame.event.get():
            dir = 0 ;
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                self.go = False  # On arrête la boucle
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.angle -= 3 ;
                elif event.key == K_RIGHT:
                    self.angle += 3 ;
                elif event.key == K_UP:
                    dir = 1 ;
                elif event.key == K_DOWN:
                    dir = -1 ;
                if dir:
                    tmp_x_p = self.x_p+dir*self.WALK_SPEED*math.cos(math.radians(self.angle)) ;
                    tmp_y_p = self.y_p+dir*self.WALK_SPEED*math.sin(math.radians(self.angle)) ;
                    scaled_tmp_x_p = int(tmp_x_p) ;
                    scaled_tmp_y_p = int(tmp_y_p) ;
                    if scaled_tmp_x_p >= 0 and scaled_tmp_x_p < self.LEVEL_WIDTH:
                        if not(self.level_array[int(self.y_p)][scaled_tmp_x_p]):
                            self.x_p = tmp_x_p ;
                    if scaled_tmp_y_p >= 0 and scaled_tmp_y_p < self.LEVEL_HEIGHT:
                        if not(self.level_array[scaled_tmp_y_p][int(self.x_p)]):
                            self.y_p = tmp_y_p ;

    def set_pos(self, x, y):
        self.x_p = x ;
        self.y_p = y ;


    def casting_engine(self):
        min_bound = self.angle-(self.FOV>>1) ;
        max_bound = self.angle+(self.FOV>>1) ;
        # print((min_bound, max_bound, self.angle)) ;
        self.angle = self.angle % 360;
        angle_step = self.FOV/__SCREEN_WIDTH__ ;
        # Cast engine
        x_screen = 0 ;
        raw_angle = -(self.FOV >> 1) ;
        angle = min_bound ;
        while min_bound <= angle < max_bound:
            # Cast the "Ray" tile per tile
            rangle = math.radians(angle) ;
            tan = math.tan(rangle)+0.000001 ; # avoid 0 division.
            invtan = 1/tan ;
            x_cast, y_cast = self.x_p,  self.y_p ;
            x_map, y_map = int(self.x_p), int(self.y_p) ;
            while(0 <= x_map < self.LEVEL_WIDTH) and (0 <= y_map < self.LEVEL_HEIGHT) and not(self.level_array[y_map][x_map]):
                reduced_angle = angle%360 ;
                if (0 <= reduced_angle < 90):
                    x_step = 1-math.modf(x_cast)[0] ;
                    y_step = 1-math.modf(y_cast)[0] ;
                elif (90 <= reduced_angle < 180):
                    x_step = -math.modf(x_cast)[0] ;
                    y_step = 1-math.modf(y_cast)[0];
                elif (180 <= reduced_angle < 270):
                    x_step = -math.modf(x_cast)[0] ;
                    y_step = -math.modf(y_cast)[0] ;
                else: # 270 <= angle < 360
                    x_step = 1-math.modf(x_cast)[0];
                    y_step = -math.modf(y_cast)[0] ;
                # Tersa's Trick  !!
                x_path = False ;
                if y_step == 0 : y_step = -1 ;
                if x_step == 0 : x_step = -1 ;
                if abs(tan) <= abs(y_step/x_step): # Tersa's Trick.
                    x_path = True ;
                    x_cast = x_cast + x_step ;
                    y_cast = y_cast + x_step*tan ;
                else:
                    y_cast = y_cast + y_step;
                    x_cast = x_cast + y_step * invtan;
                y_correct =-1 if (180 <= reduced_angle < 360) and not(x_path) else 0 ;
                x_correct =-1 if (90 <= reduced_angle < 270) and x_path else 0 ;
                x_map = int(x_cast)+x_correct ;
                y_map = int(y_cast)+y_correct ;
            ## Ray has been cast.


            ######################
            ## Displaying Walls ##
            ######################

            if (0 <= x_map < self.LEVEL_WIDTH) and (0 <= y_map < self.LEVEL_HEIGHT):
                current_block = self.level_array[y_map][x_map] ;
                dist = math.sqrt((x_cast-self.x_p)**2+(y_cast-self.y_p)**2)*math.cos(math.radians(raw_angle)) ; # cos avoids blow fish effect.
                if dist == 0: dist = 1 ;
                normalized_dist = 1-(dist/(self.LEVEL_WIDTH+self.LEVEL_HEIGHT))**2
                wall_height = int(self.s*self.wall_size/dist) ;
                if wall_height >= 2048: wall_height = 2048 ;
                y_screen_top = (__SCREEN_HEIGHT__ >> 1) - (wall_height >> 1) ;
                y_screen_bottom = (__SCREEN_HEIGHT__ >> 1) + (wall_height >> 1) ;
                if x_path:
                    x_texture = int(math.modf(y_cast)[0] * 256);
                else:
                    x_texture = int(math.modf(x_cast)[0] * 256);
                if current_block == 1:
                    column = self.wall.subsurface((x_texture, 0, 1, 256)).copy() ;
                elif current_block == 2:
                    column = self.wood.subsurface((x_texture, 0, 1, 256)).copy() ;
                column = pygame.transform.scale(column, (1, wall_height)) ;
                self.surface.blit(column, (x_screen, y_screen_top )) ;

            ######################
            ## Displaying Floor ##
            ######################

            x_delta = math.cos(math.radians(angle)) ;
            y_delta = math.sin(math.radians(angle)) ;
            for y_floor in range(y_screen_bottom+1, __SCREEN_HEIGHT__):
                dist = 2**8 / (y_floor - (__SCREEN_HEIGHT__ >> 1)) ;
                x_texture = (self.x_p + x_delta*dist)%1  ;
                y_texture = (self.y_p + y_delta*dist)%1 ;
                x_texture *= 256 ;
                y_texture *= 256 ;
                x_texture, y_texture = int(x_texture), int(y_texture) ;
                color = self.grass.get_at((x_texture, y_texture)) ;
                self.surface.set_at((x_screen, y_floor), color) ;
            #

            x_screen+=1 ;
            raw_angle+=angle_step ;
            angle+=angle_step ;








    def draw_grid(self):
        """
        :param: surface for the grid to be displayed.
        :param level_array: array that stores the current level (0 no wall, 1 wall).
        :param tile_dim: (int width, int height) : size of the primitive tile (that will be repeated to pave the grid)
        """
        color_white = (255, 255, 255) ;
        x_pos, y_pos = 0, 0 ;
        for line in level_array:
            for val in line:
                if val:
                    if val == 1:
                        wall_color = (127, 127, 127);
                    elif val == 2:
                        wall_color = (196, 128, 128);
                    elif val == 3:
                        wall_color = (0, 128, 196);

                    pygame.draw.rect(self.surface, wall_color, (x_pos, y_pos, self.tile_dim, self.tile_dim), 0) ;
                x_pos += self.tile_dim ;
            y_pos += self.tile_dim ;
            x_pos = 0 ;


level_array = [[1,2,2,2,1], [1,0,0,0,1], [1,0,0,0,1], [1, 0, 0, 0, 1], [1, 2, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]] ;

pyCastInst = pyCast(fenetre, level_array) ;
pygame.display.flip() ;
pyCastInst.set_pos(1.5 ,1.5) ;
pyCastInst.load_img() ;

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

while pyCastInst.go:
    fenetre.fill((0,0,0)) ;
    pyCastInst.ctrl() ;
    # pyCastInst.draw_grid()
    # pygame.draw.rect(pyCastInst.surface, (125,125, 125), [0, 240, 640, 480])
    pyCastInst.casting_engine();
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    pyCastInst.surface.blit(fps, (50, 50))
    clock.tick(30)
    pygame.display.flip();

